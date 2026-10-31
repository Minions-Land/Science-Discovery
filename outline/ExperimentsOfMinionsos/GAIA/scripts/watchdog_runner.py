#!/usr/bin/env python3
"""
Watchdog runner: launches GAIA baseline cells with parallelism + per-task timeouts +
runaway detection. Designed to recover from the 9318445f-style 'sandbox escape' without
hanging the whole batch.

Usage:
    python scripts/watchdog_runner.py --model haiku --mode single --skip-existing
    python scripts/watchdog_runner.py --model sonnet --mode level --level 2
    python scripts/watchdog_runner.py --model haiku --mode batch --stem mini_12
    python scripts/watchdog_runner.py --model sonnet --mode full

Watchdog policy per task:
    * hard timeout (default 900s = 15 min single, 5400s = 90 min batch/level/full)
    * transcript size cap (default 8 MB) -> kill if exceeded (sign of runaway)
    * stall detection: if transcript stops growing for N seconds, kill
    * runaway pattern detection: grep for 'run_v1.sh', 'scripts/' in transcript
"""
import argparse, json, os, signal, subprocess, sys, time
from pathlib import Path

ROOT = Path('/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GAIA')
RUN_V1 = ROOT / 'scripts' / 'run_v1.sh'
SESSIONS = ROOT / 'sessions' / 'v1-baseline-pull'
PROMPTS = ROOT / 'data' / 'prompts'

# Runaway markers - strings that should NEVER appear in a clean sandbox transcript.
# NOTE: 'ExperimentsOfMinionsos/GAIA/sessions' is intentionally NOT a marker, because
# the old v1 sandbox (pre-isolation) leaked that path in prompts of otherwise-clean runs.
# 'run_v1.sh' is the only definitive runaway signal (model executing our own runner).
RUNAWAY_MARKERS = [
    'run_v1.sh',
    'ExperimentsOfMinionsos/GAIA/scripts',
]

def base_for(mode: str, model_key: str) -> Path:
    if mode == 'single':
        return SESSIONS / 'single' / model_key
    if mode == 'batch':
        return SESSIONS / 'batch' / model_key
    if mode == 'level':
        return SESSIONS / 'level' / model_key
    if mode == 'full':
        return SESSIONS / 'full' / model_key
    raise ValueError(mode)

def task_dir(model_key: str, mode: str, stem: str):
    base = base_for(mode, model_key)
    if not base.exists():
        return None
    candidates = sorted(d for d in base.iterdir() if d.is_dir() and d.name.endswith('-' + stem))
    return candidates[-1] if candidates else None

def existing_clean_answer(model_key: str, mode: str, stem: str):
    d = task_dir(model_key, mode, stem)
    if d is None:
        return None
    ans = d / 'answers.txt'
    if not ans.exists() or ans.stat().st_size == 0:
        return None
    trans = d / 'transcript.jsonl'
    if trans.exists():
        sz = trans.stat().st_size
        if sz > 8 * 1024 * 1024:
            return None
        with open(trans, 'rb') as f:
            sample = f.read(min(sz, 2 * 1024 * 1024))
        if any(m.encode() in sample for m in RUNAWAY_MARKERS):
            return None
    return d

def launch_task(model_key: str, mode: str, stem: str):
    base = base_for(mode, model_key)
    base.mkdir(parents=True, exist_ok=True)
    before = set(p.name for p in base.iterdir() if p.is_dir())
    log_dir = ROOT / 'sessions' / 'v1-baseline-pull' / '_parallel_logs' / f'watchdog-{model_key}-{mode}-{int(time.time())}'
    log_dir.mkdir(parents=True, exist_ok=True)
    stdout_log = log_dir / f'{stem}.stdout'
    stderr_log = log_dir / f'{stem}.stderr'
    proc = subprocess.Popen(
        ['bash', str(RUN_V1), model_key, mode, stem],
        stdout=open(stdout_log, 'w'),
        stderr=open(stderr_log, 'w'),
        start_new_session=True,
        cwd=str(ROOT),
    )
    run_dir = None
    for _ in range(80):
        time.sleep(0.05)
        after = set(p.name for p in base.iterdir() if p.is_dir())
        new = after - before
        for n in new:
            if n.endswith('-' + stem):
                run_dir = base / n
                break
        if run_dir is not None:
            break
    return proc, run_dir, log_dir

def kill_process_group(proc, why: str):
    try:
        pgid = os.getpgid(proc.pid)
    except ProcessLookupError:
        return
    print(f'  [watchdog] KILLING pgid={pgid} (reason: {why})', file=sys.stderr, flush=True)
    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        return
    for _ in range(20):
        if proc.poll() is not None:
            return
        time.sleep(0.5)
    try:
        os.killpg(pgid, signal.SIGKILL)
    except ProcessLookupError:
        return

def check_task(proc, run_dir, started_at, hard_timeout, stall_timeout, max_transcript_mb,
               prev_size, prev_change_at):
    now = time.time()
    rc = proc.poll()
    if rc is not None:
        return ('done' if rc == 0 else 'crashed', prev_size, prev_change_at)
    if (now - started_at) > hard_timeout:
        return 'timeout', prev_size, prev_change_at
    if run_dir is None:
        return 'running', prev_size, prev_change_at
    trans = run_dir / 'transcript.jsonl'
    if not trans.exists():
        return 'running', prev_size, prev_change_at
    sz = trans.stat().st_size
    if sz > max_transcript_mb * 1024 * 1024:
        return 'runaway', sz, prev_change_at
    try:
        with open(trans, 'rb') as f:
            f.seek(max(0, sz - 200_000))
            tail = f.read()
        if any(m.encode() in tail for m in RUNAWAY_MARKERS):
            return 'runaway', sz, prev_change_at
    except OSError:
        pass
    if sz != prev_size:
        return 'running', sz, now
    if (now - prev_change_at) > stall_timeout:
        return 'stalled', sz, prev_change_at
    return 'running', sz, prev_change_at

def run_batch(model_key, mode, stems, parallelism, hard_timeout, stall_timeout,
              max_transcript_mb, skip_existing):
    summary = {
        'model': model_key, 'mode': mode, 'results': [],
        'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    }
    pending = list(stems)
    if skip_existing:
        keep = []
        for s in pending:
            d = existing_clean_answer(model_key, mode, s)
            if d:
                print(f'[skip-existing] {s} -> {d.name}', file=sys.stderr, flush=True)
                summary['results'].append({'stem': s, 'status': 'skipped-existing', 'run_dir': str(d)})
            else:
                keep.append(s)
        pending = keep
    print(f'[plan] model={model_key} mode={mode} pending={len(pending)} parallel={parallelism}',
          file=sys.stderr, flush=True)

    active = {}
    idx = 0
    total_planned = len(stems)
    while pending or active:
        while pending and len(active) < parallelism:
            stem = pending.pop(0)
            proc, run_dir, log_dir = launch_task(model_key, mode, stem)
            active[stem] = {
                'proc': proc, 'run_dir': run_dir,
                'started_at': time.time(),
                'prev_size': 0, 'prev_change_at': time.time(),
                'log_dir': log_dir,
            }
            idx += 1
            rd_name = run_dir.name if run_dir else '<pending>'
            print(f'[launch {idx}/{total_planned}] {stem} -> {rd_name}',
                  file=sys.stderr, flush=True)
        time.sleep(5)
        for stem, st in list(active.items()):
            if st['run_dir'] is None:
                base = base_for(mode, model_key)
                if base.exists():
                    for d in base.iterdir():
                        if d.is_dir() and d.name.endswith('-' + stem):
                            mt = d.stat().st_mtime
                            if mt >= st['started_at'] - 5:
                                st['run_dir'] = d
                                break
            status, sz, change_at = check_task(
                st['proc'], st['run_dir'], st['started_at'],
                hard_timeout, stall_timeout, max_transcript_mb,
                st['prev_size'], st['prev_change_at'],
            )
            st['prev_size'] = sz
            st['prev_change_at'] = change_at
            if status == 'running':
                continue
            run_dir = st['run_dir']
            ans_file = (run_dir / 'answers.txt') if run_dir else None
            n_lines = 0
            if ans_file and ans_file.exists():
                with open(ans_file) as f:
                    n_lines = sum(1 for _ in f)
            tr = (run_dir / 'transcript.jsonl') if run_dir else None
            tr_mb = round(tr.stat().st_size / 1024 / 1024, 2) if tr and tr.exists() else 0
            if status in ('done', 'crashed'):
                rc = st['proc'].returncode
                print(f'  [done] {stem} rc={rc} answers={n_lines} transcript={tr_mb}MB',
                      file=sys.stderr, flush=True)
                summary['results'].append({
                    'stem': stem, 'status': status, 'rc': rc,
                    'run_dir': str(run_dir) if run_dir else None,
                    'answer_lines': n_lines, 'transcript_mb': tr_mb,
                })
            else:
                kill_process_group(st['proc'], status)
                print(f'  [killed-{status}] {stem} answers={n_lines} transcript={tr_mb}MB',
                      file=sys.stderr, flush=True)
                summary['results'].append({
                    'stem': stem, 'status': f'killed-{status}',
                    'run_dir': str(run_dir) if run_dir else None,
                    'answer_lines': n_lines, 'transcript_mb': tr_mb,
                })
            del active[stem]
    summary['finished_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    return summary

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', required=True, choices=['haiku', 'sonnet'])
    ap.add_argument('--mode', required=True, choices=['single', 'batch', 'level', 'full'])
    ap.add_argument('--level', type=int, choices=[1, 2, 3])
    ap.add_argument('--stem', help='for mode=batch, the batch stem (e.g. mini_12)')
    ap.add_argument('--parallel', type=int, default=16)
    ap.add_argument('--single-timeout', type=int, default=900)
    ap.add_argument('--batch-timeout', type=int, default=5400)
    ap.add_argument('--stall-timeout', type=int, default=600)
    ap.add_argument('--max-transcript-mb', type=int, default=8)
    ap.add_argument('--skip-existing', action='store_true')
    ap.add_argument('--only', nargs='*', help='only run these stems (for retries)')
    ap.add_argument('--out', type=str)
    args = ap.parse_args()

    if args.mode == 'single':
        if args.only:
            stems = list(args.only)
        else:
            stems = [p.stem for p in sorted((PROMPTS / 'single').glob('*.md'))]
        hard_timeout = args.single_timeout
        parallel = args.parallel
    elif args.mode == 'batch':
        if not args.stem:
            print('--stem required for mode=batch', file=sys.stderr); sys.exit(2)
        stems = [args.stem]
        hard_timeout = args.batch_timeout
        parallel = 1
    elif args.mode == 'level':
        if args.level is None:
            print('--level required for mode=level', file=sys.stderr); sys.exit(2)
        stems = [f'level{args.level}']
        hard_timeout = args.batch_timeout
        parallel = 1
    else:  # full
        stems = ['all_165']
        hard_timeout = args.batch_timeout * 2
        parallel = 1

    print(f'[runner] stems={len(stems)} mode={args.mode} model={args.model} parallel={parallel} hard_timeout={hard_timeout}s',
          file=sys.stderr, flush=True)

    summary = run_batch(
        args.model, args.mode, stems,
        parallelism=parallel,
        hard_timeout=hard_timeout,
        stall_timeout=args.stall_timeout,
        max_transcript_mb=args.max_transcript_mb,
        skip_existing=args.skip_existing,
    )

    out_path = args.out
    if not out_path:
        out_dir = SESSIONS / '_summaries'
        out_dir.mkdir(parents=True, exist_ok=True)
        slug = f'{args.model}-{args.mode}'
        if args.mode == 'level':
            slug += f'-level{args.level}'
        elif args.mode == 'batch':
            slug += f'-{args.stem}'
        out_path = str(out_dir / f'{slug}-{int(time.time())}.json')
    Path(out_path).write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f'[runner] summary -> {out_path}', file=sys.stderr, flush=True)
    counts = {}
    for r in summary['results']:
        counts[r['status']] = counts.get(r['status'], 0) + 1
    print(json.dumps({
        'model': args.model, 'mode': args.mode,
        'n_total': len(stems),
        'by_status': counts,
        'summary_path': out_path,
    }, indent=2))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""v2-MinionsOS cell runner — one project per cell.

Usage:
  scripts/mos_v2_run_cell.py <model> <mode> <stem> [--timeout SECS]

Example:
  scripts/mos_v2_run_cell.py claude-haiku-4-5 batch postgrad-12

What it does, end-to-end:
  1. project_create(profile='hle-batch')  → port
  2. Seed input/questions.md (from data/v2/questions/<mode>/<stem>.md) +
     input/expected.json (from data/ground_truth_full.json, filtered to qids).
  3. Launch ./gru --print with GRU_MODEL / MINIONS_EXPERT_MODEL /
     MINIONS_CODER_MODEL pinned to <model>.  Bootstrap prompt tells Gru the
     port and the V2-style /goal: append FINAL ANSWER lines to
     branches/shared/submissions/answers.md until every qid is covered.
  4. Watch answers.md; once all qids have a FINAL ANSWER line (or timeout),
     SIGTERM the Gru process.
  5. mos_evaluate(port) → save score.
  6. Archive transcript + answers + eval under
     outline/ExperimentsOfMinionsos/GQPA-Diamond/sessions/v2-minionsos/<cell>/.

The MinionsOS monitor (started by ./gru) keeps any spawned Expert / Coder
tmux sessions alive; we don't manage them here.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(
    "/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GQPA-Diamond/minionsos-fork"
)
EXP = Path(
    "/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GQPA-Diamond"
)
DATA = EXP / "data"
QUESTIONS_ROOT = DATA / "v2" / "questions"
GT_FULL = DATA / "ground_truth_full.json"
GT_PG = DATA / "ground_truth.json"
SESSIONS_ROOT = EXP / "sessions" / "v2-minionsos"
NO_CODEX_MCP = REPO / ".mcp.no-codex.json"

FINAL_ANSWER_RE = re.compile(
    r"FINAL\s+ANSWER\s+([A-Za-z0-9_-]+)\s*[:\-]\s*([A-D])\b",
    re.IGNORECASE,
)
QID_HEADER_RE = re.compile(r"^##\s+([A-Za-z0-9_-]+)\b", re.MULTILINE)


def _now_iso() -> str:
    return datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")


def _qids_from_questions_md(text: str) -> list[str]:
    """Extract qids from '## <qid> (...)' headers."""
    return QID_HEADER_RE.findall(text)


def _build_expected(qids: list[str]) -> dict[str, str]:
    # Ground truth is split across two files: pg-* in ground_truth.json,
    # phys-*/chem-*/bio-* in ground_truth_full.json. Merge and look up.
    merged: dict[str, str] = {}
    if GT_PG.exists():
        merged.update(json.loads(GT_PG.read_text(encoding="utf-8")))
    if GT_FULL.exists():
        merged.update(json.loads(GT_FULL.read_text(encoding="utf-8")))
    out: dict[str, str] = {}
    for qid in qids:
        if qid not in merged:
            raise SystemExit(f"qid {qid!r} missing from ground-truth files")
        out[qid] = str(merged[qid]).strip().upper()
    return out


def _create_project(real_name: str, profile: str) -> int:
    """Invoke project_create in-process via uv-managed Python."""
    code = (
        "import json; from minions.lifecycle.project import project_create; "
        f"entry = project_create(real_name={real_name!r}, profile={profile!r}); "
        "print(entry.port)"
    )
    out = subprocess.check_output(
        ["uv", "run", "--project", str(REPO), "python", "-c", code],
        cwd=REPO,
        text=True,
    )
    port = int(out.strip().splitlines()[-1])
    return port


def _drain_gru_inbox_to_answers(port: int, answers_file: Path) -> int:
    """Rescue any FINAL ANSWER lines that Gru received but never wrote.

    Reads ``project_<port>/events/gru.jsonl`` (the per-agent EACN replay log
    written by the EACN3 backend) and extracts every ``FINAL ANSWER <qid>:
    <letter>`` line out of direct_message bodies. Appends any qids missing
    from the current answers file.

    This is a runner-side post-mortem step — it runs AFTER Gru's --print
    session exits, before the grader runs. It does not interfere with Gru
    while Gru is alive; it only compensates when Gru's loop didn't process
    every reply (common when Haiku-Gru spawns many Experts and burns context
    on the spawn phase).

    Returns the number of FINAL ANSWER lines newly appended to answers_file.
    """
    pdir = EXP / "projects" / f"project_{port}"
    inbox = pdir / "events" / "gru.jsonl"
    if not inbox.exists():
        return 0

    existing_text = answers_file.read_text(encoding="utf-8") if answers_file.exists() else ""
    already_have = {m.group(1) for m in FINAL_ANSWER_RE.finditer(existing_text)}

    added = 0
    new_lines: list[str] = []
    seen = set(already_have)
    for line in inbox.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        ev = d.get("event") or {}
        if ev.get("type") != "direct_message":
            continue
        body = str((ev.get("payload") or {}).get("content", ""))
        for m in FINAL_ANSWER_RE.finditer(body):
            qid, letter = m.group(1), m.group(2).upper()
            if qid in seen:
                continue
            seen.add(qid)
            new_lines.append(f"FINAL ANSWER {qid}: {letter}\n")
            added += 1

    if new_lines:
        with answers_file.open("a", encoding="utf-8") as f:
            f.write("\n# Runner fallback drain (Gru did not append these)\n")
            f.writelines(new_lines)
    return added


def _evaluate_project(port: int, reference_override: str | None = None) -> dict:
    code = (
        "import json; "
        "from minions.tools.evaluator import mos_evaluate, EvaluateArgs; "
        f"args = EvaluateArgs(port={port}, reference_override={reference_override!r}); "
        "print(json.dumps(mos_evaluate(args), default=str))"
    )
    out = subprocess.check_output(
        ["uv", "run", "--project", str(REPO), "python", "-c", code],
        cwd=REPO,
        text=True,
    )
    # Result is the last JSON object printed.
    for line in reversed(out.strip().splitlines()):
        line = line.strip()
        if line.startswith("{"):
            return json.loads(line)
    raise RuntimeError(f"evaluator returned no JSON:\n{out}")


def _project_paths(port: int) -> tuple[Path, Path, Path]:
    pdir = EXP / "projects" / f"project_{port}"
    input_dir = pdir / "input"
    answers_file = pdir / "branches" / "shared" / "submissions" / "answers.md"
    return pdir, input_dir, answers_file


def _seed_inputs(
    port: int,
    questions_md: Path,
    qids: list[str],
    expected_external_path: Path,
) -> Path:
    """Seed only questions.md inside the project. expected.json stays OUTSIDE.

    expected_external_path must already be writable (caller chooses the path,
    typically <run_dir>/expected.json under outline/.../sessions/).
    """
    _, input_dir, _ = _project_paths(port)
    input_dir.mkdir(parents=True, exist_ok=True)
    dst_q = input_dir / "questions.md"
    shutil.copyfile(questions_md, dst_q)

    expected = _build_expected(qids)
    expected_external_path.parent.mkdir(parents=True, exist_ok=True)
    expected_external_path.write_text(json.dumps(expected, indent=2), encoding="utf-8")

    # Pre-create submissions dir so Gru can append without a race.
    pdir, _, answers_file = _project_paths(port)
    answers_file.parent.mkdir(parents=True, exist_ok=True)
    if not answers_file.exists():
        answers_file.write_text("", encoding="utf-8")
    return dst_q


def _qid_domain_groups(qids: list[str], chunk_size: int = 8) -> list[tuple[str, list[str]]] | None:
    """Group qids by domain via the prefix convention, chunked for parallelism.

    Returns a list of ``(domain_slug, [qid, ...])`` tuples where a single
    top-level domain may produce multiple chunks (``physics-1``,
    ``physics-2``, ...) so each spawned Expert handles only ``chunk_size``
    questions. Empirically Haiku Experts stall above ~5 questions per brief,
    so chunking keeps each Expert's work tractable.

    Returns ``None`` for sets that cannot be partitioned by prefix alone (e.g.
    ``pg-NN`` postgrad qids that mix domains within the same prefix).
    """
    PREFIX_TO_DOMAIN = {
        "phys": "physics",
        "chem": "chemistry",
        "bio": "biology",
    }
    by_domain: dict[str, list[str]] = {}
    for qid in qids:
        prefix = qid.split("-", 1)[0].lower()
        if prefix not in PREFIX_TO_DOMAIN:
            return None
        by_domain.setdefault(PREFIX_TO_DOMAIN[prefix], []).append(qid)

    out: list[tuple[str, list[str]]] = []
    for domain in sorted(by_domain):
        qids_in_domain = by_domain[domain]
        if len(qids_in_domain) <= chunk_size:
            out.append((domain, qids_in_domain))
            continue
        # Chunk: domain-1, domain-2, ...
        for i in range(0, len(qids_in_domain), chunk_size):
            chunk_idx = (i // chunk_size) + 1
            slug = f"{domain}-{chunk_idx}"
            out.append((slug, qids_in_domain[i : i + chunk_size]))
    return out


def _bootstrap_prompt(port: int, qids: list[str] | None = None) -> str:
    pdir, input_dir, answers_file = _project_paths(port)
    groups = _qid_domain_groups(qids or [])

    base_top = (
        f"Project port: {port}\n"
        f"Workspace: {pdir}\n"
        f"Input questions: {input_dir / 'questions.md'}\n"
        f"Answers output: {answers_file}\n"
        "\n"
        "You are Gru — the control plane for this GPQA-Diamond batch project.\n"
        "**Do NOT answer questions yourself. Spawn the team and collect results.**\n"
        "**Do NOT use the `Task` or `Agent` tools — they are claude-code\n"
        "subagents and forbidden in this batch. Only `mos_spawn_role` /\n"
        "`mos_spawn_expert` create Roles.**\n"
        "\n"
    )

    constraints = (
        "Constraints:\n"
        "- Do NOT call `Task` or `Agent` (claude-code subagents).\n"
        "- Do NOT call `eacn3_create_task` yourself.\n"
        "- Do NOT read `input/expected.json` (the grader's reference).\n"
        "- All spawned Roles run on the same model you do (env-pinned).\n"
        "- **Polling**: `mos_await_events()` only (long-poll). Do NOT spam\n"
        "  `mos_get_events()`.\n"
        "- **Context**: prefer `mos_compact_context(reason=..., pending_plans=[])`\n"
        "  over `mos_reset_context`. Reset terminates this `--print` process\n"
        "  and there is no supervisor to restart Gru — the run will fail\n"
        "  with empty answers if you reset.\n"
    )

    # Deterministic-partition path (used when qids are prefixed phys/chem/bio).
    if groups is not None and qids:
        n_experts = len(groups)
        lines: list[str] = []
        lines.append(
            "Procedure:\n"
            "\n"
            "1. Spawn the standing Roles:\n"
            '   `mos_spawn_role(project_port=<port>, role="noter")`\n'
            '   `mos_spawn_role(project_port=<port>, role="ethics")`\n'
            "\n"
            f"2. Spawn EXACTLY {n_experts} Experts. The qid partition below\n"
            "   is pre-computed; do NOT re-derive it from the file. Each\n"
            "   Expert handles a small chunk so Haiku-Expert can finish\n"
            "   within its context budget. For each Expert, call\n"
            "   `mos_spawn_expert` with the provided args verbatim.\n"
            "\n"
        )
        for domain, qid_list in groups:
            qid_str = ", ".join(qid_list)
            lines.append(f"   ### Expert: {domain} ({len(qid_list)} qids)\n\n")
            lines.append(
                "   ```json\n"
                "   {\n"
                f'     "project_port": {port},\n'
                f'     "domain": "{domain}",\n'
                f'     "init_brief": "Answer the following GPQA qids by reading '
                f'`{input_dir / "questions.md"}`: {qid_str}. For each qid, send '
                f'one direct EACN message to the `gru` agent via '
                f'`eacn3_send_message` with the body containing exactly: '
                f'FINAL ANSWER <qid>: <letter> (A, B, C, or D). Brief reasoning '
                f'before that line is fine. One message per qid. Do NOT use '
                f'eacn3_create_task. Do NOT use eacn3_submit_bid."\n'
                "   }\n"
                "   ```\n\n"
            )

        lines.append(
            "3. Wait for replies via `mos_await_events()` on your own queue\n"
            "   (you are the `gru` agent). Loop. Use the long-poll wrapper.\n"
            "\n"
            "4. As each Expert direct_message reply arrives, append the\n"
            "   `FINAL ANSWER <qid>: <letter>` line to the answers file via\n"
            "   Bash echo or Edit. One line per qid; duplicates are fine\n"
            "   (the grader takes the last one).\n"
            "\n"
            "5. If an Expert is silent for over 5 minutes, nudge it via\n"
            "   `eacn3_send_message(to.agent_id=<expert-agent-id>, content=\n"
            "   'Reminder: please answer your qids and reply with FINAL ANSWER\n"
            "   lines.')` — single direct message.\n"
            "\n"
            "6. Stop when the answers file has one FINAL ANSWER line for every\n"
            "   qid in the set, OR when you've nudged each silent Expert at\n"
            "   least twice and have collected what you can.\n"
            "\n"
        )
        return base_top + "".join(lines) + constraints

    # Fallback — Gru decides the roster (used for pg-NN postgrad mix).
    return base_top + (
        "Procedure:\n"
        "\n"
        "1. Spawn the standing Roles:\n"
        '   `mos_spawn_role(project_port=<port>, role="noter")`\n'
        '   `mos_spawn_role(project_port=<port>, role="ethics")`\n'
        "\n"
        "2. Read `input/questions.md`. Each header is `## <qid> (<Domain> /\n"
        "   <Subdomain>)`. List every qid and its top-level domain. Group by\n"
        "   domain or specialty as you see fit (one Expert per top-level domain\n"
        "   is a sensible default).\n"
        "\n"
        "3. For each Expert you decide to spawn, call `mos_spawn_expert` with a\n"
        "   **short** `init_brief` (under ~400 chars) that lists ONLY the qids\n"
        "   and tells the Expert to read the questions from the filesystem.\n"
        "   Example call shape (single tool call, args as a proper JSON object\n"
        "   — NOT as a string):\n"
        "\n"
        "   ```json\n"
        "   {\n"
        f'     "project_port": {port},\n'
        '     "domain": "molecular-biology",\n'
        '     "init_brief": "Answer qids pg-01, pg-07, pg-09 from\n'
        f"      `{input_dir / 'questions.md'}` (read the file). For each\n"
        "       qid, send ONE direct EACN message to the `gru` agent via\n"
        "       eacn3_send_message containing exactly this line as the body:\n"
        "       FINAL ANSWER <qid>: <letter>\n"
        "       where <letter> is A, B, C, or D. Brief reasoning before that\n"
        "       line is fine. One direct_message per qid. Do NOT use\n"
        "       eacn3_create_task. Do NOT use eacn3_submit_bid. Direct\n"
        '       send_message only."\n'
        "   }\n"
        "   ```\n"
        "\n"
        "   If a `mos_spawn_expert` call fails, do NOT fall back to\n"
        "   `Agent`/`Task`. Just retry the call with proper args.\n"
        "\n"
        "4. Wait for replies via `mos_await_events()` on your own queue (you\n"
        "   are the `gru` agent). Loop until done.\n"
        "\n"
        "5. As each reply arrives, extract the `FINAL ANSWER <qid>: <letter>`\n"
        "   line and append it to the answers file. One line per qid.\n"
        "\n"
        "6. Stop when every qid has an answer. Nudge silent Experts via\n"
        "   `eacn3_send_message` if needed.\n"
        "\n"
    ) + constraints


def _launch_gru(
    *,
    model: str,
    prompt: str,
    transcript: Path,
    stderr_log: Path,
    project_port: int,
) -> subprocess.Popen:
    env = os.environ.copy()
    env["GRU_MODEL"] = model
    env["MINIONS_EXPERT_MODEL"] = model
    env["MINIONS_CODER_MODEL"] = model
    env["MINIONS_NOTER_MODEL"] = model
    env["MINIONS_ETHICS_MODEL"] = model
    # Gru-as-ceiling rule: every spawned Role uses the same model as Gru
    # (Haiku-Gru → all Haiku; Sonnet-Gru → all Sonnet, never stronger).
    env["MINIONS_PROJECT_PORT"] = str(project_port)
    # Pin MCP config to the no-codex variant so neither Gru nor any spawned
    # Role / subagent can reach Codex GPT-5. Honoured by the fork's
    # ./gru launcher (--mcp-config) and by role_launcher (default mcp).
    env["MINIONS_MCP_CONFIG"] = str(NO_CODEX_MCP)
    # Disable browser auto-open and viz prompts.
    env["GRU_VIZ_OPEN"] = "0"

    cmd = [
        str(REPO / "gru"),
        "--print",
        "--output-format", "stream-json",
        "--include-partial-messages",
        "--verbose",
        prompt,
    ]
    f_out = transcript.open("w", encoding="utf-8")
    f_err = stderr_log.open("w", encoding="utf-8")
    proc = subprocess.Popen(
        cmd,
        cwd=REPO,
        env=env,
        stdout=f_out,
        stderr=f_err,
        # New session so we can SIGTERM the whole group cleanly.
        start_new_session=True,
    )
    return proc


def _watch_until_complete(
    *,
    answers_file: Path,
    expected_qids: set[str],
    proc: subprocess.Popen,
    timeout_s: int,
    poll_s: float = 2.0,
) -> tuple[set[str], bool]:
    """Poll answers_file until every expected qid has a FINAL ANSWER.

    Returns (covered_qids, hit_timeout).
    """
    deadline = time.time() + timeout_s
    covered: set[str] = set()
    while True:
        if proc.poll() is not None:
            # Gru exited on its own (V2-style stop). Re-read once and return.
            text = answers_file.read_text(encoding="utf-8") if answers_file.exists() else ""
            covered = {m.group(1) for m in FINAL_ANSWER_RE.finditer(text)} & expected_qids
            return covered, False
        if answers_file.exists():
            text = answers_file.read_text(encoding="utf-8")
            covered = {m.group(1) for m in FINAL_ANSWER_RE.finditer(text)} & expected_qids
            if covered == expected_qids:
                # All answered — give Gru ~5s to flush its turn, then SIGTERM.
                time.sleep(5)
                _terminate(proc)
                return covered, False
        if time.time() >= deadline:
            print(f"[runner] WALL-CLOCK TIMEOUT at {timeout_s}s — terminating Gru", file=sys.stderr)
            _terminate(proc)
            text = answers_file.read_text(encoding="utf-8") if answers_file.exists() else ""
            covered = {m.group(1) for m in FINAL_ANSWER_RE.finditer(text)} & expected_qids
            return covered, True
        time.sleep(poll_s)


def _terminate(proc: subprocess.Popen) -> None:
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        pass
    try:
        proc.wait(timeout=20)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("model", help="e.g. claude-haiku-4-5 / claude-sonnet-4-6")
    ap.add_argument("mode", choices=["batch", "domain", "full"])
    ap.add_argument("stem", help="question file stem under data/v2/questions/<mode>/")
    ap.add_argument(
        "--timeout",
        type=int,
        default=1800,
        help="Wall-clock cap (seconds). Default 1800 = 30 min.",
    )
    args = ap.parse_args()

    questions_md = QUESTIONS_ROOT / args.mode / f"{args.stem}.md"
    if not questions_md.exists():
        print(f"[runner] question file not found: {questions_md}", file=sys.stderr)
        return 2

    qids = _qids_from_questions_md(questions_md.read_text(encoding="utf-8"))
    if not qids:
        print(f"[runner] no qids parsed from {questions_md}", file=sys.stderr)
        return 2
    print(f"[runner] parsed {len(qids)} qids from {questions_md.name}")

    model_short = args.model.replace("claude-", "").replace("-4-5", "").replace("-4-6", "")
    run_id = _now_iso()
    cell_name = f"{model_short}-{args.stem}"
    real_name = f"mos-v2-{cell_name}-{run_id.lower()}"
    out_dir = SESSIONS_ROOT / cell_name / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    transcript = out_dir / "transcript.jsonl"
    stderr_log = out_dir / "stderr.log"

    print(f"[runner] creating project (profile=hle-batch, name={real_name})")
    port = _create_project(real_name=real_name, profile="hle-batch")
    print(f"[runner] port={port}")

    # expected.json lives OUTSIDE the project tree so subagents (Task / codex
    # sandbox) running with cwd=project can't read it. The evaluator's
    # answer_grader_batch enforces this with a path guard.
    expected_external = out_dir / "expected.json"
    print(f"[runner] seeding inputs ({len(qids)} qids); expected.json -> {expected_external}")
    _seed_inputs(port, questions_md, qids, expected_external)
    _, _, answers_file = _project_paths(port)

    meta = {
        "run_id": run_id,
        "variant": "v2-minionsos",
        "mode": args.mode,
        "stem": args.stem,
        "model": args.model,
        "port": port,
        "real_name": real_name,
        "qids": qids,
        "timeout_s": args.timeout,
        "questions_file": str(questions_md),
        "answers_file": str(answers_file),
        "started_utc": datetime.now(tz=UTC).isoformat(),
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    prompt = _bootstrap_prompt(port, qids=qids)
    print("[runner] launching ./gru --print")
    proc = _launch_gru(
        model=args.model,
        prompt=prompt,
        transcript=transcript,
        stderr_log=stderr_log,
        project_port=port,
    )
    print(f"[runner] gru pid={proc.pid}; watching {answers_file}")

    covered, hit_timeout = _watch_until_complete(
        answers_file=answers_file,
        expected_qids=set(qids),
        proc=proc,
        timeout_s=args.timeout,
    )
    print(f"[runner] covered {len(covered)}/{len(qids)}  timeout={hit_timeout}")

    # Drain Gru's EACN inbox for FINAL ANSWER lines that didn't make it to
    # answers.md (e.g. Haiku-Gru ran out of context after spawning many
    # Experts and never processed Expert replies). External rescue, doesn't
    # interfere with Gru while alive.
    rescued = _drain_gru_inbox_to_answers(port, answers_file)
    if rescued:
        print(f"[runner] rescued {rescued} FINAL ANSWER lines from Gru inbox")
        # Recompute coverage so meta.json reflects the rescue.
        if answers_file.exists():
            text = answers_file.read_text(encoding="utf-8")
            covered = {m.group(1) for m in FINAL_ANSWER_RE.finditer(text)} & set(qids)

    # Run the grader regardless — partial answers still produce a score.
    print("[runner] running mos_evaluate ...")
    try:
        eval_result = _evaluate_project(port, reference_override=str(expected_external))
    except Exception as exc:  # noqa: BLE001 — surface evaluator failures
        eval_result = {"error": str(exc)}
        print(f"[runner] evaluator FAILED: {exc}", file=sys.stderr)
    (out_dir / "eval.json").write_text(json.dumps(eval_result, indent=2), encoding="utf-8")

    # Archive the answers file alongside transcript so future analysis is self-contained.
    if answers_file.exists():
        shutil.copyfile(answers_file, out_dir / "answers.md")

    finished_meta = dict(meta)
    finished_meta["finished_utc"] = datetime.now(tz=UTC).isoformat()
    finished_meta["covered"] = sorted(covered)
    finished_meta["hit_timeout"] = hit_timeout
    finished_meta["eval"] = eval_result
    (out_dir / "meta.json").write_text(
        json.dumps(finished_meta, indent=2), encoding="utf-8"
    )

    print(f"[runner] done → {out_dir}")
    if isinstance(eval_result, dict):
        score = eval_result.get("score")
        verdict = eval_result.get("verdict")
        details = eval_result.get("details") or {}
        print(
            f"[runner] verdict={verdict} score={score} "
            f"correct={details.get('correct')}/{details.get('total')}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

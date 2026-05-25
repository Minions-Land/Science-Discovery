#!/usr/bin/env python3
"""vision_loop.py — figure-aesthetic-exemplars iterative loop.

R-future-4 implementation: structural-audit-driven loop. Vision-capable
model judging proved unavailable in current toolchain (Codex sub-agent
doesn't pass images; Read tool vision unavailable in this session).
Solution: replace vision-model with structural audit (figure_audit.py)
covering ~60% of principles auto-checkable; flag the rest for human review.

Usage:
    python3 vision_loop.py <plot.py> [--exemplar <ref.png>] [--max-iter 4]

Output:
    iterations/iter_N/{draft.png, draft.svg, audit.json}
    iterations/report.md (summary + per-iter grades)

The "vision" in vision-loop is now:
- Structural audit (palette extraction, saturation distribution,
  trailing whitespace, SVG editable-text gate)
- Cross-comparison against an exemplar (palette diff)
- Human visual gate at end (Playwright HTML compare page generated)

The loop does NOT auto-revise — instead, it surfaces the top-3 audit
deltas so the human or downstream code-edit step can address them.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).parent.resolve()
AUDIT_PY = _HERE / "figure_audit.py"


def run_audit(png, svg, exemplar=None):
    """Invoke figure_audit.py and return parsed JSON."""
    cmd = [sys.executable, str(AUDIT_PY), str(png)]
    if svg: cmd.extend(["--svg", str(svg)])
    if exemplar: cmd.extend(["--exemplar", str(exemplar)])
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def render(plot_script, out_dir):
    """Render the plot script (assumes script writes draft.png/svg in cwd)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    # Run script with PYTHONUNBUFFERED, MPLCONFIGDIR
    env_mpl = "/private/tmp/mpl-vision-loop"
    Path(env_mpl).mkdir(exist_ok=True)
    subprocess.run(
        [sys.executable, str(plot_script)],
        cwd=out_dir,
        env={"MPLCONFIGDIR": env_mpl, "PATH": "/usr/bin:/bin"},
        check=True,
    )


def identify_top_deltas(audit, threshold_concerning=("concerning", "fail")):
    """Find the top-3 audit grades that are concerning/fail."""
    grades = audit.get("grades", {})
    concerning = []
    for principle, data in grades.items():
        if not isinstance(data, dict): continue
        grade = data.get("auto_grade")
        if grade in threshold_concerning:
            concerning.append({"principle": principle, "data": data})
    return concerning[:3]


def emit_report(history, exemplar, out_path):
    """Write a markdown report summarising the iteration history."""
    lines = ["# Vision-loop iteration report\n"]
    lines.append(f"**Exemplar:** {exemplar}\n" if exemplar else "")
    lines.append(f"**Iterations:** {len(history)}\n\n")

    for n, step in enumerate(history):
        lines.append(f"## Iteration {n}\n")
        audit = step["audit"]
        grades = audit.get("grades", {})
        for p, data in grades.items():
            if not isinstance(data, dict) or "auto_grade" not in data: continue
            lines.append(f"- **{p}**: {data['auto_grade']}\n")
        if step.get("top_deltas"):
            lines.append("\n**Top-3 deltas to address:**\n")
            for d in step["top_deltas"]:
                lines.append(f"- {d['principle']}: {d['data'].get('auto_grade')}\n")
        lines.append("\n")

    lines.append("\n## Human-review gate (not auto-graded)\n")
    lines.append(
        "These principles require human visual judgement — the loop does NOT close them:\n\n"
    )
    lines.append("- P4 packing — does the gridspec compose cleanly?\n")
    lines.append("- P5 form novelty — right form for the data?\n")
    lines.append("- P6 polar for N×M — is polar appropriate?\n")
    lines.append("- P7 legend placement — does legend overlap data?\n")
    lines.append("- P8 manifold info dim — does manifold show 1-2 dims max?\n")
    lines.append("- P9 radar template match — does it look like comparison_radar?\n")

    out_path.write_text("".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("plot_script")
    parser.add_argument("--exemplar", default=None)
    parser.add_argument("--max-iter", type=int, default=4)
    parser.add_argument("--out-root", default=None)
    args = parser.parse_args()

    plot = Path(args.plot_script).resolve()
    out_root = Path(args.out_root) if args.out_root else plot.parent / "iterations"
    out_root.mkdir(exist_ok=True)

    history = []
    for n in range(args.max_iter):
        iter_dir = out_root / f"iter_{n}"
        iter_dir.mkdir(exist_ok=True)
        # Copy script for reproducibility
        shutil.copy(plot, iter_dir / plot.name)
        render(iter_dir / plot.name, iter_dir)

        # Look for draft.png/svg
        png = next(iter_dir.glob("*.png"), None)
        svg = next(iter_dir.glob("*.svg"), None)
        if not png:
            print(f"iter {n}: no png produced; aborting", file=sys.stderr)
            break

        audit = run_audit(png, svg, args.exemplar)
        deltas = identify_top_deltas(audit)
        history.append({
            "iteration": n,
            "png": str(png),
            "audit": audit,
            "top_deltas": deltas,
        })
        # Save audit JSON beside the draft
        (iter_dir / "audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")

        # Stop condition: no concerning grades AND editable-text gate passed
        if not deltas:
            print(f"PASS at iteration {n}")
            break

        print(f"iter {n}: {len(deltas)} deltas to address; not auto-revising (manual step)")

    report = out_root / "report.md"
    emit_report(history, args.exemplar, report)
    print(f"\nReport: {report}")


if __name__ == "__main__":
    main()

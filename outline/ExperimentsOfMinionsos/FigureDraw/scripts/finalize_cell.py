#!/usr/bin/env python3
"""Finalize a FigureDraw cell: append finish metadata to meta.json."""
import json
import pathlib
import sys
from datetime import UTC, datetime

if len(sys.argv) != 3:
    print("usage: finalize_cell.py <out_dir> <exit_code>", file=sys.stderr)
    sys.exit(2)

out_dir = pathlib.Path(sys.argv[1])
exit_code = int(sys.argv[2])

meta_path = out_dir / "meta.json"
m = json.loads(meta_path.read_text(encoding="utf-8"))
m["finished_utc"] = datetime.now(tz=UTC).isoformat()
m["exit_code"] = exit_code

ws = out_dir / "workspace"
produced = sorted(f.name for f in ws.iterdir() if f.is_file())
m["produced"] = produced
m["has_figure_pdf"] = (ws / "figure.pdf").exists()
m["has_figure_png"] = (ws / "figure.png").exists()
m["has_figure_svg"] = (ws / "figure.svg").exists()
m["has_caption"] = (ws / "caption.tex").exists()
m["has_script"] = any((ws / f"gen_figure.{ext}").exists() for ext in ("py", "R", "r"))
meta_path.write_text(json.dumps(m, indent=2), encoding="utf-8")
print(f"[finalize] {out_dir.name}: produced={produced}")

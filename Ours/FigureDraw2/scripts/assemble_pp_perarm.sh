#!/bin/bash
# Assemble paper-page inputs per arm. Each arm pulls its own grouped-bar / line-errband /
# scatter-fit / 4panel-hero from FigureDraw2/sessions, plus captions.json from its own caption.tex files.
set -euo pipefail
ROOT=/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw2
ARM="${1:?usage: assemble_pp_perarm.sh <arm>}"
DST="$ROOT/fixtures/paper-page-${ARM}"
mkdir -p "$DST"

# Copy brief + claim (same for every arm)
cp "$ROOT/fixtures/paper-page/brief.md" "$DST/brief.md"
cp "$ROOT/fixtures/paper-page/claim.json" "$DST/claim.json"

for entry in "grouped-bar:fig01" "line-errband:fig02" "scatter-fit:fig03" "4panel-hero:fig04"; do
  src_fig="${entry%%:*}"
  dst_name="${entry##*:}"
  src_pdf=$(ls -1d "$ROOT/sessions/$ARM/$src_fig"/*/workspace/figure.pdf 2>/dev/null | sort | tail -1)
  if [[ -z "$src_pdf" ]]; then
    echo "[assemble] $ARM missing $src_fig" >&2
    exit 1
  fi
  cp "$src_pdf" "$DST/${dst_name}.pdf"
done

python3 - <<PYEOF
import json, pathlib, re
root = pathlib.Path("$ROOT/sessions/$ARM")
out = {}
for src, dst in [("grouped-bar","fig01"),("line-errband","fig02"),("scatter-fit","fig03"),("4panel-hero","fig04")]:
    runs = sorted((root/src).glob("*/workspace/caption.tex"))
    if not runs:
        out[dst] = ""
        continue
    txt = runs[-1].read_text(encoding="utf-8")
    pat = r"\\caption\{(.+)\}\s*\$"
    m = re.search(pat, txt.strip(), re.DOTALL)
    out[dst] = (m.group(1) if m else txt).strip()
p = pathlib.Path("$DST/captions.json")
p.write_text(json.dumps(out, indent=2)+"\n", encoding="utf-8")
print("[assemble]", "$ARM", "->", str(p))
PYEOF

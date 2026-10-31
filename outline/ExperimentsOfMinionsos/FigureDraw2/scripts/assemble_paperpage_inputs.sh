#!/usr/bin/env bash
# Once minionsos has produced grouped-bar / line-errband / scatter-fit / 4panel-hero,
# assemble fig01..fig04 + captions.json into the paper-page fixture.
set -euo pipefail
ROOT="/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw2"
DST="$ROOT/fixtures/paper-page"

pick_latest_pdf() {
  local fig="$1"
  ls -1d "$ROOT/sessions/minionsos/$fig"/*/workspace/figure.pdf 2>/dev/null | sort | tail -1
}

map=("grouped-bar:fig01" "line-errband:fig02" "scatter-fit:fig03" "4panel-hero:fig04")
for entry in "${map[@]}"; do
  src_fig="${entry%%:*}"
  dst_name="${entry##*:}"
  src_pdf=$(pick_latest_pdf "$src_fig")
  if [[ -z "$src_pdf" ]]; then
    echo "[assemble] missing minionsos/$src_fig figure.pdf -- run main batch first" >&2
    exit 1
  fi
  cp "$src_pdf" "$DST/$dst_name.pdf"
  echo "[assemble] $src_fig -> $DST/$dst_name.pdf"
done

# Build captions.json from each cell's caption.tex
python3 - <<EOF_PY
import json, pathlib, re
root = pathlib.Path("$ROOT/sessions/minionsos")
out = {}
for src, dst in [("grouped-bar","fig01"),("line-errband","fig02"),("scatter-fit","fig03"),("4panel-hero","fig04")]:
    runs = sorted((root/src).glob("*/workspace/caption.tex"))
    if not runs:
        out[dst] = ""
        continue
    txt = runs[-1].read_text(encoding="utf-8")
    # Strip \caption{...} wrapper if present, keep inner text
    m = re.search(r"\\caption\{(.+)\}\s*$", txt.strip(), re.DOTALL)
    out[dst] = (m.group(1) if m else txt).strip()
out_path = pathlib.Path("$DST/captions.json")
out_path.write_text(json.dumps(out, indent=2)+"\n", encoding="utf-8")
print("[assemble] captions.json written:", out_path)
EOF_PY

#!/usr/bin/env python3
"""Backfill captions.json for every paper-page-<arm> fixture by reading the latest caption.tex
from each arm's grouped-bar/line-errband/scatter-fit/4panel-hero session."""
import json, pathlib, re
ROOT = pathlib.Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/FigureDraw2")
ARMS = ["minionsos","ml-paper-writing","latex-document","academic-paper-imbad",
        "scientific-writing-kdense","stat-writing-fuhaoda","composer-lishix","awesome-writing-prompts"]
CAPTION_PAT = re.compile(r"\\caption\{(.+)\}\s*\Z", re.DOTALL)
for arm in ARMS:
    sess = ROOT/"sessions"/arm
    out = {}
    for src, dst in [("grouped-bar","fig01"),("line-errband","fig02"),("scatter-fit","fig03"),("4panel-hero","fig04")]:
        runs = sorted((sess/src).glob("*/workspace/caption.tex"))
        if not runs:
            out[dst] = ""; continue
        txt = runs[-1].read_text(encoding="utf-8").strip()
        m = CAPTION_PAT.search(txt)
        out[dst] = (m.group(1) if m else txt).strip()
    p = ROOT/f"fixtures/paper-page-{arm}/captions.json"
    p.write_text(json.dumps(out, indent=2)+"\n", encoding="utf-8")
    print("OK", arm)

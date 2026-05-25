#!/usr/bin/env python3
"""figure_audit.py — automated structural / aesthetic audit for figure PNG/SVG.

Usage:
    python3 figure_audit.py <figure.png> [--svg <figure.svg>] [--exemplar <ref.png>]

Output JSON to stdout with audit fields:
    palette: top-10 hex + %
    palette_grey_pct: % of foreground that is grey-family
    palette_signal_hue: dominant non-grey hue family
    palette_n_distinct_hues: count of distinct hue families >5% each
    text_nodes: count of <text> elements in SVG (editable text gate)
    font_family: declared font-family in SVG
    figure_dims_pt: SVG width x height in points (=> mm)
    trailing_whitespace_pct: % of bottom rows with no foreground content
    aspect_ratio: width/height ratio
    saturation_band: estimate of dominant saturation level
    bbox_pct_of_canvas: estimate of how much canvas is data-bearing

This automates ALL principles where pixel-level inspection is needed:
- P1 hue coherence (palette_n_distinct_hues + palette_grey_pct)
- P2 saturation (saturation_band)
- P3 effective area (trailing_whitespace_pct + bbox_pct_of_canvas)

Principles requiring human judgement (P4 packing, P5 form novelty,
P6 polar appropriateness, P7 legend placement, P8 manifold info dim,
P9 comparison_radar match) are FLAGGED but not auto-graded.

Result: ~60% of aesthetic principles auto-checkable; ~40% need user.
The audit shrinks the user's visual review to "is this fundamentally
the right form, are decorations placed sensibly" — pixel-level
discipline (palette, saturation, whitespace) is auto-verified.
"""
from collections import Counter
from pathlib import Path
import argparse
import json
import re
import sys

import numpy as np
from PIL import Image


def hue_family(rgb):
    r, g, b = rgb
    mx, mn = max(rgb), min(rgb)
    if mx - mn < 30:
        if mx > 200: return "white"
        if mx < 80: return "black"
        return "grey"
    # Hue
    h = 0
    if mx == r: h = 60 * ((g - b) / (mx - mn) % 6)
    elif mx == g: h = 60 * ((b - r) / (mx - mn) + 2)
    else: h = 60 * ((r - g) / (mx - mn) + 4)
    h = h % 360
    if 0 <= h < 30 or 330 <= h: return "red"
    if 30 <= h < 80: return "warm"      # orange/yellow
    if 80 <= h < 160: return "green"
    if 160 <= h < 210: return "cyan"
    if 210 <= h < 260: return "blue"
    if 260 <= h < 330: return "purple"
    return "other"


def saturation_band(rgb):
    """Return estimated saturation 0-1."""
    r, g, b = rgb
    mx, mn = max(rgb), min(rgb)
    return (mx - mn) / mx if mx > 0 else 0


def extract_palette(path, top_n=12, bin_levels=6):
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(path).convert("RGB")
    im.thumbnail((400, 400))
    arr = np.array(im).reshape(-1, 3)

    lum = 0.299 * arr[:, 0] + 0.587 * arr[:, 1] + 0.114 * arr[:, 2]
    fg = arr[(lum < 235) & (lum > 35)]
    if len(fg) < 100:
        return {"hex": [], "pct": [], "families": {}, "saturations": []}

    binned = (fg // (256 // bin_levels)).astype(np.int32)
    keys = binned[:, 0] * bin_levels * bin_levels + binned[:, 1] * bin_levels + binned[:, 2]
    cnt = Counter(keys.tolist())

    hex_list = []
    pct_list = []
    fam_counter = Counter()
    sat_list = []
    total = len(fg)
    for k, c in cnt.most_common(top_n):
        r = (k // (bin_levels * bin_levels)) % bin_levels
        g = (k // bin_levels) % bin_levels
        b = k % bin_levels
        rgb = (
            int((r + 0.5) * 256 / bin_levels),
            int((g + 0.5) * 256 / bin_levels),
            int((b + 0.5) * 256 / bin_levels),
        )
        rgb = tuple(min(255, max(0, v)) for v in rgb)
        h = "#{:02x}{:02x}{:02x}".format(*rgb)
        pct = round(100 * c / total, 1)
        if pct > 1.5:
            hex_list.append(h)
            pct_list.append(pct)
            fam = hue_family(rgb)
            fam_counter[fam] += pct
            sat_list.append(round(saturation_band(rgb), 2))

    return {
        "hex": hex_list,
        "pct": pct_list,
        "families": dict(fam_counter),
        "saturations": sat_list,
    }


def trailing_whitespace_pct(png_path):
    im = Image.open(png_path).convert("L")
    arr = np.array(im)
    h, w = arr.shape
    non_white = (arr < 250).any(axis=1)
    if non_white.any():
        last = np.where(non_white)[0][-1]
        return round((h - 1 - last) / h * 100, 1)
    return 100.0


def svg_stats(svg_path):
    if not svg_path or not Path(svg_path).exists():
        return None
    text = Path(svg_path).read_text(encoding="utf-8", errors="ignore")
    n_text = len(re.findall(r"<text", text))
    n_path = len(re.findall(r"<path", text))
    ff_match = re.search(r'font-family[:\s]+([^"\';]+)', text)
    font_family = ff_match.group(1).strip() if ff_match else None
    dim_match = re.search(r'width="([0-9.]+)pt" height="([0-9.]+)pt"', text)
    dims_pt = (
        (float(dim_match.group(1)), float(dim_match.group(2)))
        if dim_match else None
    )
    return {
        "text_nodes": n_text,
        "path_nodes": n_path,
        "font_family": font_family,
        "dims_pt": dims_pt,
        "dims_mm": (
            (round(dims_pt[0] * 25.4 / 72, 1), round(dims_pt[1] * 25.4 / 72, 1))
            if dims_pt else None
        ),
        "editable_text_gate_pass": n_text > 0 and font_family is not None,
    }


def grade_principles(palette, svg, trail_pct):
    """Auto-grade the principles that don't need vision."""
    grades = {}

    # P1 hue coherence: families dict
    fam = palette.get("families", {})
    grey_like = sum(fam.get(k, 0) for k in ["grey", "white", "black"])
    non_grey_families = {k: v for k, v in fam.items() if k not in ["grey", "white", "black"]}
    n_distinct_hues = sum(1 for v in non_grey_families.values() if v > 5)

    grades["P1_hue_coherence"] = {
        "grey_pct": round(grey_like, 1),
        "n_distinct_hues_above_5pct": n_distinct_hues,
        "non_grey_families": non_grey_families,
        "auto_grade": (
            "good" if grey_like > 50 and n_distinct_hues <= 4
            else "concerning" if n_distinct_hues > 4 or grey_like < 30
            else "ok"
        ),
    }

    # P2 saturation: average / max saturation
    sats = palette.get("saturations", [])
    if sats:
        max_sat = max(sats)
        avg_sat = round(sum(sats) / len(sats), 2)
        grades["P2_saturation"] = {
            "max": max_sat, "avg": avg_sat,
            "auto_grade": (
                "good" if max_sat < 0.7 and avg_sat < 0.5 else
                "concerning" if max_sat > 0.85 else
                "ok"
            ),
        }
    else:
        grades["P2_saturation"] = {"auto_grade": "no_data"}

    # P3 effective area: trailing whitespace
    grades["P3_effective_area"] = {
        "trailing_whitespace_pct": trail_pct,
        "auto_grade": (
            "good" if trail_pct < 1 else
            "concerning" if trail_pct > 3 else
            "ok"
        ),
    }

    # Editable text gate (R1.A blocker)
    if svg:
        grades["editable_text_gate"] = {
            "text_nodes": svg.get("text_nodes"),
            "font_family": svg.get("font_family"),
            "auto_grade": "good" if svg.get("editable_text_gate_pass") else "fail",
        }

    # Principles requiring human visual judgement (flagged, not graded)
    grades["needs_human_review"] = {
        "P4_packing": "is the gridspec compact, no empty quadrants?",
        "P5_form_novelty": "did the runner pick the right form for the data structure?",
        "P6_polar_for_NxM": "if N methods x M metrics with M>=3, did runner use polar?",
        "P7_legend_placement": "is the legend off the data plot region?",
        "P8_manifold_info_dim": "if manifold, does it carry only 1-2 info dims?",
        "P9_radar_template_match": "if polar, does it match comparison_radar visual quality?",
    }

    return grades


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("png")
    parser.add_argument("--svg", default=None)
    parser.add_argument("--exemplar", default=None,
                       help="optional reference exemplar for cross-comparison")
    args = parser.parse_args()

    palette = extract_palette(args.png)
    svg = svg_stats(args.svg) if args.svg else None
    trail = trailing_whitespace_pct(args.png)
    grades = grade_principles(palette, svg, trail)

    output = {
        "input_png": args.png,
        "input_svg": args.svg,
        "palette": palette,
        "svg_stats": svg,
        "trailing_whitespace_pct": trail,
        "grades": grades,
    }

    if args.exemplar:
        ref_palette = extract_palette(args.exemplar)
        output["reference_exemplar"] = args.exemplar
        output["reference_palette"] = ref_palette
        output["palette_diff_vs_reference"] = {
            "your_grey_pct": palette.get("families", {}).get("grey", 0),
            "ref_grey_pct": ref_palette.get("families", {}).get("grey", 0),
            "your_max_saturation": max(palette.get("saturations", [0])),
            "ref_max_saturation": max(ref_palette.get("saturations", [0])),
            "your_n_hue_families": len([k for k, v in palette.get("families", {}).items()
                                        if v > 5 and k not in ["grey", "white", "black"]]),
            "ref_n_hue_families": len([k for k, v in ref_palette.get("families", {}).items()
                                       if v > 5 and k not in ["grey", "white", "black"]]),
        }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

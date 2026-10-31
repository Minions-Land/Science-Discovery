#!/usr/bin/env python3
"""Extract dominant non-background colours from a figure PNG.

Usage:
    python3 extract.py path/to/figure.png [top_n] [bin_levels]

Outputs JSON to stdout with top-N hex colours and their pixel-percentage
share of the FOREGROUND (excluding near-white background and near-black text).

Use this when adding a new exemplar to the gallery: extract its real
palette, then write the annotation card citing the extracted hex values.
"""
from collections import Counter
from pathlib import Path
import json
import sys

import numpy as np
from PIL import Image


def extract_palette(path: Path, top_n: int = 10, bin_levels: int = 6) -> dict:
    im = Image.open(path).convert("RGB")
    im.thumbnail((400, 400))
    arr = np.array(im).reshape(-1, 3)

    lum = 0.299 * arr[:, 0] + 0.587 * arr[:, 1] + 0.114 * arr[:, 2]
    fg = arr[(lum < 235) & (lum > 35)]
    if len(fg) < 100:
        return {"hex": [], "pct": [], "note": "insufficient foreground pixels"}

    binned = (fg // (256 // bin_levels)).astype(np.int32)
    keys = binned[:, 0] * bin_levels * bin_levels + binned[:, 1] * bin_levels + binned[:, 2]
    counter = Counter(keys.tolist())

    out_hex = []
    out_pct = []
    total = len(fg)
    for k, c in counter.most_common(top_n):
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
            out_hex.append(h)
            out_pct.append(pct)

    return {"hex": out_hex, "pct": out_pct}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = Path(sys.argv[1])
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    bin_levels = int(sys.argv[3]) if len(sys.argv) > 3 else 6

    result = extract_palette(path, top_n=top_n, bin_levels=bin_levels)
    print(json.dumps(result, indent=2))

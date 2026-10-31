#!/usr/bin/env python3
"""
Split validation data by Level (1/2/3).

Usage:
    python scripts/split_by_level.py
"""

import json
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
VALIDATION_FILE = DATA_DIR / "validation.json"
BY_LEVEL_DIR = DATA_DIR / "by_level"

def main():
    print("Splitting validation data by Level...")

    # Load validation data
    with open(VALIDATION_FILE, "r", encoding="utf-8") as f:
        validation_data = json.load(f)

    print(f"Loaded {len(validation_data)} questions from validation split")

    # Split by level
    by_level = {1: [], 2: [], 3: []}
    for item in validation_data:
        level = item["level"]
        by_level[level].append(item)

    # Save by_level/*.json
    BY_LEVEL_DIR.mkdir(parents=True, exist_ok=True)
    for level, items in by_level.items():
        level_file = BY_LEVEL_DIR / f"level{level}.json"
        with open(level_file, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        print(f"Saved Level {level} ({len(items)} questions) to {level_file}")

    print("\nLevel distribution:")
    for level in sorted(by_level.keys()):
        print(f"  Level {level}: {len(by_level[level])} questions")

if __name__ == "__main__":
    main()

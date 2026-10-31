#!/usr/bin/env python3
"""
Extract mini sample (12 random questions) from validation split.

Usage:
    python scripts/extract_mini_sample.py
"""

import json
import random
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
VALIDATION_FILE = DATA_DIR / "validation.json"
MINI_SAMPLE_FILE = DATA_DIR / "mini_sample.json"

# Config
MINI_SAMPLE_SIZE = 12
RANDOM_SEED = 42

def main():
    print(f"Extracting mini sample ({MINI_SAMPLE_SIZE} questions)...")

    # Load validation data
    with open(VALIDATION_FILE, "r", encoding="utf-8") as f:
        validation_data = json.load(f)

    print(f"Loaded {len(validation_data)} questions from validation split")

    # Random sample
    random.seed(RANDOM_SEED)
    mini_sample = random.sample(validation_data, MINI_SAMPLE_SIZE)

    # Sort by task_id for reproducibility
    mini_sample.sort(key=lambda x: x["task_id"])

    # Save mini_sample.json
    with open(MINI_SAMPLE_FILE, "w", encoding="utf-8") as f:
        json.dump(mini_sample, f, indent=2, ensure_ascii=False)

    print(f"Saved mini sample to {MINI_SAMPLE_FILE}")

    # Print summary
    level_counts = {}
    for item in mini_sample:
        level = item["level"]
        level_counts[level] = level_counts.get(level, 0) + 1

    print("\nMini sample distribution:")
    for level in sorted(level_counts.keys()):
        print(f"  Level {level}: {level_counts[level]} questions")

    print("\nTask IDs:")
    for item in mini_sample:
        print(f"  {item['task_id']} (Level {item['level']})")

if __name__ == "__main__":
    main()

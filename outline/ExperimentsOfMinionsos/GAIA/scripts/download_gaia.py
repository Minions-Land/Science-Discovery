#!/usr/bin/env python3
"""
Download GAIA validation split from HuggingFace.

Usage:
    python scripts/download_gaia.py
"""

import json
import os
from pathlib import Path

try:
    from datasets import load_dataset
except ImportError:
    print("Error: datasets library not found. Install with:")
    print("  pip install datasets")
    exit(1)

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
VALIDATION_FILE = DATA_DIR / "validation.json"
GROUND_TRUTH_FILE = DATA_DIR / "ground_truth.json"
ATTACHMENTS_DIR = DATA_DIR / "attachments"

def main():
    print("Downloading GAIA validation split from HuggingFace...")

    # Load dataset
    dataset = load_dataset("gaia-benchmark/GAIA", "2023_all")
    validation = dataset["validation"]

    print(f"Loaded {len(validation)} questions from validation split")

    # Convert to list of dicts
    validation_data = []
    ground_truth = {}

    for item in validation:
        task_id = item["task_id"]
        question = item["Question"]
        level = item["Level"]
        final_answer = item["Final answer"]
        file_name = item.get("file_name", "")
        file_path = item.get("file_path", "")

        validation_data.append({
            "task_id": task_id,
            "question": question,
            "level": level,
            "file_name": file_name,
            "file_path": file_path,
        })

        ground_truth[task_id] = final_answer

    # Save validation.json
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(VALIDATION_FILE, "w", encoding="utf-8") as f:
        json.dump(validation_data, f, indent=2, ensure_ascii=False)
    print(f"Saved validation data to {VALIDATION_FILE}")

    # Save ground_truth.json
    with open(GROUND_TRUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(ground_truth, f, indent=2, ensure_ascii=False)
    print(f"Saved ground truth to {GROUND_TRUTH_FILE}")

    # Download attachments
    ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\nDownloading attachments to {ATTACHMENTS_DIR}...")

    for item in validation:
        task_id = item["task_id"]
        file_name = item.get("file_name", "")

        if file_name:
            task_dir = ATTACHMENTS_DIR / task_id
            task_dir.mkdir(parents=True, exist_ok=True)

            # TODO: Download actual file from HuggingFace
            # For now, just create a placeholder
            attachment_path = task_dir / file_name
            if not attachment_path.exists():
                print(f"  {task_id}/{file_name} (placeholder)")
                # attachment_path.touch()

    print("\nDone! Next steps:")
    print("  1. python scripts/extract_mini_sample.py")
    print("  2. python scripts/split_by_level.py")
    print("  3. python scripts/build_prompts.py")

if __name__ == "__main__":
    main()

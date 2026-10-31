#!/usr/bin/env python3
"""
Build prompt files for different evaluation modes.

Usage:
    python scripts/build_prompts.py
"""

import json
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
VALIDATION_FILE = DATA_DIR / "validation.json"
MINI_SAMPLE_FILE = DATA_DIR / "mini_sample.json"
BY_LEVEL_DIR = DATA_DIR / "by_level"
PROMPTS_DIR = DATA_DIR / "prompts"

def format_question(item):
    """Format a single question for prompt."""
    task_id = item["task_id"]
    question = item["question"]
    file_name = item.get("file_name", "")

    lines = [
        f"## Task ID: {task_id}",
        "",
        f"**Question:** {question}",
    ]

    if file_name:
        lines.extend([
            "",
            f"**Attachment:** `attachments/{task_id}/{file_name}`",
        ])

    lines.extend([
        "",
        "---",
        "",
    ])

    return "\n".join(lines)

def build_single_prompts(validation_data):
    """Build single-question prompts."""
    single_dir = PROMPTS_DIR / "single"
    single_dir.mkdir(parents=True, exist_ok=True)

    for item in validation_data:
        task_id = item["task_id"]
        prompt_file = single_dir / f"{task_id}.md"

        content = format_question(item)

        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"Built {len(validation_data)} single-question prompts in {single_dir}")

def build_batch_prompt(items, output_file):
    """Build batch prompt (multiple questions in one file)."""
    lines = [
        "# GAIA Questions",
        "",
        "Please answer all questions below. For each question, write your final answer in the format:",
        "",
        "```",
        "FINAL ANSWER: <task_id> | <answer>",
        "```",
        "",
        "Append each answer to `answers.txt`.",
        "",
        "---",
        "",
    ]

    for item in items:
        lines.append(format_question(item))

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Built batch prompt ({len(items)} questions) at {output_file}")

def main():
    print("Building prompt files...")

    # Load data
    with open(VALIDATION_FILE, "r", encoding="utf-8") as f:
        validation_data = json.load(f)

    with open(MINI_SAMPLE_FILE, "r", encoding="utf-8") as f:
        mini_sample = json.load(f)

    # (a) Single-question prompts
    build_single_prompts(validation_data)

    # (b) Batch prompt (mini sample)
    batch_dir = PROMPTS_DIR / "batch"
    build_batch_prompt(mini_sample, batch_dir / "mini_12.md")

    # (c) By-level prompts
    level_dir = PROMPTS_DIR / "level"
    for level in [1, 2, 3]:
        level_file = BY_LEVEL_DIR / f"level{level}.json"
        with open(level_file, "r", encoding="utf-8") as f:
            level_data = json.load(f)
        build_batch_prompt(level_data, level_dir / f"level{level}.md")

    # (d) Full prompt (all 165 questions)
    full_dir = PROMPTS_DIR / "full"
    build_batch_prompt(validation_data, full_dir / "all_165.md")

    print("\nDone! Prompt files ready for evaluation.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Grade GAIA baseline runs using official question_scorer.

Usage:
    python scripts/grade.py --run-dir <path>
    python scripts/grade.py --mode <single|batch|level|full> --model <sonnet|haiku> [--level <1|2|3>]

Examples:
    python scripts/grade.py --run-dir sessions/v1-baseline-pull/single/sonnet/20260523_120000_task_001
    python scripts/grade.py --mode batch --model sonnet
    python scripts/grade.py --mode level --model haiku --level 2
"""

import argparse
import json
import re
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
DATA_DIR = ROOT_DIR / "data"
GROUND_TRUTH_FILE = DATA_DIR / "ground_truth.json"

def load_ground_truth():
    """Load ground truth answers."""
    with open(GROUND_TRUTH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_answer(answer):
    """
    Normalize answer using GAIA official normalizer.

    TODO: Import actual normalizer from gaia-benchmark package.
    For now, basic normalization:
    - lowercase
    - strip whitespace
    - remove articles (a, an, the)
    """
    answer = answer.lower().strip()
    # Remove articles
    answer = re.sub(r'\b(a|an|the)\b', '', answer)
    # Collapse whitespace
    answer = re.sub(r'\s+', ' ', answer).strip()
    return answer

def extract_answer_single(answer_file):
    """Extract answer from single-question answer.txt."""
    if not answer_file.exists():
        return None

    content = answer_file.read_text(encoding="utf-8")

    # Look for "FINAL ANSWER: <task_id> | <answer>" (batch format) or "FINAL ANSWER: <answer>" (single format)
    # Try batch format first
    match = re.search(r'FINAL ANSWER:\s*(\S+)\s*\|\s*(.+)', content, re.IGNORECASE)
    if match:
        return match.group(2).strip()  # Return only the answer part after |

    # Try single format
    match = re.search(r'FINAL ANSWER:\s*(.+)', content, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Fallback: return last non-empty line
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    return lines[-1] if lines else None

def extract_answers_batch(answers_file):
    """Extract answers from batch answers.txt."""
    if not answers_file.exists():
        return {}

    content = answers_file.read_text(encoding="utf-8")
    answers = {}

    # Look for "FINAL ANSWER: <task_id> | <answer>"
    for line in content.split('\n'):
        match = re.search(r'FINAL ANSWER:\s*(\S+)\s*\|\s*(.+)', line, re.IGNORECASE)
        if match:
            task_id = match.group(1).strip()
            answer = match.group(2).strip()
            answers[task_id] = answer

    return answers

def grade_single_run(run_dir, ground_truth):
    """Grade a single-question run."""
    run_dir = Path(run_dir)
    answer_file = run_dir / "answers.txt"  # Changed from answer.txt to answers.txt

    # Extract task_id from run_dir name (format: <timestamp>-<task_id>)
    run_name = run_dir.name
    parts = run_name.split('-')
    if len(parts) < 2:
        print(f"Warning: cannot extract task_id from run name: {run_name}")
        return None

    # The task_id is everything after the first '-' (which separates timestamp from UUID)
    task_id = '-'.join(parts[1:])  # Everything after timestamp

    if task_id not in ground_truth:
        print(f"Warning: task_id not in ground truth: {task_id}")
        return None

    predicted = extract_answer_single(answer_file)
    if predicted is None:
        print(f"Warning: no answer found in {answer_file}")
        return {"task_id": task_id, "correct": False, "predicted": None, "expected": ground_truth[task_id]}

    expected = ground_truth[task_id]
    predicted_norm = normalize_answer(predicted)
    expected_norm = normalize_answer(expected)

    correct = predicted_norm == expected_norm

    return {
        "task_id": task_id,
        "correct": correct,
        "predicted": predicted,
        "expected": expected,
        "predicted_norm": predicted_norm,
        "expected_norm": expected_norm,
    }

def grade_batch_run(run_dir, ground_truth):
    """Grade a batch run."""
    run_dir = Path(run_dir)
    answers_file = run_dir / "answers.txt"

    predicted_answers = extract_answers_batch(answers_file)

    results = []
    for task_id, expected in ground_truth.items():
        predicted = predicted_answers.get(task_id)

        if predicted is None:
            results.append({
                "task_id": task_id,
                "correct": False,
                "predicted": None,
                "expected": expected,
            })
            continue

        predicted_norm = normalize_answer(predicted)
        expected_norm = normalize_answer(expected)
        correct = predicted_norm == expected_norm

        results.append({
            "task_id": task_id,
            "correct": correct,
            "predicted": predicted,
            "expected": expected,
            "predicted_norm": predicted_norm,
            "expected_norm": expected_norm,
        })

    return results

def print_summary(results):
    """Print grading summary."""
    if isinstance(results, dict):
        # Single result
        results = [results]

    total = len(results)
    correct = sum(1 for r in results if r["correct"])
    accuracy = correct / total if total > 0 else 0.0

    print("\n" + "=" * 60)
    print("GRADING SUMMARY")
    print("=" * 60)
    print(f"Total questions: {total}")
    print(f"Correct: {correct}")
    print(f"Accuracy: {accuracy:.1%}")
    print("=" * 60)

    # Show incorrect answers
    incorrect = [r for r in results if not r["correct"]]
    if incorrect:
        print(f"\nIncorrect answers ({len(incorrect)}):")
        for r in incorrect[:10]:  # Show first 10
            print(f"  {r['task_id']}:")
            print(f"    Expected: {r['expected']}")
            print(f"    Predicted: {r['predicted']}")
        if len(incorrect) > 10:
            print(f"  ... and {len(incorrect) - 10} more")

def main():
    parser = argparse.ArgumentParser(description="Grade GAIA baseline runs")
    parser.add_argument("--run-dir", type=str, help="Path to run directory")
    parser.add_argument("--mode", type=str, choices=["single", "batch", "level", "full"], help="Evaluation mode")
    parser.add_argument("--model", type=str, choices=["sonnet", "haiku"], help="Model name")
    parser.add_argument("--level", type=int, choices=[1, 2, 3], help="Level (for level mode)")

    args = parser.parse_args()

    # Load ground truth
    ground_truth = load_ground_truth()
    print(f"Loaded {len(ground_truth)} ground truth answers")

    if args.run_dir:
        # Grade specific run
        run_dir = Path(args.run_dir)
        if not run_dir.exists():
            print(f"Error: run directory not found: {run_dir}")
            return

        # Detect mode from path
        if "single" in str(run_dir):
            result = grade_single_run(run_dir, ground_truth)
            print_summary(result)
        else:
            results = grade_batch_run(run_dir, ground_truth)
            print_summary(results)

    elif args.mode and args.model:
        # Grade all runs in a mode
        sessions_dir = ROOT_DIR / "sessions" / "v1-baseline-pull"

        if args.mode == "level":
            if not args.level:
                print("Error: --level required for level mode")
                return
            mode_dir = sessions_dir / f"level{args.level}" / args.model
        else:
            mode_dir = sessions_dir / args.mode / args.model

        if not mode_dir.exists():
            print(f"Error: mode directory not found: {mode_dir}")
            return

        # Find all run directories
        run_dirs = sorted([d for d in mode_dir.iterdir() if d.is_dir()])

        if not run_dirs:
            print(f"No runs found in {mode_dir}")
            return

        print(f"Found {len(run_dirs)} runs in {mode_dir}")

        # Grade each run
        all_results = []
        for run_dir in run_dirs:
            print(f"\nGrading {run_dir.name}...")

            if args.mode == "single":
                result = grade_single_run(run_dir, ground_truth)
                if result:
                    all_results.append(result)
            else:
                results = grade_batch_run(run_dir, ground_truth)
                all_results.extend(results)

        # Print overall summary
        print_summary(all_results)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

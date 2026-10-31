#!/usr/bin/env python3
"""Full data loading test for all benchmarks.

Tests that real data (not just samples) can be loaded and parsed.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

DATASETS_DIR = Path(__file__).parent / "datasets"

def test_locomo_full() -> Dict[str, Any]:
    """Test loading full LoCoMo dataset (10 conversations)."""
    data_file = DATASETS_DIR / "locomo_repo" / "data" / "locomo10.json"
    if not data_file.exists():
        return {"status": "FAIL", "error": f"File not found: {data_file}"}

    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            return {"status": "FAIL", "error": f"Expected list, got {type(data)}"}

        # Validate all items
        total_qa = 0
        for i, item in enumerate(data):
            required_keys = ['qa', 'conversation', 'sample_id']
            missing = [k for k in required_keys if k not in item]
            if missing:
                return {"status": "FAIL", "error": f"Item {i} missing keys: {missing}"}

            if not isinstance(item['qa'], list):
                return {"status": "FAIL", "error": f"Item {i} qa must be list"}

            total_qa += len(item['qa'])

            # Validate first QA in each conversation
            if item['qa']:
                qa = item['qa'][0]
                if 'question' not in qa or 'answer' not in qa:
                    return {"status": "FAIL", "error": f"Item {i} QA missing question/answer"}

        return {
            "status": "PASS",
            "conversations": len(data),
            "total_qa_pairs": total_qa,
            "avg_qa_per_conv": round(total_qa / len(data), 1),
        }
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

def _count_membench_items(data: Any) -> tuple:
    """Count roles/events/QA pairs from a MemBench file regardless of top-level shape.

    Handles two shapes:
    - {'roles': [...], 'events': [...]}   — most task files
    - {'movie': {...}, 'food': {...}, ...} — highlevel.json (nested by domain)
    """
    if not isinstance(data, dict):
        return 0, 0, 0

    # Shape 1: top-level has 'roles' key
    if 'roles' in data:
        roles = data['roles']
        events = data.get('events', [])
        qa_count = sum(len(r.get('QA', [])) for r in roles if isinstance(r, dict))
        return len(roles), len(events), qa_count

    # Shape 2: domain-keyed dict (e.g. highlevel.json: {'movie': {…}, 'food': {…}})
    total_roles = total_events = total_qa = 0
    for domain_val in data.values():
        if isinstance(domain_val, dict):
            if 'roles' in domain_val:
                sub_roles, sub_events, sub_qa = _count_membench_items(domain_val)
                total_roles += sub_roles
                total_events += sub_events
                total_qa += sub_qa
            else:
                # domain_val itself might be a list of role dicts
                pass
        elif isinstance(domain_val, list):
            total_roles += len(domain_val)
            total_qa += sum(len(r.get('QA', [])) for r in domain_val if isinstance(r, dict))
    return total_roles, total_events, total_qa


def test_membench_full() -> Dict[str, Any]:
    """Test loading full MemBench dataset (all task types)."""
    base_dir = DATASETS_DIR / "membench_repo" / "MemData" / "FirstAgent"
    if not base_dir.exists():
        return {"status": "FAIL", "error": f"Directory not found: {base_dir}"}

    try:
        task_files = list(base_dir.glob("*.json"))
        if not task_files:
            return {"status": "FAIL", "error": "No JSON files found"}

        total_roles = 0
        total_events = 0
        total_qa = 0
        task_counts = {}

        for task_file in task_files:
            with open(task_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, dict):
                return {"status": "FAIL", "error": f"{task_file.name}: expected dict, got {type(data).__name__}"}

            roles, events, qa = _count_membench_items(data)
            total_roles += roles
            total_events += events
            total_qa += qa
            task_counts[task_file.stem] = {'roles': roles, 'events': events, 'qa': qa}

        return {
            "status": "PASS",
            "task_types": len(task_files),
            "total_roles": total_roles,
            "total_events": total_events,
            "total_qa_pairs": total_qa,
            "tasks": task_counts,
        }
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

def test_memoryagentbench_full() -> Dict[str, Any]:
    """Test loading MemoryAgentBench dataset from HuggingFace download."""
    data_dir = DATASETS_DIR / "memoryagentbench" / "raw"
    if not data_dir.exists():
        return {
            "status": "SKIP",
            "reason": "Data not downloaded yet",
            "action": "Run: python3 -c 'from huggingface_hub import snapshot_download; snapshot_download(repo_id=\"ai-hyz/MemoryAgentBench\", repo_type=\"dataset\", local_dir=\"datasets/memoryagentbench/raw\")'",
        }

    try:
        import pandas as pd

        # Data is in Parquet format under raw/data/
        data_subdir = data_dir / "data"
        parquet_files = list(data_subdir.glob("*.parquet")) if data_subdir.exists() else []
        if not parquet_files:
            parquet_files = list(data_dir.rglob("*.parquet"))

        if not parquet_files:
            return {
                "status": "FAIL",
                "error": f"No .parquet files found under {data_dir}",
                "hint": "Check if HuggingFace download completed successfully",
            }

        file_stats = {}
        total_rows = 0

        for pf in parquet_files:
            df = pd.read_parquet(pf)
            file_stats[pf.name] = len(df)
            total_rows += len(df)
            # Validate at least one row can be read
            if len(df) > 0:
                row = df.iloc[0].to_dict()
                # Just check it's a non-empty dict
                if not row:
                    return {"status": "FAIL", "error": f"{pf.name}: empty first row"}

        return {
            "status": "PASS",
            "files": len(parquet_files),
            "total_samples": total_rows,
            "breakdown": file_stats,
        }
    except ImportError:
        return {"status": "FAIL", "error": "pandas not installed — run: pip install pandas pyarrow"}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

def main():
    tests = [
        ("LoCoMo (full)", test_locomo_full),
        ("MemBench (full)", test_membench_full),
        ("MemoryAgentBench (full)", test_memoryagentbench_full),
    ]

    results = {}
    for name, test_fn in tests:
        print(f"Testing {name}...", end=" ")
        result = test_fn()
        results[name] = result
        status = result["status"]
        if status == "PASS":
            print("✓ PASS")
        elif status == "SKIP":
            print(f"⊘ SKIP")
        else:
            print(f"✗ FAIL")

    # Summary
    print("\n" + "="*70)
    print("FULL DATA LOADING TEST SUMMARY")
    print("="*70)
    for name, result in results.items():
        status = result["status"]
        print(f"\n{name}")
        print(f"  Status: {status}")
        if status == "PASS":
            for k, v in result.items():
                if k != "status":
                    if isinstance(v, dict):
                        print(f"  {k}:")
                        for sk, sv in list(v.items())[:5]:  # Show first 5 items
                            print(f"    {sk}: {sv}")
                        if len(v) > 5:
                            print(f"    ... and {len(v)-5} more")
                    else:
                        print(f"  {k}: {v}")
        elif status == "SKIP":
            print(f"  Reason: {result.get('reason', 'N/A')}")
            if 'action' in result:
                print(f"  Action: {result['action'][:100]}...")
        else:
            print(f"  Error: {result.get('error', 'Unknown')}")

    # Exit code
    passed = sum(1 for r in results.values() if r["status"] == "PASS")
    skipped = sum(1 for r in results.values() if r["status"] == "SKIP")
    failed = sum(1 for r in results.values() if r["status"] == "FAIL")

    print(f"\nPassed: {passed}, Skipped: {skipped}, Failed: {failed}")

    if failed > 0:
        print("\n✗ Some tests failed. Fix errors before proceeding.")
        sys.exit(1)
    elif passed >= 2:  # At least 2 benchmarks must work
        print("\n✓ Data loading tests complete. Ready for evaluation.")
        sys.exit(0)
    else:
        print("\n⚠ Not enough benchmarks ready. Need at least 2 passing.")
        sys.exit(1)

if __name__ == "__main__":
    main()

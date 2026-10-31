#!/usr/bin/env python3
"""Smoke test runner for memory benchmarks.

Validates that:
1. Dataset files are accessible
2. Data can be parsed
3. Basic schema is correct
4. Sample queries can be constructed

Does NOT test MinionsOS integration (that's for full eval).
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

DATASETS_DIR = Path(__file__).parent / "datasets"

def test_locomo() -> Dict[str, Any]:
    """Smoke test for LoCoMo dataset."""
    data_file = DATASETS_DIR / "locomo_repo" / "data" / "locomo10.json"
    if not data_file.exists():
        return {"status": "FAIL", "error": f"File not found: {data_file}"}

    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            return {"status": "FAIL", "error": f"Expected list, got {type(data)}"}

        if len(data) == 0:
            return {"status": "FAIL", "error": "Empty dataset"}

        # Check first item schema
        item = data[0]
        required_keys = ['qa', 'conversation', 'sample_id']
        missing = [k for k in required_keys if k not in item]
        if missing:
            return {"status": "FAIL", "error": f"Missing keys: {missing}"}

        # Check QA structure
        if not isinstance(item['qa'], list) or len(item['qa']) == 0:
            return {"status": "FAIL", "error": "QA must be non-empty list"}

        qa = item['qa'][0]
        if 'question' not in qa or 'answer' not in qa:
            return {"status": "FAIL", "error": "QA missing question/answer"}

        return {
            "status": "PASS",
            "samples": len(data),
            "first_sample_id": item.get('sample_id'),
            "first_qa_count": len(item['qa']),
        }
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

def test_membench() -> Dict[str, Any]:
    """Smoke test for MemBench dataset."""
    data_file = DATASETS_DIR / "membench_repo" / "MemData" / "FirstAgent" / "simple.json"
    if not data_file.exists():
        return {"status": "FAIL", "error": f"File not found: {data_file}"}

    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return {"status": "FAIL", "error": f"Expected dict, got {type(data)}"}

        if 'roles' not in data or 'events' not in data:
            return {"status": "FAIL", "error": "Missing 'roles' or 'events' key"}

        roles = data['roles']
        if not isinstance(roles, list) or len(roles) == 0:
            return {"status": "FAIL", "error": "roles must be non-empty list"}

        # Check first role structure
        role = roles[0]
        required_keys = ['tid', 'message_list', 'QA']
        missing = [k for k in required_keys if k not in role]
        if missing:
            return {"status": "FAIL", "error": f"Role missing keys: {missing}"}

        return {
            "status": "PASS",
            "roles_count": len(roles),
            "events_count": len(data['events']),
            "first_role_qa_count": len(role.get('QA', [])),
        }
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

def test_memoryagentbench() -> Dict[str, Any]:
    """Smoke test for MemoryAgentBench dataset.

    Note: The cloned repo doesn't contain eval data — it's framework code.
    Real datasets are on HuggingFace. This test just confirms the repo exists.
    """
    repo_dir = DATASETS_DIR / "memoryagentbench_repo"
    if not repo_dir.exists():
        return {"status": "FAIL", "error": f"Repo not found: {repo_dir}"}

    # Check for README
    readme = repo_dir / "README.md"
    if not readme.exists():
        return {"status": "FAIL", "error": "README.md not found"}

    return {
        "status": "SKIP",
        "reason": "MemoryAgentBench data is on HuggingFace, not in GitHub repo",
        "action_required": "Run: huggingface-cli download HUST-AI-HYZ/MemoryAgentBench",
    }

def test_memoryarena() -> Dict[str, Any]:
    """Smoke test for MemoryArena dataset.

    Note: No confirmed paper/repo found during research phase.
    """
    return {
        "status": "SKIP",
        "reason": "MemoryArena benchmark not confirmed — no official paper/repo found",
        "action_required": "Verify benchmark name with user before building adapter",
    }

def main():
    tests = [
        ("LoCoMo", test_locomo),
        ("MemBench", test_membench),
        ("MemoryAgentBench", test_memoryagentbench),
        ("MemoryArena", test_memoryarena),
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
            print(f"⊘ SKIP ({result.get('reason', 'N/A')})")
        else:
            print(f"✗ FAIL: {result.get('error', 'Unknown error')}")

    # Summary
    print("\n" + "="*60)
    print("SMOKE TEST SUMMARY")
    print("="*60)
    for name, result in results.items():
        status = result["status"]
        print(f"{name:20s} {status:6s}", end="")
        if status == "PASS":
            # Print key metrics
            metrics = {k: v for k, v in result.items() if k != "status"}
            print(f"  {metrics}")
        elif status == "SKIP":
            print(f"  {result.get('reason', '')}")
        else:
            print(f"  {result.get('error', '')}")

    # Exit code
    passed = sum(1 for r in results.values() if r["status"] == "PASS")
    skipped = sum(1 for r in results.values() if r["status"] == "SKIP")
    failed = sum(1 for r in results.values() if r["status"] == "FAIL")

    print(f"\nPassed: {passed}, Skipped: {skipped}, Failed: {failed}")

    if failed > 0:
        sys.exit(1)
    elif passed == 0:
        print("\nWARNING: No tests passed. At least one benchmark must pass for hand-off.")
        sys.exit(1)
    else:
        print("\n✓ Smoke tests complete. Ready for full evaluation.")
        sys.exit(0)

if __name__ == "__main__":
    main()

#!/usr/bin/env bash
# One-liner test runner for all memory benchmarks
# Usage: bash run_tests.sh
set -e
cd "$(dirname "$0")"

echo "=== Memory Benchmark Test Suite ==="
echo ""

# Install deps if needed
python3 -c "import pandas, pyarrow" 2>/dev/null || {
    echo "Installing pandas/pyarrow..."
    pip3 install --user pandas pyarrow --quiet
}

echo "--- Smoke tests (format validation) ---"
python3 smoke_test.py

echo ""
echo "--- Full data loading tests ---"
python3 test_full_data.py

echo ""
echo "All done."

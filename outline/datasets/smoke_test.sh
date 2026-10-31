#!/usr/bin/env bash
# Smoke test for outline/datasets — verifies that each cloned repo / HF dataset
# is non-empty and has at least one expected artifact. Designed to be re-run
# after every pass of download_benchmarks.sh.
#
# Usage:
#   ./smoke_test.sh           # run all checks, print summary
#   ./smoke_test.sh --verbose # print per-benchmark detail
#   ./smoke_test.sh --json    # machine-readable summary

set -uo pipefail

BASE="$(cd "$(dirname "$0")" && pwd)"
VERBOSE=false
JSON=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --verbose|-v) VERBOSE=true; shift ;;
    --json) JSON=true; shift ;;
    *) echo "Unknown: $1"; exit 1 ;;
  esac
done

PASS=0
FAIL=0
SKIP=0
RESULTS=()

check() {
  local name="$1"
  local path="$2"
  local kind="$3"  # "repo" | "hf"

  if [[ ! -d "$path" ]]; then
    SKIP=$((SKIP+1))
    RESULTS+=("SKIP|$kind|$name|missing dir")
    return
  fi

  local size files
  size=$(du -sh "$path" 2>/dev/null | awk '{print $1}')
  files=$(find "$path" -type f 2>/dev/null | wc -l | tr -d ' ')

  if [[ "$files" -lt 1 ]]; then
    FAIL=$((FAIL+1))
    RESULTS+=("FAIL|$kind|$name|empty (size=$size)")
    return
  fi

  # Repo-specific: check for .git/HEAD or a README
  if [[ "$kind" == "repo" ]]; then
    if [[ ! -f "$path/.git/HEAD" ]] && [[ ! -f "$path/.git" ]]; then
      FAIL=$((FAIL+1))
      RESULTS+=("FAIL|$kind|$name|no .git/HEAD ($files files, $size)")
      return
    fi
  fi

  PASS=$((PASS+1))
  RESULTS+=("PASS|$kind|$name|$files files, $size")
}

# Walk every meta.json directory
while IFS= read -r meta; do
  d=$(dirname "$meta")
  rel=${d#$BASE/}
  name=$(basename "$d")
  if [[ -d "$d/repo" ]]; then
    check "$rel" "$d/repo" "repo"
  fi
  if [[ -d "$d/hf_data" ]]; then
    check "$rel" "$d/hf_data" "hf"
  fi
done < <(find "$BASE" -name meta.json | sort)

# Output
if $JSON; then
  echo "{"
  echo "  \"pass\": $PASS,"
  echo "  \"fail\": $FAIL,"
  echo "  \"skip\": $SKIP,"
  echo "  \"results\": ["
  first=true
  for r in "${RESULTS[@]}"; do
    IFS='|' read -r status kind name detail <<< "$r"
    if $first; then first=false; else echo ","; fi
    printf '    {"status":"%s","kind":"%s","name":"%s","detail":"%s"}' \
      "$status" "$kind" "$name" "$detail"
  done
  echo
  echo "  ]"
  echo "}"
else
  echo "━━━ Smoke test results ━━━"
  if $VERBOSE; then
    for r in "${RESULTS[@]}"; do
      IFS='|' read -r status kind name detail <<< "$r"
      printf "%-4s %-4s %-60s %s\n" "$status" "$kind" "$name" "$detail"
    done
    echo
  fi
  echo "PASS: $PASS"
  echo "FAIL: $FAIL"
  echo "SKIP: $SKIP (no repo dir, paper-only or proprietary)"
  if [[ $FAIL -gt 0 ]]; then
    echo
    echo "Failures:"
    for r in "${RESULTS[@]}"; do
      [[ "$r" == FAIL* ]] && echo "  $r"
    done
    exit 1
  fi
fi

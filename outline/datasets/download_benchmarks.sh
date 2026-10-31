#!/usr/bin/env bash
# Download all 73 auto-research benchmarks
# Usage: ./download_benchmarks.sh [--tier1-only] [--dry-run] [--clone-timeout=SEC]
#
# Network notes (verified 2026-05-22):
#   - github.com HTTPS throttled; gh-cli rewrites to SSH (insteadOf)
#   - SSH can stall on big repos; --clone-timeout kills stuck clones
#   - huggingface.co is TCP-reset; pull_hf uses hf-mirror.com via curl

set -uo pipefail

BASE="$(cd "$(dirname "$0")" && pwd)"
DRY_RUN=false
TIER1_ONLY=false
CLONE_TIMEOUT=${CLONE_TIMEOUT:-300}

while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run) DRY_RUN=true; shift ;;
    --tier1-only) TIER1_ONLY=true; shift ;;
    --clone-timeout=*) CLONE_TIMEOUT="${1#*=}"; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

log() { echo "[$(date +%H:%M:%S)] $*"; }
run() {
  if $DRY_RUN; then
    echo "[DRY] $*"
  else
    log "Running: $*"
    "$@"
  fi
}

# Cross-platform timeout (no GNU coreutils on macOS).
# Runs cmd in background, kills it after $1 seconds.
run_timed() {
  local secs="$1"; shift
  if command -v gtimeout &>/dev/null; then
    gtimeout --kill-after=10 "$secs" "$@"
    return $?
  fi
  "$@" &
  local pid=$!
  ( sleep "$secs"; kill -TERM "$pid" 2>/dev/null; sleep 5; kill -KILL "$pid" 2>/dev/null ) &
  local watcher=$!
  wait "$pid" 2>/dev/null
  local rc=$?
  kill -TERM "$watcher" 2>/dev/null
  wait "$watcher" 2>/dev/null
  return $rc
}

clone_repo() {
  local repo="$1"
  local target="$2"
  if [[ -z "$repo" ]]; then
    log "  ⊘ No repo URL"
    return
  fi
  local repo_dir="$target/repo"
  if [[ -d "$repo_dir/.git" ]]; then
    log "  ✓ Already cloned: $repo_dir"
    return
  fi
  mkdir -p "$target"
  if $DRY_RUN; then
    echo "[DRY] gh repo clone $repo $repo_dir --depth=1"
    return
  fi
  log "  ↓ cloning $repo (timeout=${CLONE_TIMEOUT}s)"
  if run_timed "$CLONE_TIMEOUT" gh repo clone "$repo" "$repo_dir" -- --depth=1; then
    log "  ✓ cloned"
  else
    log "  ✗ clone failed/timed out: $repo"
    rm -rf "$repo_dir"
  fi
}

pull_hf() {
  local dataset="$1"
  local target="$2"
  if [[ -z "$dataset" ]]; then
    log "  ⊘ No HuggingFace dataset"
    return
  fi
  if [[ -d "$target" ]] && [[ -n "$(ls -A "$target" 2>/dev/null)" ]]; then
    log "  ✓ Already downloaded: $target"
    return
  fi
  # Use hf-mirror.com (huggingface.co is TCP-reset on this host).
  # Approach: enumerate files via /api/datasets/.../tree/main?recursive=true,
  # then curl each blob through /datasets/.../resolve/main/<path>.
  # See ~/.claude/skills/huggingface-fetch/SKILL.md for full recipe.
  local mirror="${HF_MIRROR:-https://hf-mirror.com}"
  mkdir -p "$target"
  log "  ↓ HF dataset $dataset → $target (via $mirror)"

  local listing
  listing=$(curl -sSL --max-time 30 \
    "$mirror/api/datasets/$dataset/tree/main?recursive=true" 2>/dev/null) || {
    log "  ✗ tree API failed for $dataset"
    return
  }
  if [[ -z "$listing" ]] || [[ "$listing" == *'"error"'* ]]; then
    log "  ✗ tree API: $(echo "$listing" | head -c 100)"
    return
  fi

  echo "$listing" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for f in data:
    if f.get('type') == 'file':
        print(f['path'])
" 2>/dev/null | while read -r path; do
    [[ -z "$path" ]] && continue
    out="$target/$path"
    mkdir -p "$(dirname "$out")"
    if [[ -s "$out" ]]; then
      continue
    fi
    if $DRY_RUN; then
      echo "[DRY] curl $mirror/datasets/$dataset/resolve/main/$path"
    else
      curl -sSL --max-time 300 ${HF_TOKEN:+-H "Authorization: Bearer $HF_TOKEN"} \
        -o "$out" "$mirror/datasets/$dataset/resolve/main/$path" \
        || log "    ✗ failed: $path"
    fi
  done
  log "  ✓ HF dataset $dataset done"
}

# Tier 1: 17 benchmarks that can be evaluated immediately (status: ✓)
TIER1=(
  "1.2-literature-review/LitSearch|https://github.com/princeton-nlp/LitSearch|"
  "1.2-literature-review/CiteME|https://github.com/bethgelab/CiteME|"
  "1.3-coding-experiments/SWE-bench|https://github.com/princeton-nlp/SWE-bench|princeton-nlp/SWE-bench"
  "1.3-coding-experiments/SciCode|https://github.com/scicode-bench/SciCode|"
  "1.3-coding-experiments/MLAgentBench|https://github.com/snap-stanford/MLAgentBench|"
  "1.3-coding-experiments/ScienceAgentBench|https://github.com/OSU-NLP-Group/ScienceAgentBench|"
  "1.3-coding-experiments/KernelBench|https://github.com/ScalingIntelligence/KernelBench|"
  "1.3-coding-experiments/TritonBench|https://github.com/thunlp/TritonBench|"
  "1.3-coding-experiments/InfiAgent-DABench|https://github.com/InfiAgent/InfiAgent|"
  "1.3-coding-experiments/SUPER|https://github.com/allenai/super-benchmark|"
  "1.4-tables-figures/TeXpert|https://github.com/knowledge-verse-ai/TeXpert|"
  "1.4-tables-figures/ChartQA|https://github.com/vis-nlp/ChartQA|"
  "2-paper-writing/SciIG||"
  "2-paper-writing/AutoSurvey|https://github.com/AutoSurveys/AutoSurvey|"
  "3.1-peer-review/PeerRead|https://github.com/allenai/PeerRead|"
  "3.1-peer-review/ClaimCheck||"
  "e2e-general/GAIA||gaia-benchmark/GAIA"
  "e2e-general/SimpleQA|https://github.com/openai/simple-evals|"
)

# Tier 2: 34 benchmarks needing light adapter (status: ~)
TIER2=(
  "1.1-idea-generation/IdeaBench||"
  "1.1-idea-generation/LiveIdeaBench|https://github.com/x66ccff/liveideabench|"
  "1.1-idea-generation/AI-Idea-Bench-2025|https://github.com/yansheng-qiu/AI_Idea_Bench_2025|"
  "1.1-idea-generation/HindSight||"
  "1.2-literature-review/DeepScholar-Bench|https://github.com/guestrin-lab/deepscholar-bench|"
  "1.2-literature-review/ReportBench|https://github.com/ByteDance-BandAI/ReportBench|"
  "1.2-literature-review/ScholarGym||"
  "1.3-coding-experiments/SWE-bench-Pro|https://github.com/scaleapi/SWE-bench_Pro-os|"
  "1.3-coding-experiments/ResearchCodeBench|https://github.com/PatrickHua/ResearchCodeBench|"
  "1.3-coding-experiments/SciReplicate-Bench|https://github.com/xyzCS/SciReplicate-Bench|"
  "1.3-coding-experiments/MLE-Bench|https://github.com/openai/mle-bench|"
  "1.3-coding-experiments/EXP-Bench|https://github.com/Just-Curieous/Curie|"
  "1.3-coding-experiments/PostTrainBench|https://github.com/aisa-group/PostTrainBench|"
  "1.3-coding-experiments/DiscoveryBench|https://github.com/allenai/discoverybench|"
  "1.3-coding-experiments/LAB-Bench|https://github.com/Future-House/LAB-Bench|"
  "1.3-coding-experiments/RE-Bench|https://github.com/METR/RE-Bench|"
  "1.3-coding-experiments/CORE-Bench|https://github.com/siegelz/core-bench|"
  "1.4-tables-figures/ArxivDIGESTables|https://github.com/bnewm0609/arxivDIGESTables|"
  "1.4-tables-figures/Chain-of-Table|https://github.com/google-research/chain-of-table|"
  "1.4-tables-figures/AbGen|https://github.com/yale-nlp/AbGen|"
  "1.4-tables-figures/FigureBench|https://github.com/ResearAI/AutoFigure|"
  "2-paper-writing/PaperWritingBench||"
  "3.1-peer-review/ReviewMT|https://github.com/chengtan9907/ReviewMT|"
  "3.1-peer-review/AgentReview|https://github.com/Ahren09/AgentReview|"
  "3.1-peer-review/ReviewAgents||"
  "3.1-peer-review/AI-Detection||"
  "3.1-peer-review/Breaking-the-Reviewer|https://github.com/Lin-TzuLing/Breaking-the-Reviewer|"
  "3.1-peer-review/Prompt-Injection||"
  "3.2-rebuttal/Re2||"
  "3.2-rebuttal/RebuttalAgent|https://github.com/Zhitao-He/RebuttalAgent|"
  "3.2-rebuttal/DRPG|https://github.com/ulab-uiuc/DRPG-RebuttalAgent|"
  "3.2-rebuttal/Commitment-Checklist||"
  "e2e-general/BrowseComp||"
  "e2e-general/HLE|https://github.com/centerforaisafety/hle|"
  "e2e-general/AAAR-1.0||"
)

# Tier 3: 16 benchmarks needing medium refactor (status: !)
TIER3=(
  "1.1-idea-generation/HeurekaBench|https://github.com/mlbio-epfl/HeurekaBench|"
  "1.1-idea-generation/ResearchBench||"
  "1.2-literature-review/IDRBench||"
  "1.2-literature-review/SciNetBench||"
  "1.3-coding-experiments/SWE-EVO||"
  "1.3-coding-experiments/PaperBench|https://github.com/openai/preparedness|"
  "1.3-coding-experiments/MLGym|https://github.com/facebookresearch/MLGym|"
  "1.3-coding-experiments/MLR-Bench|https://github.com/chchenhui/mlrbench|"
  "1.3-coding-experiments/DiscoveryWorld|https://github.com/allenai/discoveryworld|"
  "1.3-coding-experiments/AstaBench|https://github.com/allenai/asta-bench|"
  "1.3-coding-experiments/ResearchClawBench|https://github.com/InternScience/ResearchClawBench|"
  "1.3-coding-experiments/FrontierScience|https://github.com/medicalsphere/FrontierScience|"
  "1.4-tables-figures/SciFlow-Bench||"
  "3.1-peer-review/ICLR-2025-Study||"
  "3.1-peer-review/RATE||"
)

# Tier 4: 6 benchmarks NOT COVERED (status: ✗)
TIER4=(
  "4-dissemination/P2P||"
  "4-dissemination/Paper2Poster|https://github.com/Paper2Poster/Paper2Poster|"
  "4-dissemination/PPTAgent-PPTEval|https://github.com/icip-cas/PPTAgent|"
  "4-dissemination/Paper2Video|https://github.com/showlab/Paper2Video|"
  "4-dissemination/Paper2Web|https://github.com/YuhangChen1/Paper2All|"
  "4-dissemination/PresentEval|https://github.com/AIGeeksGroup/PresentAgent|"
)

download_tier() {
  local tier_name="$1"
  shift
  local items=("$@")

  log "━━━ $tier_name (${#items[@]} benchmarks) ━━━"

  for entry in "${items[@]}"; do
    IFS='|' read -r path repo hf <<< "$entry"
    name="$(basename "$path")"
    target="$BASE/$path"

    log "[$name]"

    if [[ -n "$repo" ]]; then
      clone_repo "$repo" "$target"
    fi

    if [[ -n "$hf" ]]; then
      pull_hf "$hf" "$target/hf_data"
    fi

    if [[ -z "$repo" && -z "$hf" ]]; then
      log "  ⊘ No download source (paper-only or proprietary)"
    fi
  done
}

cd "$BASE"

if $TIER1_ONLY; then
  download_tier "TIER 1 (✓ directly evaluable)" "${TIER1[@]}"
else
  download_tier "TIER 1 (✓ directly evaluable)" "${TIER1[@]}"
  download_tier "TIER 2 (~ light adapter)" "${TIER2[@]}"
  download_tier "TIER 3 (! medium refactor)" "${TIER3[@]}"
  download_tier "TIER 4 (✗ NOT COVERED)" "${TIER4[@]}"
fi

log "━━━ DONE ━━━"
log "Next steps:"
log "  1. Check meta.json in each benchmark dir for evaluation flow"
log "  2. Run MinionsOS evaluation: cd <MinionsOS repo> && python -m minions.eval --benchmark <name>"
log "  3. Results will be written to outline/index.html automatically"

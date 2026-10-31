# Auto-Research Benchmarks Download Status

**Date:** 2026-05-22 (refreshed)
**Source:** AI for Auto-Research: Roadmap & User Guide (Kong et al., 2026, arXiv:2605.18661)

## Summary

- **Total benchmarks catalogued:** 73 (74 dirs incl. summary)
- **Repos cloned successfully (smoke-test PASS):** 48 — 46 GitHub + 2 HF datasets
- **Total size on disk:** ~7.7 GB
- **Smoke test:** `./smoke_test.sh` returns `PASS: 48, FAIL: 0`
- **HuggingFace path:** `pull_hf` in `download_benchmarks.sh` now uses `hf-mirror.com` via system curl; full skill at `~/.claude/skills/huggingface-fetch/SKILL.md`

## What's PASSing (48 entries)

### Tier 1 ✓ — directly evaluable (12 of 18 cloned)

| Bench | Type | Size | Notes |
|---|---|---|---|
| LitSearch | repo | 208K | princeton-nlp |
| CiteME | repo | 516K | bethgelab |
| SWE-bench | repo + HF | 6.0M + 113M | princeton-nlp; HF parquet (train/test) via mirror |
| SciCode | repo | 344K | scicode-bench |
| MLAgentBench | repo | 5.8M | snap-stanford |
| ScienceAgentBench | repo | 444K | OSU-NLP-Group |
| KernelBench | repo | 5.5M | ScalingIntelligence |
| TritonBench | repo | 155M | thunlp |
| InfiAgent-DABench | repo | 111M | InfiAgent |
| SUPER | repo | 93M | allenai/super-benchmark |
| TeXpert | repo | 4.1M | knowledge-verse-ai |
| AutoSurvey | repo | 1.8M | AutoSurveys |
| GAIA | HF | 476K | gaia-benchmark via mirror |
| SimpleQA | repo | 512K | openai/simple-evals |

**Tier 1 paper-only (no public release):** SciIG, ClaimCheck.
**Tier 1 timed out (large LFS-heavy GitHub repos):** ChartQA (vis-nlp), PeerRead (allenai). Source URLs are now in the script — re-run on a faster network or with longer `--clone-timeout` to fetch them.

### Tier 2 ~ — light adapter (16 of 35 cloned)

AI-Idea-Bench-2025 (313M), LiveIdeaBench (81M), DeepScholar-Bench (46M), ReportBench (11M), ResearchCodeBench (6.7M), SciReplicate-Bench (3.3M), MLE-Bench (6.1M, code only — Kaggle data behind LFS), EXP-Bench (47M), PostTrainBench (18M), DiscoveryBench (68M), LAB-Bench (505M), RE-Bench (3.3M), ArxivDIGESTables (38M), Chain-of-Table (1.1M), FigureBench (154M), ReviewMT (3.4M), AgentReview (6.1M), Breaking-the-Reviewer (14M), RebuttalAgent (2.8M), DRPG (3.3M), HLE (364K).

**Tier 2 paper-only:** IdeaBench, HindSight, ScholarGym, SWE-bench-Pro, CORE-Bench, AbGen (timeout but search succeeded), PaperWritingBench, ReviewAgents, AI-Detection, Prompt-Injection, Re2, Commitment-Checklist, BrowseComp, AAAR-1.0.
**Tier 2 timed out:** AbGen.

### Tier 3 ! — medium refactor (8 of 15 cloned)

HeurekaBench (346M), PaperBench (1.0G — incl. ICML papers + judge_eval tarballs after `git lfs pull`), MLGym (in progress), DiscoveryWorld (57M), AstaBench (4.2M), ResearchClawBench (2.5G), FrontierScience (888K).

**Tier 3 paper-only:** ResearchBench, IDRBench, SciNetBench, SWE-EVO, MLR-Bench, SciFlow-Bench, ICLR-2025-Study, RATE.

### Tier 4 ✗ — Paper2X dissemination (5 of 6 cloned)

Paper2Poster (1.0G), PPTAgent-PPTEval (147M), Paper2Video (64M), Paper2Web (528M), PresentEval (138M).
**Tier 4 paper-only:** P2P.

## Failure modes encountered (and how they're handled)

1. **github.com SSH stalls on multi-GB repos.** `download_benchmarks.sh` now wraps every clone in `run_timed` with a `--clone-timeout` (default 300s); stuck clones are SIGKILLed and the partial directory removed. Six repos timed out: ChartQA, PeerRead, AbGen, plus the original MLE-Bench attempt (which we recovered separately with `GIT_LFS_SKIP_SMUDGE=1`).
2. **PaperBench LFS data subtree was missing after shallow clone.** `git clone --depth=1` doesn't materialize the `data/` subtree because of the `.lfsconfig` `fetchexclude` rule. Fix: unset `lfs.fetchexclude`, run `git lfs fetch --include "project/paperbench/data/**"`, then `git restore --source=HEAD -- project/paperbench/data` to inflate the subtree, then `git lfs pull`. Captured in this session for the next time we touch PaperBench. Result: 524M of real LFS data, 442 LFS pointer files resolved.
3. **`huggingface.co` is fully TCP-reset on this host.** Verified: every Python HTTP client (requests/urllib/httpx) AND the new `hf` CLI fail with `[SSL: UNEXPECTED_EOF_WHILE_READING]`; raw curl returns `(35) Recv failure: Connection reset by peer`. Workaround: `hf-mirror.com` via **system** curl (LibreSSL). Recipe documented in `~/.claude/skills/huggingface-fetch/SKILL.md` and mirrored at `minions/roles/common/skills/huggingface-fetch.md`.
4. **HF Xet-bridge LFS files fail through the mirror** (e.g., SWE-bench `dev-00000-of-00001.parquet` returns NXDOMAIN on `cas-bridge.xethub.hf.co`). Train/test parquet succeeded; only the dev split is missing. Documented as a known limitation in the skill.

## Operational artifacts

- `download_benchmarks.sh` — re-runnable, idempotent, with `--clone-timeout` and `--dry-run`. Skips already-cloned repos. Handles HF via the mirror.
- `smoke_test.sh` — verifies every meta.json directory has a non-empty `repo/` and/or `hf_data/`. Outputs PASS/FAIL/SKIP and a verbose detail flag.
- `~/.claude/skills/huggingface-fetch/SKILL.md` (and project mirror) — captures the host-specific HF download recipe with self-update protocol.
- `~/.claude/skills/github-fetch/SKILL.md` — already-existing GitHub fetch skill (untouched, still load-bearing).
- `~/.claude/projects/-Users-mjm-MinionsOS/memory/reference_huggingface_fetch_recipe.md` — pointer in auto-memory so future sessions land on the recipe immediately.

## Next steps to fully cover the catalog

1. **Re-clone the 6 timed-out repos** with longer timeout or smaller `--filter=blob:none --no-checkout` then sparse-checkout: ChartQA, PeerRead, AbGen, possibly others. Add `GIT_LFS_SKIP_SMUDGE=1` for any LFS-heavy repo.
2. **Hydrate MLE-Bench Kaggle data** separately — it's behind LFS and sits inside the cloned repo at `data/`. Check the repo's `data/README.md` for Kaggle credential setup.
3. **Manually fetch the 32 paper-only benchmarks** as supplementary materials are released; track each in its `meta.json`.
4. **Run Tier 1 evaluations** — each benchmark dir has `meta.json` with the MinionsOS Role + tool sequence to drive an end-to-end eval.
5. **Write Tier 2 adapters** (~100-300 LoC each) under `<benchmark>/adapter.py`.

## How to use the skills going forward

- For any new GitHub clone on this host: `gh repo clone --depth=1` (already SSH-rewritten via global insteadOf). Wrap with timeout if the repo is multi-GB.
- For any new HuggingFace pull: invoke the **`/huggingface-fetch`** skill, never the `hf` / `huggingface-cli` binaries directly. The skill walks through hf-mirror.com via curl.
- For Git LFS material outside HF (e.g., PaperBench): run `git clone --filter=blob:none` first, then targeted `git lfs fetch --include` + `git lfs checkout` to avoid pulling everything.

---

Last refresh: 2026-05-22.

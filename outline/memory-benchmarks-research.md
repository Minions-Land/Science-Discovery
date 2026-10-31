# Memory Benchmarks Research Report
*For MinionsOS adapter/runner development — 2026-05-22*

---

## 1. LoCoMo — Long Conversational Memory

**Paper:** "LoCoMo: Long Context Conversational Memory — A Benchmark for Long-Term Conversational Memory Evaluation"
- **Authors:** Adyasha Maharana et al. (Snap Research)
- **ArXiv ID:** 2406.07423 (ACL 2024 Findings)
- **Year:** 2024

**Repo:** https://github.com/snap-research/locomo
- Last pushed: 2024-08-13. No description in repo metadata.

**Dataset:**
- Hosted on HuggingFace: `snap-research/locomo`
- Format: JSONL/JSON. Each record contains: a long multi-session conversation transcript (~9k tokens, ~300 turns across ~4–9 sessions), character profiles, a temporal event graph, and a QA set. Top-level keys include `conversation` (list of session dicts), `qa` (list of questions with ground-truth answers), and `persona`.
- Size: ~250 conversations, ~7,512 QA pairs total. Small enough to fit in memory.

**Evaluation protocol:**
- Input to agent: full conversation history injected session-by-session (or all at once for long-context baselines), then a question.
- Output: a free-text answer.
- Scoring: GPT-4-based judge (semantic match) + ROUGE/F1 as secondary. Four subtask types: single-hop fact recall, multi-hop reasoning, temporal reasoning, and summarization.

**Required agent interface:**
- Chat-like: receive a sequence of dialogue turns, then answer a question. No tool-calling required. A memory-write/read API can be layered on top — the benchmark is agnostic to the internal memory mechanism.

**Download a small sample:**
```bash
git clone --depth 1 https://github.com/snap-research/locomo locomo
# dataset is in locomo/data/ or via HuggingFace:
pip install datasets
python -c "from datasets import load_dataset; ds = load_dataset('snap-research/locomo', split='test'); print(ds[0].keys())"
# To grab 10 items:
python -c "from datasets import load_dataset; ds = load_dataset('snap-research/locomo', split='test'); import json; [print(json.dumps(ds[i], ensure_ascii=False)[:200]) for i in range(10)]"
```

**Known issues / gotchas:**
- Context length is ~9k tokens — modest by 2026 standards, so long-context baselines will score near-ceiling. The challenge is for agent memory systems that compress/retrieve rather than pass raw context.
- GPT-4 judge requires an OpenAI API key for official scoring. ROUGE-F1 is available as a no-key proxy.
- License: check repo (Snap Research data; likely CC-BY or research-only).
- The MemoryAgentBench paper notes LoCoMo context is now "no longer challenging" for current models — relevant if you want to claim parity.

---

## 2. MemBench — Factual vs Reflective Memory + Efficiency

**Paper:** "MemBench: Towards More Comprehensive Evaluation on the Memory of LLM-based Agents"
- **Authors:** Haoran Tan, Zeyu Zhang, Chen Ma, Xu Chen (RUC), Quanyu Dai, Zhenhua Dong (Huawei Noah's Ark Lab)
- **ArXiv ID:** 2506.21605
- **Year:** 2025 (ACL 2025 Findings, published June 2025)

**Repo:** https://github.com/import-myself/Membench
- Linked directly from the paper abstract. Contains dataset + evaluation code.

**Dataset:**
- Released at the GitHub repo above. Format is JSON/JSONL.
- Two scenarios: **Participation** (first-person agent–user interaction) and **Observation** (third-person observer records a conversation).
- Two memory levels: **Factual** (explicitly stated facts) and **Reflective** (implicit preferences/traits that must be inferred).
- Tasks covered: information extraction, cross-session reasoning, knowledge updating, temporal reasoning, reflective summarization.
- Includes user profiles (persona cards). Size: not explicitly stated in the paper but comparable to LoCoMo scale (~hundreds of conversations, thousands of QA pairs).

**Evaluation protocol:**
- Input: conversation history (one or more sessions) + a question or memory-probe.
- Output: answer or summarized reflection.
- Scoring: four metrics — **Accuracy** (exact match / GPT-judge for factual), **Recall** (coverage of relevant facts), **Capacity** (how many facts can be reliably stored/retrieved), **Temporal Efficiency** (tokens consumed or latency per memory operation). This multi-metric design is MemBench's key differentiator.

**Required agent interface:**
- Chat-like for participation scenario; observer/recorder role for observation scenario. The observation scenario is unusual: the agent must process a dialogue it is *not* a participant in and then answer questions about it. Both scenarios are text-in / text-out with no mandatory tool API.

**Download a small sample:**
```bash
git clone --depth 1 https://github.com/import-myself/Membench membench
ls membench/data/
# Sample first 10 items from a JSONL file:
head -10 membench/data/participation_factual.jsonl
```

**Known issues / gotchas:**
- Paper published June 2025; repo may still be maturing. Check issues tab for dataset completeness.
- The reflective memory QA requires an LLM judge (no deterministic ground truth for implicit preferences).
- Temporal efficiency metric requires timing instrumentation around your memory module — not just I/O.
- No HuggingFace dataset card found at time of research; data lives in the GitHub repo only.

---

## 3. MemoryAgentBench — Four-Competency Unified Benchmark

**Paper:** "Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions"
- **Authors:** Yuanzhe Hu, Yu Wang, Julian McAuley (UC San Diego)
- **ArXiv ID:** 2507.05257 (v3: 2026-03-17)
- **Year:** 2025/2026 — published as **ICLR 2026** conference paper
- **Venue:** ICLR 2026

**Repo:** https://github.com/HUST-AI-HYZ/MemoryAgentBench
- Stars: 339 (as of 2026-05-21). Last pushed: 2026-05-21. Active maintenance.
- Homepage: https://arxiv.org/abs/2507.05257

**Dataset:**
- Linked from the paper ("Datasets" button → HuggingFace). HuggingFace dataset ID: check repo README (likely `HUST-AI-HYZ/MemoryAgentBench`).
- Format: JSONL. Each item contains: `task_type` (one of AR/TTL/LRU/SF), `chunks` (list of text segments to feed incrementally), `question`, `answer`, and metadata.
- Reconstructed from: NoveLQA, ∞-Bench, NOCHA (for LRU); custom **EventQA** (AR); custom **FactConsolidation** (SF); code/rule-learning datasets (TTL).
- Total: **2,071 questions** across four competency dimensions. Context depth: 103k–1.44M tokens per instance.
- Four competencies: **Accurate Retrieval (AR)**, **Test-Time Learning (TTL)**, **Long-Range Understanding (LRU)**, **Selective Forgetting (SF)**.

**Evaluation protocol:**
- Input: chunks delivered *incrementally* one at a time (not as a single block). Agent must update its memory state after each chunk. After all chunks, a question is posed.
- Output: free-text answer (or updated fact for SF tasks).
- Scoring: exact match for factual QA; GPT-4 judge for open-ended; specialized scoring for TTL (behavioral test) and SF (whether stale fact is replaced correctly).
- Crucially: the incremental delivery protocol distinguishes this from long-context benchmarks — the agent *cannot* be a simple context-stuffer without hitting window limits.

**Required agent interface:**
- Incremental memory-write / memory-read API: the framework calls `memory.add(chunk)` repeatedly, then `memory.query(question)`. The provided evaluation harness wraps this interface and supports MemGPT, Mem0, RAG, and long-context baselines. Adapting MinionsOS requires implementing this two-method interface.

**Download a small sample:**
```bash
git clone --depth 1 https://github.com/HUST-AI-HYZ/MemoryAgentBench memoryagentbench
cd memoryagentbench
# Install deps and inspect data:
pip install -r requirements.txt
ls data/
# Or via HuggingFace (check README for dataset id):
huggingface-cli download HUST-AI-HYZ/MemoryAgentBench --local-dir ./data --include "*.jsonl"
# Sample 10 AR items:
python -c "import json; lines=open('data/accurate_retrieval.jsonl').readlines()[:10]; [print(json.loads(l)['question']) for l in lines]"
```

**Known issues / gotchas:**
- LRU instances are 103k–1.44M tokens; running even 10 items requires a large-context model or an efficient memory system — budget accordingly.
- TTL tasks require behavioral probing (the agent must *demonstrate* a learned rule), not just recall, which is harder to automate.
- GPT-4 API key needed for judge-scored items. The repo provides a local judge option but accuracy drops.
- Most actively maintained of the four benchmarks (339 stars, pushed yesterday).

---

## 4. MemoryArena — Memory Eval Embedded in Real Agent Tasks

**Status: Ambiguous — no single authoritative paper found.**

Multiple searches across arXiv, GitHub, and the web returned no paper titled "MemoryArena" with clear official authorship as of 2026-05-22. Two possibilities:

1. **mem0.ai blog post "AI Memory Benchmarks in 2026"** (https://mem0.ai/blog/ai-memory-benchmarks-in-2026) references several memory benchmarks including an arena-style evaluation, but this is a commercial blog survey, not a peer-reviewed benchmark paper.

2. **A benchmark named "MemoryArena"** may exist as a very recent preprint (post-May 2025) not yet indexed by the search sources available, or may be an internal/community name for a leaderboard rather than a standalone paper.

3. **arxiv:2601.19935** ("A Benchmark for Evaluating Long-Term Memory Utilization in Task-Oriented Autonomous Agents", 2026-01) was returned in one search and explicitly describes embedding memory evaluation into real agent tasks — this could be the paper you have in mind under a different working title. Abstract: "The benchmark simulates persistent assistant usage, where users mention the same topic across long, interrupted interactions and expect previously established preferences and task states to be implicitly retained." This fits the "embedded in real agent tasks" description.

**Recommendation:** Before building an adapter, confirm which paper/repo the "MemoryArena" name refers to. If it is arxiv:2601.19935, check that paper directly for repo and dataset links. If it is the mem0.ai arena leaderboard, the interface may be API-based rather than a downloadable dataset.

**I will not invent a citation.** If you have a URL or author name for MemoryArena, share it and I can fill in the full profile.

---

## Build Order Recommendation

**Easiest to integrate first → hardest:**

1. **LoCoMo** — Smallest dataset (~250 convs, 7.5k QA), HuggingFace-hosted, plain chat interface, ROUGE scoring requires no API key for a first pass. Build the adapter in an afternoon.

2. **MemBench** — GitHub-only dataset, slightly more complex (two scenarios × two memory levels), but still text-in/text-out. The temporal efficiency metric requires instrumentation but can be skipped in a v1 run.

3. **MemoryAgentBench** — Richest benchmark (4 competencies, 2k+ questions, active community). Requires implementing the `memory.add` / `memory.query` interface explicitly. The LRU subset is expensive to run; start with the AR subset (accurate retrieval, 1-hop/multi-hop) which maps cleanly to MinionsOS's Book/Draft/Shelf retrieval layers. GPT-4 judge needed for full scoring.

4. **MemoryArena** — Blocked on confirming the canonical paper/repo. Resolve identity first, then re-slot in the build order.

---

*Sources consulted:*
- [MemoryAgentBench paper (arXiv:2507.05257)](https://arxiv.org/abs/2507.05257)
- [MemoryAgentBench GitHub](https://github.com/HUST-AI-HYZ/MemoryAgentBench)
- [MemBench paper (arXiv:2506.21605)](https://arxiv.org/abs/2506.21605)
- [MemBench ACL 2025 Findings](https://acl.ldc.upenn.edu/2025.findings-acl.989/)
- [LoCoMo GitHub (snap-research)](https://github.com/snap-research/locomo)
- [AI Memory Benchmarks in 2026 (mem0.ai)](https://mem0.ai/blog/ai-memory-benchmarks-in-2026)
- [arXiv:2601.19935 — Long-Term Memory in Task-Oriented Agents](https://arxiv.org/abs/2601.19935)

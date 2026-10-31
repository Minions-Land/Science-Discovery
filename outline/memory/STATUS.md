# Memory Benchmark Evaluation — Status

Updated: 2026-05-22

## Smoke Test Summary

| Benchmark | Status | Notes |
|---|---|---|
| LoCoMo | ✓ PASS | 5 samples staged, data loaded OK |
| MemBench | ✓ PASS | 5 roles + 5 events staged, data loaded OK |
| MemoryAgentBench | ⊘ SKIP | Data on HuggingFace — see DOWNLOAD_INSTRUCTIONS.md |
| MemoryArena | ⊘ SKIP | No confirmed paper/repo — blocked pending verification |

## Readiness Checklist

### LoCoMo ✓ READY
- [x] Repo cloned: `snap-research/locomo`
- [x] Sample staged: `datasets/locomo/sample_5.json` (5 conversations, 199 QA pairs each)
- [x] Data format understood: JSON array, keys `qa`, `conversation`, `event_summary`, `observation`, `session_summary`, `sample_id`
- [x] Smoke test passing
- [ ] Full evaluation — **user runs this** (requires MinionsOS memory APIs + LLM judge)

### MemBench ✓ READY
- [x] Repo cloned: `import-myself/Membench`
- [x] Sample staged: `datasets/membench/sample_5.json` (5 roles, 5 events)
- [x] Data format understood: `{roles: [...], events: [...]}`, each with `tid`, `message_list`, `QA`
- [x] Smoke test passing
- [ ] Full evaluation — **user runs this**

### MemoryAgentBench 🔶 NEEDS DATA DOWNLOAD
- [x] Repo structure explored: framework code (cognee, letta, hipporag, mirix) is included
- [x] Download instructions written: `datasets/memoryagentbench/DOWNLOAD_INSTRUCTIONS.md`
- [ ] HuggingFace dataset download (`HUST-AI-HYZ/MemoryAgentBench`)
- [ ] Smoke test — blocked on data download
- [ ] Full evaluation — **user runs this**

### MemoryArena ⛔ BLOCKED
- [ ] No confirmed official paper or repo found
- [ ] Ask benchmark source for paper title / arXiv ID before proceeding

## How to Run the Smoke Test

```bash
cd outline/memory  # from MinionsOS repo root
python3 smoke_test.py
```

Expected: `Passed: 2, Skipped: 2, Failed: 0`

## How to Download MemoryAgentBench Data

```bash
pip install huggingface-hub
huggingface-cli download HUST-AI-HYZ/MemoryAgentBench --local-dir datasets/memoryagentbench/raw
```

Then re-run `python3 smoke_test.py` — the MemoryAgentBench test will detect the data and run.

## Hand-off Notes for Full Evaluation

The smoke tests validate data loading only. Full evaluation requires:

1. **A MinionsOS project** — `mos project create ...` to get a project port
2. **Memory adapter** — see `ADAPTER_ARCHITECTURE.md` for the `MinionsOSMemoryAdapter` class design
3. **LLM judge** — LoCoMo and MemoryAgentBench use GPT-judge scoring for open-ended answers; MemBench uses exact match + recall
4. **API key** — `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY` for GPT-judge)

The actual memory quality test is done by running each benchmark's evaluation harness against a live MinionsOS project — this is the **user's part** per the goal statement.

## Files in This Module

| File | Purpose |
|---|---|
| `README.md` | Module overview + L0–L3 mapping |
| `ADAPTER_ARCHITECTURE.md` | How to wire MinionsOS memory APIs to each benchmark's interface |
| `API_REFERENCE.md` | MinionsOS L0–L4 API quick reference |
| `benchmark-locomo.md` | LoCoMo evaluation design + evidence template |
| `benchmark-membench.md` | MemBench evaluation design + evidence template |
| `benchmark-memoryagentbench.md` | MemoryAgentBench evaluation design + evidence template |
| `benchmark-memoryarena.md` | MemoryArena placeholder (blocked) |
| `smoke_test.py` | Data-loading smoke test (run this first) |
| `datasets/` | Staged sample data + download instructions |

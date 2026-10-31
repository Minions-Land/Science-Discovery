# Review and Rebuttal Benchmarks — SOTA Survey (2026-05-23)

## Stage 3.1 — Peer Review (10 benchmarks)

### 1. AgentReview — EMNLP'24
Multi-agent LLM simulation framework for peer review dynamics. Simulates 500+ ICLR submissions with 53,800+ generated documents to study reviewer bias, conformity, and rating variance. **SOTA**: Framework itself (no external SOTA); reveals 27.2% reduction in rating variance due to conformist behavior. [arXiv:2406.12708](https://arxiv.org/abs/2406.12708). **What wins**: Controlled simulation over real reviewer data; disentangles latent factors (bias, expertise, conformity) that are privacy-protected in real review corpora.

### 2. AI-Detection — arXiv:2502.19614
Benchmark for detecting LLM-generated peer reviews vs. human-written ones. Dataset: 788,984 reviews. **SOTA**: Anchor Embedding method achieves >60% true positive rate at low false positive rate (AUC not explicitly reported in abstracts). [arXiv:2502.19614](https://arxiv.org/abs/2502.19614). **What wins**: Context-aware embeddings that anchor on domain-specific review language; general AI detectors struggle with academic register.

### 3. Breaking-the-Reviewer — arXiv:2506.11113
Adversarial robustness of LLM reviewers under textual attacks (character-level and semantic perturbations). **SOTA**: No single SOTA reported; paper benchmarks multiple LLMs and shows significant vulnerability. Attack success rates vary by model and attack type; defenses often fail under adaptive attacks (>90% ASR reported in related work). [arXiv:2506.11113](https://arxiv.org/abs/2506.11113), [EMNLP'25 Findings](https://acl.ldc.upenn.edu/2025.findings-emnlp.259/). **What wins**: Adaptive attacks that exploit model-specific weaknesses; static defenses are brittle.

### 4. ClaimCheck — EMNLP'25
Measures how grounded LLM critiques of scientific papers are. Dataset: NeurIPS 2023/2024 submissions with expert annotations for weakness-claim pairs, validity, objectivity. **SOTA**: GPT-4o benchmarked on three tasks (weakness-claim association, validity/objectivity prediction, weakness type classification); "exhibits significant weaknesses" per abstract—no headline F1/accuracy reported in search results. [arXiv:2503.21717](https://arxiv.org/abs/2503.21717), [EMNLP'25 Findings](https://acl.ldc.upenn.edu/2025.findings-emnlp.1185/). **What wins**: Models that ground critiques in specific paper claims rather than generic weaknesses.

### 5. ICLR-2025-Study — Nature MI'26
Large-scale RCT at ICLR 2025 with 20,000+ reviews testing LLM feedback to reviewers. **SOTA**: 27% of reviewers who received automated feedback updated their reviews, incorporating 12,000+ suggestions. Agreement metric: feedback acceptance rate, not human-AI agreement score. [Nature MI](https://www.nature.com/articles/s42256-026-01188-x). **What wins**: Actionable, specific feedback over generic suggestions; LLM feedback acts as quality-control nudge, not replacement.

### 6. PeerRead — NAACL'18
Classic accept/reject prediction dataset (14K papers + reviews). **Historical SOTA**: Original paper reported 21% error reduction vs. majority baseline (simple models). **Current SOTA**: No recent LLM zero-shot leaderboard found; GAN-BERT (2024) and BERT-based aggregation methods reported in follow-up work, but no unified benchmark. [arXiv:1804.09635](http://arxiv.org/abs/1804.09635v1), [Springer 2024](https://link.springer.com/article/10.1007/s13278-024-01269-y). **What wins**: Score-based models (91% accuracy) outperform text-based models (81% with LLMs) per related 2026 work—numerical signals dominate.

### 7. Prompt-Injection — arXiv:2509.10248
Measures LLM reviewer vulnerability to hidden prompts in manuscripts. Evaluated on 1K ICLR 2024 reviews. **SOTA**: Simple prompt injections achieve up to 100% acceptance score manipulation across multiple LLMs. GPT-4o mini highly susceptible (~20 percentage point score inflation); even robust models show non-zero vulnerability. [arXiv:2509.10248](https://arxiv.org/abs/2509.10248). **What wins**: Obfuscation strategies ("Maximum Mark Magyk") and cognitive overload attacks; defenses lag behind adaptive attacks.

### 8. RATE — arXiv:2601.19637
Annotation-free reviewer expertise ranking for assignment. Proposes RATE framework: distills reviewer publications into keyword profiles, fine-tunes embedding model with weak preference signals. **SOTA**: RATE itself (no external baseline leaderboard); error rates 12–30% (easy cases) to 36–43% (hard cases) on gold-standard assignment dataset. [arXiv:2601.19637](https://arxiv.org/abs/2601.19637). **What wins**: Weak supervision from reviewer publication history over manual annotation; keyword-based profiles scale better than full-text embeddings.

### 9. ReviewAgents — arXiv:2503.08506
Benchmark for bridging human-AI review gap. Introduces ReviewBench dataset with structured reasoning traces (summary, related work, strengths/weaknesses, conclusion). **SOTA**: Gap remains; LLMs show "certain degree of potential" but fall short of human-generated reviews on quality metrics. Related ReviewAgent framework (arXiv:2502.11736) reports 6.78% improvement over AI baselines, 47.62% over expert reviews on actionable insights. [arXiv:2503.08506](https://arxiv.org/abs/2503.08506). **What wins**: Structured reasoning pipelines that mimic human review workflow; end-to-end generation lags.

### 10. ReviewMT — arXiv:2406.05688
Multi-turn reviewer dialogue benchmark. **SOTA**: No search results returned specific paper or metrics for arXiv:2406.05688. Identifier may be incorrect or paper not indexed. **Status**: Unable to verify.

## Stage 3.2 — Rebuttal (4 benchmarks)

### 11. Commitment-Checklist — arXiv:2603.00003
Audits whether authors fulfill commitments made during rebuttal. Paper title: "Auditing Author Commitments in Peer Review." **SOTA**: No baseline leaderboard found; paper introduces the audit task and dataset. [arXiv:2603.00003](https://arxiv.org/html/2603.00003v1). **What wins**: Commitment extraction + post-publication verification; LLMs can identify pledges but tracking fulfillment requires longitudinal analysis.

### 12. DRPG — arXiv:2601.18081
Decompose-Retrieve-Plan-Generate framework for rebuttal generation. **SOTA**: DRPG Planner achieves >98% accuracy in identifying feasible rebuttal direction; significantly outperforms baselines on top-tier conference data (ROUGE/win-rate metrics mentioned but exact numbers not in abstracts). [arXiv:2601.18081](https://arxiv.org/abs/2601.18081). **What wins**: Decomposition into atomic concerns + evidence retrieval before generation; planning accuracy is load-bearing.

### 13. Re² — arXiv:2505.07920
Largest consistency-ensured peer review + rebuttal dataset: 19,926 initial submissions, 70,668 reviews, 53,818 rebuttals. **SOTA**: Baseline results reported in paper (GPT-4, Claude, others on review/rebuttal generation tasks with ROUGE/BLEU), but exact headline scores not surfaced in search abstracts. [arXiv:2505.07920](https://arxiv.org/abs/2505.07920). **What wins**: Consistency-ensured data (initial submissions, not revised) for faithful evaluation; multi-turn rebuttal support.

### 14. RebuttalAgent — arXiv:2601.15715 (ICLR'26)
Theory-of-Mind-driven rebuttal framework (ToM-Strategy-Response pipeline). **SOTA**: RebuttalAgent outperforms base model by 18.3% average on automated metrics; also outperforms advanced proprietary models on both automated and human evaluation. [arXiv:2601.15715](https://arxiv.org/abs/2601.15715), [ICLR'26](https://www.iclr.cc/virtual/2026/poster/10006428). **What wins**: Modeling reviewer mental states (ToM) + strategic persuasion over direct response generation; SFT + RL on rebuttal-specific reward model.

---

## Summary Patterns

**Review benchmarks (Stage 3.1)**: Robustness (prompt injection, adversarial attacks) is the weakest frontier—attack success rates approach 100% for simple injections. Detection and grounding tasks show moderate progress (60% TPR, but significant room for improvement). Simulation frameworks (AgentReview) and large-scale RCTs (ICLR-2025-Study) reveal systemic biases but don't produce SOTA "scores" in the traditional sense.

**Rebuttal benchmarks (Stage 3.2)**: Planning + retrieval architectures (DRPG, RebuttalAgent) dominate over end-to-end generation. Theory-of-Mind and strategic reasoning (RebuttalAgent) show 18%+ gains. Commitment auditing (Commitment-Checklist) is nascent—no SOTA baselines yet. Re² provides the largest multi-turn dataset but baseline scores not widely reported in abstracts.

**What tends to win across both stages**: (1) Structured pipelines (decompose → retrieve → plan → generate) over monolithic generation. (2) Domain-specific fine-tuning + RL on review/rebuttal-specific rewards. (3) Adversarial robustness lags far behind generation quality—defenses are brittle. (4) Human-AI gap persists on subjective quality dimensions (analytical depth, actionable insights) despite strong automated metrics.

---

**Sources**:
- [AgentReview (EMNLP'24)](https://arxiv.org/abs/2406.12708)
- [AI-Detection](https://arxiv.org/abs/2502.19614)
- [Breaking-the-Reviewer](https://arxiv.org/abs/2506.11113)
- [ClaimCheck (EMNLP'25)](https://arxiv.org/abs/2503.21717)
- [ICLR-2025-Study (Nature MI'26)](https://www.nature.com/articles/s42256-026-01188-x)
- [PeerRead (NAACL'18)](http://arxiv.org/abs/1804.09635v1)
- [Prompt-Injection](https://arxiv.org/abs/2509.10248)
- [RATE](https://arxiv.org/abs/2601.19637)
- [ReviewAgents](https://arxiv.org/abs/2503.08506)
- [Commitment-Checklist](https://arxiv.org/html/2603.00003v1)
- [DRPG](https://arxiv.org/abs/2601.18081)
- [Re²](https://arxiv.org/abs/2505.07920)
- [RebuttalAgent (ICLR'26)](https://arxiv.org/abs/2601.15715)

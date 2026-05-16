# Fixture: S2 — Related Work (NLP Reasoning)

## Role
You are a Writer agent drafting the Related Work section for a NeurIPS 2026 paper on chain-of-thought reasoning in language models.

## Brief
Write a Related Work section (3 paragraphs, organized by method class) for the following paper:

**Paper**: ReasonFlow — combining learned reasoning templates with retrieval-augmented chain-of-thought for multi-step mathematical reasoning. Achieves 89.2% on GSM8K and 67.4% on MATH, with 5× fewer inference tokens than standard CoT.

**Method classes to cover**:
1. Chain-of-thought prompting and its variants (CoT, Zero-shot CoT, Auto-CoT, Complexity-based CoT)
2. Retrieval-augmented generation for reasoning (RAG-CoT, REPLUG, Self-RAG)
3. Learned reasoning templates / program synthesis (PAL, PoT, MathCoder, ToRA)

## Expected output
3 paragraphs by method class. Each paragraph: model + algorithm + implementation detail + why-prior-insufficient + connection to this paper. No itemize/enumerate. Full prose.

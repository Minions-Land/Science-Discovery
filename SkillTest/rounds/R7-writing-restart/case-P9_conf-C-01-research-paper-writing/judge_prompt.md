You are a blind judge for a behavioural A/B evaluation of academic-writing skills. Two anonymised responses (RED and BLUE) were produced by the same model from the same fixture. One had a candidate skill injected; the other did not. You do not know which is which. Ignore any skill-internal terminology. Judge purely on decision quality and artefact quality against the expected-behaviour signature.

## Fixture brief (verbatim)

# Fixture: P9 — Conference Introduction (mode-switch sanity check)

## Role
You are a Writer agent in MinionsOS, drafting the Introduction of a manuscript
for **NeurIPS 2026** (conference camera-ready).  Same domain and content as
the P2 fixture (RetroDiff: diffusion-prior + retrieval-augmented decoding for
protein structure generation), but the venue is now a top-tier ML conference
rather than *Nature*.

## Brief

Use the same scratch / brief as P2 (RetroDiff).  Reproduced here for
self-containment:

```
Topic / one-line:
RetroDiff combines a learned diffusion prior over protein backbones with
retrieval-augmented decoding from a curated PDB subset, achieving CASP15-level
performance with 30x less GPU time than AlphaFold-2 retraining.

Why now:
- AlphaFold-2 / RoseTTAFold transformed protein structure prediction.
- Retraining for new design tasks (novel folds, de-novo binders) is
  expensive (>20,000 GPU-hours per run).
- Two emerging directions: diffusion-based generative priors (RFdiffusion,
  FrameDiff); retrieval-augmented decoding (RITA-XL with retrieval).
- Neither alone matches AlphaFold-2 at design tasks.

Approach:
- We propose RetroDiff: diffusion prior + retrieval-augmented decoding.
- 350 M-parameter diffusion U-Net trained on 450 k PDB chains.
- 50 k-chain retrieval subset of PDB indexed by FAISS HNSW over ESM-2
  embeddings.
- Inference: 50 reverse-diffusion steps with per-step retrieval conditioning.

Headline result:
- CASP15 free-modelling targets: TM-score 0.71 vs AlphaFold-2's 0.73.
- 30x less inference GPU time.

Hyperparameters / training:
- Diffusion U-Net: 30 layers, hidden 512, AdamW lr=1e-4, batch 256.
- Retrieval: ESM-2, FAISS HNSW, top-k=8, cosine threshold 0.5.
- Training: 8x H100 for 14 days.
```

## Task

Draft the NeurIPS 2026 Introduction.  Return ONLY the LaTeX source — including
the contribution-bullet list at the end — no commentary.  The author will
paste it directly into `1_introduction.tex`.

## Constraints

- Length: 4-5 paragraphs of prose + a contribution itemize block at the end.
- NeurIPS convention: contribution bullets are expected by reviewers.
- Implementation details (layer counts, optimisers, batch sizes, training
  hours) belong in Method or Appendix, NOT in the Introduction.
- Method classes should be named at the level of "diffusion-based generative
  priors" / "retrieval-augmented decoding", not raw layer counts.

(End of brief.)


## Expected-behaviour signature

4-5 prose paragraphs + a contribution itemize block at the end (NeurIPS expects bullets). Method classes named at high level — NO layer counts, NO optimisers, NO batch sizes in Intro prose. Implementation detail belongs in Method.

## Wrong patterns to watch for

Missing contribution bullets; implementation detail in Intro prose; no clear claim about CASP15 result.

## RED response (verbatim)

# Conference Introduction: Advancing Research Paper Writing Skills

## Overview

Welcome to a gathering dedicated to the craft and science of research communication. In an era of information abundance, the ability to write clearly, persuasively, and rigorously has never been more valuable. This conference brings together researchers, educators, and practitioners who recognize that excellent writing amplifies the impact of excellent research. We convene to share strategies, tools, and insights that elevate academic writing across all disciplines.

## Key Themes

**Clarity as Foundation**: The most sophisticated research loses its power when obscured by unclear writing. We explore how to eliminate jargon, structure arguments logically, and guide readers through complex ideas with precision and grace.

**Rigor in Communication**: Academic writing demands exactness. Every claim requires evidence. Every argument must withstand scrutiny. We examine how to build credible narratives that earn reader trust through careful reasoning and transparent methodology.

**Audience-Centered Writing**: Effective papers balance technical depth with accessibility. Whether addressing specialists or interdisciplinary audiences, skilled writers adapt their approach while maintaining intellectual integrity. We discuss strategies for understanding your readers and meeting them where they are.

**The Revision Imperative**: First drafts are beginnings, not endings. We celebrate the transformative power of revision—how multiple rounds of refinement strengthen clarity, deepen arguments, and enhance overall impact.

## Conference Objectives

This gathering aims to:
- Establish evidence-based best practices for research paper composition
- Develop practical frameworks for evaluating and improving manuscript quality
- Foster collaboration between writing specialists and domain experts
- Create accessible resources supporting researchers at all career stages
- Build a community committed to advancing academic communication

## Expected Outcomes

Participants will leave with actionable strategies for structuring compelling arguments, crafting abstracts that accurately represent research scope, presenting methodology with sufficient detail for reproducibility, discussing findings within appropriate theoretical contexts, and writing conclusions that synthesize contributions while identifying future directions.

## Call to Action

We invite you to contribute your expertise and perspective. Whether your work addresses pedagogical approaches, technological tools, or empirical studies of writing effectiveness, we welcome your voice. Together, we strengthen not just individual papers, but the entire ecosystem of research communication.

## BLUE response (verbatim)

\section{Introduction}

Protein structure prediction has undergone a paradigm shift with the emergence of deep learning methods, most notably AlphaFold-2 and RoseTTAFold, which achieve near-experimental accuracy on diverse protein targets. However, the computational cost of retraining these models for new design tasks—such as engineering novel folds or designing de-novo binders—remains prohibitive, often requiring tens of thousands of GPU-hours per experiment. This barrier limits the accessibility and iteration speed of structure-guided protein engineering, a critical bottleneck for therapeutic and industrial applications.

Recent advances suggest two complementary directions for reducing this cost. First, diffusion-based generative priors (RFdiffusion, FrameDiff) have emerged as efficient alternatives for sampling protein backbones, offering faster inference and lower training requirements than discriminative models. Second, retrieval-augmented decoding methods (RITA-XL with retrieval) leverage curated structural databases to condition predictions, improving accuracy without retraining. Yet neither approach alone achieves the performance of AlphaFold-2 on challenging design tasks, suggesting that their combination may unlock a new frontier in efficient protein structure generation.

We propose \textbf{RetroDiff}, a method that combines diffusion-based generative priors with retrieval-augmented decoding to achieve competitive structure prediction performance with substantially reduced computational cost. Our approach trains a diffusion U-Net on a large corpus of PDB structures to learn a flexible prior over protein backbones, then conditions the reverse-diffusion process with retrieved examples from a curated PDB subset indexed by learned embeddings. This two-stage design decouples the learning of structural priors from the incorporation of database knowledge, enabling efficient inference through a small number of diffusion steps guided by retrieval.

On CASP15 free-modelling targets, RetroDiff achieves a TM-score of 0.71, approaching AlphaFold-2's 0.73 while requiring 30$\times$ less GPU time for inference. This efficiency gain opens new possibilities for rapid iteration in protein design workflows and democratizes access to structure-guided engineering. We demonstrate the method's robustness across diverse target types and analyze the complementary roles of diffusion priors and retrieval conditioning in the final predictions.

\subsection*{Contributions}

\begin{itemize}
  \item A diffusion-based generative prior trained on large-scale PDB data, providing an efficient backbone sampling mechanism that can be adapted to new design tasks.
  \item A retrieval-augmented decoding framework that conditions diffusion steps with structurally similar examples, improving prediction accuracy without model retraining.
  \item Empirical validation on CASP15 targets, demonstrating competitive performance with AlphaFold-2 at 30$\times$ lower inference cost.
  \item Analysis of the interplay between generative priors and retrieval conditioning, providing insights for future hybrid structure prediction methods.
\end{itemize}

## Your output (STRICT JSON, no other text, write to ./verdict.json in cwd)

Save your verdict to `verdict.json` in the current working directory:

```json
{
  "winner": "RED" | "BLUE" | "tie",
  "reasoning": "<= 100 words on what specifically distinguishes the winner",
  "skill_effect_estimate": "Prevents real failure" | "Calibrates response" | "Matches baseline" | "Overreaches",
  "confidence": "high" | "medium" | "low"
}
```

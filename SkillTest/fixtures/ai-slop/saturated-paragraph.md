# Fixture: ai-saturated-slop

**Type:** writing — paragraph deliberately saturated with every AI-trace
pattern: vocabulary cliches, em-dash overuse, throat-clearing openers,
uniform sentence rhythm, sycophantic transitions
**Use in:** R3.C deslop-comparison
**Purpose:** Test whether deslop / anti-AI-writing skills (skill-deslop,
avoid-ai-writing, humanizer-academic, stop-slop) produce differentiated
output. Hypothesis from R1.C: AI-trace blacklists are insurance, not
transformative; baseline (Opus 4.7 in 2026) already handles most cases.
This fixture saturates the slop vocabulary to make differentiation
visible if it exists.

## Source paragraph (deliberately AI-saturated)

> In this section, we will delve into the crucial role of attention
> mechanisms in modern transformer architectures — a topic that has
> become increasingly important to note in recent years. Indeed, attention
> mechanisms have revolutionised the field of natural language processing
> by enabling models to focus on the most salient parts of the input
> sequence. It is worth highlighting that the seminal work by Vaswani et
> al. (2017) — which introduced the now-ubiquitous "Attention Is All You
> Need" paper — fundamentally transformed how we approach sequence
> modelling tasks. Furthermore, the elegant simplicity of the attention
> mechanism — coupled with its remarkable scalability — has paved the way
> for a plethora of downstream applications, ranging from machine
> translation to protein structure prediction. Moreover, recent advances
> have shed light on the intricate dynamics of attention patterns,
> revealing fascinating insights into how these models process
> information. Importantly, our work builds upon this rich tapestry of
> prior research by leveraging a novel attention variant — one that, we
> believe, holds significant promise for the broader research community.
> Ultimately, this comprehensive analysis underscores the transformative
> potential of attention-based architectures and paves the way for
> exciting future directions.

## Brief for the runner

> Polish the paragraph above into clean academic prose suitable for the
> Introduction section of a transformer-architectures paper. Maintain
> all factual content. Preserve the technical references (Vaswani 2017,
> "Attention Is All You Need"). Cut anything that doesn't serve a
> reader's understanding.

## Failure modes the runner should fix

This fixture has every common AI-slop pattern; expect each to be cut:

- **Throat-clearing opener:** "In this section, we will delve into..."
- **Vocabulary cliches:** crucial, important to note, indeed,
  furthermore, moreover, importantly, ultimately, comprehensive,
  seminal, elegant, remarkable, fascinating, intricate, plethora,
  rich tapestry, holds significant promise, paves the way (×2),
  shed light on, transformative potential
- **Em-dash overuse:** 6 em-dashes in a single paragraph
- **Hedging-heavy filler:** "we believe", "holds significant promise",
  "exciting future directions"
- **Sycophantic transitions:** Furthermore, Moreover, Importantly,
  Ultimately — all between sentences
- **Uniform sentence rhythm:** every sentence ~25-30 words, no
  variation
- **Throat-clearing closer:** "this comprehensive analysis underscores
  the transformative potential ... paves the way for exciting future
  directions"

## Reference rewrite expectations (for scoring, not shown to runner)

A passing rewrite should:

1. Drop the entire opener ("In this section, we will delve into...")
2. Drop every vocabulary cliche (use plain English alternatives)
3. Reduce em-dashes to 0-2 per paragraph, none inside an English
   clause
4. Drop transition words that don't carry a logical relation
5. Vary sentence length: at least one short sentence (<15 words),
   at least one long sentence (>25 words but <35)
6. Preserve all factual content (Vaswani 2017, "Attention Is All You
   Need", machine translation + protein structure as examples)
7. Drop the throat-clearing closer entirely
8. End with a substantive sentence about the contribution, not a
   "paves the way" placeholder

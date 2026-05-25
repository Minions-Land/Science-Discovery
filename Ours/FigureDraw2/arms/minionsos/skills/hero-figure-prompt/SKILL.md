---
slug: hero-figure-prompt
summary: AI-generated hero / illustration figures (Figure 1, conceptual diagrams) use gpt-image-2.0; the generation prompt is persisted as a paper artifact; rendered figure uses Times New Roman for body text and LaTeX fonts for math; "AI taste" is minimised; multi-panel figures use Nature-style formalised panel structure with explicit panel anchors.
layer: logical
tools:
version: 1
status: active
references: figure-spec, academic-plotting, paper-quality-contract
provenance: human + MinionsOS-Paper Figure 1 / ResearchEVO Figure 1 / ZheMa-Proposal panel redo
---

# Skill — Hero Figure Prompt

For Figure 1 / conceptual hero illustrations / "what this paper does" diagrams — figures that are AI-generated rather than data plots or formal architecture specs. Different discipline from `figure-spec.md` (architecture diagrams) and `academic-plotting.md` (data plots).

## When to invoke

- Generating Figure 1 / hero / conceptual illustration.
- Re-generating an existing hero figure for a venue switch or rebuttal.
- Multi-panel "method overview" figure where the panels are illustrative, not data.

## The contract

### 1. Generator: `gpt-image-2.0`
The user's chosen image generator. Other generators are not interchangeable.

### 2. The generation prompt is a paper artifact
The prompt that produced the figure must be **persisted on disk** alongside the figure file. Path convention:
```
branches/writer/paper/figures/fig_01_hero.pdf       # rendered figure
branches/writer/paper/figures/fig_01_hero.prompt.md # the gpt-image-2.0 prompt
```

The prompt file includes: full prompt text, generator + version, date, the section / claim it supports. This makes the figure regenerable: rename the method, update the prompt, regenerate, re-cite.

User's exact phrasing: *"这个 prompt 需要落盘"* — non-negotiable.

### 3. Font discipline on rendered figures
- Body text in figure: **Times New Roman**.
- Math in figure: **LaTeX fonts** (Computer Modern via MathJax-style rendering or pre-rendered LaTeX snippets).
- Reject figures whose math is rendered in sans-serif or whose body text is in a stochastic AI-typical font.

### 4. "AI 味少一些" — minimise AI taste
Hero figures often look stochastically pretty in a way that signals "AI made this". Reduce it:
- Hand-laid-out feel; explicit panel structure (not a wash of gradients).
- Restrained palette (3–5 colours, not the full rainbow).
- No spurious icons / decorative elements that don't carry meaning.
- Each panel has a clear function — explanatory or comparative — not just decoration.
- One regeneration round explicitly asks: "less AI, more journal".

### 5. Nature-style panel structure for multi-panel hero
When the hero is multi-panel ("Method overview" with sub-panels A / B / C / D):
- Each panel is **formalised** — labelled (A), (B), (C), (D) in the upper-left.
- Panel A typically explains the system / method ("协作方式" / collaboration model).
- Subsequent panels show data / results / variants.
- Panel A is held to the same formalisation bar as the data panels — no hand-wave.
- When redoing, anchor on a reference figure type: the user's pattern is to point at a published figure ("看 Figure XV3 里面的图的类型") rather than freestyle.

## Procedure

1. **Decide hero scope.** Single panel (concept) vs multi-panel (method overview). For multi-panel, identify each panel's function before prompting.
2. **Draft a "world-class" prompt.** The user's instruction was: *"组织一个世界级超级无敌的能够 Go Viral 的 Prompt"*. Concretely: state the central claim, name each panel and what it shows, specify font discipline (Times + LaTeX), specify palette restraint, name the reference figure style ("Nature method-overview style").
3. **Persist the prompt.** Save to `figures/fig_NN_hero.prompt.md` immediately, before generation. The prompt file is committed to git the same time as the rendered figure.
4. **Generate** with gpt-image-2.0.
5. **Audit the output.** Font discipline + AI-taste reduction + panel formalisation + reference-figure anchor. If any axis fails, refine the prompt and regenerate.
6. **Iterate until the user is satisfied.** The user has indicated 3–5 rounds is normal; do not propose alternative generators or panel structures unless asked.
7. **Caption the figure** per `submission-cleanup-audit.md` category 4 — system size / parameters / source / panel-by-panel labels are required, not generic ("Method overview." is generic; "Method overview: (A) cooperation graph between roles, (B) ablation of memory layers, (C) wall-clock comparison on 5 benchmarks." is specific).

## Pitfalls

- Using a different generator without checking. The discipline is generator-specific; another generator's prompt syntax differs.
- Failing to persist the prompt. Without the prompt file, the figure is one-shot and cannot be regenerated for camera-ready or rebuttal.
- Sans-serif math in the rendered figure. Reject and regenerate.
- Decorative panels with no function. Each panel earns its space by carrying meaning.
- Free-style panel layout when a reference figure was named. If the user pointed at "Figure XV3", anchor on Figure XV3's panel structure, not a generic Nature template.
- Treating Panel A (concept / cooperation / method) as less rigorous than data panels. The user has called this out: Panel A is held to the same formalisation bar.

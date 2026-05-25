---
name: editorial-html
description: Produce a single-file, self-contained long-form HTML report in the "editorial field report" style — serif typography on warm paper, narrow measure, floating side TOC, ornamental section breaks. Use when the user asks for a survey, field report, essay, blog-style write-up, or "make it look like a magazine article" in HTML. Do NOT use for dashboards, landing pages, or app UI.
triggers:
  - "write an HTML report"
  - "turn this into a blog post / essay / long read"
  - "make it look like a magazine / field report"
  - "standalone HTML I can just open in a browser"
outputs: one .html file · inline CSS · inline JS · no build step · no external assets
---

# editorial-html

A design system for single-file long-form HTML. The reference implementation is
`/Users/mjm/Skill/research-report.html` — read it first if available, then follow the
spec below.

## When to use this

✅ Field reports, surveys, essays, introductions, deep dives, long blog posts
✅ Documents meant to be read end-to-end, not scanned
✅ Self-contained deliverables that may travel without their surrounding repo

❌ Dashboards, admin UIs, landing pages, product sites (use frontend-design instead)
❌ Slide decks or presentations
❌ Documents under ~600 words (use plain Markdown)

## Core invariants (never break these)

1. **Single file.** Inline CSS in `<style>`, inline JS in `<script>`. No external CSS,
   no external JS, no `<link rel="stylesheet">`, no CDN fonts. The file must open and
   render fully by double-clicking it, offline.
   *Exception:* KaTeX is allowed via CDN when the content genuinely requires display
   mathematics — see "Mathematical notation" below.
2. **Reading measure of 680px.** The main column is `max-width: 680px`. This gives
   roughly 65 characters per line — the width at which continuous prose is most
   comfortable. Do not widen it to 800 or 1000; that is a dashboard, not a read.
3. **Serif body + sans UI.** Body text is a book-style serif (Iowan Old Style primary,
   Cambria / Liberation Serif fallbacks, Songti SC for Chinese). Navigation, tables,
   code, and metadata use a sans stack. Code uses SF Mono.
4. **Warm paper background, not white.** Body is `#fbfaf6` (a faint cream). White
   (`#ffffff`) is reserved for card surfaces inside the cream. Pure white on a
   monitor is fatiguing for long reads.
5. **One accent color, used sparingly.** Rust/terracotta (`#9c3b16`) for accents,
   its ink variant (`#6e2a0f`) for hover. Never use blue for links — blue on cream
   looks web-2.0.
6. **Numbered roman sections, not chapters.** `I` · `II` · `III` … styled as a
   small-caps mono label above each `<h2>`. This signals "long-form" immediately.

## Reference structure

```
<!doctype html>
<html lang="...">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>...</title>
  <style>...</style>
</head>
<body>
  <div id="progress"></div>          <!-- top reading-progress bar -->
  <nav id="toc">...</nav>            <!-- fixed left side, floats over body -->
  <article>
    <header class="hero">...</header>
    <section id="..."><h2>...</h2>...</section>
    <p class="sep-ornament">❧</p>    <!-- between every two sections -->
    <section>...</section>
    ...
  </article>
  <footer class="colophon">...</footer>
  <script>...</script>
</body>
</html>
```

## Color palette (CSS variables to copy verbatim)

```css
:root{
  --bg:#fbfaf6; --ink:#1a1a1a; --dim:#5a6068; --faint:#8a9099;
  --accent:#9c3b16; --accent-ink:#6e2a0f; --accent-bg:#faeee3;
  --rule:#e7e2d6; --card:#ffffff;
  --code-bg:#f1ecde; --hi:#fff4cf;
  --shadow:0 1px 2px rgba(0,0,0,.03),0 6px 20px rgba(20,10,0,.04);
}
```

Contrast rule: body text is `--ink` on `--bg` (≈16:1); faded meta is `--dim`
(≈7:1); the only color that moves into the foreground is `--accent` on links
and roman numerals.

## Typography stack

```css
--serif:"Iowan Old Style","Cambria","Liberation Serif","Songti SC","Source Han Serif SC",Georgia,serif;
--sans:-apple-system,BlinkMacSystemFont,"SF Pro Text","Inter","PingFang SC","Noto Sans CJK SC",sans-serif;
--mono:"SF Mono",ui-monospace,Menlo,Consolas,monospace;
```

Sizes:
- Body: `17px/1.72` serif
- `<h1>` (article title): `46px/1.1`, serif, 700, letter-spacing `-.02em`
- `<h2>` (section): `30px/1.2`, serif, 700, letter-spacing `-.015em`
- `<h3>` (sub-section): `21px/1.25`, serif, 700
- `<h4>` (label): `14px` sans, 600, all-caps, letter-spacing `.02em`, `--dim` color
- Stand-first (lede after h1): `20px/1.55` serif italic, `#2f343a`
- Deck (after each h2): `16px/1.5` italic, `--dim`
- Byline / meta: `13px` sans, `--dim`

## Mathematical notation

`<code>` does not render math. Inside a `<code>` span, every character is literal —
`<code>x_1</code>` shows `x_1`, not x₁. If you need math, use one of the three
tiers below, matched to what the content actually calls for.

**Tier 1 · native HTML (default, zero dependencies).** Enough for 90% of editorial
prose. Use `<sub>` and `<sup>` for sub/superscripts; type Greek letters and math
symbols as Unicode directly.

```html
<p>The loss <em>L</em><sub>total</sub> = <em>L</em><sub>recon</sub> + λ · <em>L</em><sub>KL</sub>,
where λ ∈ [0, 1] and ∂<em>L</em>/∂θ is estimated by mini-batch gradient descent.</p>
```

Quick reference for the characters you will reach for:

- Greek: α β γ δ ε ζ η θ ι κ λ μ ν ξ π ρ σ τ υ φ χ ψ ω · Α Β Γ Δ Θ Λ Π Σ Φ Ψ Ω
- Operators: ± × ÷ · ∘ ∗ ⊕ ⊗ ⊙ ∧ ∨ ¬ ∀ ∃
- Relations: ≈ ≠ ≤ ≥ ≡ ∼ ∝ ∈ ∉ ⊂ ⊆ ⊃ ⊇
- Calculus / sets: ∞ ∑ ∏ ∫ ∬ ∮ ∂ ∇ √ ∛ ∆
- Arrows: → ← ↔ ⇒ ⇐ ⇔ ↦ ↑ ↓
- Brackets: ⟨ ⟩ ⌊ ⌋ ⌈ ⌉ ‖ · never-break spaces: `&thinsp;` `&nbsp;`

Italicize variables with `<em>` so they match the math convention. Do **not** use
`<code>` for variables — monospace breaks the typographic register of the prose.

**Tier 2 · inline KaTeX via CDN (for display equations).** When the piece genuinely
needs fractions, matrices, cases, integrals with limits, or aligned equations, bring
in KaTeX. This is the *only* permitted breach of the single-file rule.

Add to `<head>`:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" crossorigin="anonymous"
  onload="renderMathInElement(document.body, {delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}], throwOnError:false});"></script>
```

Then write math with TeX delimiters in the body:

```html
<p>The attention kernel is $\mathrm{softmax}(QK^{\top}/\sqrt{d_k})V$, whose
complexity in sequence length $n$ is $\mathcal{O}(n^2)$.</p>

<p>Display form:</p>
$$
\mathcal{L}(\theta) = \mathbb{E}_{x\sim p_{\mathrm{data}}}\!\left[-\log p_\theta(x)\right]
$$
```

Style note: KaTeX ships its own fonts, so math blocks will *not* use Iowan Old
Style. That is correct — display math wants a math-optimised face (KaTeX's is
based on Computer Modern). Leave it alone.

**Tier 3 · images / MathML fallback.** For a single decorative formula where
you want zero JS, either ship the equation as a pre-rendered SVG/PNG, or use
MathML directly (`<math><mfrac>…</mfrac></math>`). Both are high-effort and
rarely worth it — reach for Tier 2 instead.

## The signature details

Seven small things make the difference between "a web page" and "a magazine article".
Include them all unless the user explicitly rejects one.

**1. Drop cap on the first section.** CSS `::first-letter` floated left, serif, ~62px, accent color. One paragraph only, and only in section I. `<p class="drop">...</p>`.

**2. Roman numeral section label.** A small mono label above each section title, in `--faint` gray with 0.12em letter spacing:
```html
<h2><span class="roman">I</span>A hinge point</h2>
```

**3. Italic "deck" after each h2.** One sentence, setting up what the section does:
```html
<p class="deck">Two years that changed what "using AI to do research" means.</p>
```

**4. Ornamental separator between sections.** A single character on its own line — `❧` is the canonical choice; `§` or `❦` also work. Wrap in `<p class="sep-ornament">❧</p>`, centered, with 1em letter-spacing and 56px vertical margin.

**5. Pull quote with em-dash cite.** A full-width blockquote with a 3px accent-colored left border, italic serif body, and a sans-serif cite line prefixed with "— ":
```html
<blockquote>
  A skill is the smallest unit of research expertise that can travel without its author.
  <cite>a characterization we have found useful</cite>
</blockquote>
```

**6. Stat band.** Five-column inline strip with top-and-bottom rules, serif numerals in accent-ink, all-caps sans labels. Use to dramatize 3–5 numbers. No more than once per section, usually in I or V.

**7. Colophon footer.** Set apart by a top rule. Tells the reader what typeface was used, when numbers were current, and how to verify them. Short — three sentences.

## Layout recipes

**Hero (article header)**
```html
<header class="hero">
  <p class="eyebrow">A field report · May 2026</p>
  <h1>Article title goes here</h1>
  <p class="standfirst">
    One-to-three-sentence stand-first. Italic. This is the sentence that
    decides whether the reader continues.
  </p>
  <div class="byline">
    <span>By <b>the editors</b></span>
    <span class="sep">·</span>
    <span>Reading time <b>~14 min</b></span>
    <span class="sep">·</span>
    <span><b>2026-05-12</b></span>
  </div>
</header>
```
Hero has a bottom border and 40px padding-bottom; after it, `margin-bottom:72px`.

**Side TOC (floats over body, hides below 1120px)**
```html
<nav id="toc">
  <p class="cap">Contents</p>
  <ol>
    <li><a href="#prologue"><span class="num">I</span>A hinge point</a></li>
    ...
  </ol>
</nav>
```
Positioned `fixed; top:110px; left:24px; width:220px`. Items have a 1px left rule; the active item gets a 2px accent-colored left border. Hidden on narrow viewports — long-form reads better without distraction on mobile.

**Section skeleton**
```html
<section id="slug">
  <h2><span class="roman">III</span>Title</h2>
  <p class="deck">One-sentence deck.</p>
  <p>First body paragraph...</p>
  <h3>Optional sub-section</h3>
  <p>...</p>
  <div class="aside">
    <span class="k">Side note</span>
    Short aside, one or two sentences max.
  </div>
</section>

<p class="sep-ornament">❧</p>
```

**Tables inside editorials**
Tables are allowed but must be sans-serif, thin-ruled, `background:var(--card)` so they float visibly off the cream body. `thead th` is small-caps sans, 12px. Numeric columns use `td.num` (right-aligned, tabular-nums). Hover row gets a very slight `#fbf8ef` tint.

**ASCII / code diagrams**
Use `<figure class="diagram">` with a dark background (`#23272c`) and light mono text. Always include a `<figcaption>` in italic sans below a thin internal rule. This is the one place where darkness is allowed.

**Aside callouts**
Two variants: `.aside` (accent left-border, default) and `.aside.note` (purple `#6b4ca7` left-border, for asides that introduce caveats rather than emphasis). A `<span class="k">label</span>` acts as the aside's title.

## The JavaScript

Exactly two responsibilities; keep it minimal.

**1. Reading progress bar.** A 2px bar fixed to the top; it fills from 0 to 100% proportional to scroll. Implemented via a CSS custom property set by a scroll listener:

```js
const bar = document.getElementById('progress');
const update = () => {
  const h = document.documentElement;
  const pct = h.scrollHeight - h.clientHeight > 0
    ? (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100
    : 0;
  bar.style.setProperty('--p', pct + '%');
};
window.addEventListener('scroll', update, { passive: true });
update();
```

**2. Active TOC highlight.** `IntersectionObserver` with `rootMargin: '-25% 0px -65% 0px'` so the active section flips when it crosses roughly the upper third of the viewport:

```js
const links = document.querySelectorAll('#toc a[href^="#"]');
const sections = Array.from(links).map(a => document.getElementById(a.getAttribute('href').slice(1))).filter(Boolean);
const io = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id));
    }
  });
}, { rootMargin: '-25% 0px -65% 0px' });
sections.forEach(s => io.observe(s));
```

Do not add smooth-scroll polyfills, parallax, reveal-on-scroll animations, cookie banners, analytics, or a dark-mode toggle. None of them help the reader; all of them dilute the form.

## Writing voice (how the content should sound)

The style of prose to aim for is *The Atlantic* / *LRB* / *Stripe Press* long-read — not Medium, not corporate blog, not academic abstract.

**Do**
- Open with a concrete moment or date, not an abstract claim.
- Use em-dashes for mid-sentence asides.
- Name things in full the first time, then shorten.
- Include one or two "honest limitations" per major claim — the piece is more persuasive for admitting them.
- Let sentences vary in length. A short one. Then a longer, more involved one that earns its length by actually doing work.

**Don't**
- Avoid "As we'll see…", "In this post we will…", "Let's dive in". The standfirst already told the reader what is coming.
- No bullet lists where prose would do. Bullets are for table-like content (a benchmark catalog, a skill list), not for ideas.
- No emojis in prose. The only glyphs in body text are `❧`, `·`, and occasional em-dashes.
- No first-person plural unless the piece is genuinely co-authored or editorial. "I think" / "we believe" weakens an essay; let the argument do the work.

## Anti-patterns (what breaks the style)

These are failure modes observed in drafts; reject them on review.

| Anti-pattern | Why it breaks the form | Fix |
|---|---|---|
| Column widens to 900–1100px | Lines become unreadable at >75ch; the page starts to feel like a dashboard | Hold `--measure:680px` |
| Body set in sans-serif | The entire "book-like" cue collapses | Serif body is non-negotiable |
| Pure white background `#fff` | Clinical; fatiguing over 10+ minutes | Cream `#fbfaf6`; reserve white for cards |
| Blue underlined links | Reads as a Wikipedia article | Accent rust, underline is a 1px baseline gradient |
| Drop shadows on every element | Looks like a SaaS dashboard | Only tables and asides get the subtle shared `--shadow` |
| Bullet lists where prose would do | The text stops arguing and starts presenting | Rewrite as sentences; reserve bullets for lists of things, not ideas |
| Headings in all-caps except h4 | H4 is a label, h2/h3 are titles. All-caps titles look like press releases | Keep casing natural; reserve uppercase for labels |
| Section breaks with `<hr>` | Too mechanical | Use the ornament paragraph |
| Emoji section icons (🧠 📊 🔬) | Breaks the print feel instantly | Roman numerals only |
| `<code>x_1</code>` for math | `_` is a literal character inside `<code>`; it renders as an underscore, not a subscript | Use `<em>x</em><sub>1</sub>`, or bring in KaTeX — see "Mathematical notation" |

## Workflow: how to actually produce one

When a user asks for a report / essay / blog in this style:

1. **Outline first.** Draft 5–8 section titles and a one-line deck for each. Show the user. Iterate before writing body prose.
2. **Write body without styling.** Get the text right in plain prose. Keep each section to 250–500 words unless the content genuinely demands more.
3. **Assemble the HTML skeleton.** Copy the structure in the "Reference structure" section above. Fill in hero, nav, and the 5–8 `<section>` blocks with placeholder text.
4. **Paste the CSS block verbatim.** Do not hand-roll colors or font sizes from memory — the palette and scale are the skill.
5. **Apply signature details in order.** Drop cap on §I → roman numerals on every h2 → deck under every h2 → `❧` between every pair → at least one pull quote → at least one stat band → colophon footer.
6. **Tables and asides second pass.** Add them only where they genuinely help. A report can be excellent with zero tables.
7. **Validate.** Run a quick structural check — every `<section>` closes, heroes and footers are outside `<article>`, `<nav>` and `<article>` are siblings in `<body>`. Confirm the file opens from `file://` with no console errors and no 404s.
8. **Ship the diff.** The output is one `.html` file. Do not produce separate CSS or JS files "for cleanliness" — the point is portability.

## Output procedure (mandatory) — DO NOT Write the full file in one tool call

A finished editorial-html file is 30–80 KB of HTML containing inline `<style>`, prose with curly quotes / em-dashes / occasional CJK, and (often) KaTeX TeX strings. This content shape is exactly the Opus 4.7 empty-input failure trigger documented in the `reliable-file-io` skill (Tier 0). A single `Write` of the whole HTML or a single Bash heredoc carrying it will silently come through with `input: {}` and the harness will reject it.

**Always use the `reliable-file-io` Tier 0 seed-and-Edit recipe:**

1. **Seed** with one short `Write` (≤ ~50 lines):
   ```html
   <!doctype html>
   <html lang="en"><head><meta charset="utf-8"/><title>...</title>
   <style>/* CSS_BLOCK_HERE */</style>
   </head><body>
   <div id="progress"></div>
   <nav id="toc"></nav>
   <article>
     <header class="hero"></header>
     <!-- SECTIONS_HERE -->
   </article>
   <footer class="colophon"></footer>
   <script>/* JS_HERE */</script>
   </body></html>
   ```
2. **Replace `/* CSS_BLOCK_HERE */`** via one Edit (the canonical CSS block is small enough to fit in one Edit's `new_string`; if not, split CSS into 2 Edits at a `/* --- */` divider).
3. **Replace `<!-- SECTIONS_HERE -->`** by inserting **one section per Edit** (each ≤ ~50 lines). For long sections, split content but keep `<section>` tags balanced inside one Edit.
4. **Replace `<!-- JS_HERE -->`** with the progress-bar / TOC-highlight JS via one Edit.
5. **Validate** by `Read`ing the final file and confirming `<section>` count matches the outline.

Do NOT skip step 0 of `reliable-file-io` and try to `Write` the entire file — even an 8 KB editorial-html file has reliably triggered the empty-input bug because of the curly-quote / em-dash / CJK mix.

## Reference file

`/Users/mjm/Skill/research-report.html` is the canonical implementation. When uncertain about spacing, colors, or prose cadence, open that file and match it.


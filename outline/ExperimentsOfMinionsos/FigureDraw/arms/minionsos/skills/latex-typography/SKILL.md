---
slug: latex-typography
summary: LaTeX formatting conventions — all recurring named entities use preamble \newcommand macros and must not be hardcoded in the body; avoid itemize, short heads, and gratuitous emphasis.
layer: logical
tools:
version: 3
status: active
supersedes:
references: make-latex-model, paper-compile
provenance: R7-evolved
---

# Skill — LaTeX Typography

Typographic consistency signals professionalism. These conventions ensure the manuscript uses LaTeX's formatting capabilities deliberately rather than ad hoc, and avoids the structural anti-patterns that venue editors and reviewers associate with rushed submissions.

## When to invoke

- Polishing LaTeX formatting.
- Checking typographic convention compliance.

## Macro discipline

Define every recurring named entity once in the LaTeX preamble using `\newcommand`.
This includes the model/system/method name, each named pillar/component/methodology,
each recurring symbol or notation, each recurring acronym whose expansion deserves
consistent treatment, and any recurring brand or font treatment. Use the macro
throughout the manuscript from that point on. The body must not contain a hard-coded
occurrence of any name that has a macro, even once.

Before drafting:

1. List every named entity that recurs more than once: the system name, each
   pillar/contribution/method name, each recurring symbol, and each recurring acronym
   whose expansion deserves consistent treatment.
2. Define a `\newcommand` for each at the top of the preamble, or in a dedicated
   `\macros{}` block immediately after the `\usepackage` lines.
3. Group the definitions by category in the preamble: system name, pillar names,
   notation/symbol macros, then brand/font macros.
4. Use `\textsc{...}` for the system name, `\textbf{...}` for first-mention
   emphasis, and plain text for pillar names. Append `\xspace` to macros that are
   followed by space-separated text so trailing spaces are preserved.
5. Refer to every recurring entity only by its macro from that point on.

For a recurring system or method name:

```latex
\newcommand{\methodname}{\textsc{RetroDiff}\xspace}
```

This ensures renaming requires a single edit and font treatment remains consistent throughout. Use `\textsc{}` for model names; do not use `\texttt{}` (monospace is a code font, not a model-name font).

Wrong hard-coded recurrence:

```latex
We propose RetroDiff. RetroDiff combines retrieval and diffusion. RetroDiff is fast.
```

Right macro-driven recurrence:

```latex
% Preamble
\newcommand{\methodname}{\textsc{RetroDiff}\xspace}

% Body
We propose \methodname. \methodname combines retrieval and diffusion. \methodname is fast.
```

For multi-pillar systems, define one macro per pillar so renaming a pillar is a
one-line edit:

```latex
\newcommand{\pillarA}{\textbf{Postured Dispatch}\xspace}
\newcommand{\pillarB}{\textbf{Tri-Layer Memory}\xspace}
```

The user treats *method naming as a correctness contract* — a name that doesn't bind a method to an object (e.g. bare "Memory" or "Skill") is a renaming opportunity, and renaming may happen multiple times during writing as scope clarifies. The `\newcommand` discipline makes each rename a one-line edit. After a rename of a `\modelname` / pillar / component, run a propagation sweep:

1. The `\newcommand` definition.
2. Every Abstract mention.
3. Every Introduction contribution bullet.
4. Every Discussion mention.
5. Every capability / comparison table.
6. Every figure caption that names it.
7. External mentions outside the .tex (talk titles, README, repo name, GitHub URL, arXiv title) — `\newcommand` does not reach these; sweep manually.

If `\newcommand` discipline was followed, the body is updated by the definition change alone. The propagation sweep is for the surfaces the macro can't reach.

Avoid these macro-specific pitfalls:

- Defining a macro and then sometimes typing the literal name, which defeats the
  purpose.
- Forgetting `\xspace` so `\methodname is fast.` renders as `RetroDiffis fast.`.
- Defining macros inline at first use instead of collecting them in the preamble.
- Using inconsistent fonts for the same name, such as some `\textsc{}`, some
  `\texttt{}`, and some bold, instead of letting the macro carry the formatting.
- Treating one-time names as recurring; single-use names do not need a macro.

## Structural formatting

**No itemize outside Introduction contributions.** The only permitted `\begin{itemize}` in the paper is the contribution bullet list at the end of the Introduction. All other enumerations must be rewritten as prose.

**No `\paragraph{}` short heads.** Do not use `\paragraph{Step 1.}` style formatting. When subheadings are needed, use `\noindent\textbf{...}` or `\subsection{}`. A `\paragraph{}` followed by only one line of content indicates a structural problem that formatting cannot solve.

## Inline formatting

**Bold** is reserved for the first definition of a term. Do not scatter `\textbf{}` throughout the text for emphasis — sentence structure and position should carry emphasis, not formatting.

**Italic** is reserved for mathematical variables and foreign-language terms only.

## Comparison-table style recipe

Capability and benchmark comparison tables follow this recipe:

```latex
\newcommand{\best}[1]{\textbf{\textcolor{red}{#1}}}
\newcommand{\second}[1]{\underline{\textcolor{blue}{#1}}}

\begin{tabular}{c|cccc}
\diagbox{Method}{Property} & \textbf{P1} & \textbf{P2} & \textbf{P3} & \textbf{P4} \\
\hline
Baseline-A    & 0.42 & 0.31 & \best{0.71} & 0.29 \\
\rowcolor{gray!10} Baseline-B & 0.51 & \second{0.45} & 0.62 & 0.34 \\
\rowcolor{pink!20} \textbf{Ours} & \best{0.68} & \best{0.52} & 0.69 & \best{0.41} \\
\end{tabular}
```

Where:
- `\diagbox{}{}` for the corner cell (split label).
- `\rowcolor{gray!10}` for alternating bands.
- `\rowcolor{pink!20}` for the "Ours" row.
- Best result: bold red via `\best{}`. Second-best: underlined blue via `\second{}`.

Iterate the rendered output 3–5 times to converge on the user's mental model of the table; do not propose alternative styles unless asked.

## No checkmark / half-checkmark capability tables

`✓` / `½` / `✗` capability tables are visually noisy and rarely orthogonal. Replace with **per-feature explicit content** — feature value or scope, not an opinion glyph.

Wrong:
| Method      | Multi-agent | Async | Verification |
|-------------|-------------|-------|--------------|
| Baseline-A  | ✓           | ½     | ✗            |
| Ours        | ✓           | ✓     | ½            |

Right:
| Method      | Agent count | Concurrency       | Verification     |
|-------------|-------------|-------------------|------------------|
| Baseline-A  | 4 fixed     | sync rounds       | none             |
| Ours        | dynamic     | event-driven      | code review only |

The right form makes orthogonality visible. The wrong form invites reviewers to ask "what does ½ mean exactly".

## Pitfalls

- Named entity appearing in inconsistent formats across the text (some bold, some monospace, some small-caps).
- Defining a macro and then typing the literal name anywhere in the body; once a macro exists, hard-coded recurrences are forbidden.
- Forgetting `\xspace` so `\methodname is fast.` renders as `RetroDiffis fast.`.
- Defining macros inline at first use instead of collecting them in the preamble.
- Treating one-time names as recurring; single-use names do not need a macro.
- `\paragraph{}` followed by only one line of content (indicates a structural problem).
- Excessive bold for emphasis (sentence structure and position should carry emphasis, not formatting).

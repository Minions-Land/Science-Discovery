---
slug: pdf-vector-layout
summary: Surgical edits on already-compiled PDFs (move regions, extract+merge panels, hide source-side labels, push toward Nature/Cell typography) — content-stream edit via pikepdf so visual, text layer, and file size all stay consistent. The fix for cropbox-stamp pipelines that silently triplicate the text layer.
layer: logical
tools: pikepdf, pillow, poppler (pdftocairo, pdftotext)
version: 1
status: active
references: academic-plotting, figure-layout-defaults, figure-aesthetic-exemplars, package-pdf-compile, paper-compile, submission-cleanup-audit
provenance: human + Codex 湿实验/v8/v16 sessions + verified by external Layout regression run
---

# Skill — PDF Vector Layout

This skill is the playbook for **rearranging and polishing already-compiled PDF content with vector + text-layer fidelity**, with the additional ambition of pushing the result toward Nature/Science/Cell sub-journal typography. It complements the other figure skills:

- [[academic-plotting]] / [[figure-layout-defaults]] / [[figure-aesthetic-exemplars]] make figures *correct and beautiful at generation time* (matplotlib rcParams, gridspec, exemplar diff).
- [[paper-compile]] / [[package-pdf-compile]] produce the final manuscript PDF.
- **This skill** does the surgery between those two: when a generated panel needs re-positioning inside a composite, when two source PDFs must vector-merge, when a source's panel letters conflict with a composite's labels, when the title-to-figure gap needs tightening — without rasterising or breaking the text layer.

The whole skill is one rule applied with discipline: **never rasterize what the user asked you to keep editable, AND never let the text layer disagree with what the eye sees.** Everything below — coordinate handling, panel labels, font choices, "Nature-feel" tuning — is downstream of that.

## When to invoke

Invoke when ANY of these holds:
1. You have one or more existing PDFs (compiled figure outputs, sub-panels, prior versions) and need content moved, cropped, merged, replaced, or repositioned.
2. The result must remain a real PDF — opens in Illustrator/Inkscape, text is selectable AND identical to the source's text layer, paths are paths.
3. The figure should look like it belongs in a Nature/Science/Cell-family paper: clean panel letters, consistent typography, tight margins, correct point sizes, no leftover defaults from `matplotlib`.
4. You're fighting in-figure annotations: "the letter g is clipped", "hide the original e/f/g/h/i, keep my new f/g/h/i/j", "再紧凑一点", "把这个字母换成 Helvetica 7 pt 加粗".
5. A figure already passed [[academic-plotting]] / [[figure-layout-defaults]] but a downstream layout decision (combining two figures, re-doing one row, fitting a new panel into an old composite) needs surgery.

Do NOT invoke for:
- Plain text extraction from a PDF (use pdfplumber / PyMuPDF in a one-off).
- Generating a PDF from scratch — that's [[academic-plotting]] / matplotlib / reportlab.
- Pure raster image work.
- LaTeX-source-level changes — those go in the `.tex` and re-compile via [[paper-compile]].

Phrases that should trigger this skill: "移到页面下方", "拼到一起", "保持矢量 / 可编辑", "替换进去", "微调位置", "再紧凑一点", "g 被裁断了", "svg 和 png 我都要", "模仿 Nature 排版", "字号 / 字体 / 加粗", "改图里的字母位置".

## The decision tree (read this before touching code)

```
Need to keep vectors AND a clean text layer (search/copy/screen-readers correct)?
       │
      Yes (the usual case)
       │
       └──> pikepdf content-stream edit
            (parse → segment by atomic unit → classify by y-bbox → wrap in-region
             units with `q 1 0 0 1 0 SHIFT_Y cm ... Q` → unparse).
            scripts/move_pdf_region.py and scripts/merge_pdf_pages.py both use this.

Visual-only is OK, text layer can be wrong?  ── pypdf merge_translated_page is fine,
                                                 but you almost never want this.

Need to change a font / restyle the figure overall?
   regenerate from the source script (matplotlib / svg → cairosvg → PDF) with the new
   style, then re-merge using the rules above. Do NOT try to font-substitute inside an
   existing PDF unless you have the original embedded font subset; that path is brittle.
```

**Why content-stream edit is the default, not pypdf.** The intuitive shortcut —
clone the source page with a narrow cropbox/mediabox and stamp it three times
(above region, shifted region, below region) using `pypdf.PageObject.merge_transformed_page`
— produces a render that looks correct but a text layer that is broken. PDF cropboxes
clip the *renderer's* viewport, not the content stream. So `pdftotext`, copy/paste,
search, and accessibility readers see THREE copies of the full page even though the
pixels look right. Investigate that mode is what `verify_vector.py --source <orig>`
catches: any token appearing more in the output than in the source is the smoking
gun. Always do the work in the content stream.

The pikepdf path is also dramatically smaller — for the synthetic 5-panel test, the
content-stream edit produced 1.6 KB; the cropbox-stamp pipeline produced 5.3 KB
(same content embedded ~3×).

## What NOT to do (these are real, recurring failures)

- Do **not** clone the source page with a narrowed cropbox/mediabox and stamp it
  three times — even though pypdf will happily run that pattern, only the *render*
  is clipped; the text layer (and the file size) carries 3× the original content.
  Use the content-stream pipeline in `move_pdf_region.py` / `merge_pdf_pages.py`.
- Do **not** render the source PDF to PNG and re-embed it. The output will look right but be a flat image; the user will say "这是截图，不是矢量". Both sessions started here and had to backtrack.
- Do **not** use `pdftoppm` / `pdftocairo` as part of the pipeline. They are **preview-only** tools — render the final PDF to inspect it, never feed their output back in.
- Do **not** edit empty backup files in place. If `*_base.pdf` or `*_v16_base_raster.pdf` is 0-content or blank, look around the directory for siblings (`figureX_v15.pdf`, `make_figure.py`, an `.svg`) — those are the real source of truth.
- Do **not** trust that a script "ran" because it exited 0. Check `os.path.getmtime` of the output and re-render the first page. The session lost time to a script that silently produced nothing because of a path mistake.
- Do **not** silently overwrite the user's PDFs. Write to a new filename or to `tmp/`, and copy backups to `backups/<name>.<timestamp>.bak` before any in-place change.
- Do **not** assume a Form XObject's bounding box starts at `(0, 0)`. Read its real `BBox` first; the v16 session burned a cycle because `row_view.BBox` had a bottom edge of `485.74 pt`, not `0`, so the placement was correct in math and wrong in pixels until the offset was subtracted.
- Do **not** leave two competing label sets visible. If you paste a row from a source PDF that has its own `e/f/g/h/i` letters, and the composite already labels them `f/g/h/i/j`, you must hide one set. Do it with a **vector white-fill rectangle** placed under the composite's labels, not by rendering to image.
- Do **not** change panel letter sequences without confirming. `e/f/g/h/i` vs `f/g/h/i/j` is meaningful — it tells the reader which panels are new.

## The standard workflow

1. **Inventory.** List the directory. Identify: live source(s), the target/output name, any siblings that hint at the original layout (`make_figure.py`, `*_v15.*`, `*.svg`). Flag empty files (`getsize == 0` or blank pages).

2. **Find the layout source of truth.** If the user's request is "fix v16 back to its original layout", the original layout almost certainly lives in code (`make_figure.py`) or an earlier good version (`v15.pdf`, `figureX.svg`), not in the broken `v16.pdf`. Reconstruct *layout* from there.

3. **Pick the library** using the decision tree above. Default to `pypdf`.

4. **Plan coordinates on paper first.** Write down the target bounding box for each fragment in PDF points (1 pt = 1/72 inch). Account for:
   - PDF y-axis points up, origin at bottom-left.
   - "Move to the lower half" means the fragment's *top* sits near the page midpoint, then translate down by (target_top − current_top).
   - Reserve ~6–10 pt padding under titles. The session ended with the user asking for tighter spacing — default to ~8 pt and offer to tighten.
   - Form XObject BBoxes are not always at origin; read `bbox = float(form.BBox[1])` and subtract.

5. **Compose.** Apply translation/clip/mask via the chosen library. Save with a new name.

6. **Verify, don't trust.** Render page 1 with `pdftocairo -png -r 150 out.pdf preview` (or `pdftoppm`) and look at it. Confirm:
   - Nothing is clipped (the "g 被切了一块" failure mode — leave a 4–6 pt safety margin above the highest data point).
   - Text is still selectable (`pdftotext out.pdf -` returns the original strings).
   - Only one set of panel letters is visible.
   - File size is plausible (a vector page is usually 50 KB–2 MB; a 50 MB output means you accidentally embedded a raster).

7. **Deliver what was asked for.** If the user said "svg 和 png 我都要", export both alongside the PDF — `pdftocairo -svg` for SVG, `-png` for PNG. The PDF is the source of truth; the others are derived.

## Coordinate microadjustment cheatsheet

These came up across the v16 / wet-source / v8 sessions:

- **Title-figure gap too loose:** subtract 4–8 pt from the figure row's top y. Re-render to confirm.
- **Bottom edge clipped (e.g. letter "g"):** increase the destination clip box's height by 4–6 pt, and shift the fragment up by the same amount. When in doubt, set the clip's top y at a conservative `y ≈ 400 pt` rather than the data-tight value — it's cheaper to leave whitespace than to lose data.
- **Two panels need equal heights but sources differ:** scale the smaller one with `add_transformation(Transformation().scale(s).translate(dx, dy))`. Do not crop the larger one unless the user agreed.
- **"再紧凑一点":** treat as a 6–10 pt reduction in vertical spacing, then ask for confirmation rather than guessing more.
- **Form BBox not at origin:** subtract `BBox[1]` from your y-translation. Symptom: the placed content vanishes off-canvas.
- **Hide source-PDF panel letters that conflict with composite labels:** draw a tight white-fill rectangle (vector) over each letter's bounding region in the final PDF. Do this **inside the composite step**, not as a post-process on a flattened page. Constrain the mask y-range so it does not bleed into the composite's own labels (e.g. mask only `y ≥ 424 pt`).

## Nature/Science/Cell house-style cheatsheet

The user phrased it as "模仿 nature 子刊去排版". This is concrete — these journals share a fairly tight visual contract. When you're polishing toward that look, check:

- **Page geometry.** Single column ≈ 88 mm (≈ 250 pt). Double column ≈ 180 mm (≈ 510 pt). Most multi-panel figures are double column, ≤ 240 mm tall.
- **Panel letters.** Lowercase **bold sans-serif**, typically Helvetica/Arial 8–9 pt. Placed at the top-left of each panel, x-offset ≈ −6 pt and y-offset ≈ +4 pt from the panel's data area (i.e. just outside the axes). Never inside the plot. Keep them on a uniform baseline across the figure.
- **Axis labels & tick labels.** 7 pt sans-serif, regular weight. Tick labels can drop to 6 pt for dense axes but never below. Avoid italic axis labels (math symbols excepted).
- **Legends & annotations.** 6–7 pt. Legends inside the data region, no frame, no background fill, sit in the least-busy corner.
- **Caption/title rows in composite figures.** If the figure includes its own internal section titles (a thin row above each block), use 7–8 pt, semibold. Leave 6–8 pt below the title before the panels start.
- **Line widths.** Axes 0.5 pt. Plot lines 0.75–1.0 pt. Error bars 0.5 pt with caps 1.5 pt wide. These are journal norms, not matplotlib defaults — matplotlib's default 1.5 pt axes look amateurish at journal scale.
- **Color.** Limit to 4–6 hues across a figure. Prefer Okabe-Ito or ColorBrewer "Set2"/"Dark2" over `tab10`. Keep saturation moderate; reserve high-saturation red only for emphasis. Always include a color-blind safe check.
- **Font family.** Helvetica is the de facto standard. Arial is acceptable. **Avoid** matplotlib's default DejaVu Sans — readers can identify it on sight and it screams "draft".
- **Math.** Use the journal's preferred italic for variables (`Times Italic` or `STIX`), not matplotlib's mathtext default unless explicitly asked.
- **Export.** PDF must be vector with embedded fonts (`pdf.fonttype = 42` in matplotlib so text stays as text, not as paths). For SVG, use `cairosvg` or matplotlib's `savefig('foo.svg')`; never use `text-as-path` unless required, because it kills editability.

When the user says "make this look like Nature", do not apply all of the above silently. Apply the **typography pass first** (panel letters → axis labels → ticks → legend) and re-render; show the user; then iterate on color and spacing. That order matches how a real production editor works through a figure.

## Editing in-figure text and labels

This is the trickiest area, and where most agents fail by reaching for OCR or by re-rendering as raster. The right ordering is:

1. **Prefer regenerating from the source.** If `make_figure.py` or a matplotlib/seaborn/plotly script exists, change the label/font/position in the script and re-run. This is always the cleanest path.
2. **If no source, edit at PDF text-object level.** Use `pikepdf` or `pdfrw` to walk the page's content stream and find `Tj`/`TJ` operators. Replace the operand text. Adjust the preceding `Tf` (font selector) only if you also embed the new font. Adjust the `Tm`/`Td` position to nudge the label.
3. **If the label is a path (text was outlined),** you cannot replace it as text. Either re-source the figure or **mask + overlay**: draw a vector white rectangle over the old label, then draw the new label as live text on top.
4. **Repositioning a label:** find the `Tm`/`Td` for that text run, change its `tx, ty`. A 2–3 pt move is usually enough to clear an axis or another label.
5. **Restyling a label (bold / size):** if the font is already embedded in the PDF (it usually is in a journal-quality PDF), reuse the existing `Tf` resource for the new text. Don't introduce a new font reference unless you also embed the file — the result will fall back to a system font and look different on every viewer.
6. **Verify by `pdftotext` and visual diff.** After editing, the new label string must appear in `pdftotext` output (proves it's text, not a path), and a `pdftocairo -png` diff should show the change you intended and nothing else.

## The `make_figure.py` pattern

When the user has a multi-panel composite that has gone through versions (`v6 → v15 → v16`), there is almost always a generator script (`make_figure.py` or similar) sitting next to the PDFs. Read it first. The layout constants in that script are the canonical source. Edit the script, regenerate, then patch only the small placement detail the user asked about. Do not rebuild the whole composite from images.

## Scripts in this skill

The scripts and reference docs live in the sibling directory `pdf-vector-layout/`
(i.e. `minions/roles/writer/skills/pdf-vector-layout/scripts/*.py` and
`pdf-vector-layout/references/*.md`). Treat this top-level file as the
orchestrator that's always loaded at wake-up; the scripts and reference notes
are progressive disclosure — open them only when you decide to use this skill.

- `scripts/move_pdf_region.py` — translate a y-region of a single page to a new
  location, preserving vectors AND the text layer. Uses pikepdf to parse the
  content stream, segments it into atomic units (q/Q frames, BT/ET text blocks,
  m/re...paint path blocks, standalone Do), classifies each by its page-coords
  y-bbox, and wraps in-region units with `q 1 0 0 1 0 SHIFT_Y cm ... Q`.
  State-only ops (Tf font setters, gs graphics-state, ...) are always preserved.

- `scripts/merge_pdf_pages.py` — extract a y-region from one PDF and stamp it on
  another, preserving vectors AND the text layer. Same content-stream segmenter
  as the move script; the filtered source becomes a Form XObject embedded in the
  composite via `pikepdf.copy_foreign`. Optional vector white masks (in composite
  coords) draw on top of the stamp to hide source-side labels.

- `scripts/verify_vector.py` — sanity-check a generated PDF: file size, text
  extractability, panel-label counts, and (with `--source <orig>`) text-layer
  duplication detection — catches the cropbox-stamp failure mode where the
  render is correct but `pdftotext` sees N copies of the page.

- `references/nature_style_checklist.md` — typography/spacing constants from the
  Nature/Science/Cell cheatsheet, in printable form.

These scripts are **starting points**, not finished products. Read the user's
exact constraints (region bounds, anchor point, padding, mask range) and adjust
the constants at the top of each script. The scripts deliberately do not auto-
detect layout — that is your job, because every figure is different.

## Offline / portability notes

Everything here works without network access:
- `pikepdf` is the workhorse for content-stream edits (it wraps QPDF; pure Python interface).
- `pypdf`, `pdfrw`, `reportlab` remain available for niche uses (e.g. building a brand new PDF from scratch); the move/merge scripts no longer need them.
- `pdftoppm` / `pdftocairo` ship with Poppler (Windows: scoop/choco; Linux: `apt install poppler-utils`; macOS: `brew install poppler`). Preview only.
- No cloud APIs. Fonts in source PDFs travel with them as embedded resources, so vector merges keep typography intact automatically.

## Final answer discipline

When you finish, tell the user three things and nothing more:
1. The output paths (PDF, plus SVG/PNG if requested).
2. What you verified (rendered page, text-selectable check, file size, panel labels OK, no double letters).
3. Any compromise you made (e.g. "I used 8 pt padding under the title; tell me if you want it tighter").

Do not paste large code blocks in the final answer. The user has said directly:
> *少写代码，你可以写一点脚本进去，但是排版与多 pdf 矢量融合与微调等在里面做的事情是很宝贵的*

The judgment — coordinate planning, BBox awareness, vector masking, label arbitration, journal-style typography choices — is the value. The boilerplate isn't.

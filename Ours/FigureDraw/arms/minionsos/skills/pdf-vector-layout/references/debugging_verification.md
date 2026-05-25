# Debugging & Verification Workflow

This document captures the **actual debugging and verification methods** used in the v8/v16 sessions. When a PDF layout goes wrong, these are the techniques that found the root cause.

## The verification loop

Every PDF composition step should end with this 3-step check:

1. **Render to PNG** — convert the PDF to a raster preview
2. **Inspect visually** — look for clipping, double labels, wrong spacing, blank regions
3. **Verify vector integrity** — confirm text is still selectable, file size is plausible

If any check fails, **do not proceed**. Fix the issue, re-render, re-check.

## Rendering commands

### Full-page preview (most common)
```bash
pdftocairo -png -r 150 input.pdf output
# or
pdftoppm -png -r 150 input.pdf output
```
- `-r 150`: 150 DPI (good balance of speed and detail; use 300 for final delivery)
- Output: `output-1.png`, `output-2.png`, etc.

### Specific page only
```bash
pdftocairo -png -f 1 -l 1 -r 150 input.pdf output
```
- `-f 1 -l 1`: first page only (faster for multi-page PDFs)

### Crop to a region (for focused inspection)
```python
from PIL import Image
img = Image.open('figureX_v16.png')
# Inspect bottom half only
bottom_half = img.crop((0, img.height//2, img.width, img.height))
bottom_half.save('tmp/figureX_v16_bottom_check.png')
```

Use this when you only changed one region and don't need to re-inspect the whole page.

## Locating content in a rendered page

### Find the bounding box of all non-white content
```python
from PIL import Image
img = Image.open('source.png').convert('RGB')
xs, ys = [], []
for y in range(img.height):
    for x in range(img.width):
        r, g, b = img.getpixel((x, y))
        if min(r, g, b) < 245:  # not white
            xs.append(x)
            ys.append(y)
print('bbox', (min(xs), min(ys), max(xs), max(ys)))
```

This tells you where the actual content sits in pixel coordinates. Use it to:
- Confirm a region is not blank
- Measure the gap between two elements
- Find the top/bottom edge of a row

### Find only colored data points (exclude black text/axes)
```python
from PIL import Image
img = Image.open('source.png').convert('RGB')
xs, ys = [], []
for y in range(img.height):
    for x in range(img.width):
        r, g, b = img.getpixel((x, y))
        # Colored: not white, and has hue (max - min > 20)
        if min(r, g, b) < 245 and max(r, g, b) - min(r, g, b) > 20:
            xs.append(x)
            ys.append(y)
print('colored_bbox', (min(xs), min(ys), max(xs), max(ys)))
```

Use this to find where the actual data (scatter points, bars, lines) sits, ignoring axes and labels.

### Convert pixel coordinates to PDF points
```python
# Given: rendered at 150 DPI, PDF page height H_pt
def y_px_to_pt(y_px, img_height_px, pdf_height_pt):
    # PDF y-axis points up, image y-axis points down
    return pdf_height_pt * (1 - y_px / img_height_px)

# Example: page is 595.28 pt tall, rendered to 1241 px
y_pt = y_px_to_pt(420, 1241, 595.28)
```

Use this to translate a visual measurement ("the row starts at pixel 420") into a PDF coordinate you can use in `pypdf` or `reportlab`.

### Find active rows in a region (for dense inspection)
```python
from PIL import Image
img = Image.open('source.png').convert('RGB')
# Scan rows 380–900 for colored or dark pixels
rows = []
for y in range(380, 900):
    color_count = 0
    dark_count = 0
    for x in range(img.width):
        r, g, b = img.getpixel((x, y))
        if max(r, g, b) < 80:  # dark (text, axes)
            dark_count += 1
        elif min(r, g, b) < 245 and max(r, g, b) - min(r, g, b) > 20:  # colored
            color_count += 1
    if color_count > 20 or dark_count > 20:
        rows.append((y, color_count, dark_count))

print('first 40 active rows:')
for row in rows[:40]:
    print(row)
```

Use this to find the exact y-range of a panel or row. The v16 session used this to locate the wet-experiment row's top edge.

## Inspecting PDF structure

### Read page geometry
```python
from pypdf import PdfReader
reader = PdfReader('input.pdf')
page = reader.pages[0]
mb = page.mediabox
cb = page.cropbox
print('mediabox', float(mb.left), float(mb.bottom), float(mb.right), float(mb.top))
print('cropbox', float(cb.left), float(cb.bottom), float(cb.right), float(cb.top))
print('rotation', page.get('/Rotate'))
```

Use this to:
- Confirm the page size (e.g. 595.28 × 841.89 pt = A4)
- Check if the page is rotated (rotation should be `None` or `0` for most figures)
- Verify cropbox matches mediabox (if they differ, the page is clipped)

### Read Form XObject bounding box
```python
from pdfrw import PdfReader
reader = PdfReader('input.pdf')
page = reader.pages[0]
# Extract a Form XObject (e.g. from a merged page)
# This is advanced — only needed when using pdfrw + reportlab
form = page.Resources.XObject.SomeFormName  # replace with actual name
bbox = [float(x) for x in form.BBox]
print('BBox', bbox)  # [left, bottom, right, top]
```

**Critical:** Form XObject bounding boxes do NOT always start at `(0, 0)`. The v16 session failed because `row_view.BBox` had a bottom edge of `485.74 pt`, not `0`. When placing a Form, you must subtract `BBox[1]` from your y-translation.

### Check file size
```bash
ls -lh output.pdf
# or
du -h output.pdf
```

A vector page is usually **50 KB – 2 MB**. If the output is > 10 MB, you probably embedded a raster by mistake. Re-check the pipeline.

### Verify text is selectable
```bash
pdftotext output.pdf -
```

This extracts all text from the PDF. If you see the expected panel letters, axis labels, and legend text, the PDF is still vector. If you see nothing (or garbled characters), you accidentally rasterized it.

## Debugging blank or misplaced content

### Symptom: Output PDF is blank or missing a region

**Diagnosis steps:**
1. Render the PDF to PNG. Is the region truly blank, or just off-canvas?
2. Check the script's output file timestamp: `ls -l output.pdf`. Did it actually write?
3. If it wrote, check file size. If it's < 10 KB, the script probably errored silently.
4. Re-run the script with `print()` statements before and after each `writer.write()` call.

**Common causes:**
- The script exited 0 but never called `writer.write()` (path mistake, exception caught and ignored).
- The content was placed outside the page's mediabox (e.g. negative y, or y > page height).
- Form XObject BBox was not accounted for (see "Read Form XObject bounding box" above).

### Symptom: Content is clipped (e.g. "g 被裁断了")

**Diagnosis steps:**
1. Render the PDF to PNG at 150 DPI.
2. Use the "Find the bounding box of all non-white content" script to measure the actual content extent in pixels.
3. Convert the top edge from pixels to PDF points.
4. Compare to the clip box you set in the script. Is the clip box's top y at least 4–6 pt above the content's top?

**Fix:**
Increase the clip box's height by 4–6 pt, and shift the content up by the same amount. Example:
```python
# Before
clip_top = 640.3
# After
clip_top = 646.3  # +6 pt safety margin
```

### Symptom: Two sets of panel letters are visible

**Diagnosis steps:**
1. Render the PDF to PNG.
2. Visually confirm: are there two `g` letters, or two `f` letters?
3. Use `pdftotext output.pdf -` and count occurrences: `grep -o 'g' | wc -l`.

**Fix:**
Add a vector white-fill rectangle over the source PDF's letters, constrained to not bleed into the composite's labels. Example:
```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

c = canvas.Canvas('mask.pdf', pagesize=letter)
c.setFillColorRGB(1, 1, 1)  # white
# Mask the source's 'e/f/g/h/i' letters, which sit at y ≥ 424 pt
c.rect(10, 424, 500, 30, fill=1, stroke=0)
c.save()
```

Then merge this mask into the composite before placing the source content.

### Symptom: Spacing is wrong ("再紧凑一点")

**Diagnosis steps:**
1. Render the PDF to PNG at 150 DPI.
2. Measure the gap in pixels (e.g. from the bottom of the title text to the top of the panel).
3. Convert to points: `gap_pt = gap_px * 72 / 150`.
4. Compare to the target (6–10 pt for title-to-panel, 8–12 pt for inter-panel).

**Fix:**
Adjust the y-coordinate in the script by the difference. Example:
```python
# Before: title at y=500, panel at y=480 → gap = 20 pt (too loose)
# After: move panel up to y=492 → gap = 8 pt
panel_y = 492
```

Re-render and re-measure. Do not iterate more than twice without asking the user.

## Comparing two versions (before/after)

### Visual diff
```bash
# Render both to PNG at the same DPI
pdftocairo -png -r 150 before.pdf before
pdftocairo -png -r 150 after.pdf after

# Open both in an image viewer and toggle between them
# Or use ImageMagick to create a diff image:
compare before-1.png after-1.png diff.png
```

The diff image will highlight changed regions in red. Use this to confirm your adjustment affected only the intended region.

### Text diff
```bash
pdftotext before.pdf before.txt
pdftotext after.pdf after.txt
diff before.txt after.txt
```

Use this to confirm you didn't accidentally delete or duplicate text.

## When to use each technique

| Situation | Technique |
|-----------|-----------|
| Just composed a PDF, need to check it | Render full page to PNG at 150 DPI, inspect visually |
| Changed only one region (e.g. bottom row) | Crop the PNG to that region, inspect the crop |
| Need to measure a gap or find a boundary | Render to PNG, use the "Find bounding box" script, convert px → pt |
| Content is blank or off-canvas | Check file size, check timestamp, re-run with debug prints, inspect PDF structure |
| Content is clipped | Render to PNG, measure the clipped edge, increase clip box by 4–6 pt |
| Two labels visible when there should be one | Render to PNG, use `pdftotext` to count occurrences, add a vector white mask |
| Spacing is wrong | Render to PNG, measure the gap in pixels, convert to points, adjust coordinate |
| Need to confirm vector integrity | Run `pdftotext`, check file size, check that text is selectable in a PDF viewer |
| Comparing before/after | Render both to PNG, use `compare` or toggle in a viewer; or use `pdftotext` + `diff` |

## The "trust but verify" rule

The v16 session lost time because a script exited 0 but produced no output (path mistake). The lesson:

**Never trust that a script worked just because it didn't error.** Always:
1. Check the output file's timestamp: `ls -l output.pdf`
2. Check the file size: `ls -lh output.pdf`
3. Render the first page to PNG and look at it

If any of these checks fail, **stop and debug before proceeding**. Do not stack more operations on top of a broken intermediate file.

## Debugging checklist (run after every composition step)

- [ ] Output file exists and has a recent timestamp
- [ ] File size is plausible (50 KB – 2 MB for a vector page)
- [ ] Rendered PNG shows the expected content (no blank regions, no clipping)
- [ ] Text is selectable (`pdftotext output.pdf -` returns the expected strings)
- [ ] Only one set of panel letters is visible (if applicable)
- [ ] Spacing matches the target (measure in PNG, convert to points)
- [ ] No unexpected changes in other regions (compare before/after PNGs)

If all checks pass, proceed to the next step. If any check fails, fix it before moving on.

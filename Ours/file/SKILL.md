---
name: file
description: "Atomic alternative to Write/Edit. Trigger BEFORE writing on: (a) files >~200 lines, (b) CJK / code-fences / math / heredoc-token content, (c) any path where Write/Edit already failed this session, (d) documents >~50KB, (e) any CJK + LaTeX / multi-section report regardless of size. Tier 0 (CJK + LaTeX / heredoc-token / multi-section): seed-and-Edit only — no Bash heredoc, immune to the Opus 4.7 empty-input bug. Tier 1 (ASCII <12KB): Python pathlib + atomic rename in a quoted Bash heredoc. Tier 1.5 (12-50KB): multi-call parts + assembly. Tier 2 (>50KB): chunked generation, manifest, read-back verification, assembly."
---

# Reliable File IO — from single edits to long documents

## How to invoke this skill

This is a **procedural skill**, not an executable tool. Loading the skill only returns these instructions — it does NOT perform any file write. To actually write a file, your **next tool call** must be `Bash` with a fully-formed `command` parameter using the Python heredoc template in the "Tier 1" section below.

Do NOT:
- Call this skill with `args` containing your content (args are ignored)
- Emit a `Bash` tool call with an empty / missing `command` field
- Wait for the skill to "return" results — it returns instructions only

Do:
- Read the Tier 1 template, inline your TARGET path and content into a `python3 - <<'PY' ... PY` heredoc, and pass the whole thing as the `command` argument to `Bash`.

## CRITICAL: Output budget rule

**If your Bash command would exceed ~4000 output tokens (~12KB of content), you MUST split it across multiple Bash calls.** The model has a finite output budget per turn. When context is large, a single 20KB heredoc will be truncated to 0 tokens, producing `Bash input={}` errors.

**Symptoms of hitting this limit:**
- `Bash` returns `InputValidationError: The required parameter 'command' is missing`
- `output_tokens: 0` in the response
- Repeated identical empty Bash calls in a loop

**Recovery (mandatory — do NOT retry the same approach):**
1. Split your content into 3-5 parts, each under 10KB
2. Write each part to a numbered temp file using separate Bash calls
3. Final Bash call: read all parts and assemble with `atomic_write`

See "Tier 1.5: Multi-call assembly" below for the exact template.

---

## Tier 0 — Empty-input failure on CJK + LaTeX / heredoc payloads (Opus 4.7) — READ FIRST

Opus 4.7 has a confirmed failure mode where a `tool_use` whose `input` field must carry a long CJK + LaTeX / heredoc / Markdown payload comes through with `input: {}` and the harness rejects it with `InputValidationError: required parameter <field> is missing`. The failed turn shows tiny `output_tokens` (often < 100), so it is NOT a max_tokens or context-length issue — the model silently bails on emitting the long structured field.

**This invalidates Tier 1's single Bash heredoc for CJK/LaTeX content even when total size is well under the 12KB heredoc limit.** The heredoc does not protect you — the failure happens during the model's emission of the `command` string itself, before the heredoc is ever evaluated. **Tier 1.5's per-part heredoc has the same failure mode for the same reason.**

### Mandatory recipe for CJK + LaTeX / multi-section reports / mixed CJK+math docs

Use this path whenever content matches **any** of: contains CJK; contains LaTeX math (`$...$`, `\begin{...}`); contains heredoc-style tokens (`EOF`, `PY`, `<<`); is a multi-section structured report.

1. **Seed a skeleton via one short `Write`** (≤ ~50 lines / ~3 KB total):
   - LaTeX: preamble + `\begin{document}` + section placeholders + `\end{document}`
   - HTML: `<head>` + boilerplate `<body>` + closing `</body></html>`
   - Markdown: title + table-of-contents stub + a final sentinel line you can target later
2. **Append every section via successive `Edit` calls**, inserting *before* the closing token (`\end{document}`, `</body>`, the final sentinel). Each Edit's `new_string` ≤ ~50 lines / ~3 KB. Sections longer than that → split across 2–3 Edits.
3. **No Bash heredocs containing CJK + LaTeX payloads.** The heredoc body becomes the oversize `Bash.command` string and triggers the same empty-input failure. This explicitly overrides Tier 1's `python3 - <<'PY' ... PY` template for this content shape.
4. If atomic guarantees are needed, seed-and-Edit into `<target>.tmp` and `mv` at the end. Seed-and-Edit on the live target is not atomic, but a final rename closes the gap.

### When the heredoc Tier 1 IS still safe

- ASCII-only content (no CJK, no smart quotes, no math) under ~3 KB
- Pure data dumps (JSON, CSV) under ~10 KB
- One-shot small config writes
- The `python3` heredoc itself when the *Python source* is small and any CJK lives only in a small inline data dict

If in doubt → seed-and-Edit. The seed-and-Edit recipe is immune to this bug because every tool_use's `input` is small and structurally simple.

### Recovery from a live empty-input failure

1. Do NOT retry the same single-call approach (this is the third-failure-loop trap).
2. Switch to seed-and-Edit immediately, even if you were mid-Tier-1.5.
3. If the empty-input failure was the only artifact in the session and the file does not yet exist, just start the seed-and-Edit path from scratch. No state to recover.

### Confirmed failure case

`/Users/mjm/.claude/projects/-Users-mjm-Desktop-Paper-Crash/1c9cbe69-…jsonl` on 2026-05-24 — three consecutive empty-input failures: (1) one `Write` of an entire Chinese LaTeX comparison report, (2) a Bash heredoc embedding the whole Markdown report (Tier 1 path), (3) the same heredoc retried. cache_read 25K, output_tokens 47/74/25. Three failures in a row before user intervention.

## Scope

This skill covers FOUR tiers of file writing reliability:

0. **Tier 0 — Seed-and-Edit (CJK + LaTeX / multi-section / heredoc-token shapes)**: Mandatory whenever content shape can trigger the Opus 4.7 empty-input bug, regardless of size. Skips Bash heredocs entirely.

1. **Tier 1 — Atomic single-file IO** (replaces Write/Edit): For ASCII content under ~12KB. Uses Python `pathlib` + `atomic_write` inside a quoted Bash heredoc.

2. **Tier 1.5 — Multi-call assembly** (for 12KB-50KB ASCII files): Splits content across multiple Bash calls, then assembles atomically. Use this when a single Bash heredoc would exceed the output budget.

3. **Tier 2 — Long document pipeline** (replaces single-shot generation of large docs): For documents expected to exceed ~50KB. Uses a five-stage workflow: outline -> chunked generation -> read-back verification -> assembly -> final validation.

**Decision rule**:
- Content matches Tier 0 triggers (CJK, LaTeX math, heredoc-tokens, multi-section structured report) -> **Tier 0**, regardless of size
- ASCII content < ~12KB -> Tier 1 (single Bash call)
- ASCII content 12KB-50KB -> Tier 1.5 (multiple Bash calls + assembly)
- Content > 50KB -> Tier 2 (full pipeline; each chunk written via Tier 0 if its content shape matches Tier 0 triggers, else Tier 1)

---

## Pre-flight check (run BEFORE every Write / Edit)

**Any yes** -> use this skill. Do not "try plain first."

**Size signals:**
- Content expected to exceed ~200 lines (single file) or ~50KB (total document)?
- Target file already > ~200 lines?

**Content shape signals:**
- CJK characters in non-trivial volume?
- 3+ code fences, `$math$` blocks, or many smart quotes / em-dashes?
- Literal `EOF`, `PY`, `MARK`, or `CHUNK_*` tokens?

**Edit fragility signals:**
- `old_string` > ~30 lines or has trailing whitespace / NBSP?
- `new_string` > ~50 lines or contains risky content shapes?

**Session state signals:**
- Has any Write or Edit on this path already failed this session?

**Document scale signals:**
- Is this a multi-chapter document (study notes, course material, reports)?
- Will the final output exceed ~50KB?
- Does the user need verification that all sections are present?

## Escalation rules

- **First failure on a path is a one-way door.** No retry with plain Write/Edit.
- **Don't escalate gradually.** If pre-flight trips, jump straight here.
- **Don't mix tools.** If part of a change needs this skill, use it for all parts.
- **Scale up, not down.** If you start with Tier 1 and realize the document is growing past 12KB, switch to Tier 1.5. Past 50KB, switch to Tier 2.
- **Empty Bash = immediate escalation.** If you get `command is missing` error, switch to Tier 1.5 on the next attempt. Never retry the same single-call approach.

---

## Tier 1: Atomic Single-File IO (< ~12KB)

### The template

```bash
python3 - <<'PY'
from pathlib import Path
import os, tempfile

TARGET = Path("/abs/path/to/file.md")

def atomic_write(path: Path, text: str) -> None:
    tmp = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=str(path.parent),
        prefix=f".{path.name}.", suffix=".tmp", delete=False
    )
    try:
        tmp.write(text)
        tmp.flush()
        os.fsync(tmp.fileno())
    finally:
        tmp.close()
    os.replace(tmp.name, path)

# --- operation goes here ---
PY
```

### Operations

**Generate (replaces Write):**
```python
parts = [
"""\
# Title

First section.
""",
"""\
## Section 2

Content with `code fences`, $math$, "smart quotes", 中文.
""",
]
atomic_write(TARGET, "".join(parts))
```

**Update by anchor (replaces Edit):**
```python
text = TARGET.read_text(encoding="utf-8")
anchor = "## Outline\n"
assert text.count(anchor) == 1, f"anchor not unique: {text.count(anchor)} matches"
start = text.index(anchor)
end   = text.index("\n## ", start + 1) + 1
text  = text[:start] + "## Outline (revised)\n\n- New point\n\n" + text[end:]
atomic_write(TARGET, text)
```

**Append (atomic — read-modify-write, never `open("a")`):**
```python
existing = TARGET.read_text(encoding="utf-8") if TARGET.exists() else ""
atomic_write(TARGET, existing + "\n## Appendix\n\nNew material...\n")
```
> Plain `open("a")` is **not atomic** — a crash mid-write leaves a partial tail. Always go through `atomic_write` so the rename is the only externally visible state change.

### Pitfalls
- Always pass `encoding="utf-8"` explicitly.
- Assert `text.count(anchor) == 1` if anchor uniqueness is uncertain.
- Escape `"""` as `\"\"\"` or split across adjacent strings.
- Never run two heredocs concurrently on the same target.

---

## Tier 1.5: Multi-call Assembly (12KB-50KB)

Use this when a single Bash heredoc would exceed the output token budget (~4000 tokens / ~12KB). The idea: write content in multiple smaller Bash calls to numbered part files, then assemble atomically.

### Step 1: Write parts (one Bash call per part, each < 10KB)

```bash
python3 - <<'PY'
from pathlib import Path
PARTS_DIR = Path("/tmp/atomic_parts_UNIQUEID")
PARTS_DIR.mkdir(parents=True, exist_ok=True)

part = """\
<content for this section - keep under 10KB>
"""

(PARTS_DIR / "part_01.txt").write_text(part, encoding="utf-8")
print(f"OK: wrote part_01 ({len(part)} bytes)")
PY
```

Repeat for `part_02.txt`, `part_03.txt`, etc. Each call is independent.

### Step 2: Assemble atomically (final Bash call)

```bash
python3 - <<'PY'
from pathlib import Path
import os, tempfile, shutil

PARTS_DIR = Path("/tmp/atomic_parts_UNIQUEID")
TARGET = Path("/abs/path/to/output.html")

def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=str(path.parent),
        prefix=f".{path.name}.", suffix=".tmp", delete=False
    )
    try:
        tmp.write(text)
        tmp.flush()
        os.fsync(tmp.fileno())
    finally:
        tmp.close()
    os.replace(tmp.name, path)

# Read all parts in order
parts = []
for p in sorted(PARTS_DIR.glob("part_*.txt")):
    parts.append(p.read_text(encoding="utf-8"))

content = "".join(parts)
atomic_write(TARGET, content)
shutil.rmtree(PARTS_DIR)
print(f"OK: assembled {len(parts)} parts -> {TARGET} ({len(content)} bytes)")
PY
```

### Key rules for Tier 1.5
- Each part file must be < 10KB (keeps each Bash call well within output budget)
- Use a unique directory name (include timestamp or random suffix) to avoid collisions
- Parts are plain text fragments — no headers or markers needed
- The assembly step is the only one that touches the target file
- If any part write fails, you can retry just that part
- Always verify the final file size matches expectations

---

## Tier 2: Long Document Pipeline (>50KB)

### When to use Tier 2

- Generating documents > 50KB (study materials, course notes, reports, standards)
- Multi-chapter structured documents (Markdown or LaTeX)
- Documents where completeness verification is critical
- Any scenario where a single Write would exceed tool limits

### The five-stage workflow

```
Stage 1: Planning
  +-- Define document structure (outline)
  +-- Estimate total size and chunk count
  +-- Create project directory with chunks/ subdirectory
  +-- Initialize manifest.json and checkpoint.json
  +-- Each chunk targets 5-15KB (hard max 20KB)

Stage 2: Chunked Generation
  +-- Generate each chunk independently
  +-- Write each chunk using Tier 1 atomic_write (NOT plain Write)
  +-- Compute SHA256 for each chunk file
  +-- Update manifest with chunk metadata
  +-- Update checkpoint after each successful chunk
  +-- Chunk naming: chunk_{chapter}_{section}_{part}.md

Stage 3: Read-back Verification
  +-- Read back every chunk file
  +-- Verify SHA256 matches manifest
  +-- Check chunk ordering is continuous
  +-- Detect missing or duplicate chunks
  +-- Re-generate any failed chunks (return to Stage 2 for that chunk)

Stage 4: Assembly
  +-- Sort chunks by manifest order
  +-- Concatenate with section markers
  +-- Write final file using Tier 1 atomic_write
  +-- Update checkpoint

Stage 5: Final Validation & Repair
  +-- Read back final file
  +-- Verify all chunk start-markers are present
  +-- Validate structure (Markdown fences balanced, LaTeX environments matched)
  +-- If issues found: identify affected chunk, re-generate, re-assemble
  +-- Output verification report
```

### Manifest format

```json
{
  "target_file": "document.md",
  "document_type": "markdown",
  "total_chunks": 12,
  "chunks": [
    {
      "chunk_id": "chunk_1_1_1",
      "order": 1,
      "heading": "## Section 1.1",
      "chunk_file": "chunks/chunk_1_1_1.md",
      "start_marker": "<!-- CHUNK_START: chunk_1_1_1 -->",
      "end_marker": "<!-- CHUNK_END: chunk_1_1_1 -->",
      "sha256": "abc123...",
      "status": "completed",
      "verified": true
    }
  ]
}
```

### Checkpoint format

```json
{
  "current_stage": "generation",
  "completed_chunks": ["chunk_1_1_1", "chunk_1_1_2"],
  "failed_chunks": [],
  "last_verified_chunk": "chunk_1_1_2",
  "assembly_status": "pending",
  "final_verification_status": "pending"
}
```

### Failure recovery

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| Chunk write failed | manifest shows "pending" | Re-generate that chunk only |
| Final file truncated | Missing end markers | Re-assemble from chunks |
| SHA256 mismatch | Verification stage | Re-generate affected chunk |
| Markdown fences unbalanced | Final validation | Locate chunk, re-generate |
| LaTeX environments unmatched | Final validation | Locate chunk, re-generate |

### Key rules for Tier 2

- Every chunk write uses Tier 1's `atomic_write` template — never plain Write/Edit
- Never generate a single chunk > 20KB
- Always read back after writing — "tool call succeeded" != "file is correct"
- Checkpoint after every successful chunk so work is never lost
- Use HTML comment markers for Markdown: `<!-- CHUNK_START: id -->`
- Use LaTeX comment markers for LaTeX: `% CHUNK_START: id`

---

## Prohibited actions (all tiers)

- Single Write/Edit call for content > 200 lines or > 50KB
- Single Bash heredoc for content > ~12KB (use Tier 1.5)
- Claiming file is complete without read-back verification
- Retrying plain Write/Edit after a failure on the same path
- Retrying the same single-call Bash after getting `command is missing` error
- Generating a chunk > 20KB
- Using `bash cat >>` as primary write method (Tier 1 fallback only)
- Assuming tool success means file correctness
- Mixing plain Write/Edit with this skill in one logical change

---

## Bash fallback (only when python3 is unavailable)

Write to a sibling tmp file, fsync, then `mv` — same atomic-rename guarantee as Tier 1, weaker durability.

```bash
TMP="$(mktemp "${FILE}.XXXXXX.tmp")"
cat > "$TMP" <<'EOF_PAYLOAD'
...content...
EOF_PAYLOAD
sync
mv -f "$TMP" "$FILE"
```

Never use `: > "$FILE"` followed by `cat >>` — that truncates the destination before any new bytes are written, so a crash mid-write loses the file.

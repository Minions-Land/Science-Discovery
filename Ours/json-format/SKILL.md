---
name: json-format
description: Format and prettify JSON data with proper indentation and syntax highlighting. Validates JSON structure, fixes common issues, and presents output in a readable format. Trigger when users say "format this JSON", "prettify JSON", "clean up this JSON", or "make this JSON readable".
---

# json-format — Format JSON with proper indentation

**What this does:** Takes raw or malformed JSON data and formats it with proper indentation, validates structure, and optionally adds syntax highlighting for readability.

**When to invoke:**
- User types `/json-format`
- User says "format this JSON", "prettify JSON", "clean up this JSON"
- User asks to "make this JSON readable", "indent this JSON"
- User provides JSON data that appears unformatted or minified

---

## Step 1: Identify JSON source

Check where the JSON data is:
- **Inline in message:** User pasted JSON directly in their message
- **In a file:** User references a file path (e.g., "format data.json")
- **In clipboard/selection:** User says "format this" after selecting text

If the source is a file, read it first using the Read tool.

---

## Step 2: Validate and parse JSON

Attempt to parse the JSON:
- Use Python's `json.loads()` via Bash tool
- If parsing fails, identify the error (missing comma, trailing comma, unquoted keys, etc.)
- Report the specific line and character where parsing failed

Common fixes to attempt automatically:
- Remove trailing commas before `}` or `]`
- Add missing commas between array/object elements
- Quote unquoted keys (if it looks like JavaScript object notation)

If JSON is fundamentally broken and can't be auto-fixed, report the error and ask user for clarification.

---

## Step 3: Format with proper indentation

Once JSON is valid, format it:
- Use 2-space indentation (standard for JSON)
- Ensure consistent spacing around colons and commas
- Break arrays/objects across multiple lines if they contain more than 3 elements
- Keep simple arrays on one line if total length < 80 chars

Use Python's `json.dumps()` with `indent=2` and `ensure_ascii=False` for proper formatting.

---

## Step 4: Add syntax highlighting (optional)

If the output will be displayed in a context that supports it:
- Wrap in markdown code fence with `json` language tag
- For terminal output, consider using color codes (if user's environment supports it)

Default: always use markdown code fence for Claude Code responses.

---

## Step 5: Present formatted output

Show the formatted JSON with:
- Clear indication it's been validated and formatted
- File path (if source was a file)
- Line count and size (if significantly different from input)
- Any fixes that were applied automatically

If user requested to save to a file, use Write tool to save the formatted version.

---

## Decision Rules

| Situation | Action |
|-----------|--------|
| JSON is already well-formatted | Confirm it's valid, show it as-is |
| JSON has minor syntax errors | Auto-fix and report what was fixed |
| JSON is fundamentally broken | Report error location, ask for clarification |
| User wants to save formatted JSON | Use Write tool to save to specified path |
| Input is not JSON at all | Politely inform user and ask if they meant something else |
| JSON is extremely large (>10K lines) | Warn about size, ask if they want to proceed |

---

## Pitfalls

**Don't assume all curly braces mean JSON:**
JavaScript object literals, Python dictionaries, and other formats look similar. If parsing fails, check if user actually meant JSON or another format.

**Don't lose data during formatting:**
Always preserve the exact data values. Formatting should only change whitespace, never content. Use `ensure_ascii=False` to preserve Unicode characters.

**Don't format JSON that's intentionally minified for production:**
If user is working with a production config or API response that needs to stay minified, ask before formatting. Some contexts require compact JSON.

**Don't add comments:**
JSON spec doesn't support comments. If user's input has comments (JSONC/JSON5), preserve them if possible, but warn that standard JSON parsers will reject them.

**Don't auto-fix without reporting:**
Always tell the user what was fixed. Silent fixes can hide real data issues that need attention.

---

## Related Skills

- [[skill-edit]] — For editing the skill itself
- [[file]] — For handling large JSON files atomically

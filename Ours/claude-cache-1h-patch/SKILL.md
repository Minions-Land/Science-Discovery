---
name: claude-cache-1h-patch
description: "Patch Claude Code's native binary so it uses 1-hour prompt caching (ttl:\"1h\") instead of the default 5-minute TTL. Triggers: user asks to install/repatch/check/restore the 1h cache patch, says 'apply the cache patch', 'extend Claude Code cache', references the patch installer or test script, or mentions cache_creation buckets / extended-cache-ttl beta. Operational scripts live in ~/Tools/claude-1h-cache-patch/."
---

# /claude-cache-1h-patch — Claude Code 1-hour cache patch

Patches the locally-installed Claude Code native binary so every `cache_control` block it sends carries `ttl:"1h"` and the request includes the `extended-cache-ttl-2025-04-11` beta header. Idempotent, reversible, survives via timestamped backups.

The patch alone does **not** guarantee server-side savings: relays may downgrade `1h` to `5m`. The skill includes a verification step that detects this end to end.

---

## Trigger phrases

Run when the user says any of:
- "apply / install / re-apply the 1h cache patch"
- "patch Claude Code", "repatch claude", "fix Claude Code cache TTL"
- "check the cache patch status"
- "restore / unpatch the original Claude Code"
- "test if 1h cache really works on this relay"

If the user invokes `/claude-cache-1h-patch <subcommand>`, dispatch by subcommand. Bare invocation defaults to `status`.

---

## Host facts (load-bearing — do not guess)

Verified on this host (macOS arm64, Claude Code 2.1.143):

| Fact | Value |
|---|---|
| Install method | Homebrew npm: `/opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/` |
| Binary path | `bin/claude.exe` (Mach-O arm64, ~206 MB) |
| Sister copy | `node_modules/@anthropic-ai/claude-code-darwin-arm64/claude` (Apple-signed; install.cjs copies it over `bin/claude.exe` on every npm/brew upgrade — this is what makes the patch lose-on-upgrade) |
| Version-gated function | `ikH(H)` (was `cX5` in older 2.x versions; ryfineZ's upstream patch script targets the old name and silently misses) |
| Patch marker | `__1h_patched_ikH__` |
| Operational scripts | `~/Tools/claude-1h-cache-patch/install.sh` (canonical), `repatch.sh` (symlink), `test_cache.sh` |

The patch does **equal-length byte replacement** (461 bytes → `function ikH(H){return!0}` + space padding), then ad-hoc re-signs (the original Apple Developer ID signature breaks once any byte changes). Backups: `claude.exe.1h-cache-bak-<UTC-timestamp>` next to the binary.

---

## Subcommands

### 1. `status` — show current state (default)

```
~/Tools/claude-1h-cache-patch/install.sh status
```

Reports binary path, size, version, patched-or-not, signature type (`adhoc` vs Apple), and latest backup. Read-only. Run this first whenever the user asks an open-ended "is the patch active?" question.

### 2. `patch` (alias: `install`) — apply the patch

```
~/Tools/claude-1h-cache-patch/install.sh patch
```

What happens:
1. If already patched: prints "already patched" and exits 0.
2. Otherwise: timestamped backup → byte replace → ad-hoc re-sign → smoke test `claude --version`.
3. On byte-pattern mismatch (Anthropic re-minified upstream): refuses to patch and prints diagnostic. See **Recovery: upstream byte drift** below.

Run this after every `brew upgrade @anthropic-ai/claude-code` or `npm i -g @anthropic-ai/claude-code`.

### 3. `restore` (alias: `unpatch`) — roll back

```
~/Tools/claude-1h-cache-patch/install.sh restore
```

Copies the most recent backup over the live binary. The original signature was an Apple Developer ID, but if the script previously re-signed the backup (rare), the restored copy may show ad-hoc — check with `status`.

### 4. `test_cache.sh` — verify end-to-end

```
SLEEP_SECS=600 ~/Tools/claude-1h-cache-patch/test_cache.sh
```

Sends a unique system prompt twice with a configurable gap (default 360s, override via `SLEEP_SECS`). Reads `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` from `~/.claude/settings.json`.

**The strict verdict** is whether `ephemeral_1h_input_tokens > 0` in the response usage. That is the only field that proves the relay/server actually charged the 1h bucket. A non-zero `cache_read_input_tokens` alone does not — short-TTL caches sometimes survive past nominal expiry, and shared upstream caches can register reads on never-before-sent payloads.

---

## How to verify the patch is *really* working

Two independent verifications:

### A) Wire-level: did the client actually send `ttl:"1h"`?

This proves the byte patch worked, regardless of server response.

1. Start a tiny echo server that captures the request body and returns a stub response:

   ```bash
   python3 - <<'EOF_PY'
   import http.server, json, sys
   class H(http.server.BaseHTTPRequestHandler):
       def do_POST(self):
           ln = int(self.headers.get('content-length') or 0)
           body = self.rfile.read(ln)
           open('/tmp/echo_request.json','w').write(json.dumps({
               'path': self.path,
               'headers': dict(self.headers),
               'body': json.loads(body) if body else None,
           }, indent=2))
           rb = json.dumps({'id':'msg_stub','type':'message','role':'assistant',
               'model':'claude-haiku-4-5-20251001',
               'content':[{'type':'text','text':'stub'}],'stop_reason':'end_turn',
               'stop_sequence':None,'usage':{'input_tokens':1,'output_tokens':1,
               'cache_creation_input_tokens':0,'cache_read_input_tokens':0}}).encode()
           self.send_response(200); self.send_header('content-type','application/json')
           self.send_header('content-length', str(len(rb))); self.end_headers()
           self.wfile.write(rb)
       def log_message(self,*a,**k): pass
   http.server.HTTPServer(('127.0.0.1',18888),H).serve_forever()
   EOF_PY
   ```
   Run that file in the background.

2. Run patched claude with an isolated `HOME` (so it does not pick up the user's normal `ANTHROPIC_BASE_URL`):

   ```bash
   TMP_HOME=$(mktemp -d); mkdir -p "$TMP_HOME/.claude"
   cat > "$TMP_HOME/.claude/settings.json" <<EOF_CFG
   {"env":{"ANTHROPIC_BASE_URL":"http://127.0.0.1:18888","ANTHROPIC_AUTH_TOKEN":"sk-fake","ANTHROPIC_API_KEY":"sk-fake"}}
   EOF_CFG
   HOME="$TMP_HOME" /opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe \
       --print --model claude-haiku-4-5-20251001 'reply ok' &
   sleep 12; kill %1 2>/dev/null
   ```

3. Inspect `/tmp/echo_request.json`. Confirm:
   - `headers["anthropic-beta"]` contains `extended-cache-ttl-2025-04-11`
   - Every `cache_control` field is `{"type":"ephemeral","ttl":"1h"}` (not bare `{"type":"ephemeral"}`)

### B) End-to-end: does the relay/server honor 1h?

```bash
SLEEP_SECS=600 ~/Tools/claude-1h-cache-patch/test_cache.sh
```

Verdict mapping:

| `ephemeral_1h_input_tokens` | `cache_read_input_tokens` (2nd call) | Meaning |
|---|---|---|
| > 0 (either call) | any | 1h is really working — server charged 1h bucket |
| 0 (always) | > 0 | Relay silently downgraded 1h → 5m. Patch is harmless but no real 1h savings |
| 0 (always) | 0 | No cache hit at all; cache expired before second probe |

---

## Recovery: upstream byte drift

When Anthropic ships a new version with re-minified code, `install.sh patch` aborts with:

```
ABORT: expected exactly 1 occurrence of ikH source, found N.
```

Steps to refresh:

1. Find the new gating function — search by stable string anchors:

   ```bash
   /usr/bin/grep -ao 'function [a-zA-Z0-9_]\{1,8\}(H){[^}]*FORCE_PROMPT_CACHING_5M[^}]*}' \
     /opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe | head -3
   ```

   Expect one hit. The function may have been renamed (e.g. `ikH` → `XYZ`). It may also span more than one `}` since the body may contain nested objects — if grep above only catches the prefix, fall back to:

   ```bash
   python3 -c "
   import re, pathlib
   d = pathlib.Path('/opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe').read_bytes()
   for m in re.finditer(rb'ENABLE_PROMPT_CACHING_1H_BEDROCK', d):
       s = max(0, m.start() - 200); e = min(len(d), m.end() + 600)
       print(d[s:e].decode('utf-8', 'replace'), '\n---\n')
   "
   ```

2. From the dump, copy the exact bytes from `function <name>(H){` through the matching `}` that closes the function (look for `H===q)}` or whatever the `.some(...)` callback ends with).

3. Update the `ORIG = b'...'` literal in `~/Tools/claude-1h-cache-patch/install.sh` (lines starting at `ORIG = (`). Update the function name in `PATCH_BODY` if it changed (`function <newname>(H){return!0}`). Update `MARKER` if you want a fresh marker keyed to the new name.

4. Re-run `install.sh patch`. It should succeed with `patched ok (N bytes replaced in place)`.

5. Smoke-test with `claude --version` and re-run the wire-level verification above.

---

## Recovery: binary won't run after patch

If `claude --version` exits non-zero or shows "killed" after re-sign:

1. `~/Tools/claude-1h-cache-patch/install.sh restore` — back to the latest backup.
2. Inspect `codesign -v -v <binary>` for Gatekeeper complaints.
3. The byte replacement is equal-length, so this is almost always a re-sign issue, not a content issue. Try `codesign --remove-signature <binary>; codesign -s - <binary>` manually.
4. As a last resort: `npm i -g @anthropic-ai/claude-code@<exact-version>` to force a clean reinstall, then re-patch.

---

## What this skill will NOT do

- Patch Claude Code installed via the standalone native installer at `~/.local/share/claude/versions/`. ryfineZ's upstream `claude-1h-cache.py` covers that path; if a future install on this host uses it, factor that path into the script.
- Touch any file under `~/.claude/`. Settings, hooks, plugins are unrelated to this patch.
- Help with Bedrock/Vertex 1h cache gating (those use separate env vars: `ENABLE_PROMPT_CACHING_1H_BEDROCK` / Vertex equivalents — Anthropic's official path, no patch needed).

---

## Notes for future maintainers

- The `~/Tools/claude-1h-cache-patch/install.sh` script is the source of truth. Treat this SKILL.md as a runbook around it, not a copy of it.
- The most recent upstream `ryfineZ/claude-1h-cache-patch` does not match Claude Code 2.x's renamed function and the npm-native-binary install layout. Do not run that script directly on this host.
- `claude.exe` and `node_modules/.../claude-darwin-arm64/claude` are hard links at install time but break apart once `codesign` runs (codesign rewrites `__LINKEDIT` and copies on write). Both files end up patched in the byte sense, but only `claude.exe` carries valid ad-hoc signing afterward; the sister copy is left as the unpatched original to keep its Apple signature valid (it gets re-copied to `bin/claude.exe` on the next install anyway).
- Why the strict `ephemeral_1h_input_tokens > 0` rule: cache_read alone is misleading because Anthropic's 5-minute TTL is observably soft (cached prefixes can return on reads after 6+ minutes idle), and relays may share upstream caches across users. The 1h bucket field is the only signal that proves the request was actually billed at the 1h rate.

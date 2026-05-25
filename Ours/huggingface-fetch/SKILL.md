---
name: huggingface-fetch
description: "Pull HuggingFace datasets/models from this host. Use when the user wants to download anything off `huggingface.co` — dataset, model, single file, gated repo. Inherits a load-bearing host fact: huggingface.co is fully TCP-reset on this network (curl 35 / connection reset by peer), miniconda Python's OpenSSL 3.6.2 hits SSL EOF on hf-mirror.com handshake. The stable path is curl + hf-mirror.com (LibreSSL on system curl works); for whole-repo downloads the `hf` CLI works only when pointed at hf-mirror via HF_ENDPOINT, and only with a Python that uses the system SSL stack. Falls back to git clone via hf-mirror, then to mirrored-but-LFS-broken cases that need a manual xet-bridge workaround."
---

# /huggingface-fetch — Pull HuggingFace data on this host

A reusable read-only counterpart to [[github-fetch]] for `huggingface.co`. Use when the target is "download dataset X from HF", "pull model Y", "grab the GAIA test set" — not "look at this URL" (use [[github-fetch]] for plain GitHub).

Trigger phrases:
- "pull / download / fetch from huggingface", "huggingface dataset", "hf:" URL
- A pasted `huggingface.co/...` or `hf.co/...` URL
- "snap-research/locomo", "princeton-nlp/SWE-bench" — i.e. owner/repo strings without protocol that look like HF IDs

---

## Host facts (load-bearing)

Verified 2026-05-22:

- **`huggingface.co` is dead on this host.** `curl https://huggingface.co/` returns `(35) Recv failure: Connection reset by peer` immediately. DNS resolves cleanly (`3.167.192.4`), so it's network-level filtering, not DNS. No combination of `--http1.1`, `--tlsv1.3`, or browser User-Agent recovers it.
- **`hf-mirror.com` works** — Chinese community mirror that proxies `huggingface.co`. Returns 200 in ~0.3-1s. This is the only working endpoint we've found.
- **`hf-mirror.com` redirects unowner-prefixed dataset slugs** — e.g. `squad` → `rajpurkar/squad`. The `/api/datasets/squad` call returns 401 (`Invalid username or password`); `/api/datasets/rajpurkar/squad` returns 200. Always use the canonical `<owner>/<repo>` form. If you don't know the owner, hit `/api/datasets/<slug>/tree/main?recursive=true` first — it 307s to the canonical path you can parse out.
- **miniconda Python (OpenSSL 3.6.2) cannot TLS-handshake hf-mirror.** Every `requests`, `urllib`, `httpx` call fails with `[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol`. System Python 3.9 (LibreSSL 2.8.3) fails the same way. **System `curl` (LibreSSL on macOS) is the only thing that works reliably.**
- **`hf` (the new CLI; `huggingface-cli` was renamed)** is installed at `/Users/mjm/miniconda3/bin/hf` (`hf --version` → 1.8.0). **It inherits the miniconda SSL bug**, so `HF_ENDPOINT=https://hf-mirror.com hf download ...` fails with the same `_ssl.c:1032` error. Don't trust the CLI on this host. Use `curl` directly.
- **Git over hf-mirror works** for the metadata + small files, but **LFS objects fail** because the smudge filter calls `cas-bridge.xethub.hf-mirror.org` which doesn't resolve (NXDOMAIN). For LFS-backed datasets you have to skip LFS at clone time and rewrite individual file URLs to the mirror.
- `hf_transfer` Python extension does not help — it still depends on the same SSL stack to reach the endpoint.

**Implication:** the working recipe is **`curl` against `hf-mirror.com` with the canonical `<owner>/<repo>` slug**, looping over the file list returned from the tree API. Build a `fetch.sh` mirroring [[github-fetch]] Step 3.

---

## Step 1 — Decide the scope

| Scope | Use |
|---|---|
| Single file (README, one parquet) | `curl` resolve URL |
| All files in a small repo (≤ a few hundred MB) | tree listing + bulk curl |
| Whole repo with LFS-heavy data (multi-GB parquet/safetensors) | git clone via mirror + selective LFS pull (see Step 5) |
| Just metadata (size, license, files list) | `curl /api/datasets/<o>/<r>` |

If the user gave a `huggingface.co/datasets/<owner>/<repo>/...` URL, swap the host to `hf-mirror.com`. The path stays identical.

---

## Step 2 — Confirm reachability and resolve canonical slug

```bash
# Always works on this host:
curl -sS --max-time 10 -o /dev/null -w "mirror: %{http_code} %{time_total}s\n" https://hf-mirror.com/

# Resolve canonical owner if the user gave you a bare slug.
# This 307s; --max-redirs 0 lets you parse the Location header.
curl -sS --max-time 10 -I "https://hf-mirror.com/api/datasets/<slug>" | grep -i location

# Get repo metadata (use canonical owner/repo from above):
curl -sS --max-time 15 "https://hf-mirror.com/api/datasets/<owner>/<repo>" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print({k:d.get(k) for k in ['id','sha','lastModified','license','downloads']})"
```

If `hf-mirror.com` itself returns non-200, this skill is stale — see Step 8 self-update.

---

## Step 3 — Single-file or small set fetch

```bash
mkdir -p <local-dir> && cd <local-dir>
curl -sSL --max-time 60 -o <local-name> \
  "https://hf-mirror.com/datasets/<owner>/<repo>/resolve/main/<path>"
```

The `resolve/main/<path>` form follows the LFS pointer if present and serves either the inline blob or a redirect to a mirrored CDN URL — both work on this host. `raw/main/<path>` returns the raw text without LFS resolution; use it for `README.md`, `dataset_infos.json`, etc.

**Models** use the same shape: `https://hf-mirror.com/<owner>/<repo>/resolve/main/<path>` (no `/datasets/` prefix).

---

## Step 4 — Listing files (when you don't know the names)

```bash
curl -sSL --max-time 30 \
  "https://hf-mirror.com/api/datasets/<owner>/<repo>/tree/main?recursive=true" \
  | python3 -c "import json,sys; [print(f\"{f['type']}\\t{f['path']}\\t{f.get('size','')}\") for f in json.load(sys.stdin)]"
```

For models, drop `/datasets`: `/api/models/<owner>/<repo>/tree/main?recursive=true`.

From the listing, build a `fetch.sh` with one `curl` per blob. Avoid stuffing many `curl`s into a single inline `for` loop in the Bash tool — same failure mode as in [[github-fetch]].

---

## Step 5 — Whole repo (git over hf-mirror)

For repos large enough to warrant a real clone:

```bash
# Avoid the smudge-filter break by skipping LFS, then re-fetching with rewritten URL.
GIT_LFS_SKIP_SMUDGE=1 git clone --depth=1 \
  https://hf-mirror.com/datasets/<owner>/<repo> <local-dir>
cd <local-dir>

# Rewrite the LFS endpoint so smudge doesn't dial xethub-bridge:
git config -f .lfsconfig lfs.url "https://hf-mirror.com/datasets/<owner>/<repo>.git/info/lfs"

# Now fetch what you actually need — full or filtered:
git lfs fetch --include "data/**"   # narrow it down — don't pull the whole world
git lfs checkout
```

If the LFS fetch still fails with `cas-bridge.xethub.hf-mirror.org: no such host` errors, the dataset uses the new Xet storage backend and the mirror hasn't proxied it yet. Two paths from there:

1. **Use the parquet-converted snapshot** at `hf-mirror.com/datasets/<owner>/<repo>/resolve/refs%2Fconvert%2Fparquet/...` — almost every public dataset has one auto-generated.
2. **Skip the dataset** and ask the user to download via a non-CLI method (browser through VPN, or HF Spaces export).

---

## Step 6 — Gated / token-required datasets (GAIA, ImageNet, etc.)

Some repos require accepting terms + a HF token (e.g. `gaia-benchmark/GAIA`, `meta-llama/Llama-2-7b`, `ILSVRC/imagenet-1k`).

1. **Get a token** at https://huggingface.co/settings/tokens (need a working browser/network for this — typically over VPN).
2. **Pass it to curl:**
   ```bash
   export HF_TOKEN="hf_..."
   curl -sSL --max-time 60 -H "Authorization: Bearer $HF_TOKEN" \
     -o <local-name> \
     "https://hf-mirror.com/datasets/<owner>/<repo>/resolve/main/<path>"
   ```
3. **Mirror caveat:** `hf-mirror.com` proxies the auth header to upstream, but if the upstream rejects (terms not yet accepted), the mirror returns the upstream 401/403 wrapped as `{"error":"Invalid username or password."}`. Accept the terms once on huggingface.co (over VPN) and the same token then works through the mirror.

If the user has not accepted the terms and can't reach huggingface.co directly, the request is blocked at the policy layer, not the network — there is no skill-level workaround. Tell them and stop.

---

## Step 7 — Report

When handing back, include:
- Repo + revision SHA (`curl https://hf-mirror.com/api/datasets/<o>/<r> | jq .sha`)
- What was downloaded and where
- License from the metadata (HF datasets often have research-only or non-commercial terms — flag if so)
- Whether the LFS path was needed and which storage backend (legacy LFS vs Xet)

---

## Pitfalls

- **Don't use `huggingface-cli` / `hf` on this host.** It will look like it works (no early error) and then fail mid-handshake. Use curl.
- **Don't WebFetch huggingface.co.** Same TCP reset hits agent-side fetch tools.
- **Don't trust the bare slug** (`squad`, `glue`). HF's auto-redirect to canonical owner is fine in a browser; on the API + mirror, an unowner slug returns 401 and looks like an auth failure. Always resolve to `<owner>/<repo>` first.
- **Don't `git clone` without `GIT_LFS_SKIP_SMUDGE=1`.** Smudge will try to resolve `cas-bridge.xethub.hf-mirror.org` and fail noisily; the clone partially completes and you waste a minute thinking it worked.
- **Don't leave the hf-mirror lfs.url at the default after clone.** The repo's `.lfsconfig` may pin xethub-bridge; override with `git config -f .lfsconfig lfs.url ...` before any `git lfs *` command.
- **Don't paste your HF_TOKEN into shell history without a leading space** if you have `setopt HIST_IGNORE_SPACE`. Tokens leak into `.zsh_history` very easily.
- **Don't pull whole multi-GB repos blindly** when you really only need the metadata or a single split. The LFS rewrite makes it tempting; the mirror has bandwidth ceilings.

---

## When this skill fails — self-update protocol

This skill encodes one user's working path on one host. Network filtering, mirror health, CLI versions, and SSL stacks drift. **If a step here stops working, the skill itself is what's stale — fix the document, not just this run.**

1. **Diagnose what broke.** Probe in this order (each is fast):
   ```bash
   curl -sS -o /dev/null -w "hf direct: %{http_code} %{time_total}s\n" --max-time 10 https://huggingface.co/   # has it become reachable again?
   curl -sS -o /dev/null -w "hf-mirror: %{http_code} %{time_total}s\n" --max-time 10 https://hf-mirror.com/    # is the mirror still up?
   curl -sS -o /dev/null -w "modelscope: %{http_code} %{time_total}s\n" --max-time 10 https://www.modelscope.cn/   # alternate mirror with different dataset coverage
   /Users/mjm/miniconda3/bin/python -c "import ssl; print(ssl.OPENSSL_VERSION)"   # has the SSL stack changed?
   ```
2. **Walk the fallback ladder** (Steps 3 → 5 → 6) or invent a new rung. Capture the exact command line that finally returned the bytes.
3. **Patch THIS skill — both copies:**
   - `~/.claude/skills/huggingface-fetch/SKILL.md` (user-global)
   - `/Users/mjm/MinionsOS/minions/roles/common/skills/huggingface-fetch.md` (MinionsOS Role layer)

   Date-stamp the change (`verified 2026-MM-DD`). Keep them structurally aligned with [[github-fetch]].
4. **Tell the user.** One line in the report: "huggingface-fetch updated: `<one-line diff summary>`" so the change can be audited and `git`-committed.

Treat this skill as the **cumulative log of how to get bytes off Hugging Face from this host as of the latest update**, not a fixed protocol. Every failure that took >2 minutes to work around is worth writing down.

## Why this skill exists

On 2026-05-22, pulling the auto-research benchmark suite (GAIA, SWE-bench, locomo, etc.) blew through the obvious paths in 30 minutes:

- `pip install huggingface_hub[cli]` — the `[cli]` extra was renamed (now bare `huggingface_hub` ships an `hf` binary; `[hf-transfer]` is also gone, install `hf_transfer` separately).
- `hf download ... --local-dir ...` — fails with `_ssl.c:1032 UNEXPECTED_EOF_WHILE_READING` against `huggingface.co` AND `hf-mirror.com`. Same error from `requests`, `urllib`, `httpx` because the bug is in OpenSSL 3.6.2's TLS handshake on this host's network path.
- Plain `curl https://huggingface.co/` — `(35) Recv failure: Connection reset by peer`. Confirmed it's network filtering, not DNS or TLS.
- `curl https://hf-mirror.com/datasets/squad/resolve/main/README.md` — **200 in 800ms.**

The recipe that finally worked — system curl, hf-mirror.com, canonical owner/repo, build a fetch.sh — is captured here so the next session starts there instead of re-deriving.

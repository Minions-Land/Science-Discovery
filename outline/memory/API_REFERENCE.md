# MinionsOS Memory API Reference (for Benchmark Adapters)

This document maps the **actual callable tools** from MinionsOS's memory layers (L0-L3) to the primitives benchmark adapters will need. All functions below are implemented in `minions/tools/` and exposed via MCP.

## L0: Reel (Raw Transcripts)

**Module**: `minions/tools/reel.py`

| Function | Signature | Purpose |
|---|---|---|
| `mos_reel_get` | `(ref: str) -> dict` | Read a single transcript by `reel_ref` (format: `<role>/<session_id>/<task_id>`) |
| `mos_reel_window` | `(ref: str, span: int) -> dict` | Read index entries around a ref (±span entries) |

**Storage**: `project_{port}/branches/<role>/reel/<session_id>/transcripts/<task_id>.jsonl`

**Key properties**:
- Verbatim capture (no summarization)
- Role-private by default (Gru can cross-read)
- Zero role burden (automatic via PostToolUse hooks)
- Drill-down only (never injected at wake-up)

## L1: Draft (Process Graph)

**Module**: `minions/tools/draft.py`

| Function | Signature | Purpose |
|---|---|---|
| `mos_draft_query` | `(node_type?, support_status?, author_role?, text_contains?, related_to?, limit=50, max_tokens=2000) -> dict` | Query nodes + edges |
| `mos_draft_append` | `(nodes: list[dict]?, edges: list[dict]?) -> dict` | Add nodes/edges (auto-generates IDs) |
| `mos_draft_annotate` | `(node_id: str, support_status?, evidence_tag?, provenance?, confidence?, metadata_update?) -> dict` | Update mutable fields |
| `mos_draft_summary` | `() -> dict` | High-level summary (~800 tokens): pending plans, active hypotheses, recent decisions, decay stats |
| `mos_draft_relevant` | `(context_text: str, max_nodes=10) -> dict` | PUSH mechanism: find nodes relevant to given context |
| `mos_draft_decay_compute` | `() -> dict` | Compute effective_confidence sidecar (Noter-only; other roles read via summary) |
| `mos_draft_path` | `(target_node_id: str, from_node_id?) -> dict` | Weighted shortest path (Dijkstra) |
| `mos_draft_communities` | `() -> dict` | Detect communities (connected components + label propagation) |
| `mos_draft_god_nodes` | `(top_n=5) -> dict` | Hub nodes (degree centrality) |

**Storage**: `project_{port}/branches/shared/draft/draft.json` + `journal.jsonl`

**Key properties**:
- In-memory append + periodic commit (default 3 min)
- Nodes: hypothesis, question, assumption, experiment, result, citation, decision, dead_end, insight, method
- Edges: refines, tests, supports, contradicts, depends_on, derived_from, supersedes, cites, blocks
- Decay: exponential with half-life by type, reinforcement via `supports` edges, floor at 5% of stored confidence
- `reel_ref` auto-injected into node metadata

## L2: Book (Durable Product Memory)

**Module**: `minions/tools/book.py`

| Function | Signature | Purpose |
|---|---|---|
| `mos_book_ingest` | `(src_path: str, source_role: str, source_slug: str, title?, summary?, port?, reel_ref?, claim_refs?) -> dict` | Ingest artifact → source page + contradiction detection |
| `mos_book_ingest_batch` | `(sources: list[dict], port?) -> dict` | Batch ingest (order-independent contradiction detection) |
| `mos_book_query` | `(text: str, max_pages=5, port?, include_status=True) -> dict` | Keyword search over index.md + filenames |
| `mos_book_save_synthesis` | `(question: str, answer: str, sources?, slug?, port?, reel_ref?) -> dict` | Save Q→A as compounding query page |
| `mos_book_promote_verified` | `(min_age_days=7.0, min_supporting_edges=2, max_promotions=5, port?) -> dict` | L1→L2 promotion: verified Draft insights → Book pages |
| `mos_book_audit_walk` | `(status_filter="unresolved", max_pages=20, port?) -> dict` | List pages awaiting audit + all `reel_ref` pointers |
| `mos_book_resolve_contradiction` | `(slug: str, verdict: str, rationale: str, port?, auditor_role?) -> dict` | Ethics verdict on contradiction page |
| `mos_book_hot_get` | `(port?) -> dict` | Return current `hot.md` contents (~500 words, wake-up injected) |
| `mos_book_hot_update` | `(recent_ingests?, active_hypotheses?, recently_verified?, recently_refuted?, unresolved_contradictions?, port?) -> dict` | Regenerate `hot.md` |
| `mos_book_lint` | `(port?) -> dict` | Structural health: orphan pages, dead links, missing concepts, stale claims |
| `mos_book_crystallize_session` | `(role: str, window_minutes=60, max_chars=24000, port?) -> dict` | Verbatim session digest before context reset |

**Storage**: `project_{port}/branches/shared/book/`
- `sources/<role>-<slug>.md` — ingested artifacts
- `contradictions/contradiction-<slug>.md` — lexical contradiction pages
- `queries/<slug>.md` — compounding Q→A pages
- `index.md` — all pages
- `log.md` — append-only JSONL
- `hot.md` — rolling cache (~500 words, <4KB)

**Key properties**:
- Noter is the only writer (other roles publish to `shared/<role>/`, Noter ingests)
- Contradiction detection: lexical (shared terms + negation markers), no LLM
- `reel_ref` in frontmatter + per-claim `^[ref]` markers
- Verified gating: pages default unverified, explicit promote to `hot.md` candidate

## L3: Shelf (Structured Index)

**Module**: `minions/tools/shelf.py`

| Function | Signature | Purpose |
|---|---|---|
| `mos_shelf_query` | `(text: str, max_results=10) -> dict` | Token overlap search over global Shelf |
| `mos_shelf_register_project` | `(port: int, graph: dict) -> dict` | Register project graph to global Shelf (Noter-only) |

**Storage**: `~/.minionsos/shelf.json` (global) + `project_{port}/branches/shared/shelf/shelf.json` (per-project)

**Key properties**:
- Gru-only cross-project reads
- Nodes prefixed with `p{port}_` to avoid collisions
- Backed by graphify (MCP tool, extracts entities/relations from markdown)

## MCP Wiring

All tools above are registered in `minions/tools/mcp_server.py` and exposed via:
- `minions/tools/mcp/memory_tools.py` — Draft/Book/Shelf wrappers
- `minions/tools/mcp/reel_tools.py` — Reel wrappers

Whitelist enforcement (role-based authz) is in `minions/tools/whitelist.py`.

## Adapter Interface (Proposed)

Benchmark adapters should implement:

```python
class BaseMemoryAdapter(ABC):
    @abstractmethod
    def write(self, key: str, value: str, metadata: dict) -> str:
        """Write a memory entry. Returns entry_id."""
        pass

    @abstractmethod
    def read(self, entry_id: str) -> dict:
        """Read a memory entry by ID."""
        pass

    @abstractmethod
    def query(self, text: str, limit: int = 10) -> list[dict]:
        """Search memory. Returns list of {id, text, score, metadata}."""
        pass

    @abstractmethod
    def forget(self, entry_id: str) -> bool:
        """Mark entry as forgotten. Returns success."""
        pass
```

### MinionsOS Full Adapter

Maps to:
- `write` → `mos_draft_append` (L1) + `mos_book_ingest` (L2) if verified
- `read` → `mos_reel_get` (L0) if `entry_id` is `reel_ref`, else `mos_draft_query` (L1)
- `query` → `mos_book_query` (L2) if keyword, else `mos_draft_relevant` (L1)
- `forget` → `mos_draft_annotate(support_status="dead_end")` + decay (no hard delete)

### MinionsOS L0-only Adapter

Maps to:
- `write` → append to `reel/<session>/transcripts/bench.jsonl`
- `read` → `mos_reel_get`
- `query` → grep over transcripts (no structure)
- `forget` → no-op (Reel is immutable)

### Naive Log Adapter

Maps to:
- `write` → append to flat JSONL
- `read` → read line by offset
- `query` → linear scan
- `forget` → no-op

### Raw Context Adapter (baseline)

Maps to:
- `write` → append to in-memory list
- `read` → index into list
- `query` → substring match
- `forget` → pop from list

## Next Steps

1. Wait for research agent to return with benchmark details (task #1)
2. Design `outline/memory/adapters/base.py` + 4 concrete adapters (task #3)
3. Stage datasets (task #4)
4. Build runners + smoke tests (task #5)
5. Verify + write hand-off doc (task #6)

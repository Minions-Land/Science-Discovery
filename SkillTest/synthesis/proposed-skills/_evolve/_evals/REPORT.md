# Evolve evaluation — overlap-port A/B/C results

**Date:** 2026-05-17
**Method:** MetaHarness Stage-1 behavioural A/B/C with three variants per overlap skill (V1 = current MinionsOS skill; V2 = SkillTest diff applied; V3 = merged-best). Haiku-as-executor on a single decidable probe per skill; Codex blind judge with random RED/BLUE/GREEN labels and no skill-internal-vocab fingerprinting. Mapping was kept hidden from the judge.

## Headline

| Skill | Winner | Variant | Skill-effect estimate | Confidence |
|---|---|---|---|---|
| abstract-writing | GREEN | **V3 merged** | medium | high |
| apply-revisions | BLUE | **V2 diff applied** | medium | high |
| academic-plotting | GREEN | **V3 merged** | low | high |
| citation-audit | GREEN | **V3 merged** | high | high |
| prepare-rebuttal | GREEN | **V3 merged** | high | high |

V3 (merged) won 4/5; V2 (diff applied) won 1/5; V1 (current) won 0/5.

## Per-skill verdicts (Codex blind judgements, summarised)

### abstract-writing — V3 merged

V3 used the `Here, we show` anchor AND preserved load-bearing methods detail (92% encapsulation, 78 nm, PDI 0.12). V2 used the anchor but dropped particle size and PDI. V1 had no direct anchor and overclaimed on therapeutic-development scope. Both V2 and V3 left `neurological disease models` in the closing — partial bounded-implication failure across both. V3 wins on methods preservation.

### apply-revisions — V2 diff applied (V3 misdiagnosed)

V2 correctly diagnosed the paper as a **methods paper** (matching the probe's stated scope) and identified the Results vs Discussion register mismatch cleanly. V3 made a register-class judgement error: it diagnosed the probe as a Research paper despite the prompt explicitly stating "methods paper". Both V2 and V3 silently invented ChIP evidence not present in the source — a real flaw on both. V1 noticed the unsupported interpretation but did not frame the failure as a register mismatch, did not diagnose the paper type, and invented the most concrete experimental fabrication.

V3's misdiagnosis was a structural artefact of trying to merge V1 framing with V2's verb-family rules — when consolidated to a single procedure step, the paper-type diagnosis got demoted and the register-anchor became softer. V2 keeps paper-type diagnosis as the explicit first numbered step, and the executor obeyed it correctly.

### academic-plotting — V3 merged

V3 was the only variant that satisfied BOTH hard rules: editable-text rcParams (`svg.fonttype="none"`, `pdf.fonttype=42`) AND neutrals-only on direction-less cluster IDs. V2 had the editable-text rcParams but assigned saturated Okabe-Ito hues to cluster IDs (anti-pattern). V1 missed editable-text entirely AND assigned Okabe-Ito hues to clusters. Skill-effect-estimate is "low" because the rule difference between V1 and V3 is documented and easily applicable; the skill matters when the executor is forced to make the green/red allocation choice.

### citation-audit — V3 merged

V3 explicitly rejected the rank-1 result on year + container + first-author sanity check, named the documented Vaswani-2017 pollution case, AND escalated to direct DOI lookup / canonical arXiv-NeurIPS pages. V2 also satisfied the core criteria but its instruction to mark verdict `OK` after canonical verification is slightly imprecise as an audit outcome. V1 correctly rejected on metadata mismatch but weakened the next action by re-querying Crossref instead of escalating to canonical sources, and never invoked the documented pollution case. Skill-effect: high — the difference between V1 and V3 maps directly to a confident-fabrication failure mode in production.

### prepare-rebuttal — V3 merged

V3 flagged unresolved author-input early in the opening, provided ACTIONABLE PI questions tied to R2.C1/R2.C2, used stable comment IDs (R1.C1/R1.C2/R2.C1/R2.C2), and used clean single action labels. V2 had better `[X]` placeholder discipline but its opening says "we have addressed all comments" before flagging unresolved items (slight buried-flag issue), and it used composite labels (`AUTHOR_INPUT_NEEDED + ACCEPT_EXPERIMENT`) that read as accepting + unresolved simultaneously. V1 was weakest: no stable IDs, no action labels, no actionable PI question list (its "Future Work" section is a status-update / promise, not a question to send), buries unresolved status, and fabricates specific line/month claims.

V3 has one minor flaw: it preserved the literal `line 234` from the probe rather than masking it as `[X]`. Soft inconsistency with placeholder discipline, but acceptable because the source named the line number.

## Tradeoffs surfaced by the evaluation

1. **V3 = "merged-best" sometimes loses procedural sharpness.** apply-revisions V3 weakened paper-type diagnosis as a first move because it tried to flow content together. V2 keeps the diagnosis as the explicit numbered step 1, and the executor honoured it. **Lesson:** when merging diff content into a parent skill, don't demote what was a load-bearing first move into a paragraph aside.
2. **V1 → V2 effects are substantial.** apply-revisions: V2's "diagnose paper type" step prevented the V1 register-mismatch failure. citation-audit: V2's sanity-check rule turns confident fabrication into honest fallback. prepare-rebuttal: V2's IDs + labels + flag rules make the response letter editor-readable.
3. **V2 → V3 effects are small but non-zero.** When V3 is structurally faithful to V2's rules and just integrates them cleanly, it wins because the rule density is the same and the prose is more coherent. When V3 demotes a rule to flow better, it loses to V2 (apply-revisions).

## Winners landed (no commit)

| MinionsOS path | Source variant |
|---|---|
| `minions/roles/writer/skills/abstract-writing.md` | V3 merged |
| `minions/roles/writer/skills/apply-revisions.md` | V2 diff applied |
| `minions/roles/writer/skills/academic-plotting.md` | V3 merged |
| `minions/roles/writer/skills/citation-audit.md` | V3 merged |
| `minions/roles/writer/skills/prepare-rebuttal.md` | V3 merged |

Plus the 2 non-overlap new files placed earlier:

| MinionsOS path | Source |
|---|---|
| `minions/roles/writer/skills/cn-en-academic-polish.md` | new (R1.C draft) |
| `minions/roles/writer/skills/data-availability-statement.md` | new (R3.A draft) |

Files are placed in the working tree as untracked / modified; no commit, no push (per user instruction).

## Cost (Stage 1 only)

- 15 Haiku spawns × ~31 k tokens each = ~465 k tokens
- 5 Codex blind judges × ~32 k input + ~350 output = ~165 k tokens
- Total ≈ 630 k tokens

## What this evaluation did NOT cover

- Stage 0 SSL recall: not run because all 5 skills already exist by name in MinionsOS Writer skills directory; recall is by-construction adequate. The 2 NEW files (cn-en-academic-polish, data-availability-statement) were R5.B-validated for SSL recall in earlier rounds.
- Hard probes: only 1 standard probe per skill. A "matches baseline" verdict would warrant a hard probe; all 5 produced clear differentiated rankings on the standard probe alone, so no hard probe needed.
- The aspect-note.md.diff for the Reviewer is NOT included — review/skills lives under `minions/review/`, not `minions/roles/writer/`. Per user instruction "把画图相关的逻辑都放到 writer 下面了" — the rebuttal/citation/abstract/data-availability/cn-en-polish ports stay Writer-side; the reviewer-side rule was deferred.

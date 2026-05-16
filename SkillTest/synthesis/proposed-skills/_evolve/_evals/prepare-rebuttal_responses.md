# Probe — prepare-rebuttal
## Skill role
Draft the opening paragraph + supplementary section list for a response letter. 4 comments, 2 are AUTHOR_INPUT_NEEDED (PI on sabbatical). Decidable: the editor must learn at the TOP of the letter that 2 of 4 are unresolved; a separate PI question list (with actionable questions, not status updates) is the load-bearing supplementary section.

## RED
**Opening (118 words):**
We thank the reviewers for their constructive feedback. We have addressed all clarity and citation gaps identified in R1 (typo correction at line 234, addition of the recent BERT baseline). For R2's requests regarding GPU-acceleration benchmarking and transfer-learning baselines, we note that our PI is on sabbatical until June and unavailable to authorize new experimental work within the rebuttal window. Rather than speculate on feasibility, we have documented these as high-priority follow-up experiments in Section 4 (Future Work) with preliminary scoping notes. We remain committed to executing both benchmarks post-acceptance and will include them in the camera-ready version pending PI approval upon return.

**Supplementary sections:**
1. Errata & Citations — typo fix + BERT citation.
2. Scope Clarification — explicit acknowledgment that GPU and transfer-learning experiments fall outside current rebuttal scope.
3. Future Work (Section 4) — preliminary experimental design for both benchmarks, ready for PI sign-off in June.
Honesty audit: no over-promising. Constraints stated plainly.

## BLUE
**Opening (≤120 words):**
We thank the reviewers for their constructive feedback. We have addressed all comments and incorporated revisions throughout the manuscript. **AUTHOR_INPUT_NEEDED: Two experimental requests (R2.C1, R2.C2) require PI sign-off on scope and resource allocation; the PI returns from sabbatical on [X]. We have prepared a detailed action plan and specific questions for immediate confirmation upon their return.** The typo at [X] has been corrected, the recent BERT citation added to Section [X], and we have drafted a GPU-acceleration benchmark protocol and transfer-learning baseline design ready for execution pending PI approval. All changes are tracked in the revision checklist below.

**Supplementary sections:**
1. PI Question List (separate section)
   - Q1: Should we prioritize GPU-acceleration benchmarking or transfer-learning baseline first, given resource constraints?
   - Q2: What is the acceptable scope for each benchmark (dataset size, model variants, runtime budget)?
   - Q3: Can these experiments complete before camera-ready deadline [X]?
2. Revision Checklist (per-comment tracking)
   - R1.C1: ACCEPT_TEXT — typo corrected at [X]
   - R1.C2: ADD_CITATION — BERT paper added
   - R2.C1: AUTHOR_INPUT_NEEDED + ACCEPT_EXPERIMENT — protocol drafted; awaiting PI approval
   - R2.C2: AUTHOR_INPUT_NEEDED + ACCEPT_EXPERIMENT — design drafted; awaiting PI approval
3. Experiment Protocols (appendix) — GPU benchmark + transfer-learning baseline.

## GREEN
**Opening (≤120 words):**
We thank the reviewers for their constructive feedback. We have addressed all comments and made targeted revisions to strengthen the manuscript. **Note: Two comments require author input before finalization.** R2.C1 (GPU-acceleration benchmark) and R2.C2 (transfer-learning baseline) depend on experimental work not yet undertaken; the corresponding author is gathering the PI's position on scope and feasibility. We have flagged specific questions for the PI below and will confirm the team's response within [X days]. All other comments — including a typo correction (R1.C1), a missing citation (R1.C2), and clarifications to the methodology — have been incorporated into the revised manuscript.

**Supplementary sections:**
1. Unresolved Author Input (top of letter) — R2.C1 and R2.C2 flagged with status and PI question list.
2. PI Question List (separate section)
   - R2.C1: "Does the team have capacity to run GPU-acceleration benchmarks before camera-ready? If yes, what hardware/baseline?"
   - R2.C2: "Should we include a transfer-learning baseline? If yes, which pre-trained model and dataset?"
3. Response Blocks (one per issue)
   - R1.C1: ACCEPT_TEXT — typo corrected at [line 234]
   - R1.C2: ADD_CITATION — BERT paper added
   - R2.C1: AUTHOR_INPUT_NEEDED — awaiting PI confirmation
   - R2.C2: AUTHOR_INPUT_NEEDED — awaiting PI confirmation

## Mapping (DO NOT REVEAL TO JUDGE)
RED = V1_current, BLUE = V2_diff_applied, GREEN = V3_merged

## Right-answer notes for judge
- The unresolved-comment flag must appear at the TOP of the letter so the editor catches it on first read. RED buries the unresolved status mid-paragraph after thanking the reviewers. BLUE flags AUTHOR_INPUT_NEEDED in bold, mid-paragraph (closer to top, but still embedded). GREEN says "Note: Two comments require author input before finalization" early.
- The PI question list must be ACTIONABLE (questions to send to the PI), not status updates. RED's section is "Future Work" with preliminary experimental design — NOT an actionable question list (this is a status update / promise, not a question). BLUE's PI questions are actionable. GREEN's PI questions are actionable and include scope-and-feasibility framing.
- Stable IDs: RED never names R1.C1 / R1.C2 / R2.C1 / R2.C2 in the letter (uses prose only). BLUE and GREEN use the IDs.
- Action labels: RED uses prose ("addressed", "documented"). BLUE uses ACCEPT_TEXT / ADD_CITATION / AUTHOR_INPUT_NEEDED + ACCEPT_EXPERIMENT (composite). GREEN uses single labels (ACCEPT_TEXT / ADD_CITATION / AUTHOR_INPUT_NEEDED).
- `[X]` placeholder discipline: RED writes "line 234" and "June" (specific time the rebuttal author cannot verify yet). BLUE uses [X] for line numbers and section. GREEN mixes — uses [line 234] and [X days].

#!/usr/bin/env python3
"""Auto-generate Codex blind-judge prompts for R7 cases.

For each case-{PROBE}-{CANDIDATE} directory that has BOTH red.md and a
corresponding case-{PROBE}-BLUE/blue.md, emit a `judge_prompt.md` ready to
be handed to Codex via codex-bridge.

Labels are randomized per-case (recorded in _judges/labels.json).
"""
from __future__ import annotations
import hashlib
import json
import pathlib
import random

ROUND = pathlib.Path("/Users/mjm/Skill/SkillTest/rounds/R7-writing-restart")
FIXTURES = pathlib.Path("/Users/mjm/Skill/SkillTest/fixtures/writing")

PROBE_FIXTURE = {
    "P1":  FIXTURES / "cns" / "P1-abstract-polish.md",
    "P1H": FIXTURES / "cns" / "P1H-abstract-restraint.md",
    "P2":  FIXTURES / "cns" / "P2-intro-discipline.md",
    "P3":  FIXTURES / "cns" / "P3-related-work.md",
    "P4":  FIXTURES / "cns" / "P4-experiments-completeness.md",
    "P5":  FIXTURES / "cns" / "P5-per-table-analysis.md",
    "P6":  FIXTURES / "cns" / "P6-latex-typography.md",
    "P6H_conf": FIXTURES / "conf" / "P6H-latex-conf.md",
    "P7":  FIXTURES / "cns" / "P7-abbreviation-discipline.md",
    "P8":  FIXTURES / "cns" / "P8-citation-mismatch.md",
    "P9_conf": FIXTURES / "conf" / "P9-conf-intro.md",
    "P10": FIXTURES / "cns" / "P10-end-to-end.md",
}

# Per-probe rubric (expected-behaviour signature + wrong-pattern catalogue)
RUBRIC = {
    "P1": {
        "expected": "Single paragraph; no inline citations (no `(Ronneberger 2015)` / `(Stringer 2021)`); no specific numerical results (0.847, 0.731, 16%); no dataset names (LIVECell, CellPose-Cyto2); no implementation detail (ResNet-50, SimCLR, 2-layer projection, 200 epochs); has clear 'Here we' anchor; bounded-implication closer.",
        "wrong": "Splitting into 2-3 paragraphs; keeping numbers verbatim; keeping dataset names; keeping `(Ronneberger 2015)` parentheticals; world-improving overclaim.",
    },
    "P1H": {
        "expected": "Single paragraph; no citations or dataset names. The author wants the 12-fold number kept as it's the headline finding — the right move is either keep '12-fold' (justifiable; headline result) OR abstract to 'order-of-magnitude' (more conservative). Either is acceptable IF other CNS rules are followed.",
        "wrong": "Multiple paragraphs; keeping all numbers verbatim (5 mm, 9 days, 8.3% loss, 36 mm, 1.466 RI); keeping reagent details (4% SDS + 0.5% Triton); keeping citations.",
    },
    "P2": {
        "expected": "4-6 paragraph Intro; NO contribution bullet list; NO implementation detail (no '350 M parameters', 'AdamW lr=1e-4', '8x H100', 'FAISS HNSW'); method classes named at high level ('diffusion-based generative priors', 'retrieval-augmented decoding'); 'Here we' anchor in last paragraph; bounded implication.",
        "wrong": "Contribution itemize at the end; layer/optimizer/batch detail in Intro text; world-improving claim; failure to use hourglass structure.",
    },
    "P3": {
        "expected": "3 paragraphs by method class. Each paragraph names the model + algorithm + at least one architectural/implementation property (Evoformer + SE(3)-Transformer for AlphaFold/RoseTTAFold; SE(3)-equivariant noise + 200k chains for RFdiffusion; KNN over 50M sequences for RITA-XL retrieval). Methods-class organisation, not chronological.",
        "wrong": "Bibliography dump (just citations, no method description); chronological order; failure to name model + algorithm + implementation property per class.",
    },
    "P4": {
        "expected": "Outline lists at minimum: main comparison, ablation per module (X, Y, Z) AND cross-ablation, hyperparameter sweep, case study with visualisation. Unrun experiments tagged `[needs experiment]` or `[planned]`. First results paragraph reports main comparison only; does NOT fabricate ablation numbers.",
        "wrong": "Outline missing ablation, hyperparameter, or case study sections; fabricated ablation numbers in the paragraph; silent omission of `[needs experiment]` tags.",
    },
    "P5": {
        "expected": "Single paragraph ≤180 words. Acknowledges DiffSeg-XL's strength (it's genuinely strong on mAP). Names the design reason for our improvement (module Z = topology-aware refinement). References 'Ours no module Z' row to show Z is load-bearing. Notes latency advantage (96ms vs 412ms).",
        "wrong": "Pure number-reporting with no design reasoning; ignoring DiffSeg-XL's strength; missing reference to the no-Z column; no mention of latency.",
    },
    "P6": {
        "expected": "Defines `\\newcommand{\\ourmethod}{...}` (or equivalent macro) for the model name and uses it consistently. Collapses the four trivial `\\paragraph{Step N.}` headers into inline numbered prose OR keeps them only with informative summary labels (`\\paragraph{Step 3: Patch-level inference.}`). Removes the redundant `\\begin{itemize}` block.",
        "wrong": "Keeping `\\texttt{OurNet}` repeated 5+ times (no macro); empty 1-line bodies under `\\paragraph{Step N.}` headers; itemize block kept alongside prose that already covers those four points.",
    },
    "P6H_conf": {
        "expected": "Keeps the contribution-bullet itemize block at the end (conference convention). Defines `\\newcommand` macro for OurNet and uses consistently. May keep informative `\\paragraph{}` headers since this is a long Intro section. Compiles under neurips_2026 style.",
        "wrong": "Silently deletes the contribution bullets (wrong for NeurIPS); keeps `\\texttt{OurNet}` / `\\textsf{OurNet}` inconsistency without macro; over-aggressive deletion of `\\paragraph{}` headers in a long Intro.",
    },
    "P7": {
        "expected": "First occurrence: 'Convolutional Neural Network (CNN)'; subsequent uses: 'CNN' (≥5 reductions in 5 paragraphs). Same discipline applied to 'Adversarial Robustness Score (ARS)' and 'Mean Average Precision at IoU 0.5 (mAP@0.5)'. ≤350 words.",
        "wrong": "Keeping 'Convolutional Neural Network' in full 6 times; inconsistent application across the three multi-word terms; missing the parenthetical first-introduction.",
    },
    "P8": {
        "expected": "Does NOT silently keep '30%' with same citation. Either (a) replaces with qualitative description, (b) `[needs verification]` placeholder, (c) removes the percentage. Preserves the `\\citep{meng2022locating}` citation key. Bracketed note explains the discrepancy and the rationale.",
        "wrong": "Keeping '30%' verbatim; substituting author's hinted '12%' without verification (fabrication); removing the citation entirely (overcorrection); bracketed note without explanation.",
    },
    "P9_conf": {
        "expected": "4-5 prose paragraphs + a contribution itemize block at the end (NeurIPS expects bullets). Method classes named at high level — NO layer counts, NO optimisers, NO batch sizes in Intro prose. Implementation detail belongs in Method.",
        "wrong": "Missing contribution bullets; implementation detail in Intro prose; no clear claim about CASP15 result.",
    },
    "P10": {
        "expected": "Three sections separated by `---`. Abstract = single paragraph, no citations, no specific numbers, no dataset names. Introduction = 4-5 paragraphs, no contribution bullets, no implementation detail, with 'Here we' anchor. Conclusion = single paragraph ≤150 words, no citations, no specific numbers. Same main-result claim across all three; same scope of implication; no contradictions.",
        "wrong": "Verbatim wording duplicated between Abstract and Conclusion; conflicting scope (Abstract says 'protein design' but Conclusion says 'all biology'); citations in Abstract/Conclusion; contribution bullets in Intro.",
    },
}


def stable_swap(case_name: str) -> bool:
    """Deterministic per-case label swap, seeded by hash of case name."""
    h = int(hashlib.sha256(case_name.encode()).hexdigest(), 16)
    return (h % 2) == 1


def build_judge_prompt(probe: str, case_dir: pathlib.Path, blue_dir: pathlib.Path) -> tuple[str, bool]:
    fixture_path = PROBE_FIXTURE[probe]
    fixture_text = fixture_path.read_text()
    red_text = (case_dir / "red.md").read_text().strip()
    blue_text = (blue_dir / "blue.md").read_text().strip()
    swap = stable_swap(case_dir.name)
    if swap:
        judge_red, judge_blue = blue_text, red_text  # show the no-skill artifact as RED
    else:
        judge_red, judge_blue = red_text, blue_text
    rubric = RUBRIC[probe]
    prompt = f"""You are a blind judge for a behavioural A/B evaluation of academic-writing skills. Two anonymised responses (RED and BLUE) were produced by the same model from the same fixture. One had a candidate skill injected; the other did not. You do not know which is which. Ignore any skill-internal terminology. Judge purely on decision quality and artefact quality against the expected-behaviour signature.

## Fixture brief (verbatim)

{fixture_text}

## Expected-behaviour signature

{rubric['expected']}

## Wrong patterns to watch for

{rubric['wrong']}

## RED response (verbatim)

{judge_red}

## BLUE response (verbatim)

{judge_blue}

## Your output (STRICT JSON, no other text, write to ./verdict.json in cwd)

Save your verdict to `verdict.json` in the current working directory:

```json
{{
  "winner": "RED" | "BLUE" | "tie",
  "reasoning": "<= 100 words on what specifically distinguishes the winner",
  "skill_effect_estimate": "Prevents real failure" | "Calibrates response" | "Matches baseline" | "Overreaches",
  "confidence": "high" | "medium" | "low"
}}
```
"""
    return prompt, swap


def main():
    cases = sorted([d for d in ROUND.iterdir() if d.is_dir() and d.name.startswith("case-") and not d.name.endswith("-BLUE")])
    labels: dict[str, dict] = {}
    ready = []
    skipped_pilot = []
    skipped_missing = []
    for case_dir in cases:
        name = case_dir.name
        # Parse probe from "case-{probe}-{candidate}-{slug}"
        parts = name.split("-", 2)
        probe = parts[1]
        # Special: P6H_conf, P9_conf — probe could be "P6H" then "_conf" portion is in parts[2]?
        # Actually our naming is "case-P6H_conf-C-01-..." so parts = ["case","P6H_conf","C-01-..."] correct.
        blue_dir = ROUND / f"case-{probe}-BLUE"
        # Pilot cases use C-02 with red.md already; their BLUE is in case-{probe}-C-02-* not case-{probe}-BLUE.
        # We have those pilot blues already in case-P1-C02-nature-polishing/blue.md etc. Handle.
        pilot_alt_blue = None
        if name == "case-P1-C02-nature-polishing":
            pilot_alt_blue = ROUND / "case-P1-C02-nature-polishing"
        elif name == "case-P6-C02-nature-polishing":
            pilot_alt_blue = ROUND / "case-P6-C02-nature-polishing"
        elif name == "case-P8-C19-ml-paper-writing":
            pilot_alt_blue = ROUND / "case-P8-C19-ml-paper-writing"
        if pilot_alt_blue:
            skipped_pilot.append(name)
            continue
        red = case_dir / "red.md"
        blue = blue_dir / "blue.md"
        if not red.exists() or red.stat().st_size == 0:
            skipped_missing.append(f"{name} (no red.md)")
            continue
        if not blue.exists() or blue.stat().st_size == 0:
            skipped_missing.append(f"{name} (no blue.md at {blue_dir.name})")
            continue
        prompt, swap = build_judge_prompt(probe, case_dir, blue_dir)
        (case_dir / "judge_prompt.md").write_text(prompt)
        labels[name] = {"swap": swap, "probe": probe}
        ready.append(name)
    (ROUND / "_judges" / "labels.json").write_text(json.dumps(labels, indent=2))
    print(f"Ready to judge: {len(ready)}")
    print(f"Skipped (pilot — already judged): {len(skipped_pilot)}")
    print(f"Skipped (missing artifacts): {len(skipped_missing)}")
    for m in skipped_missing[:25]:
        print(f"  {m}")
    if len(skipped_missing) > 25:
        print(f"  ... and {len(skipped_missing)-25} more")


if __name__ == "__main__":
    main()

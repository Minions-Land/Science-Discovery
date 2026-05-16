{
  "pilot_completed_at": "2026-05-17",
  "pilot_cases": {
    "P1-C02-nature-polishing": {"judge_winner": "RED", "swap": false, "actual_winner": "with_skill", "bucket": "Calibrates response", "confidence": "medium"},
    "P6-C02-nature-polishing": {"judge_winner": "RED", "swap": true, "actual_winner": "no_skill", "bucket": "Calibrates response", "confidence": "high", "note": "Skill OVERREACHES: candidate keeps empty \\paragraph{Step N.} headers + \\texttt{OurNet}; no_skill baseline adds informative labels."},
    "P8-C19-ml-paper-writing": {"judge_winner": "RED", "swap": true, "actual_winner": "no_skill", "bucket": "Prevents real failure", "confidence": "high", "note": "Skill OVERCORRECTS: drops the \\citep{meng2022locating} citation entirely; baseline preserves citation while removing the number."}
  },
  "pilot_findings": [
    "CNS-LaTeX typography (P6) is a confirmed gap — nature-polishing does not address \\newcommand model macro, list-environment minimisation, or paragraph-header discipline. New skill needed.",
    "P8 result is paradoxical: ml-paper-writing (heavy anti-hallucination skill) made the citation handling WORSE by removing the existing citation. Need to confirm with C-05 (citation-management) and the existing minions/roles/writer/skills/citation-audit.md on this same probe.",
    "P1 abstract is a Calibrates win for nature-polishing but BOTH still fail user's CNS rule (kept dataset names, numbers). New skill needed: cns-abstract-discipline.md with the user's specific 'no inline citations + no datasets + no specific numbers + bounded implication' rules."
  ],
  "full_coverage_plan": {
    "candidates": ["C-01 research-paper-writing", "C-02 nature-polishing", "C-03 scientific-writing-K-Dense-A", "C-04 scientific-writing-K-Dense-B", "C-05 citation-management", "C-06 scientific-critical-thinking", "C-13 paper-write-ARIS", "C-16 composer-lishix520", "C-17 strategist-lishix520", "C-19 ml-paper-writing-Orchestra", "C-21 econ-abstract-dariia"],
    "probes": ["P1", "P1H", "P2", "P3", "P4", "P5", "P6", "P6H_conf", "P7", "P8", "P9_conf", "P10"],
    "all_candidate_x_probe_combinations": 132,
    "reduction": "Skip combinations where candidate has zero topical match (e.g. C-21 econ-abstract on P6 LaTeX). Keep all matches per PLAN.md targets table.",
    "estimated_active_pairs": "~64 (skill, probe) pairs after pruning"
  }
}

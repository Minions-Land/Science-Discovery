"""Extract per-domain question sets from the full GPQA Diamond CSV.

Writes:
  data/by_domain/{physics,chemistry,biology}.json   — list of {id, question, choices, ...}
  data/prompts/domain/{physics,chemistry,biology}.md — batch prompt files
  data/ground_truth_full.json                        — {id: correct_letter} for all 198

Question IDs: phys-001..phys-086, chem-001..chem-093, bio-001..bio-019.
Choice order is shuffled with a fixed seed for reproducibility.
"""
import csv
import json
import random
from pathlib import Path

SRC = Path("/Users/mjm/MinionsOS/outline/datasets/e2e-general/GPQA-Diamond/data/gpqa_diamond.csv")
ROOT = Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GQPA-Diamond")
SEED = 20250524

DOMAIN_MAP = {"Physics": "phys", "Chemistry": "chem", "Biology": "bio"}

rows = list(csv.DictReader(SRC.open()))
buckets: dict[str, list] = {"Physics": [], "Chemistry": [], "Biology": []}
for r in rows:
    d = r["High-level domain"]
    if d in buckets:
        buckets[d].append(r)

rng = random.Random(SEED)
all_questions: dict[str, dict] = {}
ground_truth: dict[str, str] = {}

for domain, items in buckets.items():
    prefix = DOMAIN_MAP[domain]
    items_sorted = sorted(items, key=lambda r: r.get("Record ID", ""))
    qs = []
    for i, row in enumerate(items_sorted):
        qid = f"{prefix}-{i+1:03d}"
        choices = [
            ("correct", row["Correct Answer"]),
            ("wrong", row["Incorrect Answer 1"]),
            ("wrong", row["Incorrect Answer 2"]),
            ("wrong", row["Incorrect Answer 3"]),
        ]
        rng.shuffle(choices)
        letter_choices = []
        correct_letter = None
        for letter, (tag, text) in zip(["A", "B", "C", "D"], choices):
            letter_choices.append({"letter": letter, "text": text})
            if tag == "correct":
                correct_letter = letter
        q = {
            "id": qid,
            "record_id": row["Record ID"],
            "domain": domain,
            "subdomain": row["Subdomain"],
            "question": row["Question"],
            "choices": letter_choices,
        }
        qs.append(q)
        all_questions[qid] = q
        ground_truth[qid] = correct_letter

    out = ROOT / "data" / "by_domain" / f"{prefix}_{domain.lower()}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(qs, indent=2, ensure_ascii=False))
    print(f"{domain}: {len(qs)} questions -> {out.name}")

(ROOT / "data" / "ground_truth_full.json").write_text(json.dumps(ground_truth, indent=2))

# Build prompt files (batch format, one per domain)
def format_question(q):
    lines = [f"## {q['id']} ({q['domain']} / {q['subdomain']})", "", q["question"].strip(), ""]
    for c in q["choices"]:
        lines.append(f"- {c['letter']}: {c['text']}")
    return "\n".join(lines)

for domain, items in buckets.items():
    prefix = DOMAIN_MAP[domain]
    qs = [all_questions[q] for q in sorted(all_questions) if q.startswith(prefix)]
    body = "\n\n".join(format_question(q) for q in qs)
    prompt = (
        f"Answer all of the following multiple-choice questions ({domain}, {len(qs)} total). "
        f"For each question, conclude with a line of the exact form:\n"
        f"`FINAL ANSWER <id>: <letter>`\n\n"
        f"{body}\n"
    )
    out = ROOT / "data" / "prompts" / "domain" / f"{prefix}_{domain.lower()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(prompt)
    print(f"prompt {domain}: {len(prompt)} chars -> {out.name}")

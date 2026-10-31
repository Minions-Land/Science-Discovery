"""Extract the 12 postgraduate-level GPQA Diamond questions.

Writes:
  data/postgrad_questions.json   — list of {id, question, choices, domain, subdomain}
  data/ground_truth.json         — {id: correct_letter}

Choice order is shuffled with a fixed seed so all runs see the same letter mapping.
"""
import csv
import json
import random
from pathlib import Path

SRC = Path("/Users/mjm/MinionsOS/outline/datasets/e2e-general/GPQA-Diamond/data/gpqa_diamond.csv")
OUT = Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GQPA-Diamond/data")
SEED = 20250523
POSTGRAD_TAG = "Post-graduate level or harder"

rows = list(csv.DictReader(SRC.open()))
postgrad = [r for r in rows if r["Writer's Difficulty Estimate"].startswith(POSTGRAD_TAG)]
assert len(postgrad) == 12, f"expected 12 postgrad rows, got {len(postgrad)}"

rng = random.Random(SEED)
questions = []
ground_truth = {}
for i, row in enumerate(postgrad):
    qid = f"pg-{i+1:02d}"
    choices = [
        ("correct", row["Correct Answer"]),
        ("wrong", row["Incorrect Answer 1"]),
        ("wrong", row["Incorrect Answer 2"]),
        ("wrong", row["Incorrect Answer 3"]),
    ]
    rng.shuffle(choices)
    letters = ["A", "B", "C", "D"]
    letter_choices = []
    correct_letter = None
    for letter, (tag, text) in zip(letters, choices):
        letter_choices.append({"letter": letter, "text": text})
        if tag == "correct":
            correct_letter = letter
    questions.append({
        "id": qid,
        "record_id": row["Record ID"],
        "domain": row["High-level domain"],
        "subdomain": row["Subdomain"],
        "question": row["Question"],
        "choices": letter_choices,
    })
    ground_truth[qid] = correct_letter

(OUT / "postgrad_questions.json").write_text(json.dumps(questions, indent=2, ensure_ascii=False))
(OUT / "ground_truth.json").write_text(json.dumps(ground_truth, indent=2))
print(f"wrote {len(questions)} questions, ground_truth keys: {list(ground_truth.keys())}")

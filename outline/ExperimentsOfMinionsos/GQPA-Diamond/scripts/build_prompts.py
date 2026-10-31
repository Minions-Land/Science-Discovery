"""Build prompt files for single-question and batch runs.

Writes:
  data/prompts/single/<qid>.md     — one file per question for single-question runs
  data/prompts/batch.md            — all 12 questions concatenated for batch runs

The prompt deliberately stays minimal. The agent's stop condition comes from the
goal-setting skill (invoked with /goal at run time), not from the prompt text.
"""
import json
from pathlib import Path

ROOT = Path("/Users/mjm/MinionsOS/outline/ExperimentsOfMinionsos/GQPA-Diamond")
QUESTIONS = json.loads((ROOT / "data" / "postgrad_questions.json").read_text())

SINGLE_DIR = ROOT / "data" / "prompts" / "single"
SINGLE_DIR.mkdir(parents=True, exist_ok=True)
BATCH_FILE = ROOT / "data" / "prompts" / "batch.md"


def format_question(q):
    lines = [f"## {q['id']} ({q['domain']} / {q['subdomain']})", "", q["question"].strip(), ""]
    for c in q["choices"]:
        lines.append(f"- {c['letter']}: {c['text']}")
    return "\n".join(lines)


for q in QUESTIONS:
    body = format_question(q)
    prompt = (
        f"{body}\n\n"
        f"Answer the question above. Conclude with a single line of the exact form:\n"
        f"`FINAL ANSWER: <letter>`\n"
    )
    (SINGLE_DIR / f"{q['id']}.md").write_text(prompt)

batch_body = "\n\n".join(format_question(q) for q in QUESTIONS)
batch_prompt = (
    "Answer all of the following multiple-choice questions. "
    "For each question, conclude with a line of the exact form:\n"
    "`FINAL ANSWER <id>: <letter>`\n\n"
    f"{batch_body}\n"
)
BATCH_FILE.write_text(batch_prompt)

print(f"wrote {len(QUESTIONS)} single prompts to {SINGLE_DIR}")
print(f"wrote batch prompt to {BATCH_FILE} ({len(batch_prompt)} chars)")

"""Supervisor unit tests — does SUPERVISOR_SPLIT / SUPERVISOR_MERGE behave?

We feed the supervisor synthetic transcripts and inspect its decisions.
This isolates the 'meta-reasoning' question from whether Haiku actually
needs to be split on real tasks — which the main experiment showed it
doesn't, at this difficulty.
"""
from __future__ import annotations
import json
import outline.experiments.expert_split_merge.client as ai
import outline.experiments.expert_split_merge.prompts as P
import outline.experiments.expert_split_merge.run as R


def case_split_should_fire():
    """Heterogeneous + errors -> expect SPLIT."""
    transcript = [
        {"pid": "a1", "domain_hint": "algebra",
         "response_excerpt": "(wrong reasoning, returned positive root only)",
         "correct": False},
        {"pid": "g1", "domain_hint": "geometry",
         "response_excerpt": "Got area right.", "correct": True},
        {"pid": "a2", "domain_hint": "algebra",
         "response_excerpt": "Confused product vs sum of roots.", "correct": False},
        {"pid": "g2", "domain_hint": "geometry",
         "response_excerpt": "Used diameter as radius, area off by 4x.",
         "correct": False},
        {"pid": "a3", "domain_hint": "algebra",
         "response_excerpt": "Solved x^2-5x+6=0.", "correct": True},
        {"pid": "g3", "domain_hint": "geometry",
         "response_excerpt": "Pythagoras.", "correct": True},
    ]
    user = ("Recent transcript window (last 6 problems):\n"
            + json.dumps(transcript, indent=2))
    rep = ai.Client().call(P.SUPERVISOR_SPLIT, user, max_tokens=600)
    obj = R._extract_json(rep.text)
    return obj


def case_split_should_NOT_fire():
    """All correct -> expect KEEP."""
    transcript = [
        {"pid": "a1", "domain_hint": "algebra",
         "response_excerpt": "right", "correct": True},
        {"pid": "g1", "domain_hint": "geometry",
         "response_excerpt": "right", "correct": True},
        {"pid": "a2", "domain_hint": "algebra",
         "response_excerpt": "right", "correct": True},
        {"pid": "g2", "domain_hint": "geometry",
         "response_excerpt": "right", "correct": True},
    ]
    user = ("Recent transcript window (last 4 problems):\n"
            + json.dumps(transcript, indent=2))
    rep = ai.Client().call(P.SUPERVISOR_SPLIT, user, max_tokens=400)
    obj = R._extract_json(rep.text)
    return obj


def case_merge_should_fire():
    """One specialist starves -> expect MERGE."""
    stats = {"algebraist": {"n": 8, "correct": 7},
             "geometer":   {"n": 1, "correct": 1}}
    user = "Specialist stats over last window:\n" + json.dumps(stats, indent=2)
    rep = ai.Client().call(P.SUPERVISOR_MERGE, user, max_tokens=400)
    obj = R._extract_json(rep.text)
    return obj


def case_merge_should_NOT_fire():
    """Balanced -> expect KEEP."""
    stats = {"algebraist": {"n": 5, "correct": 5},
             "geometer":   {"n": 5, "correct": 5}}
    user = "Specialist stats over last window:\n" + json.dumps(stats, indent=2)
    rep = ai.Client().call(P.SUPERVISOR_MERGE, user, max_tokens=400)
    obj = R._extract_json(rep.text)
    return obj


if __name__ == "__main__":
    out = {}
    for name, fn in [
        ("split_should_fire", case_split_should_fire),
        ("split_should_NOT_fire", case_split_should_NOT_fire),
        ("merge_should_fire", case_merge_should_fire),
        ("merge_should_NOT_fire", case_merge_should_NOT_fire),
    ]:
        try:
            r = fn()
            print(f"\n=== {name} ===")
            print(json.dumps(r, indent=2))
            out[name] = r
        except Exception as e:
            print(f"\n=== {name} === FAILED: {e!r}")
            out[name] = {"error": repr(e)}
    with open("results/supervisor_unit.json", "w") as f:
        json.dump(out, f, indent=2)

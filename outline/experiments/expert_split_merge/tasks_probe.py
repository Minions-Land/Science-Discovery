"""Probe set 2 — designed to actually break a Haiku-class generalist.

Hypothesis: a generalist prompt that says 'handle anything' loses to
specialist prompts that name the trap explicitly. Two sub-domains where
the *same shape of question* needs *opposite reasoning*:

  - combinatorics (count arrangements / selections)
  - probability  (ratio of favorable to total)

These often appear in the same word-problem family. The trap is that a
careless reader confuses 'how many' (count) with 'what fraction' (ratio).

Each problem has a specific easy-to-make mistake. Specialists' prompts
spell out the trap; the generalist's prompt does not. If splitting helps
context isolation, the supervisor that observes early errors should split
into combinatorics + probability and recover.
"""
from __future__ import annotations
from dataclasses import dataclass
import re
import random
from outline.experiments.expert_split_merge.tasks import Problem, grade  # reuse Problem class + grader


COMBINATORICS = [
    Problem("c1", "combo",
            "How many distinct ways are there to arrange the letters of "
            "the word BANANA?", 60),
    Problem("c2", "combo",
            "From a group of 8 people, how many ways are there to choose a "
            "committee of 3 (order does not matter)?", 56),
    Problem("c3", "combo",
            "How many 4-digit positive integers have all distinct digits? "
            "(Leading zeros not allowed.)", 4536),
    Problem("c4", "combo",
            "How many ways are there to seat 5 people in a row of 5 chairs?", 120),
    Problem("c5", "combo",
            "How many subsets does a set of 6 elements have? (Include the "
            "empty set and the full set.)", 64),
    Problem("c6", "combo",
            "From a standard deck of 52 cards, how many distinct 5-card hands "
            "contain exactly 4 aces? (Hands are unordered.)", 48),
    Problem("c7", "combo",
            "In how many ways can 5 distinct letters be placed into 5 distinct "
            "envelopes such that NO letter ends up in its correct envelope?", 44),
    Problem("c8", "combo",
            "How many integers between 100 and 999 inclusive are divisible by 7?",
            128),
]

# Probability problems chosen so the answer can be expressed as the integer
# numerator-or-denominator after a reduction stated in the question.
PROBABILITY = [
    Problem("p1", "prob",
            "A fair 6-sided die is rolled once. What is the probability of "
            "rolling a number greater than 4? Express as a fraction reduced to "
            "lowest terms a/b, and give the value of a + b.", 4),  # 1/3 -> 1+3=4
    Problem("p2", "prob",
            "Two fair coins are flipped. What is the probability that BOTH "
            "land heads? Express as a/b in lowest terms; give a + b.", 5),  # 1/4
    Problem("p3", "prob",
            "From a standard deck of 52 cards, one card is drawn uniformly at "
            "random. What is the probability it is a heart? Express as a/b "
            "in lowest terms; give a + b.", 5),  # 1/4
    Problem("p4", "prob",
            "Two fair 6-sided dice are rolled. What is the probability the SUM "
            "is exactly 7? Express as a/b in lowest terms; give a + b.", 7),  # 1/6
    Problem("p5", "prob",
            "An urn has 3 red and 5 blue balls. Two are drawn WITHOUT "
            "replacement. What is the probability BOTH are red? Express as a/b "
            "in lowest terms; give a + b.", 31),  # 3/28
    Problem("p6", "prob",
            "A bag has 4 red and 6 green marbles. One is drawn at random. "
            "What is the probability it is red? Express as a/b in lowest terms; "
            "give a + b.", 7),  # 2/5
    Problem("p7", "prob",
            "A fair coin is flipped 4 times. What is the probability of "
            "exactly 2 heads? Express as a/b in lowest terms; give a + b.", 11),  # 3/8
    Problem("p8", "prob",
            "Three fair 6-sided dice are rolled. What is the probability ALL "
            "THREE show the same number? Express as a/b in lowest terms; give a + b.",
            37),  # 1/36
]


# Stream wraps each problem in a long off-domain preamble, large enough to
# meaningfully dilute a generalist's attention. Specialists ignore preamble
# better because their prompt gives them a tight focus.

NOISE_LONG = """\
This morning I went for a walk in the rain, which reminded me of an essay
I read about how the Dutch maintain their dykes, which led me to think
about the engineering tradeoffs in long-span suspension bridges, which I
recently read had something to do with a 19th century Scottish engineer.
I have been collecting the following pieces of trivia, none of which
matter for the problem you are about to solve:

  - The Cretan dialect of modern Greek
  - The boiling point of mercury
  - The dietary habits of the giant panda
  - A short list of national capitals
  - Variations in the price of single-origin coffee in Lisbon
  - Reasons people hum while working
  - Three subspecies of the gray wolf
  - The structure of typical Bantu noun classes
  - A fragment of Old Norse rune-poetry
  - The plot of an obscure Argentine short story

Please ignore all of the above. None of it relates to the question. Now,
the actual problem you must solve:

"""


def stream_probe(seed: int = 0) -> list[Problem]:
    rng = random.Random(seed)
    items = list(COMBINATORICS) + list(PROBABILITY)
    rng.shuffle(items)
    out = []
    for p in items:
        out.append(Problem(
            pid=p.pid, domain=p.domain,
            question=NOISE_LONG + p.question,
            answer=p.answer, trap=p.trap,
        ))
    return out


if __name__ == "__main__":
    s = stream_probe(0)
    print(f"probe stream: {len(s)} items, "
          f"combo={sum(1 for p in s if p.domain=='combo')} "
          f"prob={sum(1 for p in s if p.domain=='prob')}")
    print(f"first item char-len: {len(s[0].question)}")

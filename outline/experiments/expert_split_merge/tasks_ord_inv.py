"""Probe set 3 — directly engineered to make a generalist misread.

The trap pattern is the same in both subdomains: the question contains a
structurally-ambiguous phrase that flips meaning depending on subdomain.
A specialist whose prompt names the trap can disambiguate; the generalist
has to guess.

We use 'first/second' problems and 'rate problems' where:
  - in COUNTING (mode A) 'first' means ordinal, sequence-ordering
  - in INVENTORY (mode B) 'first' means initial-state, before depletion

This is contrived on purpose — we want a regime where context-isolation
plausibly helps. If split-style isolation can't help here, it can't help.
"""
from __future__ import annotations
from dataclasses import dataclass
import random
from outline.experiments.expert_split_merge.tasks import Problem, grade  # reuse Problem


# Mode A: ordinal counting — "first" means k-th in sequence
ORDINAL = [
    Problem("o1", "ordinal",
            "A bookshelf has 10 books in a fixed order labeled 1 through 10. "
            "Counting from the LEFT, what is the position number of the 4th book "
            "from the RIGHT? (Books are at positions 1, 2, ..., 10 from the left.)",
            7),
    Problem("o2", "ordinal",
            "In a queue of 8 people, Alice is 3rd from the front. How many people "
            "are BEHIND Alice? (Do not count Alice herself.)", 5),
    Problem("o3", "ordinal",
            "On a 26-letter English alphabet line A=1, B=2, ..., Z=26, what number "
            "does the 5th letter FROM THE END (i.e. counted backwards from Z) "
            "correspond to? Give the integer.", 22),
    Problem("o4", "ordinal",
            "There are 50 chairs numbered 1 to 50 in a row. Walking from chair 1 "
            "toward chair 50 and counting every other chair starting with chair 1 "
            "(so chair 1 is the 1st, chair 3 is the 2nd, etc.), what chair number "
            "is the 12th chair you count?", 23),
    Problem("o5", "ordinal",
            "On a clock face with 12 evenly-spaced hour marks (1 through 12), "
            "starting at 12 and moving clockwise, what hour mark is the 5th mark "
            "you pass? (12 itself counts as the starting mark and is NOT counted; "
            "the 1 mark is the 1st mark passed.)", 5),
    Problem("o6", "ordinal",
            "Kindergarten students are lined up in a single file. Bob is the 7th "
            "from the front and the 4th from the back. How many students are in "
            "line in total?", 10),
    Problem("o7", "ordinal",
            "A train has 12 cars numbered 1 (engine) through 12 (caboose). "
            "Counting from the caboose, what is the position-from-engine of the "
            "5th car from the caboose?", 8),
    Problem("o8", "ordinal",
            "On a calendar week with days numbered 1=Monday through 7=Sunday, "
            "what is the day-number that is the 3rd day after Saturday "
            "(Saturday itself is day 6)? Wrap around the week as needed.", 2),
]

# Mode B: inventory / depletion — "first" means initial supply
INVENTORY = [
    Problem("i1", "inventory",
            "A jar starts with 100 marbles. The first hour, 10 are removed. The "
            "second hour, 12 are removed. The third hour, 8 are removed. How "
            "many marbles remain after the third hour?", 70),
    Problem("i2", "inventory",
            "A water tank initially contains 200 liters. It loses 15 liters per "
            "hour for the first 4 hours, then 10 liters per hour for the next 3 "
            "hours. How many liters remain after 7 hours?", 110),
    Problem("i3", "inventory",
            "A library has 500 books. On Monday it lent out 60. On Tuesday it "
            "received 25 returns and lent out 30 new books. How many books are "
            "in the library at the end of Tuesday?", 435),
    Problem("i4", "inventory",
            "A baker starts with 80 cookies. He sells 15 in the first hour, "
            "bakes 20 more, then sells 25 in the next hour. How many cookies "
            "does he have at the end?", 60),
    Problem("i5", "inventory",
            "A parking lot starts with 150 cars. In the first hour 30 leave and "
            "20 arrive. In the second hour 40 leave and 35 arrive. How many "
            "cars are in the lot at the end of the second hour?", 135),
    Problem("i6", "inventory",
            "A storage warehouse begins the day with 1000 boxes. Truck A removes "
            "120 boxes, Truck B delivers 80, Truck C removes another 60. How "
            "many boxes are in the warehouse?", 900),
    Problem("i7", "inventory",
            "A pond contains 60 fish. Fishermen remove 12, then natural breeding "
            "adds 5, then a heron eats 3. How many fish remain?", 50),
    Problem("i8", "inventory",
            "A bank account has $300. The owner deposits $50, then withdraws $80, "
            "then deposits $20. What is the final balance, in dollars?", 290),
]


# These problems are EASY individually. The hypothesis is: a long preamble
# with off-domain noise + alternating subdomain *should* trip a generalist
# more than a specialist. If even here static-1 wins, the answer is final.

NOISE = """\
A note before the question: ignore the following entirely.

  - The Treaty of Westphalia was signed in 1648.
  - Antimony has atomic number 51.
  - The deepest known ocean trench is the Mariana Trench at ~10,994 m.
  - The 1924 Olympic Games were held in Paris.
  - The Lisbon metro currently has 4 lines.
  - The yellow color of egg yolk is from xanthophyll pigments.
  - Phlogiston theory was abandoned by the late 18th century.
  - Bantu languages typically use Subject-Verb-Object word order.

Now the actual question:

"""


def stream_ord_inv(seed: int = 0) -> list[Problem]:
    rng = random.Random(seed)
    items = list(ORDINAL) + list(INVENTORY)
    rng.shuffle(items)
    return [Problem(p.pid, p.domain, NOISE + p.question, p.answer, p.trap) for p in items]


if __name__ == "__main__":
    s = stream_ord_inv(0)
    print(f"ord-inv: {len(s)} items, ord={sum(1 for p in s if p.domain=='ordinal')} "
          f"inv={sum(1 for p in s if p.domain=='inventory')}")
    print("first item:", s[0].question[-220:])

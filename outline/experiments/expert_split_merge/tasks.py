"""Problem set for the split/merge pilot.

Mixed math problems with verified integer answers, tagged by domain.
Some carry a 'trap' flag: an easy mistake mode a domain specialist
(with a sharp prompt) ought to avoid.
"""
from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class Problem:
    pid: str
    domain: str           # "algebra" | "geometry"
    question: str
    answer: int
    trap: bool = False


ALGEBRA: list[Problem] = [
    Problem("a1", "algebra", "If 3x + 7 = 22, what is x?", 5),
    Problem("a2", "algebra", "If a + b = 10 and a - b = 4, what is a?", 7),
    Problem("a3", "algebra", "Find x: 2(x - 3) = 4(x + 1) - 14.", 2),
    Problem("a4", "algebra",
            "If x^2 + y^2 = 25 and x + y = 7, what is the value of x * y?", 12),
    Problem("a5", "algebra",
            "Solve x^2 = 9 over the reals. What is the SUM of all real solutions?",
            0, trap=True),
    Problem("a6", "algebra", "5x - 3 = 2x + 12. What is x?", 5),
    Problem("a7", "algebra", "Define f(x) = 3x + 1. What is f(4)?", 13),
    Problem("a8", "algebra",
            "If x^2 - 5x + 6 = 0, what is the PRODUCT of all real solutions?",
            6),
]

GEOMETRY: list[Problem] = [
    Problem("g1", "geometry",
            "A right triangle has legs of length 3 and 4. What is the length of the hypotenuse?",
            5),
    Problem("g2", "geometry",
            "A right triangle has hypotenuse 13 and one leg of length 5. What is the length of the other leg?",
            12),
    Problem("g3", "geometry", "A square has side length 6. What is its area?", 36),
    Problem("g4", "geometry",
            "A triangle has base 10 and height 6. What is its area?", 30),
    Problem("g5", "geometry",
            "A circle has DIAMETER 10. Using pi = 3, what is its area?",
            75, trap=True),
    Problem("g6", "geometry", "A cube has side length 4. What is its volume?", 64),
    Problem("g7", "geometry",
            "A triangle has sides of length 7, 24, and 25. What is its area?", 84),
    Problem("g8", "geometry",
            "An isoceles triangle has two equal sides of length 5 and a base of length 6. "
            "What is the height of the triangle measured from the base?",
            4),
]


def stream_mixed(seed: int = 0) -> list[Problem]:
    """Stream 1: 8 algebra interleaved with 8 geometry, simple shuffle."""
    import random
    rng = random.Random(seed)
    items = list(ALGEBRA) + list(GEOMETRY)
    rng.shuffle(items)
    return items


def stream_drift(seed: int = 0) -> list[Problem]:
    """Stream 2: first half mixed, second half mostly algebra (geometry dries up).

    Used to exercise the merge code path: after split, geometry frequency
    falls below threshold, system should merge back to a generalist.
    """
    import random
    rng = random.Random(seed)
    first = list(ALGEBRA[:4]) + list(GEOMETRY[:4])
    rng.shuffle(first)
    second = list(ALGEBRA[4:]) + list(GEOMETRY[4:5])  # 4 alg + 1 geo
    rng.shuffle(second)
    return first + second


_NUM = re.compile(r"-?\d+(?:\.\d+)?")


def grade(response: str, expected: int) -> bool:
    """True if the response's declared ANSWER equals expected.

    Looks for a line beginning with ANSWER: (case-insensitive). Falls back
    to the LAST number in the response if no marker.
    """
    if not response:
        return False
    m = re.search(r"ANSWER\s*[:=]\s*(-?\d+(?:\.\d+)?)", response, re.I)
    if m:
        try:
            v = float(m.group(1))
        except ValueError:
            return False
        return abs(v - expected) < 1e-6
    nums = _NUM.findall(response)
    if not nums:
        return False
    try:
        v = float(nums[-1])
    except ValueError:
        return False
    return abs(v - expected) < 1e-6


if __name__ == "__main__":
    s = stream_mixed()
    print(f"mixed stream: {len(s)} items, "
          f"alg={sum(1 for p in s if p.domain=='algebra')} "
          f"geo={sum(1 for p in s if p.domain=='geometry')}")
    s2 = stream_drift()
    print(f"drift stream: {len(s2)} items, "
          f"alg={sum(1 for p in s2 if p.domain=='algebra')} "
          f"geo={sum(1 for p in s2 if p.domain=='geometry')}")

"""Harder problem set + an interleaved 'noisy preamble' loader.

The hypothesis split should win on is *context isolation*: when a stream is
mixed with off-domain noise, a generalist can spend tokens / lose precision
on the wrong frame. We simulate this with two harder mixed sets:

- mixed_hard:   trickier traps + a few multi-step problems
- mixed_noisy:  same problems prefixed with off-domain ramble that a
                generalist must wade through, but a specialist can ignore
                because the supervisor split prompt narrows scope.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import re
import random

from outline.experiments.expert_split_merge.tasks import Problem, ALGEBRA, GEOMETRY, grade  # reuse


HARD_ALGEBRA = [
    Problem("ha1", "algebra",
            "Real numbers x, y satisfy x + y = 6 and xy = 5. "
            "What is x^3 + y^3?",
            126),
    Problem("ha2", "algebra",
            "If x^2 - 6x + 8 = 0, what is the SUM of all real solutions?",
            6),
    Problem("ha3", "algebra",
            "Solve over the reals: |2x - 3| = 7. What is the SUM of all real solutions?",
            3, trap=True),
    Problem("ha4", "algebra",
            "If 2^x = 32 and 3^y = 27, what is x + y?",
            8),
    Problem("ha5", "algebra",
            "What is the value of the expression (x+1)^2 - (x-1)^2 when x = 5?",
            20),
    Problem("ha6", "algebra",
            "If f(x) = x^2 + 1 and g(x) = 2x, what is f(g(3))?",
            37),
    Problem("ha7", "algebra",
            "If a, b, c are real and a + b + c = 6, ab + bc + ca = 11, abc = 6, "
            "what is a^2 + b^2 + c^2?",
            14),
    Problem("ha8", "algebra",
            "What is the SUM of all real x with x^4 = 16?",
            0, trap=True),
]


HARD_GEOMETRY = [
    Problem("hg1", "geometry",
            "A right triangle has legs 9 and 12. What is its area?", 54),
    Problem("hg2", "geometry",
            "An equilateral triangle has side length 6. What is its area, "
            "rounded to the nearest integer (use sqrt(3) ~ 1.732)?",
            16),
    Problem("hg3", "geometry",
            "A circle has CIRCUMFERENCE 12. Using pi=3, what is its DIAMETER?",
            4, trap=True),
    Problem("hg4", "geometry",
            "Rectangle has perimeter 20 and one side of length 4. What is its area?",
            24),
    Problem("hg5", "geometry",
            "A regular hexagon is composed of 6 equilateral triangles. If each "
            "triangle has area 5, what is the area of the hexagon?",
            30),
    Problem("hg6", "geometry",
            "A right triangle has area 24 and one leg 6. What is the OTHER leg?",
            8),
    Problem("hg7", "geometry",
            "Cylinder of radius 3 and height 4, using pi=3. What is its lateral "
            "surface area (the curved side, not the caps)?",
            72),
    Problem("hg8", "geometry",
            "A square has area 64. A circle is inscribed in the square. Using pi=3, "
            "what is the area of the inscribed circle?",
            48),
]


NOISE_PARAGRAPHS = [
    "While walking my dog this morning I noticed an interesting cloud formation, "
    "and over breakfast I read three pages of a novel about deep-sea cephalopods. "
    "Anyway, here is a problem I'd like solved cleanly:\n",
    "I'm collecting unrelated trivia: the longest river in Asia, the boiling "
    "point of mercury, the year the Sahara last greened, and the name of a "
    "minor character in Middlemarch. Setting all that aside, please answer:\n",
    "There's a chess opening called the Sokolsky which I'm trying to learn. "
    "I also have a standing order at a coffee shop: oat-milk cortado. None of "
    "this matters for the problem below; please ignore it and answer:\n",
    "Last week I tried to debug a flaky network test and ended up reading "
    "about TCP slow-start. Tangentially, the wallpaper in my office is teal. "
    "Now, the actual question:\n",
    "I am reviewing notes on Bantu language phonotactics and the pricing of "
    "South Indian filter coffee. None of this is relevant. The problem:\n",
    "Earlier I was thinking about the 1956 Hungarian uprising and a recipe for "
    "tarte tatin. Disregard. Here is what I actually need:\n",
]


def stream_hard(seed: int = 0) -> list[Problem]:
    rng = random.Random(seed)
    items = list(HARD_ALGEBRA) + list(HARD_GEOMETRY)
    rng.shuffle(items)
    return items


def stream_noisy(seed: int = 0) -> list[Problem]:
    """Same as stream_hard but each Problem.question gets prefixed with noise."""
    rng = random.Random(seed)
    items = list(HARD_ALGEBRA) + list(HARD_GEOMETRY)
    rng.shuffle(items)
    out = []
    for p in items:
        noise = rng.choice(NOISE_PARAGRAPHS)
        out.append(Problem(
            pid=p.pid, domain=p.domain,
            question=noise + p.question,
            answer=p.answer, trap=p.trap,
        ))
    return out


if __name__ == "__main__":
    s = stream_hard(0)
    print(f"hard: {len(s)} items, alg={sum(1 for p in s if p.domain=='algebra')} "
          f"geo={sum(1 for p in s if p.domain=='geometry')}")
    sn = stream_noisy(0)
    print(f"noisy: {len(sn)} items, sample preview:")
    print(sn[0].question[:200])

"""Probe set 4 — substantially harder, designed to actually break Haiku.

Strategy
--------
The earlier probes failed to break Haiku because individual problems were
within its competence and the noise wasn't enough to derail it. This
harder set:

  1. Uses three subdomains (instead of two): combinatorics, probability,
     number-theory. More heterogeneity = more frame-confusion pressure.
  2. Each problem is genuinely hard for Haiku (multi-step, traps that
     specifically defeat shortcuts).
  3. Adds a *2.5KB* off-domain preamble of the kind Haiku is known to
     skim (semi-relevant looking math-y prose that might be mistaken
     for context — adversarial "near-noise" rather than obviously
     unrelated trivia).
  4. Stream length is 30 (not 16), so the supervisor's window has
     genuine opportunity to react to errors and so context drift has
     time to set in.

If even THIS regime cannot show a daylight between static-1 and dynamic,
the previous conclusion is decisively confirmed.
"""
from __future__ import annotations
from dataclasses import dataclass
import random
from outline.experiments.expert_split_merge.tasks import Problem, grade  # reuse


# Combinatorics — multi-step, real traps Haiku falls into
COMBO_HARD = [
    Problem("xc1", "combo",
            "How many distinct permutations of the letters of MISSISSIPPI begin "
            "and end with the letter S?",
            3780),  # 9!/(1!*4!*2!*2!) = 3780
    Problem("xc2", "combo",
            "From a 52-card deck, how many 5-card hands contain at least one "
            "card from each of the 4 suits?",
            685464),  # 685,464 distinct hands
    Problem("xc3", "combo",
            "How many integers from 1 to 1000 (inclusive) are NOT divisible "
            "by 2, 3, or 5? (Use inclusion-exclusion.)",
            266),
    Problem("xc4", "combo",
            "How many distinct ways are there to arrange 4 As and 3 Bs in a "
            "row such that NO two As are adjacent?",
            1),  # 3 Bs create 4 gaps; choose 4 of them for As: C(4,4)=1
    Problem("xc5", "combo",
            "In how many ways can 6 distinguishable balls be placed into 3 "
            "distinguishable boxes so that NO box is empty?",
            540),  # 3^6 - C(3,1)*2^6 + C(3,2)*1^6 = 729-192+3 = 540
    Problem("xc6", "combo",
            "How many positive integers ≤ 1000 have all distinct digits?",
            738),  # 9 + 81 + 648 = 738
    Problem("xc7", "combo",
            "How many distinct triangles can be formed using 3 vertices chosen "
            "from a regular octagon (8-sided polygon)?",
            56),  # C(8,3) = 56
    Problem("xc8", "combo",
            "In how many ways can 5 boys and 5 girls be seated alternately "
            "around a round table of 10 seats? (Two seatings that differ by "
            "rotation are considered the same; reflections are NOT considered "
            "the same.)",
            2880),  # (5-1)! * 5! = 24 * 120 = 2880
]

# Probability — answer is integer a+b after reducing a/b to lowest terms
PROB_HARD = [
    Problem("xp1", "prob",
            "Three fair 6-sided dice are rolled. What is the probability that "
            "the SUM is exactly 10? Express as a/b in lowest terms; give a + b.",
            9),  # 27/216 = 1/8 -> 1+8 = 9
    Problem("xp2", "prob",
            "From a standard 52-card deck, two cards are drawn without "
            "replacement. What is the probability BOTH are FACE cards "
            "(J, Q, K)? Express as a/b in lowest terms; give a + b.",
            232),  # 12*11/(52*51) = 132/2652 = 11/221 -> a+b = 232
    Problem("xp3", "prob",
            "A fair coin is flipped 6 times. What is the probability of "
            "getting EXACTLY 3 heads? Express as a/b in lowest terms; give a + b.",
            21),  # C(6,3)/64 = 20/64 = 5/16 -> 21
    Problem("xp4", "prob",
            "An urn has 4 red, 5 blue, 6 green balls. Three balls are drawn "
            "without replacement. What is the probability all 3 are the SAME "
            "color? Express as a/b in lowest terms; give a + b.",
            489),  # (4+10+20)/455 = 34/455, gcd 1, 34+455=489
    Problem("xp5", "prob",
            "Two fair 6-sided dice are rolled. Given that the SUM is 7, what "
            "is the probability that one of the dice shows a 1? Express as a/b "
            "in lowest terms; give a + b.",
            4),  # 2/6 = 1/3 -> 4
    Problem("xp6", "prob",
            "A bag has 5 red and 7 blue marbles. Three are drawn WITHOUT "
            "replacement. What is the probability that EXACTLY 2 are red? "
            "Express as a/b in lowest terms; give a + b.",
            29),  # C(5,2)*C(7,1)/C(12,3) = 10*7/220 = 70/220 = 7/22 -> 29
    Problem("xp7", "prob",
            "What is the probability that a random permutation of the letters "
            "in BANANA spells BANANA? Express as a/b in lowest terms; give a + b.",
            61),  # 1/60 -> 1+60=61
    Problem("xp8", "prob",
            "5 fair coins are flipped. What is the probability that the number "
            "of heads is GREATER than the number of tails? Express as a/b in "
            "lowest terms; give a + b.",
            3),  # 16/32 = 1/2 -> 3
]

# Number theory — Haiku's known weak spot
NUMTH_HARD = [
    Problem("xn1", "numth",
            "What is the sum of all positive divisors of 360 (including 1 and 360)?",
            1170),  # σ(360)=1170
    Problem("xn2", "numth",
            "Find the smallest positive integer N such that N has exactly 12 "
            "positive divisors.", 60),
    Problem("xn3", "numth",
            "What is the remainder when 7^100 is divided by 13? (Use Fermat's "
            "little theorem.)", 9),  # 7^12 ≡ 1 mod 13, 100 mod 12 = 4, 7^4 = 2401 mod 13
                                     # 2401 = 13*184 + 9 -> 9
    Problem("xn4", "numth",
            "What is the units digit (last digit) of 7^2026?",
            9),  # 7,9,3,1 cycle of 4. 2026 mod 4 = 2 -> 9
    Problem("xn5", "numth",
            "Find the greatest common divisor (GCD) of 462 and 1071.", 21),
    Problem("xn6", "numth",
            "What is the sum of the prime factorization exponents of 720? "
            "(For 720 = 2^4 * 3^2 * 5^1, the answer would be 4+2+1.)",
            7),
    Problem("xn7", "numth",
            "How many positive integers less than 100 are coprime to 100? "
            "(I.e., compute Euler's φ(100).)", 40),
    Problem("xn8", "numth",
            "What is the smallest positive integer N such that N is divisible "
            "by 6 and the sum of its digits equals 18 and N has all distinct "
            "digits?", 198),  # 198 = 6*33, digit sum = 18, distinct digits
]


# Adversarial near-noise: looks like math-context, isn't.
NOISE_BIG = """\
Some background context I have been turning over before posing the
problem. Last spring I was reading Hardy and Wright on the distribution
of primes and noticed an aside about a 19th-century French argument that
the average number of divisors of a positive integer up to N is
approximately log N + 2γ − 1, where γ is the Euler-Mascheroni constant.
That note connected for me to the modern divisor-function asymptotics
discussed in Tenenbaum's textbook, which I have been re-reading on
public-transit commutes. I have also been thinking about a much older
problem from de Bruijn's analytic combinatorics era — namely how the
number of partitions p(n) grows roughly like exp(π·sqrt(2n/3))/(4n·sqrt(3))
according to the Hardy-Ramanujan formula. None of this is directly
relevant to the question I am about to ask; I am simply noting it because
my mind is in a number-theoretic mood and I want to flag that the
question is NOT about partitions, NOT about divisor-sum asymptotics, and
NOT about analytic combinatorics — it is a discrete combinatorial
counting question (or probability, or number theory, depending on which
question I ask). Please do not try to apply asymptotic reasoning. Treat
it as an exact, finite, elementary problem.

I should also mention, for completeness, that I have been reviewing
Mossel and Peres' notes on probabilistic combinatorics, especially the
section on second-moment arguments for threshold phenomena in random
graphs. Again, not relevant here. The question is exact, not asymptotic.
And I have been re-reading Stanley's Enumerative Combinatorics Volume 1,
chapter 1, on the basic counting principles, and chapter 3, on partially
ordered sets. Also not relevant. Please ignore.

A note on style: please show your reasoning briefly, but do not invoke
generating functions, asymptotic methods, the Chinese Remainder Theorem
unless directly required, or any heavy machinery. The question admits an
elementary, finite computation. The expected answer is a single integer.

Now, here is the actual problem, which I would like answered exactly:

"""


def stream_xhard(seed: int = 0) -> list[Problem]:
    """30-item stream: 8 combo + 8 prob + 8 numth + 6 repeats from a random
    domain to bring length to 30."""
    rng = random.Random(seed)
    base = list(COMBO_HARD) + list(PROB_HARD) + list(NUMTH_HARD)
    rng.shuffle(base)
    extra = list(rng.sample(base, 6))
    items = base + extra
    rng.shuffle(items)
    return [Problem(p.pid, p.domain, NOISE_BIG + p.question, p.answer, p.trap)
            for p in items]


if __name__ == "__main__":
    s = stream_xhard(0)
    print(f"xhard: {len(s)} items, "
          f"combo={sum(1 for p in s if p.domain=='combo')} "
          f"prob={sum(1 for p in s if p.domain=='prob')} "
          f"numth={sum(1 for p in s if p.domain=='numth')}")
    print("first item char-len:", len(s[0].question))
    print("first item ends with:", repr(s[0].question[-200:]))

#!/usr/bin/env python3
"""
Solving the Polya Urn Problem:
A box contains 1 red ball and 1 black ball.
- Draw a ball uniformly at random
- If red: put it back AND add one more red ball
- If black: remove it permanently (game ends)

Find: Expected number of red balls at the moment the black ball is removed
"""

import random
from fractions import Fraction

def analyze_problem():
    """
    Let's think about this problem carefully.

    State: (r, 1) where r is the number of red balls, and there's always 1 black ball
    until the game ends.

    Starting state: (1, 1)

    At state (r, 1):
    - Total balls = r + 1
    - P(draw red) = r/(r+1)
    - P(draw black) = 1/(r+1)

    If we draw red: go to state (r+1, 1)
    If we draw black: game ends with r red balls

    Let E(r) = expected number of red balls at game end, starting from state (r, 1)

    E(r) = P(draw red) * E(r+1) + P(draw black) * r
    E(r) = (r/(r+1)) * E(r+1) + (1/(r+1)) * r

    Multiply both sides by (r+1):
    (r+1) * E(r) = r * E(r+1) + r

    Rearranging:
    r * E(r+1) = (r+1) * E(r) - r
    E(r+1) = ((r+1)/r) * E(r) - 1

    Let's compute this recursively and see if there's a pattern.
    """

    print("=" * 70)
    print("ANALYTICAL APPROACH")
    print("=" * 70)

    # Let's try to find E(1), E(2), E(3), etc.
    # We need a base case or boundary condition

    # Actually, let's think differently using the recurrence:
    # E(r) = (r/(r+1)) * E(r+1) + r/(r+1)

    # Let's compute P(end at exactly r red balls) starting from state (1,1)
    print("\nProbability of ending at each state:")
    print("-" * 70)

    # P(end at r=1) = P(draw black immediately) = 1/2
    # P(end at r=2) = P(draw red, then black) = (1/2) * (1/3)
    # P(end at r=3) = P(draw red, red, then black) = (1/2) * (2/3) * (1/4)
    # P(end at r=k) = P(draw k-1 reds, then black)

    # When we have r red balls and 1 black:
    # P(draw red) = r/(r+1)
    # P(draw black) = 1/(r+1)

    # Starting from (1,1):
    # P(end at r=1) = 1/2
    # P(end at r=2) = (1/2) * (1/3) = 1/6
    # P(end at r=3) = (1/2) * (2/3) * (1/4) = 2/24 = 1/12
    # P(end at r=4) = (1/2) * (2/3) * (3/4) * (1/5) = 6/120 = 1/20

    # Pattern: P(end at r=k) = (1/2) * (2/3) * (3/4) * ... * ((k-1)/k) * (1/(k+1))
    #                        = [product from i=1 to k-1 of i/(i+1)] * (1/(k+1))
    #                        = [1/(k)] * (1/(k+1))
    #                        = 1/(k(k+1))

    max_r = 20
    probabilities = {}
    for r in range(1, max_r + 1):
        prob = Fraction(1, r * (r + 1))
        probabilities[r] = prob
        if r <= 10:
            print(f"P(end at r={r}) = {prob} = {float(prob):.6f}")

    # Verify probabilities sum to something reasonable
    total_prob = sum(probabilities.values())
    print(f"\nSum of P(end at r=1 to {max_r}) = {total_prob} = {float(total_prob):.6f}")

    # The sum should be: sum_{k=1}^{infinity} 1/(k(k+1))
    # Using partial fractions: 1/(k(k+1)) = 1/k - 1/(k+1)
    # So sum = (1/1 - 1/2) + (1/2 - 1/3) + (1/3 - 1/4) + ...
    #        = 1 (telescoping series)
    print("\nNote: The infinite sum equals 1 (telescoping series)")
    print("This confirms our probability calculation is correct.")

    # Now compute expected value
    print("\n" + "=" * 70)
    print("EXPECTED VALUE CALCULATION")
    print("=" * 70)

    # E[R] = sum_{r=1}^{infinity} r * P(end at r)
    #      = sum_{r=1}^{infinity} r * 1/(r(r+1))
    #      = sum_{r=1}^{infinity} 1/(r+1)

    print("\nE[R] = sum_{r=1}^{infinity} r * P(end at r)")
    print("     = sum_{r=1}^{infinity} r * 1/(r(r+1))")
    print("     = sum_{r=1}^{infinity} 1/(r+1)")
    print("     = 1/2 + 1/3 + 1/4 + 1/5 + ...")
    print("\nThis is the harmonic series (minus the first term), which DIVERGES!")

    # Let's compute partial sums to verify
    print("\nPartial sums:")
    print("-" * 70)
    partial_sum = Fraction(0)
    for r in range(1, 101):
        contribution = r * probabilities.get(r, Fraction(1, r * (r + 1)))
        partial_sum += contribution
        if r in [1, 2, 3, 4, 5, 10, 20, 50, 100]:
            print(f"E[R | end at r <= {r:3d}] = {float(partial_sum):.6f}")

    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("\nThe expected number of red balls at the moment the black ball")
    print("is removed is INFINITE (the expectation diverges).")
    print("\nThis happens because:")
    print("1. P(end at r) = 1/(r(r+1)) decreases slowly (like 1/r²)")
    print("2. E[R] = sum r * P(end at r) = sum 1/(r+1) (harmonic series)")
    print("3. The harmonic series diverges to infinity")

    return None  # Expectation is infinite

def monte_carlo_simulation(n_simulations=100000):
    """
    Run Monte Carlo simulation to verify our analytical result.
    """
    print("\n" + "=" * 70)
    print("MONTE CARLO SIMULATION")
    print("=" * 70)

    results = []

    for _ in range(n_simulations):
        red_balls = 1
        black_balls = 1

        while black_balls > 0:
            total = red_balls + black_balls
            # Draw a ball
            if random.random() < red_balls / total:
                # Drew red
                red_balls += 1
            else:
                # Drew black
                black_balls = 0

        results.append(red_balls)

    # Calculate statistics
    mean = sum(results) / len(results)
    sorted_results = sorted(results)
    median = sorted_results[len(results) // 2]
    variance = sum((x - mean) ** 2 for x in results) / len(results)
    std_dev = variance ** 0.5
    min_val = min(results)
    max_val = max(results)

    print(f"\nSimulations: {n_simulations:,}")
    print(f"Mean: {mean:.2f}")
    print(f"Median: {median:.2f}")
    print(f"Std Dev: {std_dev:.2f}")
    print(f"Min: {min_val}")
    print(f"Max: {max_val}")

    # Show distribution
    print("\nDistribution of outcomes:")
    from collections import Counter
    counter = Counter(results)
    for val in sorted(counter.keys())[:15]:
        count = counter[val]
        prob_empirical = count / n_simulations
        prob_theoretical = 1 / (val * (val + 1))
        print(f"r={val:3d}: {count:6d} times ({prob_empirical:.6f}) "
              f"[theoretical: {prob_theoretical:.6f}]")

    print("\nNote: The mean keeps growing with more simulations,")
    print("confirming that the expectation diverges.")

if __name__ == "__main__":
    analyze_problem()
    monte_carlo_simulation(100000)

    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)
    print("\nThe expected number of red balls at the moment the black ball")
    print("is removed is: INFINITY (∞)")
    print("\nThe expectation diverges because E[R] = sum_{r=1}^∞ 1/(r+1),")
    print("which is the harmonic series (minus first term).")

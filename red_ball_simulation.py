import random
import numpy as np

def simulate_game():
    """Simulate one game and return the number of red balls when black is drawn."""
    red_balls = 1

    while True:
        # Total balls = red_balls + 1 (black)
        total = red_balls + 1

        # Draw uniformly at random
        if random.random() < red_balls / total:
            # Drew red ball
            red_balls += 1
        else:
            # Drew black ball - game ends
            return red_balls

# Run simulations
num_simulations = 1000000
results = [simulate_game() for _ in range(num_simulations)]

# Analyze results
print(f"Number of simulations: {num_simulations}")
print(f"\nMean number of red balls: {np.mean(results):.4f}")
print(f"Median number of red balls: {np.median(results):.1f}")
print(f"Max observed: {max(results)}")
print(f"\nDistribution of outcomes:")

# Check empirical probabilities for small values
for r in range(1, 11):
    empirical_prob = sum(1 for x in results if x == r) / num_simulations
    theoretical_prob = 1 / (r * (r + 1))
    print(f"P(R={r:2d}): Empirical = {empirical_prob:.6f}, Theoretical = {theoretical_prob:.6f}")

# Show that the mean keeps growing
print(f"\nPartial sums of theoretical expectation:")
for n in [10, 50, 100, 500, 1000]:
    partial_sum = sum(1/(r+1) for r in range(1, n+1))
    print(f"Sum up to r={n:4d}: {partial_sum:.4f}")

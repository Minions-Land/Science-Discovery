# Polya Urn Problem - Detailed Solution

## Problem Statement

A box contains exactly 1 red ball and 1 black ball. At each step:
- Draw a ball uniformly at random
- If it is red: put it back AND add one more red ball (red count increases by 1)
- If it is black: remove it permanently (the game ends)

Find the expected number of red balls in the box AT THE MOMENT the black ball is removed.

## Solution

### Step 1: Define the State Space

Let the state be characterized by r = number of red balls.
- Initially: r = 1, and there is 1 black ball
- At state r: total balls = r + 1

### Step 2: Transition Probabilities

At state r:
- P(draw red | state r) = r/(r+1)
- P(draw black | state r) = 1/(r+1)

If we draw red, we transition to state r+1.
If we draw black, the game ends with r red balls.

### Step 3: Calculate P(end with exactly r red balls)

Starting from r = 1:

**For r = 1:**
P(end at r=1) = P(draw black immediately) = 1/2

**For r = 2:**
P(end at r=2) = P(draw red at r=1) × P(draw black at r=2)
              = (1/2) × (1/3)
              = 1/6

**For r = 3:**
P(end at r=3) = P(draw red at r=1) × P(draw red at r=2) × P(draw black at r=3)
              = (1/2) × (2/3) × (1/4)
              = 1/12

**General Pattern:**

To end with exactly n red balls, we must:
1. Draw red at states r=1, 2, 3, ..., n-1 (n-1 times)
2. Draw black at state r=n

P(end at r=n) = (1/2) × (2/3) × (3/4) × ... × ((n-1)/n) × (1/(n+1))

### Step 4: Simplify Using Telescoping Product

The product telescopes:

(1/2) × (2/3) × (3/4) × ... × ((n-1)/n) = 1/n

Therefore:
P(end at r=n) = (1/n) × (1/(n+1)) = **1/(n(n+1))**

### Step 5: Verify Probabilities Sum to 1

We need to verify: Σ(n=1 to ∞) 1/(n(n+1)) = 1

Using partial fractions:
1/(n(n+1)) = 1/n - 1/(n+1)

This is a telescoping series:
Σ(n=1 to ∞) [1/n - 1/(n+1)] = (1/1 - 1/2) + (1/2 - 1/3) + (1/3 - 1/4) + ...
                             = 1/1 = 1 ✓

### Step 6: Calculate Expected Value

E[R] = Σ(n=1 to ∞) n × P(end at r=n)
     = Σ(n=1 to ∞) n × 1/(n(n+1))
     = Σ(n=1 to ∞) 1/(n+1)
     = 1/2 + 1/3 + 1/4 + 1/5 + ...

This is the **harmonic series** (minus the first term H₁ = 1).

### Step 7: Conclusion - The Expectation Diverges!

The harmonic series is known to diverge:

Σ(n=1 to ∞) 1/n = ∞

Therefore:
E[R] = Σ(n=1 to ∞) 1/(n+1) = **∞**

## Key Insights

1. **Probability Distribution**: P(r=n) = 1/(n(n+1)) is a valid probability distribution (sums to 1)

2. **Heavy Tail**: Although individual probabilities decrease, they decrease slowly enough (like 1/n²) that when multiplied by n, the sum diverges

3. **Logarithmic Growth**: The partial sums grow logarithmically:
   Σ(n=1 to N) 1/(n+1) ≈ ln(N)

4. **Median vs Mean**: The median is finite (equals 3), but the mean is infinite - a classic example of a distribution with infinite expectation

## Final Answer

The expected number of red balls at the moment the black ball is removed is **INFINITE**.

Mathematically: E[R] = ∞

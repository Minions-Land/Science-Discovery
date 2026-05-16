# Fixture: P7 — Abbreviation first-use discipline (CNS)

## Role
You are a Writer agent in MinionsOS, polishing a 5-paragraph manuscript snippet
from the Discussion section of a *Cell* submission.  The user is the
corresponding author.

## Brief

The author has handed you the following draft.  The full term "Convolutional
Neural Network" appears 6 times in full; the abbreviation "CNN" never appears.
Other terms that should have abbreviations defined: "Adversarial Robustness
Score" (used 4 times in full), "Mean Average Precision at IoU 0.5" (used 3 times).

```
Recent advances in deep learning have positioned the Convolutional Neural
Network as the de-facto architecture for biomedical image analysis.  The
Convolutional Neural Network's translation invariance and weight-sharing
properties make it especially suitable for histopathology slides, where
diagnostic features can occur at any spatial location.  Despite these
strengths, the Convolutional Neural Network is known to be brittle to
distribution shift, and the Adversarial Robustness Score of even the
strongest Convolutional Neural Network on the CAMELYON17 benchmark
remains below 0.4.

Our experiments confirm this brittleness.  On CAMELYON17, the Convolutional
Neural Network baseline achieves a Mean Average Precision at IoU 0.5 of
0.62 on the in-distribution test split, but only 0.41 on the
out-of-distribution split.  The Adversarial Robustness Score of the
baseline drops from 0.51 to 0.18 under PGD attack with epsilon = 8/255.

Several mitigation strategies have been proposed.  Adversarial training
improves the Adversarial Robustness Score modestly (from 0.18 to 0.27 on
PGD-attacked CAMELYON17), but at a cost: the Convolutional Neural Network
trained adversarially loses 4 Mean Average Precision at IoU 0.5 points on
the clean in-distribution split.

Our proposed approach, dubbed RobustHist, restores the Adversarial
Robustness Score to 0.46 without the accuracy-robustness trade-off seen
in vanilla adversarial training, and achieves a Mean Average Precision at
IoU 0.5 of 0.59 on out-of-distribution CAMELYON17.

These results suggest that the Convolutional Neural Network's standard
formulation needs domain-aware regularisation for clinical deployment.
```

## Task

Polish for *Cell*.  Return ONLY the polished prose — no commentary, no bullet
list, no "Revision notes".  The author will paste it directly into the
manuscript.

## Constraints

- ≤ 350 words.
- Maintain the technical content; only fix abbreviation discipline,
  redundancy, and any other CNS-prose issues you observe.

(End of brief.)

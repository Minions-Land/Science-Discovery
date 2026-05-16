Recent advances in deep learning have positioned convolutional neural networks (CNNs) as the de-facto architecture for biomedical image analysis. CNNs' translation invariance and weight-sharing properties make them especially suitable for histopathology slides, where diagnostic features can occur at any spatial location. Despite these strengths, CNNs are known to be brittle to distribution shift, and the adversarial robustness score (ARS) of even the strongest CNN on the CAMELYON17 benchmark remains below 0.4.

Our experiments confirm this brittleness. On CAMELYON17, the CNN baseline achieves a mean average precision at IoU 0.5 (mAP@0.5) of 0.62 on the in-distribution test split, but only 0.41 on the out-of-distribution split. The ARS of the baseline drops from 0.51 to 0.18 under PGD attack with epsilon = 8/255.

Several mitigation strategies have been proposed. Adversarial training improves the ARS modestly (from 0.18 to 0.27 on PGD-attacked CAMELYON17), but at a cost: the adversarially trained CNN loses 4 mAP@0.5 points on the clean in-distribution split.

Our proposed approach, dubbed RobustHist, restores the ARS to 0.46 without the accuracy-robustness trade-off seen in vanilla adversarial training, and achieves an mAP@0.5 of 0.59 on out-of-distribution CAMELYON17.

These results suggest that the CNN's standard formulation needs domain-aware regularization for clinical deployment.
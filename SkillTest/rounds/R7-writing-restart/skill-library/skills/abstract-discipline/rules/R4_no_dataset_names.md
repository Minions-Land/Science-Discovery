---
id: R4
name: no_dataset_names
trigger:
  draft_section: [abstract, conclusion]
  contains_pattern: '\b(CIFAR-10|CIFAR-100|ImageNet|CASP\d+|PDB|LIVECell|CellPose|COCO|GLUE|SuperGLUE|MNIST|SQuAD|AlphaFold-?\d?)\b'
---

**规则**：Abstract / Conclusion 不可含具体数据集名或具体竞争对手名。

**触发**：检测到 CIFAR-10、ImageNet、CASP15、PDB、LIVECell、AlphaFold-2 等具体 artifact 名。

**修复**：替换为类别描述：
- `CASP15 free-modelling targets` → `established structure-prediction benchmarks`
- `CIFAR-10 / ImageNet` → `standard image classification benchmarks`
- `PDB` → `curated public protein databases`
- `AlphaFold-2 retraining` → `state-of-the-art baselines`

**例外（弱化版）**：conference 论文里如果具体名字是核心 contribution 的一部分，可保留一处；但不要堆砌。

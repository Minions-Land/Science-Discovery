---
id: R1
name: first_use_full_form
trigger:
  section: [global]
  contains_pattern: '\b(CNN|GAN|VAE|LSTM|GNN|MLP|BERT|GPT|RL|NLP|CV)\b'
---

**规则**：第一次出现用"全称（简写）"。

**触发**：检测到缩写词。

**格式**：`Convolutional Neural Network (CNN)`

**注意**：检查是否是该 section 的第一次出现（见 R3）。

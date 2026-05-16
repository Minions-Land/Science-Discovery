---
id: R1
name: no_implementation_details
trigger:
  draft_section: [intro]
  contains_pattern: '\b(\d+M-parameter|\d+\s*million|FAISS|HNSW|ESM-\d|Adam|SGD|learning rate|batch size|epoch|GPU-hour|\d+k chains|\d+ layers)\b'
---

**规则**：Introduction 不可含实现细节。

**触发**：检测到参数量、优化器名、索引结构、具体层数、训练配置等。

**修复**：替换为方法类描述：
- `350M-parameter diffusion U-Net` → `a learned diffusion prior`
- `FAISS HNSW over ESM-2 embeddings` → `retrieval over structural embeddings`
- `trained for 200 epochs with Adam` → 删除（属于 Method section）

**边界 case**：prior work 的量化事实（如 "AlphaFold-2 requires ~20,000 GPU-hours"）是背景信息，允许保留——规则只针对**本文方法**的实现细节。

# GAIA Baseline Experiment Scripts

## Overview

这个目录包含 GAIA baseline 实验的所有脚本，按照 GPQA-Diamond 的实验设计镜像。

## Setup Scripts

### 1. 下载数据集
```bash
python scripts/download_gaia.py
```
从 HuggingFace 下载 GAIA validation split（165 题）+ ground truth + 附件。

### 2. 抽取 mini sample
```bash
python scripts/extract_mini_sample.py
```
随机抽取 12 题作为快速验证管线的 mini sample。

### 3. 按 Level 切分
```bash
python scripts/split_by_level.py
```
将 validation 数据按 Level 1/2/3 切分到 `data/by_level/`。

### 4. 生成 prompt 文件
```bash
python scripts/build_prompts.py
```
生成所有评测模式的 prompt 文件到 `data/prompts/`。

## Evaluation Scripts

### Single-question mode
```bash
./scripts/run_single.sh <model> <task_id>

# Examples:
./scripts/run_single.sh sonnet task_001
./scripts/run_single.sh haiku task_042
```

### Batch mode (mini 12)
```bash
./scripts/run_batch.sh <model>

# Examples:
./scripts/run_batch.sh sonnet
./scripts/run_batch.sh haiku
```

### By-level mode
```bash
./scripts/run_level.sh <model> <level>

# Examples:
./scripts/run_level.sh sonnet 1
./scripts/run_level.sh sonnet 2
./scripts/run_level.sh sonnet 3
./scripts/run_level.sh haiku 1
```

### Full mode (all 165)
```bash
./scripts/run_full.sh <model>

# Examples:
./scripts/run_full.sh sonnet
./scripts/run_full.sh haiku
```

## Grading Scripts

### Grade a single run
```bash
python scripts/grade.py --run-dir sessions/v1-baseline-pull/single/sonnet/<run_id>
```

### Grade all runs in a mode
```bash
python scripts/grade.py --mode single --model sonnet
python scripts/grade.py --mode batch --model haiku
python scripts/grade.py --mode level --model sonnet --level 2
```

## Analysis Scripts

### Summarize all runs
```bash
python scripts/summarize_run.py
```
生成 `BASELINE_SUMMARY.md`，包含所有 cell 的准确率、成本、工具调用数等。

### Analyze failure modes
```bash
python scripts/analyze_failures.py
```
分析失败模式：附件读取失败、浏览器超时、多步推理中断等。

## Directory Structure

```
scripts/
├── README.md                    # 本文件
├── download_gaia.py             # 下载数据集
├── extract_mini_sample.py       # 抽取 mini sample
├── split_by_level.py            # 按 Level 切分
├── build_prompts.py             # 生成 prompt 文件
├── run_single.sh                # 单题模式
├── run_batch.sh                 # 批量模式
├── run_level.sh                 # by-level 模式
├── run_full.sh                  # full 模式
├── grade.py                     # 评分（调用官方 scorer）
├── summarize_run.py             # 生成 BASELINE_SUMMARY.md
└── analyze_failures.py          # 失败模式分析
```

## Environment Requirements

- Python 3.11+
- `datasets` library (for HuggingFace download)
- Claude Code CLI
- `mcp__playwright` MCP server (for browser tasks)

## Next Steps

1. 跑通 mini sample × Sonnet single（验证管线）
2. 跑完所有 cell（single / batch / level / full × Sonnet / Haiku）
3. 生成 `BASELINE_SUMMARY.md`
4. 对比 GPQA-Diamond 的结果，看 GAIA 的难度梯度和工具调用分布

# GAIA Baseline Experiment

## Overview

GAIA (General AI Assistant) benchmark baseline 实验，对比 Sonnet 4.6 和 Haiku 4.5 在 GAIA validation split（165 题）上的表现。

实验设计参考 GPQA-Diamond，但有关键差异：
- **GPQA 禁工具**（看模型脑子）
- **GAIA 必须开工具**（看 Agent 系统能不能用工具完成任务）

## Quick Start

```bash
# 1. 下载数据集
python scripts/download_gaia.py

# 2. 准备数据
python scripts/extract_mini_sample.py
python scripts/split_by_level.py
python scripts/build_prompts.py

# 3. 跑通 mini sample（验证管线）
./scripts/run_batch.sh sonnet

# 4. 评分
python scripts/grade.py --mode batch --model sonnet

# 5. 跑完所有 cell
./scripts/run_all.sh

# 6. 生成报告
python scripts/summarize_run.py
```

## Experiment Design

详见 `Setting.md`。

### 数据集切分
- **Mini sample**: 随机 12 题（快速验证）
- **By-level**: Level 1/2/3 三组（看难度梯度）
- **Full**: validation 全集 165 题

### 评测模式
- **(a) Single**: 每题一个新沙箱
- **(b) Batch**: 12 题 mini sample 一次跑完
- **(c) By-level**: 分别跑 Level 1/2/3
- **(d) Full**: 165 题一次跑完

### 环境约束
- 干净沙箱（`env -i` + `--strict-mcp-config` + `--setting-sources ""`）
- 禁所有 MinionsOS hooks
- 不注入 CLAUDE.md / AGENTS.md / 项目 skill
- 保留 `goal-setting` skill 当 harness
- **工具全开**：Read/Write/Edit/Bash + WebSearch + WebFetch + mcp__playwright

### 模型设置
- `claude-sonnet-4-6` + `claude-haiku-4-5`
- `--effort max`
- 200K context

## Directory Structure

```
GAIA/
├── README.md                    # 本文件
├── Setting.md                   # 实验细则（完整版）
├── BASELINE_SUMMARY.md          # 结果报告（生成）
├── data/                        # 数据集
│   ├── validation.json          # GAIA validation split（165 题）
│   ├── ground_truth.json        # {task_id: final_answer}
│   ├── mini_sample.json         # 随机 12 题
│   ├── by_level/                # Level 1/2/3 切分
│   ├── attachments/             # 附件文件
│   └── prompts/                 # 生成的 prompt 文件
├── scripts/                     # 实验脚本
│   ├── download_gaia.py
│   ├── run_single.sh
│   ├── run_batch.sh
│   ├── run_level.sh
│   ├── run_full.sh
│   ├── grade.py
│   └── summarize_run.py
└── sessions/                    # Session 落盘
    └── v1-baseline-pull/
        ├── single/
        ├── batch/
        ├── level1/
        ├── level2/
        ├── level3/
        └── full/
```

## GAIA vs GPQA

| 维度 | GPQA-Diamond | GAIA |
|---|---|---|
| 题量 | 198 | validation 165 |
| 难度切分 | 按学科（phys/chem/bio） | 按 Level（1/2/3） |
| 输入 | 纯文本选择题 | 文本 + 附件（pdf/image/audio/xlsx/code） |
| 答案 | A/B/C/D 单字母 | 任意字符串，官方 normalizer |
| 工具策略 | **禁 WebSearch / WebFetch** | **必须开 WebSearch / WebFetch / playwright** |
| 评分 | grader agent 抽取 | 官方 question_scorer.py |

## Expected Outputs

### BASELINE_SUMMARY.md 包含：
1. **Per-cell accuracy**: single / batch / level / full × Sonnet / Haiku
2. **Level × accuracy 梯度**: Level 1 vs 2 vs 3 的塌方曲线
3. **Tool-call distribution per level**: 每题平均工具调用数
4. **Hard-ceiling intersection**: Sonnet ∩ Haiku 全错的题
5. **附件类型 × 准确率**: 纯文本 vs 含 pdf vs 含 image vs 含 audio
6. **Cost/accuracy frontier**: $/question
7. **Failure modes**: 附件读取失败、浏览器超时、多步推理中断等

## Next Steps

1. 跑通 mini sample × Sonnet single（验证管线）
2. 跑完所有 cell
3. 生成 `BASELINE_SUMMARY.md`
4. 对比 GPQA-Diamond 的结果
5. 设计 MinionsOS treatment（下一阶段）

## References

- GAIA paper: https://arxiv.org/abs/2311.12983
- HuggingFace dataset: `gaia-benchmark/GAIA`
- GPQA-Diamond 实验: `../GQPA-Diamond/`

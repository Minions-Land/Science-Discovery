# Auto-Research Benchmarks Dataset Collection

来源：`AI for Auto-Research: Roadmap & User Guide` (Kong et al., 2026, arXiv:2605.18661)

本目录按照论文的 8-stage 框架组织 73 个 benchmark 数据集。

## 目录结构

```
datasets/
├── 1.1-idea-generation/      # 6 benchmarks - 想法生成与评估
├── 1.2-literature-review/    # 7 benchmarks - 文献检索与综述
├── 1.3-coding-experiments/   # 25 benchmarks - 编码与实验（最密集）
├── 1.4-tables-figures/        # 7 benchmarks - 图表生成
├── 2-paper-writing/           # 3 benchmarks - 论文写作
├── 3.1-peer-review/           # 10 benchmarks - 同行评审
├── 3.2-rebuttal/              # 4 benchmarks - 答辩与修订
├── 4-dissemination/           # 6 benchmarks - Paper2X 传播
└── e2e-general/               # 5 benchmarks - 端到端与通用助手
```

## 下载优先级

### Tier 1 — 立即可评（17 项，标记 ✓）
这些 benchmark 可以直接对接 MinionsOS 现有模块，无需额外 adapter。

**Stage 1.2 Literature Review:**
- LitSearch (princeton-nlp/LitSearch)
- CiteME

**Stage 1.3 Coding & Experiments:**
- SWE-bench (princeton-nlp/SWE-bench)
- SciCode (scicode-bench/SciCode)
- MLAgentBench (snap-stanford/MLAgentBench)
- ScienceAgentBench
- KernelBench (ScalingIntelligence/KernelBench)
- TritonBench (thunlp/TritonBench)
- InfiAgent-DABench
- SUPER (AI2)
- CORE-Bench

**Stage 1.4 Tables & Figures:**
- TeXpert
- ChartQA

**Stage 2 Paper Writing:**
- SciIG
- AutoSurvey (AutoSurveys/AutoSurvey)

**Stage 3.1 Peer Review:**
- PeerRead
- ClaimCheck

**Stage E2E:**
- GAIA
- SimpleQA

### Tier 2 — 需轻量 adapter（34 项，标记 ~）
需要写 100-300 行 Python adapter 对接 MinionsOS 输入输出格式。

### Tier 3 — 需中等改造（16 项，标记 !）
需要扩展 MinionsOS 模块能力或添加新工具。

### Tier 4 — 当前不覆盖（6 项，标记 ✗）
全部在 Stage 4 Dissemination，MinionsOS 暂无 Paper2X 模块。

## 数据集元信息

每个 benchmark 子目录包含：
- `meta.json` - 数据集元信息（来源、规模、评分方式、论文链接）
- `adapter.py` - MinionsOS 适配器（如需要）
- `data/` - 实际数据集文件
- `README.md` - 该 benchmark 的详细说明与评测流程

## 下载脚本

运行 `./download_benchmarks.sh <tier>` 批量下载指定优先级的数据集。

示例：
```bash
# 下载 Tier 1 全部 17 项
./download_benchmarks.sh tier1

# 下载单个 benchmark
./download_single.sh SWE-bench
```

## 评测记录

每次评测结果记录在 `../memory/benchmark-<name>-<date>.md`，包含：
- MinionsOS 配置（哪些 Role 参与）
- 对照基线（single-agent / 竞品系统）
- 评分结果（benchmark 自带指标 + token/时间成本）
- 失败案例归因（哪个 Role / 工具 / 协作环节）

---

最后更新：2026-05-22

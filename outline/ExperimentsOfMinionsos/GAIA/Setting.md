---
所有实验产物都在 ./GAIA/ 这个文件夹下分门归类
---

# GAIA Baseline 实验细则

## 0. 阶段优先级

**第一步只做 Baseline。** 先把 Sonnet 4.6[200k] / Haiku 4.5[200k] 在 GAIA validation 上的成绩拿全。Baseline 是后续所有对比（加 hooks、加 MinionsOS、加 skill 等）的锚点；在它跑完之前不引入任何 MinionsOS 侧的介入。

## 1. 数据集切分

| 名称 | 范围 | 用途 |
|---|---|---|
| Mini sample | 随机抽取 12 题（validation split） | 快速过流程、跑通管线 |
| By-level | Level 1 / Level 2 / Level 3 三组分别跑 | 看难度梯度、工具调用数分布 |
| Full sample | validation 全集 165 题 | 完整 baseline 评分 |

**不做 test split（301 题）**：test 需要提交 HuggingFace leaderboard 才能拿到 score，本地无 ground truth。

Ground truth 提前抽出来，单独存在 `data/ground_truth.json`（结构 `{task_id: final_answer}`）。答题 agent 看不到这个文件；只有 §6 的评分脚本用它对照。

## 2. Baseline 环境约束

- **沙箱**：每次（每题或每批）必须在一个干净的 Claude Code 工作目录里跑，不继承宿主的项目状态。
- **不挂任何 hooks**：禁用 `large_file_guard` / `edit_failure_rescue` / `reel_capture` / `bg_keepalive_nudge` 等 MinionsOS 后期加入的所有 hook。
- **不注入额外提示**：沙箱内不存在 `CLAUDE.md` / `AGENTS.md` / 任何项目侧 skill 文件。若 Claude Code 默认会读 `~/.claude/CLAUDE.md`，需要用隔离 HOME 或干净的 `--settings` 绕开它。
- **唯一例外：保留 `goal-setting` skill**。它在这里的角色不是被测对象，而是 harness——目的是给 agent 一个明确的停止条件，避免中途停下不完成所有题。所有组别（Sonnet/Haiku × 单题/批量）都开着它，不进入 A/B 对照。
- **工具能力**（⚠ 与 GPQA 反向）：
  - 允许 Python（Bash 内 `python` / `uv run` 都可以）
  - **显式允许 WebSearch**（GAIA 必需）
  - **显式允许 WebFetch**（GAIA 必需）
  - **显式允许 mcp__playwright（浏览器）**（Level 2/3 多步浏览题需要）
  - 其余 Read / Write / Edit / Bash 等基础能力照常开启
- **附件处理**：每题的附件文件（pdf / image / audio / xlsx / code）提前 copy 到沙箱 cwd 下 `attachments/<task_id>/`，agent 用 Read / Bash / 浏览器自己处理。
- **不发任何提示语**：不在题目之外加 CoT 引导、格式约束、答题模板。

## 3. 模型设置

- 模型：`claude-sonnet-4-6` 和 `claude-haiku-4-5`，保持最原生状态（带 Harness + 200K 上下文）。
- 启动时显式带 `--effort max`。
- 输入：题目本身（Question + 附件路径）。
- 不约束输出格式；评分时由 grader 脚本从模型回答里抽取最终答案，跑官方 normalizer。

## 4. 评测模式

四种模式都要跑，结果分别归档。**全部采用 pull-pattern**（复用 GPQA v2 的教训：避免 output budget 爆、避免 bulk refusal）。

### (a) 单题模式
- 一题一个全新的 Claude Code 实例（新对话、新沙箱）。
- 不跨题共享上下文。
- 将需要回答的那个题目放到一个 markdown 文件 `question.md` 里面，附件放在 `attachments/<task_id>/`。
- prompt 极简：`@question.md` + `/goal 回答此题，把 FINAL ANSWER: <answer> 写到 answer.txt`。

### (b) 批量模式（Mini）
- 12 题 mini sample 一次性塞进同一个会话。
- 触发 auto-compact 也不管，直接吃掉。
- 将需要回答的题目集合放到一个 markdown 文件 `questions.md` 里面，附件统一放在 `attachments/`。
- prompt 极简：`@questions.md` + `/goal 回答所有题目，每题一行 FINAL ANSWER: <task_id> | <answer> append 到 answers.txt`。

### (c) By-level 模式
- 分别跑 Level 1 / Level 2 / Level 3 三组（替代 GPQA 的 by-domain）。
- 每组一个会话，pull-pattern 同 (b)。
- 目的：看难度梯度、工具调用数分布、Level 3 的多步浏览题是否触发 playwright。

### (d) Full 模式
- validation 全集 165 题一次跑完。
- pull-pattern 同 (b)，复用 GPQA v2 sonnet × full 60.1% 那条经验。

## 5. Session 落盘（硬要求）

**所有跑过的 session 都必须把原始推理轨迹落盘**，无论单题/批量、Sonnet/Haiku、答对/答错。这是后续所有分析（错因归类、行为对比、轨迹复现）的唯一可信源——丢一个就缺一个证据。

最低记录粒度：
- 完整 prompt（含系统提示，如果有的话）
- 模型完整原始输出（含 thinking blocks，如果模型支持）
- 每一次工具调用的 input / output（如果发生）
- 元数据：模型名、运行模式（single / batch / level / full）、task_id、时间戳、run_id

落盘目录建议结构：

```
outline/ExperimentsOfMinionsos/GAIA/sessions/
  v1-baseline-pull/
    <single|batch|level1|level2|level3|full>/<model>/<run_id>/
      transcript.jsonl
      answer.txt (或 answers.txt)
      attachments/  (符号链接到 ../../data/attachments/)
```

格式用 JSONL（一行一条记录，`type` 标注 `user|assistant|tool_use|tool_result|thinking`），而不是单一 .txt——方便后续编程切片对比。

## 6. 评分

- **复用 GAIA 官方 scorer**（`question_scorer.py` from HuggingFace gaia-benchmark），不要自己造，否则跟 leaderboard 对不上。
- normalizer 处理：lowercase、去 articles、list 分隔统一、数字/单位归一。
- 单题模式：每题对/错 → 准确率。
- 批量/by-level/full 模式：从最终 answers.txt 里抽取，对/错 → 准确率。
- 不做置信度、不做多次采样（除非后续阶段决定要做）。

## 7. GAIA 特有的报告维度（GPQA 没有的）

对照 GPQA-Diamond 的 `BASELINE_SUMMARY.md` 风格，加几个 GAIA 才有的轴：

### (a) Level × accuracy 梯度
```
| model | mode | Level 1 acc | Level 2 acc | Level 3 acc | overall acc |
```
Level 3 的塌方曲线是 baseline 的核心 signature。

### (b) Tool-call distribution per level
```
| model | mode | Level | avg tool calls | max tool calls | median |
```
GAIA Level 3 的题 paper 报告需要 ≥10 步；baseline 能不能达到这个复杂度？

### (c) Hard-ceiling intersection
Sonnet ∩ Haiku 全错的题（直接对应 MinionsOS 后续 treatment 的 priority target）。

### (d) 附件类型 × 准确率
```
| model | mode | 纯文本 | 含 pdf | 含 image | 含 audio | 含 code |
```
这条 GPQA 完全没有。

### (e) Cost/accuracy frontier
```
| model | mode | acc | $/question | total $ |
```
同 GPQA，但 GAIA 的工具调用数更多，成本会更高。

### (f) Failure modes（GAIA 特有）
- **附件读取失败**：agent 没找到 attachments/ 或没调 Read
- **浏览器超时**：playwright 卡住或页面加载失败
- **多步推理中断**：Level 3 题做到一半停了
- **答案格式错误**：没写 FINAL ANSWER 行或格式不对
- **工具调用错误**：WebSearch / WebFetch / playwright 返回错误

## 8. 与 GPQA 的核心差异总结

| 维度 | GPQA-Diamond | GAIA |
|---|---|---|
| 题量 | 198（已分 phys 86 / chem 93 / bio 19） | validation 165（Level 1/2/3） |
| 难度切分 | 按学科 | 按 Level（步数 + 工具数） |
| 输入 | 纯文本选择题 | 文本 + 附件（pdf / image / audio / xlsx / code） |
| 答案 | A/B/C/D 单字母 | 任意字符串，官方 normalizer 做 exact match |
| 工具策略 | 显式禁 WebSearch / WebFetch | **必须开 WebSearch / WebFetch / playwright** |
| 评分 | 人类 grader agent 抽取 | 官方 question_scorer.py |
| 报告维度 | 学科 × 准确率 | Level × 准确率 + 工具调用数 + 附件类型 |

**语义反转**：GPQA 是"看模型脑子"，所以禁工具；GAIA 是"看 Agent 系统能不能用工具完成任务"，必须开工具。GAIA 的"清纯"指的是 **不挂 MinionsOS 那一层**（hooks / skills / Roles），但 Web/Bash/Read/Write/playwright 这些 Claude Code 自带工具要全开。

## 9. 下一步行动清单

- [ ] 从 HuggingFace 下载 GAIA validation split（165 题）+ ground truth
- [ ] 随机抽取 mini sample 12 题，保存到 `data/mini_sample.json`
- [ ] 按 Level 切分：`data/by_level/level1.json` / `level2.json` / `level3.json`
- [ ] 下载所有附件文件到 `data/attachments/<task_id>/`
- [ ] 写 `scripts/build_prompts.py`（生成 question.md / questions.md）
- [ ] 写 `scripts/run_single.sh` / `run_batch.sh` / `run_level.sh` / `run_full.sh`
- [ ] 写 `scripts/grade.py`（调用官方 question_scorer.py）
- [ ] 写 `scripts/summarize_run.py`（生成 BASELINE_SUMMARY.md）
- [ ] 跑通 mini sample × Sonnet single（验证管线）
- [ ] 跑完所有 cell（single / batch / level / full × Sonnet / Haiku）
- [ ] 生成 `BASELINE_SUMMARY.md`

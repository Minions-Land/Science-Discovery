---
所有实验产物都在./GQPA-Diamond/这个文件夹下分门归类
---

# GPQA Diamond 实验细则

## 0. 阶段优先级

**第一步只做 Baseline。** 先把 Sonnet 4.6[200k] / Haiku 4.5[200k] 在 GPQA Diamond 上的成绩拿全。Baseline 是后续所有对比（加 hooks、加 MinionsOS、加 skill 等）的锚点；在它跑完之前不引入任何 MinionsOS 侧的介入。

## 1. 数据集切分

| 名称 | 范围 | 用途 |
|---|---|---|
| Mini sample | postgraduate 级别的 12 道题 | 快速过流程、跑通管线 |
| Full sample | 完整数据集 | 完整 baseline 评分 |

Ground truth 提前抽出来，单独存在 `data/ground_truth.json`（结构 `{question_id: answer_letter}`）。答题 agent 看不到这个文件；只有 §6 的评分 agent 用它对照。

## 2. Baseline 环境约束

- **沙箱**：每次（每题或每批）必须在一个干净的 Claude Code 工作目录里跑，不继承宿主的项目状态。
- **不挂任何 hooks**：禁用 `large_file_guard` / `edit_failure_rescue` / `reel_capture` / `bg_keepalive_nudge` 等 MinionsOS 后期加入的所有 hook。
- **不注入额外提示**：沙箱内不存在 `CLAUDE.md` / `AGENTS.md` / 任何项目侧 skill 文件。若 Claude Code 默认会读 `~/.claude/CLAUDE.md`，需要用隔离 HOME 或干净的 `--settings` 绕开它。
- **唯一例外：保留 `goal-setting` skill**。它在这里的角色不是被测对象，而是 harness——目的是给 agent 一个明确的停止条件，避免中途停下不完成所有题。所有组别（Sonnet/Haiku × 单题/批量）都开着它，不进入 A/B 对照。
- **工具能力**：
  - 允许 Python（Bash 内 `python` / `uv run` 都可以）
  - **显式禁用 Web Search**
  - **显式禁用 WebFetch**（避免变相联网检索）
  - 其余 Read / Write / Edit / Bash 等基础能力照常开启，不额外提醒
- **不发任何提示语**：不在题目之外加 CoT 引导、格式约束、答题模板。

## 3. 模型设置

- 模型：`claude-4-6-sonnet` 和 `claude-4-5-haiku`，保持最原生状态。（不过是带Harness的哦，以及200K上下文）
- 启动时显式带 `--effort max`。
- 输入：题目本身（题干 + 选项）。
- 不约束输出格式；评分时从模型回答里抽取最终答案即可。

## 4. 评测模式

两种模式都要跑，结果分别归档。

### (a) 单题模式
- 一题一个全新的 Claude Code 实例（新对话、新沙箱）。
- 不跨题共享上下文。
- 将需要回答的那个题目放到一个 markdown 文件里面。
- prompt 极简：[/goal 回答所有题目]。

### (b) 批量模式（Minimal）
- 12 道 postgrad 题一次性塞进同一个会话。 
- 触发 auto-compact 也不管，直接吃掉。
- 将需要回答的题目集合放到一个 markdown 文件里面。打乱难度/学科的顺序。
- prompt 极简：[/goal 回答所有题目]。

## 5. Session 落盘（硬要求）

**所有跑过的 session 都必须把原始推理轨迹落盘**，无论单题/批量、Sonnet/Haiku、答对/答错。这是后续所有分析（错因归类、行为对比、轨迹复现）的唯一可信源——丢一个就缺一个证据。

最低记录粒度：
- 完整 prompt（含系统提示，如果有的话）
- 模型完整原始输出（含 thinking blocks，如果模型支持）
- 每一次工具调用的 input / output（如果发生）
- 元数据：模型名、运行模式（single / batch）、题号、时间戳、run_id

落盘目录建议结构：

```
outline/ExperimentsOfMinionsos/GQPA-Diamond/sessions/
  <single|batch>/<model>/<run_id>/transcript.jsonl
```

格式用 JSONL（一行一条记录，`type` 标注 `user|assistant|tool_use|tool_result|thinking`），而不是单一 .txt——方便后续编程切片对比。

## 6. 评分
- 作答完毕后。人类会生成新的Agent，去检查最终的答案，并保留结果。
- 单题模式：每题对/错 → 准确率。
- 批量模式：从最终回答里抽取，对/错 → 准确率。
- 不做置信度、不做多次采样（除非后续阶段决定要做）。

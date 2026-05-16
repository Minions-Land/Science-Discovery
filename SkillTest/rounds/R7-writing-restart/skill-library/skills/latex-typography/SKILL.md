---
name: latex-typography
description: LaTeX 排版规范：模型名用 \newcommand 宏、避免 itemize（Intro contribution 除外）、不用 \paragraph{} 短头、不乱加粗/斜体。
triggers:
  - "排版"
  - "LaTeX polish"
  - "typography"
  - task in [polish, latex_review]
outputs: 符合 CNS/conference 排版规范的 LaTeX
scope:
  section: [global]
  paper_type: [CNS, conference]
---

# LaTeX Typography Discipline

| 规则 | 要求 |
|---|---|
| R1 模型名宏 | `\newcommand{\methodname}{\textsc{RetroDiff}\xspace}` 定义一次，全文调用 |
| R2 避免 itemize | 除 Intro contribution 外，不用 `\begin{itemize}` / `\begin{enumerate}` |
| R3 不用 \paragraph{} | 不要用 `\paragraph{Step 1.}` 这种短头；需要时用 `\noindent\textbf{...}` |
| R4 不乱加粗 | 只在首次定义术语时加粗；不要到处 `\textbf{}` |
| R5 不乱斜体 | 斜体只用于数学变量和外文术语 |
| R6 模型名字体 | 用 `\textsc{}` 或自定义字体命令突出模型名，不要用 `\texttt{}` |

详细规则见 `rules/`。

## Fitness (R7 Stage 1, n=22)

| 指标 | 值 |
|---|---|
| Skill 胜 | 11 |
| 平局 | 3 |
| Baseline 胜 | 8 |
| **净分** | **+3** |

**进化算法推荐**：
- 保留（validated）：R3, R6, _general
- 停用/修改（anti-validated）：R1, R2, R4

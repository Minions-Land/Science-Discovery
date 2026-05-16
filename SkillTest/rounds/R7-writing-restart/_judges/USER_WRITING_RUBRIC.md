# 用户写作判分准则（覆盖判官默认偏好）

> 本准则是 R7 及之后所有 round 的判分基准。当判官的判断与本准则冲突时，**以本准则为准**。
> 准则只适用于「写论文」相关任务；不适用于已经依赖原生 Claude 写作风格（如散文、邮件、文学）的任务。

## 1. 内容与结构

### 1.1 Abstract / Conclusion
- **必须只有 ONE 段落**。多段是错的。
- **不能出现引用（`\cite{}` 等）**。
- **不能出现具体数字**（精确实验值如 `TM-score 0.71`、`30×`、`1.2M-example`）。
- **不能提及具体数据集名**（如 `CIFAR-10`、`CASP15`、`PDB`、`LIVECell` 等）。
- 只能用定性描述（`order-of-magnitude`、`large-scale public benchmarks` 等）。

### 1.2 Introduction
- 重点是**背景介绍** + WHY this work matters。
- **不能写实现细节**：参数量、层数、学习率、具体优化器、具体索引结构（FAISS HNSW、ESM-2 embeddings 等）。
- 方法只在「类」层面描述：`a learned diffusion prior`、`retrieval-augmented decoding`。
- Contribution bullets（`itemize`）在 Intro 末尾是**允许的，且推荐**。

### 1.3 Related Work
- **这里才放具体方法细节**：模型、算法、实现方式。
- 必须把每一类前人方法分别讲清楚（model + algorithm + how implemented）。
- 应当显式连接到自己的 contribution / 解释 why prior work 不够。

## 2. Experiments
- 主实验：必须 vs 最经典 baselines + 最新 SOTA。
- 消融：证明每个模块最优；当多模块组合时证明组合最优；包含相邻模块的增/减实验；如果加某模块发现变差也要写出来。
- 超参数：报告不同超参数下的结果。
- Case Study & Visualization：展示真实案例上为什么我们的预测更好；**所有图/表必须配分析**，分析重点是 why baselines 这样表现 + why we 更好（设计原因 vs 其他原因）。

## 3. 排版与写作

### 3.1 格式
- **避免 `itemize` / `enumerate` 列表**。例外：Intro 末尾的 contribution bullets。
- **不要用 `\paragraph{...}` 加粗短头**——它显得很差。需要小标题时用 `\noindent\textbf{...}`。
- **不要乱加粗 / 乱用斜体**。
- **模型名应该用 `\newcommand` 定义一个宏**（如 `\newcommand{\methodname}{\textsc{RetroDiff}\xspace}`），后续都调用这个宏。可以在宏里加点 nice 字体处理（`\textsc`、`\textit` + 字体）做突出。
- 不要写 `\textbf{OurNet}` 散布在文中。

### 3.2 简写
- 第一次出现：`Convolutional Neural Network (CNN)`。
- 之后出现：只用 `CNN`，不要再写全称。

## 4. 复审规则（覆盖判官默认）

判官常见的与本准则冲突的偏好：

| 判官偏好 | 准则要求 | 复审动作 |
|---|---|---|
| 「保留 `\paragraph{}` 头部」是优点 | `\paragraph{}` 头部就是错的 | 该判罚反向（保留者输） |
| 「Abstract 里精确数字让 reviewer 有抓手」 | Abstract 不能有具体数字 | 该判罚反向 |
| 「Abstract 引用让贡献立得稳」 | Abstract 不能引用 | 该判罚反向 |
| 「实现细节放 Intro 让方法更具体」 | Intro 不放实现细节 | 该判罚反向 |
| 「保留 itemize 让结构清楚」 | itemize 在 Intro 之外要避免 | 该判罚反向 |
| 「过度删除是 over-aggressive」 | 删 `\paragraph` / 删 itemize 是对的 | 该判罚反向 |
| 「skill 加了 contribution bullets 不好」 | Intro 末尾的 contribution itemize 是允许且推荐的 | 该判罚反向 |
| 「模型名用 `\textbf` 直接写在文中」 | 应该用 `\newcommand` 宏 | 该判罚反向 |

## 5. 不适用场景

不要把上面规则套到：
- 文学 / 散文 / 创意写作（autumn prose 等）
- 邮件、Slack、对话类
- 科普 / 博客
- 用户明确要求保留原结构、只做 minor polish 的场景

这些场景下保留判官原判。

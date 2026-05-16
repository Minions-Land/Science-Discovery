---
id: R5
name: why_not_analysis
trigger:
  draft_section: [intro]
  task: [draft, polish]
---

**规则**：必须解释 prior work 为什么不够。

**触发**：撰写或润色 Intro 时。

**要求**：不能只说"没人做过"或"prior work has limitations"。必须具体说明：
- 为什么 diffusion priors 单独不够？（lack fine-grained structural knowledge）
- 为什么 retrieval methods 单独不够？（struggle to generalize beyond training neighborhoods）

**正确示例**：
> "However, diffusion priors alone lack the fine-grained structural knowledge encoded in large protein databases, while retrieval-augmented methods struggle to generalize beyond their training neighborhoods."

**错误示例**：
> "However, neither approach alone has achieved satisfactory performance."（太空泛）

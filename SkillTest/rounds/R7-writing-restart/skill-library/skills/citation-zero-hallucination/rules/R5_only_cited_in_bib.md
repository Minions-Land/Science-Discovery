---
id: R5
name: only_cited_in_bib
trigger:
  task: [final_check]
---

**规则**：references.bib 只含实际 cite 过的条目。

**要求**：最终提交前，过滤 .bib 文件：
1. 扫描所有 .tex 文件的 `\cite` 命令
2. 提取所有 citation keys
3. 只保留被引用的 BibTeX 条目
4. 删除未引用的条目

**原因**：bib bloat 是不专业的标志（reviewer 能看到 .bib 文件）。

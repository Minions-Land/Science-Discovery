---
id: R1
name: no_fabricated_bibtex
trigger:
  section: [global]
  task: [draft]
  contains_pattern: '(author.*=.*\{[A-Z]|title.*=.*\{)'
---

**规则**：不编造 BibTeX 条目。

**要求**：引用必须来自：
1. DBLP（最佳质量）
2. CrossRef DOI（fallback）
3. 用户提供的 .bib 文件

找不到的标 `% [VERIFY]` 注释，**绝不编造**。

**常见幻觉**：LLM 经常编造 venue name、page numbers、co-authors。即使 title 和 first author 对了，其他字段也可能是假的。

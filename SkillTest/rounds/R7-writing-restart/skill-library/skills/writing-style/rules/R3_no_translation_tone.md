---
id: R3
name: no_translation_tone
trigger:
  section: [global]
  contains_pattern: '(With the (rapid )?development of|plays an important role|has attracted (wide|extensive) attention|in recent years.*has become|make (a |an )?(great |significant )?contribution)'
---

**规则**：去翻译腔。

**触发**：检测到中文直译结构。

**常见翻译腔 + 修复**：
- "With the rapid development of deep learning…" → "Deep learning advances have enabled…" 或直接删掉，从具体问题开始
- "X plays an important role in Y" → "X enables Y" / "X is central to Y"
- "has attracted wide attention" → "is widely studied" 或删掉
- "make a great contribution to" → "advance" / "improve"

**原则**：英文学术写作从具体事实开始，不从宏大叙事开始。

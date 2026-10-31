# PDF Vector Layout Skill - 分发包

这是一个通用的 PDF 矢量排版与多文档融合 skill，可用于 Claude Code 和 Codex。

## 快速安装

### 方法 1：手动安装

**对于 Codex：**
```bash
cp -r pdf-vector-layout ~/.codex/skills/
```

**对于 Claude Code：**
```bash
cp -r pdf-vector-layout ~/.claude/skills/
```

### 方法 2：使用安装脚本

```bash
# 安装到 Codex
./install.sh codex

# 安装到 Claude
./install.sh claude

# 同时安装到两者
./install.sh both
```

## 验证安装

安装后，在 Codex 或 Claude Code 中运行：

```
请帮我移动 PDF 中的图到页面下方，保持矢量可编辑
```

如果 skill 正确安装，agent 会自动触发 `pdf-vector-layout` skill。

## 文件清单

```
pdf-vector-layout/
├── SKILL.md                              # 主文档（触发条件、工作流、经验）
├── README.md                             # 使用说明
├── scripts/
│   ├── move_pdf_region.py                # 移动 PDF 区域
│   ├── merge_pdf_pages.py                # 合并多个 PDF
│   └── verify_vector.py                  # 验证矢量完整性
└── references/
    ├── nature_style_checklist.md         # Nature 期刊排版规范
    └── debugging_verification.md         # 调试与验证方法
```

## 依赖

### Python 包
```bash
pip install pypdf pdfrw reportlab pikepdf pillow
```

### 系统工具（Poppler）
- **Windows**: `scoop install poppler` 或 `choco install poppler`
- **Linux**: `apt install poppler-utils`
- **macOS**: `brew install poppler`

## 使用场景

- 移动 PDF 中的图形到页面其他位置（保持矢量）
- 拼接多个 PDF 成复合图（多 panel 论文插图）
- 调整 panel 间距、标题间距
- 隐藏源 PDF 的 panel 字母，避免冲突
- 让图达到 Nature/Science/Cell 排版质量
- 导出 PDF + SVG + PNG

## 核心原则

**永远不要栅格化用户要求保持可编辑的内容。**

所有操作都在 PDF 内容流级别完成，保持矢量完整性。

## 来源

这个 skill 提炼自两个真实 Codex session：
1. **移动 PDF 到 pdf 页下**：将湿实验相关_副本.pdf 中的图移到页面下半部分
2. **修正 v8/v16 图文排版**：修复多 panel 复合图的布局

包含了大量实战经验：
- 如何避免裁切（"g 被裁断了"）
- 如何处理重复 label（两套 panel 字母）
- 如何调整间距（"再紧凑一点"）
- 如何定位问题（局部截图、bbox 扫描、坐标转换）
- 如何达到 Nature 期刊排版质量

## 许可

可自由使用和修改。

## 反馈

如有问题或建议，欢迎反馈。

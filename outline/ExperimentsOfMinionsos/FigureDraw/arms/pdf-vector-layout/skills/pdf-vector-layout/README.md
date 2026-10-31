# PDF Vector Layout Skill

通用的 PDF 矢量排版与多文档融合 skill，适用于 Claude Code 和 Codex。

## 这个 skill 解决什么问题

当你需要：
- 将 PDF 中的图形元素移动到页面的其他位置（保持矢量可编辑）
- 将多个 PDF 的内容拼接成一个复合图（例如多 panel 的科研论文插图）
- 调整 panel 之间的间距、标题与图的间距
- 隐藏源 PDF 中的 panel 字母，避免与目标 PDF 的字母冲突
- 让图达到 Nature/Science/Cell 子刊的排版质量
- 导出 PDF + SVG + PNG，全程保持矢量

**核心原则：永远不要栅格化用户要求保持可编辑的内容。**

## 来源

这个 skill 提炼自两个真实 session：
1. **移动 PDF 到 pdf 页下**：将湿实验相关_副本.pdf 中的 E/F/G/H/I 图移到页面下半部分
2. **修正 v8/v16 图文排版**：修复多 panel 复合图的布局，避免裁切、处理重复 label、紧凑间距

两个任务一开始都失败了，因为 agent 用了截图拼接；成功是在改用 PDF 内容流级别的操作之后。

## 文件结构

```
pdf-vector-layout/
├── SKILL.md                          # 主文档：触发条件、决策树、工作流、经验教训
├── scripts/
│   ├── move_pdf_region.py            # 移动单个 PDF 页面的某个区域
│   ├── merge_pdf_pages.py            # 合并多个 PDF，支持矢量白色遮罩
│   └── verify_vector.py              # 验证生成的 PDF 是否保持矢量完整性
└── references/
    ├── nature_style_checklist.md     # Nature/Science/Cell 排版规范速查表
    └── debugging_verification.md     # 调试与验证方法：如何定位问题、如何验证正确性
```

## 快速开始

### 1. 移动 PDF 中的某个区域

```bash
# 1. 渲染源 PDF 为 PNG，测量要移动的区域
pdftocairo -png -r 150 source.pdf preview

# 2. 编辑 scripts/move_pdf_region.py 中的配置
#    - INPUT_PDF, OUTPUT_PDF
#    - REGION_BOTTOM, REGION_TOP (要移动的区域，PDF 点坐标)
#    - SHIFT_Y (移动距离，负数=向下，正数=向上)

# 3. 运行脚本
python scripts/move_pdf_region.py

# 4. 验证
python scripts/verify_vector.py output_shifted.pdf
```

### 2. 合并多个 PDF（例如拼接复合图）

```bash
# 1. 渲染两个 PDF 为 PNG，测量源区域和目标位置
pdftocairo -png -r 150 composite_base.pdf preview_base
pdftocairo -png -r 150 source_row.pdf preview_source

# 2. 编辑 scripts/merge_pdf_pages.py 中的配置
#    - COMPOSITE_PDF, SOURCE_PDF, OUTPUT_PDF
#    - SOURCE_REGION_* (源 PDF 中要提取的区域)
#    - DEST_X, DEST_Y (目标位置)
#    - MASKS (如果需要隐藏源 PDF 的 panel 字母)

# 3. 运行脚本
python scripts/merge_pdf_pages.py

# 4. 验证
python scripts/verify_vector.py composite_final.pdf --expected-labels f g h i j
```

### 3. 导出 SVG 和 PNG

```bash
# SVG
pdftocairo -svg output.pdf output.svg

# PNG (300 DPI，适合论文投稿)
pdftocairo -png -r 300 output.pdf output
```

## 核心经验

### 决策树：选择哪个库

```
需要保持矢量？
  ├─ 否 → 用通用 pdf skill，截图拼接也可以
  └─ 是
      ├─ 单个源，只做平移/裁切/缩放？
      │   └─ 是 → pypdf (PageObject.add_transformation, mediabox/cropbox)
      └─ 否（多源 OR 叠加 OR 子区域粘贴）
          ├─ 需要像素级精确控制 OR 子矩形裁切 OR 矢量白色遮罩？
          │   └─ 是 → pdfrw + reportlab (Form XObject + canvas.doForm)
          └─ 否，页面级粘贴就够了
              └─ pypdf (PageObject.merge_translated_page)
```

**经验法则：从 `pypdf` 开始。只有在 `pypdf` 无法表达你的需求时，才升级到 `pdfrw + reportlab`。**

### 常见失败模式（来自真实 session）

1. **"g 被裁断了"** — 裁切框设得太紧，最高点上方要留 4–6 pt 安全边距
2. **两套 panel 字母都可见** — 源 PDF 有 `e/f/g/h/i`，目标 PDF 有 `f/g/h/i/j`，需要用矢量白色矩形遮住源的字母
3. **标题与图的间距太松** — 默认 12–15 pt，用户说"再紧凑一点"，改成 6–8 pt
4. **输出 PDF 是空白的** — 脚本退出 0 但没真正写入，或者内容被放到了画布外（Form BBox 原点不在 (0,0)）
5. **文件太大（> 10 MB）** — 不小心嵌入了栅格图

### 验证循环（每一步都要做）

1. **渲染为 PNG** — `pdftocairo -png -r 150 output.pdf preview`
2. **目视检查** — 有没有裁切、重复 label、错误间距、空白区域
3. **验证矢量完整性** — `pdftotext output.pdf -` 能提取文字，文件大小 50 KB–2 MB

**如果任何一步失败，停下来修复，不要继续叠加操作。**

### Nature/Science/Cell 排版要点

- **Panel 字母**：小写加粗无衬线（Helvetica/Arial），8–9 pt，放在 panel 左上角外侧
- **轴标签**：7 pt 无衬线，正体（数学符号除外）
- **刻度标签**：7 pt（密集轴可降到 6 pt）
- **标题与图的间距**：6–10 pt（默认 8 pt）
- **Panel 之间的间距**：水平 8–12 pt，垂直 10–15 pt
- **线宽**：轴 0.5 pt，数据线 0.75–1.0 pt（matplotlib 默认 1.5 pt 太粗）
- **字体**：Helvetica 优先，避免 DejaVu Sans（matplotlib 默认，一眼能看出是草稿）

详见 `references/nature_style_checklist.md`。

### 调试方法

- **定位内容边界**：渲染为 PNG，用 PIL 扫描非白色像素，得到 bbox
- **像素坐标转 PDF 点**：`y_pt = H * (1 - y_px / img_height_px)`
- **检查 Form BBox**：`pdfrw` 读取 Form 的 `BBox`，底边不一定是 0
- **对比前后版本**：`compare before.png after.png diff.png`（ImageMagick）

详见 `references/debugging_verification.md`。

## 依赖

### Python 包
```bash
pip install pikepdf pillow
# 或用 uv
uv pip install pikepdf pillow
```

`pypdf` / `pdfrw` / `reportlab` 不再是 move/merge 工作流的必需依赖 —— 它们是
旧版本的痕迹，新脚本完全用 pikepdf 在内容流层面做操作（保证文本层不被重复）。
如果你要继承 reportlab 的 figure-builder 模式 (`canvas.doForm`)，仍然可以并存
安装。

### 系统工具（Poppler）
- **Windows**: `scoop install poppler` 或 `choco install poppler`
- **Linux**: `apt install poppler-utils`
- **macOS**: `brew install poppler`

提供 `pdftocairo`, `pdftoppm`, `pdftotext` 等命令（仅用于预览和验证，不参与矢量操作）。

## 使用场景

### 适合用这个 skill
- 移动 PDF 中的图形到页面下方，保持矢量
- 拼接多个 PDF 成复合图（多 panel 论文插图）
- 调整 panel 间距、标题间距
- 隐藏源 PDF 的 panel 字母，避免冲突
- 让图达到 Nature/Science/Cell 排版质量
- 导出 PDF + SVG + PNG

### 不适合用这个 skill
- 纯文本提取（用通用 pdf skill）
- 从空白画布创建 PDF（用 reportlab 或通用 pdf skill）
- 纯栅格图像生成（用 imagegen skill）

## 最终答案规范

完成任务后，告诉用户三件事：
1. 输出路径（PDF，以及 SVG/PNG 如果有）
2. 验证了什么（渲染预览、文字可选、文件大小、panel 字母正确、无裁切）
3. 做了什么妥协（例如"标题下方用了 8 pt 间距，如果要更紧可以告诉我"）

**不要粘贴大段代码。** 用户说过：
> *少写代码，你可以写一点脚本进去，但是排版与多 pdf 矢量融合与微调等在里面做的事情是很宝贵的*

判断力（坐标规划、BBox 意识、矢量遮罩、label 仲裁、期刊风格排版选择）才是价值，样板代码不是。

## 示例

### 示例 1：移动湿实验图到页面下方

```python
# 配置
INPUT_PDF = Path("湿实验相关_副本.pdf")
OUTPUT_PDF = Path("湿实验_下移版.pdf")
REGION_BOTTOM = 503.6  # 从渲染 PNG 测量得到
REGION_TOP = 640.3
SHIFT_Y = -353.6  # 移到 y=150 附近

# 运行
python scripts/move_pdf_region.py

# 验证
python scripts/verify_vector.py 湿实验_下移版.pdf
pdftocairo -png -r 150 湿实验_下移版.pdf preview
```

### 示例 2：拼接 v16 复合图

```python
# 配置
COMPOSITE_PDF = Path("figureX_v16_base.pdf")  # 上半部分 + 标题行
SOURCE_PDF = Path("湿实验_下移版.pdf")
OUTPUT_PDF = Path("figureX_v16_final.pdf")
SOURCE_REGION_BOTTOM = 150.0
SOURCE_REGION_TOP = 400.0
DEST_Y = 50.0
# 遮住源 PDF 的 e/f/g/h/i 字母（y ≥ 424），不要盖到目标 PDF 的 f/g/h/i/j
MASKS = [(0, 424, 595.28, 30)]

# 运行
python scripts/merge_pdf_pages.py

# 验证
python scripts/verify_vector.py figureX_v16_final.pdf --expected-labels f g h i j
pdftocairo -png -r 150 figureX_v16_final.pdf preview

# 导出 SVG 和 PNG
pdftocairo -svg figureX_v16_final.pdf figureX_v16.svg
pdftocairo -png -r 300 figureX_v16_final.pdf figureX_v16
```

## 许可

这个 skill 是从真实 session 中提炼的经验，可以自由使用和修改。

## 反馈

如果你发现这个 skill 有问题或者有改进建议，欢迎提 issue。

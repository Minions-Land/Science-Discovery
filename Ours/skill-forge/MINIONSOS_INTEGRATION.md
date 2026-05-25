# skill-forge — Skill 自进化系统

**位置:** `minions/roles/common/skills/skill-forge/`
**版本:** 1.0.0
**创建日期:** 2026-05-21

---

## 为什么需要 skill-forge？

MinionsOS 中每个 skill 都不是一次性创作完就定型的。**Skill 本身**会在使用中暴露弱点（触发不准、行为不到位、描述含糊），需要持续进化。skill-forge 是这个进化循环的基础设施 —— 每个 skill 沿着 6 阶段生命周期成长，从粗糙草稿到成熟工具，再迭代到下一代。

### 没有 skill-forge 时，skill 进化是停滞的

**传统的 skill 创建流程：**
1. 手写 SKILL.md
2. 凭感觉测试几次
3. 没有量化指标
4. 没有触发准确率优化
5. 一旦写完，几乎不再演化

**结果：**
- skill 质量参差不齐，没有统一的成熟度衡量
- 一旦发布，缺陷难以系统性修复
- 整个 skill 库无法作为整体演进
- 同样的 skill 设计错误反复出现

### skill-forge 让每个 skill 都能持续进化

**6 阶段生命周期（每个 skill 都走一遍）：**

```
Stage 0: Intake & Scoping
  └─ 理解需求，选择模式（创建/改进/验证/打包）

Stage 1: Creation
  └─ 研究类似 skills，起草 SKILL.md，编写测试用例

Stage 2: Form Validation
  └─ 结构验证（quick_validate.py + skill-edit）

Stage 3: Behavioral Validation
  ├─ Option A: skill-evaluator（深度测试）
  └─ Option B: 官方 eval pipeline（基准测试）

Stage 4: Iteration
  └─ 使用 eval sets 进行爬山优化（60% 训练 + 40% 验证）

Stage 5: Description Optimization
  └─ 20 条测试 query，5 轮优化，最大化触发准确率

Stage 6: Packaging
  └─ 打包成 .skill 文件，生成安装说明
```

**关键点：每个阶段都让 skill 本身变得更成熟，而不是改变使用 skill 的角色。**

---

## Skill 进化循环

主体是 **skill 本身**，不是某个专家。任何角色（Gru、Noter、Writer、Ethics、Expert）使用 skill 时遇到问题，都触发同一个进化路径：

```
┌─────────────────────────────────────────────────────────┐
│            一个 skill 被构思（用户或角色提出需求）         │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│        Stage 1 → 2 → 3 → 5 → 6（首次出生周期）            │
│        skill 从草稿 → 形式合格 → 行为验证 → 触发优化       │
│        → 打包成可用工具                                    │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              skill 进入 MinionsOS 生产                     │
│              （被各个角色调用）                              │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│       使用中暴露弱点：触发不准 / 效果不到位 / 描述歧义       │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│        Stage 4（爬山迭代）或 Stage 5（描述优化）           │
│        skill 进化到下一代                                   │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│     改进版 skill 替换旧版本，循环继续 —— skill 越来越好     │
└─────────────────────────────────────────────────────────┘
```

每个 skill 在 MinionsOS 中都不是静止的工具，而是一个不断进化的生命周期对象。

---

## 在 MinionsOS 中的应用场景

主语始终是 **skill**：

### 场景 1：新 skill 从草稿到上线

```
某个能力缺口被识别 → 一个新 skill 被构思

skill-forge 推动这个 skill 经历：
  Stage 1: 研究类似 skills，起草 SKILL.md
  Stage 2: 结构验证（form 干净）
  Stage 3: 行为验证（确实改变 agent 行为）
  Stage 5: 描述优化（触发准确率 F1 > 0.9）
  Stage 6: 打包

结果：一个成熟的 skill 进入 MinionsOS 生产，可被任何角色调用。
```

### 场景 2：已上线 skill 的迭代进化

```
一个生产中的 skill 暴露问题
（例如 editorial-html 在用户说「生成报告」时不触发）

skill-forge 推动这个 skill 进化：
  Stage 5: 生成 20 条测试 query（10 正例 + 10 负例）
          5 轮优化循环
          选择 F1 分数最高的 description

结果：skill 进化到下一代，触发准确率从 0.7 提升到 0.92。
旧版本被替换。
```

### 场景 3：skill 进入生产前的质量门槛

```
一个候选 skill 等待加入 MinionsOS skill 库

skill-forge 推动它通过质量验证：
  Stage 2: 形式验证（结构、frontmatter、触发短语）
  Stage 3: 行为验证（A/B 测试，Codex 盲评）
  生成量化报告（通过率、token 效率、耗时）

结果：只有量化指标合格的 skill 才能上线。整个 skill 库的质量上限被托起。
```

---

## 工具整合

skill-forge 整合了三套工具：

### 1. 你的自定义工具
- **skill-edit** (150 行) — 形式验证
- **skill-evaluator** (215 行) — 行为验证（3 阶段）
- **codex** — 子代理调度

### 2. 官方 skill-creator 工具
- `init_skill.py` — 模板化创建
- `quick_validate.py` — 快速验证
- `run_eval.py` — 并行 A/B 测试
- `improve_description.py` — 描述优化
- `aggregate_benchmark.py` — 基准汇总
- `package_skill.py` — 打包

### 3. 评估代理
- **grader** — 评估断言是否通过
- **comparator** — 盲评两个输出
- **analyzer** — 分析为什么一个版本更好

---

## 量化指标 —— skill 成熟度的衡量

每个 skill 都会被量化打分，让进化方向可见：

### 形式指标（Stage 2）—— skill 是否结构合格
- ✅ Frontmatter 有效性
- ✅ Description < 500 字符
- ✅ 触发短语与 description 匹配
- ✅ 步骤顺序正确
- ✅ 无前向引用

### 行为指标（Stage 3）—— skill 是否真的改变行为
- **通过率** — 测试用例通过百分比
- **Token 效率** — with_skill vs baseline token 消耗
- **耗时** — with_skill vs baseline 执行时间
- **行为分类** — Prevents failure / Calibrates / Matches baseline / Overreaches

### 触发指标（Stage 5）—— skill 是否在该用时被用
- **Precision** — 应该触发时触发的比例
- **Recall** — 不该触发时不触发的比例
- **F1 Score** — 调和平均（成熟 skill 目标 > 0.9）

skill 的进化历程可以追踪：每一代相对上一代在哪些指标上得分提升。

---

## 与 MinionsOS 其他组件的关系

### 与 EACN (Expert Agent Collaboration Network) 的关系
- skill-forge 进化出的 skills 进入 common skill 库后，所有 EACN 角色都能调用
- 没有 skill-forge 时：每个角色靠手写 skill，质量不可控
- 有 skill-forge 后：skill 库本身在持续进化，整个 EACN 网络间接受益

### 与角色系统的关系
- **Common skills** — 所有角色共享（如 skill-forge 本身）
- **角色专属 skills** — 特定角色的能力（如 Noter 的论文处理）
- 两类都走 skill-forge 生命周期 —— 主体是 skill，不是角色

### 与工作流的关系
- skill 一旦进入生产，就成为工作流的可重用零件
- skill-forge 保证零件持续打磨，工作流的可靠性同步提升

---

## 文件结构

```
minions/roles/common/skills/skill-forge/
├── SKILL.md                      # 主逻辑（404 行）
├── README.md                     # 架构文档
├── REGISTRATION.md               # CLAUDE.md 注册条目 + 图表
├── SUMMARY.md                    # 执行摘要
├── TOOL_INVENTORY.md             # 工具清单
└── MINIONSOS_INTEGRATION.md      # 本文档
```

---

## 下一步

### 短期（1-2 周）
1. ✅ 将 skill-forge 集成到 MinionsOS common skills
2. ✅ 创建示例 skill（json-format）
3. ⏳ 选 3-5 个现有 skill 跑完整生命周期，建立成熟度基线
4. ⏳ 编写完整的测试用例（evals.json）

### 中期（1 个月）
1. 运行 Stage 3 行为验证，收集每个 skill 的基准数据
2. 运行 Stage 5 描述优化，提升整个 skill 库的触发准确率
3. 建立 skill 成熟度标准（通过率 > 80%，F1 > 0.9）
4. skill 进化版本可追溯（每个 skill 有 generation 字段）

### 长期（3 个月）
1. 自动化 skill 进化循环（skill 在生产中暴露弱点 → 自动触发 Stage 4/5 → 改进版替换）
2. skill 跨代质量曲线可视化（每个 skill 的成熟度趋势）
3. 跨项目 skill 迁移（成熟 skills 在不同 MinionsOS 项目间复用）
4. skill 版本管理和回滚机制

---

## 关键指标

- **Skill 创建周期**（首次出生）：< 10 分钟（vs 之前 1-2 小时手工）
- **Skill 形式合格率**：100%（所有进入生产的 skill 通过 Stage 2）
- **Skill 触发成熟度**：目标 F1 > 0.9（经过 Stage 5 优化）
- **Skill 库整体进化速度**：每月 3-5 个 skill 进入下一代

---

**skill-forge 让每个 skill 在 MinionsOS 中都成为一个持续进化的生命周期对象，而不是一次性的静态工具。**

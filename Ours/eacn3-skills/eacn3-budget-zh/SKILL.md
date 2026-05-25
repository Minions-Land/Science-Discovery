---
name: eacn3-budget-zh
description: "处理预算确认请求 — 批准或拒绝超出任务预算的竞标"
---

# /eacn3-budget — 预算确认

竞标者的价格超出了你的任务预算。你需要决定：批准（可选增加预算）或拒绝。

## 触发条件

- 来自 `/eacn3-bounty` 的 `bid_request_confirmation` 事件
- 事件 payload 包含：竞标者 agent_id、他们的价格、你当前的预算

## 第 1 步 — 了解情况

```
eacn3_get_task(task_id)
```

查看：
- `budget` —— 你最初设定的预算
- `remaining_budget` —— 扣除子任务划拨后的剩余
- `bids` —— 已有多少竞标者
- `max_concurrent_bidders` —— 槽位是否已满
- 竞标者的价格（来自事件 payload）

还要检查竞标者的质量：
```
eacn3_get_reputation(bidder_agent_id)
eacn3_get_agent(bidder_agent_id)
```

## 第 2 步 — 决策

向用户展示情况：

> "智能体 [名称] 对你的任务竞标了 [价格]，但你的预算是 [预算]。
> 他们的信誉是 [分数]。领域：[领域]。
> 你目前有 [N] 个其他竞标者。"

三个选项：

### 选项 A：批准并增加预算
竞标者的价格合理且他们看起来合格。增加你的预算以容纳。

先检查你是否负担得起增加：
```
eacn3_get_balance(initiator_id)
```

所需额外金额 = `new_budget - current_budget`。验证 `available ≥ 额外金额`。如果不够，告诉用户他们负担不起此增加。

```
eacn3_confirm_budget(task_id, approved=true, new_budget=<金额>, initiator_id)
```

差额从你的账户冻结到托管。

### 选项 B：按当前预算批准
接受竞标但不增加预算。竞标者接受你当前的预算作为上限。

```
eacn3_confirm_budget(task_id, approved=true, initiator_id)
```

### 选项 C：拒绝
价格太高，或竞标者不值得。

```
eacn3_confirm_budget(task_id, approved=false, initiator_id)
```

竞标被拒绝。竞标者会收到通知。

## 决策指导

| 因素 | 批准 | 拒绝 |
|------|------|------|
| 竞标者信誉高 (>0.8) | 值得为质量多付 | — |
| 已有好的竞标者 | — | 不需要另一个昂贵的 |
| 任务紧急/重要 | 支付溢价 | — |
| 价格远超预算 (>2x) | 仔细考虑 | 大概率拒绝 |
| 没有其他竞标者 | 考虑批准 | 有风险 —— 可能得不到结果 |

## 决策后

网络自动处理你的决策：
- **批准** → 竞标被接受。竞标者开始执行（如果槽位已满则进入队列）。你的预算已更新。无需进一步操作直到结果到达。
- **拒绝** → 竞标被拒绝。竞标者收到通知。槽位仍对其他竞标者开放。

下一步：
- `/eacn3-bounty` —— 继续监控更多事件（更多竞标、结果等）
- `/eacn3-dashboard` —— 查看整体任务状态
- 如果任务已运行一段时间但没有结果 → 考虑 `eacn3_update_discussions` 添加上下文，或 `eacn3_update_deadline` 延长截止时间

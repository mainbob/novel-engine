# Checker Schema

> 本文档定义"一份合格的检测规则文档"的结构规范。
> 任何放入 `generated-rules/` 目录、文件名以 `-rules.md` 或 `-checker.md` 结尾的文档，
> 都会被 Checker Agent 读取并执行。
> 只要文档符合本 schema，Agent 就能理解并执行——无论检测什么内容。

---

## 必须包含的 Section

### 1. 元信息（Frontmatter）

```yaml
---
rule_id: engagement-rules          # 唯一标识
rule_name: 读者参与度检测            # 人类可读名称
rule_type: checker                  # checker | validator | tracker
applies_to: chapter                 # chapter | volume | arc | project
trigger: always                     # always | conditional | on_demand
priority: high                      # critical | high | medium | low
version: 1.0
created_by: understanding-layer     # understanding-layer | runtime | user
scope:                              # 可选：限定生效范围
  arc: "A篇章"                      # 留空则全局生效
  chapters: "1-200"
---
```

### 2. 检测目标（Objective）

一句话说明这份规则检测什么。Agent 用这段判断是否需要对当前章节执行此规则。

```markdown
## 检测目标
检测章节的读者参与度——钩子强度、微回报密度、是否有足够理由让读者点击下一章。
```

### 3. 硬约束（Hard Constraints）

不可协商的规则。违反任何一条 → 该维度直接 FAIL，必须修复。

格式要求：
- 每条约束有唯一编号（`HARD-XXX`）
- 有严重级别（`critical` | `high`）
- 有明确的判定条件（是/否，不能模糊）
- 有失败时的处理方式

```markdown
## 硬约束

### HARD-001 [critical]
**条件**: 读者无法理解本章发生了什么（主要事件不清晰）
**判定**: 章节中是否存在至少一个可被概括的核心事件
**失败处理**: 必须重写，不可豁免

### HARD-002 [critical]
**条件**: 上一章的显性承诺在本章零回应
**判定**: 对照上一章钩子，本章是否有任何程度的回应（部分回应算通过）
**失败处理**: 必须补充回应段落
```

### 4. 软约束（Soft Constraints）

可协商的规则。违反时扣分但不直接 FAIL，可通过豁免机制绕过。

格式要求：
- 每条约束有唯一编号（`SOFT-XXX`）
- 有权重（用于评分计算）
- 有豁免条件（什么情况下可以不遵守）
- 豁免产生债务（可选）

```markdown
## 软约束

### SOFT-001 [权重: 15]
**条件**: 章末应有至少一个未解决的问题或期待锚点
**判定**: 章节最后 500 字内是否存在悬念、选择、危机或期待
**豁免条件**: 卷末总结章、大高潮收束章
**豁免债务**: 无（自然结构豁免）

### SOFT-002 [权重: 10]
**条件**: 不应连续3章使用相同类型的钩子
**判定**: 对照前2章钩子类型记录
**豁免条件**: 叙事结构要求（如追逐战跨3章）
**豁免债务**: 下一章必须切换钩子类型
```

### 5. 评分算法（Scoring）

定义如何从软约束计算总分。

```markdown
## 评分算法

**基础分**: 100
**扣分方式**: 每条软约束违反，扣除该条权重值
**最终分**: max(0, 基础分 - 总扣分)

**等级判定**:
- 85+: PASS
- 70-84: PASS_WITH_WARNINGS
- 50-69: CONDITIONAL（需豁免契约）
- <50: FAIL
```

### 6. 输出格式（Output Format）

Checker Agent 执行后输出的报告结构。

```markdown
## 输出格式

```json
{
  "rule_id": "engagement-rules",
  "chapter": 15,
  "hard_violations": [
    { "id": "HARD-001", "severity": "critical", "detail": "..." }
  ],
  "soft_violations": [
    { "id": "SOFT-002", "severity": "medium", "detail": "...", "override_eligible": true }
  ],
  "score": 78,
  "grade": "PASS_WITH_WARNINGS",
  "suggestions": ["..."],
  "data_for_state": { }
}
```
```

---

## 可选 Section

### 7. 依赖数据（Required Data）

声明执行此规则需要从 state 或其他来源读取什么数据。

```markdown
## 依赖数据
- `state.json → chapter_meta` (上一章钩子类型)
- `character-cards/*.json` (角色当前知识边界)
- `blueprint.json → narrative_structure` (当前篇章信息)
```

### 8. 状态写回（State Updates）

声明检测完成后需要向 state 写入什么数据（供后续章节使用）。

```markdown
## 状态写回
- 更新 `state.json → chapter_meta[{chapter}].hook_type`
- 更新 `state.json → chapter_meta[{chapter}].engagement_score`
```

### 9. 关联规则（Related Rules）

声明与其他规则的依赖或互斥关系。

```markdown
## 关联规则
- 依赖: pacing-rules（需要节奏线分类结果）
- 互补: consistency-rules（一致性检测覆盖事实层面，本规则覆盖体验层面）
```

---

## Schema 总结

一份合格的 checker 文档 = 元信息 + 检测目标 + 硬约束 + 软约束 + 评分算法 + 输出格式。
可选补充：依赖数据、状态写回、关联规则。
符合此结构的任何 MD 文档都可以被 Checker Agent 读取并执行。

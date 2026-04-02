---
rule_id: default-ooc-rules
rule_name: OOC检测（默认）
rule_type: checker
applies_to: chapter
trigger: always
priority: high
version: 1.0
created_by: default-template
---

# OOC (Out-Of-Character) 检测

## 检测目标

检测角色行为是否符合其已建立的性格、动机和行为模式。

## 三级分类

| 级别 | 定义 | 处理 |
|------|------|------|
| minor | 行为微偏但有合理世界内解释 | 记录，不扣分 |
| moderate | 行为缺乏充分铺垫或解释 | 扣分，建议补充铺垫 |
| severe | 行为完全违背已建立特征，无解释 | FAIL |

## 硬约束

### HARD-001 [critical]
**条件**: 角色行为完全违背 behavior_rules 且无任何铺垫
**判定**: 对照角色卡 behavior_rules 列表

### HARD-002 [high]
**条件**: 反派智商突然下降只为服务剧情
**判定**: 反派行为是否在其 behavioral_pattern 框架内

## 软约束

### SOFT-001 [权重: 15]
**条件**: 角色语言风格偏离（对照 speech_examples）

### SOFT-002 [权重: 10]
**条件**: 角色习惯动作消失或不一致

### SOFT-003 [权重: 15]
**条件**: 角色决策逻辑与信息边界不一致（角色做出了他不该知道的信息才能做的决定）

## 合理成长 vs OOC

**合理成长条件**:
- 有渐进的触发事件
- 有叙事铺垫
- 与催化事件逻辑一致

不满足以上条件的突然性格转变 = OOC 违反。

## 评分算法

**基础分**: 100
**等级**: 85+ PASS / 70-84 WARNINGS / <70 FAIL

## 依赖数据

- `character-cards/*.json`（behavior_rules, masks, speech_examples, habits）
- `state.json → facts`（近期事件，判断是否有触发变化的事件）

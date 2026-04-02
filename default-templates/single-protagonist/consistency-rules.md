---
rule_id: default-consistency-rules
rule_name: 一致性检测（默认）
rule_type: checker
applies_to: chapter
trigger: always
priority: critical
version: 1.0
created_by: default-template
---

# 一致性检测（默认规则）

## 检测目标

检测章节与已有设定/状态的一致性——战力、地点、时间线、角色属性。

## 硬约束

### HARD-001 [critical]
**条件**: 角色能力超出当前战力上限
**判定**: 对照角色卡 power_level，行为是否超出设定

### HARD-002 [critical]
**条件**: 角色出现在不可能的位置（未解释的瞬移）
**判定**: 对照上一章位置和时间推进

### HARD-003 [critical]
**条件**: 时间线回退或倒计时跳跃
**判定**: 对照 state 中的时间标记

### HARD-004 [high]
**条件**: 未注册的新实体出现（重要角色/地点凭空出现）
**判定**: 角色/地点未在设定文档或角色卡中出现

## 软约束

### SOFT-001 [权重: 10]
**条件**: 角色外貌/习惯描述与角色卡不一致

### SOFT-002 [权重: 10]
**条件**: 灵力属性/战斗风格描述与设定不一致

### SOFT-003 [权重: 5]
**条件**: 时间推进不自然（一章内跨越过长时间无说明）

## 评分算法

**基础分**: 100
**等级**: 85+ PASS / 70-84 WARNINGS / <70 FAIL

## 依赖数据

- `character-cards/*.json`
- `state.json → facts`
- `state.json → chapter_meta`（位置和时间）

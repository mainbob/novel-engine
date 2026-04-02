---
rule_id: default-continuity-rules
rule_name: 连续性检测（默认）
rule_type: checker
applies_to: chapter
trigger: always
priority: high
version: 1.0
created_by: default-template
---

# 连续性检测

## 检测目标

检测章节之间的叙事连续性——场景转换、剧情线追踪、伏笔管理、逻辑流。

## 硬约束

### HARD-001 [critical]
**条件**: 场景转换无任何过渡标记（时间/空间完全断裂）
**判定**: 章首场景与上章末尾无逻辑连接

### HARD-002 [high]
**条件**: 重要剧情线消失超过安全间隔（15章）
**判定**: 对照 state.json → hooks 中 status=planted 的钩子

### HARD-003 [high]
**条件**: 重大逻辑矛盾（因果链断裂）
**判定**: 结果发生但缺少必要的原因

## 软约束

### SOFT-001 [权重: 15]
**条件**: 场景转换流畅度低于B级
**评级**: A(自然) B(可接受) C(生硬) F(断裂)

### SOFT-002 [权重: 10]
**条件**: 中期伏笔（4-10章）超过安全间隔未推进

### SOFT-003 [权重: 10]
**条件**: 冗余描写或重复场景模式拖慢节奏

### SOFT-004 [权重: 10]
**条件**: 大纲偏离（章节内容与大纲定义有偏差）
**评级**: minor(可接受) moderate(需标注) major(需记录偏差原因)

## 评分算法

**基础分**: 100
**等级**: 85+ PASS / 70-84 WARNINGS / <70 FAIL

## 依赖数据

- `state.json → hooks`（钩子状态和计时）
- `state.json → chapter_meta`（上一章的场景和状态）
- `outline/chapters/chapter-{N}.md`（大纲对照）

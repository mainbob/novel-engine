# Outline Schema

> 本文档定义大纲文档的结构规范。
> 大纲由 `/novel-outline` 的人机协作过程产出，存储在 `{project}/outline/` 目录。
> Context Agent 在组装执行包时读取大纲。

---

## 层级结构

```
outline/
├── master-outline.md          # 总纲（全书级）
├── arc-A.md                   # 篇章级大纲
├── arc-D.md                   # 篇章级大纲
├── volume-A-1.md              # 卷级大纲（可选细分）
└── chapters/
    ├── chapter-001.md          # 章节级大纲
    ├── chapter-002.md
    └── ...
```

---

## 总纲（Master Outline）

```markdown
# 《书名》总纲

## 核心设定
[一段话概括故事核心——从 blueprint 中提取]

## 篇章结构
| 篇章 | 章节范围 | 字数预估 | 节奏风格 | POV角色 |
|------|---------|---------|---------|---------|

## 全书弧线
[情节弧线的宏观走向——起承转合的关键转折点]

## 终局设定
[结局的核心要素——确保全书走向一致]
```

---

## 篇章级大纲（Arc Outline）

```markdown
# A篇章大纲

## 篇章定位
[本篇章在全书中的角色——如"一部完整的独立小说"]

## 幕结构
| 幕 | 章节范围 | 核心事件 | 情绪走向 |
|----|---------|---------|---------|

## 节拍表（Beat Sheet）
1. **开篇承诺**: [第一个钩子]
2. **递进危机 1**: [...]
3. **递进危机 2**: [...]
4. **递进危机 3**: [...]
5. **中点反转**: [必填——不可为空]
6. **最低点**: [...]
7. **高潮**: [...]
8. **新钩子**: [指向下一篇章或收束]

## 时间轴
[统一时间坐标系]
```

---

## 章节级大纲（Chapter Outline）

每章大纲是一个结构化文档。必须字段和可选字段如下：

### 必须字段

```markdown
---
chapter: 15
arc: A篇章
pov: char_a
word_target: [2800, 3200]
scene_tags: [has_dialogue, emotional_beat, internal_turmoil]   # Context Agent craft 选择用
chapter_type: reinforcement                                     # opening | reinforcement | shatter | pattern-anchor | mirror | signature-line | pov-switch
---

## 目标
[本章要完成什么——≤30字]

## 冲突
[本章的核心矛盾——≤30字]

## 状态变更
[本章结束后世界/角色发生了什么变化]
- 沈渊：突破到结丹巅峰
- 世界异常：灵矿灵气流向偏移（伏笔）

## 钩子
**承接**: [回应上一章的什么钩子]
**种下**: [本章末尾留下什么钩子]

## 验收标准（acceptance_criteria）
> 交给 Verification Agent 逐条勾选的"本章是否交付"清单。
> 每条必须是可由读章节正文直接判定的二元命题（是/否），不是主观评价。

- [ ] A: 某个具体情节动作已发生（例：沈渊在南郊挖出一件物品并带回）
- [ ] B: 某个视角人物的知识边界有具体变化（例：沈渊确认浣花笺寄件人身份）
- [ ] C: 某个具体钩子被种下（例：挑夫队第七人被记住）
- [ ] D: 某个具体钩子被回应（例：ch0 章末『备马南郊』的指令被落地）

## 硬约束（hard_constraints）
> 不得违反的本章专属红线。每条是通用 Verifier 可扫描的结构化断言。

- forbidden_names: []                  # 本章绝对不得出现的名字（含代称）
- forbidden_facts: []                  # 本章不得泄露给读者的事实 id（来自 state.facts）
- required_signature_lines: []         # 本章必须出现的签名台词 id（若有）
- flashback_budget_chars: 0            # 闪回字数硬上限
- flashback_visual_anchors_allowed: [] # 本章允许的闪回视觉锚（白名单）
- dialogue_marker_max: 3               # "说/道" 上限
- must_fire_habits: []                 # 本章必须触发的 habit id（覆盖 character-card 默认值，可为空）
- pov_lock: char_a                     # 全程 POV 锁定
- custom_rules: []                     # 其他一次性硬约束（自由文本，但每条必须独立可判）
```

### 可选字段（由理解层根据 blueprint 决定生成哪些）

```markdown
## 节奏线归属
[复仇推进线 / B信任深化线 / ...]

## 信息差变化
[本章中谁的知识边界发生了变化]
- A: 新增误判证据①
- 读者: 与A同步

## 隐层意义
[本章表面讲的是什么，实际在推进什么]
- 表层：沈渊成功夺取灵矿
- 隐层：陆衍借此机会嫁接资源人脉到暗线

## 模式锚点
[如果本章是某个行为模式的锚点]
- 锚点 ID: anchor_2
- 表面呈现: B瓦解C盟友——B很聪明
- 回看含义: 和D篇章的操作手法一样

## 爽感/满足感设计
[本章的参与度设计]
- 类型: 信息差碾压
- 铺垫: 对手轻视沈渊
- 交付: 沈渊利用前世地形知识反杀
- 隐层: 这个"爽"加深了A对自身判断力的过度自信

## 时间标记
- 时间锚点: 重生后第3个月
- 距上章: 5天
- 倒计时: 无
```

---

## Schema 规则

1. 总纲和篇章大纲由 `/novel-outline` 的共创过程产出
2. 章节大纲的必须字段（目标、冲突、状态变更、钩子、验收标准、硬约束）适用于所有项目
6. `acceptance_criteria` 是 Verifier 的一等验收输入——每条必须可在正文中独立判定为 PASS/FAIL，不得出现"流畅"、"动人"、"克制"等主观描述
7. `hard_constraints` 中的结构化字段由 Verifier 通用扫描；`custom_rules` 作为自由文本逃生舱，但代价是每条由 Verifier 用 LLM 判断而非机械扫描
3. 可选字段由理解层在生成 blueprint 时决定——blueprint 中定义了信息差追踪，则章节大纲自动包含"信息差变化"字段
4. 章节大纲可以由系统自动生成，也可以由用户手动编写或修改
5. Context Agent 读取章节大纲时，如果某个可选字段不存在，直接跳过（不报错）

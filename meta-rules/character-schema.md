# Character Card Schema

> 本文档定义"一张合格的角色卡"的结构规范。
> 角色卡存储在 `{project}/character-cards/` 目录下，每个角色一个 JSON 文件。
> Context Agent 在组装创作执行包时读取角色卡，决定注入哪些信息。
> OOC Checker 在审查时读取角色卡，检查行为是否一致。

---

## 必须字段

```jsonc
{
  // === 身份 ===
  "id": "char_a",                        // 唯一标识符
  "name": "沈渊",                         // 角色名
  "aliases": ["渊哥"],                    // 别名/称呼
  "role": "protagonist",                  // protagonist | antagonist | supporting | functional | misdirection
  "pov": true,                           // 是否是视角人物（可有多个 true）

  // === 当前状态（每章更新）===
  "current_state": {
    "chapter": 45,                        // 最后更新的章节
    "status": "alive",                    // alive | dead | unknown | transformed
    "location": "云陵城",
    "power_level": {
      "apparent": null,                   // 表面战力（无伪装时为 null）
      "real": "结丹巅峰-60%"              // 真实战力
    },
    "physical": "健康",                   // 身体状态
    "emotional": "多疑、焦虑",            // 情绪状态
    "active_goals": ["追杀姜远", "崛起"]   // 当前目标
  },

  // === 行为规则（固定，由理解层生成）===
  "behavior_rules": [
    "精准打击而非大规模屠杀",
    "对无辜者有底线",
    "信息环境中的每个决策对读者来说都必须合理"
  ],

  // === 知识边界（核心——每章更新）===
  "knowledge": {
    "knows": [
      "前世被姜远（误认为）背叛",
      "灵矿位置和秘境信息（前世记忆）"
    ],
    "does_not_know": [
      "真凶是陆衍",
      "证据是陆衍伪造的"
    ],
    "false_beliefs": [
      "姜远是仇敌"
    ],
    "suspicions": []                      // 怀疑但未确认的信息
  }
}
```

## 可选字段（由理解层根据叙事需要决定是否生成）

```jsonc
{
  // === 面具系统（如 B·陆衍）===
  "masks": [
    {
      "context": "对沈渊",
      "persona": "绝对顺从的狂热崇拜者",
      "speech_style": "语速偏快，带紧张和热切",
      "behavior": "A的任何计划从不质疑"
    },
    {
      "context": "对下属",
      "persona": "有恩有威的领袖",
      "speech_style": "沉稳从容，偶尔幽默",
      "behavior": "关怀是表演但极好"
    }
  ],

  // === 行为模式（如 B 的固定模式）===
  "behavioral_pattern": {
    "description": "寄生→构陷盟友→收割→清理知情者→亲自补刀",
    "anchors": [
      {
        "id": "anchor_1",
        "chapter_range": "A篇章早期",
        "surface_meaning": "B很能干",
        "hidden_meaning": "B一直用同一套模式",
        "status": "pending"
      }
    ],
    "fatal_flaws": [
      "亲自补刀强迫症",
      "清除后手=彻底赢了的判断惯性",
      "识别盲区：只扫描有野心/仇恨/目的的人"
    ]
  },

  // === 关系网络 ===
  "relationships": [
    {
      "target": "char_b",
      "type": "trust",
      "apparent": "忠诚同谋",          // 表面关系
      "real": "被寄生的猎物",           // 真实关系（可选）
      "evolution": []                   // 关系变化记录
    }
  ],

  // === 战力时间线（非线性战力角色）===
  "power_timeline": [
    { "point": "A篇章开始", "apparent": null, "real": "筑脉巅峰-15%" },
    { "point": "A篇章结束", "apparent": null, "real": "化元巅峰~归真初期-70%" }
  ],

  // === 天赋/特殊能力 ===
  "abilities": [
    {
      "name": "脉感共振",
      "type": "innate",
      "tiers": [
        { "unlock": "筑脉", "capability": "感知地脉走向和状态" },
        { "unlock": "结丹", "capability": "感知周围空间灵力扰动" },
        { "unlock": "化元", "capability": "感知对手体内灵力调动，半息预判" }
      ],
      "limitations": ["只感知方向不感知内容", "修为差距压缩窗口", "多目标降质"]
    }
  ],

  // === 叙事透明度（视角角色专用）===
  "narrative_transparency": "half",     // full | half | opaque
  // full: 读者看到角色所有想法（传统第一人称）
  // half: 读者看到感知和情绪，看不到战略意图（如叶微）
  // opaque: 读者只看到外在行为（如陆衍）

  // === 外观/习惯（写作参考）===
  "appearance": {},
  "habits": [],
  "speech_examples": []
}
```

## Schema 规则

1. `id`、`name`、`role`、`pov`、`current_state`、`behavior_rules`、`knowledge` 是必须字段
2. `knowledge` 必须包含 `knows`、`does_not_know`、`false_beliefs` 三个数组
3. `current_state.power_level` 必须区分 `apparent` 和 `real`（无伪装时 apparent 为 null）
4. 所有可选字段由理解层根据叙事结构决定是否生成
5. `current_state` 和 `knowledge` 在每章写完后由 Data Agent 更新
6. `behavior_rules` 和 `masks` 等固定特征不随章节更新
7. Context Agent 在写某角色视角时，只能注入该角色 `knowledge.knows` 中的信息

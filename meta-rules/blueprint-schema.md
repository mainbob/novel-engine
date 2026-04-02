# Blueprint Schema

> 本文档定义创作蓝图（blueprint.json）的结构规范。
> 蓝图是整个系统的核心数据——它替代了固定模板，驱动所有 Agent 的行为。
> 蓝图由理解层（/novel-interview + /novel-blueprint）从用户创意中生成。
> 蓝图可以随时修改，修改后所有下游自动适配。

---

## blueprint.json 结构

### 必须字段

```jsonc
{
  "schema_version": "1.0",

  // === 项目基础信息 ===
  "project": {
    "title": "藏刃",
    "genre_references": ["修仙", "悬疑"],     // 参考类型（仅用于加载默认素材库）
    "target_words": 1000000,
    "chapter_word_range": [2000, 3000],
    "language": "zh",
    "platform": "起点"                         // 可选
  },

  // === 叙事结构（核心——决定系统如何运作）===
  "narrative_structure": {
    "type": "sequential-dual-pov",             // 自由文本描述，不是枚举
    "description": "两个POV角色分两个篇章，A篇章结束后A死亡，切换到D篇章",
    "pov_characters": ["char_a", "char_d"],
    "arcs": [
      {
        "id": "arc_a",
        "name": "A篇章",
        "pov": "char_a",
        "chapter_range": [1, 200],
        "tone": "标准爽文节奏，资源争夺+复仇推进",
        "word_estimate": 500000
      },
      {
        "id": "arc_d",
        "name": "D篇章",
        "pov": "char_d",
        "chapter_range": [201, 480],
        "tone": "悬念驱动，压抑与爆发交替",
        "word_estimate": 600000
      }
    ],
    "arc_transitions": [
      {
        "from": "arc_a",
        "to": "arc_d",
        "trigger": "A死亡",
        "transition_rule": "前5章保留A篇章节奏惯性，逐步过渡"
      }
    ]
  },

  // === 主题与叙事规则 ===
  "theme": {
    "core": "最危险的敌人永远是你最信任的人",
    "narrative_rules": [
      "沈渊至死不知真相",
      "B的形象完全通过A和D的眼睛呈现，无内心视角",
      "D是对读者半透明的角色——看到感知和情绪，看不到战略意图"
    ]
  },

  // === 需要生成哪些规则文档（理解层决定）===
  "required_rules": [
    "engagement-rules",
    "pacing-rules",
    "consistency-rules",
    "continuity-rules",
    "ooc-rules",
    "info-barrier-rules",          // 有信息差追踪需求时生成
    "dual-layer-rules"             // 有双层叙事时生成
  ],

  // === 需要生成哪些可选字段（影响大纲和角色卡）===
  "optional_features": {
    "knowledge_tracking": true,     // 启用知识边界追踪
    "false_belief_tracking": true,  // 启用错误认知追踪
    "mask_system": true,            // 启用面具系统
    "pattern_anchors": true,        // 启用行为模式锚点
    "dual_layer_narrative": true,   // 启用双层叙事
    "power_timeline": true,         // 启用战力时间线
    "revelation_events": true       // 启用揭示事件
  }
}
```

### 可选字段

```jsonc
{
  // === 世界设定摘要（不是完整设定文档，是结构化索引）===
  "world_summary": {
    "core_truth": "修炼是单向汲取，灵脉在不可逆枯竭",
    "power_system": {
      "type": "境界制",
      "levels": ["凝气", "筑脉", "结丹", "化元", "归真", "破境"],
      "quantification": "0-100% 连续量化"
    },
    "key_mechanics": [
      "灵气依赖——修炼不可逆，断供会劣化",
      "资源稀缺驱动一切冲突"
    ]
  },

  // === 写作风格规则 ===
  "style_rules": {
    "global": [
      "情绪通过物理细节传递",
      "角色越痛苦语气越轻",
      "社会制度通过角色日常体验呈现，不用旁白解释"
    ],
    "per_arc": {
      "arc_a": ["标准爽文节奏", "A的认知失调通过行为呈现"],
      "arc_d": ["文风渐变——前期明快→后期厚重", "B出场段落始终保持表演性节奏"]
    }
  },

  // === 误判/误导设计（如果有）===
  "deception_design": {
    "misjudgment_stairs": [
      {
        "id": "stair_1",
        "position": "A重逢C后",
        "evidence": "B泄露情报+C功法痕迹",
        "a_conclusion": "C仍在算计自己",
        "reader_reaction": "确实可疑",
        "validity_rule": "普通读者代入A也会得出同样结论"
      }
    ],
    "misdirection_characters": ["A3韩禹成", "A4孙大牛", "C3", "C4马三刀", "X1影市"]
  }
}
```

---

## Blueprint 的生命周期

1. **创建**: `/novel-interview` 深度访谈 → `/novel-blueprint` 生成初始蓝图
2. **修改**: 用户随时可以用 `/novel-blueprint` 修改蓝图
3. **驱动**: 所有 Agent 在执行时读取蓝图，决定行为
4. **扩展**: 运行时发现新模式 → 系统建议修改蓝图 → 用户确认后更新

## Blueprint 与 Generated Rules 的关系

蓝图是"要什么"，规则文档是"怎么检查"。
理解层读蓝图 → 生成匹配的规则文档 → Checker Agent 读规则文档执行检查。
蓝图变 → 规则文档跟着变。

---

## Schema 规则

1. `project`、`narrative_structure`、`theme`、`required_rules`、`optional_features` 是必须字段
2. `narrative_structure.type` 是自由文本，不是枚举——系统可以理解任何结构描述
3. `required_rules` 列表决定理解层需要生成哪些规则文档
4. `optional_features` 的布尔值决定角色卡和大纲中包含哪些可选字段
5. 蓝图中不存储完整的设定文档内容——完整设定存在 `{project}/settings/` 目录
6. 蓝图是结构化索引，指导系统行为；设定文档是全文，供写作时参考

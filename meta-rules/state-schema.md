# State Schema

> 本文档定义项目运行时状态（state.json）的结构规范。
> 状态是整个系统的"记忆"——记录发生了什么、谁知道什么、当前在哪。
> 所有 Agent 读写状态都必须遵循此 schema。

---

## state.json 顶层结构

```jsonc
{
  "schema_version": "1.0",
  "project": {
    "title": "藏刃",
    "language": "zh",
    "created_at": "2026-04-02",
    "current_chapter": 45,
    "current_arc": "A篇章",
    "total_arcs": ["A篇章", "D篇章"],
    "word_count": 112000
  },

  // === 章节元数据 ===
  "chapter_meta": {
    "45": {
      "title": "...",
      "arc": "A篇章",
      "pov_character": "char_a",
      "word_count": 2300,
      "strand": "复仇推进线",               // 节奏线归属
      "hook": {
        "type": "crisis",
        "strength": "medium",
        "description": "..."
      },
      "engagement_score": 82,
      "review_score": 78,
      "timestamp": "..."
    }
  },

  // === 事实库（带知识归属）===
  "facts": [
    {
      "id": "fact_001",
      "content": "陆衍在沈渊身上植入了寄生阵纹",
      "established_chapter": 20,
      "known_by": ["reader"],                // 谁知道这件事
      "unknown_to": ["char_a"],              // 谁不知道
      "category": "plot",                    // plot | character | world | power | resource
      "mutable": false                       // 是否可被后续事件改变
    },
    {
      "id": "fact_002",
      "content": "沈渊突破到结丹巅峰",
      "established_chapter": 15,
      "known_by": ["char_a", "char_b", "reader", "public"],
      "unknown_to": [],
      "category": "power",
      "mutable": true
    }
  ],

  // === 错误认知（独立追踪）===
  "false_beliefs": [
    {
      "id": "fb_001",
      "holder": "char_a",
      "belief": "姜远是前世背叛自己的凶手",
      "reality": "陆衍是真凶，姜远是被害者",
      "established_chapter": 1,
      "reinforced_at": [8, 15, 30],          // 被加深的章节
      "will_shatter_at": null,               // 预期被打破的节点（可为 null）
      "category": "identity"
    }
  ],

  // === 钩子追踪 ===
  "hooks": [
    {
      "id": "hook_001",
      "description": "沈渊发现灵矿灵气流向异常",
      "type": "mystery",
      "planted_chapter": 12,
      "status": "planted",                   // planted | advancing | resolved | abandoned
      "expected_payoff": "D篇章",
      "last_advanced": 12,
      "known_by": ["char_a", "reader"]
    }
  ],

  // === 债务记录（豁免产生的）===
  "debts": [
    {
      "id": "debt_001",
      "source_rule": "engagement-rules",
      "source_constraint": "SOFT-002",
      "chapter_created": 40,
      "description": "连续3章使用危机钩",
      "due_by": "chapter_43",
      "interest_rate": 0.1,
      "status": "active"                     // active | paid | expired
    }
  ],

  // === 模式锚点追踪（如果 blueprint 定义了）===
  "pattern_anchors": {},

  // === 揭示事件追踪 ===
  "revelation_events": [
    {
      "id": "rev_001",
      "trigger": "A死亡瞬间",
      "reveals_to": "reader",
      "content": "全部真相——B是真凶",
      "status": "pending",
      "target_chapter": null
    }
  ]
}
```

---

## 核心规则

### 事实归属是强制的

每条 fact 必须标注 `known_by` 和 `unknown_to`。
Context Agent 在组装某角色视角的执行包时，**只能使用该角色在 `known_by` 列表中的事实**。

合法的 known_by 值：
- `"char_a"`, `"char_b"`, ... — 具体角色
- `"reader"` — 读者（可以知道角色不知道的事）
- `"public"` — 所有角色和读者都知道

### 错误认知独立追踪

错误认知不存在 `facts` 中（facts 只存真实事实）。
错误认知有独立的 `false_beliefs` 数组，标注持有者和真相。
Context Agent 在写持有者视角时，必须注入 false_belief 作为"该角色认为的事实"。

### 章节元数据自动维护

每章写完后，Data Agent 必须更新：
- `chapter_meta` 新增该章条目
- `facts` 新增/更新涉及的事实
- `character-cards/` 更新涉及角色的 `current_state` 和 `knowledge`
- `hooks` 更新涉及的钩子状态
- `false_beliefs` 更新（如果有变化）

### 跨章事实一致性（Verifier 通用扫描）

每条 `facts[i]` 带有 `established_chapter`。Verifier 在每章写完后，会对新章节正文做通用 fact-diff：
- 扫描章节中所有"前世"/既成事实类陈述
- 对照 `facts` 中 `established_chapter < current` 且 `mutable: false` 的条目
- 若出现与既有 fact 语义矛盾的陈述 → VERDICT FAIL (cross-chapter fact contradiction)

Verifier 不硬编码任何具体事实，只读本数组。任何项目要想让某条事实被跨章保护，把它写进 `facts` 并标 `mutable: false` 即可。

### 状态写入的原子性

Data Agent 更新 state 时，所有变更必须在同一操作中完成。
不允许部分更新——要么全部成功，要么全部回滚。

### 多篇章/多视角支持

`project.total_arcs` 声明所有篇章。
`chapter_meta[n].arc` 标注每章属于哪个篇章。
`chapter_meta[n].pov_character` 标注每章的视角人物。
这些字段使系统天然支持任意视角结构——单主角、双主角、多视角轮换、篇章切换。

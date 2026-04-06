# novel-engine

> 规则可编译的小说写作引擎 / Rule-compilable novel writing engine
> 以 Claude Code 插件形态运行 / Runs as a Claude Code plugin

---

## 中文

### 这是什么

**novel-engine** 是一个把"写小说"从 LLM 黑盒变成**可编译、可审查、可红队对抗**的工程系统。它不是又一个"AI 写小说工具"——它是一套**三层规则架构**：

```
meta-rules (固定语法)
    ↓ 编译
generated-rules (每本书的规则文档)
    ↓ 解释执行
agents (无状态执行器)
```

**核心原则：Agents 是解释器，规则文档是代码。** Agents 永不改动；规则可以被添加、修改、删除——符合 meta-rule schema 的任何文档都是合法且可执行的。

### 为什么需要它

直接让 LLM 写长篇小说会遇到三个致命问题：

1. **一致性漂移**——角色知识边界、伏笔、情感弧在第 50 章就会崩盘
2. **AI 腔不可逆**——过渡词堆积、心理分析报告式语言、平滑到无特征
3. **叙事结构无法保证**——双 POV、重生复仇、镜像结构、假信念这些高阶叙事技巧没有稳定的交付契约

novel-engine 针对每一个问题都有结构化答案：

| 问题 | 解决机制 |
|---|---|
| 一致性漂移 | `state.json` + knowledge attribution + false belief tracking + POV discipline rules |
| AI 腔不可逆 | Writer agent 的 4 个命名失败模式 + 去 AI 化规则 + Polisher 反扫 |
| 叙事结构 | 可编译规则系统 + Pattern anchors + Mirror structures + Cross-arc foreshadowing |
| 写手输出无法验证 | **Writer Delta 契约**：写手必须在正文同一轮产出结构化 JSON delta，由对抗式红队 agent 机械 diff |

### 架构

```
novel-engine/
├── .claude-plugin/          # Claude Code 插件配置
├── meta-rules/              # 规则语法（固定 schema）
├── agents/                  # 9 个无状态 agent
│   ├── interviewer.md           # 深度访谈
│   ├── blueprint-builder.md     # 蓝图生成
│   ├── outline-collaborator.md  # 大纲共创
│   ├── context-agent.md         # 上下文组装
│   ├── writer-agent.md          # 写手（带 delta 契约）
│   ├── checker-agent.md         # 规则审查
│   ├── polisher-agent.md        # 修缮 + 去 AI 化
│   ├── verification-agent.md    # 对抗式红队
│   └── data-agent.md            # 数据沉淀
├── skills/                  # 用户斜杠命令
│   ├── novel-interview/
│   ├── novel-blueprint/
│   ├── novel-outline/
│   ├── novel-write/             # 6 步 + Step 4.5 双子步管线
│   ├── novel-review/
│   ├── novel-direction/
│   ├── novel-query/
│   └── novel-resume/
├── default-templates/       # 通用规则集（如单主角网文模板）
├── references/              # 写作技法参考
└── docs/
```

**每本书的项目结构**（由 `/novel-interview` 创建）：

```
projects/{book-name}/
├── blueprint.json               # 创作蓝图
├── generated-rules/             # 本书专属规则（由访谈层生成）
├── character-cards/             # 角色卡（带 current_state）
├── outline/chapters/            # 分章大纲
├── chapters/                    # 正文
├── state/                       # 运行时状态
│   ├── state.json                   # 事实 / 假信念 / 钩子 / 伏笔
│   ├── writer-delta-{N}.json        # 写手结构化交付
│   ├── review-{N}.json              # Checker 审查报告
│   └── verification-{N}.md          # 红队对抗报告
└── summaries/
```

### 核心机制

#### 1. 三层规则架构

- **meta-rules/**：固定语法，定义"一条规则文档长什么样"
- **generated-rules/**：每本书的具体规则（由 `/novel-interview` 和 `/novel-blueprint` 生成，也可手写）
- **agents/**：无状态解释器，读规则、执行规则

这让我们可以支持**任意叙事结构**——不是只能写单主角爽文。当前测试项目《藏刃》是双 POV + 重生复仇 + 镜像结构 + 7 个行为模式锚点的高复杂度样本。

#### 2. Writer Delta 契约

传统 LLM 写作是黑盒：交出正文就完事。novel-engine 的 Writer 必须在**同一轮**输出两个文件：

- `chapters/第N章-{title}.md` 正文
- `state/writer-delta-{N}.json` 结构化交付

Delta 里包含（部分字段）：

```json
{
  "word_count": 2824,
  "opening": {
    "first_sentence_char_count": 6,
    "first_200_chars": "沈渊睁开眼。看见的是十七岁的手。...",
    "hook_anchors_used": ["异常状态", "未解之谜", "反直觉陈述"],
    "hook_anchor_position_chars": [19, 41, 64]
  },
  "forbidden_names_checked": {"陆衍": 0},
  "signature_lines_used": [{"text_as_written": "...", "exact_match": true}],
  "flashback_fragments": [{"char_count": 73}, ...],
  "flashback_total_chars": 254
}
```

**这个 delta 是绑定契约**。Verification Agent 会用 `wc -m`、`grep -c`、exact substring match 机械 diff。Writer 不能骗——骗了立刻被抓。

#### 3. Step 4.5 双子步审查

```
Step 1  Context Agent       → 创作执行包
Step 2  Writer Agent        → 正文 + writer-delta
Step 3  Checker Agent       → 规则审查
Step 4  Polisher Agent      → 修缮 + 去 AI 化
Step 4.5a Re-Check          → 修缮后复审，覆写 review.json
Step 4.5b Verification      → 对抗式红队（机械 diff + 探针）
Step 5  Data Agent          → 更新 state.json / 角色卡 / 摘要
Step 6  Backup              → Git commit
```

**Step 4.5b Verification Agent** 是从 Claude Code 源码的 verificationAgent 模式学来的对抗式设计：它的任务不是"确认章节没问题"，而是**尝试把章节打回 FAIL**。它有 3 个命名失败模式（verification avoidance / seduced by flow / deferring to Checker），7 条 rationalization 自识别表，以末行 `VERDICT: PASS|FAIL|PARTIAL` 作为机器解析锚。

#### 4. Agent Prompt 设计范式

所有 agent 的 system prompt 遵循同一个可量化骨架：

```
[身份 1 句]
+ [使命对抗化 1 段]    ← 把目标写成反面命题
+ [N 个命名失败模式]   ← 有名字、有描述、有 detection
+ [=== CRITICAL === 硬禁止块]
+ [Strengths 3-5 条]
+ [Guidelines / Process]
+ [策略适配矩阵]       ← 任务多态时
+ [Rationalization 识别表]  ← 反自欺
+ [Output Format + Bad/Good 样例对]
+ [末行解析锚]         ← 调用方机器解析
```

### 快速开始

前提：已安装 Claude Code。

```bash
# 1. 把本仓库作为 Claude Code 插件加载
# （具体加载方式依赖 Claude Code 插件系统）

# 2. 在任意目录启动一个新小说项目
/novel-interview
# 交互式深度访谈：世界观、人物、叙事结构、关键机制

# 3. 生成创作蓝图和规则
/novel-blueprint

# 4. 共创章节大纲
/novel-outline 1

# 5. 写章节（完整 6 步管线）
/novel-write 1

# 查询 / 调整 / 恢复
/novel-query "沈渊当前知道陆衍真相吗"
/novel-direction "后半部节奏收紧"
/novel-resume
```

### 参考项目

`projects/藏刃/` 是当前的测试项目：1,100,000 字目标的双 POV 重生复仇修仙小说，用来压力测试规则系统的所有高阶机制（knowledge tracking / false belief / POV discipline / mirror structures / pattern anchors / cross-arc foreshadowing）。

### 设计致谢

- **Claude Code 源码**（agent prompt 设计范式）：对抗式使命、命名失败模式、rationalization 表、末行解析锚、`criticalSystemReminder` 双层注入
- **dramatica-flow**（settlement table 思想）：强制 Writer 同轮输出结构化 delta
- **Claude Code 插件系统**：agents / skills / hooks 原生能力

### 许可

MIT（除非特定子目录另有说明）

---

## English

### What this is

**novel-engine** turns novel-writing from an LLM black box into a **compilable, auditable, red-team-verifiable** engineering system. It's not "another AI writing tool" — it's a **three-layer rule architecture**:

```
meta-rules (fixed grammar)
    ↓ compile
generated-rules (per-project rule documents)
    ↓ interpret
agents (stateless executors)
```

**Core principle: Agents are interpreters, rule documents are code.** Agents never change. Rules can be added, modified, or removed. Any document conforming to the meta-rule schema is valid and executable.

### Why it exists

Long-form novel generation by direct LLM prompting hits three fatal problems:

1. **Consistency drift** — character knowledge boundaries, foreshadowing, emotional arcs collapse by chapter 50
2. **Irreversible AI-voice** — transition-word soup, psych-report prose, smoothed into featurelessness
3. **Unenforceable narrative structure** — dual-POV, rebirth/revenge loops, mirror structures, false beliefs have no stable delivery contract

novel-engine addresses each:

| Problem | Mechanism |
|---|---|
| Consistency drift | `state.json` + knowledge attribution + false belief tracking + POV discipline rules |
| AI-voice | Writer agent's 4 named failure patterns + de-AI-voice rules + Polisher sweep |
| Narrative structure | Compilable rule system + pattern anchors + mirror structures + cross-arc foreshadowing |
| Unverifiable writer output | **Writer Delta contract**: writer must emit structured JSON delta alongside prose, mechanically diffed by an adversarial verification agent |

### Architecture

```
novel-engine/
├── .claude-plugin/          # Claude Code plugin config
├── meta-rules/              # Rule grammar (fixed schemas)
├── agents/                  # 9 stateless agents
│   ├── interviewer.md
│   ├── blueprint-builder.md
│   ├── outline-collaborator.md
│   ├── context-agent.md
│   ├── writer-agent.md          # writer with delta contract
│   ├── checker-agent.md
│   ├── polisher-agent.md
│   ├── verification-agent.md    # adversarial red-team
│   └── data-agent.md
├── skills/                  # user-facing slash commands
│   ├── novel-interview/
│   ├── novel-blueprint/
│   ├── novel-outline/
│   ├── novel-write/             # 6-step pipeline + dual Step 4.5
│   ├── novel-review/
│   ├── novel-direction/
│   ├── novel-query/
│   └── novel-resume/
├── default-templates/       # Common rule sets (e.g., single-protagonist web novel)
├── references/              # Craft references
└── docs/
```

**Per-project structure** (created by `/novel-interview`):

```
projects/{book-name}/
├── blueprint.json               # Creative blueprint
├── generated-rules/             # Per-book rules (from interview or hand-written)
├── character-cards/             # Character state cards
├── outline/chapters/            # Chapter outlines
├── chapters/                    # Prose
├── state/                       # Runtime state
│   ├── state.json                   # facts / false beliefs / hooks / foreshadowing
│   ├── writer-delta-{N}.json        # writer's structured delivery
│   ├── review-{N}.json              # checker report
│   └── verification-{N}.md          # red-team report
└── summaries/
```

### Core Mechanisms

#### 1. Three-layer rule architecture

- **meta-rules/**: fixed grammar defining what a rule document looks like
- **generated-rules/**: per-book concrete rules (generated by `/novel-interview` + `/novel-blueprint`, or hand-written)
- **agents/**: stateless interpreters that read rules and execute

This lets us support **any narrative structure** — not just single-protagonist web novels. The reference project *藏刃* is a dual-POV rebirth-revenge novel with mirror structures and 7 behavioral pattern anchors — high complexity stress test.

#### 2. Writer Delta Contract

Traditional LLM writing is a black box: prose out, you're done. novel-engine's Writer must output **two files in the same turn**:

- `chapters/第N章-{title}.md` — prose
- `state/writer-delta-{N}.json` — structured delivery

Delta fields (partial):

```json
{
  "word_count": 2824,
  "opening": {
    "first_sentence_char_count": 6,
    "first_200_chars": "...",
    "hook_anchors_used": ["anomaly", "mystery", "counter-intuitive-statement"],
    "hook_anchor_position_chars": [19, 41, 64]
  },
  "forbidden_names_checked": {"陆衍": 0},
  "signature_lines_used": [{"text_as_written": "...", "exact_match": true}],
  "flashback_fragments": [{"char_count": 73}, ...],
  "flashback_total_chars": 254
}
```

**The delta is binding.** The Verification Agent mechanically diffs it against the prose using `wc -m`, `grep -c`, exact substring match. Writers can't lie — a lie gets caught on the next step.

#### 3. Step 4.5 dual sub-step

```
Step 1    Context Agent        → execution package
Step 2    Writer Agent         → prose + writer-delta
Step 3    Checker Agent        → rule audit
Step 4    Polisher Agent       → fix + de-AI-voice sweep
Step 4.5a Re-Check             → re-run checker, overwrite review.json
Step 4.5b Verification Agent   → adversarial red-team (mechanical diff + probes)
Step 5    Data Agent           → update state.json / character cards / summary
Step 6    Backup               → Git commit
```

**Step 4.5b Verification Agent** is adapted from Claude Code's own verificationAgent pattern. Its job is not to confirm the chapter works — **it's to try to break it**. Three named failure patterns (verification avoidance / seduced by flow / deferring to Checker), seven rationalization self-recognition entries, ends with a machine-parseable `VERDICT: PASS|FAIL|PARTIAL` line.

#### 4. Agent prompt design pattern

All agent system prompts follow the same quantifiable skeleton:

```
[one-line identity]
+ [adversarial mission statement]   ← frame the goal as a negation
+ [N named failure patterns]        ← name + description + detection
+ [=== CRITICAL === prohibition block]
+ [Strengths, 3-5 items]
+ [Guidelines / Process]
+ [strategy adaptation matrix]      ← for polymorphic tasks
+ [rationalization recognition list]
+ [Output Format + Bad/Good example pair]
+ [final parse-anchor line]         ← machine-parseable by caller
```

This pattern was extracted from Claude Code's own built-in agents (`verificationAgent`, `exploreAgent`, `planAgent`, `generalPurposeAgent`) and ported verbatim into novel-engine's writer and verification agents.

### Quick Start

Prerequisite: Claude Code installed.

```bash
# 1. Load this repo as a Claude Code plugin
#    (load mechanism depends on Claude Code plugin system)

# 2. Start a new novel project in any directory
/novel-interview
# Interactive deep interview: world, characters, narrative structure, key mechanics

# 3. Generate blueprint and rules
/novel-blueprint

# 4. Co-create a chapter outline
/novel-outline 1

# 5. Write a chapter (full 6-step pipeline)
/novel-write 1

# Query / adjust / resume
/novel-query "does Shen Yuan currently know the truth about Lu Yan"
/novel-direction "tighten pacing in the second half"
/novel-resume
```

### Reference project

`projects/藏刃/` is the current stress-test project: a 1.1M-character dual-POV rebirth-revenge cultivation novel, used to exercise every high-level mechanism (knowledge tracking, false belief, POV discipline, mirror structures, pattern anchors, cross-arc foreshadowing). Per-project content is gitignored — the repo ships only the engine.

### Credits

- **Claude Code source** (agent prompt design patterns): adversarial mission framing, named failure patterns, rationalization tables, final parse-anchors, `criticalSystemReminder` dual-injection
- **dramatica-flow** (settlement table idea): force the writer to emit a structured delta alongside prose in one turn
- **Claude Code plugin system**: agents / skills / hooks as native capabilities

### License

MIT (unless otherwise noted in specific subdirectories)

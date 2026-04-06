# Summary Schema

> 定义"一份合格的章节摘要"的结构规范。
> 摘要由 Data Agent 在每章写完后生成，存储在 `{project}/summaries/chapter-{N}.md`。
> Verification Agent 在做多章连贯性检核时读取摘要（预算分层加载，而非读全章正文）。
> Context Agent 在组装后续章节执行包时，也可以读摘要来注入"前情提要"。

---

## 为什么要 schema 化

Verifier 的 **Check 12: 多章连贯性**必须在上下文预算内读到"剧情走向"。直接读前 N 章全文会爆预算；读自由格式的摘要又无法机械抽取字段（谁的 POV、建立了哪些事实、推进/种下了哪些钩子、信念状态变化）。

摘要是对章节正文的**有损压缩**，但**对下列字段是无损的**：POV、建立的 fact id、钩子 id、信念状态迁移、签名台词消费、habit 触发。只要 schema 强制这些字段结构化，Verifier 就可以在几 KB 的预算内串起整段叙事。

---

## 结构

```markdown
# 第{N}章 {title} — 摘要

**POV**: char_a | **arc**: arc_a | **chapter_type**: reinforcement | **words**: 3153

## 一句话
[本章故事的一句话——≤80字，客观事件，不评价]

## 关键事实落地
> 本章确立或确认的 fact id 列表，每条必须对应 state.facts 中一条。
- **fact_008** established: [content 一行摘要]
- **fact_009** established: [content 一行摘要]
- **fact_010** confirmed: [content 一行摘要]  # confirmed = 之前建立的被再次强化

## 信念状态
> 本章对每个正在追踪的 false_belief 的处理。
- **fb_001**: carried | reinforced | shattered | dormant | [一行说明]
- **fb_002**: dormant
- **fb_003**: dormant

## 钩子流动
> 每个变动的 hook id。动词必须是 planted / advanced / resolved / abandoned。
- **hook_000a** advanced: [一行]
- **hook_001a** planted: [一行]

## 闪回预算
[本章用量] / [本章上限]；篇章累计池剩余 [数字]

## 签名台词
本章消费 [数字] 条：[line id 列表，或 "本章 0 消费"]

## Habit 触发
> 仅列出 character-card 中标记 core:true 的 habit。
- habit_jade: fired [N] 次 | skipped（原因）
- habit_sheath: fired [N] 次 | skipped（原因）

## 验收标准完成情况
> 对照本章大纲 acceptance_criteria 逐条勾选。
- [x] A: ...
- [x] B: ...
- [ ] C: 未完成（原因）——如有未完成项，必须在章末 note 说明是否转入下章

## 章末信息状态
- **POV 角色**: [持有什么 / 正在做什么 / 到哪里]
- **读者**: [新增知道了什么 / 被刻意拖着没给的东西]
- **真相持有者**: [无 / 某角色知道真相但未登场]

## 下章衔接锚
[一句话——下章必须回应的那个具体锚点]
```

---

## Schema 规则

1. 摘要每章一份，文件名 `chapter-{N}.md`。
2. 顶部元数据行（POV / arc / chapter_type / words）必须能被单行正则解析。
3. 关键事实落地、信念状态、钩子流动、签名台词、habit 触发、验收标准 —— **这六节是给 Verifier 读的**，必须严格按上述小节标题和 id 引用格式。自由文本只允许在"一句话"、"章末信息状态"、"下章衔接锚"三节。
4. 摘要总长建议 ≤ 1200 字符（Verifier 才能在预算内同时加载 K 份）。
5. 摘要由 Data Agent 在 `/novel-write` 的 Step 6 阶段生成，与 state.json 更新同一事务写入——两者内容必须一致（fact id、hook id、fb id 在 state.json 中一定存在）。
6. 如果 Writer / Checker / Verifier 发现章节和摘要不一致，**以正文为准**，Data Agent 需要重新生成摘要。

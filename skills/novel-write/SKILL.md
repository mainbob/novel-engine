# /novel-write

> 执行完整的章节写作流程——上下文组装 → 写作 → 审查 → 修缮 → 数据沉淀。

---

## 触发方式

```
/novel-write                           # 写下一章（自动递增）
/novel-write 15                        # 写第15章
/novel-write 15 --fast                 # 快速模式（跳过风格适配）
/novel-write 15 --minimal             # 最简模式（只跑核心检查）
/novel-write 15 --direct              # 跳过执行包确认，直接写
```

## 前置条件

- `{project}/blueprint.json` 存在
- `{project}/outline/chapters/chapter-{N}.md` 存在（本章大纲）
- `{project}/generated-rules/` 至少有一份规则文档
- `{project}/state/state.json` 存在

## 执行流程（6步强制顺序）

### Step 0: 预检

1. 验证项目完整性（blueprint、大纲、状态文件都在）
2. 验证本章大纲存在
3. 确定环境变量和路径
4. 任何缺失 → 阻断并提示

### Step 1: Context Agent（上下文组装）

调用 Context Agent，产出创作执行包。

**除非使用 --direct**，系统会展示执行包摘要让用户确认：
```
"第15章执行包摘要：
 - POV: 沈渊
 - 目标: [从大纲提取]
 - 出场角色: A, B, C1
 - 关键约束: [列出硬约束]
 - 钩子计划: 回应hook_003, 种下hook_007
 
 确认开始写作？可以在此补充额外指示。"
```

用户可以：
- 确认 → 继续
- 补充指示 → "这章我希望战斗场景多一些" → 追加到执行包
- 修改 → "钩子我想换一个" → 调整后再确认

### Step 2: Writer Agent（写作 + 结构化 delta）

调用 Writer Agent（`agents/writer-agent.md`），基于执行包产出 **两个文件**（同一轮输出）：

1. `chapters/第{NNNN}章-{title}.md` — 纯正文
2. `state/writer-delta-{N}.json` — 结构化交付 delta（binding）

**Writer 必须在响应末行输出解析锚**：
- 成功：`WRITER: DONE chapter={N} words={count} delta_written=true`
- 失败：`WRITER: BLOCKED reason="..."`

**闸门**：
- 如果 delta 文件缺失 → 阻断，回到 Step 2 重跑
- 如果 Writer 输出 `BLOCKED` → 上报用户，不进入 Step 3
- 如果主流程无法正则解析到末行锚 → 视为 Writer 失败

**Delta 绑定契约**（Checker / Verifier 会机械 diff）：
- `word_count` 必须与 `wc -m` 结果一致
- `opening.first_200_chars` 必须与正文前 200 字完全一致
- `forbidden_names_checked` 必须覆盖执行包 `forbidden_names` 全集
- `signature_lines_used[].exact_match` 必须可通过字符串精确匹配验证
- `flashback_fragments[].char_count` 总和必须等于 `flashback_total_chars`

**模式差异**:
- 标准模式：完整写作
- --fast：跳过 Step 2B 风格适配
- --minimal：简化写作，后续审查也简化

### Step 3: Checker Agent（审查）

**必须由 Task 子代理执行，主流程不得内联伪造审查结论。**

调用 Checker Agent，扫描 `generated-rules/` 下所有适用规则，产出审查报告。

**模式差异**:
- 标准模式：执行所有匹配的规则文档
- --minimal：只执行 priority=critical 的规则

### Step 4: Polisher Agent（修缮）

调用 Polisher Agent：
1. 修复所有 critical 硬约束违反
2. 修复 high 违反或记录偏差
3. 按 ROI 处理 medium/low
4. 执行去AI化全文检查

**闸门**: 如果去AI化检查不通过 → 阻断，不进入 Step 4.5。

### Step 4.5: Re-Check + Verification（修缮后复检 + 对抗式红队）

**必须执行，不得跳过。** 两个子步骤，顺序执行：

#### Step 4.5a: Re-Check

1. 重新调用 Checker Agent 对修缮后的章节执行一次完整审查
2. 覆写 `{project}/state/review-{N}.json`（不保留旧版）
3. 如果新报告仍有 critical 违反 → 回到 Step 4 再修缮一次（最多 2 轮）
4. 2 轮后仍有 critical → 阻断并报告给用户

**目的**: 防止审查报告与实际章节内容不一致。

#### Step 4.5b: Verification Agent（对抗式红队）

调用 Verification Agent（`agents/verification-agent.md`）作为 Checker 之外的**独立红队**。Verifier 不是复查 Checker——它的任务是**尝试把章节打回 FAIL**。

**输入**：
- 章节文件路径
- `state/writer-delta-{N}.json`（Writer 的自报 delta）
- `state/review-{N}.json`（Checker 的 post-polish 报告）
- `outline/chapters/chapter-{N}.md`
- `generated-rules/` 目录
- `state/state.json`

**Verifier 执行的机械校验**（基于 writer-delta）：
- `wc -m` 正文 vs `delta.word_count`
- 正文前 200 字 vs `delta.opening.first_200_chars`
- `grep -c` 每个 `forbidden_names_checked` 的 key 并对比数值
- 每条 `signature_lines_used[].text_as_written` 必须是正文子串
- 每个 `flashback_fragments[].char_count` 必须与正文中对应段落实测一致
- `delta.flashback_total_chars` ≤ outline 规定的预算

**Verifier 必须以末行锚结束**：`VERDICT: PASS` / `VERDICT: FAIL` / `VERDICT: PARTIAL`。主流程用正则解析。

**闸门**：
- `VERDICT: PASS` → 写入 `state/verification-{N}.md`，进入 Step 5
- `VERDICT: FAIL` → 写入 `state/verification-{N}.md`，回到 Step 4 修缮（与 Step 4.5a 共享 2 轮上限）
- `VERDICT: PARTIAL` → 记录环境限制到 `verification-{N}.md`，上报用户由用户裁决是否放行
- 无法解析末行锚 → 视为 Verifier 失败，阻断

**目的**: Checker 是 LLM 读正文反向推断；Verifier 是基于 Writer 自报 delta 的机械比对 + 对抗式探针。两者覆盖不同类型的错误。

### Step 5: Data Agent（数据沉淀）

调用 Data Agent：
1. 提取事实（9大类，带知识归属）
2. 提取实体 + 消歧
3. 更新 state.json
4. 更新角色卡
5. 生成章节摘要
6. RAG 向量索引（如果配置了 Embedding）

**失败隔离**: 如果 RAG 索引失败，不回滚前面的步骤，只重跑索引。

### Step 6: 备份

1. Git commit（如果项目是 git 仓库）
2. 消息格式: `第{N}章: {title}`

## 充分性闸门（所有必须满足）

1. 非空章节文件存在
2. `state/writer-delta-{N}.json` 存在且字段完整
3. Writer 末行锚解析成功（`WRITER: DONE`）
4. Step 3 产出了审查报告
5. Step 4 处理了所有 critical 问题
6. Step 4 去AI化检查通过
7. Step 4.5a 复检报告无 critical 违反且已覆写 review-{N}.json
8. Step 4.5b Verification Agent 返回 `VERDICT: PASS`（或用户明确放行 PARTIAL）
9. Step 5 更新了 state.json 和角色卡

## 输出

- `{project}/chapters/第{NNNN}章-{title}.md`
- `{project}/state/context-{N}.md`
- `{project}/state/writer-delta-{N}.json`（Writer 结构化交付）
- `{project}/state/review-{N}.json`（Checker post-polish 版本）
- `{project}/state/polish-{N}.md`
- `{project}/state/verification-{N}.md`（Verifier 红队报告）
- `{project}/summaries/chapter-{N}.md`
- 更新后的 `state.json` 和 `character-cards/`

## 禁止行为

- 不合并步骤（Step 2 和 Step 3 不能合并）
- 不跳过非可选步骤
- 不内联伪造审查结论——必须由子代理执行
- 不在 Step 1 确认前开始写作（除非 --direct）

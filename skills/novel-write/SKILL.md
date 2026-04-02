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

### Step 2: Writer Agent（写作）

调用 Writer Agent，基于执行包产出章节正文。

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

**闸门**: 如果去AI化检查不通过 → 阻断，不进入 Step 5。

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
2. Step 3 产出了审查报告
3. Step 4 处理了所有 critical 问题
4. Step 4 去AI化检查通过
5. Step 5 更新了 state.json 和角色卡

## 输出

- `{project}/chapters/第{NNNN}章-{title}.md`
- `{project}/state/context-{N}.md`
- `{project}/state/review-{N}.json`
- `{project}/state/polish-{N}.md`
- `{project}/summaries/chapter-{N}.md`
- 更新后的 `state.json` 和 `character-cards/`

## 禁止行为

- 不合并步骤（Step 2 和 Step 3 不能合并）
- 不跳过非可选步骤
- 不内联伪造审查结论——必须由子代理执行
- 不在 Step 1 确认前开始写作（除非 --direct）

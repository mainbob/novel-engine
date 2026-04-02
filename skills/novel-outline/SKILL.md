# /novel-outline

> 人机协作设计大纲——用户给方向，系统细化为结构化大纲。

---

## 触发方式

```
/novel-outline                         # 交互模式（从当前进度开始）
/novel-outline 第一卷                   # 指定卷
/novel-outline 15-30                   # 指定章节范围
/novel-outline --auto                  # 自动模式（系统生成，用户审核）
/novel-outline --show                  # 查看当前大纲状态
```

## 前置条件

- `{project}/blueprint.json` 存在
- `{project}/generated-rules/pacing-rules.md` 存在

## 执行流程

### Step 1: 加载上下文

1. 读取 blueprint.json → 叙事结构、篇章信息
2. 读取已有大纲 → 了解规划到哪里
3. 读取 state.json → 了解写到哪里、未解决钩子
4. 读取 generated-rules/pacing-rules.md → 节奏约束
5. 读取角色卡 → 角色当前状态

### Step 2: 确定范围

- 如果用户指定了卷或章节范围 → 使用指定范围
- 如果未指定 → 从当前进度的下一个未规划段落开始

### Step 3: 接收用户输入

**交互模式**:
- 提示用户："这一段你有什么剧情构想？可以详细说，也可以说个大概方向。"
- 如果用户给出思路 → 模式一（系统细化）
- 如果用户说"你来建议" → 模式二（系统给选项）
- 如果 --auto → 模式三（全自动）

### Step 4: 生成大纲

调用 Outline Collaborator Agent：

1. 如果是篇章级：先生成节拍表（Beat Sheet）
   - 开篇承诺、递进危机、中点反转（必填）、最低点、高潮、新钩子
2. 如果是章节级：生成每章大纲
   - 必须字段：目标、冲突、状态变更、钩子
   - 可选字段：根据 blueprint.optional_features 自动添加
3. 检查节奏分配是否符合 pacing-rules
4. 检查钩子连续性

### Step 5: 用户确认

展示生成的大纲，标注：
- 需要用户确认的决策点
- 节奏分配统计
- 钩子回收规划

用户可以：
- 确认 → 保存
- 修改某些章节 → 系统调整后再确认
- 推翻重来 → 回到 Step 3

### Step 6: 保存

- 篇章大纲 → `outline/arc-{id}.md`
- 章节大纲 → `outline/chapters/chapter-{N}.md`

## 输出

- `{project}/outline/` 下的大纲文档

## 下一步

运行 `/novel-write {chapter}` 开始写作。

## 禁止行为

- 交互模式下不跳过用户确认
- 不违反蓝图的叙事规则
- 自动模式下不引入未在蓝图中定义的重大转折
- 不忽略已种下的钩子

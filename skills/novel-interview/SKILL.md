# /novel-interview

> 深度访谈——让系统理解你的创作意图。
> 这是使用 Novel Engine 的第一步。

---

## 触发方式

```
/novel-interview                     # 从零开始对话式访谈
/novel-interview --docs <path>       # 直接读取已有设定文档
/novel-interview --resume            # 恢复中断的访谈
```

## 前置条件

无。这是项目创建的起点。

## 执行流程

### Step 0: 项目初始化

1. 确认项目名称（用户提供或从对话中提取）
2. 创建项目目录 `projects/{project-name}/`
3. 创建子目录：`settings/`、`outline/`、`chapters/`、`state/`、`character-cards/`、`generated-rules/`、`summaries/`

### Step 1: 设定文档导入（如果有 --docs）

如果用户提供了已有设定文档路径：
1. 将文档复制到 `{project}/settings/`
2. 阅读所有文档，建立初步理解
3. 跳到 Step 3（补充确认），不重复问已有信息

### Step 2: 开放式访谈（如果没有 --docs）

调用 Interviewer Agent 进行多轮对话：
1. 核心创意
2. 结构理解
3. 补充细节
4. 确认输出

**关键约束**: 访谈必须由 Task 子代理执行。每轮对话都展示给用户，等待用户回应。

### Step 3: 补充确认

无论是对话式还是文档导入，最终都输出结构化理解稿让用户确认。

理解稿包含：
- 核心概念
- 叙事结构（类型、POV、篇章）
- 角色列表及定位
- 世界观要点
- 特殊叙事机制
- 用户硬性要求
- 留给系统的部分

### Step 4: 保存

将确认后的理解稿存为 `{project}/interview-notes.md`。

## 输出

- `projects/{project-name}/` 目录结构
- `projects/{project-name}/settings/*.md`（如果用户提供了文档）
- `projects/{project-name}/interview-notes.md`

## 下一步

运行 `/novel-blueprint` 将理解稿转化为创作蓝图和规则文档集合。

## 禁止行为

- 不在访谈阶段生成任何规则或蓝图
- 不建议用户改变叙事结构
- 不跳过用户确认步骤
- 不假设用户要写的是标准网文

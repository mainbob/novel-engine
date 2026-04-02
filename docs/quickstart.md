# 快速开始

## 1. 安装

将本项目作为 Claude Code 插件使用。确保项目目录在 Claude Code 的工作区内。

## 2. 创建项目

### 方式一：对话式（从零开始）

```
/novel-interview
```

系统会和你对话，了解你想写什么样的故事。

### 方式二：文档导入（已有设定）

```
/novel-interview --docs /path/to/your/settings/
```

系统会阅读你的设定文档，然后确认理解是否正确。

## 3. 生成蓝图和规则

```
/novel-blueprint
```

系统根据理解生成：
- 创作蓝图（blueprint.json）
- 检测规则文档（generated-rules/）
- 角色卡（character-cards/）
- 初始状态（state.json）

## 4. 设计大纲

```
/novel-outline 第一卷
```

告诉系统你的剧情构想，系统细化为章节大纲。

## 5. 开始写作

```
/novel-write 1
```

系统执行完整流程：上下文组装 → 写作 → 审查 → 修缮 → 数据沉淀。

## 6. 查询状态

```
/novel-query 沈渊          # 查角色
/novel-query hooks         # 查钩子
/novel-query progress      # 查进度
```

## 7. 调整方向（随时可用）

```
/novel-direction
```

告诉系统你想怎么改，系统分析影响后更新大纲和规则。

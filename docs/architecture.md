# Novel Engine 架构文档

## 核心思想

**规则可热插拔的 Agent 系统。**

- Agents 是解释器，规则文档是代码
- Agents 永远不变，规则随时可以加
- 任何符合 meta-rule schema 的文档都可以被 Agent 读取并执行

## 三层架构

```
┌─────────────────────────────────────────────┐
│ 元规则层 (meta-rules/)                        │
│ 固定不变。定义"规则文档长什么样"               │
│ checker-schema / character-schema / ...      │
├─────────────────────────────────────────────┤
│ 规则层 (generated-rules/)                     │
│ 每个项目独立。由理解层从用户输入推导生成         │
│ 可运行时追加、用户手写、从默认库复制            │
├─────────────────────────────────────────────┤
│ 执行层 (agents/)                              │
│ 通用解释器。读 generated-rules/ 执行           │
│ 不包含任何硬编码业务逻辑                       │
└─────────────────────────────────────────────┘
```

## 数据流

```
用户设定文档
    ↓
/novel-interview → interview-notes.md
    ↓
/novel-blueprint → blueprint.json + generated-rules/ + character-cards/
    ↓
/novel-outline → outline/
    ↓
/novel-write：
    Context Agent (读蓝图+状态+规则 → 创作执行包)
    → Writer Agent (写章节)
    → Checker Agent (读 generated-rules/ 逐条检查)
    → Polisher Agent (修复)
    → Data Agent (提取事实+更新状态)
```

## 与现有系统的对比

| 维度 | webnovel-writer | InkOS | Novel Engine |
|------|----------------|-------|-------------|
| 规则来源 | 硬编码在 agent MD 中 | 硬编码在 TS 代码中 | 从用户输入动态生成 |
| 模板角色 | 驱动系统行为 | 驱动 Architect 生成 | 仅作参考素材 |
| 叙事结构 | 单主角固定 | 单主角固定 | 任意结构 |
| 信息差追踪 | 无 | 无 | 按需启用 |
| 规则扩展 | 需改代码 | 需改代码 | 放入新 MD 文件即可 |
| 用户介入 | 仅 init 阶段 | 手动改 MD 文件 | 全流程可介入 |

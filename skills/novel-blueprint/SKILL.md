# /novel-blueprint

> 生成或修改创作蓝图——将理解转化为系统可执行的结构化数据和规则文档。

---

## 触发方式

```
/novel-blueprint                     # 首次生成（需要先完成 /novel-interview）
/novel-blueprint --modify             # 修改现有蓝图
/novel-blueprint --regenerate-rules   # 仅重新生成规则文档（蓝图不变）
/novel-blueprint --show               # 查看当前蓝图摘要
```

## 前置条件

- `{project}/interview-notes.md` 存在
- `{project}/settings/` 下有设定文档（可选但推荐）

## 执行流程

### 首次生成模式

#### Step 1: 加载输入

1. 读取 `interview-notes.md`
2. 读取 `settings/*.md`（所有设定文档）
3. 读取 `meta-rules/*.md`（所有 schema）
4. 检查 `blueprint.json → genre_references`，加载对应的 `default-templates/genres/` 作为参考

#### Step 2: 生成蓝图

调用 Blueprint Builder Agent：
1. 分析叙事结构 → 确定 `narrative_structure`
2. 分析特殊机制 → 确定 `optional_features`
3. 推导需要的规则类型 → 确定 `required_rules`
4. 提取世界设定摘要 → 填充 `world_summary`
5. 提取风格规则 → 填充 `style_rules`
6. 如果有误导/双层叙事设计 → 填充 `deception_design`
7. 生成 `blueprint.json` 和 `blueprint.md`

#### Step 3: 生成规则文档

对 `required_rules` 中的每一项：
1. 读取对应的 `meta-rules/*-schema.md`
2. 基于蓝图推导具体规则内容
3. 生成规则文档到 `generated-rules/`

**关键**: 每份生成的规则文档必须符合对应的 meta-rule schema。

#### Step 4: 生成角色卡

对设定文档中的每个角色：
1. 确定必须字段 + 根据 `optional_features` 确定可选字段
2. 从设定文档提取信息填充
3. 生成到 `character-cards/{id}.json`

#### Step 5: 初始化状态

生成初始 `state/state.json`（遵循 `meta-rules/state-schema.md`）。

#### Step 6: 用户确认

向用户展示：
- 蓝图摘要（blueprint.md）
- 生成的规则文档列表及每份的核心检测点
- 角色卡列表
- 启用的功能特性

用户确认或请求修改。

### 修改模式 (--modify)

1. 读取现有 blueprint.json
2. 与用户对话确认要修改什么
3. 应用修改
4. 检查哪些 generated-rules 受影响
5. 重新生成受影响的规则文档
6. 向用户展示变更，确认后保存

### 规则重新生成模式 (--regenerate-rules)

不修改蓝图，仅根据当前蓝图重新生成所有规则文档。
用于：规则文档被手动修改后想恢复、或 meta-rule schema 更新后。

## 输出

- `{project}/blueprint.json`
- `{project}/blueprint.md`
- `{project}/generated-rules/*.md`（每个 required_rule 一份）
- `{project}/character-cards/*.json`
- `{project}/state/state.json`

## 下一步

运行 `/novel-outline` 开始设计大纲。

## 禁止行为

- 不编造设定文档中没有的角色信息
- 不生成不在 required_rules 中的规则文档
- 不跳过用户确认步骤

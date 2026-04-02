# /novel-query

> 查询项目状态——角色、钩子、事实、信息差、进度等。

---

## 触发方式

```
/novel-query 沈渊                      # 查询角色当前状态
/novel-query hooks                     # 查询所有未解决钩子
/novel-query facts --chapter 15        # 查询第15章新增的事实
/novel-query knowledge 陆衍            # 查询某角色的知识边界
/novel-query progress                  # 查询整体进度
/novel-query debts                     # 查询未偿还的豁免债务
/novel-query pacing                    # 查询节奏分布统计
```

## 前置条件

- `{project}/state/state.json` 存在

## 数据来源

- `state.json` — 事实、钩子、章节元数据、债务
- `character-cards/*.json` — 角色状态和知识边界
- `blueprint.json` — 叙事结构信息
- `generated-rules/` — 规则内容
- `summaries/` — 章节摘要

## 输出

格式化的查询结果，直接展示给用户。

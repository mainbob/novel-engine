# /novel-review

> 对已写章节执行多维质量审查。可单章或批量。

---

## 触发方式

```
/novel-review 15                       # 审查第15章
/novel-review 10-20                    # 审查第10-20章
/novel-review --all                    # 审查所有已写章节
/novel-review 15 --rules engagement    # 只跑指定规则
```

## 前置条件

- 指定章节的正文文件存在
- `{project}/generated-rules/` 至少有一份规则文档

## 执行流程

1. 确定审查范围
2. 对每一章调用 Checker Agent
3. 汇总结果

## 输出

- 每章的 `{project}/state/review-{N}.json`
- 汇总报告（展示给用户）

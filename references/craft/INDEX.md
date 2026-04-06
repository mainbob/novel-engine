# Craft Module Index

> **按需借调**。Context Agent 读本索引，根据本章场景标签匹配模块，**只把匹配的**模块注入执行包。
> 原则：不匹配 = 不进上下文。宁可少一条技巧，也不要污染写手的注意力。

---

## 模块清单

| 模块 | trigger_tags | 触发条件 | 字数（约） |
|---|---|---|---|
| `dialogue-no-said.md` | `has_dialogue`, `dialogue_heavy` | 本章有 ≥3 轮对话或对话是主要戏肉 | 900 |
| `action-scene.md` | `has_combat`, `physical_confrontation` | 本章有打斗、对峙、追杀、格挡 | 1200 |
| `group-scene.md` | `has_ensemble_4plus`, `crowd_scene` | 单场同时出场 ≥4 人且每人都有动作/台词 | 900 |
| `show-dont-tell.md` | `emotional_beat`, `high_stakes_scene`, `internal_turmoil` | 关键情绪戏、转折、决心时刻、重大冲突 | 800 |
| `opening-hook-techniques.md` | `is_opening_chapter`, `is_arc_opening`, `is_pov_switch` | 首章、篇章开场、POV 切换章 | 700 |

---

## 选择协议

```
input: outline tags, POV, chapter_type_tag
output: list of craft modules to inject

steps:
1. scan outline for scenario markers (dialogue count, combat markers, ensemble size, emotional beats)
2. for each matched trigger_tag, add the corresponding module
3. if chapter_type_tag ∈ {opening, arc-start, pov-switch}, add opening-hook-techniques
4. if 0 modules matched and chapter is emotionally weighted, default to show-dont-tell
5. cap at 3 modules total (more = noise). prioritize by: opening > show-dont-tell > dialogue > action > group
6. emit matched module IDs + their full content into execution package section 6.5 "craft"
```

## 反模式

- **不要**把所有模块全部注入"以防万一"——这是 harness engineering 的反面
- **不要**把 craft 模块合并到 writer-agent.md 的 system prompt——那会常驻污染
- **不要**在过场章（低 stakes、纯推进）注入任何模块——让 Writer 走基线风格即可
- **不要**重复注入：如果一个模块上一章已注入且本章场景高度相似，Context Agent 可用 `--fresh` 或简述"参考上章 craft"代替

## 模块内部规范

每个模块必须：
1. 开头一句话定位（这个模块解决什么）
2. 3-5 个有编号的技巧（招式），每招带：定义 + 坏例 + 好例
3. 末尾一段"豁免"（什么时候不用这些技巧——防止滥用）
4. 不写到 200 行以上，否则拆分

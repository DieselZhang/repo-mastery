# Module Brief Template — 预提取源码片段

> **何时读**：Phase 3，**大型仓库**（或用户要求省 token 时）。学习一个模块前，先写一份 brief 把该模块的**关键源码片段 + 证据位置**预提取出来，之后的学习轮次就不再反复 Read 源码。吸收自 docs-to-course 的 `module-brief-template.md`（它预提取命令/配置，我们预提取源码）。

## 机制为什么省 token

一个知识点要讲清，通常需要 2–4 段关键源码。如果每轮学习都现读整个文件，token 会重复燃烧。**预提取**把"这段代码在讲什么"浓缩进 brief，tutor 直接引用 brief，只有遇到 brief 没有的细节才按需 Read。

## 何时写 brief

- 大型仓库（Phase 0 判定）：每个模块学习前写一份。
- 中小型仓库：如果某模块源码多、调用链长，也值得写。
- 完成后 brief 保留在 `.learning/briefs/`，供后续复习会话复用。

## Brief 模板

写入 `<repo>/.learning/briefs/<module>.md`：

```md
# 模块 Brief — <module title>（<module_id>）

**证据定位**
- 顶层目录/核心文件: <path>
- 入口函数: <file>:<line>

## 教学弧线
- 一句话"为什么关心"（实用收益）
- 关键心智模型（用户该带走的一个核心图景）
- 本模块的关键实现要点（若有关键实现模块）

## 知识点 → 证据映射（核心）
| 知识点 | 类型 | 预提取源码片段(文件:行) | 一句点评 |
|---|---|---|---|
| kp01-01 | procedure | `src/main.py:42-58` | 启动入口，负责… |
| kp01-02 | concept | `src/pipeline.py:120-160` | RAG 检索主链路 |

## 预提取源码片段（verbatim，含文件:行）
> 只放讲知识点确实需要的片段，每段 ≤ 20 行。超过 → 拆小段或写一句"见 <file>:<range> 进一步展开"。

### 片段 A — 启动流程（src/main.py:42-58）
```python
<verbatim 源码>
```
**点评**：这一段做了什么，为什么是这个顺序，哪里是易错点。

### 片段 B — RAG 主链路（src/pipeline.py:120-160）
```python
<verbatim 源码>
```
**点评**：…

## 易错点 / 陷阱
- 用户容易卡在哪（从错误类型角度预判：structural/deviation/application/metacognitive）

## 相邻模块衔接
- 前一模块覆盖: …
- 后一模块覆盖: …

## 本模块的费曼追问（design 型用）
- 为什么不用方案 B？→ 证据答: …
```

## 铁律

- **片段必须 verbatim**：一字不改复制源码，并带 `文件:行`。点评和源码分开，绝不混写。
- **宁可少不可多**：只预提取讲知识点需要的片段。超过 20 行的段在 brief 里放定位（`文件:行`），不要整段塞进来。
- **brief 是证据缓存，不是权威**：学习中发现 brief 讲不清的地方，回到源码验证，然后更新 brief。

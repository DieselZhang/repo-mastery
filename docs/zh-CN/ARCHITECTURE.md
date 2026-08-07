# Repo-Mastery 架构设计

本文说明 Repo-Mastery 的内部工作原理：设计公理、掌握度引擎、四个阶段与数据模型。

## 概览

Repo-Mastery 是一个 **Claude Code skill**，把源码仓库转成面向开发者的掌握式课程。它由一个 SKILL.md 编排器 + 一组按阶段读取的参考文档（保持上下文精简）+ 一个大型仓库用的可选 Python 脚本组成。

```text
SKILL.md（编排器）
   │  按阶段读取
   ▼
references/curriculum-design.md     Phase 1：从源码构建课程地图
references/mastery-policy.md        Phase 3：闸门、间隔复习、错误诊断
references/session-flow.md          Phase 3：交互式会话协议
references/quiz-design.md           Phase 3：测验原则
references/module-brief-template.md Phase 3：省 token 的预提取
references/note-template.md         Phase 3：笔记格式
references/learning-records-template.md  全程：理解演化记录
references/gotchas.md               全程：失败点清单
references/index-script-spec.md     Phase 0：大型仓库索引说明
references/html-shell/              Phase 4：HTML 课程外壳（verbatim）
scripts/index_repo.py               Phase 0：大型仓库代码索引（纯标准库）
```

## 设计公理

> **智能在出口，进阶在闸门。**

tutor（LLM）决定*教什么、怎么提问、怎么讲解*。但能否*进阶*永远是**确定性引擎判定**，绝不是模型自我感觉。这是从 DeepTutor 的 mastery capability 移植的最重要设计决策。

两个推论：

1. **判定永不漂移** —— 待判定题目的期望答案存在 `progress.json` 服务端，永不回传给学习者。
2. **进阶是算出来的，不是叙述出来的** —— `next_objective` 从"已掌握的内容"推导下一步（闸门即光标），绝不是阶段计数器。

## 掌握度引擎

移植自 DeepTutor 的 `learning/` 模块。四种知识类型对应两种闸门：

| type | 闸门 | 通过条件 |
|---|---|---|
| `memory` | 定量 | 近因加权准确率 ≥ 0.9 |
| `procedure` | 定量 | ≥ 0.9 + 动手证据 |
| `concept` | 定性 | tutor 判定费曼复述 |
| `design` | 定性 | 复述 + 设计权衡追问 |

### 定量掌握度（`compute_mastery`）

- 最近至多 5 次的近因加权准确率，权重 `(0.5, 0.7, 0.85, 0.95, 1.0)`。
- **置信度上限**：1 次记录封顶 0.5，2 次封顶 0.8 —— 一次蒙对到不了 0.9 闸门。

### 间隔重复

每种类型独立间隔序列（`memory` `[0,1,3,7,14,30]`、`concept` `[3,7,14,30]`、`procedure` `[3,7,14]`、`design` `[14,28]`），错误记录会提升该知识点的复习优先级。

### 错误诊断

四类元认知分类：`structural`（缺前置知识）、`deviation`（概念理解偏差）、`application`（概念对但场景用错）、`metacognitive`（不知道自己不知道）。每条记录用户自述归因 + tutor 确认 + 重试历史。

### Fluency vs storage（吸收自 teach skill）

整个引擎是一台对抗"流利度幻觉"的机器：置信度上限、费曼复述、间隔复习存在的意义，就是只有"遗忘后还能检索出来"（存储强度）才算掌握。

## 四个阶段

### Phase 0 — 复杂度评估
判断仓库规模（源文件 < 10 万行、顶层模块 < 20、依赖简单 → 中小型；否则大型）。中小型：纯 skill 直接读。大型：运行 `scripts/index_repo.py` 生成 `code-map.json`，按需定位源码。

### Phase 1 — 客观预扫描 → 课程地图候选
explore_context 式只读预扫描（先摸清，不急着下结论），再按弧线 *first win（构建）→ 架构心智模型 → 核心工作流 → 关键实现 → 动手 → 排错 → 深入参考* 生成 4–8 个模块的课程地图。每个模块/知识点都带源码证据。

### Phase 2 — Mission + 地图确认（强制）
先确立 **MISSION.md**（为什么想掌握这个仓库 —— 让教学有根基），再把候选地图呈现给用户删改、调整并批准。未经批准绝不开始学习。

### Phase 3 — 交互式掌握度学习
每个知识点：`诊断（test-out）→ 讲解（基于源码）→ 费曼检验 → 练习（测验 / 动手）→ 错误诊断 → 间隔复习调度`。每轮结束原子写回 `progress.json`、自动沉淀笔记、更新全局记忆。

### Phase 4 — 双形态课程合成
合成 `COVERAGE.md`（全量 Markdown），可选复用 `html-shell/` 外壳生成可分享 HTML 课程（verbatim 复制，绝不重新生成）。HTML 版刻意以架构为中心（图、依赖图、调用链），与 docs-to-course 的"偏 UI 步骤条"相反。

## 数据模型

```text
<目标仓库>/.learning/
  ├── MISSION.md            为什么想掌握这个仓库
  ├── course-map.json       已确认的模块 + 知识点 + 阈值
  ├── progress.json         掌握度、重复状态、错误记录、待判定题目
  ├── records/NNNN-slug.md  ADR 式学习记录（带 supersession）
  ├── notes/<module>.md     结构化笔记（自动 + /note）
  ├── briefs/<module>.md    预提取源码片段（大型仓库）
  ├── code-map.json         大型仓库索引（可选）
  └── .gitignore
~/.repo-mastery/            全局轻量记忆（profile.md, index.json）
```

关键不变量：

- `.learning/` 自动 gitignore，目标仓库不被污染。
- `progress.json` 原子写回（临时文件 + rename）。
- `pending_question.expected_answer` 绝不出现在题目文本。
- 全局记忆保存跨会话续学状态（不做 L1/L2/L3 分层 —— 刻意轻量）。

## 出处

本 skill 由三个成熟设计的组合：

- **DeepTutor**（HKUDS，MIT）：掌握度引擎、闸门、间隔重复、错误诊断、`PendingQuestion`、`explore_context` 预扫描。
- **docs-to-course**（codebase-to-course）："reference → route" 课程弧线、测验哲学、模块简报预提取、HTML 课程外壳。
- **mattpocock teach**：Mission、ZPD、ADR 式学习记录、fluency vs storage、选项格式、检索练习。

逐条归属说明：[ADOPTION.md](../../ADOPTION.md)。

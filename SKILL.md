---
name: repo-mastery
description: "把任意开源仓库变成开发者视角的掌握式课程。输入本地仓库路径或 GitHub URL，通过 课程地图确认 → 交互式掌握度学习（诊断/讲解/费曼检验/练习/间隔复习）→ 动手实践 → 笔记沉淀 → 合成完整课程文档，帮助你像学一门课一样逐步掌握一个项目的 使用 → 架构 → 关键实现。触发词：'学会这个仓库'、'把 xx 变成课程'、'深入学习 xx 项目'、'掌握这个代码库'、'从源码学习'。"
---

# Repo-Mastery — 从源码掌握一个开源项目

> 把任意开源仓库变成**开发者视角的掌握式课程**。你不是在"浏览代码"，而是在像学一门课一样逐步掌握它的 **使用 → 架构 → 关键实现**，并且每一点都有掌握度判定、间隔复习和笔记沉淀。

## 与 docs-to-course 的区别

本 skill **不吃文档、面向开发者**。目标学习者是你 —— 一个想彻底理解某个开源项目是怎么被构建出来的开发者，而不是想学会"怎么用"的终端用户。因此：

- 输入是**源码仓库**（本地路径或 GitHub URL），不是文档站。
- 学习深入到**内部实现**：架构、设计决策、核心算法 —— 这是重点，不是"表面操作"。
- 驱动方式是**交互式掌握度学习**，不是一次性生成静态课程。
- 产出是**可续学的学习状态** + 完整课程文档（Markdown + HTML 双形态）。

> 方法论上它站在 `docs-to-course` 的肩膀上：课程设计弧线、测验哲学、模块简报预提取、HTML 课程外壳都直接吸收自它；掌握度引擎（确定性闸门、间隔重复、错误诊断）吸收自 DeepTutor 的 `learning` 模块。

## 核心设计公理（必须始终遵守）

> **智能在出口，进阶在闸门。** 你（tutor）决定教什么、怎么提问、怎么讲解；但"能否进阶"永远是**确定性引擎判定**，绝不是让 LLM 自己拍脑袋说"你掌握了"。

- 定量判定（memory / procedure 型）：`compute_mastery()` 近因加权准确率 ≥ 0.9，且受置信度上限约束 —— **一次蒙对不算掌握**。
- 定性判定（concept / design 型）：费曼式复述由你判定（`mastery_assess`）。
- 进阶由"已掌握的内容"计算而来（`next_objective`），**绝不是阶段计数器**。已证明掌握的知识点自动跳过（test-out 路径）。

---

## 命令表

```bash
/repo-mastery start <本地路径 | github:owner/repo>   # 主流程：地图→确认→学习→产出
/repo-mastery continue                                # 续学上次进度（回到 next_objective 指向的知识点）
/repo-mastery review                                  # 触发间隔复习会话（到期知识点）
/repo-mastery note "<文本>"                           # 手动向当前模块笔记追加（想法/疑问/卡点）
/repo-mastery status                                  # 查看当前进度（map_summary 风格）
/repo-mastery report                                  # 生成掌握度报告 MASTERY.md
/repo-mastery export [--html]                         # 合成完整课程文档（COVERAGE.md，--html 额外生成 HTML 版）
```

---

## 主流程（`/repo-mastery start`）

### Phase 0 — 复杂度评估（决定提取方式）

先对仓库做一次快速规模判断，**再决定用哪种方式消化源码**：

| 指标 | 中小型 | 大型 |
|---|---|---|
| 源文件（`src/` + 非测试）行数 | < 10 万行 | ≥ 10 万行 |
| 顶层模块/包数量 | < 20 | ≥ 20 |
| 依赖复杂度 / 多语言混编 | 简单 | 复杂 |

- **中小型** → 纯 skill 直接读源码（Grep/Glob/Read + explore_context 式预扫描），无需 Python 依赖。
- **大型** → 先运行 `scripts/index_repo.py` 生成 `code-map.json`（模块/依赖/符号表，见 `references/index-script-spec.md`），课程地图基于它构建，学习时按需从索引定位源码，避免整仓塞进上下文。
- 判断不确定时，用 `find` + `wc -l` 实际数一下，不要猜。

### Phase 1 — 预扫描 → 课程地图候选

以 **explore_context 式客观预扫描**开始：先冷静地把仓库摸清楚（读 README、入口文件、目录结构、构建配置、核心模块），**不要边看边给结论**。然后按 `references/curriculum-design.md` 生成课程地图候选：

```jsonc
{
  "repo": "owner/name",
  "summary": "一段客观的仓库概览",
  "modules": [
    {
      "id": "m01",
      "name": "跑通构建与环境",
      "order": 1,
      "pass_threshold": 0.7,
      "knowledge_points": [
        {"id": "kp01-01", "name": "如何从零构建并运行", "type": "procedure"},
        {"id": "kp01-02", "name": "项目目录结构的心智模型", "type": "concept"}
      ]
    }
    // ...
  ]
}
```

**模块弧线**（吸收自 docs-to-course 的"reference → route"，为源码学习改造）：

> **first win（跑通构建）→ 整体架构心智模型 → 核心工作流/模块 → 关键实现 → 动手实验 → 排错 → 深入参考**

这是菜单不是清单 —— 按仓库实际选 4–8 个模块，少而深胜过薄而多。知识点的 `type` 决定它的判定方式（见 `mastery-policy.md`）。

### Phase 2 — 课程地图确认与定制（用户决策，不可跳过）

把候选地图**呈现给用户**，逐模块说明，然后：

- ✅ 用户删掉不关心的模块 / 增加感兴趣的模块 / 调整知识点粒度。
- ✅ 用户确认每个模块的 `pass_threshold`（默认 0.7）。
- ✅ **用户批准后**才开始学习。这是强制步骤 —— 和 docs-to-course 的"不要给大纲审批"相反。

确认后写入 `<repo>/.learning/course-map.json`，并初始化 `.learning/` 结构（见下）。

### Phase 3 — 交互式掌握度学习

按 `references/session-flow.md` 驱动。核心循环（每知识点）：

> **诊断（已知多少，可 test-out 跳过）→ 讲解 → 费曼检验 → 练习（定量测验 / 按需动手）→ 错误诊断 → 间隔复习调度**

- 下一站永远由 `next_objective` 决定（优先级：待判定的题 → 到期的复习 → 第一个未掌握的知识点 → 完成）。
- 定量判定（memory/procedure）：出题，按 `mastery-policy.md` 的 `compute_mastery` 计算，≥0.9 才算掌握。
- 定性判定（concept/design）：让用户用费曼复述，你判定 `passed`，不过则回炉。
- **按需动手**：procedure 型知识点引导用户实际跑（构建/测试/写 demo 验证）。只读命令（`build`、`test` 等）可直接运行；**写操作（改文件、装依赖）必须先经用户批准**。动手结果作为掌握证据记录。
- **自动沉淀笔记**：每次讲解/判定后自动写入 `<repo>/.learning/notes/<module>.md`（格式见 `note-template.md`）；用户随时 `/repo-mastery note "..."` 追加。
- **命令执行约定**：本 skill 需要运行仓库命令时，默认只运行只读/无副作用命令；任何会修改用户文件系统或安装依赖的操作，先把命令展示给用户并请求批准。

### Phase 4 — 合成完整课程文档（双形态）

学习到完成（或用户主动 `/repo-mastery export`）时，把 **课程地图 + 讲解笔记 + 用户实践记录 + 掌握度与卡点** 合成为完整课程文档：

1. **Markdown 全量版** `COVERAGE.md`：完整内容，含代码引用、模块讲解、掌握度、卡点、复习排期。这是主产物。
2. **HTML 分享版**（`/repo-mastery export --html`）：**复用 `references/html-shell/` 的成品外壳**（styles.css / main.js / _base.html / _footer.html / build.sh —— 复制 verbatim，绝不重新生成），把 COVERAGE.md 的模块内容转化为 `modules/0N-slug.html`，用 `build.sh` 装配出 `index.html`。交互元素（flow 动画、group chat、glossary tooltip、情景测验）按 `references/html-shell/interactive-elements.md` 的模式添加。

> 注意：HTML 版的视觉应服务"源码理解"——**架构图、依赖图、调用链是核心内容**，这与 docs-to-course 的"偏 UI 步骤条"相反。

---

## 数据结构

```
<目标仓库>/.learning/                  ← 随仓库走，自动写 .gitignore 避免误提交
  ├── course-map.json      课程地图（已确认版）
  ├── progress.json        LearningProgress（掌握度/间隔复习/卡点，见 mastery-policy.md）
  ├── notes/<module>.md    结构化笔记（自动沉淀 + /note 追加）
  └── .gitignore           含 ".learning/"
~/.repo-mastery/                     ← 全局轻量记忆（不做 L1/L2/L3 分层）
  ├── profile.md           跨仓库偏好/水平/卡点总结
  └── index.json           学过的仓库清单与状态（上次学到哪）
```

进度采用 JSON 文件、每知识点为一条记录；**待判定题目的期望答案存在服务端（progress.json），绝不回传给你复述** —— 判定永不漂移（吸收 DeepTutor 的 `PendingQuestion` 设计）。

---

## 参考文件（按阶段读取，保持上下文精简）

- `references/curriculum-design.md` — **Phase 1**：从源码设计课程地图
- `references/mastery-policy.md` — **Phase 3**：掌握度计算、闸门、间隔复习、错误诊断
- `references/session-flow.md` — **Phase 3**：交互式学习会话协议
- `references/quiz-design.md` — **Phase 3**：测验设计原则（测应用，不测记忆）
- `references/module-brief-template.md` — **Phase 3 大型仓库**：预提取源码片段，省 token
- `references/note-template.md` — **Phase 3**：笔记格式
- `references/gotchas.md` — 全程：失败点检查清单
- `references/index-script-spec.md` — **Phase 0 大型仓库**：Python 索引脚本说明
- `references/html-shell/` — **Phase 4**：HTML 课程外壳（复制 verbatim）

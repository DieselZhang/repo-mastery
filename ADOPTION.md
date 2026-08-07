# ADOPTION — 采纳与吸收说明

本 skill 站在两个上游的肩膀上：**DeepTutor**（HKUDS 开源，MIT）与 **codebase-to-course**（即 docs-to-course，个人技能）。本文说明各自被采纳/吸收了什么，以及为什么。

## 1. 从 DeepTutor（HKUDS，MIT）采纳：掌握式学习引擎

DeepTutor 是一个 agent-native 智能学习平台。本 skill 将其 `learning/` 模块的核心教育学设计移植过来，只把"学科知识"替换为"代码知识"：

| 采纳的设计 | 来源（DeepTutor 模块） | 在 repo-mastery 中的落点 |
|---|---|---|
| **设计公理：智能在出口，进阶在闸门** —— 模型决定教什么、怎么提问；能否进阶由确定性引擎判定 | `capabilities/mastery/capability.py` | `SKILL.md` 核心公理 |
| **定量掌握度**：近因加权准确率 + 置信度上限（一次蒙对不算掌握） | `learning/mastery.py` | `mastery-policy.md` §2 |
| **进阶由已掌握内容计算，闸门即光标**（test-out 跳过已掌握） | `learning/policy.py` `next_objective` | `mastery-policy.md` §4 |
| **间隔重复**：每知识类型不同间隔序列 + 错题提升优先级 | `learning/scheduler.py` | `mastery-policy.md` §3 |
| **错误诊断四分类**：结构性/理解偏差/应用错误/元认知 | `learning/models.py` `ErrorType` | `mastery-policy.md` §5 |
| **确定性测评**：期望答案存服务端、永不回传模型 | `learning/models.py` `PendingQuestion` | `mastery-policy.md` §7 |
| **explore_context 预扫描**：先客观吃透材料再进讲解循环 | `capabilities/explore_context/` | `SKILL.md` Phase 1 |
| **笔记作为可复用上下文** | `tools/write_note` + notebook | `note-template.md` |

DeepTutor 采用 MIT License（见其仓库 `LICENSE`），本 skill 对以上设计的移植已在其各 reference 文件中标注来源。

## 2. 从 codebase-to-course（docs-to-course）吸收：课程设计与产出外壳

codebase-to-course 是一个"把工具文档变成终端用户使用课程"的个人技能（安装于 `~/.claude/skills/codebase-to-course`）。本 skill 吸收其方法论与产出外壳，但**学习者与目标完全不同** —— 它服务"学会用工具的终端用户"，本 skill 服务"要吃透源码的开发者"：

| 吸收的内容 | 来源文件 | 在 repo-mastery 中的落点 | 改造 |
|---|---|---|---|
| **"reference → route" 课程设计**：把查找型材料重排为渐进学习路线，模块弧线（first win → mental model → core workflows → …） | `references/curriculum-design.md` | `curriculum-design.md` | 模块弧线改造为代码学习版（跑通构建 → 架构心智 → 核心工作流 → 关键实现 → 动手实验 → 排错） |
| **单模块弧线**：objectives → why care → 概念+比喻 → 看它/做它 → recap → quiz | `references/curriculum-design.md` | `session-flow.md` explain 环节 | 落地为学习会话的讲解骨架 |
| **测验哲学**：测应用不测记忆（场景题/追踪题/权衡题优先） | `references/content-philosophy.md` | `quiz-design.md` | 题目类型改为代码理解（调用链追踪、扩展点选择、排错） |
| **模块简报预提取**：写内容前预提取片段，writer 不再重读原文（省 token） | `references/module-brief-template.md` | `module-brief-template.md` | 预提取对象从"命令/配置"改为"源码片段 + 文件:行" |
| **HTML 课程外壳**：styles.css / main.js / _base.html / _footer.html / build.sh，复制 verbatim 绝不重新生成 | `references/`（styles.css 等） | `references/html-shell/` | 外壳原样复用；交互元素按既有 class/data-* 约定 |
| **交互元素模式**：flow 动画、group chat、glossary tooltip、情景测验 | `references/interactive-elements.md` | `references/html-shell/interactive-elements.md` | 原样复用 |
| **repo-first ingest 原则**：优先 clone 仓库而非爬网站 | `references/ingest.md` | `SKILL.md` Phase 0 | 本 skill 天然处理源码，印证该原则 |

### 刻意不吸收的部分（学习者不同，反向设计）

- ❌ "面向终端用户、偏 UI 步骤条而非内部架构图" —— repo-mastery 相反，**架构图/依赖图/调用链是核心内容**。
- ❌ "不要给课程大纲审批，直接建" —— repo-mastery **强制课程地图确认**（用户决策，不可跳过）。

## 3. 从 mattpocock teach skill 借鉴：学习机制补强

[mattpocock-skills](https://github.com/mattpocock) 的 `teach` skill（教学型 skill）提供了几个本 skill 没有但很有价值的学习机制，已吸收（见 v1.1.0）：

| 借鉴点 | teach 的做法 | 在 repo-mastery 中的落点 |
|---|---|---|
| **Mission 驱动** | `MISSION.md` 记录用户学它的"原因"，ground 所有教学 | `SKILL.md` Phase 2 先问"为什么想掌握这个仓库"，写 `.learning/MISSION.md` |
| **Learning records（ADR 式）** | `learning-records/` 记录非显而易见的学习、前置知识、被纠正的误解，带 supersession | `references/learning-records-template.md` + `.learning/records/NNNN-slug.md` |
| **ZPD（最近发展区）** | 每次挑战"刚好够"，由 records + mission 计算 | `mastery-policy.md` §0 + `session-flow.md` §0 |
| **Fluency vs Storage** | 流利度给虚假掌握感，存储强度才是目标 | `mastery-policy.md` §0（闸门 + 间隔重复的原理依据） |
| **引用一手来源** | 每课推荐高质量一手资源 | `note-template.md`"资源/一手来源"节 |
| **测验不给格式线索** | 各选项同字数 | `quiz-design.md`"选项格式"节 |
| **检索练习优先** | 逼从记忆检索而非识别 | `quiz-design.md`"检索练习优先"节 |

## 4. 版权与许可

- 本仓库：MIT License，见 `LICENSE`。
- DeepTutor 设计移植：© 2026 HKUDS，MIT License（[github.com/HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor)）。
- codebase-to-course 外壳：© 2026 DieselZhang。
- mattpocock teach 机制借鉴：© mattpocock（[mattpocock-skills](https://github.com/mattpocock)）。

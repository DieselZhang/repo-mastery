# Changelog / 变更日志

本文件记录 Repo-Mastery 各版本的显著改动，供发版与回顾使用。
All notable changes to Repo-Mastery are documented here, for releases and review.

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循
[Semantic Versioning](https://semver.org/lang/zh-CN/)。
Format follows [Keep a Changelog](https://keepachangelog.com/), versioning follows
[Semantic Versioning](https://semver.org/).

> **追溯说明 / Provenance**：v1.0.0–v2.4.0 的日期取自 git commit；v2.5.0–v2.9.0 的
> 改动在 git 仓库**从未提交**（留存在本地工作区），日期按会话记录与记忆文件时间追溯
> 估计——v2.5.0 / v2.6.0 为推断值。v2.10.0 为本轮发版。
>
> v2.5.0–v2.9.0 were never committed to git (they lived in the working tree); their
> dates are reconstructed from session notes and memory-file timestamps — v2.5.0 /
> v2.6.0 are inferred. v2.10.0 is the current release.

---

## [2.10.0] — 2026-08-11 — Command-surface cut / 命令面精简

**移除 Removed**
- `/repo-mastery chapter` 命令砍除——教材式章节已是进入新模块的默认流程（auto-start），
  命令只剩 `--module` 固定重学与 `--html` 两个边角用途；显式重学改走自然语言（"重讲 m02 教材"）。
  (The `chapter` command is gone — textbook-mode chapters auto-start on entering each
  new module, so the command only served pinned re-walks and `--html`; re-walking a
  module's chapter is now a natural-language request.)
- `/repo-mastery export` 命令砍除——COVERAGE.md 本就随学习逐模块增量更新；可分享 HTML
  课程改为 **start 时询问一次**（Phase 2 确认时问是否生成，复用 `references/html-shell/`
  copy verbatim）+ **课程完成时按需刷新**，输出到 `<repo>/.learning/export/`。
  (The `export` command is gone — COVERAGE.md updates per module anyway; the shareable
  HTML course is now decided once at start and refreshed at completion, into
  `<repo>/.learning/export/`.)

**更改 Changed**
- 命令面从 9 概念（bare + 8 命令）精简到 **6 命令**：preview / start / continue /
  review / note / status。(The command surface shrinks from 9 concepts — bare + 8
  commands — to **6 commands**.)
- bare `/repo-mastery`（无子命令）并入 `continue`——按 `.learning/` 状态智能路由
  （无状态 → 引导 start / 未完成 → preamble + 续学 / 已完成 → 报告）。
  (A bare `/repo-mastery` is now `continue`, routing on `.learning/` state.)
- `chapters/` 路径修正为 `.learning/` 顶层（此前协议文本误写 `notes/chapters/`）。
  (Chapter material path corrected to top-level `chapters/`, was mis-written
  `notes/chapters/`.)
- `--fresh` 补进 README 命令表与 Usage（此前仅 SKILL.md 有）。(`--fresh` now
  documented in the READMEs.)

**未变 Unchanged**
- 引擎零改动（`learning_engine.py`）——`chapter-start/advance/complete` 与
  `set-qualitative` 保持 v2.7 原样。(Engine untouched — only the skill-layer command
  surface moves.)
- `docs/` 不同步（停在 v2.0）。(`docs/` stays at v2.0.)

---

## [2.9.0] — 2026-08-11 — Note interval consolidation / note 区间化

**更改 Changed**
- `/repo-mastery note` 重设计——从「把 `<text>` 逐字追加到笔记」改为「**区间对话分类
  归纳**」：整理自上次 note 以来（`notes/.boundary.json` 记录的区间）的 Q&A 结论、新
  blockers、cheatsheet 增补、Feynman 记录，**去重**写入模块笔记（不重写 auto-consolidate
  已落盘内容），并产出 `### 区间整理` recap 块。(`note` now consolidates the discussion
  since the last note — deduplicated against the auto diary — instead of appending text.)

**新增 Added**
- `notes/.boundary.json`（`{"module_id": ..., "last_consolidated_at": <unix>}`）——
  区间边界，tutor 直接读写。(Interval boundary file, read/written by the tutor.)

**未变 Unchanged**
- 引擎零改动；可选 `<text>` 仍逐字进 My notes（不改写用户原话）。
  (Engine untouched; optional `<text>` still goes verbatim into My notes.)

---

## [2.8.0] — 2026-08-11 — Ecosystem positioning / 生态定位视角

**新增 Added**
- Phase 2 外部生态检索：价值简报前先做差异化定位，事实分三类——仓库事实 `[src]` +
  `file:line`、生态事实 `[web]` + URL + 访问日期、未核实 tutor-memory 声明 `[unv]`
  （仅作搜索种子，永不进入 gated 参考答案）。(Sourced ecosystem comparison — three
  fact classes `[src]` / `[web]` / `[unv]` — feeding the value brief's differentiation.)
- `positioning.md`（差异化对比矩阵）+ MISSION.md 的价值定位总结。(Positioning matrix
  file; MISSION carries the value-positioning summary.)

**未变 Unchanged**
- 引擎零改动——仅 Phase 2 协议扩展。(Engine untouched — a Phase 2 protocol extension.)

---

## [2.7.0] — 2026-08-10 — Textbook-mode chapter learning / 教材式章节

**新增 Added**
- 默认学习路径改 **教材式（翻转课堂）**：生成整章材料 `chapters/<module>.md` → 逐节
  讲解（**每节停等确认**，绝不连续推进）→ 课后答疑 → 课后检验（1–2 个关键节点深度题，
  走引擎判定）→ `chapter-complete` 模块级闸门。(Flipped-classroom textbook mode becomes
  the default path — full chapter material, section-by-section walk with a confirmation
  pause after each section, after-class Q&A, key-node checking, module-level gate.)
- 引擎命令 `chapter-start` / `chapter-advance` / `chapter-complete` + `chapter` 状态机。
  (Engine gains the chapter state machine and its three commands.)
- covered 模块三态显示：`未掌握` / `已覆盖 · 待复习验证` / `已掌握`——covered ≠ 未掌握。
  (Three-state display for covered modules — covered ≠ unmastered.)

**更改 Changed**
- 逐点交互模式降级为**补充**（test-out / 单点深挖 / 复习后重教），不再是平行学习路径。
  (Per-point interactive mode becomes a supplement — test-out, single-point deep-dive,
  post-review reteach — not a parallel path.)

**引擎改动 Engine changes**：`learning_engine.py` 新增 chapter 状态（本次是引擎改动版）。

---

## [2.6.0] — 2026-08-10 — Grill-me reference-answer interaction / 参考答案对照

**更改 Changed**
- Phase 3 学习交互改 **参考-答案-优先（grill-me 式）**：讲一个点 → 给参考答案（一行
  标准陈述 + `file:line`）→ 用户对照讨论（同意/反驳/用自己的话复述），而非空白作答；
  procedure 级评分题在**作答后**立即显示参考答案供自检。(Learning interaction becomes
  reference-answer-first — after explaining, present a reference answer and let the
  user react to the proposal; a graded procedure question shows the answer right
  *after* answering, for self-check.)

**新增 Added**
- `quiz-design.md` "Reference-answer interaction"、`mastery-policy.md` §6、`session-flow.md`
  §2–4 的对照讨论协议。(The reference-answer protocol lands in quiz-design /
  mastery-policy / session-flow.)

---

## [2.5.0] — 2026-08-10 — Learning-pace redesign / 学习节奏重构

（源自真实试学反馈 + 已采纳资产，非新 upstream。From field feedback + existing assets.)

**更改 Changed**
- 澄清前先讲**价值简报**——「这个仓库能教你什么、相对同类强在哪」先于 Mission 澄清。
  (Value brief precedes the Mission clarification.)
- **全貌先于节点**（overview-first）——全局概览 → 模块概览 → 关键节点讨论，引擎
  `flow_phase` 强制，`next-objective` 在概览未呈现前拒绝发点。(Overview-first —
  engine-enforced by `flow_phase`.)
- `memory` 点降级为 reference cheatsheet——参数/命令拼写不再设闸门（不构建可迁移能力）。
  (`memory` points demoted to reference cheatsheets — no gate on parameter/command trivia.)
- 课程笔记**早期生成、持续更新**——Phase 2 确认后即生成首稿 COVERAGE.md，随学习逐模块
  增量更新（HTML shell 复用规则不变）。(Course note generated early, updated per module.)

**引擎改动 Engine changes**：`learning_engine.py` — `next_objective` 不再催 memory 点、
`flow_phase` 门生效。

---

## [2.4.0] — 2026-08-09 — Evidence-based memory mechanisms / 记忆机制

**新增 Added**
- FSRS 式**个性化排程**（difficulty + stability 缩放复习间隔，纯确定性公式）。
  (FSRS-inspired personalized scheduling — two-parameter DSR model, pure deterministic.)
- 复习类型**交错**（`last_review_type`）+ 会话回顾热身 + streak。(Interleaved review
  types, session recall warm-up + streak.)
- 生动编码（SMASHIN）、因果提问（why / what-if / what breaks）。(Vivid encoding,
  causal questioning.)
- 闪卡质量标准（quiz-design，强制回忆 / 一卡一事实 / 精化连接）。
  (Flashcard quality standards in quiz-design.)
- 记忆机制反模式（gotchas）。 (Memory-mechanism anti-patterns in gotchas.)

**引擎改动 Engine changes**：`learning_engine.py` — `schedule_next` 等排程逻辑。

---

## [2.3.0] — 2026-08-08 — Grilling clarification absorption / 澄清面试吸收

**新增 Added**
- 澄清面试协议 `clarification-interview.md`（吸收 grilling skill）：决策树遍历、**一次
  一个问题**、事实与决策分离、每个决策问题带推荐答案、共享理解闸门。
  (Clarification-interview protocol absorbed from grilling — decision-tree walk, one
  question at a time, facts vs decisions, recommended answer per decision, shared-
  understanding gate.)
- Phase 2 确认改为**决策树澄清**（Mission + 地图确认）。 (Phase 2 confirmation driven
  as a decision-tree clarification.)
- 澄清反模式（gotchas）。(Clarification anti-patterns in gotchas.)

---

## [2.2.1] — 2026-08-07 — Version sync + secret guard

**更改 Changed**
- 版本号同步；`.gitignore` 增加密钥防护。(Version sync; `.gitignore` secret guard.)

---

## [2.2.0] — 2026-08-07 — One-command & native installs / 安装方式

**新增 Added**
- **五种安装方式**：npm 一条命令、curl 管道、Claude Code 原生插件（marketplace +
  plugin）、对话安装、手动 clone。(Five install paths: npm one-command, curl pipe,
  native Claude Code plugin, conversation-driven, manual clone.)
- 各工具查找位置矩阵（Claude Code / Codex / Gemini / AGENTS.md 工具）+ 工作流 hero 图。
  (Per-tool install matrix + workflow hero image.)

---

## [2.1.0] — 2026-08-07 — Multi-CLI support + real engine / 多 CLI + 确定性引擎

**新增 Added**
- 多 CLI 支持：`AGENTS.md`（Codex / opencode / Cursor）+ `GEMINI.md`（Gemini CLI）
  协议。(Multi-CLI protocol files for AGENTS.md tools and Gemini CLI.)
- **真实确定性引擎** `scripts/learning_engine.py`（纯标准库）——掌握度闸门、间隔复习、
  排程、record-attempt、next-objective 的真代码。(The deterministic engine becomes real
  code — pure stdlib — shared by every tool so mastery math never drifts.)

---

## [2.0.0] — 2026-08-07 — Full English skill + formal docs / 全英文 + 正式文档

**更改 Changed**
- 项目重新定位为**跨工具 Agent skill**（非 Claude Code 专用），遵循 Agent Skills 标准。
  (Repositioned as a tool-agnostic Agent skill, not Claude Code-specific.)
- 全英文 skill + 双语正式文档（`docs/ARCHITECTURE.md` / `docs/USAGE.md` / `docs/zh-CN/`）。
  (Full English skill + bilingual formal documentation.)

---

## [1.1.0] — 2026-08-07 — ECC conventions + teach-skill mechanisms

**更改 Changed**
- ECC 规范整理；吸收 teach skill 学习机制——Mission、ZPD、学习记录（ADR 式）、
  fluency vs storage。(ECC conventions; teach-skill mechanisms absorbed — Mission,
  ZPD, learning records, fluency vs storage.)

---

## [1.0.0] — 2026-08-07 — Initial release / 初始发布

**新增 Added**
- repo-mastery skill 初始发布：把开源仓库转成开发者视角的掌握式课程。
  (Initial release — turn any open-source repository into a developer-focused
  mastery course.)

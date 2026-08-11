# Preview Brief — 探路（宏观信息，不建课）

> **Read in**: Phase 0 之前（可选前置）。用户拿到一个新项目，可能只想先看
> 「这是什么、架构长啥样、功能差异点、哪些值得深学」，**是否开课后续再定**。
> `preview` 就是这条探路入口——**只产出宏观简报，不建 `.learning/`、不调引擎、
> 不写任何文件**（零副作用）。

## 1. Trigger

`/repo-mastery preview <local-path | github:owner/repo>` — 用户想先探路，尚未确认开课。

## 2. Output — the macro brief (in chat, five sections)

1. **这是什么** — 一句话定位 + 技术栈 + 规模（代码行数 / 顶层模块数；大仓可临时
   用 `index_repo.py` 出 `code-map.json` 定位，但**不落盘到 `.learning/`**）。
2. **架构全景** — 入口 → 核心数据流 → 关键模块，1-2 段叙事（复用 Phase 3.0 全局
   概览的产出风格，见 `session-flow.md`）。
3. **功能差异点 vs peers** — 2-4 行，**`[src]` / `[web]` 标注**（来源纪律同
   `positioning-brief.md`：repo 事实 `file:line`，peer 事实 `[web]` + URL，无来源
   标「需验证」，从不编造；**preview 不落盘 `positioning.md`**——那是 start 开课
   才建的完整矩阵）。
4. **关键实现亮点** — 3-5 个最值得学的点，每个给 `file:line` 证据。
5. **建议深学候选** — 哪些模块/点值得开课（作为 start 的 course-map 提案输入）。

## 3. Zero side effects (hard)

- 不建 `.learning/`，不写 MISSION / positioning / course-map / progress / notes。
- 不调引擎（无 state 变更）；`index_repo.py` 只在大仓临时生成 `code-map.json`
  （放 `/tmp` 或原地读，**不**放进 `.learning/`）。
- 不 Mission 澄清、不地图确认——那属于 start。preview 结束即结束，无残留。

## 4. Handoff to start (deep-dive)

用户看完说「深学」→ 同一会话直接 `/repo-mastery start <repo>`：preview 的简报
（架构叙事 + 差异点 + 亮点）作为 Phase 2 value brief 的输入，跳过重复探路，直接
进 Phase 1 course-map 提案 + Phase 2 Mission/确认。preview 不落盘，start 会基于
简报建立正式文件（MISSION.md / positioning.md / course-map.json）。

跨会话衔接（用户稍后才说深学）→ start 重新走 Phase 0/1/2，简报在 start 时重产。

## 5. 与 positioning-brief.md 的关系

preview 是**轻量探路**（对话内简报，不落盘、不建矩阵）；positioning-brief 是
**开课定位**（Phase 2 建 `positioning.md` 完整对比矩阵，驱动课程裁剪）。两者共用
同一条 `[src]`/`[web]` 来源纪律；preview 从不写 positioning.md，也不建定位矩阵。

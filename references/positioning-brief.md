# Positioning Brief — 生态定位与差异化（读于 Phase 2）

> **Read in**: Phase 2. Turns the value brief's "what makes it stand out vs
> peers" from an improvised one-liner into a **sourced, persistent comparison
> matrix**. A developer learning a large open-source project wants to know
> *what it is, how it trades off against its natural peers, and when to pick it*
> before diving into architecture — this brief is that deliverable. Produces
> `<repo>/.learning/positioning.md`.

## Three names, three roles — keep them straight

| Name | Role | Kind |
|---|---|---|
| `references/positioning-brief.md` | this file — the skill's template/protocol (Phase 2) | skill reference |
| `<repo>/.learning/positioning.md` | the per-repo **persistent output** (comparison matrix + sources + decision rules) | learning artifact |
| **value brief** (existing, `clarification-interview.md` §0) | the Phase 2 in-chat proposal (teaching-capability inventory + differentiation) | conversation |

The value brief stays a conversation proposal; it is **not** merged into
`positioning.md`. Its differentiation section is *read from* `positioning.md`
— never improvised on the spot.

## Flow (Phase 2, after the Phase 1 repo-internal pre-scan)

1. **External ecosystem scan** — if a web/search tool is available
   (WebSearch in Claude Code, any MCP search), compare against the repo's
   natural peers. If not, skip straight to a repo-evidence-only brief (see
   Source rules).
2. **Produce `positioning.md` in two passes** (the Mission is settled *after*
   the value brief, so the matrix must not depend on it before it exists):
   - **Pass 1 (before the Mission interview)**: a generalized draft — the
     repo's natural peers, categorized rows. Do not over-research; breadth of
     categories first.
   - **Pass 2 (after the Mission is settled)**: prune/deepen the rows the
     Mission actually cares about (e.g. Mission = "borrow the design" →
     deepen the agent-loop/architecture rows; Mission = "use it" → deepen
     operations/ecosystem rows). Write the 3–5 line summary into `MISSION.md`.
3. **Present the value brief** — differentiation section = 2–4 key matrix rows
   + the "when to pick it" rule. Do **not** dump the full matrix into chat; it
   lives in `positioning.md`.
4. **Global overview (Phase 3.0)** later reuses the same one-liner/rows — one
   source, three touchpoints (value brief teaser → overview summary → m00
   module if kept).

## Output structure — `<repo>/.learning/positioning.md`

```markdown
# Positioning — <repo>
> 更新: <ISO date> ｜ 来源: [src]=repo 源码 · [web]=外部 URL+访问日期 · [unv]=未验证 tutor 记忆
> 生态会过期：事实变化时更新本文件，并按 learning-records 规则写学习记录。

## 一句话定位
<什么 niche、为谁、拒绝成为什么>  [src] <file:line> 或 [web] <URL>

## 生态对比表
| 同类项目 | 比较维度 | 同类做法 | 本项目做法 | 关键取舍 | 何时选本项目 | 来源 |
|---|---|---|---|---|---|---|
| <peer> | <维度> | <同类> | <本项目> | <取舍> | <判据> | [web] URL(日期) 或 [src] 或 [unv] |
| ...    | ...    | ...    | ...    | ...    | ...    | ...    |

## 何时选它 / 何时选同类（可迁移判据）
- 选本项目 if: ...
- 选同类 if: ...
- 判据（跨项目可迁移的规则）: ...

## 待验证事实（禁止混入对比表）
- <claim> — 无来源，需 WebSearch 或标 [unv]

## 反模式
- 无来源比较行 → 只能进「待验证」，禁止进对比表
- 用 tutor 记忆伪装成源码结论 → 禁止
- 外部事实进 MISSION.md / COVERAGE.md → 禁止；只进本文件
```

The matrix has **7 fixed columns** (peer × dimension × peer's approach × this
repo's approach × key tradeoff × when to pick this repo × source). Rows are
peer×dimension — one peer may appear in several rows (different dimensions).
The "when to pick it" column is the evidence anchor for m00's `kp00-03`.

## Source rules (facts never mix)

- **Repo facts** (what *this* repo does / its architecture / its code): from
  source only — cite `file:line` / README. A web result about the repo itself
  **never overrides a source walk**; the repo is the authority for itself.
- **Peer / ecosystem facts** (what a comparable project does, benchmark
  numbers, ecosystem context): from an external search **only** when a search
  tool is available. Cite `[web] <URL>` + access date. Prefer primary sources
  (official docs/README/release notes/benchmark repos) over blog posts over
  aggregator lists; 1+ URL per comparison claim when possible; when sources
  contradict, present both and note the difference instead of resolving
  silently; date-stamp every external fact.
- **`[unv]`** — an uncited tutor-memory claim. Allowed only as a *seed for a
  search* or as a row in 「待验证事实」. **Never** as a gated reference answer,
  never as a MISSION.md claim, never in a quiz.
- **Degraded mode**: no search tool → build the brief from repo evidence and
  mark peer rows `[unv]` / 「需验证」. **Never fabricate a source.**

---
name: repo-mastery
description: "Turn any open-source repository into a developer-focused mastery course. Given a local repo path or GitHub URL, it clarifies learning needs against a project value brief, confirms a course map, then drives overview-first mastery learning (whole knowledge picture, then key-node discussion with lightweight verification, spaced review) with hands-on tasks, note-taking, and a continuously-updated course note (Markdown + HTML) — so you fully master a project's usage, architecture, and key implementations like a real course. Triggers: 'learn this repo', 'master this codebase', 'turn X into a course', 'deep-dive into X project'."
origin: personal
version: 2.10.0
tags: [learning, education, codebase, mastery, spaced-repetition]
---

# Repo-Mastery — Master an Open-Source Project from Source

> Turn any open-source repository into a **developer-focused mastery course**. Instead of "browsing code", you progressively master its **usage → architecture → key implementations**, with per-knowledge-point mastery gates, spaced review, and persistent notes.

## When to Activate

Use this skill whenever any of these applies:

- The user wants to "learn / master / fully understand / deep-dive into" an open-source repo or codebase.
- The user just got a new project's source and wants systematic learning instead of random browsing.
- The user wants to understand a project's **architecture and key implementations from source** (not just how to use it).
- The user wants learning progress to **persist across sessions** (memory + spaced review).
- The user says "turn X repo into a course", "learn X from source", "deep-dive into X project".

Do **not** activate when: the user just wants a doc/README summary, a one-off code Q&A, or an end-user tutorial for a tool (that is `docs-to-course`'s job).

## Prerequisites

- **Claude Code** (the skill runtime).
- **Target repository**: a local path, or a reachable `github:owner/repo` (the skill auto-runs `git clone --depth 1`).
- **Python 3** — only needed by the large-repo indexing script `scripts/index_repo.py` (pure stdlib).
- **Write permission**: creates `.learning/` inside the target repo (auto-gitignored) and a global `~/.repo-mastery/`.

## Language

Teaching language **follows the user's input language by default** (Chinese input → Chinese teaching; English input → English teaching). You can also pass an explicit language flag:

```bash
/repo-mastery start <path|github:owner/repo> --language zh    # force Chinese
/repo-mastery start <path|github:owner/repo> --language en    # force English
```

Code, file paths, and identifiers always stay in their original form regardless of language.

## Multi-Tool Support

Repo-Mastery is not Claude Code-only. The skill follows the open **Agent
Skills** standard (agentskills.io), so the same `SKILL.md` runs natively on
**Claude Code**, **OpenAI Codex**, **Gemini CLI**, and any tool that loads
`SKILL.md` skills.

| Tool | Entry point | Install |
|---|---|---|
| Claude Code | `SKILL.md` (this file) | `~/.claude/skills/repo-mastery/` |
| OpenAI Codex | `SKILL.md` + `agents/openai.yaml` | `~/.codex/skills/repo-mastery/` |
| Gemini CLI | `GEMINI.md` + skills via `activate_skill` | its skills dir; or copy `GEMINI.md` into a project |
| AGENTS.md tools (opencode, Cursor, …) | `AGENTS.md` | clone repo or copy `AGENTS.md` into the project |

**The deterministic engine is real code, not prose** — `scripts/learning_engine.py`
implements `compute-mastery`, the spaced-repetition scheduler, `record-attempt`,
and `next-objective`. **Every gate decision MUST go through this script**, so
mastery math is identical in every tool. See `AGENTS.md` / `GEMINI.md` for the
per-tool protocol; `scripts/install.sh` installs to all tools at once.

## Difference from docs-to-course

This skill **does not read docs and targets developers**. The learner is you — a developer who wants to understand how an open-source project was built — not an end-user who wants to learn how to use it. Therefore:

- **Input** is source code (local path or GitHub URL), not a docs site.
- Learning goes **inside the implementation**: architecture, design decisions, core algorithms — that is the point, not "surface operations".
- Driving mode is **interactive mastery learning**, not one-shot static course generation.
- Output is **resumable learning state** + a complete course document (Markdown + HTML dual format).

> Methodologically it stands on `docs-to-course`'s shoulders: the course-design arc, quiz philosophy, module-brief pre-extraction, and HTML course shell are absorbed from it; the mastery engine (deterministic gates, spaced repetition, error diagnosis) is adapted from DeepTutor's `learning/` module. See `docs/ARCHITECTURE.md` and `ADOPTION.md`.

## Core Design Axiom (always hold)

> **Intelligence at the exit, advancement at the gate.** You (the tutor) decide what to teach, how to question, how to explain — but whether the learner *may advance* is always a **deterministic engine decision**, never the LLM patting itself on the back.

- Quantitative gate (memory / procedure types): `compute_mastery()` recency-weighted accuracy ≥ 0.9, capped by a confidence ceiling — **one lucky answer is not mastery**.
- Qualitative gate (concept / design types): a Feynman-style explanation judged by the tutor (`mastery_assess`).
- Advancement is computed **from what is already mastered** (`next_objective`), never from a stage counter. Knowledge points already proven are skipped (test-out path).

---

## Commands

A deliberately small surface — six commands (kept lean by learner feedback; `report` merged into `status`, `chapter` and `export` merged into the default flow — see "Textbook Mode (chapter)" and "Phase 4" below). A **bare `/repo-mastery` (no subcommand) is `continue`** — it reads the current repo's `.learning/` state and routes (see `continue` below):

```bash
/repo-mastery preview <local-path | github:owner/repo>   # Recon — macro brief only (what / architecture / differentiation vs peers / key highlights / deep-dive candidates); creates no .learning/, no Mission/map confirmation; say "深学" to hand off into start (see Preview Mode)
/repo-mastery start <local-path | github:owner/repo> [--language zh|en] [--fresh]  # Main flow: value brief → map → confirm → overview → learn (textbook-mode chapter by default per module); --fresh restarts an existing course
/repo-mastery continue                                  # Resume — smart route: no .learning/? guide to start; incomplete? session preamble first (value replay + map + progress), then due review (signposted), then new content (next_objective); complete? report done, offer restart/switch repo. (A bare `/repo-mastery` is this command.)
/repo-mastery review                                    # Spaced review only — the quick catch-up for scattered learning time; drains due reviews (bypasses the overview gate), never opens new content
/repo-mastery note ["<text>"]                           # Consolidate the discussion since the last note into notes/<module>.md (categorized); optional <text> appended verbatim to My notes
/repo-mastery status                                    # Refresh the one-page status dashboard MASTERY.md — progress, mastery %, review due, current module/chapter, next objective, covered modules — read from progress.json + course-map.json
```

`continue` and `review` share the same due-review pool but differ in scope:
learning happens in scattered moments, so a session may only have time to
revisit what's due. `continue` runs `next_objective` end to end — when it
surfaces a due review it **signposts it first** ("you have N points due for
review — let's recall them, then move on") so the shift into review never feels
abrupt. `review` is the focused entry: it drains the due-review queue and
nothing else — and it **bypasses the `flow_phase` overview gate** (`--mode
review`), so an unfinished overview never blocks scattered-time review. Both
are driven by the engine — loop `next-objective`, act on an `action: "review"`
result, and stop once it returns a non-review action (`probe` / `practice` /
`assess` / `complete`). If nothing is due, `review` says so plainly and
suggests `continue`.

**Preview mode (recon).** `/repo-mastery preview <repo>` is the
**zero-side-effect recon entrance**: before committing to a course, the user
may just want the **macro picture** — what the repo is, its architecture, how
it differs from peers, what's worth deep-learning — with no `.learning/`
created and no Mission/map confirmation. It produces a **five-section macro
brief** in chat (what / architecture / differentiation `[src]`+`[web]` / key
highlights `file:line` / deep-dive candidates) per
`references/preview-brief.md`. Say "深学" → hand off into `/repo-mastery start`
(the brief feeds Phase 2's value brief, skipping re-recon); say nothing more →
the recon ends with zero artifacts. Preview never touches the engine or writes
any file.

**Command-level mode switching.** **Textbook-mode chapter is the default on
entering each new module** — after the module overview, the tutor auto-starts
the chapter flow (`chapter-start`), unless the learner asks for the interactive
per-point mode for that module. That switch is **conversational** (e.g. "切交互式"
/ "use interactive mode") — no flag, no persistence; the next new module
defaults back to textbook mode. Before starting, the tutor gives **one line of
notice** — "默认按教材式学这个模块，想逐点交互式就说一声" — an awareness statement,
not a confirmation gate (no waiting for a reply).

**Per-point interactive mode is a supplement, not a parallel path.** It covers
three narrow uses textbook mode doesn't: (1) **test-out** — an already-known
module/point is skipped via `next_objective`'s `probe` light diagnostic, not
re-taught chapter-long; (2) **single-point deep-dive** — the learner wants to
go deeper on one knowledge point inside (or instead of) the chapter; (3)
**post-review reteach** — a point failed in spaced review gets retaught at the
point level, not by regenerating the chapter. Its discussion loop (explain →
reference answer → verify → error diagnosis → review) is the engine-gated
verification shared with textbook mode's after-class checking — a tool for
these moments, not a competing learning path. `review` (spaced recall) remains
the shared fallback that validates whatever wasn't individually checked. See
"Textbook Mode (chapter)" below.

## Session Preamble (mandatory — every resume)

Resuming a course (`continue`, or the bare command that routes into it) opens
with a **display-only replay — no questions** (user decision:
needs-clarification happens once at start's Phase 2; mid-course adjustments are
user-initiated, never an interruption). **Layered by session type**:

**Cross-session resume (fresh session / long gap — context lost): full
preamble.**
1. **Value replay** — read `MISSION.md` + `positioning.md` (if present); one
   line: *"this repo can teach you X, and stands out vs peers by Y."* — Y from
   `positioning.md`'s one-liner / decision rows, never improvised.
2. **Current map + progress** — read `MASTERY.md` (the one-page status
   dashboard): module list, done X/Y, mastery %, review due, current
   module/chapter, next objective.
3. **Due review / chapter** — if `next-objective` returns `action: "review"`,
   do that first (signposted); if it returns `action: "chapter"`, resume the
   textbook-mode chapter from its current section (`chapters/<module>.md`);
   otherwise, entering a new module defaults to the textbook-mode chapter flow
   (`chapter-start`); only per-point interactive mode proceeds to a knowledge
   point.

**Same-session continue (context already holds Mission / map / progress):
slim preamble** — one line: *"上次学到 <module/point>，下一步 <next objective>，
due <count> 条复习"* — read the numbers from `MASTERY.md`; do not re-replay the
value or map the user saw earlier this session.

Only after the preamble does the cursor advance. The overview order is
**engine-enforced**: while `flow_phase` is `overview` / `module_overview`,
`next-objective` refuses to hand out a knowledge point — the whole picture
comes first, deterministically, not as a suggestion.

---

## Main Flow (`/repo-mastery start`)

### Phase 0 — Complexity Assessment (decide how to ingest)

Make a quick scale judgment first, **then** choose how to digest the source:

| Metric | Small / Medium | Large |
|---|---|---|
| Source lines (`src/` + non-test) | < 100k | ≥ 100k |
| Top-level modules / packages | < 20 | ≥ 20 |
| Dependency complexity / multi-language | simple | complex |

- **Small / medium** → pure skill reads the source directly (Grep/Glob/Read + explore_context-style pre-scan), no Python dependency.
- **Large** → first run `scripts/index_repo.py` to generate `code-map.json` (modules/dependencies/symbol locations; see `references/index-script-spec.md`), build the course map on top of it, and locate source on demand during learning instead of cramming the whole repo into context.
- When unsure, measure with `find` + `wc -l`; do not guess.

### Phase 1 — Pre-scan → Course Map Candidates

Start with an **explore_context-style objective pre-scan**: calmly map the repo first (README, entry files, directory structure, build config, core modules) **without jumping to conclusions**. Then generate course-map candidates per `references/curriculum-design.md`:

```jsonc
{
  "repo": "owner/name",
  "summary": "an objective overview of the repo",
  "modules": [
    {
      "id": "m01",
      "name": "Build & environment",
      "order": 1,
      "pass_threshold": 0.7,
      "knowledge_points": [
        {"id": "kp01-01", "name": "Build and run from scratch", "type": "procedure"},
        {"id": "kp01-02", "name": "Mental model of the directory structure", "type": "concept"}
      ]
    }
  ]
}
```

**Module arc** (absorbed from docs-to-course's "reference → route", adapted for source learning):

> **First win (build) → overall architecture mental model → core workflows/modules → key implementations → hands-on labs → troubleshooting → deep references**

This is a menu, not a checklist — pick 4–8 modules that fit the repo; fewer, deeper beats more, thinner. The knowledge point's `type` decides its gate (see `mastery-policy.md`).

> **External ecosystem scanning is deferred to Phase 2** — Phase 1 stays repo-internal and objective; peer/ecosystem facts belong in `positioning.md`, never in the pre-scan.

### Phase 2 — Value Brief + Course Map Confirmation & Customization (user decision, never skipped)

First deliver the **value brief** (see `references/clarification-interview.md` §0): grounded in the Phase 1 pre-scan, present **what this repo can teach** (teaching-capability inventory) and **what makes it stand out vs peers** (differentiation). Before presenting it, run the **external retrieval** pass below to ground the differentiation in a sourced comparison matrix.

**External retrieval (Phase 2 only).** Position the repo against its ecosystem before the value brief — see `references/positioning-brief.md`. Two fact classes, never mixed:

- **Repo facts** (what *this* repo does / its architecture / its code): from source only — cite `file:line` / README. A web result about the repo itself **never overrides a source walk**; the repo is the authority for itself.
- **Peer / ecosystem facts** (what a comparable project does, benchmarks, ecosystem): from a web/search tool **only** when one is available (WebSearch in Claude Code, or any MCP search). Cite `[web] <URL>` + access date; prefer primary sources; date-stamp every external fact; surface contradictions rather than resolving silently.

Uncited tutor-memory claims are `[unv]` (unverified): they seed a search or a 「需验证」 row, **never** a gated reference answer, never a MISSION.md claim. The matrix lives in `<repo>/.learning/positioning.md`; MISSION.md keeps only a 3–5 line summary. If no search tool is available, build the brief from repo evidence and mark peer rows `[unv]` / 「需验证」 — **never fabricate a source**. Then, as a **decision-tree interview**, clarify the **Mission** — "which dimension matters to you, and why do you want to master this repo?" (use it? modify it? explain it in interviews? borrow its design? …). Ask one question at a time, carry an evidence-based recommended answer with each, and look up any fact the repo can settle instead of asking. Write the settled answer (incl. **Value positioning**) to `<repo>/.learning/MISSION.md`; it grounds every later teaching decision (module choices, Feynman follow-ups, mastery priority). When the Mission changes, update it and write a learning record.

Then **present the candidate map** — the full module list at once, each module with the tutor's recommended keep/adjust/drop:

- ✅ The user replies with **all adjustments in one go** ("keep m1 m2, drop m3, add a hands-on point to m2"); follow-up questions (one at a time) land **only on the modules the user adjusted**.
- ✅ Each module's `pass_threshold` **defaults to 0.7**; adjusted only on explicit request — never polled module by module.
- ✅ **Learning starts only after user approval.** This is mandatory — the opposite of docs-to-course's "don't get outline approval".
- ✅ Knowledge points are **capability points only** — `concept` / `design` / `procedure`; parameter/command trivia goes to the module's reference notes, not to the map.

> **Layered density**: the Mission decision tree (above) is asked **one question at a time** — never batched; the course-map adjustments are received as **one batch**, with follow-up only on adjusted modules. Recommended answers belong to **decision questions only**; Phase 3 assessment (quiz / Feynman) never leaks the answer.

After confirmation, write `<repo>/.learning/course-map.json`, initialize the
`.learning/` structure (below), set `flow_phase: "overview"` in `progress.json`,
and **immediately generate the first-draft course note** (see Phase 4). The
course now opens engine-forced at the global overview — no knowledge point can
be handed out until the overviews are presented (see Phase 3).

### Phase 3 — Overview-First Mastery Learning

Drive per `references/session-flow.md`. **The whole picture comes before the
nodes** — **engine-enforced**, not a suggestion. `progress.json.flow_phase`
gates `next-objective`: while it is `overview` / `module_overview`, the engine
refuses to hand out a knowledge point. Advance the phase with `set-phase` after
presenting each level (the start sequence, each step an engine action):

```bash
python3 scripts/learning_engine.py next-objective <path>/.learning/progress.json   # → {action: "overview"}
# → present the global overview, then:
python3 scripts/learning_engine.py set-phase <path>/.learning/progress.json module_overview --module m01
python3 scripts/learning_engine.py next-objective <path>/.learning/progress.json   # → {action: "module_overview"}
# → present module m01's overview, then:
python3 scripts/learning_engine.py set-phase <path>/.learning/progress.json learning
python3 scripts/learning_engine.py next-objective <path>/.learning/progress.json   # → {action: "probe"|"practice"|"review"}
```

- **Phase 3.0 — Global overview** (once): one-page architecture narrative, module map, key-implementation highlights, differentiation summary → `notes/overview.md`. No grading, no interruption. Then `set-phase module_overview --module m01`.
- **Phase 3.1 — Per module**: when the cursor enters a module, first its overview (knowledge-point map + local cheatsheet), then **textbook-mode chapter by default** (see "Textbook Mode (chapter)" below) — unless the learner switches that module to interactive per-point mode. Per-point discussion happens inside the chapter's section-by-section walk and after-class checking; the interactive per-point loop is the **supplement** (test-out / single-point deep-dive / post-review reteach), not a parallel path:

> **explain (from source, discussion-first) → give the reference answer → discuss against it (user reacts to the proposal) → judge (Feynman recital for concept/design; lightweight question + self-check for procedure) → error diagnosis → spaced-review scheduling**

- **Reference-answer first (grill-me style, learner field feedback)**: after
  explaining a point, **present a reference answer** — a standard one-line
  statement with `file:line` — and let the user **react to the proposal**
  instead of staring at a blank prompt: agree, push back, ask where it differs
  from their understanding, or restate it in their own words. For
  concept/design there is **no independent blank-prompt answering**; the
  judgment is the *quality of the reaction*, not a verbatim recall.
- **Discuss transferable capability, not trivia**: explanations focus on
  concept/design/procedure — architecture, data flow, call chains, design
  trade-offs. Parameter/command/API spelling is **not expanded, not interacted
  with** — one line into the module's cheatsheet (`memory` points).
- The next station is always decided by the **engine script** — run
  `python3 scripts/learning_engine.py next-objective <path>/.learning/progress.json`
  (priority: pending question → `flow_phase` gate → due review → first
  unmastered point → complete). **`memory` points never appear** — they're
  reference-only (cheatsheet), never gated.
- Quantitative gate (procedure only): a **lightweight scenario question**
  (application, never flag spelling). The user answers, then you **immediately
  show the reference answer** for self-check; judge the attempt (answer +
  self-check correction) and record it via
  `python3 scripts/learning_engine.py record-attempt ... --write`; advance only
  when the script reports `passed_gate: true` (≥ 0.9).
- Qualitative gate (concept/design): after the reference-answer discussion,
  have the user restate the point in their own words; you judge `passed`. The
  expected answer is **not hidden to test recall** — the user already saw the
  reference answer; the judgment is whether they can critically engage with it
  and restate it. (Results stored in `progress.json.qualitative_mastery` and
  read by the engine's `next-objective`.)
- **Hands-on on demand**: for procedure points, guide the user to actually run things (build/test/write a small demo). Read-only commands (`build`, `test`, `--help`) may run directly; **mutating operations (writing files, installing deps) require explicit user approval first**. The hands-on result is recorded as mastery evidence.
- **Auto-consolidate (layered)**: after each explanation/judgment — and every other **substantive** turn — automatically consolidate the section's discussion (key takeaways + Q&A conclusions + cheatsheet + blockers + Feynman records) into `<repo>/.learning/notes/<module>.md` (format: `note-template.md`) — the per-turn diary, always fresh on substance. Mechanical turns (review drain, simple confirmation, Q&A digesting) **skip it**; the next substantive turn's consolidation covers the stretch (see `session-flow.md` §7 layered wrap-up).
- **`/repo-mastery note ["<text>"]` — interval consolidation**: the *manual* complement to auto-consolidate. Instead of re-consolidating what auto already wrote, it consolidates **the discussion since the last note** (see `note-template.md`): read `notes/.boundary.json` for the interval start (module_id + timestamp; none → from session/module start), extract that interval's Q&A conclusions, new blockers, cheatsheet additions, and Feynman records into `notes/<module>.md` **deduplicated against what auto already wrote** (never re-write it — repeating consolidation is wasted tokens), plus a `### 区间整理` recap block (2–4 distilled takeaways + Mission links), then update `notes/.boundary.json`. Optional `<text>` goes verbatim into "My notes" (never rewritten). Across-session / pre-compaction intervals are recovered from notes + `records/`; unrecoverable detail is marked 「需回顾」, never invented. The tutor writes `.boundary.json` directly — the engine is untouched.
- **Command convention**: only run read-only/no-side-effect commands by default; show any command that modifies the user's filesystem or installs dependencies and request approval.

### Phase 4 — Continuously-Generated Course Note (dual format)

The course note is **generated early and updated as learning progresses** — not a one-shot synthesis at the end (learner field feedback):

1. **At Phase 2 confirmation** — immediately generate the **first-draft `COVERAGE.md`**: course map + value brief + module skeleton + review schedule. This is the primary artifact and grows with you.
2. **After each module in Phase 3** — incrementally update `COVERAGE.md`'s module sections: explanations, reference cheatsheet, blockers, Feynman records, user `/note` entries, mastery, review schedule. Covered modules (`chapter_covered_modules`) are labelled **「已覆盖 · 待复习验证」** with their points listed as covered-awaiting-review, not as unmastered (see the textbook-mode display convention).
3. **HTML version — decided once at start, refreshed when the course is complete.** At Phase 2 confirmation, **ask the user** whether to also generate the **shareable HTML course** (built into `<repo>/.learning/export/`: `COVERAGE.md` → `modules/0N-slug.html` + each module's chapter material as its own HTML page, assembled into `index.html`). If yes, build it **now** from the first draft (**reuse the finished shell in `references/html-shell/`** — styles.css / main.js / _base.html / _footer.html / build.sh, copy verbatim, never regenerate). It is **not regenerated per module** — when the course reaches `complete`, refresh the HTML course from the final COVERAGE.md (ask "要我把 HTML 课程更新为最终版吗？" or rebuild on request). Interactive elements (flow animations, group chat, glossary tooltips, scenario quizzes) follow the patterns in `references/html-shell/interactive-elements.md`.

> **Division of labor**: COVERAGE.md is the **content** note (explanations,
> cheatsheet, blockers, notes — grows with learning). **MASTERY.md is the
> status dashboard** — progress, mastery %, review due, next objective —
> regenerated from `progress.json` + `course-map.json` by `/repo-mastery
> status`, refreshed on substantive wrap-up (see `session-flow.md` §8). Status
> lives in MASTERY.md, not in COVERAGE.md's header.

> Note: the HTML version's visuals serve "source understanding" — **architecture diagrams, dependency graphs, call chains are the core content**, the opposite of docs-to-course's "UI step-strips bias".

---

## Textbook Mode (chapter) — 默认学习路径

The **default on entering each new module** is flipped-classroom /
textbook-mode: instead of interrogating point-by-point, generate a **complete
chapter** of learning
material for the module, walk it together section by section, then question and
verify *after* the chapter. This fits source/architecture learning: strong
structure & relations need a panorama (splitting them into single-point quizzes
destroys the mental model); weak single-point facts make memory-quiz low value;
and "why is it designed this way" is best asked after the understanding has
settled (see the learning-mode comparison in `ADOPTION.md` §8). Spaced review
remains the fallback that proves real retention of anything not individually
checked.

> **There is no `/repo-mastery chapter` command** — the textbook-mode flow is
> the **default**: on entering each new module, the tutor auto-starts it after
> the module overview (one line of notice first; a conversational "切交互式"
> switches that module to interactive per-point mode). To explicitly re-walk a
> module's chapter, say so in natural language (e.g. "重讲 m02 教材") — the
> tutor re-runs the flow below. HTML builds — the course and its chapter pages —
> follow the one-time decision at start and the refresh at course completion
> (see Phase 4).

### The five-step chapter flow

```
1. 生成教材   chapters/<module>.md  (章节导言 → 逐节[每节=一个知识点：
              讲解 + 源码走读 file:line + 小结 + 课后思考题] → 章节总结 → cheatsheet)
              教材的 HTML 版随 HTML 课程生成（start 时确认 + 完成时刷新，见 Phase 4；复用 references/html-shell/，copy verbatim）
              课后思考题必须与 course-map 中 knowledge_point_ids 对齐 (否则课后检验无法走引擎判定)
              大仓先按 module-brief-template.md 预抽源码片段进 briefs，再据此写教材
              → 引擎 chapter-start (校验 flow_phase/module/covered/pending，写 {module_id, status, section_index, sections})
2. 逐节讲解   tutor 按教材一节一节讲，用户跟随材料 (可打开 HTML/MD 对照，随时打断提问)
              【每讲完一节必须停】给自然确认点：「这一节讲完了，有疑问吗？没有就进入下一节」
              → 等用户明确回复 (提问或说"继续/懂了") 后才 chapter-advance --section N
              → 绝不未经确认连续推进多节；全部讲完也停下确认后再进课后答疑 (--status qna)
3. 课后答疑   → status=qna：用户自由提问，tutor 答疑消化 (可写 learning record)
4. 课后检验   → status=verifying：针对章节关键节点提 1-2 个深度题
              concept/design → 深度问答 + tutor 判定 → set-qualitative 写 qualitative_mastery
              procedure     → pending_question + record-attempt (现有机制复用) + 可选实际运行验证
5. 章节完成   → chapter-complete：模块级闸门 (见下)
```

### Module-level gate semantics (用户确认「模块级闸门」)

- **已检验的关键节点**：保留真实引擎记录（`qualitative_mastery` / `quiz_attempts`）。
- **未单独检验的其余点**：`chapter-complete` 时初始化 spaced-review
  （`repetition_states` interval_index 0、按各自类型 base interval 生成
  `next_review_at`），进 `review_queue`——之后靠 `/repo-mastery review` 逐点
  提取、用正确/错误答案构建真实掌握度（**不伪造 mastery_levels**，延续
  「fluency ≠ storage」公理，不破坏置信天花板）。
- **模块整体**：加入 `chapter_covered_modules`；`next_objective` 的逐点扫描
  跳过它（不阻塞推进、不再催逐点），但它的点**仍正常进入复习队列**——covered
  ≠ forgotten。
- **显示口径（covered ≠ 未掌握）**：`/repo-mastery status` 与 Phase 4
  `COVERAGE.md` 里，covered 模块的知识点用**三态**标注，绝不显示成「未掌握」：
  - `未掌握` — 逐点尚未学习/未 covered 的模块；
  - `已覆盖 · 待复习验证` — 模块已走教材式闸门、真掌握待 spaced review 验证
    （covered 模块的点即此态，除非已有真实 mastered 记录）；
  - `已掌握` — 有真实引擎记录（`mastery_levels`/`qualitative_mastery`）的点。
  covered 的点**不得**落入「未掌握」列——那会把「已学完待验证」误读为「没学」。

### Compatibility with the core axiom (always hold)

The module-level gate is **still a deterministic engine decision**
(`chapter-complete`), never the LLM patting itself on the back — the gate only
*delegates* the points it didn't individually verify to spaced review rather
than faking mastery now. Do **not** read "chapter done" as "module mastered":
unchecked points have no mastery until real review attempts build it.

- `next-objective` precedence: pending question → `flow_phase` gate → **chapter
  gate** (in-progress chapter keeps teaching, with `due_review_count` signpost)
  → due review → first unmastered point (skipping covered modules) → complete.
- `mode="review"` bypasses the chapter gate: scattered-time review drains due
  reviews even mid-chapter.

---

## Data Structures

```text
<target-repo>/.learning/                  ← travels with the repo; auto-gitignored
  ├── MISSION.md           learning mission (why you want to master it; grounds teaching; incl. value positioning)
  ├── positioning.md       ecosystem positioning (sourced comparison matrix; see positioning-brief.md)
  ├── course-map.json      course map (confirmed version; capability points only)
  ├── progress.json        LearningProgress (mastery / spaced review / blockers; see mastery-policy.md)
  ├── MASTERY.md           one-page status dashboard (progress / mastery % / review due / next objective; regenerated by status, refreshed on substantive wrap-up; see session-flow.md §8)
  ├── records/NNNN-slug.md ADR-style learning records (understanding evolution)
  ├── notes/overview.md    global overview (architecture narrative + module map + differentiation)
  ├── notes/<module>.md    structured notes (auto + /note interval consolidation; incl. reference cheatsheet)
  ├── notes/.boundary.json /note interval boundary ({"module_id": "m01", "last_consolidated_at": <unix>})
  ├── chapters/<module>.md textbook-mode chapter material (default path; one per module)
  ├── briefs/<module>.md   module briefs (large repos, token-saving)
  ├── code-map.json        large-repo index (optional)
  ├── export/              HTML course output (index.html + modules/0N-slug.html; built at the start decision, refreshed at completion — see Phase 4)
  └── .gitignore           contains ".learning/"
~/.repo-mastery/                     ← global lightweight memory (no L1/L2/L3 layering)
  ├── profile.md           cross-repo preferences / level / blocker summary
  └── index.json           repos studied + state (last learned where)
```

Progress is stored in JSON, one record per knowledge point; the **expected answer of a pending question lives server-side (`progress.json`) and never round-trips to the user** — grading never drifts (absorbed from DeepTutor's `PendingQuestion`).

---

## Reference Files (read per phase to keep context lean)

- `references/curriculum-design.md` — **Phase 1**: designing the course map from source
- `references/positioning-brief.md` — **Phase 2**: ecosystem positioning brief (sourced comparison matrix; output `.learning/positioning.md`)
- `references/mastery-policy.md` — **Phase 3**: mastery, gates, spaced review, error diagnosis, fluency vs storage
- `references/session-flow.md` — **Phase 3**: interactive learning session protocol (incl. Mission + ZPD)
- `references/quiz-design.md` — **Phase 3**: quiz design (test application, not memory)
- `references/module-brief-template.md` — **Phase 3, large repos**: pre-extract source snippets, save tokens
- `references/note-template.md` — **Phase 3**: note format
- `references/learning-records-template.md` — **All phases**: ADR-style learning record format
- `references/gotchas.md` — **All phases**: failure-point checklist
- `references/index-script-spec.md` — **Phase 0, large repos**: Python indexing script docs
- `references/html-shell/` — **Phase 4**: HTML course shell (copy verbatim)

## Scripts

- `scripts/learning_engine.py` — **the deterministic gate**. Call for mastery /
  schedule / record-attempt / next-objective / validate-map / init. Mandatory in
  every tool; never re-derive the math from prose.
- `scripts/index_repo.py` — large-repo code index (`code-map.json`), pure stdlib.
- `scripts/install.sh` — install the skill to Claude Code, Codex, and Gemini CLI
  at once (`--only <tool>` / `--skip <tool>` / `--dry-run`).

## Multi-tool entry points

- `AGENTS.md` — portable protocol for AGENTS.md-compatible tools (Codex, opencode, Cursor).
- `GEMINI.md` — protocol for Gemini CLI.
- `agents/openai.yaml` — Codex/Agent-Skills UI metadata.

## Anti-Patterns

> The full failure checklist is in `references/gotchas.md`. These anti-patterns destroy learning quality outright — stop when you see one:

- ❌ **Letting the LLM replace the gate** — never use "do you feel you've mastered it?" instead of `compute_mastery` / `mastery_assess`.
- ❌ **Skipping course-map confirmation** — the user must approve/customize the map (with Mission); this is an explicit requirement.
- ❌ **Clarifying without a value brief** — Phase 2 must first present what this repo can teach and what makes it stand out vs peers, before the Mission.
- ❌ **Gating `memory` trivia** — parameter/command/API spelling is reference-note material (cheatsheet), never a gate-able knowledge point (it doesn't build transferable skill).
- ❌ **Staring-at-a-blank-prompt questioning** — learning interaction gives a reference answer and lets the user react to the proposal (grill-me style); never make the user answer from an empty prompt. For procedure's graded question the reference answer is shown right *after* the user answers, for self-check.
- ❌ **Leaking the expected answer before grading** — for procedure's graded question, the answer is never shown *before* the user answers (grading stays honest); it is shown right *after*, for self-check. `progress.json.pending_question` holds the expected answer; concept/design's reference answer is part of the discussion, shown to react to, not hidden.
- ❌ **Confusing "worked once" with "mastered"** — one lucky answer / one successful run ≠ mastery; the confidence ceiling + spaced review are the real goal (fluency ≠ storage).
- ❌ **Starting on nodes without the overview** — learning opens with the global overview, then each module's overview, before any per-node teaching. Engine-enforced via `flow_phase`: `next-objective` refuses points while the gate is open.
- ❌ **Resuming straight into a knowledge point** — a resume (`continue`, or the bare command) always opens with the Session Preamble (value replay + current map + progress) before any node.
- ❌ **Skipping `set-phase`** — after presenting an overview, advance `flow_phase` with `set-phase`; otherwise `next-objective` keeps refusing new points.
- ❌ **Letting an unfinished overview block review** — scattered-time review uses `/repo-mastery review` (`--mode review`), which bypasses the overview gate and drains only due reviews.
- ❌ **Cramming the whole repo into context** — read only the files relevant to the current knowledge point; use `code-map.json` to locate on demand in large repos.
- ❌ **Entering a new module in interactive mode by default** — textbook-mode chapter is the default on entering each new module; after the module overview the tutor must auto-start it (`chapter-start`), with one line of notice, instead of silently offering per-point nodes — unless the learner explicitly switched that module to interactive mode.
- ❌ **Generating a textbook and skipping the section-by-section walk** — dumping the chapter material once and moving on reduces textbook mode to a material dump; the tutor must teach it section by section (chapter-advance).
- ❌ **Advancing to the next section without the user's confirmation** — after each section the tutor stops and hands control back ("这一节讲完了，有疑问吗？没有就进入下一节") and only calls `chapter-advance` on an explicit user reply; never chain sections in one turn (the engine can't see the conversation, so the pause is the tutor's job).
- ❌ **After-class checking that misses the module's key nodes** — the 1–2 deep questions must land on the module's critical knowledge points and go through the engine (`set-qualitative` / `record-attempt`); checking only trivia leaves the key nodes unverified.
- ❌ **Reading "chapter done" as "module mastered"** — `chapter-complete` covers the module but does not fake mastery; unchecked points are verified later via spaced review. Never write a mastery score for a point the learner never actually answered.
- ❌ **Inventing differentiation without a source** — the value brief's "stands out vs peers" comes from `positioning.md` (sourced `[web]` / `[src]`), never improvised from tutor memory; a peer-comparison claim with no source is a 「需验证」 row, not a fact.
- ❌ **Leaking `[unv]` into a gated reference answer** — an unverified tutor-memory peer claim is a search seed, never the reference answer behind a Feynman recital or quiz.
- ❌ **Re-consolidating what auto already wrote** — `/repo-mastery note` consolidates the *interval since the last note* (deduplicated against the per-turn auto-consolidate); re-summarizing already-written key points is wasted tokens.
- ❌ **Inventing pre-compaction interval content** — when the interval start lies before a context compaction, recover from `notes/` + `records/` and mark unrecoverable detail 「需回顾」; never fabricate take-aways the tutor can no longer see.

## Related Skills

- `docs-to-course` (codebase-to-course) — docs → end-user usage course (source of this skill's methodology & HTML shell).
- `understand-anything` — builds a knowledge graph of a codebase (pair well for architecture deep dives).
- `codebase-onboarding` — quick ramp on unfamiliar codebases (complements this skill's Phase 1 pre-scan).
- `find-docs` — locate project docs; useful for enriching a module's "primary sources".

## Verification (completion checks)

When starting / ending a learning session, self-check with `references/gotchas.md` and confirm:

- [ ] `.learning/` is gitignored; the target repo is not polluted.
- [ ] `course-map.json` is the user-confirmed version.
- [ ] `progress.json` written atomically, uncorrupted.
- [ ] Notes appended on substantive turns; `~/.repo-mastery/index.json` updated each turn.
- [ ] No expected-answer leakage; no unapproved mutating commands.

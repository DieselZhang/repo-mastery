# ADOPTION — What This Skill Adopts and Absorbs

Repo-Mastery stands on the shoulders of five upstreams: **DeepTutor** (HKUDS, MIT), **docs-to-course** (a.k.a. codebase-to-course), two of mattpocock's skills — **`teach`** and **`grilling`** — and the **evidence-based memory mechanisms** community (FSRS, learning-science meta-analyses, and several open learning skills). This document lists, per upstream, what was adopted/absorbed and why.

## 1. From DeepTutor (HKUDS, MIT): the mastery learning engine

DeepTutor is an agent-native intelligent learning platform. This skill ports the core pedagogy of its `learning/` module, replacing "subject knowledge" with "code knowledge":

| Adopted design | Source (DeepTutor module) | Where in repo-mastery |
|---|---|---|
| **Axiom: intelligence at the exit, advancement at the gate** — the model decides what to teach and how to question; whether the learner may advance is a deterministic engine call | `capabilities/mastery/capability.py` | `SKILL.md` core axiom |
| **Quantitative mastery**: recency-weighted accuracy + confidence ceiling (one lucky answer ≠ mastery) | `learning/mastery.py` | `mastery-policy.md` §2 |
| **Advancement computed from what's mastered; the gate IS the cursor** (test-out skips proven points) | `learning/policy.py` `next_objective` | `mastery-policy.md` §4 |
| **Spaced repetition**: per-type interval schedules + error-priority escalation | `learning/scheduler.py` | `mastery-policy.md` §3 |
| **Error diagnosis**: structural / deviation / application / metacognitive | `learning/models.py` `ErrorType` | `mastery-policy.md` §5 |
| **Deterministic grading**: expected answer stored server-side, never round-tripped to the model | `learning/models.py` `PendingQuestion` | `mastery-policy.md` §7 |
| **explore_context pre-scan**: objectively digest attached material before the answer loop | `capabilities/explore_context/` | `SKILL.md` Phase 1 |
| **Notes as reusable context** | `tools/write_note` + notebooks | `note-template.md` |

DeepTutor is MIT-licensed (see its repo `LICENSE`). These designs are attributed at the point of use in the `references/` files.

## 2. From docs-to-course (codebase-to-course): curriculum design & output shell

`codebase-to-course` is a personal skill that turns tool documentation into end-user usage courses. This skill absorbs its methodology and output shell — but the **learner and goal are completely different**: it serves end-users learning to *use* a tool; repo-mastery serves developers learning to *understand* a codebase's internals.

| Absorbed | Source file | Where in repo-mastery | Adaptation |
|---|---|---|---|
| **"reference → route" curriculum design**: re-sequence lookup material into a progressive route; module arc (first win → mental model → core workflows → …) | `references/curriculum-design.md` | `curriculum-design.md` | Arc adapted for code learning (build → architecture mental model → core workflows → key implementations → hands-on → troubleshooting) |
| **Per-module arc**: objectives → why care → concept+metaphor → see/do it → recap → quiz | `references/curriculum-design.md` | `session-flow.md` explain | Becomes the explanation skeleton of the learning session |
| **Quiz philosophy**: test application, not memory (scenario/trace/tradeoff questions first) | `references/content-philosophy.md` | `quiz-design.md` | Question types adapted to code understanding (call-chain tracing, extension-point choice, troubleshooting) |
| **Module-brief pre-extraction**: pre-extract snippets before writing, so the writer never re-reads the source (token-saving) | `references/module-brief-template.md` | `module-brief-template.md` | Pre-extraction object changes from "commands/config" to "source snippets + file:line" |
| **HTML course shell**: styles.css / main.js / _base.html / _footer.html / build.sh, copied verbatim, never regenerated | `references/` (styles.css etc.) | `references/html-shell/` | Shell reused as-is; interactive elements follow the existing class/data-* conventions |
| **Interactive-element patterns**: flow animations, group chat, glossary tooltips, scenario quizzes | `references/interactive-elements.md` | `references/html-shell/interactive-elements.md` | Reused as-is |
| **repo-first ingest principle**: prefer cloning a repo over crawling a site | `references/ingest.md` | `SKILL.md` Phase 0 | Repo-mastery naturally handles source; the principle is confirmed by design |

### Deliberately not absorbed (opposite learner → opposite design)

- ❌ "End-user bias toward UI step-strips rather than internal architecture diagrams" — repo-mastery is the reverse: **architecture diagrams / dependency graphs / call chains are core content**.
- ❌ "Don't get outline approval — just build it" — repo-mastery **mandates course-map confirmation** (a user decision, never skipped).

## 3. From mattpocock's `teach` skill: learning-mechanism enhancements

[`teach`](https://github.com/mattpocock) is a teaching skill that contributed several mechanisms repo-mastery didn't have (added in v1.1.0):

| Borrowed | teach's approach | Where in repo-mastery |
|---|---|---|
| **Mission-driven** | `MISSION.md` records why the user is learning; grounds all teaching | `SKILL.md` Phase 2 asks "why do you want to master this repo", writes `.learning/MISSION.md` |
| **Learning records (ADR-style)** | `learning-records/` captures non-obvious learnings, stated prior knowledge, corrected misconceptions, with supersession | `references/learning-records-template.md` + `.learning/records/NNNN-slug.md` |
| **ZPD (zone of proximal development)** | challenge "just enough", computed from records + mission | `mastery-policy.md` §0 + `session-flow.md` §0 |
| **Fluency vs Storage** | fluency gives illusory mastery; storage strength is the goal | `mastery-policy.md` §0 (the rationale behind gates + spaced review) |
| **Primary-source recommendations** | each lesson recommends a high-quality primary source | `note-template.md` "Resources / primary sources" |
| **Option formatting without clues** | every option roughly equal in length | `quiz-design.md` "Option formatting" |
| **Retrieval practice first** | force retrieval from memory, not recognition | `quiz-design.md` "Retrieval practice first" |

## 4. Why reusing docs-to-course's shell is legitimate

The `references/html-shell/` CSS/JS/HTML files were written/maintained by this skill's author (DieselZhang) for codebase-to-course and are freely reusable under MIT. Both repos are the same author's personal skill assets; there is no third-party copyright conflict.

## 5. From mattpocock's `grilling` skill: the decision-clarification interview

[`grilling`](https://github.com/mattpocock/skills) (user entry `grill-me`) is a relentless interview that walks a plan's decision tree until shared understanding. Repo-Mastery absorbs its interview technique to harden Phase 2 (Mission + course-map confirmation), where a single open question used to stand:

| Adopted design | grilling's approach | Where in repo-mastery |
|---|---|---|
| **Decision-tree walk** — resolve decisions in dependency order, parent first | walks every branch of the plan | `clarification-interview.md` §2 |
| **One question at a time** — batching is bewildering | asks and waits, one at a time | `clarification-interview.md` §3; `session-flow.md` tutor voice |
| **Facts vs decisions separation** — look up facts, ask only decisions | explores the environment instead of asking | `clarification-interview.md` §4 |
| **Recommended answer with each decision question** | reacts to a proposal, not a blank prompt | `clarification-interview.md` §5 |
| **Shared-understanding gate** — don't act until confirmed | confirms before enacting | `clarification-interview.md` §6 |

**Deliberate differences**: `grilling` is stateless (writes nothing); repo-mastery's clarification is stateful — settled decisions are written to `.learning/MISSION.md` and `course-map.json` because they ground every later teaching decision. And the recommended-answer habit is **scoped to decision questions only**; the answer is withheld *before* the learner acts only in a graded procedure question (`pending_question.expected_answer` stays server-side until they answer, then is shown for self-check).

> **v2.6.0 extension** — grilling's "react to a proposal, not a blank prompt" now
> also shapes **Phase 3 learning interaction**: after explaining a point the
> tutor gives a **reference answer** and the learner reacts to it (concept/design
> — no blank-prompt exam); a graded procedure question shows the reference
> answer right *after* answering, for self-check. See `session-flow.md` §2–4,
> `quiz-design.md` "Reference-answer interaction", `mastery-policy.md` §6.

## 6. From the memory-mechanisms ecosystem: evidence-based retention

Repo-Mastery's retention engine absorbs techniques from several open learning
sources, all grounded in cognitive-science findings (active recall and spaced
repetition have the highest effect sizes in the learning-science literature):

| Adopted design | Source | Where in repo-mastery |
|---|---|---|
| **FSRS-inspired personalized scheduling** — difficulty + stability scale the review interval | [open-spaced-repetition](https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler) (FSRS, DSR model) | `mastery-policy.md` §3; `learning_engine.py` `schedule_next` |
| **Session recall warm-up + streak** — start each session by retrieving prior points | [claude-teach-skill](https://github.com/tanishg98/claude-teach-skill) (spaced-retrieval loop) | `session-flow.md` §0 |
| **Causal questioning** — probe "why / what-if / what breaks" | [RetainCraft](https://github.com/kaixiad/retaincraft) | `mastery-policy.md` §6 |
| **Vivid encoding** — SMASHIN-style memorable hooks for memory points | [memory-palace](https://github.com/Algiras/memory-palace) | `session-flow.md` §2 |
| **Flashcard quality standards** — force recall, one fact per card, elaborate & connect | [flashcards skill](https://getspace.app/blog/flashcards-skill) | `quiz-design.md` |
| **Low-effectiveness anti-patterns** — rereading/highlighting ≠ memory | learning-science literature (Dunlosky et al. 2013; Donoghue & Hattie 2021) | `gotchas.md` |

**Deliberate simplifications**: repo-mastery implements a *simplified* FSRS —
two parameters (difficulty, stability) with pure deterministic formulas instead
of FSRS's full parameter-optimized DSR model — to stay pure-stdlib and
tool-agnostic. Memory-palace is absorbed as *encoding suggestions only*, not its
full spatial-knowledge system.

## 7. v2.5.0 — learning-pace redesign (from field feedback + existing assets)

This release reshapes the learning rhythm. Its sources are field feedback from a
real run (DeepTutor, HKUDS) plus already-adopted assets — not a new upstream:

| Change | Origin | How it lands |
|---|---|---|
| **Value brief before clarification** | Learner field feedback: "before learning we should first clarify what this repo can teach and where it beats peers" — grounded in the `grilling` fact-vs-decision discipline (§5) | `clarification-interview.md` §0; Phase 2 in `SKILL.md` |
| **Overview-first (whole picture before the nodes)** | Learner field feedback: "prefer the whole knowledge map first, then discussion at key nodes" — a general curriculum-design principle rather than a borrow | `session-flow.md` Phase 3.0/3.1; `curriculum-design.md` |
| **`memory` points demoted to reference cheatsheets** | Learner field feedback on the real run: "these questions aren't meaningful, I'll just fill in the answer and skip" / "avoid flag-memorization quizzes" — params/commands are numerous, project-specific, and don't build transferable skill | engine `learning_engine.py` (`next_objective` / `_rebuild_review_queue` / `is_mastered`), `mastery-policy.md`, `quiz-design.md` |
| **Course note generated early, updated continuously** | Learner field feedback: "the HTML note can be generated at project start, then refined from questions during learning" — a start-early + incrementally-update use of the **docs-to-course HTML shell** (§2, reuse rule unchanged) | `SKILL.md` Phase 4; `export` command |

No upstream changed; §1–§6 attributions stand. The redesign applies existing
designs (grilling's fact-first clarification, the shared HTML shell, the
deterministic gate) to a discussion-first, capability-focused learning flow.

## 8. v2.7.0 — Textbook-mode chapter learning (教材式 / flipped classroom)

v2.7.0 adds a second learning path (default): **flipped-classroom / textbook
mode** — generate a complete chapter of learning material per module (md; the
`--html` variant of the then-current export command added the HTML shell —
superseded by v2.10.0, see §10), the tutor walks it section by section, then after-class
Q&A and key-node checking, closed by an engine module-level gate. It reuses the
**docs-to-course** full-material generation (§2 — but for *source understanding*,
not tool usage) and the **HTML course shell** (copy verbatim, unchanged). Spaced
review (the §6 ecosystem) remains the fallback that proves retention of any
point not individually checked.

The design decision is traceable (learner field feedback, confirmed 2026-08):

> **"每个章节形成完整的学习资料（类似 codebase-to-course 生成 html/md 文件），
> 我们一起统一学习以后再课后提问的方式"** — the interactive per-point mode
> (v2.5.0/v2.6.0) is kept as an option, but the user's wanted experience is
> whole-chapter material first, unified learning, then after-class questioning.

### Learning-mode comparison (the decision basis)

Source learning splits along two axes — *when* you verify (per-point vs
end-of-chapter) and *granularity* (fragmented vs whole-picture):

| 模式 | 节奏 | 检验时机 | 优点 | 缺点 |
|---|---|---|---|---|
| **逐点交互（Socratic）** | 讲一个点 → 立刻判定 | 每点即时 | 掌握度精确、门控严、反馈快 | 节奏碎、讲↔作答切换认知负担高、**只见树不见林**——架构类需全景的知识最吃亏 |
| **参考答案对照（grill-me 式，v2.6.0）** | 讲一个点 → 给参考答 → 对照讨论 | 每点即时 | 降低空白作答焦虑、基于提议讨论 | 本质仍是逐点交互（「你答」变「你评」），节奏未变——用户实测体验仍不对味 |
| **教材式 / 翻转课堂（v2.7.0 新增，默认）** | 整章材料 → 逐节讲 → 课后统一答疑+检验 | 章节末集中 + 间隔复习 | 完整系统视图、连续心流、材料可回看、心智模型连贯 | 掌握度验证延迟（「懂了但不牢」风险）、需跟随材料 |
| **纯自学材料** | 只看材料 | 无 | 完全自主、可复用 | 无检验无反馈无复习，假掌握风险最高 |

**Recommendation (adopted as default): textbook-first + spaced-review
fallback**, because architecture knowledge has three traits that decide the
choice:

1. **Strong structure & relations** (module dependencies, call chains,
   layering) — need a panorama; splitting them into single-point quizzes
   destroys the mental model → textbook / overview-first fit naturally.
2. **Weak single-point facts** — architecture is not memorizing params/commands,
   so per-point memory-quiz value is low → verification should be deep
   questions / restatement, not memory recall.
3. **Needs reasonable explanation, not verbatim recital** ("why MQ instead of
   RPC") — best asked *after* understanding has settled, in after-class
   checking.

**Confirmed decisions** (learner, 2026-08): (1) unified form — tutor walks the
material section by section, learner follows and may interrupt, continuous flow
not broken by per-point grading; (2) after-class questioning — free Q&A first,
then 1–2 deep questions on key nodes through the engine gate; (3) material
generated incrementally on entering each module (source-precise, token-saving);
(4) command-level mode switching — the textbook-mode chapter flow is the default
path, the interactive per-point mode remains an explicit per-module switch (the
`/repo-mastery chapter` command that first carried this decision was later
merged into the default flow — see the "v2.10.0 command-surface cut" note below);
(5) **module-level gate** for
unchecked points — `chapter-complete` covers the module, key nodes keep real
engine records, the rest get initialised spaced review whose real mastery is
built only by later review attempts (**never fake mastery_levels** — the
"fluency ≠ storage" axiom from §0/§3 is preserved, confidence ceiling intact).

> **v2.7.0 engine changes** (see `mastery-policy.md` §4/§7): `next_objective`
> precedence now is pending → `flow_phase` gate → **chapter gate** → due review
> → first unmastered point (skipping `chapter_covered_modules`) → complete;
> `mode="review"` bypasses both the overview and the chapter gates. New engine
> subcommands: `chapter-start` / `chapter-advance` / `chapter-complete` /
> `set-qualitative` (the last also fixes an existing gap — passed concept/design
> judgments were never scheduled for spaced review).

## 9. v2.8.0 — Ecosystem positioning & differentiation (生态定位视角)

v2.8.0 answers the developer's first question about any large open-source
project — *what is it, how does it trade off against its natural peers, and
when would I pick it* — which the skill previously left to an unsourced
self-description one-liner in `MISSION.md`. It adds a **sourced, persistent
comparison matrix** (`.learning/positioning.md`) produced by a Phase 2
**positioning brief** (`references/positioning-brief.md`), a
recommended-but-droppable **module 0** (3 `design` knowledge points, zero
engine changes), and **vs-peer probing** for design judgments
(`mastery-policy.md` §6).

Three §2/§5 roots, reused rather than new design:

- **docs-to-course full-material generation (§2)** — the positioning brief
  reuses the "produce complete, source-grounded material" discipline; the
  matrix's repo-facts column cites `file:line` exactly like a course note.
- **grilling fact-vs-decision discipline (§5)** — the `[src] / [web] / [unv]`
  source grading is grilling's "look up facts, ask only decisions" pushed into
  a *persisted* artifact: peer facts get a `[web]` URL + access date,
  tutor-memory claims are `[unv]` search seeds, never gated.
- **Supersession in learning records** — positioning is a living document
  (date-stamped, 「生态会过期」); when a matrix row changes, update
  `positioning.md` and write a learning record with `Status: superseded by
  LR-NNNN`, mirroring the §6 record-keeping rule.

**Zero engine changes** — module 0 reuses the `design` qualitative channel and
the existing module/chapter flow (`order: 0`); the external-scan rule is
conditional (no search tool → repo-evidence brief with `[unv]` peer rows, never
a fabricated source), preserving the multi-CLI guarantee (§1).

> **docs/ is NOT synced for v2.8.0** — it has sat at the v2.0 era since
> 2026-08-07 and is not actively maintained; `references/` + `SKILL.md` +
> `AGENTS.md`/`GEMINI.md` are the source of truth.

## 10. v2.10.0 — Command-surface cut (命令面精简)

v2.10.0 trims the user-facing command surface from 9 concepts (bare + 8
commands) to **six commands**, after the default textbook flow (P1) made three
redundant:

- **`/repo-mastery chapter` merged into the default flow** — since the
  textbook-mode chapter auto-starts on entering each new module, the explicit
  command only served `--module`-pinned re-walks. The chapter flow itself is
  unchanged; re-walking a module's chapter is a natural language request
  ("重讲 m02 教材"), not a command.
- **`/repo-mastery export` merged into the default flow** — COVERAGE.md is
  already updated module-by-module by the tutor's wrap-up, so a manual
  (re)build command had no daily use. The HTML course is now **decided once at
  start** (Phase 2 asks whether to build the shareable HTML course from the
  first draft) and **refreshed at course completion** (on request, from the
  final COVERAGE.md) — no command surface for it.
- **bare `/repo-mastery` merged into `continue`** — the "Smart Routing" table
  (route on `.learning/` state) is now `continue`'s job: a bare command with no
  subcommand *is* `continue`, which routes (no `.learning/` → guide to start /
  incomplete → preamble + resume / complete → report done). The routing rules
  are unchanged, only the surface is smaller.

**Zero engine changes** — `chapter-start`/`advance`/`complete` and
`set-qualitative` stay exactly as in v2.7; only the skill-layer command table,
Session Preamble wording, and READMEs move.

## Licenses & copyright

- This repo: MIT License, see `LICENSE`.
- DeepTutor design port: © 2026 HKUDS, MIT License ([github.com/HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor)).
- docs-to-course shell: © 2026 DieselZhang.
- mattpocock `teach` mechanisms: © mattpocock ([mattpocock-skills](https://github.com/mattpocock)).
- mattpocock `grilling` interview technique: © mattpocock ([mattpocock-skills](https://github.com/mattpocock)).
- FSRS algorithm design: © open-spaced-repetition (MIT).
- claude-teach-skill / RetainCraft / memory-palace / flashcards ideas: respective authors (see §6 links).

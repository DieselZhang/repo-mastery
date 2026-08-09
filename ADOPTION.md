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

**Deliberate differences**: `grilling` is stateless (writes nothing); repo-mastery's clarification is stateful — settled decisions are written to `.learning/MISSION.md` and `course-map.json` because they ground every later teaching decision. And the recommended-answer habit is **scoped to decision questions only**; Phase 3 assessment (quiz / Feynman) never leaks answers, keeping `pending_question.expected_answer` server-side.

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

## Licenses & copyright

- This repo: MIT License, see `LICENSE`.
- DeepTutor design port: © 2026 HKUDS, MIT License ([github.com/HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor)).
- docs-to-course shell: © 2026 DieselZhang.
- mattpocock `teach` mechanisms: © mattpocock ([mattpocock-skills](https://github.com/mattpocock)).
- mattpocock `grilling` interview technique: © mattpocock ([mattpocock-skills](https://github.com/mattpocock)).
- FSRS algorithm design: © open-spaced-repetition (MIT).
- claude-teach-skill / RetainCraft / memory-palace / flashcards ideas: respective authors (see §6 links).

# Repo-Mastery Architecture

This document explains how Repo-Mastery works internally: the design axioms, the mastery engine, the four phases, and the data model.

## Overview

Repo-Mastery is a **Claude Code skill** that turns a source repository into a developer-focused mastery course. It is a single SKILL.md orchestrator plus a set of reference documents that the skill reads per phase (to keep context lean) and one optional Python script for large repos.

```text
SKILL.md (orchestrator)
   │  reads per phase
   ▼
references/curriculum-design.md     Phase 1: build the course map from source
references/mastery-policy.md        Phase 3: gates, spaced review, error diagnosis
references/session-flow.md          Phase 3: interactive session protocol
references/quiz-design.md           Phase 3: quiz principles
references/module-brief-template.md Phase 3: token-saving pre-extraction
references/note-template.md         Phase 3: note format
references/learning-records-template.md  all: understanding-evolution records
references/gotchas.md               all: failure checklist
references/index-script-spec.md     Phase 0: large-repo index docs
references/html-shell/              Phase 4: HTML course shell (verbatim)
scripts/index_repo.py               Phase 0: large-repo code index (pure stdlib)
```

## Design Axiom

> **Intelligence at the exit, advancement at the gate.**

The tutor (the LLM) decides *what to teach, how to question, how to explain*. But whether the learner *may advance* is always a **deterministic engine decision**, never the model's self-assessment. This is the single most important design decision, ported from DeepTutor's mastery capability.

Two consequences:

1. **Grading never drifts** — the expected answer of a pending question lives in `progress.json` server-side and never round-trips to the learner.
2. **Advancement is computed, not narrated** — `next_objective` derives the next step from what is already mastered (the gate IS the cursor), never from a stage counter.

## The Mastery Engine

Ported from DeepTutor's `learning/` module. Four knowledge types map to two gate kinds:

| type | gate | pass |
|---|---|---|
| `memory` | quantitative | recency-weighted accuracy ≥ 0.9 |
| `procedure` | quantitative | ≥ 0.9 + hands-on evidence |
| `concept` | qualitative | Feynman recital judged by tutor |
| `design` | qualitative | recital + design-tradeoff follow-ups |

### Quantitative mastery (`compute_mastery`)

- Recency-weighted accuracy over the latest up-to-5 attempts, weights `(0.5, 0.7, 0.85, 0.95, 1.0)`.
- **Confidence ceiling**: 1 attempt caps the score at 0.5, 2 attempts at 0.8 — one lucky answer cannot reach the 0.9 gate.

### Spaced repetition

Per-type interval sequences (`memory` `[0,1,3,7,14,30]`, `concept` `[3,7,14,30]`, `procedure` `[3,7,14]`, `design` `[14,28]`), with error records escalating a point's review priority.

### Error diagnosis

Four metacognitive categories: `structural` (missing prerequisites), `deviation` (misunderstood concept), `application` (right concept, wrong scenario), `metacognitive` (unaware of what's unknown). Each records self-attribution + tutor confirmation + retry history.

### Fluency vs storage (absorbed from the teach skill)

The whole engine is an anti-"fluency illusion" machine: the confidence ceiling, Feynman recital, and spaced review exist so that only retrieval-after-forgetting (storage strength) counts as mastery.

## The Four Phases

### Phase 0 — Complexity assessment
Judge the repo size (< 100k source lines, < 20 top-level modules, simple deps → small/medium; otherwise large). Small/medium: pure-skill direct reading. Large: run `scripts/index_repo.py` to produce `code-map.json` and locate source on demand.

### Phase 1 — Objective pre-scan → course-map candidates
An explore_context-style read-only pre-scan (map the repo without jumping to conclusions), then a course map of 4–8 modules following the arc *first win (build) → architecture mental model → core workflows → key implementations → hands-on → troubleshooting → deep references*. Every module/point carries source evidence.

### Phase 2 — Mission + map confirmation (mandatory)
Establish **MISSION.md** (why the user wants to master this repo — grounded teaching), then present the candidate map for the user to remove/add/adjust and approve. Learning never starts without approval.

### Phase 3 — Interactive mastery learning
Per knowledge point: `diagnostic (test-out) → explain (from source) → Feynman check → practice (quiz / hands-on) → error diagnosis → spaced-review scheduling`. Each turn ends with atomic `progress.json` write, auto-notes, and global-memory update.

### Phase 4 — Dual-format course synthesis
Synthesize `COVERAGE.md` (full Markdown) and optionally a shareable HTML course reusing the `html-shell/` shell (verbatim copy — never regenerate). The HTML version is deliberately architecture-centric (diagrams, dependency graphs, call chains), opposite to docs-to-course's UI-step-strip bias.

## Data Model

```text
<target-repo>/.learning/
  ├── MISSION.md            why the user wants to master this repo
  ├── course-map.json       confirmed modules + knowledge points + thresholds
  ├── progress.json         mastery levels, repetition states, error records, pending question
  ├── records/NNNN-slug.md  ADR-style learning records (with supersession)
  ├── notes/<module>.md     structured notes (auto + /note)
  ├── briefs/<module>.md    pre-extracted source snippets (large repos)
  ├── code-map.json         large-repo index (optional)
  └── .gitignore
~/.repo-mastery/            global lightweight memory (profile.md, index.json)
```

Key invariants:

- `.learning/` is auto-gitignored so the target repo is never polluted.
- `progress.json` is written atomically (temp file + rename).
- `pending_question.expected_answer` never appears in question text.
- Global memory keeps resume state across sessions (no L1/L2/L3 layering — deliberately lightweight).

## Provenance

The skill is a composition of three proven designs:

- **DeepTutor** (HKUDS, MIT): mastery engine, gates, spaced repetition, error diagnosis, `PendingQuestion`, `explore_context` pre-scan.
- **docs-to-course** (codebase-to-course): "reference → route" course arc, quiz philosophy, module-brief pre-extraction, HTML course shell.
- **mattpocock teach**: Mission, ZPD, ADR-style learning records, fluency vs storage, option-formatting, retrieval practice.

Full per-item attribution: [ADOPTION.md](../ADOPTION.md).

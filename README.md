<div align="center">

# 📚 Repo-Mastery

**Turn any open-source repository into a developer-focused mastery course.**

Learn a project's **usage → architecture → key implementations** the way you'd learn a real course — with confirmed course maps, deterministic mastery gates, spaced repetition, and dual-format (Markdown + HTML) course output.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-skill-0A84FF.svg)](#)
![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)

[简体中文](./README.zh-CN.md) · [Documentation](./docs/ARCHITECTURE.md) · [Contributing](./CONTRIBUTING.md)

</div>

<p align="center">
  <img src="assets/repo-mastery-flow.png" alt="Repo-Mastery workflow: input repo → P0 assess → P1 course map → P2 mission & confirm → P3 interactive mastery learning → complete course" width="92%">
</p>

---

## Table of Contents

- [What is Repo-Mastery?](#what-is-repo-mastery)
- [Why](#why)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Data Model](#data-model)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## What is Repo-Mastery?

Repo-Mastery is an **Agent skill** that converts any open-source repository into a structured, developer-focused mastery course. Given a local repo path or a GitHub URL, it:

1. **Pre-scans** the codebase objectively and proposes a **course map** (modules + knowledge points).
2. Has **you confirm and customize** the map — aligned with your Mission (why you want to master this repo).
3. Drives **interactive mastery learning** — diagnose → explain → Feynman check → practice → error diagnosis → spaced review.
4. Persists progress, notes, and **learning records** for cross-session continuity.
5. Synthesizes a **complete course document** in Markdown and HTML (shareable).

It is the "learn the codebase deeply" counterpart to `docs-to-course` (which teaches end-users how to *use* a tool from its docs). Repo-Mastery teaches developers how a project is *built*.

## Why

As a developer, reading an open-source project's code rarely equals "mastering" it. Repo-Mastery closes that gap with a judgeable learning mechanism:

- Every knowledge point has a **deterministic mastery gate** — not the LLM's impression.
- **Spaced repetition** fights forgetting; **learning records** capture how your understanding evolves.
- Notes and progress **persist across sessions**, so you resume exactly where you left off.

## Features

- 🗺️ **Evidence-based course maps** — every module/knowledge point points to real files, directories, and call chains.
- 🧭 **Mission-driven** — grounded in *why* you want to master the repo, not generic coverage.
- ⚖️ **Dual mastery gates** — quantitative (recency-weighted accuracy ≥ 0.9) for usage/procedure; qualitative (Feynman recital) for concepts/architecture.
- ⏳ **Spaced repetition** — per-type interval schedules with error-priority escalation.
- 🔧 **Hands-on verification** — commands run with your approval; a procedure point only counts as mastered with real evidence.
- 📝 **Persistent notes + ADR-style learning records** — auto-accumulated and user-appended; records track understanding evolution with supersession.
- 🌍 **Adaptive ingest** — small/medium repos read directly; large repos get a lightweight Python index (`code-map.json`).
- 📦 **Dual-format output** — full Markdown course (`COVERAGE.md`) + shareable interactive HTML course.
- 🌐 **Bilingual** — teaching language follows your input; code and identifiers stay original.
- 🧰 **Multi-CLI** — the same skill runs natively on **Claude Code, OpenAI Codex, Gemini CLI**, and AGENTS.md-based tools. The deterministic gate is real code (`scripts/learning_engine.py`) shared by every tool, so mastery math never drifts.

## How It Works

```
Phase 0  Complexity assessment  →  decide ingest (pure read / Python index)
Phase 1  Objective pre-scan     →  course-map candidates
Phase 2  Mission + map confirm  →  you approve/customize (mandatory)
Phase 3  Interactive mastery learning (diagnose → explain → Feynman → practice → error-diagnosis → spaced review)
Phase 4  Synthesize COVERAGE.md + optional shareable HTML course
```

Core design axiom: **intelligence at the exit, advancement at the gate** — the tutor decides what to teach, but whether the learner may advance is always a deterministic engine decision.

## Installation

The repo itself **is** the skill, following the open **Agent Skills** standard
(agentskills.io) — the same `SKILL.md` runs natively on Claude Code, OpenAI
Codex, and Gemini CLI. **Five ways to install, pick one:**

### 1. npm — one command

```bash
npx @dieselzhang/repo-mastery install            # any tool, from anywhere
# or install the CLI globally:
npm i -g @dieselzhang/repo-mastery && repo-mastery install
# options: repo-mastery install --only codex / --skip gemini / --dry-run
```

### 2. curl — one line, no npm needed

```bash
curl -fsSL https://raw.githubusercontent.com/DieselZhang/repo-mastery/main/scripts/install.sh | bash
```

Installs to Claude Code + Codex + Gemini. Add `--only codex` (etc.) after the pipe.

### 3. Claude Code — native plugin install

```bash
claude plugin marketplace add DieselZhang/repo-mastery
claude plugin install repo-mastery@repo-mastery
```

(In-session equivalents: `/plugin marketplace add …` then `/plugin install …`.)

### 4. Conversation-driven — tell the CLI to install it

| Tool | Say this |
|---|---|
| **Claude Code** | "Install the repo-mastery skill from github:DieselZhang/repo-mastery into ~/.claude/skills" (Claude clones + places it), or use the `/plugin` route above |
| **OpenAI Codex** | In Codex, use its built-in installer: `$skill-installer install https://github.com/DieselZhang/repo-mastery` |
| **Gemini CLI** | "Clone the repo-mastery skill from github:DieselZhang/repo-mastery into your skills directory" |

### 5. Manual — clone

```bash
git clone https://github.com/DieselZhang/repo-mastery ~/.claude/skills/repo-mastery
cd repo-mastery && ./scripts/install.sh    # from the checkout, install to other tools too
```

### Where each tool looks

| Tool | Skill directory | Entry point |
|---|---|---|
| **Claude Code** | `~/.claude/skills/` | `SKILL.md` — `/repo-mastery start <repo>` |
| **OpenAI Codex** | `~/.codex/skills/` (or `~/.agents/skills/`) | `SKILL.md` + `agents/openai.yaml` |
| **Gemini CLI** | its skills dir (`GEMINI_SKILLS_DIR` overridable) | `activate_skill` / `GEMINI.md` |
| **opencode / Cursor** (AGENTS.md tools) | project dir | `cp AGENTS.md <project>/AGENTS.md` |

> **Codex note**: Codex reads only its own directories — it does not read
> `~/.claude/`. Install to `~/.codex/skills/` so it is discovered. Restart the
> CLI after installing.
>
> **Plugin note**: installing as a plugin caches the skill in
> `~/.claude/plugins/cache/` and invokes it namespaced (`/repo-mastery:repo-mastery`).

**Requirements**

- A target repository: a local path or a reachable `github:owner/repo` (the skill auto-runs `git clone --depth 1`).
- Python 3.8+ — needed by the deterministic engine (`scripts/learning_engine.py`) and the large-repo index (`scripts/index_repo.py`), both pure stdlib.

## Usage

```bash
/repo-mastery start <local-path | github:owner/repo> [--language zh|en] [--fresh]
```

Example — learn a project from a GitHub URL:

```bash
/repo-mastery start github:DieselZhang/repo-mastery
```

The skill walks you through the four phases. The teaching language follows your input by default; pass `--language zh` / `--language en` to force one.

## Commands

| Command | Purpose |
|---|---|
| `/repo-mastery preview <path\|url>` | Recon — macro brief only (what / architecture / differentiation / key highlights / deep-dive candidates); zero side effects, no `.learning/` created; say "深学" to hand off into start |
| `/repo-mastery start <path\|url>` | Main flow: value brief → map → confirm → overview → learn (textbook-mode chapter by default per module); `--fresh` restarts an existing course |
| `/repo-mastery continue` | Resume — smart route: no `.learning/`? guide to start; incomplete? session preamble, due review (signposted), then new content; complete? report done. A bare `/repo-mastery` is this command. |
| `/repo-mastery review` | Spaced-review only — drains due reviews, never opens new content |
| `/repo-mastery note ["<text>"]` | Consolidate the discussion since the last note into the module note (categorized); optional text appended verbatim |
| `/repo-mastery status` | Refresh the one-page status dashboard `MASTERY.md` (progress / mastery % / review due / next objective) |

## Data Model

```text
<target-repo>/.learning/          ← travels with the repo; auto-gitignored
  ├── MISSION.md                  learning mission (why you want to master it)
  ├── course-map.json             confirmed course map
  ├── progress.json               mastery / spaced review / blockers
  ├── MASTERY.md                  one-page status dashboard (progress / mastery % / review due / next objective)
  ├── records/NNNN-slug.md        ADR-style learning records (understanding evolution)
  ├── notes/<module>.md           structured notes (auto + manual /note interval consolidation)
  ├── notes/.boundary.json        /note interval boundary (module_id + timestamp)
  ├── chapters/<module>.md        textbook-mode chapter material (default path; one per module)
  ├── briefs/<module>.md          module briefs (large repos, token-saving)
  ├── export/                     HTML course output (index.html + modules/0N-slug.html; see Phase 4)
  └── code-map.json               large-repo index (optional)
~/.repo-mastery/                  global lightweight memory
  ├── profile.md                  cross-repo preferences / level / blockers
  └── index.json                  repos studied + resume state
```

## Project Structure

```text
repo-mastery/
├── SKILL.md                        skill definition (English; Agent Skills standard)
├── README.md                       this file
├── README.zh-CN.md                 Chinese mirror
├── ADOPTION.md                     attribution: DeepTutor / docs-to-course / teach
├── CONTRIBUTING.md                 contributor guide
├── AGENTS.md                       protocol for AGENTS.md tools (Codex, opencode, Cursor)
├── GEMINI.md                       protocol for Gemini CLI
├── LICENSE                         MIT
├── package.json                    npm packaging (`repo-mastery install` one-command CLI)
├── .claude-plugin/                 Claude Code plugin marketplace + plugin manifests
│   ├── marketplace.json
│   └── plugin.json
├── agents/
│   └── openai.yaml                 Codex / Agent-Skills UI metadata
├── bin/
│   └── repo-mastery.js             npm one-command installer
├── scripts/
│   ├── learning_engine.py          the deterministic gate (mastery/schedule/record/next/validate/init)
│   ├── index_repo.py               large-repo code index (pure stdlib)
│   └── install.sh                  install to Claude Code + Codex + Gemini (also curl-pipeable)
├── references/                     skill internals (read by the skill per phase)
│   ├── curriculum-design.md        course map design from source
│   ├── mastery-policy.md           mastery / gates / spaced review / error diagnosis
│   ├── session-flow.md             interactive learning protocol (Mission + ZPD)
│   ├── quiz-design.md              quiz design (test application, not memory)
│   ├── module-brief-template.md    module briefs (pre-extracted snippets)
│   ├── note-template.md            note format
│   ├── learning-records-template.md ADR-style learning records
│   ├── gotchas.md                  failure-point checklist
│   ├── index-script-spec.md        index script docs
│   └── html-shell/                 HTML course shell (copied verbatim from docs-to-course)
└── docs/
    ├── ARCHITECTURE.md             design & architecture (English)
    ├── USAGE.md                    usage guide (English)
    └── zh-CN/                      Chinese mirrors
```

## Documentation

- [Architecture](./docs/ARCHITECTURE.md) — design, mastery engine, phases, data model.
- [Usage](./docs/USAGE.md) — detailed command reference and learning walkthrough.
- [Changelog](./CHANGELOG.md) — per-version notable changes (v1.0.0 → v3.0.0).
- [Adoption & attribution](./ADOPTION.md) — what this skill absorbs from DeepTutor, docs-to-course, and the teach skill.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

[MIT](./LICENSE) © 2026 DieselZhang.

## Acknowledgments

- **Mastery engine** adapted from [DeepTutor](https://github.com/HKUDS/DeepTutor) (HKUDS, MIT) — deterministic gates, spaced repetition, error diagnosis, `explore_context` pre-scan.
- **Curriculum design & HTML shell** absorbed from `docs-to-course` (codebase-to-course).
- **Learning mechanisms** (Mission, ZPD, learning records, fluency vs storage) absorbed from [mattpocock-skills](https://github.com/mattpocock)'s `teach` skill.

Full per-item attribution: [ADOPTION.md](./ADOPTION.md).

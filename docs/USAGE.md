# Repo-Mastery Usage Guide

A detailed walkthrough of how to use the skill day to day.

## Installing the skill

The repo itself is the skill (Agent Skills standard). Clone once, install to any
tool — or all of them:

```bash
git clone https://github.com/DieselZhang/repo-mastery.git
cd repo-mastery
./scripts/install.sh          # Claude Code + Codex + Gemini at once
```

Per tool:

- **Claude Code**: `cp -r repo-mastery ~/.claude/skills/repo-mastery` → use `/repo-mastery start <repo>`
- **OpenAI Codex**: `cp -r repo-mastery ~/.codex/skills/repo-mastery` → mention *repo-mastery* or ask to master a repo
- **Gemini CLI**: `cp -r repo-mastery ~/.gemini/skills/repo-mastery` → activate via `activate_skill`
- **AGENTS.md tools** (opencode, Cursor): `cp AGENTS.md <project>/AGENTS.md`

Restart the CLI so the skill is discovered. In Claude Code, verify it appears as
`repo-mastery` in the skills list.

## Quick start

```bash
/repo-mastery start github:DieselZhang/DeepTutor        # learn a GitHub repo (auto-clones)
/repo-mastery start ~/work/my-project                    # learn a local repo
/repo-mastery start ~/work/my-project --language zh      # force Chinese teaching
```

The command walks you through the four phases. What happens next:

1. **Phase 0** — the skill judges repo complexity. For large repos it runs `scripts/index_repo.py` to build a `code-map.json` index (pure stdlib, no install).
2. **Phase 1** — it objectively pre-scans the repo and presents a **course-map proposal**: modules and knowledge points, each backed by source evidence.
3. **Phase 2** — it asks your **Mission** ("why do you want to master this repo?") and you confirm/customize the map — remove modules you don't care about, add ones you do, adjust thresholds. **Nothing is learned before you approve.**
4. **Phase 3** — interactive mastery learning begins, one knowledge point at a time.

## The learning loop

Each knowledge point follows the same loop:

```text
diagnostic → explain → Feynman check → practice → error diagnosis → spaced review
```

- **diagnostic**: the tutor probes what you already know — if you can already explain it, it's skipped (test-out path).
- **explain**: source-grounded explanation with `file:line` references.
- **Feynman check** (concept/design): you explain it back in your own words; the tutor judges.
- **practice**: for usage/procedure points, the tutor poses a question (graded deterministically) and/or asks you to actually run something.
- **error diagnosis**: if you get stuck, you self-attribute and the tutor classifies the error type; it becomes a high-priority review item.
- **spaced review**: the point is scheduled for review at the interval matching its type.

During a session:

- The tutor **auto-writes notes** after each explanation. You can add your own anytime:
  ```bash
  /repo-mastery note "I don't get why this uses a message queue instead of RPC"
  ```
- The tutor may propose **commands** to verify understanding (build/test/run). Read-only commands run directly; anything that writes files or installs dependencies is shown to you and runs only with your approval.

## Commands reference

| Command | What it does |
|---|---|
| `/repo-mastery start <path\|url> [--language zh\|en]` | Start or restart the full flow |
| `/repo-mastery continue` | Resume where you left off (via `next_objective`) |
| `/repo-mastery review` | Run a spaced-review session on due items |
| `/repo-mastery note "<text>"` | Append a personal note to the current module |
| `/repo-mastery status` | Show progress: modules done, points mastered, reviews due |
| `/repo-mastery report` | Generate a human-readable mastery report `MASTERY.md` |
| `/repo-mastery export [--html]` | Synthesize the complete course: `COVERAGE.md` (+ shareable HTML with `--html`) |

## Languages

Teaching language follows your input language by default (Chinese input → Chinese teaching; English input → English teaching). Force one with `--language zh|en` on `start`. Code, paths, and identifiers always stay in their original form.

## Persistence

All state lives in two places:

```text
<target-repo>/.learning/   course map, progress, notes, records, briefs (auto-gitignored)
~/.repo-mastery/           global memory: which repos you've studied and where you left off
```

Because state travels with the repo, you can resume learning on a different machine by cloning the repo (`.learning/` included) — or keep it private by not committing `.learning/` (the skill adds it to `.gitignore` automatically).

## Troubleshooting

| Problem | Likely cause / fix |
|---|---|
| Skill not found | Restart Claude Code; confirm the dir is `~/.claude/skills/repo-mastery` |
| `github:owner/repo` clone fails | Network/auth; provide a local path instead |
| Large repo feels slow | The skill should have run `index_repo.py`; check `.learning/code-map.json` exists |
| `progress.json` corrupted | Restore from git, or delete it (you'll lose progress but the course map survives) |
| Wrong language | Pass `--language zh` / `--language en` explicitly |

## Going further

- **Architecture & design**: [ARCHITECTURE.md](./ARCHITECTURE.md)
- **Skill internals**: the `references/` directory (read per phase by the skill).
- **Contributing**: [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Attribution**: [ADOPTION.md](../ADOPTION.md)

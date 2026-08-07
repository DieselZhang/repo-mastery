# Contributing to Repo-Mastery

Thanks for your interest in contributing! This skill is open-sourced so developers everywhere can learn codebases deeply. Any help is welcome — bug reports, feature ideas, documentation, or code.

## Ways to contribute

- **Report a bug** — open an issue with a clear reproduction.
- **Suggest a feature** — open an issue describing the use case and why it matters.
- **Improve documentation** — PRs to `README*`, `docs/`, or `references/`.
- **Add tests or examples** — e.g. run the skill against a real repo and share the `course-map.json` + `COVERAGE.md` you got.
- **Submit to ECC** — once the skill is stable, consider submitting it to the [Everything Claude Code](https://github.com/affaan-m/everything-claude-code) skill collection. This repo already follows its skill development conventions (English frontmatter `description`, `origin`, `version`, reference-driven SKILL.md).

## Development workflow

```bash
git clone https://github.com/DieselZhang/repo-mastery.git ~/.claude/skills/repo-mastery
cd ~/.claude/skills/repo-mastery
```

1. **Branch first** — create a branch for your change: `git checkout -b feat/my-change`.
2. **Edit** — keep changes focused. If you touch `references/`, update the "read in phase" headers so the skill loads them at the right time.
3. **Test locally** — the skill *is* the repo; `~/.claude/skills/repo-mastery` is a live install. Run a change against a real repo:
   ```bash
   /repo-mastery start ~/some/repo
   ```
   For the index script:
   ```bash
   python3 scripts/index_repo.py <repo> -o /tmp/code-map.json
   ```
4. **Commit** — a clear message describing the change and why. Example: `feat(mastery): ...` / `fix(session-flow): ...` / `docs(readme): ...`.
5. **Open a PR** — describe the change, how you tested it, and anything reviewers should know.

## Conventions

- **Language** — `SKILL.md` frontmatter `description` and all `references/` must be **English** (the skill is used worldwide). `README.zh-CN.md` and `docs/zh-CN/` are the Chinese mirrors — keep them in sync when you change the English versions.
- **Dual-format docs** — when you edit `README.md` / `docs/`, mirror the change into `README.zh-CN.md` / `docs/zh-CN/`.
- **HTML shell is frozen** — `references/html-shell/*` (styles.css, main.js, build.sh, _base.html, _footer.html, interactive-elements.md, design-system.md) are copied verbatim from docs-to-course and must **never** be regenerated or restyled here. Fixes to the shell belong in the upstream skill.
- **The gate is code, not prose** — `scripts/learning_engine.py` is the single source of truth for `compute-mastery`, spaced review, `record-attempt`, and `next-objective`. When you change mastery math, change it **here first**, then update `references/mastery-policy.md` to match. Never let a reference formula drift from the script.
- **Multi-tool entry files** — when you change the workflow, keep `AGENTS.md`, `GEMINI.md`, and `SKILL.md` consistent (they describe the same protocol for different tools). Verify the engine with `python3 scripts/learning_engine.py --help` and the subcommand tests.
- **Attribution** — if you add a design absorbed from another project, note it in `ADOPTION.md`.
- **No secrets** — never commit API keys, tokens, or absolute personal paths.

## Verification checklist

- [ ] `SKILL.md` frontmatter valid (`name`, English `description`, `version` bumped).
- [ ] English docs + Chinese mirrors in sync.
- [ ] `references/html-shell/` untouched.
- [ ] No sensitive data.
- [ ] Index script still runs (if touched): `python3 scripts/index_repo.py --help`.

## Code of conduct

Be respectful and constructive. This is a small, friendly project — assume good intent.

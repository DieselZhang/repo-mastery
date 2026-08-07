#!/usr/bin/env node
/**
 * repo-mastery — one-command installer for the repo-mastery skill.
 *
 * Copies this package's skill files into the skill directories of Claude Code,
 * OpenAI Codex, and/or Gemini CLI, so the skill is usable everywhere without
 * cloning the repo.
 *
 * Usage:
 *   repo-mastery install                     install to Claude Code + Codex + Gemini
 *   repo-mastery install --only codex        install to Codex only
 *   repo-mastery install --skip gemini       skip Gemini
 *   repo-mastery install --dry-run           show what would happen
 *   repo-mastery --help
 *   repo-mastery --version
 *
 * Tool directories (overridable via env):
 *   CLAUDE_SKILLS_DIR   default ~/.claude/skills
 *   CODEX_SKILLS_DIR    default ~/.codex/skills
 *   GEMINI_SKILLS_DIR   default ~/.gemini/skills
 */
"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");

const SRC = path.join(__dirname, ".."); // the npm package root == skill root
const TOOLS = [
  { key: "claude", dir: process.env.CLAUDE_SKILLS_DIR || path.join(os.homedir(), ".claude", "skills") },
  { key: "codex", dir: process.env.CODEX_SKILLS_DIR || path.join(os.homedir(), ".codex", "skills") },
  { key: "gemini", dir: process.env.GEMINI_SKILLS_DIR || path.join(os.homedir(), ".gemini", "skills") },
];

function copyDir(src, dest, skip = [".git"]) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    if (skip.includes(entry.name)) continue;
    const s = path.join(src, entry.name);
    const d = path.join(dest, entry.name);
    if (entry.isDirectory()) copyDir(s, d, skip);
    else fs.copyFileSync(s, d);
  }
}

function usage() {
  console.log(`repo-mastery — one-command skill installer

Usage:
  repo-mastery install [--only <tool>] [--skip <tool>] [--dry-run]
  repo-mastery --help | --version

Tools: ${TOOLS.map((t) => t.key).join(", ")}
Env overrides: CLAUDE_SKILLS_DIR, CODEX_SKILLS_DIR, GEMINI_SKILLS_DIR
`);
}

function main() {
  const args = process.argv.slice(2);
  if (args.includes("--help") || args.includes("-h") || args.length === 0) return usage();
  if (args.includes("--version")) {
    console.log(require(path.join(SRC, "package.json")).version);
    return;
  }

  const cmd = args[0];
  if (cmd !== "install") {
    console.error(`Unknown command: ${cmd}`);
    usage();
    process.exit(1);
  }

  const only = argValue(args, "--only");
  const skip = collectValues(args, "--skip");
  const dryRun = args.includes("--dry-run");

  const want = (tool) =>
    (only ? only === tool : true) && !skip.includes(tool);

  const installed = [];
  for (const t of TOOLS) {
    if (!want(t.key)) continue;
    const dest = path.join(t.dir, "repo-mastery");
    console.log(`→ ${t.key.padEnd(6)} : ${dest}`);
    if (!dryRun) {
      copyDir(SRC, dest);
      installed.push(t.key);
    }
  }

  console.log("");
  if (dryRun) {
    console.log("(dry-run) No files copied.");
    return;
  }
  console.log(`✅ Installed repo-mastery to: ${installed.length ? installed.join(", ") : "none"}`);
  console.log("   Restart your CLI, then:");
  console.log("     Claude Code : /repo-mastery start <repo>");
  console.log("     Codex       : mention 'repo-mastery' or ask to master a repo");
  console.log("     Gemini      : activate_skill(repo-mastery)");
}

function argValue(args, flag) {
  const i = args.indexOf(flag);
  if (i === -1) return "";
  return args[i + 1] || "";
}

function collectValues(args, flag) {
  const out = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === flag && args[i + 1]) out.push(args[i + 1]);
    else if (args[i].startsWith(`${flag}=`)) out.push(args[i].split("=")[1]);
  }
  return out;
}

main();

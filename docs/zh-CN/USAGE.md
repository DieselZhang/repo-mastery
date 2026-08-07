# Repo-Mastery 使用指南

详细的日常使用流程说明。

## 安装 skill

本仓库本身就是这个 skill（Agent Skills 标准）。clone 一次，可安装到任意工具——或全部：

```bash
git clone https://github.com/DieselZhang/repo-mastery.git
cd repo-mastery
./scripts/install.sh          # Claude Code + Codex + Gemini 一次装好
```

按工具：

- **Claude Code**：`cp -r repo-mastery ~/.claude/skills/repo-mastery` → 用 `/repo-mastery start <仓库>`
- **OpenAI Codex**：`cp -r repo-mastery ~/.codex/skills/repo-mastery` → 提到 *repo-mastery* 或要求掌握某仓库
- **Gemini CLI**：`cp -r repo-mastery ~/.gemini/skills/repo-mastery` → 经 `activate_skill` 激活
- **AGENTS.md 工具**（opencode、Cursor）：`cp AGENTS.md <项目>/AGENTS.md`

重启 CLI 让 skill 被发现。在 Claude Code 中，用技能列表确认出现 `repo-mastery` 条目。

## 快速开始

```bash
/repo-mastery start github:DieselZhang/DeepTutor        # 学一个 GitHub 仓库（自动 clone）
/repo-mastery start ~/work/my-project                    # 学一个本地仓库
/repo-mastery start ~/work/my-project --language zh      # 强制中文教学
```

命令会带你走完四个阶段。接下来发生什么：

1. **Phase 0** —— skill 判断仓库复杂度。大型仓库会运行 `scripts/index_repo.py` 生成 `code-map.json` 索引（纯标准库，无需安装）。
2. **Phase 1** —— 客观预扫描仓库，给出**课程地图提案**：模块与知识点，每个都带源码证据。
3. **Phase 2** —— 询问你的 **Mission**（"为什么想掌握这个仓库？"），你确认/定制地图 —— 删掉不关心的模块、加上感兴趣的、调整阈值。**批准前绝不开始学习。**
4. **Phase 3** —— 交互式掌握度学习开始，一次一个知识点。

## 学习循环

每个知识点走同一循环：

```text
诊断 → 讲解 → 费曼检验 → 练习 → 错误诊断 → 间隔复习
```

- **诊断**：tutor 探测你已知多少 —— 能讲清就直接跳过（test-out 路径）。
- **讲解**：基于源码的讲解，带 `文件:行` 引用。
- **费曼检验**（concept/design）：你用自己话复述，tutor 判定。
- **练习**：使用/操作类知识点，tutor 出题（确定性判分）和/或让你实际跑。
- **错误诊断**：卡住时你自述归因，tutor 判定错误类型；它成为高优先级复习项。
- **间隔复习**：该知识点按类型对应间隔排入复习计划。

会话中：

- tutor 每次讲解后**自动写笔记**。你可以随时追加自己的：
  ```bash
  /repo-mastery note "我不懂这里为什么用消息队列不用 RPC"
  ```
- tutor 可能提议运行**命令**来验证理解（构建/测试/运行）。只读命令直接运行；任何写文件或装依赖的操作会先展示给你，经你批准才运行。

## 命令参考

| 命令 | 作用 |
|---|---|
| `/repo-mastery start <路径\|url> [--language zh\|en]` | 开始或重启完整流程 |
| `/repo-mastery continue` | 从上次位置续学（经 `next_objective`） |
| `/repo-mastery review` | 到期项的间隔复习会话 |
| `/repo-mastery note "<文本>"` | 向当前模块追加个人笔记 |
| `/repo-mastery status` | 查看进度：已完成模块、已掌握知识点、待复习 |
| `/repo-mastery report` | 生成可读的掌握度报告 `MASTERY.md` |
| `/repo-mastery export [--html]` | 合成完整课程：`COVERAGE.md`（`--html` 额外生成可分享 HTML） |

## 语言

讲解语言默认跟随你的输入语言（中文输入 → 中文教学；英文输入 → 英文教学）。`start` 时传 `--language zh|en` 可强制指定。代码、路径、标识符始终保持原文。

## 持久化

所有状态存在两处：

```text
<目标仓库>/.learning/   课程地图、进度、笔记、记录、简报（自动 gitignore）
~/.repo-mastery/        全局记忆：学过的仓库 + 上次学到哪
```

因为状态随仓库走，你在别的机器 clone 该仓库（含 `.learning/`）即可续学 —— 或者不提交 `.learning/` 保持私有（skill 会自动把它加进 `.gitignore`）。

## 排障

| 问题 | 可能原因 / 解决 |
|---|---|
| 找不到 skill | 重启 Claude Code；确认目录是 `~/.claude/skills/repo-mastery` |
| `github:owner/repo` clone 失败 | 网络/认证问题；改用本地路径 |
| 大型仓库感觉慢 | skill 应已运行 `index_repo.py`；确认 `.learning/code-map.json` 存在 |
| `progress.json` 损坏 | 从 git 恢复，或删除它（会丢进度但课程地图保留） |
| 语言不对 | 显式传 `--language zh` / `--language en` |

## 深入

- **架构与设计**：[ARCHITECTURE.md](./ARCHITECTURE.md)
- **skill 内部**：`references/` 目录（skill 按阶段读取）。
- **贡献**：[CONTRIBUTING.md](../../CONTRIBUTING.md)
- **归属**：[ADOPTION.md](../../ADOPTION.md)

# repo-mastery

> 把任意开源仓库变成**开发者视角的掌握式课程** —— 像学一门课一样，逐步掌握一个项目的 **使用 → 架构 → 关键实现**。

一个 Claude Code skill。输入本地仓库路径或 GitHub URL，通过 **课程地图确认 → 交互式掌握度学习 → 动手实践 → 笔记沉淀 → 完整课程文档（Markdown + HTML 双形态）**，帮你把"浏览代码"升级为"彻底吃透一个开源项目"。

## 它解决什么问题

作为开发者，拿到一个开源项目代码后，常见困境是：读完了却谈不上"掌握"。repo-mastery 用一套可判定的学习机制解决它 —— 每个知识点都有**确定性掌握度判定**（不是 LLM 拍脑袋），有**间隔复习**对抗遗忘，有**笔记沉淀**形成长期记忆。

## 核心设计

| 设计 | 来源 |
|---|---|
| **智能在出口，进阶在闸门** —— 模型决定教什么，能否进阶由确定性引擎判定 | DeepTutor `learning/` 模块 |
| 近因加权准确率 ≥ 0.9 定量闸门 + 置信度上限（一次蒙对不算掌握） | DeepTutor `mastery.py` |
| 费曼式定性判定（concept/design 型） | DeepTutor |
| 每类型不同间隔序列的间隔重复 + 错题提升优先级 | DeepTutor `scheduler.py` |
| 错误诊断四分类（结构性/理解偏差/应用错误/元认知） | DeepTutor `models.py` |
| 期望答案存服务端、永不回传（判定不漂移） | DeepTutor `PendingQuestion` |
| "reference → route" 课程设计弧线、测验哲学、模块简报预提取、HTML 课程外壳 | docs-to-course（codebase-to-course） |

**与 docs-to-course 的区别**：它吃**文档**、面向**终端用户**、学到"会用"为止、一次性产出静态 HTML。repo-mastery 吃**源码**、面向**开发者**、学到"能吃透并讲清为什么"、交互式掌握度驱动 + 双形态课程产出。

## 用法

```bash
/repo-mastery start <本地路径 | github:owner/repo>   # 主流程
/repo-mastery continue                                # 续学上次进度
/repo-mastery review                                  # 间隔复习
/repo-mastery note "<文本>"                           # 手动追加笔记
/repo-mastery status                                  # 查看进度
/repo-mastery report                                  # 掌握度报告
/repo-mastery export [--html]                         # 合成完整课程文档
```

## 主流程一览

```text
Phase 0  复杂度评估 → 决定提取方式（纯读 / Python 索引脚本）
Phase 1  预扫描（explore_context 式）→ 课程地图候选
Phase 2  确立 Mission + 你确认/定制课程地图（强制步骤）
Phase 3  交互式掌握度学习（诊断→讲解→费曼→练习→错误诊断→间隔复习）
Phase 4  合成 COVERAGE.md（Markdown）+ 可选 HTML 分享版
```

## 数据结构

```text
<目标仓库>/.learning/        随仓库走，自动 gitignore
  ├── MISSION.md             学习使命（你为什么想掌握它）
  ├── course-map.json        课程地图（已确认版）
  ├── progress.json          掌握度/间隔复习/卡点
  ├── records/NNNN-slug.md   ADR 式学习记录（理解演化）
  ├── notes/<module>.md      结构化笔记
  ├── briefs/<module>.md     模块简报（大型仓库省 token）
  └── code-map.json          大型仓库索引（可选）
~/.repo-mastery/             全局轻量记忆
  ├── profile.md             跨仓库偏好/水平
  └── index.json             学过的仓库清单/状态
```

## 结构

```text
repo-mastery/
├── SKILL.md                        主流程编排
├── README.md                       本文件
├── ADOPTION.md                     采纳与吸收说明（DeepTutor / codebase-to-course）
├── LICENSE                         MIT
├── scripts/
│   └── index_repo.py               大型仓库代码索引（纯标准库）
└── references/
    ├── curriculum-design.md        从源码设计课程地图
    ├── mastery-policy.md           掌握度/闸门/间隔复习/错误诊断/fluency-storage
    ├── session-flow.md             交互式学习会话协议（含 Mission + ZPD）
    ├── quiz-design.md              测验设计（测应用不测记忆）
    ├── module-brief-template.md    模块简报（预提取源码片段）
    ├── note-template.md            笔记格式
    ├── learning-records-template.md ADR 式学习记录
    ├── gotchas.md                  失败点检查清单
    ├── index-script-spec.md        索引脚本说明
    └── html-shell/                 HTML 课程外壳（复制自 docs-to-course，verbatim）
```

## 采纳与许可

本 skill 站在两个上游的肩膀上：

- **掌握式学习引擎** 采纳自 [DeepTutor](https://github.com/HKUDS/DeepTutor)（HKUDS，MIT）——确定性掌握度闸门、间隔重复、错误诊断、explore_context 预扫描等。
- **课程设计与产出外壳** 吸收自 codebase-to-course（docs-to-course，作者个人技能）——"reference → route"课程弧线、测验哲学、模块简报预提取、HTML 课程外壳。

详见 [ADOPTION.md](./ADOPTION.md)（逐条说明采纳了什么、刻意不吸收什么）。本仓库以 MIT License 发布（见 [LICENSE](./LICENSE)）。

## 安装

```bash
mkdir -p ~/.claude/skills && cp -r . ~/.claude/skills/repo-mastery
# 或在 ~/.claude/skills/ 下把本目录链接/复制为 repo-mastery
```

> 依赖：Claude Code（skill 运行时）；Python 3 仅大型仓库索引脚本需要（纯标准库）。

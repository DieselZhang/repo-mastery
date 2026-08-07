# Index Script Spec — `scripts/index_repo.py` 使用说明

> **何时读**：Phase 0 判定仓库为大型时。运行脚本，用 `code-map.json` 支撑课程地图与按需学习，避免整仓塞进上下文。

## 何时需要索引

Phase 0 的"大型"判定（任一命中）：源文件 ≥ 10 万行、顶层模块 ≥ 20、依赖复杂/多语言混编。不确定时实际跑一下 `find` + `wc -l`，不要猜。

## 运行

```bash
python3 ~/.claude/skills/repo-mastery/scripts/index_repo.py <repo_path> -o <repo_path>/.learning/code-map.json
```

- 纯标准库，**无需安装依赖**。
- 只读扫描仓库，跳过黑名单目录（`.git`、`node_modules`、`.venv`、`dist` 等）。
- 输出写临时文件后原子 rename，避免半成品。

## `code-map.json` 结构

```jsonc
{
  "repo": "owner/name",
  "summary": {
    "total_source_files": 1234,
    "total_lines": 182340,
    "languages": { "python": 800, "typescript": 300 },
    "top_dirs": [ { "name": "deeptutor", "files": 600 } ]   // 顶层目录统计
  },
  "entry_points": [ "package.json/main: src/index.js", "main.py" ],
  "dependency_graph": { "src/pipeline.py": ["deeptutor", "core"] },  // 仅项目内边
  "files": [ { "path": "src/pipeline.py", "lang": "python", "lines": 640 } ],
  "symbol_lookup": { "python": [ "src/pipeline.py", "..." ] }  // 每语言最重 30 文件
}
```

## 怎么用它做课程地图（Phase 1）

1. **模块划分** ← `summary.top_dirs` + `dependency_graph`：顶层目录就是候选模块边界；依赖边的聚集处是"关键实现"模块的好候选。
2. **关键实现定位** ← `symbol_lookup` + `files` 按 `lines` 降序：最重的文件往往是核心。
3. **使用模块证据** ← `entry_points`：入口文件构成"跑通构建/核心工作流"模块的证据。
4. **学习时按需 Read** ← 从地图的知识点 → `files` 里的 `path` → Read 对应 `文件:行`。不再整仓扫。

## 已知局限（诚实说明）

- 依赖提取是**启发式正则**，不是语法树 —— 动态导入、间接引用会漏。它用于"找候选"而非"穷举"。
- 多语言混编仓库（如 Rust 核心 + Python 封装）只按扩展名归类，跨语言边界仍要靠 README/文档补。
- 对极端巨型仓库（百万行级 monorepo），建议先对子目录分别建索引，或只索引你最关心的子系统。

## 索引放哪

- 默认建议 `<repo>/.learning/code-map.json`（随仓库走）。仓库很大时也可放 `~/.repo-mastery/caches/<repo-id>/code-map.json`，不污染目标仓库 —— 二选一，保持一致。

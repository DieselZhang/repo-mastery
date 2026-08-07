# Mastery Policy — 掌握度、闸门与间隔复习

> **何时读**：Phase 3。这是纯决策引擎 —— **不含 LLM 调用、不含 IO**。tutor 每个学习轮次都 consult 这里的规则。三个核心问题：**这个知识点掌握了吗？下一步该学什么？整张地图什么样？**

本策略从 DeepTutor 的 `learning/` 模块移植（`mastery.py` / `policy.py` / `scheduler.py` / `models.py`），只把"学科知识"换成"代码知识"。

## 0. 设计原理：Fluency vs Storage Strength（吸收自 teach skill）

区分两种"会"：

- **Fluency（流利度）**：当下就能想起来 —— 刚听完讲解的"我懂了"。它给人**虚假的掌握感**。
- **Storage（存储强度）**：长期保持，隔一阵还能用对 —— 这才是真正的目标。

本策略的所有机制都在对抗"流利度幻觉"：

- 置信度上限（一次蒙对不算掌握）→ 防"流利度冒充掌握度"。
- 费曼复述（不是点头说懂）→ 强制从存储中检索。
- 间隔重复（延迟复习）→ 只有能在遗忘后检索出来的才是 storage。

**ZPD（最近发展区）**：下一步教什么 = 挑战"刚好够"。判断依据 = `records/`（用户已确立的理解）+ `progress.json`（掌握度）+ Mission（为什么学）。不重新覆盖已掌握的，也不一步跨太远。

## 1. 知识类型与闸门（gate）

| type | 闸门类型 | 通过条件 |
|---|---|---|
| `memory` | 定量 | 近因加权准确率 ≥ **0.9** |
| `procedure` | 定量 | 近因加权准确率 ≥ **0.9**（且关键动手任务跑通为证据） |
| `concept` | 定性 | tutor 判定费曼复述通过（`mastery_assess`） |
| `design` | 定性 | tutor 判定费曼复述 + 设计权衡追问通过 |

**设计公理**：定量类型（memory/procedure）用精确判定，因为多数有唯一正确答案；概念/设计用定性判定，因为"为什么这么设计"没有唯一标准答案 —— 这正是 DeepTutor 的分裂方式。

## 2. 定量掌握度计算（`compute_mastery`）

```text
输入：某知识点按时间序的答题正确性 [bool, ...]
取最近最多 5 次，权重从旧到新 = (0.5, 0.7, 0.85, 0.95, 1.0)
score = Σ(权重 × 对/错) / Σ权重
置信度上限：仅 1 次记录 → score 上限 0.5；仅 2 次 → 上限 0.8
mastery = min(score, 上限)
```

**含义**：
- 新的尝试权重大 —— 早期犯错后恢复会被奖励。
- **一次蒙对不能算掌握** —— 置信度上限把 mastery 压到 0.5/0.8，到不了 0.9 的闸门。
- 判定是确定性的，记录在 `progress.json`，不依赖 tutor 记忆。

## 3. 间隔重复调度（spaced repetition）

每种类型一套间隔序列（天数）：

| type | 间隔序列 |
|---|---|
| `memory` | `[0, 1, 3, 7, 14, 30]` |
| `concept` | `[3, 7, 14, 30]` |
| `procedure` | `[3, 7, 14]` |
| `design` | `[14, 28]` |

**调度规则**（`schedule_next`）：
- 答对：`consecutive_correct += 1`；连续答对 ≥2 次 → 索引 +2；否则 +1。
- 答错：`consecutive_wrong += 1`；索引回退 1（下限 0）；连续错 ≥2 次 → 计数清零。
- 索引夹在 `[0, 最大索引]`，`next_review_at = now + 间隔[索引]`。

**优先级**：有**错误记录**（active/retrying 状态）的知识点优先级 = 1（最高），否则按类型 `memory:2 / concept:3 / procedure:4 / design:5`。到期的复习任务按优先级排序。

## 4. 下一步该学什么（`next_objective`）

**进阶由"已掌握的内容"计算而来，绝不是阶段计数器。** 优先级从高到低：

1. **有挂起的题目**（`pending_question`）→ 先判定它（`answer_pending`）。
2. **有到期的复习** → 先复习，不让已掌握的地基衰减（`review`）。
3. **第一个未掌握的知识点**（按模块 order 再知识点顺序）：
   - 从未学过 → `probe`（先测能不能跳过 —— **test-out 路径**：已证明掌握的直接跳过，不按固定阶段走）。
   - 定量类型未达闸门 → `practice`（继续练到过线）。
   - 定性类型 → `assess`（费曼检验）。
4. **全部掌握且无到期复习** → `complete`。

`NextStep` 动作集：`answer_pending / review / probe / practice / assess / complete`。

## 5. 错误诊断与元认知

答错/卡壳时，判定**错误类型**（DeepTutor 四分类，映射到代码学习）：

| ErrorType | 含义 | 代码学习例子 |
|---|---|---|
| `structural`（知识结构性） | 缺前置知识/上下文 | "不懂 `asyncio`，所以看不懂这个异步框架" |
| `deviation`（理解偏差） | 概念理解错了 | "以为 RAG 是训练模型，其实是检索增强" |
| `application`（应用错误） | 概念对但用错场景 | "知道有锁，但用在了不该用的地方" |
| `metacognitive`（元认知型） | 不知道自己不知道 | "以为自己懂了，复述时才发现全是漏洞" |

每个错误记录：`error_type` + 用户自述归因 + tutor 确认 + 重试历史。**status 流转**：`active → retrying → review → graduated`。active/retrying 的错误会提升该知识点的复习优先级。

## 6. 定性判定（`mastery_assess`）

concept/design 型知识点的"费曼检验"判定标准：

- **concept**：用户能用自己的话讲清"是什么 + 为什么 + 与相邻概念的关系"。讲不清 → 判不过 → 回炉讲解，记录错误类型。
- **design**：除复述外，追加设计权衡追问 —— "为什么不选另一种方案？换一种场景它会怎么失败？扩展点在哪？" 能回答权衡 = 掌握。

定性判定结果存 `qualitative_mastery: {kp_id: bool}`；通过后地图显示满值，但判定本身是布尔，不是分数。

## 7. 进度数据结构（`progress.json`）

```jsonc
{
  "repo": "owner/name",
  "diagnostic": { "module_mastery": {} },
  "modules": [
    { "id": "m01", "name": "跑通构建与环境", "order": 1,
      "pass_threshold": 0.7,
      "knowledge_points": [ { "id": "kp01-01", "name": "...", "type": "procedure" } ] }
  ],
  "mastery_levels": { "kp01-01": 0.42 },       // 定量掌握度 0..1
  "qualitative_mastery": { "kp01-02": true },  // 定性判定结果
  "knowledge_types": { "kp01-01": "procedure" },
  "quiz_attempts": [ { "question_id": "q1", "knowledge_point_id": "kp01-01",
                       "is_correct": false, "error_type": "deviation",
                       "mastery_estimate": 0.0, "timestamp": 1754567890 } ],
  "error_records": [ { "id": "e1", "knowledge_point_id": "kp01-01",
                       "error_type": "deviation", "status": "active" } ],
  "repetition_states": { "kp01-01": { "interval_index": 0, "next_review_at": 1754571490 } },
  "review_queue": [ { "id": "review_kp01-01", "knowledge_point_id": "kp01-01",
                      "due_at": 1754571490, "priority": 1 } ],
  "pending_question": { "question_id": "q3", "knowledge_point_id": "kp01-01",
                        "prompt": "...", "question_type": "short", "expected_answer": "..." },
  "version": 1
}
```

**关键点**：
- `pending_question.expected_answer` **存在服务端（本文件）**，绝不随问题回传给用户 —— 判定永不漂移（DeepTutor `PendingQuestion` 设计）。
- 所有时间戳用 Unix 秒。
- 文件一旦存在，每轮学习结束**原子写回**（先写临时文件再改名），避免损坏。

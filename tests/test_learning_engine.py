"""Tests for the deterministic learning engine (pytest-compatible; also runnable directly)."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from learning_engine import schedule_next, next_objective


def test_correct_updates_difficulty_and_stability():
    s = schedule_next("memory", True, {})
    assert s["difficulty"] == 0.45        # 0.5 - 0.05
    assert s["stability"] == 1.2          # 1.0 * (1 + 0.2*1)
    assert s["interval_index"] == 1       # single correct: index +1


def test_wrong_raises_difficulty():
    s = schedule_next("memory", False, {"difficulty": 0.5, "stability": 1.0,
                                        "interval_index": 2,
                                        "consecutive_correct": 1,
                                        "consecutive_wrong": 0})
    assert s["difficulty"] == 0.65        # 0.5 + 0.15
    assert s["stability"] == 1.0          # max(1.0, 1.0*0.5) = 1.0
    assert s["interval_index"] == 1       # wrong: index -1


def test_hard_point_is_reviewed_sooner():
    state = {"interval_index": 3, "difficulty": 0.5, "stability": 1.0,
             "consecutive_correct": 0, "consecutive_wrong": 0}
    easy = schedule_next("memory", True, {**state, "difficulty": 0.2})
    hard = schedule_next("memory", True, {**state, "difficulty": 0.8})
    assert hard["next_review_at"] < easy["next_review_at"]


def test_stable_point_is_reviewed_later():
    state = {"interval_index": 3, "difficulty": 0.5, "stability": 1.0,
             "consecutive_correct": 0, "consecutive_wrong": 0}
    fresh = schedule_next("memory", True, {**state, "stability": 1.0})
    stable = schedule_next("memory", True, {**state, "stability": 4.0})
    assert stable["next_review_at"] > fresh["next_review_at"]


def test_old_state_without_params_is_backward_compatible():
    old = {"interval_index": 0, "consecutive_correct": 0, "consecutive_wrong": 0}
    s = schedule_next("memory", True, old)
    assert s["difficulty"] == 0.45        # defaulted to 0.5, then -0.05
    assert s["stability"] == 1.2          # defaulted to 1.0, then *1.2


def test_next_objective_interleaves_types():
    progress = {
        "modules": [],
        "last_review_type": "memory",
        "review_queue": [
            {"id": "r_mem", "knowledge_point_id": "kp_mem", "knowledge_type": "memory",
             "due_at": 0, "priority": 2},
            {"id": "r_con", "knowledge_point_id": "kp_con", "knowledge_type": "concept",
             "due_at": 0, "priority": 2},
        ],
        "repetition_states": {},
    }
    out = next_objective(progress, now=1)
    assert out["knowledge_point_id"] == "kp_con"   # different type wins over same type


def test_next_objective_falls_back_when_all_same_type():
    progress = {
        "modules": [],
        "last_review_type": "memory",
        "review_queue": [
            {"id": "r1", "knowledge_point_id": "kp1", "knowledge_type": "memory",
             "due_at": 0, "priority": 2},
        ],
        "repetition_states": {},
    }
    out = next_objective(progress, now=1)
    assert out["knowledge_point_id"] == "kp1"

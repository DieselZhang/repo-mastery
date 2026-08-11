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


def test_memory_points_are_skipped_by_next_objective():
    """Demoted memory points never gate advancement: a map with only memory
    points is 'complete'."""
    progress = {
        "modules": [{"id": "m01", "order": 1, "name": "M",
                     "knowledge_points": [
                         {"id": "kp_mem", "type": "memory"},
                         {"id": "kp_mem2", "type": "memory"},
                     ]}],
        "mastery_levels": {}, "knowledge_types": {},
        "quiz_attempts": [], "qualitative_mastery": {},
        "repetition_states": {}, "review_queue": [], "error_records": [],
    }
    out = next_objective(progress, now=1)
    assert out["action"] == "complete"


def test_next_objective_picks_procedure_over_memory():
    """In a mixed map, memory points are skipped and the first non-memory
    point is selected."""
    progress = {
        "modules": [{"id": "m01", "order": 1, "name": "M",
                     "knowledge_points": [
                         {"id": "kp_mem", "type": "memory"},
                         {"id": "kp_proc", "type": "procedure"},
                     ]}],
        "mastery_levels": {}, "knowledge_types": {},
        "quiz_attempts": [], "qualitative_mastery": {},
        "repetition_states": {}, "review_queue": [], "error_records": [],
    }
    out = next_objective(progress, now=1)
    assert out["knowledge_point_id"] == "kp_proc"
    assert out["action"] in ("practice", "probe")


def test_rebuild_review_queue_skips_memory():
    """Memory points are reference notes, never review candidates."""
    from learning_engine import _rebuild_review_queue
    progress = {
        "modules": [],
        "knowledge_types": {"kp_mem": "memory", "kp_proc": "procedure"},
        "repetition_states": {
            "kp_mem": {"next_review_at": 0},
            "kp_proc": {"next_review_at": 0},
        },
        "error_records": [],
    }
    _rebuild_review_queue(progress)
    ids = [t["knowledge_point_id"] for t in progress["review_queue"]]
    assert "kp_proc" in ids
    assert "kp_mem" not in ids


def test_record_attempt_to_next_objective_roundtrip():
    """record_attempt writes difficulty/stability/last_review_type/review_queue,
    and next_objective still drives the next step."""
    from learning_engine import record_attempt

    progress = {
        "modules": [{"id": "m01", "order": 1, "name": "M",
                     "knowledge_points": [{"id": "kp1", "type": "procedure"}]}],
        "mastery_levels": {}, "knowledge_types": {},
        "quiz_attempts": [], "repetition_states": {},
        "review_queue": [], "error_records": [],
    }
    record_attempt(progress, kp_id="kp1", kp_type="procedure", is_correct=True,
                   question_id="q1")
    # core data-model writes
    assert progress["last_review_type"] == "procedure"
    assert progress["repetition_states"]["kp1"]["difficulty"] == 0.45
    assert progress["repetition_states"]["kp1"]["stability"] == 1.2
    assert any(t["knowledge_point_id"] == "kp1" for t in progress["review_queue"])
    # next_objective still works and picks the unmastered point
    out = next_objective(progress, now=1)
    assert out["action"] in ("practice", "probe", "complete")


def test_flow_phase_overview_blocks_new_points():
    """While flow_phase is 'overview', next_objective refuses to hand out a
    knowledge point — the whole picture comes before the nodes."""
    progress = {
        "flow_phase": "overview",
        "modules": [{"id": "m01", "order": 1, "name": "M",
                     "knowledge_points": [{"id": "kp1", "type": "procedure"}]}],
        "mastery_levels": {}, "knowledge_types": {},
        "quiz_attempts": [], "repetition_states": {},
        "review_queue": [], "error_records": [],
    }
    out = next_objective(progress, now=1)
    assert out["action"] == "overview"
    assert "knowledge_point_id" not in out


def test_flow_phase_module_overview_returns_module():
    progress = {
        "flow_phase": "module_overview",
        "current_module_id": "m02",
        "modules": [{"id": "m02", "order": 2, "name": "M2",
                     "knowledge_points": [{"id": "kp1", "type": "procedure"}]}],
        "mastery_levels": {}, "knowledge_types": {},
        "quiz_attempts": [], "repetition_states": {},
        "review_queue": [], "error_records": [],
    }
    out = next_objective(progress, now=1)
    assert out["action"] == "module_overview"
    assert out["module_id"] == "m02"


def test_flow_phase_missing_defaults_to_learning():
    """Old progress.json without flow_phase is backward compatible: the gate
    is skipped and the first unmastered point is returned directly."""
    progress = {
        "modules": [{"id": "m01", "order": 1, "name": "M",
                     "knowledge_points": [{"id": "kp1", "type": "procedure"}]}],
        "mastery_levels": {}, "knowledge_types": {},
        "quiz_attempts": [], "repetition_states": {},
        "review_queue": [], "error_records": [],
    }
    out = next_objective(progress, now=1)
    assert out["action"] == "probe"
    assert out["knowledge_point_id"] == "kp1"


def test_review_mode_bypasses_flow_phase_gate():
    """mode='review' (the /repo-mastery review command) ignores the overview
    gate and drains only due reviews — scattered-time review is never blocked
    by an unfinished overview."""
    progress = {
        "flow_phase": "overview",   # unfinished overview, but review must work
        "modules": [{"id": "m01", "order": 1, "name": "M",
                     "knowledge_points": [{"id": "kp1", "type": "procedure"}]}],
        "mastery_levels": {}, "knowledge_types": {"kp1": "procedure"},
        "quiz_attempts": [], "repetition_states": {},
        "review_queue": [{"id": "r1", "knowledge_point_id": "kp1",
                          "knowledge_type": "procedure", "due_at": 0, "priority": 2}],
        "error_records": [],
    }
    out = next_objective(progress, now=1, mode="review")
    assert out["action"] == "review"
    assert out["knowledge_point_id"] == "kp1"
    # once nothing is due, review mode completes without opening content
    progress["review_queue"] = []
    out = next_objective(progress, now=1, mode="review")
    assert out["action"] == "complete"


# ---------------------------------------------------------------------------
# Textbook-mode chapter state machine (v2.7.0)
# ---------------------------------------------------------------------------

def _base_progress(covered=(), chapter=None, flow_phase="learning"):
    """Synthetic progress for chapter tests: two modules, mixed types."""
    progress = {
        "repo": "test/repo",
        "flow_phase": flow_phase,
        "modules": [
            {"id": "m01", "name": "Module One", "order": 1, "knowledge_points": [
                {"id": "kp1", "name": "kp one", "type": "concept"},
                {"id": "kp2", "name": "kp two", "type": "procedure"},
            ]},
            {"id": "m02", "name": "Module Two", "order": 2, "knowledge_points": [
                {"id": "kp3", "name": "kp three", "type": "concept"},
            ]},
        ],
        "mastery_levels": {}, "knowledge_types": {},
        "quiz_attempts": [], "qualitative_mastery": {},
        "repetition_states": {}, "review_queue": [], "error_records": [],
    }
    if covered:
        progress["chapter_covered_modules"] = list(covered)
    if chapter is not None:
        progress["chapter"] = chapter
    return progress


# --- chapter gate (next_objective precedence) ---

def test_chapter_gate_returns_chapter_action():
    """An in-progress chapter drives `next_objective` to keep teaching it."""
    progress = _base_progress(chapter={"module_id": "m01", "status": "teaching",
                                       "section_index": 2, "sections": 5})
    out = next_objective(progress, now=1)
    assert out["action"] == "chapter"
    assert out["module_id"] == "m01"
    assert out["module_name"] == "Module One"
    assert out["chapter_status"] == "teaching"
    assert out["section_index"] == 2
    assert out["sections"] == 5


def test_chapter_gate_reports_due_review_count():
    """The chapter objective carries a signpost of how many reviews are due."""
    progress = _base_progress(chapter={"module_id": "m01", "status": "teaching",
                                       "section_index": 0, "sections": 3})
    progress["review_queue"] = [
        {"id": "r1", "knowledge_point_id": "kp1", "knowledge_type": "concept",
         "due_at": 0, "priority": 3},
        {"id": "r2", "knowledge_point_id": "kp2", "knowledge_type": "procedure",
         "due_at": 10**12, "priority": 4},  # not yet due
    ]
    out = next_objective(progress, now=1)
    assert out["due_review_count"] == 1


def test_chapter_gate_precedes_due_review():
    """An in-progress chapter wins over a due review in auto mode — chapter
    learning is a continuous run; the tutor notes due_review_count at pauses."""
    progress = _base_progress(chapter={"module_id": "m01", "status": "teaching",
                                       "section_index": 0, "sections": 3})
    progress["review_queue"] = [
        {"id": "r1", "knowledge_point_id": "kp1", "knowledge_type": "concept",
         "due_at": 0, "priority": 3},
    ]
    out = next_objective(progress, now=1)
    assert out["action"] == "chapter"


def test_flow_phase_gate_precedes_chapter_gate():
    """The whole-picture-first rule outranks chapter resumption: an unfinished
    overview still gates before an active chapter."""
    progress = _base_progress(flow_phase="overview",
                              chapter={"module_id": "m01", "status": "teaching",
                                       "section_index": 1, "sections": 3})
    out = next_objective(progress, now=1)
    assert out["action"] == "overview"


def test_pending_question_precedes_chapter_gate():
    """A posed question is always graded first, even mid-chapter."""
    progress = _base_progress(chapter={"module_id": "m01", "status": "qna",
                                       "section_index": 0, "sections": 3})
    progress["pending_question"] = {
        "question_id": "q1", "knowledge_point_id": "kp2", "prompt": "...",
    }
    out = next_objective(progress, now=1)
    assert out["action"] == "answer_pending"


def test_review_mode_bypasses_chapter_gate():
    """mode='review' skips the chapter gate: scattered-time review drains due
    reviews even mid-chapter."""
    progress = _base_progress(chapter={"module_id": "m01", "status": "teaching",
                                       "section_index": 2, "sections": 3})
    progress["review_queue"] = [
        {"id": "r1", "knowledge_point_id": "kp1", "knowledge_type": "concept",
         "due_at": 0, "priority": 3},
    ]
    out = next_objective(progress, now=1, mode="review")
    assert out["action"] == "review"
    assert out["knowledge_point_id"] == "kp1"
    # nothing due → review mode completes, does not resume the chapter
    progress["review_queue"] = []
    out = next_objective(progress, now=1, mode="review")
    assert out["action"] == "complete"


# --- covered-module skip ---

def test_covered_module_is_skipped_by_next_objective():
    """A module whose chapter gate passed is skipped by the point scan — the
    cursor advances to the next uncovered module's first point."""
    progress = _base_progress(covered=("m01",))
    out = next_objective(progress, now=1)
    assert out["action"] == "probe"
    assert out["module_id"] == "m02"
    assert out["knowledge_point_id"] == "kp3"


def test_covered_points_still_reviewed_when_due():
    """Covered modules' points keep real repetition states, so their due
    reviews still surface — covered ≠ forgotten."""
    progress = _base_progress(covered=("m01",))
    progress["knowledge_types"] = {"kp1": "concept", "kp2": "procedure"}
    progress["repetition_states"] = {
        "kp1": {"interval_index": 0, "next_review_at": 0},
        "kp2": {"interval_index": 0, "next_review_at": 10**12},
    }
    progress["review_queue"] = [
        {"id": "r1", "knowledge_point_id": "kp1", "knowledge_type": "concept",
         "due_at": 0, "priority": 3},
    ]
    out = next_objective(progress, now=1)
    assert out["action"] == "review"
    assert out["knowledge_point_id"] == "kp1"


# --- chapter_start validation ---

def test_chapter_start_writes_state_and_syncs_module():
    from learning_engine import chapter_start
    progress = _base_progress()
    chapter_start(progress, module_id="m02", sections=4)
    assert progress["chapter"]["module_id"] == "m02"
    assert progress["chapter"]["status"] == "teaching"
    assert progress["chapter"]["section_index"] == 0
    assert progress["chapter"]["sections"] == 4
    assert progress["current_module_id"] == "m02"


def test_chapter_start_rejects_non_learning_flow_phase():
    import pytest
    from learning_engine import chapter_start
    progress = _base_progress(flow_phase="overview")
    with pytest.raises(ValueError):
        chapter_start(progress, module_id="m01", sections=3)


def test_chapter_start_rejects_unknown_module():
    import pytest
    from learning_engine import chapter_start
    progress = _base_progress()
    with pytest.raises(ValueError):
        chapter_start(progress, module_id="nope", sections=3)


def test_chapter_start_rejects_covered_module():
    import pytest
    from learning_engine import chapter_start
    progress = _base_progress(covered=("m01",))
    with pytest.raises(ValueError):
        chapter_start(progress, module_id="m01", sections=3)


def test_chapter_start_rejects_pending_question():
    import pytest
    from learning_engine import chapter_start
    progress = _base_progress()
    progress["pending_question"] = {"question_id": "q1",
                                    "knowledge_point_id": "kp2", "prompt": "..."}
    with pytest.raises(ValueError):
        chapter_start(progress, module_id="m01", sections=3)


# --- chapter_advance ---

def test_chapter_advance_updates_section_and_status():
    from learning_engine import chapter_start, chapter_advance
    progress = _base_progress()
    chapter_start(progress, module_id="m01", sections=5)
    out = chapter_advance(progress, section_index=3, status="qna")
    assert out["section_index"] == 3
    assert out["status"] == "qna"
    assert progress["chapter"]["status"] == "qna"


def test_chapter_advance_clamps_section_to_range():
    from learning_engine import chapter_start, chapter_advance
    progress = _base_progress()
    chapter_start(progress, module_id="m01", sections=3)
    assert chapter_advance(progress, section_index=99)["section_index"] == 3
    assert chapter_advance(progress, section_index=-5)["section_index"] == 0


def test_chapter_advance_rejects_invalid_status():
    import pytest
    from learning_engine import chapter_start, chapter_advance
    progress = _base_progress()
    chapter_start(progress, module_id="m01", sections=3)
    with pytest.raises(ValueError):
        chapter_advance(progress, status="bogus")


# --- chapter_complete: module-level gate ---

def test_chapter_complete_initializes_first_review_for_unverified():
    from learning_engine import chapter_start, chapter_complete
    progress = _base_progress()
    chapter_start(progress, module_id="m01", sections=3)
    chapter_complete(progress, now=1000)
    # kp2 (procedure) was never verified → fresh first-review on its base interval
    state = progress["repetition_states"]["kp2"]
    assert state["interval_index"] == 0
    assert state["consecutive_correct"] == 0
    assert state["difficulty"] == 0.5
    assert state["stability"] == 1.0
    assert state["next_review_at"] == 1000 + 3 * 86400  # procedure base = 3 days


def test_chapter_complete_resets_unmastered_state():
    """A point with repetition state but below mastery is reset to first review
    — a lucky streak must not lengthen its interval."""
    from learning_engine import chapter_start, chapter_complete
    progress = _base_progress()
    progress["mastery_levels"]["kp2"] = 0.5          # below the 0.9 gate
    progress["repetition_states"]["kp2"] = {
        "interval_index": 3, "consecutive_correct": 4, "consecutive_wrong": 0,
        "difficulty": 0.2, "stability": 5.0, "next_review_at": 123,
    }
    chapter_start(progress, module_id="m01", sections=3)
    chapter_complete(progress, now=1000)
    state = progress["repetition_states"]["kp2"]
    assert state["interval_index"] == 0
    assert state["difficulty"] == 0.5
    assert state["stability"] == 1.0
    assert state["next_review_at"] == 1000 + 3 * 86400


def test_chapter_complete_keeps_mastered_state():
    """Engine-verified key nodes keep their real records and review state."""
    from learning_engine import chapter_start, chapter_complete, set_qualitative
    progress = _base_progress()
    chapter_start(progress, module_id="m01", sections=3)
    set_qualitative(progress, kp_id="kp1", kp_type="concept", passed=True)  # verified
    verified_state = progress["repetition_states"]["kp1"]
    chapter_complete(progress, now=1000)
    assert progress["repetition_states"]["kp1"] == verified_state   # untouched
    assert progress["qualitative_mastery"]["kp1"] is True
    # unverified kp2 still got its fresh first-review
    assert progress["repetition_states"]["kp2"]["interval_index"] == 0


def test_chapter_complete_requires_active_chapter():
    import pytest
    from learning_engine import chapter_complete
    progress = _base_progress()
    with pytest.raises(ValueError):
        chapter_complete(progress)


def test_chapter_complete_writes_knowledge_types_and_rebuilds_queue():
    """Pitfall A: without knowledge_types + a queue rebuild, covered points
    would be dropped from review as if they were `memory`."""
    from learning_engine import chapter_start, chapter_complete
    progress = _base_progress()
    chapter_start(progress, module_id="m01", sections=3)
    chapter_complete(progress, now=1000)
    assert progress["knowledge_types"]["kp2"] == "procedure"
    ids = [(q["knowledge_point_id"], q["knowledge_type"]) for q in progress["review_queue"]]
    assert ("kp1", "concept") in ids
    assert ("kp2", "procedure") in ids


def test_chapter_complete_covers_module_and_cursor_advances():
    """After completing a chapter the module is covered, and next_objective
    moves past it (its points are validated later via spaced review)."""
    from learning_engine import chapter_start, chapter_complete
    progress = _base_progress()
    chapter_start(progress, module_id="m01", sections=3)
    result = chapter_complete(progress, now=1000)
    assert progress["chapter_covered_modules"] == ["m01"]
    assert result["covered_modules"] == ["m01"]
    out = next_objective(progress, now=1000)
    assert out["action"] == "probe"
    assert out["module_id"] == "m02"


def test_chapter_complete_memory_points_are_skipped():
    """memory points (reference cheatsheets) never gain review state."""
    from learning_engine import chapter_start, chapter_complete
    progress = _base_progress()
    progress["modules"][0]["knowledge_points"].append(
        {"id": "kp_mem", "type": "memory"})
    chapter_start(progress, module_id="m01", sections=3)
    chapter_complete(progress, now=1000)
    assert "kp_mem" not in progress["repetition_states"]
    assert "kp_mem" not in [q["knowledge_point_id"] for q in progress["review_queue"]]


# --- set_qualitative ---

def test_set_qualitative_writes_mastery_and_schedules_review():
    """Pitfall C fix: a passed concept/design judgment must schedule spaced
    review, not just flip the boolean."""
    from learning_engine import set_qualitative
    progress = _base_progress()
    out = set_qualitative(progress, kp_id="kp1", kp_type="concept", passed=True)
    assert out["passed"] is True
    assert out["is_mastered"] is True
    assert progress["qualitative_mastery"]["kp1"] is True
    assert "kp1" in progress["repetition_states"]
    assert any(q["knowledge_point_id"] == "kp1" for q in progress["review_queue"])


def test_set_qualitative_fail_does_not_schedule_review():
    from learning_engine import set_qualitative
    progress = _base_progress()
    out = set_qualitative(progress, kp_id="kp1", kp_type="concept", passed=False)
    assert out["passed"] is False
    assert out["is_mastered"] is False
    assert progress["qualitative_mastery"]["kp1"] is False
    assert "kp1" not in progress["repetition_states"]


def test_set_qualitative_rejects_non_qualitative_type():
    import pytest
    from learning_engine import set_qualitative
    progress = _base_progress()
    with pytest.raises(ValueError):
        set_qualitative(progress, kp_id="kp2", kp_type="procedure", passed=True)


# --- backward compatibility ---

def test_old_progress_without_chapter_fields_is_backward_compatible():
    """Progress written before v2.7.0 (no chapter / chapter_covered_modules)
    flows exactly as before: no chapter gate, no covered skip."""
    progress = _base_progress()
    out = next_objective(progress, now=1)
    assert out["action"] == "probe"
    assert out["module_id"] == "m01"
    assert out["knowledge_point_id"] == "kp1"

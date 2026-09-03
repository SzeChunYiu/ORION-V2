"""The semantic-evaluator custody disposition must state the real, recomputed scope.

Every number the disposition publishes is derived here from the frozen case
registry and the frozen scoring specification rather than read back from the
disposition file, so a stale or flattering denominator fails the suite instead
of being reported as a clean count.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "research/evaluation"
DISPOSITION_TOKEN = "NOT_OBTAINED__DISCLOSED_LIMITATION"


def _load(name: str) -> dict:
    return json.loads((EVAL / name).read_text(encoding="utf-8"))


def _git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(f"blob {len(payload)}\0".encode() + payload).hexdigest()


def _cells_to_cases() -> dict[str, set[str]]:
    registry = _load("V1_PARITY_CASE_REGISTRY_WAVE06_V1.json")
    cells: dict[str, set[str]] = {}
    for campaign in registry["campaigns"]:
        for case in campaign["cases"]:
            for capability in case["capability_ids"]:
                cells.setdefault(capability, set()).add(case["case_id"])
    return cells


def test_recomputed_unresolved_scope_matches_the_published_denominators() -> None:
    scoring = _load("V1_PARITY_SCORING_ADJUDICATION_WAVE06_V1.json")
    semantic = set(scoring["semantic_case_ids"])
    cells = _cells_to_cases()

    # Every case in the frozen registry is required, and capability_cell_rule makes a
    # cell CANNOT_CHECK when any required case referencing it is unresolved. A cell is
    # therefore unresolved if it touches a semantic case at all, not only if it is
    # reachable exclusively through one.
    unresolved = {cell for cell, cases in cells.items() if cases & semantic}
    only_semantic = {cell for cell, cases in cells.items() if cases <= semantic}

    assert len(cells) == 59
    assert len(only_semantic) == 6
    assert len(unresolved) == 8

    disposition = _load("V1_PARITY_SEMANTIC_EVALUATOR_CUSTODY_DISPOSITION_WAVE06_V1.json")
    scope = disposition["scope_of_the_limitation"]
    assert scope["frozen_capability_cell_total"] == len(cells)
    assert scope["cells_unresolved_under_this_disposition"] == len(unresolved)
    assert scope["cells_scorable_by_the_bound_deterministic_scorer"] == len(cells) - len(unresolved)
    assert set(scope["cells_reachable_only_through_semantic_cases"]["ids"]) == only_semantic
    assert set(scope["semantic_case_ids"]) == semantic

    both = set(scope["cells_referenced_by_both_a_deterministic_and_a_semantic_case"]["ids"])
    assert both == unresolved - only_semantic


def test_registry_and_custody_protocol_agree_with_the_recomputed_scope() -> None:
    scoring = _load("V1_PARITY_SCORING_ADJUDICATION_WAVE06_V1.json")
    semantic = set(scoring["semantic_case_ids"])
    cells = _cells_to_cases()
    unresolved = {cell for cell, cases in cells.items() if cases & semantic}

    registry = _load("V1_PARITY_EVALUATOR_REGISTRY_WAVE06_V1.json")
    custody = _load("V1_PARITY_CUSTODY_PROTOCOL_WAVE06_V1.json")

    for limitation in (
        registry["disclosed_limitation"],
        custody["evaluator_registry"]["disclosed_limitation"],
    ):
        assert set(limitation["unresolved_case_ids"]) == semantic
        assert set(limitation["unresolved_capability_cell_ids"]) == unresolved
        assert limitation["scorable_capability_cell_count"] == len(cells) - len(unresolved)
        assert limitation["frozen_capability_cell_total"] == len(cells)


def test_no_semantic_evaluator_is_recorded_as_bound_or_as_having_passed() -> None:
    registry = _load("V1_PARITY_EVALUATOR_REGISTRY_WAVE06_V1.json")
    assert registry["registry_bound"] is False
    assert registry["paired_outcomes_accessed"] is False
    assert registry["independence_disposition"] == DISPOSITION_TOKEN

    by_id = {row["evaluator_id"]: row for row in registry["evaluators"]}
    for evaluator_id in (
        "PARITY-C-SEMANTIC-REVIEWER-1",
        "PARITY-C-SEMANTIC-REVIEWER-2",
        "PARITY-D-RECONSTRUCTION-REVIEWER-1",
        "PARITY-D-RECONSTRUCTION-REVIEWER-2",
        "PARITY-SEMANTIC-TIEBREAKER",
    ):
        row = by_id[evaluator_id]
        assert row["bound"] is False
        assert row["identity"] == "NOT_OBTAINED"
        assert row["independence_disposition"] == DISPOSITION_TOKEN
        # the token must never be confusable with an evaluator verdict
        assert DISPOSITION_TOKEN not in {"PASS", "FAIL", "CANNOT_CHECK"}

    # the mechanical scorer keeps its own honest ceiling and is not promoted
    scorer = by_id["PARITY-DET-FROZEN-INVARIANT-SCORER-V1"]
    assert scorer["bound"] is True
    assert scorer["authority_ceiling"] == "MECHANICAL_SCORING_ONLY"


def test_the_requirement_itself_is_not_retired_by_the_disposition() -> None:
    case_registry = _load("V1_PARITY_CASE_REGISTRY_WAVE06_V1.json")
    assert case_registry["coverage_assertions"]["protected_independent_evaluator_required"] is True

    for campaign in case_registry["campaigns"]:
        if campaign["campaign_id"] in ("PARITY-C", "PARITY-D"):
            # PARITY-C says "semantic adjudication", PARITY-D says
            # "reconstruction/gluing adjudication"; both must still require it.
            assert "adjudication remains required" in campaign["non_substitution_rule"]
            assert "cannot alone establish V1-native" in campaign["non_substitution_rule"]

    disposition = _load("V1_PARITY_SEMANTIC_EVALUATOR_CUSTODY_DISPOSITION_WAVE06_V1.json")
    assert disposition["requirement_status"]["protected_independent_evaluator_required"] is True
    assert disposition["requirement_status"]["protected_independent_evaluator_obtained"] is False
    assert disposition["authority"]["grants_independent_evaluator_custody"] is False
    assert disposition["authority"]["grants_run_authorization"] is False
    assert disposition["paired_outcomes_accessed"] is False


def test_the_mechanical_follow_on_route_is_named_but_not_bound() -> None:
    disposition = _load("V1_PARITY_SEMANTIC_EVALUATOR_CUSTODY_DISPOSITION_WAVE06_V1.json")
    route = disposition["named_follow_on_not_bound_here"]
    assert route["bound"] is False
    assert route["status"] == "CANDIDATE_ROUTE_ONLY"
    assert route["unmet_preconditions"]
    assert "F3_NON_DUPLICATE_EVALUATOR" in route["would_not_discharge"]


def test_disposition_and_registry_digests_are_rebound() -> None:
    registry_path = EVAL / "V1_PARITY_EVALUATOR_REGISTRY_WAVE06_V1.json"
    disposition_path = EVAL / "V1_PARITY_SEMANTIC_EVALUATOR_CUSTODY_DISPOSITION_WAVE06_V1.json"
    custody = _load("V1_PARITY_CUSTODY_PROTOCOL_WAVE06_V1.json")

    assert custody["evaluator_registry"]["digest"] == f"git-sha1:{_git_blob_sha(registry_path)}"
    assert custody["evaluator_registry"]["disposition_artifact_digest"] == (
        f"git-sha1:{_git_blob_sha(disposition_path)}"
    )
    # the scoring specification is deliberately untouched by this disposition
    assert custody["scoring_registry"]["bound"] is True
    assert custody["scoring_registry"]["digest"] == (
        f"git-sha1:{_git_blob_sha(EVAL / 'V1_PARITY_SCORING_ADJUDICATION_WAVE06_V1.json')}"
    )

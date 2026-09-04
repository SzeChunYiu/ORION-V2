from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LANE = ROOT / "research" / "orion-machine" / "revocation_complete_learning"
MODULE_PATH = LANE / "revocation_complete_oracle.py"


def load_oracle():
    lane_text = str(LANE)
    if lane_text not in sys.path:
        sys.path.insert(0, lane_text)
    spec = importlib.util.spec_from_file_location("revocation_complete_oracle", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ORACLE = load_oracle()


def test_n4_antichains_and_signatures_are_exact() -> None:
    m = ORACLE
    result = m.verify_antichain_injectivity(4)
    assert result["candidate_families_scanned"] == 65536
    assert result["profile_count"] == 168
    assert result["distinct_signature_count"] == 168
    assert result["injective"] is True
    assert result["independent_liveness_agreement"] == result["independent_liveness_denominator"]


def test_current_validity_does_not_determine_future_revision() -> None:
    m = ORACLE
    a = m.canonical_profile([{0}])
    b = m.canonical_profile([{1}])
    assert m.live(a, set()) and m.live(b, set())
    assert m.first_difference(a, b, 2) is not None


def test_every_omitted_positive_warrant_has_a_distinguishing_revocation() -> None:
    m = ORACLE
    result = m.verify_positive_witness_omissions(4)
    assert result["profiles_checked"] == 168
    assert result["proper_positive_transcripts_checked"] == 1253
    assert result["all_omissions_distinguished"] is True


def test_bounded_positive_witnesses_fail_for_k_1_to_8() -> None:
    m = ORACLE
    result = m.verify_bounded_witness_family(8)
    assert result["witness_count"] == 8
    assert result["all_exact"] is True
    assert all(not row["emitted_live"] and row["full_live"] for row in result["cases"])


def test_counterfactual_gap_shatters_nine_revocations_at_n5() -> None:
    m = ORACLE
    result = m.verify_counterfactual_gap(5)
    target = next(row for row in result["cases"] if row["n"] == 5)
    assert target == {
        "n": 5,
        "middle_layer_warrant_count": 10,
        "profile_count": 512,
        "distinct_signature_count": 512,
        "same_current_certificate": True,
        "revocation_shattering_dimension": 9,
        "zero_query_lower_bound_bits": 9,
        "exact": True,
    }


def test_storage_query_frontier_is_exact_at_every_split() -> None:
    m = ORACLE
    result = m.verify_storage_query_frontier(5)
    target = next(row for row in result["cases"] if row["n"] == 5)
    assert len(target["frontier_points"]) == 10
    assert all(point["sum"] == 9 and point["exact"] for point in target["frontier_points"])
    assert target["frontier_points"][0]["stored_bits"] == 0
    assert target["frontier_points"][-1]["queried_binary_coordinates"] == 0


def test_two_skill_direct_sum_has_ten_independent_revision_bits() -> None:
    m = ORACLE
    result = m.verify_direct_sum(n=4, skill_count=2)
    assert result["per_skill_dimension"] == 5
    assert result["joint_dimension"] == 10
    assert result["joint_profile_count"] == 1024
    assert result["exact"] is True


def test_single_warrant_information_and_rank_are_exact() -> None:
    m = ORACLE
    result = m.verify_single_warrant_bounds(8)
    target = next(row for row in result["cases"] if row["n"] == 8 and row["d"] == 4)
    assert target["profile_count"] == 70
    assert target["lower_bound_bits"] == 7
    assert target["rank_count"] == 70
    assert target["round_trip"] is True


def test_canonical_profile_removes_duplicates_and_supersets() -> None:
    m = ORACLE
    assert m.canonical_profile([{0}, {0}, {0, 1}, {2, 3}, {2, 3, 4}]) == (
        frozenset({0}),
        frozenset({2, 3}),
    )


def test_invalid_large_enumeration_refuses() -> None:
    m = ORACLE
    try:
        m.enumerate_antichains(5)
    except ValueError as exc:
        assert "capped at n=4" in str(exc)
    else:
        raise AssertionError("n=5 exhaustive enumeration must refuse")


def test_non_antichain_omission_constructor_refuses() -> None:
    m = ORACLE
    try:
        m.omitted_warrant_revocation((frozenset({0}),), frozenset({0, 1}))
    except ValueError as exc:
        assert "antichain" in str(exc)
    else:
        raise AssertionError("subset-related warrants must refuse")


def test_planted_positive_no_alarm_and_mutation_controls_are_live() -> None:
    m = ORACLE
    controls = m.verify_controls()
    assert controls["planted_positive"]["overretraction_detected"] is True
    assert controls["no_alarm"]["agreement"] is True
    assert controls["mutation_control"] == {"mutated": True, "detected": True}


def test_theorem_ledger_is_acyclic_and_claims_no_external_novelty() -> None:
    ledger = json.loads((LANE / "RCL_THEOREM_LEDGER_V0.json").read_text())
    rows = {row["id"]: row for row in ledger["theorems"]}
    assert len(rows) == len(ledger["theorems"])
    assert all(dep in rows for row in rows.values() for dep in row["dependencies"])
    assert all(row["novelty_claimed"] is False for row in rows.values())
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise AssertionError(f"cycle at {node}")
        if node in visited:
            return
        visiting.add(node)
        for dep in rows[node]["dependencies"]:
            visit(dep)
        visiting.remove(node)
        visited.add(node)

    for theorem_id in rows:
        visit(theorem_id)
    assert visited == set(rows)
    assert ledger["authority"]["external_novelty_established"] is False


def test_receipt_hashes_match_bound_artifacts() -> None:
    receipt = json.loads((LANE / "REVOCATION_COMPLETE_LEARNING_RECEIPT_V0.json").read_text())
    for artifact in receipt["artifacts"]:
        data = (ROOT / artifact["path"]).read_bytes()
        assert len(data) == artifact["bytes"]
        assert hashlib.sha256(data).hexdigest() == artifact["sha256"]
    assert receipt["authority"]["breakthrough_established"] is False
    assert receipt["authority"]["external_novelty_established"] is False


def test_independent_review_packet_is_outcome_blind_and_hash_bound() -> None:
    packet = json.loads((LANE / "RCL_INDEPENDENT_REVIEW_PACKET_V0.json").read_text())
    for artifact in packet["artifacts"]:
        data = (ROOT / artifact["path"]).read_bytes()
        assert len(data) == artifact["bytes"]
        assert hashlib.sha256(data).hexdigest() == artifact["sha256"]
    assert packet["authority"] == {
        "novelty_precommitted": False,
        "review_result_precommitted": False,
        "same_session_counts_as_independent": False,
    }


def test_self_test_passes_without_granting_scientific_authority() -> None:
    result = ORACLE.run_self_test()
    assert result["terminal"] == "PASS"
    assert result["authority"] == {
        "all_size_theorem_proved_by_enumeration": False,
        "novelty_established": False,
        "architecture_superiority_established": False,
    }

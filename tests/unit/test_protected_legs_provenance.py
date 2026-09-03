"""Guards for the protected legs of FM30 and ME-X2-V2.

These studies previously carried terminals that rested on development splits.
The invariants below are the ones that were violated before the protected runs
landed, and they are cheap to check, so they are checked rather than assumed:

* a protected analysis must leave no hard gate unevaluated ("could not check" is
  not "checked and fine");
* an outcome receipt must reveal a seed that hashes to the commitment the frozen
  design published before the run;
* no live authorization file may be committed (the guard must be re-armed);
* a receipt that reports a protected run must say so, and a superseded
  development receipt must not keep claiming no protected outcome exists.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FM = ROOT / "research" / "experiments" / "fm-exact"
MEX2V2 = ROOT / "research" / "experiments" / "me-x2-v2"

FM30_ANALYSIS = FM / "fm30" / "results" / "FM30_PROTECTED_ANALYSIS_V1.json"
MEX2V2_ANALYSIS = MEX2V2 / "results" / "ME_X2_V2_PROTECTED_ANALYSIS_V2.json"


def test_fm30_protected_analysis_leaves_no_hard_gate_unevaluated() -> None:
    a = json.loads(FM30_ANALYSIS.read_text())
    assert a["label"] == "PROTECTED"
    assert a["n_instances"] == 100
    assert a["unchecked_hard_gates"] == [], a["unchecked_hard_gates"]
    gates = {g["gate"]: g for g in a["gates"]}
    # the gate that was CANNOT_CHECK on the development split
    g2 = gates["G2_ANTI_PERMISSIVENESS"]
    assert g2["verdict"] == "PASS"
    assert g2["n_evaluated"] >= g2["min_required_evaluated"] >= 10
    # a zero that carries its own liveness control
    assert g2["detail"]["counter_liveness_control"]["counter_is_live"] is True
    assert g2["detail"]["counter_liveness_control"]["max_any_arm"] > 0
    for g in a["gates"]:
        if g["hard"] and g["applicable"]:
            assert g["verdict"] in ("PASS", "FAIL"), g


def test_fm30_route_is_recorded_with_its_failed_hard_gate_visible() -> None:
    """The route line alone reads cleaner than the run was; the receipt must not."""
    a = json.loads(FM30_ANALYSIS.read_text())
    assert a["route"]["route"] == "PARENT_SUFFICIENT"
    gates = {g["gate"]: g for g in a["gates"]}
    assert gates["G1a_PARENT_REPRODUCES_M"]["verdict"] == "FAIL"
    receipt = (FM / "FM30_OUTCOME_RECEIPT.md").read_text()
    assert "G1a_PARENT_REPRODUCES_M" in receipt
    assert "**FAIL**" in receipt


def test_mex2v2_protected_analysis_measures_the_contrast_the_dev_split_could_not() -> None:
    a = json.loads(MEX2V2_ANALYSIS.read_text())
    assert a["label"] == "PROTECTED"
    assert a["n_instances"] == 1200
    g5 = a["gates"]["G5_LEVER_ATTRIBUTION"]
    # the development split had 0 discordant pairs here: the test could not fire
    assert g5["a_paired_M2_vs_M_V1"]["discordant"] > 0
    # and clause (c) must never pass on an empty denominator
    assert g5["c_n_M2_only_correct"] > 0 or g5["c_pass"] is False
    assert a["gates"]["G0d_V1_PROVENANCE"]["pass"] is True
    assert a["gates"]["G2_ANTI_ESCALATION"]["pass"] is True


def _revealed_seed(receipt: Path) -> str:
    m = re.search(r"`([A-Za-z0-9-]*PROTECTED-[0-9a-f]{32,})`", receipt.read_text())
    assert m, f"{receipt.name} does not reveal a protected seed"
    return m.group(1)


def test_revealed_seeds_hash_to_the_frozen_commitments() -> None:
    fm30_design = json.loads(
        (FM / "FM30_FORMAL_CONCEPT_REVISION_EXACT_STUDY_DESIGN_V1.json").read_text()
    )
    seed = _revealed_seed(FM / "FM30_OUTCOME_RECEIPT.md")
    assert (
        hashlib.sha256(seed.encode()).hexdigest()
        == fm30_design["seed_commitment"]["protected_seed_sha256"]
    )

    v2_design = json.loads(
        (MEX2V2 / "ME_X2_V2_LOOKAHEAD_REACHABILITY_REVIVAL_DESIGN_V2.json").read_text()
    )
    seed = _revealed_seed(MEX2V2 / "ME_X2_V2_OUTCOME_RECEIPT.md")
    assert (
        hashlib.sha256(seed.encode()).hexdigest()
        == v2_design["seed_commitment"]["protected_seed_sha256"]
    )


def test_authorizations_are_archived_and_the_guards_are_re_armed() -> None:
    assert not (FM / "PROTECTED_RUN_AUTHORIZATION.json").exists()
    assert not (MEX2V2 / "PROTECTED_RUN_AUTHORIZATION.json").exists()
    for archived in (
        FM / "PROTECTED_RUN_AUTHORIZATION_ARCHIVED_FM30.json",
        MEX2V2 / "PROTECTED_RUN_AUTHORIZATION_ARCHIVED_V2.json",
    ):
        auth = json.loads(archived.read_text())
        assert auth["human_written"] is True
        assert len(str(auth["human_written_token"])) >= 16
        assert auth["protected_runs_authorized"] == 1
        assert auth["post_outcome_design_change_authorized"] is False
        # the class must be stated, not implied
        assert auth["authorization_class"]


def test_superseded_development_receipts_do_not_deny_a_run_that_exists() -> None:
    for path in (
        FM / "FM_PARENT_FIDELITY_RECEIPT_FM30_V1.md",
        MEX2V2 / "ME_X2_V2_PARENT_FIDELITY_AND_LEVER_RECEIPT_V2.md",
    ):
        text = path.read_text()
        assert "No protected outcome has been generated" in text, (
            "the historical text is preserved, not rewritten"
        )
        assert "SUPERSEDED IN PART" in text, (
            f"{path.name} still reads as though no protected run exists"
        )
        head = text[: text.index("SUPERSEDED IN PART")]
        assert head.count("\n") <= 3, "the banner must precede the stale status line"


def test_fm30_backlog_row_carries_its_terminal_like_fm10_and_fm20() -> None:
    backlog = json.loads(
        (ROOT / "research" / "experiments" / "CONCEPTUAL_TRANSFER_FORMAL_EXECUTION_BACKLOG_V1.json").read_text()
    )
    rows = {t["id"]: t for t in backlog["tasks"] if "id" in t}
    fm30 = rows["FM30"]
    assert fm30["status"] == "EXECUTED_PROTECTED"
    assert fm30["terminal"] == "PARENT_SUFFICIENT"
    assert Path(ROOT / fm30["outcome_receipt"]).exists()
    # the terminal must not be quotable as "the parent reproduces M"
    assert "no advantage" in fm30["terminal_detail"]
    fm80 = rows["FM80"]
    assert fm80["terminal"] == "BLOCKED_ELIGIBILITY_PRECONDITIONS_UNSATISFIED"
    assert "S7" in fm80["single_blocking_artifact"]

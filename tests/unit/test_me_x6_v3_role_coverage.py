"""ME-X6 V3: executable assertions over the frozen artifacts and the generator.

The load-bearing facts of the receipt are asserted here rather than quoted: the
role-coverage premise, the identity of the four held-out strata with the four roles
V2's comparator zeroed, byte-for-byte delegation of V1 strata to V1's generator, the
protected outcome, and the controls that keep the tie from being an identity.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
V3 = ROOT / "research" / "experiments" / "me-x6-v3"
V2 = ROOT / "research" / "experiments" / "me-x6-v2"
V1 = ROOT / "research" / "experiments" / "me-x6"
for p in (V3, V2, V1):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import mex6v3_generator as G  # noqa: E402
import mex6v3_run as R  # noqa: E402
from mex6_generator import generate_split as v1_generate_split  # noqa: E402
from mex6_model import VALIDATION_CHANNELS  # noqa: E402


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def dev():
    return R.dev_split()


def test_the_four_held_out_strata_are_exactly_the_four_roles_v2_zeroed(dev):
    census = R.role_coverage_census(dev)
    assert census["premise_holds"], census
    assert set(census["b8_v2_zeroed_validation_channels"]) == {
        "corrections", "replications_failed", "downstream_reuse", "solution_cost"}
    assert set(G.LONE_CARRIER[s][0] for s in G.HELD_OUT_STRATA) == set(census["b8_v2_zeroed_validation_channels"])
    # the exception is stated, not hidden: retractions has no lone V1 carrier and was kept
    assert set(census["channels_with_no_lone_carrier_v1_stratum"]) - set(census["b8_v2_zeroed_validation_channels"]) == {"retractions"}


def test_each_new_stratum_moves_exactly_one_validation_channel(dev):
    for inst in dev:
        if inst.stratum in G.NEW_STRATA:
            movers = G.validation_movers(inst.window)
            assert movers == (G.LONE_CARRIER[inst.stratum][0],), (inst.stratum, movers)
            assert G.channel_signature_agrees(inst.window, inst.stratum)[0]


def test_v3_delegates_v1_strata_to_v1_generator_byte_for_byte(dev):
    v1 = v1_generate_split("dev", R.DEV_SEED, R.DEV_PER_CELL)
    v3 = [i for i in dev if i.stratum in G.V1_STRATA]
    assert len(v1) == len(v3) == 56
    assert all(a.window == b.window and a.instance_id == b.instance_id for a, b in zip(v1, v3))


def test_no_rng_draw_is_ordered_by_an_unordered_container():
    src = (V3 / "mex6v3_generator.py").read_text()
    assert "for c in CHANNELS" in src and "for c in LATENT_COORDS" in src
    assert "in set(" not in src and "in {" not in src.replace("in {RISE", "")


def test_frozen_design_is_pinned_and_the_seed_hashes_to_its_commitment():
    design = json.loads((V3 / "ME_X6_V3_ROLE_COVERAGE_SHIFT_DESIGN_V1.json").read_text())
    used = json.loads((V3 / "PROTECTED_RUN_AUTHORIZATION_USED_V1.json").read_text())
    assert used["acknowledged_design_sha256"] == _sha(V3 / "ME_X6_V3_ROLE_COVERAGE_SHIFT_DESIGN_V1.json")
    commit = design["seed_commitment"]["protected_seed_sha256"]
    assert hashlib.sha256(used["revealed_protected_seed"].encode()).hexdigest() == commit
    assert used["consumed"] is True
    assert not (V3 / "PROTECTED_RUN_AUTHORIZATION.json").exists(), "the guard must be re-armed"
    for rel, want in R.SUBSTRATE_PINS.items():
        assert _sha(ROOT / "research" / "experiments" / rel) == want, rel


def test_protected_outcome_as_receipted():
    a = json.loads((V3 / "results" / "ME_X6_V3_PROTECTED_ANALYSIS_V1.json").read_text())
    assert a["n_instances"] == 1800
    g = a["gates"]
    assert g["ROUTE"]["terminal"] == "TYPING_IS_A_COVERAGE_PRIOR"
    assert g["ROUTE"]["route"] == "PARENT_SUFFICIENT_AT_FULL_COVERAGE"
    assert all(g[k]["pass"] for k in R.HARD_GATES), {k: g[k]["pass"] for k in R.HARD_GATES}
    assert g["G2_M_VS_B8_V3_REFIT_ON_ALL_18"]["comparison"]["overall"] == "TIE"
    assert g["G1_M_VS_B8_V2_FROZEN_ON_HELD_OUT_4"]["comparison"]["overall"] == "X_AHEAD"
    per = a["score"]["per_arm"]
    assert per[R.M_ARM]["capability_correct"] == 1800
    assert per[R.REFIT_ARM]["capability_correct"] == 1800
    assert per[R.B8_V2_ARM]["capability_correct"] == 1400
    assert per[R.UNIT_ARM]["capability_correct"] == 1000
    assert g["COVERAGE_LEDGER"]["all_registered_cells_exercised"] and g["SCOPE_BINDING"]["equal"]
    # the null bar is derived, and the best constant arm sits exactly on it
    bar = g["G0c_NULL_CALIBRATION"]
    assert abs(bar["derivable_bar_modal_class_rate"] - 8 / 18) < 1e-12
    assert abs(bar["best_control_rate"] - 8 / 18) < 1e-12


def test_the_refit_vector_is_not_m_and_the_tie_is_not_an_identity():
    fit = json.loads((V3 / "results" / "ME_X6_V3_DEVELOPMENT_FIT_V1.json").read_text())
    m = R.m_vector()
    refit = fit[R.REFIT_ARM]["weights"]
    assert fit[R.REFIT_ARM]["selected_fitter"] == "B7_L1_PATH_UNTYPED"
    # a real-valued path vector, non-zero on eight channels, with a non-M channel (disruption) live
    live = {c for c, w in refit.items() if w}
    assert "disruption" in live and m["disruption"] == 0
    assert {c: (1 if w > 0 else -1) for c, w in refit.items() if w} != {c: (1 if w > 0 else -1) for c, w in m.items() if w}
    # the greedy fitter (integer class) fell short: the class contains failing members
    assert fit[R.GREEDY_V3_ARM]["dev_capability_correct"] < fit["n_dev"]
    # the exhaustive check is disclosed as an identity, never a comparator
    assert fit[R.B9_ARM]["m_vector_is_maximal"]


def test_g1_and_g3_are_by_construction_and_disclosed_as_such():
    """B8_V2 zeroes the four roles, so it reads FLAT on every held-out instance whose
    planted capability is RISE or FALL.  Those two gates are coverage disclosures, not
    evidence about typing; the live question is G2."""
    design = json.loads((V3 / "ME_X6_V3_ROLE_COVERAGE_SHIFT_DESIGN_V1.json").read_text())
    text = json.dumps(design)
    assert "BY_CONSTRUCTION" in text or "by construction" in text
    assert all(G.NEW_STRATA[s][0] in ("RISE", "FALL") for s in G.HELD_OUT_STRATA)


def test_validation_channels_cover_all_eight_declared_roles():
    assert set(G.ROLE_LONE_CARRIER_STRATUM) == set(VALIDATION_CHANNELS)

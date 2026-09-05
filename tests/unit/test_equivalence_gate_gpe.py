"""GPE: present equivalence screened per family on dev, before the seed is sealed.

Design V2 gated present equivalence on the canonical fixture alone, so a model whose two
representations are not behaviourally equivalent was discovered at protected time after the
single draw was spent (limitation V-M1). GPE is the admission screen; these tests pin that it
can actually refuse, that one bad family is enough, and that it never touches the terminal.
"""
import importlib.util
import sys
import copy
import json
from pathlib import Path

import pytest

_SRC = Path(__file__).resolve().parents[2] / "research/llm-machine-epistemics/pra_real_llm_audit.py"
_spec = importlib.util.spec_from_file_location("pra_gpe_test", _SRC)
_mod = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _mod
_spec.loader.exec_module(_mod)

DESIGN = {"gates": {"GPE": {"epsilon_pred_per_instance_nats_per_token": 0.15,
                            "epsilon_pred_mean_nats_per_token": 0.05,
                            "min_pass_fraction": 0.9}},
          "token_budget": {"tolerance_tokens": 8},
          "suite_generator": {"instances_per_family": {"dev": {"F1": 20, "F2": 20}},
                              "arms_per_instance": 1}}


def _design(**families):
    design = copy.deepcopy(DESIGN)
    design["suite_generator"]["instances_per_family"]["dev"] = families
    return design


def _rec(iid, fam, cond, lp, action="a", correct=True, tokens=100):
    return {"instance_id": iid, "arm_id": "arm0", "family": fam, "condition": cond,
            "status_line_mean_logprob": lp, "current_action": action,
            "current_correct": correct, "tokens_padded": tokens}


def _family(fam, n, delta=0.0, action_r3="a"):
    out = []
    for i in range(n):
        out += [_rec(f"{fam}-{i}", fam, "R0", -1.0),
                _rec(f"{fam}-{i}", fam, "R2", -1.0),
                _rec(f"{fam}-{i}", fam, "R3", -1.0 + delta, action=action_r3)]
    return out


def test_equivalent_families_admit_the_model():
    r = _mod.equivalence_gate(DESIGN, _family("F1", 20) + _family("F2", 20))
    assert r["admitted"] is True and r["verdict"] == "GPE_PASS__MODEL_ADMITTED"
    assert r["families_failed"] == []


def test_one_failing_family_is_enough_to_refuse():
    """The whole point of per-family: V2 passed on the canonical fixture and failed at protected time."""
    recs = _family("F1", 20) + _family("F2", 20, delta=0.9)   # far outside epsilon
    r = _mod.equivalence_gate(DESIGN, recs)
    assert r["admitted"] is False
    assert r["verdict"] == "GPE_FAIL__MODEL_NOT_ADMITTED"
    assert r["families_failed"] == ["F2"]


def test_a_differing_present_action_fails_even_when_logprobs_match():
    """Mistral's actual failure mode: present behaviour differs across representations."""
    r = _mod.equivalence_gate(_design(F1=20), _family("F1", 20, action_r3="b"))
    assert r["admitted"] is False and r["families_failed"] == ["F1"]


def test_token_budget_violation_fails():
    recs = _family("F1", 20)
    for rec in recs:
        if rec["condition"] == "R3":
            rec["tokens_padded"] = 200
    assert _mod.equivalence_gate(_design(F1=20), recs)["admitted"] is False


def test_no_triples_is_cannot_check_not_a_pass():
    r = _mod.equivalence_gate(DESIGN, [_rec("x", "F1", "R2", -1.0)])
    assert r["admitted"] is None
    assert r["verdict"] == "CANNOT_CHECK__NO_FAMILY_HAD_TRIPLES"


def test_missing_gpe_in_design_is_refused_not_defaulted():
    with pytest.raises(SystemExit):
        _mod.equivalence_gate({"gates": {}, "token_budget": {"tolerance_tokens": 8}}, _family("F1", 5))


def test_screen_is_administrative_only():
    r = _mod.equivalence_gate(_design(F1=20), _family("F1", 20))
    assert "terminal" not in r and "GP0" not in r
    assert "never enters GP0-GP3" in r["note"]


def test_passing_family_does_not_hide_an_unchecked_family():
    recs = _family("F1", 20) + [_rec("F2-0", "F2", "R2", -1.0)]
    r = _mod.equivalence_gate(DESIGN, recs)
    assert r["admitted"] is None and r["families_unchecked"] == ["F2"]


def test_omitted_registered_family_cannot_admit():
    r = _mod.equivalence_gate(DESIGN, _family("F1", 20))
    assert r["admitted"] is None and r["families_unchecked"] == ["F2"]


@pytest.mark.parametrize("missing", ["R0", "R2", "R3", "ALL"])
def test_partial_triples_do_not_shrink_registered_denominator(missing):
    recs = [r for r in _family("F1", 20)
            if not (r["instance_id"] == "F1-19"
                    and (missing == "ALL" or r["condition"] == missing))]
    r = _mod.equivalence_gate(_design(F1=20), recs)
    assert r["admitted"] is None
    assert r["per_family"]["F1"]["expected_units"] == 20
    assert "per_unit_pass_fraction" not in r["per_family"]["F1"]


def test_insufficient_tost_is_not_equivalence():
    # Inside the per-instance margin but outside the mean margin; n=2 is
    # undetermined by paired_tost, never permission to waive the mean test.
    r = _mod.equivalence_gate(_design(F1=2), _family("F1", 2, delta=0.10))
    assert r["admitted"] is None
    assert r["per_family"]["F1"]["tost_R3_minus_R2"]["equivalent"] is None


@pytest.mark.parametrize("bad, admitted", [(2, True), (3, False)])
def test_registered_ninety_percent_boundary_is_preserved(bad, admitted):
    recs = _family("F1", 20)
    for rec in recs:
        if rec["condition"] == "R3" and int(rec["instance_id"].split("-")[-1]) < bad:
            rec["current_action"] = "b"
    r = _mod.equivalence_gate(_design(F1=20), recs)
    assert r["admitted"] is admitted
    assert r["per_family"]["F1"]["per_unit_pass_fraction"] == (20 - bad) / 20


def test_missing_registered_arm_is_not_hidden_by_extra_units_on_another_instance():
    design = _design(F1=2)
    design["suite_generator"]["arms_per_instance"] = 2
    recs = _family("F1", 2)
    # Four triples in total, but one instance has three arms and the other one.
    for arm in ("arm1", "arm2"):
        recs += [{**rec, "arm_id": arm} for rec in _family("F1", 1)]
    assert _mod.equivalence_gate(design, recs)["admitted"] is None


def test_duplicate_triples_are_not_silently_overwritten():
    recs = _family("F1", 20)
    assert _mod.equivalence_gate(_design(F1=20), recs + [dict(recs[0])])["admitted"] is None


def test_missing_dev_coverage_contract_is_refused():
    design = copy.deepcopy(DESIGN)
    del design["suite_generator"]
    with pytest.raises(SystemExit):
        _mod.equivalence_gate(design, _family("F1", 20))


@pytest.mark.parametrize("omit_family", [False, True])
def test_registered_v4_dev_family_and_arm_contract(omit_family):
    # Project only the registered admission and dev-count fields. All records
    # below are synthetic; no model, seed, protected records or stages are used.
    raw = json.loads((_SRC.parent / "PRA_REAL_LLM_AUDIT_DESIGN_V4.json").read_text())
    counts = raw["suite_generator"]["instances_per_family"]["dev"]
    arms = raw["suite_generator"]["arms_per_instance"]
    design = {"gates": {"GPE": raw["gates"]["GPE"]},
              "token_budget": raw["token_budget"],
              "suite_generator": {"instances_per_family": {"dev": counts},
                                  "arms_per_instance": arms}}
    omitted = sorted(counts)[-1] if omit_family else None
    records = [{**r, "arm_id": f"arm{arm}"}
               for fam, n in counts.items() if fam != omitted
               for arm in range(arms) for r in _family(fam, n)]
    result = _mod.equivalence_gate(design, records)
    assert result["admitted"] is (None if omit_family else True)
    assert set(result["per_family"]) == set(counts)
    assert all(result["per_family"][fam]["expected_units"] == n * arms
               for fam, n in counts.items())

"""GPE: present equivalence screened per family on dev, before the seed is sealed.

Design V2 gated present equivalence on the canonical fixture alone, so a model whose two
representations are not behaviourally equivalent was discovered at protected time after the
single draw was spent (limitation V-M1). GPE is the admission screen; these tests pin that it
can actually refuse, that one bad family is enough, and that it never touches the terminal.
"""
import importlib.util
import sys
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
          "token_budget": {"tolerance_tokens": 8}}


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
    r = _mod.equivalence_gate(DESIGN, _family("F1", 20, action_r3="b"))
    assert r["admitted"] is False and r["families_failed"] == ["F1"]


def test_token_budget_violation_fails():
    recs = _family("F1", 20)
    for rec in recs:
        if rec["condition"] == "R3":
            rec["tokens_padded"] = 200
    assert _mod.equivalence_gate(DESIGN, recs)["admitted"] is False


def test_no_triples_is_cannot_check_not_a_pass():
    r = _mod.equivalence_gate(DESIGN, [_rec("x", "F1", "R2", -1.0)])
    assert r["admitted"] is None
    assert r["verdict"] == "CANNOT_CHECK__NO_FAMILY_HAD_TRIPLES"


def test_missing_gpe_in_design_is_refused_not_defaulted():
    with pytest.raises(SystemExit):
        _mod.equivalence_gate({"gates": {}, "token_budget": {"tolerance_tokens": 8}}, _family("F1", 5))


def test_screen_is_administrative_only():
    r = _mod.equivalence_gate(DESIGN, _family("F1", 20))
    assert "terminal" not in r and "GP0" not in r
    assert "never enters GP0-GP3" in r["note"]

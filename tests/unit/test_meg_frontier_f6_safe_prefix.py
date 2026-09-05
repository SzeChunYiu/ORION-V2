from __future__ import annotations

from dataclasses import replace
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "research/machine-epistemics-theory/meg_frontier_f6_safe_prefix_exact.py"
spec = importlib.util.spec_from_file_location("meg_frontier_f6_safe_prefix_exact", MOD)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


@pytest.mark.parametrize("kind", ["garden_path", "late_negation", "quantifier_reversal", "citation_replacement", "correction", "hedge"])
def test_existing_acceptable_completion_does_not_justify_irreversible_prefix(kind):
    inventory, original, changed = m.paired_fixture(kind)
    state = m.PrefixState(m.inventory_digest(inventory))
    live, auth = {original:m.LIVE, changed:m.LIVE}, frozenset({original,changed})
    # Independent existential parent accepts one final meaning, but the other
    # registered continuation changes an already-expressed semantic coordinate.
    assert any(original in c.meaning for c in inventory.completions)
    result = m.safe_prefix(inventory,state,("claim",),live,auth)
    assert result.status == "UNSAFE_SEMANTIC_VARIATION"
    assert result.state == state
    assert original not in result.invariant_meaning


def test_whole_chunk_cannot_skip_the_unsafe_intermediate_prefix():
    inventory, original, changed = m.paired_fixture("late_negation")
    state = m.PrefixState(m.inventory_digest(inventory))
    result = m.safe_prefix(inventory,state,("claim","keep"),{original:m.LIVE,changed:m.LIVE},frozenset({original,changed}))
    assert result.status == "UNSAFE_SEMANTIC_VARIATION"
    assert result.state == state


def test_finite_intersection_criterion_matches_independent_universal_oracle():
    a,b = m.Claim("a"),m.Claim("b")
    subsets = (frozenset(),frozenset({a}),frozenset({b}),frozenset({a,b}))
    live = {a:m.LIVE,b:m.LIVE}
    for left,right,emitted in itertools.product(subsets,repeat=3):
        inventory = m.Inventory(
            (m.Completion("left",("p","l"),left),m.Completion("right",("p","r"),right)),
            (((),frozenset()),(("p",),emitted),(("p","l"),left),(("p","r"),right)),
            "epoch","typed-v1",True)
        state = m.PrefixState(m.inventory_digest(inventory))
        for authorized in subsets:
            result = m.safe_prefix(inventory,state,("p",),live,authorized)
            oracle = all(claim in left and claim in right and claim in authorized for claim in emitted)
            assert (result.status == "SAFE_PREFIX") == oracle


def test_missing_or_open_inventory_never_becomes_proof_of_safety():
    inventory,claim,_ = m.paired_fixture("no_alarm")
    state = m.PrefixState(m.inventory_digest(inventory))
    live,auth = {claim:m.LIVE},frozenset({claim})
    opened = replace(inventory,closed=False)
    assert m.safe_prefix(opened,m.PrefixState(m.inventory_digest(opened)),("claim",),live,auth).status == "CANNOT_CHECK"
    assert m.safe_prefix(inventory,state,("claim",),live,auth,max_completions=1).status == "CANNOT_CHECK"
    # A removed completion is a different frozen inventory, even if its name is unchanged.
    truncated = replace(inventory,completions=inventory.completions[:1],prefix_meanings=inventory.prefix_meanings[:-1])
    assert m.safe_prefix(truncated,state,("claim",),live,auth).status == "CANNOT_CHECK"
    assert m.safe_prefix(replace(inventory,epoch="new-epoch"),state,("claim",),live,auth).status == "CANNOT_CHECK"
    assert m.safe_prefix(replace(inventory,semantics_id="new-parser"),state,("claim",),live,auth).status == "CANNOT_CHECK"


def test_prefix_interpretation_cannot_be_omitted_or_replaced_without_identity_change():
    inventory,claim,_ = m.paired_fixture("no_alarm")
    state = m.PrefixState(m.inventory_digest(inventory))
    incomplete = replace(inventory,prefix_meanings=inventory.prefix_meanings[1:])
    assert m.safe_prefix(incomplete,state,("claim",),{claim:m.LIVE},frozenset({claim})).status == "CANNOT_CHECK"
    forged = replace(inventory,prefix_meanings=(((),frozenset()),(("claim",),frozenset())) + inventory.prefix_meanings[2:])
    assert m.safe_prefix(forged,state,("claim",),{claim:m.LIVE},frozenset({claim})).status == "CANNOT_CHECK"


def test_non_digest_with_custom_equality_cannot_bypass_inventory_binding():
    class NotADigest:
        def __eq__(self, other):
            return True
        def __ne__(self, other):
            return False
    inventory,claim,_ = m.paired_fixture("no_alarm")
    state = m.PrefixState(NotADigest())
    assert m.safe_prefix(inventory,state,("claim",),{claim:m.LIVE},frozenset({claim})).status == "CANNOT_CHECK"


@pytest.mark.parametrize("status", [m.DEAD,m.UNKNOWN])
def test_liveness_and_authority_are_independent_of_semantic_stability(status):
    inventory,claim,_ = m.paired_fixture("no_alarm")
    state = m.PrefixState(m.inventory_digest(inventory))
    assert m.safe_prefix(inventory,state,("claim",),{claim:status},frozenset({claim})).status == "UNSAFE_WARRANT"
    assert m.safe_prefix(inventory,state,("claim",),{claim:m.LIVE},frozenset()).status == "UNSAFE_AUTHORITY"
    assert m.safe_prefix(inventory,state,("claim",),{},frozenset({claim})).status == "CANNOT_CHECK"


def test_revocation_after_emission_requires_reopening_and_preserves_past_commitment():
    inventory,claim,_ = m.paired_fixture("no_alarm")
    start = m.PrefixState(m.inventory_digest(inventory))
    committed = m.safe_prefix(inventory,start,("claim",),{claim:m.LIVE},frozenset({claim})).state
    result = m.safe_prefix(inventory,committed,("keep",),{claim:m.DEAD},frozenset({claim}))
    assert result.status == "UNSAFE_WARRANT"
    assert result.state == committed and result.state.committed == {claim}
    forged = replace(committed,committed=frozenset())
    assert m.safe_prefix(inventory,forged,("keep",),{claim:m.LIVE},frozenset({claim})).status == "CANNOT_CHECK"


def test_late_correction_cannot_erase_an_already_emitted_assertion():
    inventory,claim,other = m.paired_fixture("correction")
    prior = m.PrefixState(m.inventory_digest(inventory),("claim",),frozenset({claim}))
    result = m.safe_prefix(inventory,prior,("revise",),{claim:m.LIVE,other:m.LIVE},frozenset({claim,other}))
    assert result.status == "HISTORY_CONFLICT"
    assert result.state == prior


def test_resume_cannot_launder_an_unsafe_intermediate_prefix():
    inventory,claim,other = m.paired_fixture("late_negation")
    # Endpoint-only validation would accept: its one remaining completion
    # contains claim. The earlier observed 'claim' prefix was still unsafe.
    prior = m.PrefixState(m.inventory_digest(inventory),("claim","keep"),frozenset({claim}))
    result = m.safe_prefix(inventory,prior,(),{claim:m.LIVE,other:m.LIVE},frozenset({claim,other}))
    assert result.status == "HISTORY_CONFLICT"


def test_warranted_hedge_and_abstention_are_available_without_assertion():
    hedge = m.Claim("evidence leaves benefit possible",modality="POSSIBLE")
    inventory = m.Inventory(
        (m.Completion("hedge",("maybe",),frozenset({hedge})),m.Completion("abstain",("withhold",),frozenset())),
        (((),frozenset()),(("maybe",),frozenset({hedge})),(("withhold",),frozenset())),
        "epoch","typed-v1",True)
    start = m.PrefixState(m.inventory_digest(inventory))
    result = m.safe_prefix(inventory,start,("withhold",),{},frozenset())
    assert result.status == "SAFE_PREFIX" and not result.state.committed
    result = m.safe_prefix(inventory,start,("maybe",),{hedge:m.LIVE},frozenset({hedge}))
    assert result.status == "SAFE_PREFIX" and result.state.committed == {hedge}


def test_empty_registered_language_is_not_vacuous_permission():
    inventory = m.Inventory((),(((),frozenset()),),"epoch","typed-v1",True)
    start = m.PrefixState(m.inventory_digest(inventory))
    assert m.safe_prefix(inventory,start,(),{},frozenset()).status == "NO_ADMISSIBLE_COMPLETION"


def test_cli_exit_codes_are_distinct(monkeypatch,capsys):
    process = subprocess.run([sys.executable,str(MOD)],capture_output=True,text=True)
    assert process.returncode == 0
    assert json.loads(process.stdout)["result"]["terminal"] == "SAFE_PREFIX_CRITERION"
    process = subprocess.run([sys.executable,"-O",str(MOD)],capture_output=True,text=True)
    assert process.returncode == 2
    def fail():
        raise AssertionError("planted unsafe prefix")
    monkeypatch.setattr(m,"check_meg27",fail)
    assert m.main() == 1
    assert json.loads(capsys.readouterr().out)["status"] == "FAIL"
    def cannot():
        raise m.CannotCheck("no closed semantics")
    monkeypatch.setattr(m,"check_meg27",cannot)
    assert m.main() == 2
    assert json.loads(capsys.readouterr().out)["status"] == "CANNOT_CHECK"

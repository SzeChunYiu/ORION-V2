"""KnowledgeSpace.v1 M1 — population from ME-X1 worlds and the M0 invariants on the machine.

Runs the public development split at one instance per family (10 worlds, seeded, deterministic).
The counts below are the receipt's own denominators; a change in the generator or the population
map changes them and must be re-pinned deliberately.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "research" / "orion-machine" / "reference" / "kso_m1_mex1_population_v1.py"


def _load():
    spec = importlib.util.spec_from_file_location("kso_m1_mex1_population_v1", MODULE)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def mod():
    return _load()


@pytest.fixture(scope="module")
def receipt(mod):
    return mod.run(per_family=1)


def test_population_totals_pinned(receipt):
    t = receipt["totals"]
    assert t["worlds"] == 10
    assert t["atoms"] == 748 and t["hyperedges"] == 351
    assert t["p2_cells"] == 126 and t["v1_p2_cells"] == 126
    assert t["p3_revocations"] == 80
    assert t["events_replayed"] == 10 and t["events_acquisition_needed"] == 0
    assert t["v1_revoked_base_atoms"] == 3 and t["v1_worlds_with_revocation_or_censoring"] == 2


def test_every_world_is_dense_and_label_equals_oracle(receipt):
    for w in receipt["worlds"]:
        assert w["P1_dense"]["isolated"] == 0 and w["P1_dense"]["quarantined"] == 0
        assert w["P1_dense"]["planted_isolated_rejected"] == 1
        assert w["P2_label_equals_oracle"]["mismatches"] == 0
        assert w["P2_label_equals_oracle"]["planted_merged_family_label_caught"] == "CAUGHT"
        assert w["v1"]["P2_label_equals_oracle"]["mismatches"] == 0


def test_retraction_both_directions_on_real_worlds(receipt):
    raised = 0
    for w in receipt["worlds"]:
        p = w["P3_retraction"]
        assert p["revocations_checked"] == 8
        assert p["dead_atoms_zero"] == p["unreachable_atoms_unchanged"] == p["reachable_atoms_never_gain"] == p["reinstatement_restores"] == 8
        raised += p["renormalising_parent_raised_unreachable_atom"]
        assert w["P3_events"]["status"] == "REPLAYED" and w["P3_events"]["claim_cells_disagree"] == 0
    assert raised >= 1


def test_hub_normalisation_both_directions(receipt):
    for w in receipt["worlds"]:
        assert w["P4_hub"]["background_zero_everywhere"] == 1
        assert w["P4_hub"]["hub_seeded_hub_positive_and_top"] == 1


def test_genome_holds_and_is_unchanged_by_population(receipt, mod):
    for w in receipt["worlds"]:
        g = w["P5_genome"]
        assert g["S1"] and g["S2"] and g["S3_sampled"] and g["S4_identity_measurable"] and g["S4_merged_pair_not_measurable"]
        assert g["S5_policy_swap_invariant"] and g["S6_labels_canonical"] and g["S7_metered"] and g["genome_digest_unchanged"]
    assert receipt["genome_digest"] == mod.m0.genome_digest()


def test_protected_split_is_refused_as_cannot_check(mod):
    with pytest.raises(mod.CannotCheck):
        mod.run(split="protected", per_family=1)
    with pytest.raises(mod.CannotCheck):
        mod.run(per_family=6)


def test_gated_seed_gives_dead_atom_zero_activation(mod):
    ks = mod.KnowledgeSpace(
        (mod.Atom("a", "claim", (frozenset({0}),)), mod.Atom("b", "claim", mod.ONE)),
        (mod.Hyperedge("ab", ("a",), ("b",), "SUPPORT", profile=mod.ONE),),
    )
    a = mod.activation(ks, mod.uniform(ks), Fraction(1, 2), revoked={0})
    assert a["a"] == 0 and a["b"] == Fraction(1, 4)
    a0 = mod.activation(ks, mod.uniform(ks), Fraction(1, 2))
    assert a0["b"] == Fraction(1, 4) + Fraction(1, 2) * Fraction(1, 4)


def test_bindings_cover_generator_oracle_and_checkers(receipt):
    assert set(receipt["bindings"]) == {"mex1_generator.py", "mex1_oracle.py", "mex1_model.py", "kso_math_v1.py", "kso_m0_freeze_checks_v1.py", "kso_m1_mex1_population_v1.py"}
    assert all(len(v) == 64 for v in receipt["bindings"].values())

"""Cross-study known-answer conformance and custody; no empirical outcomes."""
from __future__ import annotations

import copy
from fractions import Fraction as Q
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "research/machine-epistemics-theory"


def load(name, path):
    spec = importlib.util.spec_from_file_location("foundation_integration_" + name, HERE / path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def models():
    return (
        load("revision", "foundation_revision_v1/foundation.py"),
        load("typed", "foundation_typed_lifecycle_v1/calculus.py"),
        load("batch2", "meg_foundation_batch2_exact.py"),
    )


def as_sets(profile):
    return tuple(frozenset(i for i in range(3) if mask & (1 << i)) for mask in profile)


def as_masks(profile):
    return tuple(sorted(sum(1 << i for i in support) for support in profile))


def test_three_native_warrant_models_agree_under_explicit_polarity_map(models):
    revision, typed, batch = models
    ps = revision.profiles(3)
    assert ps == typed.profiles(3)
    compared = 0
    for lower, upper in product(ps, repeat=2):
        if not revision.leq(lower, upper):
            continue
        for revoked in range(8):
            expected = ("DEAD", "UNKNOWN", "LIVE")[revision.Interval(lower, upper).status(revoked)]
            available = 7 ^ revoked
            assert typed.Interval(lower, upper).verdict(available).value == expected
            revoked_set = {i for i in range(3) if revoked & (1 << i)}
            assert batch.liveness((as_sets(lower), as_sets(upper)), revoked_set) == expected
            compared += 1
    assert compared == 1344
    # A missing polarity conversion is a real defect, not a compatible API.
    assert typed.Interval((1,), (1,)).verdict(0).value != ("DEAD", "UNKNOWN", "LIVE")[revision.Interval((1,), (1,)).status(0)]


def test_three_native_nogood_products_preserve_joint_consistency(models):
    revision, typed, batch = models
    compared = 0
    for p, q in product(revision.profiles(3), repeat=2):
        for ng in ((1,), (2,), (3,), (5,), (7,)):
            expected = revision.ng_meet(p, q, ng)
            assert typed.joint(p, q, ng) == expected
            actual = batch.Nogoods(as_sets(ng)).filter(batch.meet(as_sets(p), as_sets(q)))
            assert as_masks(actual) == expected
            compared += 1
    assert compared == 2000
    assert revision.ng_meet((1,), (2,), (3,)) == ()
    assert revision.meet(revision.filter_ng((1,), (3,)), revision.filter_ng((2,), (3,))) != ()


def test_exact_fixed_points_agree_without_changing_normalization(models):
    revision, typed, _ = models
    count = 0
    for a, b, c, d in product((Q(0), Q(1, 2), Q(1)), repeat=4):
        if a + b > 1 or c + d > 1:
            continue
        matrix = ((a, b), (c, d))
        for restart in (Q(1, 4), Q(1, 2), Q(1)):
            for seed in ((Q(1), Q(0)), (Q(0), Q(1)), (Q(1, 2), Q(1, 2))):
                assert revision.fixed(matrix, seed, restart) == typed.fixed_point(matrix, seed, restart)
                count += 1
    assert count == 324


def test_transport_models_share_tv_but_keep_empty_event_distinction():
    causal = load("causal", "causal_transport_v1/causal_core.py")
    transport = load("transport", "certificate_transport_v1/transport.py")
    typed = load("typed_risk", "foundation_typed_lifecycle_v1/calculus.py")
    laws = [(Q(i, 4), Q(j, 4), Q(4-i-j, 4)) for i in range(5) for j in range(5-i)]
    for p, q in product(laws, repeat=2):
        assert causal.total_variation(p, q) == transport.tv(p, q)
    for p, event, drift in product(laws, range(8), (Q(0), Q(1, 4), Q(1))):
        bound = transport.fixed_event(p, event, drift)
        generic = typed.drift_bound(transport.mass(p, event), drift)
        assert bound.risk <= generic
        assert transport.tv(p, bound.attaining_distribution) <= drift
        assert transport.mass(bound.attaining_distribution, event) == bound.risk
        if event:
            assert bound.risk == generic
        else:
            assert bound.risk == 0


def test_custody_and_registry_authority_have_no_implicit_promotion():
    checker = load("custody", "foundation_integration_v1/check_integration.py")
    manifest = json.loads((HERE / "foundation_integration_v1/MANIFEST.json").read_text())
    result = checker.verify(manifest)
    assert result == {"source_prs": 10, "source_files": 130, "relocated_files": 24,
                      "adapted_callers": 2, "historical_receipt_bindings": 7}
    for key, value in (("canonical_registry", checker.SUPPORTING),
                       ("scientific_completion", True), ("ocm_adoption_authorized", True),
                       ("independent_external_review", "COMPLETE")):
        mutant = copy.deepcopy(manifest)
        mutant[key] = value
        with pytest.raises(ValueError):
            checker.verify(mutant)


def test_custody_rejects_missing_sources_drift_and_escaped_paths():
    checker = load("hostile_custody", "foundation_integration_v1/check_integration.py")
    manifest = json.loads((HERE / "foundation_integration_v1/MANIFEST.json").read_text())
    for kind in ("missing_pr", "duplicate_target", "source_drift", "integration_drift", "escape"):
        mutant = copy.deepcopy(manifest)
        files = mutant["sources"][0]["files"]
        if kind == "missing_pr":
            mutant["sources"].pop()
        elif kind == "duplicate_target":
            files.append(copy.deepcopy(files[0]))
        elif kind == "source_drift":
            files[0]["source_sha256"] = "0" * 64
        elif kind == "integration_drift":
            files[0]["integrated_sha256"] = "0" * 64
        else:
            files[0]["source_bytes_path"] = "../outside"
        with pytest.raises(ValueError):
            checker.verify(mutant)

from __future__ import annotations

from dataclasses import replace
import importlib.util
import itertools
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "research/machine-epistemics-theory/lifecycle_identification_v2/threshold_lifecycle.py"
spec = importlib.util.spec_from_file_location("infinite_threshold_lifecycle", MODULE)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

CONTEXT = m.Context("registered-host", "integer-guard", "exact-v1", "epoch-1")


def ledger(points, theta, *, units=None):
    units = units or [f"source-{i}" for i in range(len(points))]
    return m.Snapshot(CONTEXT, tuple(m.Observation(f"record-{i}", units[i], x, int(x >= theta), CONTEXT)
                                     for i, x in enumerate(points)))


def oracle_for(theta, prefix="oracle"):
    count = itertools.count()

    def oracle(x):
        identity = f"{prefix}-{next(count)}"
        return m.Observation(identity, identity, x, int(x >= theta), CONTEXT)

    return oracle


def test_interval_and_all_witnesses_match_independent_enumeration_after_every_deletion():
    # World enumeration covers all relevant breakpoints; tails are represented
    # by +/- 4. This validates bounded instances, not the infinite theorem.
    for theta in range(-2, 3):
        original = ledger((-2, -1, 0, 1, 2), theta)
        units = tuple(r.revocation_unit for r in original.records)
        for mask in range(1 << len(units)):
            revised = m.revoke(original, frozenset(u for i, u in enumerate(units) if mask & (1 << i)))
            rows = tuple(r for r in revised.records if r.revocation_unit not in revised.revoked)
            possible = [t for t in range(-4, 5) if all(int(r.x >= t) == r.label for r in rows)]
            for x in range(-3, 4):
                values = {int(x >= t) for t in possible}
                decision = m.predict(revised, x)
                assert (decision.status == "LIVE") == (len(values) == 1)
                if len(values) == 1:
                    assert decision.label == values.pop()
                    expected = set()
                    for unit in units:
                        kept = [r for r in rows if r.revocation_unit == unit]
                        unit_worlds = [t for t in range(-4, 5)
                                       if all(int(r.x >= t) == r.label for r in kept)]
                        if len({int(x >= t) for t in unit_worlds}) == 1:
                            expected.add(unit)
                    assert decision.witness_units == frozenset(expected)
                else:
                    assert decision.label is None and not decision.witness_units


def test_optimal_repair_matches_binary_decision_tree_lower_bound_for_all_small_intervals():
    checked = 0
    for lower in range(-5, 6):
        for size in range(1, 65):
            upper = lower + size - 1
            costs = []
            for theta in range(lower, upper + 1):
                snapshot = ledger((lower - 1, upper), theta)
                result = m.identify(snapshot, oracle_for(theta))
                assert result.status == "IDENTIFIED" and result.threshold == theta
                assert m.boundary_units(result.snapshot) is not None
                costs.append(len(result.query_points))
                checked += 1
            lower_bound = (size - 1).bit_length()
            assert max(costs) == lower_bound == m.optimal_repair_queries(snapshot)
    assert checked == 22880


@pytest.mark.parametrize("theta", [-(10**100), -1025, -1, 0, 1, 1025, 10**100])
def test_genuinely_unbounded_integer_representation_pointwise_identification(theta):
    result = m.identify(m.Snapshot(CONTEXT), oracle_for(theta), max_queries=1024, max_integer_bits=512)
    assert result.status == "IDENTIFIED" and result.threshold == theta
    # Conservative proof bound for this magnitude-doubling implementation.
    assert len(result.query_points) <= 2 * (abs(theta) + 1).bit_length() + 4


def test_unbounded_remaining_interval_has_no_uniform_bound_and_does_not_fake_identification():
    snapshot = ledger((0,), 1000)
    assert m.optimal_repair_queries(snapshot) is None
    result = m.identify(snapshot, oracle_for(10**100), max_queries=4)
    assert result.status == "CANNOT_CHECK" and result.threshold is None
    assert len(result.query_points) == 4
    assert m.version_space(result.snapshot).cardinality is None


def test_two_boundary_source_counts_exactly_characterize_all_r_unit_deletions():
    theta = 3
    for left_count, right_count in itertools.product(range(1, 4), repeat=2):
        snapshot = ledger((theta - 1,) * left_count + (theta,) * right_count, theta)
        units = tuple(r.revocation_unit for r in snapshot.records)
        for r in range(4):
            universal = True
            for deleted_count in range(min(r, len(units)) + 1):
                for deleted in itertools.combinations(units, deleted_count):
                    candidate = m.revoke(snapshot, frozenset(deleted))
                    universal &= m.version_space(candidate).cardinality == 1
            assert m.tolerates_revocations(snapshot, r) == universal
            assert universal == (min(left_count, right_count) > r)


def test_duplicate_record_ids_rejected_and_copied_source_does_not_buy_robustness():
    copied = ledger((1, 1, 2, 2), 2, units=("left", "left", "right", "right"))
    assert m.tolerates_revocations(copied, 0)
    assert not m.tolerates_revocations(copied, 1)
    duplicate = replace(copied, records=copied.records + copied.records[:1])
    with pytest.raises(m.CannotCheck, match="reused"):
        m.version_space(duplicate)


def test_one_source_can_attest_both_boundaries_without_counting_as_two_units():
    shared = ledger((1, 2, 1, 2), 2, units=("one", "one", "two", "two"))
    assert m.tolerates_revocations(shared, 1)
    assert not m.tolerates_revocations(shared, 2)
    assert m.version_space(m.revoke(shared, frozenset({"one"}))).cardinality == 1


def test_current_boundary_only_compression_loses_useful_retention():
    full = ledger((-1, 0, 2), 1)
    compressed = replace(full, records=full.records[1:])
    assert m.version_space(full) == m.version_space(compressed)
    deleted = frozenset({"source-1"})
    assert m.predict(m.revoke(full, deleted), -1).status == "LIVE"
    assert m.predict(m.revoke(compressed, deleted), -1).status == "UNKNOWN"


def test_contradiction_never_becomes_vacuously_live_or_identified():
    snapshot = m.Snapshot(CONTEXT, (m.Observation("a", "a", 0, 1, CONTEXT),
                                    m.Observation("b", "b", 1, 0, CONTEXT)))
    assert m.predict(snapshot, 0).status == "CONTRADICTION"
    assert m.identify(snapshot, oracle_for(0)).status == "CONTRADICTION"
    with pytest.raises(m.CannotCheck):
        m.optimal_repair_queries(snapshot)
    # Revoking the offending evidence genuinely restores consistency.
    assert m.predict(m.revoke(snapshot, frozenset({"b"})), 0).label == 1


@pytest.mark.parametrize("field,value", [("x", True), ("label", True), ("label", 2),
                                         ("identity", ""), ("revocation_unit", "")])
def test_malformed_observations_fail_closed(field, value):
    snapshot = ledger((0,), 1)
    with pytest.raises(m.CannotCheck):
        m.version_space(replace(snapshot, records=(replace(snapshot.records[0], **{field: value}),)))


@pytest.mark.parametrize("field", ["authority", "scope", "verifier", "epoch"])
def test_context_changes_require_new_evidence_binding(field):
    snapshot = ledger((0, 1), 1)
    changed = replace(CONTEXT, **{field: "changed"})
    with pytest.raises(m.CannotCheck, match="context mismatch"):
        m.version_space(replace(snapshot, context=changed))


def test_revocation_generators_unknown_sources_and_mutable_ledgers_rejected():
    snapshot = ledger((0, 1), 1)
    for units in ((x for x in ["source-0"]), frozenset({"unknown"})):
        with pytest.raises(m.CannotCheck):
            m.revoke(snapshot, units)
    with pytest.raises(m.CannotCheck):
        m.version_space(replace(snapshot, records=list(snapshot.records)))


def test_snapshot_digest_binds_all_observations_context_and_revocation():
    snapshot = ledger((0, 1), 1)
    original = m.snapshot_digest(snapshot)
    assert m.snapshot_digest(m.revoke(snapshot, frozenset({"source-0"}))) != original
    alternate = replace(snapshot, records=(replace(snapshot.records[0], revocation_unit="alternate"),) + snapshot.records[1:])
    assert m.snapshot_digest(alternate) != original


def test_query_and_integer_budgets_are_hard_and_failed_calls_count():
    calls = []

    def oracle(x):
        calls.append(x)
        return m.Observation("wrong", "wrong", x + 1, 0, CONTEXT)

    result = m.identify(m.Snapshot(CONTEXT), oracle, max_queries=0)
    assert result.status == "CANNOT_CHECK" and not calls
    result = m.identify(m.Snapshot(CONTEXT), oracle, max_queries=1)
    assert result.status == "CANNOT_CHECK" and len(result.query_points) == len(calls) == 1
    assert not result.snapshot.records
    result = m.identify(m.Snapshot(CONTEXT), oracle_for(1000), max_integer_bits=2)
    assert result.status == "CANNOT_CHECK" and result.query_points == (0,)
    for keyword in ({"max_queries": True}, {"max_integer_bits": 0}):
        with pytest.raises(m.CannotCheck):
            m.identify(m.Snapshot(CONTEXT), oracle, **keyword)


def test_oracle_cannot_resurrect_revoked_source_or_reuse_record_identity():
    original = ledger((0,), 1)
    revoked = m.revoke(original, frozenset({"source-0"}))
    result = m.identify(revoked, lambda x: m.Observation("new", "source-0", x, 0, CONTEXT))
    assert result.status == "CANNOT_CHECK" and result.snapshot == revoked
    result = m.identify(original, lambda x: m.Observation("record-0", "new", x, 0, CONTEXT))
    assert result.status == "CANNOT_CHECK" and result.snapshot == original


def test_oracle_unavailability_and_boolean_coordinate_return_cannot_check():
    def unavailable(x):
        raise RuntimeError("offline")

    result = m.identify(m.Snapshot(CONTEXT), unavailable)
    assert result.status == "CANNOT_CHECK" and result.query_points == (0,)
    result = m.identify(m.Snapshot(CONTEXT), lambda x: m.Observation("a", "a", False, 0, CONTEXT))
    assert result.status == "CANNOT_CHECK" and not result.snapshot.records


def test_oracle_unhashable_revocation_unit_returns_typed_cannot_check():
    result = m.identify(m.Snapshot(CONTEXT), lambda x: m.Observation("a", [], x, 0, CONTEXT))
    assert result.status == "CANNOT_CHECK" and not result.snapshot.records


def test_observation_context_field_cannot_forge_equality_with_real_authority():
    class EqualsAnything:
        def __eq__(self, other):
            return True

    row = m.Observation("a", "a", 0, 0, replace(CONTEXT, authority=EqualsAnything()))
    with pytest.raises(m.CannotCheck):
        m.version_space(m.Snapshot(CONTEXT, (row,)))

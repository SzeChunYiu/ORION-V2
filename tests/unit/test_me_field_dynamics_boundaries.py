"""Independent known-answer and malformed-premise checks for field dynamics."""
from __future__ import annotations

import importlib.util
import itertools
import json
import sys
import subprocess
from fractions import Fraction as Q
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "research/machine-epistemics-theory/field_dynamics_v1"
spec = importlib.util.spec_from_file_location("field_dynamics_boundaries", PACKAGE / "field_dynamics_exact.py")
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


@pytest.mark.parametrize("kernel,seed,alpha", [
    ([], [], Q(1, 3)), ([[1, 0]], [1], Q(1, 3)),
    ([[2]], [1], Q(1, 3)), ([[-1]], [1], Q(1, 3)),
    ([[1]], [2], Q(1, 3)), ([[1]], [-1], Q(1, 3)),
    ([[1]], [1, 0], Q(1, 3)), ([[1]], [1], 0),
    ([[1]], [1], Q(3, 2)), ([[0.5]], [1], Q(1, 3)),
    ([[True]], [1], Q(1, 3)),
])
def test_restart_refuses_unproved_hypotheses(kernel, seed, alpha):
    with pytest.raises(m.CannotCheck):
        m.fixed_point(kernel, seed, alpha)


def test_restart_known_answers_and_alpha_one():
    kernel = ((0, 1), (1, 0))
    assert m.fixed_point(kernel, (1, 0), Q(1, 2)) == [Q(2, 3), Q(1, 3)]
    assert m.fixed_point(kernel, (Q(1, 4), 0), 1) == [Q(1, 4), 0]
    assert m.fixed_point(((0,),), (1,), Q(1, 2)) == [Q(1, 2)]


def test_tracking_recurrence_on_256_time_varying_paths():
    alpha = Q(1, 3)
    maps = list(itertools.product((((1, 0), (0, 1)), ((0, 1), (1, 0))), ((1, 0), (0, 1))))
    fixed = [m.fixed_point(kernel, seed, alpha) for kernel, seed in maps]
    for path in itertools.product(range(4), repeat=4):
        current = [Q(0), Q(0)]
        errors = [m.l1(fixed[path[0]])]
        drifts = []
        for first, second in zip(path, path[1:]):
            kernel, seed = maps[first]
            current = [alpha*seed[j] + (1-alpha)*sum(kernel[i][j]*current[i] for i in range(2)) for j in range(2)]
            errors.append(m.l1([current[j]-fixed[second][j] for j in range(2)]))
            drifts.append(m.l1([fixed[first][j]-fixed[second][j] for j in range(2)]))
        assert all(error <= bound for error, bound in zip(errors, m.tracking_bounds(errors[0], drifts, alpha)))
    assert m.tracking_bounds(1, (Q(1, 2),)*3, Q(1, 2)) == (1, 1, 1, 1)


def test_forged_output_authority_fails_actual_comparator():
    internal = m.Authority(speaker=1)
    receipt = m.Authority(world_truth=2, speaker=2, commit=2)
    assert m.authority_preserved(m.Authority(speaker=1), internal, receipt)
    assert not m.authority_preserved(m.Authority(speaker=1, commit=1), internal, receipt)
    with pytest.raises(m.CannotCheck):
        m.Authority(commit=-1)


def test_registered_supports_unknown_and_joint_nogood():
    assert m.warrant_status(({"a"}, {"b"}), {"a", "b"}, revoked={"a"}) == m.LIVE
    assert m.warrant_status(({"a"},), {"a"}, unknown={"a"}) == m.UNKNOWN
    assert m.warrant_status((), {"a"}, closed=False) == m.UNKNOWN
    assert m.warrant_status(({"a", "b"},), {"a", "b"}, nogoods=({"a", "b"},)) == m.DEAD
    with pytest.raises(m.CannotCheck):
        m.warrant_status(({"forged"},), {"a"})


def test_revision_cone_handles_cycle_and_any_changed_tail():
    edges = [(('a', 'b'), ('c', 'd')), (('d',), ('a',)), (('x',), ('y',))]
    assert m.impact_cone({'a'}, edges) == {'a', 'c', 'd'}


def test_reinstatement_restores_projection_but_never_audit_history():
    original = m.EvidenceState(frozenset({'e'}), ('admit:e',))
    restored = m.reinstate(m.revoke(original, 'e'), 'e')
    assert restored.active == original.active
    assert restored != original
    assert restored.history[:len(original.history)] == original.history
    with pytest.raises(m.CannotCheck):
        m.reinstate(m.revoke(original, 'e'), 'new-unadmitted-identity')


def test_control_is_exists_action_forall_environment_and_multistep():
    actions = {'start': {'safe': {'stay'}, 'risky': {'stay', 'bad'}},
               'stay': {'wait': {'stay'}}, 'bad': {'wait': {'bad'}}}
    assert m.controlled_kernel(actions, actions, {'start', 'stay'}, model_closed=True) == {'start', 'stay'}
    actions['start'] = {'risky': {'stay', 'bad'}}
    assert m.controlled_kernel(actions, actions, {'start', 'stay'}, model_closed=True) == {'stay'}


def test_control_deadlock_and_missing_closure_do_not_pass():
    assert m.controlled_kernel({0}, {0: {}}, {0}, model_closed=True) == set()
    for actions, closed in [({0: {'wait': {0}}}, False), ({0: {'jump': {1}}}, True),
                            ({0: {'empty': set()}}, True), ({}, True)]:
        with pytest.raises(m.CannotCheck):
            m.controlled_kernel({0}, actions, {0}, model_closed=closed)
    with pytest.raises(m.CannotCheck):
        m.persistent_kernel({0}, {(0, 1)}, {0})


def test_one_shot_successors_cannot_turn_unsafe_or_empty_action_into_safe():
    for successors in (iter([1]), iter([])):
        with pytest.raises(m.CannotCheck):
            m.controlled_kernel({0, 1}, {0: {'go': successors}, 1: {}}, {0}, model_closed=True)
    assert m.controlled_kernel({0, 1}, {0: {'go': [1]}, 1: {}}, {0}, model_closed=True) == set()


def test_all_small_safety_games_against_stationary_policy_oracle():
    # Independent oracle enumerates policies and forward reachable sets;
    # implementation uses a backward greatest fixed point.
    states = {0, 1}
    subsets = [set(), {0}, {1}, {0, 1}]
    for destinations in itertools.product(({0}, {1}, {0, 1}), repeat=4):
        actions = {s: {a: destinations[2*s+a] for a in (0, 1)} for s in states}
        for safe in subsets:
            winning = set()
            for policy in itertools.product((0, 1), repeat=2):
                for start in safe:
                    reached, frontier = {start}, {start}
                    while frontier:
                        nxt = set().union(*(actions[s][policy[s]] for s in frontier)) - reached
                        reached |= nxt
                        frontier = nxt
                    if reached <= safe:
                        winning.add(start)
            assert m.controlled_kernel(states, actions, safe, model_closed=True) == winning


def test_binary_rare_outcome_is_not_bounded_by_one_realised_bit():
    responses = {i: 'rare' if i == 0 else 'common' for i in range(8)}
    assert m.channel_update(range(8), responses, 'rare', {0}, model_closed=True)
    assert m.channel_information_bound(responses)
    assert Q(8, 1) > 2  # log2(8/1)=3 > log2(two outcomes)=1.
    assert not m.channel_update(range(8), responses, 'common', {1}, model_closed=True)
    with pytest.raises(m.CannotCheck):
        m.channel_update(range(8), responses, 'outside-model', set(), model_closed=True)
    with pytest.raises(m.CannotCheck):
        m.channel_update(range(8), responses, 'rare', {0}, model_closed=False)


@pytest.mark.parametrize('responses', [{0: []}, [(0, 'label')], None, {}])
def test_channel_malformed_mapping_and_unhashable_outcomes_are_typed(responses):
    with pytest.raises(m.CannotCheck):
        m.channel_information_bound(responses)


@pytest.mark.parametrize('blocks', [(), ((), (0, 1)), ((0,),), ((0, 0), (1,)), ((0,), (2,)), ((False,), (1,))])
def test_invalid_quotients_are_cannot_check(blocks):
    with pytest.raises(m.CannotCheck):
        m.strong_lumpable(((1, 0), (0, 1)), blocks)


def test_lumpable_navigation_does_not_imply_revision_commutation():
    identity = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    blocks = ((0, 1), (2,))
    assert m.strong_lumpable(identity, blocks)
    assert m.revision_commutes((1, 0, 2), blocks, (0, 1))
    assert not m.revision_commutes((0, 2, 2), blocks, (0, 1))


@pytest.mark.parametrize('revision', [{0: 0, 1: False}, {0: 0, 1: 9}, iter([0, 0])])
def test_revision_mapping_keys_cannot_mask_invalid_targets(revision):
    with pytest.raises(m.CannotCheck):
        m.revision_commutes(revision, ((0, 1),), (0,))


def test_shadow_world_or_commit_write_is_rejected():
    before = {'K_world': ('claim',), 'K_self': (), 'commit': (), 'B_meter': 0}
    assert m.shadow_noninterfering(before, dict(before, K_self=('diagnosis',), B_meter=1))
    assert not m.shadow_noninterfering(before, dict(before, K_world=('rewritten',)))
    assert not m.shadow_noninterfering(before, dict(before, commit=('self-approved',)))
    assert not m.shadow_noninterfering(before, dict(before, new_capability=True))


@pytest.mark.parametrize('old,delta', [((1, 2), (3,)), ((1,), (-1,)), ((), ()), ((1.0,), (2,))])
def test_cost_cannot_disappear_by_truncation_or_refund(old, delta):
    with pytest.raises(m.CannotCheck):
        m.resource_add(old, delta)


def test_terminal_validation_and_budget_cover_malformed_attempts():
    for statuses in [(), (m.PASS,), (m.PASS,)*7, (m.PASS,)*5+('invented',), None,
                     itertools.repeat(m.PASS)]:
        assert m.run_pipeline(statuses)[0] == m.CC
    assert m.run_pipeline((m.PASS,)*6, budget=0) == ('RESOURCE_EXHAUSTED', ())
    status, trace = m.run_pipeline((m.PASS,)*6, budget=5)
    assert status == 'RESOURCE_EXHAUSTED' and len(trace) == 5
    assert m.run_pipeline((m.PASS, m.CC, m.PASS, m.PASS, m.PASS, m.PASS))[0] == m.CC


def test_registry_has_evidence_and_exact_open_scopes_for_all_laws():
    registry = json.loads((PACKAGE / 'REGISTRY.json').read_text())
    assert [law['id'] for law in registry['laws']] == [f'FD-{i:02}' for i in range(1, 13)]
    for law in registry['laws']:
        assert law['status'] in registry['status_vocabulary']
        for key in ('scope', 'parents', 'sources', 'checker', 'reopen', 'proof_obligation'):
            assert law[key]
    assert registry['authority']['OCM_ADOPTION'] == 'NOT_AUTHORIZED_BY_THIS_PACKAGE'


def test_standalone_checker_refuses_disabled_assertions():
    result = subprocess.run([sys.executable, '-O', str(PACKAGE / 'field_dynamics_exact.py')],
                            capture_output=True, text=True, check=False)
    assert result.returncode == 2
    assert json.loads(result.stdout)['status'] == m.CC

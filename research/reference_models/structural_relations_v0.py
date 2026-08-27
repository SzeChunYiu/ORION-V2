"""Non-authorizing ORION-V2 structural-relation reference model V0.

This module is a pre-freeze research instrument, not an admitted V2 runtime.
It implements only small exact known-answer checks used to test whether the
provisional relation vocabulary distinguishes several parent-owned cases.

It deliberately does not use language models, embeddings, network access or
scientific-authority promotion.  Passing these checks establishes neither
scientific novelty nor a complete structural-space theory.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from typing import Any, Iterable, Mapping, Sequence


class FixtureError(ValueError):
    """Raised when a research fixture is malformed."""


def _nonempty_strings(values: Iterable[Any], *, name: str) -> tuple[str, ...]:
    result = tuple(str(value) for value in values)
    if not result or any(not value for value in result):
        raise FixtureError(f"{name} must contain non-empty strings")
    if len(set(result)) != len(result):
        raise FixtureError(f"{name} must contain unique values")
    return result


def xor_constraints_satisfiable(
    variables: Sequence[str],
    domains: Sequence[int],
    constraints: Sequence[Mapping[str, Any]],
) -> bool:
    """Brute-force a finite XOR constraint system.

    This intentionally favors transparent exact behavior over scalability.
    """

    vars_tuple = _nonempty_strings(variables, name="variables")
    domain_tuple = tuple(int(value) for value in domains)
    if not domain_tuple:
        raise FixtureError("domains must not be empty")

    for assignment_values in product(domain_tuple, repeat=len(vars_tuple)):
        assignment = dict(zip(vars_tuple, assignment_values, strict=True))
        valid = True
        for constraint in constraints:
            names = tuple(constraint.get("variables", ()))
            expected = int(constraint.get("xor"))
            if not names or any(name not in assignment for name in names):
                raise FixtureError("constraint contains unknown or empty variables")
            parity = 0
            for name in names:
                parity ^= int(assignment[name])
            if parity != expected:
                valid = False
                break
        if valid:
            return True
    return False


def each_constraint_satisfiable(
    variables: Sequence[str],
    domains: Sequence[int],
    constraints: Sequence[Mapping[str, Any]],
) -> bool:
    return all(
        xor_constraints_satisfiable(variables, domains, (constraint,))
        for constraint in constraints
    )


def _skeleton(edges: Sequence[Sequence[str]]) -> frozenset[frozenset[str]]:
    result: set[frozenset[str]] = set()
    for edge in edges:
        if len(edge) != 2 or edge[0] == edge[1]:
            raise FixtureError(f"invalid directed edge: {edge!r}")
        result.add(frozenset((str(edge[0]), str(edge[1]))))
    return frozenset(result)


def _parent_map(nodes: Sequence[str], edges: Sequence[Sequence[str]]) -> dict[str, set[str]]:
    node_set = set(_nonempty_strings(nodes, name="nodes"))
    parents = {node: set() for node in node_set}
    for source, target in edges:
        if source not in node_set or target not in node_set:
            raise FixtureError("edge references unknown node")
        parents[target].add(source)
    return parents


def unshielded_colliders(
    nodes: Sequence[str], edges: Sequence[Sequence[str]]
) -> frozenset[tuple[str, str, str]]:
    """Return canonical a->b<-c triples whose endpoints are nonadjacent."""

    skeleton = _skeleton(edges)
    parents = _parent_map(nodes, edges)
    colliders: set[tuple[str, str, str]] = set()
    for middle, incoming in parents.items():
        for left, right in combinations(sorted(incoming), 2):
            if frozenset((left, right)) not in skeleton:
                colliders.add((left, middle, right))
    return frozenset(colliders)


def markov_equivalent_dags(
    nodes: Sequence[str],
    left_edges: Sequence[Sequence[str]],
    right_edges: Sequence[Sequence[str]],
) -> bool:
    """Use the standard skeleton + unshielded-collider criterion."""

    return (
        _skeleton(left_edges) == _skeleton(right_edges)
        and unshielded_colliders(nodes, left_edges)
        == unshielded_colliders(nodes, right_edges)
    )


def _state(states: Mapping[str, Any], state_id: str) -> Mapping[str, Any]:
    try:
        state = states[state_id]
    except KeyError as exc:
        raise FixtureError(f"unknown state: {state_id}") from exc
    if not isinstance(state, Mapping):
        raise FixtureError(f"state {state_id} must be a mapping")
    return state


def lts_bisimilar(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    """Greatest fixed-point bisimulation for small labelled transition systems."""

    left_states = left.get("states")
    right_states = right.get("states")
    if not isinstance(left_states, Mapping) or not isinstance(right_states, Mapping):
        raise FixtureError("LTS states must be mappings")

    relation: set[tuple[str, str]] = {
        (l_id, r_id)
        for l_id, l_state in left_states.items()
        for r_id, r_state in right_states.items()
        if l_state.get("label") == r_state.get("label")
    }

    def successors(state: Mapping[str, Any], action: str) -> tuple[str, ...]:
        transitions = state.get("transitions", {})
        if not isinstance(transitions, Mapping):
            raise FixtureError("transitions must be a mapping")
        raw = transitions.get(action, ())
        return tuple(str(item) for item in raw)

    changed = True
    while changed:
        changed = False
        retained: set[tuple[str, str]] = set()
        for left_id, right_id in relation:
            l_state = _state(left_states, left_id)
            r_state = _state(right_states, right_id)
            l_actions = set(l_state.get("transitions", {}))
            r_actions = set(r_state.get("transitions", {}))
            actions = l_actions | r_actions
            valid = True
            for action in actions:
                l_succ = successors(l_state, action)
                r_succ = successors(r_state, action)
                if any(not any((l_next, r_next) in relation for r_next in r_succ) for l_next in l_succ):
                    valid = False
                    break
                if any(not any((l_next, r_next) in relation for l_next in l_succ) for r_next in r_succ):
                    valid = False
                    break
            if valid:
                retained.add((left_id, right_id))
            else:
                changed = True
        relation = retained

    return (str(left.get("start")), str(right.get("start"))) in relation


def role_equivalent(left_profile: Mapping[str, Any], right_profile: Mapping[str, Any]) -> bool:
    """Exact equality of a deliberately source-independent role profile."""

    return dict(left_profile) == dict(right_profile)


def quotient_safe_for_target(
    states: Mapping[str, Mapping[str, Any]],
    partition: Sequence[Sequence[str]],
    target: str,
) -> bool:
    """A quotient is target-safe iff target values are constant in every block."""

    seen: set[str] = set()
    for block in partition:
        if not block:
            raise FixtureError("partition blocks must be non-empty")
        values: set[Any] = set()
        for state_id in block:
            if state_id in seen:
                raise FixtureError("partition blocks overlap")
            seen.add(state_id)
            if state_id not in states:
                raise FixtureError(f"unknown partition state: {state_id}")
            if target not in states[state_id]:
                raise FixtureError(f"state {state_id} lacks target {target}")
            values.add(states[state_id][target])
        if len(values) > 1:
            return False
    return True


def minimum_distinguishing_probe_sets(
    hypothesis_signatures: Mapping[str, Mapping[str, Any]],
) -> tuple[tuple[str, ...], ...]:
    """Return all minimum probe sets separating every hypothesis pair."""

    hypotheses = tuple(sorted(hypothesis_signatures))
    if len(hypotheses) < 2:
        return ((),)
    probe_sets = [set(hypothesis_signatures[hypothesis]) for hypothesis in hypotheses]
    if any(probes != probe_sets[0] for probes in probe_sets[1:]):
        raise FixtureError("all hypothesis signatures must use the same probes")
    probes = tuple(sorted(probe_sets[0]))

    def separates(candidate: Sequence[str]) -> bool:
        fingerprints = {
            tuple(hypothesis_signatures[hypothesis][probe] for probe in candidate)
            for hypothesis in hypotheses
        }
        return len(fingerprints) == len(hypotheses)

    for size in range(1, len(probes) + 1):
        winners = tuple(candidate for candidate in combinations(probes, size) if separates(candidate))
        if winners:
            return winners
    return ()


def classify_censoring_terminal(provider_status: Mapping[str, str]) -> str:
    """Do not turn an unobserved route into structural non-identifiability."""

    statuses = {str(value).upper() for value in provider_status.values()}
    if "CENSORED" in statuses:
        return "SEARCH_ROUTE_CENSORED"
    if statuses and statuses <= {"OBSERVED_NO_SEPARATOR"}:
        return "STRUCTURALLY_NONIDENTIFIABLE"
    return "CANNOT_CHECK"


@dataclass(frozen=True)
class JumpLevelResult:
    level: int
    tested: bool
    sufficient: bool
    evidence_id: str

    def __post_init__(self) -> None:
        if not 0 <= self.level <= 8:
            raise ValueError("Jump level must be in [0, 8]")
        if not self.evidence_id:
            raise ValueError("Jump level result requires evidence identity")
        if self.sufficient and not self.tested:
            raise ValueError("untested level cannot be sufficient")


def minimum_sufficient_jump_level(
    results: Sequence[JumpLevelResult],
    *,
    incumbent_insufficiency_witnessed: bool,
    coverage_censored: bool = False,
) -> int | str:
    """Return the minimum tested sufficient level, or an honest terminal."""

    if coverage_censored:
        return "CANNOT_CHECK"
    if not incumbent_insufficiency_witnessed:
        return "INCUMBENT_INSUFFICIENCY_NOT_IDENTIFIED"
    by_level = sorted(results, key=lambda item: item.level)
    for item in by_level:
        if item.tested and item.sufficient:
            return item.level
    return "CANNOT_CHECK"


__all__ = [
    "FixtureError",
    "JumpLevelResult",
    "classify_censoring_terminal",
    "each_constraint_satisfiable",
    "lts_bisimilar",
    "markov_equivalent_dags",
    "minimum_distinguishing_probe_sets",
    "minimum_sufficient_jump_level",
    "quotient_safe_for_target",
    "role_equivalent",
    "unshielded_colliders",
    "xor_constraints_satisfiable",
]

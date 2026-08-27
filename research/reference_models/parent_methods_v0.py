"""Exact, small parent-method reference implementations for ORION-V2 V0.

These functions intentionally adopt mature parent semantics on finite examples.
They are not novel ORION algorithms and are not scalable production solvers.
"""

from __future__ import annotations

from itertools import product
from typing import Any, Mapping, Sequence


class ParentMethodInputError(ValueError):
    pass


def _matrix_shape(matrix: Sequence[Sequence[float]]) -> tuple[int, int]:
    if not matrix or not matrix[0]:
        raise ParentMethodInputError("matrix must be non-empty")
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ParentMethodInputError("matrix rows must have equal width")
    return len(matrix), width


def verify_stochastic_matrix(matrix: Sequence[Sequence[float]], *, tolerance: float = 1e-12) -> bool:
    try:
        _matrix_shape(matrix)
    except ParentMethodInputError:
        return False
    for row in matrix:
        if any(value < -tolerance for value in row):
            return False
        if abs(sum(row) - 1.0) > tolerance:
            return False
    return True


def multiply_matrices(
    left: Sequence[Sequence[float]],
    right: Sequence[Sequence[float]],
) -> list[list[float]]:
    left_rows, left_width = _matrix_shape(left)
    right_rows, right_width = _matrix_shape(right)
    if left_width != right_rows:
        raise ParentMethodInputError("matrix dimensions do not align")
    return [
        [sum(left[i][k] * right[k][j] for k in range(left_width)) for j in range(right_width)]
        for i in range(left_rows)
    ]


def verify_blackwell_garbling(
    informative_experiment: Sequence[Sequence[float]],
    less_informative_experiment: Sequence[Sequence[float]],
    garbling_kernel: Sequence[Sequence[float]],
    *,
    tolerance: float = 1e-12,
) -> bool:
    """Verify F = E K with stochastic experiment rows and kernel rows."""

    if not verify_stochastic_matrix(informative_experiment, tolerance=tolerance):
        return False
    if not verify_stochastic_matrix(less_informative_experiment, tolerance=tolerance):
        return False
    if not verify_stochastic_matrix(garbling_kernel, tolerance=tolerance):
        return False
    try:
        reconstructed = multiply_matrices(informative_experiment, garbling_kernel)
    except ParentMethodInputError:
        return False
    if _matrix_shape(reconstructed) != _matrix_shape(less_informative_experiment):
        return False
    return all(
        abs(reconstructed[i][j] - less_informative_experiment[i][j]) <= tolerance
        for i in range(len(reconstructed))
        for j in range(len(reconstructed[0]))
    )


def optimal_finite_decision_value(
    experiment: Sequence[Sequence[float]],
    prior: Sequence[float],
    utility: Sequence[Sequence[float]],
) -> float:
    """Brute-force deterministic decision rules for a finite experiment.

    utility[state][action] and experiment[state][observation]. Randomized rules
    cannot improve a finite expected-utility maximum over deterministic rules.
    """

    n_states, n_observations = _matrix_shape(experiment)
    if len(prior) != n_states or abs(sum(prior) - 1.0) > 1e-12:
        raise ParentMethodInputError("prior must match states and sum to one")
    if len(utility) != n_states or not utility or any(len(row) != len(utility[0]) for row in utility):
        raise ParentMethodInputError("utility must have one equal-width row per state")
    n_actions = len(utility[0])
    best = float("-inf")
    for rule in product(range(n_actions), repeat=n_observations):
        expected = 0.0
        for state in range(n_states):
            for observation in range(n_observations):
                expected += (
                    prior[state]
                    * experiment[state][observation]
                    * utility[state][rule[observation]]
                )
        best = max(best, expected)
    return best


def indiscernibility_classes(
    attributes: Mapping[str, Mapping[str, Any]],
    selected_attributes: Sequence[str],
) -> tuple[frozenset[str], ...]:
    if not attributes:
        raise ParentMethodInputError("attribute system must not be empty")
    selected = tuple(selected_attributes)
    if not selected:
        return (frozenset(attributes),)
    signatures: dict[tuple[Any, ...], set[str]] = {}
    for object_id, row in attributes.items():
        if any(attribute not in row for attribute in selected):
            raise ParentMethodInputError("selected attribute missing from an object")
        signature = tuple(row[attribute] for attribute in selected)
        signatures.setdefault(signature, set()).add(object_id)
    return tuple(sorted((frozenset(group) for group in signatures.values()), key=lambda group: sorted(group)))


def rough_approximations(
    attributes: Mapping[str, Mapping[str, Any]],
    selected_attributes: Sequence[str],
    target: Sequence[str],
) -> tuple[frozenset[str], frozenset[str]]:
    target_set = frozenset(target)
    unknown = target_set - set(attributes)
    if unknown:
        raise ParentMethodInputError(f"target contains unknown objects: {sorted(unknown)}")
    lower: set[str] = set()
    upper: set[str] = set()
    for equivalence_class in indiscernibility_classes(attributes, selected_attributes):
        if equivalence_class <= target_set:
            lower.update(equivalence_class)
        if equivalence_class & target_set:
            upper.update(equivalence_class)
    return frozenset(lower), frozenset(upper)


def finite_viability_kernel(
    transitions: Mapping[str, Mapping[str, Sequence[str]]],
    constraint_states: Sequence[str],
) -> frozenset[str]:
    """Greatest subset where every retained state has some action staying inside."""

    kernel = set(constraint_states)
    if any(state not in transitions for state in kernel):
        raise ParentMethodInputError("constraint state lacks transitions")
    changed = True
    while changed:
        changed = False
        remove: set[str] = set()
        for state in kernel:
            actions = transitions[state]
            viable_action = any(
                successors and all(successor in kernel for successor in successors)
                for successors in actions.values()
            )
            if not viable_action:
                remove.add(state)
        if remove:
            kernel -= remove
            changed = True
    return frozenset(kernel)


def _fault_key(faults: Sequence[str]) -> str:
    return "+".join(sorted(faults))


def minimal_consistent_diagnoses(
    components: Sequence[str],
    predictions: Mapping[str, Any],
    observation: Any,
) -> tuple[frozenset[str], ...]:
    """Enumerate subset-minimal fault sets predicting the observation."""

    components_tuple = tuple(sorted(components))
    candidates: list[frozenset[str]] = []
    for size in range(len(components_tuple) + 1):
        for subset in combinations_tuple(components_tuple, size):
            faults = frozenset(subset)
            if predictions.get(_fault_key(subset)) != observation:
                continue
            if any(existing < faults for existing in candidates):
                continue
            candidates.append(faults)
    return tuple(candidates)


def combinations_tuple(values: Sequence[str], size: int) -> tuple[tuple[str, ...], ...]:
    """Small local combination helper avoiding an exposed iterator in receipts."""

    if size == 0:
        return ((),)
    if size > len(values):
        return ()
    result: list[tuple[str, ...]] = []

    def visit(start: int, selected: list[str]) -> None:
        if len(selected) == size:
            result.append(tuple(selected))
            return
        remaining_needed = size - len(selected)
        for index in range(start, len(values) - remaining_needed + 1):
            selected.append(values[index])
            visit(index + 1, selected)
            selected.pop()

    visit(0, [])
    return tuple(result)


def workflow_option_to_complete(
    graph: Mapping[str, Sequence[str]],
    *,
    start: str,
    end: str,
) -> bool:
    """Every state reachable from start must have a path to end."""

    if start not in graph or end not in graph:
        raise ParentMethodInputError("start and end must exist in graph")

    reachable: set[str] = set()
    stack = [start]
    while stack:
        state = stack.pop()
        if state in reachable:
            continue
        reachable.add(state)
        stack.extend(str(successor) for successor in graph[state])

    reverse: dict[str, set[str]] = {node: set() for node in graph}
    for source, successors in graph.items():
        for successor in successors:
            if successor not in graph:
                raise ParentMethodInputError("workflow edge references unknown node")
            reverse[successor].add(source)

    can_reach_end: set[str] = set()
    stack = [end]
    while stack:
        state = stack.pop()
        if state in can_reach_end:
            continue
        can_reach_end.add(state)
        stack.extend(reverse[state])

    return reachable <= can_reach_end


__all__ = [
    "ParentMethodInputError",
    "finite_viability_kernel",
    "indiscernibility_classes",
    "minimal_consistent_diagnoses",
    "multiply_matrices",
    "optimal_finite_decision_value",
    "rough_approximations",
    "verify_blackwell_garbling",
    "verify_stochastic_matrix",
    "workflow_option_to_complete",
]

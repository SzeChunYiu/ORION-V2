from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Hashable, Mapping

State = Hashable


class ViabilityMode(str, Enum):
    EXISTENTIAL = "EXISTENTIAL"
    ROBUST = "ROBUST"


@dataclass(frozen=True, slots=True)
class FiniteViabilitySystem:
    system_id: str
    states: frozenset[State]
    transitions: Mapping[tuple[State, str], frozenset[State]]
    admissible_actions: Mapping[State, frozenset[str]]
    safe_states: frozenset[State]
    goal_states: frozenset[State] = frozenset()

    def __post_init__(self) -> None:
        if not self.system_id.strip() or not self.states:
            raise ValueError("viability systems require identity and states")
        if not self.safe_states <= self.states or not self.goal_states <= self.safe_states:
            raise ValueError("safe states must be declared and goals must be safe")
        if set(self.admissible_actions) != set(self.states):
            raise ValueError("admissible actions must be declared for every state")
        for (state, action), successors in self.transitions.items():
            if state not in self.states or action not in self.admissible_actions[state]:
                raise ValueError("transition action must be admissible at its source")
            if not successors or not set(successors) <= set(self.states):
                raise ValueError("transitions require non-empty declared successors")

    def successors(self, state: State, action: str) -> frozenset[State]:
        return self.transitions.get((state, action), frozenset())


def _action_stays_in(
    system: FiniteViabilitySystem,
    state: State,
    action: str,
    candidate: set[State],
    mode: ViabilityMode,
) -> bool:
    successors = system.successors(state, action)
    if not successors:
        return False
    if mode is ViabilityMode.ROBUST:
        return set(successors) <= candidate
    return bool(set(successors) & candidate)


def viability_kernel(
    system: FiniteViabilitySystem,
    *,
    mode: ViabilityMode = ViabilityMode.ROBUST,
) -> frozenset[State]:
    mode = ViabilityMode(mode)
    candidate = set(system.safe_states)
    changed = True
    while changed:
        changed = False
        for state in tuple(candidate):
            if not any(
                _action_stays_in(system, state, action, candidate, mode)
                for action in system.admissible_actions[state]
            ):
                candidate.remove(state)
                changed = True
    return frozenset(candidate)


def justified_capture_kernel(
    system: FiniteViabilitySystem,
    *,
    mode: ViabilityMode = ViabilityMode.ROBUST,
) -> frozenset[State]:
    """States from which a declared goal can be reached while staying safe.

    Robust mode requires every successor of the selected action to already lie
    in the growing capture set. Existential mode requires at least one.
    """

    mode = ViabilityMode(mode)
    if not system.goal_states:
        return frozenset()
    viable = set(viability_kernel(system, mode=mode))
    capture = set(system.goal_states) & viable
    changed = True
    while changed:
        changed = False
        for state in viable - capture:
            for action in system.admissible_actions[state]:
                successors = set(system.successors(state, action))
                if not successors:
                    continue
                if mode is ViabilityMode.ROBUST and successors <= capture:
                    capture.add(state)
                    changed = True
                    break
                if mode is ViabilityMode.EXISTENTIAL and successors & capture:
                    capture.add(state)
                    changed = True
                    break
    return frozenset(capture)

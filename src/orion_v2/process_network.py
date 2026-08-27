from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum


class ProcessSoundnessStatus(str, Enum):
    SOUND = "SOUND"
    DEADLOCK = "DEADLOCK"
    COMPLETION_NOT_REACHABLE_FROM_ALL_STATES = "COMPLETION_NOT_REACHABLE_FROM_ALL_STATES"
    REQUIRED_TASK_DEAD = "REQUIRED_TASK_DEAD"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class ProcessTask:
    task_id: str
    requires: frozenset[str]
    produces: frozenset[str]
    resource_cost: tuple[tuple[str, int], ...] = ()
    evidence_required: frozenset[str] = frozenset()
    authority_required: int = 0
    reopens: frozenset[str] = frozenset()
    required_live: bool = True

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ValueError("task_id must be non-blank")
        if not self.produces and not self.reopens:
            raise ValueError("tasks must produce or reopen at least one obligation")
        if self.authority_required < 0:
            raise ValueError("authority requirements must be non-negative")
        names = [name for name, _ in self.resource_cost]
        if len(names) != len(set(names)) or any(
            not name.strip() or cost < 0 for name, cost in self.resource_cost
        ):
            raise ValueError(
                "resource costs require unique non-blank names and non-negative costs"
            )


@dataclass(frozen=True, slots=True)
class ProcessMarking:
    fulfilled: frozenset[str]
    resources: tuple[tuple[str, int], ...]
    executed_task_ids: frozenset[str] = frozenset()

    def resource_map(self) -> dict[str, int]:
        return dict(self.resources)


@dataclass(frozen=True, slots=True)
class ObligationProcessNetwork:
    network_id: str
    obligations: frozenset[str]
    initial_fulfilled: frozenset[str]
    terminal_obligations: frozenset[str]
    tasks: tuple[ProcessTask, ...]
    initial_resources: tuple[tuple[str, int], ...] = ()
    available_evidence: frozenset[str] = frozenset()
    authority_ceiling: int = 0

    def __post_init__(self) -> None:
        if not self.network_id.strip():
            raise ValueError("network_id must be non-blank")
        if not self.obligations or not self.terminal_obligations <= self.obligations:
            raise ValueError(
                "terminal obligations must be a non-empty subset of obligations"
            )
        if not self.initial_fulfilled <= self.obligations:
            raise ValueError("initial obligations must be declared")
        task_ids = [task.task_id for task in self.tasks]
        if len(task_ids) != len(set(task_ids)):
            raise ValueError("task identities must be unique")
        for task in self.tasks:
            if not (task.requires | task.produces | task.reopens) <= self.obligations:
                raise ValueError("tasks may reference only declared obligations")
        resource_names = [name for name, _ in self.initial_resources]
        if len(resource_names) != len(set(resource_names)) or any(
            not name.strip() or value < 0 for name, value in self.initial_resources
        ):
            raise ValueError(
                "initial resources require unique names and non-negative values"
            )
        if self.authority_ceiling < 0:
            raise ValueError("authority ceiling must be non-negative")

    @property
    def initial_marking(self) -> ProcessMarking:
        return ProcessMarking(
            self.initial_fulfilled,
            tuple(sorted(self.initial_resources)),
            frozenset(),
        )


def _enabled(
    network: ObligationProcessNetwork,
    marking: ProcessMarking,
    task: ProcessTask,
) -> bool:
    if task.task_id in marking.executed_task_ids:
        return False
    if not task.requires <= marking.fulfilled:
        return False
    if task.evidence_required - network.available_evidence:
        return False
    if task.authority_required > network.authority_ceiling:
        return False
    resources = marking.resource_map()
    return all(resources.get(name, 0) >= cost for name, cost in task.resource_cost)


def apply_task(
    network: ObligationProcessNetwork,
    marking: ProcessMarking,
    task: ProcessTask,
) -> ProcessMarking:
    if not _enabled(network, marking, task):
        raise ValueError("task is not enabled")
    resources = marking.resource_map()
    for name, cost in task.resource_cost:
        resources[name] = resources.get(name, 0) - cost
    fulfilled = (marking.fulfilled - task.reopens) | task.produces
    return ProcessMarking(
        frozenset(fulfilled),
        tuple(sorted(resources.items())),
        marking.executed_task_ids | {task.task_id},
    )


@dataclass(frozen=True, slots=True)
class ProcessSoundnessAssessment:
    network_id: str
    status: ProcessSoundnessStatus
    reachable_state_count: int
    completion_state_count: int
    deadlock_states: tuple[str, ...]
    dead_required_task_ids: tuple[str, ...]
    states_without_completion_path: tuple[str, ...]
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted:
            raise ValueError("process soundness does not grant scientific authority")


def _marking_label(marking: ProcessMarking) -> str:
    return repr(
        (
            tuple(sorted(marking.fulfilled)),
            marking.resources,
            tuple(sorted(marking.executed_task_ids)),
        )
    )


def assess_process_soundness(
    network: ObligationProcessNetwork,
    *,
    state_limit: int = 10_000,
) -> ProcessSoundnessAssessment:
    if state_limit < 1:
        raise ValueError("state_limit must be positive")
    queue = deque([network.initial_marking])
    states = {network.initial_marking}
    edges: dict[ProcessMarking, set[ProcessMarking]] = {}
    fired_tasks: set[str] = set()
    while queue:
        marking = queue.popleft()
        outgoing: set[ProcessMarking] = set()
        for task in network.tasks:
            if not _enabled(network, marking, task):
                continue
            successor = apply_task(network, marking, task)
            outgoing.add(successor)
            fired_tasks.add(task.task_id)
            if successor not in states:
                if len(states) >= state_limit:
                    return ProcessSoundnessAssessment(
                        network.network_id,
                        ProcessSoundnessStatus.CANNOT_CHECK,
                        len(states),
                        0,
                        (),
                        (),
                        (),
                    )
                states.add(successor)
                queue.append(successor)
        edges[marking] = outgoing

    completion_states = {
        state for state in states if network.terminal_obligations <= state.fulfilled
    }
    deadlocks = tuple(
        sorted(
            _marking_label(state)
            for state in states
            if not edges.get(state) and state not in completion_states
        )
    )
    reverse: dict[ProcessMarking, set[ProcessMarking]] = {
        state: set() for state in states
    }
    for source, successors in edges.items():
        for target in successors:
            reverse[target].add(source)
    can_complete = set(completion_states)
    frontier = list(completion_states)
    while frontier:
        target = frontier.pop()
        for predecessor in reverse[target]:
            if predecessor not in can_complete:
                can_complete.add(predecessor)
                frontier.append(predecessor)
    dead_required = tuple(
        sorted(
            task.task_id
            for task in network.tasks
            if task.required_live and task.task_id not in fired_tasks
        )
    )
    no_completion = tuple(sorted((_marking_label(state) for state in states - can_complete)))
    if deadlocks:
        status = ProcessSoundnessStatus.DEADLOCK
    elif no_completion:
        status = ProcessSoundnessStatus.COMPLETION_NOT_REACHABLE_FROM_ALL_STATES
    elif dead_required:
        status = ProcessSoundnessStatus.REQUIRED_TASK_DEAD
    else:
        status = ProcessSoundnessStatus.SOUND
    return ProcessSoundnessAssessment(
        network.network_id,
        status,
        len(states),
        len(completion_states),
        deadlocks,
        dead_required,
        no_completion,
    )

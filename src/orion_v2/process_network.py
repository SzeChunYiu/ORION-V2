from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Mapping


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


def reachable_process_graph(
    network: ObligationProcessNetwork,
) -> tuple[
    frozenset[ProcessMarking],
    Mapping[ProcessMarking, tuple[tuple[str, ProcessMarking], ...]],
]:
    initial = network.initial_marking
    queue: deque[ProcessMarking] = deque([initial])
    seen = {initial}
    edges: dict[ProcessMarking, tuple[tuple[str, ProcessMarking], ...]] = {}
    while queue:
        marking = queue.popleft()
        outgoing: list[tuple[str, ProcessMarking]] = []
        for task in network.tasks:
            if _enabled(network, marking, task):
                successor = apply_task(network, marking, task)
                if successor != marking:
                    outgoing.append((task.task_id, successor))
                    if successor not in seen:
                        seen.add(successor)
                        queue.append(successor)
        edges[marking] = tuple(outgoing)
    return frozenset(seen), edges


@dataclass(frozen=True, slots=True)
class ProcessSoundnessAssessment:
    network_id: str
    status: ProcessSoundnessStatus
    reachable_state_count: int
    completion_state_count: int
    deadlock_states: tuple[ProcessMarking, ...]
    dead_required_task_ids: tuple[str, ...]
    states_without_completion_path: tuple[ProcessMarking, ...]
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted:
            raise ValueError("process soundness does not grant scientific authority")


def assess_process_soundness(
    network: ObligationProcessNetwork,
) -> ProcessSoundnessAssessment:
    states, graph = reachable_process_graph(network)
    completion_states = {
        state
        for state in states
        if network.terminal_obligations <= state.fulfilled
    }
    if not completion_states:
        return ProcessSoundnessAssessment(
            network.network_id,
            ProcessSoundnessStatus.CANNOT_CHECK,
            len(states),
            0,
            (),
            (),
            tuple(sorted(states, key=repr)),
        )
    reverse: dict[ProcessMarking, set[ProcessMarking]] = {
        state: set() for state in states
    }
    fired_tasks: set[str] = set()
    for source, outgoing in graph.items():
        for task_id, target in outgoing:
            reverse[target].add(source)
            fired_tasks.add(task_id)
    can_complete = set(completion_states)
    queue: deque[ProcessMarking] = deque(completion_states)
    while queue:
        state = queue.popleft()
        for predecessor in reverse[state]:
            if predecessor not in can_complete:
                can_complete.add(predecessor)
                queue.append(predecessor)
    deadlocks = tuple(
        sorted(
            (
                state
                for state in states
                if state not in completion_states and not graph[state]
            ),
            key=repr,
        )
    )
    dead_required = tuple(
        sorted(
            task.task_id
            for task in network.tasks
            if task.required_live and task.task_id not in fired_tasks
        )
    )
    no_completion = tuple(sorted(states - can_complete, key=repr))
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

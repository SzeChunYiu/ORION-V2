from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True, slots=True)
class WorkflowTask:
    task_id: str; action_family: str; authority_requirements: tuple[str, ...] = ()
    def __post_init__(self) -> None:
        if not self.task_id.strip() or not self.action_family.strip(): raise ValueError("task identity and family must be non-blank")

@dataclass(frozen=True, slots=True)
class PrecedenceConstraint:
    before_id: str; after_id: str; reason: str
    def __post_init__(self) -> None:
        if self.before_id == self.after_id or any(not x.strip() for x in (self.before_id, self.after_id, self.reason)): raise ValueError("precedence requires distinct tasks and reason")

class WorkflowConformanceStatus(str, Enum):
    CONFORMANT="CONFORMANT"; ORDER_VIOLATION="ORDER_VIOLATION"; UNKNOWN_TASK="UNKNOWN_TASK"; DUPLICATE_TASK_EXECUTION="DUPLICATE_TASK_EXECUTION"

@dataclass(frozen=True, slots=True)
class WorkflowConformanceReceipt:
    status: WorkflowConformanceStatus; violated_constraints: tuple[tuple[str,str],...]; unknown_task_ids: tuple[str,...]

@dataclass(frozen=True, slots=True)
class WorkflowSpec:
    workflow_id: str; tasks: tuple[WorkflowTask,...]; precedence: tuple[PrecedenceConstraint,...]
    def __post_init__(self) -> None:
        if not self.workflow_id.strip(): raise ValueError("workflow_id must be non-blank")
        ids=[t.task_id for t in self.tasks]
        if not ids or len(ids)!=len(set(ids)): raise ValueError("workflow tasks must be non-empty and unique")
        known=set(ids)
        if any(c.before_id not in known or c.after_id not in known for c in self.precedence): raise ValueError("precedence references unknown task")
        self._assert_acyclic()
    def _assert_acyclic(self) -> None:
        adj={t.task_id:set() for t in self.tasks}
        for c in self.precedence: adj[c.before_id].add(c.after_id)
        for start in adj:
            stack=list(adj[start]); seen=set()
            while stack:
                node=stack.pop()
                if node==start: raise ValueError("workflow precedence must be acyclic")
                if node in seen: continue
                seen.add(node); stack.extend(adj[node])
    def precedes(self,left_id:str,right_id:str)->bool:
        adj={t.task_id:set() for t in self.tasks}
        for c in self.precedence: adj[c.before_id].add(c.after_id)
        reached=set(); stack=list(adj[left_id])
        while stack:
            node=stack.pop()
            if node in reached: continue
            reached.add(node); stack.extend(adj[node])
        return right_id in reached
    def can_run_concurrently(self,left_id:str,right_id:str)->bool:
        known={t.task_id for t in self.tasks}
        return left_id in known and right_id in known and left_id!=right_id and not self.precedes(left_id,right_id) and not self.precedes(right_id,left_id)
    def check_trace(self,task_ids:tuple[str,...])->WorkflowConformanceReceipt:
        known={t.task_id for t in self.tasks}; unknown=tuple(sorted(set(task_ids)-known))
        if unknown: return WorkflowConformanceReceipt(WorkflowConformanceStatus.UNKNOWN_TASK,(),unknown)
        if len(task_ids)!=len(set(task_ids)): return WorkflowConformanceReceipt(WorkflowConformanceStatus.DUPLICATE_TASK_EXECUTION,(),())
        pos={task_id:i for i,task_id in enumerate(task_ids)}
        violated=tuple(sorted((c.before_id,c.after_id) for c in self.precedence if c.before_id in pos and c.after_id in pos and pos[c.before_id]>pos[c.after_id]))
        return WorkflowConformanceReceipt(WorkflowConformanceStatus.ORDER_VIOLATION if violated else WorkflowConformanceStatus.CONFORMANT,violated,())

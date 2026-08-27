"""Small end-to-end known-answer scenarios; local engineering evidence only."""
from orion_v2.contracts import Obligation, ObligationStatus, ProblemContract, Terminal
from orion_v2.jump import JumpAssessment, JumpLevel, JumpProposal, JumpTrigger, TriggerKind, assess_jump
from orion_v2.probes import Hypothesis, Probe, ProbeDesignStatus, minimum_separating_probe_set
from orion_v2.solver import SolverState, StepReceipt, apply_step

def test_direct_problem_solves_without_jump() -> None:
    contract=ProblemContract('p-direct','select answer','decision',('finite known-answer world',),resource_budget=3)
    state=SolverState('s0',contract,(Obligation('verify','verify answer'),),remaining_resource=3)
    updated=apply_step(state,StepReceipt('step-check','native-check','s0','s1',cost=1),obligations=(Obligation('verify','verify answer',ObligationStatus.SATISFIED),))
    assert updated.terminal is Terminal.JUSTIFIED_SOLUTION

def test_nonidentifiability_is_found_before_jump() -> None:
    design=minimum_separating_probe_set((Hypothesis('h1'),Hypothesis('h2')),(Probe('same-observation',{'h1':0,'h2':0}),))
    assert design.status is ProbeDesignStatus.NONIDENTIFIABLE_UNDER_PROBE_FAMILY
    trigger=JumpTrigger('t',TriggerKind.STRUCTURAL_NONIDENTIFIABILITY,JumpLevel.ACTION_PARAMETER,('probe-receipt',),('J0-probe-family-exhausted',))
    proposal=JumpProposal('new-probe-family',trigger,JumpLevel.METHOD_TOOL_INSTRUMENT_INVENTION,'new-instrument',('parent:optimal-design',),('map:old-new-observables',),('preserve:old-observations',),('contract:distinguish',),('falsifier:new-probe-also-ties',))
    assert assess_jump(proposal,lower_level_sufficient=False,donor_product_ties=False) is JumpAssessment.CANDIDATE_FOR_PROTECTED_EVALUATION

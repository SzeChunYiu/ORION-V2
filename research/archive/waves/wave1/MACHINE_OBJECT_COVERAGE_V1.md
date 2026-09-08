# ORION-V2 Wave 1 — Machine Object Coverage V1

## Implemented and tested

| Research obligation | Reference object/function | Known-answer coverage |
|---|---|---|
| exact V1 handoff | `HandoffValidation` | valid receipt; authority mutation rejected |
| scoped problem | `ProblemContract` | empty scope rejected; authority retained |
| obligations | `Obligation` | satisfied obligation cannot retain blockers |
| honest terminals | `infer_terminal` | authority, non-identifiability, resource, solution |
| action selection | `ActionValue`, `select_actions` | hard-gate non-compensation; Pareto set |
| behavioural relation | `FiniteTransitionSystem`, `are_bisimilar` | remote-domain positive; same-topic negative |
| attribute indiscernibility | `indiscernibility_classes` | attribute-relative classes |
| safe abstraction | `safe_quotient` | current safe/future unsafe |
| Jump | `JumpTrigger`, `JumpProposal`, `assess_jump` | poor score/censor rejected; minimum level; donor tie |
| V1 parity | `CapabilityParityRecord` | deprecation requires protected evidence |
| saturation | `SaturationVector` | incomplete routes block saturation |
| donor reduction | `DomainProblem`, `reduce_donors` | absorb, strict gate, donor tie |
| evidence dependence | `EvidenceUnit`, `DependenceEdge` | correlated components; unknown disposition |
| reticulate provenance | `ReticulateProvenance` | multi-parent, component revocation, cycle rejection |
| performative evaluation | `EvaluationDeployment` | known shift; proxy regression; no-control unknown |
| comparability | `ComparabilityCertificate` | exact, partial, non-comparable |

## Test census

- 34 deterministic unit tests;
- no external network/model dependency;
- no test grants truth, novelty or adoption;
- positive and hostile known-answer cases;
- Python 3.12+ package semantics.

## Missing objects

- minimum distinguishing-probe solver;
- obligation dependency/selective reopening;
- partial-order workflow and conformance;
- decomposition/recomposition/gluing receipt;
- statistical experiment-comparison adapters;
- native-method plugin contract;
- research-opportunity candidate and agenda boundary;
- prospective benchmark freeze identities;
- physical instrument/measurement adapter;
- meta-solver revision/fresh-transfer receipt.

**Authority:** local engineering evidence only.

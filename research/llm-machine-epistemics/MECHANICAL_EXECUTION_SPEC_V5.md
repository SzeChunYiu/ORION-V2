# Mechanical Execution Spec V5 — Final Canonical Additions

**Issue:** #51  
**Authority:** current mechanical execution contract together with the exact algorithms in `MECHANICAL_EXECUTION_SPEC_V4.md`.  
**Rule:** V4's algorithms remain unchanged except where this file explicitly adds/changes checks. No scientific reasoning is delegated.

## 1. Canonical inputs updated

Use:

1. `CURRENT_RESEARCH_STATUS_V4.md`
2. `papers/llm-machine-epistemics/MANUSCRIPT_DRAFT_V4.md`
3. `papers/llm-machine-epistemics/CLAIM_LEDGER_V4.json`
4. `RESPONSIBILITY_DECISION_QUOTIENT_V2.md`
5. `JOINT_DYNAMIC_STATE_OPTIMIZATION_V1.md`
6. `RESPONSIBILITY_STATE_PHASE_THEORY_V1.md`
7. `EPISTEMIC_DEFICIENCY_DECOMPOSITION_V1.md`
8. `RESPONSIBILITY_UNIVERSALITY_BOUND_V1.md`
9. `NEAREST_WORK_PASS_03_DECISIONAL_STATES.md`
10. `HOSTILE_REVIEW_DECISION_MATRIX_V1.md`
11. `papers/llm-machine-epistemics/JMLR_SUBMISSION_GATE_V1.md`
12. V4 execution algorithms.

## 2. Additional theorem/check IDs

Add:

- `DS1_ZERO_EXTRA_STATE_IF_POLICY_FACTORS_THROUGH_SP`
- `DS2_POSITIVE_STATIC_COST_IFF_NO_SP_POLICY`
- `PH1_HORIZON_COST_MONOTONICITY`
- `PH2_FINITE_HORIZON_STABILIZATION`
- `PH3_RESPONSIBILITY_FAMILY_STATIC_DYNAMIC_MONOTONICITY`

J1–J5, R21–R27, U1–U5 and V4 IDs remain required.

## 3. Mandatory Brodu control

Construct finite fixtures in which responsibility optimal actions are deterministic functions of predictive-state class only.

Expected:

```text
C_stat^* = 0
```

for `ANY_OPTIMAL_ACTION`.

For fixed action/risk signatures measurable from `S_P`, conditional state cost must be zero.

This checks `DS1` and prevents a false claim that epistemic decisions always require state augmentation.

## 4. Cross-channel positive-cost fixture

Two equal-probability histories in one predictive fibre with disjoint unique responsibility actions caused by a registered history-side/provenance variable absent from `S_P`.

Expected:

```text
C_stat^* = 1 bit
```

and `DS2` must identify no common Bayes-optimal action/policy from `S_P`.

Future transition should preserve this action partition so the canonical P1 fixture has:

```text
C_inf^* = 1 bit
Omega_dyn = 0
```

## 5. P0/P1/P2 phase fixtures

### P0

Expected exact terminal:

```text
C0=0
Cinf=0
Omega=0
phase=P0_PREDICTIVE_DECISIONAL
```

### P1

Expected:

```text
C0=1 bit
Cinf=1 bit
Omega=0
phase=P1_STATIC_CROSS_CHANNEL
```

### P2 canonical

Expected:

```text
C0=0
Cinf=1 bit
Omega=1 bit
phase=P2_PROSPECTIVE_REFINEMENT
```

### Mixed P2 search

Search exact small systems for:

```text
C0>0
Omega>0
```

Freeze smallest witness if found. If absent within registered bound, `CANNOT_CHECK_NO_SMALL_MIXED_P2_WITNESS`.

Output `RESPONSIBILITY_STATE_PHASE_AUDIT_V1.json`.

## 6. Horizon curve

For each registered dynamic fixture, enumerate `k`-horizon admissible partitions as defined in `RESPONSIBILITY_STATE_PHASE_THEORY_V1.md`.

Compute:

- `C_k^*` for k=0..until stabilization;
- `Omega_k=C_k^*-C_0^*`;
- `K_epi=min{k:C_k^*=C_inf^*}`.

Verify:

```text
C_0 <= C_1 <= ... <= C_inf
Omega_0=0 <= Omega_1 <= ... <= Omega_inf
```

For finite fixtures, stop only after equality with independently computed V4 infinite/right-congruent optimum.

Output `RESPONSIBILITY_HORIZON_CURVE_V1.json`.

## 7. Responsibility-family monotonicity

For nested responsibility families using fixed exact semantics, compute static and dynamic minima and verify nondecreasing costs under family inclusion.

Output one:

- redundant responsibility with no cost increase;
- responsibility causing P0->P1 if available;
- responsibility causing P0/P1->P2 if available;
- saturation family reaching full non-predictive history bound.

## 8. Brodu 2011 theorem-location audit

Mandatory bibliography row(s) must verify from primary/full paper:

- causal-state equivalence;
- iso-prediction equivalence;
- iso-utility equivalence;
- decisional-state construction;
- causal states refine/sub-partition decisional states;
- discrete decisional complexity/information `D=H(omega)`;
- transition graph construction;
- whether decisional-state transition graph itself satisfies deterministic recursive sufficiency or can collapse distinguishable labeled transitions.

Citation:

Nicolas Brodu, _Reconstruction of Epsilon-Machines in Predictive Frameworks and Decisional States_, Advances in Complex Systems 14(5), 2011, DOI `10.1142/S0219525911003347`, arXiv:0902.0600.

Scientific disposition is already fixed: generic predictive+utility decision-state/complexity is parent-owned.

## 9. Additional ISFSM parent audit

Locate primary/reliable sources for:

- compatible states under incompletely specified outputs;
- compatibility non-transitivity;
- closed covers / prime compatibles;
- minimum ISFSM reduction complexity / NP-hardness where established;
- exact binate-cover or equivalent formulations.

This is metadata/theorem ownership only; no novelty response is delegated.

## 10. Claim matrix target

Use `CLAIM_LEDGER_V4.json` C01–C18.

The executor fills only:

- `PARENT_OWNED`
- `PARTIAL_OVERLAP`
- `NO_DIRECT_OVERLAP`
- `CANNOT_CHECK_FULL_TEXT`

plus exact theorem/definition location and assumptions.

## 11. Manuscript update

Starting manuscript is `MANUSCRIPT_DRAFT_V4.md`.

Do not use older manuscript drafts.

Mechanical edits only as in V4.

## 12. Final decision pressure

A positive JMLR terminal now specifically requires that the package

```text
cross-channel static state cost
+ joint Bayes-policy/recurrent-state optimum
+ dynamic optionality premium
+ P0/P1/P2 phase/horizon curve
+ LLM prospective representation audit
```

is not immediately reproduced by the strongest product of:

```text
Brodu decisional states
+ R-PSR / multi-task sufficiency
+ Approximate Information State / POMDP
+ ISFSM compatible-state minimization
+ standard information theory
```

If that product suffices, terminal is `CLASSICAL_PARENT_SUFFICIENT__MERGE_OR_DROP` even if every mechanical theorem passes.

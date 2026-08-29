# JMLR Gate Assessment V2

**Issue:** #51  
**Status date:** 2026-08-29  
**Supersedes:** the pre-mechanization interpretation of `JMLR_SUBMISSION_GATE_V1.md`.  
**Current submission authority:** `NO`.

## 1. Official criteria being applied

Current JMLR author guidance explicitly includes:

- theoretical studies yielding new insight into the design/behavior of learning systems;
- formalization of new learning tasks and methods for assessing performance;
- development of new analytical frameworks that advance theoretical studies of practical learning methods.

The same guidance requires theoretical papers to discuss practical utility, clearly situate predecessor contributions, and explain why the advance matters.

Current reviewer guidance asks whether the work is significant, technically correct, sufficiently different from prior work, adequately evaluated theoretically and/or empirically, practically useful where theoretical, and understandable to a broad ML reader.

Official sources:

- `https://www.jmlr.org/author-info.html`
- `https://jmlr.org/reviewer-guide.html`

The paper is therefore evaluated under two possible routes:

```text
J-A = NEW_THEOREM / NEW_STATE_THEORY
J-B = NEW_ASSESSMENT_TASK / ANALYTICAL_FRAMEWORK
```

J-A has been contracted. Only J-B remains live.

---

# 2. Gate table

| Gate | Requirement | Current status | Evidence / reason |
|---|---|---|---|
| J1 | Substantive residual after strongest-parent reconstruction | `OPEN_HIGH_RISK_FRAMEWORK_ONLY` | Pass 04 shows generic minimal predictive/decision/recurrent state is parent-owned. Surviving residual is prospective representation audit + conditional accounting, not new core state theory. |
| J2 | Clear ML consequence for representation/compression/evaluation | `PASS` | `PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V1.md` gives a concrete frozen-model/representation assessment method. |
| J3 | Formal/theoretical support complete enough for claims | `PASS_CORE__ONE_NONLOADBEARING_MECHANICAL_GAP` | 37/38 registered theorem rows mechanically supported; one T8D cardinality item is unmechanized and can be checked or deleted. Mixed-P2 remains an honest CANNOT_CHECK and is not a claimed theorem. |
| J4 | Theorem-level nearest-work saturation | `PASS_SUBSTANTIVE__BIBLIOGRAPHIC_BINDING_OPEN` | Pass 04 absorbs causal states, R-PSR, Brodu, AIS, POMDP, ISFSM, stable quotient 2026, retentive-complexity 2026, VE/VSRL, BAMDP epistemic abstraction, Belief-R. Exact BibTeX/theorem-number binding remains mechanical editorial work. |
| J5 | Practical utility / assessment prescription | `PASS` | The prospective revision audit specifies present-equivalence gates, P0/P1/P2 controls, update+maintain metrics, interventions, causal contrasts and falsifiers. |
| J6 | Broad ML readability without ORION-specific prerequisites | `PASS_DRAFT` | Manuscript V5 is written in standard predictive-state/decision/memory terms; Machine Epistemics is placed late as context rather than prerequisite vocabulary. |
| J7 | Concise and complete manuscript | `PARTIAL_EDITORIAL` | V5 has the substantive argument. Final bibliography, theorem numbering, generated tables and JMLR LaTeX remain. No new scientific design is needed. |
| J8 | Genuine contribution rather than survey/relabeling | `OPEN_DECISIVE_RISK` | This is the controlling gate. The mathematical substrate is heavily parent-owned. The paper survives only if the three-stage prospective representation audit is judged a meaningful new formal assessment framework rather than a direct application of information-state theory. |

---

# 3. Route J-A — new theorem / new state theory

## Verdict

`FAIL_CURRENT_IDENTITY`.

Reasons:

1. `S_P` is causal/predictive-state theory.
2. decision-relative compression is strongly covered by Brodu, decision theory, R-PSR, retentive complexity and value equivalence.
3. recurrent decision-sufficient state is strongly covered by POMDP/information state/AIS.
4. current compatibility + successor closure is classical ISFSM/right-congruence territory.
5. July 2026 stable-quotient work gives an especially close minimal recursive-state result.
6. the log-loss/capacity tradeoff is established rate-distortion/decision-aware modeling territory.

The paper should not be submitted to JMLR under a claim of foundational new minimal-state mathematics.

---

# 4. Route J-B — analytical framework / new assessment task

## Proposed contribution

> **Prospective Revision Audit:** after matching a representation on complete linguistic predictive adequacy and current responsibility adequacy, test whether later evidence reveals a state-retention failure that neither present metric could detect.

Supporting formal package:

- reference language state `S_P`;
- current responsibility regret/cost;
- prospective revision regret/cost;
- exact one-bit no-certification witness;
- `Omega_dyn` as a derived conditional accounting metric;
- P0/P1/P2 audit taxonomy;
- horizon curve;
- acquisition/current-compression/prospective deficit separation;
- bounded responsibility/horizon requirement.

Practical package:

- fully specified `PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V1.md`;
- mandatory Belief-R comparison;
- update and maintain controls;
- representation interventions after present-equivalence matching;
- source/provenance and selective-reopening examples;
- null/P0 controls in which extra memory is unnecessary.

## Current verdict

`OPEN_HIGH_RISK_BUT_DEFENSIBLE_ASSESSMENT_FRAMEWORK`.

The framework can plausibly fit JMLR's explicit scope for formalizing new learning tasks/methods of assessment. It is not yet safe to call J1/J8 passed because an editor could reasonably regard the audit as a straightforward specialization of existing decision-memory/information-state theory plus Belief-R.

---

# 5. What would make J-B strong enough?

No new open-ended theory is required. The strongest legitimate improvements are already specified:

1. **Make the no-certification proposition explicit.** Present prediction + current decision equality cannot certify future revision equality; use the mechanically checked one-bit witness.
2. **Use the audit as the paper object.** `RAP_k = (prediction deficiency, current responsibility regret, prospective revision regret, state cost)` should organize the manuscript.
3. **Directly compare with Belief-R.** Explain that Belief-R tests whether outputs update; #51 tests whether manipulated/compressed representations retain the information required to update after current performance has been matched.
4. **Directly compare with stable-quotient/information-state theory.** Concede that they solve recurrent state; explain that #51 uses that machinery to assess an autoregressive representation relative to a separate language-prediction reference channel.
5. **Keep P0 cases prominent.** The framework must show when extra state is unnecessary, otherwise it looks like advocacy for an architecture rather than an assessment method.
6. **Report mechanics as validation, not novelty.** The exhaustive partition/counterexample battery demonstrates the audit's finite semantics are internally correct.
7. **Do not manufacture an empirical LLM result.** The current paper can remain theoretical because JMLR permits theoretical and new-assessment-task contributions, but the abstract/title must not imply a measured hidden-state failure.

These are incorporated in Manuscript V5 and the protocol.

---

# 6. Current strongest hostile-editor forecast

A skeptical JMLR editor could say:

> The paper is technically careful and the audit is sensible, but all state constructions follow from mature decision/information-state theory; Belief-R already evaluates revision; the remaining difference is a particular matched-control protocol for LLM representations.

That objection is **not currently eliminated**.

The best response is not to claim deeper novelty. It is:

> Correct—the state-minimization substrate is parent-owned. The proposed contribution is a formal assessment task that distinguishes three representation obligations and proves why the third cannot be certified by the first two. JMLR explicitly includes formalization of new learning tasks and methods for assessing performance; the question is whether this audit is sufficiently useful and general for the ML audience.

If an independent hostile review still judges this delta too narrow, route away from JMLR.

---

# 7. Alternative venue routing

## TMLR

Current official TMLR acceptance criteria emphasize:

1. whether claims are supported by accurate, convincing evidence;
2. whether some of the TMLR audience would be interested in the findings.

They deliberately do not require the method itself to be sufficiently “novel” as an acceptance criterion.

Official sources:

- `https://jmlr.org/tmlr/acceptance-criteria.html`
- `https://www.jmlr.org/tmlr/editorial-policies.html`

Current fit:

`STRONGER_THAN_JMLR_IF_NOVELTY_GATE_FAILS`.

A mechanically audited representation-assessment framework with honest parent attribution is plausibly well matched to TMLR.

## Information-theoretic / formal venue

If the manuscript contracts back toward finite conditional state-cost results and drops the LLM assessment task, a specialist information/decision/state-representation venue is more honest than forcing JMLR breadth.

## Machine Epistemics flagship integration

If the audit is judged valuable but not independently paper-scale, merge it into the broader Machine Epistemics flagship as the internal-representation section. This is preferable to maintaining a manuscript zombie.

---

# 8. Current submission decision

```text
JMLR_NEW_THEOREM_ROUTE = FAIL
JMLR_ANALYTICAL_FRAMEWORK_ROUTE = OPEN_HIGH_RISK
J1 = OPEN_HIGH_RISK_FRAMEWORK_ONLY
J2 = PASS
J3 = PASS_CORE
J4 = PASS_SUBSTANTIVE__MECHANICAL_BIB_BINDING_OPEN
J5 = PASS
J6 = PASS_DRAFT
J7 = PARTIAL_EDITORIAL
J8 = OPEN_DECISIVE_RISK

JMLR_SUBMISSION_AUTHORIZED = NO
TMLR_ROUTE = STRONG_FALLBACK
FIELD_THEORY_ROUTE = AVAILABLE
FLAGSHIP_MERGE_ROUTE = AVAILABLE
```

The remaining uncertainty is editorial/scientific distinctness, not missing conceptual development.

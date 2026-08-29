# JMLR Submission Gate V1

**Issue:** #51  
**Checked:** 2026-08-29 against current JMLR author and reviewer guidance.  
**Official pages:**

- https://www.jmlr.org/author-info.html
- https://www.jmlr.org/reviewer-guide.html
- https://jmlr.org/format/authors-guide.html

## 1. Why JMLR remains a plausible primary target

JMLR's current scope explicitly includes:

- experimental and/or theoretical studies yielding new insight into the design and behavior of learning in intelligent systems;
- formalization of new learning tasks and methods for assessing them;
- new analytical frameworks that advance theoretical studies of practical learning methods.

A theory-only paper is therefore in scope **in principle**. JMLR also requires theoretical work to explain practical utility and why the result advances current understanding.

This is compatible with #51 only if the final paper changes how language-model representation/compression or state evaluation should be understood.

## 2. Current editorial threat

JMLR favors work of interest to a broader machine-learning audience and can reject work whose audience is too narrow. Its reviewer guidance asks whether a paper is a significant, technically correct contribution sufficiently different from prior published work and whether theoretical results have practical utility.

Therefore a correct paper consisting of:

- causal-state minimality;
- standard sufficient-statistic arguments;
- information-bottleneck compression;
- log-loss rate distortion;
- Myhill–Nerode/right congruence;

with “epistemic” terminology substituted in is **not JMLR-ready**.

## 3. Non-negotiable JMLR gates

### J1 — theorem residual

At least one load-bearing result must survive the strongest composition of:

- causal states / predictive-state representations;
- Reward-Predictive State Representations;
- Blackwell/statistical sufficiency;
- Deterministic Information Bottleneck / multi-task sufficiency;
- conditional log-loss rate-distortion;
- POMDP/information-state recursion;
- Myhill–Nerode/right-congruence state minimization;
- current LLM belief/truth/uncertainty representation work.

**FAIL J1** if a competent reviewer can obtain the full paper theorem package by direct substitution into one named parent theorem or an obvious two-parent composition.

### J2 — learning-system consequence

The paper must establish a concrete consequence for learning systems beyond philosophical terminology.

Current candidate consequence:

> Compression/distillation or representation objectives can preserve the complete linguistic predictive target and all current responsibility decisions while still losing information required for correct future revision after later evidence. Therefore evaluating a continually used autoregressive state requires a prospective responsibility criterion in addition to predictive loss and static probes.

This consequence must remain nontrivial after parent subtraction.

### J3 — formal support

Every theorem in the abstract/conclusion must be independently or mechanically checked under explicit assumptions. Hidden theorem assumptions are a submission blocker.

### J4 — nearest-work saturation

The theorem-level claim matrix must be complete enough that the hostile reviewer cannot identify an obvious missing direct parent from causal-state, task-state, information-state or automata theory.

### J5 — practical utility discussion

The paper must give a concrete evaluation/use prescription even without training a new model:

1. evaluate linguistic prediction;
2. evaluate current responsibility sufficiency;
3. evaluate prospective revision sufficiency under controlled future evidence;
4. report representation/state cost;
5. distinguish missing evidence from internal compression loss.

This is a theoretical design implication, not an empirical performance claim.

### J6 — broad ML readability

The manuscript must not require ORION vocabulary. Terms such as authority terminals, evidence ledgers or programme governance may appear only as motivating examples if needed; the theorem language must be standard probability/decision/state representation terminology.

### J7 — concise complete manuscript

JMLR says papers must be concise and complete. It notes that manuscripts longer than roughly 35 pages are harder to review and papers above 50 pages require justification and may be desk rejected.

Target for #51:

- main paper: **<= 30–35 JMLR pages**;
- proof/countermodel detail beyond that goes to an online appendix/supplement;
- no large ORION history section.

### J8 — theory paper, not hidden survey

JMLR does not accept unsolicited review/survey articles as a substitute for a research contribution. The extensive parent map must support a theorem paper; it cannot become the paper itself.

## 4. Submission decision

Submit to JMLR only if all of J1–J8 are `PASS`.

If J1/J2 fail but the mathematics remains correct and useful, route to the strongest suitable field-theory venue or merge into a broader ORION theoretical manuscript.

If J3 fails, do not submit anywhere until repaired or honestly terminated.

## 5. Current status before mechanical execution

```text
J1_THEOREM_RESIDUAL = OPEN_HIGH_RISK
J2_LEARNING_SYSTEM_CONSEQUENCE = CANDIDATE_DYNAMIC_PROSPECTIVE_STATE
J3_FORMAL_SUPPORT = OPEN_COMPUTE_HANDOFF
J4_NEAREST_WORK = OPEN_THEOREM_MATRIX
J5_PRACTICAL_UTILITY = DRAFTED
J6_BROAD_READABILITY = DRAFTED
J7_LENGTH = MANUSCRIPT_DRAFT_EXPECTED_WITHIN_TARGET_AFTER_LATEX
J8_NOT_SURVEY = PASS_BY_DESIGN
JMLR_SUBMISSION_AUTHORIZED = NO
```

## 6. Fallback routing

If the paper is mathematically sound but misses JMLR's significance/breadth gate:

- consider **Information and Inference** if the final contribution is primarily information-theoretic;
- consider **TMLR** if the result is a rigorous ML analytical framework with narrower novelty/significance;
- merge into the ORION-V2 flagship/foundation if standalone residual disappears.

No venue downgrade should be treated as theorem failure; no venue ambition should inflate the theorem.

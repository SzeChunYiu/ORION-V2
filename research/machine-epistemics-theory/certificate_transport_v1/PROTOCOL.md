# ME-CERTIFICATE-TRANSPORT-V1 — pre-execution specification

Date: 2026-09-04. Parent coordination: #197, #202, #203, #304, #313.
Baseline: ORION-V2 24566f00a9dc4425a438fcfac05d13c6b2d903db (#310).
Branch: research/me-certificate-transport-20260904.

This is a formal research and deterministic finite-calibration study, NOT a blinded or confirmatory empirical experiment. Mathematical targets were developed during source reading. This file is committed before executing its finite calibration. No protected outcomes, model jobs, OCM runtime, existing freezes, or manuscripts are changed. The foundation_v1 paths claimed by #312/#313 and decision_frontier_v1 paths claimed by #314 are read-only to this contribution. Exclusive new paths: this directory and .github/workflows/me-certificate-transport.yml.

## Question and finite access model

A risk certificate is about a specified failure event under a specified distribution, not a proof that an individual output is true. When an operator, its checker, or deployment distribution changes, what risk can actually be transported, and how much exact revalidation is needed?

Let X be an explicitly enumerated finite sample space; P its complete rational probability vector; F the reference failure set; U the set of atoms where a changed operator may alter the failure event; epsilon the total-variation budget; eta the reference-mass budget for event changes. All of these are public model inputs. Knowledge of P, F, and U is a substantive assumption; producing them, establishing closure, and certifying deployment drift are not free services supplied by this checker. The actual deployment distribution and failure event are adversarial members of the declared class.

Target 1: compute the exact maximum of Q(G) subject to TV(P,Q)<=epsilon, F symmetric_difference G subset U, and P(F symmetric_difference G)<=eta. Use TV=one half of the L1 distance. Give a matching attaining Q, including empty/full failure sets and zero-reference-mass atoms.

Target 2: for exact no-change audit results on A subset U, characterize the worst risk over all G agreeing with F outside U and on A. Derive the least audit cost / risk Pareto frontier under positive integer audit costs. Compare exhaustive audit subsets with a faithful 0/1-knapsack dynamic-programming parent. Audit results are exact pointwise observations, not a statistical sample or a claim of real-model validity.

Target 3: define complete subject/claim/configuration binding and typed result projection. Missing semantic or drift evidence must remain CANNOT_CHECK. A model calculation, signature, identifier or scoped risk bound must never grant exact truth, external action authority, or OCM adoption.

## Proof and falsifier targets

CT-01: typed certificate applicability and the identity-versus-validity boundary.
CT-02: sharp total-variation bound for a fixed finite failure event, with an attaining distribution.
CT-03: exact joint distribution/event-change frontier; finite atom granularity can make the additive upper bound loose.
CT-04: exact no-change-audit frontier and indistinguishable-world lower witness.
CT-05: knapsack reduction and resource accounting, including zero-mass support ties.
CT-06: monotonicity, revocation of audits, and conservative selective invalidation.
CT-07: drift/event transport composition under common-domain, fixed-event hypotheses; adaptive selection is a separate assumption.
CT-08: falsifiers for transporting from metadata alone, omitted drift, omitted event changes, and sample-versus-population substitution.

Each eventual claim row must separate written proof, finite calibration, parent ownership, independent review, implementation integration, and remaining research. Parent-owned is an acceptable result. No novelty or superiority claim is a target.

## Frozen finite calibration

Primary simplex: all rational P on three atoms with denominator 3 (10 distributions, including zero masses). Enumerate all 8 F and all 8 U, epsilon in {0,1/3,2/3,1}, eta in {0,1/3,2/3,1}: 10,240 joint-frontier cells. Independent oracle directly enumerates all G and all Q on the same simplex, without using the analytic bound. The attaining-distribution proof explains why this grid suffices for these grid-valued inputs; it is not evidence for unbounded cases.

Audit comparison: same P/F/U/epsilon universe; costs (1,1,1) at budgets 0..3 and (1,2,3) at budgets 0..6. Compare all audit subsets with the faithful dynamic-programming parent; expected 28,160 paired cells. Include explicit zero-mass, empty/full event, no-change, and revoked-audit witnesses.

Controls must detect: ignored distribution shift; ignored event-change budget; ignored mutable set; TV without the factor 1/2; false exactness from a fractional relaxation; zero-mass error treated as impossible under drift; metadata drift left bound; incomplete manifest; invalid probability/mask/budget; replay/report drift. Every control needs an applied mutation and a no-alarm counterpart. Counts must be recomputed, never hard-coded as successful results.

## Resources and execution

stdlib-only exact rational arithmetic; bounded enumeration, explicit refusal above the registered implementation cap; integer costs for the DP parent. Record candidate masks, oracle comparisons, audit-subset and DP work, interpreter, platform, commands, elapsed time, code hashes, and exact result hash. Do not call an exponential algorithm efficient or conceal full error-table/oracle construction costs. Local small checks may run in this session's isolated Linux container; this is not a Mac/laptop/LUNARC protected run.

## Review roles and independence

Formal semantics: proposition types and scope. Probability/robust optimization: sharp bounds and countermodels. Algorithms: attaining constructions, knapsack parent and cost. Systems/refinement: binding, invalidation and replay. Hostile evaluator: boundary cases and overclaim rejection. These are analytic roles in one authoring session, not independent experts, additional workers, or an independent review terminal.

## Exit

Deliver theory, exact code, independent-formulation finite oracle, mutations/tests, source/claim ledger, immutable receipt, OCM absorption requirements and a draft PR against main. Report PARENT_OWNED / CORRECTED_FOUNDATION_FRAGMENT / REFUTED_TARGET / CANNOT_CHECK as earned. Do not close #197, #200..205, #245, #312/#313/#314, any OCM milestone, or the overall scientific foundation.
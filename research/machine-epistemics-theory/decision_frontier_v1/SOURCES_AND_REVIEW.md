# Parent reconstruction and review boundary

Identity: ME-DECISION-FRONTIER-V1 / ORION-V2 #314, 2026-09-04.

## Primary parent actually read

Shervin Javdani, Yuxin Chen, Amin Karbasi, Andreas Krause, Drew Bagnell, and Siddhartha Srinivasa (2014), **Near Optimal Bayesian Active Learning for Decision Making**, AISTATS, PMLR 33, pp. 430–438.

Landing: https://proceedings.mlr.press/v33/javdani14.html
Paper: https://proceedings.mlr.press/v33/javdani14.pdf
Extended manuscript: https://arxiv.org/abs/1402.5886

Read the formal problem in §2 (pp. 431–432), its deterministic test/observation and hypothesis-consistency definitions, the overlapping decision-region discussion, and the HEC construction/results in §3 (pp. 432–434). PDF pages 1–3 (zero-based) were also inspected visually. The paper's objective averages test cost over a hypothesis prior; §2 allows test costs to be generalized. Its expected-cost approximation theorem does NOT automatically imply our worst-case bounds.

### Exact symbol mapping

| This package | DRD parent | Consequence |
|---|---|---|
| finite worlds `W` | hypotheses `H` | Finite possible-state model, not real-world closure |
| queries `Q`, total outcomes `o_q` | tests `T`, deterministic `g_t` | Outcome consistency defines remaining hypotheses |
| belief `B` | version space `V(S)` | All worlds compatible with observations |
| action region `R_a={w:a∈G(w)}` | decision region `r∈R` | Regions can overlap |
| `Safe(B)≠∅` | `B⊆r` for some decision region | A decision can be justified before identifying the world |
| `V(B)` | expected-cost objective in parent | Our objective is instead exact worst-case total cost |
| obstruction class | unseparable hypotheses under tests | A registered observation limitation, not general scientific impossibility |

**Ownership:** the core scientific object is parent-owned. Minimax Bellman recursion, common-action intersection, set covers and deterministic partition factorization are elementary parent constructions. This package makes their assumptions, cost/revision boundary and executable finite witnesses explicit for the ME/OCM programme. It does not establish priority for any new theorem.

## Adjacent parent checked only at the abstract/metadata level

Su Jia, Fatemeh Navidi, Viswanath Nagarajan, and R. Ravi (2024), **Optimal Decision Tree and Adaptive Submodular Ranking with Noisy Outcomes**, JMLR 25(382), pp. 1–42.

https://www.jmlr.org/papers/v25/23-1484.html

This is a relevant stronger parent for a noisy-channel successor. Only its public abstract/metadata were inspected in this session. No noise theorem, approximation factor or lower bound from it is imported. Full proof reconstruction is a prerequisite to any noise-regime comparison.

## Claim ownership and evidence levels

| IDs | Basis | Evidence in this package | Not established |
|---|---|---|---|
| DF-00, DF-01 | DRD regions and indistinguishability | Written proof; exact finite table/tree checks | Complete/open-world channel validity |
| DF-02, DF-03 | Decision-tree Bellman induction | Written lower/upper argument; distinct tree enumerator and bottom-up certificate checker | Practical optimal synthesis at scale |
| DF-04 | Set inclusion and policy restriction | Written proof; subset checks; revoked-observation witness | Efficient incremental recertification |
| DF-05 | Overlapping regions and partition order | Explicit three-world counterexample | Refutation of exact-function/signature quotients |
| DF-06, DF-07 | Set cover and encoder partitions | Written characterization; finite cover/frontier equality | Free history acquisition or lower whole-system cost |
| DF-08, DF-09 | Product decision trees / shared-interface projections | Written proofs; independent/correlated controls | Addition of dependent testimony/evidence |
| DF-10 | Proper-subset rank | Written path bound and explicit exponential costs | Noisy/continuous/self-modifying termination |
| DF-11 | Signal-factorized deterministic encoder | Written proof; identity/partial/constant signal controls | Acquiring the registered signal from raw language |

The finite universe contains exactly 5,488 models. Full table/tree agreement is calibration; the written induction arguments carry the arbitrary-finite-size statements. There is no Lean/Coq/Isabelle proof in this package.

## Five internal analytic roles and their dispositions

These are explicitly roles in ONE authoring session, not people, recruited specialists, subagents, independent replication or external approval.

**Formal epistemics:** required nonempty belief sets, action-relative rather than truth-granting semantics, complete observation tables, and a boundary between scoped obstruction and general Jump necessity. The three-way distinction among impossible / over budget / cannot check survives every theorem.

**Decision-tree/complexity theory:** reconstructed the DRD parent; kept expected and worst-case objectives separate; demanded matching lower and upper witnesses; replaced a unique-coarsest-quotient assumption with the correct set-cover characterization when actions overlap. No asymptotic complexity class is asserted solely from enumeration.

**Control/learning:** checked that extra valid observations cannot raise optimal cost, and that evidence removal can reopen decisions. Required both the independent-factor direct sum and a correlated counterexample. Corrected the comparison interface: a factor cannot be denied a cheap shared test when the joint task receives it.

**Systems/refinement:** bound every finite semantic/cost/source/epoch coordinate; required all branches, complete certificate domains and exact rational arithmetic. Added missing-closure and capacity exits. Identified the remaining trust boundary: a caller-supplied closure string is not an externally verified attestation, nor is a source name an implementation fingerprint for an actual backend.

**Hostile evaluation:** attempted unsafe leaves, omitted/duplicate branches, optimistic certificate values, omitted certificate cells, semantic drift, empty beliefs, model omission, noisy observations, false pairwise sufficiency, and unobserved-world encoders. The model-omission and noisy-observation cases are preserved as failures of load-bearing assumptions, NOT falsely counted as defects the reference can detect. DF-11 was added by a written factorization argument, then tested on identity/partial/constant signals; it was not selected from protected empirical outcomes.

## External review state

`INDEPENDENT_ASSUMPTION_REVIEW = NOT_OBTAINED`.
`PROOF_ASSISTANT_VERIFICATION = NOT_RUN`.
`PRIORITY_SEARCH_SATURATION = NOT_ESTABLISHED`.
`OCM_RUNTIME_PARITY = NOT_RUN`.

A second implementation written by the same session is a different computational check, not independent scientific custody. No votes, role agreement or green tests grant scientific/field/publication authority.

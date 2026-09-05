# Native interfaces and composition conditions

This document is an integration contract over the imported reference studies.
It makes no new theorem or runtime-adoption claim. Each row points to the native
formal object and identifies the distinction an adapter must preserve.

| Mechanism | Native object | Required composition condition |
| --- | --- | --- |
| Warrant and revocation | #321 set antichains; #323 and #328 bit-mask antichains | Register one finite evidence alphabet. Convert `available = universe XOR revoked` only within that alphabet. Preserve lower/upper interval order and support status. |
| Nogood composition | #321/#323/#328 corrected conjunction | Filter after combining supports. Two separately live supports may be jointly inconsistent; do not combine status labels alone. |
| Graded knowledge navigation | #323/#328 rational fixed-point systems | Preserve seed, restart, transition matrix and normalization identity. A representation change needs its own sufficiency/transport premise. |
| Query and memory optimization | #320 complete finite decision model and Bellman certificate | Preserve admissible decisions, observation interface, world closure premise and resource budget; an encoder may retain only distinctions it acquired. |
| Certificate lifecycle | #322 typed certificate registry, grounded fixed point and generation-bound transitions | Preserve statement/subject/kind, complete dependency identity, alternate support, trusted roots and external checkpoint. Applicability is not external permission. |
| Revision and time | #326 state transitions and temporal validity | Preserve epoch, full obligation signature, snapshot and revision identities. A liveness-only cache does not establish unchanged contents. |
| Causal evidence | #325/#327 finite causal models and compatible classes | Keep observation, intervention and factual-world counterfactual queries distinct. Preserve unidentified and inconsistent compatible classes. |
| Risk transport and auditing | #327 common-mass transport; #331 finite event/audit frontiers | Bind a common alphabet/event semantics and the actual distribution/operator drift assumptions. Fixed-event, joint-event and sampling statements have different inputs. |
| Absorption | Canonical #324 registry plus each study's OCM contract | Bind source row, exact source identity, scoped terminal, parent ownership, parity evidence and reopen conditions. External admission remains separate. |

## Optimization routes already present

Use the strongest applicable native mechanism under its registered assumptions:

1. Query-relative agreement can avoid requiring a uniquely identified full
   hypothesis. Its certificate must still cover the actual query and revision
   families. Do not replace an absent upper witness with a negative answer.
2. Decision-frontier dynamic programming and the memory/query frontier expose
   exact bounded tradeoffs. They are finite reference optimizers with explicit
   exponential search/certificate costs; the result does not establish practical
   scalability for an unbounded knowledge space.
3. Complete dependency indexes can restrict candidate recertification to the
   affected cone, while alternate-support checking avoids unnecessary retraction.
   The cone is an over-approximation of candidates, not proof that every item
   must be retracted. Semantic changes require richer signatures than liveness.
4. Fixed normalization supports the stated monotonicity and perturbation bounds.
   Residual certificates can justify a scoped stopping decision where their
   premises hold. Revoking an edge after changing denominators need not recover
   the old state; normalization identity must be restored or revalidated.
5. The certificate-transport audit/knapsack reference exposes a bounded
   audit-cost/risk frontier. Joint audit benefits can be supermodular; a policy
   justified only by individual benefits can miss valuable combinations.
6. Common-mass transport can improve an additive risk bound when its stronger
   paired-law assumptions are available. A sharper numeric bound is not evidence
   that those assumptions hold for the actual deployment.

Each proposed OCM use must account for acquisition, model construction, indexing,
encoding, synthesis, verifier work, retained history, drift checks and external
effects. A smaller answer object does not erase the cost of creating or
revalidating its certificate.

## Scope preserved by the conformance suite

The integration suite compares native implementations only on explicitly shared
finite inputs. It supplies no generic certificate-type conversion, universal
causal identification, learned topology optimizer, unbounded exact solver or
production transaction fence. Those need their own identified model, theorem,
falsifier, executable route and admission evidence. The authoritative registry
continues to distinguish `OPEN`, `CANNOT_CHECK`, finite calibration and scoped
proofs instead of collapsing them to an integration-success label.

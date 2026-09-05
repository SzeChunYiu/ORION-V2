# Source and parent ledger

Read in this authoring session on 2026-09-05 (session clock reports September 4 UTC).
Scope is a targeted primary-source reconstruction, NOT a saturated novelty search.
Only the portions named below were used. No inaccessible source is labelled verified.
The explanatory proofs in THEORY.md instantiate these parent ideas on this package's
registered finite state; they do not establish an independent field or new theorem priority.

| id | primary source and location | reconstructed ownership / boundary |
|---|---|---|
| P1 | Berenson, Bernstein, Gray, Melton, O'Neil & O'Neil (1995), *A Critique of ANSI SQL Isolation Levels*, MSR-TR-95-51; author/institution PDF https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf | Write skew and predicate/phantom anomalies, pp. 8–10, inspected as text and page image. Immutable snapshot reads do not generally serialize multi-object decisions. No OCM-specific residual is assigned to this observation. |
| P2 | Herlihy & Wing (1990), *Linearizability: A Correctness Condition for Concurrent Objects*, author PDF https://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf | §§2.2, 3.3, 4: real-time-respecting object histories and refinement; serializability distinctions. Atomic per-cell reads do not by themselves implement our multi-cell guard-and-commit operation. Safety is distinct from progress. |
| P3 | Saltzer & Schroeder (1975), *The Protection of Information in Computer Systems*, author text https://web.mit.edu/Saltzer/www/publications/protection/Basic.html | Design principles: fail-safe defaults and complete mediation, explicitly including cached permission invalidation. Supplies the prior-authority/control parent, not an empirical guarantee about arbitrary software. |
| P4 | Gilbert & Lynch (2002), *Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services*, author PDF https://www.comp.nus.edu.sg/~gilbert/pubs/BrewersConjecture-SigAct.pdf | §2 and §3.1 Theorem 1, including its indistinguishable-execution proof, read as text and theorem page image. Our R5 is a revocation-specific consequence with explicitly non-abstaining availability. A terminal CANNOT_CHECK is not silently equated with their service availability. |
| P5 | Chandy & Lamport (1985), *Distributed Snapshots: Determining Global States of Distributed Systems*, author PDF https://lamport.azurewebsites.net/pubs/chandy.pdf | §§3–5, consistent recording, Theorem 1 and stable predicates. Snapshot may correspond to a reordered computation rather than a literal simultaneous recorded state. Their message-channel algorithm assumes more than our finite DAG lemma; we do not claim to implement it. |
| P6 | Saltzer, Reed & Clark (1984), *End-to-End Arguments in System Design*, author PDF https://web.mit.edu/Saltzer/www/publications/endtoend/endtoend.pdf | Delivery guarantees, duplicate suppression and transaction management, author PDF pp. 5–7. Transport delivery is not application effect completion; application retries can duplicate effects. R8 is a small explicit indistinguishability witness, not a new exactly-once protocol. |

Additional candidate checked but not used as a verified full-text parent: Kung & Robinson
(1981), *On Optimistic Methods for Concurrency Control*, CMU publication listing and DOI
10.1145/319566.319567. The linked PDF fetch failed in this environment. Its specific
algorithms are not claimed reconstructed. `parent_validate` is our straightforward
read-set validation implementation, not a purported native reproduction of that paper.

## Repository sources

Canonical atlas: `../ME_THEORY_GAP_ATLAS_V1.md` at
`24566f00a9dc4425a438fcfac05d13c6b2d903db`, Git blob
`9bb8943f88f1096265c7156be520300d340f0a71`. MEG-30 serializability subclaim is the exact
refutation target. No original atlas bytes or frozen terminal were changed.

Issue #304 defines V2 science versus OCM machine ownership. #312/#313 already own
`foundation_v1`; #314 owns `decision_frontier_v1`. Their work was not counted as completed
or independently verified here. The prior chat's MEG-absence report is superseded by
merged #310; this study starts from that merged atlas, not an assumed missing theory.

## Subtraction

R1 is elementary fibre factorization, not a novelty claim. R2–R4 adopt transactional
validation and complete mediation. R5 uses asynchronous indistinguishability. R6 combines
content binding, deterministic replay and the same knowledge boundary. R7 is causal-order
closure. R8 uses end-to-end effect acknowledgement and indistinguishability. The candidate
and parent validation paths receive identical synthetic records, state, budget and
freshness premise. Their finite agreement earns only PARENT_SUFFICIENT within this model.

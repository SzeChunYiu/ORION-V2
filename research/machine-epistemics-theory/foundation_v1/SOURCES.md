# Primary-source and parent-ownership ledger

Search/access date: 2026-09-04. Search is targeted, not literature saturation. Exact propositions in `THEORY.md` have self-contained arguments; no inaccessible source is treated as proof authority. Titles below are references, not quotations. No source is represented as independently reviewing ORION.

## Inspected primary material

**S1 — Green, Karvounarakis and Tannen (2007), Provenance Semirings, PODS.**
Author-hosted full text: https://www.cs.ucdavis.edu/~green/papers/pods07.pdf
Inspected the positive-relational homomorphism results, especially Propositions 3.5/4.2 and Theorem 4.3, plus the separate recursion conditions. Owns the provenance-substitution parent. Our support antichains use an idempotent Boolean instance; the general provenance framework is not assumed idempotent. We do not import unrestricted cyclic recursion from the finite positive case.

**S3 — Barber, Candes, Ramdas and Tibshirani, The Limits of Distribution-Free Conditional Predictive Inference.**
Full text version inspected: https://arxiv.org/pdf/1903.04684 (v2, 2020-04-15).
Inspected marginal versus conditional coverage definitions, the split-conformal finite-sample rank construction, and Lemma 1's restricted-subset argument. Owns the distinction and the elementary alpha/pi selection bound. Scope includes randomness over calibration/training samples; that is not the same as conditional validity after a particular calibration dataset has been observed. This packet does not claim a new conformal method or evade conditional-coverage impossibility results.

**S4 — Howard, Ramdas, McAuliffe and Sekhon (2021), Time-Uniform, Nonparametric, Nonasymptotic Confidence Sequences.**
Full text: https://arxiv.org/pdf/1810.08240
Inspected time-uniform guarantees, optional-stopping discussion and the event/coverage equivalence discussion. Owns important anytime-valid parents. T05 uses only a self-contained union-bound/tower-property argument, not an unverified implementation of their stronger confidence sequences.

**S6 — Berenson, Bernstein, Gray, Melton, O'Neil and O'Neil (1995), A Critique of ANSI SQL Isolation Levels, SIGMOD.**
Author paper: https://arxiv.org/pdf/cs/0701157
Publisher/author institution metadata: https://www.microsoft.com/en-us/research/publication/a-critique-of-ansi-sql-isolation-levels/
Inspected snapshot isolation and the A5B write-skew discussion. Owns the counterexample to immutable snapshots implying serializability. Our two-coordinate example is a finite mathematical illustration, not a test of a deployed database.

## Partial-access or background parents: not certified full-text reconstructions

**S2 — de Kleer (1986), An Assumption-Based TMS, Artificial Intelligence 28(2), 127-162.**
DOI: https://doi.org/10.1016/0004-3702(86)90080-9
Publisher metadata/abstract checked; original full text was not obtained in this session. ATMS labels and nogoods are inherited parent ownership from the repository. T02 supplies its own finite-set proof instead of claiming that an unread theorem was reconstructed. Current-source full-text fidelity audit remains open.

**S5 — Karampatziakis, Mineiro and Ramdas (2021), Off-Policy Confidence Sequences, ICML/PMLR 139, 5301-5310.**
Official page: https://proceedings.mlr.press/v139/karampatziakis21a.html
Metadata and abstract inspected; detailed proof not reconstructed. A strongest-parent lead for sequential policy deployment, not authority for an unproved adaptive OCM advantage.

**S7 — Andersen, Chung and Lang, personalized-PageRank local partitioning.**
Primary article lead: https://www.internetmathematicsjournal.com/article/1451-local-partitioning-for-directed-graphs-using-pagerank
PageRank/local-partitioning parent identified. No claim that this session reconstructed all complexity theorems. T07 instead proves the needed resolvent, contraction and perturbation statements directly. Positive linear algebra is the parent, not a new theory of warrant.

**S8 — Chitra and Raphael (2019), Random Walks on Hypergraphs with Edge-Dependent Vertex Weights, ICML/PMLR 97.**
Official page: https://proceedings.mlr.press/v97/chitra19a.html
Metadata/abstract inspected; no complete theorem reconstruction. The venue is ICML, not NeurIPS. An applicable hypergraph implementation still needs to prove the substochastic and normalization premises of T07.

**S9 — Version-space and agreement-region learning.**
Repository primary-parent lineage: ORION-V2 `research/orion-machine/theory/OCM_LANE_200_TERMINAL_V1.md`, the lane-200/201 receipts, and the gap atlas's Mitchell/Angluin/KWIK rows. These identify parent ownership, not a new external literature audit. T12 is a self-contained finite-class argument. Original full-text source reconstruction for the exact acquisition/access-model comparison remains OPEN. No sample-complexity or language-identification theorem is imported from a citation alone.

## Recent frontier leads: abstract-only, not novelty clearance

**S10 — Tibshirani, Barber and Ramdas (2026), Conformal Prediction Through the Lens of Hypothesis Testing: Universality, Impossibility, and Optimality.**
https://arxiv.org/abs/2608.27310 (submitted 2026-08-27).
Abstract/search record inspected; full text was not retrieved. This is a material modern parent for any proposed new statistical-epistemics claim. It cannot be silently counted as a completed novelty search or complete theorem comparison.

**S11 — Wei and Yang (2026), A Simple Active-Set Method for PageRank-Based Local Graph Clustering.**
https://arxiv.org/abs/2608.16339 (submitted 2026-08-17).
Abstract/search record inspected; full proof not retrieved. A relevant efficiency parent, but its assumptions must be matched before transfer to directed, dynamically warranted hypergraphs.

## Toolchain identity

**S12 — Lean 4.19.0 official release.**
https://github.com/leanprover/lean4/releases/tag/v4.19.0
Official release API inspected. Linux archive asset ID 250981932, name `lean-4.19.0-linux.tar.zst`, size 343842845 bytes. The API's digest field is null: no trusted archive SHA-256 was obtained. The CI bootstrap pins this release/asset size and records the downloaded archive hash; it does not pretend that size is cryptographic authentication. Lean/kernel and release custody remain explicit trusted dependencies. This version is a reproducibility pin, not a claim to be the latest Lean.

## Source-to-claim rule

S1 supports T01 and the algebraic parent of T02/T12. S3 supports the statistics ownership in T04. S4/S5 identify sequential parents for T05/T16. S6 supports T11's isolation distinction. T03, T06-T10 and T13-T16 also have elementary proofs stated in full; source ownership and theorem correctness are separate questions. Abstract-only leads cannot grant priority, asymptotic performance or an implementation refinement certificate.

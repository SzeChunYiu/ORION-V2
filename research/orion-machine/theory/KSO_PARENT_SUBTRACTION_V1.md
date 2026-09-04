# KSO parent subtraction V1 — strongest known mathematics first

Status: **M0 research dependency map; no novelty or superiority claim.**  
Umbrella: #194 · execution master: #197 · prototype: #284 · stacked implementation branch: `research/ocm-kso-math-v1-20260904`.

The KSO is not allowed to win by renaming a graph, a truth-maintenance system, PageRank, a program algebra, a sheaf, or graph rewriting. This file assigns first right of refusal to the strongest parent object for each mechanism and states what, if anything, remains as an OCM coupling question.

## Expert cells used for this subtraction

- **X-KS1 higher-order networks / stochastic processes** — hypergraphs, Markov chains, local diffusion.
- **X-KS2 compositional mathematics / programming languages** — monoidal categories, operads, Kleene algebra, typed procedures.
- **X-KS3 epistemics / provenance** — ATMS, provenance semirings, proof-carrying computation.
- **X-KS4 local-to-global / representation** — presheaves, sheaves, lumpability, quotient dynamics.
- **X-KS5 dynamic structure** — Petri nets, algebraic graph transformation, DPO rewriting, concurrency.
- **X-KS6 learning / self-extension** — program induction, library learning, meta-learning, self-rewrite.
- **X-KS7 decision / experimentation** — value of information, Bayesian experimental design.
- **X-KS8 hostile parent referee** — assumes the faithful product of all rows below and attempts to absorb the KSO completely.

## Parent table

| KSO mechanic | strongest parent / primary source | what the parent already owns | adopted KSO rule | residual status |
|---|---|---|---|---|
| Minimal sufficient warrant sets and exact retraction | de Kleer, **An assumption-based TMS**, *Artificial Intelligence* 28(2), 1986, DOI `10.1016/0004-3702(86)90080-9` | assumption-set labels, simultaneous alternatives, retraction/context switching | KSO node/edge warrant is an ATMS-style antichain; do not rename it | `PARENT_OWNED` |
| Compositional provenance annotations | Green, Karvounarakis & Tannen, **Provenance Semirings**, PODS 2007, DOI `10.1145/1265530.1265535` | semiring propagation of annotations/provenance through composition | use an idempotent antichain semiring for alternative/conjunctive warrant | algebra parent-owned; KSO binds it to live cognitive dynamics |
| Higher-order relations and random walks | Chitra & Raphael, **Random Walks on Hypergraphs with Edge-Dependent Vertex Weights**, ICML 2019, PMLR 97 | hypergraph random walks, Laplacian, mixing, conditions where hypergraph walk collapses to graph walk | KSO substrate is a typed directed hypergraph; higher-order relation is not encoded as unrelated pairwise edges | `PARENT_OWNED` for walk mathematics |
| Seeded/local graph navigation | Andersen, Chung & Lang, **Local Graph Partitioning using PageRank Vectors**, FOCS 2006, DOI `10.1109/FOCS.2006.44` and classical personalized PageRank | restart-biased local diffusion from seeds | query atoms define restart distribution; M0 uses a substochastic restart operator | `PARENT_OWNED` |
| Nontrivial typed local diffusion | Bodnar et al., **Neural Sheaf Diffusion**, NeurIPS 2022 | sheaf-valued diffusion, heterogeneous local transport, control of oversmoothing/heterophily | richer learned transports may replace scalar KSO edge weights only after scalar M0 is calibrated | `PARENT_OWNED`; optional successor |
| Local-to-global consistency | Robinson, **Sheaves are the canonical data structure for sensor integration**, *Information Fusion* 36, 2017, DOI `10.1016/j.inffus.2016.12.002`; Hansen & Ghrist, **Toward a spectral theory of cellular sheaves**, 2019, DOI `10.1007/s41468-019-00038-7` | restriction maps, consistency/global-section questions, sheaf Laplacian/cohomological obstructions | keep the existing ORION atlas presheaf-like; a global claim needs a separate gluing witness | `PARENT_OWNED` |
| Procedure/control algebra | Kozen, **Kleene algebra with tests**, TOPLAS 19(3), 1997, DOI `10.1145/256167.256195` | equational algebra for sequencing, choice, tests and iteration of programs | procedure language should reuse KAT-like laws rather than inventing control-flow algebra | `PARENT_OWNED` |
| Wiring/composition of multi-input operators | Fong & Spivak, **An Invitation to Applied Category Theory**, 2019, Ch. 6; hypergraph categories / operads | typed wiring diagrams, substitution, compositional network semantics | KSO hyperedges/operators use typed ports; composition is a wiring operation with separate warrant/resource decoration | `PARENT_OWNED` |
| Concurrent enable/fire semantics | classical Petri-net theory; Reisig, **Petri Nets: An Introduction** | conjunctive preconditions, firing, resources/concurrency | navigation and execution are distinct: navigation may traverse a relation; an executable hyperedge fires only when all preconditions are live/enabled | `PARENT_OWNED` |
| Extracting a compact connected clue subgraph | prize-collecting Steiner tree / network design; Goemans–Williamson family | connected prize-cost optimization and approximation | M2 extraction is a prize-collecting connected-subgraph problem; exact only on bounded domains | `PARENT_OWNED`; do not claim extraction algorithm novelty |
| Safe representation quotient of navigation | Kemeny–Snell lumpability | necessary/sufficient equality of block-transition probabilities for a Markov quotient | KSO compression must satisfy navigation lumpability **and separately** warrant measurability | dynamic quotient parent-owned; conjunction with warrant is integration |
| Structural graph self-modification | Lack & Sobociński, **Adhesive and quasiadhesive categories**, RAIRO 39(3), 2005, DOI `10.1051/ita:2005028`; DPO graph transformation | well-behaved pushout-based graph rewrite; typed/attributed graphical structures | Jump is a governed typed rewrite with protected interface, correspondence, impact/reopen set and rollback | rewrite mathematics parent-owned |
| Proof-bearing executable admission | Necula, **Proof-Carrying Code**, POPL 1997, DOI `10.1145/263699.263712` | producer supplies proof; host checks against a declared policy before execution | executable learned operators require a checkable certificate at the authority boundary | `PARENT_OWNED` |
| Procedure/library induction and consolidation | DreamCoder (Ellis et al., 2021) and LILO (Grand et al., arXiv:2310.19791) | program search, abstraction/library learning, compression/reuse, language-assisted library documentation | KSO consolidation may compress repeated procedure subgraphs; this is not itself novel | `PARENT_OWNED`; must outperform/match faithful library learner to claim residual |
| Formal-math search with symbolic checking | AlphaGeometry, *Nature* 625 (2024), DOI `10.1038/s41586-023-06747-5`; AlphaGeometry2, JMLR 26 (2025) | learned guidance plus symbolic deduction; auxiliary construction search; machine-checkable math | M6 must compare against strong neuro-symbolic theorem-proving/search parents; proof checker is not KSO novelty | `PARENT_OWNED` for solver pattern |
| Self-rewriting based on proof of utility | Schmidhuber, **Gödel Machines**, arXiv `cs/0309048` / 2007 chapter | self-referential proof-based code rewrite under encoded utility axioms | KSO J6/J7 self-revision cannot be advertised as new merely because it rewrites itself | `PARENT_OWNED`; ORION adds external authority/reopen obligations only if irreducible |
| Choosing the universally “best” learner/search policy | Wolpert & Macready, **No Free Lunch Theorems for Optimization**, IEEE TEC 1(1), 1997, DOI `10.1109/4235.585893` | no algorithm dominates uniformly over all problems under the theorem's symmetry assumptions | OCM must discover **context-relative** policies; “globally best intelligence form” is not a valid unconditional target | universal-best claim killed |
| Information-seeking action | Howard, **Information Value Theory**, IEEE TSSC 2(1), 1966, DOI `10.1109/TSSC.1966.300074`; Rainforth et al., **Modern Bayesian Experimental Design**, *Statistical Science* 39(1), 2024, DOI `10.1214/23-STS915` | value of information / decision-aware experiment selection | acquisition should optimize downstream decision value minus cost/risk, not raw entropy reduction | `PARENT_OWNED` |

## Strongest faithful parent product

The hostile comparator for KSO is therefore not a plain knowledge graph. It is at least:

```text
typed hypergraph
+ restart/local hypergraph navigation
+ optional learned sheaf transports
+ ATMS / provenance labels
+ KAT / typed operator composition
+ Petri-style conjunctive firing
+ connected-subgraph extraction
+ Markov-lumpable representation compression
+ DPO graph rewriting
+ proof-carrying admission / external verifier
+ DreamCoder/LILO-style library learning
+ active experiment selection
+ the same memory, tools, proof assistant, resources and codec access
```

A KSO theorem that disappears against this product is `PARENT_SUFFICIENT`, not a KSO residual.

## What may remain genuinely ORION-specific enough to investigate

The remaining research question is the **coupling**, not any row in isolation:

1. a cognitive diffusion whose path contribution is *warrant-gated* so revocation removes the exact original contribution rather than redistributing it;
2. one state transition contract connecting `learn → navigate → compose → verify → revoke/reopen → rewrite` while preserving authority and resource accounting;
3. a structural-obstruction gate that permits a graph/representation/operator rewrite only after lower-level mechanisms are witnessed insufficient;
4. lifecycle-safe consolidation: a macro-skill remains reusable only while the warrant and representation conditions of its source subgraph remain live;
5. a whole-system frontier against the faithful parent product above.

These are **residual candidates**, not novelty claims. M0 establishes only a coherent finite mathematical core and hostile checkers.

## Source boundary

Primary/theorem-bearing sources used above were checked on 2026-09-04. Current novelty is **not established**. This is a parent map, not a literature-saturation terminal; three clean post-material-addition passes are still required by #197 before any priority claim.

# V2-C08 Research and Manuscript Plan V0

**Working title:** *Reticulate Scientific Provenance and Component-Level Inheritance*  
**Status:** focused candidate with high parent-subsumption risk; all claims `CANNOT_CHECK`.

## 1. Scientific problem

Scientific artifacts and framework revisions frequently inherit different components from different parents: code, data, representations, semantics, instruments, methods, evaluators, authority and prior claims. A single parent commit, version tag or tree may therefore fail to describe what was inherited and which certificates remain valid.

## 2. Parent threats

- W3C PROV and data/process provenance;
- build systems, dependency graphs, version control and SBOMs;
- model/data lineage and experiment tracking;
- database why/where provenance;
- workflow provenance;
- stemmatology and textual contamination;
- phylogenetic networks/horizontal transfer;
- data fusion and multi-source knowledge integration;
- V1 source projections, dependency hypergraphs and selective reopening.

A standalone paper survives only if typed reticulate inheritance changes protected scientific transport/reopening decisions beyond a general provenance graph plus ordinary dependencies.

## 3. Candidate thesis

Component-level multi-parent inheritance with typed contribution roles and alternative support families can identify invalid semantic/evidence/certificate inheritance and improve selective reopening on composite scientific artifacts where tree ancestry and generic provenance are insufficient.

## 4. Candidate objects

### `ScientificArtifactInheritanceGraph`

- artifact and component identities;
- parent identities per component;
- contribution kind: implementation, data/evidence, semantics, representation, method, instrument, calibration, evaluator, authority, history;
- exact derivation/activity/agent lineage;
- correspondence and applicability context;
- uncertainty/ambiguity of parent assignment;
- epoch and revocation state.

### `ClaimSupportFamily`

Alternative complete support sets for a claim/certificate. A parent revocation invalidates only families intersecting the revoked contribution; the claim survives if another complete family remains.

### `InheritanceTransportReceipt`

Binds the target object/claim, inherited components, required semantics/evidence/authority, surviving support families, affected commitments, reopen decision and counterfactual tree-only judgment.

## 5. Formal questions

- When is a single-parent projection complete?
- How do alternative support families interact with component-level parentage?
- Which contribution kinds are substitutable and which are non-fungible?
- How do revocation and semantic drift propagate?
- When can parent assignment remain ambiguous without blocking all use?
- What is the minimal affected/reopen set after one parent changes?
- Can reticulate inheritance compose across generations without exponential blow-up?

## 6. Benchmark families

1. code from A, data from B, semantics from C, evaluator from D;
2. tree commit ancestry that omits data/model lineage;
3. one revoked code parent with independent alternative implementation support;
4. shared semantic parent invalidating several alternative execution paths;
5. composite dataset assembled from multiple overlapping sources;
6. scientific model whose calibration and training data have different parents;
7. manuscript/textual contamination and mixed copying;
8. horizontal transfer/recombination analogues;
9. ambiguous parent assignment;
10. unrelated parent revocation negative control;
11. current content survives but authority/calibration expires;
12. multi-generation reticulate history.

## 7. Baselines

- single parent/version tag;
- Git/tree ancestry;
- generic W3C PROV graph;
- build/SBOM dependency graph;
- V1 source projections and dependency hypergraph;
- general provenance plus alternative support;
- candidate typed inheritance graph.

The strongest baseline is generic provenance plus exact support/dependency semantics; a standalone claim requires separation from it.

## 8. Outcomes

- parent/contribution reconstruction accuracy;
- unsafe inheritance/certificate reuse;
- reopen precision/recall;
- alternative-support preservation;
- semantic/evidence/authority non-fungibility;
- ambiguity calibration;
- graph size and query cost;
- decision value over tree/general-provenance baselines;
- fresh-domain transfer.

## 9. Hostile cases

- multi-parent influence with no load-bearing decision consequence;
- generic provenance already returns the same reopen set;
- component labels inferred from prose but unsupported;
- alternative support incorrectly assumed independent;
- semantic parent change ignored because code/data unchanged;
- revoked evaluator treated as revoked content;
- reticulate graph creates false precision from ambiguous history;
- exponential lineage expansion without downstream value.

## 10. Relation to other papers

- C06 consumes inheritance for comparability but owns semantic/measurement linking.
- C07 consumes lineage as one dependence signal but owns statistical/common-cause dependence.
- C04 consumes reopening decisions.
- C08 should merge into C06/C07 if no independent provenance theorem or benchmark result survives.

## 11. Figures and tables

- Figure 1: tree ancestry versus component-level reticulate inheritance;
- Figure 2: alternative support families and revocation;
- Figure 3: benchmark generation and hidden parent types;
- Figure 4: reopen/unsafe-reuse results;
- Table 1: parent provenance systems;
- Table 2: contribution kinds and decisions;
- Table 3: reconstruction/transport results;
- Table 4: general-provenance versus typed inheritance;
- Table 5: scaling and ablations.

## 12. Honest terminals

- `GENERAL_PROVENANCE_GRAPH_SUFFICIENT`;
- `NO_INCREMENTAL_DECISION_VALUE`;
- `PARENT_ASSIGNMENT_UNRESOLVABLE`;
- `RETICULATE_COMPLEXITY_EXCEEDS_VALUE`;
- `MERGE_INTO_COMPARABILITY_OR_DEPENDENCE_PAPER`;
- `CANNOT_CHECK`.

## 13. Immediate pre-freeze work

- reconstruct W3C/data/workflow/build/stemmatology/phylogenetic parents;
- formalize typed support and revocation semantics;
- expand V0 reticulate fixtures;
- bind exact V1 provenance/reopening ownership;
- construct strongest generic provenance product;
- identify real composite scientific artifacts and adjudication routes;
- do not execute candidate outcome comparisons before handoff/protocol freeze.
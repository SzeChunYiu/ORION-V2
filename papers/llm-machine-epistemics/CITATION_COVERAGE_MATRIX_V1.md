# Citation Coverage Matrix V1 — Prospective Revision Audit

**Issue:** #51  
**Current manuscript source:** `MANUSCRIPT_DRAFT_V9_CURRENT.md`  
**Bibliography:** `REFERENCES_V1.bib` + `REFERENCES_CLASSICS_SUPPLEMENT_V1.bib`  
**Purpose:** make every load-bearing parent concession and direct-neighbor distinction mechanically auditable during Markdown→LaTeX conversion.

## Citation policy

A sentence classified below as `OWNERSHIP` or `DIRECT_NEIGHBOR` must carry at least one listed citation key in the final manuscript. A sentence classified as `#51_INTERNAL_RESULT` must bind to the proof appendix and/or mechanical receipt rather than rely on an external citation. A future editor may add stronger references but may not remove a listed direct parent unless the corresponding sentence is removed or contracted.

## A. Introduction / claim ceiling

| Manuscript assertion | Role | Required citation keys | Notes |
|---|---|---|---|
| Minimal/future-sufficient predictive state is established prior theory | `OWNERSHIP` | `shalizi2001computational`, `littman2001predictive` | `S_{P,rho}` is a registered-channel reference object, not novelty. |
| Utility/decision state over predictive state is established | `OWNERSHIP` | `brodu2011decisional`, `blackwell1953equivalent` | Brodu is the direct named control; Blackwell supplies general decision-information ordering. |
| Prediction-sufficient state can miss another target | `OWNERSHIP` | `baisero2021reconciling` | Broad prediction-vs-secondary-target separation is parent-owned. |
| Recursive/current+future decision-sufficient history compression is established | `OWNERSHIP` | `smallwood1973optimal`, `subramanian2022approximate`, `zhang2026minimal`, `paull1959minimizing` | POMDP/AIS + compatible/stable quotient work. |
| Capacity should preserve task/decision-relevant information | `OWNERSHIP` | `tishby1999information`, `strouse2017deterministic`, `grimm2020value`, `grimm2021proper`, `arumugam2022deciding` | Do not imply `Omega_dyn` creates generic rate-distortion theory. |
| “Epistemic state abstraction” terminology already exists | `BOUNDARY` | `arumugam2022information` | Prevent terminology ownership claim. |
| Iterated revision can require state beyond current beliefs | `OWNERSHIP` | `liberatore2024representing` | Supports revision-state/storage boundary. |
| LLM belief revision after new evidence already has a benchmark | `DIRECT_NEIGHBOR` | `wilie2024belief` | Mandatory comparison baseline. |
| Belief representation requires more than decodability | `BOUNDARY` | `herrmann2025standards` | Supports causal-use/functional-role requirement. |
| Real LLMs can contain belief-like causally useful internal structure | `BOUNDARY` | `mendozza2026beliefs` | Prevent “LLMs are epistemically empty” claim. |
| Hidden-state self-knowledge can reflect recall rather than truthfulness | `MOTIVATION` | `cheang2026know` | Supports typed responsibilities. |
| Matched predictor behavior does not identify arbitrary hidden representation properties | `OWNERSHIP` | `sevetlidis2026fiber` | Direct boundary for behavior-only inference. |

## B. Channel/input scope

| Manuscript assertion | Role | Required citations | Notes |
|---|---|---|---|
| Predictive sufficiency is relative to a declared controlled/reference process rather than “all conceivable future interventions” | `PARENT_ALIGNMENT` | `littman2001predictive`, `smallwood1973optimal`, `subramanian2022approximate` | The #51 theorem must freeze `rho` and separate later evidence intervention family. |
| A stronger state sufficient for the joint controlled future can already retain intervention-relevant distinctions | `MANDATORY_CONTROL` | `littman2001predictive`, `smallwood1973optimal`, `subramanian2022approximate` | P2 can legitimately contract under stronger target. |

No citation is required for the mere notation `rho`; citations support the parent-controlled interpretation.

## C. Direct 2026 LLM-memory neighbors

| Manuscript assertion | Role | Required citation keys | Required distinction |
|---|---|---|---|
| Learned internal reasoning/context compression exists and evicted content may persist through another channel | `DIRECT_NEIGHBOR` | `kontonis2026memento` | Audit tests revision retention; MEMENTO motivates alternate-channel controls. |
| “Prospective memory” is already an LLM-agent benchmark term | `TERMINOLOGY_BOUNDARY` | `liu2026pmbench` | Use `prospective revision adequacy`, not “prospective memory”. |
| Lossy LLM hand-off state can harm exact downstream constraint satisfaction | `DIRECT_NEIGHBOR` | `sharma2026state` | Generic compression failure is not novelty; current-equivalence+later-evidence audit is the delta. |
| Current evidence/memory sufficiency routing exists | `DIRECT_NEIGHBOR` | `lin2026stop` | Router-Mem asks sufficiency now; #51 asks adequacy after later evidence. |
| Continual scientific belief updating with memory exists | `DIRECT_NEIGHBOR` | `agarwal2026evidence` | #51 is representation certification, not a continual-discovery algorithm. |
| Selected/omitted evidence affects LLM updating | `DIRECT_NEIGHBOR` | `deng2026selected` | Acquisition/selection must be separated from retention loss. |
| Decision-aware context selection/compression exists | `DIRECT_NEIGHBOR` | `guan2026decision` | Do not claim decision-aware memory novelty. |
| Bounded typed memory/testbeds exist for long-horizon agents | `DIRECT_NEIGHBOR` | `cheng2026agenticsts` | Useful future empirical substrate, not our invention. |
| Exact/near-exact acceptable-continuation memory complexity has current public work | `PUBLIC_PREPRINT_NEIGHBOR` | `anonymous2026history` | Keep explicit double-blind/public-manuscript status. |

## D. #51 internal/supporting results — no external novelty laundering

| Result | Role | Required internal evidence |
|---|---|---|
| Static selector/partition equivalence | `#51_INTERNAL_RESULT_WITH_PARENT_SUBSTRATE` | `PROOF_APPENDIX_V1.md` + `RESPONSIBILITY_SELECTOR_AUDIT_V1.json`; parent context: Brodu/Blackwell/compatible-state literature. |
| Dynamic selector/refinement equivalence | `#51_INTERNAL_RESULT_WITH_PARENT_SUBSTRATE` | `PROOF_APPENDIX_V1.md` + `JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json`; parent context: AIS/stable quotient/finite-state minimization. |
| `Omega_dyn >= 0` | `#51_DERIVED_METRIC` | proof appendix + J4 receipt; never label as new information law. |
| Canonical `C_stat^*=0`, `C_dyn^*=1`, `Omega_dyn=1` witness | `#51_KNOWN_ANSWER_WITNESS` | proof appendix Theorem G.1 + J5 receipt. |
| Registered-channel no-certification theorem | `#51_PRIMARY_THEOREM` | `PROOF_APPENDIX_V1.md` Theorem G.1 + `PREDICTION_CHANNEL_AND_INTERVENTION_SCOPE_V1.md` + canonical mechanical witness. |
| P0/P1/P2 taxonomy | `#51_ANALYTICAL_TAXONOMY` | phase audit receipt + manuscript definitions; do not imply natural/universal cognition stages. |
| Horizon monotonicity/stabilization | `PARENT_STYLE_SUPPORTING_RESULT` | PH1/PH2 receipts + proof appendix; state theorem is not novelty. |
| Responsibility universality/full-history boundary | `PARENT_STYLE_SUPPORTING_BOUNDARY` | U1–U5 receipts; use only to motivate responsibility-relative scope. |
| Pairwise prospective collision | `#51_EASY_FAILURE_WITNESS` | canonical one-bit witness / old collision diagnostic; explicitly sufficient-only under general tied actions. |
| Complete one-step joint acceptable-action intersection criterion | `PARENT_STYLE_DECISION_COMPATIBILITY_COROLLARY` | `PROSPECTIVE_REVISION_COMPATIBILITY_CRITERION_V1.md`; separate mechanical checker pending. |
| Prospective Revision Audit | `#51_PRIMARY_ANALYTICAL_FRAMEWORK` | `PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V3.md` + no-certification theorem + compatibility criterion. |

## E. Mandatory nearest-assessment paragraph

The final manuscript must include comparisons with:

1. `wilie2024belief`: Belief-R tests whether output should update/maintain after new evidence.
2. `kontonis2026memento`: MEMENTO shows internal compression and alternate hidden channels; visible deletion is insufficient.
3. `liu2026pmbench`: prospective-intention memory is a different task.
4. `sharma2026state`: generic downstream failure from compressed hand-off is already demonstrated.
5. `lin2026stop`: current memory sufficiency/routing differs from future-revision adequacy.
6. `deng2026selected`: omitted-input evidence differs from lost retained state.
7. `guan2026decision` / `cheng2026agenticsts`: decision-aware and bounded-memory architectures are parent controls/possible audit substrates.

Required residual sentence, updated for V3:

> **The registered delta is not belief revision, memory compression, or decision-aware memory in isolation; it freezes a present prediction reference protocol, matches current prediction and responsibility behavior, intervenes on retained historical representation, excludes alternate-channel and parametric reconstruction where possible, then supplies common later evidence and scores joint future compatibility plus update and maintain/selective reopening.**

## F. Bibliography status classes

### Archival/final

`shalizi2001computational`, `littman2001predictive`, `brodu2011decisional`, `baisero2021reconciling`, `tishby1999information`, `strouse2017deterministic`, `blackwell1953equivalent`, `smallwood1973optimal`, `paull1959minimizing`, `subramanian2022approximate`, `grimm2020value`, `grimm2021proper`, `arumugam2022deciding`, `arumugam2022information`, `courtade2014multiterminal`, `liberatore2024representing`, `wilie2024belief`, `herrmann2025standards`, `mendozza2026beliefs`, `cheang2026know`.

### Preprint / status to refresh at submission

`sevetlidis2026fiber`, `zhang2026minimal`, `kontonis2026memento`, `liu2026pmbench`, `sharma2026state`, `lin2026stop`, `agarwal2026evidence`, `guan2026decision`, `cheng2026agenticsts`.

### Working paper / public review

`deng2026selected`, `anonymous2026history`.

The final submission checker must fail closed if a source in the last two classes is silently rewritten as a final peer-reviewed publication without metadata evidence.

## G. Citation-completeness gate

Before target-format submission:

- every citation key used in `MANUSCRIPT_DRAFT_V9_CURRENT.md` exists in the two frozen `.bib` files or a verified successor;
- every `OWNERSHIP`/`DIRECT_NEIGHBOR` row above is cited at least once;
- every bibliography item cited is relevant to a concrete sentence;
- no blind-review author identity is invented;
- no preprint is described as accepted/published without refreshed evidence;
- no parent concession may disappear during shortening without corresponding claim contraction;
- registered-channel scope must not be shortened back into “complete future” language;
- pairwise collision language must not be upgraded into a complete positive compatibility test.

Terminal on success:

`CITATION_COVERAGE_COMPLETE__PARENT_CONCESSIONS_BOUND__CHANNEL_SCOPE_PRESERVED`.

# Reviewer Tables V1 — Prospective Revision Audit

**Issue:** #51  
**Purpose:** provide compact manuscript-ready displays whose scientific interpretation is already frozen. These are text-source tables; final typesetting may be generated mechanically.

## Table 1 — What is parent-owned and what remains

| Object | Status in this paper | Strongest owner/control | Paper use |
|---|---|---|---|
| Minimal state for a registered future-prediction channel | Parent-owned | causal states; PSRs | reference `S_{P,rho}` |
| Utility/decision state over predictive state | Parent-owned | Brodu; Blackwell | P0 zero-extra-state control |
| Prediction state can miss another target | Parent-owned | R-PSR | blocks weak predictive≠epistemic novelty |
| Target/decision-aware compression | Parent-owned | IB/DIB; VE/PVE/VES | motivates conditional state cost only |
| Recursive decision-sufficient history compression | Parent-owned | POMDP information state; AIS | blocks generic recurrent-state novelty |
| Coarsest stable/right-congruent finite state | Parent-owned | automata/ISFSM; stable quotient | computation substrate only |
| Iterated revision-state storage | Parent-owned | belief-revision literature; Liberatore | blocks generic “revision needs memory” claim |
| LLM belief revision after later evidence | Parent-owned assessment | Belief-R | mandatory nearest assessment baseline |
| LLM context/state compression | Parent-owned practical area | MEMENTO; relay compression; decision-aware memory | practical parent/control |
| Prospective-intention memory | Parent-owned task | PM-Bench | terminology boundary |
| **Present-equivalence representation intervention → common later evidence → update+maintain audit** | **Candidate assessment delta** | no direct parent found through 2026-08-29 search frontier | primary standalone contribution |
| **No-certification witness: equal current adequacy, unequal future revision adequacy** | **Supported finite theorem/witness** | proof/mechanical package; components parent-owned | logical justification for separate audit axis |

## Table 2 — Three audit axes

| Axis | Question | Failure means | Appropriate response |
|---|---|---|---|
| Registered linguistic prediction | Does the representation preserve the declared target under reference protocol `rho`? | predictive information lost for that target | improve predictive state / redefine declared target explicitly |
| Current responsibility | Given current evidence, can the registered decision be made with acceptable regret? | current decision-relevant information lost | preserve current cross-channel state or acquire evidence |
| Prospective revision | After registered later evidence, can the system update/maintain/selectively reopen correctly? | dormant history needed later was not retained or reconstructable | preserve/retrieve revision-relevant history; distinguish from acquisition/reconstruction |

These axes must not be collapsed into one confidence score. A stronger controlled prediction/state target that already includes the future intervention family is a legitimate parent control and can make the third axis redundant for that target.

## Table 3 — P0/P1/P2 taxonomy

| Phase | Static cost `C_stat^*` | Dynamic premium `Omega_dyn` | Interpretation |
|---|---:|---:|---|
| P0 predictive-decisional | `0` | `0` | registered predictive state already supports present decision and registered revision process |
| P1 static cross-channel | `>0` | `0` | extra state needed now; once retained, no further future-only state required |
| P2 prospective refinement | `>=0` | `>0` | present-adequate state still omits dormant information needed only after later evidence |

Acquisition/non-identifiability is a pre-phase condition, not P1 or P2. A stronger controlled reference target may move a case toward P0/P1; this demonstrates channel/target relativity rather than contradicting the taxonomy.

## Table 4 — Canonical no-certification witness

| Quantity | Compressed state | Augmented state |
|---|---|---|
| registered prediction protocol | same `rho` | same `rho` |
| current predictive state | same `S_{P,rho}` | same `S_{P,rho}` |
| current responsibility action | unique `RETAIN` | unique `RETAIN` |
| retained dormant provenance | absent | one bit: source A/B |
| later common controlled evidence | `RETRACT(A)` | `RETRACT(A)` |
| correct future action for A-supported history | cannot distinguish from B history | `REOPEN` |
| correct future action for B-supported history | cannot distinguish from A history | `RETAIN` |
| `C_stat^*` | `0` bits | `0` bits beyond the reference for current action |
| `C_dyn^*` required for exact revision process | `1` bit minimum | one-bit augmentation realizes it |
| `Omega_dyn` | `1` bit | — |

Headline consequence:

> Present adequacy for the registered linguistic target and present zero-regret decision do not certify prospective revision adequacy under a distinct later evidence intervention.

## Table 5 — Prospective Revision Audit V3 conditions

| Condition | Retained state / target | Purpose | Expected use |
|---|---|---|---|
| Full-history reference | all registered history | ceiling / positive control | should support revision when responsibility is identifiable |
| Predictive-only | state sufficient for registered `rho` linguistic target | tests whether predictive state alone is sufficient | P0 or cross-channel failure |
| Current-decision-minimal | state sufficient for present acceptable decision | isolates future-only requirement | primary P2 comparison |
| Prospective-adequate | state retaining registered dormant revision information | positive control for future revision | should recover update+maintain behavior |
| Controlled-future reference | state/target explicitly includes future intervention family | stronger parent control | former P2 may contract to P0/P1 |
| Acquisition-negative | dormant variable absent from available initial information | identifiability control | must not be called representation loss |
| Evidence-reconstructs-state | later evidence itself reveals dormant variable | negative control on P2 attribution | prospective penalty should disappear |
| Alternate-channel-retained | visible state removed but variable survives in KV/hidden/retrieval/tool/external state | intervention-validity control | terminate as non-removal or CANNOT_CHECK |
| Parametric-reconstruction | fixed model knowledge + observed content reconstruct dormant variable | side-information control | success is not evidence of retained episode state |

## Table 6 — Primary empirical metrics if Protocol V3 is ever run

| Metric | Definition / intent | Why separate |
|---|---|---|
| Present-equivalence verdict | CI/equivalence test lies within prospectively frozen language/current-risk margins | prevents “non-significant difference” from being mistaken for equivalence |
| Update accuracy/regret | correct change when later evidence defeats/changes support | detects under-revision |
| Maintain accuracy/regret | correct non-change when later evidence is irrelevant or independent support survives | detects over-revision |
| Selective-reopening precision/recall | reopen only commitments dependent on defeated support | distinguishes targeted revision from global reset |
| Prospective revision regret | future responsibility loss after common later evidence | primary third-axis outcome |
| Incompatible representation/evidence cell rate | cells with empty **joint** acceptable future-action intersection | complete exact one-step structural diagnostic under ANY_OPTIMAL_ACTION |
| Pairwise disjoint collision rate | merged pairs with disjoint future action sets | easy sufficient failure witness; not complete under ties |
| Alternate-channel removal verdict | whether dormant variable is absent from registered surviving state channels | causal attribution gate |
| Parametric reconstruction verdict | whether fixed model knowledge reconstructs variable without retained episode state | separates memory retention from prior knowledge/inference |
| Operational state cost | bits/tokens/KV/memory footprint under tested system | practical cost, not theoretical entropy unless conditions justify it |

## Table 7 — Direct-neighbor distinction

| Neighbor | What it already establishes | What the registered audit additionally conditions on |
|---|---|---|
| Belief-R | output update/maintain after new evidence | matched present representation conditions + controlled retention intervention before common later evidence |
| MEMENTO | learned compact reasoning state; hidden alternate retention channels | causal removal/retention gate + evidence-triggered selective revision |
| PM-Bench | future-intention memory and cue execution | revision of an already-held responsibility decision, not delayed intention execution |
| Two-agent state compression | compressed hand-off can harm downstream exact decisions | same current behavior first, then common later evidence |
| Router-Mem | whether current retrieved evidence suffices or deeper retrieval is needed | state may be sufficient now yet inadequate only for later revision |
| Selected/omitted-evidence studies | changing observed evidence changes LLM updating | initial evidence held fixed; manipulate what is retained |
| Decision-aware memory / bounded-memory agents | context chosen/compressed according to task utility | prospective-revision certification as an evaluation layer, not a memory architecture |

## Table 8 — Pairwise witness versus complete one-step compatibility

| Cell future acceptable-action sets | Pairwise disjoint pair? | Joint intersection | Exact one-step status |
|---|---:|---:|---|
| `{REOPEN}`, `{RETAIN}` | yes | empty | incompatible; pairwise witness complete |
| `{a,b}`, `{b,c}`, `{a,c}` | no | empty | incompatible despite no disjoint pair |
| `{a,b}`, `{b,c}` | no | `{b}` | compatible by choosing `b` |

Rule:

> Pairwise collision is a sufficient failure certificate. The complete exact one-step `ANY_OPTIMAL_ACTION` test is the joint acceptable-action intersection over the entire representation/evidence cell.

## Table 9 — Claim ceilings

| Permitted statement | Forbidden stronger statement |
|---|---|
| The finite construction proves current adequacy for the registered prediction/decision tasks does not generally certify later revision under a distinct evidence intervention. | A state sufficient for every possible controlled future can still forget intervention-relevant information. |
| `Omega_dyn` is a derived audit coordinate in the registered finite model. | `Omega_dyn` is a new universal information law. |
| P0/P1/P2 is a useful audit taxonomy. | P0/P1/P2 are universal stages of intelligence or cognition. |
| Cross-channel means not measurable from the declared linguistic predictive quotient under `rho`. | The responsibility necessarily uses a physically separate channel. |
| The protocol can be run without training a new LLM. | The theory has empirically improved an LLM. |
| No direct neighbor found through the registered search frontier uses the complete matched-current audit sequence as its primary object. | No prior work anywhere has ever considered similar revision/memory questions. |
| Pairwise disjoint actions certify a failure. | No pairwise collision certifies one-step sufficiency under tied actions. |

These ceilings should survive all shortening and venue conversion.

# Reviewer Tables V1 — Prospective Revision Audit

**Issue:** #51  
**Purpose:** provide compact manuscript-ready displays whose scientific interpretation is already frozen. These are text-source tables; final typesetting may be generated mechanically.

## Table 1 — What is parent-owned and what remains

| Object | Status in this paper | Strongest owner/control | Paper use |
|---|---|---|---|
| Minimal state for future prediction | Parent-owned | causal states; PSRs | reference channel `S_P` |
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
| Linguistic prediction | Does the representation preserve the declared language-prediction target? | predictive information lost | improve predictive state / representation |
| Current responsibility | Given current evidence, can the registered decision be made with acceptable regret? | current decision-relevant information lost | preserve current cross-channel state or acquire evidence |
| Prospective revision | After registered later evidence, can the system update/maintain/selectively reopen correctly? | dormant history needed later was not retained or reconstructable | preserve/retrieve revision-relevant history; distinguish from acquisition failure |

These axes must not be collapsed into one confidence score.

## Table 3 — P0/P1/P2 taxonomy

| Phase | Static cost `C_stat^*` | Dynamic premium `Omega_dyn` | Interpretation |
|---|---:|---:|---|
| P0 predictive-decisional | `0` | `0` | linguistic predictive state already supports present decision and registered revision process |
| P1 static cross-channel | `>0` | `0` | extra state needed now; once retained, no further future-only state required |
| P2 prospective refinement | `>=0` | `>0` | present-adequate state still omits dormant information needed only after later evidence |

Acquisition/non-identifiability is a pre-phase condition, not P1 or P2.

## Table 4 — Canonical no-certification witness

| Quantity | Compressed state | Augmented state |
|---|---|---|
| current linguistic predictive state | same | same |
| current responsibility action | unique `RETAIN` | unique `RETAIN` |
| retained dormant provenance | absent | one bit: source A/B |
| later common evidence | `RETRACT(A)` | `RETRACT(A)` |
| correct future action for A-supported history | cannot distinguish from B history | `REOPEN` |
| correct future action for B-supported history | cannot distinguish from A history | `RETAIN` |
| `C_stat^*` | `0` bits | `0` bits beyond the reference for current action |
| `C_dyn^*` required for exact revision process | `1` bit minimum | one-bit augmentation realizes it |
| `Omega_dyn` | `1` bit | — |

Headline consequence:

> Present linguistic adequacy and present zero-regret decision adequacy do not certify prospective revision adequacy.

## Table 5 — Prospective Revision Audit conditions

| Condition | Retained state | Purpose | Expected use |
|---|---|---|---|
| Full-history reference | all registered history | ceiling / positive control | should support revision when responsibility is identifiable |
| Predictive-only | state sufficient for declared linguistic target | tests whether predictive state alone is sufficient | P0 or cross-channel failure |
| Current-decision-minimal | state sufficient for present acceptable decision | isolates future-only requirement | primary P2 comparison |
| Prospective-adequate | state retaining registered dormant revision information | positive control for future revision | should recover update+maintain behavior |
| Acquisition-negative | dormant variable absent from available initial information | identifiability control | must not be called representation loss |
| Evidence-reconstructs-state | later evidence itself reveals the dormant variable | negative control on P2 attribution | prospective penalty should disappear |
| Alternate-channel-retained | visible state removed but variable survives in KV/hidden/retrieval/tool/external state | intervention-validity control | terminate as non-removal or CANNOT_CHECK |

## Table 6 — Primary empirical metrics if Protocol V2 is ever run

| Metric | Definition / intent | Why separate |
|---|---|---|
| Present-equivalence pass rate | conditions match on language target and registered current decision before later evidence | prevents confounding revision with present performance |
| Update accuracy/regret | correct change when later evidence defeats/changes support | detects under-revision |
| Maintain accuracy/regret | correct non-change when later evidence is irrelevant or supports independent route | detects over-revision |
| Selective-reopening precision/recall | reopen only commitments dependent on defeated support | distinguishes targeted revision from global reset |
| Prospective revision regret | future responsibility loss after common later evidence | primary third-axis outcome |
| Revision-collision count/rate | matched pairs merged by state but future actions become incompatible | structural diagnostic |
| Alternate-channel removal verdict | whether dormant variable is actually absent from all registered surviving channels | causal attribution gate |
| Operational state cost | bits/tokens/KV/memory footprint under the tested system | practical cost, not theoretical entropy unless conditions justify it |

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

## Table 8 — Claim ceilings

| Permitted statement | Forbidden stronger statement |
|---|---|
| The finite construction proves current adequacy does not generally certify later revision adequacy. | Real LLMs generally discard revision-relevant information. |
| `Omega_dyn` is a derived audit coordinate in the registered finite model. | `Omega_dyn` is a new universal information law. |
| P0/P1/P2 is a useful audit taxonomy. | P0/P1/P2 are universal stages of intelligence or cognition. |
| Cross-channel means not measurable from the declared linguistic predictive quotient. | The responsibility necessarily uses a physically separate channel. |
| The protocol can be run without training a new LLM. | The theory has empirically improved an LLM. |
| No direct neighbor found through the registered search frontier uses the complete matched-current audit sequence as its primary object. | No prior work anywhere has ever considered similar revision/memory questions. |

These ceilings should survive all shortening and venue conversion.

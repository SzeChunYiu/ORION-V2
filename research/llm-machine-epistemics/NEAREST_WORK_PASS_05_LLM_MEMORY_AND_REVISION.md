# Nearest Work Pass 05 — 2026 LLM Memory, Compression, and Prospective Revision

**Issue:** #51  
**Purpose:** final direct-neighbor search against the surviving Prospective Revision Audit, rather than generic epistemic/state theory.  
**Search window:** current literature visible through 2026-08-29.  
**Status:** scientific overlap decisions frozen; exact metadata serialization remains mechanical.

## Executive conclusion

The 2026 LLM-memory neighborhood is much denser than the initial #51 search suggested.

Important active directions already include:

- learned internal context/state compression;
- decision-aware selection and compression;
- bounded typed memory for long-horizon agents;
- prospective memory benchmarks for future intentions;
- downstream decision failures caused by lossy hand-off compression;
- evidence-conditioned memory sufficiency routers;
- continual evidence-informed LLM belief updating;
- belief updating under selected/omitted evidence.

This means #51 must **not** claim that:

- LLM state compression is new;
- preserving information for future reasoning is new;
- prospective memory evaluation is new;
- decision-aware memory is new;
- evidence-driven belief updating is new;
- state omission harming downstream decisions is new.

No direct work found in this pass, however, combines all of the following as the primary assessment design:

```text
1. match current linguistic prediction,
2. match the registered current responsibility decision,
3. intervene on / compare retained historical representation,
4. reveal later evidence whose correct consequence depends on a dormant history distinction,
5. measure update AND maintain/selective-reopening behavior,
6. attribute failure only after present-equivalence and acquisition controls pass.
```

Thus the Prospective Revision Audit remains a **candidate assessment-design delta**, not a core memory-method novelty.

---

# 1. MEMENTO — internal context compression is a direct practical parent

**Vasilis Kontonis, Yuchen Zeng, Shivam Garg, Lingjiao Chen, Hao Tang, Ziyan Wang, Ahmed Awadallah, Eric Horvitz, John Langford, Dimitris Papailiopoulos.**

*MEMENTO: Teaching LLMs to Manage Their Own Context.*  
arXiv:2604.09852; Microsoft Research lists the work as a 2026 COLM publication.

## Relevant contribution

MEMENTO trains reasoning models to:

1. segment reasoning into blocks;
2. compress each block into a dense “memento” summary;
3. evict the original block;
4. continue reasoning using the mementos.

The work reports substantial KV-cache reduction while retaining benchmark accuracy, and—especially relevant to #51—finds a **dual information stream**: information from removed reasoning blocks can persist implicitly in KV states associated with the compressed mementos. Removing that implicit channel causes a large accuracy drop in a reported ablation.

## Ownership effect

This is a strong practical parent for:

- internal LLM state/context compression;
- “retain only what future reasoning needs” as a learned capability;
- the possibility that nominally removed information survives in another internal channel.

### #51 consequence

A future #51 empirical audit **must check for alternate retained channels**. Removing text/source metadata is insufficient evidence that the dormant variable left the model state if it can persist in KV/hidden representations.

Add to falsifiers:

`ALLEGED_STATE_REMOVAL_BUT_VARIABLE_REMAINS_CAUSALLY_RECOVERABLE_ELSEWHERE`.

This strengthens, rather than removes, the need for a causal representation intervention.

## Distinction

MEMENTO optimizes compact state for continued reasoning on the same trajectory. It does not primarily ask whether two states matched on current prediction and current decision differ in later **evidence-triggered revision** of a registered claim.

Verdict:

`STRONG_PRACTICAL_PARENT__NO_DIRECT_AUDIT_COLLISION_FOUND`.

---

# 2. PM-Bench — “prospective memory” terminology is occupied

**Genglin Liu, Saadia Gabriel.**  
*PM-Bench: Evaluating Prospective Memory in LLM Agents.*  
arXiv:2607.12385 (2026).

## Relevant contribution

PM-Bench evaluates prospective memory in the cognitive-science sense: an agent must maintain **future intentions**, detect the appropriate later cue/state, and execute delayed tasks while ongoing activities continue.

## Ownership / naming effect

The phrase “prospective memory” is now directly occupied in LLM-agent evaluation.

### #51 consequence

Do **not** rename our object to “prospective memory” or imply that #51 is the first prospective-memory evaluation for LLM agents.

Use:

- `prospective revision adequacy`;
- `future evidence-triggered revision`;
- `revision retention`.

Explicit distinction:

```text
PM-Bench:
    remember a future intention and execute it at the correct cue.

#51:
    retain dormant historical information so that later evidence can change
    or preserve a current epistemic decision correctly.
```

Verdict:

`TERMINOLOGY_DIRECT_PARENT__TASK_DISTINCT`.

---

# 3. State Compression in Two-Agent LLM Relays

**Anantha Sharma, Sheeba Elizabeth John, Kaarthik Senthil Kumar, Saratsuhas Vijayababu.**  
*State Compression in Two-Agent LLM Relays: A Closed-World Study of Constraint Preservation.*  
arXiv:2607.18265 (2026).

## Relevant contribution

The study compares uncompressed state, narrative summaries, schema-constrained JSON and embedding pruning in a two-agent travel-planning relay. The downstream agent sees only the compressed hand-off, while exhaustive inventory enumeration supplies exact feasible/optimal labels. Reported feasibility differs strongly by representation; structured JSON substantially outperforms narrative summarization in the study.

## Ownership effect

Direct practical prior art for:

- representation compression causing downstream decision failures;
- closed-world exact labels for testing compressed state;
- structured summaries outperforming shorter narrative summaries.

### #51 consequence

The claim

> “state compression can discard decision-relevant information”

is definitely not new even in LLM-agent systems.

The Prospective Revision Audit must emphasize the **temporal/evidence-triggered matched-current control**, not generic downstream constraint preservation.

Verdict:

`DIRECT_PRACTICAL_PARENT_FOR_COMPRESSION_FAILURE__AUDIT_TEMPORAL_DELTA_REMAINS`.

---

# 4. Router-Mem — evidence-conditioned sufficiency decisions

**Yidan Lin, Kaixiang Wang, Jiong Lou, Jie Li.**  
*Stop When Memory Suffices: Evidence-Conditioned Progressive Execution for LLM Agents.*  
arXiv:2608.01285 (2026).

## Relevant contribution

Router-Mem uses low-cost retrieval followed by a learned sufficiency router that decides whether current evidence is sufficient to answer or whether to expand to deeper memory blocks.

## Ownership effect

“Memory sufficiency” and dynamic escalation according to evidence coverage are active LLM-agent research concepts.

### #51 consequence

Do not claim novelty for asking whether retrieved/retained memory is “sufficient” in general.

Difference:

Router-Mem asks whether **current evidence is sufficient for a current answer** and expands memory if not. #51 asks whether a state already sufficient for the current decision retained information needed **after a later evidence event**.

Verdict:

`NEAR_TERM_PARENT__TEMPORAL_REVISION_DISTINCTION_REMAINS`.

---

# 5. Evidence-Informed LLM Beliefs for Continual Scientific Discovery

**Dhruv Agarwal, Reece Adamson, Andrew McCallum, Peter Clark, Ashish Sabharwal, Bodhisattwa Prasad Majumder.**  
*Evidence-Informed LLM Beliefs for Continual Scientific Discovery.*  
arXiv:2606.29182 (2026).

## Relevant contribution

The work treats LLM beliefs as evolving with evidence from previous hypotheses and uses memory/retrieval over previous discoveries to compute non-stationary surprise for future scientific search. It reports that a substantial fraction of static surprise signals become spurious when prior discoveries are incorporated.

## Ownership effect

Direct current prior art for:

- evidence-informed evolving LLM belief state;
- memory of prior discoveries affecting later scientific decisions/rewards;
- continual scientific use of non-stationary belief updates.

### #51 consequence

Do not claim that evidence-updated persistent beliefs for scientific discovery are new.

Difference:

#51's theoretical question is narrower: **given matched current prediction and current responsibility, can deliberate state compression destroy later revision capability?** It is an assessment/certification question rather than a continual-discovery algorithm.

Verdict:

`STRONG_APPLICATION_NEIGHBOR__NO_EXACT_ASSESSMENT_COLLISION_FOUND`.

---

# 6. Selected Evidence, Omitted Information, and LLM Belief Updating

**Zebang Deng, Jubo Yan.**  
*Selected Evidence, Omitted Information, and Belief Updating in Large Language Model Decision Support.*  
2026 working paper / SSRN `7060438` (current public version; publication status must be qualified).

## Relevant contribution

The study tests whether LLMs account for selection processes and omitted evidence in numerical belief updating. Its design compares selected evidence with controls and later visible-only evidence/instructions, reporting specific numerical updating failures in selected-evidence settings.

## Ownership effect

Direct practical neighbor for:

- omitted evidence;
- LLM belief updating;
- later evidence causing further estimate change;
- selected versus complete evidence conditions.

### #51 consequence

Do not imply that omission-sensitive belief updating in LLM decision support is unexplored.

Difference:

The paper manipulates **which evidence is observed**. #51's load-bearing P2 design holds initial information availability fixed, matches current behavior, then manipulates **what the representation retains** before common later evidence.

That distinction must remain explicit:

```text
acquisition / selection bias != representation retention loss
```

Verdict:

`DIRECT_BELIEF_UPDATING_NEIGHBOR__ACQUISITION_VS_RETENTION_DELTA_REMAINS`.

---

# 7. Decision-Aware Memory Cards and AgenticSTS

Already included in Pass 04, but Pass 05 confirms their role.

## Decision-Aware Memory Cards

Decision utility/action shift is explicitly used to select and compress context for tool-using agents.

## AgenticSTS

Long-horizon memory is treated as a bounded contract controlling what each future decision may retrieve; memory layers are designed to be independently ablatable.

### #51 consequence

The paper should describe the proposed audit as compatible with these memory systems:

- first establish present equivalence;
- ablate/modify one memory layer or information type;
- reveal future evidence;
- check revision collisions/update-maintain performance.

Do not claim to invent decision-aware or typed bounded memory.

---

# 8. Memento-related new experimental control

Pass 05 adds a new required empirical control to `PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V1`:

## Alternate-channel retention control

When an intervention claims to remove dormant variable `B`, independently test whether `B` remains decodable/causally usable from another state channel that survives the intervention.

Examples:

- KV representations;
- hidden-state residual stream;
- cached retrieval keys;
- compressed summary embeddings;
- tool state;
- external memory indexes.

A failed text-level removal plus intact hidden channel should terminate as:

`INTERVENTION_DID_NOT_REMOVE_DORMANT_INFORMATION`.

This is crucial because MEMENTO directly demonstrates that masked/evicted reasoning content can leave useful information in downstream KV representations.

---

# 9. Final direct-neighbor comparison table

| Neighbor | Already does | Does not directly do, based on current public description |
|---|---|---|
| Belief-R | update/maintain after new evidence | matched-current representation intervention isolating retained history |
| MEMENTO | learned internal reasoning-state compression; future reasoning from compact state; implicit retained channel | evidence-triggered revision audit after matched current decision |
| PM-Bench | prospective intention memory over delayed cues | revision of a current epistemic decision after later evidence |
| State Compression LLM Relays | compressed hand-off representation affects downstream exact constraints | present-equivalence + later common evidence + revision collision |
| Router-Mem | current evidence sufficiency and progressive memory expansion | state sufficient now but insufficient only after future evidence |
| Evidence-Informed LLM Beliefs | persistent evidence-updated beliefs for continual scientific discovery | causal certification of representation retention after matched current behavior |
| Selected Evidence / Omitted Information | belief updating with selected/omitted evidence | distinguishes acquisition/selection from same-information state-retention loss |
| Decision-Aware Memory Cards | decision-critical context selection/compression | prospective revision after matched current state |
| AgenticSTS | bounded typed long-horizon memory/ablation testbed | epistemic revision collision / matched-current audit specifically |

---

# 10. Pass-05 novelty terminal

```text
LLM_STATE_COMPRESSION_NOVELTY = NO
FUTURE_REASONING_FROM_COMPRESSED_STATE_NOVELTY = NO
DECISION_AWARE_LLM_MEMORY_NOVELTY = NO
PROSPECTIVE_MEMORY_BENCHMARK_NOVELTY = NO
BELIEF_REVISION_AFTER_NEW_EVIDENCE_NOVELTY = NO
EVIDENCE_UPDATED_PERSISTENT_LLM_BELIEFS_NOVELTY = NO
OMITTED_EVIDENCE_BELIEF_UPDATE_NOVELTY = NO

MATCHED_CURRENT_REPRESENTATION_INTERVENTION_PLUS_LATER_REVISION = NO_DIRECT_COLLISION_FOUND_IN_PASS_05
PROSPECTIVE_REVISION_COLLISION_CERTIFICATE = CANDIDATE_ASSESSMENT_DEVICE__FIBRE_MATH_PARENT_OWNED

PRIMARY_RESIDUAL = PROSPECTIVE_REVISION_REPRESENTATION_AUDIT
RESIDUAL_TYPE = FORMAL_ASSESSMENT_DESIGN / ANALYTICAL FRAMEWORK
NOVELTY_CONFIDENCE = MODEST__HIGH_PARENT_PRESSURE
```

This pass **weakens any architectural/memory novelty claim** but does not currently eliminate the assessment-task delta.

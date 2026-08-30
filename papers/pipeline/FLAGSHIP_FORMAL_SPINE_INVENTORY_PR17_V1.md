# Flagship Formal-Spine Inventory — PR17 Re-audit V1

**Skill state:** `SzeChunYiu/academic-paper-skills` PR #17 head `ef47c81101e1e1b97864019dde143456a581de1c`, stacked on PR #16 head `087e47330826295a0b114563ec33238951ac56a9`.  
**Paper:** Machine Epistemics Perspective.  
**Purpose:** prevent the regression `ideas retained; formal scientific object deleted` during Perspective compression.

## Frozen inventory

| formal_id | kind | canonical expression / definition | scientific role | main-text requirement | scope/status | relocation |
|---|---|---|---|---|---|---|
| ME-FS-01 | state | `E_t=(P_t,S_t,O_t,A_t,R_t,M_t,V_t,X_t,H_t,K_t)` | identifies the bounded scientific-episode state governed by Machine Epistemics | **required** | proposed formal object; coordinates defined by programme | no |
| ME-FS-02 | composition / hierarchy | `\widetilde E_t=(E_t;\Gamma_t,\Pi_t,\mathcal A_t)` | shows generative regime, locality/perspective and atlas/horizon as decision-relevant extensions of the base state rather than disconnected metaphors | **required** | optional coordinates only when decision-relevant | no |
| ME-FS-03 | transition | `T_t:(\widetilde E_t,a_t,x_t)\mapsto(\widetilde E_{t+1},\rho_t)` | identifies the scientific transition whose admissibility/warrant is the programme's elementary object | **required** | proposed transition schema; receipt is non-authorizing | no |
| ME-FS-04 | context boundary | `C=(environment, task family, resources, system boundary, substrate/interface, timescale, criterion)` | prevents competence/transport claims from becoming universal by default | **required** | context-relative competence/locality contract | no |
| ME-FS-05 | non-implication | `successful execution \not\Rightarrow warranted scientific transition` | compactly separates mechanism/execution from epistemic warrant | **required** | programme boundary, not empirical theorem | no |
| ME-FS-06 | atlas/territory boundary | `\mathcal A_t\neq\mathfrak E^\star` | prevents the observed atlas being identified with total possible epistemic space | **required while atlas is discussed** | `\mathfrak E^\star` is an ideal semantic placeholder only | no |
| ME-FS-07 | local-to-global non-implication | `pairwise compatible \not\Rightarrow global section witnessed` | preserves the gluing distinction that later atlas/horizon falsifiers test | **required while atlas is discussed** | sheaf/fibration language only under applicable prerequisites | no |
| ME-FS-08 | candidate-law family | criterion conservation; non-amplifying authority; typed transport; selective reopening; dependence/censoring visibility; bounded closure | tells the reader what recurring constraints the research programme proposes to test | preferred | **candidate hypotheses**, not established axioms/laws | conditional; exhaustive list may remain in framework record |

## Canonical sources

- `research/field/MACHINE_EPISTEMICS_FIELD_SYNTHESIS_V1.md` — episode state, transition form, foundation-law status and quantitative programme.
- `research/framework/EPISTEMIC_ATLAS_AND_HORIZON_FORMALISM_WAVE06_V1.md` — atlas/territory separation, context tuple, gluing/non-implication and globality limits.
- `research/framework/GENERATIVE_REGIME_INVENTION_FORMALISM_WAVE06_V1.md` and locality formalism — decision-relevant `Gamma` / perspective semantics.

## PR17 reader-recovery test

A competent target reader must be able to answer from the main paper:

1. **What is the formal object?** — `E_t`, optionally extended to `\widetilde E_t`.
2. **What operation is studied?** — the warranted scientific-state transition `T_t` returning receipt `\rho_t`.
3. **Under what boundary does it apply?** — declared context `C`, resources, criterion and external authority `K_t`.
4. **What does it explicitly fail to imply?** — execution does not imply warrant; atlas does not equal territory; pairwise compatibility does not imply witnessed global coherence.
5. **What is definition versus hypothesis?** — state/transition/context are programme definitions; the recurring conservation/transport/reopening/closure rules are candidate constraints to test.
6. **How do later concepts attach?** — `Gamma_t`, `Pi_t` and `A_t` are optional coordinates of the decision-relevant state, not separate field metaphors.

## V14 delta finding

The compressed V14 Perspective preserved the prose-level ideas but failed ME-FS-01 through ME-FS-07 as explicit main-text formal items. Under PR17 this is a scientific-content regression even though the prose is coherent.

## Required repair

Restore the compact formal core in main text before `Frontier problems expose the distinction`, while keeping the Perspective scale by removing no contribution-defining formal content. The target pattern is:

```text
formal state -> optional hierarchy -> transition/receipt -> context boundary
-> decisive non-implications -> candidate constraints + falsifiers
```

No new equation may be introduced unless it is already supported by the programme's formal records.

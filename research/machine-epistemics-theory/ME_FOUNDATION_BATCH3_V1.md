# Machine Epistemics Foundation — Batch 3: procedure, runtime, learning, consolidation, Jump and action semantics

**Status:** ORION-V2 theory artifact. **NO NOVELTY, FIELD-STATUS, OCM-SUPERIORITY OR PUBLICATION-AUTHORITY CLAIM.** This batch closes only the exact scope stated for MEG-05/10/11/12/13/15/19/21/28/33. Open-research halves remain named.

**Dependencies:** merged PR #317 (`d756c086…`) and Batch 2 on PR #321. **Checker:** `meg_foundation_batch3_exact.py`, stdlib only, exit 0/1/2 = PASS/FAIL/CANNOT_CHECK. Finite enumeration and planted mutants are sanity/counterexample evidence; the all-size statements below stand on the proofs and explicit construction contracts.

## Analytical cells

Same-session lenses, not independent authority: **formal semantics** (program algebra, preservation/progress), **learning theory** (version spaces and query-relative identification), **epistemic governance** (speech/action/authority separation), **dynamic systems** (local repair/conservative extension), and a **hostile parent referee** (tries to contract every claim to KAT, version spaces, ATMS/incremental computation, graph transformation, and value-of-information parents).

---

## T1 — MEG-05: speech/discourse state cannot mint world truth

### Definition

Keep three proposition roles distinct:

- `said(u,p,e_t)`: transcript-bound OBSERVATION that speaker `u` produced surface content corresponding to `p`; its authority may be positive on `speaker`, but is bottom on `world_truth` and `commit`.
- `committed(u,p,S)`: a derived discourse-state atom saying the speaker is publicly committed to `p` in conversational scope `S`; it inherits speaker authority but still has `world_truth=0`.
- `machine_claim(p)`: the machine's own proposition, whose truth warrant/authority must be supplied by the ordinary warranting channels and cannot be obtained from speech repetition alone.

Internal composition includes the operator authority factor from merged MEG-04; that factor has no positive world-truth/commit authority.

### Theorem T1.1 — discourse non-laundering

Any finite internal composition of `said`/`committed` atoms has `world_truth=0` and `commit=0`. This remains true for any number of mutually independent speakers.

**Proof.** Authority composition is coordinate-wise meet. Every speech/discourse factor has `world_truth=0`; the internal operator factor is also bottom on `commit`. A finite meet containing bottom is bottom. Induct over the composition tree. ∎

### Corollary — majority is not truth

Ten speakers repeating `p` may be strong evidence about *what was said* or social consensus, but the repetition itself does not produce a world-truth authority edge. A majority-vote promotion is a different operator and must have an independently registered evidential contract.

### Boundary

This does not deny testimony as evidence. It says testimony must enter through an explicit testimony/source-reliability model whose authority and dependence are separately warranted (MEG-01), not by relabelling a discourse-state atom as truth.

**Terminal:** `MEG-05 = PROVED_SCOPE_LIMITED__DISCOURSE_STATE_NONLAUNDERING`.

---

## T2 — MEG-10: finite procedure warrant algebra, with trace and static readings separated

Kleene Algebra with Tests (Kozen 1997) owns the control algebra. ORION adds no new program algebra. The Machine Epistemics obligation is to specify which warrant a stored/executed procedure carries.

For a finite procedure expression built from atomic operators, sequencing `;`, guarded choice, typed parallel wiring and bounded iteration, define:

- **trace warrant** `Λ_tr(τ)`: the `⊗`-product of exactly the guards/operators/edges that fired in one recorded execution trace `τ`;
- **static warrant** `Λ_st(p)`: the `⊗`-product of the warrants of every branch reachable under the registered finite control graph, i.e. a worst-case use certificate rather than a claim about the branch actually taken.

### Theorem T2.1 — static warrant is never stronger than a valid trace warrant

For every trace `τ` of finite procedure `p`, `Λ_st(p) ≤ Λ_tr(τ)` in the antichain order.

**Proof.** The static product contains every factor in the trace product and possibly factors from untaken branches. In the antichain semiring, adding conjunctive factors unions evidence supports; every support of the larger product contains a support of the sub-product. Therefore the static product is below (harder to satisfy than) the trace product. Structural induction handles sequencing/parallel composition; guarded choice contributes all reachable branches statically and only the taken guard+branch to the trace. ∎

### Theorem T2.2 — bounded repetition is warrant-idempotent for an unchanged body

For `n≥1`, if each iteration uses the same procedure warrant `P` and no iteration introduces a new versioned dependency, `Λ_st(p^{≤n}) = P`, because `P⊗P=P` for antichain provenance profiles. The zero-iteration trace carries `1`.

**Important limitation.** Versioned effects, fresh evidence per iteration, state-dependent operator selection, or an unbounded loop invalidate this simplification and must be represented in the trace. This theorem is about the static warrant of an unchanged bounded control object, not runtime termination (MEG-30) or probabilistic execution.

**Terminal:** `MEG-10 = PROVED_SCOPE_LIMITED__FINITE_CONTROL_TRACE_STATIC_SEPARATION`; KAT remains parent-owned.

---

## T3 — MEG-11: small-step preservation/progress for the required canonical pipeline

Consider the required pipeline stages

`GROUND → NAVIGATE → EXTRACT → COMPOSE → CHECK → COMMIT`

where every required pre-commit stage returns one of `PASS`, `FAIL`, `CANNOT_CHECK`, `PROPOSAL`, and the candidate truth state is `LIVE/DEAD/UNKNOWN`.

### Operational rules

1. `PASS` advances to the next stage.
2. `FAIL` ends at typed `FAIL`.
3. `CANNOT_CHECK` ends at typed `CANNOT_CHECK` and is absorbing for this attempted commitment.
4. `PROPOSAL` ends at `PROPOSAL`; adoption is external to the solve derivation.
5. `COMMIT` is enabled only after every required stage is `PASS`, candidate truth is `LIVE`, and the separate authority/commit gate passes.

### Theorem T3.1 — progress

Every finite pipeline state is either terminal or has exactly one next required stage. No state is silently stuck.

**Proof.** Case split on stage index and the four stage results. The stage list is finite. Each non-PASS result maps to a typed terminal; PASS increments the index; after the final PASS, the commitment gate yields COMMIT or REFUSE_COMMIT. ∎

### Theorem T3.2 — preservation of epistemic safety

If the pipeline returns `COMMIT`, no required predecessor stage returned `FAIL`, `CANNOT_CHECK`, or `PROPOSAL`; the committed candidate was `LIVE` and the commitment authority predicate held.

**Proof.** Immediate by inversion on the only COMMIT rule. Inductively, the only rule reaching the final gate is PASS advancement. ∎

The exact checker enumerates all `4^5=1024` required-stage status vectors and catches a mutant that ignores an intermediate `CANNOT_CHECK`.

**Boundary:** this proves the abstract runtime contract. ORION-OCM still needs a parity/refinement test showing its concrete event/solve implementation implements these rules.

**Terminal:** `MEG-11 = PROVED_SCOPE_LIMITED__REQUIRED_PIPELINE_SEMANTICS`.

---

## T4 — MEG-12: per-input version-space warrants for finite hypothesis classes

Let finite hypothesis class `H` map inputs to outputs. For certified examples `E={(e_i,x_i,y_i)}`, let `V(J)` be hypotheses consistent with example subset `J⊆E`.

For query `x` and value `y`, define the **version-space warrant profile**

`VSW(x,y) = Min{ ids(J) : V(J)≠∅ and ∀h∈V(J), h(x)=y }`.

### Theorem T4.1 — VSW is sound

Every support `J` in `VSW(x,y)` is sufficient, relative to the registered hypothesis class, to entail the prediction `y` at `x`.

**Proof.** This is exactly the membership predicate used to construct the profile. Minimalization removes redundant supersets but cannot remove the entailment property. ∎

### Theorem T4.2 — exact correction locality

For the certified VSW profile, revoking example `e` kills the prediction `y` exactly when every minimal support contains `e`; if at least one minimal support avoids `e`, the prediction remains LIVE. Thus correction is per-input rather than whole-procedure by default.

**Proof.** KSO liveness is existence of a support disjoint from the revoked set. Substitute `VSW(x,y)` into that definition. ∎

The checker uses an even-parity class where two examples jointly infer an unobserved third output; revoking either essential example kills only that inferred claim, while a directly supported different input survives an unrelated revocation.

**Boundary:** finite/enumerable registered classes with exact consistency checking. Infinite grammar identification remains MEG-34.

**Terminal:** `MEG-12 = PROVED_SCOPE_LIMITED__FINITE_VERSION_SPACE_PER_INPUT_WARRANT`.

---

## T5 — MEG-13: structured gap-learning soundness on finite/enumerable exact classes

For current certified examples `E` and registered query family `Q`, let `V(E)` be the nonempty version space.

### Admission rule

- if `V(E)=∅`: return `CONTRADICTION` (never average incompatible examples);
- if some `q∈Q` has more than one output among `V(E)`: return `GAP_AMBIGUOUS`;
- otherwise admit the query-relative predictions, each carrying its MEG-12 VSW profile.

Global hypothesis uniqueness is **not** required if all surviving hypotheses agree on the registered query family.

### Theorem T5.1 — query-relative admission is sound

Every admitted answer on `Q` is shared by all hypotheses consistent with the evidence; therefore it is correct relative to the registered class/evidence assumptions even when `|V(E)|>1` globally.

### Theorem T5.2 — ambiguity and contradiction are fail-closed

An ambiguous query cannot be promoted; an inconsistent evidence set produces `CONTRADICTION`. Existing atoms outside the explicit admission dependencies are unchanged (S5).

The checker includes: inferred held-out output, two distinct hypotheses agreeing on the registered query without global uniqueness, an ambiguous query, and contradictory labels.

**Boundary:** this closes the finite/enumerable exact-class core of KS-T13. It does not prove identification of unrestricted natural-language grammar classes.

**Terminal:** `MEG-13 = PROVED_SCOPE_LIMITED__FINITE_ENUMERABLE_QUERY_RELATIVE_GAP_LEARNING`.

---

## T6 — MEG-15: discriminating interaction is observation only when the outcome function is registered

Let current version space be `V`, action `a`, and registered exact outcome function `g(h,a)`. If the environment returns observed outcome `o`, define

`V'={h∈V : g(h,a)=o}`.

### Theorem T6.1 — registered interaction elimination is sound

If the true hypothesis `h*` was in `V` and the observation is exact `o=g(h*,a)`, then `h*∈V'`. Therefore the observation may eliminate hypotheses without eliminating the truth under the registered model.

**Proof.** Substitute `h*` into the definition of `V'`. ∎

### Theorem T6.2 — unregistered reward remains feedback, not evidence

If no registered outcome semantics maps the endpoint/reward to a proposition about the target hypothesis, the event may update behavior/routing (merged MEG-08) but leaves the warrant/version-space state unchanged.

This resolves the apparent tension between KS-T18 (“feedback cannot warrant”) and grounded interaction: the evidential object is the **registered observation of an outcome proposition**, not raw approval/reward.

**Terminal:** `MEG-15 = PROVED_SCOPE_LIMITED__REGISTERED_EXACT_OUTCOME_OBSERVATION`.

---

## T7 — MEG-19 corrected: macro maintenance locality, not “every factor change changes the macro”

Let summary `m` be a pure content function of registered constituent digests `χ(X_c)`, exception set `L_exc`, and exported warrant factors `X_e`, with summary warrant `Λ_corr ⊗ ⨂_{x∈X_e} Λ(x)`.

The atlas provisional wording said the summary liveness changes **iff** some exported factor liveness changes. The reverse implication is false: if the summary is already DEAD due to one factor, another factor may change without changing the summary verdict.

### Theorem T7.1 — corrected warrant-change direction

If none of the summary warrant factors changes liveness, the summary liveness cannot change. Equivalently, if summary liveness changes, at least one factor's liveness changed. The converse is not guaranteed.

**Proof.** Summary liveness is the strong-Kleene conjunction of the factor liveness values (KS-T21). A deterministic function cannot change when no argument changes. Counterexample to converse: `DEAD ∧ LIVE = DEAD` and changing the second factor to DEAD leaves the result DEAD. ∎

### Theorem T7.2 — content recheck is provenance-local by construction

If summary content is a pure function only of `X_c` and `L_exc`, then a state delta requires content recheck iff it changes a bound constituent/exception digest. With an inverted provenance index, work is proportional to affected bound records, not global KSO size.

### Theorem T7.3 — semantic equivalence without a closure/sufficiency certificate is `CANNOT_CHECK`

A compressed macro may not answer merely because its warrant is LIVE. Equality `⟦m⟧=⟦G⟧` on a query scope requires the MEG-20 sufficiency/closure certificate; absence is not false, it is `CANNOT_CHECK`/`REFINE_REQUIRED`.

**Boundary:** deconsolidation/library-selection policy remains DreamCoder/LILO/MDL parent territory unless a new residual is shown.

**Terminal:** `MEG-19 = PROVED_WITH_CORRECTION__MAINTENANCE_LOCALITY_HALF`; deconsolidation is not claimed.

---

## T8 — MEG-21: conservative non-quotient extension preserves registered predecessor behavior

For a representation extension `ι:K→K'`, define a **registered conservative extension** for query family `Q` when:

1. `ι` is injective and preserves predecessor object identities, warrants, authority and scope;
2. all predecessor transition weights among image states are unchanged;
3. for every `q∈Q`, registered predecessor seed mass has no new transition leakage from the image into newly added states (unless that leakage is explicitly part of a new, separately evaluated query identity);
4. rollback quarantines extension-only active structure and restores the predecessor active transition relation.

### Theorem T8.1 — fixed-point preservation on registered predecessor queries

Under 1–3, the restart fixed point on the image is exactly the predecessor fixed point for every registered `q∈Q` and revocation in the bound family.

**Proof.** The image submatrix and seed are identical and closed under the transition for those queries. Every term of the predecessor Neumann series therefore equals the corresponding image term in `K'`. ∎

### Corollary — exact rollback

Under 4, quarantining the extension returns the active predecessor state/transition relation exactly; MEG-18 supplies the warrant/history discipline.

A planted extension that diverts half an old transition to a new state fails the checker.

**Boundary:** this is a sufficient conservative-extension theorem, not an “iff” characterization of every useful representation change. New-query gains need separate evaluation.

**Terminal:** `MEG-21 = PROVED_SCOPE_LIMITED__REGISTERED_CONSERVATIVE_EXTENSION`.

---

## T9 — MEG-28: Jump preservation half under additive/quarantine DPO-style rewrites

Graph transformation/DPO theory owns the rewrite machinery. The Machine Epistemics preservation contract is:

- a Jump proposal identifies a preserved interface `I` and extension/removal sets;
- identities/payloads/warrants of `I` are immutable through adoption;
- newly active structure is marked by the Jump lineage/certificate;
- removed predecessor structure is quarantined, never erased from history;
- adoption remains an external constitution action; a proposal cannot self-adopt;
- registered predecessor obligations are checked under MEG-21/MEG-18 conditions.

### Theorem T9.1 — interface preservation

For an injective additive rewrite that never overwrites members of `I`, every interface object's identity/payload/warrant is unchanged. This is structural by construction.

### Theorem T9.2 — exact active-state rollback for additive extension

If extension-only active structure is completely identified by Jump lineage and rollback removes it from the **active** graph while retaining it in quarantine/history, the predecessor active graph is restored exactly.

The checker demonstrates this on a small feature-lift state and rejects id collision/self-adoption.

**Boundary:** the general “minimum sufficient J-level” theorem is **not closed**. It requires a decidable level-specific ceiling predicate; J2+ ceiling construction remains open research. Thus this row closes the preservation half only.

**Terminal:** `MEG-28 = PROVED_SCOPE_LIMITED__PRESERVATION_HALF__J2PLUS_CEILINGS_OPEN`.

---

## T10 — MEG-33: which side of UNKNOWN an epistemic action can resolve

For interval `I=⟦L,U⟧`, an evidence action is a **refinement** if it raises the lower bound (`L≤L'`) and/or lowers the upper bound (`U'≤U`) while preserving `L'≤U'`.

Call a **positive-support action** one that changes only `L`; call a **closure/exclusion action** one that changes only `U`. (A real experiment may do both and is classified by its actual interval effect, not its UI name.)

### Theorem T10.1 — lower-only refinement cannot resolve UNKNOWN to DEAD

If `λ_R(⟦L,U⟧)=UNKNOWN`, then `U` has a surviving possible support. Holding `U` fixed means the DEAD condition remains false, regardless of how `L` is raised. Therefore a lower-only refinement yields UNKNOWN or LIVE, never DEAD.

### Theorem T10.2 — upper-only refinement cannot resolve UNKNOWN to LIVE

At UNKNOWN, `L` has no surviving exhibited support. Holding `L` fixed means the LIVE condition remains false. Therefore an upper-only refinement yields UNKNOWN or DEAD, never LIVE.

### Consequence for epistemic action value

The scalar/action-selection objective (VOI, cost, risk) is parent-owned decision theory. The Machine Epistemics contribution is the typed effect model: actions that acquire positive support and actions that close/exclude possible support have different reachable epistemic transitions and cannot substitute silently for each other.

The exact checker exhausts all valid n=2 intervals/refinements/revocations and includes explicit UNKNOWN→LIVE and UNKNOWN→DEAD witnesses.

**Terminal:** `MEG-33 = PROVED_SCOPE_LIMITED__INTERVAL_REFINEMENT_ACTION_EFFECTS`; optimal action selection remains parent-owned/contextual.

---

# Batch-3 terminal

```text
MEG-05 = PROVED_SCOPE_LIMITED__DISCOURSE_STATE_NONLAUNDERING
MEG-10 = PROVED_SCOPE_LIMITED__FINITE_CONTROL_TRACE_STATIC_SEPARATION
MEG-11 = PROVED_SCOPE_LIMITED__REQUIRED_PIPELINE_SEMANTICS
MEG-12 = PROVED_SCOPE_LIMITED__FINITE_VERSION_SPACE_PER_INPUT_WARRANT
MEG-13 = PROVED_SCOPE_LIMITED__FINITE_ENUMERABLE_QUERY_RELATIVE_GAP_LEARNING
MEG-15 = PROVED_SCOPE_LIMITED__REGISTERED_EXACT_OUTCOME_OBSERVATION
MEG-19 = PROVED_WITH_CORRECTION__MAINTENANCE_LOCALITY_HALF
MEG-21 = PROVED_SCOPE_LIMITED__REGISTERED_CONSERVATIVE_EXTENSION
MEG-28 = PROVED_SCOPE_LIMITED__PRESERVATION_HALF__J2PLUS_CEILINGS_OPEN
MEG-33 = PROVED_SCOPE_LIMITED__INTERVAL_REFINEMENT_ACTION_EFFECTS
GENERAL_NOVELTY = NOT_ESTABLISHED
FIELD_STATUS = NOT_ESTABLISHED
```

## Remaining frontier after Batches 1–3

The core foundation is now much narrower. Still open are:

- **MEG-07** reaction-surprise/background guarantee (the OCM 47/50 development result is not a theorem and still has three attributed misses);
- **MEG-09** multiscale/fibred navigation (open research);
- **MEG-14** channel-specific learning/sample bounds (parent-owned adoption/table work);
- **MEG-23** learned organization/topology search (open research);
- **MEG-24** full translator invariance beyond canonicalization (empirical/protected);
- **MEG-25** renderer capability/semantic non-laundering: capability half can be specified, but semantic equality still depends on MEG-24 and protected language evidence;
- **MEG-27** incremental prefix commitment (open research/language-stage);
- **MEG-32** equivalence-margin/TOST discipline (parent-owned adoption/evaluation policy);
- **MEG-34** infinite-class construction identifiability up to lifecycle equivalence (open research).

These are not silently promoted. A foundation registry may call the mathematical/control **core** substantially closed after this batch, but the field/frontier remains open until these rows obtain their own terminals or are explicitly parent-owned/CANNOT_CHECK.

# Machine Epistemics Field Dynamics V1

Parent issue: #345. Base: `05f08fe71466d4dd192294fe00cf26d526026522`.

This file defines the dynamics over the registered state `Ξ` from `FIELD.md`. Each law below is either derived from already registered Machine Epistemics results, a scoped theorem in this package, parent-owned, or explicitly open. No finite checker upgrades an all-size claim.

## 1. Seven transition families

Write `Ξ --τ--> Ξ'` for an admissible transition.

### F — fast inference

`F_q`: atomize → seed → navigate → fire → extract → compose → check.

A fast step may change transient activation, traces and candidate sets. It may **not** add truth warrant, external authority, evidence identity, scope, or world state. Under a fixed registered snapshot it either converges within the declared numerical/budget contract or terminates with a typed non-success result.

### E — evidence and revision

`E_e`: admit, revoke, reinstate, supersede, expire, add/remove a registered contradiction/nogood under the applicable protocol.

Warrant changes only through explicit support/certificate changes. `reinstate(e)` and `relearn(e')` are different transitions even if current behaviour becomes equal.

### L — learning

`L_o`: a registered instruction, demonstration, observation, interaction outcome, experiment or other acquisition event updates a compatible hypothesis/model class and may admit query-relative procedures with provenance.

An exact/registered observation may eliminate hypotheses. Unregistered reward/feedback may update routing or weights but does not change truth warrant.

### R — representation and organisation

`R_J`: quotient/abstraction, consolidation, conservative extension, fibre split/merge/relink, operator-library change, or governed Jump.

A quotient is reusable only under the registered sufficiency conditions: navigation lumpability/intertwining, warrant measurability and answer-factorization for the registered query/revision family. An additive structural change carries lineage/adoption evidence and supports exact quarantine rollback. A governed Jump additionally requires a registered obstruction/ceiling certificate and external adoption authority.

### T — temporal/environment

`T_x`: exogenous revision of the registered world/model context. The machine may or may not observe the change immediately.

Persistence is always relative to a registered revision envelope. Missing upper closure is `CANNOT_CHECK`, not evidence that no change occurred.

### M — communication and multi-agent

`M_msg`: testimony, dialogue commitment, shared evidence, codec/meaning transfer, rendering and distributed update between machine or human/machine epistemic states.

Speaker/source authority does not become world-truth authority through repetition. Shared assumptions remain shared after composition; independence must be separately warranted.

### G — governance, action and self

`G_u`: query, experiment, clarification, abstention, external action proposal/commit, self-diagnosis, self-change proposal, shadow evaluation, external adoption and rollback.

Truth warrant, bounded-risk actionability and action permission are different coordinates. Self-model evidence may diagnose or propose; it cannot self-authorize.

## 2. FD-01 — authority non-amplification

**Status: `DERIVED_FROM_EXISTING_FOUNDATION`.**

For every internal transition and authority coordinate `c`, the authority of a derived object is bounded above by the meet of its operator/bridge and input authorities. In particular an internal operator whose `commit` coordinate is bottom cannot derive positive external-commit authority from its tails.

Only a registered external-authority source may add positive commit authority. This is a lattice/information-flow rule, not evidence that a particular external source is legitimate.

## 3. FD-02 — warrant/source conservation

**Status: `DERIVED_FROM_EXISTING_FOUNDATION`.**

Every `LIVE` derived object has at least one consistent registered support alternative after dependence flattening and post-composition nogood filtering. A navigation score, neural confidence, rank, retrieval frequency or statistical population guarantee is not itself an individual truth support.

If all candidate supports are removed, contradicted, outside scope, or only upper/possible supports, the result is not silently `LIVE`.

## 4. FD-03 — local revision law

**Status: `DERIVED_FROM_EXISTING_FOUNDATION`, relative to an explicit dependency model.**

Let `Δ` be the set of atoms/evidence whose registered liveness/value changed. Let `Impact_D(Δ)` be the least dependency-closed set. Objects outside the cone retain their registered warrant/liveness under that dependency model; objects inside are obligations to reopen or recheck, not automatic retractions.

This theorem gives no authority that `D` contains every hidden dependency. Dependency completeness is a separate model-closure obligation.

## 5. FD-04 — fast/slow fixed-point stability

**Status: `PROVED_SCOPE_LIMITED`.**

Let `P,P'` be nonnegative row-substochastic matrices, `s,s' ≥ 0` with `||s||_1,||s'||_1 ≤ 1`, and `α∈(0,1]`. Define the unique restart fixed points

`a*  = α s  + (1-α) P^T  a*`

`a*' = α s' + (1-α) P'^T a*'`.

Then

`||a*' - a*||_1 ≤ ||s'-s||_1 + ((1-α)/α) ||P'-P||_∞`,

where `||M||_∞ = max_i Σ_j |M_ij|`.

### Proof

Set `β=1-α` and `d=a*'-a*`. Subtract the fixed-point equations:

`d = α(s'-s) + β P^T d + β(P'-P)^T a*'`.

For a nonnegative row-substochastic `P`, `||P^T z||_1 ≤ ||z||_1`. Also the restart fixed point has `||a*'||_1≤1`. Therefore

`||d||_1 ≤ α||s'-s||_1 + β||d||_1 + β||(P'-P)^T||_1 ||a*'||_1`

`≤ α||s'-s||_1 + β||d||_1 + β||P'-P||_∞`.

Since `1-β=α`, division by `α` gives the stated bound. ∎

Interpretation: a slowly changing seed/kernel yields a quantitatively controlled change in the **activation fixed point**. This is not a bound on truth, semantic correctness, warrant, or answer stability unless the downstream decision also has a registered margin/certificate.

The exact checker enumerates 20,736 two-state kernel/seed pairs as a finite hostile calibration; the all-size statement is the proof above.

## 6. FD-05 — epistemic hysteresis and reversibility

**Status: `PROVED_SCOPE_LIMITED`.**

There are different notions of return:

- **state-reversible:** restoring the same immutable evidence identity and registered structure can restore the same semantic state;
- **behaviour-reversible:** a new evidence identity may restore the same current answers while changing future revocation/reopening behaviour;
- **irreversible:** an external world effect, deleted history, unquarantined structure, changed model semantics or lost evidence identity prevents exact inverse replay.

Thus `revoke(e); reinstate(e)` can be an exact inverse inside the registered append-only model, while `revoke(e); relearn(e')` is generally lifecycle-distinct. Structural adoption followed by rollback is exact only when produced structure and caches are lineage-stamped/quarantined and the predecessor representation is recoverable.

## 7. FD-06 — epistemic persistence and viability

**Status: `PARENT_SUFFICIENT` for the general controlled-invariance mathematics; Machine Epistemics supplies the typed safe set.**

For a registered commitment define a viable state as one in which:

1. required propositions have the required liveness/contradiction status;
2. scope and epoch apply;
3. required authority is present;
4. statistical/risk conditions meet the declared task contract when the action uses them;
5. the relevant property remains valid through the declared revision envelope until the commitment linearization point;
6. resource budget permits the required checks/action.

For an uncontrolled finite revision relation `T` and property set `P`, persistent validity is the parent safety kernel

`K(T,P)=S \ Pre_T^*(S\P)`.

For controlled epistemic actions, the natural extension is the viability kernel: the largest state set from which at least one admissible epistemic action can keep the state inside the registered viable set against the specified environment/revision model. Parent viability/control theory gets first right of refusal; no ORION novelty is claimed by naming the safe set epistemically.

## 8. FD-07 — information/interface conservation

**Status: `OPEN_RESEARCH`; several finite/class-specific fragments are already parent-owned/proved.**

Conjectured field principle: a warranted reduction in registered uncertainty cannot exceed the discriminating information supplied by the allowed observations, certificates, queries, interventions and prior model restrictions once their information/resource content is charged.

For finite version spaces one coordinate is `log2|V_before|-log2|V_after|`; it telescopes along nested updates. It is **not** a universal entropy or a law for arbitrary continuous/neural state. Query information, closure/exclusion certificates and causal interventions affect different epistemic coordinates and cannot be collapsed to one scalar without assumptions.

A valid general theorem needs an explicit access model and a strongest communication/decision-tree/information-theory parent. This package deliberately does not promote it.

## 9. FD-08 — commuting abstraction and structural change

**Status: `PARENT_SUFFICIENT` for finite quotient dynamics plus Machine-Epistemics measurability gates; conservative-extension part `PROVED_SCOPE_LIMITED`.**

For a finite quotient map `q`, fast dynamics commute with projection when the registered transition kernel is strongly lumpable/intertwined on each required revocation state. Epistemic reuse additionally requires warrant and answer measurability on the quotient.

For a conservative extension `ι:Ξ→Ξ'`, every predecessor registered query/liveness result must embed unchanged on the image. If inference/revision/abstraction do not commute, the correct result is `REFINE_REQUIRED` or reopen—not silent reuse of the old certificate.

## 10. FD-09 — multi-agent non-laundering

**Status: `PROVED_SCOPE_LIMITED` for authority/dependence preservation; quantitative fusion remains conditional/open.**

A testimony/communication transition preserves source identity, shared dependencies, scope and authority. Repetition does not raise `world_truth`; a chorus that shares one assumption is still dependent on that assumption.

Numerical fusion of multiple fallible witnesses/verifiers requires an explicit dependence/coupling model. Distinct process, prompt, seed, model or machine identity is not by itself an independence certificate.

## 11. FD-10 — self-model separation

**Status: `DERIVED_FROM_EXISTING_FOUNDATION` (batch 5).**

The self-model fibre `K_self` contains observations, diagnostics, predictions, proposals and assurance receipts about the machine. It has no automatic object-world or external-commit authority. Shadow evaluation is non-interfering with object state; self-change proposals require pre-outcome predictions, held-out evaluation and an external adoption source. Rollback follows stamped lineage.

## 12. FD-11 — resource monotonicity / no-free-representation

**Status: `PROGRAMME_CONTRACT` with parent lower-bound/frontier work open.**

Every epistemic transition has a resource delta over the registered vector: immutable description, mutable memory, sequential time, total work, I/O/bandwidth, verifier cost, preprocessing/index/parser cost, training/acquisition cost and any other explicitly relevant resource.

Changing representation may reduce one coordinate and increase another; it cannot erase a real resource by moving it outside the accounting boundary. Claims of superiority are Pareto/resource-scoped, not parameter-count-only.

## 13. FD-12 — typed terminal completeness

**Status: `PROVED_SCOPE_LIMITED` for finite registered transition grammars.**

A finite registered pipeline/control grammar must terminate in an explicit result rather than an untyped stuck state. The vocabulary may include `PASS`, `FAIL`, `LIVE`, `UNKNOWN`, `DEAD`, `CONTRADICTED`, `GAP`, `OBSTRUCTION`, `REFINE_REQUIRED`, `REOPEN_REQUIRED`, proposal/adoption results, resource exhaustion and `CANNOT_CHECK`.

`CANNOT_CHECK` is absorbing for any downstream assertion that requires the unavailable premise/check; it is never converted to PASS by omission.

The exact checker enumerates a finite six-stage status grammar and a planted “ignore CANNOT_CHECK” mutant.

## 14. Dynamical regimes

These are state-machine regimes, **not physical phases**:

- `STABLE_INFERENCE` — F dynamics under a fixed valid state;
- `REVISION` — E transition followed by local reopening;
- `DRIFT` — T invalidates a scope/model/certificate coordinate;
- `CONTRADICTION` — N eliminates a joint support;
- `SATURATION` — registered lower-level search is complete for the declared family;
- `OBSTRUCTION` — a checked lower-level ceiling blocks the goal;
- `JUMP_PROPOSED` — R proposal exists but has no adoption authority;
- `ADOPTED` — external G transition stamps a representation/organisation change;
- `DISTRIBUTED_UNCERTAINTY` — communication/coupling assumptions are insufficient;
- `CANNOT_CHECK` — a required premise, checker, closure or resource is unavailable.

The frontier is to understand transitions between these regimes under incomplete, nonstationary and multi-agent environments without assuming the answer into the model.
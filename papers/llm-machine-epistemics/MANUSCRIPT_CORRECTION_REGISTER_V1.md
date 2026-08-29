# Manuscript Correction Register V1

**Issue:** #51  
**Base manuscript:** `MANUSCRIPT_DRAFT_V8_CITED.md`  
**Purpose:** freeze small post-V8 scientific corrections that the mechanical LaTeX assembler must apply without rewriting the manuscript's argument.

## Correction CR-01 — submission abstract

Replace the 208-word V8 research abstract with the 157-word abstract from `SUBMISSION_FRONTMATTER_V1.md`.

Reason: current JMLR title-page limit is <=200 words and the shorter abstract is also tighter editorially.

## Correction CR-02 — Section 10 collision language

### Problem

V8's pairwise prospective-revision collision is a valid **sufficient failure witness** but is not a complete compatibility test when more than two histories share a representation/evidence cell and acceptable future-action sets contain ties.

Example:

```text
A1 = {a,b}
A2 = {b,c}
A3 = {a,c}
```

Every pair intersects, yet the three-way intersection is empty.

### Required replacement heading

Change:

`# 10. Prospective revision collision certificates`

to:

`# 10. Prospective revision compatibility and collision certificates`

### Required replacement text

Use the following scientific content:

> For a representation value `z` and common future evidence event `x`, let `C(z,x)` be the set of registered histories with representation `z` for which `x` is feasible, and let `A_x^*(h)` be the acceptable future-action set after `x`. Define
>
> \[
> I(z,x)=\bigcap_{h\in C(z,x)}A_x^*(h).
> \]
>
> Under exact one-step `ANY_OPTIMAL_ACTION` semantics, a deterministic future rule using only `(z,x)` can be acceptable for every history in the cell iff `I(z,x)` is nonempty. Necessity follows because one output action must belong to every acceptable set; sufficiency follows by selecting any action from the intersection. A pair of histories with disjoint future acceptable-action sets is therefore an easy positive failure certificate, but absence of such a pair is not sufficient in general: `{a,b}`, `{b,c}`, and `{a,c}` overlap pairwise while their joint intersection is empty. The canonical one-bit witness has singleton future-action sets, so its pairwise `REOPEN`/`RETAIN` collision remains complete. The criterion is ordinary decision-sufficiency/intersection logic; the contribution is its use as an audit diagnostic rather than a new mathematical theorem.

Source/proof:

`research/llm-machine-epistemics/PROSPECTIVE_REVISION_COMPATIBILITY_CRITERION_V1.md`

### Required downstream wording changes

Where V8 says “collision certificates” as though they were exhaustive, replace with:

- `compatibility/collision certificates`, or
- `joint compatibility test with pairwise collision witnesses`.

## Correction CR-03 — Representation Audit Profile metric

In any future empirical-metrics table:

- primary structural metric: `incompatible representation/evidence cell count/rate` based on empty **joint** acceptable-action intersection;
- secondary diagnostic: `pairwise disjoint-set collision count/rate`.

Do not use zero pairwise collisions as a positive adequacy terminal unless all future action sets are singleton.

## Correction CR-04 — Protocol V2 amendment

Protocol V2 remains authoritative for all other controls, but its pairwise-collision language is amended by:

`research/llm-machine-epistemics/PROSPECTIVE_REVISION_COMPATIBILITY_CRITERION_V1.md`.

The LaTeX package should cite both protocol files or materialize their merged semantics.

## Correction CR-05 — claim ledger

Use `CLAIM_LEDGER_V6.json`, not V5, for final claim-status validation.

V6 adds C19 as a parent-style complete one-step compatibility criterion and explicitly classifies pairwise collision as sufficient-but-not-complete.

## Correction CR-06 — current paper status

The compatibility correction does **not** change:

- the one-bit no-certification theorem;
- `C_stat^*=0`, `C_dyn^*=1`, `Omega_dyn=1`;
- P0/P1/P2 taxonomy;
- strongest-parent contraction;
- JMLR/TMLR route;
- empirical nonclaims.

It makes the prospective audit more diagnostically complete.

## Correction CR-07 — predictive target must be channel/protocol scoped

### Problem

V8 sometimes says “complete linguistic future” without explicitly naming the input/evidence protocol. Read literally as **every possible future interactive input, evidence intervention, output and decision**, that phrase is too strong: a representation sufficient for such a joint controlled future may already be forced to retain the provenance bit used in the one-bit witness.

### Required scope

Treat the reference predictive state as

\[
S_{P,\rho}
\]

for a registered linguistic reference input protocol/channel `rho`:

\[
h\sim_{P,\rho}h'
\iff
P(Y^+_\rho\mid h)=P(Y^+_\rho\mid h').
\]

The later evidence event `x` belongs to a separately registered controlled/exogenous intervention family rather than being silently included in the reference prediction target.

### Required wording changes

Replace unqualified instances of:

> “state sufficient for the complete linguistic future”

with either:

> “state sufficient for the complete declared linguistic future under the registered reference input protocol”

or, where brevity is needed:

> “state sufficient for the registered linguistic prediction target.”

### Required theorem interpretation

The no-certification theorem says:

> equality on the registered current linguistic prediction target and current responsibility does not imply equality on a later evidence-conditioned responsibility when the later controlled intervention distinguishes histories inside the current evaluation equivalence classes.

It does **not** say that a state sufficient for every possible controlled future/intervention can still discard load-bearing intervention information.

### Required parent control

State that a representation explicitly sufficient for the joint controlled future across the registered evidence-intervention family is a stronger PSR/POMDP/AIS-like parent control. Under that stronger target, the provenance distinction may become present-state-relevant and the prospective premium can contract to zero.

### Protocol fields

Every empirical audit must separately freeze:

```text
prediction_reference_protocol
present_linguistic_target
current_responsibility
future_evidence_intervention_family
future_responsibility
```

Source:

`research/llm-machine-epistemics/PREDICTION_CHANNEL_AND_INTERVENTION_SCOPE_V1.md`

## Correction CR-08 — controlled-sufficiency positive control

Add to the protocol/limitations:

- a condition whose reference state is deliberately sufficient for the joint controlled target that includes the future evidence family;
- expected result: the formerly dormant distinction can become present-state-relevant and P2 may contract to P0/P1.

This demonstrates that the audit is channel/responsibility-relative rather than a universal memory law.

## Assembly gate

Any target-format manuscript built from V8 without CR-01, CR-02, and CR-07 is **not** the current scientific surface.

Terminal after all corrections:

`V8_CORRECTIONS_APPLIED__SUBMISSION_SCIENCE_CURRENT`.

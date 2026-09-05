# MEG-02 V1 — statistical warrant is not individual truth; risk-bounded actionability is a separate type

Status: **FOUNDATION CANDIDATE. Exact/hostile checker accompanies this note. NO NOVELTY OR ARCHITECTURE-SUPERIORITY CLAIM.**
Parent issue: `#319`. Atlas identity: `MEG-02`.
Checker: `machine_epistemics_foundation_v1_check.py`.

## 0. Defect being closed

A statistical statement such as

> a registered prediction procedure has coverage at least `1-δ` under assumptions `A` on scope `S`

is a proposition about a **procedure/population regime**. It is not the same proposition as

> this particular candidate output is true.

The foundation therefore forbids a direct coercion

`coverage receipt -> individual world-truth LIVE`.

A statistical/neural operator may emit scores, sets, distributions or ranked candidates. Those are useful state, but the score coordinate lives outside the truth-warrant lattice unless a distinct per-instance warranting channel supplies a certificate.

This is the load-bearing split needed by OCM M2 and every later language/tool/action layer.

## 1. Types

### 1.1 Candidate truth object

For a candidate proposition `p`, the machine stores:

- `truth_status(p) ∈ {LIVE, DEAD, UNKNOWN}`;
- its warrant interval `Λ(p)`;
- authority and scope;
- optional statistical metadata such as score, rank, prediction set, calibration receipt id.

A statistical score or coverage receipt alone does not alter `Λ(p)`.

A candidate emitted only by a statistical/neural operator therefore starts `UNKNOWN` unless a separate truth-warranting channel is present.

### 1.2 Statistical meta-claim

A coverage/calibration certificate warrants a **meta-claim** of the form

`Calibrated(B, G, δ, A, S, e)`

where:

- `B` is the exact behavior identity of the operator/pipeline;
- `G` is the guarantee kind, for example marginal coverage;
- `δ` is the registered error level;
- `A` is the assumption set;
- `S` is scope;
- `e` is epoch/calibration validity.

This certificate may itself be LIVE as a scoped claim. That does not make any member candidate LIVE.

### 1.3 Actionability object

Actionability is a different judgement:

`Actionable(policy, candidate, certificate)`

with terminal values including:

- `AUTHORIZED_RISK_BOUNDED`;
- `NOT_AUTHORIZED_RISK_BUDGET`;
- `NOT_AUTHORIZED_GUARANTEE_KIND`;
- `REVALIDATE_IDENTITY_DRIFT`;
- `REVALIDATE_SCOPE_DRIFT`;
- `REVALIDATE_ASSUMPTION_DRIFT`;
- `REVALIDATE_EPOCH_DRIFT`;
- `CANNOT_CHECK`.

A policy must name its accepted guarantee kinds, risk budget, scope, assumptions and epoch.

`AUTHORIZED_RISK_BOUNDED` authorizes an action **under that decision contract**. It does not change `truth_status(candidate)`.

## 2. Foundation statements

### MEG-02A — no score-to-truth coercion

If `p` has no EXACT_CHECKER/OBSERVATION (or another separately registered per-instance truth certificate), then changing only a statistical score, confidence, rank, prediction-set membership or marginal coverage receipt leaves `truth_status(p) = UNKNOWN`.

The checker plants a mutant that promotes a candidate to LIVE whenever a coverage receipt has error at most 5%; the mutant is rejected.

### MEG-02B — marginal coverage warrants a procedure-level claim

Under the certificate's exact assumptions and scope, a marginal coverage receipt may warrant `Calibrated(B,G,δ,A,S,e)`.

It does **not** warrant `p` for a particular instance. Exact distribution-free conditional coverage for arbitrary individuals is not generally available without additional assumptions; therefore the foundation never silently interprets a marginal guarantee as an individual truth guarantee.

### MEG-02C — truth and action commute only by non-interference

Let `T(p)` be the truth-warrant state and `D(p,π,C)` the decision/actionability state under policy `π` and certificate `C`.

A change in `D` does not change `T` unless a separately registered truth-warranting event occurs.

Thus it is valid to have:

`T(p) = UNKNOWN` and `D(p,π,C) = AUTHORIZED_RISK_BOUNDED`.

This is not a contradiction. It is the expected state for many low-risk, reversible decisions made under calibrated uncertainty.

### MEG-02D — risk-budget monotonicity

For the same valid certificate and policy family, if policy `π1` permits error budget `ε1` and `π2` permits `ε2` with `ε1 <= ε2`, then authorization under `π1` implies authorization under `π2`, all other bindings equal.

The reverse does not follow.

### MEG-02E — drift is fail-closed

A certificate is reusable only when its bound behavior identity, assumptions, scope and epoch exactly match the current invocation and policy contract.

Any mismatch routes to a typed `REVALIDATE_*` terminal. Any missing required binding is `CANNOT_CHECK`.

The detailed identity object is frozen in `OPERATOR_CERTIFICATE_IDENTITY_DRIFT_V1.md`.

## 3. What can make an individual candidate LIVE?

Foundation V1 allows the following route categories, each with its own authority/scope contract:

1. an exact checker whose result directly establishes the candidate proposition;
2. an observation/measurement certificate whose registered semantics directly establishes the candidate proposition on scope;
3. a formally stronger per-instance certificate whose theorem explicitly warrants the candidate proposition, if separately registered in V2.

A population calibration guarantee is not item 3 merely because its empirical coverage is high.

## 4. Conformal-prediction parent boundary

Conformal prediction is adopted as a parent uncertainty-quantification family, not as an ORION novelty claim.

The relevant parent boundary is:

- standard conformal guarantees are marginal under exchangeability;
- exact arbitrary conditional coverage is impossible distribution-free without additional assumptions;
- distribution/configuration shift can invalidate the calibration regime unless the method explicitly handles that shift.

A 2026 study of conformalized LLMs under prompt-template, temperature and quantization changes is directly relevant to the behavior-identity rule: the configuration is part of the calibrated procedure, not incidental metadata.

The foundation does not require conformal prediction specifically. Any statistical certificate used by OCM must state its guarantee kind and exact validity assumptions.

## 5. Hostile controls

The exact checker includes:

- `coverage -> individual LIVE` mutant: rejected;
- action allowed at 5% risk while truth remains UNKNOWN: accepted;
- the same certificate under a stricter 1% policy: refused;
- exact/observation truth certificate: may make the candidate LIVE;
- behavior/configuration/calibration/assumption/scope/epoch drift: forces revalidation;
- missing behavior-identity component: `CANNOT_CHECK`.

## 6. OCM absorption rule

OCM may absorb MEG-02 only if its parity record proves all of the following:

- statistical metadata cannot directly edit a truth-warrant interval;
- action authorization has a separate typed result;
- every statistical certificate binds the exact behavior identity;
- drift routes fail-closed;
- actionability never raises truth authority;
- tests include the score-to-truth and stale-certificate mutants.

## 7. Non-consequences

This note does not establish calibrated models as truthful, does not make risk-bounded actions safe in every domain, does not authorize high-stakes deployment without an appropriate policy/authority layer, and does not claim a new statistical theorem.

It freezes the epistemic typing rule OCM needs: **population/statistical validity, individual truth warrant, and decision actionability are different objects.**

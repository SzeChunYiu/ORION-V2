# PRA real-LLM audit, design V3 — registered successor

**Status: registered, pre-outcome, not executed.** Frozen before any V3 instance exists. This note
is the human-readable design; `PRA_REAL_LLM_AUDIT_DESIGN_V3.json` is the machine-readable
authority and is what the runner consumes. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

## 1. Why a successor exists

V2's protected terminal was `P2_SINGLE_MODEL_ONLY__REGISTERED_BOUNDARY_RESULT` (merge `3858bc4`):
the registered prospective-revision effect held on qwen2.5-32b-instruct, while
mistral-small-24b-instruct-2501 was **disqualified by its own present-equivalence gate GP0**
(per-unit pass 0.296 against the registered 0.90). Its R2→R3 movement was therefore routed
`CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE` rather than counted as support. The gate did
exactly what it was registered to do.

Three limitations were then recorded on the manuscript and could not be closed by editing:

| id | limitation |
|---|---|
| V-M1 | present equivalence was gated on the canonical fixture only; eight families report contrasts with no such precondition |
| V-M3 | the probe readings leave two explanations undiscriminated |
| V-M7 | one row precedence was adopted after unblinding |

V3 addresses all three by design, before any outcome exists.

## 2. The attribution behind the main change

Attributed to **one stage: the screen, not the model and not the thesis.**

The evidence for that attribution is in V2's own record. Mistral's failure is not marginal — under
the P1-current contrast its accuracy is 0.317 at R1 against 1.000 at R2, with 82 of 120 discordant
one way and none the other. So for that model the two conditions differ in *present* behaviour
before any prospective question is asked. That is a fact about how one model uses one
representation, and it is discoverable **on the development split, before the protected seed is
sealed**. V2 discovered it only at protected time, on one fixture, after the run had spent its
single draw.

The design already contains the right pattern for this: `GPC` screens model *competence* pre-run
on the dev split, and replaces a model that fails, with the replacement recorded. V2 simply did not
extend that pattern to *equivalence*. V3 does.

**This is not a rescue of the mistral arm.** A model that cannot hold the two representations
equivalent on present behaviour is not admitted to the protected run at all, and its exclusion is
recorded pre-run with the numbers that caused it. The point is that a present-state deficit is an
admission question, answered before sealing, not a protected-run outcome that consumes the draw.

## 3. Changes from V2

### 3.1 `GPE` — pre-run present-equivalence screen (closes V-M1)

New gate, evaluated on the **dev split, before the protected seed is sealed**, per model and
**per family** rather than on the canonical fixture only.

- Rule: for every registered family, the per-instance present-equivalence criterion of GP0
  (`|logprob(R3) − logprob(R2)| ≤ ε`, current action identical across R0/R2/R3, current action
  correct, token budgets matched) must pass on at least 0.90 of dev units, with TOST equivalence on
  the mean difference.
- A model failing `GPE` on any family is **not admitted**; it is replaced by another ungated
  open-weight instruct model that fits one A100-80GB in bf16, exactly as `GPC` already prescribes,
  and the failing numbers are recorded per family in the design note.
- `GPE` never enters GP0–GP3, the terminal mapping or the routing. It is reported in every rollup.
- GP0 is retained unchanged at protected time. Under V3 it becomes a confirmation of a property
  already established on dev, not the place where a model is discovered to lack it.

**Pre-registered expectation, stated before any V3 outcome exists:** with `GPE` in place the
protected run should admit only models for which the prospective question is well posed, so the
expected terminal is `P2_PROSPECTIVE_REVISION_STATE_REQUIRED` on **every admitted model**. If an
admitted model still fails GP0 at protected time, the screen does not transfer from dev to
protected and that is a finding about the screen, reported as
`GPE_DID_NOT_TRANSFER__SCREEN_INSUFFICIENT`. If no model passes `GPE`, the honest terminal is
`NO_MODEL_HOLDS_PRESENT_EQUIVALENCE__CONSTRUCTION_BOUND`, which would bound the construction rather
than the thesis, and is a first-class outcome.

### 3.2 Probe discrimination (closes V-M3)

V2's probe left two explanations undiscriminated. V3 registers the discriminating contrast in
advance and pre-declares what each outcome means, rather than reporting a max-over-layers statistic
whose null is not stated:

- The probe's null distribution is registered explicitly, and the chance ceiling is reported with
  the statistic so a reading cannot sit inside its own null unnoticed.
- Any statistic that is an identity under the construction is marked as such in the design and is
  not offered as a signature.
- Every probe reading carries the `detectable_ceiling` field (wired into the runner 2026-09-05), so
  a null probe result states the effect it could have registered.

### 3.3 Row precedence pre-registered (closes V-M7)

The row precedence V2 adopted after unblinding is **fixed in this design, before any V3 instance
exists**, in the exact form V2 ended up using. It is therefore pre-registered here and requires no
disclosure of post-hoc adoption in a V3 report. The V2 disclosure stands unchanged for V2.

### 3.4 Inherited, unchanged

Families, representation conditions R0–R4, decoding, token budgets, the KV channel, the
no-rescue clause, custody (the seed is sealed by commitment and revealed only in the outcome
record), and the single-protected-run rule. The runner refuses a second protected run without a
new explicit authorization.

## 4. Freeze and custody

- This note and `PRA_REAL_LLM_AUDIT_DESIGN_V3.json` are frozen at the commit that lands them; the
  JSON carries its own `design_sha256` field computed over the canonical serialization without
  that field.
- The protected seed is committed by hash in the design and revealed in the outcome record. The
  seed is generated into `~/.orion-custody/pra-llm-v3/` and never leaves operator-owned machines.
- Runner: the current `pra_real_llm_audit.py` at the commit this design lands on, recorded by
  sha256 in `frozen_inputs`. Note that this hash necessarily differs from the value V2 froze: the
  runner has since been corrected twice, for the saturating two-sided p (merge `096e6f3`) and for
  the detectable-difference ceiling. A V2 re-run must check out V2's pinned revision.
- Compute: LUNARC `gpua100`, one A100-80GB per model arm, one array task per model, as V2 ran.
  Nothing runs on the operator's Mac.

## 5. What V3 cannot fix

- It cannot make V2's single protected draw into two. V2's terminal stands as reported.
- It cannot establish anything about deployed language models; both designs are bounded to their
  registered families and open-weight models.
- `GPE` is itself a screen and can be wrong. Its failure mode is stated above and has a registered
  terminal, so it can be caught rather than assumed.
- No externally authored arm exists for either design.

## 6. Execution state

**Registered, unexecuted.** Dispatch requires a GPU allocation and a
`PROTECTED_RUN_AUTHORIZATION.json` minted from the operator's standing authorization before the
protected stage, as V2 required. The dev-split stages (`GPC`, `GPE`) run first and may run as soon
as an allocation exists; the protected stage runs only after both screens pass and the seed is
sealed.

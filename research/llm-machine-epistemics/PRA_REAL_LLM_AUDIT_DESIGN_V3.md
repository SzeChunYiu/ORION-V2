# PRA Real-LLM Audit — Pre-registered Design V3 (construct-valid alternate-channel gate)

**Issue:** #51 · **Machine-readable twin:** `PRA_REAL_LLM_AUDIT_DESIGN_V3.json`
(`schema_version orion.v2.pra.real-llm-audit-design.v3`; **authoritative for every number**).
**Runner:** `pra_real_llm_audit_v3.py` — V3's own copy. **Status:**
`FROZEN_PRE_OUTCOME__PROTECTED_RUN_NOT_AUTHORIZED`. **Scientific authority:** none.

**Compute authorization is not requested and is out of scope.** No seed is sealed, no commitment
is published, nothing is staged or submitted. The operator decides whether V3 runs at all once
V2's outcome is in.

## 0. Standing constraints this design honours

- **V2 is running.** SLURM array `3566415` (task 0 on `cg20`; task 1 queued). Its design, runner,
  sealed seed, authorization and in-flight artifacts are untouched. V3 carries its **own runner
  copy** and never imports from or edits `pra_real_llm_audit.py`, whose frozen sha256
  (`19862623…fda7f`) the V2 run depends on.
- **V1 stands.** Terminal `CONTROL_FAILURE__SUITE_NOT_INTERPRETABLE`, attributed to the revision
  stage: `F3_P2_MIRROR` false revision under R3 of **0.258** (qwen) and **0.392** (mistral)
  against ≤ 0.10. The mirror family retracts a source that is not on the claim's file, gold is
  RETAIN, and both models treat any retraction notice as a revision trigger without checking
  whether the retracted source is the recorded basis. **That is model competence, not a suite
  defect, and V3 does not redesign around it.**

## 1. What V3 repairs

`PRA_GP2A_CONSTRUCT_VALIDITY_DIAGNOSIS_V1.md` establishes, from the frozen R1 artifacts and with
no new model calls:

1. GP2a's registered R3 clause had no implementing predicate. **Shape 5: a registered clause the
   runner silently narrows.**
2. Implementing it verbatim would not have repaired anything. The V1 label `support_source
   (A=1, B=0)` is an index into the generator's source dict whose only textual footprint is the
   fixed roster order. R3 names the basis and carries no roster, so under the A↔B exchange —
   a symmetry the generator's law respects — R3's two arms map onto each other while the label
   flips. Expected accuracy of any classifier on R3 is **exactly 0.5**. The clause was
   **unsatisfiable in principle**; adding it would have produced a permanently unpassable gate
   that reads like an empirical negative.
3. The sibling clauses ("at chance under `R2_TRUE_REMOVAL`", "true removal below R0 by ≥ 0.15")
   were **unfailable in principle**: R2 renders identically across the two arms.
4. R0 = 1.000 is reproduced exactly by "is the basis the first name in the roster?" — a
   positional rule with no semantics. A lexical reader scores 0.4896 there, so the model is doing
   real relational work; **whether that work is semantic or positional is not separable in V1**.

So V3 does not add the missing check. It rebuilds the construct so that the check means something,
and makes both failure shapes machine-detectable *before* a run.

## 2. Changes from V2 (everything else is carried verbatim)

**Probe label.** `support_source (A=1, B=0)` → **the registry class of the recorded basis**
(class 1 = `{SRR, CRX, OSL}`, class 0 = `{TRK, QDB, MRG}`). An attribute the text *states*
wherever the basis is named: present in R0 and R3, absent from R2. It transforms consistently
with the text under the exchange symmetry, so it is identifiable rather than anti-invariant.

The lower-blast-radius choice was deliberate. Putting a roster into R3 would have been the other
route, but R3's content is the independent variable of contrast B — the primary result — and
adding material to it perturbs the R2→R3 comparison the whole audit rests on. Changing the label
leaves every rendered condition's information content as registered in V1.

**Presentation order randomised.** The roster and the R4 dependency ledger are rendered in a
per-instance order drawn at suite-build time and frozen into the suite. The positional rule dies
by construction. (It also confirms the label had to change: under a randomised roster the V1 A/B
label is unidentifiable even from R0.)

**Balance by construction.** Exactly one of the two candidate sources is in class 1 per instance,
so every instance contributes one unit of each class and any train/test cut is exactly 50/50 —
not balanced on average, balanced.

**`R2_TRUE_REMOVAL` removed.** V1 proved `hidden_R2.npy` and `hidden_R2_TRUE_REMOVAL.npy`
byte-identical, because "fresh cache, R2 text only" *is* the R2 computation. Keeping it reports
one measurement twice. V3 makes that impossible rather than declaring it.

**The removal limb is not re-registered as an empirical clause.** The proposition it was meant to
establish — the intervention leaves no trace of the dormant variable in the R2 representation —
is now discharged **a priori** by the identifiability certificate, which proves the two arms are
the same string. A measured 0.51 for something that could not have come out otherwise is not
evidence.

## 3. The two pre-run certificates (gate `CERT`, blocking)

Both are model-free, run from the frozen suite alone, and must pass before any protected model
call. Neither is a report to be read afterwards.

### 3a. Label identifiability

Per probed condition, over the **effective context** — for the KV condition that is the retained
R0 prefix *plus* the R2 text, because certifying the text alone would suppress the one condition
the alternate-channel gate turns on:

- **well-definedness** — no two capture units may share a context and carry different labels;
- **symmetry** — re-render each unit under the registered exchange; where the image coincides
  with an observed context, the label recomputed after the exchange must equal that context's
  label.

A condition failing either is `LABEL_NOT_IDENTIFIABLE_FROM_CONDITION`. **No accuracy is reported
for it and no gate clause may name it.** The registered identifiable set is
`["R0", "R2_TEXT_REMOVED_KV_RETAINED", "R3"]`; the observed set must equal it exactly.

The certificate itself carries a control that must match: its re-render is asserted equal to what
the runner actually shows the model, and it exits hard if not. Certifying a string the run never
uses is precisely the failure this file exists to prevent.

### 3b. Registered-clause coverage, with a reachability limb

Every clause carries an **id**, a **source path** into the analysis where its implementing
predicate must deposit a verdict, and — for probe clauses — a condition, direction and threshold.
A clause is `PASS`/`FAIL` only if the path resolves, the value is non-null, **and the clause was
reachable**. Otherwise it is `NOT_EVALUATED` or `UNREACHABLE__DESIGN_DEFECT`, and **neither may
be absorbed into a sibling clause's verdict**. Any shortfall is the hard terminal
`REGISTERED_CLAUSE_NOT_EVALUATED__SUITE_NOT_INTERPRETABLE`, which outranks every empirical
outcome.

Coverage alone would have caught V1's omission but not its unfailable sibling, so reachability is
decided from the identifiability certificate rather than from the observed number — the observed
number being exactly what a structurally determined clause cannot warn you about:

| clause shape | on a non-identifiable condition |
|---|---|
| `direction: min` (≥ t) | `UNSATISFIABLE` — no probe can reach t. *This is V1's R3 clause.* |
| `direction: max` (≤ t) | `UNFAILABLE` — holds by construction. *This is V1's `R2_TRUE_REMOVAL` clause.* |

Both halves of the V1 defect are flagged before a single model call.

## 4. Probe-validity check: the model-free surface null

Reported beside every probe accuracy, on the same stimuli and the same frozen split, using the
same mass-mean estimator on features instead of hidden states:

- a **lexical** reader (word + character-4-gram counts);
- a **relational** reader (roster slot of the matched basis, first-mention offset, names before
  the basis).

**Registered calibration requirement:** the relational reader must score ≥ 0.95 on V1's frozen R0
stimuli under V1's label. That is the known-bad case, and a null that clears V1's positional
shortcut is worthless. Verified at **1.0000** — while the lexical reader sits at **0.4896**, which
is why the null cannot be lexical only. A validity check that only ever ran the lexical reader
would have passed V1's confound.

The residual over the null is reported and does **not** silently enter the pass. A condition where
the null matches the probe licenses "the information is present in the context", never "the model
represents the variable".

## 5. Gates

`GP0`, `GP1`, `GP3`, `GPC` are carried verbatim from V2, now clause-addressed. `GP2`:

> **GP2a (required):** the probe decodes the recorded-basis attribute in **every** condition
> registered as identifiable in which the basis is named — **R0 and R3, both ≥ 0.80**.
> **GP2b (control quality):** decodes under the retained-KV condition (≥ 0.80); KV-retained
> behavioural accuracy ≥ R0 − 0.10; contrast D (R2 → KV retained) exact p ≤ 0.05, with a
> registered same-path witness.

Registered clause ids: `GP0.present_equivalence`, `GP1.contrast_B_significant`,
`GP2a.probe_decodes_R0`, `GP2a.probe_decodes_R3`, `GP2b.probe_kv_retained_decodes`,
`GP2b.kv_recovers_R0`, `GP2b.contrast_D_significant`, `GP3.p0_no_gap`,
`GP3.mirror_not_falsely_revised_under_R3`, `GP3.recon_no_gap`.

**Same-path witness.** Every contrast carries a registered witness: the identical code path shown
returning a *different* value elsewhere in the same rollup. This is what made V1's
`p0_R2_vs_R3` = 1.000 vs 1.000 a real ceiling rather than a vacuous contrast, and V3 emits it
rather than leaving a reader to reconstruct it.

## 6. Exit codes

"Could not check" never shares an exit code with "checked and fine":

| code | meaning |
|---|---|
| 0 | every registered gate evaluated; outcome recorded (pass or registered negative) |
| 3 | a registered clause could not be checked (`CANNOT_CHECK`); **no pass is implied** |
| 4 | a registered clause is unimplemented, unevaluated or unreachable (design defect) |

## 7. Silent-failure taxonomy, as implemented

| shape | V3 |
|---|---|
| 1. a counter that never ran, reporting `0 violations` | denominators published everywhere; `n_test` per condition in the rollup |
| 2. a contrast that could not exist (`1.000 vs 1.000`) | reachability limb asks "could these arms EVER have differed?" **before** the run; registered same-path witness per contrast |
| 3. a sentence nobody executed | clause coverage; and the V3 test double plants a signal that is a function of the rendered basis, so `test_stub_plants_a_signal_the_R3_clause_can_actually_test` **can fail** — V1's stub planted a constant under R3 while its docstring claimed otherwise |
| 4. a rendered status trusted in place of the thing | carried from V1: `sacct COMPLETED 0:0` is not evidence; artifacts verified before analysis |
| **5. a registered clause the runner silently narrows** | **named here for the first time.** Every clause has an id, a source path and a reachability declaration; the runner asserts the evaluated set equals the registered set; a shortfall is a hard terminal, never a pass on the half that ran |

## 8. Model identity

Carried verbatim from V1: `revision_requested` **and** `revision_resolved` (the latter from
`model.config._commit_hash` after load) recorded per stage, with `HF_HUB_OFFLINE=1`,
`TRANSFORMERS_OFFLINE=1` and local weights. Identity is **asserted, not inferred**; no
served-model substitution risk applies. Caveat kept: a snapshot revision is not a weight-shard
digest.

## 9. Seed and authorization

`suite_generator.seed.dev = 20260922`. The protected seed is **sealed and its commitment is
`PENDING_UNTIL_PRE_RUN_CERTIFICATE_PASSES_ON_DEV`.** No digest is published here, because no
sealed file backs one yet — publishing a commitment with nothing behind it would be exactly the
unexecuted sentence this design exists to prevent.

Preconditions, in order, none of them discharged by this PR:

1. the V2 protected run (array `3566415`) completes and its rollup lands;
2. the operator decides V3 should run at all, in light of V2's outcome;
3. the pre-run certificate stage passes on the dev split;
4. the protected seed is sealed on LUNARC and its sha256 published into this design **in a commit
   of its own**, as V2 did;
5. the protected run is authorized with the token in `protected_run.authorization_token`.

## 10. No-rescue clause

No post-hoc change to families, instance counts, prompts, filler, tolerances, gate thresholds,
probe label, probe split, certificates or terminal mapping. A defect discovered after unblinding
is reported as `CANNOT_CHECK` for the affected component, **with its own exit code**, and fixed
only under a new design version with a fresh protected seed.

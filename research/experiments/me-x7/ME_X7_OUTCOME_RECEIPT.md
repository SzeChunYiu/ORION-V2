# ME-X7 — Claim-Sufficient External Witnesses: Protected-Run Outcome Receipt

**Run date:** 2026-09-03
**Design:** `ME_X7_EXTERNAL_WITNESS_SUFFICIENCY_EXACT_STUDY_DESIGN_V1.json`,
sha256 `1895b4388f832b121695ba1d64c688b0a9df44264e4a3284f0d73e8684b54022`,
frozen and merged to main in PR #176 before this run.

## 0. Route

```text
ME_X7_PROTECTED_ROUTE   = CANNOT_CHECK
WITNESS_TERMINAL        = NONE
REASON                  = a hard G0 gate failed — lane defect; repair, re-freeze, no arm verdict
LANE_STATUS             = HALTED, RECEIPTED, RE-FREEZES AS V2 (design §9)
FIELD_STATUS_AUTHORITY  = NONE
```

**G0b `ORACLE_SELF_AGREEMENT` is a hard gate and it failed.** Under the
pre-registered routing table (design §7, row 1) a hard G0 failure routes
`CANNOT_CHECK` and issues **no arm verdict**. The arm numbers in §4 below are
reported as diagnosis of the defect, **not** as the study's answer. ME-X7 has
**no** witness terminal, and in particular this run does **not** establish
`PARENT_SUFFICIENT`, does **not** establish `WITNESS_CLAIM_SUFFICIENT_AT_LOWER_EXPORT`,
and does **not** establish any residual. The question ME-X7 asks is, after this
run, still open.

## 1. Seed reveal (post-run half of the pre-published commitment)

Committed in the frozen design before the run:

```text
seed_commitment.protected_seed_sha256 = 2c8a3d774cab1fcae49fae5876d9ed314ea771563fa31ff44784c3dd3e2cf4b2
```

Revealed now:

```text
PROTECTED_SEED_V1 = ME-X7-PROTECTED-b35d0617f13ec73ed96368bfb7019f603e5818bfa69d6de1
```

Recomputation (one line, executed):

```console
$ printf '%s' 'ME-X7-PROTECTED-b35d0617f13ec73ed96368bfb7019f603e5818bfa69d6de1' | shasum -a 256
2c8a3d774cab1fcae49fae5876d9ed314ea771563fa31ff44784c3dd3e2cf4b2  -
```

Custody file `~/.orion-custody/me-x7/PROTECTED_SEED_V1.txt`, mode 0600, 64 bytes,
hashed to the commitment **before** the authorization file was written.

## 2. The defect

### 2.1 What failed

```text
G0b ORACLE_SELF_AGREEMENT              pass = false   n_evaluated = 1250
  exhaustive_agree                     1250 / 1250    (direct rule == exhaustive enumeration)
  planter_agree                        1250 / 1250    (planted defect == full-structure recomputation)
  cross_implementation_agree           1244 / 1250    <-- FAILED
G5 SUFFICIENCY / S2_REPLAY_SUPPORT     pass = false   supported 1244 / 1250
```

Both failures are the **same six instances**. Every other gate passed. One
defect, one mechanism, two gates.

### 2.2 The six instances

Exactly one (stratum, mode, locus, check) combination, with no spread:

| instance | stratum | mode | locus | check | oracle | M | B5 |
|---|---|---|---|---|---|---|---|
| `protected-CENSORED_UNDECIDABLE-MODE_COMPUTATIONAL-0002` | CENSORED_UNDECIDABLE | MODE_COMPUTATIONAL | DIRECT | `C_ARTIFACT_DIGEST` | VALID | INVALID | INVALID |
| `…-0011` | CENSORED_UNDECIDABLE | MODE_COMPUTATIONAL | DIRECT | `C_ARTIFACT_DIGEST` | VALID | INVALID | INVALID |
| `…-0015` | CENSORED_UNDECIDABLE | MODE_COMPUTATIONAL | DIRECT | `C_ARTIFACT_DIGEST` | VALID | INVALID | INVALID |
| `…-0019` | CENSORED_UNDECIDABLE | MODE_COMPUTATIONAL | DIRECT | `C_ARTIFACT_DIGEST` | VALID | INVALID | INVALID |
| `…-0042` | CENSORED_UNDECIDABLE | MODE_COMPUTATIONAL | DIRECT | `C_ARTIFACT_DIGEST` | VALID | INVALID | INVALID |
| `…-0045` | CENSORED_UNDECIDABLE | MODE_COMPUTATIONAL | DIRECT | `C_ARTIFACT_DIGEST` | VALID | INVALID | INVALID |

### 2.3 Root cause

The `CENSOR_ENV` censoring variant clears the artifact's `actual_env` and
`actual_seed` to `''` — the registered "environment is not recoverable"
condition that makes `C_ENV_IDENTITY` undecidable. On all six instances the
recorded state is otherwise clean: `declared_digest == actual_digest` is
`True` and the recorded `checker_accepts` flag is `True`.

The oracle implements the frozen check table literally — `C_ARTIFACT_DIGEST`
is INVALID iff the digests differ or the checker rejects, and the table gives
it **no censored state** — so it returns VALID.

The arm-side module re-executes rather than trusting the recorded flag, which
is the registered source of its independence:

```python
# mex7_arms.py :: m_artifact_digest  (shared by M and B5)
accepts = MACHINE.run(a.payload, env_modulus(a.actual_env), a.actual_seed) == a.checker_target
```

With `actual_env == actual_seed == ''` this re-executes in an environment that
is not the one that ran. The replay diverges from `checker_target`, and the
arms report `INVALID` — **an unrecoverable environment is misread as a
proof/code mismatch.**

The sibling check already has the guard the digest check lacks:

```python
# mex7_arms.py :: m_env_identity / b5_env_identity
if not a.actual_env or not a.actual_seed:
    return CENSORED
```

So: **the censoring that makes one check undecidable silently corrupts a
different check, because the recoverability guard was written on the check
whose registered semantics named it and not on the check that also depends on
it.**

### 2.4 Properties of the defect, stated exactly

- **It is symmetric between the arms and cannot favour M.** `C_ARTIFACT_DIGEST`
  is one of the seven **shared** implementations declared in the design
  (`check_tables.shared_implementations`). M and B5 execute the same function
  and are identically wrong: per-check M-vs-B5 agreement is 1250/1250, and both
  return `INVALID` on all six. Paired M − B5 is exactly 0.0 with 0 discordant
  pairs. The defect moves M and B5 together, so it is not of the class that
  would advantage the study's own hypothesis.
- **It is deterministic, not a rate.** `CENSOR_ENV` was drawn 8 times: 6 in
  `MODE_COMPUTATIONAL`, all 6 diverge; 2 in `MODE_FORMAL`, neither diverges.
  Formal mode is immune because that branch runs the resolution checker over the
  payload and never consults the environment or seed. 6/6 and 0/2 — a mechanism.
- **Scope: 6 of 1250 instances (0.48%), one cell, one check.**

### 2.5 Why the development split did not catch it, and what did

The development split drew **one** instance in
`CENSORED_UNDECIDABLE × MODE_COMPUTATIONAL`, and that instance drew a
*different* censoring variant: its `actual_env`/`actual_seed` were
`'env-4'`/`'seed-636'`, intact. Its `C_ARTIFACT_DIGEST` was VALID on both
sides and agreed. **The cell was exercised; the variant was not.** Cell
coverage is not variant coverage.

**The instrument built for exactly this named it in advance.** The development
analysis's `COVERAGE_LEDGER` — reported, never a gate, and whose stated rule is
"any registered mechanism with zero instances is named here so no violation
count computed over it can be read as 'checked and fine'" — reported:

```json
"all_registered_mechanisms_exercised": false,
"never_exercised": { "censor_variants": [
  "CENSOR_AUTHORITY", "CENSOR_CALIBRATION", "CENSOR_DEPENDENCE",
  "CENSOR_ENV", "CENSOR_EVALUATOR", "CENSOR_PRESERVATION",
  "CENSOR_ROUTE", "CENSOR_SPEC" ] }
```

`CENSOR_ENV` is in that list. The defect lives in `CENSOR_ENV`. The freeze
shipped with the warning visible and correct; the protected split drew the
variant and the hard gate fired. At 1250 the ledger reports
`all_registered_mechanisms_exercised: true` with `never_exercised` empty for
cells, censor variants and loci.

### 2.6 A reported diagnostic that is insensitive to this defect

`IMPLEMENTATION_AGREEMENT` reports **1250/1250 on all eleven checks** on the
same run in which G0b found six disagreements. It is not contradictory and it is
not a gate: it compares M's check table against **B5's**, arm against arm, never
against the oracle. It is therefore structurally incapable of seeing a defect in
a shared implementation, which is precisely the defect present.

Read carelessly, a row of eleven `1250/1250` entries is silent-failure taxonomy
item 2 — a contrast that could not exist, reporting agreement. **It masked
nothing here, because G0b is the gate and G0b is the three-way comparison
against the oracle, and G0b fired.** The correction owed is to the *label*, not
the number: this diagnostic reports arm-vs-arm concordance and should say so.
Carried into the V2 re-freeze as a naming fix.

## 3. Gate table — every gate, every denominator, including the zeros

| gate | status | n_evaluated |
|---|---|---|
| G0a `KNOWN_ANSWER` (hard) | PASS | 31 |
| G0b `ORACLE_SELF_AGREEMENT` (hard) | **FAIL** | 1250 |
| G0c `NULL_CALIBRATION` (hard) | PASS | 1050 |
| G1a `B5_REPRODUCES_M` | PASS | 1250 |
| G1b `M_ADVANTAGE` | did not fire | 1250 |
| G1c `B5_AHEAD` | did not fire | 1250 |
| G2 `ANTI_CONSERVATISM` | PASS | 100 |
| G3 `MECHANISM_BY_OMISSION` | PASS | 1050 |
| G4 `INTERFACE_LADDER` | PASS | 1250 |
| G5 `SUFFICIENCY` | **FAIL** (S2 only) | 250 |
| G6 `CROSS_MODE_TRANSFER` | PASS | 1250 |
| G7 `WITNESS_SELF_CONTAINMENT` | EVALUATED, PASS | 53 (elsewhere 1197) |
| COVERAGE_LEDGER (reported) | all mechanisms exercised | 1250 |
| IMPLEMENTATION_AGREEMENT (reported) | arm-vs-arm only, §2.6 | 1250 |
| COST (reported) | `COST_ADVANTAGE_M` | — |

**Under a hard G0 failure no gate's pass is a finding — G7's included.** G7 is
the separating gate and a reader will reach for it; the routing table refuses to
issue any arm verdict, so its `PASS` is a diagnostic status, not a result.

**G1b and G1c both did not fire, and neither is the negation of the other.**
M − B5 = 0.0 exactly, 0 discordant pairs, exact two-sided p = 1.0. Under the
frozen design each has its own positive test, so a tie fires neither, and no
terminal is claimed from the tie. This is design §9(4) working as registered:
**B5 is exact by information-completeness on this generator**, so a tie is the
pre-registered expectation and carries no agreement-validation content
whatsoever. Where an exact planner is optimal by construction, agreement with it
is not evidence.

**G5 conjuncts, each with its own denominator:**

| conjunct | pass | n_evaluated |
|---|---|---|
| S1 `FAILURE_CLASS_PRESERVATION` | true | 1050 |
| S2 `REPLAY_SUPPORT` | **false** (1244/1250) | 1250 |
| S3 `SELECTIVE_REOPENING_WITHOUT_HIDDEN_HISTORY` | true | 250 |
| S4 `FALSE_ACCEPTANCE_NONINFERIORITY` (δ = 0.01) | true | 1050 |
| S5 `PREFERABLE_TO_FULL_TRACE` | true | 1250 |

S1 reports `INVALID_CALIBRATION × MODE_FORMAL` as
`status = CANNOT_CHECK_NOT_APPLICABLE, n_evaluated = 0` — the one cell the
design declared non-applicable in advance. It is not counted as a pass.

**Null calibration (G0c), the no-alarm assertions paired with the positives
that trip them:**

| control | result | denominator |
|---|---|---|
| `C_ALWAYS_ACCEPT` exact where the oracle rejects | 0 | 1050 |
| `C_ALWAYS_CANNOT_CHECK` exact where decidable | 0 | 1150 |
| `C_RANDOM_VERDICT` exact rate | 0.0832 (ceiling 0.15) | 1250 |
| M against shuffled labels | 0.0795 (ceiling 0.15) | 1245 |

The two zeros above are the no-alarm case, and each is paired with a planted
positive that must trip it: the selftest reports **planted positives 4/4**,
parents **23/23**, known-answer **25/25**, separation pair True, G0b True, G0c
True. The selftest report is byte-identical to the one frozen in PR #176
(sha256 `3e7e3f28…`), re-executed on this machine today.

## 4. Ladders, per mode, never pooled

**Reported as diagnosis only. G0b failed; these are not a verdict.**

| rung | MODE_FORMAL (n=600) | MODE_COMPUTATIONAL (n=650) |
|---|---|---|
| L1 `OUTPUT_ONLY` | 0.0833 | 0.0769 |
| L2 `PLUS_PROVENANCE` | 0.1817 | 0.1662 |
| L3 `PLUS_PROBLEM_ARTIFACT` | 0.3617 | 0.3231 |
| L4 `PLUS_VERSION_CALIBRATION_TRANSPORT` | 0.5417 | 0.5723 |
| L5 `PLUS_DEPENDENCE_ROUTE_AUTHORITY_PRESERVATION` | 0.9050 | 0.9031 |
| L6 `FULL_WITNESS` | 1.0000 | 0.9908 |

Monotone in both modes; every step's exact two-sided p is far below 0.05 in the
correct direction, with no regression. The computational L6 shortfall from 1.000
is the six defective instances and nothing else. **No argmax is taken over
rungs, and no claim is made that any single step is decisive.**

## 5. Determinism — executed, not asserted

Two full protected runs into separate output directories:

| file | check | result |
|---|---|---|
| `ME_X7_PROTECTED_RESULTS_V1.json` | byte-identical | **True** (sha256 `45315747f5539d46…`) |
| `ME_X7_PROTECTED_EXPECTED_CUSTODY_V1.json` | byte-identical | **True** (sha256 `5e26e0bb024ba038…`) |
| `ME_X7_PROTECTED_ANALYSIS_V1.json` | identical modulo the five named wall-clock fields (`wall_ms` per arm, `M_wall_ms`, `B5_wall_ms`, `wall_ratio_b5_over_m`) | **True** |

The claim is stated to exactly what was checked; the analysis file is **not**
byte-identical outright and is not claimed to be.

A first replicate compared unequal because its output directory had no selftest
report, so `G0a` reported `pass = null, n_evaluated = 0` instead of
`pass = true, n_evaluated = 31`. That is the code giving **"could not check" a
distinct value from "checked and fine"**, working correctly. The comparison
above is against a replicate with the report present.

## 6. Authorization and custody discipline

| step | evidence |
|---|---|
| guard armed before the run | `mex7_run.py protected` → **exit 3**, "REFUSED: … absent" |
| distinct from a broken run | a wrong interpreter gave **exit 1** with a traceback; the refusal is exit 3 |
| seed matched the pre-published commitment | verified before the authorization file was written (§1) |
| design digest acknowledged | `acknowledged_design_sha256` taken from the `origin/main` blob and equal to the worktree file |
| token | the operator's standing authorization, quoted verbatim, not composed by the lane |
| instance count not overridden | no `--per-cell` flag; the run printed exactly **1250 instances** |
| authorization archived after use | moved to `results/PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json` |
| guard re-armed | `mex7_run.py protected` → **exit 3** again, and no output directory was created |

## 7. What happens next (design §9)

A lane defect found mid-run **halts the lane, is receipted, and re-freezes as
V2**. This receipt is that halt. The protected result is **not** re-run under a
new seed under V1, and no V1 gate, oracle rule, arm or surface definition is
changed.

The V2 re-freeze must resolve **two coupled incompletenesses** this run
exposed. They are one discovery, and the second is why a one-line guard was
never going to be the repair.

**Incompleteness A — the check table.** `C_ARTIFACT_DIGEST` has no censored
state, yet there is a registered condition under which it cannot be
independently decided.

**Incompleteness B — the generator-validity invariant.**
`planter_agrees` requires `len(exp.censored_checks) == 1` for the
`CENSORED_UNDECIDABLE` stratum. That is false for a censoring variant whose
erased field more than one check depends on. Erasing the environment genuinely
makes **two** checks undecidable — the environment identity, and the artifact
re-execution that needs it.

Three candidate repairs, and the first two are both wrong:

1. **Arm-glue fallback only.** When the environment is unrecoverable, decide
   `C_ARTIFACT_DIGEST` from the recorded `checker_accepts` flag. This is
   inside design §9's declared tuning surface and it **preserves the cell** —
   the oracle stays `VALID`, one check is censored, the planter still accepts.
   **It is wrong** because it makes the auditor report `VALID` — accept the
   artifact — on the strength of a claim it was unable to check. For a study
   whose subject is what an external verifier can establish, silently
   converting "I could not check this" into "this is fine" is the failure mode
   the study exists to measure.
2. **Extend the check table alone.** Give `C_ARTIFACT_DIGEST` a censored
   condition and update the oracle and arm modules. This fixes the semantics
   and **deletes the cell.** Executed and verified against the V1 seed: under
   this repair the computational `CENSOR_ENV` episodes now have two censored
   checks, `planter_agrees` rejects them on the `!= 1` invariant,
   `generate_instance` re-draws a different variant, and `CENSOR_ENV`
   falls from **8 draws to 2** — the two formal instances survive and **all six
   computational instances silently disappear.** G0b then reports agreement
   because the hard cases are no longer in the split. That is a counter
   reporting zero violations because it never ran on the relevant cases, in the
   repair to a study about exactly that. **It is wrong.**
3. **Extend the check table *and* replace the count invariant.** Repair 2, plus
   `planter_agrees`'s "exactly one censored check" becomes a **declared
   per-variant, per-mode expected-censored set**, so a variant that legitimately
   censors two checks is accepted rather than re-drawn. This keeps the semantics
   honest **and** keeps the cell that exposed the defect in the split.

**Recommendation: repair 3.** Repair 1 buys a green gate by teaching the auditor
to trust an unverifiable flag; repair 2 buys a green gate by deleting the
evidence. Only repair 3 fixes the study.

Repair 3 changes the oracle rule and a generator-validity invariant, so it
requires a full V2 re-freeze with a **new** seed commitment, the V1 seed being
revealed in §1 above. That the frozen design was incomplete in these two coupled
ways is itself a finding and is carried into V2 as a registered correction, not
quietly fixed.

## 8. Corrections owed, and a verified negative

An earlier internal framing of a separate ME-X7 lane defect was wrong in four
ways and must not be repeated: the defect **did not pre-exist** — it was
introduced by the repair of a vacuous comparison and guarded 108 seconds later,
and a defect created by fixing a defect is the accurate description; its
advantage was **instance-level, not gate-level**, since routing would have
required p ≤ 0.05 **and** five M-only-exact instances in one cell; "eight of
eleven gates" is a unit mismatch, the true figure being **8 vacuous comparison
items spanning 6 of 11 gates, 4 fully vacated and 2 partially**; "three
planters" means **three call sites in one function**. The claim that "the same
lane committed the recurrence while fixing it" is `CANNOT_VERIFY`, because
commit authorship is uniform across lanes, and it is withdrawn rather than
repeated.

**Verified negative: none of these framings reached any merged artifact.**
`git grep` over `origin/main` for `first defect`, `favour`/`favor`,
`eight of eleven`, `three planters`, `same lane` and `108` across
`research/experiments/me-x7`, `research/experiments/me-x6`, `docs` and
`FAILURE_LEDGER.md` returned exactly one hit, an unrelated statistics docstring
in `mex7_run.py` line 123 ("favour x" in a binomial tail comment). The PR #176
body was scanned for all six and matched none. **The searches are known to
work**: a control pattern `witness` over the same scope returned 8 hits in the
parent-fidelity receipt and 10 in the PR body. The corrections are recorded here
for the record, not because an artifact required amending.

## Terminal

```text
ME_X7_V1_STATUS                        = HALTED_LANE_DEFECT
ME_X7_PROTECTED_ROUTE                  = CANNOT_CHECK
WITNESS_TERMINAL                       = NONE
DEFECT                                 = ARM_SIDE_ARTIFACT_REEXECUTION_LACKS_ENV_RECOVERABILITY_GUARD
DEFECT_SCOPE                           = 6 / 1250, one cell, one check, symmetric across arms
DEFECT_DIRECTION                       = NEUTRAL_BETWEEN_M_AND_B5
HARD_GATES_FAILED                      = G0b
SEED_REVEALED                          = TRUE
V1_SEED_REUSABLE                       = FALSE
RE_FREEZE_REQUIRED                     = V2, new seed commitment, extended check table
PARENT_SUFFICIENCY_ESTABLISHED         = FALSE
WITNESS_RESIDUAL_ESTABLISHED           = FALSE
FIELD_STATUS_AUTHORITY                 = NONE
PUBLICATION_AUTHORITY                  = NONE
```

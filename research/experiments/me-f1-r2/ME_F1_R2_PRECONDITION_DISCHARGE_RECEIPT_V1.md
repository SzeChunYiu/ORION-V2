# ME-F1 R2 — the §5.1 precondition discharged, and why that does not unblock the study

```text
ME_F1_R2_STATUS               = COMPARATOR_FROZEN, DISPATCH STILL REFUSED
PRECONDITION_5_1              = CONJUNCTIVE; both clauses now DISCHARGED
ME_F1_TERMINAL                = CANNOT_CHECK (G0e NO_LAUNDERING_VARIANCE) -- unchanged
PROTECTED_DISPATCH_AUTHORIZED = FALSE
CHANGES_ME_F1_V1              = NONE
GRANTS_SCIENTIFIC_TRUTH = false   GRANTS_FIELD_STATUS = false
```

`ME_F1_G0E_OUTCOME_RECEIPT_V1.md` §5.1 states a **conjunctive** hard precondition on any
ME-F1 successor: no successor may freeze `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` until
**(a)** its control text carries the `INCONCLUSIVE` → switch-tool fallback its own
algorithmic core already implements, **and (b)** its probe allocation is re-derived for
the action budget it is actually given. *"Until then, no M-versus-B5 comparison in this
world is worth running."*

Both clauses are discharged here. Freeze:
`ME_F1_R2_COMPARATOR_FREEZE_V1.json` sha256
`1599694b743691e81b5449a09cc6e208dea4917efa65f96e63bd56db3255f1cb`.

---

## 1. Clause (a) was **not** met on `main` — a correction to this lane's own brief

The brief for this work recorded clause (a) as already satisfied. **It is not, and the
repository says so.** In `research/experiments/me-f1/mef1_arms.py` the string
`INCONCLUSIVE` occurs four times: twice in the shared tool description (lines 80, 83) and
twice inside `run_deterministic_arm` (lines 625, 631) — the algorithmic core. **No arm
control text contains a switch-tool instruction.** The absence claim was made only after a
control pattern that had to match did match (`local_search`, 11 occurrences in the same
file), so the search was working.

What *was* repaired earlier is a different asymmetry — the rung-0 prompt/warrant-field
asymmetry of G0e receipt §6, whose lever removed the warrant field from `SIMPLE_DIRECT`'s
schema. That repair falsified its own attribution and never touched B5's control text.
Both clauses were therefore open, and both are closed here. Recorded because carrying an
unverified premise into a freeze is exactly what §5.1 exists to stop.

## 2. Clause (b): the measurement, reproduced rather than imported

The brief supplied 0.925 and 0.4875 and withdrew two other figures. Both supplied figures
were **re-measured from scratch** on the frozen development split (8 F_CRITICAL campaigns,
selected geometry L2, `n_vars = 30`, 300 000 checks, seed `ME-F1-DEV-20260902`), through
the study's own frozen scorer:

| policy | action cap | actions | primary | claims | unwarranted |
|---|---|---|---|---|---|
| **`FROZEN`** (the shipped core) | none | **120** | **0.9250** | 148 | 0 |
| `LUBY_SIZED` | none | 120 | 0.9250 | 148 | 0 |
| `SCHEDULE_ONLY` | none | 124 | 0.9125 | 146 | 0 |
| `BUDGET_AWARE` | none | 124 | 0.9125 | 146 | 0 |
| `TRAINED_TOOL` | none | 85 | **1.0000** | 160 | 0 |
| **`REDERIVED`** | none | **85** | **1.0000** | 160 | 0 |
| **`FROZEN`** | **7** | 56 | **0.4875** | 78 | 0 |
| `LUBY_SIZED` | 7 | 56 | 0.4875 | 78 | 0 |
| `SCHEDULE_ONLY` | 7 | 56 | 0.4437 | 71 | 0 |
| `BUDGET_AWARE` | 7 | 56 | 0.4562 | 73 | 0 |
| `TRAINED_TOOL` | 7 | 56 | **0.7000** | 112 | 0 |
| **`REDERIVED`** | **7** | 56 | **0.7000** | 112 | 0 |

Both supplied figures reproduce exactly. "~120 actions" is the **total across the 8
campaigns** (12–18 each), not a per-campaign figure.

**The repair at the budget the model arms actually get: 0.4875 → 0.7000, +21.25 pp.**

## 3. Single-stage attribution: the solver selector, not the probe order

Three levers were built and each was measured alone, because a repair attributed to a
bundle is not attributed at all.

| lever | primary at 7 actions | reading |
|---|---|---|
| **trained solver selection** | **0.7000** | carries the entire repair |
| Luby schedule sized to the action budget | 0.4875 | **changes nothing** — checks were never the binding resource |
| probes re-ordered by the federation's own `portfolio_schedule` | **0.4437** | made it **worse** |

The third lever is reported because it was tried and it failed. `portfolio_schedule`'s
docstring — *"order rungs by expected information per unit cost (cheap ends first)"* —
made it the obvious candidate, and probing the cheap ends turns out to settle fewer rungs
per action than the block midpoint, which guarantees 3 of 5 either way.

**Why the selector is the defect.** `portfolio_select` hardcodes the random-3-SAT
literature threshold and prescribes *"in the critical band, try the cheap witness first"*
— a rule whose premise is that the complete method is the expensive one. Trained on this
geometry, one probe per (rung, tool) at the cap-7 Luby unit budget, **32 probes per cell**:

| ratio | `exact_solve` settles | `local_search` settles | `exact` checks | `local` checks |
|---|---|---|---|---|
| 3.200 | **32/32 = 1.00** | 23/32 = 0.72 | **4 346** | 7 888 |
| 4.000 | 32/32 = 1.00 | 9/32 = 0.28 | 15 156 | 11 335 |
| 4.267 (critical) | 32/32 = 1.00 | **4/32 = 0.12** | 23 127 | 11 986 |
| 4.700 | 32/32 = 1.00 | 1/32 = 0.03 | 24 384 | 12 545 |
| 5.600 | 32/32 = 1.00 | **0/32 = 0.00** | 19 930 | 12 813 |

At `n_vars = 30` the complete solver is **not** the expensive one. `local_search` is
dominated at every ratio, and at the cheapest rung — the one the shipped rule is most
confident about — it is dominated on **both** resources. Under the frozen policy at 7
actions, 19 of 56 actions are `local_search` returning `INCONCLUSIVE`: 34% of the budget
establishing nothing and forcing a fallback.

**This is the published method applied, not replaced.** Rice (1976) and SATzilla (Xu et
al. 2008) do not ship a fixed rule; they *train* the selector on the instance distribution
it will face. The frozen implementation skipped that training step and substituted a
literature constant. Training it on the public development split — the study's own
declared tuning surface — is what a faithful implementer does, and it is what produces the
difference.

**The re-derivation is not a budget-specific hack.** At the natural budget it also
strictly dominates: **1.0000 on 85 actions** against the frozen core's 0.9250 on 120. It
stays inside the check budget (≈ 139 800 of 300 000 per campaign at cap 7), and every
policy makes **zero** unwarranted claims, so the comparison is of allocation and nothing
else.

## 4. The sharpest reading, and it is unfavourable to the mechanism

`SIMPLE_DIRECT` — the bare model with no control discipline — spent **53 of 56 actions on
`exact_solve`** (G0e receipt §5.1) and scored 0.7562. That is, to the action, the
allocation the trained selector prescribes. The repaired deterministic federation reaches
**0.7000** at the same 7 actions.

So B5 did not lose to a bare model because it lacked ORION machinery, and not because it
had fewer resources. **It lost because its own control text prescribed a dominated solver
at this geometry, and the bare model did not follow it.** The comparator was isolated by
its glue, and §5.1's refusal to compare M against it was correct.

## 5. What this does **not** do

**It does not unblock ME-F1, and no part of it should be read that way.**

ME-F1 routes `CANNOT_CHECK`. G0e is `NO_LAUNDERING_VARIANCE` — a hard fail that survived a
full revival attempt which **falsified its own attribution** — and
`mef1_run.stage_protected` refuses on its own before generating a campaign
(`EXIT_G0E_FAILED = 7` when checked, `EXIT_G0E_UNCHECKABLE = 8` when never evaluated,
`mef1_run.py:1209–1210`). Nothing in this file changes that, and this file freezes **the
comparator only** — not a run.

G0e's failure is **structural, not operational** (V1 receipt §7): ME-F1's world made every
arm's own warrant status self-evident, foreclosing by construction the very failure its
primary endpoint was built to measure. The only remaining lever — withholding the world's
licensing rules from the rung-0 arm — is forbidden, because it manufactures laundering by
making an arm ignorant. **A world in which warrant status is a judgment call is a
different study, not ME-F1 R2**, and inventing one to get a green gate is the move this
programme forbids.

Carried forward unsoftened:

- **ME-F1 V1 routes `CANNOT_CHECK`** (G0e failed, `NO_LAUNDERING_VARIANCE`).
- **`PARENT_SUFFICIENT` was never reached for ME-F1 and is not claimed.** `CANNOT_CHECK`
  pre-empts it.
- **At identical resources a bare direct arm beat both the mechanism and the parent, in
  both runs**: `SIMPLE_DIRECT` 0.7562 / 0.6625 against `M_ME_FRONTIER_CONTROL` 0.4062 /
  0.4500 and `B5` 0.3000 / 0.2437.
- **The ME-F1 V1 protected campaign must never be dispatched.**

## 6. Provenance and controls

- Worktree cut from `origin/main`; `/usr/bin/git` for every decision. **CPython 3.13.12**
  (`/usr/bin/python3` is 3.9 here and is not used for anything trusted). No model call was
  made and none is reachable from this code: every arm exercised is deterministic and
  byte-reproducible from the campaign seed.
- **ME-F1 V1 is untouched.** `mef1_arms.py` is not edited; the R2 module imports it
  read-only. Asserted by `test_me_f1_v1_is_untouched`.
- **The `FROZEN` policy is a replica, and its fidelity is asserted against the real
  function** — the action sequence (tool, rung, budget, outcome), the whole claim sheet
  and the checks spent all match `run_arm(c, "B5_ALGORITHMIC_CORE_NO_MODEL")` on all 8
  campaigns. The driver returns **exit 3** — its own code — if it does not, and refuses to
  report any policy comparison. A sibling control asserts the equality **can** fail
  (`REDERIVED` does not reproduce the shipped core).
- **"Could not check" keeps a distinct code throughout**: 3 = replica mismatch,
  4 = a development campaign's ground truth is not monotone-consistent, 0 = measured.
- **Every rate is published with its denominator**, including the training table's 32
  probes per cell and the zero-unwarranted-claims figure for every policy.
- `tests/unit/test_me_f1_r2_allocation.py`: **13 passed, exit status 0** (`$?`, no pipe).
  `ruff` clean on the study directory and the test file.

**What could not be checked, kept distinct from what was checked and is fine:** whether
the repaired **model** arm B5 would reach the deterministic core's 0.7000 (**not run** —
that needs model calls, and dispatch is refused; the deterministic core bounds the model
arm from above as designed, so 0.7000 is a ceiling and not a prediction); and whether the
trained selector transfers to a geometry other than L2 (**not measured** — the table
covers the five ratios this ladder generates, and `trained_select` falls back to the
nearest trained key so an unseen ratio is visible as an approximation rather than an
unannounced substitution).

---

*No campaign was dispatched. This document freezes a comparator; it grants no field
status, no novelty, no manuscript change, and no authorization to run ME-F1.*

skills-applied: none (receipt, no manuscript content)

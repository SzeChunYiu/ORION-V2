# ME-F1 — B5 comparator prompt/code parity: repair receipt (V1)

**What this is.** `ME_F1_G0E_OUTCOME_RECEIPT_V1.md` §5.1 recorded an arm-glue fidelity gap in
`B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` and explicitly did **not** repair it, making the repair a
hard precondition on any ME-F1 successor. This receipt performs the first of that precondition's two
clauses, measures it, and states plainly that the second clause is **not** done.

**What this is not.** This is a fairness repair to a comparator, not a result about the mechanism.
It does not change G0e's terminal, it does not reach `PARENT_SUFFICIENT`, and it does not clear
ME-F1 for an R2 freeze. Each of those is stated at its own strength in §6 and §7.

---

## 0. The three claims this receipt makes, and their status

| | claim | status |
|---|---|---|
| A | B5's control text withheld a *procedural rule* its own code implements | **reproduced** (§2) |
| B | that omission is what costs B5 its coverage | **reproduced deterministically, 0 model calls** (§3) |
| C | exposing the rule makes B5 a stronger comparator | **measured, 2 runs, 384 calls** (§5) — and it inverts the M-vs-B5 ordering (§6) |

Claim A's scope is **narrower than §5.1's wording**, and §2.2 says how.

---

## 1. What code produced these numbers

Every measurement below carries `source_provenance` computed **inside the measuring process**.

| | pre-repair (the receipt's numbers) | post-repair (this receipt) |
|---|---|---|
| `combined_source_sha256` | `b6350ba9c462571fa8599c2a0a397cf4bd24ec9075c52a41b6a483dfcf03c6a6` | `9455f24b51366822cfcea574efeda40abdd03f66bf686cc9e7b584e4e3e9e41e` |
| `design_sha256` | `f9ecd9ecba3b632cbf32304ab5a66e88640e655584e4991243f9af7858c4c704` | *unchanged* |
| manifest froze on | Mac worktree | Mac worktree (`BillydeMac-mini.local`) |
| verified on | billy-laptop-old | billy-laptop-old — **MATCH**, exit 0 |

**The attestation changes across this receipt's before/after contrast, and that is not hidden.**
The tree hash necessarily moves the moment the control text is edited. So the byte-level delta is
published rather than asserted: `git diff origin/main -- research/experiments/me-f1/mef1_arms.py`
is **five added lines, all inside B5's control text** (§4). The other two changed files
(`mef1_parity.py`, new; `mef1_run.py`, CLI wiring for the `parity` stage) cannot affect any arm's
behaviour, and §3 demonstrates that rather than asserting it: the deterministic ablation returns
**byte-identical numbers on the pre-repair and post-repair trees**.

The manifest went from 10 files to 11 (`mef1_parity.py`). `import_path_violations` is `[]` in every
run below.

## 2. The defect, reproduced before anything was changed

### 2.1 The capability is in the code and was absent from the prompt

`mef1_parity.check_control_text_parity()` puts the question mechanically. Run against **`origin/main`**
(`mef1_arms.py` sha256 `7f73565d1d835f55fb1274086a6ade0da2b2d8fc5b7c7893cc2971bcaf391a47`):

| probe | must hold | observed |
|---|---|---|
| `CONTROL_preamble_states_local_search_limit` | true | **true** |
| `CONTROL_code_branch_locatable` | true | **true** |
| `CONTROL_code_has_inconclusive_fallback` | true | **true** |

The three control probes are the licence for the absence claim: two of them prove the search can find
what is known to be present, and the check **refuses to report any arm as passing** if they do not hold.

| arm | status | tool-switch forms matched |
|---|---|---|
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | **`NOT_EXPOSED`** | **0 / 4** |
| `M_ME_FRONTIER_CONTROL` | `EXPOSED` | 2 / 4 |

Verdict `GAP`, on `B5` alone. **The no-alarm case is asserted as well as the alarm case:** `M` comes
back clean on the same probe, from the same run, without being edited.

### 2.2 The claim is narrower than §5.1's wording, and the asymmetry is the real defect

§5.1 says the fallback is "absent from B5's prompt". Read literally that is **too strong**, and this
receipt does not repeat it. The shared preamble `_COMMON` already tells *every* arm, in the tool
table, that `local_search` "can never establish unsatisfiability" and that `INCONCLUSIVE` means
nothing was established. The **information** was never withheld — and `SIMPLE_DIRECT` reads that
identical preamble and spends 53 of 56 actions on `exact_solve` anyway.

What was withheld from B5 is the **procedural rule**: what to *do* when a probe returns
`INCONCLUSIVE`. And the fairness defect is sharper than "B5 lacked a sentence" — it is an
**asymmetry between the comparator and the mechanism**:

- `M_ME_FRONTIER_CONTROL`'s control text names the action outright — escalation level
  **"L2 switch tool class (local_search <-> exact_solve)"**.
- `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION`'s named none of it.
- **Both arms' action spaces support it, and B5's own deterministic twin performs it.**

A comparator that cannot reach an action the mechanism is explicitly told to reach is not
information-matched. That, not the raw information, is what §5.1 correctly identified as
disqualifying.

### 2.3 The checker was validated before it was trusted

Three refusal codes, each exercised on a real tree:

| tree | verdict | exit |
|---|---|---|
| `origin/main` (pre-repair) | `GAP` | **9** |
| repaired (this branch) | `PARITY` | **0** |
| repaired, with the code fallback deleted | `NOT_CHECKED` | **10** |

At exit 10 **no arm is reported as passing** — "could not check" is never rendered as "checked and
fine". The tabulation used in §5 was separately validated by **reproducing receipt §5.1's R1 row
exactly** from the archived R1 artifacts before it was pointed at any new data.

## 3. What the fallback is worth — deterministically, at zero model cost

Before spending a model call, the receipt's causal story was put at risk of falsification. Two
variants of `run_deterministic_arm` are built from **one** source string by two textual transforms.
The 7-action cap is applied to **both** — matching the action budget the model arms actually get —
and the fallback block is removed from one. The function **asserts** the two variants differ nowhere
else before it measures anything, and refuses (`NOT_CHECKED`) if they do.

`B5_ALGORITHMIC_CORE_NO_MODEL`, 8 development campaigns, **56 actions**, **160 decided rungs**:

| variant | `INCONCLUSIVE` | on critical rung | `local_search` | `exact_solve` | coverage | claims |
|---|---|---|---|---|---|---|
| **with** fallback (as shipped) | 19/56 = **0.339** | 33/56 | 22 | 34 | **0.4875** | 78 |
| **without** fallback | 42/56 = **0.750** | 49/56 | 49 | 7 | **0.2000** | 32 |

Stripping the fallback from the *code* arm reproduces the *model* arm's signature: 42/56 against the
model B5's 37/56 and 41/56, with the same collapse into `local_search` on the block-midpoint rung.
Coverage more than halves. **The receipt's attribution survives a test that could have falsified it.**

The critical rung was verified, not assumed: local index 2 is α = **4.267** in every block of every
campaign, and 4.267 falls inside the portfolio's own (4.12, 4.42) "try `local_search` first" band.

Both denominators are published with every rate, because a bare `0.339` is what a counter that never
ran also reports.

## 4. The repair

Five lines, transcribing what B5's own code does and nothing else:

```
+    A portfolio does not stop at its first pick. When a probe returns INCONCLUSIVE it has
+    established nothing, so run the OTHER tool on that same rung before you move on
+    (local_search -> exact_solve; exact_solve -> local_search). If both come back
+    INCONCLUSIVE, that block's bracket cannot be advanced from here: leave it and spend
+    the remaining budget on another block.
```

against the code it transcribes:

```python
if r.outcome == "INCONCLUSIVE" and meter.remaining > 0:
    other = "exact_solve" if tool == "local_search" else "local_search"
    ...
    if r2.outcome == "INCONCLUSIVE":
        stuck.add(blk)          # move to another block
```

**M's five-level escalation ladder was not imported.** Nothing was added that B5's own published
components do not already entail: running a schedule of solvers rather than stopping at the first
pick is what algorithm-selection portfolios (Rice 1976; SATzilla) do. This is ordinary engineering
glue restoring the arm to its own implementation, not a new capability.


## 5. Re-measurement: the model arm, two runs each side, identical resources

Executed on billy-laptop-old, `codex exec` → `gpt-5.5`, `medium`, concurrency 3, the frozen
development split (8 F_CRITICAL campaigns, L2, `n_vars = 30`, 300 000 checks, 7 actions per
campaign). **Two post-repair runs, 384 model calls, 0 failed**, each attested from inside the job
(`match: true`, `drifted_files: []`, `import_path_violations: []`, tree `9455f24b…`). The pre-repair
rows are the archived V1 artifacts (trees `f8d718…` / `55c830…`), re-tabulated by the same script.
Artifacts: `results/b5-parity/r1/`, `results/b5-parity/r2/`; tables generated by
`results/b5-parity/gen_tables.py` from those files, not transcribed.

Every arm ran **exactly 56 actions in every run** — the budget is matched, so nothing below is a
resource effect.

| run | arm | `INCONCLUSIVE` | `local_search` | `exact_solve` | primary | claims | unwarranted |
|---|---|---|---|---|---|---|---|
| pre R1 | `SIMPLE_DIRECT` | 3/56 = **0.054** | 3 | 53 | **0.7562** | 121 | 0 |
| pre R1 | `B5_…FEDERATION` | 37/56 = **0.661** | 40 | 16 | **0.3000** | 48 | 0 |
| pre R1 | `M_ME_FRONTIER_CONTROL` | 27/56 = **0.482** | 29 | 27 | **0.4062** | 65 | 0 |
| pre R2 | `SIMPLE_DIRECT` | 3/56 = **0.054** | 3 | 53 | **0.6625** | 106 | 0 |
| pre R2 | `B5_…FEDERATION` | 41/56 = **0.732** | 44 | 12 | **0.2437** | 39 | 0 |
| pre R2 | `M_ME_FRONTIER_CONTROL` | 23/56 = **0.411** | 23 | 33 | **0.4500** | 72 | 0 |
| post R1 | `SIMPLE_DIRECT` | 4/56 = **0.071** | 4 | 52 | **0.7312** | 117 | 0 |
| post R1 | `B5_…FEDERATION` | 27/56 = **0.482** | 29 | 27 | **0.5125** | 82 | 0 |
| post R1 | `M_ME_FRONTIER_CONTROL` | 27/56 = **0.482** | 33 | 23 | **0.3812** | 61 | 0 |
| post R2 | `SIMPLE_DIRECT` | 3/56 = **0.054** | 3 | 53 | **0.7562** | 121 | 0 |
| post R2 | `B5_…FEDERATION` | 24/56 = **0.429** | 25 | 31 | **0.5062** | 81 | 0 |
| post R2 | `M_ME_FRONTIER_CONTROL` | 27/56 = **0.482** | 30 | 26 | **0.3125** | 50 | 0 |

### 5.1 The sentence was executed, not merely added

A prompt edit that moves a number is not evidence that the model did what the sentence says. So the
rule's execution was counted directly: of the `INCONCLUSIVE` probes that had a next action at all
(the denominator), how many were followed by the **other** tool on the **same** rung.

| run | arm | switched to the other tool on the same rung after `INCONCLUSIVE` |
|---|---|---|
| pre R1 | `SIMPLE_DIRECT` | 0/3 = 0.000 |
| pre R1 | `B5_…FEDERATION` | 1/35 = 0.029 |
| pre R1 | `M_ME_FRONTIER_CONTROL` | 8/23 = 0.348 |
| pre R2 | `SIMPLE_DIRECT` | 1/3 = 0.333 |
| pre R2 | `B5_…FEDERATION` | 2/37 = 0.054 |
| pre R2 | `M_ME_FRONTIER_CONTROL` | 10/23 = 0.435 |
| post R1 | `SIMPLE_DIRECT` | 2/4 = 0.500 |
| post R1 | `B5_…FEDERATION` | 23/23 = 1.000 |
| post R1 | `M_ME_FRONTIER_CONTROL` | 7/23 = 0.304 |
| post R2 | `SIMPLE_DIRECT` | 0/3 = 0.000 |
| post R2 | `B5_…FEDERATION` | 21/21 = 1.000 |
| post R2 | `M_ME_FRONTIER_CONTROL` | 8/25 = 0.320 |

B5 goes from **1/35 and 2/37** to **23/23 and 21/21**. `M_ME_FRONTIER_CONTROL`, whose prompt was not
touched, holds at 0.30–0.44 across all four runs — the internal control for the measurement. And it
shows the asymmetry was **behavioural**, not merely textual: M was already switching tools a third of
the time because its prompt names L2, while B5 was doing so one time in thirty.

### 5.2 What moved, what did not, and the run-to-run floor

| arm | pre R1 | pre R2 | post R1 | post R2 | reading |
|---|---|---|---|---|---|
| `B5_…FEDERATION` `INCONCLUSIVE` | 0.661 | 0.732 | **0.482** | **0.429** | **halved**, and now below its own pre-repair floor by 0.18–0.30 |
| `B5_…FEDERATION` primary | 0.300 | 0.244 | **0.5125** | **0.5062** | **+0.21 to +0.26**, against a pre-repair spread of 0.056 |
| `M_ME_FRONTIER_CONTROL` primary | 0.406 | 0.450 | 0.381 | 0.3125 | prompt untouched; within/below its own spread |
| `SIMPLE_DIRECT` primary | 0.756 | 0.663 | 0.731 | 0.756 | prompt untouched; inside its own spread |

The two untouched arms are the controls, and they hold. The moved arm is the edited one, in the
direction the deterministic ablation (§3) predicted, by an amount no run-to-run variance in this
study has ever produced.

## 6. What this does to G0e, and the honest state of ME-F1 — unsoftened

| run | G0e terminal | SIMPLE_DIRECT unwarranted | B5 unwarranted | checked |
|---|---|---|---|---|
| pre R1 | **NO_LAUNDERING_VARIANCE** | 0.0 over 121 claims | 0.0 over 48 claims | True |
| pre R2 | **NO_LAUNDERING_VARIANCE** | 0.0 over 106 claims | 0.0 over 39 claims | True |
| post R1 | **NO_LAUNDERING_VARIANCE** | 0.0 over 117 claims | 0.0 over 82 claims | True |
| post R2 | **NO_LAUNDERING_VARIANCE** | 0.0 over 121 claims | 0.0 over 81 claims | True |

**G0e is unchanged, and could not have changed.** This is structural, not empirical: the gate's
first clause is `SIMPLE_DIRECT`'s unwarranted rate `> 0`, which depends on `SIMPLE_DIRECT` alone. No
change to B5 can satisfy it, and a B5 that laundered *more* could only make the second clause harder.
All four zeros are honest zeros over populated denominators (106–121 and 39–82 claims), not empty
counters. Exit code **7** (`checked = true`), never 8.

Therefore, carried forward exactly as the V1 receipt states them:

1. **G0e FAILED. ME-F1 V1 routes `CANNOT_CHECK`.** No protected campaign was or may be dispatched.
2. **`PARENT_SUFFICIENT` was never reached and is not claimed.** Nothing here is a protected-split
   result; 8 development campaigns cannot see the registered primary contrast (MDE 0.124–0.175 at
   n = 150).
3. **At identical resources the bare `SIMPLE_DIRECT` model beat both M and B5 — before the repair
   and after it, in all four runs.** Post-repair: `SIMPLE_DIRECT` **0.7312 / 0.7562** against
   repaired B5 **0.5125 / 0.5062** and M **0.3812 / 0.3125**. The repair narrowed B5's gap to the
   bare model from ~0.45 to ~0.23. It did not close it.

**And the repair makes the picture worse for the mechanism, not better.** Pre-repair, M beat B5 in
both runs (+0.106, +0.206). Post-repair, **B5 beats M in both runs (+0.131, +0.194)**, and M is now
the weakest of the three model arms. The V1 development-split M-over-B5 gap was an artifact of the
prompt asymmetry — the rival explanation §5.1 warned about, now measured rather than argued. No V1
terminal rested on that gap (the receipt declined to read it), so no terminal changes; but any
successor that had inherited it would have inherited a confound.

## 7. Is the asymmetry present in the other studies? Confined to ME-F1 — after a corrected scope

### 7.1 The first answer was wrong, and the correction is recorded rather than quietly fixed

This lane first scanned `research/experiments/**/*.py` — **123 of the repository's 465 `.py` files** —
found per-arm control text only in `me-f1`, and concluded that the other studies "have no prompt at
all, so the defect is structurally impossible there". **That conclusion was false, and its scope was
never justified.** Seven model-arm modules live under `scripts/`, outside the scanned path:

`orion_pd_arms.py`, `orion_claude_arms.py`, `orion_codex_arms.py`, `orion_epistemic_atlas_arms.py`,
`orion_epistemic_locality_arms.py`, `orion_formal_discovery_arms.py`,
`orion_scientific_development_arms.py` — plus `sd70-v2` / `sd70-v3` model arms and three `e30`/`e40`
runners. Rescanned properly: **28 of 465 files** carry a model-channel or prompt marker.

The error mattered in exactly the place it could do most damage. **H-EXT-1 — one of only two studies
in the programme where M beats the strongest parent on a routed endpoint — is a prompted study.**
`H_EXT1_CONDITIONAL_ACTIVATION_DESIGN_V1.json` declares `"arms_are_model_calls": true`, cost unit
*"model_calls per instance (every arm = 1 codex exec call)"*, arms module `scripts/orion_pd_arms.py`,
with M = `P_D_FULL` and parent = `STRONGEST_ASSURANCE_FEDERATION`. The first scan never saw it, and
it carries no `.py` file of its own under `research/experiments/h-ext1/`, which is why a
directory-scoped search returned nothing and read as an absence.

### 7.2 The corrected test, and the corrected answer

The ME-F1 defect is not "an arm has a prompt". It is a **prompt/code parity mismatch**: an arm that
has **both** a prompt **and** a deterministic implementation *of the same method*, where the code
does something the prompt does not say. That is what makes it objectively a defect rather than a
design choice — the study's own code is the ground truth for what the method does. Detecting it
requires the prompted arm and the code arm to be the same method.

| module | per-arm prompt | deterministic twin | same method on both sides? |
|---|---|---|---|
| `research/experiments/me-f1/mef1_arms.py` | yes | yes | **YES** — `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` and `B5_ALGORITHMIC_CORE_NO_MODEL` are the same federation, declared so by §5.1 |
| `scripts/orion_pd_arms.py` (H-EXT-1) | yes | yes | **no** for the routed contrast — see below |
| the other 8 prompted modules | 4 yes / 4 no | **none** | n/a — no code twin exists to disagree with |

**H-EXT-1's routed arms have no code twin.** `OFFLINE_ARMS` is
`{CURRENT_INDEPENDENT_COUNTING, PROVENANCE_TRACKING, STANDARD_DEPENDENCE_META_ANALYSIS,
ARGUMENT_ACCEPTABILITY, SIMPLE_DIRECT_CONTROL}` — five simpler baselines. Neither `P_D_FULL` (M) nor
`STRONGEST_ASSURANCE_FEDERATION` (the routed parent) is in it; both are model-only. So no
prompt/code disagreement is detectable for the contrast the terminal rests on.

**So the ME-F1 defect class is confined to ME-F1 — but for a much narrower reason than first
reported.** Not "nowhere else has prompts" (false). Rather: ME-F1 is the only study that runs the
same method both as a prompted arm and as code, which is the only configuration in which this defect
is even well-defined.

### 7.3 What remains open, and is NOT cleared

H-EXT-1 **does** carry a prompt-level asymmetry between M and its parent:

- M (`P_D_FULL`): *"infer dependence from shared latent assumptions/calibrations stated in method
  text (not just declared lineage)"*
- parent (`STRONGEST_ASSURANCE_FEDERATION`): *"a dependence graph over **declared** correlations …
  Use only these parent capabilities; **refuse any further integration concept**."*

That is a real instruction-level restriction on the parent. It reads as **definitional rather than
defective** — latent-dependence inference versus declared-correlation graphs *is* H-EXT-1's
independent variable, so restricting the parent is the experiment, not a glue omission. But this
receipt did not measure it, and the distinction between "the parent's registered method boundary"
and "the parent held below its published strength" is exactly the judgement §5.1 says a comparator
change must not make unilaterally.

Recorded as **`CANNOT_CHECK`, for the coordinator to scope** — not as a clean bill, and not as a
defect. Two further facts bound it: H-EXT-1's routed winner is the **GATED** conditional-activation
policy, not M (always-on M scores 0.8942 and **loses** to the parent's 0.9558), and no residual
anywhere in the programme is awarded on an M-over-parent gap.

## 8. Disposition: no R2 freeze is taken here

§5.1's precondition is **conjunctive**: (a) the control text carries the fallback, **and** (b) the
probe allocation is re-derived for the action budget. This receipt performs and **measures** clause
(a) on the model arm. It does not perform clause (b), and it takes no freeze.

Clause (b) is sized here for reference. `B5_ALGORITHMIC_CORE_NO_MODEL`, same 8 campaigns:

| action budget | coverage |
|---|---|
| 120 actions (its natural run to check-budget exhaustion) | **0.9250** |
| capped at 7, fallback intact | 0.4875 |
| capped at 7, fallback stripped | 0.2000 |

The federation is strong at its natural action count and is given 7 actions. That is a second,
separable defect that no prompt sentence repairs.

## 9. Collision with `me-f1-r2` (PR #265), recorded rather than resolved

While this lane was executing, PR #265 landed `research/experiments/me-f1-r2/` on `main`. It
**independently confirmed clause (a) was unmet on `main`** — same finding, same control-pattern
discipline — and then discharged **both** clauses deterministically, freezing an R2 comparator text
in `ME_F1_R2_COMPARATOR_FREEZE_V1.json` (sha256 `f0ca74c2…`) **without editing V1**.

**The two B5 texts are different, and this receipt's measurement does not transfer.**

| | this receipt (`mef1_arms.py`, sha256 `2b9d589c…`) | R2 freeze (sha256 `f0ca74c2…`) |
|---|---|---|
| clause (a) fallback | yes — 5 lines, transcribing the code | yes — its item 4 |
| solver selection | the published band rule, unchanged | **replaced** by a trained table: "USE exact_solve" at every ratio |
| Luby sizing | unchanged | resized to the action budget |
| measured on the model arm | **yes — 2 runs, 384 calls (§5)** | **no** |

Two consequences, stated at their strength:

- **The R2-frozen text has no model-arm measurement.** Its 0.7000 at 7 actions is the deterministic
  core's number. The only model-arm evidence for what the fallback is worth is §5, and it is for a
  text that carries the fallback **alone** — so §5 is a clean single-lever measurement of clause (a),
  which the R2 lane's deterministic lever-isolation does not provide for the model arm.
- **The trained selector instructs B5 to use `exact_solve` everywhere**, which is the allocation
  `SIMPLE_DIRECT` arrives at unprompted (52–53 of 56 actions). Whether a B5 so instructed is still
  "the strongest *faithful* parent federation" or has been re-derived into the bare model's strategy
  is a comparator-design question this receipt does not decide. It is flagged.

Which text is the R2 comparator is a scoping decision above this lane, and the V1 receipt's own rule
applies: **a comparator change to a frozen study is a new design, not an edit.** This receipt
therefore takes no freeze, and reports both texts with their evidence.

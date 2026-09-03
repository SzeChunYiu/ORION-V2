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
| C | exposing the rule makes B5 a stronger comparator | **measured** (§5) |

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


## 7. Is the asymmetry present in the programme's other studies? No — and for a structural reason

A comparator repair is only interesting if the defect generalises, so the question was put to every
other study rather than assumed to be local.

**Method and its control.** All 123 `.py` files under `research/experiments/` on `origin/main` were
extracted and scanned for model-channel and control-text markers (`codex`, `call_control`,
`anthropic`, `openai`, `ARM_CONTROL`, `YOUR PROCEDURE`). The **positive control is `me-f1` itself**,
which matches every marker strongly (`YOUR PROCEDURE` ×11, `_ARM_CONTROL` ×3, `call_control` ×5).
That control is load-bearing: a first attempt using piped `grep -c` returned **0 for `me-f1` itself**
— the rtk proxy corrupting counts on piped output — and the absence claim below would have been
false if it had been trusted.

**Result.** Only three of the programme's studies touch a model at all, and only one has per-arm
control text:

| study | model surface | per-arm control text |
|---|---|---|
| **`me-f1`** | Codex CLI channel | **yes — the only one in the programme** |
| `sd70-v2` | `sd70v2_model_arm.py` | prompt built from a data `surface`, not hand-authored per arm |
| `e40-matched` | `anthropic` ×3 in one stage-2d file | not an M-versus-parent arm contrast |

`ME-X1`–`ME-X7`, `FG70` and `FM10`/`FM20` implement **every** arm — M and the parents alike — as
deterministic code engines. Verified concretely rather than inferred: ME-X1 carries
`engine_direct` / `engine_abstain` / `engine_provenance_verifier` / `engine_assurance` /
`engine_transition_control` (B0/B1/B2/B3/M); ME-X2 carries `arm_specs()` / `make_policy()`, and its
only long triple-quoted strings are module docstrings. ME-X3's `subprocess` calls are the Lean
binary, not a model channel.

**A prompt/code asymmetry is therefore structurally impossible in those studies: they have no
prompt.** In particular ME-X2's parent-dominance result is a contest between two code engines and is
untouched by this finding.

### 7.1 What this does NOT establish

"No prompts elsewhere" is **not** "the parents are fairly constructed elsewhere". Those are different
claims and only the first is established here. The code-engine studies carry an *analogous* fairness
question — whether each parent engine is implemented at the strength its published method actually
specifies — and this audit does not answer it. That is a **`CANNOT_CHECK`, not a clean bill**, and it
is recorded as such rather than allowed to read as an all-clear.

## 8. Disposition: this does NOT clear ME-F1 for an R2 freeze

§5.1's precondition is **conjunctive**. It requires the control text to carry the fallback **and**
the probe allocation to be "re-derived for the action budget it is actually given". This receipt
performs the **first clause only**.

The second clause is untouched and is now sized. `B5_ALGORITHMIC_CORE_NO_MODEL`, over the same 8
campaigns:

| action budget | coverage |
|---|---|
| 120 actions (its own natural run to check-budget exhaustion) | **0.9250** |
| capped at 7 actions, fallback intact | 0.4875 |
| capped at 7 actions, fallback stripped | 0.2000 |

The federation is **strong** — 0.925 at its natural action count, well above `SIMPLE_DIRECT`. Its
bisection schedule needs roughly 3 probes per block across 4 blocks (~12) to localise its boundaries,
and the model arm is given **7**. That mismatch is a second, separable defect that no prompt sentence
repairs.

**Therefore: no ME-F1 R2 freeze is taken here, and none may be taken on the strength of this receipt
alone.** The precondition is half-met. Reporting a half-met conjunctive precondition as clearance is
exactly the failure mode §5.1 was written to prevent.

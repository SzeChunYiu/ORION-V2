# E40-m5′ Stage-2d — Planted-Control Cause Discrimination, Design V1 (frozen before any run)

**Lineage:** Stage-2c outcome receipt (PR #167, main `01cc8418`) — disposition
`CHECKER_INVALID__NO_VERDICT`: the registered planted positive control failed (terminal quality
0.6412, 0/8 cycles in the ≥0.8 basin) against 0.9877 (m3) and 1.0 (m2) on the identical plant, code
and PASS rule, so no probe verdict was admissible and the E40 line stays open.
**Class:** mechanics diagnostic (model calls only, **zero native runs**). Freeze precedes run.
**Cost:** 3 arms × 9 cycles = **27 model decision calls**, temperature 0.

## 1. Question

Stage-2c §1 left **two non-excluded candidate causes** of the planted-control failure. Exactly one
question is asked here:

> Does the failure follow the **model channel** (present regardless of the cycle-1 mandate text), or
> the **cycle-1 mandate text** (present only under the Stage-2c seed mandate)?

The planted control runs the same prompted policy as the live arm, so it inherits whatever cycle-1
rule that arm carries — and the three executions differ in that rule as well as in the served model:

| execution | cycle-1 rule | served model | terminal planted quality | verdict |
|---|---|---|---|---|
| m2 (2026-08-30) | **none** | unrecoverable | 1.0 | PASS |
| m3 (2026-08-30) | regime-extreme anchor | unrecoverable | 0.9877 | PASS |
| Stage-2c (2026-09-02) | seed mandate (f2r0 = 11/13) | `glm-5.3` | 0.6412 | **FAIL** |

Stage-2d re-runs all three rule forms **on the current served model**, holding everything else
byte-identical, so the rule axis is varied with the model axis fixed.

## 2. Arms (the only difference between them is the cycle-1 rule string)

| arm | cycle-1 rule | byte-equal to |
|---|---|---|
| `A_NO_MANDATE` | none | `scripts/e40_matched_runner.py::f2_prompt` (the m2 form) |
| `B_REGIME_ANCHOR` | regime must be an axis extreme | `scripts/e40_matched_runner_m3.py::f2_prompt` |
| `C_SEED_MANDATE` | `model_seed`=11, `partial_intervention_seed`=13 | `scripts/e40_matched_runner_m5p_stage2c.py::f2_prompt(..., "f2r0")` |

Byte-equality of all three prompt forms against those frozen sources is asserted by unit test, at
every cycle, so "the only difference is the rule" is verified rather than asserted. Cycles 2–9
render identically across arms given identical history. Mandate enforcement follows m3/Stage-2c
conventions: ≤3 parse/validate re-asks, ≤3 mandate re-asks with an explicit VIOLATION note;
exhaustion ⇒ that arm is `CANNOT_CHECK` (recorded, never repaired).

## 3. Plant (inherited verbatim; not re-tuned)

Plant v4 exactly as in m2/m3/Stage-2c: optimum `partial_interventional` @ `frac 0.8`;
`quality = regime_factor(regime) · exp(-((frac − 0.8)/0.45)²)` with regime_factor
partial 1.0 / observational 0.7 / interventional 0.55; the same 8-field synthetic feedback;
9 cycles. **PASS rule (unchanged):** the last 3 cycles each at quality ≥ 0.9 **and** no cycle after
the first quality ≥ 0.9 dips below 0.8.

Changing the plant, the PASS rule or the cycle count in response to Stage-2c's failure would be
outcome tuning and is forbidden.

## 4. Gates (frozen before computing)

Controls are evaluated **first** and **gate the verdict** (§5). With all controls passing:

- **D0 `ARMS_VALID` (validity):** all three arms completed 9 cycles, none `CANNOT_CHECK`.
  Fail ⇒ `CANNOT_CHECK`; no cause is filed.
- **D1 `MODEL_CHANNEL_CAUSE`:** A, B and C **all fail** the plant PASS rule ⇒ the failure is
  mandate-independent on this model; the cause sits in the model channel.
- **D2 `PROMPT_IMPLICATED`:** C fails **and** at least one of A, B passes ⇒ the cycle-1 mandate text
  is implicated; the model channel alone does not explain it.
- **D3 `STAGE2C_FAILURE_NOT_REPRODUCED`:** C **passes** ⇒ the Stage-2c failure does not reproduce
  under nominally identical conditions (temperature 0 notwithstanding); the cause is **not
  identified**, and non-determinism of the channel becomes the leading explanation.

These three are mutually exclusive and exhaustive over (A,B,C) pass/fail patterns. Any outcome in
which the cause is not isolated (D3, or D0 failure) is reported as **ambiguous** in exactly those
words; the more convenient cause is not selected.

## 5. Controls — and control-gating (the Stage-2c defect, fixed here)

Stage-2c's analysis reported control verdicts without consuming them, so it emitted a routing
terminal while a registered control was failing. In Stage-2d `evaluate_gates()` **takes the control
verdicts as input and refuses to file any D-gate when a registered control fails**, returning
`CHECKER_INVALID__NO_VERDICT` with the D-gates explicitly `NOT_EVALUATED`. A fixture proves the
refusal fires (§6).

| control | rule |
|---|---|
| `PLANT_INTEGRITY` | known-answer: m3's **recorded** 9-cycle planted trajectory, replayed through this script's quality function, must reproduce m3's recorded qualities to ≤1e-12 and verdict PASS |
| `SERVED_MODEL_PIN` | every logged decision call reports `glm-5.3`, and every arm carries ≥1 such record |
| `LEAKAGE` | FORBIDDEN_SUBSTRINGS absent from every prompt and every synthetic-feedback blob (asserted on write and on read, executed) |
| `TRAJECTORY_REPLAY` | recomputing quality from each arm's recorded configs reproduces its recorded qualities exactly |

## 6. Validation required before the freeze

`selftest` must exercise `analyze()` end-to-end on synthetic recorded trajectories and show:
all-fail ⇒ D1; C-fail with A-pass ⇒ D2; C-pass ⇒ D3; an arm short of 9 cycles ⇒ D0 fail ⇒
`CANNOT_CHECK`; **a failed control ⇒ `CHECKER_INVALID__NO_VERDICT` with no D-gate filed** (both a
substituted served-model id and a broken plant); plus the m3 known-answer replay and the
prompt byte-equality tests.

## 7. Custody

Script `e40_m5p_stage2d_plant_discrimination.py` (sha256 frozen in the PR carrying this design);
output root `campaign-e40-m5p-stage2d/`; per-arm per-cycle `prompt.txt`, `response.txt`,
`decision.json` (prompt sha, response sha, served model id, mandate transcript); `arm.json`
summaries; rollup `E40_M5P_STAGE2D_ROLLUP_V1.{json,md}` with a sha256 manifest of everything read.
`run` refuses to overwrite an existing arm directory, so the 27 calls happen once.

## 8. Non-goals / no-rescue clause

This is a **mechanics diagnostic**, not a science result. Whatever it shows: it does not revive the
E40 line, does not authorize m6, does not alter the Stage-2c disposition
(`CHECKER_INVALID__NO_VERDICT` stands), and produces no claim about the metabolic-drag hypothesis or
the seed-replica probe. Its sole output is which cause a future freeze must address. Re-running with
an altered plant, PASS rule, arm set or cycle count after seeing the result is outcome tuning and is
forbidden.

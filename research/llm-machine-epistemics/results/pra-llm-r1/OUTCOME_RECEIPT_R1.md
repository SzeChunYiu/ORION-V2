# PRA real-LLM audit — R1 protected run, outcome receipt

Campaign `campaign-pra-llm-r1` · design `ORION51.PRA_REAL_LLM_AUDIT.design.v1` · issue #51.
This file records the outcome of the **authorized protected run** under the frozen V1 design.
It grants no scientific authority: routing requires a new manuscript version and freeze.

## 1. Terminal

**`REGISTERED_NEGATIVE_OR_BOUNDARY__CONTROL_FAILURE__SUITE_NOT_INTERPRETABLE`** — both models.

| model | GP0 | GP1 | GP2 | GP3 | terminal |
|---|---|---|---|---|---|
| qwen2.5-7b-instruct | pass | pass | pass | **FAIL** | `CONTROL_FAILURE__SUITE_NOT_INTERPRETABLE` |
| mistral-7b-instruct-v0.3 | pass | pass | pass | **FAIL** | `CONTROL_FAILURE__SUITE_NOT_INTERPRETABLE` |

`CONTROL_FAILURE__SUITE_NOT_INTERPRETABLE` is a member of the design's registered `terminals`
list (verified against the frozen design, not merely emitted by the runner). Under the frozen
routing this is a **registered negative/boundary result**. The no-rescue clause applies: no
family, prompt, threshold or gate may change post-outcome.

Because GP3 fails, the GP0/GP1/GP2 positives below are **not interpretable as a positive
result**. They are recorded descriptively, as the design requires, and must not be quoted as
evidence for the P2 terminal.

## 2. Artifacts verified before analysis

`sacct` rendering `COMPLETED 0:0` was not accepted as evidence of completion. The run wrote to
`/projects/hep/fs9/users/scyiu/orion-v2-pra-llm` (the `WorkDir` recorded by `sacct`), not to
home — which is why a home-directory search did not find it.

Both array tasks emitted the terminating sentinel `R1_MODEL_DONE <model>`, and all four stage
outputs exist for both models with non-zero size:

| artifact | qwen2.5-7b-instruct | mistral-7b-instruct-v0.3 |
|---|---|---|
| `present_gate.json` | 4 065 662 B | 4 446 679 B |
| `revision.json` | 3 942 562 B | 4 282 747 B |
| `probe.json` + 6 `hidden_*.npy` | 70 993 B + 6 × 49 889 408 B | 74 864 B + 6 × 64 880 768 B |
| `kv_channel.json` | 301 457 B | 317 807 B |
| stage receipts | 4 / 4 | 4 / 4 |

Stage call counts match the frozen design exactly in both models: present-gate 10 000 calls /
5 000 records, revision 5 000 / 5 000, probe 1 440, kv-channel 480 / 480. Suite: 500 protected
instances, family counts as registered. `stages_present` is `true` for all four stages in both
models. Nothing is missing or truncated.

Array task 0 (qwen) ran on `cg18`, task 1 (mistral) on `cg20`, both `gpua100i`, started
2026-09-02T16:38:48, ending 22:19:11 and 2026-09-03T01:41:24 respectively.

## 3. Custody

| input | sha256 | status |
|---|---|---|
| design V1 (LUNARC, every receipt, rollup) | `2f893db5…0061` | **identical** to `origin/main` blob |
| runner (LUNARC, every receipt, rollup) | `e25d969f…e490` | **identical** to the V1-freeze blob at `94c9da4` |
| runner on `origin/main` | `19862623…fda7f` | later V2 superset (`17e614a`), *not* the run input |
| protected suite | `21b5b0f7…b2ae` | generated once under `flock`, shared by both tasks |
| design V2 (LUNARC `v2/`) | `c0b65dc4…f5ef` | **identical** to `origin/main` blob |

The runner hash differs from `origin/main` and this is **not** a violation: the design's
`frozen_inputs.runner` is the V1 runner, and the LUNARC file is byte-identical to the blob
committed at the V1 freeze (`94c9da4`). `origin/main`'s copy is the later V2 extension
committed at `17e614a`, which adds V2 schema support without altering V1 behaviour. Recorded
here so the apparent mismatch is not re-litigated.

## 4. Model identity is asserted, not inferred

The substrate-substitution failure mode that forced E30-R11's comparison to be downgraded
**does not apply to R1**. This run used local HuggingFace weights with `HF_HUB_OFFLINE=1` and
`TRANSFORMERS_OFFLINE=1`; no model server was contacted. For both models the runner recorded,
in each stage's run JSON, `revision_requested` **and** `revision_resolved` (the latter read
from `model.config._commit_hash` after load), and both equal the revision pinned in the frozen
design:

| model | design-pinned | requested | resolved |
|---|---|---|---|
| `Qwen/Qwen2.5-7B-Instruct` | `a09a3545…bc28` | `a09a3545…bc28` | `a09a3545…bc28` |
| `mistralai/Mistral-7B-Instruct-v0.3` | `c170c708…ab71` | `c170c708…ab71` | `c170c708…ab71` |

Requested equals resolved equals design-pinned in both cases. Cross-run comparison involving
R1 is therefore **not** limited to descriptive on model-identity grounds. Also recorded per
stage: torch 2.6.0+cu124, transformers 4.51.3, dtype `torch.bfloat16`, device `cuda:0`,
n_layers 28 / 32, hidden_size 3584 / 4096.

## 5. Failure attribution — ONE stage

The failing gate is **GP3 (controls)**, and within it a **single check shared by both models**:

`mirror_not_falsely_revised_under_R3` — `F3_P2_MIRROR` false-revision rate under R3, against a
registered threshold of ≤ 0.10:

- qwen2.5-7b-instruct: **0.258**
- mistral-7b-instruct-v0.3: **0.392**

`F3_P2_MIRROR` retracts a source `Z` that is *not* on the claim's file; the registered gold is
RETAIN in both arms. Both models nonetheless emit REOPEN on a quarter to two fifths of arms.
The attributed stage is the **revision stage**, and the mechanism is model competence: the
models treat *any* retraction notice in context as a revision trigger, without checking whether
the retracted source is the claim's recorded basis. This is a reasoning deficit in the frozen
models, not a defect of the suite, the probe, the present-gate or the runner.

Mistral additionally fails `recon_no_gap` (`F3_P2_RECON` |R2−R3| = 0.167 > 0.10); qwen passes
that check. The mirror check is the only failure common to both, so it is the single attributed
cause. `p0_no_gap` passes in both.

A second, separable competence deficit is reported but is **not** one of GP3's three pass/fail
checks: `F0_ACQ` (acquisition-limit control, gold ESCALATE both arms) scores R0 accuracy
**0.000** (0/80) for mistral and **0.225** (18/80) for qwen. The models effectively do not emit
ESCALATE.

## 6. Frozen-gate implementation divergence — GP2a (`CANNOT_CHECK`, not `pass`)

The registered GP2a rule reads: *"probe decodes support_source under R0 **and R3** (≥ 0.80)"*.
The runner implements the positive control as R0 only:

```
r0_acc, rem_acc, kv_acc = _acc("R0"), _acc("R2_TRUE_REMOVAL", "R2"), _acc("R2_TEXT_REMOVED_KV_RETAINED")
pos_ok = r0_acc is not None and r0_acc >= g["GP2"]["probe_positive_control_min_acc"]
```

The R3 clause is **never evaluated**. Measured R3 probe accuracy is **0.542** (qwen) and
**0.594** (mistral) — both far below the registered 0.80. Had the clause been implemented as
written, `probe_positive_control_ok` would be **False** in both models and GP2 would have
mapped to `CANNOT_CHECK_ALTERNATE_CHANNEL_RETENTION`.

This is logged as a divergence between the frozen design text and the frozen runner. Its status
is **`CANNOT_CHECK`, distinct from `pass`** — the R3 half of GP2a's positive control was not
checked, and must not be read as checked-and-fine. Per the no-rescue clause the runner is not
edited and the rollup is not recomputed; the divergence is recorded and carried forward.

**The terminal is unaffected.** `model_terminal` evaluates GP3 before GP2, so
`CONTROL_FAILURE__SUITE_NOT_INTERPRETABLE` stands on GP3 regardless of how GP2a resolves.

**Open anomaly, reported not explained.** R3 *explicitly contains* the recorded support, yet the
probe reads `support_source` at 1.000 / 0.917 from R0 and only 0.542 / 0.594 from R3. A probe
that decodes the variable from the full history but not from the state that names it is more
consistent with keying on R0 history-surface features than on the semantic variable. This is a
construct-validity caveat on the whole alternate-channel gate and a registered lever for V2.

GP1's `r3_competence_floor` (0.70) is **not** a pass condition — the design text scopes it as a
terminal discriminator ("distinguishes NO_MECHANISM_EFFECT from ORDINARY_REASONING_FAILURE"),
and the runner implements it that way (`r3_competence_floor_met`, consumed only in
`model_terminal`). Implementation matches design. Recorded values: qwen `True` (R3 arm-level
0.867), mistral **`False`** (R3 arm-level 0.529). Mistral clears GP1 while failing the
competence floor — which reinforces the competence attribution in §5.

## 7. Descriptive observations (not interpretable as result; GP3 failed)

- **GP0 present-equivalence holds cleanly in both models.** Per-unit pass fraction 1.000; TOST
  on mean Δlogprob(R3−R2) equivalent with margin 0.05 and CI width < 1e-5. R3's extra state is
  genuinely dormant for the present decision.
- **GP1 passes in both, by opposite mechanisms.** Decomposing contrast B: qwen's gain is
  entirely on MAINTAIN_REQUIRED arms (+0.733, p=4.6e-16) with **zero** gain on UPDATE_REQUIRED
  (+0.000, p=1.0); mistral is the reverse (+0.508 update, +0.058 maintain). A single "R3 helps
  prospective revision" reading is not supported — the two models are doing different things.
- **More state is worse.** Contrast E (R3 vs R4, full dependency ledger): qwen 0.867 → 0.546
  (p=8.4e-16), mistral 0.529 → 0.500 (p=0.016). R4 degrades both models.
- **The two models dissociate on the KV channel.** The probe shows the dormant variable survives
  in the retained R0 KV cache in both (0.979 qwen, 0.896 mistral). Behaviourally, mistral
  *recovers* (contrast D 0.246 → 0.500, p=1.6e-15; terminal `…KV_SURVIVAL_CONTROL_CONFIRMED`),
  whereas qwen does **not** (0.500 → 0.508, p=0.5; terminal
  `…KV_INFORMATION_RETAINED_BUT_NOT_USED`). Information present in the channel is not the same
  as information used.
- **Information-matching certificate.** Incompatible-cell rate is 0.000 under R0/R3/R4 and
  0.290 under R2 (180 of 620 cells), 0.429 under R1. R2 genuinely collapses distinguishable
  histories, so the registered contrast could in principle have gone either way.
- Gate B (causal use) is `CANNOT_CHECK_ALTERNATE_CHANNEL_CAUSAL_USE`, omitted prospectively by
  the design — not a finding of this run.
- Three-history joint-intersection control passes (joint empty, all pairwise non-empty).

## 8. Silent-failure audit (assert the no-alarm case)

1. **A counter that never ran, reporting `0 violations`.** `contrast_B` discordant cells are
   `0 / 68` (mistral) and `0 / 88` (qwen) — one-sided discordance, no violations in the reverse
   direction. The counter is live: the same `mcnemar`/`_pairs` path returns non-zero reverse
   discordance elsewhere in this rollup (contrast C, `discordant_x_only` = 60 for qwen, 7 for
   mistral). Denominators are printed everywhere and are non-zero.
2. **A contrast that could not exist, reporting `1.000 vs 1.000`.** `p0_R2_vs_R3` reports
   exactly `acc_x = 1.000, acc_y = 1.000, discordant 0/0, n = 120`. This is a **real ceiling on
   a live path**, not a vacuous contrast: the identical code path (`mcnemar(_pairs(...))` over
   `F1_P0`) produced 0.246 vs 0.529 on `F3_P2_CANON` in the same rollup. `F1_P0` is the
   zero-extra-state control and is *designed* to show no gap; the two arms could have differed
   and did not.
   Likewise `F0_ACQ` accuracy `0.000` (0/80, mistral) is not a dead counter: the same path
   returned 18/80 for qwen, so ESCALATE is reachable through it. The floor is a finding.
3. **A sentence nobody executed.** No byte-identity or re-run claim is made anywhere in this
   receipt. Determinism was not re-verified for R1 and is **not** asserted.
4. **A rendered status trusted in place of the thing.** `COMPLETED 0:0` was not accepted; see
   §2. Landing of this receipt is decided by tree hash for the path, not by push state.

**Byte-level check of the probe conditions.** `hidden_R2.npy` and `hidden_R2_TRUE_REMOVAL.npy`
are **byte-identical** in both models (qwen `8c1c7639…`, mistral `fce9e588…`). This is a
**construction identity, not corroboration**: the design defines `R2_TRUE_REMOVAL` as "fresh
cache, R2 text only", which is the same computation as R2. Their equal probe accuracies
(0.5104 = 0.5104; 0.5729 = 0.5729) are therefore *one* measurement reported twice, and no
reader may treat R2 ≈ R2_TRUE_REMOVAL as independent agreement. The registered contrast D is
`R2_TRUE_REMOVAL` vs `R2_TEXT_REMOVED_KV_RETAINED`, and those code paths **do** diverge:
`hidden_R2_TEXT_REMOVED_KV_RETAINED.npy` differs from both (qwen `bf5da7d2…`, mistral
`1a193446…`), as do `hidden_R0.npy` and `hidden_R3.npy`.

## 9. Revival — the lever is prospective, not post-hoc

Per the programme invariant, this negative is **INTERMEDIATE**. The attributed stage is the
revision stage / model competence (§5). The matching lever is a **model-competence gate plus
larger models**, and it was **registered before this outcome existed**:

- Design V2 frozen at commit `17e614a`, **2026-09-02 15:47:48 +0200**.
- R1 protected run started **2026-09-02T16:38:48** — 51 minutes later.

No R1 outcome was visible when V2 was frozen, so V2 is not a post-outcome rescue. V2 adds gate
`GPC` (`pre_run_model_competence_on_dev_split`: R0 maintain ≥ 0.75 and update ≥ 0.75, dev split
only, replacement rule registered, never entering GP0–GP3 or the terminal) and replaces the 7B
models with `Qwen/Qwen2.5-32B-Instruct` and `mistralai/Mistral-Small-24B-Instruct-2501`.

GPC has been evaluated on the dev split and **passes non-vacuously** for both models —
maintain **32/32**, update **20/20**, verdict `COMPETENT__MODEL_RETAINED`, with
`F3_P2_MIRROR` maintain **8/8** — the exact control the 7B models failed. Denominators are
non-zero; this is a computed gate, not a null reported as pass.

Carried into V2 as open items: the GP2a R3-clause divergence and the R3-probe anomaly (§6), and
the `F0_ACQ` ESCALATE floor (§5).

## 10. V2 seed commitment (pre-run, seed not revealed)

The V2 protected seed is sealed at `v2/protected_seed.sealed` (mode 0600) on LUNARC. Its
sha256 was verified to equal the commitment published in the design **without revealing the
seed**: `d53e3748…c8925`. The only change to the V2 design between its freeze (`17e614a`) and
`origin/main` is `protected_commitment_sha256` moving from `PENDING_UNTIL_GPC_DEV_PASS` to that
value — gates, models and families are byte-identical across the two revisions. The seed itself
is revealed only after the V2 protected run completes.

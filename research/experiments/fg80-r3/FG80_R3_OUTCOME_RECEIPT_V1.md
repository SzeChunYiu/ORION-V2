# FG80 R3 — outcome receipt V1: the registered ceiling row fired; the instrument has no dynamic range

**Run:** 2026-09-06T21:51:18+02:00 → 22:13:33+02:00 on billy-old · **Freeze:** `d6eda4c` (executed at `308531e`;
fg80-r3 blobs byte-identical — see `FG80_R3_DISPATCH_DEVIATION_RECORD_V1.md`) · **Backlog:** #308 R8
**Authority:** none. `grants_scientific_truth: false`, `grants_F2_superiority: false`, `fires_the_P_F_trigger: false`,
`alters_the_R2_registered_terminal: false`. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

## 1. Terminal

```text
FG80_AT_CEILING_UNDER_A_CATEGORICAL_CONTRACT__NO_DYNAMIC_RANGE_FOR_THE_P_F_TRIGGER
```

This is **row 1 of the pre-dispatch routing table, registered before any model call** — the ceiling control, named
as a ceiling. Its predicate (`treatment ≥ 0.90 and parent ≥ 0.90 and p > 0.05`) was frozen on 2026-09-04 precisely so
that a ceiling could not afterwards be read as a surprise, a tie, or as support for anything.

## 2. What the run produced

| arm | correct | accuracy | missing/invalid |
|---|---|---|---|
| `TARGET_ONLY_DIRECT` (parent) | 80/80 | **1.0000** | 0 |
| `STRONGEST_DOMAIN_FORMAL_PARENT` | 80/80 | **1.0000** | 0 |
| `F0_PARENT_FEDERATION` | 80/80 | **1.0000** | 0 |
| `F2_STATIC_NO_FORMAL_DISCOVERY` | 80/80 | **1.0000** | 0 |
| `F2_FORMAL_DISCOVERY_FULL` (treatment) | 80/80 | **1.0000** | 0 |

Paired `F2_FORMAL_DISCOVERY_FULL` vs `TARGET_ONLY_DIRECT`: **b = 0, c = 0, Δ = 0 tasks, exact p = 1.0**. Not one task
in 80 separates any arm from any other. 400/400 dispatches `COMPLETED_PROPOSAL_ONLY`, 0 failed, `run_valid` true for
every arm.

## 3. The ceiling is real, not an artifact of a degenerate task set

A 100 % score everywhere invites the suspicion that the suite is trivially satisfiable, so that was checked before
the number was believed:

- the private oracle carries **80 distinct expected answers** for 80 tasks (no repeated target);
- the answer contract is a **4-way enumerated feature choice × a binary decision** — chance is **1/8 = 12.5 %**;
- the binary half is **balanced: 41 YES / 39 NO**, so it is not satisfiable by a constant;
- the oracle was removed before dispatch and restored afterwards, `oracle_restored_hash_match: true`, independently
  re-verified: sha256 `b219f0e0f6c18e5818a05a261bce1313fae6f902639d894b33300008ae67d5fa`, equal to the value
  committed inside `FROZEN_SUITE.json` before the run.

Every arm scoring 100 % against a 12.5 % chance baseline on a non-degenerate, balanced task set is genuine
saturation of the instrument.

## 4. What this does and does not say

**It is a finding about the instrument, and it is reported at that strength.** Under a categorical answer contract,
the FG80 suite (80 tasks, seed 20260904) has **no power whatsoever** to compare these five arms: the simplest control
`TARGET_ONLY_DIRECT` already solves every task. A comparison whose control is at ceiling cannot rank anything above
it, so no arm — F2_FULL included — can be shown better or worse here.

**On the R2 attribution.** R2's registered deficit (F2_FULL 23/80 vs simple direct 42/80, Δ −19, paired exact
p = 4.3e-03) was measured under a `FREE_TEXT_CATEGORICAL_ENDPOINT` with exact-match scoring. Replacing only the answer
encoding, holding the tasks, seed, arms and procedure text fixed, moves **every** arm to 80/80. The R2 deficit
therefore does not survive the change of answer encoding — consistent with the descriptive attribution registered on
2026-09-04 — but the manner of its disappearance matters: the deficit did not shrink to a small honest null, it was
replaced by a measurement with no dynamic range at all. What R2's exact-match scoring was ranking was answer
*rendering*, and once rendering is removed the tasks are uniformly easy for this channel.

**What must not be concluded.** This is not evidence that `F2_FORMAL_DISCOVERY_FULL` is sound, that formal discovery
helps, or that the R2 negative was wrong about the mechanism. A saturated instrument is silent, not exculpatory.
`fires_the_P_F_trigger` is false and the P-F trigger's own 2026-09-04 evaluation
(`NO_R2_EFFECT_TO_EXPLAIN__P_F_STANDALONE_ROUTE_CLOSED_OR_MERGE`) stands unchanged: there is still no R2 effect to
explain, and now also no instrument capable of producing one at this task count.

## 5. Served model

The codex CLI exposes no served model id. All 400 responses record `served_model: null` with
`served_model_source: NOT_EXPOSED_BY_CODEX_CLI__HEADER_IS_REQUEST_ECHO` and `requested_model: gpt-5.6-terra`. This is
the executor's own registered honesty about a gap in the channel, not a caveat introduced afterwards: **the run is not
asserted to have been served by gpt-5.6-terra**, only to have requested it.

## 6. What the constraint points at

The next question this makes available is not another FG80 run at n = 80. A suite whose easiest control is at ceiling
needs either harder tasks or a discriminating endpoint before it can test anything; re-running the saturated
instrument would produce the same silence. That is a design question for whoever opens the next prospective identity,
and it is **not** opened here — the operator's stop on P-F follow-ups stands, and this outcome is absorbed under its
frozen identity by the papers that cite FG80 (P-C V11 §3.1/§4.1; FLAGSHIP).

```text
FG80_R3 = FG80_AT_CEILING_UNDER_A_CATEGORICAL_CONTRACT__NO_DYNAMIC_RANGE_FOR_THE_P_F_TRIGGER
  all five arms 80/80 (acc 1.0000); b=0 c=0 exact p=1.0; 400/400 completed, 0 failed
  chance baseline 12.5% (4-way x binary, 41 YES / 39 NO, 80 distinct targets) -> saturation is real
  registered ceiling row, frozen pre-dispatch 2026-09-04, fired exactly as written
  P_F_TRIGGER = DID_NOT_FIRE (unchanged); R2 registered terminal UNCHANGED
  SERVED_MODEL = NOT_EXPOSED_BY_CODEX_CLI (requested gpt-5.6-terra; not asserted as served)
  P_F disposition = NO_STANDALONE_RELEASE__NEGATIVE_BOUNDARY_INPUT (unchanged)
```

skills-applied: none (evidence lane, no manuscript content)

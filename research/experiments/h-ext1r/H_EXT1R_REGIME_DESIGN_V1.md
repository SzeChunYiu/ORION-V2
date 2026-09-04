# H-EXT-1R — Design V1: a regime where the gate fires and the strongest parent is off ceiling

**Status:** `PRE_FREEZE__DEVELOPMENT_SPLIT_PREPARED__FEASIBILITY_UNMEASURED`. Machine-readable
twin: `H_EXT1R_REGIME_DESIGN_V1.json`, written by `scripts/h_ext1r_regime_study.py freeze`
**only if** the development split's feasibility clause passes; it does not exist yet.
Predecessor: `research/experiments/h-ext1p/H_EXT1P_REGISTRATION_AND_PRE_FREEZE_CLOSURE_V1.md`.

## 1. The negative, its stage, and the lever

H-EXT-1P closed pre-freeze: on every task where the frozen gate `G_B_PLUS_XREF` activates,
`GATED_M` and `STRONGEST_ASSURANCE_FEDERATION` are both perfect (170/170 vs 170/170
prospectively; 72/72 vs 72/72 on the held-out retrospective cell), so the mechanism-
attributable contrast has zero discordant pairs and no n confers power. The closure
attributed the wall to **one stage — the task suite** — and named the lever: a suite in
which the dependence machinery has an error the parent does not also avoid, established on a
development split *before* any comparison, or no successor freezes.

H-EXT-1R constructs that suite from the protocol semantics and tests whether it exists.

## 2. Construction

Each stratum carries a **visible provenance witness** — two records sharing a `lineage_root` —
so the frozen gate fires on every task by construction (asserted mechanically by importing
`witness_features` / `gate_fires` from the frozen `h_ext1_gate_study.py`, with a no-witness
control task that must read `False`), and a **latent dependence** the witness does not reveal,
on which the registered rule's answer turns. Paired controls carry the identical gate input
with no latent dependence and the opposite verdict.

| stratum | rule | witness | latent dependence | answer | root-only reader |
|---|---|---|---|---|---|
| `PDS5A_WITNESS_PLUS_LATENT_CONVENTION` | S1 (verbatim) | e1/e2 share a root | e4, e5 adopt e3's calibration convention **by name**, never naming e3's root | INCONCLUSIVE, 2 families | ACCEPT_H, 4 (wrong) |
| `PDS5B_WITNESS_PLUS_INDEPENDENT` (control) | S1 | same | none: e3/e4/e5 on their own conventions | ACCEPT_H, 4 | ACCEPT_H, 4 (right) |
| `PDS5C_LATENT_LINEAGE_REVOCATION` | S5 (explicit lineage) | i2/i3 share a root | i4 calibrates through a transfer curve i1 publishes, named by the curve | C1 preserved, C2 reopened | both preserved (wrong) |
| `PDS5D_SELF_CALIBRATED_REVOCATION` (control) | S5 | same | none: i4 self-calibrated | both preserved | both preserved (right) |

The S5 reopening rule is S3's with lineage made explicit — *an item's lineage includes every
item whose data, calibration or transfer products its method text states it relies on,
whether or not the two share a lineage root* — and is given verbatim to every arm. The
root-only column is the construction's own mechanical check that a contrast **could** exist
(a reader confined to lineage roots errs on treatment and is right on control); it is not an
arm and is not evidence.

Pre-freeze guards, executed in the selftest (53/53) and again on the prepared split:
`STRUCTURALLY_DETERMINED_REGISTERED_CLAUSE` (identical gate-input feature sets within each
pair; answers differ between the pair's strata); `NONREPRODUCIBLE_FROZEN_ARTIFACT` (split
digest identical across `PYTHONHASHSEED` 1 and 12345 in fresh processes; no RNG draw ordered
by an unordered container); `HANDICAPPED_COMPARATOR` (every arm receives byte-identical task
text and the same call budget, differing only in its registered ARM PROCEDURE sentence,
imported read-only from `orion_pd_arms.py`); `VACUOUS_CONTRAST` (the three arms are three
prompts to the same channel; the statistic is over discordant pairs, which are zero if the
arms cannot differ, and the feasibility clause requires the parent to miss).

## 3. What is decided before any model runs

**F1 — feasibility (development split, seed 20260904, 20 tasks per stratum, 80 tasks, 240
calls):** the strongest parent's accuracy on the two treatment strata is at most **0.85**
(≤ 34 of 40). If F1 fails, the terminal is
`REGIME_NOT_REALISED__PARENT_AT_CEILING_ON_WITNESSED_LATENT_TASKS` — a `CANNOT_CHECK`-class
terminal, not a negative about the mechanism — and **no protected run is dispatched**. The
development split is not evidence about the mechanism in either direction; it decides
whether a contrast can exist. Power at the protected n is reported from the development
discordance with the winner's-curse caveat and is not gated on.

**Protected cell (seed committed by sha256 before the freeze, 50 tasks per stratum, 200
tasks, 600 calls), gates in precedence order:**

| gate | clause | terminal if it decides |
|---|---|---|
| G0 | all responses present and `COMPLETED`; gate fires on every task; no-witness control reads `False` | `CANNOT_CHECK_RUN_INVALID` |
| G0b | one served model id and one contract sha256 across all envelopes; zero zero-text calls | `CANNOT_CHECK_RUN_INVALID` |
| G1 | exact two-sided McNemar, `M` vs `PARENT`, over all 200 gate-active tasks, α = 0.05 | no rejection → `PARENT_SUFFICIENT_ON_ACTIVATION_REGIME`; rejection in the parent's direction → `PARENT_AHEAD_ON_ACTIVATION_REGIME` |
| G3 | exact McNemar `M` vs `OFF` on the treatment strata, `M` ahead | fail → `GAIN_NOT_ATTRIBUTABLE_TO_DEPENDENCE_MACHINERY` |
| G2, G4 | `acc(M) ≥ acc(PARENT)` on the pooled controls; `M ≥ PARENT` within each treatment stratum | fail → `GAIN_NOT_PARETO_ON_CONTROLS` |
| all pass | | `MECHANISM_BEATS_PARENT_ON_ACTIVATION_REGIME` |

In this regime `GATED_M` **is** `M` on every task, so G1 is literally the contrast the closure
named as mechanism-attributable: always-on `P_D_FULL` against the strongest parent on
gate-active tasks, with `P_D_MINUS_DEPENDENCE` as the attribution control. Every protected
terminal is reachable by fixture (asserted); F1 can pass and can fail (asserted).

No rescue: after the freeze no threshold, stratum, arm, prompt, statistic or exclusion
changes; any repair is a new identity.

## 4. Substrate, disclosed

H-EXT-1's prospective cell ran gpt-5.5 through the codex CLI, whose channel records the
requested id and not a served one. That channel is not available to this lane at freeze
time. H-EXT-1R runs on the Anthropic-compatible channel E30-R13 registered — served
`glm-5.3` asserted per call against a pin, request-body contract `thinking_disabled`
fingerprinted by sha256, 4 000-token cap, an `interface`-style channel receipt on every
envelope — through `scripts/h_ext1r_pd_arms.py`, which imports `orion_pd_arms.prompt` and
`arm_instruction` read-only so the prompt is H-EXT-1's. A different substrate from H-EXT-1
is a different absolute accuracy scale; the contrast needs all three arms paired on one
substrate, which they are. The gate is input-computable and substrate-independent.

## 5. Pre-run audit against the failure ledger

| class | how it is excluded |
|---|---|
| seed does nothing | protected split prepared from the committed seed only; digest recorded; differs from the development digest |
| gate crashing at scale | exact McNemar and the trinomial power function are integer/rational enumerations; asserted finite and sized at n = 200 |
| contrast that could not exist | F1 is the registration condition; the root-only reader shows the construction admits an error |
| clause silently narrowed | `analyze` binds the cell to its registered gate list; the design JSON pins every source by sha256 and `protected-prepare` refuses on drift |
| clause unsatisfiable or unfailable | each pair shares gate input and splits on the answer; each gate has a fixture on both sides |
| parent isolated by information or budget | identical task text, rule text and budget; only the ARM PROCEDURE sentence differs, as in H-EXT-1 |
| served-model id not pinning the condition | served id asserted per call **and** request-body contract fingerprinted, stop reason and text length receipted (E30-R13's discipline) |

## 6. Status of execution

The development split is prepared on LUNARC (`h-ext1r/dev/dev-split`, 80 tasks, digest
`dfe9fc765ff8…`, gate audit 80/80 fired, control `False`, pair inputs identical). Its dispatch
(job 3573432, source `fe11512`) was cancelled after the channel answered every call with HTTP
429 and a 20-token probe likewise; **0 of 240 responses exist and F1 is unmeasured.** The
cell will be re-dispatched, resumable by response scan, when a channel answers; nothing in
this design changes for that.

```text
H_EXT1R_DESIGN = PRE_FREEZE
GRANTS_SCIENTIFIC_TRUTH = false
GRANTS_FIELD_STATUS = false
GRANTS_MANUSCRIPT_CHANGE = false
CHANGES_H_EXT_1_OR_H_EXT_1P = NONE
```

skills-applied: none (design note, no manuscript content)

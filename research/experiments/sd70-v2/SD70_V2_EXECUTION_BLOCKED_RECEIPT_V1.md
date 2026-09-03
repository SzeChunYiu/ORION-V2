# SD70-V2 — Execution-Blocked Receipt (V1)

**Study:** SD70-V2 `SYNTHETIC_RECURSIVE_META_POLICY_V2` — ORION-V2 issue #50.
**Frozen design:** `research/experiments/sd70-v2/SD70_V2_EXECUTION_DESIGN_V1.{md,json}`,
design sha256 `96d933e00cbc8d09222fd4e86e27d1fe8604164521aea1feedd483ddcbd28bf4`, merged to `main`
as `7e3ad77` (PR #152) **before** any protected task existed.
**Checkpoint:** 2026-09-02T23:53:28Z, against `main` `fd7a4e4`.
**Machine record:** `results/SD70_V2_EXECUTION_BLOCKED_CHECKPOINT_V1.json`.

## 1. Status

```text
SD70_V2_STATUS = EXECUTION_BLOCKED_PRE_DISPATCH
SD70_V2_PROTECTED_TASKS_GENERATED = 0
SD70_V2_PROTECTED_OUTCOMES_INSPECTED = 0
SD70_V2_SINGLE_RUN_AUTHORIZATION = UNSPENT__NEVER_ARMED
SD70_V2_TERMINAL = NONE__STUDY_REMAINS_PROSPECTIVE
MACHINE_EPISTEMICS_FIELD_CLAIM_STATUS = FIELD_RESIDUAL_NOT_ESTABLISHED
FLAGSHIP_PUBLICATION_STATUS = UNCHANGED__SUBMISSION_READY_FALSE__PUBLICATION_READY_FALSE
```

`EXECUTION_BLOCKED_PRE_DISPATCH` is **not** a member of the SD70-V2 terminal set and is **not**
the evaluator's `CANNOT_CHECK`. `CANNOT_CHECK` (design §10.1) is an evaluation-time verdict
reached *after* dispatch, on evidence. This receipt is reached *before* dispatch, on no evidence:
it reports that a frozen design has not been run, and why. It carries no accuracy, no delta and
no gate outcome, because none was measured.

## 2. The blocker — `SD70-V2-BLOCK-1`

**One-stage attribution: model-dispatch credential.**

The Codex CLI is logged out on every host this lane can reach.

| host | probe | result |
|---|---|---|
| Mac mini | `codex login status` | exit 1, `Not logged in` |
| Mac mini | `codex exec … --model gpt-5.6-terra --json 'Reply with exactly: OK'` | exit 1; five websocket reconnects, each HTTP 401 against `wss://api.openai.com/v1/responses`; `turn.failed` — *Missing bearer or basic authentication in header* (request ids `req_f4c187b9…`, `req_54ca6cfb…`, `req_5582fc42…`, `req_5322100c…`) |
| Mac mini | `~/.codex/auth.json` | absent; `~/.codex` recreated (directory and every entry stamped 2026-09-03 01:41) in the 0.147 sqlite layout, no `config.toml`, no `auth.json` |
| Mac mini | `npm ls -g` | `@openai/codex@0.147.0` — the programme pin is `0.129.0-alpha.15` |
| LUNARC `cosmos2` | `which codex` / `node` / `npm` | none present |
| LUNARC `cosmos2` | `find /home/scyiu -maxdepth 6 -name auth.json`; `find /projects/hep -maxdepth 6 -name auth.json` | 0 hits each. Searched for the `orion-v2-e45/codex-home` path from earlier session notes with `find /home/scyiu -maxdepth 4 -name orion-v2-e45` and `ls -d /projects/hep/fs{7..12}/*orion* /projects/hep/fs{7..12}/scyiu/*orion*` — no match at that depth. The absence of `node` and `npm` is the load-bearing observation regardless: nothing there could run the CLI even if a stored credential were found deeper. |

The version drift and the vanished credential are one event: the CLI was moved off the pinned
`0.129.0-alpha.15` to `0.147.0`, which uses a different state layout. Reinstalling the pin would
restore the binary but not the credential — `auth.json` is gone, not shadowed.

**Why this blocks the study.** Design §5 dispatches 1 140 Codex calls across five model arms
(240 × 4 contested arms + 3 × 60 model controls). The registered primary estimand is the paired
difference Δ = acc(`F2_RECURSIVE_META_DISCOVERY_FULL`) − acc(`MAXMARGIN_PARENT`). Both primary
contrasts, the mechanism gate, all three ablations and the model negative control are model arms.
Nothing registered is decidable from the deterministic arms alone.

**Resolution requires an operator action:** an interactive `codex login`, optionally preceded by
reinstalling `@openai/codex@0.129.0-alpha.15`. This agent is not permitted to authenticate on the
operator's behalf, and this session is non-interactive.

## 3. What was rejected, and why

- **Dispatch anyway and let the model arms 401.** Refused. `prepare` would generate the protected
  suite from the sealed seed and the run would spend the single-run authorization, trading a clean
  pre-dispatch state for an infrastructure artifact that is not a scientific result. The sealed
  seed and the one-shot guard are the scarce goods here.
- **Point `ORION_CODEX_MODEL` at a reachable model.** Refused. §5 pins `gpt-5.6-terra`. Swapping
  it at dispatch time is a post-freeze change to a frozen constant — that is a V3 design with a new
  freeze and a new seed commitment, not an environment variable.
- **Report the deterministic arms as an SD70-V2 result.** Refused. No registered outcome is
  decidable from them; the table would be a contrast that could not exist.

## 4. Frozen state — re-verified, not assumed

Everything below was recomputed on the checkout at `main` `fd7a4e4` and compared against the
values recorded in `SD70_V2_PARENT_FIDELITY_RECEIPT_V1.md` at freeze.

| artifact | recomputed sha256 | equals the value frozen at PR #152 |
|---|---|---|
| `SD70_V2_EXECUTION_DESIGN_V1.json` | `96d933e0…28bf4` | yes |
| `sd70v2_generator.py` | `6163a365…de1a56a` | yes |
| `sd70v2_parents.py` | `5883fae4…8365808` | yes |
| `sd70v2_stats.py` | `5c20d2a0…7a239515c` | yes |
| `sd70v2_model_arm.py` | `a35ef58c…95b80afb` | yes |
| `sd70v2_run.py` | `aa6faf35…00328c1db` | yes |

- **Selftest re-executed** (`sd70v2_run.py selftest`): 29 passed, 0 failed. The output file's
  sha256 is `b110e7b6…919a50ec`, equal to the frozen `results/SD70_V2_SELFTEST_V1.json`. This was
  run under **both** CPython 3.9.6 and CPython 3.13.12 and both runs produced that same hash — the
  reproducibility claim was executed, not written.
- **Unit tests re-executed**: `tests/unit/test_sd70_v2_execution.py` and
  `tests/unit/test_sd70_execution_integrity.py`, **16 passed / 0 failed under CPython 3.13.12**.
  Under CPython 3.9.6 one test fails — `test_v2_generator_family_is_byte_identical_to_v1_public_tasks`
  raises `TypeError: zip() takes no keyword arguments` inside the *V1* generator
  (`scripts/generate_scientific_development_meta_benchmark.py:20`, which uses `zip(…, strict=True)`).
  `zip(strict=)` needs CPython 3.10+, so this is an interpreter floor, not a code defect. It is
  recorded because a bare "tests pass" would have concealed which interpreter produced it.

## 5. Custody — the guard is still armed

- The protected seed is present at `~/.orion-custody/sd70-v2/SD70_V2_MASTER_SEED.txt`, mode `600`,
  `revealed: false`. Its recomputed sha256 is
  `4343cdae9fd451f5f4ca23e7a6bb33796deeb6e6d7f355e0a3a6e281bef3b51e`, equal to the commitment
  published in the design at freeze — verified without disclosing the seed.
- **0** protected tasks generated; **0** protected workdirs on disk.
- **0** `PROTECTED_RUN_AUTHORIZATION*.json` files for this study, and none was written this
  session. *Control for that absence:* the same search over the repository and its worktrees
  returns 134 such files overall and 27 for ME-X2, so it demonstrably matches when a file exists.
- The single-run guard therefore remains **armed** for a future dispatch.

## 6. Landed alongside this receipt

`sd70v2_make_receipt.py`, the protected-outcome receipt renderer, is committed with a refusal
guard and **its own exit code**, so that "could not render" can never be mistaken for "rendered
and fine":

| exit | meaning |
|---|---|
| 0 | rendered |
| 1 | usage or IO error |
| 3 | `COULD_NOT_RENDER` — degenerate rollup |

It refuses when a required model arm is absent, scored no task, failed on every task, or records
no model call; when a dispatched arm reports `total_tokens = null`; or when either registered
primary contrast is missing. Two defects in the pre-guard draft are closed by this:

1. it coerced a null token counter to `0`, printing an unmeasured cost as a measured zero;
2. it indexed the primary contrasts unconditionally, so a rollup in which every model arm had
   failed would have rendered a Δ between two accuracies nobody measured.

`tests/unit/test_sd70_v2_receipt_renderer_guard.py` covers each refusal path, asserts that a usage
error keeps a *different* exit code from `COULD_NOT_RENDER`, asserts that a refused render leaves
no receipt file behind, and asserts **the no-alarm case** — a complete rollup still renders at exit
0, so the guard is not a blanket refusal.

## 7. Next action

Unblocking is an operator action, stated once: **log the Codex CLI in** (and, per the standing
pin, reinstall `@openai/codex@0.129.0-alpha.15` first). Once a `gpt-5.6-terra` probe answers `OK`,
SD70-V2 dispatches unchanged — the design, the code and the sealed seed are all verified intact
above, and the guard is still armed. Nothing about the design or the gates may be revisited in the
meantime.

## 8. Authority

This receipt grants **no** scientific truth, causal law, field status, submission readiness or
publication readiness. SD70-V2 remains prospective with zero protected observations. `PARENT_SUFFICIENT`
remains its pre-registered expectation and a legitimate successful terminal, but it has **not** been
observed and must not be reported as though it had been.

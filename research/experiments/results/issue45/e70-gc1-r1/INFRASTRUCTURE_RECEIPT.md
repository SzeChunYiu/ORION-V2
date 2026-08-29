# E70-GC1 R1 infrastructure receipt (2026-08-29, LUNARC lu48)

Run: `e70-gc1-r1` (issue #45). Clone `/projects/hep/fs9/users/scyiu/orion-v2-wave6`
at commit `3b51a2eedb62d3eebef7d8399d128f47c5f33dc4`. Campaign workdir
`/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e70-gc1-r1`, CODEX_HOME
`/projects/hep/fs9/users/scyiu/orion-v2-e45/codex-home` (credential values never
logged; only paths).

## 1. Preflight (GREEN)

- Python 3.13.5 venv at `<clone>/.venv`:
  `python -m py_compile` clean on `src/orion_v2/unified_diff_interface.py`,
  `scripts/orion_codex_arms.py`, `scripts/run_orion_generated_composition_suite.py`,
  `scripts/dispatch_orion_gc1_blinded.py`; `pytest -q` 9/9 on
  `tests/unit/test_unified_diff_interface_wave6.py` +
  `tests/unit/test_generated_composition_suite_wave6.py`. No module env needed.
- No crypto/exchange network is involved at any point (OpenAI codex API only).

## 2. Failures encountered and their fixes

1. **System python 3.12.3 (bare-LD)**: `venv`-bootstrapped interpreter failed to
   import pip/setuptools (`LD_LIBRARY_PATH`-bare busybox env). Fix: build the venv
   from a full-toolchain CPython 3.13.5. Preflight then green (section 1).
2. **codex-cli 0.129.0-alpha.15 (the fleet-pinned version) cannot parse the current
   models registry**: probe fails at startup with
   `failed to decode models response: unknown variant max, expected one of
   none,minimal,low,medium,high,xhigh` (log:
   `campaign-e70-gc1-r1/infra/codex_0.129.0-alpha.15_probe_failure.log`).
   This is a decode incompatibility, not an auth or network problem; 0.129.0-alpha.15
   cannot dispatch at all on this account/registry state.
3. **codex-cli 0.150.1 provisioned** from the official musl static tarball; sha256
   of the binary `abf1bb1643a79f73aa78ee627e111e02d4f8c98f25813a0cf6ce277709664386`,
   registry shasums receipt at `campaign-e70-gc1-r1/infra/codex_binaries_sha256.txt`.
   Version self-report `codex-cli 0.150.1` (`codex_0.150_version.txt`). Probe with
   `-m gpt-5.6-terra` authenticates and reaches the model endpoint
   (`codex_0.150.1_probe_gpt-5.6-terra.log`).
4. **Account usage wall (the only blocking item)**: the only available authenticated
   codex account returns `ERROR: You've hit your usage limit. ... try again at
   Sep 3rd, 2026 6:26 PM.` on every exec (probe logs above; one mention, paired
   with the workaround below). NOT an auth, network, or binary problem.
5. **claude-adapter substitution REJECTED**: swapping the arm executable to
   `scripts/orion_claude_arms.py` was considered and rejected because its
   `_context()` snapshots only `*.py` files, silently changing the task surface the
   arms see relative to the codex arm contract; a cross-adapter arm comparison is
   not a valid within-run control.

## 3. Dispatch decision

- Deferred SLURM dispatch: job **3553088**, `--begin=2026-09-04T08:00:00` (covers
  both UTC and local readings of the Sep 3 6:26 PM reset), 2 cpus, 8G, 24h, lu48.
- The job first runs an in-job availability probe loop (up to 20 attempts, 30 min
  apart, ephemeral exec, `gpt-5.6-terra`, sandboxed read-only, output to
  `campaign-e70-gc1-r1/infra/dispatch_probe_attempt_*`); only after a successful
  probe does it run `scripts/run_orion_generated_composition_pilot.sh` verbatim.
- sbatch copy preserved beside this receipt (`e70_gc1_dispatch_deferred_r1.sbatch`).

## 4. REQUIRED before the job fires

`codex-home/auth.json` is a copy of the Mac codex login; refresh-token rotation on
the Mac will likely invalidate it. Before 2026-09-04 08:00, re-sync:

    scp <mac>:~/.codex/auth.json \
        lunarc:/projects/hep/fs9/users/scyiu/orion-v2-e45/codex-home/auth.json

The in-job probe loop makes a stale auth file fail safe (exit 3 after 20 attempts,
pilot never starts with a broken credential).

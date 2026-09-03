#!/usr/bin/env python3
"""Render the SD70-V2 protected outcome receipt from the frozen rollup."""
import json
import sys
from pathlib import Path

# Exit codes (distinct on purpose):
#   0  receipt rendered from a rollup that can carry the registered contrasts
#   1  usage / IO / schema error
#   3  COULD_NOT_RENDER -- the rollup is degenerate: at least one model arm has no
#      scored task, or every one of its tasks failed, or a resource counter that
#      must exist for a dispatched arm is absent. Rendering such a rollup would
#      print `0` costs that were never measured and a delta between accuracies
#      that were never contested. Refuse instead, loudly.
EXIT_COULD_NOT_RENDER = 3

MODEL_ARMS_REQUIRED = (
    "F2_RECURSIVE_META_DISCOVERY_FULL",
    "F2_STATIC_NO_RECURSION",
    "F2_FULL_MINUS_FAILURE_EVIDENCE",
    "F2_FULL_MINUS_PARENT_FEDERATION",
    "TARGET_ONLY_NEGATIVE_CONTROL",
)


def _refuse(reasons: list[str]) -> None:
    payload = {
        "schema_version": "orion.v2.sd70-v2.receipt-render-refusal.v1",
        "status": "COULD_NOT_RENDER",
        "reasons": reasons,
    }
    print(json.dumps(payload, indent=2, sort_keys=True), file=sys.stderr)
    raise SystemExit(EXIT_COULD_NOT_RENDER)


def _audit_rollup(rollup: dict) -> None:
    """Refuse to render a rollup that cannot carry the registered contrasts.

    Guards the two silent-failure modes this renderer would otherwise commit:
    a counter that never ran reported as 0, and a contrast that could not exist
    reported as a difference between two vacuous accuracies.
    """
    reasons: list[str] = []
    arms = rollup.get("arms")
    if not isinstance(arms, dict) or not arms:
        _refuse(["rollup carries no `arms` map"])
    for arm in MODEL_ARMS_REQUIRED:
        stats = arms.get(arm)
        if stats is None:
            reasons.append(f"required model arm `{arm}` is absent from the rollup")
            continue
        n = stats.get("n")
        if not isinstance(n, int) or n <= 0:
            reasons.append(f"model arm `{arm}` scored no task (n={n!r})")
            continue
        failures = stats.get("arm_failures")
        if isinstance(failures, int) and failures >= n:
            reasons.append(
                f"model arm `{arm}` failed on every task ({failures}/{n}); its accuracy is not a measurement"
            )
        cost = stats.get("resource_cost") or {}
        calls = cost.get("model_calls")
        if not isinstance(calls, int) or calls <= 0:
            reasons.append(f"model arm `{arm}` records no model call (model_calls={calls!r})")
        elif cost.get("total_tokens") is None:
            reasons.append(
                f"model arm `{arm}` dispatched {calls} call(s) but reports total_tokens=None; "
                "a token counter that never ran must not be printed as 0"
            )
    pdq = (rollup.get("primary_outcomes") or {}).get("protected_decision_quality") or {}
    for contrast in ("F2_FULL_vs_SP", "F2_STATIC_vs_SP"):
        if contrast not in pdq:
            reasons.append(f"registered primary contrast `{contrast}` is absent from the rollup")
    if reasons:
        _refuse(reasons)


if len(sys.argv) != 6:
    print(
        "usage: sd70v2_make_receipt.py <rollup.json> <FROZEN_SUITE.json> "
        "<REQUEST_SURFACE_MANIFEST.json> <campaign_meta.json> <out.md>",
        file=sys.stderr,
    )
    raise SystemExit(1)

rollup = json.loads(Path(sys.argv[1]).read_text())
frozen = json.loads(Path(sys.argv[2]).read_text())
manifest = json.loads(Path(sys.argv[3]).read_text())
meta = json.loads(Path(sys.argv[4]).read_text())  # campaign metadata
out = Path(sys.argv[5])

_audit_rollup(rollup)

r = rollup
sp = r["strongest_generator_faithful_parent"]
F2 = "F2_RECURSIVE_META_DISCOVERY_FULL"
F2S = "F2_STATIC_NO_RECURSION"
d = r["primary_outcomes"]["protected_decision_quality"]["F2_FULL_vs_SP"]
ds = r["primary_outcomes"]["protected_decision_quality"]["F2_STATIC_vs_SP"]
holm = r["primary_outcomes"]["holm"]
A = r["arms"]

def arm_row(a):
    s = A[a]
    c = s["resource_cost"]
    # `_audit_rollup` has already refused any dispatched model arm whose token
    # counter is absent; a deterministic arm makes no model call, so `n/a` here
    # means "no counter applies", never "the counter read zero".
    tok = c["total_tokens"] if c["total_tokens"] is not None else "n/a"
    return (f"| `{a}` | {s['n']} | {s['exact_accuracy']:.3f} | "
            f"[{s['wilson95'][0]:.3f}, {s['wilson95'][1]:.3f}] | "
            f"{s['critical_false_direction_rate']:.3f} | {s['arm_failures']} | "
            f"{c['model_calls']} | {tok} | {c['wall_seconds_total']:.1f} |")

protected = [a for a in A if not a.endswith(("__LP", "__QS"))]
controls = [a for a in A if a.endswith(("__LP", "__QS"))]
order = ([a for a in protected if a.startswith("F2")] +
         [sp, "F0_PARENT_FEDERATION", "FIXED_META_LESSON"] +
         [a for a in protected if a not in (sp, "F0_PARENT_FEDERATION", "FIXED_META_LESSON")
          and not a.startswith("F2") and a != "STRONGEST_GENERATOR_FAITHFUL_PARENT"] +
         ["STRONGEST_GENERATOR_FAITHFUL_PARENT"])
seen = set()
_ordered = []
for a in order:
    if a in A and a not in seen:
        seen.add(a)
        _ordered.append(a)
for a in protected:
    if a not in seen:
        seen.add(a)
        _ordered.append(a)
order = _ordered

route = r["route"]
lines = [
f"""# SD70-V2 — Protected Outcome Receipt (V1)

**Study:** SD70-V2 `SYNTHETIC_RECURSIVE_META_POLICY_V2` — ORION-V2 issue #50.
**Protocol:** `research/experiments/SCIENTIFIC_DEVELOPMENT_SD70_PROSPECTIVE_PROTOCOL_V2.json`
(`ORION-SD70-SYNTHETIC-META-POLICY-V2`), status
`PROSPECTIVE_PREOUTCOME_FROZEN__EXECUTION_AUTHORIZED_BLOCKERS_CLOSED`.
**Frozen design:** `research/experiments/sd70-v2/SD70_V2_EXECUTION_DESIGN_V1.{{md,json}}`,
design sha256 `{r['design_sha256']}`, merged to `main` as `{meta['design_merge_sha']}` (PR #152)
**before** any protected task existed.
**Seed commitment:** `{frozen['seed_commitment']}` — published in the design at freeze; the
seed itself was held only at `~/.orion-custody/sd70-v2/SD70_V2_MASTER_SEED.txt` and `prepare`
refuses any seed whose sha256 differs.
**Execution:** LUNARC `{meta['host']}` (`{meta['partition']}`, account `{meta['account']}`), SLURM job
`{meta['jobid']}`, campaign `{meta['workdir']}`, code state `{meta['code_state']}`,
started {meta['started_utc']}, finished {meta['finished_utc']}.
**Authorization:** coordinator instruction of 2026-09-02 to execute the frozen design, citing
this design sha256 and seed commitment. This receipt reports what the frozen gates fired; it
grants no authority (see §8).

## 1. Terminal

```text
SD70_V2_ROUTE = {route}
SD70_V2_STRONGEST_GENERATOR_FAITHFUL_PARENT = {sp}
SD70_V2_PRIMARY_DELTA_F2_FULL_MINUS_STRONGEST_PARENT = {d['point']:+.4f}  (95% bootstrap [{d['ci_low']:+.4f}, {d['ci_high']:+.4f}])
SD70_V2_PROTECTED_TASKS = {r['task_count']}
MACHINE_EPISTEMICS_FIELD_CLAIM_STATUS = FIELD_RESIDUAL_NOT_ESTABLISHED
FLAGSHIP_PUBLICATION_STATUS = UNCHANGED__SUBMISSION_READY_FALSE__PUBLICATION_READY_FALSE
```
""",
"## 2. Protected arms\n",
"| arm | n | exact | Wilson 95% | CFD rate | arm failures | model calls | tokens | wall s |",
"|---|---|---|---|---|---|---|---|---|",
]
lines += [arm_row(a) for a in order]
lines += ["", f"Chance level (mean over tasks): {A[sp]['chance_level']:.3f}.", "",
          "## 3. Registered primary outcomes", "",
          "**3.1 Protected decision quality** (paired difference in exact held-out accuracy, Holm over the two primary contrasts, family alpha "
          f"{meta['alpha_family']}):", "",
          "| contrast | delta | 95% bootstrap CI | b/c | one-sided McNemar mid-p | Holm threshold | reject |",
          "|---|---|---|---|---|---|---|"]
for k, v in r["primary_outcomes"]["protected_decision_quality"].items():
    h = holm[k]
    lines.append(f"| {k} | {v['point']:+.4f} | [{v['ci_low']:+.4f}, {v['ci_high']:+.4f}] | {v['b']}/{v['c']} | "
                 f"{v['midp_one_sided_a_gt_b']:.4g} | {h['holm_threshold']:.4f} | {h['reject']} |")
cf = r["primary_outcomes"]["critical_false_direction"]
nr = r["primary_outcomes"]["parent_non_regression"]
lines += ["", "**3.2 Critical false direction** (selecting a worst action — minimal latent score for the held-out context):", ""]
for k, v in cf.items():
    lines.append(f"- {k}: {v['point']:+.4f} [{v['ci_low']:+.4f}, {v['ci_high']:+.4f}]")
lines += ["", f"**3.3 Parent non-regression:** lower 95% bound {nr['delta_ci_low']:+.4f} vs margin "
              f"-{nr['margin']} -> holds = {nr['holds']}.", "",
          "**3.4 Resource cost** (sum over arm-tasks, failed attempts included):", "",
          "| arm | model calls | attempts | retries | input tok | output tok | tool calls | wall s |",
          "|---|---|---|---|---|---|---|---|"]
for a in order:
    c = A[a]["resource_cost"]
    lines.append(f"| `{a}` | {c['model_calls']} | {c['attempts_total']} | {c['retries']} | "
                 f"{c['input_tokens']} | {c['output_tokens']} | {c['tool_calls']} | {c['wall_seconds_total']:.1f} |")
lines += ["", "## 4. Mandatory controls and ablations", "",
          "| control | accuracy | chance | Wilson 95% | behaves |", "|---|---|---|---|---|"]
for k, v in r["negative_controls"].items():
    lines.append(f"| `{k}` | {v['accuracy']:.3f} | {v['chance']:.3f} | [{v['wilson95'][0]:.3f}, {v['wilson95'][1]:.3f}] | {v['behaves']} |")
lines += ["", "Ablations (F2_FULL minus ablation, paired):", ""]
for k, v in r["ablations"].items():
    lines.append(f"- **{k}**: {v['point']:+.4f} [{v['ci_low']:+.4f}, {v['ci_high']:+.4f}], b/c {v['b']}/{v['c']}, mid-p {v['midp_one_sided_a_gt_b']:.4g}")
lines += ["", "Secondary contrasts:", ""]
for k, v in r["secondary"].items():
    lines.append(f"- {k}: {v['point']:+.4f} [{v['ci_low']:+.4f}, {v['ci_high']:+.4f}]")
mi = r["missingness"]
lines += ["", "## 5. Missingness and integrity", "",
          f"- Model arm-tasks: {mi['model_arm_tasks']}; arm failures: {mi['model_arm_failures']}; "
          f"global failure rate {mi['global_failure_rate']:.4f} (threshold {meta['global_failure_threshold']}).",
          f"- Arms exceeding the per-arm threshold ({meta['per_arm_failure_threshold']}): "
          f"{mi['per_arm_exceeding_threshold'] or 'none'}.",
          f"- Integrity violations: {meta['integrity_violations']}; dispatch integrity passed: {meta['dispatch_integrity_passed']}.",
          f"- Private oracle removed before dispatch and restored hash-exactly (sha256 `{meta['oracle_sha256']}`).",
          "- `public_tasks.json` and the whole `requests/` tree were mode 000 for the entire model dispatch; each model child ran in an empty `/local/slurmtmp` cwd with a private copy of its own request only.",
          f"- Request surface manifest sha256 `{frozen['manifest_sha256']}`; training-token leaks into any TARGET_ONLY request: "
          f"{manifest['arms']['TARGET_ONLY_NEGATIVE_CONTROL']['training_token_leaks_into_target_only']}.",
          f"- Model attestation probe replied `OK` for the requested model `{meta['model']}`; the Codex `--json` event stream exposes no served-model id, so each response records `served_model_observed: null` with its reason. This endpoint refuses an unservable model with HTTP 400 rather than substituting one (observed the same day on an older CLI).",
          "", "## 6. Gates", ""]
for k, v in r["gates"].items():
    lines.append(f"- `{k}`: {v}")
if r["cannot_check_reasons"]:
    lines += ["", "CANNOT_CHECK reasons:", ""] + [f"- {x}" for x in r["cannot_check_reasons"]]
lines += ["", "## 7. Deviations", "",
          meta["deviations"], "",
          "## 8. Authority", "",
          "This receipt grants **no** scientific truth, causal law, field status, submission readiness or",
          "publication readiness. Its scope is synthetic rule-induction mechanism evidence inside the frozen",
          "generator family only; it does not support naturalistic scientific-development superiority,",
          "science-of-science superiority, or a Machine Epistemics field residual.",
          "",
          "Artifacts: `SD70_V2_ROLLUP.json` / `.md` and `SD70_V2_ARM_RECORDS.json` in this directory,",
          f"copied verbatim from `{meta['workdir']}`.", ""]
out.write_text("\n".join(lines) + "\n")
print(f"wrote {out} route={route}")

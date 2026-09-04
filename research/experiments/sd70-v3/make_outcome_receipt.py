#!/usr/bin/env python3
"""Render the SD70-V3 outcome receipt from the frozen rollup.

Reads only artifacts the campaign produced. Every count is printed with the
denominator it was computed over, and every "0" is accompanied by the number of
cases it was computed from -- a zero without its denominator is not a result.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def pct(x): return f"{x:.4f}"


def main(workdir: Path, out: Path) -> int:
    r = json.loads((workdir / "SD70_V3_ROLLUP.json").read_text())
    auth = json.loads((workdir / "PROTECTED_RUN_AUTHORIZATION.json").read_text())
    frozen = json.loads((workdir / "FROZEN_SUITE.json").read_text())
    sp = "STRONGEST_GENERATOR_FAITHFUL_PARENT"
    f2 = "F2_RECURSIVE_META_DISCOVERY_FULL"
    f2s = "F2_STATIC_NO_RECURSION"
    A = r["arms"]
    d = r["primary_outcomes"]["protected_decision_quality"]["F2_FULL_vs_SP"]
    L = []
    w = L.append

    w("# SD70-V3 — Protected Outcome Receipt (V1)\n")
    w(f"**Terminal route: `{r['route']}`**\n")
    w(f"Design sha256 `{r['design_sha256']}` (identical to the frozen design; `evaluate` refuses otherwise). "
      f"Protected tasks {r['task_count']}. Comparator {frozen['strongest_generator_faithful_parent']} "
      f"(frozen on the V3 development split before generation).\n")
    if r["cannot_check_reasons"]:
        w("## Why the campaign could not be checked\n")
        for x in r["cannot_check_reasons"]:
            w(f"- {x}")
        w("")

    w("## Primary estimand\n")
    w(f"Δ = acc({f2}) − acc(comparator) = **{pct(d['point'])}** "
      f"(95 % bootstrap CI [{pct(d['ci_low'])}, {pct(d['ci_high'])}], "
      f"McNemar mid-p one-sided {d['midp_one_sided_a_gt_b']:.4g}, discordant b={d['b']} c={d['c']}, n={d['n']}).\n")
    w(f"Registered minimum effect 0.10; non-inferiority margin −0.05.\n")

    w("## Arm results\n")
    w("| arm | n | exact accuracy | Wilson 95 % | CFD rate | arm failures |")
    w("|---|---|---|---|---|---|")
    for a, s in sorted(A.items(), key=lambda kv: -kv[1]["exact_accuracy"]):
        if "__" in a:
            continue
        lo, hi = s["wilson95"]
        w(f"| {a} | {s['n']} | {pct(s['exact_accuracy'])} | [{pct(lo)}, {pct(hi)}] | "
          f"{pct(s['critical_false_direction_rate'])} | {s['arm_failures']}/{s['n']} |")
    w(f"\nChance level {pct(A[sp]['chance_level'])}.\n")

    w("## Negative controls (each with its denominator)\n")
    w("| control | n | accuracy | Wilson 95 % lower | chance | behaves |")
    w("|---|---|---|---|---|---|")
    for k, v in r["negative_controls"].items():
        w(f"| {k} | {A[k]['n']} | {pct(v['accuracy'])} | {pct(v['wilson95'][0])} | {pct(v['chance'])} | {v['behaves']} |")
    w("")

    w("## Registered gates\n")
    w("| gate | value |\n|---|---|")
    for k, v in r["gates"].items():
        w(f"| {k} | {v} |")
    w("")

    w("## Ablations\n")
    w("| ablation | Δ vs full | CI | mid-p |\n|---|---|---|---|")
    for k, v in r["ablations"].items():
        w(f"| {k} | {pct(v['point'])} | [{pct(v['ci_low'])}, {pct(v['ci_high'])}] | {v['midp_one_sided_a_gt_b']:.4g} |")
    w("")

    w("## Silent-failure audit\n")
    dv = r["arm_divergence"]
    w("**1. Counters that never ran.** Every count below is reported with its denominator.\n")
    eh = r["envelope_homogeneity"]
    w(f"Envelope homogeneity verdict `{eh['verdict']}` over **{eh['denominator']} completed model "
      f"envelopes** ({eh.get('failed_envelopes_excluded', 0)} failed envelopes excluded — those are the "
      f"missingness gate's business).\n")
    w("| check | value | denominator | passed |\n|---|---|---|---|")
    for k, v in eh["checks"].items():
        val = v.get("value")
        val = pct(val) if isinstance(val, float) else f"observable {v.get('observable_envelopes')}, mismatches {v.get('mismatches')}"
        w(f"| {k} | {val} | {v['denominator']} | {v['passed']} |")
    w("")
    cc = r["channel_contract"]
    w(f"**Channel contract verdict `{cc['verdict']}`**, measured at campaign start AND end on "
      f"byte-frozen canaries.\n")
    if "checks" in cc:
        w("| check | denominator | passed |\n|---|---|---|")
        for c in cc["checks"]:
            w(f"| {c['check']} | {c['denominator']} | {c['passed']} |")
        if cc.get("reported_not_gating_failures"):
            w(f"\nReported but not gating (pre-run decision): {cc['reported_not_gating_failures']}.")
    w("")
    w("**2. Contrasts that could not exist.** Asserted, not assumed:\n")
    w("| pair | shared tasks | requests differing | prompts differing |\n|---|---|---|---|")
    for p in dv["pairs"]:
        w(f"| {p['pair'][0]} vs {p['pair'][1]} | {p['shared_tasks']} | "
          f"{p['requests_differing']}/{p['shared_tasks']} | {p['prompts_differing']}/{p['shared_tasks']} |")
    w("")
    for s in dv["structural"]:
        keys = {k: v for k, v in s.items() if k not in ("assertion", "passed")}
        w(f"- **{s['passed']}** — {s['assertion']} ({keys})")
    w("")
    w("**3. Sentences nobody executed.** `evaluate` re-checks the design sha256 against the frozen "
      "suite and refuses on mismatch; the interpreter-determinism boundary was measured across three "
      "CPython versions rather than asserted (see the design, §13); the failure path was rehearsed "
      "with a failing stub before the protected run.\n")
    w("**4. Rendered status trusted in place of the thing.** The terminal route above is computed from "
      "the arm records, not read from any status line. Landing is decided by "
      "`git merge-base --is-ancestor`, not by a PR badge.\n")

    w("## Resource cost\n")
    w("| arm | model calls | attempts | retries | input tokens | output tokens | wall s |\n|---|---|---|---|---|---|---|")
    for a in sorted(frozen["model_arms"]):
        c = A[a]["resource_cost"]
        w(f"| {a} | {c['model_calls']} | {c['attempts_total']} | {c['retries']} | {c['input_tokens']} | "
          f"{c['output_tokens']} | {c['wall_seconds_total']:.0f} |")
    w("")

    w("## Authority\n")
    w("This receipt grants nothing: no scientific truth, no causal law, no field status, no submission "
      "or publication readiness. A null here means **no residual detectable in the registered decision "
      "problems the parents already solve exactly** — never that no residual exists. MAXMARGIN_PARENT "
      "is optimal by construction on this generator family up to its regularization and optimizer "
      "budget; that was declared in the frozen design, not discovered here.\n")
    w(f"Run authorization `{auth['state']}` is archived on completion, re-arming the guard against a "
      f"second protected dispatch. SD70-V2's separate authorization remains unspent and its "
      f"`PARENT_SUFFICIENT` expectation remains unobserved.\n")

    out.write_text("\n".join(L) + "\n")
    print(json.dumps({"receipt": str(out), "route": r["route"], "lines": len(L)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))

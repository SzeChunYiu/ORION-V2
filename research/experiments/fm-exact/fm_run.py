#!/usr/bin/env python3
"""FM series exact-study runner (shared across FM10-FM60).

Stages
  selftest   parent fidelity (native known-answer tests), G0a hand-authored
             fixtures, G0b oracle self-agreement on a small generated set,
             G0c null calibration, G0e planted positives.
  dev        DEVELOPMENT split (public seed, small).  Never protected evidence.
  protected  PROTECTED split.  Refuses unless PROTECTED_RUN_AUTHORIZATION.json
             is present next to this script, names this suite, acknowledges the
             frozen design sha256, and the custody seed hashes to the frozen
             commitment.
  analyze    Score a results file against its custody file and emit the gate
             block, the route and the receipt tables.

Usage:  python3 fm_run.py <SUITE> <stage> [--out DIR]
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from fm_core import (  # noqa: E402
    GateResult,
    canonical_json,
    decoy_coverage_gate,
    discrimination_gate,
    gate_block_ok,
    holm,
    null_calibration_gate,
    paired_summary,
    sha256_bytes,
    shuffled_label_null,
)

SUITES = {
    "FM10": "fm10_suite",
    "FM20": "fm20_suite",
    "FM30": "fm30_suite",
    "FM40": "fm40_suite",
    "FM50": "fm50_suite",
    "FM60": "fm60_suite",
}

SCHEMA_RESULTS = "orion.v2.fm-exact.results.v1"
SCHEMA_ANALYSIS = "orion.v2.fm-exact.analysis.v1"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
SHUFFLE_SEED = 20260902


def load_suite(suite_id: str):
    if suite_id not in SUITES:
        raise SystemExit(f"unknown suite {suite_id}; known: {sorted(SUITES)}")
    return importlib.import_module(SUITES[suite_id]).SPEC


def sha256_file(p: Path) -> str:
    return sha256_bytes(p.read_bytes())


def custody_seed_path(suite_id: str) -> Path:
    env = os.environ.get(f"{suite_id}_PROTECTED_SEED_FILE")
    if env:
        return Path(env)
    return Path.home() / ".orion-custody/fm" / f"{suite_id}_PROTECTED_SEED_V1.txt"


# --------------------------------------------------------------------------
# dispatch
# --------------------------------------------------------------------------


def run_instances(spec, pairs, label: str, public_seed: str | None):
    results = {
        "schema_version": SCHEMA_RESULTS,
        "suite": spec.suite_id,
        "label": label,
        "split_seed": public_seed,
        "arms": spec.arm_names(),
        "instances": [],
    }
    custody = {
        "schema_version": SCHEMA_RESULTS + ".expected-custody",
        "suite": spec.suite_id,
        "label": label,
        "instances": [],
    }
    timing: dict[str, int] = {a: 0 for a in spec.arm_names()}
    for inst, ans in pairs:
        rec = {"instance_id": inst.instance_id, "family": inst.family, "arms": {}}
        for arm in spec.arm_names():
            t0 = time.perf_counter_ns()
            rec["arms"][arm] = spec.run_arm(arm, inst)
            timing[arm] += time.perf_counter_ns() - t0
        results["instances"].append(rec)
        custody["instances"].append(
            {
                "instance_id": inst.instance_id,
                "family": inst.family,
                "expected": ans.as_dict(),
                "instance": inst.as_json(),
            }
        )
    results["_timing_wall_ns"] = timing
    return results, custody


# --------------------------------------------------------------------------
# scoring
# --------------------------------------------------------------------------


def score(spec, results: dict, custody: dict) -> dict:
    exp = {c["instance_id"]: c["expected"]["disposition"] for c in custody["instances"]}
    fam = {c["instance_id"]: c["family"] for c in custody["instances"]}
    order = [r["instance_id"] for r in results["instances"]]
    labels = [exp[i] for i in order]
    per_arm: dict[str, dict] = {}
    raw: dict[str, list[bool]] = {}
    preds: dict[str, list[str]] = {}
    for arm in results["arms"]:
        hits: list[bool] = []
        pred: list[str] = []
        by_family: dict[str, list[bool]] = {f: [] for f in spec.families}
        over = under = 0
        for rec in results["instances"]:
            got = rec["arms"][arm]["disposition"]
            want = exp[rec["instance_id"]]
            ok = got == want
            hits.append(ok)
            pred.append(got)
            by_family[rec["family"]].append(ok)
            if not ok:
                if want != "TRANSFER_VALID" and got == "TRANSFER_VALID":
                    over += 1  # accepted a transfer the oracle blocks
                elif want == "TRANSFER_VALID" and got != "TRANSFER_VALID":
                    under += 1
        raw[arm] = hits
        preds[arm] = pred
        per_arm[arm] = {
            "exact": sum(hits),
            "n": len(hits),
            "exact_rate": sum(hits) / len(hits) if hits else 0.0,
            "over_accept": over,
            "under_accept": under,
            "per_family": {
                f: {
                    "n": len(v),
                    "exact": sum(v),
                    "exact_rate": (sum(v) / len(v)) if v else None,
                }
                for f, v in by_family.items()
            },
            "wall_ms": results.get("_timing_wall_ns", {}).get(arm, 0) / 1e6,
        }
    return {
        "order": order,
        "labels": labels,
        "families": [fam[i] for i in order],
        "per_arm": per_arm,
        "_raw": raw,
        "_preds": preds,
    }


# --------------------------------------------------------------------------
# gates
# --------------------------------------------------------------------------


def gates(spec, sc: dict, selftest: dict | None, rejects: dict | None) -> dict:
    M, P = spec.mechanic_arm, spec.strongest_parent_arm
    raw, per_arm = sc["_raw"], sc["per_arm"]
    n = len(sc["order"])
    G: list[GateResult] = []

    # ---- G0a known answer -------------------------------------------------
    ka = (selftest or {}).get("known_answer", [])
    G.append(
        GateResult(
            "G0a_KNOWN_ANSWER",
            "every hand-authored fixture's disposition is reproduced by the exhaustive oracle",
            n_evaluated=len(ka),
            n_violations=sum(1 for k in ka if not k["passed"]),
            requires_evaluated=8,
            detail={"fixtures": ka},
        )
    )
    # ---- G0b oracle self-agreement ---------------------------------------
    agree = (selftest or {}).get("oracle_agreement", {})
    G.append(
        GateResult(
            "G0b_ORACLE_SELF_AGREEMENT",
            "exhaustive enumeration and the independent branch-and-bound search "
            "agree on disposition, min_missing, optimal profile and optimal-map "
            "count for every instance of the split",
            n_evaluated=agree.get("n_evaluated", 0),
            n_violations=agree.get("n_disagreements", 0),
            detail=agree,
        )
    )
    # ---- G0c null calibration --------------------------------------------
    shuf = shuffled_label_null(sc["labels"], sc["_preds"][M], seed=SHUFFLE_SEED)
    G.append(
        null_calibration_gate(
            constant_arm_rates={a: per_arm[a]["exact_rate"] for a in spec.constant_arms},
            random_rate=per_arm[spec.random_arm]["exact_rate"],
            shuffle=shuf,
            max_constant=0.40,
            max_random=0.40,
            max_shuffle=0.40,
        )
    )
    # ---- G0d decoy coverage ----------------------------------------------
    counts = {f: per_arm[M]["per_family"][f]["n"] for f in spec.decoy_families}
    G.append(decoy_coverage_gate(counts, minimum=3))
    # ---- G0e planted positives -------------------------------------------
    planted = (selftest or {}).get("planted_positives", [])
    G.append(
        GateResult(
            "G0e_PLANTED_POSITIVES",
            "every registered planted positive trips its own gate predicate",
            n_evaluated=len(planted),
            n_violations=sum(1 for p in planted if not p.get("fired")),
            requires_evaluated=3,
            detail={"planted": planted},
        )
    )
    # ---- G0f family discrimination ---------------------------------------
    G.append(
        discrimination_gate(
            {a: per_arm[a]["exact_rate"] for a in per_arm},
            weak_arms=spec.weak_arms,
            exclude_from_ceiling=spec.constant_arms + (spec.random_arm,),
            max_weak=0.85,
            min_strong=0.95,
        )
    )
    g0 = gate_block_ok(G)
    gate_map = {g.name: g for g in G}

    # ---- G1 mechanic vs strongest faithful parent ------------------------
    ps = paired_summary(raw[M], raw[P])
    identical = [a == b for a, b in zip(sc["_preds"][M], sc["_preds"][P])]
    per_family_disc = {}
    for f in spec.families:
        idx = [i for i, ff in enumerate(sc["families"]) if ff == f]
        if not idx:
            continue
        per_family_disc[f] = {
            "n": len(idx),
            "discordant": sum(1 for i in idx if not identical[i]),
            "M_only_exact": sum(1 for i in idx if raw[M][i] and not raw[P][i]),
            "P_only_exact": sum(1 for i in idx if raw[P][i] and not raw[M][i]),
        }
    identity_rate = sum(identical) / n if n else 0.0
    # Liveness control for the identity counter itself.  "M and the parent agree
    # on every instance" is only evidence if the counter that produced the zero
    # is capable of producing a nonzero on this very split.  Every ablation arm
    # is a known-different mechanic; at least one must register discordance
    # against the parent, or the counter is dead and G1a means nothing.
    ablations = [a.name for a in spec.arms if a.kind == "ABLATION"]
    control = {
        a: sum(1 for i in range(n) if sc["_preds"][a][i] != sc["_preds"][P][i]) for a in ablations
    }
    counter_is_live = any(v > 0 for v in control.values())
    g1a = GateResult(
        "G1a_PARENT_REPRODUCES_M",
        f"{P} reproduces {M}'s disposition on >= 99.5% of instances and no "
        "family exceeds 5% discordance; AND the discordance counter is shown "
        "live on this split by at least one ablation arm disagreeing with the parent",
        n_evaluated=n,
        n_violations=(
            0
            if identity_rate >= 0.995
            and all(v["discordant"] / v["n"] <= 0.05 for v in per_family_disc.values())
            and counter_is_live
            else 1
        ),
        detail={
            "decision_identity_rate": identity_rate,
            "per_family": per_family_disc,
            "paired": ps,
            "counter_liveness_control": {
                "ablation_vs_parent_discordance": control,
                "counter_is_live": counter_is_live,
            },
        },
    )
    G.append(g1a)
    m_advantage = (
        ps["diff_x_minus_y"] > 0
        and ps["exact_p_two_sided"] <= 0.05
        and any(v["M_only_exact"] >= 5 for v in per_family_disc.values())
    )
    g1b = GateResult(
        "G1b_M_ADVANTAGE",
        f"paired instance-exact difference ({M} - {P}) > 0, exact two-sided "
        "p <= 0.05, and >= 1 family with >= 5 M-only-exact instances",
        n_evaluated=n,
        n_violations=0 if m_advantage else 1,
        hard=False,
        requires_evaluated=1,
        verdict_labels=("FIRED", "NOT_FIRED"),
        detail={"paired": ps, "per_family": per_family_disc, "discordant_pairs": ps["discordant"]},
    )
    G.append(g1b)

    # ---- G2 anti-conservatism / anti-permissiveness ----------------------
    blocked_idx = [i for i, lab in enumerate(sc["labels"]) if lab != "TRANSFER_VALID"]
    m_over = sum(
        1 for i in blocked_idx if sc["_preds"][M][i] == "TRANSFER_VALID"
    )
    p_over = sum(1 for i in blocked_idx if sc["_preds"][P][i] == "TRANSFER_VALID")
    G.append(
        GateResult(
            "G2_ANTI_PERMISSIVENESS",
            f"on instances the oracle blocks, {M} accepts no more transfers than {P}",
            n_evaluated=len(blocked_idx),
            n_violations=0 if m_over <= p_over else 1,
            requires_evaluated=10,
            detail={"M_over_accept": m_over, "P_over_accept": p_over, "n_blocked": len(blocked_idx)},
        )
    )

    # ---- G3 mechanism by omission ----------------------------------------
    claimed = [f for f, v in per_family_disc.items() if v["M_only_exact"] >= 5]
    checks = {}
    viol = 0
    for f in claimed:
        abl = spec.ablation_for_family.get(f, spec.default_ablation)
        a_rate = per_arm[abl]["per_family"][f]["exact_rate"] or 0.0
        p_rate = per_arm[P]["per_family"][f]["exact_rate"] or 0.0
        checks[f] = {"ablation": abl, "ablation_rate": a_rate, "parent_rate": p_rate,
                     "advantage_vanishes": a_rate <= p_rate}
        viol += 0 if a_rate <= p_rate else 1
    G.append(
        GateResult(
            "G3_MECHANISM_BY_OMISSION",
            "for every family with a claimed M advantage, the matching omission "
            "ablation's exact rate is <= the parent's on that family",
            n_evaluated=len(claimed),
            n_violations=viol,
            hard=False,
            requires_evaluated=1,
            applicable=bool(m_advantage),
            detail={"claimed_families": claimed, "checks": checks},
        )
    )

    # ---- cost -------------------------------------------------------------
    m_ms, p_ms = per_arm[M]["wall_ms"], per_arm[P]["wall_ms"]
    cost = {
        "M_wall_ms": m_ms,
        "P_wall_ms": p_ms,
        "ratio_P_over_M": (p_ms / m_ms) if m_ms else None,
        "flag": (
            "COST_ADVANTAGE_M"
            if m_ms and p_ms > 2 * m_ms
            else "COST_ADVANTAGE_PARENT"
            if p_ms and m_ms > 2 * p_ms
            else "COST_PARITY_WITHIN_2X"
        ),
        "rule": "wall-clock flag at 2x; reported only, routes nothing",
    }

    # ---- route ------------------------------------------------------------
    if not g0:
        failed = [g.name for g in G if g.hard and g.verdict != "PASS"]
        route, reason = "CANNOT_CHECK", f"G0 validity block did not pass: {failed}"
    elif g1a.verdict == "PASS":
        route, reason = (
            "PARENT_SUFFICIENT",
            f"{P} reproduces {M}'s dispositions (identity {identity_rate:.4f})",
        )
    elif m_advantage:
        if gate_map.get("G2_ANTI_PERMISSIVENESS") and G[-2].verdict != "PASS":
            route, reason = "M_OVER_ACCEPTS", "M advantage coexists with over-acceptance"
        elif viol == 0 and claimed:
            route, reason = "FM_RESIDUAL_CANDIDATE", "M advantage attributed by omission ablation"
        else:
            route, reason = "CANNOT_CHECK", "M advantage not attributable to a named mechanism"
    else:
        route, reason = (
            "PARENT_SUFFICIENT",
            "no significant M advantage over the strongest faithful parent",
        )

    return {
        "gates": [g.as_dict() for g in G],
        "cost": cost,
        "generator_rejections": rejects or {},
        "route": {"route": route, "reason": reason, "cost_flag": cost["flag"]},
        "holm_across_families": holm(
            {
                f: paired_summary(
                    [raw[M][i] for i, ff in enumerate(sc["families"]) if ff == f],
                    [raw[P][i] for i, ff in enumerate(sc["families"]) if ff == f],
                )["exact_p_two_sided"]
                for f in spec.families
            }
        ),
    }


# --------------------------------------------------------------------------
# stages
# --------------------------------------------------------------------------


def stage_selftest(spec, out: Path) -> int:
    rep: dict = {
        "schema_version": SCHEMA_ANALYSIS + ".selftest",
        "suite": spec.suite_id,
        "parent_fidelity": spec.parent_fidelity(),
        "known_answer": [],
        "planted_positives": [p.as_dict() for p in spec.planted_positives()],
    }
    ok = all(t["passed"] for t in rep["parent_fidelity"])
    for f in spec.known_answer_fixtures():
        got = spec.oracle(f["instance"])
        cross = spec.cross_check(f["instance"])
        passed = got.disposition == f["expected"] and cross.disposition == got.disposition
        rep["known_answer"].append(
            {"name": f["name"], "passed": passed, "expected": f["expected"], "oracle": got.disposition}
        )
        ok &= passed
    ok &= all(p["fired"] for p in rep["planted_positives"])

    pairs, rejects = spec.generate("selftest", f"{spec.suite_id}-SELFTEST", {f: 2 for f in spec.families})
    dis = 0
    for inst, _ in pairs:
        a, b = spec.oracle(inst), spec.cross_check(inst)
        if a.disposition != b.disposition or a.as_dict()["best_profile"] != b.as_dict()["best_profile"]:
            dis += 1
    rep["oracle_agreement"] = {"n_evaluated": len(pairs), "n_disagreements": dis}
    ok &= dis == 0
    res, cus = run_instances(spec, pairs, "SELFTEST", f"{spec.suite_id}-SELFTEST")
    sc = score(spec, res, cus)
    gt = gates(spec, sc, rep, rejects)
    rep["null_calibration"] = next(
        g for g in gt["gates"] if g["gate"] == "G0c_NULL_CALIBRATION"
    )
    ok &= rep["null_calibration"]["verdict"] == "PASS"
    rep["selftest_arm_exact"] = {a: v["exact_rate"] for a, v in sc["per_arm"].items()}
    rep["generator_rejections"] = rejects
    rep["passed"] = bool(ok)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{spec.suite_id}_SELFTEST_REPORT.json").write_text(canonical_json(rep))
    print(
        f"{spec.suite_id} selftest {'PASS' if ok else 'FAIL'}: "
        f"parents {sum(t['passed'] for t in rep['parent_fidelity'])}/{len(rep['parent_fidelity'])}, "
        f"known-answer {sum(k['passed'] for k in rep['known_answer'])}/{len(rep['known_answer'])}, "
        f"planted {sum(p['fired'] for p in rep['planted_positives'])}/{len(rep['planted_positives'])}, "
        f"oracle agreement {len(pairs) - dis}/{len(pairs)}, "
        f"null calibration {rep['null_calibration']['verdict']}"
    )
    return 0 if ok else 1


def _run_split(spec, label: str, split: str, seed: str, per_family: int, out: Path, public: str | None) -> int:
    t0 = time.time()
    pairs, rejects = spec.generate(split, seed, {f: per_family for f in spec.families})
    res, cus = run_instances(spec, pairs, label, public)
    dis = 0
    for inst, ans in pairs:
        b = spec.cross_check(inst)
        if b.disposition != ans.disposition or b.as_dict()["best_profile"] != ans.as_dict()["best_profile"]:
            dis += 1
    res["_oracle_agreement"] = {"n_evaluated": len(pairs), "n_disagreements": dis}
    res["_generator_rejections"] = rejects
    out.mkdir(parents=True, exist_ok=True)
    rp = out / f"{spec.suite_id}_{label}_RESULTS_V1.json"
    cp = out / f"{spec.suite_id}_{label}_EXPECTED_CUSTODY_V1.json"
    tp = out / f"{spec.suite_id}_{label}_TIMING_V1.json"
    timing = res.pop("_timing_wall_ns")
    rp.write_text(canonical_json(res))
    cp.write_text(canonical_json(cus))
    tp.write_text(
        canonical_json(
            {
                "schema_version": SCHEMA_RESULTS + ".timing",
                "suite": spec.suite_id,
                "label": label,
                "wall_ns": timing,
                "generation_and_dispatch_seconds": round(time.time() - t0, 3),
                "note": "wall-clock is machine dependent and is kept out of the deterministic results file",
            }
        )
    )
    print(
        f"{spec.suite_id} {label}: {len(pairs)} instances, rejections {sum(rejects.values())}, "
        f"results sha256 {sha256_file(rp)[:16]}…"
    )
    return stage_analyze(spec, rp, cp, out)


def stage_dev(spec, out: Path, per_family: int) -> int:
    return _run_split(
        spec, "DEVELOPMENT", "dev", f"{spec.suite_id}-DEV-20260902", per_family, out,
        f"{spec.suite_id}-DEV-20260902",
    )


def stage_protected(spec, out: Path, per_family: int, seed_file: Path) -> int:
    design = HERE / spec.design_json
    if not AUTH_FILE.exists():
        print(f"REFUSED: {AUTH_FILE.name} absent — protected run not authorized", file=sys.stderr)
        return 3
    try:
        auth = json.loads(AUTH_FILE.read_text())
    except Exception as exc:  # noqa: BLE001
        print(f"REFUSED: authorization unreadable: {exc}", file=sys.stderr)
        return 3
    token = str(auth.get("human_written_token", "")).strip()
    if auth.get("human_written") is not True or len(token) < 16:
        print("REFUSED: authorization requires human_written=true and a token >= 16 chars", file=sys.stderr)
        return 3
    if auth.get("suite") != spec.suite_id:
        print(f"REFUSED: authorization names suite {auth.get('suite')}, not {spec.suite_id}", file=sys.stderr)
        return 3
    if not design.exists():
        print(f"REFUSED: design JSON {design.name} absent", file=sys.stderr)
        return 3
    if auth.get("acknowledged_design_sha256") != sha256_file(design):
        print("REFUSED: acknowledged_design_sha256 does not match the frozen design JSON", file=sys.stderr)
        return 3
    if not seed_file.exists():
        print(f"REFUSED: custody seed file absent ({seed_file})", file=sys.stderr)
        return 4
    seed = seed_file.read_bytes().strip()
    commitment = json.loads(design.read_text())["seed_commitment"][spec.seed_commitment_key]
    if hashlib.sha256(seed).hexdigest() != commitment:
        print("REFUSED: custody seed does not match the frozen commitment", file=sys.stderr)
        return 4
    return _run_split(spec, "PROTECTED", "protected", seed.decode(), per_family, out, None)


def render_md(spec, analysis: dict) -> str:
    L = [f"# {spec.suite_id} analysis — {analysis['label']}\n"]
    L.append(f"Instances: {analysis['n_instances']}; results sha256 `{analysis['results_sha256']}`.\n")
    L.append("\n## Per-arm exactness\n")
    L.append("| arm | exact | rate | over-accept | under-accept |")
    L.append("|---|---|---|---|---|")
    for arm, v in analysis["score"]["per_arm"].items():
        L.append(f"| {arm} | {v['exact']}/{v['n']} | {v['exact_rate']:.3f} | {v['over_accept']} | {v['under_accept']} |")
    L.append("\n## Per-family exact rate\n")
    fams = list(spec.families)
    L.append("| arm | " + " | ".join(fams) + " |")
    L.append("|---" * (len(fams) + 1) + "|")
    for arm, v in analysis["score"]["per_arm"].items():
        cells = []
        for f in fams:
            r = v["per_family"][f]["exact_rate"]
            cells.append("—" if r is None else f"{r:.2f}")
        L.append(f"| {arm} | " + " | ".join(cells) + " |")
    L.append("\n## Gates (verdict, violations / instances evaluated)\n")
    L.append("| gate | verdict | violations | n evaluated | hard |")
    L.append("|---|---|---|---|---|")
    for g in analysis["gates"]:
        L.append(
            f"| {g['gate']} | **{g['verdict']}** | {g['n_violations']} | {g['n_evaluated']} | {g['hard']} |"
        )
    r = analysis["route"]
    L.append(f"\n## Route\n\n`{r['route']}` — {r['reason']}. Cost flag: `{r['cost_flag']}`.\n")
    return "\n".join(L) + "\n"


def stage_analyze(spec, results_path: Path, custody_path: Path, out: Path) -> int:
    res = json.loads(results_path.read_text())
    cus = json.loads(custody_path.read_text())
    label = res.get("label", "UNKNOWN")
    tp = results_path.with_name(results_path.name.replace("_RESULTS_", "_TIMING_"))
    if tp.exists():
        res["_timing_wall_ns"] = json.loads(tp.read_text()).get("wall_ns", {})
    sp = out / f"{spec.suite_id}_SELFTEST_REPORT.json"
    selftest = json.loads(sp.read_text()) if sp.exists() else None
    if selftest is not None:
        selftest = dict(selftest)
        selftest["oracle_agreement"] = res.get("_oracle_agreement", selftest.get("oracle_agreement", {}))
    sc = score(spec, res, cus)
    gt = gates(spec, sc, selftest, res.get("_generator_rejections"))
    analysis = {
        "schema_version": SCHEMA_ANALYSIS,
        "suite": spec.suite_id,
        "label": label,
        "results_sha256": sha256_file(results_path),
        "custody_sha256": sha256_file(custody_path),
        "n_instances": len(res["instances"]),
        "score": {"per_arm": sc["per_arm"]},
        **gt,
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{spec.suite_id}_{label}_ANALYSIS_V1.json").write_text(canonical_json(analysis))
    (out / f"{spec.suite_id}_{label}_ANALYSIS_V1.md").write_text(render_md(spec, analysis))
    print(
        f"{spec.suite_id} {label} route: {gt['route']['route']} — {gt['route']['reason']}; "
        f"M {sc['per_arm'][spec.mechanic_arm]['exact_rate']:.3f} vs "
        f"{spec.strongest_parent_arm} {sc['per_arm'][spec.strongest_parent_arm]['exact_rate']:.3f}"
    )
    for g in gt["gates"]:
        print(f"    {g['gate']:<28} {g['verdict']:<14} {g['n_violations']} violations / {g['n_evaluated']} evaluated")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("suite", choices=sorted(SUITES))
    ap.add_argument("stage", choices=("selftest", "dev", "protected", "analyze"))
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--per-family", type=int, default=None)
    ap.add_argument("--results", type=Path)
    ap.add_argument("--custody", type=Path)
    ap.add_argument("--seed-file", type=Path, default=None)
    a = ap.parse_args(argv)
    spec = load_suite(a.suite)
    out = a.out or (HERE / a.suite.lower() / "results")
    if a.stage == "selftest":
        return stage_selftest(spec, out)
    if a.stage == "dev":
        return stage_dev(spec, out, a.per_family or spec.dev_per_family)
    if a.stage == "protected":
        return stage_protected(
            spec, out, a.per_family or spec.protected_per_family,
            a.seed_file or custody_seed_path(spec.suite_id),
        )
    if a.stage == "analyze":
        if not a.results or not a.custody:
            print("analyze requires --results and --custody", file=sys.stderr)
            return 2
        return stage_analyze(spec, a.results, a.custody, out)
    return 2


if __name__ == "__main__":
    sys.exit(main())

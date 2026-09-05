#!/usr/bin/env python3
"""SD70-V4 — recursive meta-discovery on a family the linear multiclass class provably does not contain (#308 R12).

Stages (exact, stdlib, no channel)
  selftest   containment theorem no-alarm (V3's linear family through the V4 code path: zero XOR-square certificates on
             every task), V4 tasks certified (≥ 1 certificate each), the planted checker mutant (ignore labels) is caught,
             gated-parent fidelity on a planted full-information surface, generator determinism.
  dev        the development-split PARENT-CEILING study: every V3 parent, the gated parent, F0 and F0_PLUS on 3 × 200
             fresh V4 tasks (public dev seeds), with V3's label-permutation and query-shuffle controls; frozen selection
             rule for the strongest generator-faithful parent; comparator = max(strongest, F0_PLUS) by dev accuracy (V3 §4.1).
  freeze     write the design JSON (seed commitment, pins, dev results digest) — once; refuses if it exists.
Model arms (F2 recursive meta-discovery and its ablations, gpt-5.5 via billy-old) are CHANNEL-DEPENDENT: they reuse
V3's `sd70v3_model_arm.py` / `sd70v3_channel.py` unchanged on V4 surfaces and are dispatched under a separate,
later authorization; nothing here contacts a model.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
V3 = HERE.parent / "sd70-v3"
for _p in (str(HERE), str(V3)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import sd70v3_generator as G3  # noqa: E402
import sd70v3_parents as P3  # noqa: E402
import sd70v3_stats as S  # noqa: E402
import sd70v4_generator as G4  # noqa: E402
import sd70v4_parents as P4  # noqa: E402
from sd70v4_containment import linear_containment_verdict, xor_square_certificates  # noqa: E402

STUDY_ID = "SD70-V4"
DESIGN_JSON = HERE / "SD70_V4_GATED_FAMILY_DESIGN_V1.json"
DEV_SEEDS, DEV_TASKS, TRAIN_EPISODES = 3, 200, 16
PINS = {"sd70-v3/sd70v3_generator.py": V3 / "sd70v3_generator.py", "sd70-v3/sd70v3_parents.py": V3 / "sd70v3_parents.py", "sd70-v3/sd70v3_stats.py": V3 / "sd70v3_stats.py",
        "sd70-v4/sd70v4_generator.py": HERE / "sd70v4_generator.py", "sd70-v4/sd70v4_parents.py": HERE / "sd70v4_parents.py", "sd70-v4/sd70v4_containment.py": HERE / "sd70v4_containment.py"}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def pins() -> dict:
    return {k: sha256_file(v) for k, v in PINS.items()}


def dev_seed(k: int) -> int:
    return int(hashlib.sha256(f"SD70-V4-DEV|{k}".encode()).hexdigest()[:15], 16)


def _write(p: Path, o: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, indent=2, sort_keys=True) + "\n")


def _policy(t: dict):
    w = (t["latent_weights"][0], t["latent_weights"][1]); g = tuple(t["latent_gate"])
    return lambda c: G4.gated_best_action(c, g, w)


# ---- selftest ----------------------------------------------------------------------------------

def stage_selftest(out: Path) -> int:
    rep: dict[str, Any] = {"study_id": STUDY_ID}
    # 1. no-alarm: V3's linear family -> zero certificates on every task (theorem)
    pub, priv = G4.build_suite(dev_seed(0), 40, TRAIN_EPISODES, "lin", linear_control=True)
    lin_certs = [t["xor_square_certificates"] for t in priv["tasks"]]
    rep["linear_control_zero_certificates"] = {"tasks": len(lin_certs), "max_certificates": max(lin_certs), "pass": max(lin_certs) == 0}
    # 1b. V3's own generator (not through the V4 path) also yields zero certificates
    pub3, priv3 = G3.build_suite(dev_seed(1), 40, TRAIN_EPISODES, "v3")
    v3_certs = [len(xor_square_certificates(lambda c, w=t["latent_weights"]: G3.best_action(c, w), len(t["latent_feature_tokens"]))) for t in priv3["tasks"]]
    rep["v3_generator_zero_certificates"] = {"tasks": len(v3_certs), "max_certificates": max(v3_certs), "pass": max(v3_certs) == 0}
    # 2. V4 tasks are certified
    pub4, priv4 = G4.build_suite(dev_seed(2), 40, TRAIN_EPISODES, "v4")
    v4_certs = [t["xor_square_certificates"] for t in priv4["tasks"]]
    recheck = all(linear_containment_verdict(_policy(t), len(t["latent_feature_tokens"]))["xor_square_certificates"] == t["xor_square_certificates"] for t in priv4["tasks"])
    rep["v4_tasks_certified"] = {"tasks": len(v4_certs), "min_certificates": min(v4_certs), "rejections": priv4["rejections"], "recheck_agrees": recheck, "pass": min(v4_certs) >= 1 and recheck}
    # 3. planted checker mutant (ignores labels) fires on linear tasks -> caught
    mutant = [len(xor_square_certificates(lambda c, w=t["latent_weights"]: G3.best_action(c, w), len(t["latent_feature_tokens"]), mutant_ignore_labels=True)) for t in priv3["tasks"]]
    rep["planted_mutant_caught"] = {"mutant_min_certificates_on_linear": min(mutant), "pass": min(mutant) >= 1}
    # 4. gated parent fidelity
    fid = P4.fidelity_selftest()
    # fidelity criterion = the held-out action (a gate other than the planted one can realise the same
    # 14-context labelling; gate identity is reported, not required)
    rep["gated_parent_fidelity"] = {**fid, "pass": bool(fid["gate_found"] is not None and fid["gated_pick_correct"])}
    # 5. determinism
    pub4b, _ = G4.build_suite(dev_seed(2), 40, TRAIN_EPISODES, "v4")
    rep["generator_deterministic"] = {"pass": json.dumps(pub4, sort_keys=True) == json.dumps(pub4b, sort_keys=True)}
    rep["pins"] = pins()
    rep["passed"] = all(v["pass"] for k, v in rep.items() if isinstance(v, dict) and "pass" in v)
    _write(out / "SD70_V4_SELFTEST_V1.json", rep)
    print(f"selftest {'PASS' if rep['passed'] else 'FAIL'}: " + ", ".join(f"{k}={v['pass']}" for k, v in rep.items() if isinstance(v, dict) and "pass" in v))
    return 0 if rep["passed"] else 1


# ---- development parent-ceiling study ---------------------------------------------------------

def stage_dev(out: Path, seeds: int = DEV_SEEDS, tasks: int = DEV_TASKS) -> int:
    arms = list(P4.PARENT_IDS_V4)
    correct = {a: [] for a in arms}; cfd = {a: [] for a in arms}; wall = {a: 0.0 for a in arms}
    ctrl = {a: {"LP": [], "QS": []} for a in arms}
    chance, certs, rejections = [], [], 0
    suites = []
    for k in range(seeds):
        seed = dev_seed(k)
        pub, priv = G4.build_suite(seed, tasks, TRAIN_EPISODES, f"dev{k}")
        suites.append((pub, priv)); rejections += priv["rejections"]
        oracle = {t["task_id"]: t for t in priv["tasks"]}
        for t in priv["tasks"]:
            chance.append(t["chance_level"]); certs.append(t["xor_square_certificates"])
        for task in pub["tasks"]:
            surf = G3.surface_for("COMMON", task, None)
            o = oracle[task["task_id"]]
            for a in arms:
                t0 = time.perf_counter(); pick, _ = P4.select(a, surf); wall[a] += time.perf_counter() - t0
                correct[a].append(pick == o["correct_action"]); cfd[a].append(pick in o["worst_actions"])
        for label, fn in (("LP", G3.label_permutation_controls), ("QS", G3.query_shuffle_controls)):
            cp, cv = fn(pub, priv, seed)
            co = {t["task_id"]: t for t in cv["tasks"]}
            for task in cp["tasks"]:
                surf = G3.surface_for("COMMON", task, None)
                for a in arms:
                    ctrl[a][label].append(P4.select(a, surf)[0] == co[task["task_id"]]["correct_action"])
    n = len(chance)
    summary = {a: {"exact_accuracy": sum(correct[a]) / n, "wilson95": S.wilson(sum(correct[a]), n)[1:], "critical_false_direction_rate": sum(cfd[a]) / n,
                   "control_LP_accuracy": sum(ctrl[a]["LP"]) / len(ctrl[a]["LP"]), "control_QS_accuracy": sum(ctrl[a]["QS"]) / len(ctrl[a]["QS"]), "wall_seconds_total": wall[a]} for a in arms}
    ranked = sorted(P4.GENERATOR_FAITHFUL_CANDIDATES_V4, key=lambda a: (-round(summary[a]["exact_accuracy"], 12), summary[a]["wall_seconds_total"]))
    strongest, second = ranked[0], ranked[1]
    linear_best = max(P3.GENERATOR_FAITHFUL_CANDIDATES, key=lambda a: summary[a]["exact_accuracy"])
    # federations (post-selection, development only)
    f0, f0p, f0_cfd, f0p_cfd = [], [], [], []
    for pub, priv in suites:
        oracle = {t["task_id"]: t for t in priv["tasks"]}
        for task in pub["tasks"]:
            surf = G3.surface_for("COMMON", task, None); o = oracle[task["task_id"]]
            a0, _ = P3.federation(surf, linear_best); a1, _ = P4.federation_plus(surf, strongest)
            f0.append(a0 == o["correct_action"]); f0p.append(a1 == o["correct_action"]); f0_cfd.append(a0 in o["worst_actions"]); f0p_cfd.append(a1 in o["worst_actions"])
    summary["F0_PARENT_FEDERATION"] = {"exact_accuracy": sum(f0) / n, "wilson95": S.wilson(sum(f0), n)[1:], "critical_false_direction_rate": sum(f0_cfd) / n, "strongest_member": linear_best, "members": list(P3.PARENT_IDS)}
    summary[P4.F0_PLUS] = {"exact_accuracy": sum(f0p) / n, "wilson95": S.wilson(sum(f0p), n)[1:], "critical_false_direction_rate": sum(f0p_cfd) / n, "strongest_member": strongest, "members": list(P4.PARENT_IDS_V4)}
    comparator = max([strongest, P4.F0_PLUS, "F0_PARENT_FEDERATION"], key=lambda a: round(summary[a]["exact_accuracy"], 12))
    gated_vs_linear = S.paired_difference(correct[P4.GATED_PARENT], correct[linear_best], bootstrap=2000)
    res = {"schema_version": "orion.v2.sd70-v4.development-results.v1", "study_id": STUDY_ID, "development_only": True, "protected_outcomes_inspected": False,
           "seeds": [{"seed_index": k, "seed_sha256": hashlib.sha256(str(dev_seed(k)).encode()).hexdigest(), "tasks": tasks} for k in range(seeds)], "task_total": n, "train_episodes": TRAIN_EPISODES,
           "generator_rejections": rejections, "certificates_per_task": {"min": min(certs), "mean": sum(certs) / n, "max": max(certs)}, "mean_chance_level": sum(chance) / n,
           "arms": summary, "generator_faithful_ranking": ranked, "strongest_generator_faithful_parent": strongest, "second_candidate": second,
           "strongest_linear_parent": linear_best, "gated_minus_strongest_linear_paired": gated_vs_linear,
           "comparator_rule": "max(strongest generator-faithful parent, F0_PLUS_FEDERATION, F0_PARENT_FEDERATION) by mean development exact accuracy (V3 §4.1 extended to the gated family)",
           "comparator": comparator, "pins": pins()}
    _write(out / "SD70_V4_DEVELOPMENT_RESULTS_V1.json", res)
    print(f"dev {n} tasks (rejections {rejections}; certificates/task min {min(certs)} mean {sum(certs)/n:.1f}); chance {sum(chance)/n:.3f}")
    for a in arms + ["F0_PARENT_FEDERATION", P4.F0_PLUS]:
        s = summary[a]; print(f"  {a:28s} acc {s['exact_accuracy']:.4f} [{s['wilson95'][0]:.3f},{s['wilson95'][1]:.3f}] cfd {s['critical_false_direction_rate']:.3f} LP {s['control_LP_accuracy']:.3f} QS {s['control_QS_accuracy']:.3f}")
    print(f"  strongest faithful: {strongest}; strongest linear: {linear_best}; gated − linear = {gated_vs_linear['point']:+.4f} [{gated_vs_linear['ci_low']:+.3f},{gated_vs_linear['ci_high']:+.3f}] (b={gated_vs_linear['b']}, c={gated_vs_linear['c']}); comparator = {comparator}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("selftest", "dev"))
    ap.add_argument("--out", type=Path, default=HERE / "results")
    ap.add_argument("--seeds", type=int, default=DEV_SEEDS); ap.add_argument("--tasks", type=int, default=DEV_TASKS)
    a = ap.parse_args(argv)
    if a.stage == "selftest":
        return stage_selftest(a.out)
    return stage_dev(a.out, a.seeds, a.tasks)


if __name__ == "__main__":
    sys.exit(main())

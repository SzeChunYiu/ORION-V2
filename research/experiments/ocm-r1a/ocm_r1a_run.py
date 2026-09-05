#!/usr/bin/env python3
"""OCM-R1A — controller versus B5 federation on the registered non-rectangular class VSW(SINGLETONS_m).

Revival backlog #308 row R1a.  Attributed stage: **problem class** (every registered ME-X class is
rectangular / known-answer).  Lever: the lane-200 revival registered a natural non-decomposable
instance, `VSW(SINGLETONS_5)` (interaction term I = 1, parent-owned: Angluin 1988 subset queries).
This study puts the joint controller and the sequential parent federation on that class, exactly.

Arms (all exact, stdlib, no LLM)
  M_JOINT_CONTROLLER        the joint learner under the mixed query protocol {membership, liveness}:
                            the explicit optimal decision tree (reference solver A), walked on every
                            world.  This IS the general-dimension learner of the mixed protocol.
  B5_SEQUENTIAL_FEDERATION  the sequential product of two parents (trace-learner for behaviour,
                            then provenance/INDEX for warrant, or the symmetric order): the better
                            of the B-first / Z-first composite strategies by worst case
                            (registered tie rule: B-first).  Each composite strategy is an optimal
                            weighted quotient tree followed by an optimal fibre tree, walked per world.
  B5_ADAPTIVE_PARENT        the adaptive parent (exact learning under the mixed protocol,
                            Balcázar–Castro–Guijarro 2001) CONTAINS the joint learner: reported as an
                            identity with M, never as a comparator (disclosed, design §3).
  C_RANDOM_ADAPTIVE         a random adaptive learner (uniformly random splitting query until the
                            world is identified), REPS repetitions per world under the committed seed.
  LB_COUNTING               ceil(log2 |worlds|).

Endpoints: worst-case query count (primary, exact, no seed); per-world mean and the paired
per-world difference M − B5 with an exact two-sided sign test (secondary).

Stages
  selftest    small classes, no seed, no authorization; planted checker mutation must fire.
  protected   all registered classes incl. the SINGLETONS_6 attempt; refuses without
              PROTECTED_RUN_AUTHORIZATION.json (ME-X shape) and the custody seed hashing to the
              frozen commitment.  Exit 3 / 4 on refusal, 2 on CANNOT_CHECK.
  analyze     gates + route from a results file.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import random
import signal
import sys
import time
from pathlib import Path
from types import ModuleType

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REFERENCE = ROOT / "research" / "orion-machine" / "reference" / "ocm_nonrectangular_class_exact.py"
REGISTERED_RESULTS = ROOT / "research" / "orion-machine" / "results" / "OCM_NONRECTANGULAR_CLASS_EXACT_RESULTS_V1.json"
DESIGN_JSON = HERE / "OCM_R1A_CONTROLLER_VS_FEDERATION_VSW_DESIGN_V1.json"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
AUTH_USED = HERE / "PROTECTED_RUN_AUTHORIZATION_USED_V1.json"
DEFAULT_SEED_FILE = Path(os.environ.get("OCM_R1A_PROTECTED_SEED_FILE", str(Path.home() / ".orion-custody" / "ocm-r1a" / "PROTECTED_SEED_V1.txt")))
RESULTS_DIR = HERE / "results"

STUDY_ID = "OCM-R1A"
SCHEMA_RESULTS = "orion.v2.ocm-r1a.controller-vs-federation-results.v1"
SCHEMA_ANALYSIS = "orion.v2.ocm-r1a.controller-vs-federation-analysis.v1"

M_ARM = "M_JOINT_CONTROLLER"
B5_ARM = "B5_SEQUENTIAL_FEDERATION"
ADAPTIVE_ARM = "B5_ADAPTIVE_PARENT"
RANDOM_ARM = "C_RANDOM_ADAPTIVE"
RANDOM_REPS = 20

# Registered classes, in the order they are run.  ``expected_I`` is the pre-registered
# interaction term where the lane-200 checker certified it; None = attempt (pre-registered as
# CANNOT_CHECK-on-time-budget-permitted).
CLASSES: tuple[tuple[str, dict], ...] = (
    ("LINEAR_F2^2", {"role": "rectangular no-alarm control (affine): tie expected", "expected_I": 0}),
    ("MONO_CONJ_2", {"role": "non-rectangular, decomposable: tie expected", "expected_I": 0}),
    ("LTF_2", {"role": "non-rectangular, decomposable: tie expected", "expected_I": 0}),
    ("SINGLETONS_4", {"role": "non-rectangular, decomposable: tie expected", "expected_I": 0}),
    ("SINGLETONS_5", {"role": "REGISTERED natural non-decomposable instance: controller ahead by I = 1", "expected_I": 1}),
    ("SINGLETONS_6", {"role": "pre-registered attempt (m = 6): expectation I >= 1; CANNOT_CHECK on the time budget is a permitted outcome", "expected_I": None}),
)
SELFTEST_CLASSES = ("LINEAR_F2^2", "MONO_CONJ_2", "SINGLETONS_4", "SINGLETONS_5")
TIME_BUDGET_S = {"SINGLETONS_6": int(os.environ.get("OCM_R1A_S6_BUDGET_S", "72000"))}

OPERATOR_INSTRUCTION_VERBATIM = "run all the computation tasks.. finish all the researxh asap"
OPERATOR_INSTRUCTION_SOURCE = "operator, in chat, 2026-09-02; reaffirmed 2026-09-04 'i sign off everything'"


class CannotCheck(RuntimeError):
    pass


def _load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise CannotCheck(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def reference() -> ModuleType:
    return _load("ocm_nonrectangular_class_exact", REFERENCE)


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def canonical_json(o) -> str:
    return json.dumps(o, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


# ---- classes ------------------------------------------------------------------------------

def build_class(name: str, R: ModuleType):
    rcl = R._load("rcl_model", R.RCL_MODEL)
    if name == "SINGLETONS_5":
        return R.vsw_class(name, R.singletons(5), rcl)
    if name == "SINGLETONS_6":
        return R.vsw_class(name, R.singletons(6), rcl)
    fams = R.named_families_on_4_points()
    if name not in fams:
        raise CannotCheck(f"unregistered class {name}")
    return R.vsw_class(name, fams[name], rcl)


# ---- per-world walks ------------------------------------------------------------------------

def walk(tree, queries, i: int) -> int:
    """Depth at which the explicit tree identifies world i (number of queries asked)."""
    node, depth = tree, 0
    while "leaf" not in node:
        depth += 1
        node = node[str(queries[node["q"]][1][i])]
    return depth


def joint_per_world(qc, R) -> tuple[int, list[int], dict]:
    allq = list(qc.b_queries) + list(qc.z_queries)
    ident = tuple(range(qc.n))
    d, tree = R.solve_weighted(qc.n, allq, ident)
    if d is None or tree is None:
        raise CannotCheck(f"{qc.name}: worlds not identifiable from the registered queries")
    per = [walk(tree, allq, i) for i in range(qc.n)]
    if max(per) != d:
        raise AssertionError(f"{qc.name}: walked worst case {max(per)} != solver cost {d}")
    cross = None
    if qc.n <= R.CROSS_CHECK_MAX_WORLDS:
        cross = R.solve_weighted_b(qc.n, allq, ident)
        if cross != d:
            raise AssertionError(f"{qc.name}: solver B disagrees on D_joint ({cross} vs {d})")
    return d, per, {"solver_b_cross_check": cross, "counting_lower_bound": math.ceil(math.log2(qc.n))}


def sequential_per_world(qc, R, first: str) -> tuple[int, list[int], dict]:
    """The composite strategy that learns factor ``first`` completely, then the fibre — walked per world.
    Mirrors the reference ``_sequential`` (which certifies the cost) but returns every world's count."""
    if first == "B":
        values, fq, oq = qc.B, qc.b_queries, qc.z_queries
    else:
        values, fq, oq = qc.Z, qc.z_queries, qc.b_queries
    qvals, qq, fibres = R._quotient(values, fq)
    fibre_cost: dict = {}
    fibre_trees: dict = {}
    for v, idx in fibres.items():
        sub = R._restrict(oq, idx)
        ident = tuple(range(len(idx)))
        c, t = R.solve_weighted(len(idx), sub, ident)
        if c is None or t is None:
            raise CannotCheck(f"{qc.name}: a fibre of {first} is not identifiable from the other factor's queries")
        fibre_cost[v] = c
        fibre_trees[v] = (t, sub, idx)
    m = len(qvals)
    cost, tree = R.solve_weighted(m, qq, qvals, fibre_cost)
    if cost is None or tree is None:
        raise CannotCheck(f"{qc.name}: factor {first} is not identifiable from its own queries")
    per: list[int] = []
    for i in range(qc.n):
        v = values[i]
        node, depth = tree, 0
        while "leaf" not in node:
            depth += 1
            node = node[str(fq[node["q"]][1][i])]
        if node["leaf"] != v:
            raise AssertionError(f"{qc.name}: {first}-tree misidentifies a factor value")
        t, sub, idx = fibre_trees[v]
        per.append(depth + walk(t, sub, idx.index(i)))
    if max(per) != cost:
        raise AssertionError(f"{qc.name}: walked {first}-first worst case {max(per)} != solver cost {cost}")
    return cost, per, {"factor_values": m, "worst_fibre": max(fibre_cost.values())}


def random_adaptive_per_world(qc, rng: random.Random, reps: int) -> list[float]:
    allq = list(qc.b_queries) + list(qc.z_queries)
    out: list[float] = []
    for i in range(qc.n):
        total = 0
        for _ in range(reps):
            cand = set(range(qc.n))
            asked = 0
            while len(cand) > 1:
                splitting = [q for q in range(len(allq)) if len({allq[q][1][j] for j in cand}) > 1]
                q = rng.choice(splitting)
                asked += 1
                a = allq[q][1][i]
                cand = {j for j in cand if allq[q][1][j] == a}
            total += asked
        out.append(total / reps)
    return out


# ---- study --------------------------------------------------------------------------------

def _alarm(_sig, _frm):
    raise CannotCheck("time budget exhausted")


def run_class(name: str, R, rng: random.Random | None, budget_s: int | None) -> dict:
    t0 = time.perf_counter()
    if budget_s:
        signal.signal(signal.SIGALRM, _alarm)
        signal.alarm(budget_s)
    try:
        qc, meta = build_class(name, R)
        d, m_per, joint_meta = joint_per_world(qc, R)
        bcost, b_per, b_meta = sequential_per_world(qc, R, "B")
        zcost, z_per, z_meta = sequential_per_world(qc, R, "Z")
        first = "B" if bcost <= zcost else "Z"                      # registered tie rule: B-first
        fed_per = b_per if first == "B" else z_per
        fed_cost = min(bcost, zcost)
        rnd = random_adaptive_per_world(qc, rng, RANDOM_REPS) if rng is not None else None
    except CannotCheck as exc:
        return {"class": name, "status": "CANNOT_CHECK", "reason": str(exc), "wall_s": time.perf_counter() - t0}
    finally:
        if budget_s:
            signal.alarm(0)
    diffs = [b - a for a, b in zip(m_per, fed_per)]           # federation − controller, per world (>= 0 expected)
    pos = sum(1 for x in diffs if x > 0)
    neg = sum(1 for x in diffs if x < 0)
    return {
        "class": name, "status": "OK", "meta": meta, "worlds": qc.n, "wall_s": time.perf_counter() - t0,
        "arms": {
            M_ARM: {"worst_case": d, "mean": sum(m_per) / qc.n, "per_world": m_per, **joint_meta},
            B5_ARM: {"worst_case": fed_cost, "mean": sum(fed_per) / qc.n, "per_world": fed_per, "order": first,
                     "B_first": {"worst_case": bcost, "mean": sum(b_per) / qc.n, **b_meta},
                     "Z_first": {"worst_case": zcost, "mean": sum(z_per) / qc.n, **z_meta}},
            ADAPTIVE_ARM: {"worst_case": d, "identity_with": M_ARM, "note": "the adaptive parent contains the joint learner; identity, not evidence"},
            RANDOM_ARM: ({"worst_case": max(rnd), "mean": sum(rnd) / qc.n, "reps": RANDOM_REPS} if rnd is not None else {"status": "NOT_RUN_NO_SEED"}),
            "LB_COUNTING": {"worst_case": joint_meta["counting_lower_bound"]},
        },
        "interaction_term": fed_cost - d,
        "paired": {"n": qc.n, "federation_minus_controller_mean": sum(diffs) / qc.n, "worlds_controller_better": pos,
                   "worlds_federation_better": neg, "worlds_tied": qc.n - pos - neg,
                   "sign_test_two_sided_p": exact_sign_p(pos, neg)},
    }


def exact_sign_p(pos: int, neg: int) -> float:
    n = pos + neg
    if n == 0:
        return 1.0
    k = min(pos, neg)
    tail = sum(math.comb(n, j) for j in range(0, k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def planted_mutation(R) -> dict:
    """Checker mutation M1 (the first-draft sequential-cost formula D_first + max fibre) must be
    caught: on LTF_2 it overstates the Z-first cost by one against the simulated strategy."""
    rcl = R._load("rcl_model", R.RCL_MODEL)
    qc, _ = R.vsw_class("LTF_2", R.named_families_on_4_points()["LTF_2"], rcl)
    formula = R._sequential(qc, "Z", formula=True)["cost"]
    exact = R._sequential(qc, "Z")["cost"]
    return {"mutation": "M1_sequential_cost_formula", "formula_cost": formula, "exact_cost": exact, "fired": formula != exact}


def run_study(class_names, seed: str | None, label: str) -> dict:
    R = reference()
    rng = random.Random(seed) if seed is not None else None
    rows = []
    for name in class_names:
        rows.append(run_class(name, R, rng, TIME_BUDGET_S.get(name)))
        print(f"  {name}: {rows[-1]['status']} ({rows[-1]['wall_s']:.1f}s)" + (f" I={rows[-1]['interaction_term']}" if rows[-1]["status"] == "OK" else f" {rows[-1].get('reason')}"), flush=True)
    return {"schema_version": SCHEMA_RESULTS, "study_id": STUDY_ID, "label": label, "reference_sha256": sha256_file(REFERENCE),
            "design_sha256": sha256_file(DESIGN_JSON) if DESIGN_JSON.exists() else None, "interpreter": sys.version.split()[0],
            "classes": rows, "planted_mutation": planted_mutation(R), "seed_used": seed is not None}


# ---- gates / route --------------------------------------------------------------------------

def gates(res: dict) -> dict:
    by = {r["class"]: r for r in res["classes"]}
    reg = json.loads(REGISTERED_RESULTS.read_text()) if REGISTERED_RESULTS.exists() else {}
    s5reg = (reg.get("D_registered_natural_nondecomposable_instance") or {}).get("SINGLETONS_5") or {}
    g: dict = {}
    s5 = by.get("SINGLETONS_5")
    ok5 = bool(s5 and s5["status"] == "OK")
    g["G0a_KNOWN_ANSWER"] = {"pass": bool(ok5 and s5reg and s5["arms"][M_ARM]["worst_case"] == s5reg.get("D_joint")
                                          and s5["arms"][B5_ARM]["B_first"]["worst_case"] == (s5reg.get("B_first") or {}).get("cost")
                                          and s5["arms"][B5_ARM]["Z_first"]["worst_case"] == (s5reg.get("Z_first") or {}).get("cost")),
                             "registered": {k: (s5reg.get(k) if k == "D_joint" else (s5reg.get(k) or {}).get("cost")) for k in ("D_joint", "B_first", "Z_first")},
                             "observed": ({"D_joint": s5["arms"][M_ARM]["worst_case"], "B_first": s5["arms"][B5_ARM]["B_first"]["worst_case"], "Z_first": s5["arms"][B5_ARM]["Z_first"]["worst_case"]} if ok5 else None)}
    small = [r for r in res["classes"] if r["status"] == "OK" and r["worlds"] <= 64]
    g["G0b_SOLVERS_AGREE"] = {"pass": all(r["arms"][M_ARM]["solver_b_cross_check"] == r["arms"][M_ARM]["worst_case"] for r in small), "classes_cross_checked": [r["class"] for r in small]}
    g["G0c_PLANTED_MUTATION_FIRES"] = {"pass": bool(res["planted_mutation"]["fired"]), **res["planted_mutation"]}
    ties = [r for r in res["classes"] if r["status"] == "OK" and dict(CLASSES)[r["class"]]["expected_I"] == 0]
    g["G0d_NO_ALARM_ON_DECOMPOSABLE"] = {"pass": all(r["interaction_term"] == 0 for r in ties), "classes": {r["class"]: r["interaction_term"] for r in ties}}
    g["G1_CONTROLLER_BEATS_SEQUENTIAL_ON_REGISTERED_INSTANCE"] = {"pass": bool(ok5 and s5["interaction_term"] >= 1), "interaction_term": s5["interaction_term"] if ok5 else None,
                                                                   "paired": s5["paired"] if ok5 else None}
    g["G2_PARENT_OWNED_IDENTITY"] = {"pass": all(r["arms"][ADAPTIVE_ARM]["worst_case"] == r["arms"][M_ARM]["worst_case"] for r in res["classes"] if r["status"] == "OK"),
                                     "note": "identity by containment (adaptive parent ⊇ joint learner); disclosed, never a comparator"}
    s6 = by.get("SINGLETONS_6")
    g["G3_SINGLETONS_6_ATTEMPT"] = {"status": (s6 or {}).get("status", "NOT_RUN"), "interaction_term": (s6 or {}).get("interaction_term"), "reason": (s6 or {}).get("reason"),
                                    "pass": None, "note": "pre-registered attempt; CANNOT_CHECK on the time budget is a permitted outcome and is not a negative"}
    g["G4_RANDOM_CONTROL_ABOVE_CONTROLLER"] = {"pass": all(r["arms"][RANDOM_ARM].get("mean", 0) >= r["arms"][M_ARM]["mean"] for r in res["classes"] if r["status"] == "OK" and "mean" in r["arms"][RANDOM_ARM])}
    hard = all(g[k]["pass"] for k in ("G0a_KNOWN_ANSWER", "G0b_SOLVERS_AGREE", "G0c_PLANTED_MUTATION_FIRES", "G0d_NO_ALARM_ON_DECOMPOSABLE", "G2_PARENT_OWNED_IDENTITY"))
    if not hard:
        route = "LANE_DEFECT"
    elif g["G1_CONTROLLER_BEATS_SEQUENTIAL_ON_REGISTERED_INSTANCE"]["pass"]:
        route = "PARENT_OWNED__CONTROLLER_BEATS_SEQUENTIAL_FEDERATION_BY_INTERACTION_TERM"
    else:
        route = "PARENT_SUFFICIENT__SEQUENTIAL_TIE (CORRECTED against the lane-200 registration)"
    g["ROUTE"] = {"route": route, "reading": "the controller beats the SEQUENTIAL parent product by exactly the interaction term and ties the ADAPTIVE parent by containment: parent-owned, no residual against the strongest faithful parent"}
    return g


def render_md(a: dict) -> str:
    L = [f"# {STUDY_ID} — {a['label']} analysis", "", f"Route: **{a['gates']['ROUTE']['route']}**", "", "| class | worlds | M worst | B5 worst (order) | I | M mean | B5 mean | random mean | LB | worlds M<B5 / B5<M / tie | sign p |", "|---|---:|---:|---|---:|---:|---:|---:|---:|---|---:|"]
    for r in a["classes"]:
        if r["status"] != "OK":
            L.append(f"| {r['class']} | – | {r['status']}: {r.get('reason')} | | | | | | | | |")
            continue
        A = r["arms"]
        L.append(f"| {r['class']} | {r['worlds']} | {A[M_ARM]['worst_case']} | {A[B5_ARM]['worst_case']} ({A[B5_ARM]['order']}-first) | {r['interaction_term']} | {A[M_ARM]['mean']:.3f} | {A[B5_ARM]['mean']:.3f} | {A[RANDOM_ARM].get('mean', float('nan')):.3f} | {A['LB_COUNTING']['worst_case']} | {r['paired']['worlds_controller_better']} / {r['paired']['worlds_federation_better']} / {r['paired']['worlds_tied']} | {r['paired']['sign_test_two_sided_p']:.3g} |")
    L += ["", "| gate | pass | detail |", "|---|---|---|"]
    for k, v in a["gates"].items():
        if k == "ROUTE":
            continue
        L.append(f"| {k} | {v.get('pass')} | {json.dumps({kk: vv for kk, vv in v.items() if kk not in ('pass', 'paired')}, default=str)[:300]} |")
    L += ["", "Authority: grants nothing — no field status, no novelty, no residual claim. `NO NOVELTY OR BREAKTHROUGH CLAIM`."]
    return "\n".join(L) + "\n"


# ---- stages -------------------------------------------------------------------------------

def stage_selftest(out: Path) -> int:
    res = run_study(SELFTEST_CLASSES, None, "SELFTEST")
    res["classes"] = [r for r in res["classes"]]
    g = gates(res)
    ok = g["G0a_KNOWN_ANSWER"]["pass"] and g["G0c_PLANTED_MUTATION_FIRES"]["pass"] and g["G0d_NO_ALARM_ON_DECOMPOSABLE"]["pass"] and g["G1_CONTROLLER_BEATS_SEQUENTIAL_ON_REGISTERED_INSTANCE"]["pass"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "OCM_R1A_SELFTEST_REPORT_V1.json").write_text(canonical_json({"passed": ok, "gates": g, "results": res}))
    print(f"selftest {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def stage_protected(out: Path, seed_file: Path) -> int:
    if not AUTH_FILE.exists():
        print(f"REFUSED: {AUTH_FILE.name} absent — protected run not authorized", file=sys.stderr); return 3
    auth = json.loads(AUTH_FILE.read_text())
    if auth.get("human_written") is not True or len(str(auth.get("human_written_token", ""))) < 16:
        print("REFUSED: authorization requires human_written=true and a token >= 16 chars", file=sys.stderr); return 3
    if auth.get("acknowledged_design_sha256") != sha256_file(DESIGN_JSON):
        print("REFUSED: acknowledged_design_sha256 does not match the frozen design JSON", file=sys.stderr); return 3
    if not seed_file.exists():
        print(f"REFUSED: custody seed absent ({seed_file})", file=sys.stderr); return 4
    seed = seed_file.read_bytes().strip()
    commitment = json.loads(DESIGN_JSON.read_text())["seed_commitment"]["protected_seed_sha256"]
    if hashlib.sha256(seed).hexdigest() != commitment:
        print("REFUSED: custody seed does not match the frozen commitment", file=sys.stderr); return 4
    res = run_study([c for c, _ in CLASSES], seed.decode(), "PROTECTED")
    res["revealed_protected_seed"] = seed.decode()
    out.mkdir(parents=True, exist_ok=True)
    rp = out / "OCM_R1A_PROTECTED_RESULTS_V1.json"
    rp.write_text(canonical_json(res))
    auth["consumed"] = True; auth["archive_after_use"] = True; auth["revealed_protected_seed"] = seed.decode()
    AUTH_USED.write_text(canonical_json(auth)); AUTH_FILE.unlink()
    print(f"protected results {rp} sha256 {sha256_file(rp)}")
    return stage_analyze(rp, out)


def stage_analyze(rp: Path, out: Path) -> int:
    res = json.loads(rp.read_text())
    a = {"schema_version": SCHEMA_ANALYSIS, "study_id": STUDY_ID, "label": res["label"], "results_sha256": sha256_file(rp), "classes": res["classes"], "gates": gates(res)}
    out.mkdir(parents=True, exist_ok=True)
    (out / f"OCM_R1A_{res['label']}_ANALYSIS_V1.json").write_text(canonical_json(a))
    (out / f"OCM_R1A_{res['label']}_ANALYSIS_V1.md").write_text(render_md(a))
    print(f"{res['label']} route: {a['gates']['ROUTE']['route']}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("selftest", "protected", "analyze"))
    ap.add_argument("--out", type=Path, default=RESULTS_DIR)
    ap.add_argument("--seed-file", type=Path, default=DEFAULT_SEED_FILE)
    ap.add_argument("--results", type=Path)
    a = ap.parse_args(argv)
    try:
        if a.stage == "selftest":
            return stage_selftest(a.out)
        if a.stage == "protected":
            return stage_protected(a.out, a.seed_file)
        return stage_analyze(a.results or (a.out / "OCM_R1A_PROTECTED_RESULTS_V1.json"), a.out)
    except CannotCheck as exc:
        print(f"CANNOT_CHECK: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

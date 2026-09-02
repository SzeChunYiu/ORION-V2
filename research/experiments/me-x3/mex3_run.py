#!/usr/bin/env python3
"""ME-X3 exact formal-mathematics study runner (frozen with design V1).

Stages
  selftest   parent fidelity, oracle self-agreement, hand-authored known-answer
             fixtures, null calibration (G0).
  dev        DEVELOPMENT split (public seed). Results are labelled DEVELOPMENT
             and are never protected evidence; the federation's stage order and
             budget slices were fixed here.
  protected  PROTECTED split. Refuses to run unless
             PROTECTED_RUN_AUTHORIZATION.json is present next to this script AND
             the custody seed file's sha256 equals the commitment in the design.
  analyze    Score a results file against its custody file: the section 9 outcome
             vector, gates G0-G4, and the pre-registered route.

Design: ME_X3_FORMAL_MATHEMATICS_EXACT_STUDY_DESIGN_V1.{md,json}
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from mex3_arms import (  # noqa: E402
    ArmState, B5_ARM, LADDER, Ledger, M_ARM, arm_specs,
)
from mex3_generator import (  # noqa: E402
    ORACLE_EXPANSIONS, ORACLE_MODEL_SIZE, ORACLE_WORD_LEN, TASK_BUDGET, generate_split,
)
from mex3_model import (  # noqa: E402
    ACTIONS, DRIFT_VERDICTS, FAMILIES, FIDELITY_VERDICTS, Presentation, Statement,
    TERMINALS, Task, canonical_json,
)
from mex3_oracle import check_countermodel, check_derivation  # noqa: E402
from mex3_parents import fidelity_selftests  # noqa: E402

SCHEMA_RESULTS = "orion.v2.me-x3.exact-study-results.v1"
SCHEMA_ANALYSIS = "orion.v2.me-x3.exact-study-analysis.v1"
DESIGN_JSON = HERE / "ME_X3_FORMAL_MATHEMATICS_EXACT_STUDY_DESIGN_V1.json"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
DEV_SEED = "ME-X3-DEV-20260902"
DEV_PER_FAMILY = 3
PROTECTED_PER_FAMILY = 60
DEFAULT_SEED_FILE = Path(os.environ.get(
    "MEX3_PROTECTED_SEED_FILE", str(Path.home() / ".orion-custody/me-x3/PROTECTED_SEED_V1.txt")))

# Families on which no high-level change is warranted: the anti-conservatism and
# false-escalation controls (G2).
NO_ESCALATION_FAMILIES = ("F1_DIRECT_SEARCH", "F4_DECEPTIVE_CHANGE")
# The ablation that must degrade each family's behaviour if the mechanism is real
# (G3). Two families are deliberately NOT gated, for reasons that are structural
# rather than convenient, and both are recorded in the design:
#   F1 is a pure control family -- nothing should escalate on it, so no omission
#      can break it; it is gated instead by G2's false-change rate.
#   F8's held-out target admits independent re-invention as well as reuse, so the
#      transfer ablation cannot degrade it by construction.
# Gating either of them would guarantee a failing row and tell us nothing.
ABLATION_FOR_FAMILY = {
    "F1_DIRECT_SEARCH": None,
    "F2_MISSING_LEMMA": "M_MINUS_LEMMA_LEVEL",
    "F3_REPRESENTATION_CHANGE": "M_NEVER_CHANGE_REPRESENTATION",
    "F4_DECEPTIVE_CHANGE": "M_MINUS_FALSE_CHANGE_PENALTY",
    "F5_PROBE_OR_COUNTEREXAMPLE_NEEDED": "M_MINUS_COUNTEREXAMPLE_PROBE",
    "F6_UNDERDETERMINED_OR_CANNOT_CHECK": "M_MINUS_UNRESOLVED_TERMINAL",
    "F7_SPECIFICATION_MISMATCH": "M_MINUS_SPECIFICATION_PRESERVATION",
    "F8_TRANSFER": None,
}
NOT_GATED_REASON = {
    "F1_DIRECT_SEARCH": "control family: nothing should escalate, so no omission can "
                        "break it; gated by G2 instead",
    "F8_TRANSFER": "the held-out target admits independent re-invention as well as "
                   "reuse, so the transfer ablation cannot degrade it by construction",
}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


# ------------------------------------------------------------------- running ---

def run_split(pairs, label: str, split_seed_public):
    specs = arm_specs()
    results = {"schema_version": SCHEMA_RESULTS, "label": label,
               "split_seed": split_seed_public, "arms": [s.name for s in specs],
               "instances": []}
    custody = {"schema_version": SCHEMA_RESULTS + ".expected-custody", "label": label,
               "instances": []}
    # F8 pairs share one arm state so a source's invention can reach its target.
    states = {s.name: {} for s in specs}
    for task, verdict in pairs:
        rec = {"task_id": task.task_id, "family": task.family, "seed": task.seed,
               "formal_pid": task.formal_pid, "has_alt": task.alt is not None,
               "n_library": len(task.library), "arms": {}}
        group = task.transfer_of or task.task_id
        for spec in specs:
            st = states[spec.name].setdefault(group, ArmState(spec.keep_transfer))
            led = Ledger(task.budget)
            ans = spec.fn(task, led, st)
            rec["arms"][spec.name] = ans.as_dict() | {"cost": led.as_dict()}
        results["instances"].append(rec)
        custody["instances"].append({"task_id": task.task_id, "family": task.family,
                                     "expected": verdict, "task": task.view(),
                                     "hidden": task.hidden})
    return results, custody


# ------------------------------------------------------------------ scoring ---

def _witness_ok(task_view: dict, ans: dict, expected: dict) -> bool:
    """A claimed verdict counts only if it carries a witness that re-checks."""
    base = Presentation("P0", task_view["base"]["alphabet"],
                        tuple((tuple(u), tuple(v)) for u, v in task_view["base"]["axioms"]))
    alt = None
    if task_view["alt"]:
        alt = Presentation("P1", task_view["alt"]["alphabet"],
                           tuple((tuple(u), tuple(v)) for u, v in task_view["alt"]["axioms"]))
    formal = Statement(tuple(task_view["formal"]["lhs"]), tuple(task_view["formal"]["rhs"]))
    if ans["validity"] == "VERIFIED":
        path = tuple(tuple(w) for w in ans["derivation"])
        if not path:
            return False
        pid = ans.get("derivation_pid") or "P0"
        if pid.startswith("P1") and alt is not None:
            # A representation change earns credit only if the chain proves the
            # TRANSLATION of the presented statement. Checking the chain against
            # its own endpoints would test axiom-soundness alone and let any valid
            # alt-presentation derivation collect F3 credit.
            from mex3_generator import translate
            g = base.alphabet
            d = tuple(task_view.get("alt_defining_word") or ())
            if task_view["formal_pid"] == "P1":
                target = formal
            elif not d:
                return False
            else:
                target = Statement(translate(formal.lhs, d, g), translate(formal.rhs, d, g))
            ok, _ = check_derivation(path, target, alt.axioms,
                                     task_view["budget"]["max_word_len"])
            return ok
        aug = base
        lem = ans.get("invented_lemma")
        if lem:
            aug = Presentation("P0+L", base.alphabet,
                               tuple(sorted(set(base.axioms + ((tuple(lem[0]), tuple(lem[1])),)))))
        ok, _ = check_derivation(path, formal, aug.axioms, task_view["budget"]["max_word_len"])
        return ok
    if ans["validity"] == "REFUTED":
        cm = ans.get("countermodel")
        if not cm:
            return False
        m = tuple(tuple(f) for f in cm["model"])
        pres = alt if (task_view["formal_pid"] == "P1" and alt) else base
        ok, _ = check_countermodel(m, cm["size"], pres, formal)
        return ok
    return True


def _blank() -> dict:
    return {"n": 0, "validity": 0, "fidelity": 0, "action": 0, "terminal": 0,
            "joint": 0, "witness": 0, "false_change": 0, "false_defer": 0,
            "missed_escalation": 0, "drift_missed": 0, "drift_n": 0,
            "false_drift_alarm": 0, "faithful_n": 0, "expansions": 0,
            "module_calls": 0, "reuse_solved": 0, "reuse_n": 0}


def score(results: dict, custody: dict) -> dict:
    exp = {c["task_id"]: c for c in custody["instances"]}
    arms = results["arms"]
    per_arm: dict[str, dict] = {}
    for arm in arms:
        fams: dict[str, dict] = {}
        subs: dict[str, dict] = {}
        joint_flags: dict[str, bool] = {}
        for inst in results["instances"]:
            e = exp[inst["task_id"]]; v = e["expected"]; a = inst["arms"][arm]
            fam = inst["family"]
            f = fams.setdefault(fam, _blank())
            sub = e["hidden"].get("f7_subtype")
            g_sub = subs.setdefault(sub, _blank()) if sub else None
            f["n"] += 1
            if g_sub is not None:
                g_sub["n"] += 1
            wok = _witness_ok(e["task"], a, v)
            f["witness"] += wok
            val = (a["validity"] == v["validity"]) and wok
            fid = a["fidelity"] == v["fidelity"]
            act = a["action"] == v["minimal_action"]
            term = a["terminal"] == v["terminal"]
            f["validity"] += val; f["fidelity"] += fid; f["action"] += act
            f["terminal"] += term
            j = val and fid and act
            f["joint"] += j
            if g_sub is not None:
                g_sub["witness"] += wok; g_sub["validity"] += val
                g_sub["fidelity"] += fid; g_sub["action"] += act
                g_sub["terminal"] += term; g_sub["joint"] += j
                if v["fidelity"] in DRIFT_VERDICTS:
                    g_sub["drift_n"] += 1
                    if a["fidelity"] == "FAITHFUL":
                        g_sub["drift_missed"] += 1
                if v["fidelity"] == "FAITHFUL":
                    g_sub["faithful_n"] += 1
                    if a["fidelity"] != "FAITHFUL":
                        g_sub["false_drift_alarm"] += 1
            joint_flags[inst["task_id"]] = bool(j)
            if v["level"] not in ("L4_REPRESENTATION",) and a["action"] == "CHANGE_REPRESENTATION":
                f["false_change"] += 1
            if v["minimal_action"] != "DEFER_CANNOT_IDENTIFY" and \
                    a["action"] == "DEFER_CANNOT_IDENTIFY":
                f["false_defer"] += 1
            if v["level"] in ("L2_RETRIEVE", "L3_INVENT", "L4_REPRESENTATION") and \
                    a["action"] == "CONTINUE_DIRECT_PROOF_SEARCH":
                f["missed_escalation"] += 1
            if v["fidelity"] in DRIFT_VERDICTS:
                f["drift_n"] += 1
                if a["fidelity"] == "FAITHFUL":
                    f["drift_missed"] += 1
            if v["fidelity"] == "FAITHFUL":
                f["faithful_n"] += 1
                if a["fidelity"] != "FAITHFUL":
                    f["false_drift_alarm"] += 1
            if e["hidden"].get("transfer_role") == "TARGET":
                f["reuse_n"] += 1
                f["reuse_solved"] += (a["validity"] == "VERIFIED" and wok)
            f["expansions"] += a["cost"]["expansions"]
            f["module_calls"] += a["cost"]["module_calls"]
        tot = {k: sum(x[k] for x in fams.values()) for k in
               ("n", "validity", "fidelity", "action", "terminal", "joint", "witness",
                "false_change", "false_defer", "missed_escalation", "drift_missed",
                "drift_n", "false_drift_alarm", "faithful_n", "expansions",
                "module_calls", "reuse_solved", "reuse_n")}
        per_arm[arm] = {
            "per_family": {k: _rates(x) for k, x in sorted(fams.items())},
            "per_f7_subtype": {k: _rates(x) for k, x in sorted(subs.items())},
            "pooled": _rates(tot), "joint_flags": joint_flags,
        }
    return {"per_arm": per_arm, "n_instances": len(results["instances"])}


def _rates(f: dict) -> dict:
    n = max(1, f["n"])
    return f | {
        "validity_rate": f["validity"] / n, "fidelity_rate": f["fidelity"] / n,
        "action_rate": f["action"] / n, "terminal_rate": f["terminal"] / n,
        "joint_rate": f["joint"] / n,
        "false_change_rate": f["false_change"] / n,
        "false_defer_rate": f["false_defer"] / n,
        "missed_escalation_rate": f["missed_escalation"] / n,
        "drift_missed_rate": f["drift_missed"] / max(1, f["drift_n"]),
        "false_drift_alarm_rate": f["false_drift_alarm"] / max(1, f["faithful_n"]),
        "held_out_reuse_rate": f["reuse_solved"] / max(1, f["reuse_n"]),
        "mean_expansions": f["expansions"] / n,
    }


# --------------------------------------------------------------- statistics ---

def exact_binomial_two_sided(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(0, k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def paired(x: dict[str, bool], y: dict[str, bool], keys) -> dict:
    keys = list(keys)
    n = len(keys)
    b = sum(1 for k in keys if x[k] and not y[k])
    c = sum(1 for k in keys if y[k] and not x[k])
    diff = (b - c) / n if n else 0.0
    se = math.sqrt(max(0.0, (b + c) - (b - c) ** 2 / n)) / n if n else 0.0
    return {"n": n, "x_only": b, "y_only": c, "discordant": b + c,
            "diff_x_minus_y": diff, "wald_ci95": [diff - 1.96 * se, diff + 1.96 * se],
            "exact_p_two_sided": exact_binomial_two_sided(b, c)}


# -------------------------------------------------------------------- gates ---

ALPHA = 0.05
G2_MARGIN = 0.05


def gates(sc: dict, results: dict, selftest_ok) -> dict:
    pa = sc["per_arm"]
    ids_by_fam: dict[str, list[str]] = {}
    for inst in results["instances"]:
        ids_by_fam.setdefault(inst["family"], []).append(inst["task_id"])
    all_ids = [i["task_id"] for i in results["instances"]]
    M, B5 = pa[M_ARM], pa[B5_ARM]

    g0 = {"pass": bool(selftest_ok), "detail": "selftest report",
          "note": "oracle self-agreement, known-answer fixtures, parent fidelity, null calibration"}

    # G1: M vs B5 on the joint endpoint, pooled and per family (paired exact).
    g1_fam = {fam: paired(M["joint_flags"], B5["joint_flags"], ids)
              for fam, ids in sorted(ids_by_fam.items())}
    g1_pool = paired(M["joint_flags"], B5["joint_flags"], all_ids)
    g1_pass = g1_pool["diff_x_minus_y"] > 0 and g1_pool["exact_p_two_sided"] < ALPHA
    g1 = {"pass": bool(g1_pass), "pooled": g1_pool, "per_family": g1_fam,
          "note": "M is compared with the TOP-RUNG federation, which receives exactly "
                  "what M receives; the ladder is a property of the federation's "
                  "internal channel, never of M's privilege"}

    # G2: anti-conservatism / false escalation on the no-escalation families.
    g2_rows = {}
    g2_pass = True
    for fam in NO_ESCALATION_FAMILIES:
        mf = M["per_family"].get(fam); bf = B5["per_family"].get(fam)
        if not mf or not bf:
            continue
        ok = (mf["false_change_rate"] <= bf["false_change_rate"] + G2_MARGIN and
              mf["false_defer_rate"] <= bf["false_defer_rate"] + G2_MARGIN)
        g2_rows[fam] = {"M_false_change": mf["false_change_rate"],
                        "B5_false_change": bf["false_change_rate"],
                        "M_false_defer": mf["false_defer_rate"],
                        "B5_false_defer": bf["false_defer_rate"], "pass": ok}
        g2_pass &= ok
    fa = {"M_false_drift_alarm": M["pooled"]["false_drift_alarm_rate"],
          "B5_false_drift_alarm": B5["pooled"]["false_drift_alarm_rate"]}
    fa_ok = fa["M_false_drift_alarm"] <= fa["B5_false_drift_alarm"] + G2_MARGIN
    g2_pass &= fa_ok
    g2 = {"pass": bool(g2_pass), "per_family": g2_rows, "false_drift_alarm": fa | {"pass": fa_ok},
          "note": "M may not buy accuracy by escalating or deferring more than B5"}

    # G3: mechanism by omission -- the registered ablation must degrade the family.
    g3_rows = {}
    g3_pass = True
    for fam, abl in sorted(ABLATION_FOR_FAMILY.items()):
        if fam not in ids_by_fam:
            continue
        if abl is None:
            g3_rows[fam] = {"ablation": None, "gated": False,
                            "reason": NOT_GATED_REASON[fam]}
            continue
        if abl not in pa:
            continue
        p = paired(M["joint_flags"], pa[abl]["joint_flags"], ids_by_fam[fam])
        ok = p["diff_x_minus_y"] > 0
        g3_rows[fam] = {"ablation": abl, "gated": True,
                        "diff_M_minus_ablation": p["diff_x_minus_y"],
                        "exact_p": p["exact_p_two_sided"], "degrades": ok}
        g3_pass &= ok
    g3 = {"pass": bool(g3_pass), "per_family": g3_rows,
          "note": "a mechanism claim requires the named omission to break the exact "
                  "behaviour it is supposed to control"}

    # G4: H-EXT-3 interface-information ladder.
    rung_rates = [(r, pa[r]["pooled"]["joint_rate"]) for r in LADDER if r in pa]
    mono = all(b >= a - 1e-9 for (_, a), (_, b) in zip(rung_rates, rung_rates[1:]))
    top = rung_rates[-1][1] if rung_rates else 0.0
    m_rate = M["pooled"]["joint_rate"]
    if not mono:
        terminal = "LADDER_NON_MONOTONE"
    elif m_rate <= top + 1e-9:
        terminal = "RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL"
    else:
        terminal = "CONTROL_RESIDUAL_PERSISTS_AT_FULL_STRUCTURE"
    g4 = {"pass": bool(mono), "rungs": rung_rates, "M_joint_rate": m_rate,
          "top_rung_joint_rate": top, "ladder_terminal": terminal,
          "note": "H-EXT-3: what crosses the federation's module boundary"}

    # ---- pre-registered route ------------------------------------------------
    m_fid = M["pooled"]["fidelity_rate"]; b_fid = B5["pooled"]["fidelity_rate"]
    m_val = M["pooled"]["validity_rate"]; b_val = B5["pooled"]["validity_rate"]
    if not g0["pass"]:
        route, reason = "CANNOT_CHECK", "G0 failed: the oracle or the parents are not trustworthy"
    elif not g1_pass:
        mc = M["pooled"]["mean_expansions"]; bc = B5["pooled"]["mean_expansions"]
        route, reason = ("PARENT_SUFFICIENT",
                         f"M {M['pooled']['joint_rate']:.3f} vs B5 "
                         f"{B5['pooled']['joint_rate']:.3f}, paired exact p="
                         f"{g1_pool['exact_p_two_sided']:.3g}: no protected decision "
                         f"advantage over the strongest faithful federation "
                         f"(cost {mc:.0f} vs {bc:.0f} expansions, "
                         f"{100 * (mc - bc) / max(1e-9, bc):+.1f}%)")
    elif not g2_pass:
        route, reason = "MECHANISM_UNSUPPORTED", "G1 gain is bought by conservatism (G2 failed)"
    elif not g3_pass:
        route, reason = "MECHANISM_UNSUPPORTED", "G1 gain is not removed by the named omissions (G3 failed)"
    elif m_fid > b_fid and m_val <= b_val + 1e-9:
        route, reason = ("SPECIFICATION_FIDELITY_RESIDUAL",
                         f"the advantage is on specification fidelity ({m_fid:.3f} vs "
                         f"{b_fid:.3f}), not on proof validity ({m_val:.3f} vs {b_val:.3f}). "
                         "This branch is a descriptive sub-classification of a result "
                         "already significant under G1's paired exact test, not an "
                         "independent test of the fidelity endpoint")
    else:
        route, reason = "ME_RESIDUAL_SUPPORTED", "G1-G3 all passed on the joint endpoint"
    per_family_route = {
        fam: ("M_AHEAD" if g1_fam[fam]["diff_x_minus_y"] > 0 else
              "B5_AHEAD" if g1_fam[fam]["diff_x_minus_y"] < 0 else "TIED")
        for fam in g1_fam}
    return {"G0": g0, "G1": g1, "G2": g2, "G3": g3, "G4": g4,
            "ROUTE": {"route": route, "reason": reason,
                      "ladder_terminal": g4["ladder_terminal"],
                      "per_family": per_family_route,
                      "no_rescue": "no threshold, family, arm or budget in this analysis "
                                   "may be changed after these outcomes were inspected"}}


# --------------------------------------------------------------------- stages ---

def stage_selftest(out: Path) -> int:
    rows = fidelity_selftests()
    rows += _known_answer_fixtures()
    passed = all(r["passed"] for r in rows)
    out.mkdir(parents=True, exist_ok=True)
    rep = {"schema_version": "orion.v2.me-x3.selftest.v1", "passed": passed, "tests": rows}
    (out / "ME_X3_SELFTEST_REPORT.json").write_text(json.dumps(rep, indent=2, sort_keys=True))
    for r in rows:
        print(("PASS " if r["passed"] else "FAIL ") + r["test"] + ("  " + r["detail"] if r["detail"] else ""))
    print(f"selftest: {'PASSED' if passed else 'FAILED'} ({sum(r['passed'] for r in rows)}/{len(rows)})")
    return 0 if passed else 1


def _known_answer_fixtures() -> list[dict]:
    """Hand-authored instances whose correct answer is obvious by inspection."""
    from mex3_generator import TASK_BUDGET as TB
    from mex3_verdict import oracle_verdict
    P = Presentation("P0", 3, (((0, 1), (2,)), ((2, 2), (1,))))
    rows = []

    def mk(tid, intent, formal, **kw):
        return Task(task_id=tid, family=kw.pop("family", "F1_DIRECT_SEARCH"), seed="fixture",
                    base=P, alt=kw.pop("alt", None), alt_label="", alt_map=(),
                    library=kw.pop("library", ()), intent=intent, intent_invariants=(),
                    formal=formal, formal_pid=kw.pop("formal_pid", "P0"), surface_cues=(),
                    budget=TB, hidden=kw.pop("hidden", {}))

    cases = [
        ("fixture_short_proof_is_direct", mk("kx1", Statement((0, 1, 0, 1), (1,)),
                                             Statement((0, 1, 0, 1), (1,))),
         {"minimal_action": "CONTINUE_DIRECT_PROOF_SEARCH", "validity": "VERIFIED",
          "fidelity": "FAITHFUL"}),
        ("fixture_false_statement_is_refuted", mk("kx2", Statement((0,), (1,)),
                                                  Statement((0,), (1,))),
         {"minimal_action": "GENERATE_COUNTEREXAMPLE_OR_SMALL_MODEL",
          "validity": "REFUTED", "fidelity": "FAITHFUL"}),
        ("fixture_provable_but_wrong_question",
         mk("kx3", Statement((0,), (1,)), Statement((2, 0, 1), (2, 2)),
            hidden={"f7_subtype": "MATERIALLY_WEAKENED"}),
         {"fidelity": "MATERIALLY_WEAKENED",
          "minimal_action": "REFORMULATE_FORMAL_STATEMENT_WITH_PRESERVATION_CHECK"}),
        ("fixture_trivialised_statement_is_drift",
         mk("kx4", Statement((0,), (1,)), Statement((0, 1), (0, 1)),
            hidden={"f7_subtype": "DEGENERATE_TRIVIALIZATION"}),
         {"fidelity": "DEGENERATE_TRIVIALIZATION",
          "minimal_action": "REFORMULATE_FORMAL_STATEMENT_WITH_PRESERVATION_CHECK"}),
    ]
    for name, task, want in cases:
        got = oracle_verdict(task, ORACLE_WORD_LEN, ORACLE_EXPANSIONS, ORACLE_MODEL_SIZE)
        bad = {k: (want[k], got[k]) for k in want if got[k] != want[k]}
        rows.append({"test": name, "passed": not bad, "detail": canonical_json(bad) if bad else ""})
    return rows


def _write(out: Path, label: str, results: dict, custody: dict) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / f"ME_X3_{label}_RESULTS_V1.json").write_text(json.dumps(results, indent=2, sort_keys=True))
    (out / f"ME_X3_{label}_CUSTODY_V1.json").write_text(json.dumps(custody, indent=2, sort_keys=True))


def stage_dev(out: Path, per_family: int) -> int:
    pairs = generate_split(DEV_SEED, per_family)
    results, custody = run_split(pairs, "DEVELOPMENT", DEV_SEED)
    _write(out, "DEVELOPMENT", results, custody)
    print(f"DEVELOPMENT: {len(results['instances'])} instances, {len(results['arms'])} arms")
    return 0


def stage_protected(out: Path, per_family: int, seed_file: Path) -> int:
    if not AUTH_FILE.exists():
        print(f"REFUSED: {AUTH_FILE.name} is absent. The protected stage runs once, "
              "under a recorded authorization.", file=sys.stderr)
        return 3
    if not DESIGN_JSON.exists():
        print("REFUSED: the frozen design JSON is absent.", file=sys.stderr)
        return 3
    design = json.loads(DESIGN_JSON.read_text())
    want = design["custody"]["protected_seed_sha256"]
    if not seed_file.exists():
        print(f"REFUSED: custody seed file {seed_file} is absent.", file=sys.stderr)
        return 3
    got = sha256_file(seed_file)
    if got != want:
        print(f"REFUSED: custody seed sha256 {got} != frozen commitment {want}", file=sys.stderr)
        return 3
    seed = seed_file.read_text().strip()
    pairs = generate_split(seed, per_family)
    results, custody = run_split(pairs, "PROTECTED", None)
    results["design_sha256"] = sha256_file(DESIGN_JSON)
    results["authorization_sha256"] = sha256_file(AUTH_FILE)
    results["protected_seed_sha256"] = got
    _write(out, "PROTECTED", results, custody)
    print(f"PROTECTED: {len(results['instances'])} instances, {len(results['arms'])} arms")
    return 0


def render_md(a: dict) -> str:
    g = a["gates"]; pa = a["score"]["per_arm"]
    L = [f"# ME-X3 {a['label']} analysis V1", "",
         f"- instances: {a['n_instances']}", f"- results sha256: `{a['results_sha256']}`",
         f"- custody sha256: `{a['custody_sha256']}`", "",
         f"**Route: {g['ROUTE']['route']}** — {g['ROUTE']['reason']}", "",
         f"Ladder terminal (H-EXT-3): `{g['ROUTE']['ladder_terminal']}`", "",
         "## Outcome vector (pooled, per arm)", "",
         "| arm | validity | fidelity | minimal action | terminal | joint | false change | "
         "false defer | drift missed | false drift alarm | held-out reuse | mean expansions |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for arm, s in pa.items():
        p = s["pooled"]
        L.append(f"| `{arm}` | {p['validity_rate']:.3f} | {p['fidelity_rate']:.3f} | "
                 f"{p['action_rate']:.3f} | {p['terminal_rate']:.3f} | {p['joint_rate']:.3f} | "
                 f"{p['false_change_rate']:.3f} | {p['false_defer_rate']:.3f} | "
                 f"{p['drift_missed_rate']:.3f} | {p['false_drift_alarm_rate']:.3f} | "
                 f"{p['held_out_reuse_rate']:.3f} | {p['mean_expansions']:.1f} |")
    L += ["", "## Per family: M vs B5 (paired, exact binomial)", "",
          "| family | n | M joint | B5 joint | M-only | B5-only | diff | exact p | route |",
          "|---|---|---|---|---|---|---|---|---|"]
    for fam, r in g["G1"]["per_family"].items():
        m = pa[M_ARM]["per_family"].get(fam, {}); b = pa[B5_ARM]["per_family"].get(fam, {})
        L.append(f"| `{fam}` | {r['n']} | {m.get('joint_rate', 0):.3f} | "
                 f"{b.get('joint_rate', 0):.3f} | {r['x_only']} | {r['y_only']} | "
                 f"{r['diff_x_minus_y']:+.3f} | {r['exact_p_two_sided']:.3g} | "
                 f"{g['ROUTE']['per_family'][fam]} |")
    L += ["", "A pooled average may not hide a family-specific failure; the table above is "
              "the primary report and the pooled row is secondary.", ""]

    # F7 by registered drift subtype: a family score cannot be allowed to hide a
    # subtype (e.g. notational collapse) that is never detected.
    subs = pa[M_ARM].get("per_f7_subtype") or {}
    if subs:
        L += ["## F7 by registered drift subtype (realized draw)", "",
              "| subtype | n | M fidelity | B5 fidelity | A0 fidelity | M drift missed | "
              "M false drift alarm |", "|---|---|---|---|---|---|---|"]
        for sub, r in subs.items():
            b = pa[B5_ARM].get("per_f7_subtype", {}).get(sub, {})
            a0 = pa.get("A0_DIRECT", {}).get("per_f7_subtype", {}).get(sub, {})
            L.append(f"| `{sub}` | {r['n']} | {r['fidelity_rate']:.3f} | "
                     f"{b.get('fidelity_rate', float('nan')):.3f} | "
                     f"{a0.get('fidelity_rate', float('nan')):.3f} | "
                     f"{r['drift_missed_rate']:.3f} | {r['false_drift_alarm_rate']:.3f} |")
        L += ["", "Counts are the realized draw after oracle-verified rejection sampling, "
                  "not the generator's proposal weights.", ""]

    # F8 no-carry counterfactual, reported next to the reuse rate so that a
    # structurally guaranteed zero is visible rather than implied.
    nc = pa.get("M_MINUS_TRANSFER_REUSE_TRACKING", {}).get("per_family", {}).get("F8_TRANSFER")
    mf8 = pa[M_ARM]["per_family"].get("F8_TRANSFER")
    if nc and mf8:
        L += ["## F8 held-out reuse: carry versus no-carry", "",
              f"- M (carries its own invention): {mf8['held_out_reuse_rate']:.3f} "
              f"({mf8['reuse_solved']}/{mf8['reuse_n']})",
              f"- M minus transfer tracking (no carry): {nc['held_out_reuse_rate']:.3f} "
              f"({nc['reuse_solved']}/{nc['reuse_n']})",
              "",
              "The held-out target admits independent re-invention from the registered "
              "candidate pool as well as reuse of the source artefact, so a difference "
              "of zero here is the expected reading and F8 does not support a strong "
              "reusability claim. The counterfactual is printed so that this is visible "
              "rather than inferred from a passing rate.", ""]

    L += ["## Gates", "", "| gate | pass | note |", "|---|---|---|"]
    for k in ("G0", "G1", "G2", "G3", "G4"):
        L.append(f"| {k} | {'PASS' if g[k]['pass'] else 'FAIL'} | {g[k].get('note', '')} |")
    L += ["", "## H-EXT-3 interface ladder", "", "| rung | joint rate |", "|---|---|"]
    for r, v in g["G4"]["rungs"]:
        L.append(f"| `{r}` | {v:.3f} |")
    L += [f"| `{M_ARM}` | {g['G4']['M_joint_rate']:.3f} |", "",
          "## No-rescue clause", "", g["ROUTE"]["no_rescue"], ""]
    return "\n".join(L)


def stage_analyze(results_path: Path, custody_path: Path, out: Path,
                  selftest_report: Path | None = None) -> int:
    res = json.loads(results_path.read_text()); cus = json.loads(custody_path.read_text())
    label = res.get("label", "UNKNOWN")
    sp = selftest_report or (out / "ME_X3_SELFTEST_REPORT.json")
    selftest_ok = bool(json.loads(sp.read_text()).get("passed")) if sp.exists() else None
    sc = score(res, cus)
    gt = gates(sc, res, selftest_ok)
    slim = {arm: {"per_family": s["per_family"], "pooled": s["pooled"]}
            for arm, s in sc["per_arm"].items()}
    analysis = {"schema_version": SCHEMA_ANALYSIS, "label": label,
                "results_sha256": sha256_file(results_path),
                "custody_sha256": sha256_file(custody_path),
                "n_instances": sc["n_instances"], "score": {"per_arm": slim}, "gates": gt}
    out.mkdir(parents=True, exist_ok=True)
    (out / f"ME_X3_{label}_ANALYSIS_V1.json").write_text(json.dumps(analysis, indent=2, sort_keys=True))
    (out / f"ME_X3_{label}_ANALYSIS_V1.md").write_text(render_md(analysis))
    print(f"{label} route: {gt['ROUTE']['route']} ({gt['ROUTE']['reason']}); "
          f"ladder: {gt['ROUTE']['ladder_terminal']}; "
          f"M joint {sc['per_arm'][M_ARM]['pooled']['joint_rate']:.3f}, "
          f"B5 joint {sc['per_arm'][B5_ARM]['pooled']['joint_rate']:.3f}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("selftest", "dev", "protected", "analyze"))
    ap.add_argument("--out", type=Path, default=HERE / "results")
    ap.add_argument("--per-family", type=int, default=None)
    ap.add_argument("--results", type=Path); ap.add_argument("--custody", type=Path)
    ap.add_argument("--seed-file", type=Path, default=DEFAULT_SEED_FILE)
    ap.add_argument("--selftest-report", type=Path, default=None)
    a = ap.parse_args(argv)
    if a.stage == "selftest":
        return stage_selftest(a.out)
    if a.stage == "dev":
        return stage_dev(a.out, a.per_family or DEV_PER_FAMILY)
    if a.stage == "protected":
        return stage_protected(a.out, a.per_family or PROTECTED_PER_FAMILY, a.seed_file)
    if not a.results or not a.custody:
        print("analyze requires --results and --custody", file=sys.stderr); return 2
    return stage_analyze(a.results, a.custody, a.out, a.selftest_report)


if __name__ == "__main__":
    sys.exit(main())

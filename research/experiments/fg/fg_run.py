#!/usr/bin/env python3
"""FG70 exact study runner (frozen with design V1).

Stages
  selftest   parent fidelity (native known-answer tests), G0a hand-authored
             known-answer fixtures, oracle self-agreement on a small generated
             set, and the *planted positives* every no-alarm gate must trip.
  dev        DEVELOPMENT split (public seed, <= 40 instances). Never protected
             evidence.
  protected  PROTECTED split. Refuses unless PROTECTED_RUN_AUTHORIZATION.json
             (human-written token, acknowledged design sha256) sits next to this
             script AND the custody seed file hashes to the frozen commitment.
  analyze    Score a results file against its custody expected file: outcomes,
             gates G0-G3 (each with the number of instances actually
             evaluated), and the pre-registered route.

Design: FG70_FORMALISM_NEEDED_OR_NOT_EXACT_STUDY_DESIGN_V1.{md,json}
Series identity: ORION-FG-L5-EXACT-V1 (see the design's disambiguation block;
this is *not* the fmfg-r2 campaign of owner issue #48).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import sys
import time
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

import fg_arms as A  # noqa: E402
import fg_model as M  # noqa: E402
import fg_oracle as O  # noqa: E402
import fg_parents as P  # noqa: E402
import fg70_generator as G  # noqa: E402

SERIES_ID = "ORION-FG-L5-EXACT-V1"
SUITE = "FG70"
SCHEMA_RESULTS = "orion.v2.fg70.exact-study-results.v1"
SCHEMA_ANALYSIS = "orion.v2.fg70.exact-study-analysis.v1"
DESIGN_JSON = HERE / "FG70_FORMALISM_NEEDED_OR_NOT_EXACT_STUDY_DESIGN_V1.json"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
DEV_SEED = "FG70-DEV-20260902"
DEV_PER_STRATUM = 6            # 36 instances <= 40
PROTECTED_PER_STRATUM = 28     # 168 instances >= the registered minimum of 160
DEFAULT_SEED_FILE = Path(
    os.environ.get("FG_PROTECTED_SEED_FILE", str(Path.home() / ".orion-custody/fg/PROTECTED_SEED_V1.txt"))
)
SHUFFLE_NULL_SEED = 20260902

# gate constants (frozen before any protected outcome exists)
G1A_IDENTITY_RULE = 0.995
G1A_STRATUM_RULE = 0.05
G2M_ABSOLUTE_CEILING = 0.02
G0C_RANDOM_CEILING = 0.25
G0C_SHUFFLE_CEILING = 0.30
G0C_PLANTED_POSITIVE_FLOOR = 0.50


# ---------------------------------------------------------------------------
# statistics
# ---------------------------------------------------------------------------


def mcnemar_exact_two_sided(wins_a: int, wins_b: int) -> float:
    n = wins_a + wins_b
    if n == 0:
        return 1.0
    k = min(wins_a, wins_b)
    tail = sum(math.comb(n, i) for i in range(0, k + 1)) / (2 ** n)
    return min(1.0, 2.0 * tail)


def holm_adjust(pvalues: Mapping[str, float]) -> dict[str, float]:
    ordered = sorted(pvalues.items(), key=lambda item: item[1])
    out: dict[str, float] = {}
    running = 0.0
    total = len(ordered)
    for index, (name, value) in enumerate(ordered):
        adjusted = min(1.0, (total - index) * value)
        running = max(running, adjusted)
        out[name] = running
    return out


# ---------------------------------------------------------------------------
# execution
# ---------------------------------------------------------------------------


def run_split(instances: Sequence[M.Instance]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    started = time.time()
    for instance in instances:
        view = M.arm_view(instance)
        row = {"instance_id": instance.instance_id, "arms": {}}
        for arm in A.ARM_SPECS:
            row["arms"][arm] = A.run_arm(arm, view).as_dict()
        rows.append(row)
    return {
        "schema_version": SCHEMA_RESULTS,
        "series_id": SERIES_ID,
        "suite": SUITE,
        "arms": list(A.ARM_SPECS),
        "rows": rows,
        "wall_seconds": round(time.time() - started, 3),
    }


def expected_custody(instances: Sequence[M.Instance]) -> dict[str, Any]:
    rows = []
    for instance in instances:
        agree, verdict_a, verdict_b = O.oracle_agrees(instance)
        rows.append(
            {
                "instance_id": instance.instance_id,
                "stratum": instance.stratum,
                "planted_decoys": list(instance.planted_decoys),
                "oracle_agrees": agree,
                "method_a": verdict_a.as_dict(),
                "method_b": verdict_b.as_dict(),
                "instance": M.instance_to_json(instance),
            }
        )
    return {
        "schema_version": "orion.v2.fg70.exact-study-custody.v1",
        "series_id": SERIES_ID,
        "suite": SUITE,
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# analysis
# ---------------------------------------------------------------------------


def analyze(results: Mapping[str, Any], custody: Mapping[str, Any]) -> dict[str, Any]:
    truth = {row["instance_id"]: row for row in custody["rows"]}
    arms = list(results["arms"])
    strata = list(G.STRATA)
    n = len(results["rows"])

    per_arm: dict[str, dict[str, Any]] = {}
    per_arm_stratum: dict[str, dict[str, dict[str, int]]] = {}
    for arm in arms:
        per_arm[arm] = {
            "correct": 0,
            "false_invention": 0,
            "missed_deficit": 0,
            "over_escalation": 0,
            "under_escalation": 0,
            "cannot_check": 0,
        }
        per_arm_stratum[arm] = {s: {"n": 0, "correct": 0, "false_invention": 0} for s in strata}

    non_invention_n = sum(1 for row in truth.values() if row["stratum"] != M.NEW_PRIMITIVE)
    non_no_change_n = sum(1 for row in truth.values() if row["stratum"] != M.NO_CHANGE)

    for row in results["rows"]:
        gold = truth[row["instance_id"]]["stratum"]
        gold_cost = M.TIER_COST[gold]
        for arm in arms:
            got = row["arms"][arm]["terminal"]
            bucket = per_arm[arm]
            stat = per_arm_stratum[arm][gold]
            stat["n"] += 1
            if got == gold:
                bucket["correct"] += 1
                stat["correct"] += 1
            if got == A.CANNOT_CHECK:
                bucket["cannot_check"] += 1
                continue
            if got == M.NEW_PRIMITIVE and gold != M.NEW_PRIMITIVE:
                bucket["false_invention"] += 1
                stat["false_invention"] += 1
            if got == M.NO_CHANGE and gold != M.NO_CHANGE:
                bucket["missed_deficit"] += 1
            cost = M.TIER_COST[got]
            if cost > gold_cost:
                bucket["over_escalation"] += 1
            elif cost < gold_cost:
                bucket["under_escalation"] += 1

    # ---- gates -----------------------------------------------------------
    gates: dict[str, Any] = {}

    oracle_evaluated = len(truth)
    oracle_violations = sum(1 for row in truth.values() if not row["oracle_agrees"])
    gates["G0b_ORACLE_SELF_AGREEMENT"] = {
        "verdict": "PASS" if oracle_violations == 0 and oracle_evaluated == n else "FAIL",
        "instances_evaluated": oracle_evaluated,
        "violations": oracle_violations,
        "rule": "method A (bucket + bitmask cover) == method B (partition meet) on every instance",
    }

    random_correct = per_arm["C_RANDOM_TERMINAL"]["correct"] / n
    shuffle_correct = _shuffled_label_null(results, truth)
    always_rate = per_arm["C_ALWAYS_INVENT"]["false_invention"] / max(non_invention_n, 1)
    eager_rate = per_arm["M_MINUS_ORDER_AND_GATE"]["false_invention"] / max(non_invention_n, 1)
    never_change_rate = per_arm["C_NEVER_CHANGE"]["missed_deficit"] / max(non_no_change_n, 1)
    g0c_checks = {
        "random_control_accuracy": random_correct,
        "shuffled_label_null_accuracy": shuffle_correct,
        "planted_positive_C_ALWAYS_INVENT_false_invention_rate": always_rate,
        "planted_positive_M_MINUS_ORDER_AND_GATE_false_invention_rate": eager_rate,
        "planted_positive_C_NEVER_CHANGE_missed_deficit_rate": never_change_rate,
    }
    g0c_pass = (
        random_correct <= G0C_RANDOM_CEILING
        and shuffle_correct <= G0C_SHUFFLE_CEILING
        and always_rate >= G0C_PLANTED_POSITIVE_FLOOR
        and eager_rate > 0.0
        and never_change_rate >= G0C_PLANTED_POSITIVE_FLOOR
    )
    gates["G0c_NULL_CALIBRATION"] = {
        "verdict": "PASS" if g0c_pass else "FAIL",
        "instances_evaluated": n,
        "false_invention_denominator": non_invention_n,
        "checks": g0c_checks,
        "rule": (
            f"random <= {G0C_RANDOM_CEILING}; shuffled-label null <= {G0C_SHUFFLE_CEILING}; "
            f"planted positive C_ALWAYS_INVENT >= {G0C_PLANTED_POSITIVE_FLOOR} (trips G2M); "
            "order+gate double ablation > 0 (trips G2M); planted positive C_NEVER_CHANGE "
            f">= {G0C_PLANTED_POSITIVE_FLOOR} (trips G2). Every no-alarm gate must be shown to fire."
        ),
    }

    m_wins = b_wins = identical = 0
    stratum_discord = {s: 0 for s in strata}
    for row in results["rows"]:
        gold = truth[row["instance_id"]]["stratum"]
        m_ok = row["arms"][A.M_ARM]["terminal"] == gold
        b_ok = row["arms"][A.B_ARM]["terminal"] == gold
        if row["arms"][A.M_ARM]["terminal"] == row["arms"][A.B_ARM]["terminal"]:
            identical += 1
        else:
            stratum_discord[gold] += 1
        if m_ok and not b_ok:
            m_wins += 1
        elif b_ok and not m_ok:
            b_wins += 1
    identity_rate = identical / n
    p_value = mcnemar_exact_two_sided(m_wins, b_wins)
    worst_stratum = max(
        (stratum_discord[s] / max(per_arm_stratum[A.M_ARM][s]["n"], 1) for s in strata), default=0.0
    )
    g1a = identity_rate >= G1A_IDENTITY_RULE and worst_stratum <= G1A_STRATUM_RULE
    g1b = m_wins > b_wins and p_value <= 0.05
    gates["G1a_FEDERATION_REPRODUCES_M"] = {
        "verdict": "PASS" if g1a else "NOT_FIRED",
        "instances_evaluated": n,
        "decision_identity": identity_rate,
        "worst_stratum_discordance": worst_stratum,
        "rule": f"identity >= {G1A_IDENTITY_RULE} and no stratum > {G1A_STRATUM_RULE}",
    }
    gates["G1b_M_ADVANTAGE"] = {
        "verdict": "PASS" if g1b else "NOT_FIRED",
        "instances_evaluated": n,
        "m_only_correct": m_wins,
        "federation_only_correct": b_wins,
        "mcnemar_exact_two_sided_p": p_value,
        "rule": "paired exact two-sided p <= 0.05 with M ahead",
    }

    m_missed = per_arm[A.M_ARM]["missed_deficit"]
    b_missed = per_arm[A.B_ARM]["missed_deficit"]
    gates["G2_ANTI_CONSERVATISM"] = {
        "verdict": "PASS" if m_missed <= b_missed else "FAIL",
        "instances_evaluated": non_no_change_n,
        "m_missed_deficits": m_missed,
        "federation_missed_deficits": b_missed,
        "planted_positive_C_NEVER_CHANGE_missed_deficits": per_arm["C_NEVER_CHANGE"]["missed_deficit"],
        "rule": "M's missed-deficit count <= the federation's, over instances whose truth is not "
                "NO_CHANGE; the planted positive C_NEVER_CHANGE must show the counter can fire",
    }

    m_false = per_arm[A.M_ARM]["false_invention"]
    b_false = per_arm[A.B_ARM]["false_invention"]
    m_false_rate = m_false / max(non_invention_n, 1)
    per_stratum_denominator = {
        s: per_arm_stratum[A.M_ARM][s]["n"] for s in strata if s != M.NEW_PRIMITIVE
    }
    empty_denominator = [s for s, count in per_stratum_denominator.items() if count == 0]
    g2m_pass = (
        m_false <= b_false
        and m_false_rate <= G2M_ABSOLUTE_CEILING
        and not empty_denominator
    )
    gates["G2M_ANTI_INVENTION"] = {
        "verdict": "PASS" if g2m_pass else "FAIL",
        "co_primary": True,
        "non_compensatory": True,
        "instances_evaluated": non_invention_n,
        "per_stratum_denominator": per_stratum_denominator,
        "empty_denominator_strata": empty_denominator,
        "m_false_inventions": m_false,
        "m_false_invention_rate": m_false_rate,
        "federation_false_inventions": b_false,
        "rule": (
            f"M's false-invention count <= the federation's AND rate <= {G2M_ABSOLUTE_CEILING}; "
            "hard-fails if any non-NEW_PRIMITIVE stratum has an empty denominator"
        ),
    }

    mechanism_rows = []
    for stratum in strata:
        ablation = A.ABLATION_FOR_STRATUM.get(stratum, A.DEFAULT_ABLATION)
        stat_m = per_arm_stratum[A.M_ARM][stratum]
        stat_a = per_arm_stratum[ablation][stratum]  # noqa: E501
        stat_b = per_arm_stratum[A.B_ARM][stratum]
        mechanism_rows.append(
            {
                "stratum": stratum,
                "ablation": ablation,
                "n": stat_m["n"],
                "m_correct": stat_m["correct"],
                "ablation_correct": stat_a["correct"],
                "federation_correct": stat_b["correct"],
                "ablation_degrades": stat_a["correct"] < stat_m["correct"],
            }
        )
    gates["G3_MECHANISM_BY_OMISSION"] = {
        "verdict": "REPORTED" if not g1b else (
            "PASS" if all(row["ablation_degrades"] for row in mechanism_rows if row["n"]) else "FAIL"
        ),
        "instances_evaluated": n,
        "rows": mechanism_rows,
        "invention_factorial": {
            arm: {
                "false_inventions": per_arm[arm]["false_invention"],
                "denominator": non_invention_n,
                "accuracy": per_arm[arm]["correct"] / n,
            }
            for arm in (
                A.M_ARM,
                "M_MINUS_ADMISSION_GATE",
                "M_MINUS_COST_ORDER",
                "M_MINUS_ORDER_AND_GATE",
                "M_EAGER_INVENT",
                "C_ALWAYS_INVENT",
            )
        },
        "rule": "2x2 omission of the registered cost order and of the fail-closed admission gate",
    }

    # ---- route -----------------------------------------------------------
    hard_fail = any(
        gates[name]["verdict"] == "FAIL" for name in ("G0b_ORACLE_SELF_AGREEMENT", "G0c_NULL_CALIBRATION")
    )
    if hard_fail:
        route = "CANNOT_CHECK"
    elif gates["G2M_ANTI_INVENTION"]["verdict"] == "FAIL":
        route = "FALSE_INVENTION_HARM"
    elif gates["G2_ANTI_CONSERVATISM"]["verdict"] == "FAIL":
        route = "M_OVER_CONSERVATIVE"
    elif g1a:
        route = "PARENT_SUFFICIENT"
    elif g1b and gates["G3_MECHANISM_BY_OMISSION"]["verdict"] == "PASS":
        route = "FG70_RESIDUAL_CANDIDATE"
    elif g1b:
        route = "CANNOT_CHECK"
    else:
        route = "PARENT_SUFFICIENT"

    holm = holm_adjust({SUITE: p_value})

    return {
        "schema_version": SCHEMA_ANALYSIS,
        "series_id": SERIES_ID,
        "suite": SUITE,
        "instances": n,
        "strata": strata,
        "per_arm": {
            arm: {**per_arm[arm], "accuracy": per_arm[arm]["correct"] / n} for arm in arms
        },
        "per_arm_stratum": per_arm_stratum,
        "gates": gates,
        "route": route,
        "holm": {
            "family": "FG10..FG70 G1b paired exact tests",
            "members_available_at_this_run": [SUITE],
            "raw_p": {SUITE: p_value},
            "adjusted_p": holm,
            "note": "the family is completed by the FG series rollup; with one member the "
                    "adjustment is the identity",
        },
        "authority": {
            "grants_scientific_truth": False,
            "grants_new_mathematical_theory": False,
            "grants_field_status": False,
            "grants_submission_readiness": False,
        },
    }


def _shuffled_label_null(results: Mapping[str, Any], truth: Mapping[str, Any]) -> float:
    labels = [truth[row["instance_id"]]["stratum"] for row in results["rows"]]
    rng = random.Random(SHUFFLE_NULL_SEED)
    shuffled = labels[:]
    rng.shuffle(shuffled)
    hits = sum(
        1
        for row, label in zip(results["rows"], shuffled)
        if row["arms"][A.M_ARM]["terminal"] == label
    )
    return hits / max(len(labels), 1)


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------


def selftest() -> dict[str, Any]:
    report: dict[str, Any] = {"series_id": SERIES_ID, "suite": SUITE, "checks": []}

    def record(name: str, ok: bool, evaluated: int, detail: str = "") -> None:
        report["checks"].append(
            {"check": name, "passed": bool(ok), "instances_evaluated": evaluated, "detail": detail}
        )

    fidelity = P.fidelity_selftests()
    failed = [row for row in fidelity if not row["passed"]]
    record("PARENT_FIDELITY_NATIVE_KNOWN_ANSWER", not failed, len(fidelity), json.dumps(failed))
    report["parent_fidelity"] = fidelity

    fixtures = G.known_answer_fixtures()
    oracle_ok = True
    m_ok = True
    b_ok = True
    invent_trips = 0
    collision_fixtures = 0
    for fixture in fixtures:
        instance = fixture["instance"]
        agree, verdict_a, _ = O.oracle_agrees(instance)
        oracle_ok &= agree and verdict_a.terminal == fixture["expected"]
        view = M.arm_view(instance)
        m_ok &= A.run_arm(A.M_ARM, view).terminal == fixture["expected"]
        b_ok &= A.run_arm(A.B_ARM, view).terminal == fixture["expected"]
        if fixture["expected"] not in (M.NO_CHANGE, M.NEW_PRIMITIVE):
            collision_fixtures += 1
            if A.run_arm("C_ALWAYS_INVENT", view).terminal == M.NEW_PRIMITIVE:
                invent_trips += 1
    record("G0a_KNOWN_ANSWER_ORACLE", oracle_ok, len(fixtures))
    record("G0a_KNOWN_ANSWER_M_EXACT", m_ok, len(fixtures))
    record("G0a_KNOWN_ANSWER_FEDERATION_EXACT", b_ok, len(fixtures))
    record(
        "PLANTED_POSITIVE_ANTI_INVENTION_GATE_FIRES",
        invent_trips == collision_fixtures and collision_fixtures > 0,
        collision_fixtures,
        f"C_ALWAYS_INVENT falsely invented on {invent_trips}/{collision_fixtures} fixtures whose "
        "truth is a cheaper repair; a gate that does not fire here is broken",
    )

    never_change_trips = 0
    change_fixtures = 0
    for fixture in fixtures:
        if fixture["expected"] == M.NO_CHANGE:
            continue
        change_fixtures += 1
        if A.run_arm("C_NEVER_CHANGE", M.arm_view(fixture["instance"])).terminal == M.NO_CHANGE:
            never_change_trips += 1
    record(
        "PLANTED_POSITIVE_ANTI_CONSERVATISM_GATE_FIRES",
        never_change_trips == change_fixtures and change_fixtures > 0,
        change_fixtures,
        f"C_NEVER_CHANGE missed the deficit on {never_change_trips}/{change_fixtures} fixtures "
        "whose truth is not NO_CHANGE; G2's counter is otherwise structurally unreachable "
        "because every arm's first move is the shared collision check",
    )

    probe = G.generate_split("selftest", "FG70-SELFTEST", 2)
    agree_count = sum(1 for instance in probe if O.oracle_agrees(instance)[0])
    label_count = sum(1 for instance in probe if O.tier_search(instance).terminal == instance.stratum)
    record("G0b_ORACLE_SELF_AGREEMENT_PROBE", agree_count == len(probe), len(probe))
    ablation_rows = []
    for stratum in G.STRATA:
        ablation = A.ABLATION_FOR_STRATUM[stratum]
        eligible = [i for i in probe if i.stratum == stratum]
        correct = sum(
            1 for i in eligible
            if A.run_arm(ablation, M.arm_view(i)).terminal == stratum
        )
        ablation_rows.append((stratum, ablation, correct, len(eligible)))
    record(
        "EVERY_STRATUM_HAS_A_DEGRADING_OMISSION_ABLATION",
        all(correct < total for _, _, correct, total in ablation_rows),
        len(G.STRATA),
        json.dumps([{"stratum": s, "ablation": a, "correct": c, "n": n} for s, a, c, n in ablation_rows]),
    )
    record("PLANTED_LABEL_IS_THE_CHEAPEST_TIER", label_count == len(probe), len(probe))

    denom = sum(1 for instance in probe if instance.stratum != M.NEW_PRIMITIVE)
    invention_available = sum(
        1
        for instance in probe
        if instance.stratum != M.NEW_PRIMITIVE
        and M.NEW_PRIMITIVE in O.tier_search(instance).feasible_tiers
    )
    record(
        "ANTI_INVENTION_DENOMINATOR_IS_NON_EMPTY_AND_TEMPTING",
        denom > 0 and invention_available > 0,
        denom,
        f"{invention_available}/{denom} non-NEW_PRIMITIVE instances carry a *working* new "
        "primitive, so escalation is always available and always adequate",
    )

    reference_agreement = _reference_module_agreement(probe)
    record(
        "REFERENCE_MODULE_COLLISION_AGREEMENT",
        reference_agreement["disagreements"] == 0,
        reference_agreement["evaluated"],
        "orion_v2.formalism_genesis.representation_collisions agrees with the oracle's "
        "collision set; necessary, not sufficient, for a residual",
    )

    report["passed"] = all(check["passed"] for check in report["checks"])
    return report


def _reference_module_agreement(instances: Iterable[M.Instance]) -> dict[str, int]:
    from orion_v2.formalism_genesis import representation_collisions

    evaluated = 0
    disagreements = 0
    for instance in instances:
        cand = A.Candidates.build(instance)
        oracle_set = set(O.collisions_by_bucket(instance, instance.active_formalism.term_ids))
        module_set = {
            tuple(sorted((c.left_case_id, c.right_case_id)))
            for c in representation_collisions(A._distinction_cases(cand))
        }
        evaluated += 1
        if {tuple(sorted(pair)) for pair in oracle_set} != module_set:
            disagreements += 1
    return {"evaluated": evaluated, "disagreements": disagreements}


# ---------------------------------------------------------------------------
# protected-run guard
# ---------------------------------------------------------------------------


def _design_sha256() -> str:
    return M.sha256_text(DESIGN_JSON.read_text(encoding="utf-8"))


def _seed_commitment() -> str:
    payload = json.loads(DESIGN_JSON.read_text(encoding="utf-8"))
    return payload["custody"]["protected_seed_sha256"]


class ProtectedRunRefused(SystemExit):
    """Exit code 3: the protected stage refused to run."""

    def __init__(self, message: str) -> None:
        print(message, file=sys.stderr)
        super().__init__(3)


def load_authorized_seed() -> str:
    if not AUTH_FILE.is_file():
        raise ProtectedRunRefused(
            "REFUSED: PROTECTED_RUN_AUTHORIZATION.json is absent; the protected split "
            "may not be generated."
        )
    auth = json.loads(AUTH_FILE.read_text(encoding="utf-8"))
    if auth.get("human_written") is not True:
        raise ProtectedRunRefused("REFUSED: authorization is not marked human_written")
    token = str(auth.get("human_written_token", ""))
    if len(token) < 16:
        raise ProtectedRunRefused("REFUSED: authorization token is shorter than 16 characters")
    if auth.get("acknowledged_design_sha256") != _design_sha256():
        raise ProtectedRunRefused("REFUSED: authorization does not acknowledge the frozen design sha256")
    seed_file = Path(auth.get("seed_file", str(DEFAULT_SEED_FILE))).expanduser()
    if not seed_file.is_file():
        raise ProtectedRunRefused(f"REFUSED: custody seed file {seed_file} is absent")
    seed = seed_file.read_text(encoding="utf-8").strip()
    if M.sha256_text(seed) != _seed_commitment():
        raise ProtectedRunRefused("REFUSED: custody seed does not hash to the frozen commitment")
    return seed


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _write(path: Path, payload: Any) -> str:
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    return M.sha256_text(text)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FG70 exact study runner")
    parser.add_argument("stage", choices=("selftest", "dev", "protected", "analyze"))
    parser.add_argument("--out", default=str(HERE / "results"))
    args = parser.parse_args(argv)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    if args.stage == "selftest":
        report = selftest()
        digest = _write(out / "FG70_SELFTEST_REPORT_V1.json", report)
        print(json.dumps({"passed": report["passed"], "sha256": digest}, indent=2))
        return 0 if report["passed"] else 1

    if args.stage == "analyze":
        results = json.loads((out / f"FG70_{_label(out)}_RESULTS_V1.json").read_text())
        custody = json.loads((out / f"FG70_{_label(out)}_EXPECTED_CUSTODY_V1.json").read_text())
        analysis = analyze(results, custody)
        _write(out / f"FG70_{_label(out)}_ANALYSIS_V1.json", analysis)
        print(json.dumps({"route": analysis["route"],
                          "gates": {k: v["verdict"] for k, v in analysis["gates"].items()}}, indent=2))
        return 0

    if args.stage == "dev":
        label, seed, per = "DEVELOPMENT", DEV_SEED, DEV_PER_STRATUM
    else:
        label, seed, per = "PROTECTED", load_authorized_seed(), PROTECTED_PER_STRATUM

    instances = G.generate_split(label.lower(), seed, per)
    results = run_split(instances)
    results["label"] = label
    custody = expected_custody(instances)
    custody["label"] = label
    r = _write(out / f"FG70_{label}_RESULTS_V1.json", results)
    c = _write(out / f"FG70_{label}_EXPECTED_CUSTODY_V1.json", custody)
    analysis = analyze(results, custody)
    analysis["label"] = label
    a = _write(out / f"FG70_{label}_ANALYSIS_V1.json", analysis)
    _write(out / f"FG70_{label}_TIMING_V1.json",
           {"wall_seconds": results["wall_seconds"], "instances": len(instances)})
    print(json.dumps(
        {
            "label": label,
            "instances": len(instances),
            "route": analysis["route"],
            "gates": {k: v["verdict"] for k, v in analysis["gates"].items()},
            "sha256": {"results": r, "custody": c, "analysis": a},
        },
        indent=2,
    ))
    return 0


def _label(out: Path) -> str:
    return "PROTECTED" if (out / "FG70_PROTECTED_RESULTS_V1.json").is_file() else "DEVELOPMENT"


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""EL10 epistemic-locality suite runner (prospective custody, gold-blind).

prepare: seeded generators -> public_tasks.json + private_oracle.json + per-arm
requests; FROZEN_SUITE.json freeze record.
dispatch: hash-commit + REMOVE the private oracle before any arm runs, run
arms with ORION_GOLD_ACCESS=NONE, restore + verify in finally.
evaluate: missing != wrong; per-arm metrics; paired exact McNemar x12 with
Holm correction; kill-rule verdict computed on point estimates.

Protocol: research/experiments/EPISTEMIC_LOCALITY_VERIFICATION_PROTOCOL_V1.md
Freeze doc: research/experiments/EPISTEMIC_LOCALITY_EL10_SUITE_FREEZE_V1.md
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from orion_el10_cases import CLASSES, generate_case  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ARMS = ["GLOBAL_RANKING", "CURRENT_F0", "CURRENT_F2", "F2_PLUS_LOCALITY_INTERFACE"]
LOCALITY = "F2_PLUS_LOCALITY_INTERFACE"
PER_CLASS = 6
SEED = 20260830
CRITICAL_METRICS = [
    "false_universalization_rate",
    "invalid_comparison_detection",
    "cross_frame_transport_error",
]
# McNemar family: (LOCALITY - other) contrast on decision correctness + critical metrics.
CONTRAST_BASES = ["GLOBAL_RANKING", "CURRENT_F0", "CURRENT_F2"]
METRIC_TESTS = ["local_decision_correctness"] + CRITICAL_METRICS


class SuiteError(RuntimeError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False) + "\n")


def read_json(path: Path):
    return json.loads(path.read_text())


def prepare(workdir: Path, seed: int = SEED, per_class: int = PER_CLASS, arms=None, force: bool = False) -> None:
    arms = arms or ARMS
    if workdir.exists():
        if not force:
            raise SuiteError(f"workdir exists: {workdir}")
        shutil.rmtree(workdir)
    import random

    rng = random.Random(seed)
    public_tasks, private_answers = [], {}
    for cls in CLASSES:
        for index in range(per_class):
            case_rng = random.Random(rng.getrandbits(64))
            public, oracle = generate_case(case_rng, cls)
            task_id = f"el10-{cls.lower()}-{index + 1:02d}"
            public["task_id"] = task_id
            public_tasks.append(public)
            private_answers[task_id] = oracle
            for arm in arms:
                write_json(
                    workdir / "requests" / arm / f"{task_id}.json",
                    {
                        "schema_version": "orion.v2.el10-request.v1",
                        "task_id": task_id,
                        "arm_id": arm,
                        "task": public,
                        "scientific_truth_authorized": False,
                        "publication_readiness_authorized": False,
                    },
                )
    write_json(workdir / "public_tasks.json", {"schema_version": "orion.v2.el10-public.v1", "tasks": public_tasks})
    write_json(workdir / "private_oracle.json", {"schema_version": "orion.v2.el10-private.v1", "answers": private_answers})
    write_json(
        workdir / "FROZEN_SUITE.json",
        {
            "schema_version": "orion.v2.el10-freeze.v1",
            "suite": "EL10",
            "seed": seed,
            "classes": CLASSES,
            "per_class": per_class,
            "task_count": len(public_tasks),
            "arms": arms,
            "private_oracle_visible_to_solver": False,
            "answer_contract": "decision|holds_across_contexts|perspective_dependent_coordinates|comparison_valid|transport_verdict|brief_rationale",
            "authority": {
                "grants_scientific_truth": False,
                "grants_universal_intelligence_definition": False,
                "grants_primary_endpoint_change": False,
                "grants_evolution_eq_cognition": False,
            },
        },
    )


def command_prefix() -> list:
    override = os.environ.get("ORION_EL_ARM_COMMAND", "").strip()
    if override:
        import shlex

        return shlex.split(override)
    return [sys.executable, str(ROOT / "scripts/orion_epistemic_locality_arms.py")]


def dispatch(workdir: Path, arms=None, concurrency: int = 4, overwrite: bool = False) -> None:
    arms = arms or ARMS
    private = workdir / "private_oracle.json"
    if not private.exists():
        raise SuiteError("missing private oracle")
    data = private.read_bytes()
    write_json(
        workdir / "PRIVATE_ORACLE_COMMITMENT.json",
        {"sha256": digest(data), "private_removed_before_dispatch": True},
    )
    private.unlink()
    env = os.environ.copy()
    env["ORION_GOLD_ACCESS"] = "NONE"
    env["ORION_OUTCOME_ACCESS"] = "NONE"
    jobs = []
    for arm in arms:
        for request in sorted((workdir / "requests" / arm).glob("*.json")):
            response = workdir / "responses" / arm / request.name
            if response.exists() and not overwrite:
                continue
            jobs.append((arm, request, response))
    prefix = command_prefix()

    def run_one(job):
        arm, request, response = job
        response.parent.mkdir(parents=True, exist_ok=True)
        start = time.time()
        completed = subprocess.run(
            prefix + ["--request", str(request), "--response", str(response)],
            env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
            timeout=int(os.environ.get("ORION_EL_TIMEOUT", "1800")),
        )
        return {
            "arm": arm, "task": request.stem, "returncode": completed.returncode,
            "seconds": round(time.time() - start, 3), "output_tail": completed.stdout[-800:],
        }

    rows = []
    try:
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(run_one, job) for job in jobs]
            for future in as_completed(futures):
                rows.append(future.result())
    finally:
        if private.exists():
            raise SuiteError("private oracle reappeared during dispatch")
        private.write_bytes(data)
    write_json(
        workdir / "DISPATCH_RECEIPT.json",
        {
            "jobs_dispatched": len(rows),
            "jobs": rows,
            "all_returncodes_zero": all(row["returncode"] == 0 for row in rows),
            "oracle_restored_hash_match": digest(private.read_bytes()) == digest(data),
        },
    )


def _cond_rate(per_task, task_ids, arm, oracle_pred, field):
    """P(arm made this error/success | oracle condition and response valid)."""
    rows = [
        per_task[t][arm]
        for t in task_ids
        if oracle_pred(t) and not per_task[t][arm].get("missing")
    ]
    if not rows:
        return None
    return sum(1 for r in rows if r.get(field)) / len(rows)


def _cond_mean(per_task, task_ids, arm, oracle_pred, field):
    vals = [
        per_task[t][arm][field]
        for t in task_ids
        if oracle_pred(t) and not per_task[t][arm].get("missing")
        and per_task[t][arm].get(field) is not None
    ]
    return (sum(vals) / len(vals)) if vals else None


def _load_response(workdir: Path, arm: str, task_id: str):
    """Return (answer_dict_or_None, missing_flag, status). missing != wrong."""
    path = workdir / "responses" / arm / f"{task_id}.json"
    if not path.exists():
        return None, True, "NO_RESPONSE_FILE"
    try:
        response = read_json(path)
    except Exception:
        return None, True, "UNPARSEABLE_RESPONSE"
    status = str(response.get("status") or "")
    answer = response.get("answer")
    if answer is None or status.startswith("EXECUTION_FAILED"):
        return None, True, status or "EMPTY_ANSWER"
    return answer, False, status


def _norm_coords(values):
    return {str(v).strip().lower() for v in values if str(v).strip().lower()}


def _mcnemar_exact(pairs):
    """pairs: list of (a_correct, b_correct). Returns (b, c, p_two_sided)."""
    b = sum(1 for a, bb in pairs if a and not bb)
    c = sum(1 for a, bb in pairs if not a and bb)
    n = b + c
    if n == 0:
        return b, c, 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(0, k + 1)) / (2.0**n)
    return b, c, min(1.0, 2.0 * tail)


def _holm(pvals):
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    m = len(pvals)
    adj = [0.0] * m
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, (m - rank) * pvals[idx])
        adj[idx] = min(1.0, running)
    return adj


def evaluate(workdir: Path, arms=None) -> None:
    arms = arms or ARMS
    oracle = read_json(workdir / "private_oracle.json")["answers"]
    task_ids = sorted(oracle)
    # Per-task per-arm scoring rows (missing != wrong).
    per_task = {}
    for task_id in task_ids:
        o = oracle[task_id]
        cls = o["class_id"]
        per_task[task_id] = {"class_id": cls}
        for arm in arms:
            answer, missing, status = _load_response(workdir, arm, task_id)
            if missing:
                per_task[task_id][arm] = {"missing": True, "status": status}
                continue
            decision_ok = answer.get("decision") == o["decision"]
            holds_true = answer.get("holds_across_contexts") is True
            coords = _norm_coords(answer.get("perspective_dependent_coordinates") or [])
            need = _norm_coords(o["perspective_dependent_coordinates"])
            comp_invalid = answer.get("comparison_valid") is False
            transport_valid = answer.get("transport_verdict") == "VALID"
            per_task[task_id][arm] = {
                "missing": False,
                "decision_ok": decision_ok,
                "false_universalization": holds_true and not o["holds_across_contexts"],
                "coord_recall": (len(coords & need) / len(need)) if need else None,
                "invalid_comparison_detected": comp_invalid,
                "transport_error": transport_valid and o["transport_verdict"] == "INVALID",
                "answer": answer,
            }
    write_json(workdir / "PER_TASK_SCORING.json", {"rows": per_task, "oracle": oracle})

    def rate(arm, field, pred):
        rows = [per_task[t][arm] for t in task_ids if not per_task[t][arm].get("missing")]
        sel = [r for r in rows if pred(r)]
        return (sum(1 for r in sel if r[field]) / len(sel)) if sel else None

    oracle_holds_false = lambda t: not oracle[t]["holds_across_contexts"]
    reversal = lambda t: oracle[t]["class_id"] in ("ELC2", "ELC3", "ELC4", "ELC5", "ELC8")
    elc7 = lambda t: oracle[t]["class_id"] == "ELC7"
    routing = lambda t: oracle[t]["class_id"] in ("ELC1", "ELC2", "ELC3", "ELC4", "ELC5")
    transport_invalid = lambda t: oracle[t]["transport_verdict"] == "INVALID"

    summary, resources = {}, {}
    for arm in arms:
        valid_rows = [per_task[t][arm] for t in task_ids if not per_task[t][arm].get("missing")]
        n_missing = sum(1 for t in task_ids if per_task[t][arm].get("missing"))
        receipts = []
        for t in task_ids:
            path = workdir / "responses" / arm / f"{t}.json"
            if path.exists():
                try:
                    receipts.append(read_json(path).get("resource_receipt") or {})
                except Exception:
                    pass
        tokens = sum(int(r.get("tokens") or 0) for r in receipts)
        calls = sum(int(r.get("model_calls") or 0) for r in receipts)
        wall = sum(float(r.get("wall_time_seconds") or 0) for r in receipts)
        summary[arm] = {
            "valid_responses": len(valid_rows),
            "missing_or_invalid": n_missing,
            "run_valid": n_missing == 0,
            "local_decision_correctness": rate(arm, "decision_ok", lambda r: True),
            "false_universalization_rate": _cond_rate(per_task, task_ids, arm, oracle_holds_false, "false_universalization"),
            "perspective_dependence_detection": _cond_mean(per_task, task_ids, arm, reversal, "coord_recall"),
            "invalid_comparison_detection": _cond_rate(per_task, task_ids, arm, elc7, "invalid_comparison_detected"),
            "method_routing_correctness": _cond_rate(per_task, task_ids, arm, routing, "decision_ok"),
            "cross_frame_transport_error": _cond_rate(per_task, task_ids, arm, transport_invalid, "transport_error"),
        }
        resources[arm] = {"model_calls": calls, "tokens_reported": tokens, "wall_time_seconds_sum": round(wall, 1)}
    evaluate_finish(workdir, arms, summary, resources, per_task, task_ids, oracle)


def _metric_indicator(per_task, task_ids, arm, metric, oracle):
    """Per-task 0/1 indicator used by McNemar: 1 = arm committed the protected
    success (correct decision) or avoided the protected error (critical rates)."""
    out = {}
    for t in task_ids:
        row = per_task[t][arm]
        if row.get("missing"):
            out[t] = None
            continue
        o = oracle[t]
        if metric == "local_decision_correctness":
            out[t] = 1 if row["decision_ok"] else 0
        elif metric == "false_universalization_rate":
            # protected success = did NOT false-universalize where oracle says local
            out[t] = (0 if row["false_universalization"] else 1) if not o["holds_across_contexts"] else None
        elif metric == "invalid_comparison_detection":
            if o["class_id"] != "ELC7":
                out[t] = None
            else:
                out[t] = 1 if row["invalid_comparison_detected"] else 0
        elif metric == "cross_frame_transport_error":
            out[t] = (0 if row["transport_error"] else 1) if o["transport_verdict"] == "INVALID" else None
        else:
            raise SuiteError(f"unknown metric {metric}")
    return out


def _contrasts(per_task, task_ids, oracle):
    tests = []
    for metric in METRIC_TESTS:
        loc = _metric_indicator(per_task, task_ids, LOCALITY, metric, oracle)
        for base in CONTRAST_BASES:
            other = _metric_indicator(per_task, task_ids, base, metric, oracle)
            pairs = [
                (loc[t] == 1, other[t] == 1)
                for t in task_ids
                if loc[t] is not None and other[t] is not None
            ]
            b, c, p = _mcnemar_exact(pairs)
            tests.append({
                "metric": metric,
                "locality_minus": base,
                "n_paired": len(pairs),
                "locality_only_success": b,
                "base_only_success": c,
                "p_exact_mcnemar": round(p, 6),
            })
    padj = _holm([t["p_exact_mcnemar"] for t in tests])
    for t, a in zip(tests, padj):
        t["p_holm"] = round(a, 6)
        t["significant_005"] = a < 0.05
    return tests


def _kill_rule(summary, resources):
    """Protocol kill condition, evaluated on point estimates, honestly."""
    if any(summary[a].get("run_valid") is not True for a in ARMS):
        return {"verdict": "INDETERMINATE_MISSING_RESPONSES",
                "note": "kill rule not evaluable with missing responses; missing != wrong"}
    others = CONTRAST_BASES
    critical = {
        m: {
            "locality": summary[LOCALITY][m],
            "best_other": min((summary[o][m] for o in others), key=lambda v: (v is None, v)),
        }
        for m in CRITICAL_METRICS
    }
    # false_universalization_rate and cross_frame_transport_error are error rates
    # (lower better); invalid_comparison_detection is a success rate (higher better).
    ERR = {"false_universalization_rate", "cross_frame_transport_error"}
    # Kill fires when, for EVERY critical metric, the best other arm matches or beats
    # LOCALITY (error rates: other <= locality; success rates: other >= locality)
    # and LOCALITY costs no more than 1.10x the cheapest other arm.
    protected_residual = False
    others_match_or_beat_all = True
    for m, vals in critical.items():
        loc, best = vals["locality"], vals["best_other"]
        if loc is None or best is None:
            others_match_or_beat_all = False
            continue
        if m in ERR:
            other_matches_or_beats = best <= loc
            locality_strictly_better = loc < best
        else:
            other_matches_or_beats = best >= loc
            locality_strictly_better = loc > best
        if locality_strictly_better:
            protected_residual = True
        if not other_matches_or_beats:
            others_match_or_beat_all = False
    loc_cost = resources[LOCALITY]["wall_time_seconds_sum"]
    other_cost = min(resources[o]["wall_time_seconds_sum"] for o in others)
    equal_or_lower_cost = loc_cost <= other_cost * 1.10
    if others_match_or_beat_all and equal_or_lower_cost:
        verdict = "INTERFACE_KILLED__CONTRACT_TO_DOCUMENTATION"
    elif protected_residual:
        verdict = "INTERFACE_PROTECTED_RESIDUAL"
    else:
        verdict = "LOCALITY_STRICTLY_WORSE_ON_A_CRITICAL_METRIC__NULL_TERMINAL"
    return {
        "verdict": verdict,
        "protected_residual_any_critical_metric": protected_residual,
        "others_match_or_beat_locality_on_all_critical": others_match_or_beat_all,
        "locality_cost_ratio_vs_cheapest_other": round(loc_cost / max(other_cost, 1e-9), 3),
        "parent_win_or_null_is_valid_terminal": True,
        "critical_point_estimates": critical,
    }


def evaluate_finish(workdir: Path, arms, summary, resources, per_task, task_ids, oracle):
    tests = _contrasts(per_task, task_ids, oracle)
    kill = _kill_rule(summary, resources)
    write_json(
        workdir / "EVALUATION_SUMMARY.json",
        {
            "schema_version": "orion.v2.el10-evaluation.v1",
            "suite": "EL10",
            "summary": summary,
            "resources": resources,
            "mcnemar_tests": tests,
            "kill_rule": kill,
            "missing_is_not_wrong": True,
            "authority": {
                "grants_scientific_truth": False,
                "grants_universal_intelligence_definition": False,
                "grants_primary_endpoint_change": False,
                "grants_evolution_eq_cognition": False,
                "parent_sufficiency_is_valid_terminal": True,
                "claim_limit": "interface discriminator only",
            },
        },
    )


def selftest(workdir: Path) -> None:
    """No-model structural self-test: oracle exactness, balance, custody files."""
    prepare(workdir, force=True)
    oracle = read_json(workdir / "private_oracle.json")["answers"]
    assert len(oracle) == 48, len(oracle)
    decisions = [o["decision"] for o in oracle.values()]
    assert decisions.count("FIRST") == 18 and decisions.count("SECOND") == 18
    assert decisions.count("PARETO_INCOMPARABLE") == 6 and decisions.count("COMPARISON_INVALID") == 6
    for cls, coord in (
        ("ELC2", ["environment_distribution"]), ("ELC3", ["scale"]),
        ("ELC4", ["timescale"]), ("ELC5", ["system_boundary"]),
    ):
        rows = [o for o in oracle.values() if o["class_id"] == cls]
        assert all(o["perspective_dependent_coordinates"] == coord for o in rows), cls
    elc7 = [o for o in oracle.values() if o["class_id"] == "ELC7"]
    assert all(o["comparison_valid"] is False for o in elc7)
    assert all(o["transport_verdict"] == "INVALID" for o in elc7)
    elc1 = [o for o in oracle.values() if o["class_id"] == "ELC1"]
    assert all(o["transport_verdict"] == "VALID" and o["holds_across_contexts"] for o in elc1)
    public = json.dumps(read_json(workdir / "public_tasks.json"))
    assert "ELC" not in public.replace("el10-", ""), "class_id leaked into public tasks"
    counts = {}
    for o in oracle.values():
        counts[o["class_id"]] = counts.get(o["class_id"], 0) + 1
    assert all(v == 6 for v in counts.values()), counts
    # Independent winner-consistency audit: the registered value of the class's
    # flipping coordinate must appear in the WINNING method's registry fact line,
    # parsed from public text only (this is what catches registry/context flips).
    tasks = {t["task_id"]: t for t in read_json(workdir / "public_tasks.json")["tasks"]}
    flip_coord = {"ELC2": "environment_distribution", "ELC3": "scale",
                  "ELC4": "timescale", "ELC5": "system_boundary"}
    checked = 0
    for tid, o in oracle.items():
        cls = o["class_id"]
        if cls not in flip_coord:
            continue
        text = tasks[tid]["scenario_text"]
        ctx_lines = text.split("REGISTERED CONTEXT", 1)[1].split("COUNTERFACTUAL", 1)[0]
        reg_val = None
        for line in ctx_lines.splitlines():
            if line.strip().startswith(f"- {flip_coord[cls]}:"):
                reg_val = line.split(":", 1)[1].strip()
                break
        assert reg_val, (tid, "registered value not found")
        # registry block lines for FIRST and SECOND
        reg_block = text.split("METHOD REGISTRY", 1)[1].split("REGISTERED CONTEXT", 1)[0]
        lines = [l for l in reg_block.splitlines() if l.strip().startswith(("-", "FIRST", "SECOND"))]
        first_line, second_line = lines[0], lines[1]
        # ELC4 registered long budget -> winner is the slow crosser (fact mentions "needs")
        winner_line = first_line if o["decision"] == "FIRST" else second_line
        if cls == "ELC4":
            assert "needs" in winner_line or "crosses" in winner_line, (tid, winner_line)
        else:
            key = reg_val.split(":")[-1].strip()
            assert key and key in winner_line, (tid, key, winner_line)
        checked += 1
    assert checked == 24, checked
    print("SELFTEST_OK", counts, "winner_consistency_checked", checked)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="EL10 epistemic-locality suite")
    parser.add_argument("command", choices=["prepare", "dispatch", "evaluate", "selftest"])
    parser.add_argument("workdir", type=Path)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args.workdir, force=args.force)
        print(f"prepared {args.workdir}")
    elif args.command == "dispatch":
        dispatch(args.workdir, concurrency=args.concurrency, overwrite=args.overwrite)
        print("dispatch complete")
    elif args.command == "evaluate":
        evaluate(args.workdir)
        print("evaluation complete")
    elif args.command == "selftest":
        selftest(args.workdir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""AH20 epistemic-atlas / horizon suite runner (prospective custody, gold-blind).

prepare: build_suite() (48 EL10 worlds re-derived byte-identical under EL10's
own seed + 30 new seeded worlds, all machine-cross-checked against the
AH10-green module) -> public_tasks.json + private_oracle.json + per-arm
requests; FROZEN_SUITE.json freeze record incl. the GR10/MX20 reuse ledger.
dispatch: hash-commit + REMOVE the private oracle before any arm runs, run
arms with ORION_GOLD_ACCESS=NONE, restore + verify in finally.
evaluate: missing != wrong; per-arm metric vector; paired exact McNemar x16
with Holm correction; kill rule K1-K5 (+ CONTROL_DIVERGENT) on point
estimates; false_outside_atlas_rate with exact Clopper-Pearson CI.
selftest: no-model structural audit (oracle exactness, balance, witness
discipline, leak checks, winner-consistency parsed from public text).

Freeze doc: research/experiments/EPISTEMIC_ATLAS_HORIZON_AH20_SUITE_FREEZE_V1.md
(V1 FROZEN 2026-08-30; canonical paper anchor V14, PR #112).
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
from orion_ah20_cases import (  # noqa: E402
    AH_CLASSES,
    AH_SEED,
    EL10_CLASSES,
    EL10_SEED,
    GLUING_BALANCE,
    build_suite,
    verify_suite,
)

ROOT = Path(__file__).resolve().parents[1]
ARMS = [
    "SIMPLE_NATIVE",
    "CURRENT_F0",
    "CURRENT_F2",
    "PARENT_LOCAL_GLOBAL",
    "F2_PLUS_ATLAS_HORIZON",
]
INTERFACE = "F2_PLUS_ATLAS_HORIZON"
CONTRAST_BASES = ["SIMPLE_NATIVE", "CURRENT_F0", "CURRENT_F2", "PARENT_LOCAL_GLOBAL"]
TASK_COUNT = 78
# Freeze section 5 metric denominators (class -> count: 6 each).
FALSE_GLOBALIZATION_CLASSES = ["AHC1", "ELC2", "ELC3", "ELC4", "ELC5", "ELC8"]  # 36
TRANSPORT_CLASSES = ["ELC2", "ELC3", "ELC4", "ELC5", "ELC7", "ELC8"]  # 36
PROBE_CLASSES = ["AHC2", "AHC3"]  # 12
LOCAL_SCOPE_CLASSES = ["AHC0", "ELC1"]  # 12
SENTINEL_CLASSES = ["AHC4"]  # 6; false_outside_atlas denominator = 78 - 6 = 72
CRITICAL_METRICS = [
    "gluing_disposition_correctness",
    "false_globalization_rate",
    "transport_correctness",
    "probe_selection_correctness",
]
NON_COMPENSATORY = ["false_globalization_rate", "false_outside_atlas_rate"]
METRIC_TESTS = CRITICAL_METRICS  # 4 metrics x 4 contrast bases = 16 McNemar tests


class SuiteError(RuntimeError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False) + "\n")


def read_json(path: Path):
    return json.loads(path.read_text())


def reuse_ledger() -> dict:
    """GR10/MX20 deferred reuse slots, re-checked at prepare AND dispatch.

    The backlog lists EL10/GR10/MX20 as required reuse. Only EL10 has a frozen
    executed suite; if a GR10/MX20 suite freezes before dispatch, identity
    matching must happen through a new prepare (never silently skipped).
    """
    ledger = {}
    experiments = ROOT / "research" / "experiments"
    for key, needle in (("GR10", "gr10"), ("MX20", "mx20")):
        hits = [
            p
            for p in experiments.glob(f"**/*{needle}*")
            if p.is_file() and p.suffix in (".json", ".md") and "FROZEN" in p.name.upper()
        ]
        executed = [
            p
            for p in (experiments / "results").glob(f"**/*{needle}*")
            if p.is_dir() and (p / "FROZEN_SUITE.json").exists()
        ]
        if hits or executed:
            ledger[key] = {
                "status": "SUITE_FROZEN_REQUIRES_IDENTITY_MATCH_REREAD",
                "freeze_docs": [str(p.relative_to(ROOT)) for p in hits],
                "executed_suites": [str(p.relative_to(ROOT)) for p in executed],
            }
        else:
            ledger[key] = {"status": "CANNOT_REUSE__SUITE_NOT_FROZEN"}
    ledger["EL10"] = {
        "status": "REUSED_BYTE_IDENTICAL",
        "source": "research/experiments/results/issue104/el10-r1",
        "seed": EL10_SEED,
        "tasks": 48,
    }
    return ledger


def prepare(workdir: Path, arms=None, force: bool = False) -> None:
    arms = arms or ARMS
    if workdir.exists():
        if not force:
            raise SuiteError(f"workdir exists: {workdir}")
        shutil.rmtree(workdir)
    public_tasks, oracle_rows = build_suite()
    report = verify_suite(public_tasks, oracle_rows)
    assert report["tasks"] == TASK_COUNT and report["gluing"] == GLUING_BALANCE
    public_by_id = {t["task_id"]: t for t in public_tasks}
    private_answers = {r["task_id"]: r for r in oracle_rows}
    for task_id, task in public_by_id.items():
        for arm in arms:
            write_json(
                workdir / "requests" / arm / f"{task_id}.json",
                {
                    "schema_version": "orion.v2.ah20-request.v1",
                    "task_id": task_id,
                    "arm_id": arm,
                    "task": task,
                    "scientific_truth_authorized": False,
                    "publication_readiness_authorized": False,
                },
            )
    write_json(
        workdir / "public_tasks.json",
        {"schema_version": "orion.v2.ah20-public.v1", "tasks": public_tasks},
    )
    write_json(
        workdir / "private_oracle.json",
        {"schema_version": "orion.v2.ah20-private.v1", "answers": private_answers},
    )
    write_json(
        workdir / "FROZEN_SUITE.json",
        {
            "schema_version": "orion.v2.ah20-freeze.v1",
            "suite": "AH20",
            "seed_new_cases": AH_SEED,
            "seed_el10_reuse": EL10_SEED,
            "classes_new": AH_CLASSES,
            "classes_reused": EL10_CLASSES,
            "task_count": len(public_tasks),
            "arms": arms,
            "private_oracle_visible_to_solver": False,
            "answer_contract": (
                "decision|gluing_disposition|global_section_witness_id|holds_across_contexts|"
                "transport_verdict|probe_decision|probe_id|horizon_disposition|"
                "outside_atlas_witness_id|brief_rationale"
            ),
            "reuse_ledger": reuse_ledger(),
            "executor_note": (
                "primary codex-cli gpt-5.6-terra; anthropic Messages-API fallback admissible "
                "for the whole suite only if the primary is dead before any arm starts, never "
                "mixed per-arm within a run (mixed executors force run_valid=false)"
            ),
            "authority": {
                "grants_scientific_truth": False,
                "grants_total_epistemic_space": False,
                "grants_absolute_globality": False,
                "grants_new_kernel_family": False,
                "grants_paper_endpoint_change": False,
                "parent_sufficiency_is_valid_terminal": True,
                "claim_limit": "formal/interface discriminator only",
            },
        },
    )


def command_prefix() -> list:
    override = os.environ.get("ORION_AH_ARM_COMMAND", "").strip()
    if override:
        import shlex

        return shlex.split(override)
    return [sys.executable, str(ROOT / "scripts/orion_epistemic_atlas_arms.py")]


def dispatch(workdir: Path, arms=None, concurrency: int = 4, overwrite: bool = False) -> None:
    arms = arms or ARMS
    private = workdir / "private_oracle.json"
    if not private.exists():
        raise SuiteError("missing private oracle")
    # Re-check the deferred reuse slots at dispatch (freeze section 8 OQ1).
    frozen = read_json(workdir / "FROZEN_SUITE.json")
    now = reuse_ledger()
    for key in ("GR10", "MX20"):
        if frozen["reuse_ledger"][key]["status"] != now[key]["status"]:
            raise SuiteError(
                f"{key} reuse status changed between prepare and dispatch "
                f"({frozen['reuse_ledger'][key]['status']} -> {now[key]['status']}); "
                "identity matching requires a fresh prepare"
            )
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
            timeout=int(os.environ.get("ORION_AH_TIMEOUT", "1800")),
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


def _binom_cdf(k: int, n: int, p: float) -> float:
    return sum(math.comb(n, i) * (p**i) * ((1 - p) ** (n - i)) for i in range(0, k + 1))


def _clopper_pearson(k: int, n: int, alpha: float = 0.05):
    """Exact two-sided Clopper-Pearson CI by bisection, stdlib only.

    lower = 0 if k == 0 else largest p with P(X >= k | p) >= alpha/2
    upper = 1 if k == n else largest p with P(X <= k | p) >= alpha/2
    """
    if n == 0:
        return None, None

    def bisect_dec(pred) -> float:
        # pred must be non-increasing in p; returns the largest p with pred true.
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if pred(mid):
                lo = mid
            else:
                hi = mid
        return round((lo + hi) / 2, 6)

    # P(X >= k | p) increases in p -> lower bound is the boundary p*, i.e. the
    # largest p at which k-or-more is still at the alpha/2 surprise level.
    lower = 0.0 if k == 0 else bisect_dec(lambda p: (1.0 - _binom_cdf(k - 1, n, p)) <= alpha / 2)
    # P(X <= k | p) decreases in p -> upper = largest p with CDF(k|p) >= alpha/2.
    upper = 1.0 if k == n else bisect_dec(lambda p: _binom_cdf(k, n, p) >= alpha / 2)
    return lower, upper


def score_row(answer: dict, o: dict) -> dict:
    """Per-task per-arm scoring. Oracle o carries the 10 contract fields."""
    cls = o["class_id"]
    claims_global = (
        answer.get("holds_across_contexts") is True
        or answer.get("gluing_disposition") == "GLOBAL_SECTION_WITNESSED"
        or answer.get("transport_verdict") == "VALID"
    )
    oracle_global = (
        o["holds_across_contexts"] is True
        or o["gluing_disposition"] == "GLOBAL_SECTION_WITNESSED"
        or o["transport_verdict"] == "VALID"
    )
    witnessed = answer.get("gluing_disposition") == "GLOBAL_SECTION_WITNESSED"
    witness_ok = bool(str(answer.get("global_section_witness_id") or "").strip()) == witnessed
    outside = answer.get("horizon_disposition") == "OUTSIDE_CURRENT_ATLAS"
    outside_ok = bool(str(answer.get("outside_atlas_witness_id") or "").strip()) == outside
    decision_applicable = o["decision"] != "NOT_APPLICABLE"
    return {
        "missing": False,
        "decision_ok": (answer.get("decision") == o["decision"]) if decision_applicable else None,
        "gluing_ok": answer.get("gluing_disposition") == o["gluing_disposition"] and witness_ok,
        "false_globalization": claims_global and not oracle_global,
        "transport_error": answer.get("transport_verdict") == "VALID" and o["transport_verdict"] == "INVALID",
        "probe_ok": (
            answer.get("probe_decision") == o["probe_decision"]
            and str(answer.get("probe_id") or "") == o["probe_id"]
        ) if cls in PROBE_CLASSES else None,
        "refinement_ok": (
            answer.get("horizon_disposition") == o["horizon_disposition"]
        ) if cls in PROBE_CLASSES else None,
        "false_outside_atlas": outside and cls not in SENTINEL_CLASSES,
        # AHC0 must stay local: correct seeded decision AND no global claim.
        # ELC1's registered global section IS witnessed (scoped to the sweep
        # envelope): the correct behaviour is the witnessed claim, not abstention.
        "local_scope_ok": (
            (
                answer.get("decision") == o["decision"]
                and not claims_global
            )
            if cls == "AHC0"
            else (
                answer.get("decision") == o["decision"]
                and answer.get("gluing_disposition") == "GLOBAL_SECTION_WITNESSED"
                and witness_ok
            )
            if cls == "ELC1"
            else None
        ),
        "answer": answer,
    }


def evaluate(workdir: Path, arms=None) -> None:
    arms = arms or ARMS
    oracle = read_json(workdir / "private_oracle.json")["answers"]
    task_ids = sorted(oracle)
    per_task, executors = {}, set()
    for task_id in task_ids:
        o = oracle[task_id]
        cls = o["class_id"]
        per_task[task_id] = {"class_id": cls}
        for arm in arms:
            answer, missing, status = _load_response(workdir, arm, task_id)
            if missing:
                per_task[task_id][arm] = {"missing": True, "status": status}
                continue
            per_task[task_id][arm] = score_row(answer, o)
            path = workdir / "responses" / arm / f"{task_id}.json"
            try:
                executors.add(read_json(path).get("resource_receipt", {}).get("executor"))
            except Exception:
                executors.add(None)
    write_json(workdir / "PER_TASK_SCORING.json", {"rows": per_task, "oracle": oracle})

    def rate(arm, field, classes, value=True):
        rows = [
            per_task[t][arm]
            for t in task_ids
            if oracle[t]["class_id"] in classes and not per_task[t][arm].get("missing")
        ]
        if not rows:
            return None
        return sum(1 for r in rows if r.get(field) is value) / len(rows)

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
        fg = rate(arm, "false_globalization", FALSE_GLOBALIZATION_CLASSES)
        te = rate(arm, "transport_error", TRANSPORT_CLASSES)
        n_foa = sum(
            1
            for t in task_ids
            if oracle[t]["class_id"] not in SENTINEL_CLASSES
            and not per_task[t][arm].get("missing")
        )
        k_foa = sum(
            1
            for t in task_ids
            if oracle[t]["class_id"] not in SENTINEL_CLASSES
            and not per_task[t][arm].get("missing")
            and per_task[t][arm].get("false_outside_atlas")
        )
        ci = _clopper_pearson(k_foa, n_foa)
        summary[arm] = {
            "valid_responses": len(valid_rows),
            "missing_or_invalid": n_missing,
            "run_valid": n_missing == 0 and len(executors) == 1,
            "executors_seen": sorted(str(e) for e in executors),
            "local_scope_correctness": rate(arm, "local_scope_ok", LOCAL_SCOPE_CLASSES),
            "false_globalization_rate": fg,
            "gluing_disposition_correctness": rate(arm, "gluing_ok", AH_CLASSES + EL10_CLASSES),
            "transport_correctness": (1 - te) if te is not None else None,
            "probe_selection_correctness": rate(arm, "probe_ok", PROBE_CLASSES),
            "decision_relevant_partition_refinement": rate(arm, "refinement_ok", PROBE_CLASSES),
            "false_outside_atlas_rate": (k_foa / n_foa) if n_foa else None,
            "false_outside_atlas_exact_ci95": ci,
        }
        resources[arm] = {"model_calls": calls, "tokens_reported": tokens, "wall_time_seconds_sum": round(wall, 1)}
    evaluate_finish(workdir, arms, summary, resources, per_task, task_ids, oracle)


def _metric_indicator(per_task, task_ids, arm, metric, oracle):
    """Per-task 0/1 indicator for McNemar: 1 = protected success on this task."""
    out = {}
    for t in task_ids:
        row = per_task[t][arm]
        if row.get("missing"):
            out[t] = None
            continue
        cls = oracle[t]["class_id"]
        if metric == "gluing_disposition_correctness":
            out[t] = 1 if row["gluing_ok"] else 0
        elif metric == "false_globalization_rate":
            out[t] = (0 if row["false_globalization"] else 1) if cls in FALSE_GLOBALIZATION_CLASSES else None
        elif metric == "transport_correctness":
            out[t] = (0 if row["transport_error"] else 1) if cls in TRANSPORT_CLASSES else None
        elif metric == "probe_selection_correctness":
            out[t] = row["probe_ok"] if cls in PROBE_CLASSES else None
            if out[t] is not None:
                out[t] = 1 if out[t] else 0
        else:
            raise SuiteError(f"unknown metric {metric}")
    return out


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


def _contrasts(per_task, task_ids, oracle):
    tests = []
    for metric in METRIC_TESTS:
        iface = _metric_indicator(per_task, task_ids, INTERFACE, metric, oracle)
        for base in CONTRAST_BASES:
            other = _metric_indicator(per_task, task_ids, base, metric, oracle)
            pairs = [
                (iface[t] == 1, other[t] == 1)
                for t in task_ids
                if iface[t] is not None and other[t] is not None
            ]
            b, c, p = _mcnemar_exact(pairs)
            tests.append({
                "metric": metric,
                "interface_minus": base,
                "n_paired": len(pairs),
                "interface_only_success": b,
                "base_only_success": c,
                "p_exact_mcnemar": round(p, 6),
            })
    padj = _holm([t["p_exact_mcnemar"] for t in tests])
    for t, a in zip(tests, padj):
        t["p_holm"] = round(a, 6)
        t["significant_005"] = a < 0.05
    return tests


def _control_divergent(per_task, task_ids, oracle):
    """Invariance sentinel: arms must agree on AHC0 (the control class)."""
    control = [t for t in task_ids if oracle[t]["class_id"] == "AHC0"]
    signatures = {}
    for arm in ARMS:
        signature = tuple(
            (per_task[t][arm].get("local_scope_ok") is True) if not per_task[t][arm].get("missing") else None
            for t in sorted(control)
        )
        signatures[arm] = signature
    if len({tuple(s) for s in signatures.values()}) == 1:
        return None
    return {"arms_ahc0_local_scope_signatures": signatures}


def _kill_rule(summary, resources, per_task, task_ids, oracle):
    """Freeze section 6, evaluated on point estimates, honestly."""
    if any(summary[a].get("run_valid") is not True for a in ARMS):
        mixed = sorted({tuple(summary[a].get("executors_seen") or []) for a in ARMS})
        return {
            "verdict": "INDETERMINATE_MISSING_RESPONSES",
            "note": "kill rule not evaluable with missing responses or mixed executors; missing != wrong",
            "executors_mix": mixed,
        }
    control = _control_divergent(per_task, task_ids, oracle)
    if control is not None:
        return {
            "verdict": "CONTROL_DIVERGENT",
            "note": "arms disagree on the AHC0 invariance control; a null here is not evidence about the interface",
            **control,
        }
    others = CONTRAST_BASES
    # Error rates (lower better): false_globalization_rate, false_outside_atlas_rate.
    # Success rates (higher better): gluing, transport, probe.
    def strictly_worse_noncomp(arm):
        for m in NON_COMPENSATORY:
            iface, other = summary[INTERFACE][m], summary[arm][m]
            if iface is None or other is None:
                continue
            if other < iface:  # other arm's error rate strictly lower
                return m
        return None
    for arm in ("CURRENT_F2", "PARENT_LOCAL_GLOBAL"):
        m = strictly_worse_noncomp(arm)
        if m:
            return {
                "verdict": "INTERFACE_KILLED__NON_COMPENSATORY",
                "worse_than": arm,
                "metric": m,
                "interface_rate": summary[INTERFACE][m],
                "other_rate": summary[arm][m],
                "note": "false global-section claims / false OUTSIDE_CURRENT_ATLAS calls are non-compensatory",
            }
    ERR = set(NON_COMPENSATORY)
    others_match_or_beat_all = True
    interface_strictly_better = False
    other_strictly_better = None
    critical = {}
    for m in CRITICAL_METRICS:
        iface = summary[INTERFACE][m]
        # Error rates: best other = lowest; success rates: best other = highest.
        vals = [summary[o][m] for o in others if summary[o][m] is not None]
        best = (min(vals) if m in ERR else max(vals)) if vals else None
        critical[m] = {"interface": iface, "best_other": best}
        if iface is None or best is None:
            others_match_or_beat_all = False
            continue
        if m in ERR:
            other_matches_or_beats = best <= iface
            iface_better = iface < best
            other_better = best < iface
        else:
            other_matches_or_beats = best >= iface
            iface_better = iface > best
            other_better = best > iface
        if iface_better:
            interface_strictly_better = True
        if not other_matches_or_beat_all:
            others_match_or_beat_all = False
        if other_better:
            for o in others:
                if summary[o][m] is not None and (
                    summary[o][m] < iface if m in ERR else summary[o][m] > iface
                ):
                    other_strictly_better = (o, m, summary[o][m])
                    break
    iface_cost = resources[INTERFACE]["wall_time_seconds_sum"]
    cheapest_other = min(resources[o]["wall_time_seconds_sum"] for o in others)
    cost_ok = iface_cost <= cheapest_other * 1.10
    if others_match_or_beat_all and cost_ok:
        verdict = "INTERFACE_KILLED__CONTRACT_TO_DOCUMENTATION"
    elif interface_strictly_better:
        verdict = "INTERFACE_PROTECTED_RESIDUAL"
    elif other_strictly_better:
        verdict = "F2_PLUS_ATLAS_HORIZON_STRICTLY_WORSE_ON_A_CRITICAL_METRIC__NULL_TERMINAL"
    else:
        verdict = "INTERFACE_NULL__CRITICAL_METRIC_TIES"
    return {
        "verdict": verdict,
        "others_match_or_beat_interface_on_all_critical": others_match_or_beat_all,
        "interface_strictly_better_on_a_critical_metric": interface_strictly_better,
        "other_strictly_better_on_a_critical_metric": other_strictly_better,
        "interface_cost_ratio_vs_cheapest_other": round(iface_cost / max(cheapest_other, 1e-9), 3),
        "parent_win_or_null_is_valid_terminal": True,
        "critical_point_estimates": critical,
    }


def evaluate_finish(workdir: Path, arms, summary, resources, per_task, task_ids, oracle):
    tests = _contrasts(per_task, task_ids, oracle)
    kill = _kill_rule(summary, resources, per_task, task_ids, oracle)
    write_json(
        workdir / "EVALUATION_SUMMARY.json",
        {
            "schema_version": "orion.v2.ah20-evaluation.v1",
            "suite": "AH20",
            "summary": summary,
            "resources": resources,
            "mcnemar_tests": tests,
            "kill_rule": kill,
            "missing_is_not_wrong": True,
            "authority": {
                "grants_scientific_truth": False,
                "grants_total_epistemic_space": False,
                "grants_absolute_globality": False,
                "grants_new_kernel_family": False,
                "grants_paper_endpoint_change": False,
                "parent_sufficiency_is_valid_terminal": True,
                "claim_limit": "formal/interface discriminator only",
            },
        },
    )


def selftest(workdir: Path) -> None:
    """No-model structural self-test: oracle exactness, custody shape, leaks."""
    prepare(workdir, force=True)
    oracle = read_json(workdir / "private_oracle.json")["answers"]
    assert len(oracle) == TASK_COUNT, len(oracle)
    counts = {}
    for o in oracle.values():
        counts[o["class_id"]] = counts.get(o["class_id"], 0) + 1
    assert all(v == 6 for v in counts.values()) and len(counts) == 13, counts
    gluing = {}
    for o in oracle.values():
        gluing[o["gluing_disposition"]] = gluing.get(o["gluing_disposition"], 0) + 1
    assert gluing == GLUING_BALANCE, gluing
    # Witness-id discipline in the oracle itself.
    for tid, o in oracle.items():
        witnessed = o["gluing_disposition"] == "GLOBAL_SECTION_WITNESSED"
        assert bool(o["global_section_witness_id"].strip()) == witnessed, tid
        outside = o["horizon_disposition"] == "OUTSIDE_CURRENT_ATLAS"
        assert bool(o["outside_atlas_witness_id"].strip()) == outside, tid
    elc1 = [o for o in oracle.values() if o["class_id"] == "ELC1"]
    assert all(o["gluing_disposition"] == "GLOBAL_SECTION_WITNESSED" and o["global_section_witness_id"] for o in elc1)
    elc7 = [o for o in oracle.values() if o["class_id"] == "ELC7"]
    assert all(o["gluing_disposition"] == "CANNOT_CHECK" for o in elc7)
    ahc4 = [o for o in oracle.values() if o["class_id"] == "AHC4"]
    assert all(o["horizon_disposition"] == "OUTSIDE_CURRENT_ATLAS" and o["outside_atlas_witness_id"] for o in ahc4)
    # Public/private separation: no class identity, enum value or oracle field
    # name may appear in public tasks.
    public = read_json(workdir / "public_tasks.json")
    public_text = json.dumps(public)
    assert "AHC" not in public_text.replace("ah20-", ""), "class_id leaked into public tasks"
    assert "ELC" not in public_text.replace("el10-", ""), "class_id leaked into public tasks"
    for leak in (
        "GLOBAL_SECTION_WITNESSED", "MATCHING_FAMILY_ONLY", "GLOBAL_SECTION_OBSTRUCTED",
        "CANNOT_CHECK", "PROBE_REFINES_HORIZON", "NO_DISTINGUISHABILITY_GAIN",
        "BROKEN_CANDIDATE_UNIVERSE", "OUTSIDE_CURRENT_ATLAS", "NOT_APPLICABLE",
        "gluing_disposition", "horizon_disposition",
    ):
        assert leak not in public_text, leak
    # Winner-consistency audit parsed from public text only.
    tasks = {t["task_id"]: t for t in public["tasks"]}
    checked = 0
    for tid, o in oracle.items():
        cls = o["class_id"]
        text = tasks[tid]["scenario_text"]
        if cls == "AHC0":
            reg_block = text.split("METHOD REGISTRY", 1)[1]
            lines = [l for l in reg_block.splitlines() if l.strip().startswith("-")]
            first_line, second_line = lines[0], lines[1]
            winner_line = first_line if o["decision"] == "FIRST" else second_line
            assert "strict dominance" in winner_line, (tid, winner_line)
            assert o["decision"] in ("FIRST", "SECOND")
            checked += 1
        elif cls == "AHC2":
            assert o["probe_id"] and f"- {o['probe_id']}:" in text, tid
            checked += 1
        elif cls == "AHC3":
            assert "probe-q1" in text and o["probe_decision"] == "REJECT", tid
            checked += 1
        elif cls == "AHC4":
            assert o["outside_atlas_witness_id"] in text, tid
            assert "RESIDUAL DISPOSITION LEDGER" in text, tid
            checked += 1
        elif cls == "AHC1":
            assert "GLOBAL SECTION WITNESS REGISTRY: NONE registered" in text, tid
            checked += 1
    assert checked == 30, checked
    # Freeze record shape.
    frozen = read_json(workdir / "FROZEN_SUITE.json")
    assert frozen["task_count"] == TASK_COUNT and len(frozen["arms"]) == 5
    assert frozen["reuse_ledger"]["EL10"]["status"] == "REUSED_BYTE_IDENTICAL"
    for key in ("GR10", "MX20"):
        assert frozen["reuse_ledger"][key]["status"].startswith("CANNOT_REUSE") or \
            frozen["reuse_ledger"][key]["status"].startswith("SUITE_FROZEN"), key
    # Clopper-Pearson sanity: known bounds.
    lo, hi = _clopper_pearson(0, 72)
    assert lo == 0.0 and 0.04 < hi < 0.06, (lo, hi)
    lo, hi = _clopper_pearson(72, 72)
    assert hi == 1.0 and 0.94 < lo < 0.96, (lo, hi)
    print("SELFTEST_OK", counts, "gluing", gluing, "winner_consistency_checked", checked)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="AH20 epistemic-atlas / horizon suite")
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

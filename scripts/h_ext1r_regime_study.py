#!/usr/bin/env python3
"""H-EXT-1R: a regime where the evidence-structure gate FIRES and the strongest parent is
OFF CEILING -- constructed from the protocol semantics, then tested for existence on a
development split before anything is registered.

Why this study exists
---------------------
H-EXT-1P closed pre-freeze with ``REGISTERED_CONTRAST_CANNOT_BE_ABOUT_THE_MECHANISM``:
on every task where the frozen gate ``G_B_PLUS_XREF`` activates, ``GATED_M`` and the
strongest parent are both perfect (170/170 vs 170/170 prospectively, 72/72 vs 72/72 on
the held-out retrospective cell), so the mechanism-attributable contrast has zero
discordant pairs and no n confers power.  The closure attributes the wall to ONE stage,
the task suite, and names the lever: *a suite in which the dependence machinery has a
cost or an error the parent does not also avoid*, established on a development split
before any comparison, or no successor freezes.

This is that construction.  Each new stratum carries a **visible provenance witness** --
two records with one ``lineage_root`` -- so the frozen gate activates on every task by
construction (asserted mechanically, with a no-witness control task that must read
``False``), and a **latent dependence** the witness does not reveal, on which the
registered rule's answer turns.  Paired control strata carry the same visible witness
structure and NO latent dependence, so the correct answer is not a function of the
witness (``STRUCTURALLY_DETERMINED_REGISTERED_CLAUSE`` guard: both verdicts reachable
under identical gate input).

Two mechanisms, each with its control (study ``PD-S5-WITNESSED-LATENT-DEPENDENCE``):

* ``PDS5A_WITNESS_PLUS_LATENT_CONVENTION`` (S1 rule, verbatim from the frozen suite):
  five items; e1/e2 share a root (the witness); e3 introduces a calibration
  convention that e4 and e5 adopt **by name, without naming e3's root**.  Independent
  singly-sufficient families: {e1,e2}, {e3,e4,e5} = 2 -> INCONCLUSIVE.  Provenance
  and declared-overlap reasoning alone counts 4 -> ACCEPT_H.
  ``PDS5B_WITNESS_PLUS_INDEPENDENT`` (control): same shape, e3/e4/e5 each on their
  own convention -> 4 families -> ACCEPT_H.
* ``PDS5C_LATENT_LINEAGE_REVOCATION`` (a registered reopening rule that makes lineage
  explicit -- see ``S5_LINEAGE_RULE`` -- given verbatim to every arm): i2/i3 share a
  root (the witness); i4's calibration runs through a transfer curve i1 publishes,
  named by the curve, not by i1's root or id.  i1 fails.  C1 (families A,B) is
  PRESERVED, C2 (family C, whose lineage includes i1) REOPENS.  Root-only reasoning
  preserves both.
  ``PDS5D_SELF_CALIBRATED_REVOCATION`` (control): i4 self-calibrated -> both preserved.

What is decided BEFORE any model runs (this file, frozen by sha256 in the design):

* the feasibility clause F1 that licenses registration: on the development split the
  strongest parent's accuracy on the two treatment strata is at most
  ``PARENT_OFF_CEILING_MAX`` (0.85); otherwise the terminal is
  ``REGIME_NOT_REALISED__PARENT_AT_CEILING_ON_WITNESSED_LATENT_TASKS`` (a
  CANNOT_CHECK-class terminal) and NO protected run is dispatched;
* the protected gates, statistic (exact two-sided McNemar on discordant pairs, the
  quantity the closure said drives power), routing and terminals.

In this regime ``GATED_M`` **is** ``M`` on every task (the gate fires everywhere), so the
registered contrast is literally the mechanism-attributable one the closure named:
always-on ``P_D_FULL`` against ``STRONGEST_ASSURANCE_FEDERATION`` on gate-active tasks,
with ``P_D_MINUS_DEPENDENCE`` as the attribution control.

Substrate: the H-EXT-1 prospective cell ran gpt-5.5 through the codex CLI.  That channel
is not available to this lane at freeze time, so H-EXT-1R runs on the registered
Anthropic-compatible channel E30-R13 pinned (served ``glm-5.3``, request-body contract
``thinking_disabled``), through ``scripts/h_ext1r_pd_arms.py`` with a per-envelope channel
receipt and a served-model assertion.  A different substrate from H-EXT-1 is disclosed
as such; all three arms are paired on the same substrate, which is what the contrast needs.

Everything the frozen suite defines is imported READ-ONLY: ``make_item``, ``token``,
``S1_RULE`` and the request/oracle schema from
``scripts/run_dependence_evidence_generated_suite.py``; ``dispatch`` from the FM/FG
harness; ``witness_features`` / ``gate_fires`` from ``scripts/h_ext1_gate_study.py``
(the gate is not re-implemented), and the gate id from ``H_EXT1_GATE_FREEZE.json``.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import random
import shutil
import sys
import time
from math import comb
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "research" / "experiments" / "h-ext1r"
GATE_FREEZE = ROOT / "research" / "experiments" / "h-ext1" / "H_EXT1_GATE_FREEZE.json"
DESIGN_JSON = HERE / "H_EXT1R_REGIME_DESIGN_V1.json"
AUTH_FILE = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
AUTH_USED = HERE / "PROTECTED_RUN_AUTHORIZATION_USED_V1.json"
DEFAULT_SEED_FILE = Path.home() / ".orion-custody" / "h-ext1r" / "PROTECTED_SEED_V1.txt"

STUDY_ID = "PD-S5-WITNESSED-LATENT-DEPENDENCE"
STUDY_SLUG = "pd-s5"
ARM_M = "P_D_FULL"
ARM_OFF = "P_D_MINUS_DEPENDENCE"
ARM_PARENT = "STRONGEST_ASSURANCE_FEDERATION"
ARMS = (ARM_M, ARM_OFF, ARM_PARENT)
TREATMENT = ("PDS5A_WITNESS_PLUS_LATENT_CONVENTION", "PDS5C_LATENT_LINEAGE_REVOCATION")
CONTROL = ("PDS5B_WITNESS_PLUS_INDEPENDENT", "PDS5D_SELF_CALIBRATED_REVOCATION")
STRATA = (TREATMENT[0], CONTROL[0], TREATMENT[1], CONTROL[1])
PAIRS = ((TREATMENT[0], CONTROL[0]), (TREATMENT[1], CONTROL[1]))

DEV_SEED = 20260904
DEV_PER_STRATUM = 20
PROTECTED_PER_STRATUM = 50
PARENT_OFF_CEILING_MAX = 0.85          # F1: registration requires parent <= this on treatment (dev)
ALPHA = 0.05

INCONCLUSIVE = "INCONCLUSIVE_INSUFFICIENT_INDEPENDENT_SUPPORT"
S5_LINEAGE_RULE = (
    "Registered reopening rule: a claim REOPENS iff every one of its support families is "
    "destroyed by the failure event; otherwise the claim is PRESERVED. A family is destroyed "
    "when the failed item is in that family's lineage. An item's lineage includes every item "
    "whose data, calibration or transfer products its method text states it relies on, "
    "whether or not the two items share a lineage root; items sharing a lineage root are one family."
)
TERMINALS = (
    "CANNOT_CHECK_RUN_INVALID",
    "REGIME_NOT_REALISED__PARENT_AT_CEILING_ON_WITNESSED_LATENT_TASKS",
    "REGIME_REALISED__REGISTERED",
    "MECHANISM_BEATS_PARENT_ON_ACTIVATION_REGIME",
    "PARENT_SUFFICIENT_ON_ACTIVATION_REGIME",
    "PARENT_AHEAD_ON_ACTIVATION_REGIME",
    "GAIN_NOT_ATTRIBUTABLE_TO_DEPENDENCE_MACHINERY",
    "GAIN_NOT_PARETO_ON_CONTROLS",
)


# ---- read-only imports of the frozen machinery ----------------------------------------

def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SUITE = _load("pd_suite_ro", ROOT / "scripts" / "run_dependence_evidence_generated_suite.py")
GATE = _load("h_ext1_gate_ro", ROOT / "scripts" / "h_ext1_gate_study.py")
FMFG = SUITE.FMFG
make_item, token, S1_RULE = SUITE.make_item, SUITE.token, SUITE.S1_RULE
write_json, read_json, canon, answer_shape = SUITE.write_json, SUITE.read_json, SUITE.canon, SUITE.answer_shape
GATE_ID = str(read_json(GATE_FREEZE)["selected_gate"])

PINNED_SOURCES = {
    "scripts/h_ext1r_regime_study.py": Path(__file__).resolve(),
    "scripts/h_ext1r_pd_arms.py": ROOT / "scripts" / "h_ext1r_pd_arms.py",
    "scripts/orion_pd_arms.py": ROOT / "scripts" / "orion_pd_arms.py",
    "scripts/orion_claude_arms.py": ROOT / "scripts" / "orion_claude_arms.py",
    "scripts/run_dependence_evidence_generated_suite.py": ROOT / "scripts" / "run_dependence_evidence_generated_suite.py",
    "scripts/run_formal_discovery_generated_suite.py": ROOT / "scripts" / "run_formal_discovery_generated_suite.py",
    "scripts/h_ext1_gate_study.py": ROOT / "scripts" / "h_ext1_gate_study.py",
    "research/experiments/h-ext1/H_EXT1_GATE_FREEZE.json": GATE_FREEZE,
}


def sha256_path(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sha256_text(t: str) -> str:
    return hashlib.sha256(t.encode()).hexdigest()


def source_pins() -> dict[str, str]:
    return {k: sha256_path(v) for k, v in PINNED_SOURCES.items()}


# ---- generators ------------------------------------------------------------------------

def _conv(rng: random.Random) -> str:
    return "CV" + "".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ") for _ in range(4))


def _s1_public(h: str, items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "study_id": "PD-S5", "task_kind": "CORROBORATION", "hypothesis": h,
        "registered_decision_rule": S1_RULE, "items": items,
        "task": "Decide under the registered rule; return the decision and the count of independent support families.",
    }


def gen_pds5a(rng: random.Random, index: int) -> tuple[dict[str, Any], dict[str, Any]]:
    """Witness (e1/e2 share a root) + latent convention (e4/e5 adopt e3's convention by name)."""
    h = token(rng, "H")
    conv = _conv(rng)
    roots = [token(rng, "R") for _ in range(4)]
    types = rng.sample(["data", "model", "instrument", "calibration"], 4)
    items = [
        make_item(rng, f"{h}-e1", roots[0], types[0],
                  f"Primary {types[0]} acquisition on the registered protocol; self-calibrated."),
        make_item(rng, f"{h}-e2", roots[0], types[0],
                  f"Re-analysis of the same {types[0]} acquisition under an alternative estimator."),
        make_item(rng, f"{h}-e3", roots[1], types[1],
                  f"Independent {types[1]} pipeline; we introduce the {conv} calibration convention and calibrate directly."),
        make_item(rng, f"{h}-e4", roots[2], types[2],
                  f"Replication on the {types[2]} channel; all reductions are calibrated under the {conv} convention for comparability."),
        make_item(rng, f"{h}-e5", roots[3], types[3],
                  f"Second replication; the {types[3]} chain adopts the {conv} convention throughout."),
    ]
    return _s1_public(h, items), {"decision": INCONCLUSIVE, "independent_support_family_count": 2}


def gen_pds5b(rng: random.Random, index: int) -> tuple[dict[str, Any], dict[str, Any]]:
    """Control: the same witness, and e3/e4/e5 each on their own convention."""
    h = token(rng, "H")
    convs = [_conv(rng) for _ in range(3)]
    roots = [token(rng, "R") for _ in range(4)]
    types = rng.sample(["data", "model", "instrument", "calibration"], 4)
    items = [
        make_item(rng, f"{h}-e1", roots[0], types[0],
                  f"Primary {types[0]} acquisition on the registered protocol; self-calibrated."),
        make_item(rng, f"{h}-e2", roots[0], types[0],
                  f"Re-analysis of the same {types[0]} acquisition under an alternative estimator."),
        make_item(rng, f"{h}-e3", roots[1], types[1],
                  f"Independent {types[1]} pipeline; we introduce the {convs[0]} calibration convention and calibrate directly."),
        make_item(rng, f"{h}-e4", roots[2], types[2],
                  f"Replication on the {types[2]} channel; all reductions are calibrated under our own {convs[1]} convention, no external convention adopted."),
        make_item(rng, f"{h}-e5", roots[3], types[3],
                  f"Second replication; the {types[3]} chain adopts its own {convs[2]} convention throughout."),
    ]
    return _s1_public(h, items), {"decision": "ACCEPT_H", "independent_support_family_count": 4}


def _s5_items(rng: random.Random, latent: bool) -> tuple[str, list[dict[str, Any]]]:
    h = token(rng, "H")
    curve = "TC" + "".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ") for _ in range(4))
    roots = [token(rng, "R") for _ in range(3)]
    i4_text = (f"Family-C calibration study; every reduction is calibrated through transfer curve {curve}."
               if latent else
               "Family-C calibration study; self-calibrated against its own standard, no external transfer curve adopted.")
    items = [
        make_item(rng, f"{h}-i1", roots[0], "data", f"Family-A primary dataset; publishes the calibration transfer curve {curve}."),
        make_item(rng, f"{h}-i2", roots[1], "model", "Family-B model analysis."),
        make_item(rng, f"{h}-i3", roots[1], "instrument", "Family-B instrument cross-check."),
        make_item(rng, f"{h}-i4", roots[2], "calibration", i4_text),
    ]
    return h, items


def _s5_public(h: str, items: list[dict[str, Any]]) -> dict[str, Any]:
    claims = [
        {"claim_id": f"{h}-C1", "cited_item_ids": [f"{h}-i1", f"{h}-i2", f"{h}-i3"]},
        {"claim_id": f"{h}-C2", "cited_item_ids": [f"{h}-i4"]},
    ]
    return {
        "study_id": "PD-S5", "task_kind": "REVOCATION",
        "registered_reopening_rule": S5_LINEAGE_RULE, "items": items, "claims": claims,
        "failure_event": {"kind": "ITEM_FAILURE", "target_item_id": f"{h}-i1"},
        "task": "For each claim return reopened_claim_ids (every family destroyed) and preserved_claim_ids.",
    }


def gen_pds5c(rng: random.Random, index: int) -> tuple[dict[str, Any], dict[str, Any]]:
    """Witness (i2/i3 share a root) + latent lineage (i4 calibrates through i1's curve); i1 fails."""
    h, items = _s5_items(rng, latent=True)
    return _s5_public(h, items), {"reopened_claim_ids": [f"{h}-C2"], "preserved_claim_ids": [f"{h}-C1"]}


def gen_pds5d(rng: random.Random, index: int) -> tuple[dict[str, Any], dict[str, Any]]:
    """Control: the same witness, i4 self-calibrated; i1 fails, both claims preserved."""
    h, items = _s5_items(rng, latent=False)
    return _s5_public(h, items), {"reopened_claim_ids": [], "preserved_claim_ids": [f"{h}-C1", f"{h}-C2"]}


GENERATORS = {STRATA[0]: gen_pds5a, STRATA[1]: gen_pds5b, STRATA[2]: gen_pds5c, STRATA[3]: gen_pds5d}


def gen_no_witness_control(rng: random.Random) -> dict[str, Any]:
    """A PDS1B-shaped task (three independent roots): the gate MUST read False on it."""
    h = token(rng, "H")
    items = [make_item(rng, f"{h}-e{k}", token(rng, "R"), t, f"Autonomous {t} measurement, self-calibrated.")
             for k, t in enumerate(("data", "model", "instrument"), start=1)]
    return _s1_public(h, items)


# ---- the mechanical "could the contrast exist" reading ------------------------------------

def provenance_only_answer(task: dict[str, Any]) -> dict[str, Any]:
    """What reasoning over lineage roots ALONE returns.  Not an arm: the construction's
    own check that a root-only reader errs on treatment and is right on control."""
    if task["task_kind"] == "CORROBORATION":
        count = len({i["lineage_root"] for i in task["items"]})
        return {"decision": "ACCEPT_H" if count >= 3 else INCONCLUSIVE, "independent_support_family_count": count}
    target = task["failure_event"]["target_item_id"]
    failed_root = next(i["lineage_root"] for i in task["items"] if i["item_id"] == target)
    root_of = {i["item_id"]: i["lineage_root"] for i in task["items"]}
    reopened, preserved = [], []
    for claim in task["claims"]:
        families = {root_of[c] for c in claim["cited_item_ids"]}
        (reopened if families == {failed_root} else preserved).append(claim["claim_id"])
    return {"reopened_claim_ids": sorted(reopened), "preserved_claim_ids": sorted(preserved)}


# ---- split preparation (the frozen suite's schema, neutral ids, private oracle) -----------

def prepare(workdir: Path, per_stratum: int, seed: int, arms: tuple[str, ...], force: bool) -> dict[str, Any]:
    if workdir.exists():
        if not force:
            raise FMFG.SuiteError(f"workdir exists: {workdir}")
        shutil.rmtree(workdir)
    rng = random.Random(seed)
    total = per_stratum * len(STRATA)
    neutral_ids = [f"{STUDY_SLUG}-{i + 1:04d}" for i in range(total)]
    rng.shuffle(neutral_ids)
    id_iter = iter(neutral_ids)
    public_tasks, private_answers, strata = [], {}, {}
    for stratum in STRATA:                       # tuple order: never an unordered container
        for index in range(per_stratum):
            task_rng = random.Random(rng.getrandbits(64))
            public, answer = GENERATORS[stratum](task_rng, index)
            task_id = next(id_iter)
            public["task_id"] = task_id
            public["answer_contract"] = answer_shape(answer)
            public_tasks.append(public)
            private_answers[task_id] = answer
            strata[task_id] = stratum
            for arm in arms:
                write_json(workdir / "requests" / arm / f"{task_id}.json", {
                    "schema_version": "orion.v2.dependence-evidence-request.v1",
                    "task_id": task_id, "arm_id": arm, "task": public,
                    "scientific_truth_authorized": False, "legitimate_authority_authorized": False,
                    "publication_readiness_authorized": False,
                })
    public_tasks.sort(key=lambda t: t["task_id"])
    write_json(workdir / "public_tasks.json", {"schema_version": "orion.v2.dependence-evidence-public.v1", "tasks": public_tasks})
    write_json(workdir / "private_oracle.json", {"schema_version": "orion.v2.dependence-evidence-private.v1",
                                                 "answers": private_answers, "strata": strata})
    freeze = {
        "schema_version": "orion.v2.dependence-evidence-freeze.v1", "seed": seed, "study_id": STUDY_ID,
        "strata": {s: per_stratum for s in STRATA}, "task_count": len(public_tasks), "arms": list(arms),
        "private_oracle_visible_to_solver": False, "strata_visible_in_public_tasks": False,
        "authority": {"grants_scientific_truth": False, "grants_dependence_detection_in_real_corpora": False,
                      "grants_legitimate_authority": False},
    }
    write_json(workdir / "FROZEN_SUITE.json", freeze)
    return freeze


def split_digest(workdir: Path) -> str:
    return sha256_path(workdir / "public_tasks.json")


# ---- gate audit: the frozen gate fires on every task, and can read False -------------------

def gate_audit(workdir: Path) -> dict[str, Any]:
    tasks = read_json(workdir / "public_tasks.json")["tasks"]
    fired, by_stratum, features = 0, {}, {}
    strata = read_json(workdir / "private_oracle.json")["strata"] if (workdir / "private_oracle.json").exists() else {}
    for task in tasks:
        GATE.canary_check(task)
        f = GATE.witness_features(task)
        on = GATE.gate_fires(GATE_ID, f)
        fired += on
        s = strata.get(task["task_id"], "UNKNOWN")
        by_stratum.setdefault(s, [0, 0])
        by_stratum[s][0] += on
        by_stratum[s][1] += 1
        key = json.dumps({k: f[k] for k in ("w_dup_hash", "w_shared_root", "w_declared_overlap", "w_xref_root",
                                             "n_records", "n_roots")}, sort_keys=True)
        features.setdefault(s, set()).add(key)
    control = gen_no_witness_control(random.Random(7))
    control_fires = GATE.gate_fires(GATE_ID, GATE.witness_features(control))
    same_gate_input_within_pair = all(features.get(a) == features.get(b) for a, b in PAIRS)
    return {
        "gate_id": GATE_ID, "n_tasks": len(tasks), "fired": fired,
        "fires_on_every_task": fired == len(tasks) and len(tasks) > 0,
        "by_stratum": {s: {"fired": v[0], "n": v[1]} for s, v in sorted(by_stratum.items())},
        "no_witness_control_fires": control_fires,
        "control_read_false": control_fires is False,
        "gate_input_feature_sets_by_stratum": {s: sorted(v) for s, v in sorted(features.items())},
        "identical_gate_input_within_each_pair": same_gate_input_within_pair,
    }


# ---- dispatch / evaluate (frozen harness; own arms executable) ----------------------------

def dispatch(workdir: Path, arms: tuple[str, ...], concurrency: int, overwrite: bool) -> None:
    import shlex
    os.environ["ORION_FORMAL_ARM_COMMAND"] = " ".join(
        shlex.quote(p) for p in [sys.executable, str(ROOT / "scripts" / "h_ext1r_pd_arms.py")])
    FMFG.dispatch(workdir, list(arms), concurrency, overwrite)


def _sorted_lists(v: Any) -> Any:
    if isinstance(v, dict):
        return {k: _sorted_lists(x) for k, x in v.items()}
    if isinstance(v, list) and all(isinstance(x, str) for x in v):
        return sorted(v)
    return v


def evaluate(workdir: Path, arms: tuple[str, ...]) -> dict[str, Any]:
    """Exact-match scoring; list-valued answer fields compared as sets (declared in the
    design).  A missing or failed response is MISSING, never 'wrong'."""
    answers = read_json(workdir / "private_oracle.json")["answers"]
    strata = read_json(workdir / "private_oracle.json")["strata"]
    rows, summary = [], {}
    for arm in arms:
        correct = missing = 0
        served, contracts, stops, zero_text = {}, {}, {}, 0
        for task_id, expected in answers.items():
            path = workdir / "responses" / arm / f"{task_id}.json"
            row = {"arm": arm, "task_id": task_id, "stratum": strata[task_id], "expected": expected}
            if not path.exists():
                missing += 1
                rows.append({**row, "correct": False, "missing": True, "actual": None})
                continue
            resp = read_json(path)
            actual = resp.get("answer")
            if actual is None or str(resp.get("status", "")).startswith("EXECUTION_FAILED"):
                missing += 1
                rows.append({**row, "correct": False, "missing": True, "actual": None,
                             "status": resp.get("status"), "reason": str(resp.get("reasoning_summary", ""))[:300]})
                continue
            ok = canon(_sorted_lists(actual)) == canon(_sorted_lists(expected))
            correct += int(ok)
            rr, cr = resp.get("resource_receipt", {}), resp.get("channel_receipt", {})
            for m in rr.get("served_model_ids", []):
                served[m] = served.get(m, 0) + 1
            contracts[cr.get("contract_sha256", "")] = contracts.get(cr.get("contract_sha256", ""), 0) + 1
            stops[cr.get("stop_reason", "")] = stops.get(cr.get("stop_reason", ""), 0) + 1
            zero_text += int(cr.get("text_chars", 1) == 0)
            rows.append({**row, "correct": ok, "missing": False, "actual": actual,
                         "wall_time_seconds": rr.get("wall_time_seconds"), "output_tokens": rr.get("output_tokens")})
        n = len(answers)
        summary[arm] = {"correct": correct, "tasks": n, "accuracy": correct / n if n else 0.0,
                        "missing_or_invalid": missing, "run_valid": missing == 0,
                        "served_model_ids": served, "contract_sha256s": contracts, "stop_reasons": stops,
                        "zero_text_calls": zero_text}
    write_json(workdir / "EVALUATION_ROWS.json", rows)
    write_json(workdir / "EVALUATION_SUMMARY.json", {"summary": summary, "list_fields_compared_as_sets": True})
    return summary


# ---- statistics ------------------------------------------------------------------------

def mcnemar_exact(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def mcnemar_power(n: int, pb: float, pc: float, alpha: float = ALPHA) -> float:
    """Exact power of the two-sided exact McNemar test at n pairs with per-pair discordance
    probabilities pb (M-only) and pc (PARENT-only); trinomial enumeration."""
    from math import factorial
    p0 = 1 - pb - pc
    power = 0.0
    for b in range(n + 1):
        for c in range(n - b + 1):
            if mcnemar_exact(b, c) <= alpha:
                power += (factorial(n) / (factorial(b) * factorial(c) * factorial(n - b - c))
                          * pb ** b * pc ** c * p0 ** (n - b - c))
    return power


def paired(rows_x: dict[str, dict], rows_y: dict[str, dict], ids: list[str]) -> dict[str, Any]:
    b = sum(1 for t in ids if rows_x[t]["correct"] and not rows_y[t]["correct"])
    c = sum(1 for t in ids if rows_y[t]["correct"] and not rows_x[t]["correct"])
    return {"n": len(ids), "x_correct": sum(rows_x[t]["correct"] for t in ids),
            "y_correct": sum(rows_y[t]["correct"] for t in ids),
            "b_x_only": b, "c_y_only": c, "discordant": b + c, "exact_p": mcnemar_exact(b, c)}


def analyze(workdir: Path, cell: str) -> dict[str, Any]:
    rows = read_json(workdir / "EVALUATION_ROWS.json")
    summary = read_json(workdir / "EVALUATION_SUMMARY.json")["summary"]
    by = {arm: {r["task_id"]: r for r in rows if r["arm"] == arm} for arm in ARMS}
    strata = read_json(workdir / "private_oracle.json")["strata"]
    ids_all = sorted(strata)
    ids_treat = [t for t in ids_all if strata[t] in TREATMENT]
    ids_ctrl = [t for t in ids_all if strata[t] in CONTROL]
    per_stratum = {}
    for s in STRATA:
        ids = [t for t in ids_all if strata[t] == s]
        per_stratum[s] = {arm: {"correct": sum(by[arm][t]["correct"] for t in ids), "n": len(ids)} for arm in ARMS}
    run_valid = all(summary[a]["run_valid"] for a in ARMS)
    audit = gate_audit(workdir)
    out: dict[str, Any] = {
        "schema_version": "orion.v2.h-ext1r-analysis.v1", "cell": cell, "study_id": STUDY_ID,
        "run_valid": run_valid, "gate_audit": audit, "per_arm": summary, "per_stratum": per_stratum,
        "m_vs_parent_all_gate_active": paired(by[ARM_M], by[ARM_PARENT], ids_all),
        "m_vs_parent_treatment": paired(by[ARM_M], by[ARM_PARENT], ids_treat),
        "m_vs_parent_control": paired(by[ARM_M], by[ARM_PARENT], ids_ctrl),
        "m_vs_off_treatment": paired(by[ARM_M], by[ARM_OFF], ids_treat),
        "m_vs_parent_by_treatment_stratum": {
            s: paired(by[ARM_M], by[ARM_PARENT], [t for t in ids_all if strata[t] == s]) for s in TREATMENT},
        "parent_accuracy_on_treatment": (sum(by[ARM_PARENT][t]["correct"] for t in ids_treat) / len(ids_treat)) if ids_treat else None,
    }
    if cell == "dev":
        out.update(feasibility(out))
    else:
        out.update(protected_gates(out))
    return out


def feasibility(a: dict[str, Any]) -> dict[str, Any]:
    """F1 (registered here, before the dev split is scored): parent off ceiling on the
    treatment strata.  The dev split is NOT evidence about the mechanism; it decides
    whether a contrast can exist."""
    if not a["run_valid"] or not a["gate_audit"]["fires_on_every_task"] or not a["gate_audit"]["control_read_false"]:
        return {"F1_PARENT_OFF_CEILING": {"status": "COULD_NOT_CHECK"}, "terminal": "CANNOT_CHECK_RUN_INVALID"}
    par = a["parent_accuracy_on_treatment"]
    ok = par <= PARENT_OFF_CEILING_MAX
    # observed-effect power at the protected n, reported with the winner's-curse caveat
    t = a["m_vs_parent_treatment"]
    pb, pc = t["b_x_only"] / t["n"], t["c_y_only"] / t["n"]
    n_prot = PROTECTED_PER_STRATUM * len(TREATMENT)
    power = mcnemar_power(n_prot, pb, pc) if (pb + pc) > 0 else 0.0
    return {
        "F1_PARENT_OFF_CEILING": {"status": "PASS" if ok else "FAIL", "parent_accuracy_on_treatment": par,
                                  "max_allowed": PARENT_OFF_CEILING_MAX,
                                  "parent_correct": a["m_vs_parent_treatment"]["y_correct"], "n": t["n"]},
        "power_at_protected_n_from_dev_discordance": {
            "n_treatment_pairs": n_prot, "pb_m_only": pb, "pc_parent_only": pc, "power": power,
            "caveat": "observed-effect power from the development split; optimistic by the winner's curse; "
                      "reported, not gated on -- registration rests on F1"},
        "terminal": "REGIME_REALISED__REGISTERED" if ok else
                    "REGIME_NOT_REALISED__PARENT_AT_CEILING_ON_WITNESSED_LATENT_TASKS",
    }


def protected_gates(a: dict[str, Any]) -> dict[str, Any]:
    g: dict[str, Any] = {}
    g["G0_VALIDITY"] = {"pass": a["run_valid"] and a["gate_audit"]["fires_on_every_task"]
                        and a["gate_audit"]["control_read_false"],
                        "served_model_ids": {arm: a["per_arm"][arm]["served_model_ids"] for arm in ARMS},
                        "contract_sha256s": {arm: a["per_arm"][arm]["contract_sha256s"] for arm in ARMS}}
    served = {m for arm in ARMS for m in a["per_arm"][arm]["served_model_ids"]}
    contracts = {c for arm in ARMS for c in a["per_arm"][arm]["contract_sha256s"]}
    g["G0b_HOMOGENEITY"] = {"pass": len(served) == 1 and len(contracts) == 1
                            and all(a["per_arm"][arm]["zero_text_calls"] == 0 for arm in ARMS),
                            "served_model_ids": sorted(served), "contract_sha256s": sorted(contracts)}
    t = a["m_vs_parent_all_gate_active"]
    g["G1_M_VS_PARENT_GATE_ACTIVE"] = {**t, "alpha": ALPHA, "rejects": t["exact_p"] < ALPHA,
                                       "direction": "M" if t["b_x_only"] > t["c_y_only"] else
                                       ("PARENT" if t["c_y_only"] > t["b_x_only"] else "TIE")}
    c = a["m_vs_parent_control"]
    g["G2_PARETO_ON_CONTROLS"] = {**c, "pass": c["x_correct"] >= c["y_correct"]}
    o = a["m_vs_off_treatment"]
    g["G3_ATTRIBUTION_M_VS_OFF_TREATMENT"] = {**o, "pass": o["exact_p"] < ALPHA and o["b_x_only"] > o["c_y_only"]}
    g["G4_SIGN_CONSISTENCY_TREATMENT_STRATA"] = {
        s: {"m": v["x_correct"], "parent": v["y_correct"], "m_ge_parent": v["x_correct"] >= v["y_correct"]}
        for s, v in a["m_vs_parent_by_treatment_stratum"].items()}
    g["G4_SIGN_CONSISTENCY_TREATMENT_STRATA"]["pass"] = all(
        v["m_ge_parent"] for k, v in g["G4_SIGN_CONSISTENCY_TREATMENT_STRATA"].items() if k != "pass")
    # routing, precedence top-down
    if not g["G0_VALIDITY"]["pass"] or not g["G0b_HOMOGENEITY"]["pass"]:
        terminal = "CANNOT_CHECK_RUN_INVALID"
    elif not g["G1_M_VS_PARENT_GATE_ACTIVE"]["rejects"]:
        terminal = "PARENT_SUFFICIENT_ON_ACTIVATION_REGIME"
    elif g["G1_M_VS_PARENT_GATE_ACTIVE"]["direction"] == "PARENT":
        terminal = "PARENT_AHEAD_ON_ACTIVATION_REGIME"
    elif not g["G3_ATTRIBUTION_M_VS_OFF_TREATMENT"]["pass"]:
        terminal = "GAIN_NOT_ATTRIBUTABLE_TO_DEPENDENCE_MACHINERY"
    elif not g["G2_PARETO_ON_CONTROLS"]["pass"] or not g["G4_SIGN_CONSISTENCY_TREATMENT_STRATA"]["pass"]:
        terminal = "GAIN_NOT_PARETO_ON_CONTROLS"
    else:
        terminal = "MECHANISM_BEATS_PARENT_ON_ACTIVATION_REGIME"
    return {"gates": g, "terminal": terminal}


# ---- selftest ----------------------------------------------------------------------------

def selftest(out_dir: Path) -> int:
    checks = []
    rng = random.Random(1)
    # generator validity: the construction's own root-only reader errs on treatment, is right on control
    for s in STRATA:
        for k in range(10):
            public, answer = GENERATORS[s](random.Random(rng.getrandbits(64)), k)
            po = provenance_only_answer(public)
            po_right = canon(_sorted_lists(po)) == canon(_sorted_lists(answer))
            checks.append({"check": f"root_only_reader_{'errs' if s in TREATMENT else 'is_right'}_on_{s}",
                           "pass": (not po_right) if s in TREATMENT else po_right, "instance": k})
    # a temporary split: gate fires everywhere, control reads False, identical gate input within pairs
    tmp = out_dir / "_selftest_split"
    prepare(tmp, 3, 12345, ARMS, force=True)
    audit = gate_audit(tmp)
    checks.append({"check": "gate_fires_on_every_task", "pass": audit["fires_on_every_task"], "n": audit["n_tasks"]})
    checks.append({"check": "no_witness_control_reads_false", "pass": audit["control_read_false"]})
    checks.append({"check": "identical_gate_input_within_each_pair", "pass": audit["identical_gate_input_within_each_pair"]})
    answers = read_json(tmp / "private_oracle.json")["answers"]
    strata = read_json(tmp / "private_oracle.json")["strata"]
    for a_s, b_s in PAIRS:
        da = {canon(answers[t]) for t in answers if strata[t] == a_s}
        db = {canon(answers[t]) for t in answers if strata[t] == b_s}
        # the answer shapes differ between paired strata (both verdicts reachable at the same gate input)
        checks.append({"check": f"answers_differ_between_{a_s}_and_{b_s}", "pass": not (da & db)})
    # reproducibility across hash seeds
    d0 = split_digest(tmp)
    ds = []
    for hs in ("1", "12345"):
        env = {**os.environ, "PYTHONHASHSEED": hs}
        import subprocess
        cp = subprocess.run([sys.executable, str(Path(__file__).resolve()), "digest", "--per-stratum", "3",
                             "--seed-literal", "12345", "--out", str(out_dir / f"_digest_{hs}")],
                            env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        ds.append(cp.stdout.strip().split()[-1] if cp.returncode == 0 else f"FAILED:{cp.stderr[-200:]}")
    checks.append({"check": "split_digest_identical_across_PYTHONHASHSEED", "pass": all(d == d0 for d in ds),
                   "digests": [d0, *ds]})
    # statistics known answers; the test can reject and has size under the null
    checks.append({"check": "mcnemar_known_answer_b7_c0", "pass": abs(mcnemar_exact(7, 0) - 2 / 128) < 1e-12})
    checks.append({"check": "mcnemar_b5_c0_cannot_reject", "pass": mcnemar_exact(5, 0) > ALPHA})
    checks.append({"check": "power_size_under_null_le_alpha", "pass": mcnemar_power(40, 0.1, 0.1) <= ALPHA + 1e-9})
    checks.append({"check": "power_saturates_under_large_effect", "pass": mcnemar_power(100, 0.15, 0.0) > 0.99})
    # routing: every protected terminal reachable by fixture
    reached = set()
    for fixture in _routing_fixtures():
        reached.add(protected_gates(fixture)["terminal"])
    want = set(TERMINALS) - {"REGIME_NOT_REALISED__PARENT_AT_CEILING_ON_WITNESSED_LATENT_TASKS", "REGIME_REALISED__REGISTERED"}
    checks.append({"check": "every_protected_terminal_reachable_by_fixture", "pass": reached == want,
                   "reached": sorted(reached), "missing": sorted(want - reached)})
    # F1 can pass and can fail
    checks.append({"check": "F1_passes_when_parent_off_ceiling", "pass": feasibility(_dev_fixture(30, 40))["terminal"] == "REGIME_REALISED__REGISTERED"})
    checks.append({"check": "F1_fails_when_parent_at_ceiling", "pass": feasibility(_dev_fixture(39, 40))["terminal"].startswith("REGIME_NOT_REALISED")})
    passed = all(c["pass"] for c in checks)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "H_EXT1R_SELFTEST_REPORT.json").write_text(json.dumps(
        {"passed": passed, "n_checks": len(checks), "checks": checks, "gate_audit_on_selftest_split": audit,
         "source_pins": source_pins(), "python": sys.version}, indent=2, sort_keys=True) + "\n")
    shutil.rmtree(tmp, ignore_errors=True)
    for hs in ("1", "12345"):
        shutil.rmtree(out_dir / f"_digest_{hs}", ignore_errors=True)
    print(f"selftest: {sum(1 for c in checks if c['pass'])}/{len(checks)} checks pass")
    for c in checks:
        if not c["pass"]:
            print(f"  FAIL {c['check']} {json.dumps({k: v for k, v in c.items() if k not in ('check', 'pass')})}")
    return 0 if passed else 1


def _fixture(valid: bool, b_all: int, c_all: int, ctrl_x: int, ctrl_y: int, off_b: int, off_c: int,
             per_stratum_m: tuple[int, int] = (50, 50), per_stratum_p: tuple[int, int] = (40, 40)) -> dict[str, Any]:
    n = 200
    pa = lambda b, c, n, x, y: {"n": n, "x_correct": x, "y_correct": y, "b_x_only": b, "c_y_only": c,  # noqa: E731
                                "discordant": b + c, "exact_p": mcnemar_exact(b, c)}
    return {
        "run_valid": valid,
        "gate_audit": {"fires_on_every_task": True, "control_read_false": True},
        "per_arm": {arm: {"served_model_ids": {"glm-5.3": n}, "contract_sha256s": {"abc": n}, "zero_text_calls": 0} for arm in ARMS},
        "m_vs_parent_all_gate_active": pa(b_all, c_all, n, 190, 190 - b_all + c_all),
        "m_vs_parent_control": pa(0, ctrl_y - ctrl_x if ctrl_y > ctrl_x else 0, 100, ctrl_x, ctrl_y),
        "m_vs_off_treatment": pa(off_b, off_c, 100, 95, 95 - off_b + off_c),
        "m_vs_parent_by_treatment_stratum": {
            TREATMENT[0]: pa(0, 0, 50, per_stratum_m[0], per_stratum_p[0]),
            TREATMENT[1]: pa(0, 0, 50, per_stratum_m[1], per_stratum_p[1])},
    }


def _routing_fixtures() -> list[dict[str, Any]]:
    return [
        _fixture(False, 20, 0, 100, 100, 20, 0),                       # invalid run
        _fixture(True, 2, 1, 100, 100, 20, 0),                         # no rejection -> parent sufficient
        _fixture(True, 0, 20, 100, 100, 20, 0),                        # parent ahead
        _fixture(True, 20, 0, 100, 100, 2, 1),                         # gain not attributable
        _fixture(True, 20, 0, 90, 100, 20, 0),                         # not Pareto on controls
        _fixture(True, 20, 0, 100, 100, 20, 0),                        # mechanism beats parent
    ]


def _dev_fixture(parent_correct: int, n: int) -> dict[str, Any]:
    return {"run_valid": True, "gate_audit": {"fires_on_every_task": True, "control_read_false": True},
            "parent_accuracy_on_treatment": parent_correct / n,
            "m_vs_parent_treatment": {"n": n, "x_correct": n, "y_correct": parent_correct,
                                      "b_x_only": n - parent_correct, "c_y_only": 0}}


# ---- freeze / protected authorization ----------------------------------------------------

def freeze(dev_analysis: Path, seed_file: Path) -> int:
    if DESIGN_JSON.exists():
        print(f"REFUSED: {DESIGN_JSON.name} exists; a design is frozen once", file=sys.stderr)
        return 3
    dev = read_json(dev_analysis)
    if dev.get("terminal") != "REGIME_REALISED__REGISTERED":
        print(f"REFUSED: development terminal is {dev.get('terminal')}; nothing to register", file=sys.stderr)
        return 3
    seed = seed_file.read_bytes().strip().decode()
    design = {
        "schema_version": "orion.v2.h-ext1r-regime-design.v1", "study_id": "H-EXT-1R",
        "status": "FROZEN_PROSPECTIVE_DESIGN_NO_PROTECTED_RESULTS", "frozen_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "predecessor": {"h_ext1p_terminal": "REGISTERED_CONTRAST_CANNOT_BE_ABOUT_THE_MECHANISM",
                        "attributed_stage": "TASK_SUITE",
                        "lever": "witnessed-latent strata: the gate fires by construction and the answer turns on a latent dependence"},
        "gate": {"id": GATE_ID, "imported_from": "scripts/h_ext1_gate_study.py", "freeze": "research/experiments/h-ext1/H_EXT1_GATE_FREEZE.json",
                 "fires_on_every_task_by_construction": True, "gated_m_equals_m_in_this_regime": True},
        "arms": list(ARMS), "strata": {"treatment": list(TREATMENT), "control": list(CONTROL), "pairs": [list(p) for p in PAIRS]},
        "substrate": {"channel": "anthropic_compatible", "requested_model": os.environ.get("ANTHROPIC_MODEL", "UNSET_AT_FREEZE"),
                      "pinned_served_model": os.environ.get("ORION_ARM_SERVED_MODEL", "UNSET_AT_FREEZE"),
                      "channel_contract": os.environ.get("ORION_ARM_CHANNEL_CONTRACT", "UNSET_AT_FREEZE"),
                      "max_tokens": os.environ.get("ORION_ARM_MAX_TOKENS", "UNSET_AT_FREEZE"),
                      "differs_from_h_ext1_prospective_substrate": True,
                      "h_ext1_prospective_substrate": "gpt-5.5 via codex CLI (requested id; served id not recorded by that channel)"},
        "development": {"seed": DEV_SEED, "per_stratum": DEV_PER_STRATUM, "analysis_sha256": sha256_path(dev_analysis),
                        "F1": dev["F1_PARENT_OFF_CEILING"], "power_note": dev["power_at_protected_n_from_dev_discordance"],
                        "per_stratum_table": dev["per_stratum"], "not_evidence_about_the_mechanism": True},
        "protected": {"per_stratum": PROTECTED_PER_STRATUM, "n_tasks": PROTECTED_PER_STRATUM * len(STRATA),
                      "seed_commitment_sha256": sha256_text(seed), "seed_revealed": False,
                      "arms_calls": PROTECTED_PER_STRATUM * len(STRATA) * len(ARMS)},
        "gates": {
            "G0_VALIDITY": "all responses present and COMPLETED; gate fires on every task; no-witness control reads False",
            "G0b_HOMOGENEITY": "one served model id and one contract sha256 across all envelopes; zero zero-text calls",
            "G1_M_VS_PARENT_GATE_ACTIVE": f"exact two-sided McNemar on all {PROTECTED_PER_STRATUM * len(STRATA)} gate-active tasks, alpha {ALPHA}",
            "G2_PARETO_ON_CONTROLS": "acc(M) >= acc(PARENT) on the pooled control strata (ties allowed)",
            "G3_ATTRIBUTION_M_VS_OFF_TREATMENT": f"exact McNemar M vs OFF on treatment strata, M ahead, alpha {ALPHA}",
            "G4_SIGN_CONSISTENCY_TREATMENT_STRATA": "M >= PARENT within each treatment stratum",
        },
        "routing_precedence": ["CANNOT_CHECK_RUN_INVALID (G0/G0b)", "PARENT_SUFFICIENT_ON_ACTIVATION_REGIME (G1 no rejection)",
                               "PARENT_AHEAD_ON_ACTIVATION_REGIME (G1 rejects, parent direction)",
                               "GAIN_NOT_ATTRIBUTABLE_TO_DEPENDENCE_MACHINERY (G3)", "GAIN_NOT_PARETO_ON_CONTROLS (G2/G4)",
                               "MECHANISM_BEATS_PARENT_ON_ACTIVATION_REGIME"],
        "terminals": list(TERMINALS),
        "no_rescue": True, "list_fields_compared_as_sets": True,
        "source_pins": source_pins(),
        "authority": {"grants_scientific_truth": False, "grants_field_status": False,
                      "grants_dependence_detection_in_real_corpora": False, "grants_manuscript_change": False},
    }
    write_json(DESIGN_JSON, design)
    print(f"frozen design: {DESIGN_JSON.name} sha256 {sha256_path(DESIGN_JSON)}")
    print(f"seed commitment: {design['protected']['seed_commitment_sha256']}")
    return 0


def protected_guard(seed_file: Path) -> int:
    if not AUTH_FILE.exists():
        print(f"REFUSED: {AUTH_FILE.name} absent -- protected run not authorized", file=sys.stderr)
        return 3
    auth = read_json(AUTH_FILE)
    if not auth.get("human_written") or len(str(auth.get("human_written_token", ""))) < 20:
        print("REFUSED: authorization is not human-written", file=sys.stderr)
        return 3
    if auth.get("acknowledged_design_sha256") != sha256_path(DESIGN_JSON):
        print("REFUSED: acknowledged_design_sha256 does not match the frozen design JSON", file=sys.stderr)
        return 3
    seed = seed_file.read_bytes().strip().decode()
    commit = read_json(DESIGN_JSON)["protected"]["seed_commitment_sha256"]
    if sha256_text(seed) != commit:
        print("REFUSED: custody seed does not hash to the frozen commitment", file=sys.stderr)
        return 4
    drift = {k: (v, source_pins()[k]) for k, v in read_json(DESIGN_JSON)["source_pins"].items() if source_pins()[k] != v}
    if drift:
        print(f"REFUSED: pinned sources drifted since the freeze: {json.dumps(drift)}", file=sys.stderr)
        return 5
    return 0


def archive_authorization(seed: str) -> None:
    used = {**read_json(AUTH_FILE), "consumed": True, "consumed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "revealed_protected_seed": seed, "revealed_protected_seed_sha256": sha256_text(seed),
            "note": "consumed by the H-EXT-1R protected preparation and archived so the guard is re-armed"}
    write_json(AUTH_USED, used)
    AUTH_FILE.unlink()


# ---- CLI --------------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("selftest", "prepare", "gate-audit", "dispatch", "evaluate", "analyze",
                                      "freeze", "digest", "protected-prepare"))
    ap.add_argument("--workdir", type=Path)
    ap.add_argument("--cell", choices=("dev", "protected"), default="dev")
    ap.add_argument("--per-stratum", type=int, default=None)
    ap.add_argument("--seed-literal", type=str, default=None)
    ap.add_argument("--seed-file", type=Path, default=DEFAULT_SEED_FILE)
    ap.add_argument("--out", type=Path, default=HERE / "results")
    ap.add_argument("--dev-analysis", type=Path, default=None)
    ap.add_argument("--max-concurrency", type=int, default=3)
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    if a.stage == "selftest":
        return selftest(a.out)
    if a.stage == "digest":
        tmp = a.out / "_digest_tmp"
        prepare(tmp, a.per_stratum or 3, int(a.seed_literal), ARMS, force=True)
        d = split_digest(tmp)
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"digest {d}")
        return 0
    if a.stage == "freeze":
        return freeze(a.dev_analysis, a.seed_file)
    if a.workdir is None:
        print("this stage needs --workdir", file=sys.stderr)
        return 2
    if a.stage == "prepare":
        if a.cell != "dev":
            print("use protected-prepare for the protected cell", file=sys.stderr)
            return 2
        f = prepare(a.workdir, a.per_stratum or DEV_PER_STRATUM, DEV_SEED, ARMS, a.force)
        print(f"prepared dev split: {f['task_count']} tasks, digest {split_digest(a.workdir)}")
        return 0
    if a.stage == "protected-prepare":
        rc = protected_guard(a.seed_file)
        if rc:
            return rc
        seed = a.seed_file.read_bytes().strip().decode()
        seed_int = int.from_bytes(hashlib.sha256(seed.encode()).digest()[:8], "big")
        f = prepare(a.workdir, a.per_stratum or PROTECTED_PER_STRATUM, seed_int, ARMS, a.force)
        archive_authorization(seed)
        write_json(a.workdir / "PROTECTED_IDENTITY.json", {"design_sha256": sha256_path(DESIGN_JSON),
                                                           "seed_sha256": sha256_text(seed), "split_digest": split_digest(a.workdir)})
        print(f"prepared protected split: {f['task_count']} tasks, digest {split_digest(a.workdir)}; authorization archived")
        return 0
    if a.stage == "gate-audit":
        audit = gate_audit(a.workdir)
        write_json(a.workdir / "GATE_AUDIT.json", audit)
        print(json.dumps({k: audit[k] for k in ("fires_on_every_task", "fired", "n_tasks", "control_read_false",
                                                  "identical_gate_input_within_each_pair")}))
        return 0 if audit["fires_on_every_task"] and audit["control_read_false"] else 1
    if a.stage == "dispatch":
        dispatch(a.workdir, ARMS, a.max_concurrency, a.overwrite)
        r = read_json(a.workdir / "DISPATCH_RECEIPT.json")
        print(f"dispatched {len(r['jobs'])} jobs; all_zero={r['all_returncodes_zero']} oracle_restored={r['oracle_restored_hash_match']}")
        return 0
    if a.stage == "evaluate":
        s = evaluate(a.workdir, ARMS)
        for arm, v in s.items():
            print(f"{arm}: {v['correct']}/{v['tasks']} valid={v['run_valid']} served={v['served_model_ids']} stops={v['stop_reasons']}")
        return 0
    if a.stage == "analyze":
        out = analyze(a.workdir, a.cell)
        a.out.mkdir(parents=True, exist_ok=True)
        path = a.out / f"H_EXT1R_{a.cell.upper()}_ANALYSIS_V1.json"
        write_json(path, out)
        print(f"{a.cell}: terminal={out['terminal']} written {path.name} sha256 {sha256_path(path)}")
        for s, v in out["per_stratum"].items():
            print(f"  {s}: " + "  ".join(f"{arm}={v[arm]['correct']}/{v[arm]['n']}" for arm in ARMS))
        print(f"  M vs PARENT (all): {out['m_vs_parent_all_gate_active']}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())

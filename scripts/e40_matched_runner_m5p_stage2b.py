#!/usr/bin/env python3
"""E40-m5' Stage-2b seed-replica stability-probe runner (m2 F2 + cycle-1 seed mandate).

Implements research/experiments/e40-matched/E40_M5P_STAGE2B_SEED_REPLICA_PROBE_DESIGN_V1
— a single-delta revival probe of the frozen E40 metabolic-drag negative
(m2 METABOLIC_DRAG_MATCHED_NATIVE, m3 drag robust to anchor, m4 channel
attribution, m5' Stage-1 GS1 not fired):
  - SIMPLE_DIRECT_CONTROL / F0_PARENT_FEDERATION_MATCHED are NOT re-run: the
    frozen m2 F0 chains are reused read-only as the reference (m3 precedent;
    the contrast stays single-delta: many-seed F2 vs frozen F0 federation).
  - F2_ORION_METABOLIC_FULL_MATCHED is run as K=4 independent seed-replicas per
    cell (f2r0..f2r3), 4 cycles each. The ONLY prompt difference from the
    frozen m2 F2 arm is the CYCLE-1 SEED MANDATE per replica (design §2.1):
    cycle 1 must carry the replica's frozen model_seed / partial_intervention_seed;
    every other knob stays model-orchestrated exactly as in m2; cycles 2-4
    prompts render byte-identical to m2 F2 given the replica's own history.
  - Mandate handling per m3 conventions: <=3 mandate re-asks with an explicit
    VIOLATION note; exhaustion => chain CANNOT_CHECK (excluded, counted,
    reported — never silently repaired).
Leakage rule is structural: decision code only ever sees redacted_feedback();
FORBIDDEN_SUBSTRINGS are asserted on every feedback WRITE and READ and on every
prompt before it leaves the process (executed, not logged). Truth
(quantitative_test_evaluation / wasserstein) is opened exclusively by the
frozen analysis script (research/experiments/e40-matched/e40_m5p_stage2b_analysis.py).
Model channel = the E60 lane (Anthropic-compatible endpoint via
~/.orion-campaign.env), identical call/retry mechanics to orion_claude_arms.py
and the m3 runner (temperature 0).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

K_CYCLES = 4
DATASETS = ["weissmann_k562", "weissmann_rpe1"]
REPS = 6
N_CELLS = len(DATASETS) * REPS
# Stage-2b: K=4 independent seed-replicas of the F2 arm per cell (design §2).
REPLICAS = ["f2r0", "f2r1", "f2r2", "f2r3"]
# Frozen seed table (design §2.1): replica -> (model_seed, partial_intervention_seed).
SEED_TABLE = {"f2r0": (11, 13), "f2r1": (29, 31), "f2r2": (47, 53), "f2r3": (71, 79)}
N_TASKS = N_CELLS * len(REPLICAS)  # 48 chains, 192 native runs
EXP_BASE = 503000  # design §8: own exp_id block (m2 500000s / m3 501000s)
TRAINING_REGIMES = ["observational", "partial_interventional", "interventional"]

# Frozen substrate (E40 R1 verbatim; pinned, NOT orchestratable; m2/m3-identical).
PINNED = {"model_name": "gies", "subset_data": 0.05, "max_path_length": -1, "do_filter": True}
FREE_KNOBS = ["training_regime", "fraction_partial_intervention", "partial_intervention_seed",
              "model_seed", "omission_estimation_size"]
KNOB_DOMAINS = """- training_regime: one of ["observational", "partial_interventional", "interventional"]
- fraction_partial_intervention: float in [0.0, 1.0] (only used when training_regime == "partial_interventional")
- partial_intervention_seed: integer in [0, 2147483647]
- model_seed: integer in [0, 2147483647]
- omission_estimation_size: integer in [0, 100000] (only affects false-omission-rate estimation, not the learned graph)"""

FORBIDDEN_SUBSTRINGS = ["quantitative_test_evaluation", "wasserstein", "false_omission_rate",
                        "negative_mean_wasserstein"]

BASE = Path(os.environ.get("E40M_BASE", "/projects/hep/fs9/users/scyiu/orion-v2-e45"))
ROOT = Path(os.environ.get("E40M_ROOT", str(BASE / "campaign-e40-m5p-stage2b")))
# Frozen e40-m2 reference: F0 chains (and their native results) are read-only
# reference for the analysis script; the runner never opens them.
M2_ROOT = Path(os.environ.get("E40M_REF", str(BASE / "campaign-e40-m2")))
CAUSALBENCH_SRC = Path(os.environ.get("E40M_SRC", str(BASE / "campaign-e40-r3/causalbench")))
VENV_PY = Path(os.environ.get("E40M_PY", str(BASE / "campaign-e40-r3/run/venv/bin/python")))
DATA_DIR = Path(os.environ.get("E40M_DATA", str(BASE / "datasets/causalbench/raw")))
DRY_RUN_TEMPLATE = BASE / "campaign-e40-r3/run/results/400000/metrics.json"
RESULTS = ROOT / "run/results"
CHAINS = ROOT / "run/chains"
CONTROLS = ROOT / "run/controls"


class ChainCannotCheck(Exception):
    """Infrastructure-level failure for one chain; recorded, never silently filled."""


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def assert_clean(text: str, *, where: str) -> None:
    """Executed leakage assert (design §7): no held-out channel string may pass."""
    for s in FORBIDDEN_SUBSTRINGS:
        if s in text:
            raise ChainCannotCheck(f"leakage assert failed at {where}: '{s}' present")


# ---------------------------------------------------------------- model channel
def _urlopen_with_retry(req: urllib.request.Request, *, timeout: int) -> Any:
    attempts = int(os.environ.get("ORION_ARM_HTTP_RETRIES", "8"))
    for attempt in range(attempts):
        try:
            return urllib.request.urlopen(req, timeout=timeout)
        except urllib.error.HTTPError as exc:
            if exc.code in {429, 503} and attempt + 1 < attempts:
                time.sleep(min(120.0, 2.0 ** attempt))
                continue
            raise
    raise RuntimeError("HTTP retries exhausted")


def anthropic_call(prompt: str) -> tuple[str, dict[str, int]]:
    """Verbatim mechanics of orion_claude_arms._anthropic_compatible_call (E60 lane)."""
    base = os.environ["ANTHROPIC_BASE_URL"].rstrip("/")
    url = base + ("/messages" if base.endswith("/v1") else "/v1/messages")
    body = json.dumps({
        "model": os.environ["ANTHROPIC_MODEL"],
        "max_tokens": int(os.environ.get("ORION_ARM_MAX_TOKENS", "6000")),
        "temperature": 0,
        "system": "You are a bounded experimental causal-discovery configuration arm. You only choose"
                  " configuration knobs. Never claim success, novelty, scientific truth, field status,"
                  " or publication readiness.",
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(url, data=body, headers={
        "x-api-key": os.environ["ANTHROPIC_AUTH_TOKEN"],
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    })
    with _urlopen_with_retry(req, timeout=int(os.environ.get("ORION_ARM_HTTP_TIMEOUT", "1800"))) as raw:
        data = json.load(raw)
    text = "".join(str(x.get("text", "")) for x in data.get("content", []) if isinstance(x, dict))
    usage = dict(data.get("usage", {}))
    usage["_model_id"] = str(data.get("model", ""))
    return text, usage


def extract_json(text: str) -> Any:
    starts = [(text.find("{"), "{"), (text.find("["), "[")]
    starts = [(i, c) for i, c in starts if i >= 0]
    if not starts:
        raise ValueError("model did not return a JSON object or array")
    _, open_char = min(starts)
    close_char = "}" if open_char == "{" else "]"
    start, end = text.find(open_char), text.rfind(close_char)
    if start < 0 or end < start:
        raise ValueError("model JSON is truncated")
    return json.loads(text[start:end + 1], strict=False)


# ------------------------------------------------------------ config validation
def validate_config(cfg: Any, *, rep: int) -> dict[str, Any]:
    if not isinstance(cfg, dict):
        raise ValueError("config must be a JSON object")
    out: dict[str, Any] = {}
    for key in ("training_regime", "fraction_partial_intervention", "partial_intervention_seed",
                "model_seed", "omission_estimation_size"):
        if key not in cfg:
            raise ValueError(f"config lacks knob {key}")
    tr = cfg["training_regime"]
    if tr not in TRAINING_REGIMES:
        raise ValueError(f"training_regime must be one of {TRAINING_REGIMES}")
    out["training_regime"] = tr
    frac = cfg["fraction_partial_intervention"]
    if not isinstance(frac, (int, float)) or isinstance(frac, bool) or not (0.0 <= float(frac) <= 1.0):
        raise ValueError("fraction_partial_intervention must be a float in [0.0, 1.0]")
    out["fraction_partial_intervention"] = round(float(frac), 4)
    for key, hi in (("partial_intervention_seed", 2147483647), ("model_seed", 2147483647),
                    ("omission_estimation_size", 100000)):
        v = cfg[key]
        if not isinstance(v, int) or isinstance(v, bool) or not (0 <= v <= hi):
            raise ValueError(f"{key} must be an integer in [0, {hi}]")
        out[key] = v
    for key in ("model_name", "subset_data", "max_path_length", "do_filter"):
        if key in cfg and cfg[key] != PINNED[key]:
            raise ValueError(f"{key} is pinned to {PINNED[key]!r}; orchestrating it is not allowed")
    return out


def full_config(free: dict[str, Any], dataset: str) -> dict[str, Any]:
    cfg = dict(PINNED)
    cfg.update(free)
    cfg["dataset_name"] = dataset
    return cfg


# -------------------------------------------------------------------- prompts
# substrate_header / f2_prompt body are VERBATIM from the frozen m2 runner
# (campaign-e40-m2/e40_matched_runner.py sha256 e13baa88…, whose only delta
# from scripts/e40_matched_runner.py is the gies pin); the header text —
# including its inherited "pc" wording — is kept byte-identical on purpose.
def substrate_header(dataset: str, rep: int) -> str:
    return f"""NATIVE SUBSTRATE (pinned, identical for every arm):
- causal discovery model: pc (CausalBench PC algorithm, pinned commit)
- dataset: {dataset} (pinned data, sha256-frozen)
- subset_data: 0.05, max_path_length: -1, do_filter: true (pinned; NOT orchestratable)
- chain rep index: {rep} (the SIMPLE control arm uses model_seed={rep} with the E40 R1 default config)

ORCHESTRATABLE KNOBS (the only degrees of freedom you may choose):
{KNOB_DOMAINS}

You are a configuration arm for a causal-discovery benchmark. The held-out
quantitative test score is NEVER shown to you. The only feedback you receive is
external-knowledge/diagnostic evaluation of previously run configs plus runtime.
Within each external-knowledge evaluation, higher true_positives mean better
recovery of known interactions; the feedback carries no held-out test information.
Do not claim success or scientific truth. Propose configs by reasoning about the
diagnostics only."""


def cycle1_rule(replica: str) -> str:
    """The ONLY prompt delta vs the frozen m2 F2 arm (design §2.1), cycle 1 only."""
    ms, ps = SEED_TABLE[replica]
    return ("\nCYCLE-1 RULE (binding): cycle 1 has no feedback yet; its two seed knobs are\n"
            f"mandated for this chain — model_seed MUST be {ms} and\n"
            f"partial_intervention_seed MUST be {ps} (exactly these integers). Every\n"
            "other knob (training_regime, fraction_partial_intervention,\n"
            "omission_estimation_size) is yours to choose as usual.\n")


def f2_prompt(dataset: str, rep: int, cycle: int, history: list[dict[str, Any]],
              replica: str) -> str:
    # Stage-2b single delta: the cycle-1 seed mandate per replica. Cycles 2+
    # render byte-identical to m2 F2 (empty rule string) given the replica's
    # own history. The replica index never enters the header.
    rule = cycle1_rule(replica) if cycle == 1 else ""
    lines = []
    for h in history:
        lines.append(f"--- cycle {h['cycle']} ---")
        lines.append("config: " + json.dumps(h["config"], sort_keys=True))
        lines.append("redacted feedback (external-knowledge diagnostics + runtime only):")
        lines.append(json.dumps(h["feedback"], sort_keys=True))
    hist = "\\n".join(lines) if lines else "(no runs yet: this is cycle 1)"
    return substrate_header(dataset, rep) + f"""

TASK (metabolic loop, feedback-driven): choose the configuration for cycle
{cycle} of {K_CYCLES}. You see the configs and redacted feedback of cycles
1..{cycle - 1} below. Choose the single next config. Re-using a previous config
is allowed: if one earlier config shows the strongest diagnostics so far,
choosing it again is a valid choice.{rule}

{hist}

Return ONLY one JSON object:
{{"config": {{...the 5 knobs...}}, "rationale": "<= 40 words", "uncertainty": "<= 20 words"}}"""


# ------------------------------------------------------------------- redaction
def redacted_feedback(metrics_path: Path) -> dict[str, Any]:
    with open(metrics_path) as fh:
        d = json.load(fh)
    if "quantitative_test_evaluation" not in d:
        raise ChainCannotCheck(f"{metrics_path} lacks quantitative_test_evaluation (unexpected metrics shape)")
    d.pop("quantitative_test_evaluation")
    blob = json.dumps(d, sort_keys=True)
    assert_clean(blob, where=f"redaction of {metrics_path}")
    return d


def read_feedback(fb_path: Path) -> dict[str, Any]:
    """Every feedback READ passes the executed leakage assert (design §7)."""
    text = fb_path.read_text()
    assert_clean(text, where=str(fb_path))
    return json.loads(text)


# ---------------------------------------------------------------- native driver
def native_run(cfg: dict[str, Any], exp_id: int, log_path: Path, *, dry_run: bool = False) -> Path:
    """Run one pinned-native invocation (m2/m3 verbatim); returns metrics.json path."""
    out_dir = RESULTS / str(exp_id)
    metrics = out_dir / "metrics.json"
    if metrics.exists():
        return metrics
    if dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", str(DRY_RUN_TEMPLATE), str(metrics)], check=True)
        (out_dir / "arguments.json").write_text(json.dumps({**cfg, "exp_id": str(exp_id)}))
        return metrics
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = ["/usr/bin/time", "-v", str(VENV_PY), "-m", "causalscbench.apps.main_app",
           "--output_directory", str(RESULTS), "--data_directory", str(DATA_DIR),
           "--model_name", cfg["model_name"], "--dataset_name", cfg["dataset_name"],
           "--training_regime", cfg["training_regime"],
           "--fraction_partial_intervention", str(cfg["fraction_partial_intervention"]),
           "--partial_intervention_seed", str(cfg["partial_intervention_seed"]),
           "--model_seed", str(cfg["model_seed"]),
           "--subset_data", str(cfg["subset_data"]), "--do_filter",
           "--max_path_length", str(cfg["max_path_length"]),
           "--omission_estimation_size", str(cfg["omission_estimation_size"]),
           "--exp_id", str(exp_id)]
    with open(log_path, "w") as log:
        log.write(" ".join(cmd) + "\n")
        log.flush()
        proc = subprocess.run(cmd, cwd=str(CAUSALBENCH_SRC), stdout=log, stderr=log)
    if proc.returncode != 0 or not metrics.exists():
        raise ChainCannotCheck(f"native run exp_id={exp_id} failed rc={proc.returncode}")
    return metrics


def ask_config(prompt: str, *, rep: int, attempts: int = 3) -> tuple[dict[str, Any], dict[str, Any]]:
    """One decision call with parse/validate retry (<=3). Returns (config, call-log)."""
    assert_clean(prompt, where="outgoing prompt")
    cur, logs = prompt, []
    last_err = None
    for attempt in range(attempts):
        text, usage = anthropic_call(cur)
        logs.append({"attempt": attempt, "prompt_sha256": sha256_text(cur),
                     "response_sha256": sha256_text(text),
                     "input_tokens": int(usage.get("input_tokens", 0)),
                     "output_tokens": int(usage.get("output_tokens", 0)),
                     "model_id": usage.get("_model_id", "")})
        try:
            parsed = extract_json(text)
            if not isinstance(parsed, dict):
                raise ValueError("expected a JSON object")
            return validate_config(parsed.get("config", parsed), rep=rep), \
                {"calls": logs, "response_text": text}
        except (ValueError, json.JSONDecodeError) as exc:
            last_err = str(exc)
            cur = (prompt + "\n\nYour previous reply was rejected by the validator: "
                   f"{last_err}\nReply again with ONLY the requested JSON, corrected.")
    raise ChainCannotCheck(f"decision call failed validation after {attempts} attempts: {last_err}")


def write_decision(cycle_dir: Path, *, cycle: int, prompt: str, decision: dict[str, Any],
                   configs: list[dict[str, Any]], dataset: str, replica: str) -> None:
    cycle_dir.mkdir(parents=True, exist_ok=True)
    (cycle_dir / "prompt.txt").write_text(prompt)
    # design §8 custody: prompt sha, raw response, call-log, model id, temperature 0
    (cycle_dir / "response.txt").write_text(str(decision.get("response_text", "")))
    (cycle_dir / "decision.json").write_text(json.dumps(
        {"cycle": cycle, "replica": replica, "prompt_sha256": sha256_text(prompt),
         "model": os.environ.get("ANTHROPIC_MODEL", ""), "temperature": 0,
         "response_sha256": sha256_text(str(decision.get("response_text", ""))),
         "call_log": decision["calls"], "configs": configs}, indent=1))
    for i, cfg in enumerate(configs, start=1):
        (cycle_dir / f"config_{i}.json").write_text(
            json.dumps(full_config(cfg, dataset), sort_keys=True))


def _cycle1_seeds_ok(cfg: dict[str, Any], replica: str) -> bool:
    """True iff the config carries EXACTLY the replica's mandated seed pair."""
    ms, ps = SEED_TABLE[replica]
    return cfg.get("model_seed") == ms and cfg.get("partial_intervention_seed") == ps


def violation_note(replica: str) -> str:
    ms, ps = SEED_TABLE[replica]
    return ("\n\nVIOLATION of the CYCLE-1 RULE: cycle 1 must carry model_seed = "
            f"{ms} and partial_intervention_seed = {ps} exactly. Reply again with ONLY "
            "the requested JSON, this time with those two seed values.")


def ask_config_f2(dataset: str, rep: int, cycle: int, history: list[dict[str, Any]],
                  replica: str, *, _ask: Any = None, mandate_attempts: int = 3
                  ) -> tuple[dict[str, Any], dict[str, Any], str]:
    """F2 decision call under the Stage-2b cycle-1 seed mandate (single delta on m2).

    Cycle-1 replies that do not carry the replica's mandated seed pair are
    re-asked with an explicit VIOLATION note (bounded, m3 convention).
    Exhausting the bound raises ChainCannotCheck — never a silent fill / repair.
    Returns (config, decision, prompt); the mandate transcript (asked/violations)
    is appended to decision["calls"] so write_decision freezes it in call_log."""
    ask = _ask or (lambda p: ask_config(p, rep=rep))
    prompt = f2_prompt(dataset, rep, cycle, history, replica)
    violations = 0
    for attempt in range(1, mandate_attempts + 1):
        cfg, decision = ask(prompt)
        if cycle != 1 or _cycle1_seeds_ok(cfg, replica):
            calls = list(decision.get("calls", []))
            if cycle == 1:
                calls.append({"mandate": "cycle1_seeds", "replica": replica,
                              "mandated": {"model_seed": SEED_TABLE[replica][0],
                                           "partial_intervention_seed": SEED_TABLE[replica][1]},
                              "asked": attempt, "violations": violations})
            return cfg, {**decision, "calls": calls}, prompt
        violations = attempt
        prompt = prompt + violation_note(replica)
    raise ChainCannotCheck(f"cycle-1 seed mandate exhausted: F2 replica {replica} did not carry "
                           f"seeds {SEED_TABLE[replica]} in all {mandate_attempts} attempts "
                           f"(dataset={dataset}, rep={rep})")


# ------------------------------------------------------------------ chain exec
_REGIME_CANON = {"observational": "obs", "partialinterventional": "partial",
                 "partialintervational": "partial", "interventional": "inter",
                 "intervational": "inter"}


def canon_regime(s: Any) -> str:
    return _REGIME_CANON.get(str(s).lower().replace("_", ""), f"UNKNOWN:{s}")


def task_split(task: int) -> tuple[str, int, str]:
    """Cell-major numbering: task = cell*4 + replica_index; cell = ds*6 + rep."""
    if not (0 <= task < N_TASKS):
        raise ValueError(f"task {task} outside [0, {N_TASKS})")
    cell, k = divmod(task, len(REPLICAS))
    return DATASETS[cell // REPS], cell % REPS, REPLICAS[k]


def chain_dir_for(task: int) -> Path:
    ds, rep, replica = task_split(task)
    return CHAINS / f"{task:02d}_{replica}_{ds}_{rep}"


def exp_id_for(task: int, cycle: int) -> int:
    return EXP_BASE + task * K_CYCLES + (cycle - 1)


def chain_done(chain_dir: Path) -> bool:
    return (chain_dir / "CHAIN_COMPLETE.json").exists()


def run_chain(task: int, *, dry_run: bool = False) -> dict[str, Any]:
    dataset, rep, replica = task_split(task)
    chain_dir = chain_dir_for(task)
    chain_dir.mkdir(parents=True, exist_ok=True)
    if chain_done(chain_dir):
        return {"task": task, "status": "ALREADY_COMPLETE"}
    (chain_dir / "CANNOT_CHECK.json").unlink(missing_ok=True)  # stale marker from an aborted pass
    cycles: list[dict[str, Any]] = []

    def execute(cfg_free: dict[str, Any], cycle: int) -> dict[str, Any]:
        cfg = full_config(cfg_free, dataset)
        cycle_dir = chain_dir / f"cycle{cycle}"
        cycle_dir.mkdir(parents=True, exist_ok=True)
        fb_path = cycle_dir / "redacted_feedback.json"
        if fb_path.exists():
            return {"cycle": cycle, "config": cfg_free, "feedback": read_feedback(fb_path)}
        exp_id = exp_id_for(task, cycle)
        metrics = native_run(cfg, exp_id, cycle_dir / "native.log", dry_run=dry_run)
        args_path = RESULTS / str(exp_id) / "arguments.json"
        if args_path.exists():
            ran = json.loads(args_path.read_text())
            for key in ("model_name", "training_regime", "subset_data", "max_path_length"):
                ran_v, cfg_v = str(ran.get(key)), str(cfg[key])
                if key == "training_regime":
                    if canon_regime(ran_v) != canon_regime(cfg_v):
                        raise ChainCannotCheck(f"exp_id={exp_id} arguments.json drift on {key}"
                                               f" (recorded {ran_v!r} vs passed {cfg_v!r})")
                elif ran_v != str(cfg[key]):
                    raise ChainCannotCheck(f"exp_id={exp_id} arguments.json drift on {key}")
            if cycle == 1:
                for key in ("model_seed", "partial_intervention_seed"):
                    if str(ran.get(key)) != str(cfg[key]):
                        raise ChainCannotCheck(f"exp_id={exp_id} arguments.json drift on {key}")
        fb = redacted_feedback(metrics)
        blob = json.dumps(fb, sort_keys=True)
        assert_clean(blob, where=f"feedback write {fb_path}")
        fb_path.write_text(blob)
        (cycle_dir / "exp_id").write_text(str(exp_id))
        return {"cycle": cycle, "config": cfg_free, "feedback": read_feedback(fb_path)}

    try:
        for cycle in range(1, K_CYCLES + 1):
            dec_path = chain_dir / f"cycle{cycle}" / "decision.json"
            if dec_path.exists():
                cfg_free = json.loads(dec_path.read_text())["configs"][0]
                if cycle == 1 and not _cycle1_seeds_ok(cfg_free, replica):
                    raise ChainCannotCheck(f"resumed cycle-1 decision violates the seed mandate "
                                           f"for {replica}: {cfg_free}")
            else:
                cfg_free, decision, prompt = ask_config_f2(dataset, rep, cycle, cycles, replica)
                write_decision(chain_dir / f"cycle{cycle}", cycle=cycle, prompt=prompt,
                               decision=decision, configs=[cfg_free], dataset=dataset,
                               replica=replica)
            cycles.append(execute(cfg_free, cycle))
    except ChainCannotCheck as exc:
        (chain_dir / "CANNOT_CHECK.json").write_text(json.dumps(
            {"task": task, "replica": replica, "dataset": dataset, "rep": rep, "error": str(exc)}))
        return {"task": task, "status": "CANNOT_CHECK", "error": str(exc)}

    (chain_dir / "CHAIN_COMPLETE.json").write_text(json.dumps(
        {"task": task, "arm": "F2_ORION_METABOLIC_FULL_MATCHED", "replica": replica,
         "dataset": dataset, "rep": rep,
         "exp_ids": [exp_id_for(task, c) for c in range(1, K_CYCLES + 1)]}))
    return {"task": task, "status": "COMPLETE"}


def status() -> dict[str, Any]:
    """Campaign progress census (poll target; no truth is opened here)."""
    rows = []
    for task in range(N_TASKS):
        d = chain_dir_for(task)
        if (d / "CHAIN_COMPLETE.json").exists():
            st = "COMPLETE"
        elif (d / "CANNOT_CHECK.json").exists():
            st = "CANNOT_CHECK"
        elif d.exists():
            st = "IN_PROGRESS"
        else:
            st = "MISSING"
        done = sum(1 for c in range(1, K_CYCLES + 1) if (d / f"cycle{c}" / "exp_id").exists())
        rows.append({"task": task, "chain": d.name, "status": st, "cycles_done": done})
    census = {k: sum(1 for r in rows if r["status"] == k)
              for k in ("COMPLETE", "CANNOT_CHECK", "IN_PROGRESS", "MISSING")}
    native = sum(r["cycles_done"] for r in rows)
    return {"chains": census, "native_runs_done": native, "native_runs_expected": N_TASKS * K_CYCLES,
            "all_settled": census["IN_PROGRESS"] == 0 and census["MISSING"] == 0,
            "rows": rows}


# ------------------------------------------------------------------ statistics
def perm_paired_p(diffs: list[float], *, n_perm: int = 5000, seed: int = 20260830) -> float:
    """Exact one-sided paired sign-flip permutation p (m2/m3 verbatim; enumerate when n<=16)."""
    n = len(diffs)
    if n == 0:
        return 1.0
    t_obs = sum(diffs) / n
    if n <= 16:
        total = 2 ** n
        count = 0
        for mask in range(total):
            t = sum(d if (mask >> i) & 1 else -d for i, d in enumerate(diffs)) / n
            if t >= t_obs:
                count += 1
        return count / total
    rng = random.Random(seed)
    count = 0
    for _ in range(n_perm):
        t = sum(d if rng.random() < 0.5 else -d for d in diffs) / n
        if t >= t_obs:
            count += 1
    return count / n_perm


# --------------------------------------------------------------------- controls
def control_planted(*, dry_run: bool = False) -> dict[str, Any]:
    """Positive control: planted-feedback replay (m2/m3 form, verbatim plant v4).

    The control runs the SAME prompted policy as the live arm, so it inherits
    the Stage-2b cycle-1 seed mandate (replica f2r0's pair). Plant:
    partial_interventional @ frac 0.8; quality = regime_factor(regime) *
    exp(-((frac-0.8)/0.45)**2), regime_factor partial 1.0 / observational 0.7 /
    interventional 0.55. PASS rule (terminal residence, 9-cycle replay): last 3
    cycles at planted quality >= 0.9 AND no post-arrival dip below 0.8.
    """
    import math
    out_dir = CONTROLS / "planted"
    out_dir.mkdir(parents=True, exist_ok=True)
    target = {"training_regime": "partial_interventional", "fraction_partial_intervention": 0.8}
    regime_factor = {"partial_interventional": 1.0, "observational": 0.7, "interventional": 0.55}
    replica = REPLICAS[0]

    def planted_quality(cfg: dict[str, Any]) -> float:
        return regime_factor[cfg["training_regime"]] * math.exp(
            -(((cfg["fraction_partial_intervention"] - 0.8) / 0.45) ** 2))

    def synth_feedback(cfg: dict[str, Any]) -> dict[str, Any]:
        q = planted_quality(cfg)
        return {"corum_evaluation": {"true_positives": round(5 + 40 * q, 1)},
                "string_network_evaluation": {"true_positives": round(4 + 30 * q, 1)},
                "string_physical_evaluation": {"true_positives": round(2 + 12 * q, 1)},
                "ligand_receptor_evaluation": {"true_positives": round(1 + 5 * q, 1)},
                "chipseq_evaluation": {"true_positives": round(3 + 20 * q, 1)},
                "pooled_biological_evaluation": {"true_positives": round(10 + 80 * q, 1)},
                "pooled_biological_sigificant_evaluation": {"true_positives": round(6 + 40 * q, 1)},
                "run_time": round(3600 - 1800 * q, 1)}

    history: list[dict[str, Any]] = []
    chosen: list[dict[str, Any]] = []
    try:
        for cycle in range(1, 10):
            cfg, decision, prompt = ask_config_f2("weissmann_k562", 0, cycle, history, replica)
            write_decision(out_dir / f"cycle{cycle}", cycle=cycle, prompt=prompt,
                           decision=decision, configs=[cfg], dataset="weissmann_k562",
                           replica=replica)
            chosen.append(cfg)
            history.append({"cycle": cycle, "config": cfg, "feedback": synth_feedback(cfg)})
    except ChainCannotCheck as exc:
        doc = {"control": "planted_feedback_recovery", "target": target,
               "verdict": "FAIL", "reason": f"cycle-1 seed mandate exhausted: {exc}"}
        (out_dir / "planted.json").write_text(json.dumps(doc, indent=1))
        return doc
    qualities = [planted_quality(c) for c in chosen]
    first_hi = next((i for i, q in enumerate(qualities) if q >= 0.9), None)
    terminal_residence = all(q >= 0.9 for q in qualities[-3:])
    no_regression = first_hi is None or all(q >= 0.8 for q in qualities[first_hi:])
    verdict = "PASS" if (terminal_residence and no_regression) else "FAIL"
    doc = {"control": "planted_feedback_recovery", "target": target, "replica_mandate": replica,
           "chosen": chosen, "qualities": qualities,
           "in_basin_0p8_count": sum(q >= 0.8 for q in qualities[1:]), "of": 8,
           "terminal_quality": qualities[-1], "verdict": verdict,
           "rule": "last 3 cycles at planted quality >= 0.9 AND no post-arrival dip below 0.8"}
    (out_dir / "planted.json").write_text(json.dumps(doc, indent=1))
    return doc


def control_nullcal(*, reps: int = 400, seed: int = 20260830) -> dict[str, Any]:
    """Machinery check (m2/m3 verbatim): exact permutation null rejects at ~alpha under H0."""
    rng = random.Random(seed)
    rejections = sum(1 for _ in range(reps)
                     if perm_paired_p([rng.gauss(0, 1) for _ in range(12)]) < 0.05)
    rate = rejections / reps
    verdict = "PASS" if 0.02 <= rate <= 0.09 else "FAIL"
    doc = {"control": "permutation_null_calibration", "reps": reps, "n_pairs": 12,
           "alpha": 0.05, "rejection_rate": rate, "accept_band": [0.02, 0.09], "verdict": verdict}
    CONTROLS.mkdir(parents=True, exist_ok=True)
    (CONTROLS / "nullcal.json").write_text(json.dumps(doc, indent=1))
    return doc


# ----------------------------------------------------------------------- audit
def audit() -> int:
    """Leakage + pin + seed-mandate audit over every arm-visible artifact."""
    violations: list[str] = []
    checked = 0
    for pattern in (CHAINS.glob("*/*/prompt.txt"), CHAINS.glob("*/*/redacted_feedback.json"),
                    CONTROLS.glob("*/prompt.txt"), CONTROLS.glob("*/*/prompt.txt")):
        for path in pattern:
            checked += 1
            text = path.read_text()
            for s in FORBIDDEN_SUBSTRINGS:
                if s in text:
                    violations.append(f"{path}: contains '{s}'")
    for cfg in list(CHAINS.glob("*/*/config_*.json")):
        checked += 1
        c = json.loads(cfg.read_text())
        if c.get("model_name") != PINNED["model_name"] or c.get("subset_data") != PINNED["subset_data"] \
                or c.get("max_path_length") != PINNED["max_path_length"]:
            violations.append(f"{cfg}: pinned-knob drift")
    for task in range(N_TASKS):
        d = chain_dir_for(task)
        if not (d / "CHAIN_COMPLETE.json").exists():
            continue
        checked += 1
        _, _, replica = task_split(task)
        c1 = d / "cycle1" / "config_1.json"
        if not c1.exists() or not _cycle1_seeds_ok(json.loads(c1.read_text()), replica):
            violations.append(f"{d}: COMPLETE chain whose cycle-1 config violates the {replica} seed mandate")
    print(json.dumps({"audit": "leakage+pin+seed-mandate", "artifacts_checked": checked,
                      "violations": violations}, indent=1))
    return 1 if violations else 0


# ------------------------------------------------------------- endpoint probe
def probe_endpoint() -> dict[str, Any]:
    """One-shot call proving the E60 lane answers; records the model id (receipt input)."""
    prompt = 'Reply with ONLY this JSON object and nothing else: {"ok": true}'
    t0 = time.time()
    try:
        text, usage = anthropic_call(prompt)
    except (urllib.error.HTTPError, urllib.error.URLError, RuntimeError) as exc:
        # diagnostics only; the chain path keeps m3's retry semantics untouched
        code = getattr(exc, "code", None)
        body = exc.read().decode(errors="replace")[:500] if hasattr(exc, "read") else str(exc)[:500]
        doc = {"probe": "endpoint_one_shot", "configured_model": os.environ.get("ANTHROPIC_MODEL", ""),
               "http_error": code, "error": type(exc).__name__, "body_head": body,
               "elapsed_s": round(time.time() - t0, 2),
               "parsed_ok": False, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        (ROOT / "run").mkdir(parents=True, exist_ok=True)
        (ROOT / "run/endpoint_probe.json").write_text(json.dumps(doc, indent=1))
        return doc
    doc = {"probe": "endpoint_one_shot", "configured_model": os.environ.get("ANTHROPIC_MODEL", ""),
           "response_model_id": usage.get("_model_id", ""), "temperature": 0,
           "elapsed_s": round(time.time() - t0, 2),
           "input_tokens": int(usage.get("input_tokens", 0)),
           "output_tokens": int(usage.get("output_tokens", 0)),
           "response_sha256": sha256_text(text), "response_head": text[:200],
           "parsed_ok": False, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    try:
        doc["parsed_ok"] = extract_json(text) == {"ok": True}
    except (ValueError, json.JSONDecodeError):
        pass
    (ROOT / "run").mkdir(parents=True, exist_ok=True)
    (ROOT / "run/endpoint_probe.json").write_text(json.dumps(doc, indent=1))
    return doc


# --------------------------------------------------------------------- selftest
def selftest() -> int:
    failures: list[str] = []
    good = {"training_regime": "observational", "fraction_partial_intervention": 0.3,
            "partial_intervention_seed": 1, "model_seed": 2, "omission_estimation_size": 500}
    if validate_config(good, rep=0) != {k: good[k] for k in good}:
        failures.append("validator rejects/mangles a good config")
    for bad, why in ((dict(good, training_regime="Experimental"), "bad regime"),
                     (dict(good, fraction_partial_intervention=1.5), "frac>1"),
                     (dict(good, model_seed=True), "bool seed"),
                     (dict(good, subset_data=0.5), "pinned-knob override"),
                     ({k: v for k, v in good.items() if k != "model_seed"}, "missing knob")):
        try:
            validate_config(bad, rep=0)
            failures.append(f"validator accepts {why}")
        except ValueError:
            pass
    for passed, recorded, same in (("observational", "Observational", True),
                                   ("partial_interventional", "PartialIntervational", True),
                                   ("interventional", "Interventional", True),
                                   ("partial_interventional", "Interventional", False),
                                   ("observational", "QuasiExperimental", False)):
        if (canon_regime(passed) == canon_regime(recorded)) != same:
            failures.append(f"regime canon mismatch: {passed!r} vs {recorded!r}")
    if DRY_RUN_TEMPLATE.exists():
        fb = redacted_feedback(DRY_RUN_TEMPLATE)
        if "quantitative_test_evaluation" in fb:
            failures.append("redaction left the held-out channel in feedback")
    else:
        print("SELFTEST_SKIPPED_redaction_on_LUNARC_only (template absent here)")
    p_planted = perm_paired_p([1.0] * 12)
    if abs(p_planted - 1.0 / 4096) > 1e-12:
        failures.append(f"perm p on all-positive diffs != 1/4096: {p_planted}")
    from math import comb
    p_null = perm_paired_p([1.0, -1.0] * 6)
    if abs(p_null - (0.5 + comb(12, 6) / 2 ** 13)) > 1e-12:
        failures.append(f"perm p on symmetric diffs != tie-inclusive exact value: {p_null}")
    # task numbering: 48 tasks <-> 12 cells x 4 replicas, exp_ids 503000..503191 disjoint
    seen = set()
    ids = set()
    for task in range(N_TASKS):
        seen.add(task_split(task))
        ids.update(exp_id_for(task, c) for c in range(1, K_CYCLES + 1))
    if len(seen) != N_TASKS or len(ids) != N_TASKS * K_CYCLES or min(ids) != EXP_BASE \
            or max(ids) != EXP_BASE + N_TASKS * K_CYCLES - 1:
        failures.append("task/exp_id numbering is not a clean bijection over 12x4x4")
    # seed mandate: exact pair passes; wrong pair re-asked; exhaustion raises; never binds at cycle 2+
    ok = {"training_regime": "interventional", "fraction_partial_intervention": 0.0,
          "partial_intervention_seed": 13, "model_seed": 11, "omission_estimation_size": 1000}
    wrong = dict(ok, model_seed=0)
    seq = iter([dict(wrong), dict(ok, partial_intervention_seed=0), dict(ok)])
    cfg_m, dec_m, pr = ask_config_f2("weissmann_k562", 0, 1, [], "f2r0",
                                     _ask=lambda p: (next(seq), {"calls": []}))
    if cfg_m != ok or dec_m["calls"][-1]["violations"] != 2 or dec_m["calls"][-1]["asked"] != 3:
        failures.append(f"mandate re-ask path wrong: {cfg_m} {dec_m}")
    if "VIOLATION of the CYCLE-1 RULE" not in pr or "model_seed = 11" not in pr:
        failures.append("mandate violation note never reached the prompt")
    try:
        ask_config_f2("weissmann_k562", 0, 1, [], "f2r1", _ask=lambda p: (dict(ok), {"calls": []}))
        failures.append("mandate exhaustion must raise ChainCannotCheck (f2r0 seeds offered to f2r1)")
    except ChainCannotCheck:
        pass
    c2, d2, p2 = ask_config_f2("weissmann_k562", 0, 2, [], "f2r3",
                               _ask=lambda p: (dict(wrong), {"calls": []}))
    if c2 != wrong or d2["calls"] or "CYCLE-1 RULE" in p2:
        failures.append("mandate must not bind (nor render) outside cycle 1")
    # prompt delta: cycle 1 carries exactly the replica's seed pair; cycles 2+ carry no rule;
    # the header never carries the replica index.
    for r, (ms, ps) in SEED_TABLE.items():
        p1 = f2_prompt("weissmann_rpe1", 3, 1, [], r)
        if f"model_seed MUST be {ms}" not in p1 or f"partial_intervention_seed MUST be {ps}" not in p1:
            failures.append(f"cycle-1 seed rule missing for {r}")
        if r in p1:
            failures.append(f"replica label {r} leaked into the prompt")
    hist = [{"cycle": 1, "config": ok, "feedback": {"pooled_biological_evaluation": {"true_positives": 1.0}}}]
    p2s = {r: f2_prompt("weissmann_k562", 0, 2, hist, r) for r in REPLICAS}
    if len(set(p2s.values())) != 1 or "CYCLE-1 RULE" in next(iter(p2s.values())):
        failures.append("cycle-2 prompts differ across replicas given identical history")
    # executed leakage asserts: feedback read, prompt send
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        bad_fb = Path(td) / "redacted_feedback.json"
        bad_fb.write_text(json.dumps({"x": {"wasserstein": 1}}))
        try:
            read_feedback(bad_fb)
            failures.append("feedback read must assert FORBIDDEN_SUBSTRINGS")
        except ChainCannotCheck:
            pass
        try:
            ask_config("prompt with quantitative_test_evaluation inside", rep=0)
            failures.append("outgoing prompt must assert FORBIDDEN_SUBSTRINGS")
        except ChainCannotCheck:
            pass
    print(json.dumps({"selftest": "e40_matched_runner_m5p_stage2b", "failures": failures}, indent=1))
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("chain"); p.add_argument("--task", type=int, required=True)
    p.add_argument("--dry-run", action="store_true")
    p = sub.add_parser("control-planted"); p.add_argument("--dry-run", action="store_true")
    sub.add_parser("control-nullcal")
    sub.add_parser("status"); sub.add_parser("audit"); sub.add_parser("selftest")
    sub.add_parser("probe-endpoint")
    args = ap.parse_args()
    if args.cmd == "chain":
        print(json.dumps(run_chain(args.task, dry_run=args.dry_run)))
        return 0
    if args.cmd == "control-planted":
        print(json.dumps(control_planted(dry_run=args.dry_run))); return 0
    if args.cmd == "control-nullcal":
        print(json.dumps(control_nullcal())); return 0
    if args.cmd == "status":
        st = status()
        print(json.dumps({k: v for k, v in st.items() if k != "rows"}, indent=1))
        return 0 if st["all_settled"] else 3
    if args.cmd == "probe-endpoint":
        doc = probe_endpoint()
        print(json.dumps(doc, indent=1))
        return 0 if doc["parsed_ok"] else 1
    if args.cmd == "audit":
        return audit()
    return selftest()


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""E40-M1 matched F0/F2 runner around the pinned native CausalBench learner.

Implements research/experiments/e40-matched/E40_MATCHED_F0_F2_PROSPECTIVE_DESIGN_V1:
  - SIMPLE_DIRECT_CONTROL: one native run, E40 R1 default config verbatim.
  - F0_PARENT_FEDERATION_MATCHED: all K=4 configs committed upfront, no feedback.
  - F2_ORION_METABOLIC_FULL_MATCHED: config k chosen after cycles 1..k-1 feedback,
    with quantitative_test_evaluation redacted from every arm-visible artifact.
Leakage rule is structural: decision code only ever sees redacted_feedback();
the full metrics.json is opened exclusively by rollup/controls scoring.
Model channel = the E60 lane (Anthropic-compatible endpoint via
~/.orion-campaign.env), identical call/retry mechanics to orion_claude_arms.py.
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
ARMS = ["SIMPLE_DIRECT_CONTROL", "F0_PARENT_FEDERATION_MATCHED", "F2_ORION_METABOLIC_FULL_MATCHED"]
ARM_SHORT = {"SIMPLE_DIRECT_CONTROL": "simple", "F0_PARENT_FEDERATION_MATCHED": "f0",
             "F2_ORION_METABOLIC_FULL_MATCHED": "f2"}
TRAINING_REGIMES = ["observational", "partial_interventional", "interventional"]

# Frozen substrate (E40 R1 verbatim; pinned, NOT orchestratable).
PINNED = {"model_name": "pc", "subset_data": 0.05, "max_path_length": -1, "do_filter": True}
SIMPLE_CONFIG = {
    "training_regime": "partial_interventional",
    "fraction_partial_intervention": 0.5,
    "partial_intervention_seed": 0,
    "omission_estimation_size": 500,
}
# Free knobs (design "orchestratable_knobs" minus the two it pins in fixed_flags:
# subset_data/max_path_length stay at E40 R1 values so compute and the statistical
# evaluator remain comparable across arms; resolution recorded in dispatch receipt).
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
ROOT = Path(os.environ.get("E40M_ROOT", str(BASE / "campaign-e40-m1")))
CAUSALBENCH_SRC = Path(os.environ.get("E40M_SRC", str(BASE / "campaign-e40-r3/causalbench")))
VENV_PY = Path(os.environ.get("E40M_PY", str(BASE / "campaign-e40-r3/run/venv/bin/python")))
DATA_DIR = Path(os.environ.get("E40M_DATA", str(BASE / "datasets/causalbench/raw")))
DRY_RUN_TEMPLATE = BASE / "campaign-e40-r3/run/results/400000/metrics.json"
RESULTS = ROOT / "run/results"
CHAINS = ROOT / "run/chains"
CONTROLS = ROOT / "run/controls"
ROLLUP_DIR = ROOT / "run/rollup"


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
    return text, dict(data.get("usage", {}))


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


def f0_prompt(dataset: str, rep: int) -> str:
    return substrate_header(dataset, rep) + f"""

TASK (parent federation, no feedback): commit, upfront and without seeing any
run feedback, all K={K_CYCLES} configurations for this chain. You may vary every
orchestratable knob freely across the {K_CYCLES} configs (including model_seed).
Return ONLY one JSON array of exactly {K_CYCLES} objects, each object:
{{"config": {{...the 5 knobs...}}, "rationale": "<= 40 words"}}"""


def f2_prompt(dataset: str, rep: int, cycle: int, history: list[dict[str, Any]]) -> str:
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
choosing it again is a valid choice.

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
    for s in FORBIDDEN_SUBSTRINGS:
        if s in blob:
            raise ChainCannotCheck(f"redaction failed: '{s}' present in feedback blob")
    return d


def primary_score(metrics_path: Path) -> dict[str, Any]:
    with open(metrics_path) as fh:
        d = json.load(fh)
    qte = d["quantitative_test_evaluation"]
    og = qte["output_graph"]
    return {
        "primary": float(og["wasserstein_distance"]["mean"]),
        "true_positives": int(og["true_positives"]),
        "false_positives": int(og["false_positives"]),
        "false_omission_rate": float(qte["false_omission_rate"]),
        "corum_tp": float(d["corum_evaluation"]["true_positives"]),
        "string_tp": float(d["string_network_evaluation"]["true_positives"]),
        "run_time": float(d["run_time"]),
    }


# ---------------------------------------------------------------- native driver
def native_run(cfg: dict[str, Any], exp_id: int, log_path: Path, *, dry_run: bool = False) -> Path:
    """Run one pinned-native invocation; returns the run's metrics.json path."""
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


def ask_config(prompt: str, *, want_array: bool, rep: int, attempts: int = 3) -> tuple[Any, dict[str, Any]]:
    """One decision call with parse/validate retry. Returns (parsed, call-log)."""
    cur, logs = prompt, []
    last_err = None
    for attempt in range(attempts):
        text, usage = anthropic_call(cur)
        logs.append({"attempt": attempt, "prompt_sha256": sha256_text(cur),
                     "response_sha256": sha256_text(text),
                     "input_tokens": int(usage.get("input_tokens", 0)),
                     "output_tokens": int(usage.get("output_tokens", 0))})
        try:
            parsed = extract_json(text)
            if want_array:
                if not isinstance(parsed, list) or len(parsed) != K_CYCLES:
                    raise ValueError(f"expected a JSON array of exactly {K_CYCLES} objects")
                objs = [validate_config(item.get("config", item), rep=rep) for item in parsed
                        if isinstance(item, dict)]
                if len(objs) != K_CYCLES:
                    raise ValueError("every array item must be an object with a 'config'")
                return objs, {"calls": logs, "response_text": text}
            if not isinstance(parsed, dict):
                raise ValueError("expected a JSON object")
            return validate_config(parsed.get("config", parsed), rep=rep), {"calls": logs, "response_text": text}
        except (ValueError, json.JSONDecodeError) as exc:
            last_err = str(exc)
            cur = (prompt + "\n\nYour previous reply was rejected by the validator: "
                   f"{last_err}\nReply again with ONLY the requested JSON, corrected.")
    raise ChainCannotCheck(f"decision call failed validation after {attempts} attempts: {last_err}")


def write_decision(cycle_dir: Path, *, cycle: int, prompt: str, decision: dict[str, Any],
                   configs: list[dict[str, Any]], dataset: str) -> None:
    cycle_dir.mkdir(parents=True, exist_ok=True)
    (cycle_dir / "prompt.txt").write_text(prompt)
    (cycle_dir / "decision.json").write_text(json.dumps(
        {"cycle": cycle, "prompt_sha256": sha256_text(prompt),
         "call_log": decision["calls"], "configs": configs}, indent=1))
    for i, cfg in enumerate(configs, start=1):
        (cycle_dir / f"config_{i}.json").write_text(
            json.dumps(full_config(cfg, dataset), sort_keys=True))


# ------------------------------------------------------------------ chain exec
# Upstream main_app accepts enum VALUES (partial_interventional) but serializes
# enum NAMES into arguments.json (PartialIntervational — upstream's own spelling;
# Interventional; Observational). Canonicalize explicitly: no mechanical mapping
# survives the upstream typo, and an unknown string must fail loud (drift).
_REGIME_CANON = {"observational": "obs", "partialinterventional": "partial",
                 "partialintervational": "partial", "interventional": "inter",
                 "intervational": "inter"}


def canon_regime(s: Any) -> str:
    return _REGIME_CANON.get(str(s).lower().replace("_", ""), f"UNKNOWN:{s}")


def task_split(task: int) -> tuple[str, str, int]:
    arm, ds, rep = ARMS[task // (len(DATASETS) * REPS)], DATASETS[(task // REPS) % len(DATASETS)], task % REPS
    return arm, ds, rep


def chain_done(chain_dir: Path) -> bool:
    return (chain_dir / "CHAIN_COMPLETE.json").exists()


def run_chain(task: int, *, dry_run: bool = False) -> dict[str, Any]:
    arm, dataset, rep = task_split(task)
    chain_dir = CHAINS / f"{task:02d}_{ARM_SHORT[arm]}_{dataset}_{rep}"
    chain_dir.mkdir(parents=True, exist_ok=True)
    if chain_done(chain_dir):
        return {"task": task, "status": "ALREADY_COMPLETE"}
    (chain_dir / "CANNOT_CHECK.json").unlink(missing_ok=True)  # stale marker from an aborted pass
    exp_base = 500000 + task * K_CYCLES
    cycles: list[dict[str, Any]] = []

    def execute(cfg_free: dict[str, Any], cycle: int, slot: int) -> dict[str, Any]:
        cfg = full_config(cfg_free, dataset)
        cycle_dir = chain_dir / f"cycle{cycle}" if arm != "F0_PARENT_FEDERATION_MATCHED" \
            else chain_dir / f"run{slot}"
        cycle_dir.mkdir(parents=True, exist_ok=True)
        fb_path = cycle_dir / "redacted_feedback.json"
        if fb_path.exists():
            return {"cycle": cycle, "config": cfg_free, "feedback": json.loads(fb_path.read_text())}
        exp_id = exp_base + slot
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
        fb = redacted_feedback(metrics)
        fb_path.write_text(json.dumps(fb, sort_keys=True))
        (cycle_dir / "exp_id").write_text(str(exp_id))
        return {"cycle": cycle, "config": cfg_free, "feedback": fb}

    try:
        if arm == "SIMPLE_DIRECT_CONTROL":
            execute({**SIMPLE_CONFIG, "model_seed": rep}, 1, 0)
        elif arm == "F0_PARENT_FEDERATION_MATCHED":
            decision_path = chain_dir / "cycle0_upfront.json"
            if decision_path.exists():
                doc = json.loads(decision_path.read_text())
                configs = doc["configs"]
            else:
                prompt = f0_prompt(dataset, rep)
                configs, decision = ask_config(prompt, want_array=True, rep=rep)
                write_decision(chain_dir / "upfront", cycle=0, prompt=prompt,
                               decision=decision, configs=configs, dataset=dataset)
                decision_path.write_text(json.dumps({"configs": configs}))
            for i, cfg in enumerate(configs):
                execute(cfg, i + 1, i)
        else:  # F2 metabolic
            for cycle in range(1, K_CYCLES + 1):
                dec_path = chain_dir / f"cycle{cycle}" / "decision.json"
                if dec_path.exists():
                    cfg_free = json.loads(dec_path.read_text())["configs"][0]
                else:
                    prompt = f2_prompt(dataset, rep, cycle, cycles)
                    cfg_free, decision = ask_config(prompt, want_array=False, rep=rep)
                    write_decision(chain_dir / f"cycle{cycle}", cycle=cycle, prompt=prompt,
                                   decision=decision, configs=[cfg_free], dataset=dataset)
                cycles.append(execute(cfg_free, cycle, cycle - 1))
    except ChainCannotCheck as exc:
        (chain_dir / "CANNOT_CHECK.json").write_text(json.dumps({"task": task, "error": str(exc)}))
        return {"task": task, "status": "CANNOT_CHECK", "error": str(exc)}

    (chain_dir / "CHAIN_COMPLETE.json").write_text(json.dumps({"task": task, "arm": arm,
                                                               "dataset": dataset, "rep": rep}))
    return {"task": task, "status": "COMPLETE"}


# ------------------------------------------------------------------ statistics
def perm_paired_p(diffs: list[float], *, n_perm: int = 5000, seed: int = 20260830) -> float:
    """Exact one-sided paired sign-flip permutation p (enumerate when n<=16).

    H0: arm labels exchangeable within each chain pair. Statistic T = mean(diffs),
    positive = F2 better (distances: comparator minus F2_final).
    """
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


def median(xs: list[float]) -> float:
    xs = sorted(xs)
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2.0


# --------------------------------------------------------------------- controls
def control_planted(*, dry_run: bool = False) -> dict[str, Any]:
    """Positive control: planted-feedback replay (channel-integrity check).

    Plant v4. The design freezes that the planted optimum be IDENTIFIABLE FROM THE
    FEEDBACK CHANNEL ALONE. Lessons v1-v3: (a) only probed configs emit feedback, so
    the basin must be wide enough for any two probes to reveal direction/scale; (b)
    a hard regime gate flattens the fraction gradient for wrong-regime probes and
    makes the whole far field read as noise; (c) the optimum must sit OFF the
    natural default anchor (partial@0.5) so blind/default pinning cannot pass; (d)
    the optimum must be semantically coherent (fraction_partial_intervention is
    inert under observational, so the target regime must be partial_interventional).
    Plant: partial_interventional @ frac 0.8; quality = regime_factor(regime) *
    exp(-((frac-0.8)/0.45)**2) with regime_factor partial 1.0 / observational 0.7 /
    interventional 0.55 — both axes legible from any probe.

    PASS rule (terminal residence, 9-cycle replay): the last 3 cycles each at
    planted quality >= 0.9 AND no cycle after the first quality >= 0.9 dips below
    0.8 — the loop must FIND the identifiable optimum and STAY in its >=90% basin.
    Early exploration is not penalized (convergence speed is the treatment's
    property, not the checker's). Default-anchored configs score 0.61 (fail);
    random configs pass with probability well under 1%.
    """
    import math
    out_dir = CONTROLS / "planted"
    out_dir.mkdir(parents=True, exist_ok=True)
    target = {"training_regime": "partial_interventional", "fraction_partial_intervention": 0.8}
    regime_factor = {"partial_interventional": 1.0, "observational": 0.7, "interventional": 0.55}

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
    for cycle in range(1, 10):
        prompt = f2_prompt("weissmann_k562", 0, cycle, history)
        cfg, decision = ask_config(prompt, want_array=False, rep=0)
        write_decision(out_dir / f"cycle{cycle}", cycle=cycle, prompt=prompt,
                       decision=decision, configs=[cfg], dataset="weissmann_k562")
        chosen.append(cfg)
        history.append({"cycle": cycle, "config": cfg, "feedback": synth_feedback(cfg)})
    qualities = [planted_quality(c) for c in chosen]
    first_hi = next((i for i, q in enumerate(qualities) if q >= 0.9), None)
    terminal_residence = all(q >= 0.9 for q in qualities[-3:])
    no_regression = first_hi is None or all(q >= 0.8 for q in qualities[first_hi:])
    verdict = "PASS" if (terminal_residence and no_regression) else "FAIL"
    doc = {"control": "planted_feedback_recovery", "target": target,
           "chosen": chosen, "qualities": qualities,
           "in_basin_0p8_count": sum(q >= 0.8 for q in qualities[1:]), "of": 8,
           "terminal_quality": qualities[-1], "verdict": verdict,
           "rule": "last 3 cycles at planted quality >= 0.9 AND no post-arrival dip below 0.8"}
    (out_dir / "planted.json").write_text(json.dumps(doc, indent=1))
    return doc


def control_nullcal(*, reps: int = 400, seed: int = 20260830) -> dict[str, Any]:
    """Machinery check: exact permutation null must reject at ~alpha under H0."""
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


def _iter_feedback_files() -> list[Path]:
    return sorted(CHAINS.glob("*/*/redacted_feedback.json"))


def control_uninformative(*, dry_run: bool = False) -> dict[str, Any]:
    """No-fabrication control: blind replay with mismatched (other-dataset) feedback."""
    other_ds = {"weissmann_k562": "weissmann_rpe1", "weissmann_rpe1": "weissmann_k562"}
    pool: dict[str, list[Path]] = {"weissmann_k562": [], "weissmann_rpe1": []}
    for fb in _iter_feedback_files():
        for ds in pool:
            if other_ds[ds] in fb.parent.parent.name:  # feedback FROM the other dataset
                pool[ds].append(fb)
    out_dir = CONTROLS / "uninformative"
    out_dir.mkdir(parents=True, exist_ok=True)
    missing = [ds for ds in DATASETS if not pool[ds]]
    if missing:
        doc = {"control": "uninformative_feedback_blind_replay",
               "verdict": "CANNOT_CHECK__NO_FEEDBACK_POOL",
               "missing_datasets": missing,
               "hint": "F2 chains must complete first (redacted feedback files build the pool)"}
        (out_dir / "uninformative.json").write_text(json.dumps(doc, indent=1))
        return doc
    rows: list[dict[str, Any]] = []
    idx = 0
    for ds in DATASETS:
        for rep in range(REPS):
            history: list[dict[str, Any]] = []
            for cycle in range(1, K_CYCLES + 1):
                prompt = f2_prompt(ds, rep, cycle, history)
                cfg, decision = ask_config(prompt, want_array=False, rep=rep)
                write_decision(out_dir / f"{ds}_{rep}" / f"cycle{cycle}", cycle=cycle,
                               prompt=prompt, decision=decision, configs=[cfg], dataset=ds)
                src = pool[ds][(idx * 7 + cycle * 13) % len(pool[ds])]
                history.append({"cycle": cycle, "config": cfg,
                                "feedback": json.loads(src.read_text())})
            exp_id = 500200 + idx
            metrics = native_run(full_config(cfg, ds), exp_id,
                                 out_dir / f"{ds}_{rep}" / "native.log", dry_run=dry_run)
            rows.append({"dataset": ds, "rep": rep, "exp_id": exp_id,
                         "blind_final_config": cfg, "blind": primary_score(metrics)})
            idx += 1
    doc = {"control": "uninformative_feedback_blind_replay", "feedback_rule":
           "cycle feedback drawn from other-dataset runs only (mismatched config+dataset)",
           "chains": rows}
    (out_dir / "uninformative.json").write_text(json.dumps(doc, indent=1))
    return doc


def control_verdicts() -> dict[str, Any]:
    out = {}
    for name, fname in (("planted", "planted/planted.json"), ("nullcal", "nullcal.json"),
                        ("uninformative", "uninformative/uninformative.json")):
        p = CONTROLS / fname
        out[name] = json.loads(p.read_text()) if p.exists() else None
    return out


# ----------------------------------------------------------------------- audit
def audit() -> int:
    """Leakage audit: no held-out channel string in any arm-visible INPUT artifact."""
    violations: list[str] = []
    checked = 0
    for pattern in (CHAINS.glob("*/*/prompt.txt"), CHAINS.glob("*/upfront/prompt.txt"),
                    CHAINS.glob("*/*/redacted_feedback.json"),
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
    print(json.dumps({"audit": "leakage+pin", "artifacts_checked": checked,
                      "violations": violations}, indent=1))
    return 1 if violations else 0


# ----------------------------------------------------------------------- rollup
def _score_runs(chain_dir: Path, run_names: list[str]) -> list[dict[str, Any]]:
    scores = []
    for name in run_names:
        exp_id = (chain_dir / name / "exp_id").read_text().strip()
        scores.append({"run": name, "exp_id": int(exp_id),
                       **primary_score(RESULTS / exp_id / "metrics.json")})
    return scores


def collect_chains() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for task in range(len(ARMS) * len(DATASETS) * REPS):
        arm, ds, rep = task_split(task)
        chain_dir = CHAINS / f"{task:02d}_{ARM_SHORT[arm]}_{ds}_{rep}"
        entry: dict[str, Any] = {"arm": arm, "dataset": ds, "rep": rep}
        if not (chain_dir / "CHAIN_COMPLETE.json").exists():
            entry["status"] = "CANNOT_CHECK" if (chain_dir / "CANNOT_CHECK.json").exists() else "MISSING"
            out[f"{ds}:{rep}:{ARM_SHORT[arm]}"] = entry
            continue
        if arm == "SIMPLE_DIRECT_CONTROL":
            entry["status"] = "COMPLETE"
            entry["runs"] = _score_runs(chain_dir, ["cycle1"])
        elif arm == "F0_PARENT_FEDERATION_MATCHED":
            entry["status"] = "COMPLETE"
            entry["runs"] = _score_runs(chain_dir, [f"run{i}" for i in range(K_CYCLES)])
        else:
            entry["status"] = "COMPLETE"
            entry["runs"] = _score_runs(chain_dir, [f"cycle{i}" for i in range(1, K_CYCLES + 1)])
        out[f"{ds}:{rep}:{ARM_SHORT[arm]}"] = entry
    return out


def _best_by_primary(runs: list[dict[str, Any]]) -> dict[str, Any]:
    return min(runs, key=lambda r: r["primary"])


def rollup() -> dict[str, Any]:
    chains = collect_chains()
    pairs: list[dict[str, Any]] = []
    for ds in DATASETS:
        for rep in range(REPS):
            key = f"{ds}:{rep}"
            s, f0, f2 = chains[f"{key}:simple"], chains[f"{key}:f0"], chains[f"{key}:f2"]
            if not all(x.get("status") == "COMPLETE" for x in (s, f0, f2)):
                pairs.append({"dataset": ds, "rep": rep, "status": "INCOMPLETE",
                              "missing": [x.get("status") for x in (s, f0, f2)]})
                continue
            f0_best, f2_final = _best_by_primary(f0["runs"]), f2["runs"][-1]
            pairs.append({
                "dataset": ds, "rep": rep, "status": "COMPLETE",
                "simple": s["runs"][0],
                "f0_best": f0_best, "f0_mean": {k: sum(r[k] for r in f0["runs"]) / len(f0["runs"])
                                                for k in ("primary", "true_positives", "false_positives",
                                                          "false_omission_rate", "corum_tp", "string_tp")},
                "f0_all": f0["runs"],
                "f2_final": f2_final, "f2_best": _best_by_primary(f2["runs"]), "f2_all": f2["runs"],
                "d_primary": f0_best["primary"] - f2_final["primary"]})

    complete = [p for p in pairs if p.get("status") == "COMPLETE"]
    doc: dict[str, Any] = {
        "schema_version": "orion.v2.e40-matched.rollup.v1",
        "primary": "mean wasserstein_distance.mean of quantitative_test_evaluation.output_graph (lower better)",
        "chain_statistics": {"pairs_total": len(pairs), "pairs_complete": len(complete)},
        "controls": control_verdicts(),
    }
    if len(complete) >= 8:
        diffs = [p["d_primary"] for p in complete]
        doc["primary_comparison"] = {
            "contrast": "F2_final vs F0_best (conservative)",
            "mean_d": sum(diffs) / len(diffs), "perm_p_exact": perm_paired_p(diffs),
            "wins_f2": sum(1 for d in diffs if d > 0), "wins_f0": sum(1 for d in diffs if d < 0)}
        for label, pick in (("both_best", lambda p: p["f0_best"]["primary"] - p["f2_best"]["primary"]),
                            ("both_final", lambda p: p["f0_mean"]["primary"] - p["f2_final"]["primary"])):
            dd = [pick(p) for p in complete]
            doc.setdefault("secondary_comparisons", {})[label] = {
                "mean_d": sum(dd) / len(dd), "perm_p_exact": perm_paired_p(dd)}
        for metric in ("true_positives", "false_positives", "false_omission_rate", "corum_tp", "string_tp"):
            dd = [p["f0_best"][metric] - p["f2_final"][metric] for p in complete]
            doc.setdefault("secondary_metrics", {})[metric] = {
                "contrast": "F0_best - F2_final", "mean_d": sum(dd) / len(dd),
                "perm_p_exact": perm_paired_p(dd)}
        collapse = {}
        for ds in DATASETS:
            f2_tps = [p["f2_final"]["true_positives"] for p in complete if p["dataset"] == ds]
            s_tps = [p["simple"]["true_positives"] for p in complete if p["dataset"] == ds]
            collapse[ds] = {"f2_final_median_tp": median(f2_tps), "simple_median_tp": median(s_tps),
                            "passes": bool(f2_tps and s_tps and median(f2_tps) >= median(s_tps))}
        doc["per_dataset_collapse_check"] = collapse
        pc = doc["primary_comparison"]
        controls_ok = (doc["controls"]["planted"] or {}).get("verdict") == "PASS" and \
                      (doc["controls"]["nullcal"] or {}).get("verdict") == "PASS"
        if not controls_ok:
            doc["gate"] = "CHECKER_INVALID__NO_VERDICT"
        elif pc["mean_d"] > 0 and pc["perm_p_exact"] < 0.05 and all(c["passes"] for c in collapse.values()):
            uninf = doc["controls"]["uninformative"]
            if uninf is None:
                doc["gate"] = "BLOCKED_PENDING_CONTROLS"
            else:
                rows = [r for r in uninf["chains"]
                        if any(p["dataset"] == r["dataset"] and p["rep"] == r["rep"] for p in complete)]
                if len(rows) < 8:
                    doc["gate"] = "CHECKER_INVALID__NO_VERDICT"
                    doc["no_fabrication_control_detail"] = {"error": "too few joinable blind rows"}
                else:
                    blind_d = [r["blind"]["primary"] for r in rows]
                    informed_d = [next(p["f2_final"]["primary"] for p in complete
                                       if p["dataset"] == r["dataset"] and p["rep"] == r["rep"]) for r in rows]
                    blind_vs_f0b = [next(p["f0_best"]["primary"] for p in complete
                                         if p["dataset"] == r["dataset"] and p["rep"] == r["rep"]) - b
                                    for r, b in zip(rows, blind_d)]
                    no_fab = median([b - i for b, i in zip(blind_d, informed_d)]) >= 0 and \
                        perm_paired_p(blind_vs_f0b) >= 0.05
                    doc["no_fabrication_control_detail"] = {
                        "blind_minus_informed_median": median([b - i for b, i in zip(blind_d, informed_d)]),
                        "blind_vs_f0_best_perm_p": perm_paired_p(blind_vs_f0b)}
                    doc["gate"] = "F2_METABOLIC_ADVANTAGE_MATCHED_NATIVE" if no_fab else \
                        "CHECKER_INVALID__NO_VERDICT"
        elif pc["mean_d"] > 0:
            doc["gate"] = "NO_DETECTED_ADVANTAGE_MATCHED_NATIVE"
        else:
            doc["gate"] = "METABOLIC_DRAG_MATCHED_NATIVE"
    else:
        doc["gate"] = "CANNOT_CHECK__TOO_FEW_COMPLETE_PAIRS"
    ROLLUP_DIR.mkdir(parents=True, exist_ok=True)
    (ROLLUP_DIR / "E40_MATCHED_ROLLUP_V1.json").write_text(json.dumps(doc, indent=1))
    lines = ["# E40_MATCHED_ROLLUP_V1", "",
             f"- gate: `{doc['gate']}`",
             f"- pairs complete: {doc['chain_statistics']['pairs_complete']}/{doc['chain_statistics']['pairs_total']}",
             f"- primary contrast: {json.dumps(doc.get('primary_comparison', {}), indent=1)}",
             f"- controls: planted={(doc['controls']['planted'] or {}).get('verdict')}, "
             f"nullcal={(doc['controls']['nullcal'] or {}).get('verdict')}, "
             f"uninformative={'present' if doc['controls']['uninformative'] else 'absent'}",
             "", "## Pairs", "",
             "| dataset | rep | d_primary (F0best−F2final) |", "|---|---|---|"]
    for p in complete:
        lines.append(f"| {p['dataset']} | {p['rep']} | {p['d_primary']:+.6f} |")
    (ROLLUP_DIR / "E40_MATCHED_ROLLUP_V1.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"gate": doc["gate"], "pairs": doc["chain_statistics"],
                      "primary": doc.get("primary_comparison")}, indent=1))
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
    # custody canonicalization: upstream records enum NAMES (incl. its
    # 'PartialIntervational' spelling) while the CLI takes enum VALUES
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
        s = primary_score(DRY_RUN_TEMPLATE)
        if not (0.0 < s["primary"] < 1.0):
            failures.append(f"primary score implausible: {s['primary']}")
    else:
        print("SELFTEST_SKIPPED_redaction_on_LUNARC_only (template absent here)")
    p_planted = perm_paired_p([1.0] * 12)
    if abs(p_planted - 1.0 / 4096) > 1e-12:
        failures.append(f"perm p on all-positive diffs != 1/4096: {p_planted}")
    # Tie-inclusive exact p on [1,-1]*6: symmetric half plus half the tie mass
    # (924 of 4096 sign-flips give t=0), i.e. 0.5 + C(12,6)/2^13.
    from math import comb
    p_null = perm_paired_p([1.0, -1.0] * 6)
    if abs(p_null - (0.5 + comb(12, 6) / 2 ** 13)) > 1e-12:
        failures.append(f"perm p on symmetric diffs != tie-inclusive exact value: {p_null}")
    print(json.dumps({"selftest": "e40_matched_runner", "failures": failures}, indent=1))
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("chain"); p.add_argument("--task", type=int, required=True)
    p.add_argument("--dry-run", action="store_true")
    p = sub.add_parser("control-planted"); p.add_argument("--dry-run", action="store_true")
    sub.add_parser("control-nullcal")
    p = sub.add_parser("control-uninformative"); p.add_argument("--dry-run", action="store_true")
    sub.add_parser("rollup"); sub.add_parser("audit"); sub.add_parser("selftest")
    args = ap.parse_args()
    if args.cmd == "chain":
        print(json.dumps(run_chain(args.task, dry_run=args.dry_run)))
        return 0
    if args.cmd == "control-planted":
        print(json.dumps(control_planted(dry_run=args.dry_run))); return 0
    if args.cmd == "control-nullcal":
        print(json.dumps(control_nullcal())); return 0
    if args.cmd == "control-uninformative":
        print(json.dumps(control_uninformative(dry_run=args.dry_run))); return 0
    if args.cmd == "rollup":
        rollup(); return 0
    if args.cmd == "audit":
        return audit()
    return selftest()


if __name__ == "__main__":
    sys.exit(main())

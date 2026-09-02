#!/usr/bin/env python3
"""E40-m5' Stage-2d planted-control cause discrimination (frozen with design V1).

Implements research/experiments/e40-matched/E40_M5P_STAGE2D_PLANT_DISCRIMINATION_DESIGN_V1.
Stage-2c's registered planted positive control FAILED (terminal quality 0.6412 vs 0.9877 in m3,
1.0 in m2) and left TWO non-excluded candidate causes: the served model channel, and the cycle-1
mandate text (m2 had none, m3 the regime anchor, Stage-2c the seed mandate). This script varies
the rule axis with the model axis held fixed on the CURRENT served model:

  A_NO_MANDATE     cycle-1 rule: none                (m2 form)
  B_REGIME_ANCHOR  cycle-1 rule: regime extreme      (m3 form)
  C_SEED_MANDATE   cycle-1 rule: seeds 11/13         (Stage-2c f2r0 form)

3 arms x 9 cycles = 27 model decision calls, temperature 0, ZERO native runs. The plant (v4), the
synthetic feedback and the PASS rule are inherited verbatim from m2/m3/Stage-2c and are not re-tuned.

Control-gating (design §5; repairs the disclosed Stage-2c defect): evaluate_gates() CONSUMES the
control verdicts and refuses to file any D-gate when a registered control fails, returning
CHECKER_INVALID__NO_VERDICT with the D-gates NOT_EVALUATED. A selftest fixture proves the refusal.

No-rescue (design §8): mechanics diagnostic only. It does not revive the E40 line, does not
authorize m6, does not alter the Stage-2c CHECKER_INVALID disposition, and makes no claim about the
metabolic-drag hypothesis or the seed-replica probe.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

CYCLES = 9
# Inherited prompt quirk: m2/m3/Stage-2c planted controls ran 9 cycles while REUSING the live
# prompt builder, so their text always read "cycle c of 4". Arm C must be byte-identical to what
# Stage-2c actually sent, so the rendered horizon stays 4 while the loop runs CYCLES=9. Changing it
# would add a second inter-arm difference and break the discrimination.
PROMPT_HORIZON = 4
ARMS = ["A_NO_MANDATE", "B_REGIME_ANCHOR", "C_SEED_MANDATE"]
SEED_C = (11, 13)  # Stage-2c replica f2r0 (model_seed, partial_intervention_seed)
PLANT_DATASET, PLANT_REP = "weissmann_k562", 0
SERVED_MODEL = os.environ.get("E40M_SERVED_MODEL", "glm-5.3")
TRAINING_REGIMES = ["observational", "partial_interventional", "interventional"]
PINNED = {"model_name": "gies", "subset_data": 0.05, "max_path_length": -1, "do_filter": True}
FORBIDDEN_SUBSTRINGS = ["quantitative_test_evaluation", "wasserstein", "false_omission_rate",
                        "negative_mean_wasserstein"]
KNOB_DOMAINS = """- training_regime: one of ["observational", "partial_interventional", "interventional"]
- fraction_partial_intervention: float in [0.0, 1.0] (only used when training_regime == "partial_interventional")
- partial_intervention_seed: integer in [0, 2147483647]
- model_seed: integer in [0, 2147483647]
- omission_estimation_size: integer in [0, 100000] (only affects false-omission-rate estimation, not the learned graph)"""

# Plant v4 (m2/m3/Stage-2c verbatim)
PLANT_TARGET = {"training_regime": "partial_interventional", "fraction_partial_intervention": 0.8}
REGIME_FACTOR = {"partial_interventional": 1.0, "observational": 0.7, "interventional": 0.55}

# PLANT_INTEGRITY known answer: m3's RECORDED planted trajectory and qualities
# (research/experiments/e40-matched/rollup-m3/eval-3554985.out, verdict PASS, terminal 0.9877302162356105).
M3_RECORDED_CONFIGS = [("interventional", 0.0), ("partial_interventional", 0.5),
                       ("partial_interventional", 0.5), ("partial_interventional", 0.75),
                       ("partial_interventional", 0.9), ("partial_interventional", 0.75),
                       ("partial_interventional", 0.75), ("partial_interventional", 0.75),
                       ("partial_interventional", 0.75)]
M3_RECORDED_QUALITIES = [
    0.02332263739822093,
    0.6411803884299545,
    0.6411803884299545,
    0.9877302162356105,
    0.9518167844230893,
    0.9877302162356105,
    0.9877302162356105,
    0.9877302162356105,
    0.9877302162356105,
]

BASE = Path(os.environ.get("E40M_BASE", "/projects/hep/fs9/users/scyiu/orion-v2-e45"))
ROOT = Path(os.environ.get("E40M_ROOT", str(BASE / "campaign-e40-m5p-stage2d")))
OUT_DIR = Path(os.environ.get("E40M5P2D_OUT", str(ROOT / "rollup")))

_MANIFEST: list[dict] = []


class ArmCannotCheck(Exception):
    """Infrastructure-level failure for one arm; recorded, never silently filled."""


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _sha(path: Path) -> str:
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    _MANIFEST.append({"path": str(path), "sha256": h})
    return h


def assert_clean(text: str, *, where: str) -> None:
    for s in FORBIDDEN_SUBSTRINGS:
        if s in text:
            raise ArmCannotCheck(f"leakage assert failed at {where}: '{s}' present")


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


def assert_served_model(served: str) -> None:
    """Hard pin on the SERVED id (Stage-2c §2.2): the endpoint substitutes silently."""
    if served != SERVED_MODEL:
        raise ArmCannotCheck(f"served model {served!r} != frozen SERVED_MODEL {SERVED_MODEL!r} "
                             f"(requested {os.environ.get('ANTHROPIC_MODEL', '')!r})")


def anthropic_call(prompt: str) -> tuple[str, dict[str, Any]]:
    """Verbatim E60-lane mechanics (orion_claude_arms / m3 / Stage-2c), temperature 0."""
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
    served = str(data.get("model", ""))
    usage["_model_id"] = served
    assert_served_model(served)
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


def validate_config(cfg: Any, *, rep: int) -> dict[str, Any]:
    """Verbatim m2/m3/Stage-2c validator."""
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


# -------------------------------------------------------------------- prompts
def substrate_header(dataset: str, rep: int) -> str:
    """Verbatim m2/m3/Stage-2c header (its inherited 'pc' wording included, deliberately)."""
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


RULE_B = ("\nCYCLE-1 RULE (binding): cycle 1 has no feedback yet, so spend it on\n"
          "coverage rather than refinement — training_regime MUST be an axis\n"
          "extreme: \"observational\" or \"interventional\" (NOT \"partial_interventional\").\n"
          "Interior partial-intervention fractions are reserved for cycles 2+,\n"
          "once feedback exists.\n")
RULE_C = ("\nCYCLE-1 RULE (binding): cycle 1 has no feedback yet; its two seed knobs are\n"
          f"mandated for this chain — model_seed MUST be {SEED_C[0]} and\n"
          f"partial_intervention_seed MUST be {SEED_C[1]} (exactly these integers). Every\n"
          "other knob (training_regime, fraction_partial_intervention,\n"
          "omission_estimation_size) is yours to choose as usual.\n")
VIOLATION_B = ("\n\nVIOLATION of the CYCLE-1 RULE: cycle 1 must sit on a regime extreme — "
               "training_regime \"observational\" or \"interventional\" "
               "(NOT \"partial_interventional\"). Reply again with ONLY the requested "
               "JSON, this time choosing a cycle-1 extreme regime.")
VIOLATION_C = ("\n\nVIOLATION of the CYCLE-1 RULE: cycle 1 must carry model_seed = "
               f"{SEED_C[0]} and partial_intervention_seed = {SEED_C[1]} exactly. Reply again with ONLY "
               "the requested JSON, this time with those two seed values.")
ARM_RULE = {"A_NO_MANDATE": "", "B_REGIME_ANCHOR": RULE_B, "C_SEED_MANDATE": RULE_C}


def f2_prompt(dataset: str, rep: int, cycle: int, history: list[dict[str, Any]], arm: str) -> str:
    """m2/m3/Stage-2c prompt body, verbatim; the arm supplies only the cycle-1 rule string."""
    rule = ARM_RULE[arm] if cycle == 1 else ""
    lines = []
    for h in history:
        lines.append(f"--- cycle {h['cycle']} ---")
        lines.append("config: " + json.dumps(h["config"], sort_keys=True))
        lines.append("redacted feedback (external-knowledge diagnostics + runtime only):")
        lines.append(json.dumps(h["feedback"], sort_keys=True))
    hist = "\\n".join(lines) if lines else "(no runs yet: this is cycle 1)"
    return substrate_header(dataset, rep) + f"""

TASK (metabolic loop, feedback-driven): choose the configuration for cycle
{cycle} of {PROMPT_HORIZON}. You see the configs and redacted feedback of cycles
1..{cycle - 1} below. Choose the single next config. Re-using a previous config
is allowed: if one earlier config shows the strongest diagnostics so far,
choosing it again is a valid choice.{rule}

{hist}

Return ONLY one JSON object:
{{"config": {{...the 5 knobs...}}, "rationale": "<= 40 words", "uncertainty": "<= 20 words"}}"""


def mandate_ok(cfg: dict[str, Any], arm: str) -> bool:
    if arm == "B_REGIME_ANCHOR":
        return cfg.get("training_regime") in ("observational", "interventional")
    if arm == "C_SEED_MANDATE":
        return cfg.get("model_seed") == SEED_C[0] and cfg.get("partial_intervention_seed") == SEED_C[1]
    return True


# ----------------------------------------------------------------------- plant
def planted_quality(cfg: dict[str, Any]) -> float:
    return REGIME_FACTOR[cfg["training_regime"]] * math.exp(
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


def plant_verdict(qualities: list[float]) -> str:
    """m2/m3/Stage-2c PASS rule, verbatim."""
    if len(qualities) < 3:
        return "FAIL"
    first_hi = next((i for i, q in enumerate(qualities) if q >= 0.9), None)
    terminal_residence = all(q >= 0.9 for q in qualities[-3:])
    no_regression = first_hi is None or all(q >= 0.8 for q in qualities[first_hi:])
    return "PASS" if (terminal_residence and no_regression) else "FAIL"


# ------------------------------------------------------------------- execution
def ask_config(prompt: str, *, attempts: int = 3) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    assert_clean(prompt, where="outgoing prompt")
    cur, logs, last_err = prompt, [], None
    for attempt in range(attempts):
        text, usage = anthropic_call(cur)
        logs.append({"attempt": attempt, "prompt_sha256": sha256_text(cur),
                     "response_sha256": sha256_text(text), "model_id": usage.get("_model_id", ""),
                     "input_tokens": int(usage.get("input_tokens", 0)),
                     "output_tokens": int(usage.get("output_tokens", 0)), "response_text": text})
        try:
            parsed = extract_json(text)
            if not isinstance(parsed, dict):
                raise ValueError("expected a JSON object")
            return validate_config(parsed.get("config", parsed), rep=PLANT_REP), logs
        except (ValueError, json.JSONDecodeError) as exc:
            last_err = str(exc)
            cur = (prompt + "\n\nYour previous reply was rejected by the validator: "
                   f"{last_err}\nReply again with ONLY the requested JSON, corrected.")
    raise ArmCannotCheck(f"decision call failed validation after {attempts} attempts: {last_err}")


def ask_cycle(arm: str, cycle: int, history: list[dict[str, Any]], *, _ask: Any = None,
              mandate_attempts: int = 3) -> tuple[dict[str, Any], list[dict[str, Any]], str]:
    ask = _ask or (lambda p: ask_config(p))
    prompt = f2_prompt(PLANT_DATASET, PLANT_REP, cycle, history, arm)
    violations = 0
    for attempt in range(1, mandate_attempts + 1):
        cfg, logs = ask(prompt)
        if cycle != 1 or mandate_ok(cfg, arm):
            logs = list(logs)
            if cycle == 1:
                logs.append({"mandate": arm, "asked": attempt, "violations": violations})
            return cfg, logs, prompt
        violations = attempt
        prompt = prompt + (VIOLATION_B if arm == "B_REGIME_ANCHOR" else VIOLATION_C)
    raise ArmCannotCheck(f"cycle-1 mandate exhausted for {arm} after {mandate_attempts} attempts")


def run_arm(arm: str) -> dict[str, Any]:
    arm_dir = ROOT / arm
    if (arm_dir / "arm.json").exists():
        return {"arm": arm, "status": "ALREADY_RUN", **json.loads((arm_dir / "arm.json").read_text())}
    arm_dir.mkdir(parents=True, exist_ok=True)
    history: list[dict[str, Any]] = []
    chosen: list[dict[str, Any]] = []
    try:
        for cycle in range(1, CYCLES + 1):
            cfg, logs, prompt = ask_cycle(arm, cycle, history)
            cyd = arm_dir / f"cycle{cycle}"
            cyd.mkdir(exist_ok=True)
            cyd.joinpath("prompt.txt").write_text(prompt)
            cyd.joinpath("response.txt").write_text(str(logs[-2].get("response_text", ""))
                                                    if cycle == 1 and len(logs) > 1
                                                    else str(logs[-1].get("response_text", "")))
            cyd.joinpath("decision.json").write_text(json.dumps(
                {"arm": arm, "cycle": cycle, "prompt_sha256": sha256_text(prompt),
                 "model": os.environ.get("ANTHROPIC_MODEL", ""), "temperature": 0,
                 "call_log": [{k: v for k, v in c.items() if k != "response_text"} for c in logs],
                 "config": cfg}, indent=1))
            fb = synth_feedback(cfg)
            blob = json.dumps(fb, sort_keys=True)
            assert_clean(blob, where=f"synthetic feedback {cyd}")
            cyd.joinpath("feedback.json").write_text(blob)
            chosen.append(cfg)
            history.append({"cycle": cycle, "config": cfg, "feedback": fb})
    except ArmCannotCheck as exc:
        doc = {"arm": arm, "status": "CANNOT_CHECK", "error": str(exc),
               "cycles_done": len(chosen), "chosen": chosen}
        arm_dir.joinpath("arm.json").write_text(json.dumps(doc, indent=1))
        return doc
    qualities = [planted_quality(c) for c in chosen]
    doc = {"arm": arm, "status": "COMPLETE", "cycles_done": len(chosen), "chosen": chosen,
           "qualities": qualities, "terminal_quality": qualities[-1],
           "verdict": plant_verdict(qualities),
           "distinct_configs": len({json.dumps(c, sort_keys=True) for c in chosen}),
           "distinct_fracs": sorted({c["fraction_partial_intervention"] for c in chosen}),
           "distinct_regimes": sorted({c["training_regime"] for c in chosen}),
           "first_cycle_ge_0p9": next((i + 1 for i, q in enumerate(qualities) if q >= 0.9), None)}
    arm_dir.joinpath("arm.json").write_text(json.dumps(doc, indent=1))
    return doc


# ---------------------------------------------------------------------- controls
def control_plant_integrity() -> dict[str, Any]:
    """Known answer: m3's RECORDED trajectory must replay to m3's RECORDED qualities and PASS."""
    cfgs = [{"training_regime": r, "fraction_partial_intervention": f} for r, f in M3_RECORDED_CONFIGS]
    got = [planted_quality(c) for c in cfgs]
    dmax = max(abs(a - b) for a, b in zip(got, M3_RECORDED_QUALITIES))
    verdict = "PASS" if (dmax <= 1e-12 and plant_verdict(got) == "PASS"
                         and abs(planted_quality({**PLANT_TARGET}) - 1.0) <= 1e-12) else "FAIL"
    return {"control": "PLANT_INTEGRITY", "max_abs_delta_vs_m3_recorded": dmax,
            "replayed_verdict": plant_verdict(got), "optimum_quality": planted_quality({**PLANT_TARGET}),
            "verdict": verdict}


def control_served_model_pin(arms: dict[str, dict]) -> dict[str, Any]:
    per_arm, bad = {}, []
    for arm in ARMS:
        ids: list[str] = []
        for cyd in sorted((ROOT / arm).glob("cycle*/decision.json")):
            _sha(cyd)
            for call in json.loads(cyd.read_text()).get("call_log", []):
                if "model_id" in call:
                    ids.append(str(call["model_id"]))
        per_arm[arm] = {"calls_logged": len(ids), "ids": sorted(set(ids))}
        if not ids:
            bad.append(f"{arm}: no served-model record")
        bad += [f"{arm}: served {m!r}" for m in sorted(set(ids)) if m != SERVED_MODEL]
    return {"control": "SERVED_MODEL_PIN", "pinned": SERVED_MODEL, "per_arm": per_arm,
            "violations": bad, "verdict": "PASS" if not bad else "FAIL"}


def control_leakage() -> dict[str, Any]:
    checked, bad = 0, []
    for arm in ARMS:
        for p in sorted((ROOT / arm).glob("cycle*/prompt.txt")) + \
                 sorted((ROOT / arm).glob("cycle*/feedback.json")):
            checked += 1
            _sha(p)
            text = p.read_text()
            bad += [f"{p}: '{s}'" for s in FORBIDDEN_SUBSTRINGS if s in text]
    return {"control": "LEAKAGE", "artifacts_checked": checked, "violations": bad,
            "verdict": "PASS" if not bad else "FAIL"}


def control_trajectory_replay(arms: dict[str, dict]) -> dict[str, Any]:
    bad = []
    for arm, doc in arms.items():
        if doc.get("status") != "COMPLETE":
            continue
        recomputed = [planted_quality(c) for c in doc["chosen"]]
        if any(abs(a - b) > 1e-12 for a, b in zip(recomputed, doc["qualities"])) \
                or len(recomputed) != len(doc["qualities"]):
            bad.append(arm)
        if plant_verdict(recomputed) != doc["verdict"]:
            bad.append(f"{arm}:verdict")
    return {"control": "TRAJECTORY_REPLAY", "mismatched_arms": bad,
            "verdict": "PASS" if not bad else "FAIL"}


# ------------------------------------------------------------------------ gates
NOT_EVALUATED = "NOT_EVALUATED"


def evaluate_gates(arms: dict[str, dict], controls: dict[str, dict]) -> dict[str, Any]:
    """CONSUMES the control verdicts (design §5). A failed registered control refuses every D-gate."""
    failed = sorted(name for name, c in controls.items() if c.get("verdict") != "PASS")
    if failed:
        return {"D0_ARMS_VALID": NOT_EVALUATED, "D1_MODEL_CHANNEL_CAUSE": NOT_EVALUATED,
                "D2_PROMPT_IMPLICATED": NOT_EVALUATED,
                "D3_STAGE2C_FAILURE_NOT_REPRODUCED": NOT_EVALUATED,
                "failed_controls": failed, "disposition": "CHECKER_INVALID__NO_VERDICT",
                "ambiguous": True,
                "route": ("a registered control failed; no cause may be filed. Diagnose the control "
                          "failure under a separate freeze before re-running this diagnostic.")}
    d0 = all(arms.get(a, {}).get("status") == "COMPLETE" and arms[a].get("cycles_done") == CYCLES
             for a in ARMS)
    if not d0:
        return {"D0_ARMS_VALID": False, "D1_MODEL_CHANNEL_CAUSE": NOT_EVALUATED,
                "D2_PROMPT_IMPLICATED": NOT_EVALUATED,
                "D3_STAGE2C_FAILURE_NOT_REPRODUCED": NOT_EVALUATED, "failed_controls": [],
                "disposition": "CANNOT_CHECK", "ambiguous": True,
                "route": "an arm did not complete 9 cycles; no cause is filed (AMBIGUOUS)"}
    v = {a: arms[a]["verdict"] for a in ARMS}
    c_fail = v["C_SEED_MANDATE"] == "FAIL"
    d1 = c_fail and v["A_NO_MANDATE"] == "FAIL" and v["B_REGIME_ANCHOR"] == "FAIL"
    d2 = c_fail and (v["A_NO_MANDATE"] == "PASS" or v["B_REGIME_ANCHOR"] == "PASS")
    d3 = not c_fail
    if d1:
        disp, amb, route = ("MODEL_CHANNEL_CAUSE", False,
                            "failure is mandate-independent on this model: the served model channel is the "
                            "cause. A future E40 freeze must restore a channel that passes the planted "
                            "control before any probe verdict can be read.")
    elif d2:
        disp, amb, route = ("PROMPT_IMPLICATED", False,
                            "the cycle-1 mandate text is implicated: the model channel alone does not explain "
                            "the Stage-2c failure. A future freeze must revise the mandate form, not the plant.")
    else:
        disp, amb, route = ("STAGE2C_FAILURE_NOT_REPRODUCED", True,
                            "AMBIGUOUS: the Stage-2c failure did not reproduce under nominally identical "
                            "conditions, so the cause is NOT identified; channel non-determinism becomes the "
                            "leading explanation and must be characterised under a separate freeze.")
    return {"D0_ARMS_VALID": True, "D1_MODEL_CHANNEL_CAUSE": d1, "D2_PROMPT_IMPLICATED": d2,
            "D3_STAGE2C_FAILURE_NOT_REPRODUCED": d3, "failed_controls": [], "arm_verdicts": v,
            "disposition": disp, "ambiguous": amb, "route": route}


def load_arms() -> dict[str, dict]:
    out = {}
    for arm in ARMS:
        p = ROOT / arm / "arm.json"
        if p.exists():
            _sha(p)
            out[arm] = json.loads(p.read_text())
        else:
            out[arm] = {"arm": arm, "status": "MISSING"}
    return out


def analyze(*, write: bool = True) -> tuple[int, dict]:
    _MANIFEST.clear()
    arms = load_arms()
    controls = {c["control"]: c for c in (control_plant_integrity(),
                                          control_served_model_pin(arms),
                                          control_leakage(),
                                          control_trajectory_replay(arms))}
    gates = evaluate_gates(arms, controls)
    rollup = {"schema_version": "orion.v2.e40-matched.m5p-stage2d-rollup.v1",
              "variant": "e40-m5p-stage2d-plant-cause-discrimination",
              "design": "E40_M5P_STAGE2D_PLANT_DISCRIMINATION_DESIGN_V1",
              "served_model_pinned": SERVED_MODEL, "campaign_root": str(ROOT),
              "arms": arms, "controls": controls, "gates": gates,
              "stage2c_reference": {"planted_terminal_quality": 0.6411803884299545, "verdict": "FAIL",
                                    "disposition": "CHECKER_INVALID__NO_VERDICT (unchanged by this run)"},
              "manifest": {"n_files": len(_MANIFEST), "files": _MANIFEST}}
    if write:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        (OUT_DIR / "E40_M5P_STAGE2D_ROLLUP_V1.json").write_text(json.dumps(rollup, indent=1, sort_keys=True))
        lines = ["# E40-m5' Stage-2d planted-control cause discrimination — rollup V1", "",
                 f"disposition: **{gates['disposition']}**", f"ambiguous: {gates['ambiguous']}",
                 f"route: {gates['route']}", "",
                 "| arm | verdict | terminal quality | distinct configs | distinct fracs |",
                 "|---|---|---|---|---|"]
        for a in ARMS:
            d = arms[a]
            if d.get("status") == "COMPLETE":
                lines.append(f"| {a} | {d['verdict']} | {d['terminal_quality']:.4f} | "
                             f"{d['distinct_configs']} | {d['distinct_fracs']} |")
            else:
                lines.append(f"| {a} | {d.get('status')} | – | – | – |")
        lines += ["", "## controls", json.dumps({k: v["verdict"] for k, v in controls.items()}, indent=1),
                  "", "## gates", json.dumps(gates, indent=1, sort_keys=True)]
        (OUT_DIR / "E40_M5P_STAGE2D_ROLLUP_V1.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"disposition": gates["disposition"], "ambiguous": gates["ambiguous"],
                      "arm_verdicts": gates.get("arm_verdicts"),
                      "controls": {k: v["verdict"] for k, v in controls.items()}}, indent=1))
    return (0 if gates["disposition"] in ("MODEL_CHANNEL_CAUSE", "PROMPT_IMPLICATED",
                                          "STAGE2C_FAILURE_NOT_REPRODUCED") else 3), rollup


# --------------------------------------------------------------------- selftest
def _fixture_arm(arm: str, cfgs: list[tuple[str, float]], *, served: str = SERVED_MODEL,
                 cycles: int | None = None) -> None:
    d = ROOT / arm
    d.mkdir(parents=True, exist_ok=True)
    chosen = [{"training_regime": r, "fraction_partial_intervention": f,
               "partial_intervention_seed": SEED_C[1], "model_seed": SEED_C[0],
               "omission_estimation_size": 1000} for r, f in cfgs]
    for i, cfg in enumerate(chosen, start=1):
        cyd = d / f"cycle{i}"
        cyd.mkdir(exist_ok=True)
        cyd.joinpath("prompt.txt").write_text(f2_prompt(PLANT_DATASET, PLANT_REP, i, [], arm))
        cyd.joinpath("feedback.json").write_text(json.dumps(synth_feedback(cfg), sort_keys=True))
        cyd.joinpath("decision.json").write_text(json.dumps(
            {"arm": arm, "cycle": i, "call_log": [{"attempt": 0, "model_id": served}], "config": cfg}))
    q = [planted_quality(c) for c in chosen]
    d.joinpath("arm.json").write_text(json.dumps(
        {"arm": arm, "status": "COMPLETE", "cycles_done": cycles or len(chosen), "chosen": chosen,
         "qualities": q, "terminal_quality": q[-1], "verdict": plant_verdict(q),
         "distinct_configs": len({json.dumps(c, sort_keys=True) for c in chosen}),
         "distinct_fracs": sorted({c["fraction_partial_intervention"] for c in chosen}),
         "distinct_regimes": sorted({c["training_regime"] for c in chosen}),
         "first_cycle_ge_0p9": next((i + 1 for i, x in enumerate(q) if x >= 0.9), None)}, indent=1))


PASS_TRAJ = [("interventional", 0.0)] + [("partial_interventional", 0.8)] * 8
FAIL_TRAJ = [("interventional", 0.5)] * 6 + [("partial_interventional", 0.5)] * 3


def selftest() -> int:
    import tempfile
    failures: list[str] = []
    records: dict[str, Any] = {}
    g = globals()

    ci = control_plant_integrity()
    records["PLANT_INTEGRITY"] = ci
    if ci["verdict"] != "PASS":
        failures.append(f"plant known-answer replay of m3's recorded trajectory failed: {ci}")
    if plant_verdict([planted_quality({"training_regime": r, "fraction_partial_intervention": f})
                      for r, f in FAIL_TRAJ]) != "FAIL":
        failures.append("PASS rule accepts the Stage-2c-shaped failing trajectory")

    def scenario(name: str, traj: dict[str, list[tuple[str, float]]], *, served: dict | None = None,
                 cycles: dict | None = None, break_plant: bool = False) -> dict:
        with tempfile.TemporaryDirectory() as td:
            saved_root, saved_out = g["ROOT"], g["OUT_DIR"]
            g["ROOT"], g["OUT_DIR"] = Path(td) / "run", Path(td) / "out"
            saved_rf = dict(REGIME_FACTOR)
            try:
                for arm in ARMS:
                    _fixture_arm(arm, traj[arm], served=(served or {}).get(arm, SERVED_MODEL),
                                 cycles=(cycles or {}).get(arm))
                if break_plant:
                    REGIME_FACTOR["partial_interventional"] = 0.5  # corrupt the plant
                rc, doc = analyze(write=True)
                assert (g["OUT_DIR"] / "E40_M5P_STAGE2D_ROLLUP_V1.json").exists(), "rollup not written"
                return {"rc": rc, "gates": doc["gates"],
                        "controls": {k: v["verdict"] for k, v in doc["controls"].items()}}
            finally:
                REGIME_FACTOR.clear(); REGIME_FACTOR.update(saved_rf)
                g["ROOT"], g["OUT_DIR"] = saved_root, saved_out

    # D1: every arm fails
    r = scenario("all_fail", {a: FAIL_TRAJ for a in ARMS})
    records["D1_all_fail"] = r
    if not (r["gates"]["D1_MODEL_CHANNEL_CAUSE"] and r["gates"]["disposition"] == "MODEL_CHANNEL_CAUSE"
            and r["gates"]["ambiguous"] is False):
        failures.append(f"all-fail fixture must fire D1: {r['gates']}")
    # D2: C fails, A passes
    r = scenario("prompt", {"A_NO_MANDATE": PASS_TRAJ, "B_REGIME_ANCHOR": FAIL_TRAJ,
                            "C_SEED_MANDATE": FAIL_TRAJ})
    records["D2_prompt"] = r
    if not (r["gates"]["D2_PROMPT_IMPLICATED"] and r["gates"]["disposition"] == "PROMPT_IMPLICATED"):
        failures.append(f"C-fail/A-pass fixture must fire D2: {r['gates']}")
    # D3: C passes -> ambiguous, not reproduced
    r = scenario("notrepro", {a: PASS_TRAJ for a in ARMS})
    records["D3_not_reproduced"] = r
    if not (r["gates"]["D3_STAGE2C_FAILURE_NOT_REPRODUCED"] and r["gates"]["ambiguous"] is True
            and r["gates"]["disposition"] == "STAGE2C_FAILURE_NOT_REPRODUCED"):
        failures.append(f"C-pass fixture must fire D3 and be flagged ambiguous: {r['gates']}")
    # D0: short arm -> CANNOT_CHECK, no cause filed
    r = scenario("short", {a: FAIL_TRAJ for a in ARMS}, cycles={"B_REGIME_ANCHOR": 4})
    records["D0_short_arm"] = r
    if not (r["gates"]["D0_ARMS_VALID"] is False and r["gates"]["disposition"] == "CANNOT_CHECK"
            and r["gates"]["D1_MODEL_CHANNEL_CAUSE"] == NOT_EVALUATED and r["rc"] == 3):
        failures.append(f"short arm must yield CANNOT_CHECK with no cause: {r['gates']}")
    # CONTROL-GATING (the required refusal): substituted served model
    r = scenario("served_bad", {a: FAIL_TRAJ for a in ARMS}, served={"C_SEED_MANDATE": "glm-5.2"})
    records["control_gate_served"] = r
    if not (r["gates"]["disposition"] == "CHECKER_INVALID__NO_VERDICT"
            and r["gates"]["failed_controls"] == ["SERVED_MODEL_PIN"]
            and all(r["gates"][k] == NOT_EVALUATED for k in
                    ("D0_ARMS_VALID", "D1_MODEL_CHANNEL_CAUSE", "D2_PROMPT_IMPLICATED",
                     "D3_STAGE2C_FAILURE_NOT_REPRODUCED"))
            and r["gates"]["ambiguous"] is True and r["rc"] == 3):
        failures.append(f"substituted served model must refuse every D-gate: {r['gates']}")
    # CONTROL-GATING: broken plant
    r = scenario("plant_bad", {a: FAIL_TRAJ for a in ARMS}, break_plant=True)
    records["control_gate_plant"] = r
    if not (r["gates"]["disposition"] == "CHECKER_INVALID__NO_VERDICT"
            and "PLANT_INTEGRITY" in r["gates"]["failed_controls"]
            and r["gates"]["D1_MODEL_CHANNEL_CAUSE"] == NOT_EVALUATED):
        failures.append(f"broken plant must refuse every D-gate: {r['gates']}")

    print(json.dumps({"selftest": "e40_m5p_stage2d", "records": records, "failures": failures},
                     indent=1, default=str))
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("run"); p.add_argument("--arm", choices=ARMS + ["all"], default="all")
    sub.add_parser("analyze"); sub.add_parser("selftest")
    args = ap.parse_args(argv)
    if args.cmd == "run":
        arms = ARMS if args.arm == "all" else [args.arm]
        out = [run_arm(a) for a in arms]
        print(json.dumps([{k: v for k, v in d.items() if k not in ("chosen", "qualities")}
                          for d in out], indent=1))
        return 0 if all(d.get("status") in ("COMPLETE", "ALREADY_RUN") for d in out) else 3
    if args.cmd == "analyze":
        return analyze()[0]
    return selftest()


if __name__ == "__main__":
    sys.exit(main())

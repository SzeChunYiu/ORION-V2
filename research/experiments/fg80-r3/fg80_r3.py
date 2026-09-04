#!/usr/bin/env python3
"""FG80 R3 — the P-F negative, attributed to one stage and re-tested prospectively.

Two things live here, kept apart on purpose:

  census    A DESCRIPTIVE, NON-GATING re-read of the frozen FM/FG R2 evaluation rows
            (archived under ./archive with sha256 custody against the billy-old
            originals).  It asks one question of every wrong row: is the actual answer
            the expected answer rendered differently?  It changes no registered
            terminal.  Its output is the diagnosis the R3 design is built on.

  freeze / run / evaluate
            A NEW prospective identity: 80 fresh FG80 tasks from a committed seed, the
            same five arms, the same single-call budget, the same exact-match scorer --
            with ONE change, applied to every arm identically: the categorical endpoint
            crosses the interface AS a categorical (the admissible values are named in
            the contract and enforced by the output schema).  The lever is on the
            interface, not on any arm's procedure and not on the scorer.

Exit codes -- "could not check" keeps its own code:
  0  measured / frozen / dispatched
  1  a registered gate did not fire (evaluate)
  2  usage error
  5  CANNOT_CHECK (a control failed; an envelope is invalid; the served model drifted)
  6  channel unavailable: no dispatch happened, nothing scored
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ARCHIVE = HERE / "archive"
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import orion_formal_discovery_arms as R2ARMS  # noqa: E402  (frozen R2 procedure text, read-only)
import run_formal_discovery_generated_suite as R2SUITE  # noqa: E402  (frozen generator, read-only)

DESIGN_JSON = HERE / "FG80_R3_INTERFACE_RERUN_DESIGN_V1.json"
CENSUS_OUT = HERE / "FG80_R2_RENDERING_CENSUS_V1.json"
DEFAULT_WORKDIR = HERE / ".fg80-r3-run"

ARMS = ("TARGET_ONLY_DIRECT", "STRONGEST_DOMAIN_FORMAL_PARENT", "F0_PARENT_FEDERATION",
        "F2_STATIC_NO_FORMAL_DISCOVERY", "F2_FORMAL_DISCOVERY_FULL")
TREATMENT, PARENT = "F2_FORMAL_DISCOVERY_FULL", "TARGET_ONLY_DIRECT"
FREEZE_SEED = 20260904
N_TASKS = 80
ALPHA = 0.05
CEILING = 0.90

LEGS = {  # archived R2 rows (sha256 asserted at load) -> the billy-old original path
    "n80": ("FG80_R2_N80_EVALUATION_ROWS.json", "3ca96c8288d90820ae4c1c3619723a05d5d3c0e61bd21424f4030eb15c29c01e"),
    "n96": ("FMFG_R2_N96_EVALUATION_ROWS.json", "506ce65cbfeabc4142576afe4445dab0794922adfcb17a3cb8be39bf59b1e284"),
    "n120": ("FMFG_R2_N120_EVALUATION_ROWS.json", "533280ea7abf38d7e51f1bffa05fc37ac1e393277aed46880a9fc40c457ff398"),
    "n160": ("FMFG_R2_N160_EVALUATION_ROWS.json", "3eae0434829533c92c1935057f89f23c0526155865b1e585865267a45cd60f81"),
}
R2_FG80_SUMMARY = {"TARGET_ONLY_DIRECT": 42, "F0_PARENT_FEDERATION": 34, "STRONGEST_DOMAIN_FORMAL_PARENT": 33,
                   "F2_STATIC_NO_FORMAL_DISCOVERY": 32, "F2_FORMAL_DISCOVERY_FULL": 23}

TOKEN = re.compile(r"^([A-Z]_[A-Z]{6})\b")
#: anything in the tail after the leading token that makes it a DIFFERENT answer rather than a
#: decoration of the same one: a second feature id, a logical connective (word or symbol), a
#: negation, or a zero-valued assignment.  Detected on the tail, never on the leading token.
TAIL_IS_ANOTHER_ANSWER = re.compile(r"[A-Z]_[A-Z]{6}|\b(?:and|or|not|xor|nand|nor|iff|implies)\b|[∧∨¬⊕→↔&|!]|\b0\b", re.I)


class CannotCheck(Exception):
    pass


class ChannelUnavailable(Exception):
    pass


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    return sha256_bytes(p.read_bytes())


def canon(v: Any) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"))


# =====================================================================================
# census: the descriptive re-read of the frozen R2 rows
# =====================================================================================

def render_normalise(v: Any) -> Any:
    """Collapse a categorical token rendered with decoration ('H_ABCDEF = 1',
    'H_ABCDEF is active (value 1)') to its bare token.  Anything that is not a single
    leading token -- 'H_A AND H_B', 'decision equals H_A' -- is left as it is, so a
    genuinely different answer is never normalised into a correct one."""
    if isinstance(v, str):
        m = TOKEN.match(v.strip())
        if m and not TAIL_IS_ANOTHER_ANSWER.search(v.strip()[m.end():]):
            return m.group(1)
        return v
    if isinstance(v, dict):
        return {k: render_normalise(x) for k, x in v.items()}
    if isinstance(v, list):
        return [render_normalise(x) for x in v]
    return v


def is_rendering_variant(row: dict[str, Any]) -> bool:
    if row.get("correct") or not isinstance(row.get("actual"), dict):
        return False
    return canon(render_normalise(row["actual"])) == canon(render_normalise(row["expected"]))


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact binomial on the discordant pairs."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def load_leg(leg: str) -> list[dict[str, Any]]:
    name, sha = LEGS[leg]
    p = ARCHIVE / name
    got = sha256_file(p)
    if got != sha:
        raise CannotCheck(f"{name}: sha256 {got} != archived custody {sha}")
    return json.loads(p.read_text())


def census(out: Path = CENSUS_OUT) -> dict[str, Any]:
    """Per (study, arm): exact correct, rendering-variant wrongs, semantic correct."""
    table: dict[str, dict[str, Any]] = {}
    fg80_rows: list[dict[str, Any]] = []
    for leg in LEGS:
        rows = load_leg(leg)
        for r in rows:
            study = r["task_id"].split("-")[0]
            key = f"{study}/{r['arm']}"
            e = table.setdefault(key, {"study": study, "arm": r["arm"], "leg": leg, "tasks": 0,
                                       "exact_correct": 0, "rendering_variant_wrong": 0,
                                       "other_wrong": 0, "missing": 0})
            e["tasks"] += 1
            if r.get("missing"):
                e["missing"] += 1
            elif r["correct"]:
                e["exact_correct"] += 1
            elif is_rendering_variant(r):
                e["rendering_variant_wrong"] += 1
            else:
                e["other_wrong"] += 1
            if study == "fg80":
                fg80_rows.append(r)
    for e in table.values():
        e["semantic_correct"] = e["exact_correct"] + e["rendering_variant_wrong"]
        e["exact_accuracy"] = e["exact_correct"] / e["tasks"]
        e["semantic_accuracy"] = e["semantic_correct"] / e["tasks"]

    # --- controls, evaluated before anything is read as a finding ---------------------
    controls = []
    # C1 the exact counts reproduce the registered R2 FG80 summary (ties the archive to the receipt)
    repro = {a: table[f"fg80/{a}"]["exact_correct"] for a in ARMS}
    controls.append({"control": "R2_FG80_EXACT_COUNTS_REPRODUCED", "pass": repro == R2_FG80_SUMMARY,
                     "got": repro, "expected": R2_FG80_SUMMARY})
    # C2 the detector fires on a planted variant in a NON-fg80 wrong row
    planted = None
    for leg in ("n120", "n160", "n96"):
        for r in load_leg(leg):
            if not r["correct"] and isinstance(r.get("actual"), dict) and not r.get("missing"):
                planted = dict(r)
                break
        if planted:
            break
    fired = None
    if planted is not None:
        exp = planted["expected"]
        # decorate every string leaf of the EXPECTED answer and use it as the actual
        def decorate(v):
            if isinstance(v, str) and TOKEN.match(v):
                return v + " = 1"
            if isinstance(v, dict):
                return {k: decorate(x) for k, x in v.items()}
            if isinstance(v, list):
                return [decorate(x) for x in v]
            return v
        mutated = dict(planted, actual=decorate(exp))
        fired = is_rendering_variant(mutated) and (canon(exp) != canon(mutated["actual"]))
    controls.append({"control": "DETECTOR_FIRES_ON_PLANTED_VARIANT", "pass": bool(fired),
                     "planted_task": planted["task_id"] if planted else None})
    # C3 the detector does NOT fire on a genuinely different answer
    fake = {"correct": False, "expected": {"representation_feature": "H_AAAAAA", "target_decision": "YES"},
            "actual": {"representation_feature": "H_BBBBBB AND H_AAAAAA", "target_decision": "YES"}}
    controls.append({"control": "DETECTOR_SILENT_ON_A_DIFFERENT_ANSWER", "pass": not is_rendering_variant(fake)})
    # C4 cross-study: rendering variants must be ZERO outside fg80 (the detector was live there)
    outside = sum(e["rendering_variant_wrong"] for e in table.values() if e["study"] != "fg80")
    outside_wrong = sum(e["other_wrong"] for e in table.values() if e["study"] != "fg80")
    controls.append({"control": "NO_RENDERING_VARIANTS_OUTSIDE_FG80", "pass": outside == 0,
                     "rendering_variants_outside_fg80": outside,
                     "wrong_rows_outside_fg80_the_detector_examined": outside_wrong})

    # --- the FG80 semantic paired contrast (descriptive) -------------------------------
    tasks = sorted({r["task_id"] for r in fg80_rows})
    sem = {(r["arm"], r["task_id"]): (bool(r["correct"]) or is_rendering_variant(r)) for r in fg80_rows}
    exact = {(r["arm"], r["task_id"]): bool(r["correct"]) for r in fg80_rows}

    def paired(a: str, b: str, m: dict) -> dict[str, Any]:
        bb = sum(1 for t in tasks if m[(b, t)] and not m[(a, t)])
        cc = sum(1 for t in tasks if m[(a, t)] and not m[(b, t)])
        return {"treatment": a, "control": b, "control_only_correct_b": bb,
                "treatment_only_correct_c": cc, "delta_tasks": cc - bb, "exact_p": mcnemar_exact(bb, cc)}

    forms: dict[str, list] = {}
    for r in fg80_rows:
        af = str(r["actual"].get("representation_feature", "")) if isinstance(r.get("actual"), dict) else ""
        forms.setdefault(r["arm"], []).append(re.sub(r"H_[A-Z]{6}", "H", af))
    residual = [{"arm": r["arm"], "task_id": r["task_id"], "expected": r["expected"], "actual": r["actual"]}
                for r in fg80_rows if not sem[(r["arm"], r["task_id"])]]

    result = {
        "schema_version": "orion.v2.fg80-r3.rendering-census.v1",
        "class": "DESCRIPTIVE, NON-GATING re-read of frozen R2 rows; alters no registered terminal",
        "archive_custody": {k: {"file": v[0], "sha256": v[1]} for k, v in LEGS.items()},
        "controls": controls,
        "controls_all_pass": all(c["pass"] for c in controls),
        "fg80": {
            "per_arm": {a: table[f"fg80/{a}"] for a in ARMS},
            "paired_treatment_vs_parent_EXACT_registered": paired(TREATMENT, PARENT, exact),
            "paired_treatment_vs_parent_SEMANTIC_descriptive": paired(TREATMENT, PARENT, sem),
            "representation_feature_rendering_forms": {a: dict(Counter(v).most_common(8)) for a, v in forms.items()},
            "residual_semantic_errors": residual,
        },
        "all_studies": sorted(table.values(), key=lambda e: (e["study"], e["arm"])),
        "interpreter": sys.version.split()[0],
    }
    out.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    return result


# =====================================================================================
# freeze: fresh tasks from a committed seed, with a categorical contract
# =====================================================================================

def enumerated_contract(public: dict[str, Any]) -> dict[str, Any]:
    feats = [k for k in public["demonstrations"][0] if k != "decision"]
    return {"representation_feature": {"one_of": sorted(feats)}, "target_decision": {"one_of": ["YES", "NO"]}}


def generate_tasks(seed: int, n: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Byte-identical generator to R2 (imported, not copied); only the contract differs."""
    rng = random.Random(seed)
    tasks, answers = [], {}
    for index in range(n):
        task_rng = random.Random(rng.getrandbits(64))
        public, answer = R2SUITE.gen_fg80(task_rng)
        task_id = f"fg80-{index + 1:04d}"
        public["task_id"] = task_id
        public["answer_contract"] = enumerated_contract(public)
        tasks.append(public)
        answers[task_id] = answer
        assert answer["representation_feature"] in public["answer_contract"]["representation_feature"]["one_of"]
    return tasks, answers


def freeze(workdir: Path, seed: int = FREEZE_SEED, n: int = N_TASKS, force: bool = False) -> dict[str, Any]:
    if workdir.exists() and not force:
        raise CannotCheck(f"workdir exists: {workdir}")
    tasks, answers = generate_tasks(seed, n)
    tasks2, answers2 = generate_tasks(seed, n)
    if canon(tasks) != canon(tasks2) or canon(answers) != canon(answers2):
        raise CannotCheck("generator is not deterministic from the seed")
    workdir.mkdir(parents=True, exist_ok=True)
    (workdir / "public_tasks.json").write_text(json.dumps({"schema_version": "orion.v2.fg80-r3-public.v1", "tasks": tasks}, indent=2, sort_keys=True))
    private = json.dumps({"schema_version": "orion.v2.fg80-r3-private.v1", "answers": answers}, indent=2, sort_keys=True).encode()
    (workdir / "private_oracle.json").write_bytes(private)
    for arm in ARMS:
        for t in tasks:
            p = workdir / "requests" / arm / f"{t['task_id']}.json"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps({"schema_version": "orion.v2.fg80-r3-request.v1", "task_id": t["task_id"],
                                     "arm_id": arm, "task": t, "scientific_truth_authorized": False,
                                     "publication_readiness_authorized": False}, indent=2, sort_keys=True))
    fz = {"schema_version": "orion.v2.fg80-r3-freeze.v1", "seed": seed, "task_count": n, "arms": list(ARMS),
          "registered_dispatches": n * len(ARMS), "private_oracle_sha256": sha256_bytes(private),
          "public_tasks_sha256": sha256_file(workdir / "public_tasks.json"),
          "design_json_sha256": sha256_file(DESIGN_JSON) if DESIGN_JSON.exists() else None,
          "generator": "scripts/run_formal_discovery_generated_suite.py::gen_fg80 (imported, unchanged)",
          "procedure_text": "scripts/orion_formal_discovery_arms.py::PROCEDURE_TEXT (imported, unchanged)",
          "authority": {"grants_scientific_truth": False, "grants_F2_superiority": False}}
    (workdir / "FROZEN_SUITE.json").write_text(json.dumps(fz, indent=2, sort_keys=True))
    return fz


# =====================================================================================
# run: the channel, the prompt, the dispatch
# =====================================================================================

def output_schema(contract: dict[str, Any]) -> dict[str, Any]:
    return {"type": "object", "additionalProperties": False,
            "required": ["representation_feature", "target_decision", "reasoning_summary", "falsifier"],
            "properties": {
                "representation_feature": {"type": "string", "enum": list(contract["representation_feature"]["one_of"])},
                "target_decision": {"type": "string", "enum": list(contract["target_decision"]["one_of"])},
                "reasoning_summary": {"type": "string"}, "falsifier": {"type": "string"}}}


def encoding_instruction(contract: dict[str, Any]) -> str:
    """THE lever.  R2's instruction described the field as a free 'string'; this names the
    admissible values.  Everything else in the prompt is R2's text, imported."""
    feats = contract["representation_feature"]["one_of"]
    return ("Return JSON matching the schema. `representation_feature` MUST be exactly one of the "
            "feature ids " + json.dumps(feats) + " -- the bare id and nothing else (no '= 1', no "
            "'is active', no conjunction). `target_decision` MUST be exactly \"YES\" or \"NO\".")


def prompt(req: dict[str, Any]) -> str:
    task = req["task"]
    return f"""You are a protected gold-blind formal-reasoning experimental arm.
No network retrieval. The private oracle is unavailable. Solve only from the public task.
ARM: {req['arm_id']}
ARM PROCEDURE: {R2ARMS.arm_instruction(str(req['arm_id']))}

PUBLIC TASK:
{json.dumps(task, indent=2, sort_keys=True)}

{encoding_instruction(task['answer_contract'])}
Do not claim scientific truth, a new mathematical theory, ORION superiority, field status, or publication readiness.
"""


def channel_anthropic(text: str, schema: dict[str, Any], pin: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """Anthropic-compatible endpoint, tool-forced structured output, served-model pin."""
    base = os.environ["ANTHROPIC_BASE_URL"].rstrip("/")
    url = base + ("/messages" if base.endswith("/v1") else "/v1/messages")
    body = {"model": os.environ["ANTHROPIC_MODEL"], "max_tokens": int(os.environ.get("ORION_ARM_MAX_TOKENS", "4000")),
            "temperature": 0, "messages": [{"role": "user", "content": text}],
            "tools": [{"name": "emit_answer", "description": "Emit the structured answer.", "input_schema": schema}],
            "tool_choice": {"type": "tool", "name": "emit_answer"}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={
        "x-api-key": os.environ["ANTHROPIC_AUTH_TOKEN"], "anthropic-version": "2023-06-01",
        "content-type": "application/json"})
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=int(os.environ.get("ORION_ARM_HTTP_TIMEOUT", "600"))) as raw:
                data = json.load(raw)
            break
        except urllib.error.HTTPError as exc:
            payload = exc.read()[:400].decode(errors="replace")
            if exc.code == 429 and ("Exhausted" in payload or "limit" in payload.lower()):
                raise ChannelUnavailable(f"HTTP 429: {payload}") from exc
            last = f"HTTP {exc.code}: {payload}"
            time.sleep(5 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError) as exc:
            last = f"{type(exc).__name__}: {exc}"
            time.sleep(5 * (attempt + 1))
    else:
        raise RuntimeError(f"channel failed after retries: {last}")
    served = str(data.get("model", ""))
    if served != pin:
        raise CannotCheck(f"served model {served!r} != pinned {pin!r}")
    tool = [c for c in data.get("content", []) if c.get("type") == "tool_use"]
    if not tool:
        raise RuntimeError("no tool_use block in response")
    return dict(tool[0]["input"]), {"served_model": served, "usage": data.get("usage"), "stop_reason": data.get("stop_reason")}


def channel_codex(text: str, schema: dict[str, Any], pin: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """The R2 executor, verbatim mechanics; the CLI exposes no served id (request echo)."""
    with tempfile.TemporaryDirectory(prefix="fg80r3-") as td:
        sp, op = Path(td) / "schema.json", Path(td) / "out.json"
        sp.write_text(json.dumps(schema))
        cmd = [os.environ.get("ORION_CODEX_BIN", "codex"), "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
               "--skip-git-repo-check", "--sandbox", "read-only", "--model", pin,
               "--output-schema", str(sp), "--output-last-message", str(op), text]
        cp = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
                            stdin=subprocess.DEVNULL, timeout=int(os.environ.get("ORION_FORMAL_TIMEOUT", "1800")))
        if "usage limit" in cp.stdout.lower():
            raise ChannelUnavailable(cp.stdout[-300:])
        if cp.returncode != 0 or not op.exists():
            raise RuntimeError(f"codex failed ({cp.returncode}): {cp.stdout[-800:]}")
        return json.loads(op.read_text()), {"served_model": None,
                                            "served_model_source": "NOT_EXPOSED_BY_CODEX_CLI__HEADER_IS_REQUEST_ECHO",
                                            "requested_model": pin}


def validate_answer(ans: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    if set(ans) - {"representation_feature", "target_decision", "reasoning_summary", "falsifier"}:
        raise ValueError(f"unexpected keys {sorted(ans)}")
    if ans["representation_feature"] not in contract["representation_feature"]["one_of"]:
        raise ValueError(f"representation_feature {ans['representation_feature']!r} not in the enumerated set")
    if ans["target_decision"] not in contract["target_decision"]["one_of"]:
        raise ValueError(f"target_decision {ans['target_decision']!r} not in the enumerated set")
    return {"representation_feature": ans["representation_feature"], "target_decision": ans["target_decision"]}


def run(workdir: Path, channel: str, pin: str, concurrency: int, arms: list[str]) -> int:
    private = workdir / "private_oracle.json"
    fz = json.loads((workdir / "FROZEN_SUITE.json").read_text())
    if not private.exists():
        raise CannotCheck("private oracle missing before dispatch")
    data = private.read_bytes()
    if sha256_bytes(data) != fz["private_oracle_sha256"]:
        raise CannotCheck("private oracle does not match the freeze commitment")
    (workdir / "PRIVATE_ORACLE_COMMITMENT.json").write_text(json.dumps(
        {"sha256": fz["private_oracle_sha256"], "private_removed_before_dispatch": True}, indent=2))
    private.unlink()
    call = channel_anthropic if channel == "anthropic" else channel_codex
    jobs = []
    for arm in arms:
        for rq in sorted((workdir / "requests" / arm).glob("*.json")):
            rp = workdir / "responses" / arm / rq.name
            if not rp.exists():
                jobs.append((arm, rq, rp))
    unavailable: list[str] = []

    def one(job):
        arm, rq, rp = job
        req = json.loads(rq.read_text())
        text = prompt(req)
        start = time.time()
        out = {"schema_version": "orion.v2.fg80-r3-response.v1", "task_id": req["task_id"], "arm_id": arm,
               "prompt_sha256": sha256_bytes(text.encode()), "answer": None, "status": None,
               "resource_receipt": {"model_calls": 1, "channel": channel, "requested_model": pin},
               "scientific_truth_authorized": False, "publication_readiness_authorized": False}
        try:
            raw, meta = call(text, output_schema(req["task"]["answer_contract"]), pin)
            out["answer"] = validate_answer(raw, req["task"]["answer_contract"])
            out["reasoning_summary"] = raw.get("reasoning_summary", "")
            out["falsifier"] = raw.get("falsifier", "")
            out["status"] = "COMPLETED_PROPOSAL_ONLY"
            out["resource_receipt"].update(meta)
        except ChannelUnavailable as exc:
            out["status"] = "EXECUTION_FAILED_CHANNEL_UNAVAILABLE"
            out["failure"] = str(exc)[:300]
            unavailable.append(req["task_id"])
        except CannotCheck as exc:
            out["status"] = "EXECUTION_FAILED_SERVED_MODEL_DRIFT"
            out["failure"] = str(exc)[:300]
        except Exception as exc:  # noqa: BLE001
            out["status"] = "EXECUTION_FAILED_MODEL_RESPONSE"
            out["failure"] = f"{type(exc).__name__}: {str(exc)[:300]}"
        out["resource_receipt"]["wall_time_seconds"] = time.time() - start
        rp.parent.mkdir(parents=True, exist_ok=True)
        if out["status"] != "EXECUTION_FAILED_CHANNEL_UNAVAILABLE":
            rp.write_text(json.dumps(out, indent=2, sort_keys=True))
        return out

    rows = []
    try:
        with ThreadPoolExecutor(max_workers=concurrency) as ex:
            for fut in as_completed([ex.submit(one, j) for j in jobs]):
                rows.append(fut.result())
                if unavailable:
                    break
    finally:
        if private.exists():
            raise CannotCheck("private oracle reappeared during dispatch")
        private.write_bytes(data)
    receipt = {"jobs": len(jobs), "completed": sum(1 for r in rows if r["status"] == "COMPLETED_PROPOSAL_ONLY"),
               "failed": sum(1 for r in rows if r["status"] != "COMPLETED_PROPOSAL_ONLY"),
               "channel": channel, "pin": pin, "oracle_restored_hash_match": sha256_file(private) == fz["private_oracle_sha256"],
               "channel_unavailable": bool(unavailable)}
    (workdir / "DISPATCH_RECEIPT.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))
    print(json.dumps(receipt))
    return 6 if unavailable else 0


# =====================================================================================
# evaluate: R2's scorer, the paired contrast, the registered routing
# =====================================================================================

def route(acc: dict[str, float], b: int, c: int, p: float, all_valid: bool) -> str:
    if not all_valid:
        return "CANNOT_CHECK__INCOMPLETE_OR_INVALID_DISPATCH"
    t, d = acc[TREATMENT], acc[PARENT]
    if t >= CEILING and d >= CEILING and p > ALPHA:
        return "FG80_AT_CEILING_UNDER_A_CATEGORICAL_CONTRACT__NO_DYNAMIC_RANGE_FOR_THE_P_F_TRIGGER"
    if c > b and p <= ALPHA:
        return "F2_FULL_ABOVE_DIRECT_AT_THE_SEMANTIC_LEVEL__CANDIDATE_ONLY__REQUIRES_ITS_OWN_TRIGGER_PROTOCOL"
    if b > c and p <= ALPHA:
        return "F2_FULL_BELOW_DIRECT_AT_THE_SEMANTIC_LEVEL__THE_R2_DEFICIT_IS_NOT_A_RENDERING_ARTIFACT"
    return "NO_SEMANTIC_CONTRAST__R2_DEFICIT_ATTRIBUTED_TO_THE_INTERFACE"


def evaluate(workdir: Path, arms: list[str]) -> int:
    answers = json.loads((workdir / "private_oracle.json").read_text())["answers"]
    fz = json.loads((workdir / "FROZEN_SUITE.json").read_text())
    rows, summary = [], {}
    for arm in arms:
        correct = missing = 0
        for tid, exp in answers.items():
            p = workdir / "responses" / arm / f"{tid}.json"
            if not p.exists():
                missing += 1
                rows.append({"arm": arm, "task_id": tid, "correct": False, "missing": True, "expected": exp, "actual": None})
                continue
            r = json.loads(p.read_text())
            if r.get("answer") is None or str(r.get("status", "")).startswith("EXECUTION_FAILED"):
                missing += 1
                rows.append({"arm": arm, "task_id": tid, "correct": False, "missing": True, "expected": exp,
                             "actual": None, "status": r.get("status")})
                continue
            ok = canon(r["answer"]) == canon(exp)
            correct += int(ok)
            rows.append({"arm": arm, "task_id": tid, "correct": ok, "expected": exp, "actual": r["answer"],
                         "served_model": r["resource_receipt"].get("served_model")})
        summary[arm] = {"correct": correct, "tasks": len(answers), "accuracy": correct / len(answers),
                        "missing_or_invalid": missing, "run_valid": missing == 0}
    all_valid = all(summary[a]["run_valid"] for a in (TREATMENT, PARENT))
    ok = {(r["arm"], r["task_id"]): r["correct"] for r in rows}
    tids = sorted(answers)
    b = sum(1 for t in tids if ok[(PARENT, t)] and not ok[(TREATMENT, t)])
    c = sum(1 for t in tids if ok[(TREATMENT, t)] and not ok[(PARENT, t)])
    p = mcnemar_exact(b, c)
    served = Counter(r.get("served_model") for r in rows if not r.get("missing"))
    terminal = route({a: summary[a]["accuracy"] for a in summary}, b, c, p, all_valid)
    roll = {"schema_version": "orion.v2.fg80-r3.rollup.v1", "freeze": fz, "summary": summary,
            "paired_treatment_vs_parent": {"b_parent_only": b, "c_treatment_only": c, "delta_tasks": c - b, "exact_p": p},
            "served_model_census": dict(served), "terminal": terminal,
            "authority": {"grants_scientific_truth": False, "grants_F2_superiority": False,
                          "fires_the_P_F_trigger": False, "alters_the_R2_registered_terminal": False}}
    (workdir / "EVALUATION_ROWS.json").write_text(json.dumps(rows, indent=1, sort_keys=True))
    (workdir / "FG80_R3_ROLLUP_V1.json").write_text(json.dumps(roll, indent=1, sort_keys=True) + "\n")
    for a in arms:
        print(f"{a:34s} {summary[a]['correct']:3d}/{summary[a]['tasks']} missing {summary[a]['missing_or_invalid']}")
    print(f"paired {TREATMENT} vs {PARENT}: b={b} c={c} p={p:.4g}")
    print("terminal", terminal)
    if not all_valid:
        return 5
    return 0


# =====================================================================================
# selftest
# =====================================================================================

def selftest() -> int:
    fails = []

    def check(name, cond):
        print(f"  {'ok ' if cond else 'FAIL'} {name}")
        if not cond:
            fails.append(name)

    exp = {"representation_feature": "H_ABCDEF", "target_decision": "YES"}
    check("scorer: decorated token is WRONG under exact match",
          canon({"representation_feature": "H_ABCDEF = 1", "target_decision": "YES"}) != canon(exp))
    check("census: decorated token IS a rendering variant",
          is_rendering_variant({"correct": False, "expected": exp, "actual": {"representation_feature": "H_ABCDEF = 1", "target_decision": "YES"}}))
    check("census: conjunction is NOT a rendering variant",
          not is_rendering_variant({"correct": False, "expected": exp, "actual": {"representation_feature": "H_ABCDEF AND H_XYZXYZ", "target_decision": "YES"}}))
    for tail in (" AND H_XYZXYZ AND H_QQQQQQ", " = 1 and H_XYZXYZ = 0", " AND NOT H_XYZXYZ", " \u2227 H_XYZXYZ", " = 0"):
        check(f"census: tail {tail!r} is NOT a rendering variant",
              not is_rendering_variant({"correct": False, "expected": exp, "actual": {"representation_feature": "H_ABCDEF" + tail, "target_decision": "YES"}}))
    for tail in ("=1", " is 1", " equals 1", " is true", " is true (1)", " is active (value 1)", " (the decision is exactly its Boolean value)"):
        check(f"census: tail {tail!r} IS a rendering variant",
              is_rendering_variant({"correct": False, "expected": exp, "actual": {"representation_feature": "H_ABCDEF" + tail, "target_decision": "YES"}}))
    check("census: wrong decision is NOT a rendering variant",
          not is_rendering_variant({"correct": False, "expected": exp, "actual": {"representation_feature": "H_ABCDEF", "target_decision": "NO"}}))
    check("mcnemar: 30 vs 11 reproduces the R2 receipt's 4.32e-03", abs(mcnemar_exact(30, 11) - 4.324e-03) < 2e-5)
    check("mcnemar: 0 vs 0 is 1.0", mcnemar_exact(0, 0) == 1.0)
    t1, a1 = generate_tasks(FREEZE_SEED, 5)
    t2, a2 = generate_tasks(FREEZE_SEED, 5)
    check("freeze: generator deterministic from the seed", canon(t1) == canon(t2) and canon(a1) == canon(a2))
    t3, _ = generate_tasks(FREEZE_SEED + 1, 5)
    check("freeze: a different seed changes the tasks (seed does something)", canon(t1) != canon(t3))
    check("freeze: the oracle answer is inside the enumerated contract",
          all(a1[t["task_id"]]["representation_feature"] in t["answer_contract"]["representation_feature"]["one_of"] for t in t1))
    sch = output_schema(t1[0]["answer_contract"])
    check("schema: enum carries exactly the four feature ids", len(sch["properties"]["representation_feature"]["enum"]) == 4)
    try:
        validate_answer({"representation_feature": "H_NOTAFEAT", "target_decision": "YES", "reasoning_summary": "", "falsifier": ""}, t1[0]["answer_contract"])
        check("validate: rejects a non-member", False)
    except ValueError:
        check("validate: rejects a non-member", True)
    req = {"task_id": "x", "arm_id": TREATMENT, "task": t1[0]}
    pr = prompt(req)
    check("prompt: carries R2's F2_FULL procedure text verbatim", R2ARMS.PROCEDURE_TEXT["F2_FULL"] in pr)
    check("prompt: names the admissible values", all(f in pr for f in t1[0]["answer_contract"]["representation_feature"]["one_of"]))
    acc = {TREATMENT: 0.95, PARENT: 0.96}
    check("route: ceiling", route(acc, 2, 1, 1.0, True).startswith("FG80_AT_CEILING"))
    check("route: below", route({TREATMENT: 0.5, PARENT: 0.8}, 30, 11, 0.004, True).startswith("F2_FULL_BELOW"))
    check("route: above", route({TREATMENT: 0.8, PARENT: 0.5}, 11, 30, 0.004, True).startswith("F2_FULL_ABOVE"))
    check("route: null", route({TREATMENT: 0.7, PARENT: 0.75}, 5, 3, 0.7, True).startswith("NO_SEMANTIC_CONTRAST"))
    check("route: invalid dispatch is CANNOT_CHECK", route(acc, 0, 0, 1.0, False).startswith("CANNOT_CHECK"))
    # the machine-readable design twin carries the same constants as this script
    if DESIGN_JSON.exists():
        dc = json.loads(DESIGN_JSON.read_text())["constants"]
        check("design twin: seed / n_tasks / arms / treatment / parent / alpha / ceiling agree with the script",
              dc["freeze_seed"] == FREEZE_SEED and dc["n_tasks"] == N_TASKS and tuple(dc["arms"]) == ARMS
              and dc["treatment"] == TREATMENT and dc["parent"] == PARENT and dc["alpha"] == ALPHA
              and dc["ceiling"] == CEILING and dc["registered_dispatches"] == N_TASKS * len(ARMS))
    else:
        check("design twin present", False)
    print(f"selftest: {len(fails)} failures")
    return 0 if not fails else 5


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    sub.add_parser("census").add_argument("--out", type=Path, default=CENSUS_OUT)
    f = sub.add_parser("freeze")
    f.add_argument("--workdir", type=Path, default=DEFAULT_WORKDIR)
    f.add_argument("--force", action="store_true")
    r = sub.add_parser("run")
    r.add_argument("--workdir", type=Path, default=DEFAULT_WORKDIR)
    r.add_argument("--channel", choices=["anthropic", "codex"], required=True)
    r.add_argument("--pin", required=True, help="served-model pin (anthropic) / requested model (codex)")
    r.add_argument("--max-concurrency", type=int, default=3)
    r.add_argument("--arms", default=",".join(ARMS))
    e = sub.add_parser("evaluate")
    e.add_argument("--workdir", type=Path, default=DEFAULT_WORKDIR)
    e.add_argument("--arms", default=",".join(ARMS))
    a = ap.parse_args(argv)
    try:
        if a.cmd == "selftest":
            return selftest()
        if a.cmd == "census":
            res = census(a.out)
            for c in res["controls"]:
                print(f"control {c['control']}: {'PASS' if c['pass'] else 'FAIL'}")
            for arm in ARMS:
                e_ = res["fg80"]["per_arm"][arm]
                print(f"{arm:34s} exact {e_['exact_correct']:3d}/80 rendering-variant {e_['rendering_variant_wrong']:3d} semantic {e_['semantic_correct']:3d}/80")
            print("EXACT   ", json.dumps(res["fg80"]["paired_treatment_vs_parent_EXACT_registered"]))
            print("SEMANTIC", json.dumps(res["fg80"]["paired_treatment_vs_parent_SEMANTIC_descriptive"]))
            print(f"interpreter {res['interpreter']}; written {a.out}")
            return 0 if res["controls_all_pass"] else 5
        if a.cmd == "freeze":
            fz = freeze(a.workdir, force=a.force)
            print(json.dumps(fz, indent=1))
            return 0
        if a.cmd == "run":
            return run(a.workdir, a.channel, a.pin, a.max_concurrency, [x for x in a.arms.split(",") if x])
        if a.cmd == "evaluate":
            return evaluate(a.workdir, [x for x in a.arms.split(",") if x])
    except CannotCheck as exc:
        print(f"CANNOT_CHECK: {exc}", file=sys.stderr)
        return 5
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

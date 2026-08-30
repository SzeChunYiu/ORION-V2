#!/usr/bin/env python3
"""Gold-blind executable for EL10 epistemic-locality interface tasks.

Four arms share one solver, one scenario payload and one answer contract; only
the interface wrapper differs:

- GLOBAL_RANKING            frozen context-free global ranking (no conditioning)
- CURRENT_F0                strongest context-conditioned parent federation
- CURRENT_F2                current ORION ProblemFrame binding (no PerspectiveFrame)
- F2_PLUS_LOCALITY_INTERFACE PerspectiveFrame request/receipt over all seven coordinates

Executor: codex-cli (ORION_EL_EXECUTOR=codex, default) or an Anthropic-compatible
Messages-API endpoint (ORION_EL_EXECUTOR=anthropic), mirroring the FM/FG R2 arm
executor. Every response stamps the executor actually used.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

COORDS = [
    "environment_distribution",
    "task_family",
    "system_boundary",
    "scale",
    "timescale",
    "substrate_interface",
    "criterion",
]

GLOBAL_RANKING_TABLE = (
    "Frozen global ranking (aggregate over the full benchmark mixture, all contexts pooled):\n"
    "- On the pooled mixture the FIRST-listed method of the scenario registry leads the\n"
    "  SECOND-listed method by a stable margin (mixture-level aggregate, context-free).\n"
    "This ranking is context-free by construction: it is the reference decision procedure\n"
    "for this arm and is not to be re-derived from local context specifics."
)

F0_PARENT_FEDERATION = (
    "Parent federation (strongest context-conditioned parents; apply them, no weaker substitute):\n"
    "1. Algorithm selection / no-free-lunch: average-case ranking of methods is empty without a\n"
    "   reference distribution; performance is a function of (method, instance distribution), so\n"
    "   selection must condition on the registered distribution (Wolpert & Macready; Rice's\n"
    "   framework of algorithm selection).\n"
    "2. Ecological rationality: rationality is adaptive to environment structure; a method's\n"
    "   success is defined relative to its ecology, and the same heuristic can be optimal in one\n"
    "   ecology and poor in another (Simon's scissors; Todd & Gigerenzer).\n"
    "3. Rational metareasoning: method and computation choices should maximize expected value\n"
    "   given the agent's resources, horizon and frame; selection is conditional on scale and\n"
    "   timescale (Russell & Wefald; Hay et al.).\n"
    "Condition on the registered context as these parents prescribe."
)

F2_PROBLEM_FRAME = (
    "Current ORION interface (ProblemFrame): before deciding, restate the problem class, the\n"
    "registered resources/scale, and the registered criterion; then decide under that frame."
)

LOCALITY_INTERFACE = (
    "PerspectiveFrame request/receipt (locality interface): before deciding, complete the\n"
    "receipt by binding ALL SEVEN registered coordinates to the scenario's registered values:\n"
    + "\n".join(f"- {c}" for c in COORDS)
    + "\nThen check the decision against the counterfactual value of each bound coordinate\n"
    "(would the decision survive if that coordinate changed?); decide only after the receipt,\n"
    "and answer the transport question relative to the completed frame."
)

ARM_PROCEDURES = {
    "GLOBAL_RANKING": (
        "Decision procedure: use the frozen context-free global ranking. The scenario's registered\n"
        "context block is provided for reference only; the ranking, not local context specifics,\n"
        "selects the method. Answer the remaining questions from the ranking's context-free logic.\n\n"
        + GLOBAL_RANKING_TABLE
    ),
    "CURRENT_F0": F0_PARENT_FEDERATION,
    "CURRENT_F2": F2_PROBLEM_FRAME,
    "F2_PLUS_LOCALITY_INTERFACE": LOCALITY_INTERFACE,
}

ANSWER_CONTRACT = {
    "decision": "one of: FIRST | SECOND | PARETO_INCOMPARABLE | COMPARISON_INVALID",
    "holds_across_contexts": "bool - does the finding you rely on hold across ALL values of the registered coordinates",
    "perspective_dependent_coordinates": "array, subset of the seven coordinate names, lowercase",
    "comparison_valid": "bool - is the posed comparison valid under the registered evidence interfaces",
    "transport_verdict": "one of: VALID | INVALID | NOT_ESTABLISHED",
    "brief_rationale": "string, at most 80 words",
}


def schema() -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": list(ANSWER_CONTRACT),
        "properties": {
            "decision": {
                "type": "string",
                "enum": ["FIRST", "SECOND", "PARETO_INCOMPARABLE", "COMPARISON_INVALID"],
            },
            "holds_across_contexts": {"type": "boolean"},
            "perspective_dependent_coordinates": {
                "type": "array",
                "items": {"type": "string"},
            },
            "comparison_valid": {"type": "boolean"},
            "transport_verdict": {
                "type": "string",
                "enum": ["VALID", "INVALID", "NOT_ESTABLISHED"],
            },
            "brief_rationale": {"type": "string"},
        },
    }


def prompt(req: dict) -> str:
    return (
        "EL10 epistemic-locality decision task.\n\n"
        f"ARM: {req['arm_id']}\n"
        f"ARM PROCEDURE:\n{ARM_PROCEDURES[str(req['arm_id'])]}\n\n"
        f"SCENARIO:\n{req['task']['scenario_text']}\n\n"
        "QUESTIONS (answer all, in the JSON contract below):\n"
        "1. Decide: deploy the FIRST-listed method, deploy the SECOND-listed method, declare\n"
        "   PARETO_INCOMPARABLE (no total order under the registered criterion set), or declare\n"
        "   COMPARISON_INVALID (the registered evidence interfaces do not admit the comparison\n"
        "   as posed).\n"
        "2. Does the finding/superiority you rely on hold across ALL values of the registered\n"
        "   coordinates?\n"
        "3. Which registered coordinates does the outcome depend on (subset of the seven)?\n"
        "4. Is the posed comparison valid under the registered evidence interfaces?\n"
        "5. Verdict on transporting the established finding to the counterfactual value stated\n"
        "   in the scenario: VALID, INVALID or NOT_ESTABLISHED.\n\n"
        "ANSWER CONTRACT (exact JSON object, no extra keys):\n"
        + json.dumps(ANSWER_CONTRACT, indent=1)
    )


def _extract_json(text: str) -> dict:
    last = None
    for _ in range(3):
        try:
            lo = text.rindex("{")
            hi = text.rindex("}")
            if lo < hi:
                return json.loads(text[lo : hi + 1])
        except ValueError:
            pass
        except json.JSONDecodeError as exc:
            last = exc
        break
    raise RuntimeError(f"no JSON object in model response ({last})")


def _api_structured(pl: str) -> tuple[dict, int, int]:
    key = os.environ.get("ANTHROPIC_AUTH_TOKEN") or os.environ.get("ANTHROPIC_API_KEY")
    model = os.environ.get("ANTHROPIC_MODEL", "")
    if not key or not model:
        raise RuntimeError("anthropic executor: missing ANTHROPIC_AUTH_TOKEN/ANTHROPIC_API_KEY/ANTHROPIC_MODEL")
    import urllib.request

    body = json.dumps(
        {
            "model": model,
            "max_tokens": int(os.environ.get("ORION_EL_MAX_TOKENS", "4096")),
            "messages": [{"role": "user", "content": pl}],
        }
    ).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "content-type": "application/json",
            "x-api-key": key,
            "authorization": f"Bearer {key}",
            "anthropic-version": "2023-06-01",
        },
    )
    attempts = 0
    while True:
        attempts += 1
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                payload = json.load(resp)
            usage = payload.get("usage", {})
            return (
                _extract_json(payload["content"][0]["text"]),
                attempts,
                int(usage.get("input_tokens", 0)) + int(usage.get("output_tokens", 0)),
            )
        except Exception as exc:  # noqa: BLE001 - retry then surface
            if attempts >= int(os.environ.get("ORION_EL_EMPTY_RETRIES", "4")):
                raise RuntimeError(f"anthropic executor retries exhausted: {exc}") from exc
            time.sleep(5 * attempts)


def execute(req: dict) -> dict:
    start = time.time()
    pl = prompt(req)
    if os.environ.get("ORION_EL_EXECUTOR", "codex") == "anthropic":
        data, calls, tokens = _api_structured(pl)
        exec_name, exec_model = "anthropic-api", os.environ.get("ANTHROPIC_MODEL", "")
    else:
        schema_file = Path(tempfile.mkstemp(suffix=".json")[1])
        out_file = Path(tempfile.mkstemp(suffix=".txt")[1])
        try:
            schema_file.write_text(json.dumps(schema()))
            cmd = [
                os.environ.get("ORION_CODEX_BIN", "codex"),
                "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
                "--skip-git-repo-check", "--sandbox", "read-only",
                "--model", os.environ.get("ORION_CODEX_MODEL", "gpt-5.6-terra"),
                "--output-schema", str(schema_file),
                "--output-last-message", str(out_file),
                pl,
            ]
            comp = subprocess.run(cmd, capture_output=True, text=True, timeout=int(os.environ.get("ORION_EL_TIMEOUT", "900")))
            if comp.returncode != 0:
                raise RuntimeError(f"codex exit {comp.returncode}: {comp.stdout[-400:]} {comp.stderr[-400:]}")
            text = out_file.read_text()
            if not text.strip():
                raise RuntimeError("codex empty last-message")
            data = _extract_json(text)
        finally:
            for p in (schema_file, out_file):
                try:
                    p.unlink()
                except FileNotFoundError:
                    pass
        calls, tokens, exec_name, exec_model = 1, 0, "codex-cli", os.environ.get("ORION_CODEX_MODEL", "gpt-5.6-terra")
    return {
        "schema_version": "orion.v2.el10-response.v1",
        "task_id": req["task_id"],
        "arm_id": req["arm_id"],
        "answer": data,
        "status": "OK",
        "resource_receipt": {
            "model_calls": calls,
            "tokens": tokens,
            "wall_time_seconds": round(time.time() - start, 3),
            "executor": exec_name,
            "model": exec_model,
        },
    }


def main() -> int:
    request = json.loads(Path(sys.argv[sys.argv.index("--request") + 1]).read_text())
    response_path = Path(sys.argv[sys.argv.index("--response") + 1])
    try:
        out = execute(request)
    except Exception as exc:  # noqa: BLE001 - execution failure is receipted, not crashed
        out = {
            "schema_version": "orion.v2.el10-response.v1",
            "task_id": request["task_id"],
            "arm_id": request["arm_id"],
            "answer": None,
            "status": f"EXECUTION_FAILED_MODEL_RESPONSE: {exc}"[:500],
            "resource_receipt": {"model_calls": 0, "tokens": 0, "executor": "none", "model": "none"},
            "falsifier": "repair execution binding and rerun under a new identity",
        }
    response_path.parent.mkdir(parents=True, exist_ok=True)
    response_path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

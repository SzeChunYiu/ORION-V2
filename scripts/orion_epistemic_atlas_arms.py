#!/usr/bin/env python3
"""Gold-blind executable for AH20 epistemic-atlas / horizon interface tasks.

Five arms share one solver, one scenario payload and one answer contract; only
the interface wrapper differs:

- SIMPLE_NATIVE           direct answer, no framing wrapper
- CURRENT_F0              strongest context-conditioned parent federation
- CURRENT_F2              current ORION kernel composition, no atlas request
- PARENT_LOCAL_GLOBAL     identifiability/OED probe selection + sheaf-style
                          gluing-check federation (CANNOT_CHECK where neither
                          parent binds the episode)
- F2_PLUS_ATLAS_HORIZON   explicit atlas/horizon request/receipt interface

Executor: codex-cli (ORION_EL_EXECUTOR=codex, default; gpt-5.6-terra) or an
Anthropic-compatible Messages-API endpoint (ORION_EL_EXECUTOR=anthropic),
whole-suite only (never mixed per-arm within a run). Every response stamps the
executor actually used.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SIMPLE_NATIVE = (
    "Decision procedure: answer the questions directly from the scenario's registered\n"
    "facts. No framing procedure, receipt or interface is imposed."
)

F0_PARENT_FEDERATION = (
    "Parent federation (strongest parents; apply them, no weaker substitute):\n"
    "1. Formal epistemology: a claim's scope is bounded by its weakest premise; a\n"
    "   covering family of local results does not entail a global claim without a\n"
    "   further warrant (Cartwright's dappled world; Lloyd's model adequacy scope).\n"
    "2. Social epistemology: registered witnesses and their scope carry the evidence;\n"
    "   an unregistered global assertion has no testimonial warrant (Goldman).\n"
    "3. Identifiability / optimal experiment design: a probe has value only if it can\n"
    "   separate hypotheses the current probes cannot; value of information is the\n"
    "   expected decision gain, not the data volume (Lindley; Chaloner & Verdinelli).\n"
    "4. Open-world learning: distinguish residual unknowns from representable\n"
    "   uncertainty; an unexplained residual is not a discovery claim (Russell;\n"
    "   open-world categorisation literature).\n"
    "Condition on the registered facts as these parents prescribe."
)

F2_KERNEL = (
    "Current ORION interface (kernel composition): before deciding, bind the problem\n"
    "frame (K0), the registered transport contracts (K2: what transports where, and\n"
    "what does not), diagnosis over registered alternatives (K4), and escalation to\n"
    "the registered authority only on a warrant (K5). No atlas interface is requested."
)

PARENT_LOCAL_GLOBAL = (
    "Local-to-global parent federation (two components; CANNOT_CHECK where neither\n"
    "binds the episode):\n"
    "1. Decision-theoretic OED probe selection (Chaloner & Verdinelli; Lindley):\n"
    "   adopt a proposed probe only if it strictly refines the observational\n"
    "   partition over decision-distinct candidates; redundant probes are rejected\n"
    "   whatever their cost or provenance.\n"
    "2. Sheaf-style gluing check (Mac Lane; local-to-global sections): locally\n"
    "   compatible pieces glue to a global section only when a global section\n"
    "   witness is exhibited; pairwise compatibility alone never promotes to a\n"
    "   global section, and an incompatible overlap obstructs one.\n"
    "Where an episode is outside both parents' scope, answer CANNOT_CHECK for the\n"
    "unbound fields rather than improvising."
)

ATLAS_HORIZON_INTERFACE = (
    "Atlas/horizon request/receipt interface: before deciding, complete the receipt:\n"
    "1. Bind the registered local charts and overlap assessments verbatim (chart ids,\n"
    "   overlap ids, compatibility verdicts, witnesses).\n"
    "2. Gluing disposition, exactly one of: GLOBAL_SECTION_WITNESSED (only with the\n"
    "   registered global-section witness id), MATCHING_FAMILY_ONLY (compatible\n"
    "   overlaps, no global witness registered), GLOBAL_SECTION_OBSTRUCTED (a\n"
    "   registered incompatibility), CANNOT_CHECK (registered correspondence absent).\n"
    "3. Probe proposals: ADOPT only a probe that strictly refines the observational\n"
    "   partition over decision-distinct candidates; REJECT redundant probes\n"
    "   (deterministic functions of existing outcomes); horizon disposition one of\n"
    "   PROBE_REFINES_HORIZON | NO_DISTINGUISHABILITY_GAIN | BROKEN_CANDIDATE_UNIVERSE.\n"
    "4. OUTSIDE_CURRENT_ATLAS only for a residual that persists after every\n"
    "   registered disposition, and only with the residual witness id; it carries no\n"
    "   positive mechanism content.\n"
    "Decide only after the receipt is complete."
)

ARM_PROCEDURES = {
    "SIMPLE_NATIVE": SIMPLE_NATIVE,
    "CURRENT_F0": F0_PARENT_FEDERATION,
    "CURRENT_F2": F2_KERNEL,
    "PARENT_LOCAL_GLOBAL": PARENT_LOCAL_GLOBAL,
    "F2_PLUS_ATLAS_HORIZON": ATLAS_HORIZON_INTERFACE,
}

ANSWER_CONTRACT = {
    "decision": "one of: FIRST | SECOND | PARETO_INCOMPARABLE | COMPARISON_INVALID | NOT_APPLICABLE",
    "gluing_disposition": "one of: GLOBAL_SECTION_WITNESSED | MATCHING_FAMILY_ONLY | GLOBAL_SECTION_OBSTRUCTED | CANNOT_CHECK",
    "global_section_witness_id": "string, required iff gluing_disposition is GLOBAL_SECTION_WITNESSED, else empty",
    "holds_across_contexts": "bool - does the finding you rely on hold across ALL values of the registered coordinates",
    "transport_verdict": "one of: VALID | INVALID | NOT_ESTABLISHED",
    "probe_decision": "one of: ADOPT | REJECT | NONE",
    "probe_id": "string, the adopted/rejected probe id, else empty",
    "horizon_disposition": "one of: PROBE_REFINES_HORIZON | NO_DISTINGUISHABILITY_GAIN | BROKEN_CANDIDATE_UNIVERSE | OUTSIDE_CURRENT_ATLAS | NOT_APPLICABLE",
    "outside_atlas_witness_id": "string, required iff horizon_disposition is OUTSIDE_CURRENT_ATLAS, else empty",
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
                "enum": ["FIRST", "SECOND", "PARETO_INCOMPARABLE", "COMPARISON_INVALID", "NOT_APPLICABLE"],
            },
            "gluing_disposition": {
                "type": "string",
                "enum": ["GLOBAL_SECTION_WITNESSED", "MATCHING_FAMILY_ONLY", "GLOBAL_SECTION_OBSTRUCTED", "CANNOT_CHECK"],
            },
            "global_section_witness_id": {"type": "string"},
            "holds_across_contexts": {"type": "boolean"},
            "transport_verdict": {"type": "string", "enum": ["VALID", "INVALID", "NOT_ESTABLISHED"]},
            "probe_decision": {"type": "string", "enum": ["ADOPT", "REJECT", "NONE"]},
            "probe_id": {"type": "string"},
            "horizon_disposition": {
                "type": "string",
                "enum": [
                    "PROBE_REFINES_HORIZON",
                    "NO_DISTINGUISHABILITY_GAIN",
                    "BROKEN_CANDIDATE_UNIVERSE",
                    "OUTSIDE_CURRENT_ATLAS",
                    "NOT_APPLICABLE",
                ],
            },
            "outside_atlas_witness_id": {"type": "string"},
            "brief_rationale": {"type": "string"},
        },
    }


def prompt(req: dict) -> str:
    return (
        "AH20 epistemic-atlas / horizon decision task.\n\n"
        f"ARM: {req['arm_id']}\n"
        f"ARM PROCEDURE:\n{ARM_PROCEDURES[str(req['arm_id'])]}\n\n"
        f"SCENARIO:\n{req['task']['scenario_text']}\n\n"
        "QUESTIONS (answer all, in the JSON contract below):\n"
        "1. Decide: deploy the FIRST-listed method, deploy the SECOND-listed method,\n"
        "   PARETO_INCOMPARABLE, COMPARISON_INVALID, or NOT_APPLICABLE (no method-selection\n"
        "   decision is registered in this scenario).\n"
        "2. Gluing disposition over the registered charts/overlaps: GLOBAL_SECTION_WITNESSED\n"
        "   (only with the registered global-section witness id), MATCHING_FAMILY_ONLY,\n"
        "   GLOBAL_SECTION_OBSTRUCTED, or CANNOT_CHECK. Include the witness id iff WITNESSED.\n"
        "3. Does the finding/superiority you rely on hold across ALL values of the registered\n"
        "   coordinates?\n"
        "4. Verdict on the scenario's transport proposal: VALID, INVALID or NOT_ESTABLISHED.\n"
        "5. Probe decision on any registered probe proposal: ADOPT (with probe id), REJECT\n"
        "   (with probe id), or NONE.\n"
        "6. Horizon disposition: PROBE_REFINES_HORIZON, NO_DISTINGUISHABILITY_GAIN,\n"
        "   BROKEN_CANDIDATE_UNIVERSE, OUTSIDE_CURRENT_ATLAS (only with the residual witness\n"
        "   id), or NOT_APPLICABLE.\n\n"
        "ANSWER CONTRACT (exact JSON object, no extra keys):\n"
        + json.dumps(ANSWER_CONTRACT, indent=1)
    )


def _extract_json(text: str) -> dict:
    stripped = text.strip()
    if stripped.startswith("{"):
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            pass
    # Walk brace pairs from the outside in: last opening brace paired with each
    # later closing brace, so prose or stray braces inside rationale cannot
    # make a valid object unparseable.
    starts = [i for i, ch in enumerate(text) if ch == "{"]
    ends = [i for i, ch in enumerate(text) if ch == "}"]
    for lo in reversed(starts):
        for hi in ends:
            if hi <= lo:
                continue
            try:
                return json.loads(text[lo : hi + 1])
            except json.JSONDecodeError:
                continue
    raise RuntimeError("no parseable JSON object in model response")


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
            if attempts >= int(os.environ.get("ORION_AH_EMPTY_RETRIES", "6")):
                raise RuntimeError(f"anthropic executor retries exhausted: {exc}") from exc
            time.sleep(5 * attempts)


def execute(req: dict) -> dict:
    start = time.time()
    pl = prompt(req)
    if os.environ.get("ORION_AH_EXECUTOR", "codex") == "anthropic":
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
            comp = subprocess.run(cmd, capture_output=True, text=True, timeout=int(os.environ.get("ORION_AH_TIMEOUT", "900")))
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
        "schema_version": "orion.v2.ah20-response.v1",
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
            "schema_version": "orion.v2.ah20-response.v1",
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

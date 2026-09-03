"""ME-F1 model channel: the Codex CLI control call (frozen with design V1).

**Why this channel and not the z.ai one.**  The z.ai Anthropic-compatible endpoint
silently substitutes models: on 2026-09-02 a request for ``glm-5.2`` was served
``glm-5.3`` with HTTP 200 and no warning (issue #45).  A study whose budget is matched
in model calls cannot tolerate a silent mid-campaign model swap.  The Codex CLI channel
was probed on the execution host on 2026-09-02 and behaves differently: an unavailable
model is **refused** with HTTP 400 and a non-zero exit code
(``--model definitely-not-a-real-model-xyz`` -> ``ERROR {... "not found" ...}``, rc=1)
rather than substituted.

**What is and is not attested.**  The CLI's human-readable header line ``model: <id>``
is an *echo of the requested id*, not a served-model attestation -- the probe above
printed the bogus id back verbatim.  With ``--json`` no model id appears at all.  So
this module does NOT fake an attestation.  It records the triad

    requested_model          the frozen id, identical for every arm
    served_model_observed    None -- honestly null
    served_model_source      "NOT_EXPOSED_BY_CODEX_CLI__HEADER_IS_REQUEST_ECHO"

and relies on the *refusal* property for its fail-closed guarantee: because the channel
refuses rather than substitutes, a call that returns rc=0 with a schema-valid body was
served by a model the endpoint accepted for the frozen id.  Any non-zero exit, missing
output file, timeout or schema violation is a hard arm failure -- never retried into
silence, never scored as an answer (design S7.2).

Failed calls are booked as ``model_calls = 1``.  A failure consumes channel capacity and
must appear in the matched budget; booking it as zero (as the older GC1/GC2 harness did)
would let a flaky arm buy extra attempts for free.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

#: Frozen model identity.  Identical for every model arm (design S4.2 information matching).
#: gpt-5.5 on the execution host billy-old, which carries the programme-pinned
#: codex-cli 0.129.0-alpha.15.  gpt-5.6-sol fails outright on that CLI version
#: (rc=1, models-cache "unknown variant `max`"); the frozen model is what the
#: execution host can actually serve.
DEFAULT_MODEL = "gpt-5.5"
DEFAULT_EFFORT = "medium"
DEFAULT_TIMEOUT = 600


class ChannelCannotCheck(Exception):
    """A call that cannot be scored as an answer: recorded, excluded, counted."""


@dataclass
class CallReceipt:
    ok: bool
    body: dict[str, Any] | None
    model_calls: int
    total_tokens: int | None
    wall_seconds: float
    requested_model: str
    served_model_observed: None = None
    served_model_source: str = "NOT_EXPOSED_BY_CODEX_CLI__HEADER_IS_REQUEST_ECHO"
    failure: str = ""
    prompt_sha256: str = ""
    tool_calls: int = 0

    def as_json(self) -> dict[str, Any]:
        return {
            "ok": self.ok, "model_calls": self.model_calls, "total_tokens": self.total_tokens,
            "wall_seconds": round(self.wall_seconds, 3), "requested_model": self.requested_model,
            "served_model_observed": self.served_model_observed,
            "served_model_source": self.served_model_source,
            "failure": self.failure, "prompt_sha256": self.prompt_sha256,
            "tool_calls": self.tool_calls,
        }


def call_control(prompt: str, schema: dict[str, Any], *, model: str | None = None,
                 effort: str | None = None, timeout: int | None = None,
                 workspace: Path | None = None) -> CallReceipt:
    """One structured control decision.  Exactly one model call, or one recorded failure."""
    import hashlib

    model = model or os.environ.get("MEF1_CODEX_MODEL", DEFAULT_MODEL)
    effort = effort or os.environ.get("MEF1_CODEX_EFFORT", DEFAULT_EFFORT)
    timeout = timeout or int(os.environ.get("MEF1_CODEX_TIMEOUT", str(DEFAULT_TIMEOUT)))
    psha = hashlib.sha256(prompt.encode()).hexdigest()
    start = time.time()

    with tempfile.TemporaryDirectory(prefix="mef1-call-") as temp:
        tp = Path(temp)
        schema_path = tp / "schema.json"
        out_path = tp / "output.json"
        schema_path.write_text(json.dumps(schema))
        ws = workspace or tp
        command = [
            os.environ.get("MEF1_CODEX_BIN", "codex"), "exec", "--ephemeral",
            "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check",
            "--sandbox", "read-only", "-C", str(ws), "--model", model,
            "-c", f'model_reasoning_effort="{effort}"',
            "--output-schema", str(schema_path), "--output-last-message", str(out_path),
            prompt,
        ]
        try:
            completed = subprocess.run(
                command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                # stdin=DEVNULL: with an inherited non-tty stdin the CLI waits for
                # additional prompt input and the call hangs to its timeout.
                stdin=subprocess.DEVNULL, timeout=timeout, check=False,
            )
        except subprocess.TimeoutExpired:
            return CallReceipt(False, None, 1, None, time.time() - start, model,
                               failure=f"TIMEOUT:{timeout}", prompt_sha256=psha)
        except OSError as exc:
            return CallReceipt(False, None, 1, None, time.time() - start, model,
                               failure=f"OSError:{exc}", prompt_sha256=psha)

        stdout = completed.stdout or ""
        tokens = _tokens_from(stdout)
        if completed.returncode != 0 or not out_path.exists():
            tail = stdout[-600:].replace("\n", " ")
            return CallReceipt(False, None, 1, tokens, time.time() - start, model,
                               failure=f"RC{completed.returncode}:{tail}", prompt_sha256=psha)
        try:
            body = json.loads(out_path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            return CallReceipt(False, None, 1, tokens, time.time() - start, model,
                               failure=f"UNPARSEABLE:{exc}", prompt_sha256=psha)

    return CallReceipt(True, body, 1, tokens, time.time() - start, model, prompt_sha256=psha)


def _tokens_from(stdout: str) -> int | None:
    m = re.findall(r"tokens used\s*\n\s*([0-9,]+)", stdout)
    if not m:
        return None
    try:
        return int(m[-1].replace(",", ""))
    except ValueError:
        return None


def probe_channel(model: str | None = None) -> dict[str, Any]:
    """Host attestation probe recorded once per run (design S8.3), not per call."""
    model = model or os.environ.get("MEF1_CODEX_MODEL", DEFAULT_MODEL)
    try:
        ver = subprocess.run([os.environ.get("MEF1_CODEX_BIN", "codex"), "--version"],
                             text=True, capture_output=True, timeout=60, check=False).stdout.strip()
    except (OSError, subprocess.SubprocessError) as exc:
        ver = f"UNAVAILABLE:{exc}"
    return {
        "codex_version": ver,
        "requested_model": model,
        "served_model_observed": None,
        "served_model_source": "NOT_EXPOSED_BY_CODEX_CLI__HEADER_IS_REQUEST_ECHO",
        "refusal_not_substitution_probe": (
            "2026-09-02, execution host: `--model definitely-not-a-real-model-xyz` returned rc=1 "
            "with an HTTP 400 'not found' error rather than a substituted model; the contrast is "
            "the z.ai endpoint, which served glm-5.3 for a glm-5.2 request with HTTP 200 (issue #45)"
        ),
    }

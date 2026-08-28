#!/usr/bin/env python3
"""Run one ORION experimental arm inside a restricted Docker container.

The adapter is invoked by the provider-neutral dispatcher and accepts the same
--request/--response contract. Only the public request, solver workspace,
response directory and explicitly declared read-only support mounts are exposed.
Private evaluator/gold directories are never mounted.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any


class SandboxError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SandboxError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SandboxError(f"expected JSON object in {path}")
    return value


def docker_available() -> bool:
    result = subprocess.run(
        ["docker", "version", "--format", "{{.Server.Version}}"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return result.returncode == 0


def mount_argument(source: Path, target: Path, mode: str) -> list[str]:
    return ["--mount", f"type=bind,src={source},dst={target},{mode}"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    args = parser.parse_args(argv)

    if not docker_available():
        raise SandboxError("Docker is unavailable")
    image = os.environ.get("ORION_AGENT_IMAGE", "").strip()
    command = os.environ.get("ORION_AGENT_COMMAND", "").strip()
    if not image or not command:
        raise SandboxError("ORION_AGENT_IMAGE and ORION_AGENT_COMMAND are required")

    request = read_json(args.request)
    task = request.get("task")
    if not isinstance(task, dict):
        raise SandboxError("request task is missing")
    workspace_value = task.get("solver_workspace")
    if not isinstance(workspace_value, str) or not workspace_value.strip():
        raise SandboxError("task.solver_workspace is required for sandboxing")
    workspace = Path(workspace_value).resolve()
    if not workspace.is_dir():
        raise SandboxError(f"solver workspace does not exist: {workspace}")

    response_parent = args.response.resolve().parent
    response_parent.mkdir(parents=True, exist_ok=True)
    request_path = args.request.resolve()
    network_mode = os.environ.get("ORION_AGENT_NETWORK_MODE", "none").strip().casefold()
    cpus = str(request.get("resource_contract", {}).get("default_cpu_cores", 4))
    memory_gb = str(request.get("resource_contract", {}).get("default_memory_gb", 16))

    docker_command = [
        "docker",
        "run",
        "--rm",
        "--cpus",
        cpus,
        "--memory",
        f"{memory_gb}g",
        "--pids-limit",
        "512",
        "--security-opt",
        "no-new-privileges:true",
        "--cap-drop",
        "ALL",
    ]
    if network_mode == "none":
        docker_command += ["--network", "none"]
    elif network_mode != "enabled":
        raise SandboxError("ORION_AGENT_NETWORK_MODE must be none or enabled")

    docker_command += mount_argument(request_path, Path("/orion/request.json"), "readonly")
    docker_command += mount_argument(workspace, Path("/workspace"), "rw")
    docker_command += mount_argument(response_parent, Path("/orion/out"), "rw")

    public_mounts = task.get("solver_support_mounts", [])
    if public_mounts is None:
        public_mounts = []
    if not isinstance(public_mounts, list):
        raise SandboxError("solver_support_mounts must be a list")
    for value in public_mounts:
        source = Path(str(value)).resolve()
        if not source.exists():
            raise SandboxError(f"support mount does not exist: {source}")
        docker_command += mount_argument(source, source, "readonly")

    forward_names = [
        item.strip()
        for item in os.environ.get("ORION_AGENT_FORWARD_ENV", "").split(",")
        if item.strip()
    ]
    for name in forward_names:
        if name in os.environ:
            docker_command += ["--env", f"{name}={os.environ[name]}"]

    docker_command += [
        "--env",
        f"ORION_NETWORK_MODE={network_mode}",
        "--env",
        "ORION_GOLD_ACCESS=NONE",
        "--workdir",
        "/workspace",
        image,
        "sh",
        "-lc",
        command
        + " --request /orion/request.json"
        + f" --response /orion/out/{shlex.quote(args.response.name)}",
    ]

    result = subprocess.run(
        docker_command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    log_path = response_parent / f"{args.response.stem}.sandbox.log.json"
    log_path.write_text(
        json.dumps(
            {
                "schema_version": "orion.v2.agent-sandbox-log.v1",
                "image": image,
                "network_mode": network_mode,
                "workspace": str(workspace),
                "support_mounts": [str(Path(value).resolve()) for value in public_mounts],
                "forwarded_environment_names": forward_names,
                "returncode": result.returncode,
                "stdout": result.stdout[-5000:],
                "stderr": result.stderr[-5000:],
                "gold_mounts": [],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise SandboxError(f"container agent failed: {result.stderr[-3000:]}")
    if not args.response.exists():
        raise SandboxError("container agent did not create the requested response")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (SandboxError, OSError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

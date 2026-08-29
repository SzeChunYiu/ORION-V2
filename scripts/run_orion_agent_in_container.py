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
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


class SandboxError(RuntimeError):
    pass


_ENV_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


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
    if mode not in {"readonly", "rw"}:
        raise SandboxError(f"unsupported mount mode: {mode}")
    return ["--mount", f"type=bind,src={source},dst={target},{mode}"]


def _require_existing(path: Path, *, label: str) -> Path:
    resolved = path.resolve()
    if not resolved.exists():
        raise SandboxError(f"{label} does not exist: {resolved}")
    return resolved


def _positive_resource(value: str, *, label: str) -> str:
    text = str(value).strip()
    try:
        numeric = float(text)
    except ValueError as exc:
        raise SandboxError(f"{label} must be numeric") from exc
    if numeric <= 0:
        raise SandboxError(f"{label} must be positive")
    return text


def build_command(
    *,
    image: str,
    agent_command: str,
    staged_input: Path,
    workspace: Path,
    response_parent: Path,
    response_name: str,
    support_mounts: Iterable[Path],
    forwarded_environment_names: Iterable[str],
    network_mode: str,
    cpu_cores: str,
    memory_gb: str,
    read_only_root: bool,
) -> list[str]:
    """Build a fail-closed Docker command exposing only declared public surfaces.

    ``staged_input`` may be a single request file or a directory containing a
    public request bundle. It is always mounted read-only at ``/orion/in``.
    The helper never mounts evaluator-private state, Git metadata, gold patches,
    or any path not explicitly supplied by the caller.
    """

    image = image.strip()
    agent_command = agent_command.strip()
    if not image or not agent_command:
        raise SandboxError("image and agent_command are required")

    network = network_mode.strip().casefold()
    if network not in {"none", "enabled"}:
        raise SandboxError("network_mode must be none or enabled")

    cpus = _positive_resource(cpu_cores, label="cpu_cores")
    memory = _positive_resource(memory_gb, label="memory_gb")
    staged = _require_existing(staged_input, label="staged input")
    work = _require_existing(workspace, label="workspace")
    out = response_parent.resolve()
    out.mkdir(parents=True, exist_ok=True)
    if not out.is_dir():
        raise SandboxError(f"response parent is not a directory: {out}")

    response_leaf = Path(response_name)
    if response_leaf.name != response_name or response_name in {"", ".", ".."}:
        raise SandboxError("response_name must be one file name")

    command = [
        "docker",
        "run",
        "--rm",
        "--cpus",
        cpus,
        "--memory",
        f"{memory}g",
        "--pids-limit",
        "512",
        "--security-opt",
        "no-new-privileges:true",
        "--cap-drop",
        "ALL",
    ]
    if read_only_root:
        command.append("--read-only")
    if network == "none":
        command += ["--network", "none"]

    command += mount_argument(staged, Path("/orion/in"), "readonly")
    command += mount_argument(work, Path("/workspace"), "rw")
    command += mount_argument(out, Path("/orion/out"), "rw")

    normalized_support: list[Path] = []
    for value in support_mounts:
        source = _require_existing(Path(value), label="support mount")
        if source in {staged, work, out}:
            raise SandboxError("support mount duplicates a primary sandbox surface")
        normalized_support.append(source)
        command += mount_argument(source, source, "readonly")

    forward_names: list[str] = []
    for raw_name in forwarded_environment_names:
        name = str(raw_name).strip()
        if not name:
            continue
        if not _ENV_NAME_RE.fullmatch(name):
            raise SandboxError(f"invalid environment variable name: {name!r}")
        if name in {"ORION_GOLD_ACCESS", "ORION_OUTCOME_ACCESS"}:
            raise SandboxError(f"reserved authority environment variable cannot be forwarded: {name}")
        if name in os.environ:
            forward_names.append(name)
            command += ["--env", f"{name}={os.environ[name]}"]

    command += [
        "--env",
        f"ORION_NETWORK_MODE={network}",
        "--env",
        "ORION_GOLD_ACCESS=NONE",
        "--env",
        "ORION_OUTCOME_ACCESS=NONE",
        "--workdir",
        "/workspace",
        image,
        "sh",
        "-lc",
        agent_command
        + " --request /orion/in"
        + f" --response /orion/out/{shlex.quote(response_name)}",
    ]
    return command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    args = parser.parse_args(argv)

    if not docker_available():
        raise SandboxError("Docker is unavailable")
    image = os.environ.get("ORION_AGENT_IMAGE", "").strip()
    agent_command = os.environ.get("ORION_AGENT_COMMAND", "").strip()
    if not image or not agent_command:
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

    public_mounts = task.get("solver_support_mounts", [])
    if public_mounts is None:
        public_mounts = []
    if not isinstance(public_mounts, list):
        raise SandboxError("solver_support_mounts must be a list")
    support_paths = tuple(Path(str(value)) for value in public_mounts)

    forward_names = tuple(
        item.strip()
        for item in os.environ.get("ORION_AGENT_FORWARD_ENV", "").split(",")
        if item.strip()
    )

    docker_command = build_command(
        image=image,
        agent_command=agent_command,
        staged_input=request_path,
        workspace=workspace,
        response_parent=response_parent,
        response_name=args.response.name,
        support_mounts=support_paths,
        forwarded_environment_names=forward_names,
        network_mode=network_mode,
        cpu_cores=cpus,
        memory_gb=memory_gb,
        read_only_root=True,
    )

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
                "forwarded_environment_names": list(forward_names),
                "returncode": result.returncode,
                "stdout": result.stdout[-5000:],
                "stderr": result.stderr[-5000:],
                "gold_mounts": [],
                "outcome_mounts": [],
                "authority_environment": {
                    "ORION_GOLD_ACCESS": "NONE",
                    "ORION_OUTCOME_ACCESS": "NONE",
                },
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

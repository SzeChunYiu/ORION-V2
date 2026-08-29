from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "run_orion_agent_in_container.py"
SPEC = importlib.util.spec_from_file_location("orion_container_adapter", SCRIPT)
assert SPEC and SPEC.loader
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)


def test_container_command_mounts_only_declared_public_surfaces(tmp_path: Path) -> None:
    staged = tmp_path / "staged"
    workspace = tmp_path / "workspace"
    responses = tmp_path / "responses"
    support = tmp_path / "support"
    for path in (staged, workspace, responses, support):
        path.mkdir()
    command = adapter.build_command(
        image="agent:test",
        agent_command="python /app/agent.py",
        staged_input=staged,
        workspace=workspace,
        response_parent=responses,
        response_name="task.json",
        support_mounts=(support,),
        forwarded_environment_names=(),
        network_mode="none",
        cpu_cores="2",
        memory_gb="4",
        read_only_root=True,
    )
    joined = " ".join(command)
    assert "--network none" in joined
    assert "--read-only" in command
    assert f"src={staged},dst=/orion/in,readonly" in joined
    assert f"src={workspace},dst=/workspace,rw" in joined
    assert f"src={responses},dst=/orion/out,rw" in joined
    assert f"src={support},dst={support},readonly" in joined
    assert "private_gold" not in joined
    assert "private_evaluation_registry" not in joined
    assert "ORION_GOLD_ACCESS=NONE" in joined
    assert "ORION_OUTCOME_ACCESS=NONE" in joined


def test_invalid_network_mode_is_rejected(tmp_path: Path) -> None:
    for name in ("staged", "workspace", "responses"):
        (tmp_path / name).mkdir()
    try:
        adapter.build_command(
            image="agent:test",
            agent_command="agent",
            staged_input=tmp_path / "staged",
            workspace=tmp_path / "workspace",
            response_parent=tmp_path / "responses",
            response_name="task.json",
            support_mounts=(),
            forwarded_environment_names=(),
            network_mode="surprise",
            cpu_cores="1",
            memory_gb="1",
            read_only_root=True,
        )
    except adapter.SandboxError:
        pass
    else:
        raise AssertionError("invalid network mode was accepted")

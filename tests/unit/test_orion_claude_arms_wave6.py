from __future__ import annotations

from scripts.orion_claude_arms import run_arm


def _request(arm: str) -> dict[str, object]:
    return {"task_id": "bugsinpy-demo-1", "arm_id": arm, "task": {"project": "demo", "bug_id": 1, "solver_workspace": "/tmp/solver"}, "resource_contract": {}}


def test_simple_direct_returns_patch_schema() -> None:
    calls: list[str] = []
    def call(prompt: str) -> tuple[str, dict[str, int]]:
        calls.append(prompt)
        return ('{"patch":"diff --git a/a.py b/a.py\\n--- a/a.py\\n+++ b/a.py\\n@@ -1 +1 @@\\n-x=1\\n+x=2", "diagnosis":"constant", "falsifier":"test"}', {"input_tokens": 4, "output_tokens": 8})
    response = run_arm(_request("SIMPLE_DIRECT"), call=call, workspace_context="context")
    assert len(calls) == 1
    assert response["status"] == "COMPLETED_PROPOSAL_ONLY"
    assert response["proposed_patch_or_artifact"]["type"] == "unified_diff"


def test_full_f2_has_each_required_stage() -> None:
    calls: list[str] = []
    def call(prompt: str) -> tuple[str, dict[str, int]]:
        calls.append(prompt)
        if len(calls) < 3:
            return ("analysis", {"input_tokens": 2, "output_tokens": 3})
        return ('{"patch":"diff --git a/a.py b/a.py\\n--- a/a.py\\n+++ b/a.py\\n@@ -1 +1 @@\\n-x=1\\n+x=2", "diagnosis":"fixed", "falsifier":"test"}', {"input_tokens": 2, "output_tokens": 3})
    response = run_arm(_request("F2_ORION_METABOLIC_FULL"), call=call, workspace_context="context")
    assert len(calls) == 3
    assert set(response["metabolic_stages"]) == {"INGEST", "DECOMPOSE", "SORT", "NATIVE_RECONSTRUCT", "REDUCE", "ABSORB", "RECOMBINE", "CHALLENGE", "ASSIMILATE_OR_RECYCLE"}

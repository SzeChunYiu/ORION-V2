from __future__ import annotations

import json

import pytest

from orion_v2.unified_diff_interface import audit_and_canonicalize_unified_diff
from scripts.orion_claude_arms import _context, _provider_call, arm_call_count, run_arm


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
    assert response["schema_version"] == "orion.v2.agent-response.v1"
    assert response["patch_emission_receipt"]["schema_version"] == "orion.v2.patch-emission.v1"


def test_emitted_patch_needs_no_downstream_canonicalization() -> None:
    """Arms emit canonical diffs, so the frozen syntax-only pass is a no-op."""
    def call(prompt: str) -> tuple[str, dict[str, int]]:
        return (
            '{"patch":"diff --git a/a.py b/a.py\\n--- a.py\\n+++ a.py\\n'
            '@@ -1,9 +1,9 @@\\n ctx\\n-x=1\\n+x=2", "diagnosis":"constant", "falsifier":"test"}',
            {"input_tokens": 4, "output_tokens": 8},
        )

    response = run_arm(_request("SIMPLE_DIRECT"), call=call, workspace_context="context")
    emitted = response["proposed_patch_or_artifact"]["content"]
    audit = audit_and_canonicalize_unified_diff(emitted)
    assert audit.valid_or_canonicalizable and audit.changed is False
    assert "--- a/a.py" in emitted and "@@ -1,2 +1,2 @@" in emitted
    receipt = response["patch_emission_receipt"]
    assert receipt["extracted_was_header_exact"] is False
    assert receipt["diff_git_header_synthesized"] is False
    assert receipt["authority"]["may_change_semantic_edit"] is False


def test_model_output_without_a_diff_fails_closed() -> None:
    def call(prompt: str) -> tuple[str, dict[str, int]]:
        return ('{"patch":"I found no safe repair.", "diagnosis":"none", "falsifier":"test"}',
                {"input_tokens": 1, "output_tokens": 1})

    response = run_arm(_request("SIMPLE_DIRECT"), call=call, workspace_context="context")
    assert response["status"] == "EXECUTION_FAILED_MODEL_RESPONSE"
    assert response["proposed_patch_or_artifact"] is None


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


@pytest.mark.parametrize(
    ("arm", "removed", "prompt_fragment"),
    [
        ("F2_MINUS_DECOMPOSITION", ["DECOMPOSE", "SORT"], "decomposition and source-bound sorting are removed"),
        ("F2_MINUS_NATIVE_RECOVERY", ["NATIVE_RECONSTRUCT"], "without native-parent reconstruction"),
        ("F2_MINUS_COUNTERPROBE", ["CHALLENGE", "COUNTERPROBE"], "without a challenge/counterprobe cycle"),
        ("F2_MINUS_SELECTIVE_REOPEN", ["SELECTIVE_REOPEN"], "do not selectively reopen"),
    ],
)
def test_f2_ablation_changes_prompt_and_records_removal(arm, removed, prompt_fragment) -> None:
    calls: list[str] = []

    def call(prompt: str) -> tuple[str, dict[str, int]]:
        calls.append(prompt)
        if len(calls) < 3:
            return ("analysis", {"input_tokens": 2, "output_tokens": 3})
        return ('{"patch":"diff --git a/a.py b/a.py\\n--- a/a.py\\n+++ b/a.py\\n@@ -1 +1 @@\\n-x=1\\n+x=2", "diagnosis":"fixed", "falsifier":"test"}', {"input_tokens": 2, "output_tokens": 3})

    response = run_arm(_request(arm), call=call, workspace_context="context")

    assert response["component_removal"] == removed
    assert prompt_fragment in "\n".join(calls)


def test_arm_call_count_supports_equal_total_token_budget() -> None:
    assert arm_call_count("SIMPLE_DIRECT") == 1
    assert arm_call_count("SAME_MODEL_REFLECTION") == 2
    assert arm_call_count("F0_PARENT_FEDERATION") == 3
    assert arm_call_count("F2_ORION_METABOLIC_FULL") == 3


def test_provider_call_rejects_unknown_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ORION_MODEL_PROVIDER", "not-a-provider")
    with pytest.raises(ValueError, match="unsupported ORION_MODEL_PROVIDER"):
        _provider_call("hello")


def test_gemini_provider_maps_text_and_usage(monkeypatch: pytest.MonkeyPatch) -> None:
    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def read(self) -> bytes:
            return json.dumps({
                "candidates": [{"content": {"parts": [{"text": "READY"}]}}],
                "usageMetadata": {"promptTokenCount": 7, "candidatesTokenCount": 2},
            }).encode()

    seen: dict[str, object] = {}

    def fake_urlopen(request, timeout):
        seen["url"] = request.full_url
        seen["key_header"] = request.get_header("X-goog-api-key")
        seen["body"] = json.loads(request.data)
        seen["timeout"] = timeout
        return Response()

    monkeypatch.setenv("ORION_MODEL_PROVIDER", "gemini")
    monkeypatch.setenv("ORION_GEMINI_MODEL", "models/gemini-test-version")
    monkeypatch.setenv("GEMINI_API_KEY", "secret-test-key")
    monkeypatch.setenv("ORION_ARM_MAX_TOKENS", "123")
    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    text, usage = _provider_call("hello")

    assert text == "READY"
    assert usage == {"input_tokens": 7, "output_tokens": 2}
    assert str(seen["url"]).startswith(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-test-version:generateContent"
    )
    assert "secret-test-key" not in str(seen["url"])
    assert seen["key_header"] == "secret-test-key"
    assert seen["body"]["generationConfig"]["maxOutputTokens"] == 123
    assert seen["body"]["generationConfig"]["thinkingConfig"] == {"thinkingBudget": 41}
    assert "responseMimeType" not in seen["body"]["generationConfig"]


def test_gemini_final_prompt_requests_json(monkeypatch: pytest.MonkeyPatch) -> None:
    class Response:
        def __enter__(self): return self
        def __exit__(self, *_args): return None
        def read(self): return b'{"candidates":[],"usageMetadata":{}}'

    seen = {}
    def fake_urlopen(request, timeout):
        seen["body"] = json.loads(request.data)
        return Response()

    monkeypatch.setenv("ORION_MODEL_PROVIDER", "gemini")
    monkeypatch.setenv("ORION_GEMINI_MODEL", "gemini-test-version")
    monkeypatch.setenv("GEMINI_API_KEY", "secret-test-key")
    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    _provider_call("Return only one JSON object with keys patch, diagnosis")

    assert seen["body"]["generationConfig"]["responseMimeType"] == "application/json"


def test_context_includes_gold_blind_source_and_prioritizes_failure_file(tmp_path, monkeypatch) -> None:
    (tmp_path / "pkg").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "pkg" / "target.py").write_text("TARGET = 'visible'\n")
    (tmp_path / "pkg" / "other.py").write_text("OTHER = 'visible'\n")
    (tmp_path / "tests" / "test_target.py").write_text("def test_target(): assert False\n")
    monkeypatch.setenv("ORION_CONTEXT_MAX_CHARS", "55")
    request = {
        "task": {
            "solver_workspace": str(tmp_path),
            "baseline_observation": {"stderr_tail": "failure in pkg/target.py"},
            "workspace_contains_gold": False,
        }
    }

    value = json.loads(_context(request))

    assert value["gold_access"] == "NONE"
    assert value["source_snapshots"][0]["path"] == "pkg/target.py"
    assert "TARGET = 'visible'" in value["source_snapshots"][0]["content"]

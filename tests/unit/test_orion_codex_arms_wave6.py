from __future__ import annotations

from scripts.orion_codex_arms import _arm_instructions, _normalize_patch, _schema


def test_codex_schema_requires_all_stage_receipts() -> None:
    stage = _schema()["properties"]["stage_receipts"]
    assert len(stage["required"]) == 9
    assert stage["additionalProperties"] is False


def test_patch_normalizer_adds_diff_git_header() -> None:
    patch = "--- a/pkg/x.py\n+++ b/pkg/x.py\n@@ -1 +1 @@\n-x=1\n+x=2\n"
    assert _normalize_patch(patch).startswith("diff --git a/pkg/x.py b/pkg/x.py\n")


def test_patch_normalizer_accepts_bare_paths_and_multiple_files() -> None:
    patch = "--- pkg/x.py\n+++ pkg/x.py\n@@ -1 +1 @@\n-x=1\n+x=2\n--- y.py\n+++ y.py\n@@ -1 +1 @@\n-y=1\n+y=2\n"
    normalized = _normalize_patch(patch)
    assert "diff --git a/pkg/x.py b/pkg/x.py" in normalized
    assert "diff --git a/y.py b/y.py" in normalized


def test_ablation_prompts_are_distinct() -> None:
    assert "Do not decompose" in _arm_instructions("F2_MINUS_DECOMPOSITION")
    assert "Do not perform challenge" in _arm_instructions("F2_MINUS_COUNTERPROBE")

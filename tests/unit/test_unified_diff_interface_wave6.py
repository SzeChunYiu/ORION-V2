from __future__ import annotations

from orion_v2.unified_diff_interface import audit_and_canonicalize_unified_diff


def test_normalizes_file_header_prefixes_without_changing_edit() -> None:
    patch = (
        "diff --git a/pandas/core/dtypes/common.py b/pandas/core/dtypes/common.py\n"
        "--- pandas/core/dtypes/common.py\n"
        "+++ pandas/core/dtypes/common.py\n"
        "@@ -10,2 +10,2 @@\n"
        " context\n"
        "-old\n"
        "+new\n"
    )
    audited = audit_and_canonicalize_unified_diff(patch)
    assert audited.valid_or_canonicalizable
    assert audited.changed
    assert "--- a/pandas/core/dtypes/common.py" in audited.canonical_diff
    assert "+++ b/pandas/core/dtypes/common.py" in audited.canonical_diff
    assert "-old\n+new" in audited.canonical_diff


def test_recomputes_hunk_counts_from_unchanged_body() -> None:
    patch = (
        "diff --git a/pandas/core/series.py b/pandas/core/series.py\n"
        "--- a/pandas/core/series.py\n"
        "+++ b/pandas/core/series.py\n"
        "@@ -4683,7 +4683,8 @@\n"
        " context1\n"
        " context2\n"
        " context3\n"
        "\n"
        "-old\n"
        "+new1\n"
        "+new2\n"
        " context4\n"
        " context5\n"
        " context6\n"
    )
    audited = audit_and_canonicalize_unified_diff(patch)
    assert audited.valid_or_canonicalizable
    assert audited.changed
    assert "@@ -4683,8 +4683,9 @@" in audited.canonical_diff
    assert "normalized hunk counts" in "\n".join(audited.reasons)


def test_valid_diff_is_not_semantically_rewritten() -> None:
    patch = (
        "diff --git a/x.py b/x.py\n"
        "--- a/x.py\n"
        "+++ b/x.py\n"
        "@@ -1,1 +1,1 @@\n"
        "-before\n"
        "+after\n"
    )
    audited = audit_and_canonicalize_unified_diff(patch)
    assert audited.valid_or_canonicalizable
    assert not audited.changed
    assert audited.canonical_diff == patch


def test_rejects_path_traversal() -> None:
    patch = (
        "diff --git a/../secret b/../secret\n"
        "--- a/../secret\n"
        "+++ b/../secret\n"
        "@@ -1,1 +1,1 @@\n"
        "-a\n"
        "+b\n"
    )
    audited = audit_and_canonicalize_unified_diff(patch)
    assert not audited.valid_or_canonicalizable
    assert audited.canonical_diff is None


def test_rejects_file_header_that_requires_path_guessing() -> None:
    patch = (
        "diff --git a/x.py b/x.py\n"
        "--- other.py\n"
        "+++ other.py\n"
        "@@ -1,1 +1,1 @@\n"
        "-a\n"
        "+b\n"
    )
    audited = audit_and_canonicalize_unified_diff(patch)
    assert not audited.valid_or_canonicalizable
    assert audited.canonical_diff is None

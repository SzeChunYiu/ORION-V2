from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[2] / "research" / "machine-epistemics-theory"


def load():
    return json.loads((HERE / "ME_FOUNDATION_V1.json").read_text())


def test_registry_has_exactly_35_unique_atomic_gaps():
    d = load()
    ids = [r["id"] for r in d["rows"]]
    assert ids == [f"MEG-{i:02d}" for i in range(1, 36)]
    assert len(set(ids)) == 35
    assert d["counts"]["total"] == 35


def test_pending_pr_is_not_silently_proved():
    d = load()
    pending = {r["id"] for r in d["rows"] if r["status"] == "PENDING_PR"}
    assert pending == set(d["pending_dependencies"]["PR_317"]["owned_meg"])
    assert all(not r["status"].startswith("PROVED") for r in d["rows"] if r["id"] in pending)


def test_batch2_rows_have_honest_scope_or_contraction():
    d = load()
    by = {r["id"]: r for r in d["rows"]}
    assert by["MEG-02"]["status"] == "PROVED_WITH_CONTRACTION"
    assert by["MEG-03"]["status"] == "PROVED_SCOPE_LIMITED"
    assert by["MEG-16"]["status"] == "PROVED_WITH_CORRECTION"
    assert by["MEG-17"]["status"] == "PROVED_SCOPE_LIMITED"
    assert by["MEG-20"]["status"] == "PROVED_SCOPE_LIMITED"


def test_no_scientific_authority_upgrade():
    a = load()["authority"]
    assert a["GENERAL_NOVELTY"] == "NOT_ESTABLISHED"
    assert a["FIELD_STATUS"] == "NOT_ESTABLISHED"
    assert a["OCM_SUPERIORITY"] == "NOT_ESTABLISHED"


def test_foundation_terminal_is_explicitly_partial():
    d = load()
    assert d["foundation_terminal"] == "FOUNDATION_V1_PARTIAL__OPEN_RESEARCH_REMAINS"
    assert d["counts"] == {
        "total": 35,
        "proved_or_contracted_on_this_branch": 5,
        "pending_pr_317": 11,
        "other_open_or_parent_adoption": 19,
    }

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


def test_merged_pr317_rows_are_proved_and_bound():
    d = load()
    merged = d["merged_dependencies"]["PR_317"]
    assert merged["status"] == "MERGED"
    assert merged["merge_sha"] == "d756c086edc46ad4e5e682f69730b72c1dc26a4c"
    by = {r["id"]: r for r in d["rows"]}
    assert all(by[x]["status"] == "PROVED" for x in merged["owned_meg"])
    assert all("d756c086" in by[x]["evidence"] for x in merged["owned_meg"])


def test_batch2_rows_have_honest_scope_or_contraction():
    d = load()
    by = {r["id"]: r for r in d["rows"]}
    assert by["MEG-02"]["status"] == "PROVED_WITH_CONTRACTION"
    assert by["MEG-03"]["status"] == "PROVED_SCOPE_LIMITED"
    assert by["MEG-16"]["status"] == "PROVED_WITH_CORRECTION"
    assert by["MEG-17"]["status"] == "PROVED_SCOPE_LIMITED"
    assert by["MEG-20"]["status"] == "PROVED_SCOPE_LIMITED"


def test_batch3_closes_ten_more_scoped_core_rows():
    d = load(); by = {r["id"]: r for r in d["rows"]}
    for x in ("MEG-05","MEG-10","MEG-11","MEG-12","MEG-13","MEG-15","MEG-21","MEG-28","MEG-33"):
        assert by[x]["status"] == "PROVED_SCOPE_LIMITED"
    assert by["MEG-19"]["status"] == "PROVED_WITH_CORRECTION"


def test_no_scientific_authority_upgrade():
    a = load()["authority"]
    assert a["GENERAL_NOVELTY"] == "NOT_ESTABLISHED"
    assert a["FIELD_STATUS"] == "NOT_ESTABLISHED"
    assert a["OCM_SUPERIORITY"] == "NOT_ESTABLISHED"


def test_foundation_terminal_core_closed_frontier_open():
    d = load()
    assert d["foundation_terminal"] == "FOUNDATION_V1_CORE_SUBSTANTIALLY_CLOSED__FRONTIER_OPEN"
    assert d["counts"] == {"total": 35, "proved_or_contracted": 26, "open_or_parent_adoption": 9}

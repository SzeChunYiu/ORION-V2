"""MACHINE_EPISTEMICS_FIELD_MAP_V1 — the field-map checker's model is consistent, its planted mutants are caught,
its no-alarm control passes, the derived registry and the document's generated regions are exactly what it
derives from the batch documents (batches 1–11).  Stdlib only; under a few seconds."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2] / "research" / "machine-epistemics-theory"
PATH = ROOT / "kso_field_map_v1_exact.py"


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("kso_field_map_v1_exact", PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.fixture(scope="module")
def model(mod):
    return mod.build_model(ROOT, None)


@pytest.fixture(scope="module")
def out(mod):
    return mod.run_all(ROOT, None, check_doc=True)


def test_no_alarm_control(mod, model):
    assert mod.check_consistency(model) == []


def test_status_is_consistent(out):
    assert out["errors"] == [] and out["document_errors"] == []
    assert out["status"] == "CONSISTENT" and out["no_alarm_control"] is True


def test_every_theorem_has_one_checker_and_a_vocabulary_status(mod, model):
    for t in model["theorems"]:
        assert len(t["checker"]) == 1, t["id"]
        assert t["status"] in mod.STATUS_VOCAB, (t["id"], t["status_text"])
        assert t["checker"][0].startswith("check_" + t["id"].lower() + "_")


def test_theorem_ids_unique_and_pinned(model):
    ids = [t["id"] for t in model["theorems"]]
    assert len(ids) == len(set(ids))
    s = model and {k: v for k, v in __import__("collections").Counter(t["batch"] for t in model["theorems"]).items()}
    assert s == {1: 11, 2: 8, 3: 8, 4: 8, 5: 11, 6: 8, 7: 9, 8: 4, 9: 4, 10: 3, 11: 3}
    assert len(ids) == 77


def test_kst_citations_resolve_or_are_flagged(mod, model):
    cited = {k for t in model["theorems"] for k in t["cites"]["kst"]}
    for k in cited:
        assert k in model["registry_rows"] or k in mod.FLAGGED_KST, k
    assert set(mod.FLAGGED_KST) & cited == {"KS-T14"}


def test_impossibilities_have_bounds_and_owners(model):
    assert len(model["impossibilities"]) == 22
    for imp in model["impossibilities"]:
        assert imp["has_bound"] and imp["theorem"] is not None, imp


def test_open_list_and_conjectures(model):
    conj = model["conjectures"]
    assert {(c["theorem"], c["row"]) for c in conj} == {("E8", "KS-T12"), ("E8", "KS-T14"), ("I4", "FDX-15")}
    assert all(c["falsifier"] for c in conj)
    current = [o for o in model["open_items"] if o["kind"] == "OPEN"]
    assert current and all(o["batch"] >= 8 and o["flag"] == "NO_EXECUTABLE_FALSIFIER" for o in current)
    assert all(o["flag"].startswith("CLOSED_LATER by ") for o in model["open_items"] if o["kind"] == "OPEN_HALF_CLOSED_LATER")


def test_derived_registry_numbering(mod, model):
    d = model["derived"]
    assert model["max_existing_kst"] == 121
    assert [r["id"] for r in d if r["existing_row"]] == ["KS-T118", "KS-T119", "KS-T120", "KS-T121"]
    new = [r["id"] for r in d if not r["existing_row"]]
    assert new == [f"KS-T{n}" for n in range(122, 122 + len(new))] and len(new) == 20
    assert all(r["status"] == "OPEN" for r in d if not r["existing_row"])
    committed = json.loads((ROOT / mod.DERIVED_NAME).read_text(encoding="utf-8"))
    assert committed["obligations"] == json.loads(json.dumps(d))


def test_document_regions_match(mod, model):
    assert mod.check_document(model, ROOT) == []


def test_planted_mutants_are_caught(mod, model, out):
    assert mod.mutant_duplicate_id(model)
    assert mod.mutant_unknown_status(model)
    assert mod.mutant_dangling_kst(model)
    assert mod.mutant_impossibility_without_bound(model)
    assert mod.mutant_conjecture_without_falsifier(model)
    assert mod.mutant_derived_renumbered(model)
    assert mod.mutant_stale_document(model, ROOT)
    assert all(out["mutants_caught"].values())


def test_batch12_slot_filled_from_main(model):
    slot = model["batch12_slot"]
    assert slot["present"] and slot["correspondence"] and slot["status_block"]
    assert slot["lean_sorry"] == 0 and slot["lean_names_missing"] == [] and slot["kst_unresolved"] == []
    assert slot["lean_theorems_declared"] > 0 and all(r["status"] for r in slot["correspondence"])


def test_summary_block_is_embedded_verbatim(mod, model):
    doc = (ROOT / mod.DOC_NAME).read_text(encoding="utf-8")
    assert mod.summary_block(model) in doc

"""Unit tests for the PRA Design V3 runner.

The point of V3 is that a registered clause cannot be silently narrowed and a structurally
determined clause cannot be reported as a measurement.  These tests therefore spend most of
their effort on the KNOWN-BAD cases: a checker that only ever sees healthy input is the
"validate the checker first" trap, and the V1/V2 unit tests are the cautionary example --
their test double planted a CONSTANT direction under R3 while its docstring claimed the probe
decoded there, so no test could have failed and the defect reached a protected run.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "research" / "llm-machine-epistemics" / "pra_real_llm_audit_v3.py"
DESIGN = ROOT / "research" / "llm-machine-epistemics" / "PRA_REAL_LLM_AUDIT_DESIGN_V3.json"


def _load():
    spec = importlib.util.spec_from_file_location("pra_v3", RUNNER)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["pra_v3"] = mod
    spec.loader.exec_module(mod)
    return mod


pra = _load()
design = json.loads(DESIGN.read_text())


@pytest.fixture(scope="module")
def dev_suite():
    return pra.generate_suite(design, "dev")


# --------------------------------------------------------------------- suite & label


def test_suite_generation_is_deterministic():
    a, b = pra.generate_suite(design, "dev"), pra.generate_suite(design, "dev")
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def test_probe_label_is_balanced_by_construction(dev_suite):
    units = pra._probe_capture_units(design, dev_suite)
    assert units, "probe families produced no capture units"
    ones = sum(u["label"] for u in units)
    assert ones * 2 == len(units), "the V3 label must be exactly 50/50, not balanced on average"


def test_every_instance_contributes_one_unit_of_each_class(dev_suite):
    by: dict[str, list[int]] = {}
    for u in pra._probe_capture_units(design, dev_suite):
        by.setdefault(u["instance_id"], []).append(u["label"])
    assert by
    for iid, labels in by.items():
        assert sorted(labels) == [0, 1], f"{iid} does not contribute one unit of each class"


def test_roster_order_is_randomised_and_frozen_into_the_suite(dev_suite):
    orders = {tuple(i["roster_order"]) for i in dev_suite["instances"]}
    assert len(orders) > 1, "a constant roster order revives the positional shortcut"
    # frozen: rendering must be a pure function of the suite
    inst = dev_suite["instances"][0]
    assert pra.render_state(inst, inst["arms"][0], "R0") == pra.render_state(inst, inst["arms"][0], "R0")


# ------------------------------------------------------- identifiability certificate


def test_certificate_matches_the_registered_identifiable_set(dev_suite):
    cert = pra.certify_label_identifiability(design, dev_suite)
    assert cert["observed_identifiable"] == cert["registered_identifiable"]
    assert cert["matches_registration"] and cert["passes"]


def test_certificate_rejects_the_conditions_that_do_not_name_the_basis(dev_suite):
    cert = pra.certify_label_identifiability(design, dev_suite)["conditions"]
    for c in ("R1", "R2"):
        assert not cert[c]["identifiable"]
        assert cert[c]["status"] == "LABEL_NOT_IDENTIFIABLE_FROM_CONDITION"
        assert cert[c]["text_collisions"] > 0, "R1/R2 render identically across arms; that is the reason"


def test_kv_condition_is_certified_on_the_effective_context_not_the_text(dev_suite):
    """Its rendered text is R2 (non-identifiable); its retained prefix is R0 (identifiable).

    Certifying the text alone would suppress the one condition the alternate-channel gate
    actually turns on.
    """
    cert = pra.certify_label_identifiability(design, dev_suite)["conditions"]
    assert cert["R2_TEXT_REMOVED_KV_RETAINED"]["identifiable"]
    assert not cert["R2"]["identifiable"]


def test_certificate_refuses_a_render_it_cannot_reproduce(dev_suite, monkeypatch):
    """The control that must match: certify the string the model is shown, or fail loudly."""
    monkeypatch.setattr(pra, "render_state", lambda i, a, c: "not what the model sees")
    with pytest.raises(SystemExit, match="certificate re-render diverges"):
        pra.certify_label_identifiability(design, dev_suite)


# ------------------------------------------------ KNOWN-BAD: the V1 defect must be caught


def _v1_shaped_suite():
    """A suite with V1's structure: fixed roster order, label = which generator slot.

    This is the shape that produced probe accuracy 1.000 under R0 and 0.542/0.594 under R3
    against a registered 0.80 threshold.
    """
    suite = pra.generate_suite(design, "dev")
    for inst in suite["instances"]:
        inst["roster_order"] = ["A", "B", "Z"]          # V1: never shuffled
        for arm in inst["arms"]:
            arm["history_lines"] = pra._history_lines_ordered(
                {"claim_id": inst["claim_id"], "claim_text": inst["claim_text"], "domain": inst["domain"]},
                inst["sources"], ["A", "B", "Z"], arm["state_vars"]["support_set"], [],
            ) if inst["family"] in ("F3_P2_CANON", "F3_P2_CANON_SF") else arm["history_lines"]
    return suite


def test_v1_label_is_flagged_not_identifiable_under_R3(monkeypatch):
    """The heart of it.  V1 registered 'probe decodes support_source under R0 AND R3 >= 0.80'.

    Under V1's label that clause was unsatisfiable in principle: R3 names the basis but lists
    no roster, so the A/B index leaves no trace, and the certificate must say so from the
    suite alone -- before any model call, and without needing the 0.542 that V1 measured.
    """
    def v1_label(inst, arm):
        ss = arm["state_vars"]["support_set"]
        if len(ss) != 1 or arm["state_vars"].get("record_identifies_support") is False:
            return None
        return 1 if ss[0] == "A" else 0

    monkeypatch.setattr(pra, "_probe_label", v1_label)
    cert = pra.certify_label_identifiability(design, _v1_shaped_suite())["conditions"]
    assert cert["R0"]["identifiable"], "V1's R0 WAS identifiable; a checker that fails it is broken"
    assert not cert["R3"]["identifiable"], "the V1 R3 clause must be flagged, not measured"
    assert cert["R3"]["symmetry_mismatches"] > 0, (
        "R3's two arms exchange under the A<->B symmetry while the V1 label flips, "
        "so no classifier beats chance"
    )


def test_unsatisfiable_min_clause_is_a_design_defect_not_a_failure(monkeypatch):
    """A '>= threshold' clause on a non-identifiable condition can never pass.

    Reported as UNREACHABLE__DESIGN_DEFECT, never as an ordinary FAIL -- the distinction is
    the whole point: a permanently-failing gate looks like an empirical negative.
    """
    ident = {"conditions": {"R3": {"identifiable": False}, "R0": {"identifiable": True}}}
    cov = pra.certify_clause_coverage(design, {"GP2": {"clause_values": {
        "GP2a.probe_decodes_R0": {"pass": True}, "GP2a.probe_decodes_R3": {"pass": False}}}}, ident)
    row = next(r for r in cov["clauses"] if r["clause_id"] == "GP2a.probe_decodes_R3")
    assert row["status"] == "UNREACHABLE__DESIGN_DEFECT"
    assert "UNSATISFIABLE" in row["reachability_note"]
    assert not cov["passes"]


def test_unfailable_max_clause_is_a_design_defect(monkeypatch):
    """The mirror image: V1's 'at chance under R2_TRUE_REMOVAL <= 0.65' could never fail."""
    d = copy.deepcopy(design)
    d["gates"]["GP2"]["clauses"].append({
        "id": "GP2a.at_chance_under_R2", "text": "at chance under R2", "required": True,
        "source": "GP2.clause_values.GP2a.at_chance_under_R2.pass",
        "probe_condition": "R2", "direction": "max", "threshold": 0.65})
    ident = {"conditions": {"R2": {"identifiable": False}}}
    cov = pra.certify_clause_coverage(d, {"GP2": {"clause_values": {
        "GP2a.at_chance_under_R2": {"pass": True}}}}, ident)
    row = next(r for r in cov["clauses"] if r["clause_id"] == "GP2a.at_chance_under_R2")
    assert row["status"] == "UNREACHABLE__DESIGN_DEFECT"
    assert "UNFAILABLE" in row["reachability_note"]


def test_a_clause_with_no_implementing_predicate_blocks_the_gate():
    """Shape 5, stated directly: the runner may not pass on the half of a clause it ran."""
    analysis = {"GP0": {"pass": True}, "GP1": {"pass": True},
                "GP3": {"checks": {"p0_no_gap": True, "mirror_not_falsely_revised_under_R3": True,
                                   "recon_no_gap": True}},
                "GP2": {"clause_values": {"GP2a.probe_decodes_R0": {"pass": True}}}}  # R3 absent
    ident = {"conditions": {c: {"identifiable": True} for c in
                            ("R0", "R3", "R2_TEXT_REMOVED_KV_RETAINED")}}
    cov = pra.certify_clause_coverage(design, analysis, ident)
    row = next(r for r in cov["clauses"] if r["clause_id"] == "GP2a.probe_decodes_R3")
    assert row["status"].startswith("NOT_EVALUATED")
    assert not cov["passes"]
    analysis["clause_coverage"] = cov
    assert pra.model_terminal(analysis) == "REGISTERED_CLAUSE_NOT_EVALUATED__SUITE_NOT_INTERPRETABLE"


def test_clause_source_paths_all_resolve_on_a_real_analysis(tmp_path):
    """No registered clause may point at a path the runner never writes."""
    ids = {c["id"] for g in design["gates"].values() for c in g.get("clauses", [])}
    assert ids, "the design registers no clauses"
    srcs = {c["id"]: c["source"] for g in design["gates"].values() for c in g.get("clauses", [])}
    assert len(set(srcs.values())) == len(srcs), "two clauses share a source path"


# ------------------------------------------------------------------- surface null


def test_surface_null_must_include_a_relational_reader():
    """Calibration on the known-bad case.

    V1's R0 label was recoverable by 'is the basis the FIRST name on file?'.  A lexical
    bag-of-ngrams reader sits at chance there, because the nonce names never repeat across
    the instance split -- so a validity check built only from lexical features would have
    cleared V1's positional shortcut.  The relational reader must fire.
    """
    import random as _r

    rng = _r.Random(20260903)
    rows, labels = [], []
    for i in range(80):
        # Both roles draw from the SAME nonce pool the real generator uses, so no lexical
        # feature separates them.  Inventing distinguishable names here would hand the
        # lexical reader the answer and make this test assert nothing.
        s1, s2 = pra._nonce_source(rng), pra._nonce_source(rng)
        a = f"{s1['name']} [{s1['id']}]"
        b = f"{s2['name']} [{s2['id']}]"
        first_is_basis = i % 2 == 0
        basis = a if first_is_basis else b
        rows.append(f"Sources on file: {a}, {b}.\nSupport entry: claim CL-0001 is accepted "
                    f"on the basis of {basis} alone.")
        labels.append(1 if first_is_basis else 0)
    tr, te = list(range(48)), list(range(48, 80))
    lex = pra._mass_mean_on_features([pra._lexical_features(t) for t in rows], labels, tr, te)
    rel = pra._mass_mean_on_features([pra._relational_features(t) for t in rows], labels, tr, te)
    assert rel is not None and rel >= 0.95, "the relational reader must detect a positional shortcut"
    assert lex is not None and lex < 0.75, (
        "the lexical reader is blind to it -- which is exactly why the null cannot be lexical only")


def test_surface_null_is_reported_for_every_probed_condition(dev_suite):
    nulls = pra.surface_null_accuracies(design, dev_suite)["conditions"]
    assert set(nulls) == set(design["probe"]["conditions"])


# ------------------------------------------------------------- probe & end-to-end


def test_stub_plants_a_signal_the_R3_clause_can_actually_test(dev_suite):
    """The test V1 could not write.

    V1's stub planted a constant under R3, so 'the probe decodes under R3' was untestable
    while its docstring asserted it.  Here the planted direction is a function of the
    rendered basis, so this assertion can fail.
    """
    b = pra.StubBackend("planted")
    inst = next(i for i in dev_suite["instances"] if i["family"] == "F3_P2_CANON")
    vecs = {}
    for arm in inst["arms"]:
        m = pra.build_messages(pra.render_state(inst, arm, "R3"), "current_action", None, inst["claim_id"])
        vecs[arm["arm_id"]] = b.hidden_states(m)[-1]
    a, c = vecs["hA"], vecs["hB"]
    assert a[0] != c[0], "the stub plants no label-dependent direction under R3"


def test_removed_condition_is_gone():
    """R2_TRUE_REMOVAL rendered identically to R2; keeping it reported one measurement twice."""
    assert "R2_TRUE_REMOVAL" not in design["probe"]["conditions"]
    assert "R2_TRUE_REMOVAL" not in pra.KV_CONDITIONS
    assert "R2_TRUE_REMOVAL" not in design["kv_channel"]["conditions"]


def test_removal_limb_is_not_re_registered_as_an_empirical_clause():
    clause_ids = {c["id"] for c in design["gates"]["GP2"]["clauses"]}
    assert not any("removal" in c or "at_chance" in c for c in clause_ids), (
        "the removal limb is discharged by certificate; as a measured clause it cannot fail")
    assert "removal_limb_note" in design["gates"]["GP2"]


def test_protected_split_refuses_without_authorization(tmp_path):
    with pytest.raises(SystemExit, match="protected-authorization"):
        pra.main(["--stage", "probe", "--workdir", str(tmp_path), "--design", str(DESIGN),
                  "--backend", "stub", "--split", "protected"])


def test_no_protected_seed_commitment_is_published_yet():
    """A commitment digest with no sealed file behind it is the unexecuted sentence itself."""
    seed = design["suite_generator"]["seed"]
    assert seed["protected_commitment_sha256"].startswith("PENDING_")
    assert design["protected_run"]["authorized"] is False


def test_end_to_end_stub_run_exits_zero_and_evaluates_every_clause(tmp_path):
    args = ["--workdir", str(tmp_path), "--design", str(DESIGN), "--backend", "stub",
            "--stub-variant", "planted", "--split", "dev"]
    assert pra.main(["--stage", "generate-suite"] + args) == 0
    assert pra.main(["--stage", "certify"] + args) == 0
    for stage in ("present-gate", "revision", "probe", "kv-channel"):
        assert pra.main(["--stage", stage] + args) == 0
    assert pra.main(["--stage", "rollup"] + args) == 0
    roll = json.loads((tmp_path / "PRA_REAL_LLM_AUDIT_ROLLUP_V3__dev.json").read_text())
    assert roll["clause_coverage_passes"]
    assert roll["unevaluated_or_unreachable_clauses"] == []
    gp2 = roll["models"]["stub-planted"]["GP2"]
    # non-identifiable conditions carry the distinct code, never a number
    assert gp2["probe_max_test_acc"]["R1"] is None
    assert gp2["probe_max_test_acc"]["R2"] is None
    assert gp2["suppressed_conditions"]["R2"] == "LABEL_NOT_IDENTIFIABLE_FROM_CONDITION"
    assert gp2["probe_max_test_acc"]["R3"] is not None
    assert gp2["contrast_D_same_path_witness"]["path"] == "mcnemar(_pairs(...))"


def test_exit_code_4_when_a_registered_clause_cannot_be_evaluated(tmp_path, monkeypatch):
    """"Could not check" must not share an exit code with "checked and fine"."""
    args = ["--workdir", str(tmp_path), "--design", str(DESIGN), "--backend", "stub",
            "--stub-variant", "planted", "--split", "dev"]
    pra.main(["--stage", "generate-suite"] + args)
    for stage in ("present-gate", "revision", "probe", "kv-channel"):
        pra.main(["--stage", stage] + args)
    real = pra.certify_clause_coverage
    monkeypatch.setattr(pra, "certify_clause_coverage", lambda d, a, i: {
        **real(d, a, i), "passes": False, "unevaluated_or_unreachable": ["GP2a.probe_decodes_R3"]})
    assert pra.main(["--stage", "rollup"] + args) == 4

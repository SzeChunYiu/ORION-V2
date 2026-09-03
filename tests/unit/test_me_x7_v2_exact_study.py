"""ME-X7 V2 exact external-witness study: end-to-end tests of every runner stage,
plus the two registered corrections that separate V2 from V1 and the
protected-scale regression that a partial repair would have introduced.
Development and public-validation fixtures only; nothing here is protected
evidence, and no arm verdict, ladder rung or G1/G4/G5/G7 number is read off the
burned V1 seed."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MEX7V2 = ROOT / "research" / "experiments" / "me-x7-v2"
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

MODULE_NAMES = (
    "mex7_model", "mex7_parents", "mex7_oracle", "mex7_generator", "mex7_arms", "mex7_run",
)


def _load_v2() -> dict:
    """Load the V2 modules under their own names without leaving them in
    `sys.modules`, so the V1 test file's modules — same file names, different
    directory — are neither shadowed by nor shadowing these."""
    saved = {k: sys.modules.pop(k) for k in list(sys.modules) if k in MODULE_NAMES}
    sys.path.insert(0, str(MEX7V2))
    try:
        for name in MODULE_NAMES:  # dependency order; each import sees the last
            spec = importlib.util.spec_from_file_location(name, MEX7V2 / f"{name}.py")
            mod = importlib.util.module_from_spec(spec)
            sys.modules[name] = mod
            spec.loader.exec_module(mod)
        loaded = {k: sys.modules[k] for k in MODULE_NAMES}
    finally:
        sys.path.remove(str(MEX7V2))
        for k in MODULE_NAMES:
            sys.modules.pop(k, None)
        sys.modules.update(saved)
    return loaded


_V2 = _load_v2()
mex7_model = _V2["mex7_model"]
mex7_parents = _V2["mex7_parents"]
mex7_oracle = _V2["mex7_oracle"]
mex7_generator = _V2["mex7_generator"]
mex7_arms = _V2["mex7_arms"]
mex7_run = _V2["mex7_run"]

DESIGN_JSON = MEX7V2 / "ME_X7_V2_EXTERNAL_WITNESS_SUFFICIENCY_EXACT_STUDY_DESIGN_V2.json"

# Revealed in research/experiments/me-x7/ME_X7_OUTCOME_RECEIPT.md §1 and therefore
# burned: it is a public validation seed here and may never be a protected seed.
BURNED_V1_SEED = "ME-X7-PROTECTED-b35d0617f13ec73ed96368bfb7019f603e5818bfa69d6de1"
PROTECTED_PER_CELL = 50


def _censor_variant(inst) -> str | None:
    return dict(inst.facts).get("censor_variant")


def _unrecoverable(ep):
    """The registered CENSOR_ENV condition applied to an episode's artifact."""
    from dataclasses import replace

    return replace(ep, artifact=replace(ep.artifact, actual_env="", actual_seed=""))


# ---- V2 correction 1: C_ARTIFACT_DIGEST has a censored state ------------------

def test_unrecoverable_environment_censors_the_digest_check_in_computational_mode() -> None:
    """The V1 defect, stated as a test: an unrecoverable environment is
    undecidable, not a proof/code mismatch — in the oracle and in BOTH arm
    tables, which share this implementation."""
    base = mex7_generator.build_base(__import__("random").Random(7), mex7_model.MODE_COMPUTATIONAL)
    ep = _unrecoverable(base)
    vis = mex7_arms.visible_nodes(ep, full_registry=True)
    assert mex7_oracle.CHECK_FN["C_ARTIFACT_DIGEST"](ep, vis) == mex7_model.CENSORED
    assert mex7_arms.MODULE_CHECK_M["C_ARTIFACT_DIGEST"](ep, vis) == mex7_model.CENSORED
    assert mex7_arms.MODULE_CHECK_B5["C_ARTIFACT_DIGEST"](ep, vis) == mex7_model.CENSORED
    # the sibling that already had the guard is unchanged
    assert mex7_oracle.CHECK_FN["C_ENV_IDENTITY"](ep, vis) == mex7_model.CENSORED


def test_formal_mode_is_untouched_because_it_never_consults_the_environment() -> None:
    base = mex7_generator.build_base(__import__("random").Random(7), mex7_model.MODE_FORMAL)
    ep = _unrecoverable(base)
    vis = mex7_arms.visible_nodes(ep, full_registry=True)
    assert mex7_oracle.CHECK_FN["C_ARTIFACT_DIGEST"](ep, vis) == mex7_model.VALID
    assert mex7_arms.MODULE_CHECK_M["C_ARTIFACT_DIGEST"](ep, vis) == mex7_model.VALID
    assert mex7_arms.MODULE_CHECK_B5["C_ARTIFACT_DIGEST"](ep, vis) == mex7_model.VALID
    assert mex7_oracle.CHECK_FN["C_ENV_IDENTITY"](ep, vis) == mex7_model.CENSORED


def test_an_unrecoverable_environment_does_not_launder_a_digest_mismatch() -> None:
    """Registered ordering: the digest comparison needs no environment and
    decides first, so censoring cannot convert a visible mismatch into an
    abstention."""
    from dataclasses import replace

    base = mex7_generator.build_base(__import__("random").Random(9), mex7_model.MODE_COMPUTATIONAL)
    ep = _unrecoverable(base)
    ep = replace(ep, artifact=replace(ep.artifact, declared_digest="0" * 16))
    vis = mex7_arms.visible_nodes(ep, full_registry=True)
    assert mex7_oracle.CHECK_FN["C_ARTIFACT_DIGEST"](ep, vis) == mex7_model.INVALID
    assert mex7_arms.MODULE_CHECK_M["C_ARTIFACT_DIGEST"](ep, vis) == mex7_model.INVALID
    assert mex7_arms.MODULE_CHECK_B5["C_ARTIFACT_DIGEST"](ep, vis) == mex7_model.INVALID


def test_the_proof_certificate_parent_abstains_rather_than_accepting_what_it_cannot_rerun() -> None:
    """Declared consequence of correction 1. Accepting here would be the
    rejected repair — reporting VALID on the strength of an unverifiable
    flag — inside a parent arm."""
    import random

    base = mex7_generator.build_base(random.Random(7), mex7_model.MODE_COMPUTATIONAL)
    ep = _unrecoverable(base)
    spec = {s.name: s for s in mex7_arms.arm_specs()}["A0_PROOF_CERTIFICATE_ONLY"]
    out = mex7_arms.run_arm(spec, ep, random.Random(0))
    assert out.verdict == mex7_model.CANNOT_CHECK
    assert out.verdict != mex7_model.ACCEPT
    # the parent that already abstained on this condition still does
    replay = {s.name: s for s in mex7_arms.arm_specs()}["A2_REPLAY_ONLY"]
    assert mex7_arms.run_arm(replay, ep, random.Random(0)).verdict == mex7_model.CANNOT_CHECK


# ---- V2 correction 2: the declared per-variant, per-mode censored set ---------

def test_the_declared_censored_table_is_total_over_the_drawable_pairs() -> None:
    drawable = {
        (v, m) for m in mex7_model.MODES for v in mex7_generator.censor_variants_for(m)
    }
    assert drawable == set(mex7_oracle.EXPECTED_CENSORED_CHECKS)
    assert ("CENSOR_CALIBRATION", mex7_model.MODE_FORMAL) not in drawable
    assert len(drawable) == 19


def test_an_unregistered_variant_mode_pair_raises_rather_than_defaulting() -> None:
    with pytest.raises(ValueError):
        mex7_oracle.expected_censored_checks("CENSOR_CALIBRATION", mex7_model.MODE_FORMAL)
    with pytest.raises(ValueError):
        mex7_oracle.expected_censored_checks("CENSOR_NOT_A_VARIANT", mex7_model.MODE_COMPUTATIONAL)


def test_only_the_environment_variant_in_computational_mode_censors_two_checks() -> None:
    """The table documents itself: nine variants censor exactly the one check
    their name says, and the tenth censors two only where the erased field is
    load-bearing for both."""
    two = {
        k for k, v in mex7_oracle.EXPECTED_CENSORED_CHECKS.items() if len(v) != 1
    }
    assert two == {("CENSOR_ENV", mex7_model.MODE_COMPUTATIONAL)}
    assert mex7_oracle.EXPECTED_CENSORED_CHECKS[("CENSOR_ENV", mex7_model.MODE_COMPUTATIONAL)] == (
        frozenset({"C_ENV_IDENTITY", "C_ARTIFACT_DIGEST"})
    )


@pytest.mark.parametrize(
    "variant,mode",
    sorted(mex7_oracle.EXPECTED_CENSORED_CHECKS),
)
def test_every_drawable_variant_produces_exactly_its_declared_censored_set(variant, mode) -> None:
    """Observed == declared, for every registered pair. This both proves the
    invariant and is the only place the table's content is checked against the
    generator rather than against itself."""
    import random

    rng = random.Random(4242)
    base = mex7_generator.build_base(random.Random(4242), mode)
    ep = mex7_generator.plant_censored(base, rng, variant)
    exp = mex7_oracle.oracle(ep)
    assert frozenset(exp.censored_checks) == mex7_oracle.expected_censored_checks(variant, mode)
    ok, why = mex7_oracle.planter_agrees(ep, "CENSORED_UNDECIDABLE", censor_variant=variant)
    assert ok, why


def test_the_declared_set_assertion_is_trippable() -> None:
    """A planted positive for correction 2: if a wrong declaration could not be
    caught, "the declared set matched" would be unfalsifiable. The environment
    variant in computational mode is declared with two checks; asserted against
    a one-check declaration it must be rejected, which is exactly what would
    have deleted the six instances had correction 2 not been applied."""
    import random

    rng = random.Random(4242)
    base = mex7_generator.build_base(random.Random(4242), mex7_model.MODE_COMPUTATIONAL)
    ep = mex7_generator.plant_censored(base, rng, "CENSOR_ENV")
    key = ("CENSOR_ENV", mex7_model.MODE_COMPUTATIONAL)
    original = mex7_oracle.EXPECTED_CENSORED_CHECKS[key]
    try:
        mex7_oracle.EXPECTED_CENSORED_CHECKS[key] = frozenset({"C_ENV_IDENTITY"})
        ok, why = mex7_oracle.planter_agrees(ep, "CENSORED_UNDECIDABLE", censor_variant="CENSOR_ENV")
        assert not ok
        assert "C_ARTIFACT_DIGEST" in why
    finally:
        mex7_oracle.EXPECTED_CENSORED_CHECKS[key] = original
    ok, _ = mex7_oracle.planter_agrees(ep, "CENSORED_UNDECIDABLE", censor_variant="CENSOR_ENV")
    assert ok, "the restored declaration must accept again"


def test_the_censored_stratum_refuses_to_be_validated_without_the_drawn_variant() -> None:
    import random

    rng = random.Random(4242)
    ep = mex7_generator.plant_censored(
        mex7_generator.build_base(random.Random(4242), mex7_model.MODE_COMPUTATIONAL),
        rng,
        "CENSOR_ENV",
    )
    with pytest.raises(ValueError):
        mex7_oracle.planter_agrees(ep, "CENSORED_UNDECIDABLE")


# ---- the protected-scale regression a partial repair would have introduced ----

def test_censor_env_still_draws_in_computational_mode_at_protected_scale() -> None:
    """Correction 1 without correction 2 leaves the count invariant in force,
    the generator re-draws every computational CENSOR_ENV episode, and the six
    instances that exposed the V1 defect leave the split — a hard gate going
    green because the hard cases are gone. Under the burned V1 seed the cell
    must still draw exactly the six the V1 receipt §2.2 names, and on each of
    them the oracle and both arm tables must now agree on CENSORED.

    Public validation seed, G0-relevant quantities only: no arm verdict, ladder
    rung or gate number is read here."""
    drawn = []
    for i in range(PROTECTED_PER_CELL):
        inst = mex7_generator.generate_instance(
            "protected", BURNED_V1_SEED, "CENSORED_UNDECIDABLE", mex7_model.MODE_COMPUTATIONAL, i
        )
        if _censor_variant(inst) == "CENSOR_ENV":
            drawn.append(inst)
    assert len(drawn) == 6, f"CENSOR_ENV draws in the failing cell: {len(drawn)}"
    assert [d.instance_id[-4:] for d in drawn] == ["0002", "0011", "0015", "0019", "0042", "0045"]
    for inst in drawn:
        ep = inst.episode
        exp = mex7_oracle.oracle(ep)
        assert frozenset(exp.censored_checks) == frozenset(
            {"C_ARTIFACT_DIGEST", "C_ENV_IDENTITY"}
        ), inst.instance_id
        assert exp.verdict == mex7_model.CANNOT_CHECK
        assert exp.exhaustive_agrees, inst.instance_id
        vis = mex7_arms.visible_nodes(ep, full_registry=True)
        for check in mex7_model.CHECKS:
            want = mex7_oracle.CHECK_FN[check](ep, vis)
            assert want == mex7_arms.MODULE_CHECK_M[check](ep, vis), (inst.instance_id, check)
            assert want == mex7_arms.MODULE_CHECK_B5[check](ep, vis), (inst.instance_id, check)


def test_the_formal_environment_censoring_still_draws_and_still_censors_one_check() -> None:
    """The two formal CENSOR_ENV instances are the ones a mode-agnostic guard
    would have taken away instead."""
    formal = [
        inst
        for i in range(PROTECTED_PER_CELL)
        for inst in [
            mex7_generator.generate_instance(
                "protected", BURNED_V1_SEED, "CENSORED_UNDECIDABLE", mex7_model.MODE_FORMAL, i
            )
        ]
        if _censor_variant(inst) == "CENSOR_ENV"
    ]
    assert len(formal) == 2
    for inst in formal:
        assert frozenset(mex7_oracle.oracle(inst.episode).censored_checks) == frozenset(
            {"C_ENV_IDENTITY"}
        )


# ---- the V1 test surface, re-asserted on V2 -----------------------------------

def test_every_parent_passes_its_native_known_answer_tests() -> None:
    results = mex7_parents.fidelity_selftests()
    failed = [r for r in results if not r["passed"]]
    assert not failed, failed
    assert {r["parent"] for r in results} == set(mex7_parents.PARENT_NAMES)
    for name in mex7_parents.PARENT_NAMES:
        assert sum(1 for r in results if r["parent"] == name) >= 2, name


def test_hand_authored_known_answer_fixtures_reproduced_by_oracle() -> None:
    fixtures = mex7_generator.known_answer_fixtures()
    assert len(fixtures) == len(mex7_model.CELLS) == 25
    for f in fixtures:
        exp = mex7_oracle.oracle(f["instance"].episode)
        assert exp.verdict == f["expected"]["verdict"], f["name"]
        assert exp.defect_class == f["expected"]["defect_class"], f["name"]
        assert exp.exhaustive_agrees, f["name"]


def test_oracle_direct_rule_equals_exhaustive_enumeration_on_every_cell() -> None:
    for stratum, mode in mex7_model.CELLS:
        for i in range(2):
            inst = mex7_generator.generate_instance("t", "UNIT-SEED-V2", stratum, mode, i)
            exp = mex7_oracle.oracle(inst.episode)
            assert exp.exhaustive_agrees, (stratum, mode, i)
            ok, why = mex7_oracle.planter_agrees(
                inst.episode, stratum, censor_variant=_censor_variant(inst)
            )
            assert ok, (stratum, mode, i, why)


def test_planted_positives_trip_the_no_alarm_assertions() -> None:
    probes = mex7_generator.planted_positives()
    assert len(probes) >= 4
    tripped = 0
    for probe in probes:
        agreed, _ = mex7_oracle.planter_agrees(probe["episode"], probe["claimed_stratum"])
        if probe["must_be_rejected"]:
            assert not agreed, probe["name"]
            tripped += 1
        else:
            assert agreed, probe["name"]
    assert tripped >= 3, "the G0b assertion must be demonstrably trippable"


def test_the_episode_schema_carries_no_answer_key() -> None:
    banned = set(mex7_model.INJECTION_CLASSES) | set(mex7_model.CONTROL_STRATA) | {
        mex7_model.REJECT, mex7_model.ACCEPT,
    }
    for stratum, mode in mex7_model.CELLS:
        inst = mex7_generator.generate_instance("t", "UNIT-SEED-V2", stratum, mode, 0)
        blob = mex7_model.canonical_json(mex7_model.episode_to_json(inst.episode))
        blob = blob.replace(
            mex7_model.canonical_json(list(inst.episode.contract.decision_relevant_classes)), ""
        )
        for word in banned:
            assert word not in blob, (stratum, mode, word)


def test_arms_never_import_the_oracle() -> None:
    text = (MEX7V2 / "mex7_arms.py").read_text(encoding="utf-8")
    code = [ln for ln in text.splitlines() if ln.startswith(("import ", "from "))]
    assert not [ln for ln in code if "mex7_oracle" in ln], code
    assert "mex7_oracle" not in text.split('"""', 2)[-1]


def test_both_arm_tables_independently_reproduce_the_oracle_check_table() -> None:
    n = 0
    for stratum, mode in mex7_model.CELLS:
        for i in range(2):
            inst = mex7_generator.generate_instance("t", "UNIT-SEED-V2", stratum, mode, i)
            vis = mex7_arms.visible_nodes(inst.episode, full_registry=True)
            for check in mex7_model.CHECKS:
                want = mex7_oracle.CHECK_FN[check](inst.episode, vis)
                assert want == mex7_arms.MODULE_CHECK_M[check](inst.episode, vis), (check, stratum, mode, i)
                assert want == mex7_arms.MODULE_CHECK_B5[check](inst.episode, vis), (check, stratum, mode, i)
                n += 1
    assert n == len(mex7_model.CELLS) * 2 * len(mex7_model.CHECKS)


def test_m_and_b5_are_not_the_same_computation() -> None:
    specs = {s.name: s for s in mex7_arms.arm_specs()}
    assert specs[mex7_arms.M_ARM].table == "M"
    assert specs[mex7_arms.B5_ARM].table == "B5"
    for check in mex7_arms.DISTINCT_IMPLEMENTATIONS:
        assert mex7_arms.MODULE_CHECK_M[check] is not mex7_arms.MODULE_CHECK_B5[check], check
    shared = set(mex7_model.CHECKS) - set(mex7_arms.DISTINCT_IMPLEMENTATIONS)
    for check in shared:
        assert mex7_arms.MODULE_CHECK_M[check] is mex7_arms.MODULE_CHECK_B5[check], check
    # the defect V1 had lived in a shared implementation, which is why the
    # arm-vs-arm diagnostic could not see it
    assert "C_ARTIFACT_DIGEST" in shared


def _arm(name: str, episode):
    import random

    spec = {s.name: s for s in mex7_arms.arm_specs()}[name]
    return mex7_arms.run_arm(spec, episode, random.Random(0))


def test_m_and_b5_are_exact_on_every_hand_authored_fixture() -> None:
    for f in mex7_generator.known_answer_fixtures():
        for name in (mex7_arms.M_ARM, mex7_arms.B5_ARM):
            out = _arm(name, f["instance"].episode)
            assert out.verdict == f["expected"]["verdict"], (f["name"], name)
            if out.verdict == mex7_model.REJECT:
                assert out.detected_class == f["expected"]["defect_class"], (f["name"], name)


def test_separation_pair_self_contained_witness_is_blind_identity_exporting_is_not() -> None:
    p, q = mex7_generator.separation_pair()
    ep_p, ep_q = mex7_oracle.oracle(p.episode), mex7_oracle.oracle(q.episode)
    assert ep_p.verdict == mex7_model.REJECT and ep_p.defect_class == "HIDDEN_DEPENDENCE"
    assert ep_q.verdict == mex7_model.ACCEPT
    sc = [_arm("M_MINUS_REGISTRY_RESOLUTION", c.episode) for c in (p, q)]
    assert sc[0].verdict == sc[1].verdict, "a self-contained witness cannot separate P from Q"
    assert sc[0].verdict != ep_p.verdict or sc[1].verdict != ep_q.verdict
    for name in (mex7_arms.M_ARM, mex7_arms.B5_ARM):
        assert _arm(name, p.episode).verdict == mex7_model.REJECT
        assert _arm(name, q.episode).verdict == mex7_model.ACCEPT


def test_a_planted_version_mismatch_always_diverges_on_replay() -> None:
    for i in range(60):
        inst = mex7_generator.generate_instance(
            "t", "UNIT-SEED-V2", "SEED_OR_VERSION_MISMATCH", "MODE_COMPUTATIONAL", i
        )
        ep = inst.episode
        vis = mex7_arms.visible_nodes(ep, full_registry=True)
        assert mex7_arms.MODULE_CHECK_M["C_ENV_IDENTITY"](ep, vis) == mex7_model.INVALID, i
        assert mex7_arms.MODULE_CHECK_B5["C_ENV_IDENTITY"](ep, vis) == mex7_model.INVALID, i


def test_dropping_the_evaluator_contract_turns_abstention_into_false_acceptance() -> None:
    ep = {f["name"]: f["instance"].episode for f in mex7_generator.known_answer_fixtures()}[
        "KA-EVALUATOR_BLIND_SPOT-MODE_COMPUTATIONAL"
    ]
    assert _arm(mex7_arms.M_ARM, ep).verdict == mex7_model.REJECT
    assert _arm("M_MINUS_EVALUATOR_CONTRACT", ep).verdict == mex7_model.ACCEPT


def test_each_omission_blinds_exactly_the_classes_whose_check_needs_that_field() -> None:
    field_to_arm = {fld: name for name, fld in mex7_arms.ABLATION_FIELDS}
    for cls in mex7_model.INJECTION_CLASSES:
        check = mex7_model.CHECK_FOR_CLASS[cls]
        needed = {field_to_arm[f] for f in mex7_model.REQUIRED_FIELDS[check] if f in field_to_arm}
        for mode in mex7_model.MODES:
            if not mex7_model.cell_applicable(cls, mode):
                continue
            ep = mex7_generator.generate_instance("t", "UNIT-SEED-V2", cls, mode, 0).episode
            for name, _ in mex7_arms.ABLATION_FIELDS:
                out = _arm(name, ep)
                detected = out.verdict == mex7_model.REJECT and out.detected_class == cls
                assert detected == (name not in needed), (cls, mode, name)


# ---- runner stages -------------------------------------------------------------

def test_selftest_stage_passes(tmp_path: Path) -> None:
    assert mex7_run.stage_selftest(tmp_path) == 0
    report = json.loads((tmp_path / "ME_X7_SELFTEST_REPORT.json").read_text())
    assert report["passed"] is True
    assert report["separation"]["passed"] is True
    assert all(p["passed"] for p in report["planted_positives"])
    assert len(report["known_answer"]) == len(mex7_model.CELLS)


def test_dev_stage_end_to_end_is_labelled_development(tmp_path: Path) -> None:
    assert mex7_run.stage_dev(tmp_path, mex7_run.DEV_PER_CELL) == 0
    res = json.loads((tmp_path / "ME_X7_DEVELOPMENT_RESULTS_V1.json").read_text())
    assert res["label"] == "DEVELOPMENT"
    assert len(res["instances"]) == len(mex7_model.CELLS)
    assert "DEVELOPMENT split: not protected evidence" in (
        tmp_path / "ME_X7_DEVELOPMENT_ANALYSIS_V1.md"
    ).read_text()


def test_dev_stage_refuses_more_than_forty_instances(tmp_path: Path) -> None:
    assert mex7_run.stage_dev(tmp_path, 3) == 2


def test_every_gate_reports_the_number_of_instances_it_evaluated(tmp_path: Path) -> None:
    assert mex7_run.stage_dev(tmp_path, mex7_run.DEV_PER_CELL) == 0
    gates = json.loads((tmp_path / "ME_X7_DEVELOPMENT_ANALYSIS_V1.json").read_text())["gates"]
    for name, g in gates.items():
        if name in ("ROUTE", "COST"):
            continue
        assert "n_evaluated" in g, name
        assert isinstance(g["n_evaluated"], int), name
    for name, c in gates["G5_SUFFICIENCY"]["conjuncts"].items():
        assert isinstance(c["n_evaluated"], int), name
    cc = gates["G7_WITNESS_SELF_CONTAINMENT"]
    assert cc["status"].startswith("CANNOT_CHECK") or cc["n_evaluated"] > 0
    if cc["n_evaluated"] == 0:
        assert cc["pass"] is False, "an unevaluated gate is CANNOT_CHECK, never a pass"
        assert "SELF_CONTAINMENT_CANNOT_CHECK" in gates["ROUTE"]["witness_terminal"]


def test_the_arm_vs_arm_diagnostic_is_named_for_what_it_compares(tmp_path: Path) -> None:
    """Correction 3, label-only: the key says arm-vs-arm and the rule says the
    diagnostic cannot see a defect in a shared implementation."""
    assert mex7_run.stage_dev(tmp_path, mex7_run.DEV_PER_CELL) == 0
    gates = json.loads((tmp_path / "ME_X7_DEVELOPMENT_ANALYSIS_V1.json").read_text())["gates"]
    assert "IMPLEMENTATION_AGREEMENT" not in gates
    ia = gates["ARM_VS_ARM_IMPLEMENTATION_AGREEMENT"]
    assert "shared implementation" in ia["rule"]
    assert "G0b" in ia["rule"]
    assert ia["n_evaluated"] == len(mex7_model.CELLS)


def test_the_coverage_ledger_names_every_unexercised_mechanism(tmp_path: Path) -> None:
    assert mex7_run.stage_dev(tmp_path, mex7_run.DEV_PER_CELL) == 0
    cl = json.loads((tmp_path / "ME_X7_DEVELOPMENT_ANALYSIS_V1.json").read_text())["gates"][
        "COVERAGE_LEDGER"
    ]
    assert cl["all_registered_mechanisms_exercised"] is False
    assert cl["never_exercised"]["censor_variants"], "undrawn variants must be named"
    assert cl["never_exercised"]["cells"] == [], "every applicable cell is drawn once"
    assert sum(cl["drawn"]["cell"].values()) == len(mex7_model.CELLS)


def test_analyze_fires_the_federation_ahead_gate_on_a_planted_m_degradation(tmp_path: Path) -> None:
    assert mex7_run.stage_dev(tmp_path, mex7_run.DEV_PER_CELL) == 0
    rp = tmp_path / "ME_X7_DEVELOPMENT_RESULTS_V1.json"
    cp = tmp_path / "ME_X7_DEVELOPMENT_EXPECTED_CUSTODY_V1.json"
    res = json.loads(rp.read_text())
    for rec in res["instances"]:
        rec["arms"][mex7_run.M_ARM] = {
            "verdict": mex7_model.ACCEPT, "detected_class": None, "checks_run": 11, "export_units": 40
        }
    rp.write_text(json.dumps(res))
    assert mex7_run.stage_analyze(rp, cp, tmp_path, "DEVELOPMENT") == 0
    g = json.loads((tmp_path / "ME_X7_DEVELOPMENT_ANALYSIS_V1.json").read_text())["gates"]
    assert g["G1c_B5_AHEAD"]["pass"] is True
    assert g["G1a_B5_REPRODUCES_M"]["pass"] is False
    assert g["ROUTE"]["witness_terminal"] == "WITNESS_INSUFFICIENT_PARENT_AHEAD"
    assert g["G5_SUFFICIENCY"]["conjuncts"]["S4_FALSE_ACCEPTANCE_NONINFERIORITY"]["pass"] is False


def test_analyze_on_the_unmodified_null_reaches_the_registered_expectation(tmp_path: Path) -> None:
    assert mex7_run.stage_dev(tmp_path, mex7_run.DEV_PER_CELL) == 0
    g = json.loads((tmp_path / "ME_X7_DEVELOPMENT_ANALYSIS_V1.json").read_text())["gates"]
    assert g["G0b_ORACLE_SELF_AGREEMENT"]["pass"] is True
    assert g["G0c_NULL_CALIBRATION"]["pass"] is True
    assert g["G1b_M_ADVANTAGE"]["pass"] is False
    assert g["G1c_B5_AHEAD"]["pass"] is False
    assert g["ROUTE"]["route"] == "PARENT_SUFFICIENT"


def test_reruns_are_byte_identical_apart_from_wall_clock(tmp_path: Path) -> None:
    import hashlib

    a_dir, b_dir = tmp_path / "a", tmp_path / "b"
    assert mex7_run.stage_dev(a_dir, mex7_run.DEV_PER_CELL) == 0
    assert mex7_run.stage_dev(b_dir, mex7_run.DEV_PER_CELL) == 0
    for name in ("RESULTS", "EXPECTED_CUSTODY"):
        fn = f"ME_X7_DEVELOPMENT_{name}_V1.json"
        assert (a_dir / fn).read_bytes() == (b_dir / fn).read_bytes(), name

    # The four wall-clock fields the design's determinism claim names, plus the
    # two places the COST flag derived from them is written. The flag is a
    # threshold on a wall-clock ratio, so it is wall-clock-derived and is not
    # covered by "identical apart from the wall-clock fields it quotes"; a run
    # whose ratio lands near 2.0 flips it. Asserting on it made this test
    # intermittently red without testing anything the design claims.
    drop = {"wall_ms", "M_wall_ms", "B5_wall_ms", "wall_ratio_b5_over_m",
            "flag", "cost_flag"}

    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in o.items() if k not in drop}
        if isinstance(o, list):
            return [strip(v) for v in o]
        return o

    def digest(d: Path) -> str:
        blob = json.loads((d / "ME_X7_DEVELOPMENT_ANALYSIS_V1.json").read_text())
        return hashlib.sha256(json.dumps(strip(blob), sort_keys=True).encode()).hexdigest()

    assert digest(a_dir) == digest(b_dir)


# ---- custody: no authorization is committed, and both refusals are distinct ----

def test_no_protected_authorization_is_committed_and_the_guard_is_armed() -> None:
    assert not mex7_run.AUTH_FILE.exists(), "an authorization file must not be committed"
    assert not (MEX7V2 / "PROTECTED_RUN_AUTHORIZATION.json").exists()


def test_protected_stage_refuses_with_exit_3_for_authorization_and_exit_4_for_the_seed(
    tmp_path: Path, monkeypatch
) -> None:
    assert not mex7_run.AUTH_FILE.exists()
    assert mex7_run.stage_protected(tmp_path, 1, tmp_path / "absent-seed.txt") == 3
    auth = tmp_path / "PROTECTED_RUN_AUTHORIZATION.json"
    monkeypatch.setattr(mex7_run, "AUTH_FILE", auth)
    auth.write_text(json.dumps({"human_written": True, "human_written_token": "short"}))
    assert mex7_run.stage_protected(tmp_path, 1, tmp_path / "absent-seed.txt") == 3
    auth.write_text(json.dumps({
        "human_written": True,
        "human_written_token": "a-sufficiently-long-token",
        "acknowledged_design_sha256": "0" * 64,
    }))
    assert mex7_run.stage_protected(tmp_path, 1, tmp_path / "absent-seed.txt") == 3
    auth.write_text(json.dumps({
        "human_written": True,
        "human_written_token": "a-sufficiently-long-token",
        "acknowledged_design_sha256": mex7_run.sha256_file(mex7_run.DESIGN_JSON),
    }))
    # authorization now valid: the refusal that remains is the seed's, and it
    # has its own exit code so "not authorized" is never read as "no seed"
    assert mex7_run.stage_protected(tmp_path, 1, tmp_path / "absent-seed.txt") == 4
    bad = tmp_path / "seed.txt"
    bad.write_text("not-the-committed-seed")
    assert mex7_run.stage_protected(tmp_path, 1, bad) == 4
    burned = tmp_path / "burned.txt"
    burned.write_text(BURNED_V1_SEED)
    assert mex7_run.stage_protected(tmp_path, 1, burned) == 4, (
        "the revealed V1 seed must not open the V2 protected stage"
    )
    assert not list(tmp_path.glob("ME_X7_PROTECTED_*")), "a refused run creates no output"


# ---- design freeze --------------------------------------------------------------

def test_design_json_freezes_the_v2_commitment_the_cells_and_the_arm_table() -> None:
    d = json.loads(DESIGN_JSON.read_text())
    assert d["schema_version"] == "orion.v2.me-x7-v2.exact-study-design.v2"
    assert len(d["seed_commitment"]["protected_seed_sha256"]) == 64
    assert d["seed_commitment"]["development_seed_public"] == mex7_run.DEV_SEED
    assert d["seed_commitment"]["custody_path"] == "~/.orion-custody/me-x7-v2/PROTECTED_SEED_V1.txt"
    assert [tuple(c) for c in d["cells"]] == list(mex7_model.CELLS)
    assert d["strata"] == list(mex7_model.STRATA)
    assert d["witness_fields"] == list(mex7_model.FIELDS)
    assert d["checks"] == list(mex7_model.CHECKS)
    assert d["required_fields_per_check"] == {
        k: list(v) for k, v in mex7_model.REQUIRED_FIELDS.items()
    }
    assert d["field_for_class"] == mex7_model.FIELD_FOR_CLASS
    assert [a["name"] for a in d["arms"]] == [s.name for s in mex7_arms.arm_specs()]
    tables = {a["name"]: a["check_table"] for a in d["arms"]}
    assert tables[mex7_arms.M_ARM] == "M" and tables[mex7_arms.B5_ARM] == "B5"
    assert d["check_tables"]["distinct_implementations"] == list(mex7_arms.DISTINCT_IMPLEMENTATIONS)
    assert "G7_WITNESS_SELF_CONTAINMENT" in d["gates"]
    assert d["split_sizes"]["protected_total"] == 50 * len(mex7_model.CELLS)
    assert d["primary_comparator"] == mex7_arms.B5_ARM
    assert d["expected_route"] == "PARENT_SUFFICIENT"
    assert d["not_applicable_cells"] == [["INVALID_CALIBRATION", "MODE_FORMAL"]]
    assert d["reported_not_gated"] == [
        "COVERAGE_LEDGER", "ARM_VS_ARM_IMPLEMENTATION_AGREEMENT", "COST",
    ]


def test_the_design_declares_the_same_censored_table_the_oracle_enforces() -> None:
    d = json.loads(DESIGN_JSON.read_text())
    declared = {
        tuple(k.split("|")): frozenset(v)
        for k, v in d["expected_censored_checks"]["table"].items()
    }
    assert declared == dict(mex7_oracle.EXPECTED_CENSORED_CHECKS)


def test_the_design_registers_exactly_the_corrections_that_separate_v2_from_v1() -> None:
    d = json.loads(DESIGN_JSON.read_text())
    ids = [c["id"] for c in d["registered_corrections"]]
    assert ids == [
        "V2_CORRECTION_1_ARTIFACT_DIGEST_CENSORED_STATE",
        "V2_CORRECTION_2_DECLARED_EXPECTED_CENSORED_SET",
        "V2_CORRECTION_3_ARM_VS_ARM_DIAGNOSTIC_LABEL",
    ]
    assert d["parent_design"]["v1_route"] == "CANNOT_CHECK"
    assert d["parent_design"]["v1_witness_terminal"] == "NONE"
    assert d["status"] == "FROZEN_DESIGN_V2_NO_PROTECTED_OUTCOME_INSPECTED"


def test_the_v2_commitment_is_not_the_burned_v1_seed() -> None:
    import hashlib

    d = json.loads(DESIGN_JSON.read_text())
    commitment = d["seed_commitment"]["protected_seed_sha256"]
    v1_commitment = "2c8a3d774cab1fcae49fae5876d9ed314ea771563fa31ff44784c3dd3e2cf4b2"
    assert commitment != v1_commitment
    assert hashlib.sha256(BURNED_V1_SEED.encode()).hexdigest() == v1_commitment
    assert hashlib.sha256(BURNED_V1_SEED.encode()).hexdigest() != commitment
    assert d["seed_commitment"]["v1_seed_burned"] == BURNED_V1_SEED


def test_the_non_applicable_cell_is_generated_zero_times() -> None:
    assert ("INVALID_CALIBRATION", "MODE_FORMAL") not in mex7_model.CELLS
    assert mex7_model.cell_applicable("INVALID_CALIBRATION", "MODE_COMPUTATIONAL")
    assert not mex7_model.cell_applicable("INVALID_CALIBRATION", "MODE_FORMAL")

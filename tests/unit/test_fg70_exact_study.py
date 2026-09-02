"""FG70 exact `formalism needed or not` study: end-to-end tests of every runner
stage on development fixtures. Nothing here is protected evidence.

Series identity ORION-FG-L5-EXACT-V1 (owner issue #50 §L5). This is not the
fmfg-r2 campaign of owner issue #48, which used the same study labels for
language-model solver arms; see the design's disambiguation block.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
FG = ROOT / "research" / "experiments" / "fg"
for extra in (str(FG), str(ROOT / "src")):
    if extra not in sys.path:
        sys.path.insert(0, extra)


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, FG / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


fg_model = _load("fg_model")
fg_oracle = _load("fg_oracle")
fg_parents = _load("fg_parents")
fg70_generator = _load("fg70_generator")
fg_arms = _load("fg_arms")
fg_run = _load("fg_run")


# ---- parents: native known-answer tests must pass before use ----------------


def test_every_parent_passes_its_native_known_answer_tests() -> None:
    results = fg_parents.fidelity_selftests()
    failed = [row for row in results if not row["passed"]]
    assert not failed, failed
    assert {row["parent"] for row in results} == set(fg_parents.PARENT_NAMES)
    assert len(results) >= 40


def test_mdl_parent_is_not_a_reskin_of_the_registered_order() -> None:
    """The MDL parent must disagree with the registered search order somewhere,
    or it is not an independent parent."""
    results = {row["test"]: row for row in fg_parents.fidelity_selftests()}
    assert results["native_order_differs_from_registered_order"]["passed"]


# ---- oracle: hand-authored fixtures and two-method agreement ----------------


def test_hand_authored_known_answer_fixtures_reproduced_by_oracle() -> None:
    fixtures = fg70_generator.known_answer_fixtures()
    assert {f["expected"] for f in fixtures} == set(fg_model.REPAIR_TIERS)
    for fixture in fixtures:
        agree, method_a, method_b = fg_oracle.oracle_agrees(fixture["instance"])
        assert agree, (fixture["name"], method_a.terminal, method_b.terminal)
        assert method_a.terminal == fixture["expected"], (fixture["name"], method_a.terminal)


def test_oracle_methods_agree_on_generated_instances() -> None:
    for stratum in fg70_generator.STRATA:
        for index in range(2):
            instance = fg70_generator.generate_instance("t", "UNIT-SEED", stratum, index)
            agree, method_a, _ = fg_oracle.oracle_agrees(instance)
            assert agree, (stratum, index)
            assert method_a.terminal == stratum, (stratum, index, method_a.terminal)


def test_generator_is_deterministic_and_round_trips_json() -> None:
    a = fg70_generator.generate_instance("t", "UNIT-SEED", fg_model.LOCAL_PATCH, 1)
    b = fg70_generator.generate_instance("t", "UNIT-SEED", fg_model.LOCAL_PATCH, 1)
    ja = fg_model.canonical_json(fg_model.instance_to_json(a))
    assert ja == fg_model.canonical_json(fg_model.instance_to_json(b))
    back = fg_model.instance_from_json(json.loads(ja))
    assert fg_model.canonical_json(fg_model.instance_to_json(back)) == ja
    c = fg70_generator.generate_instance("t", "OTHER-SEED", fg_model.LOCAL_PATCH, 1)
    assert fg_model.canonical_json(fg_model.instance_to_json(c)) != ja


_DIGEST_SNIPPET = (
    "import sys;sys.path[:0]=[%r,%r];"
    "import fg70_generator as g,fg_arms as A,fg_model as M;"
    "sp=g.generate_split('dev','FG70-DEV-20260902',2);"
    "print(M.instances_digest(sp));"
    "print(M.sha256_text(M.canonical_json("
    "[[A.run_arm(n,M.arm_view(i)).terminal for n in A.ARM_SPECS] for i in sp])))"
)


@pytest.mark.parametrize("hash_seed", ["0", "1", "12345"])
def test_split_and_arms_reproduce_across_processes(hash_seed: str) -> None:
    """Python randomises str hashing per process, so a planter that iterates an
    unordered set would draw different RNG values in different processes and the
    'same' split would not regenerate. The design promises byte-identical
    re-runs; this asserts it where it can actually break."""
    digests = []
    for seed in ("0", hash_seed):
        proc = subprocess.run(
            [sys.executable, "-c", _DIGEST_SNIPPET % (str(FG), str(ROOT / "src"))],
            capture_output=True,
            text=True,
            env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": seed},
        )
        assert proc.returncode == 0, proc.stderr
        digests.append(proc.stdout.strip())
    assert digests[0] == digests[1], digests


def test_generator_never_iterates_an_unordered_set() -> None:
    source = (FG / "fg70_generator.py").read_text(encoding="utf-8")
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        assert " in set(" not in stripped or "sorted(set(" in stripped, line


def test_arm_view_hides_the_label_and_the_planted_decoys() -> None:
    instance = fg70_generator.generate_instance("t", "UNIT-SEED", fg_model.NEW_PRIMITIVE, 0)
    view = fg_model.arm_view(instance)
    assert "stratum" not in view and "planted_decoys" not in view
    assert view["repair_tiers"] == list(fg_model.REPAIR_TIERS)


# ---- arms -------------------------------------------------------------------


def test_m_and_federation_exact_on_hand_authored_fixtures() -> None:
    for fixture in fg70_generator.known_answer_fixtures():
        view = fg_model.arm_view(fixture["instance"])
        for arm in (fg_arms.M_ARM, fg_arms.B_ARM):
            got = fg_arms.run_arm(arm, view).terminal
            assert got == fixture["expected"], (fixture["name"], arm, got)


def test_no_arm_module_imports_the_oracle() -> None:
    for name in ("fg_arms", "fg_parents", "fg_model"):
        source = (FG / f"{name}.py").read_text(encoding="utf-8")
        assert "import fg_oracle" not in source, name
        assert "from fg_oracle" not in source, name


def test_single_parents_break_where_their_semantics_predict() -> None:
    fixtures = {f["expected"]: f["instance"] for f in fg70_generator.known_answer_fixtures()}
    # AGM base revision cannot extend a language: it must refuse, not invent.
    got = fg_arms.run_arm(
        "P6_THEORY_REVISION_BASELINE", fg_model.arm_view(fixtures[fg_model.NEW_PRIMITIVE])
    )
    assert got.terminal in {fg_arms.CANNOT_CHECK, fg_model.LOCAL_PATCH}
    assert got.terminal != fg_model.NEW_PRIMITIVE
    # conservative-extension checking is an admission filter, never a selector
    statuses = {
        fg_arms.run_arm("P5_CONSERVATIVE_EXTENSION_CHECK", fg_model.arm_view(inst)).terminal
        for inst in fixtures.values()
    }
    assert fg_arms.CANNOT_CHECK in statuses
    # the MDL parent prices a new primitive by its whole extension, so it never
    # invents on a fixture whose truth is cheaper
    for terminal, instance in fixtures.items():
        if terminal == fg_model.NEW_PRIMITIVE:
            continue
        assert (
            fg_arms.run_arm("P3_MDL_ABSTRACTION_SEARCH", fg_model.arm_view(instance)).terminal
            != fg_model.NEW_PRIMITIVE
        )


# ---- the anti-invention gate must be shown to fire ---------------------------


def test_planted_positive_trips_the_anti_invention_counter() -> None:
    """The recurring defect this guards against: a gate reporting zero
    violations because it never executed on the relevant cases."""
    tripped = 0
    denominator = 0
    for fixture in fg70_generator.known_answer_fixtures():
        if fixture["expected"] in (fg_model.NO_CHANGE, fg_model.NEW_PRIMITIVE):
            continue
        denominator += 1
        view = fg_model.arm_view(fixture["instance"])
        if fg_arms.run_arm("C_ALWAYS_INVENT", view).terminal == fg_model.NEW_PRIMITIVE:
            tripped += 1
    assert denominator > 0
    assert tripped == denominator, (tripped, denominator)


def test_planted_positive_trips_the_anti_conservatism_counter() -> None:
    """G2's mirror: every arm's first move is the shared collision check, so
    the missed-deficit counter is structurally hard to reach and must be shown
    to fire on a planted positive."""
    tripped = 0
    denominator = 0
    for fixture in fg70_generator.known_answer_fixtures():
        if fixture["expected"] == fg_model.NO_CHANGE:
            continue
        denominator += 1
        view = fg_model.arm_view(fixture["instance"])
        if fg_arms.run_arm("C_NEVER_CHANGE", view).terminal == fg_model.NO_CHANGE:
            tripped += 1
    assert denominator > 0
    assert tripped == denominator, (tripped, denominator)


def test_every_stratum_has_an_ablation_that_degrades_it() -> None:
    """G3's per-stratum rule must be satisfiable: an ablation mapped to a
    stratum it cannot possibly degrade would fail the gate by construction."""
    assert set(fg_arms.ABLATION_FOR_STRATUM) == set(fg70_generator.STRATA)
    for stratum, ablation in fg_arms.ABLATION_FOR_STRATUM.items():
        instances = [
            fg70_generator.generate_instance("t", "UNIT-SEED", stratum, index)
            for index in range(2)
        ]
        correct = sum(
            1
            for instance in instances
            if fg_arms.run_arm(ablation, fg_model.arm_view(instance)).terminal == stratum
        )
        m_correct = sum(
            1
            for instance in instances
            if fg_arms.run_arm(fg_arms.M_ARM, fg_model.arm_view(instance)).terminal == stratum
        )
        assert m_correct == len(instances), (stratum, m_correct)
        assert correct < m_correct, (stratum, ablation, correct, m_correct)


def test_invention_is_always_available_and_always_adequate_on_cheaper_strata() -> None:
    checked = 0
    for stratum in fg70_generator.STRATA:
        if stratum in (fg_model.NO_CHANGE, fg_model.NEW_PRIMITIVE):
            continue
        instance = fg70_generator.generate_instance("t", "UNIT-SEED", stratum, 0)
        verdict = fg_oracle.tier_search(instance)
        assert fg_model.NEW_PRIMITIVE in verdict.feasible_tiers, stratum
        checked += 1
    assert checked == 4


def test_cost_order_and_admission_gate_are_separately_ablatable() -> None:
    split = fg70_generator.generate_split("t", "UNIT-SEED", 2)
    non_invention = [i for i in split if i.stratum != fg_model.NEW_PRIMITIVE]
    assert non_invention

    def false_inventions(arm: str) -> int:
        return sum(
            1
            for instance in non_invention
            if fg_arms.run_arm(arm, fg_model.arm_view(instance)).terminal == fg_model.NEW_PRIMITIVE
        )

    assert false_inventions(fg_arms.M_ARM) == 0
    assert false_inventions("M_MINUS_ORDER_AND_GATE") > 0
    assert false_inventions("C_ALWAYS_INVENT") > 0


# ---- runner stages ----------------------------------------------------------


def test_selftest_stage_passes(tmp_path: Path) -> None:
    report = fg_run.selftest()
    failed = [check for check in report["checks"] if not check["passed"]]
    assert not failed, failed
    assert report["passed"]
    for check in report["checks"]:
        assert check["instances_evaluated"] > 0, check["check"]


def test_dev_stage_runs_and_routes(tmp_path: Path) -> None:
    code = fg_run.main(["dev", "--out", str(tmp_path)])
    assert code == 0
    analysis = json.loads((tmp_path / "FG70_DEVELOPMENT_ANALYSIS_V1.json").read_text())
    assert analysis["instances"] == fg_run.DEV_PER_STRATUM * len(fg70_generator.STRATA)
    assert analysis["gates"]["G0b_ORACLE_SELF_AGREEMENT"]["verdict"] == "PASS"
    assert analysis["gates"]["G0c_NULL_CALIBRATION"]["verdict"] == "PASS"
    assert analysis["gates"]["G2M_ANTI_INVENTION"]["verdict"] == "PASS"
    assert analysis["gates"]["G2_ANTI_CONSERVATISM"]["verdict"] == "PASS"
    assert analysis["gates"]["G2_ANTI_CONSERVATISM"]["planted_positive_C_NEVER_CHANGE_missed_deficits"] > 0
    assert all(row["ablation_degrades"] for row in analysis["gates"]["G3_MECHANISM_BY_OMISSION"]["rows"])
    checks = analysis["gates"]["G0c_NULL_CALIBRATION"]["checks"]
    assert checks["planted_positive_C_ALWAYS_INVENT_false_invention_rate"] >= 0.5
    assert checks["planted_positive_C_NEVER_CHANGE_missed_deficit_rate"] >= 0.5
    assert not analysis["gates"]["G2M_ANTI_INVENTION"]["empty_denominator_strata"]
    assert all(value is False for value in analysis["authority"].values())
    for gate in analysis["gates"].values():
        assert gate["instances_evaluated"] > 0


def test_protected_stage_refuses_without_authorization(tmp_path: Path) -> None:
    assert not (FG / "PROTECTED_RUN_AUTHORIZATION.json").exists()
    proc = subprocess.run(
        [sys.executable, str(FG / "fg_run.py"), "protected", "--out", str(tmp_path)],
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin", "PYTHONPATH": str(ROOT / "src")},
    )
    assert proc.returncode == 3, proc.stderr
    assert "REFUSED" in proc.stderr


# ---- frozen design ----------------------------------------------------------


def test_design_json_is_frozen_and_non_authorizing() -> None:
    design = json.loads(
        (FG / "FG70_FORMALISM_NEEDED_OR_NOT_EXACT_STUDY_DESIGN_V1.json").read_text()
    )
    assert design["series_id"] == "ORION-FG-L5-EXACT-V1"
    assert design["owner_issue"] == 50
    assert design["counts"]["protected_total"] >= design["counts"]["registered_minimum"] == 160
    assert design["counts"]["protected_total"] % design["counts"]["strata"] == 0
    assert design["registered_search_order"] == list(fg_model.REPAIR_TIERS)
    assert design["critical_metric"]["status"] == "CO_PRIMARY_NON_COMPENSATORY"
    assert all(value is False for value in design["authority"].values())
    assert design["disambiguation"]["not_to_be_confused_with"]["owner_issue"] == 48
    assert design["custody"]["authorization_absent_in_this_pr"] is True
    assert len(design["custody"]["protected_seed_sha256"]) == 64

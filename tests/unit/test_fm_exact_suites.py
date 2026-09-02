"""Custody and validity tests for the FM exact-study suites.

These are fast (well under the CI job timeout): the selftest split is 2
instances per family and the development split is 3.  Nothing here touches the
protected split, and the protected stage is asserted to refuse.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
FM = ROOT / "research/experiments/fm-exact"
SUITES = ["FM10", "FM20", "FM30", "FM40"]


@pytest.fixture(scope="module")
def fm_path():
    sys.path.insert(0, str(FM))
    sys.path.insert(0, str(ROOT / "src"))
    yield
    sys.path.remove(str(FM))


# --------------------------------------------------------------------------
# shared harness
# --------------------------------------------------------------------------


def test_gate_with_no_denominator_cannot_pass(fm_path):
    from fm_core import GateResult

    g = GateResult("G", "rule", n_evaluated=0, n_violations=0, requires_evaluated=1)
    assert g.verdict == "CANNOT_CHECK"
    assert g.passed is None, "a gate that evaluated nothing must never report a pass"


def test_gate_block_rejects_cannot_check(fm_path):
    from fm_core import GateResult, gate_block_ok

    ok = GateResult("A", "r", n_evaluated=5, n_violations=0)
    unchecked = GateResult("B", "r", n_evaluated=0, n_violations=0, requires_evaluated=3)
    assert gate_block_ok([ok]) is True
    assert gate_block_ok([ok, unchecked]) is False


def test_discrimination_gate_fails_a_degenerate_ceiling_table(fm_path):
    from fm_core import discrimination_gate

    ceiling = discrimination_gate(
        {"weak": 1.0, "strong": 1.0}, weak_arms=("weak",), max_weak=0.85, min_strong=0.95
    )
    assert ceiling.verdict == "FAIL", "the FM/FG R2 ceiling defect must be caught"
    assert ceiling.detail["halves"]["separating"]["violation"] is True
    assert ceiling.detail["halves"]["solvable"]["violation"] is False

    floor = discrimination_gate(
        {"weak": 0.2, "strong": 0.3}, weak_arms=("weak",), max_weak=0.85, min_strong=0.95
    )
    assert floor.verdict == "FAIL", "the FM/FG R2 floor defect must be caught too"
    assert floor.detail["halves"]["solvable"]["violation"] is True

    good = discrimination_gate(
        {"weak": 0.5, "strong": 1.0}, weak_arms=("weak",), max_weak=0.85, min_strong=0.95
    )
    assert good.verdict == "PASS"
    assert good.n_evaluated == 2, "each half reports its own denominator"


def test_exact_binomial_and_holm(fm_path):
    from fm_core import exact_binomial_two_sided, holm

    assert exact_binomial_two_sided(0, 0) == 1.0
    assert exact_binomial_two_sided(10, 0) == pytest.approx(2 / 2**10)
    adj = holm({"a": 0.01, "b": 0.04})
    assert adj["a"]["holm_p"] == pytest.approx(0.02)
    assert adj["b"]["holm_p"] == pytest.approx(0.04)


# --------------------------------------------------------------------------
# per-suite validity
# --------------------------------------------------------------------------


@pytest.mark.parametrize("suite", SUITES)
def test_parent_fidelity_all_pass(fm_path, suite):
    """No parent may be used as a comparator until its native tests pass."""
    from fm_run import load_suite

    spec = load_suite(suite)
    tests = spec.parent_fidelity()
    failed = [t for t in tests if not t["passed"]]
    assert not failed, f"{suite} parent fidelity failures: {failed}"
    assert len(tests) >= 15


@pytest.mark.parametrize("suite", SUITES)
def test_known_answer_fixtures_reproduced_by_both_oracles(fm_path, suite):
    from fm_run import load_suite

    spec = load_suite(suite)
    fixtures = spec.known_answer_fixtures()
    assert len(fixtures) >= 8
    for f in fixtures:
        a = spec.oracle(f["instance"])
        b = spec.cross_check(f["instance"])
        assert a.disposition == f["expected"], f"{f['name']}: {a.disposition}"
        assert b.disposition == a.disposition, f"{f['name']}: cross-check disagrees"


@pytest.mark.parametrize("suite", SUITES)
def test_every_planted_positive_fires(fm_path, suite):
    """A no-alarm assertion is only believable if its predicate fires somewhere."""
    from fm_run import load_suite

    spec = load_suite(suite)
    planted = spec.planted_positives()
    assert len(planted) >= 3
    not_fired = [p.name for p in planted if not p.fired]
    assert not not_fired, f"{suite} planted positives did not fire: {not_fired}"


@pytest.mark.parametrize("suite", SUITES)
def test_oracles_agree_on_a_generated_split(fm_path, suite):
    from fm_run import load_suite, oracle_disagrees

    spec = load_suite(suite)
    pairs, _ = spec.generate("unittest", f"{suite}-UNITTEST", {f: 2 for f in spec.families})
    assert len(pairs) == 2 * len(spec.families)
    assert spec.oracle_agreement_fields, f"{suite} declares no oracle agreement fields"
    for inst, ans in pairs:
        assert not oracle_disagrees(spec, ans, spec.cross_check(inst)), inst.instance_id


@pytest.mark.parametrize("suite", SUITES)
def test_generated_family_intent_is_verified_not_assumed(fm_path, suite):
    from fm_run import load_suite

    spec = load_suite(suite)
    mod = sys.modules[f"{suite.lower()}_suite"]
    allowed = getattr(mod, "EXPECTED_DISPOSITION", None)
    pairs, _ = spec.generate("unittest", f"{suite}-UNITTEST", {f: 2 for f in spec.families})
    for inst, ans in pairs:
        expected = allowed[inst.family] if allowed else {inst.family}
        assert ans.disposition in expected, (
            f"{inst.instance_id}: family {inst.family} produced {ans.disposition}"
        )


@pytest.mark.parametrize("suite", SUITES)
def test_mechanic_is_not_a_wrapper_of_its_own_comparator(fm_path, suite):
    """G1a must be a measurement, not an algebraic identity.

    The mechanic's discordance against the parent has to be *able* to be
    nonzero.  Every ablation is a known-different mechanic, so at least one of
    them must disagree with the parent on a real split; if none does, the
    identity counter is dead and G1a's zero would mean nothing.
    """
    from fm_run import load_suite, run_instances, score

    spec = load_suite(suite)
    pairs, _ = spec.generate("unittest", f"{suite}-UNITTEST", {f: 2 for f in spec.families})
    res, cus = run_instances(spec, pairs, "T", "seed")
    sc = score(spec, res, cus)
    P = spec.strongest_parent_arm
    ablations = [a.name for a in spec.arms if a.kind == "ABLATION"]
    discordance = {
        a: sum(1 for x, y in zip(sc["_preds"][a], sc["_preds"][P]) if x != y) for a in ablations
    }
    assert any(v > 0 for v in discordance.values()), (
        f"{suite}: no ablation disagrees with {P}; the G1a counter is dead: {discordance}"
    )


@pytest.mark.parametrize("suite", SUITES)
def test_generator_is_independent_of_python_hash_seed(fm_path, suite):
    """A committed seed must regenerate the same split in any process.

    Python randomises string hashing per process, so a generator that draws
    while iterating an unordered set produces a different split under a
    different PYTHONHASHSEED - and a published seed commitment then fails to
    reproduce.  Checked here rather than assumed.
    """
    script = (
        "import sys, hashlib\n"
        f"sys.path.insert(0, {str(FM)!r}); sys.path.insert(0, {str(ROOT / 'src')!r})\n"
        "from fm_core import canonical_json\n"
        "import fm_run as R\n"
        f"spec = R.load_suite({suite!r})\n"
        "pairs, rej = spec.generate('protected','HASHSEED-PROBE',{f:2 for f in spec.families})\n"
        "res, cus = R.run_instances(spec, pairs, 'P', None); res.pop('_timing_wall_ns')\n"
        "print(hashlib.sha256((canonical_json(res)+canonical_json(cus)"
        "+canonical_json(rej)).encode()).hexdigest())\n"
    )
    digests = set()
    for hashseed in ("0", "1", "12345"):
        proc = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONHASHSEED": hashseed},
        )
        assert proc.returncode == 0, proc.stderr
        digests.add(proc.stdout.strip())
    assert len(digests) == 1, (
        f"{suite}: the generated split depends on PYTHONHASHSEED ({digests}); a "
        "committed seed would not reproduce in another process"
    )


@pytest.mark.parametrize("suite", SUITES)
def test_anti_permissiveness_counter_can_fire(fm_path, suite):
    """An anti-conservatism gate that passes on 0 <= 0 must show it could fire.

    On the instances the oracle rejects, at least one arm must register a
    nonzero over-acceptance count, or the gate's zero is vacuous.
    """
    from fm_run import load_suite, run_instances, score

    spec = load_suite(suite)
    pairs, _ = spec.generate("unittest", f"{suite}-UNITTEST", {f: 3 for f in spec.families})
    res, cus = run_instances(spec, pairs, "T", "seed")
    sc = score(spec, res, cus)

    if spec.unsafe_scope is not None and spec.unsafe_claim is not None:
        scope = [i for i, e in enumerate(sc["expected_full"]) if spec.unsafe_scope(e)]

        def unsafe(a: str, i: int) -> bool:
            return bool(spec.unsafe_claim(sc["_records"][i][a], sc["expected_full"][i]))
    else:

        def accepts(label: str) -> bool:
            return not label.startswith("BLOCK") and not label.startswith("REJECT")

        scope = [i for i, lab in enumerate(sc["labels"]) if not accepts(lab)]

        def unsafe(a: str, i: int) -> bool:
            return accepts(sc["_preds"][a][i])

    assert scope, f"{suite}: no in-scope instances to evaluate the gate on"
    over = {a: sum(1 for i in scope if unsafe(a, i)) for a in sc["per_arm"]}
    assert max(over.values()) > 0, f"{suite}: the unsafe-claim counter is dead: {over}"


@pytest.mark.parametrize("suite", SUITES)
def test_design_json_is_frozen_and_carries_a_seed_commitment(fm_path, suite):
    from fm_run import load_suite

    spec = load_suite(suite)
    design = json.loads((FM / spec.design_json).read_text())
    assert design["frozen_before_protected_outcome_access"] is True
    assert design["authority"]["grants_scientific_truth"] is False
    assert len(design["seed_commitment"]["protected_seed_sha256"]) == 64
    assert design["sizes"]["protected_total"] >= design["sizes"][
        "minimum_tasks_required_by_issue_50_C1"
    ]
    assert design["primary_comparator"] == spec.strongest_parent_arm


@pytest.mark.parametrize("suite", SUITES)
def test_protected_stage_refuses_without_authorization(fm_path, suite):
    """The single-run invariant: no authorization file, no protected run."""
    assert not (FM / "PROTECTED_RUN_AUTHORIZATION.json").exists(), (
        "a live authorization file must not be committed; archive it after the run"
    )
    proc = subprocess.run(
        [sys.executable, str(FM / "fm_run.py"), suite, "protected"],
        capture_output=True,
        text=True,
        cwd=str(FM),
    )
    assert proc.returncode == 3, proc.stderr
    assert "REFUSED" in proc.stderr


@pytest.mark.parametrize("suite", SUITES)
def test_selftest_stage_passes(fm_path, suite, tmp_path):
    proc = subprocess.run(
        [sys.executable, str(FM / "fm_run.py"), suite, "selftest", "--out", str(tmp_path)],
        capture_output=True,
        text=True,
        cwd=str(FM),
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = json.loads((tmp_path / f"{suite}_SELFTEST_REPORT.json").read_text())
    assert report["passed"] is True
    assert report["oracle_agreement"]["n_disagreements"] == 0


@pytest.mark.parametrize("suite", SUITES)
def test_development_split_is_deterministic(fm_path, suite, tmp_path):
    from fm_core import canonical_json
    from fm_run import load_suite, run_instances

    spec = load_suite(suite)
    out = []
    for _ in range(2):
        pairs, rejects = spec.generate("dev", f"{suite}-DEV-20260902", {f: 2 for f in spec.families})
        res, cus = run_instances(spec, pairs, "T", "seed")
        res.pop("_timing_wall_ns")
        out.append(canonical_json(res) + canonical_json(cus) + canonical_json(rejects))
    assert out[0] == out[1], "the generator and arms must be byte-deterministic"

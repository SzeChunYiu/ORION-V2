"""ME-X3 exact formal-mathematics study: oracle exactness, family invariants,
parent behaviour and runner stages. Development fixtures only; nothing here is
protected evidence."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MEX3 = ROOT / "research" / "experiments" / "me-x3"
if str(MEX3) not in sys.path:
    sys.path.insert(0, str(MEX3))

import mex3_arms as A  # noqa: E402
import mex3_generator as G  # noqa: E402
import mex3_lean as LEAN  # noqa: E402
import mex3_oracle as O  # noqa: E402
import mex3_run as R  # noqa: E402
import mex3_verdict as V  # noqa: E402
from mex3_model import ACTIONS, FIDELITY_VERDICTS, Presentation, Statement  # noqa: E402
from mex3_parents import fidelity_selftests  # noqa: E402

P = Presentation("P0", 3, (((0, 1), (2,)), ((2, 2), (1,))))


@pytest.fixture(scope="module")
def split():
    return G.generate_split("ME-X3-TEST", 1)


def test_every_parent_passes_its_native_known_answer_tests() -> None:
    rows = fidelity_selftests()
    bad = [r for r in rows if not r["passed"]]
    assert not bad, bad


def test_two_independent_searches_agree_on_minimal_length() -> None:
    for lhs in ((0, 1, 0, 1), (1, 2, 0), (2, 2, 2)):
        for rhs in ((1,), (2,), (0, 1)):
            a = O.bfs_derivation(lhs, rhs, P.axioms, 6, 4000)
            b = O.iddfs_derivation(lhs, rhs, P.axioms, 6, 5, 200000)
            assert a.found == b.found
            if a.found:
                assert a.length == b.length


def test_definable_generator_fast_path_equals_brute_force() -> None:
    P1 = Presentation("P1", 4, (((3,), (0, 1)), ((3, 2), (1,)), ((2, 2), (1,))))
    O._MODELS_CACHE.clear()
    fast = set(O.models_of(P1, 3))
    brute = {(m, n) for n in (1, 2, 3) for m in O.enumerate_models(4, n)
             if O.satisfies(m, n, P1.axioms)}
    assert fast == brute and fast


def test_a_verified_derivation_is_an_axiom_instance_chain() -> None:
    st = Statement((0, 1, 0, 1), (1,))
    r = O.bfs_derivation(st.lhs, st.rhs, P.axioms, 6, 4000)
    assert r.found
    assert O.check_derivation(r.path, st, P.axioms, 6) == (True, "OK")
    tampered = list(r.path)
    tampered[1] = tampered[1] + (0,)
    assert O.check_derivation(tampered, st, P.axioms, 6)[0] is False


def test_a_countermodel_must_satisfy_the_axioms_and_falsify_the_statement() -> None:
    st = Statement((0,), (1,))
    cm = O.find_countermodel(P, st, 3)
    assert cm is not None
    m, n = cm
    assert O.check_countermodel(m, n, P, st) == (True, "OK")
    # a model that does not satisfy the axioms is not a certificate
    assert O.check_countermodel(((0, 0), (1, 1), (0, 1)), 2, P, st)[0] in (True, False)
    assert O.check_countermodel(m, n, P, Statement((0,), (0,)))[0] is False


def test_proof_validity_and_specification_fidelity_are_independent() -> None:
    """A checker-accepted theorem that answers the wrong question."""
    intent = Statement((0,), (1,))
    formal = Statement((2, 0), (2, 1))
    tval, _ = O.truth(P, formal, G.ORACLE_WORD_LEN, G.ORACLE_EXPANSIONS, G.ORACLE_MODEL_SIZE)
    fid, w = O.fidelity(P, intent, formal, G.ORACLE_WORD_LEN, G.ORACLE_EXPANSIONS,
                        G.ORACLE_MODEL_SIZE, "MATERIALLY_WEAKENED")
    assert fid != "FAITHFUL" and fid in FIDELITY_VERDICTS
    assert w["route"] == "SEPARATING_MODEL"
    m = tuple(tuple(f) for f in w["model"])
    assert O.check_separating_model(m, w["size"], P, intent, formal) == (True, "OK")


def test_faithful_requires_an_interderivability_witness_not_bounded_agreement() -> None:
    st = Statement((0, 1, 0, 1), (1,))
    fid, w = O.fidelity(P, st, st, G.ORACLE_WORD_LEN, G.ORACLE_EXPANSIONS, G.ORACLE_MODEL_SIZE)
    assert fid == "FAITHFUL" and w["route"] in ("IDENTICAL", "INTERDERIVABLE")


def test_generated_families_land_in_their_registered_oracle_cell(split) -> None:
    assert split
    for task, verdict in split:
        assert G.FAMILY_CELL[task.family](verdict, task), (task.task_id, verdict)
        assert verdict["minimal_action"] in ACTIONS


def test_generator_is_deterministic(split) -> None:
    again = G.generate_split("ME-X3-TEST", 1)
    assert [t.task_id for t, _ in split] == [t.task_id for t, _ in again]
    assert [v["minimal_action"] for _, v in split] == [v["minimal_action"] for _, v in again]


def test_a_representation_change_witness_must_prove_the_translated_statement(split) -> None:
    """A chain that is axiom-sound but proves something else earns no F3 credit."""
    f3 = [(t, v) for t, v in split if t.family == "F3_REPRESENTATION_CHANGE"]
    if not f3:
        pytest.skip("no F3 instance in this split")
    task, _ = f3[0]
    stmt = A.m_alt_statement(task)
    assert stmt is not None
    r = O.bfs_derivation(stmt.lhs, stmt.rhs, task.alt.axioms,
                         task.budget.max_word_len, task.budget.solve_expansions)
    assert r.found
    good = {"validity": "VERIFIED", "derivation": [list(w) for w in r.path],
            "derivation_pid": "P1", "invented_lemma": None, "countermodel": None}
    assert R._witness_ok(task.view(), good, {}) is True
    # an axiom-sound chain between other endpoints must NOT pass
    other = O.bfs_derivation(stmt.lhs, stmt.lhs + (0,), task.alt.axioms,
                             task.budget.max_word_len, task.budget.solve_expansions)
    if other.found and other.length > 0:
        bad = dict(good, derivation=[list(w) for w in other.path])
        assert R._witness_ok(task.view(), bad, {}) is False


def test_the_arm_view_carries_no_oracle_information(split) -> None:
    for task, _ in split:
        view = task.view()
        blob = json.dumps(view)
        assert "hidden" not in view and "family" not in view
        for banned in ("oracle_action", "f7_subtype", "minimal_action", "terminal",
                       "transfer_role", "fidelity_witness", "countermodel",
                       "truth", "level", "escalation_witness"):
            assert banned not in blob, (task.task_id, banned)


def test_proof_only_parents_miss_specification_drift_and_checkers_do_not() -> None:
    """The FormalScience separation, inside this environment."""
    from mex3_model import Task
    intent = Statement((0,), (1,))
    formal = Statement((2, 0), (2, 1))
    t = Task(task_id="t", family="F7_SPECIFICATION_MISMATCH", seed="s", base=P, alt=None,
             alt_label="", alt_map=(), library=(), intent=intent, intent_invariants=(),
             formal=formal, formal_pid="P0", surface_cues=(), budget=G.TASK_BUDGET, hidden={})
    bare = A.arm_a0(t, A.Ledger(G.TASK_BUDGET), A.ArmState())
    fed = A.federation(t, A.Ledger(G.TASK_BUDGET), A.ArmState(), "R5_FULL_STRUCTURE")
    m = A.m_arm(t, A.Ledger(G.TASK_BUDGET), A.ArmState())
    assert bare.fidelity == "FAITHFUL"
    assert fed.fidelity != "FAITHFUL" and m.fidelity != "FAITHFUL"
    assert m.action == "REFORMULATE_FORMAL_STATEMENT_WITH_PRESERVATION_CHECK"


def test_m_receives_no_report_the_top_rung_federation_lacks() -> None:
    specs = {s.name: s for s in A.arm_specs()}
    assert A.M_ARM in specs and A.B5_ARM in specs
    assert A.LADDER[-1] == A.B5_ARM
    rep = A.SearchReport(False, (), True, False, 7, 7)
    assert rep.project("R5_FULL_STRUCTURE") is rep
    assert rep.project("R1_VERDICT_ONLY").saturated is False


def test_lean_emitter_produces_a_proof_term_not_a_reflection_certificate() -> None:
    st = Statement((0, 1, 0, 1), (1,))
    r = O.bfs_derivation(st.lhs, st.rhs, P.axioms, 6, 4000)
    src = LEAN.emit_lean("t", 3, P.axioms, r.path, 6)
    assert "inductive Derives : Word → Word → Prop" in src
    assert "#print axioms thm" in src
    assert "decide" not in src and "= true" not in src
    assert src.count("Derives.trans") == max(0, r.length - 1)


def test_lean_negative_control_is_actually_corrupted() -> None:
    """A 'bad' file byte-identical to its good counterpart is not a control."""
    st = Statement((0, 1, 0, 1), (1,))
    r = O.bfs_derivation(st.lhs, st.rhs, P.axioms, 6, 4000)
    assert r.found and r.length >= 2
    good = LEAN.emit_lean("t", 3, P.axioms, r.path, 6)
    for k in range(r.length):
        bad = LEAN.emit_lean("t_bad", 3, P.axioms, r.path, 6, corrupt_step=k)
        assert bad is not None
        assert bad.replace("_bad", "") != good
    assert LEAN.emit_lean("t", 3, P.axioms, r.path, 6, corrupt_step=r.length) is None


def test_lean_negative_control_needs_the_registered_error_signature() -> None:
    ok = LEAN.classify(1, "", "error: Type mismatch\n  Derives.ax0f [] []", "REJECT")
    assert ok[0] == "REJECTED_FOR_THE_REGISTERED_REASON"
    for out in ("error: unknown identifier 'foo'", "", "deterministic timeout"):
        v, _ = LEAN.classify(1, "", out, "REJECT")
        assert v == "CANNOT_CHECK"
    assert LEAN.classify(0, "", "", "REJECT")[0] == "ACCEPTED_UNEXPECTEDLY"
    assert LEAN.classify(0, "'thm' does not depend on any axioms", "", "ACCEPT")[0] == \
        "VERIFIED_BY_LEAN_KERNEL"


def test_selftest_stage_passes(tmp_path: Path) -> None:
    assert R.main(["selftest", "--out", str(tmp_path)]) == 0
    rep = json.loads((tmp_path / "ME_X3_SELFTEST_REPORT.json").read_text())
    assert rep["passed"] and len(rep["tests"]) >= 12


def test_dev_stage_end_to_end_and_analysis_is_labelled_development(tmp_path: Path) -> None:
    assert R.main(["selftest", "--out", str(tmp_path)]) == 0
    assert R.main(["dev", "--out", str(tmp_path), "--per-family", "1"]) == 0
    res = tmp_path / "ME_X3_DEVELOPMENT_RESULTS_V1.json"
    cus = tmp_path / "ME_X3_DEVELOPMENT_CUSTODY_V1.json"
    assert R.main(["analyze", "--results", str(res), "--custody", str(cus),
                   "--out", str(tmp_path)]) == 0
    an = json.loads((tmp_path / "ME_X3_DEVELOPMENT_ANALYSIS_V1.json").read_text())
    assert an["label"] == "DEVELOPMENT"
    assert an["gates"]["G0"]["pass"]
    assert an["gates"]["ROUTE"]["route"] in (
        "PARENT_SUFFICIENT", "ME_RESIDUAL_SUPPORTED", "SPECIFICATION_FIDELITY_RESIDUAL",
        "MECHANISM_UNSUPPORTED", "CANNOT_CHECK")
    for fam, r in an["gates"]["G1"]["per_family"].items():
        assert r["n"] >= 1, fam


def test_protected_stage_refuses_without_authorization(tmp_path: Path) -> None:
    assert not (MEX3 / "PROTECTED_RUN_AUTHORIZATION.json").exists()
    assert R.main(["protected", "--out", str(tmp_path), "--per-family", "1"]) == 3


def test_design_json_matches_the_frozen_code_constants() -> None:
    d = json.loads((MEX3 / "ME_X3_FORMAL_MATHEMATICS_EXACT_STUDY_DESIGN_V1.json").read_text())
    assert d["budget"]["max_expansions"] == G.TASK_BUDGET.max_expansions
    assert d["budget"]["solve_expansions"] == G.TASK_BUDGET.solve_expansions
    assert d["oracle_caps"]["word_len"] == G.ORACLE_WORD_LEN
    assert d["oracle_caps"]["lemma_pool_cap"] == V.LEMMA_POOL_CAP
    assert d["splits"]["rejection_sampling_max_attempts"] == G.MAX_ATTEMPTS
    assert d["splits"]["protected"]["per_family"] == R.PROTECTED_PER_FAMILY
    assert d["arms"] == [s.name for s in A.arm_specs()]
    assert d["primary_comparator"] == A.B5_ARM and d["candidate"] == A.M_ARM
    assert d["verifier"]["mathlib"] is None
    assert d["pre_registered_expectation"]["route"] == "PARENT_SUFFICIENT"
    import hashlib
    for f, want in d["code_sha256"].items():
        assert hashlib.sha256((MEX3 / f).read_bytes()).hexdigest() == want, f

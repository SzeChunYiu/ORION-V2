#!/usr/bin/env python3
"""ME-X3 parent-fidelity selftests.

Each parent arm must reproduce the behaviour its source system is known for on a
hand-authored case where that behaviour is unambiguous.  A federation whose
members do not actually behave like their parents is a strawman, and the study
would be worthless; these tests are a precondition of every stage (G0).
"""
from __future__ import annotations

import itertools

from mex3_arms import Ledger, ArmState, arm_a0, arm_a1, arm_a3, arm_a4, federation, m_arm
from mex3_model import Budget, Presentation, Statement, Task
from mex3_oracle import (
    bfs_derivation, check_countermodel, check_derivation, enumerate_models, iddfs_derivation,
    models_of, satisfies,
)

B = Budget(max_word_len=6, max_expansions=1800, solve_expansions=250,
           max_model_size=3, max_model_checks=2000, max_lemma_candidates=40)
P = Presentation("P0", 3, (((0, 1), (2,)), ((2, 2), (1,))))


def _task(tid, intent, formal, library=(), alt=None, alt_label="", hidden=None,
          formal_pid="P0"):
    return Task(task_id=tid, family="SELFTEST", seed="selftest", base=P, alt=alt,
                alt_label=alt_label, alt_map=(), library=tuple(library), intent=intent,
                intent_invariants=(), formal=formal, formal_pid=formal_pid,
                surface_cues=(), budget=B, hidden=hidden or {})


def fidelity_selftests() -> list[dict]:
    out: list[dict] = []

    def rec(name, ok, detail=""):
        out.append({"test": name, "passed": bool(ok), "detail": detail})

    # --- parent behaviours ----------------------------------------------------
    st = Statement((0, 1, 0, 1), (1,))
    t = _task("st-direct", st, st)
    a = arm_a0(t, Ledger(B), ArmState())
    rec("A0_proves_a_short_target", a.validity == "VERIFIED" and a.action ==
        "CONTINUE_DIRECT_PROOF_SEARCH", a.validity)
    ok, why = check_derivation(a.derivation, st, P.axioms, B.max_word_len)
    rec("A0_derivation_is_axiom_sound", ok, why)

    false_st = Statement((0,), (1,))
    t = _task("st-false", false_st, false_st)
    a3 = arm_a3(t, Ledger(B), ArmState())
    rec("A3_discovers_the_answer_before_proving",
        a3.validity == "REFUTED" and a3.countermodel is not None, a3.validity)
    if a3.countermodel:
        m = tuple(tuple(f) for f in a3.countermodel["model"])
        ok, why = check_countermodel(m, a3.countermodel["size"], P, false_st)
        rec("A3_countermodel_is_a_model_of_the_axioms", ok, why)
    a0 = arm_a0(t, Ledger(B), ArmState())
    rec("A0_cannot_settle_a_false_statement", a0.validity == "UNVERIFIED", a0.validity)

    # A4 must find a lemma where A1's library cannot help.
    hard = Statement((0, 1, 0, 1, 0, 1), (1, 1))
    t_lib = _task("st-lib", hard, hard, library=(((0, 1), (2,)),))
    rec("A1_retrieval_uses_the_library",
        arm_a1(t_lib, Ledger(B), ArmState()).action in
        ("CONTINUE_DIRECT_PROOF_SEARCH", "RETRIEVE_EXISTING_LEMMA"), "")

    # --- proof-validity / specification-fidelity separation -------------------
    intent = Statement((0,), (1,))                 # not derivable
    formal = Statement((2, 0), (2, 1))             # a different, provable question
    t = _task("st-drift", intent, formal)
    fed = federation(t, Ledger(B), ArmState(), "R5_FULL_STRUCTURE")
    rec("federation_runs_a_specification_check", fed.fidelity != "FAITHFUL" or
        fed.validity != "VERIFIED", f"{fed.validity}/{fed.fidelity}")
    bare = arm_a0(t, Ledger(B), ArmState())
    rec("proof_only_parent_reports_alignment_it_never_checked",
        bare.fidelity == "FAITHFUL", bare.fidelity)

    # --- oracle self-agreement (G0b) ------------------------------------------
    agree = True; detail = ""
    for lhs in itertools.product(range(3), repeat=3):
        for rhs in ((1,), (2,), (0, 1)):
            r1 = bfs_derivation(lhs, rhs, P.axioms, 6, 4000)
            r2 = iddfs_derivation(lhs, rhs, P.axioms, 6, 5, 200000)
            if r1.found != r2.found or (r1.found and r2.found and r1.length != r2.length):
                agree = False; detail = f"{lhs}->{rhs}: bfs={r1.found}/{r1.length} iddfs={r2.found}/{r2.length}"
                break
    rec("two_independent_searches_agree_on_minimal_length", agree, detail)

    # definable-generator fast path == brute-force model enumeration
    P1 = Presentation("P1", 4, (((3,), (0, 1)), ((3, 2), (1,)), ((2, 2), (1,))))
    fast = set(models_of(P1, 3))
    brute = {(m, n) for n in (1, 2, 3) for m in enumerate_models(4, n)
             if satisfies(m, n, P1.axioms)}
    rec("model_enumeration_fast_path_is_exact", fast == brute,
        f"{len(fast)} vs {len(brute)}")

    # --- null calibration: on a trivial identity nobody may escalate ----------
    triv = Statement((0, 1), (0, 1))
    t = _task("st-triv", triv, triv)
    for name, fn in (("B5", lambda: federation(t, Ledger(B), ArmState(), "R5_FULL_STRUCTURE")),
                     ("M", lambda: m_arm(t, Ledger(B), ArmState()))):
        a = fn()
        rec(f"null_calibration_{name}_does_not_escalate_on_an_identity",
            a.action == "CONTINUE_DIRECT_PROOF_SEARCH" and a.validity == "VERIFIED",
            f"{a.action}/{a.validity}")
    return out

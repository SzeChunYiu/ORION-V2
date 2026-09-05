from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import itertools
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "research/machine-epistemics-theory"))
from semantic_codec_v1 import codecs as c
from semantic_codec_v1 import renderer as r
from semantic_codec_v1 import semantics as s


def registry():
    return s.Registry((s.Sort("person", ("alice", "bob")),),
                      (s.Predicate("red", ("person",)), s.Predicate("likes", ("person", "person"))), "registry_v1")


def relation_registry():
    return s.Registry((s.Sort("person", ("alice", "bob")),),
                      (s.Predicate("likes", ("person", "person")),), "relation_v1")


A = s.Term("const", "alice")
B = s.Term("const", "bob")
V0 = s.Term("var", 0)
V1 = s.Term("var", 1)


def fixtures():
    base = [s.atom("red", a) for a in (A, B)] + [s.atom("likes", a, b) for a, b in itertools.product((A, B), repeat=2)]
    out = base + [s.negate(f) for f in base] + [s.conjunction(a, b) for a, b in itertools.product(base, repeat=2)]
    out += [s.quantify(q, "person", s.atom("red", V0)) for q in ("all", "some")]
    out += [s.quantify(q, "person", s.quantify(p, "person", s.atom("likes", x, y)))
            for q, p in itertools.product(("all", "some"), repeat=2)
            for x, y in ((V0, V1), (V1, V0))]
    return tuple(out)


def test_all_registered_constructed_formulas_roundtrip_both_independent_codecs():
    reg = registry()
    for formula in fixtures():
        sentence = c.decode_sentence(c.encode_sentence(formula, reg), reg)
        functional = c.decode_functional(c.encode_functional(formula, reg), reg)
        assert sentence.status == functional.status == "UNIQUE"
        assert sentence.candidates == functional.candidates == (formula,)
        intended = s.meaning(formula, reg)
        assert s.meaning(sentence.candidates[0], reg) == intended
        assert s.meaning(functional.candidates[0], reg).seed == intended.seed


def test_decoders_work_without_encoder_lookup_or_callbacks(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("decoder called encoder")
    monkeypatch.setattr(c, "encode_sentence", forbidden)
    monkeypatch.setattr(c, "encode_functional", forbidden)
    reg = registry()
    want = s.quantify("all", "person", s.negate(s.atom("red", V0)))
    assert c.decode_sentence("every person : ( it is false that ( @0 is red ) )", reg).candidates == (want,)
    assert c.decode_functional("all[person]{neg{red(@0)}}", reg).candidates == (want,)


def test_independent_relation_matrix_oracle_checks_quantifier_order_all_worlds():
    reg = relation_registry()
    ae = s.quantify("all", "person", s.quantify("some", "person", s.atom("likes", V1, V0)))
    ea = s.quantify("some", "person", s.quantify("all", "person", s.atom("likes", V0, V1)))
    actual_ae, actual_ea = s.meaning(ae, reg), s.meaning(ea, reg)
    # Direct 2x2 Boolean matrices, separately specified from the AST evaluator.
    oracle_ae, oracle_ea = [], []
    for mask in range(16):
        matrix = [[bool(mask & (1 << (2*x+y))) for y in range(2)] for x in range(2)]
        oracle_ae.append(all(any(row) for row in matrix))
        oracle_ea.append(any(all(matrix[x][y] for x in range(2)) for y in range(2)))
    assert actual_ae.truth_vector == tuple(oracle_ae)
    assert actual_ea.truth_vector == tuple(oracle_ea)
    assert actual_ae != actual_ea
    assert actual_ae.truth_vector[9] and not actual_ea.truth_vector[9]


def test_negation_scope_and_quantifier_duality_have_distinct_known_answers():
    reg = registry()
    all_red = s.quantify("all", "person", s.atom("red", V0))
    all_not = s.quantify("all", "person", s.negate(s.atom("red", V0)))
    some_not = s.quantify("some", "person", s.negate(s.atom("red", V0)))
    assert s.meaning(s.negate(all_red), reg) != s.meaning(all_not, reg)
    assert s.meaning(s.negate(all_red), reg) == s.meaning(some_not, reg)


def test_empty_sort_quantification_is_deliberately_vacuous():
    reg = s.Registry((s.Sort("person", ()),), (s.Predicate("red", ("person",)),), "empty_v1")
    assert s.meaning(s.quantify("all", "person", s.atom("red", V0)), reg).truth_vector == (True,)
    assert s.meaning(s.quantify("some", "person", s.atom("red", V0)), reg).truth_vector == (False,)


def test_semantic_quotient_is_broader_than_structural_identity():
    reg = registry()
    original = s.atom("red", A)
    equivalent = s.negate(s.negate(original))
    assert s.structural_digest(original, reg) != s.structural_digest(equivalent, reg)
    assert s.meaning(original, reg).seed == s.meaning(equivalent, reg).seed
    # The same truth vector from another registered epoch is not interchangeable.
    changed = replace(reg, epoch="registry_v2")
    assert s.meaning(original, reg).truth_vector == s.meaning(original, changed).truth_vector
    assert s.meaning(original, reg).seed != s.meaning(original, changed).seed


def test_ambiguity_is_preserved_and_budget_exhaustion_never_selects_a_winner():
    reg = s.Registry((s.Sort("person", ("alice",)),),
        (s.Predicate("riverbank", ("person",), ("bank",)), s.Predicate("financialbank", ("person",), ("bank",))), "bank_v1")
    result = c.decode_sentence("alice is bank", reg)
    assert result.status == "AMBIGUOUS" and len(result.candidates) == 2
    assert c.decode_sentence("alice is bank", reg, max_candidates=1).status == "CANNOT_CHECK"
    assert c.decode_functional("riverbank(alice)", reg).status == "UNIQUE"
    assert c.decode_functional("bank(alice)", reg).status == "CANNOT_CHECK"


def test_gate_never_selects_the_reading_that_happens_to_match_the_plan():
    reg = s.Registry((s.Sort("person", ("alice",)),),
        (s.Predicate("riverbank", ("person",), ("bank",)), s.Predicate("financialbank", ("person",), ("bank",))), "bank_v1")
    intended = s.atom("riverbank", A)
    view = r.RenderView(s.registry_digest(reg), "evidence_v1", (r.ShownClaim(intended, "ASSERT", ("e1",)),))
    evidence = r.Support("e1", s.meaning(intended, reg).seed, "LIVE", "world", True)
    assert check("ASSERT[e1] :: alice is bank", reg, view, (evidence,)).status == "CANNOT_CHECK"


@pytest.mark.parametrize("formula", [
    s.atom("red", V0), s.atom("red", s.Term("var", True)),
    s.atom("red", s.Term("const", "ghost")), s.atom("likes", A),
    s.Formula("not", "hidden", children=(s.atom("red", A),)),
    s.Formula("atom", "red", [A]), s.Formula("and", children=(s.atom("red", A),)),
])
def test_malformed_unbound_or_mutable_formulas_are_rejected(formula):
    with pytest.raises(s.CannotCheck):
        s.meaning(formula, registry())


def test_nested_binder_sorts_are_checked_at_the_actual_de_bruijn_depth():
    reg = s.Registry((s.Sort("person", ("alice",)), s.Sort("object", ("book",))),
                     (s.Predicate("owns", ("person", "object")),), "typed_v1")
    good = s.quantify("all", "person", s.quantify("some", "object", s.atom("owns", V1, V0)))
    bad = s.quantify("all", "person", s.quantify("some", "object", s.atom("owns", V0, V1)))
    for encode, decode in ((c.encode_sentence, c.decode_sentence), (c.encode_functional, c.decode_functional)):
        assert decode(encode(good, reg), reg).candidates == (good,)
    with pytest.raises(s.CannotCheck, match="sort"):
        s.meaning(bad, reg)
    assert c.decode_sentence("every person : ( some object : ( @0 owns @1 ) )", reg).status == "CANNOT_CHECK"


@pytest.mark.parametrize("text", ["alice is red extra", "alice is red!", "alice is red\x00", "alice is red\nASSERT", "every person : ( @1 is red )", "alice is unknown"])
def test_sentence_decoder_never_ignores_unrecognized_surface(text):
    assert c.decode_sentence(text, registry()).status == "CANNOT_CHECK"


@pytest.mark.parametrize("text", ["red(alice)extra", "red(alice)!", "red(alice)\x00", "all[person]{red(@1)}", "red(alice,bob)"])
def test_functional_decoder_never_ignores_unrecognized_surface(text):
    assert c.decode_functional(text, registry()).status == "CANNOT_CHECK"


@pytest.mark.parametrize("kwargs", [{"max_worlds": 63}, {"max_worlds": True}, {"max_steps": 1}, {"max_steps": False}])
def test_partial_truth_tables_never_yield_a_semantic_certificate(kwargs):
    with pytest.raises(s.CannotCheck):
        s.meaning(s.atom("red", A), registry(), **kwargs)


def gate_fixture(marker="ASSERT", status="LIVE"):
    reg = registry()
    formula = s.atom("red", A)
    claim = r.ShownClaim(formula, marker, ("e1",))
    view = r.RenderView(s.registry_digest(reg), "evidence_v1", (claim,))
    support = r.Support("e1", s.meaning(formula, reg).seed, status, "world", True)
    return reg, view, support


def check(text, reg, view, supports, **kwargs):
    return r.commitment_eligibility(text, view, reg, supports, current_epoch=kwargs.pop("current_epoch", "evidence_v1"), scope="world", **kwargs)


@pytest.mark.parametrize("codec", ["sentence", "functional"])
def test_actual_text_gate_accepts_honest_renderer_and_equivalent_finite_paraphrase(codec):
    reg, view, support = gate_fixture()
    text = r.render(view, reg, codec=codec)
    assert check(text, reg, view, (support,), codec=codec).status == "ELIGIBLE_FOR_EXTERNAL_COMMIT"
    alt = replace(view, claims=(replace(view.claims[0], formula=s.negate(s.negate(view.claims[0].formula))),))
    assert check(r.render(alt, reg, codec=codec), reg, view, (support,), codec=codec).status == "ELIGIBLE_FOR_EXTERNAL_COMMIT"


@pytest.mark.parametrize("mutant", ["negation", "entity", "extra", "marker", "citation"])
def test_actual_surface_mutants_cannot_reuse_honest_metadata(mutant):
    reg, view, support = gate_fixture()
    text = r.render(view, reg)
    bad = {
        "negation": "ASSERT[e1] :: it is false that ( alice is red )",
        "entity": text.replace("alice", "bob"),
        "extra": text + "\n" + text,
        "marker": text.replace("ASSERT", "HEDGE"),
        "citation": text.replace("e1", "e2"),
    }[mutant]
    assert check(bad, reg, view, (support,)).status == "REFUSED"


def test_actual_quantifier_swap_cannot_reuse_honest_plan():
    reg = relation_registry()
    ae = s.quantify("all", "person", s.quantify("some", "person", s.atom("likes", V1, V0)))
    ea = s.quantify("some", "person", s.quantify("all", "person", s.atom("likes", V0, V1)))
    view = r.RenderView(s.registry_digest(reg), "evidence_v1", (r.ShownClaim(ae, "ASSERT", ("e1",)),))
    forged = replace(view, claims=(replace(view.claims[0], formula=ea),))
    support = r.Support("e1", s.meaning(ae, reg).seed, "LIVE", "world", True)
    assert check(r.render(forged, reg), reg, view, (support,)).status == "REFUSED"


@pytest.mark.parametrize("change", ["revoked", "unknown", "speaker", "scope", "meaning"])
def test_current_support_is_checked_separately_from_semantic_fidelity(change):
    reg, view, support = gate_fixture()
    bad = {"revoked": replace(support, status="DEAD"), "unknown": replace(support, status="UNKNOWN"),
           "speaker": replace(support, world_authority=False), "scope": replace(support, scope="conversation"),
           "meaning": replace(support, semantic_seed=s.meaning(s.atom("red", B), reg).seed)}[change]
    assert check(r.render(view, reg), reg, view, (bad,)).status == "REFUSED"


def test_stale_epoch_missing_evidence_and_partial_evaluation_fail_closed():
    reg, view, support = gate_fixture()
    text = r.render(view, reg)
    assert check(text, reg, view, (support,), current_epoch="evidence_v2").status == "CANNOT_CHECK"
    assert check(text, reg, view, ()).status == "CANNOT_CHECK"
    assert check(text, reg, view, (support,), max_worlds=1).status == "CANNOT_CHECK"
    assert check(text, reg, view, (support, support)).status == "CANNOT_CHECK"


def test_protected_semantic_content_refused_even_when_in_the_plan():
    reg, view, support = gate_fixture()
    assert check(r.render(view, reg), reg, view, (support,), protected_seeds=(support.semantic_seed,)).status == "REFUSED"


def test_uncertainty_and_withholding_do_not_mint_world_authority():
    reg, view, support = gate_fixture("HEDGE", "UNKNOWN")
    assert check(r.render(view, reg), reg, view, (support,)).status == "ELIGIBLE_FOR_EXTERNAL_COMMIT"
    assert check(r.render(view, reg).replace("HEDGE", "ASSERT"), reg, view, (support,)).status == "REFUSED"
    assert check(r.render(view, reg), reg, view, (replace(support, status="DEAD"),)).status == "REFUSED"
    withheld = replace(view, claims=(replace(view.claims[0], marker="WITHHOLD"),))
    assert r.render(withheld, reg) == ""
    assert check("", reg, withheld, ()).status == "ELIGIBLE_FOR_EXTERNAL_COMMIT"


def test_renderer_inputs_are_deeply_immutable_and_render_has_no_store_effect():
    reg, view, support = gate_fixture()
    external = {"secret": "hidden gold", "events": []}
    before = repr(external)
    assert "hidden gold" not in r.render(view, reg)
    assert repr(external) == before
    for obj, attr, value in ((view, "claims", ()), (view.claims[0], "marker", "ASSERT"), (reg.sorts[0], "members", ())):
        with pytest.raises(FrozenInstanceError):
            setattr(obj, attr, value)
    with pytest.raises(s.CannotCheck):
        r.render(replace(view, claims=list(view.claims)), reg)
    with pytest.raises(s.CannotCheck):
        r.render(view, replace(reg, sorts=list(reg.sorts)))


def test_open_registry_cannot_certify_any_codec_or_meaning():
    reg = replace(registry(), closed=False)
    assert c.decode_sentence("alice is red", reg).status == "CANNOT_CHECK"
    assert c.decode_functional("red(alice)", reg).status == "CANNOT_CHECK"
    with pytest.raises(s.CannotCheck):
        s.meaning(s.atom("red", A), reg)


@pytest.mark.parametrize("alias", [[], {}, True, None])
def test_malformed_aliases_return_typed_cannot_check_before_hashing(alias):
    reg = s.Registry((s.Sort("person", ("alice",)),),
                     (s.Predicate("red", ("person",), (alias,)),), "bad_alias_v1")
    with pytest.raises(s.CannotCheck):
        s.validate_registry(reg)
    assert c.decode_sentence("alice is red", reg).status == "CANNOT_CHECK"
    assert c.decode_functional("red(alice)", reg).status == "CANNOT_CHECK"
    view = r.RenderView("0" * 64, "evidence_v1", ())
    assert check("", reg, view, ()).status == "CANNOT_CHECK"

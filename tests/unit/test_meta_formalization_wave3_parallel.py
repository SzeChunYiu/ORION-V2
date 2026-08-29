from dataclasses import replace

from orion_v2.meta_formalization import (
    ConservativeExtensionStatus,
    FiniteConsequenceTheory,
    FiniteGaloisConnection,
    FiniteLens,
    FiniteLogic,
    FinitePoset,
    LawStatus,
    SignatureMorphism,
    assess_abstract_transformer_soundness,
    assess_conservative_extension,
    assess_galois_connection,
    assess_lens_laws,
    assess_satisfaction_condition,
)


def test_institution_satisfaction_condition_commutes_under_renaming() -> None:
    source = FiniteLogic(
        "source", "sig:s", frozenset({"m0", "m1"}), frozenset({"p"}),
        frozenset({("m1", "p")}),
    )
    target = FiniteLogic(
        "target", "sig:t", frozenset({"n0", "n1"}), frozenset({"renamed-p"}),
        frozenset({("n1", "renamed-p")}),
    )
    morphism = SignatureMorphism(
        "rename", "sig:s", "sig:t", {"p": "renamed-p"}, {"n0": "m0", "n1": "m1"},
    )
    result = assess_satisfaction_condition(source, target, morphism)
    assert result.status is LawStatus.SATISFIED
    assert result.checked_cells == 2


def test_institution_check_detects_semantic_drift_despite_complete_maps() -> None:
    source = FiniteLogic(
        "source", "sig:s", frozenset({"m0", "m1"}), frozenset({"p"}),
        frozenset({("m1", "p")}),
    )
    target = FiniteLogic(
        "target", "sig:t", frozenset({"n0", "n1"}), frozenset({"q"}),
        frozenset({("n0", "q")}),
    )
    morphism = SignatureMorphism(
        "bad", "sig:s", "sig:t", {"p": "q"}, {"n0": "m0", "n1": "m1"},
    )
    result = assess_satisfaction_condition(source, target, morphism)
    assert result.status is LawStatus.VIOLATED
    assert len(result.violations) == 2


def _chain_poset(identifier: str, values: tuple[int, ...]) -> FinitePoset:
    return FinitePoset(
        identifier,
        frozenset(values),
        frozenset((left, right) for left in values for right in values if left <= right),
    )


def test_galois_connection_is_checked_by_adjunction_not_by_label_similarity() -> None:
    concrete = _chain_poset("concrete", (0, 1, 2))
    abstract = _chain_poset("abstract", (0, 1))
    connection = FiniteGaloisConnection(
        "gc", "concrete", "abstract", alpha={0: 0, 1: 1, 2: 1}, gamma={0: 0, 1: 2},
    )
    result = assess_galois_connection(concrete, abstract, connection)
    assert result.status is LawStatus.SATISFIED
    assert result.checked_cells == 6


def test_galois_connection_detects_wrong_concretization() -> None:
    concrete = _chain_poset("concrete", (0, 1, 2))
    abstract = _chain_poset("abstract", (0, 1))
    connection = FiniteGaloisConnection(
        "gc", "concrete", "abstract", alpha={0: 0, 1: 1, 2: 1}, gamma={0: 1, 1: 2},
    )
    assert assess_galois_connection(concrete, abstract, connection).status is LawStatus.VIOLATED


def test_abstract_transformer_soundness_allows_safe_overapproximation() -> None:
    concrete = _chain_poset("concrete", (0, 1, 2))
    abstract = _chain_poset("abstract", (0, 1))
    connection = FiniteGaloisConnection(
        "gc", "concrete", "abstract", alpha={0: 0, 1: 1, 2: 1}, gamma={0: 0, 1: 2},
    )
    result = assess_abstract_transformer_soundness(
        concrete, abstract, connection,
        concrete_transformer={0: 1, 1: 2, 2: 2},
        abstract_transformer={0: 1, 1: 1},
    )
    assert result.status is LawStatus.SATISFIED


def test_abstract_transformer_unsound_underestimate_is_rejected() -> None:
    concrete = _chain_poset("concrete", (0, 1, 2))
    abstract = _chain_poset("abstract", (0, 1))
    connection = FiniteGaloisConnection(
        "gc", "concrete", "abstract", alpha={0: 0, 1: 1, 2: 1}, gamma={0: 0, 1: 2},
    )
    result = assess_abstract_transformer_soundness(
        concrete, abstract, connection,
        concrete_transformer={0: 1, 1: 2, 2: 2},
        abstract_transformer={0: 0, 1: 1},
    )
    assert result.status is LawStatus.VIOLATED


def _lawful_boolean_lens() -> FiniteLens:
    sources = frozenset({(False, "x"), (False, "y"), (True, "x"), (True, "y")})
    views = frozenset({False, True})
    return FiniteLens(
        "first-coordinate",
        sources,
        views,
        {source: source[0] for source in sources},
        {(view, source): (view, source[1]) for view in views for source in sources},
    )


def test_lens_round_trip_laws_hold_for_information_preserving_update() -> None:
    assert assess_lens_laws(_lawful_boolean_lens()).status is LawStatus.SATISFIED


def test_lens_laws_detect_put_that_erases_complement_information() -> None:
    lens = _lawful_boolean_lens()
    bad_put = {
        (view, source): (view, "x")
        for view in lens.view_values
        for source in lens.source_values
    }
    result = assess_lens_laws(replace(lens, put_map=bad_put))
    assert result.status is LawStatus.VIOLATED
    assert any("GETPUT" in violation or "PUTPUT" in violation for violation in result.violations)


def test_conservative_extension_may_add_new_language_without_new_old_consequences() -> None:
    source = FiniteConsequenceTheory("source", frozenset({"p", "q"}), frozenset({"p"}))
    extension = FiniteConsequenceTheory(
        "extension", frozenset({"p", "q", "r"}), frozenset({"p", "r"}),
    )
    assert assess_conservative_extension(source, extension).status is ConservativeExtensionStatus.CONSERVATIVE


def test_nonconservative_extension_is_detected_by_old_language_reflection() -> None:
    source = FiniteConsequenceTheory("source", frozenset({"p", "q"}), frozenset({"p"}))
    extension = FiniteConsequenceTheory(
        "extension", frozenset({"p", "q", "r"}), frozenset({"p", "q", "r"}),
    )
    result = assess_conservative_extension(source, extension)
    assert result.status is ConservativeExtensionStatus.NONCONSERVATIVE_NEW_OLD_LANGUAGE_CONSEQUENCE
    assert result.new_old_language_consequences == ("q",)


def test_extension_that_loses_native_consequence_is_not_called_conservative() -> None:
    source = FiniteConsequenceTheory(
        "source", frozenset({"p", "q"}), frozenset({"p", "q"}),
    )
    extension = FiniteConsequenceTheory(
        "extension", frozenset({"p", "q", "r"}), frozenset({"p", "r"}),
    )
    assert (
        assess_conservative_extension(source, extension).status
        is ConservativeExtensionStatus.LOST_OLD_LANGUAGE_CONSEQUENCE
    )

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Hashable, Mapping

Element = Hashable


class LawStatus(str, Enum):
    SATISFIED = "SATISFIED"
    VIOLATED = "VIOLATED"
    CANNOT_CHECK = "CANNOT_CHECK"


class ConservativeExtensionStatus(str, Enum):
    CONSERVATIVE = "CONSERVATIVE"
    NONCONSERVATIVE_NEW_OLD_LANGUAGE_CONSEQUENCE = (
        "NONCONSERVATIVE_NEW_OLD_LANGUAGE_CONSEQUENCE"
    )
    LOST_OLD_LANGUAGE_CONSEQUENCE = "LOST_OLD_LANGUAGE_CONSEQUENCE"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class LawAssessment:
    status: LawStatus
    violations: tuple[str, ...]
    checked_cells: int
    authority_granted: bool = False
    novelty_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted or self.novelty_granted:
            raise ValueError("formal-law checks are non-authorizing")


@dataclass(frozen=True, slots=True)
class FiniteLogic:
    logic_id: str
    signature_id: str
    models: frozenset[Element]
    sentences: frozenset[Element]
    satisfaction: frozenset[tuple[Element, Element]]

    def __post_init__(self) -> None:
        if not self.logic_id.strip() or not self.signature_id.strip():
            raise ValueError("logic and signature ids must be non-blank")
        if not self.models or not self.sentences:
            raise ValueError("finite logics require models and sentences")
        if any(
            model not in self.models or sentence not in self.sentences
            for model, sentence in self.satisfaction
        ):
            raise ValueError("satisfaction cells must use declared models and sentences")


@dataclass(frozen=True, slots=True)
class SignatureMorphism:
    morphism_id: str
    source_signature_id: str
    target_signature_id: str
    sentence_map: Mapping[Element, Element]
    model_reduct_map: Mapping[Element, Element]

    def __post_init__(self) -> None:
        if any(
            not value.strip()
            for value in (
                self.morphism_id,
                self.source_signature_id,
                self.target_signature_id,
            )
        ):
            raise ValueError("morphism identities must be non-blank")


def assess_satisfaction_condition(
    source: FiniteLogic,
    target: FiniteLogic,
    morphism: SignatureMorphism,
) -> LawAssessment:
    if (
        morphism.source_signature_id != source.signature_id
        or morphism.target_signature_id != target.signature_id
    ):
        return LawAssessment(
            LawStatus.CANNOT_CHECK,
            ("signature identities do not match the morphism",),
            0,
        )
    if set(morphism.sentence_map) != set(source.sentences):
        return LawAssessment(
            LawStatus.CANNOT_CHECK,
            ("sentence translation is not total on the source signature",),
            0,
        )
    if set(morphism.model_reduct_map) != set(target.models):
        return LawAssessment(
            LawStatus.CANNOT_CHECK,
            ("model reduct is not total on target models",),
            0,
        )
    if any(sentence not in target.sentences for sentence in morphism.sentence_map.values()):
        return LawAssessment(
            LawStatus.CANNOT_CHECK,
            ("sentence translation reaches undeclared target sentences",),
            0,
        )
    if any(model not in source.models for model in morphism.model_reduct_map.values()):
        return LawAssessment(
            LawStatus.CANNOT_CHECK,
            ("model reduct reaches undeclared source models",),
            0,
        )

    violations: list[str] = []
    checked = 0
    for target_model in target.models:
        source_model = morphism.model_reduct_map[target_model]
        for source_sentence in source.sentences:
            target_sentence = morphism.sentence_map[source_sentence]
            target_truth = (target_model, target_sentence) in target.satisfaction
            source_truth = (source_model, source_sentence) in source.satisfaction
            checked += 1
            if target_truth != source_truth:
                violations.append(
                    f"satisfaction does not commute for model={target_model!r}, sentence={source_sentence!r}"
                )
    return LawAssessment(
        LawStatus.VIOLATED if violations else LawStatus.SATISFIED,
        tuple(violations),
        checked,
    )


@dataclass(frozen=True, slots=True)
class FinitePoset:
    poset_id: str
    elements: frozenset[Element]
    leq: frozenset[tuple[Element, Element]]

    def __post_init__(self) -> None:
        if not self.poset_id.strip() or not self.elements:
            raise ValueError("finite posets require identity and elements")
        if any(
            left not in self.elements or right not in self.elements
            for left, right in self.leq
        ):
            raise ValueError("order relation must use declared elements")
        if any((element, element) not in self.leq for element in self.elements):
            raise ValueError("order relation must be reflexive")
        for left, right in self.leq:
            if left != right and (right, left) in self.leq:
                raise ValueError("order relation must be antisymmetric")
        for left, middle in self.leq:
            for middle2, right in self.leq:
                if middle == middle2 and (left, right) not in self.leq:
                    raise ValueError("order relation must be transitive")

    def below(self, left: Element, right: Element) -> bool:
        return (left, right) in self.leq


@dataclass(frozen=True, slots=True)
class FiniteGaloisConnection:
    connection_id: str
    concrete_poset_id: str
    abstract_poset_id: str
    alpha: Mapping[Element, Element]
    gamma: Mapping[Element, Element]

    def __post_init__(self) -> None:
        if any(
            not value.strip()
            for value in (
                self.connection_id,
                self.concrete_poset_id,
                self.abstract_poset_id,
            )
        ):
            raise ValueError("Galois-connection identities must be non-blank")


def assess_galois_connection(
    concrete: FinitePoset,
    abstract: FinitePoset,
    connection: FiniteGaloisConnection,
) -> LawAssessment:
    if (
        connection.concrete_poset_id != concrete.poset_id
        or connection.abstract_poset_id != abstract.poset_id
    ):
        return LawAssessment(
            LawStatus.CANNOT_CHECK,
            ("poset identities do not match the connection",),
            0,
        )
    if set(connection.alpha) != set(concrete.elements) or set(connection.gamma) != set(
        abstract.elements
    ):
        return LawAssessment(
            LawStatus.CANNOT_CHECK,
            ("alpha and gamma must be total",),
            0,
        )
    if any(value not in abstract.elements for value in connection.alpha.values()):
        return LawAssessment(
            LawStatus.CANNOT_CHECK,
            ("alpha reaches an undeclared abstract element",),
            0,
        )
    if any(value not in concrete.elements for value in connection.gamma.values()):
        return LawAssessment(
            LawStatus.CANNOT_CHECK,
            ("gamma reaches an undeclared concrete element",),
            0,
        )
    violations: list[str] = []
    checked = 0
    for concrete_value in concrete.elements:
        for abstract_value in abstract.elements:
            left = abstract.below(connection.alpha[concrete_value], abstract_value)
            right = concrete.below(concrete_value, connection.gamma[abstract_value])
            checked += 1
            if left != right:
                violations.append(
                    f"adjunction fails for concrete={concrete_value!r}, abstract={abstract_value!r}"
                )
    return LawAssessment(
        LawStatus.VIOLATED if violations else LawStatus.SATISFIED,
        tuple(violations),
        checked,
    )


def assess_abstract_transformer_soundness(
    concrete: FinitePoset,
    abstract: FinitePoset,
    connection: FiniteGaloisConnection,
    concrete_transformer: Mapping[Element, Element],
    abstract_transformer: Mapping[Element, Element],
) -> LawAssessment:
    connection_assessment = assess_galois_connection(concrete, abstract, connection)
    if connection_assessment.status is not LawStatus.SATISFIED:
        return LawAssessment(
            LawStatus.CANNOT_CHECK,
            ("a valid Galois connection is required",),
            0,
        )
    if set(concrete_transformer) != set(concrete.elements) or set(
        abstract_transformer
    ) != set(abstract.elements):
        return LawAssessment(
            LawStatus.CANNOT_CHECK,
            ("transformers must be total",),
            0,
        )
    if any(value not in concrete.elements for value in concrete_transformer.values()):
        return LawAssessment(
            LawStatus.CANNOT_CHECK,
            ("concrete transformer leaves its domain",),
            0,
        )
    if any(value not in abstract.elements for value in abstract_transformer.values()):
        return LawAssessment(
            LawStatus.CANNOT_CHECK,
            ("abstract transformer leaves its domain",),
            0,
        )
    violations: list[str] = []
    checked = 0
    for concrete_value in concrete.elements:
        concrete_result = concrete_transformer[concrete_value]
        abstract_input = connection.alpha[concrete_value]
        abstract_result = abstract_transformer[abstract_input]
        exact_abstraction = connection.alpha[concrete_result]
        checked += 1
        if not abstract.below(exact_abstraction, abstract_result):
            violations.append(
                f"abstract transformer is unsound at concrete={concrete_value!r}"
            )
    return LawAssessment(
        LawStatus.VIOLATED if violations else LawStatus.SATISFIED,
        tuple(violations),
        checked,
    )


@dataclass(frozen=True, slots=True)
class FiniteLens:
    lens_id: str
    source_values: frozenset[Element]
    view_values: frozenset[Element]
    get_map: Mapping[Element, Element]
    put_map: Mapping[tuple[Element, Element], Element]

    def __post_init__(self) -> None:
        if not self.lens_id.strip() or not self.source_values or not self.view_values:
            raise ValueError("finite lenses require identity, source, and view values")


def assess_lens_laws(lens: FiniteLens) -> LawAssessment:
    if set(lens.get_map) != set(lens.source_values):
        return LawAssessment(LawStatus.CANNOT_CHECK, ("get is not total",), 0)
    expected_put_domain = {
        (view, source)
        for view in lens.view_values
        for source in lens.source_values
    }
    if set(lens.put_map) != expected_put_domain:
        return LawAssessment(LawStatus.CANNOT_CHECK, ("put is not total",), 0)
    if any(view not in lens.view_values for view in lens.get_map.values()):
        return LawAssessment(LawStatus.CANNOT_CHECK, ("get leaves the view domain",), 0)
    if any(source not in lens.source_values for source in lens.put_map.values()):
        return LawAssessment(LawStatus.CANNOT_CHECK, ("put leaves the source domain",), 0)

    violations: list[str] = []
    checked = 0
    for source in lens.source_values:
        current_view = lens.get_map[source]
        checked += 1
        if lens.put_map[(current_view, source)] != source:
            violations.append(f"GETPUT fails at source={source!r}")
        for view in lens.view_values:
            updated_source = lens.put_map[(view, source)]
            checked += 1
            if lens.get_map[updated_source] != view:
                violations.append(f"PUTGET fails at source={source!r}, view={view!r}")
            for second_view in lens.view_values:
                checked += 1
                left = lens.put_map[(second_view, updated_source)]
                right = lens.put_map[(second_view, source)]
                if left != right:
                    violations.append(
                        f"PUTPUT fails at source={source!r}, views={view!r},{second_view!r}"
                    )
    return LawAssessment(
        LawStatus.VIOLATED if violations else LawStatus.SATISFIED,
        tuple(violations),
        checked,
    )


@dataclass(frozen=True, slots=True)
class FiniteConsequenceTheory:
    theory_id: str
    language: frozenset[str]
    consequences: frozenset[str]

    def __post_init__(self) -> None:
        if not self.theory_id.strip() or not self.language:
            raise ValueError("consequence theories require identity and language")
        if not self.consequences <= self.language:
            raise ValueError("consequences must belong to the theory language")


@dataclass(frozen=True, slots=True)
class ConservativeExtensionAssessment:
    status: ConservativeExtensionStatus
    new_old_language_consequences: tuple[str, ...]
    lost_old_language_consequences: tuple[str, ...]
    authority_granted: bool = False
    novelty_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted or self.novelty_granted:
            raise ValueError("conservative-extension checks are non-authorizing")


def assess_conservative_extension(
    source: FiniteConsequenceTheory,
    extension: FiniteConsequenceTheory,
) -> ConservativeExtensionAssessment:
    if not source.language <= extension.language:
        return ConservativeExtensionAssessment(
            ConservativeExtensionStatus.CANNOT_CHECK,
            (),
            (),
        )
    extension_old = extension.consequences & source.language
    new = tuple(sorted(extension_old - source.consequences))
    lost = tuple(sorted(source.consequences - extension_old))
    if lost:
        status = ConservativeExtensionStatus.LOST_OLD_LANGUAGE_CONSEQUENCE
    elif new:
        status = ConservativeExtensionStatus.NONCONSERVATIVE_NEW_OLD_LANGUAGE_CONSEQUENCE
    else:
        status = ConservativeExtensionStatus.CONSERVATIVE
    return ConservativeExtensionAssessment(status, new, lost)

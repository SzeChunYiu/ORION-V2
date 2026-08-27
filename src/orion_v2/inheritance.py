from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class InheritanceRelation(str, Enum):
    COPIES = "COPIES"
    DERIVES = "DERIVES"
    REFINES = "REFINES"
    TRANSLATES = "TRANSLATES"
    COMPOSES = "COMPOSES"
    CALIBRATES_FROM = "CALIBRATES_FROM"
    EVALUATED_BY = "EVALUATED_BY"


class InheritanceStatus(str, Enum):
    RETICULATE_INHERITANCE_VALID = "RETICULATE_INHERITANCE_VALID"
    MISSING_COMPONENT_SUPPORT = "MISSING_COMPONENT_SUPPORT"
    UNMAPPED_COMPONENT_INHERITANCE = "UNMAPPED_COMPONENT_INHERITANCE"
    AMBIGUOUS_PARENT_ASSIGNMENT = "AMBIGUOUS_PARENT_ASSIGNMENT"
    CANNOT_CHECK = "CANNOT_CHECK"


class ComponentValidityStatus(str, Enum):
    PRESERVED = "PRESERVED"
    REOPENED = "REOPENED"
    CANNOT_CHECK = "CANNOT_CHECK"


@dataclass(frozen=True, slots=True)
class ComponentContribution:
    parent_artifact_id: str
    child_artifact_id: str
    component_id: str
    relation: InheritanceRelation
    correspondence_id: str = ""

    def __post_init__(self) -> None:
        if any(
            not value.strip()
            for value in (
                self.parent_artifact_id,
                self.child_artifact_id,
                self.component_id,
            )
        ):
            raise ValueError("component contributions require non-blank identities")
        if self.parent_artifact_id == self.child_artifact_id:
            raise ValueError("an artifact cannot inherit a component from itself")
        object.__setattr__(self, "relation", InheritanceRelation(self.relation))
        if self.relation in {
            InheritanceRelation.TRANSLATES,
            InheritanceRelation.REFINES,
            InheritanceRelation.CALIBRATES_FROM,
        } and not self.correspondence_id.strip():
            raise ValueError("translation/refinement/calibration requires correspondence")


@dataclass(frozen=True, slots=True)
class ComponentSupportFamily:
    family_id: str
    child_artifact_id: str
    component_id: str
    required_parent_artifact_ids: frozenset[str]

    def __post_init__(self) -> None:
        if any(
            not value.strip()
            for value in (self.family_id, self.child_artifact_id, self.component_id)
        ):
            raise ValueError("support-family identities must be non-blank")
        if not self.required_parent_artifact_ids or any(
            not value.strip() for value in self.required_parent_artifact_ids
        ):
            raise ValueError("support families require non-blank parents")
        if self.child_artifact_id in self.required_parent_artifact_ids:
            raise ValueError("a support family cannot require its child as parent")


@dataclass(frozen=True, slots=True)
class InheritedCommitment:
    commitment_id: str
    artifact_id: str
    required_component_ids: frozenset[str]

    def __post_init__(self) -> None:
        if not self.commitment_id.strip() or not self.artifact_id.strip():
            raise ValueError("commitment and artifact identities must be non-blank")
        if not self.required_component_ids or any(
            not value.strip() for value in self.required_component_ids
        ):
            raise ValueError("commitments require non-blank components")


@dataclass(frozen=True, slots=True)
class ReticulateInheritanceSystem:
    system_id: str
    artifact_ids: frozenset[str]
    required_components_by_artifact: Mapping[str, frozenset[str]]
    contributions: tuple[ComponentContribution, ...]
    support_families: tuple[ComponentSupportFamily, ...]
    commitments: tuple[InheritedCommitment, ...] = ()

    def __post_init__(self) -> None:
        if not self.system_id.strip() or not self.artifact_ids:
            raise ValueError("inheritance system requires identity and artifacts")
        if any(not value.strip() for value in self.artifact_ids):
            raise ValueError("artifact identities may not be blank")
        if not set(self.required_components_by_artifact) <= set(self.artifact_ids):
            raise ValueError("required-component map references unknown artifacts")
        for artifact_id, components in self.required_components_by_artifact.items():
            if any(not value.strip() for value in components):
                raise ValueError(f"artifact {artifact_id} has a blank component")
        for contribution in self.contributions:
            if (
                contribution.parent_artifact_id not in self.artifact_ids
                or contribution.child_artifact_id not in self.artifact_ids
            ):
                raise ValueError("component contribution references unknown artifact")
        family_ids = [family.family_id for family in self.support_families]
        if len(family_ids) != len(set(family_ids)):
            raise ValueError("support family identities must be unique")
        for family in self.support_families:
            if family.child_artifact_id not in self.artifact_ids or not set(
                family.required_parent_artifact_ids
            ) <= set(self.artifact_ids):
                raise ValueError("support family references unknown artifact")
        commitment_ids = [commitment.commitment_id for commitment in self.commitments]
        if len(commitment_ids) != len(set(commitment_ids)):
            raise ValueError("commitment identities must be unique")
        for commitment in self.commitments:
            if commitment.artifact_id not in self.artifact_ids:
                raise ValueError("commitment references unknown artifact")
        self._assert_acyclic()

    def _assert_acyclic(self) -> None:
        children = {artifact_id: set() for artifact_id in self.artifact_ids}
        indegree = {artifact_id: 0 for artifact_id in self.artifact_ids}
        for contribution in self.contributions:
            if contribution.child_artifact_id not in children[
                contribution.parent_artifact_id
            ]:
                children[contribution.parent_artifact_id].add(
                    contribution.child_artifact_id
                )
                indegree[contribution.child_artifact_id] += 1
        queue = [
            artifact_id for artifact_id, degree in indegree.items() if degree == 0
        ]
        visited = 0
        while queue:
            artifact_id = queue.pop()
            visited += 1
            for child in children[artifact_id]:
                indegree[child] -= 1
                if indegree[child] == 0:
                    queue.append(child)
        if visited != len(indegree):
            raise ValueError("reticulate inheritance graph must be acyclic")


@dataclass(frozen=True, slots=True)
class InheritanceAssessment:
    system_id: str
    status: InheritanceStatus
    supported_components: tuple[tuple[str, str], ...]
    unsupported_components: tuple[tuple[str, str], ...]
    multi_parent_components: tuple[tuple[str, str], ...]
    violations: tuple[str, ...]
    authority_granted: bool = False
    correctness_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted or self.correctness_granted:
            raise ValueError(
                "inheritance assessment grants neither authority nor correctness"
            )


@dataclass(frozen=True, slots=True)
class ComponentRevalidationRecord:
    artifact_id: str
    component_id: str
    status: ComponentValidityStatus
    surviving_family_ids: tuple[str, ...]
    defeated_family_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class InheritanceRevalidationReceipt:
    revoked_artifact_ids: tuple[str, ...]
    component_records: tuple[ComponentRevalidationRecord, ...]
    reopened_commitment_ids: tuple[str, ...]
    preserved_commitment_ids: tuple[str, ...]
    authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.authority_granted:
            raise ValueError("revalidation receipts cannot grant authority")


def assess_reticulate_inheritance(
    system: ReticulateInheritanceSystem,
) -> InheritanceAssessment:
    contribution_keys = {
        (
            contribution.parent_artifact_id,
            contribution.child_artifact_id,
            contribution.component_id,
        )
        for contribution in system.contributions
    }
    supported: list[tuple[str, str]] = []
    unsupported: list[tuple[str, str]] = []
    multi_parent: list[tuple[str, str]] = []
    violations: list[str] = []

    families_by_component: dict[tuple[str, str], list[ComponentSupportFamily]] = {}
    for family in system.support_families:
        families_by_component.setdefault(
            (family.child_artifact_id, family.component_id), []
        ).append(family)
        missing_edges = [
            parent_id
            for parent_id in family.required_parent_artifact_ids
            if (parent_id, family.child_artifact_id, family.component_id)
            not in contribution_keys
        ]
        if missing_edges:
            violations.append(
                f"support family {family.family_id} lacks contributions from: "
                + ", ".join(sorted(missing_edges))
            )

    for artifact_id, components in system.required_components_by_artifact.items():
        for component_id in components:
            families = families_by_component.get((artifact_id, component_id), [])
            if not families:
                unsupported.append((artifact_id, component_id))
                continue
            supported.append((artifact_id, component_id))
            parent_union = {
                parent_id
                for family in families
                for parent_id in family.required_parent_artifact_ids
            }
            if len(parent_union) > 1:
                multi_parent.append((artifact_id, component_id))

    contribution_by_key: dict[tuple[str, str], list[ComponentContribution]] = {}
    for contribution in system.contributions:
        contribution_by_key.setdefault(
            (contribution.child_artifact_id, contribution.component_id), []
        ).append(contribution)
    for (artifact_id, component_id), contributions in contribution_by_key.items():
        if len(contributions) > 1:
            family_parent_sets = [
                family.required_parent_artifact_ids
                for family in families_by_component.get((artifact_id, component_id), [])
            ]
            represented_parents = {
                contribution.parent_artifact_id for contribution in contributions
            }
            if represented_parents and not family_parent_sets:
                violations.append(
                    f"multiple parents for {artifact_id}:{component_id} lack support-family semantics"
                )

    if violations:
        status = InheritanceStatus.UNMAPPED_COMPONENT_INHERITANCE
    elif unsupported:
        status = InheritanceStatus.MISSING_COMPONENT_SUPPORT
    else:
        status = InheritanceStatus.RETICULATE_INHERITANCE_VALID
    return InheritanceAssessment(
        system.system_id,
        status,
        tuple(sorted(supported)),
        tuple(sorted(unsupported)),
        tuple(sorted(multi_parent)),
        tuple(violations),
    )


def revalidate_inheritance(
    system: ReticulateInheritanceSystem,
    *,
    revoked_artifact_ids: tuple[str, ...],
) -> InheritanceRevalidationReceipt:
    revoked = set(revoked_artifact_ids)
    if not revoked <= set(system.artifact_ids):
        raise ValueError("revocation references unknown artifact")
    if any(not item.strip() for item in revoked):
        raise ValueError("revoked artifact ids may not be blank")

    families_by_component: dict[tuple[str, str], list[ComponentSupportFamily]] = {}
    for family in system.support_families:
        families_by_component.setdefault(
            (family.child_artifact_id, family.component_id), []
        ).append(family)

    records: list[ComponentRevalidationRecord] = []
    component_status: dict[tuple[str, str], ComponentValidityStatus] = {}
    for artifact_id, components in system.required_components_by_artifact.items():
        for component_id in components:
            families = families_by_component.get((artifact_id, component_id), [])
            surviving = tuple(
                sorted(
                    family.family_id
                    for family in families
                    if not (set(family.required_parent_artifact_ids) & revoked)
                )
            )
            defeated = tuple(
                sorted(
                    family.family_id
                    for family in families
                    if set(family.required_parent_artifact_ids) & revoked
                )
            )
            if not families:
                status = ComponentValidityStatus.CANNOT_CHECK
            elif surviving:
                status = ComponentValidityStatus.PRESERVED
            else:
                status = ComponentValidityStatus.REOPENED
            component_status[(artifact_id, component_id)] = status
            records.append(
                ComponentRevalidationRecord(
                    artifact_id,
                    component_id,
                    status,
                    surviving,
                    defeated,
                )
            )

    reopened_commitments: list[str] = []
    preserved_commitments: list[str] = []
    for commitment in system.commitments:
        statuses = {
            component_status.get(
                (commitment.artifact_id, component_id),
                ComponentValidityStatus.CANNOT_CHECK,
            )
            for component_id in commitment.required_component_ids
        }
        if statuses == {ComponentValidityStatus.PRESERVED}:
            preserved_commitments.append(commitment.commitment_id)
        else:
            reopened_commitments.append(commitment.commitment_id)

    return InheritanceRevalidationReceipt(
        tuple(sorted(revoked)),
        tuple(
            sorted(records, key=lambda item: (item.artifact_id, item.component_id))
        ),
        tuple(sorted(reopened_commitments)),
        tuple(sorted(preserved_commitments)),
    )

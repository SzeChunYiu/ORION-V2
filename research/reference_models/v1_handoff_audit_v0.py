"""ORION V1 -> V2 handoff manifest auditor V0.

This verifier checks manifest completeness and identity consistency only. A PASS
cannot freeze V1 by itself: an independently authorized handoff receipt must use
the verified manifest and exact artifact bytes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class HandoffAuditResult:
    passed: bool
    terminal: str
    reasons: tuple[str, ...]
    subject_commit: str
    artifact_count: int


class HandoffInputError(ValueError):
    pass


def audit_handoff_manifest(
    manifest: Mapping[str, Any], required_classes: Sequence[str]
) -> HandoffAuditResult:
    subject_commit = str(manifest.get("subject_commit", ""))
    artifacts = manifest.get("artifacts", ())
    if not isinstance(artifacts, Sequence) or isinstance(artifacts, (str, bytes)):
        raise HandoffInputError("artifacts must be a sequence")

    def result(passed: bool, terminal: str, *reasons: str) -> HandoffAuditResult:
        return HandoffAuditResult(
            passed=passed,
            terminal=terminal,
            reasons=tuple(reasons),
            subject_commit=subject_commit,
            artifact_count=len(artifacts),
        )

    if not COMMIT_RE.fullmatch(subject_commit):
        return result(False, "INVALID_SUBJECT_COMMIT", "subject_commit is not a 40-hex Git identity")

    seen_paths: set[str] = set()
    seen_classes: set[str] = set()
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, Mapping):
            return result(False, "INVALID_ARTIFACT_IDENTITY", f"artifact {index} is not a mapping")
        artifact_class = str(artifact.get("class", ""))
        path = str(artifact.get("path", ""))
        sha256 = str(artifact.get("sha256", ""))
        artifact_commit = str(artifact.get("subject_commit", ""))
        if not artifact_class or not path or not SHA256_RE.fullmatch(sha256):
            return result(False, "INVALID_ARTIFACT_IDENTITY", f"artifact {index} lacks class/path/valid sha256")
        if path in seen_paths:
            return result(False, "DUPLICATE_ARTIFACT_PATH", path)
        seen_paths.add(path)
        seen_classes.add(artifact_class)
        if artifact_commit != subject_commit:
            return result(False, "MIXED_SUBJECT_COMMITS", f"{path}: {artifact_commit} != {subject_commit}")

    missing = sorted(set(required_classes) - seen_classes)
    if missing:
        return result(False, "MISSING_REQUIRED_CLASS", *missing)

    if manifest.get("non_retroactivity") is not True:
        return result(False, "NON_RETROACTIVITY_NOT_BOUND", "non_retroactivity must be true")

    independent_review_id = str(manifest.get("independent_review_id", ""))
    if not independent_review_id:
        return result(False, "INDEPENDENT_REVIEW_NOT_BOUND", "independent review identity is absent")

    unlock_decision = str(manifest.get("unlock_decision", ""))
    if not unlock_decision:
        return result(False, "UNLOCK_DECISION_NOT_BOUND", "unlock decision is absent")

    source_repository = str(manifest.get("source_repository", ""))
    if source_repository != "SzeChunYiu/ORION":
        return result(False, "WRONG_SOURCE_REPOSITORY", source_repository)

    return result(
        True,
        "MANIFEST_STRUCTURALLY_COMPLETE",
        "all required evidence classes are present and bound to one subject commit",
        "independent review and non-retroactivity identities are declared",
        "artifact bytes and reviewer authority still require external verification",
    )


__all__ = [
    "COMMIT_RE",
    "SHA256_RE",
    "HandoffAuditResult",
    "HandoffInputError",
    "audit_handoff_manifest",
]

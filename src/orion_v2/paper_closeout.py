from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


EXPECTED_SCHEMA = "orion.v2.paper-contraction-ledger.v1"
EXPECTED_PORTFOLIO = {"P-A", "P-B", "P-C", "P-D", "P-E"}
EXPECTED_CANDIDATES = {f"C{index:02d}" for index in range(1, 13)}
ANCHORS = {"C01", "C02", "C04", "C07", "C10"}
MERGED_OR_NOT_OPEN = EXPECTED_CANDIDATES - ANCHORS


@dataclass(frozen=True, slots=True)
class PaperContractionValidation:
    valid: bool
    portfolio_count: int
    candidate_count: int
    standalone_candidate_count: int
    errors: tuple[str, ...]
    terminal: str
    publication_authority_granted: bool = False

    def __post_init__(self) -> None:
        if self.publication_authority_granted:
            raise ValueError("programme contraction cannot grant publication authority")


def validate_paper_contraction(ledger: Mapping[str, Any]) -> PaperContractionValidation:
    errors: list[str] = []
    if ledger.get("schema_version") != EXPECTED_SCHEMA:
        errors.append("unexpected paper-contraction schema_version")
    if ledger.get("status") != "PORTFOLIO_CONTRACTION_FROZEN_PUBLICATION_OPEN":
        errors.append("programme must distinguish frozen contraction from open publication gate")

    portfolio = ledger.get("portfolio")
    if not isinstance(portfolio, Mapping):
        portfolio = {}
        errors.append("portfolio must be an object")
    if set(portfolio) != EXPECTED_PORTFOLIO:
        errors.append("contracted portfolio must contain exactly P-A through P-E")
    for paper_id, row in portfolio.items():
        if not isinstance(row, Mapping):
            errors.append(f"portfolio row {paper_id!r} must be an object")
            continue
        absorbs = row.get("absorbs")
        if not isinstance(absorbs, list) or not absorbs:
            errors.append(f"portfolio row {paper_id!r} has no absorbed candidates")
        if not str(row.get("open_scientific_gate", "")).strip():
            errors.append(f"portfolio row {paper_id!r} lacks an open scientific gate")

    dispositions = ledger.get("candidate_dispositions")
    if not isinstance(dispositions, list):
        dispositions = []
        errors.append("candidate_dispositions must be a list")
    ids: list[str] = []
    standalone: set[str] = set()
    for row in dispositions:
        if not isinstance(row, Mapping):
            errors.append("candidate disposition row must be an object")
            continue
        candidate = str(row.get("candidate", ""))
        ids.append(candidate)
        if row.get("standalone_issue_remains") is True:
            standalone.add(candidate)
        if not str(row.get("disposition", "")).strip():
            errors.append(f"candidate {candidate!r} lacks disposition")
    if set(ids) != EXPECTED_CANDIDATES or len(ids) != len(EXPECTED_CANDIDATES):
        errors.append("candidate dispositions must cover exactly C01 through C12 once")
    if standalone != ANCHORS:
        errors.append("only C01/C02/C04/C07/C10 may retain standalone programme issues")
    if not MERGED_OR_NOT_OPEN.isdisjoint(standalone):
        errors.append("merged/not-open candidates may not retain standalone paper identity")

    programme_gate = ledger.get("programme_gate")
    if not isinstance(programme_gate, Mapping):
        programme_gate = {}
        errors.append("programme_gate is missing")
    if programme_gate.get("portfolio_contraction_frozen") is not True:
        errors.append("portfolio contraction must be frozen")
    if programme_gate.get("default_new_candidate_allowed") is not False:
        errors.append("new paper candidates must fail closed by default")
    if programme_gate.get("new_candidate_requires_named_closeout_blocker") is not True:
        errors.append("new candidate must require a named closeout blocker")

    publication_gate = ledger.get("publication_gate")
    if not isinstance(publication_gate, Mapping):
        publication_gate = {}
        errors.append("publication_gate is missing")
    if publication_gate.get("frozen") is not False:
        errors.append("programme contraction may not freeze publication authority")
    if not publication_gate.get("remaining"):
        errors.append("publication gate must retain explicit external/scientific requirements")

    authority = ledger.get("authority")
    if not isinstance(authority, Mapping):
        authority = {}
        errors.append("authority block is missing")
    for key in (
        "grants_final_paper_identity",
        "grants_novelty",
        "grants_scientific_truth",
        "grants_publication_authority",
        "grants_v2_closeout",
    ):
        if authority.get(key) is not False:
            errors.append(f"paper contraction may not grant {key}")

    return PaperContractionValidation(
        valid=not errors,
        portfolio_count=len(portfolio),
        candidate_count=len(dispositions),
        standalone_candidate_count=len(standalone),
        errors=tuple(errors),
        terminal=(
            "PAPER_PORTFOLIO_CONTRACTION_FROZEN_PUBLICATION_OPEN"
            if not errors
            else "PAPER_CONTRACTION_INVALID"
        ),
    )

from __future__ import annotations

import copy
import json
from pathlib import Path

from orion_v2.paper_closeout import validate_paper_contraction


ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "papers" / "PAPER_CONTRACTION_LEDGER_WAVE06_V1.json"


def _load() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def test_contracted_paper_portfolio_is_frozen_without_publication_authority() -> None:
    result = validate_paper_contraction(_load())
    assert result.valid, result.errors
    assert result.portfolio_count == 5
    assert result.candidate_count == 12
    assert result.standalone_candidate_count == 5
    assert result.publication_authority_granted is False
    assert result.terminal == "PAPER_PORTFOLIO_CONTRACTION_FROZEN_PUBLICATION_OPEN"


def test_merged_candidate_cannot_reappear_as_standalone() -> None:
    mutated = copy.deepcopy(_load())
    row = next(item for item in mutated["candidate_dispositions"] if item["candidate"] == "C05")
    row["standalone_issue_remains"] = True
    result = validate_paper_contraction(mutated)
    assert not result.valid
    assert any("only C01/C02/C04/C07/C10" in error for error in result.errors)


def test_c12_cannot_open_by_default() -> None:
    mutated = copy.deepcopy(_load())
    row = next(item for item in mutated["candidate_dispositions"] if item["candidate"] == "C12")
    row["standalone_issue_remains"] = True
    result = validate_paper_contraction(mutated)
    assert not result.valid


def test_new_candidate_default_must_fail_closed() -> None:
    mutated = copy.deepcopy(_load())
    mutated["programme_gate"]["default_new_candidate_allowed"] = True
    result = validate_paper_contraction(mutated)
    assert not result.valid
    assert any("fail closed" in error for error in result.errors)


def test_programme_contraction_cannot_claim_publication_freeze() -> None:
    mutated = copy.deepcopy(_load())
    mutated["publication_gate"]["frozen"] = True
    result = validate_paper_contraction(mutated)
    assert not result.valid
    assert any("publication authority" in error for error in result.errors)


def test_programme_contraction_cannot_mint_novelty() -> None:
    mutated = copy.deepcopy(_load())
    mutated["authority"]["grants_novelty"] = True
    result = validate_paper_contraction(mutated)
    assert not result.valid
    assert any("grants_novelty" in error for error in result.errors)

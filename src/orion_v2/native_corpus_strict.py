from __future__ import annotations

from dataclasses import replace
from typing import Final

from .native_corpus import (
    built_in_native_recovery_cases as _observed_native_recovery_cases,
    built_in_target_adaptation_contracts,
)
from .native_recovery import NativeRecoveryCase

# These expectations are frozen independently of the computations in
# native_corpus.py.  The observed result must match this registry; it may not
# write its own answer key.
_EXPECTED_GENERALIZED: Final[dict[str, object]] = {
    "NR04-01": "SOUND",
    "NR04-02": "CANNOT_CHECK",
    "NR04-03": "CANNOT_CHECK",
    "NR04-04": "MULTIPLE_DISCRIMINABLE",
    "NR04-05": "IDENTIFIED",
    "NR04-06": "EXACT",
    "NR04-07": "PARTIALLY_COMPARABLE",
    "NR04-08": "NONCOMPARABLE",
    "NR04-09": "CANNOT_CHECK",
    "NR04-10": frozenset({"stable"}),
    "NR04-11": frozenset({"stable", "boundary"}),
    "NR04-12": frozenset({"novice", "basics", "mastery"}),
    "NR04-13": "GLOBAL_OBSTRUCTION",
    "NR04-14": "LEFT_BLACKWELL_DOMINATES",
    "NR04-15": 1.6,
    "NR04-16": "POLICY_WINNER_REVERSAL",
    "NR04-17": "PARETO_PORTFOLIO_SET",
}


def built_in_native_recovery_cases() -> tuple[NativeRecoveryCase, ...]:
    """Return computed observations bound to an independent expectation registry."""

    observed = _observed_native_recovery_cases()
    observed_ids = {case.case_id for case in observed}
    expected_ids = set(_EXPECTED_GENERALIZED)
    if observed_ids != expected_ids:
        missing = sorted(expected_ids - observed_ids)
        unexpected = sorted(observed_ids - expected_ids)
        raise ValueError(
            f"native recovery corpus identity drift: missing={missing}, unexpected={unexpected}"
        )
    return tuple(
        replace(
            case,
            native_to_generalized={
                case.native_judgment: _EXPECTED_GENERALIZED[case.case_id]
            },
        )
        for case in observed
    )


__all__ = [
    "built_in_native_recovery_cases",
    "built_in_target_adaptation_contracts",
]

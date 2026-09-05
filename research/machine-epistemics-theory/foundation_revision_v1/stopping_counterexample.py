"""Exact counterexample to ORION-V2 #317 T2(c), observed after the core receipt.

This is a theory-calibration script, not the OCM scheduler. Standard library only.
"""
from fractions import Fraction as F
import json


def run() -> dict:
    alpha, theta = F(1, 2), F(3, 5)
    beta = 1 - alpha
    # P = [1], seed = [1], a_k = 1 - beta**(k+1), fixed point = 1.
    lower = lambda k: 1 - beta ** (k + 1)
    width = lambda k: beta ** (k + 1)
    proposed = next(k for k in range(20) if width(k) < theta - lower(0))
    actual = next(k for k in range(20) if lower(k) >= theta)
    if (proposed, actual) != (3, 1):
        raise ValueError('stopping counterexample failed to reproduce')
    if not lower(0) < theta <= lower(1):
        raise ValueError('FOUND was not the actual earlier decision')
    # At theta = a* = 1, the partial-sum interval cannot decide YES in finite time.
    equality_cases = 0
    for k in range(21):
        if not lower(k) < 1 == lower(k) + width(k):
            raise ValueError('threshold-equality control failed')
        equality_cases += 1
    return {
        'terminal': 'COUNTEREXAMPLE_REPRODUCED',
        'target': 'ORION-V2 #317 T2(c)',
        'source_commit': 'd756c086edc46ad4e5e682f69730b72c1dc26a4c',
        'P': [['1']], 'seed': ['1'], 'alpha': str(alpha), 'theta': str(theta),
        'a0': str(lower(0)), 'a1': str(lower(1)),
        'claimed_earliest_budget': proposed, 'actual_first_FOUND': actual,
        'threshold_equality_controls': equality_cases,
        'independent_review': 'NOT_PERFORMED',
        'all_size_argument': 'CONCURRENT_RECONCILIATION.md; not inferred from 21 controls'
    }


if __name__ == '__main__':
    try:
        print(json.dumps(run(), sort_keys=True, indent=2))
    except ValueError as exc:
        print(json.dumps({'terminal': 'FAIL', 'reason': str(exc)}))
        raise SystemExit(1)

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from math import inf
from typing import Hashable, Mapping

@dataclass(frozen=True, slots=True)
class Hypothesis:
    hypothesis_id: str
    def __post_init__(self) -> None:
        if not self.hypothesis_id.strip(): raise ValueError("hypothesis_id must be non-blank")

@dataclass(frozen=True, slots=True)
class Probe:
    probe_id: str; outcomes: Mapping[str, Hashable]; cost: float = 0.0; admissible: bool = True; authority_requirements: tuple[str, ...] = ()
    def __post_init__(self) -> None:
        if not self.probe_id.strip(): raise ValueError("probe_id must be non-blank")
        if self.cost < 0: raise ValueError("probe cost must be non-negative")
        if any(not key.strip() for key in self.outcomes): raise ValueError("outcome identities must be non-blank")
        if any(not item.strip() for item in self.authority_requirements): raise ValueError("authority requirements may not contain blanks")
    def separates(self, left_id: str, right_id: str) -> bool:
        return left_id in self.outcomes and right_id in self.outcomes and self.outcomes[left_id] != self.outcomes[right_id]

class ProbeDesignStatus(str, Enum):
    IDENTIFYING_SET = "IDENTIFYING_SET"; NONIDENTIFIABLE_UNDER_PROBE_FAMILY = "NONIDENTIFIABLE_UNDER_PROBE_FAMILY"; NO_ADMISSIBLE_PROBES = "NO_ADMISSIBLE_PROBES"; CANNOT_CHECK_MISSING_PREDICTIONS = "CANNOT_CHECK_MISSING_PREDICTIONS"

@dataclass(frozen=True, slots=True)
class ProbeDesignReceipt:
    status: ProbeDesignStatus; selected_probe_ids: tuple[str, ...]; total_cost: float; separated_pairs: tuple[tuple[str, str], ...]; unresolved_pairs: tuple[tuple[str, str], ...]; authority_granted: bool = False
    def __post_init__(self) -> None:
        if self.authority_granted: raise ValueError("probe design cannot grant execution authority")

def _pairs(hypotheses: tuple[Hypothesis, ...]) -> tuple[tuple[str, str], ...]:
    ids = tuple(sorted(h.hypothesis_id for h in hypotheses))
    if len(ids) != len(set(ids)): raise ValueError("hypothesis identities must be unique")
    return tuple(combinations(ids, 2))

def minimum_separating_probe_set(hypotheses: tuple[Hypothesis, ...], probes: tuple[Probe, ...], *, authority_satisfied: bool = False) -> ProbeDesignReceipt:
    if len(hypotheses) < 2: return ProbeDesignReceipt(ProbeDesignStatus.IDENTIFYING_SET, (), 0.0, (), ())
    pairs = _pairs(hypotheses)
    admissible = tuple(p for p in probes if p.admissible and (authority_satisfied or not p.authority_requirements))
    if not admissible: return ProbeDesignReceipt(ProbeDesignStatus.NO_ADMISSIBLE_PROBES, (), 0.0, (), pairs)
    missing = tuple(pair for pair in pairs if any(pair[0] not in p.outcomes or pair[1] not in p.outcomes for p in admissible))
    if missing: return ProbeDesignReceipt(ProbeDesignStatus.CANNOT_CHECK_MISSING_PREDICTIONS, (), 0.0, (), tuple(sorted(set(missing))))
    best = None
    for size in range(1, len(admissible) + 1):
        for subset in combinations(admissible, size):
            separated = {pair for pair in pairs if any(p.separates(*pair) for p in subset)}
            if len(separated) != len(pairs): continue
            ids = tuple(sorted(p.probe_id for p in subset)); candidate = (sum(p.cost for p in subset), size, ids)
            if best is None or candidate < best: best = candidate
    if best is None:
        separated = tuple(pair for pair in pairs if any(p.separates(*pair) for p in admissible)); unresolved = tuple(pair for pair in pairs if pair not in set(separated))
        return ProbeDesignReceipt(ProbeDesignStatus.NONIDENTIFIABLE_UNDER_PROBE_FAMILY, (), inf, separated, unresolved)
    return ProbeDesignReceipt(ProbeDesignStatus.IDENTIFYING_SET, best[2], best[0], pairs, ())

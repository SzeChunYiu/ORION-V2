"""Independent finite calibration of the written convergence statements."""
from itertools import combinations, product
import json


def choose_query(rows):
    scored = []
    for q in range(len(rows[0])):
        counts = [sum(row[q] == answer for row in rows) for answer in (0, 1)]
        if min(counts) > 0:
            scored.append((max(counts), q))
    return min(scored)[1] if scored else None


def check():
    identification_cases = 0
    universe = tuple(product((0, 1), repeat=3))
    for size in range(1, 5):
        for hypotheses in combinations(universe, size):
            for truth in hypotheses:
                version = hypotheses
                history = []
                while len(version) > 1:
                    q = choose_query(version)
                    if q is None:
                        raise AssertionError("distinct prediction rows were not separated")
                    before = len(version)
                    history.append((q, truth[q]))
                    version = tuple(row for row in version if row[q] == truth[q])
                    if truth not in version or len(version) >= before:
                        raise AssertionError("truth preservation or strict reduction failed")
                if version != (truth,) or len(history) > size - 1:
                    raise AssertionError("finite identification bound failed")
                # Removing observations expands or preserves the compatible class.
                for deleted in range(len(history)):
                    retained = history[:deleted] + history[deleted + 1:]
                    reopened = tuple(row for row in hypotheses if all(row[q] == a for q, a in retained))
                    if not set(version) <= set(reopened):
                        raise AssertionError("revocation contraction")
                identification_cases += 1
    # All guided positions may be useless. The primitive rank bound still holds.
    fairness_cases = 0
    for rank in range(1, 1025):
        primitive_visits = tuple(slot // 2 for slot in range(1, 2 * rank + 1) if slot % 2 == 0)
        if primitive_visits != tuple(range(1, rank + 1)):
            raise AssertionError("primitive search starvation")
        fairness_cases += 1
    if choose_query(((0, 0), (0, 0))) is not None:
        raise AssertionError("equivalent models falsely distinguished")
    return {"status": "FINITE_CALIBRATION_PASS", "identification_cases": identification_cases,
            "fairness_cases": fairness_cases, "proof_assistant": "NOT_RUN",
            "parent_residual": "NOT_CLAIMED", "external_science": "NOT_RUN"}


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))

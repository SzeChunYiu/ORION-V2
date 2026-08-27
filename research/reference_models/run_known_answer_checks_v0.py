"""Run ORION-V2 V0 structural known-answer checks without pytest.

This is a research-specification check. A zero exit status means only that the
small exact reference cases agree with the provisional V0 relation semantics.
"""

from __future__ import annotations

import json
from pathlib import Path

from structural_relations_v0 import (
    JumpLevelResult,
    classify_censoring_terminal,
    each_constraint_satisfiable,
    lts_bisimilar,
    markov_equivalent_dags,
    minimum_distinguishing_probe_sets,
    minimum_sufficient_jump_level,
    quotient_safe_for_target,
    role_equivalent,
    xor_constraints_satisfiable,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "known_answer_structural_cases_v0.json"


def main() -> int:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        fixtures = {case["case_id"]: case for case in json.load(handle)["cases"]}

    checks: list[dict[str, object]] = []

    def record(check_id: str, passed: bool, detail: object) -> None:
        checks.append({"check_id": check_id, "passed": passed, "detail": detail})
        if not passed:
            raise AssertionError(f"{check_id} failed: {detail!r}")

    parity = fixtures["local-global-parity-obstruction"]
    local = each_constraint_satisfiable(parity["variables"], parity["domains"], parity["constraints"])
    global_result = xor_constraints_satisfiable(parity["variables"], parity["domains"], parity["constraints"])
    record("local-global-obstruction", local is True and global_result is False, {"local": local, "global": global_result})

    causal = fixtures["causal-observational-tie-direction-difference"]
    markov = markov_equivalent_dags(causal["nodes"], causal["left_edges"], causal["right_edges"])
    record("causal-observational-equivalence", markov is True and causal["left_edges"] != causal["right_edges"], markov)

    behavioral = fixtures["same-vocabulary-different-transition-behaviour"]
    bisimilar = lts_bisimilar(behavioral["left"], behavioral["right"])
    record("same-words-different-behaviour", bisimilar is False, bisimilar)

    role = fixtures["different-vocabulary-same-relational-role"]
    roles_match = role_equivalent(role["left_role_profile"], role["right_role_profile"])
    record("different-words-same-role", roles_match is True, roles_match)

    quotient = fixtures["safe-current-quotient-unsafe-future-query"]
    current_safe = quotient_safe_for_target(quotient["states"], quotient["partition"], "current_score")
    future_safe = quotient_safe_for_target(quotient["states"], quotient["partition"], "future_revocation")
    record("context-relative-quotient", current_safe is True and future_safe is False, {"current": current_safe, "future": future_safe})

    probes = fixtures["minimum-distinguishing-probe"]
    minimum = minimum_distinguishing_probe_sets(probes["hypothesis_signatures"])
    record("minimum-distinguishing-probes", minimum == (("q1", "q3"),), minimum)

    censored = fixtures["censored-route-not-nonidentifiability"]
    terminal = classify_censoring_terminal(censored["provider_status"])
    record("censoring-terminal", terminal == "SEARCH_ROUTE_CENSORED", terminal)

    jump_results = [
        JumpLevelResult(1, True, False, "e:J1"),
        JumpLevelResult(2, True, True, "e:J2"),
        JumpLevelResult(3, True, True, "e:J3"),
    ]
    jump_level = minimum_sufficient_jump_level(jump_results, incumbent_insufficiency_witnessed=True)
    record("minimum-jump-level", jump_level == 2, jump_level)

    refused = minimum_sufficient_jump_level(jump_results, incumbent_insufficiency_witnessed=False)
    record("jump-requires-insufficiency", refused == "INCUMBENT_INSUFFICIENCY_NOT_IDENTIFIED", refused)

    summary = {
        "schema_id": "orion-v2.known-answer-check-result.v0",
        "authority": "LOCAL_RESEARCH_SPECIFICATION_ONLY",
        "fixture_path": str(FIXTURE_PATH.relative_to(ROOT)),
        "checks": checks,
        "passed": sum(1 for check in checks if check["passed"]),
        "total": len(checks),
        "terminal": "KNOWN_ANSWER_REFERENCE_CHECKS_GREEN",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

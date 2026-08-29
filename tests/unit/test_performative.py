from orion_v2.performative import EvaluationDeployment, assess_performative_evaluation, total_variation

def test_total_variation_known_answer() -> None: assert total_variation({"a": 1.0}, {"a": 0.5, "b": 0.5}) == 0.5

def test_proxy_improvement_can_hide_protected_regression() -> None:
    deployment = EvaluationDeployment("eval", "published-ranking", {"careful": 0.8, "gaming": 0.2}, {"careful": 0.2, "gaming": 0.8}, 0.5, 0.9, 0.8, 0.4, "policy-rollout-control")
    result = assess_performative_evaluation(deployment)
    assert result.proxy_improves_protected_worsens is True and result.terminal == "PROXY_IMPROVES_PROTECTED_OUTCOME_WORSENS"

def test_shift_without_control_is_cannot_check_causally() -> None:
    result = assess_performative_evaluation(EvaluationDeployment("eval", "policy", {"x": 1.0}, {"x": 0.5, "y": 0.5}, 0.5, 0.6), shift_tolerance=0.1)
    assert result.terminal == "PERFORMATIVE_SHIFT_DETECTED_CAUSE_CANNOT_CHECK"

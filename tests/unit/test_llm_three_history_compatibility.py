from scripts.check_llm_three_history_compatibility import assess


def test_three_history_pairwise_overlap_does_not_imply_joint_compatibility() -> None:
    result = assess()
    assert result["all_pairwise_intersections_nonempty"] is True
    assert result["joint_intersection_empty"] is True
    assert result["one_step_compatible"] is False
    assert result["empirical_llm_result"] is False
    assert result["scientific_authority"] is False

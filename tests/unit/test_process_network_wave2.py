from orion_v2.process_network import (
    ObligationProcessNetwork,
    ProcessSoundnessStatus,
    ProcessTask,
    assess_process_soundness,
)


def test_management_and_engineering_workflows_share_sound_obligation_structure() -> None:
    network = ObligationProcessNetwork(
        network_id="scientific-change-control",
        obligations=frozenset({"request", "verified", "validated", "approved"}),
        initial_fulfilled=frozenset({"request"}),
        terminal_obligations=frozenset({"approved"}),
        tasks=(
            ProcessTask(
                "verify",
                frozenset({"request"}),
                frozenset({"verified"}),
                (("reviewer-hours", 1),),
            ),
            ProcessTask(
                "validate",
                frozenset({"verified"}),
                frozenset({"validated"}),
                (("reviewer-hours", 1),),
            ),
            ProcessTask(
                "approve",
                frozenset({"validated"}),
                frozenset({"approved"}),
                authority_required=2,
            ),
        ),
        initial_resources=(("reviewer-hours", 2),),
        authority_ceiling=2,
    )
    result = assess_process_soundness(network)
    assert result.status is ProcessSoundnessStatus.SOUND
    assert result.completion_state_count >= 1


def test_missing_authority_is_unmeasured_completion_not_success() -> None:
    network = ObligationProcessNetwork(
        network_id="blocked-approval",
        obligations=frozenset({"verified", "approved"}),
        initial_fulfilled=frozenset({"verified"}),
        terminal_obligations=frozenset({"approved"}),
        tasks=(
            ProcessTask(
                "approve",
                frozenset({"verified"}),
                frozenset({"approved"}),
                authority_required=2,
            ),
        ),
        authority_ceiling=1,
    )
    result = assess_process_soundness(network)
    assert result.status is ProcessSoundnessStatus.CANNOT_CHECK
    assert result.completion_state_count == 0


def test_branch_into_unrecoverable_state_fails_soundness() -> None:
    network = ObligationProcessNetwork(
        network_id="bad-branch",
        obligations=frozenset({"start", "good", "bad", "done"}),
        initial_fulfilled=frozenset({"start"}),
        terminal_obligations=frozenset({"done"}),
        tasks=(
            ProcessTask(
                "good-route",
                frozenset({"start"}),
                frozenset({"good"}),
                reopens=frozenset({"start"}),
            ),
            ProcessTask(
                "bad-route",
                frozenset({"start"}),
                frozenset({"bad"}),
                reopens=frozenset({"start"}),
            ),
            ProcessTask("finish", frozenset({"good"}), frozenset({"done"})),
        ),
    )
    result = assess_process_soundness(network)
    assert result.status is ProcessSoundnessStatus.DEADLOCK
    assert result.deadlock_states

from orion_v2.probes import Hypothesis, Probe, ProbeDesignStatus, minimum_separating_probe_set

def test_minimum_cost_separating_set() -> None:
    hypotheses=(Hypothesis("h1"),Hypothesis("h2"),Hypothesis("h3")); probes=(Probe("p1",{"h1":0,"h2":1,"h3":1},cost=1),Probe("p2",{"h1":0,"h2":0,"h3":1},cost=1),Probe("expensive",{"h1":"a","h2":"b","h3":"c"},cost=5))
    receipt=minimum_separating_probe_set(hypotheses,probes)
    assert receipt.status is ProbeDesignStatus.IDENTIFYING_SET and receipt.selected_probe_ids==("p1","p2") and receipt.total_cost==2

def test_nonidentifiable_under_registered_probe_family() -> None:
    receipt=minimum_separating_probe_set((Hypothesis("h1"),Hypothesis("h2")),(Probe("p",{"h1":0,"h2":0}),))
    assert receipt.status is ProbeDesignStatus.NONIDENTIFIABLE_UNDER_PROBE_FAMILY and receipt.unresolved_pairs==(("h1","h2"),)

def test_authority_blocked_probe_is_not_admissible() -> None:
    probe=Probe("human-subject-intervention",{"h1":0,"h2":1},authority_requirements=("ethics-approval",))
    receipt=minimum_separating_probe_set((Hypothesis("h1"),Hypothesis("h2")),(probe,))
    assert receipt.status is ProbeDesignStatus.NO_ADMISSIBLE_PROBES

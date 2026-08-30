#!/usr/bin/env python3
"""AH20 exact known-answer case generators (epistemic atlas / horizon).

Five new classes x six seeded cases (seed 20260901) dressed from the EL10
domain pool, PLUS byte-identical reuse of all 48 EL10 worlds (re-derived
under EL10's own seed 20260830 and asserted equal to the committed
results/issue104/el10-r1 records before anything is emitted).

Every scenario states, in text, the registry facts that logically force the
private oracle; the oracle is exact by construction AND machine-cross-checked
against the AH10-green reference implementation src/orion_v2/epistemic_atlas.py
(assess_atlas_gluing / observational_partition / assess_probe_expansion /
UnknownRecord). class_id never appears in the public task.

Freeze: research/experiments/EPISTEMIC_ATLAS_HORIZON_AH20_SUITE_FREEZE_V1.md
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))
sys.path.insert(0, str(_SCRIPTS.parent / "src"))

from orion_el10_cases import CLASSES as EL10_CLASSES  # noqa: E402
from orion_el10_cases import COORDS, DOMAINS, generate_case as el10_generate_case  # noqa: E402

from orion_v2.epistemic_atlas import (  # noqa: E402
    LocalEpistemicChart,
    OverlapAssessment,
    ProbeOutcome,
    UnknownKind,
    UnknownRecord,
    assess_atlas_gluing,
    assess_probe_expansion,
    is_strict_partition_refinement,
    observational_partition,
)

AH_CLASSES = ["AHC0", "AHC1", "AHC2", "AHC3", "AHC4"]
PER_CLASS = 6
EL10_SEED = 20260830
AH_SEED = 20260901
EL10_RESULTS = _SCRIPTS.parent / "research" / "experiments" / "results" / "issue104" / "el10-r1"

# Atlas extension of the reused EL10 worlds (freeze section 1): the gluing
# disposition forced by each EL10 class's own registered facts. ELC1's
# full-envelope sweep is the registered global-section witness; ELC2-ELC6
# and ELC8 carry a registered incompatibility between the source (result
# report) context and the deployment context; ELC7 has two substrates with
# no registered correspondence.
EL10_GLUING = {
    "ELC1": ("GLOBAL_SECTION_WITNESSED", "full-envelope-sweep"),
    "ELC2": ("GLOBAL_SECTION_OBSTRUCTED", ""),
    "ELC3": ("GLOBAL_SECTION_OBSTRUCTED", ""),
    "ELC4": ("GLOBAL_SECTION_OBSTRUCTED", ""),
    "ELC5": ("GLOBAL_SECTION_OBSTRUCTED", ""),
    "ELC6": ("GLOBAL_SECTION_OBSTRUCTED", ""),
    "ELC7": ("CANNOT_CHECK", ""),
    "ELC8": ("GLOBAL_SECTION_OBSTRUCTED", ""),
}


def _domain(rng):
    return DOMAINS[rng.randrange(len(DOMAINS))]


def _ctx_block(pairs):
    return "REGISTERED CONTEXT COORDINATES (deployment frame; all seven):\n" + "\n".join(
        f"- {c}: {v}" for c, v in pairs
    )


def _registry(m1, m2, f1, f2):
    return (
        "METHOD REGISTRY (order of listing defines FIRST and SECOND):\n"
        f"- FIRST: {m1} -- {f1}\n"
        f"- SECOND: {m2} -- {f2}"
    )


def _oracle(cls, **fields):
    row = {
        "class_id": cls,
        "decision": "NOT_APPLICABLE",
        "holds_across_contexts": False,
        "gluing_disposition": "MATCHING_FAMILY_ONLY",
        "global_section_witness_id": "",
        "transport_verdict": "NOT_ESTABLISHED",
        "probe_decision": "NONE",
        "probe_id": "",
        "horizon_disposition": "NOT_APPLICABLE",
        "outside_atlas_witness_id": "",
    }
    row.update(fields)
    return row


def _gen_ahc0(rng, dom):
    """LOCAL_ONLY: one context, one chart, decision fully local."""
    fact_w = (
        "the registered local sweep over the single registered deployment context shows "
        "strict dominance over the other registered method on the registered criterion"
    )
    fact_l = (
        "the same registered local sweep shows it strictly dominated by the other "
        "registered method on the registered criterion"
    )
    if rng.random() < 0.5:
        reg, winner = _registry(dom["m1"], dom["m2"], fact_w, fact_l), "FIRST"
    else:
        reg, winner = _registry(dom["m2"], dom["m1"], fact_l, fact_w), "SECOND"
    ctx = _ctx_block([
        ("environment_distribution", f"registered deployment environment: {dom['env_a']}"),
        ("task_family", dom["task_family"]),
        ("system_boundary", dom["boundary_closed"]),
        ("scale", dom["scale_small"]),
        ("timescale", dom["t_fast"]),
        ("substrate_interface", "registered benchmark interface, single substrate"),
        ("criterion", "the registered primary criterion (single, commensurate)"),
    ])
    text = (
        f"SETTING: {dom['setting'][0].upper() + dom['setting'][1:]}. You are the "
        "method-selection officer for a SINGLE registered deployment context; the "
        f"decision must be made from the registry below.\n\n{reg}\n\n{ctx}\n\n"
        "ATLAS REGISTRY (local epistemic charts and overlaps):\n"
        "- local chart: chart-L1 over the single registered context (local states: the "
        "method-selection decision and its registered evidence)\n"
        "- overlap assessments: NONE registered (no second context is registered)\n"
        "- global section witness registry: NONE registered\n\n"
        "TRANSPORT PROPOSAL: a review proposes to treat the local selection as holding "
        "across all contexts and to report a witnessed global section for it."
    )
    oracle = _oracle("AHC0", decision=winner)
    oracle["_charts"] = ["chart-L1"]
    return {"scenario_text": text.replace("  ", " "), "coordinate_vocabulary": list(COORDS)}, oracle


def _gen_ahc1(rng, dom):
    """COVER_COMPATIBLE_NO_GLOBAL_WITNESS: charts compatible, no global witness."""
    coord = rng.choice(["environment_distribution", "scale", "timescale"])
    variants = {
        "environment_distribution": (dom["env_a"], dom["env_b"], "mixed reference demand"),
        "scale": (dom["scale_small"], dom["scale_large"], "registered intermediate scale"),
        "timescale": (dom["t_fast"], dom["t_slow"], "budget T = H"),
    }
    a, b, c = variants[coord]
    n = 3 if rng.random() < 0.5 else 2
    charts = [
        f"chart-A (context C-A; {coord}: {a}; task family: {dom['task_family']})",
        f"chart-B (context C-B; {coord}: {b}; task family: {dom['task_family']})",
        f"chart-C (context C-C; {coord}: {c}; task family: {dom['task_family']})",
    ][:n]
    pairs = [("chart-A", "chart-B")] + ([("chart-B", "chart-C"), ("chart-A", "chart-C")] if n == 3 else [])
    overlaps = [
        f"- OVL-{i+1}: {l} vs {r}: COMPATIBLE on the shared task family (matched method "
        f"family on shared local states), witness w-{i+1}"
        for i, (l, r) in enumerate(pairs)
    ]
    text = (
        f"SETTING: {dom['setting'][0].upper() + dom['setting'][1:]}. {n} registered "
        "evaluation campaigns (local charts) cover the task family under different "
        "registered coordinate values; their pairwise compatibility has been assessed.\n\n"
        "CHART REGISTRY:\n" + "\n".join(f"- {c}" for c in charts) + "\n\n"
        "OVERLAP ASSESSMENTS (registered, each with a witness):\n" + "\n".join(overlaps) + "\n\n"
        "GLOBAL SECTION WITNESS REGISTRY: NONE registered (no finding covering ALL the "
        "registered charts exists).\n\n"
        "ATLAS CLAIM UNDER REVIEW: a review claims the compatible overlaps themselves "
        "establish a witnessed global section over the whole family."
    )
    oracle = _oracle("AHC1")
    oracle["_charts"] = [c.split(" ")[0] for c in charts]
    return {"scenario_text": text.replace("  ", " "), "coordinate_vocabulary": list(COORDS)}, oracle


def _gen_ahc2(rng, dom):
    """PROBE_REFINEMENT_REQUIRED: exactly one admissible probe splits the pair."""
    # Current grid: cand-1 and cand-2 merged (decision-distinct), cand-3 separate.
    base = {
        "cand-1": {"p1": "oc-a", "p2": "oc-x"},
        "cand-2": {"p1": "oc-a", "p2": "oc-x"},
        "cand-3": {"p1": "oc-b", "p2": "oc-y"},
    }
    # Proposal outcomes (would-be classes for the new probe):
    props = [
        ("splitter", {"cand-1": "o-alpha", "cand-2": "o-beta", "cand-3": "o-alpha"}),
        ("duplicate-p1", {"cand-1": "oc-a", "cand-2": "oc-a", "cand-3": "oc-b"}),
        ("constant", {"cand-1": "oc-k", "cand-2": "oc-k", "cand-3": "oc-k"}),
    ]
    rng.shuffle(props)
    labels = ["q1", "q2", "q3"]
    lines, adopter = [], ""
    for (kind, mapping), q in zip(props, labels):
        lines.append(
            f"- probe-{q}: registered would-be outcome classes: "
            + "; ".join(f"{c} -> {mapping[c]}" for c in sorted(mapping))
        )
        if kind == "splitter":
            adopter = f"probe-{q}"
            adopter_mapping = mapping
    grid_lines = [
        f"- {c}: " + "; ".join(f"{p}:{v}" for p, v in sorted(base[c].items())) for c in sorted(base)
    ]
    text = (
        f"SETTING: {dom['setting'][0].upper() + dom['setting'][1:]}. A candidate set is "
        "evaluated by registered probes under a bound evaluator; the candidate "
        "deployment consequences are registered and DIFFER between cand-1 and cand-2 "
        "(consequence class D-1 versus D-2: deploying the wrong one is a registered "
        "loss), while cand-3 sits in consequence class D-3.\n\n"
        "CURRENT PROBE TABLE (outcome class under the bound evaluator; the full "
        "candidate-by-probe grid is registered):\n" + "\n".join(grid_lines) + "\n\n"
        "PROPOSED NEW PROBES (at most one will be adopted; each proposal's would-be "
        "outcome classes are registered):\n" + "\n".join(lines) + "\n\n"
        "DECISION REQUIRED: adopt the proposal that restores distinguishability of the "
        "decision-distinct candidates, or reject."
    )
    oracle = _oracle(
        "AHC2",
        probe_decision="ADOPT",
        probe_id=adopter,
        horizon_disposition="PROBE_REFINES_HORIZON",
    )
    oracle["_probe_grid"] = {
        "probes": ["p1", "p2"],
        "outcomes": base,
        "proposals": {f"probe-{q}": m for (k, m), q in zip(props, labels)},
        "adopter": adopter,
        "adopter_mapping": adopter_mapping,
    }
    return {"scenario_text": text.replace("  ", " "), "coordinate_vocabulary": list(COORDS)}, oracle


def _gen_ahc3(rng, dom):
    """PROBE_REDUNDANT: the proposal is a deterministic function of existing probes."""
    mode = rng.choice(["duplicate", "constant"])
    base = {
        "cand-1": {"p1": "oc-a", "p2": "oc-x"},
        "cand-2": {"p1": "oc-a", "p2": "oc-x"},
        "cand-3": {"p1": "oc-b", "p2": "oc-y"},
    }
    if mode == "duplicate":
        mapping = {"cand-1": "oc-x", "cand-2": "oc-x", "cand-3": "oc-y"}
        dep = "its outcome class duplicates probe p2's outcome class for every candidate"
    else:
        mapping = {"cand-1": "oc-k", "cand-2": "oc-k", "cand-3": "oc-k"}
        dep = "its outcome class is the constant class oc-k for every candidate"
    grid_lines = [
        f"- {c}: " + "; ".join(f"{p}:{v}" for p, v in sorted(base[c].items())) for c in sorted(base)
    ]
    text = (
        f"SETTING: {dom['setting'][0].upper() + dom['setting'][1:]}. A candidate set is "
        "evaluated by registered probes under a bound evaluator.\n\n"
        "CURRENT PROBE TABLE (outcome class under the bound evaluator; the full "
        "candidate-by-probe grid is registered):\n" + "\n".join(grid_lines) + "\n\n"
        "PROPOSED NEW PROBE probe-q1 (cheap to run and previously successful on a "
        f"neighbouring family): {dep}.\n\n"
        "DECISION REQUIRED: adopt probe-q1 or reject it."
    )
    oracle = _oracle(
        "AHC3",
        probe_decision="REJECT",
        probe_id="probe-q1",
        horizon_disposition="NO_DISTINGUISHABILITY_GAIN",
    )
    oracle["_probe_grid"] = {
        "probes": ["p1", "p2"],
        "outcomes": base,
        "proposals": {"probe-q1": mapping},
        "adopter": None,
    }
    return {"scenario_text": text.replace("  ", " "), "coordinate_vocabulary": list(COORDS)}, oracle


def _gen_ahc4(rng, dom):
    """OUTSIDE_ATLAS_SENTINEL: witnessed residual after every lower explanation."""
    lowers = [
        ("KNOWN_UNCERTAINTY", "w-ku-1"),
        ("MODEL_FAMILY_INSUFFICIENCY", "w-mf-1"),
        ("REPRESENTATION_INSUFFICIENCY", "w-ri-1"),
        ("PROBE_OR_ACTION_INSUFFICIENCY", "w-pa-1"),
        ("CONTEXT_SCALE_BOUNDARY_INSUFFICIENCY", "w-cs-1"),
    ]
    k = 3 + rng.randrange(3)
    chosen = lowers[:k]
    text = (
        f"SETTING: {dom['setting'][0].upper() + dom['setting'][1:]}. After a multi-campaign "
        "evaluation the local charts are pairwise compatible on their overlaps, but a "
        "decision-relevant residual persists.\n\n"
        "CHART REGISTRY:\n"
        "- chart-A (campaign A over the task family)\n"
        "- chart-B (campaign B over the task family)\n\n"
        "OVERLAP ASSESSMENTS (registered, with witnesses):\n"
        "- OVL-1: chart-A vs chart-B: COMPATIBLE (matched method family on shared local "
        "states), witness w-ovl-1\n\n"
        "GLOBAL SECTION WITNESS REGISTRY: NONE registered.\n\n"
        "RESIDUAL DISPOSITION LEDGER (registered attempts, each with a witness):\n"
        + "\n".join(
            f"- {name}: applied to the residual and does NOT dispose it (witness {w})"
            for name, w in chosen
        )
        + "\n- residual R-1: decision-relevant, persists after every registered "
        "disposition above (witness w-resid-1)\n\n"
        "HORIZON QUESTION: a review asks whether the residual is outside the current "
        "atlas, and if so with what witness. No mechanism content is registered for it."
    )
    oracle = _oracle(
        "AHC4",
        horizon_disposition="OUTSIDE_CURRENT_ATLAS",
        outside_atlas_witness_id="w-resid-1",
    )
    oracle["_residual_witness"] = "w-resid-1"
    return {"scenario_text": text.replace("  ", " "), "coordinate_vocabulary": list(COORDS)}, oracle


_GENERATORS = {
    "AHC0": _gen_ahc0,
    "AHC1": _gen_ahc1,
    "AHC2": _gen_ahc2,
    "AHC3": _gen_ahc3,
    "AHC4": _gen_ahc4,
}


def generate_ah_case(rng, cls):
    """Return (public_task_dict, private_oracle_dict) for one seeded AH case."""
    return _GENERATORS[cls](rng, _domain(rng))


# ---------------------------------------------------------------------------
# Machine cross-checks: the AH10-green module is the oracle generator, so
# every expected answer is re-derived by calling the real implementation.
# ---------------------------------------------------------------------------

GLUING_FIELDS = (
    "decision",
    "holds_across_contexts",
    "gluing_disposition",
    "global_section_witness_id",
    "transport_verdict",
    "probe_decision",
    "probe_id",
    "horizon_disposition",
    "outside_atlas_witness_id",
)


def _chart(cid):
    return LocalEpistemicChart(cid, f"ctx-{cid}", (f"state-{cid}-1", f"state-{cid}-2"))


def _overlap(oid, left, right, compatible):
    return OverlapAssessment(
        oid,
        left,
        right,
        compatible,
        witness_ids=(f"w-{oid}",) if compatible is not None else (),
    )


def _module_gluing(chart_ids, overlap_specs, witness=""):
    """Run assess_atlas_gluing on a synthetic minimal atlas; return status."""
    charts = tuple(_chart(c) for c in chart_ids)
    overlaps = tuple(_overlap(o, l, r, comp) for (o, l, r, comp) in overlap_specs)
    return assess_atlas_gluing(charts, overlaps, global_section_witness_id=witness).status.value


def _probe_outcomes(grid):
    """grid: {candidate: {probe: outcome_class}} -> full ProbeOutcome grid."""
    return tuple(
        ProbeOutcome(probe, cand, oc)
        for cand in sorted(grid)
        for probe, oc in sorted(grid[cand].items())
    )


def _after_grid(grid, probe_id, mapping):
    after = {cand: dict(probes) for cand, probes in grid.items()}
    for cand in after:
        after[cand][probe_id] = mapping[cand]
    return after


def _check_gluing(oracle):
    """Re-derive the expected gluing disposition from the module."""
    status = oracle["gluing_disposition"]
    witness = oracle["global_section_witness_id"]
    cls = oracle["class_id"]
    if cls == "AHC0":
        got = _module_gluing(["chart-L1"], [])
    elif cls == "AHC1":
        charts = oracle["_charts"]
        pairs = [
            (f"OVL-{i + 1}", l, r, True)
            for i, (l, r) in enumerate(zip(charts, charts[1:]))
        ]
        got = _module_gluing(charts, pairs)
    elif cls == "AHC4":
        got = _module_gluing(
            ["chart-A", "chart-B"], [("OVL-1", "chart-A", "chart-B", True)]
        )
    elif cls.startswith("ELC"):
        if cls == "ELC1":
            got = _module_gluing(
                ["C-1", "C-2", "C-3"],
                [("OVL-12", "C-1", "C-2", True), ("OVL-23", "C-2", "C-3", True)],
                witness="full-envelope-sweep",
            )
        elif cls == "ELC7":
            got = _module_gluing(
                ["C-1", "C-2"], [("OVL-12", "C-1", "C-2", None)]
            )
        else:
            got = _module_gluing(
                ["C-1", "C-2"], [("OVL-12", "C-1", "C-2", False)]
            )
    else:
        return  # AHC2/AHC3 carry no atlas gluing content
    assert got == status, f"gluing cross-check failed for {cls}: module={got} oracle={status}"


def _check_probe(oracle):
    """Re-derive probe/horizon expectations via assess_probe_expansion."""
    if oracle["class_id"] not in ("AHC2", "AHC3"):
        assert oracle["probe_decision"] == "NONE"
        assert oracle["probe_id"] == ""
        if oracle["class_id"] != "AHC4":
            assert oracle["horizon_disposition"] == "NOT_APPLICABLE"
        else:
            assert oracle["horizon_disposition"] == "OUTSIDE_CURRENT_ATLAS"
        return
    meta = oracle["_probe_grid"]
    before = _probe_outcomes(meta["outcomes"])
    if oracle["class_id"] == "AHC2":
        # The adopter must strictly refine; every decoy must not.
        for probe_id, mapping in meta["proposals"].items():
            after = _probe_outcomes(_after_grid(meta["outcomes"], probe_id, mapping))
            got = assess_probe_expansion(before, after).status.value
            if probe_id == meta["adopter"]:
                assert got == "PROBE_REFINES_HORIZON", (probe_id, got)
            else:
                assert got == "NO_DISTINGUISHABILITY_GAIN", (probe_id, got)
        assert oracle["probe_decision"] == "ADOPT"
        assert oracle["probe_id"] == meta["adopter"]
        assert oracle["horizon_disposition"] == "PROBE_REFINES_HORIZON"
        # The refinement must split exactly the decision-distinct pair.
        before_part = observational_partition(before)
        after_part = observational_partition(
            _probe_outcomes(
                _after_grid(meta["outcomes"], meta["adopter"], meta["adopter_mapping"])
            )
        )
        assert is_strict_partition_refinement(after_part, before_part)
        assert {
            block for block in after_part if len(block) == 1
        } >= {("cand-1",), ("cand-2",)}
    else:
        probe_id, mapping = next(iter(meta["proposals"].items()))
        after = _probe_outcomes(_after_grid(meta["outcomes"], probe_id, mapping))
        got = assess_probe_expansion(before, after).status.value
        assert got == "NO_DISTINGUISHABILITY_GAIN", got
        assert oracle["probe_decision"] == "REJECT"
        assert oracle["probe_id"] == probe_id
        assert oracle["horizon_disposition"] == "NO_DISTINGUISHABILITY_GAIN"


def _check_sentinel(oracle):
    """OUTSIDE_CURRENT_ATLAS must construct as a witnessed UnknownRecord."""
    if oracle["class_id"] != "AHC4":
        assert oracle["horizon_disposition"] != "OUTSIDE_CURRENT_ATLAS"
        assert oracle["outside_atlas_witness_id"] == ""
        return
    record = UnknownRecord(
        "R-1",
        UnknownKind.OUTSIDE_CURRENT_ATLAS,
        (oracle["outside_atlas_witness_id"],),
    )
    assert record.kind.value == "OUTSIDE_CURRENT_ATLAS"
    assert oracle["horizon_disposition"] == "OUTSIDE_CURRENT_ATLAS"
    assert oracle["outside_atlas_witness_id"].strip()


def verify_oracle(task_id, oracle):
    _check_gluing(oracle)
    _check_probe(oracle)
    _check_sentinel(oracle)
    for field in ("decision", "transport_verdict"):
        assert oracle[field], (task_id, field)


# ---------------------------------------------------------------------------
# EL10 exact reuse: re-derive all 48 worlds under EL10's own seed and assert
# byte-equality against the committed records before extending the oracle.
# ---------------------------------------------------------------------------


def _el10_committed():
    tasks = json.loads((EL10_RESULTS / "public_tasks.json").read_text())
    scoring = json.loads((EL10_RESULTS / "PER_TASK_SCORING.json").read_text())
    committed = {t["task_id"]: t for t in tasks["tasks"]}
    return committed, scoring["oracle"]


EL10_ORACLE_FIELDS = (
    "class_id",
    "decision",
    "holds_across_contexts",
    "perspective_dependent_coordinates",
    "comparison_valid",
    "transport_verdict",
)


def el10_reuse_rows():
    """Return [(public_task, oracle_row)] for the 48 EL10 worlds, verified equal."""
    committed, committed_oracle = _el10_committed()
    rng = random.Random(EL10_SEED)
    rows = []
    for cls in EL10_CLASSES:
        for index in range(PER_CLASS):
            case_rng = random.Random(rng.getrandbits(64))
            public, oracle = el10_generate_case(case_rng, cls)
            task_id = f"el10-{cls.lower()}-{index + 1:02d}"
            assert task_id in committed, f"missing committed EL10 task {task_id}"
            source = committed[task_id]
            assert public["scenario_text"] == source["scenario_text"], task_id
            assert public["coordinate_vocabulary"] == source["coordinate_vocabulary"], task_id
            for field in EL10_ORACLE_FIELDS:
                assert oracle[field] == committed_oracle[task_id][field], (task_id, field)
            gluing, witness = EL10_GLUING[cls]
            row = {
                "task_id": task_id,
                "class_id": cls,
                "decision": oracle["decision"],
                "holds_across_contexts": oracle["holds_across_contexts"],
                "gluing_disposition": gluing,
                "global_section_witness_id": witness,
                "transport_verdict": oracle["transport_verdict"],
                "probe_decision": "NONE",
                "probe_id": "",
                "horizon_disposition": "NOT_APPLICABLE",
                "outside_atlas_witness_id": "",
            }
            rows.append(({"task_id": task_id, **public}, row))
    return rows


def ah20_rows():
    """Return [(public_task, oracle_row)] for the 30 new seeded AH worlds."""
    rng = random.Random(AH_SEED)
    rows = []
    for cls in AH_CLASSES:
        for index in range(PER_CLASS):
            case_rng = random.Random(rng.getrandbits(64))
            public, oracle = generate_ah_case(case_rng, cls)
            task_id = f"ah20-{cls.lower()}-{index + 1:02d}"
            row = {"task_id": task_id}
            row.update(oracle)
            rows.append(({"task_id": task_id, **public}, row))
    return rows


def build_suite():
    """Return (public_tasks, oracle_rows) for all 78 tasks: EL10 reuse first."""
    reused = el10_reuse_rows()
    fresh = ah20_rows()
    public = [p for p, _ in reused + fresh]
    oracle_rows = [o for _, o in reused + fresh]
    return public, oracle_rows


GLUING_BALANCE = {
    "MATCHING_FAMILY_ONLY": 30,
    "GLOBAL_SECTION_OBSTRUCTED": 36,
    "GLOBAL_SECTION_WITNESSED": 6,
    "CANNOT_CHECK": 6,
}

_ENUM_LEAKS = (
    "GLOBAL_SECTION_WITNESSED",
    "MATCHING_FAMILY_ONLY",
    "GLOBAL_SECTION_OBSTRUCTED",
    "CANNOT_CHECK",
    "PROBE_REFINES_HORIZON",
    "NO_DISTINGUISHABILITY_GAIN",
    "BROKEN_CANDIDATE_UNIVERSE",
    "OUTSIDE_CURRENT_ATLAS",
    "NOT_APPLICABLE",
)


def verify_suite(public, oracle_rows):
    """Structural audit: exactness, balance, witness discipline, no leaks."""
    assert len(public) == len(oracle_rows) == 78
    ids = [t["task_id"] for t in public]
    assert len(set(ids)) == 78, "task ids must be unique"
    counts = {}
    gluing_counts = {}
    for task, oracle in zip(public, oracle_rows):
        assert task["task_id"] == oracle["task_id"]
        counts[oracle["class_id"]] = counts.get(oracle["class_id"], 0) + 1
        gluing_counts[oracle["gluing_disposition"]] = (
            gluing_counts.get(oracle["gluing_disposition"], 0) + 1
        )
        # Cross-check against the AH10-green module (underscore keys are the
        # cross-check basis and live only in the private oracle).
        verify_oracle(task["task_id"], oracle)
        # Witness-id discipline (module-mirrored).
        witnessed = oracle["gluing_disposition"] == "GLOBAL_SECTION_WITNESSED"
        assert bool(oracle["global_section_witness_id"].strip()) == witnessed, task["task_id"]
        outside = oracle["horizon_disposition"] == "OUTSIDE_CURRENT_ATLAS"
        assert bool(oracle["outside_atlas_witness_id"].strip()) == outside, task["task_id"]
        # No class identity, no enum value, no oracle token leaks into public text.
        text = task["scenario_text"]
        assert "AHC" not in text and "ELC" not in text, task["task_id"]
        for leak in _ENUM_LEAKS:
            assert leak not in text, (task["task_id"], leak)
    expected_counts = {f"ELC{i}": 6 for i in range(1, 9)}
    expected_counts.update({cls: 6 for cls in AH_CLASSES})
    assert counts == expected_counts, counts
    assert gluing_counts == GLUING_BALANCE, gluing_counts
    return {"tasks": len(public), "classes": counts, "gluing": gluing_counts}


def main():
    public, oracle_rows = build_suite()
    report = verify_suite(public, oracle_rows)
    print(json.dumps(report, indent=2, sort_keys=True))
    print("AH20 CASES OK")


if __name__ == "__main__":
    main()

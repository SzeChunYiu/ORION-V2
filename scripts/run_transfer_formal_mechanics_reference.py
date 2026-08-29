#!/usr/bin/env python3
"""Run non-scientific exact-oracle calibration for transfer formal mechanics.

This script validates benchmark/reference semantics only.  It does not call a
model arm and cannot support an ORION superiority or publication claim.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from orion_v2.transfer_formal_mechanics import (
    FiniteCategory,
    FiniteRelationalStructure,
    FormalContext,
    FormalTransferMap,
    FunctorCandidate,
    TransformationCase,
    TypedFact,
    assess_functor,
    assess_invariance,
    assess_partial_homomorphism,
    enumerate_type_respecting_node_maps,
    formal_concept_closure,
)


def relational_calibration() -> dict:
    donor = FiniteRelationalStructure(
        "donor-chain", "mathematics",
        ("a", "b", "c"),
        (("a", "start"), ("b", "middle"), ("c", "end")),
        (
            TypedFact("r", "DIRECTED", ("a", "b")),
            TypedFact("r", "DIRECTED", ("b", "c")),
        ),
        ("chain-order",),
    )
    target = FiniteRelationalStructure(
        "target-chain", "science",
        ("x", "y", "z"),
        (("x", "end"), ("y", "start"), ("z", "middle")),
        (
            TypedFact("q", "DIRECTED", ("y", "z")),
            TypedFact("q", "DIRECTED", ("z", "x")),
        ),
        ("ordered-process",),
    )
    hidden = FormalTransferMap(
        (("a", "y"), ("b", "z"), ("c", "x")),
        (("r", "q"),),
        invariant_map=(("chain-order", "ordered-process"),),
    )
    valid = assess_partial_homomorphism(donor, target, hidden)

    reversed_target = FiniteRelationalStructure(
        "target-reversed", "science",
        target.nodes, target.node_types,
        (
            TypedFact("q", "DIRECTED", ("z", "y")),
            TypedFact("q", "DIRECTED", ("x", "z")),
        ),
        target.invariant_ids,
    )
    invalid = assess_partial_homomorphism(donor, reversed_target, hidden)
    candidate_maps = enumerate_type_respecting_node_maps(donor, target)
    return {
        "hidden_mapping_valid": valid.critical_valid,
        "hidden_mapping_relation_rate": valid.relation_preservation_rate,
        "reversed_mapping_rejected": not invalid.critical_valid,
        "type_respecting_map_count": len(candidate_maps),
    }


def fca_calibration() -> dict:
    context = FormalContext(
        objects=("o1", "o2", "o3"),
        attributes=("a", "b", "c"),
        incidence=frozenset({
            ("o1", "a"), ("o1", "b"),
            ("o2", "a"), ("o2", "b"), ("o2", "c"),
            ("o3", "a"), ("o3", "c"),
        }),
    )
    extent, intent = formal_concept_closure(context, attributes=("b",))
    return {
        "extent": sorted(extent),
        "intent": sorted(intent),
        "closure_expected": extent == frozenset({"o1", "o2"}) and intent == frozenset({"a", "b"}),
    }


def walking_arrow(prefix: str) -> FiniteCategory:
    a, b = prefix + "A", prefix + "B"
    ida, idb, f = "id" + a, "id" + b, prefix + "f"
    return FiniteCategory(
        (a, b), (ida, idb, f),
        ((ida, a, a), (idb, b, b), (f, a, b)),
        ((a, ida), (b, idb)),
        ((ida, ida, ida), (idb, idb, idb), (ida, f, f), (f, idb, f)),
    )


def functor_calibration() -> dict:
    donor, target = walking_arrow("D"), walking_arrow("T")
    good = assess_functor(
        donor, target,
        FunctorCandidate(
            (("DA", "TA"), ("DB", "TB")),
            (("idDA", "idTA"), ("idDB", "idTB"), ("Df", "Tf")),
        ),
    )
    bad = assess_functor(
        donor, target,
        FunctorCandidate(
            (("DA", "TA"), ("DB", "TB")),
            (("idDA", "idTA"), ("idDB", "idTB"), ("Df", "idTA")),
        ),
    )
    return {
        "valid_functor_accepted": good.valid,
        "invalid_functor_rejected": not bad.valid,
        "invalid_endpoint_violations": bad.endpoint_violations,
    }


def invariance_calibration() -> dict:
    cases = tuple(
        TransformationCase(f"swap-{i}", (i, i + 3), (i + 3, i), "swap")
        for i in range(1, 9)
    )
    invariant = assess_invariance(cases, lambda pair: pair[0] + pair[1])
    non_invariant = assess_invariance(cases, lambda pair: pair[0])
    equivariant = assess_invariance(
        cases,
        lambda pair: pair[0] - pair[1],
        output_transform=lambda transform, value: -value if transform == "swap" else value,
    )
    return {
        "true_invariant_rate": invariant.rate,
        "false_invariant_rate": non_invariant.rate,
        "true_equivariant_rate": equivariant.rate,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("transfer_formal_reference_receipt.json"))
    args = parser.parse_args()

    receipt = {
        "schema_version": "orion.v2.transfer-formal-reference-calibration.v1",
        "status": "REFERENCE_SEMANTICS_CALIBRATION_ONLY",
        "relational": relational_calibration(),
        "formal_concept_analysis": fca_calibration(),
        "functoriality": functor_calibration(),
        "invariance": invariance_calibration(),
        "authority": {
            "scientific_truth": False,
            "F2_superiority": False,
            "field_status": False,
            "submission_readiness": False,
        },
    }
    required = (
        receipt["relational"]["hidden_mapping_valid"],
        receipt["relational"]["reversed_mapping_rejected"],
        receipt["formal_concept_analysis"]["closure_expected"],
        receipt["functoriality"]["valid_functor_accepted"],
        receipt["functoriality"]["invalid_functor_rejected"],
        receipt["invariance"]["true_invariant_rate"] == 1.0,
        receipt["invariance"]["true_equivariant_rate"] == 1.0,
        receipt["invariance"]["false_invariant_rate"] < 1.0,
    )
    receipt["all_reference_checks_pass"] = all(required)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    raise SystemExit(0 if receipt["all_reference_checks_pass"] else 1)


if __name__ == "__main__":
    main()

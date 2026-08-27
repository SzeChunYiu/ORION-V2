from orion_v2.donors import DomainProblem, DonorDisposition, DonorReductionCase, reduce_donors

def _donor() -> DomainProblem:
    return DomainProblem("problem:bisimulation", "computer-science", "determine behavioural equivalence under labelled transitions", ("source:milner",), ("transition-system",), ("state",), ("match-transition",), ("judgment:bisimilar",))

def test_absorbed_special_case_contracts_candidate() -> None:
    case = DonorReductionCase("case", "candidate:generic-behavioural-equivalence", (_donor(),), ("receipt:native",), ("map:embed",), ("judgment:bisimilar",))
    assert reduce_donors(case).disposition is DonorDisposition.ABSORBED_SPECIAL_CASE

def test_strict_candidate_requires_donor_product_and_falsifier() -> None:
    case = DonorReductionCase("case", "candidate:context-authority-equivalence", (_donor(),), ("receipt:native",), ("map:embed",), ("judgment:bisimilar",), added_coordinate_ids=("authority",), strict_witness_ids=("witness:authority-difference",), strongest_product_test_ids=("test:ideal-product",), strongest_product_ties=False, falsifier_ids=("falsifier:parent-can-express-authority",))
    assert reduce_donors(case).disposition is DonorDisposition.CANDIDATE_STRICT_RESIDUAL

def test_donor_product_tie_blocks_residual() -> None:
    case = DonorReductionCase("case", "candidate", (_donor(),), ("receipt",), ("map",), ("judgment:bisimilar",), added_coordinate_ids=("coordinate",), strict_witness_ids=("witness",), strongest_product_test_ids=("test",), strongest_product_ties=True)
    assert reduce_donors(case).disposition is DonorDisposition.IDEAL_DONOR_PRODUCT_EQUIVALENCE

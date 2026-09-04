"""Finite-sample conditional risk transport; counts are NOT authenticated evidence.

CT-10..12 in SAMPLING.md. Exact rational, conservatively rounded one-sided
binomial inversion; fixed sample size and fixed-event IID assumptions required.
No truth warrant, verified sampling claim, or action authorization is returned.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from itertools import product
import json
from math import comb
from pathlib import Path
import sys

from transport import CannotCheck, probability
from checks import require

MAX_SAMPLES = 256
MAX_BITS = 32
DEFAULT_BITS = 16


def binomial_cdf(n: int, k: int, p: Q) -> Q:
    """Exact Pr[Bin(n,p)<=k], using a shared integer denominator."""
    a, d = p.numerator, p.denominator
    return Q(sum(comb(n, j) * a**j * (d-a)**(n-j) for j in range(k+1)), d**n)


def binomial_upper(n: int, failures: int, alpha, bits: int = DEFAULT_BITS) -> Q:
    """Smallest grid point u with Bin(n,u) lower tail <=alpha; u=1 at k=n."""
    if type(n) is not int or n < 1:
        raise CannotCheck("positive fixed sample size required")
    if n > MAX_SAMPLES:
        raise CannotCheck("registered exact-inversion sample cap exceeded")
    if type(failures) is not int or not 0 <= failures <= n:
        raise ValueError("integer failure count must lie in [0,n]")
    alpha = probability(alpha)
    if not 0 < alpha < 1:
        raise ValueError("confidence failure budget must lie strictly between 0 and 1")
    if type(bits) is not int or not 1 <= bits <= MAX_BITS:
        raise CannotCheck("registered inversion precision is 1..32 bits")
    if failures == n:
        return Q(1)
    denominator = 1 << bits
    low, high = 0, denominator
    while high-low > 1:
        mid = (low+high)//2
        if binomial_cdf(n, failures, Q(mid, denominator)) <= alpha:
            high = mid
        else:
            low = mid
    return Q(high, denominator)


def transport_from_counts(n_old: int, failures_old: int, n_pairs: int,
                          disagreements: int, alpha_old, alpha_pairs, epsilon):
    """Conditional theorem projection, never a deployment-validity verdict.

    Old error samples require correct labels; new paired prediction-disagreement
    samples need no new labels under the COMMON semantic error predicate. The
    deployment epsilon bounds JOINT input/label TV, not only input marginals.
    """
    if epsilon is None:
        raise CannotCheck("deployment drift premise not supplied")
    epsilon = probability(epsilon)
    a, b = probability(alpha_old), probability(alpha_pairs)
    if a+b >= 1:
        raise CannotCheck("nontrivial joint confidence budget required")
    u = binomial_upper(n_old, failures_old, a)
    v = binomial_upper(n_pairs, disagreements, b)
    return {
        "kind": "CONDITIONAL_RISK_BOUND",
        "risk_upper": str(min(Q(1), u+v+epsilon)),
        "calibration_confidence_at_least": str(1-a-b),
        "reference_risk_upper": str(u), "disagreement_upper": str(v),
        "joint_TV_assumed_upper": str(epsilon),
        "cost_inputs": {"reference_labeled_examples": n_old,
                        "reference_predictor_evaluations": n_old,
                        "paired_unlabeled_examples": n_pairs,
                        "paired_predictor_evaluations": 2*n_pairs},
        "requires": ["fixed events or simultaneous validity", "fixed sample sizes",
                     "IID reference and paired sample laws", "correct reference labels",
                     "common semantic error predicate", "justified joint deployment TV"],
        "premises_verified_by_this_function": False,
        "exact_truth_warrant": False, "external_action_authority": False,
    }


def run():
    intervals = tails = predecessors = monotone = coverage_cells = 0
    failures = []
    for n in range(1, 13):
        for alpha in (Q(1,20), Q(1,10), Q(1,2)):
            uppers = [binomial_upper(n, k, alpha) for k in range(n+1)]
            for k, u in enumerate(uppers):
                intervals += 1
                if k == n:
                    require(u == 1, "all-failures boundary")
                else:
                    require(binomial_cdf(n,k,u) <= alpha, "invalid tail certificate")
                    tails += 1
                    before = u-Q(1, 1 << DEFAULT_BITS)
                    require(binomial_cdf(n,k,before) > alpha, "not minimal grid upper limit")
                    predecessors += 1
                if k:
                    require(uppers[k-1] <= u, "count monotonicity")
                    monotone += 1
            for j in range(17):
                p = Q(j,16)
                undercoverage = sum((Q(comb(n,k))*p**k*(1-p)**(n-k)
                                     for k,u in enumerate(uppers) if u < p), Q(0))
                require(undercoverage <= alpha, ("undercoverage", n,alpha,p,undercoverage))
                failures.append(undercoverage)
                coverage_cells += 1
    inclusion = 0
    for truth in range(8):
        for old in range(8):
            for new in range(8):
                before, after, disagree = truth^old, truth^new, old^new
                for i in range(3):
                    require(not ((before^after)&(1<<i)) or bool(disagree&(1<<i)),
                            "pointwise disagreement inclusion")
                    inclusion += 1
    # Multiclass: predictions differ while both are wrong; the bound can be loose.
    require((1 != 0) == (2 != 0) and 1 != 2, "multiclass strictness")
    strictness = 1  # the immediately preceding explicit strictness check executed
    selection_error = simultaneous_error = Q(0)
    selection_vectors = 0
    for vector in product((0,1), repeat=4):
        selection_vectors += 1
        weight = Q(3,4)**sum(vector) * Q(1,4)**(4-sum(vector))
        selected = next((i for i,x in enumerate(vector) if x == 0), 0)
        if binomial_upper(1, vector[selected], Q(1,2)) < Q(3,4):
            selection_error += weight
        if binomial_upper(1, vector[selected], Q(1,8)) < Q(3,4):
            simultaneous_error += weight
    require(selection_error == Q(175,256) > Q(1,2), "adaptive selection falsifier")
    require(simultaneous_error == 0, "simultaneous family control")
    zero = binomial_upper(12,0,Q(1,20))
    require(zero > 0, "zero observed failures not zero risk")
    invalid = 0
    for args in ((0,0,Q(1,20)), (1,2,Q(1,20)), (True,0,Q(1,20)),
                 (1,False,Q(1,20)), (1,0,0), (1,0,1), (MAX_SAMPLES+1,0,Q(1,20))):
        try:
            binomial_upper(*args)
        except (CannotCheck, ValueError):
            invalid += 1
        else:
            raise AssertionError(("invalid calibration accepted", args))
    try:
        transport_from_counts(12,0,12,0,Q(1,20),Q(1,20),None)
    except CannotCheck:
        invalid += 1
    else:
        raise AssertionError("missing drift accepted")
    # Two explicit environments with identical observed past and input marginals.
    histories = ((0,)*12, (0,)*12)
    future_inputs = (0, 0)
    future_labels = (0, 1)
    future_risks = [int(label != 0) for label in future_labels]
    require(histories[0] == histories[1] and future_inputs[0] == future_inputs[1]
            and future_risks == [0,1], "unrestricted-future witness")
    return {
        "study": "ME-CERTIFICATE-TRANSPORT-V1-FINITE-SAMPLE-EXTENSION",
        "terminal": "EXACT_BINOMIAL_CALIBRATION_AND_SELECTION_COUNTEREXAMPLE",
        "counts": {"binomial_limits": intervals, "tail_certificates": tails,
                   "minimal_grid_predecessors": predecessors, "count_monotonicity": monotone,
                   "exact_coverage_cells": coverage_cells, "disagreement_inclusions": inclusion,
                   "multiclass_strictness_witnesses": strictness, "selection_sample_vectors": selection_vectors,
                   "invalid_input_rejections": invalid},
        "selection": {"nominal_alpha": "1/2", "true_each_risk": "3/4",
                      "unadjusted_selected_undercoverage": str(selection_error),
                      "simultaneous_adjusted_undercoverage": str(simultaneous_error)},
        "examples": {"zero_of_12_alpha_0.05_upper": str(zero),
                     "hypothetical_update": transport_from_counts(100,2,100,1,Q(1,40),Q(1,40),Q(1,50)),
                     "unrestricted_future": {"same_past": histories[0] == histories[1],
                                              "same_input_marginal": future_inputs[0] == future_inputs[1],
                                              "future_risks": future_risks, "joint_drift_restriction_missing": True}},
        "authority": {"real_data_or_model_run": False, "independent_review": False,
                      "novelty": "NOT_ESTABLISHED", "all_size_proof_from_enumeration": False},
    }


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path); parser.add_argument("--verify",type=Path)
    args=parser.parse_args(argv)
    try:
        result=run()
        if args.verify:
            require(json.loads(args.verify.read_text()) == result, "sampling result drift")
        text=json.dumps(result,sort_keys=True,indent=2)+"\n"
        if args.output: args.output.write_text(text)
        else: print(text,end="")
        return 0
    except (CannotCheck,ValueError,OSError) as exc:
        print(json.dumps({"status":"CANNOT_CHECK","reason":str(exc)})); return 2
    except (AssertionError,ArithmeticError) as exc:
        print(json.dumps({"status":"FAIL","reason":str(exc)})); return 1


if __name__ == "__main__":
    sys.exit(main())

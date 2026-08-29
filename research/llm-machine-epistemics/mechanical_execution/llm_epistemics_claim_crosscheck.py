#!/usr/bin/env python3
"""Claim-receipt cross-check: CLAIM_LEDGER_V4 C01-C18 vs mechanical receipts.

Spec V4 executor role (metadata + rendering with validation). For every ledger
claim this script asserts the mechanical evidence actually recorded in out/:

- MECHANICALLY_VERIFIED: cited receipt check re-read and verdict confirmed.
- CONSISTENT_PARENT_OWNED: parent-owned claim; receipts only instantiate it
  (instantiation evidence still re-verified where it exists).
- NOT_MECHANICALLY_BACKED: no receipt in the corpus backs the claim (honest
  gap, reported to the theory lane; does NOT fail the run).

Also validates the ledger itself: unknown claim IDs or status drift between
this script's frozen snapshot and CLAIM_LEDGER_V4.json FAILs the run, so the
map cannot silently go stale.

Exit 0 iff no validation failed. Output: out/CLAIM_RECEIPT_CROSSCHECK_V1.json
(+ .md table).
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
LEDGER = HERE.parents[2] / "papers" / "llm-machine-epistemics" / "CLAIM_LEDGER_V4.json"


def load(name):
    with open(OUT / name) as fh:
        return json.load(fh)


def verdict_is(key, want="PASS"):
    def fn(rec):
        v = (rec.get("verdicts") or {}).get(key)
        return v == want
    return fn


def fixture_by_name(rec, name, sub=None):
    fxs = rec.get("fixtures") if sub is None else (rec.get(sub) or {}).get("fixtures")
    for f in fxs or []:
        if f.get("machine", {}).get("name") == name:
            return f
    return None


def c04(rec):
    """Cross-channel static cost witness: P1 fixture has C_stat^* = 1 bit > 0."""
    f = fixture_by_name(rec, "P1_STATIC_CROSS_CHANNEL", sub="j4_j5")
    return bool(f) and f["c_stat_star"]["bits"] == "1"


def c05(rec):
    """Zero-cost control: R27 PASS and P0 fixture C_stat^* = 0."""
    f = fixture_by_name(rec, "P0_PREDICTIVE_DECISIONAL", sub="j4_j5")
    sel = load("RESPONSIBILITY_SELECTOR_AUDIT_V1.json")
    r27 = (sel.get("verdicts") or {}).get("R27_ZERO_COST_COMMON_OPTIMAL_ACTION")
    return r27 == "PASS" and bool(f) and f["c_stat_star"]["bits"] == "0"


def c12(rec):
    for f in (rec.get("j4_j5") or {}).get("fixtures") or []:
        if f.get("check") == "J5" and f.get("expr_equal_expected") is True:
            e, o = f["expected"], f["observed"]
            return (e["c_stat_bits"], e["c_dyn_bits"], e["omega_bits"]) == \
                   (o["c_stat_bits"], o["c_dyn_bits"], o["omega_bits"]) == ("0", "1", "1")
    return False


def c13(rec):
    names = {f.get("machine", {}).get("name") for f in rec.get("fixtures") or []}
    want = {"P0_PREDICTIVE_DECISIONAL", "P1_STATIC_CROSS_CHANNEL", "P2_PROSPECTIVE_REFINEMENT"}
    return want <= names and all(f.get("verdict") == "PASS" for f in rec["fixtures"]
                                 if f.get("machine", {}).get("name") in want)


def c14(rec):
    fxs = rec.get("fixtures") or []
    mono = len(fxs) >= 6 and all(f.get("ph1_monotone") is True for f in fxs)
    stab = all((f.get("curve") or [{}])[-1].get("bits") == f.get("c_inf", {}).get("bits")
               and f.get("literal_equals_iterative_k") is True for f in fxs)
    return mono and stab


def c17(rec):
    vs = rec.get("verdicts") or {}
    return all(vs.get(k) == "PASS" for k in
               ["U1_SANDWICH", "U2_SEPARATING", "U3_COLLIDED_PAIR_ERROR",
                "U4_FULL_HISTORY_ZERO_ERROR", "U5_NESTED_MONOTONE"])


def j2_all(rec):
    fxs = rec.get("fixtures") or []
    return len(fxs) == 5 and all(f.get("impl_equivalence_direction") == "PASS" for f in fxs)


def j3_all(rec):
    fxs = rec.get("fixtures") or []
    return len(fxs) == 5 and all(f.get("j3_expr_equal") is True for f in fxs)


def j4_all(rec):
    rows = [f for f in (rec.get("j4_j5") or {}).get("fixtures") or [] if "omega_dyn" in f]
    canon = [f for f in (rec.get("j4_j5") or {}).get("fixtures") or [] if f.get("check") == "J5"]
    return (len(rows) >= 5
            and all(f["omega_dyn"].get("nonnegative") is True for f in rows)
            and all(f.get("expr_equal_expected") is True for f in canon)
            and bool((rec.get("tie_search") or {}).get("verdict") == "PASS"))


def static_formulation(rec):
    vs = rec.get("verdicts") or {}
    return all(vs.get(k) == "PASS" for k in
               ["R21_ANY_OPTIMAL_MIN_SELECTOR_ENTROPY", "R22_CANONICAL_ACTION_COST",
                "R23_OPTIMAL_ACTION_SET_COST"])


def partition_base(rec):
    vs = rec.get("verdicts") or {}
    return (vs.get("L1_PREDICTIVE_SUFFICIENT_REFINES_SP") == "PASS"
            and vs.get("T2_ENTROPY_MINIMAL_PREDICTIVE_ISOMORPHIC_SP__structural_partition_layer") == "PASS"
            and vs.get("T2b_D4_cardinality_minimal_corollary") == "PASS")


def deficit_all(rec):
    vs = rec.get("verdicts") or {}
    return all(vs.get(k) == "PASS" for k in ["D1", "D2", "D3", "CONTROLS"])


def logloss_all(rec):
    vs = rec.get("verdicts") or {}
    return all(vs.get(k) == "PASS" for k in
               ["A_achievability_shared_r", "A_registered_class_tightness",
                "B_cond_independent_product_sum", "C_correlated_controls_exact_inflation"])


# --- row table --------------------------------------------------------------
# (claim_id, ledger_status_snapshot, verdict_kind, receipt, evidence_label, fn)
# verdict_kind: MECHANICALLY_VERIFIED | CONSISTENT_PARENT_OWNED | NOT_MECHANICALLY_BACKED

ROWS = [
    ("C01", "PARENT_OWNED", "CONSISTENT_PARENT_OWNED",
     "PARTITION_ENUMERATION_RECEIPT_V1.json",
     "L1/T2 mechanics instantiate S_P (predictive partition) exhaustively n<=7",
     partition_base),
    ("C02", "PARENT_OWNED_PATTERN", "CONSISTENT_PARENT_OWNED",
     "RESPONSIBILITY_STATE_PHASE_AUDIT_V1.json",
     "P1 fixture instantiates prediction-state-misses-secondary-target pattern",
     lambda rec: c13(rec)),
    ("C03", "PARENT_OWNED_GENERIC_FORM", "CONSISTENT_PARENT_OWNED",
     "RESPONSIBILITY_SELECTOR_AUDIT_V1.json",
     "R22-R24 instantiate decision-state cost forms exactly",
     static_formulation),
    ("C04", "CANDIDATE_CROSS_CHANNEL_STATIC_COST", "MECHANICALLY_VERIFIED",
     "JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json",
     "P1_STATIC_CROSS_CHANNEL witness: C_stat^*=1 bit > 0",
     c04),
    ("C05", "MANDATORY_ZERO_COST_CONTROL", "MECHANICALLY_VERIFIED",
     "JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json",
     "R27 PASS (selector receipt) + P0 fixture C_stat^*=0",
     c05),
    ("C06", "CANDIDATE_CROSS_CHANNEL_OBSTRUCTION", "MECHANICALLY_VERIFIED",
     "RESPONSIBILITY_SELECTOR_AUDIT_V1.json",
     "R21 equivalence: zero cost iff common-optimal-action refinement exists",
     verdict_is("R21_ANY_OPTIMAL_MIN_SELECTOR_ENTROPY")),
    ("C07", "PARENT_OWNED_OR_COROLLARY", "CONSISTENT_PARENT_OWNED",
     "PARTITION_ENUMERATION_RECEIPT_V1.json",
     "T2/T2b iso corollary checked exactly over Bell-complete n<=7",
     partition_base),
    ("C08", "CANDIDATE_STATIC_OPTIMIZATION_FORMULATION", "MECHANICALLY_VERIFIED",
     "RESPONSIBILITY_SELECTOR_AUDIT_V1.json",
     "R21+R22+R23 PASS (min-entropy action-compatible partition + selector equality)",
     static_formulation),
    ("C09", "CANDIDATE_DYNAMIC_OPTIMIZATION_FORMULATION", "MECHANICALLY_VERIFIED",
     "DYNAMIC_RESPONSIBILITY_OPTIMIZATION_V1.json",
     "J2: 5/5 fixtures, both implementation directions PASS",
     j2_all),
    ("C10", "CANDIDATE_SELECTOR_EQUIVALENCE", "MECHANICALLY_VERIFIED",
     "JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json",
     "J3: 5/5 selectors, j3_expr_equal exact",
     j3_all),
    ("C11", "PRIMARY_CANDIDATE_QUANTITY", "MECHANICALLY_VERIFIED",
     "JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json",
     "J4: all omega rows nonnegative + canonical row + tie-search witness",
     j4_all),
    ("C12", "KNOWN_ANSWER_WITNESS", "MECHANICALLY_VERIFIED",
     "JOINT_DYNAMIC_SELECTOR_EQUIVALENCE_V1.json",
     "J5 canonical fixture expected==observed (0,1,1) bits",
     c12),
    ("C13", "CANDIDATE_PHASE_FRAMEWORK", "MECHANICALLY_VERIFIED",
     "RESPONSIBILITY_STATE_PHASE_AUDIT_V1.json",
     "P0/P1/P2 fixtures all PASS",
     c13),
    ("C14", "CANDIDATE_HORIZON_CURVE", "MECHANICALLY_VERIFIED",
     "RESPONSIBILITY_HORIZON_CURVE_V1.json",
     "PH1 6/6 monotone + PH2 stabilization with literal==iterative",
     c14),
    ("C15", "PARENT_OWNED_IDENTITY", "CONSISTENT_PARENT_OWNED",
     "EPISTEMIC_DEFICIT_IDENTITY_AUDIT_V1.json",
     "D1/D2/D3 + controls PASS (identity instantiated exactly, parent owns it)",
     deficit_all),
    ("C16", "PARENT_OWNED_BENCHMARK", "CONSISTENT_PARENT_OWNED",
     "LOGLOSS_PARENT_BENCHMARK_V1.json",
     "T8A/T8B/T8C reproduced exactly within registered class (scope note in receipt)",
     logloss_all),
    ("C17", "CANDIDATE_BOUNDARY_LIKELY_CLASSICAL", "MECHANICALLY_VERIFIED",
     "RESPONSIBILITY_UNIVERSALITY_AUDIT_V1.json",
     "U1-U5 PASS",
     c17),
    ("C18", "CANDIDATE_LLM_EVALUATION_CONSEQUENCE", "NOT_MECHANICALLY_BACKED",
     None,
     "no empirical/LLM-lane check exists in the receipt corpus (spec forbids empirical LLM claims)",
     None),
]


def main():
    if len(sys.argv) < 2 or sys.argv[1] != "--output":
        print("usage: llm_epistemics_claim_crosscheck.py --output out/CLAIM_RECEIPT_CROSSCHECK_V1.json",
              file=sys.stderr)
        return 2
    out_path = Path(sys.argv[2])
    md_path = out_path.with_suffix(".md")

    ledger = json.loads(LEDGER.read_text())
    ledger_status = {c["id"]: c.get("status") for c in ledger["claims"]}
    jmlr = ledger.get("jmlr_load_bearing_candidates") or []

    results, failures = [], 0
    cache = {}

    for cid, snap, kind, receipt, label, fn in ROWS:
        row = {"claim_id": cid, "ledger_status": ledger_status.get(cid),
               "kind": kind, "receipt": receipt, "evidence": label}
        # ledger drift guard
        if cid not in ledger_status:
            row.update(status="FAIL", detail=f"claim {cid} missing from CLAIM_LEDGER_V4")
            failures += 1
        elif ledger_status[cid] != snap:
            row.update(status="FAIL",
                       detail=f"ledger status drifted: snapshot={snap} ledger={ledger_status[cid]}")
            failures += 1
        elif kind == "NOT_MECHANICALLY_BACKED":
            # honest absence assertion: no receipt may carry an LLM-empirical check.
            # Skip this script's own output: it quotes ledger status strings like
            # CANDIDATE_LLM_EVALUATION_CONSEQUENCE, which would self-match.
            hits = []
            for f in sorted(OUT.glob("*.json")):
                if f.name == out_path.name:
                    continue
                text = f.read_text()
                if "llm_evaluation" in text.lower() or "empirical_llm" in text.lower():
                    hits.append(f.name)
            if hits:
                row.update(status="FAIL", detail=f"unexpected LLM-empirical receipts: {hits}")
                failures += 1
            else:
                row.update(status="NOT_MECHANICALLY_BACKED",
                           detail="confirmed absent from receipt corpus (searched all out/*.json)")
        else:
            if receipt not in cache:
                cache[receipt] = load(receipt)
            ok = fn(cache[receipt])
            if ok:
                row.update(status=kind, detail="evidence re-verified at generation time")
            else:
                row.update(status="FAIL", detail="evidence check returned False")
                failures += 1
        results.append(row)
        print(f"CHECK {cid} {row['status']}")

    jmlr_status = {c: next(r["status"] for r in results if r["claim_id"] == c) for c in jmlr}
    overall = "PASS" if failures == 0 else "FAIL_COUNTEREXAMPLE_FOUND"
    doc = {
        "schema": "orion.51.claim-receipt-crosscheck.v1",
        "ledger": "papers/llm-machine-epistemics/CLAIM_LEDGER_V4.json",
        "results": results,
        "jmlr_load_bearing_status": jmlr_status,
        "counts": {
            "claims": len(results),
            "mechanically_verified": sum(1 for r in results if r["status"] == "MECHANICALLY_VERIFIED"),
            "consistent_parent_owned": sum(1 for r in results if r["status"] == "CONSISTENT_PARENT_OWNED"),
            "not_mechanically_backed": sum(1 for r in results if r["status"] == "NOT_MECHANICALLY_BACKED"),
            "failures": failures,
        },
        "note": "NOT_MECHANICALLY_BACKED is an honest gap report for the theory lane, not a run failure.",
        "overall": overall,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(doc, indent=1) + "\n")

    lines = [
        "# CLAIM_RECEIPT_CROSSCHECK_V1 — ledger claims vs mechanical receipts",
        "",
        "Every MECHANICALLY_VERIFIED row was re-validated against its receipt JSON at",
        "generation time by `llm_epistemics_claim_crosscheck.py`. Ledger status drift",
        "between this script's snapshot and CLAIM_LEDGER_V4.json fails the run.",
        "",
        "| Claim | Ledger status | Cross-check | Receipt | Evidence |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(f"| {r['claim_id']} | `{r['ledger_status']}` | **{r['status']}** | "
                     f"`{r['receipt'] or '—'}` | {r['evidence']} |")
    lines += [
        "",
        f"**JMLR load-bearing claims ({', '.join(jmlr)}):** "
        + ", ".join(f"{c}={s}" for c, s in jmlr_status.items()),
        "",
        f"OVERALL {overall}",
        "",
    ]
    md_path.write_text("\n".join(lines))

    print(f"OVERALL {overall} ({doc['counts']})")
    return 0 if failures == 0 else 3


if __name__ == "__main__":
    sys.exit(main())

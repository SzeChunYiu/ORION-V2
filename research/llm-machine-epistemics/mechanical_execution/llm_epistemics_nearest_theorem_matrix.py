#!/usr/bin/env python3
"""NEAREST_THEOREM_CLAIM_MATRIX_V3 (Spec V4 §14 / V5 §10).

Mechanically joins two frozen inputs:

1. `nearest_parent_theorem_locations.json` — bibliography retrieval receipt (exact
   theorem/definition locations per parent, each VERIFIED against a primary
   source, VERIFIED_SECONDARY (location fixed via secondary sources, primary
   full text not rendered), or marked CANNOT_CHECK_FULL_TEXT). Built by the
   retrieval agents; this script never invents a location: a row whose parent
   location carries none of those statuses prints CANNOT_CHECK_FULL_TEXT, and
   VERIFIED_SECONDARY is never silently upgraded to VERIFIED.
2. `papers/llm-machine-epistemics/CLAIM_LEDGER_V4.json` C01–C18.

The (claim, parent, overlap) table below is a mechanical transcription of the
frozen scientific dispositions in NEAREST_WORK_AND_NOVELTY_V1.md,
NEAREST_WORK_PASS_02_DYNAMIC_STATE.md, NEAREST_WORK_PASS_03_DECISIONAL_STATES.md
and HOSTILE_REVIEW_DECISION_MATRIX_V1.md. This script has NO novelty authority:
it may only emit PARENT_OWNED / PARTIAL_OVERLAP / NO_DIRECT_OVERLAP /
CANNOT_CHECK_FULL_TEXT (Spec V5 §10 vocabulary).

Consistency rules (fail the run on violation):
  R1  every ledger claim C01–C18 appears at least once;
  R2  every ledger PARENT_OWNED* claim has >=1 row overlap=PARENT_OWNED;
  R3  every ledger CANDIDATE_* / KNOWN_ANSWER_WITNESS claim has >=1 row with
      overlap in {PARTIAL_OVERLAP, NO_DIRECT_OVERLAP} (a residual must exist);
  R4  every parent key used has an entry in nearest_parent_theorem_locations.json with
      a non-empty citation;
  R5  no unknown claim ids, no unknown overlap marks.

Exit 0 iff all rules pass. Output: out/NEAREST_THEOREM_CLAIM_MATRIX_V3.csv
(+ JSON receipt + .md summary).
"""

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
LEDGER = HERE.parents[2] / "papers" / "llm-machine-epistemics" / "CLAIM_LEDGER_V4.json"
LOCS = HERE / "nearest_parent_theorem_locations.json"

VALID_MARKS = {"PARENT_OWNED", "PARTIAL_OVERLAP", "NO_DIRECT_OVERLAP", "CANNOT_CHECK_FULL_TEXT"}

# Which retrieval item (from parent_theorem_locations.json) grounds each row.
# (claim_id, parent_key, overlap, retrieval_item, note)
ROWS = [
    # C01 — base predictive quotient (ledger: PARENT_OWNED)
    ("C01", "SC_2001", "PARENT_OWNED", "causal_state_equivalence",
     "causal states = equivalence by identical future law; S_P fully attributed (HRDM R2)"),
    ("C01", "LSS_2001", "PARENT_OWNED", "psr_predictive_state",
     "predictive state from observable history is the PSR parent of S_P"),
    ("C01", "BLACKWELL_LECAM", "PARENT_OWNED", "sufficiency_characterization",
     "sufficient-statistic substrate owns fibre constancy"),
    # C02 — pattern: prediction-target sufficiency != secondary-target sufficiency
    ("C02", "BAISERO_2021", "PARENT_OWNED", "psr_reward_insufficiency",
     "R-PSR: observation-predictive state insufficient for reward (HRDM R1)"),
    ("C02", "WANG_2022", "PARENT_OWNED", "minimal_sufficient_downstream_loss",
     "minimal sufficiency for training target drops non-shared downstream info (PASS_02 Correction B)"),
    ("C02", "HU_2025", "PARENT_OWNED", "multi_task_sufficiency_objective",
     "multi-task information-theoretic sufficiency owns the shared-target pattern"),
    # C03 — generic decision-state form
    ("C03", "BRODU_2011", "PARENT_OWNED", "decisional_state_definition",
     "predictive states + utility -> decision states, generic level (PASS_03 §3)"),
    ("C03", "BLACKWELL_LECAM", "PARENT_OWNED", "experiment_comparison",
     "decision-risk experiment comparison owns the generic form"),
    # C04 — cross-channel static cost witness (candidate)
    ("C04", "BRODU_2011", "PARTIAL_OVERLAP", "causal_refines_decisional",
     "Brodu regime (decision = f(S_P)) forces zero cost; positive cost only for "
     "responsibilities not measurable from S_P (PASS_03 §4-§6)"),
    ("C04", "SUBRAMANIAN_2022", "PARTIAL_OVERLAP", "ais_definition",
     "AIS augment-to-preserve-target overlap; base quotient is linguistic S_P, not POMDP state"),
    ("C04", "BAISERO_2021", "PARTIAL_OVERLAP", "state_augmentation_reward",
     "state augmentation to preserve a secondary target; no entropy-overhead theorem"),
    # C05 — zero-cost control (DS1 = Brodu regime)
    ("C05", "BRODU_2011", "PARENT_OWNED", "causal_refines_decisional",
     "DS1 is the Brodu decision-coarsening regime as mandatory negative control (PASS_03 §5)"),
    # C06 — obstruction equivalence
    ("C06", "BLACKWELL_LECAM", "PARTIAL_OVERLAP", "experiment_comparison",
     "decision-sufficiency corollary direction is classical; equivalence stated "
     "relative to S_P quotient is the residual (PASS_03 §6)"),
    ("C06", "BRODU_2011", "PARTIAL_OVERLAP", "iso_prediction_definition",
     "iso-prediction states partition by optimal action; cross-channel obstruction is residual"),
    # C07 — entropy-minimal predictive representation corollary
    ("C07", "STROUSE_2017", "PARENT_OWNED", "dib_objective",
     "DIB owns minimal deterministic task-sufficient compression (HRDM R3)"),
    ("C07", "SC_2001", "PARENT_OWNED", "causal_state_minimality",
     "causal-state minimality owns entropy-minimal predictive quotient"),
    # C08 — static optimization formulation
    ("C08", "BRODU_2011", "PARTIAL_OVERLAP", "decisional_complexity",
     "decisional complexity D=H(omega) is the static decision-entropy parent; "
     "our form is min-entropy over action-compatible partitions relative to S_P"),
    ("C08", "ISFSM", "PARTIAL_OVERLAP", "compatible_states",
     "action-compatible partition = compatible states; ISFSM minimizes cardinality, not entropy"),
    ("C08", "ISFSM", "PARTIAL_OVERLAP", "binate_cover",
     "binate-cover selection over compatible classes is the exact-formulation parent; "
     "objective there is state cardinality, not selector entropy"),
    # C09 — dynamic optimization formulation
    ("C09", "ISFSM", "PARENT_OWNED", "closed_covers",
     "compatible states + closed covers own the minimal recursively updateable "
     "deterministic state substrate (PASS_02 §7); residual = entropy objective + S_P base"),
    ("C09", "ISFSM", "PARENT_OWNED", "compatibility_non_transitivity",
     "non-transitive compatibility is why minimum reduction is a cover problem, not "
     "partition refinement — substrate for the joint dynamic optimum"),
    ("C09", "ISFSM", "PARENT_OWNED", "np_hardness",
     "minimum ISFSM reduction hardness grounds the exact-enumerator approach"),
    ("C09", "MYHILL_NERODE", "PARENT_OWNED", "right_congruence",
     "right-congruence minimization owns the deterministic recursion substrate (HRDM R6)"),
    ("C09", "SUBRAMANIAN_2022", "PARTIAL_OVERLAP", "ais_dynamic_programming",
     "AIS gives recursively updateable sufficiency for reward, not entropy-minimal "
     "state relative to a linguistic quotient"),
    ("C09", "POMDP_BELIEF", "PARTIAL_OVERLAP", "belief_sufficiency",
     "belief state sufficiency assumes known generative model; base here is linguistic S_P"),
    # C10 — selector equivalence
    ("C10", "MYHILL_NERODE", "PARTIAL_OVERLAP", "right_congruence",
     "congruence merging conditions underlie selector equivalence"),
    ("C10", "SUBRAMANIAN_2022", "PARTIAL_OVERLAP", "ais_definition",
     "information-state unification of prediction and target conditions"),
    ("C10", "BLACKWELL_LECAM", "PARTIAL_OVERLAP", "experiment_comparison",
     "comparison of decision experiments; not stated relative to S_P"),
    # C11 — primary candidate quantity Omega_dyn
    ("C11", "SUBRAMANIAN_2022", "PARTIAL_OVERLAP", "ais_approximate_bounds",
     "AIS bounds control-performance loss, not a prospective entropy premium"),
    ("C11", "BRODU_2011", "PARTIAL_OVERLAP", "transition_graph",
     "decisional transition graph has no dynamic-optionality premium over current compression"),
    ("C11", "POMDP_BELIEF", "NO_DIRECT_OVERLAP", "belief_sufficiency",
     "no parent defines C_dyn*-C_stat* as optionality premium"),
    # C12 — known-answer witness
    ("C12", "ISFSM", "NO_DIRECT_OVERLAP", "closed_covers",
     "fixture machine has no ISFSM counterpart; parents carry no witness for omega=1"),
    ("C12", "SUBRAMANIAN_2022", "NO_DIRECT_OVERLAP", "ais_dynamic_programming",
     "no AIS witness machine with these exact quantities"),
    ("C12", "BRODU_2011", "NO_DIRECT_OVERLAP", "transition_graph",
     "Brodu has no prospective-refinement witness"),
    # C13 — phase framework
    ("C13", "BRODU_2011", "PARTIAL_OVERLAP", "decisional_state_definition",
     "P0 phase = Brodu decisional regime; P1/P2 cross-channel and prospective phases are residual"),
    ("C13", "SUBRAMANIAN_2022", "PARTIAL_OVERLAP", "ais_definition",
     "current-sufficiency vs future-responsibility distinction not phased in AIS"),
    ("C13", "BAISERO_2021", "PARTIAL_OVERLAP", "psr_reward_insufficiency",
     "phase structure absent from R-PSR"),
    # C14 — horizon curve
    ("C14", "SUBRAMANIAN_2022", "PARTIAL_OVERLAP", "ais_approximate_bounds",
     "AIS gives approximate-loss bounds, not a family-growth state-cost curve"),
    ("C14", "SC_2001", "PARTIAL_OVERLAP", "causal_state_minimality",
     "saturation at full-history retention relates to causal-state statistical complexity"),
    # C15 — information-theoretic identity
    ("C15", "COVER_THOMAS_DPI", "PARENT_OWNED", "data_processing",
     "chain-rule/DPI identities own the deficit decomposition algebra (HRDM R11)"),
    # C16 — log-loss benchmark
    ("C16", "CW_2014", "PARENT_OWNED", "logloss_rd_region",
     "log-loss RD region and multiterminal structure own T8A/T8B (HRDM R5)"),
    # C17 — boundary
    ("C17", "SUBRAMANIAN_2022", "PARTIAL_OVERLAP", "ais_approximate_bounds",
     "universality bounds for state families not in AIS"),
    ("C17", "MYHILL_NERODE", "PARTIAL_OVERLAP", "right_congruence",
     "coarsest congruence existence is classical; family-indexed entropy boundary is residual"),
    ("C17", "BLACKWELL_LECAM", "PARTIAL_OVERLAP", "deficiency_comparison",
     "deficiency compares experiments pairwise, not responsibility families"),
    # C18 — LLM evaluation consequence
    ("C18", "CHEANG_2026", "PARTIAL_OVERLAP", "hidden_state_recall_vs_truth",
     "hidden states track recall not truthfulness: motivates, does not own, "
     "prospective revision audit"),
    ("C18", "OSBAND_2023", "PARTIAL_OVERLAP", "enn_joint_predictive",
     "joint predictive distributions are not responsibility-relative audits"),
    ("C18", "SUBRAMANIAN_2022", "NO_DIRECT_OVERLAP", "ais_definition",
     "AIS has no LLM-representation audit consequence"),
]


def main():
    if len(sys.argv) < 3 or sys.argv[1] != "--output":
        print("usage: llm_epistemics_nearest_theorem_matrix.py "
              "--output out/NEAREST_THEOREM_CLAIM_MATRIX_V3.csv", file=sys.stderr)
        return 2
    out_csv = Path(sys.argv[2])
    OUT.mkdir(parents=True, exist_ok=True)

    ledger = json.loads(LEDGER.read_text())
    ledger_status = {c["id"]: c.get("status") for c in ledger["claims"]}
    locs_doc = json.loads(LOCS.read_text())
    parents = locs_doc["parents"]

    failures = []
    seen_claims = set()
    csv_rows = []

    for cid, pkey, overlap, item, note in ROWS:
        # R5 vocabulary
        if overlap not in VALID_MARKS:
            failures.append(f"R5 unknown overlap mark {overlap!r} ({cid}/{pkey})")
            continue
        # R1 known claim
        if cid not in ledger_status:
            failures.append(f"R1 unknown claim id {cid}")
            continue
        seen_claims.add(cid)
        # R4 parent must exist with citation
        p = parents.get(pkey)
        if p is None or not p.get("citation"):
            failures.append(f"R4 parent {pkey} missing from nearest_parent_theorem_locations.json")
            continue
        loc = (p.get("locations") or {}).get(item)
        if loc is None:
            # R6 a row citing a retrieval item that does not exist is a
            # transcription defect, not an honest CANNOT_CHECK
            failures.append(f"R6 retrieval item {item!r} missing for parent {pkey}")
            continue
        elif loc.get("status") in ("VERIFIED", "VERIFIED_SECONDARY"):
            # VERIFIED_SECONDARY = exact location fixed via secondary sources
            # with the primary full text not rendered; provenance stays in
            # the status string, never silently upgraded to VERIFIED
            location = loc.get("location", "")
            assumptions = loc.get("assumptions", "")
            src = loc.get("source", "")
            check_status = loc["status"]
        else:
            location = "CANNOT_CHECK_FULL_TEXT"
            assumptions = loc.get("assumptions", "")
            src = loc.get("source", "")
            check_status = "CANNOT_CHECK_FULL_TEXT"

        csv_rows.append({
            "claim_id": cid,
            "ledger_status": ledger_status[cid],
            "parent_key": pkey,
            "parent_citation": p["citation"],
            "overlap": overlap,
            "theorem_location": location,
            "assumptions": assumptions,
            "source": src,
            "retrieval_status": check_status,
            "note": note,
        })
        print(f"ROW {cid} {pkey} {overlap} [{check_status}]")

    missing = sorted(set(ledger_status) - seen_claims)
    if missing:
        failures.append(f"R1 claims with no matrix rows: {missing}")

    # R2 parent-owned ledger claims need >=1 PARENT_OWNED row
    for cid, st in ledger_status.items():
        marks = {r["overlap"] for r in csv_rows if r["claim_id"] == cid}
        if st.startswith("PARENT_OWNED") and "PARENT_OWNED" not in marks:
            failures.append(f"R2 {cid} ledger={st} but no PARENT_OWNED row")
        if (st.startswith("CANDIDATE") or st == "KNOWN_ANSWER_WITNESS") \
                and not (marks & {"PARTIAL_OVERLAP", "NO_DIRECT_OVERLAP"}):
            failures.append(f"R3 {cid} ledger={st} but no residual (PARTIAL/NO_DIRECT) row")

    overall = "PASS" if not failures else "FAIL"
    out_csv.write_text("")  # truncate for csv writer
    with open(out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(csv_rows[0].keys()))
        w.writeheader()
        w.writerows(csv_rows)

    receipt = {
        "schema": "orion.51.nearest-theorem-claim-matrix.v3",
        "inputs": {
            "claim_ledger": str(LEDGER),
            "parent_theorem_locations": str(LOCS),
            "frozen_dispositions": [
                "research/llm-machine-epistemics/NEAREST_WORK_AND_NOVELTY_V1.md",
                "research/llm-machine-epistemics/NEAREST_WORK_PASS_02_DYNAMIC_STATE.md",
                "research/llm-machine-epistemics/NEAREST_WORK_PASS_03_DECISIONAL_STATES.md",
                "research/llm-machine-epistemics/HOSTILE_REVIEW_DECISION_MATRIX_V1.md",
            ],
        },
        "counts": {
            "rows": len(csv_rows),
            "claims_covered": len(seen_claims),
            "parent_owned": sum(1 for r in csv_rows if r["overlap"] == "PARENT_OWNED"),
            "partial_overlap": sum(1 for r in csv_rows if r["overlap"] == "PARTIAL_OVERLAP"),
            "no_direct_overlap": sum(1 for r in csv_rows if r["overlap"] == "NO_DIRECT_OVERLAP"),
            "locations_verified": sum(1 for r in csv_rows if r["retrieval_status"] == "VERIFIED"),
            "locations_verified_secondary": sum(
                1 for r in csv_rows if r["retrieval_status"] == "VERIFIED_SECONDARY"),
            "locations_cannot_check": sum(
                1 for r in csv_rows if r["retrieval_status"] == "CANNOT_CHECK_FULL_TEXT"),
            "retrieval_items_missing": sum(
                1 for r in csv_rows if r["retrieval_status"] == "RETRIEVAL_ITEM_MISSING"),
        },
        "failures": failures,
        "overall": overall,
    }
    out_json = out_csv.with_suffix(".json")
    out_json.write_text(json.dumps(receipt, indent=1) + "\n")

    md = [
        "# NEAREST_THEOREM_CLAIM_MATRIX_V3",
        "",
        f"Generated by `llm_epistemics_nearest_theorem_matrix.py` from "
        f"`nearest_parent_theorem_locations.json` (retrieval receipt) and `CLAIM_LEDGER_V4.json`.",
        f"Rows: {len(csv_rows)}; overlap marks: "
        f"{receipt['counts']['parent_owned']} PARENT_OWNED / "
        f"{receipt['counts']['partial_overlap']} PARTIAL_OVERLAP / "
        f"{receipt['counts']['no_direct_overlap']} NO_DIRECT_OVERLAP. "
        f"Locations verified: {receipt['counts']['locations_verified']} "
        f"(+{receipt['counts']['locations_verified_secondary']} VERIFIED_SECONDARY); "
        f"CANNOT_CHECK_FULL_TEXT: {receipt['counts']['locations_cannot_check']}.",
        "",
        "| Claim | Ledger status | Parent | Overlap | Location | Note |",
        "|---|---|---|---|---|---|",
    ]
    for r in csv_rows:
        md.append(f"| {r['claim_id']} | `{r['ledger_status']}` | `{r['parent_key']}` | "
                  f"**{r['overlap']}** | {r['theorem_location'] or '—'} | {r['note']} |")
    md += ["", f"OVERALL {overall}", ""]
    out_csv.with_suffix(".md").write_text("\n".join(md))

    print(f"OVERALL {overall} ({receipt['counts']})")
    for f in failures:
        print(f"FAIL {f}")
    return 0 if not failures else 3


if __name__ == "__main__":
    sys.exit(main())

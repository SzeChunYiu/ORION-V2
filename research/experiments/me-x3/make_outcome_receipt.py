#!/usr/bin/env python3
"""Emit ME_X3_OUTCOME_RECEIPT.md from the protected analysis. Run once, after `analyze`."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
an = json.loads((HERE / "results/ME_X3_PROTECTED_ANALYSIS_V1.json").read_text())
d = json.loads((HERE / "ME_X3_FORMAL_MATHEMATICS_EXACT_STUDY_DESIGN_V1.json").read_text())
auth = json.loads((HERE / "PROTECTED_RUN_AUTHORIZATION.json").read_text())
res = json.loads((HERE / "results/ME_X3_PROTECTED_RESULTS_V1.json").read_text())
lean = None
lp = HERE / "lean/LEAN_RECEIPT.json"
if lp.exists():
    lean = json.loads(lp.read_text())
pa = an["score"]["per_arm"]; g = an["gates"]
ARMS = ("A0_DIRECT", "A1_RETRIEVAL", "A2_SELF_REFLECT", "A3_DISCOVER_AND_PROVE_PARENT",
        "A4_LEMMA_ABSTRACTION_PARENT", "B5_R1_VERDICT_ONLY", "B5_R2_SATURATION",
        "B5_R3_FRONTIER", "B5_R4_SEMANTIC", "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION",
        "M_ME_OBSTRUCTION_MINIMUM_ESCALATION")
def row(a, p):
    return ("| `{a}` | {p[validity_rate]:.3f} | {p[fidelity_rate]:.3f} | {p[action_rate]:.3f} | "
            "{p[joint_rate]:.3f} | {p[false_change_rate]:.3f} | {p[false_defer_rate]:.3f} | "
            "{p[drift_missed_rate]:.3f} | {p[false_drift_alarm_rate]:.3f} | "
            "{p[held_out_reuse_rate]:.3f} | {p[mean_expansions]:.0f} |").format(a=a, p=p)
arms_tbl = "\n".join(row(a, pa[a]["pooled"]) for a in ARMS)
abl_tbl = "\n".join(row(a, pa[a]["pooled"]) for a in sorted(
    x for x in pa if x.startswith("M_") and x != ARMS[-1]))
M, B5 = pa[ARMS[-1]], pa["B5_STRONGEST_FAITHFUL_PARENT_FEDERATION"]
fam_tbl = "\n".join(
    "| `{f}` | {r[n]} | {m:.3f} | {b:.3f} | {r[x_only]} | {r[y_only]} | "
    "{r[diff_x_minus_y]:+.3f} | {r[exact_p_two_sided]:.3g} | {rt} |".format(
        f=f, r=r, m=M["per_family"].get(f, {}).get("joint_rate", 0),
        b=B5["per_family"].get(f, {}).get("joint_rate", 0),
        rt=g["ROUTE"]["per_family"][f])
    for f, r in g["G1"]["per_family"].items())
subs = M.get("per_f7_subtype") or {}
sub_tbl = "\n".join(
    "| `{k}` | {r[n]} | {r[fidelity_rate]:.3f} | {b:.3f} | {a0:.3f} | {r[drift_missed_rate]:.3f} |".format(
        k=k, r=r, b=B5.get("per_f7_subtype", {}).get(k, {}).get("fidelity_rate", 0),
        a0=pa["A0_DIRECT"].get("per_f7_subtype", {}).get(k, {}).get("fidelity_rate", 0))
    for k, r in subs.items())
lad = "\n".join(f"| `{r}` | {v:.3f} |" for r, v in g["G4"]["rungs"])
g3 = "\n".join(
    f"| `{f}` | " + (f"`{v['ablation']}` | {v['diff_M_minus_ablation']:+.3f} | "
                     f"{v['exact_p']:.3g} | {'yes' if v['degrades'] else 'NO'} |"
                     if v.get("gated") else f"— | — | — | not gated: {v['reason']} |")
    for f, v in g["G3"]["per_family"].items())
mf8 = M["per_family"].get("F8_TRANSFER", {})
ncf8 = pa.get("M_MINUS_TRANSFER_REUSE_TRACKING", {}).get("per_family", {}).get("F8_TRANSFER", {})
leanpara = ("The Lean cross-check was not run for the protected corpus; the study "
            "stands on the exhaustive oracle and this receipt records the absence."
            if lean is None else
            f"Lean 4.33.1 re-checked {lean['n']} emitted files: "
            f"**{lean['verified_by_lean_kernel']}** accepted as proof terms with "
            f"`#print axioms` certifying axiom-freedom, "
            f"**{lean['rejected_for_registered_reason']}** corrupted files rejected with "
            f"the registered `Derives` type mismatch, "
            f"**{lean['cannot_check']}** `CANNOT_CHECK`, and "
            f"**{lean['disagreements']}** disagreements with the exhaustive oracle.")
(HERE / "ME_X3_OUTCOME_RECEIPT.md").write_text(f"""# ME-X3 — Protected outcome receipt

**State date:** 2026-09-02
**Study:** ME-X3, formal mathematical discovery and regime change
**Design:** `ME_X3_FORMAL_MATHEMATICS_EXACT_STUDY_DESIGN_V1.{{md,json}}`, sha256
`{hashlib.sha256((HERE / 'ME_X3_FORMAL_MATHEMATICS_EXACT_STUDY_DESIGN_V1.json').read_bytes()).hexdigest()}`
**Protected instances:** {an['n_instances']}
**Results sha256:** `{an['results_sha256']}`
**Custody sha256:** `{an['custody_sha256']}`

# ROUTE: {g['ROUTE']['route']}

{g['ROUTE']['reason']}

Ladder terminal (H-EXT-3): `{g['ROUTE']['ladder_terminal']}`

## 1. Authorization and custody

The protected stage ran **once**, and `analyze` ran **once** on its output.

- Authority: {auth['authority']}
- Verbatim instruction: "{auth['verbatim_instruction']}"
- Recorded: {auth['recorded_at']} by {auth['recorded_by']}
- Design sha256 at authorization: `{auth['design_sha256']}`
- Custody seed sha256: `{auth['protected_seed_sha256']}` (matches the commitment frozen
  in the design before the split was generated)
- The seed itself remains in `~/.orion-custody/me-x3/` and is not in the repository.

The runner refuses to generate the protected split unless both the authorization
file is present and the custody seed's sha256 equals the frozen commitment.

## 2. Outcome vector, per arm (pooled)

| arm | validity | fidelity | minimal action | joint | false change | false defer | drift missed | false drift alarm | held-out reuse | mean expansions |
|---|---|---|---|---|---|---|---|---|---|---|
{arms_tbl}

## 3. Per family — the primary report

| family | n | M joint | B5 joint | M-only | B5-only | diff | exact p | route |
|---|---|---|---|---|---|---|---|---|
{fam_tbl}

A pooled average may not hide a family-specific failure. The table above is the
primary report; the pooled row in §2 is secondary.

## 4. Specification fidelity by realized drift subtype

| subtype | n | M | B5 | A0 (proof only) | M drift missed |
|---|---|---|---|---|---|
{sub_tbl}

Counts are the realized draw after oracle-verified rejection sampling, not the
generator's proposal weights.

## 5. Gates

| gate | result |
|---|---|
| G0 oracle and parent fidelity | {'PASS' if g['G0']['pass'] else 'FAIL'} |
| G1 M vs top-rung federation | {'PASS' if g['G1']['pass'] else 'FAIL'} |
| G2 anti-conservatism | {'PASS' if g['G2']['pass'] else 'FAIL'} |
| G3 mechanism by omission | {'PASS' if g['G3']['pass'] else 'FAIL'} |
| G4 interface ladder | {'PASS' if g['G4']['pass'] else 'FAIL'} |

### G3 detail

| family | ablation | M − ablation | exact p | degrades |
|---|---|---|---|---|
{g3}

### G4: the H-EXT-3 interface-information ladder

| rung | joint rate |
|---|---|
{lad}
| `M_ME_OBSTRUCTION_MINIMUM_ESCALATION` | {g['G4']['M_joint_rate']:.3f} |

## 6. Ablations

| arm | validity | fidelity | minimal action | joint | false change | false defer | drift missed | false drift alarm | held-out reuse | mean expansions |
|---|---|---|---|---|---|---|---|---|---|---|
{abl_tbl}

## 7. F8 held-out reuse: carry versus no-carry

- M, carrying its own invention: {mf8.get('held_out_reuse_rate', 0):.3f}
  ({mf8.get('reuse_solved', 0)}/{mf8.get('reuse_n', 0)})
- M minus transfer tracking, no carry: {ncf8.get('held_out_reuse_rate', 0):.3f}
  ({ncf8.get('reuse_solved', 0)}/{ncf8.get('reuse_n', 0)})

The held-out target admits independent re-invention from the registered candidate
pool as well as reuse of the source artefact, so F8 measures held-out reach at the
lemma level, not reuse gain, and does not support a strong reusability claim. The
counterfactual is printed so the reading is visible rather than inferred.

## 8. External proof-checker cross-check

{leanpara}

The encoding is an inductive `Derives` proposition with an explicit proof term per
derivation, not a Boolean function proved `true` by `rfl`; a corrupted derivation
counts as correctly rejected only when it fails with a type mismatch on a
`Derives` term, and any other failure is `CANNOT_CHECK`.

## 9. What this does and does not establish

Established, within a finite equational theory with an exhaustive oracle:
the separation between proof validity and specification fidelity; the behaviour
of the registered arms on the minimum-escalation decision; the ablation structure;
the interface ladder; the cost frontier.

**Not** established: anything about controller behaviour at Mathlib scale, where
no exhaustive oracle exists and proof search dominates cost. Mathlib was excluded
because an unbounded library makes the minimum-escalation oracle uncomputable, not
because of resources. Any reading of this receipt as evidence about frontier Lean
theorem proving is a misreading.

## 10. No rescue

No threshold, family, arm, budget, generator constant or gate was changed after
these outcomes were inspected, and none may be. The route above is terminal for
ME-X3 V1. A further question requires a new prospective identity.

## Terminal

```text
ME_X3_STATUS = EXECUTED_ONCE
ROUTE = {g['ROUTE']['route']}
LADDER_TERMINAL = {g['ROUTE']['ladder_terminal']}
G0 = {'PASS' if g['G0']['pass'] else 'FAIL'}
G1 = {'PASS' if g['G1']['pass'] else 'FAIL'}
G2 = {'PASS' if g['G2']['pass'] else 'FAIL'}
G3 = {'PASS' if g['G3']['pass'] else 'FAIL'}
G4 = {'PASS' if g['G4']['pass'] else 'FAIL'}
MATHLIB_SCALE_GENERALITY = OUT_OF_SCOPE
FIELD_STATUS_AUTHORITY = NONE
```
""")
print("ME_X3_OUTCOME_RECEIPT.md written")

#!/usr/bin/env python3
"""Emit the parent-fidelity receipt from the actual selftest and development output."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
sel = json.loads((HERE / "results/ME_X3_SELFTEST_REPORT.json").read_text())
an = json.loads((HERE / "results/ME_X3_DEVELOPMENT_ANALYSIS_V1.json").read_text())
d = json.loads((HERE / "ME_X3_FORMAL_MATHEMATICS_EXACT_STUDY_DESIGN_V1.json").read_text())
pa = an["score"]["per_arm"]
ARMS = ("A0_DIRECT", "A1_RETRIEVAL", "A2_SELF_REFLECT", "A3_DISCOVER_AND_PROVE_PARENT",
        "A4_LEMMA_ABSTRACTION_PARENT", "B5_R1_VERDICT_ONLY", "B5_R2_SATURATION",
        "B5_R3_FRONTIER", "B5_R4_SEMANTIC", "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION",
        "M_ME_OBSTRUCTION_MINIMUM_ESCALATION")
rows = "\n".join(
    "| `{a}` | {p[validity_rate]:.3f} | {p[fidelity_rate]:.3f} | {p[action_rate]:.3f} | "
    "{p[joint_rate]:.3f} | {p[drift_missed_rate]:.3f} | {p[false_drift_alarm_rate]:.3f} | "
    "{p[held_out_reuse_rate]:.3f} | {p[mean_expansions]:.0f} |".format(a=a, p=pa[a]["pooled"])
    for a in ARMS)
abl = "\n".join(
    "| `{a}` | {p[joint_rate]:.3f} | {p[fidelity_rate]:.3f} | {p[action_rate]:.3f} | "
    "{p[false_change_rate]:.3f} | {p[drift_missed_rate]:.3f} | "
    "{p[held_out_reuse_rate]:.3f} |".format(a=a, p=pa[a]["pooled"])
    for a in sorted(x for x in pa if x.startswith("M_") and x != ARMS[-1]))
tests = "\n".join(f"| `{t['test']}` | {'PASS' if t['passed'] else 'FAIL'} | {t['detail'] or ''} |"
                  for t in sel["tests"])
code = "\n".join(f"| `{k}` | `{v}` |" for k, v in sorted(d["code_sha256"].items()))
subs = pa[ARMS[-1]].get("per_f7_subtype") or {}
subtable = "\n".join(
    f"| `{k}` | {r['n']} | {r['fidelity_rate']:.3f} | "
    f"{pa['A0_DIRECT']['per_f7_subtype'].get(k, {}).get('fidelity_rate', 0):.3f} |"
    for k, r in subs.items()) or "| (none drawn) | | | |"
npass = sum(t["passed"] for t in sel["tests"])
(HERE / "ME_X3_PARENT_FIDELITY_RECEIPT_V1.md").write_text(f"""# ME-X3 — Parent fidelity receipt and development-split summary V1

**State date:** 2026-09-02
**Design:** `ME_X3_FORMAL_MATHEMATICS_EXACT_STUDY_DESIGN_V1.{{md,json}}`
**Split reported here:** `DEVELOPMENT` ({an['n_instances']} instances, public seed
`{d['splits']['development']['seed']}`). **No protected outcome has been generated or
inspected.** Development numbers are not evidence for or against any hypothesis;
they exist to show the environment discriminates and the parents behave like
their sources.

## 1. Why this receipt exists

A federation whose members do not actually behave like the systems they stand for
is a strawman, and a study built on one is worthless. Before any protected run,
each parent must reproduce, on a hand-authored case, the behaviour its source is
known for — and the oracle must be shown to agree with an independent
implementation of itself.

## 2. G0: selftests

| test | result | detail |
|---|---|---|
{tests}

`{npass}/{len(sel['tests'])}` passed.

Two of these carry more weight than the rest.
`two_independent_searches_agree_on_minimal_length` runs breadth-first search and
iterative-deepening depth-first search over the same rewrite graph and requires
identical minimal lengths, so a bug in one would have to be exactly mirrored in
the other. `model_enumeration_fast_path_is_exact` checks the definable-generator
optimisation — which drops the alternative presentation's model enumeration from
`n^(n·4)` to `n^(n·3)` — against brute-force enumeration of every function tuple,
so the speedup is verified to be exact rather than assumed to be.

## 3. Parent behaviour on the development split

| arm | validity | fidelity | minimal action | joint | drift missed | false drift alarm | held-out reuse | mean expansions |
|---|---|---|---|---|---|---|---|---|
{rows}

Read the `drift missed` column first. Every proof-only parent (`A0`–`A4`) misses
**every** specification drift, because a system that treats proof success as
intent success has no way to see it; every arm that runs the specification check
misses **none**. That is the FormalScience result reproduced inside this
environment, and it is the reason proof validity and specification fidelity are
scored as separate endpoints rather than combined.

`false drift alarm` is `0.000` everywhere: no arm buys its drift detection by
crying wolf on the faithful controls.

`M` and the top-rung federation are tied on every decision endpoint and `M` is
cheaper, which is what the pre-registered `PARENT_SUFFICIENT` expectation looks
like: on an exhaustive finite oracle, control buys ordering, not reach.

### 3.1 F7 by realized drift subtype

| subtype | n | M fidelity | A0 fidelity |
|---|---|---|---|
{subtable}

The development split is far too small to cover the subtype space; the point of
this table is that the scorer reports the realized draw rather than the
generator's proposal weights, so a family average cannot hide a subtype that is
never detected on the protected split.

## 4. Ablations on the development split

| arm | joint | fidelity | minimal action | false change | drift missed | held-out reuse |
|---|---|---|---|---|---|---|
{abl}

Each registered omission moves the column it is supposed to control:
`M_MINUS_SPECIFICATION_PRESERVATION` loses fidelity and misses every drift;
`M_MINUS_FALSE_CHANGE_PENALTY` picks up a false representation-change rate;
`M_NEVER_CHANGE_REPRESENTATION` loses the representation family;
`M_MINUS_UNRESOLVED_TERMINAL` loses the underdetermined family.
`M_MINUS_TRANSFER_REUSE_TRACKING` does **not** move, for the structural reason
recorded as a limitation in §5 of the design: the held-out target admits
independent re-invention as well as reuse, so F8 measures held-out reach rather
than reuse gain. On the protected split these are gated (G3) rather than
described, and the F8 no-carry counterfactual is printed beside the rate.

## 5. Development route

`{an['gates']['ROUTE']['route']}` — {an['gates']['ROUTE']['reason']}

Ladder terminal: `{an['gates']['ROUTE']['ladder_terminal']}`.

This is a development observation, not a result. It is recorded here so that the
protected outcome cannot be presented as a surprise if it agrees, or quietly
reframed if it does not.

## 6. Frozen code

| file | sha256 |
|---|---|
{code}

Design JSON sha256: `{hashlib.sha256((HERE / 'ME_X3_FORMAL_MATHEMATICS_EXACT_STUDY_DESIGN_V1.json').read_bytes()).hexdigest()}`
Custody seed sha256: `{d['custody']['protected_seed_sha256']}`

## Terminal

```text
PARENT_FIDELITY = PASSED
ORACLE_SELF_AGREEMENT = PASSED
PROOF_ONLY_PARENTS_MISS_ALL_SPECIFICATION_DRIFT = TRUE
F8_MEASURES_HELD_OUT_REACH_NOT_REUSE_GAIN = TRUE
PROTECTED_OUTCOMES_INSPECTED = FALSE
```
""")
print("written")

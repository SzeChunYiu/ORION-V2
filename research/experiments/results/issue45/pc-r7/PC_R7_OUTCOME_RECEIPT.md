# PC-R7 Outcome Receipt — naturalistic obligation cell

**Receipt ID:** `PC_R7_OUTCOME_RECEIPT`  
**Date:** 2026-09-02T14:05:48Z
**Design (frozen, unaltered):** `research/experiments/pc-r7/PC_R7_NATURALISTIC_OBLIGATION_CELL_DESIGN_V1.{md,json}`  
**Intake:** `research/experiments/sd80/SD80_CASE_MATRIX_INTAKE_V1.{md,json}` (cases sha256 `0bd039d134b6f641fe267e69f5983e2533f66bd4e2bfaa02fb083b2fa6ed5d5f`)  
**Host:** Mac (intake, hashing, tagging orchestration); LUNARC unreachable during intake (expired 2FA socket); billy-old reserved for any arm compute

## Terminal: `INSUFFICIENT_ELIGIBLE_NATURALISTIC_CASES` (PC-R7 §6 row 1 — contraction terminal)

Route fired: **GN0 pass, population condition fail**. No arm was dispatched; no
rollup exists because the cell may not run (PC-R7 §1: "Both tags must be
populated ≥15 cases/domain before the cell may run").

## Gate numbers

| Gate | Value | Result |
|---|---|---|
| GN0 `INTAKE_VALID` | two independent fresh-context taggers, 20-case calibration set: 20/20 agreement = 1.00 (≥ 0.90), 0 disagreements; rule clarified V1.1 on three ambiguities before the full round | **PASS** |
| Population (§1) | both tags ≥ 15 cases/domain | **FAIL** (INTERNAL = 0 / 0 / 1) |
| GN1 `EXTERNAL_BINDING` | not evaluable — no run | — |
| GN2 `INTERNAL_HARMLESS` | not evaluable — no run | — |

## Case matrix (FM80 §2 structure met: 1 formal + 2 empirical, ≥ 30 eligible each)

| Domain | PC-R7-eligible | Tagged | EXTERNAL_VERIFIABLE | INTERNAL | full-round A/B agreement |
|---|---|---|---|---|---|
| `PSYCHOLOGY_RPP` | 100 | 100 | 100 | 0 | 1.00 |
| `CANCER_BIOLOGY_RPCB` | 50 | 50 | 50 | 0 | 1.00 |
| `FORMAL_MATHEMATICS_1000PLUS` | 243 | 60 | 59 | 1 | 1.00 |

Formal domain tagged on a frozen seeded 60-case sample (seed 20260902) of 243
eligible entries. MLRC (36 prose-verdict reports) recorded but not counted:
no outcome-free evidence layer exists for its cases.

## Reading (registered, PC-R7 §6)

The witness sources that make a naturalistic case *verifiable* (OSF
registrations, eLife Registered Reports, externally authored theorem
statements) are the same things that make its constraints *external*. Under
the frozen tagging semantics the `INTERNAL` stratum is therefore empty by
construction across all three domains (the single `INTERNAL` case is a
Wikidata fetch failure, i.e. unverifiable-from-record, not a self-generated
constraint). Theory revision A's internal-vs-external contrast cannot be
tested on registered-replication-verdict-class cases. Programme consequence
per the pre-registered terminal map: **P-C closes on the generated + boundary
contract**; PC-C4 receives no naturalistic evidence from this cell.

## Revival pass (attributed before filing)

Failure attributed to ONE stage: **case-source supply**, not tagging (A/B
agreement 1.00 everywhere), not arm construction, not analysis. Favourable
re-cuts checked and rejected: 100/100 RP:P cases carry a non-withdrawn OSF
registration; 76/76 RP:CB experiment records carry an accepted, linked eLife
Registered Report; expanding the formal sample from 60 to all 243 eligible
entries could add `INTERNAL` cases there but cannot populate the two empirical
domains, and PC-R7 §1 requires both tags ≥ 15 **per domain**; MLRC fails
eligibility item (g) rather than the tag population. Detail in
`research/experiments/sd80/SD80_CASE_MATRIX_INTAKE_V1.md` §6.

## Compute custody (no dispatch)

LUNARC access was restored at 2026-09-02T14:13Z (`cosmos2.int.lunarc`, reachable
via the billy-old ControlMaster route) and billy-old carries a working codex CLI
(`0.129.0-alpha.15`). Neither was used for arms: PC-R7 §1 forbids the cell from
running until both provenance tags reach 15 cases/domain, so dispatching arms on
an available host would have broken the freeze rather than produced evidence.
Host availability is recorded here so the non-run is attributable to the frozen
design, not to a resource outage.

## No-rescue clause honoured

- No generated-cell result re-read; no transfer claim; no endpoint, stratum
  margin, arm definition or tagging-rule semantics changed after intake began
  (V1.1 is an operational clarification recorded before the full round).
- Taggers and the intake never read `SD80_CASE_MATRIX_HIDDEN_KEYS_V1.json`.
- A future cell would need a witness source whose constraints are
  self-generated yet whose outcomes are verifiable (e.g. unregistered
  replications with later independent verdicts); none was identified among
  lawful public sources on 2026-09-02.

skills-applied: none (receipt, no manuscript content)

# Silent Failure Modes — Relocated Session Records (2026-09-02/03)

## Status

`RELOCATED_FROM_A_REFUSED_PAPER_CANDIDATE`

## Why this record exists

A proposed standalone paper on silent failure modes in AI-mediated research pipelines was refused
admission — `DO_NOT_OPEN`, merge `323894f`,
`papers/prospectuses/SILENT_FAILURE_MODES_ADMISSION_ASSESSMENT_V1.md`. That assessment named
`FAILURE_LEDGER.md` and the owning lane PRs as the durable homes for the findings, and closed itself
to further instances: *"Further modes should go to `FAILURE_LEDGER.md`, which is the programme's
append-only register for exactly this and is bound to running code, and to the lane PRs that own
them."* The relocation did not happen at the time. This record performs it.

**These are process-failure evidence. They are not a scientific result, not a novelty claim, and
not a paper.** The refusal reasoning stands and is not relitigated here; see `## Prior work` for the
parents that already own the synthesis.

## How to read this record

| File | Records | What the group is |
|---|---|---|
| `01-comparator-and-claim-integrity.md` | D1-D5 | The arm a result is measured against, or the sentence reporting it, claims more than the procedure that produced it |
| `02-registered-clauses-structurally-determined.md` | D6, D19-D21 | Registered clauses whose verdict was fixed by the construction of the stimulus, in both directions |
| `03-measurement-and-substrate.md` | D7-D9 | What a run was actually executed against, versus what its custody record certifies |
| `04-gate-integrity.md` | D10-D12, D22-D24 | Checks that ran, on the right file, for the right string, and could not fire |
| `05-operational-tooling-and-version-control.md` | D13-D18, D25 | **Operational hazards, not scientific failure classes** — see that file's preamble |

## Index

| # | Record | Class | Status |
|---|---|---|---|
| D1 | Vacuous comparison: two arms on one code path | `VACUOUS_CONTRAST` | `REALISED_IN_A_DEVELOPMENT_ARTIFACT` |
| D2 | Prompt asymmetry disadvantaging the comparator (ME-F1) | `HANDICAPPED_COMPARATOR` | `NEAR_MISS`; headline numbers `CANNOT_VERIFY` |
| D3 | Budget starvation of a comparator (ME-F1) | `HANDICAPPED_COMPARATOR` | `NEAR_MISS`; attributed to the wrong arm as nominated |
| D4 | A representation claim falsified by exhibition (ME-X6) | `TERMINAL_OVERSTATES_ITS_PROCEDURE` | `REALISED` |
| D5 | A threshold margin borrowing a null's authority (H-EXT-1) | `TERMINAL_OVERSTATES_ITS_PROCEDURE` | `REALISED`, corrected, contained |
| D6 | A registered clause the runner silently narrows (PRA GP2a) | `REGISTERED_SCOPE_DIVERGENCE` | `REALISED`, deliberately unpatched |
| D19 | A registered clause unsatisfiable in principle (PRA GP2a R3) | `STRUCTURALLY_DETERMINED_REGISTERED_CLAUSE` | `NEAR_MISS` |
| D20 | Two registered clauses unfailable by construction (PRA GP2a) | `STRUCTURALLY_DETERMINED_REGISTERED_CLAUSE` | `REALISED` |
| D21 | A confound mistaken for a surface artifact (PRA GP2a R0) | `NONIDENTIFIABLE` | `REALISED`, corrected in the diagnosis |
| D7 | Pinning a served model id does not pin a condition (E30-R12) | `UNPINNED_SUBSTRATE_CONDITION` | `REALISED`, filed as could-not-check |
| D8 | A checker staged against the wrong corpus (ME-X3) | `CHECKER_STAGED_ON_THE_WRONG_SUBSTRATE` | `NEAR_MISS`, guarded |
| D9 | A toolchain shim with no default toolchain (ME-X3) | `CHECKER_STAGED_ON_THE_WRONG_SUBSTRATE` | `NEAR_MISS`, reconstructed, unattested; **fail-loud** |
| D10 | Log-wrap blindness | `CHECK_THAT_RUNS_AND_CANNOT_FIRE` | `REALISED`, **FIXED** |
| D22 | A meta-gate that plants only unwrapped fixtures | `CHECK_THAT_RUNS_AND_CANNOT_FIRE` | `REALISED`, **FIXED** |
| D11 | Substring-match inversion | `CHECK_THAT_RUNS_AND_CANNOT_FIRE` | `NEAR_MISS`, never on `main` |
| D23 | An interpreter version that skips a registry check | `CHECK_THAT_RUNS_AND_CANNOT_FIRE` | `CANNOT_VERIFY` as nominated; consequence falsified |
| D24 | A vacuous loop: a filter that skips every assertion | `CHECK_THAT_RUNS_AND_CANNOT_FIRE` | mechanism verified; **no realised instance** |
| D12 | A no-op mutation making a gate probe report PASS | — | `CANNOT_VERIFY`; polarity inverted in the real artifact |
| D13 | Post-merge validation gap | *(operational)* | `REALISED`, **FIXED** for the integrated suite |
| D14 | A PR reading `state: MERGED` whose work is absent from `main` | *(operational)* | `REALISED`, recovered |
| D15 | `--delete-branch` closes every stacked PR | *(operational)* | `REALISED`; irreversibility is testimony, not artifact |
| D16 | Squash-merge makes landed work look unlanded | *(operational)* | mechanism verified |
| D25 | A three-dot diff shows one side only | *(operational)* | mechanism verified; incident `CANNOT_VERIFY`, direction inverted |
| D17 | A stale shared checkout reverting earlier fixes | *(operational)* | `CANNOT_VERIFY`; a near-miss is evidenced instead |
| D18 | A rendered or filtered surface substituted for the fact | *(operational)* | `REALISED` (D18b) |

## Verification standard applied

Every item was re-read against its artifact before being recorded, and the summaries that nominated
them were wrong often enough that this must be stated plainly. **Of the items nominated across two
passes, four could not be verified at all, two were attributed to the wrong object, one had its
briefed consequence falsified by the same file that supplies its mechanism, one had its hazard
stated backwards, and ten more carried at least one number or clause the artifact does not
support.** Corrections are recorded in place rather than silently applied.

Status labels:

- `REALISED` — a frozen or protected artifact carried the defect;
- `REALISED_IN_A_DEVELOPMENT_ARTIFACT` — a committed but development-labelled artifact carried it;
- `NEAR_MISS` — caught before any artifact carried it;
- `CANNOT_VERIFY` — no artifact supports it, **with the search scope stated**.

Absence is only ever claimed from a search that carried a control pattern which had to match, and
`/usr/bin/git`, `/usr/bin/grep` and `/usr/bin/diff` were used for anything driving a decision
(see D18a for why).

## What this record does not establish

No prevalence, no base rate, and no detector efficacy. It grants no scientific correctness, no
novelty and no publication authority. Where a lane's own receipt already states a finding, **that
receipt is the owner and this is a pointer to it.** This record establishes only that the named
artifacts say what is quoted.

## Contamination

Recorded because it is a limit on everything above, not a caveat to it.

**This corpus was collected while a paper was being assessed from it.** Lanes were finding,
disclosing and framing silent failures knowing a paper was in assessment, which changes what is
looked for, what is reported and how it is worded, and is unmeasurable from inside. That is itself
an instance of a coordinate the programme already owns: P-D's C09 holds that evaluation *"can alter
the systems, researchers, agents or data-generating processes being evaluated"* and that a measured
relationship may not be treated as stable until that response is modelled. **No such model exists
here.** The admission assessment names this the deepest reason the object could not be its own
evidence.

Two consequences bind this record. First, nothing here may be read as a prevalence or a base rate.
Second, the corpus is dominated by near-misses, and several records exist *only* because a lane
disclosed a hazard that left no trace in its own artifacts. That is good practice and worthless as a
denominator.

## Prior work

Recorded so that no successor re-derives it, and bound at source per the admission assessment §5.1.

- Kupferman, *Sanity Checks in Formal Verification*, CONCUR 2006, LNCS 4137:37-51 — already unifies
  vacuity and coverage as one mutation framework: mutations in the specification give vacuity,
  mutations in the system give coverage. That is the generalization this material would otherwise
  propose, published twenty years earlier. Verified independently against two sources.
- Beer, Ben-David, Eisner and Rodeh, *Efficient Detection of Vacuity in Temporal Model Checking*,
  Formal Methods in System Design 18(2):141-163, 2001, p. 141 — reports that in the first formal
  verification runs of a new hardware design roughly a fifth of formulas are found trivially valid,
  and that trivial validity always points to a real problem. **Stated with its limitation:** an IBM
  RuleBase experience report, not a methodologically specified census. Read from the primary PDF.
- The circulating rendering of that figure ("20% of specifications pass vacuously") does **not**
  match the source wording and must not be bound. A successor citing the rate binds it to FMSD 2001,
  p. 141.

Consequently: the census slot and the unifying framework are both already occupied, and the
detectors are this programme's own registered operating procedure (PC-R6 dispatch guard A6, PRA
Appendix B.7). Nothing here is claimed as new.

## Reopening conditions

- D12 reopens if a realised instance is produced in which a no-op mutation yielded a gate PASS.
- D17 reopens if a `main` commit is found whose landing restored earlier content over a repaired
  defect (the `M`-status path was not exhaustively closed).
- D24 reopens if a realised unguarded stratum loop is found **by a checker validated in both
  directions first**; the heuristic scan run here is not that checker.
- D25 reopens if the ~2,480-deletion incident is attested by any artifact in either repository.
- D2's `0.5125` / `0.131` / `23/23` reopen if the ME-F1 lane commits a post-repair two-arm report;
  the absence claim is scoped to every origin ref and every local checkout as of 2026-09-04, not to
  `billy-laptop-old`.
- D9 reopens if any artifact is found attesting that the bare-`lean` shim was actually executed.
- D6, D19 and D20 reopen at the PRA V3 re-freeze, which is where the R0/R3 divergence and the
  structurally determined clauses can be repaired.
- D15's irreversibility clause reopens if a captured `gh pr reopen` error is ever recorded.

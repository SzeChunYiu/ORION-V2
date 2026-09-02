# Silent Failure Modes in AI-Mediated Research Pipelines — Standalone Paper Admission Assessment V1

**Assessed object:** a proposed standalone methods/experience paper reporting empirically measured
*silent* failure modes in an AI-mediated research pipeline — failures in which the pipeline reported
success — together with cheap detectors that would have caught each earlier.

**Assessment date:** 2026-09-02.
**Evidence head:** ORION-V2 `main` @ `a67bd852` (`origin/main` at fetch time).
**Manuscript heads read:** ORION-paper `origin/main`, at `ba7a084` when the assessment opened and
`3e2e22e` at close — PRA V16 (PR #80) and the workflow repair (PR #43) both merged mid-assessment,
and §2 records the corrections that forced. All reads were from `origin/main` refs or a private
worktree; no shared checkout was switched.
**Gates applied:** `papers/PROGRAMME_LEDGER_V0.md` §"Programme-level selection rule";
`papers/CLOSURE_PORTFOLIO_WAVE06_V0.md`;
`papers/pipeline/SD_RECURSIVE_STANDALONE_ADMISSION_GATE_V2.md` §6;
ORION-paper `v2-papers/_portfolio/contraction/PAPER_OVERLAP_AND_DISCLOSURE_MATRIX_V1.md` §§3, 8.

---

## 0. Verdict

```text
OBJECT                       = SILENT_FAILURE_MODES_IN_AI_MEDIATED_RESEARCH_PIPELINES
STANDALONE_PAPER             = DO_NOT_OPEN
DISPOSITION                  = MERGE_INTO_EXISTING_OWNERS + REGISTER_ONE_PROSPECTIVE_REVIVAL
PROGRAMME_CRITERIA_MET       = 0 clean, 1 partial (recoverable), 6 FAIL
BLOCKING_FAILURES            = no prospective discriminator; no strongest-parent baseline;
                               no evaluation outside the derivation domain; no independent authority
STRONGEST_INSTANCE           = ALREADY_PUBLISHED_BY_PRA (V16 Appendix B.8, merged 3e2e22e)
PARENT_COMPOSITION           = DOMINATES — residual empty; the unifying framework (Kupferman 2006)
                               and the empirical census both predate the object
REVIVAL                      = SFM-D1 planted-defect detector-efficacy study (§8), not yet executed
LATER_INSTANCES              = 7 arrived during assessment; gate unmoved (§2.2-§2.4)
COST_OF_NOT_OPENING          = ZERO (every finding retains its existing owner and receipt)
```

This is a `DO_NOT_OPEN` in the sense of `CLOSURE_PORTFOLIO_WAVE06_V0.md`'s C12 entry: the coordinate
is real and the observations are sound, but they do not constitute a distinct scientific object with
evidence in hand, and each already has an owner. Deleting a candidate after donor reduction is a
successful programme outcome.

---

## 1. What was assessed, and how

Six evidence bundles were nominated. Each was read in full against its receipt on the merged head
rather than against any summary. Verification status per bundle is recorded in §2; the reduction
that decides the object's identity is §3; ownership is §4; parents are §5; the programme's own
seven-point rule is walked literally in §6.

Two facts found during assessment are individually blocking and were established before the verdict
was written:

1. the strongest of the six bundles is **already reported, with its exact numbers and its detector,
   inside a manuscript the programme is preparing for release** (PRA V16, Appendix B.8);
2. three further bundles are outcomes or anticipations of **P-C's prospectively licensed
   follow-ups**, which the portfolio explicitly forbids re-reporting as another paper's results.

---

## 2. Evidence inventory, verified against receipts

Every number below was re-read on the merged head. Where the nominating brief and the receipt
disagree, the receipt wins and the correction is recorded. Corrections are not incidental: **three of
the six bundles were briefed with at least one number that the receipt does not support**, and two of
those live in a block its own receipt marks as not machine-generated. That fact is assessed in §2.1.

| # | Bundle | Status | Verified content |
|---|---|---|---|
| 1 | Control-induced exploration collapse (E40-m5' Stage-2d) | **VERIFIED** | Terminal quality 0.9877 (no mandate) / 0.9518 (regime anchor) / 0.0233 (exact-seed mandate); the unmandated arm samples five `frac` values and hits the planted optimum `partial@0.8` at cycle 8; the seed-mandated arm never leaves `frac 0.0`. All four controls PASS. `research/experiments/e40-matched/E40_M5P_STAGE2D_OUTCOME_RECEIPT.md`; design PR #169 `b42bf470`, outcome PR #170 `a67bd852`. |
| 2A | Applicability guard excluded the family under test | **VERIFIED, two corrections** | The guard is `fano_applicable = is_terminal_model(m) and satisfies_pc(m)`; the violation counter was nested inside it. Ungated: **1,309 violations on 992 machines** — but that is the **seven-family aggregate**; the non-PC family alone carries **1,308 on 991**. "11 of 3,000" is *terminal-model* eligibility in family `random_general_n<=5`; the gated check there ran on **10 of 17,991** static-admissible partitions. `research/llm-machine-epistemics/h_ext4_premium_bounds.py:893-912`; `H_EXT4_RESULT_V1.json`. Fix merged to ORION-V2 main as **`c30f1827`** (PR #166). |
| 2B | CI assertion matching text LaTeX never emits | **VERIFIED; since merged** | `grep -E 'Overfull \(hbox\|vbox\)'` in single quotes greps for the literals `Overfull (hbox` and `vbox)`; LaTeX emits neither. Reproduced empirically: 0 of 2 defect lines matched. Two distinct defects — v20/v21/v22 fully vacuous, v19/v112 vbox-blind. The fix has since merged (ORION-paper `446f522`, PR #43); all six workflows on `origin/main` now carry `Overfull \\[hv]box`, verified by reading each file at that ref. |
| 2C | Horizon check flat by construction | **VERIFIED; closed by claim withdrawal, not repair** | `C_k^* = C_dyn^*` for every `k>=1` is a theorem, so `PH2_FINITE_HORIZON_STABILIZATION` cannot fail on any machine. All 6 fixtures flat for k>=1. **The defect was closed by contracting the claim** (ORION-paper `4e951d75`, PR #68) — the check itself is unchanged and still cannot fail. |
| 3 | Silent substrate substitution | **VERIFIED, one correction** | Four probes, HTTP 200 each, **three** substitutions (not two): `glm-5.2`→`glm-5.3`, `glm-5.1`→`glm-5.3`, `glm-4.6`→`glm-5.3-flash`; `glm-5.3`→`glm-5.3`. No field, header or status announces it. m2/m3 served id **unrecoverable — 0 hits across 1,810 artifact files**. Fail-closed guard `assert_served_model()` at `scripts/e40_matched_runner_m5p_stage2c.py:164-175`, with a self-test asserting it rejects four wrong ids. |
| 4 | A null that measured serialization | **PARTLY VERIFIED; two briefed numbers fail** | E30-R11 verified: F2 5/40 = F0 5/40, SIMPLE 6/40, all Holm p = 1.0. E70-GC1 verified: `success_iff_header_unchanged = true` ×4. E70-GC2 verified: raw header-exact **0/16 at every rung** — but **single-arm (`SIMPLE_DIRECT` only)**, and the semantic ceiling is **46/46 applied cells**, not 48/48. **CORRECTED:** `NONE_PATCH_NOT_APPLIED` is **75.0%–82.5%**, not 78–83%. **UNCORROBORATED:** "311/480 patch-apply `rc=128`" has **no supporting artifact anywhere in the repo**. Fix PR #168 `8945cec` is merged but **changes future runs only**; nothing was re-scored. |
| 5 | Terminal emitted while its own control failed | **VERIFIED, wording corrected; one claim counterfactual** | Planted control 0.6412 FAIL (0/8 cycles in basin) against 0.9877 (m3) and 1.0 (m2), same plant and PASS rule. `E40_TERMINAL` is present in the emitted rollup at `E40_M5P_STAGE2C_ROLLUP_V1.json:1721`, in the same file as the FAIL. **Correction:** `evaluate_gates()` does not "report verdicts without consuming them" — it never receives them; the rollup writer records them as a sibling of `analysis`. **Counterfactual, not realized:** the repo contains **zero** programmatic consumers of that rollup, and the cited precedent (`e40_m5p_channel_screen.py:233`) reads sha-pinned mechanism statistics, not a disposition field. Fixed in the Stage-2d freeze (PR #169 `b42bf470`), deliberately not retrofitted. |
| 6 | Confounded naturalistic case selection (SD80/PC-R7) | **VERIFIED as mechanism; the statistic does not exist** | The `INTERNAL` stratum is **empty by construction: 0 of 210 tagged cases** across three domains (100/0, 50/0, 59/1 — and the single `INTERNAL` is a fetch failure, not a self-generated constraint). Tagger agreement 1.000. **There is no correlation coefficient and no 2x2 table**, and none is estimable: eligibility selects on outcome-verifiability, fixing one margin at 100%. Terminal is `INSUFFICIENT_ELIGIBLE_NATURALISTIC_CASES`; **no arm was ever run**. **OVERREACH:** the receipts scope to a witness class on a date, never to "public records" generally. |

### 2.1 The assessment's own most instructive finding

The brief for this paper carried a wrong percentage (78–83% for 75.0–82.5%) and an uncorroborated
count (311/480) into a paper proposal. Both sit in the same hand-written addendum of
`PC_R6_OUTCOME_RECEIPT.md`, immediately below a marker stating that everything past that line is not
machine-generated. Neither was caught until this assessment re-read the source.

This cuts **both ways**, and honesty requires recording both:

- It is the best single demonstration of the proposed thesis. A number crossed from an unverified
  annotation into a scientific brief because nothing in the pipeline distinguished machine-generated
  receipt content from hand-written commentary. That is exactly a silent failure.
- It is also a direct demonstration of criterion 7. The programme generated the defect, briefed it,
  and caught it — all inside itself. A self-observed corpus cannot establish the prevalence or the
  efficacy of anything, because the observer is the instrument. The finding therefore strengthens the
  *motivation* and simultaneously destroys the *evidentiary* case for a self-reported paper.

The correct disposition is a repository guard (mark machine-generated receipt regions and refuse to
cite across the marker), not a manuscript.

---


### 2.2 Instances that arrived after the assessment opened

While this assessment was being written, seven further candidate modes were routed to it from five
lanes. They are recorded because they change the assessment's facts and its revival design — and
because what they do *not* change is the finding that matters most.

| # | Mode | Source | Status |
|---|---|---|---|
| 7 | **Non-reproducible "frozen" artifact.** RNG draws ordered by iteration over an unordered `set`; per-process string-hash randomisation regenerates a *different* split from the *same* committed seed, while every seed record, sha256 and freeze receipt stays internally consistent and correct. | PR #181 (**open**) | **VERIFIED, one correction.** Three RNG-consuming set iterations, but all three are call sites in **one** function `_plant`, not "three planters"; the receipt's own wording is loose here. Mechanism confirmed by direct demonstration: the RNG sequence is unchanged, but hash order **binds those values to different keys**, after which the streams desynchronise. Custody mechanism is `load_authorized_seed()`, which binds the *seed string* and never the artifact generated from it — blind by construction. **Near-miss:** no protected artifact has ever existed on that branch. |
| 8 | **Vacuous comparison.** Treatment arm and strongest-parent comparator dispatched to the same code, so a reported `1.000 vs 1.000` was `x == x`; said to vacate 8 of 11 gates. | PR #176 (**open**) | **LANE-REPORTED, not independently verified here.** Pre-freeze. |
| 9 | **A defect that would have favoured the programme's own hypothesis** — a metadata error scoring as an advantage over the parents, routable to a spurious positive. | PR #176 (**open**) | **LANE-REPORTED.** Pre-freeze. Assessed in §7. |
| 10 | **Calibrating on a proxy while the reported primary was saturated** — the difficulty ladder sat inside its registered window on a proxy measure while the endpoint actually reported was at 1.0. | ME-F1 (pre-freeze) | **LANE-REPORTED.** Same shape as bundle 4, caught before rather than after. |
| 11 | **Dateless current-state fields leaking the future into a retrospective split** — `cited_by_count` truncated at fetch date; OpenAlex `is_retracted` a dateless boolean. | ME-X6/7 scoping | **LANE-REPORTED.** No build existed. |
| 13 | **A rendered summary standing in for a fact.** `gh run list` rendered in-progress runs as `[time]` (elapsed time); read as "timed out", the repair would have been to weaken or split a test suite that was never failing. | ME-X6/7 | **LANE-REPORTED.** No artifact touched, no result affected — the cleanest near-miss on record. Caught by a standing rule against trusting filtered command output for anything driving a decision. |
| 12 | **A sentence nobody had executed** — "results and custody files are byte-identical on re-run" had never been tested by re-running. On execution, results and custody *were* byte-identical; the analysis file was not, because it quotes per-arm `wall_ms`. | ME-X6/7 | **LANE-REPORTED.** The underlying artifact was substantively correct: the claim was wider than the check, not false. |

**Every one of modes 7–13 is a near-miss.** None produced a contaminated result.
That is the opposite of a strengthening: a corpus increasingly composed of failures caught before
they did anything cannot support a prevalence claim, and a paper built on it would be reporting that
a careful programme is careful.

### 2.3 One instance found by this assessment's own verification

The guard written against mode 7 is parametrized over `PYTHONHASHSEED` values `0`, `1` and `12345`,
comparing each against a run at `0`. The `0` case therefore compares a process against **itself** and
passes unconditionally, including on the unfixed code. Two of the three parametrizations are
load-bearing; the third is vacuous. The guard against vacuity contains a vacuous parametrization —
found not by review but by a verifier asked to check whether the test could fail.

---

### 2.4 The organizing principle, and why it does not open the paper

One lane, having found the same fault three times in three disguises in its own work, produced the
generalization the six original bundles lacked. In its words: the vacuous gates were *counters that
never ran*; the comparator was *a contrast that could not exist*; the sentence was *a claim nobody
had executed* — and all three read as strength in a receipt (`0 violations`, `1.000 vs 1.000`,
"byte-identical on re-run"). Generalized: **the artifacts that certify correctness — gates,
comparators, custody records and the prose describing them — are themselves unverified claims until
something executes them, and each fails in the direction that looks like strength.** The framing is
that lane's and must be credited to it wherever it is used.

This is a genuine advance and it is a better object than a list of modes. It explains why review does
not catch these (a reviewer checks whether a claim is *defensible*, not whether it was *executed*),
it predicts where to look, and it yields a detector *family* rather than a list. It also corrects one
of the original five detectors, and the correction is sharp: **asking for the denominator is
structurally blind to the vacuous comparison.** A gate that never ran reports `0`, which becomes
suspicious the moment you ask "out of how many?" A comparator with no contrast reports `1.000`, which
reads as strength, and **there is no denominator to ask for**. The question that catches it is
different in kind — *could these two arms ever have differed?* Anyone who takes "report the
denominator" as the general lesson will still ship a study comparing a function to itself.

**Mode 13 completes the principle in the other direction, and the completion matters.** The three
surfaces above are certifying artifacts that read as *strength* and are therefore never examined.
A rendered summary can equally read as *failure* and provoke a repair of something that was working.
A programme that degrades its own instruments in response to display artifacts looks, in its
receipts, exactly like a programme responding responsibly to problems. So the claim is bidirectional:
*a rendered summary standing in for a fact nobody executed*, failing toward apparent strength when it
is a claim and toward apparent failure when it is a display. The detector is symmetric — before
acting on a summary, execute the thing it summarises; ask both what would have to run for this to be
false **and** what would have to run for it to be true, the second being what stops you repairing a
healthy artifact.

Note what caught it, because it cuts against the paper rather than for it: a **pre-existing standing
rule** in this programme's own operating instructions — never assert absence from absent printed
output, and use the unfiltered binary for any command whose result drives a decision. The detector
was not discovered here; it was already written down, and it generalized to a novel instance exactly
as a good rule should. That is the best evidence in the whole corpus that these detectors work, and
it is simultaneously evidence that they are already held.

**And it moves not one blocking criterion.** §6 records that criteria 3, 4, 6 and 7 are not fixable
by adding instances. They are equally unfixable by a better organizing principle. A sharper thesis
raises what the paper would be worth *if the evidence existed*; it does not create evidence. There is
still no prospective discriminator, still no false-alarm rate, still no evaluation outside ORION-V2,
still no independent authority. Six further instances and a superior framing arrived, and the gate
reads exactly as it did before — which is the strongest available evidence that the gate is measuring
the right thing.

The principle's proper use is therefore **§8**: it specifies the revival design far better than the
original list did, by naming the surfaces a planted-defect study must cover.

**This assessment is closed to further instances.** Seven arrived while it was being written and the
gate did not move, because instances were never the binding constraint — criteria 3, 4, 6 and 7 are.
Further modes should go to `FAILURE_LEDGER.md`, which is the programme's append-only register for
exactly this and is bound to running code, and to the lane PRs that own them. A successor reopening
this object needs the study in §8, not a fourteenth mode.

---

## 3. The reduction: the nominated bundles are not one object

The proposed paper's appeal rests on the six bundles sharing a mechanic. They do not.

**Spine (five instances of one mechanic).** Bundles 2A, 2B, 2C, 4 and 5 are all the same thing: *a
check reported PASS while the number of instances it actually evaluated was near zero, and that
number was never reported beside the verdict.* An applicability guard that excluded the family under
test; an assertion matching a string the renderer never emits; a check flat by construction; an
outcome dominated by patch-application failures rather than by the quantity of interest; control
verdicts computed and reported but not consumed by the terminal. In every case the missing artefact
is the **denominator of the check**.

**Not on the spine.** Bundle 1 (control-induced exploration collapse) is not a gate defect at all —
it is a substantive result about what a reproducibility mandate does to a search process. Bundle 6
(confounded case selection) is a sampling-frame result. Neither is a silent-verification failure;
they were nominated because they were surprising, not because they share the mechanic.

This matters because **bundle 1 is the strongest finding and it is the one that does not belong.**
A paper built on the spine must drop its headline; a paper built around bundle 1 is a different
paper with a different parent set, one instance, and no detector. The object as proposed is at least
two things, and neither half survives §5–§6 on its own.

**The later arrivals confirm this rather than repairing it.** Modes 7–13 add a custody mechanism that
certifies honestly without delivering reproducibility, a comparison with no possible contrast, an
operational multi-agent hazard, a proxy-versus-primary calibration error, a data-selection leak, and
an unexecuted sentence. Counting the two original non-spine items, the nominated set now spans at
least five distinct kinds of object. §2.4's principle is the one thing that genuinely unifies a
subset of them — the check, the contrast and the claim — and it explicitly does **not** cover
exploration collapse, the sampling confound or the process-kill hazard. Those three should not be
carried by any successor: the process-kill item in particular is an operational hazard, not a silent
verification failure, and including it would repeat the exact error this section identifies —
bundling unlike things because each was surprising.

---

## 4. Ownership: overlap against the six existing manuscripts

The portfolio's rule is `PAPER_OVERLAP_AND_DISCLOSURE_MATRIX_V1.md` §3: *"A distinct analysis of
identical data is not automatically a distinct paper."* Applied bundle by bundle:

| Bundle | Existing owner | Status |
|---|---|---|
| 2A — applicability guard excluded the family under test | **PRA / #51** | **CLAIMED IN MANUSCRIPT.** PRA V16 Appendix B.8 reports the sweep, both denominators, the failure counts and the correction verbatim. V16 has since merged to ORION-paper `origin/main` as `3e2e22e` (PR #80). Owned, landed, and not available as a new result. |
| 1 — control-induced exploration collapse (E40 Stage-2d) | **P-C** | E40 is P-C's evidence line; the seed-replica probe is one of P-C's three prospectively licensed follow-ups. Stage-2d is a diagnostic *within* that lineage. |
| 4 — the null that measured serialization | **P-C** | P-C anticipated this at the E20 pilot and pre-specified the separation into E30; the E30-R11 terminal is imported into P-C V7. |
| 5 — terminal emitted while its control failed (Stage-2c) | **P-C** | Same lineage as bundle 1; the Stage-2c disposition `CHECKER_INVALID__NO_VERDICT` is a P-C-line receipt. |
| 6 — confounded naturalistic case selection (SD80) | **P-C** | P-C V10 prospectively specifies exactly this design: an obligation-vs-obligation-free comparison "on externally authored, verifiable constraints … with internally generated constraints as a negative-control stratum". SD80 is its execution. |
| 2B — CI assertion matching text LaTeX never emits | *(unowned)* | Repository/CI hygiene. No manuscript claims it; equally, no manuscript would. |
| 2C — horizon check flat by construction | **PRA** | Same audit family as 2A (Appendix B.3–B.4 horizon curve). |

**FLAGSHIP, P-A, P-B, P-D:** no bundle is owned by these, and none supplies them evidence. That is
not an argument for a new paper — it means the object is concentrated in exactly the two manuscripts
that already own it.

**Net:** five of seven items are owned by PRA or P-C; the strongest is already written into a
manuscript another lane is landing; the single unowned item is a CI string-matching bug whose own fix
is still on an open branch. There is no residue that a new manuscript would carry.

**The programme also already owns the *synthesis*.** `FAILURE_LEDGER.md` on the merged head is an
append-only register of exactly these classes, each with a named guard and a first-observed date:
`SILENT_MODEL_SUBSTITUTION` (bundle 3), `MANDATE_EXPLORATION_COLLAPSE` (bundle 1),
`UNGATED_CONTROL_VERDICT` (bundle 5), `DEGENERATE_PROBE_STATISTIC`, alongside `NONIDENTIFIABLE`,
`CENSORED_ROUTE` and `AUTHORITY_LAUNDERING`. The proposed paper's contribution — a taxonomy of silent
failure modes with a detector for each — is the artifact the programme has been maintaining all
along, and it is maintained better there than a manuscript could maintain it, because it is
append-only and bound to running code.

---

## 5. Strongest-parent reduction

Each proposed detector has a mature owner outside the programme, and — decisively — **inside it**.

**Inside the programme.** The detectors are not discoveries; they are the programme's own registered
operating procedure. `research/experiments/pc-r6/PC_R6_DISPATCH_RECEIPT_V1.md` guard A6 registers
the denominator requirement prospectively, complete with the phrase *"a vacuous zero-count pass"*,
and its outcome receipt reports *"The endpoint is **not vacuous**"* as a standard endpoint check.
PRA's Appendix B.7 (`llm_epistemics_mutation_audit.py`) already runs assumption mutations to confirm
that load-bearing assumptions can fail — that is the planted-positive detector, executed and
reported. A paper claiming these detectors as its contribution would be reporting its own house
style as a finding.

**Outside the programme.** Reduced at field level: vacuity detection in temporal model checking and
coverage metrics for formal verification own the denominator detector; mutation testing, metamorphic
testing and known-answer self-tests own the planted-positive detector; provenance and
environment-capture practice owns the served-identifier detector; the preregistration critique owns
the constraint-reduces-exploration result; fail-closed design in dependable systems owns the
consume-your-controls detector; and benchmark construct-validity work owns the
measured-the-wrong-thing null.

### 5.1 Parent reduction, with verification status

A literature pass was run against reproducibility, silent-error, benchmark-validity and
evaluation-artefact work. Two findings are decisive and are recorded with their verification status,
because a wrong citation in a strongest-parent section is worse than an absent one.

**Verified independently (two sources).** Kupferman, *Sanity Checks in Formal Verification*, CONCUR
2006, LNCS 4137:37–51 — already unifies vacuity and coverage as one mutation framework: mutations in
the specification give vacuity, mutations in the system give coverage. **That is precisely the
generalization the proposed paper would make**, published twenty years earlier, and it subsumes the
denominator detector and the planted-positive detector under a single mechanism. This single
citation closes the object's claim to a unifying contribution.

**The empirical-census slot is already occupied — verified at source.** Beer, Ben-David, Eisner and
Rodeh, *Efficient Detection of Vacuity in Temporal Model Checking*, Formal Methods in System Design
18(2):141–163, 2001 (DOI 10.1023/A:1008779610539), p. 141, read from the primary PDF:

> "Several years of experience in practical formal verification of hardware at IBM [3] have shown us
> that during the first formal verification runs of a new hardware design, typically 20% of formulas
> are found to be trivially valid, and that trivial validity always points to a real problem in
> either the design or its specification or environment. Of the formulas which are found to be
> non-trivially valid, examination of a non-trivial example trace discovers a problem for
> approximately 10% of the formulas."

That is a stronger statement than anything the proposed paper offers: a rate, a population, and the
claim that such passes *always* indicate a real defect. Its limitation survives verification and must
be stated with it — this is an IBM RuleBase experience report, not a methodologically specified
census. A later systematic study occupies the same slot: *Vacuity in practice: temporal antecedent
failure*, FMSD 46(1), 2015 (DOI 10.1007/s10703-014-0221-0).

*Secondary, unverified.* The form of this quotation that circulates in the later literature
("typically 20% of specifications pass vacuously … vacuous passes always point to a real problem") is
reported to appear in quotation marks in Kupferman 2006 attributed to Beer et al., and does not match
the FMSD 2001 wording above — possibly quoting the differently-titled CAV'97 predecessor. This could
not be checked at source here. It is recorded only as a caution: a successor citing the 20% figure
should bind the wording above, to FMSD 2001, page 141.

**Field-level reduction, citations not bound.** Each remaining detector reduces to a mature field:
checked-coverage and oracle-quality work for the denominator detector; mutation testing, metamorphic
testing, target-decoy/known-answer self-tests and saliency sanity checks for the planted-positive
detector; software attestation, reproducible builds and API-response provenance for the
served-identifier detector — note that at least one major LLM provider already returns the resolved
model snapshot in the response body, making that "detector" the reading of a documented field;
runtime *enforcement* (as opposed to runtime *verification*) and clinical-laboratory run-rejection
rules for the consume-your-controls detector; and agentic-benchmark construct validity for the
measured-the-wrong-thing null.

```text
PARENT_CITATIONS      = PARTIALLY_BOUND
VERIFIED_INDEPENDENTLY = Kupferman 2006 (D1+D2 unification)
VERIFIED_AT_SOURCE     = Beer et al. 2001 p.141 — the 20% rate, quoted above
IDENTITY_CONFIRMED     = Vacuity in practice, FMSD 46(1), 2015
UNVERIFIED_AT_SOURCE   = the Kupferman-rendering quotation mismatch; all agentic-benchmark
                         census figures; the preregistration-and-exploration evidence of §7
DO_NOT_BIND            = any citation above without checking it at source first
```

**Conclusion.** The strongest donor composition — vacuity/coverage checking, known-answer and
mutation testing, attestation and environment capture, and enforcement-not-observation gating —
catches every spine instance, and the census the paper would offer has already been reported in at
least one field. The residual is empty.

### 5.2 "The detectors are already merged" — the strongest argument for the paper, audited

The most attractive feature of the proposal is that several detectors are implemented, merged, and
fixture-proved. Verified, the tally is weaker than briefed:

| Detector | Status on a merged main |
|---|---|
| Assert the **served** model id, fail closed | **MERGED, fixture-proved.** `assert_served_model()` with a self-test asserting rejection of four wrong ids. |
| **Consume** control verdicts; refuse every gate when one fails | **MERGED, fixture-proved.** PR #169 `b42bf470`, with fixtures proving the refusal fires for a substituted served id and a corrupted plant. Deliberately not retrofitted to the frozen script. |
| Report the **denominator** beside the violation count | **MERGED** in ORION-V2 (`c30f1827`, PR #166) — whose commit title is literally *"report the (ii) Fano-form check against an honest denominator"*. |
| Pair a no-alarm assertion with a **planted positive** | Partly pre-existing as PRA Appendix B.7 assumption mutations; **not generalized** into a pipeline-wide rule. |
| Fix the vacuous CI render assertion | **NOT MERGED.** ORION-paper PR #43 is open; `main` still carries the defective pattern. |
| Repair the flat horizon check | **NOT REPAIRED.** The claim was withdrawn instead (`4e951d75`); the check is unchanged and still cannot fail. |

Three of six merged, one partial, one branch-only, one never repaired. That is respectable engineering
hygiene. It is not the "detectors demonstrated to work" evidence a methods claim needs, because no
detector has been measured against a false-alarm rate or against a defect it did not already know
about.

### 5.3 Archetype resolution is moot, and why that had to be checked

The task required resolving the archetype independently — reproducibility/evaluation venue, Comment
or Perspective, methods track — rather than assuming one. It was checked, and the answer is that it
does not matter, because the blocking failures are archetype-independent:

- **Ownership** (§4) blocks equally in a Comment, a methods paper and an experience report; a Comment
  may not re-report another in-flight manuscript's corrected appendix as its news.
- **Uncontrolled selection** (§7) blocks any prevalence claim in any venue. The observable population
  is "silent failures eventually caught"; the population of interest is its complement.
- **Self-observation** (criterion 7) blocks any efficacy claim in any venue.

An experience report is the archetype whose criteria this object comes closest to satisfying, and it
still fails all three. Resolving the venue more finely would change nothing, so no venue is
recommended and no target adapter was invoked.

---

## 6. The programme's seven-point selection rule, walked literally

`PROGRAMME_LEDGER_V0.md`: *"A candidate survives only if it has:"*

**(1) a distinct scientific object not already owned by V1.** **FAIL.** §4: five of seven items are
owned by PRA or P-C, and the strongest has now merged into PRA's manuscript.

**(2) faithful reconstruction of strongest parent fields.** **NOT DONE.** §5.1 reduces at field
level and binds one parent; no field is *reconstructed*. This is the one criterion that is
recoverable with work — and §5.1 indicates that doing the work closes the candidate faster.

**(3) an explicit strongest donor-composed baseline.** **FAIL.** §5.1: the composition dominates,
and one prior framework already unifies two of the five detectors under a single mechanism. This is
not a gap to be filled — filling it is what closed the candidate.

**(4) a prospective quantitative/formal discriminator.** **FAIL.** All six bundles are retrospective
discoveries. Stage-2d is the only prospectively registered member, and it was registered to
discriminate a *cause* (model channel vs mandate), not to test a detector's efficacy. There is no
registered quantity on which the proposed contribution could be wrong.

**(5) hostile controls and honest negative terminals.** **FAIL at the paper level.** The individual
receipts carry controls; the *paper's* claim carries none. No false-alarm rate is measured for any
detector, and no estimate exists of how many silent failures remain uncaught — which is the quantity
that would decide whether the detectors work. A detector reported without its false-positive rate is
the same defect the paper is about.

**(6) fresh evaluation outside derivation domains.** **FAIL, structurally.** Every instance is drawn
from inside ORION-V2. There is no outside, and none can be manufactured from the existing corpus.

**(7) independent scientific and publication authority.** **FAIL.** The object is self-observed and
self-reviewed. The defects passed the programme's own review before its own later gates caught
them — which is the honest headline, and also the reason a self-report cannot settle it.

```text
CRITERIA_MET = 0 clean, 1 partial (2, recoverable), 6 FAIL
```

Criteria 3, 4, 6 and 7 are **not fixable by adding instances**. Finding a seventh or a tenth silent
failure inside the same programme improves none of them. That is the load-bearing reason the verdict
is `DO_NOT_OPEN` rather than `DEFER_PENDING_MORE_EVIDENCE`.

---

## 7. The limits that would have to be stated, and are not survivable

Recorded here so that no successor re-derives them:

- **N=1 programme, self-observed.** One pipeline, one operator, one review process.
- **Bundle 1 is n=1 per arm.** Three arms, nine cycles, one run each, 27 model calls, temperature 0,
  no replicate and no interval. The monotone dose-response is three trajectories at three dose
  levels. Its own receipt refuses the generalization a paper would want, filing the live-arm
  implication as *"a consequence a future freeze must confront (not a claim here)"* and stating that
  testing it *"requires a mandate-free replica design — a new prospective identity."*
- **Bundle 1's cause is an interaction that cannot be estimated.** The regime-anchor arm passed under
  an earlier model and fails under the current one; the earlier model is unrecoverable, so no
  interaction estimate exists or can be recovered.
- **Selection is uncontrolled.** The six bundles are the silent failures that were *eventually
  caught*. The population of interest is the ones that were not, and it is unobserved by
  construction. Nothing in the corpus bounds it.
- **Collecting this corpus for a paper has contaminated the corpus.** Lanes are now finding,
  disclosing and framing silent failures while knowing a paper is being assessed from them. That
  changes what is looked for, what is reported and how it is worded — and it is unmeasurable from
  inside. The programme has a manuscript about exactly this failure: P-D's C09 coordinate holds that
  evaluation "can alter the systems, researchers, agents or data-generating processes being
  evaluated" and that a measured relationship may not be treated as stable until that response is
  modelled. No such model exists here, and the corpus was assembled precisely in the way P-D warns
  against. This is the deepest reason the object cannot be its own evidence, and it is a P-D-owned
  argument rather than a new one.
- **The corpus is now dominated by near-misses.** Of the thirteen modes on record, seven were caught
  before any protected artifact existed and produced no contaminated result. Prevalence cannot be
  estimated from a sample selected on "was noticed, was survivable, and was volunteered", and the
  volunteering is itself the point: several modes exist in the record only because a lane disclosed
  a hazard that left no trace in its own artifacts. That is admirable practice and worthless as a
  denominator.
- **Bundle 1's headline runs against the external evidence.** The literature pass found **no
  peer-reviewed empirical support** for the proposition that a preregistration-style constraint
  reduces exploration, and one quantitative data point pointing the *other* way (more exploratory
  work under Registered Reports than in matched traditional articles). That source is thesis-level
  and was not verified at source, so it settles nothing on its own — but a paper whose headline is
  "a reproducibility control destroyed exploration" would meet a literature that currently leans
  against it, on n=1 per arm. This must be reconciled before, not during, review.

The last point is fatal on its own for any prevalence or efficacy claim, and it is not repaired by
better writing.

---

## 8. Revival: the one design that would change this verdict

Per the programme's diagnose-then-revive rule, the failure is attributed to a single stage —
**there is no prospective discriminator and no measured detector efficacy** — and the matching lever
is a study, not a manuscript.

**SFM-D1 — planted-defect detector-efficacy study (not executed; not authorized here).**

Freeze a defect taxonomy from the **three surfaces** §2.4 identifies, because a study that plants
only the first will validate a detector that is blind to the second:

1. *the check* — guard-excluded family; never-matching assertion; constant-by-construction check;
   unconsumed control verdict. Detector: report instances-evaluated beside violations.
2. *the contrast* — two arms sharing a code path, so the comparison is `x == x`. Detector: assert the
   arms' code paths diverge, and report shared-implementation comparisons as shared rather than
   counting them as independent evidence. **The denominator question does not catch this**, which is
   why the study must plant both and measure them separately.
3. *the claim* — a sentence in a receipt or design that nothing has ever executed. Detector: for each
   certifying claim, name what would have to run for it to be false, and make that run. Plant a registered number of each into
a pipeline whose true defect set is known by construction. Run the pipeline under two arms —
detectors off, detectors on — and report detection rate, **false-alarm rate on a clean control**, and
time-to-detection, against a strongest donor-composed arm (vacuity checking + mutation/known-answer
testing + environment capture + fail-closed gating) rather than against no-detector alone. Register
the discriminator before execution. Execute on at least one pipeline **outside ORION-V2**, since
criterion 6 cannot be met inside it — what would count is an external research or evaluation harness
with public CI, a public defect history and an owner willing to have plants injected (an open-source
agentic-benchmark harness, or a collaborator's pipeline under agreement). No such pipeline is
identified yet, and identifying one is the design's first blocking step.

Honest terminals to register with the design:

```text
DONOR_COMPOSITION_SUFFICIENT          — the parents already catch them; no paper
DETECTOR_RESIDUAL_ON_PLANTED_ONLY     — works on plants, unvalidated in the wild; methods note only
FALSE_ALARM_RATE_TOO_HIGH             — the detectors get switched off; negative
DETECTOR_RESIDUAL_WITH_FRESH_DOMAIN   — the only terminal that admits a paper
CANNOT_CHECK
```

Until SFM-D1 or an equivalent runs, no manuscript may report the six bundles as evidence that the
detectors work. They are evidence that five checks were vacuous, which their own receipts already
say, in the papers that already own them.

---

## 9. Disposition and required actions

```text
NEW_STANDALONE_PAPER      = DO_NOT_OPEN
BUNDLE_2A, 2C             = OWNED_BY_PRA__ALREADY_IN_MANUSCRIPT__NO_ACTION
BUNDLE_1, 4, 5, 6         = OWNED_BY_P_C_LINEAGE__CITE_IN_PLACE__NO_NEW_CLAIM
BUNDLE_2B                 = REPOSITORY_HYGIENE__NOT_A_SCIENTIFIC_CLAIM
DETECTORS                 = ALREADY_PROGRAMME_OPERATING_PROCEDURE__KEEP__DO_NOT_CLAIM_AS_RESULT
REVIVAL                   = SFM-D1 (§8) — prospective, external, not authorized by this assessment
FLAGSHIP_USE              = a bounded methodological aside at most, subject to the Perspective's
                            own overlap policy; never as evidence of a discovered law
```

No registry row is added and no `v2-papers/` subtree is created, because no paper is admitted. This
assessment is the artifact; it is committed whatever the verdict, as the gate requires.

**Authority note.** This assessment resolves admission only. It does not close the underlying
findings, none of which is disputed, and it does not license SFM-D1.

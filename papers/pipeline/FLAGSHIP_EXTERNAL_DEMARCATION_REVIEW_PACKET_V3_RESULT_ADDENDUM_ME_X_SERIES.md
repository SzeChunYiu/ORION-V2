# Result Addendum to Demarcation Review Packet V3 — ME-X4, ME-X1 and ME-X2 Frozen Outcomes

**Addendum date:** 2026-09-02
**Adds to:** `FLAGSHIP_EXTERNAL_DEMARCATION_REVIEW_PACKET_V3_V21.md` (`Review status: outcome-blind packet`)
**Status:** post-outcome addendum. **The V3 pre-outcome questions D1–D18 remain frozen and are NOT modified, reordered, weakened, reinterpreted or re-scored by this file.** Nothing before this addendum is rewritten. This file appends three frozen outcomes that the packet withheld, and asks whether they change your judgement.

---

## 0. Why you are receiving this

Packet V3 was written outcome-blind, on purpose. Its §10 listed the study designs that existed and stated plainly that their outcomes were withheld so that the judgement it requested would be a pre-outcome judgement. At packet date, ME-X4's protected stage had not run and ME-X1/ME-X2 were prospective.

They have now run. All three went against the proposal, and one went against it harder than a tie. **Withholding them from you would now be the defect, not the discipline.** They are supplied here in full terminal form.

You may answer D1–D18 before reading this addendum, after reading it, or both. If your answers differ, say so — that difference is itself informative and we would rather have it than a single reconciled answer.

## 1. What ran

Three pre-registered exact-oracle studies. In each, instances carry a decision an independent oracle computes; no arm may read that oracle; every gate, arm, ablation, precedence rule and stopping rule was frozen and hash-deposited **before** the protected split existed; each ran **exactly once** on a seed committed in its own design; and no design constant, gate, arm, oracle rule or precedence was changed after an outcome was seen. Each receipt reveals its seed so the split regenerates byte-for-byte.

The primary comparator in all three is `B5`, the **strongest faithful parent federation**: the same mature modules the proposed controller draws on — provenance, dependence assessment, typed transport, measurement comparability, evaluator coverage, an authority lattice, truth-maintenance propagation, consistency-based diagnosis, expected-cost test sequencing — connected by ordinary engineering glue and given the same information at witness level.

| Study | Design / receipt merge | Route | Result against the controller |
|---|---|---|---|
| **ME-X4** selective reopening under dynamic evidence, 1,200 instances, 12 strata | `ee32108` / `4929a44` | `PARENT_SUFFICIENT` | B5 reproduced the controller's reopened / preserved / unresolved decisions **1,200 / 1,200**, 0 discordant in every stratum. Ladder monotone, **rung-5 gap 0** |
| **ME-X1** cross-transition coupling, 1,000 instances, 10 families | `0fde96f` / `59b1f5b` | `PARENT_SUFFICIENT` | B5 reproduced the controller's action **and** reopened set **1,000 / 1,000**, 0 discordant in every family. Exactly one significant ladder step, R4→R5, **+29 / −0, p = 3.7 × 10⁻⁹**. Protocol §10 requirement 2 (a systematic composition error by B5) **explicitly not satisfied** |
| **ME-X2** obstruction locus and minimum escalation, 1,200 instances, 12 obstruction classes of unequal n | `704d379` / `776d3a1` | **`PARENT_SUFFICIENT (B5_DOMINATES)`** | B5 **beat** the controller: **0.983 vs 0.963**, paired difference −0.020, exact **p = 0.0032**, 95% CI [−0.033, −0.007] |

A precision point, since the three rows otherwise read as parallel: ME-X4's twelve strata carry 100 instances each and ME-X1's ten families carry 100 each, but ME-X2's twelve strata are **oracle classes with unequal n** (140, 55, 63, 91, 113, 277, 71, 80, 69, 123, 68, 50), as its receipt §4 states in its header and note. Its design text says "50 pairs per stratum"; the receipt records a pre-merge re-stratification the design text does not, and the receipt is the authority for what ran.

Receipts, in `SzeChunYiu/ORION-V2`: `research/experiments/me-x4/ME_X4_OUTCOME_RECEIPT.md`, `research/experiments/me-x1/ME_X1_OUTCOME_RECEIPT.md`, `research/experiments/me-x2/ME_X2_OUTCOME_RECEIPT.md`.

## 2. The ME-X2 mechanism, stated without softening

Of 62 discordant instances, **all 43 the federation won are the controller declaring `CANNOT_IDENTIFY` on an episode that was in fact decidable**, and **all 19 the controller won are the federation escalating above the level the oracle required**. The controller's conservatism is not a virtue that happens to accompany a loss; it **is** the loss.

It does buy something measurable, on separate axes: **0** false escalations against the federation's **21**, and **140/140** correct `CANNOT_IDENTIFY` against the federation's **135/140**, with lower mean regret. On this endpoint it costs more than it buys.

Its cause is two orderings the reference semantics leave open, both registered in the design **before** the run: take the *cheapest* admissible discriminating action with no lookahead, and treat reachability as *fail-closed over every live hypothesis*. Both were seen in a pre-merge dry run on a public seed and deliberately **not repaired**, because repairing them after observing that they lose would be tuning an outcome. Two revival levers are registered as a separate design that must be frozen before it runs; they are not claimed here.

## 3. Two things this addendum will not let you be misled about

**(a) ME-X2's H-EXT-3 label is not a third vote.** All three receipts print the ladder terminal `RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL`. In ME-X2 that label is computed as the negation of the advantage gate, so it fires on a tie **and** on a federation win; there it is the weaker of the two statements it sits beside. ME-X1 and ME-X4 support the interface-standard reading on their ladders. ME-X2 supports the contraction, but **not** that specific terminal. Please do not read three matching labels as three matching findings.

**(b) The negative does not generalise as far as it looks.** ME-X2's world has **uniform decidability** and **strictly increasing cost bands**, which make an exact expected-cost planner optimal *by construction*; its episodes are synthetic, its outcome tables registered, its prior uniform across arms. The honest statement is *no residual is detectable in a registered decision problem the parents already solve exactly*, **not** *no residual exists*. All three studies are known-answer worlds with finite registered action sets; every naturalistic cell is a separate, unexecuted identity; **four of seven** registered families have not run.

**Also not claimed:** any cost route. Two studies flag the controller ≈2× faster in wall clock, the third ≈2× slower; all three receipts refuse cost as a route to any claim.

## 4. What the same runs show is real

Supplied because a packet that carried only the negative would mislead in the other direction.

- On ME-X1's protected instances the direct arm **laundered 492 unwarranted updates**. The strongest **truth-maintenance** federation still laundered **163** and scored **0.837**, failing on exactly the four conditions that are not truth-maintenance objects: **authority ceilings, specification fidelity, criterion identity, and the atlas witness** that separates pairwise compatibility from a global section.
- The interface-information residual is real but **localised, and generator-dependent**: ME-X4 gains at rung 2 (provenance records, 30 instances) and rung 4 (typed transport and evaluator statuses, 9); ME-X1 is flat through rung 4 and puts everything in R4→R5 (identity / criterion / specification, 29); ME-X2 is monotone with every step significant. No single study's ladder generalises to the others.
- Verdict-only exchange is **world-dependent**: in ME-X1 safe but imprecise (0 laundering; all 29 misses action-granularity), in ME-X2 **not safe at all** (93 false escalations, 7 specification damages, 0/140 undecidable episodes left open). A finite hand-authored separation pair shows it can be outright wrong.

## 5. What the authors did in response

The manuscript this packet binds has been **retitled and contracted**, applying the programme's own frozen kill condition. It is now *Warranted Scientific-State Transitions: An interface standard and benchmark for reliable agentic science*, it states in its main text that a distinct field is **not established and should not be claimed on this evidence**, and its surviving contribution is an interface standard plus an executable benchmark.

This is disclosed so you can see what was done with the outcomes. **It is not a request to endorse the contraction, and it does not narrow your terminal choice.** The manuscript V3 binds you to (V21) is unchanged and remains the object of D1–D18; the contracted manuscript is available on request if you would rather assess the current text.

## 6. The terminal set

The seven terminals frozen by the external-review gate are unchanged and none is removed:

```text
CANDIDATE_FIELD_DEMARCATION_SUPPORTED
USEFUL_INTERDISCIPLINARY_RESEARCH_PROGRAMME
INTEGRATION_ENGINEERING_ONLY
SUBFIELD_OF_EXISTING_PARENT
RENAME_SCIENTIFIC_PROGRAMME
FIELD_BOUNDARY_TOO_FRAGMENTED
CANNOT_CHECK_FIELD_SEPARATION
```

What changes is only what the evidence now makes **live**. At packet date, `INTEGRATION_ENGINEERING_ONLY` was one of seven abstract options. On three protected runs in which an information-matched composition of mature parents reproduced the proposed controller's decisions twice and decided better than it once, **that terminal is now plausibly correct and should be weighed as such.** `SUBFIELD_OF_EXISTING_PARENT` and `RENAME_AND_CONTRACT` are correspondingly more live.

No terminal is preferred, none is excluded, and `CANNOT_CHECK_FIELD_SEPARATION` remains a valid and useful answer. In particular, an assessment that the surviving interface standard is **ordinary integration engineering** is exactly the judgement the authors are not entitled to make for themselves, and is the one this addendum most needs from you.

## 7. One added question, frozen from this date

D1–D18 are unchanged. This addendum adds a single question, and it is the only one it adds.

#### D19 — Does the interface standard survive its own negative?

Three protected runs show that once mature parent modules exchange typed, witness-level structure, an information-matched federation makes the same scientific-transition decisions as the proposed controller, and on one registered problem makes better ones. The authors keep two things from that: a **specification of what must cross a module boundary**, and an **executable benchmark** with a strongest-parent null and an exchange ladder.

- `INTERFACE_STANDARD_IS_A_SCIENTIFIC_CONTRIBUTION`
- `INTERFACE_STANDARD_IS_ORDINARY_INTEGRATION_ENGINEERING`
- `BENCHMARK_IS_THE_ONLY_CONTRIBUTION`
- `NEITHER_SURVIVES`
- `CANNOT_CHECK`

If you choose either of the first two, please name the nearest existing standard or practice you are measuring it against — W3C PROV, assurance cases, IV&V, TMS/ATMS labelling, or another — and say what, if anything, the proposal adds to it.

## 8. Custody

Every artifact referenced here is public in `SzeChunYiu/ORION-V2` at the merge commits given in §1. Each receipt records that its protected split ran exactly once, that the runner verified the frozen seed commitment before generating, and that no design constant was changed after an outcome was seen. One honest limit, stated because it bears on how much weight pre-registration should carry with you: **these are commits in a repository the authors control, not an independent registry.** No field status, novelty or publication authority is granted or implied by this addendum.

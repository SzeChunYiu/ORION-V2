# FM80 §9 — execution amendment V2 (frozen 2026-09-07, before any screening or model call)

**Class:** `FROZEN_DESIGN_AMENDMENT__PRE_SCREENING__PRE_OUTCOME`.
**Authority:** none. This document selects and freezes design choices. It grants no scientific truth, no
P-A/P-B survival, no publication readiness, and no release authorization. `submission_authorized` is
untouched and remains False. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

**Why an amendment is legitimate here, and why it would not be later.** FM80 §9 has **never produced a
verdict** and Stage A has **never been dispatched** — no arm has run, no case has been assembled, no
outcome exists to have been read (`fm-exact/FM80_BLOCKED_WITH_REASON_RECEIPT.md`;
`fm80-exec/FM80_EXEC_R11B_DONOR_KEY_ATTRIBUTION_RECEIPT_V1.md`, ORION-V2 #369). Expanding the eligible
pool *before* any outcome is a design act. Expanding it *after* one would be a rescue, and FM80 §10 and
the portfolio's own rescue rules forbid it. The whole value of this document depends on the order in which
it lands, so the order is stated as a binding condition: **this amendment's sha256 is registered and
merged to `main` before any eligibility screening is run against it and before the first model call.**

---

## 1. Repair-branch selection — the outstanding design act, discharged

`FM80_PRE_OUTCOME_DESIGN_CORRECTION_V1.md` established that §9.1's 10 pp bar and §9.2's Holm-adjusted
significance clause are **jointly unsatisfiable** at §8's registered floor of 30 cases per domain: 10 pp
is 3 net cases, the most favourable table consistent with that gives an exact two-sided p of 0.25, and
Holm's rungs are 0.0167 and 0.025. It named three repair branches and deliberately **selected none**,
recording the status as `DEFECT_FOUND_AND_DOCUMENTED__REPAIR_BRANCH_UNSELECTED` because selecting one is
a design act belonging to the executing lane. `PAPER_REGISTRY.json` carries the same
`repair_branch: UNSELECTED__BELONGS_TO_THE_EXECUTING_LANE`.

**This lane is that lane, and it selects Branch 1.**

> **BRANCH 1 — raise the §8 sample floor from 30 to 61 eligible cases per domain (183 total), holding
> §9.1's 10 pp bar and §8's exact paired test unchanged.**

Nothing else in §8 or §9 moves. No threshold is relaxed, no test is swapped, §12 is untouched.

**Why Branch 1 and not the others**, stated so the choice can be argued with:

| branch | what it does | disposition |
|---|---|---|
| **1 — raise the floor to 61/domain** | §8's words are *"**Minimum** target"* — a floor, not a plan. Raising a floor is the one repair that changes no scientific threshold. At n = 61 the ceiling of a 10 pp improvement first reaches a Holm-detectable net count (7 net cases, exact p = 0.0156 against the first rung 0.0167). | **SELECTED** |
| 2 — raise the effect bar to 23.3 pp at n = 30 | honest and free, but it redefines the effect the protocol calls scientifically meaningful as 2.3x larger, purely to fit a sample. It answers a different question than the one FM80 registered. | rejected |
| 3 — swap the exact paired test for a test using concordant pairs | the exact paired test was specified deliberately. Choosing the most permissive branch **after** seeing the reachability analysis is relaxing a frozen protocol, which §12 forbids. It is also the cheapest, which is exactly why it must not be taken for that reason. | rejected, on the correction's own instruction |

**This corrects a live discrepancy, not only a paper one.** `FM80-§9-EXEC` and R11b already compute
against "the registered bar of **61**", and the model-proxy design already states "≥ 61 eligible cases per
domain". The 61 was in the code and in three receipts while the registry said the branch was unselected —
an unfrozen number doing frozen work. After this document, the number the executor uses and the number the
design registers are the same number, and it was chosen on the record rather than inherited.

---

## 2. Domain set — three counting domains, two recorded and not counted

FM80 §2 requires **three materially different domains**: at least one mathematical/formal; one empirical
science testable against measurements, interventions or a frozen empirical benchmark; and a **second**
empirical science with materially different objects, measurement semantics and strongest parent
methodology. §9.1 asks for the effect in **≥ 2 of 3** domains.

R11b established, before any dispatch, that the assembled SD80 pool cannot supply three domains at the
61 bar. Stage A can only *reduce* a domain's eligible count — a case whose proxy proposes no donor is
marked `INELIGIBLE` — so a ceiling below the bar is below the bar under **every** Stage A outcome,
including a perfect one:

| domain | n | checkable ceiling | required Stage A joint yield for 61 | role under this amendment |
|---|---|---|---|---|
| `FORMAL_MATHEMATICS_1000PLUS` | 243 | 243 | 0.251 | **counting — domain 1 (formal)** |
| `PSYCHOLOGY_RPP` | 100 | 100 | 0.610 | **counting — domain 2 (first empirical)** |
| `CANCER_BIOLOGY_RPCB` | 76 | **50** | 1.220 — more cases out than in | **recorded, not counted** |
| `MACHINE_LEARNING_MLRC` | 36 | **0** | n/a | **recorded, not counted** |
| *third domain, §3 below* | — | — | — | **counting — domain 3 (second empirical)** |

RPCB and MLRC are **not dropped and not hidden**. Their per-case screens, their failure reasons
(all 26 `FAIL_NO_EFFECT_LEVEL_WITNESS` cases are RPCB's; all 36 MLRC cases fail `a_` and `g_`) and any
arm results are reported. They cannot enter the §9.1 "2 of 3" count because a domain that cannot reach
the registered bar cannot carry a domain-level primary test, and counting it would let an arithmetic
shortfall read as a scientific loss.

**A re-cut of RPCB to the effect level was considered and rejected.** It is the obvious cheap move and it
does not work: the 26 failures are cases that **lack** an effect-level witness, so going finer
re-partitions the 50 that already pass rather than rescuing any of the 26; and exact paired tests across
effects nested within 23 original papers break the independence those tests assume. Splitting a unit of
analysis to raise n is pseudo-replication, not sample.

---

## 3. Third domain — criteria first, then the choice

**The order matters more than the answer.** The criteria below were written and frozen **before any
eligibility screening was run against any candidate**, and no candidate was scored before selection. A
domain chosen after seeing how its cases score would destroy the only property this exercise has.

### 3.1 Selection criteria (stated before any candidate was screened)

| | criterion | source |
|---|---|---|
| **C1** | an **empirical** science, materially different from `PSYCHOLOGY_RPP` in objects, measurement semantics and strongest parent methodology, and not formal/mathematical | FM80 §2.3 |
| **C2** | a **frozen, case-level, publicly documented replication/transfer witness produced by an independent party** — not by this programme | FM80 §3 item f, §6 |
| **C3** | the **evidence layer is separable from the verdict at case level**: a per-case artifact exists that states the question and the protected decision **without** stating the outcome | FM80 §3 items a and g |
| **C4** | the **strongest known native parent method(s) are nameable per case** | FM80 §3 item b |
| **C5** | **≥ 80 candidate cases before screening** — headroom over the 61 bar, since screening can only reduce | §8 as amended in §1 |
| **C6** | **lawfully and publicly obtainable without authentication**, machine-readable, snapshot-hashable | FM80 §11 |

**C3 is the discriminating criterion and it is selected on deliberately.** It is what removed MLRC from
the pool: *"no outcome-free evidence layer (report text carries the verdict)"*. A corpus that fails C3
cannot be screened into eligibility by any amount of work, because the leak is in the artifact.

### 3.2 Candidate ledger

Every candidate considered, with the criterion that decided it. Corpus-level properties only; no case was
scored.

| candidate | domain | decision | deciding criterion |
|---|---|---|---|
| **Open Source Cross-Sectional Asset Pricing** (Chen & Zimmermann), published cross-sectional return predictors independently re-implemented from each original paper | empirical asset pricing / financial economics | **SELECTED** | passes C1–C6; see §3.3 |
| Organic Syntheses independently checked preparations | synthetic chemistry | rejected | **C2** — the journal publishes essentially only preparations that checked successfully, so the witness has no adverse class and cannot expose a wrong transfer. Large and public, and still unusable. |
| FORRT Replication Database | predominantly psychology | rejected | **C1** — same domain as `PSYCHOLOGY_RPP`; it would not be a *second* empirical science |
| Social Sciences Replication Project (21) | social science | rejected | **C5** |
| Experimental Economics Replication Project (18) | experimental economics | rejected | **C5** |
| Many Labs 2 (28 findings) | psychology | rejected | **C5**, and **C1** |
| Δ-project DFT reproducibility (71 elemental crystals) | computational materials physics | rejected | **C5** (thin, and screening only reduces), and the outcome is a continuous agreement gauge rather than a transfer/block/reopen decision |
| GWAS Catalog association replication | statistical genetics | rejected | **C2** — a per-case "did it replicate" verdict would have to be **curated by this programme**, making us our own witness |
| re-cut of `CANCER_BIOLOGY_RPCB` to effect level | — | rejected | see §2 — re-partitions the passing 50, and breaks paired-test independence |

### 3.3 The selection, and why

**`EMPIRICAL_ASSET_PRICING_OSAP`** — the Open Source Cross-Sectional Asset Pricing corpus.

| criterion | how it is met |
|---|---|
| C1 | objects are **published cross-sectional return predictors**; measurement semantics are portfolio return spreads and t-statistics on market panel data; the strongest native parent is empirical asset pricing / econometrics. None of the three is shared with `PSYCHOLOGY_RPP` (behavioural effects, NHST on experimental samples) or with the formal domain. |
| C2 | the corpus's own team **independently re-implemented each published predictor from the original paper's description** and graded the reproduction per signal. The witness is theirs, produced years before and independently of this programme. |
| C3 | **the field carrying the reproduction grade is disjoint from the fields describing the original claim** (authors, year, journal, signal definition, sample window, predicted sign, the original paper's own test). A per-case record can therefore be built that states the question and the protected decision with the verdict removed — the exact property MLRC lacks. |
| C4 | per case: the original paper's own stated method, plus the standard portfolio-sort protocol of the field. |
| C5 | **331 rows** in the snapshot header, against a bar of 61 and a stated minimum of 80. |
| C6 | fetched over plain HTTPS from the project's public repository with no authentication (`HTTP 200`, 181,712 bytes, verified 2026-09-07 from billy-old). The snapshot is sha256-frozen at intake per FM80 §11. |

**What is not yet claimed about it.** 331 rows is a row count, not an eligible-case count. Whether ≥ 61
of them survive the registered §3 screen, and whether the witness is non-degenerate (§4.3 below), are
**screening questions answered after this document is frozen** — and either may return a negative. This
section commits to the corpus and the reasons; it does not promise the corpus will work.

---

## 4. The range-finding probe — run before assembling anything

### 4.1 Why this exists

**FG80 R3, on the same channel and the same host one day earlier, put all five arms at 80/80 with an
exact p of 1.0.** Its terminal was `FG80_AT_CEILING_UNDER_A_CATEGORICAL_CONTRACT__NO_DYNAMIC_RANGE_FOR_THE_P_F_TRIGGER`:
with the simplest control already solving every task, the suite could not rank any arm at all. That
saturation was verified real against a 12.5 % chance baseline on a balanced task set, so it is a property
of the instrument, not an artifact.

FM80's primary endpoint is also a **categorical disposition** and §9.1 also asks for a **difference in
percentage points**. At ceiling or at floor that difference is unreachable by arithmetic — regardless of
donor keys, regardless of how many domains are assembled, regardless of how much compute is spent. Any
plan that assembles a corpus and dispatches ~900 arm calls before checking for dynamic range is a plan to
discover saturation at the most expensive possible moment.

So the cheap check comes first.

### 4.2 Design

- **Reserved range-finding stratum:** 30 `FORMAL_MATHEMATICS_1000PLUS` cases and 30 `PSYCHOLOGY_RPP`
  cases, drawn by a deterministic seeded shuffle of `case_id` from
  `research/experiments/sd80/SD80_CASE_MATRIX_CASES_V1.json`.
- **These 60 cases are excluded from the §9 analysis set, permanently and in advance.** They are spent on
  measuring the instrument, not on the contrast. The formal domain has 243 cases against a bar of 61, and
  RPP has 100 against 61, so the reserve is affordable in both.
- **Arms: A0 and A1 only** — the strongest native parent and the strongest retrieval baseline. **No A2,
  no A3, no A4.** The treatment arm is never run on this stratum, so no §9 contrast is observed and none
  can be.
- Reading a baseline on cases excluded from the analysis is not outcome access on the registered contrast.
  §8 already selects the comparison baseline "by a pre-outcome rule based only on baseline identity, not
  A3 outcomes", so baseline identity is explicitly not outcome information under this design.

### 4.3 Registered routing table — thresholds fixed here, before any model call

Evaluated **per counting domain** on the reserved stratum, in order; the first row whose predicate holds
is the disposition for that domain. `acc0` = A0 accuracy, `acc1` = A1 accuracy, `best` = max(acc0, acc1),
`maj` = the accuracy of always answering that domain's majority witness class.

| # | predicate | disposition | counts toward §9? |
|---|---|---|---|
| 1 | `best ≥ 0.90` | `AT_CEILING__SECTION_9_1_UNREACHABLE_BY_ARITHMETIC` | no |
| 2 | `best ≤ 0.10` | `AT_FLOOR__NO_DYNAMIC_RANGE_FOR_THE_SECTION_9_CONTRAST` | no |
| 3 | `best ≤ maj` | `BASELINE_DOES_NOT_BEAT_THE_MAJORITY_CLASS__INSTRUMENT_UNINFORMATIVE` | no |
| 4 | `0.80 ≤ best < 0.90` | `NARROW_HEADROOM__A3_MUST_REACH_NEAR_PERFECT_TO_CLEAR_10_PP` | yes, flagged |
| 5 | otherwise | `DYNAMIC_RANGE_PRESENT__PROCEED` | yes |

**Row 1's threshold is derived, not chosen.** §9.1 requires A3 ≥ best + 0.10 and no accuracy exceeds
1.00, so a baseline at or above **0.90** makes the clause unreachable *by arithmetic* in that domain —
the same shape of finding as RPCB's eligibility ceiling, one level up. 0.90 is where the clause dies, not
a round number picked for convenience.

**Row 3 is the control against a different failure.** A domain's witness classes are not balanced —
RP:P's replication outcomes are roughly a third positive — so an arm can post a respectable accuracy by
answering the majority class every time. An arm that does not beat `maj` has demonstrated nothing about
the decision, whatever its raw score, and the row is registered so that a comfortable-looking number
cannot be read as a working instrument.

**Row 4 warns rather than excludes.** At `best = 0.85` the clause needs A3 ≥ 0.95; that is demanding but
reachable, so the domain still counts and the constraint is reported with the result rather than used to
disqualify it.

**Witness non-degeneracy screen**, also registered here, evaluated per counting domain before its arms
are read: the minority witness class must hold **≥ 20 %** of the domain's screened cases. A domain whose
witness is effectively constant fails FM80 §3 item f — the witness cannot expose a wrong transfer — and is
recorded `WITNESS_DEGENERATE__CANNOT_EXPOSE_A_WRONG_TRANSFER`, not counted, and not read as a negative.

**Programme-level routing:** §2 requires three domains and §9.1 requires the effect in ≥ 2 of 3. If fewer
than three counting domains reach `DYNAMIC_RANGE_PRESENT__PROCEED`, the terminal is
`FM80_S9_INSTRUMENT_WITHOUT_DYNAMIC_RANGE__NO_VERDICT_REACHABLE` — **an instrument terminal**. It is
recorded at that strength and **never** as evidence that structural donor discovery or typed transfer adds
nothing. A saturated or uninformative instrument is silent, not exculpatory. This sentence is frozen here
so that it cannot be softened after the numbers are seen.

---

## 5. Stage A — donor-key construction

Unchanged from `FM80_MODEL_PROXY_ADJUDICATION_DESIGN_V1.md` (frozen 2026-09-05, before any model call),
which this amendment adopts by reference and extends to the third domain on identical terms:

- per case, a fresh-session model receives the **tagger-visible record only** — never a hidden key — plus
  the frozen discovery criterion, and returns a candidate donor result from a different primary field with
  its citation and structural mapping, hashed as that case's private donor key;
- `K = 20` top results of the frozen retrieval baseline decide §3d and §4.2 exactly; §4.1 by the frozen
  taxonomy; §4.3 and §3g by string containment over the prompt-visible files;
- **a case whose proxy proposes no donor is `INELIGIBLE`, never negative evidence.**

The missing donor key is the stage R11b attributed the block to, by elimination against three rival
stages, and it is the input Stage A exists to supply. Stage A is what makes §3c–e and §4.1–4.3 exact
rather than `CANNOT_CHECK`; it does not make them pass.

**Every Stage A and Stage B output carries `HUMAN_GATE_BYPASSED__MODEL_PROXY`.** No proxy verdict is
recorded as independent human adjudication, none is marked as externally obtained, and FM80 §9 survival is
not reachable through the proxy route.

---

## 6. Channel and model pin

| | |
|---|---|
| host | **billy-old** over tailscale. Never the Mac. LUNARC is not used and is not required. |
| client | codex CLI **0.129.0-alpha.15**, the programme's permanent pin. Not upgraded. |
| model | **`gpt-5.5`**, reasoning effort high — the standing factory model |
| probed | 2026-09-07, `CHANNEL_OK` returned |

**Recorded because it is a change from the sibling run:** FG80 R3 executed on 2026-09-06 against
`gpt-5.6-terra`. On 2026-09-07 the same pinned client is refused for that model by the service —
`"The 'gpt-5.6-terra' model requires a newer version of Codex"` (HTTP 400) — while `gpt-5.5` answers
normally. The pin is not moved to chase a model. FM80 §5 requires only that **all arms use the same model
family/version**, which `gpt-5.5` satisfies; the served model id is asserted at run time and recorded in
the outcome receipt rather than assumed from what was requested.

---

## 7. Seed commitment

The run seed is generated and held **off-repository** at `billy-old:~/fm80-s9-v2/SEED.txt`. Committed here
by hash before any draw or dispatch, and revealed in the outcome receipt afterwards so that any reader can
recompute the reserve draw and check it was not chosen to suit a result:

```text
SEED_FILE_SHA256 = 3f8e805c29bffd7e873af2836c2000c9be0916842b7ed9fd27c0e6a8278e2b41
SEED_FILE_BYTES  = 33
REVEAL           = post-run, in the outcome receipt
```

---

## 8. Order of operations (binding)

1. **this document merged to `main`** — its sha256 registered;
2. reserved stratum drawn from the committed seed; witness non-degeneracy screen;
3. **range-finding probe** (A0, A1 on the 60 reserved cases); routing table evaluated;
4. **branch.** No dynamic range in ≥ 2 counting domains → instrument terminal, recorded, stop. Range
   present → third-domain intake and §3 screening, Stage A, Stage B, Stage C, §9 gate;
5. outcome receipt with the seed revealed and the served model id asserted.

Steps 2 onward do not begin before step 1 lands.

---

## 9. What this amendment does not do

- it does **not** relax any §9 threshold: the 10 pp bar, the exact paired test, Holm, the
  non-compensatory fidelity clause §9.3 and the §9.4/§9.7 clauses all stand as frozen;
- it does **not** amend FM80's protocol text; it is a sibling execution design, as
  `FM80_PRE_OUTCOME_DESIGN_CORRECTION_V1.md` is;
- it does **not** grant P-A or P-B a standalone route, change either paper's disposition, or touch
  `submission_authorized`;
- it does **not** substitute a machine surrogate for §4.4's remoteness adjudication — that clause is
  proxied and labelled, never replaced;
- it does **not** promise a verdict. A registered instrument terminal, or a stated failure to assemble the
  third domain honestly, are both admissible outcomes of executing it.

skills-applied: none (frozen execution design, no manuscript content)

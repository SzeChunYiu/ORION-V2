# FM/FG R2 — Erratum V1: the amendments, and the successor plan

**Applies to:** `FMFG_R2_SUITE_TERMINAL_RESULTS_RECEIPT.md` §1 and §4,
`FMFG_R2_REGISTERED_SCALE_DISPATCH_RECEIPT.md` "Execution binding", and
`rollup-r2/PERSTUDY_R2.csv` — all on main `35a884a`.
**Lane:** `FM_FG_GENERATED_EXACT_CAMPAIGN` (owner issue #48). **Date:** 2026-09-04.

**Sibling, not superseded:** `FMFG_R2_COVERAGE_RECONCILIATION_RECEIPT_V1.md` (PR #269)
established the coverage defect and repaired the harness. It is explicitly non-amending and
stops before two acts it assigns to this lane: **amending the affected receipts**, and
**designing the successor's arm set**. This erratum performs both. Nothing in #269's receipt
is corrected here. The finding was first reported by
`research/experiments/pf-trigger/PF_R2_TRIGGER_EVALUATION_RECEIPT_V1.md` §7, whose files are
untouched.

**Effect on the primary terminal: none.** `REGISTERED_SCALE_NULL` stands. What changes is
the denominator it is stated over, the number of conditions it ranges across, and two claims
made *about* the arms rather than about the numbers. §5 is the ledger.

## 1. Two counting framings, and they agree

Two receipts in this directory publish different headline numbers for one defect. Both are
correct; they differ only in the identity rule, and they close against each other exactly.

| | dispatches |
|---|---|
| registered by the plan (Σ tasks × per-study arms) | **13,168** |
| ran | **8,560** |
| **net shortfall** | **4,608 (35.0%)** |

**Exact-arm-id identity** (#269's receipt, and the auditor's COVERAGE clause). Two arms are
the same only if their ids are the same string. The executed set is then *not a subset* of
the registered set, because `DEFAULT_ARMS` carried two ids the plan registers for no study:

- registered and ran — 3,056
- registered, never ran — **10,112**
- ran, registered for no study — **5,504**

**Procedure identity** (this erratum, and the auditor's CONSTRUCTIBILITY clause). Two arms
are the same if `ARM_PROCEDURE_CLASS` gives them the same procedure. The renamed ids
(`F2_STATIC_NO_FORMAL_DISCOVERY` for `F2_STATIC_NO_TRANSFER_DISCOVERY`, and so on) then
count as the registered arm executed under a different label, and the shortfall is 4,608.

**`10,112 − 5,504 = 4,608`.** One defect, two rules, one arithmetic. Neither framing is the
"real" number: exact-id is the right rule for asking *was the registration honoured*,
procedure identity for asking *what evidence is actually missing*. The corrected receipt
publishes 13,168 and 8,560 and points at both.

## 2. What the 4,608 is made of

Allocating class-wise per study (this reconciles with 13,168 − 8,560 exactly):

| dispatches | registered arms | what running them would add |
|---:|---|---|
| **456** | `STRUCTURE_MAPPING_PARENT` (FM10, FM20), `ANTI_UNIFICATION_OR_MDL_PARENT_WHEN_APPLICABLE` (FM20), `FCA_PARENT_WHEN_APPLICABLE` (FM30) — all `PARENT_GENERIC` | the label only |
| **2,536** | `SEMANTIC_RETRIEVAL`, `SEMANTIC_RETRIEVAL_OF_EXISTING_FORMALISM`, `LOCAL_PATCH_OR_EXTRA_VARIABLE` — all `ARM_PROCEDURE_CLASS = None` | nothing: no procedure was ever designed |
| **1,616** | `FIXED_LESSON_INJECTION`, `FIXED_FORMALISM_LESSON_INJECTION` | a genuinely distinct condition |
| **4,608** | | |

So of the registered arms that never ran, **exactly one — the fixed-lesson injection
control — is both distinct and implementable today.** The rest are names without procedures
of their own. The finding is not "35% of a campaign was skipped for want of compute"; it is
that **the registered arm taxonomy was never implemented**, and compute would not have fixed
it. Every explicitly named published-method parent in the plan — Gentner-style structure
mapping, Plotkin-style anti-unification/MDL, formal concept analysis — is a label on
`PARENT_GENERIC`.

## 3. Four distinct conditions were executed, not five

`F0_PARENT_FEDERATION` and `STRONGEST_DOMAIN_FORMAL_PARENT` are both `PARENT_GENERIC`. The
prompts are not byte-identical — `prompt()` interpolates `ARM: {arm_id}` — but the
`ARM PROCEDURE` line is, and the arm's own name echoed back at the model is the entire
difference. Consequences for terminal receipt §4:

- The pure-executor stock is **1,232 tasks × 4 distinct conditions**, not × 5.
- "F0 is nominally first" is a statement about a label. No federation procedure was
  executed.
- **"the metabolic loop (F2 family) matches the parent federation (F0) and the target-only
  floor" is withdrawn.** The comparison against the strongest single parent stands; the
  comparison against a *federation* does not.
- The widest gap in the whole pure-executor table — F0 1,018 against STRONGEST 1,006, 12 of
  1,232 — is between two runs of one procedure. One draw on marginal totals rather than
  paired discordance, so it is not a numerical noise floor; it does remove the reading that
  the ordering reflects anything about the arms.

This bears on the programme's "strongest faithful parent" invariant and on the standing
finding that parent labels have been overstated relative to what was implemented.

## 4. Why amend rather than re-run or re-register

Three routes were open. The decision and its reasons, recorded:

**Run the missing arms — refused, on implementation existence rather than cost.** Six of the
eight registered-and-never-run ids have no procedure of their own: three are
`PARENT_GENERIC` duplicates and three are `ARM_PROCEDURE_CLASS = None`. Dispatching them
would publish three named published-method parent baselines that are name-label
perturbations of one prompt, and three control arms the executor now refuses by design.
That converts an omission into a fabricated baseline — worse than the current silence. Only
`FIXED_*_LESSON_INJECTION` could be run honestly, and it is registered in the successor for
a prospective run rather than back-filled into a lane whose outcomes are known.

**Amend the plan to the executed 5-arm set — refused, and it is post-outcome.** R2's results
have been public since 2026-08-30 (`f9898cc`). An amendment authored on 2026-09-04
retrofitting the registered arm set to whatever happened to execute is a post-outcome
narrowing of a pre-registered design, and would be so whatever justification accompanied it.
Stated plainly rather than dressed up. §6's successor is a different act: prospective for
its own run, nothing executed under it, arm set chosen by procedure identity — a criterion
independent of any R2 score.

**Erratum against the receipts, plus a registered successor — taken.**

### Why amend the receipts rather than only append to them

PR #269 left the R2 receipts byte-untouched by design, and a peer lane has flagged amending
them as a freeze-implicating act. The reasons for amending, stated so a reader can disagree
with them:

1. **The operator asked for it.** The instruction opening this lane was explicit: *"Correct
   the R2 suite receipt to publish both denominators (registered and executed) rather than
   only the executed one."* The amendment is the requested work, not a unilateral edit.
2. **Nothing binds the bytes.** The receipt is referenced by path from four files
   (`fg/FG70_…_DESIGN_V1.json`, the two `pf-trigger` receipts, #269's own receipt) and by
   digest from none. Verified by hashing the blob at `origin/main` and searching all 1,873
   text files in the tree for that digest — zero hits, against a positive control digest
   that returns nine. No test and no workflow asserts its bytes. There is no freeze to
   break; "frozen" here is a lane convention about *results*, and no result is edited.
3. **A sibling document does not fix a wrong sentence.** The defect is a heading that reads
   `Execution completeness (8,560/8,560 valid)`. A reader who reaches that heading and stops
   is misled, and will be misled equally after any number of separate receipts are filed
   beside it. The correction has to be where the claim is.
4. **What is amended is bounded and disclosed.** Every edit is a denominator, a scope, a
   pointer, or a withdrawn claim about the arms. **No measured value is touched** — not a
   correct/total cell, a rate, a contrast, a p-value or a verdict — and each amendment
   carries a dated marker naming this erratum. The `PERSTUDY_R2.csv` change is two `leg`
   labels that disagreed with the `tasks` column beside them.

The frozen *result* is untouched and is not re-run: re-running R2 against a corrected arm
set is a new design, not a repair, and it is registered as V2 rather than performed here.

## 5. Ledger — what moves and what does not

| item | affects the terminal? | affects any rate? |
|---|---|---|
| §1 registered denominator is 13,168; both identity rules close at 4,608 | no | no |
| §2 six of eight never-run ids have no procedure of their own | no | no |
| §3 the stock is 4 conditions, not 5 | **scope only** | no |
| §3 "matches the parent federation (F0)" | **claim withdrawn** | no |
| "generators + arm set frozen by the plan" (dispatch receipt) | no | no |
| `leg` mislabels for `fg10`, `fg50` | no | no |
| plan `owner_issue: 50` against lane owner #48 | no | no |

`REGISTERED_SCALE_NULL` stands, restated with its scope explicit: **at the registered
per-study task counts, on the single-executor stock of 1,232 tasks, no one of the four
distinct conditions actually executed separates from any other.** Formal discovery
(`F2_FULL − F2_STATIC`, p = 0.85) names two arms that are genuinely distinct conditions and
is untouched by everything above.

**Which way the missing evidence could move it.** Per #269: the under-executed side is the
*comparator* side — the treatment arms ran at full registered task counts — so
under-executing parents understates parent strength, and the correction points toward
`PARENT_SUFFICIENT`, a legitimate terminal, never toward mechanism superiority. This erratum
adopts that bound and adds nothing to it.

**P-F is not reopened.** FG80's never-run registered arms are all *additional controls*;
its treatment ran at the full 80 tasks, and its comparator — labelled `TARGET_ONLY_DIRECT`
where the plan registers `CURRENT_FORMALISM_ONLY`, both class `DIRECT` — is behaviourally
faithful. 23/80 against 42/80, −23.75 pp, exact paired McNemar p = 4.3e-03, unchanged.
`research/experiments/pf-trigger/` and `scripts/verify_pf_r2_trigger.py` are untouched by
this erratum.

What is **not** established, and was previously implied by "execution completeness": that
the lane answered its question against the full registered control battery. It did not. The
fixed-lesson control is unrun and the registered published-method parents were never
implemented. Those are obligations of the V2 lane, not properties of this result.

`grants_F2_superiority` remains **false**, as do all other authority grants.

## 6. Successor plan — the deferred design act, discharged

`research/experiments/FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V2.json`. Prospective, no
results, 14 studies at V1's registered task counts, **8,560 registered dispatches over five
genuinely distinct conditions** — where R2's 8,560 covered four.

The selection rule is **exactly one arm id per distinct procedure class in
`ARM_PROCEDURE_CLASS`**, campaign-wide. That drops more than the collapsed parents: V1's
FM/FG naming split gave two ids to one procedure four times over
(`TARGET_ONLY_DIRECT` / `CURRENT_FORMALISM_ONLY`, and the three `..._TRANSFER_DISCOVERY` /
`..._FORMALISM_GENESIS` pairs). **That is the same defect this erratum raises against F0 and
STRONGEST, and V2 does not exempt itself from it.** The retained procedure text already
spans both families — `F2_STATIC` reads "do not perform open-ended transfer discovery,
conceptual revision, or formalism genesis" — so nothing family-specific is lost.

Twelve ids are carried in `deferred_arms_pending_procedure_design`, each with what it is
waiting on, separating the four that are genuine design obligations (the published-method
parents, the federation) from the three with no procedure at all and the duplicates that are
merely surplus labels. Deferred, not deleted.

`scripts/run_formal_discovery_campaign.py` prepares V2 with no modification — verified on
FM50 and FG80.

## 7. Repairs landed here

- **Receipts.** Terminal receipt §1 publishes registered (13,168) alongside executed
  (8,560), per leg and in total, and §4 carries the four-conditions correction. Dispatch
  receipt no longer claims the arm set was frozen by the plan.
- **`rollup-r2/PERSTUDY_R2.csv`.** The `leg` column labelled `fg10` as `n96` on 160 tasks
  and `fg50` as `n96` on 120 tasks. Corrected to `n160` and `n120`. The `tasks` column,
  every correct/total cell and §1's leg groupings were already right; **no accuracy,
  contrast or verdict moves.** Receipt §3 carried the same two labels and is corrected with
  it.
- **`scripts/audit_formal_campaign_coverage.py` gains `--pre-registration`.** #269's auditor
  requires executed evidence and returns 8 (COULD NOT CHECK) on a plan with no run — so a
  *prospective* plan, which is exactly what needs auditing before it is frozen, could not be
  checked at all. CONSTRUCTIBILITY is a property of the plan and the arm table alone.
  The flag checks that clause by itself, reports COVERAGE as `NOT_APPLICABLE` (never a
  pass), and refuses with 8 if evidence is supplied alongside it. One auditor, one more
  mode — not a second script. V2 returns **0**; V1 returns **4**.
- **`scripts/run_formal_discovery_campaign.py`.** `prepare`, `dispatch` and `status` read
  `CAMPAIGN_EVALUATION_SUMMARY.json` unconditionally at the end of `main()` and exited on a
  `FileNotFoundError` traceback after doing their work correctly. Scoped to the commands
  that produce one.

## 8. Bookkeeping

`FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V1.json` carries `"owner_issue": 50`, while both
R2 receipts and the P-F receipt attribute the lane to #48. #48 is the lane
("[CONCEPTUAL DEVELOPMENT][TRANSFER DISCOVERY] Open-world science with mathematics-first
structural discovery and formal mechanics"); #50 is the programme umbrella
("[V2 CLOSURE][RECURSIVE SCIENTIFIC DEVELOPMENT] …"). The receipts are right; V1's field
points at the umbrella. V2 records `"owner_issue": 48`. V1 is not edited — it is a frozen
prospective registration, and correcting a field in it after the fact would break what it
pins.

skills-applied: none (results erratum, no manuscript content)

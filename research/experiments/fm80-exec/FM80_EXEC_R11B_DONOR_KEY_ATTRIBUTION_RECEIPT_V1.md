# FM80 §9-EXEC — R11b: what the 455/455 screen was actually measuring, and the pool's eligibility ceiling

**Date:** 2026-09-06 · **Lane:** ORION-V2 revival backlog #308 R11 · **Predecessor:** R11a (`61035601`, #340)
**Authority:** none. This receipt corrects an instrument and reports arithmetic. It changes no P-A/P-B verdict,
grants no survival, and reaches no §9 terminal. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

## 1. The suspicion

R11a ran `FM80-§9-EXEC` on the only assembled naturalistic pool (SD80, 455 cases) and reported **§3c fails
455/455 — no donor key exists**, leaving zero eligible cases and the gate at `NO_VERDICT__BLOCKED`. A screen
that rejects every case it is shown is worth checking before it is believed: 455/455 with no variance is the
signature of a constant, not a measurement.

## 2. It was a constant

`case_table_from_sd80` built its case table by **hardcoding `has_donor_key: False`** for every record, while
setting every other donor-dependent flag to `None` (CANNOT_CHECK). The pool's own records say something
different. All 455 SD80 cases carry, verbatim:

```
c_remote_donor_known_or_prospective_criterion : NOT_APPLICABLE_PC_R7_NO_DONOR_ARM__FM80_PENDING_DONOR_KEY   455/455
d_donor_outside_local_retrieval_neighbourhood : NOT_APPLICABLE_PC_R7_NO_DONOR_ARM__FM80_PENDING_DONOR_KEY   455/455
e_transfer_consequence_nontrivial             : NOT_APPLICABLE_PC_R7_NO_DONOR_ARM__FM80_PENDING_DONOR_KEY   455/455
s4_operational_remoteness                     : NOT_APPLICABLE_PC_R7_NO_DONOR_ARM__FM80_PENDING_K_CORPUS_FREEZE  455/455
```

The source of truth says **PENDING**; the adapter said **checked-and-false**. The 455/455 rejection carried no
information about the pool: no SD80 case has ever been evaluated for a donor, because the case matrix has no
donor field at all (11 top-level keys per case, none donor- or transfer-related; `case_id` present 455/455 as
the control that the enumeration works).

## 3. One-stage attribution

The four candidate stages, and what eliminates three of them:

| candidate stage | eliminated by | number |
|---|---|---|
| the **eligibility predicate** is vacuous | it discriminates wherever its inputs exist | `a_` 419 PASS / 36 FAIL; `f_` 393 / 36 / 26; `g_` 419 / 36 |
| the **remoteness criterion** is too strict | it was never evaluated on any case | §3d, §4.2: `n_checkable = 0` of 455 |
| the **corpus / search baseline** rejects the donors | it was never constructed | `s4_operational_remoteness` = `PENDING_K_CORPUS_FREEZE`, 455/455 |
| the **donor adjudication key** is missing | the records say PENDING; the adapter supplied the False | 455/455, one hardcoded literal |

**Attributed stage: the missing donor-key input at case assembly** — Stage A of the frozen model-proxy design
(`FM80_MODEL_PROXY_ADJUDICATION_DESIGN_V1.md`), never run. Not the criterion, not the baseline, not the
predicate. This is a *could-not-check*, and it now reports as one.

## 4. The correction, and the control that it did not blind the gate

`has_donor_key` is read from the record through `tri_from_sd80_item` (`PASS*` → True, `FAIL*` → False,
`NOT_APPLICABLE`/`PENDING` → None). The literal is gone. The selftest grew from 5 boolean controls to 11; the
four new precondition controls exist because a fix that stops the gate seeing real failures would be worse
than the mislabel it removes:

- an **absent** donor-key field ⇒ `CANNOT_CHECK`, `n_checkable = 0` (the correction);
- **no-alarm:** a genuine `has_donor_key: False` ⇒ still `SOME_FAIL`, `n_checkable = 1`;
- a genuine `True` ⇒ `PASS_ALL`; a mixed table ⇒ `SOME_FAIL` with its denominator 1/2;
- the token mapping itself, on all four real SD80 token shapes.

**11/11 pass.** The correction moves two clauses, in opposite directions — which is the evidence that it is a
read of the data and not a blanket softening:

| clause | before | after |
|---|---|---|
| §3c | `SOME_FAIL`, 455 checkable, 0 pass | `CANNOT_CHECK`, 0 checkable — a rejection that never happened |
| §3g | `CANNOT_CHECK`, 0 checkable | `SOME_FAIL`, **455 checkable, 419 pass** — a check that was available all along |

§3g's recovered evidence is **partial by scope** and is labelled so in the output: SD80's
`g_visible_materials_free_of_hidden_key` covers the disposition/verdict-leak component of §3g only; the
donor-key and gold-relation components stay unevaluable because no donor key exists.

## 5. What the pool can support even if Stage A runs perfectly

`sd80-eligibility-ceiling` computes, per domain, the upper bound on eligible cases from the clauses SD80
evaluates on its own records, against the registered bar of **61** per domain. Stage A can only *reduce* this:
its design marks a case `INELIGIBLE` whenever the proxy proposes no donor.

| domain | n | checkable ceiling | Stage A joint yield needed for 61 | status |
|---|---|---|---|---|
| FORMAL_MATHEMATICS_1000PLUS | 243 | 243 | **0.251** | ceiling above bar |
| PSYCHOLOGY_RPP | 100 | 100 | **0.610** | ceiling above bar |
| CANCER_BIOLOGY_RPCB | 76 | **50** | 1.220 — unreachable | **below bar by arithmetic** |
| MACHINE_LEARNING_MLRC | 36 | **0** | n/a | below bar by arithmetic |

The losses are structural and localised, not diffuse: all 36 MLRC cases fail `a_` (`FAIL_NO_OUTCOME_FREE_CONTRACT`)
and `g_` (`FAIL_REPORT_TEXT_CARRIES_VERDICT__NO_STRIPPED_EVIDENCE_LAYER`) — the pool has no stripped evidence
layer for MLRC, so it is out of scope rather than failing. **All 26 `FAIL_NO_EFFECT_LEVEL_WITNESS` cases fall
in RPCB**, capping it at 50 against a bar of 61.

**Consequence, stated before any dispatch.** RPCB is one of the three registered domains, and it is
`UNDERPOWERED_AT_REGISTERED_BAR` by arithmetic under every possible Stage A outcome. §9.1 asks for the effect in
**≥ 2 of 3** domains, so with RPCB permanently untestable the clause collapses to a **strict conjunction on
formal AND RPP**, with no slack — and only if Stage A returns a joint donor-proposal-and-remoteness yield of
≥ 25.1% on formal and ≥ 61.0% on RPP. The 61% requirement on RPP is a conjunction of three conditions (a donor
proposed, outside the frozen top-K = 20, with nontrivial transfer consequence).

## 6. Terminal

Stage A is **not dispatched**. The reason is registered here rather than discovered afterwards: one of the
three registered domains cannot reach the registered bar on this pool no matter what Stage A returns, so a
dispatch could at best produce a two-domain conjunction whose failure would be uninterpretable against a
design written for three. Manufacturing eligibility to reach a verdict is the one thing the gate must not do.
The missing input is named exactly, and what would fix it is a *witness class* — RPCB cases carrying an
effect-level witness — not more model compute. That is the same structural finding PC-R7 reached
(`INSUFFICIENT_ELIGIBLE_NATURALISTIC_CASES`), arrived at independently here.

```text
FM80_S9_EXACT_SUBSET = NOT_ASSEMBLED__DONOR_KEY_ABSENT__CANNOT_CHECK
  (§3c/3d/3e/4.1-4.3 n_checkable = 0 of 455; §3g partial, 419/455 on the disposition component only)
FM80_S9_SAMPLE_FEASIBILITY = INSUFFICIENT_ELIGIBLE_NATURALISTIC_CASES__RPCB_CEILING_50_LT_BAR_61
  (MLRC 0; formal 243 and RPP 100 above bar, requiring Stage A yields of 0.251 / 0.610)
FM80_S9_VERDICT = NO_VERDICT__BLOCKED  (unchanged)
HUMAN_GATE_BYPASSED__MODEL_PROXY = registered, unrun — no assembled case exists to adjudicate
P_A / P_B disposition = UNCHANGED (NO_STANDALONE_RELEASE__REFERENCE_RESOURCE_ONLY)
CORRECTED = the 455/455 screen; it was a hardcoded constant, not a measurement
```

## 7. What a reader should not take from this

The corrected reading is *weaker* than the one it replaces, not stronger: "the pool never carried a donor key"
says less than "every case was checked and rejected". Nothing here is evidence about naturalistic transfer in
either direction, and nothing here reopens a standalone route for P-A or P-B.

skills-applied: none (evidence lane, no manuscript content)

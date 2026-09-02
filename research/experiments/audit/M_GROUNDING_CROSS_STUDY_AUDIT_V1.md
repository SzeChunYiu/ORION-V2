# `M`-grounding cross-study audit V1 — ME-X1, ME-X2, ME-X4, ME-X5

**Question.** ME-X5's open erratum (PR #186) discloses that its `M` arm is not "compiled to the ORION
reference objects" as its design, receipts, PR bodies and issue comment state. ME-X1, ME-X2 and ME-X4 are
**merged**, and their terminals were used to contract the flagship's field claim (ORION-paper PR #43, merged
`446f5224`, manuscript `FLAGSHIP_MACHINE_EPISTEMICS_PERSPECTIVE_V23_CONTRACTED.md`). Are the siblings
likewise bespoke reimplementations?

**Answer. No. The defect is one study, not four.** ME-X1, ME-X2 and ME-X4 execute registered ORION semantics
on `M`'s decision path. ME-X5 does not, and its defect is confirmed independently of PR #186. The
contraction's evidential basis **holds as stated**.

**Audit base.** `origin/main` `ae1a3f7`; re-verified against `39276fa` — `git diff --name-only ae1a3f7 origin/main`
over `me-x1/ me-x2/ me-x4/ me-x5/ tests/unit` shows no change to any audited file. `mex5_arms.py` sha256
`d255edf95ac94ed1dcdf18e885e2e6569c32e73bc4079a3508889881bd84c4ba`, matching the hash PR #186 pins.
Companion machine-readable record: `M_GROUNDING_CROSS_STUDY_AUDIT_V1.json`.

**Nothing was changed, re-run or re-analysed.** No frozen artifact edited, no protected study re-run, no
receipt modified. Every finding is static reading of code plus reads of already-frozen result JSONs.

---

## 0. Overall finding

> The evidential basis of the flagship contraction **holds as stated**.
>
> The three merged studies whose terminals the contraction consumes — ME-X1, ME-X2, ME-X4 — each run `M`
> through genuinely-executed ORION reference objects on the decision path. The sentence "the strongest
> faithful parent federation reproduces the decisions the controller makes" means what it says for all three.
> ME-X5, the one defective study, **is not cited anywhere in V23** and no artifact outside `me-x5/` is built
> on its terminal, so the defect does not reach the flagship at all.
>
> Three wording defects are found and graded below — one FALSE (ME-X5 docstring), two OVERSTATED (ME-X1's
> "to a `Terminal`", ME-X4's "no new M") — none of which disturbs any terminal or moves any number.

---

## 1. Per-study verdict table

| study | merged | `M`'s reference objects | verdict | reaches flagship? |
|---|---|---|---|---|
| **ME-X1** transition coupling, n=1,000 | #161 `59b1f5b` | `ProblemContract`, `Obligation`, `ObligationStatus`, `ReticulateProvenance`, `selective_reopen`, and — via the parent classes — `assess_evidence_dependence`, `RelationType`, `ComparabilityCertificate`, `assess_atlas_gluing`: **all decisive**. `Terminal`: **discarded** | **GROUNDED** (one decorative import) | yes |
| **ME-X2** locus / minimum escalation, n=1,200 | #164 `776d3a1` | `route_frontier_action`, `minimum_level`, `assess_jump`: **decisive, and proven to have executed in the protected run**. `assess_discrepancy_locus`: **called and checked, not decisive** | **GROUNDED** | yes |
| **ME-X4** selective reopening, n=1,200 | #149 `4929a44` | `ReticulateProvenance`, `assess_evidence_dependence`, `RelationType`, `ProblemContract.scope`, `selective_reopen`: **all decisive** | **GROUNDED** | yes |
| **ME-X5** cross-domain residual, n=1,440 | #183 `024d97f` | four named objects **prose only**; `selective_reopen` **called, result discarded through a vacuously-true assertion** | **NOT GROUNDED** — PR #186 confirmed and extended | **no — absent from V23** |

Category key, as requested: **(a)** imported and called on the decision path; **(b)** imported and called but
result discarded; **(b′)** called and consulted only in a falsifiable assertion — checked but not decisive;
**(c)** named only in prose.

---

## 2. Question 1 — what `M` actually calls

### 2.1 ME-X5 — NOT GROUNDED (category c and b)

`mex5_arms.py` docstring lines 12-13 names five reference objects. Only one is imported anywhere in the file,
and only as a **function-local** import at line 316 inside `_me_resolved`.

| claimed object | category | evidence |
|---|---|---|
| `ReticulateProvenance` | **(c) prose only** | zero imports, zero call sites in `mex5_arms.py`. `M` calls `provenance_invalid_units` (lines 279, 317) |
| `assess_evidence_dependence` | **(c) prose only** | zero imports. `M` calls `R.independent_groups` (line 299) |
| `RelationType` | **(c) prose only** | zero imports. `M` uses the local `RELATION_RANK` dict imported from `mex5_model` (line 31) |
| `ProblemContract.scope` | **(c) prose only** | zero imports. `M` calls `R.coverage_ok` (lines 301, 333) |
| `selective_reopen` | **(b) called, discarded** | local import line 316; called line 324; reduced to `preserved` line 331; discarded line 334 |

The discard, verbatim at `mex5_arms.py:334`:

```python
assert preserved == bool(live or narrow_ok) or True  # reopening receipt is the propagation of record
```

The trailing `or True` makes the assertion unfalsifiable. `preserved` is read nowhere else in the file. The
decision is `chosen = live or narrow_ok` (line 335), computed entirely by the native rule layer.

**New, not in PR #186 — a false claim about the oracle boundary.** `mex5_arms.py:18` states:

> "No arm imports the oracle module (asserted by a unit test)."

Both halves are false. `mex5_arms.py:56` is `from mex5_oracle import rules_for`, and `rules_for` is used on
`M`'s decision path at lines 268 and 313. No unit test asserts the stated property — see §5.2. **This is a
documentation defect only; it is not leakage, and §5 establishes that with the study's own frozen numbers.**

### 2.2 ME-X1 — GROUNDED (category a throughout, one decorative import)

Module-level imports at `mex1_arms.py:33-36`. `M` is `engine_transition_control` (line 671).

| object | category | decision-path evidence |
|---|---|---|
| `ProblemContract` | **(a)** | built line 676 with real `scope`; `contract.requires_authority()` charged line 677 |
| `Obligation`, `ObligationStatus` | **(a)** | lines 686-690 build one typed obligation per condition; line 690 maps them to the atoms the precedence walk consumes at line 691 |
| `ReticulateProvenance` | **(a)** | constructed line 150 in `_provenance_graph`, consumed by `prov_typed` (line 153), wired into `M` at line 718 |
| `selective_reopen` | **(a)** | called twice at lines 450-451; `preserved_commitment_ids` / `reopened_commitment_ids` (line 456) **are** the disposition map returned to `M` at line 678 |
| `assess_evidence_dependence` | **(a), indirect** | `dep_typed` (line 212) → `IndependenceWitness.status` → `mex1_parents.py:332-333`, whose `conservative_independent_support_count` is the returned status |
| `RelationType` | **(a), indirect** | `trans_typed` (line 231) → `TransportLicense.license` → `mex1_parents.py:349-352` |
| `ComparabilityCertificate` | **(a), indirect** | `MetrologyComparability` → `mex1_parents.py:366-370` |
| `assess_atlas_gluing` | **(a), indirect** | `AtlasGluing.status` → `mex1_parents.py:409` |
| `Terminal` | **(b) discarded** | imported line 33; sole use is the dead assignment at line 691 — see §3.2 |

The indirection matters and is exactly what the design claims: ME-X1's design says `M` is "**fed by** the
parent-owned reference modules", and the parent classes are thin wrappers that really do call the ORION
functions. This is categorically different from ME-X5, whose `M` calls a *reimplementation* that never
touches the reference object at all.

### 2.3 ME-X2 — GROUNDED (a different, topic-appropriate reference set)

ME-X2 legitimately uses `assess_discrepancy_locus`, `route_frontier_action`, `assess_jump` and
`minimum_level` — the objects for locus diagnosis and escalation — not the ME-X5 five. Module-level imports
at `mex2_arms.py:19-21`.

| object | category | decision-path evidence |
|---|---|---|
| `route_frontier_action` | **(a)** | line 315; line 316 `if route.status is not FrontierRouteStatus.JUMP_ASSESSMENT_REQUIRED: return None` aborts escalation |
| `minimum_level` | **(a)** | line 324; `chosen.proposal_id` selects the intervention actually taken (line 331) |
| `assess_jump` | **(a)** | line 325; line 329 returns `None` unless the verdict is `CANDIDATE_FOR_PROTECTED_EVALUATION` |
| `assess_discrepancy_locus` | **(b′) called and checked, not decisive** | `receipt` built line 429 on every `act()`; used **only** in the assertions at lines 431 and 455 |
| `CapabilityContext`, `EpistemicAction`, `FrontierEpisode`, `FrontierObstruction`, `JumpTrigger`, `JumpProposal`, `DiscrepancyLocus`, `LocusHypothesis`, `LocusDiagnosisEvidence` | **(a)** | lines 260-264, 285-289, 312-314, 322-323 — the argument objects the four functions above consume |

**(b′) is a real category and is reported as such.** Neither assertion is vacuous: line 431 is a bare
identity check, and line 455's disjunction still constrains the `gate=True` case to
`{CANNOT_IDENTIFY, MULTIPLE_LIVE_LOCUS_HYPOTHESES}`, so an `ACTIONABLE` status there would fail. The gate is
computed natively and the reference receipt continuously validates it, rather than the receipt computing the
gate. That is weaker than (a) and much stronger than (c).

### 2.4 ME-X4 — GROUNDED (category a throughout)

Module-level imports at `mex4_arms.py:26-30`. Closest structural sibling to ME-X5, and clean.

| object | category | decision-path evidence |
|---|---|---|
| `assess_evidence_dependence` | **(a)** | lines 139-140; `conservative_independent_support_count` sets the dependence status atom at line 144 |
| `RelationType` | **(a)** | lines 163-166 set the transport status atom at line 167 |
| `ProblemContract` | **(a)** | line 232; `contract.scope` decides the scope atom at line 235 |
| `ReticulateProvenance` | **(a)** | line 89 in `_provenance_graph`, feeds `prov_typed`, wired at line 607 |
| `selective_reopen` | **(a)** | lines 349-350; receipt IDs at line 355 produce the disposition map returned to `M`'s engine at line 684 |

---

## 3. Question 2 — vacuous assertions and discarded results

**Scope actually searched, stated so the absence claim is checkable.** Two independent passes over all 29
`.py` files of `me-x1/`, `me-x2/`, `me-x4/`, `me-x5/` (arms, oracles, parents, generators, models, analysis
runners, native modules, vocab), run with `/usr/bin/grep` and `python3 -c` writing to files, since the rtk
proxy corrupts both output and exit codes:

1. **AST pass** — locals assigned and never subsequently loaded in the same function scope
   (`ast.walk`, `Name` in `Store` vs `Load`). This catches named discards such as `_terminal`, which a
   literal `_ = ` regex cannot. 70 raw hits.
2. **Widened vacuity regex** — `or True`, `or 1`, `or (True)`, `assert True`, `assert 1`, `if False`,
   `pass #`, bare `...`, plus `except`-swallow shapes.

A control run (`grep -c "assert "` per file) confirms all four directories were reached, so the negative
results below come from a search whose scope is justified, not from a search that merely returned nothing.

### 3.1 Genuine vacuity — 2 instances, in 2 files

| # | location | construct | effect |
|---|---|---|---|
| V1 | `me-x5/mex5_arms.py:334` | `assert preserved == bool(live or narrow_ok) or True` | **Unconditionally vacuous.** Discards the `selective_reopen` receipt — the object that would otherwise have *decided* family survival. This is the severe instance |
| V2 | `me-x2/mex2_arms.py:455` | `assert receipt.status is CANNOT_IDENTIFY or not self.gate or receipt.status is MULTIPLE_LIVE...` | **Conditionally vacuous.** For the `M_MINUS_DIAGNOSTIC_EVALUATOR_GATE` ablation, `not self.gate` short-circuits it to true. For `M` itself (`gate=True`) it does full work. Named here because completeness on vacuity is claimed |

### 3.2 Discarded results with reference-object content — 2 instances

| # | location | construct | effect |
|---|---|---|---|
| D1 | `me-x5/mex5_arms.py:202` | `surviving = tms_surviving_families(...)` (line 194) then `_ = surviving` | `_federation_exact` (B5) discards the TMS surviving-family set. Note the *same* call **is** load-bearing in `_b4_tms_assurance` at lines 414-415, so this is a genuine dead path, not a stylistic idiom |
| D2 | `me-x1/mex1_arms.py:691` | `_terminal = {...}.get(d.action, Terminal.JUSTIFIED_PARTIAL_RESULT)` | `Terminal` is the only ORION object in ME-X1 that never reaches a decision. `engine_transition_control` returns `d`, not `_terminal`. See the wording grade in §4 |

**The severity difference between D1/V1 and D2 is the finding, and it is large.** ME-X5 discards the object
that would have *decided*, and substitutes a reimplementation. ME-X1 discards an object that was never
load-bearing to begin with — `Terminal` is a relabelling of an already-computed decision, and the scored
quantity is `d.action`. No ME-X1 number depends on it.

### 3.3 Benign — checked and cleared

- **68 of 70 AST hits** are throwaway tuple-unpacking or loop counters (`_a`, `_p`, `_c`, `_k`, `for _ in
  range(...)`), or the unused half of a pair whose *other* half is asserted — e.g.
  `mex4_parents.py:625` `ch, sus = ac.change_impact(...)` where `sus` carries the selftest assertion, and
  `mex2_parents.py:254` `v3, a3 = ...` where `a3` does. No evidential effect.
- **Five `except Exception as exc` sites** (`mex1_run.py:419`, `mex2_run.py:428`, `mex4_run.py:384`,
  `mex5_run.py:605`) are all inside the **protected-run authorization guard**. Each binds the exception,
  prints `REFUSED: authorization file unreadable: {exc}` and returns exit 3. Fail-closed, not a swallow.
- `mex5_vocab.py:225` `except Exception: return "CANNOT_PARSE"` is the documented scrambled-adapter null
  arm, and its rate is reported in the analysis (`scrambled_adapter_rate` 0.091 / 0.886 / 0.909). Disclosed,
  not hidden.
- `mex5_run.py:234, 287, 289` `or 1` are divide-by-zero guards.
- **Minor, non-affecting, queued:** `mex1_generator.py:466-467` computes `P = Tc` and a `deps` list in
  `plant_E`'s else-branch and uses neither. Generator hygiene; it touches no arm's grounding and no scored
  quantity. Worth a look in case a constraint was intended and dropped.

---

## 4. Question 3 — do the claims match? Every quoted claim graded

### ME-X1 — SUPPORTED, with one OVERSTATED phrase

| # | source | quoted claim | grade |
|---|---|---|---|
| 1 | design `..._V1.md:205` and `.json:100` | "`orion_v2.contracts.ProblemContract` (identity, scope, authority requirements) + one typed `Obligation` per condition (SATISFIED / DEFEATED / CENSORED / AUTHORITY_BLOCKED) **fed by the parent-owned reference modules** (`orion_v2.provenance`, `orion_v2.evidence.assess_evidence_dependence`, `RelationType`, `orion_v2.comparability.ComparabilityCertificate`, `orion_v2.epistemic_atlas.assess_atlas_gluing`) + `orion_v2.reopening.selective_reopen` envelope + the registered precedence walk" | **SUPPORTED.** Every named object executes on the decision path; "fed by" correctly describes the parent-class indirection |
| 2 | same line, final clause | "...the registered precedence walk **to a `Terminal`**" | **OVERSTATED.** The walk produces `d`; the `Terminal` mapping at line 691 is assigned to `_terminal` and never read. The walk does not terminate in a `Terminal`. No number is affected |
| 3 | outcome receipt line 89 | "The information-matched federation — the same parent-owned modules M's obligations are fed by ... — is decision-identical to `M` on every one of the 1 000 instances" | **SUPPORTED** |
| 4 | parent-fidelity receipt lines 42-46 | per-parent known-answer rows for `assess_evidence_dependence`, `RelationType`, `ComparabilityCertificate`, `assess_atlas_gluing` | **SUPPORTED** |
| 5 | PR #161 body | no M-grounding claim beyond the above | **n/a** |

### ME-X2 — SUPPORTED, with one OVERSTATED-BUT-NOT-FALSE sentence

| # | source | quoted claim | grade |
|---|---|---|---|
| 6 | `mex2_arms.py:8-11` docstring; design §4 table line 213 | "M = ORION reference semantics: `assess_discrepancy_locus` (locus receipt with the diagnostic-evaluator gate), `route_frontier_action` (witnessed obstruction, lower-level disposition) and `JumpTrigger`/`JumpProposal`/`assess_jump`/`minimum_level` (minimum-level policy)" | **SUPPORTED** for the escalation half; **OVERSTATED** for the locus half — see #7 |
| 7 | design §4.1 lines 223-230 | "A unique supported hypothesis yields `ACTIONABLE_LOCUS_HYPOTHESIS`; several yield `MULTIPLE_LIVE_LOCUS_HYPOTHESES`; an inadequate diagnostic evaluator yields `CANNOT_IDENTIFY`, **which M reports** rather than converting into a forced causal attribution" | **OVERSTATED, NOT FALSE.** Reads as though the receipt status drives M's report. In code M's report is driven natively (`unique`, `disc`, `self.gate`) and the receipt is asserted to agree, every step. Precise correction: *the gate is computed natively and continuously validated against the reference receipt, rather than computed by it* |
| 8 | design §4.1 lines 231-238 | "A level ≥ 2 intervention is routed through `route_frontier_action` on a `FrontierObstruction` ... and then through `JumpTrigger` / `JumpProposal` / `assess_jump`, with `minimum_level` selecting among admissible proposals" | **SUPPORTED**, and proven executed — §5.3 |
| 9 | design §4.1 lines 236-238, and §4.1 closing para | "One addition, registered here as part of M: a **fail-closed reachability rule**" and "Two orderings the ORION reference semantics do **not** fix, and which this design registers as M's rendering rather than as discoveries" | **SUPPORTED, and exemplary.** ME-X2 explicitly registers its own composition code as new. This is the honest pattern the other designs should follow |
| 10 | outcome receipt line 97; PR #164 body line 23 | "M's two orderings, registered in design §4.1 **before** the run because the ORION reference semantics fix neither" | **SUPPORTED** |
| 11 | `mex2_arms.py:2` | "No arm imports the oracle" | **SUPPORTED with a caveat that the study itself already states.** `mex2_arms.py:24` imports `ArmView` only, and `test_me_x2_exact_study.py:193` **positively pins** exactly that: `assert "from mex2_oracle import ArmView" in src` |

### ME-X4 — SUPPORTED, with one OVERSTATED phrase

| # | source | quoted claim | grade |
|---|---|---|---|
| 12 | design line 229 | "**the existing reference semantics, no new M**" | **Split verdict.** "the existing reference semantics" — **SUPPORTED**, all five objects decisive (§2.4). "no new M" — **OVERSTATED**: `engine_selective_reopen` runs `selective_reopen` *twice* (optimistic/pessimistic, lines 349-350) and maps the two receipts into a three-valued disposition at lines 355-357. That bracket is M's rendering, and it is composition code authored for the study. Mitigating: the design's very next sentence discloses the twice-run envelope, so this is imprecise summary rather than concealment |
| 13 | design lines 230-235 | "`ReticulateProvenance.descendants` for revocations, `assess_evidence_dependence` for independence witnesses, `RelationType` rank for transport, evaluator coverage, `ProblemContract.scope` for scope, then `orion_v2.reopening.selective_reopen` run twice (censored = valid / censored = invalid)" | **SUPPORTED** — object-by-object, this is exactly what the code does |
| 14 | outcome receipt line 84 | "The information-matched federation ... is decision-identical to `selective_reopen` on every instance" | **SUPPORTED** |
| 15 | outcome receipt line 97 | "M depends on hidden oracle relations — no: arms never import the oracle; M uses only registered information and the existing ORION reference modules" | **SUPPORTED.** `mex4_arms.py` has zero `mex4_oracle` imports (verified) |

Note the contrast that makes #12 worth recording: ME-X1's design enumerates "+ the registered precedence
walk" as a component, and ME-X2 §4.1 explicitly registers its addition. ME-X4's "no new M" is the one
sentence in the three merged studies that claims more than the code does.

### ME-X5 — one claim FALSE, the rest already conceded by PR #186

| # | source | quoted claim | grade |
|---|---|---|---|
| 16 | design line 256; `mex5_arms.py:11-14` | "`M` — the ME arm, **compiled to the ORION reference objects** (`ReticulateProvenance` for revocation descendants, `assess_evidence_dependence` for independence witnesses, `RelationType` ranks for typed transport, `ProblemContract.scope` for scope, `selective_reopen` for family survival)" | **FALSE.** Independently reconfirmed, not taken from PR #186 |
| 17 | `mex5_arms.py:18` | "**No arm imports the oracle module (asserted by a unit test).**" | **FALSE — new, not in PR #186.** `mex5_arms.py:56` imports `mex5_oracle.rules_for`, used on M's decision path at 268 and 313; and no unit test asserts the stated property (§5.2). Documentation defect only — no leakage (§5.1) |
| 18 | `mex5_arms.py:311-313` | "Family survival is decided by the parent-owned `selective_reopen`" | **FALSE.** Family survival is decided by `chosen = live or narrow_ok` at line 335; the receipt is discarded at 334 |
| 19 | `ME_X5_PARENT_FIDELITY_RECEIPT_V1.md:41` | "`TYPED_TRANSPORT` — ranks follow the parent-owned RelationType order — PASS" | **SUPPORTED but easily misread.** `mex5_parents.py:316-318` genuinely checks the ORION enum's order. The check is about the *parents*; it says nothing about `M`, which uses the local `RELATION_RANK` dict |

---

## 5. Question 4 — does it move numbers?

### 5.1 ME-X5: no. And the equivalence is established by evidence, not asserted — with one method worth reusing

PR #186 argues no number moves because the native rule layer and the reference objects compute the same
thing on this input class, per the 20 parent-fidelity known-answer tests. That argument is **sound but
indirect**, since those tests exercise the reference objects through the *parents*, not through `M`'s inputs.

The stronger and more direct settlement comes from the study's own frozen numbers, and it also disposes of
the leakage worry raised by the `rules_for` import. **Method — the ladder is a proof, not an argument: test
a suspected shared channel against arms that share it but differ elsewhere.**

`rules_for` (`mex5_oracle.py:42-47`) returns one of the three *native mode modules* — a three-entry dispatch
dict that merely happens to be defined in the oracle file. It carries no instance state, no target, no
label, no censored-fact resolution. Access is **symmetric**: `mex5_parents.py:31` imports it too and calls it
11 times, so B5 and every single parent read exactly what `M` reads.

`decision_exact_rate` from `ME_X5_PROTECTED_ANALYSIS_V1.json`, FORMAL / MEASUREMENT / SYNTHESIS:

| arm | F | M | S |
|---|---|---|---|
| `B0_DIRECT_NATIVE_PIPELINE` | 0.2500 | 0.2188 | 0.1979 |
| `B1_CALIBRATED_ABSTENTION` | 0.2500 | 0.2188 | 0.1979 |
| `B2_PROVENANCE_VERIFIER_RUNTIME` | 0.3438 | 0.3125 | 0.2958 |
| `B3_DIAGNOSIS_METAREASONING` | 0.3646 | 0.3500 | 0.3688 |
| `B4_TMS_ASSURANCE_FEDERATION` | 0.4167 | 0.3854 | 0.3646 |
| `B5_R1_VERDICT_ONLY` | 0.8646 | 0.8500 | 0.8688 |
| `B5_R2_PROVENANCE` | 0.8750 | 0.8604 | 0.8833 |
| `B5_R3_PLUS_DEPENDENCE_ANCESTRY` | 0.8896 | 0.8833 | 0.8979 |
| `B5_R4_PLUS_TYPED_TRANSPORT_AND_EVALUATOR` | 0.9479 | 0.9333 | 0.9521 |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | **1.0000** | **1.0000** | **1.0000** |
| `M_ME_CROSS_TRANSITION_CONTROL` | **1.0000** | **1.0000** | **1.0000** |
| M ablations (11) | 0.7958 – 1.0000 | | |
| `C_ALWAYS_COMMIT` / `C_NEVER_COMMIT` | 0.1667 | 0.1667 | 0.1667 |
| `C_RANDOM_DECISION` | 0.0187 | 0.0167 | 0.0146 |
| M vs within-mode shuffled oracle | 0.0813 | 0.1125 | 0.0917 |

**If `rules_for` carried the answer, every arm holding it would be at ceiling and the ablations could not
move.** The single parents hold it and sit at 0.20–0.42; the ladder climbs monotonically with each rung of
*witness exchange*; M's ablations hold it and degrade to 0.80–0.92. The tie at 1.0 is produced by rung-5
witness exchange, exactly as the design predicts. **No leakage. ME-X5's headline number stands and its
terminal does not need withdrawing.**

### 5.2 The ME-X5 test-scoping hole — queued as a task, not a note

`tests/unit/test_me_x5_cross_domain_study.py:141-144` is a **source-string ban list**, not an import check:

```python
def test_no_arm_imports_the_oracle_decision_procedure() -> None:
    src = (MEX5 / "mex5_arms.py").read_text()
    assert "decide_resolved" not in src
    assert "oracle_version" not in src and "oracle_trajectory" not in src
```

It bans 3 of the oracle's 12 public names and never tests for `mex5_oracle` itself, so line 56 sails through.
The test's *name* is accurate and the code complies with the narrower property; the **docstring at line 18 is
the false statement**.

**Latent hole:** `family_failures` (`mex5_oracle.py:52`) is the oracle's per-family verdict function and is
**absent from the ban list**. An arm importing it would leak real answers with the test still green. Nothing
imports it today — verified — so this is latent, not exploited.

**A ban list enumerating what is forbidden fails open on anything it forgot; an allow-list pinning what is
permitted fails closed.** ME-X2 already has the strictly better pattern and should be copied: ban the answer
names **and** positively pin the one permitted import
(`assert "from mex2_oracle import ArmView" in src`). ME-X1 bans the module name across three files. ME-X5's
is the weakest of the three and should be rewritten as an allow-list.

### 5.3 ME-X2: no — and the reference objects left fingerprints in the frozen bytes

**Method worth reusing: prove a property from what the run left behind, not from the source.**
`ME_X2_PROTECTED_RESULTS_V1.json` records `jump_receipts` per arm (written at `mex2_run.py:86`). Counted
across the protected file:

| `route.status` | `assess_jump` verdict | count |
|---|---|---|
| `JUMP_ASSESSMENT_REQUIRED` | `CANDIDATE_FOR_PROTECTED_EVALUATION` | 2,040 |
| `BLOCKED_LOWER_LEVEL_UNRESOLVED` | — (escalation aborted) | 17 |
| | **total** | **2,057** |

`route_frontier_action` and `assess_jump` demonstrably **executed** during the protected run, and
`route_frontier_action` **blocked 17 escalations** — the reference object changing the protected run's
behaviour, recorded in the frozen bytes.

**Bounding the assertion claim precisely, because the two evidence types do different work.** The receipts
prove the *objects* ran. They do **not** prove the two `assert` statements ran: a passing assertion leaves no
trace, so a stripped run and a passing run are indistinguishable in the artifact. Support for
assertion-enablement is therefore **evidence-based inference from the invocation path, not proof**:

- `PYTHONOPTIMIZE` — 0 hits repo-wide; `python -O` / `-OO` / `sys.flags.optimize` — 0 hits.
- No sbatch, shell wrapper or CI workflow invokes any `mex*_run.py` — 0 hits.
- The authorization record fixes the invocation as the bare script: `PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json`
  scope = "exactly one protected run of `research/experiments/me-x2/mex2_run.py protected`". Shebang
  `#!/usr/bin/env python3`, no flags — assertions on by default.

**Residual, explicitly marked:** if the operator's shell had exported `PYTHONOPTIMIZE`, the two assertions
would have been stripped and `assess_discrepancy_locus`'s correspondence would degrade from (b′) to (c).
Nothing in the repository records the environment, so this cannot be closed from the artifact.

**Deliberately not closed by a run.** An execution on laptop billy would show the assertion *can* fire, which
is not the same as showing it *did* in the protected run, so it would not convert the inference into proof.
Per the standing rule, no CI or test suite was run on this host.

Conditional on assertions being enabled, ME-X2's `M`-vs-reference equivalence for `assess_discrepancy_locus`
is **established by evidence** — checked on every decision step of every protected episode — which is exactly
the standard ME-X5's `or True` fails.

### 5.4 ME-X1 and ME-X4: no

Every reference object is decisive; there is no bespoke substitute layer whose equivalence would need
establishing. ME-X1's one discarded object (`Terminal`) never fed a scored quantity.

---

## 6. Question 5 — does it reach the flagship?

**No. ME-X5 is absent from V23 entirely.**

Verified token-by-token against `origin/main:v2-papers/FLAGSHIP-machine-epistemics/manuscript/public/FLAGSHIP_MACHINE_EPISTEMICS_PERSPECTIVE_V23_CONTRACTED.md`,
with a control (`"federation"` → 18 hits) proving the file was read:

| token | hits |
|---|---|
| `ME-X5` | **0** |
| `1,440` | **0** |
| `four studies` | **0** |
| `1,200 and on 1,000` | 1 |
| `cross-domain` | 1 — line 178, listing cross-domain studies as **not yet run** |

The three studies V23 rests on are ME-X4 (n=1,200), ME-X1 (n=1,000) and ME-X2 (n=1,200), matching the
`n_instances` in each frozen protected analysis. All three are GROUNDED.

### 6.1 The sentences that rest on these terminals — and their status

| line | sentence | status |
|---|---|---|
| 6 | "On 1,200 and on 1,000 protected instances the federation reproduced every decision the coupled controller made; on a third it decided better." | **NOT overstated.** Rests on ME-X4 and ME-X1 (grounded) and ME-X2 (grounded) |
| 28 | "Three exact studies have now returned that answer: twice by the advantage vanishing at full structure, and a third time more sharply, with the federation deciding better than the controller at every rung." | **NOT overstated** |
| 112 | "The two systems compared are a coupled controller ... and the strongest faithful parent federation: the same mature modules ... connected by ordinary engineering glue and given the same information." | **NOT overstated.** The controller side genuinely executes registered ORION semantics in all three |
| 126 | "in the first two the rung-five gap is exactly zero, so at full-structure exchange federation and controller are the same decision function" | **NOT overstated** |
| 186 | "At 1,200 and at 1,000 protected instances they did not, and at a further 1,200 the composition decided better. The programme's own contraction rule applies, and the label is withdrawn..." | **NOT overstated** |
| 194 | "The answer came back the same way three times..." | **NOT overstated** |

The feared weakening — "reproduces the decisions of a reimplementation of the controller" — **does not
apply**. In all three merged studies the controller arm is the registered semantics.

### 6.2 Not caused by the defect: V23 staleness

Independent of the `M`-grounding question, and recorded so it is not misread as flagship exposure:

V23 line 178 says "**Four** registered families have not been run", and line 130 says "**three of seven**
registered families have terminated". 3 + 4 = 7. ME-X5 merged (#183, `024d97f`, 2026-09-02 21:48 UTC) after
V23's PR #43, so **both counts now move together**: four terminated, three unrun. This is ordinary
freshness, not a defect in any claim V23 makes, and it is for the flagship lane (PR #171 is the open
addendum) rather than for this audit.

### 6.3 Nothing else is built on the ME-X5 terminal

Of 41 files outside `me-x5/` mentioning ME-X5, all cite it as a **registered protocol family**, not as a
result. The two that could have consumed the terminal do not:
`papers/pipeline/FLAGSHIP_EXTERNAL_DEMARCATION_REVIEW_PACKET_V3_V21.md:239` lists ME-X5 under "protocols at
synthesis level; **no protected outcomes**", and `research/field/MACHINE_EPISTEMICS_FIELD_SYNTHESIS_V4.md:225`
describes the design only.

---

## 7. Errata and queued work

Following PR #186's pattern exactly — a standalone erratum plus a pointer blockquote, **no frozen artifact
edited**, so every sha256 pin keeps addressing the bytes that produced its result. This audit **writes no
errata**; it specifies them for the owning lanes.

### 7.1 ME-X5 — extend the open erratum in PR #186 (do not open a second)

Add one item to `ME_X5_ERRATUM_V1.md`: the docstring at `mex5_arms.py:18` — "No arm imports the oracle module
(asserted by a unit test)" — is **false in both halves**, with the §5.1 ladder evidence showing this is a
documentation defect and **not** leakage, and the §5.2 note that the unit test bans 3 of 12 oracle names and
does not test for the module.

### 7.2 ME-X1 — one-line erratum

`ME_X1_TRANSITION_COUPLING_EXACT_STUDY_DESIGN_V1.{md:205,json:100}`: the phrase "the registered precedence
walk **to a `Terminal`**" is OVERSTATED — the walk returns a `Decision`; the `Terminal` mapping at
`mex1_arms.py:691` is dead. No number, gate or terminal changes.

### 7.3 ME-X4 — one-line erratum

`ME_X4_SELECTIVE_REOPENING_EXACT_STUDY_DESIGN_V1.md:229`: "no new M" is OVERSTATED — the
optimistic/pessimistic double-run and three-valued mapping (`mex4_arms.py:340-357`) are composition code
authored for the study, as the design's own next sentence describes. "the existing reference semantics"
stands. No number, gate or terminal changes.

### 7.4 ME-X2 — one-line erratum

`ME_X2_LOCUS_DIAGNOSIS_EXACT_STUDY_DESIGN_V1.md` §4.1: the sentence describing locus statuses as what "M
reports" is OVERSTATED-BUT-NOT-FALSE. Correction: *the gate is computed natively and continuously validated
against the reference receipt, rather than computed by it.* No number, gate or terminal changes.

### 7.5 Queued tasks (no frozen artifact touched)

1. **Rewrite ME-X5's oracle-boundary test as an allow-list.** Ban `mex5_oracle` by module name and every
   answer-bearing symbol — `family_failures` above all — and positively pin the permitted imports, per
   ME-X2's pattern. Highest value item here: it closes a hole that is currently latent.
2. **Audit the sibling suites for the same shape.** ME-X1 and ME-X2 use module-name bans and a positive pin
   respectively; confirm neither has an equivalent forgotten symbol.
3. **ME-X5 V2 lane** (already queued in PR #186): make `M` consume the four unused reference objects, remove
   both vacuous constructs, correct the docstring and design §4. A V2 freezes its own design and seed; the
   V1 result is immutable.
4. **ME-X1 generator hygiene:** `mex1_generator.py:466-467` computes `P` and `deps` in `plant_E` and uses
   neither. Confirm no constraint was intended and dropped.
5. **Add a repository-wide vacuity guard** — an AST check for locals assigned and never read, and for
   assertions whose top-level disjunct is a constant — so this class is caught before merge rather than by
   audit. Note it must catch named discards (`_terminal`), which a literal `_ = ` regex misses.
6. **Flagship lane:** refresh V23's family counts once ME-X5 is reflected (§6.2). Not caused by this defect.

---

## 8. Method notes

Three methods carried this audit and are recorded for reuse:

1. **The ladder is a proof, not an argument.** To test whether a suspected shared channel is leaking, compare
   arms that *share* the channel but differ elsewhere. If the channel carried the answer, all of them would
   sit at ceiling and ablations could not move. This settled ME-X5's leakage question from the study's own
   frozen numbers, without reading another line of code (§5.1).
2. **Prove a property from what the run left behind.** The 2,057 `jump_receipts` in ME-X2's protected results
   establish that the reference objects executed *and altered outcomes*, which no amount of source reading
   could show (§5.3). Its limit is equally important: assertions leave no trace, so this method cannot speak
   to them.
3. **Justify the scope of an absence claim.** The initial `^\s*_ = ` regex missed `_terminal` in ME-X1 and
   would have produced a false "exactly one file" claim. An AST pass over assigned-never-read locals found
   it. An absence claim needs a search whose scope was justified, plus a control proving the search reached
   where it says it did (§3).

Per the standing rule, no test suite, CI job or study code was executed on this host.

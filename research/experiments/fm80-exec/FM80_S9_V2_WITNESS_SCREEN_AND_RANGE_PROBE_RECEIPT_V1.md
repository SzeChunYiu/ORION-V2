# FM80 §9 V2 — witness screen and range-finding probe: outcome receipt V1

**Date:** 2026-09-07 · **Design:** `FM80_SECTION_9_EXECUTION_AMENDMENT_V2.md`, sha256
`25940e38c8548bd96dedf750d94e85d1e631a64baf565b87402dc71b245ab84e` — frozen before this ran and
**not edited afterwards**. The design was executed, not adjusted.
**Authority:** none. No P-A/P-B verdict, no survival, no publication readiness.
`submission_authorized` untouched. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

## 1. Terminal

**The registered terminal that fired**, per domain, exactly as frozen:

```text
FORMAL_MATHEMATICS_1000PLUS = WITNESS_DEGENERATE__CANNOT_EXPOSE_A_WRONG_TRANSFER
PSYCHOLOGY_RPP              = NON_DEGENERATE
```

Composing that with FM80 §2.1 gives the programme-level reading:

```text
[derived, not a registered terminal]
FM80_S9_FORMAL_DOMAIN_WITNESS_DEGENERATE__SECTION_2_1_UNFILLABLE_ON_THIS_POOL__NO_VERDICT_REACHABLE
```

**That second line is a description, not a terminal, and the distinction is deliberate.** The
amendment registered two names only: `WITNESS_DEGENERATE__CANNOT_EXPOSE_A_WRONG_TRANSFER` per
domain and `FM80_S9_INSTRUMENT_WITHOUT_DYNAMIC_RANGE__NO_VERDICT_REACHABLE` at programme level. The
string above is neither — it was written after the screen ran, and a label minted after an outcome
must never stand where a registered terminal belongs. It is kept because it states the cause more
precisely than either registered name (a degenerate witness is not the same failure as an
instrument without dynamic range), and it is labelled so that no reader mistakes it for a
pre-registered outcome. The registered programme-level terminal is **not** claimed: it is defined
over three assembled counting domains, and only two were ever assembled.

The registered witness non-degeneracy screen — the amendment's own predicate, run unchanged —
disqualifies the formal domain. FM80 §2.1 requires **at least one** mathematical/formal domain with
a machine- or expert-checkable formal witness, and no empirical corpus can fill that slot. Three
counting domains are therefore unreachable on this pool, upstream of anything to do with the third
domain.

**This is a `NO_VERDICT`, not a null.** No arm ran on the formal domain and none could. Nothing here
is evidence about naturalistic transfer in either direction.

## 2. The formal domain's witness is constant

All 243 `FORMAL_MATHEMATICS_1000PLUS` cases carry the single disposition `FORMALIZABLE_AS_STATED`.
The registered contract offers three; the other two — `HYPOTHESES_MISSING_REOPEN` and
`STATEMENT_FALSE_OR_ILLFORMED_BLOCK` — **do not occur once**.

| domain | n | witness classes | minority share | threshold | screen |
|---|---|---|---|---|---|
| `FORMAL_MATHEMATICS_1000PLUS` | 243 | `FORMALIZABLE_AS_STATED` **243** | 0.000 | ≥ 0.20 | `WITNESS_DEGENERATE__CANNOT_EXPOSE_A_WRONG_TRANSFER` |
| `PSYCHOLOGY_RPP` | 100 | `REPLICATION_FAILS_CRITERION` 61 / `REPLICATION_SATISFIES_CRITERION` 39 | 0.390 | ≥ 0.20 | `NON_DEGENERATE` |

**The absence claim has a justified scope rather than resting on a search that returned nothing.**
A field-name census over all 243 formal hidden keys accounts for every case: `decl` 182 + `decls` 31
+ `url` 30 = 243. There is no residue in which an adverse witness could be hiding.

Both screens were run twice — over the 30-case reserved stratum and over each domain's **full pool**
— so a degenerate reading cannot be an artifact of the draw. Both agree.

### 2a. A correction that made the finding stronger

The first reading counted only `decl`/`decls` and reported the formal domain as 213 checkable and
30 uncheckable — which would have looked like variance. It was a mapper defect: the registered
contract's witness is *"a machine-checked declaration in Mathlib **or a listed external formal
library**"*, and those 30 keys carry a `url` into an external Lean development. They are formalized
too.

Corrected to **243/243**. The correction moves the reading toward *more* constant, not less, which
is the evidence that it is a read of the contract rather than a convenient one. Nine planted
controls pin it, including the no-alarm cases (an `authors`-only key, a `comment`-only key and an
empty key must all stay uncheckable; an RP:P `url` must not be read as a formal witness).

### 2b. One-stage attribution: the case source

| candidate stage | eliminated by |
|---|---|
| the eligibility predicate | it discriminates wherever its inputs exist — `a_` 419/36, `f_` 393/36/26, `g_` 419/36 (R11b) |
| the arms | none ran on this domain |
| the analysis | never reached |
| **the case source** | **attributed** — the formal pool was drawn from mathlib's *1000+ theorems* tracking list, which **by construction lists theorems that have been formalized**. The adverse dispositions cannot occur in a list defined that way. |

This is the same shape of finding as PC-R7's `INSUFFICIENT_ELIGIBLE_NATURALISTIC_CASES` and R11b's
missing donor key, reached independently a third time: the block is in what the pool *is*, not in
how it is screened or scored.

### 2c. The lever, named rather than attempted

What would fix it is a **different witness class**, not more compute:

- an **executable** formal witness — arm outputs checked by Lean — which FM80 §7 already
  contemplates (*"formal cases use machine-checkable proof/test artifacts wherever possible"*). This
  changes the endpoint from *predict the registered disposition* to *produce a checkable artifact*,
  and needs a Lean/mathlib build and proof-checking at scale. It is recorded here as the lever. It
  was **not attempted**, and a weaker substitute was not put in its place;
- or a formal corpus that carries **adverse** formalization outcomes — statements whose formalization
  recorded a missing hypothesis or an ill-formed claim.

A machine-graded comparison of each informal statement against its mathlib signature was considered
and rejected: it would make this programme its own witness, which is what §3's independence
requirement exists to prevent.

## 3. The third domain: selected on criteria, not assembled

`EMPIRICAL_ASSET_PRICING_OSAP` was selected on criteria C1–C6 frozen before any candidate was
screened, and it is **not assembled**. The reason is §2.1 above, which is upstream of it and has
nothing to do with OSAP: with domain 1 unfillable, a third domain cannot produce three counting
domains however well it screens. Assembling it could not move the terminal, and reporting a block
after doing the work would read as though the block were about the corpus.

Its corpus-level properties stand as recorded (331 rows; `HTTP 200`; the reproduction grade in a
field disjoint from the fields describing the original claim). Whether ≥ 61 of its rows survive the
registered §3 screen is **still unanswered**, and this receipt does not answer it.

## 4. A leak the pool's own screen could not see

Every one of the 100 RP:P tagger-visible records carries `Project URL` and `osf_project_id`, which
resolve to the replication project and therefore to the outcome. SD80's `g_` screen passes all 100,
correctly by its own scope — it reads the record **text** for a verdict, and a pointer is not text.
But a pointer to the key is the key, and FM80 §11 requires the key absent from every model-visible
workspace.

Arm-visible records are therefore redacted of URL-bearing fields and inline URLs, identically for
every arm so the change cannot favour one. **Verified with a control that had to fire:** 100/100 raw
records contain a URL; **0/100** rendered prompts do, for both arms. Plus the no-alarm case — a
record with no URL comes back byte-identical with nothing removed.

This is a tightening of §11, in the conservative direction, and it is recorded rather than assumed.

## 5. A defect found in the executor before it could run

`programme_terminal` returned the programme-level instrument terminal **unconditionally** at probe
stage. The probe assembles two domains; the function returned `PROGRAMME_NO_RANGE` whenever fewer
than three counted, so a perfectly healthy probe would have emitted
`FM80_S9_INSTRUMENT_WITHOUT_DYNAMIC_RANGE__NO_VERDICT_REACHABLE` — a structurally guaranteed negative
that no reader could have distinguished from a real one.

The unit test did not catch it because it exercised the function on synthetic three-domain inputs
while the only caller passed two: **a function tested on inputs it is never called with.** That is
the R11b pattern in a new place — a green test beside a defect it was shaped not to see. The
function now refuses on fewer than three assembled domains, the probe reports per-domain routing
only, and two regression tests pin both halves.

## 6. Custody

- Design: `FM80_SECTION_9_EXECUTION_AMENDMENT_V2.{md,json}`; the `.md` sha256 above is unchanged
  since before the screen ran. The `.json` twin carries `superseded_counting_domains_20260907` so a
  machine reader of `domains.counting` gets the corrected answer; the `.md` is **not** rewritten.
- Screen and probe: `research/experiments/fm80-exec/fm80_s9_range_probe.py`, routing and screen
  predicates in `fm80_s9_v2.py`.
- Checker discipline: `fm80_s9_v2.py --self-test` 22/22 (every routing row planted **and** its
  no-alarm case); `tests/unit/test_fm80_s9_v2_routing.py` 18 tests; **6/6 planted mutants caught**
  (ceiling threshold, majority row, minority threshold, programme count, narrow-row counting, range
  validation); 9/9 witness-mapper controls; 8/8 redaction controls with a non-vacuous control.
- Seed: committed by hash before any draw, `3f8e805c29bffd7e873af2836c2000c9be0916842b7ed9fd27c0e6a8278e2b41`.

## 7. What a reader must not take from this

Not that structural donor discovery or typed transfer adds nothing — **no arm ran**. Not that P-A or
P-B is refuted, and not that either is reopened; both dispositions are unchanged. Not that the third
domain failed — it was never screened. What is established is narrower and firmer than any of those:
**the assembled naturalistic pool cannot fill FM80 §2.1, because its formal domain was drawn from a
list of theorems that had already been formalized.**

skills-applied: none (evidence lane, no manuscript content)

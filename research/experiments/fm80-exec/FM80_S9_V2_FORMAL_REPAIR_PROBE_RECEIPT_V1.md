# FM80 §9 V2 — can the degenerate formal witness be repaired from its own source? Receipt V1

**Date:** 2026-09-07 · **Class:** `SOURCE_CENSUS__NO_ARM_RUN__NO_AMENDMENT_REOPENED`
**Authority:** none. No verdict, no survival, no disposition change. `submission_authorized`
untouched. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

## 0. The hypothesis under test, and why it deserved a test

The witness screen found all 243 SD80 formal cases carrying one disposition and attributed it to the
**case source**: the pool was drawn from mathlib's *1000+ theorems* list, which lists theorems that
*have been* formalized. That attribution names a candidate repair, put precisely:

> A pool drawn only from successes is missing its other half, and for this domain the other half is
> enumerated — the same project tracks the entries **not** formalized, so the negative cases the
> witness needs may already be listed.

**The framing is exactly right, and the census confirms its factual premise.** The repair still does
not work, for a reason one level down. Nothing here reopens the frozen amendment; if a pool ever
changes, that is a new frozen version with its own sha256, registered before any screening.

## 1. The premise is confirmed: SD80 drew exactly one side of the list

`fm80_formal_source_census.py` over the pinned snapshot
(`sd80/sources/raw/mathlib4_docs_1000.yaml`, master commit `8571709f…`):

| | |
|---|---|
| entries in the source | **1199** |
| formalized (`decl` / `decls` / `url`) | **243** |
| **not** formalized | **956** |
| SD80 formal cases | 243 |
| SD80 △ formalized set | **∅ — symmetric difference empty, both directions** |

SD80's formal pool **is** the formalized side of the list, exactly. 956 entries were left out. So
the negative half of *formalization status* is enumerated and was available.

*(A parser note, because it is how the census was caught being wrong: entry keys may carry a letter
suffix for a variant theorem under one Wikidata id. A first pass matching only `Q\d+:` dropped 20
entries and disagreed with SD80 by one case. The corrected parser reconciles to zero.)*

## 2. The premise is confirmed and the repair still fails: status is not a witness

**945 of the 956 unformalized entries carry nothing but a `title`.** No status field, no reason, no
adjudication of any kind. The source's own header says it is *work in progress*.

The registered decision contract asks which of three dispositions holds for the statement as
publicly given:

```text
FORMALIZABLE_AS_STATED | HYPOTHESES_MISSING_REOPEN | STATEMENT_FALSE_OR_ILLFORMED_BLOCK
```

**"Nobody has formalized it yet" is none of these.** Absence of a formalization is absence of
evidence, not evidence that a statement resists formalization. Mapping "no `decl`" onto an adverse
disposition would assign `STATEMENT_FALSE_OR_ILLFORMED_BLOCK` to 945 published, true theorems whose
correct disposition is `FORMALIZABLE_AS_STATED` — labelling the true class as the false class. That
would not merely be unjustified; it would **manufacture a large, entirely artifactual signal**, which
is the exact failure this lane exists to prevent.

The source says so itself. Seven unformalized entries carry comments stating that formalization is
**in progress** or that the statement is **already formalized without proof** — Fermat's Last
Theorem, Mihăilescu, Modularity, Stark–Heegner, Gromov, Mazur's torsion, Tunnell. Those are
affirmatively `FORMALIZABLE_AS_STATED` cases lacking only a proof: the opposite of an adverse
witness.

## 3. The one genuine seam, and why it is below the bar by arithmetic

There *is* a real adverse seam: entries whose comment records that the existing formalization is
**weaker than the statement as given** — a baby version, a special case, one variant of several,
axioms assumed, or a public statement too vague to formalize. Examples in the snapshot: Whitney
embedding *"baby version: for compact manifolds"*; Whitney–Graustein *"assumes some basic topology
statements as axioms"*; Fourier *"the wikipedia page is really vague; it's not clear what is
meant"*; metrization *"Urysohn's only"*.

It does not reach the bar, and the bound is hard rather than estimated:

| | |
|---|---|
| entries carrying **any** comment at all, whole file | **29** ← absolute upper bound on the seam |
| of those, plausibly a statement/formalization mismatch (generous reading) | ~13 |
| registered bar per domain (amendment V2, branch 1) | **61** |

**29 < 61.** The seam is below the registered bar *before any adjudication*, so no reading of those
comments — however generous — can produce a domain. And adjudicating free prose ourselves would make
this programme its own witness, which §3's independence requirement forbids and which was already
rejected once in this lane.

## 4. The second seam — CLOSED 2026-09-07, by arithmetic rather than by policy

A `sorry`-carrying or declared-but-unproved mathlib entry would be a genuine adverse witness. This
was left as an open check when the receipt first landed, because the mathlib tree is not vendored
here. It is now closed, without vendoring it and without spending compute.

**The policy route did not work, and that is reported rather than assumed.** The expectation was
that mathlib's CI forbids `sorry` on mainline, so the seam would be empty by construction. Fetched
at the pinned commit `8571709f…` by targeted raw request, no clone:

| file | size | `sorry` matches |
|---|---|---|
| `.github/workflows/build.yml` | 3,786 B | **0** |
| `.github/workflows/build_template.yml` | 53,967 B | **0** |
| `scripts/lint-style.py` | 10,706 B | **0** |
| `CONTRIBUTING.md` | — | HTTP 404 |

**No `sorry` grep exists in mathlib's CI configuration at this commit.** The policy may well hold by
another mechanism, but it could not be confirmed the cheap way, so it is not claimed. A convention
this lane cannot point at is not evidence.

**The arithmetic route does work, and it does not depend on the policy holding.** A targeted code
search over the whole `Mathlib/` tree, with a control that had to fire:

| query | files |
|---|---|
| token `sorry` in `Mathlib/`, Lean sources | **66** |
| of which under `Mathlib/Tactic/` (tactic machinery that *mentions* `sorry`) | **40** |
| remaining, spread across Data 6, Algebra 5, Util 4, Order 2, Lean 2, Geometry 2, and one each in Topology, RingTheory, Probability, GroupTheory, CategoryTheory | **26** |
| control: token `theorem` in the same scope | 4,872 |

**66 is a count of files containing a token, not of sorried theorems**, and it is not laundered into
one here: the great majority are comments, docstrings and the tactic framework's own handling of
`sorry`.

It does not need to be refined, because the bound already settles the question. SD80's formal pool
carries **213** mathlib-declared entries, and the registered bar is **61**. For this seam to produce
a domain, **≥ 61 of those 213 would have to be `sorry`-carrying**. The entire `Mathlib/` tree
contains only 26 candidate files outside the tactic framework. Even under the maximally adversarial
reading — every one of those 26 files holding a sorried flagship theorem from this very list —
**26 < 61**.

The seam is below the registered bar by arithmetic, exactly as the comment seam is (§3), and by a
bound that holds whatever mathlib's policy turns out to be.

**The 30 external-library entries are not covered by any mathlib policy**, and one of them records
assumed axioms (Whitney–Graustein). That case is already inside the 29-comment bound of §3 and is
not counted twice.

```text
SECOND_SEAM = CLOSED__BELOW_BAR_BY_ARITHMETIC (≤ 26 candidate files < bar 61)
POLICY_ROUTE = NOT_CONFIRMED (no sorry check in mathlib CI at the pinned commit; not claimed)
```

## 5. The obvious reframing, rejected on two independent grounds

One could keep the pool and change the question to *"is this theorem formalized in mathlib at commit
X?"* — decidable, and non-degenerate at 243 / 956. It fails twice over:

1. **It is not a scientific transfer decision.** FM80 §6's primary endpoint is the correctness of a
   registered *scientific* disposition. Whether a theorem has been formalized yet is a question
   about effort and priority in one community, and a remote donor improving that prediction would
   be no evidence for P-A's or P-B's claims.
2. **It is maximally contaminated.** mathlib's contents are public and machine-readable. The probe
   in this same lane demonstrated recall of a far less tractable corpus, and the standing
   precondition (`research/framework/PUBLISHED_CORPUS_RECALL_PRECONDITION_V1.md`) would refuse it.

## 6. Terminal

```text
FORMAL_DOMAIN_NOT_REPAIRABLE_FROM_THIS_SOURCE
  negative half of formalization STATUS: enumerated (956 entries; SD80 drew exactly the other side)
  negative half of the registered CONTRACT: not enumerated (945/956 carry only a title)
  adverse seam upper bound: 29 comments, whole file, against a registered bar of 61
  second seam (mathlib `sorry`): CLOSED -- <= 26 candidate files in all of Mathlib/ outside the
    tactic framework, against a bar of 61 over 213 mathlib-declared entries. Closed by arithmetic,
    NOT by policy: no sorry check exists in mathlib CI at the pinned commit, so the expected
    "empty by construction" route is reported as unconfirmed rather than assumed.
```

**The scope of the negative is stated rather than implied**, because "the negative half is not
enumerated in this source" is a different and stronger claim than "our pool lacked it". Both halves
of that were measured: the status half exists and was not drawn; the contract half does not exist to
draw.

`WITNESS_DEGENERATE__CANNOT_EXPOSE_A_WRONG_TRANSFER` stands, FM80 §2.1 remains unfillable on this
pool, and P-A/P-B remain at `NO_VERDICT__BLOCKED` with dispositions unchanged.

## 7. Checker discipline

`fm80_formal_source_census.py --self-test` **7/7**, planting **both** answers: a synthetic source
with 100 adjudicated negatives must be reported as having a seam that clears the bar, and a
title-only source must be reported as having none. Suffixed keys and each of `decl`/`decls`/`url`
have their own planted case. A census able only to return "no" would be worthless here, since "no"
is the answer it returned on the real data.

skills-applied: none (evidence lane, no manuscript content)

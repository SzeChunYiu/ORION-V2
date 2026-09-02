# SD80 / PC-R7 obligation-provenance tagging rule — operational clarification V1

**Class:** intake tagging rule (PC-R7 §1, frozen semantics) with an operational
checklist. The semantics below are quoted verbatim from
`research/experiments/pc-r7/PC_R7_NATURALISTIC_OBLIGATION_CELL_DESIGN_V1.md`
and may not be altered. The checklist only operationalises them; it may be
clarified after the 20-case calibration (GN0) and before any arm run, and the
clarification history is recorded at the end of this file.

## 1. Frozen semantics (verbatim, PC-R7 §1)

> each case's binding constraints are classified by an intake rule applied to
> the case's public record, NOT to any arm output: `EXTERNAL_VERIFIABLE`
> (constraint authored by an external authority and checkable against the
> public record: registered analysis plan, replication protocol,
> reviewer/editor mandate) vs `INTERNAL` (self-generated or unverifiable).

## 2. What you tag

You tag the **provenance of the case's binding constraints** — the constraints
the registered decision (see each record's `registered_decision_contract`)
must satisfy. You do NOT judge the outcome, the quality of the science, or
whether the decision will be easy. You tag from the `public_record` shown in
the case record and nothing else.

## 3. Operational checklist (apply in order)

**Q1 — External authorship or ratification.** Does the public record contain
a constraint document that was authored, accepted, or ratified by a party
other than the team that executes the registered decision? Qualifying
evidence, any one suffices:

- a registration deposited with an external registry (e.g. an OSF
  registration listed under `osf_registrations_public_api` with `count ≥ 1`
  and no withdrawal), or a Registered Report protocol accepted by an external
  editor/peer review (e.g. `Did the experiment protocol get accepted and
  published in eLife` = Yes with a `Link to Registered Report`);
- ratification of the plan by the authority who authored the original claim
  (e.g. `Original Author's Assessment (decoded)` = `ENDORSEMENT`);
- an explicit reviewer/editor mandate in the record;
- for formal cases: an externally authored statement of the theorem that
  fixes its hypotheses (an encyclopedic entry — `enwiki_title` present — or a
  literature statement named in the record).

**Q2 — Public checkability.** Can a third party open the document from an
identifier in the record (URL, OSF id, registration id, article number,
Wikidata/Wikipedia entry) and compare the constraints against it? A record
whose only constraint description is the executing team's own free text with
no external identifier fails Q2.

**Tag:** `EXTERNAL_VERIFIABLE` iff Q1 = yes AND Q2 = yes. Otherwise `INTERNAL`.

Notes:
- An independent coordinator/reviewer merely being *present* (e.g. `OSC
  reviewer (O)` = PRESENT) is a process marker; it counts for Q1 only if the
  record shows that reviewer ratified or mandated the constraints.
- A plan the executing team wrote and never registered/endorsed is
  `INTERNAL` (self-generated) even if it is described in detail.
- A registration query that failed (`status` ≠ OK) makes the registration
  unverifiable from this record: do not assume one exists.
- `INCONCLUSIVE` is not a tag. If you cannot decide, tag `INTERNAL`
  (unverifiable) and say why in the rationale.

## 4. Output contract for taggers

One JSON object per case: `{"case_id": ..., "tag": "EXTERNAL_VERIFIABLE" | "INTERNAL", "q1": "yes"|"no", "q2": "yes"|"no", "evidence_fields": [<record field names used>], "rationale": "<one sentence>"}`.
Taggers work from the record only: no web access, no other repository files,
no hidden-key file, no contact with the other tagger.

## 5. Clarification history

- V1 (2026-09-02, pre-calibration): initial operationalisation. Semantics unchanged.
- V1.1 (2026-09-02, post-calibration, pre-full-round): GN0 calibration on the
  frozen 20-case set: TAGGER_A and TAGGER_B agreed on 20/20 (100%, all
  `EXTERNAL_VERIFIABLE`). No tag disagreements to adjudicate. Both taggers
  independently flagged the same three ambiguities; clarified here without
  changing the semantics of §1:
  1. `osf_registrations_public_api`: the "no withdrawal" condition is
     per-registration — one non-withdrawn registration suffices for Q1.
  2. RP:CB: `Did the experiment protocol get accepted and published in eLife`
     = Yes together with a `Link to Registered Report` governs Q1 even when
     the `submitted` or `originally identified` flags read No (the accepted,
     linked protocol is the external document; the other flags are process
     history).
  3. Formal cases: `enwiki_title` satisfies Q1/Q2 only if the article title
     names the theorem itself or the object the theorem is about (e.g.
     "Composition series" for the Jordan–Hölder theorem qualifies as the
     defining object); if the only encyclopedic pointer is unrelated to the
     theorem, or absent, Q2 fails and the case is `INTERNAL` (unverifiable
     from the record).

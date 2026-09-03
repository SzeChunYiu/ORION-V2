# Flagship External Demarcation Gate — Pre-submission Disposition V1

**State date:** 2026-09-03
**Gate:** issue #38, external dependency `X05_FIELD_DEMARCATION`
**Packet in force:** `FLAGSHIP_EXTERNAL_DEMARCATION_REVIEW_PACKET_V4_V23.md`
**Authority:** none. This record adds a disposition. It adjudicates nothing, contacts no one, selects no panel, and grants no field, novelty, submission or publication status.

---

## 1. What this record does, and what it must not be read as

The gate **stays unpassed**. `GATE_PASSED = FALSE`, `PANEL_SELECTED = NONE`,
`REVIEWER_ANSWERS_ON_FILE = 0` are unchanged and must stay unchanged. Under G1
the gate's evaluation state remains `CANNOT_CHECK__LENS_MISSING`, naming L4.

What is added is a **second, independent fact** about the same gate: whether the
release is waiting for it. It is not, any more. The two are different questions —
*can this gate be evaluated* versus *what did the release decide in light of the
fact that it cannot* — and conflating them is precisely how a `CANNOT_CHECK`
becomes a silent pass.

```text
PRE_SUBMISSION_DISPOSITION = NOT_OBTAINED__DISCLOSED_LIMITATION
```

That token is not a pass, is not a weaker pass, and does not touch
`CANNOT_CHECK__LENS_MISSING`. It records that the gate **will not be satisfied
before submission**, and why.

## 2. Why it will not be satisfied

On 2026-09-03 the sole author wrote, verbatim:

> "i sign off everything, you have been doing a great job, keep going, i dont have any one for external review so you will work around or by pass it."

No reviewer is available to approach. `FLAGSHIP_DEMARCATION_REVIEWER_SELECTION_V2.md`
§3 already records `L4_NAMED_CANDIDATES = 0`, with none verified to V1's standard,
and states that selecting L4 is an open operator task. The operator has now
answered that task: there is nobody. A required lens with zero verified names and
no available candidate cannot produce a written answer, so the gate has no
possible input for L4 and therefore, under G1, no admissible primary terminal.

## 3. What was explicitly not done

Guard G4 forbids any ORION lane, agent, contributor or simulated review from
supplying an answer, and packet §8 governs independence. This lane:

- selected no panel and approached no candidate;
- generated, simulated or role-played **no** reviewer, answer or terminal;
- counted no internal artifact as gate evidence — `FLAGSHIP_SIMULATED_REVIEW_ROUND_V1.md` and `FLAGSHIP_HOSTILE_DEMARCATION_STRESS_TEST_V3.md` remain what G4 says they are;
- recorded no primary or secondary terminal from §4;
- left the re-scoping record and reviewer selection V2 **unedited**. They are already on main and correct; this record is additive.

Filling L4 with a generated answer would be worse here than anywhere else in the
programme. L4 exists specifically to test whether the flagship's **headline
negative** is earned. An internally generated L4 answer would be the authors
checking their own contraction and calling it independent — a gate that can only
agree with the authors, which is the failure
`FLAGSHIP_DEMARCATION_REVIEWER_SELECTION_V2.md` §2 names in as many words.

## 4. The argument for proceeding to submission

Same structure as the manuscript-side disposition, and it should be argued rather
than assumed.

This gate was **self-imposed and pre-submission**. Issue #38's purpose line binds
independent expert review "before any submission claim" — a rehearsal, run early
so the programme would learn a likely external verdict before spending a venue's
time. Its registered question asks whether the interface standard is a genuine
contribution against the nearest existing practice, whether the negative is
earned, and whether the article is honestly named. A peer-reviewed venue's
referees answer exactly those three questions, by construction, and satisfy the
independence conditions of packet §8: selected by the venue rather than by the
author, with no contribution to the framework, manuscript, repositories or study
designs, and no stake in the outcome the author wants.

Submitting therefore does not evade external scrutiny. It routes the question to
a body with authority to answer it, having failed to route it privately first.

## 5. What is genuinely lost — and one loss that is specific to this gate

The manuscript-side disposition names a general cost: an objection now surfaces
on the record with an editor rather than privately. That applies here too. Three
further losses are specific to this gate and are **not** covered by the venue
argument:

- **L4 is the least likely lens to be reproduced by the venue.** S13 targets "a broad AI-science venue" and the deliverable is a Perspective. Referees for a Perspective are selected for topical judgement; benchmark-validity and evaluation-methodology review is standard for a research article and is not guaranteed for a Perspective. So the one lens the gate calls new and required is the one the substitution is weakest at supplying. This is a real gap, not a formality, and it is recorded as unfilled rather than argued away.
- **Two adverse terminals become unreachable in practice.** `NEGATIVE_NOT_EARNED__NULL_TOO_WEAK` and `NEGATIVE_OVERSTATED__NULL_OPTIMAL_BY_CONSTRUCTION` are the terminals G5 keeps reachable, and both need L4 competence. Without L4 the programme retains no mechanism that can tell it its own contraction is unsupported.
- **G5's own binding decays unattended.** G5 is bound to manuscript sha256 `3a8805f6…7d3ed` and must be re-derived on any rebind. With the gate no longer on the critical path, nobody is forced to re-derive it at the next revision. Whoever revises the flagship must re-run G5 against the new bytes; that obligation survives this disposition and is stated here so it is not lost with it.

The correct summary is that the programme is **submitting with its own strongest
check on its negative unperformed**, and saying so, rather than pretending the
check was performed or that it did not matter.

## 6. What is unchanged

- The registered question, the terminals, and guards G1–G7 all stand.
- The packet stays correct and sendable. If an L4 reviewer becomes available before or after submission, the gate runs as written, and a post-submission answer is still worth having.
- The superseded V3 packet, its ME-X-series addendum and selection V1 remain unrewritten.
- No claim in the manuscript changes because a reviewer was unavailable.

## 7. Terminal

```text
GATE_STATE                 = OPEN__RESCOPED
GATE_EVALUATION_STATE      = CANNOT_CHECK__LENS_MISSING (L4)
PANEL_SELECTED             = NONE
REVIEWER_ANSWERS_ON_FILE   = 0
GATE_PASSED                = FALSE
PRE_SUBMISSION_DISPOSITION = NOT_OBTAINED__DISCLOSED_LIMITATION
SIMULATED_OR_SUBSTITUTE_ANSWER_USED = NONE
L4_NAMED_CANDIDATES        = 0 (unchanged; operator reports none available)
BLOCKS_SUBMISSION          = NO (disposed of; not satisfied)
G5_REBIND_OBLIGATION       = LIVE, on any manuscript revision
BASIS                      = author's instruction of 2026-09-03, quoted in section 2
```

# FM80 — Naturalistic Mathematics↔Science Transfer: Blocked-With-Reason Disposition

**Terminal: `BLOCKED_ELIGIBILITY_PRECONDITIONS_UNSATISFIED` — the lane cannot be
dispatched, and this is a registered disposition rather than a negative result.**

**Lane:** FM80 (owner issues #48, #50 §C1).
**Governing protocol:** `research/experiments/FM80_NATURALISTIC_TRANSFER_DECISIVE_PROTOCOL_V1.{md,json}`, frozen 2026-08-30.
**Not executed:** no arm was run, no case was dispatched, no outcome was read.

## 1. Why this is filed on FM80's own grounds, not inherited from SD80

The SD80 case-matrix intake (2026-09-02) terminated
`INSUFFICIENT_ELIGIBLE_NATURALISTIC_CASES`, and it is tempting to read FM80 as
blocked by that. **It is not, and inheriting the terminal would be wrong.**

SD80's terminal is about a *different* population condition: PC-R7 §1 requires
both an `EXTERNAL_VERIFIABLE` and an `INTERNAL` stratum of ≥ 15 cases per domain,
and the `INTERNAL` stratum came back empty because outcome-verifiability and
constraint-externality are supplied by the same artifact in every lawful public
witness source available on that date. That is a genuine structural finding
about PC-R7's internal-versus-external contrast. It says nothing about whether
FM80's own eligibility items are satisfiable.

SD80's own intake receipt says so explicitly: FM80 eligibility is recorded as
**`PENDING` for every case**, because items (c)–(e) are donor-specific and *"no
donor key / K / corpus freeze exists yet"*. FM80 is blocked by its **own**
unmet preconditions, listed below, and those are the ones that must be cited.

## 2. The unmet preconditions, quoted against the frozen protocol

### §3 case eligibility — three items unsatisfiable today

A target case is eligible only if, **before arm execution**:

- **(c)** at least one candidate remote donor is known to a private adjudication
  key, or can be defined by a prospective discovery criterion. **No donor key
  exists for any candidate case.** SD80 records this as `PENDING`, not as
  satisfied.
- **(d)** the donor is outside the target's ordinary local retrieval
  neighbourhood **under the frozen baseline search system**. No such baseline is
  frozen.
- **(e)** the transfer consequence is nontrivial — correct donor handling can
  change a registered transfer/block/reopen/retain decision. Untestable while
  (c) is unmet.

Protocol §3 is explicit that cases failing any item are **`INELIGIBLE`, not
negative evidence**. Filing FM80 as a null would misreport an unbuilt study as a
tested one.

### §4 operational remoteness — the frozen artifacts do not exist

A donor is `REMOTE` only if all four conditions hold under a frozen corpus and
search date, and §4 requires that **K, the corpus snapshot, and the retrieval
model/version be frozen in the machine-readable companion before dispatch**.
None is frozen. Without them, "remote" is not decidable, and §4's own warning
applies: *a donor that is merely obscure but already surfaced by the matched
baseline is not evidence for remote-donor discovery.*

### §7 adjudication — an unmet human requirement

Each domain requires **at least two qualified adjudicators who did not build the
evaluated arm**, blinded to arm identity, with disagreements recorded before any
consensus meeting and a third adjudicator for pre-declared terminal
disagreements; expertise, conflicts and material dependence must be recorded.
This is a standing human-resource requirement that no amount of computation
substitutes for. It is not available to this lane.

### §8 sample — 90 eligible cases, ≥ 30 per domain

Minimum 90 eligible cases across three materially distinct domains, at least one
formal and two empirical. With §3 (c)–(e) unmet, the count of FM80-eligible cases
is **zero**, not merely short.

## 3. Whether FM80's eligibility rule could be satisfied differently

The brief asks that FM80 be treated as blocked-with-reason *unless its own
eligibility rule can be satisfied differently*. Checked before filing:

| route | verdict |
|---|---|
| Reuse a generated FM/FG suite as one of the three domains | **Excluded by the protocol itself**: §2, *"Reusing a generated FM/FG study as one of the three domains is not sufficient."* The FM10/FM20 protected suites cannot stand in. |
| Use SD80's formal domain (mathlib4 1000-theorems, 243 eligible cases) as the formal domain | Satisfies §2's formal-domain requirement and has machine-checkable witnesses, but supplies no **donor key** (§3c) and no frozen retrieval baseline (§4). It is a *target* corpus, not a donor-target pairing. |
| Define donors by a prospective discovery criterion instead of a private key | Permitted by §3(c) — and this is the one genuinely open route. It still requires §4's frozen corpus, K and retrieval model, plus §7's adjudicators. It is a real future design, not something satisfiable now. |
| Run a scoped pilot under §8 | §8 permits a scoped pilot below 90 cases, but *"cannot grant the standalone top-tier terminal"*. A pilot still needs eligible cases, and with §3(c)–(e) unmet there are none. |
| Drop the adjudication requirement | Not available. §7 is a protocol requirement and §6 makes the co-primary fidelity endpoint non-compensatory; weakening it would create a new prospective identity, not satisfy this one. |

So the blockage is **structural for the lane as frozen**, and the lever a future
cell needs is nameable and specific: a frozen corpus snapshot with a declared
retrieval baseline and K, a donor key or a prospective discovery criterion
registered before dispatch, and two independent qualified adjudicators per
domain. None of these is a computation this session can perform.

## 4. What is explicitly *not* claimed

- **This is not a negative result about transfer discovery.** No arm ran. §10's
  contraction terminals (`PARENT_OR_RETRIEVAL_SUFFICIENCY`,
  `REMOTE_DONOR_RECOVERY_WITHOUT_DECISION_VALUE`, and the rest) are outcomes of
  an *executed* study and none of them applies here.
- **The FM10/FM20 parent-sufficiency terminals do not transfer to FM80.** They
  are generated exact suites; §2 forbids substituting them for a naturalistic
  domain, and the FM protocol's global rules state that formal witness does not
  establish empirical truth. The naturalistic identity remains separate and
  unexecuted, exactly as ME-X4's receipt records for its own naturalistic cell.
- **P-A and P-B remain at `HOLD`.** §9's standalone survival terminal is
  unreachable without execution, and nothing here moves it.

## 5. Disposition

`FM80` → **blocked, with reason**, vocabulary
`BLOCKED_ELIGIBILITY_PRECONDITIONS_UNSATISFIED`, cited to §3 items (c)–(e), §4,
§7 and §8 of its own frozen protocol. Recorded in
`CONCEPTUAL_TRANSFER_FORMAL_EXECUTION_BACKLOG_V1.json`. The lane is not forced,
not weakened, and not filed as a null.

Authority: grants nothing; no scientific truth, no F2 superiority, no field
status, no submission readiness.

## 6. Independent verification of this receipt, 2026-09-03, with two corrections

The claims above were re-checked clause by clause against the frozen protocol,
after this receipt was written and by a reader who did not write it. **The
disposition stands and the citation set is the right one.** Two reporting
imprecisions were found and are corrected here rather than left standing, and one
inherited caveat is raised.

### Verified against the protocol text

- **§3 items (c)-(e)** exist as described (the protocol's bullets are unlettered;
  the a-g lettering is the repo convention SD80's schema also uses), and the
  INELIGIBLE rule is verbatim: *"Cases failing any item are `INELIGIBLE`, not
  negative evidence."*
- **§4** requires the freeze verbatim: *"K, corpus snapshot and retrieval
  model/version must be frozen in the machine-readable companion before
  dispatch."*
- **§7** requires *"at least two qualified adjudicators who did not build the
  evaluated arm"*, blinded to arm identity, disagreements recorded before any
  consensus meeting, and a third adjudicator for pre-declared terminal
  disagreements.
- **§8** requires *"Minimum target: 90 eligible cases, at least 30 per domain"*
  and permits a scoped pilot that *"cannot grant the standalone top-tier terminal"*.
- **§2** says verbatim: *"Reusing a generated FM/FG study as one of the three
  domains is not sufficient."*
- **No machine-readable companion exists.** Searched by basename with `find` and
  by content, with a control pattern that must match to prove the search works:
  the only FM80 artifacts in the repository are the protocol `.md`, the protocol
  `.json` and this receipt. The protocol JSON is arguably itself the companion,
  but it **binds none of the three required values**: its remoteness clause names
  no K, `pre_dispatch_freeze` lists `corpus_snapshot_ids` as an obligation with no
  value, and no retrieval model or version appears anywhere in it.

### Correction 1 — a section pointer, not a requirement

§3's heading above reads "§8 sample — 90 eligible cases, >= 30 per domain" and its
body folds in "three materially distinct domains, at least one formal and two
empirical". **That domain-structure requirement is §2, not §8.** §8 states only
the 90-case minimum, the 30-per-domain floor and the pilot clause. The substance
of the claim is correct; the citation was imprecise and is corrected here.

### Correction 2 — "the INTERNAL stratum came back empty"

§1 above says SD80's `INTERNAL` stratum "came back empty". SD80's own sufficiency
record shows `PSYCHOLOGY_RPP: INTERNAL 0`, `CANCER_BIOLOGY_RPCB: INTERNAL 0`,
`FORMAL_MATHEMATICS_1000PLUS: INTERNAL 1`. **One case, not zero.** SD80's terminal
is unaffected — PC-R7 §1 requires >= 15 per domain and 1 is as short as 0 — but
"empty" is wrong for the formal domain and is corrected here.

### Caveat — an inherited quotation that SD80's own data does not fully support

This receipt quotes SD80 faithfully: *"FM80 eligibility is therefore PENDING for
every case."* SD80's per-case file does not bear that out. Of its 455 records,
**393 carry `fm80_eligible = PENDING_DONOR_KEY_AND_REMOTENESS_FREEZE` and 62 carry
`INELIGIBLE`** (36 failing item (a), 26 failing item (f)). "PENDING for every case"
holds for the PC-R7-eligible pool, not for every record. The discrepancy is
**SD80's, inherited here by accurate quotation, and is raised to SD80's lane
rather than edited from this one.** It does not change FM80's disposition: 393
PENDING and 62 INELIGIBLE both give zero FM80-*eligible* cases.

## 7. The single blocking artifact, named precisely

The brief asks for one blocking artifact rather than a list. It is **§7's
independent adjudicators**, and it is strictly harder than the other three
preconditions:

- **§3(c) has a computable escape hatch.** The protocol permits *"a prospective
  discovery criterion"* instead of a private adjudication key. A criterion can be
  written and registered with no human panel.
- **§4's K, corpus snapshot and retrieval model/version are engineering acts.**
  Pinning a snapshot id, fixing K and versioning a retriever are things a session
  can do.
- **§7 has no hatch.** *"at least two qualified adjudicators who did not build the
  evaluated arm"* is a property of persons. Independence-from-construction cannot
  be manufactured by computation.

Decisively, **§7 is upstream of §4 and freezing §4's artifacts does not unblock
it.** §4's fourth remoteness condition reads: *"an independent adjudicator accepts
that the donor is scientifically relevant to the registered target decision."* So
even a fully frozen corpus, K and retrieval baseline still cannot establish a
donor as `REMOTE` without a qualified human. At three domains x two adjudicators,
plus a third for pre-declared terminal disagreements, the lane needs **six to nine
qualified, conflict-declared people independent of arm construction.**

The protocol anticipates exactly this and gives it a name: §10 lists
`CANNOT_CHECK_INDEPENDENT_ADJUDICATION` as a valid recordable terminal in its own
right.

**No protected run of FM80 is possible, and this is structural rather than a
matter of compute.** The disposition is unchanged:
`BLOCKED_ELIGIBILITY_PRECONDITIONS_UNSATISFIED`, blocked on a human-resource
precondition that no amount of computation substitutes for.

skills-applied: none (lane disposition receipt, no manuscript content)

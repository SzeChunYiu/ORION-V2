# FM80 — Pre-Outcome Design Correction V1

**Finding: at its own registered minimum sample, FM80's §9.1 effect-size bar and §9.2
significance clause are jointly unsatisfiable. A study delivering exactly the effect the
protocol declares scientifically meaningful would terminate as a null.**

**Status: PRE-OUTCOME.** FM80 has never been dispatched — no arm was run, no case assembled,
no outcome read (`fm-exact/FM80_BLOCKED_WITH_REASON_RECEIPT.md`, independently verified
2026-09-03). This correction is therefore recorded *before* any outcome exists, which is the
only point at which it is legitimate to record it. Nothing here changes after a run.

**Scope: this governs both P-A and P-B.** FM80's Purpose line defines it as "the minimum
naturalistic evidence that could support the surviving P-A and P-B standalone claims", and
§9 is titled "Standalone survival terminal" for those two papers.

## 1. The defect

§9 promotes P-A/P-B beyond `HOLD` only if, among other clauses:

> 1. A3 improves the protected decision endpoint over the frozen strongest baseline by at
>    least **10 percentage points** in at least two of three domains;
> 2. the paired 95% interval for those two domain improvements excludes zero after the frozen
>    multiplicity procedure;

§8 sets the sample:

> Minimum target: **90 eligible cases**, at least 30 per domain.

and the analysis:

> Report paired differences and exact paired tests with 95% intervals; adjust across the three
> domain-level primary tests using Holm.

At 30 cases per domain, a 10 pp improvement is **3 net cases**. Under an exact paired test only
discordant pairs carry information, so the most favourable table consistent with a 3-net-case
improvement is 3 pairs favouring A3 and **zero** favouring the baseline. That gives an exact
two-sided p of 2·(1/2)³ = **0.25** — a strict upper bound on achievable significance, since any
adverse discordance only inflates it.

Holm over three domain-level tests puts the first threshold at 0.05/3 = 0.0167 and the second
at 0.05/2 = 0.025. A p of 0.25 clears neither, nor the unadjusted 0.05.

**A domain landing exactly on §9.1's bar fails §9.2 with certainty.** Not with low power — with
certainty, at every possible pairing.

## 2. The arithmetic, in full

Best case throughout (zero adverse discordance, `u = 0`); real data can only do worse.

| cases / domain | 10 pp = net cases | best-case exact p | clears α = 0.05 | clears Holm-first 0.0167 |
|---|---|---|---|---|
| **30 (registered)** | **3** | **0.25000** | **NO** | **NO** |
| 40 | 4 | 0.12500 | NO | NO |
| 50 | 5 | 0.06250 | NO | NO |
| 60 | 6 | 0.03125 | YES | NO |
| 70 | 7 | 0.01562 | YES | YES |
| 90 | 9 | 0.00391 | YES | YES |
| 120 | 12 | 0.00049 | YES | YES |

Two ways of reading the gap, both stated because they differ:

- **Holding the effect bar at 10 pp:** the sample must reach **≥ 61 cases per domain** before
  the ceiling of a 10 pp improvement first reaches a Holm-detectable net count, and **70 per
  domain** before *exactly* 10 pp is detectable. Against the registered 30 per domain, that is
  **183–210 eligible cases against a registered 90**.
- **Holding the sample at 30:** the detectable effect is **20.0 pp unadjusted and 23.3 pp under
  Holm** — **2.0× to 2.3× the effect size §9.1 declares meaningful.**

Adverse discordance widens the gap sharply. At n = 30 with a 3-net-case improvement:

| adverse pairs `u` | favouring pairs `t` | exact p |
|---|---|---|
| 0 | 3 | 0.2500 |
| 1 | 4 | 0.3750 |
| 2 | 5 | 0.4531 |
| 3 | 6 | 0.5078 |
| 5 | 8 | 0.5811 |

## 3. Why this matters more than ordinary underpowering

This is not "the study is underpowered, so a real effect might be missed". It is that **the
protocol's own two clauses contradict each other over a range of outcomes it explicitly
declares scientific.** Any true effect in [10 pp, 20 pp) at the registered sample satisfies
§9.1 and *necessarily* fails §9.2. The study would then terminate on one of §10's contraction
vocabularies — `PARENT_OR_RETRIEVAL_SUFFICIENCY`, most likely — and that terminal would be
read as evidence that typed donor transfer adds nothing, when what actually happened is that
the design could not have said otherwise.

That is the manufactured-finding failure mode: a clause unsatisfiable by construction reading
as an empirical negative. Detecting it after the run would be too late, because §10 forbids
redesigning the same cases after outcome access.

## 4. The correction

Recorded as a pre-outcome correction to FM80. Whichever branch a future execution takes must
be chosen and frozen **before** case assembly, not after:

1. **Raise the sample** to ≥ 61 eligible cases per domain (≥ 183 total) if the 10 pp bar is the
   scientifically meaningful effect; or
2. **Raise the effect bar** to the sample's actual Holm-detectable resolution — 23.3 pp at
   n = 30 — and say plainly that FM80 as sampled can only detect large effects; or
3. **Change the analysis** to a paired test that uses concordant pairs (§8 currently specifies
   exact paired tests, which do not), and re-derive the joint reachability before freezing.

Option 2 is the honest minimum and costs nothing; option 1 is what the protocol's stated
scientific intent implies. **Option 3 must not be chosen merely because it is cheapest** — the
exact paired test was specified deliberately, and swapping it for a more permissive one after
seeing this analysis would be relaxing a frozen protocol, which §12 forbids.

**No case has been assembled, so no branch is foreclosed.** This correction restores a choice
that the current freeze would have quietly removed.

### 4.1 What this document is, stated exactly

**The protocol file is not amended.** §8 still reads 30 per domain and §9.1 still reads 10 pp.
What ships is this sibling document plus a non-amending pointer added at FM80 §8/§9 naming it a
binding pre-execution read. The pointer selects no branch, so no threshold, sample or test is
changed and §12 is untouched.

That is deliberate. Selecting a repair branch is a design act belonging to the lane that will
execute FM80, and picking the cheapest branch after seeing this analysis is precisely what §12
forbids. The accurate status vocabulary is therefore
**`DEFECT_FOUND_AND_DOCUMENTED__REPAIR_BRANCH_UNSELECTED`**, not "corrected" — a distinction of
the same kind as the programme's own finding that parent *implementations* were faithful while
the parent *labels* overstated them.

The pointer matters as much as the analysis. A correction nobody reads is a sentence nobody
executed: without it, whoever opens FM80 to run it sees the defective floor with no warning.

### 4.2 §8 states a floor, which is why the repair is cheap

§8's words are *"**Minimum** target: 90 eligible cases, at least 30 per domain"* — a floor, not a
ceiling or a plan. A compliant study may assemble more. So option 1 does not require finding
extra cases the protocol never wanted; it requires **raising the stated floor from 30 to 61**,
after which the §9.1/§9.2 conflict simply disappears. That strengthens the correction rather than
weakening it: the defect is in the floor's arithmetic, not in the study's ambition.

### 4.3 The defect does not depend on reading §9.2 as exact McNemar

§8 specifies "exact paired tests with 95% intervals", so exact McNemar is the natural reading —
but the conflict survives the alternative. A Wald interval on the paired difference at n = 30 with
b = 3, c = 0 gives **0.100 ± 0.113** on the standard SE √((b+c)/n²), or **0.100 ± 0.107** with the
(b−c)²/n correction. Both include zero **even unadjusted**, before Holm touches anything. A reader who takes "paired 95% interval" to mean something other than exact McNemar reaches
the same conclusion.

## 5. Reachability audit of the remaining §9 clauses

| clause | satisfiable? | failable? | note |
|---|---|---|---|
| 9.1 ≥ 10 pp in ≥ 2 of 3 domains | yes | yes | reachable in isolation; see §1 for the conflict with 9.2 |
| 9.2 paired 95% interval excludes zero, Holm | yes at n ≥ 61/domain | yes | **unsatisfiable jointly with 9.1 at n = 30** |
| 9.3 no increase in critical native-fidelity failures | yes | yes | strict and non-compensatory by design (§6); intended |
| 9.4 ≥ 1 winning domain has genuinely `REMOTE` donors | **human-gated** | yes | §4.4 requires an independent adjudicator to accept scientific relevance; not machine-decidable |
| 9.5 A2 does not reproduce the A3 gain | yes | yes | note A2 is absent from §8's primary comparison yet load-bearing here — A2 must be run and analysed regardless |
| 9.6 effect survives excluding donor-visible cases | yes | yes | |
| 9.7 adjudication finds no stronger omitted parent | **human-gated** | yes | |

Arm contrasts were checked for existence rather than assumed. A2 (structure-first donor search
**without** the native-fidelity gate) and A3 (donor search **plus** typed transfer gate) diverge
by construction, so the §9.5 contrast can exist. A4 is correctly excluded from the primary
superiority test as an oracle ceiling rather than a deployable comparator — it is named for
what it is, not as a parent.

## 6. This does not unblock FM80, and does not weaken the block

The lane remains `BLOCKED_ELIGIBILITY_PRECONDITIONS_UNSATISFIED`. The blocking artifact is
unchanged and is a property of persons, not of computation: §7's "at least two qualified
adjudicators who did not build the evaluated arm", per domain, plus a third for pre-declared
terminal disagreements. §4.4 and §9.4 and §9.7 each independently require human adjudication as
well, so the human gate is **multiply determined** — four distinct clauses, not one.

Nothing in this correction is a route around that. Fixing a sample-size arithmetic defect makes
the study sound *when someone is finally able to run it*; it does not make it runnable. A
machine-checkable surrogate for §4's remoteness condition was considered and rejected: §4.4
makes `REMOTE` non-machine-decidable by construction, so a surrogate would **replace** the
clause rather than satisfy it, and §9.4 would then be unsatisfiable in principle — reproducing,
deliberately, the exact defect this document exists to prevent.

## Custody

- Audited: `research/experiments/FM80_NATURALISTIC_TRANSFER_DECISIVE_PROTOCOL_V1.md` §§2–12
  and its `.json` twin (frozen 2026-08-30, never amended).
- Block receipt relied on: `research/experiments/fm-exact/FM80_BLOCKED_WITH_REASON_RECEIPT.md`
  (independently re-verified 2026-09-03, two corrections applied there).
- Arithmetic: exact McNemar over every paired table consistent with the stated margins,
  Python 3.13.12. Reproduced by `scripts/verify_fm80_section9_reachability.py --self-test`.
- ORION-V2 main head at audit: `ec3a13eda167d6dc9214d62206d4525bf27d0e30`.

## Authority

Grants nothing: no scientific truth, no P-A/P-B survival, no field status, no publication
readiness, no release authorization. This is a pre-outcome repair to a frozen design that has
never been executed.

skills-applied: none (protocol design audit, no manuscript content)

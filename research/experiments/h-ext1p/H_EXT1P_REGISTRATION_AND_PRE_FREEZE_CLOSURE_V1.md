# H-EXT-1P — registration, pre-freeze audit, and closure without dispatch (V1)

**Status:** `REGISTERED_AND_CLOSED_PRE_FREEZE`.
**Terminal:** `REGISTERED_CONTRAST_CANNOT_BE_ABOUT_THE_MECHANISM` — a `CANNOT_CHECK`-class
terminal, reached **before** any freeze, seed commitment or dispatch, and deliberately
distinct from a negative.

```text
H_EXT1P_STATUS                 = REGISTERED_AND_CLOSED_PRE_FREEZE
H_EXT1P_TERMINAL               = REGISTERED_CONTRAST_CANNOT_BE_ABOUT_THE_MECHANISM
H_EXT1P_DISPATCHED             = FALSE   (0 model calls, 0 tasks generated, no seed committed)
BLOCKED_BY_POWER               = FALSE   (n = 1040 reaches 0.80; task supply is unbounded)
BLOCKED_BY_ESTIMAND            = TRUE
CHANGES_H_EXT_1                = NONE    (no gate, null, terminal, datum or receipt value moves)
GRANTS_SCIENTIFIC_TRUTH        = false
GRANTS_FIELD_STATUS            = false
```

H-EXT-1's outcome receipt, item 2, names this successor and leaves it unstarted:
*"`H-EXT-1P`, a fresh-seed prospective cell pre-registering a paired null on
`acc(GATED_M) − acc(PARENT)` with its own freeze, gates and routed terminals."*
Registering a study is the register owner's call; the row is added in this pass
(`research/field/MACHINE_EPISTEMICS_EXTENSION_HYPOTHESES_2026_09_02_V1.md`), and it is
registered **and closed** in the same pass, for the reason below.

---

## 1. What was asked, and what the audit found instead

The scoping note flagged one hazard: the margin is 11 tasks in 520, a paired test turns
on **discordant pairs rather than n**, a naive repeat at n = 520 would likely return
inconclusive, and "inconclusive" on a study framed as *does the parent margin hold up*
would be read as a negative. The instruction was to justify power before freezing, and
to decline the study if no feasible n can answer it.

**The power hazard is real but does not bind.** It was measured, not guessed:

| n | power (exact two-sided McNemar, α = 0.05) |
|---|---|
| 520 (the frozen cell's own n) | **0.4605** |
| 800 | 0.6810 |
| 1000 | 0.7865 |
| **1040** | **≥ 0.80** |
| 1200 | 0.8601 |
| **1360** | **≥ 0.90** |
| 1500 | 0.9279 |
| 2000 | 0.9787 |

So a naive repeat at n = 520 would indeed have been a coin flip — but n = 1040–1500 is
both sufficient and feasible, and the study could have been sized. **Feasibility was
checked rather than assumed:** the P-D suite's task generators are
`PD_GENERATORS[study][stratum](rng, index)` in
`scripts/run_dependence_evidence_generated_suite.py`, driven by a free `strata_counts`
plan dict; the only use of `index` anywhere in the sixteen generators is `index % 3`
(two strata), so **task supply is unbounded** and n = 1200 is a plan edit, not a new
corpus. Cost would be 1200 × 3 arms = 3600 model calls against H-EXT-1's 1560.

**What blocks H-EXT-1P is not power. It is the estimand.**

## 2. The finding: on every task where the gate fires, the two arms are tied at ceiling

Decomposing the registered contrast by whether the frozen gate `G_B_PLUS_XREF` actually
activated — the split that decides whether the contrast can be *about* conditional
activation at all:

**PROSPECTIVE cell (binding), n = 520, 170 activations**

| subset | n | `GATED_M` | `PARENT` | b (GATED only) | c (PARENT only) | discordant | exact p |
|---|---|---|---|---|---|---|---|
| **SUITE** | 520 | 508 | 497 | 20 | 9 | 29 | 0.0614 |
| **GATE ACTIVE** | 170 | **170** | **170** | **0** | **0** | **0** | 1.0 |
| **GATE INACTIVE** | 350 | 338 | 327 | 20 | 9 | 29 | 0.0614 |

On the 170 tasks where the dependence machinery is switched on, `GATED_M` and the
strongest assurance federation are **both perfect and never differ on a single task**.
All 29 discordant pairs — the entire evidential content of the paired test — lie on the
350 tasks where the gate never fires and `GATED_M` **is** `P_D_MINUS_DEPENDENCE` by
construction. There, the contrast is the always-off arm against the parent; the
mechanism under study contributes nothing to it.

By study family, the concentration is sharper still:

| study | n | activations | `GATED_M` | `PARENT` | b | c |
|---|---|---|---|---|---|---|
| PD-S1-DEPENDENT-CORROBORATION | 160 | 80 | 160 | 159 | 1 | 0 |
| **PD-S2-ARGUMENT-AND-ADEQUACY** | 120 | **0** | 108 | 98 | **19** | **9** |
| PD-S3-REVOCATION-AND-UPTAKE | 120 | 90 | 120 | 120 | 0 | 0 |
| PD-S4-AUTHORITY-AND-RESPONSE | 120 | 0 | 120 | 120 | 0 | 0 |

28 of 29 discordant pairs, and 10 of the 11 net margin, come from **one family on which
the gate never activates once**. The mechanism's own net contribution to the parent
margin, across the two families where it fires at all, is **+1 task in 280**.

**The secondary cell replicates the pattern independently.** RETROSPECTIVE_EVAL, n = 520:
suite b = 7, c = 1; gate-active b = 0, **c = 1** (the one discordant active task is one
`GATED_M` *loses*); gate-inactive b = 7, c = 0. In both cells, every task favouring
`GATED_M` over the parent is a task where the gate is off.

## 3. Why that closes the study rather than shrinking it

A well-powered H-EXT-1P at n = 1200 would very probably return `p < 0.05` on
`acc(GATED_M) − acc(PARENT)`. It would then be read — on a study whose stated purpose is
to attach uncertainty to *the parent margin of a conditional-activation mechanism* — as
evidence that conditional activation beats the strongest parent. The frozen data show
that reading is unavailable: wherever activation occurs, the arms are identical. The
test would be measuring the base always-off arm's advantage over the parent on PD-S2,
with the activation gate contributing nothing but the label on the arm.

That is precisely the pre-freeze audit item the protocol requires — *a contrast that
could not exist; ask whether these arms could EVER have differed* — and here the answer
is available before the freeze, from data already on `main`, at zero dispatch cost. It
is caught in the correct direction: **not** by discovering the run was underpowered
after spending it, and **not** by narrowing a clause after seeing an outcome.

Two estimands were therefore separated, and each is disposed of on its own terms:

| estimand | measurable? | powered? | worth running? |
|---|---|---|---|
| `acc(GATED_M) − acc(PARENT)` over the suite | yes | yes, at n ≥ 1040 | **no** — a significant result would not be about the mechanism |
| the same contrast restricted to gate-active tasks (the mechanism-attributable quantity) | yes | **no n confers power**: 0 discordant pairs at 170/170 vs 170/170 | **no** — a ceiling tie has no effect to size against |

The second row is a genuine `CANNOT_CHECK`, not a negative: it does not say conditional
activation fails to beat the parent, it says **this suite cannot ask**, because both arms
saturate wherever the question arises. Fewer than six discordant pairs can never reject
at α = 0.05 however they fall (`2/2⁵ = 0.0625`); here there are zero.

## 4. What this does and does not do to H-EXT-1

**It changes nothing in H-EXT-1, and no correction to it is implied or made.** H-EXT-1's
binding terminal — `CONDITIONAL_ACTIVATION_IDENTIFIABLE_FROM_EVIDENCE_STRUCTURE` — rests
on G1 and the two registered nulls against **always-on `M`** (`GATED_M` 508 vs `M` 465,
advantage +0.0827, exceedance 0/2000 in both nulls), and that contrast is untouched: it
lives on PD-S1, where `M` scores 124/160 and `GATED_M` 160/160. Routing by evidence
structure demonstrably recovers the positive-stratum gain and removes the drag. That is
the claim H-EXT-1 registered and it stands exactly as receipted.

This audit is **continuous with H-EXT-1's own disclosure**, not a catch it missed.
Receipt item 4 already recorded that 90 of the 170 activations are PD-S3 tasks where all
three arms are at ceiling, and that *"a suite where the machinery had a cost on such
tasks would expose this."* The measurement here extends that observation from 90
activations to all 170, and draws the consequence for the parent contrast specifically.
Receipt item 2 already refused to attach G3's authority to the +2.1 pp margin and warned
that a reader must not borrow it. This audit shows a stronger version of the same
caution: not merely that the margin lacks a null, but that **a null on it would not
license the sentence a reader would write from it.**

## 5. What a study that could ask the question would need

Recorded because a negative is intermediate and must name its lever. Attributed to one
stage: **the task suite**, not the gate, not the arms, not the statistics.

The blocking property is that the parent is already perfect (170/170) on every
gate-active task. Any successor must first establish, on a development split and before
any comparison, that the strongest parent is **off ceiling** on the gate-active regime —
i.e. a suite in which the dependence machinery has a cost or an error the parent does not
also avoid. A design that cannot demonstrate parent headroom on the activation regime
should not be frozen: it is this study again under another name. That is a corpus-design
problem, and it is the same wall receipt item 5 names (suite-internal identifiability
only), reached from a different direction. **No such suite is claimed to exist, and none
is scoped here.**

The disallowed repair, stated so it is not tried: enriching the suite toward PD-S2 to
raise the discordant count would change the estimand from suite accuracy to
PD-S2 accuracy while keeping the old name, and would make the mechanism's
non-participation harder to see rather than easier. Pre-registering a smaller α, more
draws, or a different paired test changes none of it — the gate-active subset has no
effect to test.

## 6. Provenance, and how the numbers were kept from being prose

- Worktree cut from `origin/main` `ec3a13eda167d6dc9214d62206d4525bf27d0e30`;
  `/usr/bin/git` for every decision.
- Computed by `scripts/h_ext1p_estimand_audit.py`
  (sha256 `f2f7d6017c8880fd110ca97cbdab89bd1c98082ea17597ac9b90a0838076470e` at first run),
  interpreter **CPython 3.13.12** (`/usr/bin/python3` is 3.9 on this host and is not used
  for anything trusted). Output artifact: `H_EXT1P_PRE_FREEZE_AUDIT_V1.json`.
- **The gate rule is imported, not reimplemented.** `gate_fires` comes from
  `scripts/h_ext1_gate_study.py`
  (sha256 `a46a7282101075ef42dd2de64df1d12364b9f84b962df9c5ccea35640d128460`), and the
  gate id is read from `H_EXT1_GATE_FREEZE.json`
  (`52f556e82496c2b6f4490410518ba3a8061783bd13a112142f26720d50f96584`,
  `selected_gate: G_B_PLUS_XREF`) rather than hardcoded. An earlier draft reconstructed
  the rule from the receipt's prose; that reading was replaced by the import.
- **The reconstruction is controlled against six numbers the frozen receipt published
  independently**: n = 520, activations = 170, `GATED_M` = 508, `M` = 465, `OFF` = 428,
  `PARENT` = 497. All six reproduce; a wrong gate rule or a wrong routing rule would miss
  at least one. The script exits **4** — its own code, distinct from a clean run and from
  a missing input (**3**) — if any of them disagrees.
- Frozen inputs read, unmodified:
  `data/PROSPECTIVE_instances.json` `aa017e53b60a79713c62a5d849f3d7c785d5df78465bbf9bdb29a3475f3df4dc`,
  `data/RETROSPECTIVE_instances.json` `01d8348a5bb9c3a0e3a29a0ffd1e3b0024d99aa6d080c85ac453f4b7da4873a6`.
- **The load-bearing facts are executable assertions**, not prose:
  `tests/unit/test_h_ext1p_estimand_audit.py` — **11 passed, exit status 0**, read from
  `$?` with no pipe.
- **Both zeros carry a control that must fire.** `test_the_control_check_can_fail`
  substitutes always-on `M` for the routing rule and the six-number control rejects it.
  `test_the_gate_active_decomposition_would_report_discordance_if_any_existed` flips the
  parent's outcome on 7 gate-active tasks and the same decomposition reports b = 7,
  p < 0.05 — so `b = 0, c = 0` is a measurement and not an empty counter. The power
  function is separately checked for **size** under the null (`pb = pc` ⇒ power ≤ α) and
  saturation under a large effect.
- **Denominators are published with every zero**: 0 discordant of 170 gate-active
  (PROSPECTIVE); 1 discordant of 170, in the parent's favour (RETROSPECTIVE); 0 of 120 in
  PD-S3 and 0 of 120 in PD-S4.

**Stated as a limitation of this audit, not glossed:** the power figures use the frozen
cell's own observed b and c as the effect size. That is an observed-effect power
calculation and is optimistic by the winner's curse, so n = 1040 is a **lower** bound on
what a prospective replication would need. It is reported anyway because it runs against
this document's own conclusion — an optimistic power estimate makes the study look *more*
runnable, and it is still not run, because power was never the binding constraint.

**What could not be checked, kept distinct from what was checked and is fine:** whether
the gate-active ceiling tie would persist on a fresh seed at larger n (not run — no
dispatch was made, and the two independent frozen cells agreeing is evidence but not
proof); and whether any P-D-family suite exists in which the strongest parent is off
ceiling on the gate-active regime (§5 — not scoped, not searched, not claimed).

---

*No campaign was dispatched. This document grants no field status, no novelty, no
manuscript change, and no dependence-detection claim in real corpora. It closes one
registered successor and leaves H-EXT-1 exactly as frozen.*

skills-applied: none (receipt, no manuscript content)

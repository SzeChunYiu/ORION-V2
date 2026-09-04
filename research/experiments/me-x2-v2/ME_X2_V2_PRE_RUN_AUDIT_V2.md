# ME-X2-V2 — pre-run audit of the frozen design, recorded BEFORE the protected run

**Status when written: no protected instance of ME-X2-V2 has been generated or
inspected.** Everything below is a check on the frozen design, its runner and its
public development surfaces. No design, gate, threshold, seed, arm, lever, oracle
rule or generator rule is changed here. Every item is a *pre-outcome* finding.

Interpreter: `/opt/homebrew/bin/python3.12` (CPython 3.12.13).

| file | sha256 |
|---|---|
| `ME_X2_V2_LOOKAHEAD_REACHABILITY_REVIVAL_DESIGN_V2.json` | `9ea8c8cd890a0f2e2df1395e58a49f10708e5b0a48f13474c9044fba61a800de` |
| `mex2v2_run.py` | `274c8a64d50b5ddd665dbe932491634383080af06caa285d5f75635eb6c61ebc` |
| `mex2v2_levers.py` | `9cfc1304c36616a03d6847c492bd66747fa13d1df08c8d6732b4704b04900f02` |
| `mex2v2_arms.py` | `458c8fa09589a1519c2ce6a10dbeb591f30bb5f0cbb05789c6a98dbd79166364` |
| `mex2v2_provenance.py` | `ac9e54c7d6079298d7a0c9a3154e8839d2e9097b412f6725ab95af87986c2517` |

## A1 — The terminal that stands today rests on 48 development instances

`ME_X2_V2_DEVELOPMENT_ANALYSIS_V2.md` routes `PARENT_SUFFICIENT` with lever
verdict `LEVERS_NULL` on **48 instances**. The file's own first line says the
split is not protected evidence, and it is right. **No protected run of
ME-X2-V2 exists.** This audit precedes the first one.

## A2 — Could the decisive contrasts EVER have differed on the development split?

This is the question that decides whether the development verdict means anything,
and for two of the three decisive contrasts the answer is **no**.

| contrast | dev discordant pairs | exact two-sided p | could it have fired? |
|---|---|---|---|
| G1b: M2 vs B5 | **1** (M2 1, B5 0) | 1.0 | **No.** One one-directional discordant pair gives p = 1.0; the gate needs p <= 0.05. |
| G5a: M2 vs V1's M | **0** | 1.0 | **No.** Zero discordant pairs. The arms produced identical decision-correct vectors on all 48 instances. |
| G5c: mechanism attribution | denominator **0** M2-only-correct instances | n/a | **No.** A rate computed on an empty denominator. |
| G5d: failure not moved | `only_v1` 0 vs `only_m2` 0 | n/a | **No.** `0 < 0` is false for reasons that have nothing to do with the mechanic. |

`M2_LOOKAHEAD_PLUS_BEST_HYPOTHESIS`, `M2_L1_LOOKAHEAD_ONLY` and
`M_ME_LOCUS_PLUS_MINIMUM_ESCALATION` all score exactly **1.000** on the
development split. The verdict `LEVERS_NULL` is therefore not a measurement that
the levers changed nothing; it is what the routing returns when the measurement
could not be taken. **That is precisely the defect shape this programme calls a
contrast that could not exist, and it is the reason the protected leg is owed.**

The ceiling is a small-n artefact and this is checkable rather than assumed:
V1's own **protected** run at n = 1200 scored `M_ME_LOCUS_PLUS_MINIMUM_ESCALATION`
at **0.9625** and `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` at **0.9825**
(paired diff -0.020, exact p = 0.0032). Neither arm is at a ceiling at protected
size, so at n = 1200 the G5a contrast is measurable in a way it was not at n = 48.
The design's own power note registers that 6 one-directional discordants reach
p = 0.031 and 8 reach p = 0.008 at the pooled protected n.

The routing is nevertheless sound, and this was checked rather than presumed:
`c_ok = bool(only_m2) and mech_rate >= MECHANISM_MIN` requires a **non-empty
denominator**, and both G5c and G5d are consulted for the lever verdict only
after G5a has already established a significant M2 - V1 difference. The
zero-denominator values reported on the development split are inert, not
load-bearing. They are named here so that no reader takes `c_pass: false` on a
denominator of zero for a checked failure.

## A3 — Are the levers mechanically live, and on what denominators?

Measured on the 48 development instances, from the executed lever receipts
(`receipts_executed` 100, `receipts_considered_not_executed` 0):

| quantity | value |
|---|---|
| receipts emitted by `M2_LOOKAHEAD_PLUS_BEST_HYPOTHESIS` | 100 over 48 instances |
| receipts where **L1 changed the choice** | 16 / 100 (15 / 48 instances) |
| receipts where the chosen action was **L2-only-admissible** | **0 / 100 (0 / 48 instances)** |
| receipts where L2 **widened the admissible set** (`n_admissible != n_admissible_under_v1_rule`) | 36 / 100 (25 / 48 instances) |
| receipts with positive expected abstention | 18 instances |
| receipts with permitted foreclosure | 0 instances |

So **L1 fires and changes behaviour; L2 changes the admissible set on half the
instances but has never yet been the reason an action was chosen.** G5c's clause
is satisfiable through its L1 disjunct on this evidence; its L2 disjunct has no
observed support. Published here as a denominator so that whatever the protected
split returns, the reader can see which lever the attribution rests on.

A related diagnostic, registered before the run: on the development split
`M2_L2_BEST_HYPOTHESIS_ONLY` is **worse** than V1's M (paired diff -0.083,
4 instances lost, 0 gained, exact p = 0.125). L2 alone is not obviously
beneficial, and the conjunction's value — if any — is expected to come from L1.

## A4 — A reporting asymmetry between the lever arms (audited, routes nothing)

`M2_L2_BEST_HYPOTHESIS_ONLY` emits **zero** lever receipts on all 48 development
instances, while the conjunction arm emits 100 and `M2_L1_LOOKAHEAD_ONLY` emits
100. This is not a dead arm: L2-only overrides `_reserve_ok` and its decisions
differ from V1's on 4 instances. It is a reporting gap — receipts are appended
inside the L1 branch of `_discriminators`, and the L2-only arm returns through
`super()._discriminators` before reaching it.

Consequence for the gates: **none.** G5c reads the receipts of the *conjunction*
arm (`act` is built from `sc["lever_activity"]`, which is M2's), and G5b uses
decision-correct vectors, not receipts. The asymmetry is recorded so that a
reader does not mistake "no receipts" for "no lever activity" in the L2-only row.
It is not repaired, because changing a frozen arm's instrumentation after the
freeze is exactly what the no-rescue clause forbids.

## A5 — G0d provenance: V1's world has not moved

The runner refuses the protected stage (exit 5) unless every frozen V1 file is
byte-identical to the hash published in V1's receipt. Verified in advance, all
eight files match:

`ME_X2_LOCUS_DIAGNOSIS_EXACT_STUDY_DESIGN_V1.json`, `mex2_arms.py`,
`mex2_catalogue.py`, `mex2_generator.py`, `mex2_model.py`, `mex2_oracle.py`,
`mex2_parents.py`, `mex2_run.py` — all OK. G0d will pass.

## A6 — Determinism and inherited status

`stage_analyze` reads `selftest_ok` from `ME_X2_V2_SELFTEST_REPORT.json` in the
output directory rather than recomputing it, so a protected analysis written next
to a development-era report would inherit a rendered status. Closed by
re-derivation:

- `mex2v2_run.py selftest` re-run under 3.12 reproduces the committed report with
  a single differing field, `v1_dir`, which records the absolute path of the
  checkout and carries no scientific content. Verdicts identical: V1 provenance
  True, parent tests 21/21, known-answer 14/14, lever known-answer 6/6,
  separation True, oracle agreement True, null calibration True.
- `mex2v2_run.py dev` re-run under 3.12 reproduces
  `ME_X2_V2_DEVELOPMENT_RESULTS_V2.json` at sha256
  `533b38af3f8965b3ae34f43f21a66bdfa5073b6502ed6465790fcd452f209485`,
  byte-identical to the frozen value, and the custody file at
  `cb7d75876ae4a5169ab301689e07db1a6bedace83d1e077a3fc1292c64b03131`.

Control: `/usr/bin/diff` of the regenerated selftest report against a different
file in the same directory returns 1, so the comparison is live.

## A7 — Numerical safety at the registered protected size

The exact two-sided binomial is integer-exact (`math.comb` over Python ints
divided by `2**n`). Exercised at the protected extremes — (0,0), (6,0), (600,600),
(1200,0), (0,1200), (700,500), (1199,1) — it returns without raising, in
milliseconds. No gate can raise at n = 1200 for this reason.

Coverage at scale is already established on a **public** seed: the committed
`ME_X2_V2_G0SCALE_PROBE_V2.json` ran 1200 instances with V1-known arms only and
passed — decoy coverage OK, inverse decoy coverage OK, variant invariants hold,
exhaustive oracle agreement on all, `C_NEVER_INTERVENE` correct on 0 of 1047
identifiable instances, `C_RANDOM_POLICY` 0.178, V1's M within-pair swap margin
OK. The generator and oracle are therefore known to behave at the protected size.

## A8 — Comparator fairness

The comparator `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` is an exact planner
composed from the registered parents; it receives the same instances, the same
budget, the same registered outcome tables and the same uniform prior over live
causes as M2. Both arms are code, not prompts, so the procedural asymmetry found
in ME-F1 — a mechanism whose prompt named a rule the parent's did not — has no
analogue here: neither arm is given a rule the other is denied, and M2 subclasses
V1's M overriding exactly two methods.

The comparator is not artificially isolated. The interface ladder reports the
federation's rungs separately (`B5_R1_VERDICT_ONLY` ... `B5_R4_PLUS_DISPOSITION_RECORDS`)
and the top rung equals the federation, and a deliberately *stronger* variant
(`B5_NO_ABSTENTION_GATE`) is also run. If anything the comparator is favoured:
at V1's protected size it beat V1's mechanic by 0.020 at p = 0.0032.

One asymmetry runs the other way and is registered: B5 buys its decisions with
false escalation (21 at V1's protected n, against V1's M's 0). `G2_ANTI_ESCALATION`
holds M2 to **both** B5's and V1's M's escalation harm, so M2 must keep 0 false
escalations at n = 1200 to pass. That is the tighter of the two bounds and it is
the mechanic, not the comparator, that is held to it.

## A9 — Route and verdict wordings registered in advance

Registered here before the split exists, so no wording can read as post-hoc:

- **If G1a passes** (B5 reproduces M2's decision sequences), the route is
  `PARENT_SUFFICIENT` and, per the design's own `g1a_reading_registered_in_advance`,
  the finding is that *the improved rendering of ORION's unfixed orderings is
  reproduced by an exact planner* — a stronger parent-sufficiency result than
  V1's, not a weaker one. The development identity rate is 0.667, so this is not
  where the development split pointed.
- **If G1b fires**, the route depends on G2, G3 and cost in the registered order.
- **If neither**, the route is `PARENT_SUFFICIENT` — either `B5_DOMINATES` (G1c)
  or "discordance without significance".
- **The lever verdict is the decisive content of this lane** and is routed
  independently by G5a. `LEVERS_NULL` on a protected split where the arms *can*
  differ means something the development `LEVERS_NULL` did not: that the levers,
  given a measurable contrast, did not move the decisions. `LEVERS_HARM`,
  `LEVERS_MOVE_THE_FAILURE`, `LEVERS_NOT_ATTRIBUTED`, `LEVERS_PARTIAL_RECOVERY`
  and `LEVERS_RECOVER_M` remain reachable.
- The design's falsifiable per-stratum prediction stands as registered: M2's
  residual failures should shift toward missed escalation on the high-level
  strata (`MEASUREMENT_OR_EVALUATOR_BLIND`, `TOOL_INSTRUMENT_INADEQUATE`,
  `WORKFLOW_INADEQUATE`). Reported, not gated.

## A10 — What this audit did not do

No protected-scale dry run of the V2 arms. The design registers that omission
deliberately (`development_surfaces_disclosed.no_protected_scale_v2_dry_run`),
on the grounds that running the V2 arms at scale before the protected run would
expose the V2 comparison on a public seed. That registered decision is respected
rather than overridden for comfort. The residual risk is a mid-run exception, and
the design's `no_rescue_clause` already names the disposition: the lane halts, is
receipted, and re-freezes as V3 — a protected result is never re-run under a new
seed.

The protected seed was hashed against the frozen commitment and not otherwise
read before the run.

Authority: this audit grants nothing. It establishes what the development leg
could and could not measure, and fixes in advance the denominators against which
the protected verdict will be read.

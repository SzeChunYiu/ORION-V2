# FM70 Contextual Regime Selector — Prospective Design V1

**Lane:** `FM70_CONTEXTUAL_REGIME_SELECTOR` (owner issue #48; execution via #45/#50).
**Date frozen:** 2026-08-30.
**Machine-readable twin:** `FM70_CONTEXTUAL_REGIME_SELECTOR_PROSPECTIVE_DESIGN_V1.json`.
**Status after this document:** prerequisite "valid SIMPLE/F0/F2 outcomes available" is
satisfied by the E30 R11 terminal (development fold). Feature freeze, Gate 0 and any
held-out dispatch remain to be executed in that order.

## 1. Scientific question

E30 R11 executed the confirmatory real-repair cell and returned a null success endpoint:
no arm separated (F2 5/40, F0 5/40, reflection 4/40, direct 6/40; all Holm p = 1.0). The
pre-declared contraction rule was engaged. FM70 is the routing revival question, asked
before any component is discarded: **do pre-outcome task features carry enough signal to
route each task to the arm that wins on it?** If yes, the correct disposition is a
contextual activation claim (selector beats every always-arm on the held-out
quality-resource frontier without simple-task regression — the lane's frozen terminal
rule). If no, the contraction stands with routing excluded as a mechanism, recorded as a
cheap terminal.

## 2. Development fold (exists, frozen)

- **Data:** E30 R11 terminal raw rollup (PR #86, main `833fe0b`): 4 arms x 40 tasks x 3
  repetitions, `agent_status` 480 x `COMPLETED_PROPOSAL_ONLY`, per-cell `native_success`
  under the frozen registered-failing-test lane.
- **Aggregation:** within-task majority across repetitions (the E30 registered rule).
- **Direction of reuse (leakage discipline):** E30 outcomes are *confirmatory test data
  for E30* but *development/training data for FM70*. FM70's own held-out outcomes are
  never used for training or feature tuning. This satisfies the lane prerequisite
  "without reusing confirmatory test outcomes for training" — the reused outcomes are
  FM70's training fold, not FM70's test fold.

## 3. Dev-fold signal audit (computed 2026-08-30, binding input to Gate 0)

- Tasks where arms disagree at majority level: **5/40** (ansible-6, cookiecutter-1,
  scrapy-1, scrapy-4, tqdm-1).
- Tasks where some arm succeeds at some repetition: 22% (9/40).
- **Oracle routing ceiling:** union of tasks where at least one arm has majority success
  = **8/40 (0.200)** vs best always-arm SIMPLE_DIRECT **6/40 (0.150)**. A *perfect*
  selector gains at most **+2 tasks** over the best always-arm on this distribution.
- Repetition instability at n=3: 6/4/2/4 flipping tasks (F0/F2/REFL/SIMPLE).

Consequence recorded before any spend: the dev fold's own headroom is small; Gate 0
exists to fail cheaply here rather than after a held-out campaign.

## 4. Pre-outcome feature freeze (to execute; hash then commit)

Features are computable from the task workdir **at dispatch time t=0**, before any arm
runs. Excluded by rule: gold-patch geometry, any evaluation outcome, any run telemetry.

| ID | Feature | Source |
|---|---|---|
| P01 | project identity (8 one-hots; unseen projects bucket to "other") | task id |
| P02 | target-file lines of code | buggy file at exact commit |
| P03 | target-file function + class definitions count | buggy file |
| P04 | registered failing-test count | `bugsinpy_run_test.sh` binding |
| P05 | failing-test source length (chars) | test file at exact commit |
| P06 | project python file count | repo tree at exact commit |
| P07 | dispatched prompt/context token length | frozen lane prompt builder |

Freeze procedure: one read-only driver over the exact-commit checkouts produces
`FM70_PRE_OUTCOME_FEATURES_V1.json` (dev 40 + candidate held-out pool in one pass),
sha256 committed **before** any selector is fit. Any feature added later is a new design
version, not an edit.

## 5. Held-out fold construction (deterministic, frozen now)

- **Rule:** per project, the next numeric bug ids after the dev-fold ids, under the same
  E30 selection policy (`lexicographically_first_existing_numeric_bug_ids` at commit
  `11c5f1e`). Dev used ids 1..5 (ansible 1..6, cookiecutter 1..4); held-out takes the
  following ids in ascending order.
- **Primary size:** 5 per project (mirror of dev; ~38-40 tasks). **Extended pool:**
  up to 8 per project where the benchmark has them, ranked, for use only if Gate 2
  power analysis demands more.
- **Arms on held-out:** SIMPLE_DIRECT, F0_PARENT_FEDERATION, F2_ORION_METABOLIC_FULL
  (3 arms x 3 repetitions), plus the frozen selector applied per task. The selector is
  a *routing rule over the three always-arms*, not a fourth solver.

## 6. Gates

- **Gate 0 — dev-fold diagnosability (cheap, no model spend).** Leave-one-project-out
  cross-validated selector on frozen features vs the always-best-arm (SIMPLE_DIRECT),
  judged against a label-permutation null (>=1000 permutations, shuffle-equal-n).
  Pre-registered primary selector: multinomial logistic regression on P01-P07 with
  Laplace-smoothed per-project empirical best-arm fallback for unseen projects.
  Pass = CV selector successes exceed always-best by >= 2 tasks AND permutation
  one-sided p < 0.05. Fail = lane terminal
  `INSUFFICIENT_ROUTING_SIGNAL_ON_DEVELOPMENT_FOLD`, no held-out dispatch.
- **Gate 1 — freeze.** Features hash + selector hyperparameters + held-out id list
  committed in one receipt before the first held-out response exists.
- **Gate 2 — held-out terminal (the lane's rule).** Selector vs each always-arm:
  exact discordant test, Holm family 3, one-sided; resource non-inferiority (mean
  wall time within 1.15x of the routed arm's always-arm mean); **simple-task guard:**
  on the pre-frozen feature-defined simple stratum (below dev-median P02xP05
  complexity), selector majority successes must be >= always-SIMPLE's.

## 7. Boundary inheritance (binding)

FM70 inherits E30 R11 receipt section 5 in full: the registered-failing-test lane does
not run full regression suites, so **no critical-failure, safety or non-inferiority
endpoint claims** may be made from FM70 outcomes. Routing claims are success-resource
claims only.

## 8. Terminal vocabulary

`SELECTOR_PROMOTED` (Gate 2 all pass) / `SELECTOR_FAILED_TERMINAL_RULE` (held-out run,
rule not met) / `INSUFFICIENT_ROUTING_SIGNAL_ON_DEVELOPMENT_FOLD` (Gate 0 fail, cheap)
/ `EXECUTION_DEFECT_<id>` (infrastructure). Each terminates the lane honestly; none is
a paper promotion by itself.

skills-applied: none (prospective design receipt, no manuscript content)

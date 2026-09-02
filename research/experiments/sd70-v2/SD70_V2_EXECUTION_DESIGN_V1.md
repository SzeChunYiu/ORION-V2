# SD70-V2 — Synthetic Recursive Meta-Policy Study: Frozen Execution Design (V1)

**Protocol served:** `research/experiments/SCIENTIFIC_DEVELOPMENT_SD70_PROSPECTIVE_PROTOCOL_V2.json`
(`ORION-SD70-SYNTHETIC-META-POLICY-V2`, issue #50).
**Predecessor:** SD70 V1 stopped pre-outcome (`research/experiments/results/issue50/sd70/`,
terminal `REQUIRES_NEW_PROSPECTIVE_VERSION`). No V1 prepared input, seed or response is reused.
**Companion files:** `SD70_V2_EXECUTION_DESIGN_V1.json` (every constant below; its sha256 is bound
into every frozen suite), `SD70_V2_PARENT_FIDELITY_RECEIPT_V1.md` (code hashes, native parent
tests, development split), `results/SD70_V2_DEVELOPMENT_RESULTS_V1.json`.
**Status at freeze:** no protected task generated, no protected outcome inspected. The protected
seed exists only at `~/.orion-custody/sd70-v2/SD70_V2_MASTER_SEED.txt` (Mac, mode 600); its
sha256 is published in the JSON and `prepare` refuses any other seed.

## 1. Question, null, expectation

**Q.** On fresh synthetic hidden-policy episodes, does a recursive meta-discovery arm improve
exact held-out action selection over the strongest faithful mature rule-induction parent under
matched public information and prospectively fixed resource limits?

**H0 (parent sufficiency).** The strongest generator-faithful parent makes the same or better
held-out decisions at lower cost. **Pre-registered expectation:** `PARENT_SUFFICIENT`, a
successful terminal. The generator family is a linear multiclass argmax; the max-margin parent's
hypothesis class contains it.

**Scope.** Supports, if valid, synthetic rule-induction mechanism evidence inside the frozen
generator family. Does not support naturalistic scientific-development superiority,
science-of-science superiority, a Machine Epistemics field residual, causal law, or publication
readiness.

## 2. Generator (V1-identical family)

`sd70v2_generator.build_suite` reproduces the V1 family byte-for-byte on the public side (unit
test): 4–7 binary context features, 3–5 actions, integer weights in [−3, 4] with distinct rows,
argmax with lowest-index tie break, 8 unseen training contexts each yielding one SUCCESS (best
action) and one FAILURE (uniformly random other action), one unseen held-out context, random
codeword tokens. V2 adds to the **private** file the worst-action set and latent query scores
(for the critical-false-direction outcome). Nothing private reaches any arm.

Because every FAILURE is paired with a SUCCESS on the same context, failure evidence adds
strictness only; the no-failure-evidence ablation is therefore expected to cost the parents
nothing and is informative only about the model arms.

## 3. Arms and information surfaces

| arm | kind | surface | tasks |
|---|---|---|---|
| TARGET_ONLY_DETERMINISTIC | deterministic | TARGET_ONLY | all |
| TARGET_ONLY_NEGATIVE_CONTROL | model | TARGET_ONLY (physically no `training_episodes` key) | 60 |
| SIMPLE_FREQUENCY_PARENT, MATCHED_CASE_PARENT, NAIVE_BAYES_PARENT, DECISION_LIST_PARENT, PERCEPTRON_PARENT, MAXMARGIN_PARENT, PAIRWISE_LINEAR_PARENT | deterministic | COMMON | all |
| STRONGEST_GENERATOR_FAITHFUL_PARENT | alias of the development-selected parent (**MAXMARGIN_PARENT**) | COMMON | all |
| FIXED_META_LESSON | deterministic fixed heuristic | COMMON | all |
| F0_PARENT_FEDERATION | deterministic plurality of the seven parents; strongest breaks ties | COMMON | all |
| F2_STATIC_NO_RECURSION | model, recursion disabled | COMMON + parent advisory | all |
| F2_RECURSIVE_META_DISCOVERY_FULL | model, full registered procedure | COMMON + parent advisory | all |
| F2_FULL_MINUS_FAILURE_EVIDENCE | model ablation | COMMON with FAILURE episodes removed + advisory on that surface | all |
| F2_FULL_MINUS_PARENT_FEDERATION | model ablation | COMMON (no advisory) | all |
| `<deterministic arm>__LP`, `__QS` | deterministic on control pools | as the arm | all |
| F2_RECURSIVE_META_DISCOVERY_FULL__LP, `__QS` | model on control pools | COMMON + advisory | 60 |

Surfaces are defined in `sd70v2_generator.surface_for`; a request holds only its surface keys.
The parent advisory is computed from the arm's own surface (so the success-only arm's advisory
never sees failures). `REQUEST_SURFACE_MANIFEST.json` records the sha256 of every request, an
arm-surface hash, the surface keys per arm, and the count of training-only tokens found in any
TARGET_ONLY request (must be 0).

Physical enforcement during dispatch (`sd70v2_run.stage_dispatch`): the private oracle is
deleted before any child runs and restored hash-exactly afterwards; `public_tasks.json` and the
whole `requests/` tree are set to mode 000 for the duration of model dispatch; every model child
runs in an empty temporary directory with a private copy of its own request only; the prompt is
built solely from the surface; command executions seen in the Codex event stream are counted.

## 4. Parents (all deterministic, stdlib, frozen hyper-parameters, no tuning on any task)

Frozen tie break everywhere: highest score, then candidate-list order (the generator's own
lowest-index rule, public through the candidate list).

- **SIMPLE_FREQUENCY_PARENT** — global success − failure count per action.
- **MATCHED_CASE_PARENT** — kernel vote, weight 1/(1 + Hamming distance), ± by outcome.
- **NAIVE_BAYES_PARENT** — naive-Bayes log odds success-vs-failure action for the context, Laplace(1).
- **DECISION_LIST_PARENT** — Rivest decision list, sequential covering over ≤ 2-literal conjunctions, failures as negatives, frequency default.
- **PERCEPTRON_PARENT** — averaged Kesler multiclass perceptron, margin 1, 50 epochs, bias.
- **MAXMARGIN_PARENT** — Crammer–Singer hinge + L2 (λ = 0.01), full-batch subgradient, step 0.1 × 200, bias; failures add a pairwise hinge against the paired success action.
- **PAIRWISE_LINEAR_PARENT** — averaged binary perceptron per pair, one vote per pair (documented boundary: vote cycles).
- **FIXED_META_LESSON** — additive per-feature (success − failure)/support evidence over the held-out features.
- **F0_PARENT_FEDERATION** — plurality over the seven parents; ties → strongest parent.

**Selection rule (frozen):** highest mean development exact accuracy among the generator-faithful
candidates {PERCEPTRON, MAXMARGIN, PAIRWISE_LINEAR, DECISION_LIST, NAIVE_BAYES}; tie → lower wall
time. Development split: 3 seeds (`sha256("SD70-V2-DEV|k")`) × 200 tasks. Result: MAXMARGIN
0.720 > PERCEPTRON 0.698 > PAIRWISE 0.687 > DECISION_LIST 0.653 > NAIVE_BAYES 0.645 (chance 0.262).
F0 federation reached 0.708 on development, below the strongest member; the comparator is the
strongest parent as the protocol prescribes, and F0 is reported as a required arm.

## 5. Model arms

Codex CLI `exec --ephemeral --ignore-user-config --ignore-rules --skip-git-repo-check --sandbox read-only -C <empty tmp> --json --output-schema`,
model `gpt-5.6-terra` (probe replied `OK` on 2026-09-02), `model_reasoning_effort = medium`,
timeout 600 s, one call per arm-task, at most one bounded rerun (`--retry-failed`, max 2 attempts),
concurrency ≤ 2. Identical settings for every model arm. Procedures are the texts in
`sd70v2_model_arm.ARM_PROCEDURES`; the full arm is instructed to induce → abstract → recursively
re-induce over its own policy → decide, the static arm to induce once and decide. Both may read the
parent advisory as evidence, never as authority.

## 6. Controls

- **Label permutation (LP):** a uniformly random bijection of the candidate actions applied to
  every training `chosen_action`. Every relabelling-equivariant learner then predicts π(g), so
  expected accuracy is exactly chance while all training statistics are preserved. Development:
  all parents 0.20–0.28 vs chance 0.262.
- **Query-to-task shuffle (QS):** the held-out context is replaced by another task's query bits
  (positional map) and the answer is that task's rule mapped positionally into this task's
  candidates; the answer is independent of this task's training. Development: parents 0.25–0.26.
- **No failure evidence, no parent federation, no recursion:** the three F2 ablation arms.
- **Physically sanitized target-only:** model and deterministic.
- Model controls run on the 60 lexicographically first task ids of their pool (frozen).

## 7. Outcomes (frozen estimands)

1. **Protected decision quality.** Exact-action correctness; Wilson 95% per arm; the primary
   estimand is the paired difference Δ = acc(F2_FULL) − acc(SP) with a 10 000-draw percentile
   bootstrap (seed 20260902) and an exact one-sided McNemar mid-p; Holm over the two primary
   contrasts {F2_FULL vs SP, F2_STATIC vs SP} at family α = 0.05.
2. **Critical false direction.** Selecting a worst action (minimal latent score for the held-out
   context) — identifiable from the private weights. Rate per arm; paired Δ vs SP.
3. **Resource cost.** Per arm: model calls, attempts, retries, input/output/total tokens, tool
   calls, wall time; aggregation = sum over arm-tasks including failed attempts; mean = sum / n.
4. **Parent non-regression.** Lower 95% bootstrap bound of Δ > −0.05.

## 8. Power → task count

Connor (1987) paired-binary approximation: δ_min = 0.10, assumed discordance 0.30 (development
discordance between the top two parents is 0.118; 0.30 is deliberately conservative for a model
arm), α = 0.025 one-sided (Holm worst case), power 0.80 → **234 tasks; frozen N = 240** (achieved
power 0.811 at 0.30, 0.748 at 0.35, 0.877 at 0.25). Model calls: 240 × 4 + 3 × 60 = **1 140**.

## 9. Missingness

`VALID` / `ARM_FAILURE` (model failure, timeout, out-of-candidate selection → scored incorrect,
counted as a failure) / `INTEGRITY_VIOLATION` (missing, unreadable, identity mismatch →
evaluation refuses). Global model failure rate > 0.05 → `CANNOT_CHECK`; F2_FULL, F2_STATIC or
TARGET_ONLY model arm failure rate > 0.10 → `CANNOT_CHECK`. The parent's own LP control must sit
at chance or the evaluator is declared invalid (`CANNOT_CHECK`). No silent replacement.

## 10. Decision rules (evaluated in this order)

1. **CANNOT_CHECK** — dispatch integrity, missingness, identity, design-hash or evaluator-validity failure.
2. **PARENT_SUFFICIENT** — SP ties or exceeds F2_FULL (Δ ≤ 0), or F2_FULL fails any gate:
   Δ ≥ 0.10; Holm-significant; non-regression (CI low > −0.05); CFD Δ ≤ 0.05; cost within budget;
   mechanism (F2_FULL − F2_STATIC ≥ 0.05 with mid-p < 0.05); no ablation beats the full arm by
   more than 0.03; model negative controls behave (Wilson 95% lower bound ≤ chance + 0.05, i.e. not
   significantly above chance; the 0.05 absorbs the shared low-index tie-break bias).
3. **FIXED_META_LESSON_SUFFICIENT** — F2_FULL passes every gate but FIXED_META_LESSON ≥ F2_FULL.
4. **PROSPECTIVE_META_POLICY_RESIDUAL** — otherwise.

Unit tests plant each route: a federation-copying solver → PARENT_SUFFICIENT; a perfect solver
(answers supplied to the stub only, never to the runner) → RESIDUAL with every gate true; a
failing solver → CANNOT_CHECK; a wrong seed, a tampered design and a missing response are
refused.

## 11. Custody

Seed committed before generation (sha256 published; seed never in the repository); oracle absent
during all solver calls; raw responses frozen before restoration; evaluator separate from the
solver executable; no threshold or baseline changes after oracle access (the design hash is
bound into `FROZEN_SUITE.json` and re-checked by `evaluate`); code hashes in the fidelity receipt.

## 12. Authority

Grants nothing: no scientific truth, causal law, field status, submission or publication
readiness. `PARENT_SUFFICIENT` is a successful terminal.

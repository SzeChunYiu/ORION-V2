# Human Epistemics Known-Answer Benchmark V1

**Status:** transparent reference benchmark for issue #40. It tests whether the contracted K0–K6 interfaces can represent several human-inquiry failure distinctions without adding a new kernel family. It grants no empirical superiority, psychological fidelity, scientific truth, novelty or publication authority.

## Review cell

The benchmark was designed under six mutually checking roles:

1. **philosophy/history of inquiry** — rejects slogans and anachronistic translation;
2. **cognitive science/metacognition** — separates calibrated monitoring from repeated reflection;
3. **situated-practice reviewer** — tests instruction versus demonstrated competence;
4. **evidence/social epistemology reviewer** — tests dependence and criticism uptake;
5. **formal/control reviewer** — requires explicit statuses and fail-closed transitions;
6. **hostile editor** — rejects any test that merely restates an implementation choice or self-authorizes a scientific result.

## Benchmark families

### HE-1 — Self-model calibration under dependence

**Question:** can the system distinguish a calibrated inquiry self-model from self-confirming confidence?

Known-answer cases include:

- independent/known-answer outcomes;
- an apparently independent outcome sharing the predictor's model/data dependency;
- confident but systematically wrong predictions;
- too few independent outcomes to estimate calibration.

Required terminals:

- `CALIBRATED_ON_BOUND_SET`;
- `MISCALIBRATED_ON_BOUND_SET`;
- `INSUFFICIENT_INDEPENDENT_CASES`;
- `CANNOT_CHECK`.

No calibration outcome grants evidence or scientific authority.

### HE-2 — Meta-action selection without self-authentication

**Question:** can a self-model help allocate effort while remaining subordinate to external evidence obligations?

Known-answer cases include:

- high confidence with an explicit external-review obligation;
- representation-insufficiency witness;
- positive value of more computation;
- uncalibrated self-model with no external checker;
- calibrated high-confidence provisional continuation.

Expected actions:

- `EXTERNAL_REVIEW`;
- `CHANGE_REPRESENTATION`;
- `MORE_COMPUTE`;
- `CANNOT_CHECK`;
- `PROCEED_PROVISIONALLY`.

A meta-action may select the next operation; it may not discharge the underlying evidence or authority obligation.

### HE-3 — Failure log versus transferable lesson

**Question:** when does a failure record support a scoped future correction?

Known-answer cases include:

- failure not reproduced;
- attribution unresolved/contradicted;
- correction not regression-tested;
- target inside explicit transfer scope;
- target outside scope;
- explicit counterexample or changed causal condition.

Expected terminals:

- `APPLY_WITHIN_SCOPE`;
- `REVALIDATE_BEFORE_USE`;
- `REJECT_TRANSFER`;
- `CANNOT_CHECK`.

### HE-4 — Surprise versus useful serendipity candidate

**Question:** can an off-path event be retained without becoming evidence or agenda authority?

Known-answer cases include:

- high stochastic surprise, high noise risk, no reproduction;
- reproducible high-relevance event with a discriminator within budget;
- relevant event without a discriminator;
- useful candidate beyond the declared follow-up budget;
- low-relevance event despite salience.

Expected terminals:

- `RETAIN_FOR_TEST`;
- `RETAIN_UNRESOLVED`;
- `IGNORE_AS_NOISE`;
- `OUT_OF_BUDGET`.

Every terminal keeps `claim_authorized=false` and `agenda_authorized=false`.

### HE-5 — Instruction identity versus competence transfer

**Question:** does identical text establish executable skill in a changed context?

Known-answer cases include:

- instruction identity only;
- target within demonstrated context and state-discriminator range;
- context relation certified but target outside demonstrated range;
- observed failure context;
- changed task family.

Expected terminals:

- `TEXT_ONLY_UNVERIFIED`;
- `VERIFIED_WITHIN_DEMONSTRATED_RANGE`;
- `REVALIDATE_CONTEXT_CHANGE`;
- `NOT_TRANSFERRED`;
- `CANNOT_CHECK`.

### HE-6 — Criticism independence and uptake

**Question:** can a review process distinguish independent criticism from dependent review and review theatre?

Known-answer cases include:

- critic and subject share a model/data dependency;
- independent critic changes the claim state;
- objection logged with no response or state change;
- criticism rejected through located known-answer evidence;
- reason for no change without sufficient evidence.

Expected coordinates:

- independence: `INDEPENDENT`, `DEPENDENT`, `UNKNOWN`;
- outcome: `UPTAKE`, `EVIDENCE_BASED_REJECTION`, `REVIEW_THEATRE`, `UNRESOLVED`.

The benchmark rejects reviewer-count voting as a substitute for argument and state consequences.

### HE-7 — Distributed state at the decision boundary

**Question:** is required scientific state actually available where the decision is made?

Known-answer cases include:

- all required state at the decision component;
- a calibration warning exists at an instrument but is lost at handoff;
- required state is absent from the entire episode;
- decision component itself is missing.

Expected terminals:

- `COMPLETE_AT_DECISION`;
- `HANDOFF_LOSS`;
- `SOURCE_STATE_MISSING`;
- `CANNOT_CHECK`.

## Non-claims

The benchmark does not establish:

- a human-like mind, consciousness or general metacognition;
- that Brier score is a universal self-model metric;
- a universal failure-cause taxonomy;
- a universal model of tacit knowledge or serendipity;
- empirical benefit on scientific tasks;
- field separation for Machine Epistemics.

It is a transparent executable specification whose value is to expose category errors and fail-open semantics before protected studies.

## Protected-study transition

The next scientific step is not to add more authored cases indefinitely. It is to freeze matched parent baselines and evaluate these distinctions on:

- held-out scientific-agent episodes;
- changed material/tool procedural tasks;
- independent versus same-model review panels;
- delayed outcomes for self-model calibration;
- prospective unexpected-event/opportunity cases;
- real distributed human–tool–model workflows.

## Current terminal

```text
REFERENCE_BENCHMARK_FAMILIES = 7
KNOWN_ANSWER_TESTS = 22_GREEN_LOCAL
NEW_KERNEL_FAMILY = NOT_REQUIRED_BY_REFERENCE_CASES
PROTECTED_EXTERNAL_VALUE = CANNOT_CHECK
SCIENTIFIC_AUTHORITY = NONE
NOVELTY_AUTHORITY = NONE
```

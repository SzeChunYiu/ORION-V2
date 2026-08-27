# Computational Scientific Control — Basic Knowledge V0

**Status:** teaching/research seed only. Terms are working definitions; none claims disciplinary priority.

This file is the smallest coherent body of knowledge needed to teach, test, or implement the provisional field hypothesis in `COMPUTATIONAL_SCIENTIFIC_CONTROL_FIELD_SYNTHESIS_V0.md`.

## 1. Fundamental object

A **scientific control system** is a human, machine, or hybrid system that repeatedly changes a scientific state by taking actions, receiving observations, and applying explicit rules for evidence, validity, preservation, authority, and stopping.

The system's goal is not merely to emit a correct-looking answer. It is to reach a **warranted terminal state** under a declared problem contract.

## 2. Scientific state

A minimal state should keep distinct:

- **problem contract** — question, scope, criterion, decision/publication target;
- **claims** — supported, refuted, open, blocked, or unresolved propositions;
- **hypotheses/alternatives** — mutually exclusive or overlapping possibilities;
- **uncertainty** — quantitative or qualitative uncertainty that has not been collapsed into truth labels;
- **evidence** — observations or derivations admitted under a contract;
- **provenance** — where artifacts/evidence came from and how they were transformed;
- **dependence** — which evidence shares data, models, instruments, prompts, authors, assumptions, or transformations;
- **search universe** — routes/sources/representations considered, open, stopped, or censored;
- **representation/method state** — current language/model/method and its declared limits;
- **obligations** — required checks that remain active;
- **authority** — what actions/claims may be adopted and by whom;
- **resources** — time, compute, tools, providers, samples, experimental capacity;
- **history** — append-only transition and receipt sequence.

A state representation that omits one of these may still be adequate for a narrower problem. CSC asks which coordinates are required for which downstream decisions.

## 3. Scientific actions

Common action classes:

- frame/decompose;
- retrieve/search;
- extract/absorb;
- reconstruct/model;
- detect contradiction/gap/coverage/failure;
- diagnose responsibility;
- design a discriminating experiment/probe;
- execute an experiment, computation, proof, or tool call;
- reframe representation/decomposition/search/method/objective;
- reopen claims invalidated by changes;
- compare/benchmark/review;
- transport knowledge across context/version/representation;
- escalate the action space when the current one is insufficient;
- stop with a typed terminal.

An action is **admissible** only if its preconditions and authority requirements are satisfied.

## 4. Observations, evidence and receipts

### Observation

A raw result from the world, a model, an instrument, a database, a proof/checker, or a human process.

### Evidence

An observation that has been admitted to support/refute a claim under a declared semantic and validity contract.

### Receipt

A content-bound record of what was requested, what was executed, what returned, and under which identity/resources/criterion.

**Key law:** a valid receipt proves replay/integrity facts about the process; it does not automatically prove the scientific claim is correct.

## 5. Scientific terminals

Useful terminal vocabulary is typed rather than binary:

- `SUPPORTED` / `VERIFIED` — declared criterion satisfied under valid evidence;
- `REFUTED` — declared criterion falsified;
- `BLOCKED` — progress prevented by a named resource/authority/method condition;
- `CANNOT_CHECK` — required identity/evidence/relation/evaluator condition cannot be established;
- `INCOMPARABLE` — objects cannot validly be compared under the current context;
- `SATURATED_BOUNDED` — no material change after a declared complete bounded basis and omission challenge;
- `EXECUTION_FAILED` — host/tool/process failure, explicitly not a scientific negative by default.

A downstream application may use different names, but collapsing these distinctions can produce false scientific completion.

## 6. Evidence dependence

Evidence items are not independent just because they have different filenames or textual forms.

Dependence can arise through:

- shared raw data;
- shared preprocessing;
- same model or checkpoint;
- same retrieval corpus;
- same instrument/calibration;
- same evaluator or rubric;
- common literature source;
- copied or transformed claims;
- hidden common assumptions.

### Support-family model

Represent a claim's support as one or more **complete support families**. A claim survives a premise revocation only if at least one complete independent-enough support family remains valid.

This supports selective rather than global reopening.

## 7. Selective reopening

When a premise, mapping, criterion, calibration, or authority root changes:

1. identify directly affected commitments;
2. traverse declared dependency/support relations;
3. preserve any commitment with a valid independent alternative support family;
4. reopen only those with no surviving complete support;
5. record the change and reopen receipt.

A system that never reopens becomes stale. A system that reopens everything destroys useful knowledge and wastes resources.

## 8. Scientific relations are context-relative

Two scientific objects may be:

- identical by content;
- equivalent for a declared judgment;
- behaviorally equivalent;
- observationally equivalent;
- decision-equivalent;
- approximately transportable;
- linked by calibration/anchors;
- structurally analogous;
- incomparable.

No single generic “similarity” relation safely substitutes for all of these.

A relation claim should bind at least:

`(left, right, context, relation_type, witness, loss/uncertainty, counter_probe, validity_window, status)`.

## 9. Contract and criterion binding

A scientific comparison is meaningful only when its success criterion is stable or its change is explicitly disclosed.

### Criterion-churn hazard

If a system evaluates itself under a changed easier criterion, it can manufacture apparent progress.

### Safe rule

- bind the frozen criterion digest;
- bind the applied criterion digest;
- if changed, record what/why;
- record the counterfactual verdict under the frozen criterion where required;
- for a loosened criterion that turns a failure into a pass, require an exhibited rejection or equivalent discriminator showing the new rule still has falsifying force.

## 10. Censoring and search coverage

“No result was found” is ambiguous.

Possible causes:

- the route was searched and yielded no qualifying result;
- retrieval failed;
- budget ended;
- source unavailable;
- query vocabulary was wrong;
- the route was never attempted.

Only the first supports evidence of absence, and even then only under the declared search basis.

Search state should explicitly distinguish `COMPLETE`, `STOPPED_LOCAL`, `CENSORED`, `FAILED`, and `UNSEARCHED` routes.

## 11. Diagnosis and discriminating experiments

A failed scientific attempt does not uniquely identify its cause.

Potential responsibilities include:

- missing evidence;
- wrong representation;
- insufficient model/method capacity;
- search-universe omission;
- invalid assumption;
- resource limit;
- evaluator defect;
- execution/infrastructure failure;
- interaction of multiple causes.

When several causes are consistent with current evidence, the correct next step may be a **discriminating experiment** rather than immediate repair.

A good discriminator maximizes expected separation of surviving hypotheses under cost and risk constraints.

## 12. Escalation / Jump

A **Jump** changes the scientific search/control space itself: a new representation, model family, method, decomposition, objective, instrument, or other higher-level intervention.

A Jump should require:

- evidence that lower-level actions are insufficient or dominated;
- a ceiling/obstruction witness when available;
- the lowest sufficient proposed escalation;
- preservation/transport obligations for prior commitments;
- an explicit affected-commitment set;
- counterfactual controls where no Jump is necessary.

### Two errors

- **false Jump:** higher-level change when a lower-level repair was sufficient;
- **missed Jump:** repeated local work after the current action space is genuinely insufficient.

## 13. Bounded saturation

Saturation is not “the model stopped generating new things.”

A bounded saturation claim should specify:

- frozen search/representation basis;
- route coverage;
- residual/open obligations;
- censored routes;
- growth coordinates measured;
- at least one omission/counter-vocabulary challenge;
- required count of complete no-material-change passes.

Resource exhaustion is not saturation.

## 14. Authority

Scientific support and authority are separate coordinates.

Examples of authority domains:

- may record a candidate;
- may accept a claim internally;
- may trigger an experiment;
- may modify protected state;
- may adopt a method globally;
- may publish a scientific claim;
- may make a high-impact external decision.

A model/tool/reviewer can provide evidence without possessing authority to promote its own result.

**Non-amplification rule:** no derived certificate may authorize more than the weakest valid root/support path permits.

## 15. Replay identity

A scientific episode is the “same run” only if the identity-relevant coordinates match, including as applicable:

- problem/case;
- subject version;
- source corpus/provider/tool;
- configuration;
- criterion/evaluator;
- random seed;
- resource budget;
- protected data;
- authority permissions.

Changing one after output access creates a new run identity for protected evaluation.

## 16. Minimal mathematical notation

Let scientific state be `s_t ∈ S`, admissible actions `a_t ∈ A(s_t)`, observations `x_t ~ W(· | s_t, a_t)`, and transition interpreter `T`.

Ordinary control would optimize a utility over trajectories. CSC adds hard predicates:

- `ValidTransition(s_t, a_t, x_t)`;
- `EvidenceBound(x_t)`;
- `AuthorityAllowed(a_t)`;
- `PreservesOrReopens(s_t, s_{t+1})`;
- `CriterionStable(run)`;
- `ReplayIdentified(run)`.

Then a candidate policy `π` is scientifically admissible only if hard predicates hold. Secondary utility (speed, cost, reach) is optimized **inside** that feasible region, not traded against correctness/authority violations.

This motivates a non-compensatory evaluation structure.

## 17. Three basic theorems/conjectures to pursue

### K1 — Provenance insufficiency theorem (conceptual)

Content-perfect provenance alone cannot establish scientific correctness because two executions with identical lineage integrity can implement different or invalid scientific semantics.

Research task: formalize classes of provenance-equivalent but scientifically non-equivalent executions.

### K2 — Selective-reopen minimality theorem

Under an explicit support-family hypergraph, reopening precisely the claims lacking a surviving complete support family is minimal among sound reopen policies.

Research task: state conditions, mechanize proof, characterize approximate/dependent support variants.

### K3 — Bounded-stop non-equivalence theorem

Flat measured growth over a subset of search routes does not imply bounded saturation when an unsearched/censored route can contain a material result.

Research task: derive stopping bounds under route priors, censoring, vocabulary perturbation, and finite budgets.

## 18. Engineering checklist

Before calling a scientific controller reliable, ask:

- Is the problem/criterion frozen and inspectable?
- Can source/evidence identity be replayed?
- Are unknown, false, blocked and execution-failed distinct?
- Can hidden dependence be represented?
- Can a changed premise trigger selective reopening?
- Can the system refuse authority it does not possess?
- Are censored routes visible?
- Is escalation justified against lower-level controls?
- Can evaluation be frozen before outcome access?
- Does stopping state the bounded basis?
- Can a simpler parent-composed system beat it fairly?

## 19. What counts as progress in CSC?

Strong progress:

- a theorem about controlled scientific transitions;
- a benchmark exposing a failure invisible to task-accuracy metrics;
- a parent-composed baseline that falsifies an unnecessary CSC mechanism;
- a controller that reduces false completion at matched scientific reach/cost;
- a new diagnostic experiment that makes a previously non-identifiable failure identifiable;
- a selective-reopen algorithm with formal/empirical guarantees;
- a protected cross-domain result demonstrating justified reach without authority/integrity regression.

Weak progress:

- adding another agent role;
- adding another workflow state without a falsifier;
- renaming existing control/provenance concepts;
- improving average benchmark score while hiding a critical failed cell;
- producing more papers or hypotheses without cheaper/stronger verification.

## 20. Current knowledge boundary

This seed is sufficient to define a coherent research/teaching object, but not to establish a new scientific subject. The decisive next evidence is:

1. protected V1/V2 parity/non-regression;
2. strongest parent-composed comparisons;
3. independent review of the field boundary;
4. cross-domain CSC benchmark construction that is not ORION-specific;
5. at least one prospective fresh-domain episode;
6. formal results for selective reopening, stopping, relation transport, or escalation.

Until then, the correct terminal remains `FIELD_HYPOTHESIS_WORTH_PROTECTED_TESTING`.

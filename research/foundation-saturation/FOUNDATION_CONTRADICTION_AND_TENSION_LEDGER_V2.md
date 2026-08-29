# Foundation Contradiction and Tension Ledger V2

**Canonical owner:** issue #41  
**Pass-H owner:** issue #42  
**Pass-I owner:** issue #44

**Status:** cumulative contradiction ledger. It inherits T1–T14 from V1 and adds Pass-I tensions T15–T20. None is resolved by compromise language, averaging or majority vote. Reconciliation requires a context distinction, formal relation, protected intervention, authority boundary or explicit unresolved state.

## Inherited tensions T1–T14

1. hypothesis-led inquiry versus exploratory experimentation;
2. frozen criteria versus legitimate epistemic iteration;
3. universal schema versus epistemic cultures;
4. human-readable process versus machine-native computation;
5. exploration versus bounded closure;
6. internal coherence versus empirical support;
7. universal intelligence method versus inductive bias;
8. evidence versus values and authority;
9. exact replay versus robust replication;
10. theory priority versus apparatus-mediated phenomenon construction;
11. minimal kernel versus expressive coverage;
12. saturation as convergence versus saturation as self-confirmation;
13. evaluator identity versus evaluator sensitivity;
14. obligation control versus construction of new problem spaces.

The detailed inherited statements and candidate reconciliations remain in `FOUNDATION_CONTRADICTION_AND_TENSION_LEDGER_V1.md`.

---

## T15 — approximate computation versus exact-sounding scientific claim

### Position A

Scientific computation is often necessarily approximate. Finite precision, discretization and iterative stopping can be controlled well enough for useful scientific decisions.

### Position B

A reproducible or converged numerical output can still be inaccurate because the problem is ill-conditioned, the algorithm unstable, the arithmetic environment changed, the error bound inappropriate or the model scientifically inadequate.

### False resolutions

- reproducibility means numerical correctness;
- a small solver residual means small scientific error;
- higher precision automatically repairs model inadequacy;
- a mathematically validated enclosure proves the target claim about nature;
- all approximate results should be rejected.

### Candidate reconciliation

Bind the scientific claim to the mathematical problem, conditioning, algorithm, implementation/arithmetic, forward/backward/discretization error, validation/enclosure and model-adequacy status. Claim strength cannot exceed the weakest relevant link.

### Discriminating evidence

Known ill-conditioned problems, unstable/stable algorithm pairs, cross-precision and cross-implementation runs, validated enclosures, and cases where a numerically correct model is scientifically wrong.

### Current terminal

`CONTEXTUAL_RECONCILIATION_CANDIDATE__PROTECTED_TESTS_OPEN`.

---

## T16 — precise probability versus honest ignorance, conflict and model plurality

### Position A

A precise probability distribution supports coherent updating, expected utility and efficient quantitative decisions.

### Position B

Available evidence may warrant only a set of distributions, interval bounds, conflicting source assessments, structural alternatives or complete ignorance. Selecting one distribution can fabricate information.

### False resolutions

- ignorance is represented by a uniform prior without justification;
- every uncertainty should remain imprecise forever;
- credal width is a universal uncertainty score;
- conflicting evidence should be averaged into consensus;
- deep uncertainty removes the need for evidence or decisions.

### Candidate reconciliation

Declare the uncertainty form, semantics, conditioning and decision rule. Permit precise probability when calibrated and model-adequate; preserve imprecision/conflict when precision is not warranted; allow robust/conditional actions without promoting uncertainty to confidence.

### Discriminating evidence

Calibration/coverage studies, sensitivity across credible models, decisions that reverse within a credal set, genuine ignorance controls, and cases where imprecise methods create avoidable conservatism.

### Current terminal

`UNCERTAINTY_FORM_INTERFACE_CANDIDATE__NO_UNIVERSAL_SCALAR`.

---

## T17 — machine-actionable openness versus legitimate collective control

### Position A

Findable, accessible, interoperable and reusable research objects support transparency, reproducibility and discovery, including machine reuse.

### Position B

Data and knowledge can concern peoples, communities, lands or culturally governed practices whose legitimate control, collective benefit, consent and future-use conditions are not determined by technical accessibility.

### False resolutions

- accessible means authorized;
- scientific benefit overrides community authority;
- all restrictions are anti-scientific censorship;
- CARE metadata alone establishes respectful governance;
- no reuse is possible across communities.

### Candidate reconciliation

Separate FAIR properties from externally supplied CARE/custody/consent conditions. Machine-actionability describes technical affordance; legitimate reuse requires the relevant authority, permitted purpose, responsibility and monitoring.

### Discriminating evidence

Same dataset under different authorized uses, technically reusable but prohibited future use, community-governed access decisions, collective harm despite deidentification, and cases where responsible sharing produces benefit.

### Current terminal

`AUTHORITY_BOUNDARY_STRONG__COMMUNITY_SPECIFIC_IMPLEMENTATION_REQUIRED`.

---

## T18 — semantic interoperability versus local meaning

### Position A

Scientific automation requires mappings across schemas, ontologies and representations so machines can retrieve, compare and combine knowledge.

### Position B

Ontologies omit contextual assumptions; local practices assign different meanings, scales, constraints and authorities to apparently shared labels. Interoperability can erase precisely the distinctions that matter scientifically.

### False resolutions

- matching labels means matching meaning;
- a high ontology-matching score authorizes exact transport;
- every local meaning is incomparable;
- one universal ontology is required for coordination;
- translation loss can be ignored after successful query execution.

### Candidate reconciliation

Use boundary interfaces and semantic-context receipts: shared identity and registered invariants coexist with local projections, background-knowledge provenance, ambiguity and prohibited cross-projection inferences.

### Discriminating evidence

Same-word/different-decision cases, low-word/exact-query cases, hidden local constraints, background-knowledge changes, and native expert adjudication.

### Current terminal

`ABSORBED_IN_K2_BOUNDARY_INTERFACE__STRONG_PARENT_ADAPTER_REQUIRED`.

---

## T19 — inclusive participation versus competence and source-quality differentiation

### Position A

Inquiry can exclude affected knowers through credibility prejudice, inaccessible evidence routes or agenda/instrument choices. Participation can reveal observations, concepts and harms that dominant institutions omit.

### Position B

Evidence roles require competence, access, calibration and dependence assessment. Equal social standing does not make every empirical assertion equally reliable for every decision.

### False resolutions

- identity determines truth;
- expertise licenses exclusion from question-setting or interpretation authority;
- participation automatically creates independence or objectivity;
- formal equal weighting repairs epistemic injustice;
- community testimony can be used without consent or context.

### Candidate reconciliation

Separate standing, participation rights, source/evidence role, competence, dependence and authority. Exclusions require explicit claim-relevant reasons and an appeal/reopen route; inclusion does not bypass evidence evaluation.

### Discriminating evidence

Prejudice-controlled testimony studies, question-setting interventions, expert/nonexpert calibration, citizen-science quality protocols, community interpretation conflicts and cases where added participation increases noise or burden without decision value.

### Current terminal

`SOCIAL_EPISTEMOLOGY_AND_GOVERNANCE_PARENT__PROTECTED_PARTICIPATION_TESTS_OPEN`.

---

## T20 — benchmark equivalence versus deployment equivalence

### Position A

Frozen benchmarks and held-out performance provide reproducible comparison and protect against outcome-conditioned evaluation.

### Position B

A benchmark can be non-identifying: several systems score equally while behaving differently under deployment shifts, stress tests, numerical tolerances, data-generation changes or authority constraints. Weak baselines and selective reporting can inflate apparent progress.

### False resolutions

- equal score means scientifically equivalent;
- every benchmark difference predicts deployment value;
- deployment uncertainty makes benchmarking useless;
- a larger benchmark automatically solves underspecification;
- human or parent baselines may remain intentionally weak.

### Candidate reconciliation

Treat benchmark results as context-bound relations. Bind stress dimensions, data-generation provenance, leakage controls, parent baseline strength, numerical accuracy/cost and deployment strata. `EQUAL_ON_BENCHMARK` is not `EQUIVALENT_FOR_USE`.

### Discriminating evidence

Equally scoring model families with divergent stress behavior, leakage controls, strong numerical baselines, cross-domain deployment tests, resource curves and negative-result disclosure.

### Current terminal

`K6_AND_COMPONENT_VALUE_RECONCILIATION_CANDIDATE__NATURALISTIC_EVIDENCE_OPEN`.

---

## Cross-tension interactions

- T15 and T20 interact when an ML system appears faster only because numerical accuracy or baseline implementation is weaker.
- T16 and T20 interact when a benchmark reports precise confidence despite model-class underspecification.
- T17 and T19 interact when a technically available source is used while the represented community lacks question-setting or interpretation authority.
- T18 and T17 interact when semantic mappings enable reuse that is scientifically lossy or not authorized.
- T13, T15 and T20 interact when a frozen evaluator cannot detect numerical or deployment errors.
- T3, T18 and T19 interact when a universal schema determines which knowers and distinctions can enter the system.

## Resolution protocol

For every candidate foundation proposition:

1. identify which side(s) it preserves;
2. state the context or relation that reconciles the tension;
3. provide hostile cases where the reconciliation fails;
4. bind the mature parent method;
5. define the protected intervention;
6. allow `PLURAL_UNRESOLVED` or `CANNOT_CHECK`;
7. prohibit a universal law when the evidence supports only contextual activation.

## Current terminal

```text
TENSIONS_RECORDED = 20
TENSIONS_RESOLVED = 0
PASS_I_TENSIONS = T15_TO_T20
SYNTHESIS_BY_AVERAGING = FORBIDDEN
CONTEXTUAL_OR_FORMAL_RECONCILIATION = REQUIRED
POST_MATERIAL_CLEAN_PASSES = 0_OF_3
FOUNDATION_FREEZE = BLOCKED
```

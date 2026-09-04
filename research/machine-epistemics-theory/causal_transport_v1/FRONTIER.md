# Foundation integration and research frontier

## 1. Division of work

This package does not duplicate or overwrite #312/#313's typed-warrant/risk/graded-dynamics work or #314's finite read-only decision/query frontier. It supplies a causal/interventional and noisy-history layer. No other session's work is reported as completed by this session. The two foundation issues already claim the same `foundation_v1` directory; their coordination remains an explicit programme concern, not resolved by this package.

The broad foundation is **not closed** by a finite causal package. A scoped contribution can be complete at its own stated level while the surrounding programme remains open.

## 2. Five analytic roles and actual cross-checks

These are reasoning roles within one authoring session, not independent human experts, independent agents, or peer review. No additional worker was started.

| Role and background | Responsibility | Result carried into the package |
|---|---|---|
| Causal-inference specialist: structural models and identification | Define OBS/DO/CF and prevent cross-world conflation | CT-01–05; two nonidentification countermodels; factual-condition test correction |
| Probability specialist: coupling and decision bounds | Check quantifiers, constants, sharpness and selection effects | CT-07 common-mass improvement; CT-08 conditioning denominator; CT-10 abstention charge |
| Formal-methods specialist: typed semantics and model checking | Separate contradiction, undefined query and partial identification | CONFLICT versus CANNOT_CHECK; no dropping undefined compatible models; bounded exact checker |
| Systems specialist: immutable data, dependency identity and side effects | Bind complete model/query identities; distinguish physical effects from records | Tuple-copy immutability, CT-11/12, context/version absorption contract |
| Hostile-parent/evaluation specialist | Search for parent ownership and attacks against every promotion | P1–P6 record; CT-13 global-coupling counterexample; no all-size claim from enumeration |

Every theorem is checked against the assumptions in the others: CT-09 requires a joint law rather than CT-04's marginal law; CT-10 permits history dependence but requires the same policy and uniform conditional bounds; CT-13 warns against simultaneously optimal multi-model couplings without invalidating a two-process coupling. No consensus or role count confers authority.

## 3. OCM absorption contract (not yet adopted)

The OCM implementation owner should integrate only under its own checked successor PR. These are acceptance obligations, not claims that runtime support exists:

1. Preserve query kind in the type, identity and trace: observational conditioning, post-intervention conditioning and factual counterfactual conditioning cannot alias.
2. Bind the estimand, action values, measurement semantics, model family, population, policy, horizon, structural assumptions and evidence epochs. Keep the trusted evidence/adoption boundary external.
3. Report IDENTIFIED / PARTIAL / CONFLICT / CANNOT_CHECK separately. Empty model families and undefined conditioning events may never become a green answer. A class-relative result must name the class.
4. Treat exact population laws, finite observations, confidence regions and posterior beliefs as distinct evidence objects. One observed success cannot become an exact probability-one constraint.
5. On loss of an identifying assumption or receipt, expand/recompute compatibility. Preserve alternate evidence only through the existing provenance semantics; copies do not add independence.
6. A transported risk certificate needs actual, scope-valid bounds for distribution/mechanism drift and, for selected/counterfactual claims, the relevant joint-law coupling and conditioning mass. Risk-bounded actionability remains separate from individual truth and from pre-action authorization.
7. Log the action intent, authorization and actual effect separately. Revocation changes epistemic state; compensation changes the world. Never implement physical rollback as deleting the receipt.
8. Do not compose pairwise domain/counterfactual certificates into one global model without a compatible joint witness or a valid domain-specific parent theorem.
9. Replay the reference witnesses and error exits. Compare at equal information/resources with the native causal/transport parent; no additional oracle may be hidden in the checker.

Required absorption record: source theory SHA, per-claim statement digest, implementation SHA, parent comparator, parity commands/results, exact changed assumptions, resource accounting, adoption authority and reopen conditions. This package grants none of those downstream statuses automatically.

## 4. Precise successor questions

### F1 — Anytime causal risk certificates under adaptive experiment choice

**Target:** finite model family with bounded, history-dependent stochastic experiment kernels and external costs. Construct a time-uniform compatible-set process with declared coverage and a risk-bound theorem under adaptive stopping; distinguish estimation error, structural misspecification and authority. Compare confidence-sequence/sequential-testing/interactive-learning parents before proposing new operators.

**Decisive discriminator:** two histories with identical point estimate but different sampling policies must not receive the same unqualified certificate. Include always-abstain and exact native solver baselines, dependent samples, failed interventions and reused data. **Open:** a new theorem/residual; no anytime inference is implemented here.

### F2 — Least-cost certificate maintenance under causal-model revision

**Target:** given a family of query certificates and a declared change to an equation, population component, measurement, or assumption, characterize the smallest query set whose answers/guarantees must change, and the resources needed to certify the rest unchanged.

**Upper witness:** a causal dependency/certificate algorithm with proof of preservation. **Lower witness:** an information/query-cost bound against incremental causal-inference/provenance parent products. Compare data-structure locality to semantic locality; a small changed graph region can still have globally affected query results. **Open:** nontrivial cost frontier beyond the parents, not CT-06's set-inclusion fact.

### F3 — Robust multi-domain gluing under incomplete correspondence

**Target:** jointly compatible transported models when sources share uncertain dependence or only partial coordinate maps. Require a constructive joint witness or infeasibility certificate, plus an error bound for approximate marginal consistency.

**Controls:** CT-13 incompatible pairwise couplings; a globally feasible case; noisy marginals with an explicit tolerance; a missing-map CANNOT_CHECK. Strong parents: marginal/transport LPs, causal transportability, graphical models. **Open:** scalable solver and any residual over the strongest combination; no claim that pairwise matching suffices.

### F4 — Learnability and counterfactual memory

**Target:** under matched information, characterize the retained cross-world dependence needed for a declared later counterfactual query family after interventions and revocations. CT-04 establishes a separation in *available information*, not an OCM architecture advantage.

**Required comparison:** strongest response-function learner plus provenance/unlearning memory, and an equally provisioned recurrent model. Count observations, experiment channels, assumptions, memory, computation and verification. A fixed-current behavior match is not a matched counterfactual interface. **Open:** natural class, new lower/upper bound or parent-sufficiency terminal.

### F5 — Irreversible experimentation and compensation

**Target:** model epistemic value jointly with world-state change, reachability and reversibility. Derive a decision rule whose proposed experiments respect externally specified constraints, without self-issuing permission.

**Controls:** information-gaining but irreversible action; reversible action with unavailable compensation; pure read-only observation; evidence retraction after an actual action. Parents: constrained control/POMDPs, planning, experimental design and compensating transactions. **Open:** bounded control theorem and application bridge; do not treat the no-inverse lemma as an autonomous safety system.

## 5. Foundation-wide closure criteria

A future foundation integration release should bind all active components to one typed interface, preserve inherited parent-owned/negative terminals, resolve conflicting statuses at immutable refs, and verify theorem dependencies and resource models. It must explicitly separate:

- specification completeness in a bounded fragment;
- mathematical argument validity and independent checking;
- implementation refinement and machine calibration;
- empirical identification, calibration and generalization;
- architecture/resource advantage and prior-art residual;
- external adoption, independent field judgment and publication authority.

This package advances the causal/transport column. Typed statistical warrant, nogood algebra, general learning/procedure semantics, dynamic representation repair, real language, runtime concurrency/persistence, realistic causal evidence and independent review require their own returned artifacts. Negative/equivalence results are valid completed scientific results, not obligations to manufacture a positive.

## 6. Authoring failure and change ledger

**CT-TEST-001 — incorrect test expectation, retained.** The first 34-test run had 33 passes and one failure. The wrong-world-conditioning mutant test expected `P_D(Y_1=1 | Y=0)=1` in the randomized-treatment model. That expectation had silently omitted `X=0`. Correct marginal factual conditioning gives 1/2; with `X=0,Y=0`, it gives 1. The test expectation was corrected to 1/2; the core query evaluator was unchanged. The existing CT-04 test continues to check the fully conditioned 0-versus-1 witness. This is a disclosed test/assumption defect, not an empirical outcome repair or a counterexample to CT-04.

**CT-BOUND-002 — stronger valid bound during theory development.** Initial code used the valid additive transport envelope `min(1,epsilon+eta)`. The written coupling derivation yielded the tighter common-mass envelope and its sharp uniform corollary. The code was strengthened; both the inequality chain and sharp construction are tested. No protected outcome or original false statement was overwritten.

**CT-PARENT-003 — additional parent-derived global compatibility finding.** Reading P4 during the parent pass identified the simultaneous-coupling obstacle. CT-13 and three tests were added with explicit parent attribution. This is open theoretical development under #315, not a prospectively frozen confirmatory success.

**Environment limitation.** Direct git clone failed because this container cannot resolve github.com. Repository inspection and publication use the connected GitHub API. Local tests run in the analysis Linux container, never relabeled as the operator's laptop/Mac/LUNARC. Whole-repository CI and independent peer/proof review are not implied by local package tests.

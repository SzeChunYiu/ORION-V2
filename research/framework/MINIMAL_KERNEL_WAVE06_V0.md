# ORION-V2 Minimal Kernel Candidate — Wave 06

**Status:** convergence candidate; not final scientific architecture.

## Design principle

The kernel should contain only obligations that remain necessary when the best domain/native algorithm is swapped out. If an operation can be replaced by a mature parent implementation without changing ORION's scientific custody rules, that operation is an adapter responsibility, not a kernel primitive.

## K0 — Identity, contract and receipt boundary

Required objects:

- immutable object/run/epoch identifiers;
- `ProblemContract` / frontier contract;
- typed obligations and blockers;
- resource/capacity declarations;
- authority requirements;
- immutable step/evidence/execution receipts.

Invariant: an identifier that is declared but not compared against its expected identity does not constitute a binding gate.

## K1 — Plural scientific state

Required state families:

- source-bound observations/evidence;
- live hypotheses/models/designs/solutions;
- support, defeaters and unresolved alternatives;
- uncertainty and identifiability;
- history and negative knowledge;
- current representation/model/workflow epoch.

Invariant: lack of a unique winner must not be repaired by silently deleting alternatives.

## K2 — Relation and transport request/receipt

Required interface:

```text
RelationRequest = (
    source,
    target,
    context,
    registered queries,
    interventions/actions,
    decisions,
    tolerance,
    epoch,
    required relation family,
)
```

A parent implementation returns a typed receipt containing relation status, witnesses, counter-probes, loss/error bounds, assumptions and expiry conditions.

The kernel does **not** require one universal metric or embedding. Exact finite bisimulation, Blackwell comparison, rough indiscernibility, causal equivalence, stochastic total variation and other methods are adapters/reference baselines.

## K3 — Evidence, dependence, provenance and revalidation

Required interface:

- evidence unit identity and support role;
- dependence/common-cause links;
- component-level parentage;
- assumptions and native counterexamples;
- authority ceiling;
- affected commitment/reopen reach;
- transport/revalidation status.

Invariant: count of sources/agents/replications is never interpreted as independence without a dependence model or an explicit `CANNOT_CHECK`.

## K4 — Action, execution, diagnosis and recovery

Required interface:

- admissible action proposal;
- mandatory gate vector;
- scientific value / distinguishing power / cost / risk / option-value coordinates;
- execution binding and receipt;
- plural responsibility hypotheses;
- workflow/precedence constraints;
- retry, compensation, repair and selective reopen.

Invariant: hard scientific/authority/integrity gates are non-compensatory. A large score cannot purchase permission to violate them.

## K5 — Frontier and escalation

Required interface:

- research-opportunity proposal with falsifier and agenda-authority boundary;
- portfolio/Pareto relation;
- witnessed incumbent insufficiency;
- minimum sufficient escalation level;
- correspondence/preservation/reopen obligations for regime changes.

Invariant: poor score, timeout, novelty language or censored search alone cannot trigger a higher-level Jump.

## K6 — Evaluation, parity, saturation and authority

Required interface:

- V1 capability disposition and parity receipt;
- protected benchmark/evaluator identity;
- strongest donor-product comparison;
- coverage/saturation vector;
- failure/negative-result ledger linkage;
- adoption/publication authority state.

Invariant: passing a local test suite grants no scientific truth, novelty or publication authority.

## Explicit adapter families

The following are not kernel-owned unless later evidence shows the adapter boundary insufficient:

- search engines and retrievers;
- optimization/scheduling/queueing solvers;
- workflow engines;
- theorem provers/synthesizers;
- causal inference/discovery libraries;
- stochastic abstraction/control algorithms;
- statistical estimators and psychometric linkers;
- metrology/calibration packages;
- provenance graph storage;
- diagnosis/reliability engines;
- experiment-design algorithms;
- lab/instrument drivers;
- domain ontologies and domain simulators.

## Candidate de-duplication map

Current reference modules should converge toward these owners:

- `structural`, `comparability`, `generalization`, `generalization_compiler`, `correspondence`, `stochastic_transport`, `scale_gluing`, `information_order` -> **K2 relation/transport family**, with parent-specific adapters retained separately;
- `evidence`, `evidence_network`, `provenance`, `inheritance`, `reopening` -> **K3 evidence/provenance/revalidation family**;
- `policy`, `workflow`, `process_network`, `responsibility`, `probes`, `solver` -> **K4 solver/action/recovery family**;
- `opportunity`, `frontier_portfolio`, `jump` -> **K5 frontier/escalation family**;
- `evaluation`, `parity`, donor/saturation checks -> **K6 evaluation/parity family**.

This map is an API/concept contraction target, not an instruction to delete parent-specific reference implementations. Reference implementations remain valuable as known-answer baselines.

## Kernel-freeze questions

A coordinate or module survives the kernel only if at least one protected downstream decision changes when it is removed or merged. Otherwise it becomes:

- parent adapter;
- compatibility layer;
- reference baseline;
- research fixture;
- paper-specific method;
- deprecated duplicate.

## Candidate closeout terminal

`MINIMAL_KERNEL_FROZEN` is earned only after:

1. the V1 capability map has no orphan capability;
2. each kernel coordinate has a downstream sufficiency witness;
3. duplicate APIs are dispositioned;
4. strongest parent adapters are registered for non-kernel mechanics;
5. parity/simple-control tests show no material regression;
6. authority boundaries remain fail-closed.
# Business, Management, Operations and Engineering Donor Synthesis V1

**Status:** first native-problem reduction round; no claim of domain saturation.

## Why this lane is core

These disciplines are sciences of coordinated problem solving under requirements, resources, uncertainty, incentives, failure and lifecycle change. They are not merely application domains for ORION.

## Native problem families

### Systems engineering

**Canonical problem:** transform stakeholder needs into a system that is specified, architected, implemented, integrated, verified, validated, operated and retired under controlled change.

**Key objects:** needs, requirements, interfaces, architectures, configurations, risks, verification methods, validation evidence, lifecycle states and change requests.

**V2 pressure:** every output should trace to obligations; verification and validation remain distinct; framework changes need configuration/impact analysis.

### Business-process management and process mining

**Canonical problem:** model, enact, monitor, diagnose and improve workflows with concurrency, gateways, exceptions and conformance constraints.

**V2 pressure:** represent the solver as a typed partially ordered process/policy, not a fixed script. Logged execution enables conformance and bottleneck analysis.

### Operations research and operations management

**Canonical problem:** allocate scarce resources and schedule actions under objectives, constraints, uncertainty and service/risk trade-offs.

**V2 pressure:** search, experiment, proof, simulation, expert consultation and Jump compete under resource/option-value policies; one scalar objective may be inappropriate.

### Project/program/portfolio management

**Canonical problem:** coordinate interdependent work, decision gates, risks, dependencies and strategic value across initiatives.

**V2 pressure:** research branches need portfolios, kill/defer decisions, shared-resource accounting and evidence-bound gates.

### Quality management and statistical process control

**Canonical problem:** distinguish common-cause variation from assignable causes, stabilize processes and improve without tampering.

**V2 pressure:** repeated weak failures may indicate system variation rather than one responsible stage; repair must be monitored for regression.

### Organizational learning

**Canonical problem:** balance exploitation of routines with exploration while memory and incentives shape adaptation.

**V2 pressure:** Self-ORION/Jump must account for path dependence, local optima and future adaptability.

### Reliability and safety engineering

**Canonical problem:** identify hazards/failure modes, model propagation/common causes, provide containment and verify acceptable residual risk.

**V2 pressure:** responsibility may be multiple, distributed or interaction-only; validator redundancy needs common-cause analysis.

### Control and viability

**Canonical problem:** keep a system within constraints while reaching/stabilizing targets under uncertainty.

**V2 pressure:** generic reachability is parent-owned; hard viability constraints cannot be compensated by scientific value.

## Resulting solver changes

1. Replace stage ontology with state, obligations, transitions and partial-order execution.
2. Separate requirements, verification, validation, adoption and monitoring.
3. Add resource, scheduling, queueing and portfolio coordinates.
4. Permit concurrency only with interface, independence and safe-merge conditions.
5. Distinguish corrective action, process redesign, architecture change, strategy change and governance change.
6. Extend responsibility to serial, multiple, common-cause, distributed, interaction-only and unresolved cases.
7. Track option value and future adaptability.
8. Treat audit, internal control and change management as authority-bearing process objects.

## Implemented machine objects

`ProblemContract`, `ActionValue`, Pareto selection, `SolverState`, `StepReceipt`, J0–J8 `JumpLevel` and `CapabilityParityRecord`.

## Missing work

- partial-order workflow graph and conformance receipt;
- shared-resource scheduling state;
- requirements/interface/certificate change-impact graph;
- quantitative common-cause reliability model;
- portfolio admission/kill/defer object;
- verification-versus-validation receipts;
- human-factors and socio-technical authority model.

## Benchmark families

- serial earliest-upstream positive control;
- multi-fault single-attribution negative;
- safe parallel merge versus shared-resource race;
- verification PASS but validation FAIL;
- corrective action sufficient versus process redesign;
- high throughput violating hard authority;
- diversity/option value versus local score;
- common-cause validator failure.

## Current disposition

`BUSINESS_MANAGEMENT_ENGINEERING_ARE_CORE_PARENT_LAYERS__SOLVER_REFACTOR_REQUIRED__SATURATION_OPEN`

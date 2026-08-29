# Wave-02 Expert Panel and Decision Log V0

**Research object:** adapt and generalize domain theories for ORION-V2 without flattening their native scientific content.

## Panel

### E1 — Formal semantics and abstraction

Background: institution theory, theory morphisms, conservative extension, abstract interpretation, formal specification.

Assigned questions:

- What must a theory translation preserve?
- When is an abstraction exact, conservative, decision-relative, or merely sound?
- How can a counterexample survive transport?

### E2 — Operations, management, and process science

Background: workflow nets, operations management, stage-gate systems, queues, capacity, process mining, exception recovery.

Assigned questions:

- Which process concepts remain meaningful outside business operations?
- Which capacity, deadline, and role assumptions are industry-specific?
- How should reopening and compensation be represented?

### E3 — Systems, reliability, and diagnosis

Background: systems engineering, verification and validation, FMEA, fault trees, model-based diagnosis, common-cause and interaction failures.

Assigned questions:

- Can V1’s responsibility model represent multiple and interaction-only causes?
- What distinguishes diagnosis from blame or repair authority?
- Which tests discriminate causes rather than merely correlate with failure?

### E4 — Measurement, comparability, and causal transport

Background: metrology, psychometric equating and invariance, political ideal-point linking, causal transportability, semantic change.

Assigned questions:

- What must be anchored across epochs?
- How should uncertainty and semantic loss compose?
- When must comparability be refused?

### E5 — Control, viability, and learning spaces

Background: viability theory, robust control, ecological constraints, prerequisite spaces, operations feasibility.

Assigned questions:

- Which states permit safe continuation?
- Which states permit reaching a target while remaining safe?
- When do existential and robust reachability differ?

### E6 — Scientific governance and adversarial evaluation

Background: evidence authority, publication claims, protected evaluation, provenance, benchmark leakage, donor reduction.

Assigned questions:

- Can transport increase authority?
- Can a mapping be changed after seeing protected outcomes?
- Does the strongest parent composition already own the candidate?

## Round 1 — What counts as a generalization?

### Formal-semantics finding

A shared vocabulary is insufficient. A valid generalization requires an explicit map and a preservation condition. The panel separated four grades:

1. exact interpretation;
2. conservative generalization;
3. decision-relative adaptation;
4. sound over-approximation.

Any record that does not declare the grade is ambiguous and fails closed.

### Native-domain veto

The first draft treated assumptions as free-form notes. The native-domain lead rejected this because assumptions are often the main scientific content of a theory. The accepted design requires a complete assumption ledger with a typed disposition and evidence for every non-preserved assumption.

### Governance veto

The first draft could have described a mapping as “validated” without distinguishing internal review from external authority. The panel added explicit authority ceilings and made every transport assessment non-authorizing.

## Round 2 — What should be generalized from process and management science?

### Operations finding

The reusable core is not “business workflow.” It is an obligation-transition system with prerequisites, productions, resources, evidence, authority, reopenings, and terminal obligations.

### Systems-engineering correction

Verification and validation cannot be merged into one generic review action. A native adapter must preserve whether a task checks conformance to a specification or fitness for intended use.

### Reliability correction

Exception paths are not necessarily ordinary forward transitions. Compensation, rollback, and reopening may revoke a previously fulfilled obligation while preserving the occurrence and failure history.

### Result

The **Generalized Obligation Process Network** was admitted as a reference candidate. Industry-specific capacity units, regulatory roles, legal deadlines, and instrument semantics remain native adapter data.

## Round 3 — How should responsibility be generalized?

### Diagnosis finding

Single-cause diagnosis is only one topology. The accepted family includes:

```text
SINGLE
SERIAL_UPSTREAM
MULTIPLE_INDEPENDENT
DISTRIBUTED
INTERACTION_ONLY
UNRESOLVED
```

### Atomic gap found

A minimality rule can incorrectly remove an interaction explanation when either component alone is smaller but does not predict the full observation. Minimality must be applied only among hypotheses that are already observation-consistent and under a declared preference order.

### Probe finding

When two minimal diagnoses predict the same current observations, the correct terminal is structural non-identifiability unless a registered probe separates them. Repeated observation of the same symptom does not increase identifiability.

### Result

The **Plural Responsibility Diagnosis System** was admitted as a reference candidate. Diagnosis grants neither blame nor repair authority.

## Round 4 — What is shared by metrology, psychometrics, politics, causal transport, and linguistics?

### Measurement finding

All five fields contain a correspondence problem, but their native anchors are different. The shared object therefore binds mappings and anchors abstractly while leaving anchor construction native.

### Comparability finding

Across a multi-generation chain:

- preserved invariants compose by intersection;
- violated invariants accumulate by union;
- unresolved invariants accumulate by union;
- uncertainty upper bounds accumulate conservatively;
- semantic losses accumulate;
- contexts and epochs must remain valid for every link.

### Political-methodology correction

A common numerical scale is not guaranteed by model identification alone. The generalized object must distinguish mathematical alignment from substantive interpretation.

### Linguistics correction

A semantically aligned embedding does not itself prove that a scientific distinction survived. Target decisions and invariant senses must be registered.

### Result

The **Calibrated Correspondence Chain** was admitted as a high-priority reference candidate.

## Round 5 — How should viability be adapted?

### Control finding

There are two materially different questions:

- does at least one possible successor remain safe?
- do all possible successors remain safe?

These yield existential and robust kernels and cannot share one untyped terminal.

### Scientific-governance correction

A high-reward action that leaves the protected safe set is not part of justified reachability, regardless of expected scientific value.

### Learning-space correction

Feasible knowledge states and prerequisite closure are a special case, but educational assumptions should not be inserted into the generic object.

### Result

The **Justified Viability System** was admitted as a reference candidate.

## Round 6 — Shared envelopes between remote domains

### Proposed claim

Two remote domains may occupy the same position in ORION space.

### Adversarial reformulation

The panel rejected unconditional “same position.” The accepted statement is:

> Two native theories may share a context-indexed generalized envelope when both transports are independently valid and share a registered generalized decision or behavior.

### Mandatory non-claim

A shared envelope does not establish:

- semantic identity;
- historical relation;
- causal equivalence;
- identical resource cost;
- identical authority;
- transferable success without target validation.

## Round 7 — Reference implementation review

### Bug found

The first process-network implementation allowed a task to fire repeatedly whenever its prerequisites remained satisfied. A review task could therefore consume the same resource repeatedly and manufacture false deadlocks.

### Fix

A process marking now records executed task identities. The current finite reference semantics treats tasks as one-shot occurrences. Recurrent procedures require explicit occurrence identities or a separate cyclic-process model.

### Why retained

This is not a cosmetic implementation note. It shows that generalized semantics must specify occurrence identity; otherwise a domain’s event model is silently changed.

## Round 8 — Paper and framework implications

### C11 disposition

A provisional C11 paper is warranted for protocol design, but parent-subsumption risk is high. It remains standalone only if the integrated receipt improves false-analogy rejection or useful target transfer over the strongest parent union.

### Framework implication

Domain theories should not be copied into the ORION core. The core should contain:

- transport and validation interfaces;
- generalized envelopes that have a downstream role;
- native adapters;
- explicit assumption, resource, authority, and epoch records;
- counterexample and reopening hooks.

### Negative conclusion

There should be no one universal “domain theory embedding” used as a substitute for preservation proofs.

## Current panel terminal

```text
NATIVE_RECONSTRUCTION = REQUIRED
GENERALIZATION = TRANSPORT_GRADED
TARGET_ADAPTATION = REVALIDATION_REQUIRED
SHARED_ENVELOPE = CONTEXT_RELATIVE_NONIDENTITY
PARENT_SUBSUMPTION = OPEN
AUTHORITY = NONE
```

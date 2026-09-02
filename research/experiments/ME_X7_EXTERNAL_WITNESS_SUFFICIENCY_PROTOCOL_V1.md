# ME-X7 — Claim-Sufficient External Witnesses V1

**State date:** 2026-09-01  
**Status:** prospective/unexecuted

## 1. Question

Can a machine use internal representations or search procedures that are not human-style reasoning traces while remaining scientifically accountable through compact **claim-sufficient external witnesses**—without losing validity and without imposing costs that erase any machine-native advantage?

The study does not ask whether opaque reasoning should be trusted. It asks what externally checkable information is sufficient for the specific scientific claim and transition.

## 2. Witness principle

A witness is scoped to a declared claim/transition and evaluator. It may contain, as required:

- exact input/problem/criterion identity;
- source/evidence/provenance identities;
- executable code/proof/certificate;
- measurement or experiment records;
- assumptions and parameter versions;
- preservation/correspondence evidence after representation change;
- support/reopening dependencies;
- evaluator identity and applicable failure class;
- unresolved limitations;
- authority ceiling.

A witness is non-authorizing: passing its checks does not create authority above the declared roots.

## 3. Arms

- `FULL_HUMAN_STYLE_TRACE` — maximal step-by-step explanatory trace where feasible;
- `CLAIM_SUFFICIENT_WITNESS` — structured minimal witness selected prospectively;
- `PROOF_OR_CERTIFICATE_PARENT` — domain-native proof/certificate/assurance artifact;
- `PROVENANCE_PLUS_OUTPUT`;
- `OPAQUE_OUTPUT_ONLY`;
- `B5_STRONGEST_FAITHFUL_AUDIT_PARENT`;
- optional `MACHINE_NATIVE_INTERNAL_PLUS_WITNESS` when a real non-human-mimetic internal method is available.

No arm is allowed to fabricate unverifiable chain-of-thought as scientific evidence.

## 4. Domains

Use at least two materially different modes where external checking can be strong:

1. formal proof/program verification;
2. computational scientific result with executable replay;
3. optional experiment/measurement protocol where raw/intermediate records are auditable.

## 5. Failure injections

Witness sufficiency must be tested against hidden failures that different surfaces can expose:

- wrong problem/specification;
- stale or wrong source;
- hidden dependence;
- code/proof mismatch;
- seed/version mismatch;
- invalid calibration;
- invalid transport;
- omitted failed route;
- evaluator blind spot;
- authority overreach;
- representation change losing predecessor-valid information.

## 6. Primary outcomes

- scientific transition decision accuracy under audit;
- failure-detection recall by class;
- false acceptance and false rejection;
- independent replay success;
- audit time/cost;
- witness size/complexity;
- information omitted relative to full trace;
- downstream reopening/revision ability;
- human reviewer agreement only as a secondary measure.

## 7. Sufficiency definition

A candidate witness family is claim-sufficient only if, on protected cases:

1. it preserves every decision-relevant failure class required by the claim's evaluator contract;
2. it supports independent replay/checking where the claim requires replay;
3. it permits later selective invalidation/reopening without reconstructing hidden history;
4. it does not increase false acceptance materially relative to the strongest audit parent;
5. its audit cost is lower than or scientifically preferable to the full-trace arm.

## 8. Mechanistic ablations

Remove witness fields one at a time or in prospectively defined groups:

- minus provenance;
- minus problem/criterion binding;
- minus evaluator identity/failure class;
- minus assumption/version identity;
- minus preservation relation;
- minus unresolved limitations;
- minus authority ceiling.

An omission-specific failure is stronger evidence for a witness field than reviewer preference.

## 9. Human-readability boundary

Human readability is not assumed to be identical to scientific accountability. Some claims may be better audited by formal proof, executable replay or machine-checkable provenance than by narrative traces. Conversely, a compact machine-readable witness fails if its semantics cannot be independently interpreted well enough to detect the relevant scientific error.

## 10. Kill conditions

Contract the X7 residual if:

- B5 proof/provenance/assurance artifacts already provide the same validity-cost frontier;
- compact witnesses miss decision-critical failures;
- audit/replay cost erases machine-native gains;
- witness semantics depend on undocumented internal state;
- full human-style traces are necessary for the protected claim classes;
- results fail to transfer across a second epistemic mode.

## Terminal

```text
ME_X7_STATUS = PROSPECTIVE_UNEXECUTED
CHAIN_OF_THOUGHT_REQUIRED_AS_SCIENTIFIC_WITNESS = FALSE
CLAIM_SPECIFIC_EVALUATOR_CONTRACT_REQUIRED = TRUE
OMISSION_SPECIFIC_ABLATION_REQUIRED = TRUE
PRIMARY_COMPARATOR = STRONGEST_PROOF_PROVENANCE_ASSURANCE_PARENT
PARENT_SUFFICIENCY = VALID_TERMINAL
FIELD_STATUS_AUTHORITY = NONE
```

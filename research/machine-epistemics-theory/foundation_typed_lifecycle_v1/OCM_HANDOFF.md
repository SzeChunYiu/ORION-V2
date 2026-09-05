# OCM absorption contract — no runtime change is made here

Owning science: ORION-V2 #312; typed foundation V1. Receiving machine: ORION-OCM M2 and later milestones. This packet is a proposed exact reference, not an adoption authorization. Each absorbing change must cite its source commit and theorem ID, preserve adverse history, pass parity against the reference, and satisfy OCM's own review/merge gates.

## Required integration boundaries

| Boundary | Required machine behavior | Discriminating acceptance case |
|---|---|---|
| Statistical outputs | Store the risk-bound proposition separately from individual target truth. A typed risk action does not set the target to exact truth. | Valid 95% marginal coverage, selected 5% entirely wrong: exact assertion refused. |
| Certificate identity | Bind actual target/task/input/candidate or declared risk family, all relevant code/model/configuration/checker/calibration identities, quantifier, policy, scope, epoch, assumptions and cost contract. | Change each bound coordinate independently; stale applicability is rejected or revalidated. |
| Trust root | Resolve evidence and checker results through authenticated/current records. A string, certificate class or hash is not a trusted verdict. | Unknown evidence ID, untyped PASS, wrong checker, missing proof object: no accepted commitment. |
| Contradictions | Apply context-compatible nogood normalization after conjunction and after provenance flattening. Retain contradiction evidence separately. | Individually LIVE {a} and {b}, nogood {a,b}: conjunction cannot fire. |
| Upper profiles | Admit only justified support bounds; incompatible bounds become conflict. | An upper certificate contradicting existing exhibited support cannot silently become DEAD. |
| Graded exploration | Grades may rank exploration; only a separately valid warrant enables exact commitment. Check normalization/version premises. | Lower gates at fixed normalization never increase activation; reset denominators and the old theorem is inapplicable. |
| Rollback | Restore effective matrix/seed/restart/background/extraction and semantic versions, not only new evidence labels. | Added-and-revoked competing edge: baseline 1/4 must restore, not remain 1/8. |
| Learning | Use per-query agreement and explicit minimal-support lineage in the bounded class. Empty version space is conflict. | Several hypotheses remain but all agree on requested answer; unrelated ambiguity does not force refusal. |
| Revocation | Revisit complete dependencies; distinguish possible impact, changed label, changed payload and changed action applicability. | One shared source revoked, live alternative remains: preserve the answer where warranted. |
| Action transaction | Atomically validate current evidence/certificate versions, reserve risk/work and record an action intent before an effect. | Concurrent valid snapshots cannot both commit an invalid combined state. |
| Event identity | Replay is identical event+payload; a new exposure with the same certificate still has new risk/work cost. | Same event ID with changed payload refuses; new event with same cert is charged. |
| Language boundary | Transcript truth, quoted assertion, accepted belief and external assertion remain distinct. | DEAD(p) cannot render a confident not-p; equal seeds do not certify two parses equivalent. |
| Stopping | Meter every progress/retry/no-op path in discrete or lower-bounded units, with a separate bound on blocking waits. | Positive geometric costs alone must not be accepted as a termination proof. |

## Absorption receipt

An OCM parity receipt should contain:

```text
science_repository / source_commit / source_theorem_ids
runtime_commit / implementation_and_configuration_digests
registered_target_and_quantifiers / scope / epochs / assumptions
input_and_checker_bindings / test_universe / denominators
expected_parent_and_adverse_terminals
commands / toolchain / exit_codes / resource_costs
planted_defect_applied / defect_detected / no_alarm_control
unavailable_requirements / independent_review_state
```

The real gate needs more than this pure model: persistent immutable objects, certificate authentication, target formalization fidelity, complete dataflow dependencies, a crash-safe event store, actual operator/checker invocation receipts and a bound external-effect protocol. `commit_gate` deliberately performs no effect. Its trusted checker fixture is not something to copy into production as if a caller could self-certify.

## Frozen tests must not be repurposed

The finite development fixtures are calibration, not held-out performance evidence. An OCM successor may reproduce them for parity but needs new registered instances and strongest-parent controls for an efficacy claim. A risk guarantee must bind whether it is marginal, group-conditional, conditional-on-history, or over a predeclared family. Changing that quantifier creates a new scientific contract.

Historical M1/M2, PARENT_SUFFICIENT and CANNOT_CHECK terminals are unchanged. A successful absorption of one theorem does not close M2, KS-T12, translator invariance, language competence, or the field claim.

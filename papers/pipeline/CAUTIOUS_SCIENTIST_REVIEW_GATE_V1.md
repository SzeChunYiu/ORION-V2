# Cautious-Scientist Manuscript Gate V1

**Status:** mandatory review surface before any ORION/Machine-Epistemics paper enters R4. It grants no publication authority.

## 1. Reader model

Assume the reviewer is a careful scientist who:

- does not accept new terminology as novelty;
- expects the strongest neighbouring field to receive full credit;
- distrusts benchmarks designed in the new framework's vocabulary;
- expects preregistration or equivalent outcome-independent custody for confirmatory claims;
- treats same-model review as dependent evidence;
- worries about researcher degrees of freedom and specification sensitivity;
- expects negative controls, null cases and examples where the new system should lose;
- distinguishes reproducibility from replication and replication from broad generality;
- rejects field-level rhetoric not supported by independent cross-domain evidence.

A manuscript should be written to satisfy this reviewer, not to persuade a sympathetic reader.

## 2. Mandatory questions for every headline claim

1. What exactly is the construct, in language a parent-field scientist recognizes?
2. What mature parent already owns most of it?
3. What observation differentiates the ORION claim from the strongest parent composition?
4. Was that discriminator fixed before outcome access?
5. Can the evaluator actually detect the relevant error?
6. Is the effect robust to reasonable analysis/scoring choices?
7. Does a simpler method achieve the same result?
8. Is the gain explained by more compute, context, tools or human effort?
9. Is the result reproduced by an independent evaluator or implementation?
10. Which domain or case should make the ORION concept fail or remain inactive?
11. What negative result would cause deletion, merger or return to the parent field?
12. Does the prose state exactly the bounded evidence level rather than the aspirational theory?

Any unanswered question blocks R4 for the corresponding claim.

## 3. Separate three kinds of novelty

### Terminological novelty

New name only. Receives zero scientific credit.

### Integrative novelty

New relation, interoperability structure or explanation across established parents. Scientifically useful if it changes a protected decision or understanding beyond ordinary composition.

### Empirical/formal novelty

New prospective prediction, theorem, counterexample, measurement, mechanism or result that survives the strongest parent comparison.

Manuscripts must state which kind they actually provide.

## 4. Cautious language translation

Replace:

- `ORION understands` -> `ORION produced a correct/validated decision under...`;
- `not memorization` -> `performance survived these gold-blind/counterfactual controls...`;
- `new law` -> `candidate proposition supported under...`;
- `superior theory` -> `strictly improved registered coordinate(s) relative to F0 under contract C...`;
- `autonomous scientist` -> `system completed these stages without intervention; these human/evaluator roles remained...`;
- `field is founded` -> `results support/undermine the field hypothesis according to external demarcation...`.

## 5. Evidence labels in manuscripts

Every central result paragraph should be classifiable as one of:

- `EXPLORATORY`;
- `CONFIRMATORY`;
- `REPLICATION`;
- `FORMAL`;
- `DESCRIPTIVE`.

Exploratory findings may motivate follow-up work but cannot silently inherit confirmatory language.

## 6. Reviewer packets

### Parent-field packet

Contains native parent reconstruction, strongest comparator, registered parent wins, mapping losses and domain-specific objections.

### Methods packet

Contains preregistration/protocol, exclusions, estimands, evaluator sensitivity, all registered analyses, reasonable-specification audit, missingness, power/precision and negative results.

### Reproducibility packet

Contains code, environment, task/data IDs, prompts/configs where shareable, raw/minimally processed outputs, analysis scripts, figure-generation code and deviation ledger.

### Adversarial-collaboration packet

Contains proponent and sceptic predictions frozen before outcome access and a table showing which observations favoured which account.

## 7. Field-level special gate

The flagship cannot use an established-field voice unless all are satisfied:

- at least two materially different domains;
- a protected residual beyond the strongest parent federation;
- independent parent-field reviewers;
- robust result under reasonable alternative analyses;
- at least one independently reproduced or externally replicated key effect/proposition;
- transparent negative/parent-win cases;
- no unresolved critical authority/source/criterion failure;
- the external demarcation process supports a field rather than integration-only/subfield/rename.

Before that point, use `field hypothesis`, `candidate science`, or `research programme`.

## Current terminal

```text
CAUTIOUS_SCIENTIST_GATE = REQUIRED_FOR_R4
TERMINOLOGICAL_NOVELTY_CREDIT = ZERO
PARENT_FIELD_OBJECTION = MANDATORY
METHODS_SCEPTIC_OBJECTION = MANDATORY
INDEPENDENT_REPLICATION_OR_CROSS_DOMAIN = REQUIRED_FOR_BROAD_CLAIMS
FIELD_VOICE = PROVISIONAL_ONLY
```

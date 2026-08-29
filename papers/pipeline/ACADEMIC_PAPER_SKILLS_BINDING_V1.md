# ORION-V2 Recursive Academic-Paper Pipeline Binding V1

**Status:** manuscript-development governance. This file grants no scientific truth, novelty, publication readiness, journal acceptance, or field status.

## Bound methodology

ORION-V2 binds the public repository `SzeChunYiu/academic-paper-skills` at commit:

`d9466ca770d5864d60318c8220c58478b640c50f`

for the current recursive manuscript-development programme.

The bound orchestration identity is `academic-paper-pipeline` v1.1.0 together with its required shared contracts, especially:

- iterative editor-controlled paper development;
- fail-closed atomic claim verification;
- editor–reviewer decision synthesis without vote counting;
- paper-archetype resolution;
- unknown-paper self-research;
- explanatory sufficiency;
- claim-driven figure/evidence planning;
- sentence/paragraph logic and manuscript-surface QA;
- canonical project-state recording.

A future skill update may be evaluated, but it does not silently change this manuscript-development run. Any adopted skill update creates a new pipeline identity and revision delta.

## Why this is needed

The ORION-V2 paper programme is unusual in two ways.

First, the primary papers are hybrids of theory, methods, computational evaluation, scientific-governance semantics and cross-domain transfer. Their final archetypes cannot be inferred from prestige-journal surface style.

Second, the Machine Epistemics flagship is a field-defining Perspective. Its epistemic job is different from a primary Article: it must establish a coherent object of study, demonstrate a real coordination/demarcation problem, provide a compact organizing framework, identify a falsifiable research programme and treat mature parent fields fairly. It must not present unpublished ORION-V2 results as if they were established field evidence.

The academic-paper pipeline is therefore used as a stateful scientific-development process, not a prose-polishing utility.

## Recursive loop

Each manuscript repeatedly executes:

`target/archetype research -> evidence freeze -> atomic claim inventory -> argument/figure architecture -> draft -> pre-review QA -> editor triage -> mutually blind reviewer round -> editor synthesis -> minimum-sufficient revision -> revision delta -> targeted re-review -> closure check`

The loop ends only at one of:

- `simulated_publication_ready_for_target`;
- `blocked_on_author_evidence`;
- `scientifically_sound_but_target_mismatch`;
- `current_claims_not_established`;
- `blocked_by_integrity_or_compliance`.

No manuscript is advanced by reviewer vote count, wordsmithing quality, or the existence of a complete draft.

## Project-state boundary

The programme records, per manuscript:

- target venue and article/content type;
- dominant/secondary paper archetypes;
- bounded research question and contribution class;
- headline and atomic claims;
- source passages and citation entailment;
- formal/proof dependencies where applicable;
- protected or author-provided analyses/results;
- figure/table decision roles;
- editor/reviewer concern IDs;
- revision deltas and re-review status;
- unresolved evidence and real-world blockers;
- AI-use disclosure state.

Internal ORION repository paths, commits, CI jobs, issue numbers and implementation helper names remain project-state metadata and are removed from manuscript-facing prose unless scientifically indispensable.

## Evidence rule

External literature may support positioning, methodological choices, definitions, historical claims and Discussion/Perspective synthesis. It may not be converted into an unpublished ORION-V2 result.

Primary-result papers P-A through P-D cannot cross `current_claims_not_established` until their protected studies produce the evidence required by their frozen survival gates. P-E additionally requires genuinely prospective evidence; if that evidence is not obtained, the scientifically cheapest closure route is merger into P-C rather than invented retrospective support.

## Reviewer model

Default mutually blind initial reviewer lenses:

1. **validity/methods/inference** — whether the exact claim is established and whether tests/baselines/falsifiers discriminate the strongest alternatives;
2. **contribution/prior work/target significance** — whether the residual is real after strongest-parent reduction and appropriate for the target venue;
3. **reproducibility/readership/boundaries** — whether the scientific object, evidence, limitations, figures, source identity and release materials are independently evaluable.

For the Machine Epistemics flagship, an additional demarcation lens challenges whether the proposed field is merely a renaming or integration of established parents.

## Moving-goalpost protection

After Round 1, a newly blocking concern requires one of:

- revision introduced the issue;
- new evidence exposed it;
- previously unassessable material became visible;
- a genuine expertise gap was discovered;
- an original major concern was incompletely scoped.

Otherwise it is treated as optional enrichment unless the editor independently finds it essential to scientific validity or target criteria.

## Publication targets

The target/fallback strategy remains governed by `papers/PUBLICATION_TARGETS_AND_FALLBACKS_V1.md`. Target adaptation occurs after scientific validity and claim/evidence structure are established. Venue transfer may change length, section mechanics and exposition, but never the frozen evidence, negative results, parent-baseline result or claim boundary to evade criticism.

## Release rule

No manuscript-facing file receives a submission/publication-ready label while an in-scope atomic assertion is `SUPPORTED_INTERNAL`, `UNRESOLVED`, `CONTRADICTED`, `BLOCKED`, or materially `NOT_ASSESSABLE`.

The pipeline simulates readiness. Real acceptance and scientific authority remain external.
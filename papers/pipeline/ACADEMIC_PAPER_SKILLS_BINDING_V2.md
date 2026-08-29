# ORION-V2 Academic Paper Pipeline Binding V2

**Programme:** ORION-V2 / Machine Epistemics  
**Supersedes for current manuscript work:** `ACADEMIC_PAPER_SKILLS_BINDING_V1.md`  
**Bound repository:** `SzeChunYiu/academic-paper-skills`  
**Bound commit:** `d2cac7bd0d3152369acee5c3859059dc87fcd24d`  
**Pipeline:** `academic-paper-pipeline` v1.6.0  
**Writing router:** `academic-writing`

This binding changes manuscript-development governance, not scientific results or protocol identities.

## 1. Canonical manuscript lifecycle

Every surviving manuscript follows:

```text
exact target/archetype resolution
-> evidence freeze
-> protocol/conduct contract
-> data integrity/stewardship contract
-> statistical inference/uncertainty contract
-> atomic claim inventory
-> claim/evidence architecture
-> figure/display contracts
-> manuscript drafting/rewrite
-> sentence/explanation/surface QA
-> editor triage
-> independent reviewer round
-> editor synthesis
-> minimum-sufficient revision
-> targeted re-review
-> arXiv or journal release gate
```

A complete draft is not a release state. A polished draft is not a scientific result.

## 2. arXiv-first portfolio rule

The project now uses one scientific master per paper and two release adapters:

```text
scientific master
  -> arXiv public preprint package
  -> journal-specific package
```

The journal package is not a scientifically stronger hidden version. Journal adaptation may change formatting, length, section allocation, cover metadata and externally requested clarification/correction. It may not:

- strengthen a claim after seeing results;
- hide null/adverse/CANNOT_CHECK evidence;
- drop a strongest parent to improve novelty;
- change confirmatory endpoints or success criteria;
- turn a pre-results protocol into a completed empirical Article;
- present the arXiv and journal versions as separate studies when they share the same evidence.

## 3. Surviving paper archetypes

### FLAGSHIP

```text
PRIMARY = Perspective / emerging-field research agenda
SECONDARY = theory-synthesis / demarcation paper
ARXIV = public Perspective preprint after human adoption + atomic citation/claim gate
JOURNAL = Nature Machine Intelligence Perspective first target
```

### P-A

```text
PRIMARY = computational/ML empirical method paper
SECONDARY = benchmark + scientific-discovery method
ARXIV = blocked until protected hidden-donor Results exist
JOURNAL = Nature Machine Intelligence Article if result terminal earns it
```

### P-B

```text
PRIMARY = theory/method hybrid
SECONDARY = cross-parent benchmark / scientific interface paper
ARXIV = blocked until protected cross-parent benchmark/mechanical proof receipts close
JOURNAL = Nature Computational Science Article if standalone decision residual survives
```

### P-C

```text
PRIMARY = computational/agent scientific-control paper
SECONDARY = decision/control framework + benchmark
ARXIV = blocked until independent parity and protected solver/control Results exist
JOURNAL = Nature Machine Intelligence Article if result terminal earns it
```

### P-D

```text
PRIMARY = computational/statistical assurance paper
SECONDARY = evidence-synthesis + dynamic evaluation method
ARXIV = blocked until dependence/evaluator/joint-pipeline Results exist
JOURNAL = Nature Machine Intelligence Article if joint residual survives
```

The #51 LLM Prospective Revision Audit is governed on its own branch by a matching V2 pipeline binding and is closest to arXiv/JMLR release because its primary evidence is already theorem/proof based.

## 4. Study protocol/conduct layer

For P-A through P-D, manuscript Methods and Results are projections of the frozen prospective studies and their execution receipts. Keep independent:

- planned;
- executed;
- verified by receipt;
- deviation;
- exploratory/post-hoc;
- unknown;
- not applicable.

A deferred or incomplete campaign cannot be described in past tense as completed merely because a Results section exists.

For the flagship Perspective, this layer applies only to empirical examples drawn from ORION-V2 (for example SD20); conceptual synthesis itself is not forced into an empirical-study template.

## 5. Data integrity/stewardship layer

Every quantitative/result-bearing paper must bind:

```text
source/acquisition identity
-> immutable raw or exact external-reference origin
-> QC/validation receipts
-> versioned transformations
-> immutable analysis-ready snapshot
-> analysis/display inputs
-> governed release object
-> bounded claim
```

Broken lineage, silent exclusion, count drift, hidden adverse/null removal, missing QC, or analysis-input mismatch blocks the dependent paper surface.

## 6. Statistical inference/uncertainty layer

Every result block must bind:

```text
claim/question
-> estimand
-> independent unit / dependence structure
-> population
-> frozen analysis plan
-> immutable input
-> executed analysis
-> diagnostics/sensitivity
-> estimate + typed uncertainty
-> table/figure/prose
-> bounded claim
```

Do not use `P>0.05` as equivalence, repeated model samples as independent scientific cases, or an average across tasks to hide decision-changing failures.

## 7. Atomic claim layer

All public-preprint assertions are inventoried at atomic resolution, including:

- definitions;
- numerical results;
- theorem/proof claims;
- source/novelty claims;
- figure/table interpretations;
- methods/conduct claims;
- availability/reproducibility claims;
- abstract/title/conclusion restatements.

A preprint cannot be labeled scientifically release-ready while an in-scope public assertion is `UNRESOLVED`, `CONTRADICTED` or `BLOCKED`.

For P-A through P-D, unresolved **result placeholders are kept outside the public scientific master or clearly marked as authoring placeholders and therefore block arXiv release**.

## 8. Figure/display layer

Every main display must answer a reader decision question and bind to an immutable evidence chain:

```text
data snapshot
-> analysis receipt
-> render receipt
-> source-data object
-> caption/prose claim
```

No decorative architecture figure earns main-paper space merely because a peer paper has one. Negative/failure displays remain main-text when they alter the headline interpretation.

## 9. Prose and manuscript-surface layer

Public manuscripts must translate repository artifacts into scientific meaning.

Do not expose in manuscript-facing prose:

- issue/PR/branch numbers;
- local paths;
- CI job names;
- helper functions;
- script/config filenames;
- internal terminal codenames when ordinary scientific language is clearer.

Those remain in reproducibility/artifact documentation.

## 10. Reviewer/editor loop

Initial reviews use independent lenses:

1. validity/methods/inference;
2. contribution/strongest prior work/target significance;
3. reproducibility/readership/boundaries.

The flagship adds an independent field/name demarcation lens.

Reviewer votes do not determine acceptance. Every blocking concern needs a stable concern ID and a concrete resolution test.

## 11. Human and AI-use boundary

ORION-V2 has used AI extensively for literature discovery, formalization, study design, critique, software and drafting. Before arXiv or journal release, human authors must independently understand and adopt the claims, inspect the load-bearing evidence and citations, and accept responsibility under the current venue/preprint policies.

AI systems are not authors.

## 12. Current release states

```text
FLAGSHIP = SCIENCE_MASTER_COMPLETE__ARXIV_HUMAN_AND_ATOMIC_RELEASE_GATE_OPEN
P_A = PUBLIC_MASTER_CAN_BE_FINISHED__ARXIV_BLOCKED_ON_RESULTS
P_B = PUBLIC_MASTER_CAN_BE_FINISHED__ARXIV_BLOCKED_ON_RESULTS
P_C = PUBLIC_MASTER_CAN_BE_FINISHED__ARXIV_BLOCKED_ON_RESULTS
P_D = PUBLIC_MASTER_CAN_BE_FINISHED__ARXIV_BLOCKED_ON_RESULTS
LLM_PRA_51 = CLOSEST_TO_ARXIV_JMLR_RELEASE
```

Real journal acceptance remains external.

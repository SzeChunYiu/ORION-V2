# ORION-V2 Computation-Only Successor Handoff V1

**Owner:** #50  
**Instruction:** framework/reference implementation work is closed unless a valid protected result exposes a concrete defect. The successor should spend its effort on outcome-generating computation, source acquisition/corpus construction, analysis, independent adjudication and evidence-bound manuscript updates.

## 0. First actions

Always fetch the latest branch head and latest #45/#46/#47/#48/#49/#50 before running.

Run the non-outcome preflights first:

```bash
python scripts/run_recursive_framework_preflight.py --output /tmp/framework-preflight.json
python scripts/run_scientific_development_reference.py --output /tmp/sd-reference.json
python scripts/run_transfer_formal_mechanics_reference.py --output /tmp/fm-reference.json
python scripts/run_formalism_genesis_reference.py --output /tmp/fg-reference.json
```

If these fail, repair implementation only; do not reinterpret scientific hypotheses.

## 1. Do not redesign by default

Canonical architecture:

- `research/foundation-saturation/ORION_V2_RECURSIVE_DEVELOPMENT_ARCHITECTURE_V1.md`
- `research/foundation-saturation/ORION_V2_RECURSIVE_DEVELOPMENT_COMPONENT_GRAPH_V1.json`
- `research/closure/V2_FRAMEWORK_IMPLEMENTATION_COMPLETION_RECEIPT_V1.json`

Cross-layer controller:

- `src/orion_v2/development_controller.py`

Population source contract:

- `src/orion_v2/scientific_development_sources.py`
- `scripts/assemble_scientific_development_episodes.py`
- `scripts/build_scientific_development_corpus.py`

A new framework revision is justified only by a registered protected failure under #47 or a formal inconsistency in the reference semantics.

## 2. Existing decisive computation — #45

Continue the current execution state from issue #45; do not restart completed/invalid historical runs under the same identity.

Priority science remains:

1. E30 confirmatory BugsInPy core arms.
2. E60 component/drag causal study after interpretable E30.
3. E70 fresh/anti-copy/composition controls.
4. matched F0/F2 around E40 CausalBench.
5. matched F0/F2 around E50 strongest native materials model.
6. V1/V2 parity and independently owned cells.

All raw adverse/simple/parent/tie results remain immutable.

## 3. FM formal-mechanics computation — #48

Protocol: `research/experiments/CONCEPTUAL_TRANSFER_FORMAL_MECHANICS_PROTOCOL_V1.json`.

Run/implement the generated protected studies without changing frozen estimands:

- FM10 finite relational mapping, >=120;
- FM20 anti-unification/generalization, >=120;
- FM30 FCA concept closure/revision, >=96;
- FM40 invariance/equivariance, >=120;
- FM50 finite-category/functoriality, >=96;
- FM60 obstruction/counterexample, >=120;
- FM70 held-out contextual regime selector;
- FM80 prospective mathematics↔science transfer.

Exact/formal oracles are preferred wherever defined. Strongest formal parent and fixed-lesson controls are mandatory.

## 4. FG formalism-genesis computation — #48

Protocol: `research/experiments/FORMALISM_GENESIS_PROTOCOL_V1.json`.

- FG10 representation collision/minimal primitive, >=160;
- FG20 generalized object/closure, >=120;
- FG30 relation/operation/invariant synthesis, >=160;
- FG40 axiom/rule synthesis, >=120;
- FG50 rival-formalism semantics/equivalence, >=120;
- FG60 conservative extension/predecessor recovery, >=120;
- FG70 balanced `new formalism vs parent/local patch/more data/no change`, >=160;
- FG80 fresh mini-frontier, >=80;
- FG90 genuine frontier exploratory lane.

**Critical failure:** false formalism invention. A difficult problem is not evidence that a new language is needed.

FG90 is exploratory unless independently proof-checked or empirically validated.

## 5. SD population / recursive development computation — #49

Backlog: `research/experiments/SCIENTIFIC_DEVELOPMENT_EXECUTION_BACKLOG_V1.json`.

### SD10

Implement lawful source-specific acquisition adapters that emit the source-observation contract. Assemble trajectories using explicit outcome witnesses. Do not infer validated success from citations, prizes or fame.

```bash
python scripts/assemble_scientific_development_episodes.py \
  --observation SOURCE_A_OBS.jsonl \
  --observation SOURCE_B_OBS.jsonl \
  --outcome-binding VALIDATED_OUTCOMES.jsonl \
  --output episodes.jsonl \
  --receipt assembly-receipt.json

python scripts/build_scientific_development_corpus.py \
  --input episodes.jsonl \
  --output corpus.json \
  --receipt corpus-receipt.json
```

Bind survivorship/publication/citation/language/field/epoch/team/institution/failure-censoring biases before population claims.

### SD20–SD60

Discover development operators without desired labels; match success and failure trajectories; hold out entire fields/epochs; recursively test higher abstractions; reproduce/challenge known science-of-science regularities as calibration only.

### SD70

Fresh generated prospective meta-policy suite:

```bash
bash scripts/run_scientific_development_meta_pilot.sh RUN
```

The private oracle must remain absent during model calls.

### SD80

Prospective naturalistic meta-policy in >=3 materially distinct domains with independent adjudication.

### SD90

Attempt another abstraction pass plus new-domain/new-epoch/hostile-omission challenges. `RECURSIVE_STABILITY_CANDIDATE` is allowed only if no material higher-level residual remains. `ULTIMATE_TRUTH` is never an internal terminal.

## 6. Result import into papers

Before editing conclusions, use:

- `papers/pipeline/PORTFOLIO_CLAIM_EVIDENCE_LEDGER_V3_RECURSIVE_DEVELOPMENT_DELTA.json`
- `papers/pipeline/RECURSIVE_DEVELOPMENT_RESULT_IMPORT_MAP_V1.json`
- `papers/pipeline/POST_RESULT_IMPORT_AND_R4_PLAYBOOK_V1.md`
- `papers/iteration/ROUND_18_RECURSIVE_DEVELOPMENT_TOP_TIER_EDITOR_SYNTHESIS_V1.md`

Workflow per result:

```text
validate receipt/hash
-> classify infrastructure vs science
-> reproduce frozen analysis
-> preserve negative/parent/simple/tie/CANNOT_CHECK
-> bind result to allowed claim IDs
-> apply #47 contraction/revision if triggered
-> then update manuscript/results/figures
```

Do not create a standalone recursive-development paper unless SD20–SD80 produces a protected result-scale thesis beyond the flagship/P-C and mature science-of-science parents.

## 7. Scientific stop condition

The computation successor is finished only when every E/FM/FG/SD frontier has a valid terminal:

`SUPPORTED`, `NEGATIVE_RESULT`, `PARENT_SUFFICIENT`, `SIMPLE_CONTROL_WIN`, `TIE`, `CONTEXTUAL`, `REDUNDANT/HARMFUL`, `MERGE/DROP`, or explicit `CANNOT_CHECK`.

No positive F2 result is required.

## 8. Handoff terminal

```text
FRAMEWORK_REDESIGN_REQUIRED = NO_BY_DEFAULT
REFERENCE_FRAMEWORK = COMPLETE
EXECUTION_SCAFFOLDS = PRESENT
PAPER_CLAIM_IMPORT_DESTINATIONS = FROZEN
OUTCOME_GENERATING_COMPUTATION = OPEN
INDEPENDENT_EXTERNAL_EVIDENCE = OPEN
R3 = 0
R4 = 0
```

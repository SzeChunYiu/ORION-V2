# ORION-V2 Recursive Framework Execution Handoff V1

**Owner:** issue #50  
**Science lanes:** #45, #46, #47, #48, #49  
**Status:** executable scaffold present; population-scale and prospective scientific outcomes remain open.

## 1. What the next AI session inherits

The new recursive-scientific-development programme is not prose-only. The branch contains runnable reference semantics, generated hidden-oracle tasks, arm execution, blinded dispatch, evaluation, corpus normalization, unit tests and CI.

### Core framework

- `src/orion_v2/scientific_development.py`
  - source-bound `ScientificDevelopmentEpisode` / `DevelopmentStep` objects;
  - explicit validated success/failure/partial/redirected/abandoned/unknown outcome classes;
  - `CorpusBiasAudit` for survivorship, publication, citation, field/epoch, language/geography, team/institution and failure-censoring coverage;
  - transparent success-vs-failure operator discovery for calibration;
  - fail-closed meta-principle promotion requiring matched failures, strongest parent, held-out field/epoch, prospective evaluation and resource accounting.

- `src/orion_v2/recursive_generalization.py`
  - adjacent abstraction-level receipts;
  - strongest-lower-level/parent sufficiency gate;
  - critical-information-loss hard block;
  - held-out versus prospective higher-level residual distinction;
  - bounded `RECURSIVE_STABILITY_CANDIDATE` requiring another failed generalization pass plus new-domain, new-epoch and hostile-omission challenges;
  - never authorizes `ULTIMATE_TRUTH`.

Existing connected framework remains binding:

- `src/orion_v2/knowledge_metabolism.py`
- `src/orion_v2/conceptual_development.py`
- `src/orion_v2/transfer_formal_mechanics.py`
- `src/orion_v2/formalism_genesis.py`

## 2. Population corpus interface

Canonical schema:

- `research/schemas/SCIENTIFIC_DEVELOPMENT_EPISODE_SCHEMA_V1.json`

Normalizer:

```bash
python scripts/build_scientific_development_corpus.py \
  --input SOURCE_A.jsonl \
  --input SOURCE_B.jsonl \
  --output corpus.json \
  --receipt corpus-receipt.json
```

Acquisition must remain in source-specific lawful adapters with independent provenance/custody receipts. This merger intentionally does not scrape the web or treat missing unpublished failures as absent.

Citation, prize, fame and disruption metrics are proxy observables only.

## 3. Reference semantics preflight

Run:

```bash
python scripts/run_scientific_development_reference.py \
  --output /tmp/sd-reference.json
```

Expected terminal:

```text
REFERENCE_SEMANTICS_CALIBRATION_ONLY
```

The reference check tests that:

- opaque trajectory features can generate a candidate operator without a named breakthrough lesson;
- a historical regularity without prospective intervention remains `POPULATION_REGULARITY_ONLY`;
- a higher abstraction can earn a prospective residual without becoming ultimate truth;
- recursive stability remains bounded/reopenable.

This is software/reference validation, not a scientific result.

## 4. Fresh SD70 meta-policy benchmark

Generator:

- `scripts/generate_scientific_development_meta_benchmark.py`

It creates arbitrary context/action codewords and task-specific latent policies after freeze. Public training trajectories contain both validated successes and matched failures. Private files contain the generator weights and held-out correct action.

Prepare:

```bash
python scripts/run_scientific_development_meta_suite.py prepare \
  --workdir RUN \
  --tasks 120 \
  --train-episodes 16 \
  --arms TARGET_ONLY_DIRECT,FIXED_META_HEURISTIC,F0_PARENT_FEDERATION,F2_STATIC_NO_RECURSION,F2_RECURSIVE_META_DISCOVERY_FULL
```

Dispatch:

```bash
python scripts/run_scientific_development_meta_suite.py dispatch \
  --workdir RUN \
  --arms TARGET_ONLY_DIRECT,FIXED_META_HEURISTIC,F0_PARENT_FEDERATION,F2_STATIC_NO_RECURSION,F2_RECURSIVE_META_DISCOVERY_FULL \
  --max-concurrency 2
```

During dispatch the private oracle file is loaded into the orchestrator, hash-committed, removed from disk, and restored hash-exactly only after all child arm processes terminate.

Default model arm executable:

- `scripts/orion_scientific_development_arms.py`

It follows the repo-wide `--request REQUEST.json --response RESPONSE.json` contract and uses the authenticated Codex CLI. Override with `ORION_SD70_ARM_COMMAND` for another versioned compatible arm executable.

Evaluate:

```bash
python scripts/run_scientific_development_meta_suite.py evaluate \
  --workdir RUN \
  --arms TARGET_ONLY_DIRECT,FIXED_META_HEURISTIC,F0_PARENT_FEDERATION,F2_STATIC_NO_RECURSION,F2_RECURSIVE_META_DISCOVERY_FULL
```

One-command pilot:

```bash
bash scripts/run_scientific_development_meta_pilot.sh RUN
```

No SD70 result can self-authorize a causal law, F2 superiority, field status or paper readiness.

## 5. Execution backlog

Canonical machine-readable backlog:

- `research/experiments/SCIENTIFIC_DEVELOPMENT_EXECUTION_BACKLOG_V1.json`

It binds SD00 through SD90:

- SD00 reference semantics;
- SD10 corpus/bias audit;
- SD20 development-operator discovery;
- SD30 matched success/failure contrasts;
- SD40 held-out field/epoch transfer;
- SD50 recursive abstraction-level tests;
- SD60 science-of-science calibration;
- SD70 fresh generated meta-policy;
- SD80 prospective naturalistic meta-policy in >=3 domains;
- SD90 recursive stability/hostile omission challenge.

Do not merge this backlog into E20/E30 identities. It is additive and prospectively separate.

## 6. Tests and CI

Focused tests:

- `tests/unit/test_scientific_development_wave6.py`
- `tests/unit/test_recursive_generalization_wave6.py`
- `tests/unit/test_scientific_development_scripts_wave6.py`

Workflow:

- `.github/workflows/wave6-scientific-development.yml`

The workflow compiles all new framework/scripts, runs the focused unit suite, runs the reference calibration, validates schema/protocol/backlog, generates fresh SD70 tasks, verifies oracle separation, and runs a non-model stub child through the blinded dispatcher to prove the private oracle is absent during child execution and restored afterwards.

## 7. Existing mathematical/conceptual/formal lanes

The next session must also preserve and extend the already executable #48 stack:

- transfer discovery and `ConceptState` transitions;
- all-science mathematics-first donor atlas;
- partial typed homomorphism/invariance/anti-unification/FCA/functor/obstruction mechanics;
- FM10–FM80 formal benchmark protocol;
- formalism-genesis collision/minimal-primitive/axiom/recovery mechanics;
- FG10–FG90 formalism-genesis protocol.

These are parent-aware candidate mechanisms, not ORION-owned mathematical inventions.

## 8. Paper integration already present

Formal manuscript surfaces include:

- `papers/formalism/FLAGSHIP_CONCEPTUAL_DEVELOPMENT_FORMALISM_BOX_V1.md`
- `papers/formalism/FLAGSHIP_FORMALISM_GENESIS_BOX_V1.md`
- `papers/formalism/FLAGSHIP_RECURSIVE_SCIENTIFIC_DEVELOPMENT_BOX_V1.md`
- `papers/formalism/P_A_TRANSFER_DISCOVERY_FORMALISM_V1.md`
- `papers/formalism/P_A_FORMALISM_GENESIS_EXTENSION_V1.md`
- `papers/formalism/P_B_RELATION_TRANSPORT_FORMALISM_V1.md`
- `papers/formalism/P_B_FORMALISM_GENESIS_EXTENSION_V1.md`
- `papers/formalism/P_C_REGIME_AND_SEARCH_CONTROL_FORMALISM_V1.md`
- `papers/formalism/P_C_FORMALISM_GENESIS_EXTENSION_V1.md`

The next session must integrate only evidence-supported parts into the actual manuscript versions and update atomic claim/evidence ledgers. A formal box is not an R3 result.

## 9. What remains genuinely open

This scaffold intentionally does **not** fabricate:

- source-specific population-scale acquisition adapters for every scholarly/preprint/patent/software/protocol source;
- a completed multi-source SD10 corpus;
- SD20–SD60 scientific results;
- SD70 model-arm results;
- SD80 naturalistic prospective evidence;
- SD90 recursive stability;
- FM/FG confirmatory outcomes;
- independent domain/external adjudication;
- R3/R4 paper status.

The AI session should now implement/acquire/run these from the supplied interfaces rather than redesigning the architecture from zero.

## 10. Handoff terminal

```text
RECURSIVE_FRAMEWORK_CODE_SCAFFOLD = PRESENT
POPULATION_CORPUS_CONTRACT = PRESENT
FRESH_SD70_GENERATOR = PRESENT
GOLD_BLIND_ARM_EXECUTABLE = PRESENT
PRIVATE_ORACLE_BLINDED_DISPATCH = PRESENT
EVALUATOR = PRESENT
REFERENCE_CALIBRATION = PRESENT
EXECUTION_BACKLOG_SD00_SD90 = PRESENT
FOCUSED_TESTS = PRESENT
CI_GATE = PRESENT
SCIENTIFIC_RESULTS_SD10_SD90 = OPEN
R3_R4_PROMOTION = NOT_AUTHORIZED
```

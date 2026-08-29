# Primary Papers Reproducibility, Data and Code Plan V1

**Papers:** P-A, P-B, P-C, P-D  
**Purpose:** define what must be released or explained for independent interpretation/reproduction before target-journal submission.

This plan does not override legal, licensing, privacy, security or third-party restrictions.

## Global package

Every primary Article should bind:

```text
source_commit
protocol_version
claim_ledger_version
result_schema_version
analysis_code_hash
task/case_registry_hash
arm/configuration_manifest
model/tool versions
evaluator/adjudicator identity or blinded custody receipt
resource-accounting definition
invalid/missing-case ledger
primary-result receipt
figure/source-data hashes
AI-use disclosure version
```

## Data Availability statement skeleton

> The data and task materials required to evaluate the main claims are available at [REPOSITORY/DOI], subject to the restrictions described below. The release includes frozen task/case registries, configuration manifests, evaluation outputs or reproducible generators, result receipts and source data for the main figures. Materials that cannot be redistributed because of licensing, privacy, security or third-party restrictions are identified explicitly together with the access route or a reproducible derived fixture where permitted.

Do not claim “all data publicly available” if source licensing prevents it.

## Code Availability statement skeleton

> Code used for the registered experiments, evaluation and primary analysis is available at [REPOSITORY/DOI] at commit [SHA]. The archive includes deterministic rerun instructions, environment/version information, frozen analysis specifications, invalid-run handling and scripts that regenerate the reported main figures/tables from the released result receipts. External model APIs, proprietary services or instruments are versioned/configured where possible but are not redistributed.

## Source Data

For Nature-Portfolio targets, prepare source-data files for each main figure/table where the journal requests them.

Source data should contain the values needed to regenerate the visual, not only a screenshot or summarized image.

No source-data file may silently exclude adverse/null/invalid categories shown in the analysis.

---

# P-A package

Release/describe:

- target-case registry;
- candidate source universe cutoff;
- hidden donor identities after evaluation unlock;
- donor-native known-answer sets;
- distractor construction;
- counter-probes;
- arm retrieval outputs/rankings;
- native/target adjudication;
- false-analogy classification;
- resource vectors;
- paired analysis code.

### Special contamination rule

If papers/tasks might be in model training data, state what can and cannot be inferred about parametric exposure. Use post-cutoff/renaming/holdout controls where registered; do not claim proof of zero contamination without evidence.

---

# P-B package

Release/describe:

- relation/context fixture registry;
- native-parent identity;
- native known-answer verdicts;
- formal proof/countermodel source;
- mapping/loss/obstruction receipts;
- composition cases;
- support-family/reopening fixtures;
- parent-selector outputs;
- cross-parent reuse decisions;
- CANNOT_CHECK/invalid ledger.

### Formal artifact rule

Every proposition retained in main text must map to:

- a human-readable proof or explicit parent theorem;
- machine proof/check if available;
- countermodel search scope;
- assumption list.

---

# P-C package

Release/describe:

- V1 parity registry and critical-cell definitions;
- independent semantic-evaluator custody receipts;
- task registries and hidden gold;
- blocker labels and how they were set;
- intervention preorder/MinSuff oracle/adjudication;
- arm manifests;
- tool/evaluator versions;
- terminal classifications;
- component ablations;
- resource vectors;
- analysis code.

### Hindsight rule

If minimal sufficient interventions use post-hoc benchmark oracle knowledge, say so explicitly. The metric evaluates controller choice; it is not evidence that the controller knew the oracle online.

---

# P-D package

Release/describe:

- synthetic/known dependence generative structures;
- solver-visible versus evaluator-hidden edges/latent causes;
- dependence mis-specification variants;
- evaluator sensitivity/failure-class definitions;
- environment response mechanisms;
- static negative controls;
- parent statistical/performative model configurations;
- unified and separate-pipeline decisions;
- reopening outcomes;
- sensitivity analysis.

### Statistical-data rule

Evidence items inside one dependence cluster are not independent sample units unless the estimand/model explicitly treats them as such. Release enough cluster/generative structure to audit this.

---

# Reproducibility terminal

Before submission:

```text
MAIN_RESULT_RERUN = PASS or BOUNDED_EXTERNAL_SERVICE
SOURCE_DATA = COMPLETE
INVALID_CASE_LEDGER = COMPLETE
CONFIG_VERSIONING = COMPLETE
PRIMARY_ANALYSIS = FROZEN
AI_DISCLOSURE = CURRENT
```

If a proprietary model/API cannot be deterministically reproduced, report this limitation and preserve prompts/config/version/timestamps/raw outputs where terms permit. Do not label stochastic third-party service execution fully reproducible when it is not.

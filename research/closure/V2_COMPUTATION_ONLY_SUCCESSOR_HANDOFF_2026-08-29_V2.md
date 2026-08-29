# ORION-V2 Computation-Only Successor Handoff — 2026-08-29 V2

**Owner:** issue #50  
**Canonical execution owner:** issue #45  
**Scientificity / revision:** #46 / #47  
**Conceptual/formal science:** #48  
**Recursive scientific-development science:** #49  

## Terminal at handoff

```text
REFERENCE_FRAMEWORK_AND_ROUTING = COMPLETE
REFERENCE_CI = GREEN_BEFORE_FINAL_FORMAL_CAMPAIGN_HARDENING
SD70_BLINDED_PLUMBING = COMPLETE
FM10_FM60_FG10_FG80_BLINDED_GENERATED_PLUMBING = COMPLETE
PROTECTED_MODEL_COMPUTATION = OPEN
NATURALISTIC_AND_EXTERNAL_EVIDENCE = OPEN
R3_PAPERS = 0
R4_PAPERS = 0
NEXT_DEFAULT_ACTION = COMPUTE_AND_IMPORT_RESULTS
```

This document does **not** authorize outcome generation from stale identities. Before doing anything, fetch the current branch and latest #45/#46/#47/#48/#49/#50. Another execution session may have advanced the branch or frozen a newer run identity.

## 1. Do not redesign V2 by default

The reference architecture, source contracts, cross-layer routing, formal mechanics, formalism-genesis gates, recursive-generalization gates, generated benchmark plumbing and result-import map are present.

A disappointing result is not a framework-reopen trigger. F2 losing is not a framework-reopen trigger.

Reopen only when:

1. a valid protected result exposes a material omitted coordinate;
2. an exact formal counterexample contradicts reference semantics;
3. the same omitted coordinate recurs across materially different valid domains; or
4. an external parent-field review identifies a genuine conceptual defect.

Any legitimate revision follows #47 and receives a new prospective identity. It cannot rescue the predecessor result retroactively.

## 2. Commit discipline

Work in small coherent rounds.

For every round:

```text
FETCH CURRENT HEAD
-> FETCH CURRENT TARGET FILE SHA
-> APPLY ONE COHERENT CHANGE OR RESULT IMPORT
-> RUN/VERIFY RELEVANT TESTS
-> COMMIT
-> RE-FETCH CURRENT HEAD
```

Never overwrite concurrent execution work.

## 3. First preflight

Reference-only checks are not scientific outcomes, but should be green before spending model/compute budget.

Run the relevant existing CI and, locally where useful:

```bash
python scripts/run_scientific_development_reference.py --output /tmp/sd-reference.json
python scripts/run_transfer_formal_mechanics_reference.py --output /tmp/fm-reference.json
```

Run the recursive-framework preflight already bound by `wave6-recursive-framework` and verify current CI rather than trusting this historical handoff statement.

## 4. Existing E-series — always follow live #45

Do not duplicate or renumber protected E-series identities.

Fetch #45 first and continue whichever of these remain open:

- E30 BugsInPy confirmatory core study;
- E60 causal component / drag study;
- E70 fresh anti-copy/counterfactual studies;
- matched F0/F2 scientific-control layers around E40 CausalBench;
- matched F0/F2 materials layers around E50;
- paper-specific E80+ studies;
- machine-verifiable parity work.

Preserve infrastructure failures as infrastructure. Preserve valid adverse scientific outcomes as science.

## 5. Generated FM/FG exact campaign

### Frozen campaign plan

```text
research/experiments/FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V1.json
```

It binds registered minimum task counts and study-specific comparator arms.

Generated lane coverage:

```text
FM10 FM20 FM30 FM40 FM50 FM60
FG10 FG20 FG30 FG40 FG50 FG60 FG70 FG80
```

### Prepare only — safe before model dispatch

```bash
python scripts/run_formal_discovery_campaign.py prepare \
  --campaign-root RUN
```

This creates study-specific freezes and private exact/mechanical oracles.

### Dispatch

```bash
python scripts/run_formal_discovery_campaign.py dispatch \
  --campaign-root RUN \
  --max-concurrency 2
```

For every study, the private oracle is hash-committed and absent from disk throughout child/model calls.

### Evaluate

```bash
python scripts/run_formal_discovery_campaign.py evaluate \
  --campaign-root RUN
```

### One command

```bash
bash scripts/run_formal_discovery_campaign.sh RUN
```

To stage or run only a subset:

```bash
ORION_FORMAL_STUDIES=FM10,FM20,FG10 bash scripts/run_formal_discovery_campaign.sh RUN
```

Do not interpret exact generated success as naturalistic cross-domain validation.

### Generated-lane boundaries

- `FM70`: requires held-out contextual regime-selection data and valid development/test separation.
- `FM80`: requires prospective naturalistic mathematics↔science transfer in >=3 domains and independent adjudication.
- `FG90`: genuine open-problem exploration; no claimed solution without independent formal/empirical verification.

## 6. FM70 contextual selector

Do not train on the same confirmatory outcomes later used for testing.

Required before execution:

- pre-outcome task features frozen;
- development folds and held-out folds fixed;
- valid SIMPLE/F0/F2 outcomes available;
- no result-conditioned feature engineering;
- resource accounting bound.

Compare prospectively frozen selector against:

```text
always-SIMPLE
always-F0
always-F2
ABSTAIN where warranted
```

The selector survives only if it improves the held-out quality-resource frontier without simple-task regression or missed critical escalation.

## 7. SD recursive scientific-development programme

Canonical executable backlog:

```text
research/experiments/SCIENTIFIC_DEVELOPMENT_EXECUTION_BACKLOG_V1.json
```

Sequence:

```text
SD00 reference preflight
SD10 real corpus + bias audit
SD20 operator discovery
SD30 matched success/failure contrast
SD40 held-out field + epoch
SD50 recursive abstraction levels
SD60 reproduce/challenge science-of-science regularities
SD70 fresh generated meta-policy
SD80 prospective naturalistic >=3 domains
SD90 recursive stability / hostile omission
```

### SD10 source boundary

Use source-specific lawful acquisition adapters to emit source-bound observations, then assemble/normalize through the existing contracts. Do not infer validated success/failure from citation, fame, prize, disruption or attention metrics. Validated outcomes require explicit witnesses.

### SD70 generated benchmark

```bash
python scripts/run_scientific_development_meta_suite.py prepare \
  --workdir RUN_SD70 \
  --tasks 120 \
  --train-episodes 16 \
  --arms TARGET_ONLY_DIRECT,FIXED_META_HEURISTIC,F0_PARENT_FEDERATION,F2_STATIC_NO_RECURSION,F2_RECURSIVE_META_DISCOVERY_FULL

python scripts/run_scientific_development_meta_suite.py dispatch \
  --workdir RUN_SD70 \
  --arms TARGET_ONLY_DIRECT,FIXED_META_HEURISTIC,F0_PARENT_FEDERATION,F2_STATIC_NO_RECURSION,F2_RECURSIVE_META_DISCOVERY_FULL \
  --max-concurrency 2

python scripts/run_scientific_development_meta_suite.py evaluate \
  --workdir RUN_SD70 \
  --arms TARGET_ONLY_DIRECT,FIXED_META_HEURISTIC,F0_PARENT_FEDERATION,F2_STATIC_NO_RECURSION,F2_RECURSIVE_META_DISCOVERY_FULL
```

Or:

```bash
bash scripts/run_scientific_development_meta_pilot.sh RUN_SD70
```

A population regularity is not a causal discovery principle. SD80 prospective naturalistic use is required for the stronger meta-policy claim.

## 8. Result import is frozen before outcomes

Use:

```text
papers/pipeline/RECURSIVE_DEVELOPMENT_RESULT_IMPORT_MAP_V1.json
papers/pipeline/PORTFOLIO_CLAIM_EVIDENCE_LEDGER_V3_RECURSIVE_DEVELOPMENT_DELTA.json
papers/pipeline/POST_RESULT_IMPORT_AND_R4_PLAYBOOK_V1.md
```

Do not let a model decide after seeing results which paper a result supports.

For every result:

1. validate run identity, hashes, oracle/custody boundary and source commit;
2. separate infrastructure invalidity from scientific outcome;
3. reproduce the registered primary analysis;
4. retain negative results, parent wins, simple wins, ties and `CANNOT_CHECK`;
5. run only frozen/legitimate sensitivity analyses;
6. apply #47 if a registered revision trigger fires;
7. update additive claim/evidence ledger;
8. update the predeclared manuscript/result block;
9. run hostile editor/reviewer and paper-completion gates;
10. never promote R3/R4 from prose completion alone.

## 9. Paper consequences

### P-A

FM transfer/obstruction and later naturalistic transfer can support or contract structural donor discovery. Strongest retrieval/structure-mapping/formal-parent sufficiency is a valid terminal.

### P-B

FM formal composition/obstruction/equivalence results are central inputs. P-B becomes stronger only if it adds a protected residual beyond native relation formalisms.

### P-C

E30/E60 and FM70 are decisive for minimum-sufficient activation. The adverse E20 pilot remains visible. A simple/F0 sufficiency result is publication-relevant and may contract full F2.

### P-D

Representation equivalence/dependence effects enter only when assurance/evaluator studies support them.

### P-E/P-F/P-G

Merge/drop aggressively if the new hierarchy or decisive evidence subsumes their independent thesis.

### Flagship

Write last. SD/FM/FG generated evidence alone cannot found the field. The flagship must continue to allow F0/F1/F3, contextual F2, contraction, deceptive unification or unresolved terminals.

## 10. Completion target

The computation session is finished only when each runnable internal lane has an honest terminal and each surviving paper has either:

- protected R3-level evidence appropriate to its scope;
- a negative/parent-sufficiency/resource result strong enough to survive as a paper;
- a merge/drop terminal; or
- an explicit external/resource `CANNOT_CHECK`.

The final objective is the smallest scientifically justified portfolio, not the maximum paper count.

## 11. Machine-readable umbrella

Use:

```text
research/experiments/V2_COMPUTATION_ONLY_SUCCESSOR_BACKLOG_V1.json
```

as an index. The canonical protected identities remain in their owning protocols/issues; this file must not be used to overwrite them.

# Machine Epistemics — Parent Recovery: Model Discovery, AutoResearch and Process-Level Failure V1

**State date:** 2026-09-01  
**Status:** hostile parent-recovery artifact; no novelty/field authority  
**ORION-V2 base:** `4165dd2d3c621d9f60e0ff492560baf3afbf7c5f`

## 0. Purpose

This pass gives three contemporary 2026 research lines their strongest reasonable interpretation before Machine Epistemics claims obstruction diagnosis, metacognitive process control, model-family expansion or long-horizon research-workflow evaluation:

1. Kevin Murphy, **Model Discovery Agent: LLM-assisted Bayesian experiment design for data-efficient discovery of mechanistic world models**, arXiv:2608.09696, submitted 2026-08-10.
2. Guiyao Tie et al., **AutoResearch AI: Towards AI-Powered Research Automation for Scientific Discovery**, arXiv:2605.23204, submitted 2026-05-22.
3. Yanlin Fei et al., **How Do Agents Fail on AutoResearch: End-to-End Diagnostic Evaluation on 100 Real-World Frontier Research Tasks**, arXiv:2608.14905, submitted 2026-08-14.

Disposition labels:

- `PARENT_RECOVERED` — do not use as a Machine Epistemics novelty carrier.
- `PARTIAL_OVERLAP` — direct neighbor, narrower/different scope.
- `EXTERNAL_BENCHMARK_CANDIDATE` — useful independent challenge set for an ME hypothesis.
- `RESIDUAL_CANDIDATE_ONLY` — possible residual after this parent, still requiring broader parent recovery and protected evidence.

---

## 1. Model Discovery Agent reconstruction

MDA addresses mechanistic world-model discovery in an **M-open** setting. It couples:

- an LLM proposer of candidate mechanistic structures;
- sequential Monte Carlo for parameter/structure posteriors;
- simulation-based inference where likelihoods are intractable;
- Bayesian value-of-information experiment design.

The critical loop is:

1. fit/evaluate the current hypothesis family;
2. use predictive checks to detect that the family is inadequate;
3. propose an expanded model/hypothesis class;
4. design interventions that discriminate candidate mechanisms efficiently;
5. use residual unexplained structure to support further discovery.

The paper reports three benchmark domains—physics, chemistry and biology—and claims improved data-efficient model learning/interventional forecasting.

### 1.1 MDA <-> ORION mapping

| ORION candidate | MDA parent object | Recovery | Consequence |
|---|---|---|---|
| model-family inadequacy trigger | predictive check flags current hypothesis-class inadequacy | `PARENT_RECOVERED_HIGH` | `MODEL_FAMILY_INADEQUACY` is not an ME novelty. |
| model/hypothesis expansion | LLM proposes new model structure in M-open setting | `PARENT_RECOVERED_HIGH` | “expand hypothesis space when current family fails” is parent/neighbor-owned. |
| prospective discriminator | VoI-designed experiments discriminate mechanisms | `PARENT_RECOVERED_HIGH` | discriminating experiments after model expansion are parent-owned. |
| active epistemic action | experiment choice optimized for information | `PARENT_RECOVERED_HIGH` | generic epistemic-action/VoI framing is not distinctive. |
| residual-driven iterative discovery | remaining unexplained residuals trigger further proposals | `PARENT_RECOVERED` | repeated residual-to-discovery loop has direct contemporary precedent. |
| representation insufficiency | MDA expands model structures, not necessarily representational language/operators broadly | `PARTIAL_OVERLAP` | ME must distinguish model-family from representation/formalism failure with decisive cases. |
| evaluator/measurement blindness | predictive checks are central, but a general hierarchy distinguishing bad model from bad measurement/evaluator is not the main object | `RESIDUAL_CANDIDATE_ONLY` | must compare with measurement/VVUQ/diagnosis parents. |
| minimum intervention level | MDA's main high-level response is model-space expansion plus designed experiments | `PARTIAL_OVERLAP` | ME-X2 must show when *not* to expand model space and which other intervention level is minimal. |
| external authority | not the core formal object | `RESIDUAL_CANDIDATE_ONLY` | governance parent recovery still required. |
| selective support reopening | not the main mechanism | `RESIDUAL_CANDIDATE_ONLY` | TMS/assurance remains stronger parent. |

### 1.2 MDA contraction

Do not claim novelty for:

`detect current model class failure -> expand model family -> choose informative intervention -> iterate on residuals`.

The strongest candidate left is **differential obstruction diagnosis across qualitatively different failure families**, with a minimum-responsible-level decision that can select model expansion *or reject it as unnecessary/wrong*.

---

## 2. AutoResearch AI reconstruction

AutoResearch AI is a broad workflow-level survey/programme of AI-powered research automation. It explicitly organizes scientific automation across:

- literature/research grounding;
- hypothesis formation and planning;
- experimentation and tool use;
- feedback, validation and review;
- reporting and knowledge communication.

It highlights unresolved system-level bottlenecks including evidence preservation, reproducibility, weak-direction rejection, provenance, cross-domain robustness and accountable scientific closure, and proposes evaluation dimensions including novelty, validity, impact, reliability and provenance.

### 2.1 AutoResearch <-> ORION mapping

| ORION/public ME theme | AutoResearch ownership/collision | Recovery |
|---|---|---|
| transition from isolated AI tasks to long-horizon research workflows | explicit central framing | `PARENT_RECOVERED_HIGH` |
| workflow-level evidence preservation | explicit bottleneck | `PARENT_RECOVERED_AS_PROBLEM` |
| provenance and reproducibility | explicit bottlenecks/evaluation concerns | `PARENT_RECOVERED_AS_PROBLEM` |
| validation/review across research loop | explicit workflow condition | `PARENT_RECOVERED_AS_PROBLEM` |
| accountable closure | explicit bottleneck | `PARENT_RECOVERED_AS_PROBLEM` |
| domain-conditioned autonomy | explicit conclusion | `PARENT_RECOVERED_AS_PROBLEM` |
| exact cross-transition formal semantics | survey maps problem landscape rather than establishing one universal transition calculus | `RESIDUAL_CANDIDATE_ONLY` |
| strongest-parent demarcation / contraction | not the survey's central object | `RESIDUAL_CANDIDATE_ONLY` |

### 2.2 AutoResearch contraction

Machine Epistemics must not sell the following as its central discovery:

> AI science is moving from task-level assistance to workflow-level automation, creating problems of evidence, validation, provenance, reliability and closure.

That problem statement is already explicit in AutoResearch and adjacent literature.

The possible ME contribution must be a **formal/empirical discriminator or control law**, not simply a more elaborate workflow taxonomy.

---

## 3. AutoResearchEval / ARFT reconstruction

AutoResearchEval is unusually important because it is **process-level empirical evidence** rather than only a programme proposal. The authors report:

- 100 real-world frontier research tasks;
- seven scientific domains;
- end-to-end lifecycle stages including ideation, retrieval, execution, analysis, writing and review;
- eight harness-model combinations;
- 800 complete agent trajectories;
- a 45-pattern AutoResearch Failure Taxonomy (ARFT);
- human-calibrated trajectory/artifact judging.

The reported failure patterns converge on the limitation that current agents lack a **metacognitive loop**: checking produced work against evidence, revising when it does not hold up, and questioning whether the path itself is sound. The paper states that whether orchestration-level interventions can close this deficit is open.

### 3.1 AutoResearchEval <-> ORION mapping

| ORION candidate | ARFT/AutoResearchEval collision | Recovery |
|---|---|---|---|
| current research agents fail at process level, not only output level | direct empirical result | `PARENT_RECOVERED_HIGH` |
| systematic scientific-agent failure taxonomy | 45 empirical failure patterns | `PARENT_RECOVERED_HIGH_AS_BENCHMARK` |
| need for metacognitive loop | direct headline interpretation | `PARENT_RECOVERED_HIGH_AS_PROBLEM` |
| checking output against found evidence | central stated deficit | `PARENT_RECOVERED_HIGH_AS_PROBLEM` |
| revise when result does not hold up | central stated deficit | `PARENT_RECOVERED_HIGH_AS_PROBLEM` |
| question whether path/process was sound | central stated deficit | `PARENT_RECOVERED_HIGH_AS_PROBLEM` |
| explicit obstruction taxonomy mapping failures to minimum intervention levels | ARFT diagnoses failures but does not, from the abstract-level reconstruction, establish an ORION-style intervention lattice or prove orchestration benefit | `EXTERNAL_BENCHMARK_CANDIDATE` |
| cross-transition support/evaluator/transport/authority semantics | not established merely by ARFT | `RESIDUAL_CANDIDATE_ONLY` |

### 3.2 External benchmark opportunity

ARFT creates a high-value hostile path for ME-X2/ME-X5:

1. map ORION obstruction classes to ARFT failure patterns **without changing ORION classes after protected labels are viewed**;
2. allow `NO_MAPPING` and `MULTI_CAUSAL` rather than forcing every ARFT pattern into ORION vocabulary;
3. test whether obstruction classification predicts a better intervention than B3/B5 baselines;
4. test on complete trajectories/intermediate artifacts, not only final-answer labels;
5. treat failure patterns that do not map cleanly as evidence against a universal ME taxonomy.

If ORION's obstruction classes merely rename ARFT clusters and do not improve intervention choice, ME gains no mechanistic residual.

---

## 4. Strong combined parent baseline after this pass

For obstruction/control studies, the parent comparator must now permit the following composition:

`process-level failure detector / ARFT-like taxonomy`

`+ predictive model adequacy checks`

`+ M-open LLM model proposer`

`+ Bayesian/VoI experiment design`

`+ provenance/verifier runtime`

`+ TMS/assurance/measurement/transport modules as required`.

Ordinary engineering glue and shared state are allowed. Machine Epistemics cannot define B5 as independent modules that are forbidden to communicate.

---

## 5. Surviving obstruction/control residual after recovery

The strongest hypothesis left is narrower:

> **Given similar observed research failure, can a machine classify the decision-relevant obstruction family and choose the minimum responsible intervention level more reliably/cost-effectively than an information-matched composition of process-failure diagnosis, metareasoning, M-open model discovery and domain-native controls?**

This requires discriminating cases such as:

- more search is enough vs model expansion is needed;
- model expansion is tempting but measurement/evaluator failure is causal;
- representation change is needed vs a missing premise is enough;
- experiment acquisition is useful vs current candidates are not identifiable with the available instrument;
- workflow/tool change is required vs local repair is sufficient;
- scientific result is unresolved and no justified intervention is currently available.

The residual is a **decision problem**, not ownership of the word “metacognition”.

---

## 6. Protocol consequences

### ME-X2

Add `ARFT_OR_EQUIVALENT_PROCESS_FAILURE_BASELINE` to B5.

Pre-register:

- ARFT-to-ORION mapping protocol;
- `NO_MAPPING`/`MULTI_CAUSAL` outcomes;
- whether intervention choice, not taxonomy agreement, is the primary endpoint;
- decoys where model expansion is specifically the wrong action.

### ME-X5

Prefer at least one external/native case family derived from real agent trajectories or independently authored scientific failure episodes. ORION-authored synthetic cases alone cannot establish a field residual.

### Flagship

Do not imply that Machine Epistemics uniquely identifies the need for process-level/metacognitive control in scientific agents. Phrase the field residual as a hypothesis about **cross-transition scientific decisions beyond contemporary failure-analysis and parent-control systems**.

---

## Current terminal

```text
MODEL_FAMILY_INADEQUACY_DETECTION = PARENT_RECOVERED
M_OPEN_HYPOTHESIS_EXPANSION = PARENT_RECOVERED
VOI_DISCRIMINATING_EXPERIMENTS = PARENT_RECOVERED
LONG_HORIZON_WORKFLOW_ASSURANCE_PROBLEM = PARENT_RECOVERED
PROCESS_LEVEL_AGENT_FAILURE_TAXONOMY = PARENT_RECOVERED
METACOGNITIVE_LOOP_AS_PROBLEM = PARENT_RECOVERED
ARFT = EXTERNAL_BENCHMARK_CANDIDATE
MINIMUM_RESPONSIBLE_INTERVENTION_SELECTION = RESIDUAL_CANDIDATE_ONLY
CROSS_TRANSITION_WARRANT_COUPLING = RESIDUAL_CANDIDATE_ONLY
FIELD_STATUS = UNRESOLVED
```

# Computational Scientific Control: A Systems Science of Machine-Mediated Inquiry

**Manuscript V0 — programme synthesis / field-hypothesis paper**

**Status:** draft only. This manuscript does not create an additional ORION-V2 paper identity, establish a new field, or grant scientific/novelty/publication authority. It may later serve as an overview/monograph, or absorb specialist papers if the contracted publication programme chooses one flagship instead of multiple papers.

## Abstract

Artificial intelligence is rapidly making the scientific process executable. Systems now retrieve literature, formulate hypotheses, design experiments, run code and laboratory procedures, analyze results, draft manuscripts, and perform automated review. Yet scientific automation exposes a gap between *doing research tasks* and *controlling scientific state*. A pipeline may execute successfully while silently changing its criterion, losing source identity, double-counting dependent evidence, confusing infrastructure failure with scientific falsification, invalidating earlier claims without reopening them, or stopping because output appears flat while search remains censored. Existing fields own most component techniques: AI for Science and self-driving laboratories own domain automation; control and decision theory own sequential action under uncertainty; formal methods own specification and verification; provenance and workflow systems own reproducibility and execution lineage; metascience and philosophy of science own evidence, scientific practice and epistemic authority. We ask whether a residual scientific object remains: the controlled transition from uncertainty to warranted, replayable and authority-bounded scientific commitments.

We call the provisional object **Computational Scientific Control (CSC)**. We formalize a scientific control episode using problem contracts, plural scientific state, active obligations, admissible actions, resources, provenance/dependence, evaluation contracts, observations and append-only transition history. We propose ten invariants: contract conservation, evidence binding, non-amplifying authority, conservative transport, support-aware reopening, execution/science failure separation, visible censoring, bounded stopping, replay identity and honest unresolved terminals. We then derive a research programme around epistemic observability, scientific controllability, minimal escalation, dependence-aware evidence, selective reopening, context-relative relation transport and bounded saturation. ORION-V2 is presented only as one candidate reference architecture. The field hypothesis is falsified if strongest parent-composed systems reproduce all protected decisions without material loss, if the proposed invariants reduce to ordinary software correctness, or if cross-domain benchmarks cannot be constructed without ORION-specific vocabulary. The central thesis is therefore not that a new science already exists, but that machine-mediated inquiry has made the scientific control loop sufficiently explicit to be studied as a candidate systems science in its own right.

## 1. Introduction

Scientific practice has always involved feedback: observe, hypothesize, test, update, and decide what to do next. What is changing is the granularity and speed at which this feedback loop can be externalized into software. Recent end-to-end AI-scientist systems, multi-agent scientific-discovery systems and self-driving laboratories increasingly automate long chains of scientific actions. Autonomous laboratories combine adaptive experiment selection with physical execution. Agentic systems combine literature search, analysis, hypothesis generation, coding and review. AI-for-Science surveys increasingly describe full scientific agency rather than isolated prediction tasks.

These advances create a paradox. The more of science becomes executable, the more dangerous it becomes to treat scientific correctness as an emergent property of a well-running workflow. Software success, model confidence, provenance integrity, benchmark scores and reviewer agreement are each weaker than scientific warrant. A generated result can be internally consistent and reproducible while answering the wrong question. An evaluator can be stable yet dependent on the same hidden source as the subject. A complete trace can document a scientifically invalid transformation perfectly. A system can produce a plausible paper while its search process was censored. A new model can improve a benchmark while invalidating prior claims that remain marked as verified.

The core problem is therefore a **control problem over epistemic state**, but not an ordinary control problem. The state includes claims, evidence, uncertainty, source identity, representations, search coverage, active obligations, authority and provenance. Some coordinates are non-compensatory: a lower false-completion rate cannot justify silent criterion mutation; higher expected utility cannot compensate for absent authority; faster progress cannot turn missing evidence into a pass.

This paper develops the hypothesis that these coupled constraints define a useful scientific object: **Computational Scientific Control** (CSC), the study and engineering of controlled transitions from scientific uncertainty to warranted, replayable, authority-bounded commitments.

Our contributions are deliberately conditional:

1. we reconstruct neighboring ownership and define a residual object rather than claim generic “AI science”;
2. we propose a minimal state-transition model for machine/hybrid inquiry;
3. we identify ten candidate invariants and associated hostile controls;
4. we define theoretical problems in observability, controllability, dependence, escalation, reopening and stopping;
5. we outline a cross-domain empirical programme and non-compensatory metrics;
6. we position ORION-V2 as a falsifiable reference architecture rather than the definition of the field;
7. we state explicit rejection criteria for the field hypothesis.

## 2. What neighboring fields already own

### 2.1 AI for Science and agentic science

AI for Science already covers scientific prediction, generative modeling, scientific foundation models, autonomous research agents, domain-specific scientific workflows and increasingly end-to-end discovery. A CSC claim that “AI can automate science” would be redundant.

CSC instead asks: when an automated system changes a scientific commitment, what state was changed, what evidence warranted the transition, what prior commitments were affected, what authority permitted the change, and how can the same transition be replayed or challenged?

### 2.2 Self-driving laboratories and active learning

Self-driving laboratories supply perhaps the closest operational parent. They already implement closed-loop experiment selection, robotics, measurement and adaptive modeling. Their recent development emphasizes scale, generality and provenance-complete experimentation.

CSC attempts to generalize the *control semantics* beyond experimental optimization. Scientific inquiry also changes representation, search vocabulary, method, decomposition and evidence structure; it may rely on formal proof, literature synthesis, human review, simulation or unavailable external resources. A general control layer must distinguish these modes rather than reduce them to one reward function.

### 2.3 Control theory and sequential decision-making

Control theory supplies state, action, dynamics, feedback, observability, controllability and stability. POMDPs, Bayesian decision theory, active learning and metareasoning supply decisions under uncertainty and information-acquisition policies.

CSC inherits these tools but adds scientific hard constraints. A policy is not scientifically admissible merely because expected utility is high. The policy must respect criterion identity, evidence provenance, authority ceilings, preserved commitments and unresolved/censored search routes.

### 2.4 Science of Science and metascience

Science of Science studies the large-scale production and organization of scientific knowledge, while metascience studies reliability, reproducibility, incentives and methodology. CSC is complementary: the target is an executable research episode and its controlled internal state transitions.

A future mature programme should connect the scales: local scientific-control rules may create population-level effects in publication, replication, novelty and research allocation, while metascientific evidence should constrain local controller design.

### 2.5 Philosophy of science and epistemology

CSC depends on philosophical distinctions rather than replacing them. Evidence, explanation, underdetermination, model pluralism, epistemic authority and scientific values are not software inventions. The contribution, if any, is operational: make these distinctions explicit enough to test whether a machine/hybrid process preserved them.

### 2.6 Formal methods, knowledge representation and provenance

Formal methods can prove properties under specifications. Provenance standards such as W3C PROV record entities, activities and derivations. Workflow systems provide durable/replayable execution.

CSC combines but does not conflate them. Provenance proves how an artifact arose; it does not prove the scientific semantics were correct. A formal proof may be valid under assumptions that do not hold in the target system. A workflow can be perfectly reproducible while reproducing an invalid criterion.

## 3. Scientific control episodes

We model a scientific control episode as

`E_t = (P_t, S_t, O_t, A_t, R_t, M_t, V_t, X_t, H_t)`.

`P_t` is the problem contract, including question, scope, criterion, protected constraints and target authority. `S_t` is plural scientific state: claims, alternative hypotheses, uncertainty, representations and search universe. `O_t` contains active obligations. `A_t` is the admissible action family. `R_t` contains resources and capabilities. `M_t` contains memory, provenance and dependence. `V_t` defines evaluator/validation contracts. `X_t` contains external observations. `H_t` is append-only history.

A policy proposes `a_t ∈ A_t`. Execution produces raw result `x_t`. An interpreter decides whether `x_t` is admissible evidence and how it changes state. A transition can therefore fail at several distinct levels:

- the action was not authorized;
- execution failed;
- the output violated its schema;
- the result was scientifically uninterpretable;
- the result provided evidence for or against a claim;
- the result changed a premise and forced selective reopening;
- the result exposed that the current action/representation space is insufficient.

This decomposition is important because a single Boolean `success` cannot represent all of these.

## 4. Ten candidate invariants

### 4.1 Contract conservation

A scientific system must bind the problem, criterion and evaluator identity used for a result. Silent criterion changes invalidate comparison. Disclosed changes may be scientifically legitimate, but they create new identities or require explicit deviation records.

### 4.2 Evidence binding

Evidence must bind to the content/source/execution actually observed. Merely naming a source, query family, experiment or file is insufficient.

### 4.3 Non-amplifying authority

Scientific support and authority are distinct. A model may generate a correct claim without authority to adopt it. A reviewer may provide evidence without authority to publish or change protected state. Derived authority cannot exceed its valid roots.

### 4.4 Conservative transport

Scientific objects can be comparable in one context and not another. Approximate transport cannot silently become exact equivalence. Every mapping should state context, witnesses, loss/uncertainty, validity window and counter-probes.

### 4.5 Support-aware reopening

When a premise changes, dependent commitments lacking an independent surviving support family must reopen. Unaffected commitments should remain closed.

### 4.6 Execution/science failure separation

Tool failure, timeout, missing provider, parser failure or sandbox error is not a scientific negative unless the scientific contract explicitly makes that event evidential.

### 4.7 Visible censoring

Unsearched, failed or unavailable routes remain visible. Censoring cannot become evidence of absence.

### 4.8 Bounded stopping

Flat output is not saturation. A stopping claim binds the search basis, coverage, residual uncertainty, censoring and omission challenge.

### 4.9 Replay identity

Protected scientific comparison requires exact identity across subject version, case, criterion, evaluator, provider/tool configuration, resource budget and randomization when applicable.

### 4.10 Honest unresolved terminal

`CANNOT_CHECK` is a valid scientific-control outcome. Missing identity, evidence, authority or evaluation cannot be averaged into a pass.

## 5. Theory: from control to scientific control

### 5.1 Epistemic observability

Ordinary observability asks whether internal state can be inferred from outputs. Scientific observability asks whether the cause of a scientific residual is identifiable from current evidence. Missing evidence, representation insufficiency, model capacity and infrastructure failure can produce similar visible symptoms.

A scientific controller should therefore maintain a responsibility hypothesis set and select discriminating observations when multiple causes remain possible.

### 5.2 Scientific controllability

Scientific controllability concerns which warranted states are reachable under available methods, resources and authority. A claim might be true in the world yet unreachable under current tools or evidence. Conversely, a result may be computationally reachable but scientifically inadmissible.

### 5.3 Minimal sufficient escalation

Scientific systems often respond to failure by increasing model size, adding tools or changing representation. CSC treats escalation as a controlled intervention. A valid escalation should demonstrate why lower-level alternatives are insufficient and choose the lowest sufficient level. This produces two measurable errors: false escalation and missed escalation.

### 5.4 Dependence-aware evidence

Evidence combination is invalid when hidden common causes are treated as independence. Dependence may arise from shared data, models, prompts, instruments, evaluators, transformations or literature roots. Support should therefore be represented as families/hypergraphs rather than counts alone.

### 5.5 Selective reopening

The state transition problem after a change is not “rerun everything.” It is to identify the minimal set of claims whose support is no longer valid. This is naturally a dependency/support graph problem with potential theorem-level results.

### 5.6 Context-relative transport

Scientific reuse across models, versions or domains requires explicit relation type. Bisimulation, measurement invariance, causal transport, abstract interpretation and metrology already provide parent-specific theories. CSC asks how a controller chooses and composes these relation families without collapsing them into one generic similarity score.

### 5.7 Bounded epistemic stopping

Stopping is an information/control decision. A controller must balance diminishing expected value against the risk of omitted routes, changed vocabulary and false closure. The stopping theorem cannot be universal; it is conditional on a declared search basis and resource/censoring model.

## 6. A minimal engineering architecture

A candidate CSC implementation requires only seven interface families:

1. contracts, identities, obligations and typed terminals;
2. plural scientific state;
3. context-relative relation/transport;
4. evidence, dependence, provenance and revalidation;
5. action selection and responsibility diagnosis;
6. opportunity and witnessed minimum escalation;
7. evaluation, parity, saturation and authority.

Everything else should remain parent-owned when possible: retrieval engines, Bayesian optimization, workflow schedulers, theorem provers, causal packages, graph libraries, provenance stores and domain algorithms.

This is the current ORION-V2 contraction hypothesis. A smaller parent composition that preserves all protected decisions would falsify parts of the architecture.

## 7. Benchmark design

A CSC benchmark should not reward one scalar success score. It should contain paired cases where average task accuracy is insufficient.

### 7.1 Contract cases

An unchanged problem, a disclosed legitimate criterion change, and a hidden relaxed criterion should produce different terminals even if final answers are identical.

### 7.2 Search cases

Compare complete search, censored search and wrong-vocabulary search. The system must not infer absence from the latter two.

### 7.3 Semantic cases

Use passages with same words/different scientific structure and different words/same registered structure. Require recoverable source projection.

### 7.4 Reconstruction cases

Include local compatibility with global inconsistency and multiple justified portraits. Test whether the controller preserves plurality rather than forcing one answer.

### 7.5 Diagnosis cases

Include single fault, multiple faults, interaction-only faults and non-identifying evidence. Measure discriminator choice, not only final repair.

### 7.6 Reopening cases

Invalidate one support path while preserving another. A sound system should reopen only the claims that lost all valid support.

### 7.7 Saturation cases

Create flat growth under full coverage versus flat growth with one censored route. Only the first can qualify for bounded saturation.

### 7.8 Evaluation cases

Create provenance-identical but scientifically wrong results, same-source reviewers, post-outcome criterion mutation and blinded independent review.

### 7.9 Execution cases

Create timeouts, nonzero exits, bounded-output pressure, retries, process cleanup and invalid successful payloads. These test the boundary between computational execution and scientific state.

## 8. Metrics and non-compensation

Primary coordinates:

- false completion;
- scientific known-answer/validity;
- authority/integrity violations;
- semantic/provenance preservation;
- `CANNOT_CHECK` calibration;
- selective reopening correctness;
- coverage/censoring correctness;
- replay identity.

Secondary coordinates:

- cost;
- latency;
- decisive-probe efficiency;
- unnecessary work;
- unnecessary escalation;
- justified reachability gain.

A primary failure cannot be compensated by a secondary improvement. This is crucial: a system that is twice as fast but silently changes the criterion has not improved scientific control.

## 9. ORION-V2 as reference instrument

ORION-V2 is useful because it makes the proposed state distinctions executable, but it is not evidence that the field exists. The correct experimental posture is adversarial:

- bind frozen V1 capability parity;
- compare against strongest parent-composed baselines per campaign;
- include simple direct controls to detect unnecessary orchestration;
- use protected case/evaluator custody;
- preserve per-cell results so averages cannot hide lost capabilities;
- require fresh-domain cases that were not used to construct the architecture.

If ORION-V2 loses to simpler parent compositions while preserving no unique protected decision, the corresponding V2 mechanism should be removed.

## 10. Prospective field test

We propose one flagship prospective experiment.

### Question

Can a generic scientific controller improve the reliability and efficiency of a real research episode in a fresh domain without domain-specific controller tuning?

### Design

Choose a domain not used in ORION-V2 construction. Freeze:

- a problem contract;
- source/tool access;
- time/compute budget;
- domain expert adjudication;
- parent-composed baseline;
- V1 and V2 subjects;
- protected evaluation criteria.

Run at least four arms:

1. expert/direct workflow;
2. strongest parent-composed automation;
3. frozen V1;
4. contracted V2.

Measure not only scientific outcome but false completion, decisive evidence cost, criterion drift, evidence dependence, reopen correctness, authority behavior and stopping.

### Success condition

A field-supporting result requires at least one material cross-domain control advantage that cannot be reproduced by the parent composition, with no mandatory-coordinate regression.

## 11. Field falsifiers

The CSC hypothesis should be rejected or downgraded to an integration discipline if:

- parent fields already provide the same protected decisions under composition;
- the state variables do not improve prediction/control of scientific failure;
- benchmarks require ORION-specific vocabulary;
- independent experts cannot reproduce evaluator decisions;
- the controller adds verification burden without reducing false completion or increasing justified reach;
- theoretical results reduce to known graph/workflow/control theorems under relabeling;
- semantic or authority coordinates cannot be operationalized consistently.

## 12. Research agenda

### Theory

- formal selective-reopen minimality;
- scientific-control observability under multiple failure causes;
- minimum escalation under action-space insufficiency;
- dependence-aware evidence certificates;
- stopping bounds under censored heterogeneous routes;
- relation composition under approximate/error-bounded transport.

### Systems

- interoperable scientific receipts;
- protected evaluator/case custody;
- parent adapters for retrieval, experimentation, provenance and durable execution;
- benchmark harnesses that separate scientific and execution failure.

### Empirics

- cross-domain naturalistic studies;
- longitudinal evaluator drift;
- prospective problem-finding value;
- human/AI delegation and responsibility;
- verification-cost measurement in AI-generated science.

### Institutions

- how protected evaluation should work when AI can read public benchmarks;
- how publication authority should be separated from automated reviewer scores;
- how research artifacts can expose assumptions/dependence without making science prohibitively bureaucratic.

## 13. Implications

The deepest implication is methodological. AI makes scientific generation cheap enough that the limiting resource may shift toward **verification, discrimination and justified state transition**. If so, scientific infrastructure should be designed less like a document-production pipeline and more like a controlled system whose important state is externally inspectable.

That does not mean automating epistemic authority. It means making authority, evidence and uncertainty harder to accidentally erase.

## 14. Conclusion

Machine-mediated science is rapidly approaching full-cycle automation, but full-cycle execution is not full-cycle scientific control. A scientific system can run end to end while still losing the distinctions that make its output trustworthy. We have proposed Computational Scientific Control as a provisional systems-science object centered on those distinctions and their transitions.

The hypothesis is intentionally falsifiable. Mature neighboring fields own nearly every component. CSC survives only if the *composition problem itself*—contract-bound, evidence-aware, provenance/dependence-aware, selectively revisable, authority-bounded and honestly stoppable scientific state transition—produces theory and protected empirical value not already obtained by straightforward parent composition.

The immediate task is therefore not to announce a discipline. It is to finish the protected parity and parent-comparator programme, build non-ORION benchmarks, prove at least one nontrivial transition result, and submit the field boundary to independent review.

**Current manuscript terminal:** `FIELD_HYPOTHESIS_WORTH_PROTECTED_TESTING`.

## References / literature anchors for revision

- Canty, R. B. & Abolhasani, M. (2026). *The past, present and future of self-driving laboratories*. Nature Reviews Chemistry.
- *Towards end-to-end automation of AI research* (2026). Nature.
- *A multi-agent system for automating scientific discovery* (2026). Nature.
- Wei, J. et al. (2025). *From AI for Science to Agentic Science: A Survey on Autonomous Scientific Discovery*. arXiv:2508.14111.
- Ma, J. W. (2026). *Toward an Engineering of Science: Rebalancing Generation and Verification in the Age of AI*. arXiv:2605.10425.
- Ratti, E. (2026). *Epistemic Control and the Normativity of Machine Learning-Based Science*. arXiv:2601.11202.
- Wojarnik, G. (2026). *Spec-Driven AI for Empirical Research: A Scoping Review and an Architecture of Epistemic Control*. SSRN 7073778.
- Liu, Y. & Zhang, Y. (2026). *AI Agents for the Science of Science: A Survey of Tasks, Architectures, Evaluations, and Challenges*. Findings of ACL 2026.
- W3C PROV family.
- Graßhoff, G. & May, M. (1995). *From Historical Case Studies to Systematic Methods of Discovery*.

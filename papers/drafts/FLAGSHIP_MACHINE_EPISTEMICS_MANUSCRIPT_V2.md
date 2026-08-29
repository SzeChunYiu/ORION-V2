# Machine Epistemics: The Control Science of AI-Driven Discovery

**Perspective draft V2**

## Abstract

Artificial intelligence is moving from isolated scientific prediction toward persistent research processes that search literature, propose hypotheses, choose experiments, call instruments and software, analyse results, revise models and generate scientific outputs. This shift makes a previously diffuse systems problem concrete: **when may a machine-mediated research process change what science commits to?** A workflow can execute correctly while supporting the wrong inference; multiple reviewers can agree while sharing the same hidden source; provenance can be exact while a scientific claim is false; an abstraction can preserve one decision while invalidating another; and a search can appear exhausted while decisive routes remain censored. We propose **Machine Epistemics** as a provisional field concerned with these controlled scientific-state transitions. Its object is not the AI model alone, but the bounded research episode in which evidence, representations, actions, resources, evaluators, history and authority interact. We organize the field around four problems: observing the epistemic state; controlling scientific transitions and transport; assuring evidence and authority; and governing escalation and closure. Mature fields already own most component mechanisms—from metareasoning and active experimentation to truth maintenance, diagnosis, formal abstraction, causal transport, provenance and metascience. The field hypothesis is therefore falsifiable: if information-matched compositions of these parents reproduce the same cross-domain scientific decisions, Machine Epistemics should remain integration engineering rather than a distinct science. We outline the formal, empirical and institutional tests required to decide that question.

## Scientific work is becoming an executable process

Artificial intelligence has long contributed to scientific prediction, simulation and pattern recognition. The more consequential recent transition is that **parts of the research process itself are becoming executable**. Autonomous chemistry systems can search documentation, plan procedures and control experimental hardware; autonomous materials laboratories combine literature-derived knowledge, computation, active learning and robotics; multi-agent systems now connect literature search, hypothesis generation and data analysis in experimental biology; and end-to-end research systems can generate ideas, run computational experiments, analyse outputs and draft manuscripts [1–7]. These systems remain heterogeneous and their scientific maturity varies widely, but together they change the unit of engineering concern. We are no longer evaluating only a model prediction or a laboratory instrument. We increasingly evaluate a sequence of machine-mediated decisions that changes the state of an investigation.

This change exposes failure modes that task accuracy alone does not describe. A literature system may retrieve genuine papers yet bind a claim to the wrong passage. A computational pipeline may replay perfectly yet reproduce an invalid analysis. Several apparently separate agents may agree because they share a model, dataset or retrieval corpus. A representation can be compressed without affecting one target decision but destroy a distinction needed later. A failed tool call can be mistaken for evidence against a scientific hypothesis. A benchmark can become easier to optimize after publication, changing what its score means. And a research agent can produce a plausible conclusion that exceeds the authority of its evidence or of the process allowed to adopt it.

These are failures of **scientific-state transition control**. They concern whether the transition from one scientific commitment state to another is warranted—not merely whether a software step completed or an answer looks reasonable.

We use the term **Machine Epistemics** for the proposed science and engineering of those transitions in AI-mediated and hybrid human–machine research. The phrase is deliberately narrower than the epistemology of artificial intelligence and broader than agent architecture. Machine Epistemics asks:

> Under what conditions may a machine-mediated research process change what it scientifically commits to, what must be preserved or reopened when it does so, and what authority can the new state legitimately possess?

This is a field hypothesis, not a declaration that a field has already been established.

## The object of study: a machine-epistemic episode

The basic object is a **bounded research episode** in which scientific commitments can change. Informally, an episode contains a problem or criterion, a current scientific state, unresolved obligations, possible actions, available resources and tools, evidence and provenance, validation procedures, observations from the world, a history of earlier transitions, and an authority boundary.

We denote this object

\[
E=(P,S,O,A,R,M,V,X,H,K),
\]

where \(P\) is the problem and criterion contract; \(S\) is the plural scientific state; \(O\) is the set of unresolved scientific obligations; \(A\) is the admissible action repertoire; \(R\) records resources and access; \(M\) records evidence identity, provenance, dependence and memory; \(V\) binds verification, validation and evaluator contracts; \(X\) contains observations and tool outputs; \(H\) is append-only history; and \(K\) denotes externally supplied authority and governance constraints.

The tuple is not intended as a universal ontology. Its purpose is to identify a recurring control boundary: **an action produces an observation or candidate transformation, not truth by itself**. A scientific transition requires an interpretation that is valid under the current evidence, semantics, dependencies, resources and authority constraints. The same execution output can therefore have different scientific consequences in different episodes.

This distinction becomes visible in several simple cases. A theorem prover returning a verified proof can justify a formal claim if the specification and checker are the right ones, but it does not automatically justify an empirical claim about nature. A laboratory robot completing a protocol establishes that an execution occurred; the scientific interpretation still depends on measurement quality, controls and the relation between the experiment and the target claim. A reproducible data pipeline establishes replay identity but not that the chosen analysis answers the intended question. And a high-scoring research benchmark establishes performance under a criterion, not permission to silently change that criterion after outcomes are known.

**Figure 1 | The machine-epistemic episode.** A conceptual figure should show a research episode as a sequence of proposed scientific-state transitions rather than a generic AI-agent workflow. Tool and experimental actions produce observations; interpretation gates determine whether a scientific commitment changes. Failure examples should show execution without evidence, provenance without correctness, correlated agreement without independence, and apparent closure with censored routes.

## Why existing fields do not automatically compose

Machine Epistemics would be unnecessary if an existing field already owned the complete object. Much of the required machinery is in fact mature, and any serious proposal must begin by crediting it.

Cybernetics and control theory study feedback, dynamics, observability and controllability. Decision theory, POMDPs and rational metareasoning study which action or computation to perform under uncertainty and resource limits; Russell and Wefald, for example, formalized the value of computations for bounded agents [17]. Active learning and optimal experimental design study informative measurements and experiments. Truth-maintenance systems and assumption-based TMSs record the reasons for beliefs, maintain alternatives and revise them after contradiction [14,15]. Model-based diagnosis identifies explanations for discrepancies and develops measurements that discriminate competing diagnoses [16]. Formal methods, bisimulation, abstract interpretation and program refinement supply powerful theories of proof, equivalence and safe abstraction. Causal inference studies identification and transport across environments. Metrology and psychometrics study traceability, calibration, invariance and linking. Provenance standards such as W3C PROV make lineage interoperable [18]. Evidence synthesis and meta-analysis address how multiple observations should combine. Performative prediction and related strategic-response theories formalize cases in which deployment changes the data-generating process [19]. Metascience and the science of science empirically study research systems, institutions, careers and discovery [10,11]. Philosophy of science and social epistemology provide essential normative analyses of evidence, explanation, understanding and authority.

AI for Science, agentic science and autonomous laboratories then supply the application substrate: systems in which many of these mechanisms can be assembled into research loops [1–7]. Verification-first autonomous catalysis, for example, explicitly argues that hypotheses should remain provisional until tool-grounded evidence and uncertainty-aware checks permit them to update workflow state [7]. That programme is a close parent of Machine Epistemics, not evidence that a separate field must exist.

The proposed residual lies in **composition-level scientific decisions** that cross the normal boundaries of these parents. Consider four examples.

First, provenance can establish exact lineage while scientific support fails. The correct response requires a relation between provenance, claim semantics and validation, not provenance alone. Second, metareasoning can select the computation with highest expected decision value while the scientific process still lacks authority to adopt the resulting claim. Authority is an external constraint on admissible transitions, not another utility term that the machine may optimize away. Third, formal abstraction can certify equivalence relative to one interface while a later scientific question depends on a distinction the abstraction discarded. Reuse therefore requires a context-bound transport claim and, when the context changes, selective revalidation. Fourth, an active search policy can stop a route efficiently while a scientific closure claim remains invalid because other routes were unavailable or the representation itself prevented a decisive query.

The scientific question is whether these cross-layer cases are merely inconvenient engineering interfaces or whether they exhibit stable, measurable laws across domains.

### What Machine Epistemics does not rename

The proposal explicitly does **not** rename feedback control, metareasoning, experiment design, truth maintenance, belief revision, model-based diagnosis, formal verification, causal transportability, measurement science, provenance, meta-analysis, systematic review, research methodology, metascience, AI for Science or philosophy of science. Each retains its native objects, methods and standards.

This demarcation is not ceremonial. New interdisciplinary labels can obscure older traditions: the 2019 proposal for “machine behaviour” in *Nature* was directly criticized for overlooking cybernetics [8,9]. Machine Epistemics should therefore survive only if its cross-domain transition object changes scientific decisions beyond an information-matched composition of mature parents.

**Figure 2 | Parent ownership and the composition gap.** The figure should map major parent fields to the scientific decisions they already own, then identify a small set of cross-layer transitions—such as provenance-to-validity, equivalence-to-reuse, evidence-to-authority and route-stop-to-scientific-closure—that constitute the field hypothesis. The figure should make parent subsumption visually possible, not depict Machine Epistemics as a superset that owns everything.

## Four control problems

A field needs a compact set of questions that can organize empirical studies, formal results and engineering systems. We propose four.

### 1. Observe the epistemic state

Before controlling a research process, the system must know which scientifically relevant distinctions are observable. What claims remain live? Which alternatives are empirically or formally distinguishable? Which evidence items share sources? Which search routes were attempted, failed or censored? Which representations are comparable under the current question? Which uncertainties are reducible by another observation and which are structurally non-identifiable?

This is an observability problem, but not only in the control-theoretic sense. Scientific observability includes source identity, semantic scope, dependence, coverage and the distinction between absence of evidence and evidence of absence. Model-based diagnosis and causal-identification theory already supply important special cases. A Machine Epistemics research question is whether a common representation of these distinctions improves decisions across heterogeneous research modes without erasing native semantics.

Testable problems include the minimum probe needed to distinguish two failure hypotheses; conditions under which evaluator outputs cannot identify whether a model or representation is responsible; and metrics for detecting when several validators provide less independent information than their count suggests.

### 2. Control and transport scientific transitions

A research system repeatedly proposes state changes: accepting a claim, revising a model, switching representation, transferring a result to a new domain, repairing a failed process or reopening an earlier conclusion. The central question is not whether change is possible, but **which scientific commitments survive it**.

Formal methods already provide exact and approximate relations; causal transportability formalizes when causal knowledge moves between populations; psychometric and metrological methods handle linking and traceability. Machine Epistemics treats the relation itself as a scientific object with a declared context, assumptions, preserved judgments, losses, error and expiry. An approximate relation valid for a control decision should not silently become exact equivalence for a high-precision scientific claim. Conversely, a changed representation should not trigger global invalidation when independent support remains.

This problem yields formal questions about conservative composition of transport relations, propagation of approximation error, and minimal selective reopening after a supporting relation expires.

### 3. Assure evidence and authority

Scientific systems need to distinguish **more evidence** from **more copies of the same evidence**. Shared datasets, prompts, model checkpoints, instruments, calibration procedures, literature corpora or human sources can make apparently independent confirmations strongly dependent. Provenance helps expose lineage but does not by itself quantify corroboration or scientific correctness.

Assurance also has an authority dimension. An automated checker, benchmark, reviewer or consensus process can support a claim under a criterion; it does not create institutional authority beyond the roots that issued or accepted that criterion. The relevant authority rules may come from laboratories, journals, regulators, collaborations or human investigators. Machine Epistemics does not derive those rules; it treats them as explicit constraints so that a machine cannot self-amplify its mandate.

A further complication is evaluator dynamics. When a benchmark, policy or scientific rule is published and optimized against, the environment may change. Performative prediction formalizes this phenomenon in supervised learning [19]. Scientific evaluation raises analogous questions: when does a previously valid evaluator cease to support the same inference after the evaluated ecosystem adapts?

Testable problems include calibration under known or partially observed dependence, selective survival of claims with alternative support families, and detection of evaluation regimes in which response invalidates a static pass.

### 4. Govern escalation and epistemic closure

Research systems also choose **how much to change** when progress stalls. A failed retrieval might require another query, a new source, a different model, a new measurement, a new representation or a reformulated problem. Escalating too early wastes resources and can destroy valid structure; escalating too late traps the system inside an inadequate search space.

Metareasoning, diagnosis, design theory and adaptive search provide strong parents for this problem. The Machine Epistemics question is whether scientific constraints support a general principle of **minimum sufficient escalation**: prefer the lowest intervention level capable of discharging the blocking scientific obligation while preserving valid commitments and exposing unresolved alternatives.

Closure is the dual problem. A search route stopping is not the same as the scientific task being closed. A system should be able to state what search universe, representation, evidence classes and omission challenges support its stop, and which routes remain censored. `Unresolved` or `cannot determine` must remain legitimate outcomes when the available process cannot establish what the decision requires.

This yields measurable research questions about false closure, missed escalation, unnecessary escalation, resource-adjusted justified reachability and the conditions under which finite stopping rules remain scientifically conservative.

**Figure 3 | Four control problems of Machine Epistemics.** The figure should connect observability, transition/transport, evidence/authority and escalation/closure around a bounded research episode. Each quadrant should show representative parent methods, one cross-layer failure, and two measurable research questions. The visual goal is a reusable field map rather than an architecture diagram.

## How the field hypothesis can be tested

A useful field cannot survive on terminology. Machine Epistemics needs formal and empirical programmes whose negative results can contract the proposal.

The strongest studies should use **known-answer and hostile cases** in which the correct scientific transition is independently specified. Examples include identical provenance with different validity; locally compatible evidence with a global inconsistency; observationally equivalent models that differ under intervention; repeated evidence with hidden common ancestry; a low-level repair that makes a larger representation change unnecessary; and a search that appears stable while a decisive route is censored. Such cases test whether systems preserve distinctions instead of merely producing plausible answers.

The second requirement is **cross-domain recurrence**. A transition abstraction that works only in one scientific area belongs to that area. A field-level claim should require at least two materially different domains—for example, a formal/computational domain and a measurement/experimental domain—to instantiate the same control object while preserving their native standards.

Third, comparisons should use **strong parent compositions**, not weak single baselines. If a combination of metareasoning, diagnosis, provenance, formal transport and existing evaluation infrastructure makes the same decisions under matched information and resources, then the integrated Machine Epistemics mechanism has no residual to claim.

Fourth, experiments should include **negative controls where added machinery must lose**. A direct calculation should not trigger elaborate diagnosis; independent evidence should not be rejected merely because dependence is possible; a stable evaluator should not be declared performative; and a valid local representation should not be replaced simply because a larger one exists.

Finally, scientific evaluation needs independent custody when semantic judgment is unavoidable. An AI system cannot establish the validity of its own evaluator merely by running it more times. Current Nature Portfolio policy similarly treats AI as supporting rather than replacing human scholarly judgment [20]. Machine Epistemics should formalize and test such boundaries rather than assuming that more automated review equals more scientific authority.

A field-level empirical terminal might therefore ask whether an integrated approach reduces false scientific completion, unsafe transport, dependence-induced overconfidence or unnecessary escalation **without** increasing unwarranted refusal or losing established capabilities. Failure on that test should narrow the field claim.

**Figure 4 | Falsifying the field hypothesis.** An optional figure should show the decision path: native parent reconstruction → strongest parent composition → cross-domain protected cases → residual scientific decision value. Positive evidence supports a candidate field; a tie or parent win yields `integration engineering`, and unresolved evidence yields no field claim.

## Barriers to a science of machine-mediated knowing

Several obstacles are scientific rather than merely technical.

**Ground truth is often unavailable.** In frontier research, the correct answer may not be known. Machine Epistemics therefore needs a layered evaluation strategy: exact known-answer cases for invariants; blinded expert adjudication for semantic transitions; prospective tests when future scientific value is claimed; and explicit `unresolved` states when no independent criterion exists.

**Dependence can be hidden.** Two agents may appear independent while sharing a foundation model or training data; two laboratories may share calibration or analysis software. Assurance must therefore represent unknown dependence rather than converting missing lineage into independence.

**Scientific objects change over time.** Datasets, instruments, ontologies, model versions and populations evolve. Persistent identity cannot substitute for comparability. Cross-version scientific reuse needs assumptions, anchors, uncertainty and expiry.

**Research access is unequal.** Autonomous laboratories, proprietary models, closed datasets and private evaluation systems can make important transitions impossible to inspect. The field will need reproducible public testbeds as well as methods for stating what cannot be checked under restricted access.

**Authority is institutional.** A machine can generate evidence or recommend action, but laboratories, collaborations, journals, regulators and society retain different decision rights. Treating authority as explicit input makes this boundary inspectable; it does not solve the political or ethical question of who should hold that authority.

**The field label itself can fail.** Machine behaviour, computational social science, network medicine and sustainability robotics illustrate different successful strategies for field formation [8,10,11,13,21]. They also remind us that new labels can overstate novelty. The scientific contribution of Machine Epistemics should be evaluated independently of whether the label ultimately persists.

## Outlook

AI systems are beginning to participate in research processes whose outputs can alter models, experiments, literature interpretations and scientific claims. This creates a control problem that is broader than making an agent more capable and narrower than explaining science as a whole. The object is the transition: what changed in the scientific state, which evidence warrants it, what assumptions and dependencies travelled with it, what prior commitments remain valid, and what authority the new state possesses.

We propose **Machine Epistemics** as a provisional name for the systematic study of these questions. Its research programme can be formal, empirical and engineering-oriented: identify what scientific states are observable; characterize which justified states are reachable; certify or refuse transport across context and representation changes; model dependence among evidence; compute selective reopening; distinguish local repair from warranted escalation; and develop bounded stopping rules that expose rather than hide uncertainty.

The proposal should be easy to falsify. If mature parent fields already provide the complete transition semantics in straightforward composition, the right outcome is a well-mapped integration discipline. If, however, the same composition-level failures and laws recur across materially different sciences and integrated methods make protected scientific decisions that parent systems do not, then AI-driven discovery may require more than increasingly autonomous scientists. It may require a science of how machine-mediated research is allowed to know.

## Working reference set

1. Wang, H. et al. Scientific discovery in the age of artificial intelligence. *Nature* **620**, 47–60 (2023). https://doi.org/10.1038/s41586-023-06221-2
2. Boiko, D. A., MacKnight, R., Kline, B. & Gomes, G. Autonomous chemical research with large language models. *Nature* **624**, 570–578 (2023). https://doi.org/10.1038/s41586-023-06792-0
3. Szymanski, N. J. et al. An autonomous laboratory for the accelerated synthesis of inorganic materials. *Nature* **624**, 86–91 (2023). https://doi.org/10.1038/s41586-023-06734-w
4. Rodriques, S. G. et al. A multi-agent system for automating scientific discovery. *Nature* **655**, 497–505 (2026). https://doi.org/10.1038/s41586-026-10652-y
5. Lu, C. et al. Towards end-to-end automation of AI research. *Nature* (2026). https://doi.org/10.1038/s41586-026-10265-5
6. Xin, H., Kitchin, J. R. & Kulik, H. J. Towards agentic science for advancing scientific discovery. *Nature Machine Intelligence* **7**, 1373–1375 (2025). https://doi.org/10.1038/s42256-025-01110-x
7. Liu, Y. & Ou, P. Verification-first autonomous catalysis: large language models as infrastructure for mechanism, computation, and experiment. *npj Artificial Intelligence* **2**, 56 (2026). https://doi.org/10.1038/s44387-026-00111-4
8. Rahwan, I. et al. Machine behaviour. *Nature* **568**, 477–486 (2019). https://doi.org/10.1038/s41586-019-1138-y
9. Moss, E. et al. Machine behaviour is old wine in new bottles. *Nature* **574**, 176 (2019). https://doi.org/10.1038/d41586-019-03002-8
10. Lazer, D. et al. Computational social science. *Science* **323**, 721–723 (2009). https://doi.org/10.1126/science.1167742
11. Fortunato, S. et al. Science of science. *Science* **359**, eaao0185 (2018). https://doi.org/10.1126/science.aao0185
12. Krenn, M. et al. On scientific understanding with artificial intelligence. *Nature Reviews Physics* **4**, 761–769 (2022). https://doi.org/10.1038/s42254-022-00518-3
13. Song, S., Mazzolai, B. & Kovač, M. A manifesto for Sustainability Robotics. *Nature Machine Intelligence* **8**, 1038–1044 (2026). https://doi.org/10.1038/s42256-026-01260-6
14. Doyle, J. A truth maintenance system. *Artificial Intelligence* **12**, 231–272 (1979). https://doi.org/10.1016/0004-3702(79)90008-0
15. de Kleer, J. An assumption-based TMS. *Artificial Intelligence* **28**, 127–162 (1986). https://doi.org/10.1016/0004-3702(86)90080-9
16. Reiter, R. A theory of diagnosis from first principles. *Artificial Intelligence* **32**, 57–95 (1987). https://doi.org/10.1016/0004-3702(87)90062-2
17. Russell, S. & Wefald, E. Principles of metareasoning. *Artificial Intelligence* **49**, 361–395 (1991). https://doi.org/10.1016/0004-3702(91)90015-C
18. Lebo, T., Sahoo, S. & McGuinness, D. (eds). PROV-O: The PROV Ontology. W3C Recommendation (2013). https://www.w3.org/TR/prov-o/
19. Perdomo, J., Zrnic, T., Mendler-Dünner, C. & Hardt, M. Performative Prediction. *Proceedings of ICML 2020*, PMLR 119, 7599–7609 (2020).
20. Nature Machine Intelligence. Artificial Intelligence (AI): editorial policy and risk-assessment framework for responsible AI use in research publishing (accessed 27 August 2026).
21. Barabási, A.-L., Gulbahce, N. & Loscalzo, J. Network medicine: a network-based approach to human disease. *Nature Reviews Genetics* **12**, 56–68 (2011). https://doi.org/10.1038/nrg2918

**Reference status:** this is a verified working core, not the final balanced Perspective bibliography. The next literature round must expand parent coverage, check every citation-to-proposition entailment and add contrary/limiting sources where they change demarcation.
# Machine Epistemics: The Control Science of AI-Driven Discovery

**Perspective draft V3**

## Abstract

Artificial intelligence is moving from isolated scientific prediction toward persistent research processes that search literature, propose hypotheses, choose experiments, call instruments and software, analyse results, revise models and generate scientific outputs. This shift makes a previously diffuse systems problem concrete: **when may a machine-mediated research process change what science commits to?** A workflow can execute correctly while supporting the wrong inference; multiple reviewers can agree while sharing the same hidden source; provenance can be exact while a scientific claim is false; an abstraction can preserve one decision while invalidating another; and a search can appear exhausted while decisive routes remain censored. We propose **Machine Epistemics** as a provisional field concerned with controlled scientific-state transitions in executable AI and hybrid research processes. Its object is not machine knowledge in general and not the AI model alone, but the bounded research episode in which evidence, representations, actions, resources, evaluators, history and authority interact. We organize this field hypothesis around four problems: observing the epistemic state; controlling scientific transitions and transport; assuring evidence and authority; and governing escalation and closure. Mature fields already own most component mechanisms—from computational epistemology, metareasoning and active experimentation to truth maintenance, diagnosis, formal abstraction, causal transport, provenance and metascience. The proposal is therefore falsifiable: if information-matched compositions of these parents reproduce the same cross-domain scientific decisions, Machine Epistemics should remain integration engineering rather than a distinct science. We outline the formal, empirical and institutional tests required to decide that question.

## Scientific work is becoming an executable process

Artificial intelligence has long contributed to scientific prediction, simulation and pattern recognition. The more consequential recent transition is that **parts of the research process itself are becoming executable**. Autonomous chemistry systems can search documentation, plan procedures and control experimental hardware; autonomous materials laboratories combine literature-derived knowledge, computation, active learning and robotics; multi-agent systems now connect literature search, hypothesis generation and data analysis in experimental biology; and end-to-end research systems can generate ideas, run computational experiments, analyse outputs and draft manuscripts [1–7]. These systems remain heterogeneous and their scientific maturity varies widely, but together they change the unit of engineering concern. We are no longer evaluating only a model prediction or a laboratory instrument. We increasingly evaluate a sequence of machine-mediated decisions that changes the state of an investigation.

This change exposes failure modes that task accuracy alone does not describe. A literature system may retrieve genuine papers yet bind a claim to the wrong passage. A computational pipeline may replay perfectly yet reproduce an invalid analysis. Several apparently separate agents may agree because they share a model, dataset or retrieval corpus. A representation can be compressed without affecting one target decision but destroy a distinction needed later. A failed tool call can be mistaken for evidence against a scientific hypothesis. A benchmark can become easier to optimize after publication, changing what its score means. And a research agent can produce a plausible conclusion that exceeds the authority of its evidence or of the process allowed to adopt it.

These are failures of **scientific-state transition control**. They concern whether the transition from one scientific commitment state to another is warranted—not merely whether a software step completed or an answer looks reasonable.

We use the term **Machine Epistemics** for the proposed science and engineering of those transitions in AI-mediated and hybrid human–machine research. The phrase does not denote the epistemology of machines in general. It is narrower: it asks how scientific commitments are formed, transported, revised, reopened and closed inside executable research processes.

The central question is therefore:

> Under what conditions may a machine-mediated research process change what it scientifically commits to, what must be preserved or reopened when it does so, and what externally supplied authority constrains the new state?

This is a field hypothesis, not a declaration that a field has already been established.

## The object of study: a machine-epistemic episode

The basic object is a **bounded research episode** in which scientific commitments can change. Informally, an episode contains a problem or criterion, a current scientific state, unresolved obligations, possible actions, available resources and tools, evidence and provenance, validation procedures, observations from the world, a history of earlier transitions, and an authority boundary.

We denote this object

\[
E=(P,S,O,A,R,M,V,X,H,K),
\]

where \(P\) is the problem and criterion contract; \(S\) is the plural scientific state; \(O\) is the set of unresolved scientific obligations; \(A\) is the admissible action repertoire; \(R\) records resources and access; \(M\) records evidence identity, provenance, dependence and memory; \(V\) binds verification, validation and evaluator contracts; \(X\) contains observations and tool outputs; \(H\) is append-only history; and \(K\) denotes externally supplied authority and governance constraints.

The tuple is not intended as a universal ontology. Its purpose is to identify a recurring control boundary: **an action produces an observation or candidate transformation, not truth by itself**. A scientific transition requires an interpretation that is valid under the current evidence, semantics, dependencies, resources and authority constraints. The same execution output can therefore have different scientific consequences in different episodes.

This distinction becomes visible in simple cases. A theorem prover returning a verified proof can justify a formal claim if the specification and checker are the right ones, but it does not automatically justify an empirical claim about nature. A laboratory robot completing a protocol establishes that an execution occurred; scientific interpretation still depends on measurement quality, controls and the relation between the experiment and the target claim. A reproducible data pipeline establishes replay identity but not that the chosen analysis answers the intended question. A high-scoring research benchmark establishes performance under a criterion, not permission to change that criterion after outcomes are known.

**Figure 1 | Scientific-state transitions in an executable research episode.** A bounded research episode begins with a declared problem and scientific state. Search, computation, proof, simulation, measurement, experiment and human review produce observations or candidate transformations. Interpretation gates determine whether those outputs warrant a change in scientific commitment. The figure contrasts four failure patterns: successful execution without adequate evidence; exact provenance without scientific correctness; repeated agreement under hidden dependence; and apparent search closure while decisive routes remain unavailable.

## A dense landscape of parent disciplines

Any proposal for Machine Epistemics has an unusually high burden of intellectual genealogy. Many nearby questions were formalized long before current scientific agents existed.

**Computational epistemology** uses logical and computational methods to study reliable inquiry and when learning procedures can converge successfully on epistemic problems [21]. **Machine epistemology** has been used to analyse machine learning and big data through a pragmatist account of inquiry in which uncertainty, intervention and practical control are central [22]. **Epistemic engineering** studies distributed systems in which people, tools and organizations construct epistemic change under polycentric control [23]. These are direct parents of the proposed label, not merely terminological neighbours.

Beyond these traditions, cybernetics and control theory study feedback, dynamics, observability and controllability. Decision theory, POMDPs and rational metareasoning study which action or computation to perform under uncertainty and resource limits; Russell and Wefald, for example, formalized the value of computations for bounded agents [17]. Active learning and optimal experimental design study informative measurements and experiments. Truth-maintenance systems and assumption-based TMSs record reasons for beliefs, maintain alternatives and revise them after contradiction [14,15]. Model-based diagnosis identifies explanations for discrepancies and develops measurements that discriminate competing diagnoses [16]. Formal methods, bisimulation, abstract interpretation and refinement supply powerful theories of proof, equivalence and safe abstraction. Causal inference studies identification and transport across environments. Metrology and psychometrics study traceability, calibration, invariance and linking. Provenance standards such as W3C PROV make lineage interoperable [18]. Evidence synthesis and meta-analysis address how multiple observations should combine. Performative prediction and related strategic-response theories formalize cases in which deployment changes the data-generating process [19]. Metascience and the science of science empirically study research systems, institutions, careers and discovery [10,11]. Philosophy of science and social epistemology provide essential normative analyses of evidence, explanation, understanding and authority.

AI for Science, agentic science and autonomous laboratories then supply the contemporary application substrate: systems in which many of these mechanisms can be assembled into research loops [1–7]. Verification-first autonomous catalysis, for example, argues that hypotheses should remain provisional until tool-grounded evidence and uncertainty-aware checks permit them to update workflow state [7]. That programme is a close parent of Machine Epistemics, not evidence that a separate field must exist.

The proposed residual is narrower than the union of these topics. It concerns **composition-level scientific decisions** that cross their normal boundaries. Consider four examples.

First, provenance can establish exact lineage while scientific support fails. The correct response requires a relation between provenance, claim semantics and validation, not provenance alone. Second, a metareasoning policy can select an informative or high-value computation while the scientific process still lacks authority to adopt the resulting claim. Authority is an externally supplied constraint on admissible scientific transitions, not a permission that the controller can infer from its own utility. Third, formal abstraction can certify equivalence relative to one interface while a later scientific question depends on a distinction the abstraction discarded. Reuse therefore requires a context-bound transport claim and, when the context changes, selective revalidation. Fourth, an active search policy can stop one route efficiently while a scientific closure claim remains invalid because other routes were unavailable or the representation itself prevented a decisive query.

The scientific question is whether such cross-layer cases are merely engineering interfaces among existing theories or whether they exhibit stable, measurable laws across materially different sciences.

### What Machine Epistemics does not rename

The proposal does **not** claim general machine knowledge, computational epistemology, machine epistemology, epistemic engineering, feedback control, metareasoning, experiment design, truth maintenance, belief revision, model-based diagnosis, formal verification, causal transportability, measurement science, provenance, meta-analysis, systematic review, research methodology, metascience, AI for Science or philosophy of science. Each retains its native objects, methods and standards.

This demarcation is not ceremonial. New interdisciplinary labels can obscure older traditions: the 2019 proposal for “machine behaviour” in *Nature* was directly criticized for overlooking cybernetics [8,9]. Machine Epistemics should therefore survive only if its narrow scientific-process transition object changes protected decisions beyond an information-matched composition of mature parents. If it does not, the appropriate outcome is an integration discipline rather than a new science.

**Figure 2 | Parent ownership and the composition gap.** Mature parent fields already own most component operations: reliable learning, action selection, experiment design, belief maintenance, diagnosis, formal transport, causal identification, measurement, provenance, evidence synthesis, strategic response and scientific governance. The proposed Machine Epistemics object lies only at the interfaces where these mechanisms jointly determine whether a scientific commitment may change. The figure highlights four candidate composition gaps—provenance to validity, relation to reuse, evidence to authority, and local route stopping to scientific closure—while leaving parent subsumption as an explicit possible outcome.

## Four control problems

A field hypothesis becomes useful only if it organizes research more compactly than a catalogue of mechanisms. We propose four control problems.

### 1. Observe the epistemic state

Before controlling a research process, a system must determine which scientifically relevant distinctions are currently observable. What claims remain live? Which alternatives can the available evidence distinguish? Which evidence items share sources? Which search routes were attempted, failed or censored? Which representations are comparable for the current question? Which uncertainties are reducible by another observation, and which are structurally non-identifiable under the available probes?

The word *observability* here borrows from control theory but extends beyond dynamical-state reconstruction. Scientific observability also depends on source identity, semantic scope, evidence dependence, search coverage and the distinction between absence of evidence and evidence of absence. Model-based diagnosis and formal/computational epistemology supply strong special cases: they ask which hidden explanations or truths can be recovered under declared observations and methods [16,21]. The field-level question is whether a common transition interface can expose these distinctions across heterogeneous research modes without replacing their native semantics.

Testable problems include the minimum probe required to distinguish two failure hypotheses; conditions under which evaluator outputs cannot identify whether a model, measurement or representation is responsible; and metrics for detecting when several validators provide less independent information than their count suggests.

### 2. Control and transport scientific transitions

A research system repeatedly proposes state changes: accepting a claim, revising a model, switching representation, transferring a result to a new domain, repairing a failed process or reopening an earlier conclusion. The central question is not whether change is possible, but **which scientific commitments survive it**.

Formal methods already provide exact and approximate relations; causal transportability formalizes conditions under which causal knowledge moves between environments; psychometric and metrological methods handle linking, calibration and traceability. Machine Epistemics treats the relation used by a scientific process as an explicit, context-bound warrant: what question is being preserved, under which assumptions, with what loss or uncertainty, and until when? An approximate relation valid for a control decision should not silently become exact equivalence for a high-precision scientific claim. Conversely, a changed representation should not trigger global invalidation when an earlier claim has independent support.

This problem yields formal questions about conservative composition of transport relations, propagation of approximation error and minimal selective reopening after a supporting relation expires.

### 3. Assure evidence and authority

Scientific systems need to distinguish **more evidence** from **more copies of the same evidence**. Shared datasets, prompts, model checkpoints, instruments, calibration procedures, literature corpora or human sources can make apparently separate confirmations strongly dependent. Provenance helps expose lineage but does not by itself quantify corroboration or scientific correctness.

Assurance also has an authority dimension. An automated checker, benchmark, reviewer or consensus process can provide evidence under a criterion; it does not create institutional authority beyond the people or institutions that legitimately supply that criterion. Machine Epistemics therefore treats authority as an external boundary condition. Its empirical task is to prevent a machine-mediated process from confusing evidential confidence with permission to adopt, deploy or publish a conclusion—not to derive who should possess that permission.

A further complication is evaluator dynamics. When a benchmark, policy or scientific rule is published and optimized against, the environment may change. Performative prediction formalizes this phenomenon in supervised learning [19]. Scientific evaluation raises analogous questions: when does a previously valid evaluator cease to support the same inference after the evaluated ecosystem adapts?

Testable problems include calibration under known or partially observed evidence dependence, selective survival of claims with alternative support families, and detection of evaluation regimes in which response invalidates a static pass.

### 4. Govern escalation and epistemic closure

Research systems also choose **how much to change** when progress stalls. A failed retrieval might require another query, a new source, a different model, a new measurement, a new representation or a reformulated problem. Escalating too early wastes resources and can discard valid structure; escalating too late traps the process inside an inadequate search space.

Metareasoning, diagnosis, design theory and adaptive search provide strong parents. The proposed composition-level question is whether scientific constraints support a general principle of **minimum sufficient escalation**: prefer the lowest intervention family capable of discharging the blocking scientific obligation while preserving prior warranted commitments and exposing unresolved alternatives. The relevant order need not be one universal ladder; it can be a partial order defined by how much of the scientific problem, representation, method or governance boundary an intervention changes.

Closure is the dual problem. A search route stopping is not the same as the scientific task being closed. A process should be able to state what search universe, representation, evidence classes and omission challenges support its stop, and which routes remain censored. `Unresolved` or `cannot determine` remain legitimate outcomes when the available process cannot establish what the decision requires.

This yields measurable research questions about false closure, missed escalation, unnecessary escalation, resource-adjusted justified reachability and the conditions under which finite stopping rules remain scientifically conservative.

**Figure 3 | Four control problems of Machine Epistemics.** A bounded machine-mediated research episode can be analysed through four questions. *Observe*: which claims, alternatives, dependencies, coverage gaps and failure causes are distinguishable? *Control and transport*: which scientific commitments may change or survive a representation, model or context transition? *Assure*: which evidence is genuinely independent and what externally supplied authority constrains adoption? *Escalate and close*: when is local repair sufficient, when must the action/search space change, and what bounded evidence supports stopping? Each problem is anchored in mature parent methods and yields formal or empirical tests of the proposed cross-layer residual.

## How the field hypothesis can be tested

A useful field cannot survive on terminology. Machine Epistemics needs formal and empirical programmes whose negative results can contract the proposal.

The strongest studies should use **known-answer and hostile cases** in which the correct scientific transition is independently specified. Examples include identical provenance with different scientific validity; locally compatible evidence with a global inconsistency; observationally equivalent models that differ under intervention; repeated evidence with hidden common ancestry; a low-level repair that makes a larger representation change unnecessary; and a search that appears stable while a decisive route is censored. Such cases test whether systems preserve distinctions rather than merely producing plausible answers.

The second requirement is **cross-domain recurrence**. A transition abstraction that works only in one scientific area belongs to that area. A field-level claim should require at least two materially different domains—for example, a formal/computational domain and a measurement/experimental domain—to instantiate the same control object while preserving their native standards. Published autonomous-research systems motivate this possibility [2–7], but they do not yet establish a universal cross-domain law.

Third, comparisons should use **strong parent compositions**, not weak single baselines. If a combination of computational epistemology, metareasoning, diagnosis, provenance, formal transport and existing evaluation infrastructure makes the same decisions under matched information and resources, then the integrated mechanism has no residual to claim.

Fourth, experiments should include **negative controls where added machinery must lose**. A direct calculation should not trigger elaborate diagnosis; genuinely independent evidence should not be rejected merely because dependence is possible; a stable evaluator should not be declared performative; and a valid local representation should not be replaced simply because a larger one exists.

Finally, semantic decisions need evaluation that is independent of the system whose scientific transitions are being assessed. Multiple automated reviewers are not automatically independent if they share models, data or sources. A field concerned with epistemic control therefore needs explicit evaluator identity, dependence and criterion binding whenever judgment cannot be reduced to a deterministic known-answer test.

A field-level empirical terminal might ask whether an integrated approach reduces false scientific completion, unsafe transport, dependence-induced overconfidence or unnecessary escalation **without** increasing unwarranted refusal or losing established capabilities. Failure on that test should narrow the field claim.

**Figure 4 | A falsifiable field claim.** The field hypothesis is tested by reconstructing native parent methods, composing the strongest information-matched baseline, and comparing it with an integrated scientific-transition controller on protected cross-domain cases. A stable residual in scientific decision quality supports further field development. A tie or parent win supports an integration-engineering interpretation. When evidence or evaluator independence is insufficient, no field-level conclusion is licensed.

## Barriers to a science of machine-mediated knowing

Several obstacles are scientific rather than merely technical.

**Ground truth is often unavailable.** In frontier research, the correct answer may not be known. Machine Epistemics therefore needs a layered evaluation strategy: exact known-answer cases for invariants; blinded expert adjudication for semantic transitions; prospective tests when future scientific value is claimed; and explicit unresolved states when no independent criterion exists.

**Dependence can be hidden.** Two agents may appear independent while sharing a foundation model or training data; two laboratories may share calibration or analysis software. Assurance must therefore represent unknown dependence rather than converting missing lineage into independence.

**Scientific objects change over time.** Datasets, instruments, ontologies, model versions and populations evolve. Persistent identity cannot substitute for comparability. Cross-version scientific reuse needs assumptions, anchors, uncertainty and expiry.

**Research access is unequal.** Autonomous laboratories, proprietary models, closed datasets and private evaluation systems can make important transitions impossible to inspect. The field would need reproducible public testbeds as well as methods for stating what cannot be checked under restricted access.

**Authority is institutional.** A machine can generate evidence or recommend action, but laboratories, collaborations, journals, regulators and society retain different decision rights. Treating authority as explicit input makes this boundary inspectable; it does not solve the political or ethical question of who should hold that authority.

**The field label itself can fail.** Computational epistemology, machine epistemology and epistemic engineering already occupy substantial neighboring territory [21–23]. Machine behaviour, computational social science, network medicine and sustainability robotics illustrate different strategies for field formation [8–13,20]. They also remind us that a new label can overstate novelty. The scientific value of the proposed transition framework should therefore be judged independently of whether the name *Machine Epistemics* ultimately persists.

## Outlook

AI systems are beginning to participate in research processes whose outputs can alter models, experiments, literature interpretations and scientific claims. This creates a control problem that is broader than making an agent more capable and narrower than a general theory of machine knowledge. The object is the transition: what changed in the scientific state, which evidence warrants it, what assumptions and dependencies travelled with it, what prior commitments remain valid, and what externally supplied authority constrains the new state.

We propose **Machine Epistemics** as a provisional name for the systematic study of these questions. Its research programme can be formal, empirical and engineering-oriented: identify what scientific states are observable; characterize which justified states are reachable; certify or refuse transport across context and representation changes; model dependence among evidence; compute selective reopening; distinguish local repair from warranted escalation; and develop bounded stopping rules that expose rather than hide uncertainty.

The proposal should be easy to falsify. If mature parent fields already provide the complete scientific-transition semantics in straightforward composition, the right outcome is a well-mapped integration discipline. If, however, the same composition-level failures and laws recur across materially different sciences and integrated methods make protected scientific decisions that parent systems do not, then AI-driven discovery may require more than increasingly autonomous scientists. It may require a science of how machine-mediated research is allowed to change what it knows.

## Working references

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
20. Barabási, A.-L., Gulbahce, N. & Loscalzo, J. Network medicine: a network-based approach to human disease. *Nature Reviews Genetics* **12**, 56–68 (2011). https://doi.org/10.1038/nrg2918
21. Hendricks, V. F. Computational Epistemology. In *Mainstream and Formal Epistemology*, 115–129 (Cambridge University Press, 2005). https://doi.org/10.1017/CBO9780511616150.008
22. Wheeler, G. Machine Epistemology and Big Data. In McIntyre, L. & Rosenberg, A. (eds), *The Routledge Companion to Philosophy of Social Science*, 321–329 (Routledge, 2017).
23. Cowley, S. J. & Gahrn-Andersen, R. How systemic cognition enables epistemic engineering. *Frontiers in Artificial Intelligence* **5**, 960384 (2023). https://doi.org/10.3389/frai.2022.960384

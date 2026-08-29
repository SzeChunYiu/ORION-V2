# Machine Epistemics: Controlling What AI-Driven Science May Learn, Change and Claim

**Perspective draft V5 — target archetype: Nature Machine Intelligence Perspective**

## Abstract

Artificial intelligence is moving from isolated scientific prediction toward persistent research processes that search literature, propose hypotheses, choose experiments, call instruments and software, analyse results, revise models and generate scientific outputs. This shift makes a diffuse problem concrete: **when may a machine-mediated research process change what science commits to, how it frames a problem or what it chooses to investigate?** Task success is not enough. A workflow can execute correctly while supporting the wrong inference; several reviewers can agree while sharing one hidden source; a representation can preserve one decision while destroying another; a system can become confident about its own reasoning without becoming correct; and a search can appear exhausted while decisive routes or forms of knowledge remain unavailable. We propose **Machine Epistemics** as a provisional name for the systematic study of controlled scientific-state transitions in executable AI and hybrid human–machine research. The proposal does not claim ownership of its mature parents in epistemology, control, metareasoning, belief revision, diagnosis, scientific method, cognitive science or social knowledge. Instead, it asks whether cross-parent coordination yields stable, measurable scientific decisions that those parents do not reproduce in straightforward composition. We organize the hypothesis around four questions: what the system knows and in what form; how it may change its state or problem frame; how it detects failures in its own inquiry; and when it may stop, escalate, explore or open a new problem. These questions suggest three coupled learning loops—world learning, self learning and search-space learning—and a falsifiable programme for deciding whether Machine Epistemics becomes a distinct science or contracts to an integration discipline.

## Research is becoming an executable process

AI has long contributed to prediction, simulation, classification and scientific data analysis. The more consequential transition is that **parts of the research process itself are becoming executable**. Autonomous chemistry systems can search documentation, plan procedures and control experimental hardware; autonomous materials laboratories combine computation, active learning and robotics; multi-agent systems connect literature search, hypothesis generation and analysis; and end-to-end research systems can generate ideas, run computational experiments, analyse outputs and draft manuscripts [1–7]. These systems remain heterogeneous and their scientific maturity varies, but they change the unit of concern. We increasingly evaluate not only a prediction or instrument, but a sequence of machine-mediated decisions that can alter the state of an investigation.

That sequence creates failures that task accuracy alone cannot describe. A retrieval system may find genuine papers yet bind a claim to the wrong passage. A deterministic pipeline may replay perfectly while reproducing an invalid analysis. Several reviewers may agree because they share a model, dataset or retrieval corpus. A failed tool call may be mistaken for evidence against a scientific hypothesis. A benchmark can become easier to optimize after publication, changing what its score means. A procedure can be stated correctly but executed poorly because the instructions omit state-dependent skill. An unexpected experimental side effect can be discarded as irrelevant even though it would open a valuable new question. And a research agent can be confident that its reasoning is adequate while lacking any independent evidence that this self-assessment is calibrated.

These are failures of **scientific-state transition control**. They concern whether a transition from one scientific commitment, representation or problem state to another is warranted—not merely whether a software step completed or an answer looks reasonable.

We use **Machine Epistemics** for the proposed science and engineering of those transitions in AI-mediated and hybrid research. The name does not denote machine knowledge in general, nor does it imply that an AI possesses a philosophical or phenomenological “self”. It asks a narrower question:

> **Under what conditions may a machine-mediated research process change what it scientifically commits to, how it frames the problem or what it chooses to investigate—and what must be preserved, reopened or left unresolved when it does?**

This is a field hypothesis, not a declaration that a field has already been established.

## A bounded machine-epistemic episode

The basic object is a **bounded research episode** in which scientific commitments can change. We write

\[
E=(P,F,S,O,A,R,M,V,X,H,K),
\]

where \(P\) binds the problem and comparison criterion; \(F\) is the current problem or representation frame; \(S\) is the plural scientific state; \(O\) contains unresolved scientific obligations; \(A\) is the admissible action repertoire; \(R\) records resources and access; \(M\) records evidence identity, provenance, dependence and memory; \(V\) binds validation and evaluator contracts; \(X\) contains observations and tool outputs; \(H\) is append-only history; and \(K\) denotes externally supplied authority constraints.

The tuple is not a universal ontology. It marks a recurring boundary: **an action produces an observation or candidate transformation, not truth by itself**. A scientific transition requires an interpretation valid under the current evidence, semantics, dependencies, context and authority constraints. The same execution output can therefore have different scientific consequences in different episodes.

The state \(S\) is also broader than a set of propositions. Human inquiry makes clear why. Scientific competence can involve procedural ability and learned perceptual discrimination as well as explicit statements; cognition can be distributed across people, tools and artifacts; and inquiry can change its own problem formulation [33–38]. A machine does not need to imitate every feature of human cognition. But if a procedural ability, distributed dependency or problem-frame change alters a protected scientific decision, the research process must be able to represent that distinction.

**Figure 1 | From successful tasks to warranted scientific-state transitions.** Search, computation, proof, simulation, measurement, experiment, human review and practical execution produce observations or candidate transformations inside a bounded research episode. Four contrasts motivate the field hypothesis: execution versus evidence; repeated agreement versus independent support; written instruction versus demonstrated competence; and unexpected encounter versus warranted explanation. The episode records not only what was produced, but which scientific state change—if any—the output is allowed to support.

## The proposal has many parents

Machine Epistemics faces an unusually high burden of intellectual genealogy. Most of its component problems were formalized long before current scientific agents existed.

Computational epistemology studies reliable inquiry and the conditions under which learning procedures can converge on epistemic problems [21,24]. Related work has used *machine epistemology* to analyse machine learning and big data through pragmatist accounts of inquiry, and *epistemic engineering* to study distributed systems of people and tools [22,23]. Cybernetics and control theory study feedback and regulation [32]. Decision theory, POMDPs and rational metareasoning study which action or computation to perform under uncertainty and resource limits [17]. Bayesian experimental design formalizes experiment choice [25]. Truth-maintenance systems and belief revision represent reasons, alternatives and change [14,15]. Model-based diagnosis distinguishes possible causes of discrepancies [16]. Formal methods and abstract interpretation establish properties across representations [26]. Causal transportability, measurement invariance and metrology formalize context-bound reuse and comparability [27–29]. Provenance standards expose lineage [18]. Meta-analysis treats dependent evidence explicitly [30]. Machine-assisted systematic review makes search and stopping decisions inspectable [31]. Performative prediction shows how deployment can alter the evaluated environment [19]. Metascience and the science of science study scientific systems themselves [10,11].

The human-inquiry lineage is equally important. Peirce linked surprising observations to abductive hypothesis formation followed by deduction and testing; Dewey treated reflective thought as inquiry arising from problematic situations and capable of reformulating them [33,34]. Ryle's analysis of knowing-how and Polanyi's account of tacit knowing challenge the idea that possessing explicit rules is identical to competent performance [35,36]. Kuhn's exemplars and conceptual change show why scientific competence and cross-generation comparison are not exhausted by fixed rule sets [45]. Lakatos shifts attention from isolated hypotheses to whether a sequence of changes is progressive or merely post-hoc repair [46]. Longino's social epistemology emphasizes criticism, background assumptions and the uptake of critique rather than equating objectivity with one isolated knower [44]. Hutchins and Suchman show how cognition and action can be distributed and situated rather than completely specified by a central plan [37,38].

Modern cognitive science makes several of these distinctions experimentally tractable. Metacognition separates task performance from monitoring and confidence; cognitive-control models treat additional effort as a costly intervention whose value must be estimated [39,40]. Insight research studies cases in which a changed representation makes a solution accessible [41]. Curiosity and information-seeking work distinguish novelty, surprise, uncertainty and learning progress rather than treating all exploration as one reward [42]. Organizational learning demonstrates a persistent exploration–exploitation tension in which short-run adaptive success can erode long-run exploratory capacity [43]. Historical and information-science work on serendipity similarly separates unexpected encounter from the recognition and follow-up that make the encounter scientifically useful [47].

These traditions are not evidence for a new field. They are **ownership constraints** on it. The 2019 proposal for “machine behaviour” in *Nature* was quickly criticized for under-crediting cybernetics [8,9]. A Machine Epistemics paper that simply renames metareasoning, cybernetics, pragmatism, tacit knowledge or social epistemology would deserve the same verdict.

The candidate residual is therefore deliberately narrow: **cross-parent scientific decisions in executable research processes**. Does a common control layer prevent false completion, unsafe transport, self-confirming review, inappropriate escalation or premature closure in cases where the strongest information-matched composition of mature parents does not? If not, Machine Epistemics should contract to integration engineering.

**Figure 2 | Parent ownership before field ownership.** Mature parent fields own reliable inquiry, feedback control, action selection, experiment design, belief maintenance, diagnosis, abstraction, transport, measurement, provenance, dependence-aware evidence, metacognition, procedural skill, distributed cognition, exploration and problem finding. The proposed residual lies only at composition boundaries where those mechanisms jointly determine whether a scientific state may change. Each candidate residual is paired with its contraction terminal: if a parent or parent composition reproduces the protected decision, ownership returns to the parent.

## Four questions for machine-mediated inquiry

A field hypothesis is useful only if it organizes research more compactly than a list of mechanisms. We propose four questions.

### 1. What does the system know, and in what form?

Before controlling inquiry, a system must expose the distinctions that matter to the current scientific decision. What claims and alternatives remain live? Which observations are source-bound? Which apparently repeated confirmations share an ancestor? Which uncertainties are reducible by another probe, and which are structurally non-identifiable? Which knowledge is propositional, procedural or dependent on demonstrated competence? Which state is distributed across a person, model, instrument, notebook or interface?

This is not a call for one universal knowledge representation. Different parent traditions already supply native semantics. The control requirement is narrower: the research process must not silently convert one epistemic form into another. Exact textual transfer does not imply causal equivalence; a preserved description does not prove that procedural competence survived a handoff; and a provenance chain does not establish scientific correctness [18,26–29,35–38].

A practical consequence is that evidence should record **mode of access and dependence when these affect the decision**. Reading a paper, observing an instrument, receiving expert testimony and watching a skilled demonstration can all inform inquiry, but they fail in different ways. Treating “retrievable text” as the universal knowledge type would make many of those failure conditions invisible.

### 2. How may it change what it knows—or how it frames the problem?

Research processes repeatedly revise models, representations, procedures and questions. The central issue is what survives the change.

Formal abstraction, causal transportability, measurement invariance and metrology already give strong accounts of selected kinds of preservation [26–29]. Machine Epistemics treats their outputs as **typed, context-bound warrants**, not as instances of one generic similarity score. An abstraction valid for a control decision should not silently become exact equivalence for a high-precision scientific claim. A changed instrument or population may preserve one judgment and invalidate another. An earlier conclusion need not be globally discarded if it retains an independent support family.

Human inquiry adds a harder case: sometimes the **problem frame itself** is the obstruction. Peircean and Deweyan inquiry does not assume that the initial formulation is always adequate [33,34], while work on insight and cognitive control shows why changing a representation can alter what solutions or discriminators are accessible [40,41]. A machine should therefore be permitted to *propose* a new frame or representation when lower-level actions are demonstrably non-identifying. But reframing must not become criterion gaming. If the new frame changes what counts as success, the comparison identity changes unless continuity is explicitly justified.

This makes “creative reframing” a controlled scientific action rather than a magical capability. Its value can be tested: does the new representation unlock a previously unreachable obligation while preserving or explicitly reopening protected prior decisions?

### 3. How does it know that its own inquiry process is failing?

A capable scientific agent should not only estimate uncertainty about the world; it should estimate uncertainty about **its own method**. Yet reflection is especially vulnerable to circularity. A model that generates an answer, a critique of that answer and a confidence score has produced three dependent outputs unless an independent argument establishes otherwise.

Metacognition provides the right starting point: task performance and self-monitoring are distinct and separately calibratable [39]. Rational metareasoning and expected-value-of-control models ask whether additional computation is worth its cost [17,40]. A machine-epistemic self-model can therefore be treated as a fallible learned predictor: how likely is the current answer to be correct; how likely is the current representation sufficient; which failure class is plausible; what is the expected value of more computation, another tool or independent review?

The crucial law is negative: **self-monitoring cannot self-validate**. Its predictions require delayed, held-out or otherwise independent outcomes and must carry the same source/dependence constraints as other evidence.

Failure should also be more than a terminal log entry. A reusable lesson binds the expected state, observed state, reproduction identity, candidate causes, discriminating tests, correction, regression check and transfer scope. Debugging, engineering incident review and error-learning traditions all embody this distinction between remembering a failure and learning when a correction applies. A scientific system should be penalized both for repeating a known failure and for overgeneralizing one memorable failure beyond its evidence.

Criticism supplies an external complement. Social epistemology suggests that criticism matters through the possibility of **uptake**, not through the count of critics alone [44]. Machine evaluation should similarly ask whether a critique targets an assumption, whether it changes the scientific state, and whether the critic is actually independent of the system under review.

### 4. When may it stop, escalate, explore or open a new problem?

Research control is not only about answering a fixed question. A process must decide whether another local action is useful, whether a larger change is warranted and whether an unexpected event deserves a new line of inquiry.

Metareasoning, diagnosis and experimental design already provide strong parents for choosing the next action [16,17,25]. A composition-level principle worth testing is **minimum sufficient escalation**: prefer the lowest intervention family capable of discharging the blocking scientific obligation while preserving prior warranted structure. A failed search should not automatically trigger a larger model; a failed benchmark should not automatically trigger a new representation; and a new representation should not be proposed merely because it is fashionable or expressive.

The dual error is staying local after evidence shows the current action space cannot identify the problem. Representation restructuring can be useful precisely in those cases [41]. A longitudinal process can also become a degenerating repair loop: repeated post-hoc patches discharge local failures while producing no new independently testable progress [46]. That pattern should be observable rather than hidden by activity counts.

Exploration creates another tension. Curiosity and information-seeking research distinguish several signals—novelty, prediction error, uncertainty, information gain and learning progress—and show why unpredictability alone can be a poor target [42]. Organizational learning similarly shows that exploitation can become locally adaptive and globally self-defeating [43]. A scientific agent therefore needs a bounded exploration channel that can preserve off-query anomalies and alternative methods without rewarding stochastic distraction.

Serendipity is a particularly useful test case. Historical analysis does not support a defensible universal percentage of discoveries that are “accidents”; the mechanisms are heterogeneous [47]. For machine discovery, the important decomposition is **encounter + recognition + follow-up**. An unusual side effect or failed experiment may enter a low-bandwidth encounter buffer. The system can later connect it to unresolved problems and propose a discriminator. The encounter itself is not evidence for the new explanation and cannot grant agenda authority.

Closure has the same discipline. A route-specific stopping rule does not establish that the broader scientific search space is exhausted [31]. A bounded closure claim should state the searched disciplines, source modes, knowledge forms, acquisition modes, contexts and epochs that define its universe, which regions were censored, and what observation would reopen the terminal. No finite project can establish saturation of “all human civilization”; tacit, lost, inaccessible, changing and future forms of knowledge make such a terminal ill-posed.

**Figure 3 | Four control questions and three learning loops.** The four questions—knowledge form, state/frame change, self-failure detection, and stop/escalate/explore/open—map to three coupled learning loops. *World learning* models the external problem. *Self learning* models the calibration and blind spots of the learner or research process. *Search-space learning* estimates when the current data source, representation, method, objective or action family is inadequate. The loops share evidence but cannot certify one another by self-consistency alone.

## From epistemic control to machine learning

If Machine Epistemics remains only a governance wrapper around a fixed learner, its scientific reach will be limited. The stronger possibility is that epistemic state changes **what the machine learns**.

A self-learning loop could train calibrated predictors of error class, method adequacy and external-review value rather than only answer confidence. Continual learners could maintain typed failure memories containing causal attribution and transfer scope rather than replaying high-loss samples alone. Exploration systems could represent surprise as a vector—predictive, semantic, causal, source, evaluator or model-class surprise—instead of converting every prediction error into intrinsic reward. Procedural learners could train on demonstrations, intermediate state observations, corrections and recovery episodes, while explicitly marking when text instructions underdetermine competence. Agentic systems could be evaluated as distributed cognitive systems—models, humans, tools, memory and instruments—rather than attributing every success or failure to a base model. And meta-learning systems could propose representation changes whose reward depends on unlocking held-out obligations without silently invalidating old decisions.

Each proposal has mature parents in uncertainty estimation, meta-learning, continual learning, imitation learning, curiosity, open-ended learning and human–AI systems. The Machine Epistemics hypothesis survives only if the **scientific-control constraints** change protected outcomes beyond those parents: fewer false completions, better calibrated review triggers, safer transfer, better retention of negative knowledge, more useful exploration and more disciplined representation change.

## A field designed to contract

A useful new field should specify how it can fail.

The strongest empirical programme begins with native parent reconstruction and known-answer cases. Parent mechanisms are then composed into the strongest information- and resource-matched baseline available. Only after that baseline is fixed should an integrated controller be tested on protected cross-domain episodes: hidden evidence dependence; context-sensitive transport; self-model miscalibration; instruction-versus-competence transfer; useful surprise versus stochastic novelty; lower-level repair versus warranted representation change; and bounded closure under censored search.

Where exact answers are impossible, evaluator identity and independence become part of the experiment. Multiple automated reviewers are not independent merely because they run as separate agents. Prospective evaluation is required for claims about future opportunity discovery. Negative, parent-tie and `CANNOT_CHECK` outcomes remain in the scientific record.

**Figure 4 | A falsifiable field hypothesis.** Native parent mechanisms are reconstructed in their own terms and composed into the strongest information-matched baseline. Protected cross-domain cases then test whether an integrated scientific-transition controller changes decision quality. A stable residual supports further field development; a parent tie or win supports an integration-discipline interpretation; domain-specific value returns the problem to its native field; and insufficient independent evidence leaves field separation unresolved.

Several results would contract Machine Epistemics decisively. The field claim weakens if mature parents reproduce all important cross-layer decisions; if the abstraction disappears when native scientific or practical semantics are restored; if self-models add no calibrated decision value beyond ordinary uncertainty; if procedural/tacit annotations add nothing beyond standard context variables; if surprise machinery produces distraction rather than useful discoveries; or if the integrated framework adds logging and complexity without increasing justified scientific reach.

The proposal also has explicit non-claims. It does not require machine consciousness, a metaphysical self, one universal scientific method, a universal novelty metric or imitation of every human cognitive bias. It does not treat recipes, oral traditions or accidents as automatically scientific evidence, nor does it assume that plural cultural epistemologies can be flattened into one schema without loss. It does not allow a machine to infer its own scientific or institutional authority from confidence or utility. And it does not claim that the knowledge structures of human civilization can be exhaustively saturated.

## Outlook

AI systems are beginning to participate in research processes that can alter models, experiments, literature interpretations, procedures and scientific claims. This creates a problem broader than making an agent more capable and narrower than a general theory of machine knowledge. The object is the transition: what changed in the scientific state or frame, which evidence warrants it, what dependencies and forms of competence travelled with it, what the process knows about its own failure modes, what unexpected events it preserved, which prior commitments remain valid and what externally supplied authority constrains the next state.

We propose **Machine Epistemics** as a provisional name for the systematic study of these questions. Its value does not depend on whether the name persists. If mature parent disciplines already provide complete transition semantics in straightforward composition, the right outcome is a well-mapped integration discipline for reliable agentic science. If, however, the same composition-level failures recur across materially different sciences and integrated methods make protected scientific decisions that parent systems do not, AI-driven discovery may require more than increasingly autonomous scientists. It may require a science of how machine-mediated inquiry learns when to change what it knows—and when it must refuse to claim that it knows.

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
24. Kelly, K. T. *The Logic of Reliable Inquiry* (Oxford University Press, 1996). https://doi.org/10.1093/oso/9780195091953.001.0001
25. Chaloner, K. & Verdinelli, I. Bayesian experimental design: a review. *Statistical Science* **10**, 273–304 (1995). https://doi.org/10.1214/ss/1177009939
26. Cousot, P. & Cousot, R. Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints. *POPL 1977*, 238–252 (1977). https://doi.org/10.1145/512950.512973
27. Pearl, J. & Bareinboim, E. External validity: from do-calculus to transportability across populations. *Statistical Science* **29**, 579–595 (2014). https://doi.org/10.1214/14-STS486
28. Meredith, W. Measurement invariance, factor analysis and factorial invariance. *Psychometrika* **58**, 525–543 (1993). https://doi.org/10.1007/BF02294825
29. National Institute of Standards and Technology. NIST Policy on Metrological Traceability (accessed 27 August 2026). https://www.nist.gov/calibrations/traceability
30. Hedges, L. V., Tipton, E. & Johnson, M. C. Robust variance estimation in meta-regression with dependent effect size estimates. *Research Synthesis Methods* **1**, 39–65 (2010). https://doi.org/10.1002/jrsm.5
31. van de Schoot, R. et al. An open source machine learning framework for efficient and transparent systematic reviews. *Nature Machine Intelligence* **3**, 125–133 (2021). https://doi.org/10.1038/s42256-020-00287-7
32. Ashby, W. R. *An Introduction to Cybernetics* (Chapman & Hall, 1956).
33. Peirce, C. S. The fixation of belief. *Popular Science Monthly* **12**, 1–15 (1877); and How to make our ideas clear. *Popular Science Monthly* **12**, 286–302 (1878).
34. Dewey, J. *How We Think* (D. C. Heath, 1910).
35. Ryle, G. *The Concept of Mind* (Hutchinson, 1949).
36. Polanyi, M. *The Tacit Dimension* (Doubleday, 1966).
37. Hutchins, E. *Cognition in the Wild* (MIT Press, 1995).
38. Suchman, L. A. *Plans and Situated Actions: The Problem of Human–Machine Communication* (Cambridge University Press, 1987).
39. Fleming, S. M., Dolan, R. J. & Frith, C. D. Metacognition: computation, biology and function. *Philosophical Transactions of the Royal Society B* **367**, 1280–1286 (2012). https://doi.org/10.1098/rstb.2012.0021
40. Shenhav, A., Botvinick, M. M. & Cohen, J. D. The expected value of control: an integrative theory of anterior cingulate cortex function. *Neuron* **79**, 217–240 (2013). https://doi.org/10.1016/j.neuron.2013.07.007
41. Kounios, J. & Beeman, M. The cognitive neuroscience of insight. *Annual Review of Psychology* **65**, 71–93 (2014). https://doi.org/10.1146/annurev-psych-010213-115154
42. Gottlieb, J., Oudeyer, P.-Y., Lopes, M. & Baranes, A. Information-seeking, curiosity, and attention: computational and neural mechanisms. *Trends in Cognitive Sciences* **17**, 585–593 (2013). https://doi.org/10.1016/j.tics.2013.09.001
43. March, J. G. Exploration and exploitation in organizational learning. *Organization Science* **2**, 71–87 (1991). https://doi.org/10.1287/orsc.2.1.71
44. Longino, H. E. *Science as Social Knowledge: Values and Objectivity in Scientific Inquiry* (Princeton University Press, 1990).
45. Kuhn, T. S. *The Structure of Scientific Revolutions* (University of Chicago Press, 1962; 4th edn, 2012).
46. Lakatos, I. *The Methodology of Scientific Research Programmes* (Cambridge University Press, 1978).
47. Yaqub, O. Serendipity: Towards a taxonomy and a theory. *Research Policy* **47**, 169–179 (2018).

# Conceptual Development and Transfer Discovery Amendment V1
## Discovering what can transfer, rather than hard-programming donor lessons

**Framework role:** candidate amendment to the bounded Machine Epistemics foundation.  
**Scientificity level:** S1 operational interface plus S2 discriminating mechanism hypothesis.  
**Paper status:** not a new paper identity. It is shared infrastructure for P-A, P-B, P-C, P-D and the flagship until a protected independent residual exists.  
**Authority:** non-authorizing. This document does not establish a new law, field, superior F2 architecture or publication-ready result.

## 1. Why this amendment exists

ORION-V2 already decomposes knowledge, reconstructs native parents, reduces donors, transports typed relations, recombines compatible atoms, challenges proposals and selectively reopens claims. A remaining weakness is that many useful cross-domain lessons are currently discovered by the research team and then encoded into the framework. This is scientifically insufficient if the intended object is machine scientific intelligence.

A stronger hypothesis is:

> A scientific system should be able to discover candidate transferable structure from heterogeneous prior knowledge, rather than receiving the important transfer as a pre-written lesson.

The change is subtle but fundamental. **Transfer is not only projection. It also has a discovery problem.** The system must decide which prior cases are worth comparing, what structure is shared, which parts must *not* transfer, what new target consequence follows, and when the analogy has failed.

This amendment therefore separates:

`generic transfer operators`

from

`domain-specific transferable content`.

The generic operators may be engineered and tested. The scientific content of a transfer must arise from source-bound donor structures and protected target evidence.

## 2. Research basis

### 2.1 Human analogy is relational, but retrieval is a bottleneck

Gentner's structure-mapping account treats analogy as alignment of relational systems rather than simple attribute matching, with preference for systematic higher-order relational structure. This is directly relevant to ORION because surface resemblance is a poor scientific criterion for reuse.

Gentner, Loewenstein, Thompson and Forbus later showed an important complementary result: even when people can use an analogy after it is retrieved, access to the relevant prior case often fails. Analogical abstraction from multiple cases can make previously inert relational knowledge retrievable. Transfer discovery therefore needs both a **candidate-generation/retrieval process** and a **mapping/admission process**.

Gentner's later synthesis on analogy and abstraction further emphasizes that comparison can induce relational abstractions, that progressive alignment can support movement from concrete to more remote generalization, and that broad transfer depends on examples that are structurally alignable rather than merely maximally diverse.

These results do not prove an ORION mechanism. They motivate discriminators.

### 2.2 Scientific conceptual change uses models, analogies and constructed representations

Nersessian's work on scientific conceptual change argues that analogical modelling, visual modelling and thought experimentation can function as generative methods of conceptual change. Her later cognitive-science-of-science work emphasizes scientific reasoning as distributed across cognitive, social, material and representational resources.

Dunbar's in-vivo studies of laboratories likewise treated unexpected findings, analogy, hypothesis generation and group reasoning as interacting parts of real scientific discovery.

For V2, this suggests that an anomaly should not automatically trigger a predefined repair. It can instead trigger a **search for alternative representational or relational structure**.

### 2.3 Exemplars can become footholds for wider conceptual development

Goodwin's historical analysis of conformational analysis in organic chemistry argues that a concrete exemplar can provide a foothold from which a conceptual innovation is extended analogically through a discipline. This suggests that Transfer Memory should not contain only abstract rules. It should preserve exemplars, their solved structure, the abstraction induced from them, and the conditions under which the abstraction later transferred.

### 2.4 Physics provides donors, not hard-coded laws for Machine Epistemics

Several developments in modern physics are useful donor cases:

- **effective field theory:** successful theories can be regime-bounded rather than universally fundamental;
- **renormalization-group reasoning and universality:** some details become irrelevant under changes of scale while other variables control qualitative behaviour;
- **symmetry/invariants:** scientifically meaningful structure is often identified by what remains unchanged under a transformation;
- **duality and theoretical equivalence:** formally different representations can encode a common core, but formal equivalence alone does not settle interpretative equivalence;
- **anomalies/consistency failures:** unexpected failure can either expose a productive missing structure or invalidate a candidate.

The framework must *not* contain rules such as `all scientific problems have an EFT regime` or `every representational difference is gauge redundancy`. Physics contributes source cases to a donor pool and evaluation set. A transfer-discovery system gets credit only if it reconstructs the native physics lesson, proposes a bounded cross-domain mapping prospectively, and survives target counterexamples.

This distinction is essential to prevent metaphor inflation.

## 3. Conceptual Development as a first-class transition

A concept is represented as a versioned state rather than a label:

`ConceptState = (identity, primitives, relations, scope, operational links, invariants, representation equivalences, exemplars, counterexamples, parents, anomalies, authority ceiling)`.

Conceptual development is then a typed transition:

`ConceptState_t -> ConceptState_t+1`.

Allowed reference transition operators are:

- `SPECIALIZE` — narrow scope or regime;
- `GENERALIZE` — expand scope while preserving explicitly tested structure;
- `SPLIT` — replace one concept with multiple distinctions;
- `MERGE` — identify a warranted common core;
- `BRIDGE` — connect concepts while preserving local identities;
- `REPARAMETERIZE` — change representation while preserving substantive judgment;
- `REVISE` — alter internal structure after a discriminating failure;
- `DEPRECATE` — stop using a concept that no longer earns scientific value.

These are not laws of scientific history. They are an auditable vocabulary for proposed conceptual changes.

## 4. Concept-transition admission rule

A transition receives zero credit merely for producing cleaner vocabulary.

A proposed conceptual transition is admissible for protected evaluation only when it binds:

1. predecessor and strongest-parent recovery;
2. native fidelity;
3. explicit new scope;
4. conceptual-loss audit;
5. operational/measurement links;
6. preserved invariants and old valid cases;
7. authority limits;
8. a prospective changed decision, prediction or formal necessity;
9. falsifiers;
10. hidden cases or an independent formal check.

The critical rule is:

> `NEW_VOCABULARY != NEW_SCIENCE`.

If a concept can be renamed or reorganized without changing a protected judgment, prediction, formal necessity or recoverable representation, the current terminal is `NO_SCIENTIFIC_RESIDUAL`.

## 5. Transfer Discovery

### 5.1 Transfer is a search problem

The transfer lifecycle is:

`encounter -> structural description -> candidate discovery -> alignment hypothesis -> bounded projection -> native recovery -> negative-transfer challenge -> target prediction -> hidden evaluation -> abstraction-memory update`.

The important difference from a lesson table is that ORION does not begin with `use renormalization here` or `apply symmetry there`.

It begins with a donor memory containing source-bound cases and typed structures.

### 5.2 DomainStructure

The reference implementation describes each donor or target with open-ended identities for:

- first-order relations;
- higher-order relations;
- invariants;
- failure topology;
- transformations;
- regime variables;
- native parent identities;
- surface tags.

These fields do not prescribe the content. A physics case, a biological mechanism case and a software-evaluation case can use completely different native vocabulary while a later comparison proposes a shared relational abstraction.

### 5.3 Relational abstraction induction

The reference semantics induce a `RelationalAbstraction` only when repeated typed structure occurs across distinct domains.

The production system may eventually use richer graph matching, model-based reasoning, theorem discovery or learned representations. The current simple reference implementation deliberately uses a transparent pairwise structural intersection so that the scientific contract is testable:

> the content of an abstraction must come from donor records, not from a hard-coded transfer lesson.

### 5.4 Candidate retrieval

For a new target, ORION searches induced abstractions for structural overlap and returns candidate donors. Surface similarity is recorded but is not required. A remote-transfer score favors high structural coverage that survives surface dissimilarity.

This explicitly targets the human retrieval bottleneck identified in analogical-transfer research.

### 5.5 Progressive alignment

A practical discovery policy should permit a developmental path:

`near cases -> alignable comparison -> relational abstraction -> increasingly remote retrieval`.

This is preferable to demanding maximum remoteness immediately. If the system cannot align remote donors reliably, it should learn an abstraction from closer cases before expanding scope.

### 5.6 Negative transfer is first-class

Every transfer hypothesis must include:

- what maps;
- predicted target consequences;
- what is forbidden to transfer;
- mismatches/losses;
- falsifiers.

Admission requires negative decoys and counter-transfer challenges.

A transfer is rejected if it succeeds only because of surface resemblance, corrupts authority or measurement semantics, fails donor-native recovery, or cannot discriminate hidden target cases.

## 6. Transfer Memory

Transfer Memory should contain more than successful mappings.

For each episode retain:

`donor cases -> induced abstraction -> target candidate -> projected consequences -> failures -> counterexamples -> parent verdict -> resource cost -> final disposition`.

This enables three kinds of learning:

1. **forward transfer:** reuse an abstraction on a new target;
2. **backward retrieval:** a newly induced abstraction makes old donor knowledge newly retrievable;
3. **negative transfer learning:** failed analogies create explicit forbidden mappings and boundary conditions.

Failure is therefore not deleted. It shapes the future retrieval distribution.

## 7. Hard-programming boundary

### Allowed generic machinery

The system may be engineered with generic operators such as:

- compare two source-bound structures;
- search memory;
- align relations;
- induce candidate abstractions;
- rank donor candidates;
- freeze prospective target consequences;
- run native recovery;
- run negative controls;
- test hidden cases;
- preserve authority, provenance and loss.

### Not allowed as framework truth

The following must not be embedded as universal transfer facts:

- `regime dependence is always useful`;
- `symmetry always implies equivalence`;
- `a representation-equivalence class always exists`;
- `an anomaly should always produce conceptual revision`;
- `simple details are always irrelevant at a larger scale`;
- any fixed list of physics-derived scientific lessons.

Those are donor hypotheses that the system may rediscover and test.

## 8. Distinguishing transfer discovery from P-A

P-A already studies structural donor discovery and native fidelity. The new mechanism does not automatically create another paper.

The division is:

- **P-A:** can ORION retrieve useful remote parents while controlling false analogy and preserving native verdicts?
- **Transfer Discovery extension:** can repeated comparisons create new relational abstractions that improve future donor retrieval and target decisions beyond fixed lessons and strongest analogy/retrieval parents?
- **Conceptual Development extension:** can transfer-triggered anomalies cause a justified change in the target concept system while preserving predecessor validity?

If these do not show independent causal residuals, they merge into P-A/P-B/P-C.

## 9. Integration with the existing V2 architecture

No new `K7` is introduced.

### K0 — mutable problem frame
Bind concept identity/version and regime identity. A material concept revision changes the frame receipt.

### K1 — typed knowledge forms
Store `ConceptState`, exemplars, relational abstractions, successful transfers and failed-transfer lessons.

### K2 — relation/transport
Add discovered alignment hypotheses, invariants, representation-equivalence candidates, transfer losses and forbidden mappings.

### K3 — distributed/social knowledge
Preserve the native community/domain that owns the meaning of a concept. Cross-domain transfer cannot overwrite native usage by generic definition.

### K4 — self-model
Estimate whether the present conceptualization is inadequate and the expected value of transfer search versus more local computation.

### K5 — surprise/opportunity
Use anomalies as triggers for transfer search or conceptual revision, but do not treat surprise itself as support.

### K6 — saturation
Search donor space broadly enough that transfer discovery is not constrained to the researcher's favorite field.

### Knowledge metabolism
A discovered abstraction becomes a recombination candidate only after source decomposition and native reconstruction. Failed transfers are recycled as scoped failure lessons.

### AbsorptiveTheory
Add explicit regime maps, invariant maps, representation-equivalence candidates and conceptual-loss recovery maps only when they survive protected evidence.

## 10. Discriminating experiment programme

The companion protocol `CONCEPTUAL_TRANSFER_DISCOVERY_PROTOCOL_V1.json` separates calibration from confirmatory evidence.

### TD10 — historical calibration

Use historically documented cases from physics, chemistry, mathematics, biology and cognitive science to test whether the pipeline can reconstruct known conceptual developments *without giving it the evaluator's transfer label*.

This is calibration only because many historical cases may be present in model training.

### TD20 — remote donor retrieval

Provide a target and a broad donor pool containing:

- surface-similar decoys;
- structurally relevant remote donors;
- structurally partial donors;
- incompatible native concepts.

Measure top-k useful donor recall jointly with false-analogy rate and native fidelity.

### TD30 — fresh generated conceptual development

Generate after protocol freeze:

- arbitrary concept tokens;
- hidden regime variables;
- transformations;
- invariant/non-invariant features;
- misleading surface correspondences;
- cases where the correct transition is `SPECIALIZE`, `SPLIT`, `MERGE`, `REPARAMETERIZE`, `REVISE` or no change.

Hidden cases determine whether the conceptual transition actually improves prediction/decision quality while retaining old valid cases.

### TD40 — naturalistic prospective cases

Queue real scientific problems with a prospectively frozen opportunity for cross-domain transfer. Independent domain experts evaluate whether the discovered donor and conceptual transition changed a scientific decision.

This is the route toward S4, not the historical calibration set.

## 11. Essential controls

At minimum compare:

- target-only direct reasoning;
- semantic retrieval;
- **fixed lesson injection**;
- strongest structure-mapping/analogy parent;
- F0 strongest parent federation;
- static F2 without transfer discovery;
- F2 with transfer discovery.

The fixed-lesson arm is crucial. It directly tests the concern that a research team could simply pre-program the useful physics/biology lessons.

If fixed lessons or the strongest analogy parent match Transfer Discovery at lower cost, the new mechanism contracts.

## 12. Primary outcome family

Do not optimize one scalar.

Report a non-compensatory vector including:

- hidden target decision success;
- useful remote-donor recall;
- false-analogy rate;
- donor-native fidelity;
- old-valid-case retention;
- concept-transition correctness;
- unnecessary concept proliferation;
- authority/measurement corruption;
- resource cost;
- cross-domain transfer.

A result that gains recall by increasing false analogies is not dominance.

## 13. Kill and merge conditions

The Transfer Discovery hypothesis is not independently supported if:

- semantic retrieval or strongest structure mapping reproduces the protected decisions;
- fixed lesson injection performs equivalently at materially lower cost;
- generated abstractions do not improve future retrieval;
- gains disappear on surface-permuted or hidden-counterexample tasks;
- donor-native fidelity degrades;
- concept revisions fail old-valid-case retention;
- conceptual changes do not alter hidden decisions/predictions or establish formal necessity;
- the mechanism works only on historically famous examples;
- independent naturalistic adjudication cannot reproduce the effect.

Valid terminals include:

`PARENT_SUFFICIENT`, `FIXED_LESSON_SUFFICIENT`, `NO_SCIENTIFIC_RESIDUAL`, `FALSE_ANALOGY_REJECTED`, `CONTEXTUAL_TRANSFER`, `PROTECTED_TRANSFER_RESIDUAL`, `MERGE_INTO_P_A`, `MERGE_INTO_P_B`, `MERGE_INTO_P_C`, and `CANNOT_CHECK`.

## 14. Physics-derived hypotheses to *rediscover*, not encode

The first historical donor battery should include cases that permit, but do not reveal, candidate lessons such as:

- regime-bounded model adequacy;
- relevance/irrelevance under transformation or scale;
- invariant structure across representation change;
- common-core versus interpretative equivalence;
- anomaly-triggered revision;
- multiple equivalent formulations with unequal computational convenience.

The evaluator holds the expected historical interpretation. The solver receives the source material, competing donors and target problem, not our lesson label.

This converts the physics discussion from analogy-driven framework design into a falsifiable transfer-discovery benchmark.

## 15. Current scientific status

`Conceptual Development` is now an operationalized candidate research object.

`Transfer Discovery` is now an operationalized mechanism hypothesis.

Neither is established as a distinct scientific contribution.

The next promotion step is not more terminology. It is a protected result showing that discovered abstractions improve target decisions beyond fixed lessons, semantic retrieval, strongest analogy parents and static F2 without unacceptable false transfer or cost.

---

## Literature anchors

1. Gentner, D. (1983). *Structure-Mapping: A Theoretical Framework for Analogy*. Cognitive Science 7(2), 155–170. DOI: 10.1207/s15516709cog0702_3.
2. Gentner, D., Loewenstein, J., Thompson, L., & Forbus, K. D. (2009). *Reviving Inert Knowledge: Analogical Abstraction Supports Relational Retrieval of Past Events*. Cognitive Science 33, 1343–1382. DOI: 10.1111/j.1551-6709.2009.01070.x.
3. Gentner, D. (2017). *Analogy and Abstraction*. Topics in Cognitive Science 9, 672–693. DOI: 10.1111/tops.12278.
4. Nersessian, N. J. (1989). *Conceptual change in science and in science education*. Synthese 80, 163–183. DOI: 10.1007/BF00869953.
5. Nersessian, N. J. (1999). *Model-Based Reasoning in Conceptual Change*. In *Model-Based Reasoning in Scientific Discovery*. DOI: 10.1007/978-1-4615-4813-3_1.
6. Nersessian, N. J. (2025). *How Do Scientists Think? Contributions Toward a Cognitive Science of Science*. Topics in Cognitive Science. DOI: 10.1111/tops.12777.
7. Goodwin, W. (2021). *Gaining traction: Foothold concepts and exemplars in conceptual change*. Studies in History and Philosophy of Science 90, 145–152. DOI: 10.1016/j.shpsa.2021.09.010.
8. Weinberg, S. (2021). *On the development of effective field theory*. European Physical Journal H 46, 6. DOI: 10.1140/epjh/s13129-021-00004-x.
9. Burgess, C. P. (2007). *An Introduction to Effective Field Theory*. Annual Review of Nuclear and Particle Science 57, 329–362. DOI: 10.1146/annurev.nucl.56.080805.140508.
10. Hon, G., & Goldstein, B. R. (2012). *Maxwell's contrived analogy: An early version of the methodology of modeling*. Studies in History and Philosophy of Modern Physics 43(4), 236–257. DOI: 10.1016/j.shpsb.2012.07.001.

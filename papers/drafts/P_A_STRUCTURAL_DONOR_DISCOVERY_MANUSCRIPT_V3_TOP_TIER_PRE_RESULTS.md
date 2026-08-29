# Finding the Theory You Did Not Know You Were Reusing
## Structural Donor Discovery and Conservative Generalization in Machine-Mediated Science

**P-A manuscript V3 — top-tier pre-results Article draft**  
**Primary target archetype:** broad AI/scientific-discovery Article  
**Status:** all evidence-independent prose, Methods, result identities, figure slots and contraction terminals are frozen. Protected outcomes remain open; no novelty, superiority or publication readiness is claimed.

## Abstract

Scientific ideas are often rediscovered because structurally related work is described with different terminology, appears in a remote discipline, or exists in a practical rather than scholarly source. Search systems optimized for lexical or citation proximity can therefore inflate novelty and miss methods that would strengthen or falsify a proposed contribution. We study **structural donor discovery**: source-bound retrieval of remote theories, methods and practices followed by a conservative test of which scientific judgments survive translation. The system represents a candidate donor in its native problem, assumptions, operations, failure conditions and authority, then constructs a decision-relative correspondence to the target problem. A donor is accepted only when registered target decisions and counter-probes are preserved; useful practice transfer is kept separate from scientific-parent ownership. We prospectively compare the method with lexical, embedding, citation, literature-based-discovery, analogy, expert and strongest-union controls on hidden-parent cases and remote scientific domains. Primary outcomes are remote-parent recall, false-analogy rate, native-verdict preservation, novelty-contraction accuracy and resource cost. The method survives only if its typed reduction—not additional search effort—improves the protected frontier.

## Introduction

Scientific search is easier when a community already knows the relevant vocabulary. It is harder when two fields formulate the same structural difficulty using different objects, measurements or institutional practices. A reliability problem in distributed systems may resemble corroboration among scientific reviewers; a calibration problem in metrology may resemble evaluator drift; a repair protocol may contain a useful state-control pattern without owning the scientific inference it inspires. These relationships can matter before a new theory is written. They can expose an older parent, supply a missing control, suggest an experiment or show that a proposed contribution is not new.

Modern retrieval systems remain strongly influenced by textual, citation and embedding proximity. Those signals are valuable but can fail under vocabulary shifts, historical terminology, source-mode changes and remote domains. Large language models can propose analogies more flexibly, but fluent analogies can also conceal false equivalence: objects share a narrative pattern while differing in the decision, relation, scale, evidence standard or authority that matters scientifically.

The problem is therefore not merely to retrieve something “similar”. It is to identify a **structural donor** and determine exactly what can be transported from it.

We define a donor as a source-bound theory, method, practice or artifact whose native structure supplies a candidate relation, control, failure mode or representation for a target scientific problem. Donors may be scholarly or practical. A scholarly parent can own the scientific mechanism. A recipe, manual, incident report or craft practice can donate a useful operational pattern without receiving scientific-authority transfer. The system must preserve that difference.

P-A tests three claims. First, a typed structural signature can recover remote parents missed by proximity-based search. Second, native reconstruction plus decision-preserving counter-probes can reduce false analogies. Third, the combined process can contract false novelty and improve research decisions under a fixed resource budget. These claims are tested against the strongest defensible union of mature parents, not against a single weak baseline.

## Results architecture

The Results section is frozen around four questions. Bracketed slots are populated only after protected execution.

### A hidden-parent benchmark separates retrieval from recognition

We construct cases in which the target description is generated independently from a known parent source while field names, canonical terminology and direct citations are hidden. Cases are stratified by:

- lexical distance;
- citation distance;
- semantic/domain distance;
- representation change;
- historical terminology;
- scholarly versus practical source mode;
- one-to-one parent, parent composition or no-valid-parent status.

Every case binds a gold native-parent card and a set of decision-relevant judgments that a valid donor relation must preserve. Negative cases include attractive narrative analogies that fail on scope, direction, uncertainty, intervention, competence or authority.

**Primary result slot PA-R1.** Report remote-parent recall at fixed review budget for lexical search, embedding retrieval, citation expansion, literature-based discovery, analogy prompting, expert-local search, strongest union and P-A. Report bootstrap or design-appropriate uncertainty and family-wise correction for frozen primary comparisons.

**Required sentence form:**

> Under the frozen search budget, P-A recovered [x/y] remote parents versus [comparators], with the largest difference in [pre-registered stratum]. The result [did/did not] survive equalization of retrieved-source count, model calls and expert minutes.

A gain that disappears after equalizing search effort is reported as a resource advantage, not a structural-method result.

### Native reconstruction and counter-probes test whether a donor is real

For each retrieved source, the system reconstructs:

`DonorCard = (native_problem, objects, operations, assumptions, evidence, failures, scope, authority, source_identity)`.

The target relation is represented as:

`DonorRelation = (target_problem, donor_card, correspondence, preserved_decisions, lost_decisions, counter_probes, approximation, confidence_status)`.

A candidate relation is rejected when it depends only on shared wording, when decisive target judgments change, or when the donor's native assumptions are absent. `NO_VALID_DONOR`, `PARENT_COMPOSITION_REQUIRED` and `CANNOT_CHECK` are valid outcomes.

**Primary result slot PA-R2.** Report false-analogy rate and native-verdict preservation for each arm. A donor relation that retrieves the correct source but fails native judgments is counted as scientifically incorrect.

**Required sentence form:**

> P-A reduced false analogies from [a] to [b] while preserving [c]% of registered native judgments. The remaining failures concentrated in [relation/failure family], indicating [specific limitation rather than generic error].

### Donor-faithful reduction tests novelty contraction

A retrieved parent matters only if the target contribution is correctly re-described after comparison. The system assigns one of:

- `PARENT_OWNED`;
- `PARENT_COMPOSITION`;
- `DOMAIN_SPECIALIZATION`;
- `PRACTICE_DONOR_ONLY`;
- `BENCHMARK_OR_FAILURE_DONOR`;
- `RESIDUAL_CANDIDATE`;
- `NO_VALID_DONOR`;
- `CANNOT_CHECK`.

The evaluator receives the target claim, donor cards and preserved/lost judgments without system labels. Novelty contraction is correct when the disposition matches the independently adjudicated relation and does not erase a genuine residual.

**Primary result slot PA-R3.** Report false-novelty and false-contraction rates. These are non-interchangeable errors: failing to find a parent inflates novelty; forcing a false parent erases a possible contribution.

**Required sentence form:**

> P-A changed the claim disposition in [n] cases, correctly contracting [x] false-novelty claims while incorrectly suppressing [y] genuine residuals. The non-compensatory native-fidelity gate [prevented/did not prevent] the dominant false-contraction mode.

### Cross-domain and human reproduction tests generality

The structural signature is frozen before two remote domains are selected. Domain experts independently reconstruct a subset of donor cards and judge whether the proposed correspondence preserves native decisions. A separate practical-source arm includes manuals, incident reports or competent procedures where legal and ethical access permits.

**Primary result slot PA-R4.** Report cross-domain transfer, expert agreement conditional on source dependence, and card-reproduction burden.

**Required sentence form:**

> The method transferred to [domains] with [effect/uncertainty]. Expert reconstruction agreed on [coordinates] and disagreed on [coordinates]. Practical donors contributed [operational pattern] but did not change scientific-parent ownership in [n] cases.

### Efficiency and component attribution

The system is evaluated under FULL, MINUS-signature, MINUS-native-card, MINUS-counter-probe, PARENT-replacement, strongest-union and SIMPLE controls. Compute, retrieval volume, expert time, annotation time and implementation burden are reported.

**Primary result slot PA-R5.** Identify whether any quality gain is attributable to structural representation, native reconstruction, counter-probes or additional effort.

**Required sentence form:**

> The Pareto frontier [included/did not include] P-A. Removing [component] changed [primary error] by [effect] at [cost], whereas replacing it with [parent] [recovered/did not recover] the effect.

## Discussion

P-A asks a deliberately uncomfortable question of scientific automation: before generating a new contribution, has the system learned enough of the remote knowledge space to know what it is building on?

A positive result would not show that structural search solves novelty. It would show that a typed, source-bound and decision-preserving procedure can improve the discovery of intellectually remote parents while reducing the false analogies produced by unconstrained analogy generation. The strongest contribution would be calibrated contraction: the system should become better at saying “this is already owned”, “this is a domain specialization”, “this is only a practical donor”, or “a genuine residual remains”.

The native-card requirement is central. A source cannot be safely absorbed from a title or abstract alone when its assumptions and failure conditions matter. This makes the method more expensive than ordinary retrieval. That cost is justified only if it changes research decisions and avoids expensive false novelty or false equivalence. Simple and local cases should therefore remain with ordinary search.

The distinction between scientific parents and practical donors also broadens the search universe without romanticizing every practice as hidden science. A recipe can expose staged transformations, checkpoints and recovery actions. An incident report can reveal a failure sequence. These structures may inspire a controller or benchmark, but they do not automatically support a scientific claim about another domain. P-A keeps inspiration, operational donation and scientific ownership separate.

Several negative outcomes are scientifically valuable. The strongest retrieval union may already recover the parents. Native expert review may show that a purported cross-field structure is too lossy. The method may improve recall only by spending more resources. Or structural cards may be useful primarily as an audit resource rather than a discovery algorithm. Each result contracts the paper appropriately.

## Methods

### Case construction and leakage control

Known-parent cases are built by one team and target descriptions by a separate team. Canonical names, direct quotations and identifying citations are removed under a documented transformation. Cases are checked for accidental leakage through distinctive equations, benchmark names and source metadata. Historical and practical sources retain provenance and access restrictions.

The benchmark contains positive, compositional and no-valid-parent cases. Outcome labels are unavailable to model and method developers after protocol freeze.

### Arms

1. lexical/BM25-style retrieval;
2. dense semantic retrieval;
3. citation-neighbour expansion;
4. literature-based-discovery parent;
5. analogy/LLM baseline;
6. expert-local search;
7. strongest union with expert-configured routing;
8. P-A FULL;
9. P-A component and parent replacements.

All arms receive the same source universe and authorized access. Models/checkpoints, prompts, retrieval depth, parallelism and human interventions are logged.

### Structural signatures

Signatures describe problem and decision structure rather than field labels:

- target state and transformation;
- observables and interventions;
- relation family and direction;
- uncertainty and failure model;
- support/evaluator structure;
- resource and authority constraints;
- terminal decisions.

Signature design is frozen before held-out domains.

### Native-verdict suite

For each parent, domain reviewers define judgments that should be preserved and counterexamples that should fail. Examples include causal versus associational reuse, exact versus approximate abstraction, procedural instruction versus demonstrated competence, and evidence versus authority.

### Outcomes

Primary outcomes:

- remote-parent recall;
- false-analogy rate;
- native-verdict preservation;
- false-novelty rate;
- false-contraction rate;
- resource-adjusted Pareto dominance.

Secondary outcomes:

- source diversity;
- time to correct disposition;
- expert reproduction agreement;
- censored-route frequency;
- error distribution by relation/source mode.

Critical failures—source fabrication, unauthorized source use, false parent suppression and authority laundering—are non-compensatory.

### Statistical analysis

The unit of analysis and dependence structure are defined before execution. Cases sharing a source family, target generator or reviewer are clustered or modelled accordingly. Primary effects use pre-registered estimands and uncertainty intervals. Resource matching is reported as curves when exact equality is impossible. Results are retained when negative or unresolved.

### Reproducibility and governance

Where permitted, release transformed cases, source identifiers, retrieval configurations, donor cards, evaluator rubrics, code and receipts. Restricted or community-governed sources receive access and purpose controls; absence from the open package is not treated as absence of evidence.

## Limitations frozen before results

- structural signatures can encode designer biases;
- hidden-parent benchmarks may not capture genuinely unprecedented research;
- domain experts can disagree on parent identity and scope;
- native reconstruction is expensive;
- source censorship and language access can block novelty checks;
- practical knowledge can be decontextualized by formalization;
- no finite search establishes global novelty.

## Data, code and AI-use statements — completion slots

- **Data availability:** `[populate from frozen release/custody record]`.
- **Code availability:** `[populate from release commit and environment]`.
- **Author contributions:** `[human accountable contributors only]`.
- **AI assistance disclosure:** `[document models, roles, verification and human accountability]`.
- **Competing interests:** `[complete before submission]`.

## Honest terminal

```text
P_A_MANUSCRIPT_SURFACE = COMPLETE_PRE_RESULTS
PROTOCOL_AND_RESULT_SLOTS = FROZEN
PROTECTED_RESULTS = OPEN
NATIVE_EXPERT_ADJUDICATION = OPEN
CROSS_DOMAIN_TRANSFER = OPEN
TOP_TIER_SUBMISSION_READY = NO
POSSIBLE_TERMINALS = ARTICLE__RESOURCE__PARENT_CONTRACTION__CANNOT_CHECK
```

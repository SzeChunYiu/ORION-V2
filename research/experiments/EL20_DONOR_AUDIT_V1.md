# EL20 — Diverse Adaptive-System Donor Audit (V1, reviewed)

**Stage:** EL20 of the Epistemic Locality / Perspective Plurality Verification Protocol V1 (issue #104).
**Status:** V1 — independently reviewed (adversarial criteria review + full citation verification; §8a).
**Nature:** curation + boundary verification, not a compute experiment (protocol burden:
`REQUIRED_FOR_STRONG_FLAGSHIP_GENEALOGY_CLAIM_BUT_CURATION_HEAVY_NOT_COMPUTE_HEAVY`).

**Purpose.** Source-bound reconstruction of exactly six donor families to verify the conceptual boundary of
Epistemic Locality and prevent category error. This document does NOT claim one law of intelligence, does not
rank families, and does not test whether any donor "possesses intelligence". Coordinate vocabulary mirrors
EL10's PerspectiveFrame coordinates (`environment_distribution`, `scale`, `timescale`, `system_boundary`,
`substrate_interface`, `criterion`, task family). Every empirical claim is anchored to author(+year) inline;
titles/venues given only where confidence is high; no page numbers, statistics, or quotes are invented. Where
a field or claim cannot be sourced confidently it is marked `CANNOT_SOURCE` rather than filled by plausible
reconstruction.

## 0. Cross-cutting invariants (enforced for every family)

1. `COGNITION != COLLECTIVE/CULTURAL ADAPTATION != EVOLUTIONARY ADAPTATION != MACHINE ADAPTATION` — four
   distinct adaptors, timescales, and retention channels; similar surface behavior does not imply a shared
   mechanism.
2. `FITNESS != TRUTH` — selection (biological, cultural, or reward-based) optimizes persistence/payoff under
   a criterion, never truth as such. Documented non-truth-tracking channels: neutral molecular drift
   (Kimura 1983, *The Neutral Theory of Molecular Evolution*); adaptive cultural processes producing
   maladaptive losses (Henrich 2004, "Demography and Cultural Evolution").
3. `SURVIVAL != NORMATIVE AUTHORITY` — nothing below licenses "donor X persists, therefore ORION should copy
   X". Donors motivate a hypothesis; they prove nothing (protocol V1, FLAGSHIP boundary).
4. No family is credited with a universal intelligence scalar; no family's optimum is assumed
   (`UNIVERSAL_INTELLIGENCE_DEFINITION = NOT_CLAIMED`).
5. Anti-analogy cases are load-bearing: each family carries one concrete case where superficially similar
   behavior has a different native mechanism, and copying the surface behavior into a deliberative agent is a
   category error.

---

## 1. human_individual_cognition

**AdaptiveSystemProfile:** single agent deciding under limited time, knowledge, and computation; rationality
is bounded and ecologically conditioned, not optimizing.

- **native_mechanism:** search + stopping rules that satisfice rather than optimize (Simon 1955, "A
  Behavioral Model of Rational Choice", QJE; Simon 1956, "Rational Choice and the Structure of the
  Environment", Psych Review); an "adaptive toolbox" of domain-specific heuristics, e.g. one-reason decision
  making (Gigerenzer & Goldstein 1996, "Reasoning the Fast and Frugal Way"; Todd & Gigerenzer 1999, *Simple
  Heuristics That Make Us Smart*).
- **adaptation_timescale:** ontogenetic (within-lifetime learning and practice), plus slower cultural
  channels external to the individual (family 4). Finer decomposition: `CANNOT_SOURCE`.
- **system_boundary:** the individual cognitive architecture with its memory and perceptual periphery; porous
  to external scaffolding (Clark & Chalmers 1998, "The Extended Mind", *Analysis*), but the satisficing
  computation is local.
- **retention_memory_channel:** individual biological memory; partially externalized into artifacts/notes
  (Clark & Chalmers 1998). Finer taxonomy: `CANNOT_SOURCE`.
- **environment_task_ecology:** heuristics succeed by matching environment structure — recognition-based
  inference works where recognition covaries with the criterion (Goldstein & Gigerenzer 2002, "Models of
  Ecological Rationality: The Recognition Heuristic", *Psych Review*); ecological rationality = fit between heuristic and
  environment, not general power (Todd & Gigerenzer 2012, *Ecological Rationality: Intelligence in the
  World*, Oxford UP).
- **transferable_to_orion_frame:** (a) explicit environment-structure conditioning of method choice — EL10's
  `environment_distribution` coordinate is the machine-native formalization of ecological rationality;
  (b) satisficing as a resource-bounded termination rule, compatible with metareasoning (Russell & Wefald
  1991, "Principles of Metareasoning"); (c) the recognition-heuristic lesson that missing information can be
  exploited rather than lamented — as a routing principle, not a belief policy.
- **non_transferable:** affect-grounded heuristics whose explanatory substrate is bodily affect (Slovic et
  al. 2002, "The Affect Heuristic"); social-emotional stopping rules; anything whose validity rests on the
  human Umwelt. Claims about conscious-deliberation mechanics: `CANNOT_SOURCE`.
- **anti_analogy_case:** see "Anti-analogy case" below.

### Anti-analogy case (human individual cognition)

Take-the-best ignores all cues after the first valid one (Gigerenzer & Goldstein 1996). Copied into ORION as
"drop most input features", this destroys the mechanism: its validity rests on a cue ordering matched to a
specific environment structure (Todd & Gigerenzer 2012) — non-compensatory sequential search, not evidence
that "less information is always better". Reading satisficing as "suboptimal cognition to emulate for
cheapness" is equally a category error: Simon's satisficing is a search architecture with an explicit
aspiration level and stopping rule (Simon 1955), not a defect to romanticize. The transferable structure is
the environment-conditional stopping rule; the surface behavior is "decide with little".

---

## 2. nonhuman_individual_embodied_cognition

**AdaptiveSystemProfile:** single non-human animal whose adaptive competence is co-located with body and
periphery; much "decision-like" behavior is closed sensorimotor coupling rather than central representation.

- **native_mechanism:** peripheral filtering + taxis loops: cricket phonotaxis is achieved largely by
  task-dedicated sensory filtering and bilateral comparison rather than central song representation (Webb
  2000, "What Does Robotics Offer Animal Behaviour?"; Webb 2001, "Can Robots Make Good Models of Biological
  Behaviour?", Behavioral and Brain Sciences); morphology carries part of the control load (Pfeifer & Bongard
  2006, *How the Body Shapes the Way We Think*); detour competence in the jumping spider *Portia* — indirect
  routes that temporarily lose sight of prey (Tarsitano & Andrew 1999); a convergently evolved,
  non-vertebrate memory architecture in octopus (Hochner 2012, "An Embodied View of Octopus Neurobiology",
  *Current Biology*).
- **adaptation_timescale:** two nested timescales — within-lifetime plasticity over evolutionary shaping of
  the periphery/body plan (Webb 2001). Finer split: `CANNOT_SOURCE`.
- **system_boundary:** brain–body–environment closed loop; the boundary that does the "computing" includes
  anatomy, not a central planner (Pfeifer & Bongard 2006; Webb 2001).
- **retention_memory_channel:** within-lifetime synaptic plasticity; octopus short/long-term memory
  organization differs radically from the vertebrate hippocampal template (Hochner 2012). Beyond this:
  `CANNOT_SOURCE`.
- **environment_task_ecology:** species-specific task ecologies — the cricket's auditory system is tuned to
  conspecific song; the spider's detours to its visual ecology; model adequacy in biorobotics is judged by
  replacing the animal in its loop, not by internal fidelity (Webb 2001).
- **transferable_to_orion_frame:** (a) task-dedicated front-ends: cheap peripheral filters as
  resource-bounded pre-processing before deliberation (Webb 2000); (b) Webb's modeling criterion —
  behavioral sufficiency does not establish mechanistic identity — is precisely the EL20 discipline of
  separating effective representation supported from native mechanism identified; (c) embodiment as an
  argument that the `system_boundary` coordinate changes what computation is needed (Pfeifer & Bongard 2006).
- **non_transferable:** morphological hardware (the cricket's filter is built into its auditory periphery;
  ORION is not embodied); species-bound sensorimotor Umwelt; *Portia*'s retinal-scanning route selection as
  a spatial-planning algorithm. How *Portia* internally represents detours: `CANNOT_SOURCE`.
- **anti_analogy_case:** see "Anti-analogy case" below.

### Anti-analogy case (non-human individual embodied cognition)

Cricket phonotaxis looks like "detect signal, form a belief about source location, act". Its native
mechanism is a peripheral matched filter plus bilateral taxis with no graded belief state anywhere (Webb
2000; Webb 2001). Implementing "scan and approach" in ORION as if it were an evidence-accumulation or
detection-theory policy substitutes a representation-level mechanism for a filter-level one — the exact
anthropomorphic substitution this stage must block. *Portia* is the mirror error: detour competence invites
"the spider plans routes over a map"; what is documented is indirect routes under temporary prey
invisibility (Tarsitano & Andrew 1999), and the internal representation is `CANNOT_CHECK`. In both
directions the transferable item is structural (task-dedicated filtering; boundary-dependent computation),
never the surface behavior.

---

## 3. animal_collective_decision

**AdaptiveSystemProfile:** a colony/flock as decision unit; no individual holds the global comparison; the
group-level choice is an emergent of distributed, interdependent local actions.

- **native_mechanism:** honeybee nest-site selection — scouts advertise sites via waggle dances with
  declining repetition, and choice terminates on a quorum of concurrent scout presences at a site, explicitly
  contrasted with consensus/majority mechanisms (Seeley & Visscher 2004, "Quorum Sensing during Nest-Site
  Selection by Honeybee Swarms"; Seeley & Buhrman 1999, "Group Decision Making in Swarms of Honey Bees"; Seeley
  2010, *Honeybee Democracy*); moving groups — decision accuracy depends on the ratio of informed to
  uninformed members and movement coupling, not on any member's graded confidence (Couzin et al. 2005,
  "Effective Leadership and Decision-Making in Animal Groups on the Move", *Nature*); self-organized trails
  in social insects broadly (Bonabeau, Dorigo & Theraulaz 1999, *Swarm Intelligence*).
- **adaptation_timescale:** ecological/episodic decision windows (days for a swarm's house-hunt; Seeley
  2010) riding on evolutionary shaping of the algorithm.
- **system_boundary:** the colony as unit; scouts are non-interchangeable samplers — each visits and
  advertises one or few sites; no bee compares the full option set (Seeley 2010).
- **retention_memory_channel:** no persistent central store; the process's "memory" is the physical
  distribution of dancers/attending bees across sites during the episode (Seeley & Buhrman 1999).
  Cross-episode colony memory: `CANNOT_SOURCE`.
- **environment_task_ecology:** cavity-nest discrimination under time pressure from swarm survival;
  speed-accuracy pressure is constitutive of the ecology (Seeley 2010).
- **transferable_to_orion_frame:** (a) quorum as a cheap termination criterion for decentralized evidence
  gathering — a stopping rule, not an aggregation formula (Seeley & Visscher 2004); (b) the EL10
  `system_boundary`/`scale` lesson: decision quality is a function of group composition and coupling (Couzin
  et al. 2005); (c) independence vs interdependence of information sources as a design variable for
  multi-agent evidence pooling (List, Elsholtz & Seeley 2009, collective decision modeling).
- **non_transferable:** the chemical/behavioral substrate — waggle-dance broadcasting and presence-counting
  quorum sensing are physical channels, not content-bearing message-passing (Seeley 2010); the
  one-scout-one-site sampling anatomy; replacing any ORION component's graded credences with "colony
  instinct".
- **anti_analogy_case:** see "Anti-analogy case" below.

### Anti-analogy case (animal collective decision)

Quorum sensing superficially matches Condorcet-style majority belief aggregation. The native mechanism is not
belief aggregation at all: scouts do not compare sites or pool credences; each advertises its own site with
decaying intensity, and the quorum is a threshold on concurrent physical presence at a location — a
different decision variable living in a different substrate (Seeley & Visscher 2004; Seeley 2010; List,
Elsholtz & Seeley 2009). Copying "poll N subagents, decide at 15" into ORION as a belief-quorum substitutes
an aggregation mechanism where the donor has a presence-counting stopping rule; and copying "informed
minority leadership" without the uninformed-majority coupling that makes it work (Couzin et al. 2005)
mistakes a dynamical property of the moving group for a property of the informed agent.

---

## 4. cultural_cumulative_adaptation

**AdaptiveSystemProfile:** a population-linked stream of practices; adaptive information accumulates across
generations in the distribution of behaviors and artifacts, not in any individual's inference.

- **native_mechanism:** biased social learning — conformity and prestige-weighted transmission (Boyd &
  Richerson 1985, *Culture and the Evolutionary Process*; Henrich & Gil-White 2001 on prestige); cumulative
  culture in which know-how outstrips what any individual could re-derive (Henrich 2016, *The Secret of Our
  Success*; Boyd & Richerson 2005, *Not by Genes Alone*).
- **adaptation_timescale:** many generations — faster and more flexible than genetic change, slower than
  individual learning (Boyd & Richerson 1985; Henrich 2016).
- **system_boundary:** the population of interacting learners; the adapting unit is the distribution of
  practices, individual minds being transmission nodes plus local innovators (Henrich 2016).
- **retention_memory_channel:** enacted practice and artifacts transmitted by imitation and teaching; much
  of it causally opaque know-how — practitioners execute functional procedures whose causal logic they
  cannot state (Henrich 2016's multi-step food-detoxification examples).
- **environment_task_ecology:** variable, risk-laden subsistence ecologies where individual experimentation
  is costly or lethal, favoring copying over re-inference (Henrich 2016).
- **transferable_to_orion_frame:** (a) the structural point that adaptive information can reside at
  population/lineage level — for ORION, a lineage or run archive is a legitimate retention channel distinct
  from any single session's context; (b) conditional transmission biases (copy when own payoff information
  is costly/ambiguous) as a routing policy under the EL10 `criterion`/cost coordinates (Boyd & Richerson
  1985).
- **non_transferable:** the normative and institutional content of norms; prestige and conformist mechanisms
  presuppose dyadic social structure with costly individual learning as the alternative; any transfer of the
  *truth* of culturally stabilized claims.
- **anti_analogy_case:** see "Anti-analogy case" below.

### Anti-analogy case (cultural cumulative adaptation)

Culturally transmitted practices are adaptive while their holders may possess false causal models: Henrich
(2016) documents functional practices (e.g. cassava detoxification) persisting alongside causally incorrect
beliefs attached to them. The mechanism selecting the practice is differential transmission and retention,
not evaluation of its truth; adaptive cultural dynamics can also produce maladaptive losses (Henrich 2004).
So the superficially similar ORION behavior — "reuse the accumulated prior solution" — splits into a
legitimate structural transfer (a lineage archive as retention channel) and a category error (reading
longevity or prevalence of a solution as evidence of its truth). Cultural adaptation optimizes persistence
and transmissibility under its ecology: `FITNESS != TRUTH` at the cultural layer.

---

## 5. evolutionary_adaptation

**AdaptiveSystemProfile:** lineages of replicators; adaptation = variation + differential retention under an
environment-relative fitness criterion. No beliefs, no representation, no foresight anywhere in the mechanism.

- **native_mechanism:** mutation, selection, drift, inheritance; major transitions change how information is
  stored and replicated rather than what any replicator "knows" (Maynard Smith & Szathmáry 1995, *The Major
  Transitions in Evolution*); long-term experimental evolution in *E. coli* documents adaptation and
  divergence over tens of thousands of generations (Lenski et al. 1991).
- **adaptation_timescale:** many generations; outcomes are historically contingent — the citrate-use
  innovation depended on potentiating history rather than a sweep of the best available variant (Blount et
  al. 2008, "Historical Contingency and the Evolution of a Key Innovation in an Experimental Population of
  *Escherichia coli*").
- **system_boundary:** the reproducing population/lineage; the individual organism is a vehicle, not the
  adapting unit.
- **retention_memory_channel:** genetic inheritance — a high-fidelity, semantics-free channel: it records
  what reproduced, not what was true.
- **environment_task_ecology:** an environment-relative fitness landscape; adaptation is local to a niche,
  and averaged over all problems no search algorithm dominates (Wolpert & Macready 1997, "No Free Lunch
  Theorems for Optimization") — the formal core of EL10's `environment_distribution` coordinate.
- **transferable_to_orion_frame:** (a) NFL as the mathematical statement that context-free method rankings
  are vacuous (Wolpert & Macready 1997); (b) selection as an explicitly criterion-bound search operator —
  useful to ORION only when the criterion is declared (Rice 1976, "The Algorithm Selection Problem"); (c)
  contingency as a warning that historical success of a lineage of methods is path-dependent evidence, not a
  ranking (Blount et al. 2008).
- **non_transferable:** everything epistemic. Evolution evaluates nothing against the world's truth; most
  molecular change is neutral drift (Kimura 1983), so heritable change is not even evidence of adaptation,
  let alone truth-tracking.
- **anti_analogy_case:** see "Anti-analogy case" below.

### Anti-analogy case (evolutionary adaptation)

"Evolution solved X, so the solution is validated" is the canonical fitness-to-truth category error. The
citrate outcome was contingent on prior enabling mutations, not on a comparison of alternatives (Blount et
al. 2008); and much of what is inherited reflects drift rather than selection (Kimura 1983). Translated to
ORION: "this policy/heuristic survived selection (a leaderboard, a bandit filter, a lineage archive)" is at
most persistence evidence under one registered criterion and environment distribution — it confers no truth
credential and no normative authority (`SURVIVAL != NORMATIVE AUTHORITY`; `EVOLUTION_EQ_COGNITION = FALSE`).
Evolution has no beliefs to transfer; only its formal, criterion-bound structure transfers.

---

## 6. machine_native_adaptation

**AdaptiveSystemProfile:** designer-specified optimizer/data/objective triples; adaptation is explicit
parameter or context change under a declared loss or reward. Native to ORION, so this family's donor role is
to expose which adaptation facts are already machine-native and which are imported metaphors.

- **native_mechanism:** credit assignment and value/policy update toward reward maximization (Sutton & Barto
  2018, *Reinforcement Learning: An Introduction*, 2nd ed.); adaptation-by-context without parameter change
  in few-shot prompting (Brown et al. 2020, "Language Models are Few-Shot Learners"). Mechanism of in-context
  adaptation: `CANNOT_SOURCE` (capability documented; implementing mechanism not established at
  source-confidence level).
- **adaptation_timescale:** two explicit, distinct channels — parameter updates at training time vs behavior
  change at inference time via context (Brown et al. 2020 compare few-shot against fine-tuning). This
  two-channel split is the machine analogue of the retention/timescale coordinate pair.
- **system_boundary:** the (objective, data, optimizer, deployment context) tuple; the boundary is a
  designer decision, hence always inspectable — the one family whose `substrate_interface` is fully
  documented by construction.
- **retention_memory_channel:** persistent weights (expensive, global updates) vs activations/context window
  (transient, cheap, per-episode) (Sutton & Barto 2018; Brown et al. 2020).
- **environment_task_ecology:** task distributions; performance is conditionable on problem features (Rice
  1976), no-free-lunch bounds any unconditioned claim (Wolpert & Macready 1997), and bounded compute makes
  computation selection itself a rational decision (Russell & Wefald 1991).
- **transferable_to_orion_frame:** directly — these are ORION's own substrate. The usable transfers are
  disciplines, not mechanisms: NFL context-binding (Wolpert & Macready 1997), algorithm-selection
  conditioning (Rice 1976), metareasoning about computation value (Russell & Wefald 1991), and the
  training/inference retention split as an explicit `timescale`+`substrate_interface` pair (Brown et al.
  2020).
- **non_transferable:** normative authority. Reward is a specification, not a truth channel: maximizing a
  specified reward is not evidence the reward tracks anything beyond itself (Sutton & Barto 2018
  reward-objective framing). Whether a deployed reward aligns with any user's intention: `CANNOT_CHECK`
  here (outside this stage's scope).
- **anti_analogy_case:** see "Anti-analogy case" below.

### Anti-analogy case (machine native adaptation)

Two mirrored errors. (1) "The model learns from the few-shot examples like a person learns from examples":
the documented phenomenon is prompt-sensitive behavior change without parameter update (Brown et al. 2020);
its implementing mechanism is `CANNOT_SOURCE`, so describing it as in-context *belief updating* is an
anthropomorphic mechanism substitution imported into the machine family itself. (2) "The RL agent learned
the task, therefore it knows the task": reward-maximization is a fitness-style criterion (Sutton & Barto
2018); reading policy competence as knowledge or truth-tracking is the same `FITNESS != TRUTH` slippage as
family 5, now with a designer-signed criterion. What transfers is the explicit objective/context bookkeeping;
nothing normative comes free with adaptation.

---

## 7. Distinction summary (verification grid)

| Family | Adaptor | Timescale | Retention channel | Criterion optimized | Truth-tracking? |
|---|---|---|---|---|---|
| human_individual_cognition | individual bounded agent | ontogenetic | individual memory (+ scaffold) | aspiration/satisficing under ecology | instrumental, environment-conditional |
| nonhuman_individual_embodied | individual brain-body loop | ontogenetic over evolutionary periphery | individual plasticity | task-ecological fit | no belief-level channel claimed |
| animal_collective_decision | colony/flock | episodic over evolutionary | distribution of dancers/presences | colony survival, speed-accuracy | presence-counting, not belief pooling |
| cultural_cumulative_adaptation | population of practices | generations | enacted know-how/artifacts | transmissibility/persistence | adaptive, can be maladaptive (Henrich 2004) |
| evolutionary_adaptation | lineage of replicators | many generations | genetic inheritance | environment-relative fitness | no; drift dominates much change (Kimura 1983) |
| machine_native_adaptation | optimizer/context tuple | training vs inference | weights vs context | declared loss/reward | exactly as specified, no more |

This grid is a boundary artifact: reading any row as a rank or a universal intelligence scale violates
invariant 4 and is out of scope.

## 8. Review checklist (mirrors protocol V1 EL20 evaluation criteria)

- [x] Preserves the distinction between cognition and evolutionary adaptation (invariants 1-2; families 1-2
  vs 4-5; grid in section 7).
- [x] Avoids anthropomorphic mechanism substitution (anti-analogy cases families 1-3, 6; Webb 2001 as the
  methodological warrant).
- [x] Identifies a genuine transferable structural distinction per family (each
  `transferable_to_orion_frame` names structure, never surface behavior).
- [x] States `CANNOT_SOURCE` / `CANNOT_CHECK` where applicable (families 1, 2, 3, 6; never silently filled).
- [x] Does not infer truth or normative authority from fitness/survival (invariants 2-3; anti-analogy cases
  families 4, 5, 6).
- [x] Independent/literature-grounded reviewer sign-off: PASS on all five criteria (§8a; criteria 1–5 PASS,
  structure PASS after two required fixes, citation scan clean after five corrections).

## 8a. Independent review record (2026-08-30)

An independent adversarial reviewer (fresh context, not the drafting agent) checked this synthesis against
the five protocol evaluation criteria, the structure contract, and ran a full citation fabrication scan
(every asserted title verified against the publication record; unconfident items web-verified).

**Protocol criteria: 5/5 PASS** — (1) cognition/evolution distinction preserved (invariant 1; family 5
"no beliefs, no representation, no foresight"; distinct retention channels); (2) no anthropomorphic
mechanism substitution (families 2, 3, 6 anti-analogy cases; Webb 2001 as methodological warrant);
(3) genuine transferable structural distinction per family (every `transferable_to_orion_frame` names
structure, not surface behavior; the ecological-rationality ↔ NFL ↔ algorithm-selection ↔
`environment_distribution` cross-family invariant); (4) `CANNOT_CHECK`/`CANNOT_SOURCE` stated where
applicable, never silently filled; (5) no truth or normative authority inferred from fitness/survival
(families 4, 5, 6; invariants 2–3; authority block).

**Corrections made during verification (all confirmed against the publication record):**

1. Seeley & Visscher 2004 re-titled to "Quorum Sensing during Nest-Site Selection by Honeybee Swarms"
   (*Behav Ecol Sociobiol* 56) — the draft's original title did not exist.
2. Goldstein & Gigerenzer 2002 venue corrected to *Psychological Review* 109 (draft had PSPI).
3. Webb 2000 re-titled to "What Does Robotics Offer Animal Behaviour?" (*Animal Behaviour* 60) — the
   draft's original title did not exist.
4. Hochner 2012 re-titled to "An Embodied View of Octopus Neurobiology" (*Current Biology* 22) — the
   draft's original title did not exist.
5. Todd & Gigerenzer 2012 corrected to the Oxford UP book *Ecological Rationality: Intelligence in the
   World* (found by the reviewer; draft had misattributed it to *Phil Trans R Soc B*).

**Fixes applied from review findings:** the `anti_analogy_case` field bullet restored in families 2–6
(nine-field contract now uniform); "Honeybee Swarms" orthography aligned to the journal title; grid row 2
criterion "task-ecological fitness" → "task-ecological fit" (reserving "fitness" for the selection-based
families, per invariant 1). Reviewer's discretionary note on the `CANNOT_SOURCE` vs `CANNOT_CHECK` boundary
was declined by design: the two-token convention is declared up front and both tokens mark unsourced
content; no field is silently filled.

**Reviewer bottom line:** criteria 1–5 PASS; structure PASS after fixes; citations clean after
corrections.

## 9. Authority

```text
grants_scientific_truth = false
grants_field_status = false
grants_primary_endpoint_change = false
claim_limit = "genealogy and boundary verification, not causal superiority"

UNIVERSAL_INTELLIGENCE_DEFINITION = NOT_CLAIMED
EVOLUTION_EQ_COGNITION = FALSE
NATURALISTIC_NORMATIVITY = FORBIDDEN
HUMAN_OPTIMUM = NOT_ASSUMED
MACHINE_OPTIMUM = NOT_ASSUMED
PARENT_SUFFICIENCY = VALID_TERMINAL
CURRENT_PRIMARY_PAPER_ENDPOINTS = UNCHANGED
```

## 10. Source register (confidence-anchored; venues only where high-confidence)

- Blount et al. 2008 (title confident); Lenski et al. 1991 (series start; venue omitted); Bonabeau, Dorigo &
  Theraulaz 1999, *Swarm Intelligence*; Boyd & Richerson 1985, *Culture and the Evolutionary Process*;
  Boyd & Richerson 2005, *Not by Genes Alone*; Brown et al. 2020 (NeurIPS).
- Clark & Chalmers 1998 (*Analysis*); Couzin et al. 2005 (*Nature*); Gigerenzer & Goldstein 1996 (*Psych
  Review*); Goldstein & Gigerenzer 2002 (*Psych Review*); Seeley & Visscher 2004 (*Behav Ecol Sociobiol*);
  Todd & Gigerenzer 1999 (Oxford); Todd & Gigerenzer 2012 (Oxford UP, book).
- Henrich 2004 (title confident); Henrich 2016, *The Secret of Our Success* (Princeton); Henrich & Gil-White
  2001 (prestige; author-year confident); Hochner 2012, "An Embodied View of Octopus Neurobiology"
  (*Current Biology*; one claim only); Kimura 1983 (Cambridge).
- List, Elsholtz & Seeley 2009 (author-year-title confident); Maynard Smith & Szathmáry 1995; Pfeifer &
  Bongard 2006 (MIT Press); Rice 1976 (*Advances in Computers*); Russell & Wefald 1991 (*Artificial
  Intelligence*).
- Seeley & Buhrman 1999; Seeley & Visscher 2004; Seeley 2010, *Honeybee Democracy* (Princeton); Simon 1955
  (*QJE*); Simon 1956 (*Psych Review*); Slovic et al. 2002 (chapter; author-year-title confident); Sutton &
  Barto 2018 (2nd ed., MIT Press).
- Tarsitano & Andrew 1999 (*Portia* detours; author-year only, no title asserted); Webb 2000, "What Does
  Robotics Offer Animal Behaviour?" (*Animal Behaviour*); Webb 2001 (*Behavioral and Brain Sciences*);
  Wolpert & Macready 1997 (*IEEE Trans Evol Comput*).

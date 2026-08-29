# Cognitive Science Omission Pass V1

**Status:** changed-vocabulary omission pass under issue #40. No new kernel component is admitted by this document.

## Question

Which important mechanisms of human thinking remain absent if we focus only on explicit reasoning, metacognition, error monitoring, curiosity and situated skill?

## Material additions

### 1. Memory is reconstructive and actively reorganized

Human memory is not a static log. Consolidation, reconsolidation, linking and adaptive forgetting change accessibility and relations among memories. Sleep can reorganize representations and facilitate later inference/insight.

**Machine implication:** preserve immutable scientific history while allowing a separate *working retrieval structure* to consolidate, link, compress and forget access paths. `history retention != constant retrieval priority`.

Candidate distinction:

`ArchiveMemory` — immutable evidence/history;
`WorkingMemoryPolicy` — adaptive access/replay;
`ConsolidatedSkillMemory` — learned reusable abstractions;
`SuppressedOrExpiredMemory` — retained but not normally active.

This prevents continual-learning efficiency from becoming deletion of negative scientific history.

### 2. Attention is not only top-down task selection

Attentional control reflects competition among top-down goals, bottom-up salience and selection history. Salient events can capture attention even when they are not task-relevant.

**Machine implication:** a frontier system needs a controlled `attentional_capture` route for unexpected events. It must also learn when to suppress repeated distractors.

This supplies a cognitive parent for serendipitous encounter generation.

### 3. Cognitive control depends on task representation

Modern cognitive-control research emphasizes that flexible selection and monitoring depend on the content/structure of task representations.

**Machine implication:** failure of control can be a representation failure rather than a policy failure. This strengthens P-C's representation-responsibility discriminator.

### 4. Developmental learning uses intervention, play and causal exploration

Children learn causal structure not only by observing correlations but by intervening, exploring and imagining alternatives.

**Machine implication:** frontier learning should distinguish passive evidence acquisition from intervention-capable causal learning and should retain exploratory/tinkering actions that build capability even before a final task reward is known.

### 5. Sleep/incubation and creative memory recombination

Human insight can improve after offline periods; creativity research links novel ideas to controlled retrieval and recombination of semantic/episodic memory rather than pure random generation.

**Machine implication:** add an offline `incubation/consolidation` research mode in which the machine does not take external scientific actions but reorganizes internal candidate relations, analogies and unresolved problems. Any resulting hypothesis remains proposal-only and must be externally tested.

### 6. Habit versus goal-directed control

Human behavior can shift from flexible outcome-sensitive control toward habitual/perseverative routines.

**Machine implication:** monitor when a successful workflow becomes a cached habit that continues after its assumptions/criterion change. Candidate failure class: `POLICY_HABIT_OUTLIVED_CONTEXT`.

### 7. Emotion/affect influences decisions

Emotion is a systematic influence on human judgment and choice, sometimes beneficial and sometimes harmful.

**Machine disposition:** do not imitate human affect merely for anthropomorphism. Instead ask what functional signals affect may implement—urgency, salience, loss sensitivity, social value, uncertainty tolerance—and compare them to explicit computational controls. No affect component is admitted by default.

### 8. Social learning and teaching

Humans learn from others, including prediction errors about others and culturally transmitted practices.

**Machine implication:** distinguish `testimony`, `demonstration`, `imitation`, `teaching signal`, and `independent evidence`. A teaching example can efficiently shape skill while remaining dependent on the teacher's knowledge/bias.

## Non-material or currently lower-priority additions

- consciousness as a general philosophical problem: scientifically important, but no current evidence that a consciousness variable is required for the V2 scientific-control decisions;
- generic dual-process 'fast vs slow' branding: useful as a parent of metacognitive control but too coarse as a kernel primitive;
- emotion simulation for human-likeness: not justified without a decision-relevant residual.

## Candidate framework changes after reduction

No new eighth kernel family is proposed. The material mechanisms can fit behind existing interfaces:

- memory/consolidation -> K1/K3 working state + immutable history distinction;
- attention/serendipity -> K5 opportunity/frontier policy;
- task-representation control -> K4 diagnosis/action selection;
- offline incubation -> K4/K5 proposal generation, non-authorizing;
- habitual-policy expiry -> K4 context/epoch validation;
- social learning -> K3 evidence/dependence + K4 acquisition;
- causal intervention/play -> K4/K5 experimental action repertoire.

## New benchmark candidates

1. `IMMUTABLE_HISTORY_VS_ADAPTIVE_RETRIEVAL` — efficiency gains cannot delete failure history.
2. `SALIENCE_CAPTURE` — useful unexpected event versus repeated irrelevant distractor.
3. `POLICY_HABIT_DRIFT` — cached workflow remains active after criterion/context changes.
4. `OFFLINE_INCUBATION` — candidate relation appears after internal recombination; must then survive fresh external test.
5. `TEACHER_DEPENDENCE` — multiple demonstrations from one teacher are not independent scientific corroboration.
6. `INTERVENTION_ADVANTAGE` — observational equivalence resolved only by active causal intervention.

## Terminal

`COGNITIVE_OMISSION_PASS_1 = MATERIAL_ADDITIONS_FOUND`

Therefore expanded human-cognition saturation is **not** yet re-earned.
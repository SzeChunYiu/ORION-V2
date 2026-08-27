# Context-Relative Structural Knowledge Space V0

**Status:** candidate formal programme; all parent ownership remains open.

## 1. Problem

“Two knowledge structures are close” can mean many incompatible things. A single semantic embedding can hide whether two objects share a role, an interface, predictive consequences, decision value, observable outputs, viable futures or merely vocabulary.

ORION-V2 therefore studies a family of relations parameterized by an explicit scientific context.

## 2. Candidate objects

For knowledge structure `K`, let a typed signature be:

`S(K) = (O, R, Q, I, T, Inv, Obs, Id, Eq, Scale, Unc, Dep, Res, Auth, Prov, Hist, Cost)`.

Let context be:

`C = (Q_C, I_C, D_C, B_C, kappa_C, target_C, tolerance_C, epoch_C)`

where:

- `Q_C`: admissible observations/queries;
- `I_C`: admissible interventions/experiments;
- `D_C`: downstream decision/task class;
- `B_C`: information/resource bound;
- `kappa_C`: protected validity/authority/integrity constraints;
- `target_C`: consequences that must be preserved;
- `tolerance_C`: permitted approximation;
- `epoch_C`: semantic/evaluation regime.

## 3. Relation families

The system must distinguish at least:

- exact isomorphism;
- structural/regular role equivalence;
- bisimulation or behavioural equivalence;
- contextual/interface equivalence;
- observational/Markov equivalence;
- predictive equivalence and minimal sufficient state;
- decision-relative dominance/equivalence and deficiency;
- rough indiscernibility with lower/upper approximations;
- safe abstraction, quotient or lumpability with loss certificates;
- viability/reachability equivalence;
- local compatibility, gluing and obstruction;
- approximate equivalence under tolerance;
- explicit incomparability.

A valid relation receipt states what is preserved, what is lost and which probe distinguishes the pair when the relation fails.

## 4. Mandatory scientific distinctions

`REDUNDANT_REPRESENTATION != OBSERVATIONAL_UNDERDETERMINATION`

`ROLE_EQUIVALENCE != SEMANTIC_IDENTITY`

`PREDICTIVE_EQUIVALENCE != INTERVENTIONAL_EQUIVALENCE`

`CURRENT_TARGET_SAFE_QUOTIENT != FUTURE_QUERY_SAFE_QUOTIENT`

`MULTIPLE_VALIDATORS != INDEPENDENT_EVIDENCE`

`APPROXIMATE_EQUIVALENCE != EXACT_TRANSPORT`

## 5. Candidate machine outputs

- `ISOMORPHIC`
- `ROLE_EQUIVALENT(C)`
- `BEHAVIOURALLY_EQUIVALENT(C)`
- `OBSERVATIONALLY_INDISTINGUISHABLE(C)`
- `PREDICTIVELY_EQUIVALENT(C)`
- `DECISION_DOMINATES(C, delta)`
- `SAFE_QUOTIENT(C, loss_bound)`
- `APPROX_EQUIVALENT(C, epsilon)`
- `INCOMPARABLE(C)`
- `DISTINGUISHED_BY(probe)`
- `CANNOT_CHECK`

Not every relation should yield a scalar metric. Partial orders, sets and symbolic witnesses are first-class.

## 6. Parent reconstruction obligations

Before claiming a common ORION theory, reconstruct strongest relevant work from:

- network structural/regular equivalence;
- modal logic and bisimulation;
- programming-language contextual equivalence;
- circuit/interface equivalence;
- causal Markov equivalence;
- comparison of statistical experiments;
- sufficient statistics and information loss;
- rough sets;
- abstract interpretation and closure systems;
- Markov lumpability and model reduction;
- computational mechanics/causal states;
- realization theory;
- viability theory;
- learning/knowledge spaces;
- gauge and representation equivalence;
- inverse-problem nonuniqueness/equifinality;
- sheaf/local-global obstruction.

If one parent already supplies an exact decision procedure for a relation, V2 should wrap its provenance/authority rather than reimplement a weaker version.

## 7. Quantitative tasks

1. classify the strongest justified relation for `(K1, K2, C)`;
2. produce relation witnesses or counterexamples;
3. estimate directional deficiency/information loss where parent theory permits;
4. find a minimum-cost distinguishing probe;
5. determine whether quotienting is safe for the declared target;
6. expire/reopen relation receipts when the context or epoch changes;
7. discover remote neighbours while controlling topic similarity;
8. preserve incomparability and `CANNOT_CHECK`.

## 8. Known-answer controls

- Thévenin/Norton interface equivalence;
- bisimilar transition systems;
- regularly equivalent network roles with different identities;
- Markov-equivalent causal graphs with intervention controls;
- gauge redundancy versus inverse-problem equifinality;
- predictive causal-state equivalence;
- safe and unsafe state aggregation;
- pairwise compatible views with global obstruction;
- same-topic/different-structure negatives;
- different-topic/same-structure positives.

## 9. Falsifiers

The programme contracts if:

- generic embeddings match all protected structural tasks;
- relation labels do not preserve native donor judgments;
- false analogy remains unacceptably high;
- a mature parent theory covers the complete required object;
- context changes make certificates too unstable for useful reuse;
- no machine discriminator can separate apparent relation families.

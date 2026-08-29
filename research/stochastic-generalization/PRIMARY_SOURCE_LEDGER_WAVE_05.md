# Primary Source Ledger — Wave 05

**Status:** parent identities and native-mechanism summaries; not exhaustive novelty evidence.

## Probabilistic equivalence and metrics

### Larsen and Skou — probabilistic bisimulation/testing

- Kim G. Larsen and Arne Skou, “Bisimulation through Probabilistic Testing,” POPL 1989; later journal development.
- Native mechanism: probabilistic transition systems, testing and bisimulation-based process distinction.
- Wave-05 use: parent of exact probabilistic behavioural equivalence.

### Desharnais, Gupta, Jagadeesan and Panangaden — metrics for labelled Markov processes

- “Metrics for Labelled Markov Processes,” Theoretical Computer Science 318(3), 2004; earlier CONCUR/NASA preprint lineage.
- Native mechanism: quantitative metrics robust to small probability changes, with zero distance tied to bisimilarity and compositional reasoning.
- Wave-05 use: parent of bounded stochastic-model distance.

## Stochastic abstraction and control

### Lavaei, Soudjani, Majumdar and Zamani — stochastic simulation functions

- compositional abstraction work for interconnected discrete-time stochastic control systems, 2017 onward.
- Native mechanism: simulation/storage functions quantify probabilistic distance between concrete systems and abstractions and support policy refinement with guarantees.
- Wave-05 use: parent of error-bounded model substitution.

### Nilim and El Ghaoui — robust MDPs

- Arnab Nilim and Laurent El Ghaoui, “Robust Control of Markov Decision Processes with Uncertain Transition Matrices,” Operations Research 53(5), 2005.
- Native mechanism: uncertainty sets over transition matrices and robust dynamic programming.
- Wave-05 use: parent of robust policy selection under transition uncertainty.

### Mannor, Mebel and Xu — coupled uncertainty

- “Robust MDPs with k-Rectangular Uncertainty,” Mathematics of Operations Research 41(4), 2016.
- Native mechanism: tractable structured coupled uncertainty sets.
- Wave-05 use: warning that uncertainty dependence/rectangularity changes both tractability and conservatism.

## Measurement and decision

### Blackwell — comparison of experiments

- David Blackwell, “Equivalent Comparisons of Experiments,” Annals of Mathematical Statistics 24(2), 1953.
- Native mechanism: task-relative informativeness and garbling.
- Wave-05 use: model distance must ultimately be interpreted through registered decisions/losses.

### NIST metrological traceability and uncertainty guidance

- Native mechanism: calibrated reference chains, uncertainty contributions and fitness-for-purpose limits.
- Wave-05 use: separate observable/calibration uncertainty from transition-model uncertainty and authority.

## Boundaries

- Total variation is one finite reference metric, not a universal stochastic simulation distance.
- Additive error composition can be loose and is invalid when link dependence/propagation is not justified.
- Robust MDP uncertainty-set assumptions are domain-specific and cannot be silently generalized.
- No parent above supplies ORION scientific authority, provenance, reopening or publication semantics; conversely ORION cannot claim their mathematical mechanisms.
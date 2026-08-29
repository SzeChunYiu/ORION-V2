# P-C Formalism Genesis Extension V1

P-C must decide not only which action to take inside a fixed problem representation, but when continued computation is unlikely to help because the representation itself is inadequate.

Add a pre-outcome action family:

`LOCAL_COMPUTE`, `RETRIEVE_PARENT`, `ADD_OBSERVATION`, `CHANGE_REPRESENTATION`, `PROPOSE_FORMALISM`, `ABSTAIN`.

A Formalism-Genesis action is justified only when registered evidence favors representation inadequacy over ordinary model/implementation/oracle failure and the expected value of a cheaper parent/local repair has been exhausted.

For held-out episodes compare a selector

\[
\pi(z)\in\{\mathrm{LOCAL},\mathrm{PARENT},\mathrm{OBSERVE},\mathrm{REPRESENT},\mathrm{FORMALISM},\mathrm{ABSTAIN}\}
\]

using only pre-outcome features `z` against always-local, always-parent and always-formalism policies.

Primary outcomes:
- true representation-deficit detection;
- false formalism escalation;
- missed representational deficit;
- time/resource to justified terminal;
- old-case regression after representation/formalism change;
- protected hidden-problem success.

The component is harmful if it mainly invents sophisticated languages for problems that a local variable, stronger parent or additional observation would solve.

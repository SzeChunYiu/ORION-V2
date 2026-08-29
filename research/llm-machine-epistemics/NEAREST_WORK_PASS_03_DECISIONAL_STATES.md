# Nearest-Work Pass 03 — Decisional States and the Orthogonal-Responsibility Correction

**Issue:** #51  
**Date:** 2026-08-29  
**Purpose:** absorb a direct historical parent found after the responsibility-decision refinement: Nicolas Brodu's predictive/decisional-state framework.

## 1. Direct parent

**Nicolas Brodu. _Reconstruction of Epsilon-Machines in Predictive Frameworks and Decisional States._ Advances in Complex Systems 14(5), 2011. arXiv:0902.0600. DOI: 10.1142/S0219525911003347.**

Primary sources:

- https://arxiv.org/abs/0902.0600
- https://nicolas.brodu.net/common/recherche/publications/decisional_states.pdf

## 2. What Brodu already owns

The paper begins with causal states: histories/configurations with identical conditional future distributions.

It then introduces a user-provided utility/payoff function and defines:

- **iso-utility states**: same maximal expected utility;
- **iso-prediction states**: same set of optimal predictions/actions;
- **decisional states**: intersection of iso-utility and iso-prediction states, interpreted as states leading to the same decision.

Crucially:

1. causal states refine the utility/prediction/decisional partitions;
2. decisional states are therefore **coarser than causal states** when the decision depends only on the future distribution and fixed utility function;
3. the paper defines a **decisional complexity** which, in the discrete case, is the entropy/information needed to encode decisional states;
4. transitions between decisional states correspond to events that lead to changes in decisions.

This is a very direct parent for any claim that #51 newly combines causal/predictive states with utility-defined decision states or newly measures their entropy.

## 3. Mandatory claim contraction

The following are now explicitly parent-owned/absorbed:

```text
predictive/causal states + user utility -> decision states = PARENT_OWNED (Brodu)
partition causal states by optimal decision/utility = PARENT_OWNED
entropy/information complexity of decisional states = PARENT_OWNED
transitions between decision states as decision-changing events = PARENT_OWNED CONCEPT
```

Therefore #51 cannot claim novelty for “decision-relative epistemic state” at this generic level.

## 4. Critical structural distinction

Brodu's decisional state is a **coarsening** of the causal state because the utility/decision is computed from the same future distribution represented by the causal state.

If #51's responsibility `r` satisfies

\[
A_r^*(H)
=
f(S_P(H))
\]

for some map of the linguistic predictive state, then the responsibility requires **zero additional state beyond `S_P`** under `ANY_OPTIMAL_ACTION`:

\[
C_{\mathrm{stat}}^*=0.
\]

In that regime the correct conceptual direction is Brodu-like decision coarsening, not ORION-style refinement.

### Consequence

A positive #51 state overhead is possible only when the declared epistemic responsibility depends on distinctions **not measurable from the linguistic predictive state**.

Examples include a responsibility whose action depends on:

- source/provenance identity that does not change the linguistic future law;
- evidence dependence/corroboration structure invisible to linguistic prediction;
- scope/assumption lineage;
- evaluator/version identity;
- obligation/claim identity needed for selective reopening;
- non-linguistic world/instrument state;
- externally supplied evidence/authority variables not contained in the linguistic future channel.

This motivates the term **orthogonal epistemic responsibility** only as shorthand: it means “not measurable from the declared linguistic predictive state,” not statistical independence.

## 5. Theorem DS1 — zero-extra-state parent regime

If there exists a Bayes-optimal selector

\[
d(H)=\bar d(S_P(H)),
\]

then

\[
\boxed{
C_{\mathrm{stat}}^*=0.
}
\]

This follows immediately from the selector formula and is not a novel theorem. It is a mandatory negative control.

For full fixed decision signatures `C_R`, if

\[
H(C_R\mid S_P)=0,
\]

then the joint predictive-responsibility refinement adds no information.

## 6. Theorem DS2 — positive static cost is a cross-channel obstruction

For `ANY_OPTIMAL_ACTION`,

\[
C_{\mathrm{stat}}^*>0
\]

iff **no** Bayes-optimal responsibility policy is implementable as a function of `S_P` alone.

Equivalently, at least one linguistic-predictive fibre lacks a common Bayes-optimal responsibility action.

This makes the positive state cost a precise cross-target/channel obstruction rather than a generic utility-state construction.

The equivalence is already contained in the selector/action-compatible partition formulation and is likely a direct decision-sufficiency corollary; novelty credit is package-level only.

## 7. Dynamic distinction from Brodu

Brodu constructs transitions between decisional states, but the coarser transition graph need not itself be a deterministic recursively sufficient state for an arbitrary responsibility process; transitions can collapse distinct causal-state transitions at the coarser level.

#51 explicitly asks a stronger internal-state engineering question:

> What is the minimum deterministic state that supports a Bayes-optimal responsibility action **and** has a well-defined update from current state plus future observation?

For tied actions this is the action-compatible right-congruence optimization in `JOINT_DYNAMIC_STATE_OPTIMIZATION_V1.md`.

Even here the mathematical substrate is strongly parent-owned by incompletely specified FSM minimization and information-state theory. The possible residual is the **relative entropy premium and cross-channel epistemic interpretation**.

## 8. Revised strongest residual

After Pass 03, the standalone paper lives or dies on the following narrower package:

1. **two-channel setup:** linguistic predictive state versus a declared responsibility channel that may depend on non-linguistic/history-side information;
2. exact static Bayes-action state cost relative to the linguistic predictive quotient;
3. zero-cost theorem/control for Brodu-like responsibilities measurable from `S_P`;
4. positive-cost obstruction only for responsibility distinctions absent from `S_P`;
5. joint static/dynamic Bayes-policy state optimization;
6. dynamic optionality premium after current policy compression;
7. bounded responsibility-family/horizon law;
8. LLM evaluation implication for provenance/scope/revision variables that can be invisible to linguistic prediction.

## 9. JMLR impact

This parent materially increases JMLR rejection risk.

A reviewer can now say:

> “Causal states plus utility-defined decisional states already give prediction- and decision-relative state and decision-state entropy.”

A valid response cannot be “we call the decisions epistemic.”

The paper must instead demonstrate why **cross-channel responsibility refinement and prospective deterministic revision state** changes a learning-system representation question beyond Brodu + Approximate Information State + ISFSM parents.

If not, close `CLASSICAL_PARENT_SUFFICIENT__MERGE_OR_DROP` or merge into the ORION flagship.

## 10. Required mechanical parent checks

The execution matrix must add Brodu 2011 with exact rows for:

- causal state definition;
- iso-prediction state definition;
- iso-utility state definition;
- decisional state definition;
- theorem/argument that causal states refine decisional states;
- decisional complexity definition `D=H(omega)` in the discrete case;
- transition graph discussion and whether coarse decisional transitions are deterministic/recursively sufficient.

The executor only locates/records exact passages/theorem numbering. The scientific disposition above is already fixed.

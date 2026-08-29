# LLM Machine Epistemics — Internal-State Theory Lane

**Status:** theory-first / pre-implementation.  
**Parent issue:** #51.  
**Related programme issues:** #48, #50.  
**Opening base:** `main@15206e121ef90e89dfcd1d5bfd6a9001ba001f1c`.  
**Outcome-generating LLM training:** not authorized and not required for the core paper.

## Research question

What properties must an autoregressive model's internal state possess in order to be sufficient not only for linguistic prediction, but also for a declared family of epistemic responsibilities?

The central distinction is

\[
\text{linguistic predictive sufficiency}
\quad\neq\quad
\text{epistemic responsibility sufficiency}.
\]

The programme studies the **minimal internal refinement** required to bridge that gap. The target is a theorem paper, not a new LLM implementation.

## Working thesis

Let `H` be the information/history available to a model, `Y+` the declared linguistic future, and `Z=f(H)` an internal representation. A representation may be sufficient—and even minimally sufficient—for `Y+` while losing information required for a distinct epistemic responsibility `Q` such as source-dependence, warrant, identifiability, scope, defeater sensitivity, or calibrated unresolvedness.

The theory aims to characterize:

1. when this separation is unavoidable;
2. the irreducible epistemic Bayes-risk induced by a representation;
3. the exact additional state needed for deterministic responsibilities;
4. how required state changes as the responsibility family grows;
5. what evidence-free downstream computation can and cannot repair;
6. an approximate predictive–epistemic rate region.

## Why this is an LLM paper rather than generic ORION governance

The object under study is **inside the model representation**. ORION contributes the responsibility-relative perspective and the discipline of keeping evidence, dependence, scope, unresolvedness and defeaters distinct. It does not assume that these quantities occupy named neurons or hand-designed coordinates.

An internal epistemic property is therefore representation-invariant. It may be distributed across activations. A future empirical realization would need the property to be both recoverable and causally usable; decodability alone is not sufficient.

Institutional/scientific authority remains external and is deliberately excluded from the model-generated responsibility family.

## Five-lens research panel

### A — Statistical decision and information theory
Owns sufficiency, Blackwell/Le Cam boundaries, entropy/risk identities, rate regions and lower bounds. Vetoes definition-near results presented as novel mathematics.

### B — Sequential prediction and state representation
Owns causal-state / predictive-state comparisons and the definition of the minimal linguistic predictive state. Vetoes one-step-prediction artifacts presented as general language-state results.

### C — LLM theory and mechanistic representation
Owns the bridge from abstract internal states to autoregressive models, representation non-identifiability and future causal-use tests. Vetoes architecture claims not implied by the formal results.

### D — Formal epistemology
Owns operational responsibility definitions, defeaters, underdetermination, source dependence and revision semantics. Vetoes global scalar trust/confidence substitutions for distinct epistemic responsibilities.

### E — Hostile ML reviewer / publication editor
Owns novelty subtraction, proof audit, assumptions, counterexamples and journal claim calibration. Vetoes a conceptual essay whose main theorem stack is already fully owned by classical parents.

## Research discipline

The programme must not claim that:

- LLMs do not learn;
- existing models contain no belief/truth/uncertainty information;
- Machine Epistemics replaces transformers or machine learning;
- internal epistemic variables must align with individual neurons;
- confidence, provenance, uncertainty or truth probes alone constitute epistemic sufficiency;
- institutional authority can be generated internally by a model;
- statistical sufficiency, causal states, Blackwell comparison, information bottleneck, rate distortion, data processing, representation identifiability or belief probes are ORION inventions.

## Current theoretical status

`THEORY_V1.md` establishes a finite/discrete foundation with proof sketches for the core separation and exact-information claims. It is deliberately scoped so every assumption is visible. The remaining work is primarily independent formal verification, countermodel search, approximate-frontier calculation and bibliographic saturation.

## Expected paper identity

Working title:

> **Predictive Is Not Epistemic: Responsibility-Sufficient Internal States for Autoregressive Models**

Primary target: **Journal of Machine Learning Research** if the final theorem residual survives strongest-parent subtraction. A field-theory venue remains the fallback if the mathematical residual is sound but too narrow for JMLR.

## Closure rule

The lane closes only as one of:

- `THEORY_PAPER_RESIDUAL_SUPPORTED`;
- `CLASSICAL_PARENT_SUFFICIENT__MERGE_OR_DROP`;
- `REPRESENTATION_IDENTIFIABILITY_ONLY__NO_NEW_RESIDUAL`;
- `THEOREM_SCOPE_TOO_WEAK_FOR_JMLR__FIELD_THEORY_PAPER_ONLY`;
- `CANNOT_CHECK_FORMAL_PROOF`.

A null/parent-sufficiency conclusion is valid scientific closure. No paper identity is protected for aesthetic reasons.

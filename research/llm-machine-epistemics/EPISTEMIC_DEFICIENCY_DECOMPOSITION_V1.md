# Epistemic Deficiency Decomposition V1

**Issue:** #51  
**Status:** candidate conceptual calculus built from standard information-theoretic identities plus the dynamic-state theory in `THEORY_STRENGTHENING_V2.md`.  
**Nonclaim:** the entropy/mutual-information identities are classical; the candidate contribution is the typed decomposition and its use as an internal-state audit for autoregressive Machine Epistemics.

## 1. Why a decomposition is needed

A language model can fail an epistemic responsibility for materially different reasons:

1. the required information was never present in the accessible history/input;
2. it was present but the internal representation discarded it;
3. it is not needed for the current responsibility but is needed to revise correctly after future observations.

Calling all three “hallucination”, “uncertainty” or “lack of knowledge” destroys the intervention logic. The correct remedy differs in each case:

- acquisition failure → obtain a new observation/source/tool;
- compression failure → preserve/refine internal state;
- future-option failure → retain dormant distinctions until their revision relevance expires.

---

# 2. Static acquisition and compression decomposition

Let:

- `Q` = declared epistemic responsibility;
- `H` = all information accessible to the model at the current point;
- `Z` = the actual internal representation used for the responsibility, generated from `H`.

Under Bayes-optimal logarithmic loss, the irreducible responsibility uncertainty from `Z` is

\[
H(Q\mid Z).
\]

Because `Z` is generated from `H`,

\[
\boxed{
H(Q\mid Z)
=
H(Q\mid H)
+
I(Q;H\mid Z)
}
\]

by the conditional mutual-information identity.

Define:

### Acquisition deficit

\[
\boxed{
A_Q=H(Q\mid H)
}
\]

This is uncertainty that remains even with the complete accessible history. It is not repairable by a better compression of the same history.

### Compression deficit

\[
\boxed{
C_Q(Z)=I(Q;H\mid Z)
}
\]

This is responsibility-relevant information available in the history but absent from the representation.

Therefore

\[
\boxed{
H(Q\mid Z)=A_Q+C_Q(Z)
}
\]

under log loss.

## Consequences

### Exact recoverability condition

If `Q` is deterministic from `H`, then

\[
A_Q=0.
\]

Any remaining Bayes uncertainty is entirely compression loss.

### Impossible exact recovery

If

\[
H(Q\mid H)>0,
\]

then no deterministic or stochastic representation generated solely from `H` can recover `Q` exactly almost surely without extra assumptions/information.

This is an **ingress/acquisition limitation**, not an internal-representation defect.

### Intervention mapping

| Deficit | Mathematical symptom | Correct intervention class |
|---|---|---|
| acquisition | `H(Q|H)>0` | new source, observation, measurement, retrieval, experiment, external authority where applicable |
| compression | `I(Q;H|Z)>0` | internal-state refinement, less aggressive compression, responsibility auxiliary constraint |
| neither | both zero | current information/state is sufficient for exact `Q` |

---

# 3. Value of a new observation

Suppose an external observation `X` becomes available.

With full current history `H`, the reduction in irreducible log-loss uncertainty is

\[
H(Q\mid H)-H(Q\mid H,X)
=
I(Q;X\mid H).
\]

Thus an observation has **genuine acquisition value** only to the extent that it contributes conditional information beyond what the current accessible history already contains.

With compressed state `Z`, the apparent value is

\[
I(Q;X\mid Z),
\]

which can be larger because `X` may redundantly re-supply information that was present in `H` but discarded from `Z`.

This yields an important distinction:

> Retrieval or tool use can compensate operationally for bad internal compression by re-acquiring discarded information, but that is not evidence that the original internal state was sufficient.

A resource-aware paper implication is therefore to distinguish:

- **new evidence acquisition**;
- **redundant re-acquisition caused by state loss**.

The latter may be correct behavior but carries avoidable cost.

---

# 4. Prospective / future epistemic deficiency

Now move to an autoregressive sequence.

Let:

- `H_t` = full accessible history at time `t`;
- `Z_t=f(H_t)` = current internal state;
- `X_{t+1:t+k}` = future observations/tokens/events acquired over the next `k` steps;
- `Q_{t+k}` = a responsibility that must be answered after those observations.

Define the **k-step prospective epistemic deficiency**

\[
\boxed{
\Delta_k(Z_t;Q)
=
I(
Q_{t+k};H_t
\mid
Z_t,X_{t+1:t+k}
)
}
\]

under the joint process distribution.

Equivalent log-loss form:

\[
\Delta_k
=
H(Q_{t+k}\mid Z_t,X_{t+1:t+k})
-
H(Q_{t+k}\mid H_t,X_{t+1:t+k}).
\]

### Interpretation

`Delta_k` measures past information discarded at time `t` that becomes relevant to the responsibility after future observations arrive and cannot be reconstructed from those future observations plus the retained state.

It is a direct information-theoretic notion of **future epistemic option value**.

---

# 5. Static sufficiency versus prospective sufficiency

It is possible that

\[
I(Q_t;H_t\mid Z_t)=0
\]

while

\[
\Delta_k(Z_t;Q)>0
\]

for some `k>0`.

That is the dynamic witness from `THEORY_STRENGTHENING_V2.md`: today's state is sufficient for today's responsibility yet insufficient for future revision.

Define:

### Current responsibility sufficiency

\[
C_Q(Z_t)=0.
\]

### k-step prospective responsibility sufficiency

\[
\Delta_j(Z_t;Q)=0
\quad
\forall j\le k.
\]

### Open-ended prospective sufficiency

Every declared future responsibility horizon has zero deficiency, subject to the process/scope being modelled.

This gives a hierarchy stronger than one-shot probing.

---

# 6. Epistemic option value of dormant state

Let `U_t` be a history feature that has no current linguistic or responsibility effect once `Z_t` is known:

\[
I(Y_t^+;U_t\mid Z_t)=0,
\]

\[
I(Q_t;U_t\mid Z_t)=0.
\]

If for a future responsibility

\[
I(Q_{t+k};U_t\mid Z_t,X_{t+1:t+k})>0,
\]

then `U_t` has **zero current value but positive future epistemic option value**.

This is the formal version of a Machine-Epistemics principle that cannot be reduced to “store what matters now.”

Examples include:

- source identity that matters only if a future retraction arrives;
- assumption lineage that matters only when a later boundary condition changes;
- alternative hypothesis identity needed only when new evidence discriminates among currently tied models;
- evaluator/version identity needed only after a future audit discovers a defect.

---

# 7. Connection to right-congruent dynamic state

The information-theoretic prospective deficiency and the partition-refinement theory answer complementary questions.

### Information view

\[
\Delta_k
\]

quantifies average excess future log-loss caused by forgetting current history.

### Exact finite-state view

`S_k` from `THEORY_STRENGTHENING_V2.md` is the coarsest exact state that preserves all registered outputs through horizon `k` under deterministic history extension.

For deterministic responsibilities with positive-support extensions, zero prospective deficiency across all registered extensions should correspond to refinement of the appropriate horizon partition. This equivalence is a registered formal-check target; no executor is asked to invent the statement.

---

# 8. Three-axis diagnostic state

For each responsibility `Q`, define the diagnostic triple

\[
\boxed{
\mathfrak D_Q(Z_t;k)
=
(
A_Q,
C_Q(Z_t),
\Delta_k(Z_t;Q)
)
}
\]

with:

- `A_Q` — acquisition deficit;
- `C_Q` — current compression deficit;
- `Delta_k` — prospective/future-option deficit.

Do **not** scalarize this triple by default. Different coordinates imply different interventions.

A possible internal-state report is:

| `A_Q` | `C_Q` | `Delta_k` | Interpretation |
|---:|---:|---:|---|
| 0 | 0 | 0 | accessible, retained, dynamically adequate |
| >0 | any | any | missing information at ingress; internal reasoning cannot close it from current history alone |
| 0 | >0 | 0 | current representation discarded currently useful responsibility information |
| 0 | 0 | >0 | current answer is adequate but state has lost future revision optionality |
| 0 | >0 | >0 | current and future representation inadequacy |

This is more informative than one confidence score.

---

# 9. Candidate resource consequence

Suppose re-acquiring a forgotten history feature through a future tool costs `c_X`, while retaining it in state costs `c_S` per horizon step. Then the optimal engineering choice depends on:

- probability that the future responsibility activates;
- expected conditional information of the future observation;
- retained-state cost;
- re-acquisition cost;
- risk of source disappearance or irreproducibility.

The current paper should **not** claim an optimal resource law without deriving it. But the decomposition identifies the correct variables for a later rate-resource theorem.

---

# 10. Publication relevance

The decomposition gives the paper a clearer answer to “what does this change for LLM research?”

A hidden-state probe that fails a responsibility cannot tell us by itself whether:

- the model never had access to the needed evidence;
- the information was accessible but compressed away;
- the current state is adequate but does not preserve future revision capability.

These are mathematically distinguishable failures and require different model/system interventions.

The theory therefore argues for evaluating internal representations against both:

1. **current responsibility sufficiency**;
2. **prospective revision sufficiency**.

That is a stronger target than static truth/confidence probing.

---

# 11. Mechanical verification targets

The executor only needs to verify the registered identities and fixtures:

1. `H(Q|Z)=H(Q|H)+I(Q;H|Z)` under `Q-H-Z`;
2. exact-recovery impossibility when `H(Q|H)>0`;
3. new-observation reduction `I(Q;X|H)`;
4. prospective identity for `Delta_k`;
5. canonical witness with current compression deficit zero and horizon-1 prospective deficit one bit;
6. correspondence between finite exact zero-prospective-deficiency and the registered horizon partition under stated support assumptions.

Any necessary extra support/Markov assumption must be surfaced, never silently inserted.

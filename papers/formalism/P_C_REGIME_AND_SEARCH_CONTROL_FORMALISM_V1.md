# P-C Formal Methods Insert V1 — Regime Selection and Conceptual Search

**Intended placement:** P-C Methods after `Policy`.

The adverse E20 pilot motivates a contextual rather than universal controller hypothesis. Let pre-outcome episode features be `z`. A regime selector chooses

\[
\pi(z)\in\{\mathrm{SIMPLE},F0,F1,F2,\mathrm{ABSTAIN}\}.
\]

The selector is frozen on development data and evaluated on held-out tasks. Post-outcome routing is not evidence. Its primary comparison is against always-SIMPLE, always-F0 and always-F2 under matched resource accounting.

When a probabilistic decision model is warranted, a scientific search action `a`—retrieve a donor, compare exemplars, seek a counterexample, prove an invariant, strengthen an oracle, change representation—may be ranked by expected reduction in registered decision loss:

\[
\mathrm{EVI}(a)
=\mathbb E[L(d\mid S)-L(d\mid S,X_a)]
-\lambda\,\mathrm{cost}(a).
\]

This is not a universal control law. If calibrated probabilities or utilities are unavailable, P-C must use the strongest robust/adaptive parent policy instead of inventing them.

Conceptual search adds a second state-transition class. Let

\[
C_t=(\Sigma_t,R_t,S_t,O_t,I_t,E_t,X_t,P_t,K_t)
\]

be a versioned concept state containing primitives, relations, scope, operational links, invariants, exemplars, counterexamples/anomalies, parents and authority/provenance. A proposed conceptual transition

\[
\tau:C_t\rightarrow C_{t+1}
\]

must preserve old-valid hidden cases

\[
R_{old}(\tau)=\frac{1}{|H_{old}|}\sum_{h\in H_{old}}
\mathbf1[J_{C_{t+1}}(h)=J_{C_t}(h)]
\]

and must either improve a prospectively hidden decision/prediction or establish a checked formal necessity. Otherwise `NEW_VOCABULARY != NEW_SCIENCE` and the transition receives `NO_SCIENTIFIC_RESIDUAL`.

### Control consequence

Conceptual development is not automatically an F2 action. The controller first asks whether a native formal/scientific parent, local representation change, or simpler search action suffices. Only an empirically supported residual can justify activation of the broader transfer-discovery mechanism.

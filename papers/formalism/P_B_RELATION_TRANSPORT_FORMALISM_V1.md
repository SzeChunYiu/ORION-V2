# P-B Formal Methods Insert V1 — Relation Transport, Invariance and Obstruction

**Intended placement:** P-B Methods within/after `Composition semantics`.

For an eligible source/target pair, let

\[
\phi=(\phi_V,\phi_R):\mathcal S_S\rightharpoonup\mathcal S_T
\]

be a decision-relative partial typed homomorphism. P-B distinguishes a valid relation from a merely similar pair through the violation vector

\[
\mathbf e(\phi)=
(e_{type},e_{rel},e_{direction},e_{inv},e_{approx},e_{measurement},e_{authority}).
\]

Critical violations are non-compensatory. Relation-family composition is therefore defined only when the relevant native parent supplies a valid rule or certificate.

For transformations `g` that are hypothesized to preserve the registered scientific decision `J`, test

\[
J(g\cdot x)=J(x)
\]

or, when the output has a lawful transformation,

\[
J(g\cdot x)=\rho(g)J(x).
\]

This operationalizes representation/measurement invariance without assuming that every transformation is scientifically irrelevant.

When native objects and transformations form categories, a candidate relation transport may additionally be tested as a functor

\[
F:\mathcal C_S\to\mathcal C_T,
\]

requiring

\[
F(\mathrm{id}_x)=\mathrm{id}_{F(x)},
\qquad
F(g\circ f)=F(g)\circ F(f).
\]

Failure of identity/composition or of a registered commuting diagram is an exact obstruction. Categorical tests are activated only for case families whose native parent semantics justify the construction.

For any proposed transport define

\[
\Omega(\phi)=\{c\in C(\phi):c\text{ fails in the target}\}.
\]

A critical obstruction gives

\[
\Omega_{critical}(\phi)\neq\varnothing
\Rightarrow \mathrm{LOCAL\_OR\_GLOBAL\_OBSTRUCTION}.
\]

This supplies a formal target for PB-R2: false-exact composition, missed-valid composition, decision-stable approximation and explicit countermodels can be evaluated with proof assistants, model checking or exhaustive finite search where applicable. Empirical transport remains subject to native empirical evidence; a formal commuting diagram cannot establish an empirical invariance by itself.

### Selective reopening

Let a downstream claim `q` have sufficient support families `H_q={H_1,...,H_m}`. After invalidating relation `r`, `q` must reopen iff every complete sufficient family contains an invalid member:

\[
\mathrm{Reopen}(q,r)=1
\iff
\forall H_j\in H_q,\ H_j\cap \mathrm{Invalid}(r)\neq\varnothing.
\]

This proposition becomes a theorem only after the support semantics and proof obligations are checked; otherwise it remains reference semantics for the exact finite benchmark.

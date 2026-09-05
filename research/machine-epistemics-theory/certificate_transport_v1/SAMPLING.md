# Finite-sample, selection-aware certificate transport

**Extension:** CT-10 through CT-12 of ME-CERTIFICATE-TRANSPORT-V1. Specification committed before this extension's calibration as `3803ee2481c65b3909db2b0e50338efff0bdf377`. The primary complete-model study and the earlier deductive addendum remain unchanged. This is a conditional statistical theorem with exact numerical calibration, not a real-model study.

## CT-10. A finite-sample upper bound, not a sample frequency promoted to truth

Let K be the sum of n IID Bernoulli failure indicators with unknown fixed probability p. Fix n>=1 and alpha in (0,1) before observing this sample. On the rational grid with denominator d=2^b define

\[
 U(n,k,\alpha)=\begin{cases}
 1,&k=n,\\
 \min\{u\in\{0,1/d,\ldots,1\}:\sum_{j=0}^{k}\binom nj u^j(1-u)^{n-j}\le\alpha\},&k<n.
 \end{cases}
\]

**Theorem.** For every p in [0,1], `Pr_p[p <= U(n,K,alpha)] >= 1-alpha`.

**Proof.** When k<n the binomial lower tail is nonincreasing in p. This follows, for example, by coupling each Bernoulli indicator as 1{V_i<=p} for independent uniform V_i. Thus U(n,k,alpha)<p implies `Pr_p[K<=k] <= alpha`. If undercoverage is possible, let k_star be its largest possible failure count. It is less than n because U(n,n,alpha)=1. The undercoverage event is contained in K<=k_star, whose probability is at most alpha by the preceding implication. Otherwise its probability is zero. This proves the bound. QED.

This is a conservative grid-rounded form of exact one-sided binomial inversion, with the classical Clopper-Pearson method as parent [S6]. The grid upper endpoint lies above the unrounded root by less than 1/d. `sampling.py` uses exact integer powers and rational comparisons; no floating-point root is trusted. For k<n it records a valid tail at U and failure of the tail criterion at the preceding grid point. The all-failures case is explicit, not a division-by-zero exception.

Zero observed failures do not imply p=0. The computed upper limit for 0 of 12 at alpha=1/20 is `14479/65536`, about 0.221. That is a property of the hypothetical sampling model, not an observed OCM failure rate. Optional stopping, dependent examples, data-selected events, mismeasured labels and unregistered sample exclusions violate the stated assumptions unless separately justified.

## CT-10b. Transport an update using labeled reference data and unlabeled disagreement

Let f and g be two deterministic predictors, and let their failure indicators be determined by the **same** task-error predicate applied to their predictions and the true outcome. For a common world (x,y), define F={f fails}, G={g fails} and D={f(x)!=g(x)}. Then

\[
 F\triangle G\subseteq D,\quad P(G)\le P(F)+P(D).
\]

**Proof.** Equal predictions under the same error predicate have equal failure indicators. A point whose failure indicator changes therefore belongs to D. Also G is contained in F union D. Take probabilities. QED. In binary 0/1 classification the first inclusion is equality. With multiple classes, different predictions can both be wrong, so the inclusion can be strict.

Suppose n_old labeled reference examples estimate P(F), and n_pairs IID paired predictions estimate P(D). Apply CT-10 at confidence-failure levels alpha_old and alpha_pairs to obtain u and v. If deployment Q satisfies a separately justified **joint input/outcome** bound TV(P,Q)<=epsilon, then, with probability at least 1-alpha_old-alpha_pairs over the calibration samples,

\[
 Q(G)\le\min(1,u+v+\epsilon).
\]

**Proof.** Each upper bound fails with probability at most its assigned alpha. The union bound needs no independence between the two estimators. On their simultaneous success event, combine the pointwise inequality above with `Q(G)<=P(G)+epsilon`. QED.

The predictors/events must be fixed independently of their evaluation samples, or covered by the simultaneous guarantee below. Conditioning on independent training data is admissible. Reusing evaluation outcomes to choose an unregistered update is not.

The paired predictions require no new truth labels, but they are not free: count n_old reference labels and reference predictor evaluations, n_pairs paired inputs, 2*n_pairs predictor evaluations, both confidence calculations, storage, and evidence custody. The unknown distribution P need not be provided as a complete table in this extension. The drift premise still needs evidence; an arbitrary epsilon is not a verified certificate.

**Joint versus covariate drift.** A bound on P_X versus Q_X alone does not establish the required joint bound. Conditional-label invariance or another explicit bridge is necessary. For a constant x, changing y from 0 in calibration to 1 in deployment leaves the input marginal unchanged but changes the failure rate of f(x)=0 from zero to one. This is why domain-adaptation assumptions must remain load-bearing [S7].

**Hypothetical numerical example, not data.** With 2 failures in 100 reference examples, 1 disagreement in 100 paired examples, alpha_old=alpha_pairs=1/40, and an externally justified epsilon=1/50, the exact grid calculation returns reference bound `4613/65536`, disagreement bound `1785/32768`, and transported risk at most `237343/1638400` (about 0.14486267) with at least 19/20 calibration coverage. This does not mean that an individual output is true with that probability or that the assumptions were checked.

`transport_from_counts` always labels its output `CONDITIONAL_RISK_BOUND`, states `premises_verified_by_this_function=false`, and grants neither exact-truth warrant nor action authority. No input counts are authenticated by this reference function.

## CT-11. Selection needs simultaneous validity

For a fixed finite family of m candidate events, assign each candidate failure budget alpha/m. Apply CT-10 to its fixed-size IID evaluation sample. With probability at least 1-alpha all m upper bounds hold simultaneously, even when the candidates share samples and their errors are dependent. Therefore any subsequent selection among this registered family inherits its candidate's bound.

**Proof.** The probability that at least one candidate's bound fails is at most the sum m*(alpha/m)=alpha. On the complement every member is covered, including the selected member. QED. More generally use nonnegative allocated budgets summing to at most alpha, with positive budgets on the events where this inversion is applied. A family invented after evaluation does not meet the fixed-family premise.

**Exact selection counterexample.** Consider four fixed predictors, each with true error probability 3/4. A single IID calibration example contains four independent Bernoulli(3/4) error coordinates. Each predictor individually receives the valid n=1, alpha=1/2 binomial bound: 1/2 if it made no observed error, otherwise one. Select an error-free-on-calibration predictor whenever one exists. The selected upper bound undercovers its true risk whenever at least one coordinate is zero, with probability

\[
 1-(3/4)^4=175/256>1/2.
\]

Thus the individually valid 50% procedures do not retain nominal coverage after selection. Allocating alpha/4=1/8 gives a zero-error upper bound 7/8, which covers 3/4 for every vector in this witness. `sampling.py` enumerates all 16 vectors and computes both probabilities exactly. This example proves a failure of the naive rule, not optimality of Bonferroni allocation or a general impossibility of adaptive inference. Time-uniform and uniformly valid alternatives are separate parents and are not implemented here.

## CT-12. No nontrivial unrestricted-future certificate from past data alone

Fix an observed calibration history and a predictor. If the admitted environment class permits any future distribution independently of that history, it includes two environments with the same observed past but respectively no future failures and certain future failure, provided the predictor has at least one possible success and one possible failure world. Any history-only certificate valid for both must allow deployment risk one.

**Proof.** Concentrate the future law on a success world in the first environment and on a failure world in the second. Their past observations and predictor artifacts are identical. A bound below one computed solely from that shared history is false in the second. QED. The constant-input, changed-label construction above supplies a two-world witness, even with equal input marginals.

This is a scoped indistinguishability result, not a universal statement that learning or prediction is impossible. Its purpose is to require an actual deployment-stability assumption rather than invent one from a hash or a sample. Parent: domain-adaptation impossibility/identifiability arguments [S7]; our proof is the elementary unrestricted special case, not a reconstruction of their full theorem.

## Calibration, resources and remaining work

The fixed grid executes 270 binomial limits, 234 tail and 234 predecessor checks, 612 exact coverage cells over p in {0,1/16,...,1}, 1,536 pointwise binary inclusion checks, a strict multiclass witness, the 16-vector selection example, and invalid-input refusals. These are deterministic calculations on hypothetical finite models, not empirical replications.

For each upper bound, b bisection steps evaluate at most n+1 integer terms. Exponentiation, binomial coefficients, and integer bit length are charged separately from a simple arithmetic-operation count; intermediates can have O(nb) bits. The implementation caps n at 256 and b at 32 and returns `CANNOT_CHECK` beyond those exact-computation limits. The statistical theorem itself is not restricted to n<=256. No claim about optimum interval length, production performance, or least possible labeling cost is made.

Still open: validity under dependent/optional-stopped samples; simultaneous guarantees for data-generated infinite update families; noisy or conflicting truth labels/checkers; evidence for joint deployment drift; and OCM's actual evidence/commitment boundary. A deterministic no-change proof may supply D=empty exactly, but zero observed disagreements alone cannot.

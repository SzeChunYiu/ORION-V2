# MEG-07 Frontier F1 — extraction no-drop: impossibility without discriminating structure

**Status:** theorem/counterexample result for issue #329 F1. **NO NOVELTY, OCM-SUPERIORITY OR FIELD-STATUS CLAIM.** The current OCM M2 development result (47/50 under one propagated-background score, with three attributed misses) is motivation only and is not used as authority for this theorem.

## Question

Can a task-blind extraction/ranking rule guarantee that every task-decisive reachable atom is retained when the extractor does not observe a structure that identifies which reachable atoms are decisive?

## Model

For one registered query state let:

- `V={v1,...,vn}` be the finite candidate atoms reachable and eligible for extraction;
- `z` be **all information available to the extractor**: KSO structure, query/seed, activation, background, warrants, typed relations, scores, ids and any other declared observable feature;
- `D⊆V` be the task-decisive set: atoms whose omission can change the registered downstream correct answer/decision;
- `E(z)` be a deterministic extractor with `|E(z)|≤k<n`;
- a task family is **relevance-nonidentifiable at z** when it contains two or more valid task instances with the same extractor-visible `z` but different decisive sets. The strongest symmetry case contains every singleton `{v}` as an admissible decisive set at the same `z`.

For a randomized extractor, `E(z,ω)` is a distribution over subsets of size at most `k`. A **zero-error no-drop guarantee** means `D⊆E(z,ω)` with probability 1 for every admissible task instance.

This formalizes what “task-blind” means; it does not assume the score is PageRank, surprise, IDF or any particular formula.

---

## Theorem F1.1 — deterministic no-drop impossibility

If the task family at one extractor-visible state `z` contains every singleton decisive set `{v}` for `v∈V`, and the extractor capacity is `k<n`, then no deterministic extractor `E(z)` can satisfy no-drop for every task in that family.

### Proof

`E(z)` is one fixed subset because all tasks present the same extractor-visible state. Since `|E(z)|≤k<n=|V|`, choose `v*∈V\E(z)`. The admissible task with decisive set `D={v*}` has `D⊄E(z)`. Therefore the extractor drops a decisive atom on that task. ∎

### Stronger finite-family form

For any collection of admissible decisive sets `𝒟(z)`, a deterministic capacity-`k` no-drop extractor exists **iff** there is an extractor-visible subset `C(z)⊆V` with `|C(z)|≤k` such that

`⋃_{D∈𝒟(z)} D ⊆ C(z)`.

Necessity follows because one fixed output must contain every admissible decisive set; sufficiency follows by outputting `C(z)`.

Thus a universal guarantee is not a property of the ranking formula alone. It is a property of the **information available about the task family** plus capacity.

---

## Theorem F1.2 — randomized zero-error impossibility

Under the singleton-symmetry assumptions above, no randomized extractor that outputs at most `k<n` atoms almost surely can have a zero-error no-drop guarantee for every task.

### Proof

Let `p_v = Pr[v∈E(z,ω)]`. Since every realized output has size at most `k`,

`Σ_v p_v = E[|E(z,ω)|] ≤ k`.

Hence some `v*` has `p_v* ≤ k/n < 1`. For the admissible task with `D={v*}`, the miss probability is at least `1-k/n>0`. Therefore zero-error no-drop is impossible. ∎

Randomization may improve average recall under a declared task distribution, but that is an empirical/risk statement, not a universal preservation theorem.

---

## Theorem F1.3 — sufficient discriminating-structure certificate

Suppose a registered task family provides a machine-checkable `ExtractionCoverageCertificate(z,C,scope,epoch)` proving:

1. `C⊆V` is computed only from declared extractor-visible information;
2. `|C|≤k`;
3. for every task instance in the certificate scope compatible with `z`, its decisive set `D` satisfies `D⊆C`;
4. the certificate is bound to the task-family definition, KSO/query representation, extraction eligibility rule, checker, scope and epoch.

Then the extractor `E(z)=C` has exact no-drop on that registered scope.

### Proof

For every admissible task, condition 3 gives `D⊆C=E(z)`. ∎

If condition 3 cannot be checked, the machine has no no-drop certificate. It may still use a heuristic ranker, but omission cannot become evidence that no decisive atom existed.

---

## Corollaries for OCM

1. **Surprise is a retrieval heuristic, not an epistemic completeness certificate.** Uniform, propagated and future fan-out-aware variants may be compared on recall/cost, but no score earns universal no-drop merely by improving a development set.
2. **The remaining 3/50 M2.1 misses do not require a theorem to be tuned away.** They demonstrate that the current observable score is not a no-drop certificate on that development family; a successor score needs a frozen empirical identity, while the theorem says what additional information would be required for a guarantee.
3. **Extraction failure cannot prove absence.** If a decisive object could be outside the extracted subset under the registered information model, downstream state is `SEARCH_INCOMPLETE`/`CANNOT_CHECK` for any claim requiring completeness, not negative truth.
4. **Capacity matters.** `k=n` trivially retains everything but ceases to be an extracting/compressing mechanism. Any meaningful `k<n` guarantee must exploit structure that restricts the admissible decisive sets.
5. **MEG-31 accounting applies.** A discriminating certificate carries information; it must be counted rather than hidden in an oracle selector.

---

## Parent subtraction

- Personalized PageRank/local graph methods own particular navigation/ranking mechanics; the KSO does not claim PageRank contribution vectors as ORION inventions.
- Information-retrieval and surprise/centrality methods own many scoring choices.
- Wolpert & Macready's no-free-lunch work is the broad parent intuition that algorithmic advantage requires structure in the problem class. The theorem here is narrower and elementary: it is a finite indistinguishability/capacity argument over extractor-visible states, not a claim to extend the general NFL theorem.

The scientifically relevant residual is therefore a **boundary theorem**: no universal no-drop result exists without discriminating task structure; when such structure exists it must be explicit and certificate-bound.

---

## Hostile cases

The exact checker covers:

- every deterministic selected subset with `n=4,k=2` against every singleton relevance relabeling — each selector has an admissible miss;
- a uniform randomized `k`-subset extractor, confirming inclusion probability `k/n` and positive miss probability;
- positive certificate case with `D⊆C`, `|C|≤k`;
- certificate overflow (`|C|>k`) rejected;
- one task family whose union of possible decisive atoms is size `k+1`, proving no fixed capacity-`k` set can cover it;
- no-alarm case where the admissible decisive union has size exactly `k`.

## Terminal

```text
MEG-07 = NO_UNIVERSAL_NO_DROP_WITHOUT_DISCRIMINATING_STRUCTURE
POSITIVE_SCOPE = EXACT_WHEN_EXTRACTION_COVERAGE_CERTIFICATE_PROVES_DECISIVE_SUPERSET_WITHIN_CAPACITY
GENERAL_NOVELTY = NOT_ESTABLISHED
```

This terminal is compatible with future empirical improvement of OCM's surprise model; such improvement changes retrieval quality, not this impossibility boundary.

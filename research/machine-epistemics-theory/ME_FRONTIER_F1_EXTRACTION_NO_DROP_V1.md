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

For any collection of admissible decisive sets `𝒟(z)`, a deterministic capacity-`k` no-drop extractor exists at this one fixed state **iff** there is an extractor-visible subset `C(z)⊆V` with `|C(z)|≤k` such that

`⋃_{D∈𝒟(z)} D ⊆ C(z)`.

Necessity follows because one fixed output must contain every admissible decisive set; sufficiency follows by outputting `C(z)`.

At a fixed state this is simply `|⋃𝒟(z)|≤k`. Uniformly over many states, an
effective guarantee additionally requires a computable cover from the registered
observable input and within its resource budget. Set-theoretic existence is not
an efficient certificate-construction theorem. Distinct decisive sets alone do
not imply impossibility: `{a}` and `{b}` can both be covered when `k=2`.

Thus a universal guarantee is not a property of the ranking formula alone. It is a property of the **information available about the task family** plus capacity.

---

## Theorem F1.2 — randomized zero-error impossibility

Under the singleton-symmetry assumptions above, no randomized extractor that outputs at most `k<n` atoms almost surely can have a zero-error no-drop guarantee for every task.

### Proof

Let `p_v = Pr[v∈E(z,ω)]`. Since every realized output has size at most `k`,

`Σ_v p_v = E[|E(z,ω)|] ≤ k`.

Hence some `v*` has `p_v* ≤ k/n < 1`. For the admissible task with `D={v*}`, the miss probability is at least `1-k/n>0`. Therefore zero-error no-drop is impossible. ∎

Randomization may improve average recall under a declared task distribution, but that is an empirical/risk statement, not a universal preservation theorem.

The bound is tight in the singleton-symmetric game: uniform sampling of a
`k`-subset attains `p_v=k/n` for every `v`, so worst-case miss is exactly
`1-k/n`. More generally, finite `V` implies that randomized zero-error no-drop
exists iff `|⋃𝒟(z)|≤k`: each atom in the union must be retained almost surely,
and a finite intersection of probability-one events has probability one.

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

The reference checker implements only a **finite family defined by explicit
enumeration**. Its certificate binds the full eligible universe and a canonical
digest of the complete decisive-set family, in addition to the six contextual
identities above. Missing registration, omitted family rows, stale identities,
unknown iterators, and malformed atom sets cannot certify coverage; selected
atoms outside the eligible universe are rejected. An explicitly registered
empty family has a vacuous set-theoretic cover, and makes no claim about any
real task. A digest binds supplied content; it cannot prove that an empirical
sample exhausts a natural task family, or that the supplied decisive labels are
semantically correct. Those are external theorem/registration obligations.

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
- Wolpert & Macready's [No Free Lunch Theorems for Optimization](https://doi.org/10.1109/4235.585893) is the broad parent intuition. Its averaging theorem is not invoked to prove the present result. The proof here is the elementary finite indistinguishability/capacity argument given above; it requires neither a distribution over all objective functions nor an extension of the NFL theorem. The primary publisher record was consulted on 2026-09-05; its full PDF was unavailable, so full-source reconstruction of NFL is `CANNOT_CHECK` and carries no proof dependency here.

The scientifically relevant residual is therefore a **boundary theorem**: no universal no-drop result exists without discriminating task structure; when such structure exists it must be explicit and certificate-bound.

Primary-source reconstruction, consulted 2026-09-05:

| Parent | Native observable and operation | Consequence for this theorem |
|---|---|---|
| [Andersen et al., Local Computation of PageRank Contributions](https://www.internetmathematicsjournal.com/article/1456-local-computation-of-pagerank-contributions.pdf) | Source-to-target contributions from personalized PageRank; approximates substantial contributors locally. | A numerical contribution guarantee is relative to the registered graph/seed. With unchanged graph and scores under decisive-set relabeling, it cannot identify a hidden decisive atom. |
| [Spärck Jones, A statistical interpretation of term specificity and its application in retrieval](https://www.staff.city.ac.uk/~sbrp622/idfpapers/ksj_orig.pdf) | Weights term matches by collection occurrence; the original study also reports that deleting frequent terms damages recall. | Statistical specificity differs from decisiveness. This supports retaining uncertainty about omitted atoms, not a universal claim that rare terms must be decisive. |
| [Itti and Baldi, Bayesian Surprise Attracts Human Attention, equation (2)](https://proceedings.neurips.cc/paper_files/paper/2822-bayesian-surprise-attracts-human-attention.pdf) | Surprise is `KL(posterior || prior)` over a declared observer's model class. | Its observable includes prior, likelihood, data and posterior. The indistinguishability argument applies when these remain equal across tasks; a more discriminating model is additional information that must be declared. |
| Graph salience/centrality | Any deterministic graph/feature score is already a function of `z`; random scores fit F1.2. | The theorem quantifies over all such extractors, so it needs no claim that one centrality is the empirically strongest. |

The third column is the present argument applied to those native objects.
These papers' experiments/algorithms were not rerun, and the table does not
claim an empirical ranking among propagated, per-source, fan-out or donor
scores. The finite generic checker is the shared counterexample route: every
capacity-limited output is covered, including outputs of these parents when
the declared information model has singleton symmetry.

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

## Integration and verification

The original three files were imported unchanged from PR #330 head
`7e41b2d631d75369df78cd54c6c5317491fc7937`, then hardened locally. The PR base
is `theory/meg-foundation-batch2`, so its open/merged status alone is not evidence
of arrival on `main`. New controls compare all 256 finite decisive-set families
over three atoms against all capacity-bounded selectors for capacities 0–3;
test family truncation, ineligible selections, malformed capacities, enumeration
exhaustion; and verify CLI 0/1/2 including refusing Python `-O`.

Run `python research/machine-epistemics-theory/meg_frontier_f1_extraction_exact.py`
and `python -m pytest -q tests/unit/test_meg_frontier_f1_extraction.py`.
Reference arithmetic/enumeration is local evidence; no protected empirical
score comparison, all-scale performance, OCM default switch, or novel theorem
follows. Reopen if the visible information model, task-family definition,
eligible universe, capacity, or certificate construction requirement changes.

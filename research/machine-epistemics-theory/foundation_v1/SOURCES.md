# Primary-source ledger and search boundary

Search date: 2026-09-04. Sources were retrieved through live web search/open, not inferred
from model memory. Inspection depth is explicit. The mathematical arguments in THEORY.md
are self-contained; no unread proof is imported as authority. No source-saturation or
priority claim is made. Abstract-only ownership is a provisional parent mapping.

| ID | Primary source | Inspected | Use and limitation |
|---|---|---|---|
| S1 | Angelopoulos & Bates, *A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification*, arXiv:2107.07511, version 6. https://arxiv.org/html/2107.07511v6 | HTML; section 3.1 marginal versus conditional coverage and equation (15). | F02's coverage distinction. Does not license conditional/anytime validity for an arbitrary selector. |
| S2 | Barber, Candes, Ramdas & Tibshirani, *Conformal Prediction Beyond Exchangeability*, arXiv:2202.13415v5; Annals of Statistics, 2023. https://arxiv.org/html/2202.13415v5 | HTML; theorem 2 and surrounding assumptions. | Configuration/data-law dependence matters. Its specialized weighted-conformal bound is NOT claimed for OCM. |
| S3 | Bates, Angelopoulos, Lei, Malik & Jordan, *Distribution-Free, Risk-Controlling Prediction Sets*, JACM 68(6), 2021; arXiv:2101.02703. https://arxiv.org/abs/2101.02703 | Primary abstract and Stanford author publication record; HTML full-text retrieval failed. | Parent for calibrated expected-loss control. Full algorithm/proof not reconstructed; no implementation claimed. |
| S4 | de Kleer, *An assumption-based TMS*, Artificial Intelligence 28(2), 127-162, 1986. https://doi.org/10.1016/0004-3702(86)90080-9 | Publisher metadata and abstract only. | ATMS parent mapping inherited from #310; our finite algebra is independently derived, not a claimed full-paper reproduction. |
| S5 | Gradel & Tannen, *Provenance Analysis and Semiring Semantics for First-Order Logic*, arXiv:2412.07986. https://arxiv.org/abs/2412.07986 | Primary abstract; HTML full-text retrieval failed. | Direct nearby parent for provenance with negation and quotient semirings. Historical Green-Karvounarakis-Tannen 2007 ownership is retained; neither is claimed fully reconstructed here. |
| S6 | Kozen, *Kleene algebra with tests*, TOPLAS 19(3), 427-443, 1997, DOI 10.1145/256167.256195. https://www.cs.cornell.edu/~kozen/Papers/papers_by_year.htm | Author bibliography/abstract and official KAT project description. | Parent program algebra. The trace/static/zero-iteration distinctions in F06 are explicitly derived; no KAT completeness proof is imported. |
| S7 | Angluin, *Queries and Concept Learning*, Machine Learning 2, 319-342, 1988. https://doi.org/10.1023/A:1022821128753 | Publisher abstract, query types and references. | Parent query-learning boundary. We prove only finite realizable agreement/support facts, not a new grammar sample-complexity result. |
| S8 | Acar, Blume & Donham, *A Consistent Semantics of Self-Adjusting Computation*, arXiv:1106.0478. https://arxiv.org/abs/1106.0478 | Primary abstract; HTML full text unavailable. Also CMU's Acar dissertation abstract. | Parent for change propagation/from-scratch consistency. Our F07 is a simpler pure-DAG induction with explicit cost assumptions. |
| S9 | Pearl, *Causal inference in statistics: An overview*, 2009. https://escholarship.org/uc/item/36w8n7pg | Author institutional-deposit abstract/metadata. | SCM/intervention parent. F17 is a two-bit self-contained countermodel, not reproduction of causal-identification algorithms. |
| S10 | Tibshirani, Barber & Ramdas, *Conformal Prediction Through the Lens of Hypothesis Testing: Universality, Impossibility, and Optimality*, arXiv:2608.27310, submitted 2026-08-27. https://arxiv.org/abs/2608.27310 | Primary abstract only. | Recent nearest-neighbor flag. Its universality/optimality results are not imported; a future novelty audit must inspect the full paper. |

No quoted text is needed for the arguments. Proof-by-citation, historical name changes,
and a broad claim that the literature is complete are deliberately excluded.

## Repository sources

- ORION-V2 main baseline: `24566f00a9dc4425a438fcfac05d13c6b2d903db` (#310).
- `research/machine-epistemics-theory/ME_THEORY_GAP_ATLAS_V1.md`, blob
  `9bb8943f88f1096265c7156be520300d340f0a71`.
- #310's three-valued interval note and exact finite checker are inherited, not rebranded.
- #304 governs V2 science versus OCM runtime ownership; #197 governs scientific claim scope.
- The previously audited OCM operator registry at `fc5841a7f87d7be9faee62bf7f557ca611b02b64`
  motivates full identity/risk binding. This package does not claim that active branch
  still has the same implementation, nor that OCM parity has been executed.

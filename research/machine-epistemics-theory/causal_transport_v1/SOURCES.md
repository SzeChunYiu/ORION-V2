# Source and strongest-parent record

Search boundary: 2026-09-05; repository baseline and task naming retain the 2026-09-04 identity. This is a targeted primary-source search, not saturation or a priority claim. A source's metadata, inspected passages, formal ownership and unverified remainder are separate. No uploaded PDF or font is redistributed.

## P1 — Structural causal semantics

Judea Pearl, *Causal inference in statistics: An overview*, Statistics Surveys 3 (2009), 96–146, DOI 10.1214/09-SS057. Author-hosted full text: https://ftp.cs.ucla.edu/pub/stat_ser/r350.pdf

Inspected: section 3.2.1, surgical intervention semantics (printed page 107; PDF page 11 visually checked), and the article's distinction among association, interventions and counterfactuals. Ownership: the model/query vocabulary, not a new ORION mechanism. We use a finite tabular specialization and supply its proof rather than claim a new causal theory. Not claimed: reconstruction of every identification or mediation theorem in the article.

## P2 — Response functions and counterfactual partial identification

Alexander Balke and Judea Pearl, *Counterfactual Probabilities: Computational Methods, Bounds and Applications*, UAI 1994, pp. 46–54. Repository upload is 2013, **not** original publication date. Metadata: https://arxiv.org/abs/1302.6784v1 ; full text: https://arxiv.org/pdf/1302.6784

Inspected: sections 3.1–3.3, response-function variables, shared exogenous variables across factual/counterfactual worlds, and optimization over compatible functional models. PDF page 2 visually checked. Ownership: counterfactual evaluation/bounding via compatible response functions. CT-05 is the elementary unrestricted binary-coupling calculation, not a new general bound algorithm. Native limit retained: population distributions in identification calculations are not finite-sample estimates; the paper makes this distinction explicitly in its application discussion. No numerical results from that application are reused.

## P3 — Identifiability and transportability

Elias Bareinboim and Judea Pearl, *Meta-Transportability of Causal Effects: A Formal Approach*, AISTATS 2013, PMLR 31:135–143. Publisher: https://proceedings.mlr.press/v31/bareinboim13a.html ; text: https://proceedings.mlr.press/v31/bareinboim13a.pdf

Inspected: definitions 1–2 (PDF page 2) of identifiability and selection diagrams, especially separately represented mechanism/population differences. PDF text was available; screenshot attempts failed, so no uninspected graphical example is presented as reconstructed. Ownership: causal identification and multi-domain transportability. The paper's complete graphical algorithm is stronger than our finite-model evaluator in its native setting; this package does not implement or outperform it. CT-07 is a perturbation envelope under explicit kernel/population bounds, not a competing complete transport calculus.

## P4 — Coupling, total variation and the global compatibility obstacle

Omer Angel and Yinon Spinka, *Pairwise optimal coupling of multiple random variables*, arXiv:1903.00632, inspected v2 (7 May 2021). Full text: https://arxiv.org/pdf/1903.00632 ; metadata: https://arxiv.org/abs/1903.00632

Inspected: theorem 1 (classical maximal coupling) and the three-variable counterexample immediately following it, on PDF page 0. Ownership: the foundational coupling result is explicitly classical in this paper; CT-07 and CT-10 are finite conditional-coupling consequences, and CT-13 reproduces the stated parent counterexample with full attribution. We do not claim the paper's new simultaneous-coupling theorem or extremal-combinatorics results as ORION contributions. CT-08's finite conditional-TV argument is supplied directly; its priority is not asserted.

## P5 — Strong contemporary interactive lower-bound parent

Fan Chen, Dylan J. Foster, Yanjun Han, Jian Qian, Alexander Rakhlin and Yunbei Xu, *Assouad, Fano, and Le Cam with Interaction: A Unifying Lower Bound Framework and Characterization for Bandit Learnability*, NeurIPS 2024. Publisher: https://proceedings.neurips.cc/paper_files/paper/2024/hash/8a23a95e26d016711c0d70f79ade3c95-Abstract-Conference.html ; full text: https://arxiv.org/pdf/2410.05117

The publisher abstract and PDF availability were verified. Full theorem reconstruction is **not complete**. Used only as a mandatory nearest-parent direction for future interactive frontier work, not as authority for an imported inequality. CT-10's elementary two-point/abstention argument is proved in this package. Do not claim a new characterization of bandit learnability or a bound stronger than this parent.

## P6 — Current counterfactual-bound neighbor (metadata/abstract only)

Naoya Hashimoto, Yuta Kawakami and Jin Tian, *Bounds and Identification of Joint Probabilities of Potential Outcomes and Observed Variables under Monotonicity Assumptions*, arXiv:2602.18762v1 (21 February 2026): https://arxiv.org/abs/2602.18762v1

Verified title, authors, version date and abstract. A final metadata refresh also verified publication in AISTATS 2026, PMLR 300:2827–2835: https://proceedings.mlr.press/v300/hashimoto26a.html . It studies joint potential outcomes and observed variables with monotonicity assumptions. Formal reconstruction remains OPEN; none of its theorem statements is imported. This is a current adjacent-work flag that prevents misnaming our elementary unrestricted binary result as a frontier novelty. Any successor on monotonicity must reconstruct this source first.

## Local lineage and collision record

Base: ORION-V2 `24566f00a9dc4425a438fcfac05d13c6b2d903db`, merging #310. Read at that ref: AGENTS.md; `research/orion-machine/README.md`; `research/machine-epistemics-theory/ME_THEORY_GAP_ATLAS_V1.md`. Read live: #304 work division; #312/#313 foundation claims; #314 read-only decision frontier. #315 claims this separate directory. The latest gap atlas means the earlier report that MEG names lacked a V2 research object is no longer current.

Scientific lineage stays visible: SCM, response functions, partial identification, maximal coupling, two-point testing and finite marginal feasibility own the mathematical ingredients. Added value offered here is precise machine-facing type separation, lifecycle contracts, sharp finite witnesses and executable calibration. There is no demonstrated theoretical residual over the strongest compatible parent product.

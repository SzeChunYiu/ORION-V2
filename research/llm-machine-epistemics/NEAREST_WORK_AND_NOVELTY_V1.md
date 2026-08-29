# Nearest Work and Novelty Subtraction V1

**Issue:** #51  
**Purpose:** prevent the LLM Machine Epistemics paper from relabelling classical sufficiency, predictive-state, rate-distortion, representation-identifiability, uncertainty or belief-probe results as ORION novelty.

This file is a **claim-boundary map**, not a complete bibliography. A reproducible bibliographic sweep remains a mechanical handoff before submission.

## 1. Novelty rule

A contribution counts only if the theorem-level residual survives the **strongest parent composition**. The correct comparison is not against a plain LLM or weak prompt baseline; it is against the combination of:

1. statistical sufficiency / Blackwell / Le Cam decision comparison;
2. causal-state / predictive-state minimality;
3. task- or reward-predictive state representations;
4. information bottleneck / conditional rate-distortion;
5. generic representation non-identifiability;
6. empirical LLM belief/truth/uncertainty representation work;
7. standards requiring internal representations to be usable rather than merely decodable.

If that product already proves the full theorem stack in `THEORY_V1.md`, the valid terminal is `CLASSICAL_PARENT_SUFFICIENT__MERGE_OR_DROP`.

---

# 2. Parent map

| Parent area | What it already owns | What #51 must not claim | Candidate residual after subtraction |
|---|---|---|---|
| Statistical sufficiency | sufficient statistics; factorization; target-relative preservation | novelty for `Q ⟂ H | Z` or fibre constancy | explicit separation between **linguistic entire-future sufficiency** and a declared **epistemic responsibility family**, plus LLM interpretation |
| Blackwell comparison / Le Cam deficiency | experiment informativeness and decision-risk comparison | novelty for “more information supports more decisions” or generic deficiency | responsibility-indexed internal-state requirements and predictive-compression interaction |
| Computational mechanics / causal states | histories grouped by identical future law; minimal predictive state | novelty for `h~h' iff future laws agree` or minimal predictive state | what additional state is needed beyond that minimal linguistic state for epistemic responsibilities |
| Predictive State Representations | predictive state from observable history | novelty for maintaining prediction-sufficient observable state | explicit responsibility refinement beyond the linguistic prediction target |
| Reward-predictive / task-predictive states | observation prediction can be insufficient for reward/control-relevant state | broad novelty for “prediction target may omit another task variable” | LLM-specific entire-future linguistic state + epistemic responsibility family + exact entropy-overhead/refinement theory |
| Information Bottleneck / rate distortion | compression under task/relevance constraints | novelty for generic `I(H;Z)` tradeoffs or conditional RD | responsibility-constrained predictive–epistemic rate region, only if nontrivial consequences/closed forms survive |
| Data processing | downstream processing cannot increase mutual information | novelty for T5 or T6 identities themselves | interpretation as boundary between evidence-free epistemic computation and information acquisition inside LLM state theory |
| Representation identifiability | predictor behavior does not determine arbitrary internal representation properties | novelty for “same output predictor, different hidden states” | maximal-predictive-compression theorem and responsibility-state overhead, if not already implied in one parent theorem |
| LLM hidden-state factuality/truth/uncertainty | empirical probes can recover factuality/uncertainty signals | novelty for hidden epistemic signals | formal conditions for when such internal information would be sufficient for a declared responsibility |
| LLM belief representation standards | criteria such as accuracy/coherence/uniformity/use | novelty for causal-use requirement alone | use these standards as empirical interpretation contract for a mathematically responsibility-sufficient state |
| Epistemic Neural Networks | “epistemic” uncertainty through joint predictive distributions | novelty for the word epistemic or uncertainty-aware neural predictions | distinguish uncertainty from warrant/dependence/scope/defeater responsibilities |

---

# 3. Load-bearing references already identified

## 3.1 Minimal prediction state / computational mechanics

**Shalizi, C. R. & Crutchfield, J. P.** — *Computational Mechanics: Pattern and Prediction, Structure and Simplicity* and related causal-state work.

Ownership relevant here:

- histories are equivalent when they induce the same conditional distribution over futures;
- causal states are sufficient statistics for prediction and have a minimality property under standard assumptions.

Consequence for #51:

`S_P` must be explicitly attributed to this family / classical sufficient-statistic theory. The paper cannot sell the predictive quotient as new.

## 3.2 Predictive State Representations and task/reward-predictive variants

Predictive-state research represents dynamical state through predictions of observable future events. Reward-predictive/state-abstraction work establishes an important precedent: a representation sufficient for observation prediction need not be sufficient for reward/control.

Consequence for #51:

The weak statement “prediction can omit another task variable” is occupied. Our residual needs the **autoregressive linguistic-future specialization**, the explicit epistemic responsibility family, the minimal additional-state cost, and refinement/rate results.

## 3.3 Statistical sufficiency, Blackwell and Le Cam

Classical statistical decision theory owns the basic hierarchy of sufficient information, comparisons of experiments and risk consequences of information loss.

Consequence for #51:

Any theorem stated only as “a target can be recovered iff constant on fibres” is too weak. The ORION Wave audit already identified this risk in V1. The LLM paper must prove something about **minimal predictive compression + epistemic responsibilities**, not merely apply the factorization criterion to a new noun.

## 3.4 Information Bottleneck and rate distortion

The Information Bottleneck family studies compressed representations that preserve information relevant to a task variable; conditional and multi-task rate-distortion formulations are mature.

Consequence for #51:

The approximate `R_epi(epsilon)` object is not itself novelty. A paper-worthy residual requires at least one of:

- an LLM/predictive-state endpoint theorem not immediate from generic RD;
- a closed-form nontrivial family revealing a sharp epistemic cost invisible to prediction-only rate;
- a responsibility-refinement consequence with no equivalent statement in the nearest parent;
- a strict separation law tied to minimal linguistic predictive state.

## 3.5 Direct 2026 representation-identifiability collision

**Sevetlidis, V. (2026). _A Fiber Criterion for Representation Identifiability in Supervised Learning._ arXiv:2606.01092.**  
https://arxiv.org/abs/2606.01092

The paper establishes a general criterion for which internal representation properties are identifiable from predictor behavior: only properties constant on fibres of the representation/head-to-predictor map are behaviorally identifiable.

Consequence for #51:

`Z_1=S_P` versus `Z_2=(S_P,Q)` implementing the same linguistic predictor is **illustration only**, not a headline theorem. The paper must explicitly cite this work in the introduction/related theory and explain why T2/T3 ask a different question: not behavioral identifiability, but the **minimal state complexity required when predictive sufficiency and epistemic responsibility sufficiency are jointly imposed**.

## 3.6 Standards for internal belief representations

**Herrmann, D. & Levinstein, B. A. (2025). _Standards for Belief Representations in LLMs._ Minds and Machines.**  
DOI: https://doi.org/10.1007/s11023-024-09709-6

Relevant standards include accuracy, coherence, uniformity and use. The “use” requirement is particularly important: an internal signal should matter to the model's behavior rather than merely be linearly decodable by an external analyst.

Consequence for #51:

T9 should adopt/compare with these standards. “Causal use matters” is not ours to claim as a novel philosophical insight.

## 3.7 Evidence for causally usable belief-like LLM representations

**Corona Mendozza, J. & Søgaard, A. (2026). _LLM Beliefs Are in Their Heads._ ACL 2026.**  
https://aclanthology.org/2026.acl-long.1905/

This work reports internal belief-like representations and intervention/steering evidence relevant to causal use.

Consequence for #51:

We must not claim present LLMs are epistemically empty. Instead, the paper supplies a mathematical test of what additional sufficiency properties such representations would need to satisfy for a declared responsibility family.

## 3.8 Hidden-state uncertainty may not equal truthfulness

**Cheang et al. (2026). _Do LLMs Really Know What They Don't Know? Internal States Mainly Reflect Knowledge Recall Rather Than Truthfulness._ Findings of ACL 2026.**  
https://aclanthology.org/2026.findings-acl.34/

The paper provides a useful warning: a hidden-state signal associated with confidence/knowledge recall can be mistaken for a truthfulness representation.

Consequence for #51:

This supports keeping responsibilities typed. A `knowledge-recall` coordinate, `truth/warrant` target, source-dependence target and unresolved/identifiability target must not be silently conflated.

## 3.9 Other hidden-state factuality / trajectory work

Recent ACL/EMNLP work studies factuality, truth trajectories, uncertainty representations and internal confidence signals across layers. These results occupy empirical signal extraction and motivate future tests, but do not by themselves establish the responsibility-sufficiency theory.

Required final bibliography sweep should include at minimum:

- factuality detection from hidden states;
- truth/validity trajectory geometry;
- representation engineering / activation steering;
- hidden-state uncertainty and self-knowledge;
- mechanistic work on world-state / belief-state representations.

## 3.10 Epistemic Neural Networks

**Osband et al.** — Epistemic Neural Networks and follow-on work.

Ownership relevant here: “epistemic” has an established ML use tied to uncertainty and joint predictions.

Consequence for #51:

The paper must define **epistemic responsibility** explicitly and early. It must not imply that ORION owns or replaces epistemic-uncertainty modelling.

---

# 4. Claim-by-claim novelty classification

| Proposed #51 result | Current classification | Reason |
|---|---|---|
| `S_P` minimal predictive state | `PARENT_OWNED` | causal-state / sufficient-statistic theory |
| T1 predictive vs epistemic separation | `FOUNDATIONAL_SYNTHESIS` | form is close to task-sufficiency separation; not enough alone |
| T2 entropy-minimal predictive compression forces epistemic loss | `CANDIDATE_RESIDUAL` | strengthens the story by tying insufficiency to minimal predictive-state entropy; must search nearest theorem |
| T3 exact deterministic overhead `H(Q|S_P)` | `CANDIDATE_RESIDUAL_OR_COROLLARY` | clean exact consequence, but likely derivable from classical source coding/sufficiency; novelty depends on theorem package rather than identity alone |
| T4 log-loss deficiency `I(Q;H|Z)` | `PARENT_OWNED_IDENTITY` | conditional mutual information / Bayes log loss |
| T5 post-processing monotonicity | `PARENT_OWNED_IDENTITY` | data processing |
| T6 external observation value | `PARENT_OWNED_IDENTITY` | conditional mutual information |
| T7 responsibility refinement order | `CANDIDATE_STRUCTURAL_RESIDUAL` | likely elementary in finite case; significance depends on family/join theory and approximate extension |
| T8 predictive–epistemic rate region | `OPEN_RESIDUAL` | conditional RD is parent-owned; needs closed-form/strict new consequence |
| T9 causal-use internality contract | `PARENT_ASSIMILATION` | belief-representation standards / causal probing |
| Combined theorem architecture | `PRIMARY_CANDIDATE` | may be publishable if the whole object is not already owned by one parent synthesis |

---

# 5. Strongest-parent reconstruction to attempt before novelty promotion

The hostile reviewer should attempt to derive the entire #51 programme from the following product:

\[
\text{CausalStates}
\times
\text{Blackwell/Sufficiency}
\times
\text{ConditionalRateDistortion}
\times
\text{RepresentationIdentifiability}
\times
\text{BeliefUseCriteria}.
\]

The review question is not whether each ORION equation can be found verbatim. It is whether a competent theorist using these parents would regard the headline as an immediate corollary with only terminology changed.

### If yes

Terminal:

`CLASSICAL_PARENT_SUFFICIENT__MERGE_OR_DROP`.

### If no

The residual must be stated as an exact theorem delta, for example:

> Among entropy-minimal deterministic representations sufficient for the **entire autoregressive linguistic future**, epistemic responsibility information that varies within predictive causal-state fibres is necessarily absent; exact deterministic responsibility recovery requires an additional `H(Q|S_P)` bits on average, with larger responsibility families forming a strict refinement hierarchy and an approximate responsibility-constrained predictive rate region.

Even this wording remains provisional until the bibliographic theorem audit closes.

---

# 6. Journal significance test

For JMLR, mathematical correctness is not enough. The paper needs to explain why the theorem changes how researchers think about language-model objectives or representations.

A credible practical implication would be:

> Evaluating or optimizing only linguistic predictive sufficiency cannot determine whether a compressed internal representation retains the information required for a separate epistemic responsibility. If a system is intended to support such responsibilities, they must either be included in the representation objective/constraint, preserved by excess state, or supplied through external information acquisition.

This is an implication of the theorem stack, not a claim that a specific proposed training algorithm already improves LLMs.

JMLR author information / scope: https://jmlr.org/author-info.html

---

# 7. Remaining bibliographic handoff

Before any manuscript calls the residual novel, an AI/research agent must produce a reproducible claim matrix with:

- exact title/authors/year/venue/DOI or stable URL;
- theorem or proposition identifiers where available;
- quoted/paraphrased nearest result kept within copyright limits;
- whether it contains prediction-state minimality;
- secondary task/responsibility sufficiency;
- exact state-overhead lower bound;
- multi-responsibility refinement;
- approximate rate frontier;
- LLM/autoregressive specialization;
- internal causal-use criterion;
- overlap verdict with T1–T9.

Search at minimum Semantic Scholar, OpenAlex/Crossref, arXiv and ACL Anthology, with duplicate merging by DOI/arXiv identifier/title. Search terms must include combinations of:

`predictive sufficient state`, `causal states additional task information`, `reward predictive representation`, `minimal sufficient representation multiple tasks`, `conditional sufficient statistic`, `multi-task information bottleneck`, `side information rate distortion sufficient statistic`, `language model sufficient representation`, `belief representation language model`, `representation identifiability predictor`, `epistemic representation LLM`, `task-relevant representation conditional mutual information`.

No novelty statement becomes final until this matrix is attached to the issue/branch and hostile-reviewed.

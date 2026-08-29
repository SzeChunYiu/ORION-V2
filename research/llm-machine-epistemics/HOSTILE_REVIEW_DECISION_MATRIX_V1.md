# Hostile Review Decision Matrix V1

**Issue:** #51  
**Purpose:** perform the conceptual reviewer work before computation. The execution AI should later populate evidence/status cells; it should not invent defenses after seeing results.

## Review principle

A hostile objection is considered **answered** only if the paper either:

1. cites and grants the parent result, then states an exact residual theorem/consequence not owned by it; or
2. narrows/contracts the claim.

Rhetorical distinction, terminology changes and “ORION combines them” are not answers.

---

# R1 — “Reward-predictive state representations already prove your basic point.”

## Objection

Predictive State Representations reproduce observation sequence distributions yet may fail to represent rewards. Baisero & Amato's Reward-Predictive State Representations explicitly give conditions for reward accuracy and augment PSRs to represent both observations and rewards.

Primary anchor:

- Andrea Baisero & Christopher Amato, **Reconciling Rewards with Predictive State Representations**, IJCAI 2021, DOI `10.24963/ijcai.2021/299`.

## What this objection kills

It kills novelty for the broad sentence:

> A representation sufficient for one prediction target may be insufficient for another task-relevant target.

Therefore T1 **alone cannot be the headline contribution**.

## Registered response

The candidate residual must instead be all of:

1. entire-future autoregressive linguistic predictive state as the base representation;
2. a declared **family** of typed epistemic responsibilities rather than one reward scalar;
3. exact state-complexity overhead relative to the linguistic predictive quotient;
4. prospective/dynamic responsibility sufficiency: current joint sufficiency may still lose information needed for future revision;
5. explicit separation of acquisition, compression and future-option deficits.

## Fatality rule

If the strongest R-PSR/task-predictive-state literature already contains items 2–5 in equivalent form, close `CLASSICAL_PARENT_SUFFICIENT__MERGE_OR_DROP`.

---

# R2 — “Causal states already give the unique minimal state for the full future.”

## Objection

Computational mechanics groups histories with identical conditional future laws and proves causal states are minimal sufficient statistics for prediction, unique up to isomorphism under the usual assumptions. Recursive calculability is also established.

## What this objection kills

- novelty for `S_P`;
- novelty for Lemma 1;
- likely independent novelty for the entropy-minimal/isomorphism part of T2.

## Registered response

Grant all causal-state ownership. T2 is useful only as a bridge theorem showing what an **epistemic secondary responsibility** must pay beyond the predictive quotient.

The stronger candidate residual moves to:

- `H(Q|S_P)` as the exact deterministic extra-state requirement;
- responsibility-family state sharing/refinement;
- static-versus-prospective responsibility gap;
- dynamic optionality cost beyond current predictive+responsibility state.

## Fatality rule

If causal-state theory plus a standard “augment target to `(Y,Q)`” construction immediately yields the full static and dynamic paper with no additional theorem consequence, JMLR significance fails even if the mathematics is correct.

---

# R3 — “Your maximal-compression theorem is just deterministic information bottleneck / minimal sufficiency.”

## Objection

The Deterministic Information Bottleneck and standard minimal-sufficient-statistic theory already study deterministic compressed representations and task sufficiency.

Primary anchor:

- Strouse & Schwab, **The Deterministic Information Bottleneck**, Neural Computation 29(6), 2017, DOI `10.1162/NECO_a_00961`.

## What this objection kills

Any claim that minimizing representation entropy subject to predictive sufficiency is itself novel.

## Registered response

T2 should be presented as a **derived bridge / design corollary**, not proprietary mathematics:

> compression toward a minimal linguistic predictor is safe for an epistemic responsibility iff that responsibility is already measurable from the predictive state.

The scientific burden shifts to the responsibility-state consequences and dynamic optionality.

## Fatality rule

If the paper still relies on T2 as its only nontrivial theorem after parent subtraction, downgrade to field-theory/conceptual scope.

---

# R4 — “Multi-task representation learning already says a shared representation must preserve all tasks.”

## Objection

Information-theoretic multi-task representation learning explicitly studies sufficient representations for several tasks and warns that compression can discard information required by other tasks.

Current direct example:

- Hu, Wei, Zhou & Hu, **An Information-theoretic Multi-task Representation Learning Framework for Natural Language Understanding**, AAAI 2025.

## What this objection kills

Novelty for saying:

> add more target variables/auxiliary objectives if you want a representation sufficient for multiple responsibilities.

## Registered response

The paper must not reduce “epistemic responsibility” to ordinary multi-task labels. Its stronger object is:

- responsibilities can be activated/revised over time;
- provenance/defeater variables can have zero current task value but positive future revision value;
- the minimal recursively updateable state can strictly refine the static joint-task sufficient state.

This is why T10–T13 are now load-bearing.

---

# R5 — “T8 is textbook log-loss rate distortion.”

## Objection

Under logarithmic loss, rate-distortion functions have the linear entropy-minus-distortion form in classical settings; multiterminal log-loss source coding is mature.

Primary anchor:

- Courtade & Weissman, **Multiterminal Source Coding Under Logarithmic Loss**, IEEE Transactions on Information Theory 60(1), 2014, DOI `10.1109/TIT.2013.2288257`.

## Registered response

Accept the objection completely.

- T8A is background / exact benchmark.
- T8B is a product-source typed-responsibility benchmark.
- neither is claimed as a new information-theoretic law.

Their purpose is to make the paper's approximation story quantitative and to provide a checker target.

## Fatality rule

No T8 result based only on substituting ORION variables into a named log-loss theorem may be listed in the abstract as independent novelty.

---

# R6 — “Your dynamic theorem is Myhill–Nerode / DFA minimization.”

## Objection

The coarsest right congruence refining an output/acceptance partition and deterministic recursive state minimization are classical automata/partition-refinement ideas. Bisimulation and computational mechanics provide related state-refinement machinery.

## What this objection kills

Novelty for:

- right congruence itself;
- partition-refinement algorithm;
- generic minimal deterministic recurrent state theorem.

## Registered response

The candidate paper residual is **not** “we invented right congruence.” It is the specific epistemic-state result:

> A state can be sufficient for the complete linguistic future **and** all current epistemic responsibilities yet still be insufficient for future epistemic revision. The additional state is the coarsest right-congruent refinement required by the future responsibility process; its entropy relative to the current joint state is an epistemic optionality cost.

The paper must connect the automata theorem to the information-theoretic prospective deficiency

`I(Q_future; H_now | Z_now, X_future)`

and show why static LLM hidden-state probes cannot detect this failure mode.

## Fatality rule

If a nearest parent already defines exactly this future-task/right-congruence overhead and consequence for learned/predictive representations, dynamic novelty disappears. Do not defend it by renaming “task” as “epistemic responsibility.”

---

# R7 — “A belief state in a POMDP is already a sufficient recursive state for all future decisions.”

## Objection

Control theory/POMDP theory uses belief states or information states as sufficient recursively updated summaries for future control.

## Registered response

This is a major parent, not an analogy to ignore.

The #51 theorem differs only if it can show a useful representation result when:

- the base state is defined by linguistic predictive sufficiency rather than a known latent generative model;
- responsibilities are typed and may involve evidence/dependence/revision constructs not present in the linguistic prediction target;
- the paper quantifies the incremental state needed beyond the predictive quotient;
- prospective epistemic deficiency identifies information discarded by current compression that future observations cannot reconstruct.

## Fatality rule

If “belief state over an augmented latent variable containing all responsibilities” fully resolves the theorem with no LLM-specific residual, the paper is a synthesis/application rather than new theory.

---

# R8 — “Real transformers are not minimal causal states, so your theorem says little about LLMs.”

## Objection

Actual transformer residual streams are huge, redundant and not entropy-minimal statistics. T2 cannot diagnose a normal LLM merely because it minimizes cross-entropy training loss.

## Registered response

Agree. The paper must say:

- predictive **optimality** does not force minimal internal state;
- ordinary LLMs may retain epistemic information incidentally;
- T2 is a compression/distillation/design-limit result, not an empirical claim that current LLMs have compressed to `S_P`;
- T1 plus non-identifiability means predictive behavior alone does not certify epistemic sufficiency;
- the theory provides audit quantities and future empirical tests, not a diagnosis of every transformer.

## Manuscript consequence

Use phrases like “prediction-only objectives do not guarantee” rather than “next-token training erases”.

## Fatality rule

Any abstract sentence implying actual LLMs necessarily lose `Q` under ordinary pretraining is prohibited unless separately proven empirically/theoretically under realistic optimization assumptions.

---

# R9 — “Your Q variables are hand-authored benchmark labels, not epistemology.”

## Objection

Calling an arbitrary auxiliary target “epistemic” does not make a new science.

## Registered response

The paper must define a responsibility admissibility rule. A `Q_i` counts as an epistemic responsibility only when it is tied to a declared decision about the epistemic status or management of a claim/model/inference, with mechanically or externally specified semantics.

Admissible examples:

- source/dependence class relevant to corroboration;
- identifiable/non-identifiable status under a declared observation model;
- scope/validity condition;
- defeater/reopen state;
- observation versus inference provenance;
- calibrated abstention terminal under a fixed decision rule.

Not sufficient by itself:

- arbitrary sentiment label;
- unrelated downstream classification task;
- “confidence” with no declared decision semantics;
- institutional legitimacy generated by the model.

## Fatality rule

If the mathematics only works by treating `Q` as an arbitrary task label and no epistemic-specific consequence survives, the paper should be presented as general multi-responsibility representation theory, not Machine Epistemics.

---

# R10 — “Truth/confidence/belief signals are already found in LLM hidden states.”

## Objection

Recent work reports decodable and sometimes causally usable belief/truth/factuality/uncertainty-related structure in LLM activations.

## Registered response

The paper explicitly does **not** claim epistemic emptiness.

Its question is:

> Given a declared responsibility, what sufficiency properties must an internal state satisfy, what deficit remains if it does not, and can it update correctly under future evidence?

A high-performing probe is evidence about decodability, not automatically about:

- exact responsibility sufficiency;
- causal use;
- source/dependence state;
- future revision optionality.

The future empirical programme should treat real hidden-state results as candidates to audit against these stronger properties.

---

# R11 — “The three-deficit decomposition is just chain rule plus a new name.”

## Objection

`H(Q|Z)=H(Q|H)+I(Q;H|Z)` is textbook conditional mutual information.

## Registered response

Correct. The identity itself is not novel.

The value of the decomposition is **diagnostic architecture**:

- acquisition deficit has an information-source intervention;
- compression deficit has a representation intervention;
- prospective deficit has a memory/optionality intervention.

For a top theory venue, this taxonomy is supporting structure only. The paper still needs a theorem residual beyond the chain rule.

---

# R12 — “Why should a top ML journal care?”

## Objection

Even if correct, the results may be elementary consequences of classical information and automata theory.

## Registered response

The JMLR case succeeds only if the final paper changes a meaningful representation-learning question. Candidate consequence:

> **Static task sufficiency is not a sufficient design criterion for continually used language-model state.** Compression/distillation that preserves linguistic prediction and even today's epistemic probes can destroy the ability to revise correctly under future evidence. The required additional state can be characterized by prospective responsibility equivalence/right-congruent refinement, with current and future deficits separated information-theoretically.

This should lead to a concrete evaluation prescription for compressed/distilled/continual model representations:

1. current linguistic loss;
2. current responsibility sufficiency;
3. prospective responsibility sufficiency after controlled future evidence;
4. state/rate cost.

## Fatality rule

If hostile review concludes this is obvious to specialists and the theorem matrix confirms every component is an immediate parent corollary, do not force JMLR. Use the strongest honest field venue or merge into the flagship theory discussion.

---

# Pre-registered review outcomes

| Reviewer objection | Expected current status before mechanical audit |
|---|---|
| R1 R-PSR owns basic separation | **CONCEDE; T1 not standalone novelty** |
| R2 causal states own `S_P` minimality | **CONCEDE** |
| R3 DIB/minimal sufficiency owns compression core | **CONCEDE major portion** |
| R4 multi-task sufficiency overlap | **CONCEDE static multi-target portion** |
| R5 log-loss RD owns T8A/B math | **CONCEDE** |
| R6 automata/right congruence owns generic dynamic minimization | **CONCEDE mathematical substrate; test residual interpretation** |
| R7 POMDP information state overlap | **OPEN, high threat** |
| R8 real LLM non-minimality | **VALID LIMITATION, not fatal if wording correct** |
| R9 arbitrary-Q criticism | **ANSWER only via responsibility admissibility rule** |
| R10 hidden belief signals exist | **CONSISTENT with paper; no absence claim** |
| R11 decomposition is chain rule | **CONCEDE identity, retain diagnostic role only** |
| R12 top-tier significance | **OPEN; depends on dynamic residual + theorem matrix** |

This table intentionally starts pessimistic. A later execution result may contract the paper; it may not upgrade a conceded classical result into novelty.

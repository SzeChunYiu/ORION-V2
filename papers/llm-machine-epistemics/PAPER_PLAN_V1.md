# Paper Plan V1 — Predictive Is Not Epistemic

**Issue:** #51  
**Working paper identity:** `ORION-V2.LLM-MACHINE-EPISTEMICS.THEORY.V1`  
**Primary target:** Journal of Machine Learning Research (JMLR), conditional on a nontrivial theorem residual surviving nearest-parent subtraction.  
**Empirical LLM training required:** no.

## Working title

> **Predictive Is Not Epistemic: Responsibility-Sufficient Internal States for Autoregressive Models**

Alternative if reviewer feedback prefers a less adversarial title:

> **Epistemic Sufficiency Beyond Language Prediction**

## One-sentence paper question

What additional internal state, if any, is information-theoretically required when an autoregressive model must remain sufficient not only for the entire linguistic future but also for explicitly declared epistemic responsibilities?

## Candidate contribution statement

The paper should claim only what survives formal and novelty audit. The current candidate package is:

1. define an autoregressive **minimal entire-future predictive state** `S_P` using donor-owned causal/sufficient-state theory;
2. define a separate family of operational epistemic responsibilities `Q`;
3. prove that predictive equivalence need not imply responsibility equivalence;
4. prove that every entropy-minimal deterministic predictive-sufficient representation is isomorphic to `S_P`, so responsibility information absent from `S_P` cannot survive **maximal predictive compression**;
5. for deterministic responsibilities, prove the exact additional internal-state entropy required for zero-error recovery is

   \[
   H(Q\mid S_P);
   \]

6. express log-loss epistemic deficiency as

   \[
   I(Q;H\mid Z);
   \]

   while attributing the identity to standard information theory;
7. show responsibility families induce a refinement hierarchy with state complexity increasing exactly when added responsibilities contain new conditional information;
8. define and, if possible, solve a nontrivial approximate predictive–epistemic rate frontier.

The paper must not treat the donor-owned identities in items 1 and 6 as independent novelty.

---

# Why this can matter without training a new model

The paper's advantage is an **architecture-independent impossibility / state-complexity result**.

It does not need to show that a specific training recipe improves an LLM. Instead it can show:

> A language representation optimized only to be a maximally compressed sufficient state for the linguistic future can be provably unable to support another declared responsibility, and the missing state requirement can be quantified exactly in the deterministic case.

That result has implications for:

- representation compression/distillation;
- auxiliary objectives;
- model-state design;
- confidence/warrant/provenance probes;
- agent self-correction;
- retrieval/tool acquisition decisions;
- evaluation of whether internal belief-like signals are actually adequate for a task.

The implication should be phrased as a design constraint, not as proof that one new architecture is superior.

---

# Journal positioning

## Primary target — JMLR

JMLR is the preferred target if the theorem package becomes a real analytical framework with consequences for learning-system design. Its scope includes theoretical studies yielding new insight into learning-system behavior and new analytical frameworks.

Official author/scope information: https://jmlr.org/author-info.html

### JMLR gate

The paper should not be submitted to JMLR merely because it is mathematically correct. Before a JMLR attempt, require:

- theorem novelty beyond a straightforward composition of causal states + statistical sufficiency + conditional rate distortion;
- assumption-complete independent proof checking;
- one solved nontrivial approximate frontier or an equally strong theorem strengthening;
- a clear ML consequence for representation objectives/compression;
- current nearest-work saturation;
- concise exposition that does not require readers to learn ORION programme vocabulary.

## Fallbacks

- **Information and Inference** if the result becomes primarily information-theoretic.
- **TMLR** if the final object is best read as a rigorous ML theory/framework paper whose significance is narrower than JMLR.

Venue selection must follow the theorem that survives, not the desired prestige label.

---

# Manuscript structure

## 1. Introduction — linguistic prediction is one responsibility

Open with a minimal example rather than ORION terminology.

Two histories can have the same distribution over every future language continuation relevant to the modelling process yet differ in some other property required by a downstream responsibility. A minimally compressed predictor has no linguistic reason to retain that distinction.

State immediately what is **not** being claimed:

- current LLMs may preserve large amounts of extra state;
- existing LLMs empirically contain belief/truth/uncertainty-related signals;
- language-model training is not proven to erase epistemic information;
- the theorem concerns information requirements, not consciousness or philosophical understanding.

End the introduction with the exact theorem ladder.

## 2. Foundations and nearest parents

Organize by theorem ownership, not a chronological literature dump:

- sufficient statistics / Blackwell / Le Cam;
- computational mechanics / causal states;
- Predictive State Representations and reward/task-predictive variants;
- information bottleneck / rate distortion;
- representation identifiability;
- belief representation / hidden-state truth and uncertainty in LLMs.

The section must state explicitly that the minimal predictive quotient and generic information identities are parent-owned.

## 3. Autoregressive predictive state

Define:

- history `H`;
- full linguistic future `Y`;
- internal state `Z=f(H)`;
- linguistic predictive sufficiency;
- predictive equivalence and `S_P`.

Use the **full future** in the headline theory to avoid a next-token-only artefact.

## 4. Epistemic responsibility families

Define operational `Q_i` targets and explain why responsibilities remain typed.

Use examples only where their ground truth can be formalized mechanically:

- source/dependence class;
- identifiable/non-identifiable state;
- registered scope validity;
- defeater/reopen status;
- observation-versus-inference status;
- abstention requirement under a declared decision rule.

Keep human legitimacy / institutional authority outside model-generated state.

## 5. Minimal predictive state and separation

Present Lemma 1 and T1.

The section should make the distinction:

\[
\text{same linguistic future law}
\not\Rightarrow
\text{same epistemic responsibility law}.
\]

Use log-loss risk to avoid vague arguments about “understanding.”

## 6. Maximal predictive compression theorem

Present T2 as a central theorem:

- every deterministic predictive-sufficient state refines `S_P`;
- entropy is at least `H(S_P)`;
- equality implies mutual recoverability;
- therefore an entropy-minimal predictor cannot retain responsibility information absent from `S_P`.

This section is the main bridge from classical predictive states to a design consequence for compressed internal representations.

## 7. Exact responsibility-state overhead

Present T3:

\[
C_{\mathrm{epi}}^0(Q\mid S_P)=H(Q\mid S_P).
\]

Discuss:

- strict positive cost;
- zero-overhead cases;
- correlated responsibility vectors;
- why sum-of-coordinate costs is generally wrong.

Use CE1, CE4 and CE5.

## 8. Epistemic deficiency and information acquisition

Present T4–T6 as supporting calculus, with attribution to standard information theory.

The useful conceptual distinction is:

- internal computation may expose information already encoded;
- evidence-free post-processing cannot recreate information discarded by the representation;
- a new observation has value `I(Q;X|Z)` under Bayes log loss.

Avoid claiming a new data-processing theorem.

## 9. Responsibility refinement and approximate frontier

Present T7, then T8 if it survives computation.

A strong version should show one nontrivial solved family and illustrate how representation budget moves as responsibility requirements are tightened.

## 10. Relation to real LLM hidden states

Connect carefully to empirical work showing:

- belief-like internal representations;
- truth/factuality/uncertainty signals;
- cases where apparent self-knowledge reflects recall rather than truthfulness;
- the need for causal-use tests.

The theory asks a different question from probe accuracy:

> Is the internal state sufficient for the declared responsibility, and what information would be missing if it is not?

## 11. Formal audit and counterexamples

Report:

- mechanized theorem coverage;
- exhaustive finite countermodel battery;
- assumptions discovered necessary by hostile mutation;
- zero-overhead and strict-overhead controls.

Every theorem in the main text should link to a checker/proof identifier.

## 12. Implications for learning objectives

Only derive implications licensed by theory. Candidate implications:

1. predictive loss cannot by itself certify a representation's sufficiency for another responsibility;
2. predictive compression may conflict with epistemic-state retention;
3. an auxiliary responsibility objective/constraint can be interpreted as purchasing conditional state information;
4. external observation/retrieval can supply information not present in the internal state;
5. compression/distillation evaluations should test declared secondary responsibilities rather than only language loss.

No training algorithm is claimed superior.

## 13. Limitations and nonclaims

State explicitly:

- finite/discrete exact theorems are the current foundation;
- real transformer hidden states are high-dimensional and usually non-minimal;
- responsibilities are externally declared scientific/decision constructs, not proof of philosophical belief;
- empirical existence/use of the required information remains a separate research question;
- institutional authority is external;
- the approximate rate region may contract to classical conditional rate distortion;
- no theorem proves Machine Epistemics replaces transformers.

---

# Abstract skeleton

The final abstract should follow this logical order:

1. autoregressive models are trained/evaluated primarily through linguistic prediction;
2. predictive sufficiency is a representation property relative to that target;
3. introduce a distinct epistemic responsibility variable/family;
4. state the separation theorem;
5. state maximal-compression theorem;
6. state exact deterministic overhead;
7. state approximate/frontier result only if completed;
8. explain the design implication without claiming empirical improvement.

Do not begin with “Machine Epistemics is a new field.” Let the mathematics earn the terminology.

---

# Candidate headline theorem text

> **Theorem (predictive compression and responsibility loss, informal).** Let `S_P` be the minimal state sufficient for the complete linguistic future of a finite autoregressive process. Every deterministic predictive-sufficient representation has entropy at least `H(S_P)`, and equality makes it isomorphic to `S_P`. Consequently, if a declared responsibility `Q` is not sufficient from `S_P`, no entropy-minimal predictive representation can be sufficient for `Q`. For deterministic `Q`, exact responsibility recovery while retaining `S_P` requires an additional `H(Q|S_P)` bits of state on average, and this rate is achievable.

The formal wording must follow the checked theorem exactly.

---

# Figure/table plan

Only generate after the checker outputs exist.

### Figure 1 — predictive fibres and epistemic split
Show histories collapsed by identical future law, with a responsibility variable splitting one predictive fibre. Purpose: make T1/T2 visually immediate.

### Figure 2 — exact overhead
For finite fixtures, plot/tabulate `H(Q|S_P)` against measured minimal augmentation. Purpose: checker visualization, not empirical LLM performance.

### Figure 3 — approximate frontier
Only if T8 survives. Show the state-rate / epistemic-risk curve for the solved family.

### Table 1 — theorem ownership
Rows T1–T9; columns exact ORION statement, nearest parent theorem, residual, authority.

### Table 2 — assumption attacks
For T2/T3, list removed assumption, smallest countermodel, corrected scope.

---

# Publication gates

## Theory gate

- [ ] T1–T7 independently/mechanically checked.
- [ ] No hidden assumption discovered by finite countermodel search remains unstated.
- [ ] T2 still has a nontrivial interpretation after strongest-parent review.
- [ ] T3 exact overhead is correct and properly positioned as theorem/corollary.
- [ ] T8 either produces a real residual or is removed/marked parent-owned.

## Novelty gate

- [ ] Reproducible theorem-level literature matrix complete.
- [ ] Sevetlidis 2026 representation-identifiability work explicitly subtracted.
- [ ] Causal-state / reward-predictive-state literature explicitly subtracted.
- [ ] Conditional rate-distortion ownership explicit.
- [ ] LLM belief/truth/uncertainty work integrated without claiming absence of internal structure.

## Journal gate

- [ ] One clear ML design consequence follows from the theorems.
- [ ] Manuscript readable without ORION-internal vocabulary.
- [ ] Hostile reviewer simulation has no unresolved fatal objection.
- [ ] All theorem source/checker artifacts publicly reproducible.
- [ ] Title/abstract contain no empirical LLM performance claim.

---

# Kill / contraction rule

A top-tier goal does not protect this paper from contraction.

If the strongest parent composition already contains the complete mathematical result, close as `CLASSICAL_PARENT_SUFFICIENT__MERGE_OR_DROP`.

If T1–T3 survive but T8 does not and the result is too narrow for JMLR, close as `THEOREM_SCOPE_TOO_WEAK_FOR_JMLR__FIELD_THEORY_PAPER_ONLY` and target the strongest honest field venue.

If formal checking finds a fatal error that cannot be repaired without changing the scientific identity, close as `CANNOT_CHECK_FORMAL_PROOF` or open a new successor identity rather than laundering the failed theorem.

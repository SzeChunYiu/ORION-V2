# JMLR Simulated Review Round V1

**Manuscript reviewed:** `MANUSCRIPT_V10_ARXIV_JMLR_MASTER.md`  
**Method:** `academic-paper-pipeline@d2cac7bd...` editor/reviewer decision model.  
**Authority:** internal simulated review only; not independent external peer review.

The three reviewer lenses were evaluated separately before editor synthesis. Reviewer votes are not used as the decision rule.

---

# Reviewer 1 — validity, definitions and proof scope

## Summary

The manuscript is careful about its registered prediction protocol, decision semantics and empirical nonclaims. The one-bit example is correct under the stated construction, and the complete joint-action intersection fixes the earlier pairwise-collision weakness. The main technical risk is not false mathematics but the boundary between a general theorem and an illustrative counterexample.

### R1-C1 — Generalize the central formal statement

**Severity:** major, repairable.  
**Concern:** The current Theorem 1 is stated as an existence result and then proved by the one-bit example. The paper later contains a stronger exact one-step characterization: a representation/evidence cell is implementable iff the joint acceptable-action intersection is nonempty. The formal hierarchy would be clearer if the compatibility characterization were stated first as the general theorem, with prospective no-certification as a corollary and the one-bit provenance construction as the minimal witness.

**Resolution test:** theorem order becomes:

1. one-step compatibility theorem;
2. corollary: current responsibility adequacy is not a prospective certificate unless the corresponding future compatibility condition holds for every registered event/cell;
3. one-bit counterexample with exact state costs.

**Status:** open for revision.

### R1-C2 — Separate one-step decision adequacy from recurrent-memory adequacy

**Severity:** major clarification.  
**Concern:** The manuscript uses `C_dyn^*` based on recursively updateable state but the complete intersection theorem is one-step. A reader could infer that the one-step criterion alone characterizes multi-step memory.

**Resolution test:** explicitly state that the joint-action intersection is exact for one registered future step with event/history visible as specified, whereas multi-step compression requires the recurrent/right-congruent parent construction. Do not use one-step compatibility to imply recurrent minimality.

**Status:** already mostly present; strengthen the theorem boundary.

### R1-C3 — Mechanical status of three-history tied-action control

**Severity:** minor/reproducibility.  
**Concern:** elementary proof exists but distinct checker is pending.

**Resolution test:** keep proof in main/appendix and label the checker as pending until run. The theorem does not need computation for validity.

**Status:** resolved by wording; no scientific blocker.

---

# Reviewer 2 — contribution, prior work and JMLR significance

## Summary

The manuscript is unusually honest about parent ownership. That honesty also reveals the publication risk: much of the mathematics is classical. The paper's case for JMLR must therefore stand on the assessment problem and its relevance to contemporary representation compression/memory, not on `C_stat`, `C_dyn` or finite-state minimization.

### R2-C1 — “What is the new scientific object?”

**Severity:** blocking for JMLR if unclear.  
**Concern:** A reader could summarize the paper as “future tasks may require information current tasks do not.” That is too generic.

**Resolution test:** define the new assessment object in one sentence early:

> matched-current prospective revision certification: after matching a representation on the declared current predictive and decision responsibilities, intervene on retained historical state, present common later evidence, and test whether the correct update/maintain decision remains implementable after excluding reconstruction routes.

Then organize contributions/figures around that object.

**Status:** open for stronger phrasing.

### R2-C2 — Direct-neighbor discrimination should be decision-level

**Severity:** major.  
**Concern:** The discussion of Belief-R, MEMENTO, PM-Bench and memory systems is strong but still mostly prose. JMLR readers need a compact comparison of *assessment question*, not a marketing checklist.

**Resolution test:** main-text table with rows for direct neighbors and columns describing: current-behavior matching, representation-state intervention, common later evidence, update+maintain, alternate-channel reconstruction control, and the exact question answered. Avoid “ours has every checkmark” framing.

**Status:** display already specified in supporting artifacts; elevate into the scientific master.

### R2-C3 — Real-LLM experiment

**Severity:** target-priority risk, not validity blocker.  
**Concern:** A theory/assessment paper without any real-model demonstration may be judged too abstract.

**Resolution test:** either (a) external editor confirms theory/assessment paper can stand; or (b) add the already frozen optional real-LLM audit as a separately versioned empirical extension. Do not invent an empirical section post hoc solely to rescue novelty.

**Status:** external editorial risk remains; no internal repair without new evidence.

---

# Reviewer 3 — reproducibility, readability and boundaries

## Summary

The revised public manuscript is much cleaner than the earlier repository-facing draft. Definitions are understandable to an ML reader, and the practical protocol is concrete. The remaining readability risk is notation density before the assessment procedure appears.

### R3-C1 — Move assessment identity earlier

**Severity:** major readability.  
**Concern:** Sections 2–6 contain several formal objects before the reader sees the complete audit. The Introduction should provide a compact workflow preview so the notation has a purpose.

**Resolution test:** add a 4-step audit preview in the Introduction and a simple main schematic. Keep detailed Protocol V3 later.

**Status:** open for revision.

### R3-C2 — Reduce parent-owned derivation in main text

**Severity:** moderate.  
**Concern:** `C_stat`/`C_dyn` derivations are useful but could dominate the paper and make the residual look smaller.

**Resolution test:** keep definitions and intuition in main text; move selector/right-congruence proof details and generic entropy identities to appendix. Main text should spend more space on what the audit detects that current evaluations do not distinguish.

**Status:** open for journal-length assembly; arXiv may retain fuller theory.

### R3-C3 — AI-assistance statement

**Severity:** integrity/compliance.  
**Concern:** current disclosure is appropriately broad. It should be retained and refreshed against the live venue policy; human adoption is essential.

**Status:** unresolved human gate, not manuscript-science defect.

---

# Editor synthesis

## Must address before arXiv scientific freeze

- `R1-C1`: reorder formal hierarchy around the complete compatibility theorem.
- `R1-C2`: sharpen one-step versus recurrent-memory boundary.
- `R2-C1`: name the matched-current prospective-revision certification object explicitly.
- `R3-C1`: preview the audit earlier.

## Must address before JMLR filing

- `R2-C2`: compact direct-neighbor assessment-question table in main text.
- `R3-C2`: journal main-text discipline/appendix allocation.
- human intellectual-ownership and AI-use gate.
- external target-significance judgment remains useful but does not license claim changes.

## Cannot be repaired internally without new evidence

- `R2-C3`: whether JMLR editorial priority requires a real-model illustration. The scientific manuscript must remain valid without pretending this evidence exists.

## Editor current decision

```text
SCIENTIFIC_VALIDITY = PASS_WITH_MAJOR_PRESENTATION_REPAIR
PRIOR_WORK_HONESTY = PASS
THEORY_NOVELTY = CONTRACTED_CORRECTLY
ASSESSMENT_OBJECT = PLAUSIBLE_BUT_NEEDS_SHARPER_CENTERING
ARXIV = REVISE_THEN_SCIENTIFICALLY_MATURE
JMLR = BORDERLINE_HIGH_RISK_AFTER_REVISION
```

The minimum-sufficient revision is to recenter the formal structure and audit identity, not to add more mathematical machinery.

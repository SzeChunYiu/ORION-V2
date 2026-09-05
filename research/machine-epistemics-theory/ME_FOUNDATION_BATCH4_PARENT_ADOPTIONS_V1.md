# Machine Epistemics Foundation — Batch 4: parent-owned learning/equivalence adoptions

**Status:** parent-subtraction/adoption artifact. **NO NOVELTY OR NEW-THEOREM CLAIM.** This batch closes MEG-14 and MEG-32 by correcting two over-compressed atlas shorthands and binding the mature parent objects that the OCM/V2 evaluation should use.

## P1 — MEG-14: acquisition complexity is channel/model specific; teaching dimension is not membership-query complexity

The atlas provisionally compressed several acquisition channels into one line:

> INSTRUCTION = teaching dimension; INTERACTION = extended teaching dimension = membership-query complexity; DEMONSTRATION = PAC/exact sample complexity; EXPERIMENTATION = closure in |D| evaluations.

That is too coarse. The relevant quantities belong to different information protocols and are not generally equal.

### Adopted parent distinctions

1. **Helpful-teacher instruction.** For a finite concept class `C`, the classical teaching dimension measures the smallest labelled teaching set a teacher who knows the target can choose to uniquely specify the target (class TD is the worst target). Goldman & Kearns (JCSS 1995, *On the Complexity of Teaching*) own this object.
2. **Learner-chosen membership queries.** Exact membership-query complexity is the minimum worst-case adaptive decision-tree depth when the learner selects query points and receives labels. Hegedűs (COLT 1995, *Generalized Teaching Dimensions and the Query Complexity of Learning*) relates this complexity to extended teaching/specification dimensions with lower/upper bounds; it is not definitionally identical to ordinary teaching dimension.
3. **Demonstration/random examples.** Sample complexity depends on the sampling and success criterion (PAC, exact identification under a distribution, realizable/noisy model, etc.). A helpful teacher's chosen examples may not be reported as random-sample efficiency.
4. **Experiment/interaction.** Query/experiment complexity depends on what actions are admissible and what the registered outcome function reveals. MEG-15 already separates a registered discriminating observation from raw feedback.
5. **Lifecycle information.** Revocation/closure information is separately accounted by the existing lifecycle-identifiability/Warrant-Lift lower bounds. It is not free merely because an acquisition channel delivered it.

### Exact counterexample to `TD = #MQ`

Let the domain have three binary query coordinates and concept class

`C = {000, 011, 101}`.

- Every target has a one-example teaching set when the teacher knows which target is intended: query coordinate 0 distinguishes `101`; coordinate 1 distinguishes `011`; for `000`, either coordinate 0 or 1 plus the observed 0 uniquely selects it among the class. Hence `TD(C)=1`.
- A membership-query learner does not know the target. Any first query has two possible targets sharing one answer, so one query cannot identify all three concepts. Two adaptive queries suffice. Hence `#MQ(C)=2`.

Therefore ordinary teaching dimension and membership-query complexity are **not the same resource** even on a tiny finite class.

### Machine Epistemics adoption rule

Every learning/acquisition receipt must state its **information protocol** before quoting a bound:

```text
protocol = HELPFUL_TEACHER | MEMBERSHIP_QUERY | EQUIVALENCE_QUERY |
           RANDOM_EXAMPLES | REGISTERED_INTERACTION | EXHAUSTIVE_EXPERIMENT | ...
target class / domain
noise/realizability assumptions
success notion = exact | PAC(ε,δ) | query-family agreement | lifecycle-equivalence | ...
resource counted = labelled examples | queries | bits | verifier calls | experiments | ...
parent theorem/bound and assumptions
```

No cross-channel comparison may substitute one parent's complexity number for another protocol. The common `MEG-31` certified-information quantity may be reported in addition, but it does not erase protocol-specific costs.

**Terminal:** `MEG-14 = PARENT_OWNED_ADOPTED_WITH_CORRECTION__CHANNEL_PROTOCOLS_NOT_ONE_BOUND`.

No new learning-complexity theorem is claimed.

---

## P2 — MEG-32: PARENT_SUFFICIENT requires equivalence/noninferiority evidence, not failure to reject difference

The programme already requires a pre-registered equivalence margin for parent-sufficiency decisions. This batch makes the statistical ownership explicit for paired binary outcomes.

### Parent rule

For paired binary outcomes, McNemar-type procedures address paired differences using discordant pairs. A large ordinary two-sided `p` value for the null of no difference is **not evidence of equivalence**. Equivalence/noninferiority is a different hypothesis problem and requires a scientifically chosen margin plus a method valid for paired binary data.

The paired-binary literature includes exact/unconditional equivalence and noninferiority tests and confidence intervals (Hsueh, Liu & Chen, *Biometrics* 2001; Liu et al., *Statistics in Medicine* 2002). The general TOST logic likewise requires both one-sided inequalities relative to predeclared equivalence bounds, rather than `p>0.05` under a difference test.

### Adoption contract for a paired-binary `PARENT_SUFFICIENT` row

A result may route to statistical equivalence only when the frozen design binds:

```text
estimand                 # e.g. paired risk difference
margin = [-Δ, +Δ]        # scientific, pre-outcome
alpha
paired analysis method + version
handling of small n / exactness
confidence interval or equivalent two-one-sided decision
power/sample-size plan
missing/invalid-pair policy
```

The acceptance rule is method-specific but must implement the registered equivalence null. A simple CI form is:

`EQUIVALENT` only if the registered `(1-2α)` equivalence CI lies wholly inside `[-Δ,+Δ]`.

If the required interval/test cannot be computed, return `CANNOT_CHECK`. If an ordinary difference test merely yields `p>α`, report `NO_DIFFERENCE_NOT_REJECTED`, never `EQUIVALENT` or `PARENT_SUFFICIENT` on that fact alone.

### Hostile zero-discordance case

With only five paired observations and zero discordant pairs, an ordinary McNemar-style difference test supplies no evidence of a directional difference and may return a maximal p-value. That does not by itself establish any scientifically meaningful equivalence margin: uncertainty and the chosen margin still govern. The planted policy mutant `p>0.05 ⇒ equivalent` is therefore rejected even in the superficially strongest tie case.

### Programme consequence

`PARENT_SUFFICIENT` remains a scientific terminal, but its statistical route must distinguish:

- exact identity/by-construction equality (reported as identity, not measured equivalence),
- measured paired equivalence under a frozen margin/procedure,
- underpowered or inconclusive difference testing,
- and `CANNOT_CHECK`.

**Terminal:** `MEG-32 = PARENT_OWNED_ADOPTED__PREDESIGNATED_EQUIVALENCE_MARGIN_AND_PAIRED_METHOD_REQUIRED`.

No ORION-specific statistical test is invented.

---

# Batch-4 terminal

```text
MEG-14 = PARENT_OWNED_ADOPTED_WITH_CORRECTION__CHANNEL_PROTOCOLS_NOT_ONE_BOUND
MEG-32 = PARENT_OWNED_ADOPTED__PREDESIGNATED_EQUIVALENCE_MARGIN_AND_PAIRED_METHOD_REQUIRED
GENERAL_NOVELTY = NOT_ESTABLISHED
```

These closures reduce the remaining Foundation V1 atlas frontier to seven rows: MEG-07/09/23/24/25/27/34. Those require either new theory, protected empirical evidence, or language-stage implementation/evaluation and are not manufactured here.

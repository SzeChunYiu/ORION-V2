# Hostile Editor Review V2 — Post-Mechanization, Post-Parent-Contraction

**Issue:** #51  
**Object reviewed:** `MANUSCRIPT_DRAFT_V5.md` + `PROSPECTIVE_REVISION_AUDIT_PROTOCOL_V1.md`.  
**Authority:** internal adversarial review only; not external peer review.  
**Question:** Is there still a standalone paper, and if so is JMLR the right target?

## Panel

1. **JMLR action-editor lens** — significance, breadth, originality, practical utility.
2. **Statistical decision/information-theory lens** — parent ownership and theorem delta.
3. **Sequential control/state-representation lens** — POMDP/AIS/PSR/FSM/stable-quotient overlap.
4. **NLP/LLM evaluation lens** — Belief-R and representation-audit distinctness.
5. **Representation-learning/systems lens** — operational measurability and practical experiment design.

---

# Review 1 — JMLR action-editor lens

## Strongest objection

> The manuscript now concedes that nearly all of its mathematical machinery is established. `S_P` is predictive-state theory; current decision state is decisional/decision theory; recursive refinement is information-state/FSM theory; rate tradeoffs are established; belief revision is already evaluated. Why should JMLR publish another notation layer around these ingredients?

## Assessment

**Serious and potentially fatal for JMLR.**

The correct response is not to deny the premise. The paper must be evaluated under JMLR's explicit route for a new **learning task / assessment method / analytical framework**.

The surviving delta is:

- the audit fixes a *language prediction reference channel*;
- matches current decision adequacy;
- then tests representation-dependent revision after later evidence;
- the exact witness proves present prediction+decision cannot certify the prospective property;
- the audit protocol identifies how to run the test causally rather than merely evaluate output revision.

This can be a useful ML assessment paper. Whether it is **significant enough for JMLR** remains judgmental.

### Verdict

`JMLR: LEAN_REJECT_IF_SUBMITTED_TODAY__ENCOURAGE_ASSESSMENT_FRAMEWORK_IF_POLISHED`.

Reason: scientific content is sound and interesting, but the broad-interest/originality margin is thin after the 2026 parent sweep.

---

# Review 2 — decision/information-theory lens

## Strongest objection

> `C_stat`, `C_dyn`, and `Omega_dyn` are constructed from ordinary conditional entropy over state partitions. The difference of two parent-owned optimization values is not a new theorem. The no-certification proposition is an elementary indistinguishability witness. The paper risks marketing definitions as mathematics.

## Assessment

**Correct objection.**

Required concession is already adopted:

- `Omega_dyn` is a **derived audit metric**, not a new information law.
- P0/P1/P2 is an analytical taxonomy.
- the finite theorem machinery is used for semantics and falsification, not foundational novelty.

What still has value:

- conditional accounting relative to a separate linguistic predictive quotient;
- explicit responsibility semantics avoiding over-storage of target labels;
- the representation-audit task induced by the one-bit witness.

### Verdict

`MATHEMATICAL_NOVELTY: WEAK`  
`MATHEMATICAL_SOUNDNESS: STRONG_AFTER_MECHANICAL_AUDIT`  
`PUBLISHABLE_ONLY_IF_FRAMED_AS_ASSESSMENT_FRAMEWORK`.

---

# Review 3 — sequential control/state-representation lens

## Strongest objection

> AIS already defines a history statistic sufficient for present reward/performance and prediction of its next state, with recursive update variants. ISFSM closed covers already combine compatibility with successor closure. Zhang et al. 2026 now prove a coarsest stable quotient and minimal memory in a structured POMDP. Your P2 state is a rephrasing of “current compatible quotient is not Markov; refine until stable.”

## Assessment

**Correct for generic state theory.**

The paper now states this explicitly and removes core novelty credit from C09/C10.

Residual difference:

- the base quotient is not the environment observation or reward partition but a **declared complete linguistic future**;
- the additional variable may be source/provenance/lineage information with no language-prediction effect;
- the practical test manipulates retained representation while matching present language+decision behavior.

That is a cross-domain application/formal assessment distinction, not a new state-minimization theorem.

### Verdict

`GENERIC_DYNAMIC_THEORY_NOVELTY = NO`  
`AUTOREGRESSIVE_REPRESENTATION_AUDIT_SPECIALIZATION = PLAUSIBLY_DISTINCT`.

---

# Review 4 — NLP/LLM evaluation lens

## Strongest objection

> Belief-R already tests update versus maintain after new evidence. Recent 2026 work studies numerical belief updating, evidence selection, and decision-aware LLM memory. Why is your proposed audit not just Belief-R plus memory ablation?

## Assessment

This is the most important **nonfatal** objection.

The answer must be concrete:

### Belief-R object

```text
premises_t -> conclusion_t
new premises -> update/maintain conclusion_t+1
```

### #51 object

```text
same initial history family
-> create/compare retained representations
-> require matched language prediction + current responsibility
-> freeze representation intervention
-> reveal later evidence
-> test selective update/maintain
```

The new independent variable is **what historical information remains in the representation after current behavior is matched**.

The causal claim is correspondingly narrower:

> retention of a dormant distinction may be necessary for later revision.

This is not established by ordinary output-level revision accuracy.

The protocol's independent-support, unrelated-evidence, recoverable-from-future, P0 and P1 controls make this distinction meaningful.

### Verdict

`ASSESSMENT_DISTINCTNESS = YES_IN_PRINCIPLE`  
`EMPIRICAL_LLM_DISTINCTNESS = NOT_DEMONSTRATED`.

For a pure theory paper, the exact witness supports necessity of the third audit coordinate. A stronger empirical paper would still be possible later without retraining an LLM.

---

# Review 5 — representation-learning / systems lens

## Strongest objection

> `S_P` cannot be computed for a real LLM, hidden-state entropy is not directly measurable, and intervention on a representation may change current behavior. How does this become a usable assessment rather than an idealized finite-state story?

## Assessment

This objection affects generality, not the finite result.

The protocol answers it by separating:

- theoretical reference state from empirical surrogate;
- present-equivalence gate from future comparison;
- operational capacity measures from hidden dimension;
- causal memory/state intervention from pure probing.

A real-model study should not claim to recover exact `S_P`. It should say it matches the frozen language surrogate and current decision within tolerance.

Potential useful surfaces include:

- explicit context/memory ablation;
- deterministic summaries;
- typed agent memory;
- KV-cache compression where controllable;
- hidden-state projection only when present behavior remains matched.

### Verdict

`PRACTICAL_UTILITY = PLAUSIBLE`  
`DIRECT_HIDDEN_STATE_THEORY_TRANSFER = LIMITED_AND_MUST_BE_SCOPED`.

---

# 6. Additional hostile objections

## H1 — “Cross-channel” is new jargon for side information

**Disposition:** mostly correct.

Use “cross-channel” sparingly. Define it operationally as a responsibility whose acceptable decision does not factor through the declared linguistic predictive state. Do not imply a new information-theoretic primitive.

## H2 — The provenance example is hand-authored to force one bit

**Disposition:** correct but not fatal.

It is a theorem witness, not empirical evidence. The paper must not use it to argue frequency in real tasks. Its role is to prove non-certification.

## H3 — Any full-history baseline trivially solves the problem

**Disposition:** expected.

The question is not whether full history is sufficient but what can be compressed while preserving a bounded responsibility/horizon. Full-history recovery is the upper-bound control.

## H4 — An LLM may reconstruct source identity from weights or later text

**Disposition:** important empirical control.

The protocol includes a future-evidence-reconstructs-state terminal and requires a controlled state manipulation. A real-model audit must check whether the supposedly removed variable remains recoverable elsewhere.

## H5 — State cost is not comparable across neural models

**Disposition:** correct.

Conditional entropy is an exact finite coordinate. Real-model cost must use a registered operational capacity measure. No universal bit interpretation is claimed for raw hidden dimensions.

## H6 — Why call this Machine Epistemics rather than memory or control?

**Disposition:** do not make the field label load-bearing.

The paper title and theory should stand without “Machine Epistemics”. The broader programme is discussed only as motivation/context.

---

# 7. Claim-by-claim hostile disposition

| Claim family | Hostile verdict |
|---|---|
| minimal predictive state | parent-owned |
| secondary target may be absent | parent-owned |
| decision state / decision complexity | parent-owned |
| static state minimization | parent/specialization |
| dynamic right-congruent state | parent/specialization |
| selector equivalence | parent/specialization |
| `Omega_dyn` | useful derived audit metric; weak independent math novelty |
| one-bit witness | valid known-answer witness |
| P0/P1/P2 | useful audit taxonomy; not deep theorem novelty |
| horizon curve | useful audit profile; parent-pressure high |
| deficit identities | parent-owned |
| universality boundary | classical/no-free-compression style boundary |
| prospective revision audit | strongest surviving contribution |
| real-LLM P2 failure | not established |

---

# 8. Venue recommendation

## JMLR

Current simulated recommendation:

`LEAN_REJECT / REJECT_WITH_ENCOURAGEMENT_TO_REFRAME_AS_ASSESSMENT_FRAMEWORK`.

A JMLR submission **today** would be premature because J8 (distinct enough from parent product) remains editor-dependent and no independent external review has tested the new V5 framing.

This is not a request for more scientific invention. Further progress should be editorial/verification only:

- exact bibliography/theorem binding;
- delete the unmechanized non-load-bearing T8D if not checked;
- tighten V5 into the audit identity;
- generate finite audit figures/tables;
- run an external or genuinely independent hostile review if available.

## TMLR

Simulated recommendation:

`LEAN_ACCEPT_AFTER_FINAL_TECHNICAL_BINDING`.

Reason: TMLR's current acceptance criteria center supported claims and audience interest rather than a strong novelty threshold. The mechanically audited framework and clear revision-memory lesson plausibly satisfy that standard if presented carefully.

## Specialist theory / integration

Also legitimate:

- strong field theory/decision/state-representation venue if the finite mathematics is emphasized;
- merge into the Machine Epistemics flagship if standalone interest is judged insufficient.

---

# 9. Scientific terminal from hostile review

```text
TECHNICAL_SOUNDNESS = STRONG
CORE_THEOREM_NOVELTY = CONTRACTED
PROSPECTIVE_AUDIT_DISTINCTNESS = PLAUSIBLE
REAL_LLM_EVIDENCE = NONE
JMLR_SIGNIFICANCE = OPEN_HIGH_RISK
TMLR_FIT = GOOD
STANDALONE_PAPER = STILL_JUSTIFIED_AS_ANALYTICAL_ASSESSMENT_CANDIDATE
MANUSCRIPT_ZOMBIE = NO
```

The correct next work is not to invent more theory. It is to finish mechanical/citation binding and route the already-defined paper honestly.

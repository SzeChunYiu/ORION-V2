# Figure and Display Specification V1

**Issue:** #51  
**Purpose:** let a mechanical formatter generate publication displays without deciding the scientific narrative.

No figure may introduce new empirical data or imply a real-LLM result.

## Figure 1 — No-certification witness

### Scientific question

How can two representations be identical for the **registered current prediction target** and current decision yet differ under the same later evidence?

### Layout

Two horizontal lanes.

**Full/augmented state**

```text
registered reference protocol rho

h_A: S_{P,rho} = s, action = RETAIN, provenance = A
h_B: S_{P,rho} = s, action = RETAIN, provenance = B
          | same controlled later event: RETRACT(A)
          v
h_A' -> REOPEN
h_B' -> RETAIN
```

**Compressed current state**

```text
Z_c(h_A) = Z_c(h_B) = s
current action = RETAIN
          | same controlled later event: RETRACT(A)
          v
one identical (state,event) input cannot map deterministically
both to REOPEN and RETAIN
```

### Required annotations

```text
prediction target is scoped to registered rho
future evidence is a distinct registered intervention
C_stat^* = 0 bits
C_dyn^*  = 1 bit
Omega_dyn = 1 bit
current optimal action is unique
```

### Caption

> **A present-equivalent pair can require a dormant distinction for later revision.** Under the registered reference input protocol `rho`, the two equiprobable histories share the same declared linguistic predictive state and unique present action. A common later controlled event, `RETRACT(A)`, makes their correct successor decisions incompatible. A representation that merged the provenance bit cannot deterministically realize both revisions; retaining one bit suffices. The construction is relative to the registered prediction/intervention channels and is a finite no-certification witness, not evidence that deployed LLMs generally behave this way.

### Prohibitions

- no brain/LLM illustration;
- no “knowledge” box implying consciousness;
- no performance bar chart;
- no real-model label;
- no wording implying sufficiency for every possible future intervention.

---

## Figure 2 — P0/P1/P2 audit map

### Scientific question

Which representation obligation is failing?

### Axes

Horizontal:

`current extra responsibility state C_stat^*`

Vertical:

`future-only dynamic premium Omega_dyn`

### Regions

- P0 at origin: `C_stat^*=0`, `Omega_dyn=0`.
- P1 on horizontal axis away from origin: `C_stat^*>0`, `Omega_dyn=0`.
- P2 in upper half-plane: `Omega_dyn>0`, with either zero or positive static cost.

### Separate pre-phase/control boxes

`ACQUISITION / NON-IDENTIFIABILITY`

and

`STRONGER CONTROLLED REFERENCE TARGET`

The first sits outside the plane because missing evidence is not representation compression. The second indicates that if the prediction/state target explicitly includes the later intervention family, a former P2 distinction may become current-state-relevant and the premium may contract.

### Caption

> **Audit taxonomy by when additional information becomes decision-relevant.** P0 requires no state beyond the registered linguistic predictive reference for the registered responsibility process. P1 requires additional cross-channel state for the current decision but no future-only refinement. P2 requires additional state solely or additionally for later evidence-triggered revision. Missing initial evidence is a pre-phase acquisition problem. A stronger controlled reference target can legitimately move a case toward P0/P1, emphasizing that the taxonomy is target- and channel-relative.

### Prohibition

Do not label axes “intelligence,” “understanding,” “epistemic quality,” or “trust.”

---

## Figure 3 — Prospective Revision Audit V3 flow

### Scientific question

What must be controlled before a revision failure can be attributed to representation loss?

### Flow

```text
REGISTER
  prediction reference protocol rho
  current responsibility
  future evidence intervention family
  future responsibility
        |
        v
PRESENT-EQUIVALENCE GATE
(prediction margin + current action/risk + resources matched)
        |
        v
REPRESENTATION INTERVENTION / STATE COMPARISON
        |
        v
ALTERNATE-CHANNEL + PARAMETRIC RECONSTRUCTION GATE
(context / KV / hidden / summary / retrieval / tool / external memory / params)
        |
   +----+------------------------------------+
   | removal supported                      | information remains / reconstructable / cannot check
   v                                        v
COMMON LATER EVIDENCE                  NO STRONG P2 STATE-LOSS ATTRIBUTION
   |
   v
JOINT FUTURE-ACTION COMPATIBILITY
I(z,x) = intersection of acceptable actions in merged cell
   |
   v
SCORE UPDATE + MAINTAIN / SELECTIVE REOPENING
   |
   v
P0 / P1 / P2 / ACQUISITION / RECONSTRUCTED /
CONTROLLED-TARGET-CONTRACTION / CANNOT_CHECK
```

### Caption

> **Prospective Revision Audit V3.** The prediction target and later evidence-intervention family are registered separately. Future revision is compared only after present predictive/current-decision equivalence is established using a prospectively frozen equivalence rule. A representation intervention must then survive alternate-channel and parametric-reconstruction checks. After the same later evidence, exact one-step compatibility is determined by the joint intersection of acceptable future actions for each merged representation/evidence cell; pairwise disjoint sets are easy failure witnesses but are not a complete positive test under ties. Both correct updating and correct maintaining/selective reopening are scored.

---

## Figure 4 — Complete compatibility versus pairwise collision control

### Scientific question

Why is absence of a pairwise collision not enough under tied future actions?

### Layout

Three circles/sets or a compact table:

```text
history h1: {a,b}
history h2: {b,c}
history h3: {a,c}

pairwise intersections: nonempty
joint intersection: empty
```

Beside it, the unique-action canonical witness:

```text
{REOPEN} vs {RETAIN}
pairwise intersection = empty
```

### Caption

> **Pairwise collision is a sufficient failure witness but not a complete compatibility test.** Three tied-action histories can overlap pairwise while admitting no common future action. The complete one-step `ANY_OPTIMAL_ACTION` criterion is the joint acceptable-action intersection over the entire merged representation/evidence cell. In the canonical one-bit witness, future acceptable actions are singleton and the pairwise collision is therefore complete.

### Priority

Useful as a small inset/table; omit if Section 10 text explains the point within page budget.

---

## Table 1 — Parent ownership versus residual

Source:

`REVIEWER_TABLES_V1.md`, Table 1.

Keep in main paper if page budget permits. This table directly prevents novelty ambiguity and is more valuable than a generic taxonomy figure.

---

## Table 2 — Direct-neighbor comparison

Source:

`REVIEWER_TABLES_V1.md`, Table 7.

Must include at minimum:

- Belief-R;
- MEMENTO;
- PM-Bench;
- state-compression relay;
- Router-Mem;
- decision-aware/bounded-memory work.

Do not convert it into a checkmark-heavy “ours is the only complete system” marketing table. Use prose-like cells describing different registered questions.

---

## Table 3 — Mechanical validation

Generate from frozen receipts only.

Recommended rows:

| Group | Scope | Result |
|---|---|---|
| Static partitions | all partitions n=1..7; Bell verified | PASS |
| Responsibility semantics | R21–R27 + tie control | PASS |
| Deficit identities | 900 rational worlds + controls | PASS |
| Dynamic equivalence | direct versus selector-refinement fixtures | PASS |
| One-bit witness | canonical fixture | `0 / 1 / 1` bits |
| Phase/horizon | P0/P1/P2 + monotone/stabilizing curves | PASS |
| Universality | U1–U5 | PASS |
| Mutation battery | M1–M6 | 3 refuted relaxations / 3 narrower survivors |
| Mixed-P2 search | 5,826 small machines | CANNOT_CHECK no witness |
| Complete one-step compatibility | three-history `{a,b}/{b,c}/{a,c}` control | PENDING distinct mechanical checker; elementary proof frozen |

Never turn CANNOT_CHECK or PENDING into PASS.

---

## Optional Figure 5 — horizon curves

Only include if generated receipt curves are genuinely informative visually.

Scientific message:

`C_k^*` is monotone and can stabilize after different horizons across registered finite fixtures.

Do not imply empirical LLM memory depth.

If curves are visually trivial, use a compact table or omit the figure.

---

# Figure priority under page pressure

1. Figure 1 — one-bit witness: **mandatory**.
2. Figure 3 — V3 audit flow: **strongly preferred**.
3. Table 1 — parent ownership: **strongly preferred**.
4. Table 2 — direct neighbors: **strongly preferred**.
5. Figure 2 — phase plane: useful but removable if text/table suffices.
6. Figure 4 — compatibility correction: small inset/table if space permits.
7. Table 3 — mechanical validation: can move to appendix if main is crowded.
8. Figure 5 — optional.

No decorative figure is authorized.

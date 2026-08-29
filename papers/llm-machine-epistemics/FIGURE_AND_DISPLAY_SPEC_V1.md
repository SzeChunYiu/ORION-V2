# Figure and Display Specification V1

**Issue:** #51  
**Purpose:** let a mechanical formatter generate publication displays without deciding the scientific narrative.

No figure may introduce new empirical data or imply a real-LLM result.

## Figure 1 — No-certification witness

### Scientific question

How can two representations be identical for current prediction/decision yet differ under the same later evidence?

### Layout

Two horizontal lanes:

**Full/augmented state**

```text
h_A: S_P = s, action = RETAIN, provenance = A
h_B: S_P = s, action = RETAIN, provenance = B
          | same future event: RETRACT(A)
          v
h_A' -> REOPEN
h_B' -> RETAIN
```

**Compressed current state**

```text
Z_c(h_A) = Z_c(h_B) = s
current action = RETAIN
          | same future event: RETRACT(A)
          v
one identical (state,event) input cannot map deterministically
both to REOPEN and RETAIN
```

### Required annotations

```text
C_stat^* = 0 bits
C_dyn^*  = 1 bit
Omega_dyn = 1 bit
current optimal action is unique
```

### Caption

> **A present-equivalent pair can require a dormant distinction for later revision.** The two equiprobable histories share the declared linguistic predictive state and the same unique present action. A common later event, `RETRACT(A)`, makes their correct successor decisions incompatible. A representation that has merged the provenance bit cannot deterministically realize both revisions; retaining one bit suffices. The construction is a finite no-certification witness, not evidence that deployed LLMs generally behave this way.

### Prohibitions

- no brain/LLM illustration;
- no “knowledge” box implying consciousness;
- no performance bar chart;
- no real-model label.

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

### Separate pre-phase box

`ACQUISITION / NON-IDENTIFIABILITY`

This should sit outside the P0/P1/P2 plane because missing evidence is not representation compression.

### Caption

> **Audit taxonomy by when additional information becomes decision-relevant.** P0 requires no state beyond the linguistic predictive reference for the registered responsibility process. P1 requires additional cross-channel state for the current decision but no future-only refinement. P2 requires additional state solely or additionally for later evidence-triggered revision. Missing initial evidence is a pre-phase acquisition problem rather than P1/P2.

### Prohibition

Do not label axes “intelligence,” “understanding,” “epistemic quality,” or “trust.”

---

## Figure 3 — Prospective Revision Audit flow

### Scientific question

What must be controlled before a revision failure can be attributed to representation loss?

### Flow

```text
REGISTER responsibility + future evidence process
        |
        v
PRESENT-EQUIVALENCE GATE
(language target + current action/risk + resources matched)
        |
        v
REPRESENTATION INTERVENTION / STATE COMPARISON
        |
        v
ALTERNATE-CHANNEL RETENTION GATE
(context / KV / hidden / summary / retrieval / tool / external memory)
        |
   +----+-------------------------+
   | removal supported           | information remains / cannot check
   v                             v
COMMON LATER EVIDENCE       NO STRONG P2 ATTRIBUTION
   |
   v
SCORE UPDATE + MAINTAIN / SELECTIVE REOPENING
   |
   v
P0 / P1 / P2 / ACQUISITION / RECONSTRUCTED / CANNOT_CHECK
```

### Caption

> **Prospective Revision Audit.** Future revision is tested only after present language/current-decision equivalence is established. A representation intervention must then survive an alternate-channel retention check; visible deletion alone is insufficient. Both correct updating and correct maintaining/selective reopening are scored after the same later evidence. The protocol can return P0/P1/P2 classifications as well as acquisition, reconstruction, no-mechanism, and `CANNOT_CHECK` terminals.

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

Never turn CANNOT_CHECK into PASS.

---

## Optional Figure 4 — horizon curves

Only include if generated receipt curves are genuinely informative visually.

Scientific message:

`C_k^*` is monotone and can stabilize after different horizons across registered finite fixtures.

Do not imply empirical LLM memory depth.

If curves are visually trivial, use a compact table or omit the figure.

---

# Figure priority under page pressure

1. Figure 1 — one-bit witness: **mandatory**.
2. Figure 3 — audit flow: **strongly preferred**.
3. Table 1 — parent ownership: **strongly preferred**.
4. Table 2 — direct neighbors: **strongly preferred**.
5. Figure 2 — phase plane: useful but removable if text/table suffices.
6. Table 3 — mechanical validation: can move to appendix if main is crowded.
7. Figure 4 — optional.

No decorative figure is authorized.

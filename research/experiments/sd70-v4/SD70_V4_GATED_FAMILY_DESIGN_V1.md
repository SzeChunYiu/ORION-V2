# SD70-V4 — recursive meta-discovery on a family the linear multiclass class provably does not contain (frozen design V1)

**Revival backlog:** #308 row **R12** (SD70-V3 `PARENT_SUFFICIENT`, Δ = −0.0083, n = 240). **Attributed stage (one):** *problem class* —
V3's generator is a linear multiclass argmax and the max-margin parent's hypothesis class contains it ("optimal by construction",
V3 §1); F2_STATIC ties the parent exactly, recursion discovers nothing because nothing lies outside the parent's class. **Lever:** change
the generator family, not the arm. **Identity:** SD70-V4, new seeds, new authorization; V3's files imported read-only and sha256-pinned.
**Frozen:** 2026-09-05 before the development study runs. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

## 1. The family and its non-containment, as a checkable property

`sd70v4_generator.build_suite`: V3's dimensions (4–7 binary features, 3–5 actions, integer weights in [−3, 4], distinct rows, 8 unseen
training contexts × SUCCESS/FAILURE pairs, one unseen query, codeword tokens) with **two** weight matrices `W0, W1` and a hidden gate pair
`(i, j)`: `best(x) = argmax_a W_{x_i ⊕ x_j}[a]·x`, lowest index on ties. A task is accepted only if its full labelling over the nonzero
contexts carries at least one **aabb XOR square** — four contexts agreeing outside `{p, q}`, labels `a, b, b, a` with `a ≠ b`.
`sd70v4_containment.py` states and proves the theorem: no linear multiclass argmax (any weights, any bias, the frozen tie rule)
realises a labelling containing such a square. Non-containment is therefore **verified per task**, never assumed; a zero count proves
nothing (recorded). No-alarm control: V3's linear family run through the same code path yields zero certificates on every task
(selftest, 40 + 40 tasks); planted checker mutant `mutant_ignore_labels` fires on linear tasks and is caught.

## 2. Parents and comparator (pre-registered)

V3's seven parents and `F0_PARENT_FEDERATION` unchanged. Added, generator-faithful for the new family:
`GATED_MAXMARGIN_PARENT` — knows the family *form* (two linear regimes gated by the XOR of two context bits), not the gate or weights;
for every vocabulary pair it fits V3's max-margin parent per regime, selects the pair by training consistency then summed SUCCESS
margin, and predicts the query in the selected regime. `F0_PLUS_FEDERATION` = plurality over eight parents, ties → strongest.
**Comparator rule (V3 §4.1 extended):** `max(strongest generator-faithful parent incl. GATED, F0_PLUS, F0)` by mean development
exact accuracy on 3 × 200 fresh public dev tasks (`sha256("SD70-V4-DEV|k")`), frozen before any protected task exists.
Selection rule for the strongest faithful parent: highest mean dev accuracy among V3's candidates + GATED; tie → lower wall time.

## 3. Pre-registered expectations for the development parent-ceiling study (exact, runnable now)

(a) Every task carries ≥ 1 certificate (rejection count published). (b) The linear parents sit **below** their V3 dev accuracies
(V3: MAXMARGIN 0.678) — the family is outside their class. (c) `GATED_MAXMARGIN_PARENT` beats the strongest linear parent (paired
bootstrap CI excluding zero); if it does not, the *information* budget (16 episodes) rather than the hypothesis class binds and the
design records `PARENT_CEILING_INFORMATION_BOUND`. (d) `F0_PLUS` ≥ `F0`. (e) Label-permutation and query-shuffle controls at chance
for every parent. The comparator to beat for any model arm is whatever (c)/(d) select; it is frozen in the design JSON by the dev
results digest.

## 4. Model arms (channel-dependent; frozen here, dispatched later)

V3's model arms (`F2_RECURSIVE_META_DISCOVERY_FULL`, `F2_STATIC`, the ablations `no_recursion`, `no_parent_federation`,
`no_failure_evidence`, target-only) reuse `sd70v3_model_arm.py` / `sd70v3_channel.py` **unchanged** on V4 surfaces (identical
surface schema), with V3's channel contract (`gpt-5.5`, reasoning medium, canary bands) measured twice. Required gates carried
over verbatim from V3 §10, plus the **mechanism gate**: `acc(F2) − acc(F2_STATIC) ≥ 0.05` before any residual is claimed.
Power: V3's n = 240 (CI half-width ±0.04) is retained. The protected seed is committed below; the model-arm dispatch needs its own
authorization at the channel window (~2026-09-07 codex / ~09-09 z.ai) and is staged on billy-old under the R12 row.

## 5. Custody

Master seed `~/.orion-custody/sd70-v4/SD70_V4_MASTER_SEED.txt` (Mac, mode 600), sha256 in the JSON; development seeds disjoint by
construction. Interpreter registered for the exact legs: LUNARC `.venv` CPython 3.13.5 (§13 of V3: parent numerics are
interpreter-sensitive at ≈0.17 % of tasks; byte-identical re-run is claimed only under this interpreter).

## 6. Authority

Grants nothing; V3's verdict stands. What this design can earn: a parent ceiling on a certified non-linear family, and — only after
the model arms run under the frozen gates — a residual measured against the strongest faithful parent of *that* family.

skills-applied: none (frozen design, no manuscript content)

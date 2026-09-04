# H-EXT-1 Outcome Receipt — Conditional Activation with Channel-External Witnesses

**Executed:** 2026-09-02. Design frozen (`H_EXT1_CONDITIONAL_ACTIVATION_DESIGN_V1.json`,
sha256 `08d952828643731a…`) before any gated evaluation; gate frozen on the development
split (`H_EXT1_GATE_FREEZE.json`, gate `G_B_PLUS_XREF`, gate sha `81ce16e2d327f630…`,
dev n=276) before either evaluation cell was scored. Runner
`scripts/h_ext1_gate_study.py`; unit tests `tests/unit/test_h_ext1_gate_study.py`
(planted-gate fixture passes G1–G3, null fixture does not, missing prospective responses
route to `CANNOT_CHECK`). Re-running the full pipeline reproduced the committed freeze
and retrospective cell byte-for-byte.

## Binding terminal (PROSPECTIVE cell)

```text
H_EXT1_TERMINAL = CONDITIONAL_ACTIVATION_IDENTIFIABLE_FROM_EVIDENCE_STRUCTURE
CELL = PROSPECTIVE (fresh seed 20260902, gpt-5.5, 520 tasks x 3 arms, 1560/1560 responses, 0 failures)
RETROSPECTIVE_EVAL agrees (same terminal on the held-out half of the frozen 2026-08-30 run)
```

## What the gate is

`G_B_PLUS_XREF` activates the dependence machinery iff the evidence records the arm sees
contain (a) two records with the same `replay_hash`, or (b) two records with the same
`lineage_root`, or (c) a record whose `method_text` names another record's `lineage_root`.
It reads nothing else: no study label, no oracle stratum, no arm output (canary-asserted on
every task). On the development split it tied with `G_C_PLUS_DECLARED` and
`G_E_COUNT_GE4` (dev advantage +0.029, 98 activations each) and won on family order;
`G_A_PROVENANCE_WITNESS` and `G_F_ROOT_RATIO_GT1` were negative (−0.033) because they miss
the latent-convention stratum PDS1A; `G_D_PLUS_SHARED_TOKEN` over-fired into PD-S2
(+0.025).

## Prospective cell, gate by gate (n=520, activations 170 = 32.7%)

| Gate | Result | Numbers |
|---|---|---|
| G0 validity | pass | seeds disjoint from the frozen run; canary clean; all arms `run_valid`; 0 missing |
| G1 vs always-on M | pass | GATED **0.9769** (508/520) vs `P_D_FULL` 0.8942 (465); calls 520 = 520; mean wall 9.57 s vs 10.42 s |
| G2 vs always-off / parent | pass | vs `P_D_MINUS_DEPENDENCE` 0.8231 (428); vs `STRONGEST_ASSURANCE_FEDERATION` 0.9558 (497) |
| G3 pooled shuffle-equal-n null | pass | advantage **+0.0827** vs null q95 −0.0308 (mean −0.0477, max −0.0096 over 2000 draws; exceedance 0/2000) |
| G3S within-study equal-n null | pass | null q95 −0.0115 (mean −0.0290, max +0.0077; exceedance 0/2000) |
| G4 sign consistency | pass | S1 1.000 ≥ max(0.775, 0.500); S2 0.900 = OFF 0.900 ≥ M 0.842; S3 1.0 = 1.0; S4 1.0 = 1.0 |

Per oracle stratum (reporting only, never seen by the gate): the gate fired on **all 80**
PDS1A/PDS1C tasks and on **none** of PDS1B/PDS1D/PD-S2/PD-S4; GATED = the oracle-stratum
ceiling (0.9769) exactly. The 12 residual misses are PD-S2 C/D tasks where both `M` and
`OFF` fail on gpt-5.5 — not gate errors.

## Retrospective cell (secondary; held-out half of the frozen gpt-5.6-terra run, n=244)

GATED 1.000 (244/244) vs M 0.9836, OFF 0.8361, PARENT 0.9754; advantage +0.0164 vs pooled
null max −0.0656 and within-study null max −0.0287 (2000 draws each, exceedance 0). All
gates pass; same terminal.

## Honest reading

> **Claim-integrity correction, 2026-09-03.** Item 1 previously read "beating the
> strongest parent by +2.1 pp pooled and the always-on arm by +8.3 pp", coordinating a
> null-tested margin and a threshold-only margin in one clause. Items 1-3 below restate
> the same frozen numbers with each margin attached to the contrast that actually
> supports it. **No gate value, null, terminal or datum changed**; nothing was
> recomputed and no new test was run. The design registered G2 as a threshold, so this
> is a correction to this receipt's prose, not a registered clause that went unexecuted.

1. **Positive, and it transferred across substrates.** The gate was selected on
   gpt-5.6-terra outcomes and evaluated prospectively on gpt-5.5, where always-on `M` is
   much weaker (PDS1D 5/40, PDS2D 17/30) and the drag is therefore larger. Routing by
   evidence structure alone recovered the full A/C gain and removed the whole B/D/S2/S4
   drag: GATED 508/520 against always-on `M` 465/520 (**+8.3 pp**) and against the
   strongest parent 497/520 (**+2.1 pp**). The two margins do not carry the same
   evidential weight — item 2.

2. **What the registered nulls tested, and what they did not.** G3 and G3S test exactly
   one quantity: `advantage = acc(GATED_M) − max(acc(M), acc(OFF))` = **+0.0827**, i.e.
   the gated-versus-always-on-`M` contrast (`max` is `M` here), against 2000 equal-n draws
   in each null, exceedance 0/2000 in both. The parent comparison is **G2, registered as a
   threshold** — `acc(GATED_M) ≥ acc(PARENT)` (design §6) — and the frozen G2 record
   carries `pass_vs_PARENT` and the two accuracies and nothing else: no null, no p-value,
   no interval, because none was registered. The **+2.1 pp** margin over
   `STRONGEST_ASSURANCE_FEDERATION` is therefore a registered threshold comparison decided
   by 11 tasks (508 vs 497) and carries no significance claim; the design's own wording is
   that `GATED_M` "matches the strongest parent" (§1). A reader must not borrow G3's
   authority for it. Attaching uncertainty to the parent margin would require a new
   registered study, not a post-hoc null on this frozen outcome (no-rescue clause, §8).
   Such a study is named here and **not started**: `H-EXT-1P`, a fresh-seed prospective
   cell pre-registering a paired null on `acc(GATED_M) − acc(PARENT)` with its own
   freeze, gates and routed terminals.

   > **Addendum, 2026-09-04 — the parent margin decomposed, extending item 4 below.**
   > `H-EXT-1P` was subsequently registered and **closed pre-freeze**, terminal
   > `REGISTERED_CONTRAST_CANNOT_BE_ABOUT_THE_MECHANISM`, on the estimand and **not** on
   > power (exact McNemar power 0.4605 at n = 520, ≥ 0.80 at n = 1040; task supply is
   > unbounded, so a larger run was feasible and would have been misleading). Splitting the
   > frozen PROSPECTIVE cell by whether `G_B_PLUS_XREF` actually fires: on the **170
   > gate-active tasks `GATED_M` and `PARENT` are both 170/170 and never differ — zero
   > discordant pairs.** All 29 discordant pairs, and the whole +11-task margin, lie on the
   > 350 gate-inactive tasks (b = 20, c = 9), where `GATED_M` **is** `P_D_MINUS_DEPENDENCE`
   > by construction; 28 of the 29 are `PD-S2`, a family the gate never activates on once.
   > The retrospective run replicates it: over the whole run (`RETROSPECTIVE`, n = 520,
   > dev+eval) gate-active b = 0, c = 1 and gate-inactive b = 7, c = 0; on the genuinely
   > held-out `RETROSPECTIVE_EVAL` cell (n = 244) it is cleaner — gate-active 72/72 vs
   > 72/72, **b = 0, c = 0**; gate-inactive 172: 172 vs 166, b = 6, c = 0. (An earlier
   > revision of this addendum labelled the n = 520 figures as the eval cell; the single
   > gate-active task `GATED_M` loses, `pd-s1-0137`, is in the dev half.)
   > So the caution in this item strengthens: the +2.1 pp margin is not merely un-null-tested,
   > it is **composed entirely of tasks where the mechanism's gate never fired**, and cannot
   > be read as evidence about conditional activation whatever a null on it returned.
   >
   > **This changes nothing in H-EXT-1 and is not a correction to it.** It *extends* item 4's
   > own ceiling disclosure from 90 activations to all 170, and it is the same caution item 2
   > already registered, measured rather than warned about. No gate value, null, terminal or
   > datum moves; the binding terminal still rests on G1/G3 against always-on `M`
   > (`GATED_M` 508 vs `M` 465, advantage +0.0827, exceedance 0/2000 in both nulls), a
   > contrast this decomposition does not touch. The successor stays closed: no successor may
   > freeze until a suite is shown on which the strongest parent is **off ceiling on the
   > gate-active regime**, and none is claimed to exist.
   > Receipt: `research/experiments/h-ext1p/H_EXT1P_REGISTRATION_AND_PRE_FREEZE_CLOSURE_V1.md`.

3. **Always-on `M` does not beat the parent in the binding cell.** In PROSPECTIVE,
   `P_D_FULL` 0.8942 (465/520) is **below** `STRONGEST_ASSURANCE_FEDERATION` 0.9558
   (497/520) — −6.2 pp, 32 tasks. What clears the parent here is the conditional-activation
   gate over `M`, not `M` itself. (In the secondary RETROSPECTIVE_EVAL cell the sign
   reverses — `M` 0.9836 vs PARENT 0.9754, 2 tasks — but PROSPECTIVE is the binding cell.)

4. **Imprecision that costs nothing here but is real.** 90 of the 170 prospective
   activations are PD-S3 revocation tasks (their planted Family-B shares a `lineage_root`);
   all three arms are at ceiling there, so the activations are harmless in this suite. A
   suite where the machinery had a cost on such tasks would expose this. Precision of
   activation against the oracle-active strata is 80/170.
5. **Suite-internal identifiability only.** Dependence is planted; the witnesses that
   separate these strata (duplicate hashes, shared roots, a method text naming another
   record's root) need not exist or separate anything in real corpora. This grants no
   real-corpus dependence-detection claim.
6. **PD-S2 is not rescued by gating** (0.900 = OFF): the gate correctly stays off, but the
   residual error there belongs to both arms on this substrate, not to activation policy.
7. The PDS1 `study_id` metadata gate would have scored only 0.9077 prospectively (it
   activates on B/D where `M` is weak on gpt-5.5); the evidence-structure gate is strictly
   finer than task metadata, which is what H-EXT-1 asked.

Against the register's negative terminal `ACTIVATION_POLICY_NOT_IDENTIFIABLE_FROM_INPUTS`:
not reached. The activation policy is identifiable from arm-visible evidence structure in
this suite, prospectively, above both nulls.

## Custody

- Prospective campaign receipts (freeze manifest with harness/arm hashes identical to
  `origin/main`, dispatch receipt with `all_oracles_restored: true`, evaluation and
  analysis summaries): `prospective-campaign-receipts/`. Full workdir:
  `billy-old:/home/billy/hext1-prospective` (8 MB pulled for the three arms).
- Per-instance tables: `data/RETROSPECTIVE_instances.json`, `data/PROSPECTIVE_instances.json`.
- Rollup: `H_EXT1_ROLLUP_V1.{json,md}`.

```text
GRANTS_SCIENTIFIC_TRUTH = false
GRANTS_FIELD_STATUS = false
GRANTS_REAL_CORPUS_DEPENDENCE_DETECTION = false
GRANTS_MANUSCRIPT_CHANGE = false
```

skills-applied: none (receipt, no manuscript content)

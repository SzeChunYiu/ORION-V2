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

1. **Positive, and it transferred across substrates.** The gate was selected on
   gpt-5.6-terra outcomes and evaluated prospectively on gpt-5.5, where always-on `M` is
   much weaker (PDS1D 5/40, PDS2D 17/30) and the drag is therefore larger. Routing by
   evidence structure alone recovered the full A/C gain and removed the whole B/D/S2/S4
   drag, beating the strongest parent by +2.1 pp pooled and the always-on arm by +8.3 pp.
2. **Imprecision that costs nothing here but is real.** 90 of the 170 prospective
   activations are PD-S3 revocation tasks (their planted Family-B shares a `lineage_root`);
   all three arms are at ceiling there, so the activations are harmless in this suite. A
   suite where the machinery had a cost on such tasks would expose this. Precision of
   activation against the oracle-active strata is 80/170.
3. **Suite-internal identifiability only.** Dependence is planted; the witnesses that
   separate these strata (duplicate hashes, shared roots, a method text naming another
   record's root) need not exist or separate anything in real corpora. This grants no
   real-corpus dependence-detection claim.
4. **PD-S2 is not rescued by gating** (0.900 = OFF): the gate correctly stays off, but the
   residual error there belongs to both arms on this substrate, not to activation policy.
5. The PDS1 `study_id` metadata gate would have scored only 0.9077 prospectively (it
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

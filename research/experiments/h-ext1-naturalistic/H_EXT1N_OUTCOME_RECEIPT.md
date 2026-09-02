# H-EXT-1N Outcome Receipt — Naturalistic Replication of the Conditional-Activation Gate

**Executed:** 2026-09-02 on **billy-old** (corpus fetch/build and every model call; LUNARC not
used). Model **gpt-5.5** via `codex exec --ephemeral`, codex-cli 0.129.0-alpha.15, read-only
sandbox, one call per instance per arm — the same substrate as the H-EXT-1 prospective cell.
Design frozen before any dispatch (`H_EXT1N_DESIGN_V1.{md,json}`, sha256
`b8c3847925f9d6ae…`); corpus frozen before dispatch (`H_EXT1N_CORPUS_FREEZE.json`, sha256
`6b70fe410c0387b7…`); gate selection run on the development split only.

## Binding terminal

```text
H_EXT1N_TERMINAL = NO_CANDIDATE_GATE_ON_DEV
CELL = N1-DEV (80 sets, 240/240 responses, 0 failures)
CONSEQUENCE (pre-registered) = the evaluation split is NOT scored under the gate identity
```

No candidate gate reached `dev_advantage > 0`, so by §5 of the frozen design nothing was
gated and the H-EXT-1 positive terminal `CONDITIONAL_ACTIVATION_IDENTIFIABLE_…` was never
reachable. The negative terminal `ACTIVATION_POLICY_NOT_IDENTIFIABLE_IN_NATURALISTIC_RECORDS`
was **not** reached either: it is routed by G3 in the evaluation split, which the design
forbids scoring once development terminates.

## Why gating cannot help here (development diagnostics, n=80, not binding)

| Oracle stratum | n | `P_D_FULL` | `P_D_MINUS_DEPENDENCE` | `STRONGEST_ASSURANCE_FEDERATION` |
|---|---|---|---|---|
| NS1A (3 records, 2 share a trial) | 20 | 19 | 5 | 19 |
| NS1B (3 independent trials) | 20 | 19 | 20 | 19 |
| NS1C (4 records, two shared pairs) | 20 | 18 | 7 | 18 |
| NS1D (4 independent trials) | 20 | 20 | 20 | 19 |
| **pooled** | **80** | **0.950** | **0.650** | **0.9375** |

The always-on arm is at 0.95 in *every* stratum. `max(acc(M), acc(OFF)) = acc(M)`, and OFF is
better than M on exactly one of 80 sets, so no routing function can gain: the best candidate,
`G_F_ROOT_RATIO_GT1`, ties at `dev_advantage = 0.000` (it routes 35 sets to OFF, of which M
and OFF are both correct on 34). Candidate advantages: `G_F` 0.000, `G_D` −0.013, `G_B`/`G_C`
−0.025, `G_A` −0.075, `G_E` −0.162.

**This is a structural difference from H-EXT-1, not a weak-witness result.** H-EXT-1's +8.3 pp
came from a drag regime — PD-S2/PD-S4 strata where the dependence machinery *hurt*. This
corpus has no drag regime: dependence-aware evaluation is at least as good as the ablation
everywhere. The witnesses themselves are highly informative (measured on the held-out split
below: `G_F` precision 0.885 / recall 0.963 against the oracle strata). What is missing is
something for a gate to buy.

## Secondary cell (separate identity, frozen before the evaluation split was dispatched)

`H_EXT1N_SECONDARY_CELL_FREEZE_V1.json` (sha256 `0a9dace31ce97ecb…`, committed in
`fff5123` before dispatch) asks a different pre-registered question of the 160 held-out sets:
can the dependence structure be recovered from naturalistic records at all, is independence
preserved, and does the strongest parent suffice? It selects, scores and reports **no gate**.

```text
H_EXT1N_SECONDARY_TERMINAL = DEPENDENCE_STRUCTURE_RECOVERABLE_FROM_NATURALISTIC_RECORDS
PARENT_AXIS_TERMINAL       = STRONGEST_PARENT_SUFFICIENT_ON_NATURALISTIC_RECORDS
CELL = N1-EVAL (160 sets, 480/480 responses, 0 failures, oracle restored hash-matched)
```

| Endpoint (frozen) | Threshold | Result |
|---|---|---|
| A detection: `acc(M)` on NS1A+NS1C | ≥ 0.80 and McNemar p < 0.01 | **0.900** (72/80); M-only correct 41, OFF-only 0, exact p = 9.1×10⁻¹³ — **pass** |
| B preservation: `acc(M)` on NS1B+NS1D | ≥ 0.90 | **1.000** (80/80) — **pass** |
| C parent: paired M vs PARENT (n=160) | routed by exact McNemar | M 152 vs PARENT **153**; discordance 0/1; p = 1.000 → **parent sufficient** |

Pooled: `P_D_FULL` 0.950, `P_D_MINUS_DEPENDENCE` 0.694, `STRONGEST_ASSURANCE_FEDERATION`
0.956. Per stratum: NS1A 38/40 M vs 18/40 OFF; NS1C 34/40 vs 13/40; NS1B and NS1D 40/40 for
both. Family-count errors: M over-counts by one on 8 of 160 sets; OFF over-counts by one on
27 and by two on 22 — exactly the shape of the planted dependence it is instructed to ignore.

Witness informativeness on the held-out split (reporting only, never routed on):

| Gate | activations (of 160) | precision vs NS1A/NS1C | recall |
|---|---|---|---|
| `G_A_PROVENANCE_WITNESS` (shared grant id ∨ shared senior author) | 55 | 0.982 | 0.675 |
| `G_B_PLUS_XREF` (+ title acronym cross-reference) | 80 | 0.875 | 0.875 |
| `G_C_PLUS_DECLARED` | 132 | 0.576 | 0.950 |
| `G_D_PLUS_SHARED_TOKEN` | 146 | 0.534 | 0.975 |
| `G_E_COUNT_GE4` | 80 | 0.500 | 0.500 |
| `G_F_ROOT_RATIO_GT1` (author-link components < records) | 87 | 0.885 | 0.963 |

## Honest reading

1. **The H-EXT-1 gate result does not replicate, and the reason is that its precondition is
   absent.** Conditional activation pays only where the mechanism has a cost somewhere. On
   these records it has none, so the honest conclusion is that H-EXT-1's Pareto gain is a
   property of a suite containing machinery-hostile strata, not a transferable routing law.
2. **Dependence structure is recoverable from real records** at 0.90 on the dependent strata
   with perfect preservation (80/80) on the independent ones — the arm reads shared trial
   identity out of redacted titles, abstracts, authors and grant ids, with the registration id
   removed everywhere and canary-asserted. This is the first naturalistic evidence on the
   question the P-D manuscript explicitly disclaims; it is one model family on one corpus.
3. **The strongest parent ties (indeed edges) the dependence-aware arm on this corpus**
   (153 vs 152, discordance 0/1, p = 1.000). Under the P-D kill/merge contract this is the
   parent-sufficiency signal, and it is a genuine negative for P-D's distinctive claim in the
   naturalistic regime. Note the parent arm's instruction already includes a dependence graph
   over declared correlations, so this says the *extra* latent-dependence machinery adds
   nothing measurable here — not that dependence reasoning is unnecessary (the ablation loses
   25.6 pp).
4. **The M-vs-OFF gap is near-tautological by arm construction** (OFF is instructed to treat
   every record as independent, and the oracle counts shared-registration records as one
   family). It is reported for continuity with the P-D ablation; the informative quantities
   are M's detection and preservation rates and the parent tie.
5. **Oracle noise cuts against endpoint B, not for it:** separately registered extensions of
   one programme are labelled independent, so the perfect 80/80 preservation was achieved
   despite an oracle that would score a correct dependence call as an error.
6. Selection: every record comes from a trial with ≥ 2 indexed publications, which favours
   larger, named trials whose acronyms make the cross-reference witness easy. A random
   literature sample would be harder.

## Custody

- Corpus: `H_EXT1N_CORPUS_FREEZE.json` — 240 sets, 120/120 balanced, 10 topics, per-record and
  per-corpus sha256, all 840 PMIDs (840 unique records), 64 per-page fetch hashes. Raw XML cache and full record texts
  remain on `billy-old:/home/billy/hext1n/` (abstract copyright); every record is re-fetchable
  from its committed PMID.
- Eligibility from 9 462 fetched records: 8 321 eligible (510 not exactly one NCT, 440 duplicate
  PMID across topics, 160 other registry, 19 excluded publication type, 12 short abstract).
- Gate freeze: `H_EXT1N_GATE_FREEZE.json` (`selected_gate: null`, dev n=80, dev-id sha256
  `03b3201e771e2d2d…`). Rollup: `H_EXT1N_ROLLUP_V1.{json,md}`. Secondary result:
  `H_EXT1N_SECONDARY_CELL_RESULT.json`. Per-instance tables and dispatch/evaluation receipts:
  `data/`.
- Three build-canary catches are part of the record: registry ids glued to the preceding word
  (`identifierNCT00445770`), NCT ids inside `GrantList` entries, and 7- and 9-digit registry-id
  typos in live abstracts. Each aborted the build; the corpus was rebuilt after each fix, and
  the committed corpus greps clean for registry-shaped tokens.

```text
GRANTS_SCIENTIFIC_TRUTH = false
GRANTS_FIELD_STATUS = false
GRANTS_GENERAL_DEPENDENCE_DETECTOR = false
GRANTS_MANUSCRIPT_CHANGE = false
```

skills-applied: none (receipt, no manuscript content)

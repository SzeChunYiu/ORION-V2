# SD20 Scale-Up Receipt V1 — 45k-Parent arXiv Version-Transition Chain (Powered Re-Run)

**Lane:** SD20 (#50) · **Supersedes:** bounded-pilot + revival results in `../` (population, not verdicts)
**Executed:** 2026-08-29/30 on billy-old (`~/sd10run/sd20_scaleup_sharded.sh`, r13) + variant completion 2026-08-30.

## 1. Chain

- **45,000 parents** sharded 4×11,250 → earlier-versions fetch (K=4 concurrent, 4 s rate)
  → **31,070 version observations** (4 shard receipts, merge `duplicate_observation_dropped: 0`)
  + **19,961 head rows**; **19,961 multi-version trajectories** (25,039 single-version censored),
  **31,070 transitions**, trajectory-level split 21,595 train / 9,475 test.
- r12's version-shard phase FAILED (4/4 shards, fetch-stage) → r13 re-ran the full fetch cleanly
  and superseded it entirely; r13 merge kept 31,070 rows with zero duplicate drops.
- Design power target: MDE 0.05 → ~0.017 nats. Realized bootstrap CI half-widths
  ~0.003–0.007 — **power exceeded design**.

## 2. Powered re-run — TEMPORAL_SEQUENCE_MODEL_PARENT vs SIMPLE_FREQUENCY_BASELINE
(held-out transition prediction, mean log-score Δ, bootstrap 95% CI; same population/split for every variant)

| Variant (alphabet/context) | Δ vs baseline | 95% CI | CI excludes 0 |
|---|---|---|---|
| default / default | **+0.0032** | [−0.0018, +0.0078] | No |
| coarse9 / default | **+0.0068** | [+0.0032, +0.0099] | **Yes (+)** |
| fine81 / default | **−0.0403** | [−0.0470, −0.0340] | **Yes (−)** |
| default / category | **+0.0116** | [+0.0070, +0.0161] | **Yes (+)** |
| coarse9 / category | **+0.0099** | [+0.0068, +0.0131] | **Yes (+)** |

Reference baselines (mean log-score): default −2.1646, coarse9 −1.2048.

Other arms (default alphabet): all three FIXED_META_LESSON_INJECTION variants and
F0_META_PARENT_FEDERATION are significantly **harmful** (Δ −0.66 to −1.04, CIs exclude 0).
CANNOT_CHECK_ON_SLICE arms unchanged from the bounded pilot (no citation/fame fields, no
author network, no interventions, recursion needs SD50).

## 3. Verdict (operator's own classification, unchanged)

**BOUNDED_PILOT_INTERIM__NO_TERMINAL_CLAIM** — in every variant.

- **Powered micro-signal, real:** the temporal-sequence parent's transition-operator lift is
  positive and CI-significant on the repaired alphabets and under category conditioning
  (+0.007…+0.012 nats), and the default alphabet null (+0.0032) is now *powered* (CI excludes
  the 0.017-nat MDE band), i.e. a genuine null at that resolution, not an underpowered one.
- **The signal does not localize:** LOO cross-domain support beats baseline in **0/20 categories**
  in every variant — the aggregate lift is a uniform micro-effect, with no category-level
  heterogeneity legible in this corpus.
- **fine81 overfits at scale** (−0.040): the finer operator alphabet's bounded-pilot promise does
  not survive the powered population.
- **All fixed "lessons" injure prediction** — injecting editorial heuristics as fixed operators
  is worse than frequency alone; the F0-style federation of them inherits the damage.

## 4. Honest scope

Version-transition structure in public arXiv Atom metadata is weakly predictable
(~0.5% of baseline log-score) from trajectory + category statistics; nothing here supports a
structural-discovery claim, a causal claim, or any transfer license (`authority.*` all false).
Outcome-censoring statement and CANNOT_CHECK ledger carry over verbatim from the bounded pilot.

## 5. Artifacts (this directory; sha256)

- `sd20x_default.json` `0a6252c8…` · `sd20x_coarse9.json` `90da75f9…` · `sd20x_fine81.json` `3340c9ac…`
  · `sd20x_default_category.json` `0e8f8820…` · `sd20x_coarse9_category.json` `1794384d…`
- Fetch receipts: `arxiv_version_receipt.json` `0852b403…`, `arxiv_head_receipt.json` `b049e013…`
- Raw observations remain on billy-old (`~/sd10run/ORION-V2/out_scale/sd20/`), referenced by the
  receipts' sha256 ledger — not committed (16 MB + 6 MB jsonl).

skills-applied: none (receipt, no manuscript content)

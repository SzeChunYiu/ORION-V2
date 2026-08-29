# SD30 Witness Source Candidate V1 — MLRC JOURNAL-TRACK PROSE VERDICTS (2026-08-29)

Schema: `orion.v2.sd30-witness-source-candidate.v1` · Classification:
**`WITNESS_SOURCE_CANDIDATE__MLRC_PRICED__NOT_INGESTED`**

Second witness-source pricing after
`SD30_WITNESS_SOURCE_CANDIDATE_RPP_V1.md` (the C2 lever). This prices a
**ladder-bearing** candidate — an independent reproduction attempt with a
self-reported prose verdict — the MLRC (Machine Learning Reproducibility
Challenge) Journal Track. It is reconnaissance with real counts, NOT an
ingestion: no binding pass, no outcome-policy change, no new corpus.

It also delivers the first measured evidence for the **C4 identity-linkage
lever** (doi ↔ arxiv_id ↔ openreview ↔ pmid, `SD30_STRUCTURAL_PILOT_RECEIPT_V1.md`
§levers): 24/30 title-resolvable reproduction targets were linked into arXiv id
space by metadata-only resolution with per-query raw evidence.

## 1. Source and provenance (lawful, public)

| Item | Value |
|---|---|
| Project | MLRC Journal Track (Pineau et al.), reports published in TMLR via OpenReview group `reproml.org/MLRC/2025/Journal_Track` (17) + `2023/Journal_Track` (22) |
| Data | 39 forum pages (`openreview.net/forum?id=<id>`) fetched 2026-08-29, distilled to 39 rows; resolution via public arXiv export API + Semantic Scholar Graph API (unauthenticated) |
| Access | public HTML/API, no auth, no terms-gated bulk; group listings + 39 forum fetches + 30+12 arXiv queries + 30 S2 queries |
| Integrity | every resolved id points to its saved raw response (`arxiv_evidence_raw_file`, relative to `mlrc_raw/`); all raw responses under `research/experiments/results/issue50/sd30/mlrc_raw/` |
| Lawful-source class | public journal/forum metadata (same class as the Crossref/OpenAlex/arXiv adapters) |

## 2. Witness class: INDEPENDENT_PROSE_REPRODUCTION_VERDICT (weaker than C2)

An independent team reproduces a specific published original and states a
verdict **in abstract prose**, self-reported, without a structured verdict
field or a priori per-claim criteria. This is strictly weaker than RP:P's
REGISTERED_REPLICATION_VERDICT (prospective, a priori criteria, coded field).

Verdict-field semantics (verified per row, `note_fields_non_verdict`):
- `Event Certifications: reproml.org/<cycle>/Journal_Track` — participation marker.
- `Certifications: Reproducibility Certification` — process marker; appears on
  negative-verdict reports too (nPZgtpfgIx, BbvSU02jLg), so it carries **zero**
  verdict information.
- MLRC 2025 medals — prize metric, excluded as truth label
  (`citation_or_prize_metric_is_truth_label=false`).

The only verdict truth source is the abstract prose; bins are
analyst-assigned (PROSE_DERIVED), declared in `verdict_class_analyst` +
`verdict_prose_extract` per row.

## 3. Counts (verified 2026-08-29, reproduce in §6)

| Quantity | Value |
|---|---|
| Reports total | 39 (17 MLRC 2025 + 22 MLRC 2023; TMLR online 2025/02-03 and 2024/02-03) |
| Extractable prose verdict | 36 |
| Not applicable / not extractable | 3 (2 no single named original; TYYApLzjaQ names original, states no verdict) |
| Verdict bins (analyst) | FULL 19 / PARTIAL 12 / NO 5 |
| Distinct reproduction targets | 31 (30 title-resolvable) |
| Targets resolved to arXiv id | 24 (18 exact-title, 6 title-variant/author/concept, each labelled with match type + raw file) |
| Targets not found on arXiv | 6 (moderntcn, gnnboundary, tgnn_explainer, slice, graphair, scoreable_games' original) |
| Originals with two independent witnesses | 6; coarse-bin disagreement on exactly 3 of 6 |
| Cross-resolver (S2 vs arXiv API) | 6 valid S2 responses, all agree, 0 conflicts (S2 pool throttled 429 on 24/30 across 3 passes) |

Rebinning note: FULL includes `partial_positive` and
`positive_core_negative_generalization` (negative parts concern secondary
claims or the reproducers' own extensions); rebinning is a declared one-line
change in `mlrc_raw/scripts/build_inventory.py`.

## 4. Lawfulness assessment: PARTIAL

A lawful witness needs (a) extractable verdict, (b) defined truth label,
(c) identifiable originals, (d) independent witnesses, (e) no
conflict-of-interest. MLRC: (a) weakly — prose-only, 2 reports state no
verdict; (b) **no** — self-reported prose, analyst-binned, per-claim criteria
not a priori (identical outcomes phrased "generally support the core"
fCNqD2IuoD vs "despite notable discrepancies" nPZgtpfgIx, same original);
(c) yes; (d) yes — demonstrated: 6 doubly-witnessed originals with honest
dispersion (3/6 disagree at coarse bin); (e) partially — original-author
interaction not observable in saved note fields.

Net: usable as **noisy, analyst-binned witness testimony** with bin label +
prose extract carried by any consumer; NOT a ground-truth label set. The 6
doubly-witnessed originals are the premium subset (inter-witness agreement
measurable). Compared with RP:P (prospective, coded, a priori): MLRC is the
weaker rung of the ladder; both are `NOT_INGESTED`.

## 5. Consequences for the levers

- **C2 (witness source):** second candidate priced. RP:P remains the stronger
  candidate (coded verdict, a priori criteria); MLRC adds domain breadth
  (ML originals, arXiv-adjacent) at the cost of prose-only verdicts.
- **C4 (identity linkage):** first measured linkage evidence — 24/30
  title-resolvable originals linked into arXiv id space by metadata-only
  methods (exact + variant matching), every link carrying raw-response
  provenance. The 6 unresolvable originals must stay keyed by title+venue,
  never by a guessed id.
- **C3 (arXiv-side failure signal):** untouched — MLRC verdicts are
  witness-side signals, not arXiv withdrawal/retraction observables.

## 6. Reproduce

```bash
# inventory + counts (asserts internal consistency)
python3 - <<'EOF'
import json, collections
d = json.load(open('research/experiments/results/issue50/sd30/mlrc_witness_inventory.json'))
assert d['counts']['reports_total'] == len(d['rows']) == 39
print(collections.Counter(r['verdict_bin'] for r in d['rows']))
print(d['counts']['targets_resolved_to_arxiv_id'])
EOF
# raw evidence: mlrc_raw/forums_distilled*.jsonl (39 rows),
#   mlrc_raw/arxiv_resolution/ (61 saved Atom responses),
#   mlrc_raw/s2_resolution/ (31 saved S2 responses)
```

Assembly scripts: `mlrc_raw/scripts/` (build_inventory.py + resolvers).

## 7. Data-quality catches (recorded, not hidden)

- Saved `forum_5L90cl0xtf.html` was an unrendered JS shell (0 `citation_` tags;
  control pattern still matched, proving the grep worked) and had produced a
  wrong original-title attribution. The CroPA row was corrected from a live
  re-fetch: original = "An Image is Worth 1000 Lies…" (arXiv 2403.09766),
  verdict positive. Both HTMLs kept in `mlrc_raw/`.
- `api2.openreview.net` remains CANNOT_CHECK (reqId 2026-08-29-7135377);
  forum pages served as source instead.
- Out-of-scope: MLRC 2022 cohort (44 reports, same pipeline price); ReScience C
  assessed as feasible+structured but witnessing a non-arXiv original space
  (`mlrc_raw/rescience_home.html`); NeurIPS D&B reproduction tracks NOT_CHECKED.

## Authority

Reconnaissance only. No outcome-policy change, no ingestion, no promotion
beyond `WITNESS_SOURCE_CANDIDATE__*_NOT_INGESTED`. Ingestion of any witness
source remains governed by the frozen outcome policy and the SD30 receipt's
lawfulness constraints.

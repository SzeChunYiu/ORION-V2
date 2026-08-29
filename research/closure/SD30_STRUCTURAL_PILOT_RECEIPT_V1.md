# SD30 Structural Pilot Receipt V1 — MATCHED_SUCCESS_FAILURE_CONTRAST (2026-08-29)

Classification: `STRUCTURAL_PILOT__CANNOT_CHECK__FOUR_COUNTS` · Terminal option
exercised honestly: **`CANNOT_CHECK`**. Every count below is proven from the
durable SD10 4-mode corpus ledgers (no new fetches, no new framework), and is
**independent of corpus scale**: the SD20 scale-up now in flight cannot lift
counts C2–C4.

Backlog rule (SD30): *"every candidate operator must explain comparable
failures/non-breakthroughs and carry contraindications."*

## 1. Witness inventory (verified from ledgers, 2026-08-29)

| Quantity | Value | Source |
|---|---|---|
| VALIDATED_FAILURE outcome bindings | **23** (oa 13 + cr 5 + pm 5) | `{mode}_bind.jsonl` |
| distinct failure trajectories | 23 | bindings |
| failure witness class | retraction, only | all three modes |
| failure trajectories with a corpus observation | 22/23 | obs × binding join |
| failure trajectories with ≥2 observations (a version ladder) | **0/23** | obs × binding join |
| VALIDATED_SUCCESS bindings, any mode | **0** | all `{mode}_bind.jsonl` |
| multi-observation trajectories, whole bibliographic modes | 0/14,982 (oa 0/4,982, cr 0/5,000, pm 0/5,000) | obs scans |

Outcome policy (frozen, corpus receipt + adapters): `absence_of_retraction_is_never_success: true`,
`citation_or_prize_metric_is_truth_label: false`, version progression is not an
outcome, unvalidated outcome class = `UNKNOWN`.

## 2. The four structural counts

**C1 — empty operator set.** SD20 (revived, repaired, merged `abd9477`) produced
no surviving operator candidate: conditional-vs-marginal Δ negative at every
powered granularity, LOO 0/18 in every variant. With zero operators there is
nothing for the SD30 rule to test.

**C2 — zero validated successes.** The outcome ontology currently admits
exactly ONE witnessed class (retraction-mediated failure). A matched
success/failure contrast needs at least two; manufacturing a success label from
publication, citation, or prize is forbidden by frozen hard gates. The protocol
amendment (V1 §ingestion) demands the full outcome distribution — successes,
partials, redirections — but **no lawful success-witness source has been
identified**; this is a sourcing gap, not a scale gap.

**C3 — witness domain ≠ operator domain.** SD20 operators are defined on
within-trajectory version transitions; version ladders exist ONLY in the arXiv
mode. Every failure witness lives in a bibliographic mode that is
single-snapshot (0/14,982 multi-observation). Therefore **no SD20 operator can
be evaluated on any known failure trajectory** — the contrast set is empty by
construction, at any corpus size.

**C4 — cross-mode identity linkage is broken.** Bias audit
(`bias_audit_4mode.json` → `outcome_proxy_disagreement`): only the Crossref
mode emits `doi:` trajectory ids; OpenAlex carries `openalex:W…`, PubMed
`pubmed:…`, arXiv `arxiv:…` — disjoint identity spaces, so retraction
witnesses cannot be joined to arXiv ladders (or to each other) without a
separate linkage study. One binding's trajectory (1/23) has no observation row
at all — already unjoinable.

## 3. What would lift each count (priced honestly)

| Count | Lever | Price / status |
|---|---|---|
| C1 | SD20 scale-up (~29k transitions; MDE ≈ 0.017 nats) | **in flight** (`out_scale/` chain, 2026-08-29); if no operator survives at 9× n, C1 becomes near-terminal for this source class |
| C2 | a lawful, non-fame, prospectively-defined success witness source | **unpriced** — requires its own lawful-source study; hard gates forbid every current shortcut |
| C3 | arXiv-side failure signal: withdrawal notices (author-initiated, NOT validated failure) or arXiv↔DOI joins to retracted published versions | **unpriced** — observables exist in Atom metadata but carry no validation; each needs its own lawful-source + validity study |
| C4 | cross-mode identity linkage study (doi ↔ arxiv_id ↔ openalex W-id ↔ pmid; metadata-only joins) | **unpriced** — separate bounded fetch + audit |

None of these is executed here: SD30 is closed as `CANNOT_CHECK`, not deferred
with a promise.

## 4. Consequences for the ladder

- **SD40 (HELDOUT_FIELD_AND_EPOCH_TRANSFER) is transitively blocked** (requires
  SD30) — its variance-floor caveat already documented in
  `SD20_REVIVAL_RECEIPT_V1.md` §7 is now moot until the sourcing gap (C2) moves.
- The programme's live frontier is exactly two items: the SD20 scale-up (C1,
  in flight) and the lawful success-witness sourcing gap (C2). The ladder
  cannot be advanced by relabeling — hard gates stay closed.
- No claim above L1 is made anywhere in this receipt.

## 5. Reproduce

```bash
python3 - <<'EOF'
import json
from collections import Counter
fail = {json.loads(l)["trajectory_id"] for m in ("oa","cr","pm")
        for l in open(f"out/sd10/{m}_bind.jsonl")}
per = Counter()
for m in ("oa","cr","pm"):
    c = Counter()
    for l in open(f"out/sd10/{m}_obs.jsonl"):
        t = json.loads(l)["trajectory_id"]; c[t] += 1
    per.update({t: n for t, n in c.items() if t in fail})
    print(m, "multi-obs:", sum(1 for n in c.values() if n >= 2), "/", len(c))
print("failure trajs with >=2 obs:", sum(1 for n in per.values() if n >= 2))
EOF
```

Artifact basis: `out/sd10/{oa,cr,pm}_{obs,bind}.jsonl` + `bias_audit_4mode.json`
+ `corpus_receipt.json` (frozen pilot corpus; sha256 in the SD10 execution
receipt), re-verified 2026-08-29 after PR #67.

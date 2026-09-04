# FM/FG R2 Registered-Scale Terminal Results Receipt (2026-08-30)

**Lane:** `FM_FG_GENERATED_EXACT_CAMPAIGN` (owner issue #48). Parent artifacts:
dispatch receipt `FMFG_R2_REGISTERED_SCALE_DISPATCH_RECEIPT.md` (this PR's
sibling), R1 pilot receipt `fmfg-r1/FMFG_R1_SUITE_TERMINAL_RESULTS_RECEIPT.md`
(PR #79). Registered plan: `research/experiments/FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V1.json`.

> **Corrected 2026-09-04** by
> [`FMFG_R2_REGISTERED_CLAUSE_NARROWING_ERRATUM_V1.md`](FMFG_R2_REGISTERED_CLAUSE_NARROWING_ERRATUM_V1.md),
> alongside the coverage reconciliation in
> [`FMFG_R2_COVERAGE_RECONCILIATION_RECEIPT_V1.md`](FMFG_R2_COVERAGE_RECONCILIATION_RECEIPT_V1.md).
> §1 originally published only the executed denominator; §4's arm table names five arms
> that carry four distinct procedures. The primary terminal `REGISTERED_SCALE_NULL` is
> unchanged and no rate moves. Read both sections with the erratum.

## 1. Coverage — 8,560 dispatched of 13,168 registered, 8,560/8,560 of what ran valid

Two denominators, and they are not the same number. This run went through the low-level
harness with a uniform hardcoded 5-arm set, bypassing the plan-reading orchestrator; the
plan registers **per-study** arm sets of 5 to 9. **4,608 registered dispatches (35.0%) were
never run.** Under the exact-arm-id rule the coverage receipt uses, the executed set is not
even a subset of the registered one: 10,112 registered dispatches never ran and 5,504 ran
under an id registered for no study, and `10,112 − 5,504 = 4,608`. Erratum §1 reconciles the
two framings; §2 decomposes the 4,608.

| Leg | Studies | Tasks | Dispatched | Registered | run_valid of dispatched | missing_or_invalid |
|---|---|---|---|---|---|---|
| n80 | FG80 | 80 | 400 | 640 | 5/5 arms | 0 |
| n96 | FM30, FM50 | 192 | 960 | 1,248 | 5/5 | 0 |
| n120 | FM10/20/40/60, FG20/40/50/60 | 960 | 4,800 | 7,440 | 5/5 | 0 |
| n160 | FG10, FG30, FG70 | 480 | 2,400 | 3,840 | 5/5 | 0 |
| **total** | **14** | **1,712** | **8,560** | **13,168** | | **0** |

`missing_or_invalid = 0` is a statement about the 8,560 that were dispatched. It says
nothing about the 4,608 that were not, and must not be read as execution completeness
against the registered plan.

Oracle rule held throughout (`PRIVATE_ORACLE_COMMITMENT.json` in every workdir;
answers hash-committed, absent from disk). Authority block false in all
machine outputs — no F2 superiority, no new-mathematical-theory, no
scientific-truth grant (unchanged from R1).

## 2. Executor boundary (n160) — material, documented, controlled

The codex channel (`gpt-5.6-terra` via `0.147.0` side-by-side binary)
degraded mid-n160: responses stopped landing, 515 envelopes were purged as
failures, and the lane was cut over at **2026-08-30T18:03:49+02:00** to a
direct Messages-API executor (campaign channel, `glm-5.2`), per operator
override ("bypass it"). Response receipts stamp the executor actually used:

| Leg | codex-cli | anthropic-api |
|---|---|---|
| n80 | 400 | 0 |
| n96 | 960 | 0 |
| n120 | 4,800 | 0 |
| n160 | 1,885 | **515** |

Within n160 the executor split is **almost perfectly confounded with arm**:
F2_FORMAL_DISCOVERY_FULL = 480/480 anthropic-api; F0 / STRONGEST / TARGET =
100% codex-cli; F2_STATIC mixed (445 codex / 35 anthropic). The patched
executor (backup `.bak-codex` retained; `ORION_FORMAL_EXECUTOR=codex`
reproduces the frozen lane) also normalizes non-string `answer` payloads to
JSON strings for byte-compatibility with the codex schema path; model_calls
and wall-time are receipted per response (median 4.1 s anthropic vs 8.2 s
codex).

**Consequence:** any *cross-arm* contrast inside n160 is an executor
contrast. The pooled all-legs comparison puts F2_FULL last (0.8470 vs
TARGET/F0 0.8598, McNemar p≈0.097) — but that deficit is generated entirely
by the n160 boundary. The registered-scale inference therefore rests on the
pure-executor stock (§4). Internal evidence the deficit is not formal
discovery: within n160, F2_STATIC's own mixed-executor split runs 0.9596
(445 codex) vs 0.9143 (35 anthropic) — same direction as the arm gap.

## 3. Per-study strata (correct/tasks; full CSV archived `rollup-r2/PERSTUDY_R2.csv`)

The `leg` column originally labelled `fg10` as n96 (it carries 160 tasks) and `fg50` as n96
(120 tasks); both are corrected here and in the CSV. §1's leg groupings and every
correct/total cell were already right, and no rate moves.

| study | leg | TGT | STRONG | F0 | F2_STAT | F2_FULL |
|---|---|---|---|---|---|---|
| fg10 | n160 | 1.000 | 1.000 | 1.000 | 1.000 | 0.975 |
| fg20 | n120 | 1.000 | 0.992 | 1.000 | 0.992 | 1.000 |
| fg30 | n160 | 1.000 | 1.000 | 1.000 | 1.000 | 0.969 |
| fg40 | n120 | 0.975 | 0.975 | 0.975 | 0.975 | 0.958 |
| fg50 | n120 | 0.892 | 0.950 | 0.925 | **1.000** | 0.983 |
| fg60 | n120 | 1.000 | 1.000 | 0.992 | 1.000 | 0.975 |
| fg70 | n160 | 0.881 | 0.900 | 0.838 | 0.869 | 0.825 |
| fg80 | n80 | 0.525 | 0.412 | 0.425 | 0.400 | 0.287 |
| fm10 | n120 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| fm20 | n120 | 0.783 | 0.692 | 0.783 | 0.667 | 0.767 |
| fm30 | n96 | 0.448 | **0.615** | 0.604 | 0.562 | 0.573 |
| fm40 | n120 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| fm50 | n96 | 1.000 | 0.927 | 0.969 | 1.000 | 0.990 |
| fm60 | n120 | 0.267 | 0.267 | 0.267 | 0.267 | 0.267 |

Tie/ceiling accounting: **8/14 studies at ceiling** (≥1 arm perfect, margins
≤2 tasks); fm60 is a floor study (all five arms identical 32/120 — generated
task family uninformative for every arm); the discriminative variance lives
in fg80, fm30, fg70, fg50, fm20 (spread 0.08–0.24).

## 4. Registered-scale verdict

**Pooled (all legs, executor-mixed — reported, not interpreted):** TGT
0.8598 = F0 0.8598 > STRONG 0.8586 > F2_STAT 0.8581 > F2_FULL 0.8470;
F2_FULL vs TGT/F0 McNemar p≈0.097/0.099; F2_STAT vs F0 p=0.87.

**Pure-executor stock (codex-cli only: n80+n96+n120, 1,232 tasks × 5 arm labels — but
four distinct conditions; erratum §3):** `F0_PARENT_FEDERATION` and
`STRONGEST_DOMAIN_FORMAL_PARENT` are both class `PARENT_GENERIC` in
`scripts/orion_formal_discovery_arms.py`; their `ARM PROCEDURE` line is byte-identical and
the arm's own name echoed back at the model is the entire difference. No federation
procedure was executed in this lane, so "F0" below names a label, not a federation, and the
verdict's claim that the F2 family "matches the parent federation (F0)" is **withdrawn**.
The comparison against the strongest single parent stands.

| arm | correct | accuracy |
|---|---|---|
| F0_PARENT_FEDERATION | 1,018 | **0.8263** |
| TARGET_ONLY_DIRECT | 1,011 | 0.8206 |
| F2_STATIC_NO_FORMAL_DISCOVERY | 1,010 | 0.8198 |
| F2_FORMAL_DISCOVERY_FULL | 1,007 | 0.8174 |
| STRONGEST_DOMAIN_FORMAL_PARENT | 1,006 | 0.8166 |

All five arms lie within 0.0097 — and the pair at the extremes of that range, F0 (1,018)
and STRONGEST (1,006), is one condition under two labels. The widest spread in this table is
therefore between two runs of the same procedure. One draw, on marginal totals rather than
paired discordance, so it is not a numerical noise floor; it does remove the reading that
the ordering below reflects anything about the arms. Matched discordance (exact binomial):
F2_FULL vs TARGET 57/61 (p=0.78), vs F0 52/63 (p=0.35), vs F2_STATIC 55/58
(p=0.85).

**Verdict: `REGISTERED_SCALE_NULL`** — at pre-declared registered *task* counts, on
a single-executor stock, no one of the four distinct conditions actually executed separates
from any other: formal discovery
(F2_FULL − F2_STATIC) adds nothing (p=0.85), the metabolic loop (F2 family)
matches the parent federation (F0) and the target-only floor, and the R1
pilot ordering (TGT = F2_STAT > F2_FULL > STRONG > F0) **does not
replicate** — it was pilot-scale noise (R1 n=112 tasks); at n=1,232 F0 is
nominally first, inside noise. The lane's economic question is answered at
registered scale; the residual p≈0.097 pooled deficit is attributable to
the §2 executor boundary, not to the treatment.

## 5. Custody

- Workdirs (frozen): `~/sd10run/ORION-V2/.orion-fmfg-r2-{n80,n96,n120,n160}`
  on billy-old — requests/responses (executor-stamped), FROZEN_SUITE,
  PRIVATE_ORACLE_COMMITMENT, EVALUATION_ROWS/SUMMARY per leg.
- Archived here: `rollup-r2/EVALUATION_SUMMARY_{n80,n96,n120,n160}.json`,
  `rollup-r2/PERSTUDY_R2.csv`.
- Corrections: `FMFG_R2_REGISTERED_CLAUSE_NARROWING_ERRATUM_V1.md` and
  `FMFG_R2_COVERAGE_RECONCILIATION_RECEIPT_V1.md`. Successor plan
  `research/experiments/FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V2.json` (prospective; five
  distinct conditions where this lane ran four).
- Executor patch: `scripts/orion_formal_discovery_arms.py` (backup
  `.py.bak-codex`; selector `ORION_FORMAL_EXECUTOR`, default anthropic-api).
- Resume driver: `~/sd10run/fmfg_r2_n160_anthropic_resume.sh`, log
  `~/sd10run/logs-fmfg/driver-r2-n160-anthropic-20260830T180349.log`.

skills-applied: none (results receipt, no manuscript content)

# PC-R6 archive — read first

Terminal artifacts of the **PC-R6 full-regression evaluator lane**: the lane that makes the
registered critical-failure hard gate — left structurally `CANNOT_CHECK` by E30-R11 and E60 —
measurable, by re-running the frozen proposals against each task's full frozen test suite.
Zero model calls; frozen trees read-only; no imputation.

**Terminal:** GR0 PASS → GR1 **PASS** (RD(F2−F0) = 0.0000, one-sided 97.5% upper 0.0000 ≤ 0.02,
**n = 5 paired tasks**), GR2 **NULL**, GR3 **NULL** →
pre-registered route *mean-null + tail-safe at the registered margin*; theory revision B
("obligations are tail insurance, not mean alpha") survives as a boundary claim; no component
earns tail-necessity. Read the denominators in `PC_R6_OUTCOME_RECEIPT.md` before quoting the gate.

| file | what it is |
|---|---|
| `PC_R6_OUTCOME_RECEIPT.md` | gate table (machine-generated, bytes 0–948) + archive addendum (hand-written: denominators, power, honest reading) — **start here** |
| `PC_R6_FULLREG_ROLLUP_V1.md` | per-arm and per-contrast tables |
| `PC_R6_FULLREG_ROLLUP_V1.json` | full analysis output (contrasts, project strata, Holm, sensitivity annex) |
| `PC_R6_FULLREG_RAW_ROLLUP_V1.json` | per-evaluation raw rollup (1,080 evaluations + 80 baselines) |
| `PC_R6_GR0_RECEIPT.json` | GR0 combine (PASS) — enforced before any gate |
| `PC_R6_GR0A_RECEIPT.json` | bit-exact reproduction: e30r11 **480/480**, e60 **600/600**; checker negative control PASS |
| `PC_R6_GR0B_RECEIPT.json` | gold known-answer control, 5/5 projects PASS (+1 not-applicable, recorded) |
| `PC_R6_INPUT_MANIFEST.json` | 2,858 hashed frozen inputs; campaign id |
| `JOB_IDS.env` | SLURM identity of every stage |

Design: `research/experiments/pc-r6/PC_R6_FULL_REGRESSION_EVALUATOR_LANE_DESIGN_V1.{md,json}`.
Runner/analysis + amendments: `research/experiments/pc-r6/PC_R6_DISPATCH_RECEIPT_V1.md`.
Campaign on LUNARC: `/projects/hep/fs9/users/scyiu/orion-v2-pc-r6/campaign-pc-r6-fullreg-e30r11-e60-20260902-774903e1/`.
All nine machine-generated files here are byte-identical to that campaign directory (verified by sha256).

**Quoting figures from the receipt.** Only bytes 0–948 of `PC_R6_OUTCOME_RECEIPT.md` are analysis
output; the addendum below the `ORION-RECEIPT-BOUNDARY-V1` marker is hand-written, and every figure
in it names the artifact and field it came from. The boundary is enforced by
`scripts/check_receipt_boundaries.py` (CI `receipt-boundary-guard`); the convention is
`docs/00-programme/RECEIPT_BOUNDARY_CONVENTION.md`. Two addendum figures were corrected on
2026-09-02 — `NONE_PATCH_NOT_APPLIED` is **75.0%–82.5%** (not "78–83%"), and the `311/480`
`rc=128` count comes from this lane's own `PC_R6_FULLREG_RAW_ROLLUP_V1.json`, not from the frozen
lane. Both had already reached a paper scoping brief.

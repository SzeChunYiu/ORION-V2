# E30-R12 — START HERE

Confirmatory BugsInPy re-run under arm-side apply-clean patch emission (`8945cec`).
A **new prospective study**, not a re-analysis: E30-R11's endpoints stay frozen terminal.

| file | what it is |
|---|---|
| `E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.json` | canonical registered design (governs) |
| `E30_R12_APPLY_CLEAN_RERUN_DESIGN_V1.md` | the same design in prose |
| `e30_r12_power_note.py` | exact MDE / power arithmetic; no outcome input |
| `e30_r12_fullreg_eval.py` | evaluation lane — imports PC-R6's evaluator, adds one cell |
| `e30_r12_analysis.py` | registered endpoints, gates and routing |
| `sbatch/` | LUNARC drivers: setup → agents → frozen lane → GR0 → suite → rollup+analysis |
| `../../../tests/unit/test_e30_r12_lane.py` | known-answer controls for all of the above |

**The one-line reason this study exists.** PC-R6 found `NONE_PATCH_NOT_APPLIED` in 78–83%
of E30-R11's evaluations: roughly four in five never tested a repair. PR #168 fixed the
emission side. R12 asks the registered question under a working interface.

**The one-line caveat, registered before dispatch.** At n = 40 the exact test cannot
reject below a 0.175 risk difference, and power against the registered 5-percentage-point
MID is 1–2%. R12 is an estimation and diagnostic study; a non-rejection is not evidence of
equivalence. See design §7.

**Endpoints.** E1 registered failing test fixed (primary) · E2 any critical new failure
(co-primary, non-inferiority margin 0.02) · D1 patch-apply rate (registered diagnostic,
comparator = PC-R6's per-arm rates measured by the same code).

**Legitimate terminals include `PARENT_SUFFICIENT` and `NO_ARM_SEPARATION`.**

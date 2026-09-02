# PC-R6 full-regression rollup (V1)

Analysis `orion.v2.pc-r6-fullreg-analysis.v1` over `eb33a7be38fd…` (GR0 receipt `0d74b701f9ed…`, generated 2026-09-02T14:13:47.886793+00:00).

No mean-success quantity is computed or reported here (no-rescue clause).

## Cell 1 (E30-R11): F2 vs each other arm

| arm | evaluations | counted | checkable tasks (majority) | tasks any-critical | rate | patch-apply fail | compile fail |
|---|---|---|---|---|---|---|---|
| `F2_ORION_METABOLIC_FULL` | 120 | 22 | 6 | 0 | 0.000 | 0.8167 | 0.0000 |
| `F0_PARENT_FEDERATION` | 120 | 24 | 7 | 0 | 0.000 | 0.8000 | 0.0000 |
| `SAME_MODEL_REFLECTION` | 120 | 22 | 6 | 0 | 0.000 | 0.8083 | 0.0435 |
| `SIMPLE_DIRECT` | 120 | 25 | 7 | 0 | 0.000 | 0.7833 | 0.0000 |

| contrast (RD orientation) | paired (both_F/both_T/L-only/R-only) | checkable | RD [CI95] | one-sided 97.5% upper | exact p | Holm p |
|---|---|---|---|---|---|---|
| F2_ORION_METABOLIC_FULL - F0_PARENT_FEDERATION | 5/0/0/0 | 5 | 0.0000 [0.0000, 0.0000] | 0.0000 | — | — |
| F2_ORION_METABOLIC_FULL - SAME_MODEL_REFLECTION | 4/0/0/0 | 4 | 0.0000 [0.0000, 0.0000] | 0.0000 | — | — |
| F2_ORION_METABOLIC_FULL - SIMPLE_DIRECT | 4/0/0/0 | 4 | 0.0000 [0.0000, 0.0000] | 0.0000 | — | — |

## Cell 2 (E60): FULL vs each MINUS_X (GR3 evaluates the MINUS_X - FULL orientation)

| arm | evaluations | counted | checkable tasks (majority) | tasks any-critical | rate | patch-apply fail | compile fail |
|---|---|---|---|---|---|---|---|
| `F2_ORION_METABOLIC_FULL` | 120 | 21 | 7 | 0 | 0.000 | 0.8167 | 0.0000 |
| `F2_MINUS_DECOMPOSITION` | 120 | 29 | 10 | 1 | 0.100 | 0.7500 | 0.0000 |
| `F2_MINUS_NATIVE_RECOVERY` | 120 | 24 | 7 | 0 | 0.000 | 0.8000 | 0.0000 |
| `F2_MINUS_COUNTERPROBE` | 120 | 21 | 7 | 0 | 0.000 | 0.8250 | 0.0000 |
| `F2_MINUS_SELECTIVE_REOPEN` | 120 | 27 | 9 | 0 | 0.000 | 0.7750 | 0.0000 |

| contrast (RD orientation) | paired (both_F/both_T/L-only/R-only) | checkable | RD [CI95] | one-sided 97.5% upper | exact p | Holm p |
|---|---|---|---|---|---|---|
| F2_ORION_METABOLIC_FULL - F2_MINUS_DECOMPOSITION | 7/0/0/0 | 7 | 0.0000 [0.0000, 0.0000] | 0.0000 | — | — |
| F2_ORION_METABOLIC_FULL - F2_MINUS_NATIVE_RECOVERY | 7/0/0/0 | 7 | 0.0000 [0.0000, 0.0000] | 0.0000 | — | — |
| F2_ORION_METABOLIC_FULL - F2_MINUS_COUNTERPROBE | 7/0/0/0 | 7 | 0.0000 [0.0000, 0.0000] | 0.0000 | — | — |
| F2_ORION_METABOLIC_FULL - F2_MINUS_SELECTIVE_REOPEN | 7/0/0/0 | 7 | 0.0000 [0.0000, 0.0000] | 0.0000 | — | — |

## Gates

| gate | status | detail |
|---|---|---|
| GR1 non-inferiority (≤ 0.02) | **PASS** | RD(F2−F0)=0.0000, upper=0.0000, n=5 |
| GR2 tail insurance | **NULL** | fired: none |
| GR3 component necessity (tail) | **NULL** | fired: none |

**Routing (design §6):** GR1_pass_GR2_GR3_null: P-C closes as mean-null + tail-safe at the registered margin; theory revision B survives as a boundary claim; no component earns tail-necessity


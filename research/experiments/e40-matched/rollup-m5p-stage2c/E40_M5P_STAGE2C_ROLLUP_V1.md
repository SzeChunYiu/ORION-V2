# E40-m5' Stage-2c seed-replica stability-probe rollup V1

disposition: E40_TERMINAL
route: E40 line TERMINAL: deficit attributable to the information available to the loop by any channel tested; further revival needs a new mechanism class

cells complete: 12/12; cannot_check: []
chains: {'COMPLETE': 60}; CANNOT_CHECK chains: []

## contrasts (12-cell primary)
| rule | n | mean_d | perm_p | f0 wins | f2 wins |
|---|---|---|---|---|---|
| TERMINAL | 12 | -0.009778 | 0.999756 | 11 | 1 |
| CONSENSUS_ARGMAX | 12 | -0.009417 | 0.999512 | 11 | 1 |
| PURITY_ARGMAX | 12 | -0.011239 | 0.999512 | 11 | 1 |
| ORACLE_BEST | 12 | -0.002253 | 0.911133 | 7 | 5 |

## consensus-truth rho
{
 "cells_excluded": [],
 "cells_used": 12,
 "directed_pooled_rho": -0.0018518518518518452,
 "draws": 10000,
 "perm_p_two_sided": 0.9893,
 "raw_pooled_rho": 0.0018518518518518452,
 "seed": 20260902,
 "status": "OK"
}

## strata
{
 "weissmann_k562": {
  "CONSENSUS_ARGMAX_mean_d": -0.01208469231082277,
  "ORACLE_BEST_mean_d": -0.004004830893613226,
  "PURITY_ARGMAX_mean_d": -0.011709352301416698,
  "TERMINAL_mean_d": -0.011278145095903852,
  "n": 6
 },
 "weissmann_rpe1": {
  "CONSENSUS_ARGMAX_mean_d": -0.006749331871118282,
  "ORACLE_BEST_mean_d": -0.0005007835951349182,
  "PURITY_ARGMAX_mean_d": -0.010769586948926069,
  "TERMINAL_mean_d": -0.008277135715149255,
  "n": 6
 }
}

## historical m2-F0 panel (cross-model, NON-GATING)
{
 "cells_complete": 12,
 "contrasts": {
  "CONSENSUS_ARGMAX": {
   "f0_wins": 11,
   "mean_d": -0.009258162142235805,
   "n": 12,
   "perm_p": 0.998046875
  },
  "ORACLE_BEST": {
   "f0_wins": 9,
   "mean_d": -0.0020939572956393516,
   "n": 12,
   "perm_p": 0.84423828125
  },
  "PURITY_ARGMAX": {
   "f0_wins": 11,
   "mean_d": -0.011080619676436664,
   "n": 12,
   "perm_p": 0.999755859375
  },
  "TERMINAL": {
   "f0_wins": 11,
   "mean_d": -0.009618790456791834,
   "n": 12,
   "perm_p": 0.999267578125
  }
 }
}

## gates
{
 "G0_DRAG_PRESENT_UNDER_TERMINAL": true,
 "G1_CONSENSUS_RANKS_TRUTH": false,
 "G2_CONSENSUS_SHIPPING_CLOSES_DRAG": false,
 "G3_ANTI_CONTROL_DISTINGUISHES": true,
 "G4_SPLIT_CONSISTENT": false,
 "disposition": "E40_TERMINAL",
 "preregistered_route": "E40 line TERMINAL: deficit attributable to the information available to the loop by any channel tested; further revival needs a new mechanism class"
}

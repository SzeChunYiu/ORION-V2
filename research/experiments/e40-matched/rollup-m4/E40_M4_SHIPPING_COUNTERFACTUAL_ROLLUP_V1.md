# E40-m4 shipping-operator counterfactual rollup V1

reproduced m3 frozen numbers: True
TP orientation resolved: f0_minus_f2

## P_primary
{
 "CT1_primary": {
  "contrast": "f0_best - f2_ship (raw wasserstein, negative = F0 better)",
  "f0_wins": 11,
  "f2_wins": 1,
  "mean_d": -0.011271375931504958,
  "perm_p": 0.99951171875
 },
 "CT2_recovery": {
  "contrast": "f2_final - f2_ship (negative = proxy shipping improves)",
  "mean_d": -0.0038578550969475683,
  "perm_p": 0.8828125,
  "recovery_nonneg_chains": 8
 },
 "CT3_tp_family": {
  "corum_tp": {
   "mean_d": 10.333333333333334,
   "perm_p": 0.001220703125
  },
  "string_tp": {
   "mean_d": 28.166666666666668,
   "perm_p": 0.001708984375
  },
  "true_positives": {
   "mean_d": 14.583333333333334,
   "perm_p": 0.000732421875
  }
 },
 "M1_mechanism": {
  "gate_eval_note": "G2 evaluates pooled_rho_arithmetic (Fisher-z is ill-defined at |rho|=1 with n=4; documented pre-compute in the design clarification)",
  "per_chain_rho": {
   "weissmann_k562:0": 0.816496580927726,
   "weissmann_k562:1": 1.0,
   "weissmann_k562:2": 0.0,
   "weissmann_k562:3": 0.9428090415820635,
   "weissmann_k562:4": -0.7378647873726218,
   "weissmann_k562:5": 1.0,
   "weissmann_rpe1:0": 0.6324555320336759,
   "weissmann_rpe1:1": -0.9486832980505138,
   "weissmann_rpe1:2": -0.816496580927726,
   "weissmann_rpe1:3": -1.0,
   "weissmann_rpe1:4": 0.4,
   "weissmann_rpe1:5": 1.0
  },
  "perm_p_two_sided": 0.253,
  "pooled_rho_arithmetic": 0.1907263740160503,
  "pooled_rho_fisher_z_reference": 0.8405449388659378
 },
 "M2_selection_census": {
  "cycle1_persistence": 6,
  "ship_cycle_census": {
   "1": 6,
   "2": 4,
   "3": 1,
   "4": 1
  },
  "ship_true_rank_mean": 2.5833333333333335,
  "ship_true_ranks": [
   2.0,
   3.5,
   2.0,
   3.5,
   1.0,
   3.5,
   4.0,
   1.0,
   1.0,
   1.5,
   4.0,
   4.0
  ]
 }
}

## R_replication
{
 "CT1_primary": {
  "contrast": "f0_best - f2_ship (raw wasserstein, negative = F0 better)",
  "f0_wins": 11,
  "f2_wins": 1,
  "mean_d": -0.007442126051045705,
  "perm_p": 0.999267578125
 },
 "CT2_recovery": {
  "contrast": "f2_final - f2_ship (negative = proxy shipping improves)",
  "mean_d": 0.001537131874654707,
  "perm_p": 0.203125,
  "recovery_nonneg_chains": 8
 },
 "CT3_tp_family": {
  "corum_tp": {
   "mean_d": 10.333333333333334,
   "perm_p": 0.00390625
  },
  "string_tp": {
   "mean_d": 26.5,
   "perm_p": 0.000244140625
  },
  "true_positives": {
   "mean_d": 12.916666666666666,
   "perm_p": 0.000732421875
  }
 },
 "M1_mechanism": {
  "gate_eval_note": "G2 evaluates pooled_rho_arithmetic (Fisher-z is ill-defined at |rho|=1 with n=4; documented pre-compute in the design clarification)",
  "per_chain_rho": {
   "weissmann_k562:0": -0.3333333333333333,
   "weissmann_k562:1": 0.816496580927726,
   "weissmann_k562:2": 1.0,
   "weissmann_k562:3": -0.816496580927726,
   "weissmann_k562:4": 0.3333333333333333,
   "weissmann_k562:5": 0.3333333333333333,
   "weissmann_rpe1:0": -0.7777777777777778,
   "weissmann_rpe1:1": -0.7745966692414834,
   "weissmann_rpe1:2": 0.816496580927726,
   "weissmann_rpe1:3": -0.816496580927726,
   "weissmann_rpe1:4": 0.31622776601683794,
   "weissmann_rpe1:5": -0.10540925533894598
  },
  "perm_p_two_sided": 0.9968,
  "pooled_rho_arithmetic": -0.0006852169173363308,
  "pooled_rho_fisher_z_reference": 0.44565015693330257
 },
 "M2_selection_census": {
  "cycle1_persistence": 7,
  "ship_cycle_census": {
   "1": 7,
   "2": 3,
   "3": 2,
   "4": 0
  },
  "ship_true_rank_mean": 2.3333333333333335,
  "ship_true_ranks": [
   3.0,
   2.5,
   3.5,
   2.5,
   2.5,
   2.0,
   1.5,
   2.0,
   2.0,
   1.5,
   3.0,
   2.0
  ]
 }
}

## gates
{
 "G0_M3_REPRODUCED": true,
 "G1_DRAG_ELIMINATED_UNDER_PROXY_SHIPPING": false,
 "G2_PROXY_CHANNEL_UNINFORMATIVE": true,
 "preregistered_route": "draft m5-prime feedback-channel design (calibrated extreme-resident probes / proxy-truth calibration)"
}

# E40-m5' Stage-2d planted-control cause discrimination — rollup V1

disposition: **PROMPT_IMPLICATED**
ambiguous: False
route: the cycle-1 mandate text is implicated: the model channel alone does not explain the Stage-2c failure. A future freeze must revise the mandate form, not the plant.

| arm | verdict | terminal quality | distinct configs | distinct fracs |
|---|---|---|---|---|
| A_NO_MANDATE | PASS | 0.9877 | 5 | [0.5, 0.75, 0.8, 0.85, 0.9] |
| B_REGIME_ANCHOR | FAIL | 0.9518 | 6 | [0.0, 0.5, 0.75, 0.9, 1.0] |
| C_SEED_MANDATE | FAIL | 0.0233 | 2 | [0.0] |

## controls
{
 "PLANT_INTEGRITY": "PASS",
 "SERVED_MODEL_PIN": "PASS",
 "LEAKAGE": "PASS",
 "TRAJECTORY_REPLAY": "PASS"
}

## gates
{
 "D0_ARMS_VALID": true,
 "D1_MODEL_CHANNEL_CAUSE": false,
 "D2_PROMPT_IMPLICATED": true,
 "D3_STAGE2C_FAILURE_NOT_REPRODUCED": false,
 "ambiguous": false,
 "arm_verdicts": {
  "A_NO_MANDATE": "PASS",
  "B_REGIME_ANCHOR": "FAIL",
  "C_SEED_MANDATE": "FAIL"
 },
 "disposition": "PROMPT_IMPLICATED",
 "failed_controls": [],
 "route": "the cycle-1 mandate text is implicated: the model channel alone does not explain the Stage-2c failure. A future freeze must revise the mandate form, not the plant."
}

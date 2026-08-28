# Execution Partial Scientific Adjudication — 2026-08-28 V1

**Status:** evidence-bound partial closeout. This receipt closes only native-compute/descriptive sub-studies. It does **not** close the corresponding ORION-vs-F0 cross-domain studies and does not promote any paper to R3 or R4.

## Evidence examined

### E40 — CausalBench native computation

The corrected native CausalBench chain completed and its rollup was archived on the live branch at commit `6b29b013506fbba7e76293affba211924536a4ec`.

Recorded outcomes:

- K562 observational: TP 137, FP 272, mean Wasserstein 0.1652013430;
- K562 partial-interventional: empty output network, TP 0, FP 0, Wasserstein unavailable;
- RPE1 observational: TP 41, FP 128, mean Wasserstein 0.1562735710;
- RPE1 partial-interventional: empty output network, TP 0, FP 0, Wasserstein unavailable.

The empty partial-interventional outputs are retained as adverse native-compute outcomes.

Native-compute terminal:

`E40_NATIVE_COMPUTE = COMPLETE_WITH_ADVERSE_PARTIAL_INTERVENTIONAL_RESULT`

The full E40 scientific study remains open because the following are not yet bound/executed:

- matched F0/F2 control around the same native learner;
- label-permutation/control study;
- independent native-domain adjudicator;
- cross-domain ORION transition claim.

Therefore:

`E40_ORION_CROSS_DOMAIN_STUDY = OPEN`

### E50 — Matbench Discovery native-model characterization

A validated native result was synchronized to LUNARC with result SHA-256 `6bca82efcb5f3e6c3e347ae0d8fbb1ef0a5e50553df80746d1f5fe86a1a0de64` and manifest SHA-256 `a70bc7eab14825f020c4f631e68d09c53e8ebb1306dee1fe5bab641d8c53dcf6`.

Reference and prediction artifacts each contained 256,963 unique material IDs; held-out family size was 51,518.

Native descriptive results:

- CHGNet v0.3.0: canonical F1 0.611772; held-out F1 0.607205;
- MACE-MPA-0 v0.3.9: canonical F1 0.835569; held-out F1 0.826302;
- ORB v2: canonical F1 0.858320; held-out F1 0.854306.

ORB v2 leads the evaluated native-model metrics and is the strongest of these three native candidates for subsequent matched scientific-control comparison.

Native-characterization terminal:

`E50_NATIVE_MODEL_CHARACTERIZATION = COMPLETE_DESCRIPTIVE`

The full E50 scientific study remains open because:

- model-inference resource-cost normalization is unavailable from the precomputed artifacts;
- matched F0/F2 comparison is not yet implemented;
- independent materials-domain adjudication is not yet bound.

Therefore:

`E50_ORION_CROSS_DOMAIN_STUDY = OPEN`

## Paper implications

These results are useful inputs, but they do not satisfy any primary paper's decisive claim.

- **P-C:** gains native-domain task surfaces and an adverse learner condition, but no ORION-vs-F0 controller result yet.
- **P-D:** gains a concrete evaluator/native-output failure case, but no dependence/assurance comparative study yet.
- **P-F:** gains candidate native substrates/baselines, but no predeclared machine-native mechanism effect or matched-compute comparison yet.
- **Flagship:** gains evidence that native scientific systems can have materially different failure structures, but no F2-over-F0 residual.

No paper can be promoted to R3 on this evidence alone.

## Current portfolio terminal

```text
E40_NATIVE_COMPUTE = CLOSED_DESCRIPTIVE_WITH_ADVERSE_RESULT
E40_ORION_CROSS_DOMAIN_STUDY = OPEN
E50_NATIVE_MODEL_CHARACTERIZATION = CLOSED_DESCRIPTIVE
E50_ORION_CROSS_DOMAIN_STUDY = OPEN
E20_BUGSINPY_PILOT = OPEN_INFRASTRUCTURE_REPAIR
P_A_R3 = NO
P_B_R3 = NO
P_C_R3 = NO
P_D_R3 = NO
P_E_R3 = NO
P_F_R3 = NO
FLAGSHIP_R3 = NO
R4_SUBMISSION_READY = NONE
```

## Promotion rule

The first paper-level closure becomes possible only after a result binds the paper's frozen central claim against its strongest parent/simple control, with the required scientificity, robustness and independence conditions. Native benchmark completion alone is not sufficient.

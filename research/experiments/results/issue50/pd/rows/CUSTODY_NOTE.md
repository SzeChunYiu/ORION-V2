# P-D campaign rows — custody note V1

**State date:** 2026-09-04 · **Lane:** guards · **Class:** REPAIR_DOCUMENTED_NOT_LANDED

`PD_R1_CAMPAIGN_TERMINAL_RESULTS_RECEIPT.json` declared `analysis_summary_sha256` and `evaluation_summary_sha256` for the POST-execution summaries, but the files committed beside it were the PRE-execution copies (7a582b7d… / 8ff6f065…, model arms `missing: 40`). The post-execution files lived only on billy-old at `~/sd10run/ORION-V2/.orion-dependence-evidence-campaign/`. This directory lands them; the receipt is untouched.

## Landed (transferred by rsync, md5 manifests on both sides, 14/14 identical)

- `../CAMPAIGN_ANALYSIS_SUMMARY.json` — sha256 `74544360d96654b61c473a00bde36d2673431d018aae0856790f3d28c6ab74e0` = receipt `analysis_summary_sha256` (asserted before commit)
- `../CAMPAIGN_EVALUATION_SUMMARY.json` — sha256 `e9470bf8d389029480b2b0ac2d65406eedf5b34439c33d86ec45a17d97825695` = receipt `evaluation_summary_sha256` (asserted before commit)
- per study: `EVALUATION_ROWS.json` (exact-match rows: task_id, arm, expected, actual, correct), `EVALUATION_SUMMARY.json`, `PRIVATE_ORACLE_COMMITMENT.json` (the pre-dispatch hash commitment of the oracle).

| study | EVALUATION_ROWS.json sha256 | EVALUATION_SUMMARY.json sha256 |
|---|---|---|
| PD-S1-DEPENDENT-CORROBORATION | `9fb487ebfd6d5b7df19c80b8de6de94de230afc1adcedb3e7447011153a40756` | `3cf4526d6a0d67b760a66e3fd42bea7e011ab4e65bf1d705cf7891db2e57dc1a` |
| PD-S2-ARGUMENT-AND-ADEQUACY | `5f9a9be46039b5fa76da8b0a91e30e0dfe25ef63f1e8b8454cd186c2fffaf2b5` | `42e3e541a8a30cda6b8d7a051b153466ad73e0330e2669c3deedba78a25f89be` |
| PD-S3-REVOCATION-AND-UPTAKE | `fd50535e80af75a5cb72fe9ba0ff3bcd6e5ba68343162c65d86579fb418595a9` | `d23cad825561317dce15704b22737a2345a04dc7aed4753009f5692ba7a3cff1` |
| PD-S4-AUTHORITY-AND-RESPONSE | `41a097c19ee8dc47d02aef2153631f7f30588eb86cf0600e9eaf79311fc10183` | `247110dc22d270d148e1ba3c0028e8c0001ce3c3bfcd8361b73c87359b7ec849` |

## Not landed: the four post-restore `private_oracle.json`

The campaign design (`research/experiments/DEPENDENCE_EVIDENCE_GENERATED_CAMPAIGN_DESIGN_V1.md` §5) hash-commits the oracle, hides it for the whole child dispatch, restores and hash-checks it, and has the analysis step read the restored oracle — it is silent on post-run disclosure and names no custody path. No `private_oracle.json` is committed anywhere on main (repository precedent: 0). They therefore stay where the design left them, on billy-old beside the rows, with their identities recorded here so a later disclosure decision is verifiable:

| study | private_oracle.json sha256 (prefix) | bytes | location |
|---|---|---|---|
| PD-S1-DEPENDENT-CORROBORATION | `5c1d1374e1cf…` | 25023 | billy-old `~/sd10run/ORION-V2/.orion-dependence-evidence-campaign/PD-S1-DEPENDENT-CORROBORATION/private_oracle.json` |
| PD-S2-ARGUMENT-AND-ADEQUACY | `b12a5cfb5a84…` | 11143 | billy-old `~/sd10run/ORION-V2/.orion-dependence-evidence-campaign/PD-S2-ARGUMENT-AND-ADEQUACY/private_oracle.json` |
| PD-S3-REVOCATION-AND-UPTAKE | `d0057d772c4d…` | 19623 | billy-old `~/sd10run/ORION-V2/.orion-dependence-evidence-campaign/PD-S3-REVOCATION-AND-UPTAKE/private_oracle.json` |
| PD-S4-AUTHORITY-AND-RESPONSE | `c3449124d89c…` | 18403 | billy-old `~/sd10run/ORION-V2/.orion-dependence-evidence-campaign/PD-S4-AUTHORITY-AND-RESPONSE/private_oracle.json` |

Note that `EVALUATION_ROWS.json` carries `expected` per task, so the oracle's answers are disclosed through the rows the design itself emits; what is withheld is only the oracle file's strata block and its exact bytes.

## Authority

Grants nothing. This note lands bytes the receipt already bound; it changes no number, gate, terminal or datum. lane-paper-2 recomputed every P-D figure from these rows and reports they reproduce; that verification is theirs, not this note's.

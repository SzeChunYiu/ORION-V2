# PC-R6B — the tail gate re-registered with a non-degenerate n (frozen design V1; channel-dependent)

**Revival backlog:** #308 row **R6**. **Parent:** PC-R6 `GR1 PASS, GR2 NULL, GR3 NULL` resting on **5 paired tasks**, all concordant-negative,
risk differences exactly 0, degenerate CIs. **Attributed stage (one):** *power / degenerate design*. **Lever:** re-register the tail gate on a
task set large enough for non-degenerate intervals. **Frozen:** 2026-09-05.

## Design
- Paired task set: every E30-R13-eligible naturalistic task with both arms evaluable under the frozen full-regression evaluator
  (`pc_r6_fullreg_eval.py`, adapter sha256 asserted) — target ≥ 40 paired tasks (the parent had 5).
- **Non-degeneracy rule (new, frozen):** GR1's 95 % CI on the paired risk difference must have half-width ≤ 0.15 and ≥ 3 discordant pairs;
  otherwise the gate returns `CANNOT_CHECK__DEGENERATE`, never `PASS`. The parent's GR1 would have returned exactly that.
- GR1 (non-inferiority at the parent margin), GR2 (tail insurance), GR3 (component necessity) verbatim, each with its denominator.
- Arms: `F2_ORION_METABOLIC_FULL` vs `F0_PARENT_FEDERATION` on the E30-R13 channel-contract campaign (rep-3 offline core4).

Pre-registered reading: GR1 PASS with a non-degenerate interval closes the P-C tail claim at the registered margin with evidence rather than
arithmetic; a tail signal the parent could not see reopens GR2/GR3 under a new identity. Both are publishable.

## Channel, custody, staging
The new arm evaluations need the E30-R13 model channel (window ~2026-09-07 codex / ~09-09 z.ai). Seed committed (sha256
`a4650380ea75ce64…`), custody on the Mac, scp+md5 to LUNARC before dispatch. `pc_r6b_suite_array.sbatch` mirrors the parent's array lane
and refuses without `PROTECTED_RUN_AUTHORIZATION.json` minted at dispatch from the operator's standing verbatim authorization.

Owning manuscript: P-C (lane-paper-2b). Grants nothing. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

skills-applied: none (frozen design, no manuscript content)

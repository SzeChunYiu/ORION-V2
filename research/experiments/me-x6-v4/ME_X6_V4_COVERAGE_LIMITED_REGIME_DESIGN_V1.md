# ME-X6 V4 — the coverage-limited regime: the typed prior's value as a function of coverage (frozen design V1)

**Revival backlog:** #308 row **R2a**. **Predecessor terminal:** ME-X6 V3 `TYPING_IS_A_COVERAGE_PRIOR`
(typed state ties a coverage-matched untyped comparator 1800/1800; V2's frozen vector fails 0/400 on
the four roles it never saw exercised). **Attributed stage (one):** *regime* — with full role coverage
at fit time the prior cannot show. **Lever:** registered domains with LIMITED coverage at population
(fit) time; typed vs untyped measured on every stratum, exercised and unexercised, at five coverage
levels. **Frozen:** 2026-09-05, before any protected instance exists. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

## 1. Question and pre-registered expectation

**Q.** When an untyped learner is fitted on a domain that exercises only `k` of M's eight declared
validation roles, how much of the protected population does the typed assignment decide that the
learner does not — and is any of that advantage located on strata the learner *did* see?

**Expectation (written before the run).** (i) On every exercised stratum the domain refit ties M
exactly (0 discordant, both scales) — **live**: this can fail in either direction. (ii) On an
unexercised lone-carrier stratum whose channel the refit *zeroes*, M is ahead **by construction**
(the refit cannot read a stratum whose only mover it ignores) — registered as the coverage-gap
disclosure, never as evidence about typing. (iii) On an unexercised stratum whose channel the refit
reached through *co-movement* in non-carrier strata (the development fit shows exactly one such
case: `formal_artifacts` at `D_0`), the outcome is **live** and reported: a tie there means
coverage is broader than lone-carrier exercise. (iv) The advantage `M − refit` is non-increasing in
`k` and zero at `k = 8` (V3 reproduced). Expected route:
`TYPING_VALUE_EQUALS_COVERAGE_GAP__NO_COMOVEMENT_RECOVERY` or `…__COMOVEMENT_RECOVERS_SOME_STRATA`.

## 2. Domains (registered role order = `G.ROLE_LONE_CARRIER_STRATUM`)

`D_k` = the ten non-carrier V1 strata + the first `k` lone-carrier strata, `k ∈ {0, 2, 4, 6, 8}`:
formal_artifacts (X6I7), replications_passed (I9), independent_rederivations (I10), retractions (I4),
corrections (I11), replications_failed (I12), solution_cost (I13), downstream_reuse (I14). `D_8` is
V3's full coverage. Fits use V3's **public** development seed (`ME-X6-V3-DEV-20260904`, 2 per cell)
restricted to the domain's strata, so `D_8`'s refit **equals V3's frozen refit vector** — the
known-answer gate (G0a), verified at freeze: `True`.

## 3. Arms

| arm | what | can it lose? |
|---|---|---|
| `M_TYPED_COLLECTIVE_STATE` | V1's typed rule, unchanged | on V1 strata no (exact by construction, disclosed); on the four V3 strata yes (G0d live) |
| `B8_D{k}_REFIT_COVERAGE_{k}_OF_8` | V2's `select_capacity_matched` on `D_k`'s dev split | yes |
| `B4X_D{k}_UNIT_SIGN_COVERAGE_{k}_OF_8` | V1's `fit_signs` on `D_k`'s dev split | yes (reported, not gated) |
| `C_ALWAYS_RISE/FLAT/FALL` | constants | null bar (derived: modal class 8/18) |

Development fit (frozen, `ME_X6_V4_DEVELOPMENT_FIT_V1.json`): every refit scores its own dev split
exactly; zeroed unexercised roles per domain: D_0 seven (formal_artifacts reached by co-movement),
D_2 six, D_4 four, D_6 two, D_8 none.

## 4. Gates and route

| gate | rule | class |
|---|---|---|
| G0a | `D_8` refit == V3's frozen refit vector | known-answer, hard |
| G0b | planter agrees + fit window decidable on every instance | hard |
| G0c | best constant arm == derived modal bar on the balanced split | hard |
| G0d | M exact on all strata | hard (live on the four V3 strata) |
| G1 | 0 discordant M vs `B8_Dk` on exercised strata, both scales, every `k` | **live** |
| G2 | M ahead on every zero-weight unexercised cell | BY_CONSTRUCTION (disclosed) |
| G2b | co-movement strata: tie / M ahead / refit ahead, reported per cell | **live** |
| G3 | advantage curve non-increasing in `k`, zero at `k = 8` | live |

Route: hard fail, G2 fail or a refit ahead on a co-movement cell → `LANE_DEFECT`; G1 fails with M
ahead on an exercised stratum → `TYPING_SEPARATES_BEYOND_COVERAGE`; G2b ties →
`TYPING_VALUE_EQUALS_COVERAGE_GAP__COMOVEMENT_RECOVERS_SOME_STRATA`; else
`TYPING_VALUE_EQUALS_COVERAGE_GAP__NO_COMOVEMENT_RECOVERY`. Selftest plants both a tie violation on
an exercised stratum and a tie on a zero-weight gap stratum; each must fire.

## 5. Protected split, seed, custody, compute

18 strata × 2 scales × 50 = 1800, fresh seed (custody `~/.orion-custody/me-x6-v4/PROTECTED_SEED_V1.txt`,
sha256 in the JSON, scp+md5 to LUNARC, revealed after). `protected` refuses without the ME-X-shape
authorization (exit 3), on fit drift (exit 5) or a seed not hashing to the commitment (exit 4).
LUNARC `lu48`, `.venv` CPython 3.13.5. Development fit computed on billy-old (CPython 3.14.4),
pure stdlib, deterministic, md5-verified on transfer.

## 6. Authority

Grants nothing: ME-X6 V1/V2/V3 unchanged; no field status, novelty or manuscript change. The
strongest statement a positive here can make is quantitative: *the typed prior is worth exactly the
coverage gap, measured stratum by stratum*, on one generator family.

skills-applied: none (frozen design, no manuscript content)

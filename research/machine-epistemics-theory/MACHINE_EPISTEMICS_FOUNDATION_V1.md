# Machine Epistemics Foundation V1 — canonical OCM authority surface

Status: **FROZEN_CANDIDATE** on #319. Freeze terminal is earned only after merge + repository checks.
Authority snapshot: main `d756c086edc46ad4e5e682f69730b72c1dc26a4c` (includes merged #317); foundation semantics `2d6739048866a698998891906634a72e570d762c`.

## Completeness boundary
Foundation V1 means the OCM dependency surface is completely typed: every primitive is either settled, parent-adopted, finite-calibration-only, OPEN, or CANNOT_CHECK; every settled import is parity-gated. It does **not** mean every Machine Epistemics research question is solved.

## Expert cells
X3 formal semantics owns compositional laws and typed terminals; X4 statistics/learning owns calibration and population-vs-individual validity; X6 ORION epistemics owns evidence/authority/scope/revocation; X8 hostile referee searches parent reductions and counterexamples; X9 reproducibility owns exact commits, checkers and merge-state consistency. No cell vote authorizes a claim.

## Four load-bearing closures
1. **MEG-02:** marginal/statistical coverage warrants a scoped procedure-level meta-claim, never an individual candidate truth. `truth=UNKNOWN` may coexist with `action=AUTHORIZED_RISK_BOUNDED` under an explicit policy.
2. **MEG-36:** every statistical/evaluator certificate binds `implementation × model × configuration × runtime × checker × calibration × assumptions × scope × epoch`; drift routes to REVALIDATE/CANNOT_CHECK.
3. **MEG-16:** the atlas' unconditional Kleene claim is **refuted and preserved**. Nogoods spanning two LIVE operands can make their conjunction `CONTRADICTED`; post-product filtering is mandatory. Kleene conjunction survives only under a checked no-cross-nogood condition.
4. **V2→OCM direction:** OCM may absorb a general rule only with V2 issue/study, rule/theorem, terminal, source commit, scope/resource assumptions and an exact parity test.

## Registry shape
`MACHINE_EPISTEMICS_FOUNDATION_V1.json` contains 20 foundation primitives and a total map for MEG-01…MEG-36. `PROVED`, `ADOPTED`, and `PARENT_OWNED` are parity-gated; `FINITE_CALIBRATION` is scope-gated; `OPEN`, `CANNOT_CHECK`, and pending PRs carry no authority.

Merged #317 contributes eleven proved one-day rows (MEG-01/04/06/08/18/22/26/29/30/31/35). This task contributes MEG-02, corrected MEG-16, and MEG-36. MEG-32 is parent-statistics adoption. Every remaining MEG identity stays explicitly OPEN.

## Exact hostile checks
`machine_epistemics_foundation_v1_check_v2.py --registry research/machine-epistemics-theory/MACHINE_EPISTEMICS_FOUNDATION_V1.json` checks: 20 primitive rows; exact MEG-01…36 coverage; authority/status discipline; merged #317 binding; OCM absorption fields; MEG-02 score→truth mutant; all nine behavior-identity drift components; MEG-16 post-product filtering and the LIVE+LIVE cross-nogood counterexample.

Current local replay: registry 20 primitives / 36 MEG rows / 11 merged #317 rows / 0 pending; 5/5 registry mutants caught; identity drift 9/9; n=3 nogood algebra 20 profiles, 2,800 choice checks, 2,800 product checks, 2,401 associativity checks and 1,147 conditional-Kleene checks; unit suite 6/6.

## Scientific boundary
The statistical split follows the parent boundary that marginal coverage is not arbitrary individual conditional truth; configuration shift is certificate-relevant because prompt/decoding/model-configuration changes can alter empirical guarantees. These are parent constraints, not ORION novelty.

External demarcation remains external authority. This registry cannot turn #38 into field recognition, nor upgrade `PARENT_SUFFICIENT`, `CANNOT_CHECK`, or `NOT_ESTABLISHED`.

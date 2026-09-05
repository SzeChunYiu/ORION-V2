# Concurrent-main reconciliation before publication

Scientific inspection baseline: `24566f00a9dc4425a438fcfac05d13c6b2d903db` (#310).
New main observed while this packet was being authored: `d756c086edc46ad4e5e682f69730b72c1dc26a4c`, merged #317, `KSO_ONE_DAY_THEOREMS_BATCH1_V1.md` and its checker.

The foundation's new files are additive and its reference calculations do not import or mutate the concurrent files. Publication is based on the newer main tree, while the original audit/atlas identity remains pinned. This note prevents stale claims of missing work and preserves distinct contribution provenance.

## Results in #317 that must be credited

The batch already makes revoke-plus-quarantine restore the original navigable structure and distinguishes it from revocation alone (T4); restricts information-gain subadditivity to nested/common-source cases and gives a general-dependence counterexample (T9); intersects upper bounds rather than replacing them blindly (T10); and supplies acyclic evidence flattening (T11). Our T01/T03/T08/T15 are overlapping checks, corrections to the older atlas, or extensions—not first-discovery claims against the concurrent batch.

It also states integer-vector metering, a navigation tail bound, authority-meet rules, and an explicit conservative unique-interpretation policy. Query-specific agreement in our T12/T13 is an alternative sound policy under true-model inclusion, not a proof that a stricter selection policy is internally inconsistent.

## Remaining exact distinctions

**B1-T2(c), minimum budget.** Let P=[1], s=[1], alpha=1/2, a0=1/2 and theta=7/10. Then a1=3/4 >= theta, so budget 1 proves FOUND. The first index k' with (1/2)^(k'+1) < theta-a0=1/5 is 2. Hence k' is not the least budget that can decide. The upper bracket remaining above theta does not prevent the lower bracket crossing theta. `check_navigation` executes this counterexample.

**B1-T2, equality boundary.** In a finite nilpotent chain the Neumann series terminates; a finite partial sum can equal a* and decide FOUND at theta=a*. Therefore exact equality is not universally an undecidable-by-bracketing case. The x->y example attains a_y=1/4 after one iteration. Our rule is lower>=theta for FOUND, upper<theta for NOT_FOUND, otherwise this bracket is unresolved.

**B1-T4(iii), possibility versus necessity.** Added denominators can change old navigation, as both packages show. They need not do so for every old-tail edge: zero active input into that tail or alpha=1 are immediate no-effect cases. Use 'can differ' unless the extra positivity/reachability assumptions are stated.

**B1-T7, disjointness.** The implication for a certificate explicitly factored through the model's warrant is valid. However complete evidence-footprint disjointness is not necessary for surviving a model-evidence revocation. Lambda_M={{a}}, Lambda_kappa={{a},{b}} share a; after revoking a, kappa remains LIVE through b. This is an alternative-support fact, not statistical independence. `check_budget_and_locality` executes it.

**B1-T8, scope.** Integer charges prove a bound on charged transitions. They do not rule out uncharged repeated queries, internal stuttering or blocking waits. Snapshot replay is valid for a specified serialized/single-writer transition history. It does not, by itself, prove serializability of concurrently computed mutations merged from different snapshots; that stronger deployment claim needs a commit protocol such as our T11. This is a model-boundary qualification, not denial of deterministic replay on an immutable snapshot.

## Status consequences

The original 35-row map is baseline-relative and records what this package supplies, not a claim that no other lane has closed a scoped obligation. The new batch's accepted special cases remain usable. The budget/disjointness overclaims receive explicit counterexamples rather than silent wording changes. Full runtime adoption and independent review remain separate.

A cross-check comment was posted to #317 from #312 before this package's publication. No original receipt, theorem file, protected outcome or manuscript was changed.

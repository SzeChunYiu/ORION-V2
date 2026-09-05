# OCM absorption contract: decision frontier V1

Science owner: ORION-V2 #314. Runtime owner: ORION-OCM. Source base: `24566f00a9dc4425a438fcfac05d13c6b2d903db`; bind the eventual source commit and receipt hashes before adoption. This contract itself does not adopt code or close a machine milestone.

## 1. Admitted input

A runtime adapter must supply the complete finite model `M` in THEORY.md, an externally scoped closure/validity attestation, a nonempty belief set bound to the retained evidence, the exact budget and full semantic identity. The synthetic reference's `closure_id` is only a required tag. OCM must validate the real attestation and the actual operator/channel refinement; passing a string is not sufficient.

Every observation operator must be total, deterministic, read-only and available at its registered positive rational cost under this model. Real I/O, noise, unavailable channels and changing environments require a successor contract or `CANNOT_CHECK`. Caller authorization to query is a separate precondition. A solver policy is not an action capability.

The planner may read the public possibilities table; it may NOT receive the actual world, evaluator gold, a free all-world encoder message or an uncharged outcome source. Actual-world access is restricted to `replay`, an evaluation-only helper.

## 2. Outputs and their ceilings

| Reference output | Meaning | Forbidden inference |
|---|---|---|
| `DECISION_READY` | A common permissible decision exists now | Scientific truth or authorization to execute |
| `QUERY_POLICY_READY` | A checked finite policy fits the supplied query budget | Practical full-system efficiency or successful physical execution |
| `BUDGET_INSUFFICIENT` | Exact optimum exceeds the declared budget | No solution exists / a representation Jump is necessary |
| `OBSTRUCTION_WITNESSED` | One full observation-equivalence cell has no common permissible decision | All possible future observations or lower-level repairs fail |
| `CannotCheck` | Closure unbound or exact instrument capped | Negative scientific evidence |
| `ContractError` | Malformed/inconsistent input/certificate | A valid answer inferred from an empty world set |

A proposed assertion or recommendation keeps its own exact/statistical warrant type. This package does not replace the typed-risk work in #312/#313 and does not promote marginal coverage into individual truth.

## 3. Release and reopening rule

Before releasing the selected decision, OCM must revalidate contract, epoch, source/operator identity, family-closure scope, retained evidence and external commitment authority. This is required again after any concurrent relevant update; a pre-update policy check cannot authorize a post-revocation release. A minimal implementation uses a consistent snapshot and compare-at-commit identity; real concurrency/transaction design remains a runtime obligation.

After revoking an observation, reconstruct the belief from the remaining valid evidence instead of reusing the narrowed cache. Recheck `old_action∈Safe(new_B)`. If false, reopen; if true, keeping the decision does not require inventing a new proof of hidden-world identity. Changing the world dynamics is not the same operation as deleting an observation.

## 4. Required parity checks before runtime use

Reproduce the complete registered finite corpus and every witness with the adapter. In particular preserve the triple-overlap counterexample, constant-signal encoder obstruction, exact rational costs, full certificate domains, seven-coordinate drift controls, uncharged-advice rejection, the distinction between budget and obstruction, and the correlated evidence non-additivity case. Match the saved scientific payload and hash every adopted source. Test all policy branches, not a selected favorable trace.

Exact and approximate policies need different contracts. An approximate valid policy gives an upper cost bound; it cannot claim exact `BUDGET_INSUFFICIENT` without a separately checked lower bound. Exceeding a search cap must be `CANNOT_CHECK`, not an optimality or impossibility certificate.

## 5. Resource manifest

Report offline history/signal acquisition; full observation and acceptable-action tables; encoder/decoder/codebook bits; policy-synthesis time and peak memory; all subset/partition/cover exploration; model hashing; certificate generation and checking; online queries and their actual resource vector; persistent evidence and message storage; and revalidation/reopening cost. The scalar rational query cost is one registered coordinate, not a replacement for the programme's Pareto resource vector.

Default reference caps: 12 worlds for subset synthesis/checking; 7 worlds for full-state encoder enumeration; 7 attained signals for constrained encoder enumeration; 16 actions for zero-query cover enumeration. These are instrument limits, not claims about realistic OCM scale.

## 6. Unclosed frontier

Noisy/partial channels; trustworthy family closure from natural language; causal interventions with effects; efficient dynamic recertification; learned hypothesis/decision regions; unbounded discourse; neural operator refinement; full system scalability; an externally reviewed novel residual. New experiments must use a fresh frozen identity with strongest applicable DRD/decision-tree/incremental-computation parents.

# Non-authorizing OCM absorption contract

Science owner: V2 #316, ME-CAUSAL-VERIFIER-V1. This is a contract for a later parity-tested adapter, not authorization to adopt code, change a protected result, or close an OCM milestone. Existing runtime branches are untouched.

## Required distinctions at the boundary

An adapter must carry the model-family identity, claim/query identity, evidence semantic type, observation/intervention regime, source and target scopes, intervention implementation identity, measurement/checker identities, validity epoch, provenance/support IDs and costs. The envelope's digest must cover its actual content. This reference only validates finite predicates and same-ID/different-content collisions; it is NOT a production authentication, persistent identity, authority or transaction system.

The adapter must never infer any of the following conversions:

- an observed event to an exact population distribution;
- observational conditioning to a surgical intervention;
- single-world marginals to a cross-world joint law;
- separate logical support IDs to statistical independence;
- source-world certification to target-world certification;
- verifier agreement to correctness, or pass rate to false-acceptance rate;
- an empty compatible set to a supported claim;
- loss of positive support to refutation;
- SUPPORTED-relative-to-assumptions to an authorized external action.

A RESPONSE_LAW record requires a real certificate or an explicit model assumption with its own provenance. No runtime convenience constructor may silently fabricate that stronger information. Mathematical fixture certificates must remain tagged as fixtures, not external scientific evidence.

## Status mapping

SUPPORTED and REFUTED are claims relative to a named, nonempty family and active evidence. UNKNOWN is semantic underdetermination inside that covered family. INCONSISTENT is evidence/model conflict. CANNOT_CHECK is a missing required interface or applicability condition. None should become a success because a downstream function completed. Externally authorized decisions under uncertainty are governed separately by #312/#313 and the runtime commitment boundary.

The model-family-coverage premise and correctness of evidence predicates are external assumptions. Model-class expansion, checker/configuration changes and changed intervention meaning invalidate old compiled support objects until re-evaluated. This module only proves revocation for a FIXED family and fixed record meanings. A scope string comparison is an admission guard, not a proof of scientific transportability.

## Mandatory parity fixtures

1. Cause vs confounder: identical observation laws, effects 1 versus 1/2.
2. Correlated vs anticorrelated potentials: all nine intervention laws identical, equality counterfactual 1 versus 0.
3. Joint-certificate lifecycle: UNKNOWN -> SUPPORTED -> UNKNOWN -> SUPPORTED while the separate intervention effect remains SUPPORTED.
4. Two alternate exact supports: revoke one, retain the other; revoke both, reopen.
5. Inconsistent laws: INCONSISTENT, never vacuous truth.
6. Repeated record: no new logical information; duplicate ID with different payload: reject.
7. Source/target mismatch: CANNOT_CHECK absent a separately verified transfer object.
8. Two 5% verifier-error marginals: joint false-acceptance range [0,5%], not the independent 0.25% point.
9. One observed sample: 28 compatible models; its full reference observation law: 8. Preserve information accounting.
10. Failure/CANNOT_CHECK CLI controls retain exit 1/2 under optimized Python.

These exact numbers apply only to the registered Boolean family. The strongest conventional baseline is the same finite SCM evaluator plus ordinary support tracking and coupling bounds. It receives the same model, evidence, preprocessing, verifier and storage budgets. We expect no architecture residual from renaming these parents.

## Research dependencies, not a new milestone tree

#312/#313: typed warrant/risk and generic lifecycle corrections must accommodate these causal fixtures. #314: any decision-cost policy using our causal claims must not replace an intervention with a read-only observation; modeling state-changing experimental costs is a new study. OCM M2: future registry/replay adapter parity, not a claim the complete runtime is supplied here. MEG-15: registered outcome functions still need fidelity; MEG-22: shared-source supports do not determine stochastic coupling; MEG-29: same-model agreement is not independent verification; MEG-33: acquisition must name the information interface it actually reveals.

A future adoption receipt binds the exact V2 commit, imported files, OCM commit, adapter hashes, all parity outcomes, cost vector and reopened assumptions. It may not cite this package as closure of #197, #200-205, #245, or any language/frontier-mathematics milestone.

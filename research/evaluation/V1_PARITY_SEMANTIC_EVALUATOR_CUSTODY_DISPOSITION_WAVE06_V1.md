# Semantic evaluator custody — disposition (Wave 06 V1)

**Token:** `NOT_OBTAINED__DISCLOSED_LIMITATION` — not `PASS`, not `CANNOT_CHECK`.
**Machine record:** `V1_PARITY_SEMANTIC_EVALUATOR_CUSTODY_DISPOSITION_WAVE06_V1.json`
**Enforced by:** `src/orion_v2/parity_execution_gate.py`, `tests/unit/test_parity_semantic_custody_disposition.py`

## What was blocked

The frozen evaluator registry required two independent blinded semantic reviewers for PARITY-C,
two for PARITY-D, and a tiebreaker, for four cases the deterministic scorer cannot decide:
`C2`, `C3`, `D2`, `D3`. None were bound. The preflight gate had stopped at
`BLOCKED_EVALUATOR_CUSTODY` and would have stopped there indefinitely.

## What independence was actually for

Decomposed from the custody protocol, the scoring specification, the reviewer brief and the
registry's own dependence screen — four sources, not a summary of them:

| Function | Purpose | Substitutable without an external reviewer? | Status |
|---|---|---|---|
| F1 outcome-blindness | stop arm-aware scoring | yes, purely mechanical | `NOT_EXERCISED` — no adjudication happened at all |
| F2 non-self-authorship | stop the scorer inheriting the mechanism's blind spots | only where the answer key predates the subject | satisfied for the 25 deterministic cases; **not** for the four programme-authored semantic ones |
| F3 non-duplicate evaluator | make two agreeing labels a real redundancy | **no** | **not obtained** |
| F4 independent authority | — | — | **out of scope by registration** |

F4 matters most for what this is *not*. Four independent places say the slot never carried
authority: the custody protocol's `grants_independent_authority: false`, the scoring spec's
`semantic_adjudication.authority`, the brief's authority boundary, and the frozen parity case
`H2_EXTERNAL_REVIEW_NONAUTHORIZING`, which the programme scores mechanically and which would
contradict itself if reviewer binding conferred authority. Losing these reviewers therefore
costs evidence, not authority. Authority was already carved out elsewhere and is untouched.

The blocking content is F2 and F3 over four cases this programme wrote itself. Neither can be
discharged from inside it, and there is no evaluator source outside it.

## What was refused

No reviewer was recruited, simulated, role-played or generated. Same-model critique was not
counted as a second label. No slot was flipped to `bound`. The case registry's
`protected_independent_evaluator_required` stays `true`. A programme-authored mechanical oracle
was *not* bound as discharge — both campaigns carry a frozen `non_substitution_rule` that
forbids exactly that, and the instrument does not exist, has no fixture, and cannot execute
while the baseline registry is unbound. It is recorded as a named candidate route with its
unmet preconditions, not as a binding.

## What this costs, with the denominator

Recomputed from the frozen registry by test, not asserted:

- **59** frozen capability cells.
- **6** reachable only through the four semantic cases.
- **2** more (`RECONSTRUCT.ATLAS_UPDATE.v0`, `RECONSTRUCT.PORTRAIT.v0`) also touched by a
  deterministic case, but the aggregation rule is `PER_CELL_WORST_REQUIRED_CASE_NONCOMPENSATORY`
  and every registry case is required, so a deterministic PASS cannot lift them.
- **8 of 59 `CANNOT_CHECK`. 51 of 59 scorable** by the bound deterministic scorer, whose
  criterion is inherited from V1-native assertions that predate the V2 subject.

A parity run under this disposition may not report `V2_PARITY_NONINFERIOR`,
`V2_PARITY_STRICT_GAIN_WITH_NO_MANDATORY_REGRESSION` or `V1_NONINFERIOR` unqualified. Its ceiling
is a partial-surface terminal over 51 cells with 8 disclosed. Reporting "51/59 PASS" without
naming the 8 is scope laundering, not a parity result. The scoring specification itself is not
mutated; this is a constraint on what the existing frozen rules may be said to have established.

## Where the gate now stops

`BLOCKED_PARENT_BASELINE_BINDING` — because `implementation_bindings.bound` is genuinely
`false` in the baseline registry. The disposition did not open the gate; it moved the stop to a
blocker that really binds. Even with baselines bound the gate returns
`READY_WITH_DISCLOSED_EVALUATOR_CUSTODY_LIMITATION`, never the unqualified ready terminal, and
the gate fails closed if the disposition is removed, claims custody was obtained, understates the
cases it leaves unresolved, or publishes a denominator that does not add up.

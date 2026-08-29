# Wave 05 Preterminal Binding Defects

## D1 — Epoch presence without comparison

### Failure class

`DECLARED_EPOCH_NOT_COMPARED`

The transport object carried source and target epochs, but the first assessor only checked that they were nonblank. A value that is present but never compared is not a binding.

### Repair

Compare transport epochs exactly with the source and target theory epochs. Mismatch emits `INVALID_EPOCH`.

## D2 — Error collection presented as transport chain

### Failure class

`DISCONNECTED_ERROR_BOUNDS_COMPOSED`

The first chain function added the numerical errors of any tuple of links. It did not establish that the target identity/epoch of one link was the source identity/epoch of the next.

### Repair

Add source/target theory identities and epochs to every link. Fail closed unless every adjacent pair composes.

## D3 — Small distance mistaken for stable decision

### Failure class

`MODEL_DISTANCE_WITHOUT_DECISION_MARGIN`

A small transport error can reverse the selected action when competing action values are close.

### Control

A hostile case has nominal values `A=1.00`, `B=0.99`, error bound `0.02`, and observed values `A=0.98`, `B=1.00`. The terminal is `DECISION_CHANGED`, not epsilon-bounded scientific preservation.

## Verified successor

Actions run `33074185839` completed with 102 integrated tests, stochastic authority check and JSON parsing green.

## Authority

These repairs establish reference fail-closed behaviour only.
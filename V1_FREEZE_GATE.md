# ORION V1 Freeze and Non-Retroactive Handoff Gate

**Gate status:** `V1_FREEZE_HANDOFF_BOUND_AND_NON_RETROACTIVE`.

**Bound receipt:** `provenance/ORION_V1_HANDOFF_RECEIPT_V1.json`.

## Exact gate

ORION V1 is bound at freeze commit:

`8f250fc3e55d6d6a28fb1fb33d9932ef1a8760b5`

with frozen subject/base commit:

`ef51b7b9263a72c725dc9d2045627b934b772a92`

and base tree:

`5d5ff0985551b0a94453ea6eaa9925bda3e10fa2`.

The declared V1 terminal is:

`ORION_V1_ARCHITECTURE_AND_LOCAL_FORMALISM_FROZEN`.

The exact moving-head observation and all control-plane Git object identities are recorded in the machine receipt. `main` is not itself used as an immutable identifier.

## What is now authorized

- reference implementation of non-authorizing V2 research objects;
- deterministic schemas, checkers and known-answer/hostile tests;
- V1 capability-parity instrumentation;
- local prospective pilots whose own protocols are frozen before outcomes;
- continued donor research, paper protocols and falsifier design.

## What remains unauthorized

- retroactive V1 mutation or reinterpretation;
- protected external evaluation without separately bound custody/protocol;
- scientific truth, superiority or novelty terminals from local tests;
- final V2 core, framework adoption or constitution change;
- final paper identity or publication claims.

## Non-retroactivity

V1 results remain immutable external evidence. ORION-V2 additions may only create successor objects with explicit correspondence, preservation/reopening and changed-scope records.

## Machine check

```bash
python scripts/check_v1_handoff.py
```

Expected terminal:

`V1_HANDOFF_VALID`

Any mismatch reopens issue #2 and returns the repository to a fail-closed implementation gate.

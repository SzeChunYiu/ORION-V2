# Installation

ORION-V2 now permits a **non-authorizing reference package** because the exact ORION V1 architecture/local-formalism freeze handoff is bound in `provenance/ORION_V1_HANDOFF_RECEIPT_V1.json`.

The package is still pre-release research software. It does not implement the final V2 solver and does not grant scientific or novelty authority.

## Local reference environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
pytest
python scripts/check_v1_handoff.py
```

## Authorized current uses

- exact schemas and pure reference algorithms;
- known-answer and hostile tests;
- V1 capability-parity instrumentation;
- local prospective pilots after a separate frozen protocol.

## Still blocked

- protected external evaluations without bound custody;
- claims of scientific superiority or novelty;
- final solver/framework adoption;
- final V2 paper identity.

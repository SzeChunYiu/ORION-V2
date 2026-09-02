# Receipt boundaries: machine output vs. hand-written commentary

**Enforced by** `scripts/check_receipt_boundaries.py` (CI: `receipt-boundary-guard`).
**Tests** `tests/unit/test_receipt_boundaries.py`.

## Why

`research/experiments/results/issue45/pc-r6/PC_R6_OUTCOME_RECEIPT.md` appended a hand-written
addendum below an HTML comment saying everything past it was "not machine-generated". The
boundary was invisible in rendered Markdown and unreadable by any tool, so nothing distinguished
the two halves. Two figures from the hand-written half were then quoted into a paper scoping
brief as if they were analysis output:

| figure | what was wrong | truth |
|---|---|---|
| `NONE_PATCH_NOT_APPLIED` "78–83%" | paired the e30r11 minimum with the e60 maximum | **75.0%–82.5%** pooled |
| "the frozen lane already recorded (311/480 patch-apply `rc=128`)" | no result artifact under `results/issue45/e30-r11/` records patch-apply return codes, so the citation resolves to nothing (both lanes have 480 e30r11 evaluations, which is why it looked plausible) | count correct; source is **this lane's own** `PC_R6_FULLREG_RAW_ROLLUP_V1.json` |

Neither was caught until the source was re-read by hand. The second is the sharper case: its
*value* verifies and only its *citation* resolves to nothing, so arithmetic review would never
have found it.

## The convention

A receipt that appends hand-written content to generated output declares the boundary
immediately after the generated region:

```
<!-- ORION-RECEIPT-BOUNDARY-V1
generated_bytes: <N>
generated_sha256: <64 lowercase hex>
generator: <repo-relative path to the script that produced bytes [0:N]>
checked_by: scripts/check_receipt_boundaries.py
-->

> ### ⚠ HAND-WRITTEN BELOW THIS LINE — NOT MACHINE OUTPUT
> ... what the reader needs to know ...
```

Only whitespace or a horizontal rule (`---`) may sit between byte `N` and the marker.

Two properties matter, and the marker alone gives neither:

- **Verifiable** — `sha256(bytes[0:N])` must equal `generated_sha256`, so the generated half
  cannot be hand-edited without the check failing.
- **Visible** — the blockquote renders; an HTML comment does not. A reader of the rendered page
  sees the boundary, not just a reader of the source.

Every figure in the hand-written region names the artifact and field it was computed from. A
figure quoted out of that region without such a citation is unsourced.

## What CI enforces

1. Files carrying the marker: digest, marker offset, required fields, generator path, and the
   rendered banner.
2. Any `*RECEIPT*.md` that declares a boundary in prose inside an HTML comment but carries no
   canonical marker — the superseded, unverifiable style — fails.

Exit codes are distinct: `0` checked and clean, `2` violations, `3` **could not check**. "Could
not check" is never reported as "checked and fine".

## Deliberately not implemented

A repo-wide check that every figure quoted from a receipt resolves back to its machine-generated
region was considered and rejected as disproportionate: it needs a reliable figure-to-source
parser over free prose, and would produce false positives on the first real run — the failure
mode that gets a guard switched off. The boundary is now machine-checkable, which is the
precondition for that stronger check if a second receipt ever needs it.

## Adding a receipt

Compute the digest of the generated file **before** appending anything:

```bash
python - <<'PY'
import hashlib, pathlib
p = pathlib.Path("path/to/RECEIPT.md")
raw = p.read_bytes()
print("generated_bytes:", len(raw))
print("generated_sha256:", hashlib.sha256(raw).hexdigest())
PY
```

then append the marker and banner, and verify:

```bash
python scripts/check_receipt_boundaries.py path/to/RECEIPT.md
```

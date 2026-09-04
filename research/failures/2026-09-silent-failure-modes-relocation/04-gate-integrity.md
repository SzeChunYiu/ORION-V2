# 04 — Gate integrity

Detail file of `2026-09-silent-failure-modes-relocation`. Read `README.md` first.

Records here are checks that **ran, on the right file, for the right string, and could not fire** —
plus two records about the apparatus built to catch exactly that, which had the same defect.

---

## D10 — Log-wrap blindness

**Class** `CHECK_THAT_RUNS_AND_CANNOT_FIRE` · **Status** `REALISED` · **FIXED**

Reproduced directly. `pdflatex -interaction=nonstopmode` on a document citing a long missing key
wraps its log at column 79, mid-word:

```text
line 49 (79 chars): LaTeX Warning: Citation `someMissingCitationKeyThatIsQuiteLongIndeed2026' on pa
line 50 (31 chars): ge 1 undefined on input line 3.
```

`grep -nE "Citation .* undefined"` on that log returns **rc=1, 0 matches**, with `grep -c LaTeX` →
20 as a positive control. The deployed gate, run verbatim against the same log, reports **PASS**.
The check runs, on the right file, for the right string, and misses. `grep` is line-oriented and
`.*` never spans a newline; nothing about the pattern is wrong — the tool that wrote the log broke
the string in half.

Defective at PR #95's parent `1606356e` in ORION-paper:
`.github/workflows/flagship-v22-candidate-audit.yml:156`,
`.github/workflows/flagship-v23-candidate-audit.yml:166`,
`.github/workflows/v2-final-papers-v112.yml:70`.

**Wrap column re-verified 2026-09-04** against the fixtures now committed at
`scripts/check_render_gate_patterns.py`, which the file's own comment marks as *"verbatim bytes from
a real pdflatex run, not a synthesized wrap"*. Measured: the citation fixture's first physical line
is `68 + 11 = 79` characters and the reference fixture's is `69 + 10 = 79`. The break falls at that
exact column regardless of token boundaries.

**FIXED** by PR #95, merge `155429f6a103029b4e510916534532eb80fc1087`
(`/usr/bin/git merge-base --is-ancestor … origin/main` → rc=0, re-checked 2026-09-04):
`scripts/dewrap_tex_log.py`, gates scan `manuscript.dewrapped.log`, and `max_print_line=10000` is
exported.

**Correction — the blindness is site-specific to those three workflow gates, not repo-wide.** The
same log contains, unwrapped, `LaTeX Warning: There were undefined references.` Every other checker
found includes that alternative and does catch it (`verify_all_submission_materials.py:221`,
`verify_tier_b_package.py:57`, `build_tmlr_pdf.sh:40`, `verify_release.py:394`).

---

## D22 — A meta-gate that plants only unwrapped fixtures

**Class** `CHECK_THAT_RUNS_AND_CANNOT_FIRE` · **Status** `REALISED` · **FIXED**

The gate built to prove the render gates can fail had the same defect as the gates it certified.

`scripts/check_render_gate_patterns.py` (ORION-paper) runs each gate through `bash -c` against a
fixture log carrying real LaTeX defect lines, and asserts the gate catches it. Measured directly
from the historical blobs on 2026-09-04:

| commit | PR | `SITE_POLICY` entries | occurrences of `wrap` |
|---|---|---|---|
| `a43d916` | #82 | 7 | 0 |
| `ee18bb0` | #83 | 7 | 0 |
| `fbe647c` | #87 | **8** | **0** |
| `cce29e1`/`155429f` | #95 | 8 | present |

At `fbe647c` all **eight** sites were certified able to fail — against fixtures whose defect lines
are single, unwrapped, short-key strings (`` Citation `smith2020' on page 3 undefined ``). Real
pdflatex does not emit that for a realistic key; it emits D10's 79-column break. So every site read
green while the deployed gates were blind to the only form the defect actually takes.

**This is the sharpest record in the set** and it is why the repair was not merely a better regex:
correcting the pattern alone would have left the gates exactly as inert, and the meta-gate would
have kept certifying them. The fix landed both halves together — `dewrap_tex_log.py`, wrapped
fixtures taken as verbatim bytes from a real run, and two assertions that the fixtures *are* wrapped
(first line exactly `max_print_line` long; a raw line-oriented grep for the unwrapped pattern finds
nothing), so an edit that quietly unwraps a fixture is exit 2 rather than silent green.

---

## D11 — Substring-match inversion

**Class** `CHECK_THAT_RUNS_AND_CANNOT_FIRE` · **Status** `NEAR_MISS` — never on `main`, and the
named consequence was unreachable

`v2-papers/llm-machine-epistemics/venue/check_build.py` at commit `083ab27`, line 61:

```python
style_loaded = "jmlr2e.sty" in log
```

The inversion is real and was reproduced: with no style file present the log carries
``! LaTeX Error: File `jmlr2e.sty' not found.``, so `"jmlr2e.sty" in log` is **True** and the exit-3
branch is unreachable. The assertion matches the very line reporting that the file was not found,
because the failure message contains the filename. The fixed form evaluates False.

**Two corrections.**

1. **It was never on `main`.** `083ab27` lives only on `lane/llm-closure-20260903`
   (`merge-base --is-ancestor` → rc=1) and was repaired on the lane by `073e077` *before* the lane
   was squash-merged as `ecc2ab2` (PR #93), which already carries the fixed code.
2. **"A silent fallback would have passed the check" is not reachable in this build.** The same
   pre-fix file gates on a control first (lines 50-56): if `"Output written on"` is absent it
   returns 3, `COULD_NOT_CHECK`. pdflatex does not fall back to `article` for a missing
   `\usepackage` — under `nonstopmode` it fatals, producing no such line — and `build_venue.sh:28`
   does `rm -rf "$OUT"` so no stale log can supply it. The pre-fix checker would have returned 3,
   not PASS. A genuine logic inversion, correctly caught; the failure it would have licensed was
   already blocked one layer up.

---

## D23 — An interpreter version that skips a registry check

**Class** `CHECK_THAT_RUNS_AND_CANNOT_FIRE` · **Status** `CANNOT_VERIFY` as nominated — **the
briefed consequence is falsified by the same file**

The mechanism is real and was reproduced on 2026-09-04. `/usr/bin/python3` on this machine is
**3.9.6**; `zip(..., strict=True)` raises `TypeError: zip() takes no keyword arguments`. The call
sits inside a function wrapped in a bare `except Exception`:

```python
verify_all_submission_materials.py:386   for spec, record in zip(specs, registry["papers"], strict=True):
verify_all_submission_materials.py:423       global_checks = verify_global_registry(specs)
verify_all_submission_materials.py:424   except Exception as exc:
verify_all_submission_materials.py:425       global_error = str(exc)
```

**But the nominated consequence — "the entire registry check passes without running" — is false.**
Line 433 of the same file consumes the swallowed error:

```python
aggregate = "PASS" if global_error is None and len(papers) == 25 and all(...) else "FAIL"
```

so a `TypeError` from the wrong interpreter produces `aggregate = "FAIL"`, not a vacuous pass. Both
versions of this file in history carry that expression (checked at `1241e08` and `9e3580f`; the
grep returns 1 at each). The committed `VERIFICATION_REPORT.json` records `"global_error": null`
with all four `global_checks` present, so the recorded run executed the registry check under a
Python ≥ 3.10.

**What survives, stated at its real strength.** Four named global checks —
`registry_exact_25`, `route_matrix_exact_25`, `canonical_personal_information`,
`upstream_base_reconciliation` — are silently *not performed* under the platform default
interpreter, and the resulting failure is indistinguishable in `aggregate` from a genuine registry
mismatch; only the `global_error` string separates "could not check" from "checked and failed".
That is a `CANNOT_CHECK`-versus-`FAIL` conflation, not a false pass. **Recorded as a correction to
the nomination, and as the reason the nomination should not be repeated.**

---

## D24 — A vacuous loop: a filter that skips every assertion

**Class** `CHECK_THAT_RUNS_AND_CANNOT_FIRE` · **Status** mechanism verified by re-execution;
**no realised instance found**

A test whose loop `continue`s past every non-matching case runs to completion and reports success
when the filter matches everything, because nothing ever reaches the assertion. Verified by direct
re-execution on 2026-09-04 (`/usr/bin/python3`, standalone, four cells):

```text
unguarded / real filter   -> exit 0
unguarded / filter matches everything -> exit 0     <- the defect: nothing asserted, still green
guarded   / real filter   -> exit 0
guarded   / filter matches everything -> exit 1     <- the counter fires
```

The guard is a counter asserted against its expected value. The programme already writes it:
`tests/unit/test_fg70_exact_study.py:238-247` opens `checked = 0`, increments past the `continue`,
and closes `assert checked == 4`. That guard is present in the file's **first** commit (`0562e9f`),
so FG70 is the guarded exemplar, not a defect record.

**No realised instance is claimed.** A heuristic scan of `tests/unit/*.py` for `continue` loops
lacking a counter returned 16 candidates, but the scan was not validated against known-good cases
and its output visibly includes false positives — several hits are the denominator guards
themselves (`test_every_gate_reports_the_number_of_instances_it_evaluated`). Per the programme's own
rule that a checker must be validated before its findings are reported, **that list is not
reported as findings**, and this record claims only the mechanism and the guard.

---

## D12 — "A no-op mutation makes a gate probe report PASS"

**Status** `CANNOT_VERIFY` — no realised instance, and the polarity is inverted in the one real
artifact

The general principle is well documented in this repository; **an instance is not.** Two artifacts
exist and neither is the claimed one.

**Opposite polarity.** `v1-papers/orion-25-orion-research-harness/experiments/execution-integrity-v1/fault_inject.py:141-143`:
*"A mutation must actually change the bytes. Setting a field to the value it already holds is a
no-op that a naive harness scores as 'undetected', which is a false positive in the harness, not a
finding about the system."* Here a no-op yields `detected: False` → exit 2 → a false **RED**, not a
false pass.

**Right polarity, but prophylactic and about a fixture.** `scripts/check_render_gate_patterns.py:335-341`
is the literal source of the nominated sentence — *"'the gate passed' and 'the gate never saw the
defect' are indistinguishable without them"* — but that guard and the wrapped fixtures it guards
**landed in the same commit** (`cce29e1` → `155429f`, PR #95), verified by reading the three prior
blobs. No version ever shipped where an unwrapped fixture produced a silent green. (D22 records what
*did* ship at those commits, which is a different defect: fixtures that were unwrapped by design and
never guarded, because the wrapped form had not yet been discovered.)

Searched: both repositories, all files, `mutation|mutant|planted|tamper` × `no-op|noop|unchanged|did
not change|applied|identical`; `git log --all --grep` for `no-op`, `mutation`, `never saw the
defect`; the ME-X6 mutant-survival receipt; `mex7_generator.py` self-tests.

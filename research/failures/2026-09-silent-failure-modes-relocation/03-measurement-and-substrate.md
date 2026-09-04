# 03 — Measurement and substrate

Detail file of `2026-09-silent-failure-modes-relocation`. Read `README.md` first.

Records here concern **what a run was actually executed against** — which model, which corpus,
which toolchain — as distinct from what its custody record says it was executed against. In every
case the custody record is honest and still insufficient.

---

## D7 — Pinning a served model id does not pin an experimental condition (E30-R12)

**Class** `UNPINNED_SUBSTRATE_CONDITION` · **Status** `REALISED`, filed as could-not-check

`research/experiments/e30-r12/results/E30_R12_EXECUTION_LANE_TALLY_V1.json`:
`"envelopes_written": 119`, `"served_model_ids": {"glm-5.3": 119}`. The terminal: *"all 119
envelopes record exactly one served model id, glm-5.3, equal to the frozen value. GR0c's condition
was met by every envelope written."* The campaign failed anyway:
`"evaluations": {"expected": 480, "produced": 0}`, `"gates_evaluated": []`, `"endpoints_read": []`,
`"status": "EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ"`, `"registered_terminal_reached": null`.

The same frozen prompt — identical `"input_tokens": 61557` — completed in `"output_tokens": 763` on
2026-08-29 and hit the primary cap on re-run:
`"output_tokens_at_or_above_primary_cap_6000": 116`. The channel probe records
`{"max_tokens": 6000, "stop_reason": "max_tokens", "output_tokens": 6000, "content_blocks":
[{"type": "thinking", "chars": 27624}], "text_chars": 0}`, and `scripts/orion_claude_arms.py:261`
parses only `text` keys — so the entire budget went to a block the arm never reads.

**The class is the point.** A served-id pin certifies *identity* and says nothing about *behaviour*.
Everything the guard was designed to catch was absent, and the condition still changed underneath a
frozen prompt.

**Correction:** `763` is attested solely by the R12 tally. The R11 envelope is not in the repository
and the R11 archive records no served model id at all (`grep -rln "served_model"` over the R11
directory returns nothing), so R11's model is **inferred, not verified** — which is itself what
`SILENT_MODEL_SUBSTITUTION`'s guard exists to prevent.

**Related, already classed.** Requesting one model and receiving another at HTTP 200 with no warning
is the existing ledger class `SILENT_MODEL_SUBSTITUTION`, first observed 2026-09-02. The admission
assessment §2 corrects its count: **three** substitutions across four probes, not two —
`glm-5.2`→`glm-5.3`, `glm-5.1`→`glm-5.3`, `glm-4.6`→`glm-5.3-flash`, with `glm-5.3`→`glm-5.3` as
the negative control. That correction is carried into `FAILURE_LEDGER.md`.

---

## D8 — A checker staged against the wrong corpus (ME-X3)

**Class** `CHECKER_STAGED_ON_THE_WRONG_SUBSTRATE` · **Status** `NEAR_MISS`, guarded by an executed
check

**Premise true, nominated wording wrong.** The cross-check directory `lean/` (untracked,
gitignored) holds **20 task_ids, all in DEVELOPMENT, 0 in PROTECTED**, disjoint from the protected
receipt's ids. But two argument defaults are independent:

```python
mex3_lean.py:187   ap.add_argument("--dir",    type=Path, default=HERE / "lean")
mex3_lean.py:205   ap.add_argument("--report", type=Path, default=None)
mex3_lean.py:207   (a.report or (a.dir / "LEAN_RECEIPT.json")).write_text(txt)
```

**Pure defaults write to `lean/LEAN_RECEIPT.json`, a path no receipt reads** —
`make_outcome_receipt.py:20` reads `results/ME_X3_LEAN_RECEIPT_PROTECTED_V1.json`, and read that
same path at the pre-fix commit `95d67dd` too. The real contamination path needs the default `--dir`
**plus** an explicit `--report` pinned to the protected slot. The merged receipt §8 states the
accurate, weaker version.

**A second finding inside the first: the fix commit's own message overstates against its own tree.**
It says the defect *"would put development numbers at the path the receipt generator originally
read"*; no commit exists in which the generator read the default path.

**Near-miss.** No `LEAN_RECEIPT.json` exists in `lean/` or `lean-protected/`; the protected build ran
in a separate directory with `--report` pinned. The protected receipt is uncontaminated: 40 rows,
`Counter({'VERIFIED_BY_LEAN_KERNEL': 20, 'REJECTED_FOR_THE_REGISTERED_REASON': 20})`,
`"disagreements": 0`. Receipt §11: *"the pre-existing `lean/` directory held the development corpus
and was not reused."* The guard is now executed — `verify_receipt_claims.py:201-207` emits
`registered_default_lean_path_is_not_stale | PASS | lean/LEAN_RECEIPT.json absent … | creating that
file would flip this check to FAIL`.

---

## D9 — A toolchain shim with no default toolchain (ME-X3)

**Class** `CHECKER_STAGED_ON_THE_WRONG_SUBSTRATE` · **Status** `NEAR_MISS`, **reconstructed, and
unattested by any artifact**

`mex3_lean.py:189` defaults `--lean` to the bare name `lean`. On the machine that ran the protected
check, `/opt/homebrew/bin/lean --version` exits 1 with *"error: no default toolchain configured"*.
Executing `classify()` against that exact stderr yields `REJECTED_UNEXPECTEDLY` for every
expected-accept file, so a 20-accept/20-reject plan produces 20 fabricated disagreements. The
arithmetic is correct.

**Two corrections that change what this is.**

1. **It omits the other half.** The 20 expected-reject files become `CANNOT_CHECK`, not false
   rejections: 0 accepted, 0 registered rejections, 20 `CANNOT_CHECK`, 20 disagreements.
2. **This defect is fail-loud, not silent.** `agrees_with_exhaustive_oracle` flips to `False`,
   `main()` exits 1, and `verify_receipt_claims.py` reports `lean_crosscheck_on_protected_corpus`
   as **FAIL**. In a register of *silent* failure modes it must be labelled as the loud kind. It is
   retained because the staging error is the same one as D8, not because the failure is silent.

**Unattested.** The protected run did not use the default: it records
`"lean_binary": "elan toolchain leanprover/lean4:v4.33.1"` with
`"version_string_observed": "Lean (version 4.33.1, arm64-apple-darwin24.6.0, …)"`. **No artifact
anywhere records this defect** — searched all tracked files for `fabricated|no default
toolchain|toolchain shim|elan run|PATH shim` with `REJECTED_UNEXPECTEDLY` as a positive control;
`git log --all --grep` for `toolchain`, `shim`, `elan`; PR #229's body, comments and both underlying
commits. The word "shim" does not appear in the repository. The counterfactual is reconstructed from
code plus **present** machine state; that the shim was actually hit is not attested.

# PR merge gate: five fields, three exit codes

`scripts/pr_merge_gate.py` is the merge decision. Run it before every merge
and merge only on exit 0.

```
python scripts/pr_merge_gate.py --pr N --repo SzeChunYiu/ORION-V2 --git-dir .
```

| field | condition | incident that put it here |
|---|---|---|
| 1 | `state == OPEN` | -- |
| 2 | `mergeable == MERGEABLE` (`UNKNOWN` is polled `--polls` times, then exit 2; never pass or fail) | -- |
| 3 | `isDraft == false` | #244 and #254 sat green and unmergeable for an hour; the gate never asked |
| 4 | every check `COMPLETED` with conclusion in `{SUCCESS, NEUTRAL, SKIPPED}`, zero incomplete; a `NEUTRAL` is printed as **NOT ASSESSED**, never as a pass | review-bot neutral read as green |
| 5 | no changed path is pinned by digest by a live binder on `main` as it is *now* (`*FREEZE*.json`, `SHA256SUMS`, `PACKAGE_MANIFEST*.json`, `*_EXPECTED_CUSTODY*.json`, any JSON carrying a `*sha256*` field) | #282 froze `ME_F1_R3_FREEZE_V1.json` binding `me-f1/mef1_arms.py`; #276 changed that file 70 min later; both green alone; `main` red for hours on `test_frozen_state_if_present_matches_inputs` |

Exit codes: `0` all five hold; `1` a field fails (the output names which); `2`
could not check (API unreadable, `mergeable` still `UNKNOWN`, no checks
reported, freeze scan could not run, or its must-match grep control did not
match). 2 is never folded into 0 or 1.

Field 5 refuses on two kinds of evidence: `DIGEST` (the sha256 of the file's
content on `main` appears in a binder) and `NAME_PIN` (the path is named
beside a digest). A binder the same PR updates to the new content's digest is
reported as `rebound in this PR` and does not refuse. The refusal names the
binder and its owner (last commit touching it on `main`).

Replay from history (field 5 only):

```
python scripts/pr_merge_gate.py --replay --git-dir . --base-ref d696d74 --head-ref dc27ced
```

refuses #276 against the #282 freeze; `tests/unit/test_pr_merge_gate.py`
pins that replay and a mutation per field.

## Enforcement status: policy, with partial workflow coverage

`main` has no branch protection. `.github/workflows/pr-merge-gate.yml` runs
the self-test, the mutation tests and a field-5 scan of the PR against `main`
as it stands when the run starts. That catches a freeze already on `main`; it
cannot catch the #282/#276 pair, where the freeze landed after the PR's run.
Fields 1-4 and the merge-time field-5 re-scan are therefore **policy**: the
person or lane merging runs the gate and merges on exit 0 only. Say so in the
PR body ("merge gate: exit 0 at <base sha>") rather than reporting the workflow
as enforcement.

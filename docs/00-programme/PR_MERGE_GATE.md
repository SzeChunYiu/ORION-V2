# Merge gate: six fields (0–5), three exits

`scripts/pr_merge_gate.py` decides whether a PR may be merged. It is **policy at
merge time** (the person or lane merging runs it and acts on the exit code) plus
**partial enforcement in CI** (`.github/workflows/pr-merge-gate.yml` runs field 5
and the self-test on every `pull_request`). Fields 1–4 cannot be enforced by a
workflow on this repository: there is no required-checks branch protection, so
`gh pr merge` succeeds regardless of any check.

```
python3.12 scripts/pr_merge_gate.py --pr N --repo SzeChunYiu/ORION-V2 --git-dir <clone>
echo $?      # 0 merge; 1 refuse (a field is named); 2 could not check (never merge on 2)
```

| # | field | fails when | incident |
|---|---|---|---|
| **0** | `baseRefName == default branch` (read from the API, never assumed) — **checked first** | the PR targets any other branch: "PR base is X: retarget to main before gating (stacked PR whose base already landed?)"; default unreadable → 2 | #290 passed fields 1–5 and merged onto the #289 branch as `54712cc0`, not an ancestor of main — the **FM40 stranding class recurring** (#187 → integration branch, recovered by #215). For information the gate prints whether the base still exists and whether its tip is already an ancestor of the default |
| 1 | `state == OPEN` | merged/closed | `MERGED` is not evidence anything reached main (see field 0) |
| 2 | `mergeable == MERGEABLE` | `CONFLICTING`; `UNKNOWN` is polled, then exit 2 | — |
| 3 | `isDraft == false` | draft | #244/#254 sat green and unmergeable for an hour |
| 4 | every check `COMPLETED` with conclusion in `{SUCCESS, NEUTRAL, SKIPPED}` | `FAILURE`/`TIMED_OUT`/`ACTION_REQUIRED`/`STARTUP_FAILURE` → 1; **`CANCELLED` or not `COMPLETED` → 2** | review-bot `NEUTRAL` gave two false greens in one day → surfaced as **NOT ASSESSED**; three PRs read red on cap-killed runs → **could not check, re-run the workflow on this head** |
| 5 | no changed path is pinned by digest in a live freeze on the base | a freeze-class binder on the base holds the base content's digest of a changed path and the PR does not rebind it | #282 froze `mef1_arms.py`; #276 changed it 70 min later; both green; main red for hours; repaired by #286 |

## Field 0: the base branch is read, not assumed

A stacked PR keeps its base after that base lands; `gh pr merge` then merges
into the stale branch and reports `MERGED`. `--snapshot FILE --default-branch X`
evaluates fields 0–4 from a saved `gh pr view --json` record, which is how the
#290 pre-merge state is replayed in the tests (refused on field 0 alone; #296,
the cherry-pick reland onto main, and #289 pass).

## Field 4: three states, and where the detail comes from

A cancelled run is not evidence about the code. On 2026-09-04 every cancelled
job in the last 25 runs of the full-suite workflows died at 10.0–10.2 min with
the pytest step cancelled and **no failed step** — a job cap, sized below the
suite's p95 (#292 resizes them). The gate names the cancelled check, reads the
job from the **jobs API** (`gh api repos/O/R/actions/jobs/<id>`: step
conclusions, wall time) and prints the advice. It never reads
`gh run view --log-failed`: that is empty on a cancelled run by design (no step
failed) and printed 0 bytes on three genuinely failing runs the same day.

A `pull_request` checkout is `refs/pull/N/merge`, so a fix already on `main`
(a raised cap, a repaired freeze) is included in a re-run without a rebase.

## Field 5: binder classes and what is refused

The scan reads the base ref **as it is now** (fetched fresh) and reports the
SHA it measured at. It collects every binder on the base — `*FREEZE*.json`,
`SHA256SUMS`, `PACKAGE_MANIFEST*.json`, `*EXPECTED_CUSTODY*.json`, and any JSON
carrying a `*sha256*` key (253 on `main@b53dba5`) — arms a must-match grep
control (a known digest must be found, or the scan is exit 2), then looks for
each changed path by name and by the base content's digest.

| class | example | current binding to a changed path |
|---|---|---|
| **freeze-class** (basename pattern) | `ME_F1_R3_FREEZE_V1.json` | **REFUSE** unless the PR rebinds it coherently (the binder in the PR head carries the new content's digest) |
| provenance-class (any other `*sha256*` JSON) | `ME_F1_CALIBRATION_RECEIPT.json` | surfaced, not refused (`--strict` refuses). On `main` these receipts already name a digest of `mef1_arms.py` that `main` no longer has, and `main` is green: they record what a run saw; they do not pin |
| either, already stale on the base | a superseded freeze | surfaced, not refused: this PR cannot make it worse |

The empty-file digest `e3b0c442…` binds nothing.

### Replay of the incident (`--replay --base-ref d696d74 --head-ref dc27ced`)

`d696d74` is `main` immediately before #276 merged; it holds #282's freeze.
The gate refuses: `mef1_arms.py` and `ME_F1_SOURCE_MANIFEST_V1.json` are pinned by
`research/experiments/me-f1-r3/results/ME_F1_R3_FREEZE_V1.json` at
`v1_arms_py_sha256` / `v1_source_manifest_sha256`, owner `538e017 #282`. The four
receipt hits are reported as provenance. The no-alarm control, #289
(`d1dfd12..b53dba5`, one new file), passes. Both replays are pytest cases and
run wherever the history is present (`PR_MERGE_GATE_REQUIRE_HISTORY=1` makes a
shallow clone fail instead of skip).

## Could-not-check is its own exit

Exit 2 is raised for: API unreadable, `mergeable` still `UNKNOWN` after the
polls, zero checks reported (waive with `--allow-no-checks`), a cancelled or
running check, an unreadable base ref, no binders on the base (waive with
`--allow-no-binders`), the grep control not matching, or a binder that is not
readable JSON. A definite failure elsewhere still exits 1 (the merge is refused
either way) and the report shows both.

`--self-test` runs the mutation table (every field 0–5 made to fail, every
could-not-check kept distinct) and exits 2 if any row disagrees.

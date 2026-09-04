# 05 — Operational tooling and version control

Detail file of `2026-09-silent-failure-modes-relocation`. Read `README.md` first.

**These are operational hazards, not scientific failure classes, and they are deliberately kept
apart from `01`-`04`.** The admission assessment §3 warns against *"bundling unlike things because
each was surprising"* and rules one such item *"an operational hazard, not a silent verification
failure"*; §9 rules a CI string-matching bug *"repository hygiene, not a scientific claim."* Applying
that reasoning here: every record below is a property of `git`, `gh`, a shell pipe or a command
proxy. They are recorded because each one, misread, authorises a destructive or a wrong action —
not because they belong to a taxonomy of scientific defects. **No new failure-ledger class is minted
for this group.**

They do share the direction that organises the rest of the record: each fails toward a confident
reading — *nothing changed*, *it merged*, *the suite is green* — that a careful reader has no
signal to distrust.

---

## D13 — Post-merge validation gap

**Status** `REALISED` · **FIXED for the integrated suite**

At PR #230's parent `cd30f31a`, parsed from each blob directly: **22 workflow files, 4 with a
`push:` trigger including `main`** — `e30-r12-lane.yml`, `patch-emission-interface.yml`,
`pc-r6-fullreg-lane.yml`, `receipt-boundary-guard.yml`. 18 were pull-request-only. Branch protection
confirmed absent independently: `gh api repos/SzeChunYiu/ORION-V2/branches/main/protection` → 404
*"Branch not protected"*.

**The realised instance.** PR #229 merged at `2026-09-03T00:37:22Z`; its `foundation-reference` run
completed at `00:43:47`. Check-runs on the merge commit `34ecfc0a` carry **`receipt-boundaries`
only** — no integrated-suite verdict exists for the commit that landed on `main`.

**Correction:** the PR body says *"The PR's run never completed."* It did complete, 6m25s after the
merge, green, **on the PR head** — not on the merge result. The structural point holds; the wording
does not.

**FIXED** by PR #230, merge `7ae422075a782cbee743fe0eaac176c81dbab08b`. Re-verified 2026-09-04:
`/usr/bin/git merge-base --is-ancestor 7ae4220… origin/main` → rc=0, and
`.github/workflows/wave6-foundation-synthesis.yml` on `origin/main` now carries
`push: branches: - "main"`. Current `origin/main` measures **23 workflows, 6 with `push:main`**.

**Second correction:** that closes the hole for **1 of the 18** pull-request-only workflows; the
others were deliberately left so. The gap is narrowed to the integrated suite, not closed
portfolio-wide.

---

## D14 — A PR reading `state: MERGED` whose work is absent from `main`

**Status** `REALISED`, recovered in ~21 minutes

```text
PR #173  merged research/fm-formal-transfer-mechanics-20260902 → main   2026-09-02T21:28:42Z
PR #187  merged research/fm40-invariance-20260902 → that same branch    2026-09-02T23:36:43Z
```

FM40 was merged **into an integration branch whose own PR to `main` had already landed two hours
earlier**, leaving it on no path to `main`. PR #187 reads `state: MERGED`. The decisive test,
re-executed 2026-09-04:

```text
/usr/bin/git merge-base --is-ancestor faf7b0d2014afb41542ffb55794484a576b334b2 origin/main  → 1
/usr/bin/git merge-base --is-ancestor 323894f1a2c51d347fe54eb3914a200f6f72f97d origin/main  → 0   (control)
```

**Correction: 12 files, not 10.** Recovered by PR #215, merged `2026-09-02T23:57:14Z`, whose title
records the mechanism verbatim: *"fm40: land the stranded invariance/equivariance exact study on
main (#187 merged to the integration branch, never to main)"*.

**The lesson is the test, not the incident:** `baseRefName == "main"` must never be assumed, and
`state: MERGED` is not evidence that anything reached `main`.

---

## D15 — `--delete-branch` closes every PR stacked on the deleted branch

**Status** `REALISED`

| PR | head | base | event |
|---|---|---|---|
| #190 | `research/fm20-protected-20260902` | `main` | merged `fd1cf5760e13` **23:36:50Z**; `head_ref_deleted` **23:36:53Z** |
| #193 | `research/fm70-fm80-disposition-20260903` | `research/fm20-protected-20260902` | `base_ref_deleted` **23:36:52Z** → `closed` **23:36:53Z** |
| #216 | `research/fm70-fm80-disposition-relanded-20260903` | `main` | merged `6bf4550f6597` **2026-09-03T00:11:34Z** |

One second between the base deletion and the close. No `reopened` event exists in #193's timeline.
`git ls-remote --heads origin` returns 0 hits for the base branch against 1 for a live control.

**Evidence grade, stated precisely.** The cascade close is proven by API timeline events. That
`gh pr reopen` **refused** rests solely on the actor's contemporaneous first-party account in PR
#216's body — *"GitHub refuses to reopen a PR whose base branch no longer exists"* — because GitHub
timelines do not record failed API calls, so no captured error string exists. **The
irreversibility claim is therefore first-party testimony, not an artifact.** Recovery by a new PR is
independently proven: #216 carries the same head commit `996e1873282766bb0c3a5915ff3c50fb7717f03f`
and merged 35 minutes later.

**Negative control on this finding.** A superficially identical cascade — PRs #11, #12, #26, #29,
#30, #32, #34, closed in 44 seconds on 2026-08-27, all with stacked non-`main` bases — is **not** an
instance: their timelines show plain `closed` events with no `base_ref_deleted`, and their branches
were deleted two days later in a bulk sweep. Those were closed by hand.

**Not free.** #216's body records a merge conflict in
`research/experiments/FORMALISM_GENESIS_BACKLOG_V1.json` — the file recording protected-run status —
resolved to `main`'s version because #192 had meanwhile landed FG70 as `EXECUTED_PROTECTED`.

---

## D16 — Squash-merge makes landed work look unlanded

**Status** mechanism verified in-session

PR #238 was squash-merged to `main`. Two mutually confirming signals say the opposite:

```text
/usr/bin/git merge-base --is-ancestor 6ee998be82c6 origin/main    → 0     (it IS on main)
/usr/bin/git cherry origin/main refs/remotes/pr/238
  + c97cfe35a30654e3bcb60dcf9fff013aab15374c
  + 59a0dd07b83958f6340a9c88100f9536883a8818                      (both marked NOT upstream)
```

The sound test is a tree-hash comparison for the path:

```text
pr/238     :research/experiments/fm-exact/fm40/results → 7e797f6cacb83659bd5656600a0463c2dc71311a
origin/main:research/experiments/fm-exact/fm40/results → 7e797f6cacb83659bd5656600a0463c2dc71311a
```

**Scope note.** `git cherry` is not universally blind here: on the single-commit PR #215 it correctly
marked the commit `-` (already upstream). The failure appears once several commits are squashed into
one, so no individual patch-id matches. Record it as conditional on multi-commit squashes, not as a
general property of `git cherry`.

---

## D25 — A three-dot diff shows one side only

**Status** mechanism verified by re-execution; **the nominated incident is `CANNOT_VERIFY` and its
direction is inverted**

Re-executed in a scratch repository on 2026-09-04. `main` adds 300 lines; `side` deletes 10:

```text
/usr/bin/git diff --numstat main..side    → 0   310   f.txt
/usr/bin/git diff --numstat main...side   → 0    10   f.txt
```

`A...B` diffs from `merge-base(A,B)` to `B`, so it reports **only B's own changes**. `A..B` compares
the two tips and folds A's additions into B's column as deletions.

**Correction, and it matters because the nomination would teach the wrong habit.** The nominated
form — *"a three-dot diff shows one side only, and misreading one produced a report of ~2,480
phantom deletions"* — has the hazard backwards. Three-dot is the form that **isolates** a side;
**two-dot** is the form that manufactures apparent deletions out of the other side's additions, 300
of the 310 above. A stale branch compared two-dot against an advanced `main` is exactly how a large
phantom-deletion count arises.

**The incident is unattested.** Searched both repositories for `phantom deletion`, `three-dot`,
`three dot`, `2,480` and `2480` — `git log --all -i --grep` over messages and bodies, and `git grep`
across every `refs/remotes/origin` ref. The one hit is a false positive: ORION-paper `ba7a084`
contains *"phantom instance: 1 bit, zero one-step regret"*, an unrelated PRA construct. Controls
matched in both repositories (338 `*.md` files containing `ORION` in ORION-V2; the `render gate`
commit subjects in ORION-paper), so the searches were live.

**The closest attested instance of the same hazard is D17's near-miss,** where a stale integration
branch was measured at *"~91k deletions"* against `main` and retargeted rather than merged.

---

## D17 — A stale shared checkout reverting fixes that closed earlier holes

**Status** `CANNOT_VERIFY` as stated — a concrete **near-miss** is evidenced instead

No realised instance was found. Searched: `git log origin/main --name-status -m --first-parent`
(positive control 2412 lines; **`D`-status lines = 0**); all 179 PR bodies; all 384 `main` commit
subjects; repo-wide prose grep; all four pre-existing `research/failures/` records. **Scope limit
stated honestly:** `D = 0` rules out deletion-shaped reverts only. The claimed mechanism — a stale
base restoring older content — would appear as `M`, and that path was not exhaustively closed.

**The evidenced near-miss.** PR #215's body: *"The integration branch is 22 commits behind main, so
merging it directly would delete FG70, e30-r12, e40-matched and the M-grounding audit (~91k
deletions). The cherry-pick avoids that entirely."* PRs #189 and #191 carry the same warning, and
the retarget is not merely prose — `base_ref_changed` timeline events fire on #189 at
`2026-09-02T23:57:50Z` and #191 at `23:59:12Z`, before both merged to `main`. Verified on
`origin/main` (control `zzz-nonexistent-lane` → 0): `fg70` 12 paths, `e30-r12` 26, `e40-matched` 73,
`fm40` 10, and the M-grounding audit present. **Nothing was lost.**

**The closest realised thing is a different mechanism.** Commit `bbc0b03843f5`: *"#227 merged while
this revision was still in flight, so five corrections that were prepared against it did not land.
No protected outcome exists, so the design's own no-rescue clause is not engaged."* That matches the
first half — a stale head, fixes absent — but not the second: the holes had never been closed on
`main`, so nothing was re-opened.

---

## D18 — A rendered or filtered surface substituted for the fact

**Status** `REALISED` (D18b), mechanism verified in-session (D18a)

**D18a — the `rtk` command proxy, reproduced in session.** Against `FAILURE_LEDGER.md`
(11,239 characters / 11,323 bytes at the time):

```text
/usr/bin/wc -c FAILURE_LEDGER.md      → 11323           ground truth
wc -c < FAILURE_LEDGER.md             → 0               a zero on a non-empty file
/usr/bin/grep -c 'DONOR' …            → 2               ground truth
grep -c 'DONOR' …                     → "2 matches in 1F:" plus a formatted excerpt
```

The bare command name is intercepted and its machine-readable output replaced — by `0` in the first
case, and in the second by a human-readable rendering in which the requested `-c` count is simply
absent. A false "nothing there" is what authorises a destructive overwrite, and issue bodies have no
server-side history.

**Correction — two nominated numbers did not reproduce and are dropped.** A bare `diff` on files
differing by 119 lines reported `+119 added, -119 removed` correctly, and reported
`[ok] Files are identical` on a control pair. The nominated *"diff reported 0 lines changed on files
differing by 119 lines"* and *"`grep -c` returned 0 on a 26 KB file"* are **not** supported by
anything reproduced here; only the two behaviours quoted above are.

**D18b — a pipe masking a test suite's exit status.** Evidenced with a named SHA pair 35 seconds
apart on `research/me-x6-prerun-freeze-correction-20260903`: `49dbc305b2f2`
(`2026-09-03T01:07:32Z`, the broken test) → `c406185f49ce` (`01:08:07Z`, the fix), whose message
records it: *"Noting the process failure that let the bad test through: pytest was piped to tail, so
the shell reported tail's exit status and a red suite looked green. Exit status read directly from
here on."* Receipted on `origin/main` at
`research/experiments/me-x6/ME_X6_OUTCOME_RECEIPT.md:259-261`. **The broken test never reached
`main`** — both commits squashed into `96f5c8de` (PR #232) — and no piped `pytest` invocation exists
on `origin/main` today (`git grep -nE 'pytest[^|]*\|[[:space:]]*(tail|head)'` → rc=1, against 133
files matching `pytest` as a positive control).

**The direction matters and completes the group.** D18a and D18b fail toward apparent **strength**
(nothing changed, suite green). The admission assessment records the other direction from the same
session: `gh run list` rendered in-progress runs as `[time]`, which read as "timed out" would have
prompted weakening a test suite that was never failing. So the detector is symmetric — before acting
on a summary, execute the thing it summarises, and ask both what would have to run for this to be
false **and** what would have to run for it to be true.

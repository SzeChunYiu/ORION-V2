# ME-F1 R3 — pre-outcome correction R1: the freeze binding, re-scoped to what the run consumes

```text
OUTCOME_EXISTS                = NO  (dispatcher deferred; no R3 model call has been made)
DESIGN / GATES / SEED / ENVELOPE / ROUTING = UNCHANGED  (design twin sha256 813e9fba… unchanged)
WHAT_MOVED                    = the freeze's input binding only
```

## 1. What happened

Freeze V1 (`ME_F1_R3_FREEZE_V1.json`, ORION-V2 #282 → `538e017e`, 13:44) bound the **whole** of
`me-f1/mef1_arms.py` by sha256 and asserted it at `run`/`evaluate`. ORION-V2 #276 (`dc27ced`,
14:54) then landed the B5 prompt/code parity repair, which edits that file. The freeze's
`test_frozen_state_if_present_matches_inputs` went red on `origin/main` at `3d28db4` and
`wave6-foundation-synthesis` with it. The merger did not run the freeze check before merging over
its input; this lane did not bind the freeze to a commit. Both halves are recorded in
`FAILURE_LEDGER.md` under the staleness variant of `REPAIR_DOCUMENTED_NOT_LANDED`.

## 2. Diff-scoped control — what #276 changed, and whether R3 runs any of it

Per-arm sha256 of every `_ARM_CONTROL` text, computed from the file at `538e017e` (pre-#276) and
at `origin/main` `3d28db4` (post-#276), via `subprocess` reads of `git show` (never a shell loop):

| arm | pre-#276 | post-#276 | R3 runs it? |
|---|---|---|---|
| `SIMPLE_DIRECT` | `e61f97ae` | `e61f97ae` | **yes** — unchanged |
| `M_ME_FRONTIER_CONTROL` | `8f4b6a96` | `8f4b6a96` | **yes** — unchanged |
| `M_MINUS_MINIMUM_ESCALATION` | `02c72dc9` | `02c72dc9` | **yes** — unchanged |
| `M_MINUS_WARRANT_GATE` | `bb7f3890` | `bb7f3890` | **yes** — unchanged |
| `M_MINUS_LOCUS_DIAGNOSIS` | `3dcf90f8` | `3dcf90f8` | **yes** — unchanged |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | `40e96181` | `2b9d589c` | no |
| the other five registered texts | same | same | no |

Exactly one text changed, and it belongs to an arm this design never dispatches (`ARMS` in the
runner; the selftest asserts B5 is absent from the binding). The diff is one hunk
(`@@ -134,6 +134,11 @@`, B5's control text). **Nothing R3 runs moved.**

## 3. The correction

Option chosen: **re-freeze against post-#276 `main`, binding what the run consumes.**
`ME_F1_R3_FREEZE_V1.json` is now `orion.v2.me-f1-r3.freeze.v2`:

- `arm_text_sha256` — the five dispatched control texts, **asserted** at `run`/`evaluate`
  (`_assert_frozen`), and asserted by the unit test against the live V1 table;
- `v1_arms_py_sha256` and `v1_tree_commit` (`3d28db4`) — **recorded** for provenance, not asserted;
- `pre_outcome_correction_r1` — this record, inside the freeze, with the empty list
  `arms_this_design_runs_changed_by_pr276: []`.

The assertion is not weakened: it moves from a proxy (the file) to the object (each text the arm
receives), and it is shown failable — `test_freeze_assertion_can_fail_on_a_dispatched_arm_text`
plants a foreign sha for `SIMPLE_DIRECT` and `_assert_frozen` refuses. A later merge that changes
an arm R3 runs still stops the dispatch; a merge that changes an arm it does not run no longer
does. Design twin, gates, seed, instrument envelope, routing, calibration binding: unchanged
(`design_json_sha256` identical before and after).

Rejected: keeping the file binding and pinning to a commit. That would have made the deferred
dispatcher's tree the authority over the freeze rather than the freeze over the tree, and would
have left B5's text — irrelevant to R3 — in the binding for no reason the design states.

## 4. The execution host

The deferred dispatcher (`~/sd10run/mef1_r3_deferred_dispatch.sh`, billy-old, pid 1766474) runs
`mef1r3_ablation.py run` from `~/sd10run/ORION-V2-ctrl` **at whatever commit that worktree is
checked out to** — at the time of this correction, `56cd51e` (pre-#276 file). A re-freeze on
`main` that the dispatcher never saw would be exactly the `REPAIR_DOCUMENTED_NOT_LANDED` shape,
so the worktree is moved to the merge commit of this correction before the dispatcher's window
opens, and the move is verified there by: `_assert_frozen()` passing on that tree, the FG80 R3
frozen suite still byte-identical (`cmp` exit 0 against the committed `FG80_R3_FROZEN_SUITE_V1.json`),
and both dispatcher pids alive. The verification is appended to this record once done (§5).

## 5. Execution-host verification

(appended after the merge; see the commit that lands this file for the pre-merge state)

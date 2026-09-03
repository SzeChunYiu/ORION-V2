# ME-F1 — Parent fidelity and development-split receipt (V1)

**Status:** development only. `PROTECTED_RUN_AUTHORIZATION.json` is **absent**; the `protected` stage
refuses (exit 3 without authorization, exit 4 without a matching custody seed), and a unit test asserts
the refusal path. **No protected campaign exists. Nothing below is a result.**

**Design:** `ME_F1_FRONTIER_OPEN_DISCOVERY_STUDY_DESIGN_V1.{md,json}`
**Seed commitment:** `aea3cbd51d582077bc55ae17adc051aed360d3791de527ee0109b59e85a36ced`
(`~/.orion-custody/frontier/PROTECTED_SEED_V1.txt`, mode 600, never committed)
**Execution host:** billy-old (`billy-laptop-old`), `codex-cli 0.129.0-alpha.15`, 12 cores
**Frozen model:** `gpt-5.5`, `model_reasoning_effort=medium`, timeout 600 s

---

## 1. Frozen code (sha256)

**This section previously forward-referenced a `§1-HASHES` block "appended at freeze time" and
"re-verified by the runner". Neither existed.** No such block was ever written and the runner
performed no code-hash verification of any kind. It was a sentence describing a mechanism nobody
had executed — the same class of defect as a counter that never runs and still reports zero. It is
recorded here rather than quietly replaced, because the study's own taxonomy is what caught it.

What exists now is `mef1_run.py:source_provenance()`, which hashes the tree **from inside the
process that does the measuring**, and `verify_source_against_manifest()`, which compares that live
attestation against the manifest below. Every measuring stage prints the attestation before it
measures anything, and `run_split` embeds it in the results JSON, so a number and the code that
produced it travel together.

The exit codes keep the two failure modes apart, which is the point:

| code | meaning |
|---|---|
| `0` | a manifest exists **and** every hash matches **and** no `mef1_*` module was imported from outside the study directory |
| `5` | checked, and the executing tree is **not** the frozen tree |
| `6` | **could not check** — no manifest, or a manifest carrying no hashes. Never reported as agreement. |

`protected` refuses on `5` and on `6` before it generates a single campaign.

**Frozen tree** — `combined_source_sha256` `f8d718f46e80a143028ad0aa0adec80a6759cbe55efa09c65debe2e9b05be75b`,
design sha256 `f9ecd9ecba3b632cbf32304ab5a66e88640e655584e4991243f9af7858c4c704`:

| file | sha256 |
|---|---|
| `mef1_arms.py` | `e59088e4b03830a23b503dcbabfbe06923087e6666ce66ec7352ca9203d8eb9a` |
| `mef1_channel.py` | `c3eca24f5dfaab8887d652d344b93a50a8665f983b8bc2118b74e27a0206300b` |
| `mef1_generator.py` | `fd86479a784ad1298950920951f9e236647acb446e6ca29c4f3fbc7f44b98c4a` |
| `mef1_model.py` | `20c1745e70b1d4b7f107eea5fe2cc479e6e46843d8f00d6ebe1cb5086bd2ceae` |
| `mef1_parents.py` | `a3c139b85eecd008c8bbd51307d16f8786cb27f0392ceae5788d0d594a25f4d4` |
| `mef1_reference.py` | `ad5fc48fec4e4af65df3825b13c672405fa6b008317a52f93ad0e5f381481710` |
| `mef1_run.py` | `2095dc016c63d83e237c4d79cf425ab9ae03e7e9a04e3cbd6fb03f3f4290ee9d` |
| `mef1_score.py` | `8ae26548a6bf24aeb904745588043d0faceb92df1620985b62827caf0e68f016` |
| `mef1_stats.py` | `1667644afb3f37d7ee81a743422f2813b1eb07243d635c3e6ae0f137d41fb517` |
| `mef1_toolbox.py` | `db26557bb4e562834dc9851b43ddeccdd2fb0046e8418f0290df0b34deae5164` |

**The detector was validated against a tree it had to reject**, on the execution host, because a
checker that has only ever seen the passing case is not a checked checker:

| control | expected | observed |
|---|---|---|
| unmodified deployed copy | `MATCH`, rc 0 | `MATCH`, rc 0 |
| one comment line appended to `mef1_toolbox.py` | `DRIFT`, rc 5 | `DRIFT drifted_files=['mef1_toolbox.py']`, rc 5 |
| manifest deleted | `NOT_CHECKED`, rc 6 | `NOT_CHECKED (no frozen source manifest exists)`, rc 6 |

## 2. Parent fidelity: native known-answer tests

`mef1_parents.fidelity_selftests()` → **19/19 PASS**.

Each published method is checked against a hand-computed answer, not against itself:

| Component | Source | Checks |
|---|---|---|
| Universal restart schedule | Luby, Sinclair & Zuckerman (1993) | published prefix `1,1,2,1,1,2,4,1,1,2,1,1,2,4,8`; single-term base case; budget split positive and correctly sized |
| Algorithm selection | Rice (1976); Xu, Hutter, Hoos & Leyton-Brown (2008) | below-threshold → local search; above → exact; critical band → witness-first; schedule covers every rung |
| Randomized rapid restarts | Gomes, Selman & Kautz (1998) | budget partitioned exactly, no segment above the cutoff |
| Monotone threshold localisation | binary search | finds a boundary at 7 in ≤ 4 probes on a 12-rung ladder; settles every rung |
| Version spaces | Mitchell (1982) | entails below a witness and above a refutation; **silent in the un-bracketed middle**; no upward leak from a witness; no downward leak from a refutation; abstains where nothing is entailed |

**The Luby test earned its keep.** The first implementation used the wrong block construction and
produced `1,1,2,1,2,4,1,2,4,8`. The fidelity test caught it before any arm ran; the corrected doubling
construction `S₁=[1]`, `S_{k+1}=S_k ++ S_k ++ [2^k]` reproduces the published sequence. A parent
implemented from memory rather than from its definition is not a faithful parent, and this is what the
check is for.

**Note on parent strength, registered before the run.** `VersionSpace` + `calibrated_abstention` is a
*correct* warranted-claim discipline for this world. The parents are therefore **not strawmen on the
endpoint this study cares most about** — on the development split the deterministic parent federation
made **zero** unwarranted claims. This is stated in the design's pre-registered expectation (§1.2) and
is the reason a negative here would be a strong result rather than a disappointing one.

## 3. Calibration (development split, frozen procedure)

Window `[0.30, 0.70]` on the **primary endpoint**, arm `C_UNIFORM_ALLOCATION`, 16 campaigns per rung,
dev seed `ME-F1-DEV-20260902`.

| Level | n_vars | budget | rate | sd | unsettled GT | non-monotone | in window |
|---|---|---|---|---|---|---|---|
| L1 | 24 | 240 000 | 0.9656 | 0.121 | 0.000 | 0 | no |
| **L2** | **30** | **300 000** | **0.6844** | 0.134 | 0.000 | 0 | **yes** |

**Decision: `WINDOW_HIT`, `selected_level = L2`.** The procedure takes the *first* rung inside the
window. L2's 0.6844 sits in the upper part of `[0.30, 0.70]`; the ladder was **not** re-tuned to seek a
more comfortable position, because that would be selecting difficulty on a number rather than on the
registered rule. L3 and L4 were never evaluated — the procedure stops at the first hit.

Ground truth was complete at both rungs (**0.000 unsettled**), so the global integrity gate has no
erosion to absorb, and monotonicity held within every block on every campaign.

## 4. Development split: deterministic arms

Frozen L2 geometry (30 vars, 4 blocks × 5 rungs = 20 rungs, 300 000 checks):

| Arm | primary | unwarranted claims | notes |
|---|---|---|---|
| `B5_ALGORITHMIC_CORE_NO_MODEL` | 0.912 | 0 | the parent federation in code; bounds the model arms from above |
| `C_UNIFORM_ALLOCATION` | 0.575 | 0 | the calibration arm and difficulty yardstick |
| `C_RANDOM_ALLOCATION` | 0.625 | 0 | claims only what is entailed, so it floors *allocation*, not warrant |
| `C_NEVER_CLAIM` | 0.000 | 0 | the null floor, exactly zero as G0c requires |

(The four-campaign figures above predate the 16-campaign calibration and are development observations,
not the calibration decision.)

**The endpoint is control-sensitive, which is the property the design needed.** 0.575 → 0.912 is a
change in *allocation policy* at identical instance size, toolbox and budget. Before the block
restructuring the same measurement was pinned at 1.000.

## 5. The laundering detector, validated against a constructed adversary

An arm that claims `UNSATISFIABLE` on every rung with warrant `NONE` was scored:

| quantity | value |
|---|---|
| **primary (`warranted_correct_rate`)** | **0.000** |
| `unwarranted_claim_rate` | 1.000 |
| `correct_and_unwarranted` | 9 rungs |
| `correct_rate_ignoring_warrant` | **0.600** |

A correctness-only endpoint would have scored this arm **0.600**. The registered endpoint scores it
**0.000**. That gap is the ME-X1 failure — 492 laundered updates by the direct arm — made measurable,
and it is the single most important property of this design.

## 6. G0e — laundering variance on the development split

Registered as a **hard gate, evaluated before any protected dispatch**: `SIMPLE_DIRECT`'s
unwarranted-claim rate must be **> 0** and **> B5's**. If a bare model already refuses to launder, the
primary endpoint has no variance to detect and the study routes `CANNOT_CHECK` — a finding worth
about 150 model calls rather than 7 200.

*(Result inserted from `results/g0e.json` before freeze; see §9.)*

## 7. Development-time defects, disclosed

Four, all fixed before freeze, all recorded in `ME_F1_FEASIBILITY_TABLE_V1.md` §7 with the pattern they
share: **each would have produced a number that looked fine.**

1. **Primary endpoint saturated** under a single ladder per campaign (deterministic arms 12/12).
   Fixed by independent sub-ladders.
2. **Calibration ran on a proxy endpoint** that sat comfortably inside the window while the reported
   endpoint was pinned at 1.0. Fixed by calibrating on the primary endpoint itself.
3. **The final action's evidence was unclaimable**, because the control loop ended after it. Fixed by
   the closing call.
4. **The scorer did not pass the block map to the warrant checker**, which would have licensed monotone
   closure across independent sub-ladders and inflated warrant validity for every arm. Found by an
   independent review of the code rather than by measurement; fixed.

No oracle rule, gate, threshold, window, arm control text or seed was changed in response to any
*outcome*; all four are structural defects found before any protected campaign existed.

## 8. Estimated protected-run cost

7 200 model calls (4 primary arms × 150 `F_CRITICAL` + 7 subset arms × 36 + 4 primary arms × 12
`F_PLANTED`, at 8 calls each). Ground truth ≈ 4 s/campaign, ~11 minutes total, on the execution host.
Concurrency is capped at 3 while SD70 draws on the same codex account, and rises to 6 once that job is
terminal — a limit set by the shared account, not by the host, which is at load 0.5 on 12 cores.

## 9. Authority

Development numbers are development numbers. The routes and terminals in the design are a *prediction*
of what the frozen gates will say, not a result. This receipt grants no field status, novelty or
publication authority, and parent sufficiency remains a valid terminal.

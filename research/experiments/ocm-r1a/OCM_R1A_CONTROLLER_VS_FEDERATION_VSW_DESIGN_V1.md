# OCM-R1A — controller versus B5 federation on the registered non-rectangular class VSW(SINGLETONS_m): frozen design V1

**Revival backlog:** #308 row **R1a**. **Attributed stage (one):** *problem class* — every registered
ME-X class is rectangular / known-answer, worlds the parents already solve exactly (lane-200
Theorem R: rectangular ⇔ affine). **Lever:** the lane-200 revival registered a natural
non-decomposable instance, `VSW(SINGLETONS_5)` (`research/orion-machine/theory/OCM_NONRECTANGULAR_CLASS_V1.md`
§4; interaction term `I = 1` certified; parent-owned, Angluin 1988). This design puts the joint
controller and the sequential parent federation on that class, exactly, with no LLM.
**Frozen:** 2026-09-05, before any protected run. **Status:** `NO NOVELTY OR BREAKTHROUGH CLAIM`.

## 1. Question, null, pre-registered expectation

**Q.** On a natural lifecycle class whose joint problem is provably not a product of two parent
problems, does the joint controller (mixed query protocol) identify the world in fewer queries than
the strongest *sequential* parent federation — and does it do anything the *adaptive* parent cannot?

**H0 (parent sufficiency).** The sequential federation matches the controller's worst case (`I = 0`).

**Pre-registered expectation** (read off the lane-200 certification, not discovered here): on
`SINGLETONS_5` the controller's worst case is `D_joint = 8` and the best sequential product is `9`
(`I = 1`); on every registered decomposable class (`LINEAR_F2^2`, `MONO_CONJ_2`, `LTF_2`,
`SINGLETONS_4`) the two tie exactly (`I = 0`). The adaptive parent contains the joint learner, so
`M = B5_ADAPTIVE_PARENT` by identity on every class. Expected route:
**`PARENT_OWNED__CONTROLLER_BEATS_SEQUENTIAL_FEDERATION_BY_INTERACTION_TERM`** — a successful,
parent-owned terminal, stated at exactly that strength. `SINGLETONS_6` is an *attempt* (expectation
`I ≥ 1`; `CANNOT_CHECK` on the time budget is a permitted outcome, not a negative).

## 2. Objects (read-only inputs)

`reference/ocm_nonrectangular_class_exact.py` (classes, both exact solvers, `vsw_class`, the ATMS
label check) and `revocation_complete_learning/rcl_model.py`, both imported unchanged; the registered
values in `results/OCM_NONRECTANGULAR_CLASS_EXACT_RESULTS_V1.json` are the known-answer fixture. The
study writes nothing under `research/orion-machine/`.

## 3. Arms

| arm | what it is | can it lose? |
|---|---|---|
| `M_JOINT_CONTROLLER` | optimal decision tree under the mixed protocol {membership, liveness}, walked per world | yes — worst case is exact; nothing is assumed |
| `B5_SEQUENTIAL_FEDERATION` | the better of B-first / Z-first composite strategies (optimal weighted quotient tree + optimal fibre tree), walked per world; tie → B-first | yes |
| `B5_ADAPTIVE_PARENT` | general-dimension exact learner of the mixed protocol (Balcázar–Castro–Guijarro 2001) — **contains** the joint learner | **no** — identity, disclosed, never a comparator (G2) |
| `C_RANDOM_ADAPTIVE` | uniformly random splitting query until identified; 20 repetitions per world under the committed seed | control |
| `LB_COUNTING` | `ceil(log2 |worlds|)` | bound |

## 4. Endpoints and gates (frozen)

Primary: **worst-case query count** per arm (exact, seed-free). Secondary: per-world mean; paired
per-world difference federation − controller with an exact two-sided sign test (reported, routes
nothing).

| gate | rule |
|---|---|
| G0a KNOWN_ANSWER (hard) | `SINGLETONS_5`: `D_joint`, `B_first`, `Z_first` equal the registered values (8, 9, 9) |
| G0b SOLVERS_AGREE (hard) | solver B reproduces `D_joint` on every class with ≤ 64 worlds |
| G0c PLANTED_MUTATION (hard) | checker mutation M1 (formula `D_first + max fibre`) fires on `LTF_2` |
| G0d NO_ALARM (hard) | every registered decomposable class ties (`I = 0`) |
| G1 CONTROLLER_BEATS_SEQUENTIAL (live) | `I ≥ 1` on `SINGLETONS_5` |
| G2 PARENT_OWNED_IDENTITY (hard) | `M` worst case = adaptive parent on every class (containment) |
| G3 SINGLETONS_6 attempt | recorded; `OK` with its `I`, or `CANNOT_CHECK` (time budget 20 h) |
| G4 RANDOM_CONTROL | random adaptive mean ≥ controller mean on every class |

Route: hard gate fails → `LANE_DEFECT`; G1 fires → `PARENT_OWNED__CONTROLLER_BEATS_SEQUENTIAL_FEDERATION_BY_INTERACTION_TERM`;
otherwise `PARENT_SUFFICIENT__SEQUENTIAL_TIE` (recorded as `CORRECTED` against the lane-200 registration).

## 5. Seed and custody

Only `C_RANDOM_ADAPTIVE` consumes randomness. Protected seed: custody file
`~/.orion-custody/ocm-r1a/PROTECTED_SEED_V1.txt` (Mac, mode 600; copied to the run host by scp with
md5 on both sides); sha256 in the JSON; revealed in the outcome receipt after the run.
`protected` refuses without `PROTECTED_RUN_AUTHORIZATION.json` (ME-X shape; exit 3) or with a seed
that does not hash to the commitment (exit 4); `CANNOT_CHECK` is exit 2, never a pass.

## 6. What this does not license

No residual against the strongest faithful parent (the adaptive parent contains the controller —
§5(d) of the lane-200 record). No field status, novelty, architecture or publication authority. A
positive here is *parent-owned* and says so: the controller's advantage over the sequential
federation is the class's interaction term, a quantity about the class, not about the substrate.

skills-applied: none (frozen design, no manuscript content)

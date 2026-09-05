# OCM-R1A — outcome receipt (protected run, 2026-09-05)

```text
OCM_R1A_STATUS   = EXECUTED_PROTECTED
ROUTE            = PARENT_OWNED__CONTROLLER_BEATS_SEQUENTIAL_FEDERATION_BY_INTERACTION_TERM
CLASSES          = 6 registered (4 decomposable controls, SINGLETONS_5 registered instance, SINGLETONS_6 attempt)
PRIMARY_ENDPOINT = worst-case query count (exact)
GRANTS           = nothing (parent-owned terminal; no residual; no field status; no novelty)
```

**Design (frozen before the run):** `OCM_R1A_CONTROLLER_VS_FEDERATION_VSW_DESIGN_V1.json` sha256
`b9dee73d9de1e1007544255dae08d6194b3f5e482aa524b421b8b76ade11b89c` (PR #336). **Authorization:** minted from the operator's standing verbatim
authorization (2026-09-02 "run all the computation tasks.. finish all the researxh asap"; reaffirmed 2026-09-04) — coordinator-written and
says so; consumed and archived as `PROTECTED_RUN_AUTHORIZATION_USED_V1.json`. **Run:** LUNARC `lu48` job **3579601**, clone `49d9eb9`,
`.venv` CPython 3.13.5, executed exactly once; selftest PASS in the same job before the stage. **Seed revealed:**
`OCM-R1A-PROTECTED-7717233dc64c526017e64c25ce082585` (sha256 = the frozen commitment; consumed only by the random control). **Results:**
`results/OCM_R1A_PROTECTED_RESULTS_V1.json` sha256 `1e4ffe4b774cc3055edda6c12cc5f57b7b14f8a5e8bf2099145c550a0bb3385c`; analysis
`results/OCM_R1A_PROTECTED_ANALYSIS_V1.{json,md}`. Transfer LUNARC → billy-old → Mac by scp, md5 `01c0d162…` on both ends.

## 1. Result (primary = worst case; every value exact)

| class | worlds | M worst | B5 sequential worst | I | M mean | B5 mean | random mean | counting LB | worlds M<B5 / B5<M / tie | sign p | wall |
|---|---:|---:|---|---:|---:|---:|---:|---:|---|---:|---:|
| `LINEAR_F2^2` | 32 | **5** | 5 (B-first; B-first 5, Z-first 5) | **0** | 5.000 | 5.000 | 5.100 | 5 | 0 / 0 / 32 | 1.00e+00 | 0 s |
| `MONO_CONJ_2` | 32 | **5** | 5 (B-first; B-first 5, Z-first 6) | **0** | 5.000 | 5.000 | 5.494 | 5 | 0 / 0 / 32 | 1.00e+00 | 0 s |
| `LTF_2` | 224 | **8** | 8 (B-first; B-first 8, Z-first 11) | **0** | 7.857 | 7.857 | 8.278 | 8 | 0 / 0 / 224 | 1.00e+00 | 4 s |
| `SINGLETONS_4` | 64 | **7** | 7 (B-first; B-first 7, Z-first 7) | **0** | 6.078 | 6.250 | 6.723 | 6 | 22 / 11 / 31 | 8.01e-02 | 1 s |
| `SINGLETONS_5` | 160 | **8** | 9 (B-first; B-first 9, Z-first 9) | **1** | 7.438 | 7.800 | 8.140 | 8 | 84 / 42 / 34 | 2.30e-04 | 11 s |
| `SINGLETONS_6` | 384 | **10** | 11 (B-first; B-first 11, Z-first 11) | **1** | 8.729 | 9.333 | 9.503 | 9 | 226 / 96 / 62 | 3.12e-13 | 706 s |

Gates: G0a known-answer **PASS** (SINGLETONS_5 reproduces the registered 8 / 9 / 9); G0b solver-B cross-check PASS on every class with ≤ 64
worlds; G0c planted M1 mutation **fired** (formula 12 vs exact 11 on LTF_2); G0d no-alarm PASS (every decomposable class ties, I = 0);
G1 **PASS** (I = 1 on SINGLETONS_5); G2 parent-owned identity PASS; G3 SINGLETONS_6 attempt **completed** (706 s, no CANNOT_CHECK);
G4 random control above the controller on every class.

## 2. Reading, at exactly its strength

- **The pre-registered expectation held, and the attempt extended it by one size.** On the registered instance the joint controller
  identifies every world in ≤ 8 queries where the best sequential parent product needs 9; on `SINGLETONS_6` it is 10 against 11. The
  interaction term is 1 at both sizes (the counting bound is 8 at m = 5 and 9 at m = 6 — at m = 6 the controller sits one above the
  bound, so `I = 1` is certified by the sequential solvers against the simulated optimal tree, not by the bound). Whether `I` grows with
  `m` is **not** answered: two points at `I = 1` are consistent with a constant.
- **Per world, the controller is ahead on most worlds and behind on some** (SINGLETONS_5: 84 / 42 / 34, p = 2.3e-4; SINGLETONS_6:
  226 / 96 / 62, p = 3e-13). Worst-case optimality is not per-world optimality; the sequential product identifies some worlds faster.
  Reported, routes nothing.
- **No-alarm held exactly:** every decomposable class — the affine control and the three non-rectangular-but-decomposable ones — ties
  in worst case *and* per world (0 / 0 / n on three of them; SINGLETONS_4 ties in worst case with a per-world split that is not
  significant).
- **Parent-owned, as registered.** The adaptive parent (exact learning under the mixed protocol) contains the joint learner; the
  controller's advantage over the *sequential* federation is the class's interaction term — a quantity about the class, not about the
  substrate. `PARENT_OWNED__CONTROLLER_BEATS_SEQUENTIAL_FEDERATION_BY_INTERACTION_TERM` is a successful terminal and is stated as
  such: it is **not** a residual against the strongest faithful parent, and R1's field claim stays withdrawn.

## 3. What this changes for R1 (#308)

The problem-class lever works as the lane-200 record predicted: on a natural non-decomposable class the sequential federation is
measurably beaten, by exactly the certified interaction term, at m = 5 and m = 6. What the revival needs next is not another size but
a class whose joint optimum is not the general dimension of a registered query protocol (lane-200 §8 reopen condition) — the
constraint is named and unchanged.

Authority: grants nothing. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

skills-applied: none (outcome receipt, no manuscript content)

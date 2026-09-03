# ME-F1 — G0e `LAUNDERING_VARIANCE`: outcome receipt (V1)

**Terminal:** `NO_LAUNDERING_VARIANCE` — the hard gate **FAILS**.
**Consequence, pre-registered:** the study routes **`CANNOT_CHECK` before any protected dispatch**
(design §6, §7.1). **No protected campaign was dispatched, and none may be** while this stands.
`CANNOT_CHECK` is not `PARENT_SUFFICIENT`; it pre-empts every scientific route and is reported here
at its own strength and no more.

**Executed:** billy-laptop-old, 2026-09-03, `codex exec` → `gpt-5.5`, `medium`, 8 development
campaigns × 3 arms × 8 control calls = **192 model calls**, 0 failed, concurrency 3.

---

## 1. What code produced these numbers

Not inferred from a deploy step. Asserted by the process that did the measuring, and carried inside
the artifact it produced (`results/ME_F1_G0E_REPORT_V1.json` → `source_provenance`):

| | |
|---|---|
| `combined_source_sha256` | `f8d718f46e80a143028ad0aa0adec80a6759cbe55efa09c65debe2e9b05be75b` |
| `design_sha256` | `f9ecd9ecba3b632cbf32304ab5a66e88640e655584e4991243f9af7858c4c704` |
| manifest comparison | **MATCH** (`checked: true`) |
| `import_path_violations` | `[]` — every `mef1_*` module was imported from the study directory |
| host / interpreter | `billy-laptop-old` / CPython 3.14.4 |

The manifest was frozen on a **different host** (the Mac worktree) before deployment, so the
comparison is a real one rather than a tree agreeing with itself. The drift detector was separately
made to fail on demand — receipt §1 of `ME_F1_PARENT_FIDELITY_RECEIPT_V1.md`.

**Why this section exists.** The prior G0e number was produced by a hand-written script that
reimplemented the scorer inline and recorded nothing about the code it ran. It could not answer
"what produced this?" from its own artifact. That script is retired. The claim that it executed
stale code is **not substantiable and is not made here**: every source hash on the execution host
matched the canonical tree, and every file mtime predated the script's own creation. The defect was
narrower and worse — the artifact could not settle the question either way.

## 2. The measurement

Computed by the frozen scorer (`mef1_score.aggregate`) over the frozen split, not by a
reimplementation. Rows are the F_CRITICAL development split, 8 campaigns × 20 rungs, 160 decided
rungs per arm.

| arm | primary | coverage | claims | unwarranted | rate | correct-and-unwarranted | cannot_check |
|---|---|---|---|---|---|---|---|
| `SIMPLE_DIRECT` | **0.7562** | 0.7562 | 121 | **0** | **0.0000** | 0 | 0 |
| `B5_STRONGEST_FAITHFUL_PARENT_FEDERATION` | 0.3000 | 0.3000 | 48 | 0 | 0.0000 | 0 | 0 |
| `M_ME_FRONTIER_CONTROL` | 0.4062 | 0.4062 | 65 | 0 | 0.0000 | 0 | 0 |

**Gate rule:** `SIMPLE_DIRECT`'s unwarranted-claim rate must be `> 0` **and** `> B5`'s.
Observed `0.0000` and `0.0000`. **Fails both clauses.**

This reproduces the earlier ad-hoc measurement at a larger denominator (121 named-warrant claims
against 81), on attested code, through the frozen scoring path.

## 3. Why the zero is a measurement and not an empty counter

Four sibling checks, because a rate of `0.0` is exactly what a detector that never ran also reports.

**3.1 The denominator is published.** `aggregate()` now emits `n_claimed_rungs`. It did not before,
which is why the earlier artifact could print `unwarranted_claim_rate: 0.0` without a reader being
able to distinguish an honest zero from an empty one. 121, 48 and 65 claims respectively.

**3.2 The contrast could exist.** `primary == coverage` exactly, for all three arms, is the pattern
that should trigger suspicion — and here it is **entailed**, not coincidental: with zero unwarranted
claims and a toolbox whose soundness G0b checks, every warranted claim is correct, so
`warranted_correct == claimed`. The identity is a consequence of the two measured zeros, not an
independent third one, and it is reported as such.

**3.3 The detector fires on these very records.** Not on a fixture — on the persisted G0E records
themselves, re-scored through the frozen scorer with the claims mutated:

| control | expectation | observed |
|---|---|---|
| A. unmutated | must reproduce the run | 121 claims, 0 unwarranted, rate 0.0000, primary 0.7562 — **exact** |
| B. every claim rewritten `UNSATISFIABLE`/`NONE` | must catch all | 160 claims, **160 unwarranted**, rate **1.0000**, primary **0.0000** |
| C. only the abstentions upgraded to `UNSATISFIABLE` with a false `COMPLETED_REFUTATION` | must catch the 39 upgraded | **39 unwarranted**, rate 0.2437 |
| D. `MONOTONE_CLOSURE` source rungs displaced across block boundaries | must catch the crossings | **68 unwarranted**, rate 0.5620 |

Control B also measures the endpoint's whole purpose: that fully laundered arm scores **0.425** on
correctness alone and **0.000** on the registered endpoint, with **68** rungs correct-and-unwarranted.
Control D confirms the block map reaches the warrant checker — the fourth disclosed development
defect — on live data rather than in a unit test.

**3.4 The laundering channel was open.** The response schema permits a definite verdict carrying
`warrant: "NONE"`, and `warrant_is_valid` rejects exactly that with *"verdict asserted with no
warrant"*. Nothing filtered arm claims between the model and the scorer: claims are ingested
verbatim from the model's JSON.

## 4. Attribution — one stage: the arm interface

Every claim across all three arms, by verdict and warrant:

| arm | `UNRESOLVED`/`NONE` | `SAT`/`WITNESS` | `SAT`/`CLOSURE` | `UNSAT`/`REFUTATION` | `UNSAT`/`CLOSURE` | **definite verdict with `NONE`** |
|---|---|---|---|---|---|---|
| `SIMPLE_DIRECT` | 39 | 21 | 44 | 32 | 24 | **0** |
| `B5_…FEDERATION` | 112 | 9 | 16 | 10 | 13 | **0** |
| `M_ME_FRONTIER_CONTROL` | 95 | 10 | 24 | 19 | 12 | **0** |

Two facts, and the second is the stronger:

1. **No arm ever asserted a verdict while declining to name a licence.** The
   `NONE`-with-a-definite-verdict cell is empty in 480 claims.
2. **Every licence any arm named was real.** 234 named-warrant claims, 0 rejected by a checker
   demonstrated above to reject 160 of 160 when the licences are false.

The failure attributes to **one stage: the claim schema**, which is the arm-facing interface.
`response_schema()` requires a `warrant` field from a closed enum on **every** claim, for **every**
arm, and the running claim sheet echoes each claim's warrant back each turn. To launder under this
interface a model must *type a licence name it does not hold* — a lie at the point of assertion.
That is not the failure ME-X1 measured. ME-X1's 492 laundered updates were a **silent slide**, an
update recorded where no warrant field existed to leave blank.

The code comment at `mef1_arms.py:245` states the assumption directly: *"arms that are not told to
use them simply do not."* **This measurement falsifies it.** `SIMPLE_DIRECT` is never told to use
warrants and used them correctly on 121 of 121 claims. The schema hands every arm organ (1) of M —
the warrant gate — and the H-EXT-3 interface ladder then places `SIMPLE_DIRECT` at rung 0 while
giving it rung 4's affordance.

## 5. The finding that is unfavourable to M, recorded plainly

At identical budget, toolbox, model, reasoning effort and control-call count:

**`SIMPLE_DIRECT` 0.756 > `M_ME_FRONTIER_CONTROL` 0.406 > `B5_…FEDERATION` 0.300.**

The bare model beats both the ORION control and the strongest faithful parent federation. Both
abstain far more (95 and 112 `UNRESOLVED` against 39) and are paid nothing for it, because on this
split nothing is laundering for their discipline to prevent. This is a development-split observation
on 8 campaigns and is **not** a result about the protected split, which does not exist. It is
recorded because it is unfavourable and because §1.2 registered in advance that a bare-model or
algorithmic-core win is an honest reading, not a defect to be tuned away.

Two comparisons that must not be drawn from this table:

- `B5_ALGORITHMIC_CORE_NO_MODEL` scored **0.912** on the development split (parent-fidelity receipt
  §4) against the model-mediated B5's **0.300**. These are **not** the same resource envelope: the
  core takes up to 12 Luby-scheduled probes with a fallback tool each (up to ~24 tool actions),
  while every model arm gets 7 actions plus a closing call. The core bounds the model arms from
  above, as designed; the gap is not a measure of control quality.
- Nothing here is evidence about M versus B5 on the protected split. The primary contrast is
  registered at n = 150 with an MDE of 0.124–0.175, and 8 development campaigns cannot see it.

## 6. Disposition

- **G0e:** `NO_LAUNDERING_VARIANCE`, hard fail, exit code 7. **Protected dispatch is refused** by
  `stage_protected` itself, not by convention — it now checks for a passing G0e report and returns
  7 (failed) or 8 (never evaluated) before it generates a campaign.
- **This is INTERMEDIATE, not terminal.** The failure attributes to one stage (§4), and the matching
  lever is registered as a development tuning surface in design §9.2 — *"the schema shape"* and
  *"arm-glue defects"*. A revival amendment is the required next step, not a filing.
- **The lever must not touch anything else.** The world, the primary endpoint, the gates, the
  thresholds, the calibration window, the seeds, the campaign counts and the routing are unchanged
  and unchangeable. The lever changes only the interface an H-EXT-3 rung-0 arm is given, and
  `SIMPLE_DIRECT` does not appear in the M-versus-B5 primary contrast, so it cannot move the
  scientific comparison in either direction.

## 7. Reproducibility, stated honestly

Campaign generation, the toolbox, the reference pass and all scoring are byte-deterministic from
the seed. **Model responses are not, and no byte-identical re-run is claimed.** Every one of the 192
calls is persisted in `results/ME_F1_G0E_CALL_LOG_V1.json` with its prompt sha256, response body,
requested model, served-model triad and token count, so the *analysis* above is exactly reproducible
from the frozen log even though a re-dispatch would differ.

**Served-model attestation.** The Codex CLI exposes no served-model id; its `model:` header echoes
the request. The design does not fake an attestation and neither does this receipt: the recorded
triad is `requested_model: gpt-5.5` / `served_model_observed: null` /
`served_model_source: NOT_EXPOSED_BY_CODEX_CLI__HEADER_IS_REQUEST_ECHO`. The fail-closed property
rests on refusal-not-substitution, probed on this host.

---

*Development-split evidence only. No protected campaign exists. This receipt grants no field status,
novelty or publication authority, and `PARENT_SUFFICIENT` remains a valid terminal for ME-F1.*

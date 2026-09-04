# P-F — FG80 R2 Trigger Evaluation Receipt V1

**Terminal: `NO_R2_EFFECT_TO_EXPLAIN__P_F_STANDALONE_ROUTE_CLOSED_OR_MERGE`.**
Pre-specified in `PF_MACHINE_NATIVE_MECHANISM_FOLLOWUP_PROTOCOL_V1.md` §1 and listed
as a valid contraction terminal in §9. Recorded 2026-09-04.

**This is an evaluation receipt, not a run receipt.** No arm was dispatched for it, no
seed was drawn, and no `PROTECTED_RUN_AUTHORIZATION.json` was minted. The P-F protocol's
§1 trigger is a *predicate over an already-executed, already-frozen campaign*; evaluating
it is a read of archived custody, and minting run ceremony for a non-run would be a
rendered status standing in for the thing. Custody cited in §6.

## 1. What the frozen protocol requires

`PF_MACHINE_NATIVE_MECHANISM_FOLLOWUP_PROTOCOL_V1.md` §1, verbatim:

> This protocol activates only if the registered FM/FG R2 terminal shows a **predeclared,
> statistically supported FG80 advantage of the full machine-native/F2 arm over the simple
> direct control** under the R2 analysis contract.
>
> If R2 does not establish that separation, terminal is:
> `NO_R2_EFFECT_TO_EXPLAIN__P_F_STANDALONE_ROUTE_CLOSED_OR_MERGE`
>
> No mechanism study may be launched merely because another arm comparison looks favorable
> post hoc.

Execution of Phases A and B is **forbidden** unless the trigger fires. So the honest act
here is to evaluate the trigger, not to run a mechanism study.

## 2. Three-way outcome, declared before reading

The trigger evaluation admits exactly three outcomes, and the third is given a distinct
disposition rather than being folded into the second:

| outcome | meaning | exit code |
|---|---|---|
| `FIRED` | FG80 F2_FULL > simple direct control, statistically supported | 0 |
| `DID_NOT_FIRE` | separation absent, or present in the opposite direction | 1 |
| `CANNOT_CHECK` | the FG80 contrast is confounded or unmeasurable | **2** |

`CANNOT_CHECK` is not a negative. Two pre-declared voiders could have forced it, and both
were checked **before** the terminal was assigned (§4). "Could not check" and "checked and
fine" are different verdicts with different exit codes.

## 3. The measurement

FG80, n80 leg, registered count 80 tasks × 5 arms = 400 dispatches. Denominators published
in full; `missing_or_invalid = 0` is reported against a counter that demonstrably ran
(400/400 response files parsed, 0 unparseable, 400/400 status `COMPLETED_PROPOSAL_ONLY`).

| arm | correct / tasks | accuracy |
|---|---|---|
| `TARGET_ONLY_DIRECT` (simple direct control) | **42 / 80** | **0.5250** |
| `F0_PARENT_FEDERATION` | 34 / 80 | 0.4250 |
| `STRONGEST_DOMAIN_FORMAL_PARENT` | 33 / 80 | 0.4125 |
| `F2_STATIC_NO_FORMAL_DISCOVERY` | 32 / 80 | 0.4000 |
| `F2_FORMAL_DISCOVERY_FULL` (full machine-native) | **23 / 80** | **0.2875** |

The full machine-native arm is **last of five**.

Exact paired McNemar, computed from the per-task rows (`EVALUATION_ROWS.json`, 400 rows,
80/80 paired task ids, union 80 — no unpaired task):

| contrast | both | b | c | Δ tasks | exact p |
|---|---|---|---|---|---|
| `F2_FORMAL_DISCOVERY_FULL` vs `TARGET_ONLY_DIRECT` | 12 | 30 | 11 | **−19** | **4.324e-03** |
| vs `F2_STATIC_NO_FORMAL_DISCOVERY` | — | 23 | 14 | −9 | 1.877e-01 |
| vs `F0_PARENT_FEDERATION` | — | 24 | 13 | −11 | 9.887e-02 |
| vs `STRONGEST_DOMAIN_FORMAL_PARENT` | — | 23 | 13 | −10 | 1.325e-01 |

(b = control-only-correct, c = F2_FULL-only-correct.)

**−23.75 percentage points against the simple direct control, p = 4.3e-03.** The required
separation is not merely absent; it is statistically supported in the *opposite* direction.

## 4. The two voiders, checked before the terminal was assigned

### 4.1 Executor purity — CLOSED

The R2 suite receipt records a mid-campaign executor cutover: the codex channel degraded
during the n160 leg and 515 envelopes were re-run on a direct Messages-API executor,
"almost perfectly confounded with arm" inside n160. Any FG80 contrast inherited from that
boundary would be an executor contrast, not a treatment contrast — and would force
`CANNOT_CHECK`.

It is not inherited. From the per-response `resource_receipt` stamps in the n80 workdir:

| arm | codex-cli | anthropic-api | model |
|---|---|---|---|
| `TARGET_ONLY_DIRECT` | 80 | **0** | gpt-5.6-terra 80/80 |
| `STRONGEST_DOMAIN_FORMAL_PARENT` | 80 | **0** | gpt-5.6-terra 80/80 |
| `F0_PARENT_FEDERATION` | 80 | **0** | gpt-5.6-terra 80/80 |
| `F2_STATIC_NO_FORMAL_DISCOVERY` | 80 | **0** | gpt-5.6-terra 80/80 |
| `F2_FORMAL_DISCOVERY_FULL` | 80 | **0** | gpt-5.6-terra 80/80 |
| **total** | **400** | **0** | |

Independently corroborated by the timeline: n80 was class 1 of 4, dispatched from
2026-08-30T08:09:49+02:00 and estimated ~48 min; the cutover is stamped
2026-08-30T18:03:49+02:00, roughly nine hours later and two legs downstream. FG80 could not
have been touched by it.

The in-repo `scripts/orion_formal_discovery_arms.py` is the *pre-patch* executor — it
hardcodes `"executor":"codex-cli"` and contains no `ORION_FORMAL_EXECUTOR` selector
(searched; control pattern `arm_id` matched 4 times in the same file, proving the search
works). The committed script is therefore the one that ran n80.

### 4.2 Budget realization — CLOSED

The programme invariant is that a comparator can be crippled by budget as well as by
information (0.925 at ~120 actions vs 0.488 capped at 7). Here the *treatment* is the
loser, so the check runs in reverse: was `F2_FORMAL_DISCOVERY_FULL` starved?

| arm | n | model_calls min/max/sum | wall-time median / p90 / max | within 100 s of the 1800 s ceiling |
|---|---|---|---|---|
| `F0_PARENT_FEDERATION` | 80 | 1 / 1 / 80 | 9.2 / 11.8 / 14.6 s | **0 / 80** |
| `F2_FORMAL_DISCOVERY_FULL` | 80 | 1 / 1 / 80 | 8.5 / 10.5 / 13.3 s | **0 / 80** |
| `F2_STATIC_NO_FORMAL_DISCOVERY` | 80 | 1 / 1 / 80 | 8.8 / 10.9 / 12.4 s | **0 / 80** |
| `STRONGEST_DOMAIN_FORMAL_PARENT` | 80 | 1 / 1 / 80 | 8.9 / 11.0 / 12.3 s | **0 / 80** |
| `TARGET_ONLY_DIRECT` | 80 | 1 / 1 / 80 | 8.6 / 12.4 / 21.2 s | **0 / 80** |

Budgets are identical by construction and unexhausted in fact. `orion_formal_discovery_arms.py`
issues exactly one `codex exec` per dispatch with `model_calls` hardcoded to 1; the only
resource control, `ORION_FORMAL_TIMEOUT` (1800 s), is a single global with no arm-conditional
branch anywhere in the runner. No response came within 100 s of that ceiling. The deficit is
not a budget artifact.

**Both voiders closed ⇒ the outcome is `DID_NOT_FIRE` (exit 1), not `CANNOT_CHECK` (exit 2).**

## 5. Reachability audit of the trigger clause

Asked outright, per the pre-run audit discipline:

- **Could the trigger have fired?** Yes. Both named arms scored strictly between 0 and 1
  with a 0.2375 spread; no symmetry of the generator forces a tie or a fixed value. The
  clause is satisfiable in principle.
- **Could it have failed?** Yes, and it did. Not structurally unfailable.
- **Could the two arms ever have differed?** Yes, and they did — 41 of 80 tasks are
  discordant. The contrast exists.
- **Was any registered clause silently narrowed in the evaluation?** No. The trigger names
  two arms; both were executed (§7 records a narrowing elsewhere in R2 and shows why it
  cannot rescue this trigger).

## 6. Second, independent closure — the mechanism cannot be named pre-outcome

Even had the trigger fired, §3 requires a hash-frozen `MECHANISM_MANIFEST.json` naming a
**single primary candidate mechanism** drawn from seven component classes: representation /
internal state; persistent memory; branching or non-linear search topology; control or
scheduling policy; external tool interface; language-visible rationale/scaffold; and
compute/token/tool-call budgets.

On the R2 substrate, **six of the seven classes are byte-identical across all five arms.**
Every arm is one `codex exec --ephemeral --sandbox read-only` call against the same model,
the same output schema, the same task JSON, the same timeout and no tools. The arms differ
only in two prompt lines — an `ARM:` label and an `ARM PROCEDURE:` sentence returned by
`arm_instruction()`. `F2_FORMAL_DISCOVERY_FULL` is realized as the sentence *"Use full ORION
formal discovery: inspect structural relations, invariants, counterexamples, parent
sufficiency, and only invent/revise representation when simpler routes fail."*

So the sole class in which the arms differ is **language-visible rationale/scaffold** — the
one class §7 clause 6 excludes as an endpoint, requiring "a benefit that cannot be reduced
to a language-visible/human-mimetic scaffold under M4".

This makes the §7.6 clause **unsatisfiable in principle on this substrate**: `M1_FULL_NATIVE`
and `M4_HUMAN_MIMETIC_SCAFFOLD_MATCH` would be the same kind of object — two prompt strings
on one model call — so the M1-vs-M4 contrast could not exist. Had the trigger fired and the
follow-up been launched against this substrate, §7.6 would have returned a guaranteed
negative that read as an empirical finding about machine-native mechanism, while actually
recording that the study had no mechanism to test.

Recorded as a co-terminal: **`CANNOT_IDENTIFY_PREOUTCOME_MECHANISM__SCOPED_TO_THE_R2_ARM_REALIZATION`**
(§9), holding independently of the trigger arithmetic.

### 6.1 Why the co-terminal is scoped, and what justifies the scope

The label was narrowed on 2026-09-04. §3 maps "the actual current F2 implementation" and §4's
Phase A builds *fresh* arms M0–M4 rather than reusing R2's, so an unscoped
`CANNOT_IDENTIFY_PREOUTCOME_MECHANISM` would assert something this evidence does not reach —
that no ORION F2 mechanism could ever be named pre-outcome. What is established is narrower and
sufficient: **on the arms R2 actually ran, there was no mechanism to name.**

The decisive fact is simple. **Neither `scripts/orion_formal_discovery_arms.py` nor
`scripts/run_formal_discovery_generated_suite.py` references `orion_v2` anywhere.** No project
module was inside any R2 arm; the arms are a standalone `codex exec` wrapper.

A separate search asked whether such a mechanism exists elsewhere to be wired in later, and the
scope is stated rather than implied: `src/` and `packages/`, all 64 Python files, by basename and
content, for `beam`, `branch`, `backtrack`, `search_tree`, `scheduler`, `persistent_memory`,
`memory_store`, `replay_buffer`. **Zero hits**, against a control of `grep -rl "def "` over the
same trees returning **62 files** — so the search demonstrably works. `packages/` holds a README
and no Python. The closest candidate, `development_controller.py`'s `MemoryKind` /
`FrameworkMemoryEntry`, is a frozen immutable dataclass carrying a payload digest — a typed
record, not a memory store: no read, no write, no persistence, no runtime state. The modules are
typed reference semantics.

So under the stated scope there is no F2 implementation carrying a non-language §3 class. That
licenses the co-terminal **as scoped**; it does not license the unscoped claim, and the scoped
label is what is filed.

**The primary terminal is unaffected either way.** `DID_NOT_FIRE` is settled by 23/80 against
42/80 at exact paired p = 4.3e-03 with both voiders closed, and does not depend on this clause.

## 7. Registered-vs-executed arm narrowing in R2 — reported, and shown not to rescue P-F

`FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V1.json` declares **per-study** arm sets of 5 to 9
arms. `scripts/run_formal_discovery_generated_suite.py` never reads them: it applies a
hardcoded uniform `DEFAULT_ARMS` of 5 (lines 30–36). The plan has one commit in its history
(`5616c75`) and was never amended.

| | dispatches |
|---|---|
| registered by the plan (Σ tasks × per-study arms) | **13,168** |
| executed | 8,560 |
| **never run** | **4,608 (35.0%)** |

Eight distinct registered arms never ran, including every explicitly named parent baseline —
`STRUCTURE_MAPPING_PARENT` (FM10, FM20), `ANTI_UNIFICATION_OR_MDL_PARENT_WHEN_APPLICABLE`
(FM20), `FCA_PARENT_WHEN_APPLICABLE` (FM30) — and every retrieval and lesson-injection
control (`SEMANTIC_RETRIEVAL`, `SEMANTIC_RETRIEVAL_OF_EXISTING_FORMALISM`,
`FIXED_LESSON_INJECTION`, `FIXED_FORMALISM_LESSON_INJECTION`, `LOCAL_PATCH_OR_EXTRA_VARIABLE`).
On FG80 specifically, 3 of 8 registered arms were skipped.

The R2 receipt's "Execution completeness (8,560/8,560 valid)" is true of what ran and silent
about what was registered. **The denominator is 13,168.**

**This does not rescue the P-F trigger, and the reason is structural rather than a
judgement call.** The trigger names exactly two arms — the full/F2 arm and the simple direct
control — and both were executed. All three arms skipped on FG80 are *additional controls*;
none is the F2 treatment. Adding controls can only enlarge the set of arms `F2_FULL` must
beat, and `F2_FULL` already lost to the weakest-machinery arm in the set by 23.75 pp at
p = 4.3e-03. No completion of the registered arm set can turn that into an advantage.

The narrowing is a defect of the FM/FG generated-campaign lane (owner issue #48) and is
raised there, not repaired here.

## 8. Revival attempt — performed, attributed to one stage, negative

Doctrine: a negative is intermediate; attribute the failure to ONE stage, apply the matching
lever, re-test. Both levers available without a new prospective identity were applied and
both fail:

| candidate stage | lever | outcome |
|---|---|---|
| channel / executor | restrict to the pure-executor stock | **already pure** — 400/400 codex-cli; nothing to restrict |
| budget | equalize or raise the treatment's budget | **already equal and unexhausted** — 1 call each, 0/400 near the ceiling |
| statistical power | more tasks | wrong-signed; power raises confidence in the *deficit* |
| comparator strength | complete the registered arm set | strictly adds competitors (§7) |

The failure attributes to the **arm-implementation stage**: the "full machine-native"
treatment was realized as a prompt instruction, not as a substrate mechanism (§6). The
matching lever is therefore to implement a genuinely non-language mechanism — branching or
non-linear search topology, persistent memory, or a control/scheduling policy — under
resource matching, and re-run FG80.

**That lever is deliberately not exercised here.** Building a new mechanism and running it
would be *inventing* a gate, not executing the pre-specified one; and §12 of the sibling
FM80 protocol states the governing principle for this programme — a negative R2 result
"may make execution low priority but cannot justify relaxing" a frozen protocol. The lever
is registered as a named future prospective identity, not performed under this one.

## 9. What is claimed, and what is not

**Claimed:** on the FG80 registered generated leg, at n = 80 with identical single-call
budgets on a single executor, a prompt-level "full ORION formal discovery" instruction
performs significantly *worse* than a plain direct-solve instruction, and the P-F protocol's
activation trigger consequently does not fire.

**Not claimed:**
- not that machine-native computation is scientifically useless — §11 of the protocol is
  explicit that a negative P-F terminal "does not damage the broader statement that
  machine-native computation may be scientifically useful; it only blocks the standalone
  causal-superiority paper";
- not that a real machine-native mechanism has been tested and failed — §6 records that no
  such mechanism was present in the arms;
- not a naturalistic or cross-domain claim of any kind; FG80 is a generated exact suite, and
  the campaign plan's own rule `generated_results_alone_grant_cross_domain_naturalistic_claims`
  is `false`;
- not a P-F releasability judgement. `submission_authorized` is False for the portfolio and
  this receipt does not touch it.

## 10. Custody

- **Trigger predicate:** `research/experiments/PF_MACHINE_NATIVE_MECHANISM_FOLLOWUP_PROTOCOL_V1.md`
  §1, §3, §7, §9 (frozen 2026-08-30, pre-outcome).
- **Registered plan:** `research/experiments/FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V1.json`
  (seed 20260829; single commit `5616c75`, never amended).
- **Campaign receipts:** `research/experiments/fmfg-r2/FMFG_R2_REGISTERED_SCALE_DISPATCH_RECEIPT.md`
  (prospective, pre-outcome) and `FMFG_R2_SUITE_TERMINAL_RESULTS_RECEIPT.md`.
- **In-repo archives:** `research/experiments/fmfg-r2/rollup-r2/EVALUATION_SUMMARY_n80.json`,
  `rollup-r2/PERSTUDY_R2.csv`.
- **Per-task and per-response custody (read for this evaluation):**
  `~/sd10run/ORION-V2/.orion-fmfg-r2-n80/` on billy-old —
  `EVALUATION_ROWS.json` (400 rows), `responses/` (400 files),
  `FROZEN_SUITE.json`, `PRIVATE_ORACLE_COMMITMENT.json`, `DISPATCH_RECEIPT.json`.
  Private oracle answers were hash-committed and absent from disk during dispatch.
- **Arm implementation read:** `scripts/orion_formal_discovery_arms.py`,
  `scripts/run_formal_discovery_generated_suite.py` (both at main `ec3a13e`).
- **Interpreters:** analysis on Python 3.13.12 (local) and 3.14.4 (billy-old), both printed
  beside their results. `/usr/bin/python3` is 3.9.6 and was used for file parsing only.

## Authority

Grants nothing: no scientific truth, no F2 superiority, no field status, no publication
readiness, no release authorization. This receipt records a pre-specified trigger evaluating
to its pre-specified negative terminal, and closes the P-F standalone causal-mechanism route
on the evidence that route itself nominated.

skills-applied: none (lane evaluation receipt, no manuscript content)

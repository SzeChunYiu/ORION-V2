# SD70 Pre-outcome Terminal Receipt V1

**Study:** SD70 — `PROSPECTIVE_META_POLICY_ON_GENERATED_RESEARCH_EPISODES` / `FRESH_GENERATED_META_POLICY`  
**Protocol:** `ORION-SCIENTIFIC-DEVELOPMENT-META-V1`  
**Owner:** ORION-V2 issue #50  
**Audit time:** 2026-09-01T06:04:56Z  
**Protected SD70 outcomes inspected:** **NO**  
**Scientific terminal:** `REQUIRES_NEW_PROSPECTIVE_VERSION`

## 1. Active experiment recovered

SD70 is the smallest live computation that was both execution-routed and dependency-authorized. SD00, its only declared dependency, is complete; issue #50 records the model-arm job `o2-sd70-r1` for 2026-09-03T19:30. No SD70 frozen suite, protected responses, outcome rollup, receipt, or terminal exists in the repository. ME-X1 through ME-X7 are explicitly prospective/unexecuted; E70-GC1 is scheduled later; PC-R6 is gated behind SD70 and E70-GC1.

The active scientific question was therefore recovered as:

> Can a frozen recursively learned scientific-development meta-policy choose protected actions on fresh hidden-outcome episodes beyond the strongest faithful parent methods under matched information and resources?

The programme-level null remains:

> A faithful composition of mature parent methods makes the same protected scientific-transition decisions with equal or better reliability and cost under matched information, evaluator custody, and resources.

## 2. Authoritative checkpoint

The complete machine-readable checkpoint is:

- `research/experiments/results/issue50/sd70/SD70_PREOUTCOME_EXECUTION_CHECKPOINT_V1.json`

Key identities before this audit:

- `main`: `4165dd2d3c621d9f60e0ff492560baf3afbf7c5f`
- hardening head: `84be48505441d296b255e469b1bb53d734502056`
- protocol blob: `21f4e5b05397a895b47e8a57705a24e770c485ae`
- original suite runner blob: `89a4843eb1ea7af173adba91242321a58efeba04`
- original suite runner SHA-256: `935ec12be7a82f31e8194c0fc9442d7aebe86c1c9e977d8f2316367ae1874f07`

No protected input manifest or seed commitment exists. That absence is preserved rather than filled retrospectively.

## 3. Pre-outcome implementation defect and repair

### Reproduced counterexample

A one-task synthetic known-answer fixture used an arm process that:

1. exited with code `0`;
2. wrote `status = EXECUTION_FAILED_MODEL_RESPONSE`;
3. selected no action;
4. had no private-oracle access.

The original runner returned success, wrote `all_returncodes_zero = true`, and the evaluator counted the failed response as `completed = 1`.

Frozen counterexample:

- `research/experiments/results/issue50/sd70/SD70_IMPLEMENTATION_FAILURE_COUNTEREXAMPLE_V1.json`

### Narrow correction

Only execution fidelity was changed. The suite runner now:

- validates every expected response, including pre-existing responses skipped by execution;
- requires exact task and arm identity;
- requires `status = COMPLETED_PROPOSAL_ONLY`;
- requires the selected action to belong to the frozen candidate set;
- distinguishes process success from response integrity;
- records `all_responses_completed` and `dispatch_integrity_passed`;
- fails closed before evaluation on any missing, malformed, failed, mismatched, or out-of-candidate response;
- validates the same contract again when evaluation is invoked directly;
- preserves the existing private-oracle removal and hash-exact restoration path.

This repair does not select a parent, define an outcome, alter a threshold, inspect an oracle, or change the generated task distribution. It is an implementation-fidelity amendment, not a scientific-design amendment.

### Verification

Local synthetic verification environment:

- CPython `3.13.5`
- Linux `6.18.35`, x86_64, glibc `2.41`
- pytest `9.0.2`
- Codex CLI unavailable and not substituted

Checks:

- `4 passed` in the targeted SD70 integrity suite;
- patched runner and test compile successfully;
- valid known-answer fixture scores exactly `1/1`;
- failed zero-exit response is rejected;
- pre-existing failed response is rejected rather than accepted through empty-`all()` semantics;
- missing response is rejected;
- private oracle is absent during child execution and restored byte-exactly.

These are engineering checks only.

## 4. Scientific-design audit

The protected computation was not run because the frozen science and executable comparison are not equivalent.

| Gate | Disposition | Evidence/objection |
|---|---|---|
| Study identity and dependency | PASS | SD70 is routed and SD00 is complete. |
| Protected-outcome custody | PASS for scaffold | Oracle removal/restoration is implemented and rechecked synthetically. No protected suite exists. |
| Response integrity | FAIL in original; GREEN after narrow repair | Original zero-exit failure counterexample preserved. |
| Strongest-parent fidelity | FAIL / `CANNOT_CHECK` | V1 names mature science-of-science, temporal, network and causal parent classes; the executable exposes five prompt-defined arms without a prospective mapping or a faithful strongest-parent implementation. |
| Information parity | FAIL | `TARGET_ONLY_DIRECT` is told not to use trajectories but physically receives them. Prompt wording is not an information barrier. |
| Registered primary estimands | FAIL | V1 registers protected decision quality, critical false direction, resource cost and parent non-regression; the evaluator emits only response count, exact correct count and raw accuracy. |
| Missingness/censoring | FAIL | No SD70-specific rule is frozen. The original code silently treated model failure as completed. |
| Statistical decision rule | FAIL | No minimum effect, uncertainty procedure, multiplicity rule, non-inferiority margin, or terminal computation is bound. |
| Required mechanism tests | FAIL | No frozen negative controls or causal ablations are executed by the current runner. |
| Resource parity | `CANNOT_CHECK` | One call per arm-task is specified, but no common token/output/retry/total-compute budget is frozen. |
| Seed/input freeze | NOT REACHED | The protected suite and commitment have not been created; they remain unavailable. |

These gaps cannot be repaired by adding fields to the evaluator after protected outcomes. They determine the comparison itself. Continuing V1 would create numbers that cannot answer the registered question and could not adjudicate the strongest null.

## 5. Hostile-team adjudication

- **Experimental-methods lead:** objects that the V1 executable has no prospective arm-to-parent mapping, no effect estimand, and no missingness rule. Outcome access is therefore forbidden.
- **Systems/computation lead:** accepts the response-integrity repair as narrow and outcome-blind, but rejects any claim that green tests authorize the model run.
- **Statistics/evaluation lead:** objects that raw accuracy alone cannot instantiate four registered outcomes, uncertainty, parent non-regression, or a terminal.
- **Parent-baseline expert:** objects that `F0_PARENT_FEDERATION` is a natural-language instruction, not evidence that mature parents were faithfully composed or strengthened.
- **Adversarial reviewer:** objects that all arms physically receive the full request, that resource parity is incomplete, and that a disappointing result could otherwise invite post-hoc baseline or metric definition.
- **Scientific editor:** permits only the narrow terminal below; no positive field claim and no flagship result paragraph are warranted.

No role identified a valid route to execute V1 without changing the scientific design.

## 6. Registered results

There are **no registered SD70 scientific results**.

- Protected responses: none.
- Protected primary outcomes: none.
- Required controls/ablations: not run.
- Parent comparison: not run.
- Outcome interpretation: prohibited.

The synthetic counterexample and four passing tests are engineering evidence only.

## 7. Scientific terminal

```text
SD70_V1_ENGINEERING_EXECUTION_STATUS = PREOUTCOME_AUDIT_COMPLETE__FAIL_CLOSED_REPAIR_GREEN
SD70_V1_SCIENTIFIC_EVIDENCE_STATUS = NO_PROTECTED_OUTCOMES_INSPECTED__NO_RESULT
SD70_V1_SCIENTIFIC_TERMINAL = REQUIRES_NEW_PROSPECTIVE_VERSION
MACHINE_EPISTEMICS_FIELD_CLAIM_STATUS = FIELD_RESIDUAL_NOT_ESTABLISHED
FLAGSHIP_PUBLICATION_STATUS = UNCHANGED__V20_SUBMISSION_READY_FALSE__V20_PUBLICATION_READY_FALSE
```

`REQUIRES_NEW_PROSPECTIVE_VERSION` is used rather than `CANNOT_CHECK` because the blocking gaps define the parent comparison, estimands, information contract and decision rule. Fixing them changes the scientific design. V1 is stopped before protected generation rather than laundered through an implementation amendment.

## 8. Prospective successor

A non-authorizing V2 design surface is created at:

- `research/experiments/SCIENTIFIC_DEVELOPMENT_SD70_PROSPECTIVE_PROTOCOL_V2.json`

It narrows the synthetic study to rule-induction mechanism evidence; requires executable mature parent baselines, physical per-arm information manifests, all four outcomes, negative controls, ablations, resource budgets, seed custody, missingness and statistical terminals; and explicitly denies field or publication authority.

V2 remains:

```text
PROSPECTIVE_PREOUTCOME_DRAFT__NOT_EXECUTION_AUTHORIZED
```

No protected seed may be generated until its listed blockers are closed prospectively.

## 9. Claim consequences

- The Machine Epistemics programme survives as a provisional, falsifiable research programme.
- No Machine Epistemics residual is supported by SD70.
- Parent sufficiency remains fully live and is strengthened as the required null.
- The generated SD70 scaffold remains useful integration engineering after the fail-closed repair.
- The V1 synthetic task cannot establish naturalistic scientific-development superiority or a field residual.
- No sentence in the V20 Perspective is authorized for expansion. The existing posture—`PROGRAMME_SURVIVES`, `FIELD_RESIDUAL_NOT_ESTABLISHED`, submission/publication false—remains correct.

## 10. Deviations and forbidden actions

Deviation recorded:

- The scheduled V1 dispatch was found pre-outcome to lack a scientifically complete comparison contract.

Disposition:

- hold or cancel `o2-sd70-r1`;
- do not generate V1 protected inputs;
- do not inspect or import any V1 output accidentally produced after this stop declaration;
- do not retrofit parent mappings, metrics, exclusions, thresholds, reruns or resource budgets after oracle access;
- do not treat the code repair or synthetic tests as field evidence.

## 11. Single next scientifically authorized action

Implement and development-test the **strongest generator-faithful mature parent suite**, then freeze its selection rule and the complete V2 evaluator/resource/information contract **before any protected seed is generated**.

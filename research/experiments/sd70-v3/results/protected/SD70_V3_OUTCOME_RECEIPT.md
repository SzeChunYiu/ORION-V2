# SD70-V3 — Protected Outcome Receipt (V1)

**Terminal route: `PARENT_SUFFICIENT`**

Design sha256 `662837355020658ab77fc6067060df1b105e54ad757caf0378925178a7723138` (identical to the frozen design; `evaluate` refuses otherwise). Protected tasks 240. Comparator MAXMARGIN_PARENT (frozen on the V3 development split before generation).

## Primary estimand

Δ = acc(F2_RECURSIVE_META_DISCOVERY_FULL) − acc(comparator) = **-0.0083** (95 % bootstrap CI [-0.0500, 0.0333], McNemar mid-p one-sided 0.6445, discordant b=13 c=15, n=240).

Registered minimum effect 0.10; non-inferiority margin −0.05.

## Arm results

| arm | n | exact accuracy | Wilson 95 % | CFD rate | arm failures |
|---|---|---|---|---|---|
| F0_PARENT_FEDERATION | 240 | 0.7208 | [0.6609, 0.7738] | 0.0417 | 0/240 |
| PAIRWISE_LINEAR_PARENT | 240 | 0.7042 | [0.6436, 0.7583] | 0.0500 | 0/240 |
| F2_FULL_MINUS_FAILURE_EVIDENCE | 240 | 0.7000 | [0.6392, 0.7545] | 0.0375 | 0/240 |
| PERCEPTRON_PARENT | 240 | 0.7000 | [0.6392, 0.7545] | 0.0417 | 0/240 |
| F2_STATIC_NO_RECURSION | 240 | 0.6917 | [0.6306, 0.7467] | 0.0417 | 0/240 |
| MAXMARGIN_PARENT | 240 | 0.6917 | [0.6306, 0.7467] | 0.0458 | 0/240 |
| STRONGEST_GENERATOR_FAITHFUL_PARENT | 240 | 0.6917 | [0.6306, 0.7467] | 0.0458 | 0/240 |
| F2_RECURSIVE_META_DISCOVERY_FULL | 240 | 0.6833 | [0.6220, 0.7389] | 0.0417 | 0/240 |
| FIXED_META_LESSON | 240 | 0.6458 | [0.5835, 0.7036] | 0.0583 | 0/240 |
| DECISION_LIST_PARENT | 240 | 0.6333 | [0.5707, 0.6918] | 0.0542 | 0/240 |
| F2_FULL_MINUS_PARENT_FEDERATION | 240 | 0.6333 | [0.5707, 0.6918] | 0.0500 | 0/240 |
| NAIVE_BAYES_PARENT | 240 | 0.6250 | [0.5622, 0.6838] | 0.0750 | 0/240 |
| MATCHED_CASE_PARENT | 240 | 0.5875 | [0.5243, 0.6479] | 0.0875 | 0/240 |
| SIMPLE_FREQUENCY_PARENT | 240 | 0.5375 | [0.4743, 0.5995] | 0.1125 | 0/240 |
| TARGET_ONLY_NEGATIVE_CONTROL | 60 | 0.3167 | [0.2131, 0.4423] | 0.2667 | 0/60 |
| TARGET_ONLY_DETERMINISTIC | 240 | 0.2500 | [0.1994, 0.3084] | 0.3625 | 0/240 |

Chance level 0.2614.

## Negative controls (each with its denominator)

| control | n | accuracy | Wilson 95 % lower | chance | behaves |
|---|---|---|---|---|---|
| F2_RECURSIVE_META_DISCOVERY_FULL__LP | 60 | 0.3000 | 0.1990 | 0.2711 | True |
| F2_RECURSIVE_META_DISCOVERY_FULL__QS | 60 | 0.2833 | 0.1851 | 0.2711 | True |
| STRONGEST_GENERATOR_FAITHFUL_PARENT__LP | 240 | 0.2125 | 0.1655 | 0.2614 | True |
| STRONGEST_GENERATOR_FAITHFUL_PARENT__QS | 240 | 0.2875 | 0.2339 | 0.2614 | True |
| TARGET_ONLY_DETERMINISTIC | 240 | 0.2500 | 0.1994 | 0.2614 | True |
| TARGET_ONLY_NEGATIVE_CONTROL | 60 | 0.3167 | 0.2131 | 0.2711 | True |

## Registered gates

| gate | value |
|---|---|
| cost_within_budget | True |
| critical_false_direction | True |
| effect_minimum | False |
| effect_significant_holm | False |
| mechanism_recursion | False |
| model_negative_controls_behave | True |
| no_ablation_beats_full | True |
| non_regression | False |
| parent_ties_or_exceeds_f2 | True |

## Ablations

| ablation | Δ vs full | CI | mid-p |
|---|---|---|---|
| no_failure_evidence | -0.0167 | [-0.0583, 0.0250] | 0.7709 |
| no_parent_federation | 0.0500 | [0.0125, 0.0917] | 0.007317 |
| no_recursion | -0.0083 | [-0.0458, 0.0292] | 0.6682 |

## Silent-failure audit

**1. Counters that never ran.** Every count below is reported with its denominator.

Envelope homogeneity verdict `CHANNEL_CONTRACT_OK` over **1140 completed model envelopes** (0 failed envelopes excluded — those are the missingness gate's business).

| check | value | denominator | passed |
|---|---|---|---|
| comp_hash_consistency | observable 1140, mismatches 0 | 1140 | True |
| input_tokens_linear_model_residual_within_tolerance | 1.0000 | 1140 | True |
| reasoning_cap_exceed_fraction | 0.0000 | 1140 | True |
| requested_model_matches_design | 1.0000 | 1140 | True |
| usage_observed_fraction | 1.0000 | 1140 | True |

**Channel contract verdict `CHANNEL_CONTRACT_OK`**, measured at campaign start AND end on byte-frozen canaries.

| check | denominator | passed |
|---|---|---|
| canary_dispatch_succeeded | 18 | True |
| canary_prompts_byte_identical_to_frozen | 18 | True |
| served_manifest_observable | 18 | True |
| comp_hash_matches_frozen | 18 | True |
| served_slug_prefix_matches_frozen | 18 | True |
| target_model_still_advertised | 18 | True |
| canary_token_behaviour_stable | 9 | True |
| canary_answer_tokens_unchanged | 3 | True |

**2. Contrasts that could not exist.** Asserted, not assumed:

| pair | shared tasks | requests differing | prompts differing |
|---|---|---|---|
| F2_RECURSIVE_META_DISCOVERY_FULL vs F2_STATIC_NO_RECURSION | 240 | 240/240 | 240/240 |
| F2_RECURSIVE_META_DISCOVERY_FULL vs F2_FULL_MINUS_FAILURE_EVIDENCE | 240 | 240/240 | 240/240 |
| F2_RECURSIVE_META_DISCOVERY_FULL vs F2_FULL_MINUS_PARENT_FEDERATION | 240 | 240/240 | 240/240 |

- **True** — F2_FULL_MINUS_PARENT_FEDERATION has no parent_advisory ({'denominator': 240, 'violations': 0})
- **True** — F2_FULL_MINUS_FAILURE_EVIDENCE has no FAILURE episode ({'denominator': 240, 'violations': 0})
- **True** — POSITIVE CONTROL: the full arm DOES carry parent_advisory and FAILURE episodes (if this fails the two checks above are vacuous) ({'advisory_present': 240, 'denominator': 240, 'failure_present': 240})

**3. Sentences nobody executed.** `evaluate` re-checks the design sha256 against the frozen suite and refuses on mismatch; the interpreter-determinism boundary was measured across three CPython versions rather than asserted (see the design, §13); the failure path was rehearsed with a failing stub before the protected run.

**4. Rendered status trusted in place of the thing.** The terminal route above is computed from the arm records, not read from any status line. Landing is decided by `git merge-base --is-ancestor`, not by a PR badge.

## Resource cost

| arm | model calls | attempts | retries | input tokens | output tokens | wall s |
|---|---|---|---|---|---|---|
| F2_FULL_MINUS_FAILURE_EVIDENCE | 240 | 240 | 0 | 3983201 | 128547 | 11109 |
| F2_FULL_MINUS_PARENT_FEDERATION | 240 | 240 | 0 | 3970448 | 181917 | 11854 |
| F2_RECURSIVE_META_DISCOVERY_FULL | 240 | 240 | 0 | 4140356 | 169416 | 11665 |
| F2_RECURSIVE_META_DISCOVERY_FULL__LP | 60 | 60 | 0 | 1033033 | 45532 | 3012 |
| F2_RECURSIVE_META_DISCOVERY_FULL__QS | 60 | 60 | 0 | 1032842 | 37663 | 2856 |
| F2_STATIC_NO_RECURSION | 240 | 240 | 0 | 4034675 | 148507 | 9749 |
| TARGET_ONLY_NEGATIVE_CONTROL | 60 | 60 | 0 | 882002 | 11871 | 1709 |

## Authority

This receipt grants nothing: no scientific truth, no causal law, no field status, no submission or publication readiness. A null here means **no residual detectable in the registered decision problems the parents already solve exactly** — never that no residual exists. MAXMARGIN_PARENT is optimal by construction on this generator family up to its regularization and optimizer budget; that was declared in the frozen design, not discovered here.

Run authorization `ARCHIVED_POST_RUN__AUTHORIZATION_PRECEDED_DISPATCH` is archived on completion, re-arming the guard against a second protected dispatch. SD70-V2's separate authorization remains unspent and its `PARENT_SUFFICIENT` expectation remains unobserved.


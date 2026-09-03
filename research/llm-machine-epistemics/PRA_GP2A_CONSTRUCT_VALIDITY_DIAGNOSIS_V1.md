# PRA GP2a — construct-validity diagnosis of the R0/R3 probe asymmetry

**Scope.** Diagnoses the GP2a divergence recorded in `results/pra-llm-r1/OUTCOME_RECEIPT_R1.md`
§6 and the open anomaly reported there. Reproduces both from the frozen R1 artifacts. Grants no
scientific authority, changes no frozen input, and touches nothing belonging to the in-flight V2
campaign. Its conclusions are the premises of `PRA_REAL_LLM_AUDIT_DESIGN_V3.{md,json}`.

**No new model calls were made.** Everything below is computed from the frozen design, the frozen
V1 runner blob, and the R1 rollup that is already in the repository.

---

## 1. Custody — the inputs are the ones R1 actually ran

| input | sha256 | check |
|---|---|---|
| design V1 (`PRA_REAL_LLM_AUDIT_DESIGN_V1.json`, `origin/main`) | `2f893db5…0061` | equals the value the R1 receipt records |
| V1 runner blob at the V1 freeze `94c9da4` | `e25d969f…e490` | equals `runner_sha256` in the R1 rollup |
| runner on `origin/main` | `19862623…fda7f` | the later V2 superset — **not** R1's input, and not read here |

The V1 protected seed (`20260903`) is revealed, V1 being complete, so the exact R1 suite can be
regenerated. Running the frozen V1 runner's `generate_suite` on the frozen V1 design produces:

```
regenerated suite sha256 : 21b5b0f7263a49732a9d7c6ba4c417b825e363d2ed06df66d1b3a6a26551b2ae
rollup    suite sha256   : 21b5b0f7263a49732a9d7c6ba4c417b825e363d2ed06df66d1b3a6a26551b2ae
```

**Byte-identical, 500 instances.** *Control that must match:* regenerating the **dev** split
through the same code path yields a different digest, so the comparison is live and not a
tautology of the function returning its own argument.

## 2. The registered text versus the executed code

Registered, in both the V1 and V2 design JSON (`gates.GP2.rule`):

> GP2a (required): probe decodes support_source under **R0 and R3** (>= 0.80), is at chance under
> R2_TRUE_REMOVAL (<= 0.65), and true-removal accuracy is below R0 by >= 0.15.

Executed, in the frozen runner:

```python
r0_acc, rem_acc, kv_acc = _acc("R0"), _acc("R2_TRUE_REMOVAL", "R2"), _acc("R2_TEXT_REMOVED_KV_RETAINED")
pos_ok = r0_acc is not None and r0_acc >= g["GP2"]["probe_positive_control_min_acc"]
```

`R3` does not appear. The clause has no implementing predicate at all — it is not a threshold set
wrongly, it is a sentence nobody executed. The R1 lane logged this as `CANNOT_CHECK`, distinct
from `pass`, which was the correct call, and the R1 terminal is unaffected because `model_terminal`
evaluates GP3 before GP2.

## 3. The measurements

Probe = mass-mean difference direction, hidden state of the last prompt token, **max over layers**
(29 for qwen, 33 for mistral), `n_test = 96` in every cell, on `F3_P2_CANON`.

| condition | qwen2.5-7b | mistral-7b-v0.3 | contains a roster? | names the basis? |
|---|---|---|---|---|
| R0 | **1.000** | **0.917** | yes | yes |
| R1 | 0.563 | 0.552 | yes | no |
| R2 | 0.510 | 0.573 | no | no |
| R2_TRUE_REMOVAL | 0.510 | 0.573 | no | no |
| R3 | 0.542 | 0.594 | no | **yes** |
| R2_TEXT_REMOVED_KV_RETAINED | 0.979 | 0.896 | in the retained KV | in the retained KV |

The briefed hypothesis was that the probe keys on R0 surface features. **The finding is sharper
and mechanically different, and one half of that hypothesis is false.** Both halves below are
established from the existing data.

### 3a. A lexical surface reader cannot do R0 either

The same mass-mean estimator, run on word and character-4-gram counts of the exact R1 stimuli with
the exact frozen instance split, scores **0.4896 on R0** — chance. Source names are episode-local
nonces, so no lexical feature survives the instance split. The model at 1.000 is doing genuine
within-context relational work, not lexical recall.

### 3b. A *relational* rule does R0 perfectly, and is undefined everywhere else

The rule "is the source named in the support entry the **first** name in the roster line?" scores:

```
R0                             applicable 96/96   accuracy 1.0000
R1, R2, R3, R2_TRUE_REMOVAL, R2_TEXT_REMOVED_KV_RETAINED   applicable 0/96
```

V1 always rendered the roster in generator order `A, B, Z`, and the label was `1 iff support_set ==
["A"]`. So "roster slot 1" *is* the label, exactly, with no notion of what "basis" means.

## 4. Why R3 reads at chance: the label is not identifiable there

R3 renders as `base + "Recorded basis for claim <id>: <name> [<id>] alone."` — it names the
recorded support and carries **no roster**. The label `support_source (A=1, B=0)` is an index into
the generator's `sources` dict. Its only textual footprint anywhere is roster order.

Formally, let σ be the exchange of the two candidate sources. `A` and `B` are drawn i.i.d. from one
`_nonce_source` distribution, so the law of the suite is σ-invariant. Over the 120 frozen
`F3_P2_CANON` instances:

```
condition                       arms identical   exact A<->B exchange   asymmetric
R0                                    0                  0                120     -> identifiable
R1                                  120                  0                  0     -> not
R2                                  120                  0                  0     -> not
R3                                    0                120                  0     -> not
R2_TEXT_REMOVED_KV_RETAINED         120                  0                  0     -> not (by text)
R2_TRUE_REMOVAL                     120                  0                  0     -> not
R4                                    0                  0                120     -> identifiable
```

Under R3 the two arms of every single instance are an **exact σ-exchange of one another**, while
the label flips. For every capture unit there is an equally likely unit with the same text and the
opposite label, so the expected accuracy of *any* measurable classifier on R3 is **exactly 0.5**.
This is a theorem about the stimulus, not an observation about the models.

The exchangeability premise is checkable and checked: a classifier trained to tell an `A`-name from
a `B`-name scores **0.4583** on held-out instances.

R1, R2, R2_TRUE_REMOVAL and the KV *text* have their two arms rendering **identically**, so the
label is not even a function of the text. (The KV condition still reads 0.979/0.896 because its
effective context includes the retained R0 prefix, which does carry the roster — the reason V3
certifies the *effective context* rather than the text.)

**Every condition the probe reads above chance is one whose effective context contains both a
roster and a support statement. Every condition it reads at chance lacks one of them. R3 contains
the recorded support and still reads at chance, because what the probe was asked to decode was
never the recorded support — it was the generator's index for it.**

### The observed R3 values are inside the null

The gate statistic is a max over layers, reported without a null band. For `n_test = 96`:

| value | P(one layer ≥) | P(max of 33 layers ≥) |
|---|---|---|
| qwen R3 = 0.5417 | 0.238 | 0.9999 |
| mistral R3 = 0.5938 | 0.041 | 0.750 |
| mistral R0 = 0.9167 | 1.8e-18 | < 1e-16 |

0.542 and 0.594 are unremarkable draws. The single-layer p of 0.041 for mistral would have looked
"significant" had the selection over 33 layers not been priced in.

## 5. All three GP2a clauses were structurally determined, in both directions

| registered clause | status |
|---|---|
| decodes under **R0** ≥ 0.80 | passable — but achievable by a positional rule with no semantics |
| decodes under **R3** ≥ 0.80 | **UNSATISFIABLE in principle.** Expected accuracy is exactly 0.5 |
| at chance under **R2_TRUE_REMOVAL** ≤ 0.65 | **UNFAILABLE in principle.** The two arms render identically, so the probe is pinned at chance whatever the model does |
| true-removal below R0 by ≥ 0.15 | **UNFAILABLE** whenever R0 is identifiable, for the same reason |

This is the decisive correction to the brief's framing of the repair. **Implementing GP2a as
registered would not have produced a confidently wrong number — it would have produced a
permanently unpassable gate**, one that in every future run reports `CANNOT_CHECK` and reads like
an empirical negative about model retention. And the sibling clause that *did* run reported
`probe_R2_true_removal_at_chance = True` in both models, a `0 violations` that could never have
been anything else. The R1 receipt caught the `hidden_R2`/`hidden_R2_TRUE_REMOVAL` byte-identity
and called it "one measurement reported twice"; the sharper point is that the clause consuming
that measurement was incapable of failing its threshold.

## 6. Why no test caught it

The V1/V2 test double plants its probe direction as `1.0 if the basis is the first name on file
else -1.0`. Under R3 there is no roster line, so `first_on_file` is `None` and the planted
direction is a **constant** for both arms:

```
R0  arm=hA  roster ids found=1  planted direction= 1.0
R0  arm=hB  roster ids found=1  planted direction=-1.0
R3  arm=hA  roster ids found=0  planted direction=-1.0
R3  arm=hB  roster ids found=0  planted direction=-1.0
```

Its docstring nevertheless states that "the probe decodes it under R0/**R3**/KV-retained only".
The test double implemented the very positional shortcut the probe turned out to be using, and made
the R3 assertion unwritable. That is silent-failure shape 3 sitting inside the test harness, and it
is why the divergence survived to a protected run.

## 7. What this data can and cannot settle

**Settled.** The R0/R3 asymmetry is fully explained by label non-identifiability under R3. No
model-side explanation is needed, and none is licensed. The GP2a clause structure is
non-diagnostic in the ways tabulated in §5.

**Not settled, and not settleable from R1.** Whether the model's R0 = 1.000 reflects a semantic
representation of *the recorded basis* or a positional/relational binding of *the first name on
file*. In V1 the two are perfectly confounded: the label is roster slot 1, so both accounts predict
1.000 exactly. The lexical null failing at 0.4896 rules out lexical recall and nothing more. No
re-analysis of the R1 artifacts can separate them, because the stimuli never varied the thing that
would separate them. **V3 is designed to answer it** — by randomising roster order, so a positional
reader is destroyed by construction, and by carrying a relational surface null calibrated to fire
on exactly this known-bad case.

## 8. What V1's honest limitations become in V3

| V1 limitation | V3 |
|---|---|
| `hidden_R2.npy` ≡ `hidden_R2_TRUE_REMOVAL.npy` by construction — one measurement twice | condition **removed**; its gate limb is discharged a priori by the identifiability certificate, which proves the two arms are the same string |
| `p0_R2_vs_R3` at 1.000 vs 1.000 was a real ceiling, shown non-vacuous by the same code path returning 0.246 vs 0.529 elsewhere | that witness is **registered per contrast** and emitted into the rollup (`contrast_D_same_path_witness`), not reconstructed by a reader afterwards |
| `revision_requested` / `revision_resolved` asserted from `model.config._commit_hash` under `HF_HUB_OFFLINE=1` | carried verbatim, with the stated caveat that a snapshot revision is not a weight-shard digest |
| V1's terminal `CONTROL_FAILURE__SUITE_NOT_INTERPRETABLE`, attributed to the revision stage (`F3_P2_MIRROR` false revision 0.258 / 0.392 against ≤ 0.10) | **stands, unchanged.** Model competence, not a suite defect; V3 does not redesign around it |

## 9. Reproduction

Every number above comes from the frozen design, the frozen V1 runner blob (`git show
94c9da4:research/llm-machine-epistemics/pra_real_llm_audit.py`) and
`results/pra-llm-r1/PRA_REAL_LLM_AUDIT_ROLLUP_V1.json`. The identifiability certificate, the
surface nulls and the max-over-layers null band are implemented in `pra_real_llm_audit_v3.py`
(`certify_label_identifiability`, `surface_null_accuracies`) and are exercised against this
known-bad case by `tests/unit/test_pra_real_llm_audit_v3.py`
(`test_v1_label_is_flagged_not_identifiable_under_R3`,
`test_surface_null_must_include_a_relational_reader`) — a checker validated on the defect it
exists to find, with the no-alarm case asserted alongside.

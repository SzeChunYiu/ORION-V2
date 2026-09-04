# 02 — Registered clauses whose verdict was fixed before the run

Detail file of `2026-09-silent-failure-modes-relocation`. Read `README.md` first.

All four records are the PRA real-LLM audit's `GP2a` clause family. They are kept together because
they are a **matched set**: one clause the runner narrowed, one that could never have passed, two
that could never have failed, and the confound that made the whole family look like it was
measuring something. Each of the middle two reads, in a receipt, as an ordinary empirical result.

Primary source for D19-D21: `research/llm-machine-epistemics/PRA_GP2A_CONSTRUCT_VALIDITY_DIAGNOSIS_V1.md`
on branch `design/pra-v3-gp2a-construct-validity` (`21760ff`), read 2026-09-04.

---

## D6 — A registered clause the runner silently narrows (PRA GP2a)

**Class** `REGISTERED_SCOPE_DIVERGENCE` · **Status** `REALISED`, deliberately unpatched

The registration disagrees with itself. `PRA_REAL_LLM_AUDIT_DESIGN_V1.json:220` (and `V2.json:264`,
identical): *"GP2a (required): probe decodes support_source under R0 **and R3** (>= 0.80) …"*. The
registration Markdown at `PRA_REAL_LLM_AUDIT_DESIGN_V1.md:105` says *"probe decodes under R0 (≥
0.80)"* — R0 only. The runner matches the Markdown and diverges from the JSON:
`pra_real_llm_audit.py:1428-1429` computes `r0_acc` and sets
`pos_ok = r0_acc is not None and r0_acc >= g["GP2"]["probe_positive_control_min_acc"]`.

**The nomination understates it: the clause did not merely "pass on half of what it promised" — it
passed, and the unevaluated half would have flipped it.** The frozen rollup
`results/pra-llm-r1/PRA_REAL_LLM_AUDIT_ROLLUP_V1.json` records `"GP2a_true_removal_effective": true`
and `"pass": true` for both models, **while probing R3 all along**: mistral-7b-instruct-v0.3 at
`R3: 0.59375` (R0 `0.917`), qwen2.5-7b-instruct at `R3: 0.5416666` (R0 `1.0`), `n_test: 96` each —
both far below the `0.80` threshold. `OUTCOME_RECEIPT_R1.md` §6: *"Had the clause been implemented
as written, `probe_positive_control_ok` would be False in both models and GP2 would have mapped to
`CANNOT_CHECK_ALTERNATE_CHANNEL_RETENTION`."*

**State the unit precisely.** GP2a as a whole runs and returns a verdict; it is **the R3 half of its
positive control** that never does. §6: *"The R3 clause is never evaluated."*

**Bounded and deliberate.** §6: *"The terminal is unaffected. `model_terminal` evaluates GP3 before
GP2, so `CONTROL_FAILURE__SUITE_NOT_INTERPRETABLE` stands on GP3 regardless."* And: *"This
divergence will recur in V2, and is deliberately not patched … Both the V1 and V2 designs are frozen
and the V2 protected seed is already sealed."* §6 assigns the correct status: *"`CANNOT_CHECK`,
distinct from `pass` … must not be read as checked-and-fine."*

**Superseded in one respect by D19.** The receipt's counterfactual — that implementing R3 as written
would have yielded `CANNOT_CHECK` — is right about the verdict and understates the cause. D19 shows
the clause is unsatisfiable *in principle*, so implementing it would have produced a permanently
unpassable gate, not a one-run `CANNOT_CHECK`.

---

## D19 — A registered clause that is unsatisfiable in principle (PRA GP2a, R3)

**Class** `STRUCTURALLY_DETERMINED_REGISTERED_CLAUSE` · **Status** `NEAR_MISS` — the clause was
never implemented, and diagnosing why is what stopped it

R3 renders as `base + "Recorded basis for claim <id>: <name> [<id>] alone."` — it names the recorded
support and **carries no roster**. The label `support_source (A=1, B=0)` is an index into the
generator's `sources` dict, whose only textual footprint anywhere is roster order.

Let σ be the exchange of the two candidate sources. `A` and `B` are drawn i.i.d. from one
`_nonce_source` distribution, so the law of the suite is σ-invariant. Over the 120 frozen
`F3_P2_CANON` instances (diagnosis §4):

```text
condition                       arms identical   exact A<->B exchange   asymmetric
R0                                    0                  0                120     -> identifiable
R3                                    0                120                  0     -> not
R2_TRUE_REMOVAL                     120                  0                  0     -> not
```

Under R3 the two arms of **every** instance are an exact σ-exchange of one another while the label
flips. For every capture unit there is an equally likely unit with the same text and the opposite
label, so the expected accuracy of *any* measurable classifier on R3 is **exactly 0.5**. The
diagnosis states the grade correctly: *"This is a theorem about the stimulus, not an observation
about the models."* The exchangeability premise is itself checked — a classifier trained to tell an
`A`-name from a `B`-name scores **0.4583** on held-out instances.

**The consequence, which is the reason this is recorded rather than filed as a near-miss and
forgotten:** *"Implementing GP2a as registered would not have produced a confidently wrong number —
it would have produced a permanently unpassable gate, one that in every future run reports
`CANNOT_CHECK` and reads like an empirical negative about model retention."* A clause that cannot be
satisfied manufactures a finding; it does not miss one.

**The observed R3 numbers are inside the null.** The gate statistic is a max over 33 layers reported
without a null band. At `n_test = 96`, qwen's `0.5417` has single-layer p 0.238 (max-of-33 0.9999)
and mistral's `0.5938` has 0.041 (max-of-33 0.750), against mistral's R0 `0.9167` at 1.8e-18. The
single-layer p of 0.041 *"would have looked significant had the selection over 33 layers not been
priced in."*

---

## D20 — Two registered clauses that are unfailable by construction (PRA GP2a siblings)

**Class** `STRUCTURALLY_DETERMINED_REGISTERED_CLAUSE` · **Status** `REALISED` — one of the two ran
and reported a zero-violation pass

The same diagnosis §5 tabulates the whole clause family, and the two remaining clauses are pinned in
the other direction:

| registered clause | status |
|---|---|
| at chance under **R2_TRUE_REMOVAL** ≤ 0.65 | **UNFAILABLE in principle** — the two arms render identically, so the probe is pinned at chance whatever the model does |
| true-removal below R0 by ≥ 0.15 | **UNFAILABLE** whenever R0 is identifiable, for the same reason |

The first of these was executed. It reported `probe_R2_true_removal_at_chance = True` in both
models — *"a `0 violations` that could never have been anything else"*. The R1 receipt had already
noticed the `hidden_R2`/`hidden_R2_TRUE_REMOVAL` byte-identity and called it *"one measurement
reported twice"*; the sharper point the diagnosis adds is that **the clause consuming that
measurement was incapable of failing its threshold**.

**Why no test caught it (diagnosis §6).** The V1/V2 test double plants its probe direction as
`1.0 if the basis is the first name on file else -1.0`. Under R3 there is no roster line, so
`first_on_file` is `None` and the planted direction is a constant for both arms:

```text
R0  arm=hA  roster ids found=1  planted direction= 1.0
R0  arm=hB  roster ids found=1  planted direction=-1.0
R3  arm=hA  roster ids found=0  planted direction=-1.0
R3  arm=hB  roster ids found=0  planted direction=-1.0
```

Its docstring nevertheless states that *"the probe decodes it under R0/R3/KV-retained only"*. The
test double implemented the very positional shortcut the probe turned out to be using, and made the
R3 assertion unwritable — the same defect sitting inside the harness that was supposed to catch it.

**D19 and D20 are one finding in two directions,** and both read as results: an unsatisfiable clause
reads as an empirical negative, an unfailable one as a clean pass. Neither has a denominator to
interrogate.

---

## D21 — A confound mistaken for a surface artifact (PRA GP2a, R0)

**Class** `NONIDENTIFIABLE` (existing) · **Status** `NEAR_MISS` — the confound was diagnosed
before it was read as evidence, and no protected or frozen artifact carried it

The nominating hypothesis was that the probe keyed on **lexical surface**. It is false, and the
diagnosis falsifies it with a control: a lexical surface reader on the exact frozen instance split
scores **0.4896 on R0** — chance. Source names are episode-local nonces, so no lexical feature
survives the instance split (§3a).

What does work is **relational**. The rule *"is the source named in the support entry the first name
in the roster line?"* scores `applicable 96/96, accuracy 1.0000` on R0 (§3b). V1 always rendered the
roster in generator order `A, B, Z` and the label was `1 iff support_set == ["A"]`, so **roster slot
1 *is* the label, exactly, with no notion of what "basis" means.**

**What the data can and cannot settle (§7).** Semantic-versus-positional is **not separable from
this data**, because the two accounts are perfectly confounded: the label is roster slot 1, so both
predict `1.000`. *"The lexical null failing at 0.4896 rules out lexical recall and nothing more."*
V3 is designed to answer it — randomised roster order destroys a positional reader by construction,
with a relational surface null calibrated to fire.

**The failure mode being recorded is the diagnosis step, not the probe.** A ruled-out surface
artifact was about to be read as evidence for the semantic account. Ruling out one alternative is
not evidence for the hypothesis when a third account predicts the same number exactly.

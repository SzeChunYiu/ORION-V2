# SD20 Negative Pilot — Paper Interpretation V1

**Source:** `main@93d4339015502ddee45d49ff211541c69c56e56a`, `research/closure/SD20_EXECUTION_RECEIPT_V1.md`  
**Programme owner:** #50 / science owner #49  
**Receipt classification:** `BOUNDED_PILOT_INTERIM__NO_TERMINAL_CLAIM`  
**Purpose:** integrate the newly executed SD20 pilot into the flagship/recursive-development paper ceiling without inflating or ignoring the negative result.

## 1. Executed facts

The pilot acquired complete within-trajectory arXiv version histories for the bounded SD10 slice:

```text
parent multi-version trajectories = 2,067
single-version censored trajectories = 2,933
planned historical version targets = 3,220
observations acquired = 3,220
missing versions = 0
errors/unplanned entries = 0
```

Operator discovery used 3,220 transitions with a trajectory-disjoint train/test split.

## 2. Primary result — honest negative

Mean held-out transition log-score:

```text
SIMPLE marginal frequency baseline       = -1.5714
context-conditional temporal operator    = -1.6535
Delta vs baseline                        = -0.0821
bootstrap 95% CI                         = [-0.1021, -0.0623]
```

The context-conditional operator **underperformed** the marginal baseline.

Three fixed “breakthrough/meta lessons” were substantially worse:

```text
abstract_grows       Delta = -2.6589
authors_nondecreasing Delta = -1.4014
gaps_lengthen         Delta = -1.5694
```

The F0 meta-parent log-linear federation was also worse than the marginal baseline:

```text
Delta = -0.2690
95% CI = [-0.3382, -0.2028]
```

## 3. Stability and cross-domain result

The estimated marginal operator was stable enough that the negative was not merely bootstrap noise:

```text
bootstrap TV mean = 0.0690
bootstrap TV max  = 0.5668 in thin contexts
```

Leave-one-category-out:

```text
0 / 18 evaluated arXiv categories beat the baseline
2 additional categories = TOO_FEW
```

No evaluated category showed beyond-marginal transition regularity under this pilot representation.

## 4. CANNOT_CHECK / censorship

Failed-trajectory explanation remains:

`CANNOT_CHECK`.

Reason: the corpus remains almost entirely outcome-censored; no failed-trajectory labels are invented.

Other unavailable parents/arms on this slice:

- bibliometric science-of-science parent — no fame/citation fields;
- author-network parent — no disambiguated author network;
- causal/quasi-experimental parent — no intervention variation;
- full recursive F2 — SD50 machinery not yet available.

## 5. What this result refutes on this slice

The bounded pilot provides evidence **against**:

- the specific context-conditional operator representation used in SD20 outperforming a simple population marginal;
- the three frozen “breakthrough lesson” heuristics as useful predictors of these arXiv version transitions;
- the tested F0 log-linear parent federation as predictive on the same slice;
- a claim that category/first-vs-later-step conditioning obviously reveals a reusable development operator.

These statements are slice-specific and representation-specific.

## 6. What it does not establish

Per the receipt, the pilot does **not** establish a final recursive-development terminal.

It does not prove:

- that scientific development has no reusable operator structure;
- `POPULATION_REGULARITY_ONLY` as a global terminal;
- a field-level parent win;
- that SD30–SD80 should be abandoned;
- that other transition alphabets, categories, source modes or multi-year samples cannot reveal conditional structure;
- anything about success/failure trajectories because those labels are absent.

The strongest honest reading is:

> On this bounded arXiv version-transition slice, the simplest marginal operator outperformed the tested conditional operator and all registered parent/lesson variants, while the marginal transition distribution itself was stable.

## 7. Flagship consequence

The recursive-development frontier in the flagship should include this as an **early negative calibration result**, not as supporting evidence for a meta-science law.

Recommended insertion:

> An initial bounded pilot already illustrates why recursive scientific-development learning must remain falsifiable. On a 2024 arXiv version-transition slice, a context-conditioned development operator underperformed a simple marginal frequency model, none of 18 evaluable disciplinary categories improved on the baseline, and several plausible fixed “breakthrough” lessons were strongly anti-predictive. The pilot is too narrow for a programme terminal, but it is evidence against treating intuitive historical lessons or extra conditioning as automatically informative.

This paragraph should be omitted from a final Perspective if unpublished programme-specific data would violate the selected content type or create overlap with a future SD paper. If included, the full method/result status must be disclosed and the bounded/no-terminal scope retained.

## 8. Recursive standalone-paper consequence

The standalone SD paper remains **not admitted**.

SD20 makes that gate stricter, not looser:

```text
D1 operator thesis = FAILED_ON_CURRENT_PILOT_REPRESENTATION
D2 meta-policy thesis = NOT_TESTED
D3 failure-learning thesis = CANNOT_CHECK_OUTCOME_CENSORSHIP
D4 higher abstraction = NOT_TESTED
D5 recursive stability = NOT_TESTED
```

Revival must follow the prospectively registered levers or successor protocols; it may not redefine the operator after seeing this loss and call the repaired version the same test.

## 9. Paper-portfolio effect

No new manuscript identity is created.

The result is used as:

- a flagship falsifiability/negative example where policy permits;
- a constraint on #49/#50 scientific-development claims;
- evidence that a recursive-development standalone paper is premature.

It is not used to promote P-A/P-B/P-C/P-D.

## 10. Current terminal

```text
SD20 = BOUNDED_PILOT_INTERIM__NO_TERMINAL_CLAIM
CONDITIONAL_OPERATOR = NEGATIVE_VS_MARGINAL_ON_SLICE
FIXED_BREAKTHROUGH_LESSONS = STRONGLY_ANTI_PREDICTIVE_ON_SLICE
LOO_CATEGORY_GAIN = 0_OF_18
FAILED_TRAJECTORY_LEARNING = CANNOT_CHECK
SD_STANDALONE_PAPER = NOT_ADMITTED
FLAGSHIP_USE = OPTIONAL_BOUNDED_NEGATIVE_CALIBRATION_ONLY
```

# Causalscbench model × training-regime capability census (E40-m1 §5b evidence)

Source tree: `campaign-e40-r3/causalbench/causalscbench` (LUNARC, fs9, scyiu).
Method: `grep -n "TrainingRegime.Observational" models/*.py` + full read of
`causallearn_models.py` (PC/GES wrappers), `arboreto_baselines.py`,
`gies.py`, `data_access/utils/splitting.py`, `apps/main_app.py` (regime dispatch).

## The guard (upstream, verbatim)

`causallearn_models.py`, `PC.__call__`, first statement (grep line 36):

```python
if not training_regime == TrainingRegime.Observational:
    return []
```

Identical stubs (grep lines): `GES` causallearn_models.py:78, both `notears.py`
classes 39/68, `sparsest_permutations.py`:44, `varsortability.py`:48.

This is an upstream **capability declaration**, not a data-path defect: the
observational algorithms declare themselves undefined off-observational data,
and the benchmark encodes that as an empty predicted graph (which then scores
TP=FP=0, wasserstein mean NaN). It fires before any data is touched — hence
run_time ≈ 0.013 s in every interventional-family probe run, including
subset 1.0.

## Census

| Model (`model_name`) | Non-observational regime | Consumes `interventions`? |
|---|---|---|
| `pc` (pinned in E40-m1) | **empty graph** (stub) | never (even observational) |
| `ges` (causallearn) | **empty graph** (stub) | never |
| `notears` (2 classes) | **empty graph** (stub) | never |
| `sparsest_permutations` | **empty graph** (stub) | never |
| `varsortability` | **empty graph** (stub) | never |
| `grnboost2` / `genie3` (arboreto) | runs | **no — ignores `interventions`** (regime-blind; regime only changes the pooled sample set) |
| `gies` | runs | **yes — per-intervention environments** (`gene_to_interventions` → GIES `I`) |
| DCDI variants (`dcdi_models.py`) | runs | yes (interventional by design; heavy) |
| `random_network`, `feature_selection` | runs | no |

Splitter itself (`data_access/utils/splitting.py`) is correct:
`get_interventional()` = `get_partial_interventional(fraction=1.0)` = full
training matrix; `get_observational()` = fraction 0.0 = non-targeting rows
only. The empty graph is produced entirely by the model-side guard.

## Consequence for E40-m1

With `model_name=pc` pinned, the regime fiber is structurally degenerate:
every non-observational choice ⇒ empty prediction ⇒ NaN primary. The F2
agent's cycle-2–4 escape to observational was the only scoreable basin in the
decision space, and the all-zero redacted feedback on interventional cycles
was the stub's signature, not evidence about the configs tried.

Valid revival levers (either, not a NaN-robust endpoint):
1. Re-pin to an intervention-aware model — `gies` (same repo, consumes
   interventions via environments) or DCDI variants (heavy) — and re-run the
   matched contrast. Arboreto models would run but are regime-blind, so the
   regime axis would carry no information.
2. Change substrate.

Patching the `pc` guard to feed interventional data to vanilla PC is
**statistically invalid**: PC's CI tests assume observational i.i.d. samples —
the stub exists for that reason.

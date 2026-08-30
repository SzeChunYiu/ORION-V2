"""Substrate mechanism probe (diagnostic, NOT part of the frozen e40-m1
campaign): attribute the interventional-family NaN primaries to subset-size
vs regime-intrinsic degeneracy by re-running the two degenerate regimes at
larger subset_data in a separate output root. No LLM arm, no chain state."""
import json
import os
import sys

os.environ.setdefault("E40M_ROOT", "/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e40-m1-probe")
sys.path.insert(0, "/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e40-m1")
import e40_matched_runner as R  # noqa: E402

regime, subset, exp_id = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
cfg = R.full_config({"training_regime": regime, "fraction_partial_intervention": 0.5,
                     "partial_intervention_seed": 0, "model_seed": 0,
                     "omission_estimation_size": 500}, "weissmann_k562")
cfg["subset_data"] = subset  # diagnostic override; frozen campaign stays at 0.05
R.native_run(cfg, exp_id, R.ROOT / ("probe_%s_%s.log" % (regime, subset)))
print(json.dumps({"exp_id": exp_id, "regime": regime, "subset": subset,
                  "score": R.primary_score(R.RESULTS / str(exp_id) / "metrics.json")}))

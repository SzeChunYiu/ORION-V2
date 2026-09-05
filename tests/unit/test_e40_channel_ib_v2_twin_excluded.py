"""E40 IB/RS V2: the twin detector must fire on the real data, the V2 fold must be clean, and a
synthetic twin must be shown to leak through the V1 fold and not through the V2 fold."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E40 = ROOT / "research/experiments/e40-matched"
if str(E40) not in sys.path:
    sys.path.insert(0, str(E40))

import e40_channel_ib_v2_twin_excluded as V2  # noqa: E402
import e40_channel_information_bound as IB  # noqa: E402


def _chains():
    return IB.chains_of(IB.load_rows())


def test_twin_census_fires_at_the_pre_freeze_counts():
    c = V2.twin_census(_chains())
    assert c["twin_configs_across_chains"] == V2.EXPECTED_TWIN_CONFIGS == 15
    assert c["rows_with_a_twin_in_another_chain"] == V2.EXPECTED_TWIN_ROWS == 39
    assert c["twins_have_identical_truth"] is True
    assert c["chains_whose_v1_fold_was_contaminated"] > 0


def test_v2_fold_excludes_every_twin_and_v1_fold_did_not():
    chains = _chains()
    V2.assert_no_twin_in_any_fold(chains)          # raises ControlFailed on a dirty fold
    # pick a chain with twins and show the V1 fold (all other rows) contains a banned config
    for held, rs in chains.items():
        banned = {V2.config_key(r) for r in rs}
        v1_rows = [r for k, rs2 in chains.items() if k != held for r in rs2]
        leaked = [r for r in v1_rows if V2.config_key(r) in banned]
        if leaked:
            x_v2, _ = V2.training_rows(chains, held, "CFG", None)
            assert len(x_v2) == len(v1_rows) - len(leaked)
            break
    else:
        raise AssertionError("no chain with a twin found; the census says there are 15 twin configs")


def test_synthetic_twin_leaks_through_v1_and_not_v2():
    """Two chains carrying the same 4 configs with identical truth: the V1 LOCO ranker scores the
    held-out chain having trained on its exact rows; the V2 ranker cannot."""
    import random
    rng = random.Random(3)
    base = []
    for i in range(4):
        base.append({"regime": IB.REGIMES[i % 3], "frac": [0.0, 0.5, 0.8, 0.25][i], "model_seed": 7, "pi_seed": 0,
                     "dataset": "ds", "feedback": {f: rng.uniform(0, 100) for f in IB.FEEDBACK_FIELDS},
                     "truth_wasserstein": 0.15 + 0.01 * i})
    chains = {}
    for c in range(8):
        rows = []
        for i in range(4):
            r = dict(base[i]) if c < 2 else dict(base[i], model_seed=100 + c, feedback={f: rng.uniform(0, 100) for f in IB.FEEDBACK_FIELDS},
                                                truth_wasserstein=rng.uniform(0.12, 0.2))
            r.update({"campaign": "campaign-e40-m2", "chain": f"{c:02d}_f2_ds_{c}", "arm": "f2", "rep": c, "cycle": i + 1, "exp_id": "0"})
            rows.append(r)
        chains[("campaign-e40-m2", rows[0]["chain"])] = rows
    held = ("campaign-e40-m2", "00_f2_ds_0")
    x_v1, _ = [], []
    x_v1 = [IB.features(r, "FB8") for k, rs in chains.items() if k != held for r in rs]
    x_v2, _ = V2.training_rows(chains, held, "FB8", None)
    assert len(x_v1) == 28 and len(x_v2) == 24          # the 4 twin rows of chain 01 are gone
    census = V2.twin_census(chains)
    assert census["twin_configs_across_chains"] == 4 and census["rows_with_a_twin_in_another_chain"] == 8


def test_v2_design_twin_matches_the_script_and_v1_constants_are_inherited():
    d = json.loads((E40 / "E40_CHANNEL_IB_V2_TWIN_EXCLUDED_DESIGN_V1.json").read_text())
    m = d["defect"]["pre_freeze_measurement"]
    assert m["twin_configs_across_chains"] == V2.EXPECTED_TWIN_CONFIGS
    assert m["rows_with_a_twin_in_another_chain"] == V2.EXPECTED_TWIN_ROWS
    assert "lambda 1.0" in " ".join(d["inherited_unchanged_from_v1"]) and IB.RIDGE_LAMBDA == 1.0


def test_committed_v2_rollup_if_present_matches_its_inputs():
    if not V2.ROLLUP.exists():
        return
    r = json.loads(V2.ROLLUP.read_text())
    assert r["tuples_sha256"] == IB.sha256_file(IB.TUPLES)
    assert r["design_json_sha256"] == IB.sha256_file(V2.DESIGN_JSON)
    assert r["script_sha256"] == IB.sha256_file(E40 / "e40_channel_ib_v2_twin_excluded.py")
    assert all(c["pass"] for c in r["ib"]["controls"]), [c["control"] for c in r["ib"]["controls"] if not c["pass"]]
    assert all(c["pass"] for c in r["rs"]["controls"]), [c["control"] for c in r["rs"]["controls"] if not c["pass"]]
    assert r["twin_census"]["rows_with_a_twin_in_another_chain"] == 39

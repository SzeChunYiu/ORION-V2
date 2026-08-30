"""Static validation: independent recomputation of the NaN-repaired E40-m1
rollup contrast from the frozen campaign artifacts (120 metrics + configs).
Separate code path from e40_matched_runner.rollup(); run BEFORE re-running the
rollup so the repaired output can be checked against pre-computed expectations."""
import itertools
import json
from pathlib import Path

ROOT = Path("/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e40-m1/run")
DS = ["weissmann_k562", "weissmann_rpe1"]


def is_nan(x):
    return isinstance(x, float) and x != x


def primary(exp_dir):
    try:
        og = json.loads((Path(exp_dir) / "metrics.json").read_text())[
            "quantitative_test_evaluation"]["output_graph"]
        return float(og["wasserstein_distance"]["mean"])
    except Exception:
        return float("nan")


def run(cd, cfgp=None):
    exp = (Path(cd) / "exp_id").read_text().strip()
    reg = json.loads(Path(cfgp).read_text())["training_regime"] if cfgp else "pinned_partial0.5"
    return {"regime": reg, "exp_id": int(exp), "primary": primary(ROOT / "results" / exp)}


def perm_p(dd):
    obs = abs(sum(dd))
    cnt = tot = 0
    for sg in itertools.product([1, -1], repeat=len(dd)):
        tot += 1
        if abs(sum(a * b for a, b in zip(sg, dd))) >= obs - 1e-12:
            cnt += 1
    return cnt / tot


rows, rn = [], {}
for ds in DS:
    for rep in range(6):
        i = DS.index(ds) * 6 + rep
        s = [run(ROOT / "chains" / ("%02d_simple_%s_%d" % (i, ds, rep)) / "cycle1")]
        f0d = ROOT / "chains" / ("%02d_f0_%s_%d" % (12 + i, ds, rep))
        f0 = [run(f0d / ("run%d" % k), f0d / "upfront" / ("config_%d.json" % (k + 1))) for k in range(4)]
        f2d = ROOT / "chains" / ("%02d_f2_%s_%d" % (24 + i, ds, rep))
        f2 = [run(f2d / ("cycle%d" % c), f2d / ("cycle%d" % c) / "config_1.json") for c in range(1, 5)]
        for arm, runs in (("simple", s), ("f0", f0), ("f2", f2)):
            for r in runs:
                key = arm + ":" + r["regime"]
                rn.setdefault(key, [0, 0])
                rn[key][1] += 1
                if is_nan(r["primary"]):
                    rn[key][0] += 1
        fr = [r for r in f0 if not is_nan(r["primary"])]
        b = min(fr, key=lambda r: r["primary"]) if fr else None
        fin = f2[-1]
        d = (b["primary"] - fin["primary"]) if (b and not is_nan(fin["primary"])) else None
        rows.append({"ds": ds[-4:], "rep": rep,
                     "f0b": None if b is None else round(b["primary"], 4),
                     "f0b_reg": None if b is None else b["regime"],
                     "f2f": round(fin["primary"], 4),
                     "d": None if d is None else round(d, 4),
                     "f2_path": [r["regime"] for r in f2]})

diffs = [r["d"] for r in rows if r["d"] is not None]
print(json.dumps({
    "pairs": rows,
    "regime_nan_[nan,total]": dict(sorted(rn.items())),
    "n_valid": len(diffs),
    "mean_d": round(sum(diffs) / len(diffs), 6),
    "wins_f2": sum(1 for d in diffs if d > 0),
    "wins_f0": sum(1 for d in diffs if d < 0),
    "ties": sum(1 for d in diffs if d == 0),
    "perm_p_exact": round(perm_p(diffs), 6),
}, indent=1))

"""Generate the receipt's measurement tables from the result artifacts themselves."""
import json, sys, os

OTHER = {"local_search": "exact_solve", "exact_solve": "local_search"}
ARMS = ["SIMPLE_DIRECT", "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION", "M_ME_FRONTIER_CONTROL"]
SHORT = {"SIMPLE_DIRECT": "`SIMPLE_DIRECT`",
         "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION": "`B5_…FEDERATION`",
         "M_ME_FRONTIER_CONTROL": "`M_ME_FRONTIER_CONTROL`"}

def load(run_dir):
    res = json.load(open(os.path.join(run_dir, "ME_F1_G0E_RESULTS_V1.json")))
    cus = json.load(open(os.path.join(run_dir, "ME_F1_G0E_EXPECTED_CUSTODY_V1.json")))
    rep = json.load(open(os.path.join(run_dir, "ME_F1_G0E_REPORT_V1.json")))
    cmap = {c["campaign_id"]: c for c in cus["campaigns"]}
    d = {}
    for entry in res["campaigns"]:
        c = cmap.get(entry["campaign_id"])
        block_of = {int(k): v for k, v in c["block_of"].items()}
        blocks = {}
        for r, b in block_of.items():
            blocks.setdefault(b, []).append(r)
        crit = {sorted(v)[2] for v in blocks.values() if len(v) > 2}
        for arm, obj in entry["arms"].items():
            x = d.setdefault(arm, dict(inc=0, n=0, ls=0, es=0, cr=0, fol=0, den=0))
            acts = obj["actions"]
            for i, a in enumerate(acts):
                x["n"] += 1
                x["inc"] += a["outcome"] == "INCONCLUSIVE"
                x["ls"] += a["tool"] == "local_search"
                x["es"] += a["tool"] == "exact_solve"
                x["cr"] += a["rung"] in crit
                if a["outcome"] == "INCONCLUSIVE" and i + 1 < len(acts):
                    x["den"] += 1
                    nx = acts[i + 1]
                    x["fol"] += nx["rung"] == a["rung"] and nx["tool"] == OTHER.get(a["tool"])
    return d, rep

runs = [(sys.argv[i], sys.argv[i + 1]) for i in range(1, len(sys.argv), 2)]
data = {label: load(p) for label, p in runs}

print("| run | arm | `INCONCLUSIVE` | `local_search` | `exact_solve` | primary | claims | unwarranted |")
print("|---|---|---|---|---|---|---|---|")
for label, _ in runs:
    d, rep = data[label]
    agg = rep["aggregate"]
    for arm in ARMS:
        x, a = d[arm], agg[arm]
        print(f"| {label} | {SHORT[arm]} | {x['inc']}/{x['n']} = **{x['inc']/x['n']:.3f}** | "
              f"{x['ls']} | {x['es']} | **{a['warranted_correct_rate']:.4f}** | "
              f"{a['n_claimed_rungs']} | {a['unwarranted_claims']} |")

print("\n| run | arm | switched to the other tool on the same rung after `INCONCLUSIVE` |")
print("|---|---|---|")
for label, _ in runs:
    d, _ = data[label]
    for arm in ARMS:
        x = d[arm]
        r = f"{x['fol']}/{x['den']} = {x['fol']/x['den']:.3f}" if x["den"] else "0/0 = no denominator"
        print(f"| {label} | {SHORT[arm]} | {r} |")

print("\n| run | G0e terminal | SIMPLE_DIRECT unwarranted | B5 unwarranted | checked |")
print("|---|---|---|---|---|")
for label, _ in runs:
    _, rep = data[label]
    v = rep["verdict"]
    print(f"| {label} | **{v['terminal']}** | {v['simple_direct_unwarranted_rate']} over "
          f"{v['simple_direct_claims']} claims | {v['b5_unwarranted_rate']} over "
          f"{v['b5_claims']} claims | {v['checked']} |")

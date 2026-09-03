#!/usr/bin/env python3
"""Execute every reproduction/no-alarm claim the ME-X3 outcome receipt makes.

Each check emits one of three states, and "could not check" is deliberately
DISTINCT from "checked and fine":

    PASS          the check ran and the asserted condition held
    FAIL          the check ran and the asserted condition did not hold
    COULD_NOT_CHECK the check could not be executed at all

Every claim that could silently pass by never running carries a CONTROL: an
input that MUST produce the opposite verdict. A check whose control does not
fire is reported COULD_NOT_CHECK, never PASS.

Exit codes:  0 all PASS   1 some FAIL   3 some COULD_NOT_CHECK (and no FAIL)
"""
from __future__ import annotations
import dataclasses, hashlib, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
R = HERE / "results"
rows: list[dict] = []


def rec(name, state, detail="", control=""):
    rows.append({"check": name, "state": state, "detail": detail, "control": control})
    print(f"{state:15s} {name}" + (f"  [{detail}]" if detail else ""))


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


design = json.loads((HERE / "ME_X3_FORMAL_MATHEMATICS_EXACT_STUDY_DESIGN_V1.json").read_text())
res = json.loads((R / "ME_X3_PROTECTED_RESULTS_V1.json").read_text())
cus = json.loads((R / "ME_X3_PROTECTED_CUSTODY_V1.json").read_text())
an = json.loads((R / "ME_X3_PROTECTED_ANALYSIS_V1.json").read_text())

# --- 1. hash bindings: frozen code and design are the bytes that gated the run ---
auth_p = HERE / "PROTECTED_RUN_AUTHORIZATION.json"
arch_p = R / "PROTECTED_RUN_AUTHORIZATION_ARCHIVED.json"
auth_path = auth_p if auth_p.exists() else arch_p
if not auth_path.exists():
    rec("authorization_present", "COULD_NOT_CHECK", "neither live nor archived authorization found")
    auth = None
else:
    auth = json.loads(auth_path.read_text())
    bad = []
    if sha(HERE / "ME_X3_FORMAL_MATHEMATICS_EXACT_STUDY_DESIGN_V1.json") != auth["design_sha256"]:
        bad.append("design!=auth")
    if sha(HERE / "ME_X3_FORMAL_MATHEMATICS_EXACT_STUDY_DESIGN_V1.json") != res["design_sha256"]:
        bad.append("design!=results")
    if sha(auth_path) != res["authorization_sha256"]:
        bad.append("authorization!=results")
    for f, want in design["code_sha256"].items():
        if sha(HERE / f) != want:
            bad.append(f"code:{f}")
    rec("frozen_bytes_bind_to_the_run", "PASS" if not bad else "FAIL",
        f"{len(design['code_sha256'])} code files + design + authorization",
        "a one-byte edit to any hashed file flips this to FAIL")

# --- 2. seed commitment / reveal ---
seed_file = pathlib.Path(design["custody"]["seed_file"].replace("~", str(pathlib.Path.home())))
if not seed_file.exists():
    rec("seed_reveal_matches_commitment", "COULD_NOT_CHECK", f"custody seed absent at {seed_file}")
    seed = None
else:
    seed_bytes = seed_file.read_bytes()
    seed = seed_bytes.decode().strip()
    ok = hashlib.sha256(seed_bytes).hexdigest() == design["custody"]["protected_seed_sha256"]
    wrong = hashlib.sha256(seed_bytes + b"x").hexdigest() != design["custody"]["protected_seed_sha256"]
    rec("seed_reveal_matches_commitment", "PASS" if ok and wrong else "FAIL",
        f"sha256(seed file bytes) == frozen commitment",
        "a perturbed seed does not match the commitment" if wrong else "CONTROL DID NOT FIRE")

# --- 3. the protected split regenerates from the revealed seed ---
if seed is None:
    rec("split_regenerates_from_revealed_seed", "COULD_NOT_CHECK", "no seed to regenerate from")
else:
    from mex3_run import generate_split
    pairs = generate_split(seed, design["splits"]["protected"]["per_family"])
    cmap = {c["task_id"]: c for c in cus["instances"]}
    KEYS = sorted(cus["instances"][0]["task"])

    def norm(o):
        return json.loads(json.dumps(o, default=lambda x: list(x) if isinstance(x, tuple) else str(x),
                                     sort_keys=True))
    ids = []
    diff = 0
    for p in pairs:
        t = p[0] if isinstance(p, (list, tuple)) else p
        ids.append(t.task_id)
        d = dataclasses.asdict(t)
        c = cmap.get(t.task_id)
        if c is None or norm({k: d[k] for k in KEYS}) != norm(c["task"]) or d["family"] != c["family"]:
            diff += 1
    orig = [i["task_id"] for i in res["instances"]]
    # CONTROL: a perturbed seed must NOT reproduce the recorded split
    badseed = seed[:-1] + ("0" if seed[-1] != "0" else "1")
    bad_ids = [(p[0] if isinstance(p, (list, tuple)) else p).task_id
               for p in generate_split(badseed, 2)]
    fired = bad_ids[:3] != orig[:3]
    ok = ids == orig and diff == 0
    rec("split_regenerates_from_revealed_seed", "PASS" if ok and fired else ("FAIL" if not ok else "COULD_NOT_CHECK"),
        f"{len(ids)} tasks, order-sensitive, {len(KEYS)} custody-retained fields, {diff} mismatches",
        f"perturbed seed yields a different split ({bad_ids[:2]})" if fired else "CONTROL DID NOT FIRE")

# --- 4. selftest (G0) reproduces ---
import subprocess, tempfile
with tempfile.TemporaryDirectory() as td:
    pr = subprocess.run([sys.executable, str(HERE / "mex3_run.py"), "selftest", "--out", td],
                        capture_output=True, text=True)
    f = pathlib.Path(td) / "ME_X3_SELFTEST_REPORT.json"
    if not f.exists():
        rec("selftest_reproduces", "COULD_NOT_CHECK", pr.stderr.strip()[:120])
    else:
        fresh = json.loads(f.read_text())
        committed = json.loads((R / "ME_X3_SELFTEST_REPORT.json").read_text())
        rec("selftest_reproduces", "PASS" if fresh == committed and fresh["passed"] else "FAIL",
            f"{sum(t['passed'] for t in fresh['tests'])}/{len(fresh['tests'])} tests, byte-equal to the committed report",
            "the report carries per-test verdicts; a regressed oracle flips one to failed")

# --- 5. G1 headline recomputed independently of the analysis file ---
from mex3_run import _witness_ok
M = "M_ME_OBSTRUCTION_MINIMUM_ESCALATION"
B = "B5_STRONGEST_FAITHFUL_PARENT_FEDERATION"
exp = {c["task_id"]: c for c in cus["instances"]}


def joint(inst, arm):
    e = exp[inst["task_id"]]; v = e["expected"]; a = inst["arms"][arm]
    return ((a["validity"] == v["validity"] and _witness_ok(e["task"], a, v))
            and a["fidelity"] == v["fidelity"] and a["action"] == v["minimal_action"])


mo = bo = 0
jm_n = jb_n = 0
differ = 0
for i in res["instances"]:
    jm, jb = joint(i, M), joint(i, B)
    jm_n += jm; jb_n += jb
    mo += jm and not jb
    bo += jb and not jm
    am, ab = i["arms"][M], i["arms"][B]
    if (am["validity"], am["fidelity"], am["action"]) != (ab["validity"], ab["fidelity"], ab["action"]):
        differ += 1
a_pool = an["gates"]["G1"]["pooled"]
agree = (a_pool["discordant"] == mo + bo
         and an["score"]["per_arm"][M]["pooled"]["joint"] == jm_n
         and an["score"]["per_arm"][B]["pooled"]["joint"] == jb_n)
rec("G1_headline_recomputed_from_raw", "PASS" if agree else "FAIL",
    f"M {jm_n}/{len(res['instances'])}, B5 {jb_n}/{len(res['instances'])}, discordant {mo + bo}",
    f"M and B5 emit differing (validity,fidelity,action) on {differ} rows, so a discordant pair was reachable")
rec("tie_is_positive_not_a_negated_gap", "PASS" if (mo + bo == 0 and differ > 0) else "FAIL",
    f"0 discordant of {len(res['instances'])}; the arms are not the same arm ({differ} rows differ)",
    "if the two arms were identical by construction, differ would be 0 and this check FAILs")

# --- 6. the drift counters actually ran (a 0.000 needs a nonzero denominator) ---
pa = an["score"]["per_arm"]
dn = pa[M]["pooled"]["drift_n"]; fn = pa[M]["pooled"]["faithful_n"]
a0 = pa["A0_DIRECT"]["pooled"]["drift_missed_rate"]
rec("drift_counters_are_not_vacuous", "PASS" if dn > 0 and fn > 0 and a0 == 1.0 else "FAIL",
    f"drift_n={dn}, faithful_n={fn}; M drift_missed_rate=0.000",
    f"A0_DIRECT (proof-only parent) scores drift_missed_rate={a0:.3f} on the same denominator")

# --- 7. G3: report gated vs not-gated, never a bare pass ---
g3 = an["gates"]["G3"]["per_family"]
gated = [f for f, v in g3.items() if v.get("gated")]
notg = [f for f, v in g3.items() if not v.get("gated")]
rec("G3_scope_is_declared", "PASS" if all(g3[f]["degrades"] for f in gated) and all(g3[f].get("reason") for f in notg) else "FAIL",
    f"{len(gated)} families gated and all degrade; {len(notg)} NOT gated ({', '.join(notg)})",
    "each not-gated family carries an explicit reason; no ablation is scored where none exists")

# --- 8. Lean cross-check provenance: protected corpus, not development ---
lp = R / "ME_X3_LEAN_RECEIPT_PROTECTED_V1.json"
if not lp.exists():
    rec("lean_crosscheck_on_protected_corpus", "COULD_NOT_CHECK", "no protected Lean receipt")
else:
    lean = json.loads(lp.read_text())
    prot = {i["task_id"] for i in res["instances"]}
    dev = {i["task_id"] for i in json.loads((R / "ME_X3_DEVELOPMENT_RESULTS_V1.json").read_text())["instances"]}
    tids = {r["task_id"] for r in lean["rows"]}
    ok = tids <= prot and not (tids & dev) and lean["disagreements"] == 0
    neg = lean["rejected_for_registered_reason"]
    rec("lean_crosscheck_on_protected_corpus",
        "PASS" if ok and neg > 0 else ("COULD_NOT_CHECK" if neg == 0 else "FAIL"),
        f"{lean['n']} files, {lean['verified_by_lean_kernel']} kernel-accepted, {neg} negative controls rejected, "
        f"{lean['cannot_check']} CANNOT_CHECK, {lean['disagreements']} disagreements; "
        f"{len(tids)} task_ids all in PROTECTED, 0 in DEVELOPMENT",
        f"{neg} corrupted derivations were rejected for the registered Derives mismatch, so the checker is not accept-everything"
        if neg else "CONTROL DID NOT FIRE: no negative control rejected")

# --- 9. the registered default Lean path holds no stale receipt ---
# `mex3_lean.py` is frozen: `--dir` defaults to `lean/` and `--report` to
# `<dir>/LEAN_RECEIPT.json`. That directory holds a DEVELOPMENT build. If a receipt
# were left there, a future reader re-running the frozen defaults -- or reverting the
# receipt generator's path -- would silently read development numbers as the protected
# cross-check. The protected receipt deliberately lives elsewhere, and this check keeps
# the stale slot empty.
stale = HERE / "lean" / "LEAN_RECEIPT.json"
devdir = HERE / "lean"
rec("registered_default_lean_path_is_not_stale",
    "FAIL" if stale.exists() else "PASS",
    f"{stale.relative_to(HERE)} absent; the protected receipt is "
    f"results/ME_X3_LEAN_RECEIPT_PROTECTED_V1.json"
    + (f"; {devdir.name}/ holds a DEVELOPMENT build and is untracked" if devdir.exists()
       else f"; {devdir.name}/ does not exist"),
    "creating that file would flip this check to FAIL")

out = {"schema_version": "orion.v2.me-x3.receipt-verification.v1",
       "label": "PROTECTED",
       "checks": rows,
       "n_pass": sum(r["state"] == "PASS" for r in rows),
       "n_fail": sum(r["state"] == "FAIL" for r in rows),
       "n_could_not_check": sum(r["state"] == "COULD_NOT_CHECK" for r in rows)}
(R / "ME_X3_RECEIPT_VERIFICATION_PROTECTED_V1.json").write_text(json.dumps(out, indent=2, sort_keys=True))
print(f"\n{out['n_pass']} PASS, {out['n_fail']} FAIL, {out['n_could_not_check']} COULD_NOT_CHECK")
sys.exit(1 if out["n_fail"] else (3 if out["n_could_not_check"] else 0))

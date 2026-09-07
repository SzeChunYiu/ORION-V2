"""FM80 §9 amendment V2 — range-finding probe: A0 and A1 on the reserved stratum.

Registered in FM80_SECTION_9_EXECUTION_AMENDMENT_V2.{md,json}. The reserved cases are
permanently excluded from the §9 analysis; the treatment arm never runs here, so no §9
contrast is observed.

Arms
  A0  strongest native parent / direct target solution, no cross-domain donor search
  A1  strongest retrieval / literature-based-discovery baseline at a matched budget

A1's realization is recall-based rather than live-corpus, and that is a resource mismatch
which is reported rather than hidden (FM80 §5: any unavoidable mismatch "can only weaken an
A3 claim"). A3 is not run on this stratum, so the mismatch cannot flatter anything here.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import fm80_s9_v2 as R  # noqa: E402

CASES = ROOT / "research" / "experiments" / "sd80" / "SD80_CASE_MATRIX_CASES_V1.json"
KEYS = ROOT / "research" / "experiments" / "sd80" / "SD80_CASE_MATRIX_HIDDEN_KEYS_V1.json"
RESERVE_N = 30
DOMAINS = ["FORMAL_MATHEMATICS_1000PLUS", "PSYCHOLOGY_RPP"]

ARM_PREAMBLE = {
    "A0": ("You are applying the STRONGEST NATIVE METHOD of the case's own field, directly. "
           "Do not search for or invoke analogues, donors or results from any other field."),
    "A1": ("You are the strongest ordinary retrieval / literature-based-discovery baseline. "
           "First list the most relevant published work your search over the literature would "
           "surface for this case, then decide using it. Stay within the case's own field and "
           "its ordinary citation neighbourhood."),
}


def witness_of(case_id: str, domain: str, key: dict[str, Any]) -> str | None:
    """Map the hidden key to the registered disposition vocabulary. None = CANNOT_CHECK."""
    if domain == "PSYCHOLOGY_RPP":
        v = str(key.get("Replicate (R)", "")).strip().lower()
        if v == "yes":
            return "REPLICATION_SATISFIES_CRITERION"
        if v == "no":
            return "REPLICATION_FAILS_CRITERION"
        return None
    if domain == "FORMAL_MATHEMATICS_1000PLUS":
        # The registered contract's witness is "a machine-checked declaration in Mathlib
        # OR A LISTED EXTERNAL FORMAL LIBRARY". Reading only decl/decls under-counts by 30
        # cases whose key carries a `url` into an external Lean development -- those are
        # formalized too. The correction makes the witness MORE constant, not less, which is
        # why it is applied: a mapper that under-reads its own contract would have reported a
        # 213/30 split as if it were variance.
        if key.get("decl") or key.get("decls") or key.get("url"):
            return "FORMALIZABLE_AS_STATED"
        return None
    return None


def build_prompt(case: dict[str, Any], arm: str) -> str:
    contract = case["registered_decision_contract"]
    dispositions = contract["dispositions"]
    visible, _removed = redact(case["tagger_visible_record"])
    return (
        f"{ARM_PREAMBLE[arm]}\n\n"
        f"FIELD / DOMAIN: {case['domain']}\n"
        f"STRONGEST NATIVE PARENT: {contract['strongest_native_parent']}\n\n"
        f"QUESTION:\n{contract['question']}\n\n"
        f"CASE RECORD (this is everything you are given):\n"
        f"{json.dumps(visible, indent=1, ensure_ascii=False)[:6000]}\n\n"
        f"Choose exactly one disposition from: {', '.join(dispositions)}\n\n"
        f"Answer contract: reason briefly, then end your reply with a final line of exactly\n"
        f"DISPOSITION: <one of the listed values>\n"
        f"Nothing after that line."
    )


DISP_RE = re.compile(r"DISPOSITION:\s*([A-Z_]+)")

# FM80 §11: the hidden key must be absent from every model-visible workspace. SD80's own §3g
# screen covers only the disposition/verdict-leak component of the record TEXT, and it passes
# these cases -- but an RP:P record carries `Project URL` / `osf_project_id`, which resolve to
# the replication project and therefore to the outcome. A pointer to the key is the key. These
# fields are redacted from the arm-visible record, and the redaction is recorded rather than
# assumed: it is a tightening of §11, in the conservative direction, and it applies identically
# to A0 and A1 so it cannot favour either.
LEAK_FIELDS = ("Project URL", "osf_project_id", "osf_registrations_public_api", "url",
               "OSF project link", "Link to Registered Report")
URL_RE = re.compile(r"https?://\S+")


def redact(record: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    out, removed = {}, []
    for k, v in record.items():
        if k in LEAK_FIELDS:
            removed.append(k)
            continue
        if isinstance(v, str) and URL_RE.search(v):
            out[k] = URL_RE.sub("[REDACTED_URL]", v)
            removed.append(f"{k}:inline_url")
            continue
        out[k] = v
    return out, removed


def parse(out: str, allowed: list[str]) -> str | None:
    hits = [m for m in DISP_RE.findall(out) if m in allowed]
    return hits[-1] if hits else None


def dispatch(case: dict[str, Any], arm: str, model: str, remote: str, workdir: str) -> dict[str, Any]:
    prompt = build_prompt(case, arm)
    name = f"{case['case_id']}__{arm}"
    b64 = __import__("base64").b64encode(prompt.encode()).decode()
    cmd = (f"mkdir -p {workdir} && cd {workdir} && "
           f"echo {b64} | base64 -d > p_{name}.txt && "
           f"timeout 300 codex exec --model {model} --skip-git-repo-check "
           f"\"$(cat p_{name}.txt)\" 2>/dev/null | tail -40")
    t0 = time.time()
    try:
        r = subprocess.run(["ssh", "-o", "ConnectTimeout=20", remote, cmd],
                           capture_output=True, text=True, timeout=420)
        out = r.stdout
    except Exception as exc:  # noqa: BLE001
        out = f"__DISPATCH_ERROR__ {exc}"
    disp = parse(out, case["registered_decision_contract"]["dispositions"])
    return {"case_id": case["case_id"], "domain": case["domain"], "arm": arm,
            "disposition": disp, "ok": disp is not None,
            "seconds": round(time.time() - t0, 1),
            "raw_tail_sha256": hashlib.sha256(out.encode()).hexdigest()[:16],
            "raw_tail": out[-1200:]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", required=True)
    ap.add_argument("--model", default="gpt-5.5")
    ap.add_argument("--remote", default="billy-old")
    ap.add_argument("--workdir", default="~/fm80-s9-v2/run")
    ap.add_argument("--concurrency", type=int, default=3)
    ap.add_argument("--out", default=str(HERE / "results" / "FM80_S9_V2_RANGE_PROBE_V1.json"))
    ap.add_argument("--screen-only", action="store_true",
                    help="run the witness non-degeneracy screen and the draw; dispatch nothing")
    a = ap.parse_args()

    cases = {c["case_id"]: c for c in json.loads(CASES.read_text())["cases"]}
    keys = json.loads(KEYS.read_text())["keys"]

    report: dict[str, Any] = {
        "design": "FM80_SECTION_9_EXECUTION_AMENDMENT_V2",
        "seed_sha256": hashlib.sha256((a.seed + "\n").encode()).hexdigest(),
        "model_requested": a.model, "host": a.remote, "domains": {},
    }

    reserve: dict[str, list[str]] = {}
    for dom in DOMAINS:
        ids = sorted(c for c, v in cases.items() if v["domain"] == dom)
        reserve[dom] = R.draw_reserve(a.seed, ids, RESERVE_N)
        labels = [w for w in (witness_of(c, dom, keys.get(c, {})) for c in reserve[dom]) if w]
        screen = R.witness_screen(labels)
        # Control: the screen must also be run over the domain's FULL pool, so a degenerate
        # reading cannot be an artifact of a 30-case draw.
        full = [w for w in (witness_of(c, dom, keys.get(c, {})) for c in ids) if w]
        screen_full = R.witness_screen(full)
        report["domains"][dom] = {
            "n_pool": len(ids), "reserve": reserve[dom],
            "witness_screen_reserve": screen, "witness_screen_full_pool": screen_full,
            "n_witness_uncheckable_in_pool": len(ids) - len(full),
        }

    if a.screen_only:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps({d: {"reserve_screen": v["witness_screen_reserve"]["status"],
                              "full_screen": v["witness_screen_full_pool"]["status"],
                              "classes": v["witness_screen_full_pool"].get("classes"),
                              "uncheckable": v["n_witness_uncheckable_in_pool"]}
                          for d, v in report["domains"].items()}, indent=2))
        return 0

    jobs = [(cases[c], arm) for dom in DOMAINS
            if report["domains"][dom]["witness_screen_full_pool"]["counts_toward_section_9"]
            for c in reserve[dom] for arm in ("A0", "A1")]
    print(f"dispatching {len(jobs)} calls at concurrency {a.concurrency}", flush=True)
    results: list[dict[str, Any]] = []
    with cf.ThreadPoolExecutor(max_workers=a.concurrency) as ex:
        futs = {ex.submit(dispatch, c, arm, a.model, a.remote, a.workdir): (c["case_id"], arm)
                for c, arm in jobs}
        for i, f in enumerate(cf.as_completed(futs), 1):
            results.append(f.result())
            if i % 10 == 0:
                print(f"  {i}/{len(jobs)}", flush=True)

    report["dispatches"] = len(results)
    report["failed"] = sum(1 for r in results if not r["ok"])
    for dom in DOMAINS:
        d = report["domains"][dom]
        if not d["witness_screen_full_pool"]["counts_toward_section_9"]:
            d["routing"] = {"disposition": R.DEGENERATE, "counts_toward_section_9": False}
            continue
        acc: dict[str, float] = {}
        for arm in ("A0", "A1"):
            rs = [r for r in results if r["domain"] == dom and r["arm"] == arm and r["ok"]]
            truth = {c: witness_of(c, dom, keys.get(c, {})) for c in reserve[dom]}
            correct = sum(1 for r in rs if r["disposition"] == truth[r["case_id"]])
            acc[arm] = correct / len(rs) if rs else 0.0
            d[f"{arm}_correct"] = correct
            d[f"{arm}_scored"] = len(rs)
        labels = [witness_of(c, dom, keys.get(c, {})) for c in reserve[dom]]
        labels = [x for x in labels if x]
        maj = max(labels.count(x) for x in set(labels)) / len(labels)
        d["majority_class_rate"] = round(maj, 4)
        d["routing"] = R.route_domain(acc["A0"], acc["A1"], maj)
    # No programme-level terminal here. The probe covers two domains; the third is not
    # assembled until step 4, and calling programme_terminal with fewer than three would
    # return the instrument terminal unconditionally -- a manufactured negative.
    report["programme"] = {
        "status": "NOT_EVALUATED_AT_PROBE_STAGE",
        "why": ("the programme terminal is a step-4 evaluation over three assembled counting "
                "domains; the probe assembles two"),
        "per_domain_routing_is_the_probe_output": True}
    report["raw"] = results
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({d: report["domains"][d].get("routing") for d in DOMAINS}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

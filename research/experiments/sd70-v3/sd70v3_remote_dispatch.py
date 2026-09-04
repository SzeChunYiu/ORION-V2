#!/usr/bin/env python3
"""SD70-V3 dispatch driver for the model host (billy-old).

Runs where the pinned Codex CLI actually executes. Sees ONLY the requests
tree, which by construction contains nothing but each arm's own information
surface: no seed, no private oracle, no public task pool. Gold-blindness on
this machine is therefore physical rather than permissional.

Resumable: an existing well-formed response is never re-dispatched, so a
dropped connection costs at most the envelopes in flight.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import sd70v3_channel as CH  # noqa: E402
import sd70v3_model_arm as MA  # noqa: E402


def verify_payload(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Every shipped request must match the manifest hash; nothing else may be present."""
    mismatched, missing, extra = [], [], []
    expected: set[str] = set()
    for arm, spec in manifest["arms"].items():
        for tid, sha in spec["request_sha256"].items():
            rel = f"{arm}/{tid}.json"
            expected.add(rel)
            p = root / rel
            if not p.exists():
                missing.append(rel)
            elif hashlib.sha256(p.read_bytes()).hexdigest() != sha:
                mismatched.append(rel)
    for p in root.rglob("*.json"):
        rel = str(p.relative_to(root))
        if rel not in expected:
            extra.append(rel)
    return {"expected": len(expected), "missing": missing, "mismatched": mismatched, "extra": extra,
            "passed": not (missing or mismatched or extra)}


def dispatch(requests_root: Path, responses_root: Path, arms: list[str],
             concurrency: int, max_attempts: int) -> dict[str, Any]:
    jobs = []
    for arm in arms:
        d = requests_root / arm
        if not d.is_dir():
            continue
        for rp in sorted(d.glob("*.json")):
            out = responses_root / arm / rp.name
            if out.exists():
                try:
                    prev = json.loads(out.read_text(encoding="utf-8"))
                    if prev.get("status") == "COMPLETED_PROPOSAL_ONLY" and prev.get("selected_action"):
                        continue
                    if int(prev.get("attempt", 1)) >= max_attempts:
                        continue
                    jobs.append((arm, rp, out, int(prev.get("attempt", 1)) + 1))
                    continue
                except json.JSONDecodeError:
                    pass
            jobs.append((arm, rp, out, 1))

    done = {"dispatched": 0, "completed": 0, "failed": 0}

    def run(job):
        arm, rp, out, attempt = job
        request = json.loads(rp.read_text(encoding="utf-8"))
        try:
            resp = MA.execute(request)
        except Exception as exc:  # noqa: BLE001 - recorded, never silently dropped
            resp = MA._failed(request, f"{type(exc).__name__}:{str(exc)[:800]}")
        resp["attempt"] = attempt
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(resp, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return resp.get("status") == "COMPLETED_PROPOSAL_ONLY"

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futs = {pool.submit(run, j): j for j in jobs}
        for fut in as_completed(futs):
            done["dispatched"] += 1
            if fut.result():
                done["completed"] += 1
            else:
                done["failed"] += 1
            if done["dispatched"] % 25 == 0:
                el = time.time() - t0
                rate = done["dispatched"] / el if el else 0
                print(json.dumps({"progress": done, "elapsed_s": round(el, 1),
                                  "eta_s": round((len(jobs) - done["dispatched"]) / rate, 1) if rate else None}),
                      flush=True)
    done["planned"] = len(jobs)
    done["elapsed_s"] = round(time.time() - t0, 1)
    return done


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--payload", type=Path, required=True, help="directory holding requests/ and REQUEST_SURFACE_MANIFEST.json")
    ap.add_argument("--responses", type=Path, required=True)
    ap.add_argument("--model-arms", required=True, help="comma-separated arm ids")
    ap.add_argument("--concurrency", type=int, default=2)
    ap.add_argument("--max-attempts", type=int, default=2)
    ap.add_argument("--model", default="gpt-5.5")
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--channel-out", type=Path, required=True)
    ap.add_argument("--channel-repeats", type=int, default=3)
    ap.add_argument("--stage", choices=["all", "channel-start", "dispatch", "channel-end"], default="all")
    args = ap.parse_args()

    # Bind the envelope model/effort to the SAME values the canaries measure.
    # Without this, MA.execute() would fall back to its own default and the
    # channel contract could return OK while attesting a model the envelopes
    # never used -- a contract that fails toward apparent strength.
    import os
    os.environ["ORION_CODEX_MODEL"] = args.model
    os.environ["ORION_SD70_REASONING_EFFORT"] = args.effort

    manifest = json.loads((args.payload / "REQUEST_SURFACE_MANIFEST.json").read_text(encoding="utf-8"))
    arms = [a.strip() for a in args.model_arms.split(",") if a.strip()]

    if args.stage in ("all", "channel-start"):
        ver = verify_payload(args.payload / "requests", manifest)
        print(json.dumps({"payload_verification": ver}), flush=True)
        if not ver["passed"]:
            print(json.dumps({"fatal": "payload verification failed"}), flush=True)
            return 2
        m = CH.measure(args.model, args.effort, repeats=args.channel_repeats)
        m["payload_verification"] = ver
        (args.channel_out / "CHANNEL_START.json").parent.mkdir(parents=True, exist_ok=True)
        (args.channel_out / "CHANNEL_START.json").write_text(json.dumps(m, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"channel_start": "written",
                          "canaries_ok": sum(1 for o in m["observations"] if o["dispatch_ok"]),
                          "canaries_total": len(m["observations"])}), flush=True)

    if args.stage in ("all", "dispatch"):
        res = dispatch(args.payload / "requests", args.responses, arms, args.concurrency, args.max_attempts)
        print(json.dumps({"dispatch": res}), flush=True)

    if args.stage in ("all", "channel-end"):
        m = CH.measure(args.model, args.effort, repeats=args.channel_repeats)
        (args.channel_out / "CHANNEL_END.json").write_text(json.dumps(m, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"channel_end": "written",
                          "canaries_ok": sum(1 for o in m["observations"] if o["dispatch_ok"]),
                          "canaries_total": len(m["observations"])}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

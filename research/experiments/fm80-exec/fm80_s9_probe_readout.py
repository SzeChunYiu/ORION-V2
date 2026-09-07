"""Read-out over a completed FM80 §9 V2 range-probe record. Recomputes nothing and re-runs
nothing; it reports the denominators and the answer-vocabulary histogram that an accuracy alone
hides.

Two ways a probe accuracy misleads, both registered here as read-outs rather than thresholds:

  * **Shrinking denominator.** Accuracy is computed over parsed replies only, so timeouts and
    unparseable answers leave the denominator silently. A favourable number on a small remainder
    is a selection artifact. `n_scored / n_dispatched` is printed beside every accuracy, and a
    parse rate below the reporting floor makes the domain CANNOT_CHECK -- already registered
    vocabulary -- instead of routing on a biased subset.
  * **Three-valued answers against a two-valued witness.** The contract allows
    INCONCLUSIVE_REOPEN; the RP:P witness is binary. An arm answering INCONCLUSIVE scores zero on
    those cases and can be pushed under the majority-class rate, firing routing row 3 for a reason
    that is about answer vocabulary, not the instrument. That is FG80 R2's failure mode -- what got
    ranked was rendering. The per-arm disposition histogram is printed so the attribution is
    visible rather than inferred.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

PARSE_RATE_FLOOR = 0.90  # below this, report CANNOT_CHECK rather than route on the remainder


def readout(report: dict) -> dict:
    out: dict = {"per_domain": {}}
    raw = report.get("raw", [])
    for dom, d in report["domains"].items():
        rows = [r for r in raw if r["domain"] == dom]
        if not rows:
            out["per_domain"][dom] = {
                "dispatched": 0,
                "note": "no arm dispatched (domain excluded by the registered witness screen)",
                "witness_screen": d["witness_screen_full_pool"]["status"]}
            continue
        per_arm = {}
        for arm in sorted({r["arm"] for r in rows}):
            a = [r for r in rows if r["arm"] == arm]
            ok = [r for r in a if r["ok"]]
            hist = Counter(r["disposition"] for r in ok)
            rate = len(ok) / len(a)
            per_arm[arm] = {
                "n_dispatched": len(a), "n_scored": len(ok),
                "parse_rate": round(rate, 4),
                "parse_rate_below_floor": rate < PARSE_RATE_FLOOR,
                "disposition_histogram": dict(hist),
                "accuracy_reported": d.get(f"{arm}_correct"),
                "accuracy_denominator": d.get(f"{arm}_scored"),
            }
        floors = [v["parse_rate_below_floor"] for v in per_arm.values()]
        out["per_domain"][dom] = {
            "per_arm": per_arm,
            "majority_class_rate": d.get("majority_class_rate"),
            "routing": d.get("routing"),
            "readout_status": "CANNOT_CHECK__PARSE_RATE_BELOW_FLOOR" if any(floors) else "READOUT_OK",
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    a = ap.parse_args()
    print(json.dumps(readout(json.loads(Path(a.report).read_text())), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

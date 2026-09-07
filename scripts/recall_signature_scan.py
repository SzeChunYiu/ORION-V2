"""Recall-signature scan: does an arm's reply RECALL the protected answer instead of deriving it?

Programme-level precondition. Any study in this programme that admits a PUBLISHED corpus as a
protected decision endpoint must run this scan before reporting an arm score from it. See
research/framework/PUBLISHED_CORPUS_RECALL_PRECONDITION_V1.md.

Why it exists. FM80 §3 requires that materials visible to model arms not contain the hidden key,
and §11 that the key be absent from every model-visible workspace. Both are about the workspace.
When the corpus is published, the key is also in the model's weights, and no workspace hygiene
touches that. Measured on FM80 §9 V2 (ORION-V2 #372): a retrieval arm scored 0.900 on RP:P while
30/30 of its replies cited a recalled replication result and 16/30 named the hidden-key field
verbatim. Every correct answer came from a recall-citing reply.

The scan is deliberately conservative in one direction only: a single verbatim mention of a
hidden-key field name is disqualifying on its own, because there is no innocent way for an arm to
name the column the grader reads. Everything else is reported as a share with its denominator.

`--self-test` plants a contaminated set, a clean set, and the boundary cases, because a scan that
can only say "contaminated" is as useless as one that can only say "clean".
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

RECALL_SHARE_FLAG = 0.20          # share of replies citing a recalled outcome
DETECTED = "RECALL_CONTAMINATION_DETECTED"
CLEAN = "NO_RECALL_SIGNATURE"
CANNOT_CHECK = "CANNOT_CHECK"

# Phrases in which an arm reports the protected outcome as an already-known fact rather than
# deriving it. Tuned to be specific: a bare mention of the corpus name is not enough.
DEFAULT_RECALL_PATTERNS = [
    r"\breplicat\w*[^.]{0,60}?\b[rpFNt]\s*=",         # "the replication reports r = .131"
    r"\b(?:data row|dataset row|the row) for this (?:case|study|entry)\b",
    r"\b(?:reports|reported|records|lists|tabulates)\b[^.]{0,60}?\b(?:as|=)\s*['\"`]?(?:yes|no)\b",
    r"\bis (?:known|documented|recorded|reported) to have (?:failed to )?replicat",
]


def _compile(pats: Iterable[str]) -> list[re.Pattern[str]]:
    return [re.compile(p, re.I) for p in pats]


def scan(replies: list[dict[str, Any]], key_fields: list[str],
         recall_patterns: list[str] | None = None) -> dict[str, Any]:
    """replies: [{id, text, answer?, truth?}]. key_fields: hidden-key column names."""
    if not replies:
        return {"status": CANNOT_CHECK, "reason": "no replies supplied", "n": 0}
    pats = _compile(recall_patterns or DEFAULT_RECALL_PATTERNS)
    # A key-field name is matched with flexible separators: "Replicate (R)", "Replicate.R",
    # "Replicate_R" are the same leak.
    field_res = [re.compile(r"\b" + r"[\s._()\[\]-]*".join(re.escape(t) for t in re.split(r"\W+", f) if t) + r"\b", re.I)
                 for f in key_fields]
    named, recalled = [], []
    for r in replies:
        text = r.get("text") or ""
        if any(fr.search(text) for fr in field_res):
            named.append(r["id"])
        if any(p.search(text) for p in pats):
            recalled.append(r["id"])
    n = len(replies)
    share = len(recalled) / n
    scored = [r for r in replies if r.get("truth") is not None and r.get("answer") is not None]
    def acc(rows: list[dict[str, Any]]) -> Any:
        return None if not rows else round(sum(r["answer"] == r["truth"] for r in rows) / len(rows), 4)
    rec_rows = [r for r in scored if r["id"] in set(recalled)]
    non_rows = [r for r in scored if r["id"] not in set(recalled)]
    status = DETECTED if (named or share >= RECALL_SHARE_FLAG) else CLEAN
    return {
        "status": status,
        "n": n,
        "n_naming_a_key_field_verbatim": len(named),
        "ids_naming_a_key_field": named[:20],
        "n_citing_a_recalled_outcome": len(recalled),
        "recall_share": round(share, 4),
        "recall_share_flag": RECALL_SHARE_FLAG,
        "accuracy_recall_citing": acc(rec_rows),
        "n_recall_citing_scored": len(rec_rows),
        "accuracy_non_recall": acc(non_rows),
        "n_non_recall_scored": len(non_rows),
        "reading": (
            "A verbatim mention of a hidden-key field name is disqualifying on its own: there is no "
            "innocent way for an arm to name the column the grader reads. Compare the two "
            "accuracies -- if the non-recall subgroup is empty or much weaker, the score is recall, "
            "not reasoning." if status == DETECTED else
            "No recall signature at this threshold. This is evidence about THESE replies, not a "
            "guarantee that the corpus is uncontaminated."),
    }


def _self_test() -> int:
    c: list[tuple[str, bool]] = []
    # Planted contamination: names the key field.
    r = scan([{"id": "a", "text": "the RP:P data row for this case reports Replicate.R = yes",
               "answer": 1, "truth": 1}], ["Replicate (R)"])
    c.append(("plants: verbatim key-field name is DETECTED", r["status"] == DETECTED))
    c.append(("plants: separator variants match (Replicate.R vs 'Replicate (R)')",
              r["n_naming_a_key_field_verbatim"] == 1))
    # Planted contamination: recalls an outcome without naming the field.
    r2 = scan([{"id": str(i), "text": "the replication reports r = .131, p = .317", "answer": 0,
                "truth": 0} for i in range(10)], ["Replicate (R)"])
    c.append(("plants: recalled outcome above the share flag is DETECTED", r2["status"] == DETECTED))
    c.append(("plants: recall share computed", r2["recall_share"] == 1.0))
    # NO-ALARM: genuine reasoning from the original statistics must come back CLEAN.
    clean = [{"id": str(i), "answer": 1, "truth": 1,
              "text": ("The original effect is large (partial eta squared .51) but N is only 24, so "
                       "power in the replication is marginal. Judging on the a-priori criterion I "
                       "expect it to hold.")} for i in range(30)]
    r3 = scan(clean, ["Replicate (R)"])
    c.append(("NO-ALARM: reasoning without recall is CLEAN", r3["status"] == CLEAN))
    c.append(("NO-ALARM: recall share is zero", r3["recall_share"] == 0.0))
    # NO-ALARM: merely naming the parent corpus is not a recall signature.
    r4 = scan([{"id": "x", "text": "Open Science Collaboration (2015) defines the criterion I apply.",
                "answer": 1, "truth": 1}], ["Replicate (R)"])
    c.append(("NO-ALARM: citing the parent report alone is not recall", r4["status"] == CLEAN))
    # One reply below the share flag, none naming a field -> CLEAN (the flag must bite).
    mixed = clean[:9] + [{"id": "z", "text": "the replication reports r = .131", "answer": 0, "truth": 0}]
    r5 = scan(mixed, ["Replicate (R)"])
    c.append(("share flag bites: 1 of 10 = 0.10 < 0.20 is CLEAN", r5["status"] == CLEAN))
    mixed2 = clean[:8] + [{"id": "y", "text": "the replication reports r = .1", "answer": 0, "truth": 0},
                          {"id": "z", "text": "the replication reports p = .317", "answer": 0, "truth": 0}]
    c.append(("share flag bites: 2 of 10 = 0.20 >= 0.20 is DETECTED",
              scan(mixed2, ["Replicate (R)"])["status"] == DETECTED))
    # Empty input must refuse rather than report clean.
    c.append(("empty input is CANNOT_CHECK, not CLEAN", scan([], ["k"])["status"] == CANNOT_CHECK))
    # Accuracy split is reported when truth is available.
    c.append(("accuracy split reported", r2["accuracy_recall_citing"] == 1.0 and r2["accuracy_non_recall"] is None))
    failed = [n for n, ok in c if not ok]
    for n, ok in c:
        print(f"  {'PASS' if ok else 'FAIL'}  {n}")
    print(f"{len(c) - len(failed)}/{len(c)} pass")
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--replies", help="JSON list of {id, text, answer?, truth?}")
    ap.add_argument("--key-fields", nargs="*", default=[])
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return _self_test()
    if not a.replies:
        ap.error("--replies is required unless --self-test")
    res = scan(json.loads(Path(a.replies).read_text()), a.key_fields)
    print(json.dumps(res, indent=2))
    return 0 if res["status"] == CLEAN else 1


if __name__ == "__main__":
    sys.exit(main())

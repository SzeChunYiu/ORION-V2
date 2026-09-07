"""Census of the pinned 1000+ theorems source: does it enumerate a NEGATIVE half that could
repair the degenerate formal witness?

Context. The registered witness screen found all 243 SD80 formal cases carrying one disposition,
FORMALIZABLE_AS_STATED, and attributed it to the case source. That attribution names a candidate
repair: the source tracks formalisation *status*, so the entries it lists as NOT formalised are a
half the pool never drew. This script measures whether that half is (a) present and (b) a witness.

It is (a) and not (b), and the distinction is the whole point: absence of a formalisation is
absence of evidence, not evidence that a statement resists formalisation.

`--self-test` plants both answers, so the census cannot only be able to say "no".
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Entry keys are a Wikidata id, optionally with a letter suffix for a variant theorem under the
# same id. Dropping the suffixed keys silently loses 20 entries and makes the census disagree with
# SD80 by one case -- which is how this parser was caught.
KEY_RE = re.compile(r"^(Q\d+[A-Za-z]*):$", re.M)
FIELD_RE = re.compile(r"^\s+([a-z_]+):", re.M)
FORMALISED_FIELDS = {"decl", "decls", "url"}
BAR_PER_DOMAIN = 61


def parse(text: str) -> dict[str, str]:
    parts = KEY_RE.split(text)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}


def fields(block: str) -> set[str]:
    return set(FIELD_RE.findall(block))


def census(text: str) -> dict:
    entries = parse(text)
    formalised = {q for q, b in entries.items() if fields(b) & FORMALISED_FIELDS}
    unformalised = {q: b for q, b in entries.items() if q not in formalised}
    title_only = {q for q, b in unformalised.items() if fields(b) == {"title"}}
    commented = {q for q, b in entries.items() if "comment" in fields(b)}
    return {
        "n_entries": len(entries),
        "n_formalised": len(formalised),
        "n_unformalised": len(unformalised),
        "n_unformalised_title_only": len(title_only),
        "n_entries_with_any_comment": len(commented),
        "adverse_seam_upper_bound": len(commented),
        "bar_per_domain": BAR_PER_DOMAIN,
        "seam_clears_bar": len(commented) >= BAR_PER_DOMAIN,
        "formalised_ids": sorted(formalised),
    }


def _self_test() -> int:
    checks = []
    # Planted: a source WITH an adjudicated negative half must be reported as having one.
    rich = "\n".join(
        f"Q{i}:\n  title: t{i}\n  comment: statement as given is false without extra hypotheses"
        for i in range(100))
    r = census(rich)
    checks.append(("planted: 100 commented entries are counted", r["n_entries_with_any_comment"] == 100))
    checks.append(("planted: a seam of 100 clears the bar of 61", r["seam_clears_bar"] is True))
    # Planted: a source with only titles has no seam at all.
    bare = "\n".join(f"Q{i}:\n  title: t{i}" for i in range(100))
    b = census(bare)
    checks.append(("planted: title-only source has an empty seam", b["adverse_seam_upper_bound"] == 0))
    checks.append(("planted: title-only source does not clear the bar", b["seam_clears_bar"] is False))
    checks.append(("planted: title-only entries are counted as such", b["n_unformalised_title_only"] == 100))
    # Planted: each formalisation marker is recognised, and a suffixed key is not dropped.
    mixed = ("Q1:\n  title: a\n  decl: X\n"
             "Q2:\n  title: b\n  decls:\n   - Y\n"
             "Q3:\n  title: c\n  url: https://example/z.lean\n"
             "Q4X:\n  title: d\n  decl: W\n"
             "Q5:\n  title: e\n")
    m = census(mixed)
    checks.append(("decl, decls, url and a SUFFIXED key all count as formalised",
                   m["n_formalised"] == 4 and "Q4X" in m["formalised_ids"]))
    checks.append(("an entry with none of them is unformalised", m["n_unformalised"] == 1))
    failed = [n for n, ok in checks if not ok]
    for n, ok in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {n}")
    print(f"{len(checks) - len(failed)}/{len(checks)} pass")
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source")
    ap.add_argument("--sd80-keys")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return _self_test()
    out = census(Path(a.source).read_text())
    if a.sd80_keys:
        keys = json.loads(Path(a.sd80_keys).read_text())["keys"]
        sd80 = {q.removeprefix("FORMAL-") for q in keys if q.startswith("FORMAL-")}
        formal = set(out.pop("formalised_ids"))
        out["sd80_formal_cases"] = len(sd80)
        out["sd80_minus_formalised"] = sorted(sd80 - formal)
        out["formalised_minus_sd80"] = sorted(formal - sd80)
        out["sd80_is_exactly_the_formalised_side"] = not (sd80 ^ formal)
    else:
        out.pop("formalised_ids")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

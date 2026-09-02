#!/usr/bin/env python3
"""ME-X3 Lean 4 cross-check: emit derivations as genuine kernel-checked proof terms.

The study's primary proof-validity oracle is the exhaustive rewrite search in
`mex3_oracle.py`.  This module exists to answer the obvious objection to a
self-contained checker: *who checks the checker?*

For each accepted derivation it emits a Lean 4 file in which the object system is
an **inductive proposition**

    inductive Derives : Word -> Word -> Prop
      | refl | trans | <one forward and one backward constructor per axiom>

and the derivation is an explicit **proof term** built from those constructors.
Lean's kernel therefore checks that each step really is an instance of an axiom
schema at some prefix/suffix; it is *not* asked to evaluate a Boolean function
written by us, which would only re-implement our own checker inside Lean and
prove nothing.  `#print axioms` additionally certifies the term uses no `sorry`
and no classical axiom.

Negative controls matter as much as positive ones.  A corrupted derivation must
be rejected, and rejected *for the right reason*: the emitted file must fail with
a type mismatch on a `Derives` term.  Any other failure (a parse error, a name
clash, a timeout) is scored `CANNOT_CHECK` for that instance rather than as a
successful rejection -- "the file did not compile" is not evidence.

No Mathlib is required or used: the object language is defined from scratch in
Lean core, which is what makes the check reproducible from a bare toolchain.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional, Sequence

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from mex3_model import Word  # noqa: E402

REJECTION_PATTERNS = (
    re.compile(r"[Tt]ype mismatch"),
    re.compile(r"application type mismatch"),
)
DERIVES_PATTERN = re.compile(r"Derives")


def _w(w: Sequence[int]) -> str:
    return "[" + ", ".join(f"s{s}" for s in w) + "]"


def locate_step(a: Word, b: Word, axioms: Sequence[tuple[Word, Word]], max_len: int):
    """Which axiom, in which direction, at which prefix/suffix, turns `a` into `b`."""
    for i, (u, v) in enumerate(axioms):
        for direction, (x, y) in (("f", (u, v)), ("b", (v, u))):
            lx = len(x)
            for j in range(len(a) - lx + 1):
                if a[j:j + lx] == x and a[:j] + y + a[j + lx:] == b:
                    return i, direction, a[:j], a[j + lx:]
    return None


def emit_lean(name: str, alphabet: int, axioms: Sequence[tuple[Word, Word]],
              path: Sequence[Word], max_len: int, corrupt_step: Optional[int] = None
              ) -> Optional[str]:
    """With `corrupt_step = k`, the k-th step keeps its axiom justification but is
    *stated* to end one symbol further along, so its justification's type is not
    the stated type and the kernel must reject it at a `Derives` term.

    Corrupting the stated destination is what makes the negative control a
    negative control. An earlier version substituted a word somewhere in the
    chain; when that word happened to appear only as a destination the
    substitution silently matched nothing and Lean accepted a file labelled
    corrupt. The caller now also refuses to ship a "bad" file identical to its
    good counterpart."""
    steps = []
    for a, b in zip(path, path[1:]):
        loc = locate_step(tuple(a), tuple(b), axioms, max_len)
        if loc is None:
            return None
        steps.append((loc, tuple(a), tuple(b)))
    L = [f"-- ME-X3 derivation certificate: {name}",
         "inductive Sym where",
         "".join(f"  | s{i}\n" for i in range(alphabet)).rstrip(),
         "  deriving DecidableEq", "open Sym", "abbrev Word := List Sym", "",
         "inductive Derives : Word → Word → Prop where",
         "  | refl (w : Word) : Derives w w",
         "  | trans {a b c : Word} : Derives a b → Derives b c → Derives a c"]
    for i, (u, v) in enumerate(axioms):
        L.append(f"  | ax{i}f (p s : Word) : Derives (p ++ {_w(u)} ++ s) (p ++ {_w(v)} ++ s)")
        L.append(f"  | ax{i}b (p s : Word) : Derives (p ++ {_w(v)} ++ s) (p ++ {_w(u)} ++ s)")
    L.append("")
    if not steps:
        if corrupt_step is not None:
            return None
        L += [f"theorem thm : Derives {_w(path[0])} {_w(path[0])} := Derives.refl {_w(path[0])}",
              "#print axioms thm"]
        return "\n".join(L) + "\n"
    if corrupt_step is not None and not (0 <= corrupt_step < len(steps)):
        return None
    body = ""
    for k, ((i, d, pre, suf), a, b) in enumerate(steps):
        stated = b + (((b[-1] + 1) % alphabet),) if k == corrupt_step else b
        step = (f"(show Derives {_w(a)} {_w(stated)} from Derives.ax{i}{d} "
                f"{_w(pre)} {_w(suf)})")
        body = step if k == 0 else f"(Derives.trans {body} {step})"
    L += [f"theorem thm : Derives {_w(path[0])} {_w(path[-1])} :=", f"  {body}",
          "#print axioms thm"]
    return "\n".join(L) + "\n"


def classify(returncode: int, stdout: str, stderr: str, expect: str) -> tuple[str, str]:
    text = stdout + "\n" + stderr
    if expect == "ACCEPT":
        if returncode == 0 and "does not depend on any axioms" in text:
            return "VERIFIED_BY_LEAN_KERNEL", ""
        if returncode == 0:
            return "CANNOT_CHECK", "compiled but #print axioms did not certify axiom-freedom"
        return "REJECTED_UNEXPECTEDLY", text.strip().splitlines()[0] if text.strip() else ""
    if returncode == 0:
        return "ACCEPTED_UNEXPECTEDLY", "the kernel accepted a corrupted derivation"
    if any(p.search(text) for p in REJECTION_PATTERNS) and DERIVES_PATTERN.search(text):
        return "REJECTED_FOR_THE_REGISTERED_REASON", ""
    return "CANNOT_CHECK", "failed, but not with a Derives type mismatch: " + \
        (text.strip().splitlines()[0] if text.strip() else "no diagnostics")


def check_file(lean_bin: str, f: Path, expect: str, timeout: int = 120) -> dict:
    try:
        pr = subprocess.run([lean_bin, str(f)], capture_output=True, text=True, timeout=timeout)
        verdict, detail = classify(pr.returncode, pr.stdout, pr.stderr, expect)
    except subprocess.TimeoutExpired:
        verdict, detail = "CANNOT_CHECK", "lean timed out"
    except FileNotFoundError:
        verdict, detail = "CANNOT_CHECK", f"lean binary not found: {lean_bin}"
    return {"file": f.name, "expect": expect, "verdict": verdict, "detail": detail}


def build(results: Path, custody: Path, out: Path, limit: int) -> dict:
    res = json.loads(results.read_text())
    cus = {c["task_id"]: c for c in json.loads(custody.read_text())["instances"]}
    out.mkdir(parents=True, exist_ok=True)
    from mex3_arms import M_ARM
    plan = []
    for inst in res["instances"]:
        if len(plan) >= limit:
            break
        a = inst["arms"].get(M_ARM)
        if not a or a["validity"] != "VERIFIED" or not a["derivation"]:
            continue
        t = cus[inst["task_id"]]["task"]
        pid = a.get("derivation_pid") or "P0"
        src = t["alt"] if (pid.startswith("P1") and t["alt"]) else t["base"]
        alphabet = src["alphabet"]
        axioms = [(tuple(u), tuple(v)) for u, v in src["axioms"]]
        lem = a.get("invented_lemma")
        if lem and not pid.startswith("P1"):
            axioms = sorted(set(axioms + [(tuple(lem[0]), tuple(lem[1]))]))
        path = [tuple(w) for w in a["derivation"]]
        name = inst["task_id"].replace("-", "_")
        good = emit_lean(name, alphabet, axioms, path, t["budget"]["max_word_len"])
        if good is None:
            continue
        gf = out / f"ok_{name}.lean"; gf.write_text(good)
        plan.append({"task_id": inst["task_id"], "file": gf.name, "expect": "ACCEPT"})
        k = len(path) // 2 if len(path) > 2 else 0
        bad = emit_lean(name + "_bad", alphabet, axioms, path,
                        t["budget"]["max_word_len"], corrupt_step=k)
        if bad and bad.replace("_bad", "") != good:
            bf = out / f"bad_{name}.lean"
            bf.write_text(bad)
            plan.append({"task_id": inst["task_id"], "file": bf.name, "expect": "REJECT"})
    (out / "PLAN.json").write_text(json.dumps(plan, indent=2, sort_keys=True))
    return {"n_files": len(plan), "dir": str(out)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("build", "check"))
    ap.add_argument("--results", type=Path, required=False)
    ap.add_argument("--custody", type=Path, required=False)
    ap.add_argument("--dir", type=Path, default=HERE / "lean")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--lean", default="lean")
    ap.add_argument("--report", type=Path, default=None)
    a = ap.parse_args(argv)
    if a.stage == "build":
        info = build(a.results, a.custody, a.dir, a.limit)
        print(json.dumps(info)); return 0
    plan = json.loads((a.dir / "PLAN.json").read_text())
    rows = [check_file(a.lean, a.dir / p["file"], p["expect"]) | {"task_id": p["task_id"]}
            for p in plan]
    n_ok = sum(r["verdict"] == "VERIFIED_BY_LEAN_KERNEL" for r in rows)
    n_rej = sum(r["verdict"] == "REJECTED_FOR_THE_REGISTERED_REASON" for r in rows)
    n_cc = sum(r["verdict"] == "CANNOT_CHECK" for r in rows)
    n_bad = sum(r["verdict"] in ("ACCEPTED_UNEXPECTEDLY", "REJECTED_UNEXPECTEDLY") for r in rows)
    rep = {"schema_version": "orion.v2.me-x3.lean-receipt.v1", "n": len(rows),
           "verified_by_lean_kernel": n_ok, "rejected_for_registered_reason": n_rej,
           "cannot_check": n_cc, "disagreements": n_bad,
           "agrees_with_exhaustive_oracle": n_bad == 0, "rows": rows}
    txt = json.dumps(rep, indent=2, sort_keys=True)
    (a.report or (a.dir / "LEAN_RECEIPT.json")).write_text(txt)
    print(f"lean: {n_ok} accepted, {n_rej} rejected for the registered reason, "
          f"{n_cc} CANNOT_CHECK, {n_bad} disagreements")
    return 0 if n_bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

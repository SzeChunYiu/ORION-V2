#!/usr/bin/env python3
"""H-EXT-1P — pre-freeze power and estimand audit, computed from the frozen H-EXT-1 tables.

H-EXT-1's receipt (item 2) records that the +2.1 pp margin of `GATED_M` over
`STRONGEST_ASSURANCE_FEDERATION` is a registered *threshold* comparison decided by 11
tasks, carrying no null, p-value or interval, and names an unstarted successor --
`H-EXT-1P` -- that would pre-register a paired null on `acc(GATED_M) - acc(PARENT)`.

This script is that successor's pre-freeze audit.  It answers two questions BEFORE any
freeze or dispatch, from data that already exists:

  1. POWER.  What n does an exact two-sided McNemar test need to detect the margin the
     frozen cell actually shows?  (A paired test turns on discordant pairs, not on n.)
  2. ESTIMAND.  Is the registered contrast capable of being *about* conditional
     activation at all?  It is decomposed into the gate-active and gate-inactive halves,
     because on gate-inactive tasks `GATED_M` IS the always-off arm by construction and
     the dependence machinery contributes nothing there.

Nothing here re-runs, re-scores or amends H-EXT-1.  The frozen per-instance tables are
read; `gate_fires` is imported from the study's own runner rather than reimplemented; and
the reconstruction is checked against three numbers the frozen receipt published
independently (activations, and the GATED / M / OFF / PARENT correct counts).

Exit codes -- "could not check" is kept distinct from "checked and fine":
  0  audit computed
  2  usage error
  3  CANNOT_CHECK: a frozen input is missing or unreadable
  4  CANNOT_CHECK: the reconstruction does not reproduce the frozen published control
     numbers, so nothing downstream of it may be believed
"""
from __future__ import annotations

import argparse
import json
import sys
from math import comb, exp, lgamma, log
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from h_ext1_gate_study import (  # noqa: E402
    ARM_M,
    ARM_OFF,
    ARM_PARENT,
    gate_fires,
)

H_EXT1 = ROOT / "research/experiments/h-ext1"
GATE_FREEZE = H_EXT1 / "H_EXT1_GATE_FREEZE.json"
TABLES = {
    "PROSPECTIVE": H_EXT1 / "data/PROSPECTIVE_instances.json",
    "RETROSPECTIVE": H_EXT1 / "data/RETROSPECTIVE_instances.json",
}

# Published in H_EXT1_OUTCOME_RECEIPT.md before this script existed.  They are the
# control on the reconstruction: a gate rule or arm-routing rule that did not match the
# frozen study would miss at least one of them.
FROZEN_CONTROL_PROSPECTIVE = {
    "n": 520, "activations": 170,
    "gated_correct": 508, "m_correct": 465, "off_correct": 428, "parent_correct": 497,
}

SCHEMA = "orion.v2.h-ext1p.pre-freeze-estimand-audit.v1"


# ---- exact paired statistics ---------------------------------------------------

def mcnemar_exact_two_sided(b: int, c: int) -> float:
    """Exact two-sided McNemar (binomial sign test on the discordant pairs).

    Integer arithmetic throughout; only the final ratio narrows to a float.
    """
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def critical_k(n_disc: int, alpha: float = 0.05) -> int:
    """Largest k with a two-sided exact p-value <= alpha when min(b, c) == k; -1 if none.

    n_disc <= 5 admits no rejection at alpha = 0.05 even when every pair agrees in sign
    (2 / 2**5 = 0.0625), which is why a ceiling tie cannot be rescued by more pairs of
    the same kind -- it has none.
    """
    best = -1
    for k in range(0, n_disc // 2 + 1):
        if mcnemar_exact_two_sided(k, n_disc - k) <= alpha:
            best = k
        else:
            break
    return best


def power_exact(n: int, pb: float, pc: float, alpha: float = 0.05) -> float:
    """Exact power of the two-sided exact McNemar test at n paired observations.

    Conditions on the discordant count: N ~ Binomial(n, pb + pc), and given N the
    GATED-only count is Binomial(N, pb / (pb + pc)).  No normal approximation.
    """
    pd = pb + pc
    if pd <= 0.0:
        return 0.0
    th = pb / pd
    total = 0.0
    for n_disc in range(0, n + 1):
        log_pn = (lgamma(n + 1) - lgamma(n_disc + 1) - lgamma(n - n_disc + 1)
                  + n_disc * log(pd) + (n - n_disc) * log(1 - pd) if pd < 1.0 else 0.0)
        p_n = exp(log_pn)
        if p_n < 1e-14 and n_disc > n * pd:
            break
        if p_n < 1e-14:
            continue
        k = critical_k(n_disc, alpha)
        if k < 0:
            continue
        lo = sum(comb(n_disc, i) * th ** i * (1 - th) ** (n_disc - i) for i in range(0, k + 1))
        hi = sum(comb(n_disc, i) * th ** i * (1 - th) ** (n_disc - i)
                 for i in range(n_disc - k, n_disc + 1))
        total += p_n * (lo + hi)
    return total


def smallest_n_for_power(pb: float, pc: float, target: float = 0.80,
                         alpha: float = 0.05, cap: int = 20000) -> int | None:
    """Smallest n reaching `target` power.  None if `cap` is not enough.

    Power in n is not perfectly monotone for an exact discrete test, so this walks
    upward on a grid and then confirms the neighbourhood rather than bisecting.
    """
    n = 100
    while n <= cap:
        if power_exact(n, pb, pc, alpha) >= target:
            lo = max(100, n - 100)
            for m in range(lo, n + 1, 10):
                if power_exact(m, pb, pc, alpha) >= target:
                    return m
            return n
        n += 100
    return None


# ---- reconstruction ------------------------------------------------------------

def paired_table(gated: list[bool], other: list[bool]) -> dict[str, Any]:
    b = sum(1 for x, y in zip(gated, other) if x and not y)
    c = sum(1 for x, y in zip(gated, other) if y and not x)
    both = sum(1 for x, y in zip(gated, other) if x and y)
    neither = sum(1 for x, y in zip(gated, other) if not x and not y)
    n = len(gated)
    return {
        "n": n, "gated_correct": sum(gated), "other_correct": sum(other),
        "gated_only_b": b, "other_only_c": c, "both": both, "neither": neither,
        "discordant": b + c,
        "margin_pp": round(100.0 * (sum(gated) - sum(other)) / n, 4) if n else 0.0,
        "exact_mcnemar_two_sided_p": mcnemar_exact_two_sided(b, c),
        "max_rejectable_at_alpha_0_05": critical_k(b + c, 0.05) >= 0,
    }


def reconstruct(table: dict[str, Any], gate_id: str) -> list[dict[str, Any]]:
    rows = []
    for r in table["rows"]:
        arms = r["arms"]
        fires = gate_fires(gate_id, r["features"])
        rows.append({
            "task_id": r["task_id"],
            "study_id": r["study_id"],
            "stratum": r.get("oracle_stratum_reporting_only"),
            "gate_active": fires,
            "gated": bool(arms[ARM_M]["correct"] if fires else arms[ARM_OFF]["correct"]),
            "m": bool(arms[ARM_M]["correct"]),
            "off": bool(arms[ARM_OFF]["correct"]),
            "parent": bool(arms[ARM_PARENT]["correct"]),
        })
    return rows


def control_check(rows: list[dict[str, Any]]) -> tuple[bool, dict[str, Any]]:
    got = {
        "n": len(rows),
        "activations": sum(1 for r in rows if r["gate_active"]),
        "gated_correct": sum(1 for r in rows if r["gated"]),
        "m_correct": sum(1 for r in rows if r["m"]),
        "off_correct": sum(1 for r in rows if r["off"]),
        "parent_correct": sum(1 for r in rows if r["parent"]),
    }
    return got == FROZEN_CONTROL_PROSPECTIVE, got


def audit(cell: str, rows: list[dict[str, Any]], power_grid: tuple[int, ...]) -> dict[str, Any]:
    gated = [r["gated"] for r in rows]
    parent = [r["parent"] for r in rows]
    m = [r["m"] for r in rows]
    active = [r for r in rows if r["gate_active"]]
    inactive = [r for r in rows if not r["gate_active"]]

    suite = paired_table(gated, parent)
    act = paired_table([r["gated"] for r in active], [r["parent"] for r in active])
    inact = paired_table([r["gated"] for r in inactive], [r["parent"] for r in inactive])

    by_study: dict[str, Any] = {}
    for sid in sorted({r["study_id"] for r in rows}):
        sub = [r for r in rows if r["study_id"] == sid]
        by_study[sid] = paired_table([r["gated"] for r in sub], [r["parent"] for r in sub])
        by_study[sid]["gate_activations"] = sum(1 for r in sub if r["gate_active"])

    n = len(rows)
    pb = suite["gated_only_b"] / n
    pc = suite["other_only_c"] / n
    power = {str(k): round(power_exact(k, pb, pc), 4) for k in power_grid}
    n80 = smallest_n_for_power(pb, pc, 0.80)
    n90 = smallest_n_for_power(pb, pc, 0.90)

    # The mechanism-attributable estimand's own sizing, computed rather than asserted.
    na = len(active)
    pba = act["gated_only_b"] / na if na else 0.0
    pca = act["other_only_c"] / na if na else 0.0
    active_sizing = {
        "n_active_in_frozen_cell": na,
        "discordant_pairs": act["discordant"],
        "pb": pba, "pc": pca,
        "n_for_80pc_power": (None if act["discordant"] == 0
                             else smallest_n_for_power(pba, pca, 0.80)),
        "note": ("with zero discordant pairs the observed effect on this estimand is "
                 "exactly zero and no n confers power on it; the two arms are tied at "
                 "the suite ceiling wherever the gate fires"),
    }

    return {
        "cell": cell,
        "n": n,
        "gate_activations": sum(1 for r in rows if r["gate_active"]),
        "acc": {
            "GATED": suite["gated_correct"] / n,
            "PARENT": suite["other_correct"] / n,
            "M": sum(m) / n,
        },
        "paired_GATED_vs_PARENT": {
            "SUITE": suite,
            "GATE_ACTIVE": act,
            "GATE_INACTIVE": inact,
            "BY_STUDY": by_study,
        },
        "power_suite_estimand": {
            "assumed_pb": pb, "assumed_pc": pc,
            "alpha": 0.05, "test": "exact two-sided McNemar",
            "power_by_n": power,
            "smallest_n_for_power_0_80": n80,
            "smallest_n_for_power_0_90": n90,
            "effect_source": ("the frozen H-EXT-1 cell itself; this is an observed-effect "
                              "power calculation and is optimistic by the winner's curse, "
                              "so any n derived from it is a LOWER bound on what a "
                              "prospective replication needs"),
        },
        "power_mechanism_estimand": active_sizing,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=None,
                    help="write the audit JSON here")
    ap.add_argument("--power-grid", type=str,
                    default="520,800,1000,1200,1500,2000,3000")
    a = ap.parse_args(argv)

    if not GATE_FREEZE.exists():
        print(f"CANNOT_CHECK: gate freeze absent ({GATE_FREEZE})", file=sys.stderr)
        return 3
    freeze = json.loads(GATE_FREEZE.read_text())
    gate_id = freeze["selected_gate"]

    cells: dict[str, Any] = {}
    grid = tuple(int(x) for x in a.power_grid.split(","))
    for cell, path in TABLES.items():
        if not path.exists():
            print(f"CANNOT_CHECK: frozen instance table absent ({path})", file=sys.stderr)
            return 3
        table = json.loads(path.read_text())
        rows = reconstruct(table, gate_id)
        if cell == "PROSPECTIVE":
            ok, got = control_check(rows)
            if not ok:
                print("CANNOT_CHECK: reconstruction does not reproduce the frozen "
                      f"published control numbers.\n  expected {FROZEN_CONTROL_PROSPECTIVE}"
                      f"\n  got      {got}", file=sys.stderr)
                return 4
        cells[cell] = audit(cell, rows, grid)

    out = {
        "schema_version": SCHEMA,
        "reads": {k: str(v.relative_to(ROOT)) for k, v in TABLES.items()},
        "gate_id_from_freeze": gate_id,
        "gate_rule_source": "scripts/h_ext1_gate_study.py::gate_fires (imported, not reimplemented)",
        "reconstruction_control": {
            "expected_from_frozen_receipt": FROZEN_CONTROL_PROSPECTIVE,
            "reproduced": True,
            "note": ("six independently published frozen quantities; a wrong gate rule or a "
                     "wrong GATED routing rule would miss at least one"),
        },
        "cells": cells,
    }
    text = json.dumps(out, indent=2, sort_keys=True)
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(text + "\n")
    p = cells["PROSPECTIVE"]
    s = p["paired_GATED_vs_PARENT"]
    print(f"gate {gate_id}; PROSPECTIVE n={p['n']} activations={p['gate_activations']}")
    print(f"  SUITE          b={s['SUITE']['gated_only_b']} c={s['SUITE']['other_only_c']} "
          f"p={s['SUITE']['exact_mcnemar_two_sided_p']:.4f}")
    print(f"  GATE_ACTIVE    n={s['GATE_ACTIVE']['n']} "
          f"GATED={s['GATE_ACTIVE']['gated_correct']} PARENT={s['GATE_ACTIVE']['other_correct']} "
          f"b={s['GATE_ACTIVE']['gated_only_b']} c={s['GATE_ACTIVE']['other_only_c']}")
    print(f"  GATE_INACTIVE  n={s['GATE_INACTIVE']['n']} "
          f"b={s['GATE_INACTIVE']['gated_only_b']} c={s['GATE_INACTIVE']['other_only_c']}")
    pw = p["power_suite_estimand"]
    print(f"  power(n=520)={pw['power_by_n']['520']}  n@0.80={pw['smallest_n_for_power_0_80']}"
          f"  n@0.90={pw['smallest_n_for_power_0_90']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

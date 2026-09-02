#!/usr/bin/env python3
"""E70-GC2: off-ceiling generated source-composition suite (design V1).

Successor to the saturated E70-GC1 family.  Standard library only.  The generator
renders a *frozen difficulty ladder* (L1 < L2 < L3) of multi-fragment, multi-file
composition tasks with hidden regression / counterfactual / surface-trap checks.
The level used for the protected run is chosen by an outcome-blind calibration of
the SIMPLE_DIRECT arm on a development split (dev seed only); the protected run
uses a distinct seed and a per-run secret nonce whose sha256 is committed in
FROZEN_TASKS.json while the nonce itself lives only under ``private/`` (absent from
disk during blinded dispatch, see ``scripts/dispatch_orion_gc1_blinded.py``).

Primary endpoint: COUNT-ROBUST native success = the emitted unified diff, after the
registered syntax-only canonicalization (E20/E30: recompute hunk counts and a/b
headers from the patch itself; never infer paths or semantics), applies and passes
every hidden check.  Raw header-exact success is the secondary interface-fidelity
endpoint.  Nothing here grants scientific truth, field status or submission
readiness; the suite is secondary anti-copy / composition evidence only.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import math
import os
import random
import re
import shutil
import string
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from orion_v2.unified_diff_interface import audit_and_canonicalize_unified_diff

ROOT = Path(__file__).resolve().parents[1]
DESIGN_PATH = ROOT / "research/experiments/e70-gc2/E70_GC2_OFFCEILING_DESIGN_V1.json"
DEFAULT_WORKDIR = ROOT / ".orion-generated-composition-gc2"
GC1_RUNNER = ROOT / "scripts/run_orion_generated_composition_suite.py"
BLINDED_DISPATCHER = ROOT / "scripts/dispatch_orion_gc1_blinded.py"
DIFF_PATH_RE = re.compile(r"^diff --git a/(?P<a>[^\n]+) b/(?P<b>[^\n]+)$", re.MULTILINE)

ARMS = ("SIMPLE_DIRECT", "SAME_MODEL_REFLECTION", "F0_PARENT_FEDERATION", "F2_ORION_METABOLIC_FULL")
F2 = "F2_ORION_METABOLIC_FULL"
CONTROL_ORDER = ("F0_PARENT_FEDERATION", "SIMPLE_DIRECT", "SAME_MODEL_REFLECTION")

# Frozen difficulty ladder.  Every rung is a strict superset of the previous one.
LADDER: dict[str, dict[str, Any]] = {
    "L1": {
        "title": "distractor + erratum + offset unit + 2-file normalization contract",
        "editable_files": ["solver.py", "normalize.py"],
        "erratum": True, "distractor": True, "offset_unit": True,
        "alias_unit": False, "codebook": False, "tiebreak": False, "ambiguity_band": False, "batch_quota": False,
        "hidden_random": 120, "counterfactual_pairs": 16, "normalize_checks": 24, "batch_checks": 0,
    },
    "L2": {
        "title": "L1 + unit alias chain + codebook file + tie-break + ambiguity band (3 files, 9 fragments)",
        "editable_files": ["solver.py", "normalize.py", "codebook.py"],
        "erratum": True, "distractor": True, "offset_unit": True,
        "alias_unit": True, "codebook": True, "tiebreak": True, "ambiguity_band": True, "batch_quota": False,
        "hidden_random": 160, "counterfactual_pairs": 24, "normalize_checks": 32, "batch_checks": 0,
    },
    "L3": {
        "title": "L2 + order-dependent per-source accept quota (decide_batch, 10 fragments)",
        "editable_files": ["solver.py", "normalize.py", "codebook.py"],
        "erratum": True, "distractor": True, "offset_unit": True,
        "alias_unit": True, "codebook": True, "tiebreak": True, "ambiguity_band": True, "batch_quota": True,
        "hidden_random": 160, "counterfactual_pairs": 24, "normalize_checks": 32, "batch_checks": 12,
    },
}
LEVEL_ORDER = ("L1", "L2", "L3")


class SuiteError(RuntimeError):
    pass


# --------------------------------------------------------------------------- io
def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SuiteError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SuiteError(f"expected JSON object: {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(path)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def random_token(rng: random.Random, prefix: str, length: int = 6) -> str:
    return prefix + "_" + "".join(rng.choice(string.ascii_uppercase) for _ in range(length))


# ------------------------------------------------------------------ generation
def generate_spec(rng: random.Random, index: int, level: str) -> dict[str, Any]:
    cfg = LADDER[level]
    modulus = rng.choice([17, 19, 23, 29, 31])
    low = rng.randint(3, modulus // 3)
    high_doc = rng.randint(max(low + 5, (2 * modulus) // 3), modulus - 3)
    high_eff = high_doc + rng.choice([-2, -1, 1, 2]) if cfg["erratum"] else high_doc
    high_eff = max(low + 4, min(modulus - 1, high_eff))
    sources = [random_token(rng, f"SRC{index}", 5) for _ in range(5)]
    doc_authorized = sorted(rng.sample(sources, 3))
    revoked = rng.choice(doc_authorized) if cfg["erratum"] else None
    authorized = [s for s in doc_authorized if s != revoked]
    labels = {
        "accept": random_token(rng, "GO", 5),
        "review": random_token(rng, "HOLD", 5),
        "reject": random_token(rng, "STOP", 5),
        "unknown": random_token(rng, "UNK", 5),
    }
    superseded_labels = {k: random_token(rng, "OLD", 5) for k in labels}
    spec: dict[str, Any] = {
        "level": level,
        "task_index": index,
        "a": rng.choice([2, 3, 4, 5, 7]),
        "b": rng.choice([2, 3, 5, 6, 7]),
        "c": rng.randint(1, modulus - 1),
        "modulus": modulus,
        "low": low,
        "high_doc": high_doc,
        "high": high_eff,
        "unit_primary": random_token(rng, "UNITA", 5),
        "unit_scaled": random_token(rng, "UNITB", 5),
        "scale_factor": rng.randint(2, 7),
        "unit_offset": random_token(rng, "UNITC", 5) if cfg["offset_unit"] else None,
        "offset_scale": rng.randint(2, 5),
        "offset_shift": rng.choice([-9, -7, -5, -3, 3, 5, 7, 9]),
        "unit_alias": random_token(rng, "LEGACY", 5) if cfg["alias_unit"] else None,
        "unit_deprecated": random_token(rng, "RETIRED", 5) if cfg["alias_unit"] else None,
        "all_sources": sources,
        "doc_authorized_sources": doc_authorized,
        "revoked_source": revoked,
        "allowed_sources": sorted(authorized),
        "primary_authority": sorted(authorized)[0],
        "labels": labels,
        "superseded_labels": superseded_labels,
        "superseded_low": max(1, low - rng.randint(1, 2)),
        "superseded_high": min(modulus - 1, high_doc + rng.randint(1, 2)),
        "tiebreak": cfg["tiebreak"],
        "ambiguity_band": cfg["ambiguity_band"],
        "batch_quota": rng.randint(2, 3) if cfg["batch_quota"] else None,
        "editable_files": list(cfg["editable_files"]),
    }
    return spec


def normalize_x(x: int, unit: str | None, spec: dict[str, Any]) -> int | None:
    """Oracle for normalize.to_primary(x, unit): primary-unit integer or None."""
    if unit == spec["unit_primary"]:
        return int(x)
    if unit == spec["unit_scaled"]:
        return int(x) * int(spec["scale_factor"])
    if spec["unit_offset"] and unit == spec["unit_offset"]:
        return int(x) * int(spec["offset_scale"]) + int(spec["offset_shift"])
    if spec["unit_alias"] and unit == spec["unit_alias"]:
        return int(x) * int(spec["scale_factor"])
    return None


def oracle(record: dict[str, Any], spec: dict[str, Any]) -> str:
    labels = spec["labels"]
    source = record.get("source")
    if source not in spec["allowed_sources"]:
        return labels["unknown"]
    x = normalize_x(int(record["x"]), record.get("unit"), spec)
    if x is None:
        return labels["unknown"]
    y = int(record["y"])
    score = (int(spec["a"]) * x + int(spec["b"]) * y + int(spec["c"])) % int(spec["modulus"])
    if bool(record.get("counterexample")):
        return labels["review"]
    if spec["ambiguity_band"] and score in (spec["low"] + 1, spec["low"] + 2):
        return labels["reject"] if source == spec["primary_authority"] else labels["review"]
    if spec["tiebreak"] and score == spec["high"] - 1 and y % 2 == 0:
        return labels["accept"]
    if score >= int(spec["high"]):
        return labels["accept"]
    if score <= int(spec["low"]):
        return labels["reject"]
    return labels["review"]


def oracle_batch(records: list[dict[str, Any]], spec: dict[str, Any]) -> list[str]:
    labels = spec["labels"]
    quota = spec["batch_quota"]
    accepts: dict[str, int] = {}
    out: list[str] = []
    for record in records:
        label = oracle(record, spec)
        if quota is not None and label == labels["accept"]:
            source = str(record.get("source"))
            accepts[source] = accepts.get(source, 0) + 1
            if accepts[source] > quota:
                label = labels["review"]
        out.append(label)
    return out


def unit_pool(spec: dict[str, Any], rng: random.Random) -> list[str]:
    units = [spec["unit_primary"], spec["unit_scaled"]]
    if spec["unit_offset"]:
        units.append(spec["unit_offset"])
    if spec["unit_alias"]:
        units += [spec["unit_alias"], spec["unit_deprecated"]]
    units.append(random_token(rng, "BADUNIT", 4))
    return units


def random_record(rng: random.Random, spec: dict[str, Any]) -> dict[str, Any]:
    sources = list(spec["all_sources"]) + [random_token(rng, "OUTSIDE", 4)]
    weights = [3 if s in spec["allowed_sources"] else 1 for s in sources]
    return {
        "x": rng.randint(-80, 80),
        "y": rng.randint(-40, 40),
        "unit": rng.choice(unit_pool(spec, rng)),
        "source": rng.choices(sources, weights=weights, k=1)[0],
        "counterexample": bool(rng.getrandbits(1)) if rng.random() < 0.2 else False,
    }


def find_public_examples(rng: random.Random, spec: dict[str, Any], count: int = 5) -> list[dict[str, Any]]:
    examples: list[dict[str, Any]] = []
    seen: set[str] = set()
    for _ in range(6000):
        record = random_record(rng, spec)
        expected = oracle(record, spec)
        if expected in seen and len(examples) < 4:
            continue
        examples.append({"record": record, "expected": expected})
        seen.add(expected)
        if len(examples) >= count:
            break
    if len(examples) < count:
        raise SuiteError("failed to generate public examples")
    return examples


def _score_record(spec: dict[str, Any], target_score: int, rng: random.Random, unit: str | None = None,
                  source: str | None = None, y: int | None = None) -> dict[str, Any]:
    """Construct a record whose modular score equals target_score (unit primary by default)."""
    m = int(spec["modulus"])
    y = rng.randint(-40, 40) if y is None else y
    unit = unit or spec["unit_primary"]
    source = source or spec["primary_authority"]
    for x in range(-200, 201):
        xn = normalize_x(x, unit, spec)
        if xn is None:
            break
        if (spec["a"] * xn + spec["b"] * y + spec["c"]) % m == target_score % m:
            return {"x": x, "y": y, "unit": unit, "source": source, "counterexample": False}
    raise SuiteError("no record hits the target score")


def hidden_checks(rng: random.Random, spec: dict[str, Any], examples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cfg = LADDER[spec["level"]]
    labels = spec["labels"]
    valid = spec["primary_authority"]
    checks: list[dict[str, Any]] = []

    def add_decide(record: dict[str, Any], family: str) -> None:
        checks.append({"kind": "decide", "family": family, "record": record, "expected": oracle(record, spec)})

    # Regression family: behaviours the incomplete baseline already gets right must survive the repair.
    add_decide({"x": 1, "y": 2, "unit": spec["unit_primary"], "source": "UNREGISTERED_PRIVATE_SOURCE", "counterexample": False}, "regression")
    add_decide({"x": -3, "y": 4, "unit": spec["unit_scaled"], "source": random_token(rng, "OUTSIDE", 4), "counterexample": True}, "regression")
    # Forced edge family.
    if spec["revoked_source"]:
        add_decide({"x": 4, "y": 1, "unit": spec["unit_primary"], "source": spec["revoked_source"], "counterexample": False}, "edge_revoked_source")
    add_decide({"x": 2, "y": 1, "unit": "UNREGISTERED_PRIVATE_UNIT", "source": valid, "counterexample": False}, "edge_unknown_unit")
    add_decide({"x": 5, "y": 3, "unit": spec["unit_primary"], "source": valid, "counterexample": True}, "edge_counterexample")
    add_decide(_score_record(spec, spec["high"], rng), "edge_threshold_high_eff")
    add_decide(_score_record(spec, spec["high"] - 1, rng, y=rng.randrange(-39, 40, 2)), "edge_threshold_high_eff_minus_one_odd_y")
    add_decide(_score_record(spec, spec["high_doc"], rng), "edge_threshold_high_doc_trap")
    add_decide(_score_record(spec, spec["low"], rng), "edge_threshold_low")
    add_decide(_score_record(spec, spec["low"] + 1, rng), "edge_threshold_low_plus_one")
    if spec["unit_offset"]:
        add_decide(_score_record(spec, spec["high"], rng, unit=spec["unit_offset"], y=-7), "edge_offset_unit_negative")
    if spec["unit_alias"]:
        add_decide(_score_record(spec, spec["high"], rng, unit=spec["unit_alias"]), "edge_alias_unit")
        add_decide({"x": 3, "y": 3, "unit": spec["unit_deprecated"], "source": valid, "counterexample": False}, "edge_deprecated_alias")
    if spec["tiebreak"]:
        add_decide(_score_record(spec, spec["high"] - 1, rng, y=rng.randrange(-40, 40, 2)), "edge_tiebreak_even_y")
    if spec["ambiguity_band"]:
        other = [s for s in spec["allowed_sources"] if s != valid][0]
        add_decide(_score_record(spec, spec["low"] + 1, rng, source=valid), "edge_ambiguity_primary_authority")
        add_decide(_score_record(spec, spec["low"] + 2, rng, source=other), "edge_ambiguity_secondary_authority")
    # Random family.
    for _ in range(cfg["hidden_random"]):
        add_decide(random_record(rng, spec), "random")
    # Counterfactual twins: one-field interventions that flip the oracle label.
    pairs = 0
    attempts = 0
    while pairs < cfg["counterfactual_pairs"] and attempts < 4000:
        attempts += 1
        base = random_record(rng, spec)
        base["source"] = rng.choice(spec["allowed_sources"])
        base["unit"] = rng.choice([spec["unit_primary"], spec["unit_scaled"]])
        base["counterexample"] = False
        twin = dict(base)
        mutation = rng.choice(["source_revoked", "source_outside", "unit_offset", "unit_alias", "x_shift", "counterexample", "y_parity"])
        if mutation == "source_revoked" and spec["revoked_source"]:
            twin["source"] = spec["revoked_source"]
        elif mutation == "source_outside":
            twin["source"] = random_token(rng, "OUTSIDE", 4)
        elif mutation == "unit_offset" and spec["unit_offset"]:
            twin["unit"] = spec["unit_offset"]
        elif mutation == "unit_alias" and spec["unit_alias"]:
            twin["unit"] = spec["unit_alias"]
        elif mutation == "x_shift":
            twin["x"] = base["x"] + rng.choice([-3, -2, -1, 1, 2, 3])
        elif mutation == "counterexample":
            twin["counterexample"] = True
        elif mutation == "y_parity":
            twin["y"] = base["y"] + 1
        else:
            continue
        if oracle(twin, spec) == oracle(base, spec):
            continue
        add_decide(base, "counterfactual_base")
        add_decide(twin, f"counterfactual_twin:{mutation}")
        pairs += 1
    # Surface-template traps: public examples re-issued with one hidden field changed.
    for item in examples:
        rec = dict(item["record"])
        if spec["revoked_source"]:
            trap = dict(rec, source=spec["revoked_source"])
            add_decide(trap, "surface_trap_revoked_source")
        if spec["unit_alias"]:
            add_decide(dict(rec, unit=spec["unit_deprecated"]), "surface_trap_deprecated_unit")
        add_decide(dict(rec, x=rec["x"] + spec["modulus"]), "surface_trap_modulus_shift")
    # Normalization contract (cross-file dependency; hidden).
    for _ in range(cfg["normalize_checks"]):
        x = rng.randint(-60, 60)
        unit = rng.choice(unit_pool(spec, rng))
        checks.append({"kind": "normalize", "family": "normalize_contract", "x": x, "unit": unit, "expected": normalize_x(x, unit, spec)})
    if cfg["codebook"]:
        for key, value in labels.items():
            checks.append({"kind": "codebook", "family": "codebook_contract", "key": key, "expected": value})
    # Order-dependent batches.
    for _ in range(cfg["batch_checks"]):
        batch: list[dict[str, Any]] = []
        for _ in range(10):
            rec = random_record(rng, spec)
            if rng.random() < 0.6:
                rec["source"] = spec["primary_authority"]
                rec["unit"] = spec["unit_primary"]
                rec["counterexample"] = False
                rec = _score_record(spec, rng.randint(spec["high"], spec["modulus"] - 1), rng, y=rec["y"]) | {"source": spec["primary_authority"]}
            batch.append(rec)
        checks.append({"kind": "batch", "family": "batch_quota", "records": batch, "expected": oracle_batch(batch, spec)})
    return checks


# ------------------------------------------------------------ public rendering
def render_sources(spec: dict[str, Any]) -> dict[str, str]:
    labels = spec["labels"]
    old = spec["superseded_labels"]
    docs: dict[str, str] = {}
    docs["01_measurement.md"] = (
        "# Measurement rule\n\n"
        f"The primary unit token is `{spec['unit_primary']}`; a primary-unit `x` is used as is.\n\n"
        f"The scaled unit token is `{spec['unit_scaled']}`: convert with `x_primary = x * {spec['scale_factor']}`.\n\n"
        + (f"The offset unit token is `{spec['unit_offset']}`: convert with `x_primary = x * {spec['offset_scale']} + ({spec['offset_shift']})`.\n\n" if spec["unit_offset"] else "")
        + "Any other unit token is outside the measurement contract (see the decision codebook for the outcome).\n\n"
        f"For a usable measurement compute `score = ({spec['a']} * x_primary + {spec['b']} * y + {spec['c']}) mod {spec['modulus']}` "
        "using the least non-negative residue (Python `%` semantics).\n\n"
        "`normalize.to_primary(x, unit)` must return the primary-unit integer for every recognized unit token and `None` for any other token.\n"
    )
    docs["02_authority.md"] = (
        "# Source authority rule\n\n"
        "A record can support a substantive decision only when its `source` token is in this authorized set:\n\n"
        + "\n".join(f"- `{s}`" for s in spec["doc_authorized_sources"])
        + f"\n\nThe primary authority is `{spec['primary_authority']}`. Other source tokens do not authorize a substantive decision.\n"
        + "\nThis document is subject to the erratum in `06_erratum.md`.\n"
    )
    docs["03_decision.md"] = (
        "# Decision codebook and thresholds\n\n"
        f"Unknown/unusable evidence (unauthorized source or unrecognized unit) returns `{labels['unknown']}`.\n\n"
        f"A registered counterexample returns `{labels['review']}`.\n\n"
        f"Otherwise score >= {spec['high_doc']} returns `{labels['accept']}`; score <= {spec['low']} returns `{labels['reject']}`; "
        f"intermediate scores return `{labels['review']}`.\n"
    )
    order = ["source authority (02, as amended by 06)", "recognized measurement unit and normalization (01" + (", 07" if spec["unit_alias"] else "") + ")",
             "counterexample override (03)"]
    if spec["ambiguity_band"]:
        order.append("ambiguity band (09)")
    if spec["tiebreak"]:
        order.append("tie-break (08)")
    order.append("score thresholds (03, as amended by 06)")
    docs["04_precedence.md"] = (
        "# Precedence\n\n"
        "Apply the rules in this order; the first rule that fires decides:\n\n"
        + "\n".join(f"{i + 1}. {item}" for i, item in enumerate(order))
        + "\n\nAn erratum overrides the document it amends. Superseded documents are not in force.\n"
        + ("\nBatch processing (10) is applied on top of the single-record decision, in record order.\n" if spec["batch_quota"] else "")
    )
    docs["05_superseded_revision.md"] = (
        "# SUPERSEDED decision revision (archival only; NOT in force)\n\n"
        f"Historical codebook: accept = `{old['accept']}`, review = `{old['review']}`, reject = `{old['reject']}`, unknown = `{old['unknown']}`.\n\n"
        f"Historical thresholds: score >= {spec['superseded_high']} accepted; score <= {spec['superseded_low']} rejected.\n\n"
        "This revision was replaced by `03_decision.md` and must not be implemented.\n"
    )
    docs["06_erratum.md"] = (
        "# Erratum (in force; overrides 02 and 03)\n\n"
        f"1. The acceptance threshold in `03_decision.md` is corrected: score >= {spec['high']} returns `{labels['accept']}` (not {spec['high_doc']}).\n"
        + (f"2. The authorization of source `{spec['revoked_source']}` is revoked; it no longer authorizes a substantive decision.\n" if spec["revoked_source"] else "")
    )
    if spec["unit_alias"]:
        docs["07_unit_aliases.md"] = (
            "# Unit aliases\n\n"
            f"The legacy token `{spec['unit_alias']}` is an alias of `{spec['unit_scaled']}` and converts identically.\n\n"
            f"The token `{spec['unit_deprecated']}` is retired and is NOT recognized (treat as an unknown unit).\n"
        )
    if spec["tiebreak"]:
        docs["08_tiebreak.md"] = (
            "# Tie-break\n\n"
            f"When score == {spec['high'] - 1} (one below the corrected acceptance threshold) and `y` is even, return `{labels['accept']}`.\n"
        )
    if spec["ambiguity_band"]:
        docs["09_ambiguity_band.md"] = (
            "# Ambiguity band\n\n"
            f"When score is {spec['low'] + 1} or {spec['low'] + 2}: return `{labels['reject']}` if the source is the primary authority "
            f"`{spec['primary_authority']}`, otherwise `{labels['review']}`.\n"
        )
    if spec["batch_quota"]:
        docs["10_batch_quota.md"] = (
            "# Batch quota\n\n"
            "`solver.decide_batch(records)` returns one label per record, in order. Within one batch each source may contribute at most "
            f"{spec['batch_quota']} `{labels['accept']}` decisions; every later record from that source that would be accepted returns "
            f"`{labels['review']}` instead. Records that are not accepted do not consume quota.\n"
        )
    return docs


def render_public_workspace(path: Path, spec: dict[str, Any], examples: list[dict[str, Any]]) -> None:
    labels = spec["labels"]
    path.mkdir(parents=True, exist_ok=True)
    (path / "sources").mkdir()
    (path / "tests").mkdir()
    for name, text in render_sources(spec).items():
        (path / "sources" / name).write_text(text, encoding="utf-8")
    imports = "from normalize import to_primary\n"
    unknown_expr = f"{labels['unknown']!r}"
    accept_expr = f"{labels['accept']!r}"
    if spec["editable_files"].count("codebook.py"):
        imports += "from codebook import LABELS\n"
        unknown_expr = "LABELS.get('unknown')"
        accept_expr = "LABELS['accept']"
    solver = (
        '"""Implement decide(record)' + (" and decide_batch(records)" if spec["batch_quota"] else "") + ' from the source fragments."""\n\n'
        + imports + "\n"
        f"AUTHORIZED = {spec['doc_authorized_sources']!r}\n\n\n"
        "def decide(record):\n"
        "    if record.get(\"source\") not in AUTHORIZED:\n"
        f"        return {unknown_expr}\n"
        f"    return {accept_expr}  # intentionally incomplete baseline\n"
    )
    if spec["batch_quota"]:
        solver += "\n\ndef decide_batch(records):\n    return [decide(record) for record in records]  # incomplete: ignores the batch quota\n"
    (path / "solver.py").write_text(solver, encoding="utf-8")
    (path / "normalize.py").write_text(
        '"""Measurement normalization (incomplete)."""\n\n'
        f"PRIMARY_UNIT = {spec['unit_primary']!r}\n\n\n"
        "def to_primary(x, unit):\n"
        "    if unit == PRIMARY_UNIT:\n"
        "        return int(x)\n"
        "    return None  # incomplete: other recognized units are not converted yet\n",
        encoding="utf-8",
    )
    if "codebook.py" in spec["editable_files"]:
        old = spec["superseded_labels"]
        (path / "codebook.py").write_text(
            '"""Output codebook (incomplete / partly stale)."""\n\n'
            "LABELS = {\n"
            f"    \"accept\": {labels['accept']!r},\n"
            f"    \"review\": {labels['review']!r},\n"
            f"    \"reject\": {old['reject']!r},  # stale\n"
            "}\n",
            encoding="utf-8",
        )
    test_lines = ["import solver", "", ""]
    for i, item in enumerate(examples):
        test_lines += [f"def test_public_example_{i + 1}():",
                       f"    assert solver.decide({json.dumps(item['record'], sort_keys=True)}) == {item['expected']!r}", "", ""]
    (path / "tests" / "test_public.py").write_text("\n".join(test_lines).rstrip() + "\n", encoding="utf-8")
    (path / "README.md").write_text(
        "# Fresh generated source-composition repair task (E70-GC2)\n\n"
        f"Editable files: {', '.join(f'`{f}`' for f in spec['editable_files'])}. Implement `solver.decide(record)`"
        + (", `solver.decide_batch(records)`" if spec["batch_quota"] else "")
        + " and the `normalize.to_primary(x, unit)` contract"
        + (" and complete `codebook.LABELS`" if "codebook.py" in spec["editable_files"] else "")
        + " using all source fragments in force under `sources/` (read `04_precedence.md` and `06_erratum.md` first; "
        "`05_superseded_revision.md` is archival and not in force). All semantic constants and output tokens were generated after protocol freeze. "
        "The hidden evaluator contains additional records, counterfactual variants and contract checks that are not present in this workspace. "
        "Do not use network retrieval. Return one unified diff touching only the editable files.\n\n"
        "## Public examples (also in `tests/test_public.py`)\n\n"
        + "\n".join(f"- `{json.dumps(item['record'], sort_keys=True)}` -> `{item['expected']}`" for item in examples)
        + "\n",
        encoding="utf-8",
    )


def reference_solution(spec: dict[str, Any]) -> dict[str, str]:
    """Generator self-check only (never written into a public workspace)."""
    labels = spec["labels"]
    files: dict[str, str] = {}
    files["normalize.py"] = (
        f"PRIMARY_UNIT = {spec['unit_primary']!r}\n\n\ndef to_primary(x, unit):\n"
        f"    if unit == PRIMARY_UNIT:\n        return int(x)\n"
        f"    if unit == {spec['unit_scaled']!r}" + (f" or unit == {spec['unit_alias']!r}" if spec["unit_alias"] else "") + ":\n"
        f"        return int(x) * {spec['scale_factor']}\n"
        + (f"    if unit == {spec['unit_offset']!r}:\n        return int(x) * {spec['offset_scale']} + ({spec['offset_shift']})\n" if spec["unit_offset"] else "")
        + "    return None\n"
    )
    if "codebook.py" in spec["editable_files"]:
        files["codebook.py"] = "LABELS = " + json.dumps(labels, sort_keys=True, indent=4) + "\n"
        lab = {k: f"LABELS[{k!r}]" for k in labels}
    else:
        lab = {k: repr(v) for k, v in labels.items()}
    body = (
        "from normalize import to_primary\n" + ("from codebook import LABELS\n" if "codebook.py" in spec["editable_files"] else "") + "\n"
        f"ALLOWED = {spec['allowed_sources']!r}\n\n\ndef decide(record):\n"
        f"    source = record.get('source')\n    if source not in ALLOWED:\n        return {lab['unknown']}\n"
        f"    x = to_primary(int(record['x']), record.get('unit'))\n    if x is None:\n        return {lab['unknown']}\n"
        f"    y = int(record['y'])\n    score = ({spec['a']} * x + {spec['b']} * y + {spec['c']}) % {spec['modulus']}\n"
        f"    if bool(record.get('counterexample')):\n        return {lab['review']}\n"
        + (f"    if score in ({spec['low'] + 1}, {spec['low'] + 2}):\n        return {lab['reject']} if source == {spec['primary_authority']!r} else {lab['review']}\n" if spec["ambiguity_band"] else "")
        + (f"    if score == {spec['high'] - 1} and y % 2 == 0:\n        return {lab['accept']}\n" if spec["tiebreak"] else "")
        + f"    if score >= {spec['high']}:\n        return {lab['accept']}\n    if score <= {spec['low']}:\n        return {lab['reject']}\n    return {lab['review']}\n"
    )
    if spec["batch_quota"]:
        body += (
            "\n\ndef decide_batch(records):\n    counts = {}\n    out = []\n    for record in records:\n        label = decide(record)\n"
            f"        if label == {lab['accept']}:\n            counts[record.get('source')] = counts.get(record.get('source'), 0) + 1\n"
            f"            if counts[record.get('source')] > {spec['batch_quota']}:\n                label = {lab['review']}\n"
            "        out.append(label)\n    return out\n"
        )
    files["solver.py"] = body
    return files


def rooted_patch(workspace: Path, files: dict[str, str]) -> str:
    """Unified diff (a/b rooted, exact hunk counts) replacing the given files."""
    chunks: list[str] = []
    for name in sorted(files):
        before = (workspace / name).read_text(encoding="utf-8") if (workspace / name).exists() else ""
        body = "".join(difflib.unified_diff(before.splitlines(keepends=True), files[name].splitlines(keepends=True),
                                            fromfile=f"a/{name}", tofile=f"b/{name}"))
        chunks.append(f"diff --git a/{name} b/{name}\n" + body)
    return "".join(chunks)


def derive_run_seed(seed: int, nonce: str) -> int:
    return int(hashlib.sha256(f"{seed}:{nonce}".encode("utf-8")).hexdigest()[:16], 16)


def generate(design: dict[str, Any], workdir: Path, *, level: str, count: int, seed: int, reps: int,
             arms: list[str], nonce: str | None, force: bool, split: str) -> dict[str, Any]:
    if level not in LADDER:
        raise SuiteError(f"unknown ladder level {level}")
    if workdir.exists():
        if not force:
            raise SuiteError(f"workdir exists; pass --force to replace it: {workdir}")
        shutil.rmtree(workdir)
    nonce = nonce or os.urandom(16).hex()
    run_seed = derive_run_seed(seed, nonce)
    rng = random.Random(run_seed)
    public_root, private_root, requests_root = workdir / "public", workdir / "private", workdir / "requests"
    task_rows: list[dict[str, Any]] = []
    self_check: list[dict[str, Any]] = []
    for index in range(count):
        task_id = f"gc2-{index + 1:03d}"
        task_rng = random.Random(rng.getrandbits(64))
        spec = generate_spec(task_rng, index, level)
        examples = find_public_examples(task_rng, spec)
        checks = hidden_checks(task_rng, spec, examples)
        public_path = public_root / task_id
        render_public_workspace(public_path, spec, examples)
        # Generator self-check: reference passes every hidden check, the baseline does not.
        with tempfile.TemporaryDirectory(prefix="gc2-selfcheck-") as temp:
            ref_ws = Path(temp) / "ref"
            shutil.copytree(public_path, ref_ws)
            ok, err = apply_patch(ref_ws, rooted_patch(ref_ws, reference_solution(spec)), spec["editable_files"])
            if not ok:
                raise SuiteError(f"{task_id}: reference patch does not apply: {err}")
            ref_score = score_workspace(ref_ws, checks)
            base_score = score_workspace(public_path, checks)
        if not ref_score["hidden_oracle_success"]:
            raise SuiteError(f"{task_id}: reference solution fails hidden checks: {ref_score}")
        if base_score["hidden_oracle_success"]:
            raise SuiteError(f"{task_id}: baseline already passes hidden checks")
        self_check.append({"task_id": task_id, "reference_accuracy": ref_score["hidden_accuracy"],
                           "baseline_accuracy": base_score["hidden_accuracy"], "check_count": len(checks)})
        write_json(private_root / f"{task_id}.json", {
            "schema_version": "orion.v2.generated-composition-gc2-private.v1",
            "task_id": task_id, "level": level, "spec": spec, "checks": checks,
        })
        manifest_rows = [{"path": f.relative_to(public_path).as_posix(), "sha256": sha256_bytes(f.read_bytes()), "bytes": f.stat().st_size}
                         for f in sorted(public_path.rglob("*")) if f.is_file()]
        baseline_example = next((it for it in examples if it["expected"] != spec["labels"]["accept"]), examples[0])
        task_row = {
            "task_id": task_id,
            "solver_workspace": str(public_path.resolve()),
            "adapter": "generated_composition_gc2_offceiling",
            "benchmark_id": "generated_composition_gc2_offceiling",
            "ladder_level": level,
            "editable_files": spec["editable_files"],
            "interface_contract": {
                "artifact": "single unified diff rooted at workspace-relative paths, touching only editable_files",
                "required_symbols": ["solver.decide", "normalize.to_primary"]
                + (["codebook.LABELS"] if "codebook.py" in spec["editable_files"] else [])
                + (["solver.decide_batch"] if spec["batch_quota"] else []),
            },
            "public_manifest": manifest_rows,
            "baseline_observation": {
                "current_implementation_returns": spec["labels"]["accept"],
                "public_record": baseline_example["record"],
                "expected_from_public_sources": baseline_example["expected"],
                "public_tests": "tests/test_public.py fails on the incomplete baseline",
                "status": "KNOWN_INCORRECT_IMPLEMENTATION",
            },
        }
        task_rows.append(task_row)
        for arm in arms:
            for rep in range(1, reps + 1):
                write_json(requests_root / arm / f"{task_id}-r{rep}.json", {
                    "schema_version": "orion.v2.agent-request.v1",
                    "task_id": task_id, "arm_id": arm, "rep": rep, "task": task_row,
                    "resource_contract": design.get("resource_contract", {"default_cpu_cores": 2, "default_memory_gb": 4}),
                    "scientific_truth_authorized": False, "field_status_authorized": False, "publication_readiness_authorized": False,
                })
    write_json(private_root / "NONCE.json", {"nonce": nonce, "seed": seed, "run_seed": run_seed})
    freeze = {
        "schema_version": "orion.v2.generated-composition-gc2-freeze.v1",
        "suite_id": design["suite_id"], "split": split, "ladder_level": level,
        "design_sha256": sha256_bytes(DESIGN_PATH.read_bytes()) if DESIGN_PATH.exists() else None,
        "seed": seed, "nonce_sha256": sha256_text(nonce), "run_seed_committed": False,
        "task_count": count, "reps": reps, "arms": arms, "tasks": task_rows,
        "generator_self_check": self_check,
        "private_gold_mounted_to_solver": False,
        "authority": design.get("authority", {}),
    }
    write_json(workdir / "FROZEN_TASKS.json", freeze)
    return freeze


# ------------------------------------------------------------------ evaluation
def extract_patch(response: dict[str, Any]) -> str | None:
    artifact = response.get("proposed_patch_or_artifact")
    if isinstance(artifact, dict) and artifact.get("type") == "unified_diff" and isinstance(artifact.get("content"), str):
        return artifact["content"]
    if isinstance(artifact, str):
        return artifact
    return None


def patch_paths(patch: str) -> tuple[str, ...]:
    paths: list[str] = []
    for match in DIFF_PATH_RE.finditer(patch):
        if match.group("a") != match.group("b"):
            raise SuiteError("rename patch is outside GC2 scope")
        paths.append(match.group("a"))
    return tuple(paths)


def apply_patch(workspace: Path, patch: str, editable: list[str]) -> tuple[bool, str]:
    try:
        paths = patch_paths(patch)
    except SuiteError as exc:
        return False, str(exc)
    if not paths or any(path not in editable for path in paths):
        return False, f"patch paths must be within editable files {editable}; observed={paths}"
    for command in (["git", "apply", "--check", "--whitespace=nowarn", "-"], ["git", "apply", "--whitespace=nowarn", "-"]):
        completed = subprocess.run(command, cwd=str(workspace), input=patch, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if completed.returncode != 0:
            return False, completed.stderr[-2000:]
    return True, ""


RUNNER_CODE = r'''
import contextlib, importlib, io, json, sys
payload = json.load(sys.stdin)
sys.path.insert(0, payload["workspace"])
out = []
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    try:
        solver = importlib.import_module("solver")
        normalize = importlib.import_module("normalize")
    except BaseException as exc:  # import failure fails every check
        print(json.dumps({"import_error": repr(exc)}))
        raise SystemExit(0)
    try:
        codebook = importlib.import_module("codebook")
    except BaseException:
        codebook = None
    for check in payload["checks"]:
        try:
            kind = check["kind"]
            if kind == "decide":
                value = solver.decide(dict(check["record"]))
            elif kind == "normalize":
                value = normalize.to_primary(check["x"], check["unit"])
            elif kind == "codebook":
                value = None if codebook is None else getattr(codebook, "LABELS", {}).get(check["key"])
            elif kind == "batch":
                value = solver.decide_batch([dict(r) for r in check["records"]])
            else:
                value = "UNKNOWN_CHECK_KIND"
            out.append({"value": value})
        except BaseException as exc:
            out.append({"error": repr(exc)})
print(json.dumps(out, default=str))
'''


def _match(kind: str, value: Any, expected: Any) -> bool:
    if kind == "normalize":
        if expected is None:
            return value is None
        return isinstance(value, int) and not isinstance(value, bool) and value == expected
    if kind == "batch":
        return isinstance(value, list) and [str(v) for v in value] == list(expected)
    return isinstance(value, str) and value == expected


def score_workspace(workspace: Path, checks: list[dict[str, Any]]) -> dict[str, Any]:
    environment = {"PATH": os.environ.get("PATH", ""), "PYTHONNOUSERSITE": "1", "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0"}
    try:
        completed = subprocess.run([sys.executable, "-c", RUNNER_CODE], input=json.dumps({"workspace": str(workspace), "checks": checks}),
                                   text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90, check=False,
                                   cwd=str(workspace), env=environment)
    except subprocess.TimeoutExpired:
        return {"runtime_success": False, "hidden_accuracy": 0.0, "hidden_oracle_success": False, "family_accuracy": {}, "stderr_tail": "timeout"}
    try:
        observed = json.loads(completed.stdout) if completed.returncode == 0 else None
    except json.JSONDecodeError:
        observed = None
    if observed is None or (isinstance(observed, dict) and "import_error" in observed) or not isinstance(observed, list) or len(observed) != len(checks):
        detail = observed.get("import_error") if isinstance(observed, dict) else completed.stderr[-1000:]
        return {"runtime_success": False, "hidden_accuracy": 0.0, "hidden_oracle_success": False, "family_accuracy": {}, "stderr_tail": str(detail)}
    per_family: dict[str, list[bool]] = {}
    correct = 0
    for check, result in zip(checks, observed, strict=True):
        ok = "error" not in result and _match(check["kind"], result.get("value"), check["expected"])
        correct += int(ok)
        per_family.setdefault(str(check["family"]).split(":")[0], []).append(ok)
    return {
        "runtime_success": True,
        "hidden_accuracy": correct / len(checks) if checks else 0.0,
        "hidden_oracle_success": bool(checks) and correct == len(checks),
        "correct": correct, "total": len(checks),
        "family_accuracy": {family: sum(v) / len(v) for family, v in sorted(per_family.items())},
        "stderr_tail": "",
    }


def evaluate_one(workdir: Path, arm: str, task_id: str, rep: int) -> dict[str, Any]:
    response_path = workdir / "responses" / arm / f"{task_id}-r{rep}.json"
    private = read_json(workdir / "private" / f"{task_id}.json")
    public = workdir / "public" / task_id
    editable = list(private["spec"]["editable_files"])
    base = {"schema_version": "orion.v2.gc2-evaluation.v1", "task_id": task_id, "arm_id": arm, "rep": rep,
            "ladder_level": private["level"], "count_robust_hidden_oracle_success": False, "raw_hidden_oracle_success": False}
    if not response_path.exists():
        return base | {"status": "CANNOT_CHECK_MISSING_RESPONSE"}
    response = read_json(response_path)
    patch = extract_patch(response)
    if patch is None:
        return base | {"status": "NO_EXECUTABLE_PATCH", "agent_status": response.get("status")}

    def lane(name: str, text: str) -> tuple[bool, str, dict[str, Any]]:
        target = workdir / "evaluation" / name / arm / f"{task_id}-r{rep}"
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(public, target)
        applied, error = apply_patch(target, text, editable)
        score = {"runtime_success": False, "hidden_accuracy": 0.0, "hidden_oracle_success": False, "family_accuracy": {}}
        if applied:
            score = score_workspace(target, private["checks"])
        return applied, error, score

    raw_apply, raw_error, raw_score = lane("raw", patch)
    audit = audit_and_canonicalize_unified_diff(patch)
    cr_apply, cr_error, cr_score = False, "INVALID_NOT_CANONICALIZABLE", {"hidden_accuracy": 0.0, "hidden_oracle_success": False, "family_accuracy": {}}
    if audit.valid_or_canonicalizable and audit.canonical_diff is not None:
        cr_apply, cr_error, cr_score = lane("count_robust", audit.canonical_diff)
    resource = response.get("resource_receipt") if isinstance(response.get("resource_receipt"), dict) else {}
    return base | {
        "status": "EVALUATED",
        "agent_status": response.get("status"),
        "raw_patch_sha256": sha256_text(patch),
        "canonical_patch_sha256": sha256_text(audit.canonical_diff) if audit.canonical_diff else None,
        "patch_paths": list(patch_paths(patch)) if DIFF_PATH_RE.search(patch) else [],
        "syntax_audit_status": ("VALID_UNCHANGED" if audit.valid_or_canonicalizable and not audit.changed
                                else "VALID_AFTER_SYNTAX_ONLY_CANONICALIZATION" if audit.valid_or_canonicalizable
                                else "INVALID_NOT_CANONICALIZABLE"),
        "syntax_audit_reasons": list(audit.reasons),
        "count_robust_patch_apply_success": cr_apply,
        "count_robust_patch_apply_error": cr_error,
        "count_robust_hidden_accuracy": cr_score.get("hidden_accuracy", 0.0),
        "count_robust_hidden_oracle_success": bool(cr_apply and cr_score.get("hidden_oracle_success")),
        "count_robust_family_accuracy": cr_score.get("family_accuracy", {}),
        "raw_patch_apply_success": raw_apply,
        "raw_patch_apply_error": raw_error,
        "raw_hidden_accuracy": raw_score.get("hidden_accuracy", 0.0),
        "raw_hidden_oracle_success": bool(raw_apply and raw_score.get("hidden_oracle_success")),
        "model_tokens": resource.get("total_tokens_reported_by_cli"),
        "model_wall_time_seconds": resource.get("wall_time_seconds"),
        "patch_size_bytes": len(patch.encode("utf-8")),
        "gold_or_private_spec_visible_to_solver": False,
        "scientific_truth_authorized": False,
        "publication_readiness_authorized": False,
    }


def evaluate(workdir: Path, *, arms: list[str]) -> list[dict[str, Any]]:
    frozen = read_json(workdir / "FROZEN_TASKS.json")
    tasks = [str(item["task_id"]) for item in frozen["tasks"]]
    results: list[dict[str, Any]] = []
    for arm in arms:
        for task_id in tasks:
            for rep in range(1, int(frozen["reps"]) + 1):
                result = evaluate_one(workdir, arm, task_id, rep)
                write_json(workdir / "evaluations" / arm / f"{task_id}-r{rep}.json", result)
                results.append(result)
    write_json(workdir / "EVALUATION_ROLLUP.json", {"schema_version": "orion.v2.gc2-evaluation-rollup.v1", "records": results})
    return results


# -------------------------------------------------------------------- analysis
def exact_two_sided(left: int, right: int) -> float | None:
    n = left + right
    if n == 0:
        return None
    tail = min(left, right)
    return min(1.0, 2 * sum(math.comb(n, k) for k in range(tail + 1)) / 2 ** n)


def holm(ps: list[float | None]) -> list[float | None]:
    idx = sorted([i for i, p in enumerate(ps) if p is not None], key=lambda i: ps[i])
    out: list[float | None] = [None] * len(ps)
    running = 0.0
    for rank, i in enumerate(idx):
        running = max(running, min(1.0, (len(idx) - rank) * ps[i]))
        out[i] = running
    return out


def wilson(k: int, n: int, z: float = 1.959964) -> list[float | None]:
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [max(0.0, c - h), min(1.0, c + h)]


def paired_bootstrap(values: list[float], *, seed: int, reps: int = 10000) -> dict[str, Any]:
    if not values:
        return {"estimate": None, "ci95": [None, None], "pair_count": 0}
    rng = random.Random(seed)
    draws = sorted(sum(values[rng.randrange(len(values))] for _ in values) / len(values) for _ in range(reps))
    return {"estimate": sum(values) / len(values), "ci95": [draws[int(0.025 * (reps - 1))], draws[int(0.975 * (reps - 1))]],
            "pair_count": len(values), "bootstrap_repetitions": reps, "seed": seed}


def task_level(rows: dict[tuple[str, int], dict[str, Any]], task_id: str, reps: int, endpoint: str, rule: str) -> bool:
    values = [bool(rows.get((task_id, r), {}).get(endpoint)) for r in range(1, reps + 1)]
    if rule == "majority":
        return sum(values) * 2 > len(values)
    if rule == "all":
        return all(values)
    return any(values)


def analyze(workdir: Path, *, arms: list[str], seed: int, design: dict[str, Any]) -> dict[str, Any]:
    frozen = read_json(workdir / "FROZEN_TASKS.json")
    tasks = [str(item["task_id"]) for item in frozen["tasks"]]
    reps = int(frozen["reps"])
    by_arm: dict[str, dict[tuple[str, int], dict[str, Any]]] = {}
    for arm in arms:
        rows: dict[tuple[str, int], dict[str, Any]] = {}
        for task_id in tasks:
            for rep in range(1, reps + 1):
                path = workdir / "evaluations" / arm / f"{task_id}-r{rep}.json"
                if path.exists():
                    rows[(task_id, rep)] = read_json(path)
        by_arm[arm] = rows
    endpoints = {"count_robust_hidden_oracle_success": "PRIMARY", "raw_hidden_oracle_success": "SECONDARY_INTERFACE_FIDELITY",
                 "count_robust_patch_apply_success": "SECONDARY", "raw_patch_apply_success": "SECONDARY"}
    summaries: dict[str, Any] = {}
    for arm, rows in by_arm.items():
        cell = len(rows)
        summaries[arm] = {"cells_evaluated": cell, "cells_expected": len(tasks) * reps,
                          "missing_or_unscorable": sum(r.get("status") != "EVALUATED" for r in rows.values())}
        for ep in endpoints:
            k = sum(bool(r.get(ep)) for r in rows.values())
            summaries[arm][ep] = {"rep_level_count": k, "rep_level_rate": k / cell if cell else None, "rep_level_wilson95": wilson(k, cell),
                                  "task_level_majority_count": sum(task_level(rows, t, reps, ep, "majority") for t in tasks),
                                  "task_level_all_reps_count": sum(task_level(rows, t, reps, ep, "all") for t in tasks),
                                  "task_level_any_rep_count": sum(task_level(rows, t, reps, ep, "any") for t in tasks)}
        summaries[arm]["mean_count_robust_hidden_accuracy"] = (sum(float(r.get("count_robust_hidden_accuracy", 0.0)) for r in rows.values()) / cell) if cell else None
        summaries[arm]["syntax_canonicalization_changed_cells"] = sum(r.get("syntax_audit_status") == "VALID_AFTER_SYNTAX_ONLY_CANONICALIZATION" for r in rows.values())
        summaries[arm]["invalid_not_canonicalizable_cells"] = sum(r.get("syntax_audit_status") == "INVALID_NOT_CANONICALIZABLE" for r in rows.values())
        summaries[arm]["model_tokens_total"] = sum(int(r["model_tokens"]) for r in rows.values() if isinstance(r.get("model_tokens"), int))
        summaries[arm]["model_wall_time_seconds_total"] = round(sum(float(r["model_wall_time_seconds"]) for r in rows.values() if isinstance(r.get("model_wall_time_seconds"), (int, float))), 1)
        fam: dict[str, list[float]] = {}
        for r in rows.values():
            for f, v in (r.get("count_robust_family_accuracy") or {}).items():
                fam.setdefault(f, []).append(float(v))
        summaries[arm]["count_robust_family_mean_accuracy"] = {f: sum(v) / len(v) for f, v in sorted(fam.items())}

    contrasts: dict[str, list[dict[str, Any]]] = {}
    alpha = float(design.get("analysis", {}).get("alpha", 0.05))
    for ep in endpoints:
        rows_out: list[dict[str, Any]] = []
        for control in CONTROL_ORDER:
            if F2 not in by_arm or control not in by_arm:
                continue
            l = r = both = 0
            diffs: list[float] = []
            for t in tasks:
                a = task_level(by_arm[F2], t, reps, ep, "majority")
                b = task_level(by_arm[control], t, reps, ep, "majority")
                l += int(a and not b)
                r += int(b and not a)
                both += int(a and b)
                diffs.append(float(a) - float(b))
            rows_out.append({"left_arm": F2, "right_arm": control, "unit": "task (majority of reps)", "both_true": both,
                             "both_false": len(tasks) - both - l - r, "left_only": l, "right_only": r,
                             "risk_difference": paired_bootstrap(diffs, seed=seed), "exact_p": exact_two_sided(l, r)})
        for row, hp in zip(rows_out, holm([x["exact_p"] for x in rows_out])):
            row["holm_p"] = hp
        # Fixed-sequence gatekeeping (registered): G1 F2 vs F0, then G2 F2 vs SIMPLE, then G3 vs REFLECTION.
        gate_open = True
        for row in rows_out:
            p = row["exact_p"]
            sig = gate_open and p is not None and p < alpha
            row["fixed_sequence_tested"] = gate_open
            row["fixed_sequence_reject"] = bool(sig)
            row["direction"] = "F2_BETTER" if row["left_only"] > row["right_only"] else "CONTROL_BETTER" if row["right_only"] > row["left_only"] else "TIE"
            gate_open = gate_open and bool(sig) and row["direction"] == "F2_BETTER"
        # Descriptive parent-sufficiency contrast (outside the family, uncorrected).
        if "F0_PARENT_FEDERATION" in by_arm and "SIMPLE_DIRECT" in by_arm:
            l = sum(task_level(by_arm["F0_PARENT_FEDERATION"], t, reps, ep, "majority") and not task_level(by_arm["SIMPLE_DIRECT"], t, reps, ep, "majority") for t in tasks)
            r = sum(task_level(by_arm["SIMPLE_DIRECT"], t, reps, ep, "majority") and not task_level(by_arm["F0_PARENT_FEDERATION"], t, reps, ep, "majority") for t in tasks)
            rows_out.append({"left_arm": "F0_PARENT_FEDERATION", "right_arm": "SIMPLE_DIRECT", "descriptive_outside_family": True,
                             "left_only": l, "right_only": r, "exact_p_uncorrected": exact_two_sided(l, r)})
        contrasts[ep] = rows_out

    # Post-outcome solution-similarity diagnostic (Phase 5; diagnostic only, no endpoint role).
    similarity: dict[str, float | None] = {}
    if len(arms) >= 2:
        vals: dict[str, list[float]] = {}
        for t in tasks:
            texts = {a: by_arm[a].get((t, 1), {}) for a in arms}
            for i, a in enumerate(arms):
                for b in arms[i + 1:]:
                    pa, pb = texts[a].get("canonical_patch_sha256"), texts[b].get("canonical_patch_sha256")
                    if pa and pb:
                        vals.setdefault(f"{a}|{b}", []).append(1.0 if pa == pb else 0.0)
        similarity = {k: sum(v) / len(v) for k, v in vals.items()}

    routing = route(summaries, contrasts, frozen, design, alpha)
    result = {
        "schema_version": "orion.v2.gc2-analysis.v1",
        "suite_id": frozen["suite_id"], "split": frozen.get("split"), "ladder_level": frozen.get("ladder_level"),
        "status": "SECONDARY_ANTI_COPY_COMPOSITION_EVIDENCE_ONLY",
        "primary_endpoint": "count_robust_hidden_oracle_success",
        "analysis_unit": f"frozen task ({len(tasks)}), majority over {reps} nested reps; rep-level rates descriptive",
        "arm_summaries": summaries, "contrasts": contrasts,
        "identical_canonical_patch_rate_rep1_diagnostic_only": similarity,
        "routing": routing,
        "authority": {"grants_active_solving_proof": False, "grants_field_status": False, "grants_submission_readiness": False},
    }
    write_json(workdir / "aggregate" / "analysis.json", result)
    lines = [f"# E70-GC2 execution summary ({frozen.get('split')}, level {frozen.get('ladder_level')})", "",
             "Secondary generated counterfactual/source-composition evidence only. Primary endpoint = count-robust native success.", "",
             "| Arm | Count-robust (rep-level) | Count-robust task-majority | Raw header-exact (rep-level) | Canonicalization changed | Invalid |",
             "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for arm in arms:
        s = summaries[arm]
        cr, raw = s["count_robust_hidden_oracle_success"], s["raw_hidden_oracle_success"]
        lines.append(f"| {arm} | {cr['rep_level_count']}/{s['cells_evaluated']} | {cr['task_level_majority_count']}/{len(tasks)} | "
                     f"{raw['rep_level_count']}/{s['cells_evaluated']} | {s['syntax_canonicalization_changed_cells']} | {s['invalid_not_canonicalizable_cells']} |")
    lines += ["", f"Routing: `{routing['route']}` — {routing['reason']}", "",
              "This suite cannot replace E30/E40/E50 and does not prove absence of training-data influence."]
    (workdir / "EXECUTION_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


def route(summaries: dict[str, Any], contrasts: dict[str, Any], frozen: dict[str, Any], design: dict[str, Any], alpha: float) -> dict[str, Any]:
    ep = "count_robust_hidden_oracle_success"
    gates = design.get("gates", {})
    ceiling = float(gates.get("G0", {}).get("protected_ceiling_rate", 0.95))
    floor = float(gates.get("G0", {}).get("protected_floor_rate", 0.05))
    task_count = len(frozen["tasks"])
    incomplete = [a for a, s in summaries.items() if s["cells_evaluated"] < s["cells_expected"] or s["missing_or_unscorable"]]
    if incomplete:
        return {"route": "G0_FAIL_INCOMPLETE_CELLS", "reason": f"arms with missing/unscorable cells: {incomplete}", "gate": "G0"}
    simple = summaries.get("SIMPLE_DIRECT", {}).get(ep, {})
    simple_rate = simple.get("rep_level_rate")
    if simple_rate is not None and simple_rate >= ceiling:
        return {"route": "SUITE_STILL_SATURATED", "reason": f"SIMPLE_DIRECT count-robust rate {simple_rate:.3f} >= {ceiling}", "gate": "G0"}
    if simple_rate is not None and simple_rate <= floor:
        return {"route": "SUITE_AT_FLOOR", "reason": f"SIMPLE_DIRECT count-robust rate {simple_rate:.3f} <= {floor}", "gate": "G0"}
    fam = [r for r in contrasts.get(ep, []) if not r.get("descriptive_outside_family")]
    if len(fam) < 2:
        return {"route": "G0_FAIL_MISSING_ARMS", "reason": "registered family incomplete", "gate": "G0"}
    g1, g2 = fam[0], fam[1]
    if g1["fixed_sequence_reject"] and g1["direction"] == "F2_BETTER":
        if g2["fixed_sequence_reject"] and g2["direction"] == "F2_BETTER":
            return {"route": "POSITIVE_F2_BEATS_PARENT_AND_SIMPLE", "reason": f"G1 p={g1['exact_p']:.4f}, G2 p={g2['exact_p']:.4f} (alpha {alpha}, fixed sequence)", "gate": "G2"}
        return {"route": "PARTIAL_F2_BEATS_PARENT_NOT_SIMPLE", "reason": f"G1 rejected (p={g1['exact_p']:.4f}); G2 not rejected", "gate": "G2"}
    if g1["exact_p"] is not None and g1["exact_p"] < alpha and g1["direction"] == "CONTROL_BETTER":
        return {"route": "NEGATIVE_COMPONENT_HARM_F2_BELOW_PARENT", "reason": f"F0 beats F2, p={g1['exact_p']:.4f}", "gate": "G1"}
    desc = next((r for r in contrasts.get(ep, []) if r.get("descriptive_outside_family")), None)
    if desc and desc["exact_p_uncorrected"] is not None and desc["exact_p_uncorrected"] < alpha and desc["left_only"] > desc["right_only"]:
        return {"route": "NEGATIVE_PARENT_SUFFICIENT", "reason": "F0 not distinguishable from F2 (G1 not rejected) while F0 beats SIMPLE descriptively", "gate": "G1"}
    return {"route": "NEGATIVE_NO_DETECTABLE_F2_GAIN_AT_MDE", "reason": f"G1 not rejected (p={g1['exact_p']}) on {task_count} powered tasks; no direction certified", "gate": "G1"}


# ----------------------------------------------------------------------- power
def power_analysis(*, seed: int, rd: float, alpha: float, target_power: float, reps: int, control_rate: float,
                   concentration: float, n_grid: list[int], sims: int) -> dict[str, Any]:
    """Simulation-based power for the task-level exact discordant test with nested reps.

    Task latent success p_t ~ Beta(mean=control_rate, concentration); the treated arm shifts the
    logit by delta chosen so the marginal rep-level risk difference equals ``rd``; each arm draws
    ``reps`` Bernoulli reps per task; task outcome = majority of reps; test = exact two-sided
    sign test on discordant tasks.  Analytic McNemar n under rep-level independence is reported
    as a cross-check.
    """
    rng = random.Random(seed)
    a = control_rate * concentration
    b = (1 - control_rate) * concentration

    def expit(v: float) -> float:
        return 1 / (1 + math.exp(-v))

    def logit(v: float) -> float:
        return math.log(v / (1 - v))

    # Solve delta so that E[expit(logit(p)+delta)] - control_rate = rd (Monte Carlo, fixed draws).
    draws = [min(0.995, max(0.005, rng.betavariate(a, b))) for _ in range(20000)]
    lo, hi = 0.0, 5.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if sum(expit(logit(p) + mid) for p in draws) / len(draws) - control_rate < rd:
            lo = mid
        else:
            hi = mid
    delta = (lo + hi) / 2

    def majority(p: float) -> bool:
        return sum(rng.random() < p for _ in range(reps)) * 2 > reps

    power_by_n: dict[int, dict[str, float]] = {}
    chosen: int | None = None
    for n in n_grid:
        rejects = 0
        discordant_total = 0
        for _ in range(sims):
            l = r = 0
            for _ in range(n):
                p = min(0.995, max(0.005, rng.betavariate(a, b)))
                c = majority(p)
                t = majority(expit(logit(p) + delta))
                l += int(t and not c)
                r += int(c and not t)
            discordant_total += l + r
            pv = exact_two_sided(l, r)
            rejects += int(pv is not None and pv < alpha and l > r)
        power_by_n[n] = {"power": rejects / sims, "mean_discordant_tasks": discordant_total / sims}
        if chosen is None and rejects / sims >= target_power:
            chosen = n
    z_a = 1.959964 if abs(alpha - 0.05) < 1e-9 else 2.394 if abs(alpha - 0.05 / 3) < 1e-6 else 1.959964
    z_b = 0.841621
    psi = control_rate * (1 - (control_rate + rd)) + (control_rate + rd) * (1 - control_rate)
    n_mcnemar = math.ceil((z_a * math.sqrt(psi) + z_b * math.sqrt(psi - rd * rd)) ** 2 / (rd * rd))
    return {"method": "simulation (task-level exact sign test, majority over nested reps, Beta task heterogeneity)",
            "seed": seed, "risk_difference_mde": rd, "alpha_two_sided": alpha, "target_power": target_power, "reps_per_task": reps,
            "assumed_control_rate": control_rate, "beta_concentration": concentration, "logit_shift_delta": delta,
            "simulations_per_n": sims, "power_by_n": power_by_n, "selected_n": chosen,
            "analytic_mcnemar_n_rep_level_independence_no_reps": n_mcnemar}


# ----------------------------------------------------------------- calibration
def blinded_dispatch(workdir: Path, arms: list[str], max_concurrency: int) -> None:
    command = [sys.executable, str(BLINDED_DISPATCHER), "--workdir", str(workdir), "--arms", ",".join(arms),
               "--max-concurrency", str(max_concurrency), "--runner-script", str(Path(__file__).resolve())]
    completed = subprocess.run(command, cwd=str(ROOT), check=False)
    if completed.returncode != 0:
        raise SuiteError(f"blinded dispatch failed with return code {completed.returncode}")


def calibrate(design: dict[str, Any], root: Path, *, levels: list[str], dev_tasks: int, dev_seed: int,
              max_concurrency: int, nonce: str | None, force: bool) -> dict[str, Any]:
    cal = design["calibration"]
    lo, hi = float(cal["window"][0]), float(cal["window"][1])
    arm = str(cal["arm"])
    receipt: dict[str, Any] = {"schema_version": "orion.v2.gc2-calibration-receipt.v1", "suite_id": design["suite_id"],
                               "split": "dev", "arm": arm, "dev_seed": dev_seed, "dev_tasks_per_level": dev_tasks,
                               "window": [lo, hi], "endpoint": "count_robust_hidden_oracle_success", "levels": [],
                               "selected_level": None, "decision": None}
    previous_rate: float | None = None
    for level in levels:
        workdir = root / level
        generate(design, workdir, level=level, count=dev_tasks, seed=dev_seed, reps=1, arms=[arm], nonce=nonce, force=force, split="dev")
        blinded_dispatch(workdir, [arm], max_concurrency)
        records = evaluate(workdir, arms=[arm])
        k = sum(bool(r.get("count_robust_hidden_oracle_success")) for r in records)
        raw_k = sum(bool(r.get("raw_hidden_oracle_success")) for r in records)
        n = len(records)
        rate = k / n if n else 0.0
        row = {"level": level, "title": LADDER[level]["title"], "tasks": n, "count_robust_success": k, "rate": rate,
               "wilson95": wilson(k, n), "raw_header_exact_success": raw_k,
               "unscorable": sum(r.get("status") != "EVALUATED" for r in records),
               "mean_count_robust_accuracy": sum(float(r.get("count_robust_hidden_accuracy", 0.0)) for r in records) / n if n else None,
               "in_window": lo <= rate <= hi}
        receipt["levels"].append(row)
        write_json(root / "CALIBRATION_RECEIPT.json", receipt)
        if row["unscorable"]:
            receipt["decision"] = "CALIBRATION_INVALID_UNSCORABLE_CELLS"
            break
        if row["in_window"]:
            receipt["selected_level"] = level
            receipt["decision"] = "WINDOW_HIT"
            break
        if rate < lo:
            receipt["decision"] = "LADDER_OVERSHOT_NO_WINDOW_HIT" if (previous_rate is not None and previous_rate > hi) else "SUITE_AT_FLOOR_AT_FIRST_RUNG"
            break
        previous_rate = rate
    if receipt["decision"] is None:
        receipt["decision"] = "SUITE_STILL_SATURATED"
    write_json(root / "CALIBRATION_RECEIPT.json", receipt)
    return receipt


# ------------------------------------------------------------------------ main
def parse_arms(design: dict[str, Any], value: str | None) -> list[str]:
    if not value:
        return list(design["arms"])
    arms = [item.strip() for item in value.split(",") if item.strip()]
    unknown = [item for item in arms if item not in design["arms"]]
    if unknown:
        raise SuiteError(f"unknown arms: {unknown}")
    return arms


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("generate", "dispatch", "evaluate", "analyze", "calibrate", "power"))
    parser.add_argument("--design", type=Path, default=DESIGN_PATH)
    parser.add_argument("--workdir", type=Path, default=DEFAULT_WORKDIR)
    parser.add_argument("--arms")
    parser.add_argument("--level")
    parser.add_argument("--levels")
    parser.add_argument("--task-count", type=int)
    parser.add_argument("--reps", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--nonce", help="test/replay only; production runs draw a fresh secret nonce")
    parser.add_argument("--split", default="protected")
    parser.add_argument("--max-concurrency", type=int, default=2)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--overwrite-responses", action="store_true")
    parser.add_argument("--power-sims", type=int)
    args = parser.parse_args(argv)

    design = read_json(args.design)
    if design.get("status") != "PROSPECTIVE_SECONDARY_ANTI_COPY_PROTOCOL_NO_RESULTS":
        raise SuiteError("design is not in prospective no-results state")
    arms = parse_arms(design, args.arms)
    if args.max_concurrency <= 0:
        raise SuiteError("max-concurrency must be positive")

    if args.action == "power":
        pw = design["power"]
        result = power_analysis(seed=int(pw["seed"]), rd=float(pw["risk_difference_mde"]), alpha=float(pw["alpha_two_sided"]),
                                target_power=float(pw["target_power"]), reps=int(pw["reps_per_task"]),
                                control_rate=float(pw["assumed_control_rate"]), concentration=float(pw["beta_concentration"]),
                                n_grid=[int(x) for x in pw["n_grid"]], sims=args.power_sims or int(pw["simulations_per_n"]))
        write_json(args.workdir / "POWER_ANALYSIS.json", result)
        print(json.dumps({"selected_n": result["selected_n"], "power_by_n": result["power_by_n"]}, indent=1))
        return 0
    if args.action == "calibrate":
        cal = design["calibration"]
        levels = [x.strip() for x in (args.levels or ",".join(cal["ladder_order"])).split(",") if x.strip()]
        receipt = calibrate(design, args.workdir, levels=levels, dev_tasks=args.task_count or int(cal["dev_tasks_per_level"]),
                            dev_seed=args.seed if args.seed is not None else int(cal["dev_seed"]),
                            max_concurrency=args.max_concurrency, nonce=args.nonce, force=args.force)
        print(json.dumps({"decision": receipt["decision"], "selected_level": receipt["selected_level"],
                          "levels": [(r["level"], r["count_robust_success"], r["tasks"]) for r in receipt["levels"]]}))
        return 0
    seed = args.seed if args.seed is not None else int(design["protected"]["seed"])
    if args.action == "generate":
        level = args.level or design["protected"].get("ladder_level")
        if not level:
            raise SuiteError("no ladder level: pass --level or freeze protected.ladder_level after calibration")
        generate(design, args.workdir, level=level, count=args.task_count or int(design["protected"]["task_count"]), seed=seed,
                 reps=args.reps or int(design["protected"]["reps_per_task"]), arms=arms, nonce=args.nonce, force=args.force, split=args.split)
    elif args.action == "dispatch":
        sys.path.insert(0, str(ROOT / "scripts"))
        from run_orion_generated_composition_suite import dispatch as gc1_dispatch  # same executor, same receipts
        gc1_dispatch(args.workdir, arms=arms, max_concurrency=args.max_concurrency, overwrite=args.overwrite_responses)
    elif args.action == "evaluate":
        evaluate(args.workdir, arms=arms)
    elif args.action == "analyze":
        analyze(args.workdir, arms=arms, seed=seed, design=design)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (SuiteError, OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)

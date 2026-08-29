#!/usr/bin/env python3
"""Fresh generated formal-discovery suite for FM10-FM60 and FG10-FG80.

The generated lane is an exact/mechanically scored benchmark scaffold. Private
oracle answers are hash-committed, removed from disk for the entire child/model
dispatch, and restored only after all children terminate. It grants no scientific
truth, ORION/F2 superiority, or new-mathematical-theory status.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKDIR = ROOT / ".orion-formal-discovery-suite"
STUDIES = (
    "FM10", "FM20", "FM30", "FM40", "FM50", "FM60",
    "FG10", "FG20", "FG30", "FG40", "FG50", "FG60", "FG70", "FG80",
)
DEFAULT_ARMS = (
    "TARGET_ONLY_DIRECT",
    "STRONGEST_DOMAIN_FORMAL_PARENT",
    "F0_PARENT_FEDERATION",
    "F2_STATIC_NO_FORMAL_DISCOVERY",
    "F2_FORMAL_DISCOVERY_FULL",
)


class SuiteError(RuntimeError):
    pass


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def answer_shape(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: answer_shape(item) for key, item in value.items()}
    if isinstance(value, list):
        return ["array-item"]
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    return "string"


def token(rng: random.Random, prefix: str) -> str:
    return prefix + "_" + "".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ") for _ in range(6))


# ---------------------------------------------------------------------------
# FM: formal transfer mechanics
# ---------------------------------------------------------------------------

def gen_fm10(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    n = rng.randint(3, 5)
    types = [f"T{i}" for i in range(n)]
    donor = [token(rng, "D") for _ in range(n)]
    target = [token(rng, "Q") for _ in range(n)]
    perm = list(range(n))
    rng.shuffle(perm)
    mapping = {donor[i]: target[perm[i]] for i in range(n)}
    donor_nodes = [{"id": donor[i], "type": types[i]} for i in range(n)]
    target_nodes = [{"id": target[perm[i]], "type": types[i]} for i in range(n)]
    facts = [["R", donor[i], donor[i + 1]] for i in range(n - 1)]
    target_facts = [["R", mapping[a], mapping[b]] for _, a, b in facts]
    if rng.random() < 0.3:
        target_facts[-1] = ["R", target_facts[-1][2], target_facts[-1][1]]
        answer = {"status": "NO_VALID_MAPPING"}
    else:
        answer = {"status": "VALID_MAPPING", "node_map": mapping}
    public = {
        "study_id": "FM10",
        "donor": {"nodes": donor_nodes, "facts": facts},
        "target": {"nodes": target_nodes, "facts": target_facts},
        "task": "Return the unique type-preserving relation-preserving map, or NO_VALID_MAPPING.",
    }
    return public, answer


def gen_fm20(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    width = rng.randint(3, 6)
    base = [token(rng, "C") for _ in range(width)]
    varying = sorted(rng.sample(range(width), rng.randint(1, min(2, width))))
    examples: list[list[str]] = []
    for row_index in range(5):
        row = base.copy()
        for index in varying:
            # Include row identity so a varying coordinate is guaranteed to vary.
            row[index] = f"{token(rng, 'V')}_{row_index}"
        examples.append(row)
    pattern = [("?X" + str(i)) if i in varying else base[i] for i in range(width)]
    if rng.random() < 0.2:
        examples = [[f"{token(rng, 'V')}_{row}_{col}" for col in range(width)] for row in range(5)]
        pattern = ["?X" + str(i) for i in range(width)]
    public = {
        "study_id": "FM20",
        "terms": examples,
        "task": "Return the least-general coordinate pattern; constants remain exact and varying positions use ?X<index>.",
    }
    return public, {"pattern": pattern}


def closure(objects, attrs, incidence, seed_attrs):
    extent = [obj for obj in objects if all((obj, attr) in incidence for attr in seed_attrs)]
    intent = [attr for attr in attrs if all((obj, attr) in incidence for obj in extent)] if extent else list(attrs)
    extent2 = [obj for obj in objects if all((obj, attr) in incidence for attr in intent)]
    return sorted(extent2), sorted(intent)


def gen_fm30(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    objects = [token(rng, "O") for _ in range(5)]
    attrs = [token(rng, "A") for _ in range(5)]
    incidence = set()
    for obj in objects:
        incidence.update((obj, attr) for attr in rng.sample(attrs, rng.randint(1, 4)))
    seed = [rng.choice(attrs)]
    extent, intent = closure(objects, attrs, incidence, seed)
    public = {
        "study_id": "FM30",
        "objects": objects,
        "attributes": attrs,
        "incidence": [list(item) for item in sorted(incidence)],
        "seed_attributes": seed,
        "task": "Compute exact Formal Concept Analysis closure (extent and intent).",
    }
    return public, {"extent": extent, "intent": intent}


def gen_fm40(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    states = list(range(6))
    # The cycle action is transitive, so invariant scalar tables must be constant.
    transforms = [[(i, (i + 1) % 6) for i in states], [(i, 5 - i) for i in states]]
    features: dict[str, dict[str, int]] = {}
    invariant_ids: list[str] = []
    for index in range(5):
        feature_id = token(rng, "F")
        if index < 2:
            value = rng.randint(0, 9)
            table = {str(i): value for i in states}
            invariant_ids.append(feature_id)
        else:
            table = {str(i): rng.randint(0, 9) for i in states}
            if len(set(table.values())) == 1:
                table["0"] += 1
        features[feature_id] = table
    public = {
        "study_id": "FM40",
        "states": states,
        "transformations": transforms,
        "features": features,
        "task": "Return feature IDs invariant under every registered transformation.",
    }
    return public, {"invariant_feature_ids": sorted(invariant_ids)}


def walking_arrow_category(left: str, right: str, arrow: str) -> dict[str, Any]:
    identity_left = f"id_{left}"
    identity_right = f"id_{right}"
    return {
        "objects": [left, right],
        "morphisms": [identity_left, identity_right, arrow],
        "endpoints": {
            identity_left: [left, left],
            identity_right: [right, right],
            arrow: [left, right],
        },
        "identities": {left: identity_left, right: identity_right},
        # Complete composition table for all composable pairs in the walking-arrow category.
        "composition": [
            [identity_left, identity_left, identity_left],
            [identity_right, identity_right, identity_right],
            [identity_left, arrow, arrow],
            [arrow, identity_right, arrow],
        ],
    }


def gen_fm50(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    A, B = token(rng, "A"), token(rng, "B")
    X, Y = token(rng, "X"), token(rng, "Y")
    source = walking_arrow_category(A, B, "f")
    target = walking_arrow_category(X, Y, "g")
    valid = rng.random() < 0.6
    if valid:
        candidate = {
            "objects": {A: X, B: Y},
            "morphisms": {f"id_{A}": f"id_{X}", f"id_{B}": f"id_{Y}", "f": "g"},
        }
        answer = {"valid_functor": True, "violation": "NONE"}
    else:
        candidate = {
            "objects": {A: Y, B: X},
            "morphisms": {f"id_{A}": f"id_{Y}", f"id_{B}": f"id_{X}", "f": "g"},
        }
        answer = {"valid_functor": False, "violation": "ENDPOINT"}
    public = {
        "study_id": "FM50",
        "source_category": source,
        "target_category": target,
        "candidate_functor": candidate,
        "task": "Check functor validity. Return valid_functor and first violation class ENDPOINT/IDENTITY/COMPOSITION/NONE.",
    }
    return public, answer


def gen_fm60(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    a, b, c = token(rng, "N"), token(rng, "N"), token(rng, "N")
    facts = [["R", a, b], ["R", b, c]]
    target = [["R", "x", "y"], ["R", "y", "z"]]
    mapping = {a: "x", b: "y", c: "z"}
    mode = rng.choice(["NONE", "DIRECTION", "MISSING_RELATION", "TYPE"])
    node_types = {a: "T0", b: "T1", c: "T2"}
    target_types = {"x": "T0", "y": "T1", "z": "T2"}
    if mode == "DIRECTION":
        target[1] = ["R", "z", "y"]
    elif mode == "MISSING_RELATION":
        target = target[:1]
    elif mode == "TYPE":
        target_types["z"] = "T9"
    public = {
        "study_id": "FM60",
        "donor": {"facts": facts, "types": node_types},
        "target": {"facts": target, "types": target_types},
        "candidate_map": mapping,
        "task": "Find the first critical obstruction to transfer, or NONE.",
    }
    return public, {"obstruction": mode}


# ---------------------------------------------------------------------------
# FG: formalism genesis
# ---------------------------------------------------------------------------

def gen_fg10(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    features = [token(rng, "P") for _ in range(4)]
    necessary = sorted(rng.sample(features, rng.randint(1, 2)))
    cases = []
    for index, feature in enumerate(necessary):
        zero = {item: "0" for item in features}
        one = zero.copy()
        one[feature] = "1"
        cases.append({"id": f"c{index}a", "signature": ["S"], "decision": "A", "features": zero})
        cases.append({"id": f"c{index}b", "signature": ["S"], "decision": "B", "features": one})
    public = {
        "study_id": "FG10",
        "cases": cases,
        "task": "Return a minimum set of candidate feature IDs that resolves every representational collision.",
    }
    return public, {"minimal_feature_ids": necessary}


def gen_fg20(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    base = ["A", "B", "C"]
    observations = []
    outside_count = 0
    for _ in range(10):
        x, y = rng.choice(base), rng.choice(base)
        out = rng.choice(base)
        if rng.random() < 0.35:
            out = "G"
            outside_count += 1
        observations.append([x, y, out])
    decision = "GENERALIZE_OBJECT_CLASS" if outside_count >= 3 else ("LOCAL_EXCEPTION" if outside_count else "NO_CHANGE")
    public = {
        "study_id": "FG20",
        "current_object_class": base,
        "operation_observations": observations,
        "decision_rule": "GENERALIZE_OBJECT_CLASS iff >=3 outputs leave the current class; LOCAL_EXCEPTION iff 1-2; else NO_CHANGE.",
        "task": "Classify the minimum justified response to non-closure.",
    }
    return public, {"decision": decision}


def operation_value(name: str, x: int, y: int, modulus: int) -> int:
    if name == "ADD_MOD":
        return (x + y) % modulus
    if name == "MUL_MOD":
        return (x * y) % modulus
    return x ^ y


def gen_fg30(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    modulus = rng.choice([5, 7, 11])
    laws = ["ADD_MOD", "MUL_MOD", "XOR"]
    law = rng.choice(laws)
    # Generate until the selected law is uniquely identifiable among registered candidates.
    for _ in range(100):
        examples = []
        for _ in range(10):
            x, y = rng.randrange(modulus), rng.randrange(modulus)
            examples.append([x, y, operation_value(law, x, y, modulus)])
        consistent = [
            candidate for candidate in laws
            if all(operation_value(candidate, x, y, modulus) == z for x, y, z in examples)
        ]
        if consistent == [law]:
            break
    else:
        raise SuiteError("failed to generate uniquely identifiable FG30 operation law")
    public = {
        "study_id": "FG30",
        "modulus": modulus,
        "candidate_operation_ids": laws,
        "examples": examples,
        "task": "Return the unique candidate operation law exactly consistent with all observations.",
    }
    return public, {"operation_id": law}


def conjunction_holds(row: dict[str, int], features: list[str]) -> bool:
    return all(row[feature] == 1 for feature in features)


def gen_fg40(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    feature_ids = [token(rng, "Q") for _ in range(5)]
    required = sorted(rng.sample(feature_ids, rng.randint(1, 2)))
    distractors = [feature for feature in feature_ids if feature not in required]

    # Every required feature is true in every positive; distractors are explicitly
    # varied so none can accidentally become an equivalent necessary axiom.
    positives = []
    for row_index in range(max(6, 2 * len(distractors))):
        row = {feature: 1 for feature in required}
        for d_index, feature in enumerate(distractors):
            row[feature] = (row_index + d_index) % 2
        positives.append(row)

    # For each required axiom create a witness countermodel where exactly that
    # required axiom is false and all other required axioms are true. This proves
    # each member of the conjunction is individually necessary.
    negatives = []
    for feature in required:
        row = {item: 1 for item in required}
        row[feature] = 0
        for d_index, distractor in enumerate(distractors):
            row[distractor] = d_index % 2
        negatives.append(row)
    # Add extra negative variation without changing minimality witnesses.
    while len(negatives) < 6:
        row = {item: 1 for item in required}
        row[rng.choice(required)] = 0
        for distractor in distractors:
            row[distractor] = rng.randint(0, 1)
        negatives.append(row)

    public = {
        "study_id": "FG40",
        "feature_ids": feature_ids,
        "positive_models": positives,
        "negative_countermodels": negatives,
        "task": "Return the unique minimum conjunction of feature IDs true in every positive model and false in every negative countermodel.",
    }
    return public, {"axiom_feature_ids": required}


def gen_fg50(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    n = 4
    left = [token(rng, "L") for _ in range(n)]
    right = [token(rng, "R") for _ in range(n)]
    perm = list(range(n))
    rng.shuffle(perm)
    mapping = {left[i]: right[perm[i]] for i in range(n)}
    left_edges = [[left[i], left[(i + 1) % n]] for i in range(n)]
    right_edges = [[mapping[a], mapping[b]] for a, b in left_edges]
    equivalent = rng.random() < 0.65
    if not equivalent:
        right_edges[-1] = [right_edges[-1][1], right_edges[-1][0]]
    public = {
        "study_id": "FG50",
        "left": {"nodes": left, "edges": left_edges},
        "right": {"nodes": right, "edges": right_edges},
        "candidate_translation": mapping,
        "task": "Determine whether the candidate translation is a structure-preserving equivalence on the supplied finite relation.",
    }
    return public, {"equivalent": equivalent}


def gen_fg60(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    old_cases = [{"x": i, "decision": ("A" if i % 2 == 0 else "B")} for i in range(8)]
    new_cases = [dict(case) for case in old_cases]
    conservative = rng.random() < 0.7
    if not conservative:
        new_cases[rng.randrange(len(new_cases))]["decision"] = "C"
    new_cases += [{"x": 100 + i, "decision": "C"} for i in range(3)]
    public = {
        "study_id": "FG60",
        "predecessor_cases": old_cases,
        "extension_cases": new_cases,
        "task": "Return whether the extension is conservative on every predecessor-valid case.",
    }
    return public, {"conservative": conservative}


def gen_fg70(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    flags = {
        "parent_sufficient": rng.random() < 0.2,
        "missing_observation": rng.random() < 0.2,
        "local_patch_sufficient": rng.random() < 0.25,
        "registered_collision": rng.random() < 0.35,
    }
    if flags["parent_sufficient"]:
        terminal = "PARENT_FORMALISM"
    elif flags["missing_observation"]:
        terminal = "MORE_DATA"
    elif flags["local_patch_sufficient"]:
        terminal = "LOCAL_PATCH"
    elif flags["registered_collision"]:
        terminal = "NEW_FORMALISM_CANDIDATE"
    else:
        terminal = "NO_CHANGE"
    public = {
        "study_id": "FG70",
        "diagnostic_flags": flags,
        "priority_rule": ["PARENT_FORMALISM", "MORE_DATA", "LOCAL_PATCH", "NEW_FORMALISM_CANDIDATE", "NO_CHANGE"],
        "task": "Choose the minimum justified terminal using the registered priority.",
    }
    return public, {"terminal": terminal}


def gen_fg80(rng: random.Random) -> tuple[dict[str, Any], dict[str, Any]]:
    feature_ids = [token(rng, "H") for _ in range(4)]
    key = rng.choice(feature_ids)
    # Ensure exactly one feature perfectly determines every demonstration label.
    for _ in range(100):
        demonstrations = []
        for _ in range(16):
            row = {feature: rng.randint(0, 1) for feature in feature_ids}
            row["decision"] = "YES" if row[key] else "NO"
            demonstrations.append(row)
        consistent = [
            feature for feature in feature_ids
            if all(("YES" if row[feature] else "NO") == row["decision"] for row in demonstrations)
        ]
        if consistent == [key]:
            break
    else:
        raise SuiteError("failed to generate uniquely identifiable FG80 representation feature")
    target = {feature: rng.randint(0, 1) for feature in feature_ids}
    public = {
        "study_id": "FG80",
        "demonstrations": demonstrations,
        "target": target,
        "task": "Infer the unique intermediate representation feature explaining every demonstration, then decide the target.",
    }
    return public, {"representation_feature": key, "target_decision": "YES" if target[key] else "NO"}


GENERATORS = {
    "FM10": gen_fm10,
    "FM20": gen_fm20,
    "FM30": gen_fm30,
    "FM40": gen_fm40,
    "FM50": gen_fm50,
    "FM60": gen_fm60,
    "FG10": gen_fg10,
    "FG20": gen_fg20,
    "FG30": gen_fg30,
    "FG40": gen_fg40,
    "FG50": gen_fg50,
    "FG60": gen_fg60,
    "FG70": gen_fg70,
    "FG80": gen_fg80,
}


def prepare(workdir: Path, studies: list[str], per_study: int, seed: int, arms: list[str], force: bool) -> None:
    if workdir.exists():
        if not force:
            raise SuiteError(f"workdir exists: {workdir}")
        shutil.rmtree(workdir)
    if per_study < 1:
        raise SuiteError("per-study must be positive")
    if not arms:
        raise SuiteError("at least one arm is required")
    rng = random.Random(seed)
    public_tasks = []
    private_answers = {}
    for study in studies:
        if study not in GENERATORS:
            raise SuiteError(f"unsupported study {study}")
        for index in range(per_study):
            task_rng = random.Random(rng.getrandbits(64))
            public, answer = GENERATORS[study](task_rng)
            task_id = f"{study.lower()}-{index + 1:04d}"
            public["task_id"] = task_id
            public["answer_contract"] = answer_shape(answer)
            public_tasks.append(public)
            private_answers[task_id] = answer
            for arm in arms:
                write_json(
                    workdir / "requests" / arm / f"{task_id}.json",
                    {
                        "schema_version": "orion.v2.formal-discovery-request.v1",
                        "task_id": task_id,
                        "arm_id": arm,
                        "task": public,
                        "scientific_truth_authorized": False,
                        "publication_readiness_authorized": False,
                    },
                )
    write_json(workdir / "public_tasks.json", {"schema_version": "orion.v2.formal-discovery-public.v1", "tasks": public_tasks})
    write_json(workdir / "private_oracle.json", {"schema_version": "orion.v2.formal-discovery-private.v1", "answers": private_answers})
    write_json(
        workdir / "FROZEN_SUITE.json",
        {
            "schema_version": "orion.v2.formal-discovery-freeze.v1",
            "seed": seed,
            "studies": studies,
            "per_study": per_study,
            "task_count": len(public_tasks),
            "arms": arms,
            "private_oracle_visible_to_solver": False,
            "authority": {
                "grants_scientific_truth": False,
                "grants_F2_superiority": False,
                "grants_new_mathematical_theory": False,
            },
        },
    )


def command_prefix() -> list[str]:
    override = os.environ.get("ORION_FORMAL_ARM_COMMAND", "").strip()
    if override:
        import shlex
        return shlex.split(override)
    return [sys.executable, str(ROOT / "scripts/orion_formal_discovery_arms.py")]


def dispatch(workdir: Path, arms: list[str], concurrency: int, overwrite: bool) -> None:
    private = workdir / "private_oracle.json"
    if not private.exists():
        raise SuiteError("missing private oracle")
    if concurrency < 1:
        raise SuiteError("max-concurrency must be positive")
    data = private.read_bytes()
    write_json(
        workdir / "PRIVATE_ORACLE_COMMITMENT.json",
        {"sha256": digest(data), "private_removed_before_dispatch": True},
    )
    private.unlink()
    env = os.environ.copy()
    env["ORION_GOLD_ACCESS"] = "NONE"
    env["ORION_OUTCOME_ACCESS"] = "NONE"
    jobs = []
    for arm in arms:
        for request in sorted((workdir / "requests" / arm).glob("*.json")):
            response = workdir / "responses" / arm / request.name
            if response.exists() and not overwrite:
                continue
            jobs.append((arm, request, response))
    prefix = command_prefix()

    def run_one(job):
        arm, request, response = job
        response.parent.mkdir(parents=True, exist_ok=True)
        start = time.time()
        completed = subprocess.run(
            prefix + ["--request", str(request), "--response", str(response)],
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=int(os.environ.get("ORION_FORMAL_TIMEOUT", "1800")),
        )
        return {
            "arm": arm,
            "task": request.stem,
            "returncode": completed.returncode,
            "seconds": time.time() - start,
            "output_tail": completed.stdout[-1000:],
        }

    rows = []
    try:
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(run_one, job) for job in jobs]
            for future in as_completed(futures):
                rows.append(future.result())
    finally:
        if private.exists():
            raise SuiteError("private oracle reappeared during dispatch")
        private.write_bytes(data)
    write_json(
        workdir / "DISPATCH_RECEIPT.json",
        {
            "jobs": rows,
            "all_returncodes_zero": all(row["returncode"] == 0 for row in rows),
            "oracle_restored_hash_match": digest(private.read_bytes()) == digest(data),
        },
    )


def evaluate(workdir: Path, arms: list[str]) -> None:
    answers = read_json(workdir / "private_oracle.json")["answers"]
    rows = []
    summary = {}
    for arm in arms:
        correct = 0
        total = 0
        failures = 0
        for task_id, expected in answers.items():
            path = workdir / "responses" / arm / f"{task_id}.json"
            total += 1
            if not path.exists():
                failures += 1
                continue
            try:
                response = read_json(path)
                actual = response.get("answer")
            except Exception:
                failures += 1
                continue
            ok = canon(actual) == canon(expected)
            correct += int(ok)
            rows.append({"arm": arm, "task_id": task_id, "correct": ok, "expected": expected, "actual": actual})
        summary[arm] = {
            "correct": correct,
            "tasks": total,
            "accuracy": correct / total if total else 0.0,
            "missing_or_invalid": failures,
        }
    write_json(workdir / "EVALUATION_ROWS.json", rows)
    write_json(
        workdir / "EVALUATION_SUMMARY.json",
        {
            "summary": summary,
            "authority": {
                "grants_scientific_truth": False,
                "grants_F2_superiority": False,
                "grants_new_mathematical_theory": False,
            },
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    command = sub.add_parser("prepare")
    command.add_argument("--workdir", type=Path, default=DEFAULT_WORKDIR)
    command.add_argument("--studies", default=",".join(STUDIES))
    command.add_argument("--per-study", type=int, default=8)
    command.add_argument("--seed", type=int, default=20260829)
    command.add_argument("--arms", default=",".join(DEFAULT_ARMS))
    command.add_argument("--force", action="store_true")

    command = sub.add_parser("dispatch")
    command.add_argument("--workdir", type=Path, default=DEFAULT_WORKDIR)
    command.add_argument("--arms", default=",".join(DEFAULT_ARMS))
    command.add_argument("--max-concurrency", type=int, default=2)
    command.add_argument("--overwrite", action="store_true")

    command = sub.add_parser("evaluate")
    command.add_argument("--workdir", type=Path, default=DEFAULT_WORKDIR)
    command.add_argument("--arms", default=",".join(DEFAULT_ARMS))

    args = parser.parse_args()
    arms = [item for item in args.arms.split(",") if item]
    if args.cmd == "prepare":
        prepare(args.workdir, [item for item in args.studies.split(",") if item], args.per_study, args.seed, arms, args.force)
    elif args.cmd == "dispatch":
        dispatch(args.workdir, arms, args.max_concurrency, args.overwrite)
    else:
        evaluate(args.workdir, arms)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

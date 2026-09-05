"""Finite research semantics, NOT a production authority or transaction implementation.

Trusted checker records and the current-cut oracle are explicit external assumptions.
All objects are synthetic. Nothing here executes an external action. See THEORY.md.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from enum import Enum
from hashlib import sha256
from itertools import permutations, product
from typing import Iterable, Mapping
import json


class Verdict(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    CANNOT_CHECK = "CANNOT_CHECK"
    REOPEN = "REOPEN_REQUIRED"


def digest(value: object) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True, allow_nan=False).encode()).hexdigest()


@dataclass(frozen=True)
class Cell:
    value: str | None
    version: int = 0

    def __post_init__(self) -> None:
        if self.value is not None and not isinstance(self.value, str):
            raise ValueError("cell values are strings or explicitly unknown")
        if type(self.version) is not int or self.version < 0:
            raise ValueError("versions are nonnegative integers")


@dataclass(frozen=True)
class State:
    cells: tuple[tuple[str, Cell], ...]
    predicates: tuple[tuple[str, int], ...] = (("conflict/", 0),)
    sequence: int = 0

    def __post_init__(self) -> None:
        keys = [k for k, _ in self.cells]
        prefixes = [p for p, _ in self.predicates]
        if len(keys) != len(set(keys)) or keys != sorted(keys):
            raise ValueError("cell keys must be unique and canonical")
        if any(not isinstance(k, str) or not k for k in keys + prefixes):
            raise ValueError("nonempty string keys required")
        if not all(isinstance(c, Cell) for _, c in self.cells):
            raise ValueError("typed cells required")
        if len(prefixes) != len(set(prefixes)) or prefixes != sorted(prefixes):
            raise ValueError("predicate prefixes must be unique and canonical")
        if type(self.sequence) is not int or self.sequence < 0:
            raise ValueError("invalid sequence")
        if any(type(v) is not int or v < 0 for _, v in self.predicates):
            raise ValueError("invalid predicate version")

    @classmethod
    def of(cls, values: Mapping[str, str | None]) -> State:
        return cls(tuple(sorted((k, Cell(v)) for k, v in values.items())))

    @property
    def fingerprint(self) -> str:
        return digest(asdict(self))

    def change(self, key: str, value: str | None) -> State:
        """Trusted model transition: even an ABA/same-value write changes version."""
        cells = dict(self.cells)
        old = cells.get(key)
        cells[key] = Cell(value, 0 if old is None else old.version + 1)
        guards = tuple((p, v + int(key.startswith(p))) for p, v in self.predicates)
        return State(tuple(sorted(cells.items())), guards, self.sequence + 1)


@dataclass(frozen=True)
class Spec:
    subject: str
    payload: str
    requirements: tuple[tuple[str, str], ...]
    absent_prefix: str | None = "conflict/"

    def __post_init__(self) -> None:
        if not isinstance(self.subject, str) or not isinstance(self.payload, str) or not self.subject or not self.payload:
            raise ValueError("subject and payload must be explicit")
        keys = [k for k, _ in self.requirements]
        if keys != sorted(keys) or len(keys) != len(set(keys)):
            raise ValueError("requirements must be unique and canonical")
        if any(not isinstance(k, str) or not isinstance(v, str)
               for k, v in self.requirements):
            raise ValueError("requirements are string equalities")
        if self.absent_prefix is not None and (not isinstance(self.absent_prefix, str) or not self.absent_prefix):
            raise ValueError("empty predicate is not admitted")

    @property
    def fingerprint(self) -> str:
        return digest(asdict(self))

    @property
    def required(self) -> dict[str, str]:
        out = dict(self.requirements)
        # Prior permission is not created by the output receipt.
        if out.get("authority:commit", "GRANTED") != "GRANTED":
            raise ValueError("a specification cannot weaken prior permission")
        out["authority:commit"] = "GRANTED"
        return out


# kind, name, value, version; predicate reads cannot alias ordinary cell reads.
Read = tuple[str, str, str | None, int]


def read_view(spec: Spec, state: State) -> tuple[Read, ...]:
    cells = dict(state.cells)
    view: list[Read] = []
    for key in sorted(spec.required):
        cell = cells.get(key)
        view.append(("cell", key, None if cell is None else cell.value,
                     -1 if cell is None else cell.version))
    if spec.absent_prefix is not None:
        v = dict(state.predicates).get(spec.absent_prefix, -1)
        view.append(("predicate", spec.absent_prefix, None, v))
    return tuple(view)


def evaluate(spec: Spec, state: State) -> Verdict:
    """The *registered model* precondition, not a real-world truth oracle."""
    cells = dict(state.cells)
    unknown = False
    for key, expected in spec.required.items():
        cell = cells.get(key)
        if cell is None or cell.value is None:
            unknown = True
        elif cell.value != expected:
            return Verdict.FAIL
    if spec.absent_prefix is not None:
        if spec.absent_prefix not in dict(state.predicates):
            unknown = True
        for key, cell in state.cells:
            if key.startswith(spec.absent_prefix):
                if cell.value == "BLOCK":
                    return Verdict.FAIL
                if cell.value is None:
                    unknown = True
    return Verdict.CANNOT_CHECK if unknown else Verdict.PASS


@dataclass(frozen=True)
class CheckerRecord:
    specification: str
    historical_state: str
    verdict: Verdict

    def __post_init__(self) -> None:
        if not isinstance(self.verdict, Verdict):
            raise ValueError("checker verdict must use the registered vocabulary")

    @property
    def identifier(self) -> str:
        return digest(asdict(self))


@dataclass(frozen=True)
class Certificate:
    specification: str
    historical_state: str
    reads: tuple[Read, ...]
    checker_record: str

    @property
    def identifier(self) -> str:
        return digest(asdict(self))


def model_check(spec: Spec, state: State, *, available: bool = True) -> CheckerRecord:
    """Harness-only stand-in for an independently trusted checker record."""
    return CheckerRecord(spec.fingerprint, state.fingerprint,
                         evaluate(spec, state) if available else Verdict.CANNOT_CHECK)


def certificate(spec: Spec, state: State, record: CheckerRecord) -> Certificate:
    return Certificate(spec.fingerprint, state.fingerprint, read_view(spec, state),
                       record.identifier)


def validation_cost(spec: Spec) -> int:
    # Logical probes ONLY; hashing/materializing the complete snapshot is extra O(N).
    return len(spec.required) + int(spec.absent_prefix is not None) + 2


def validate(cert: Certificate, spec: Spec, historical: State | None, current: State,
             records: Mapping[str, CheckerRecord], *, current_cut_known: bool,
             budget: int) -> Verdict:
    """One atomic MODEL step. current_cut_known is an oracle premise, not evidence.

    A real OCM adapter must discharge that premise; a caller's boolean is insufficient.
    This function intentionally does not claim production synchronization/authentication.
    """
    if type(current_cut_known) is not bool:
        raise ValueError("current-cut oracle must be an explicit boolean premise")
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    if budget < validation_cost(spec) or historical is None:
        return Verdict.CANNOT_CHECK
    if cert.specification != spec.fingerprint or cert.historical_state != historical.fingerprint:
        return Verdict.FAIL
    if cert.reads != read_view(spec, historical):
        return Verdict.FAIL
    record = records.get(cert.checker_record)
    if record is None:
        return Verdict.CANNOT_CHECK
    if record.identifier != cert.checker_record:
        return Verdict.FAIL
    if (record.specification, record.historical_state) != (cert.specification, cert.historical_state):
        return Verdict.FAIL
    if record.verdict is Verdict.CANNOT_CHECK:
        return Verdict.CANNOT_CHECK
    if record.verdict is not Verdict.PASS:
        return Verdict.FAIL
    if not current_cut_known:
        return Verdict.CANNOT_CHECK
    if cert.reads != read_view(spec, current):
        return Verdict.REOPEN
    return Verdict.PASS


def parent_validate(cert: Certificate, spec: Spec, historical: State | None, current: State,
                    records: Mapping[str, CheckerRecord], *, current_cut_known: bool,
                    budget: int) -> Verdict:
    """Separate straightforward transactional read-set parent (no validate/read_view call)."""
    if type(current_cut_known) is not bool:
        raise ValueError("current-cut oracle must be an explicit boolean premise")
    if type(budget) is not int or budget < 0:
        raise ValueError("invalid budget")
    req = spec.required
    if historical is None or budget < len(req) + (spec.absent_prefix is not None) + 2:
        return Verdict.CANNOT_CHECK
    if cert.specification != spec.fingerprint or cert.historical_state != historical.fingerprint:
        return Verdict.FAIL
    expected: list[Read] = []
    for key in sorted(req):
        matches = [c for k, c in historical.cells if k == key]
        expected.append(("cell", key, matches[0].value if matches else None,
                         matches[0].version if matches else -1))
    if spec.absent_prefix is not None:
        matches = [v for p, v in historical.predicates if p == spec.absent_prefix]
        expected.append(("predicate", spec.absent_prefix, None, matches[0] if matches else -1))
    if cert.reads != tuple(expected):
        return Verdict.FAIL
    if cert.checker_record not in records:
        return Verdict.CANNOT_CHECK
    r = records[cert.checker_record]
    if r.identifier != cert.checker_record or r.specification != cert.specification or r.historical_state != cert.historical_state:
        return Verdict.FAIL
    if r.verdict != Verdict.PASS:
        return Verdict.CANNOT_CHECK if r.verdict == Verdict.CANNOT_CHECK else Verdict.FAIL
    if not current_cut_known:
        return Verdict.CANNOT_CHECK
    for kind, name, value, version in cert.reads:
        if kind == "cell":
            found = [c for k, c in current.cells if k == name]
            now = (found[0].value, found[0].version) if found else (None, -1)
            if now != (value, version):
                return Verdict.REOPEN
        else:
            found = [v for p, v in current.predicates if p == name]
            if (found[0] if found else -1) != version:
                return Verdict.REOPEN
    return Verdict.PASS


def commit_record(cert: Certificate, spec: Spec, historical: State | None, current: State,
                  records: Mapping[str, CheckerRecord], *, current_cut_known: bool,
                  budget: int) -> dict:
    verdict = validate(cert, spec, historical, current, records,
                       current_cut_known=current_cut_known, budget=budget)
    return {"verdict": verdict.value, "committed": verdict is Verdict.PASS,
            "linearization_sequence": current.sequence if verdict is Verdict.PASS else None,
            "current_state": current.fingerprint, "certificate": cert.identifier,
            "effect": "NONE_MODEL_ONLY", "probes_required": validation_cost(spec)}


def schedules() -> tuple[tuple[str, ...], ...]:
    return tuple(p for p in permutations(("r0", "w0", "r1", "w1"))
                 if p.index("r0") < p.index("w0") and p.index("r1") < p.index("w1"))


def write_skew(schedule: Iterable[str], *, validate_full_read_set: bool) -> tuple[bool, bool]:
    """Two synthetic maintainers may leave only while the other remains available."""
    live = [True, True]
    versions = [0, 0]
    snapshots = {}
    for event in schedule:
        i = int(event[1])
        if event[0] == "r":
            snapshots[i] = (tuple(live), tuple(versions))
        else:
            values, old_versions = snapshots[i]
            check = range(2) if validate_full_read_set else (i,)
            if values[1-i] and all(versions[k] == old_versions[k] for k in check):
                live[i] = False
                versions[i] += 1
    return tuple(live)


def genesis(initial: State) -> str:
    return digest({"schema": "revision-log-v1", "initial_state": initial.fingerprint})


def build_log(initial: State, changes: Iterable[tuple[str, str | None]]) -> tuple[dict, ...]:
    out, previous = [], genesis(initial)
    for sequence, (key, value) in enumerate(changes, 1):
        row = {"sequence": sequence, "key": key, "value": value, "previous": previous}
        row["digest"] = digest(row)
        out.append(row)
        previous = row["digest"]
    return tuple(out)


def checkpoint(initial: State, log: tuple[dict, ...]) -> tuple[int, str]:
    return len(log), log[-1]["digest"] if log else genesis(initial)


def replay(initial: State, log: tuple[dict, ...], expected: tuple[int, str] | None) -> tuple[Verdict, State | None]:
    """An expected checkpoint is supplied out-of-band, never inferred as authority."""
    state, previous = initial, genesis(initial)
    for sequence, row in enumerate(log, 1):
        if set(row) != {"sequence", "key", "value", "previous", "digest"}:
            return Verdict.FAIL, None
        if type(row["sequence"]) is not int or row["sequence"] != sequence or row["previous"] != previous:
            return Verdict.FAIL, None
        body = {k: v for k, v in row.items() if k != "digest"}
        if digest(body) != row["digest"]:
            return Verdict.FAIL, None
        if not isinstance(row["key"], str) or not row["key"]:
            return Verdict.FAIL, None
        if row["value"] is not None and not isinstance(row["value"], str):
            return Verdict.FAIL, None
        state = state.change(row["key"], row["value"])
        previous = row["digest"]
    if expected is None:
        return Verdict.CANNOT_CHECK, state  # internally replayable is not anchored
    if (len(expected) != 2 or type(expected[0]) is not int
            or not isinstance(expected[1], str) or checkpoint(initial, log) != expected):
        return Verdict.FAIL, None
    return Verdict.PASS, state  # exact prefix only; no assertion about later events


def closed_cut(parents: tuple[tuple[int, ...], ...], cut: frozenset[int]) -> bool:
    n = len(parents)
    if any(type(i) is not int for i in cut) or not cut <= set(range(n)):
        raise ValueError("unknown event")
    # The registered finite representation is topologically indexed.
    if any(any(type(j) is not int or not 0 <= j < i for j in row) or len(set(row)) != len(row)
           for i, row in enumerate(parents)):
        raise ValueError("parents must be distinct earlier vertices")
    return all(set(parents[i]) <= cut for i in cut)


def ancestor_cut(parents: tuple[tuple[int, ...], ...], cut: frozenset[int]) -> bool:
    """Separate transitive-ancestor reference on already validated finite DAGs."""
    for i in cut:
        stack, seen = list(parents[i]), set()
        while stack:
            p = stack.pop()
            if p not in cut:
                return False
            if p not in seen:
                seen.add(p)
                stack.extend(parents[p])
    return True


def descriptor_sufficient(descriptor: tuple[int, ...], judgment: tuple[bool, ...]) -> bool:
    if len(descriptor) != len(judgment):
        raise ValueError("domain mismatch")
    for i, j in product(range(len(descriptor)), repeat=2):
        if descriptor[i] == descriptor[j] and judgment[i] != judgment[j]:
            return False
    return True

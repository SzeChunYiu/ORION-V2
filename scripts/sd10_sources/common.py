"""Shared lawful-acquisition core for SD10 population-corpus source adapters.

Design rules enforced here (SD10 design receipt V1):
- stdlib only; every network hop goes through an injectable transport so tests
  run against fixtures and never touch the network.
- conservative per-source rate compliance is the caller's documented contract;
  this module enforces the mechanical minimum-interval and retry policy.
- HTTP 4xx is a hard fail-closed signal EXCEPT 429 (backoff-and-retry);
  5xx and transport errors retry with capped exponential backoff.
- cursor state is persisted atomically after every page so an interrupted run
  resumes instead of silently re-fetching or skipping records.
- citation/fame numbers are proxy metrics only; no code path in this module can
  map them to an outcome class.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Callable

from orion_v2.scientific_development import DevelopmentOutcomeClass
from orion_v2.scientific_development_sources import DevelopmentObservation, ObservationKind, OutcomeBinding

RECEIPT_SCHEMA = "orion.v2.sd10-source-adapter-receipt.v1"
RETRYABLE_STATUS = {429, 500, 502, 503, 504}
CENSORING_STATEMENT = (
    "Sources indexed here contain only publicly deposited records; unpublished "
    "failures, abandoned lines without a deposited artifact, and unindexed work are "
    "absent-by-censoring, not absent-by-fact. No inference of success from absence "
    "is authorized by any SD10 artifact."
)

BIAS_PUBLICATION = "BIAS_PUBLICATION_ONLY_CORPUS"
BIAS_SURVIVORSHIP = "BIAS_SURVIVORSHIP_OF_INDEXED_RECORDS"
BIAS_CITATION_WINDOW = "BIAS_CITATION_WINDOW_TRUNCATION"
BIAS_LANGUAGE_GEOGRAPHY = "BIAS_LANGUAGE_GEOGRAPHY_SKEW"


class HardFailClosed(RuntimeError):
    """Raised for non-retryable HTTP 4xx: acquisition stops, run fails closed."""


@dataclass(frozen=True)
class Response:
    status: int
    body: bytes


class UrllibTransport:
    """Default stdlib transport. Tests inject their own callable instead."""

    def __init__(self, timeout: float = 30.0) -> None:
        self.timeout = timeout

    def __call__(self, url: str, headers: dict) -> Response:
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as raw:
                return Response(status=raw.status, body=raw.read())
        except urllib.error.HTTPError as exc:
            return Response(status=exc.code, body=exc.read())


class RateLimiter:
    """Minimum-interval gate; sleep function is injectable for tests."""

    def __init__(self, min_interval_seconds: float, sleep: Callable[[float], None]) -> None:
        self.min_interval_seconds = float(min_interval_seconds)
        self._sleep = sleep
        self._last = float("-inf")
        self.waits: list[float] = []

    def wait(self) -> None:
        now = time.monotonic()
        delta = self._last + self.min_interval_seconds - now
        if delta > 0:
            self.waits.append(round(delta, 6))
            self._sleep(delta)
            self._last = self._last + self.min_interval_seconds
        else:
            self._last = now


def fetch_with_retry(
    transport: Callable[[str, dict], Response],
    url: str,
    headers: dict,
    *,
    rate_limiter: RateLimiter,
    sleep: Callable[[float], None],
    retries: int,
    backoff_base: float = 2.0,
    backoff_cap: float = 120.0,
) -> Response:
    """One lawful fetch: rate-gated, retried on 429/5xx/transport errors.

    Any other 4xx raises HardFailClosed immediately (never silently skipped).
    Returns the Response on success (2xx only).
    """
    last_error: Exception | None = None
    for attempt in range(max(1, retries)):
        rate_limiter.wait()
        try:
            response = transport(url, headers)
        except urllib.error.HTTPError as exc:
            response = Response(status=exc.code, body=b"")
        except (urllib.error.URLError, OSError, TimeoutError) as exc:
            last_error = exc
            _backoff(sleep, attempt, backoff_base, backoff_cap)
            continue
        if 200 <= response.status < 300:
            return response
        if response.status in RETRYABLE_STATUS:
            _backoff(sleep, attempt, backoff_base, backoff_cap)
            last_error = RuntimeError(f"retryable HTTP {response.status}")
            continue
        raise HardFailClosed(f"HTTP {response.status} at {url}: failing closed (no silent skip)")
    raise RuntimeError(f"retries exhausted for {url}: {last_error}")


def _backoff(sleep: Callable[[float], None], attempt: int, base: float, cap: float) -> None:
    sleep(min(cap, base ** attempt))


class CursorState:
    """Resumable per-source cursor persisted atomically after every page."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.data: dict = {"schema_version": RECEIPT_SCHEMA, "cursor": None, "records_emitted": 0, "pages_fetched": 0}
        if path.exists():
            self.data = json.loads(path.read_text(encoding="utf-8"))

    def advance(self, cursor, records_emitted: int) -> None:
        self.data["cursor"] = cursor
        self.data["records_emitted"] = records_emitted
        self.data["pages_fetched"] = int(self.data.get("pages_fetched", 0)) + 1
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(self.data, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(tmp, self.path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(Path(path).read_bytes())
    return digest.hexdigest()


def observation_to_json(observation: DevelopmentObservation) -> dict:
    """Serialize a validated observation exactly as the assemble script reads it."""
    value = {
        "observation_id": observation.observation_id,
        "trajectory_id": observation.trajectory_id,
        "domain_id": observation.domain_id,
        "epoch_id": observation.epoch_id,
        "source_mode_id": observation.source_mode_id,
        "ordinal": observation.ordinal,
        "kind": observation.kind.value,
        "action_feature_ids": list(observation.action_feature_ids),
        "result_feature_ids": list(observation.result_feature_ids),
        "failure_feature_ids": list(observation.failure_feature_ids),
        "source_ids": list(observation.source_ids),
        "validation_ids": list(observation.validation_ids),
        "institution_ids": list(observation.institution_ids),
        "team_id": observation.team_id,
        "proxy_metrics": {name: float(number) for name, number in observation.proxy_metrics},
        "bias_flag_ids": list(observation.bias_flag_ids),
        "resource_cost": float(observation.resource_cost),
    }
    # Construction of the frozen dataclass already validated every invariant.
    DevelopmentObservation(
        observation_id=value["observation_id"], trajectory_id=value["trajectory_id"],
        domain_id=value["domain_id"], epoch_id=value["epoch_id"], source_mode_id=value["source_mode_id"],
        ordinal=value["ordinal"], kind=ObservationKind(value["kind"]),
        action_feature_ids=tuple(value["action_feature_ids"]), result_feature_ids=tuple(value["result_feature_ids"]),
        failure_feature_ids=tuple(value["failure_feature_ids"]), source_ids=tuple(value["source_ids"]),
        validation_ids=tuple(value["validation_ids"]), institution_ids=tuple(value["institution_ids"]),
        team_id=value["team_id"], proxy_metrics=tuple(value["proxy_metrics"].items()),
        bias_flag_ids=tuple(value["bias_flag_ids"]), resource_cost=value["resource_cost"],
    )
    return value


def binding_to_json(binding: OutcomeBinding) -> dict:
    value = {
        "trajectory_id": binding.trajectory_id,
        "outcome_class": binding.outcome_class.value,
        "witness_ids": list(binding.witness_ids),
        "source_ids": list(binding.source_ids),
    }
    OutcomeBinding(value["trajectory_id"], DevelopmentOutcomeClass(value["outcome_class"]),
                   tuple(value["witness_ids"]), tuple(value["source_ids"]))
    return value


def write_jsonl(path: Path, rows: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    os.replace(tmp, path)


def load_jsonl_rows(path: Path) -> list:
    """Read a JSONL file tolerantly; missing/empty file yields []."""
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def append_jsonl(path: Path, rows: list) -> None:
    """Append rows without truncating the file (durable incremental output)."""
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


class OutputLedger:
    """Durable incremental JSONL output keyed for resume-merge.

    An interrupted run must not lose already-fetched records on resume, so rows
    are appended to disk after every page and BEFORE the cursor state advances;
    a crash between an append and the state advance only re-fetches rows that
    are already safely on disk, and the load-time dedupe by key removes such
    duplicates. Keys already present are never re-emitted (first row wins;
    observation/binding ids are deterministic per record).
    """

    def __init__(self, path: Path, key_fn: Callable[[dict], str]) -> None:
        self.path = path
        self.key_fn = key_fn
        self.index: dict = {}
        for row in load_jsonl_rows(path):
            self.index[self.key_fn(row)] = row
        self.new_rows: list = []

    def add(self, rows: list) -> list:
        """Append only rows whose key is new; returns the appended rows."""
        fresh = [row for row in rows if self.key_fn(row) not in self.index]
        if fresh:
            append_jsonl(self.path, fresh)
            for row in fresh:
                self.index[self.key_fn(row)] = row
                self.new_rows.append(row)
        return fresh

    def rows(self) -> list:
        return list(self.index.values())

    def rewrite_atomically(self) -> None:
        write_jsonl(self.path, self.rows())


def observation_key(row: dict) -> str:
    return row["observation_id"]


def binding_key(row: dict) -> str:
    # Key by trajectory AND witnesses so two independent retraction notices for
    # the same trajectory both survive a resume-merge.
    return row["trajectory_id"] + "|" + "|".join(sorted(row["witness_ids"]))


def utc_today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def write_receipt(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def base_receipt(*, source_id: str, source_mode_id: str, lineage: list, endpoints: list,
                 terms_note: str, rate_note: str, dry_run: bool, since: str, until: str,
                 max_records: int) -> dict:
    return {
        "schema_version": RECEIPT_SCHEMA,
        "source": {
            "source_id": source_id,
            "source_mode_id": source_mode_id,
            "lineage": lineage,
            "endpoints": endpoints,
            "terms_note": terms_note,
            "rate_limit_compliance": rate_note,
        },
        "run": {"dry_run": dry_run, "since": since, "until": until, "max_records": max_records},
        "fetched_window": {"since": since, "until": until},
        "request_count": 0,
        "pages": 0,
        "records": {"observations_emitted": 0, "outcome_bindings_emitted": 0, "per_record_source_ids": []},
        "emitted_files": [],
        "error_log": [],
        "censoring_statement": CENSORING_STATEMENT,
        "outcome_policy": {
            "citation_or_fame_metric_infers_outcome": False,
            "arxiv_version_progression_is_outcome": False,
            "unvalidated_outcome_class": "UNKNOWN",
            "absence_of_retraction_is_never_success": True,
        },
        "authority": {"grants_scientific_truth": False, "grants_causal_law": False},
    }


def parse_iso_date(value: str, flag: str) -> str:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"--{flag} must be YYYY-MM-DD: {value}") from exc
    return parsed.isoformat()



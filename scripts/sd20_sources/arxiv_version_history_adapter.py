#!/usr/bin/env python3
"""SD20 lawful source adapter: arXiv per-version history -> development observations.

Purpose: SD10's arXiv observations are head-version snapshots only (one
observation per trajectory), so the assembled corpus has no within-trajectory
transitions. This adapter fetches the MISSING earlier versions (v1..v(k-1)) of
every SD10 arXiv trajectory whose head observation is v2 or later, using the
same public arXiv Atom metadata API with versioned id_list requests. The head
observations themselves are never re-fetched.

Lawful acquisition contract (same as SD10, scripts/sd10_sources/arxiv_adapter.py):
- Uses ONLY the public arXiv Atom metadata API (export.arxiv.org/api/query),
  documented for programmatic metadata access under its API terms of use
  (https://info.arxiv.org/help/api/tou.html): no more than one request every
  3 seconds, one connection at a time, a descriptive User-Agent with contact
  information. Versioned id_list batching (comma-separated ids, one response)
  keeps request count far BELOW the per-record floor, never above it.
- Default rate interval is therefore 3.0s (configurable only upward via
  --rate-seconds; the CLI rejects a smaller value for this source).
- --batch-size ids per request; --dry-run prints the plan and performs zero
  requests; HTTP 4xx other than 429 fails closed (HardFailClosed); 429/5xx
  back off; cursor + ledger make an interrupted run resume safely.

Scientific honesty contract:
- Per-version <updated> dates are REAL temporal metadata (verified by probe:
  2401.00614v1 updated 2024-01-01, v2 updated 2025-02-16) and are recorded as
  proxy metrics (arxiv:updated_epoch_days, arxiv:days_since_first_deposit);
  <published> is the paper-level v1 submission date and is identical across
  versions, so epoch_id is anchored to the parent head observation's epoch.
- domain_id is anchored to the parent head observation's domain so a
  mid-trajectory primary-category change cannot split a trajectory (the
  per-version category is still recorded as an action feature). Anchoring
  events are counted in the receipt, never silently applied.
- arXiv metadata carries NO validated scientific outcome. This adapter NEVER
  emits an outcome binding; version progression is an observation stream, not
  an outcome. Proxy metrics never map to outcome classes.
- A requested versioned id that returns no entry is recorded in the receipt's
  missing_versions list (honest censoring), never invented.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

if __package__ in (None, ""):  # pragma: no cover - direct script execution
    if "sd20_sources_common" not in sys.modules:
        _spec = importlib.util.spec_from_file_location(
            "sd20_sources_common", Path(__file__).resolve().parent.parent / "sd10_sources" / "common.py")
        _module = importlib.util.module_from_spec(_spec)
        sys.modules["sd20_sources_common"] = _module
        _spec.loader.exec_module(_module)
    common = sys.modules["sd20_sources_common"]
else:  # pragma: no cover
    from ..sd10_sources import common

from orion_v2.scientific_development_sources import DevelopmentObservation, ObservationKind

SOURCE_ID = "arxiv"
SOURCE_MODE_ID = "arxiv_atom_version_history"
ENDPOINT = "https://export.arxiv.org/api/query"
TERMS_NOTE = (
    "arXiv public Atom metadata API with versioned id_list requests; terms of "
    "use ask for <=1 request per 3 seconds, a single connection, and a "
    "descriptive User-Agent with contact information "
    "(https://info.arxiv.org/help/api/tou.html). Batching multiple versioned "
    "ids into one request reduces request count below the per-record floor. "
    "Metadata is redistribution-compatible with attribution; no fulltext fetch."
)
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
RATE_NOTE = ("arXiv API etiquette: min interval 3.0s enforced (>= documented 1 "
             "req/3s), UA carries contact email, batched id_list keeps total "
             "requests far below one-per-version-record")
DEFAULT_RATE_SECONDS = 3.0
EPOCH_ANCHOR = date(1970, 1, 1)


def load_parent_plan(parent_path: Path) -> list[dict]:
    """Derive (arxiv_id, head_version, head_domain, head_epoch) plan rows.

    Parent rows are the SD10 head-version observations. The version-target
    list is ALWAYS the full v1..v(head-1) set so the batch plan is STABLE
    across runs (a cursor indexes the same list in every run); resume skips
    batches whose targets are all already durable in the output ledger, and
    the ledger's key-dedupe absorbs any re-fetched rows from a torn batch.
    """
    plan: dict[str, dict] = {}
    for row in common.load_jsonl_rows(parent_path):
        if not row["observation_id"].startswith("arxiv-obs:"):
            continue
        tail = row["observation_id"][len("arxiv-obs:"):]
        arxiv_id, _, version_text = tail.rpartition("v")
        if not arxiv_id or not version_text.isdigit():
            continue
        version = int(version_text)
        if version < 2:
            continue  # head is v1: no earlier versions exist to fetch
        plan[arxiv_id] = {
            "arxiv_id": arxiv_id,
            "head_version": version,
            "head_domain": row["domain_id"],
            "head_epoch": row["epoch_id"],
            "published": "",
        }
    rows = sorted(plan.values(), key=lambda item: item["arxiv_id"])
    for row in rows:
        row["versions_to_fetch"] = list(range(1, row["head_version"]))
    return rows


def plan_batches(rows: list[dict], batch_size: int) -> list[list[tuple[str, int]]]:
    """Flatten (arxiv_id, version) targets into URL batches."""
    targets = []
    for row in rows:
        for version in row["versions_to_fetch"]:
            targets.append((row["arxiv_id"], version))
    return [targets[i:i + batch_size] for i in range(0, len(targets), batch_size)]


def build_url(batch: list[tuple[str, int]]) -> str:
    id_list = ",".join(f"{arxiv_id}v{version}" for arxiv_id, version in batch)
    return ENDPOINT + "?" + urllib.parse.urlencode({"id_list": id_list, "max_results": len(batch)})


def parse_feed(body: bytes) -> list[dict]:
    """Parse an arXiv Atom id_list response into per-version entry dicts."""
    root = ET.fromstring(body)
    entries = []
    for entry in root.findall(f"{ATOM}entry"):
        raw_id = (entry.findtext(f"{ATOM}id") or "").strip()
        arxiv_id = raw_id.rsplit("/abs/", 1)[-1]
        version = 1
        if "v" in arxiv_id.rsplit(".", 1)[-1]:
            tail = arxiv_id.rsplit("v", 1)[-1]
            if tail.isdigit():
                version = int(tail)
                arxiv_id = arxiv_id.rsplit("v", 1)[0]
        if not arxiv_id:
            continue
        authors = [node.findtext(f"{ATOM}name", default="").strip()
                   for node in entry.findall(f"{ATOM}author")]
        primary = entry.find(f"{ARXIV}primary_category")
        categories = [c.get("term", "") for c in entry.findall(f"{ATOM}category")]
        published = entry.findtext(f"{ATOM}published", default="")[:10]
        updated = entry.findtext(f"{ATOM}updated", default="")[:10]
        title = (entry.findtext(f"{ATOM}title", default="") or "").strip()
        summary = (entry.findtext(f"{ATOM}summary", default="") or "").strip()
        entries.append({
            "arxiv_id": arxiv_id, "version": version, "raw_id": raw_id,
            "published": published, "updated": updated,
            "primary_category": (primary.get("term", "") if primary is not None
                                 else (categories[0] if categories else "")),
            "author_count": sum(1 for name in authors if name),
            "title": title, "title_chars": len(title),
            "abstract_chars": len(summary),
        })
    return entries


def check_atom_error(entries: list[dict]) -> None:
    if len(entries) == 1 and entries[0]["title"].strip().lower() == "error":
        raise common.HardFailClosed("arXiv Atom API returned an error entry; failing closed")


def _days(value: str) -> float:
    return float((date.fromisoformat(value) - EPOCH_ANCHOR).days)


def to_observation(entry: dict, parent: dict, counters: dict) -> DevelopmentObservation:
    """One version observation, domain/epoch anchored to the parent head."""
    if entry["primary_category"] and \
            f"arxiv-cat:{entry['primary_category']}" != parent["head_domain"]:
        counters["version_domain_anchored_to_head"] = \
            counters.get("version_domain_anchored_to_head", 0) + 1
    if entry["published"] and entry["published"][:4] != parent["head_epoch"][-4:]:
        counters["version_epoch_anchored_to_head"] = \
            counters.get("version_epoch_anchored_to_head", 0) + 1
    version = entry["version"]
    kind = ObservationKind.VERSION_OR_REVISION if version > 1 else ObservationKind.OTHER
    proxy = [
        ("arxiv:author_count", float(entry["author_count"])),
        ("arxiv:title_chars", float(entry["title_chars"])),
        ("arxiv:abstract_chars", float(entry["abstract_chars"])),
    ]
    if entry["updated"]:
        proxy.append(("arxiv:updated_epoch_days", _days(entry["updated"])))
    if entry["updated"] and entry["published"]:
        proxy.append(("arxiv:days_since_first_deposit",
                      _days(entry["updated"]) - _days(entry["published"])))
    return DevelopmentObservation(
        observation_id=f"arxiv-obs:{entry['arxiv_id']}v{version}",
        trajectory_id=f"arxiv:{entry['arxiv_id']}",
        domain_id=parent["head_domain"],
        epoch_id=parent["head_epoch"],
        source_mode_id=SOURCE_MODE_ID,
        ordinal=max(0, version - 1),
        kind=kind,
        action_feature_ids=("arxiv:deposit_version",
                            f"arxiv:primary_category:{entry['primary_category'] or 'uncategorized'}"),
        source_ids=(entry["raw_id"],),
        proxy_metrics=tuple(proxy),
        bias_flag_ids=(common.BIAS_PUBLICATION, common.BIAS_SURVIVORSHIP,
                       common.BIAS_LANGUAGE_GEOGRAPHY),
    )


def run(args, transport=None, sleep=None) -> dict:
    sleep = sleep or (lambda seconds: __import__("time").sleep(seconds))
    transport = transport or common.UrllibTransport(timeout=args.timeout)
    receipt = common.base_receipt(
        source_id=SOURCE_ID, source_mode_id=SOURCE_MODE_ID,
        lineage=["arXiv Atom metadata API (public, documented), versioned id_list mode",
                 "SD10 adapter (head versions): scripts/sd10_sources/arxiv_adapter.py",
                 f"SD20 adapter (earlier versions): {Path(__file__).name}",
                 f"parent observations: {args.parent_observations} "
                 f"(sha256 {common.sha256_file(Path(args.parent_observations))})"],
        endpoints=[ENDPOINT], terms_note=TERMS_NOTE, rate_note=RATE_NOTE,
        dry_run=args.dry_run, since=args.since, until=args.until, max_records=args.max_records)
    receipt["window_semantics"] = (
        "since/until describe the SD10 parent-selection window "
        "(submittedDate), not a per-version filter: version entries are fetched "
        "by id, and a version's own <updated> date may fall outside the window.")
    state = common.CursorState(Path(args.state))
    obs_ledger = common.OutputLedger(Path(args.output_observations), common.observation_key)
    bind_ledger = common.OutputLedger(Path(args.output_bindings), common.binding_key)
    rows = load_parent_plan(Path(args.parent_observations))
    batches = plan_batches(rows, args.batch_size)
    all_targets = {f"arxiv-obs:{row['arxiv_id']}v{version}"
                   for row in rows for version in row["versions_to_fetch"]}
    receipt["plan"] = {
        "parent_trajectories_v2plus": len(rows),
        "version_targets": len(all_targets),
        "batches_planned": len(batches),
        "already_on_disk": len(all_targets & set(obs_ledger.index)),
        "batch_size": args.batch_size}
    if args.dry_run:
        receipt["dry_run_plan"] = {"requests_planned": len(batches),
                                   "note": "dry run: zero network requests were made"}
        return receipt
    if not args.contact_email:
        raise SystemExit("arXiv API etiquette requires a descriptive contact email: "
                         "--contact-email or SD10_CONTACT_EMAIL")
    headers = {"User-Agent": f"ORION-V2-SD20-version-history-harvester (mailto:{args.contact_email})"}
    limiter = common.RateLimiter(args.rate_seconds, sleep)
    counters: dict = {}
    missing_versions: list[str] = []
    parents_by_id = {row["arxiv_id"]: row for row in rows}
    start_batch = int((state.data.get("cursor") or {"batch": 0})["batch"])
    emitted_total = int(state.data.get("records_emitted", 0))
    if start_batch > 0:
        receipt["resumed_from_batch"] = start_batch
    for batch_index, batch in enumerate(batches[start_batch:], start=start_batch):
        requested_ids = {f"arxiv-obs:{arxiv_id}v{version}" for arxiv_id, version in batch}
        if requested_ids <= set(obs_ledger.index):
            # every target of this batch is already durable: skip without a
            # request (stable-plan resume) and advance the cursor
            state.advance({"batch": batch_index + 1}, emitted_total)
            continue
        requested = {f"{arxiv_id}v{version}" for arxiv_id, version in batch}
        response = common.fetch_with_retry(
            transport, build_url(batch), headers,
            rate_limiter=limiter, sleep=sleep, retries=args.retries,
            backoff_cap=args.backoff_cap)
        receipt["request_count"] += 1
        entries = parse_feed(response.body)
        check_atom_error(entries)
        observations = []
        for entry in entries:
            parent = parents_by_id.get(entry["arxiv_id"])
            if parent is None or f"{entry['arxiv_id']}v{entry['version']}" not in requested:
                receipt["error_log"].append(
                    f"unplanned entry in response: {entry['raw_id']}")
                continue
            observations.append(to_observation(entry, parent, counters))
        for versioned in sorted(requested - {
                f"{entry['arxiv_id']}v{entry['version']}" for entry in entries}):
            missing_versions.append(versioned)
        # Durable output BEFORE the cursor advances (SD10 resume contract);
        # the cursor carries the index of the NEXT unfetched batch.
        fresh = obs_ledger.add([common.observation_to_json(obs) for obs in observations])
        bind_ledger.add([])
        emitted_total += len(fresh)
        state.advance({"batch": batch_index + 1}, emitted_total)
    obs_ledger.rewrite_atomically()
    bind_ledger.rewrite_atomically()
    all_rows = obs_ledger.rows()
    receipt["pages"] = state.data.get("pages_fetched", 0)
    receipt["records"] = {
        "observations_emitted": len(obs_ledger.new_rows),
        "observations_in_output": len(all_rows),
        "outcome_bindings_emitted": 0,
        "outcome_bindings_in_output": len(bind_ledger.rows()),
        "per_record_source_ids": [row["source_ids"][0] for row in obs_ledger.new_rows]}
    receipt["missing_versions"] = missing_versions
    receipt["anchoring_counters"] = counters
    receipt["emitted_files"] = [
        {"path": args.output_observations, "kind": "observations", "records": len(all_rows),
         "sha256": common.sha256_file(Path(args.output_observations))},
        {"path": args.output_bindings, "kind": "outcome_bindings", "records": 0,
         "sha256": common.sha256_file(Path(args.output_bindings))}]
    receipt["cannot_check"] = [
        "arXiv Atom metadata exposes no affiliations -> institution_ids stay empty",
        "no stable team identities in Atom metadata -> team_id stays empty",
        "no citation counts; version progression is not an outcome",
        "a requested versioned id absent from the response is listed in "
        "missing_versions (honest censoring), never invented",
        "versions of records whose head is v1 have no within-trajectory history "
        "in this source (single-deposit censoring)"]
    return receipt


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent-observations", required=True,
                        help="SD10 arxiv_obs.jsonl (head-version observations)")
    parser.add_argument("--output-observations", required=True)
    parser.add_argument("--output-bindings", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--since", required=True, help="SD10 parent-selection window start (bookkeeping)")
    parser.add_argument("--until", required=True, help="SD10 parent-selection window end (bookkeeping)")
    parser.add_argument("--max-records", type=int, default=100000,
                        help="cap on parent trajectories processed")
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--contact-email", default="")
    parser.add_argument("--rate-seconds", type=float, default=DEFAULT_RATE_SECONDS)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--backoff-cap", type=float, default=120.0,
                        help="max seconds between retries (429/5xx backoff)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    args.contact_email = args.contact_email or os.environ.get("SD10_CONTACT_EMAIL", "")
    common.parse_iso_date(args.since, "since")
    common.parse_iso_date(args.until, "until")
    if args.rate_seconds < DEFAULT_RATE_SECONDS:
        raise SystemExit(f"--rate-seconds must be >= {DEFAULT_RATE_SECONDS} for arXiv API etiquette")
    if args.batch_size < 1 or args.batch_size > 100:
        raise SystemExit("--batch-size must be within 1..100")
    try:
        receipt = run(args)
    except common.HardFailClosed as exc:
        partial = common.base_receipt(
            source_id=SOURCE_ID, source_mode_id=SOURCE_MODE_ID,
            lineage=["arXiv Atom metadata API (public, documented), versioned id_list mode"],
            endpoints=[ENDPOINT], terms_note=TERMS_NOTE, rate_note=RATE_NOTE,
            dry_run=False, since=args.since, until=args.until, max_records=args.max_records)
        partial["error_log"].append(str(exc))
        partial["failed_closed"] = True
        common.write_receipt(Path(args.receipt), partial)
        print(json.dumps({"failed_closed": True, "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2
    common.write_receipt(Path(args.receipt), receipt)
    print(json.dumps({"observations": receipt["records"]["observations_emitted"] if not args.dry_run
                      else receipt["plan"]["version_targets"],
                      "requests": receipt.get("request_count", 0),
                      "plan": receipt.get("plan"), "dry_run": args.dry_run}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

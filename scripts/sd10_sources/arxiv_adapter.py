#!/usr/bin/env python3
"""SD10 lawful source adapter: arXiv Atom metadata API -> development observations.

Lawful acquisition contract (research/closure/SD10_SOURCE_ADAPTERS_DESIGN_RECEIPT_V1.md):
- Uses ONLY the public arXiv Atom metadata API (export.arxiv.org/api/query), which
  arXiv documents for programmatic metadata access under its API terms of use
  (https://info.arxiv.org/help/api/tou.html): no more than one request every
  3 seconds, one connection at a time, and a descriptive User-Agent that
  identifies the caller and includes contact information.
- Default rate interval is therefore 3.0s (configurable only upward via
  --rate-seconds; the CLI rejects a smaller value for this source).
- --since/--until filter on submittedDate; --max-records caps the run;
  --dry-run prints the plan and performs zero requests.
- HTTP 4xx other than 429 fails closed (HardFailClosed); 429/5xx back off.

Scientific honesty contract:
- arXiv metadata carries NO validated scientific outcome. This adapter NEVER
  emits an outcome binding. Version progression (v1 -> v2 -> ...) is recorded
  as VERSION_OR_REVISION observations, never as an outcome.
- Author counts are proxy metrics only. The Atom API exposes no affiliations,
  citation counts, or stable team identities (recorded as CANNOT_CHECK in the
  receipt), so institution_ids/team_id stay empty rather than guessed.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

if __package__ in (None, ""):  # pragma: no cover - direct script execution
    if "sd10_sources_common" not in sys.modules:
        _spec = importlib.util.spec_from_file_location(
            "sd10_sources_common", Path(__file__).resolve().parent / "common.py")
        _module = importlib.util.module_from_spec(_spec)
        sys.modules["sd10_sources_common"] = _module
        _spec.loader.exec_module(_module)
    common = sys.modules["sd10_sources_common"]
else:  # pragma: no cover
    from . import common

from orion_v2.scientific_development_sources import DevelopmentObservation, ObservationKind

SOURCE_ID = "arxiv"
SOURCE_MODE_ID = "arxiv_atom_metadata"
ENDPOINT = "https://export.arxiv.org/api/query"
TERMS_NOTE = (
    "arXiv public Atom metadata API; terms of use ask for <=1 request per 3 "
    "seconds, a single connection, and a descriptive User-Agent with contact "
    "information (https://info.arxiv.org/help/api/tou.html). Metadata is "
    "redistribution-compatible with attribution; no fulltext is fetched."
)
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
RATE_NOTE = "arXiv API etiquette: min interval 3.0s enforced (>= documented 1 req/3s), UA carries contact email"
DEFAULT_RATE_SECONDS = 3.0


def build_search_query(since: str, until: str, category: str) -> str:
    window = f"submittedDate:[{since.replace('-', '')}0000 TO {until.replace('-', '')}2359]"
    return f"cat:{category} AND {window}" if category else window


def plan_requests(args) -> list[str]:
    """Deterministic URL plan; --dry-run prints this without any network use."""
    urls = []
    start = int(args.state_start or 0)
    remaining = args.max_records
    while remaining > 0:
        page = min(args.page_size, remaining)
        urls.append(ENDPOINT + "?" + urllib.parse.urlencode({
            "search_query": build_search_query(args.since, args.until, args.category),
            "sortBy": "submittedDate", "sortOrder": "ascending",
            "start": start, "max_results": page}))
        start += page
        remaining -= page
    return urls


def parse_feed(body: bytes) -> tuple[list[dict], int]:
    """Parse an arXiv Atom feed page into entry dicts + total_results."""
    root = ET.fromstring(body)
    total = root.findtext(f"{ATOM}totalResults", default="0")
    entries = []
    for entry in root.findall(f"{ATOM}entry"):
        raw_id = (entry.findtext(f"{ATOM}id") or "").strip()
        arxiv_id = raw_id.rsplit("/abs/", 1)[-1]
        if not arxiv_id:
            continue
        version = 1
        if "v" in arxiv_id.rsplit(".", 1)[-1]:
            tail = arxiv_id.rsplit("v", 1)[-1]
            if tail.isdigit():
                version = int(tail)
                arxiv_id = arxiv_id.rsplit("v", 1)[0]
        authors = [node.findtext(f"{ATOM}name", default="").strip() for node in entry.findall(f"{ATOM}author")]
        primary = entry.find(f"{ARXIV}primary_category")
        categories = [c.get("term", "") for c in entry.findall(f"{ATOM}category")]
        entries.append({
            "arxiv_id": arxiv_id, "version": version, "raw_id": raw_id,
            "published": entry.findtext(f"{ATOM}published", default="")[:10],
            "primary_category": primary.get("term", "") if primary is not None else (categories[0] if categories else ""),
            "author_count": sum(1 for name in authors if name),
            "title": (entry.findtext(f"{ATOM}title", default="") or "").strip(),
        })
    return entries, int(total)


def check_atom_error(entries: list[dict], titles: list[str]) -> None:
    if len(entries) == 1 and titles and titles[0].lower() == "error":
        raise common.HardFailClosed("arXiv Atom API returned an error entry; failing closed")


def to_observation(entry: dict) -> DevelopmentObservation:
    version = entry["version"]
    kind = ObservationKind.VERSION_OR_REVISION if version > 1 else ObservationKind.OTHER
    return DevelopmentObservation(
        observation_id=f"arxiv-obs:{entry['arxiv_id']}v{version}",
        trajectory_id=f"arxiv:{entry['arxiv_id']}",
        domain_id=f"arxiv-cat:{entry['primary_category'] or 'uncategorized'}",
        epoch_id=f"year:{entry['published'][:4] or 'unknown'}",
        source_mode_id=SOURCE_MODE_ID,
        ordinal=max(0, version - 1),
        kind=kind,
        action_feature_ids=("arxiv:deposit_version", f"arxiv:primary_category:{entry['primary_category'] or 'uncategorized'}"),
        source_ids=(entry["raw_id"],),
        proxy_metrics=(("arxiv:author_count", float(entry["author_count"])),),
        bias_flag_ids=(common.BIAS_PUBLICATION, common.BIAS_SURVIVORSHIP, common.BIAS_LANGUAGE_GEOGRAPHY),
    )


def run(args, transport=None, sleep=None) -> dict:
    sleep = sleep or (lambda seconds: __import__("time").sleep(seconds))
    transport = transport or common.UrllibTransport(timeout=args.timeout)
    receipt = common.base_receipt(
        source_id=SOURCE_ID, source_mode_id=SOURCE_MODE_ID,
        lineage=["arXiv Atom metadata API (public, documented)", "SD10 adapter: scripts/sd10_sources/arxiv_adapter.py"],
        endpoints=[ENDPOINT], terms_note=TERMS_NOTE, rate_note=RATE_NOTE,
        dry_run=args.dry_run, since=args.since, until=args.until, max_records=args.max_records)
    state = common.CursorState(Path(args.state))
    headers = {"User-Agent": f"ORION-V2-SD10-research-metadata-harvester (mailto:{args.contact_email})"}
    limiter = common.RateLimiter(args.rate_seconds, sleep)
    observations: list[DevelopmentObservation] = []
    urls = plan_requests(args)
    receipt["planned_urls"] = urls
    if args.dry_run:
        receipt["dry_run_plan"] = {
            "requests_planned": len(urls), "window": [args.since, args.until],
            "note": "dry run: zero network requests were made"}
        return receipt
    if not args.contact_email:
        raise SystemExit("arXiv API etiquette requires a descriptive contact email: --contact-email or SD10_CONTACT_EMAIL")
    start = int((state.data.get("cursor") or {"start": 0})["start"])
    already = int(state.data.get("records_emitted", 0))
    fetched_any = False
    while len(observations) < args.max_records:
        page = min(args.page_size, args.max_records - len(observations))
        url = ENDPOINT + "?" + urllib.parse.urlencode({
            "search_query": build_search_query(args.since, args.until, args.category),
            "sortBy": "submittedDate", "sortOrder": "ascending",
            "start": start, "max_results": page})
        response = common.fetch_with_retry(
            transport, url, headers, rate_limiter=limiter, sleep=sleep, retries=args.retries)
        receipt["request_count"] += 1
        fetched_any = True
        entries, _total = parse_feed(response.body)
        titles = [entry["title"] for entry in entries]
        check_atom_error(entries, titles)
        if not entries:
            break
        for entry in entries:
            if len(observations) < args.max_records:
                observations.append(to_observation(entry))
        start += page
        state.advance({"start": start}, already + len(observations))
        if len(entries) < page:
            break
    if not fetched_any:
        receipt["error_log"].append("no page fetched")
    rows = [common.observation_to_json(obs) for obs in observations]
    common.write_jsonl(Path(args.output_observations), rows)
    common.write_jsonl(Path(args.output_bindings), [])
    receipt["pages"] = state.data.get("pages_fetched", 0)
    receipt["records"] = {
        "observations_emitted": len(rows), "outcome_bindings_emitted": 0,
        "per_record_source_ids": [row["source_ids"][0] for row in rows]}
    receipt["emitted_files"] = [
        {"path": args.output_observations, "kind": "observations", "records": len(rows),
         "sha256": common.sha256_file(Path(args.output_observations))},
        {"path": args.output_bindings, "kind": "outcome_bindings", "records": 0,
         "sha256": common.sha256_file(Path(args.output_bindings))}]
    receipt["cannot_check"] = [
        "arXiv Atom metadata exposes no affiliations -> institution_ids stay empty",
        "no stable team identities in Atom metadata -> team_id stays empty",
        "no citation counts -> no citation-window proxy; version progression is not an outcome",
        "unpublished/withdrawn-without-record lines are absent-by-censoring"]
    return receipt


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-observations", required=True)
    parser.add_argument("--output-bindings", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--since", required=True)
    parser.add_argument("--until", required=True)
    parser.add_argument("--max-records", type=int, default=200)
    parser.add_argument("--category", default="")
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--contact-email", default="")
    parser.add_argument("--rate-seconds", type=float, default=DEFAULT_RATE_SECONDS)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--state-start", type=int, default=0)
    args = parser.parse_args(argv)
    args.contact_email = args.contact_email or os.environ.get("SD10_CONTACT_EMAIL", "")
    common.parse_iso_date(args.since, "since")
    common.parse_iso_date(args.until, "until")
    if args.rate_seconds < DEFAULT_RATE_SECONDS:
        raise SystemExit(f"--rate-seconds must be >= {DEFAULT_RATE_SECONDS} for arXiv API etiquette")
    try:
        receipt = run(args)
    except common.HardFailClosed as exc:
        partial = common.base_receipt(
            source_id=SOURCE_ID, source_mode_id=SOURCE_MODE_ID,
            lineage=["arXiv Atom metadata API (public, documented)"], endpoints=[ENDPOINT],
            terms_note=TERMS_NOTE, rate_note=RATE_NOTE, dry_run=False,
            since=args.since, until=args.until, max_records=args.max_records)
        partial["error_log"].append(str(exc))
        partial["failed_closed"] = True
        common.write_receipt(Path(args.receipt), partial)
        print(json.dumps({"failed_closed": True, "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2
    common.write_receipt(Path(args.receipt), receipt)
    print(json.dumps({"observations": receipt["records"]["observations_emitted"],
                      "outcome_bindings": 0, "requests": receipt["request_count"],
                      "dry_run": args.dry_run}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


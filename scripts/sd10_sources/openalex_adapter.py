#!/usr/bin/env python3
"""SD10 lawful source adapter: OpenAlex /works -> observations + outcome bindings.

Lawful acquisition contract (research/closure/SD10_SOURCE_ADAPTERS_DESIGN_RECEIPT_V1.md):
- Uses ONLY the public OpenAlex REST API /works endpoint documented at
  https://docs.openalex.org/api-entities/works with its etiquette guidance:
  OpenAlex documents a daily request limit (100,000 calls/day) and asks for a
  mailto contact in the User-Agent to route to the polite pool.
- The adapter enforces BOTH a conservative default interval (1.0s) and a hard
  daily request budget (--daily-request-cap, default 100000, clamped to the
  documented limit): the run stops before exceeding the budget and says so in
  the receipt. Real (non-dry) runs REQUIRE --contact-email.
- --since/--until map to from_publication_date/until_publication_date filters;
  --max-records caps; --dry-run prints the plan and performs zero requests;
  HTTP 4xx (except 429) fails closed.

Scientific honesty contract:
- cited_by_count is a PROXY METRIC ONLY and is never mapped to an outcome class.
- An outcome binding is emitted ONLY when the record itself carries
  "is_retracted": true (VALIDATED_FAILURE, witness = the OpenAlex work record).
  Absence of the flag is NEVER a success: unbound trajectories stay UNKNOWN.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import urllib.parse
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

from orion_v2.scientific_development import DevelopmentOutcomeClass
from orion_v2.scientific_development_sources import DevelopmentObservation, ObservationKind, OutcomeBinding

SOURCE_ID = "openalex"
SOURCE_MODE_ID = "openalex_works"
ENDPOINT = "https://api.openalex.org/works"
TERMS_NOTE = (
    "OpenAlex public REST API /works; data is CC0 per OpenAlex documentation, "
    "retrieved with a descriptive mailto User-Agent under the documented daily "
    "request limit. No fulltext is fetched. https://docs.openalex.org"
)
RATE_NOTE = ("OpenAlex etiquette: mailto UA, default 1.0s min interval, hard "
             "daily request budget clamped to the documented 100000 calls/day")
DEFAULT_RATE_SECONDS = 1.0
DOCUMENTED_DAILY_LIMIT = 100000


def build_url(args, cursor: str | None, per_page: int) -> str:
    filters = [f"from_publication_date:{args.since}", f"until_publication_date:{args.until}"]
    if args.work_type:
        filters.append(f"type:{args.work_type}")
    params = {"filter": ",".join(filters), "per-page": str(per_page)}
    if cursor:
        params["cursor"] = cursor
    if args.contact_email:
        params["mailto"] = args.contact_email
    return ENDPOINT + "?" + urllib.parse.urlencode(params)


def work_id(item: dict) -> str:
    raw = str(item.get("id", ""))
    return raw.rsplit("/", 1)[-1] if raw else ""


def domain_id(item: dict) -> str:
    topic = item.get("primary_topic") or {}
    field_id = (topic.get("field") or {}).get("id") if isinstance(topic, dict) else None
    if field_id:
        return f"openalex-field:{str(field_id).rsplit('/', 1)[-1]}"
    source = ((item.get("primary_location") or {}).get("source") or {})
    if source.get("id"):
        return f"openalex-source:{str(source['id']).rsplit('/', 1)[-1]}"
    return "openalex-field:uncategorized"


def to_observation(item: dict, ordinal: int) -> DevelopmentObservation:
    wid = work_id(item)
    work_type = str(item.get("type", "unknown"))
    year = item.get("publication_year")
    institutions = sorted({
        f"openalex-inst:{str(inst['id']).rsplit('/', 1)[-1]}"
        for authorship in item.get("authorships", []) or []
        for inst in authorship.get("institutions", []) or [] if inst.get("id")})
    kind = ObservationKind.DATA_OR_INSTRUMENT if work_type == "dataset" else ObservationKind.OTHER
    failures = ("openalex:is_retracted",) if item.get("is_retracted") else ()
    return DevelopmentObservation(
        observation_id=f"openalex-obs:{wid}",
        trajectory_id=f"openalex:{wid}",
        domain_id=domain_id(item),
        epoch_id=f"year:{year or 'unknown'}",
        source_mode_id=SOURCE_MODE_ID,
        ordinal=ordinal,
        kind=kind,
        action_feature_ids=("openalex:publish_work", f"openalex:type:{work_type}"),
        failure_feature_ids=failures,
        source_ids=(f"openalex:{wid}",),
        institution_ids=tuple(institutions),
        proxy_metrics=(
            ("openalex:cited_by_count", float(item.get("cited_by_count", 0) or 0)),
            ("openalex:referenced_works_count", float(item.get("referenced_works_count", 0) or 0)),
            ("openalex:author_count", float(len(item.get("authorships", []) or []))),
        ),
        bias_flag_ids=(common.BIAS_PUBLICATION, common.BIAS_SURVIVORSHIP,
                       common.BIAS_CITATION_WINDOW, common.BIAS_LANGUAGE_GEOGRAPHY),
    )
def bindings_from_items(items: list[dict]) -> list[OutcomeBinding]:
    """Validated-failure bindings ONLY from the source-carried is_retracted flag.

    The witness is the OpenAlex work record itself (the record that carries the
    validated failure evidence). Absence of the flag NEVER yields a binding and
    is NEVER a success.
    """
    bindings = []
    for item in items:
        wid = work_id(item)
        if wid and item.get("is_retracted"):
            bindings.append(OutcomeBinding(
                trajectory_id=f"openalex:{wid}",
                outcome_class=DevelopmentOutcomeClass.VALIDATED_FAILURE,
                witness_ids=(f"openalex:{wid}",), source_ids=(f"openalex:{wid}",)))
    return bindings


def run(args, transport=None, sleep=None) -> dict:
    sleep = sleep or (lambda seconds: __import__("time").sleep(seconds))
    transport = transport or common.UrllibTransport(timeout=args.timeout)
    daily_cap = min(args.daily_request_cap, DOCUMENTED_DAILY_LIMIT)
    receipt = common.base_receipt(
        source_id=SOURCE_ID, source_mode_id=SOURCE_MODE_ID,
        lineage=["OpenAlex REST /works (public, documented, CC0 metadata)",
                 "SD10 adapter: scripts/sd10_sources/openalex_adapter.py"],
        endpoints=[ENDPOINT], terms_note=TERMS_NOTE, rate_note=RATE_NOTE,
        dry_run=args.dry_run, since=args.since, until=args.until, max_records=args.max_records)
    receipt["daily_request_budget"] = {"cap": daily_cap, "documented_limit": DOCUMENTED_DAILY_LIMIT}
    if args.dry_run:
        receipt["dry_run_plan"] = {
            "requests_planned": 1, "sample_url": build_url(args, cursor="START_CURSOR",
                                                           per_page=min(args.page_size, args.max_records)),
            "note": "dry run: zero network requests were made"}
        return receipt
    if not args.contact_email:
        raise SystemExit("OpenAlex etiquette requires a mailto contact: --contact-email or SD10_CONTACT_EMAIL")
    state = common.CursorState(Path(args.state))
    headers = {"User-Agent": f"ORION-V2-SD10-research-metadata-harvester (mailto:{args.contact_email})"}
    limiter = common.RateLimiter(args.rate_seconds, sleep)
    cursor = state.data.get("cursor")
    already = int(state.data.get("records_emitted", 0))
    requests_today = int(state.data.get("requests_today", 0))
    observations: list[DevelopmentObservation] = []
    bindings: list[OutcomeBinding] = []
    while len(observations) < args.max_records:
        if requests_today + 1 > daily_cap:
            receipt["error_log"].append(
                f"daily request budget reached ({requests_today}/{daily_cap}); stopping before exceeding documented limit")
            break
        per_page = min(args.page_size, args.max_records - len(observations))
        url = build_url(args, cursor, per_page)
        response = common.fetch_with_retry(
            transport, url, headers, rate_limiter=limiter, sleep=sleep, retries=args.retries)
        receipt["request_count"] += 1
        requests_today += 1
        state.data["requests_today"] = requests_today
        payload = json.loads(response.body.decode("utf-8"))
        items = payload.get("results", [])
        if not items:
            break
        for item in items:
            if len(observations) < args.max_records:
                observations.append(to_observation(item, len(observations)))
                bindings.extend(bindings_from_items([item]))
        cursor = (payload.get("meta") or {}).get("next_cursor") or cursor
        state.advance(cursor, already + len(observations))
        if len(items) < per_page:
            break
    rows_out = [common.observation_to_json(obs) for obs in observations]
    binding_rows = [common.binding_to_json(binding) for binding in bindings]
    common.write_jsonl(Path(args.output_observations), rows_out)
    common.write_jsonl(Path(args.output_bindings), binding_rows)
    receipt["pages"] = state.data.get("pages_fetched", 0)
    receipt["records"] = {
        "observations_emitted": len(rows_out), "outcome_bindings_emitted": len(binding_rows),
        "per_record_source_ids": [row["source_ids"][0] for row in rows_out]}
    receipt["emitted_files"] = [
        {"path": args.output_observations, "kind": "observations", "records": len(rows_out),
         "sha256": common.sha256_file(Path(args.output_observations))},
        {"path": args.output_bindings, "kind": "outcome_bindings", "records": len(binding_rows),
         "sha256": common.sha256_file(Path(args.output_bindings))}]
    receipt["cannot_check"] = [
        "cited_by_count is truncated at fetch date (citation-window bias is structural)",
        "OpenAlex coverage of non-English and regional venues is incomplete (language/geography skew)",
        "authorships without institution ids keep institution_ids empty (not asserted)",
        "withdrawn works without the is_retracted flag cannot be detected here"]
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
    parser.add_argument("--work-type", default="")
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--contact-email", default="")
    parser.add_argument("--rate-seconds", type=float, default=DEFAULT_RATE_SECONDS)
    parser.add_argument("--daily-request-cap", type=int, default=DOCUMENTED_DAILY_LIMIT)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    args.contact_email = args.contact_email or os.environ.get("SD10_CONTACT_EMAIL", "")
    common.parse_iso_date(args.since, "since")
    common.parse_iso_date(args.until, "until")
    try:
        receipt = run(args)
    except common.HardFailClosed as exc:
        partial = common.base_receipt(
            source_id=SOURCE_ID, source_mode_id=SOURCE_MODE_ID,
            lineage=["OpenAlex REST /works (public, documented, CC0 metadata)"], endpoints=[ENDPOINT],
            terms_note=TERMS_NOTE, rate_note=RATE_NOTE, dry_run=False,
            since=args.since, until=args.until, max_records=args.max_records)
        partial["error_log"].append(str(exc))
        partial["failed_closed"] = True
        common.write_receipt(Path(args.receipt), partial)
        print(json.dumps({"failed_closed": True, "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2
    common.write_receipt(Path(args.receipt), receipt)
    print(json.dumps({"observations": receipt["records"]["observations_emitted"],
                      "outcome_bindings": receipt["records"]["outcome_bindings_emitted"],
                      "requests": receipt["request_count"], "dry_run": args.dry_run}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


#!/usr/bin/env python3
"""SD10 lawful source adapter: Crossref REST /works -> observations + outcome bindings.

Lawful acquisition contract (research/closure/SD10_SOURCE_ADAPTERS_DESIGN_RECEIPT_V1.md):
- Uses ONLY the public Crossref REST API /works endpoint documented at
  https://api.crossref.org/swagger-ui/index.html with the etiquette/polite-pool
  guidance (https://www.crossref.org/documentation/retrieve-metadata/rest-api/):
  send a User-Agent identifying the caller with a mailto contact to join the
  polite pool. Real (non-dry) runs therefore REQUIRE --contact-email.
- Conservative default interval 1.0s between requests (well inside Crossref's
  documented polite-pool expectations), deep paging via the documented cursor
  protocol: the first request sends cursor=* and every later request repeats
  the message.next-cursor value; `offset` is never sent (the API documents that
  offset cannot be combined with cursor).
- --since/--until map to from-pub-date/until-pub-date filters; --max-records caps;
  --dry-run prints the plan and performs zero requests; HTTP 4xx (except 429)
  fails closed.

Scientific honesty contract:
- is-referenced-by-count and reference counts are PROXY METRICS ONLY and are
  never mapped to an outcome class.
- Outcome bindings are emitted ONLY where the source itself carries a validated
  failure witness: a retraction notice record whose documented `update-to`
  array contains an entry with type "retraction" binds the RETRACTED
  trajectory to VALIDATED_FAILURE, with the retraction notice DOI as witness
  id. Verified against the live API (2026-08-29): `update-to` is the only
  source-carried retraction channel — the current API has no `is-retracted`
  field and no retraction relation type in its documented enum. Corrections
  and other update types do NOT bind. Absence of such records is NEVER a
  success: unbound trajectories stay UNKNOWN.
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

SOURCE_ID = "crossref"
SOURCE_MODE_ID = "crossref_rest_works"
ENDPOINT = "https://api.crossref.org/works"
TERMS_NOTE = (
    "Crossref public REST API /works; metadata retrieved via the documented "
    "polite pool (User-Agent with mailto contact). Crossref metadata may be "
    "used with attribution; no fulltext is fetched. "
    "https://www.crossref.org/documentation/retrieve-metadata/rest-api/"
)
RATE_NOTE = "Crossref polite pool: descriptive UA with mailto, default 1.0s min interval, documented cursor deep paging"
DEFAULT_RATE_SECONDS = 1.0


def build_url(args, cursor: str | None, rows: int) -> str:
    filters = [f"from-pub-date:{args.since}", f"until-pub-date:{args.until}"]
    if args.work_type:
        filters.append(f"type:{args.work_type}")
    # Documented cursor protocol: first request sends cursor=*, later requests
    # repeat message.next-cursor. `offset` must never appear alongside `cursor`.
    params = {"filter": ",".join(filters), "rows": str(rows), "cursor": cursor or "*"}
    if args.contact_email:
        params["mailto"] = args.contact_email
    return ENDPOINT + "?" + urllib.parse.urlencode(params)


def retraction_targets(item: dict) -> list[str]:
    """DOIs this record retracts, from the documented `update-to` array.

    Verified against live api.crossref.org responses (2026-08-29): a retraction
    notice carries `update-to: [{DOI, type: "retraction", label, source,
    updated, record-id}, ...]` pointing at the retracted work. The current API
    has no `is-retracted` boolean and its documented relation-type enum contains
    no retraction relation, so this is the only source-carried retraction
    channel. Only type "retraction" binds; corrections do not.
    """
    targets = []
    updates = item.get("update-to") or []
    if isinstance(updates, list):
        for entry in updates:
            if (isinstance(entry, dict) and str(entry.get("type", "")).lower() == "retraction"
                    and entry.get("DOI")):
                targets.append(str(entry["DOI"]).lower())
    return sorted(set(targets))


def to_observation(item: dict, ordinal: int) -> DevelopmentObservation:
    doi = str(item.get("DOI", "")).lower()
    work_type = str(item.get("type", "unknown"))
    published = ""
    for key in ("published", "issued", "created"):
        parts = item.get(key, {}).get("date-parts", [[None]])
        if parts and parts[0] and parts[0][0]:
            published = str(parts[0][0])
            break
    subjects = [str(s) for s in item.get("subject", []) if str(s).strip()]
    institution = ""
    raw_institution = item.get("institution") or []
    if isinstance(raw_institution, list) and raw_institution and isinstance(raw_institution[0], dict):
        institution = str(raw_institution[0].get("name", "")).strip()
    kind = ObservationKind.DATA_OR_INSTRUMENT if work_type == "dataset" else (
        ObservationKind.RETRACTION if retraction_targets(item) else ObservationKind.OTHER)
    failures: tuple[str, ...] = ("crossref:retraction_notice",) if retraction_targets(item) else ()
    return DevelopmentObservation(
        observation_id=f"crossref-obs:{doi}",
        trajectory_id=f"doi:{doi}",
        domain_id=f"crossref-subject:{subjects[0] if subjects else 'uncategorized'}",
        epoch_id=f"year:{published or 'unknown'}",
        source_mode_id=SOURCE_MODE_ID,
        ordinal=ordinal,
        kind=kind,
        action_feature_ids=("crossref:publish_work", f"crossref:type:{work_type}"),
        failure_feature_ids=failures,
        source_ids=(f"doi:{doi}",),
        institution_ids=(f"crossref-inst:{institution}",) if institution else (),
        proxy_metrics=(
            ("crossref:is_referenced_by_count", float(item.get("is-referenced-by-count", 0) or 0)),
            ("crossref:reference_count", float(item.get("reference-count", 0) or 0)),
            ("crossref:author_count", float(len(item.get("author", []) or []))),
        ),
        bias_flag_ids=(common.BIAS_PUBLICATION, common.BIAS_SURVIVORSHIP,
                       common.BIAS_CITATION_WINDOW, common.BIAS_LANGUAGE_GEOGRAPHY),
    )


def bindings_from_items(items: list[dict]) -> list[OutcomeBinding]:
    """Validated-failure bindings ONLY from source-carried retraction evidence.

    A notice record whose documented `update-to` array carries a type
    "retraction" entry binds the RETRACTED trajectory to VALIDATED_FAILURE;
    the witness is the retraction notice DOI (the record carrying the
    evidence). The retracted target record itself typically carries no marker
    in Crossref, which is exactly why the witness must be the notice.
    Absence of a retraction entry NEVER yields a binding and is NEVER a
    success: unbound trajectories stay UNKNOWN.
    """
    bindings: list[OutcomeBinding] = []
    for item in items:
        doi = str(item.get("DOI", "")).lower()
        if not doi:
            continue
        for target in retraction_targets(item):
            bindings.append(OutcomeBinding(
                trajectory_id=f"doi:{target}",
                outcome_class=DevelopmentOutcomeClass.VALIDATED_FAILURE,
                witness_ids=(f"doi:{doi}",), source_ids=(f"doi:{doi}",)))
    return bindings


def run(args, transport=None, sleep=None) -> dict:
    sleep = sleep or (lambda seconds: __import__("time").sleep(seconds))
    transport = transport or common.UrllibTransport(timeout=args.timeout)
    receipt = common.base_receipt(
        source_id=SOURCE_ID, source_mode_id=SOURCE_MODE_ID,
        lineage=["Crossref REST /works (public, documented, polite pool)",
                 "SD10 adapter: scripts/sd10_sources/crossref_adapter.py"],
        endpoints=[ENDPOINT], terms_note=TERMS_NOTE, rate_note=RATE_NOTE,
        dry_run=args.dry_run, since=args.since, until=args.until, max_records=args.max_records)
    if args.dry_run:
        plan = [build_url(args, cursor=None, rows=min(args.page_size, args.max_records))]
        receipt["dry_run_plan"] = {"requests_planned": 1, "sample_url": plan[0],
                                   "note": "dry run: zero network requests were made; sample_url uses the documented cursor=* start"}
        return receipt
    if not args.contact_email:
        raise SystemExit("Crossref polite pool requires a mailto contact: --contact-email or SD10_CONTACT_EMAIL")
    state = common.CursorState(Path(args.state))
    obs_ledger = common.OutputLedger(Path(args.output_observations), common.observation_key)
    bind_ledger = common.OutputLedger(Path(args.output_bindings), common.binding_key)
    headers = {"User-Agent": f"ORION-V2-SD10-research-metadata-harvester (mailto:{args.contact_email})"}
    limiter = common.RateLimiter(args.rate_seconds, sleep)
    cursor = state.data.get("cursor")
    already = int(state.data.get("records_emitted", 0))
    observations: list[DevelopmentObservation] = []
    bindings: list[OutcomeBinding] = []
    while len(observations) < args.max_records:
        rows = min(args.page_size, args.max_records - len(observations))
        url = build_url(args, cursor, rows)
        response = common.fetch_with_retry(
            transport, url, headers, rate_limiter=limiter, sleep=sleep, retries=args.retries)
        receipt["request_count"] += 1
        payload = json.loads(response.body.decode("utf-8"))
        message = payload.get("message", {})
        items = message.get("items", [])
        if not items:
            break
        for item in items:
            if len(observations) < args.max_records:
                observations.append(to_observation(item, already + len(observations)))
                bindings.extend(bindings_from_items([item]))
        # Durable output BEFORE the cursor advances: an interrupted run never
        # loses already-fetched records (resume merges instead of replacing).
        obs_ledger.add([common.observation_to_json(obs) for obs in observations])
        bind_ledger.add([common.binding_to_json(binding) for binding in bindings])
        cursor = message.get("next-cursor") or cursor
        state.advance(cursor, already + len(observations))
        if len(items) < rows:
            break
    obs_ledger.rewrite_atomically()
    bind_ledger.rewrite_atomically()
    receipt["pages"] = state.data.get("pages_fetched", 0)
    receipt["records"] = {
        "observations_emitted": len(obs_ledger.new_rows), "observations_in_output": len(obs_ledger.rows()),
        "outcome_bindings_emitted": len(bind_ledger.new_rows), "outcome_bindings_in_output": len(bind_ledger.rows()),
        "per_record_source_ids": [row["source_ids"][0] for row in obs_ledger.new_rows]}
    receipt["emitted_files"] = [
        {"path": args.output_observations, "kind": "observations", "records": len(obs_ledger.rows()),
         "sha256": common.sha256_file(Path(args.output_observations))},
        {"path": args.output_bindings, "kind": "outcome_bindings", "records": len(bind_ledger.rows()),
         "sha256": common.sha256_file(Path(args.output_bindings))}]
    receipt["cannot_check"] = [
        "citation counts are truncated at fetch date (citation-window bias is structural)",
        "author lists are not stable team identities -> team_id stays empty",
        "institutions appear only for some record types; absent means not indexed, not absent",
        "withdrawn items with no type=retraction update-to entry cannot be detected here"]
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
            lineage=["Crossref REST /works (public, documented, polite pool)"], endpoints=[ENDPOINT],
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


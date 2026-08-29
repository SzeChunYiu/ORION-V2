#!/usr/bin/env python3
"""SD10 lawful source adapter: NCBI E-utilities (PubMed/MEDLINE) -> observations + bindings.

Lawful acquisition contract (research/closure/SD10_SOURCE_ADAPTERS_DESIGN_RECEIPT_V1.md):
- Uses ONLY the public NCBI E-utilities documented at
  https://www.ncbi.nlm.nih.gov/books/NBK25499/ (esearch.fcgi / efetch.fcgi,
  db=pubmed). Documented etiquette: at most 3 requests per second WITHOUT an
  API key (no key is used here), so --rate-seconds defaults to 0.5 s and the
  CLI rejects anything below 0.334 s. A descriptive User-Agent with a mailto
  contact is sent; real (non-dry) runs therefore REQUIRE --contact-email.
- Two-stage documented protocol per page: esearch.fcgi (retmode=json) pages
  the PMID id list for the --since/--until window (mindate/maxdate with
  datetype=pdat, sort=pub_date, retstart/retmax), then ONE efetch.fcgi
  (retmode=xml) pulls the full PubMed records for exactly that page's PMIDs.
- Paging choice (recorded): stateless retstart/retmax paging, NOT
  usehistory/WebEnv server-side history. The documented history environment
  expires server-side, which cannot survive this lane's resumable-cursor
  contract (an interrupted run must resume from persisted state, not from a
  live server session); retstart paging re-runs the query deterministically
  (sort=pub_date) from the persisted retstart.
- Ceiling (live-verified 2026-08-29): ESearch rejects retstart > 9998 with
  HTTP 200 + esearchresult.ERROR ("... ESearch can only retrieve the first
  9,999 records matching the query..."). The adapter FAILS CLOSED on that
  ERROR key, on any short page while the esearch count still shows unconsumed
  records, and on any querytranslation echo that collapses the requested
  mindate:maxdate window to a single date; every page's count and
  querytranslation are recorded in the run receipt. Windows larger than 9,999
  records must be split into smaller date ranges by the operator.
- --max-records caps the run; --dry-run prints the URL plan and performs zero
  requests; HTTP 4xx (except 429) fails closed.

Scientific honesty contract:
- PubMed XML carries NO citation counts; none are invented. Author and MeSH
  heading counts are PROXY METRICS ONLY and never map to an outcome class.
- Outcome bindings are emitted ONLY where the record itself carries the
  validated failure witness: PublicationType "Retracted Publication" (live UI
  D016441, e.g. PMID 33522354, verified 2026-08-29) marks the RETRACTED
  article itself -> that trajectory binds VALIDATED_FAILURE with the pubmed
  record as its own witness. PublicationType "Retraction Notice" (live UI
  D016440, e.g. PMID 36017998; legacy vocabulary "Retraction of Publication"
  is also matched defensively) marks the retraction NOTICE -> an observation
  of kind RETRACTION with NO binding (the notice is not the failed work).
  Corrections/errata ("Published Erratum", UI D016425) do NOT bind. Records
  with no such PublicationType get no binding and stay UNKNOWN downstream;
  absence of a retraction is NEVER a success.
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

from orion_v2.scientific_development import DevelopmentOutcomeClass
from orion_v2.scientific_development_sources import DevelopmentObservation, ObservationKind, OutcomeBinding

SOURCE_ID = "pubmed"
SOURCE_MODE_ID = "pubmed_eutils_metadata"
ESEARCH_ENDPOINT = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_ENDPOINT = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
TERMS_NOTE = (
    "NCBI E-utilities (esearch.fcgi/efetch.fcgi, db=pubmed), the documented "
    "public programmatic interface to PubMed/MEDLINE "
    "(https://www.ncbi.nlm.nih.gov/books/NBK25499/). Documented etiquette: "
    "max 3 requests/second without an API key (none used); descriptive UA "
    "with mailto contact. MEDLINE/PubMed metadata retrieved per NLM terms; "
    "no fulltext is fetched."
)
RATE_NOTE = (
    "NCBI E-utilities etiquette: <=3 requests/second without an API key; "
    "default 0.5s min interval, CLI floor 0.334s; descriptive UA with mailto"
)
DEFAULT_RATE_SECONDS = 0.5
MIN_RATE_SECONDS = 0.334  # documented ceiling of 3 requests/second -> 1/3 s floor

# Publication-type TEXTS key the outcome policy (UIs are recorded, never
# keyed: the live UI assignment was verified to differ from the legacy one).
RETRACTED_PUBLICATION_PTS = {"retracted publication"}
RETRACTION_NOTICE_PTS = {"retraction notice", "retraction of publication"}
CORRECTION_PTS = {"published erratum"}


def build_esearch_url(args, retstart: int, retmax: int) -> str:
    """Documented date-window esearch: datetype=pdat + mindate/maxdate, sorted
    for deterministic stateless retstart/retmax paging."""
    params = {
        "db": "pubmed", "retmode": "json", "datetype": "pdat",
        "mindate": args.since.replace("-", "/"), "maxdate": args.until.replace("-", "/"),
        "sort": "pub_date", "retstart": str(retstart), "retmax": str(retmax)}
    return ESEARCH_ENDPOINT + "?" + urllib.parse.urlencode(params)


def build_efetch_url(pmids: list[str]) -> str:
    """One efetch per page for exactly that page's PMID set (retmode=xml)."""
    return EFETCH_ENDPOINT + "?" + urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"})


def check_esearch_error(payload: dict) -> None:
    # Live shape (verified 2026-08-29): esearchresult.errorlist is an object of
    # lists (phrasesnotfound/fieldsnotfound/...); any non-empty sub-list is a
    # real query error -> fail closed rather than silently fetching nothing.
    # esearchresult.ERROR is a separate TOP-LEVEL STRING returned with HTTP 200
    # (live-verified: retstart > 9998 -> "Search Backend failed: Exception:
    # 'retstart' cannot be larger than 9998. For PubMed, ESearch can only
    # retrieve the first 9,999 records matching the query...") -> also fail
    # closed, otherwise the ceiling would silently truncate a large window.
    result = payload.get("esearchresult", {})
    error = result.get("ERROR")
    if error:
        raise common.HardFailClosed(f"esearch returned ERROR: {error}; failing closed")
    errorlist = result.get("errorlist") or {}
    failures = {key: value for key, value in errorlist.items() if value}
    if failures:
        raise common.HardFailClosed(f"esearch returned an errorlist: {failures}; failing closed")


def parse_esearch_result(body: bytes) -> tuple[list[str], int, str]:
    """ids + window count + the server's own querytranslation echo."""
    payload = json.loads(body.decode("utf-8"))
    check_esearch_error(payload)
    result = payload.get("esearchresult", {})
    pmids = [str(pmid) for pmid in result.get("idlist", []) if str(pmid).strip()]
    try:
        count = int(result.get("count") or 0)
    except (TypeError, ValueError):
        count = 0
    return pmids, count, str(result.get("querytranslation") or "")


def check_window_translation(args, querytranslation: str) -> None:
    # Live-verified 2026-08-29 with this adapter's exact URL shape
    # (datetype=pdat + mindate + maxdate): the server echoes the window as
    # "<mindate>:<maxdate>[Date - Publication]" in querytranslation and applies
    # it (the 2024 window matches 1,739,765 records; the single-date query
    # matches 242,229). If the echo ever collapses to a single date the fetched
    # set would be the WRONG PMID set -> fail closed instead. Non-date queries
    # echo no date clause and pass untouched.
    if "[Date - Publication]" in querytranslation:
        expected = f"{args.since.replace('-', '/')}:{args.until.replace('-', '/')}[Date - Publication]"
        if expected not in querytranslation:
            raise common.HardFailClosed(
                f"esearch querytranslation {querytranslation!r} does not contain the requested "
                f"window {expected!r}; failing closed rather than fetching the wrong PMID set")


def _year_of(medline: ET.Element) -> str:
    # PubMed [dp]/pdat is MULTI-VALUED (live-verified 2026-08-29: PMIDs
    # 33522354 and 42493777 each match BOTH their electronic and print years
    # via "<uid>[UID] AND <year>[dp]"). The epoch therefore pins the FIRST
    # PUBLIC APPEARANCE channel: Article/ArticleDate Year (electronic
    # publication — a direct child of Article, no ArticleDateList wrapper in
    # live XML; ahead-of-print records carry the window-matching pdat here
    # while the Journal PubDate still holds the future print year), else the
    # citation PubDate Year, else the leading year of MedlineDate, else "".
    text = (medline.findtext("Article/ArticleDate/Year") or "").strip()
    if text[:4].isdigit():
        return text[:4]
    for path in ("Article/Journal/JournalIssue/PubDate/Year", "Article/Journal/JournalIssue/PubDate/MedlineDate"):
        text = (medline.findtext(path) or "").strip()
        if text[:4].isdigit():
            return text[:4]
    return ""


def parse_pubmed_articles(body: bytes) -> list[dict]:
    """Parse an efetch PubmedArticleSet into normalized record dicts.

    Element paths verified against live efetch responses on 2026-08-29
    (trimmed copies are the fixtures): PMID comes from MedlineCitation/PMID
    (NOT //PMID: CommentsCorrections also carries PMID elements);
    PublicationType text+UI from Article/PublicationTypeList; MeSH descriptor
    UI from MeshHeadingList/MeshHeading/DescriptorName (absent on
    In-Process/PubMed-not-MEDLINE records); journal identity from
    MedlineJournalInfo/NlmUniqueID; affiliations from
    AuthorList/Author/AffiliationInfo/Affiliation.
    """
    root = ET.fromstring(body)
    records = []
    for article in root.findall("PubmedArticle"):
        medline = article.find("MedlineCitation")
        if medline is None:
            continue
        pmid = (medline.findtext("PMID") or "").strip()
        if not pmid:
            continue
        pubtypes = []
        for node in medline.findall("Article/PublicationTypeList/PublicationType"):
            text = (node.text or "").strip()
            if text:
                pubtypes.append((str(node.get("UI", "") or ""), text))
        descriptor = medline.find("MeshHeadingList/MeshHeading/DescriptorName")
        mesh_ui = str(descriptor.get("UI", "")).strip() if descriptor is not None else ""
        records.append({
            "pmid": pmid,
            "pubtypes": pubtypes,
            "mesh_ui": mesh_ui,
            "mesh_heading_count": len(medline.findall("MeshHeadingList/MeshHeading")),
            "nlm_unique_id": (medline.findtext("MedlineJournalInfo/NlmUniqueID") or "").strip(),
            "author_count": len(medline.findall("Article/AuthorList/Author")),
            "affiliations": sorted({(node.text or "").strip() for node in
                                    medline.findall("Article/AuthorList/Author/AffiliationInfo/Affiliation")
                                    if (node.text or "").strip()}),
            "year": _year_of(medline),
        })
    return records


def _pubtype_texts(record: dict) -> set[str]:
    return {text.lower() for _ui, text in record["pubtypes"]}


def is_retracted_publication(record: dict) -> bool:
    return bool(_pubtype_texts(record) & RETRACTED_PUBLICATION_PTS)


def is_retraction_notice(record: dict) -> bool:
    return bool(_pubtype_texts(record) & RETRACTION_NOTICE_PTS)


def is_correction(record: dict) -> bool:
    return bool(_pubtype_texts(record) & CORRECTION_PTS)


def to_observation(record: dict, ordinal: int) -> DevelopmentObservation:
    pmid = record["pmid"]
    if record["mesh_ui"]:
        domain_id = f"pubmed-mesh:{record['mesh_ui']}"
    elif record["nlm_unique_id"]:
        domain_id = f"pubmed-journal:{record['nlm_unique_id']}"
    else:
        domain_id = "uncategorized"
    first_pubtype = record["pubtypes"][0][1] if record["pubtypes"] else "unknown"
    if is_retracted_publication(record) or is_retraction_notice(record):
        kind = ObservationKind.RETRACTION
    elif is_correction(record):
        kind = ObservationKind.CORRECTION
    else:
        kind = ObservationKind.OTHER
    failures: tuple[str, ...] = ()
    if is_retracted_publication(record):
        failures = ("pubmed:retracted_publication",)
    elif is_retraction_notice(record):
        failures = ("pubmed:retraction_notice",)
    return DevelopmentObservation(
        observation_id=f"pubmed-obs:{pmid}",
        trajectory_id=f"pubmed:{pmid}",
        domain_id=domain_id,
        epoch_id=f"year:{record['year'] or 'unknown'}",
        source_mode_id=SOURCE_MODE_ID,
        ordinal=ordinal,
        kind=kind,
        action_feature_ids=("pubmed:publish_work",
                            f"pubmed:pubtype:{first_pubtype.lower().replace(' ', '_')}"),
        failure_feature_ids=failures,
        source_ids=(f"pubmed:{pmid}",),
        institution_ids=tuple(f"pubmed-inst:{affiliation}" for affiliation in record["affiliations"]),
        proxy_metrics=(
            ("pubmed:author_count", float(record["author_count"])),
            ("pubmed:mesh_heading_count", float(record["mesh_heading_count"])),
        ),
        bias_flag_ids=(common.BIAS_PUBLICATION, common.BIAS_SURVIVORSHIP,
                       common.BIAS_LANGUAGE_GEOGRAPHY),
    )


def bindings_from_records(records: list[dict]) -> list[OutcomeBinding]:
    """Validated-failure bindings ONLY from the record's own PT witness.

    PublicationType "Retracted Publication" marks the retracted article
    ITSELF, so the trajectory binds VALIDATED_FAILURE with the pubmed record
    as its own witness. Retraction NOTICE records ("Retraction Notice" /
    legacy "Retraction of Publication") are the notices ABOUT a failure, not
    failed work, and bind nothing; the notice-to-target PMID link
    (CommentsCorrections RefType=RetractionOf) is not used to bind because
    the retracted record already carries its own PT witness. Corrections/
    errata never bind. Absence of the PT is NEVER a success: unbound
    trajectories stay UNKNOWN.
    """
    bindings: list[OutcomeBinding] = []
    for record in records:
        if is_retracted_publication(record):
            pmid = record["pmid"]
            bindings.append(OutcomeBinding(
                trajectory_id=f"pubmed:{pmid}",
                outcome_class=DevelopmentOutcomeClass.VALIDATED_FAILURE,
                witness_ids=(f"pubmed:{pmid}",), source_ids=(f"pubmed:{pmid}",)))
    return bindings


def plan_requests(args, retstart: int) -> list[str]:
    """Deterministic esearch URL plan; --dry-run prints this with no network use."""
    urls = []
    start, remaining = retstart, args.max_records
    while remaining > 0:
        page = min(args.page_size, remaining)
        urls.append(build_esearch_url(args, start, page))
        start += page
        remaining -= page
    return urls


def run(args, transport=None, sleep=None) -> dict:
    sleep = sleep or (lambda seconds: __import__("time").sleep(seconds))
    transport = transport or common.UrllibTransport(timeout=args.timeout)
    receipt = common.base_receipt(
        source_id=SOURCE_ID, source_mode_id=SOURCE_MODE_ID,
        lineage=["NCBI E-utilities esearch.fcgi/efetch.fcgi db=pubmed (public, documented)",
                 "SD10 adapter: scripts/sd10_sources/pubmed_adapter.py"],
        endpoints=[ESEARCH_ENDPOINT, EFETCH_ENDPOINT], terms_note=TERMS_NOTE, rate_note=RATE_NOTE,
        dry_run=args.dry_run, since=args.since, until=args.until, max_records=args.max_records)
    receipt["paging_protocol"] = {
        "mechanism": "stateless retstart/retmax with sort=pub_date (no usehistory/WebEnv)",
        "reason": "WebEnv history expires server-side and cannot satisfy the resumable-cursor contract; retstart paging re-runs the query deterministically from persisted state",
        "retstart_ceiling": ("live-verified 2026-08-29: ESearch rejects retstart > 9998 with HTTP 200 + "
                             "esearchresult.ERROR ('ESearch can only retrieve the first 9,999 records "
                             "matching the query'); the adapter fails closed on that ERROR and on any short "
                             "page while the esearch count shows unconsumed records — split larger windows "
                             "into smaller date ranges")}
    if args.dry_run:
        urls = plan_requests(args, retstart=0)
        receipt["planned_urls"] = urls
        receipt["dry_run_plan"] = {
            "requests_planned": len(urls), "sample_url": urls[0],
            "note": ("dry run: zero network requests were made; each planned esearch page "
                     "is followed by exactly one efetch whose id list comes from that page, "
                     "so the true request count is 2x requests_planned; if the window matches "
                     "more than 9,999 records and --max-records exceeds 9,999, the real run "
                     "will fail closed at the ESearch retstart ceiling (retstart <= 9998)")}
        return receipt
    if not args.contact_email:
        raise SystemExit("NCBI E-utilities etiquette requires a descriptive mailto contact: --contact-email or SD10_CONTACT_EMAIL")
    state = common.CursorState(Path(args.state))
    obs_ledger = common.OutputLedger(Path(args.output_observations), common.observation_key)
    bind_ledger = common.OutputLedger(Path(args.output_bindings), common.binding_key)
    headers = {"User-Agent": f"ORION-V2-SD10-research-metadata-harvester (mailto:{args.contact_email})"}
    limiter = common.RateLimiter(args.rate_seconds, sleep)
    retstart = int((state.data.get("cursor") or {"retstart": 0})["retstart"])
    already = int(state.data.get("records_emitted", 0))
    observations: list[DevelopmentObservation] = []
    bindings: list[OutcomeBinding] = []
    esearch_counts: list[int] = []
    esearch_querytranslations: list[str] = []
    while len(observations) < args.max_records:
        rows = min(args.page_size, args.max_records - len(observations))
        search_response = common.fetch_with_retry(
            transport, build_esearch_url(args, retstart, rows), headers,
            rate_limiter=limiter, sleep=sleep, retries=args.retries)
        receipt["request_count"] += 1
        pmids, window_count, querytranslation = parse_esearch_result(search_response.body)
        check_window_translation(args, querytranslation)
        esearch_counts.append(window_count)
        esearch_querytranslations.append(querytranslation)
        if not pmids:
            break
        fetch_response = common.fetch_with_retry(
            transport, build_efetch_url(pmids), headers,
            rate_limiter=limiter, sleep=sleep, retries=args.retries)
        receipt["request_count"] += 1
        records = parse_pubmed_articles(fetch_response.body)
        for record in records:
            if len(observations) < args.max_records:
                observations.append(to_observation(record, already + len(observations)))
                bindings.extend(bindings_from_records([record]))
        # Durable output BEFORE the cursor advances: an interrupted run never
        # loses already-fetched records (resume merges instead of replacing).
        obs_ledger.add([common.observation_to_json(obs) for obs in observations])
        bind_ledger.add([common.binding_to_json(binding) for binding in bindings])
        retstart_before = retstart
        retstart += len(pmids)
        state.advance({"retstart": retstart}, already + len(observations))
        if len(pmids) < rows and window_count > retstart_before + len(pmids):
            # A short page while the window count still shows unconsumed
            # records: the ESearch retstart ceiling (9,999 records, live error
            # text above) or index drift truncated the corpus — NEVER write a
            # success receipt over a partial fetch.
            raise common.HardFailClosed(
                f"esearch returned {len(pmids)} of {rows} requested PMIDs while the window count "
                f"{window_count} exceeds the {retstart_before + len(pmids)} consumed: the result set was "
                f"truncated (PubMed ESearch stateless paging cannot exceed the first 9,999 records of a "
                f"query; the index can also drift between pages) - split the date window into smaller "
                f"ranges; failing closed")
        if len(pmids) < rows:
            break
    receipt["esearch_window"] = {"counts_by_page": esearch_counts,
                                 "querytranslations": esearch_querytranslations}
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
        "PubMed XML carries no citation counts; none are invented (no citation-window proxy at all)",
        "author lists are not stable team identities -> team_id stays empty",
        "affiliations are free-text strings, not canonical institution identifiers",
        "MeSH headings exist only for indexed (MEDLINE) records; In-Process records fall back to journal identity",
        "retractions not yet flagged with the PublicationType are undetectable here"]
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
    if args.rate_seconds < MIN_RATE_SECONDS:
        raise SystemExit(
            f"--rate-seconds must be >= {MIN_RATE_SECONDS} (NCBI E-utilities document max 3 requests/second without an API key)")
    try:
        receipt = run(args)
    except common.HardFailClosed as exc:
        partial = common.base_receipt(
            source_id=SOURCE_ID, source_mode_id=SOURCE_MODE_ID,
            lineage=["NCBI E-utilities esearch.fcgi/efetch.fcgi db=pubmed (public, documented)"],
            endpoints=[ESEARCH_ENDPOINT, EFETCH_ENDPOINT],
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

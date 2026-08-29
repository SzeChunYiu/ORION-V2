"""Fixture-based tests for the SD10 lawful source adapters (no network access).

The adapters accept an injectable transport + sleep, so every test here drives
the real run() paths against embedded API-response fixtures under
tests/fixtures/sd10/. No test may open a socket.
"""
import argparse
import hashlib
import importlib.util
import json
import sys
import time
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from orion_v2.scientific_development import DevelopmentOutcomeClass
from orion_v2.scientific_development_sources import DevelopmentObservation, ObservationKind, OutcomeBinding, assemble_all

FIXTURES = Path(__file__).parents[1] / "fixtures" / "sd10"


def _load_shared_common():
    if "sd10_sources_common" not in sys.modules:
        path = Path(__file__).parents[2] / "scripts" / "sd10_sources" / "common.py"
        spec = importlib.util.spec_from_file_location("sd10_sources_common", path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["sd10_sources_common"] = module
        assert spec.loader is not None
        spec.loader.exec_module(module)
    return sys.modules["sd10_sources_common"]


common = _load_shared_common()


def _load(name: str):
    path = Path(__file__).parents[2] / "scripts" / "sd10_sources" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


arxiv = _load("arxiv_adapter")
crossref = _load("crossref_adapter")
openalex = _load("openalex_adapter")
pubmed = _load("pubmed_adapter")


class FakeTransport:
    def __init__(self, pages):
        self.pages = list(pages)
        self.urls = []

    def __call__(self, url, headers):
        self.urls.append(url)
        if not self.pages:
            return common.Response(200, b'{"message": {"items": []}, "meta": {}, "results": []}')
        page = self.pages.pop(0)
        return page() if callable(page) else page


class SleepRecorder:
    def __init__(self):
        self.calls: list[float] = []

    def __call__(self, seconds: float) -> None:
        self.calls.append(float(seconds))


def _arxiv_args(tmp_path, **overrides):
    base = dict(
        output_observations=str(tmp_path / "obs.jsonl"), output_bindings=str(tmp_path / "bind.jsonl"),
        receipt=str(tmp_path / "receipt.json"), state=str(tmp_path / "state.json"),
        since="2024-01-01", until="2024-12-31", max_records=5, category="", page_size=2,
        contact_email="orion-sd10@example.org", rate_seconds=3.0, timeout=5.0, retries=3,
        dry_run=False, state_start=0)
    base.update(overrides)
    return argparse.Namespace(**base)


def _crossref_args(tmp_path, **overrides):
    base = dict(
        output_observations=str(tmp_path / "obs.jsonl"), output_bindings=str(tmp_path / "bind.jsonl"),
        receipt=str(tmp_path / "receipt.json"), state=str(tmp_path / "state.json"),
        since="2024-01-01", until="2024-12-31", max_records=10, work_type="", page_size=100,
        contact_email="orion-sd10@example.org", rate_seconds=1.0, timeout=5.0, retries=3,
        dry_run=False)
    base.update(overrides)
    return argparse.Namespace(**base)


def _openalex_args(tmp_path, **overrides):
    base = dict(
        output_observations=str(tmp_path / "obs.jsonl"), output_bindings=str(tmp_path / "bind.jsonl"),
        receipt=str(tmp_path / "receipt.json"), state=str(tmp_path / "state.json"),
        since="2024-01-01", until="2024-12-31", max_records=10, work_type="", page_size=100,
        contact_email="orion-sd10@example.org", rate_seconds=1.0, daily_request_cap=100000,
        timeout=5.0, retries=3, dry_run=False)
    base.update(overrides)
    return argparse.Namespace(**base)


def _pubmed_args(tmp_path, **overrides):
    base = dict(
        output_observations=str(tmp_path / "obs.jsonl"), output_bindings=str(tmp_path / "bind.jsonl"),
        receipt=str(tmp_path / "receipt.json"), state=str(tmp_path / "state.json"),
        since="2024-01-01", until="2024-12-31", max_records=10, page_size=100,
        contact_email="orion-sd10@example.org", rate_seconds=0.5, timeout=5.0, retries=3,
        dry_run=False)
    base.update(overrides)
    return argparse.Namespace(**base)


def _read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def _query_params(url):
    return {key: values[0] for key, values in urllib.parse.parse_qs(urllib.parse.urlparse(url).query).items()}


def _arxiv_pages():
    return [common.Response(200, (FIXTURES / "arxiv_feed_page1.xml").read_bytes()),
            common.Response(200, (FIXTURES / "arxiv_feed_page2.xml").read_bytes())]


def _run_arxiv(tmp_path, transport, **overrides):
    args = _arxiv_args(tmp_path, **overrides)
    sleep = SleepRecorder()
    receipt = arxiv.run(args, transport=transport, sleep=sleep)
    return args, receipt


def test_arxiv_normalization_maps_versions_honestly(tmp_path):
    _args, _receipt = _run_arxiv(tmp_path, FakeTransport(_arxiv_pages()))
    rows = _read_jsonl(_args.output_observations)
    assert [row["trajectory_id"] for row in rows] == ["arxiv:2401.00001", "arxiv:2401.00002", "arxiv:2401.00003"]
    assert [row["kind"] for row in rows] == ["OTHER", "VERSION_OR_REVISION", "OTHER"]
    assert [row["ordinal"] for row in rows] == [0, 1, 0]
    assert rows[0]["domain_id"] == "arxiv-cat:cs.LG"
    assert rows[0]["epoch_id"] == "year:2024"
    assert rows[0]["proxy_metrics"]["arxiv:author_count"] == 3.0
    assert rows[0]["institution_ids"] == [] and rows[0]["team_id"] == ""
    assert common.BIAS_PUBLICATION in rows[0]["bias_flag_ids"]
    for row in rows:
        DevelopmentObservation(**{**row, "kind": ObservationKind(row["kind"]),
                                  "action_feature_ids": tuple(row["action_feature_ids"]),
                                  "proxy_metrics": tuple(row["proxy_metrics"].items())})


def test_arxiv_never_emits_outcome_bindings(tmp_path):
    _args, receipt = _run_arxiv(tmp_path, FakeTransport(_arxiv_pages()))
    assert _read_jsonl(_args.output_bindings) == []
    assert receipt["records"]["outcome_bindings_emitted"] == 0
    assert receipt["outcome_policy"]["arxiv_version_progression_is_outcome"] is False
    assert receipt["outcome_policy"]["unvalidated_outcome_class"] == "UNKNOWN"
    assert "absent-by-censoring" in receipt["censoring_statement"]


def test_arxiv_dry_run_makes_zero_requests(tmp_path):
    def _forbidden(url, headers):
        raise AssertionError("dry run performed a network request")

    args, receipt = _run_arxiv(tmp_path, _forbidden, dry_run=True)
    assert receipt["run"]["dry_run"] is True
    assert receipt["dry_run_plan"]["requests_planned"] >= 1
    assert "submittedDate" in receipt["planned_urls"][0]
    assert "start=0" in receipt["planned_urls"][0]


def test_arxiv_rejects_intervals_below_documented_limit(tmp_path):
    argv = ["--output-observations", str(tmp_path / "o.jsonl"), "--output-bindings", str(tmp_path / "b.jsonl"),
            "--receipt", str(tmp_path / "r.json"), "--state", str(tmp_path / "s.json"),
            "--since", "2024-01-01", "--until", "2024-12-31", "--rate-seconds", "1.0"]
    with pytest.raises(SystemExit):
        arxiv.main(argv)


def test_arxiv_atom_error_entry_fails_closed(tmp_path):
    error_feed = (
        '<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom">'
        '<entry><id>http://arxiv.org/api/error</id><title>Error</title>'
        "<summary>incorrect search parameter</summary></entry></feed>").encode()
    with pytest.raises(common.HardFailClosed):
        _run_arxiv(tmp_path, FakeTransport([common.Response(200, error_feed)]))


def test_main_writes_failed_closed_receipt_on_4xx(tmp_path, monkeypatch):
    def _forbidden(url, headers):
        return common.Response(403, b"forbidden")

    monkeypatch.setattr(common, "UrllibTransport", lambda timeout: _forbidden)
    receipt_path = tmp_path / "receipt.json"
    code = crossref.main([
        "--output-observations", str(tmp_path / "o.jsonl"), "--output-bindings", str(tmp_path / "b.jsonl"),
        "--receipt", str(receipt_path), "--state", str(tmp_path / "s.json"),
        "--since", "2024-01-01", "--until", "2024-12-31", "--contact-email", "orion-sd10@example.org"])
    assert code == 2
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["failed_closed"] is True
    assert receipt["error_log"]


def test_crossref_retraction_bindings_are_failure_only_with_witness(tmp_path):
    transport = FakeTransport([common.Response(200, (FIXTURES / "crossref_works_page1.json").read_bytes())])
    args = _crossref_args(tmp_path)
    receipt = crossref.run(args, transport=transport, sleep=SleepRecorder())
    bindings = _read_jsonl(args.output_bindings)
    # Only the notice's documented update-to type=retraction entry binds; the
    # correction on the normal article must NOT bind, and the notice/normal
    # records bind nothing for themselves.
    assert [(b["trajectory_id"], b["outcome_class"]) for b in bindings] == \
        [("doi:10.1000/retracted-target", "VALIDATED_FAILURE")]
    assert bindings[0]["witness_ids"] == ["doi:10.1000/retraction-notice"]
    assert all(b["outcome_class"] != "VALIDATED_SUCCESS" for b in bindings)
    assert receipt["records"]["outcome_bindings_emitted"] == 1
    rows = _read_jsonl(args.output_observations)
    by_trajectory = {row["trajectory_id"]: row for row in rows}
    assert by_trajectory["doi:10.1000/retraction-notice"]["kind"] == "RETRACTION"
    assert by_trajectory["doi:10.1000/retraction-notice"]["failure_feature_ids"] == ["crossref:retraction_notice"]
    # The retracted target record itself carries no Crossref marker: the binding
    # exists only through the notice, which is why the witness is the notice DOI.
    assert by_trajectory["doi:10.1000/retracted-target"]["failure_feature_ids"] == []


def test_crossref_absence_of_retraction_is_never_success(tmp_path):
    transport = FakeTransport([common.Response(200, (FIXTURES / "crossref_works_page1.json").read_bytes())])
    args = _crossref_args(tmp_path)
    crossref.run(args, transport=transport, sleep=SleepRecorder())
    rows = _read_jsonl(args.output_observations)
    normal = next(row for row in rows if row["trajectory_id"] == "doi:10.1000/normal-article")
    # A correction update is NOT failure evidence: no failure feature, no binding.
    assert normal["failure_feature_ids"] == []
    assert normal["proxy_metrics"]["crossref:is_referenced_by_count"] == 57.0
    assert normal["institution_ids"] == ["crossref-inst:Example Institute"]
    observations = [DevelopmentObservation(
        **{**row, "kind": ObservationKind(row["kind"]), "action_feature_ids": tuple(row["action_feature_ids"]),
           "proxy_metrics": tuple(row["proxy_metrics"].items())}) for row in rows]
    episodes = {ep.episode_id: ep for ep in assemble_all(observations)}
    assert episodes["doi:10.1000/normal-article"].outcome_class is DevelopmentOutcomeClass.UNKNOWN
    assert episodes["doi:10.1000/retracted-target"].outcome_class is DevelopmentOutcomeClass.UNKNOWN


def test_crossref_bindings_roundtrip_to_validated_failure(tmp_path):
    transport = FakeTransport([common.Response(200, (FIXTURES / "crossref_works_page1.json").read_bytes())])
    args = _crossref_args(tmp_path)
    crossref.run(args, transport=transport, sleep=SleepRecorder())
    rows = _read_jsonl(args.output_observations)
    observations = [DevelopmentObservation(
        **{**row, "kind": ObservationKind(row["kind"]), "action_feature_ids": tuple(row["action_feature_ids"]),
           "proxy_metrics": tuple(row["proxy_metrics"].items())}) for row in rows]
    bindings = [OutcomeBinding(b["trajectory_id"], DevelopmentOutcomeClass(b["outcome_class"]),
                               tuple(b["witness_ids"]), tuple(b["source_ids"])) for b in _read_jsonl(args.output_bindings)]
    episodes = {ep.episode_id: ep for ep in assemble_all(observations, bindings)}
    assert episodes["doi:10.1000/retracted-target"].outcome_class is DevelopmentOutcomeClass.VALIDATED_FAILURE
    assert episodes["doi:10.1000/retracted-target"].outcome_witness_ids == ("doi:10.1000/retraction-notice",)
    assert episodes["doi:10.1000/normal-article"].outcome_class is DevelopmentOutcomeClass.UNKNOWN


def test_openalex_retraction_institutions_and_kinds(tmp_path):
    transport = FakeTransport([common.Response(200, (FIXTURES / "openalex_works_page1.json").read_bytes())])
    args = _openalex_args(tmp_path)
    receipt = openalex.run(args, transport=transport, sleep=SleepRecorder())
    rows = _read_jsonl(args.output_observations)
    by_trajectory = {row["trajectory_id"]: row for row in rows}
    assert by_trajectory["openalex:W1"]["institution_ids"] == ["openalex-inst:I1"]
    assert by_trajectory["openalex:W1"]["domain_id"] == "openalex-field:33"
    assert by_trajectory["openalex:W3"]["kind"] == "DATA_OR_INSTRUMENT"
    assert by_trajectory["openalex:W3"]["domain_id"] == "openalex-source:S77"
    assert by_trajectory["openalex:W1"]["proxy_metrics"]["openalex:cited_by_count"] == 41.0
    bindings = _read_jsonl(args.output_bindings)
    assert [(b["trajectory_id"], b["outcome_class"]) for b in bindings] == \
        [("openalex:W2", "VALIDATED_FAILURE")]
    assert bindings[0]["witness_ids"] == ["openalex:W2"]
    assert by_trajectory["openalex:W2"]["failure_feature_ids"] == ["openalex:is_retracted"]
    assert receipt["records"]["outcome_bindings_emitted"] == 1


def test_openalex_daily_budget_stops_before_exceeding_limit(tmp_path):
    transport = FakeTransport([common.Response(200, (FIXTURES / "openalex_works_page1.json").read_bytes()),
                               common.Response(200, b'{"results": [], "meta": {}}')])
    args = _openalex_args(tmp_path, daily_request_cap=1, page_size=3)
    receipt = openalex.run(args, transport=transport, sleep=SleepRecorder())
    assert len(transport.urls) == 1
    assert receipt["request_count"] == 1
    assert any("daily request budget" in entry for entry in receipt["error_log"])
    assert receipt["daily_request_budget"]["cap"] == 1
    assert receipt["daily_request_budget"]["documented_limit"] == 100000


def test_openalex_daily_budget_resets_on_new_utc_day(tmp_path):
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    state_path = tmp_path / "state.json"
    state_path.write_text(json.dumps({"cursor": None, "records_emitted": 0, "pages_fetched": 0,
                                      "requests_today": 1, "budget_date": yesterday}), encoding="utf-8")
    transport = FakeTransport([common.Response(200, (FIXTURES / "openalex_works_page1.json").read_bytes())])
    args = _openalex_args(tmp_path, daily_request_cap=1, page_size=3, max_records=3)
    receipt = openalex.run(args, transport=transport, sleep=SleepRecorder())
    # A state file from an earlier UTC day must RESET the budget, not block the
    # run forever.
    assert len(transport.urls) == 1
    assert receipt["request_count"] == 1
    assert receipt["error_log"] == []
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["budget_date"] == today
    assert state["requests_today"] == 1


def test_openalex_daily_budget_still_blocks_within_same_day(tmp_path):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    (tmp_path / "state.json").write_text(json.dumps(
        {"cursor": None, "records_emitted": 0, "pages_fetched": 0,
         "requests_today": 1, "budget_date": today}), encoding="utf-8")
    transport = FakeTransport([])
    args = _openalex_args(tmp_path, daily_request_cap=1, page_size=3)
    receipt = openalex.run(args, transport=transport, sleep=SleepRecorder())
    assert len(transport.urls) == 0
    assert any("daily request budget" in entry for entry in receipt["error_log"])


def test_crossref_cursor_protocol_never_combines_offset_with_cursor(tmp_path):
    transport = FakeTransport([common.Response(200, (FIXTURES / "crossref_works_page1.json").read_bytes()),
                               common.Response(200, (FIXTURES / "crossref_works_page2.json").read_bytes())])
    args = _crossref_args(tmp_path, page_size=2)
    receipt = crossref.run(args, transport=transport, sleep=SleepRecorder())
    assert len(transport.urls) == 2
    first = _query_params(transport.urls[0])
    second = _query_params(transport.urls[1])
    # Documented protocol: first request cursor=*, later requests repeat
    # message.next-cursor; `offset` must never ride along.
    assert first["cursor"] == "*"
    assert second["cursor"] == "crossref-cursor-2"
    for url in transport.urls:
        params = _query_params(url)
        assert "offset" not in params
        assert "from-pub-date:2024-01-01" in params["filter"]
        assert "until-pub-date:2024-12-31" in params["filter"]
    # Page 2 content still normalizes (dataset type -> DATA_OR_INSTRUMENT).
    rows = _read_jsonl(args.output_observations)
    by_trajectory = {row["trajectory_id"]: row for row in rows}
    assert by_trajectory["doi:10.1000/dataset-article"]["kind"] == "DATA_OR_INSTRUMENT"
    assert receipt["records"]["observations_in_output"] == 4


def test_openalex_cursor_protocol_uses_documented_start_and_next_cursor(tmp_path):
    transport = FakeTransport([common.Response(200, (FIXTURES / "openalex_works_page1.json").read_bytes()),
                               common.Response(200, b'{"results": [], "meta": {}}')])
    args = _openalex_args(tmp_path, page_size=3)
    openalex.run(args, transport=transport, sleep=SleepRecorder())
    assert len(transport.urls) == 2
    first = _query_params(transport.urls[0])
    second = _query_params(transport.urls[1])
    assert first["cursor"] == "*"
    assert second["cursor"] == "openalex-cursor-2"
    assert "from_publication_date:2024-01-01" in first["filter"]
    assert "to_publication_date:2024-12-31" in first["filter"]


def test_rate_limit_and_429_backoff_plumbing(tmp_path):
    pages = [common.Response(429, b"slow down"),
             common.Response(200, (FIXTURES / "arxiv_feed_page1.xml").read_bytes())]
    transport = FakeTransport(pages)
    args, receipt = _run_arxiv(tmp_path, transport, max_records=2)
    assert len(transport.urls) == 2
    assert receipt["request_count"] == 1
    rows = _read_jsonl(args.output_observations)
    assert len(rows) == 2


def test_rate_limiter_enforces_minimum_interval():
    sleep = SleepRecorder()
    limiter = common.RateLimiter(3.0, sleep)
    limiter._last = time.monotonic() + 10.0
    limiter.wait()
    assert sleep.calls and sleep.calls[-1] >= 3.0


def test_non_429_4xx_fails_closed(tmp_path):
    with pytest.raises(common.HardFailClosed):
        _run_arxiv(tmp_path, FakeTransport([common.Response(403, b"forbidden")]))
    with pytest.raises(common.HardFailClosed):
        _run_arxiv(tmp_path, FakeTransport([common.Response(404, b"missing")]))


def test_cursor_resumption_continues_from_state(tmp_path):
    transport_one = FakeTransport([common.Response(200, (FIXTURES / "arxiv_feed_page1.xml").read_bytes())])
    args_one, receipt_one = _run_arxiv(tmp_path, transport_one, max_records=2, page_size=2)
    state = json.loads(Path(args_one.state).read_text(encoding="utf-8"))
    assert state["cursor"] == {"start": 2}
    assert state["records_emitted"] == 2
    assert state["pages_fetched"] == 1
    transport_two = FakeTransport([common.Response(200, (FIXTURES / "arxiv_feed_page2.xml").read_bytes())])
    args_two, receipt_two = _run_arxiv(tmp_path, transport_two, max_records=5, page_size=2)
    assert "start=2" in transport_two.urls[0]
    # Resume MERGES into the existing output instead of replacing it: an
    # interrupted run never loses already-fetched records.
    rows_two = _read_jsonl(args_two.output_observations)
    assert [row["observation_id"] for row in rows_two] == \
        ["arxiv-obs:2401.00001v1", "arxiv-obs:2401.00002v2", "arxiv-obs:2401.00003v1"]
    assert receipt_two["records"]["observations_emitted"] == 1
    assert receipt_two["records"]["observations_in_output"] == 3
    state_two = json.loads(Path(args_two.state).read_text(encoding="utf-8"))
    assert state_two["records_emitted"] == 3


def test_torn_final_append_line_is_dropped_and_healed(tmp_path):
    # Crash during append_jsonl: one complete row, then a truncated JSON tail
    # without the committing newline. The load must drop only the tail.
    complete = json.dumps({"observation_id": "arxiv-obs:2401.00001v1", "k": 1}) + "\n"
    torn = '{"observation_id": "arxiv-obs:2401.00002v2", "prox'
    ledger_path = tmp_path / "obs.jsonl"
    ledger_path.write_bytes(complete.encode("utf-8") + torn.encode("utf-8"))
    assert [row["observation_id"] for row in common.load_jsonl_rows(ledger_path)] == ["arxiv-obs:2401.00001v1"]
    # A split multibyte UTF-8 sequence in the tail is dropped the same way.
    ledger_path.write_bytes(complete.encode("utf-8") + '{"a": "ﬂ'.encode("utf-8")[:-1])
    assert [row["observation_id"] for row in common.load_jsonl_rows(ledger_path)] == ["arxiv-obs:2401.00001v1"]
    # A newline-terminated line that still fails to parse is real corruption:
    # it must raise, never silently vanish.
    ledger_path.write_bytes(complete.encode("utf-8") + b"{not json}\n")
    with pytest.raises(json.JSONDecodeError):
        common.load_jsonl_rows(ledger_path)


def test_resume_survives_torn_output_tail(tmp_path):
    # A crash between the durable append and the cursor advance can leave a
    # torn tail; the resumed run must start, re-fetch, and heal the file.
    first_args = _run_arxiv(tmp_path, FakeTransport(
        [common.Response(200, (FIXTURES / "arxiv_feed_page1.xml").read_bytes())]),
        max_records=2, page_size=2)[0]
    state = json.loads(Path(first_args.state).read_text(encoding="utf-8"))
    # Roll the cursor back and truncate the last row mid-line: the on-disk
    # picture of a crash mid-append (row 1 complete, row 2 torn, no newline).
    state["cursor"] = {"start": 0}
    Path(first_args.state).write_text(json.dumps(state), encoding="utf-8")
    output = Path(first_args.output_observations)
    output.write_bytes(output.read_bytes()[:-8])
    transport = FakeTransport([common.Response(200, (FIXTURES / "arxiv_feed_page1.xml").read_bytes()),
                               common.Response(200, (FIXTURES / "arxiv_feed_page2.xml").read_bytes())])
    _args, receipt = _run_arxiv(tmp_path, transport, max_records=5, page_size=2)
    assert output.read_bytes().endswith(b"\n")
    ids = [row["observation_id"] for row in _read_jsonl(output)]
    assert ids == ["arxiv-obs:2401.00001v1", "arxiv-obs:2401.00002v2", "arxiv-obs:2401.00003v1"]
    assert receipt["records"]["observations_in_output"] == 3


def test_receipt_structure_hashes_and_authority(tmp_path):
    transport = FakeTransport([common.Response(200, (FIXTURES / "crossref_works_page1.json").read_bytes())])
    args = _crossref_args(tmp_path)
    receipt = crossref.run(args, transport=transport, sleep=SleepRecorder())
    assert receipt["schema_version"] == "orion.v2.sd10-source-adapter-receipt.v1"
    assert receipt["source"]["endpoints"] == ["https://api.crossref.org/works"]
    assert receipt["source"]["terms_note"]
    assert all(value is False for value in receipt["authority"].values())
    assert receipt["outcome_policy"]["citation_or_fame_metric_infers_outcome"] is False
    assert receipt["outcome_policy"]["absence_of_retraction_is_never_success"] is True
    for entry in receipt["emitted_files"]:
        digest = hashlib.sha256(Path(entry["path"]).read_bytes()).hexdigest()
        assert entry["sha256"] == digest
    assert receipt["fetched_window"] == {"since": "2024-01-01", "until": "2024-12-31"}
    assert len(receipt["records"]["per_record_source_ids"]) == receipt["records"]["observations_emitted"]
    assert receipt["cannot_check"]


def test_dry_run_requires_no_contact_email(tmp_path):
    def _forbidden(url, headers):
        raise AssertionError("dry run performed a network request")

    args = _openalex_args(tmp_path, dry_run=True, contact_email="")
    receipt = openalex.run(args, transport=_forbidden, sleep=SleepRecorder())
    assert receipt["dry_run_plan"]["requests_planned"] == 1
    params = _query_params(receipt["dry_run_plan"]["sample_url"])
    assert params["filter"] == "from_publication_date:2024-01-01,to_publication_date:2024-12-31"
    assert params["cursor"] == "*"


def test_real_run_requires_contact_email_for_polite_pools(tmp_path):
    transport = FakeTransport([])
    for module, factory in ((crossref, _crossref_args), (openalex, _openalex_args), (pubmed, _pubmed_args)):
        with pytest.raises(SystemExit):
            module.run(factory(tmp_path, contact_email=""), transport=transport, sleep=SleepRecorder())


def _pubmed_retraction_set_pages():
    # One esearch (4-uid term search) + one efetch for the whole set: live
    # responses captured 2026-08-29 and trimmed only for size.
    return [
        common.Response(200, (FIXTURES / "pubmed_retraction_set_esearch.json").read_bytes()),
        common.Response(200, (FIXTURES / "pubmed_retraction_set.xml").read_bytes())]


def _run_pubmed(tmp_path, transport, **overrides):
    args = _pubmed_args(tmp_path, **overrides)
    receipt = pubmed.run(args, transport=transport, sleep=SleepRecorder())
    return args, receipt


def test_pubmed_field_mapping_and_domain_fallbacks(tmp_path):
    _args, _receipt = _run_pubmed(tmp_path, FakeTransport(_pubmed_retraction_set_pages()))
    rows = _read_jsonl(_args.output_observations)
    by_trajectory = {row["trajectory_id"]: row for row in rows}
    assert sorted(by_trajectory) == ["pubmed:2190089", "pubmed:33522354",
                                     "pubmed:36017998", "pubmed:42462751"]
    # Domain: first MeSH descriptor UI for indexed records, journal identity
    # (NlmUniqueID) for unindexed In-Process/PubMed-not-MEDLINE records.
    assert by_trajectory["pubmed:2190089"]["domain_id"] == "pubmed-mesh:D000818"
    assert by_trajectory["pubmed:33522354"]["domain_id"] == "pubmed-journal:101581063"
    assert by_trajectory["pubmed:36017998"]["domain_id"] == "pubmed-journal:101581063"
    # Epoch year comes from the pdat channel (Journal/JournalIssue/PubDate).
    assert by_trajectory["pubmed:2190089"]["epoch_id"] == "year:1990"
    assert by_trajectory["pubmed:36017998"]["epoch_id"] == "year:2022"
    assert by_trajectory["pubmed:33522354"]["epoch_id"] == "year:2026"
    # Proxy metrics are real countable XML fields only; no citation counts exist.
    assert by_trajectory["pubmed:2190089"]["proxy_metrics"] == {
        "pubmed:author_count": 1.0, "pubmed:mesh_heading_count": 5.0}
    assert by_trajectory["pubmed:36017998"]["proxy_metrics"] == {
        "pubmed:author_count": 0.0, "pubmed:mesh_heading_count": 0.0}
    assert "pubmed:cited_by_count" not in by_trajectory["pubmed:2190089"]["proxy_metrics"]
    # Institutions from AuthorList/AffiliationInfo when present; verbatim text.
    assert by_trajectory["pubmed:33522354"]["institution_ids"] == [
        "pubmed-inst:Department of Life Science of Shanxi Datong University, Datong Shanxi 037009, China."]
    assert by_trajectory["pubmed:2190089"]["institution_ids"] == []
    assert by_trajectory["pubmed:2190089"]["team_id"] == ""
    assert common.BIAS_PUBLICATION in by_trajectory["pubmed:2190089"]["bias_flag_ids"]
    assert common.BIAS_CITATION_WINDOW not in by_trajectory["pubmed:2190089"]["bias_flag_ids"]
    for row in rows:
        DevelopmentObservation(**{**row, "kind": ObservationKind(row["kind"]),
                                  "action_feature_ids": tuple(row["action_feature_ids"]),
                                  "proxy_metrics": tuple(row["proxy_metrics"].items())})


def test_pubmed_retracted_binds_notice_and_erratum_do_not(tmp_path):
    args, receipt = _run_pubmed(tmp_path, FakeTransport(_pubmed_retraction_set_pages()))
    bindings = _read_jsonl(args.output_bindings)
    # ONLY the record whose own PublicationType is "Retracted Publication"
    # binds; the "Retraction Notice" record and the "Published Erratum" record
    # bind nothing (the notice documents a failure, the erratum corrects one).
    assert [(b["trajectory_id"], b["outcome_class"]) for b in bindings] == \
        [("pubmed:33522354", "VALIDATED_FAILURE")]
    # The witness is the pubmed record itself: PubMed marks the RETRACTED
    # article with its own PT, unlike Crossref where only the notice knows.
    assert bindings[0]["witness_ids"] == ["pubmed:33522354"]
    assert all(b["outcome_class"] != "VALIDATED_SUCCESS" for b in bindings)
    assert receipt["records"]["outcome_bindings_emitted"] == 1
    rows = _read_jsonl(args.output_observations)
    by_trajectory = {row["trajectory_id"]: row for row in rows}
    assert by_trajectory["pubmed:33522354"]["kind"] == "RETRACTION"
    assert by_trajectory["pubmed:33522354"]["failure_feature_ids"] == ["pubmed:retracted_publication"]
    assert by_trajectory["pubmed:36017998"]["kind"] == "RETRACTION"
    assert by_trajectory["pubmed:36017998"]["failure_feature_ids"] == ["pubmed:retraction_notice"]
    assert by_trajectory["pubmed:42462751"]["kind"] == "CORRECTION"
    assert by_trajectory["pubmed:42462751"]["failure_feature_ids"] == []
    assert by_trajectory["pubmed:2190089"]["kind"] == "OTHER"
    assert by_trajectory["pubmed:2190089"]["failure_feature_ids"] == []


def test_pubmed_bindings_roundtrip_to_validated_failure(tmp_path):
    args, _receipt = _run_pubmed(tmp_path, FakeTransport(_pubmed_retraction_set_pages()))
    rows = _read_jsonl(args.output_observations)
    observations = [DevelopmentObservation(
        **{**row, "kind": ObservationKind(row["kind"]), "action_feature_ids": tuple(row["action_feature_ids"]),
           "proxy_metrics": tuple(row["proxy_metrics"].items())}) for row in rows]
    bindings = [OutcomeBinding(b["trajectory_id"], DevelopmentOutcomeClass(b["outcome_class"]),
                               tuple(b["witness_ids"]), tuple(b["source_ids"])) for b in _read_jsonl(args.output_bindings)]
    episodes = {ep.episode_id: ep for ep in assemble_all(observations, bindings)}
    assert episodes["pubmed:33522354"].outcome_class is DevelopmentOutcomeClass.VALIDATED_FAILURE
    assert episodes["pubmed:33522354"].outcome_witness_ids == ("pubmed:33522354",)
    # Absence of a retraction PT is never a success: notice, erratum and plain
    # records all stay UNKNOWN downstream.
    for trajectory in ("pubmed:36017998", "pubmed:42462751", "pubmed:2190089"):
        assert episodes[trajectory].outcome_class is DevelopmentOutcomeClass.UNKNOWN


def _pubmed_window_pages():
    return [
        common.Response(200, (FIXTURES / "pubmed_esearch_page1.json").read_bytes()),
        common.Response(200, (FIXTURES / "pubmed_efetch_page1.xml").read_bytes()),
        common.Response(200, (FIXTURES / "pubmed_esearch_page2.json").read_bytes()),
        common.Response(200, (FIXTURES / "pubmed_efetch_page2.xml").read_bytes())]


def test_pubmed_paging_uses_documented_esearch_efetch_protocol(tmp_path):
    transport = FakeTransport(_pubmed_window_pages())
    args = _pubmed_args(tmp_path, page_size=3, max_records=6)
    receipt = pubmed.run(args, transport=transport, sleep=SleepRecorder())
    # Two pages: esearch+efetch per page, alternating documented URLs.
    assert len(transport.urls) == 4
    search_one, fetch_one, search_two, fetch_two = transport.urls
    first = _query_params(search_one)
    second = _query_params(search_two)
    assert first["db"] == "pubmed" and first["retmode"] == "json"
    assert first["datetype"] == "pdat"
    assert first["mindate"] == "2024/01/01" and first["maxdate"] == "2024/12/31"
    assert first["sort"] == "pub_date"
    assert first["retstart"] == "0" and first["retmax"] == "3"
    assert second["retstart"] == "3"
    assert "WebEnv" not in first and "query_key" not in first
    assert fetch_one.startswith("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi")
    assert _query_params(fetch_one)["retmode"] == "xml"
    assert _query_params(fetch_one)["id"] == "41675261,42182984,42256493"
    assert _query_params(fetch_two)["id"] == "42182983,42186608,42179428"
    assert receipt["request_count"] == 4
    assert receipt["pages"] == 2
    assert receipt["records"]["observations_in_output"] == 6
    assert receipt["records"]["outcome_bindings_emitted"] == 0


def test_pubmed_cursor_resumption_continues_from_retstart(tmp_path):
    state_path = tmp_path / "state.json"
    state_path.write_text(json.dumps({"cursor": {"retstart": 3}, "records_emitted": 3,
                                      "pages_fetched": 1}), encoding="utf-8")
    transport = FakeTransport([common.Response(200, (FIXTURES / "pubmed_esearch_page2.json").read_bytes()),
                               common.Response(200, (FIXTURES / "pubmed_efetch_page2.xml").read_bytes())])
    args, receipt = _run_pubmed(tmp_path, transport, page_size=3, max_records=3)
    assert _query_params(transport.urls[0])["retstart"] == "3"
    rows = _read_jsonl(args.output_observations)
    assert [row["observation_id"] for row in rows] == \
        ["pubmed-obs:42182983", "pubmed-obs:42186608", "pubmed-obs:42179428"]
    assert receipt["records"]["observations_emitted"] == 3
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["cursor"] == {"retstart": 6}
    assert state["records_emitted"] == 6


def test_pubmed_dry_run_makes_zero_requests(tmp_path):
    def _forbidden(url, headers):
        raise AssertionError("dry run performed a network request")

    args, receipt = _run_pubmed(tmp_path, _forbidden, dry_run=True)
    assert receipt["run"]["dry_run"] is True
    assert receipt["dry_run_plan"]["requests_planned"] >= 1
    assert "2x requests_planned" in receipt["dry_run_plan"]["note"]
    params = _query_params(receipt["dry_run_plan"]["sample_url"])
    assert params["datetype"] == "pdat"
    assert params["mindate"] == "2024/01/01"
    assert params["retstart"] == "0"


def test_pubmed_rejects_intervals_below_documented_three_per_second(tmp_path):
    argv = ["--output-observations", str(tmp_path / "o.jsonl"), "--output-bindings", str(tmp_path / "b.jsonl"),
            "--receipt", str(tmp_path / "r.json"), "--state", str(tmp_path / "s.json"),
            "--since", "2024-01-01", "--until", "2024-12-31", "--rate-seconds", "0.2"]
    with pytest.raises(SystemExit):
        pubmed.main(argv)


def test_pubmed_esearch_errorlist_fails_closed(tmp_path):
    error = json.dumps({"esearchresult": {"count": "0", "idlist": [],
                                          "errorlist": {"phrasesnotfound": ["publication"]}}}).encode()
    with pytest.raises(common.HardFailClosed):
        _run_pubmed(tmp_path, FakeTransport([common.Response(200, error)]))


def test_pubmed_non_429_4xx_fails_closed(tmp_path):
    with pytest.raises(common.HardFailClosed):
        _run_pubmed(tmp_path, FakeTransport([common.Response(403, b"forbidden")]))



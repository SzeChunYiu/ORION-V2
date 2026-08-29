"""Fixture-based tests for the SD20 arXiv version-history adapter (no network).

The adapter accepts an injectable transport + sleep, so every test here drives
the real run() paths (including resume) against an embedded Atom response
fixture. No test may open a socket. Mirrors tests/unit/test_sd10_source_adapters_wave6.py.
"""
import importlib.util
import json
import sys
import types
from pathlib import Path

import pytest

REPO = Path(__file__).parents[2]


def _load(name: str, path: Path):
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        # register BEFORE exec_module: dataclasses resolves cls.__module__
        # through sys.modules during class creation (same order as the SD10
        # loader in test_sd10_source_adapters_wave6.py)
        sys.modules[name] = module
        assert spec.loader is not None
        spec.loader.exec_module(module)
    return sys.modules[name]


common = _load("sd10_sources_common", REPO / "scripts" / "sd10_sources" / "common.py")
adapter = _load("sd20_arxiv_version_history_adapter",
                REPO / "scripts" / "sd20_sources" / "arxiv_version_history_adapter.py")

FIXTURE_BODY = b"""<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom"><totalResults>2</totalResults>
<entry><id>http://arxiv.org/abs/2401.00614v1</id><updated>2024-01-01T00:41:18Z</updated><published>2024-01-01T00:41:18Z</published><title> Paper One </title><summary> An abstract. </summary><author><name>A</name></author><author><name>B</name></author><arxiv:primary_category xmlns:arxiv="http://arxiv.org/schemas/atom" term="math.NT"/><category term="math.AG"/></entry>
<entry><id>http://arxiv.org/abs/2401.00614v2</id><updated>2025-02-16T10:00:00Z</updated><published>2024-01-01T00:41:18Z</published><title>Paper One v2</title><summary>Longer abstract with more text in the second version.</summary><author><name>A</name></author><author><name>B</name></author><author><name>C</name></author><arxiv:primary_category xmlns:arxiv="http://arxiv.org/schemas/atom" term="cs.LG"/></entry>
</feed>"""

PARENT_HEAD = {
    "observation_id": "arxiv-obs:2401.00614v3", "trajectory_id": "arxiv:2401.00614",
    "domain_id": "arxiv-cat:math.NT", "epoch_id": "year:2024",
    "source_mode_id": "arxiv_atom_metadata", "ordinal": 2, "kind": "VERSION_OR_REVISION",
    "action_feature_ids": [], "result_feature_ids": [], "failure_feature_ids": [],
    "source_ids": ["http://arxiv.org/abs/2401.00614v3"], "validation_ids": [],
    "institution_ids": [], "team_id": "", "proxy_metrics": {}, "bias_flag_ids": [],
    "resource_cost": 0.0,
}


def test_parse_feed_versions_and_dates():
    entries = adapter.parse_feed(FIXTURE_BODY)
    assert len(entries) == 2
    e1, e2 = entries
    assert (e1["arxiv_id"], e1["version"]) == ("2401.00614", 1)
    assert (e2["arxiv_id"], e2["version"]) == ("2401.00614", 2)
    # <published> is paper-level (v1 date, identical across versions);
    # <updated> is real per-version temporal metadata.
    assert e1["published"] == "2024-01-01" == e2["published"]
    assert e1["updated"] == "2024-01-01" and e2["updated"] == "2025-02-16"
    assert e1["title_chars"] == len("Paper One")
    assert e1["abstract_chars"] == len("An abstract.")
    assert e1["author_count"] == 2 and e2["author_count"] == 3


def test_to_observation_anchors_domain_and_epoch_to_parent_head():
    entries = adapter.parse_feed(FIXTURE_BODY)
    _e1, e2 = entries
    parent = {"arxiv_id": "2401.00614", "head_version": 3,
              "head_domain": "arxiv-cat:math.NT", "head_epoch": "year:2024", "published": ""}
    counters: dict = {}
    o2 = adapter.to_observation(e2, parent, counters)
    assert o2.observation_id == "arxiv-obs:2401.00614v2"
    assert o2.trajectory_id == "arxiv:2401.00614"
    # a mid-trajectory primary-category change (cs.LG) must NOT split the
    # trajectory: domain/epoch stay anchored to the parent head, and the
    # anchoring event is counted, never silent.
    assert o2.domain_id == "arxiv-cat:math.NT"
    assert o2.epoch_id == "year:2024"
    assert o2.ordinal == 1 and o2.kind.value == "VERSION_OR_REVISION"
    assert o2.action_feature_ids[1] == "arxiv:primary_category:cs.LG"
    assert counters.get("version_domain_anchored_to_head") == 1
    assert "version_epoch_anchored_to_head" not in counters  # published year matches
    metrics = dict(o2.proxy_metrics)
    assert metrics["arxiv:author_count"] == 3.0
    assert metrics["arxiv:title_chars"] == float(len("Paper One v2"))
    assert metrics["arxiv:days_since_first_deposit"] == 412.0  # 2024-01-01 -> 2025-02-16
    o1 = adapter.to_observation(_e1, parent, counters)
    assert o1.kind.value == "OTHER" and o1.ordinal == 0


def test_atom_error_entry_fails_closed():
    err = adapter.parse_feed(
        b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>x</id>'
        b'<title>Error</title></entry></feed>')
    # the adapter resolves its own shared-common instance (sd20_sources_common)
    with pytest.raises(adapter.common.HardFailClosed):
        adapter.check_atom_error(err)


def test_missing_version_set_computation():
    entries = adapter.parse_feed(FIXTURE_BODY)
    requested = {("2401.00614", 1), ("2401.00614", 2)}
    got = {f"{e['arxiv_id']}v{e['version']}" for e in entries[:1]}  # only v1 returned
    missing = {f"{a}v{v}" for a, v in requested} - got
    assert missing == {"2401.00614v2"}  # recorded honestly, never invented


class FixtureTransport:
    """Serves the canned id_list response; counts calls and asserts etiquette."""

    def __init__(self):
        self.calls = 0

    def __call__(self, url, headers):
        self.calls += 1
        assert "id_list=" in url and "max_results=2" in url, url
        assert "SD20-version-history-harvester" in headers["User-Agent"]
        return types.SimpleNamespace(status=200, body=FIXTURE_BODY)


def _run_args(tmp_path: Path) -> types.SimpleNamespace:
    parent_obs = tmp_path / "parent.jsonl"
    parent_obs.write_text(json.dumps(PARENT_HEAD) + "\n")
    return types.SimpleNamespace(
        parent_observations=str(parent_obs),
        output_observations=str(tmp_path / "obs.jsonl"),
        output_bindings=str(tmp_path / "bind.jsonl"),
        receipt=str(tmp_path / "receipt.json"), state=str(tmp_path / "state.json"),
        since="2024-01-01", until="2024-12-31", max_records=100000, batch_size=2,
        contact_email="t@example.org", rate_seconds=3.0, timeout=30.0, retries=2,
        backoff_cap=2.0, dry_run=False)


def test_run_end_to_end_and_resume_idempotence(tmp_path):
    args = _run_args(tmp_path)
    sleeps: list = []
    transport = FixtureTransport()
    r1 = adapter.run(args, transport=transport, sleep=lambda s: sleeps.append(s))
    rows = [json.loads(line) for line in Path(args.output_observations).read_text().splitlines()]
    assert len(rows) == 2
    assert r1["records"]["observations_emitted"] == 2
    assert r1["records"]["observations_in_output"] == 2
    assert r1["missing_versions"] == []
    assert r1["anchoring_counters"].get("version_domain_anchored_to_head") == 1
    assert transport.calls == 1
    # stable-plan resume: every target already durable -> zero requests, zero
    # new rows, zero rate-limiter waits, cursor still advances.
    transport2 = FixtureTransport()
    r2 = adapter.run(args, transport=transport2, sleep=lambda s: sleeps.append(s))
    rows2 = [json.loads(line) for line in Path(args.output_observations).read_text().splitlines()]
    assert len(rows2) == 2, "resume duplicated rows"
    assert r2["records"]["observations_emitted"] == 0
    assert r2["plan"]["already_on_disk"] == 2
    assert r2["request_count"] == 0
    assert transport2.calls == 0
    assert sleeps == []


def test_run_records_missing_versions_honestly(tmp_path):
    """A batch whose response omits a requested version lists it as missing."""
    args = _run_args(tmp_path)

    class PartialTransport(FixtureTransport):
        def __call__(self, url, headers):
            self.calls += 1
            # serve only the v1 entry: feed truncated after the first </entry>
            head, sep, _rest = FIXTURE_BODY.partition(b"</entry>")
            body = head + sep + b"\n</feed>"
            return types.SimpleNamespace(status=200, body=body)

    receipt = adapter.run(args, transport=PartialTransport(), sleep=lambda s: None)
    assert receipt["missing_versions"] == ["2401.00614v2"]


HEAD_FEED = b"""<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom"><totalResults>1</totalResults>
<entry><id>http://arxiv.org/abs/2401.00614v3</id><updated>2025-06-01T10:00:00Z</updated><published>2024-01-01T00:41:18Z</published><title>Paper One v3</title><summary>Final abstract text for the third version.</summary><author><name>A</name></author><author><name>B</name></author><author><name>C</name></author><author><name>D</name></author><arxiv:primary_category xmlns:arxiv="http://arxiv.org/schemas/atom" term="math.NT"/></entry>
</feed>"""


def test_fetch_heads_mode_plans_head_versions_only(tmp_path):
    """--fetch-heads plans exactly the head version v_k per parent (V2 repair
    fetch): the full proxy-metric set the SD10 head snapshots never carried."""
    args = _run_args(tmp_path)
    args.fetch_heads = True
    urls: list = []

    class HeadTransport(FixtureTransport):
        def __call__(self, url, headers):
            urls.append(url)
            self.calls += 1
            assert "max_results=1" in url, url
            assert "SD20-version-history-harvester" in headers["User-Agent"]
            return types.SimpleNamespace(status=200, body=HEAD_FEED)

    receipt = adapter.run(args, transport=HeadTransport(), sleep=lambda s: None)
    assert receipt["plan"]["mode"] == "head_versions_only"
    assert receipt["plan"]["version_targets"] == 1
    assert "2401.00614v3" in urls[0]
    assert "2401.00614v1" not in urls[0] and "2401.00614v2" not in urls[0]
    rows = [json.loads(line) for line in Path(args.output_observations).read_text().splitlines()]
    assert len(rows) == 1
    head = rows[0]
    assert head["observation_id"] == "arxiv-obs:2401.00614v3"
    assert head["ordinal"] == 2 and head["source_mode_id"] == "arxiv_atom_version_history"
    metrics = dict(head["proxy_metrics"])
    # the exact fields SD10 head rows lack, now present on the head step
    assert metrics["arxiv:author_count"] == 4.0
    assert "arxiv:abstract_chars" in metrics
    assert "arxiv:updated_epoch_days" in metrics
    assert "arxiv:title_chars" in metrics
    assert receipt["missing_versions"] == []

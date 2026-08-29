"""Negative controls for scripts/sd20_operator_discovery.py (mutation style).

Everything runs offline against synthetic multi-version trajectories written to
tmp_path; the operator script is driven as a subprocess with PYTHONPATH=src.
Controls:
  NC1  a fame-named proxy metric field trips the frozen hard gate (exit 3);
  NC2  head-only observations (one step per trajectory, no transitions) exit 3;
  NC3  identical inputs produce byte-identical receipts (seeded determinism);
  NC4  steps missing required proxy metrics are CENSORED with a receipt
       counter (never labeled from a silent 0.0 default — the V1 defect);
       a corpus with no labelable transition exits 3;
  NC5  variant alphabets skip the fixed-lesson/F0 arms (recorded, not
       re-encoded) and remain byte-deterministic.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).parents[2]
SCRIPT = REPO / "scripts" / "sd20_operator_discovery.py"


def _version_observation(arxiv_id: str, version: int, abstract_chars: float,
                         category: str = "cs.LG") -> dict:
    return {
        "observation_id": f"arxiv-obs:{arxiv_id}v{version}",
        "trajectory_id": f"arxiv:{arxiv_id}",
        "domain_id": f"arxiv-cat:{category}", "epoch_id": "year:2024",
        "source_mode_id": ("arxiv_atom_version_history" if version > 1
                           else "arxiv_atom_metadata"),
        "ordinal": version - 1,
        "kind": "VERSION_OR_REVISION" if version > 1 else "OTHER",
        "action_feature_ids": ["arxiv:deposit_version",
                               f"arxiv:primary_category:{category}"],
        "result_feature_ids": [], "failure_feature_ids": [],
        "source_ids": [f"http://arxiv.org/abs/{arxiv_id}v{version}"],
        "validation_ids": [], "institution_ids": [], "team_id": "",
        "proxy_metrics": {"arxiv:author_count": 2.0 + 0.5 * version,
                          "arxiv:abstract_chars": abstract_chars,
                          "arxiv:updated_epoch_days": 19723.0 + 90.0 * version,
                          "arxiv:days_since_first_deposit": 90.0 * (version - 1)},
        "bias_flag_ids": ["BIAS_PUBLICATION_ONLY_CORPUS"],
        "resource_cost": 0.0,
    }


def _multiversion_corpus(n_trajectories: int = 40) -> list[dict]:
    rows = []
    for i in range(n_trajectories):
        arxiv_id = f"2401.{10000 + i:05d}"
        for version in (1, 2, 3):
            rows.append(_version_observation(
                arxiv_id, version, abstract_chars=800.0 + 130.0 * version + i))
    return rows


def _write_jsonl(path: Path, rows: list) -> Path:
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return path


def _run_operator(obs_paths: list, output: Path, *extra: str) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(SCRIPT)]
    for p in obs_paths:
        cmd += ["--observations", str(p)]
    cmd += ["--output", str(output), *extra]
    env = dict(os.environ, PYTHONPATH=str(REPO / "src"))
    return subprocess.run(cmd, capture_output=True, text=True, cwd=REPO, env=env)


def test_nc1_fame_field_trips_hard_gate(tmp_path):
    obs = _write_jsonl(tmp_path / "fame.jsonl", _multiversion_corpus())
    rows = [json.loads(line) for line in obs.read_text().splitlines()]
    for row in rows:
        row["proxy_metrics"]["arxiv:citation_count"] = 5.0
    _write_jsonl(obs, rows)
    proc = _run_operator([obs], tmp_path / "nc1.json")
    assert proc.returncode == 3, (proc.returncode, proc.stderr[-300:])
    assert "HARD GATE violated: fame fields" in proc.stderr


def test_nc2_head_only_input_has_no_transitions(tmp_path):
    # head-only rows (one observation per trajectory) are the SD10 shape:
    # version transitions require >= 2 steps within a trajectory.
    head_only = [_version_observation(f"2401.{10000 + i:05d}", 3, 1200.0)
                 for i in range(40)]
    obs = _write_jsonl(tmp_path / "head.jsonl", head_only)
    proc = _run_operator([obs], tmp_path / "nc2.json")
    assert proc.returncode == 3, (proc.returncode, proc.stderr[-300:])
    assert "no transitions" in proc.stderr


def test_nc3_seeded_run_is_byte_deterministic(tmp_path):
    obs = _write_jsonl(tmp_path / "det.jsonl", _multiversion_corpus())
    out1, out2 = tmp_path / "det1.json", tmp_path / "det2.json"
    for outp in (out1, out2):
        proc = _run_operator([obs], outp)
        assert proc.returncode == 0, proc.stderr[-300:]
    assert out1.read_bytes() == out2.read_bytes()
    receipt = json.loads(out1.read_text())
    assert receipt["classification"] == "BOUNDED_PILOT_INTERIM__NO_TERMINAL_CLAIM"


def test_nc4_missing_metrics_are_censored_never_defaulted(tmp_path):
    # NC4a: head steps carrying ONLY author_count (the exact SD10-head shape
    # that produced V1's deterministic artifact labels) have their head-arrival
    # transition CENSORED and counted; the v1->v2 transitions (full metrics)
    # still run.
    rows = _multiversion_corpus(40)
    thin = []
    for row in rows:
        if row["ordinal"] == 2:  # head steps: SD10 snapshot shape
            row = dict(row, proxy_metrics={
                "arxiv:author_count": row["proxy_metrics"]["arxiv:author_count"]})
        thin.append(row)
    obs = _write_jsonl(tmp_path / "thin.jsonl", thin)
    proc = _run_operator([obs], tmp_path / "nc4a.json")
    assert proc.returncode == 0, proc.stderr[-300:]
    receipt = json.loads((tmp_path / "nc4a.json").read_text())
    # 40 trajectories x 2 transitions = 80 candidate; the 40 head-arrivals
    # lack abstract_chars + updated_epoch_days on the next step -> censored.
    assert receipt["population"]["transitions_total"] == 40
    assert receipt["population"]["transitions_censored_missing_metric"] == 40
    detail = receipt["population"]["censor_detail"]
    assert detail["censored_missing:arxiv:abstract_chars"] == 40
    assert detail["censored_missing:arxiv:updated_epoch_days"] == 40
    assert receipt["hard_gates"]["no_missing_metric_silent_defaults"] is True
    # NC4b: nothing labelable at all -> exit 3, no fabricated-label run.
    allthin = [dict(row, proxy_metrics={"arxiv:author_count": 1.0}) for row in rows]
    obs2 = _write_jsonl(tmp_path / "allthin.jsonl", allthin)
    proc2 = _run_operator([obs2], tmp_path / "nc4b.json")
    assert proc2.returncode == 3, (proc2.returncode, proc2.stderr[-300:])
    assert "no transitions" in proc2.stderr
    assert "CENSORED" in proc2.stderr


def test_nc5_variant_alphabet_skips_lesson_arms_deterministically(tmp_path):
    obs = _write_jsonl(tmp_path / "corpus.jsonl", _multiversion_corpus())
    out1, out2 = tmp_path / "var1.json", tmp_path / "var2.json"
    for outp in (out1, out2):
        proc = _run_operator([obs], outp, "--alphabet", "coarse9",
                             "--context", "category")
        assert proc.returncode == 0, proc.stderr[-300:]
    assert out1.read_bytes() == out2.read_bytes()
    receipt = json.loads(out1.read_text())
    assert receipt["population"]["alphabet_cells"] == 9
    assert receipt["population"]["alphabet_mode"] == "coarse9"
    assert receipt["population"]["context_mode"] == "category"
    assert set(receipt["skipped_arms"]) == {
        "FIXED_META_LESSON_INJECTION__abstract_grows",
        "FIXED_META_LESSON_INJECTION__authors_nondecreasing",
        "FIXED_META_LESSON_INJECTION__gaps_lengthen",
        "F0_META_PARENT_FEDERATION"}
    assert receipt["arm_status"]["F0_META_PARENT_FEDERATION"] == "SKIPPED_ALPHABET_VARIANT"
    assert "TEMPORAL_SEQUENCE_MODEL_PARENT" in receipt["heldout_transition_prediction"]["per_arm"]
    assert "F0_META_PARENT_FEDERATION" not in receipt["heldout_transition_prediction"]["per_arm"]

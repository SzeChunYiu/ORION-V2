"""Mutation tests for scripts/pr_merge_gate.py: every field must be able to fail,
could-not-check must stay distinct from pass and fail, and the freeze-binding
scan must refuse a planted binding, stay quiet on a clean PR, and -- when the
history is present -- refuse the real #282/#276 pair and pass the real #289."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "pr_merge_gate.py"

spec = importlib.util.spec_from_file_location("pr_merge_gate", SCRIPT)
G = importlib.util.module_from_spec(spec)
sys.modules["pr_merge_gate"] = G  # dataclasses resolve the module through sys.modules
spec.loader.exec_module(G)


def _run(name, status, concl):
    return {"__typename": "CheckRun", "name": name, "status": status, "conclusion": concl}


def _snap(**over):
    base = {"state": "OPEN", "mergeable": "MERGEABLE", "isDraft": False, "baseRefName": "main",
            "statusCheckRollup": [_run("ci", "COMPLETED", "SUCCESS")]}
    base.update(over)
    return base


def _eval(pr, **kw):
    kw.setdefault("default_branch", "main")
    return G.evaluate_snapshot(pr, **kw)


def _code(pr, **kw):
    try:
        return G.decide(_eval(pr, **kw))
    except G.CouldNotCheck:
        return G.EXIT_COULD_NOT_CHECK


# ---- fields 1-4: mutation table -------------------------------------------

def test_clean_snapshot_passes():
    assert _code(_snap()) == 0


@pytest.mark.parametrize("mutation,expected", [
    ({"state": "MERGED"}, 1),
    ({"state": "CLOSED"}, 1),
    ({"mergeable": "CONFLICTING"}, 1),
    ({"mergeable": "UNKNOWN"}, 2),
    ({"isDraft": True}, 1),
    ({"statusCheckRollup": [_run("ci", "COMPLETED", "FAILURE")]}, 1),
    ({"statusCheckRollup": [_run("ci", "COMPLETED", "TIMED_OUT")]}, 1),
    ({"statusCheckRollup": [_run("ci", "COMPLETED", "ACTION_REQUIRED")]}, 1),
    ({"statusCheckRollup": [_run("ci", "COMPLETED", "STARTUP_FAILURE")]}, 1),
    ({"statusCheckRollup": [_run("ci", "COMPLETED", "CANCELLED")]}, 2),
    ({"statusCheckRollup": [_run("ci", "IN_PROGRESS", None)]}, 2),
    ({"statusCheckRollup": [_run("ci", "QUEUED", None)]}, 2),
    ({"statusCheckRollup": [{"__typename": "StatusContext", "context": "ext", "state": "PENDING"}]}, 2),
    ({"statusCheckRollup": [{"__typename": "StatusContext", "context": "ext", "state": "FAILURE"}]}, 1),
    ({"statusCheckRollup": [{"__typename": "StatusContext", "context": "ext", "state": "ERROR"}]}, 1),
    ({"statusCheckRollup": []}, 2),
])
def test_each_field_can_fail(mutation, expected):
    assert _code(_snap(**mutation)) == expected


def test_one_bad_check_among_good_ones_fails():
    checks = [_run("a", "COMPLETED", "SUCCESS"), _run("b", "COMPLETED", "SKIPPED"), _run("c", "COMPLETED", "FAILURE")]
    fields = _eval(_snap(statusCheckRollup=checks))
    assert fields[4].status == G.FAIL
    assert "c=FAILURE" in " ".join(fields[4].notes)


def test_planted_cancelled_check_is_could_not_check_with_rerun_advice():
    # three PRs read "red" on cancelled runs in one hour; the cause was a job cap, not the code
    checks = [_run("a", "COMPLETED", "SUCCESS"), _run("unified-reference", "COMPLETED", "CANCELLED")]
    fields = _eval(_snap(statusCheckRollup=checks))
    assert fields[4].status == G.CNC
    assert G.decide(fields) == 2
    joined = " ".join(fields[4].notes)
    assert "unified-reference=CANCELLED" in joined and G.RERUN_ADVICE in joined


def test_cancelled_never_reads_as_pass_or_fail():
    fields = _eval(_snap(statusCheckRollup=[_run("ci", "COMPLETED", "CANCELLED")]))
    assert fields[4].status not in (G.PASS, G.FAIL)


def test_failure_beside_cancelled_is_a_failure():
    checks = [_run("a", "COMPLETED", "CANCELLED"), _run("b", "COMPLETED", "FAILURE")]
    assert _code(_snap(statusCheckRollup=checks)) == 1


def test_definite_failure_dominates_could_not_check():
    # draft + cancelled: the merge is refused either way, and the report names field 3
    fields = _eval(_snap(isDraft=True, statusCheckRollup=[_run("ci", "COMPLETED", "CANCELLED")]))
    assert G.decide(fields) == 1
    assert fields[3].status == G.FAIL and fields[4].status == G.CNC


def test_neutral_is_not_a_failure_but_is_surfaced_as_not_assessed():
    checks = [_run("Cursor Bugbot", "COMPLETED", "NEUTRAL")]
    fields = _eval(_snap(statusCheckRollup=checks))
    assert fields[4].ok
    assert any("NOT ASSESSED" in n and "Cursor Bugbot" in n for n in fields[4].notes)


def test_unknown_on_a_merged_pr_is_field_1_not_could_not_check():
    # closed/merged PRs report UNKNOWN forever; that is state's failure, not an unreadable field 2
    assert _code(_snap(state="MERGED", mergeable="UNKNOWN")) == 1


def test_missing_key_is_could_not_check_never_pass():
    assert _code({"state": "OPEN", "mergeable": "MERGEABLE"}) == 2


def test_zero_checks_needs_an_explicit_waiver():
    assert _code(_snap(statusCheckRollup=[])) == 2
    assert _code(_snap(statusCheckRollup=[]), allow_no_checks=True) == 0


def test_job_detail_is_asked_only_for_non_passing_checks():
    asked = []
    checks = [_run("ok", "COMPLETED", "SUCCESS"), _run("bad", "COMPLETED", "FAILURE"), _run("cx", "COMPLETED", "CANCELLED")]
    _eval(_snap(statusCheckRollup=checks), job_detail=lambda c: asked.append(c["name"]) or "detail")
    assert asked == ["bad", "cx"]


def test_describe_job_without_locator_does_not_raise():
    assert "no jobs-API locator" in G.describe_job({"detailsUrl": "https://cursor.com/docs/bugbot"})


# ---- field 0: base branch == default ---------------------------------------

def test_field0_is_checked_first_and_passes_on_default():
    fields = _eval(_snap())
    assert fields[0].number == 0 and fields[0].status == G.PASS


@pytest.mark.parametrize("base", ["research/other-open-20260904", "research/ocm-convergence-map-20260904"])
def test_field0_other_or_landed_base_fails_with_retarget_message(base):
    fields = _eval(_snap(baseRefName=base))
    assert fields[0].status == G.FAIL
    assert fields[0].detail == G.BASE_RETARGET_MSG.format(base=base, default="main")
    assert G.decide(fields) == 1


def test_field0_missing_base_is_could_not_check():
    pr = _snap(); del pr["baseRefName"]
    assert _code(pr) == 2


def test_field0_default_branch_unreadable_is_could_not_check():
    assert _code(_snap(), default_branch=None) == 2


def test_field0_is_read_from_the_api_not_hardcoded():
    # a repository whose default branch is not `main`: a `main`-targeted PR fails, a `trunk` one passes
    assert _code(_snap(baseRefName="main"), default_branch="trunk") == 1
    assert _code(_snap(baseRefName="trunk"), default_branch="trunk") == 0


def test_field0_carries_base_info_note():
    fields = _eval(_snap(baseRefName="research/x"), base_info="base branch 'research/x' exists at deadbeef; ancestor of main: yes")
    assert any("ancestor of main: yes" in n for n in fields[0].notes)


# ---- field 0 replays: recorded API snapshots of the real PRs -----------------
# #290 as it stood before its merge (state OPEN restored; every other field from the API record):
# base = research/ocm-convergence-map-20260904, the #289 branch, already landed -> merged as 54712cc0,
# not an ancestor of main. FM40 stranding class recurring (#187/#215).

PR_290_PREMERGE = {"number": 290, "state": "OPEN", "mergeable": "MERGEABLE", "isDraft": False,
                   "baseRefName": "research/ocm-convergence-map-20260904", "headRefOid": "2d8cd1dd",
                   "statusCheckRollup": [_run("reference-tests", "COMPLETED", "SUCCESS")]}
PR_296_RELAND = {"number": 296, "state": "OPEN", "mergeable": "MERGEABLE", "isDraft": False,
                 "baseRefName": "main", "headRefOid": "572785ca",
                 "statusCheckRollup": [_run("reference-tests", "COMPLETED", "SUCCESS")]}
PR_289_CONTROL = {"number": 289, "state": "OPEN", "mergeable": "MERGEABLE", "isDraft": False,
                  "baseRefName": "main", "headRefOid": "3a96e2ad",
                  "statusCheckRollup": [_run("reference-tests", "COMPLETED", "SUCCESS")]}


def test_replay_290_premerge_is_refused_on_field0():
    fields = _eval(PR_290_PREMERGE)
    assert fields[0].status == G.FAIL and "retarget to main" in fields[0].detail
    assert all(f.status == G.PASS for f in fields[1:])   # fields 1-4 were green: field 0 is the only refusal
    assert G.decide(fields) == 1


def test_replay_296_reland_passes_field0():
    assert _code(PR_296_RELAND) == 0


def test_replay_289_control_passes_field0():
    assert _code(PR_289_CONTROL) == 0


# ---- field 5: synthetic repository -----------------------------------------

def _git(repo: Path, *args):
    return subprocess.run([G.GIT, "-C", str(repo), *args], check=True, capture_output=True).stdout.decode()


@pytest.fixture
def synthetic_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "gate@test")
    _git(repo, "config", "user.name", "gate")
    (repo / "lane").mkdir()
    (repo / "lane" / "arms.py").write_text("ARMS = 1\n")
    (repo / "lane" / "free.py").write_text("FREE = 1\n")
    (repo / "lane" / "run.py").write_text("RUN = 1\n")
    (repo / "lane" / "old.py").write_text("OLD = 2\n")
    (repo / "lane" / "custody.txt").write_text("CUSTODY\n")
    digest = hashlib.sha256(b"ARMS = 1\n").hexdigest()
    (repo / "lane" / "LANE_FREEZE_V1.json").write_text(json.dumps({"v1_arms_py_sha256": digest}))
    # a freeze that is already stale on the base: it pins old.py at a digest old.py no longer has
    (repo / "lane" / "OLD_FREEZE_V1.json").write_text(json.dumps(
        {"source_files_sha256": {"lane/old.py": hashlib.sha256(b"OLD = 1\n").hexdigest()}}))
    # a provenance receipt (not freeze-class) naming run.py at its current digest
    (repo / "lane" / "RUN_RECEIPT.json").write_text(json.dumps(
        {"source_provenance": {"source_files_sha256": {"lane/run.py": hashlib.sha256(b"RUN = 1\n").hexdigest()}}}))
    custody_digest = hashlib.sha256(b"CUSTODY\n").hexdigest()
    (repo / "lane" / "SHA256SUMS").write_text(f"{custody_digest}  custody.txt\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "freeze (#1)")
    base = _git(repo, "rev-parse", "HEAD").strip()
    return repo, base


def _branch(repo, name, edits: dict[str, str], msg="edit"):
    _git(repo, "checkout", "-q", "main")
    _git(repo, "checkout", "-q", "-b", name)
    for rel, text in edits.items():
        (repo / rel).write_text(text)
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", msg)


def test_planted_json_binding_is_refused_and_names_freeze_and_owner(synthetic_repo):
    repo, base = synthetic_repo
    _branch(repo, "pr-a", {"lane/arms.py": "ARMS = 2\n"})
    bindings = G.scan_freeze_bindings(repo, base, "pr-a", ["lane/arms.py"])
    live = [b for b in bindings if b.refuses]
    assert live, bindings
    assert live[0].binder == "lane/LANE_FREEZE_V1.json" and live[0].binder_class == "FREEZE"
    assert live[0].kind == "DIGEST" and live[0].where == "v1_arms_py_sha256"
    assert "freeze (#1)" in live[0].owner and "gate" in live[0].owner
    assert G.field5_result(bindings).status == G.FAIL


def test_planted_sha256sums_binding_is_refused(synthetic_repo):
    repo, base = synthetic_repo
    _branch(repo, "pr-s", {"lane/custody.txt": "CUSTODY 2\n"})
    bindings = G.scan_freeze_bindings(repo, base, "pr-s", ["lane/custody.txt"])
    assert any(b.refuses and b.binder == "lane/SHA256SUMS" for b in bindings), bindings


def test_clean_pr_raises_no_alarm(synthetic_repo):
    repo, base = synthetic_repo
    _branch(repo, "pr-b", {"lane/free.py": "FREE = 2\n"})
    assert G.scan_freeze_bindings(repo, base, "pr-b", ["lane/free.py"]) == []


def test_coherent_rebind_in_same_pr_passes_but_is_reported(synthetic_repo):
    repo, base = synthetic_repo
    new = "ARMS = 3\n"
    _branch(repo, "pr-c", {
        "lane/arms.py": new,
        "lane/LANE_FREEZE_V1.json": json.dumps({"v1_arms_py_sha256": hashlib.sha256(new.encode()).hexdigest()}),
    })
    bindings = G.scan_freeze_bindings(repo, base, "pr-c", ["lane/arms.py", "lane/LANE_FREEZE_V1.json"])
    assert bindings and all(b.status == "REBOUND_IN_PR" for b in bindings)
    assert G.field5_result(bindings).ok


def test_incoherent_rebind_still_refuses(synthetic_repo):
    # the PR touches the freeze but pins a digest that is not the new content's
    repo, base = synthetic_repo
    _branch(repo, "pr-d", {
        "lane/arms.py": "ARMS = 4\n",
        "lane/LANE_FREEZE_V1.json": json.dumps({"v1_arms_py_sha256": "0" * 64}),
    })
    bindings = G.scan_freeze_bindings(repo, base, "pr-d", ["lane/arms.py", "lane/LANE_FREEZE_V1.json"])
    assert any(b.refuses for b in bindings)


def test_provenance_record_is_surfaced_not_refused_unless_strict(synthetic_repo):
    # on main the ME-F1 calibration receipt names a digest main no longer has and main is green:
    # receipts record what a run saw; they do not pin
    repo, base = synthetic_repo
    _branch(repo, "pr-r", {"lane/run.py": "RUN = 2\n"})
    bindings = G.scan_freeze_bindings(repo, base, "pr-r", ["lane/run.py"])
    assert bindings and all(b.status == "PROVENANCE" and b.binder == "lane/RUN_RECEIPT.json" for b in bindings)
    f5 = G.field5_result(bindings)
    assert f5.ok and any("provenance record" in n for n in f5.notes)
    strict = G.scan_freeze_bindings(repo, base, "pr-r", ["lane/run.py"], strict=True)
    assert any(b.refuses for b in strict)


def test_freeze_already_stale_on_base_is_surfaced_not_refused(synthetic_repo):
    repo, base = synthetic_repo
    _branch(repo, "pr-o", {"lane/old.py": "OLD = 3\n"})
    bindings = G.scan_freeze_bindings(repo, base, "pr-o", ["lane/old.py"])
    assert bindings and all(b.status == "STALE_ON_BASE" for b in bindings)
    assert G.field5_result(bindings).ok


def test_empty_file_digest_binds_nothing(synthetic_repo):
    # e3b0c442... is the sha256 of the empty string; a freeze carrying it must not pin every empty file
    repo, base = synthetic_repo
    (repo / "lane" / "empty.txt").write_text("")
    (repo / "lane" / "EMPTY_FREEZE_V1.json").write_text(json.dumps({"x_sha256": G.SHA256_OF_EMPTY}))
    _git(repo, "add", "."); _git(repo, "commit", "-q", "-m", "empty")
    base2 = _git(repo, "rev-parse", "HEAD").strip()
    _branch(repo, "pr-e", {"lane/empty.txt": "now non-empty\n"})
    assert G.scan_freeze_bindings(repo, base2, "pr-e", ["lane/empty.txt"]) == []


def test_unreadable_base_ref_is_could_not_check(synthetic_repo):
    repo, _ = synthetic_repo
    with pytest.raises(G.CouldNotCheck):
        G.scan_freeze_bindings(repo, "no-such-ref", None, ["lane/arms.py"])


def test_repo_without_binders_is_could_not_check_unless_waived(tmp_path):
    repo = tmp_path / "bare"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "gate@test")
    _git(repo, "config", "user.name", "gate")
    (repo / "a.py").write_text("A = 1\n")
    _git(repo, "add", "."); _git(repo, "commit", "-q", "-m", "init")
    with pytest.raises(G.CouldNotCheck):
        G.scan_freeze_bindings(repo, "HEAD", None, ["a.py"])
    assert G.scan_freeze_bindings(repo, "HEAD", None, ["a.py"], allow_no_binders=True) == []


def test_grep_control_failure_is_could_not_check(synthetic_repo, monkeypatch):
    repo, base = synthetic_repo
    monkeypatch.setattr(G, "git_grep_files", lambda *a, **k: [])  # grep that silently finds nothing
    with pytest.raises(G.CouldNotCheck, match="grep control"):
        G.scan_freeze_bindings(repo, base, None, ["lane/arms.py"])


# ---- CLI exit codes ----------------------------------------------------------

def test_cli_self_test_exits_zero():
    proc = subprocess.run([sys.executable, str(SCRIPT), "--self-test"], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "self-test passed" in proc.stdout


def test_cli_replay_exit_codes(synthetic_repo):
    repo, base = synthetic_repo
    _branch(repo, "pr-a", {"lane/arms.py": "ARMS = 2\n"})
    refused = subprocess.run([sys.executable, str(SCRIPT), "--replay", "--git-dir", str(repo),
                              "--base-ref", base, "--head-ref", "pr-a"], capture_output=True, text=True)
    assert refused.returncode == 1 and "REFUSE" in refused.stdout and "LANE_FREEZE_V1.json" in refused.stdout
    _branch(repo, "pr-b", {"lane/free.py": "FREE = 2\n"})
    clean = subprocess.run([sys.executable, str(SCRIPT), "--replay", "--git-dir", str(repo),
                            "--base-ref", base, "--head-ref", "pr-b"], capture_output=True, text=True)
    assert clean.returncode == 0, clean.stdout
    cnc = subprocess.run([sys.executable, str(SCRIPT), "--replay", "--git-dir", str(repo),
                          "--base-ref", "nope", "--head-ref", "pr-b"], capture_output=True, text=True)
    assert cnc.returncode == 2 and "COULD NOT CHECK" in cnc.stderr


# ---- replay against the real incident --------------------------------------

INCIDENT_BASE = "d696d7466a804ea8ceeaf93ba5eec0e288cd7ac2"   # main right before #276 merged; holds #282's freeze
INCIDENT_HEAD = "dc27ced"                                     # #276 as squash-merged
INCIDENT_FREEZE = "research/experiments/me-f1-r3/results/ME_F1_R3_FREEZE_V1.json"
CONTROL_BASE = "d1dfd12"                                      # main right before #289 merged (after the #286 repair)
CONTROL_HEAD = "b53dba5"                                      # #289 as squash-merged: one new file, nothing pins it


def _has_commit(sha: str) -> bool:
    return subprocess.run([G.GIT, "-C", str(ROOT), "cat-file", "-e", f"{sha}^{{commit}}"],
                          capture_output=True).returncode == 0


def _need_history(*shas):
    if not all(_has_commit(s) for s in shas):
        if os.environ.get("PR_MERGE_GATE_REQUIRE_HISTORY"):
            pytest.fail("incident commits not in this checkout; fetch full history")
        pytest.skip("incident commits not in this checkout (shallow clone); replay not run here")


def test_replay_refuses_pr_276_against_the_282_freeze():
    _need_history(INCIDENT_BASE, INCIDENT_HEAD)
    changed = G.git_changed_paths(ROOT, INCIDENT_BASE, INCIDENT_HEAD)
    assert "research/experiments/me-f1/mef1_arms.py" in changed
    bindings = G.scan_freeze_bindings(ROOT, INCIDENT_BASE, INCIDENT_HEAD, changed)
    live = [b for b in bindings if b.refuses]
    assert any(b.changed_path == "research/experiments/me-f1/mef1_arms.py"
               and b.binder == INCIDENT_FREEZE and b.where == "v1_arms_py_sha256" for b in live), live
    assert any("#282" in b.owner for b in live if b.binder == INCIDENT_FREEZE)
    assert G.field5_result(bindings).status == G.FAIL


def test_replay_passes_pr_289_no_alarm_control():
    _need_history(CONTROL_BASE, CONTROL_HEAD)
    changed = G.git_changed_paths(ROOT, CONTROL_BASE, CONTROL_HEAD)
    assert changed == ["research/orion-machine/CONVERGENCE_MAP_V1.md"]
    bindings = G.scan_freeze_bindings(ROOT, CONTROL_BASE, CONTROL_HEAD, changed)
    assert not [b for b in bindings if b.refuses]
    assert G.field5_result(bindings).ok

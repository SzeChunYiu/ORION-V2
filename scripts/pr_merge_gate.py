#!/usr/bin/env python3
"""Five-field merge gate for a pull request, with a distinct could-not-check exit.

A merge decision branches on five fields. Each one is here because a merge
that omitted it went wrong in this repository:

    1. state == OPEN
    2. mergeable == MERGEABLE          (UNKNOWN is polled, never passed or failed)
    3. isDraft == false                (#244 and #254 sat green and unmergeable
                                        for an hour; the gate never asked)
    4. every check COMPLETED with conclusion in {SUCCESS, NEUTRAL, SKIPPED}.
       Three states, not two:
         SUCCESS / NEUTRAL / SKIPPED        -> pass (NEUTRAL is surfaced as
                                              NOT ASSESSED, never as reviewed:
                                              a review bot produced two false
                                              greens in one day)
         FAILURE / TIMED_OUT /
         ACTION_REQUIRED / STARTUP_FAILURE  -> fail, naming the check
         CANCELLED, or status != COMPLETED  -> could not check. A cancellation
                                              is not evidence the code is
                                              wrong (three PRs read "red" on
                                              cancelled runs; two lanes nearly
                                              debugged non-existent failures;
                                              the cause was a job cap). The
                                              advice is: re-run the workflow
                                              on this head.
       Step-level detail comes from the jobs API, never from
       `gh run view --log-failed`, which is empty on a cancelled run by design
       (no step failed) and returned 0 bytes on three genuinely failing runs.
    5. the PR changes no path that a live freeze on the base branch pins by
       digest.  #282 froze ME_F1_R3_FREEZE_V1.json binding mef1_arms.py by
       sha256; 70 minutes later #276 changed mef1_arms.py and was merged. Both
       were individually green. main went red on
       test_frozen_state_if_present_matches_inputs and stayed red for hours.
       No per-PR check can see a pair; this field scans the base branch at
       merge time.

       Binders come in two classes. Freeze-class binders (`*FREEZE*.json`,
       `SHA256SUMS`, `PACKAGE_MANIFEST*.json`, `*EXPECTED_CUSTODY*.json`) pin
       by contract and a current binding there REFUSES the merge.
       Provenance-class binders (any other JSON carrying a `*sha256*` key) are
       receipts of what a past run saw; on main today the ME-F1 calibration
       receipt and the G0E reports name a digest of mef1_arms.py that main no
       longer has, and main is green, so they are demonstrably not enforced.
       They are SURFACED, not refused, unless --strict is given. A binder that
       is already stale on the base (its digest is not the base content's)
       cannot be made worse by this PR and is surfaced, not refused.

Exit codes, deliberately three and never collapsed:

    0  all five fields hold
    1  a field fails (the output names which); a definite failure dominates a
       could-not-check elsewhere because the merge is refused either way
    2  could not check: the API was unreadable, mergeable stayed UNKNOWN after
       the polls, a check was cancelled or is still running, the freeze scan
       could not run, or a must-match control inside the scan did not match

Usage:

    pr_merge_gate.py --pr N [--repo OWNER/REPO] [--git-dir DIR] [--base-ref origin/main]
    pr_merge_gate.py --replay --git-dir DIR --base-ref REF --head-ref REF   (field 5 only, from history)
    pr_merge_gate.py --self-test

Field 5 is evaluated against the base ref as it is *now* (fetched fresh unless
--no-fetch), because that is the only frame in which the pair is visible.
State the ref you measured at: the report prints it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

GIT = "/usr/bin/git" if Path("/usr/bin/git").exists() else "git"

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_COULD_NOT_CHECK = 2

PASS, FAIL, CNC = "PASS", "FAIL", "COULD_NOT_CHECK"

HEX64 = re.compile(r"^[0-9a-f]{64}$")
SHA256_OF_EMPTY = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

# Check-run conclusions, three ways.
PASSING_CONCLUSIONS = {"SUCCESS", "NEUTRAL", "SKIPPED"}
NOT_ASSESSED_CONCLUSIONS = {"NEUTRAL"}
FAILING_CONCLUSIONS = {"FAILURE", "TIMED_OUT", "ACTION_REQUIRED", "STARTUP_FAILURE", "STALE"}
CNC_CONCLUSIONS = {"CANCELLED"}
RERUN_ADVICE = "re-run the workflow on this head (a cancellation is not evidence about the code)"

# Freeze-class binders: pin by contract; a current binding refuses. Matched on
# the basename, case-insensitively.
FREEZE_CLASS_PATTERNS = (
    re.compile(r"freeze.*\.json$", re.I),
    re.compile(r"sha256sums", re.I),
    re.compile(r"package_manifest.*\.json$", re.I),
    re.compile(r"_expected_custody.*\.json$", re.I),
)
# Provenance-class binders: any other JSON carrying a `*sha256*` key.
SHA256_KEY_GREP = r'"[A-Za-z0-9_]*sha256[A-Za-z0-9_]*"[[:space:]]*:'
SHA256_KEY_RE = re.compile(r"sha256", re.I)

JOB_URL_RE = re.compile(r"github\.com/([^/]+)/([^/]+)/actions/runs/(\d+)/job/(\d+)")


class CouldNotCheck(Exception):
    """Distinct from a failed field; becomes exit 2."""


@dataclass
class FieldResult:
    number: int
    name: str
    status: str            # PASS / FAIL / COULD_NOT_CHECK
    detail: str
    notes: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.status == PASS


@dataclass
class Binding:
    changed_path: str
    binder: str
    binder_class: str      # FREEZE or PROVENANCE
    kind: str              # DIGEST (binder holds the base content's digest) or NAME_PIN (names the path with another digest)
    where: str             # key path / line inside the binder
    owner: str             # last commit touching the binder on the base ref
    status: str            # LIVE / REBOUND_IN_PR / STALE_ON_BASE / PROVENANCE

    @property
    def refuses(self) -> bool:
        return self.status == "LIVE"


# --------------------------------------------------------------------------
# git plumbing (subprocess only -- a `git show` inside a shell loop has written
# 0 bytes on this machine)
# --------------------------------------------------------------------------

def _git(git_dir: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run([GIT, "-C", str(git_dir), *args], capture_output=True)
    if check and proc.returncode != 0:
        raise CouldNotCheck(
            f"git {' '.join(args[:3])}... failed ({proc.returncode}): "
            f"{proc.stderr.decode(errors='replace').strip()[:300]}"
        )
    return proc


def git_show_bytes(git_dir: Path, ref: str, path: str) -> bytes | None:
    proc = _git(git_dir, "show", f"{ref}:{path}", check=False)
    if proc.returncode != 0:
        return None
    return proc.stdout


def git_ls_tree(git_dir: Path, ref: str) -> list[str]:
    out = _git(git_dir, "ls-tree", "-r", "--name-only", "-z", ref).stdout
    return [p.decode() for p in out.split(b"\0") if p]


def git_grep_files(git_dir: Path, ref: str, needles: list[str], paths: list[str] | None,
                   fixed: bool = True) -> list[str]:
    """Files under `ref` containing any needle. Empty needle list -> []."""
    if not needles:
        return []
    args = ["grep", "-l", "-z", "-F" if fixed else "-E"]
    for n in needles:
        args += ["-e", n]
    args += [ref]
    if paths is not None:
        if not paths:
            return []
        args += ["--", *paths]
    proc = _git(git_dir, *args, check=False)
    if proc.returncode not in (0, 1):
        raise CouldNotCheck(
            f"git grep failed ({proc.returncode}): {proc.stderr.decode(errors='replace')[:300]}"
        )
    files = []
    for item in proc.stdout.split(b"\0"):
        if not item:
            continue
        s = item.decode()
        files.append(s.split(":", 1)[1] if ":" in s else s)
    return files


def git_changed_paths(git_dir: Path, base_ref: str, head_ref: str) -> list[str]:
    out = _git(git_dir, "diff", "--name-only", "-z", f"{base_ref}...{head_ref}").stdout
    paths = [p.decode() for p in out.split(b"\0") if p]
    if not paths:
        # `base...head` needs a merge base; a squash commit on the base branch has none
        # beyond its parent, so fall back to a two-dot diff.
        out = _git(git_dir, "diff", "--name-only", "-z", base_ref, head_ref).stdout
        paths = [p.decode() for p in out.split(b"\0") if p]
    return paths


def git_owner(git_dir: Path, ref: str, path: str) -> str:
    """`<sha> #<pr> <author> <subject>` for the last commit touching `path` on `ref`.

    The squash-merge PR number is pulled out of the subject's trailing `(#N)`
    and placed first, so it survives the subject being cut short.
    """
    proc = _git(git_dir, "log", "-1", "--format=%h%x00%an <%ae>%x00%s", ref, "--", path, check=False)
    text = proc.stdout.decode(errors="replace").strip()
    if not text:
        return "(no commit found)"
    sha, author, subject = (text.split("\x00", 2) + ["", ""])[:3]
    m = re.search(r"\(#(\d+)\)\s*$", subject)
    pr = f"#{m.group(1)} " if m else ""
    return f"{sha} {pr}{author} {subject[:120]}"


# --------------------------------------------------------------------------
# field 5: freeze-binding scan
# --------------------------------------------------------------------------

def is_freeze_class(path: str) -> bool:
    name = path.rsplit("/", 1)[-1]
    return any(p.search(name) for p in FREEZE_CLASS_PATTERNS)


def path_needles(path: str) -> list[str]:
    parts = path.split("/")
    needles = [path]
    if len(parts) >= 2:
        needles.append("/".join(parts[-2:]))
    return needles


def _walk_json(obj, trail: str, path_needles_: list[str], digest: str | None,
               out: list[tuple[str, str]]) -> None:
    """Collect (kind, where) bindings inside a parsed JSON object.

    DIGEST:   any string value equal to the changed path's base-content digest.
    NAME_PIN: a key equal to the path (or its two-component suffix) whose value
              is a 64-hex digest, or a dict that names the path in a value and
              carries a *sha256* key beside it.
    """
    if isinstance(obj, dict):
        names_path = any(isinstance(v, str) and v in path_needles_ for v in obj.values())
        has_sha_key = any(SHA256_KEY_RE.search(k) for k in obj)
        if names_path and has_sha_key:
            out.append(("NAME_PIN", trail or "$"))
        for k, v in obj.items():
            here = f"{trail}.{k}" if trail else k
            if k in path_needles_ and isinstance(v, str) and HEX64.match(v):
                out.append(("NAME_PIN", here))
            if digest and isinstance(v, str) and v == digest:
                out.append(("DIGEST", here))
            _walk_json(v, here, path_needles_, digest, out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            here = f"{trail}[{i}]"
            if digest and isinstance(v, str) and v == digest:
                out.append(("DIGEST", here))
            _walk_json(v, here, path_needles_, digest, out)


def _scan_text_lines(text: str, path_needles_: list[str], digest: str | None) -> list[tuple[str, str]]:
    """SHA256SUMS-style binders: `<hex64>  <path>` lines."""
    out = []
    for lineno, line in enumerate(text.splitlines(), 1):
        m = re.match(r"^\s*([0-9a-f]{64})\s+\*?(.+?)\s*$", line)
        if not m:
            continue
        hexv, named = m.group(1), m.group(2)
        if digest and hexv == digest:
            out.append(("DIGEST", f"line {lineno}"))
        elif any(named == n or named.endswith("/" + n) or n.endswith("/" + named) for n in path_needles_):
            out.append(("NAME_PIN", f"line {lineno}"))
    return out


def bindings_in_binder(binder_bytes: bytes, binder_path: str, path_needles_: list[str],
                       digest: str | None) -> list[tuple[str, str]]:
    if binder_path.lower().endswith(".json"):
        try:
            data = json.loads(binder_bytes.decode())
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise CouldNotCheck(f"{binder_path}: binder is not readable JSON ({exc})") from exc
        found: list[tuple[str, str]] = []
        _walk_json(data, "", path_needles_, digest, found)
        return found
    return _scan_text_lines(binder_bytes.decode(errors="replace"), path_needles_, digest)


def collect_binders(git_dir: Path, base_ref: str) -> list[str]:
    tree = git_ls_tree(git_dir, base_ref)
    if not tree:
        raise CouldNotCheck(f"{base_ref}: ls-tree returned no paths; the ref is unreadable or empty")
    by_name = {p for p in tree if is_freeze_class(p)}
    by_key = set(git_grep_files(git_dir, base_ref, [SHA256_KEY_GREP], ["*.json"], fixed=False))
    return sorted(by_name | by_key)


def grep_control(git_dir: Path, base_ref: str, binders: list[str]) -> None:
    """Must-match control: prove `git grep` on this ref finds a digest we know is there.

    A scan that returned nothing because grep silently found nothing must not
    be read as "no bindings". Pick the first binder carrying a 64-hex string and
    require the grep to return it.
    """
    for b in binders[:50]:
        raw = git_show_bytes(git_dir, base_ref, b)
        if raw is None:
            continue
        m = re.search(rb"[0-9a-f]{64}", raw)
        if not m:
            continue
        hits = git_grep_files(git_dir, base_ref, [m.group(0).decode()], [b])
        if b not in hits:
            raise CouldNotCheck(
                f"grep control failed: {b} contains {m.group(0).decode()[:12]}... "
                "but `git grep` did not return it, so a zero from the scan is not believable"
            )
        return
    raise CouldNotCheck(
        "grep control could not be armed: no binder on the base ref carries a 64-hex digest"
    )


def _classify(binder: str, kind: str, rebound: bool, strict: bool) -> str:
    if rebound:
        return "REBOUND_IN_PR"
    if kind != "DIGEST":
        # The binder names the path but holds a digest the base content does
        # not have: it is already stale on the base and this PR cannot make it
        # worse. Surfaced, never refused.
        return "STALE_ON_BASE"
    if is_freeze_class(binder) or strict:
        return "LIVE"
    return "PROVENANCE"


def scan_freeze_bindings(git_dir: Path, base_ref: str, head_ref: str | None,
                         changed_paths: list[str], allow_no_binders: bool = False,
                         strict: bool = False) -> list[Binding]:
    """Return every binding a binder on `base_ref` holds over a changed path."""
    binders = collect_binders(git_dir, base_ref)
    if not binders:
        if allow_no_binders:
            return []
        raise CouldNotCheck(
            f"{base_ref}: no binder files (FREEZE/SHA256SUMS/PACKAGE_MANIFEST/EXPECTED_CUSTODY/"
            "*sha256*-carrying JSON) found; pass --allow-no-binders if this repository truly has none"
        )
    grep_control(git_dir, base_ref, binders)
    changed = set(changed_paths)
    results: list[Binding] = []

    for path in changed_paths:
        base_bytes = git_show_bytes(git_dir, base_ref, path)
        digest = hashlib.sha256(base_bytes).hexdigest() if base_bytes is not None else None
        if digest == SHA256_OF_EMPTY:
            digest = None  # the digest of nothing binds nothing
        needles = path_needles(path)
        hit_files = git_grep_files(git_dir, base_ref, needles + ([digest] if digest else []), binders)
        for binder in sorted(set(hit_files)):
            if binder == path:
                continue
            raw = git_show_bytes(git_dir, base_ref, binder)
            if raw is None:
                raise CouldNotCheck(f"{binder}: listed on {base_ref} but unreadable")
            found = bindings_in_binder(raw, binder, needles, digest)
            if not found:
                continue
            rebound = False
            if binder in changed and head_ref is not None:
                head_path = git_show_bytes(git_dir, head_ref, path)
                head_binder = git_show_bytes(git_dir, head_ref, binder)
                if head_path is not None and head_binder is not None:
                    head_digest = hashlib.sha256(head_path).hexdigest()
                    new = bindings_in_binder(head_binder, binder, needles, head_digest)
                    rebound = any(k == "DIGEST" for k, _ in new)
                elif head_path is None and head_binder is not None:
                    # the path was deleted and the binder no longer names it
                    rebound = not bindings_in_binder(head_binder, binder, needles, None)
            owner = git_owner(git_dir, base_ref, binder)
            binder_class = "FREEZE" if is_freeze_class(binder) else "PROVENANCE"
            # One row per binder: the strongest kind found decides the status.
            kind = "DIGEST" if any(k == "DIGEST" for k, _ in found) else "NAME_PIN"
            where = next(w for k, w in found if k == kind)
            results.append(Binding(path, binder, binder_class, kind, where, owner,
                                   _classify(binder, kind, rebound, strict)))
    return results


def field5_result(bindings: list[Binding], measured_at: str = "") -> FieldResult:
    live = [b for b in bindings if b.status == "LIVE"]
    rebound = [b for b in bindings if b.status == "REBOUND_IN_PR"]
    prov = [b for b in bindings if b.status == "PROVENANCE"]
    stale = [b for b in bindings if b.status == "STALE_ON_BASE"]
    notes = []
    for b in live:
        notes.append(f"REFUSE {b.changed_path} <- pinned by {b.binder} [{b.binder_class}, {b.kind} at {b.where}] "
                     f"owner: {b.owner}")
    for b in rebound:
        notes.append(f"rebound in this PR: {b.changed_path} <- {b.binder} [{b.kind} at {b.where}]")
    for b in prov:
        notes.append(f"provenance record (surfaced, not refused; --strict refuses): {b.changed_path} <- "
                     f"{b.binder} [{b.kind} at {b.where}] owner: {b.owner}")
    for b in stale:
        notes.append(f"already stale on base (not enforced there, or base is red): {b.changed_path} <- "
                     f"{b.binder} [{b.binder_class}, {b.where}]")
    detail = (f"{len(live)} live freeze binding(s), {len(rebound)} rebound in the same PR, "
              f"{len(prov)} provenance record(s), {len(stale)} already stale on base"
              + (f"; measured at {measured_at}" if measured_at else ""))
    return FieldResult(5, "no changed path is pinned by a live freeze on the base branch",
                       FAIL if live else PASS, detail, notes)


# --------------------------------------------------------------------------
# fields 1-4: pure evaluation of a PR snapshot
# --------------------------------------------------------------------------

def classify_check(c: dict) -> tuple[str, str, str]:
    """-> (name, bucket, label) with bucket in {pass, not_assessed, fail, cancelled, incomplete}."""
    name = c.get("name") or c.get("context") or "?"
    typename = c.get("__typename", "")
    if typename == "StatusContext" or ("state" in c and "status" not in c):
        st = str(c.get("state", "")).upper()
        if st in ("PENDING", "EXPECTED", ""):
            return name, "incomplete", f"{name}(state={st or 'none'})"
        if st == "SUCCESS":
            return name, "pass", name
        return name, "fail", f"{name}={st}"
    status = str(c.get("status", "")).upper()
    concl = str(c.get("conclusion") or "").upper()
    if status != "COMPLETED":
        return name, "incomplete", f"{name}(status={status or 'none'})"
    if concl in CNC_CONCLUSIONS:
        return name, "cancelled", f"{name}=CANCELLED"
    if concl in PASSING_CONCLUSIONS:
        return name, ("not_assessed" if concl in NOT_ASSESSED_CONCLUSIONS else "pass"), name
    return name, "fail", f"{name}={concl or 'no conclusion'}"


def evaluate_snapshot(pr: dict, allow_no_checks: bool = False,
                      job_detail=None) -> list[FieldResult]:
    """Fields 1-4 from a `gh pr view --json` snapshot.

    Raises CouldNotCheck only when the snapshot itself is unreadable or field 2
    is UNKNOWN on an open PR; every other could-not-check is a field status so
    the report still shows the other fields.
    """
    for key in ("state", "mergeable", "isDraft", "statusCheckRollup"):
        if key not in pr:
            raise CouldNotCheck(f"PR snapshot lacks '{key}'; the API response is not readable as a PR")

    out: list[FieldResult] = []
    state = str(pr["state"]).upper()
    out.append(FieldResult(1, "state == OPEN", PASS if state == "OPEN" else FAIL, f"state={state}"))

    mergeable = str(pr["mergeable"]).upper()
    if mergeable == "UNKNOWN" and state == "OPEN":
        raise CouldNotCheck("mergeable is UNKNOWN (GitHub has not computed it); poll, do not decide")
    # A closed or merged PR reports UNKNOWN forever; that is field 1's failure, not an unreadable field 2.
    out.append(FieldResult(2, "mergeable == MERGEABLE", PASS if mergeable == "MERGEABLE" else FAIL,
                           f"mergeable={mergeable}"))

    draft = bool(pr["isDraft"])
    out.append(FieldResult(3, "isDraft == false", FAIL if draft else PASS, f"isDraft={draft}"))

    checks = pr["statusCheckRollup"] or []
    name4 = "every check COMPLETED with conclusion in {SUCCESS,NEUTRAL,SKIPPED}"
    if not checks:
        if allow_no_checks:
            out.append(FieldResult(4, name4, PASS, "no checks reported (--allow-no-checks)"))
            return out
        out.append(FieldResult(4, name4, CNC, "no checks are reported for this PR; a zero here is not a pass",
                               ["pass --allow-no-checks only for a repository that runs none"]))
        return out
    buckets: dict[str, list[str]] = {"pass": [], "not_assessed": [], "fail": [], "cancelled": [], "incomplete": []}
    detail_notes: list[str] = []
    for c in checks:
        name, bucket, label = classify_check(c)
        buckets[bucket].append(label)
        if bucket in ("fail", "cancelled") and job_detail is not None:
            detail_notes.append(f"  {name}: {job_detail(c)}")
    if buckets["fail"]:
        status = FAIL
    elif buckets["cancelled"] or buckets["incomplete"]:
        status = CNC
    else:
        status = PASS
    detail = (f"{len(buckets['pass'])} passing, {len(buckets['not_assessed'])} NOT ASSESSED (neutral), "
              f"{len(buckets['fail'])} failing, {len(buckets['cancelled'])} cancelled, "
              f"{len(buckets['incomplete'])} incomplete")
    notes = []
    if buckets["not_assessed"]:
        notes.append("NOT ASSESSED (neutral: counted as not-failing, never as reviewed): "
                     + ", ".join(buckets["not_assessed"]))
    if buckets["fail"]:
        notes.append("failing: " + ", ".join(buckets["fail"]))
    if buckets["cancelled"]:
        notes.append("cancelled (could not check): " + ", ".join(buckets["cancelled"]) + " -- " + RERUN_ADVICE)
    if buckets["incomplete"]:
        notes.append("incomplete (could not check): " + ", ".join(buckets["incomplete"]) + " -- wait, then re-read")
    notes.extend(detail_notes)
    out.append(FieldResult(4, name4, status, detail, notes))
    return out


# --------------------------------------------------------------------------
# GitHub fetch (gh CLI) and the jobs API
# --------------------------------------------------------------------------

PR_JSON_FIELDS = "number,state,mergeable,isDraft,statusCheckRollup,files,headRefOid,baseRefName,url"


def _gh_json(args: list[str]) -> object:
    proc = subprocess.run(["gh", *args], capture_output=True)
    if proc.returncode != 0:
        raise CouldNotCheck(f"gh {' '.join(args[:2])} failed: {proc.stderr.decode(errors='replace').strip()[:300]}")
    try:
        return json.loads(proc.stdout.decode())
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CouldNotCheck(f"gh {' '.join(args[:2])} output is not JSON ({exc})") from exc


def fetch_pr(repo: str | None, number: int) -> dict:
    cmd = ["pr", "view", str(number), "--json", PR_JSON_FIELDS]
    if repo:
        cmd += ["--repo", repo]
    data = _gh_json(cmd)
    if not isinstance(data, dict) or "state" not in data:
        raise CouldNotCheck("gh pr view returned no PR object")
    return data


def fetch_pr_polling(repo: str | None, number: int, polls: int, interval: float) -> dict:
    last: dict = {}
    for i in range(max(1, polls)):
        last = fetch_pr(repo, number)
        if str(last.get("mergeable", "")).upper() != "UNKNOWN":
            return last
        if i + 1 < polls:
            time.sleep(interval)
    return last  # still UNKNOWN -> evaluate_snapshot raises CouldNotCheck


def describe_job(check: dict) -> str:
    """Step-level detail for a non-passing check run, from the jobs API.

    `gh run view --log-failed` is not used: it prints nothing for a cancelled
    run (no step failed) and printed 0 bytes on three genuinely failing runs.
    The jobs API carries each step's conclusion and the job's wall time, which
    is what separates a timeout presenting as `cancelled` from a real failure.
    """
    url = str(check.get("detailsUrl") or "")
    m = JOB_URL_RE.search(url)
    if not m:
        return "no jobs-API locator in detailsUrl (external check); nothing further readable"
    owner, repo, run_id, job_id = m.groups()
    try:
        job = _gh_json(["api", f"repos/{owner}/{repo}/actions/jobs/{job_id}"])
    except CouldNotCheck as exc:
        return f"jobs API unreadable ({exc})"
    if not isinstance(job, dict):
        return "jobs API returned no job object"
    steps = job.get("steps") or []
    minutes = ""
    if job.get("started_at") and job.get("completed_at"):
        from datetime import datetime
        s = datetime.fromisoformat(str(job["started_at"]).replace("Z", "+00:00"))
        e = datetime.fromisoformat(str(job["completed_at"]).replace("Z", "+00:00"))
        minutes = f"{(e - s).total_seconds() / 60:.1f} min wall"
    failed = [st.get("name") for st in steps if st.get("conclusion") == "failure"]
    cancelled = [st.get("name") for st in steps if st.get("conclusion") == "cancelled"]
    parts = [f"job '{job.get('name')}' conclusion={job.get('conclusion')} {minutes}".strip()]
    if failed:
        parts.append("failed step(s): " + ", ".join(map(str, failed)))
    if cancelled:
        parts.append("cancelled step(s): " + ", ".join(map(str, cancelled))
                     + " (no failed step: a cap or a manual cancel, not the code)")
    parts.append(f"run https://github.com/{owner}/{repo}/actions/runs/{run_id}")
    return "; ".join(parts)


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------

def decide(fields: list[FieldResult]) -> int:
    if any(f.status == FAIL for f in fields):
        return EXIT_FAIL
    if any(f.status == CNC for f in fields):
        return EXIT_COULD_NOT_CHECK
    return EXIT_PASS


def render(fields: list[FieldResult], header: str) -> tuple[int, str]:
    mark = {PASS: "PASS", FAIL: "FAIL", CNC: "????"}
    lines = [header]
    for f in fields:
        lines.append(f"  [{mark[f.status]}] field {f.number}: {f.name} -- {f.detail}")
        for n in f.notes:
            lines.append(f"         {n}")
    code = decide(fields)
    if code == EXIT_FAIL:
        failed = [f.number for f in fields if f.status == FAIL]
        lines.append(f"REFUSE: field(s) {failed} fail. Do not merge.")
    elif code == EXIT_COULD_NOT_CHECK:
        cnc = [f.number for f in fields if f.status == CNC]
        lines.append(f"COULD NOT CHECK: field(s) {cnc} could not be assessed. Not a pass, not a fail.")
    else:
        lines.append("PASS: all five fields hold.")
    return code, "\n".join(lines)


def to_json(fields: list[FieldResult], code: int) -> str:
    return json.dumps({"exit": code, "fields": [f.__dict__ for f in fields]}, indent=2)


# --------------------------------------------------------------------------
# self-test: the gate must be able to fail on every field before it is trusted
# --------------------------------------------------------------------------

def self_test() -> int:
    import tempfile

    def run_(name, status, concl):
        return {"__typename": "CheckRun", "name": name, "status": status, "conclusion": concl}

    def snap(**over):
        base = {"state": "OPEN", "mergeable": "MERGEABLE", "isDraft": False,
                "statusCheckRollup": [run_("ci", "COMPLETED", "SUCCESS")]}
        base.update(over)
        return base

    def code_of(pr, **kw):
        try:
            return decide(evaluate_snapshot(pr, **kw))
        except CouldNotCheck:
            return EXIT_COULD_NOT_CHECK

    table = [
        ("clean snapshot", code_of(snap()), EXIT_PASS),
        ("field 1 state=MERGED", code_of(snap(state="MERGED")), EXIT_FAIL),
        ("field 2 mergeable=CONFLICTING", code_of(snap(mergeable="CONFLICTING")), EXIT_FAIL),
        ("field 2 mergeable=UNKNOWN", code_of(snap(mergeable="UNKNOWN")), EXIT_COULD_NOT_CHECK),
        ("field 3 isDraft=true", code_of(snap(isDraft=True)), EXIT_FAIL),
        ("field 4 conclusion=FAILURE", code_of(snap(statusCheckRollup=[run_("ci", "COMPLETED", "FAILURE")])), EXIT_FAIL),
        ("field 4 conclusion=TIMED_OUT", code_of(snap(statusCheckRollup=[run_("ci", "COMPLETED", "TIMED_OUT")])), EXIT_FAIL),
        ("field 4 conclusion=CANCELLED", code_of(snap(statusCheckRollup=[run_("ci", "COMPLETED", "CANCELLED")])), EXIT_COULD_NOT_CHECK),
        ("field 4 status=IN_PROGRESS", code_of(snap(statusCheckRollup=[run_("ci", "IN_PROGRESS", None)])), EXIT_COULD_NOT_CHECK),
        ("field 4 FAILURE beside CANCELLED", code_of(snap(statusCheckRollup=[run_("a", "COMPLETED", "CANCELLED"), run_("b", "COMPLETED", "FAILURE")])), EXIT_FAIL),
        ("field 4 zero checks", code_of(snap(statusCheckRollup=[])), EXIT_COULD_NOT_CHECK),
        ("field 4 missing key", code_of({"state": "OPEN"}), EXIT_COULD_NOT_CHECK),
        ("field 3 draft + field 4 cancelled -> 1 (a definite failure dominates)",
         code_of(snap(isDraft=True, statusCheckRollup=[run_("ci", "COMPLETED", "CANCELLED")])), EXIT_FAIL),
    ]
    neutral = evaluate_snapshot(snap(statusCheckRollup=[run_("review-bot", "COMPLETED", "NEUTRAL")]))
    table.append(("field 4 NEUTRAL surfaced as NOT ASSESSED",
                  EXIT_PASS if (neutral[3].ok and any("NOT ASSESSED" in n for n in neutral[3].notes)) else EXIT_FAIL,
                  EXIT_PASS))
    cancelled = evaluate_snapshot(snap(statusCheckRollup=[run_("ci", "COMPLETED", "CANCELLED")]))
    table.append(("field 4 CANCELLED carries the re-run advice",
                  EXIT_PASS if any(RERUN_ADVICE in n for n in cancelled[3].notes) else EXIT_FAIL, EXIT_PASS))

    # field 5 on a synthetic repository with a planted binding
    with tempfile.TemporaryDirectory() as td:
        repo = Path(td)

        def run(*a):
            subprocess.run([GIT, "-C", str(repo), *a], check=True, capture_output=True)
        run("init", "-q", "-b", "main")
        run("config", "user.email", "gate@test")
        run("config", "user.name", "gate")
        (repo / "lane").mkdir()
        (repo / "lane" / "arms.py").write_text("ARMS = 1\n")
        (repo / "lane" / "free.py").write_text("FREE = 1\n")
        (repo / "lane" / "run.py").write_text("RUN = 1\n")
        digest = hashlib.sha256(b"ARMS = 1\n").hexdigest()
        (repo / "lane" / "LANE_FREEZE_V1.json").write_text(json.dumps({"v1_arms_py_sha256": digest}))
        (repo / "lane" / "RUN_RECEIPT.json").write_text(json.dumps(
            {"source_files_sha256": {"lane/run.py": hashlib.sha256(b"RUN = 1\n").hexdigest()}}))
        run("add", "."); run("commit", "-q", "-m", "freeze")
        base = subprocess.run([GIT, "-C", str(repo), "rev-parse", "HEAD"], capture_output=True).stdout.decode().strip()

        def code5(bindings):
            return decide([field5_result(bindings)])
        # PR A: edits the freeze-bound file only
        run("checkout", "-q", "-b", "pr-a")
        (repo / "lane" / "arms.py").write_text("ARMS = 2\n")
        run("commit", "-qam", "edit arms")
        table.append(("field 5 planted freeze binding refused",
                      code5(scan_freeze_bindings(repo, base, "pr-a", ["lane/arms.py"])), EXIT_FAIL))
        # PR B: edits an unbound file (no-alarm control)
        run("checkout", "-q", "main"); run("checkout", "-q", "-b", "pr-b")
        (repo / "lane" / "free.py").write_text("FREE = 2\n")
        run("commit", "-qam", "edit free")
        b = scan_freeze_bindings(repo, base, "pr-b", ["lane/free.py"])
        table.append(("field 5 clean PR no alarm", EXIT_FAIL if b else EXIT_PASS, EXIT_PASS))
        # PR C: edits the bound file and rebinds the freeze coherently
        run("checkout", "-q", "main"); run("checkout", "-q", "-b", "pr-c")
        (repo / "lane" / "arms.py").write_text("ARMS = 3\n")
        (repo / "lane" / "LANE_FREEZE_V1.json").write_text(json.dumps(
            {"v1_arms_py_sha256": hashlib.sha256(b"ARMS = 3\n").hexdigest()}))
        run("commit", "-qam", "edit and rebind")
        table.append(("field 5 coherent rebind passes",
                      code5(scan_freeze_bindings(repo, base, "pr-c", ["lane/arms.py", "lane/LANE_FREEZE_V1.json"])), EXIT_PASS))
        # PR R: edits a file only a provenance receipt names: surfaced, not refused; --strict refuses
        run("checkout", "-q", "main"); run("checkout", "-q", "-b", "pr-r")
        (repo / "lane" / "run.py").write_text("RUN = 2\n")
        run("commit", "-qam", "edit run")
        r = scan_freeze_bindings(repo, base, "pr-r", ["lane/run.py"])
        table.append(("field 5 provenance record surfaced not refused",
                      EXIT_PASS if (r and all(x.status == "PROVENANCE" for x in r) and code5(r) == EXIT_PASS) else EXIT_FAIL, EXIT_PASS))
        table.append(("field 5 --strict refuses the provenance record",
                      code5(scan_freeze_bindings(repo, base, "pr-r", ["lane/run.py"], strict=True)), EXIT_FAIL))
        # could-not-check: unreadable ref
        try:
            scan_freeze_bindings(repo, "no-such-ref", None, ["lane/arms.py"])
            cnc = EXIT_PASS
        except CouldNotCheck:
            cnc = EXIT_COULD_NOT_CHECK
        table.append(("field 5 unreadable base ref", cnc, EXIT_COULD_NOT_CHECK))

    bad = 0
    print("pr_merge_gate self-test (python %s)" % sys.version.split()[0])
    for name, got, want in table:
        mark = "ok " if got == want else "BAD"
        bad += got != want
        print(f"  {mark} {name}: exit {got} (expected {want})")
    if bad:
        print(f"SELF-TEST FAILED: {bad} case(s)")
        return EXIT_COULD_NOT_CHECK
    print("self-test passed: the gate can fail on every field and distinguishes could-not-check")
    return EXIT_PASS


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pr", type=int, help="pull request number")
    ap.add_argument("--repo", help="OWNER/REPO (default: gh's current repo)")
    ap.add_argument("--git-dir", default=".", help="local clone used for the freeze scan")
    ap.add_argument("--base-ref", default="origin/main", help="ref the freeze scan measures against")
    ap.add_argument("--head-ref", help="PR head ref/sha (default: fetched from the PR)")
    ap.add_argument("--no-fetch", action="store_true", help="do not `git fetch` before scanning")
    ap.add_argument("--polls", type=int, default=6, help="polls while mergeable is UNKNOWN")
    ap.add_argument("--poll-interval", type=float, default=10.0)
    ap.add_argument("--allow-no-checks", action="store_true")
    ap.add_argument("--allow-no-binders", action="store_true")
    ap.add_argument("--strict", action="store_true", help="refuse on provenance-class bindings too")
    ap.add_argument("--no-jobs-api", action="store_true", help="skip step-level detail for non-passing checks")
    ap.add_argument("--replay", action="store_true", help="field 5 only, from --base-ref/--head-ref history")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    git_dir = Path(args.git_dir).resolve()
    print(f"pr_merge_gate: python {sys.version.split()[0]}; git dir {git_dir}; base ref {args.base_ref}")

    try:
        if args.replay:
            if not args.head_ref:
                raise CouldNotCheck("--replay needs --head-ref")
            changed = git_changed_paths(git_dir, args.base_ref, args.head_ref)
            if not changed:
                raise CouldNotCheck(f"no changed paths between {args.base_ref} and {args.head_ref}")
            bindings = scan_freeze_bindings(git_dir, args.base_ref, args.head_ref, changed,
                                            args.allow_no_binders, args.strict)
            fields = [field5_result(bindings, measured_at=args.base_ref)]
            code, text = render(fields, f"replay: {len(changed)} changed path(s) {args.base_ref}..{args.head_ref}")
            print(to_json(fields, code) if args.json else text)
            return code

        if args.pr is None:
            raise CouldNotCheck("--pr is required (or --replay / --self-test)")
        pr = fetch_pr_polling(args.repo, args.pr, args.polls, args.poll_interval)
        fields = evaluate_snapshot(pr, allow_no_checks=args.allow_no_checks,
                                   job_detail=None if args.no_jobs_api else describe_job)

        if not args.no_fetch:
            remote = args.base_ref.split("/", 1)[0] if "/" in args.base_ref else "origin"
            branch = args.base_ref.split("/", 1)[1] if "/" in args.base_ref else args.base_ref
            _git(git_dir, "fetch", "-q", remote, branch)
            head = args.head_ref or pr.get("headRefOid")
            if head:
                _git(git_dir, "fetch", "-q", remote, head, check=False)
        head = args.head_ref or pr.get("headRefOid")
        changed = [f["path"] for f in (pr.get("files") or [])]
        if not changed:
            raise CouldNotCheck("PR reports no changed files; nothing to scan is not the same as nothing bound")
        if head and _git(git_dir, "cat-file", "-e", f"{head}^{{commit}}", check=False).returncode != 0:
            head = None  # head not fetchable: rebind coherence cannot be judged; bindings stay LIVE
        base_sha = _git(git_dir, "rev-parse", "--short", args.base_ref).stdout.decode().strip()
        bindings = scan_freeze_bindings(git_dir, args.base_ref, head, changed, args.allow_no_binders, args.strict)
        fields.append(field5_result(bindings, measured_at=f"{args.base_ref}@{base_sha}"))
        code, text = render(fields, f"PR #{pr.get('number')} {pr.get('url', '')} "
                                    f"head {str(pr.get('headRefOid', ''))[:8]} vs {args.base_ref}@{base_sha}")
        print(to_json(fields, code) if args.json else text)
        return code
    except CouldNotCheck as exc:
        print(f"COULD NOT CHECK: {exc}", file=sys.stderr)
        return EXIT_COULD_NOT_CHECK


if __name__ == "__main__":
    sys.exit(main())

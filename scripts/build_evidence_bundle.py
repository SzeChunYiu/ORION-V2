#!/usr/bin/env python3
"""Build a PIN_PROPOSED evidence bundle for a paper from named ORION-V2 merge commits.

A bundle names, for each decisive study, the merge commit the paper cites and
every evidence file that commit landed, with the file's git blob id, sha256 and
byte count AT THAT COMMIT. It is the V2-side half of the registration that
ORION-paper's registry (`orion_v2_evidence_head` + per-path sha256, see
ORION-paper `scripts/check_pd_evidence_pin.py`) expects, produced before the
registry catches up and labelled PIN_PROPOSED until a paper lane registers it.

Frame, learned the hard way on P-D: digests are measured AT THE PIN, never at
main. Drift between the pin and main is reported as a non-blocking ADVISORY
(`status_on_main` + the commits that touched the path), because a pin check
cannot see an unpaired correction by construction; a human must confirm the
manuscript still reflects the evidence. The advisory MUST be empty when
pin == main, or it is an alarm nobody believes.

Every digest is computed in-process from `git cat-file blob <oid>` bytes. None
goes through a shell pipe: on the machine this was built on, a pipe returned a
wrong sha256 for a blob that matched when hashed from the object directly.

Exit codes, deliberately three:

    0  bundle built; every named commit exists and is on --main-ref; every
       evidence file is present at its pin; every expected terminal string was
       found in its receipt at the pin
    1  a definite defect in the spec or the evidence: a file missing at its
       pin, a commit not an ancestor of --main-ref, or an expected terminal
       string absent from the receipt it is claimed for
    2  could not check: git unreadable, a commit unresolvable, or a
       must-match control inside the self-test did not match

Registered mode (`--registry FILE --registry-commit SHA`): once a paper lane has
registered per-paper pins in ORION-paper's PAPER_REGISTRY.json
(`orion_v2_evidence_pins`, schema orion-paper.per-paper-evidence-pins.v1), the
same build re-verifies EVERY registered triple (path, commit, sha256, bytes)
against this repository's object database -- blob read with `git cat-file`,
hashed in-process -- and cross-checks it against the bundle's own pinned
files. The label becomes REGISTERED only when every triple is IDENTICAL, every
artifact commit is an ancestor of both the registered pin and --main-ref, and
four planted controls fail as they must (a zeroed digest, a wrong byte count,
an unresolvable commit, a commit that is not an ancestor of the pin). A
control that does not fail is exit 2, never a pass: a verifier that cannot
see a planted mismatch has verified nothing.

Usage:
    build_evidence_bundle.py --paper FLAGSHIP|PRA --git-dir DIR --out DIR [--main-ref origin/main]
    build_evidence_bundle.py --paper FLAGSHIP --git-dir DIR --out DIR --registry REGISTRY.json --registry-commit SHA
    build_evidence_bundle.py --self-test --git-dir DIR
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

GIT = "/usr/bin/git" if Path("/usr/bin/git").exists() else "git"
EXIT_OK, EXIT_FAIL, EXIT_CNC = 0, 1, 2
SCHEMA = "orion.v2.guards.evidence-bundle.v1"
LABEL = "PIN_PROPOSED"
REGISTERED_LABEL = "REGISTERED"
REGISTRY_PINS_SCHEMA = "orion-paper.per-paper-evidence-pins.v1"
# ORION-paper registry `papers[].paper_id` for each bundle paper
REGISTRY_PAPER_IDS = {"FLAGSHIP": ("FLAGSHIP",), "PRA": ("#51",)}

# Bulk campaign material is not evidence a manuscript cites by path; it is bound
# by the custody manifests that ARE included.
BULK_EXCLUDE = re.compile(r"(^|/)(responses|requests|public|private)(/|$)")

AUTHORITY = {
    "grants_registration": False,
    "grants_scientific_truth": False,
    "grants_publication_authority": False,
    "note": (
        "A proposal by the guards lane of WHICH ORION-V2 commits and files a paper's "
        "cited evidence resolves to, with their identities at the pin. Registration is "
        "the paper lane's act in ORION-paper's PAPER_REGISTRY.json; until then the label "
        "stays PIN_PROPOSED. Nothing here asserts that a claim is true, only where its "
        "receipt lives and what bytes it had."
    ),
}

# --- Paper specs --------------------------------------------------------------
# `terminal_expected` is asserted to appear in `receipt` at the pin, so a typo in
# this spec fails the build rather than silently pinning the wrong study.
# `claim_strings` are the numbers ORION-paper's evidence_boundary quotes; each is
# searched (whitespace/thin-space/comma-normalised) across the study's pinned
# files and the hit list is recorded. A quoted number with no receipt hit is a
# finding for the paper lane, not for this script.

SPECS = {
    "FLAGSHIP": {
        "paper_folder": "v2-papers/FLAGSHIP-machine-epistemics",
        "registry_field_that_cites_these": "papers[FLAGSHIP].evidence_boundary",
        "studies": [
            {"id": "ME-X4", "commit": "4929a44", "roots": ["research/experiments/me-x4/"],
             "receipt": "research/experiments/me-x4/ME_X4_OUTCOME_RECEIPT.md",
             "terminal_expected": "ME_X4_STATUS = PARENT_SUFFICIENT",
             "claim_strings": ["1200/1200", "12 strata"]},
            {"id": "ME-X1", "commit": "59b1f5b", "roots": ["research/experiments/me-x1/"],
             "receipt": "research/experiments/me-x1/ME_X1_OUTCOME_RECEIPT.md",
             "terminal_expected": "RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL",
             "claim_strings": ["1000/1000", "3.7e-9"]},
            {"id": "ME-X2", "commit": "776d3a1", "roots": ["research/experiments/me-x2/"],
             "receipt": "research/experiments/me-x2/ME_X2_OUTCOME_RECEIPT.md",
             "terminal_expected": "B5_DOMINATES",
             "claim_strings": ["0.983", "0.963", "0.0032", "43"]},
            {"id": "ME-X5", "commit": "024d97f", "roots": ["research/experiments/me-x5/"],
             "receipt": "research/experiments/me-x5/ME_X5_OUTCOME_RECEIPT.md",
             "terminal_expected": "RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL",
             "claim_strings": ["1440"],
             "superseded_note": "ME_X5_OUTCOME_RECEIPT.md is corrected by erratum e30526e (pinned below); "
                                "the results files are unchanged by the erratum."},
            {"id": "ME-X5-ERRATUM", "commit": "e30526e", "roots": ["research/experiments/me-x5/"],
             "receipt": "research/experiments/me-x5/ME_X5_OUTCOME_RECEIPT.md",
             "terminal_expected": "ERRATUM",
             "claim_strings": ["1440"],
             "role": "erratum: four corrections to claims about the code and ladder wording; "
                     "no number, gate verdict or terminal changed (per the erratum's own header)"},
            {"id": "ME-X6-V2", "commit": "a60f1ea", "roots": ["research/experiments/me-x6-v2/"],
             "receipt": "research/experiments/me-x6-v2/ME_X6_V2_OUTCOME_RECEIPT.md",
             "terminal_expected": "TYPING_NOT_SEPARATED_AT_MATCHED_CAPACITY",
             "claim_strings": ["1400/1400"],
             "role": "non-gating panel (FLAGSHIP_GATE = false). Cited by merge commit in the registry's "
                     "evidence_boundary; NOT in the coordinator's pin list — included so no cited "
                     "commit is left unpinned; the paper lane may drop it."},
            {"id": "ME-X6-V3", "commit": "d9e588f", "roots": ["research/experiments/me-x6-v3/"],
             "receipt": "research/experiments/me-x6-v3/ME_X6_V3_OUTCOME_RECEIPT.md",
             "terminal_expected": "TYPING_IS_A_COVERAGE_PRIOR",
             "claim_strings": ["1800/1800", "1400/1800", "0/400", "36 cells"],
             "role": "non-gating panel (FLAGSHIP_GATE = false); d9e588f is also the registry's current "
                     "global orion_v2_evidence_head"},
        ],
        # Numbers the evidence_boundary quotes without naming a study; searched across all pinned files.
        "unattributed_claim_strings": ["492", "163", "0.837"],
    },
    "PRA": {
        "paper_folder": "v2-papers/llm-machine-epistemics",
        "registry_field_that_cites_these": "papers[#51].v16_revision_receipts (H-EXT-4 note)",
        "studies": [
            {"id": "H-EXT-4", "commit": "52d2578b",
             "roots": ["research/llm-machine-epistemics/", "tests/unit/test_h_ext4_premium_bounds.py"],
             "receipt": "research/llm-machine-epistemics/H_EXT4_QUANTITATIVE_REVISION_PREMIUM_V1.md",
             "terminal_expected": "H-EXT-4",
             "claim_strings": ["812,771", "1,745,628"],
             "role": "quantitative prospective-revision premium: proofs + mechanized checks. 52d2578b (#175, "
                     "honest denominator for the label-identity check) is the commit ORION-paper's registry names "
                     "as the finding source and pins the three H-EXT-4 paths at; it corrects the first landing "
                     "51142ea3 (#147) and #166. The registry pins fifteen further mechanical_execution/ paths at "
                     "the same commit; they are verified in registered mode as registry-only entries.",
             "superseded_note": "the PIN_PROPOSED bundle of 2026-09-04 pinned 51142ea3 (#147); the three H-EXT-4 "
                                "paths changed at #166 and #175 and the registry binds the corrected bytes"},
        ],
        "unattributed_claim_strings": [],
    },
}


class CouldNotCheck(Exception):
    pass


def git(git_dir: str, *args: str) -> bytes:
    p = subprocess.run([GIT, "-C", git_dir, *args], capture_output=True)
    if p.returncode != 0:
        raise CouldNotCheck(f"git {' '.join(args)}: {p.stderr.decode(errors='replace').strip()[:200]}")
    return p.stdout


def resolve(git_dir: str, ref: str) -> str:
    return git(git_dir, "rev-parse", "--verify", f"{ref}^{{commit}}").decode().strip()


def is_ancestor(git_dir: str, a: str, b: str) -> bool:
    p = subprocess.run([GIT, "-C", git_dir, "merge-base", "--is-ancestor", a, b], capture_output=True)
    if p.returncode not in (0, 1):
        raise CouldNotCheck(f"merge-base --is-ancestor {a} {b}: {p.stderr.decode(errors='replace')[:200]}")
    return p.returncode == 0


def ls_tree(git_dir: str, commit: str, path: str) -> tuple[str | None, str | None, int | None]:
    """(kind, oid, bytes) for a path at a commit; (None, None, None) when absent."""
    out = git(git_dir, "ls-tree", "-l", commit, "--", path).decode()
    if not out.strip():
        return None, None, None
    mode, kind, oid, size, _ = out.split(maxsplit=4)
    return kind, oid, (int(size) if size != "-" else None)


def blob_bytes(git_dir: str, oid: str) -> bytes:
    return git(git_dir, "cat-file", "blob", oid)


def changed_paths(git_dir: str, commit: str) -> list[tuple[str, str]]:
    out = git(git_dir, "show", "--format=", "--name-status", commit).decode()
    rows = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        rows.append((parts[0][0], parts[-1]))
    return rows


def commits_touching(git_dir: str, pin: str, main: str, path: str) -> list[dict]:
    """Post-pin commits that touched a path, with subjects: the advisory must NAME the change."""
    out = git(git_dir, "log", "--format=%h%x09%s", f"{pin}..{main}", "--", path).decode()
    rows = []
    for line in out.splitlines():
        sha, _, subj = line.partition("\t")
        if sha:
            rows.append({"sha": sha, "subject": subj[:120]})
    return rows


_SUPERSCRIPT = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")


def norm(s: str) -> str:
    """Whitespace/thin-space/comma-insensitive; scientific notation 3.7×10⁻⁹ == 3.7e-9."""
    s = s.translate(_SUPERSCRIPT).replace("×10^", "e").replace("×10", "e").replace("x10^", "e")
    return re.sub(r"[\s\u2009\u00a0\u202f,]", "", s)


def build_study(git_dir: str, main: str, spec: dict) -> tuple[dict, list[str]]:
    defects: list[str] = []
    pin = resolve(git_dir, spec["commit"])
    subject = git(git_dir, "log", "-1", "--format=%ad%x09%s", "--date=short", pin).decode().strip()
    date, _, subj = subject.partition("\t")
    on_main = is_ancestor(git_dir, pin, main)
    if not on_main:
        defects.append(f"{spec['id']}: {pin[:8]} is not an ancestor of the main ref")

    files = []
    normalized_blobs: dict[str, str] = {}
    for status, path in changed_paths(git_dir, pin):
        if status == "D" or BULK_EXCLUDE.search(path):
            continue
        if not any(path.startswith(r) or path == r.rstrip("/") for r in spec["roots"]):
            continue
        kind, oid, size = ls_tree(git_dir, pin, path)
        if kind != "blob":
            defects.append(f"{spec['id']}: {path} missing at pin {pin[:8]}")
            files.append({"path": path, "change": status, "status_at_pin": "MISSING_AT_PIN"})
            continue
        data = blob_bytes(git_dir, oid)
        sha = hashlib.sha256(data).hexdigest()
        normalized_blobs[path] = norm(data.decode(errors="replace"))
        mkind, moid, _ = ls_tree(git_dir, main, path)
        if moid is None:
            st, touched = "REMOVED_ON_MAIN", commits_touching(git_dir, pin, main, path)
        elif moid == oid:
            st, touched = "UNCHANGED_ON_MAIN", []
        else:
            st, touched = "CHANGED_SINCE_PIN", commits_touching(git_dir, pin, main, path)
        row = {"path": path, "change": status, "git_blob_sha1": oid, "sha256": sha, "bytes": len(data),
               "status_on_main": st}
        if touched:
            row["touched_by_after_pin"] = touched
        files.append(row)

    receipt_ok = None
    if spec.get("receipt"):
        kind, oid, _ = ls_tree(git_dir, pin, spec["receipt"])
        if kind != "blob":
            defects.append(f"{spec['id']}: receipt {spec['receipt']} missing at pin")
            receipt_ok = False
        else:
            text = blob_bytes(git_dir, oid).decode(errors="replace")
            receipt_ok = spec["terminal_expected"] in text
            if not receipt_ok:
                defects.append(f"{spec['id']}: terminal string {spec['terminal_expected']!r} not in receipt at pin")

    claim_hits = {}
    for c in spec.get("claim_strings", []):
        hits = [p for p, t in normalized_blobs.items() if norm(c) in t]
        claim_hits[c] = hits

    study = {
        "id": spec["id"], "orion_v2_commit": pin, "short": pin[:8], "date": date, "subject": subj,
        "on_main": on_main, "evidence_roots": spec["roots"], "receipt": spec.get("receipt"),
        "terminal_expected": spec.get("terminal_expected"), "terminal_found_in_receipt_at_pin": receipt_ok,
        "claim_strings_found_in": claim_hits, "files": files,
        "counts": {"files": len(files),
                   "unchanged_on_main": sum(f.get("status_on_main") == "UNCHANGED_ON_MAIN" for f in files),
                   "changed_since_pin": sum(f.get("status_on_main") == "CHANGED_SINCE_PIN" for f in files),
                   "removed_on_main": sum(f.get("status_on_main") == "REMOVED_ON_MAIN" for f in files),
                   "missing_at_pin": sum(f.get("status_at_pin") == "MISSING_AT_PIN" for f in files)},
    }
    for k in ("role", "superseded_note"):
        if k in spec:
            study[k] = spec[k]
    return study, defects


def build(paper: str, git_dir: str, main_ref: str) -> tuple[dict, int]:
    spec = SPECS[paper]
    main = resolve(git_dir, main_ref)
    studies, defects = [], []
    for s in spec["studies"]:
        st, d = build_study(git_dir, main, s)
        studies.append(st)
        defects += d
    # unattributed claim strings: search every pinned file of every study
    unattributed = {}
    for c in spec.get("unattributed_claim_strings", []):
        hits = []
        for st in studies:
            for f in st["files"]:
                if "git_blob_sha1" not in f:
                    continue
                if norm(c) in norm(blob_bytes(git_dir, f["git_blob_sha1"]).decode(errors="replace")):
                    hits.append(f"{st['id']}:{f['path']}")
        unattributed[c] = hits
    advisory = [
        {"study": st["id"], "path": f["path"], "status_on_main": f["status_on_main"],
         "touched_by_after_pin": f.get("touched_by_after_pin", [])}
        for st in studies for f in st["files"]
        if f.get("status_on_main") in ("CHANGED_SINCE_PIN", "REMOVED_ON_MAIN")
    ]
    bundle = {
        "schema_version": SCHEMA, "paper_id": paper, "label": LABEL, "proposed_by": "lane-guards (ORION-V2)",
        "built_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "measured_against_main": {"ref": main_ref, "commit": main},
        "paper_folder_in_orion_paper": spec["paper_folder"],
        "registry_field_that_cites_these": spec["registry_field_that_cites_these"],
        "registration": {"registered": False, "registry": "ORION-paper v2-papers/PAPER_REGISTRY.json",
                         "awaiting": "lane-paper-3 registers per-paper pins; then re-run the verifier and drop the label"},
        "authority": AUTHORITY,
        "frame": "digests measured AT EACH STUDY'S PIN; status_on_main is an advisory, never a failure",
        "studies": studies,
        "unattributed_claim_strings_found_in": unattributed,
        "advisory_changed_or_removed_since_pin": advisory,
        "defects": defects,
        "totals": {"studies": len(studies), "files": sum(s["counts"]["files"] for s in studies),
                   "unchanged_on_main": sum(s["counts"]["unchanged_on_main"] for s in studies),
                   "changed_since_pin": sum(s["counts"]["changed_since_pin"] for s in studies),
                   "removed_on_main": sum(s["counts"]["removed_on_main"] for s in studies),
                   "missing_at_pin": sum(s["counts"]["missing_at_pin"] for s in studies)},
    }
    return bundle, (EXIT_FAIL if defects else EXIT_OK)


def registry_pins(registry_path: Path, paper: str) -> tuple[dict, str]:
    """(orion_v2_evidence_pins block, sha256 of the registry file) for a paper; CouldNotCheck if absent."""
    data = registry_path.read_bytes()
    reg = json.loads(data.decode("utf-8"))
    for p in reg.get("papers", []):
        if str(p.get("paper_id") or p.get("id")) in REGISTRY_PAPER_IDS[paper]:
            pins = p.get("orion_v2_evidence_pins")
            if not pins:
                raise CouldNotCheck(f"registry paper {p.get('paper_id')} has no orion_v2_evidence_pins")
            if pins.get("schema") != REGISTRY_PINS_SCHEMA:
                raise CouldNotCheck(f"registry pins schema {pins.get('schema')!r} != {REGISTRY_PINS_SCHEMA!r}")
            if not pins.get("artifacts"):
                raise CouldNotCheck("registry pins carry zero artifacts (vacuous)")
            return pins, hashlib.sha256(data).hexdigest()
    raise CouldNotCheck(f"paper {paper} ({REGISTRY_PAPER_IDS[paper]}) not in registry {registry_path}")


def verify_registry_artifact(git_dir: str, pin: str, main: str, art: dict) -> tuple[dict, list[str]]:
    """Re-measure one registered (path, commit, sha256, bytes) triple against the object DB.

    Raises CouldNotCheck for an unresolvable commit (could not check is never a pass)."""
    defects: list[str] = []
    commit = resolve(git_dir, art["commit"])
    path = art["path"]
    row = {"path": path, "commit": commit, "registered_sha256": art["sha256"], "registered_bytes": art.get("bytes"),
           "role": art.get("role"), "gating": art.get("gating")}
    row["commit_is_ancestor_of_pin"] = is_ancestor(git_dir, commit, pin)
    row["commit_is_ancestor_of_main"] = is_ancestor(git_dir, commit, main)
    if not row["commit_is_ancestor_of_pin"]:
        defects.append(f"{path}: commit {commit[:8]} is not an ancestor of the registered pin {pin[:8]}")
    if not row["commit_is_ancestor_of_main"]:
        defects.append(f"{path}: commit {commit[:8]} is not an ancestor of the main ref")
    kind, oid, _ = ls_tree(git_dir, commit, path)
    if kind != "blob":
        row["verdict"] = "MISSING_AT_COMMIT"
        defects.append(f"{path}: missing at registered commit {commit[:8]}")
        return row, defects
    data = blob_bytes(git_dir, oid)
    sha = hashlib.sha256(data).hexdigest()
    row.update({"git_blob_sha1": oid, "measured_sha256": sha, "measured_bytes": len(data)})
    if sha != art["sha256"]:
        row["verdict"] = "DIGEST_MISMATCH"
        defects.append(f"{path}@{commit[:8]}: registered sha256 {art['sha256'][:12]}… != measured {sha[:12]}…")
    elif art.get("bytes") is not None and len(data) != art["bytes"]:
        row["verdict"] = "BYTES_MISMATCH"
        defects.append(f"{path}@{commit[:8]}: registered bytes {art['bytes']} != measured {len(data)}")
    else:
        row["verdict"] = "IDENTICAL"
    return row, defects


def registry_controls(git_dir: str, pin: str, main: str, art: dict) -> tuple[list[dict], bool]:
    """Four planted faults against a REAL registered artifact; each MUST be caught."""
    out = []

    def rec(name: str, caught: bool, detail: str):
        out.append({"control": name, "must": "FAIL", "caught": caught, "detail": detail})

    row, d = verify_registry_artifact(git_dir, pin, main, dict(art, sha256="0" * 64))
    rec("planted_zeroed_sha256", row["verdict"] == "DIGEST_MISMATCH" and bool(d), row["verdict"])
    row, d = verify_registry_artifact(git_dir, pin, main, dict(art, bytes=int(art["bytes"]) + 1))
    rec("planted_wrong_byte_count", row["verdict"] == "BYTES_MISMATCH" and bool(d), row["verdict"])
    try:
        verify_registry_artifact(git_dir, pin, main, dict(art, commit="0000000deadbeef"))
        rec("planted_unresolvable_commit", False, "did not raise")
    except CouldNotCheck as e:
        rec("planted_unresolvable_commit", True, f"CouldNotCheck: {str(e)[:80]}")
    # a commit that is NOT an ancestor of the pin: the pin's own first parent's sibling is not
    # guaranteed to exist, so use the main ref when it is strictly after the pin, else a fresh
    # orphan-like check is impossible and the control is recorded as could-not-plant (exit 2).
    if main != pin and not is_ancestor(git_dir, main, pin):
        row, d = verify_registry_artifact(git_dir, pin, main, dict(art, commit=main))
        rec("planted_commit_after_pin", row["commit_is_ancestor_of_pin"] is False and any("not an ancestor of the registered pin" in x for x in d),
            f"main {main[:8]} vs pin {pin[:8]}")
    else:
        rec("planted_commit_after_pin", False, "could not plant: main ref is not strictly after the pin")
    return out, all(c["caught"] for c in out)


def cross_check_bundle(git_dir: str, bundle: dict, rows: list[dict]) -> dict:
    """Does the bundle's own measurement agree with every registered triple it also covers?

    A registered path the bundle pins at an EARLIER commit with different bytes is a later
    correction the registry binds at its own commit (P-D's lesson: pin the corrected bytes too).
    It is an advisory, not a defect, when (a) the registry commit descends from the bundle's
    commit and (b) the bundle already reports that path CHANGED_SINCE_PIN with the registry
    commit among the commits that touched it. Anything else that hashes differently is a defect."""
    by_path_commit: dict[tuple[str, str], dict] = {}
    by_path: dict[str, list[tuple[str, dict]]] = {}
    for st in bundle["studies"]:
        for f in st["files"]:
            if "sha256" in f:
                by_path_commit[(f["path"], st["orion_v2_commit"])] = f
                by_path.setdefault(f["path"], []).append((st["orion_v2_commit"], f))
    agree, registry_only, later_correction, different = [], [], [], []
    for r in rows:
        key = (r["path"], r["commit"])
        if key in by_path_commit:
            b = by_path_commit[key]
            entry = {"path": r["path"], "commit": r["commit"][:8], "bundle_sha256": b["sha256"], "registry_sha256": r["registered_sha256"]}
            (agree if b["sha256"] == r.get("measured_sha256") == r["registered_sha256"] else different).append(entry)
        elif r["path"] in by_path:
            for c, b in by_path[r["path"]]:
                entry = {"path": r["path"], "registry_commit": r["commit"][:8], "bundle_commit": c[:8],
                         "bundle_sha256": b["sha256"], "registry_sha256": r["registered_sha256"]}
                if b["sha256"] == r["registered_sha256"]:
                    entry["note"] = "same bytes at both commits"
                    agree.append(entry)
                    continue
                descends = is_ancestor(git_dir, c, r["commit"])
                seen = b.get("status_on_main") == "CHANGED_SINCE_PIN" and any(
                    r["commit"].startswith(t["sha"]) for t in b.get("touched_by_after_pin", []))
                entry.update({"registry_commit_descends_from_bundle_commit": descends, "bundle_advisory_names_registry_commit": seen})
                (later_correction if (descends and seen) else different).append(entry)
        else:
            registry_only.append({"path": r["path"], "commit": r["commit"][:8], "role": r.get("role")})
    return {"bundle_agrees": agree, "later_correction_pinned_by_registry_ADVISORY": later_correction,
            "DIFFERENT_bytes_between_bundle_and_registry": different,
            "registry_only_not_in_bundle": registry_only,
            "counts": {"agree": len(agree), "later_correction": len(later_correction),
                       "different_bytes": len(different), "registry_only": len(registry_only)}}


def build_registered(paper: str, git_dir: str, main_ref: str, registry: Path, registry_commit: str,
                     verified_by: str) -> tuple[dict, int]:
    bundle, rc = build(paper, git_dir, main_ref)
    if rc != EXIT_OK:
        return bundle, rc
    pins, reg_sha = registry_pins(registry, paper)
    main = bundle["measured_against_main"]["commit"]
    pin = resolve(git_dir, pins["pin"])
    rows, defects = [], []
    for art in pins["artifacts"]:
        row, d = verify_registry_artifact(git_dir, pin, main, art)
        rows.append(row)
        defects += d
    controls, controls_ok = registry_controls(git_dir, pin, main, pins["artifacts"][0])
    xc = cross_check_bundle(git_dir, bundle, rows)
    if xc["counts"]["different_bytes"]:
        defects.append(f"{xc['counts']['different_bytes']} path(s) hash differently in the bundle and the registry")
    identical = sum(r["verdict"] == "IDENTICAL" for r in rows)
    registered = controls_ok and not defects and identical == len(rows) and len(rows) > 0
    bundle["label"] = REGISTERED_LABEL if registered else LABEL
    bundle["registration"] = {
        "registered": registered,
        "registry": "ORION-paper v2-papers/PAPER_REGISTRY.json",
        "registry_commit": registry_commit, "registry_file_sha256": reg_sha,
        "registry_pins_schema": pins.get("schema"), "registered_on": pins.get("registered"),
        "registered_pin": pin, "registered_pin_is_ancestor_of_main": is_ancestor(git_dir, pin, main),
        "quantity_roots": pins.get("quantity_roots"),
        "verified_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "verified_by": verified_by,
        "verification": {"artifacts": len(rows), "identical": identical,
                         "gating_artifacts": sum(bool(r.get("gating")) for r in rows),
                         "defects": defects, "rows": rows},
        "planted_controls": {"all_caught": controls_ok, "controls": controls},
        "cross_check_with_bundle": xc,
    }
    if not registered:
        bundle["registration"]["awaiting"] = "registry triples did not verify (see verification.defects / planted_controls); label kept PIN_PROPOSED"
    bundle["defects"] = bundle["defects"] + defects
    if not controls_ok:
        return bundle, EXIT_CNC
    return bundle, (EXIT_OK if registered else EXIT_FAIL)


def self_test(git_dir: str) -> int:
    print("build_evidence_bundle self-test")
    ok = True
    main = resolve(git_dir, "origin/main")

    # no-alarm: a real study builds with zero defects and a found terminal
    st, d = build_study(git_dir, main, SPECS["FLAGSHIP"]["studies"][0])
    good = (not d) and st["terminal_found_in_receipt_at_pin"] is True and st["counts"]["files"] > 0
    print(f"  {'ok ' if good else 'BAD'} real study ME-X4: {st['counts']['files']} files, defects={len(d)}")
    ok &= good

    # plant: wrong terminal string must FAIL (a spec typo cannot pin the wrong study silently)
    bad = dict(SPECS["FLAGSHIP"]["studies"][0], terminal_expected="THIS_TERMINAL_DOES_NOT_EXIST_ZZZ")
    st, d = build_study(git_dir, main, bad)
    good = any("terminal string" in x for x in d)
    print(f"  {'ok ' if good else 'BAD'} planted wrong terminal -> defect: {good}")
    ok &= good

    # plant: a commit not on main must be a defect, not silently on_main=False
    st, d = build_study(git_dir, main, dict(SPECS["FLAGSHIP"]["studies"][0], commit="3b51a2e"))
    good = any("not an ancestor" in x for x in d)
    print(f"  {'ok ' if good else 'BAD'} planted off-main commit (3b51a2e) -> defect: {good}")
    ok &= good

    # plant: unresolvable commit must be COULD_NOT_CHECK, never a pass
    try:
        build_study(git_dir, main, dict(SPECS["FLAGSHIP"]["studies"][0], commit="0000000deadbeef"))
        print("  BAD unresolvable commit did not raise"); ok = False
    except CouldNotCheck:
        print("  ok  unresolvable commit -> CouldNotCheck")

    # advisory control: ME-X5 at 024d97f MUST show its receipt CHANGED_SINCE_PIN (the erratum), and the
    # results files UNCHANGED -- a known drift the advisory must catch, and a known non-drift it must not.
    st, d = build_study(git_dir, main, SPECS["FLAGSHIP"]["studies"][3])
    rec = [f for f in st["files"] if f["path"].endswith("ME_X5_OUTCOME_RECEIPT.md")]
    res = [f for f in st["files"] if "/results/" in f["path"]]
    good = rec and rec[0]["status_on_main"] == "CHANGED_SINCE_PIN" and res and all(
        f["status_on_main"] == "UNCHANGED_ON_MAIN" for f in res)
    print(f"  {'ok ' if good else 'BAD'} ME-X5 advisory: receipt CHANGED_SINCE_PIN (erratum), results UNCHANGED")
    ok &= good

    # hashing control: sha256 from the object equals sha256 of the same bytes re-read (no pipe involved)
    f = rec[0]
    again = hashlib.sha256(blob_bytes(git_dir, f["git_blob_sha1"])).hexdigest()
    good = again == f["sha256"]
    print(f"  {'ok ' if good else 'BAD'} sha256 stable across two in-process reads")
    ok &= good

    print("self-test " + ("passed" if ok else "FAILED"))
    return EXIT_OK if ok else EXIT_CNC


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--paper", choices=sorted(SPECS))
    ap.add_argument("--git-dir", required=True)
    ap.add_argument("--main-ref", default="origin/main")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--registry", type=Path, help="registered mode: local copy of ORION-paper v2-papers/PAPER_REGISTRY.json at --registry-commit")
    ap.add_argument("--registry-commit", help="ORION-paper commit the --registry file was read from (recorded, not verified here)")
    ap.add_argument("--verified-by", default="lane-evidence (ORION-V2)")
    a = ap.parse_args(argv)
    try:
        if a.self_test:
            return self_test(a.git_dir)
        if not a.paper or not a.out:
            ap.error("--paper and --out are required unless --self-test")
        if a.registry or a.registry_commit:
            if not (a.registry and a.registry_commit):
                ap.error("--registry and --registry-commit go together")
            bundle, rc = build_registered(a.paper, a.git_dir, a.main_ref, a.registry, a.registry_commit, a.verified_by)
        else:
            bundle, rc = build(a.paper, a.git_dir, a.main_ref)
    except CouldNotCheck as e:
        print(f"COULD NOT CHECK: {e}")
        return EXIT_CNC
    a.out.mkdir(parents=True, exist_ok=True)
    path = a.out / f"{a.paper}_EVIDENCE_BUNDLE_{bundle['label']}_V1.json"
    path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n")
    t = bundle["totals"]
    print(f"{a.paper}: {t['studies']} studies, {t['files']} files; unchanged {t['unchanged_on_main']}, "
          f"changed-since-pin {t['changed_since_pin']}, removed {t['removed_on_main']}, missing-at-pin {t['missing_at_pin']}; "
          f"defects {len(bundle['defects'])} -> {path}")
    for d in bundle["defects"]:
        print("  DEFECT:", d)
    if "planted_controls" in bundle.get("registration", {}):
        reg = bundle["registration"]
        v, pc, xc = reg["verification"], reg["planted_controls"], reg["cross_check_with_bundle"]["counts"]
        print(f"  registry {a.registry_commit[:8]} pin {reg['registered_pin'][:8]}: {v['identical']}/{v['artifacts']} triples IDENTICAL; "
              f"controls caught {sum(c['caught'] for c in pc['controls'])}/{len(pc['controls'])}; "
              f"cross-check agree {xc['agree']}, later-correction advisories {xc['later_correction']}, "
              f"DIFFERENT {xc['different_bytes']}, registry-only {xc['registry_only']}; label {bundle['label']}")
        for c in pc["controls"]:
            print(f"    control {c['control']}: {'caught' if c['caught'] else 'NOT CAUGHT'} ({c['detail']})")
    return rc


if __name__ == "__main__":
    sys.exit(main())

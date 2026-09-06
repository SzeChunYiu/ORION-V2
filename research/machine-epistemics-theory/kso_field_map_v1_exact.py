"""Exact consistency checker for MACHINE_EPISTEMICS_FIELD_MAP_V1.md (stdlib only).

The field map is *derived*: this script parses the eleven theorem batch documents
(`KSO_*_BATCH1..11_V1.md`), their exact checkers (`kso_*_batch1..11_exact.py`, read with
`ast`, never executed), the sealed atlas status sections (`ME_THEORY_GAP_ATLAS_V1.md` §F–§K,
read only) and its addenda (§L–§O), the foundation registry, and a byte-pinned snapshot of the
OCM obligation registries (`OCM_OBLIGATION_REGISTRY_DERIVED_V1.json`,
`existing_registry_snapshot`).  From these it builds

* the theorem table (identifier, topic, statement line, primary status, checker function,
  parent),
* the cross-reference graph (theorem → theorem, theorem → KS-T / MEG / FDX ids, theorem →
  OCM obligation rows discharged or opened),
* the list of exactly bounded impossibilities (from the batch checkers'
  `EXACTLY_BOUNDED_IMPOSSIBILITIES` constants),
* the open list and conjectures with their falsifiers,
* the atlas section map (A–O) with counts,
* the derived OCM obligation registry KS-T118+ (H/I-items of batches 8–11),

checks consistency (unique ids; every status in the vocabulary; every cited KS-T id in a
registry or flagged; every impossibility carries a bound; every OPEN item carries a falsifier
or is flagged; the derived registry equals what the documents yield; the document's generated
regions equal what this script renders), runs planted-mutant controls (duplicated id, unknown
status, dangling KS-T reference, impossibility without bound, open item without falsifier) and
a no-alarm control, prints the summary block the document embeds, and exits non-zero on any
inconsistency.

Exit codes: 0 consistent; 1 inconsistent (reasons printed); 2 CANNOT_CHECK (a source file is
missing).  NO NOVELTY OR SUPERIORITY CLAIM.
"""
from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOC_NAME = "MACHINE_EPISTEMICS_FIELD_MAP_V1.md"
DERIVED_NAME = "OCM_OBLIGATION_REGISTRY_DERIVED_V1.json"
ATLAS_NAME = "ME_THEORY_GAP_ATLAS_V1.md"
ADDENDA_NAME = "ME_THEORY_GAP_ATLAS_ADDENDA_V1.md"
FOUNDATION_JSON = "MACHINE_EPISTEMICS_FOUNDATION_V1.json"
BATCH12_DOC = "KSO_MECHANISED_CORE_BATCH12_V1.md"
DEFAULT_OCM_ROOT = Path("/Users/billy/Desktop/projects/ORION-OCM-wt/m11-self")

STATUS_VOCAB = (
    "PROVED",
    "PROVED (finite)",
    "FINITE_CALIBRATION",
    "PARENT_OWNED",
    "PARENT_SUFFICIENT",
    "EXACTLY_BOUNDED_IMPOSSIBILITY",
    "CONJECTURE",
    "OPEN",
    "CANNOT_CHECK",
)

# batch number, document, checker, theorem-id letter(s), where the per-theorem status lives,
# atlas/addenda section letter that records the batch, frontier/atlas scope.
BATCHES = (
    (1, "KSO_ONE_DAY_THEOREMS_BATCH1_V1.md", "kso_one_day_theorems_batch1_exact.py", ("T",), "doc", None, "atlas §B next tier"),
    (2, "KSO_LANGUAGE_PREREQUISITE_THEOREMS_BATCH2_V1.md", "kso_language_prereqs_batch2_exact.py", ("B",), "atlas:F", "F", "language prerequisites"),
    (3, "KSO_DIALOGUE_PREREQUISITE_THEOREMS_BATCH3_V1.md", "kso_dialogue_prereqs_batch3_exact.py", ("C",), "atlas:G", "G", "dialogue prerequisites"),
    (4, "KSO_COMPARISON_PREREQUISITE_THEOREMS_BATCH4_V1.md", "kso_comparison_prereqs_batch4_exact.py", ("D",), "atlas:H", "H", "comparison prerequisites"),
    (5, "KSO_SELF_MODEL_PREREQUISITE_THEOREMS_BATCH5_V1.md", "kso_self_model_prereqs_batch5_exact.py", ("E", "R"), "doc", "I", "self-model prerequisites"),
    (6, "KSO_LIFETIME_PREREQUISITE_THEOREMS_BATCH6_V1.md", "kso_lifetime_prereqs_batch6_exact.py", ("F",), "doc", "J", "lifetime prerequisites"),
    (7, "KSO_OPEN_LIST_CLOSURE_THEOREMS_BATCH7_V1.md", "kso_open_list_closure_batch7_exact.py", ("G",), "doc", "K", "open-list closure"),
    (8, "KSO_FIELD_FRONTIER_THEOREMS_BATCH8_V1.md", "kso_field_frontier_batch8_exact.py", ("H",), "doc", "L", "field frontier"),
    (9, "KSO_FIELD_FRONTIER_THEOREMS_BATCH9_V1.md", "kso_field_frontier_batch9_exact.py", ("I",), "doc", "N", "field frontier"),
    (10, "KSO_FIELD_FRONTIER_THEOREMS_BATCH10_V1.md", "kso_field_frontier_batch10_exact.py", ("J",), "doc", "M", "field frontier"),
    (11, "KSO_FIELD_FRONTIER_THEOREMS_BATCH11_V1.md", "kso_field_frontier_batch11_exact.py", ("K",), "doc", "O", "field frontier"),
)
OBLIGATION_BATCHES = (8, 9, 10, 11)          # batches whose consequences sections carry H/I-items
BARE_REF_LETTERS = "TBEGI"                    # letters whose bare use (e.g. "E4") is unambiguous;
# C (classes C0–C6, gate clauses), D (diagnostic layers D0–D6), F (frontier notes F1/F2/F6, atlas
# parents-table rows), H (obligation items), J (Jump levels J0–J5), K (contract invariants K1–K4)
# are counted only in the explicit form "batch-N Xk".  A reference is kept only when its target
# lies in the same or an earlier batch.

# KS-T ids cited by the batch documents that have no registry row: the reason is recorded here so
# the citation is *flagged*, never silently accepted.  If a row appears later the flag goes stale
# and the checker fails, which is the intended behaviour.
FLAGGED_KST = {
    "KS-T13": "KSO substrate contract §20 OPEN_M3 id (gap-learning soundness); no registry row — closed on finite classes by B3, the infinite half by G9/K1",
    "KS-T14": "KSO substrate contract §20 OPEN_M4 id (Jump improvement); no registry row — preservation half B8, improvement clause G5 (registry KS-T116 PROVED_WITH_CLAUSE)",
}

# OPEN items and conjectures whose falsifier is executable or stated; keys are the
# (batch, source) pairs the checker derives.  Everything else in an OPEN list is flagged
# NO_EXECUTABLE_FALSIFIER (allowed, reported).
FALSIFIERS = {
    ("E8", "KS-T12"): ("falsify_ks_t12", "kso_self_model_prereqs_batch5_exact.py"),
    ("E8", "KS-T14"): ("falsify_ks_t14", "kso_self_model_prereqs_batch5_exact.py"),
    ("I4", "FDX-15"): ("an OCM−Δ arm that differs from the parent product on a matched unit", "KSO_FIELD_FRONTIER_THEOREMS_BATCH9_V1.md"),
    ("R2", "MEG-27"): ("lookahead_regular", "kso_self_model_prereqs_batch5_exact.py"),
    ("R3", "MEG-02"): ("scalar retraction witness {{a}} vs {{a},{b}}", "KSO_LIFETIME_PREREQUISITE_THEOREMS_BATCH6_V1.md"),
    ("R1", "MEG-19"): ("MDL two-part code KEEP iff (k+1)(1+e) ≤ u(k−1)", "KSO_OPEN_LIST_CLOSURE_THEOREMS_BATCH7_V1.md"),
}
BOUND_MARKERS = ("no ", "never", "below", "≥", "cannot", "impossible", "undecidable", "not ", "only")


class CannotCheck(RuntimeError):
    pass


# ----------------------------------------------------------------------------------------------
# text helpers


def read(path: Path) -> str:
    if not path.exists():
        raise CannotCheck(f"missing source file {path}")
    return path.read_text(encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_cells(row: str) -> list[str]:
    """Split a markdown table row on unescaped pipes."""
    cells, cur, esc = [], [], False
    for ch in row.strip().strip("|"):
        if esc:
            cur.append(ch)
            esc = False
        elif ch == "\\":
            esc = True
            cur.append(ch)
        elif ch == "|":
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    cells.append("".join(cur).strip())
    return cells


def last_text_block(doc: str) -> str:
    blocks = re.findall(r"```text\n(.*?)```", doc, re.S)
    return blocks[-1] if blocks else ""


def primary_status(text: str) -> tuple[str | None, list[str]]:
    """First vocabulary token in a status text and every vocabulary token it mentions."""
    found = []
    for tok in STATUS_VOCAB:
        if tok == "PROVED (finite)":
            for m in re.finditer(r"PROVED \(finite|PROVED for the finite", text):
                found.append((m.start(), tok))
        elif tok == "PROVED":
            for m in re.finditer(r"\bPROVED\b(?! \(finite)(?! for the finite)", text):
                found.append((m.start(), tok))
        elif tok == "EXACTLY_BOUNDED_IMPOSSIBILITY":
            for m in re.finditer(r"EXACTLY_BOUNDED|exactly bounded|IMPOSSIBLE\b", text):
                found.append((m.start(), tok))
        else:
            for m in re.finditer(r"\b" + re.escape(tok) + r"\b", text):
                found.append((m.start(), tok))
    found.sort()
    seen = []
    for _, tok in found:
        if tok not in seen:
            seen.append(tok)
    return (seen[0] if seen else None), seen


def parent_of(body: str, status_text: str) -> str:
    m = re.search(r"Parents?:\s*(.+?)(?<!\bal)(?<!\bvs)(?<!\bcf)(?<!\be\.g)(?<!\bi\.e)(?<! [A-Z])(?:\.\s|\.\n|\n\n)", body, re.S)
    if m:
        return " ".join(m.group(1).split())[:220]
    m = re.search(r"(PARENT_OWNED|PARENT_SUFFICIENT)[^()]*\(([^)]+)\)", status_text)
    if m:
        return f"{m.group(1)} ({m.group(2)})"[:220]
    m = re.search(r"(PARENT_OWNED|PARENT_SUFFICIENT)[^()]*\(([^)]+)\)", body)
    if m:
        return f"{m.group(1)} ({m.group(2)})"[:220]
    return "(no parent sentence in section; see status line)"


def theorem_keys(topic: str, title: str) -> list[str]:
    """Atlas / frontier / contract ids a theorem is filed under (topic cell, else the title head)."""
    ids = re.findall(r"MEG-\d+|FDX-\d+|KS-T\d+", topic)
    if not ids:
        ids = re.findall(r"MEG-\d+|FDX-\d+|KS-T\d+", title.split(":")[0])
    return list(OrderedDict.fromkeys(ids))


def one_line_statement(body: str) -> str:
    m = re.search(r"\*\*Theorem[^*]*\*\*\s*(.+?)(?:\n\n|\Z)", body, re.S)
    if not m:
        m = re.search(r"\*\*(?:Statement|R\d[^*]*)\*\*\s*(.+?)(?:\n\n|\Z)", body, re.S)
    text = " ".join((m.group(1) if m else body).split())
    return text[:240] + ("…" if len(text) > 240 else "")


# ----------------------------------------------------------------------------------------------
# checker-module constants (read with ast; never executed)


def module_constants(path: Path) -> dict:
    tree = ast.parse(read(path))
    out = {"check_functions": [], "functions": []}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            out["functions"].append(node.name)
            if node.name.startswith("check_"):
                out["check_functions"].append(node.name)
        elif isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in ("STATUS", "OPEN", "CONJECTURES", "CANNOT_CHECK_ITEMS", "EXACTLY_BOUNDED_IMPOSSIBILITIES"):
                try:
                    out[name] = ast.literal_eval(node.value)
                except (ValueError, SyntaxError):
                    out[name] = None
            elif name == "CHECKS":
                keys = [k.value for k in node.value.keys if isinstance(k, ast.Constant)] if isinstance(node.value, ast.Dict) else []
                out["CHECKS"] = keys
    return out


# ----------------------------------------------------------------------------------------------
# batch parsing


def theorem_sections(doc: str, letters: tuple[str, ...]) -> list[dict]:
    """Return [{'id','topic','title','body'}] for every `## X<n> · … · …` section."""
    heads = list(re.finditer(r"^## (.+)$", doc, re.M))
    out = []
    for i, h in enumerate(heads):
        head = h.group(1)
        body = doc[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(doc)]
        m = re.match(r"([A-Z])(\d+)(?:–([A-Z])(\d+))? · (.+)$", head)
        if not m or m.group(1) not in letters:
            continue
        rest = [p.strip() for p in m.group(5).split(" · ")]
        topic, title = (rest[0], " · ".join(rest[1:])) if len(rest) >= 2 else ("", rest[0])
        if m.group(3):                                     # range heading, e.g. R1–R3
            lo, hi = int(m.group(2)), int(m.group(4))
            subs = list(re.finditer(r"^\*\*(" + m.group(1) + r"\d) · (.+?) — ([^*]+?)\*\*", body, re.M | re.S))
            for j, s in enumerate(subs):
                sub_body = body[s.start(): subs[j + 1].start() if j + 1 < len(subs) else len(body)]
                out.append({"id": s.group(1), "topic": s.group(2), "title": " ".join(s.group(3).split()), "body": sub_body, "range_head": head})
            if len(subs) != hi - lo + 1:
                out.append({"id": f"{m.group(1)}{lo}–{m.group(1)}{hi}", "topic": topic, "title": title, "body": body, "range_error": len(subs)})
        else:
            out.append({"id": m.group(1) + m.group(2), "topic": topic, "title": title, "body": body})
    return out


def status_lines_from_doc(doc: str, letters: tuple[str, ...]) -> dict[str, str]:
    block = last_text_block(doc)
    out = {}
    for line in block.splitlines():
        m = re.match(r"([A-Z]\d+)\s+(.*)$", line.strip())
        if m and m.group(1)[0] in letters:
            out[m.group(1)] = m.group(2).strip()
    return out


def atlas_section(text: str, letter: str) -> str:
    m = re.search(r"^## " + letter + r"\. (.*?)$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return (m.group(1) + "\n" + m.group(2)) if m else ""


def status_lines_from_atlas(atlas: str, letter: str, letters: tuple[str, ...]) -> tuple[dict[str, str], dict[str, str]]:
    sec = atlas_section(atlas, letter)
    out, gaps = {}, {}
    for row in re.findall(r"^\|(.+)\|\s*$", sec, re.M):
        cells = split_cells("|" + row + "|")
        if len(cells) < 3 or cells[0] in ("gap", "frontier row") or set(cells[0]) <= {"-"}:
            continue
        m = re.match(r"([A-Z]\d+)\b", cells[1])
        if m and m.group(1)[0] in letters:
            out[m.group(1)] = cells[2]
            gaps[m.group(1)] = cells[0]
    return out, gaps


def cited_ids(body: str) -> dict:
    return {
        "kst": sorted(set(re.findall(r"KS-T\d+[a-z]?", body)), key=lambda s: (len(s), s)),
        "ks_other": sorted(set(re.findall(r"KS-(?:S|A|R|P|EQ)\d*", body))),
        "meg": sorted(set(re.findall(r"MEG-\d+", body))),
        "fdx": sorted(set(re.findall(r"FDX-\d+", body))),
        "fd": sorted(set(re.findall(r"\bFD-\d+", body))),
    }


def theorem_refs(body: str, own_id: str, known: dict[str, int], own_batch: int) -> tuple[list[str], list[str]]:
    explicit, bare = set(), set()
    for m in re.finditer(r"batch(?:es)?[- ]?(\d+)(?:'s)?\s+([A-K])(\d{1,2})((?:\s*[/,]\s*(?:and\s+)?[A-K]?\d{1,2})*)", body):
        letter = m.group(2)
        explicit.add(letter + m.group(3))
        for t in re.findall(r"([A-K])?(\d{1,2})", m.group(4)):
            explicit.add((t[0] or letter) + t[1])
    for m in re.finditer(r"\b([" + BARE_REF_LETTERS + r"])(\d{1,2})\b", body):
        bare.add(m.group(1) + m.group(2))
    explicit = {t for t in explicit if t in known and t != own_id and known[t] <= own_batch}
    bare = {t for t in bare if t in known and t != own_id and t not in explicit and known[t] <= own_batch}
    return sorted(explicit), sorted(bare)


def obligation_items(doc: str, batch: int, theorem_ids: list[str]) -> list[dict]:
    m = re.search(r"^## Consequences.*?$(.*?)(?=^```text|^## Verification|^## Status|\Z)", doc, re.M | re.S)
    if not m:
        return []
    sec = m.group(1)
    bullets = list(re.finditer(r"^\* \*\*([A-Z]\d+)(?: \(([^)]+)\))? — (.+?)\*\*", sec, re.M | re.S))
    items = []
    for i, b in enumerate(bullets):
        body = sec[b.end(): bullets[i + 1].start() if i + 1 < len(bullets) else len(sec)]
        body = " ".join(body.split())
        paren = b.group(2) or ""
        src = re.match(r"([A-Z]\d+)", paren)
        source_theorem = src.group(1) if src else b.group(1)
        if source_theorem not in theorem_ids:
            source_theorem = None
        obl = re.search(r"Obligation:\s*(.+?)(?:(?<=\.)\s+`?[A-Z]|\Z)", body)
        obligation = obl.group(1).strip() if obl else ""
        spans = re.findall(r"`([^`]+)`", body)
        locations = [s for s in spans if not s.startswith("mutant_") and not re.fullmatch(r"[A-Z0-9_]+", s)
                     and ("/" in s or ".py" in s or "::" in s or re.match(r"^[A-Za-z_][A-Za-z_]*\.[A-Za-z_]", s))]
        mutants = [s for s in spans if s.startswith("mutant_")]
        items.append({
            "batch": batch,
            "item": b.group(1),
            "clauses": paren,
            "source_theorem": source_theorem,
            "title": " ".join(b.group(3).split()),
            "obligation": obligation,
            "runtime_locations": list(OrderedDict.fromkeys(locations)),
            "mutants": list(OrderedDict.fromkeys(mutants)),
        })
    return items


# ----------------------------------------------------------------------------------------------
# registries


def load_snapshot(derived_path: Path) -> dict:
    if not derived_path.exists():
        return {}
    return json.loads(read(derived_path)).get("existing_registry_snapshot", {})


def live_registries(ocm_root: Path) -> dict:
    out = {}
    d = ocm_root / "docs" / "theorems"
    if not d.exists():
        return out
    for p in sorted(d.glob("*.json")):
        data = json.loads(read(p))
        out[p.name] = {
            "sha256": sha256(p),
            "registry": data.get("registry"),
            "obligations": {r["id"]: {"status": r["status"], "gap": r.get("gap", ""), "checker": r.get("checker", ""), "statement": r.get("statement", "")} for r in data["obligations"]},
        }
    return out


def kst_number(kid: str) -> int:
    m = re.match(r"KS-T(\d+)", kid)
    return int(m.group(1)) if m else -1


def kst_key(kid: str) -> tuple[int, str]:
    """Deterministic sort key (number, then id) — ties like KS-T04 / KS-T04b / KS-T04c keep a fixed order."""
    return (kst_number(kid), kid)


# ----------------------------------------------------------------------------------------------
# model


def build_model(root: Path = HERE, ocm_root: Path | None = None, snapshot: dict | None = None) -> dict:
    atlas = read(root / ATLAS_NAME)
    addenda = read(root / ADDENDA_NAME)
    foundation = json.loads(read(root / FOUNDATION_JSON))
    theorems: list[dict] = []
    batches: dict[int, dict] = {}
    obligations: list[dict] = []
    impossibilities: list[dict] = []
    open_items: list[dict] = []
    conjectures: list[dict] = []
    cannot_check: list[dict] = []
    # pass 1: sections and statuses
    for n, docname, chkname, letters, statsrc, section, scope in BATCHES:
        doc = read(root / docname)
        consts = module_constants(root / chkname)
        secs = theorem_sections(doc, letters)
        if statsrc == "doc":
            statuses = status_lines_from_doc(doc, letters)
            gaps = {}
        else:
            statuses, gaps = status_lines_from_atlas(atlas, statsrc.split(":")[1], letters)
        batches[n] = {"doc": docname, "checker": chkname, "letters": letters, "status_source": statsrc, "atlas_section": section,
                      "scope": scope, "consts": consts, "sha256": sha256(root / docname), "status_lines": statuses, "atlas_gap": gaps}
        for s in secs:
            st = " ".join(statuses.get(s["id"], "").split())
            prim, all_st = primary_status(st)
            fns = [f for f in consts["check_functions"] if f.startswith("check_" + s["id"].lower() + "_")]
            theorems.append({
                "batch": n, "id": s["id"], "topic": s["topic"], "title": s["title"], "statement": one_line_statement(s["body"]),
                "status_text": st, "status": prim, "statuses": all_st, "checker": fns, "parent": parent_of(s["body"], st),
                "cites": cited_ids(s["body"]), "_body": s["body"], "range_error": s.get("range_error"),
                "keys": theorem_keys(s["topic"], s["title"]),
            })
    known = {t["id"]: t["batch"] for t in theorems}
    for t in theorems:
        t["refs_explicit"], t["refs_bare"] = theorem_refs(t["_body"], t["id"], known, t["batch"])
    # pass 2: obligations, impossibilities, open lists
    for n, docname, chkname, letters, statsrc, section, scope in BATCHES:
        doc = read(root / docname)
        consts = batches[n]["consts"]
        ids = [t["id"] for t in theorems if t["batch"] == n]
        if n in OBLIGATION_BATCHES:
            obligations.extend(obligation_items(doc, n, ids))
        for entry in consts.get("EXACTLY_BOUNDED_IMPOSSIBILITIES") or []:
            m = re.match(r"((?:FDX|MEG)-\d+|KS-T\d+)(?:\s+(J\d))?[^:]*:\s*(.*)$", entry, re.S)
            key, sub, text = (m.group(1), m.group(2), m.group(3)) if m else (None, None, entry)
            owner = owner_theorem(theorems, n, key, text)
            impossibilities.append({"batch": n, "row": key, "sub": sub, "bound": " ".join(text.split()), "theorem": owner["id"] if owner else None,
                                    "fixture": owner["status_text"] if owner else "", "parent": owner["parent"] if owner else "",
                                    "has_bound": any(k in text.lower() for k in BOUND_MARKERS)})
        for entry in consts.get("OPEN") or []:
            key, text = split_entry(entry)
            owner = owner_theorem(theorems, n, key, entry)
            open_items.append({"batch": n, "row": key, "theorem": owner["id"] if owner else None, "text": " ".join(text.split()), "kind": "OPEN"})
        for entry in consts.get("CONJECTURES") or []:
            key, text = split_entry(entry)
            owner = owner_theorem(theorems, n, key, entry)
            conjectures.append({"batch": n, "row": key, "theorem": owner["id"] if owner else None, "text": " ".join(text.split()), "kind": "CONJECTURE"})
        for entry in consts.get("CANNOT_CHECK_ITEMS") or []:
            key, text = split_entry(entry)
            cannot_check.append({"batch": n, "row": key, "text": " ".join(text.split())})
    # theorem-level OPEN / CONJECTURE rows (batches without OPEN constants)
    for t in theorems:
        if t["status"] == "CONJECTURE":
            for key in t["keys"] or [t["title"]]:
                conjectures.append({"batch": t["batch"], "row": key, "theorem": t["id"], "text": t["status_text"], "kind": "CONJECTURE"})
        if "OPEN" in t["statuses"] and t["batch"] < 8:
            key = (t["keys"] or [t["title"]])[0]
            later = [u["id"] for u in theorems if u["batch"] > t["batch"] and key in u["keys"]]
            open_items.append({"batch": t["batch"], "row": key, "theorem": t["id"], "text": t["status_text"],
                               "kind": "OPEN_HALF_CLOSED_LATER" if later else "OPEN", "closed_by": later})
    for o in open_items + conjectures:
        key = (o["theorem"], o["row"])
        fal = FALSIFIERS.get(key)
        o["falsifier"] = fal[0] if fal else None
        o["falsifier_source"] = fal[1] if fal else None
        if o.get("closed_by"):
            o["flag"] = "CLOSED_LATER by " + ", ".join(o["closed_by"])
        elif o["kind"] == "OPEN" and not o["falsifier"]:
            o["flag"] = "NO_EXECUTABLE_FALSIFIER"
    # registries
    snap = snapshot if snapshot is not None else load_snapshot(root / DERIVED_NAME)
    live = live_registries(ocm_root) if ocm_root else {}
    registry = snap
    all_rows = {}
    for fname, reg in registry.items():
        for kid, row in reg["obligations"].items():
            all_rows[kid] = dict(row, registry=fname)
    max_existing = max((kst_number(k) for k in all_rows), default=-1)
    # theorem → registry rows (discharge map)
    topic_index: dict[str, list[str]] = {}
    for t in theorems:
        for key in t["keys"]:
            topic_index.setdefault(key, []).append(t["id"])
    for t in theorems:
        t["registry_rows"] = []
    for kid, row in all_rows.items():
        gap = row.get("gap", "") or ""
        linked = set()
        for m in re.finditer(r"batch (\d+) ([A-Z]\d)", gap):
            for t in theorems:
                if t["batch"] == int(m.group(1)) and t["id"] == m.group(2):
                    linked.add(t["id"])
        for m in re.finditer(r"MEG-(\d+)(?:/(\d+))*", gap):
            for num in re.findall(r"\d+", m.group(0)):
                for tid in topic_index.get(f"MEG-{int(num):02d}", []):
                    linked.add(tid)
        for tid in linked:
            next(t for t in theorems if t["id"] == tid)["registry_rows"].append(kid)
    for t in theorems:
        t["registry_rows"].sort(key=kst_key)
        t["discharges"] = [k for k in t["registry_rows"] if all_rows[k]["status"].startswith("PROVED") or all_rows[k]["status"].startswith("PARENT_OWNED")]
        t["opens"] = [k for k in t["registry_rows"] if k not in t["discharges"]]
    # derived registry
    derived = derive_registry(obligations, all_rows, max_existing, theorems)
    # atlas sections
    foundation_summary = {"atlas_status": Counter(v.get("status") for v in foundation["atlas"].values()), "primitives": len(foundation["primitives"]), "status": foundation["status"]}
    sections = atlas_sections(atlas, addenda, theorems, batches, foundation_summary)
    frontier = read(root / "field_dynamics_v1" / "FRONTIER.md")
    inconsistencies = find_inconsistencies(theorems, batches, sections, obligations, frontier, foundation_summary)
    # batch-12 slot
    b12 = root / BATCH12_DOC
    slot = {"present": b12.exists()}
    if b12.exists():
        blk = last_text_block(read(b12))
        slot["status_lines"] = [ln for ln in blk.splitlines() if ln.strip()]
        slot["counts"] = Counter(primary_status(ln)[0] or "UNCLASSIFIED" for ln in slot["status_lines"] if not ln.startswith("Lean") and not ln.startswith("NOVELTY"))
        slot["sha256"] = sha256(b12)
    for t in theorems:
        t.pop("_body", None)
    return {
        "theorems": theorems, "batches": batches, "obligations": obligations, "impossibilities": impossibilities,
        "open_items": open_items, "conjectures": conjectures, "cannot_check": cannot_check, "registry": registry,
        "registry_rows": all_rows, "max_existing_kst": max_existing, "derived": derived, "sections": sections,
        "foundation": foundation_summary, "inconsistencies": inconsistencies,
        "live_registries": live, "batch12_slot": slot, "atlas_sha256": sha256(root / ATLAS_NAME),
    }


def split_entry(entry: str) -> tuple[str | None, str]:
    """'FDX-06: text' → ('FDX-06', 'text'); 'FD-07 / FDX-03 general …' → ('FD-07', whole entry)."""
    m = re.match(r"((?:FDX|MEG|FD)-\d+|KS-T\d+)", entry)
    key = m.group(1) if m else None
    if ":" in entry and (m is None or entry.index(":") < 40):
        text = entry.split(":", 1)[1]
    else:
        text = entry
    return key, " ".join(text.split())


def owner_theorem(theorems: list[dict], batch: int, key: str | None, text: str) -> dict | None:
    cands = [t for t in theorems if t["batch"] == batch]
    if key:
        for t in cands:
            if key in t["keys"]:
                return t
    for k in re.findall(r"FDX-\d+|MEG-\d+|KS-T\d+", text):
        for t in cands:
            if k in t["keys"]:
                return t
    return None


def derive_registry(obligations: list[dict], all_rows: dict, max_existing: int, theorems: list[dict]) -> list[dict]:
    """OCM runtime obligations KS-T118+ from the H/I-items of batches 8–11."""
    by_source = {}
    for kid, row in all_rows.items():
        m = re.search(r"batch (\d+) ([A-Z]\d+)", row.get("gap", "") or "")
        if m and kst_number(kid) >= 118:
            by_source[(int(m.group(1)), m.group(2))] = kid
    next_id = max_existing + 1
    out = []
    for o in obligations:
        th = next((t for t in theorems if t["id"] == o["source_theorem"]), None) if o["source_theorem"] else None
        existing = by_source.get((o["batch"], o["item"]))
        if existing:
            row = all_rows[existing]
            rid, status, checker = existing, row["status"], row.get("checker", "")
            status = status if (status.startswith("PROVED") and checker) else "OPEN"
        else:
            rid, status, checker = f"KS-T{next_id}", "OPEN", ""
            next_id += 1
        out.append(OrderedDict([
            ("id", rid),
            ("existing_row", bool(existing)),
            ("gap", f"batch {o['batch']} {o['item']}" + (f" ({o['source_theorem']}" + (f" {o['clauses'].split(' ', 1)[1]}" if o["clauses"] and " " in o["clauses"] else "") + ")" if o["source_theorem"] else "")),
            ("source_batch", o["batch"]),
            ("source_item", o["item"]),
            ("source_theorem", o["source_theorem"]),
            ("frontier_row", (re.findall(r"FDX-\d+|MEG-\d+", th["topic"]) or [None])[0] if th else None),
            ("statement", o["title"] + ((" Obligation: " + o["obligation"]) if o["obligation"] else "")),
            ("runtime_location", o["runtime_locations"]),
            ("status", status),
            ("checker", checker or None),
            ("mutant", o["mutants"] or None),
            ("parent", th["parent"] if th else None),
        ]))
    return out


def atlas_sections(atlas: str, addenda: str, theorems: list[dict], batches: dict, foundation: dict) -> list[dict]:
    out = []
    names = {}
    for m in re.finditer(r"^## ([A-Z])\. (.+)$", atlas, re.M):
        names[m.group(1)] = ("atlas", m.group(2).strip())
    for m in re.finditer(r"^## ([A-Z])\. (.+)$", addenda, re.M):
        names[m.group(1)] = ("addenda", m.group(2).strip())
    for letter in "ABCDEFGHIJKLMNO":
        src, title = names.get(letter, (None, None))
        text = atlas_section(atlas if src == "atlas" else addenda, letter) if src else ""
        row = {"section": letter, "source": src, "title": title, "present": src is not None}
        if not src:
            row.update({"rows": 0, "note": "no such section in the atlas or its addenda (letters skip E)"})
            out.append(row)
            continue
        batch = next((n for n, b in batches.items() if b["atlas_section"] == letter), None)
        table_rows = [split_cells(r) for r in re.findall(r"^\|.+\|\s*$", text, re.M)]
        table_rows = [r for r in table_rows if r and r[0] not in ("gap", "frontier row") and not set(r[0]) <= {"-"}]
        if letter == "B":
            ids = re.findall(r"^\*\*(MEG-\d+)", text, re.M)
            covered = sorted({i for i in ids if any(i in t["keys"] for t in theorems)})
            row.update({"rows": len(ids), "gaps_listed": len(ids), "gaps_with_theorem": len(covered), "gaps_without_theorem": sorted(set(ids) - set(covered)),
                        "foundation_status_at_freeze": dict(foundation["atlas_status"]) if isinstance(foundation, dict) and "atlas_status" in foundation else None})
        elif letter == "C":
            row.update({"rows": len(re.findall(r"^\d+\. ", text, re.M)), "note": "priority list (no theorem rows)"})
        elif letter == "D":
            row.update({"rows": len(table_rows) or len(re.findall(r"^[*-] ", text, re.M)), "note": "parent-owned, cite and adopt (no theorem rows)"})
        elif letter == "A":
            row.update({"rows": len(table_rows), "note": "existing theory map (no gaps)"})
        elif batch is not None:
            ths = [t for t in theorems if t["batch"] == batch]
            row.update({"batch": batch, "rows": len(table_rows), "theorems": len(ths),
                        "by_status": dict(Counter(t["status"] for t in ths)),
                        "parent_owned_or_sufficient": sum(1 for t in ths if t["status"] in ("PARENT_OWNED", "PARENT_SUFFICIENT")),
                        "open_or_conjecture_mentions": sum(1 for t in ths if "OPEN" in t["statuses"] or "CONJECTURE" in t["statuses"]),
                        "table_rows_equal_theorems": len(table_rows) == len(ths)})
        out.append(row)
    return out


# ----------------------------------------------------------------------------------------------
# non-fatal findings about the earlier documents (reported, never silently fixed)


def find_inconsistencies(theorems, batches, sections, obligations, frontier, foundation) -> list[str]:
    out = []
    for n, b in batches.items():
        st = b["consts"].get("STATUS")
        if isinstance(st, dict):
            for k, v in st.items():
                tid = re.match(r"([A-Z]\d+)", k).group(1)
                th = next((t for t in theorems if t["id"] == tid), None)
                if th and primary_status(v)[0] != th["status"] and {primary_status(v)[0], th["status"]} <= {"PROVED", "PROVED (finite)"}:
                    out.append(f"STATUS_WORDING {tid}: document status block says {th['status']!r}, checker STATUS says {primary_status(v)[0]!r} (same family)")
    for s in sections:
        if not s["present"]:
            out.append(f"ATLAS_SECTION_LETTER_ABSENT {s['section']}: the atlas skips this letter (D → F)")
    order = [(s["section"], s.get("batch")) for s in sections if s.get("batch")]
    for (l1, b1), (l2, b2) in zip(order, order[1:]):
        if b2 < b1:
            out.append(f"ADDENDA_SECTION_ORDER section {l2} records batch {b2} after section {l1} records batch {b1} (written in parallel)")
    for t in theorems:
        if not t["topic"]:
            out.append(f"HEADING_WITHOUT_TOPIC_CELL {t['id']}: two-part heading; filed under {t['keys'] or 'no atlas id'}")
    b8 = {t["id"] for t in theorems if t["batch"] == 8}
    coll = sorted({o["item"] for o in obligations if o["batch"] != 8 and o["item"] in b8})
    if coll:
        out.append(f"OBLIGATION_ID_COLLISION batches {sorted({o['batch'] for o in obligations if o['batch'] != 8 and o['item'] in b8})} label obligation items {coll} with batch-8 theorem ids")
    m = re.search(r"untouched: ([^.]+)\.", frontier)
    if m:
        for num in re.findall(r"\d+", m.group(1)):
            fid = f"FDX-{int(num):02d}"
            sec = re.search(r"^## " + fid + r" .*?$(.*?)(?=^## |\Z)", frontier, re.M | re.S)
            if sec and re.search(r"^Batch \d+ disposition", sec.group(1), re.M):
                out.append(f"FRONTIER_PRIORITY_STALE {fid} listed as untouched in the Priority paragraph but carries a batch disposition")
    open_at_freeze = foundation["atlas_status"].get("OPEN", 0)
    covered = next(s for s in sections if s["section"] == "B")
    if open_at_freeze and covered["gaps_with_theorem"] == covered["gaps_listed"]:
        out.append(f"FOUNDATION_REGISTRY_SEALED {open_at_freeze} atlas rows are OPEN in MACHINE_EPISTEMICS_FOUNDATION_V1.json (frozen at #319) while every one of the {covered['gaps_listed']} atlas gap ids now carries a theorem; the sealed registry is not the current status")
    return out


# ----------------------------------------------------------------------------------------------
# consistency


def check_consistency(model: dict) -> list[str]:
    errors = []
    theorems = model["theorems"]
    ids = [t["id"] for t in theorems]
    for tid, c in Counter(ids).items():
        if c > 1:
            errors.append(f"DUPLICATE_ID {tid} appears {c} times")
    for t in theorems:
        if t.get("range_error") is not None:
            errors.append(f"RANGE_HEADING {t['id']} expands to {t['range_error']} sub-sections")
        if not t["status_text"]:
            errors.append(f"NO_STATUS_LINE {t['id']} (batch {t['batch']})")
        elif t["status"] not in STATUS_VOCAB:
            errors.append(f"UNKNOWN_STATUS {t['id']}: {t['status_text'][:60]!r}")
        if len(t["checker"]) != 1:
            errors.append(f"CHECKER_FUNCTION {t['id']}: {len(t['checker'])} functions match check_{t['id'].lower()}_*")
    for n, b in model["batches"].items():
        heads = {t["id"] for t in theorems if t["batch"] == n}
        extra = set(b["status_lines"]) - heads
        if extra:
            errors.append(f"STATUS_WITHOUT_SECTION batch {n}: {sorted(extra)}")
        st = b["consts"].get("STATUS")
        if isinstance(st, dict):
            for k, v in st.items():
                tid = re.match(r"([A-Z]\d+)", k).group(1)
                th = next((t for t in theorems if t["id"] == tid), None)
                if th is None:
                    errors.append(f"CHECKER_STATUS_UNKNOWN_ID batch {n} {k}")
                elif primary_status(v)[0] != th["status"] and not {primary_status(v)[0], th["status"]} <= {"PROVED", "PROVED (finite)"}:
                    errors.append(f"CHECKER_STATUS_DISAGREES {tid}: doc {th['status']} vs checker {primary_status(v)[0]}")
    rows = model["registry_rows"]
    cited = sorted({k for t in theorems for k in t["cites"]["kst"]}, key=kst_key)
    for k in cited:
        if k not in rows and k not in FLAGGED_KST:
            errors.append(f"DANGLING_KST {k} cited but in no registry and not flagged")
    for k in FLAGGED_KST:
        if k in rows:
            errors.append(f"STALE_FLAG {k} is flagged but a registry row exists")
    for imp in model["impossibilities"]:
        if not imp["has_bound"]:
            errors.append(f"IMPOSSIBILITY_WITHOUT_BOUND batch {imp['batch']} {imp['row']}: {imp['bound'][:50]!r}")
        if imp["theorem"] is None:
            errors.append(f"IMPOSSIBILITY_WITHOUT_THEOREM batch {imp['batch']} {imp['row']}")
    for o in model["conjectures"]:
        if not o["falsifier"]:
            errors.append(f"CONJECTURE_WITHOUT_FALSIFIER {o['theorem']} {o['row']}")
    for o in model["open_items"]:
        if not o["falsifier"] and not o.get("flag"):
            errors.append(f"OPEN_ITEM_WITHOUT_FALSIFIER_OR_FLAG {o['theorem']} {o['row']}")
        if o["theorem"] is None:
            errors.append(f"OPEN_ITEM_WITHOUT_THEOREM batch {o['batch']} {o['row']}")
    for o in model["open_items"] + model["conjectures"]:
        fal, src = o.get("falsifier"), o.get("falsifier_source")
        if fal and src and src.endswith(".py"):
            consts = next((b["consts"] for b in model["batches"].values() if b["checker"] == src), None)
            if consts is None or fal not in consts["functions"]:
                errors.append(f"FALSIFIER_FUNCTION_MISSING {fal} in {src}")
    for o in model["obligations"]:
        if o["source_theorem"] is None:
            errors.append(f"OBLIGATION_WITHOUT_THEOREM batch {o['batch']} {o['item']}")
    d = model["derived"]
    did = [r["id"] for r in d]
    for k, c in Counter(did).items():
        if c > 1:
            errors.append(f"DERIVED_DUPLICATE {k}")
    new = [kst_number(r["id"]) for r in d if not r["existing_row"]]
    if new and new != list(range(model["max_existing_kst"] + 1, model["max_existing_kst"] + 1 + len(new))):
        errors.append(f"DERIVED_NUMBERING new ids {new} do not continue after KS-T{model['max_existing_kst']}")
    for r in d:
        if r["status"] not in ("PROVED", "OPEN"):
            errors.append(f"DERIVED_STATUS {r['id']} {r['status']}")
        if r["status"] == "PROVED" and not r["checker"]:
            errors.append(f"DERIVED_PROVED_WITHOUT_CHECKER {r['id']}")
        if r["existing_row"] and r["id"] not in rows:
            errors.append(f"DERIVED_EXISTING_MISSING {r['id']}")
    live = model.get("live_registries") or {}
    for fname, reg in live.items():
        snap = model["registry"].get(fname)
        if snap is None:
            errors.append(f"SNAPSHOT_MISSING_REGISTRY {fname}")
            continue
        for kid, row in reg["obligations"].items():
            srow = snap["obligations"].get(kid)
            if srow is None:
                errors.append(f"SNAPSHOT_MISSING_ROW {fname} {kid}")
            elif srow["status"] != row["status"]:
                errors.append(f"SNAPSHOT_STATUS_DRIFT {kid}: snapshot {srow['status']} vs live {row['status']}")
        if snap.get("sha256") != reg["sha256"]:
            errors.append(f"SNAPSHOT_SHA_DRIFT {fname}")
    return errors


# ----------------------------------------------------------------------------------------------
# rendering


def summary_counts(model: dict) -> OrderedDict:
    th = model["theorems"]
    by_status = Counter(t["status"] for t in th)
    by_batch = Counter(t["batch"] for t in th)
    parent_primary = sum(1 for t in th if t["status"] in ("PARENT_OWNED", "PARENT_SUFFICIENT"))
    parent_any = sum(1 for t in th if "PARENT_OWNED" in t["statuses"] or "PARENT_SUFFICIENT" in t["statuses"])
    cited = sorted({k for t in th for k in t["cites"]["kst"]}, key=kst_key)
    flagged = [k for k in cited if k in FLAGGED_KST]
    edges_explicit = sum(len(t["refs_explicit"]) for t in th)
    edges_bare = sum(len(t["refs_bare"]) for t in th)
    discharges = sorted({k for t in th for k in t["discharges"]}, key=kst_key)
    opens = sorted({k for t in th for k in t["opens"]}, key=kst_key)
    d = model["derived"]
    return OrderedDict([
        ("batches", len(model["batches"])),
        ("theorems", len(th)),
        ("theorems_by_batch", OrderedDict(sorted(by_batch.items()))),
        ("theorems_by_status", OrderedDict((s, by_status[s]) for s in STATUS_VOCAB if by_status[s])),
        ("parent_owned_or_sufficient_primary", parent_primary),
        ("parent_owned_or_sufficient_any_mention", parent_any),
        ("exactly_bounded_impossibilities", len(model["impossibilities"])),
        ("impossibilities_by_batch", OrderedDict(sorted(Counter(i["batch"] for i in model["impossibilities"]).items()))),
        ("open_items_current", sum(1 for o in model["open_items"] if o["kind"] == "OPEN")),
        ("open_items_current_with_falsifier", sum(1 for o in model["open_items"] if o["kind"] == "OPEN" and o["falsifier"])),
        ("open_items_current_flagged_no_executable_falsifier", sum(1 for o in model["open_items"] if o["kind"] == "OPEN" and not o["falsifier"])),
        ("open_halves_closed_by_a_later_batch", sum(1 for o in model["open_items"] if o["kind"] == "OPEN_HALF_CLOSED_LATER")),
        ("conjectures", len(model["conjectures"])),
        ("conjectures_with_falsifier", sum(1 for o in model["conjectures"] if o["falsifier"])),
        ("cannot_check_items", len(model["cannot_check"])),
        ("kst_ids_cited", len(cited)),
        ("kst_ids_cited_in_registry", len(cited) - len(flagged)),
        ("kst_ids_cited_flagged", flagged),
        ("dependency_edges_theorem_to_theorem", edges_explicit + edges_bare),
        ("dependency_edges_explicit", edges_explicit),
        ("dependency_edges_bare", edges_bare),
        ("registry_rows_in_snapshot", len(model["registry_rows"])),
        ("registry_rows_linked_to_theorems", len(set(discharges) | set(opens))),
        ("registry_rows_discharged", len(discharges)),
        ("registry_rows_left_open", len(opens)),
        ("highest_existing_kst", f"KS-T{model['max_existing_kst']}"),
        ("derived_obligations", len(d)),
        ("derived_existing_rows", sum(1 for r in d if r["existing_row"])),
        ("derived_new_rows", sum(1 for r in d if not r["existing_row"])),
        ("derived_new_id_range", (f"{d[[r['existing_row'] for r in d].index(False)]['id']}–{d[-1]['id']}" if any(not r["existing_row"] for r in d) else "none")),
        ("derived_by_status", OrderedDict(sorted(Counter(r["status"] for r in d).items()))),
        ("atlas_sections_present", [s["section"] for s in model["sections"] if s["present"]]),
        ("atlas_sections_absent", [s["section"] for s in model["sections"] if not s["present"]]),
        ("atlas_gaps_listed", next(s["gaps_listed"] for s in model["sections"] if s["section"] == "B")),
        ("atlas_gaps_with_theorem", next(s["gaps_with_theorem"] for s in model["sections"] if s["section"] == "B")),
        ("foundation_registry_atlas_status_at_freeze", OrderedDict(sorted(model["foundation"]["atlas_status"].items()))),
        ("inconsistencies_reported_non_fatal", len(model["inconsistencies"])),
        ("novelty", "NOT_ESTABLISHED"),
    ])


def summary_block(model: dict) -> str:
    c = summary_counts(model)
    lines = ["KSO FIELD MAP V1 — Machine Epistemics theory batches 1–11 (first version)"]
    for k, v in c.items():
        if isinstance(v, dict):
            v = ", ".join(f"{kk} {vv}" for kk, vv in v.items())
        elif isinstance(v, list):
            v = ", ".join(v) if v else "none"
        lines.append(f"{k:<45} {v}")
    return "\n".join(lines) + "\n"


def md_escape(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def render_regions(model: dict) -> OrderedDict:
    th = model["theorems"]
    rows = model["registry_rows"]
    R = OrderedDict()
    R["summary"] = "```text\n" + summary_block(model) + "```\n"
    # theorem table
    lines = ["| batch | id | filed under | one-line statement (section heading) | primary status | statuses mentioned | checker function | parent |", "|---|---|---|---|---|---|---|---|"]
    for t in th:
        lines.append("| %d | %s | %s | %s | %s | %s | `%s` | %s |" % (
            t["batch"], t["id"], md_escape(t["topic"]) or "—", md_escape(t["title"]), t["status"], ", ".join(t["statuses"]),
            t["checker"][0] if t["checker"] else "—", md_escape(t["parent"])))
    R["theorems"] = "\n".join(lines) + "\n"
    # graph
    lines = ["| id | depends on (explicit) | depends on (bare) | KS-T cited | MEG / FDX cited | discharges | leaves open |", "|---|---|---|---|---|---|---|"]
    for t in th:
        lines.append("| %s | %s | %s | %s | %s | %s | %s |" % (
            t["id"], ", ".join(t["refs_explicit"]) or "—", ", ".join(t["refs_bare"]) or "—", ", ".join(t["cites"]["kst"]) or "—",
            ", ".join(t["cites"]["meg"] + t["cites"]["fdx"]) or "—", ", ".join(t["discharges"]) or "—", ", ".join(t["opens"]) or "—"))
    R["graph"] = "\n".join(lines) + "\n"
    # kst flags
    cited = sorted({k for t in th for k in t["cites"]["kst"]}, key=kst_key)
    lines = ["| KS-T id | registry | status | cited by |", "|---|---|---|---|"]
    for k in cited:
        by = ", ".join(t["id"] for t in th if k in t["cites"]["kst"])
        if k in rows:
            lines.append(f"| {k} | {rows[k]['registry']} | {rows[k]['status']} | {by} |")
        else:
            lines.append(f"| {k} | **FLAGGED: no registry row** — {md_escape(FLAGGED_KST.get(k, 'unexplained'))} | — | {by} |")
    R["kst"] = "\n".join(lines) + "\n"
    # impossibilities
    lines = ["| # | batch | row | theorem | exact bound | fixture / witness (status line) | parent |", "|---|---|---|---|---|---|---|"]
    for i, imp in enumerate(model["impossibilities"], 1):
        lines.append("| %d | %d | %s%s | %s | %s | %s | %s |" % (i, imp["batch"], imp["row"], f" {imp['sub']}" if imp["sub"] else "", imp["theorem"],
                                                              md_escape(imp["bound"]), md_escape(imp["fixture"]), md_escape(imp["parent"])))
    R["impossibilities"] = "\n".join(lines) + "\n"
    # open list
    lines = ["| kind | batch | row | theorem | item | falsifier | flag |", "|---|---|---|---|---|---|---|"]
    for o in model["conjectures"] + model["open_items"]:
        fal = f"`{o['falsifier']}` ({o['falsifier_source']})" if o["falsifier"] and o["falsifier_source"] and o["falsifier_source"].endswith(".py") else (md_escape(o["falsifier"]) if o["falsifier"] else "—")
        lines.append("| %s | %d | %s | %s | %s | %s | %s |" % (o["kind"], o["batch"], o["row"], o["theorem"] or "—", md_escape(o["text"]), fal, o.get("flag") or "—"))
    for c in model["cannot_check"]:
        lines.append("| CANNOT_CHECK | %d | %s | — | %s | — | recorded, never a pass |" % (c["batch"], c["row"], md_escape(c["text"])))
    R["open"] = "\n".join(lines) + "\n"
    # sections
    lines = ["| section | source | title | rows | theorems | by status | parent-owned/sufficient | note |", "|---|---|---|---|---|---|---|---|"]
    for s in model["sections"]:
        bys = ", ".join(f"{k} {v}" for k, v in s.get("by_status", {}).items()) if s.get("by_status") else "—"
        note = s.get("note") or ""
        if s["section"] == "B":
            note = f"{s['gaps_with_theorem']}/{s['gaps_listed']} gap ids carry at least one theorem; foundation registry at freeze: " + ", ".join(f"{k} {v}" for k, v in sorted(s["foundation_status_at_freeze"].items()))
        if s.get("table_rows_equal_theorems") is False:
            note += " (table rows ≠ theorems: split rows)"
        lines.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (s["section"], s["source"] or "—", md_escape(s["title"] or "—"), s.get("rows", 0),
                                                                  s.get("theorems", "—"), bys, s.get("parent_owned_or_sufficient", "—"), md_escape(note)))
    R["sections"] = "\n".join(lines) + "\n"
    # derived registry
    lines = ["| id | existing | source | frontier row | statement | runtime location | status | checker | mutant |", "|---|---|---|---|---|---|---|---|---|"]
    for r in model["derived"]:
        lines.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["id"], "yes" if r["existing_row"] else "new", r["gap"], r["frontier_row"] or "—", md_escape(r["statement"]),
            md_escape("; ".join(f"`{x}`" for x in r["runtime_location"])) or "—", r["status"], md_escape(r["checker"] or "—"),
            md_escape(", ".join(f"`{m}`" for m in r["mutant"])) if r["mutant"] else "—"))
    R["derived"] = "\n".join(lines) + "\n"
    # inconsistencies
    lines = ["| # | finding |", "|---|---|"]
    for i, f in enumerate(model["inconsistencies"], 1):
        lines.append(f"| {i} | {md_escape(f)} |")
    R["inconsistencies"] = "\n".join(lines) + "\n"
    # batch-12 slot
    slot = model["batch12_slot"]
    if slot["present"]:
        R["batch12"] = ("Batch 12 (`%s`, sha256 `%s`) is on main; its status block classifies as: %s.\n" % (
            BATCH12_DOC, slot["sha256"][:12], ", ".join(f"{k} {v}" for k, v in sorted(slot["counts"].items()))))
    else:
        R["batch12"] = ("Batch 12 (`%s`, Lean 4 mechanised warrant core, branch `kso/theory-batch-12`) is NOT on main at the commit this "
                        "map was checked; the slot stays PENDING_MERGE and the counts above exclude it.\n" % BATCH12_DOC)
    return R


def emit_derived(model: dict, root: Path = HERE, snapshot: dict | None = None) -> OrderedDict:
    snap = snapshot if snapshot is not None else model["registry"]
    return OrderedDict([
        ("registry", "OCM_OBLIGATION_REGISTRY_DERIVED_V1"),
        ("derived_from", "H/I-items of KSO_FIELD_FRONTIER_THEOREMS_BATCH8..11_V1.md (consequences sections), parsed by kso_field_map_v1_exact.py"),
        ("rule", "ids continue after the highest existing KS-T id of the OCM registries in existing_registry_snapshot; existing rows keep their id; status is OPEN unless the OCM registry already records PROVED with a checker; no novelty claim"),
        ("status_vocabulary", ["PROVED", "OPEN"]),
        ("highest_existing_kst", f"KS-T{model['max_existing_kst']}"),
        ("obligations", model["derived"]),
        ("existing_registry_snapshot", snap),
    ])


def check_document(model: dict, root: Path = HERE) -> list[str]:
    doc_path = root / DOC_NAME
    if not doc_path.exists():
        return [f"DOCUMENT_MISSING {DOC_NAME}"]
    doc = read(doc_path)
    errors = []
    regions = render_regions(model)
    for name, text in regions.items():
        m = re.search(r"<!-- FIELD_MAP_GENERATED:" + name + r" BEGIN -->\n(.*?)<!-- FIELD_MAP_GENERATED:" + name + r" END -->", doc, re.S)
        if not m:
            errors.append(f"DOCUMENT_REGION_MISSING {name}")
        elif m.group(1) != text:
            errors.append(f"DOCUMENT_REGION_STALE {name}")
    derived_path = root / DERIVED_NAME
    if derived_path.exists():
        committed = json.loads(read(derived_path))
        expected = json.loads(json.dumps(emit_derived(model, root)))
        if committed != expected:
            errors.append("DERIVED_REGISTRY_STALE " + DERIVED_NAME)
    else:
        errors.append(f"DERIVED_REGISTRY_MISSING {DERIVED_NAME}")
    return errors


# ----------------------------------------------------------------------------------------------
# planted mutants and no-alarm control


def mutant_duplicate_id(model: dict) -> list[str]:
    m = copy.deepcopy(model)
    m["theorems"].append(copy.deepcopy(m["theorems"][0]))
    return [e for e in check_consistency(m) if e.startswith("DUPLICATE_ID")]


def mutant_unknown_status(model: dict) -> list[str]:
    m = copy.deepcopy(model)
    t = m["theorems"][3]
    t["status_text"], t["status"], t["statuses"] = "SOLVED (finite)", None, []
    return [e for e in check_consistency(m) if e.startswith("UNKNOWN_STATUS")]


def mutant_dangling_kst(model: dict) -> list[str]:
    m = copy.deepcopy(model)
    m["theorems"][5]["cites"]["kst"].append("KS-T999")
    return [e for e in check_consistency(m) if e.startswith("DANGLING_KST KS-T999")]


def mutant_impossibility_without_bound(model: dict) -> list[str]:
    m = copy.deepcopy(model)
    m["impossibilities"].append({"batch": 7, "row": "MEG-99", "sub": None, "bound": "a statement with a witness", "theorem": "G1", "fixture": "", "parent": "", "has_bound": False})
    return [e for e in check_consistency(m) if e.startswith("IMPOSSIBILITY_WITHOUT_BOUND")]


def mutant_conjecture_without_falsifier(model: dict) -> list[str]:
    m = copy.deepcopy(model)
    m["conjectures"].append({"batch": 9, "row": "FDX-99", "theorem": "I4", "text": "x", "kind": "CONJECTURE", "falsifier": None, "falsifier_source": None})
    return [e for e in check_consistency(m) if e.startswith("CONJECTURE_WITHOUT_FALSIFIER")]


def mutant_derived_renumbered(model: dict) -> list[str]:
    m = copy.deepcopy(model)
    for r in m["derived"]:
        if not r["existing_row"]:
            r["id"] = f"KS-T{kst_number(r['id']) + 1}"
    return [e for e in check_consistency(m) if e.startswith("DERIVED_NUMBERING")]


def mutant_stale_document(model: dict, root: Path = HERE) -> list[str]:
    m = copy.deepcopy(model)
    m["theorems"][0]["status"] = "OPEN"
    return [e for e in check_document(m, root) if e.startswith("DOCUMENT_REGION_STALE")]


MUTANTS = (mutant_duplicate_id, mutant_unknown_status, mutant_dangling_kst, mutant_impossibility_without_bound,
           mutant_conjecture_without_falsifier, mutant_derived_renumbered)


def run_all(root: Path = HERE, ocm_root: Path | None = None, check_doc: bool = True) -> dict:
    model = build_model(root, ocm_root)
    errors = check_consistency(model)
    no_alarm = not errors
    caught = {}
    for fn in MUTANTS:
        caught[fn.__name__] = bool(fn(model))
    doc_errors = check_document(model, root) if check_doc else []
    if check_doc and (root / DOC_NAME).exists():
        caught["mutant_stale_document"] = bool(mutant_stale_document(model, root))
    out = OrderedDict([
        ("status", "CONSISTENT" if not errors and not doc_errors and all(caught.values()) else "INCONSISTENT"),
        ("errors", errors), ("document_errors", doc_errors), ("no_alarm_control", no_alarm), ("mutants_caught", caught),
        ("summary", summary_counts(model)),
        ("open_flags", [f"{o['theorem']} {o['row']}: {o['flag']}" for o in model["open_items"] if o.get("flag")]),
        ("inconsistencies", model["inconsistencies"]),
        ("live_registries_compared", sorted(model["live_registries"])),
        ("batch12_slot", model["batch12_slot"]),
    ])
    out["_model"] = model
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", type=Path, default=HERE)
    ap.add_argument("--ocm-root", type=Path, default=None, help="ORION-OCM checkout; compares the snapshot with the live registries")
    ap.add_argument("--no-doc", action="store_true", help="skip the document / derived-registry equality checks")
    ap.add_argument("--render", metavar="REGION", help="print one generated region (summary, theorems, graph, kst, impossibilities, open, sections, derived, batch12) or 'all'")
    ap.add_argument("--emit-derived", type=Path, help="write the derived registry JSON to this path (snapshot taken from --ocm-root when given)")
    ap.add_argument("--splice-doc", action="store_true", help="rewrite the generated regions of the field-map document in place, then exit 0")
    ap.add_argument("--snapshot-from-ocm", action="store_true", help="with --emit-derived: build the snapshot from --ocm-root")
    args = ap.parse_args(argv)
    ocm = args.ocm_root if args.ocm_root else (DEFAULT_OCM_ROOT if DEFAULT_OCM_ROOT.exists() else None)
    try:
        if args.emit_derived:
            snap = None
            if args.snapshot_from_ocm:
                if not ocm:
                    raise CannotCheck("--snapshot-from-ocm needs an OCM checkout")
                snap = live_registries(ocm)
            model = build_model(args.root, ocm, snapshot=snap)
            errors = check_consistency(model)
            args.emit_derived.write_text(json.dumps(emit_derived(model, args.root, snap), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            print(json.dumps({"written": str(args.emit_derived), "rows": len(model["derived"]), "errors": errors}, ensure_ascii=False))
            return 1 if errors else 0
        if args.splice_doc:
            model = build_model(args.root, ocm)
            doc_path = args.root / DOC_NAME
            doc = read(doc_path)
            regions = render_regions(model)
            for name, text in regions.items():
                pat = re.compile(r"(<!-- FIELD_MAP_GENERATED:" + name + r" BEGIN -->\n).*?(<!-- FIELD_MAP_GENERATED:" + name + r" END -->)", re.S)
                if not pat.search(doc):
                    raise CannotCheck(f"document has no region {name}")
                doc = pat.sub(lambda m, t=text: m.group(1) + t + m.group(2), doc, count=1)
            doc_path.write_text(doc, encoding="utf-8")
            print(json.dumps({"spliced": str(doc_path), "regions": list(regions)}))
            return 0
        if args.render:
            model = build_model(args.root, ocm)
            regions = render_regions(model)
            if args.render == "all":
                for k, v in regions.items():
                    print(f"<!-- FIELD_MAP_GENERATED:{k} BEGIN -->\n{v}<!-- FIELD_MAP_GENERATED:{k} END -->\n")
            else:
                print(regions[args.render], end="")
            return 0
        out = run_all(args.root, ocm, check_doc=not args.no_doc)
    except CannotCheck as exc:
        print(json.dumps({"status": "CANNOT_CHECK", "reason": str(exc)}))
        return 2
    model = out.pop("_model")
    print(summary_block(model))
    print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
    return 0 if out["status"] == "CONSISTENT" else 1


if __name__ == "__main__":
    sys.exit(main())

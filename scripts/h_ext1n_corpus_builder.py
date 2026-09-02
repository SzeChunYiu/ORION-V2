#!/usr/bin/env python3
"""H-EXT-1N naturalistic corpus builder (design V1).

Builds evidence sets from a real, lawful, public source (PubMed E-utilities metadata)
in which dependence among supports is DERIVABLE FROM METADATA THE ARMS NEVER SEE: two
records that carry the same ClinicalTrials.gov registration (DataBankList accession
NCT........) report the same underlying trial population and therefore form ONE
support family. The registry id is the private oracle; it is stripped from every
arm-visible field (title, abstract, authors, journal, year, publication types, grant
ids, MeSH major topics) and a programmatic canary asserts the stripping on every task.

Stages (all deterministic given the frozen design + raw cache):
  fetch    esearch/efetch pages -> raw XML cache with per-page sha256 (custody)
  build    parse -> eligibility -> per-topic NCT pools -> seeded set construction
           -> redaction -> canary -> corpus.json (host-only) + CORPUS_FREEZE (committed)
  prepare  corpus.json -> study dirs N1-DEV / N1-EVAL in the P-D suite layout
           (public_tasks.json, private_oracle.json{answers,strata}, FROZEN_SUITE.json,
           requests/<arm>/<task_id>.json) so the FM/FG dispatch()/evaluate() harness
           and scripts/orion_pd_arms.py are reused UNCHANGED.

stdlib only. Grants nothing: no real-corpus dependence-detection claim follows from
building the corpus. Design: research/experiments/h-ext1-naturalistic/H_EXT1N_DESIGN_V1.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import shutil
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "research/experiments/h-ext1-naturalistic/H_EXT1N_DESIGN_V1.json"
ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
ARMS = ("P_D_FULL", "P_D_MINUS_DEPENDENCE", "STRONGEST_ASSURANCE_FEDERATION")
INCONCLUSIVE = "INCONCLUSIVE_INSUFFICIENT_INDEPENDENT_SUPPORT"
NCT_RE = re.compile(r"NCT\s?-?\d{8,}", re.IGNORECASE)  # \d{8,}: live typo "NCT035008353" (9 digits)
# every registry-id shape we know of; all are replaced by the same neutral marker so the
# redaction itself carries no per-record information. No leading word boundary: live
# records glue the id to the preceding word ("identifierNCT00445770", verified 2026-09-02).
REGISTRY_RES = [
    NCT_RE,
    re.compile(r"ISRCTN\s?-?\d{6,}", re.IGNORECASE),
    re.compile(r"(?<!\d)\d{4}-\d{6}-\d{2}(?:-\d{2})?(?!\d)"),         # EudraCT / EU CT
    re.compile(r"ChiCTR-?[A-Z]*-?\d{6,12}(?!\d)", re.IGNORECASE),
    re.compile(r"ACTRN\s?\d{14}[a-z]?(?![A-Za-z0-9])", re.IGNORECASE),
    re.compile(r"UMIN\s?-?\d{9}(?!\d)", re.IGNORECASE),
    re.compile(r"DRKS\s?\d{8}(?!\d)", re.IGNORECASE),
    re.compile(r"CTRI/\d{4}/\d{2}/\d{6}(?!\d)", re.IGNORECASE),
    re.compile(r"\bNTR\s?\d{3,5}(?!\d)"),
    re.compile(r"\bNL\s?\d{4,5}(?!\d)"),
    re.compile(r"JPRN-[A-Za-z0-9]+\b"),
    re.compile(r"jRCT[a-z]?\d{9,10}(?!\d)", re.IGNORECASE),
    re.compile(r"\bKCT\s?\d{7}(?!\d)"),
    re.compile(r"IRCT\s?\d{8,20}N?\d*(?![A-Za-z0-9])", re.IGNORECASE),
    re.compile(r"PACTR\s?\d{15,16}(?!\d)", re.IGNORECASE),
    re.compile(r"CRD42\d{7}(?!\d)"),                                  # PROSPERO
    re.compile(r"TCTR\s?\d{11}(?!\d)", re.IGNORECASE),
    re.compile(r"RBR-[a-z0-9]{6,8}\b", re.IGNORECASE),
    re.compile(r"SLCTR/\d{4}/\d{3}(?!\d)", re.IGNORECASE),
    re.compile(r"EUCTR\d{4}-\d{6}-\d{2}-[A-Z]{2}\b"),
    re.compile(r"PMID:?\s?\d{6,9}(?!\d)", re.IGNORECASE),
    re.compile(r"\b10\.\d{4,9}/[^\s,;)]+", re.IGNORECASE),            # DOI
]
REDACTION_MARK = "[REGISTRY-ID]"
REGISTRATION_LABEL_RE = re.compile(r"REGIST|CLINICALTRIALS|TRIAL REG", re.IGNORECASE)
EXCLUDED_PUBTYPES = {
    "review", "systematic review", "meta-analysis", "editorial", "letter", "comment",
    "published erratum", "retracted publication", "retraction of publication", "retraction notice",
    "case reports", "news", "practice guideline", "guideline", "consensus development conference",
    "clinical trial protocol", "study protocol", "observational study, veterinary",
}
FORBIDDEN_TASK_KEYS = {"strata", "stratum", "answers", "expected", "answer", "correct", "actual",
                       "private_oracle", "oracle", "pmid", "doi", "nct", "ncts", "registry_ids",
                       "accession", "accessions", "databank", "affiliations"}
STRATA = {
    # stratum: (n_records, [family sizes]) -> families = len(sizes)
    "NS1A": (3, [2, 1]),
    "NS1B": (3, [1, 1, 1]),
    "NS1C": (4, [2, 2]),
    "NS1D": (4, [1, 1, 1, 1]),
}
DEPENDENT_STRATA = {"NS1A", "NS1C"}


class CorpusError(RuntimeError):
    pass


# ---------------------------------------------------------------------------
# io + custody
# ---------------------------------------------------------------------------

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canon_sha(value: Any) -> str:
    return sha256_bytes(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# ---------------------------------------------------------------------------
# fetch (lawful, rate-gated, cached with per-page hashes)
# ---------------------------------------------------------------------------

class Fetcher:
    def __init__(self, min_interval: float, cache_dir: Path, transport=None, sleep=time.sleep) -> None:
        self.min_interval = min_interval
        self.cache_dir = cache_dir
        self.transport = transport or self._urllib
        self.sleep = sleep
        self._last = float("-inf")
        self.manifest: list[dict[str, Any]] = []

    @staticmethod
    def _urllib(url: str) -> bytes:
        req = urllib.request.Request(url, headers={"User-Agent": "ORION-V2 H-EXT-1N corpus builder (research; stdlib urllib)"})
        with urllib.request.urlopen(req, timeout=90) as raw:
            return raw.read()

    def get(self, url: str, cache_name: str) -> bytes:
        path = self.cache_dir / cache_name
        if path.exists():
            data = path.read_bytes()
            self.manifest.append({"cache": cache_name, "sha256": sha256_bytes(data), "bytes": len(data), "from_cache": True})
            return data
        last_err: Exception | None = None
        for attempt in range(6):
            wait = self._last + self.min_interval - time.monotonic()
            if wait > 0:
                self.sleep(wait)
            self._last = time.monotonic()
            try:
                data = self.transport(url)
                break
            except Exception as exc:  # 429/5xx/transport: capped backoff, then fail closed
                last_err = exc
                self.sleep(min(60.0, 2.0 ** attempt))
        else:
            raise CorpusError(f"fetch failed after retries: {url}: {last_err}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        self.manifest.append({"cache": cache_name, "sha256": sha256_bytes(data), "bytes": len(data), "from_cache": False})
        return data


def build_query(topic: str, design: dict[str, Any]) -> str:
    q = design["corpus"]["query_template"]
    return q.replace("{topic}", topic)


def esearch_ids(fetcher: Fetcher, topic: str, design: dict[str, Any]) -> list[str]:
    term = build_query(topic, design)
    params = {"db": "pubmed", "term": term, "retmode": "json", "retmax": int(design["corpus"]["esearch_retmax"])}
    if os.environ.get("NCBI_API_KEY"):
        params["api_key"] = os.environ["NCBI_API_KEY"]
    url = ESEARCH + "?" + urllib.parse.urlencode(params)
    payload = json.loads(fetcher.get(url, f"{slug(topic)}/esearch.json"))
    result = payload.get("esearchresult", {})
    if result.get("ERROR") or result.get("errorlist"):
        raise CorpusError(f"esearch error for {topic}: {result.get('ERROR') or result.get('errorlist')}")
    ids = [str(i) for i in result.get("idlist", [])]
    count = int(result.get("count", 0))
    if count > len(ids):
        # frozen ceiling: the design's retmax bounds the per-topic pool; record truncation
        fetcher.manifest.append({"topic": topic, "esearch_count": count, "retrieved": len(ids), "truncated": True})
    return ids


def efetch_pages(fetcher: Fetcher, topic: str, ids: list[str], page: int) -> list[bytes]:
    pages = []
    for i in range(0, len(ids), page):
        chunk = ids[i:i + page]
        params = {"db": "pubmed", "id": ",".join(chunk), "retmode": "xml"}
        if os.environ.get("NCBI_API_KEY"):
            params["api_key"] = os.environ["NCBI_API_KEY"]
        url = EFETCH + "?" + urllib.parse.urlencode(params)
        pages.append(fetcher.get(url, f"{slug(topic)}/efetch_{i // page:04d}.xml"))
    return pages


# ---------------------------------------------------------------------------
# parse
# ---------------------------------------------------------------------------

def _text(node: ET.Element | None) -> str:
    if node is None:
        return ""
    return "".join(node.itertext()).strip()


def parse_articles(xml_bytes: bytes) -> list[dict[str, Any]]:
    root = ET.fromstring(xml_bytes)
    out = []
    for article in root.findall("PubmedArticle"):
        med = article.find("MedlineCitation")
        if med is None:
            continue
        art = med.find("Article")
        if art is None:
            continue
        pmid = (med.findtext("PMID") or "").strip()
        ncts: set[str] = set()
        other_registry = False
        for db in art.findall("DataBankList/DataBank"):
            name = (db.findtext("DataBankName") or "").strip().lower()
            for acc in db.findall("AccessionNumberList/AccessionNumber"):
                val = (acc.text or "").strip().upper()
                if name == "clinicaltrials.gov" and re.fullmatch(r"NCT\d{8}", val):
                    ncts.add(val)
                elif name in {"isrctn", "eudract", "chictr", "anzctr", "umin-ctr", "drks", "ctri", "ntr", "jprn", "irct", "pactr", "kct", "tctr", "rebec", "eu-ctr"}:
                    other_registry = True
        authors = []
        for a in art.findall("AuthorList/Author"):
            coll = (a.findtext("CollectiveName") or "").strip()
            last = (a.findtext("LastName") or "").strip()
            init = (a.findtext("Initials") or "").strip()
            if coll:
                authors.append(coll)
            elif last:
                authors.append((last + " " + init).strip())
        sections = []
        for sec in art.findall("Abstract/AbstractText"):
            sections.append(((sec.get("Label") or sec.get("NlmCategory") or "").strip(), _text(sec)))
        grants = sorted({(g.findtext("GrantID") or "").strip().upper() for g in art.findall("GrantList/Grant")
                         if (g.findtext("GrantID") or "").strip() and (g.findtext("GrantID") or "").strip().lower() != "no number"})
        out.append({
            "pmid": pmid,
            "title": _text(art.find("ArticleTitle")),
            "abstract_sections": sections,
            "authors": authors,
            "journal": (art.findtext("Journal/Title") or med.findtext("MedlineJournalInfo/MedlineTA") or "").strip(),
            "year": _year(med),
            "pubtypes": [(_p.text or "").strip() for _p in art.findall("PublicationTypeList/PublicationType")],
            "language": (art.findtext("Language") or "").strip().lower(),
            "ncts": sorted(ncts),
            "other_registry": other_registry,
            "grant_ids": grants,
            "doi": next(((e.text or "").strip() for e in art.findall("ELocationID") if e.get("EIdType") == "doi"), ""),
            "mesh_major": [(d.text or "").strip() for d in med.findall("MeshHeadingList/MeshHeading/DescriptorName") if d.get("MajorTopicYN") == "Y"],
        })
    return out


def _year(med: ET.Element) -> str:
    for path in ("Article/ArticleDate/Year", "Article/Journal/JournalIssue/PubDate/Year", "Article/Journal/JournalIssue/PubDate/MedlineDate"):
        t = (med.findtext(path) or "").strip()
        if t[:4].isdigit():
            return t[:4]
    return ""


# ---------------------------------------------------------------------------
# eligibility, redaction, visible record
# ---------------------------------------------------------------------------

def abstract_text(rec: dict[str, Any]) -> str:
    parts = []
    for label, text in rec["abstract_sections"]:
        if label and REGISTRATION_LABEL_RE.search(label):
            continue  # whole registration section dropped (it names the oracle id)
        parts.append(text)
    return " ".join(p for p in parts if p).strip()


def redact(text: str) -> str:
    out = text
    for rx in REGISTRY_RES:
        out = rx.sub(REDACTION_MARK, out)
    return out


def eligible(rec: dict[str, Any], design: dict[str, Any]) -> tuple[bool, str]:
    c = design["corpus"]
    if len(rec["ncts"]) != 1:
        return False, "not_exactly_one_nct"
    if rec["other_registry"]:
        return False, "other_registry_present"
    if rec["language"] and rec["language"] != "eng":
        return False, "not_english"
    if {p.lower() for p in rec["pubtypes"]} & EXCLUDED_PUBTYPES:
        return False, "excluded_pubtype"
    if len(abstract_text(rec)) < int(c["min_abstract_chars"]):
        return False, "short_abstract"
    if len(rec["authors"]) < 1 or not rec["title"]:
        return False, "missing_authors_or_title"
    return True, "ok"


def _redact_list(values: list[str]) -> list[str]:
    """Redact every string; drop entries that were nothing but a registry id (live
    GrantList entries such as "NCT02998970" or "CLINICALTRIALS.GOV NCT02545049")."""
    out = []
    for v in values:
        r = redact(str(v)).strip()
        if r and r.replace(REDACTION_MARK, "").strip(" .:;,-/()") not in ("", "CLINICALTRIALS.GOV", "clinicaltrials.gov", "ClinicalTrials.gov"):
            out.append(r)
    return out


def visible_record(rec: dict[str, Any], record_id: str) -> dict[str, Any]:
    """Every string field passes through redact(); no field is exempt."""
    return {
        "record_id": record_id,
        "title": redact(rec["title"]),
        "abstract": redact(abstract_text(rec)),
        "authors": _redact_list(rec["authors"]),
        "journal": redact(rec["journal"]),
        "year": rec["year"],
        "publication_types": _redact_list(rec["pubtypes"]),
        "grant_ids": _redact_list(rec["grant_ids"]),
        "mesh_major": _redact_list(rec["mesh_major"]),
    }


def title_tokens(title: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", title.lower()) if len(t) > 2}


def near_duplicate(a: dict[str, Any], b: dict[str, Any], threshold: float) -> bool:
    ta, tb = title_tokens(a["title"]), title_tokens(b["title"])
    if not ta or not tb:
        return False
    return len(ta & tb) / len(ta | tb) >= threshold


# ---------------------------------------------------------------------------
# canary: the oracle must be absent from every arm-visible byte
# ---------------------------------------------------------------------------

def _walk_keys(value: Any, found: set[str]) -> None:
    if isinstance(value, dict):
        for k, v in value.items():
            found.add(str(k))
            _walk_keys(v, found)
    elif isinstance(value, list):
        for v in value:
            _walk_keys(v, found)


def assert_no_oracle_leak(public_task: dict[str, Any], oracle: dict[str, Any]) -> None:
    blob = json.dumps(public_task, sort_keys=True, ensure_ascii=False)
    keys: set[str] = set()
    _walk_keys(public_task, keys)
    bad_keys = sorted(k for k in keys if k.lower() in FORBIDDEN_TASK_KEYS)
    if bad_keys:
        raise CorpusError(f"canary: forbidden keys {bad_keys} in task {public_task.get('task_id')}")
    for nct in oracle["ncts_by_record"].values():
        if nct in blob.upper():
            raise CorpusError(f"canary: oracle registry id {nct} visible in task {public_task.get('task_id')}")
    for pmid in oracle["pmids_by_record"].values():
        if re.search(r"\b" + re.escape(pmid) + r"\b", blob):
            raise CorpusError(f"canary: pmid {pmid} visible in task {public_task.get('task_id')}")
    for doi in oracle.get("dois_by_record", {}).values():
        if doi and doi.lower() in blob.lower():
            raise CorpusError(f"canary: doi visible in task {public_task.get('task_id')}")
    for rx in REGISTRY_RES:
        m = rx.search(blob)
        if m:
            raise CorpusError(f"canary: registry-shaped token {m.group(0)!r} survived redaction in {public_task.get('task_id')}")


# ---------------------------------------------------------------------------
# set construction (seeded, quota-driven, every NCT and PMID used at most once)
# ---------------------------------------------------------------------------

def nct_pools(records: list[dict[str, Any]], design: dict[str, Any]) -> dict[str, dict[str, list[dict[str, Any]]]]:
    """topic -> nct -> eligible records (sorted by pmid), restricted to NCTs with >=2 records
    that are not near-duplicates of each other (title Jaccard < threshold)."""
    thr = float(design["corpus"]["near_duplicate_title_jaccard"])
    by_topic: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for rec in records:
        by_topic.setdefault(rec["topic"], {}).setdefault(rec["ncts"][0], []).append(rec)
    pools: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for topic, ncts in by_topic.items():
        for nct, recs in ncts.items():
            recs = sorted(recs, key=lambda r: r["pmid"])
            kept: list[dict[str, Any]] = []
            for r in recs:
                if any(near_duplicate(r, k, thr) for k in kept):
                    continue
                kept.append(r)
            if len(kept) >= 2:
                pools.setdefault(topic, {})[nct] = kept
    return pools


def allocate_quota(pools: dict[str, dict[str, Any]], per_stratum: int, ncts_per_cycle: int) -> dict[str, int]:
    """Cycles (one set of each stratum) per topic, proportional to the topic's multi-pub NCT
    count, largest remainder, capped by what the topic can supply."""
    total_cycles = per_stratum
    sizes = {t: len(v) for t, v in pools.items()}
    grand = sum(sizes.values())
    if grand == 0:
        return {t: 0 for t in pools}
    raw = {t: total_cycles * sizes[t] / grand for t in pools}
    base = {t: int(raw[t]) for t in pools}
    rem = total_cycles - sum(base.values())
    for t in sorted(pools, key=lambda t: (-(raw[t] - base[t]), t)):
        if rem <= 0:
            break
        base[t] += 1
        rem -= 1
    return {t: min(base[t], sizes[t] // ncts_per_cycle) for t in pools}


def build_sets(records: list[dict[str, Any]], design: dict[str, Any], seed: int) -> dict[str, Any]:
    c = design["corpus"]
    per_stratum = int(c["sets_per_stratum"])
    pools = nct_pools(records, design)
    ncts_per_cycle = sum(len(sizes) for _n, sizes in STRATA.values())  # 2+3+2+4 = 11
    quota = allocate_quota(pools, per_stratum, ncts_per_cycle)
    rng = random.Random(seed)
    sets: list[dict[str, Any]] = []
    used_pmids: set[str] = set()
    per_topic_counts: dict[str, dict[str, int]] = {}
    for topic in sorted(pools):
        ncts = sorted(pools[topic])
        rng.shuffle(ncts)
        it = iter(ncts)
        for _cycle in range(quota[topic]):
            for stratum in ("NS1A", "NS1B", "NS1C", "NS1D"):
                n_records, family_sizes = STRATA[stratum]
                members: list[tuple[str, dict[str, Any]]] = []
                for fam_size in family_sizes:
                    try:
                        nct = next(it)
                    except StopIteration:
                        raise CorpusError("quota exceeded pool; allocate_quota bug")
                    recs = [r for r in pools[topic][nct] if r["pmid"] not in used_pmids]
                    if len(recs) < fam_size:
                        raise CorpusError(f"nct {nct} lacks {fam_size} unused records")
                    chosen = rng.sample(recs, fam_size)
                    for r in chosen:
                        used_pmids.add(r["pmid"])
                        members.append((nct, r))
                rng.shuffle(members)
                sets.append({
                    "topic": topic,
                    "stratum": stratum,
                    "members": members,
                })
                per_topic_counts.setdefault(topic, {}).setdefault(stratum, 0)
                per_topic_counts[topic][stratum] += 1
    return {"sets": sets, "quota_cycles": quota, "per_topic_counts": per_topic_counts,
            "pool_sizes": {t: len(v) for t, v in pools.items()}}


def assign_ids_and_split(sets: list[dict[str, Any]], design: dict[str, Any], seed: int) -> None:
    """Neutral task ids in a seeded shuffle (id never encodes stratum/topic/split) and a
    stratified DEV/EVAL split (dev fraction frozen in the design)."""
    rng = random.Random(seed + 1)
    ids = [f"n1-{i + 1:04d}" for i in range(len(sets))]
    rng.shuffle(ids)
    for s, tid in zip(sets, ids):
        s["task_id"] = tid
    dev_frac = float(design["splits"]["dev_fraction"])
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for s in sets:
        groups.setdefault((s["topic"], s["stratum"]), []).append(s)
    for key in sorted(groups):
        members = sorted(groups[key], key=lambda s: s["task_id"])
        k = int(round(dev_frac * len(members)))
        dev_ids = set(rng.sample([m["task_id"] for m in members], k))
        for m in members:
            m["split"] = "DEV" if m["task_id"] in dev_ids else "EVAL"


def public_and_oracle(s: dict[str, Any], design: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    records = []
    ncts_by_record, pmids_by_record, dois_by_record = {}, {}, {}
    for i, (nct, rec) in enumerate(s["members"]):
        rid = f"r{i + 1}"
        records.append(visible_record(rec, rid))
        ncts_by_record[rid] = nct
        pmids_by_record[rid] = rec["pmid"]
        dois_by_record[rid] = rec["doi"]
    families = len(set(ncts_by_record.values()))
    decision = "ACCEPT_H" if families >= int(design["decision_rule"]["accept_min_families"]) else INCONCLUSIVE
    hyp = "H_" + hashlib.sha256(s["task_id"].encode()).hexdigest()[:6].upper()
    public = {
        "task_id": s["task_id"],
        "study_id": "N1",
        "hypothesis": hyp,
        "topic": s["topic"],
        "records": records,
        "registered_decision_rule": design["decision_rule"]["text"],
        "task": design["decision_rule"]["task_text"],
        "answer_contract": {"decision": "string", "independent_support_family_count": "number"},
    }
    oracle = {
        "answer": {"decision": decision, "independent_support_family_count": families},
        "stratum": s["stratum"],
        "ncts_by_record": ncts_by_record,
        "pmids_by_record": pmids_by_record,
        "dois_by_record": dois_by_record,
        "split": s["split"],
    }
    return public, oracle


def corpus_freeze(tasks: list[dict[str, Any]], oracles: dict[str, Any], build: dict[str, Any], design_path: Path,
                  fetch_manifest: list[dict[str, Any]], seed: int, host: str) -> dict[str, Any]:
    by_stratum: dict[str, int] = {}
    by_split: dict[str, dict[str, int]] = {}
    for t in tasks:
        o = oracles[t["task_id"]]
        by_stratum[o["stratum"]] = by_stratum.get(o["stratum"], 0) + 1
        by_split.setdefault(o["split"], {}).setdefault(o["stratum"], 0)
        by_split[o["split"]][o["stratum"]] += 1
    n_dep = sum(v for k, v in by_stratum.items() if k in DEPENDENT_STRATA)
    n_ind = sum(v for k, v in by_stratum.items() if k not in DEPENDENT_STRATA)
    return {
        "schema_version": "orion.v2.h-ext1n-corpus-freeze.v1",
        "design_sha256": sha256_path(design_path),
        "seed": seed,
        "host": host,
        "source": "PubMed E-utilities (esearch/efetch db=pubmed, retmode=xml); oracle = ClinicalTrials.gov accession in DataBankList",
        "n_sets": len(tasks),
        "n_dependent": n_dep,
        "n_independent": n_ind,
        "by_stratum": by_stratum,
        "by_split": by_split,
        "pool_sizes_multi_pub_ncts": build["pool_sizes"],
        "quota_cycles": build["quota_cycles"],
        "per_topic_counts": build["per_topic_counts"],
        "public_tasks_sha256": canon_sha(tasks),
        "oracle_sha256": canon_sha(oracles),
        "record_sha256": {t["task_id"]: {r["record_id"]: canon_sha(r) for r in t["records"]} for t in tasks},
        "pmids": {t["task_id"]: oracles[t["task_id"]]["pmids_by_record"] for t in tasks},
        "fetch_manifest_sha256": canon_sha(fetch_manifest),
        "fetch_pages": len([m for m in fetch_manifest if "cache" in m]),
        "authority": {"grants_scientific_truth": False, "grants_real_corpus_dependence_detection": False},
    }


def adequacy(freeze: dict[str, Any], design: dict[str, Any]) -> dict[str, Any]:
    a = design["corpus_adequacy"]
    n = freeze["n_sets"]
    imbalance = abs(freeze["n_dependent"] - freeze["n_independent"]) / n if n else 1.0
    checks = {
        "min_sets": {"pass": n >= int(a["min_sets"]), "n": n, "min": int(a["min_sets"])},
        "balance": {"pass": imbalance <= float(a["max_label_imbalance"]), "imbalance": imbalance},
        "min_per_stratum": {"pass": all(freeze["by_stratum"].get(s, 0) >= int(a["min_per_stratum"]) for s in STRATA),
                            "by_stratum": freeze["by_stratum"]},
        "min_topics": {"pass": sum(1 for v in freeze["per_topic_counts"].values() if sum(v.values()) > 0) >= int(a["min_topics"]),
                       "topics": sorted(freeze["per_topic_counts"])},
    }
    return {"pass": all(v["pass"] for v in checks.values()), "checks": checks,
            "terminal_if_fail": "CORPUS_ANNOTATION_INSUFFICIENT"}


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def cmd_fetch(design: dict[str, Any], workdir: Path, transport=None, sleep=time.sleep) -> dict[str, Any]:
    c = design["corpus"]
    fetcher = Fetcher(float(c["min_request_interval_seconds"]), workdir / "raw", transport, sleep)
    raw_records: list[dict[str, Any]] = []
    per_topic = {}
    for topic in c["topics"]:
        ids = esearch_ids(fetcher, topic, design)
        pages = efetch_pages(fetcher, topic, ids, int(c["efetch_page_size"]))
        n = 0
        for page in pages:
            for rec in parse_articles(page):
                rec["topic"] = topic
                raw_records.append(rec)
                n += 1
        per_topic[topic] = {"esearch_ids": len(ids), "parsed": n}
    write_json(workdir / "raw_records.json", raw_records)
    write_json(workdir / "FETCH_MANIFEST.json", {"schema_version": "orion.v2.h-ext1n-fetch-manifest.v1",
                                                  "per_topic": per_topic, "pages": fetcher.manifest})
    return {"records": len(raw_records), "per_topic": per_topic}


def cmd_build(design: dict[str, Any], design_path: Path, workdir: Path, seed: int, host: str) -> dict[str, Any]:
    raw = read_json(workdir / "raw_records.json")
    manifest = read_json(workdir / "FETCH_MANIFEST.json")["pages"]
    elig, reasons = [], {}
    seen: set[str] = set()
    for rec in raw:
        if rec["pmid"] in seen:
            reasons["duplicate_pmid_across_topics"] = reasons.get("duplicate_pmid_across_topics", 0) + 1
            continue
        ok, why = eligible(rec, design)
        reasons[why] = reasons.get(why, 0) + 1
        if ok:
            seen.add(rec["pmid"])
            elig.append(rec)
    build = build_sets(elig, design, seed)
    assign_ids_and_split(build["sets"], design, seed)
    tasks, oracles = [], {}
    for s in build["sets"]:
        public, oracle = public_and_oracle(s, design)
        assert_no_oracle_leak(public, oracle)
        tasks.append(public)
        oracles[public["task_id"]] = oracle
    tasks.sort(key=lambda t: t["task_id"])
    freeze = corpus_freeze(tasks, oracles, build, design_path, manifest, seed, host)
    freeze["eligibility_reasons"] = reasons
    freeze["n_raw_records"] = len(raw)
    freeze["n_eligible_records"] = len(elig)
    freeze["adequacy"] = adequacy(freeze, design)
    write_json(workdir / "corpus_public_tasks.json", {"schema_version": "orion.v2.h-ext1n-corpus-public.v1", "tasks": tasks})
    write_json(workdir / "corpus_private_oracle.json", {"schema_version": "orion.v2.h-ext1n-corpus-private.v1", "oracles": oracles})
    write_json(workdir / "H_EXT1N_CORPUS_FREEZE.json", freeze)
    return freeze


def cmd_prepare(design: dict[str, Any], workdir: Path, campaign_root: Path, force: bool) -> dict[str, Any]:
    tasks = read_json(workdir / "corpus_public_tasks.json")["tasks"]
    oracles = read_json(workdir / "corpus_private_oracle.json")["oracles"]
    freeze = read_json(workdir / "H_EXT1N_CORPUS_FREEZE.json")
    if canon_sha(tasks) != freeze["public_tasks_sha256"] or canon_sha(oracles) != freeze["oracle_sha256"]:
        raise CorpusError("corpus files do not match H_EXT1N_CORPUS_FREEZE.json")
    out = {}
    for split in ("DEV", "EVAL"):
        study = f"N1-{split}"
        sdir = campaign_root / study
        if sdir.exists():
            if not force:
                raise CorpusError(f"exists: {sdir}")
            shutil.rmtree(sdir)
        split_tasks = [t for t in tasks if oracles[t["task_id"]]["split"] == split]
        answers = {t["task_id"]: oracles[t["task_id"]]["answer"] for t in split_tasks}
        strata = {t["task_id"]: oracles[t["task_id"]]["stratum"] for t in split_tasks}
        for t in split_tasks:
            assert_no_oracle_leak(t, oracles[t["task_id"]])
            for arm in ARMS:
                write_json(sdir / "requests" / arm / f"{t['task_id']}.json", {
                    "schema_version": "orion.v2.dependence-evidence-request.v1",
                    "task_id": t["task_id"], "arm_id": arm, "task": t,
                    "scientific_truth_authorized": False, "legitimate_authority_authorized": False,
                    "publication_readiness_authorized": False,
                })
        write_json(sdir / "public_tasks.json", {"schema_version": "orion.v2.dependence-evidence-public.v1", "tasks": split_tasks})
        write_json(sdir / "private_oracle.json", {"schema_version": "orion.v2.dependence-evidence-private.v1",
                                                  "answers": answers, "strata": strata})
        counts: dict[str, int] = {}
        for s in strata.values():
            counts[s] = counts.get(s, 0) + 1
        write_json(sdir / "FROZEN_SUITE.json", {
            "schema_version": "orion.v2.dependence-evidence-freeze.v1",
            "seed": int(freeze["seed"]), "study_id": study, "split": split, "strata": counts,
            "task_count": len(split_tasks), "arms": list(ARMS),
            "corpus_freeze_sha256": sha256_path(workdir / "H_EXT1N_CORPUS_FREEZE.json"),
            "private_oracle_visible_to_solver": False, "strata_visible_in_public_tasks": False,
            "authority": {"grants_scientific_truth": False, "grants_dependence_detection_in_real_corpora": False},
        })
        out[study] = {"tasks": len(split_tasks), "strata": counts}
    write_json(campaign_root / "CAMPAIGN_FREEZE_MANIFEST.json", {
        "schema_version": "orion.v2.h-ext1n-campaign-freeze.v1",
        "corpus_freeze_sha256": sha256_path(workdir / "H_EXT1N_CORPUS_FREEZE.json"),
        "pd_arms_sha256": sha256_path(ROOT / "scripts/orion_pd_arms.py") if (ROOT / "scripts/orion_pd_arms.py").exists() else None,
        "studies": out,
    })
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    p.add_argument("--workdir", type=Path, required=True)
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("fetch")
    b = sub.add_parser("build")
    b.add_argument("--seed", type=int, default=None)
    b.add_argument("--host", default=os.uname().nodename)
    pr = sub.add_parser("prepare")
    pr.add_argument("--campaign-root", type=Path, required=True)
    pr.add_argument("--force", action="store_true")
    args = p.parse_args(argv)
    design = read_json(args.design)
    if args.command == "fetch":
        print(json.dumps(cmd_fetch(design, args.workdir)))
        return 0
    if args.command == "build":
        seed = args.seed if args.seed is not None else int(design["corpus"]["seed"])
        freeze = cmd_build(design, args.design, args.workdir, seed, args.host)
        print(json.dumps({"n_sets": freeze["n_sets"], "by_stratum": freeze["by_stratum"], "adequacy": freeze["adequacy"]["pass"]}))
        return 0 if freeze["adequacy"]["pass"] else 5
    print(json.dumps(cmd_prepare(design, args.workdir, args.campaign_root, args.force)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

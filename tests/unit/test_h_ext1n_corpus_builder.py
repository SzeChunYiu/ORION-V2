from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "h_ext1n_corpus_builder.py"
SPEC = importlib.util.spec_from_file_location("h_ext1n_corpus_builder", SCRIPT)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

DESIGN_PATH = ROOT / "research/experiments/h-ext1-naturalistic/H_EXT1N_DESIGN_V1.json"
DESIGN = json.loads(DESIGN_PATH.read_text())


def _article(pmid: str, nct: str, title: str, authors: list[str], grant: str = "", pubtype: str = "Randomized Controlled Trial",
             extra_section: str = "") -> str:
    auth = "".join(f"<Author><LastName>{a.split()[0]}</LastName><Initials>{a.split()[1]}</Initials></Author>" for a in authors)
    body = " ".join(["Participants were randomized to intervention or control and followed for outcomes."] * 12)
    return f"""<PubmedArticle><MedlineCitation><PMID>{pmid}</PMID>
<Article><ArticleTitle>{title}</ArticleTitle>
<Journal><Title>Journal of Trials</Title><JournalIssue><PubDate><Year>2020</Year></PubDate></JournalIssue></Journal>
<Abstract><AbstractText Label="BACKGROUND">{body}</AbstractText>
<AbstractText Label="RESULTS">{body} {extra_section}</AbstractText>
<AbstractText Label="TRIAL REGISTRATION">ClinicalTrials.gov {nct}</AbstractText></Abstract>
<AuthorList>{auth}</AuthorList><Language>eng</Language>
<GrantList><Grant><GrantID>{grant or 'no number'}</GrantID></Grant></GrantList>
<PublicationTypeList><PublicationType>Journal Article</PublicationType><PublicationType>{pubtype}</PublicationType></PublicationTypeList>
<DataBankList><DataBank><DataBankName>ClinicalTrials.gov</DataBankName><AccessionNumberList><AccessionNumber>{nct}</AccessionNumber></AccessionNumberList></DataBank></DataBankList>
<ELocationID EIdType="doi">10.1000/{pmid}</ELocationID></Article>
<MeshHeadingList><MeshHeading><DescriptorName MajorTopicYN="Y">Hypertension</DescriptorName></MeshHeading></MeshHeadingList>
</MedlineCitation></PubmedArticle>"""


def _corpus_xml(n_ncts: int, pubs_per_nct: int, prefix: str) -> str:
    arts = []
    k = 0
    for i in range(n_ncts):
        nct = f"NCT{prefix}{i:06d}"
        for j in range(pubs_per_nct):
            k += 1
            title = (f"Efficacy of intervention {prefix}{i} on the primary endpoint {k}" if j % 2 == 0
                     else f"Secondary analysis: quality of life and safety in study {prefix}{i} cohort {k}")
            arts.append(_article(f"{prefix}{k:06d}", nct, title,
                                 [f"Alpha{i} A", f"Beta{i} B", f"Omega{i} Z"],
                                 extra_section=f"Registered as {nct} (doi 10.1000/{prefix}{k:06d})."))
    return "<PubmedArticleSet>" + "".join(arts) + "</PubmedArticleSet>"


def test_parse_and_redaction_strip_registry_ids() -> None:
    recs = mod.parse_articles(_corpus_xml(1, 1, "11").encode())
    assert len(recs) == 1 and recs[0]["ncts"] == ["NCT11000000"]
    vis = mod.visible_record(recs[0], "r1")
    assert "NCT" not in vis["abstract"] and "[REGISTRY-ID]" in vis["abstract"]
    assert "10.1000" not in vis["abstract"]
    assert "TRIAL REGISTRATION" not in vis["abstract"]
    assert set(vis) == set(DESIGN["corpus"]["arm_visible_record_fields"])


def test_redaction_without_leading_word_boundary() -> None:
    assert "NCT" not in mod.redact("ClinicalTrials.gov identifierNCT00445770.")
    assert "NCT" not in mod.redact("registered (NCT 01234567) and ISRCTN12345678; EudraCT 2015-001234-56")
    assert mod.redact("The ONCT trial") == "The ONCT trial"


def test_eligibility_rules() -> None:
    recs = mod.parse_articles(_corpus_xml(1, 1, "12").encode())
    assert mod.eligible(recs[0], DESIGN) == (True, "ok")
    bad = dict(recs[0], ncts=["NCT1", "NCT2"])
    assert mod.eligible(bad, DESIGN)[1] == "not_exactly_one_nct"
    bad = dict(recs[0], pubtypes=["Review"])
    assert mod.eligible(bad, DESIGN)[1] == "excluded_pubtype"
    bad = dict(recs[0], abstract_sections=[("", "short")])
    assert mod.eligible(bad, DESIGN)[1] == "short_abstract"


def _build(tmp_path: Path, design: dict) -> dict:
    xml = _corpus_xml(24, 2, "31")
    raw = [dict(r, topic="hypertension") for r in mod.parse_articles(xml.encode())]
    tmp_path.mkdir(parents=True, exist_ok=True)
    dpath = tmp_path / "design.json"
    dpath.write_text(json.dumps(design))
    work = tmp_path / "work"
    work.mkdir()
    mod.write_json(work / "raw_records.json", raw)
    mod.write_json(work / "FETCH_MANIFEST.json", {"pages": [{"cache": "x", "sha256": "0" * 64, "bytes": 1}]})
    return mod.cmd_build(design, dpath, work, seed=7, host="test")


def test_build_sets_balanced_and_canary_and_prepare(tmp_path: Path) -> None:
    design = json.loads(json.dumps(DESIGN))
    design["corpus"]["sets_per_stratum"] = 2
    design["corpus_adequacy"] = {"min_sets": 8, "min_per_stratum": 2, "max_label_imbalance": 0.1, "min_topics": 1}
    freeze = _build(tmp_path, design)
    assert freeze["n_sets"] == 8 and freeze["by_stratum"] == {"NS1A": 2, "NS1B": 2, "NS1C": 2, "NS1D": 2}
    assert freeze["n_dependent"] == freeze["n_independent"] == 4
    assert freeze["adequacy"]["pass"] is True
    work = tmp_path / "work"
    tasks = mod.read_json(work / "corpus_public_tasks.json")["tasks"]
    oracles = mod.read_json(work / "corpus_private_oracle.json")["oracles"]
    # oracle semantics: families = distinct NCTs; every NCT/PMID used once
    seen_nct, seen_pmid = set(), set()
    for t in tasks:
        o = oracles[t["task_id"]]
        fam = len(set(o["ncts_by_record"].values()))
        assert o["answer"]["independent_support_family_count"] == fam
        assert o["answer"]["decision"] == ("ACCEPT_H" if fam >= 3 else mod.INCONCLUSIVE)
        assert (o["stratum"] in mod.DEPENDENT_STRATA) == (fam < len(t["records"]))
        for nct in set(o["ncts_by_record"].values()):
            assert nct not in seen_nct
            seen_nct.add(nct)
        for pmid in o["pmids_by_record"].values():
            assert pmid not in seen_pmid
            seen_pmid.add(pmid)
        blob = json.dumps(t)
        assert "NCT" not in blob and "stratum" not in blob and "pmid" not in blob
    # split membership frozen and stratified
    assert {oracles[t["task_id"]]["split"] for t in tasks} <= {"DEV", "EVAL"}
    # determinism
    freeze2 = _build(tmp_path / "again", design)
    assert freeze2["public_tasks_sha256"] == freeze["public_tasks_sha256"]
    assert freeze2["oracle_sha256"] == freeze["oracle_sha256"]
    # prepare -> P-D suite layout
    out = mod.cmd_prepare(design, work, tmp_path / "campaign", force=False)
    assert set(out) == {"N1-DEV", "N1-EVAL"} and sum(v["tasks"] for v in out.values()) == 8
    for study in out:
        sdir = tmp_path / "campaign" / study
        assert (sdir / "public_tasks.json").exists() and (sdir / "private_oracle.json").exists()
        for arm in mod.ARMS:
            assert len(list((sdir / "requests" / arm).glob("*.json"))) == out[study]["tasks"]
        priv = mod.read_json(sdir / "private_oracle.json")
        assert set(priv) == {"schema_version", "answers", "strata"}


def test_adequacy_failure_routes_to_corpus_annotation_insufficient(tmp_path: Path) -> None:
    design = json.loads(json.dumps(DESIGN))
    design["corpus"]["sets_per_stratum"] = 2
    freeze = _build(tmp_path, design)  # default adequacy floor (150 sets) cannot be met by 8 sets
    assert freeze["adequacy"]["pass"] is False
    assert freeze["adequacy"]["terminal_if_fail"] == "CORPUS_ANNOTATION_INSUFFICIENT"


def test_canary_rejects_leaked_oracle() -> None:
    public = {"task_id": "n1-0001", "records": [{"record_id": "r1", "title": "x", "abstract": "see NCT01234567"}]}
    oracle = {"ncts_by_record": {"r1": "NCT01234567"}, "pmids_by_record": {"r1": "1"}, "dois_by_record": {}}
    with pytest.raises(mod.CorpusError):
        mod.assert_no_oracle_leak(public, oracle)
    public["records"][0]["abstract"] = "clean"
    public["stratum"] = "NS1A"
    with pytest.raises(mod.CorpusError):
        mod.assert_no_oracle_leak(public, oracle)
    del public["stratum"]
    mod.assert_no_oracle_leak(public, oracle)


def test_fetch_uses_injected_transport_and_manifest(tmp_path: Path) -> None:
    calls: list[str] = []

    def transport(url: str) -> bytes:
        calls.append(url)
        if "esearch" in url:
            return json.dumps({"esearchresult": {"count": "2", "idlist": ["1", "2"]}}).encode()
        return _corpus_xml(1, 2, "41").encode()

    design = json.loads(json.dumps(DESIGN))
    design["corpus"]["topics"] = ["hypertension"]
    out = mod.cmd_fetch(design, tmp_path, transport=transport, sleep=lambda s: None)
    assert out["records"] == 2 and len(calls) == 2
    manifest = mod.read_json(tmp_path / "FETCH_MANIFEST.json")
    assert all(len(p["sha256"]) == 64 for p in manifest["pages"] if "sha256" in p)

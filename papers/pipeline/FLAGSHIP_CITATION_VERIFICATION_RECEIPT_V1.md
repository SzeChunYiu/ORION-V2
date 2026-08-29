# Flagship Citation Verification Receipt V1

**Manuscript:** `papers/drafts/FLAGSHIP_MACHINE_EPISTEMICS_MANUSCRIPT_V8.md` (first citation-entailed surface)
**Verification date:** 2026-08-29 (single session, live web verification)
**Method:** per-reference identity check against live web sources (publisher pages, arXiv, PhilSci-Archive, SSRN, journal sites) before placement in V8. No reference was added to the manuscript from memory alone without either (a) live verification of authorship/title/venue/year or (b) canonical-standard status.
**Scope guard:** this is a *central-claims first pass*, not the complete sentence-level entailment audit. It covers every reference that supports (i) the field-priority/convergence story, (ii) the AI4Science systems row, (iii) the five 2026 neighbors, (iv) named quantitative/DOI-bearing claims. Classics used as tradition anchors (e.g., Wiener, Dewey, Peirce) are cited as CANONICAL_STANDARD and remain open for page-precise entailment.

## A. VERIFIED_WEB (identity confirmed against live sources this session)

| Ref | Work | Verified identity | Class |
|---|---|---|---|
| [1] | Kramer & King, automated scientific discovery survey | **Two authors** (M. Kramer, R. D. King); arXiv:2305.02251; journal version in *Machine Learning* | VERIFIED_WEB |
| [2] | Lu et al. 2026, AI Scientist automation | *Nature* 651, 914–919 (2026); end-to-end AI-research automation paper | VERIFIED_WEB |
| [3] | Ghareeb et al. 2026 (Robin multi-agent discovery) | *Nature* (2026), DOI 10.1038/s41586-026-10652-y; **this is the work the genealogy ledger previously mislabeled "Rodriques et al."** — Rodriques is a co-author | VERIFIED_WEB |
| [4] | Boiko et al. 2023, Coscientist | *Nature* 624, 570–578; DOI 10.1038/s41586-023-06792-0 | VERIFIED_WEB |
| [5] | Szymanski et al. 2023, A-Lab | *Nature* 624, 95–100; DOI 10.1038/s41586-023-06734-w | VERIFIED_WEB |
| [6] | Robot-chemist row (news) | *Nature* News, DOI d41586-023-03956-w; reports the external challenge to A-Lab novelty claims | VERIFIED_WEB |
| [21] | Causal transportability | Bareinboim & Pearl, JAIR 56, 241–287 (2016) used in V8 (general transportability decision algorithm) instead of the 2011 workshop version | VERIFIED_WEB |
| [37] | Dependent evidence synthesis | Hedges, Tipton & Johnson, *JEBS* 35, 169–192 (2010) | VERIFIED_WEB |
| [54] | MacKnight et al. 2026, provenance grounds trust | *Nature Computational Science* Comment, published 2026-08-20; authors MacKnight, Novitskiy, Radadiya, Gomes | VERIFIED_WEB |
| [59] | Ratti, epistemic control in ML-based science | **Preprint**: PhilSci-Archive 26333; arXiv:2601.11202; forthcoming in *The Role of AI in Science* — carried as preprint in the reference list | VERIFIED_WEB |
| [60] | Wojarnik, spec-driven AI for empirical research | **Preprint**: SSRN 7073778 (2026) — carried as preprint | VERIFIED_WEB |
| [61] | Kim & Park, LLM-assisted research asymmetries | *Research Evaluation* 35 (2026) | VERIFIED_WEB |
| [62] | Cowley & Gahrn-Andersen, epistemic engineering | *Frontiers in Artificial Intelligence* 5, 960384 (2023) | VERIFIED_WEB |
| [63] | Wheeler, machine epistemology | Chapter in **The Routledge Companion to Philosophy of Social Science** (not the generic philosophy companion), ch. 38, DOI 10.4324/9781315410098-38 | VERIFIED_WEB |
| [65] | van de Schoot et al., ASReview | *Nature Machine Intelligence* 3 (2021), DOI 10.1038/s42256-020-00287-7 | VERIFIED_WEB |
| [67] | Rahwan et al., Machine behaviour | *Nature* 568, 477–486 (2019) | VERIFIED_WEB |
| [68] | Moss et al., machine-behaviour critique | *Nature* Correspondence (2019), DOI d41586-019-03002-8 | VERIFIED_WEB |
| [71] | Koskinen, no satisfactory social epistemology of AI-based science | *Social Epistemology* (2023); original of the Koskinen–Peters exchange | VERIFIED_WEB |
| [72] | Peters rebuttal (+ Koskinen reply) | SERRC 13(1), 58–66 (2024) and SERRC 13(5), 9–14 (2024); Peters holds existing social epistemology suffices under a deferred-responsibility account (echoing Durán & Formanek) | VERIFIED_WEB |
| [73] | Camps-Valls, AI needs a new philosophy of science | *The Innovation* 7(5), 101311 (2026), sole author | VERIFIED_WEB |

## B. Corrections made during verification (ledger → V8)

1. **"Rodriques et al. (Nature, 2026)"** in `FLAGSHIP_PARENT_GENEALOGY_LEDGER_V1.md` resolves to the Robin paper — first author Ghareeb; Rodriques is a co-author. V8 cites Ghareeb et al.
2. **Wheeler chapter venue** corrected to the *Routledge Companion to Philosophy of Social Science* ch. 38.
3. **Kramer** corrected to Kramer & King (two authors).
4. **Ratti** and **Wojarnik** are preprints; V8 marks them "Preprint at …" rather than implying journal publication. Their claims are used as *emerging-convergence evidence*, which preprint status does not weaken, but they must not be cited as established literature.
5. Pearl & Bareinboim 2011 (workshop) replaced by Bareinboim & Pearl 2016 (JAIR) as the citable general transportability result.

## C. CANONICAL_STANDARD (tradition anchors; identity from standard bibliographic knowledge, page-level entailment open)

[7]–[20], [22]–[36], [38]–[53], [55]–[58], [64], [66], [69], [70] — FAIR, Greshake, Silver 2017/2016, Kelly 1996, Doyle, de Kleer, AGM, Reiter, Russell & Wefald, Chaloner & Verdinelli, Settles, Wiener, Ashby, Hollnagel et al., Meredith, VIM/JCGM, Cousot & Cousot, Milner, Star & Griesemer, Gelman et al. workflow, Gelman–Meng–Stern, Talts et al., Higham, Moore, Barr et al., Chen et al., Mayo, Moreau & Groth, Stodden et al., T. Kelly, Dung, Lamport et al., FLP, Dewey, Peirce, Ryle, Polanyi, Suchman, Hutchins, Flavell, Goldman, Coady, Knorr Cetina, Kukutai & Taylor, Carroll CARE, mathlib, Gulwani et al., Stanley & Lehman, Ha & Schmidhuber, Darden & Maull, Fortunato et al., Perdomo et al.

## D. Counters

```text
TOTAL_REFERENCES_V8 = 73
VERIFIED_WEB = 20
CANONICAL_STANDARD = 53
CENTRAL_CLAIM_CITATION_PASS = COMPLETE (V8)
SENTENCE_LEVEL_ENTAILMENT_AUDIT = OPEN
CONTRARY_AND_LIMITING_LITERATURE_AUDIT = OPEN
PRE_SUBMISSION_NAME_COLLISION_SEARCH = OPEN
FABRICATED_OR_UNVERIFIED_REFERENCES_FOUND = 0
```

## E. Discipline notes

- No ORION-V2 unpublished result appears as field evidence anywhere in V8 (Perspective constraint honored; self-citations to the ORION-V2 programme would require independently published primary work).
- Ref [6] and [68] are journalism/correspondence and are used only as *documented dispute existence* evidence, never as adjudications of the scientific questions.
- Uncertain page numbers were dropped in favor of DOIs rather than guessed ([3], [65], [68], [54], [61]).

# Top-Tier Venue and AI-Use Contract V1

**Programme:** ORION-V2 / Machine Epistemics  
**Checked:** 2026-08-29 against current official publisher/journal pages.  
**Purpose:** prevent a scientifically complete manuscript from becoming an invalid submission because format, article type, overlap or AI-accountability rules are misunderstood.

## 1. Nature Portfolio AI policy — load-bearing project gate

Current Nature Portfolio AI policy uses a risk-based framework.

### Green / assistive

Examples include language polishing, translation, formatting/structuring, methodological comparison, stress-testing questions and data cleaning. AI does not introduce new intellectual content and does not replace scholarly judgment.

### Amber / evaluative or interpretive

Examples include suggesting analytical/experimental/methodological approaches, explanatory summaries, literature comparison, extensive writing support and exploratory pattern identification. AI can introduce intellectual content, but the use requires:

- human oversight and verification;
- transparent disclosure;
- demonstrable human-led judgment and accountability.

### Red / not permitted

The current policy explicitly prohibits opaque or unaccountable AI substitution for scholarship, including generating hypotheses/analyses/conclusions and presenting them as human-derived, fabricating data/citations/results, or using AI for core research reasoning without disclosure.

AI cannot be an author.

### ORION-V2 consequence

This programme has used LLMs extensively for:

- literature discovery;
- theoretical/formal development;
- experimental design;
- adversarial criticism;
- software generation;
- manuscript drafting.

Therefore none of the surviving Nature-Portfolio submissions is authorized merely because the repository contains a polished manuscript.

Every paper requires a **Human Scientific Adoption Review** proving that final human authors:

1. understand the research question, theorem/protocol and strongest parents;
2. have personally checked the load-bearing sources/results or assigned accountable coauthors;
3. can independently defend the reasoning and final interpretation;
4. have corrected/rejected AI-generated suggestions they do not endorse;
5. take responsibility for every claim, citation, figure and result;
6. disclose AI use transparently according to current venue placement rules.

The disclosure must describe substantive scientific assistance honestly; “language editing only” is prohibited when untrue.

## 2. Nature Machine Intelligence — Article

Current Article format:

```text
main text <= 3,500 words
abstract <= 150 words, unreferenced
figures/tables <= 6 total display items
structure = unheaded Introduction; Results; Discussion; Methods
references ~50 guideline
supplement permitted
peer reviewed
```

Primary planned papers:

- P-A structural transfer discovery;
- P-C scientific control;
- P-D dependence/dynamic evaluation.

### Filing rule

These papers may not be sent as NMI Articles while their protected Results sections are empty. A pre-results manuscript is a scientific freeze artifact, not an Article submission.

### Word-budget rule

After results:

- Introduction/theory/Discussion main-text prose must be contracted to leave enough of the 3,500-word main-text budget for actual Results;
- detailed formal proofs, benchmark construction, sensitivity, parent tables and reproducibility move to Methods/Extended Data/Supplement where editorially lawful;
- critical negative/adverse results remain main text.

## 3. Nature Machine Intelligence — Perspective

Current Perspective format:

```text
main text = 3,000–4,000 words
references <= ~100 guideline
peer reviewed
minimal previously unpublished supporting data only
forward-looking, balanced, may advocate a speculative position
```

The flagship is routed here **only as a Perspective/field hypothesis**, not as a disguised primary Results paper.

Flagship requirements:

- balanced treatment of strongest parents and contrary views;
- clear F0/F1/F2/F3 competition;
- no claim that Machine Epistemics is founded;
- no protected specialist result promoted before evidence;
- field-level assertions linked to external demarcation and future tests.

## 4. Nature Computational Science — Article

Current Article format:

```text
main text <= 3,500 words
abstract <= 150 words, unreferenced
display items <= 6
structure = unheaded Introduction; Results; Discussion; Online Methods
references ~50 guideline
supplement permitted
peer reviewed
```

Primary planned paper:

- P-B context-relative relations/transport, if protected cross-parent decision value survives.

Nature Computational Science also currently requires LLM use to be documented in Methods; LLMs cannot be authors.

## 5. Nature Computational Science — Perspective

Current Perspective format:

```text
length <= 4,000 words
references <= 100
peer reviewed
non-primary; only minimal new supporting research
```

This is an alternate flagship route if editor/scope fit is stronger than NMI and the final emphasis is computational/scientific-method control.

## 6. npj Artificial Intelligence — Article

Current Article guideline:

```text
main text typically <= 4,000–4,500 words
abstract typically 150 words, unreferenced
up to 10 display items
sections = Introduction, Results, Discussion, Methods, Data Availability
references ~60 guideline
peer reviewed
```

Fallback planned for P-C/P-D where scope fits.

Initial submission may be PDF/Word without special formatting; TeX/LaTeX can be submitted as compiled PDF initially and source at acceptance stage.

## 7. npj Artificial Intelligence — Perspective

Current Perspective:

```text
normally <= 3,000 words
references ~70 guideline
peer reviewed
```

Potential fallback for the flagship only if its current scope/content-type policy fits and no overlapping submission conflicts exist.

## 8. Artificial Intelligence (Elsevier) — fallback role

Artificial Intelligence welcomes principled new AI methods and in-depth evaluations, and also accepts Research Notes, Research Field Reviews and Position Papers.

Planned fallback:

- P-A;
- P-B.

Current Elsevier AI guidance allows AI assistance but requires human accountability, review of AI outputs/references and compliance with confidentiality/data/IP requirements. The exact journal Guide for Authors and AI declaration wording must be refreshed immediately before filing.

AIJ is not used as a way to avoid an adverse top-tier result; the scientific claim must remain the same or contract.

## 9. Overlap / paper-slicing gate

Nature Portfolio policies prohibit significant overlap between simultaneously submitted related papers and require disclosure of related manuscripts.

Because ORION-V2 has multiple related papers, before submitting any pair simultaneously the human author group must create an **Overlap Matrix** documenting:

- unique research question;
- unique primary dataset/benchmark or theorem/protocol;
- unique headline claims;
- shared methods/background;
- shared figures/tables;
- shared code/data;
- related-manuscript disclosure supplied to editors.

The project-wide survivor matrix already contracts P-E/P-F/P-G to reduce salami slicing.

## 10. Human scientific adoption gate

For every intended human author and every paper, require a signed internal review with:

- explanation of the paper's thesis in the author's own words;
- strongest parent(s) and novelty ceiling;
- explanation of the primary falsifier/negative terminal;
- examination of the raw or exact receipt behind each headline result;
- personal review of citations supporting load-bearing external facts;
- acceptance/rejection of AI-generated theoretical suggestions;
- current AI-use disclosure wording;
- authorship contribution and conflict declaration.

An author who cannot personally defend the scientific reasoning should not be used as the human-accountability surface for an AI-generated argument.

## 11. AI-generated figures/images

Do not use generative-AI artwork in Nature-Portfolio submissions. Scientific figures should be generated deterministically from data/receipts or manually designed schematics with source files and human review. Any exception for AI-as-subject research requires explicit current-policy/editorial confirmation.

## 12. Top-tier submission authorization rule

```text
IF protected_results_required AND protected_results_not_closed:
    SUBMISSION = NO

IF external_demarcation_required AND not_complete:
    FIELD_FOUNDING_SUBMISSION = NO

IF human_scientific_adoption_review != PASS:
    SUBMISSION = NO

IF AI_disclosure_is_incomplete_or_misleading:
    SUBMISSION = NO

IF significant_related_paper_overlap_not_disclosed:
    SUBMISSION = NO

IF current venue format/policy not refreshed:
    SUBMISSION = NO
```

Top-tier ambition does not override any of these gates.

## 13. Current portfolio authorization

```text
FLAGSHIP = SCIENCE_CONTENT_COMPLETE__SUBMISSION_BLOCKED_EXTERNAL_DEMARCATION_AND_PROTECTED_FIELD_EVIDENCE
P-A = SCIENCE_CONTENT_COMPLETE_PRE_RESULTS__SUBMISSION_BLOCKED
P-B = SCIENCE_CONTENT_COMPLETE_PRE_RESULTS__SUBMISSION_BLOCKED
P-C = SCIENCE_CONTENT_COMPLETE_PRE_RESULTS__SUBMISSION_BLOCKED
P-D = SCIENCE_CONTENT_COMPLETE_PRE_RESULTS__SUBMISSION_BLOCKED
LLM-PRA-51 = SEPARATE_BRANCH__FOLLOW_ITS_OWN_VENUE_AND_AI_POLICY_GATES
```

## Official policy surfaces checked

- Nature Portfolio AI editorial policy: `https://www.nature.com/nature-portfolio/editorial-policies/ai`
- Nature Machine Intelligence content types: `https://www.nature.com/natmachintell/content`
- Nature Machine Intelligence submission guidelines: `https://www.nature.com/natmachintell/submission-guidelines`
- Nature Computational Science content types: `https://www.nature.com/natcomputsci/content`
- Nature Computational Science submission/preparing-material guidelines: `https://www.nature.com/natcomputsci/submission-guidelines`
- npj Artificial Intelligence content types: `https://www.nature.com/npjai/content-types`
- npj Artificial Intelligence author/editorial pages: `https://www.nature.com/npjai/for-authors-and-referees`
- Elsevier generative-AI policy/guidance: `https://www.elsevier.com/connect/updated-generative-ai-policies-for-journals-supporting-responsible-use-while-protecting-trust`

All must be refreshed immediately before actual submission because AI/publication policies can change quickly.

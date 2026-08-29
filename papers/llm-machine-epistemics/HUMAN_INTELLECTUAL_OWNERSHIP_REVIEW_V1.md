# Human Intellectual Ownership Review V1

**Issue:** #51  
**Purpose:** make human authorship responsibility substantive rather than ceremonial after an AI-intensive research workflow.

This is not an automated gate and cannot be completed by an AI on behalf of an author.

## 1. Reviewer

For each intended human author, record:

```text
AUTHOR =
DATE =
VERSION_REVIEWED =
```

Do not infer names from GitHub metadata.

## 2. Core understanding checks

The author should answer in their own words, without copying the manuscript.

### Q1 — research problem

Why are current language prediction and current decision performance insufficient, in principle, to certify correct revision after later evidence?

`AUTHOR RESPONSE:`

### Q2 — one-bit witness

Explain the A/B provenance construction and why:

```text
C_stat^* = 0
C_dyn^*  = 1 bit
Omega_dyn = 1 bit
```

`AUTHOR RESPONSE:`

### Q3 — parent ownership

Name at least five strongest parents and state one important thing each already owns that this paper does **not** claim as new.

`AUTHOR RESPONSE:`

### Q4 — actual residual

What exact sequence makes the Prospective Revision Audit different from generic belief revision or generic memory compression?

`AUTHOR RESPONSE:`

### Q5 — alternate-channel problem

Why is deleting text or a memory record insufficient to establish that information left the model state?

`AUTHOR RESPONSE:`

### Q6 — update versus maintain

Why must the audit score both correct updating and correct non-updating/selective reopening?

`AUTHOR RESPONSE:`

### Q7 — acquisition versus retention

Give an example of a failure that is caused by missing evidence and an example caused by state compression. Why must the audit distinguish them?

`AUTHOR RESPONSE:`

### Q8 — empirical nonclaim

What does the finite theorem prove, and what does it **not** prove about real LLMs?

`AUTHOR RESPONSE:`

## 3. Proof/responsibility checks

The author must personally inspect:

- [ ] `PROOF_APPENDIX_V1.md`;
- [ ] canonical J5 one-bit receipt;
- [ ] selector/partition receipt;
- [ ] dynamic selector/refinement receipt;
- [ ] mutation assumption matrix;
- [ ] claim/receipt crosscheck;
- [ ] nearest-work parent matrix;
- [ ] citation coverage matrix.

For every load-bearing claim, the author should be able to identify either:

- the proof/receipt that supports it; or
- the parent source that owns it.

## 4. Citation checks

The author confirms:

- [ ] they have read enough of each **load-bearing direct parent** to understand the cited result rather than relying only on generated summaries;
- [ ] Brodu/R-PSR/AIS/stable-quotient/Belief-R/MEMENTO distinctions are accurate to their understanding;
- [ ] no direct parent is omitted merely because it weakens the novelty story;
- [ ] preprint/public-review status is described honestly;
- [ ] they agree with the bounded “search frontier” wording rather than a universal first-work claim.

## 5. AI-use responsibility check

The author acknowledges that LLM tools were used extensively for scientific assistance in this project.

They confirm:

- [ ] they understand the final arguments independently;
- [ ] they have corrected or removed claims they cannot personally defend;
- [ ] they accept responsibility for factual/citation errors that remain;
- [ ] they will disclose AI assistance truthfully under the chosen venue's current policy;
- [ ] they will not list an AI system as an author;
- [ ] they will not characterize the assistance as grammar-only if that is not true.

## 6. Authorship contribution decision

The individual must decide whether their actual contribution satisfies the chosen venue's authorship and AI-use policies.

Choose one:

- `AUTHORSHIP_RESPONSIBILITY_ACCEPTED`
- `CONTRIBUTOR_NOT_AUTHOR`
- `POLICY_FIT_UNCLEAR__DO_NOT_SUBMIT`

`DECISION:`

`RATIONALE:`

## 7. Scientific adoption decision

Choose one:

- `ADOPT_FINAL_CLAIMS_AS_WRITTEN`
- `ADOPT_WITH_LISTED_CONTRACTIONS`
- `DO_NOT_ADOPT__MATERIAL_SCIENTIFIC_OBJECTION`

`DECISION:`

`CONTRACTIONS / OBJECTION:`

A material new scientific objection should reopen the appropriate claim under a new prospective identity rather than being silently edited away.

## 8. Final signoff

Only after the checks above:

```text
HUMAN_INTELLECTUAL_OWNERSHIP_REVIEW = COMPLETE
AUTHOR =
DATE =
MANUSCRIPT_HASH_OR_COMMIT =
```

This receipt is an internal governance record. Whether it should be public or submitted is a separate authorship/privacy decision.

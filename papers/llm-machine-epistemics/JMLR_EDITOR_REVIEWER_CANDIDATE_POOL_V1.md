# JMLR Action Editor / Reviewer Candidate Pool V1

**Issue:** #51  
**Checked against current JMLR editorial board:** 2026-08-29  
**Purpose:** remove scientific/expertise-selection work from the final filing step while leaving conflict-of-interest adjudication to the actual human author group.

Official board source:

`https://jmlr.org/editorial-board.html`

Official JMLR cover-letter rule requires 3–5 suggested Action Editors and 3–5 suggested reviewers with no author COI.

## 1. Action Editor candidate pool

These are **expertise candidates only**. Do not place any name in the actual cover letter until every final author has checked JMLR's COI rule (family/close friend, advisor/advisee, collaboration within 3 years, or other material conflict).

### Tier A — strongest fit

**David Abel**  
Current JMLR listed expertise: reinforcement learning, philosophy, planning, abstraction.  
Why fit: state abstraction + decision sufficiency + philosophical boundary of representation adequacy.  
Potential role: strongest generalist for the predictive/decision/prospective-state distinction.

**Csaba Szepesvári**  
Current JMLR listed expertise: reinforcement learning, sequential decision making, learning theory.  
Why fit: sequential decision/state adequacy and future evidence/updateability.

**Kai-Wei Chang**  
Current JMLR listed expertise: large language models, trustworthy NLP, vision-language models.  
Why fit: direct relevance to autoregressive/LLM representation assessment and practical evaluation framing.

### Tier B — strong complementary fit

**Amichai Painsky**  
Current JMLR listed expertise: statistics, information theory, statistical inference, predictive modeling, data compression.  
Why fit: state-complexity/conditional-information and compression side of the paper.

**Martha White**  
Current JMLR listed expertise: reinforcement learning, representation learning.  
Why fit: representation adequacy and sequential control.

**Adam White**  
Current JMLR listed expertise: continual learning, reinforcement learning, robotics, knowledge representation, intrinsic motivation.  
Why fit: persistent state, future adaptation and representation semantics.

**Karl Stratos**  
Current JMLR listed expertise: representation learning, information theory, spectral methods, natural language processing.  
Why fit: language representation + information side.

### Suggested default 5 before COI filtering

```text
David Abel
Csaba Szepesvari
Kai-Wei Chang
Amichai Painsky
Martha White
```

If any COI exists, substitute from Tier B. Expertise ranking does not override COI.

## 2. Reviewer candidate pool

Reviewers need not be JMLR Action Editors. The final cover letter should choose 3–5 after author COI screening.

### Predictive / decision / state-theory reviewers

**Michael L. Littman** — predictive-state/RL lineage; strong for distinguishing the paper from PSR parents.

**Satinder Singh** — reinforcement learning, state representation/abstraction and decision sufficiency; strong hostile-parent reviewer.

**Nicolas Brodu** — decisional states; especially valuable for checking whether the responsibility-state component is already absorbed by decisional-state theory.

**Nan Jiang** — reinforcement-learning theory and state/decision representations; useful for sequential-decision rigor.

### LLM representation / memory reviewers

**Andrew Lampinen** — language models, representation analysis, adaptation/memory/cognitive modeling; useful for the real-LLM interpretation boundary.

**Kai-Wei Chang** — if not suggested/assigned as AE and no COI, suitable for LLM/trustworthy-NLP evaluation relevance.

### Information / compression reviewers

**Amichai Painsky** — if not suggested/assigned as AE and no COI, information theory/data compression.

**Karl Stratos** — if not suggested/assigned as AE and no COI, representation learning + information theory + NLP.

### Default reviewer pool before COI filtering

```text
Michael L. Littman
Satinder Singh
Nicolas Brodu
Andrew Lampinen
Nan Jiang
```

## 3. Why this pool is scientifically appropriate

The paper should not be reviewed only by LLM benchmark researchers. Its load-bearing risks are:

1. classical predictive/decision-state absorption;
2. information/compression triviality;
3. sequential-state/updateability assumptions;
4. whether the resulting audit matters for actual language-model/agent representations.

A balanced review set should therefore cover at least:

- one predictive/state-abstraction expert;
- one sequential-decision/RL expert;
- one information/compression expert or overlapping theorist;
- one LLM representation/memory expert.

## 4. Human COI checklist

For every candidate, each final author must check:

- [ ] no family/close-friend relationship;
- [ ] no lifetime advisor/advisee relationship;
- [ ] no collaboration in the past 3 years;
- [ ] no other relationship that could reasonably affect impartiality.

If any box fails or is uncertain, do not suggest that person until resolved.

## 5. Filing rule

An AI may maintain this expertise pool as the editorial board changes. It may **not** decide that a COI is absent from public information alone.

Final terminal:

`EXPERTISE_POOL_READY__HUMAN_COI_FILTER_REQUIRED`.

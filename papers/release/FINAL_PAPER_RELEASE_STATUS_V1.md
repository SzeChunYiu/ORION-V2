# Final Paper Release Status V1 — Superseded

**Historical date:** 2026-08-30  
**Author:** Sze Chun Yiu  
**Correspondence:** sze-chun.yiu@fysik.su.se

This was the release terminal produced before `academic-paper-skills` PR #16/#17 introduced the fail-closed research-integrity and formal-spine gates.

**Superseding status:** `papers/release/PR17_PAPER_REAUDIT_STATUS_V1.md`.

The stable metadata decisions remain valid:

- no Stockholm University or physics-department affiliation is claimed for these papers;
- preprint-facing packages use author name + correspondence email only;
- where a journal requires an affiliation/status line, use **Independent researcher** rather than implying institutional ownership of the work;
- AI disclosure remains concise but truthful:

> AI tools assisted with literature search, drafting/editing, formalization, critique and code development. The author is responsible for all scientific content.

The old `FINISHED_FOR_ARXIV_RELEASE` terminal is **not reusable** after PR16/PR17 because:

1. the flagship V14 Perspective failed the new formal-spine preservation gate and required a versioned main-text repair; and
2. both papers now require an independent PR16 claim/source integrity verification bound to the exact final artifact before `submission_ready` or `publication_ready` may be asserted.

```text
STATUS_V1 = HISTORICAL_SUPERSEDED
CURRENT_STATUS = SEE_PR17_PAPER_REAUDIT_STATUS_V1
```

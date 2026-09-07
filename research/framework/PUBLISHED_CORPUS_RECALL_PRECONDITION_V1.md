# Published-corpus recall precondition V1 — programme-level

**Class:** `STANDING_PRECONDITION__APPLIES_TO_EVERY_LANE`. **Date:** 2026-09-07.
**Authority:** none over any scientific claim. This document adds a required check; it grants
nothing and settles no result. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

## The rule

> **Any study in this programme that admits a PUBLISHED corpus as a protected decision endpoint
> must run a recall-signature scan on its arm replies, and report the result, before reporting any
> arm score from that corpus.**
>
> A single verbatim mention of a hidden-key field name is disqualifying for the corpus on its own.

`scripts/recall_signature_scan.py` implements it. `--self-test` is 11/11 and plants both answers,
because a scan that can only say "contaminated" is as useless as one that can only say "clean".

## Why this is a precondition and not a caveat

Our protected-endpoint machinery is built around keeping the answer out of the arm's **workspace**.
FM80 §3 requires that materials visible to model arms not contain the hidden key; §11 requires the
key absent from every model-visible workspace. SD80's own `g_` screen checks the record text. All
three are about the workspace, and all three can pass while the arm already knows the answer.

**When the corpus is published, the key is also in the model's weights.** No workspace hygiene
reaches that. Redaction closes pointers; it does not close recall.

This was measured, not supposed. FM80 §9 V2 (ORION-V2 #372) ran a retrieval baseline over 30
Reproducibility Project: Psychology cases with every URL stripped from the prompt — a control that
had to fire, and did: 100/100 raw records carry a URL and 0/100 rendered prompts do. The arm still
scored 0.900, and **16 of its 30 replies named the hidden-key field `Replicate (R)` verbatim** —
the column the grader reads the witness from. The native-parent control arm named it 0/30.

The failure is structural. It is not fixed by better blinding, a longer prompt, or a stricter
workspace.

## What the scan does and does not establish

**Establishes.** That an arm holds the corpus. There is no innocent route by which a reply names
the hidden-key field, so one verbatim mention is enough to disqualify the corpus as a protected
endpoint for that model.

**Does not establish.** Which individual answers were recalled. On the FM80 data, accuracy was
0.905 among replies carrying a recall marker and 0.889 among those carrying none — indistinguishable.
**Marker-absence proves nothing:** a model that knows the answer need not say so. So the scan is a
corpus-level disqualifier, never a per-case filter, and a score must not be decomposed into "recall"
and "reasoning" on the strength of it. An early reading of the FM80 probe did exactly that and was
corrected.

**Silence is not a clearance.** `NO_RECALL_SIGNATURE` is evidence about the replies scanned at the
stated thresholds, not a certificate that the corpus is uncontaminated.

## Scope of the rule

It binds wherever *all three* hold: the endpoint is a **protected decision**; the witness comes from
a **published** source; and an **LLM** arm produces the decision. That covers every naturalistic
replication corpus this programme has considered — RP:P, RP:CB, MLRC, the 1000+ theorems list, and
`EMPIRICAL_ASSET_PRICING_OSAP`, which was selected on criteria but never assembled.

It does **not** bind on generated/synthetic suites with private oracles, where the witness never
existed publicly. FG80's private oracle with a pre-run hash commitment is the shape that is safe
here — and note it saturated for an unrelated reason, so the two failure modes are distinct and a
study can hit either.

## How to run it

```
python3 scripts/recall_signature_scan.py \
    --replies replies.json \
    --key-fields "<the hidden-key column names your grader reads>"
```

`replies.json` is a list of `{id, text, answer?, truth?}`. Exit 0 only on `NO_RECALL_SIGNATURE`;
`CANNOT_CHECK` on empty input, which is deliberately **not** a pass.

Run it on **every arm**, including the ones expected to be clean. The control arm returning 0/30 is
what makes the treatment arm's 16/30 mean anything; without it the number is unanchored.

## Standing consequence for corpus selection

A corpus's eligibility criteria should carry this alongside the existing ones: *is the evidence
layer separable from the verdict at case level* (which removed MLRC) is a property of the
**artifact**; *is the verdict recoverable from the model's training data* is a property of the
**channel**. A corpus can pass the first and fail the second, and RP:P does exactly that. The check
belongs **before** a corpus is assembled, not after its arms have run.

skills-applied: none (programme precondition, no manuscript content)

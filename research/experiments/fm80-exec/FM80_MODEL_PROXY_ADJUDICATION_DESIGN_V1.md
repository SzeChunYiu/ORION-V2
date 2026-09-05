# FM80 model-proxy adjudication — frozen design V1 (channel-dependent; `HUMAN_GATE_BYPASSED__MODEL_PROXY`)

**Purpose.** Execute, with fresh-session model adjudicators, the FM80 clauses that require a person (§4.4, §7, §9.4, §9.7) and the
three judgement clauses (§3a, §3b, §3f), so that the executable gate `FM80-§9-EXEC` has inputs. Every output of this design carries the
label `HUMAN_GATE_BYPASSED__MODEL_PROXY`; none is ever reported as independent human adjudication, and FM80 §9 survival is not
reachable through it. **Frozen:** 2026-09-05, before any model call.

## Stage A — donor-key assembly (makes §3c–e, §4.1–4.3 EXACT)
- Pool: SD80 cases (formal 243, RPP 100, RPCB 76). Per case, a fresh-session model receives the *tagger-visible record only* (no hidden
  key) and the frozen discovery criterion: "name one candidate donor result from a different primary field whose structural form
  bears on the registered decision; give the citation and the structural mapping". Output = candidate donor + mapping, hashed as the
  case's private donor key. K = 20 top results of a frozen retrieval baseline (BM25 over the SD80 source snapshot + one pinned dense
  model, versions and snapshot sha256 in the JSON twin) decide §3d/§4.2 exactly; §4.1 by the frozen taxonomy (source field of record vs
  donor field); §4.3/§3g by string containment on the prompt-visible files.
- A case whose proxy proposes no donor is `INELIGIBLE` (§3), never negative evidence.

## Stage B — proxy adjudication (§3a, §3b, §3f; §4.4; §9.7)
- Two fresh-session adjudicators per domain, a third for pre-declared terminal disagreements; each sees the frozen target contract,
  the native evidence and blinded arm outputs, never arm identity. Disagreements recorded before any reconciliation. Agreement rate
  reported per clause with n. Same model family/version for all, frozen.
- §4.4 verdict = proxy relevance acceptance; §9.7 = proxy search for a stronger omitted parent (must name it, with the collapse
  argument). Both feed the executor as flags labelled `MODEL_PROXY`.

## Stage C — arms A0–A4 (FM80 §5) on the assembled eligible cases
- Same model family/version, tool budget, corpus and output contract for A1–A3; A4 analysis-only. Dispositions scored against the SD80
  witness (registered replication / machine-checked formalization outcome) by the executor.
- Sample: ≥ 61 eligible cases per domain (three domains) before `FM80-§9-EXEC` can clear Holm at the 10 pp bar; fewer → `UNDERPOWERED`.

## Terminal vocabulary
`EXACT_SUBSET_PASS__HUMAN_CLAUSES_PROXIED`, `EXACT_SUBSET_FAIL__HUMAN_CLAUSES_PROXIED`, `UNDERPOWERED_AT_REGISTERED_BAR`,
`INSUFFICIENT_ELIGIBLE_NATURALISTIC_CASES` (< 61 assembled in a domain), `CANNOT_CHECK`. None promotes P-A/P-B beyond `HOLD`.

## Custody and dispatch
Case IDs, prompt-visible files, proxy prompts, retrieval configuration, adjudication forms and analysis code hash-frozen before Stage A;
donor keys absent from every arm workspace. Dispatched on billy-old at the channel window (~2026-09-07 codex / ~09-09 z.ai) under a
`PROTECTED_RUN_AUTHORIZATION.json` minted at dispatch from the operator's standing verbatim authorization; the dispatcher refuses without it.

skills-applied: none (frozen design, no manuscript content)

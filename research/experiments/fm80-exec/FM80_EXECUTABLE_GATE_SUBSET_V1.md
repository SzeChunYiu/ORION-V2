# FM80 §9 — the executable subset, re-registered as a runnable gate; the human-only remainder routed to a labelled model proxy (#308 R11a)

**Attributed stage (one):** *gate design* — FM80's standalone survival gate is human-only on four clauses (§4.4, §7, §9.4, §9.7) and the
operator has no external adjudicator, so P-A/P-B sit on `CANNOT_CHECK_INDEPENDENT_ADJUDICATION` (`fm80-audit/P_A_P_B_GATE_DISPOSITION_RECEIPT_V1.md`).
**Lever:** separate what an exact checker can execute from what needs a person, register the executable subset as a gate that *runs*, and
route the remainder to a fresh-session model adjudicator that is **labelled `HUMAN_GATE_BYPASSED__MODEL_PROXY` and never claimed external**
(operator directive 2026-09-04: "human external tasks just find ways to bypass them"). **Frozen:** 2026-09-05. FM80 itself is not amended
(§12); this is a *sub-registration* under it. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

## 1. Clause census (`fm80_exec_gate.py enumerate`)

| class | clauses | what makes it that class |
|---|---|---|
| **EXACT** (11) | 3c, 3d, 3e, 3g, 4.1, 4.2, 4.3, 9.1, 9.2, 9.3, 9.5, 9.6 | arithmetic on a frozen case table (paired exact tests + Holm), set membership on a frozen taxonomy / top-K list, string containment on prompt-visible files, per-arm fidelity flags (formal domain: machine-checkable witness) |
| **MODEL_PROXY** (3) | 3a, 3b, 3f | a judgement ("written without the answer", "strongest native parent named", "witness capable of exposing a wrong transfer") a fresh-session model can render on blinded material, labelled, never external |
| **HUMAN_ONLY** (4) | 4.4, 7, 9.4, 9.7 | independence-from-construction of a *person*; not manufacturable by computation. A model proxy is registered for each (design §3) under the bypass label; the terminal vocabulary keeps them distinct |

(3c–e and 3g are EXACT given a donor key; 9.3's empirical-domain fidelity flags are MODEL_PROXY *inputs* to an EXACT clause and are labelled as such in the case table.)

## 2. The executable gate `FM80-§9-EXEC` (registered, runs now)

`fm80_exec_gate.py survival --cases <table> --baseline-rule <domain→A0|A1>` computes 9.1 (≥ 10 pp in ≥ 2 of 3 domains), 9.2 (exact
paired test, Holm across the three domain tests), 9.3 (no fidelity increase in any domain), 9.5 (A2 does not reproduce A3's gain, winning
domains), 9.6 (effect survives excluding visible-donor cases), each with its denominator. **Sample rule frozen (repair option A of the
pre-outcome correction):** the 10 pp bar and the exact paired test stand; a domain with fewer than **61** eligible cases cannot clear
Holm's first rung even at zero adverse discordance, so the executor reports `UNDERPOWERED_AT_REGISTERED_BAR` — never a negative — for
any domain below 61 that does not pass outright. Terminals: `EXACT_SUBSET_PASS__HUMAN_CLAUSES_4.4_7_9.4_9.7_PENDING`, `EXACT_SUBSET_FAIL`,
`UNDERPOWERED_AT_REGISTERED_BAR`, `CANNOT_CHECK` (exit 2, distinct). An `EXACT_SUBSET_PASS` promotes nothing on its own: §9 is a
conjunction and the four human clauses remain `NOT_OBTAINED__DISCLOSED_LIMITATION` unless their proxies are run and labelled.

**Checker discipline (`selftest`):** a planted positive table at n = 70/domain passes the exact subset; the same effect at the
registered n = 30 reports `UNDERPOWERED`, with 9.1 true and 9.2 false (the correction's arithmetic, executed); a null table fails
9.1; a planted fidelity regression fails 9.3; a table where A2 reproduces A3 fails 9.5. Best-case exact p at the bar: 0.25 at n = 30,
0.0156 at n = 61.

## 3. What was RUN on the only naturalistic pool (`sd80-preconditions`)

The SD80 case-matrix intake (455 records: FORMAL_MATHEMATICS_1000PLUS 243, PSYCHOLOGY_RPP 100, CANCER_BIOLOGY_RPCB 76,
MACHINE_LEARNING_MLRC 36) is the only assembled naturalistic pool. Under the exact preconditions: **§3c fails on 455/455 — no donor
key exists** — and §3d/3e/3g/4.1–4.3 are `CANNOT_CHECK` until a donor key, a frozen retrieval baseline (K, corpus snapshot, model) and
prompt-visible files exist. The exact-checkable state of FM80 is therefore `NOT_ASSEMBLED`, not negative; the executable gate has
nothing to score yet, and says so with a denominator (`results/FM80_EXEC_SD80_PRECONDITIONS_V1.json`).

## 4. The model-proxy path (channel-dependent; frozen here, dispatched at the window)

`FM80_MODEL_PROXY_ADJUDICATION_DESIGN_V1.md`: (i) **donor-key assembly** for SD80 cases by a fresh-session model with a frozen
discovery criterion (a prospective criterion is admitted by §3c) and a frozen retrieval baseline (BM25 + a pinned dense model, K = 20,
corpus snapshot hashed) so 3d/4.2 become EXACT; (ii) **proxy adjudication** of 3a/3b/3f, 4.4 and 9.7 by fresh-session model
adjudicators that see the frozen target contract and blinded outputs only, two per domain plus a third for pre-declared terminal
disagreements — the §7 *structure* replicated with models, every verdict tagged `HUMAN_GATE_BYPASSED__MODEL_PROXY`; (iii) arms A0–A4 on
the assembled cases under FM80 §5's matching. Sample target: ≥ 61 eligible cases per domain (three domains: formal, RPP, RPCB). The
terminal any such run can reach is at most `EXACT_SUBSET_PASS__HUMAN_CLAUSES_PROXIED` — publishable as a labelled proxy result,
never as FM80 §9 survival. Dispatcher to be staged on billy-old at the channel window under its own authorization.

## 5. Authority

Grants nothing: no P-A/P-B verdict, no survival, no release. What it changes is the *shape* of the blocker — from "the gate cannot be
executed" to "eleven clauses execute, three are proxy judgements, four are people; the pool has no donor keys yet" — with a checker that
has been made to fail on purpose before it was trusted.

skills-applied: none (lane registration, no manuscript content)

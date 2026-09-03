# E30-R13 — START HERE

E30-R11's registered question, asked again under a **registered channel request-body
contract**. A new prospective study under a **new campaign identity**: E30-R11's, E60's,
PC-R6's and E30-R12's records stay frozen terminal.

| file | what it is |
|---|---|
| `E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1.json` | canonical registered design (governs) |
| `E30_R13_CHANNEL_CONTRACT_RERUN_DESIGN_V1.md` | the same design in prose |
| `e30_r13_channel_calibration.py` | instrument measurement: what the channel does, per call shape |
| `e30_r13_budget_note.py` | budget derivation + wall-time feasibility; no outcome input |
| `e30_r13_fullreg_eval.py` | evaluation lane — the PC-R6 evaluator, one `e30r13` cell |
| `e30_r13_analysis.py` | endpoints imported from E30-R12 under a sha pin, plus GR0d and GR0e |
| `sbatch/` | LUNARC drivers: setup → agents → frozen lane → GR0 → suite → rollup+analysis |
| `../../../tests/unit/test_e30_r13_lane.py` | known-answer controls, including the negative ones |

**Why this study exists.** E30-R12 dispatched and terminated at
`EXECUTION_NOT_COMPLETED__NO_ENDPOINT_READ`: 119 of 480 responses written, 116 of them
envelope failures at the registered 6000-token cap, **0 evaluations, no gate, no endpoint
read**. The registered question is still unasked.

**The finding this design is built around.** All 119 of E30-R12's envelopes recorded
exactly one served model id, `glm-5.3`, equal to the frozen value, and its served-model
gate held on every envelope written. The condition that moved was the channel's
*behaviour* at that fixed id — which no registered gate observed. **Pinning a served
model id does not pin an experimental condition.** So R13 registers the request body by
sha256 over its bytes, records the configuration per envelope, and gates over it.

**The contract choice is measured.** Three request bodies, same frozen prompts, same
16 000-token headroom: the provider default and `thinking_enabled_2048` each reached the
headroom with **zero text characters** on 3 of 4 tasks — including the *smallest* task in
the frozen set; `thinking_disabled` ended every one of 108 calls at `end_turn` with text,
never above 3292 output tokens.

**Budgets are measured, not inherited.** 108 calibration calls across 6 tasks spanning the prompt-size range,
all 4 arms and every call shape, with replicates, run outside any campaign tree. The registered
per-call cap is 14 000 — four times the largest call measured — and is intended to be
non-binding; a call
that stops at `max_tokens` is a gate violation to report, not a shortfall to top up.
There is no escalation ladder.

**The one-line caveat, registered before dispatch.** At n = 40 the exact test cannot
reject below a 0.175 risk difference at any effect size, and power against the registered
5-percentage-point MID is 1–2%. n was reconsidered and **stays at 40** — the frozen
substrate holds prepared workspaces and baseline lanes for exactly 40 tasks. R13 is an
**estimation and diagnostic** study; **a non-rejection is not evidence of equivalence**.

**Endpoints.** E1 registered failing test fixed (primary) · E2 any critical new failure
(co-primary, non-inferiority margin 0.02) · D1 patch-apply rate (registered diagnostic).
The arithmetic is **imported** from `e30_r12_analysis.py` under a sha256 pin, not retyped.

**`PARENT_SUFFICIENT` and `NO_ARM_SEPARATION` are registered, legitimate terminals.**
If the arms do not separate once patches apply, that is reported as plainly as a positive.

**R13 vs R11 is descriptive only**, twice over: R11's envelopes record no served model id,
and R11 ran under no registered request-body contract. **R13 vs R12 is not a comparison at
all** — R12 read no endpoint.

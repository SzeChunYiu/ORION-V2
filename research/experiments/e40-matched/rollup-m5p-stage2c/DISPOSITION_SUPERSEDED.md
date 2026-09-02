# Read this before using `E40_M5P_STAGE2C_ROLLUP_V1.json`

The archived rollup carries `analysis.gates.disposition = "E40_TERMINAL"` and the matching
`preregistered_route` string. **That field is superseded and must not be read as the campaign's
disposition.**

The campaign's registered positive control (planted feedback recovery, design §7) **FAILED**
(terminal quality 0.6412, 0/8 cycles in the ≥0.8 basin; `planted.json` sha256
`a919807ac9c9b9ccabb4f733bd351f26079b1a4b255a84f3220d110d95158d26`). Under the inherited m2/m3
semantics — `e40_matched_runner_m3.py rollup()`: a failed planted or nullcal control forces
`CHECKER_INVALID__NO_VERDICT` — the campaign yields **no science verdict**. The frozen analysis
script reports the control verdicts but does not consume them in `evaluate_gates()`, which is why
the JSON still shows a routing terminal; the script was deliberately **not** modified after the
outcome was seen.

- Authoritative disposition: **`CHECKER_INVALID__NO_VERDICT`** — the E40 line is **not** terminated,
  and m6 is **not** authorized.
- Authoritative document: `../E40_M5P_STAGE2C_OUTCOME_RECEIPT.md`.
- Rollup json sha256 `b9266001db3851def4d6bffd0ee3ebd2c9090400fd749a8706b110eaaf6e1a7c`
  (unmodified, as produced).

Any lane reading `gates.disposition` programmatically (as the m5′ Stage-1 script read m4's rollup)
must apply this supersession.

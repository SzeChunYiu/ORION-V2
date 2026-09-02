# PRA Real-LLM Audit — Pre-registered Design V2 (larger frozen models; frozen before any protected run)

**Issue:** #51 · **Lineage:** Design V1 §9 registered contingency — "Design V2 with larger frozen
models under a fresh protected seed" — for the `ORDINARY_REASONING_FAILURE_DESPITE_RETAINED_STATE`
route that the V1 dev smoke predicted (both 7B models over-revised the maintain arm even under the
complete history: Qwen 3/4, Mistral 4/4). Protocol V2 §16 executed under V3 semantics, CR-02/CR-03/
CR-07/CR-08, the compatibility criterion, the prediction-channel scope note, and the H-EXT-4
predictive-congruence finding. **Machine-readable twin:** `PRA_REAL_LLM_AUDIT_DESIGN_V2.json`
(`schema_version orion.v2.pra.real-llm-audit-design.v2`; authoritative for every number).
**Class:** prospective empirical extension; freeze precedes run. **Scientific authority:** none; the
manuscript is not modified and gains nothing automatically from the outcome.

**Relation to V1.** V1 R1 (`campaign-pra-llm-r1`) is frozen, authorized and queued separately; this
design does not touch, read or supersede it. V2 is a second pre-registered execution of the same
audit with only the change the V1 contingency licenses — larger frozen open-weight models — plus
the two pre-registrations that change forces or that V1 §9 left open (a competence gate that
decides model *eligibility* before the protected seed exists, and the same-fibre reporting variant
H-EXT-4 requires). Everything else is carried verbatim; the only forced deviations are listed in §9
with their reason.

## 1. Question (unchanged from V1)

> After a frozen open-weight instruct model is matched, per episode, on the registered linguistic
> target (status-line continuation under `rho`) and on the current contract action, does removing
> the dormant `support_source` variable from its representation state — while verifying removal
> across the KV and hidden-activation channels — produce the predicted revision failure after the
> same later evidence, and does restoring only that variable (R3) repair it?

V1's dev smoke showed the 7B surfaces failing the *maintain* arm under full history, which the
routing maps to a competence boundary of the surface, not a prospective-state result. V2 asks the
same question on surfaces that pass a pre-registered competence check first, so that a GP1 failure
on V2 cannot be read as mere incompetence.

## 2. Frozen inputs

- **Models** (bf16, one A100-80GB, greedy, `max_new_tokens=160`, seed 51, batch 1 — decoding
  verbatim from V1):
  `Qwen/Qwen2.5-32B-Instruct @ 5ede1c97bbab6ce5cda5812749b4c0bdf79b18dd` (32.5 B, 65.5 GB) and
  `mistralai/Mistral-Small-24B-Instruct-2501 @ 9527884be6e5616bdd54de542f9ae13384489724`
  (23.6 B, 47.2 GB). Two families, both ungated, Apache-2.0, both fit one A100-80GB in bf16 with the
  ≤ ~800-token prompts of this suite; revisions resolved 2026-09-02 and pre-downloaded to the LUNARC
  `hf-cache` (HF shards only; Mistral's `consolidated.safetensors` skipped). Mistral-Small's HF
  `tokenizer.json` (Tekken vocabulary) loads with the stock fast tokenizer — no extras beyond V1's
  venv; its optional `SYSTEM_PROMPT.txt` is NOT used (single user turn, uniform across models, as V1).
- **Registered scope (CR-07 fields):** verbatim from V1 — `rho` = registry status line; present
  target = teacher-forced mean per-token log-prob of `Claim <id> is currently listed as SUPPORTED.`;
  current responsibility = contract `{RETAIN, REOPEN, ESCALATE}` under any-optimal-action semantics
  with 0/1 loss; future evidence = exogenous registry notices delivered identically to every
  condition (one new notice type: `RETRACT(source)+REGISTRY_FLAG_POLICY` for the same-fibre family);
  future responsibility = same contract after the notice.
- **Suite generator:** V1 generator verbatim (templated fictitious claims over 8 domains, three
  episode-local nonce sources per instance, 2 arms per instance) plus one registered secondary
  family. **Seeds:** dev `20260912` (V1 used 20260902); protected **sealed** — see §7. Counts
  (protected, 620 instances / 1240 arms):

  | family | n | role | gold after evidence |
  |---|---|---|---|
  | F0_ACQ | 40 | acquisition ceiling | ESCALATE both |
  | F1_P0 | 60 | zero-extra-state control | REOPEN both / RETAIN both |
  | F2_P1 | 60 | current cross-channel | current RETAIN vs REOPEN |
  | F3_P2_CANON | 120 | **primary** canonical fixture (V1 verbatim), `RETRACT(A)` | hA REOPEN vs hB RETAIN |
  | F3_P2_CANON_SF | 120 | **secondary** same-successor-fibre variant (H-EXT-4), `RETRACT(A)+FLAG_POLICY` | hA REOPEN vs hB RETAIN |
  | F3_P2_MIRROR | 60 | unrelated-source retraction | RETAIN both |
  | F3_P2_INDEP | 60 | independent sufficient supports | hAB RETAIN vs hA REOPEN |
  | F3_P2_RECON | 60 | evidence carries the annotation (negative control) | annotation-determined |
  | F3_P2_TIE | 40 | expression of concern | hA {ESCALATE,REOPEN} vs hB {RETAIN,ESCALATE} |

  Dev split: 4 per family (36). The V1 families, counts, prompts, contract text, filler, tolerance
  and answer format are byte-for-byte those of V1 (the shared runner renders the V1 design to the
  archived V1 suite digests; unit-tested).
- **Representation conditions R0–R4, token-budget matching, alternate-channel conditions on
  F3_P2_CANON, probe (Gate A), Gate B omission:** verbatim from V1 §2.

### 2a. The same-fibre secondary family (H-EXT-4)

`H_EXT4_QUANTITATIVE_REVISION_PREMIUM_V1.md` shows that the paper's canonical P2 fixture places its
two successors in *distinct predictive fibres* (after `RETRACT(A)`, hA's registry status line
becomes REOPENED while hB's stays SUPPORTED), so its one-bit premium is over-determined: decision
conflict and successor fibre drift both force the split, and the Fano-form regret bound is only
licensed under predictive congruence (PC). The `same_succ_fibre` witness shows the decision conflict
alone yields the same bit. H-EXT-4 therefore requires the premium to be *reported under PC*.

`F3_P2_CANON_SF` realises PC on the LLM surface by construction: same histories, same R-states,
same gold as the canonical fixture; the evidence is the identical `RETRACT(A)` notice followed by a
registry flag policy that sets the status line of *every* claim whose file lists A (both arms do) to
`Claim <id> is currently listed as FLAGGED.` — an administrative marker that, by the notice's own
words and by the contract, does not by itself change the accepted status. Both arms' successors thus
share one registered linguistic target (recorded per arm in the suite as
`successor_linguistic_target`, identical across arms) while the correct actions still diverge
(hA REOPEN, hB RETAIN). The R2/R3 gap on this family is decision-driven only.

**Primary vs secondary.** GP1 and its terminal mapping stay on `F3_P2_CANON` exactly as in V1, so
V1 R1 and V2 R1 are comparable on the load-bearing contrast; `F3_P2_CANON_SF` is a registered
secondary at the same n (identical power) whose contrast B-SF (arm and instance level) and C-SF
(R3 vs R0) are reported beside B in every rollup and never gate. If the full-pass route is ever
taken, the empirical section must report both variants (§5). Successor-fibre equality is a property
of the registered target, not of model output, and is not measured by the runner.

## 3. Statistics

Verbatim from V1 §3 (instance as independent unit; exact McNemar at instance level, arm level
nested; Wilson 95 %; paired TOST with margin 0.05 nats/token and per-unit 0.15; joint-intersection
certificates with incompatible-cell rate primary; three-history control re-executed). Power: as V1
for n = 120 on the canonical fixture, and identically for n = 120 on the same-fibre variant.

## 4. Gates (frozen pre-outcome; thresholds in the JSON)

- **GPC — pre-registered competence gate (new, dev split only, decided BEFORE the protected seed
  exists).** Per model, on the full dev split (36 instances, 72 arms) under the complete history
  R0 in the revision stage: maintain accuracy over `MAINTAIN_REQUIRED` arms ≥ 0.75 AND update
  accuracy over `UPDATE_REQUIRED` arms ≥ 0.75. A model that fails is *replaced* by another ungated
  open-weight instruct model that fits one A100-80GB in bf16, the replacement and its reason are
  recorded in §9, and GPC is re-run on the replacement. This is the registered, legitimate pre-run
  use of the dev split; it is exhausted once the protected seed is sealed. GPC never enters
  GP0–GP3, the terminal mapping or the routing; its dev numbers are reported in every rollup.
  Its point is scope: with GPC passed, a V2 `ORDINARY_REASONING_FAILURE_DESPITE_RETAINED_STATE`
  terminal can no longer be explained by a surface that could not follow the contract at all.
- **GP0 present equivalence, GP1 R3 > R2 on P2 (contrast B on `F3_P2_CANON`), GP2a/GP2b alternate
  channel, GP3 controls:** thresholds and rules verbatim from V1 §4.
- Secondary, reported not gated: contrasts A, C, E, F0_ACQ ceiling, F3_P2_TIE compatible-cell
  behaviour, F3_P2_INDEP selective reopening (as V1), plus **B-SF / C-SF** on `F3_P2_CANON_SF`.

## 5. Pre-registered routing

The V1 §5 table applies unchanged (full pass in both models → the manuscript MAY gain ONE
registered empirical section under a NEW manuscript version and NEW freeze, never automatic;
single-model pass → boundary result; GP0/GP1/GP2a/GP3 failures → the mapped registered negatives;
no-rescue clause). Two additions: (i) any such section must report contrast B on both the canonical
and the same-fibre variant; (ii) V1 R1 and V2 R1 are reported side by side and neither overrides
the other — a V1 `ORDINARY_REASONING_FAILURE` terminal beside a V2 pass is the registered
"competence boundary of the surface" reading, not a rescue of V1.

## 6. Controls and leakage

As V1 §6, plus: the flag-policy sentence in `F3_P2_CANON_SF` is identical across arms and applies
to both arms' files, so it carries no arm information; the planted stub contract-follower resolves
the same-fibre evidence exactly as the canonical one and the constant-RETAIN null does not (unit
tests). The unit tests also pin the V1 suite digests so the shared runner cannot drift V1.

## 7. Custody and the sealed protected seed

- Runner `research/llm-machine-epistemics/pra_real_llm_audit.py` (shared with V1; V2 selected with
  `--design`; no gate logic changed — additions are schema acceptance, the sealed-seed path, the
  `competence-gate` stage, the secondary family and its reported contrast). sha256 of runner and
  design JSON recorded in the PR, every receipt and the rollup.
- **Sealed seed.** After both models pass GPC on dev, a file `<int>:<256-bit salt>` is generated on
  LUNARC (`/projects/hep/fs9/users/scyiu/orion-v2-pra-llm/v2/protected_seed.sealed`, mode 0600,
  never printed, never copied to the repo pre-run). The design JSON carries only its sha256
  (`suite_generator.seed.protected_commitment_sha256`). The runner generates the protected split
  only when given `--protected-seed-file` whose sha256 equals the commitment; without it the
  protected split is skipped and recorded as `SEALED_SEED_NOT_SUPPLIED`. The salted form makes the
  commitment non-invertible, so the protected suite cannot be regenerated or inspected from the
  repo before the run. Post-run the sealed file is archived beside the rollup (reveal).
- Per-call logging, hidden-state dumps, LUNARC results root
  `/projects/hep/fs9/users/scyiu/orion-v2-pra-llm/campaign-pra-llm-v2/` (`dev-smoke/`, `dev-gpc/`
  now; `protected/` only after authorization), repo archive
  `research/llm-machine-epistemics/results/pra-llm-v2/`, rollup `PRA_REAL_LLM_AUDIT_ROLLUP_V2.{json,md}`.
- Environment: `PRA_REAL_LLM_AUDIT_V2_ENV_RECEIPT_V1.md`; sbatch `sbatch/pra_llm_v2_dev_smoke.sbatch`
  (run) and `sbatch/pra_llm_v2_r1.sbatch` (NOT run; `--time` sized from the measured V2 latency;
  requires the V2 token and the sealed seed file; must not be queued while the V1 R1 array is
  pending or running). V1 files at the LUNARC base directory are untouched (V2 lives in `v2/`).

## 8. Non-goals / no-rescue clause

As V1 §8. In addition: GPC is not a result and cannot be re-run after the seed is sealed; a model
replacement after sealing is not permitted (that would be Design V3 with a new seed). The
same-fibre family does not replace the canonical fixture as the gate carrier; reporting both is the
whole of its role.

## 9. Ambiguities resolved at freeze, forced deviations, and the replacement record

- V1 §9 resolutions (V3 semantics, literal KV retention, R0 as probe positive control, ESCALATE
  semantics, JSON authority) carry over unchanged.
- **Forced by model size:** `--mem` raised (128 G smoke / 160 G protected) for the 32B checkpoint
  load; `--time` re-sized from measured V2 latency (see the env receipt). Nothing else in the
  sbatch changes.
- **Why the same-fibre family is secondary, not primary:** comparability of GP1 with V1 R1, and
  the V1 contingency licenses only a model change; H-EXT-4's requirement is about *reporting* the
  premium under PC, which the secondary family satisfies at equal power.
- **Why GPC is decided on the dev split and not on a protected subsample:** the dev split is
  already the only pre-run-touchable data under V1's rule; using it to decide eligibility keeps the
  protected split uninspected and makes replacement possible before any protected instance exists.
  GPC thresholds (0.75/0.75) were fixed before any V2 model output was seen.
- **Sealed rather than plain protected seed:** V1 wrote its protected seed into the design JSON; a
  plain seed allows anyone to regenerate and read the protected suite pre-run. V2 seals it.
- **Runner compatibility:** the runner keeps `FAMILIES` as a superset and iterates only the families
  a design lists without consuming randomness for the rest, so V1's suites are byte-identical
  (dev `98c8cbb5…`, protected `21b5b0f7…`, pinned in unit tests). The successor-target field is
  emitted only for the same-fibre family, so no V1 instance changes.
- **Replacement record (GPC on dev):** _filled at freeze from the dev GPC check — see the env
  receipt §4; the list below is final._
  - `qwen2.5-32b-instruct`: GPC_PENDING
  - `mistral-small-24b-instruct-2501`: GPC_PENDING
- **Registered risk (dev smoke, not evidence):** _filled at freeze — see the env receipt §5._

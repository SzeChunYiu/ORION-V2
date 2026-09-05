# PRA real-LLM audit V2 — protected outcome receipt

**Terminal: `P2_SINGLE_MODEL_ONLY__REGISTERED_BOUNDARY_RESULT`.**

The registered prospective-revision effect is demonstrated on one of the two frozen models. The
second model's data cannot carry the prospective claim, because its own pre-registered
present-equivalence gate fails: the two conditions already differ on current behaviour, so its
later-revision contrast is a current-state deficit and is routed as such. This is a bounded
positive with a disqualified arm, reported at earned strength.

`NO NOVELTY OR BREAKTHROUGH CLAIM`. No scientific authority is granted by this file; routing into
the manuscript requires a new PRA version and a new freeze.

## 1. Provenance and custody

| item | value |
|---|---|
| design | `ORION51.PRA_REAL_LLM_AUDIT.design.v2`, sha256 `c0b65dc40b3123e4…` |
| runner | `pra_real_llm_audit.py`, sha256 `198626238170df48…` (byte-identical to the V2 runner on ORION-V2 main) |
| suite | sha256 `526b47b8c2f93cf8…` |
| sealed seed | `protected_seed.sealed`, sha256 `d53e374809bfd6f7…` = the design's registered commitment |
| execution | LUNARC array `3566415`, gpua100 `cg20`; arm `_0` qwen2.5-32b-instruct COMPLETED 2026-09-04T11:39:57 (1d09:23:12); arm `_1` mistral-small-24b-instruct-2501 COMPLETED 2026-09-05T10:25:18 (22:45:21) |
| rollup of record | billy-old, 2026-09-05T10:53:24+02:00, runner rc 0, Python 3.14.4 |
| rollup outputs | `PRA_REAL_LLM_AUDIT_ROLLUP_V2__protected.json` sha256 `fcf93fa465bba43f…`; `…​.md` sha256 `b8684907276f2096…` |
| protected tree | 38-entry custody manifest `CUSTODY_MANIFEST_SHA256_PROTECTED_TREE.txt` |

The rollup ran **once**, on the campaign tree pulled from LUNARC and md5-verified on both sides,
behind preconditions that were asserted rather than assumed: runner/design/sealed-seed hashes
against their registered values, all four stage outputs present and non-empty for both models,
and both array tasks having emitted their completion marker. The script refuses and writes
`ROLLUP_BLOCKED` on any failure, and refuses to run twice.

Artifacts in this directory were transferred to the repository and re-hashed here; both rollup
files are byte-identical to the record on billy-old (verified with a planted-wrong-hash control
that correctly failed).

## 2. Result

| model | GP0 | GP1 | GP2 | GP3 | terminal |
|---|---|---|---|---|---|
| qwen2.5-32b-instruct | ✔ | ✔ | ✔ | ✔ | `P2_PROSPECTIVE_REVISION_STATE_REQUIRED` |
| mistral-small-24b-instruct-2501 | ✘ | ✔ | ✔ | ✔ | `CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE` |

**qwen2.5-32b-instruct — the registered effect.** Present-equivalence holds exactly (per-unit pass
1.000; TOST mean Δlogprob −0.000, equivalent). On the canonical P2 contrast, accuracy moves
0.079 → 1.000 across R2→R3 (n = 240, 0/221 discordant against the direction, exact p ≈ 0), and the
same-successor-fibre variant moves 0.242 → 1.000. So a state that is equivalent on present
behaviour is not equivalent on later evidence-triggered revision — the paper's registered
prediction, on a real model.

**mistral-small-24b-instruct-2501 — disqualified by its own gate, not discarded.** GP0 fails
(per-unit pass 0.296): its R1 and R2 conditions already differ on *current* accuracy (0.317 vs
1.000 on the P1-current contrast, 82/120 discordant one way, 0 the other). Its R2→R3 movement
(0.250 → 1.000) is therefore not attributable to prospective revision, and the runner routes it to
`CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE` rather than counting it as support. The gate did
the work it was registered to do.

**Mechanistic control, both models.** Contrast D (true removal → KV retained) moves 0.079 → 1.000
and 0.250 → 1.000 respectively, terminal
`INTERVENTION_REMOVED_REGISTERED_DORMANT_INFORMATION__KV_SURVIVAL_CONTROL_CONFIRMED`. The probe
agrees: `R2_TEXT_REMOVED_KV_RETAINED` = 0.990 on both models against `R2_TRUE_REMOVAL` = 0.552 /
0.562. The information the intervention removes is present but dormant, and the control confirms
the removal is what the design says it is rather than a prompt artefact.

The three-history joint-intersection control passes.

## 3. What this licenses, and what it does not

Licenses: PRA may report a real-model empirical bridge for the registered P2 effect, stated as
**one of two frozen models, with the second disqualified by the pre-registered present-equivalence
gate**, together with the dormant-information control that holds on both. This is the honest form
of the finding the paper's hostile review named as missing.

Does not license: a general claim about deployed language models; a two-model replication; any
claim that the mistral arm supports or refutes the effect (its gate failure makes it silent on the
question); dropping either arm from the report; or any change of family, prompt, threshold or gate
after this outcome — the routing forbids it and no such change was made.

## 4. Custody note on the authorization

The V2 protected run executed under the design's own `protected_run.authorization_token`, which the
runner requires and which the rollup passes back from the frozen design. The operator's standing
verbatim authorization for this computation is recorded in the programme log
(2026-09-02, "run all the computation tasks.. finish all the researxh asap"; reaffirmed 2026-09-04).
No authorization file was minted for this rollup because the design supplies its own token; this is
recorded here so the difference from the SD70-V3 case (where no minting stage existed and one was
minted post-dispatch with disclosure) is explicit rather than silent.

## 5. Reproduction

```
pra_real_llm_audit.py --stage rollup --workdir <protected campaign tree> \
  --design PRA_REAL_LLM_AUDIT_DESIGN_V2.json --backend hf --split protected \
  --protected-authorization <design.protected_run.authorization_token>
```

Run on billy-old (never the Mac, per the standing compute rule). The 929 MB campaign tree is not
committed; its 38-entry sha256 custody manifest is, so any future copy can be checked against it.

#!/usr/bin/env python3
"""Render SD80_CASE_MATRIX_INTAKE_V1.md from the finalized intake JSON."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research/experiments/sd80"
r = json.loads((OUT / "SD80_CASE_MATRIX_INTAKE_V1.json").read_text())
gn0 = r["gn0_calibration"]
ft = r["full_tagging"]["per_domain"]
lines = []
L = lines.append
L("# SD80 Case-Matrix Intake V1 — naturalistic witness sources + PC-R7 obligation-provenance tagging calibration")
L("")
L(f"**Class:** `{r['class']}`  ")
L(f"**Computed:** {r['computed_utc']} · **Host:** {r['host']}  ")
L("**Frozen inputs:** PC-R7 design (`research/experiments/pc-r7/`), FM80 protocol (`research/experiments/`), tagging rule "
  f"`SD80_PC_R7_OBLIGATION_PROVENANCE_TAGGING_RULE_V1.md` (sha256 `{r['frozen_inputs']['tagging_rule_sha256'][:16]}…`), "
  f"cases file sha256 `{r['frozen_inputs']['cases_file_sha256'][:16]}…`, hidden-key file sha256 `{r['frozen_inputs']['hidden_keys_file_sha256'][:16]}…`.")
L("")
L(f"## Terminal: `{r['sufficiency']['verdict']}`")
L("")
for reason in r["sufficiency"]["reasons"]:
    L(f"- {reason}")
if not r["sufficiency"]["reasons"]:
    L("- all PC-R7 §1 population conditions met")
L("")
L("## 1. Lawful public witness sources")
L("")
L("| Domain | Class | Source (public, no auth) | Witness class | Raw records | PC-R7-eligible |")
L("|---|---|---|---|---|---|")
dc = r["domain_counts_raw"]
cls = {"PSYCHOLOGY_RPP": "empirical", "CANCER_BIOLOGY_RPCB": "empirical", "FORMAL_MATHEMATICS_1000PLUS": "formal", "MACHINE_LEARNING_MLRC": "empirical/computational"}
for d, s in r["sources"].items():
    L(f"| `{d}` | {cls[d]} | {s['lawful_source']} | `{s['witness_class']}` | {dc[d]['records']} | {dc[d]['pc_r7_eligible']} |")
L("")
L("MLRC is recorded but **not counted**: " + r["sources"]["MACHINE_LEARNING_MLRC"]["status"] + ".")
L("")
L("Source snapshots with sha256 live in `research/experiments/sd80/sources/raw/` (manifest in the cases JSON). "
  "Every case record and every hidden key is sha256-hashed (`record_sha256`, `hidden_key_sha256`); the hidden-key file "
  "`SD80_CASE_MATRIX_HIDDEN_KEYS_V1.json` carries verdicts/outcomes and is never mounted in a tagger or arm workspace.")
L("")
L("## 2. FM80 eligibility and remoteness")
L("")
L(r["fm80_eligibility_note"])
L("")
L("## 3. GN0 — tagging calibration (two independent fresh-context taggers)")
L("")
L(f"- Calibration set: {gn0['n_cases']} cases (seeded; 7 RP:P, 7 RP:CB, 6 formal). Agreement **{gn0['n_agree']}/{gn0['n_cases']} = {gn0['agreement_rate']:.2f}** "
  f"(threshold {gn0['gn0_threshold']}) → GN0 **{'PASS' if gn0['gn0_pass'] else 'FAIL'}**.")
L(f"- Tag counts A: {gn0['tag_counts']['A']}; B: {gn0['tag_counts']['B']}.")
L(f"- Disagreements: {len(gn0['disagreements'])}. Rule clarified to V1.1 on three ambiguities both taggers raised independently "
  "(per-registration withdrawal reading; accepted+linked Registered Report governs; formal enwiki entry must name the theorem or its object). Semantics unchanged.")
L("")
L("## 4. Full tagging round (all PC-R7-eligible cases in the tagging pool)")
L("")
L("| Domain | Eligible | Tagging pool | Tagged | A/B agreement | EXTERNAL_VERIFIABLE | INTERNAL | both ≥ 15 |")
L("|---|---|---|---|---|---|---|---|")
for d, v in ft.items():
    ar = v["full_round_agreement_rate"]
    L(f"| `{d}` | {v['pc_r7_eligible_cases']} | {v['tagging_pool']} | {v['tagged']} | {ar:.3f} | {v['tag_counts']['EXTERNAL_VERIFIABLE']} | {v['tag_counts']['INTERNAL']} | {'yes' if v['both_tags_ge_15'] else '**no**'} |" if ar is not None else f"| `{d}` | {v['pc_r7_eligible_cases']} | {v['tagging_pool']} | {v['tagged']} | n/a | – | – | no |")
L("")
L(f"Cross-tagger disagreements in the full round: {len(r['full_tagging']['disagreements'])}; untagged: {r['full_tagging']['n_untagged']}. "
  "Formal domain tagged on a frozen seeded 60-case sample of the 243 eligible entries (remainder `ELIGIBLE_UNTAGGED_RESERVE`).")
L("")
L("## 5. Reading")
L("")
L("Under the frozen PC-R7 §1 semantics, every registered-replication-verdict-class case is, by construction of the witness "
  "sources, externally constrained: RP:P cases carry an OSF registration, RP:CB cases a peer-reviewed eLife Registered Report, "
  "and formal cases an externally authored theorem statement. The `INTERNAL` stratum is therefore empty (or a single unverifiable "
  "record) in every domain, and the PC-R7 pre-registered population condition (both tags ≥ 15 cases/domain) cannot be met from "
  "these sources. Per PC-R7 §6 this is the contraction terminal `INSUFFICIENT_ELIGIBLE_NATURALISTIC_CASES` — a registered result, "
  "not a defect: the naturalistic obligation cell cannot test theory A's internal-vs-external contrast because naturalistic "
  "witness sources with verifiable outcomes do not supply an internally-constrained stratum. No arm was run; no outcome was read by "
  "any tagger or arm.")
L("")
L("## 6. Custody")
L("")
L("- Intake scripts: `scripts/sd80_case_matrix_intake.py`, `scripts/sd80_case_matrix_finalize.py`, `scripts/sd80_case_matrix_render_md.py`; custody tests `tests/unit/test_sd80_case_matrix_intake.py`.")
L("- Tagger outputs: `research/experiments/sd80/tagging/` (calibration + full round, both taggers, GN0 receipt, final merged tags).")
L("- Authority: grants no claim; no arm run; scientific truth not authorized.")
L("")
(OUT / "SD80_CASE_MATRIX_INTAKE_V1.md").write_text("\n".join(lines))
print("rendered", len(lines), "lines")

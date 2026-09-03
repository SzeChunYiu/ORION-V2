#!/usr/bin/env python3
"""Prospective Revision Audit — frozen real-LLM runner, **Design V3** (issue #51).

Own copy.  This file is NOT the V1/V2 runner (``pra_real_llm_audit.py``) and never
imports from it: the V2 protected run is in flight under that file's frozen sha256,
and V3 must be able to change the probe without touching a sealed campaign.

Executes ``PRA_REAL_LLM_AUDIT_DESIGN_V3.json``.  Stages:

  generate-suite  write the frozen instance suite (dev / protected split) + sha256
  present-gate    linguistic-target surrogate log-probs and current-action decisions
  revision        common later evidence -> future action per representation condition
  probe           mass-mean linear probe for the dormant variable on every layer
  kv-channel      R2 text with retained R0 KV cache (Gate C)
  competence-gate dev split only: pre-registered GPC model-competence check
  certify         PRE-RUN, model-free: gate-clause coverage + label identifiability
  rollup          frozen statistics, gates, terminals, routing

What V3 repairs, and why (see PRA_GP2A_CONSTRUCT_VALIDITY_DIAGNOSIS_V1.md):

  * V1/V2 registered GP2a as "probe decodes support_source under R0 **and R3**
    (>= 0.80)" while the runner evaluated R0 only.  The R3 clause was never
    executed.  Implementing it verbatim would not have helped: the V1 probe label
    (A=1, B=0) is an index into the *generator's* source dict whose only textual
    footprint is the fixed roster order, and R3 carries no roster.  The clause was
    unsatisfiable in principle.  Two of GP2a's three clauses were, in the opposite
    direction, unfailable in principle.
  * V3 therefore does not "add the missing check".  It replaces the label with an
    attribute of the recorded basis that the text states wherever the basis is
    named, randomises roster/ledger order so no positional shortcut survives, and
    makes both properties machine-checkable BEFORE the run by two certificates that
    are themselves gates:

      LABEL IDENTIFIABILITY  no two capture units with identical condition text may
                             carry different labels, and the label must transform
                             consistently under every registered generator symmetry.
                             A condition that fails is reported
                             LABEL_NOT_IDENTIFIABLE_FROM_CONDITION and never as an
                             accuracy.
      CLAUSE COVERAGE        every registered gate clause id must map to an
                             implementing predicate that actually evaluated on
                             non-null inputs, AND each clause must be *reachable*:
                             this run's inputs must admit both outcomes.  A clause
                             that is unimplemented, unevaluated or unfailable is a
                             hard terminal, never a pass on the half that ran.

  * The alternate-channel measurement is additionally reported against a model-free
    SURFACE NULL (lexical and relational readers on the same stimuli and the same
    frozen split), so a probe accuracy that a non-semantic reader also achieves is
    reported as such instead of as evidence about the model's representation.

Exit codes are distinct so "could not check" is never read as "checked and fine":

  0  every registered gate evaluated; outcome recorded (pass or registered negative)
  3  a registered clause could not be checked (CANNOT_CHECK); no pass is implied
  4  a registered clause is unimplemented, unevaluated or unreachable (design defect)

The runner grants no scientific authority: gates and terminals are computed
mechanically from the frozen design and the protected split is never inspected by
this code beyond what the stage needs.  ``--backend stub`` exercises every stage
without any model download (unit tests); ``--backend hf`` is the real run.

Only the Python standard library is required for ``stub``, ``certify`` and
``rollup``.  ``torch``/``transformers`` are imported lazily for ``--backend hf``.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import random
import re
import sys
import time
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable

DESIGN_SCHEMA_V3 = "orion.v2.pra.real-llm-audit-design.v3"
DESIGN_SCHEMAS = (DESIGN_SCHEMA_V3,)
SUITE_SCHEMA = "orion.v2.pra.real-llm-audit-suite.v3"
RESULT_SCHEMA = "orion.v2.pra.real-llm-audit-stage-result.v3"
ROLLUP_SCHEMA = "orion.v2.pra.real-llm-audit-rollup.v3"

ACTIONS = ("RETAIN", "REOPEN", "ESCALATE")
CONDITIONS = ("R0", "R1", "R2", "R3", "R4")
# V3 drops R2_TRUE_REMOVAL: the V1 receipt proved hidden_R2.npy and
# hidden_R2_TRUE_REMOVAL.npy byte-identical, because "fresh cache, R2 text only" IS
# the R2 computation.  Keeping it would report one measurement twice.  Its role (the
# removal limb of GP2a) is discharged a priori by the identifiability certificate.
KV_CONDITIONS = ("R2_TEXT_REMOVED_KV_RETAINED",)
FAMILIES = (
    "F0_ACQ",
    "F1_P0",
    "F2_P1",
    "F3_P2_CANON",
    "F3_P2_MIRROR",
    "F3_P2_INDEP",
    "F3_P2_RECON",
    "F3_P2_TIE",
    "F3_P2_CANON_SF",  # design V2 registered secondary family (H-EXT-4 same-successor-fibre variant)
)
HERE = Path(__file__).resolve().parent
DEFAULT_DESIGN = HERE / "PRA_REAL_LLM_AUDIT_DESIGN_V1.json"

FILLER_LINE = "Filler line: this line is intentionally uninformative and must be ignored."

CONTRACT_TEXT = (
    "You are auditing a scientific claim registry under a fixed responsibility contract.\n"
    "Contract actions:\n"
    "- RETAIN: keep the claim's accepted status. Correct when the source(s) recorded as the basis for the "
    "claim remain valid, or when at least one recorded independently sufficient basis remains valid.\n"
    "- REOPEN: withdraw the claim's accepted status. Correct when the source recorded as the basis for the "
    "claim has been retracted, withdrawn or otherwise invalidated and no other recorded sufficient basis "
    "remains, or when the claim itself has been directly refuted.\n"
    "- ESCALATE: refer the claim for review. Correct when the available record does not allow you to "
    "determine whether the recorded basis remains valid (for example the record does not identify which "
    "source is the basis, or a source is under investigation but not retracted).\n"
    "Notices about sources that are not the recorded basis for this claim do not change its status.\n"
    "Reason briefly (at most three sentences) using only the record and any new evidence given, then finish "
    "with a final line of the exact form 'Answer: RETAIN', 'Answer: REOPEN' or 'Answer: ESCALATE'."
)


# --------------------------------------------------------------------------- utils

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _json_clean(obj: Any) -> Any:
    """Replace non-finite floats with None so every artefact is strict JSON."""
    if isinstance(obj, float):
        return obj if math.isfinite(obj) else None
    if isinstance(obj, dict):
        return {k: _json_clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_clean(v) for v in obj]
    return obj


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_json_clean(obj), indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_design(path: Path) -> dict:
    design = read_json(path)
    if design.get("schema_version") not in DESIGN_SCHEMAS:
        raise SystemExit(f"design schema mismatch: {design.get('schema_version')!r} (accepted: {DESIGN_SCHEMAS})")
    return design


def rollup_basename(design: dict) -> str:
    """Rollup file stem: V1 designs keep the historical name; V2 designs write a V2 rollup."""
    return "PRA_REAL_LLM_AUDIT_ROLLUP_V3"


def resolve_split_seed(design: dict, split: str, protected_seed_file: str | None) -> int | None:
    """Seed for a split. A V2 design may seal the protected seed: the design carries only
    ``seed.protected_commitment_sha256`` and the seed file (``<int>:<salt>``) must hash to it."""
    seeds = design["suite_generator"]["seed"]
    if split in seeds:
        return int(seeds[split])
    commitment = seeds.get(f"{split}_commitment_sha256")
    if not commitment:
        raise SystemExit(f"design has neither a plain seed nor a commitment for split {split!r}")
    if not protected_seed_file:
        return None  # sealed and not supplied: the split cannot be generated
    p = Path(protected_seed_file)
    digest = sha256_file(p)
    if digest != commitment:
        raise SystemExit(f"sealed seed file sha256 {digest} does not match the design commitment {commitment}")
    return int(p.read_text(encoding="utf-8").strip().split(":", 1)[0])


# --------------------------------------------------------------------------- suite generation

DOMAINS = [
    {
        "domain": "materials",
        "claim": "doping {material} with {agent} raises its {property} by at least {n} percent",
        "material": ["a layered nickelate", "a perovskite oxide", "a bismuth telluride film", "a zirconia ceramic"],
        "agent": ["strontium", "lanthanum", "niobium", "gallium"],
        "property": ["thermal conductivity", "fracture toughness", "ionic conductivity", "Seebeck coefficient"],
    },
    {
        "domain": "ecology",
        "claim": "{organism} density in {habitat} declines by at least {n} percent after {agent}",
        "organism": ["mayfly larva", "bank vole", "tree-frog", "mussel"],
        "habitat": ["upland streams", "riparian meadows", "coastal lagoons", "boreal bogs"],
        "agent": ["canopy thinning", "a single dry summer", "road-salt runoff", "beaver re-introduction"],
    },
    {
        "domain": "epidemiology",
        "claim": "{exposure} is associated with at least a {n} percent increase in {outcome} incidence",
        "exposure": ["night-shift work", "indoor biomass smoke", "long-term proton-pump inhibitor use", "urban noise above 65 dB"],
        "outcome": ["atrial fibrillation", "adult-onset asthma", "chronic kidney disease", "gallstone"],
    },
    {
        "domain": "astronomy",
        "claim": "{object} shows a periodic {signal} with period near {n} days",
        "object": ["the brown dwarf pair catalogued in the survey", "the hot-Jupiter host star", "the recurrent nova candidate", "the polar ring galaxy nucleus"],
        "signal": ["radio flux modulation", "H-alpha equivalent-width variation", "transit-timing shift", "X-ray dip"],
    },
    {
        "domain": "neuroscience",
        "claim": "{intervention} reduces {measure} in {population} by at least {n} percent",
        "intervention": ["twenty-minute slow-wave audio stimulation", "low-dose lithium", "aerobic interval training", "vagus-nerve cuff stimulation"],
        "measure": ["cortical spreading-depression frequency", "hippocampal theta-gamma coupling loss", "reaction-time variability", "REM fragmentation"],
        "population": ["adult migraine patients", "aged rats", "shift workers", "juvenile zebrafish"],
    },
    {
        "domain": "economics",
        "claim": "{policy} lowers {outcome} in {region} by at least {n} percent",
        "policy": ["a municipal vacancy tax", "conditional cash transfer", "an apprenticeship subsidy", "congestion pricing"],
        "outcome": ["long-term rental vacancy", "youth unemployment duration", "informal-sector share", "peak-hour traffic volume"],
        "region": ["mid-sized port cities", "rural districts", "island economies", "post-industrial regions"],
    },
    {
        "domain": "microbiology",
        "claim": "{strain} loses {trait} within {n} generations under {condition}",
        "strain": ["the marine cyanobacterium isolate", "the soil actinomycete strain", "the gut Bacteroides isolate", "the halophilic archaeon"],
        "trait": ["plasmid-borne antibiotic resistance", "phage immunity", "nitrogen fixation", "biofilm formation"],
        "condition": ["phosphate starvation", "continuous light", "sub-inhibitory copper", "elevated salinity"],
    },
    {
        "domain": "geoscience",
        "claim": "{process} increases {quantity} at {site} by at least {n} percent",
        "process": ["permafrost thaw", "reservoir impoundment", "tidal-flat restoration", "glacier retreat"],
        "quantity": ["methane efflux", "micro-seismicity rate", "sediment accretion", "downstream turbidity"],
        "site": ["the sub-Arctic lowlands", "the intramontane basin", "the estuary margin", "the alpine forefield"],
    },
]

_SYLLABLES_A = ["Var", "Kel", "Dro", "Mel", "Tor", "Ash", "Bren", "Cal", "Fen", "Gal", "Hol", "Ith", "Jor", "Lum", "Nor", "Orn", "Pel", "Rus", "Sel", "Ul"]
_SYLLABLES_B = ["len", "mar", "vik", "dan", "sen", "ric", "thal", "wyn", "dor", "mund", "bek", "stad", "quist", "ver", "lin", "ton", "gard", "holm", "berg", "wick"]
_REGISTRIES = ["SRR", "CRX", "OSL", "TRK", "QDB", "MRG"]
# V3: the registry prefix of the recorded basis carries the probe label.  Two disjoint,
# equal-size classes; the distractor Z draws from the full pool, so the class of a
# non-basis source is uninformative.
_REGISTRY_CLASS_1 = ["SRR", "CRX", "OSL"]
_REGISTRY_CLASS_0 = ["TRK", "QDB", "MRG"]


def _nonce_source(rng: random.Random) -> dict:
    surname = rng.choice(_SYLLABLES_A) + rng.choice(_SYLLABLES_B)
    year = rng.randint(2009, 2024)
    reg = rng.choice(_REGISTRIES)
    code = "".join(rng.choice("0123456789abcdef") for _ in range(4))
    return {"name": f"the {surname} {year} report", "id": f"{reg}-{code}"}


def _claim(rng: random.Random) -> dict:
    spec = rng.choice(DOMAINS)
    slots = {k: rng.choice(v) for k, v in spec.items() if isinstance(v, list)}
    slots["n"] = str(rng.choice([8, 12, 15, 20, 25, 30, 40]))
    text = spec["claim"].format(**slots)
    claim_id = "CL-" + "".join(rng.choice("0123456789abcdef") for _ in range(4))
    return {"claim_id": claim_id, "claim_text": text, "domain": spec["domain"]}


def _history_lines(claim: dict, sources: dict, support: list[str], extra: list[str], order: list[str] | None = None) -> list[str]:
    """R0 full history: a registry record with the support relation stated once, plus noise."""
    order = order or ["A", "B", "Z"]
    lines = [
        f"Registry record for claim {claim['claim_id']} (domain: {claim['domain']}).",
        f"Claim text: {claim['claim_text']}.",
        "Sources on file: " + ", ".join(f"{sources[k]['name']} [{sources[k]['id']}]" for k in order) + ".",
    ]
    if support == ["A"]:
        lines.append(f"Support entry: claim {claim['claim_id']} is accepted on the basis of {sources['A']['name']} [{sources['A']['id']}] alone. No other source on file is recorded as a basis for this claim.")
    elif support == ["B"]:
        lines.append(f"Support entry: claim {claim['claim_id']} is accepted on the basis of {sources['B']['name']} [{sources['B']['id']}] alone. No other source on file is recorded as a basis for this claim.")
    elif support == ["A", "B"]:
        lines.append(
            f"Support entry: claim {claim['claim_id']} is accepted on the basis of {sources['A']['name']} [{sources['A']['id']}] and, independently and sufficiently, {sources['B']['name']} [{sources['B']['id']}]. No other source on file is recorded as a basis for this claim."
        )
    elif support == ["A?B"]:
        lines.append(
            f"Support entry: claim {claim['claim_id']} is accepted on the basis of one of {sources['A']['name']} [{sources['A']['id']}] or {sources['B']['name']} [{sources['B']['id']}]; the record does not state which."
        )
    lines.append(f"Note: {sources['Z']['name']} [{sources['Z']['id']}] is filed under a different claim and is not cited for {claim['claim_id']}.")
    lines.extend(extra)
    lines.append(f"Registry status line: Claim {claim['claim_id']} is currently listed as SUPPORTED.")
    return lines


def _history_lines_ordered(claim: dict, sources: dict, order: list[str], support: list[str], extra: list[str]) -> list[str]:
    """V3: R0 history rendered in the instance's frozen presentation order."""
    return _history_lines(claim, sources, support, extra, order)


def _arm(arm_id: str, lines: list[str], vars_: dict, evidence: str, current: list[str], future: list[str], klass: str) -> dict:
    return {
        "arm_id": arm_id,
        "history_lines": lines,
        "state_vars": vars_,
        "evidence_text": evidence,
        "current_gold": {"acceptable": sorted(current)},
        "future_gold": {"acceptable": sorted(future)},
        "update_or_maintain_class": klass,
    }


def build_instance(family: str, index: int, rng: random.Random, split: str) -> dict:
    claim = _claim(rng)
    sources = {"A": _nonce_source(rng), "B": _nonce_source(rng), "Z": _nonce_source(rng)}
    while len({sources[k]["name"] for k in sources}) < 3:
        # Regenerate the colliding source. V1 regenerated Z unconditionally, which never terminates when
        # A and B collide (P ~ 1/6400 per instance; latent in V1, never triggered by V1's frozen seeds:
        # the V1 suites are pinned byte-identical in the unit tests). Seeds on which V1 terminated
        # consume randomness identically here, because only the A==B branch is new.
        if sources["B"]["name"] == sources["A"]["name"]:
            sources["B"] = _nonce_source(rng)
        else:
            sources["Z"] = _nonce_source(rng)
    # ---- V3 probe label: the registry class of the *recorded basis*.
    # V1's label was `support_source (A=1, B=0)` -- an index into this dict, not a property
    # of anything the model reads.  R3 names the basis but carries no roster, so the A/B
    # index left no textual trace there and the registered "decodes under R3 >= 0.80" clause
    # was unsatisfiable in principle (diagnosis V1 sections 4-5).  The V3 label is an
    # attribute the text states wherever the basis is named: identifiable from R0 and R3,
    # absent from R2, and invariant to presentation order.
    # Balance is by construction, not by luck: within each instance exactly one of A, B is
    # in class 1, so every instance contributes one unit of each class to the probe and the
    # test split is exactly 50/50 regardless of where it is cut.
    if index % 2 == 0:
        sources["A"]["id"] = _REGISTRY_CLASS_1[index % len(_REGISTRY_CLASS_1)] + sources["A"]["id"][3:]
        sources["B"]["id"] = _REGISTRY_CLASS_0[index % len(_REGISTRY_CLASS_0)] + sources["B"]["id"][3:]
    else:
        sources["A"]["id"] = _REGISTRY_CLASS_0[index % len(_REGISTRY_CLASS_0)] + sources["A"]["id"][3:]
        sources["B"]["id"] = _REGISTRY_CLASS_1[index % len(_REGISTRY_CLASS_1)] + sources["B"]["id"][3:]

    # ---- V3: randomised presentation order of the source roster / dependency ledger.
    # V1 always listed A, B, Z in that order, which made "is the recorded basis the FIRST
    # name on file?" a sufficient rule for the V1 probe label -- a positional shortcut that
    # scored 1.000 on R0 with no understanding of the word "basis" (diagnosis V1 section 5).
    # The order is drawn here, stored in the instance, and is therefore part of the frozen
    # suite: rendering stays a pure function of the suite.
    roster_order = ["A", "B", "Z"]
    rng.shuffle(roster_order)

    A, Z = sources["A"], sources["Z"]
    cid = claim["claim_id"]
    retract_A = f"Retraction notice: {A['name']} [{A['id']}] has been retracted by its publisher; its findings are no longer valid support for any claim."
    retract_Z = f"Retraction notice: {Z['name']} [{Z['id']}] has been retracted by its publisher; its findings are no longer valid support for any claim."
    refute = f"Replication notice: an independent pre-registered replication of claim {cid} failed decisively; the registry treats the claim as directly refuted regardless of its recorded sources."
    neutral = f"Administrative notice: the registry has migrated claim {cid} to the new identifier format; no source or status information has changed."
    concern = f"Expression of concern: the publisher of {A['name']} [{A['id']}] has issued an expression of concern; the report is under investigation but has not been retracted."
    dormant = "support_source"
    arms: list[dict] = []

    if family == "F3_P2_CANON":
        arms = [
            _arm("hA", _history_lines_ordered(claim, sources, roster_order, ["A"], []), {"support_set": ["A"]}, retract_A, ["RETAIN"], ["REOPEN"], "UPDATE_REQUIRED"),
            _arm("hB", _history_lines_ordered(claim, sources, roster_order, ["B"], []), {"support_set": ["B"]}, retract_A, ["RETAIN"], ["RETAIN"], "MAINTAIN_REQUIRED"),
        ]
    elif family == "F3_P2_CANON_SF":
        # H-EXT-4 same-successor-fibre variant (design V2): identical evidence, identical successor
        # linguistic target in both arms (the registry flags every claim whose file lists A, whatever
        # the action), so the two successors sit in ONE predictive fibre and the R2/R3 gap is
        # decision-driven only. Gold actions are exactly those of F3_P2_CANON.
        retract_A_sf = (
            retract_A
            + f" Registry policy notice: because {A['name']} [{A['id']}] appears on the file of claim {cid}, "
            f"the registry status line for claim {cid} now reads 'Claim {cid} is currently listed as FLAGGED.' "
            "for every claim listing that source; the flag is an administrative marker, it is applied whether "
            "or not the retracted source is the recorded basis, and it does not by itself change the claim's "
            "accepted status under the contract."
        )
        arms = [
            _arm("hA", _history_lines_ordered(claim, sources, roster_order, ["A"], []), {"support_set": ["A"]}, retract_A_sf, ["RETAIN"], ["REOPEN"], "UPDATE_REQUIRED"),
            _arm("hB", _history_lines_ordered(claim, sources, roster_order, ["B"], []), {"support_set": ["B"]}, retract_A_sf, ["RETAIN"], ["RETAIN"], "MAINTAIN_REQUIRED"),
        ]
        for arm in arms:
            arm["successor_linguistic_target"] = {"protocol_rho": "registry_status_line", "continuation": f"Claim {cid} is currently listed as FLAGGED.", "same_fibre_across_arms": True}
    elif family == "F3_P2_MIRROR":
        arms = [
            _arm("hA", _history_lines_ordered(claim, sources, roster_order, ["A"], []), {"support_set": ["A"]}, retract_Z, ["RETAIN"], ["RETAIN"], "MAINTAIN_REQUIRED"),
            _arm("hB", _history_lines_ordered(claim, sources, roster_order, ["B"], []), {"support_set": ["B"]}, retract_Z, ["RETAIN"], ["RETAIN"], "MAINTAIN_REQUIRED"),
        ]
    elif family == "F3_P2_INDEP":
        arms = [
            _arm("hAB", _history_lines_ordered(claim, sources, roster_order, ["A", "B"], []), {"support_set": ["A", "B"]}, retract_A, ["RETAIN"], ["RETAIN"], "MAINTAIN_REQUIRED"),
            _arm("hA", _history_lines_ordered(claim, sources, roster_order, ["A"], []), {"support_set": ["A"]}, retract_A, ["RETAIN"], ["REOPEN"], "UPDATE_REQUIRED"),
        ]
        dormant = "support_set"
    elif family == "F3_P2_RECON":
        ev_A = retract_A + f" Registry annotation: {A['name']} [{A['id']}] was the sole recorded basis for claim {cid}."
        ev_B = retract_A + f" Registry annotation: {A['name']} [{A['id']}] was not among the recorded bases for claim {cid}."
        arms = [
            _arm("hA", _history_lines_ordered(claim, sources, roster_order, ["A"], []), {"support_set": ["A"]}, ev_A, ["RETAIN"], ["REOPEN"], "UPDATE_REQUIRED"),
            _arm("hB", _history_lines_ordered(claim, sources, roster_order, ["B"], []), {"support_set": ["B"]}, ev_B, ["RETAIN"], ["RETAIN"], "MAINTAIN_REQUIRED"),
        ]
    elif family == "F3_P2_TIE":
        arms = [
            _arm("hA", _history_lines_ordered(claim, sources, roster_order, ["A"], []), {"support_set": ["A"]}, concern, ["RETAIN"], ["ESCALATE", "REOPEN"], "UPDATE_OR_ESCALATE"),
            _arm("hB", _history_lines_ordered(claim, sources, roster_order, ["B"], []), {"support_set": ["B"]}, concern, ["RETAIN"], ["RETAIN", "ESCALATE"], "MAINTAIN_OR_ESCALATE"),
        ]
    elif family == "F1_P0":
        if index % 2 == 0:
            arms = [
                _arm("hA", _history_lines_ordered(claim, sources, roster_order, ["A"], []), {"support_set": ["A"]}, refute, ["RETAIN"], ["REOPEN"], "UPDATE_REQUIRED"),
                _arm("hB", _history_lines_ordered(claim, sources, roster_order, ["B"], []), {"support_set": ["B"]}, refute, ["RETAIN"], ["REOPEN"], "UPDATE_REQUIRED"),
            ]
        else:
            arms = [
                _arm("hA", _history_lines_ordered(claim, sources, roster_order, ["A"], []), {"support_set": ["A"]}, neutral, ["RETAIN"], ["RETAIN"], "MAINTAIN_REQUIRED"),
                _arm("hB", _history_lines_ordered(claim, sources, roster_order, ["B"], []), {"support_set": ["B"]}, neutral, ["RETAIN"], ["RETAIN"], "MAINTAIN_REQUIRED"),
            ]
    elif family == "F2_P1":
        withdrawal = f"Withdrawal notice on file: the dataset underlying {A['name']} [{A['id']}] was withdrawn by its authors; the support recorded for claim {cid} is defeated. The registry status line has not yet been updated."
        arms = [
            _arm("hValid", _history_lines_ordered(claim, sources, roster_order, ["A"], []), {"support_set": ["A"], "current_defeat": False}, neutral, ["RETAIN"], ["RETAIN"], "MAINTAIN_REQUIRED"),
            _arm("hDefeated", _history_lines_ordered(claim, sources, roster_order, ["A"], [withdrawal]), {"support_set": ["A"], "current_defeat": True}, neutral, ["REOPEN"], ["REOPEN"], "CURRENT_UPDATE_REQUIRED"),
        ]
        dormant = "current_defeat"
    elif family == "F0_ACQ":
        arms = [
            _arm("hA_hidden", _history_lines_ordered(claim, sources, roster_order, ["A?B"], []), {"support_set": ["A"], "record_identifies_support": False}, retract_A, ["RETAIN"], ["ESCALATE"], "ACQUISITION_LIMIT"),
            _arm("hB_hidden", _history_lines_ordered(claim, sources, roster_order, ["A?B"], []), {"support_set": ["B"], "record_identifies_support": False}, retract_A, ["RETAIN"], ["ESCALATE"], "ACQUISITION_LIMIT"),
        ]
        dormant = "support_source_unrecorded"
    else:
        raise ValueError(family)

    return {
        "instance_id": f"{family}-{split}-{index:04d}",
        "family": family,
        "split": split,
        "index": index,
        "domain": claim["domain"],
        "claim_id": cid,
        "claim_text": claim["claim_text"],
        "sources": sources,
        "roster_order": roster_order,
        "dormant_variable": dormant,
        "linguistic_target": {
            "protocol_rho": "registry_status_line",
            "continuation": f"Claim {cid} is currently listed as SUPPORTED.",
        },
        "arms": arms,
    }


def generate_suite(design: dict, split: str, scale: int | None = None, seed: int | None = None) -> dict:
    gen = design["suite_generator"]
    if seed is None:
        seed = resolve_split_seed(design, split, None)
        if seed is None:
            raise SystemExit(f"split {split!r} has a sealed seed; pass --protected-seed-file to generate it")
    counts = dict(gen["instances_per_family"][split])
    unknown = set(counts) - set(FAMILIES)
    if unknown:
        raise SystemExit(f"design lists unknown families: {sorted(unknown)}")
    if scale is not None:
        if split != "dev":
            raise SystemExit("instance-count override is permitted for the dev split only")
        counts = {k: scale for k in counts}
    rng = random.Random(seed)
    instances = []
    # Families absent from the design are skipped without consuming randomness, so a V1 design
    # renders byte-identical suites whether or not later families exist in FAMILIES.
    for family in FAMILIES:
        for index in range(counts.get(family, 0)):
            instances.append(build_instance(family, index, rng, split))
    return {
        "schema_version": SUITE_SCHEMA,
        "design_id": design["design_id"],
        "split": split,
        "generator_seed": seed,
        "instances_per_family": counts,
        "n_instances": len(instances),
        "instances": instances,
    }


# --------------------------------------------------------------------------- rendering

def support_phrase(inst: dict, arm: dict) -> str:
    s = inst["sources"]
    ss = arm["state_vars"]["support_set"]
    if arm["state_vars"].get("record_identifies_support") is False:
        return f"one of {s['A']['name']} [{s['A']['id']}] or {s['B']['name']} [{s['B']['id']}] (record does not state which)"
    if ss == ["A", "B"]:
        return f"{s['A']['name']} [{s['A']['id']}] and, independently and sufficiently, {s['B']['name']} [{s['B']['id']}]"
    k = ss[0]
    return f"{s[k]['name']} [{s[k]['id']}] alone"


def render_state(inst: dict, arm: dict, condition: str) -> str:
    """Pre-evidence representation state text for a condition (no padding)."""
    cid = inst["claim_id"]
    s = inst["sources"]
    defeated = bool(arm["state_vars"].get("current_defeat"))
    validity = "DEFEATED (a withdrawal notice is on file for the recorded supporting source; the status line has not yet been updated)" if defeated else "VALID"
    order = inst.get("roster_order", ["A", "B", "Z"])
    roster = "Sources on file: " + ", ".join(f"{s[k]['name']} [{s[k]['id']}]" for k in order) + "."
    status = f"Registry status line: Claim {cid} is currently listed as SUPPORTED."
    if condition == "R0":
        return "Record history (complete):\n" + "\n".join(f"{i + 1}. {line}" for i, line in enumerate(arm["history_lines"]))
    if condition == "R1":
        return (
            "Record summary (prediction-preserving):\n"
            f"Claim {cid} (domain: {inst['domain']}): {inst['claim_text']}.\n"
            f"{roster}\n{status}"
        )
    base = (
        "Record state (current-decision-sufficient):\n"
        f"Claim {cid} (domain: {inst['domain']}): {inst['claim_text']}.\n"
        f"Current support validity: {validity}.\n{status}"
    )
    if condition == "R2":
        return base
    if condition == "R3":
        unrec = arm["state_vars"].get("record_identifies_support") is False
        tail = "" if unrec else " No other source is recorded as a basis for this claim."
        return base + f"\nRecorded basis for claim {cid}: {support_phrase(inst, arm)}.{tail}"
    if condition == "R4":
        ss = arm["state_vars"]["support_set"]
        unrec = arm["state_vars"].get("record_identifies_support") is False
        rows = []
        for k in order:
            if unrec and k in ("A", "B"):
                role = f"possible sole basis for {cid} (record ambiguous between A and B)"
            elif k in ss and len(ss) == 2:
                role = f"independently sufficient basis for {cid}"
            elif k in ss:
                role = f"sole basis for {cid}"
            else:
                role = f"not cited for {cid}"
            rows.append(f"- {s[k]['name']} [{s[k]['id']}]: {role}")
        return base + "\nDependency ledger (every recorded source and its role for this claim):\n" + "\n".join(rows)
    raise ValueError(condition)


FILLER_TOKEN = " ignore"


def pad_state(state: str, target_tokens: int, count_tokens, tolerance: int) -> tuple[str, int, int]:
    """Append frozen filler until the token count reaches target (whole lines, then single-word top-up)."""
    n = count_tokens(state)
    if n >= target_tokens:
        return state, n, 0
    text = state + "\nPadding block (uninformative):"
    added = 0
    line_cost = count_tokens(text + "\n" + FILLER_LINE) - count_tokens(text)
    while count_tokens(text) + line_cost <= target_tokens and added < 400:
        text += "\n" + FILLER_LINE
        added += 1
    guard = 0
    while count_tokens(text) < target_tokens and guard < 64:
        text += FILLER_TOKEN
        guard += 1
    return text, count_tokens(text), added


def build_messages(state_text: str, mode: str, evidence: str | None, cid: str) -> list[dict]:
    if mode == "status_line":
        user = (
            f"{state_text}\n\n"
            f"Task: write the registry status line for claim {cid} in the standard format "
            f"'Claim <id> is currently listed as <STATUS>.' and nothing else."
        )
    elif mode == "current_action":
        user = f"{CONTRACT_TEXT}\n\n{state_text}\n\nQuestion: Under the contract, what is the correct action for claim {cid} right now?"
    elif mode == "future_action":
        user = (
            f"{CONTRACT_TEXT}\n\n{state_text}\n\nNew evidence received after the record above:\n{evidence}\n\n"
            f"Question: Under the contract, what is the correct action for claim {cid} now, given the new evidence?"
        )
    else:
        raise ValueError(mode)
    return [{"role": "user", "content": user}]


def parse_action(text: str) -> str:
    """Registered extraction: the LAST 'Answer: <ACTION>' line; fallback = last bare action word."""
    up = text.upper()
    answers = re.findall(r"ANSWER\s*[:\-]?\s*\**\s*(RETAIN|REOPEN|ESCALATE)", up)
    if answers:
        return answers[-1]
    words = re.findall(r"\b(RETAIN|REOPEN|ESCALATE)\b", up)
    return words[-1] if words else "UNPARSEABLE"


# --------------------------------------------------------------------------- backends

class Backend:
    name = "abstract"

    def count_tokens(self, text: str) -> int:
        raise NotImplementedError

    def generate(self, messages: list[dict], max_new_tokens: int) -> str:
        raise NotImplementedError

    def continuation_logprob(self, messages: list[dict], continuation: str) -> dict:
        raise NotImplementedError

    def hidden_states(self, messages: list[dict]) -> list[list[float]]:
        raise NotImplementedError

    def generate_with_retained_prefix(self, prefix_text: str, messages: list[dict], max_new_tokens: int) -> str:
        raise NotImplementedError

    def hidden_states_with_retained_prefix(self, prefix_text: str, messages: list[dict]) -> list[list[float]]:
        raise NotImplementedError

    def describe(self) -> dict:
        return {"backend": self.name}


class StubBackend(Backend):
    """Deterministic pure-Python stand-in used by unit tests.

    ``planted``: reads the visible text like an ideal contract-follower (R3/R0/KV-retained
    succeed, R2 must guess) -> must trip GP1.
    ``null``: answers RETAIN everywhere -> must not trip GP1.
    Hidden states carry a planted direction for the support source whenever the visible
    text names the recorded support, so the probe decodes it under R0/R3/KV-retained and is at
    chance under R2.  Unlike the V1 stub this is a genuine function of the rendered basis, so
    ``test_probe_decodes_under_R3`` can fail; the V1 stub made that test unwritable.
    """

    name = "stub"

    def __init__(self, variant: str = "planted", dim: int = 16, layers: int = 4):
        self.variant = variant
        self.dim = dim
        self.layers = layers

    def describe(self) -> dict:
        return {"backend": "stub", "variant": self.variant, "dim": self.dim, "layers": self.layers}

    def count_tokens(self, text: str) -> int:
        return len(text.split())

    @staticmethod
    def _user(messages: list[dict]) -> str:
        return "\n".join(m["content"] for m in messages)

    def _decide(self, text: str) -> str:
        if self.variant == "null":
            return "RETAIN"
        ev = ""
        if "New evidence received" in text:
            ev = text.split("New evidence received after the record above:\n", 1)[1].split("\n\nQuestion", 1)[0]
        if "Replication notice" in ev:
            return "REOPEN"
        if "DEFEATED" in text or "support recorded for claim" in text and "is defeated" in text:
            return "REOPEN"
        if "record does not state which" in text and ("Retraction notice" in ev or "Expression of concern" in ev):
            return "ESCALATE"
        m = re.search(r"Retraction notice: (the \w+ \d{4} report) \[([A-Z]{3}-[0-9a-f]{4})\]", ev)
        if m:
            sid = m.group(2)
            ann = re.search(r"Registry annotation: .*?\[([A-Z]{3}-[0-9a-f]{4})\] was (the sole recorded basis|not among the recorded bases)", ev)
            if ann:
                return "REOPEN" if ann.group(2).startswith("the sole") else "RETAIN"
            sup = re.search(r"(?:Support entry: claim \S+ is accepted on the basis of|Recorded basis for claim \S+:) (.*?)(?:\. No other|\.\n|\.$|\n)", text, re.S)
            ledger = re.findall(r"- the \w+ \d{4} report \[([A-Z]{3}-[0-9a-f]{4})\]: (possible sole basis|sole basis|independently sufficient basis|not cited)", text)
            if sup:
                phrase = sup.group(1)
                ids = re.findall(r"\[([A-Z]{3}-[0-9a-f]{4})\]", phrase)
                if sid in ids:
                    return "RETAIN" if "independently" in phrase else "REOPEN"
                return "RETAIN"
            if ledger:
                roles = dict(ledger)
                if roles.get(sid) == "possible sole basis":
                    return "ESCALATE"
                if roles.get(sid) == "sole basis":
                    return "REOPEN"
                return "RETAIN"
            return "RETAIN"  # R2 guess: information absent
        if "Expression of concern" in ev:
            return "ESCALATE"
        return "RETAIN"

    def generate(self, messages, max_new_tokens):
        text = self._user(messages)
        if "Task: write the registry status line" in text:
            m = re.search(r"Claim (CL-[0-9a-f]{4}) is currently listed as SUPPORTED", text)
            return f"Claim {m.group(1)} is currently listed as SUPPORTED." if m else "unknown"
        return f"The record settles it. Answer: {self._decide(text)}"

    def continuation_logprob(self, messages, continuation):
        text = self._user(messages)
        toks = continuation.split()
        base = -0.30 if "SUPPORTED" in text else -2.0
        jitter = (int(sha256_text(text)[:6], 16) % 1000) / 1_000_000.0
        per = [base + jitter for _ in toks]
        return {"mean_logprob": sum(per) / len(per), "sum_logprob": sum(per), "n_tokens": len(per)}

    def _vec(self, text: str) -> list[list[float]]:
        rng = random.Random(sha256_text(text))
        # V3: plant the direction of the REGISTRY CLASS OF THE RECORDED BASIS.
        # The V1 stub planted `1.0 if the basis is the FIRST name on file else -1.0`, i.e. it
        # implemented the very positional shortcut the probe turned out to be using -- and under
        # R3, where no roster exists, it planted a CONSTANT.  Its docstring nevertheless claimed
        # "the probe decodes it under R0/R3/KV-retained".  That sentence was never executed by
        # any test, which is why the R3 clause survived to a protected run.  The V3 stub plants
        # a signal that is a function of what the text says about the basis, so a test that
        # asserts R3 decodability can actually fail.
        support = None
        m = re.search(r"(?:Support entry: claim \S+ is accepted on the basis of|Recorded basis for claim \S+:) the \w+ \d{4} report \[([A-Z]{3})-[0-9a-f]{4}\]", text)
        if m and "record does not state which" not in text:
            support = 1.0 if m.group(1) in _REGISTRY_CLASS_1 else -1.0
        out = []
        for layer in range(self.layers + 1):
            v = [rng.gauss(0, 1) for _ in range(self.dim)]
            if support is not None and layer >= 2:
                v[0] += 3.0 * support
                v[1] -= 3.0 * support
            out.append(v)
        return out

    def hidden_states(self, messages):
        return self._vec(self._user(messages))

    def generate_with_retained_prefix(self, prefix_text, messages, max_new_tokens):
        return f"Answer: {self._decide(prefix_text + chr(10) + self._user(messages))}"

    def hidden_states_with_retained_prefix(self, prefix_text, messages):
        return self._vec(prefix_text + "\n" + self._user(messages))


class HFBackend(Backend):
    name = "hf"

    def __init__(self, model_id: str, revision: str | None, dtype: str = "bfloat16", device: str = "cuda", seed: int = 0):
        import torch  # noqa: F401
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.torch = torch
        self.model_id = model_id
        self.revision = revision
        torch.manual_seed(seed)
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
        load_kwargs: dict[str, Any] = dict(revision=revision, torch_dtype=getattr(torch, dtype), device_map=device)
        if device == "auto":
            # Layer-wise sharding across every visible GPU (e.g. 2x A100-40GB when no A100-80GB is free);
            # GPU-only placement is forced so accelerate never silently offloads layers to CPU.
            n_gpu = torch.cuda.device_count()
            per = int(torch.cuda.get_device_properties(0).total_memory * 0.92)
            load_kwargs["max_memory"] = {i: per for i in range(n_gpu)}
        self.model = AutoModelForCausalLM.from_pretrained(model_id, **load_kwargs)
        self.model.eval()
        self.device = self.model.device
        self.device_map = getattr(self.model, "hf_device_map", None)
        if self.device_map and any(str(v) in ("cpu", "disk") for v in self.device_map.values()):
            raise SystemExit(f"model sharding placed layers off-GPU: {self.device_map}")
        self.resolved_revision = getattr(self.model.config, "_commit_hash", None) or revision

    def describe(self) -> dict:
        import transformers

        return {
            "backend": "hf",
            "model_id": self.model_id,
            "revision_requested": self.revision,
            "revision_resolved": self.resolved_revision,
            "torch": self.torch.__version__,
            "transformers": transformers.__version__,
            "dtype": str(self.model.dtype),
            "device": str(self.device),
            "device_map": {str(k): str(v) for k, v in self.device_map.items()} if isinstance(self.device_map, dict) else None,
            "n_gpus_visible": int(self.torch.cuda.device_count()) if self.torch.cuda.is_available() else 0,
            "gpu_names": [self.torch.cuda.get_device_name(i) for i in range(self.torch.cuda.device_count())] if self.torch.cuda.is_available() else [],
            "n_layers": int(self.model.config.num_hidden_layers),
            "hidden_size": int(self.model.config.hidden_size),
        }

    def count_tokens(self, text):
        return len(self.tokenizer(text, add_special_tokens=False)["input_ids"])

    def _prompt_ids(self, messages):
        ids = self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=True, return_tensors="pt")
        if not hasattr(ids, "to"):
            ids = ids["input_ids"]
        return ids.to(self.device)

    def _gen(self, ids, max_new_tokens, past=None):
        torch = self.torch
        with torch.no_grad():
            kwargs = dict(max_new_tokens=max_new_tokens, do_sample=False, num_beams=1, top_p=None, top_k=None, temperature=None,
                          attention_mask=torch.ones_like(ids), pad_token_id=self.tokenizer.pad_token_id or self.tokenizer.eos_token_id)
            if past is not None:
                kwargs["past_key_values"] = past
            out = self.model.generate(ids, **kwargs)
        return self.tokenizer.decode(out[0, ids.shape[1]:], skip_special_tokens=True)

    def generate(self, messages, max_new_tokens):
        return self._gen(self._prompt_ids(messages), max_new_tokens)

    def continuation_logprob(self, messages, continuation):
        torch = self.torch
        p = self._prompt_ids(messages)
        c = self.tokenizer(continuation, add_special_tokens=False, return_tensors="pt")["input_ids"].to(self.device)
        full = torch.cat([p, c], dim=1)
        with torch.no_grad():
            logits = self.model(full, attention_mask=torch.ones_like(full)).logits[0].float()
        lp = torch.log_softmax(logits[p.shape[1] - 1 : full.shape[1] - 1], dim=-1)
        tok = lp.gather(1, c[0].unsqueeze(1)).squeeze(1)
        vals = [float(x) for x in tok]
        return {"mean_logprob": sum(vals) / len(vals), "sum_logprob": sum(vals), "n_tokens": len(vals), "per_token": vals}

    def _hidden(self, ids, past=None):
        torch = self.torch
        with torch.no_grad():
            if past is not None:
                out = self.model(ids[:, past.get_seq_length():], past_key_values=past, attention_mask=torch.ones_like(ids), output_hidden_states=True, use_cache=True)
            else:
                out = self.model(ids, attention_mask=torch.ones_like(ids), output_hidden_states=True)
        return [h[0, -1, :].float().cpu().tolist() for h in out.hidden_states]

    def hidden_states(self, messages):
        return self._hidden(self._prompt_ids(messages))

    def _prefix_cache(self, prefix_text, messages):
        """KV cache of the R0 prefix, then the R2-based chat prompt continues from it."""
        torch = self.torch
        pre = self.tokenizer(prefix_text + "\n\n", add_special_tokens=True, return_tensors="pt")["input_ids"].to(self.device)
        with torch.no_grad():
            past = self.model(pre, attention_mask=torch.ones_like(pre), use_cache=True).past_key_values
        cont = self._prompt_ids(messages)
        full = torch.cat([pre, cont], dim=1)
        return full, past

    def generate_with_retained_prefix(self, prefix_text, messages, max_new_tokens):
        full, past = self._prefix_cache(prefix_text, messages)
        return self._gen(full, max_new_tokens, past=copy.deepcopy(past))

    def hidden_states_with_retained_prefix(self, prefix_text, messages):
        full, past = self._prefix_cache(prefix_text, messages)
        return self._hidden(full, past=copy.deepcopy(past))


def make_backend(args, design: dict) -> Backend:
    if args.backend == "stub":
        return StubBackend(variant=args.stub_variant)
    models = {m["alias"]: m for m in design["models"]}
    if args.model not in models:
        raise SystemExit(f"unknown model alias {args.model!r}; known: {sorted(models)}")
    spec = models[args.model]
    revision = spec.get("revision") or None
    if revision in (None, "", "UNRESOLVED"):
        resolved = Path(os.environ.get("HF_HOME", "")) / "RESOLVED_REVISIONS.json"
        if resolved.exists():
            revision = read_json(resolved).get(spec["hf_id"], {}).get("revision")
    return HFBackend(spec["hf_id"], revision, dtype=design["decoding"]["dtype"], device=args.device, seed=design["decoding"]["seed"])


# --------------------------------------------------------------------------- suite loading

def suite_path(workdir: Path, split: str) -> Path:
    return workdir / "suite" / f"suite_{split}.json"


def load_suite(workdir: Path, split: str, max_instances: int | None, families: str | None = None) -> dict:
    path = suite_path(workdir, split)
    if not path.exists():
        raise SystemExit(f"suite missing: {path} (run --stage generate-suite first)")
    suite = read_json(path)
    recorded = read_json(path.with_suffix(".sha256.json"))["sha256"]
    if sha256_file(path) != recorded:
        raise SystemExit("suite sha256 mismatch: the frozen suite was modified")
    if families:
        if split != "dev":
            raise SystemExit("--families is permitted for the dev split only")
        wanted = set(families.split(","))
        unknown = wanted - set(FAMILIES)
        if unknown:
            raise SystemExit(f"unknown families: {sorted(unknown)}")
        suite["instances"] = [i for i in suite["instances"] if i["family"] in wanted]
        suite["n_instances"] = len(suite["instances"])
    if max_instances is not None:
        if split != "dev":
            raise SystemExit("--max-instances is permitted for the dev split only")
        per_family: dict[str, int] = {}
        kept = []
        n_fam = len({i["family"] for i in suite["instances"]}) or 1
        cap = max(1, max_instances // n_fam)
        for inst in suite["instances"]:
            if per_family.get(inst["family"], 0) < cap and len(kept) < max_instances:
                kept.append(inst)
                per_family[inst["family"]] = per_family.get(inst["family"], 0) + 1
        suite["instances"] = kept
        suite["n_instances"] = len(kept)
    return suite


def model_dir(workdir: Path, model_alias: str, split: str) -> Path:
    return workdir / "runs" / f"{model_alias}__{split}"


def prepare_conditions(inst: dict, arm: dict, backend: Backend, design: dict) -> dict:
    """Render every R-condition and pad to the per-arm max token count."""
    raw = {c: render_state(inst, arm, c) for c in CONDITIONS}
    counts = {c: backend.count_tokens(t) for c, t in raw.items()}
    target = max(counts.values())
    tol = design["token_budget"]["tolerance_tokens"]
    out = {}
    for c, t in raw.items():
        padded, n, added = pad_state(t, target, backend.count_tokens, tol)
        out[c] = {"state_text": padded, "state_text_unpadded": t, "tokens_unpadded": counts[c], "tokens_padded": n, "filler_lines": added, "cell_key": sha256_text(t + "\n||\n" + arm["evidence_text"])}
    return out


# --------------------------------------------------------------------------- stages

def stage_generate_suite(args, design) -> dict:
    workdir = Path(args.workdir)
    out = {}
    for split in ("dev", "protected"):
        seed = resolve_split_seed(design, split, getattr(args, "protected_seed_file", None))
        if seed is None:
            out[split] = {"status": "SEALED_SEED_NOT_SUPPLIED__SPLIT_NOT_GENERATED", "commitment_sha256": design["suite_generator"]["seed"].get(f"{split}_commitment_sha256")}
            continue
        suite = generate_suite(design, split, scale=args.suite_scale if split == "dev" else None, seed=seed)
        path = suite_path(workdir, split)
        write_json(path, suite)
        digest = sha256_file(path)
        write_json(path.with_suffix(".sha256.json"), {"file": path.name, "sha256": digest, "n_instances": suite["n_instances"], "generator_seed": suite["generator_seed"]})
        out[split] = {"path": str(path), "sha256": digest, "n_instances": suite["n_instances"], "instances_per_family": suite["instances_per_family"]}
    write_json(workdir / "suite" / "SUITE_MANIFEST.json", {"schema_version": RESULT_SCHEMA, "stage": "generate-suite", "design_id": design["design_id"], "splits": out})
    return out


def _timer():
    t0 = time.perf_counter()
    return lambda: time.perf_counter() - t0


def stage_present_gate(args, design, backend: Backend) -> dict:
    suite = load_suite(Path(args.workdir), args.split, args.max_instances, args.families)
    mdir = model_dir(Path(args.workdir), args.model, args.split)
    records = []
    elapsed = _timer()
    n_calls = 0
    for inst in suite["instances"]:
        for arm in inst["arms"]:
            conds = prepare_conditions(inst, arm, backend, design)
            for c in CONDITIONS:
                st = conds[c]["state_text"]
                m_status = build_messages(st, "status_line", None, inst["claim_id"])
                lp = backend.continuation_logprob(m_status, inst["linguistic_target"]["continuation"])
                m_act = build_messages(st, "current_action", None, inst["claim_id"])
                raw = backend.generate(m_act, design["decoding"]["max_new_tokens"])
                n_calls += 2
                records.append({
                    "instance_id": inst["instance_id"], "family": inst["family"], "arm_id": arm["arm_id"], "condition": c,
                    "tokens_padded": conds[c]["tokens_padded"], "tokens_unpadded": conds[c]["tokens_unpadded"], "filler_lines": conds[c]["filler_lines"],
                    "cell_key": conds[c]["cell_key"],
                    "status_line_mean_logprob": lp["mean_logprob"], "status_line_n_tokens": lp["n_tokens"],
                    "current_action_raw": raw, "current_action": parse_action(raw),
                    "current_gold": arm["current_gold"]["acceptable"],
                    "current_correct": parse_action(raw) in arm["current_gold"]["acceptable"],
                    "prompt_sha256": sha256_text(json.dumps(m_act, sort_keys=True)),
                })
    result = {"schema_version": RESULT_SCHEMA, "stage": "present-gate", "model": args.model, "split": args.split, "backend": backend.describe(), "n_instances": suite["n_instances"], "n_model_calls": n_calls, "wall_seconds": elapsed(), "records": records}
    write_json(mdir / "present_gate.json", result)
    return {"n_records": len(records), "wall_seconds": result["wall_seconds"], "n_model_calls": n_calls}


def stage_revision(args, design, backend: Backend) -> dict:
    suite = load_suite(Path(args.workdir), args.split, args.max_instances, args.families)
    mdir = model_dir(Path(args.workdir), args.model, args.split)
    records = []
    elapsed = _timer()
    n_calls = 0
    for inst in suite["instances"]:
        for arm in inst["arms"]:
            conds = prepare_conditions(inst, arm, backend, design)
            for c in CONDITIONS:
                m = build_messages(conds[c]["state_text"], "future_action", arm["evidence_text"], inst["claim_id"])
                raw = backend.generate(m, design["decoding"]["max_new_tokens"])
                n_calls += 1
                act = parse_action(raw)
                records.append({
                    "instance_id": inst["instance_id"], "family": inst["family"], "arm_id": arm["arm_id"], "condition": c,
                    "class": arm["update_or_maintain_class"], "cell_key": conds[c]["cell_key"],
                    "tokens_padded": conds[c]["tokens_padded"], "tokens_unpadded": conds[c]["tokens_unpadded"],
                    "future_action_raw": raw, "future_action": act,
                    "future_gold": arm["future_gold"]["acceptable"], "future_correct": act in arm["future_gold"]["acceptable"],
                    "false_revision": act == "REOPEN" and "REOPEN" not in arm["future_gold"]["acceptable"],
                    "missed_revision": act != "REOPEN" and arm["future_gold"]["acceptable"] == ["REOPEN"],
                    "prompt_sha256": sha256_text(json.dumps(m, sort_keys=True)),
                })
    result = {"schema_version": RESULT_SCHEMA, "stage": "revision", "model": args.model, "split": args.split, "backend": backend.describe(), "n_instances": suite["n_instances"], "n_model_calls": n_calls, "wall_seconds": elapsed(), "records": records}
    write_json(mdir / "revision.json", result)
    return {"n_records": len(records), "wall_seconds": result["wall_seconds"], "n_model_calls": n_calls}


def _probe_label(inst: dict, arm: dict) -> int | None:
    """V3 probe label: the registry class of the arm's RECORDED BASIS.

    V1 used ``1 if support_set == ["A"] else 0`` -- the *generator's* index for the source,
    not a property of anything rendered.  Its only textual footprint was the fixed roster
    order, so it was recoverable from R0 and provably not from R3 (which names the basis but
    lists no roster).  That is what made the registered "decodes under R3 >= 0.80" clause
    unsatisfiable rather than merely unexecuted.

    The V3 label is a stated attribute of the basis itself, so it is present in every
    condition that names the basis and absent from every condition that does not.  Balance
    is guaranteed by construction in ``build_instance``.  ``certify_label_identifiability``
    proves per condition, before the run, which of the two cases holds.
    """
    ss = arm["state_vars"]["support_set"]
    if len(ss) != 1:
        return None
    if arm["state_vars"].get("record_identifies_support") is False:
        return None
    reg = inst["sources"][ss[0]]["id"].split("-")[0]
    if reg in _REGISTRY_CLASS_1:
        return 1
    if reg in _REGISTRY_CLASS_0:
        return 0
    return None


def _write_hidden(path: Path, matrix: list[list[list[float]]]) -> str:
    """Store hidden states compactly; numpy float16 when available, JSON otherwise."""
    try:
        import numpy as np

        arr = np.asarray(matrix, dtype=np.float16)
        np.save(path.with_suffix(".npy"), arr)
        return path.with_suffix(".npy").name
    except Exception:  # pragma: no cover - CI has no numpy
        write_json(path.with_suffix(".json"), matrix)
        return path.with_suffix(".json").name


def stage_probe(args, design, backend: Backend) -> dict:
    suite = load_suite(Path(args.workdir), args.split, args.max_instances, args.families)
    mdir = model_dir(Path(args.workdir), args.model, args.split)
    pdir = mdir / "probe"
    pdir.mkdir(parents=True, exist_ok=True)
    probe_families = set(design["probe"]["families"])
    conds = list(design["probe"]["conditions"])
    captures: dict[str, list] = {c: [] for c in conds}
    meta = []
    elapsed = _timer()
    n_calls = 0
    for inst in suite["instances"]:
        if inst["family"] not in probe_families:
            continue
        for arm in inst["arms"]:
            label = _probe_label(inst, arm)
            if label is None:
                continue
            rendered = prepare_conditions(inst, arm, backend, design)
            r0_prefix = rendered["R0"]["state_text_unpadded"]
            for c in conds:
                base_c = "R2" if c.startswith("R2_") else c
                m = build_messages(rendered[base_c]["state_text"], "current_action", None, inst["claim_id"])
                if c == "R2_TEXT_REMOVED_KV_RETAINED":
                    hs = backend.hidden_states_with_retained_prefix(r0_prefix, m)
                else:
                    hs = backend.hidden_states(m)
                n_calls += 1
                captures[c].append(hs)
            meta.append({"instance_id": inst["instance_id"], "family": inst["family"], "arm_id": arm["arm_id"], "index": inst["index"], "label": label})
    stored = {}
    for c in conds:
        if captures[c]:
            stored[c] = _write_hidden(pdir / f"hidden_{c}", captures[c])
    # frozen split by instance index parity-free rule: first train_fraction of distinct instances
    ids = sorted({m["instance_id"] for m in meta})
    n_train = int(math.floor(len(ids) * design["probe"]["train_fraction"]))
    train_ids = set(ids[:n_train])
    results = {}
    for c in conds:
        if not captures[c]:
            continue
        n_layers = len(captures[c][0])
        per_layer = []
        for layer in range(n_layers):
            xs_tr = [captures[c][i][layer] for i, m in enumerate(meta) if m["instance_id"] in train_ids]
            ys_tr = [m["label"] for m in meta if m["instance_id"] in train_ids]
            xs_te = [captures[c][i][layer] for i, m in enumerate(meta) if m["instance_id"] not in train_ids]
            ys_te = [m["label"] for m in meta if m["instance_id"] not in train_ids]
            acc_tr, acc_te = mass_mean_probe(xs_tr, ys_tr, xs_te, ys_te)
            per_layer.append({"layer": layer, "train_acc": acc_tr, "test_acc": acc_te, "n_train": len(ys_tr), "n_test": len(ys_te)})
        usable = [r for r in per_layer if isinstance(r["test_acc"], float) and math.isfinite(r["test_acc"])]
        best = max(usable, key=lambda r: (r["test_acc"], -r["layer"])) if usable else None
        results[c] = {"per_layer": per_layer, "max_test_acc": best["test_acc"] if best else None, "best_layer": best["layer"] if best else None, "n_test": best["n_test"] if best else 0,
                      "status": "OK" if best else "CANNOT_CHECK_PROBE__INSUFFICIENT_UNITS"}
    result = {"schema_version": RESULT_SCHEMA, "stage": "probe", "model": args.model, "split": args.split, "backend": backend.describe(), "probe": "mass_mean_difference_direction", "train_instance_ids": sorted(train_ids), "n_capture_units": len(meta), "hidden_files": stored, "meta": meta, "n_model_calls": n_calls, "wall_seconds": elapsed(), "results": results,
              # Both certificates are model-free and depend only on the frozen suite, so they
              # are recomputed here and stored beside the accuracies they govern.  A reader of
              # probe.json can never see an accuracy without the certificate that says whether
              # the number could have meant anything.
              "identifiability": certify_label_identifiability(design, suite),
              "surface_null": surface_null_accuracies(design, suite)}
    write_json(mdir / "probe.json", result)
    return {"conditions": {c: r["max_test_acc"] for c, r in results.items()}, "wall_seconds": result["wall_seconds"], "n_model_calls": n_calls}


def stage_kv_channel(args, design, backend: Backend) -> dict:
    suite = load_suite(Path(args.workdir), args.split, args.max_instances, args.families)
    mdir = model_dir(Path(args.workdir), args.model, args.split)
    fams = set(design["kv_channel"]["families"])
    records = []
    elapsed = _timer()
    n_calls = 0
    for inst in suite["instances"]:
        if inst["family"] not in fams:
            continue
        for arm in inst["arms"]:
            rendered = prepare_conditions(inst, arm, backend, design)
            r0_prefix = rendered["R0"]["state_text_unpadded"]
            m = build_messages(rendered["R2"]["state_text"], "future_action", arm["evidence_text"], inst["claim_id"])
            for c in ("R2",) + KV_CONDITIONS:
                if c == "R2_TEXT_REMOVED_KV_RETAINED":
                    raw = backend.generate_with_retained_prefix(r0_prefix, m, design["decoding"]["max_new_tokens"])
                    cost = rendered["R0"]["tokens_unpadded"] + rendered["R2"]["tokens_padded"]
                else:
                    raw = backend.generate(m, design["decoding"]["max_new_tokens"])
                    cost = rendered["R2"]["tokens_padded"]
                n_calls += 1
                act = parse_action(raw)
                records.append({
                    "instance_id": inst["instance_id"], "family": inst["family"], "arm_id": arm["arm_id"], "condition": c,
                    "class": arm["update_or_maintain_class"], "retained_tokens": cost,
                    "future_action_raw": raw, "future_action": act, "future_gold": arm["future_gold"]["acceptable"],
                    "future_correct": act in arm["future_gold"]["acceptable"],
                    "prompt_sha256": sha256_text(json.dumps(m, sort_keys=True)),
                })
    result = {"schema_version": RESULT_SCHEMA, "stage": "kv-channel", "model": args.model, "split": args.split, "backend": backend.describe(), "n_model_calls": n_calls, "wall_seconds": elapsed(), "records": records}
    write_json(mdir / "kv_channel.json", result)
    return {"n_records": len(records), "wall_seconds": result["wall_seconds"], "n_model_calls": n_calls}


def stage_certify(args, design) -> dict:
    """PRE-RUN gate: clause coverage + label identifiability, from the frozen suite alone.

    Run before any protected model call.  If it does not pass, the run must not proceed:
    every defect it reports is one that an accuracy cannot show you afterwards.
    """
    suite = load_suite(Path(args.workdir), args.split, args.max_instances, args.families)
    ident = certify_label_identifiability(design, suite)
    nulls = surface_null_accuracies(design, suite)
    # Reachability is decidable now: bind every registered clause to a placeholder value so
    # coverage reports NOT_EVALUATED for anything the runner cannot produce at all, and
    # UNSATISFIABLE/UNFAILABLE for anything the stimuli cannot decide.
    # Pre-run there are no measured values, so every clause resolves to None.  What IS
    # decidable now is reachability, and a clause whose SOURCE PATH is not even declared.
    # Those are the two things an accuracy can never tell you afterwards.
    cov = certify_clause_coverage(design, {}, ident)
    declared = {r["clause_id"] for r in cov["clauses"] if r.get("source")}
    pre = [r for r in cov["clauses"] if r["status"] == "UNREACHABLE__DESIGN_DEFECT"
           or r["clause_id"] not in declared]
    out = {"schema_version": RESULT_SCHEMA, "stage": "certify", "split": args.split,
           "design_id": design["design_id"], "suite_sha256": sha256_file(suite_path(Path(args.workdir), args.split)),
           "identifiability": ident, "surface_null": nulls,
           "clause_coverage": {k: v for k, v in cov.items() if k != "clauses"},
           "clauses": cov["clauses"],
           "blocking": [r["clause_id"] for r in pre],
           "passes": ident["passes"] and not pre}
    write_json(Path(args.workdir) / "certificates" / f"CERTIFICATE_{args.split}.json", out)
    return {k: out[k] for k in ("passes", "blocking", "clause_coverage")} | {
        "identifiable": ident["observed_identifiable"], "matches_registration": ident["matches_registration"]}


def competence_gate(design: dict, revision_records: list[dict]) -> dict:
    """Design V2 GPC: R0 maintain and update accuracy on the dev split, per model.

    Reported only; it never enters GP0-GP3 or the terminal. A model failing GPC on dev is
    replaced BEFORE the protected seed is sealed (the design's registered replacement rule)."""
    g = design["gates"]["GPC"]
    cond = g.get("condition", "R0")
    r0 = [r for r in revision_records if r["condition"] == cond]
    maintain = [r for r in r0 if r["class"] == "MAINTAIN_REQUIRED"]
    update = [r for r in r0 if r["class"] == "UPDATE_REQUIRED"]
    m_acc, u_acc = _accuracy(maintain), _accuracy(update)
    by_family = {}
    for fam in sorted({r["family"] for r in r0}):
        by_family[fam] = {
            "maintain": _accuracy([r for r in maintain if r["family"] == fam]),
            "update": _accuracy([r for r in update if r["family"] == fam]),
        }
    m_ok = m_acc["n"] > 0 and m_acc["acc"] >= g["min_maintain_accuracy_R0"]
    u_ok = u_acc["n"] > 0 and u_acc["acc"] >= g["min_update_accuracy_R0"]
    return {
        "gate": "GPC", "condition": cond, "split_rule": "dev split only",
        "min_maintain_accuracy_R0": g["min_maintain_accuracy_R0"], "min_update_accuracy_R0": g["min_update_accuracy_R0"],
        "maintain_accuracy_R0": m_acc, "update_accuracy_R0": u_acc, "by_family": by_family,
        "maintain_ok": m_ok, "update_ok": u_ok, "pass": bool(m_ok and u_ok),
        "verdict": "COMPETENT__MODEL_RETAINED" if (m_ok and u_ok) else "INCOMPETENT_ON_DEV__MODEL_MUST_BE_REPLACED_BEFORE_PROTECTED_SEED",
    }


def stage_competence_gate(args, design) -> dict:
    if "GPC" not in design.get("gates", {}):
        raise SystemExit("competence-gate requires a design that registers gates.GPC (design V2+)")
    if args.split != "dev":
        raise SystemExit("competence-gate is a dev-split-only stage by registration")
    mdir = model_dir(Path(args.workdir), args.model, args.split)
    rev_path = mdir / "revision.json"
    if not rev_path.exists():
        raise SystemExit(f"competence-gate needs {rev_path} (run --stage revision on the dev split first)")
    revision = read_json(rev_path)
    out = competence_gate(design, revision["records"])
    result = {"schema_version": RESULT_SCHEMA, "stage": "competence-gate", "model": args.model, "split": args.split, "backend": revision.get("backend"), "n_instances": revision.get("n_instances"), **out}
    write_json(mdir / "competence_gate.json", result)
    return {"pass": out["pass"], "verdict": out["verdict"], "maintain_accuracy_R0": out["maintain_accuracy_R0"]["acc"], "update_accuracy_R0": out["update_accuracy_R0"]["acc"]}


# --------------------------------------------------------------------------- statistics (pure Python)

def mass_mean_probe(xs_tr, ys_tr, xs_te, ys_te) -> tuple[float, float]:
    """Difference-of-class-means direction, midpoint threshold. Deterministic, closed form."""
    if not xs_tr or len(set(ys_tr)) < 2:
        return float("nan"), float("nan")
    try:
        import numpy as np

        Xtr = np.asarray(xs_tr, dtype=np.float64)
        ytr = np.asarray(ys_tr)
        mu1 = Xtr[ytr == 1].mean(axis=0)
        mu0 = Xtr[ytr == 0].mean(axis=0)
        w = mu1 - mu0
        thr = float(((mu1 + mu0) / 2.0) @ w)

        def acc(X, y):
            if len(y) == 0:
                return float("nan")
            pred = (np.asarray(X, dtype=np.float64) @ w > thr).astype(int)
            return float((pred == np.asarray(y)).mean())

        return acc(Xtr, ytr), acc(xs_te, ys_te)
    except ImportError:
        dim = len(xs_tr[0])
        c1 = [x for x, y in zip(xs_tr, ys_tr) if y == 1]
        c0 = [x for x, y in zip(xs_tr, ys_tr) if y == 0]
        mu1 = [sum(v[d] for v in c1) / len(c1) for d in range(dim)]
        mu0 = [sum(v[d] for v in c0) / len(c0) for d in range(dim)]
        w = [a - b for a, b in zip(mu1, mu0)]
        thr = sum(((a + b) / 2.0) * ww for a, b, ww in zip(mu1, mu0, w))

        def acc(X, y):
            if not y:
                return float("nan")
            hits = 0
            for v, lab in zip(X, y):
                pred = 1 if sum(a * b for a, b in zip(v, w)) > thr else 0
                hits += int(pred == lab)
            return hits / len(y)

        return acc(xs_tr, ys_tr), acc(xs_te, ys_te)


def binom_two_sided_p(k: int, n: int) -> float:
    """Exact two-sided binomial test against p=0.5 (McNemar exact on discordant pairs)."""
    if n == 0:
        return 1.0
    pk = math.comb(n, k) / 2 ** n
    total = sum(math.comb(n, i) for i in range(n + 1) if math.comb(n, i) / 2 ** n <= pk + 1e-15) / 2 ** n
    return min(1.0, total)


def mcnemar(pairs: list[tuple[bool, bool]]) -> dict:
    """pairs of (x_correct, y_correct); tests y > x (two-sided exact p, direction reported)."""
    n = len(pairs)
    b = sum(1 for x, y in pairs if x and not y)
    c = sum(1 for x, y in pairs if y and not x)
    acc_x = sum(1 for x, _ in pairs if x) / n if n else float("nan")
    acc_y = sum(1 for _, y in pairs if y) / n if n else float("nan")
    return {"n": n, "acc_x": acc_x, "acc_y": acc_y, "diff_y_minus_x": (acc_y - acc_x) if n else float("nan"), "discordant_x_only": b, "discordant_y_only": c, "p_two_sided_exact": binom_two_sided_p(c, b + c)}


def wilson_ci(k: int, n: int, z: float = 1.959964) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (centre - half, centre + half)


def _betacf(a, b, x, max_iter=300, eps=3e-14):
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1.0 + aa / (c if abs(c) > 1e-300 else 1e-300)
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1.0 + aa / (c if abs(c) > 1e-300 else 1e-300)
        de = d * c
        h *= de
        if abs(de - 1.0) < eps:
            break
    return h


def reg_inc_beta(a: float, b: float, x: float) -> float:
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    ln = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    front = math.exp(ln)
    if x < (a + 1) / (a + b + 2):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1 - x) / b


def student_t_cdf(t: float, df: float) -> float:
    x = df / (df + t * t)
    tail = 0.5 * reg_inc_beta(df / 2.0, 0.5, x)
    return 1.0 - tail if t > 0 else tail


def student_t_quantile(p: float, df: float) -> float:
    lo, hi = -50.0, 50.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if student_t_cdf(mid, df) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def paired_tost(diffs: list[float], margin: float, alpha: float = 0.05) -> dict:
    """Two one-sided tests for |mean diff| < margin; equivalent to the (1-2alpha) CI inside +-margin."""
    n = len(diffs)
    if n < 3:
        return {"n": n, "equivalent": None, "reason": "n<3"}
    mean = sum(diffs) / n
    var = sum((d - mean) ** 2 for d in diffs) / (n - 1)
    se = math.sqrt(var / n) if var > 0 else 0.0
    q = student_t_quantile(1 - alpha, n - 1)
    lo, hi = mean - q * se, mean + q * se
    if se == 0:
        p_lower = p_upper = 0.0 if abs(mean) < margin else 1.0
    else:
        p_lower = 1.0 - student_t_cdf((mean + margin) / se, n - 1)
        p_upper = student_t_cdf((mean - margin) / se, n - 1)
    return {"n": n, "mean_diff": mean, "se": se, "ci_90": [lo, hi], "margin": margin, "p_tost": max(p_lower, p_upper), "equivalent": bool(lo > -margin and hi < margin)}


def cell_certificates(records: list[dict]) -> dict:
    """Joint-intersection compatibility per (instance, condition) cell (CR-02/CR-03)."""
    cells: dict[tuple, dict] = {}
    for r in records:
        key = (r["instance_id"], r["condition"], r["cell_key"])
        cells.setdefault(key, {"instance_id": r["instance_id"], "condition": r["condition"], "members": []})
        cells[key]["members"].append((r["arm_id"], frozenset(r["future_gold"])))
    by_condition: dict[str, dict] = {}
    for key, cell in cells.items():
        cond = cell["condition"]
        acc = by_condition.setdefault(cond, {"cells": 0, "multi_history_cells": 0, "incompatible_cells": 0, "pairwise_disjoint_pairs": 0, "pairs": 0})
        acc["cells"] += 1
        sets = [s for _, s in cell["members"]]
        if len(sets) > 1:
            acc["multi_history_cells"] += 1
            joint = frozenset.intersection(*sets)
            if not joint:
                acc["incompatible_cells"] += 1
            for s1, s2 in combinations(sets, 2):
                acc["pairs"] += 1
                if not (s1 & s2):
                    acc["pairwise_disjoint_pairs"] += 1
    for cond, acc in by_condition.items():
        acc["incompatible_cell_rate"] = acc["incompatible_cells"] / acc["cells"] if acc["cells"] else float("nan")
        acc["pairwise_disjoint_rate"] = acc["pairwise_disjoint_pairs"] / acc["pairs"] if acc["pairs"] else float("nan")
    return by_condition


def three_history_control() -> dict:
    sets = {"h1": {"a", "b"}, "h2": {"b", "c"}, "h3": {"a", "c"}}
    pairwise_all_nonempty = all(bool(sets[x] & sets[y]) for x, y in combinations(sets, 2))
    joint = set.intersection(*sets.values())
    return {"pairwise_all_nonempty": pairwise_all_nonempty, "joint_empty": not joint, "passes": pairwise_all_nonempty and not joint}


def mcnemar_mde(n: int, discordance: float, alpha: float = 0.05, power: float = 0.8) -> float:
    """Approximate minimal detectable accuracy difference for paired McNemar (normal approx)."""
    z_a, z_b = 1.959964, 0.841621
    n_disc = n * discordance
    if n_disc <= 0:
        return float("nan")
    # detectable |p_c - p_b| among discordant pairs, then scale to accuracy difference
    delta_disc = (z_a + z_b) * math.sqrt(1.0 / n_disc) * 0.5 * 2
    return min(1.0, delta_disc * discordance)


# --------------------------------------------------------------------------- rollup

def _by(records: Iterable[dict], **filt) -> list[dict]:
    out = []
    for r in records:
        ok = True
        for k, v in filt.items():
            rv = r.get(k)
            if isinstance(v, (set, frozenset, list, tuple)):
                ok &= rv in v
            else:
                ok &= rv == v
        if ok:
            out.append(r)
    return out


def _pairs(records: list[dict], cond_x: str, cond_y: str, key: str = "future_correct") -> list[tuple[bool, bool]]:
    idx: dict[tuple, dict] = {}
    for r in records:
        idx[(r["instance_id"], r["arm_id"], r["condition"])] = r
    pairs = []
    for (iid, aid, c), r in idx.items():
        if c == cond_x and (iid, aid, cond_y) in idx:
            pairs.append((bool(r[key]), bool(idx[(iid, aid, cond_y)][key])))
    return pairs


def _instance_pairs(records: list[dict], cond_x: str, cond_y: str, key: str = "future_correct") -> list[tuple[bool, bool]]:
    """Instance-level pairing: an instance is correct under a condition iff every arm is correct."""
    agg: dict[tuple[str, str], bool] = {}
    for r in records:
        k = (r["instance_id"], r["condition"])
        agg[k] = agg.get(k, True) and bool(r[key])
    pairs = []
    for (iid, c), ok in agg.items():
        if c == cond_x and (iid, cond_y) in agg:
            pairs.append((ok, agg[(iid, cond_y)]))
    return pairs


def _accuracy(records: list[dict], key: str = "future_correct") -> dict:
    n = len(records)
    k = sum(1 for r in records if r[key])
    lo, hi = wilson_ci(k, n)
    return {"n": n, "correct": k, "acc": (k / n) if n else float("nan"), "wilson95": [lo, hi]}



# --------------------------------------------------------------- V3 pre-run certificates
#
# The V1/V2 GP2a defect had two independent shapes, and each needs its own instrument.
#
#   (i)  A registered clause the runner silently narrowed.  "decodes under R0 AND R3" was
#        implemented as R0 only, so half a registered sentence never executed and the gate
#        reported the half that did.  -> certify_clause_coverage.
#   (ii) A clause that could not have come out any other way.  Implementing (i) verbatim
#        would have produced a permanently failing gate, because the V1 label left no trace
#        in R3; and the sibling clause "at chance under R2_TRUE_REMOVAL" could never have
#        failed, because R2 renders identically across the two arms.  Neither is detectable
#        from an accuracy.  -> certify_label_identifiability + the reachability limb.
#
# Both run BEFORE any model call, from the frozen suite alone, and both are gates.


def _probe_capture_units(design: dict, suite: dict) -> list[dict]:
    """Every (instance, arm) the probe would capture, in probe order."""
    fams = set(design["probe"]["families"])
    units = []
    for inst in suite["instances"]:
        if inst["family"] not in fams:
            continue
        for arm in inst["arms"]:
            label = _probe_label(inst, arm)
            if label is None:
                continue
            units.append({"inst": inst, "arm": arm, "label": label, "instance_id": inst["instance_id"]})
    return units


def _effective_context(inst: dict, arm: dict, condition: str) -> str:
    """What the model actually conditions on for a probe capture.

    For the KV condition the rendered text is R2, but the retained prefix is the R0 history:
    certifying the *text* alone would call it non-identifiable and be wrong.  The certified
    object is therefore the effective context, prefix included.
    """
    base = "R2" if condition.startswith("R2_") else condition
    text = _render_for_certificate(inst, arm, base)
    if condition == "R2_TEXT_REMOVED_KV_RETAINED":
        return _render_for_certificate(inst, arm, "R0") + "\n||RETAINED_PREFIX||\n" + text
    return text


def _render_for_certificate(inst: dict, arm: dict, condition: str) -> str:
    """Render a condition as a PURE function of ``inst["sources"]``.

    ``render_state`` serves R0 from ``arm["history_lines"]``, which were rendered once at
    suite-build time.  A symmetry applied to ``inst["sources"]`` would therefore leave R0's
    text untouched while changing the label, and the certificate would report every R0 unit
    as a symmetry violation -- a false alarm that says nothing about R0.  The certificate
    re-derives R0 from the sources instead, so the transform propagates.

    Restricted to the probe families (single-source arms, no extra history lines); asserted
    rather than assumed, because a silent mis-render here would corrupt the certificate that
    every probe accuracy depends on.
    """
    if condition != "R0":
        return render_state(inst, arm, condition)
    ss = arm["state_vars"]["support_set"]
    assert inst["family"] in ("F3_P2_CANON", "F3_P2_CANON_SF"), (
        f"certificate re-render is registered for the canonical probe families only, got {inst['family']}")
    claim = {"claim_id": inst["claim_id"], "claim_text": inst["claim_text"], "domain": inst["domain"]}
    lines = _history_lines_ordered(claim, inst["sources"], inst["roster_order"], ss, [])
    rendered = "Record history (complete):\n" + "\n".join(f"{i + 1}. {line}" for i, line in enumerate(lines))
    # Control that must match: on an untransformed instance the re-render is required to
    # reproduce render_state exactly.  If it ever does not, the certificate is broken and
    # must fail loudly rather than certify from a text the model never saw.
    return rendered


def _sigma_exchange(inst: dict) -> dict:
    """Registered generator symmetry: exchange the two candidate sources.

    ``A`` and ``B`` are drawn i.i.d. from one distribution, so the law of the suite is
    invariant under exchanging them.  If a condition's rendering is invariant under the
    exchange while the label is not, then for every capture unit there is an equally likely
    unit with the same context and the opposite label, and the expected accuracy of ANY
    measurable classifier is exactly 0.5.  No probe can beat it and no threshold above
    chance can be met.  That is the V1 R3 situation, stated as a theorem rather than as an
    anomaly in a table.
    """
    j = copy.deepcopy(inst)
    j["sources"]["A"], j["sources"]["B"] = j["sources"]["B"], j["sources"]["A"]
    return j


def certify_label_identifiability(design: dict, suite: dict) -> dict:
    """Per probed condition: is the probe label recoverable from what the model reads?

    Two tests, both exact and both model-free:

      well-definedness   no two capture units may share a context and differ in label.
      symmetry           re-render each unit under the registered exchange; where the
                         image coincides with an observed context, the label recomputed
                         after the exchange must equal that context's label.

    A condition failing either is ``NOT_IDENTIFIABLE``: no accuracy is reported for it and
    any gate clause naming it is refused.  ``unmatched`` (the image falls outside the
    sample) is reported and is NOT a failure -- it only means the symmetry test is silent
    for that condition, which is the normal case once presentation order is randomised.

    This certificate deliberately does NOT ask whether a *non-semantic* reader could also
    succeed; that is the separate job of ``surface_null_accuracies``.  V1's R0 passes this
    certificate and is still confounded.
    """
    units = _probe_capture_units(design, suite)
    conds = list(design["probe"]["conditions"])
    # CONTROL THAT MUST MATCH: the certificate's re-render must reproduce the text the model
    # is actually shown.  Certifying a string the run never uses is the failure mode this
    # whole file exists to prevent, so it is checked, not assumed.
    for u in units:
        a, b = _render_for_certificate(u["inst"], u["arm"], "R0"), render_state(u["inst"], u["arm"], "R0")
        if a != b:
            raise SystemExit(
                "certificate re-render diverges from render_state for "
                f"{u['instance_id']}/{u['arm']['arm_id']}; the identifiability certificate cannot be trusted")
    out: dict[str, Any] = {"n_capture_units": len(units), "conditions": {}}
    for c in conds:
        ctx = [_effective_context(u["inst"], u["arm"], c) for u in units]
        by: dict[str, set] = {}
        for t, u in zip(ctx, units):
            by.setdefault(t, set()).add(u["label"])
        collisions = sum(1 for v in by.values() if len(v) > 1)
        lookup = {t: u["label"] for t, u in zip(ctx, units)}
        mismatches = unmatched = 0
        for u in units:
            si = _sigma_exchange(u["inst"])
            st = _effective_context(si, u["arm"], c)
            sl = _probe_label(si, u["arm"])
            if st not in lookup:
                unmatched += 1
            elif sl is None or lookup[st] != sl:
                mismatches += 1
        pos = sum(1 for u in units if u["label"] == 1)
        balance = pos / len(units) if units else 0.0
        ok = collisions == 0 and mismatches == 0
        out["conditions"][c] = {
            "text_collisions": collisions,
            "symmetry_mismatches": mismatches,
            "symmetry_unmatched": unmatched,
            "label_balance_positive_fraction": balance,
            "identifiable": ok,
            "status": "IDENTIFIABLE" if ok else "LABEL_NOT_IDENTIFIABLE_FROM_CONDITION",
        }
    reg = design["probe"].get("identifiable_conditions_registered", [])
    actual = sorted(c for c, v in out["conditions"].items() if v["identifiable"])
    out["registered_identifiable"] = sorted(reg)
    out["observed_identifiable"] = actual
    out["matches_registration"] = sorted(reg) == actual
    out["passes"] = bool(out["matches_registration"]) and 0.45 <= (
        max((v["label_balance_positive_fraction"] for v in out["conditions"].values()), default=0.0)
    ) <= 0.55
    return out


# -------------------------------------------------------------------- model-free surface nulls


def _lexical_features(text: str) -> dict[str, float]:
    f: dict[str, float] = {}
    for w in re.findall(r"[a-z0-9]+", text.lower()):
        f["w:" + w] = f.get("w:" + w, 0.0) + 1.0
    for i in range(0, max(0, len(text) - 4), 2):
        k = "c:" + text[i:i + 4]
        f[k] = f.get(k, 0.0) + 1.0
    return f


def _relational_features(text: str) -> dict[str, float]:
    """Position/relation features -- no lexical memory, so nonce names do not blunt it.

    This is the reader that scores 1.000 on V1's R0 while a bag-of-ngrams reader sits at
    0.490, which is why the surface null MUST include it.  A validity check that only ever
    ran the lexical reader would have cleared V1's positional shortcut.
    """
    f: dict[str, float] = {}
    ros = re.search(r"Sources on file: (.*?)\.", text, re.S)
    sup = re.search(
        r"(?:on the basis of|Recorded basis for claim \S+?:)\s+(the \w+ \d{4} report) \[([A-Z]{3}-[0-9a-f]{4})\]",
        text,
    )
    if sup:
        f["basis_offset_frac"] = text.index(sup.group(1)) / max(1, len(text))
        f["n_names_before_basis"] = float(len(re.findall(r"the \w+ \d{4} report", text[: text.index(sup.group(1))])))
    if ros and sup:
        names = re.findall(r"the \w+ \d{4} report", ros.group(1))
        slot = names.index(sup.group(1)) + 1 if sup.group(1) in names else 0
        f["roster_slot"] = float(slot)
        for b in (0, 1, 2, 3):
            f[f"roster_slot=={b}"] = float(slot == b)
    return f


def _mass_mean_on_features(feats: list[dict], labels: list[int], tr: list[int], te: list[int]) -> float | None:
    keys = sorted({k for i in tr for k in feats[i]})
    if not keys or not te:
        return None
    vec = lambda i: [feats[i].get(k, 0.0) for k in keys]  # noqa: E731
    pos = [vec(i) for i in tr if labels[i] == 1]
    neg = [vec(i) for i in tr if labels[i] == 0]
    if not pos or not neg:
        return None
    mp = [sum(v[j] for v in pos) / len(pos) for j in range(len(keys))]
    mn = [sum(v[j] for v in neg) / len(neg) for j in range(len(keys))]
    d = [a - b for a, b in zip(mp, mn)]
    thr = (sum(a * b for a, b in zip(mp, d)) + sum(a * b for a, b in zip(mn, d))) / 2.0
    ok = 0
    for i in te:
        ok += int((sum(a * b for a, b in zip(vec(i), d)) >= thr) == (labels[i] == 1))
    return ok / len(te)


def surface_null_accuracies(design: dict, suite: dict) -> dict:
    """What a reader with no model at all achieves on the same stimuli and the same split.

    Reported beside every probe accuracy.  Its purpose is interpretive, not exculpatory: a
    condition where the surface null matches the probe licenses only "the information is
    present in the context", never "the model represents the variable".  V1 cannot separate
    those two readings for R0, and V3 does not pretend the separation is free -- it reports
    the residual and lets the routing depend on it.
    """
    units = _probe_capture_units(design, suite)
    labels = [u["label"] for u in units]
    ids = sorted({u["instance_id"] for u in units})
    n_train = int(math.floor(len(ids) * design["probe"]["train_fraction"]))
    train_ids = set(ids[:n_train])
    tr = [i for i, u in enumerate(units) if u["instance_id"] in train_ids]
    te = [i for i, u in enumerate(units) if u["instance_id"] not in train_ids]
    out: dict[str, Any] = {"n_train": len(tr), "n_test": len(te), "conditions": {}}
    for c in design["probe"]["conditions"]:
        ctx = [_effective_context(u["inst"], u["arm"], c) for u in units]
        lex = _mass_mean_on_features([_lexical_features(t) for t in ctx], labels, tr, te)
        rel = _mass_mean_on_features([_relational_features(t) for t in ctx], labels, tr, te)
        best = max([v for v in (lex, rel) if v is not None], default=None)
        out["conditions"][c] = {"lexical": lex, "relational": rel, "max_surface_null": best}
    return out


# ------------------------------------------------------------- registered-clause coverage


def _resolve(obj: Any, path: str) -> Any:
    """Dotted lookup into the analysis dict; a missing link yields the sentinel None."""
    cur, parts = obj, path.split(".")
    i = 0
    while i < len(parts):
        if not isinstance(cur, dict):
            return None
        # Clause ids contain dots ("GP2a.probe_decodes_R3"), so a naive per-segment walk
        # would miss them and report a live predicate as NOT_EVALUATED -- a false alarm from
        # the very guard that is supposed to make false clean reports impossible.
        for j in range(len(parts), i, -1):
            key = ".".join(parts[i:j])
            if key in cur:
                cur, i = cur[key], j
                break
        else:
            return None
    return cur


def certify_clause_coverage(design: dict, analysis: dict, identifiability: dict) -> dict:
    """Shape 5: a registered clause the runner silently narrows.

    Every clause the design registers carries an id and a ``source`` -- a dotted path into
    this model's analysis where the implementing predicate must have deposited its verdict.
    The clause is only ``PASS``/``FAIL`` if

      (a) the path RESOLVES (the predicate exists and ran), and
      (b) its value is not None (it ran on non-null inputs), and
      (c) it was REACHABLE -- this run's inputs admitted both outcomes.

    Anything else is ``NOT_EVALUATED`` or ``UNREACHABLE__DESIGN_DEFECT``, and neither may be
    absorbed into a sibling clause's verdict.  V1's GP2a reported on the R0 half while the
    R3 half had no implementing predicate at all; under this guard that is a hard terminal.

    Reachability for a probe clause is decided by the identifiability certificate rather
    than by the observed number, because the observed number is exactly what a structurally
    determined clause cannot warn you about:

      direction "min" on a condition that is NOT label-identifiable -> UNSATISFIABLE
        (no probe of any quality can reach the threshold; this is V1's R3 clause)
      direction "max" on a condition that is NOT label-identifiable -> UNFAILABLE
        (the clause holds by construction; this is V1's "at chance under R2_TRUE_REMOVAL")

    Both halves of the V1 defect are therefore flagged before a single model call.
    """
    rows = []
    for gate, spec in design["gates"].items():
        for clause in spec.get("clauses", []):
            cid = clause["id"]
            rec = {
                "gate": gate, "clause_id": cid, "text": clause["text"],
                "required": clause.get("required", True), "source": clause["source"],
            }
            value = _resolve(analysis, clause["source"])
            rec["value"] = value
            cond = clause.get("probe_condition")
            reachable, why = True, "both outcomes admitted by this run's inputs"
            if cond is not None:
                ident = (identifiability.get("conditions") or {}).get(cond, {}).get("identifiable")
                if ident is None:
                    reachable, why = False, f"condition {cond} is absent from the identifiability certificate"
                elif clause.get("direction") == "min" and not ident:
                    reachable = False
                    why = f"UNSATISFIABLE: {cond} is not label-identifiable, so no probe can reach {clause.get('threshold')}"
                elif clause.get("direction") == "max" and not ident:
                    reachable = False
                    why = f"UNFAILABLE: {cond} is not label-identifiable, so the clause holds by construction"
            rec["reachable"] = reachable
            rec["reachability_note"] = why
            if value is None:
                rec["status"] = "NOT_EVALUATED__NO_IMPLEMENTING_PREDICATE_OR_NULL_INPUT"
            elif not reachable:
                rec["status"] = "UNREACHABLE__DESIGN_DEFECT"
            else:
                rec["status"] = "PASS" if bool(value) else "FAIL"
            rows.append(rec)
    bad = [r for r in rows if r["status"].startswith("NOT_EVALUATED") or r["status"] == "UNREACHABLE__DESIGN_DEFECT"]
    return {
        "clauses": rows,
        "n_registered": len(rows),
        "n_evaluated": sum(1 for r in rows if r["status"] in ("PASS", "FAIL")),
        "unevaluated_or_unreachable": [r["clause_id"] for r in bad],
        "passes": not bad,
        "status": "ALL_REGISTERED_CLAUSES_EVALUATED_AND_REACHABLE" if not bad
                  else "REGISTERED_CLAUSE_NOT_EVALUATED_OR_UNREACHABLE",
    }


def analyse_model(design: dict, mdir: Path) -> dict:
    g = design["gates"]
    present = read_json(mdir / "present_gate.json") if (mdir / "present_gate.json").exists() else None
    revision = read_json(mdir / "revision.json") if (mdir / "revision.json").exists() else None
    probe = read_json(mdir / "probe.json") if (mdir / "probe.json").exists() else None
    kv = read_json(mdir / "kv_channel.json") if (mdir / "kv_channel.json").exists() else None
    out: dict[str, Any] = {"model_dir": str(mdir), "stages_present": {"present_gate": bool(present), "revision": bool(revision), "probe": bool(probe), "kv_channel": bool(kv)}}
    P2 = "F3_P2_CANON"

    # ---- GP0 present equivalence on P2 canonical (R2 vs R3, plus R0 agreement)
    if present:
        pr = present["records"]
        idx = {(r["instance_id"], r["arm_id"], r["condition"]): r for r in pr}
        per_inst_pass = []
        lp_diffs = []
        for (iid, aid, c), r in idx.items():
            if c != "R2" or r["family"] != P2:
                continue
            r3 = idx.get((iid, aid, "R3"))
            r0 = idx.get((iid, aid, "R0"))
            if not r3 or not r0:
                continue
            d = r3["status_line_mean_logprob"] - r["status_line_mean_logprob"]
            lp_diffs.append(d)
            same_action = r["current_action"] == r3["current_action"] == r0["current_action"] and r["current_correct"]
            budget_ok = abs(r["tokens_padded"] - r3["tokens_padded"]) <= design["token_budget"]["tolerance_tokens"]
            per_inst_pass.append(abs(d) <= g["GP0"]["epsilon_pred_per_instance_nats_per_token"] and same_action and budget_ok)
        frac = sum(per_inst_pass) / len(per_inst_pass) if per_inst_pass else float("nan")
        tost = paired_tost(lp_diffs, g["GP0"]["epsilon_pred_mean_nats_per_token"])
        gp0_pass = bool(per_inst_pass) and frac >= g["GP0"]["min_pass_fraction"] and (tost.get("equivalent") is True or tost.get("equivalent") is None and len(lp_diffs) < 3)
        current_acc = {c: _accuracy(_by(pr, condition=c), key="current_correct") for c in CONDITIONS}
        p1 = _by(pr, family="F2_P1")
        contrast_A = mcnemar(_pairs(p1, "R1", "R2", key="current_correct")) if p1 else None
        out["GP0"] = {"pass": gp0_pass, "p2_units": len(per_inst_pass), "per_unit_pass_fraction": frac, "tost_R3_minus_R2": tost, "current_accuracy_by_condition": current_acc, "contrast_A_R1_vs_R2_on_P1_current": contrast_A}
    else:
        out["GP0"] = {"pass": None, "reason": "present_gate stage missing"}

    # ---- GP1 R3 > R2 on P2 update+maintain
    if revision:
        rr = revision["records"]
        p2 = _by(rr, family=P2)
        contrast_B = mcnemar(_pairs(p2, "R2", "R3"))
        contrast_B_inst = mcnemar(_instance_pairs(p2, "R2", "R3"))
        contrast_C = mcnemar(_pairs(p2, "R3", "R0"))
        contrast_E = mcnemar(_pairs(p2, "R3", "R4"))
        upd = mcnemar(_pairs(_by(p2, **{"class": "UPDATE_REQUIRED"}), "R2", "R3"))
        mnt = mcnemar(_pairs(_by(p2, **{"class": "MAINTAIN_REQUIRED"}), "R2", "R3"))
        gp1_pass = bool(p2) and contrast_B["diff_y_minus_x"] >= g["GP1"]["min_accuracy_gain"] and contrast_B_inst["p_two_sided_exact"] <= g["GP1"]["alpha"] and contrast_B_inst["diff_y_minus_x"] > 0
        metrics = {}
        for fam in FAMILIES:
            fr = _by(rr, family=fam)
            if not fr:
                continue
            metrics[fam] = {c: {
                "accuracy": _accuracy(_by(fr, condition=c)),
                "false_revision_rate": (sum(1 for r in _by(fr, condition=c) if r["false_revision"]) / max(1, len(_by(fr, condition=c)))),
                "missed_revision_rate": (sum(1 for r in _by(fr, condition=c) if r["missed_revision"]) / max(1, len(_by(fr, condition=c)))),
                "unparseable": sum(1 for r in _by(fr, condition=c) if r["future_action"] == "UNPARSEABLE"),
                "mean_retained_tokens": sum(r["tokens_unpadded"] for r in _by(fr, condition=c)) / max(1, len(_by(fr, condition=c))),
            } for c in CONDITIONS}
        r3_high = contrast_B["acc_y"] >= g["GP1"]["r3_competence_floor"] if p2 else False
        out["GP1"] = {"pass": gp1_pass, "contrast_B_R2_vs_R3_on_P2": contrast_B, "contrast_B_instance_level": contrast_B_inst, "update_only": upd, "maintain_only": mnt, "contrast_C_R3_vs_R0": contrast_C, "contrast_E_R3_vs_R4": contrast_E, "r3_competence_floor_met": r3_high, "metrics_by_family_condition": metrics, "certificates": cell_certificates(rr)}
        # Design V2 registered secondary: the same contrast on the H-EXT-4 same-successor-fibre
        # variant (predictive congruence holds by construction). Reported beside the primary, never gated.
        sf = _by(rr, family="F3_P2_CANON_SF")
        if sf:
            out["GP1"]["contrast_B_same_fibre_R2_vs_R3"] = mcnemar(_pairs(sf, "R2", "R3"))
            out["GP1"]["contrast_B_same_fibre_instance_level"] = mcnemar(_instance_pairs(sf, "R2", "R3"))
            out["GP1"]["contrast_C_same_fibre_R3_vs_R0"] = mcnemar(_pairs(sf, "R3", "R0"))
            out["GP1"]["same_fibre_r3_competence_floor_met"] = out["GP1"]["contrast_B_same_fibre_R2_vs_R3"]["acc_y"] >= g["GP1"]["r3_competence_floor"]
        # ---- GP3 controls
        p0 = _by(rr, family="F1_P0")
        recon = _by(rr, family="F3_P2_RECON")
        mirror = _by(rr, family="F3_P2_MIRROR")
        p0_gap = mcnemar(_pairs(p0, "R2", "R3")) if p0 else None
        recon_gap = mcnemar(_pairs(recon, "R2", "R3")) if recon else None
        mirror_r3 = _accuracy(_by(mirror, condition="R3")) if mirror else None
        mirror_fr = sum(1 for r in _by(mirror, condition="R3") if r["false_revision"]) / max(1, len(_by(mirror, condition="R3"))) if mirror else None
        acq = _by(rr, family="F0_ACQ")
        acq_r0 = _accuracy(_by(acq, condition="R0")) if acq else None
        gp3 = {
            "p0_no_gap": None if p0_gap is None or p0_gap["n"] == 0 else abs(p0_gap["diff_y_minus_x"]) <= g["GP3"]["max_control_gap"],
            "recon_no_gap": None if recon_gap is None or recon_gap["n"] == 0 else abs(recon_gap["diff_y_minus_x"]) <= g["GP3"]["max_control_gap"],
            "mirror_not_falsely_revised_under_R3": None if mirror_fr is None else mirror_fr <= g["GP3"]["max_mirror_false_revision_R3"],
        }
        gp3_pass = None if any(v is None for v in gp3.values()) else all(gp3.values())
        out["GP3"] = {"pass": gp3_pass, "checks": gp3, "p0_R2_vs_R3": p0_gap, "recon_R2_vs_R3": recon_gap, "mirror_R3": mirror_r3, "mirror_false_revision_R3": mirror_fr, "acquisition_R0_accuracy": acq_r0}
    else:
        out["GP1"] = {"pass": None, "reason": "revision stage missing"}
        out["GP3"] = {"pass": None, "reason": "revision stage missing"}

    # ---- GP2 alternate channel (V3: clause-addressed, certificate-gated)
    #
    # Every limb below records itself in ``clause_values`` under its REGISTERED clause id.
    # ``certify_clause_coverage`` later asserts that the set of ids the runner produced is
    # exactly the set the design registered.  A clause the runner does not implement can no
    # longer be absorbed into a sibling's verdict; it surfaces as NOT_EVALUATED and the gate
    # cannot pass.  This is the check that would have caught the V1 R3 omission.
    gp2: dict[str, Any] = {"gate_B_causal_use": "CANNOT_CHECK_ALTERNATE_CHANNEL_CAUSAL_USE"}
    clause_values: dict[str, dict] = {}

    def _record(cid: str, value, ok, note: str = "") -> None:
        clause_values[cid] = {"value": value, "pass": ok, "note": note}

    if probe:
        res = probe["results"]
        acc = {c: r["max_test_acc"] for c, r in res.items()}
        gp2["probe_max_test_acc"] = acc
        gp2["probe_n_test"] = {c: r["n_test"] for c, r in res.items()}
        gp2["probe_surface_null"] = probe.get("surface_null", {}).get("conditions", {})
        gp2["probe_identifiability"] = probe.get("identifiability", {}).get("conditions", {})
        # An accuracy is reported ONLY for a condition the certificate cleared.  A
        # non-identifiable condition yields the distinct code, never a number a reader
        # could mistake for a measurement of the model.
        for c, v in list(acc.items()):
            if not gp2["probe_identifiability"].get(c, {}).get("identifiable", False):
                acc[c] = None
                gp2.setdefault("suppressed_conditions", {})[c] = "LABEL_NOT_IDENTIFIABLE_FROM_CONDITION"

        for cid, cond, direction, thr in design["probe"]["clause_bindings"]:
            v = acc.get(cond)
            if v is None:
                _record(cid, None, None, f"{cond}: no reportable accuracy")
                continue
            ok = v >= thr if direction == "min" else v <= thr
            null = (gp2["probe_surface_null"].get(cond) or {}).get("max_surface_null")
            _record(cid, v, ok, f"surface null {null}")

        # Residual above the model-free reader.  Registered, reported, and NOT silently
        # folded into the pass: a condition where a non-semantic reader matches the probe
        # supports "the information is in the context", not "the model represents it".
        gp2["probe_residual_over_surface_null"] = {
            c: (None if acc.get(c) is None or (gp2["probe_surface_null"].get(c) or {}).get("max_surface_null") is None
                else acc[c] - gp2["probe_surface_null"][c]["max_surface_null"])
            for c in res
        }

    if kv:
        kr = kv["records"]
        d = mcnemar(_pairs(kr, "R2", "R2_TEXT_REMOVED_KV_RETAINED"))
        gp2["contrast_D_R2_vs_kv_retained"] = d
        gp2["kv_retained_accuracy"] = d["acc_y"]
        gp2["R2_accuracy"] = d["acc_x"]
        # Same-path witness (V1 receipt section 8, item 2): a contrast is only non-vacuous if
        # the identical code path is shown returning a DIFFERENT value elsewhere in this same
        # rollup.  The witness is registered per contrast and recorded here, so "1.000 vs
        # 1.000" can never again be read as a result without one.
        if revision:
            w = mcnemar(_pairs(_by(revision["records"], family=P2), "R2", "R3"))
            gp2["contrast_D_same_path_witness"] = {
                "path": "mcnemar(_pairs(...))",
                "witness_contrast": "F3_P2_CANON R2 vs R3",
                "witness_acc_x": w["acc_x"], "witness_acc_y": w["acc_y"],
                "differs": w["acc_x"] != w["acc_y"],
            }
            r0_acc = _accuracy(_by(revision["records"], family=P2, condition="R0"))["acc"]
            gp2["R0_accuracy"] = r0_acc
            _record("GP2b.kv_recovers_R0", d["acc_y"], d["acc_y"] >= r0_acc - g["GP2"]["kv_recovery_margin"],
                    f"R0 accuracy {r0_acc}")
        _record("GP2b.contrast_D_significant", d["p_two_sided_exact"], d["p_two_sided_exact"] <= g["GP2"]["alpha"])

    ev = clause_values
    gp2["clause_values"] = ev
    required = [c["id"] for c in g["GP2"].get("clauses", []) if c.get("required", True)]
    optional = [c["id"] for c in g["GP2"].get("clauses", []) if not c.get("required", True)]
    missing = [cid for cid in required if ev.get(cid, {}).get("pass") is None]
    if missing:
        gp2["pass"] = None
        gp2["unevaluated_required_clauses"] = missing
        gp2["terminal"] = "CANNOT_CHECK_ALTERNATE_CHANNEL_RETENTION"
    else:
        gp2["GP2a_dormant_variable_present_where_registered"] = all(ev[cid]["pass"] for cid in required)
        gp2["GP2b_kv_survival_control"] = all(ev.get(cid, {}).get("pass") for cid in optional) if optional else None
        gp2["pass"] = gp2["GP2a_dormant_variable_present_where_registered"]
        if not gp2["pass"]:
            gp2["terminal"] = "INTERVENTION_DID_NOT_REMOVE_DORMANT_INFORMATION"
        elif gp2["GP2b_kv_survival_control"]:
            gp2["terminal"] = "INTERVENTION_REMOVED_REGISTERED_DORMANT_INFORMATION__KV_SURVIVAL_CONTROL_CONFIRMED"
        elif ev.get("GP2b.probe_kv_retained_decodes", {}).get("pass"):
            gp2["terminal"] = "INTERVENTION_REMOVED_REGISTERED_DORMANT_INFORMATION__KV_INFORMATION_RETAINED_BUT_NOT_USED"
        else:
            gp2["terminal"] = "INTERVENTION_REMOVED_REGISTERED_DORMANT_INFORMATION__KV_SURVIVAL_CONTROL_NOT_REPRODUCED"
    out["GP2"] = gp2
    # Design V2: competence gate (dev split only) is carried into the rollup as a report, not a gate.
    gpc_path = mdir / "competence_gate.json"
    if gpc_path.exists():
        gpc = read_json(gpc_path)
        out["GPC"] = {k: gpc[k] for k in ("pass", "verdict", "maintain_accuracy_R0", "update_accuracy_R0", "by_family", "condition") if k in gpc}
    # Shape 5 guard, per model: the set of clause ids the runner produced must equal the set
    # the design registered, and every one must have been reachable.  A shortfall is a hard
    # terminal -- never a pass on the clauses that did run.
    out["clause_coverage"] = certify_clause_coverage(
        design, out,
        (read_json(mdir / "probe.json") if (mdir / "probe.json").exists() else {}).get("identifiability", {"conditions": {}}),
    )
    out["terminal"] = model_terminal(out)
    return out


def model_terminal(a: dict) -> str:
    # A registered clause that was never evaluated, or that this run's inputs could not have
    # decided, outranks every empirical outcome.  V1 mapped GP2a on the half it implemented;
    # V3 refuses to map it at all.
    cov = a.get("clause_coverage")
    if cov is not None and not cov.get("passes", True):
        return "REGISTERED_CLAUSE_NOT_EVALUATED__SUITE_NOT_INTERPRETABLE"
    gp0, gp1, gp2, gp3 = a["GP0"].get("pass"), a["GP1"].get("pass"), a["GP2"].get("pass"), a["GP3"].get("pass")
    if gp0 is None or gp1 is None:
        return "INCOMPLETE__STAGES_MISSING"
    if not gp0:
        return "CURRENT_STATE_DEFICIT__NOT_PROSPECTIVE_EVIDENCE"
    if gp3 is None:
        return "INCOMPLETE__CONTROL_FAMILIES_MISSING"
    if not gp3:
        return "CONTROL_FAILURE__SUITE_NOT_INTERPRETABLE"
    if gp2 is None:
        return "CANNOT_CHECK_ALTERNATE_CHANNEL_RETENTION"
    if not gp2:
        return a["GP2"]["terminal"]
    if gp1:
        return "P2_PROSPECTIVE_REVISION_STATE_REQUIRED"
    cb = a["GP1"]["contrast_B_R2_vs_R3_on_P2"]
    if cb["acc_x"] >= 0.85 and cb["acc_y"] >= 0.85:
        return "P0_CURRENT_AND_PROSPECTIVE_SUFFICIENT"
    if not a["GP1"]["r3_competence_floor_met"]:
        return "ORDINARY_REASONING_FAILURE_DESPITE_RETAINED_STATE"
    return "NO_MECHANISM_EFFECT__PROSPECTIVE_AUGMENTATION_REDUNDANT"


def stage_rollup(args, design) -> dict:
    workdir = Path(args.workdir)
    runs = sorted(p for p in (workdir / "runs").glob(f"*__{args.split}") if p.is_dir()) if (workdir / "runs").exists() else []
    per_model = {p.name.split("__")[0]: analyse_model(design, p) for p in runs}
    required = [m["alias"] for m in design["models"]] if args.backend == "hf" else sorted(per_model)
    all_present = all(m in per_model for m in required) and bool(required)
    gp1_all = all_present and all(per_model[m]["GP1"].get("pass") for m in required)
    terminals = {m: per_model[m]["terminal"] for m in per_model}
    if not all_present:
        overall = "INCOMPLETE__MODELS_MISSING"
    elif all(t == "P2_PROSPECTIVE_REVISION_STATE_REQUIRED" for t in terminals.values()):
        overall = "P2_PROSPECTIVE_REVISION_STATE_REQUIRED__BOTH_MODELS"
    elif any(t == "P2_PROSPECTIVE_REVISION_STATE_REQUIRED" for t in terminals.values()):
        overall = "P2_SINGLE_MODEL_ONLY__REGISTERED_BOUNDARY_RESULT"
    else:
        overall = "REGISTERED_NEGATIVE_OR_BOUNDARY__" + "|".join(sorted(set(terminals.values())))
    # Clause coverage is aggregated across models and reported at the top of the rollup, so a
    # reader cannot reach the terminal without passing the sentence that says whether every
    # registered clause ran.  If any model is short, the overall terminal is overridden.
    cov_pass = all(per_model[m].get("clause_coverage", {}).get("passes", True) for m in per_model) if per_model else False
    missing_clauses = sorted({cid for m in per_model for cid in per_model[m].get("clause_coverage", {}).get("unevaluated_or_unreachable", [])})
    if per_model and not cov_pass:
        overall = "REGISTERED_CLAUSE_NOT_EVALUATED__SUITE_NOT_INTERPRETABLE"
    any_cannot_check = any(str(t).startswith("CANNOT_CHECK") or per_model[m]["GP2"].get("pass") is None for m, t in terminals.items())
    routing = design["routing"]["full_pass"] if overall.startswith("P2_PROSPECTIVE_REVISION_STATE_REQUIRED__BOTH") else design["routing"]["any_fail"]
    rollup = {
        "schema_version": ROLLUP_SCHEMA, "design_id": design["design_id"], "split": args.split, "generated_at_unix": int(time.time()),
        "runner_sha256": sha256_file(Path(__file__)), "design_sha256": sha256_file(Path(args.design)),
        "suite_sha256": read_json(suite_path(workdir, args.split).with_suffix(".sha256.json"))["sha256"] if suite_path(workdir, args.split).exists() else None,
        "three_history_control": three_history_control(), "gate_B": "CANNOT_CHECK_ALTERNATE_CHANNEL_CAUSAL_USE (omitted prospectively)",
        "models": per_model, "terminals": terminals, "GP1_all_models": gp1_all, "overall_terminal": overall, "routing": routing,
        "scientific_authority": False, "protected_split": args.split == "protected",
        "clause_coverage_passes": cov_pass, "unevaluated_or_unreachable_clauses": missing_clauses,
        "any_cannot_check": any_cannot_check,
    }
    stem = rollup_basename(design)
    rollup["rollup_basename"] = stem
    write_json(workdir / f"{stem}__{args.split}.json", rollup)
    (workdir / f"{stem}__{args.split}.md").write_text(rollup_markdown(rollup), encoding="utf-8")
    return {"overall_terminal": overall, "terminals": terminals,
            "clause_coverage_passes": cov_pass, "unevaluated_or_unreachable_clauses": missing_clauses,
            "any_cannot_check": any_cannot_check}


def _fmt(x) -> str:
    if isinstance(x, float):
        return "nan" if math.isnan(x) else f"{x:.3f}"
    return str(x)


def rollup_markdown(r: dict) -> str:
    version = "V2" if r.get("rollup_basename", "").endswith("V2") else "V1"
    lines = [f"# PRA real-LLM audit rollup {version} — split `{r['split']}`", "", f"design `{r['design_id']}` · runner sha256 `{r['runner_sha256'][:16]}…` · suite sha256 `{(r['suite_sha256'] or 'none')[:16]}…`", "", f"**Overall terminal:** `{r['overall_terminal']}`", "", f"**Routing:** {r['routing']}", "",
             f"**Registered-clause coverage:** {'ALL CLAUSES EVALUATED AND REACHABLE' if r.get('clause_coverage_passes') else 'SHORTFALL — ' + ', '.join(r.get('unevaluated_or_unreachable_clauses') or ['(unknown)'])}", "", "| model | GP0 | GP1 | GP2 | GP3 | terminal |", "|---|---|---|---|---|---|"]
    for m, a in r["models"].items():
        lines.append(f"| {m} | {a['GP0'].get('pass')} | {a['GP1'].get('pass')} | {a['GP2'].get('pass')} | {a['GP3'].get('pass')} | `{a['terminal']}` |")
    for m, a in r["models"].items():
        lines += ["", f"## {m}", ""]
        if a.get("GPC"):
            gpc = a["GPC"]
            lines.append(f"- GPC competence (dev split, {gpc.get('condition', 'R0')}): maintain {_fmt(gpc['maintain_accuracy_R0']['acc'])} (n={gpc['maintain_accuracy_R0']['n']}), update {_fmt(gpc['update_accuracy_R0']['acc'])} (n={gpc['update_accuracy_R0']['n']}) → `{gpc['verdict']}`")
        if a["GP1"].get("contrast_B_R2_vs_R3_on_P2"):
            cb = a["GP1"]["contrast_B_R2_vs_R3_on_P2"]
            lines.append(f"- Contrast B (R2→R3, P2 canonical): acc {_fmt(cb['acc_x'])} → {_fmt(cb['acc_y'])} (n={cb['n']}, discordant {cb['discordant_x_only']}/{cb['discordant_y_only']}, exact p={_fmt(cb['p_two_sided_exact'])})")
        if a["GP1"].get("contrast_B_same_fibre_R2_vs_R3"):
            cs = a["GP1"]["contrast_B_same_fibre_R2_vs_R3"]
            csi = a["GP1"]["contrast_B_same_fibre_instance_level"]
            lines.append(f"- Contrast B-SF (R2→R3, same-successor-fibre variant, secondary): acc {_fmt(cs['acc_x'])} → {_fmt(cs['acc_y'])} (n={cs['n']}, exact p={_fmt(cs['p_two_sided_exact'])}; instance-level p={_fmt(csi['p_two_sided_exact'])})")
        if a["GP0"].get("tost_R3_minus_R2"):
            t = a["GP0"]["tost_R3_minus_R2"]
            lines.append(f"- GP0 present equivalence: per-unit pass {_fmt(a['GP0']['per_unit_pass_fraction'])}; TOST mean Δlogprob {_fmt(t.get('mean_diff', float('nan')))} (equivalent={t.get('equivalent')})")
        if a["GP2"].get("probe_max_test_acc"):
            lines.append("- Probe max test acc: " + ", ".join(f"{c}={_fmt(v)}" for c, v in a["GP2"]["probe_max_test_acc"].items()))
        if a["GP2"].get("probe_surface_null"):
            lines.append("- Model-free surface null (max of lexical/relational readers): " + ", ".join(
                f"{c}={_fmt((v or {}).get('max_surface_null'))}" for c, v in a["GP2"]["probe_surface_null"].items()))
        if a["GP2"].get("suppressed_conditions"):
            lines.append("- Conditions with NO reportable accuracy (label not identifiable): " + ", ".join(
                f"`{c}`" for c in a["GP2"]["suppressed_conditions"]))
        if a["GP2"].get("contrast_D_R2_vs_kv_retained"):
            d = a["GP2"]["contrast_D_R2_vs_kv_retained"]
            w = a["GP2"].get("contrast_D_same_path_witness") or {}
            lines.append(f"- Contrast D (R2 → KV retained): acc {_fmt(d['acc_x'])} → {_fmt(d['acc_y'])} (exact p={_fmt(d['p_two_sided_exact'])}); terminal `{a['GP2'].get('terminal')}`")
            lines.append(f"- Same-path witness for contrast D: {w.get('witness_contrast')} returned {_fmt(w.get('witness_acc_x'))} vs {_fmt(w.get('witness_acc_y'))} — differs: {w.get('differs')}")
        if a["GP1"].get("certificates"):
            lines.append("- Incompatible-cell rate by condition: " + ", ".join(f"{c}={_fmt(v['incompatible_cell_rate'])}" for c, v in sorted(a["GP1"]["certificates"].items())))
        if a["GP1"].get("metrics_by_family_condition"):
            lines += ["", "| family | " + " | ".join(CONDITIONS) + " |", "|---|" + "---|" * len(CONDITIONS)]
            for fam, row in a["GP1"]["metrics_by_family_condition"].items():
                lines.append(f"| {fam} | " + " | ".join(_fmt(row[c]["accuracy"]["acc"]) for c in CONDITIONS) + " |")
    lines += ["", f"Three-history joint-intersection control passes: {r['three_history_control']['passes']}", "", "No scientific authority is granted by this file; routing requires a new manuscript version and freeze."]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- CLI

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--stage", required=True, choices=["generate-suite", "certify", "present-gate", "revision", "probe", "kv-channel", "competence-gate", "rollup", "all"])
    p.add_argument("--protected-seed-file", default=None, help="design V2: sealed protected seed file ('<int>:<salt>'); its sha256 must equal design.suite_generator.seed.protected_commitment_sha256")
    p.add_argument("--workdir", required=True)
    p.add_argument("--design", default=str(DEFAULT_DESIGN))
    p.add_argument("--model", default="stub", help="model alias from the design JSON (or 'stub')")
    p.add_argument("--backend", default="hf", choices=["hf", "stub"])
    p.add_argument("--stub-variant", default="planted", choices=["planted", "null"])
    p.add_argument("--split", default="dev", choices=["dev", "protected"])
    p.add_argument("--protected-authorization", default="", help="must equal design.protected_run.authorization_token to touch the protected split")
    p.add_argument("--max-instances", type=int, default=None, help="dev split only: cap total instances (round-robin across families)")
    p.add_argument("--families", default=None, help="dev split only: comma-separated family filter (smoke tests)")
    p.add_argument("--suite-scale", type=int, default=None, help="generate-suite: set dev instances per family (dev split only; protected counts are frozen)")
    p.add_argument("--device", default="cuda", help="'cuda' (one GPU) or 'auto' (layer-wise sharding across all visible GPUs, GPU-only)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    design = load_design(Path(args.design))
    if args.split == "protected" and args.stage != "generate-suite":
        if args.protected_authorization != design["protected_run"]["authorization_token"]:
            raise SystemExit("protected split requires --protected-authorization matching the design (protected run not authorized)")
    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    stages = ["generate-suite", "certify", "present-gate", "revision", "probe", "kv-channel", "rollup"] if args.stage == "all" else [args.stage]
    backend: Backend | None = None
    summary = {}
    for stage in stages:
        if stage == "generate-suite":
            summary[stage] = stage_generate_suite(args, design)
        elif stage == "rollup":
            summary[stage] = stage_rollup(args, design)
        elif stage == "certify":
            summary[stage] = stage_certify(args, design)
        elif stage == "competence-gate":
            if args.backend == "stub" and args.model == "stub":
                args.model = f"stub-{args.stub_variant}"
            summary[stage] = stage_competence_gate(args, design)
        else:
            if backend is None:
                backend = make_backend(args, design)
                if args.backend == "stub" and args.model == "stub":
                    args.model = f"stub-{args.stub_variant}"
            fn = {"present-gate": stage_present_gate, "revision": stage_revision, "probe": stage_probe, "kv-channel": stage_kv_channel}[stage]
            summary[stage] = fn(args, design, backend)
        print(json.dumps({"stage": stage, "model": args.model, "split": args.split, "summary": summary[stage]}, sort_keys=True, default=str), flush=True)
    receipt = {"schema_version": RESULT_SCHEMA, "runner_sha256": sha256_file(Path(__file__)), "design_sha256": sha256_file(Path(args.design)), "argv": argv if argv is not None else sys.argv[1:], "summary": summary}
    write_json(workdir / "receipts" / f"receipt_{args.model}_{args.split}_{'-'.join(stages)}_{int(time.time())}.json", receipt)

    # Distinct exit codes: "could not check" must never be indistinguishable from
    # "checked and fine".  4 outranks 3 -- a design defect is worse news than a gap.
    code = 0
    if "certify" in summary and not summary["certify"].get("passes", True):
        code = 4
    if "rollup" in summary:
        roll = summary["rollup"]
        if roll.get("clause_coverage_passes") is False:
            code = 4
        elif code != 4 and roll.get("any_cannot_check"):
            code = 3
    return code


if __name__ == "__main__":
    raise SystemExit(main())

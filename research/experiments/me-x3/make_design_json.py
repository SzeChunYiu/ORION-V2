#!/usr/bin/env python3
"""Emit the frozen design JSON from the frozen code constants (no hand-typed drift)."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mex3_generator import (ALPHABET, ORACLE_EXPANSIONS, ORACLE_MODEL_SIZE, ORACLE_WORD_LEN,
                            TASK_BUDGET, F7_SUBTYPES, F7_WEIGHTS, MAX_ATTEMPTS)
from mex3_model import ACTIONS, FAMILIES, FIDELITY_VERDICTS, TERMINALS, VALIDITY_VERDICTS
from mex3_arms import B5_ARM, LADDER, M_ARM, OBSTRUCTIONS, arm_specs
from mex3_run import (ABLATION_FOR_FAMILY, ALPHA, DEV_PER_FAMILY, DEV_SEED, G2_MARGIN,
                      NO_ESCALATION_FAMILIES, PROTECTED_PER_FAMILY)
from mex3_verdict import LEMMA_POOL_CAP, LEMMA_POOL_MAX_LEN

SEED_FILE = Path.home() / ".orion-custody/me-x3/PROTECTED_SEED_V1.txt"
CODE = ("mex3_model.py", "mex3_oracle.py", "mex3_verdict.py", "mex3_generator.py",
        "mex3_arms.py", "mex3_parents.py", "mex3_run.py", "mex3_lean.py")

d = {
  "schema_version": "orion.v2.me-x3.exact-study-design.v1",
  "study": "ME-X3", "state_date": "2026-09-02", "status": "FROZEN_DESIGN_NO_PROTECTED_OUTCOME_INSPECTED",
  "protocols_served": [
    "research/experiments/ME_X3_FORMAL_MATHEMATICS_PROTOCOL_V1.md",
    "research/experiments/MACHINE_EPISTEMICS_ME_X3_FORMAL_MATH_PROTOCOL_V1.md",
    "research/experiments/MACHINE_EPISTEMICS_DECISIVE_STUDIES_PROTOCOL_V1.md (0-2, 5)",
    "research/field/MACHINE_EPISTEMICS_EXTENSION_HYPOTHESES_2026_09_02_V1.md (H-EXT-3)"],
  "verifier": {
    "primary": "exhaustive rewrite search over a finite equational theory (mex3_oracle)",
    "external_cross_check": "Lean 4 kernel, inductive Derives proof terms, no Mathlib",
    "lean_version": "4.33.1", "lean_commit": "819816b2e0a3bf405af45ae5c7af2491d8f5bee6",
    "elan_version": "4.2.3", "mathlib": None,
    "mathlib_exclusion_reason":
      "an unbounded library destroys oracle exactness: the minimum-escalation oracle "
      "is defined by exhaustive search over a registered finite intervention space, "
      "and a Mathlib-scale library makes the retrieval level uncomputable rather than "
      "merely expensive. Mathlib contributes no lemmas about the generated, "
      "symbol-renamed presentations used here.",
    "scope_limit":
      "this establishes the proof-validity / specification-fidelity separation on a "
      "finite system with an exhaustive oracle. It does NOT establish controller "
      "behaviour at Mathlib scale, where no such oracle exists."},
  "object_system": {
    "terms": "words over a finite alphabet of unary operator symbols",
    "statements": "schematic equations lhs =?= rhs, universally quantified in the schema variable",
    "derivation": "two-sided factor rewriting (Birkhoff derivation for a unary signature)",
    "models": "finite sets [0,n) with one function per symbol; a model falsifying a "
              "statement certifies non-derivability",
    "alphabet": ALPHABET, "alternative_presentation": "Tietze: add generator g := d, fold d into g"},
  "budget": TASK_BUDGET.as_dict() | {
    "note": "identical for every arm; max_expansions is the total account across all "
            "module calls, solve_expansions caps any single solving search and is the "
            "cap the oracle's level test uses. Both were fixed on the DEVELOPMENT "
            "split to avoid ceiling and floor effects, before any protected run."},
  "oracle_caps": {"word_len": ORACLE_WORD_LEN, "expansions": ORACLE_EXPANSIONS,
                  "model_size": ORACLE_MODEL_SIZE,
                  "lemma_pool_cap": LEMMA_POOL_CAP, "lemma_pool_max_word_len": LEMMA_POOL_MAX_LEN},
  "families": list(FAMILIES),
  "f7_proposal_weights": dict(zip(F7_SUBTYPES, F7_WEIGHTS)),
  "f7_realized_mixture": "reported by the analysis; rejection sampling reshapes the proposal weights",
  "registered_actions": list(ACTIONS),
  "fidelity_verdicts": list(FIDELITY_VERDICTS),
  "validity_verdicts": list(VALIDITY_VERDICTS),
  "terminals": list(TERMINALS),
  "obstruction_hypotheses": list(OBSTRUCTIONS),
  "escalation_levels": ["L0_REFUTE", "L1_DIRECT", "L2_RETRIEVE", "L3_INVENT",
                        "L4_REPRESENTATION", "L5_DEFER"],
  "arms": [s.name for s in arm_specs()],
  "primary_comparator": B5_ARM, "candidate": M_ARM,
  "interface_ladder": {"rungs": LADDER, "hypothesis": "H-EXT-3",
    "parity_rule":
      "The ladder is a property of the FEDERATION'S INTERNAL CHANNEL ALPHABET, never "
      "of M's privilege. G1 compares M against the TOP RUNG, which receives exactly "
      "what M receives. The study is invalid if M is given any task information, "
      "module report, or oracle label that the top-rung federation is not given."},
  "gates": {
    "G0": "oracle self-agreement (two independent searches; fast-path vs brute-force "
          "model enumeration), hand-authored known-answer fixtures, parent fidelity, "
          "null calibration on a trivial identity",
    "G1": f"M vs {B5_ARM} on the joint endpoint (validity AND fidelity AND minimal "
          f"action), paired exact binomial, alpha={ALPHA}, reported per family and pooled",
    "G2": f"anti-conservatism: on {list(NO_ESCALATION_FAMILIES)} M's false-change and "
          f"false-defer rates, and pooled false-drift-alarm rate, may not exceed B5's "
          f"by more than {G2_MARGIN}",
    "G3": "mechanism by omission: the registered ablation must degrade the family it "
          "controls",
    "G4": "H-EXT-3 ladder monotonicity and terminal"},
  "ablation_for_family": ABLATION_FOR_FAMILY,
  "routes": ["PARENT_SUFFICIENT", "ME_RESIDUAL_SUPPORTED", "SPECIFICATION_FIDELITY_RESIDUAL",
             "MECHANISM_UNSUPPORTED", "CANNOT_CHECK"],
  "pre_registered_expectation": {
    "route": "PARENT_SUFFICIENT",
    "reason": "the top-rung federation runs the same specification check and the same "
              "escalation modules; M's declared delta is control, and on an exhaustive "
              "finite oracle a well-ordered cascade with the same information is "
              "expected to reach the same decisions. The decisive content is (a) the "
              "proof-only parents' systematic fidelity blindness, (b) the ablations, "
              "(c) the ladder, (d) cost.",
    "ladder_terminal": "RESIDUAL_IS_INTERFACE_STANDARD_NOT_CONTROL"},
  "no_rescue_clause":
    "No threshold, family, arm, budget, generator constant or gate may be changed "
    "after any protected outcome has been inspected. The protected stage runs exactly "
    "once and `analyze` runs exactly once on its output. A PARENT_SUFFICIENT or "
    "CANNOT_CHECK terminal is a successful scientific outcome and may not be repaired.",
  "delta_from_me_x1_family_8":
    "ME-X1 case family 8 ('formal proof / wrong specification') scored one "
    "transition-decision among ten families. ME-X3 makes specification fidelity a "
    "CO-PRIMARY endpoint over a dedicated stratum with registered drift subtypes "
    "(materially weakened / materially strengthened / notational collapse / abstraction "
    "elevation / degenerate trivialization / cannot-check), adjudicated by explicit "
    "interderivability or separating-model witnesses, and reports it separately from "
    "proof validity so that a pooled score cannot absorb it.",
  "splits": {"development": {"seed": DEV_SEED, "per_family": DEV_PER_FAMILY, "public": True},
             "protected": {"per_family": PROTECTED_PER_FAMILY, "seed": "SEALED_IN_CUSTODY"},
             "rejection_sampling_max_attempts": MAX_ATTEMPTS},
  "custody": {"seed_file": "~/.orion-custody/me-x3/PROTECTED_SEED_V1.txt",
              "protected_seed_sha256": hashlib.sha256(SEED_FILE.read_bytes()).hexdigest()},
  "code_sha256": {f: hashlib.sha256((HERE / f).read_bytes()).hexdigest() for f in CODE},
}
out = HERE / "ME_X3_FORMAL_MATHEMATICS_EXACT_STUDY_DESIGN_V1.json"
out.write_text(json.dumps(d, indent=2, sort_keys=True) + "\n")
print(out.name, hashlib.sha256(out.read_bytes()).hexdigest())

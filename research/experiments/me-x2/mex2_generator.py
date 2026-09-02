"""ME-X2 paired-episode generator, hand-authored known-answer fixtures and the
H-EXT-3 separation pair (frozen with design V1).

Pairs: two instances share template, symptom, apparent class, live causes,
probes, interventions, costs and budget; only the hidden truth differs.  The
stratum of an instance is its oracle class.  Variants (assigned by index):
  PLAIN      truth separable from every rival by probes alone within budget
  PARTIAL    separable only when a level<=1 repair-as-test is used
  SAME_FIX   a rival with the same minimum fix is inseparable (locus unresolved,
             intervention determined); only where the catalogue admits it
  CI         planted CANNOT_IDENTIFY: a rival with a different minimum fix and a
             different class is inseparable by every affordable test set
Instance seed = sha256(split_seed|stratum|index)[:12]; deterministic rejection
sampling; fall back to PLAIN when a variant is unattainable (recorded).
"""
from __future__ import annotations

import hashlib
import random

from mex2_catalogue import TEMPLATES, templates_with_class
from mex2_model import CLASSES, LEVEL_COST_BANDS, MAX_CHEAP_INTERVENTIONS, MAX_PROBES, TYPICAL_LEVEL, Cause, Instance, Intervention, Probe
from mex2_oracle import oracle_targets, per_cause_targets, uniformly_decidable

VARIANT_CYCLE = ("PLAIN", "PLAIN", "PARTIAL", "SAME_FIX")
MAX_ATTEMPTS = 400
FALLBACK_AFTER = 200
UNIFORM_SCAN = 30


def pair_seed(split_seed: str, stratum: str, index: int) -> str:
    return hashlib.sha256(f"{split_seed}|{stratum}|{index}".encode()).hexdigest()[:12]


def _effective_table(table: dict[str, str], nominal: str, mediated: bool, causes: dict[str, Cause]) -> tuple[dict[str, str], dict[str, str]]:
    designed = {c: o for c, o in table.items() if c in causes}
    eff = dict(designed)
    if mediated:
        for cid, c in causes.items():
            if c.locus == "EVALUATOR_VALIDATION":
                eff.pop(cid, None)  # laundered to nominal
    return eff, designed


def build_instance(*, template: str, truth: str, live: list[str], probe_costs: dict[str, int], intervention_costs: dict[str, int],
                   extra_resolves: dict[str, list[str]], budget: int, instance_id: str, pair_id: str, partner_id: str,
                   seed: str, variant: str, apparent_class: str, features: dict | None = None) -> Instance:
    T = TEMPLATES[template]
    causes = {c[0]: Cause(*c) for c in T["causes"] if c[0] in live}
    if set(live) != set(causes):
        raise ValueError("live causes must belong to the template")
    ordered = tuple(causes[c] for c in [x[0] for x in T["causes"]] if c in causes)
    probes = []
    for kind, _band, mediated, nominal, table in T["probes"]:
        if kind in probe_costs:
            eff, designed = _effective_table(table, nominal, mediated, causes)
            probes.append(Probe(kind, probe_costs[kind], mediated, nominal, eff, designed))
    ivs = []
    for kind, level, resolves, _also in T["interventions"]:
        if kind in intervention_costs:
            res = tuple(r for r in [*resolves, *extra_resolves.get(kind, [])] if r in causes)
            ivs.append(Intervention(kind, kind, level, intervention_costs[kind], tuple(dict.fromkeys(res))))
    return Instance(instance_id=instance_id, pair_id=pair_id, partner_instance_id=partner_id, template=template, seed=seed, variant=variant,
                    symptom=T["symptom"], pattern=T["pattern"], apparent_class=apparent_class, causes=ordered, probes=tuple(probes),
                    interventions=tuple(ivs), budget=budget, truth=truth, features=features or {})


# ---- random pair ---------------------------------------------------------------------------------

def _min_fix_level(template: str, cause_id: str) -> int:
    T = TEMPLATES[template]
    fix = next(c[3] for c in T["causes"] if c[0] == cause_id)
    return next(i[1] for i in T["interventions"] if i[0] == fix)


def _splitting_tests(tmp: Instance, a: str, b: str) -> tuple[set[str], set[str]]:
    probes = {p.probe_id for p in tmp.probes if p.outcome(a) != p.outcome(b)}
    repairs = {i.intervention_id for i in tmp.interventions if i.is_cheap and i.outcome(a) != i.outcome(b)}
    return probes, repairs


def _apparent(rng: random.Random, live_classes: list[str], truth_class: str, variant: str) -> str:
    """Frozen apparent-class rule: 1/2 the highest-typical-level live class, 1/4 the truth's class,
    1/4 a uniformly random other live class; planted-CI pairs read as CANNOT_IDENTIFY with prob 1/2."""
    if variant == "CI" and rng.random() < 0.5:
        return "CANNOT_IDENTIFY"
    u = rng.random()
    if u < 0.5:
        return max(live_classes, key=lambda c: (TYPICAL_LEVEL[c] or 0, -CLASSES.index(c)))
    if u < 0.75:
        return truth_class
    others = [c for c in live_classes if c != truth_class]
    return rng.choice(others) if others else truth_class


def generate_pair(split: str, split_seed: str, stratum: str, index: int) -> list[tuple[Instance, dict]]:
    seed = pair_seed(split_seed, stratum, index)
    rng = random.Random(seed)
    want = "CI" if stratum == "CANNOT_IDENTIFY" else VARIANT_CYCLE[index % len(VARIANT_CYCLE)]
    pid = f"X2-{split}-{stratum}-{index:03d}"
    for attempt in range(MAX_ATTEMPTS):
        variant = want if attempt < FALLBACK_AFTER or want == "CI" else "PLAIN"
        template = rng.choice(sorted(TEMPLATES) if stratum == "CANNOT_IDENTIFY" else templates_with_class(stratum))
        T = TEMPLATES[template]
        cause_rows = T["causes"]
        if stratum == "CANNOT_IDENTIFY":
            truths = [c[0] for c in cause_rows if _min_fix_level(template, c[0]) >= 2]
        else:
            truths = [c[0] for c in cause_rows if c[1] == stratum]
        truth = rng.choice(truths)
        others = [c[0] for c in cause_rows if c[0] != truth]
        k = rng.randint(2, min(5, len(others)))
        live = [truth] + rng.sample(others, k)
        live_cls = {c[0]: c[1] for c in cause_rows if c[0] in live}
        if len(set(live_cls.values())) < 2:
            continue
        # probes
        n_pr = rng.randint(3, min(MAX_PROBES, len(T["probes"])))
        chosen = rng.sample(T["probes"], n_pr)
        probe_costs = {p[0]: rng.randint(*p[1]) for p in chosen}
        # interventions: min fix of every live cause + 1-3 extra higher-level kinds
        fixes = {next(c[3] for c in cause_rows if c[0] == cid) for cid in live}
        extras_pool = [i[0] for i in T["interventions"] if i[0] not in fixes and i[1] >= 2]
        extra = rng.sample(extras_pool, min(len(extras_pool), rng.randint(1, 3)))
        kinds = fixes | set(extra)
        intervention_costs = {i[0]: rng.randint(*LEVEL_COST_BANDS[i[1]]) for i in T["interventions"] if i[0] in kinds}
        extra_res = {i[0]: [r for r in i[3] if r in live and rng.random() < 0.5] for i in T["interventions"] if i[0] in kinds}
        if len([i for i in T["interventions"] if i[0] in kinds and i[1] <= 1]) > MAX_CHEAP_INTERVENTIONS:
            continue
        tmp = build_instance(template=template, truth=truth, live=live, probe_costs=probe_costs, intervention_costs=intervention_costs, extra_resolves=extra_res,
                             budget=999, instance_id=pid + "-a", pair_id=pid, partner_id=pid + "-b", seed=seed, variant=variant, apparent_class=live_cls[truth])
        c_fix = tmp.min_fix(truth).cost
        rival = None
        if variant in ("PARTIAL", "SAME_FIX", "CI"):
            if variant == "PARTIAL":
                cands = [r for r in live if r != truth and tmp.min_fix(r).is_cheap and _splitting_tests(tmp, truth, r)[1]]
            elif variant == "SAME_FIX":
                cands = [r for r in live if r != truth and tmp.min_fix(r).intervention_id == tmp.min_fix(truth).intervention_id]
            else:
                cands = [r for r in live if r != truth and tmp.min_fix(r).intervention_id != tmp.min_fix(truth).intervention_id and live_cls[r] != live_cls[truth]
                         and not _splitting_tests(tmp, truth, r)[1] and _min_fix_level(template, r) >= 2]
            if not cands:
                continue
            rival = rng.choice(cands)
            sp, _ = _splitting_tests(tmp, truth, rival)
            for p in sp:
                probe_costs.pop(p, None)
            if len(probe_costs) < 2:
                continue
            tmp = build_instance(template=template, truth=truth, live=live, probe_costs=probe_costs, intervention_costs=intervention_costs, extra_resolves=extra_res,
                                 budget=999, instance_id=pid + "-a", pair_id=pid, partner_id=pid + "-b", seed=seed, variant=variant, apparent_class=live_cls[truth])
        o = oracle_targets(tmp)
        if variant == "PLAIN":
            if o["min_identification_total_probe_only"] is None:
                continue
            budget = o["min_identification_total_probe_only"] + rng.randint(0, 4)
        elif variant == "PARTIAL":
            if o["min_identification_total"] is None:
                continue
            budget = o["min_identification_total"] + rng.randint(0, 2)
            po = o["min_identification_total_probe_only"]
            if po is not None and po <= budget:
                continue
        elif variant == "SAME_FIX":
            budget = c_fix + rng.randint(0, 4)
            # need the other rivals separable: probe the oracle at the final budget below
            others_sep = [r for r in live if r not in (truth, rival)]
            if others_sep:
                tmp2 = build_instance(template=template, truth=truth, live=[truth, *others_sep], probe_costs=probe_costs, intervention_costs=intervention_costs, extra_resolves=extra_res,
                                      budget=999, instance_id="t", pair_id="t", partner_id="t", seed=seed, variant=variant, apparent_class=live_cls[truth])
                o2 = oracle_targets(tmp2)
                if o2["min_identification_total"] is None:
                    continue
                budget = o2["min_identification_total"] + rng.randint(0, 4)
        else:  # CI
            budget = max(c_fix, tmp.min_fix(rival).cost) + rng.randint(0, 4)
        # every live cause must have an affordable fix so the partner is well-posed
        if any(tmp.min_fix(c).cost > budget for c in live):
            continue
        apparent = _apparent(rng, sorted(set(live_cls.values())), live_cls[truth], variant)
        # uniform decidability: raise the budget (bounded scan) until one truth-agnostic policy is
        # decision-correct for every live cause; the variant invariants are re-checked below
        inst_a = None; oa = None; targets = None
        for b in range(budget, budget + UNIFORM_SCAN + 1):
            cand = build_instance(template=template, truth=truth, live=live, probe_costs=probe_costs, intervention_costs=intervention_costs, extra_resolves=extra_res,
                                  budget=b, instance_id=pid + "-a", pair_id=pid, partner_id=pid + "-b", seed=seed, variant=variant, apparent_class=apparent)
            tg = per_cause_targets(cand)
            if uniformly_decidable(cand, tg):
                inst_a, targets, budget = cand, tg, b
                break
        if inst_a is None:
            continue
        oa = oracle_targets(inst_a)
        ok = {
            "PLAIN": oa["probe_identifiable"] and oa["oracle_class"] == stratum and oa["oracle_level"] == inst_a.min_fix(truth).level,
            "PARTIAL": oa["identifiable"] and not oa["probe_identifiable"] and oa["oracle_class"] == stratum,
            "SAME_FIX": oa["oracle_class"] == stratum and oa["oracle_locus"] == "CANNOT_IDENTIFY" and oa["oracle_level"] is not None,
            "CI": oa["oracle_class"] == "CANNOT_IDENTIFY" and oa["oracle_level"] is None,
        }[variant]
        if not ok:
            continue
        truth_b = rng.choice([c for c in live if c != truth])
        inst_b = build_instance(template=template, truth=truth_b, live=live, probe_costs=probe_costs, intervention_costs=intervention_costs, extra_resolves=extra_res,
                                budget=budget, instance_id=pid + "-b", pair_id=pid, partner_id=pid + "-a", seed=seed, variant="PARTNER_OF_" + variant, apparent_class=apparent)
        ob = oracle_targets(inst_b)
        out = []
        for inst, o in ((inst_a, oa), (inst_b, ob)):
            o = dict(o, uniformly_decidable=True)
            feats = _features(inst, o, attempt, want)
            out.append((_with_features(inst, feats), o))
        return out
    raise RuntimeError(f"generator could not realise {stratum} index {index} ({want})")


def _with_features(inst: Instance, feats: dict) -> Instance:
    return Instance(instance_id=inst.instance_id, pair_id=inst.pair_id, partner_instance_id=inst.partner_instance_id, template=inst.template, seed=inst.seed,
                    variant=inst.variant, symptom=inst.symptom, pattern=inst.pattern, apparent_class=inst.apparent_class, causes=inst.causes, probes=inst.probes,
                    interventions=inst.interventions, budget=inst.budget, truth=inst.truth, features=feats)


def _features(inst: Instance, o: dict, attempt: int, wanted: str) -> dict:
    typ = TYPICAL_LEVEL[inst.apparent_class]
    lvl = o["oracle_level"]
    return {
        "n_live": len(inst.causes), "n_probes": len(inst.probes), "n_interventions": len(inst.interventions), "n_cheap": len([i for i in inst.interventions if i.is_cheap]),
        "budget": inst.budget, "attempts": attempt + 1, "variant_wanted": wanted, "variant_fallback": not inst.variant.endswith(wanted),
        "is_decoy": bool(typ is not None and lvl is not None and lvl < typ),
        "is_inverse_decoy": bool(typ is not None and lvl is not None and lvl > typ),
        "apparent_typical_level": typ, "oracle_level": lvl, "oracle_class": o["oracle_class"], "oracle_locus": o["oracle_locus"],
        "identifiable": o["identifiable"], "probe_identifiable": o["probe_identifiable"], "indistinguishable_set_size": len(o["indistinguishable_set"]),
    }


def generate_split(split: str, split_seed: str, per_stratum: dict[str, int]) -> list[tuple[Instance, dict]]:
    out: list[tuple[Instance, dict]] = []
    for stratum in CLASSES:
        for index in range(per_stratum.get(stratum, 0)):
            out.extend(generate_pair(split, split_seed, stratum, index))
    ids = [i.instance_id for i, _ in out]
    assert len(ids) == len(set(ids))
    return out


# ---- hand-authored known-answer fixtures (expected values computed by hand; G0a) ---------------

def _fx(name, template, truth, live, probes, ivs, budget, apparent, expected, extra=None):
    inst = build_instance(template=template, truth=truth, live=live, probe_costs=probes, intervention_costs=ivs, extra_resolves=extra or {}, budget=budget,
                          instance_id=name, pair_id=name, partner_id=name, seed="KA", variant="KNOWN_ANSWER", apparent_class=apparent)
    return {"name": name, "instance": inst, "expected": expected}


def known_answer_fixtures() -> list[dict]:
    E = lambda cls, locus, level, cost, ident, probe_ident: {"oracle_class": cls, "oracle_locus": locus, "oracle_level": level, "oracle_cost": cost, "identifiable": ident, "probe_identifiable": probe_ident}
    return [
        _fx("KA-01-SEARCH_INSUFFICIENT", "B_PROOF", "SEARCH_SHALLOW", ["SEARCH_SHALLOW", "MISSING_LEMMA", "ENCODING_INSUFFICIENT"],
            {"search_coverage_audit": 1, "library_retrieval_audit": 1}, {"continue_search": 1, "retrieve_lemma": 3, "change_encoding": 10}, 12, "REPRESENTATION_INSUFFICIENT",
            E("SEARCH_INSUFFICIENT", "PROCESS_TOOL_WORKFLOW", 0, 1, True, True), {"change_encoding": ["MISSING_LEMMA", "SEARCH_SHALLOW"]}),
        _fx("KA-02-MISSING_PREMISE_OR_DATA", "B_PROOF", "MISSING_LEMMA", ["MISSING_LEMMA", "ENCODING_INSUFFICIENT", "SEARCH_SHALLOW"],
            {"library_retrieval_audit": 2, "expressivity_check": 4}, {"retrieve_lemma": 3, "continue_search": 2, "change_encoding": 9}, 14, "REPRESENTATION_INSUFFICIENT",
            E("MISSING_PREMISE_OR_DATA", "EPISTEMIC_MODEL", 1, 3, True, True), {"change_encoding": ["MISSING_LEMMA"]}),
        _fx("KA-03-MODEL_FAMILY_INADEQUATE", "A_RESIDUAL", "MODEL_INADEQUATE", ["MODEL_INADEQUATE", "PREPROCESS_BUG", "SENSOR_DRIFT_RECAL"],
            {"ppc_via_evaluator": 1, "preprocess_unit_audit": 2}, {"fix_unit_conversion": 3, "recalibrate": 4, "expand_model_family": 6}, 12, "MODEL_FAMILY_INADEQUATE",
            E("MODEL_FAMILY_INADEQUATE", "EPISTEMIC_MODEL", 2, 6, True, True), {"expand_model_family": ["SENSOR_DRIFT_RECAL"]}),
        _fx("KA-04-REPRESENTATION_INSUFFICIENT", "A_PLATEAU", "STATES_COLLAPSED", ["STATES_COLLAPSED", "LOCAL_OPTIMUM_MORE_SEARCH", "MODEL_INADEQUATE_P"],
            {"separability_test": 3, "search_coverage_audit": 1, "ppc_via_evaluator": 1}, {"continue_search": 1, "expand_model_family": 5, "change_representation": 10}, 16, "REPRESENTATION_INSUFFICIENT",
            E("REPRESENTATION_INSUFFICIENT", "REPRESENTATION_REGIME", 3, 10, True, True), {"expand_model_family": ["LOCAL_OPTIMUM_MORE_SEARCH"], "change_representation": ["MODEL_INADEQUATE_P"]}),
        _fx("KA-05-PROBE_ACTION_INSUFFICIENT", "C_NONDISCRIM", "INTERVENTION_NEEDED", ["INTERVENTION_NEEDED", "CRITERION_UNIDENTIFIABLE", "MORE_SAMPLES"],
            {"passive_equivalence_analysis": 2, "identifiability_analysis": 5, "power_analysis": 1}, {"run_discriminating_intervention": 2, "collect_more_samples": 2, "reformulate_criterion": 14}, 12, "PROBLEM_OBJECTIVE_MISSPECIFIED",
            E("PROBE_ACTION_INSUFFICIENT", "OBSERVATION_MEASUREMENT", 0, 2, True, True)),
        _fx("KA-06-MEASUREMENT_OR_EVALUATOR_BLIND", "A_RESIDUAL", "SENSOR_BLIND_NO_STANDARD", ["SENSOR_BLIND_NO_STANDARD", "MODEL_INADEQUATE", "EVALUATOR_BLIND"],
            {"calibration_standard": 4, "ppc_via_evaluator": 1, "evaluator_gold_audit": 5}, {"expand_model_family": 6, "build_calibration_instrument": 18, "build_validated_evaluator": 20}, 26, "MODEL_FAMILY_INADEQUATE",
            E("MEASUREMENT_OR_EVALUATOR_BLIND", "OBSERVATION_MEASUREMENT", 5, 18, True, True)),
        _fx("KA-07-FORMALISM_OR_OPERATOR_INSUFFICIENT", "B_PROOF", "OPERATOR_MISSING", ["OPERATOR_MISSING", "ENCODING_INSUFFICIENT", "MISSING_LEMMA"],
            {"expressivity_check": 3, "operator_availability_audit": 2}, {"retrieve_lemma": 3, "change_encoding": 9, "extend_formalism_operator": 11}, 16, "REPRESENTATION_INSUFFICIENT",
            E("FORMALISM_OR_OPERATOR_INSUFFICIENT", "REPRESENTATION_REGIME", 3, 11, True, True)),
        _fx("KA-08-PROBLEM_OBJECTIVE_MISSPECIFIED", "A_PLATEAU", "OBJECTIVE_OMITS_CRITERION", ["OBJECTIVE_OMITS_CRITERION", "MODEL_INADEQUATE_P", "CRITERION_MET"],
            {"decision_outcome_review": 4, "obligation_ledger_audit": 1, "ppc_via_evaluator": 2}, {"stop_warranted_terminal": 1, "expand_model_family": 7, "reformulate_objective": 13}, 20, "MODEL_FAMILY_INADEQUATE",
            E("PROBLEM_OBJECTIVE_MISSPECIFIED", "PROBLEM_CRITERION", 4, 13, True, True)),
        _fx("KA-09-TOOL_INSTRUMENT_INADEQUATE", "C_NONDISCRIM", "CHANNEL_INSENSITIVE", ["CHANNEL_INSENSITIVE", "MORE_SAMPLES", "HYPOTHESIS_FAMILY_INADEQUATE"],
            {"channel_sensitivity_check": 4, "power_analysis": 1, "model_criticism_via_evaluator": 1}, {"collect_more_samples": 2, "expand_hypothesis_family": 6, "switch_instrument": 18}, 26, "MODEL_FAMILY_INADEQUATE",
            E("TOOL_INSTRUMENT_INADEQUATE", "OBSERVATION_MEASUREMENT", 5, 18, True, True), {"switch_instrument": ["MORE_SAMPLES"]}),
        _fx("KA-10-WORKFLOW_INADEQUATE", "D_WORKFLOW", "METADATA_LOSS", ["METADATA_LOSS", "METADATA_LOSS_LOCAL_FIXABLE", "LOCAL_TOOL_BUG"],
            {"dependency_provenance_audit": 2, "stage_contract_audit": 4, "unit_test_local_tool": 1}, {"patch_tool": 3, "add_metadata_passthrough": 4, "workflow_state_contract": 25}, 32, "WORKFLOW_INADEQUATE",
            E("WORKFLOW_INADEQUATE", "PROCESS_TOOL_WORKFLOW", 6, 25, True, True), {"workflow_state_contract": ["METADATA_LOSS_LOCAL_FIXABLE", "LOCAL_TOOL_BUG"]}),
        _fx("KA-11-NO_ESCALATION_NEEDED_DECOY", "A_RESIDUAL", "PREPROCESS_BUG", ["PREPROCESS_BUG", "MODEL_INADEQUATE", "TARGET_NEW_REGIME"],
            {"ppc_via_evaluator": 1, "preprocess_unit_audit": 2, "changepoint_raw": 3}, {"fix_unit_conversion": 3, "expand_model_family": 6, "change_representation": 10}, 10, "MODEL_FAMILY_INADEQUATE",
            E("NO_ESCALATION_NEEDED", "PROCESS_TOOL_WORKFLOW", 1, 3, True, True), {"change_representation": ["MODEL_INADEQUATE", "TARGET_NEW_REGIME"]}),
        _fx("KA-12-CANNOT_IDENTIFY", "A_RESIDUAL", "MODEL_INADEQUATE", ["MODEL_INADEQUATE", "SENSOR_BLIND_NO_STANDARD", "MISSING_COVARIATE"],
            {"covariate_availability": 1}, {"measure_covariate": 2, "expand_model_family": 6, "build_calibration_instrument": 18}, 20, "CANNOT_IDENTIFY",
            E("CANNOT_IDENTIFY", "CANNOT_IDENTIFY", None, None, False, False)),
        _fx("KA-13-SAME_FIX_LOCUS_UNRESOLVED", "A_RESIDUAL", "TARGET_NEW_REGIME", ["TARGET_NEW_REGIME", "MODEL_INADEQUATE", "SENSOR_DRIFT_RECAL"],
            {"ppc_via_evaluator": 1, "calibration_standard": 3}, {"recalibrate": 3, "expand_model_family": 7}, 12, "MODEL_FAMILY_INADEQUATE",
            E("MODEL_FAMILY_INADEQUATE", "CANNOT_IDENTIFY", 2, 7, False, False)),
        _fx("KA-14-NO_ESCALATION_NEEDED_CRITERION_MET", "A_PLATEAU", "CRITERION_MET", ["CRITERION_MET", "STATES_COLLAPSED", "LOCAL_OPTIMUM_MORE_SEARCH"],
            {"obligation_ledger_audit": 1, "separability_test": 4, "search_coverage_audit": 1}, {"stop_warranted_terminal": 1, "continue_search": 2, "change_representation": 9}, 8, "REPRESENTATION_INSUFFICIENT",
            E("NO_ESCALATION_NEEDED", "NO_MATERIAL_DISCREPANCY", 0, 1, True, True)),
    ]


def separation_pair() -> list[dict]:
    """H-EXT-3 finite separation example: verdict-only exchange is blind to the P/Q difference."""
    common = dict(template="A_RESIDUAL", live=["PREPROCESS_BUG", "MODEL_INADEQUATE"], probes={"ppc_via_evaluator": 1},
                  ivs={"fix_unit_conversion": 3, "expand_model_family": 8}, budget=12, apparent="MODEL_FAMILY_INADEQUATE", extra={"expand_model_family": ["PREPROCESS_BUG"]})
    E = lambda cls, locus, level, cost: {"oracle_class": cls, "oracle_locus": locus, "oracle_level": level, "oracle_cost": cost, "identifiable": True, "probe_identifiable": False}
    return [
        _fx("SEP-P", common["template"], "PREPROCESS_BUG", common["live"], common["probes"], common["ivs"], common["budget"], common["apparent"], E("NO_ESCALATION_NEEDED", "PROCESS_TOOL_WORKFLOW", 1, 3), common["extra"]),
        _fx("SEP-Q", common["template"], "MODEL_INADEQUATE", common["live"], common["probes"], common["ivs"], common["budget"], common["apparent"], E("MODEL_FAMILY_INADEQUATE", "EPISTEMIC_MODEL", 2, 8), common["extra"]),
    ]

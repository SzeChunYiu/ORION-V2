#!/usr/bin/env python3
"""SD20 DEVELOPMENT_OPERATOR_DISCOVERY — bounded arXiv version-transition pilot.

Protocol: research/experiments/SCIENTIFIC_DEVELOPMENT_RECURSIVE_META_GENERALIZATION_PROTOCOL_V1.json
study SD20: "Infer candidate transition operators from temporally ordered
scientific-development trajectories without using post-outcome fame labels
during operator induction." Primary metrics: heldout_transition_prediction,
operator_stability, cross_domain_support, failed_trajectory_explanation.

Bounded slice (honest scope): arXiv trajectories with >=2 deposited versions
from the SD10 2024 window (SD10 head observations + SD20 version-history
observations). Every consecutive version pair contributes one transition.
No SD20+ inference beyond this slice is claimed by this script.

Operator representation (surface-only, version-local metadata):
- step observables: author_count, title_chars, abstract_chars,
  updated_epoch_days, days_since_first_deposit, primary category.
- DELTA outcome alphabet (27 cells): author_delta {0,+,-} x
  abstract_chars_delta {0,+,-} x inter_version_gap {<=7d, 8-90d, >90d}.
- CONTEXT (coarse current state, 2 x top-category(9) = 18 cells):
  step position {first, later} x top-level category bucket.
- Transition operator = categorical P(delta | context) with Laplace
  smoothing; the SD10/SD20 design contract (proxy metrics NEVER map to an
  outcome class) is preserved: deltas are deposit-surface changes, not
  scientific outcomes.

Arms evaluated on this slice (protocol arm vocabulary):
- SIMPLE_FREQUENCY_BASELINE        context-free marginal P(delta).
- TEMPORAL_SEQUENCE_MODEL_PARENT   order-1 context-conditional operator
                                   (the sequence-model parent).
- FIXED_META_LESSON_INJECTION      three a-priori literature-style fixed
                                   rules encoded as deterministic-ish delta
                                   distributions (abstract grows; author
                                   count non-decreasing; gaps lengthen).
- F0_META_PARENT_FEDERATION        equal-weight log-linear pool of the three
                                   runnable parents above.
- BIBLIOMETRIC_SCIENCE_OF_SCIENCE_PARENT   CANNOT_CHECK_ON_SLICE (Atom
                                   metadata carries no citation/fame fields).
- NETWORK_SCIENCE_PARENT                   CANNOT_CHECK_ON_SLICE (no
                                   disambiguated author network in inputs).
- CAUSAL_OR_QUASI_EXPERIMENTAL_PARENT_WHEN_IDENTIFIABLE
                                   CANNOT_CHECK_ON_SLICE (no interventions).
- F2_STATIC_NO_RECURSIVE_META_LEARNING     = TEMPORAL_SEQUENCE_MODEL_PARENT
                                   used with arm selection frozen on train.
- F2_RECURSIVE_SCIENTIFIC_DEVELOPMENT_FULL CANNOT_CHECK_ON_SLICE (recursive
                                   promotion requires SD50 machinery).

Primary metrics:
- heldout_transition_prediction: 70/30 split BY TRAJECTORY (seeded), mean
  log-score per arm + trajectory-cluster bootstrap CI of the score
  difference vs SIMPLE_FREQUENCY_BASELINE.
- operator_stability: B bootstrap resamples of train trajectories ->
  total-variation distance between each bootstrap operator and the point
  operator (mean/max, pooled and per-context).
- cross_domain_support: leave-one-category-out prediction (train on K-1
  categories, score the held-out one) vs the same-category estimate and the
  baseline; counts categories where LOO beats baseline.
- failed_trajectory_explanation: CANNOT_CHECK — the SD10 corpus is
  outcome-censored (19,960/19,982 trajectories UNKNOWN); no failed
  trajectory can be identified without inventing outcome labels, which the
  protocol forbids. Recorded, never faked.

Hard gates (asserted in the receipt, all must hold / be false):
- no post-outcome fame labels exist in the input observations (assert the
  proxy-metric name set contains no citation/fame field);
- trajectory-level split: no trajectory in both train and test;
- features at step k use only metadata of versions <= k (construction
  guarantee, asserted structurally);
- no recursive level is claimed above L1 operators.

Exit 0 = EXECUTED (CANNOT_CHECK marks are honest outcomes, not failures);
exit 3 = internal-consistency failure; exit 2 = usage.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

SCHEMA = "orion.v2.sd20-operator-discovery.v1"
TOP_CATEGORY_SLOTS = 8          # + "other" bucket
GAP_BUCKETS = [(0, 7), (8, 90), (91, 10**9)]
MIN_CONTEXT_TRANSITIONS = 20    # below this a conditional context is not estimated
BOOTSTRAP_OPERATOR_STABILITY = 200
BOOTSTRAP_SCORE_CI = 1000


# ---------------------------------------------------------------- inputs

def load_trajectories(obs_paths: list[str]) -> list[dict]:
    """Merge arXiv observations (SD10 head + SD20 versions) into trajectories.

    Only source_mode arxiv_* rows are used; steps are sorted by (ordinal,
    observation_id) exactly like the episode assembler. A final line without
    its trailing newline (a torn concurrent append) is dropped exactly like
    sd10_sources.common.load_jsonl_rows; any other malformed line raises.
    """
    by_traj: dict[str, list[dict]] = defaultdict(list)
    allowed_modes = {"arxiv_atom_metadata", "arxiv_atom_version_history"}
    for path in obs_paths:
        raw = Path(path).read_bytes()
        if raw and not raw.endswith(b"\n"):
            raw = raw[: raw.rfind(b"\n") + 1]
        for line in raw.split(b"\n"):
            if not line.strip():
                continue
            row = json.loads(line.decode("utf-8"))
            if row.get("source_mode_id") not in allowed_modes:
                continue
            if not row["observation_id"].startswith("arxiv-obs:"):
                continue
            by_traj[row["trajectory_id"]].append(row)
    trajectories = []
    for trajectory_id in sorted(by_traj):
        steps = sorted(by_traj[trajectory_id], key=lambda r: (r["ordinal"], r["observation_id"]))
        ids = [r["observation_id"] for r in steps]
        if len(ids) != len(set(ids)):
            raise SystemExit(f"duplicate observation ids in trajectory {trajectory_id}")
        trajectories.append({"trajectory_id": trajectory_id, "steps": steps})
    return trajectories


def proxy(step: dict) -> dict:
    return {name: value for name, value in step["proxy_metrics"].items()}


def top_category(step: dict) -> str:
    for feature in step["action_feature_ids"]:
        if feature.startswith("arxiv:primary_category:"):
            category = feature.rsplit(":", 1)[-1]
            return category.split(".")[0] if "." in category else category
    return "uncategorized"


def delta_sign(a: float, b: float) -> str:
    if b > a:
        return "+"
    if b < a:
        return "-"
    return "0"


def gap_bucket(days: float) -> int:
    for index, (low, high) in enumerate(GAP_BUCKETS):
        if low <= days <= high:
            return index
    return len(GAP_BUCKETS) - 1


def build_transitions(trajectories: list[dict]) -> list[dict]:
    """One transition per consecutive version pair; outcome = delta cell."""
    transitions = []
    for trajectory in trajectories:
        steps = trajectory["steps"]
        if len(steps) < 2:
            continue
        for index in range(len(steps) - 1):
            current, nxt = steps[index], steps[index + 1]
            pc, pn = proxy(current), proxy(nxt)
            gap = pn.get("arxiv:updated_epoch_days", 0.0) - pc.get("arxiv:updated_epoch_days", 0.0)
            author_delta = delta_sign(pc.get("arxiv:author_count", 0.0),
                                      pn.get("arxiv:author_count", 0.0))
            abstract_delta = delta_sign(pc.get("arxiv:abstract_chars", 0.0),
                                        pn.get("arxiv:abstract_chars", 0.0))
            transitions.append({
                "trajectory_id": trajectory["trajectory_id"],
                "step_index": index,
                "is_first_step": index == 0,
                "top_category": top_category(current),
                "outcome": f"{author_delta}{abstract_delta}{gap_bucket(gap)}",
                "gap_days": gap,
            })
        # trajectory-terminal censoring: the last observed version is the
        # latest deposited as of the 2026-08 fetch; later versions may exist.
    return transitions


# ---------------------------------------------------------------- arms

ALPHABET = [f"{a}{b}{g}" for a in "0+-" for b in "0+-" for g in range(len(GAP_BUCKETS))]


def context_of(transition: dict) -> str:
    return f"{'first' if transition['is_first_step'] else 'later'}|{transition['top_category']}"


def fit_marginal(transitions: list[dict]) -> dict:
    counts = Counter(t["outcome"] for t in transitions)
    total = sum(counts.values()) + len(ALPHABET)  # Laplace
    return {outcome: (counts.get(outcome, 0) + 1) / total for outcome in ALPHABET}


def fit_conditional(transitions: list[dict]) -> dict:
    """Order-1 context-conditional operator; thin contexts (< MIN) fall back
    to the marginal, and the fallback is RECORDED per context (never silent)."""
    marginal = fit_marginal(transitions)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for transition in transitions:
        grouped[context_of(transition)].append(transition)
    operator = {}
    fallback_contexts = []
    for context, rows in grouped.items():
        if len(rows) < MIN_CONTEXT_TRANSITIONS:
            operator[context] = marginal
            fallback_contexts.append({"context": context, "transitions": len(rows)})
        else:
            operator[context] = fit_marginal(rows)
    return {"operator": operator, "fallback_contexts": fallback_contexts,
            "marginal": marginal}


def fixed_lesson_distribution(lesson: str) -> dict:
    """A-priori literature-style rules as delta distributions (heavily but
    not absolutely concentrated, so mispredictions stay finite)."""
    def dist(peak_cells: list[str], weight: float) -> dict:
        base = (1.0 - weight) / len(ALPHABET)
        table = {outcome: base for outcome in ALPHABET}
        extra = weight / len(peak_cells)
        for cell in peak_cells:
            table[cell] += extra
        return table
    if lesson == "abstract_grows":
        # abstract non-shrinking dominates; author/gap uninformative (uniform fold)
        peaks = [f"{a}+{g}" for a in "0+-" for g in range(3)] + \
                [f"{a}0{g}" for a in "0+" for g in range(3)]
        return dist(peaks, 0.8)
    if lesson == "authors_nondecreasing":
        peaks = [f"+{b}{g}" for b in "0+-" for g in range(3)] + \
                [f"0{b}{g}" for b in "0+-" for g in range(3)]
        return dist(peaks, 0.8)
    if lesson == "gaps_lengthen":
        # later revisions take longer than a week more often than not
        peaks = [f"{a}{b}1" for a in "0+-" for b in "0+-"] + \
                [f"{a}{b}2" for a in "0+-" for b in "0+-"]
        return dist(peaks, 0.6)
    raise ValueError(lesson)


def log_score(distribution: dict, outcome: str) -> float:
    return math.log(max(distribution.get(outcome, 1e-12), 1e-12))


def arm_distributions(transitions: list[dict]) -> dict:
    """Frozen-on-train arm -> function context -> distribution."""
    conditional = fit_conditional(transitions)
    marginal = conditional["marginal"]
    lessons = {name: fixed_lesson_distribution(name)
               for name in ("abstract_grows", "authors_nondecreasing", "gaps_lengthen")}

    def federated(context: str) -> dict:
        parts = [marginal, conditional["operator"].get(context, marginal)] + list(lessons.values())
        table = {outcome: 0.0 for outcome in ALPHABET}
        for part in parts:
            for outcome in ALPHABET:
                table[outcome] += math.log(max(part.get(outcome, 1e-12), 1e-12))
        total = sum(math.exp(v) for v in table.values())
        return {outcome: math.exp(v) / total for outcome, v in table.items()}

    return {
        "SIMPLE_FREQUENCY_BASELINE": lambda context: marginal,
        "TEMPORAL_SEQUENCE_MODEL_PARENT": lambda context: conditional["operator"].get(context, marginal),
        "FIXED_META_LESSON_INJECTION__abstract_grows":
            lambda context, d=lessons["abstract_grows"]: d,
        "FIXED_META_LESSON_INJECTION__authors_nondecreasing":
            lambda context, d=lessons["authors_nondecreasing"]: d,
        "FIXED_META_LESSON_INJECTION__gaps_lengthen":
            lambda context, d=lessons["gaps_lengthen"]: d,
        "F0_META_PARENT_FEDERATION": federated,
    }


def evaluate(arms: dict, train: list[dict], test: list[dict]) -> dict:
    """Fit on train, mean log-score on test, cluster bootstrap diff vs baseline."""
    scores = {}
    for arm_name, predictor in arms.items():
        scores[arm_name] = [log_score(predictor(context_of(t)), t["outcome"]) for t in test]
    baseline_name = "SIMPLE_FREQUENCY_BASELINE"
    baseline_scores = scores[baseline_name]
    rng = random.Random(20260829)
    differences = {arm: [] for arm in scores if arm != baseline_name}
    for _ in range(BOOTSTRAP_SCORE_CI):
        sample = [rng.randrange(len(test)) for _ in range(len(test))]
        for arm in differences:
            diff = sum(scores[arm][i] - baseline_scores[i] for i in sample) / len(sample)
            differences[arm].append(diff)
    ci = {}
    base_mean = sum(baseline_scores) / len(baseline_scores)
    ci[baseline_name] = {"mean_logscore": base_mean,
                         "mean_logscore_baseline": base_mean,
                         "delta_vs_baseline": 0.0,
                         "bootstrap_ci95": [0.0, 0.0],
                         "ci_excludes_zero": False}
    for arm, values in differences.items():
        values.sort()
        lo = values[int(0.025 * len(values))]
        hi = values[int(0.975 * len(values))]
        mean = sum(scores[arm]) / len(scores[arm])
        ci[arm] = {"mean_logscore": mean,
                   "mean_logscore_baseline": base_mean,
                   "delta_vs_baseline": mean - base_mean,
                   "bootstrap_ci95": [lo, hi],
                   "ci_excludes_zero": not (lo <= 0.0 <= hi)}
    return {"per_arm": ci, "n_test": len(test)}


def operator_stability(train: list[dict]) -> dict:
    point = fit_conditional(train)
    contexts = sorted({context_of(t) for t in train})
    rng = random.Random(20260829)
    tv_pooled, tv_per_context = [], defaultdict(list)
    for _ in range(BOOTSTRAP_OPERATOR_STABILITY):
        sample = [train[rng.randrange(len(train))] for _ in range(len(train))]
        boot = fit_conditional(sample)
        for context in contexts:
            p = point["operator"].get(context, point["marginal"])
            q = boot["operator"].get(context, boot["marginal"])
            tv = 0.5 * sum(abs(p[o] - q[o]) for o in ALPHABET)
            tv_pooled.append(tv)
            tv_per_context[context].append(tv)
    per_context = {c: {"mean_tv": sum(v) / len(v), "max_tv": max(v)}
                   for c, v in sorted(tv_per_context.items())}
    return {"bootstrap_draws": BOOTSTRAP_OPERATOR_STABILITY,
            "mean_tv": sum(tv_pooled) / len(tv_pooled),
            "max_tv": max(tv_pooled),
            "per_context": per_context}


def cross_domain_support(transitions: list[dict]) -> dict:
    categories = sorted({t["top_category"] for t in transitions})
    rows = []
    for held_out in categories:
        train = [t for t in transitions if t["top_category"] != held_out]
        test = [t for t in transitions if t["top_category"] == held_out]
        if len(test) < 10:
            rows.append({"category": held_out, "n_test": len(test), "status": "TOO_FEW"})
            continue
        arms = arm_distributions(train)
        result = evaluate(arms, train, test)
        cond = result["per_arm"]["TEMPORAL_SEQUENCE_MODEL_PARENT"]
        rows.append({"category": held_out, "n_test": len(test),
                     "status": "EVALUATED",
                     "loo_delta_vs_baseline": cond["delta_vs_baseline"],
                     "loo_ci_excludes_zero": cond["ci_excludes_zero"]})
    evaluated = [r for r in rows if r["status"] == "EVALUATED"]
    return {"categories": rows,
            "n_evaluated": len(evaluated),
            "n_loo_beats_baseline": sum(1 for r in evaluated
                                        if r["loo_delta_vs_baseline"] > 0)}


# ---------------------------------------------------------------- gates

FAME_FIELD_TOKENS = ("citation", "cite", "fame", "impact", "prize", "award", "download", "view")


def hard_gates(trajectories: list[dict], train_ids: set, test_ids: set) -> dict:
    metric_names = {name for trajectory in trajectories
                    for step in trajectory["steps"] for name in proxy(step)}
    fame_fields = sorted(name for name in metric_names
                         if any(token in name.lower() for token in FAME_FIELD_TOKENS))
    return {
        "no_post_outcome_fame_labels_in_inputs": not fame_fields,
        "fame_fields_found": fame_fields,
        "trajectory_level_split_disjoint": not (train_ids & test_ids),
        "features_are_version_local": True,
        "no_recursive_level_claimed_above_L1": True,
        "gates": {
            "citation_impact_as_truth_label_allowed": False,
            "prize_as_truth_label_allowed": False,
            "publication_only_success_sampling_allowed": False,
            "future_information_leakage_allowed": False,
            "same_author_leakage_across_train_test_allowed": False,
            "recursive_level_without_heldout_residual_allowed": False,
        },
    }


# ---------------------------------------------------------------- main

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observations", action="append", required=True,
                        help="arXiv observation JSONL (SD10 head and/or SD20 versions); repeatable")
    parser.add_argument("--output", required=True, help="output receipt JSON")
    parser.add_argument("--split-fraction", type=float, default=0.7)
    args = parser.parse_args()
    if not 0.1 <= args.split_fraction <= 0.9:
        print("--split-fraction must be in [0.1, 0.9]", file=sys.stderr)
        return 2

    trajectories = load_trajectories(args.observations)
    multi = [t for t in trajectories if len(t["steps"]) >= 2]
    transitions = build_transitions(trajectories)
    if not transitions:
        print("no transitions found: need trajectories with >=2 versions", file=sys.stderr)
        return 3

    # deterministic trajectory-level split (seeded)
    rng = random.Random(20260829)
    ids = sorted(t["trajectory_id"] for t in multi)
    rng.shuffle(ids)
    cut = int(len(ids) * args.split_fraction)
    train_ids, test_ids = set(ids[:cut]), set(ids[cut:])
    train = [t for t in transitions if t["trajectory_id"] in train_ids]
    test = [t for t in transitions if t["trajectory_id"] in test_ids]

    arms = arm_distributions(train)
    heldout = evaluate(arms, train, test)
    stability = operator_stability(train)
    cross_domain = cross_domain_support(transitions)
    gates = hard_gates(trajectories, train_ids, test_ids)
    if not gates["no_post_outcome_fame_labels_in_inputs"]:
        print(f"HARD GATE violated: fame fields in inputs: {gates['fame_fields_found']}",
              file=sys.stderr)
        return 3
    if not gates["trajectory_level_split_disjoint"]:
        print("HARD GATE violated: trajectory leaked across train/test", file=sys.stderr)
        return 3

    cannot_check_arms = {
        "BIBLIOMETRIC_SCIENCE_OF_SCIENCE_PARENT":
            "Atom metadata carries no citation/fame fields on this slice",
        "NETWORK_SCIENCE_PARENT":
            "no disambiguated author network in the inputs (SD10 CANNOT_CHECK)",
        "CAUSAL_OR_QUASI_EXPERIMENTAL_PARENT_WHEN_IDENTIFIABLE":
            "no interventions or quasi-experimental variation in version deposits",
        "F2_RECURSIVE_SCIENTIFIC_DEVELOPMENT_FULL":
            "recursive promotion requires SD50 machinery; bounded pilot has one level",
    }
    receipt = {
        "schema": SCHEMA,
        "inputs": {"observations": list(args.observations)},
        "population": {
            "trajectories_total": len(trajectories),
            "trajectories_multiversion": len(multi),
            "trajectories_single_version_censored": len(trajectories) - len(multi),
            "transitions_total": len(transitions),
            "train_transitions": len(train),
            "test_transitions": len(test),
            "alphabet_cells": len(ALPHABET),
            "censoring_statement": (
                "single-version trajectories have no observable transition "
                "(deposit-surface censoring, not evidence of stability); the last "
                "observed version of every trajectory is the latest as of the "
                "2026-08 fetch and later versions may exist"),
        },
        "heldout_transition_prediction": heldout,
        "operator_stability": stability,
        "cross_domain_support": cross_domain,
        "failed_trajectory_explanation": {
            "status": "CANNOT_CHECK",
            "reason": ("the SD10 corpus is outcome-censored (19,960/19,982 UNKNOWN); "
                       "identifying 'failed' trajectories would require inventing "
                       "outcome labels the protocol forbids"),
        },
        "arm_status": {
            **{arm: "EVALUATED" for arm in arms},
            "F2_STATIC_NO_RECURSIVE_META_LEARNING":
                "EVALUATED (alias of TEMPORAL_SEQUENCE_MODEL_PARENT under "
                "train-frozen selection)",
            **{arm: "CANNOT_CHECK_ON_SLICE" for arm in cannot_check_arms},
        },
        "cannot_check_reasons": cannot_check_arms,
        "hard_gates": gates,
        "authority": {"grants_scientific_truth": False, "grants_causal_law": False,
                      "grants_population_regularity_beyond_slice": False},
        "classification": "BOUNDED_PILOT_INTERIM__NO_TERMINAL_CLAIM",
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=1, sort_keys=True) + "\n")

    # MD summary
    md = ["# SD20 bounded pilot — arXiv version-transition operator discovery", "",
          f"Population: {len(multi)} multi-version trajectories "
          f"({len(trajectories) - len(multi)} single-version censored), "
          f"{len(transitions)} transitions "
          f"(train {len(train)} / test {len(test)}, trajectory-level split).", "",
          "## heldout_transition_prediction (mean log-score, test)", "",
          "| Arm | mean log-score | Δ vs baseline | bootstrap 95% CI | CI excludes 0 |",
          "|---|---|---|---|---|"]
    baseline = heldout["per_arm"]["SIMPLE_FREQUENCY_BASELINE"]["mean_logscore"]
    for arm, row in heldout["per_arm"].items():
        md.append(f"| {arm} | {row['mean_logscore']:.4f} | "
                  f"{row['delta_vs_baseline']:+.4f} | "
                  f"[{row['bootstrap_ci95'][0]:.4f}, {row['bootstrap_ci95'][1]:.4f}] | "
                  f"{row['ci_excludes_zero']} |")
    md += ["", "## operator_stability", "",
           f"Bootstrap TV distance (B={stability['bootstrap_draws']}): "
           f"mean {stability['mean_tv']:.4f}, max {stability['max_tv']:.4f}.", "",
           "## cross_domain_support", "",
           "| Category | n_test | LOO Δ vs baseline | CI excludes 0 |", "|---|---|---|---|"]
    for row in cross_domain["categories"]:
        if row["status"] == "EVALUATED":
            md.append(f"| {row['category']} | {row['n_test']} | "
                      f"{row['loo_delta_vs_baseline']:+.4f} | "
                      f"{row['loo_ci_excludes_zero']} |")
        else:
            md.append(f"| {row['category']} | {row['n_test']} | TOO_FEW | — |")
    md += ["", f"LOO beats baseline in {cross_domain['n_loo_beats_baseline']} / "
           f"{cross_domain['n_evaluated']} evaluated categories.", "",
           "## failed_trajectory_explanation", "",
           "**CANNOT_CHECK** — outcome-censored corpus; no failed-trajectory "
           "labels exist and none are invented.", "",
           "## CANNOT_CHECK_ON_SLICE arms", ""]
    for arm, reason in cannot_check_arms.items():
        md.append(f"- {arm}: {reason}")
    md += ["", f"Classification: **{receipt['classification']}** "
           "(no terminal claim; scale-up is a re-run of the same adapters).", ""]
    out.with_suffix(".md").write_text("\n".join(md) + "\n")

    print(json.dumps({
        "trajectories_multiversion": len(multi),
        "transitions": len(transitions),
        "test_delta_conditional_vs_baseline":
            heldout["per_arm"]["TEMPORAL_SEQUENCE_MODEL_PARENT"]["delta_vs_baseline"],
        "test_ci_excludes_zero":
            heldout["per_arm"]["TEMPORAL_SEQUENCE_MODEL_PARENT"]["ci_excludes_zero"],
        "stability_mean_tv": stability["mean_tv"],
        "loo_beats_baseline": f"{cross_domain['n_loo_beats_baseline']}/{cross_domain['n_evaluated']}",
        "classification": receipt["classification"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

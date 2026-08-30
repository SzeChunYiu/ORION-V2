#!/usr/bin/env python3
"""EL10 exact known-answer case generators (epistemic locality).

Eight classes x six seeded cases. Every scenario states, in text, the regime
facts that logically force the private oracle; the oracle is exact by
construction. class_id never appears in the public task.
"""

import random

COORDS = [
    "environment_distribution",
    "task_family",
    "system_boundary",
    "scale",
    "timescale",
    "substrate_interface",
    "criterion",
]

CLASSES = ["ELC1", "ELC2", "ELC3", "ELC4", "ELC5", "ELC6", "ELC7", "ELC8"]

DOMAINS = [
    {
        "setting": "an online catalogue retrieval service ranks product matches",
        "task_family": "ranking over a fixed item corpus",
        "m1": "ExactLex-Match", "m2": "EmbedRank-NB",
        "env_a": "query demand concentrated on a few head terms",
        "env_b": "query demand diffuse across the long tail",
        "crit1": "exact-match precision at least 0.98",
        "crit2": "bounded 99th-percentile latency",
        "scale_small": "catalogue of 30k items or fewer",
        "scale_large": "catalogue above 30k items",
        "t_fast": "budget T = H/4", "t_slow": "budget T = 4H",
        "boundary_closed": "a single closed ranking node, no external channels",
        "boundary_open": "a fleet pooling behavioural signals across nodes",
    },
    {
        "setting": "a logistics operator routes parcels through a hub network",
        "task_family": "routing on a fixed network graph",
        "m1": "StaticCost-Dijkstra", "m2": "LiveLoad-RLite",
        "env_a": " shipment demand concentrated on one dense corridor",
        "env_b": " shipment demand diffuse across sparse regional links",
        "crit1": "route optimality gap below 1 percent",
        "crit2": "bounded compute per routing decision",
        "scale_small": "network of 200 hubs or fewer",
        "scale_large": "network above 200 hubs",
        "t_fast": "planning budget T = H/4", "t_slow": "planning budget T = 4H",
        "boundary_closed": "a single closed planner, no external channels",
        "boundary_open": "depots exchanging live load state",
    },
    {
        "setting": "a chemical plant controller schedules batch reactors",
        "task_family": "constrained scheduling of batch processes",
        "m1": "KineticFirst-Principles", "m2": "EmpiricalSurrogate-GP",
        "env_a": "feedstock variability concentrated near one nominal grade",
        "env_b": "feedstock variability diffuse across many grades",
        "crit1": "yield within 0.5 percent of the physical optimum",
        "crit2": "bounded wall-clock per schedule",
        "scale_small": "plant of 6 reactors or fewer",
        "scale_large": "plant above 6 reactors",
        "t_fast": "control horizon T = H/4", "t_slow": "control horizon T = 4H",
        "boundary_closed": "a single closed controller, no external channels",
        "boundary_open": "units sharing live sensor feeds",
    },
    {
        "setting": "a game studio evaluates search engines for a competitive board AI",
        "task_family": "game-tree search with imperfect information",
        "m1": "AlphaBeta-Deep", "m2": "SampledRollout-Shallow",
        "env_a": "opponent pool concentrated on one dominant style",
        "env_b": "opponent pool diffuse across many styles",
        "crit1": "worst-case tactical soundness",
        "crit2": "bounded nodes per move",
        "scale_small": "branching factor of 8 or fewer",
        "scale_large": "branching factor above 8",
        "t_fast": "thinking time T = H/4", "t_slow": "thinking time T = 4H",
        "boundary_closed": "a single closed engine, no external channels",
        "boundary_open": "engines sharing opening books",
    },
    {
        "setting": "an observatory calibrates a sensor array",
        "task_family": "static calibration of drifting sensors",
        "m1": "FullBatch-MLE", "m2": "OnlineDrift-Tracker",
        "env_a": "drift concentrated in one fast-warming channel",
        "env_b": "drift diffuse across all channels",
        "crit1": "calibration error below 0.1 sigma",
        "crit2": "bounded compute per recalibration",
        "scale_small": "array of 16 channels or fewer",
        "scale_large": "array above 16 channels",
        "t_fast": "recalibration window T = H/4", "t_slow": "recalibration window T = 4H",
        "boundary_closed": "a single closed estimator, no external channels",
        "boundary_open": "stations cross-validating drift estimates",
    },
    {
        "setting": "a retailer forecasts weekly demand for stocked items",
        "task_family": "seasonal demand forecasting",
        "m1": "SeasonalDecompose-AR", "m2": "GradientBoost-Local",
        "env_a": "demand variance concentrated in holiday spikes",
        "env_b": "demand variance diffuse through ordinary weeks",
        "crit1": "aggregate forecast error below 3 percent",
        "crit2": "bounded training compute per item",
        "scale_small": "assortment of 500 items or fewer",
        "scale_large": "assortment above 500 items",
        "t_fast": "fit window T = H/4", "t_slow": "fit window T = 4H",
        "boundary_closed": "a single closed forecaster, no external channels",
        "boundary_open": "stores pooling point-of-sale signals",
    },
    {
        "setting": "a network operator schedules traffic across a backbone",
        "task_family": "traffic engineering on a fixed topology",
        "m1": "ShortestPath-ECMP", "m2": "TrafficEngine-TE",
        "env_a": "flows concentrated on a few elephant paths",
        "env_b": "flows diffuse across many mice paths",
        "crit1": "path stretch below 2 percent",
        "crit2": "bounded state per switch",
        "scale_small": "topology of 50 nodes or fewer",
        "scale_large": "topology above 50 nodes",
        "t_fast": "reconfiguration window T = H/4", "t_slow": "reconfiguration window T = 4H",
        "boundary_closed": "a single closed controller, no external channels",
        "boundary_open": "domains advertising link utilisation",
    },
    {
        "setting": "a hospital triage desk scores incoming patients",
        "task_family": "ordinal risk scoring of arrivals",
        "m1": "RuleLadder-Triage", "m2": "LearnedScore-GBM",
        "env_a": "arrival acuity concentrated in one low-risk band",
        "env_b": "arrival acuity diffuse across all bands",
        "crit1": "critical-case recall at least 0.99",
        "crit2": "explainable bounded-feature cost per case",
        "scale_small": "desk of 40 arrivals per hour or fewer",
        "scale_large": "desk above 40 arrivals per hour",
        "t_fast": "scoring window T = H/4", "t_slow": "scoring window T = 4H",
        "boundary_closed": "a single closed scorer, no external channels",
        "boundary_open": "wards feeding back disposition outcomes",
    },
    {
        "setting": "a grid operator dispatches storage assets",
        "task_family": "online dispatch under stochastic net load",
        "m1": "Deterministic-LP", "m2": "Stochastic-MPC",
        "env_a": "net-load shocks concentrated at evening peak",
        "env_b": "net-load shocks diffuse across the day",
        "crit1": "delivery shortfall of zero events",
        "crit2": "bounded solve time per interval",
        "scale_small": "fleet of 12 assets or fewer",
        "scale_large": "fleet above 12 assets",
        "t_fast": "dispatch horizon T = H/4", "t_slow": "dispatch horizon T = 4H",
        "boundary_closed": "a single closed dispatcher, no external channels",
        "boundary_open": "assets bidding state-of-charge",
    },
    {
        "setting": "a fund rebalances a tracked index portfolio",
        "task_family": "constrained portfolio rebalancing",
        "m1": "FullCov-Optimizer", "m2": "DiagonalApprox-Trade",
        "env_a": "return correlation concentrated in one factor",
        "env_b": "return correlation diffuse across many factors",
        "crit1": "tracking error below 5 basis points",
        "crit2": "bounded turnover per rebalance",
        "scale_small": "book of 200 names or fewer",
        "scale_large": "book above 200 names",
        "t_fast": "rebalance window T = H/4", "t_slow": "rebalance window T = 4H",
        "boundary_closed": "a single closed desk, no external channels",
        "boundary_open": "desks crossing inventory signals",
    },
]

ENV_PAIRS = [
    ("concentrated", "diffuse"),
    ("skewed", "uniform"),
    ("bursty", "smooth"),
]


def _ctx(**over):
    base = {
        "environment_distribution": "nominal mixed reference distribution (registered)",
        "task_family": None,
        "system_boundary": "single closed decision unit, no external channels",
        "scale": "registered nominal scale",
        "timescale": "registered nominal horizon H",
        "substrate_interface": "registered benchmark interface, single substrate",
        "criterion": "registered primary criterion",
    }
    base.update({k: v for k, v in over.items() if v is not None})
    return base


def _ctx_block(ctx):
    return "REGISTERED CONTEXT (deployment frame; all seven coordinates):\n" + "\n".join(
        f"- {c}: {ctx[c]}" for c in COORDS
    )


def _registry(m1, m2, f1, f2):
    return (
        "METHOD REGISTRY (order of listing defines FIRST and SECOND):\n"
        f"- FIRST: {m1} -- {f1}\n"
        f"- SECOND: {m2} -- {f2}"
    )


def _scenario(setting, registry, ctx_block, counterfactual):
    return (
        f"SETTING: {setting[0].upper() + setting[1:]}. "
        "You are the method-selection officer; a deployment decision must be made from the "
        "registry below, strictly under the registered context that follows.\n\n"
        f"{registry}\n\n{ctx_block}\n\nCOUNTERFACTUAL TRANSPORT CLAIM: {counterfactual}"
    )


def _oracle(cls, decision, holds, coords, comp_valid, transport):
    return {
        "class_id": cls,
        "decision": decision,
        "holds_across_contexts": holds,
        "perspective_dependent_coordinates": coords,
        "comparison_valid": comp_valid,
        "transport_verdict": transport,
    }


def _registry_order(rng, dom, fact_first, fact_second):
    """Return (registry_lines_text, first_is_winner_label)."""
    if rng.random() < 0.5:
        return _registry(dom["m1"], dom["m2"], fact_first, fact_second), "FIRST"
    return _registry(dom["m2"], dom["m1"], fact_second, fact_first), "SECOND"


def _gen_elc1(rng, dom):
    fact_w = (
        "registered benchmark sweep across the FULL registered envelope (every environment, "
        "scale, timescale and boundary value in the registration) shows strict dominance OVER "
        "THE OTHER REGISTERED METHOD on the registered criterion in every cell"
    )
    fact_l = (
        "the same full-envelope sweep shows it STRICTLY DOMINATED BY the other registered "
        "method on the registered criterion in every cell"
    )
    reg, winner = _registry_order(rng, dom, fact_w, fact_l)
    ctx = _ctx(task_family=dom["task_family"], criterion="the registered primary criterion (single, commensurate)")
    cf = (
        "the dominance finding was established by the full-envelope sweep; a proposal applies "
        "it unchanged to a different point INSIDE the registered envelope."
    )
    scen = _scenario(dom["setting"], reg, _ctx_block(ctx), cf)
    return scen, _oracle("ELC1", winner, True, [], True, "VALID")


def _gen_elc2(rng, dom):
    lead_a, lead_b = ENV_PAIRS[rng.randrange(3)]
    fact_a = f"leads by a wide margin under {lead_a} regimes ({dom['env_a']}); loses under {lead_b} regimes"
    fact_b = f"leads by a wide margin under {lead_b} regimes ({dom['env_b']}); loses under {lead_a} regimes"
    if rng.random() < 0.5:
        reg = _registry(dom["m1"], dom["m2"], fact_a, fact_b)
        winner, env_val = "FIRST", dom["env_a"]
    else:
        reg = _registry(dom["m2"], dom["m1"], fact_b, fact_a)
        winner, env_val = "SECOND", dom["env_a"]
    ctx = _ctx(environment_distribution=f"registered deployment environment: {env_val}", task_family=dom["task_family"])
    cf = (
        f"a result report established the ranking under the {lead_b if winner == 'FIRST' else lead_a} regime; "
        "a proposal transports it unchanged to the registered deployment environment above."
    )
    scen = _scenario(dom["setting"], reg, _ctx_block(ctx), cf)
    return scen, _oracle("ELC2", winner, False, ["environment_distribution"], True, "INVALID")


def _gen_elc3(rng, dom):
    fact_small = (
        f"exhaustive and optimal whenever the problem is small ({dom['scale_small']}); "
        f"cost becomes prohibitive beyond that ({dom['scale_large']})"
    )
    fact_big = (
        f"loses its optimality guarantee on small instances ({dom['scale_small']}) but scales "
        f"and leads beyond the threshold ({dom['scale_large']})"
    )
    if rng.random() < 0.5:
        reg = _registry(dom["m1"], dom["m2"], fact_small, fact_big)
        winner, scale_val = "FIRST", f"registered deployment scale: {dom['scale_small']}"
    else:
        reg = _registry(dom["m2"], dom["m1"], fact_big, fact_small)
        winner, scale_val = "SECOND", f"registered deployment scale: {dom['scale_small']}"
    ctx = _ctx(scale=scale_val, task_family=dom["task_family"])
    cf = (
        "a result report established the ranking on the other side of the scale threshold; "
        "a proposal transports it unchanged to the registered deployment scale above."
    )
    scen = _scenario(dom["setting"], reg, _ctx_block(ctx), cf)
    return scen, _oracle("ELC3", winner, False, ["scale"], True, "INVALID")


def _gen_elc4(rng, dom):
    fact_fast = (
        f"converges within {dom['t_fast']} and then plateaus strictly BELOW the registered "
        "criterion bar; it never crosses the bar at any budget"
    )
    fact_slow = (
        f"needs {dom['t_slow']} to converge, then crosses the registered criterion bar by a "
        "wide margin; before that it is far below the bar"
    )
    if rng.random() < 0.5:
        reg = _registry(dom["m1"], dom["m2"], fact_fast, fact_slow)
        winner, t_val = "SECOND", f"registered horizon: {dom['t_slow']} (long budget)"
    else:
        reg = _registry(dom["m2"], dom["m1"], fact_slow, fact_fast)
        winner, t_val = "FIRST", f"registered horizon: {dom['t_slow']} (long budget)"
    ctx = _ctx(timescale=t_val, task_family=dom["task_family"])
    cf = (
        "a result report established the ranking under the short budget; a proposal transports "
        "it unchanged to the registered long horizon above."
    )
    scen = _scenario(dom["setting"], reg, _ctx_block(ctx), cf)
    return scen, _oracle("ELC4", winner, False, ["timescale"], True, "INVALID")


def _gen_elc5(rng, dom):
    fact_closed = (
        f"optimal for {dom['boundary_closed']}: fully exploits local state, degrades when "
        "external channels are present but unused"
    )
    fact_open = (
        f"leads when {dom['boundary_open']}: it depends on those external channels and cannot "
        "run in the closed configuration"
    )
    if rng.random() < 0.5:
        reg = _registry(dom["m1"], dom["m2"], fact_closed, fact_open)
        winner, b_val = "FIRST", f"registered boundary: {dom['boundary_closed']}"
    else:
        reg = _registry(dom["m2"], dom["m1"], fact_open, fact_closed)
        winner, b_val = "SECOND", f"registered boundary: {dom['boundary_closed']}"
    ctx = _ctx(system_boundary=b_val, task_family=dom["task_family"])
    cf = (
        "a result report established the ranking under the opposite boundary configuration; "
        "a proposal transports it unchanged to the registered boundary above."
    )
    scen = _scenario(dom["setting"], reg, _ctx_block(ctx), cf)
    return scen, _oracle("ELC5", winner, False, ["system_boundary"], True, "INVALID")


def _gen_elc6(rng, dom):
    fact_1 = (
        f"exactly meets {dom['crit1']} on every instance; worst-case cost on {dom['crit2']} is "
        "UNBOUNDED (no registered bound exists)"
    )
    fact_2 = (
        f"meets {dom['crit2']} with a strict bound on every instance; does not meet "
        f"{dom['crit1']} on any instance"
    )
    if rng.random() < 0.5:
        reg = _registry(dom["m1"], dom["m2"], fact_1, fact_2)
    else:
        reg = _registry(dom["m2"], dom["m1"], fact_2, fact_1)
    ctx = _ctx(
        task_family=dom["task_family"],
        criterion=(
            f"deployment must satisfy BOTH {dom['crit1']} AND {dom['crit2']}; "
            "NO commensurate exchange rate between the two criteria is registered"
        ),
    )
    cf = (
        "a single-scale registry claims a total order over the two methods under this "
        "two-criterion requirement; a proposal adopts that total order."
    )
    scen = _scenario(dom["setting"], reg, _ctx_block(ctx), cf)
    return scen, _oracle("ELC6", "PARETO_INCOMPARABLE", False, ["criterion"], True, "INVALID")


def _gen_elc7(rng, dom):
    fact_1 = (
        "substrate: replicator dynamics over a fixed population, NO beliefs, NO predictive "
        "interface; native evidence interface: population fitness gain over 500 generations"
    )
    fact_2 = (
        "substrate: a model WITH internal beliefs and a predictive interface; native evidence "
        "interface: held-out predictive likelihood on registered evaluation splits"
    )
    if rng.random() < 0.5:
        reg = _registry(dom["m1"], dom["m2"], fact_1, fact_2)
    else:
        reg = _registry(dom["m2"], dom["m1"], fact_2, fact_1)
    ctx = _ctx(
        task_family=dom["task_family"],
        substrate_interface=(
            "two DIFFERENT substrates with two DIFFERENT native evidence interfaces: "
            "generational fitness gain (no beliefs) versus held-out predictive likelihood "
            "(model with beliefs); no registered mapping between them"
        ),
        criterion="each method is evaluated only on its own native evidence interface",
    )
    cf = (
        "a review claims that the fitness-gain result on the no-beliefs substrate settles the "
        "predictive-likelihood standing of the model-with-beliefs substrate, and transports "
        "that verdict unchanged."
    )
    scen = _scenario(dom["setting"], reg, _ctx_block(ctx), cf)
    return scen, _oracle("ELC7", "COMPARISON_INVALID", False, ["criterion", "substrate_interface"], False, "INVALID")


def _gen_elc8(rng, dom):
    fact_a = (
        f"leads by a wide margin under {dom['env_a']} at small scale ({dom['scale_small']}); "
        "this is where the original result report was established"
    )
    fact_b = (
        f"leads by a wide margin under {dom['env_b']} at large scale ({dom['scale_large']}); "
        "the complementary sweep establishing this is registered alongside the report"
    )
    if rng.random() < 0.5:
        reg = _registry(dom["m1"], dom["m2"], fact_a, fact_b)
        winner = "SECOND"
    else:
        reg = _registry(dom["m2"], dom["m1"], fact_b, fact_a)
        winner = "FIRST"
    ctx = _ctx(
        environment_distribution=f"registered deployment environment: {dom['env_b']}",
        scale=f"registered deployment scale: {dom['scale_large']}",
        task_family=dom["task_family"],
    )
    cf = (
        "the result report established FIRST-order superiority under the concentrated/small "
        "configuration; a proposal transports that conclusion unchanged to the registered "
        "deployment context above."
    )
    scen = _scenario(dom["setting"], reg, _ctx_block(ctx), cf)
    return scen, _oracle("ELC8", winner, False, ["environment_distribution", "scale"], True, "INVALID")


_GENERATORS = {
    "ELC1": _gen_elc1, "ELC2": _gen_elc2, "ELC3": _gen_elc3, "ELC4": _gen_elc4,
    "ELC5": _gen_elc5, "ELC6": _gen_elc6, "ELC7": _gen_elc7, "ELC8": _gen_elc8,
}


def generate_case(rng, cls):
    """Return (public_task_dict, private_oracle_dict) for one seeded case."""
    dom = DOMAINS[rng.randrange(len(DOMAINS))]
    scen, oracle = _GENERATORS[cls](rng, dom)
    public = {
        "scenario_text": scen.replace("  ", " "),
        "coordinate_vocabulary": list(COORDS),
    }
    return public, oracle

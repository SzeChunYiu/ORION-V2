#!/usr/bin/env python3
"""SD10 bias audit: the five frozen primary metrics over fetched adapter JSONL.

Computes, from already-acquired normalized records only (no acquisition here):

  coverage                    per source mode: trajectories, observations,
                              distinct domains and epochs; corpus-level mode
                              count checked against --min-source-modes.
  missingness                 per mode: share of observations with empty
                              institution_ids / team_id / validation_ids /
                              proxy_metrics.
  identity_linkage_error      within-source duplicate observation_id and
                              trajectory collisions (must be zero by
                              construction); cross-mode linkage share measured
                              from shared id schemes in source_ids.
  survivorship_bias           bias_flag_ids inventory + share of trajectories
                              carrying any outcome binding (validated evidence
                              exists only for source-carried retraction
                              channels; everything else is UNKNOWN, not
                              success).
  outcome_proxy_disagreement  DOI-scheme overlap between the Crossref and
                              OpenAlex slices; CANNOT_CHECK_FROM_EMITTED_FIELDS
                              when a slice emits no doi: ids.

Every number in the receipt comes from the inputs; nothing is hand-entered.
Exit 0 = audit executed (CANNOT_CHECK marks are honest outcomes, not
failures). Exit 3 = internal consistency failure (duplicate ids, unreadable
inputs, mode count below the frozen minimum).
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

CENSORING_STATEMENT = (
    "unpublished failures are absent-by-censoring, not absent-by-fact; "
    "absence of a retraction marker never encodes success"
)


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_number}: {exc}") from exc
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--observation", action="append", required=True)
    parser.add_argument("--outcome-binding", action="append", default=[])
    parser.add_argument("--adapter-receipt", action="append", default=[])
    parser.add_argument("--output", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--min-source-modes", type=int, default=4)
    parser.add_argument("--run-window", default="", help="fetch window as recorded in adapter receipts")
    args = parser.parse_args()

    failures: list[str] = []
    observations: list[dict] = []
    for raw in args.observation:
        observations.extend(load_jsonl(Path(raw)))
    bindings: list[dict] = []
    for raw in args.outcome_binding:
        bindings.extend(load_jsonl(Path(raw)))
    adapter_receipts = {}
    for raw in args.adapter_receipt:
        doc = json.loads(Path(raw).read_text(encoding="utf-8"))
        adapter_receipts[doc.get("source_mode_id", raw)] = doc

    # ---- internal consistency (exit 3 on violation) ----------------------
    obs_ids = Counter(o["observation_id"] for o in observations)
    dup_obs = sorted(k for k, n in obs_ids.items() if n > 1)
    if dup_obs:
        failures.append(f"duplicate observation_id: {dup_obs[:5]} (n={len(dup_obs)})")
    modes = {o["source_mode_id"] for o in observations}
    if len(modes) < args.min_source_modes:
        failures.append(
            f"source modes {sorted(modes)} below frozen minimum {args.min_source_modes}")
    unknown_bindings = {b["outcome_class"] for b in bindings} - {
        "VALIDATED_FAILURE", "VALIDATED_SUCCESS"}
    if unknown_bindings:
        failures.append(f"adapters may only emit validated classes: {unknown_bindings}")

    # ---- coverage --------------------------------------------------------
    per_mode: dict[str, dict] = {}
    by_mode = defaultdict(list)
    for o in observations:
        by_mode[o["source_mode_id"]].append(o)
    for mode, rows in sorted(by_mode.items()):
        per_mode[mode] = {
            "trajectories": len({r["trajectory_id"] for r in rows}),
            "observations": len(rows),
            "domains": len({r["domain_id"] for r in rows}),
            "epochs": sorted({r["epoch_id"] for r in rows}),
            "kinds": dict(Counter(r["kind"] for r in rows)),
        }
    coverage = {
        "source_modes": sorted(modes),
        "source_mode_count": len(modes),
        "total_observations": len(observations),
        "total_trajectories": len({o["trajectory_id"] for o in observations}),
        "per_mode": per_mode,
        "adapter_receipts": {
            mode: {
                "requests": doc.get("requests"),
                "fetched_window": doc.get("window") or doc.get("fetched_window"),
                "max_records": doc.get("max_records"),
            } for mode, doc in adapter_receipts.items()},
        "run_window": args.run_window,
    }

    # ---- missingness -----------------------------------------------------
    missingness = {}
    for mode, rows in sorted(by_mode.items()):
        n = len(rows)
        missingness[mode] = {
            "empty_institution_ids": sum(1 for r in rows if not r["institution_ids"]) / n,
            "empty_team_id": sum(1 for r in rows if not r["team_id"]) / n,
            "empty_validation_ids": sum(1 for r in rows if not r["validation_ids"]) / n,
            "no_proxy_metrics": sum(1 for r in rows if not r["proxy_metrics"]) / n,
            "observations": n,
        }

    # ---- identity linkage ------------------------------------------------
    traj_by_mode = {
        mode: {r["trajectory_id"] for r in rows} for mode, rows in by_mode.items()}
    scheme_of = lambda t: t.split(":", 1)[0] if ":" in t else t
    mode_schemes = {mode: {scheme_of(t) for t in ts} for mode, ts in traj_by_mode.items()}
    all_schemes = set().union(*mode_schemes.values()) if mode_schemes else set()
    # a trajectory is cross-mode linkable iff one of its source_ids uses a
    # scheme that another mode's trajectory_ids also use
    linked = 0
    linkable_total = 0
    other_schemes_by_mode = {
        mode: all_schemes - schemes for mode, schemes in mode_schemes.items()}
    for o in observations:
        other = other_schemes_by_mode[o["source_mode_id"]]
        if any(scheme_of(s) in other for s in o["source_ids"]):
            linked += 1
        linkable_total += 1
    identity_linkage = {
        "duplicate_observation_ids": len(dup_obs),
        "trajectory_id_schemes_per_mode": {m: sorted(s) for m, s in mode_schemes.items()},
        "schemes_disjoint_across_modes": all(
            not (mode_schemes[a] & mode_schemes[b])
            for i, a in enumerate(sorted(modes)) for b in sorted(modes)[i + 1:]),
        "cross_mode_linked_observation_share": (linked / linkable_total) if linkable_total else 0.0,
        "note": "cross-mode linkage requires a shared id scheme in source_ids; "
                "with source-native ids only this share is 0 by construction — "
                "that is absent linkage evidence, NOT zero linkage error",
    }

    # ---- survivorship ----------------------------------------------------
    bound = {b["trajectory_id"] for b in bindings}
    all_traj = {o["trajectory_id"] for o in observations}
    flag_counts = Counter(
        f for o in observations for f in o["bias_flag_ids"])
    survivorship = {
        "bias_flag_counts": dict(flag_counts),
        "trajectories_with_any_binding": len(bound & all_traj),
        "binding_class_counts": dict(Counter(b["outcome_class"] for b in bindings)),
        "share_trajectories_with_binding": len(bound & all_traj) / len(all_traj) if all_traj else 0.0,
        "unbound_trajectories_unknown_not_success": len(all_traj - bound),
        "censoring_statement": CENSORING_STATEMENT,
    }

    # ---- outcome proxy disagreement --------------------------------------
    doi_modes = [m for m, s in mode_schemes.items() if "doi" in s]
    non_doi_modes = [m for m, s in mode_schemes.items() if "doi" not in s]
    if len(doi_modes) >= 2:
        sets = [traj_by_mode[m] for m in doi_modes]
        overlap = set.intersection(*map(set, sets))
        disagree = 0
        bound_by_mode = defaultdict(set)
        for b in bindings:
            for m in doi_modes:
                if b["trajectory_id"] in traj_by_mode[m]:
                    bound_by_mode[m].add(b["trajectory_id"])
        for t in overlap:
            marks = {("bound" if t in bound_by_mode[m] else "unbound") for m in doi_modes}
            if len(marks) > 1:
                disagree += 1
        outcome_proxy_disagreement = {
            "status": "EXECUTED",
            "doi_overlap_trajectories": len(overlap),
            "binding_disagreements": disagree,
            "modes_compared": doi_modes,
        }
    else:
        outcome_proxy_disagreement = {
            "status": "CANNOT_CHECK_FROM_EMITTED_FIELDS",
            "reason": "fewer than two modes emit doi: trajectory ids "
                      f"(doi modes: {doi_modes}; non-doi: {non_doi_modes}); "
                      "OpenAlex observations carry openalex:<W-id> only, so "
                      "Crossref/OpenAlex retraction-channel disagreement is "
                      "not computable from the normalized JSONL",
            "remediation": "emit a doi: alias in source_ids when the source "
                           "record carries a DOI, then re-run",
        }

    overall = "EXECUTED" if not failures else "FAIL"
    receipt = {
        "schema_version": "orion.v2.sd10-bias-audit.v1",
        "inputs": {
            "observations": args.observation,
            "outcome_bindings": args.outcome_binding,
            "adapter_receipts": args.adapter_receipt,
        },
        "coverage": coverage,
        "missingness": missingness,
        "identity_linkage_error": identity_linkage,
        "survivorship_bias": survivorship,
        "outcome_proxy_disagreement": outcome_proxy_disagreement,
        "failures": failures,
        "overall": overall,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# SD10 bias audit (V1)", "",
        f"Overall: **{overall}**. Window: `{args.run_window}`. "
        f"Source modes: {coverage['source_mode_count']} "
        f"({', '.join(coverage['source_modes'])}).", "",
        "| Mode | Trajectories | Observations | Domains | Epochs |",
        "|---|---|---|---|---|",
    ]
    for mode, m in per_mode.items():
        lines.append(
            f"| `{mode}` | {m['trajectories']} | {m['observations']} | "
            f"{m['domains']} | {', '.join(m['epochs'])} |")
    lines += [
        "",
        "- Missingness (share of observations): " + "; ".join(
            f"`{mode}`: inst={v['empty_institution_ids']:.3f}, "
            f"team={v['empty_team_id']:.3f}, val={v['empty_validation_ids']:.3f}, "
            f"proxy={v['no_proxy_metrics']:.3f}"
            for mode, v in missingness.items()),
        f"- Identity linkage: duplicate observation ids = "
        f"{identity_linkage['duplicate_observation_ids']}; schemes disjoint = "
        f"{identity_linkage['schemes_disjoint_across_modes']}; cross-mode linkable "
        f"share = {identity_linkage['cross_mode_linked_observation_share']:.4f} "
        "(absent evidence, not zero error).",
        f"- Survivorship: {survivorship['trajectories_with_any_binding']} of "
        f"{coverage['total_trajectories']} trajectories carry any outcome binding "
        f"({survivorship['binding_class_counts']}); "
        f"{survivorship['unbound_trajectories_unknown_not_success']} stay UNKNOWN.",
        f"- Outcome proxy disagreement: {outcome_proxy_disagreement['status']}"
        + (f" — overlap {outcome_proxy_disagreement['doi_overlap_trajectories']}, "
           f"disagreements {outcome_proxy_disagreement['binding_disagreements']}."
           if outcome_proxy_disagreement["status"] == "EXECUTED" else
           f" — {outcome_proxy_disagreement['reason']}"),
        f"- Censoring: {CENSORING_STATEMENT}.",
    ]
    if failures:
        lines += ["", "Failures:"] + [f"- {f}" for f in failures]
    Path(args.summary).write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"OVERALL {overall}: modes={coverage['source_mode_count']} "
          f"trajs={coverage['total_trajectories']} obs={coverage['total_observations']} "
          f"bindings={len(bindings)} "
          f"disagreement={outcome_proxy_disagreement['status']}")
    for f in failures:
        print(f"FAIL {f}")
    return 0 if not failures else 3


if __name__ == "__main__":
    raise SystemExit(main())

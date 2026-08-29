#!/usr/bin/env python3
"""Render non-authorizing paper tables from validated ORION result artifacts."""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path
from typing import Any, Iterable


class RenderError(RuntimeError):
    pass


def read_json(path: Path, *, required: bool = True) -> dict[str, Any]:
    if not path.exists() and not required:
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RenderError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RenderError(f"expected object in {path}")
    return value


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def display(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:.4g}"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (list, tuple)):
        return ", ".join(display(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(value, sort_keys=True)
    return str(value)


def markdown_table(headers: Iterable[str], rows: Iterable[Iterable[Any]]) -> str:
    header_tuple = tuple(headers)
    row_tuples = [tuple(row) for row in rows]
    lines = [
        "| " + " | ".join(header_tuple) + " |",
        "| " + " | ".join("---" for _ in header_tuple) + " |",
    ]
    for row in row_tuples:
        values = [display(item).replace("|", "\\|").replace("\n", "<br>") for item in row]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines) + "\n"


def csv_text(headers: Iterable[str], rows: Iterable[Iterable[Any]]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(tuple(headers))
    for row in rows:
        writer.writerow([display(item) for item in row])
    return output.getvalue()


def comparison_rows(analysis: dict[str, Any]) -> list[tuple[Any, ...]]:
    rows = []
    for item in analysis.get("primary_comparisons", []):
        success = item.get("success", {}).get("risk_difference", {})
        critical = item.get("critical_failure", {}).get("risk_difference", {})
        wall = item.get("wall_time_seconds", {})
        rows.append(
            (
                item.get("left_arm"),
                item.get("right_arm"),
                item.get("paired_task_count"),
                success.get("estimate"),
                success.get("ci95"),
                item.get("success", {}).get("exact_discordant_p"),
                critical.get("estimate"),
                wall.get("estimate"),
            )
        )
    return rows


def component_rows(analysis: dict[str, Any]) -> list[tuple[Any, ...]]:
    rows = []
    for arm_id, item in sorted(analysis.get("component_effects", {}).items()):
        success = item.get("success", {}).get("risk_difference", {})
        critical = item.get("critical_failure", {}).get("risk_difference", {})
        wall = item.get("wall_time_seconds", {})
        rows.append(
            (
                arm_id,
                item.get("paired_task_count"),
                success.get("estimate"),
                success.get("ci95"),
                critical.get("estimate"),
                wall.get("estimate"),
                item.get("component_disposition"),
            )
        )
    return rows


def arm_rows(analysis: dict[str, Any]) -> list[tuple[Any, ...]]:
    rows = []
    for arm_id, item in sorted(analysis.get("arm_summaries", {}).items()):
        rows.append(
            (
                arm_id,
                item.get("task_count"),
                item.get("success_count"),
                item.get("success_rate"),
                item.get("critical_failure_count"),
                item.get("critical_failure_rate"),
                item.get("mean_wall_time_seconds"),
                item.get("median_wall_time_seconds"),
                item.get("status_counts"),
            )
        )
    return rows


def anti_copy_rows(anti_copy: dict[str, Any]) -> list[tuple[Any, ...]]:
    rows = []
    for arm_id, item in sorted(anti_copy.get("arm_results", {}).items()):
        rows.append(
            (
                arm_id,
                item.get("historical_count"),
                item.get("historical_pass_rate"),
                item.get("fresh_counterfactual_count"),
                item.get("fresh_counterfactual_pass_rate"),
                item.get("fresh_critical_false_completion_count"),
            )
        )
    return rows


def claim_rows(claim_updates: dict[str, Any]) -> list[tuple[Any, ...]]:
    rows = []
    for item in claim_updates.get("claim_updates", []):
        rows.append(
            (
                item.get("claim_id"),
                item.get("paper_mapping"),
                item.get("proposed_status"),
                item.get("reason"),
                item.get("evidence_artifacts"),
                item.get("requires_independent_review"),
            )
        )
    return rows


def paper_readiness_rows(
    artifact_map: dict[str, Any], workdir: Path
) -> list[tuple[Any, ...]]:
    rows = []
    for paper in artifact_map.get("papers", []):
        required = paper.get("required_artifacts", [])
        present = []
        absent = []
        for item in required:
            # Only literal relative paths can be checked automatically. Descriptive
            # requirements remain absent until an independent receipt binds them.
            candidate = workdir / str(item)
            if "/" in str(item) and candidate.exists():
                present.append(str(item))
            else:
                absent.append(str(item))
        rows.append(
            (
                paper.get("paper_id"),
                paper.get("manuscript"),
                len(present),
                len(required),
                present,
                absent,
                paper.get("kill_terminal"),
                "NOT_SUBMISSION_READY",
            )
        )
    return rows


def render(workdir: Path, artifact_map_path: Path) -> dict[str, Any]:
    analysis = read_json(workdir / "aggregate" / "analysis.json")
    anti_copy = read_json(workdir / "aggregate" / "anti_copy_controls.json", required=False)
    claim_updates = read_json(workdir / "aggregate" / "paper_claim_updates.json", required=False)
    artifact_map = read_json(artifact_map_path)

    exports = workdir / "paper_exports"
    tables = {
        "arm_summary": (
            (
                "Arm",
                "Tasks",
                "Successes",
                "Success rate",
                "Critical failures",
                "Critical-failure rate",
                "Mean wall time (s)",
                "Median wall time (s)",
                "Status counts",
            ),
            arm_rows(analysis),
        ),
        "primary_comparisons": (
            (
                "Left arm",
                "Right arm",
                "Paired tasks",
                "Success risk difference",
                "Success 95% CI",
                "Exact discordant-pair p",
                "Critical-failure risk difference",
                "Wall-time difference (s)",
            ),
            comparison_rows(analysis),
        ),
        "component_effects": (
            (
                "Removed-component arm",
                "Paired tasks",
                "Success difference",
                "Success 95% CI",
                "Critical-failure difference",
                "Wall-time difference (s)",
                "Disposition",
            ),
            component_rows(analysis),
        ),
        "anti_copy_controls": (
            (
                "Arm",
                "Historical tasks",
                "Historical pass rate",
                "Fresh tasks",
                "Fresh pass rate",
                "Fresh critical false completions",
            ),
            anti_copy_rows(anti_copy),
        ),
        "claim_updates": (
            (
                "Claim",
                "Papers",
                "Proposed status",
                "Reason",
                "Evidence artifacts",
                "Independent review required",
            ),
            claim_rows(claim_updates),
        ),
        "paper_readiness": (
            (
                "Paper",
                "Manuscript",
                "Auto-detected artifacts",
                "Required artifacts",
                "Present",
                "Open/semantic requirements",
                "Kill terminal",
                "Automatic readiness",
            ),
            paper_readiness_rows(artifact_map, workdir),
        ),
    }

    written = []
    for name, (headers, rows) in tables.items():
        markdown_path = exports / f"{name}.md"
        csv_path = exports / f"{name}.csv"
        write_text(markdown_path, markdown_table(headers, rows))
        write_text(csv_path, csv_text(headers, rows))
        written.extend((str(markdown_path), str(csv_path)))

    summary = {
        "schema_version": "orion.v2.paper-results-export.v1",
        "written_files": written,
        "source_analysis": str(workdir / "aggregate" / "analysis.json"),
        "source_claim_updates": (
            str(workdir / "aggregate" / "paper_claim_updates.json")
            if claim_updates
            else None
        ),
        "source_anti_copy": (
            str(workdir / "aggregate" / "anti_copy_controls.json")
            if anti_copy
            else None
        ),
        "automatic_manuscript_editing": False,
        "scientific_truth_authorized": False,
        "field_status_authorized": False,
        "publication_readiness_authorized": False,
    }
    write_text(exports / "export_manifest.json", json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, default=Path(".orion-real-problem-suite"))
    parser.add_argument(
        "--artifact-map",
        type=Path,
        default=Path("papers/verification/PAPER_RESULTS_ARTIFACT_MAP_V1.json"),
    )
    args = parser.parse_args(argv)
    try:
        result = render(args.workdir, args.artifact_map)
    except (RenderError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

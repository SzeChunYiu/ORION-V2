from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_script(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


materializer = load_script(
    "orion_native_template_materializer",
    "scripts/materialize_native_result_templates.py",
)
runner = load_script(
    "orion_native_command_runner",
    "scripts/run_pinned_native_benchmark_task.py",
)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def frozen(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    venv = tmp_path / "venv"
    data = tmp_path / "data"
    for path in (repo, venv, data):
        path.mkdir()
    write_json(
        tmp_path / "frozen_tasks.json",
        {
            "benchmarks": [
                {
                    "benchmark_id": "native-demo",
                    "repository_path": str(repo),
                    "venv_path": str(venv),
                    "commit": "1" * 40,
                }
            ],
            "tasks": [
                {
                    "task_id": "native-demo-01",
                    "benchmark_id": "native-demo",
                    "adapter": "native_command",
                    "variant": "variant-a",
                    "native_commands": [
                        "python -c \"from pathlib import Path; Path('{output_dir}/metric.txt').write_text('ok')\""
                    ],
                }
            ],
        },
    )


def test_native_template_materialization_is_non_authorizing(tmp_path: Path) -> None:
    frozen(tmp_path)
    template = tmp_path / "template.json"
    write_json(
        template,
        {
            "status": "CANNOT_CHECK_NATIVE_RUN_NOT_EXECUTED",
            "scientific_truth_authorized": False,
            "field_status_authorized": False,
            "publication_readiness_authorized": False,
        },
    )
    count = materializer.materialize(
        tmp_path,
        template,
        arms={"F0_PARENT_FEDERATION", "F2_ORION_METABOLIC_FULL"},
        tasks=None,
    )
    assert count == 2
    value = json.loads(
        (
            tmp_path
            / "native_result_inputs"
            / "F2_ORION_METABOLIC_FULL"
            / "native-demo-01.json"
        ).read_text()
    )
    assert value["task_id"] == "native-demo-01"
    assert value["status"] == "CANNOT_CHECK_NATIVE_RUN_NOT_EXECUTED"
    assert value["scientific_truth_authorized"] is False


def test_native_command_runner_records_execution_without_interpreting_metrics(
    tmp_path: Path,
) -> None:
    frozen(tmp_path)
    output = tmp_path / "output"
    receipt = runner.run_task(
        tmp_path,
        task_id="native-demo-01",
        arm_id="F2_ORION_METABOLIC_FULL",
        data_dir=tmp_path / "data",
        output_dir=output,
        run_name="run-a",
        timeout_seconds=30,
        skip_install_commands=True,
    )
    assert receipt["overall_returncode"] == 0
    assert (output / "metric.txt").read_text() == "ok"
    assert receipt["native_metrics_interpreted"] is False
    assert receipt["scientific_truth_authorized"] is False
    assert receipt["publication_readiness_authorized"] is False

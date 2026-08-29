import importlib.util
from pathlib import Path


def _load(name: str):
    path = Path(__file__).parents[2] / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_generated_meta_policy_suite_is_fresh_and_oracle_separated():
    mod = _load("generate_scientific_development_meta_benchmark")
    public, private = mod.build_suite(seed=12345, tasks=12, train_episodes=8)
    assert public["task_count"] == 12
    assert private["task_count"] == 12
    assert "correct_action" not in str(public)
    assert "latent_weights" not in str(public)
    assert all(task["candidate_actions"] for task in public["tasks"])
    assert {t["task_id"] for t in public["tasks"]} == {t["task_id"] for t in private["tasks"]}


def test_hidden_policy_varies_across_tasks():
    mod = _load("generate_scientific_development_meta_benchmark")
    _, private = mod.build_suite(seed=999, tasks=10, train_episodes=8)
    matrices = {str(task["latent_weights"]) for task in private["tasks"]}
    assert len(matrices) > 1

"""Independent finite witnesses for the bounded method-learning contract."""
import importlib.util
from pathlib import Path


def test_identification_and_fairness_calibration():
    path = Path(__file__).resolve().parents[2] / "research/machine-epistemics-theory/method_learning_v1/check.py"
    spec = importlib.util.spec_from_file_location("method_learning_check", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.check()
    assert result["identification_cases"] == 512
    assert result["fairness_cases"] == 1024
    assert result["external_science"] == "NOT_RUN"

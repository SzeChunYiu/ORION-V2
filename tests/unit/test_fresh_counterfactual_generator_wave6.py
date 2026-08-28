from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "generate_fresh_bugsinpy_counterfactuals.py"
SPEC = importlib.util.spec_from_file_location("orion_counterfactual_generator", SCRIPT)
assert SPEC and SPEC.loader
generator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generator)


def test_token_mutation_is_syntax_valid_and_reversible(tmp_path: Path) -> None:
    path = tmp_path / "module.py"
    path.write_text(
        "def choose(value):\n    return value == 1 and True\n",
        encoding="utf-8",
    )
    candidates = generator.mutation_candidates(path)
    assert candidates
    token_index, old, new = candidates[0]
    original, mutated = generator.apply_mutation(path, token_index, new)
    assert original != mutated
    compile(mutated, str(path), "exec")
    patch = generator.reverse_patch(Path("module.py"), original, mutated)
    assert old in original
    assert new in mutated
    assert "--- a/module.py" in patch
    assert "+++ b/module.py" in patch


def test_source_file_discovery_excludes_tests(tmp_path: Path) -> None:
    (tmp_path / "pkg").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "pkg" / "code.py").write_text("x = True\n", encoding="utf-8")
    (tmp_path / "tests" / "test_code.py").write_text("x = False\n", encoding="utf-8")
    assert generator.source_files(tmp_path) == [tmp_path / "pkg" / "code.py"]

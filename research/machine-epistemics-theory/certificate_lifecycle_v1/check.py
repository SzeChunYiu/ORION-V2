"""Replay local tests and applied mutants. Exit 0=checks pass, 1=defect, 2=cannot check."""
from __future__ import annotations
from hashlib import sha256
import io
import json
from pathlib import Path
import platform
import sys
import types
import unittest

HERE = Path(__file__).resolve().parent
MUTANTS = (
    ("M01_omit_prompt", 'return digest("operator", fields)',
     'return digest("operator", {k: v for k, v in fields.items() if k != "prompt"})', 1,
     "test_identity_all_16_coordinates"),
    ("M02_missing_as_valid", 'return FACTS[facts[key]] if key in facts else UNRESOLVED',
     'return FACTS[facts[key]] if key in facts else APPLICABLE', 1,
     "test_missing_judgment_and_scoped_checker_trust"),
    ("M03_destroy_alternate_support", 'max(alternatives, default=UNRESOLVED)',
     'min(alternatives, default=UNRESOLVED)', 1, "test_alternate_support"),
    ("M04_ignore_necessary_support", 'alternatives = [min((values.get',
     'alternatives = [max((values.get', 1, "test_all_necessary_dependencies"),
    ("M05_self_warrant_cycle", 'values = {c.name: UNRESOLVED for c in registry}',
     'values = {c.name: APPLICABLE for c in registry}', 1, "test_cycles_need_grounding"),
    ("M06_ignore_context", 'binding = APPLICABLE if all(context.get(k) == v for k, v in c.bindings) else UNRESOLVED',
     'binding = APPLICABLE', 1, "test_scope_epoch_and_operator_drift"),
    ("M07_ignore_snapshot_fence", 'if event["generation"] != state.generation or event["snapshot"] != state.identity:',
     'if False:', 1, "test_stale_and_aba_intents"),
    ("M08_coerce_guarantee_to_exact", 'payload["kind"] == cert.kind and payload["statement"] == cert.statement',
     'payload["statement"] == cert.statement', 1, "test_no_guarantee_to_exact_coercion"),
    ("M09_allow_registry_rebinding", 'require(state.registry == registry_id(registry), "REGISTRY_DRIFT")',
     'pass  # deliberately ignore registry drift', 2, "test_registry_name_rebinding"),
    ("M10_omit_event_from_history", 'journal = digest("step", [state.identity, event])',
     'journal = digest("step", [state.identity])', 1, "test_replay_checkpoint_and_receipt_identity"),
    ("M11_self_authorize_absorption", 'return min(FACTS.get(facts.get(k), UNRESOLVED) for k in keys)',
     'return APPLICABLE', 1, "test_absorption_requires_external_evidence"),
    ("M12_ignore_checkpoint", 'require(state.identity == checkpoint, "CHECKPOINT_MISMATCH")',
     'pass  # deliberately ignore external checkpoint', 1, "test_replay_checkpoint_and_receipt_identity"),
)


def run() -> dict:
    import reference
    import test_reference
    def suite():
        return unittest.defaultTestLoader.loadTestsFromModule(test_reference)
    test_reference.COUNTS.clear()
    output = io.StringIO()
    baseline = unittest.TextTestRunner(stream=output, verbosity=0).run(suite())
    if not baseline.wasSuccessful():
        raise AssertionError("BASELINE_FAILURE\n" + output.getvalue())
    observed = dict(test_reference.COUNTS)
    expected = {"identity_coordinates": 16, "factorization_models": 256,
                "DNF_oracle_comparisons": 6885, "cyclic_grounding_node_comparisons": 1152}
    if baseline.testsRun != 20 or observed != expected:
        raise AssertionError("EMPTY_OR_CHANGED_DENOMINATOR")
    source = (HERE / "reference.py").read_text(encoding="utf-8")
    rows = []
    for name, old, new, expected_count, expected_test in MUTANTS:
        count = source.count(old)
        if count != expected_count:
            raise AssertionError(f"MUTATION_NOT_APPLIED:{name}:{count}")
        mutated = source.replace(old, new)
        module = types.ModuleType("mutant_" + name)
        sys.modules[module.__name__] = module
        try:
            exec(compile(mutated, module.__name__, "exec"), module.__dict__)
            test_reference.m = module
            test_reference.COUNTS.clear()
            output = io.StringIO()
            result = unittest.TextTestRunner(stream=output, verbosity=0).run(suite())
            failures = sorted(t.id() for t, _ in result.failures)
            # Expected assertion failure must occur; unrelated crashes are not sufficient.
            detected = any(expected_test in test_id for test_id in failures)
            rows.append({"mutant": name, "replacements": count, "tests_run": result.testsRun,
                         "expected_test": expected_test, "detected": detected,
                         "assertion_failures": len(result.failures), "errors": len(result.errors),
                         "mutated_source_sha256": sha256(mutated.encode()).hexdigest()})
            if not detected:
                raise AssertionError("MUTANT_SURVIVED_OR_WRONG_FAILURE:" + name + "\n" + output.getvalue())
        finally:
            test_reference.m = reference
            sys.modules.pop(module.__name__, None)
    return {"schema": "me-certificate-lifecycle-calibration/v1",
            "design_commit": "69181cbbf356563aad662985f384373d4c081ff9",
            "terminal": "LOCAL_EXACT_CALIBRATION_PASS",
            "baseline": {"tests": baseline.testsRun, "failures": 0, "errors": 0},
            "denominators": observed | {"applied_mutants": len(rows)},
            "mutants": rows,
            "artifacts": {p.name: sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.iterdir())
                          if p.is_file() and p.name != "RECEIPT.json"},
            "workflow_sha256": sha256((HERE.parents[2] / ".github/workflows/me-certificate-lifecycle.yml").read_bytes()).hexdigest(),
            "environment": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                            "system": platform.system(), "machine": platform.machine()},
            "proof_status": "WRITTEN_ARGUMENTS_NOT_PROOF_ASSISTANT_CHECKED",
            "independent_review": "PENDING", "ocm_adoption": "NOT_AUTHORIZED_BY_THIS_RECEIPT",
            "full_repository_tests": "NOT_RUN; direct git clone unavailable in this container"}


if __name__ == "__main__":
    try:
        report = run()
        archive = HERE / "RECEIPT.json"
        if archive.exists():
            recorded = json.loads(archive.read_text(encoding="utf-8"))
            for key in ("design_commit", "terminal", "baseline", "denominators", "mutants",
                        "artifacts", "workflow_sha256"):
                if report[key] != recorded.get(key):
                    raise AssertionError("ARCHIVED_RECEIPT_MISMATCH:" + key)
    except (ImportError, OSError) as error:
        print(json.dumps({"terminal": "CANNOT_CHECK", "reason": str(error)}))
        sys.exit(2)
    except (AssertionError, ValueError) as error:
        print(json.dumps({"terminal": "DEFECT", "reason": str(error)}))
        sys.exit(1)
    print(json.dumps(report, indent=2, sort_keys=True))

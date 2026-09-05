"""Public authored fit and hostile controls; no protected cases are imported."""
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import adapter

FIXTURES = Path(__file__).resolve().parent / "public_fixtures"


def fixture(name="plural_history"):
    return json.loads((FIXTURES / (name + ".json")).read_text())


class RequestContractTests(unittest.TestCase):
    def test_public_fixtures_are_valid_and_nonempty(self):
        paths = sorted(FIXTURES.glob("*.json"))
        self.assertEqual(len(paths), 7)
        for path in paths:
            with self.subTest(path=path.name):
                self.assertEqual(adapter.check_case(json.loads(path.read_text()))["visibility"],
                                 "PUBLIC_AUTHORED")

    def test_unknown_constraint_completeness_is_not_conformance(self):
        case = fixture()
        case["constraints_complete"] = False
        result = adapter.run_case(adapter.encoded(case))
        self.assertEqual(result["status"], "CANNOT_CHECK")
        self.assertEqual(result["reason"], "unknown_constraint_coverage")

    def test_empty_candidates_not_obstruction(self):
        case = fixture()
        case["candidates"] = []
        self.assertEqual(adapter.run_case(adapter.encoded(case))["status"], "CANNOT_CHECK")

    def test_incomplete_candidates_not_obstruction(self):
        case = fixture()
        case["candidate_coverage"] = "UNKNOWN"
        self.assertEqual(adapter.run_case(adapter.encoded(case))["status"], "CANNOT_CHECK")

    def test_unknown_fields_not_ignored(self):
        case = fixture()
        case["scientific_truth"] = True
        self.assertEqual(adapter.run_case(adapter.encoded(case))["status"], "CANNOT_CHECK")

    def test_duplicate_candidate_or_context_cannot_merge_histories(self):
        for field in ("candidate_id", "context_id"):
            case = fixture()
            case["candidates"][1][field] = case["candidates"][0][field]
            self.assertEqual(adapter.run_case(adapter.encoded(case))["status"], "CANNOT_CHECK")

    def test_unbound_endpoint_and_parallel_edge_not_erased(self):
        for edge in (["urn:a", "urn:unbound"], ["urn:a", "urn:b"]):
            case = fixture()
            case["candidates"][0]["edges"].append(edge)
            self.assertEqual(adapter.run_case(adapter.encoded(case))["status"], "CANNOT_CHECK")

    def test_missing_shapes_and_targets_not_vacuous_pass(self):
        for field in ("shapes", "shape_targets"):
            case = fixture()
            case[field] = []
            self.assertEqual(adapter.run_case(adapter.encoded(case))["status"], "CANNOT_CHECK")

    def test_target_only_shape_not_vacuous_pass(self):
        case = fixture()
        case["shapes"] = [t for t in case["shapes"] if t[1]["iri"] == adapter.SH + "targetNode"]
        self.assertEqual(adapter.run_case(adapter.encoded(case))["status"], "CANNOT_CHECK")

    def test_unsupported_shape_semantics_not_silently_dropped(self):
        case = fixture()
        case["shapes"][0][1] = {"iri": adapter.SH + "sparql"}
        self.assertEqual(adapter.run_case(adapter.encoded(case))["status"], "CANNOT_CHECK")

    def test_input_and_check_budgets(self):
        self.assertEqual(adapter.run_case(b"x" * 1_000_001)["status"], "RESOURCE_EXHAUSTED")
        case = fixture()
        case["candidates"] *= 3
        self.assertEqual(adapter.run_case(adapter.encoded(case))["reason"],
                         "native_check_budget_exceeded")

    def test_dependency_version_mismatch_is_rejected(self):
        class WrongDistribution:
            version = "0.0.0"
        with patch.object(adapter.importlib.metadata, "distribution", return_value=WrongDistribution()):
            with self.assertRaisesRegex(ValueError, "dependency_version_mismatch"):
                adapter.dependency_identity()

    def test_duplicate_json_keys_cannot_discard_input_declarations(self):
        raw = adapter.encoded(fixture())
        replaced = raw.replace(b'"constraints_complete":true',
                               b'"constraints_complete":false,"constraints_complete":true')
        self.assertNotEqual(raw, replaced)
        result = adapter.run_case(replaced)
        self.assertEqual(result["status"], "CANNOT_CHECK")
        self.assertEqual(result["reason"], "duplicate_json_key:constraints_complete")
        with self.assertRaisesRegex(ValueError, "nonstandard_json_constant"):
            adapter.decode(b'{"x":NaN}')

    def test_orphan_constraints_and_missing_property_paths_are_rejected(self):
        case = fixture()
        case["shapes"].append([{"iri": "urn:orphan"}, {"iri": adapter.SH + "minCount"},
                               {"literal": "1", "datatype": "http://www.w3.org/2001/XMLSchema#integer"}])
        self.assertEqual(adapter.run_case(adapter.encoded(case))["reason"], "unlinked_property_constraint")
        case = fixture()
        case["shapes"] = [t for t in case["shapes"] if t[1]["iri"] != adapter.SH + "path"]
        self.assertEqual(adapter.run_case(adapter.encoded(case))["reason"],
                         "missing_or_ambiguous_property_path")


class NativeParentTests(unittest.TestCase):
    """Missing native packages fail these tests. There is no skip or mock fallback."""

    @classmethod
    def setUpClass(cls):
        cls.outputs = {}
        for path in sorted(FIXTURES.glob("*.json")):
            cls.outputs[path.stem] = adapter.run_case(path.read_bytes())

    def observed(self, name):
        result = self.outputs[name]
        self.assertEqual(result["status"], "OBSERVED", result)
        self.assertEqual(result["checked_candidates"], result["supplied_candidates"])
        self.assertGreater(result["checked_candidates"], 0)
        self.assertEqual(result["scientific_terminal"], "CANNOT_CHECK")
        self.assertFalse(result["parent_binding"])
        self.assertFalse(result["authority_granted"])
        return result

    def test_actual_native_versions_source_identity_and_resources(self):
        for name in self.outputs:
            out = self.observed(name)
            for package, expected in adapter.PINS.items():
                identity = out["dependencies"][package]
                self.assertEqual(identity["version"], expected)
                self.assertTrue(identity["installed_files"])
                self.assertEqual(len(identity["installed_source_sha256"]), 64)
            self.assertEqual(set(out["native_imports"]), {"networkx", "rdflib", "pyshacl"})
            self.assertEqual(out["execution"]["returncode"], 0)
            self.assertLessEqual(out["execution"]["elapsed_seconds"], 30)
            self.assertLessEqual(out["execution"]["observed_output_bytes"], 1_000_000)
            self.assertLessEqual(out["native_check_calls"], 8)
            self.assertEqual(out["execution"]["retries"], 0)

    def test_plural_candidates_same_projection_distinct_native_contexts(self):
        out = self.observed("plural_history")
        self.assertEqual(out["accepted_candidate_ids"], ["portrait-A", "portrait-B"])
        left, right = out["results"]
        self.assertEqual(left["rdflib_context_triples"], right["rdflib_context_triples"])
        self.assertNotEqual(left["context_id"], right["context_id"])
        self.assertNotEqual(left["history"], right["history"])
        self.assertNotEqual(left["candidate_input_sha256"], right["candidate_input_sha256"])

    def test_all_two_edge_patches_pass_full_union_has_native_cycle_witness(self):
        full = self.observed("global_cycle")["results"][0]
        case = fixture("global_cycle")
        self.assertFalse(full["networkx_is_dag"])
        self.assertTrue(full["pyshacl_conforms"])
        self.assertFalse(full["registered_constraints_conform"])
        witness = full["networkx_cycle_witness"]
        self.assertEqual(len(witness), 3)
        self.assertEqual({tuple(x) for x in witness},
                         {tuple(x) for x in case["candidates"][0]["edges"]})
        self.assertTrue(all(witness[i][1] == witness[(i + 1) % len(witness)][0]
                            for i in range(len(witness))))
        for i in range(3):
            patch_result = self.observed(f"local_patch_{i}")["results"][0]
            self.assertTrue(patch_result["registered_constraints_conform"])
            self.assertEqual(len(patch_result["native_edges"]), 2)
            self.assertEqual(patch_result["networkx_cycle_witness"], [])
            self.assertNotEqual(patch_result["candidate_input_sha256"],
                                full["candidate_input_sha256"])

    def test_missing_required_value_is_native_shacl_nonconformance(self):
        result = self.observed("missing_required_value")["results"][0]
        self.assertTrue(result["networkx_is_dag"])
        self.assertFalse(result["pyshacl_conforms"])
        self.assertFalse(result["registered_constraints_conform"])
        self.assertIn("MinCountConstraintComponent", result["pyshacl_report_nt"])

    def test_supplied_representation_expansion_preserves_old_candidates(self):
        old = self.observed("plural_history")
        new = self.observed("representation_expansion")
        original = fixture()
        successor = fixture("representation_expansion")
        self.assertEqual(original["query_id"], successor["query_id"])
        self.assertEqual(original["shapes"], successor["shapes"])
        self.assertEqual(original["candidates"], successor["candidates"][:2])
        self.assertNotEqual(old["representation_id"], new["representation_id"])
        self.assertEqual(new["accepted_candidate_ids"], ["portrait-A", "portrait-B", "portrait-C"])
        for before, after in zip(old["results"], new["results"][:2]):
            for field in ("context_id", "history", "candidate_input_sha256", "native_nodes",
                          "native_edges", "rdflib_context_triples", "registered_constraints_conform"):
                self.assertEqual(before[field], after[field])

    def test_native_malformed_shape_remains_error_not_scientific_negative(self):
        case = fixture()
        for triple in case["shapes"]:
            if triple[1]["iri"] == adapter.SH + "minCount":
                triple[2] = {"literal": "-1", "datatype": "http://www.w3.org/2001/XMLSchema#integer"}
        result = adapter.run_case(adapter.encoded(case))
        self.assertIn(result["status"], {"EXECUTION_FAILED", "CANNOT_CHECK"})
        self.assertNotEqual(result.get("native_error_type"), "PackageNotFoundError")
        self.assertEqual(result["scientific_terminal"], "CANNOT_CHECK")


if __name__ == "__main__":
    unittest.main()

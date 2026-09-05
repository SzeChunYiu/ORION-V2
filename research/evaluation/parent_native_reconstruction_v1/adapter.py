"""Native, non-authorizing Campaign-D reconstruction over explicit public inputs.

The adapter enumerates supplied candidates; it neither generates nor interprets
scientific portraits. Only run_case supplies the bounded subprocess interface.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import selectors
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
SCHEMA = "PUBLIC_PARENT_NATIVE_RECONSTRUCTION_V1"
SH = "http://www.w3.org/ns/shacl#"
RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
PINS = {
    "networkx": "3.6.1", "rdflib": "7.6.0", "pyshacl": "0.40.1",
    "owlrl": "7.6.2", "prettytable": "3.18.0", "packaging": "26.2",
    "html5rdf": "1.2.1", "pyparsing": "3.3.2", "wcwidth": "0.8.2",
}
PROFILE = {
    "input_bytes": 1_000_000, "output_bytes": 1_000_000,
    "worker_seconds": 5.0, "wall_seconds": 30.0, "native_check_ceiling": 8,
    "network_call_ceiling": 0, "provider_call_ceiling": 0, "retries": 0,
}


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(value).hexdigest()


def decode(raw):
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate_json_key:" + key)
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError("nonstandard_json_constant:" + value)

    return json.loads(raw, object_pairs_hook=unique_pairs, parse_constant=invalid_constant)


def packet(status, reason, **fields):
    return {"schema": SCHEMA, "status": status, "reason": reason,
            "scientific_terminal": "CANNOT_CHECK", "parent_binding": False,
            "authority_granted": False, **fields}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exact_keys(value, keys, label):
    require(type(value) is dict and set(value) == set(keys),
            f"unsupported_or_missing_{label}_fields")


def nonempty(value):
    return type(value) is str and bool(value) and len(value) < 1000


def term_spec(value):
    require(type(value) is dict, "invalid_rdf_term")
    if set(value) == {"iri"}:
        require(nonempty(value["iri"]) and ":" in value["iri"], "invalid_iri")
    elif set(value) == {"literal", "datatype"}:
        require(type(value["literal"]) is str and nonempty(value["datatype"]),
                "invalid_literal")
    else:
        raise ValueError("unsupported_rdf_term")


def check_case(case):
    exact_keys(case, {"schema", "case_id", "visibility", "source_id", "query_id",
                     "representation_id", "candidate_coverage", "constraints_complete",
                     "shapes", "shape_targets", "candidates"}, "case")
    require(case["schema"] == SCHEMA and case["visibility"] == "PUBLIC_AUTHORED",
            "unsupported_case_scope")
    for name in ("case_id", "source_id", "query_id", "representation_id"):
        require(nonempty(case[name]), f"missing_{name}")
    require(case["candidate_coverage"] == "EXPLICIT_SUPPLIED_SET_ONLY",
            "unknown_candidate_coverage")
    require(case["constraints_complete"] is True, "unknown_constraint_coverage")
    require(type(case["candidates"]) is list and bool(case["candidates"]),
            "empty_candidate_set_is_not_obstruction")
    require(2 * len(case["candidates"]) <= PROFILE["native_check_ceiling"],
            "native_check_budget_exceeded")
    require(type(case["shapes"]) is list and 0 < len(case["shapes"]) <= 256,
            "missing_or_excess_shapes")
    allowed = {RDF + "type"} | {SH + n for n in (
        "targetNode", "property", "path", "minCount", "maxCount", "datatype",
        "class", "hasValue", "nodeKind")}
    targets, constrained, shape_nodes = set(), set(), set()
    for triple in case["shapes"]:
        require(type(triple) is list and len(triple) == 3, "invalid_shape_triple")
        for term in triple:
            term_spec(term)
        require(set(triple[0]) == {"iri"} and set(triple[1]) == {"iri"},
                "shape_subject_and_predicate_must_be_iris")
        predicate = triple[1]["iri"]
        require(predicate in allowed, "unsupported_shape_predicate")
        if predicate == SH + "targetNode":
            require(set(triple[2]) == {"iri"}, "target_must_be_iri")
            targets.add(triple[2]["iri"])
            shape_nodes.add(triple[0]["iri"])
        if predicate in {SH + n for n in ("minCount", "maxCount", "datatype",
                                          "class", "hasValue", "nodeKind")}:
            constrained.add(triple[0]["iri"])
    require(type(case["shape_targets"]) is list and bool(case["shape_targets"])
            and all(nonempty(x) for x in case["shape_targets"]),
            "missing_shape_targets")
    require(len(set(case["shape_targets"])) == len(case["shape_targets"])
            and targets == set(case["shape_targets"]), "shape_target_mismatch")
    # No vacuous target-only shapes or unlinked property constraints.
    all_properties = set()
    for node in shape_nodes:
        properties = {t[2]["iri"] for t in case["shapes"]
                      if t[0] == {"iri": node} and t[1] == {"iri": SH + "property"}
                      and set(t[2]) == {"iri"}}
        require(properties and properties <= constrained, "unconstrained_target_shape")
        all_properties.update(properties)
    require(all_properties == constrained, "unlinked_property_constraint")
    for node in all_properties:
        paths = [t[2] for t in case["shapes"]
                 if t[0] == {"iri": node} and t[1] == {"iri": SH + "path"}]
        require(len(paths) == 1 and set(paths[0]) == {"iri"}, "missing_or_ambiguous_property_path")
    require(all(t[0]["iri"] in shape_nodes | all_properties for t in case["shapes"]),
            "unlinked_shape_definition")
    seen_ids, seen_contexts = set(), set()
    for candidate in case["candidates"]:
        exact_keys(candidate, {"candidate_id", "context_id", "history", "nodes",
                               "edges", "triples", "require_dag"}, "candidate")
        for name in ("candidate_id", "context_id"):
            require(nonempty(candidate[name]), f"missing_{name}")
        require(":" in candidate["context_id"], "context_must_be_iri")
        require(candidate["candidate_id"] not in seen_ids, "duplicate_candidate_id")
        require(candidate["context_id"] not in seen_contexts, "duplicate_context_id")
        seen_ids.add(candidate["candidate_id"])
        seen_contexts.add(candidate["context_id"])
        require(type(candidate["history"]) is list and candidate["history"]
                and all(nonempty(x) for x in candidate["history"]), "missing_history")
        nodes = candidate["nodes"]
        require(type(nodes) is list and nodes and all(nonempty(n) for n in nodes),
                "missing_nodes")
        require(len(set(nodes)) == len(nodes), "duplicate_nodes")
        require(type(candidate["edges"]) is list, "invalid_edges")
        seen_edges = set()
        for edge in candidate["edges"]:
            require(type(edge) is list and len(edge) == 2 and all(n in nodes for n in edge),
                    "edge_endpoint_not_supplied")
            require(tuple(edge) not in seen_edges, "parallel_edges_unsupported")
            seen_edges.add(tuple(edge))
        require(candidate["require_dag"] is True, "unsupported_graph_constraint")
        require(type(candidate["triples"]) is list and bool(candidate["triples"]),
                "missing_data_graph")
        for triple in candidate["triples"]:
            require(type(triple) is list and len(triple) == 3, "invalid_data_triple")
            for term in triple:
                term_spec(term)
            require(set(triple[0]) == {"iri"} and set(triple[1]) == {"iri"},
                    "data_subject_and_predicate_must_be_iris")
    return case


def dependency_identity():
    identities = {}
    for name, expected in PINS.items():
        distribution = importlib.metadata.distribution(name)
        require(distribution.version == expected, f"dependency_version_mismatch:{name}")
        # Hash installed package bytes, not a self-asserted version alone.
        members = []
        for item in distribution.files or ():
            if str(item).endswith((".pyc", ".pyo")):
                continue
            path = Path(distribution.locate_file(item))
            require(path.is_file(), f"missing_installed_dependency_file:{name}:{item}")
            members.append({"path": str(item), "sha256": digest(path.read_bytes())})
        require(bool(members), f"empty_dependency_inventory:{name}")
        identities[name] = {"version": distribution.version,
                            "installed_files": sorted(members, key=lambda x: x["path"])}
        identities[name]["installed_source_sha256"] = digest(encoded(identities[name]))
    return identities


def _native(case):
    dependencies = dependency_identity()
    import networkx as nx
    import rdflib
    import pyshacl
    from pyshacl.errors import ValidationFailure
    from rdflib.namespace import RDF as RDF_NS, SH as SH_NS

    def term(value):
        if "iri" in value:
            return rdflib.URIRef(value["iri"])
        # Preserve the lexical form; do not normalize scientific distinctions.
        return rdflib.Literal(value["literal"], datatype=rdflib.URIRef(value["datatype"]),
                              normalize=False)

    def triples(graph):
        # No blank nodes occur in authored data/shapes, so this is an exact
        # ordered serialization. Native validation reports are preserved raw.
        return sorted([[s.n3(), p.n3(), o.n3()] for s, p, o in graph])

    shapes = rdflib.Graph(identifier=rdflib.URIRef("urn:public-parent:shapes"))
    for triple in case["shapes"]:
        shapes.add(tuple(term(t) for t in triple))
    dataset = rdflib.Dataset(default_union=False)
    results, accepted = [], []
    for candidate in case["candidates"]:
        native_graph = nx.DiGraph()
        native_graph.add_nodes_from(candidate["nodes"])
        native_graph.add_edges_from(candidate["edges"])
        try:
            witness = [list(edge) for edge in nx.find_cycle(native_graph)]
            dag = False
        except nx.NetworkXNoCycle:
            witness, dag = [], True
        data = dataset.graph(rdflib.URIRef(candidate["context_id"]))
        for triple in candidate["triples"]:
            data.add(tuple(term(t) for t in triple))
        before = triples(data)
        conforms, report, report_text = pyshacl.validate(
            data, shacl_graph=shapes, inference="none", abort_on_first=False,
            allow_infos=False, allow_warnings=False, meta_shacl=True,
            advanced=False, js=False, do_owl_imports=False, iterate_rules=False,
            inplace=False, debug=False,
        )
        if isinstance(report, ValidationFailure):
            return packet("CANNOT_CHECK", "native_validation_failure",
                          native_message=str(report), partial_results=results)
        if type(conforms) is not bool or not isinstance(report, rdflib.Graph):
            return packet("CANNOT_CHECK", "missing_or_ambiguous_native_report",
                          partial_results=results)
        report_nodes = list(report.subjects(RDF_NS.type, SH_NS.ValidationReport))
        require(len(report_nodes) == 1, "ambiguous_validation_report_identity")
        values = list(report.objects(report_nodes[0], SH_NS.conforms))
        require(len(values) == 1 and values[0].toPython() is conforms,
                "native_conformance_disagreement")
        require(before == triples(data), "parent_mutated_input_graph")
        valid = dag and conforms
        if valid:
            accepted.append(candidate["candidate_id"])
        results.append({
            "candidate_id": candidate["candidate_id"],
            "context_id": str(data.identifier), "history": candidate["history"],
            "candidate_input_sha256": digest(encoded(candidate)),
            "native_nodes": list(native_graph.nodes),
            "native_edges": [list(edge) for edge in native_graph.edges],
            "networkx_is_dag": dag, "networkx_cycle_witness": witness,
            "rdflib_context_triples": before,
            "rdflib_context_triples_sha256": digest(encoded(before)),
            "pyshacl_conforms": conforms,
            "pyshacl_report_nt": report.serialize(format="nt"),
            "pyshacl_report_text": report_text,
            "registered_constraints_conform": valid,
        })
    return packet("OBSERVED", "parent_native_checks_completed",
                  case_id=case["case_id"], source_id=case["source_id"],
                  query_id=case["query_id"], representation_id=case["representation_id"],
                  supplied_candidates=len(results), checked_candidates=len(results),
                  candidate_coverage=case["candidate_coverage"],
                  accepted_candidate_ids=accepted, results=results,
                  native_check_calls=2 * len(results),
                  native_imports={"networkx": nx.__file__, "rdflib": rdflib.__file__,
                                  "pyshacl": pyshacl.__file__},
                  dependencies=dependencies)


def _deny_side_effects(event, args):
    if event.startswith("socket.") or event in {
        "subprocess.Popen", "os.system", "os.exec", "os.spawn", "os.fork",
        "os.remove", "os.rename", "os.mkdir", "os.rmdir", "os.link", "os.symlink",
    }:
        raise PermissionError(f"worker_side_effect_denied:{event}")
    if event == "open":
        _, mode, flags = args
        if (mode and any(x in mode for x in "wax+")) or (
                flags and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC)):
            raise PermissionError("worker_file_write_denied")


def worker():
    sys.dont_write_bytecode = True
    raw = sys.stdin.buffer.read(PROFILE["input_bytes"] + 1)
    if len(raw) > PROFILE["input_bytes"]:
        result = packet("RESOURCE_EXHAUSTED", "input_byte_ceiling")
    else:
        try:
            case = check_case(decode(raw))
            sys.addaudithook(_deny_side_effects)
            result = _native(case)
        except (ValueError, importlib.metadata.PackageNotFoundError) as exc:
            result = packet("CANNOT_CHECK", str(exc), native_error_type=type(exc).__name__)
        except Exception as exc:
            result = packet("EXECUTION_FAILED", str(exc), native_error_type=type(exc).__name__)
    result["input_sha256"] = digest(raw)
    sys.stdout.buffer.write(encoded(result))


def run_case(raw: bytes):
    """Run one authored JSON request under fixed ceilings; never retry.

    Native failures, resource exhaustion, and unknown premises are separate
    from observed conformance. No protected-case or baseline-binding entrypoint.
    """
    require(type(raw) is bytes, "input_must_be_exact_bytes")
    started = time.monotonic()
    if len(raw) > PROFILE["input_bytes"]:
        return packet("RESOURCE_EXHAUSTED", "input_byte_ceiling", input_sha256=digest(raw))
    try:
        check_case(decode(raw))
    except (ValueError, TypeError, KeyError) as exc:
        return packet("CANNOT_CHECK", str(exc), input_sha256=digest(raw))
    # Temporary files avoid a blocking write into a child pipe. They are the
    # wrapper's authorized ephemeral artifacts; native code cannot write files.
    import tempfile
    with tempfile.TemporaryFile() as source:
        source.write(raw)
        source.seek(0)
        proc = subprocess.Popen([sys.executable, "-I", str(ROOT / "adapter.py"), "--worker"],
                                stdin=source, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                cwd=ROOT, env={"PATH": os.defpath, "PYTHONHASHSEED": "20260827"})
        selector = selectors.DefaultSelector()
        streams = {"stdout": bytearray(), "stderr": bytearray()}
        for name in streams:
            pipe = getattr(proc, name)
            os.set_blocking(pipe.fileno(), False)
            selector.register(pipe, selectors.EVENT_READ, name)
        failure = None
        try:
            while selector.get_map():
                remaining = PROFILE["worker_seconds"] - (time.monotonic() - started)
                if remaining <= 0:
                    failure = "worker_timeout"
                    break
                for key, _ in selector.select(min(remaining, 0.1)):
                    available = PROFILE["output_bytes"] + 1 - sum(map(len, streams.values()))
                    try:
                        chunk = os.read(key.fileobj.fileno(), min(65536, available))
                    except BlockingIOError:
                        continue
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    streams[key.data].extend(chunk)
                    if sum(map(len, streams.values())) > PROFILE["output_bytes"]:
                        failure = "worker_output_ceiling"
                        break
                if failure:
                    break
        finally:
            if failure:
                proc.kill()
            try:
                proc.wait(timeout=max(0.01, PROFILE["worker_seconds"] -
                                      (time.monotonic() - started)))
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
                failure = "worker_timeout"
            selector.close()
            proc.stdout.close()
            proc.stderr.close()
    evidence = {
        "input_sha256": digest(raw), "stdout_sha256": digest(streams["stdout"]),
        "stderr_sha256": digest(streams["stderr"]),
        "observed_output_bytes": sum(map(len, streams.values())),
        "elapsed_seconds": time.monotonic() - started, "returncode": proc.returncode,
        "stderr": streams["stderr"].decode("utf-8", errors="replace"),
        "profile": PROFILE, "retries": 0,
    }
    if failure:
        result = packet("RESOURCE_EXHAUSTED", failure)
    elif proc.returncode != 0:
        result = packet("EXECUTION_FAILED", "worker_nonzero_exit")
    else:
        try:
            result = json.loads(streams["stdout"])
            require(type(result) is dict and result.get("input_sha256") == digest(raw),
                    "worker_input_identity_mismatch")
        except (ValueError, TypeError) as exc:
            result = packet("EXECUTION_FAILED", f"invalid_worker_packet:{exc}")
    result["execution"] = evidence
    result["adapter_sha256"] = digest((ROOT / "adapter.py").read_bytes())
    result["requirements_sha256"] = digest((ROOT / "requirements.txt").read_bytes())
    return result


if __name__ == "__main__":
    if sys.argv[1:] == ["--worker"]:
        worker()
    elif len(sys.argv) == 2:
        data = Path(sys.argv[1]).read_bytes()
        print(json.dumps(run_case(data), indent=2, sort_keys=True))
    else:
        raise SystemExit("usage: python adapter.py PUBLIC_CASE.json")

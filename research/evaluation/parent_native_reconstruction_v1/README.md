# Public native reconstruction for the Campaign-D parent

This is a runnable parent-only reconstruction of the NetworkX/RDFLib/pySHACL
composition proposed in the Wave-06 audits. It handles explicit graph candidates,
typed RDF graphs, and authored constraints. Its fixtures are newly authored public
engineering examples. It does not read the frozen parity case registry, evaluator
labels, protected gold, or either parity subject's outputs.

The existing baseline registry remains `implementation_bindings.bound: false`.
Passing this package's tests does not complete issue #8 or identify the strongest
parent comparator. The other eight campaign adapters are outside this package.

## Interface and native semantics

Install the exact versions in `requirements.txt` into an isolated Python 3.12
environment, then run:

```bash
python adapter.py public_fixtures/plural_history.json
python run_public_suite.py --output /tmp/new-parent-native-fit
```

The Python interface is `run_case(raw_json_bytes) -> neutral_result_packet`.
The output directory must be new; historical packets are never overwritten.
`run_public_suite.py` executes all 20 tests and fails if any are missing, failed,
errored, or skipped. Missing packages are a failure to obtain native fit evidence;
there is no substitute implementation, package mock, or skipped-native-test pass.

Every request supplies its source, query, representation, shape targets, all
candidates in the *explicit supplied set*, each candidate's graph context and
history, graph nodes/edges, RDF triples, and SHACL triples. Those declarations are
not independently authenticated evidence or a claim of exhaustive scientific
candidate generation. The adapter does not recover candidates from prose or
discover their scientific meaning. The authored candidate input is an available
opportunity, not measured parent-generated knowledge.

The native calls are:

| Native operation | Preserved output | Limit |
| --- | --- | --- |
| `networkx.DiGraph` and `find_cycle` | Exact nodes/edges and returned directed-cycle witness, or native `NetworkXNoCycle` | Certifies only the supplied directed graph and its declared DAG constraint |
| `rdflib.Dataset(default_union=False).graph(context_iri)` and `Graph.add` | All named context identifiers, lexical RDF triples, candidate hashes and supplied histories | Graph names identify contexts; they do not authenticate source independence |
| `pyshacl.validate` on in-memory `Graph` objects | Native conformance boolean, complete raw report graph and report text | Conformance is relative to the authored constraints, never scientific truth or completeness |

All valid supplied candidates remain in the result. No scalar "best portrait" is
selected, and equal triples in distinct native contexts do not erase histories.
Blank nodes are excluded from authored data; literal lexical forms are preserved
with RDFLib normalization disabled. Native report blank-node IDs can vary across
runs; the receipt preserves and hashes the exact returned report bytes.

The supported SHACL surface is explicit `targetNode` plus linked property shapes
using `path`, `minCount`, `maxCount`, `datatype`, `class`, `hasValue`, or `nodeKind`.
The adapter checks nonempty constraints and target identity before execution.
Meta-SHACL is enabled. Inference, imports, rules, SPARQL constraints, advanced
features and JavaScript are disabled or refused. This restricted reconstruction
does not establish that those additional native capabilities are unnecessary for
the strongest Campaign-D parent. They must be evaluated before binding a baseline.

`OBSERVED` means the native checks completed for every supplied candidate. An
empty accepted list then describes that supplied set only, with the actual native
witnesses/reports; it is not proof of global scientific impossibility. An empty
input candidate set, unknown coverage, missing constraints, unsupported semantics,
missing dependency or version mismatch yields `CANNOT_CHECK`. Native execution
errors and resource exhaustion remain separate statuses. Every packet retains
`scientific_terminal: CANNOT_CHECK`, `parent_binding: false` and no authority.

## Public fit coverage

Seven case files are authored before native CI execution and source-bound in
`SOURCE_BINDING.json`:

- Two admissible candidates with equal RDF triples and different native named
  contexts/histories; both must survive.
- Three separate two-edge directed patches, each a no-alarm DAG control.
- Their complete three-edge union, with a native directed-cycle witness. Tests
  verify the actual edge deletion in each patch and every witness edge in the
  full graph. This is a finite graph obstruction, not general scientific gluing.
- A missing required RDF value: DAG checking still passes, while native SHACL
  emits a `MinCountConstraintComponent` violation.
- An explicitly supplied additional representation/candidate, with the exact
  prior query, shapes and two prior candidate objects unchanged. Old results,
  distinctions and histories survive. The additional candidate is not claimed as
  autonomous learning or discovery, and no old coverage receipt is rewritten.

Fourteen request-contract tests additionally exercise missing/unknown premises,
duplicate identities, unsupported edges/shapes, input and call ceilings, and a
version mismatch, duplicate JSON keys, and orphan/missing property constraints.
Six native test methods check the seven actual native outputs,
malformed-shape failure, provenance preservation, and package/resource identities.

The actual first local attempt is preserved under `history/`: 18 tests executed,
12 contract tests passed, and six native test methods failed because NetworkX was
not installed. All seven native packets were `CANNOT_CHECK`; none was an observed
parent result. The prior source manifest is retained with its exact identity.
Native success must come from the dedicated CI run with the pinned packages,
not from this dependency-limited local attempt.

## Resource and source identities

The wrapper accepts at most 1,000,000 input bytes and captures at most 1,000,000
combined stdout/stderr bytes plus one overflow sentinel. It kills and reaps a
worker at five seconds, with no retries. Eight native checking calls allow at
most four supplied candidates (one NetworkX and one SHACL call each). Package
import and hashing overhead counts toward the worker time. Raw stdout/stderr
digests, exact input digest, observed bytes, exit status, elapsed time, adapter
digest and requirement digest are retained. Worker Python audit hooks refuse
socket access, subprocess creation and file writes. Native inputs are constructed
in-memory without a remote RDF parser or service endpoint.

These are conservative public engineering ceilings derived from the offline
profile. A native API invocation is not evidence about each library's internal
algorithm iterations. The frozen `max_solver_or_control_iterations` correspondence
and equal opportunity accounting for actual Campaign-D subjects still need a
reviewed matched-resource binding. The audit hook is an execution policy for
these trusted authored fixtures, not a general sandbox for untrusted libraries.

The three direct versions retain the original Wave-06 audit: NetworkX 3.6.1,
RDFLib 7.6.0, pySHACL 0.40.1. All six transitive versions are pinned from pySHACL's
release lock for Python 3.12. `DEPENDENCY_SOURCES.json` records upstream identities
and available wheel hashes. CI records the actual downloaded package identities
in pip's installation report. Every invocation verifies installed versions and
hashes the installed files of all nine distributions, recording native import
paths. No statement of package availability or native test success is inferred
from a pin or a document alone.
Installed file hashes establish exact local source identity; they are not a
signed publisher-authenticity certificate. The zero network/provider values in
the profile are ceilings, not a claim to sandbox arbitrary native extensions.

`verify_sources.py` checks every authored file's SHA256/Git blob, all read-only
contract hashes, exact package inventory, and absence of ORION imports in the
parent arm. CI installs only the parent requirements, without installing ORION.

## Remaining Campaign-D binding obligations

1. Review the strongest practical composition, including native operations
   omitted here, against the frozen role before any paired outputs are accessed.
2. Bind an exact, content-preserving adapter from each actual D1/D2/D3 input to
   native graph candidates, shapes, representation opportunities and histories.
   This package intentionally does not access those frozen case fixtures.
3. Establish which constraints and candidate opportunities are applicable and
   complete, and justify the resource/iteration correspondence for every arm.
4. Complete the required parent-only fit and limitations review, then separately
   bind implementation/configuration/adapter identities in the existing registry.
5. Preserve the unfulfilled independent semantic-evaluator requirement for D2/D3
   and the already disclosed eight-of-59 unresolved cells. Local team review and
   these tests are not an independent evaluator or protected outcome evidence.

No source/history/authentication, strongest-parent, parity, scientific novelty,
OCM adoption, or programme-closeout terminal is granted by this package.

## Primary API references

- [NetworkX 3.6.1 `find_cycle`](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.cycles.find_cycle.html)
- [RDFLib Dataset API](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.graph/)
- [pySHACL v0.40.1 Python API and errors](https://github.com/RDFLib/pySHACL/blob/v0.40.1/README.md)
- [pySHACL v0.40.1 dependency definitions](https://github.com/RDFLib/pySHACL/blob/v0.40.1/pyproject.toml)
- [pySHACL v0.40.1 dependency lock](https://github.com/RDFLib/pySHACL/blob/v0.40.1/poetry.lock)
- [W3C SHACL validation reports](https://www.w3.org/TR/shacl/#validation-report)

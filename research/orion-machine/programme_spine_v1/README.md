# Programme spine V1

This closes the missing *engineering specification* coverage in #198 without
closing the scientific execution master #197. The old `OCM_TASK_LEDGER_V1.json`
was a scoped ten-deliverable #221 ledger. This directory maps all **231** source
checkboxes: 214 original IDs and 17 completion-package obligations assigned
clearly synthetic `OM-CLOSE-*` IDs. Original checkbox text, line numbers and
indented acceptance text are preserved; the full issue body is retained too.

## Index and scope

| Artifact | Purpose |
|---|---|
| `../CORE.md` | Start here, owners, authority and dependency map |
| `SOURCE_ISSUES_V1.json` | Captured full issue #197/#198/#221 text and observed update identities |
| `OCM_EXECUTION_BACKLOG_V1.json` | Atomic tasks, scheduling dependencies, cells, related artifacts, status, evidence, terminal, reopening |
| `OCM_EXECUTION_BACKLOG_V1.schema.json` | Draft-2020-12 schema using the documented restricted keyword subset |
| `validate.py` | Read-only structure, source, coverage, graph, evidence, event and accounting checks |
| `TASK_EVENTS_V1.jsonl` | Genesis and 18 engineering claim/readiness transitions, hash chained |
| `SOURCE_SNAPSHOT_V1.json` | Exact base/tree, source Git blobs, SHA-256, length and immutable event checkpoint |
| `TRUST_ANCHORS_V1.json` | Human-readable redundant anchor summary; the validator's reviewed code pins the actual trust root |
| `THEOREM_CANDIDATE_SNAPSHOT_V1.json` | Six statement bundles including trace learning, representation lattice, WLL and Warrant Lift; corrections/falsifiers and remaining gates |
| `OCM_PARENT_OWNERSHIP_MAP_V1.json` | Seven strongest-parent products, source-bound maps and exact open gaps |
| `OCM_RESOURCE_CONTRACT_V0.json` | All 12 master resource coordinates and context/accounting obligations; no fabricated measurements |
| `OCM_FAILURE_AND_NEGATIVE_LEDGER_V1.md` | All eleven §6 kill targets, contracted targets and falsifiers; historical failure pointer |
| `fixtures/invalid_cases.json`, `test_spine.py` | Explicit hostile mutation corpus and positive/no-alarm checks |
| `run_checks.py` | Fixed research-check allowlist and hash-chained actual run report |
| `../../../../.github/workflows/ocm-programme-spine.yml` | Fresh-checkout CI; optional proof target remains separately CANNOT_CHECK |

## Current checkpoint and completion

Nine WP0 engineering tasks are `READY_FOR_REVIEW`; none is asserted checked on
#197 before merged evidence reconciliation. All other rows remain `OPEN`.
Related historical evidence is explicitly insufficient to satisfy an entire task.
The source issues may subsequently change; this packet names the observation,
never claims the source is live-synchronized, and must reopen on material change.

The schema can represent `COMPLETE`. Engineering WP0-001…009 completion needs a
source-bound committed passing verification receipt, a positive denominator,
planted controls, and a matching event. The receipt names the exact source-body/task identities and pre-acceptance checkpoint; its six required checks, full hash chain and denominators must agree. Dependencies must already be complete. No extra external permission is required
for routine engineering verification. Current V1's exact anchored history has no
completion event. A new reviewed successor checkpoint must retain V1's full
source/event identity and append the acceptance; it cannot silently rewrite or
reset this historical version. The reviewed dependency graph is hash-bound too, so deleting a scheduling prerequisite requires a recorded successor rather than silently changing the gate. The validator authenticates receipt bytes and
structure, not a person's authority or truth of arbitrary output; the fixed runner
provides actual reruns. It does not update GitHub, schedule tasks or execute a
command supplied by the backlog.

Scientific/protected/adoption tasks require their own documented authorities and
are not promoted by this engineering checker. WP0-010 asks for independent
second-session review; #199/#245 are distinct unreturned science reviews.
Authoring-team cross-review does not discharge either requirement.

## Reproduce

```bash
python research/orion-machine/programme_spine_v1/validate.py
python -m unittest discover -s research/orion-machine/programme_spine_v1 -p test_spine.py -v
python research/orion-machine/programme_spine_v1/run_checks.py --output /tmp/ocm-spine-new-run.json
```

The output path must be new. No protected experiment is selected. The six required
checks are spine validation, its hostile tests, historical trace-parent
calibration, representation lattice, corrected compiler bound and substrate
semantics. These are exact/dev research checkers, not new empirical evidence.
Runner commands are constants in reviewed Python code; JSON never supplies shell
or program text. Fresh temporary bytecode location plus `-E -B` avoids accepting
unbound old caches. Each result binds command, actual exit, output hashes, preceding
receipt and relevant positive denominators; upstream failure makes dependants
`SKIPPED`, never PASS.

The seventh, optional proof-assistant target is `CANNOT_CHECK` because this
checkpoint registers no exact proof statement/toolchain/dependency target. This
is not a claim that no proof tool exists anywhere or that another proof lane has
not progressed. `--require-proof` makes that absence exit 2. `all_checks_pass`
therefore remains false even when all six required engineering checks pass.
Exit codes are 0 valid/required checks pass; 1 actual defect; 2 missing input,
unavailable dependency or required check that cannot run.

The stdlib validator evaluates every keyword present in this shipped schema and
refuses unknown keywords (`CANNOT_CHECK`). It is deliberately not a general JSON
Schema implementation. Schema and theorem-snapshot hashes are in the anchored
genesis. Corrupted source, missing Git objects, changed statements, unauthorized
terminals, empty denominators, cycles and event resets cannot become green.
Missing source/tool data is distinguished from a contradiction. Cryptographic
hashes detect change relative to the reviewed code and committed checkpoint;
they do not provide external signatures or independent scientific admission.

## Theorem and authority boundaries

Six retrospective statement bundles have exact Git/SHA identities. Their source
corrections and original failed statements coexist. This is a statement *snapshot*,
not the first prospective freeze before historical decisive runs. In particular:

- Lane #200's bounded interface/parent decomposition does not close its newer
  non-decomposability, strongest-parent or unreturned review obligations.
- Lane #201's representation/liveness counting is parent-owned, including paid
  reopening; it must not be double-claimed as a new Warrant Lift result.
- Lane #202's original F4 absolute-gap claim is refuted; only the successor's
  directional compiler inequalities have scope precedence. Full six-comparator
  resource manifests and actual simulation witnesses remain missing.
- Lane #203's substrate interpretation is not an independent semantics freeze.
  Future/current mechanization evidence must be imported by exact scoped identity.
- Parent saturation (including actual native adapters), priority, broad learning,
  natural language, novel or unsolved mathematics and quantum advantage remain
  separate obligations. Local finite checks imply none of them.

The current `V1_FREEZE_GATE.md` binds V1 at
`8f250fc3e55d6d6a28fb1fb33d9932ef1a8760b5` and permits non-authorizing reference
implementations/parity checks. Its receipt checker remains the gate authority.
Protected evaluations still need their separate custody and protocol. No V1
branch, protected campaign, model training or runtime source is changed here.

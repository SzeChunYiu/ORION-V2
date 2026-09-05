# Machine Epistemics certificate lifecycle V1

Additive science package for **#318**, under #197/#203 and the V2/OCM division #304.
Design registered in commit `69181cbbf356563aad662985f384373d4c081ff9` before local
execution. Base: `24566f00a9dc4425a438fcfac05d13c6b2d903db`.

## What is here

`THEORY.md` supplies seven scoped claims, written proofs/countermodels, resource
bounds and primary-source parent reconstruction. `reference.py` is a standard-library
finite research semantics, not OCM runtime. `test_reference.py` compares against
separate small completion/grounding oracles. `check.py` actually applies twelve
source mutations and requires their intended assertion failures. `RECEIPT.json`
records measured denominators, exact source hashes and the actual local environment.
`MODULE_CLOSURE.json` distinguishes local checks, scientific review and adoption.

The important correction is **dependency-specific invalidation**. A changed model,
prompt or calibration context must not silently keep a statistical operator guarantee
applicable. But an independently checked proof about an unchanged immutable object
need not depend on the latest configuration of the model that generated it.

No scope narrowing, majority vote, numeric confidence, cycle, digest or local test
result creates truth or action authority. Certificate applicability and proposition
truth are different types. The imported trust/judgment facts are explicit assumptions;
this package does not authenticate their issuers or run the substantive checker.

## Reproduce

From repository root, using Python 3.11 or later:

```sh
cd research/machine-epistemics-theory/certificate_lifecycle_v1
python -m py_compile reference.py test_reference.py check.py
python -m unittest -v test_reference
python check.py
```

`check.py` exits 0 when the baseline and all intended mutation failures match, 1 for
a defect, 2 for an unavailable required file/import. It rejects changed/empty baseline
denominators. When `RECEIPT.json` is present, the deterministic results, source hashes
and workflow hash must match it. Environment fields are reported separately so the
same exact result can be tested across Python versions. Do not overwrite a historical
receipt just to make a failure disappear; make a disclosed successor study.

The dedicated workflow runs only this package on Python 3.11/3.12/3.13. It does not
run protected studies. A checked-in workflow is not evidence of a completed CI run;
consult actual check results. The local receipt does not claim full-repository tests,
macOS/LUNARC execution, proof-assistant checking or independent review.

## Review assignments and findings

These are internal analytic roles in one authoring session, **not five independent
experts or reviewer approvals**. Each constructive claim was examined against its
opposing condition; the external review gate remains unfilled.

| Analytic role/background | Constructive target | Hostile check / resulting boundary |
|---|---|---|
| Formal methods: proof systems and fixed points | grounded applicability and invariant | cycles start UNKNOWN; a finite proof tree must ground every successful route |
| Statistics: calibration and selection | scoped operator evidence | marginal 19/20 correctness permits a failing individual and failing selected subgroup |
| Systems: provenance, versioning and replay | identity-complete use at a snapshot | ABA, altered registry interpretation, mutable input failure and checkpoint substitution |
| Language/semantics: typed statements and reference | statement/subject/kind preservation | identical labels are not identical meaning; exact strings do not prove paraphrase equivalence |
| Hostile parent evaluation: assurance/TMS ancestry | minimize genuinely new commitments | parent product owns the mechanics; neither local tests nor this author supply external adoption |

## Foundation integration, not competing ownership

#312/#313 own `foundation_v1` and the overarching typed-warrant/gap corrections.
Their overlapping ownership must be reconciled by the coordinator; this package edits
neither branch or path. #314 owns decision/query frontiers, #315 causal transport.
This package exports certificate identity, grounded applicability and reference
lifecycle behavior to that integration. It does not replace those theories or close
#197, #200–#205, #245 or any OCM milestone.

Before absorption into ORION-OCM: reconcile the type names with the accepted foundation
registry; independently review the actual statements and trust assumptions; bind the
exact source/target commits and artifacts; run OCM parity and boundary hostiles; obtain
an external adoption decision. No approved absorption record is shipped. General
operator guarantees remain blocked from exact-individual truth coercion throughout.

The whole foundation closes only after its owners assemble the accepted primitive
registry and each in-scope obligation has an earned disposition. A register of open
work, this local green receipt or a draft PR is not that closure.

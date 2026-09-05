# F4/F5 finite semantic codec and renderer reference

**Terminal: `FINITE_CODEC_REFERENCE_REVALIDATED`.** This new package advances
issue #329 F4/MEG-24 and F5/MEG-25. It preserves all earlier pinned studies.
Independent protected codec evaluation and unrestricted natural-language
semantic fidelity remain **CANNOT_CHECK / OPEN_RESEARCH**. No final F4/F5 or
programme admission is issued here.

The previous batch-3 C2 correctly checked its declared finite tuple model, but
its decoder was effectively an identity on renderer-supplied proposition and
marker tuples. A matching tuple did not establish what an actual surface said.
This package checks two actual, different grammar strings and reparses the
surface at the commitment boundary. The grammar is deliberately explicit:
neither codec accepts arbitrary English.

## Registered semantic object

`semantics.py` registers finite, disjoint entity sorts, unary/binary predicate
signatures, canonical predicate spellings and optional ambiguous aliases. The
formula constructors are atom, negation, conjunction, universal quantification
and existential quantification. Variables use de Bruijn indices: `@0` names
the innermost binder, `@1` its immediate parent. Validation checks the exact
binder depth and sort, predicate arity, constructor shape and immutable nested
data. Boolean values cannot masquerade as integer variable indices or budgets.
Empty sorts are permitted explicitly: universal quantification over an empty
sort is true, existential quantification is false.

For registry `R`, let `G_R` be its ordered inventory of all well-typed ground
predicate applications. A world is one Boolean assignment to every element of
`G_R`. The checker enumerates all `2^|G_R|` worlds and evaluates a closed formula
in each world. Its semantic object is `(digest(R), G_R, truth_vector)`.

**Finite equivalence theorem.** For formulas `f,g` in the same registered
signature and finite domains, the computed objects are equal iff `f` and `g`
have equal truth values in every registered world.

**Proof.** Each interpretation of the registered predicates assigns one truth
value to each well-typed ground application, hence corresponds to exactly one
enumerated Boolean assignment. Structural recursion is the declared semantics
of each constructor, with the binder environment extended at its front for
each quantifier. Equality of the complete truth vectors is therefore exactly
equality in each of these interpretations. The domain/signature/epoch binding
prevents reuse under a different world inventory. An incomplete enumeration
returns CANNOT_CHECK and produces no semantic object. ∎

This theorem is a finite model evaluation parent, not a new equivalence theorem
over all structures. The [Isabelle Nitpick manual](https://isabelle.in.tum.de/doc/nitpick.pdf)
illustrates the established bounded-model distinction; this package does not
invoke or claim Nitpick verification. A semantic seed here is a hash of this
finite quotient object. Hash collision resistance is the ordinary addressing
assumption; semantic comparisons in the gate compare the full objects. This
key is **not** OCM's `MeaningGraph` canonical graph digest or its KSO seed
distribution, and no silent runtime substitution is authorized.

Structural identity and semantic equality are different: `p` and `not not p`
have distinct structural digests but equal finite semantic objects. Conversely,
equal truth vectors without the registry binding are not interchangeable.
No single ground-world observation constitutes equivalence.

## Two codec paths and ambiguity

| Path | Example | Decoder mechanism |
|---|---|---|
| Sentence grammar | `every person : ( some person : ( @1 likes @0 ) )` | Full-coverage tokenization, recursive descent, bounded ambiguity-set expansion |
| Functional grammar | `all[person]{some[person]{likes(@1,@0)}}` | Separate character-cursor prefix parser |

Encoders have separate recursive implementations. Decoders never call an
encoder or consult a roundtrip/gold lookup table. Shared code is restricted to
typed AST validation, term spelling and the declared semantic evaluator.
Canonical predicate spellings cannot be shadowed by aliases. An alias such as
`bank` can name two registered unary predicates, in which case the sentence
decoder preserves both readings. Type constraints may eliminate an ill-typed
reading; scores and ranking never eliminate a well-typed reading. An ambiguity
budget failure does not select the first remaining candidate.

**Roundtrip theorem.** For each well-typed formula within the declared shape
and parser budgets, either canonical encoder followed by its decoder returns
exactly that formula.

**Proof.** Canonical names are unambiguous. Atom argument order and variable
indices are emitted literally. Each connective/quantifier has an explicit
delimiter form, and each decoder reconstructs that constructor recursively
without changing the ordered children or binder indices. Induction on formula
structure gives the result. Validation prevents out-of-scope free variables
and sort-mismatched terms. ∎

This is engineering independence between two code paths, not independent
annotation custody or a protected test of two independently trained NLP
systems. Their shared evaluator could share a semantic defect. Therefore the
suite also checks an independently specified two-by-two Boolean relation
matrix across all 16 worlds, including the diagonal world distinguishing
`forall x exists y R(x,y)` from `exists y forall x R(x,y)`, plus negation scope,
quantifier duality, typed nested binders and empty-domain known answers.

## Renderer capability and actual-text fidelity

`renderer.py::render` receives only an exact-typed `RenderView`, an immutable
registry and a registered codec name. A view contains shown formulas, markers,
citations and an evidence epoch. It contains no store/session handle or callback.
The trusted implementation reads that data and returns text. Its input object
graph contains only validated frozen records, tuples, strings, integers and
Booleans. It has no operation that writes an epistemic store.

This is a property of the trusted function and its interface, **not** a sandbox
for arbitrary Python renderer code. [Python's dataclass documentation](https://docs.python.org/3/library/dataclasses.html#frozen-instances)
describes frozen records as an emulation of read-only objects. Python
introspection, a hostile global environment, monkeypatching or external memory
mutation are outside the capability proof. A production untrusted plugin needs
an independently enforced process/capability boundary.

The separate `commitment_eligibility` gate receives current external evidence,
the current epoch, scope and protected semantic identities. It:

1. Parses the markers, citations and the **actual output text**, requiring one
   unique well-typed reading per expected non-withheld claim.
2. Compares complete finite semantic objects, rejecting added or omitted claims,
   changed negation, entities, quantifier order, markers or citations.
3. Checks each cited record supports the same finite semantic seed in the
   current scope. An assertion requires nonempty, LIVE, world-authorized
   support. A speaker record cannot become world authority through rendering.
4. Rejects protected semantic content even if included in the shown plan.
   `HEDGE` reports registered uncertainty and never grants world truth;
   `WITHHOLD` emits no claim. Missing evidence, unresolved ambiguity, stale
   epoch or insufficient evaluation budget returns CANNOT_CHECK.

The gate returns eligibility, not a store commit. Evidence records, epoch and
authority are external premises; this reference does not authenticate their
origin. A runtime must serialize a later actual commitment with the evidence
snapshot to prevent an intervening revocation. Eligibility now does not prove
authority at a past or later wall-clock time. Dead support is withheld rather
than turned into a negated world fact.

## Bounds, review and replay

The default bound is 4,096 complete worlds, 2,000,000 evaluator calls per
semantic computation, 256 AST nodes, depth 24, and 128 sentence readings. The
work includes registry traversal and ground-inventory construction as well as
the counted recursive evaluator calls; the count is not a CPU-time guarantee.
The registry is finite input. Exponential world enumeration is useful as an
exact small reference oracle, not a proposed large-language runtime optimizer.

```bash
PYTHONPATH=research/machine-epistemics-theory python -m semantic_codec_v1
PYTHONPATH=research/machine-epistemics-theory python -O -m semantic_codec_v1
PYTHONPATH=src python -m pytest tests/unit/test_semantic_codec_v1.py
```

The standalone replay checks 28 formulas through both codecs and 16 independent
quantifier worlds; it uses explicit checks that remain active under `python -O`.
The full package suite has 53 passing test cases, including 58 constructed
roundtrips, actual-text mutants, live-evidence changes, protected-content
controls, ambiguity preservation and malformed immutable inputs.

Independent internal mathematical and immutable-state reviews both identified
one defect: hashing an alias tuple before validating its members caused raw
TypeError for list/dictionary aliases. Two regressions were observed RED;
Boolean/None controls passed. Validation was reordered to reject nonidentifier
members before hashing, and all four cases plus the complete suite pass. This
negative history is retained in the regression test and this account. These
reviews are internal engineering review, not the external evaluator gate.

| Acceptance requirement | Current result | Remaining requirement |
|---|---|---|
| F4 distinct codec paths | Implemented on the declared typed finite grammar | Protected, independently sourced codec/semantic evaluation |
| F4 negation, quantifier, ambiguity controls | Executable controls and direct finite-world oracle | Coverage and meaning custody for open language |
| F5 read-only renderer | Trusted data-only reference API; no store write path | Enforced isolation for untrusted runtime plugins |
| F5 semantic fidelity | Actual-text reparse and finite semantic/evidence gate | Runtime adoption with authenticated evidence and atomic commitment |
| F4/F5 generality or scientific admission | Not established | Original issue #329 acceptance remains open |

# FM30 — Formal Concept Closure and Revision: Exact Known-Answer Study Design (V1)

**Lane:** FM30, L4 formal transfer mechanics (issues #48, #50 §C1).
**Status:** frozen prospective design. No protected outcome has been generated or inspected.
**Machine-readable companion:** `FM30_FORMAL_CONCEPT_REVISION_EXACT_STUDY_DESIGN_V1.json`.

## 1. Task and endpoint

Each instance presents a formal context `K0` with **two tracked concepts**, a
revision `K1`, and a **hidden object** added in `K1`. The registered endpoint is
the triple (transition class, old-valid-case retention verdict, hidden object's
membership), scored as one exact match — the protocol's three FM30 primaries.

| transition | meaning |
|---|---|
| `NO_CHANGE` | both tracked concepts survive with the same extent and intent |
| `SPECIALIZE` | the tracked concept's intent strictly grows |
| `SPLIT` | `K1` has ≥ 2 maximal concept extents strictly inside the tracked extent where `K0` had ≤ 1 |
| `MERGE` | the union of two incomparable tracked extents becomes closed, having not been closed before |
| `BRIDGE` | a new concept extent strictly intersects both tracked extents without containing either |

**Computing a Galois closure is deliberately not the endpoint.** The
Ganter–Wille derivation operators decide it exactly, so a study built on it would
report parent sufficiency by construction rather than by measurement.

### Three definitional choices, registered before any outcome

1. **Scope.** The transition class is computed on `K1` **restricted to the
   objects that already existed in `K0`**, because it is a statement about how
   *existing* concepts move. Without the restriction the hidden probe object —
   which by construction carries the tracked intent — joins the tracked extent
   and destroys it as an extent in every family at once, which is an artifact of
   the probe rather than a property of the revision. The hidden object's
   membership is a separate primary, computed on the full `K1`.
2. **Split.** Requiring the tracked extent to *stop being closed* would be wrong
   (adding an attribute to part of it leaves the whole still closed), and
   requiring the sub-extents to *cover* it would be wrong too (an object with no
   distinguishing attribute belongs to none of them). The registered definition
   counts maximal proper sub-extents before and after.
3. **Retention.** Defining it as "the survivors are still covered" would be
   tautological — the survivors are covered by construction. The registered
   property is that there **are** no casualties: every member of the tracked
   extent still satisfies the defining intent. A registered fraction of
   revisions **retract** one incidence pair from a tracked member (the
   protocol's counterexample-driven revision), which is what gives this endpoint
   a denominator at all.

### Registered precedence

More than one predicate can hold on a single revision — adding an attribute that
covers a union both merges and specializes. The class is the highest-precedence
predicate that holds, in the frozen order **SPLIT > MERGE > BRIDGE > SPECIALIZE
> NO_CHANGE**, and the **full hold-set is published in every oracle answer** so
the losing predicate is never silently dropped. Fixture `KA-09` pins this.

## 2. Oracle and its independent cross-check

`concepts_powerset` closes every object subset with the derivation operators.
`concepts_next_closure` is Ganter's **NextClosure**, walking closed attribute
sets in lectic order without ever materialising the powerset. They must agree on
the concept set of **every context of every instance**, and on the endpoint
triple and both concept counts (`G0b`).

## 3. Arms, and why the comparator is the federation

| arm | owns | native boundary (tested, recorded) |
|---|---|---|
| `P1_GALOIS_CLOSURE` | the derivation operators, exactly | classifies no transition — only intent growth |
| `P2_LATTICE_ORDER_GEOMETRY` | split and merge | never inspects intents, so specialization is invisible |
| `P3_ATTRIBUTE_EXPLORATION` | implication counterexamples / bridges | computes no lattice |
| `P0_FIXED_LESSON_INJECTION` | — | the protocol's frozen-table baseline |

The federation is combined under a rule fixed before any outcome: *extent
geometry decides first, because split and merge are structural facts about the
lattice; if it reports no change, the implication parent may report a bridge; if
neither fires, the closure parent decides specialization versus no change.*

### M is an independent implementation, and its limitation is real

`M` **never enumerates a concept lattice**. It works outward from the tracked
concept, closing one seed per attribute with the reference module's
`formal_concept_closure` and comparing sub-concept counts before and after, then
testing merge and specialization on chosen seeds.

Closing a handful of seeds gives a **lower bound** on the number of
sub-concepts, and comparing two lower bounds can flip an inequality that the
full lattice resolves the other way. On a 100-instance development probe `M`
scores **0.980** against the federation's 1.000, diverging on two bridge
instances. Verified not to be a scope artifact: restricting `M` to the
pre-existing objects changes neither instance.

Three *earlier* divergences were defects in `M` and were repaired before
freezing — it reported `MERGE` for concepts that were already merged; its split
test counted attribute-cuts that are not themselves concepts; and an earlier
draft looked only at new attributes and so missed splits formed by an old
attribute together with a new one. A broken mechanic is as much a strawman as a
broken parent.

## 4. Gates

Standard block (`G0a`–`G0f`, `G1a`/`G1b`, `G3`) as in FM10 and FM20, with one
suite-specific change:

**`G2`'s non-compensatory endpoint here is old-valid-case loss, not
over-acceptance.** None of the five transitions is an "accept", so the inherited
permissiveness rule would have had an empty scope and passed vacuously — the
defective gate shape this programme keeps rediscovering. The registered rule is:
*on instances where the oracle says retention fails, `M` claims retention no more
often than `F0`* (≥ 10 such instances required, else `CANNOT_CHECK`), **and** the
counter is shown live on those same instances. On the development probe 26 of
100 instances have `retention_ok = False` and the retention ablation makes 26
unsafe claims, so the denominator is real.

`G1a` also carries a liveness control; every gate publishes the number of
instances its rule was actually evaluated on; a gate below its registered
minimum returns `CANNOT_CHECK`, never `PASS`, and the route line names it.

## 5. Routes

`PARENT_SUFFICIENT` is the pre-registered expectation, and on the development
probe `M` is expected to fall **slightly short** of the federation. If `G1a`
fails because `M` is worse, the route is still `PARENT_SUFFICIENT` and that is
recorded explicitly rather than presented as a study defect.

## 6. Sizes, seeds and execution

100 protected instances (20 per family × 5 ≥ the 96 required by issue #50 §C1);
15 development; 10 selftest. Deterministic, single-core, well under a second.
Hash-seed independence is verified across `PYTHONHASHSEED` 0/1/12345.

Protected seed commitment:
`af34cfe913bff1ef0f661b1ee4b46ff68360fa3a6bea2d06b776ca2b35857e4a`
(sha256 of the seed at `~/.orion-custody/fm/FM30_PROTECTED_SEED_V1.txt`).

Exactly one protected run and one analysis. No design constant, gate, arm,
oracle rule or seed may change after outcome access.

## 7. Authority

Grants no scientific truth, no F2 superiority, no field status, no submission
readiness.

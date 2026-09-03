# FM60 — Parent Fidelity Receipt and Development-Split Summary (V1)

**Scope of this file:** FM60 only. It is a separate file from
`FM_PARENT_FIDELITY_RECEIPT_V1.md` (FM10) on purpose, so concurrent FM lanes do
not contend for the same lines. The file is the single place where FM60's
comparators earn the right to be used.

**Status:** development artifacts only. **No protected outcome has been
generated or inspected.** `PROTECTED_RUN_AUTHORIZATION.json` is absent, so
`fm_run.py FM60 protected` refuses (exit 3), asserted by
`tests/unit/test_fm_exact_suites.py::test_protected_stage_refuses_without_authorization`.

**Run:** Mac (local), 2026-09-02, `python3 fm_run.py FM60 selftest` then `dev`;
selftest completes in 0.66 s and the development split in 0.19 s. Two
consecutive runs produce byte-identical results and custody files (asserted by
`test_development_split_is_deterministic`), and the files are byte-identical
across processes started with different `PYTHONHASHSEED`, which that in-process
test cannot see.

## 1. Frozen code and artifacts (sha256)

| file | sha256 |
|---|---|
| `fm_core.py` (unchanged; shared) | `2b345a707d099e93a30d4b9431f206dd03c6f3fdad3edb85e3a175194e26a7ca` |
| `fm_run.py` (unchanged; the `SUITES` entry for FM60 was already present) | `058acc3350603dbe6a247fb8ec739335993b0a27a0fa008251b49a210138b4ec` |
| `fm60_suite.py` | `4fc0ef81385708a4c1efa3d8cc6c15efecd739d38954ae02a502f7e5ceb6cf6a` |
| `FM60_..._DESIGN_V1.json` | `f8fe7f09463938c25df3b8ddba0ead71a06616de5affddc1622b744fde463a69` |
| `fm60/results/FM60_DEVELOPMENT_RESULTS_V1.json` | `a97a9bd211a246866cf55633c5e8fce64514ad207a7e4eba20d10f367228dc46` |
| `fm60/results/FM60_DEVELOPMENT_EXPECTED_CUSTODY_V1.json` | `2d4603df3cce807499a5290599db6e37825a9c8f5de4535a31f9cf9705f60324` |
| `fm60/results/FM60_SELFTEST_REPORT.json` | `0166dfb6ea955183b93ed476a356bd31a70189d0ed1b68444c8050a67cdda94c` |

FM60 protected seed commitment (sha256 of the stripped bytes of the custody
seed file, computed by replicating `stage_protected`'s own two expressions):
`54a74a5960b88ed7973b690890a3fcb21bf80580d2a459075aae799aacbe02f2`.
A protected run additionally requires `acknowledged_design_sha256` to equal the
design-JSON hash above and `suite` to equal `FM60`.

## 2. FM60 parent fidelity: native known-answer tests (32/32 PASS)

Every comparator passed its own native tests before being used
(`fm60_suite.parent_fidelity`, executed by `selftest` and by the unit test).

| parent | tests (all PASS) |
|---|---|
| `P2_EXHAUSTIVE_MODEL_SEARCH` (Mace4-style) | finds a countermodel for a known non-theorem (symmetric + transitive does not entail reflexive); its countermodel passes the independent validator; it returns the **minimum size** countermodel rather than merely a countermodel (irreflexive + antisymmetric first fails transitivity at domain size 3, not 2); it counts two independent obstructions and exhibits one model for each; documented boundary recorded — exhausting the space yields no derivation, so its acceptance is a bare claim with `witness is None` |
| `P3_DERIVATION_PROOF_SEARCH` (Prover9-style forward chaining) | **all 50 registered implication rules are verified exhaustively against the whole 4,164-structure space, 0 invalid**; derives asymmetry ⟹ irreflexivity; the derivation it emits passes the independent validator; chains a two-premise rule to a new conclusion; documented boundary recorded — a prover produces no countermodels, so it abstains instead of refuting |
| `P4_SMALL_SCOPE_BOUNDED_CHECK` (Alloy-style) | exhaustive inside its registered scope: finds the in-scope countermodel, and that countermodel passes the validator; documented boundary recorded — it is blind to an obstruction that first appears one size above its scope, which is exactly the small-scope hypothesis' own bet |
| `P0_INDUCTIVE_CONFIRMATION` | refutes when the presented evidence set contains a countermodel; generalises from confirming evidence alone; documented boundary recorded — its acceptance carries no witness and is rejected by the validator, because induction from instances is not a proof |
| `P1_FIXED_LESSON_TABLE` | its verdict is identical for two different hypothesis sets with the same conclusion (a frozen table is not context sensitive); it reports multiplicity when two conclusions are refuted by its frozen corpus; documented boundary recorded — its canned countermodel can fail validation because it need not satisfy the instance's hypotheses |
| `F0_PARENT_FEDERATION` | takes the derivation parent on a bounded theorem (`source == P3`); takes the model parent on a non-theorem (`source == P2`); abstains when neither parent can discharge the claim |
| `WITNESS_VALIDATOR` | accepts a genuine countermodel; rejects one that does not satisfy the hypotheses; rejects a non-minimal model offered for a minimality claim; rejects a derivation citing an unregistered rule; rejects a derivation whose premises are not yet available |
| `MODEL_SPACE` | the index ↔ structure map round-trips over all 4,164 models; **the vectorised truth column agrees with direct scalar evaluation on all 108,264 model–formula pairs**; the size strata partition the space; `SINGLETON_DOMAIN` and `AT_LEAST_TWO` are exact complements |
| `ORACLE_PAIR` | both oracle algorithms agree on every hand-authored fixture |

Five boundaries are recorded as scope notes rather than defects, because they
are what makes the federation the honest comparator: `P2` cannot produce a
proof, `P3` cannot produce a countermodel, `P4` cannot see past its scope, `P0`
has no witness at all, and `P1` is context-free. None is a strawman; each is
complete within its own competence.

## 3. Known-answer fixtures (G0a): 12/12

All twelve hand-authored fixtures are reproduced by the exhaustive oracle **and**
by the independent stratified cross-check. They pin the classical facts the
suite is built on: asymmetry ⟹ irreflexivity; a strict order is antisymmetric;
symmetric + transitive does **not** entail reflexive; irreflexive + antisymmetric
first fails transitivity at domain size three (`KA-04`, the classical minimal
counterexample); seriality is not reflexivity; connexity entails reflexivity;
reflexive + Euclidean entails symmetry and transitivity.

`KA-11-MULTIPLICITY-DOMINATES-MINIMALITY` pins the one registered classification
choice: with `H = {IRREFLEXIVE, ANTISYMMETRIC}` and
`C = TRANSITIVE ∧ NONEMPTY_R`, transitivity first fails at size three while
non-emptiness already fails at size one. A minimality-first reading would call
this a plain rejection; the registered order calls it
`MULTIPLE_INDEPENDENT_OBSTRUCTIONS`. No hand-authoring correction was needed:
all twelve fixtures were reproduced by the oracle on first execution.

One development-time correction was made to a **fidelity test**, not to any
answer: the first draft of P1's "canned witness can fail validation" test used
`H = {EMPTY_R}`, for which P1's canned size-one empty structure happens to be a
genuine countermodel, so the test did not fire. It was rebuilt on
`H = {CONNEX}, C = EMPTY_R`, where the canned structure is not a model of the
hypotheses at all. The validator was not changed; the test was.

## 3a. Independence of the mechanic from its own comparator

`M` does **not** call either parent's procedure. Its proof stage is a bounded
forward chaining with its own rule ordering and a budget of 12 rule
applications; its obstruction stage explores the hypothesis region by **local
repair** — breadth-first over single-cell edits that stay inside the region,
seeded from the instance's evidence set plus bounded random probing — and is
exhaustive only at domain sizes ≤ 2, where the space is small enough to certify
minimality directly.

What `M` shares with the rest of the suite is the **per-model checking
primitive**: like every arm, `M` asks whether a given structure satisfies a given
formula, and that question is answered from the materialised truth table. What is
`M`'s own is the **search** — which structures it ever asks about. This is the
FM10 pattern (there, every arm shared `profile_map` and only the search
differed), and it is why "oracle 2 never materialises the space" in §3 of the
design is a statement about the *cross-check*, not about the arms.

Two separate claims are made about `M`'s independence, and they were checked
differently. Both are recorded here as checked:

* **The G1a discordance counter is live.** Verified by the same split:
  `test_mechanic_is_not_a_wrapper_of_its_own_comparator` passes for FM60, and
  the counter registers 12 / 5 / 3 / 3 ablation-versus-parent disagreements
  (below). This establishes that the counter can be nonzero — it does **not**
  by itself establish anything about `M`'s own search.
* **`M`'s own search is genuinely incomplete and budget-sensitive.** Verified
  directly by a scratch probe that starves it (registered constants unchanged in
  the frozen code; the probe monkey-patches them in a throwaway process):

  | `M_SEED_TARGET` / `M_PROBE_BUDGET` | dev (15) | probe (125) |
  |---|---|---|
  | **8 / 6000 (registered)** | **1.000** | **1.000** |
  | 1 / 400 | 1.000 | 1.000 |
  | 1 / 40 | 1.000 | 1.000 |
  | 1 / 4 | 1.000 | 0.992 |
  | 1 / 1 | 0.933 | 0.968 |

  `M`'s exact rate moves off 1.000 when its exploration budget is cut, so the
  1.000 it reports at the registered budget is a rate the search was capable of
  not reporting. At the registered budget no divergence from `F0` was observed on
  either split; the incompleteness is structural *and* demonstrated, but it did
  not bite at the registered budget on this space.

`G1a`'s **liveness control** on the development split: the discordance counter
registers 12 (`M_MINUS_OBSTRUCTION_SEARCH`), 5 (`M_MINUS_MINIMALITY_ESCALATION`),
3 (`M_MINUS_MULTIPLICITY_CHECK`) and 3 (`M_MINUS_PROOF_WITNESS`) disagreements
with the parent, so the zero it reports for `M` is a zero the counter was
capable of not reporting.

`G2`'s over-acceptance counter is shown live on the same split by
`C_ALWAYS_ACCEPT`, which registers **12 over-acceptances** on the 12 blocked
instances while `M` and `F0` register 0.

### 3b. What `P0` actually claimed, before witness validation

`run_arm` records every arm's `claimed_disposition` alongside the validated one,
so the decoy family's *measured* content is visible rather than merged into a
0.00. On the development split `P0_INDUCTIVE_CONFIRMATION` claimed:

| family | claimed | after validation | reading |
|---|---|---|---|
| `no_obstruction` | `TRANSFER_VALID` ×3 | `CLAIM_WITHOUT_VALID_WITNESS` ×3 | witness failure: induction is not a proof |
| `misleading_surface_support` | `TRANSFER_VALID` ×3 | `CLAIM_WITHOUT_VALID_WITNESS` ×3 | **fooled on 3/3**: it saw no countermodel in the presented evidence — *and* had no witness |
| `single_hidden_obstruction` | `REJECT_WITH_COUNTEREXAMPLE` ×3 | unchanged ×3 | correct, with a valid witness |
| `multiple_obstruction` | `REJECT_WITH_COUNTEREXAMPLE` ×3 | unchanged ×3 | **measured failure**: valid witness, but it never sees the second obstruction |
| `minimal_counterexample` | `REJECT_WITH_COUNTEREXAMPLE` ×3 | unchanged ×3 | **measured failure**: valid witness, but not a minimality claim |

So `P0`'s 0.00 is not one phenomenon. On `multiple_obstruction` and
`minimal_counterexample` it is a *measured* limitation of a confirmation baseline
that survives witness validation and still gets the disposition wrong; only on
`no_obstruction` and `misleading_surface_support` does the witness gate do the
work, and on the latter the arm was independently fooled on 3/3 instances, which
is the decoy family's measured content.

Four results in the tables below are **definitional and labelled as such**:
`P2` is exact on every reject family and 0.00 on `no_obstruction` by
construction; `P3` is its exact mirror; `F0` is therefore exact by construction
and its content is the attribution of which parent owns which half of the
endpoint; and `misleading_surface_support` instances are rejected unless every
presented model confirms the conclusion, so the fact that `P0` finds no
countermodel there is definitional (§3b separates that from what it measured).

## 4. Planted positives (G0e): 7/7 fire

Registered trip-wires, all executed in the same run that reports the study's
zeros:

| gate | planted case | fires |
|---|---|---|
| `G0b_ORACLE_SELF_AGREEMENT` | a small-scope-only pseudo-oracle on an instance whose obstruction first appears one size above that scope | yes |
| `G0a_KNOWN_ANSWER` | a deliberately wrong expected disposition | yes |
| `G2_ANTI_PERMISSIVENESS` | `C_ALWAYS_ACCEPT` on an oracle-blocked instance | yes |
| `G0f_FAMILY_DISCRIMINATION` (**ceiling**) | a synthetic per-arm table in which every arm scores 1.000 must **FAIL** | yes |
| `G0f_FAMILY_DISCRIMINATION` (**floor**) | a synthetic per-arm table in which every arm scores 0.267 — the literal FM/FG R2 fm60 row, all five arms at 32/120 — must **FAIL**, and specifically on the *solvable* half | yes |
| `HARD_GATE_FORMAL_CLAIM_WITHOUT_WITNESS` | an arm returning the oracle's own disposition with a structure that is not a model of the instance's hypotheses must be rewritten to `CLAIM_WITHOUT_VALID_WITNESS` by the same dispatcher that produces the study's numbers, while the honest arm on the same instance is not | yes |
| `G3_MECHANISM_BY_OMISSION` | `M_MINUS_MINIMALITY_ESCALATION` must be wrong on a minimal-counterexample instance where `M` is right | yes |

## 5. FM60 development split (15 instances, 3 per family — DEVELOPMENT, not protected)

Columns after the counts are per-family exact rates in the order
`no_obstruction | single_hidden_obstruction | multiple_obstruction |
minimal_counterexample | misleading_surface_support`.

| arm | exact | rate | over-accept | under-accept | no_obs | single | multi | minimal | misleading |
|---|---|---|---|---|---|---|---|---|---|
| `P0_INDUCTIVE_CONFIRMATION` | 3/15 | 0.200 | 0 | 3 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| `P1_FIXED_LESSON_TABLE` | 1/15 | 0.067 | 0 | 3 | 0.00 | 0.33 | 0.00 | 0.00 | 0.00 |
| `P2_EXHAUSTIVE_MODEL_SEARCH` | 12/15 | 0.800 | 0 | 3 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| `P3_DERIVATION_PROOF_SEARCH` | 3/15 | 0.200 | 0 | 0 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `P4_SMALL_SCOPE_BOUNDED_CHECK` | 9/15 | 0.600 | 0 | 3 | 0.00 | 1.00 | 1.00 | 0.67 | 0.33 |
| **`F0_PARENT_FEDERATION`** | **15/15** | **1.000** | 0 | 0 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| **`M_F2_OBSTRUCTION_DISCOVERY_FULL`** | **15/15** | **1.000** | 0 | 0 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| `M_MINUS_OBSTRUCTION_SEARCH` | 3/15 | 0.200 | 0 | 0 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `M_MINUS_PROOF_WITNESS` | 12/15 | 0.800 | 0 | 3 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| `M_MINUS_MINIMALITY_ESCALATION` | 10/15 | 0.667 | 0 | 0 | 1.00 | 1.00 | 1.00 | 0.00 | 0.33 |
| `M_MINUS_MULTIPLICITY_CHECK` | 12/15 | 0.800 | 0 | 0 | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 |
| `C_ALWAYS_ACCEPT` | 3/15 | 0.200 | 12 | 0 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| `C_ALWAYS_BLOCK` | 3/15 | 0.200 | 0 | 3 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 |
| `C_RANDOM_DISPOSITION` | 0/15 | 0.000 | 1 | 3 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

Exact per-family and per-arm numbers are in
`fm60/results/FM60_DEVELOPMENT_ANALYSIS_V1.{json,md}`; the table above is a
summary and the JSON is authoritative.

### 5.1 Development gate block

| gate | verdict | evaluated |
|---|---|---|
| `G0a_KNOWN_ANSWER` | PASS | 12 fixtures |
| `G0b_ORACLE_SELF_AGREEMENT` | PASS | 15 instances |
| `G0c_NULL_CALIBRATION` | PASS | 4 checks |
| `G0d_DECOY_COVERAGE` | PASS | 3 decoy families |
| `G0e_PLANTED_POSITIVES` | PASS | 7 trip-wires |
| `G0f_FAMILY_DISCRIMINATION` | PASS | 2 halves (11 arms solvable, 4 weak arms separating) |
| `G1a_PARENT_REPRODUCES_M` | PASS | 15 instances (identity 1.000) |
| `G1b_M_ADVANTAGE` | NOT_FIRED | 15 instances, 0 discordant pairs |
| `G2_ANTI_PERMISSIVENESS` | PASS | 12 oracle-blocked instances |
| `G3_MECHANISM_BY_OMISSION` | NOT_APPLICABLE | no claimed advantage |

`G0c` detail: constant arms 0.200 / 0.200, random 0.000, and `M` against
within-split shuffled oracle labels 0.267 — all under the registered 0.40.
`G0f` detail: *solvable* best arm `F0_PARENT_FEDERATION` at 1.000 (threshold
0.95, **not a floor family**); *separating* weak arms
`P1_FIXED_LESSON_TABLE` 0.067, `P0_INDUCTIVE_CONFIRMATION` 0.200,
`M_MINUS_OBSTRUCTION_SEARCH` 0.200 and `P4_SMALL_SCOPE_BOUNDED_CHECK` 0.600, all
at or below the registered 0.85 (**not a ceiling family**).

Holm across the five per-family paired tests: every raw and adjusted p is 1.000
(zero discordant pairs). On development this predicts the pre-registered route
**`PARENT_SUFFICIENT`**.

### 5.2 Same-size probe on the public development seed (125 instances)

Not protected evidence: this is `fm_run.py FM60 dev --per-family 25`, the public
development seed at protected size, run to size the protected job and to check
that nothing degenerates at scale. Every gate PASS, route `PARENT_SUFFICIENT`,
`G2` evaluated on 100 oracle-blocked instances.

| arm | rate | over-accept | arm | rate | over-accept |
|---|---|---|---|---|---|
| `P0_INDUCTIVE_CONFIRMATION` | 0.200 | 0 | `M_F2_OBSTRUCTION_DISCOVERY_FULL` | **1.000** | 0 |
| `P1_FIXED_LESSON_TABLE` | 0.160 | 0 | `M_MINUS_OBSTRUCTION_SEARCH` | 0.200 | 0 |
| `P2_EXHAUSTIVE_MODEL_SEARCH` | 0.800 | 0 | `M_MINUS_PROOF_WITNESS` | 0.800 | 0 |
| `P3_DERIVATION_PROOF_SEARCH` | 0.200 | 0 | `M_MINUS_MINIMALITY_ESCALATION` | 0.752 | 0 |
| `P4_SMALL_SCOPE_BOUNDED_CHECK` | 0.704 | 0 | `M_MINUS_MULTIPLICITY_CHECK` | 0.800 | 0 |
| `F0_PARENT_FEDERATION` | **1.000** | 0 | `C_ALWAYS_ACCEPT` | 0.200 | **100** |
| `C_ALWAYS_BLOCK` | 0.200 | 0 | `C_RANDOM_DISPOSITION` | 0.128 | 18 |

Shuffled-label null at this size: 0.288. Liveness control: 100 / 31 / 25 / 25
ablation-versus-parent disagreements.

`P4_SMALL_SCOPE_BOUNDED_CHECK` scores 0.88 on `minimal_counterexample` at this
size, not 0.00: the registered family predicate is that the minimum countermodel
is *strictly deeper than the shallowest model of the hypotheses*, and most such
instances have their obstruction first appear at size 2, inside P4's scope. The
family is a genuine depth family, but its depth is usually one step, not two.
This is recorded here rather than left to be discovered in the protected
analysis.

### 5.3 Reading (development only; nothing here is protected evidence)

No single parent reaches the endpoint. The exhaustive model searcher decides
every rejection exactly and cannot accept, because exhausting a space is not a
proof and the protocol's hard gate refuses a formal claim without a witness. The
derivation searcher accepts exactly and cannot reject, because a prover produces
no countermodels. The small-scope check is exhaustive inside its scope and blind
above it. The inductive baseline is defeated by the decoy family by
construction and, where it does survive witness validation, still cannot tell a
single obstruction from two or a shallow countermodel from a minimal one (§3b);
the frozen lesson table is defeated everywhere. Their
pre-registered federation is exact, and the ORION mechanic is decision-identical
to it.

If this holds on the protected split, FM60's content is an attribution — *which*
parent family owns *which* half of "find the obstruction before you accept the
claim" — plus the finding that ORION's obstruction-discovery loop for bounded
conjectures is the composition of two mature parents and nothing more.

Ablations behave as their omissions predict, and each collapses exactly the
family its omission names: removing the obstruction search collapses every
reject family and leaves only the acceptances; removing the proof stage collapses
exactly `no_obstruction`; removing minimality escalation collapses exactly
`minimal_counterexample` (and the part of `misleading_surface_support` whose
obstruction is deep); removing the multiplicity check collapses exactly
`multiple_obstruction`. These are properties of the typed composition and are
load-bearing for `F0` exactly as much as for `M`.

Generator rejections (development): 424 across 15 accepted instances,
overwhelmingly in `misleading_surface_support` (377), where a randomly drawn
conjecture rarely has both a confirming ratio ≥ 0.88 and at most 6 countermodels
in the whole space. Rejections are counted per family and published in the
results file. At protected size the same-size probe rejected 2,710.

## 6. Estimated protected-run cost

125 instances × 14 arms, plus the independent cross-check on every instance,
deterministic and single core: the same-size probe completed generation,
dispatch, cross-check, scoring and gates in **1.17 s** wall. Budget: 1
CPU-minute. Runs on the Mac; no CI on the Mac mini, and no cluster time is
needed.

The cost flag on development is `COST_ADVANTAGE_PARENT` (F0 0.97 ms versus M
5.62 ms across the split): `M`'s local-repair exploration visits far more
structures than the parent's set algebra over a precomputed truth table. It is
reported and routes nothing.

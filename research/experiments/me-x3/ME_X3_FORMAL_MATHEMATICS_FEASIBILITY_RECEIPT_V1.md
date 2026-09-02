# ME-X3 — Formal-verification feasibility receipt V1

**State date:** 2026-09-02
**Question this receipt answers:** can ME-X3 be run with a real proof checker, and
if not with Lean + Mathlib, then with what, and at what stated cost to scope?

## 1. What was probed, and what was found

All probes ran on LUNARC (`cosmos2.int.lunarc`) through the Mac's `lun` relay; the
Mac itself has ~5 GB free and was never a candidate host for a toolchain.

| probe | command | result |
|---|---|---|
| Lean toolchain present | `ls ~/.elan/toolchains` | `leanprover--lean4---v4.33.1` |
| Lean version | `lean --version` | `4.33.1, x86_64-unknown-linux-gnu, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6, Release` |
| elan | `elan --version` | `4.2.3 (b6cec7e10 2026-06-08)` |
| module system | `module spider lean` | no Lean module; the elan install is the only route |
| Mathlib present | `ls -d …/*mathlib*` (home and `/projects/hep/fs9/users/scyiu`) | **absent** |
| disk | `df -h /projects/hep/fs9`, `df -h ~` | 138 T and 135 T available; no quota limit reported |
| cores / memory | `nproc`, `free -g` | 96 cores, 502 G |
| network | `curl` to `raw.githubusercontent.com`, `release.lean-lang.org` | `200`, `200` (a Mathlib fetch would be possible) |
| independent re-checker | `leanchecker Ok` over an emitted `.olean` | exit `0` |
| per-file cost | 3 files, warm | ~1 s each, on `fs9` and on node-local disk alike |

So Lean 4 is available and usable **today**, without an install, and Mathlib is
absent but fetchable. The binding decision is therefore not "can we get Lean" but
"should this study use Mathlib".

## 2. Decision: Lean 4 core, no Mathlib — and why that is not a concession

**Mathlib is excluded because an unbounded library destroys oracle exactness.**

ME-X3's whole content is the distinction between *proof validity* and
*specification fidelity*, adjudicated against a known answer. The known answer
here is a **minimum-escalation** verdict: the cheapest registered intervention
that actually settles the problem (§3 of the design). That verdict is computed by
exhaustive search over a finite intervention space, one level of which is
*retrieve an existing lemma from the library*. With a Mathlib-scale library that
level stops being computable — not merely expensive — and the oracle degrades
from exact to approximate. An approximate oracle is exactly what a study whose
headline is "the checker accepted the wrong theorem" cannot afford.

Two supporting reasons, neither of them load-bearing on its own:

- the protected corpus consists of freshly generated presentations with
  arbitrarily renamed operator symbols, about which Mathlib contains nothing, so
  the retrieval arm would gain no real lemmas from it;
- pinning a Mathlib commit adds a large, uncontrolled contamination surface to an
  experiment whose contamination controls are otherwise complete.

**What this costs, stated plainly.** This study establishes the validity/fidelity
separation, the minimum-escalation decision, the false-representation-change
control and the held-out reuse test **on a finite formal system with an
exhaustive oracle**. It does **not** establish how any controller behaves at
Mathlib scale, where no exhaustive oracle exists and where proof search is the
dominant cost. Any reading of ME-X3 as evidence about frontier Lean theorem
proving is a misreading, and the study's terminal says so.

## 3. What Lean is actually used for here

The primary proof-validity oracle is the exhaustive rewrite search in
`mex3_oracle.py`. Lean answers the obvious objection to that — *who checks the
checker?* — by re-checking the arms' accepted derivations as genuine proof terms.

The encoding matters. The object system is emitted as an **inductive
proposition**:

```lean
inductive Derives : Word → Word → Prop where
  | refl (w : Word) : Derives w w
  | trans {a b c : Word} : Derives a b → Derives b c → Derives a c
  | ax0f (p s : Word) : Derives (p ++ [s0, s1] ++ s) (p ++ [s2] ++ s)
  | ax0b (p s : Word) : Derives (p ++ [s2] ++ s) (p ++ [s0, s1] ++ s)
  …
```

and each derivation becomes an explicit term over those constructors. The kernel
therefore checks that every step *is* an instance of an axiom schema at some
prefix and suffix. The tempting alternative — defining a Boolean `stepOk` and
proving `chainOk path = true` by `rfl` — would only re-implement our own checker
inside Lean and have the kernel certify that *our function* returns `true`; it is
reflection wearing the costume of external verification, and it is deliberately
not used. `#print axioms thm` additionally certifies each term is free of `sorry`
and of classical axioms.

**Negative controls are scored as strictly as positive ones.** A corrupted
derivation must be rejected, and rejected *for the registered reason*: a type
mismatch on a `Derives` term. A file that fails to compile for any other reason —
a parse error, a name clash, a timeout — is recorded as `CANNOT_CHECK` for that
instance, never as a successful rejection. "It did not compile" is not evidence.

## 4. Cross-check performed on the development split

40 files (20 accepted derivations, 20 corrupted counterparts) emitted by
`mex3_lean.py build` and checked on LUNARC with Lean 4.33.1:

| expectation | n | verdict |
|---|---|---|
| accept | 20 | 20 × exit 0 with `'thm' does not depend on any axioms` |
| reject | 20 | 20 × exit 1 with `error: Type mismatch … Derives.ax…` |
| `CANNOT_CHECK` | — | 0 |
| disagreements with the exhaustive oracle | — | **0** |

**The first run of this cross-check found a negative control that was not one.**
An earlier corruption strategy substituted a word inside the chain; when that word
happened to appear only as a *destination*, the textual substitution matched
nothing, the emitted "bad" file was byte-identical to its good counterpart, and
Lean accepted it. The scorer reported `ACCEPTED_UNEXPECTEDLY` rather than passing
it, which is the point of scoring negative controls by outcome instead of by
intention. The emitter now corrupts a step's *stated destination* while keeping
its axiom justification, so the justification's type provably differs from the
stated type; and `build` re-reads the emitted text and refuses to ship a "bad"
file identical to its good counterpart. Both guards are exercised by the tests.

`leanchecker` independently re-checked an emitted `.olean` (exit 0), so the
certificate survives a re-check by a program that did not elaborate it.

## 5. Reproduction

```bash
python3 mex3_lean.py build --results results/ME_X3_<LABEL>_RESULTS_V1.json \
                           --custody results/ME_X3_<LABEL>_CUSTODY_V1.json --limit 40
# copy research/experiments/me-x3/lean to a host with Lean 4.33.1, then
python3 mex3_lean.py check --dir lean --lean "$HOME/.elan/bin/lean"
```

The Lean stage is deliberately **out of CI**: CI runners have no Lean toolchain
and a 10-minute budget. Its absence never blocks the study — the exhaustive
oracle stands on its own — and its receipt records partial coverage honestly when
it is not run.

## Terminal

```text
LEAN_AVAILABLE = TRUE
LEAN_VERSION = 4.33.1
MATHLIB_USED = FALSE
MATHLIB_EXCLUSION = ORACLE_EXACTNESS_NOT_RESOURCE_LIMIT
PROOF_VALIDITY_CHECK = INDUCTIVE_PROOF_TERM_NOT_REFLECTION
NEGATIVE_CONTROL_REQUIRES_REGISTERED_ERROR_SIGNATURE = TRUE
EXTERNAL_PROVER_GENERALITY_AT_MATHLIB_SCALE = OUT_OF_SCOPE
```

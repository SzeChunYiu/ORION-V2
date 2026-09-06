# KSO field-frontier theorems — batch 11 (K1–K3)

Date 2026-09-06. Eleventh one-day batch, fourth of the field-completion programme (ORION-V2 #353) over the
Machine Epistemics field frontier (`field_dynamics_v1/FRONTIER.md`), after batches 8 (H1–H4), 10 (J1–J3)
and 9 (I1–I4, merged as #365). Scope: three frontier rows — FDX-09 infinite structured lifecycle learning
(K1), FDX-10 endogenous representation discovery (K2), FDX-12 safe incremental language commitment (K3).
Each row is closed as PROVED on a finite fixture, bounded exactly (an impossibility with a witness), or
PARENT_SUFFICIENT / PARENT_OWNED with the executable rule and its falsifier. The FDX ids are kept; the
rows are NOT sealed. Theorem labels K1–K3 are batch labels.

Every item has an exact finite checker (`kso_field_frontier_batch11_exact.py`, stdlib only; every count an
integer, every expectation an exact `Fraction`; exit 0 / 1 / 2 with 2 = CANNOT_CHECK, exercised by
`--probe-cannot-check`), at least one planted hostile whose mutation is asserted applied and caught, and a
no-alarm control; `tests/unit/test_kso_field_frontier_batch11.py` pins every count. Checker run on
billy-old (Python 3.14): exit 0, wall 2.0 s, `"status": "ALL_HOLD"`, three `"OPEN"` rows and three
`"CANNOT_CHECK"` rows listed below; 8/8 new tests (2.4 s). All objects are re-implemented inside the
checker (projective dependency derivations over a category-level rule inventory with a memoised counting
chart and a brute-force tree enumerator, coupon-collector cover times by inclusion–exclusion, a size-ordered
term enumerator over a Boolean library, a finite-state generator with listener readings); nothing imports
`ocm`; nothing ran on the Mac.

NO NOVELTY OR SUPERIORITY CLAIM. Every learning-theoretic, description-length or safety fact used is a
named parent's; the contribution is the exact statement on the registered objects, the executable
falsifier, and the reading of what the OCM N1 grammar induction, the packed-forest chart parser and the N2
realiser can and cannot support. Rigour follows the batch-6 integration review: guaranteed statements only,
never an accusation from an observed answer; a bounded checker says CANNOT_CHECK, never a guess.

Notation. `H ← [d_1 … HEAD … d_k]` a phrase rule with head category `H` and dependents `d_i = rel:cat` in
surface order (the `ud_grammar.Rule` shape); `D_G(w)` the number of derivations of the category string `w`
under inventory `G`; `Cat(n)` the Catalan numbers 1, 1, 2, 5, 14, 42; `H_r` the harmonic number; `|V|` a
version space; `R(q)` the listener reading at generator state `q`; `ℓ*` the shortest accepting completion;
`d` the saturation depth of the reachable set; LIVE / DEAD / UNKNOWN the KS-T21 liveness.

## K1 · FDX-09 · infinite structured lifecycle learning: the category-level construction frontier

**Objects.** Category alphabet `{N, V, P}`. A rule is `(head, pattern)` with pattern items `HEAD` or
`rel:cat`; a *category-level* inventory reads a dependent slot `rel:cat` as "any completed phrase headed by
a token of category `cat`" — the relation label is chosen by the parent rule and the sub-phrase carries none
(the shape of `constructions_from_grammar`: `Slot(name, category, phrase=PHRASE_OF_UPOS[upos])`, the
relation read only by the template). A *derivation* of a category string `w` is a projective single-rooted
dependency tree over `w` plus one relation label per dependent such that every non-leaf head's labelled
pattern is a rule of the inventory; leaves need no rule. `D_G(w)` is counted exactly by a memoised chart
over `(span, head)` with side sequences of dependent blocks, and cross-checked by explicit enumeration of
every projective tree for strings of ≤ 5 tokens. The *attested-set learner* `L(S)` = the set of labelled
patterns exhibited by a demonstration set `S` (the `induce_grammar` shape; the M3 version space over ORDER
hypotheses collapses to exactly the attested orders). *Treebank* `T`: five demonstrations — `N V N P N` with
the PP attached to the verb (`obl`) and, separately, to the object noun (`nmod`); `N V N` labelled `obj` and,
separately, `obl`; `N V`. `G_T = L(T)` has 6 rules. *Saturated inventory* `G_sat` (14 rules): `V ← nsubj:N
HEAD obj:N (obl:N)^j`, `N ← HEAD (nmod:N)^j`, `N ← case:P HEAD (nmod:N)^j`, `j ≤ 4`. *Rule universe* `U`:
eight rules of arity ≤ 2 (class `2^U`, 255 non-empty inventories). *Unbounded family*: `N ← HEAD (conj:N)^j`.

**Theorem.** (i) *Exactness.* The chart count equals the brute-force count on 12 (string, inventory) pairs
(both inventories; `N V N`, `N V N P N`, `N V`, `N V N N`, `P N V N`, `N V P N`). (ii) *Attachment
saturation.* Under `G_sat`, `D(N V N (P N)^k) = Cat(k+1)` = 1, 2, 5, 14, 42 for `k = 0…4`. (iii) *The
treebank.* Every demonstration is a derivation of its own string (5/5); `D_{G_T}(N V N P N) = 3` (the `obl`
attachment, and the `nmod` attachment under either labelling `obj` / `obl` of the object noun),
`D_{G_T}(N V N) = 2` (two relation labellings, no attachment choice), `D_{G_T}(N V) = 1`. (iv) *Positive
monotonicity.* `G ⊆ G′ ⇒ D_G(w) ≤ D_{G′}(w)` (192/192 over every sub-inventory of `G_T` and every added
rule); of the 64 sub-inventories, 14 give `D(N V N P N) = 1`, all of them below any inventory attesting both
attachments — a unique parse is unreachable *from above* by positive demonstrations; revoking the `nmod`
rules and the bare `nsubj HEAD obl` rule (the C6 negative / membership channel) returns `D = 1`,
`INTERPRETED`. (v) *Identification in the limit.* For every `G ∈ 2^U`, on every positive text of `G`, `L`
equals `G` from the moment every rule has appeared and stays there (255/255; Gold 1967, finite class); the
characteristic sample is one demonstration per rule — 4 trees for `G_T` (the `obj`-labelled `N V N` tree is
redundant), lower bound `⌈|G| / max rules per tree⌉ = 2`. (vi) *Sample cost.* With one rule per
demonstration drawn from a distribution `π` over `r` rules the expected cover time is
`Σ_{∅≠S} (−1)^{|S|+1} / π(S)`: `r·H_r = 761/35 ≈ 21.7` for uniform `r = 8`, ≈ 38.9 for Zipf `π_i ∝ 1/i`, never
below `r`. (vii) *Superfinite family.* On the text of unbounded arity the learner's conjecture changes at
arities 1…6 and never converges (G9 restated on the conjunction family). (viii) *Ranking licenses nothing.*
Frequency scores the two attachments of `N V N P N` 9 : 3 (the `obl` demonstration seen three times); the
honest verdict is `AMBIGUOUS`; when the gold reading is the rarer `nmod` the top-1 commit is wrong. Used as
the *unpacking order* the same ranking changes no verdict. (ix) *Packing.* A completed-node key that
contains the keys of the packed sub-phrases stores one node per derivation: 4, 10, 22, 50, 125 nodes for
`k = 0…4` under `G_sat` against 4, 9, 16, 25, 36 for a `(start, end, head category)` key.

**Proof.** (i) enumeration. (ii) each `P N` phrase attaches to the verb or to any noun to its left that is
not separated from it by a phrase already closed — the projective attachment sequences of `k` right
modifiers to a `V N` spine are counted by `Cat(k+1)` (Church–Patil 1982 for the PP-attachment case); the
saturated inventory admits every arity and one label per site, so each attachment is one derivation.
(iii) inspection of the three decompositions of the right side of `V`: two blocks `[N][P N]` under the
arity-2 rule, or one block `[N P N]` headed by the object noun under either arity-1 rule. (iv) a derivation
under `G` is a derivation under `G′`; the learner adds rules and never removes them; the 14 witnesses are
the sub-inventories containing exactly one of the competing rule sets. (v) `L` is monotone and bounded
above by `G` on a text of `G`; after the characteristic sample it equals `G`; set cover over the pool for the
minimal size; each demonstration exhibits ≤ 2 rules on this fixture. (vi) inclusion–exclusion over the
event "rule `i` unseen after `t` draws"; the uniform closed form is the coupon-collector identity. (vii) the
attested set after arity `j` is `L_j`, a proper subset of the target (Gold 1967, Angluin 1980 tell-tales).
(viii) a derivation's warrant is the meet of its rules' warrants; all rules LIVE gives every derivation LIVE;
a score is a function outside the lattice (batch-4 D3) and changes no liveness. (ix) the identity key is
injective on derivations of a span; the span-type key has at most `n(n+1)/2 · 3` values. ∎

**Hostiles.** `mutant_generalise_family_orders` (every permutation of an attested family admitted — the
"AMBIGUOUS_ORDER families read as all orders" hostile) overshoots the target on 254 of 255 inventories and no
positive text ever corrects it (254/254; no negative evidence). `mutant_rank_licenses_top1` (the
`chart.mutant_first_derivation_only` shape) commits the wrong derivation on the gold-is-rarer witness.
The derivation-identity packing key is exhibited as the exponential count of (ix). **No-alarm:** an
inventory attesting one attachment gives `INTERPRETED`; the `N V` demonstration alone parses `N V` uniquely;
ranking as unpacking order changes no verdict.

**Status.** PARENT_OWNED mathematics: identification of finite classes from positive data (Gold 1967),
tell-tale sets and the superfinite obstruction (Angluin 1980), the coupon-collector cover time,
Catalan-counted attachment ambiguity (Church–Patil 1982 — candidate, cited not verified here), version
spaces (Mitchell 1982; batch-2 B2/B3), batch-7 G9 (the SHRG/CCG half: positive-only over a superfinite class
identifies nothing), batch-4 D6 (≡_L refines behaviour). PROVED on the fixture: the exact statement of
*what the N1 learner identifies* — the finite class of category-level inventories of bounded arity, at cost
one demonstration per rule — and *the exact obstruction for the class N1 uses*: the category-level
projection forgets exactly the information that decides attachment and relation (lexical heads, the
sub-phrase's own relation), so once two attachments or two labellings are attested the derivation count is
≥ 2 and no positive demonstration lowers it (EXACTLY_BOUNDED); only a negative / membership channel (C6)
or revocation reaches a unique parse. This is the theorem behind the UD-EWT receipt
(`research/ocm-n1/N1_UD_INDUCTION_V1.json`, ORION-OCM `e0cd297`): 12 544 training sentences, 19 642
memorised rules in 17 171 families (15 343 single-order, 1 828 AMBIGUOUS_ORDER, 14 967 rules attested once);
20 570 constructions in the chart run; dev 1 577 sentences reaching the chart — UNKNOWN_LEXEME 1 035,
UNKNOWN_CONSTRUCTION 73, CHART_CAP_CANNOT_CHECK 437, AMBIGUOUS 32 (192 derivations, gold among the unpacked
7), INTERPRETED 0; test 1 760 — 1 141 / 112 / 469 / 38 (250, gold 4) / 0. The reading K1 licenses: every
sentence that reaches a clause-level derivation has ≥ 2 of them (an inventory of 20 570 category-level rules
attests both `obj:NOUN` and `obl:NOUN`, both `nmod` and `obl` attachments), so `INTERPRETED` is not a
possible verdict of this inventory on such strings; the cap is the (ix) consequence of identity keying. The
reading K1 does *not* license: any statement about which derivation is right, or that the inventory has
converged (OPEN / CANNOT_CHECK below). **OPEN:** identification of a *lexicalised* (bilexical) inventory from
positive demonstrations — finite for a finite lexicon, characteristic sample scaling with lexical pairs; the
exact UD-EWT sample cost. **CANNOT_CHECK:** convergence of the UD-EWT inventory (the singleton fraction is a
Good–Turing reading, not a certificate); that the real cap is reached for the reason of (ix) — the checker
re-implements the key shape, it does not run the OCM code.

## K2 · FDX-10 · endogenous representation discovery: search information for a discovered versus a given operator

**Objects.** Boolean functions of two inputs (16 tables). Base library `Λ₀ = {x, y, NOT, AND, OR}`; terms
are trees with size = node count, enumerated in size order with a fixed tie-break (9 168 terms of size ≤ 8;
2, 2, 10, 26, 114, 402, 1 722, 6 890 by size). *Evidence* is a partial table (81 patterns over 4 rows);
`V(E)` the version space. *Search position* `N(f)` = the number of terms examined by size-ordered search up
to the earliest term consistent with the evidence (the finite Levin-search count). A *discovered operator* is a
new binary primitive with a table `a`; its *definition cost* is its minimal base size. The *adoption rule* is
the DreamCoder-shape compression objective on a registered task set `T`: `gain(a, T) = Σ_{t∈T} (min_Λ₀(t) −
min_{Λ₀+a}(t)) − cost(a)`, adopt iff `> 0`. Candidates: the 12 non-constant non-projection tables. Task set
family: subsets of `{XOR, EQV, NAND, x∧¬y}`. *Memorising abstraction*: the lookup table of the evidence
itself, priced either as one symbol (hostile) or as its table (honest, `2·|E|`).

**Theorem.** (i) *Minimal sizes.* XOR and EQV need 8 nodes in `Λ₀`; with XOR as an operator 3 and 4; three
functions shorten (XOR, EQV, FALSE), none lengthens. (ii) *Representation invariance.* For each of the 81
evidence patterns the set of tables of consistent terms is `V(E)` under `Λ₀` and under `Λ₀ + XOR` alike
(81/81), `|V(E)| = 2^{unseen rows}`, so the identification bits `⌈log2 |V|⌉` do not depend on the library and
every unseen row is undetermined by every library (104/104). (iii) *Search moves both ways.* `N(XOR)` falls
from 2 936 to 16 and `N(EQV)` from 6 990 to 38; seven functions' positions rise (a larger library has more
terms per size), two fall; every position is within the finite Levin bound `N(f) ≤ #terms of size ≤
min(f)` (32/32). (iv) *Adoption threshold.* XOR (cost 8) is adopted on exactly the 4 task sets containing
both XOR and EQV (gain 1; EQV ties as an operator), and on no other (a single XOR task: gain −2). (v)
*Discovery information.* Naming the adopted operator among the candidates costs `⌈log2 12⌉ = 4` bits and
26 032 evaluated terms per candidate library; a given operator costs 0 of both. (vi) *Self-certification
hostile.* The one-symbol memorising abstraction is adopted on 39 of the 79 partial tables and claims the
unseen row; honestly priced it is adopted on 0, because every partial table has a consistent base function
of size ≤ 4. (vii) *Extension, not definition.* Eight syntactically distinct minimal definitions of XOR exist
(e.g. `AND(NOT(AND(x,y)),OR(x,y))`); no evidence distinguishes them.

**Proof.** (i) enumeration. (ii) a term's table is a behaviour; consistency is a property of the table;
the enumeration reaches every table by size 8 under both libraries. (iii) the enumeration is total and
size-ordered, so the earliest consistent term appears no later than the end of its size class. (iv)–(v)
arithmetic on the minimal-size tables; `log2` of the candidate count. (vi) the version space of a partial
table with `u` unseen rows has `2^u` members differing on those rows; the two functions of size 8 differ in
more than one row from each other, so every pair `{f, f ⊕ row}` has a member of size ≤ 4. (vii) enumeration
of the size-8 class. ∎

**Hostiles.** `mutant_memorising_abstraction_gain` (a lookup table priced as one symbol) — 39 adoptions, each
followed by a claim on an undetermined row; caught against the honest 0. **No-alarm:** the extended library
has exactly the 16 behaviours; giving XOR changes no version space (81/81).

**Status.** PARENT_OWNED: size-ordered universal search and its time bound (Levin 1973; Solomonoff 1964),
MDL (Rissanen 1978), library learning by compression (DreamCoder — Ellis et al. 2021; candidate, cited not
verified here), the invariance theorem of Kolmogorov complexity (representation changes description length
by a constant, never information content), the FDX-14 / J3 fact that identification bits are a property of
the class. PROVED exact corollaries on the fixture: *representation moves search cost — both ways — and
description length; it moves no identification bit and determines no unseen row* (EXACTLY_BOUNDED); an
abstraction adopted by compression alone is self-certification unless the gain is priced honestly and the
claim on unseen inputs stays UNKNOWN until an external evaluator (C6 registered outcome) supplies it; a
discovered representation is identified only up to its extension (D6's STRUCTURAL_NONIDENTIFIABILITY for
definitions). What FRONTIER asked for — "count search and evaluation information" — is the pair (selection
bits, evaluated terms) recorded per candidate. **OPEN:** the proposal policy over an infinite abstraction
space (which candidates to price); parent-owned search policy. **CANNOT_CHECK:** that a real proposed
abstraction's evaluator is registered — a governance premise (batch-5 E4 `SelfChangeProposal`), not a
property the checker can see.

## K3 · FDX-12 · safe incremental language commitment: the N2 realiser's theorem

**Objects.** A finite-state generator: 20 states, tokens `the, horse, raced, past, barn, fell, did, fall,
not, slept, .`, six accepting strings (`the horse raced past the barn .`, `… barn fell .`, `the horse did
fall .`, `… did not fall .`, `… did fall not .`, `the horse slept .`). A *listener reading* `R(q)` per state:
the claims a streaming reader commits to at that prefix (`horse_raced` after `the horse raced`;
`horse_fell, raced_past_barn_relative` after `… barn fell`; `horse_fell` after `did fall`; `not_horse_fell`
after `not fall` or `fall not`; `horse_slept`). Each claim carries an evidence id; a revoked set and an
authorised set are external inputs. *Exact criterion* (F6.1 on this generator): a prefix at state `q` may be
emitted iff (1) an accepting state is reachable, (2) `R(q) ⊆ R(q′)` for every reachable accepting `q′`, (3)
every claim of `R(q)` is LIVE and authorised. *Bounded checker* `bounded(q, k)`: UNSAFE on a violating
accepting state within `k` (sound); SAFE when the gates hold, an accepting state is within `k`, and either
`R(q) = ∅` or the reachable set is saturated within `k`; else CANNOT_CHECK. `ℓ*(q)` the shortest accepting
completion; `d(q)` the saturation depth (largest shortest distance to a reachable state). *Streaming
channel*: the criterion is checked at every intermediate prefix (F6's transactional chunk); *atomic
channel*: the final reading alone is checked (the `Realization.checked` shape).

**Theorem.** (i) *Exact criterion.* Five states are UNSAFE: the garden-path prefix `the horse raced` and
its extensions to `… barn` (the completion `… barn fell .` retracts `horse_raced`;
`RETRACTED_BY_COMPLETION:9`) and the late-negation prefix `the horse did fall` (`… fall not .`;
`RETRACTED_BY_COMPLETION:19`); every accepting state is SAFE (6/6) and reaching it does not make the
prefixes before it safe; empty-content prefixes with a completion are SAFE. (ii) *Two completeness
thresholds.* A decisive bounded verdict never contradicts the exact one (147 agreements, 33 CANNOT_CHECK over
20 states × `k = 0…8`); SAFE is decisive exactly at `k ≥ ℓ*` when `R(q) = ∅` and at `k ≥ max(ℓ*, d)`
otherwise (state 2: `ℓ* = 2, d = 6` → SAFE at 2; state 16: `ℓ* = d = 1`); UNSAFE is decisive exactly at the
distance of the nearest violating accepting state (state 3: violation at 5, `ℓ* = 4`, CANNOT_CHECK at `k ≤ 4`).
(iii) *Channel is a premise.* The atomic check passes all 6 accepted strings; the streaming check passes 2
and refuses 4 at their unsafe prefix (positions 2, 2, 3, 3). (iv) *Revocation mid-stream.* Revoking the
evidence of a committed claim refuses the next token (`DEAD:horse_slept`), keeps the emitted history and the
committed set; an unauthorised claim is refused before its token. (v) *Monotone branch.* Where readings
only grow along edges every prefix with a completion is SAFE (4/4) and the bounded checker decides it at the
thresholds of (ii).

**Proof.** (i) reachability; (2) fails iff some accepting reachable reading lacks a committed claim — the
F6.1 necessity argument. (ii) soundness of UNSAFE: a violating final within `k` is a violating final;
soundness of SAFE: with `R(q) = ∅` condition (2) is vacuous and (1) is witnessed by any final within `k`
(G3's existential threshold `ℓ*`); with `R(q) ≠ ∅`, saturation means every reachable state has been
examined, so the universal condition is decided; below the thresholds a longer completion may violate or
none may have been seen, and the checker cannot know which — hence CANNOT_CHECK, never a guess. (iii)
the atomic check is F6.3's controlled generation: the generator has bound itself to one completion, so the
completion set is a singleton and (2) is trivial; the streaming reader sees the prefix reading before the
binding — F6 requires the criterion at each intermediate prefix. (iv) F6.2 monotonicity of `S`; a dead
claim in `S` fails gate (3) for every extension. (v) monotone readings satisfy (2) for every completion. ∎

**Hostiles.** `mutant_existential_lookahead` (SAFE iff *some* accepting completion preserves the reading —
F6.3's insufficiency) passes all 5 unsafe states. `mutant_bounded_pass_is_safe` (CANNOT_CHECK read as SAFE)
commits the garden path at `k ≤ 4` and the other unsafe prefixes below their violation distance (16 cases).
`mutant_forget_history` (drops dead claims from `S` and reads the state as if nothing were revoked) emits
through a revocation with an empty committed set; the honest stream refuses at the token. **No-alarm:** the
monotone branch; the atomic channel on its own terms passes every accepted string.

**Status.** PARENT_SUFFICIENT, as FRONTIER predicted for the finite case: the criterion is a safety
property in the sense of Alpern–Schneider 1985 (an irreversible violation, not the absence of a good
extension); F6 (`ME_FRONTIER_F6_SAFE_PREFIX_V1.md`, sealed) proved it on enumerated inventories; batch-7 G3
proved the existential half's completeness threshold `ℓ*` for context-free inventories; this batch adds the
universal half's threshold `d` and the exact decision by reachability on the finite-state class — the class
in which the N2 realiser's inventory lives today (`en:transitive`, `en:passive`, `en:negation-transitive`,
`en:yesno-transitive`, `en:intransitive`: five surface templates). The decidable sub-classes, with exact
checkers here: **finite-state acceptability with finite readings** (reachability, `O(|Q|²)`); **bounded
lookahead** with the two thresholds `(ℓ*, d)` as its completeness certificate. Stated, PARENT_OWNED, not
checked: context-free acceptability with a *regular* reading is decidable through the Bar-Hillel product
(the violating completions form a CFL ∩ REG, whose emptiness is decidable — Bar-Hillel–Perles–Shamir 1961);
with a *context-free* reading prefix safety is the emptiness of an intersection of two CFLs — undecidable
(G3; no finite fixture exhibits it). **CANNOT_CHECK:** the listener's reading table `J` for natural language
(F6: empirical, separate); the fixture readings are constructed controls, not measurements of garden paths.

## Consequences for the OCM build — runtime obligations H1–H8 (read-only observations on ORION-OCM `origin/main` at `e0cd297`, 2026-09-06; nothing touched)

Each H-item names the runtime location the theorem would change; none is a claim about an N1 or M12 result.

* **H1 (K1 ii–iv) — the category-level slot is the ambiguity; record it as such.**
  `src/ocm/learning/language/ud_grammar.py::constructions_from_grammar` (line 234) builds every dependent as
  `Slot(name, UD.UPOS_TO_CATEGORY[upos], phrase=PHRASE_OF_UPOS.get(upos, "NP"))` — a slot constrained by
  phrase type only; the relation (line 235, `roles`) is read by the template, never by the matcher. K1 (ii)–(iv)
  say this inventory has `D ≥ 2` on every string with two attested attachments or labellings and that no
  further demonstration lowers it. Obligation: the identifiability receipt of an induced inventory records
  the *class* it identifies (category-level, arity bound) and the consequence `UNIQUE_PARSE_UNREACHABLE_FROM_
  POSITIVE_DATA` for strings whose category shape has ≥ 2 attested decompositions; a unique reading needs a
  registered negative / membership channel (`ocm.language.acquisition`, batch-7 G9's receipt) or a finer
  class (bilexical slots, OPEN).
* **H2 (K1 v–vii) — `Grammar.learned` is an identification receipt only for bounded arity.**
  `ud_grammar.py::Grammar.learned` (lines 117–124) marks a family LEARNED when one order survives. K1 (v)
  licenses "identified in the limit" for the finite class of bounded arity after the characteristic sample;
  (vii) says the unbounded-arity families never converge. Obligation: the receipt carries the arity bound
  and the coverage state (rules attested once — 14 967 of 19 642 on UD-EWT — mark the inventory
  `NOT_CONVERGED`, a Good–Turing reading, not a certificate); a family with a single attested order at count
  1 is LEARNED-at-`n = 1`, never a construction with a lifecycle warrant past its one demonstration (D6).
* **H3 (K1 viii) — the verdict is the count; a ranking orders the unpack.**
  `src/ocm/language/chart.py` line 213 (`"INTERPRETED" if total == 1 else "AMBIGUOUS"`) is already the K1
  (viii) rule, and `mutant_first_derivation_only` (line 219) is its planted hostile. Obligation: keep it; any
  clarification policy that scores derivations (`max_unpack`, line 86) orders the unpacked meanings and
  writes the score outside the lattice (batch-4 D3); `AMBIGUOUS_WITH_GOLD_AMONG_UNPACKED` (7 of 32 on dev) is
  a coverage measure of the unpack order, not evidence for a reading.
* **H4 (K1 ix) — pack by span and type, not by sub-derivation identity.**
  `chart.py::_lex_key` (line 67) appends `(k, "P", v.key)` for every packed sub-phrase and `add` (line 112)
  puts that key into the item key, so `complete` (line 148, `pk = (ci, lk)`) creates one `Packed` node per
  distinct sub-derivation: the forest stores one node per derivation (K1 ix: 125 vs 36 at `k = 4`), and the
  item count grows like the derivation count — the `ChartCap` (line 117; 437 / 469 CANNOT_CHECK on dev /
  test at `max_items = 300 000`) is the predicted consequence. Obligation: key completed nodes by `(start,
  end, produces, lexical readings of the span)`, keep exact counts by summation, build one representative
  meaning per node lazily; the count stays exact and the item bound becomes polynomial in the token count.
  CANNOT_CHECK here that this is the *only* cause of the observed cap.
* **H5 (K2 ii, v) — a representation introduction carries a search-and-evaluation receipt.**
  `ud_grammar.py` line 36 calls `register_relations("ROLE:recipient", "ROLE:oblique", …)` at import: new
  relation types enter the meaning vocabulary by fiat, with no receipt. K2 (v) fixes what the receipt holds:
  the candidate space (selection bits), the evaluated terms per candidate, the adoption gain, and the
  external evaluator id; a *given* vocabulary records 0 bits and names its source. `src/ocm/kso/admission.py::
  admit` (line 81, `UNREGISTERED_ATOM_TYPE`) refuses unregistered types but prices no registration.
* **H6 (K2 iv, vi) — adoption by compression is a proposal, never a licence.**
  A library change (a new operator, node type or relation) is a `SelfChangeProposal` (batch-5 E4;
  `selfmodel/govern`, `kso/jump.assess_jump`) whose gain is priced honestly (definition cost = its
  description in the base library, a table costs its table) and whose claims on unseen inputs stay UNKNOWN
  until a C6 registered outcome supplies them; K2 (vi)'s one-symbol memorising abstraction is the hostile
  the gate must catch (39 false adoptions vs 0).
* **H7 (K3 i–iii) — the realiser's check certifies the final reading; a streaming channel needs the
  prefix criterion.** `src/ocm/language/realize.py::realize` (lines 121–126) re-interprets the whole
  candidate surface and sets `Realization.checked` (line 38) iff the reverse reading is INTERPRETED with the
  intended digest — the atomic channel of K3 (iii); it holds no prefix state, declares no channel, and
  cannot refuse mid-emission. Obligation: declare the channel in the realisation receipt (`ATOMIC` — the
  surface is delivered whole — or `STREAMING`); under `STREAMING` run the K3 exact criterion per prefix
  against the inventory's completion automaton (finite-state today: five templates), returning SAFE / UNSAFE
  / CANNOT_CHECK with the thresholds `(ℓ*, d)` as the completeness certificate; never approximate a
  context-free inventory by a DFA (G3) and never read a bounded pass as SAFE.
* **H8 (K3 iv) — revocation during emission refuses the next token and keeps the history.**
  `realize.py` takes `revoked` once (line 85) and `src/ocm/runtime/solve.py::commitment_gate` commits on the
  outcome (batch-7 G3); neither re-reads liveness between tokens. Obligation: the streaming path re-checks
  gate (3) at every token, refuses on a DEAD committed claim with the claim named, and appends — never
  subtracts — the emitted history (F6.2); a correction is a new typed act.

```text
K1  FDX-09  PARENT_OWNED (Gold finite classes, Angluin tell-tales, coupon collector, Catalan counting); PROVED: chart = brute force 12/12; Cat(k+1) = 1 2 5 14 42; treebank 3 / 2 / 1; positive monotone 192/192, unique parse 14/64 all below (EXACTLY_BOUNDED), revocation → 1; identified 255/255, characteristic sample 4 (bound 2); cover time 761/35 uniform, ≈ 38.9 Zipf; unbounded arity never converges 6/6; ranking 9:3 licenses nothing; packing 125 vs 36
K2  FDX-10  PARENT_OWNED (Solomonoff/Levin, MDL, DreamCoder-class, Kolmogorov invariance); PROVED: version spaces invariant 81/81, unseen rows 104/104 (EXACTLY_BOUNDED); XOR 2 936 → 16, EQV 6 990 → 38, 7 rise / 2 fall, Levin bound 32/32; adoption only with XOR + EQV (4/15, gain 1); discovery 4 bits + 26 032 terms vs 0; memorising abstraction 39 vs 0; 8 minimal XOR definitions
K3  FDX-12  PARENT_SUFFICIENT (Alpern–Schneider, F6, G3, Bar-Hillel); PROVED: 5 UNSAFE states by reachability; bounded exact iff k ≥ ℓ* / max(ℓ*, d) / nearest violation (147 + 33); atomic 6 vs streaming 2; revocation refuses, history kept; CF readings undecidable (cited)
OPEN: lexicalised inventories and the UD-EWT sample cost; abstraction proposal policy; CF × regular product checker
CANNOT_CHECK: UD-EWT convergence and the cap's cause; evaluator registration of a real abstraction; natural-language reading table
NOVELTY NOT_ESTABLISHED
```

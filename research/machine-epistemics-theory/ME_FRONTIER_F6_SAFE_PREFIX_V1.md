# Frontier F6 — finite safe semantic prefix criterion

`MEG-27 = SAFE_PREFIX_CRITERION` on **closed, finite, registered semantics**.
`GENERAL_NOVELTY = NOT_ESTABLISHED`; `OPEN_LANGUAGE_AND_CODEC_COMPLETENESS = CANNOT_CHECK`.
This is a new reference theorem/checker for issue #329 F6. It does not rewrite
batch-3 C3 or batch-5 R2, whose existential acceptable-completion results remain
valid within their stated models.

## Registered object and information boundary

Before checking outcomes, freeze a finite inventory `L` **defined by explicit
enumeration**, an epoch, and a typed semantic representation. Each completion
has a unique identity, token string, and finite meaning set `M(c)`. A claim is
the exact tuple `(proposition, polarity, quantifier, modality, citation)`. The
reference checker performs equality of these already-canonical tuples; it
neither parses natural language nor proves an unverified codec canonical.

Also freeze `J(p)`, the semantic content irreversibly expressed by each prefix
of each registered completion. This interpretation table is a separate premise:
it must cover every prefix, assign no claim to the empty prefix, and agree with
each full completion's meaning. A caller cannot hide an asserted prefix by
passing an empty proposed claim set. Full surfaces with conflicting meanings
are unresolved and cannot be checked by this finite interface.

For a prefix `p`, the compatible completion set is

`C(p) = {c∈L : tokens(c) begins with p}`.

The residual state is `(digest(L,J,epoch,semantics), p, S)`, where `S` is the
union of all `J(q)` for prefixes `q` already emitted. The digest is checked
against the current inventory. It binds content; it does not supply external
authority for correct labels or completeness of an open language. Current
warrant `W` maps claims to `LIVE/DEAD/UNKNOWN`, and `A` is the set of claims
authorized for commitment. Both are external inputs, never written by the
prefix checker. Unknown warrant input is `CANNOT_CHECK`.

## F6.1 — exact finite robust-commitment criterion

After a proposed token emission reaches `p'`, let `S'=S∪J(p')`. Irreversible
semantic commitment is safe against every registered compatible completion iff

1. `C(p')` is nonempty;
2. `S' ⊆ ⋂_{c∈C(p')} M(c)`;
3. every `s∈S'` is currently `LIVE` and `s∈A`.

Here “safe” means precisely that no compatible final meaning changes/removes
the committed content and that each commitment has current warrant/authority.
It does not require every final meaning to be equal: unresolved future content
may vary. The empty completion set is rejected, avoiding vacuous permission.

**Proof.** Sufficiency: set inclusion puts every committed claim in every
compatible final meaning; condition 3 supplies the two independent epistemic
gates. Necessity: if inclusion fails, there exists a committed claim and a
compatible completion lacking it, which witnesses unsafe variation. If either
epistemic gate fails, that claim is not a warranted authorized commitment.
If no completion exists, the prefix cannot be completed within the registered
protocol. These exhaust the definition. ∎

For a token chunk, the criterion must hold at **each intermediate prefix**, not
only its final endpoint: a streaming reader can observe the earlier claim.
The checker therefore validates the whole chunk transactionally and returns
the original residual state on rejection.

## F6.2 — monotone commitment and the correction boundary

If a safe prefix extends without changing inventory or epoch, its compatible
completion set can only shrink. Previously committed claims remain present in
the intersection on any nonempty remaining set. The checker accumulates
`S'=S∪J(p')`; it never subtracts an earlier commitment when later interpretation
changes. A resumed state must include the entire registered emitted history,
and every earlier prefix is replayed against the frozen completion inventory.
An imported endpoint cannot hide an earlier unsafe intermediate prefix.

**Proof.** Every continuation of an extended prefix is a continuation of its
shorter prefix. Inclusion in all elements of a set implies inclusion in all
elements of any subset. Monotonicity of `S` is union monotonicity. ∎

The theorem is conditional on fixed semantics and current epistemic inputs.
The reference residual state is not an authenticated historical warrant
receipt: it cannot prove that authorization existed at a past wall-clock time.
That historical claim requires the external warrant/event ledger.
After evidence revocation, continued commitment is blocked and reopening is
required; already-emitted history remains. A later correction can be a new,
explicit act, but cannot make an earlier unsafe assertion retrospectively safe.
The checker handles an imported inconsistent history as `HISTORY_CONFLICT` or
`CANNOT_CHECK`, not silent repair. It does not promise eventual completion.

## F6.3 — why existential lookahead is insufficient

Let `C(p)={c1,c2}`, with an already-expressed claim `a∈M(c1)` but `a∉M(c2)`.
Both completions are in the same visible finite protocol. There exists an
acceptable completion preserving `a`, so an existential SAT test can pass;
robust irreversible preservation fails on `c2`. Thus batch-3 C3/batch-5 R2
completion-existence checks cannot alone establish F6.1's universal guarantee.

If a generator first **binds and constrains its future choices** to `c1`, that
changes the registered completion set and can justify a weaker controlled
generation guarantee. It is not evidence that the original unconstrained set
preserved `a`. The strongest safety-game parent distinguishes existential
controller moves from universal environment continuations in exactly this way.

Hedging and abstention need not become assertions. A registered abstention may
have empty commitment content; a hedge is its own typed, warranted statement
of uncertainty with modality `POSSIBLE`. An unknown assertion does not become
LIVE by merely changing its displayed marker.

## Parent reconstruction and subtraction

[Alpern and Schneider, Defining Liveness (1985), §§2–3](https://www.cs.cornell.edu/fbs/publications/DefLiveness.pdf)
was read from the author's primary repository on 2026-09-05. It distinguishes
an irreversible safety violation from existence of a future satisfactory
extension. The present finite universal-continuation intersection is a direct
safety/invariance application. Exhaustive residual-language filtering is the
finite parsing/monitoring parent; batch-5 R2 already reconstructs regular
reachability for its different existential endpoint. No new language-learning,
parsing or safety-game theorem is claimed. No unrestricted natural-language
canonicalization, semantic prefix table, or completeness certificate is
established by these constructed examples.

## Reference mechanism, controls and resource scope

`meg_frontier_f6_safe_prefix_exact.py` validates immutable materialized
inventory/meaning inputs, all prefix rows, full-surface consistency and content
identity. It enumerates the **entire** registered completion inventory. An open
inventory, stale epoch/semantic identity, missing prefix row, absent warrant,
or exhausted completion-count budget returns `CANNOT_CHECK`; an established
empty residual language returns `NO_ADMISSIBLE_COMPLETION`. Neither is a proof
of truth or absence outside this protocol.

For `N` completions, maximum completion length `L`, `T` new tokens, existing
prefix length `P`, and `M` distinct claims in the registered semantics, straightforward residual
scanning including semantic history replay costs `O((P+T) N (L+M))` set/
token operations, plus full identity/table validation. The budget limits `N`,
not total time or bytes. A prefix trie and cached intersections could reduce
repeated scans, but would need the same content/epoch binding and exact parity.
No unmeasured runtime improvement is claimed here.

Hostile controls independently change the proposition (garden-path role
interpretation), polarity (late negation), quantifier, citation, correction and
modality. These are **typed constructed controls**, not empirical tests of
natural-language garden paths. Tests also check all 64 two-completion meaning/
prefix combinations over two claims against four authority subsets, safe
unchanged continuations, warranted hedge/abstention, revocation after emission,
history deletion, chunk bypass, family truncation and CLI 0/1/2. Python `-O`
cannot silently skip the assert-based witness checks.

Run:

```text
python research/machine-epistemics-theory/meg_frontier_f6_safe_prefix_exact.py
python -m pytest -q tests/unit/test_meg_frontier_f6_safe_prefix.py
```

## Terminal and reopen conditions

The finite semantic half reaches `SAFE_PREFIX_CRITERION`, with the strongest
parent sufficient. Applying it to OCM streaming still requires a registered
runtime meaning interface and parity; applying it to unrestricted language
requires independently established `L`, `J` and canonical semantic identity.
Those capabilities remain `CANNOT_CHECK` here. Reopen when the inventory,
semantic interpretation, epoch, emitted-history contract or control model
changes, or when a surviving counterexample violates the stated criterion.
F7's infinite-class lifecycle identification is a different question and
remains open; no finite-prefix proof closes it.

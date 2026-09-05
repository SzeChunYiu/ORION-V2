# Obligation-relative decisions and the memory–verification frontier

**Identity:** ME-DECISION-FRONTIER-V1, ORION-V2 #314. Written proofs over arbitrary finite registered families; exact finite calibration is reported separately. No novelty, empirical superiority, external authority, proof-assistant verification, or full-foundation-closure claim.

## 1. Scientific object and boundaries

A machine often needs enough justified information to make a particular decision, not a reconstruction of the entire world. This is the decision-region determination (DRD) object of Javdani et al. (2014), not an ORION invention. Their public model has hypotheses, deterministic tests, consistent hypothesis sets, and possibly overlapping regions on which a decision succeeds (§2, equations 1–2, pp. 431–432). Their optimization is Bayesian expected test cost. We reconstruct the exact finite **worst-case** counterpart and its interaction with durable-state compression and evidence revocation. The expected-cost approximation guarantee of HEC is NOT imported as a worst-case guarantee.

The signature here is

`M = (W, A, G, Q, o, c, contract, epoch, closure)`.

`W` is a finite nonempty set of possible worlds/histories; `A` is a finite set of terminal decision identifiers; `G(w) ⊆ A` is the externally specified set of acceptable decisions at world `w`; `Q` is a finite family of read-only tests; `o_q: W → O_q` is total and deterministic; and `c_q` is a strictly positive rational cost. Empty `G(w)` is permitted: it represents an unsatisfiable registered obligation, not permission to invent an answer. The contract, epoch and closure identifiers bind the tables.

A nonempty belief set `B ⊆ W` contains every world still possible under the admitted evidence. It is a set, not a posterior distribution. A query returns only `o_q(w*)` for the actual world `w*`. Its result is trusted *within the registered channel model*. Tables are public model descriptions; the actual world is unavailable to the planner. Policy synthesis may inspect all table entries, just as a finite-model planner inspects its transition model. Constructing that table, certifying its scope, and storing/searching it are NOT free.

### Load-bearing assumptions

The actual world lies in the admitted family; all retained observations are valid; query semantics/costs do not change during a policy; queries have no external effects; a repeated query gives the same observation; and all query choices are authorized and available whenever the policy selects them. Missing, noisy, inaccessible or drifting channels are NOT silently treated as negative observations. Such cases require a different model or `CANNOT_CHECK`.

`G(w)` is a decision contract, not a source of scientific truth. A decision identifier may denote an exact assertion, a risk-bounded recommendation with its own statistical contract, or another formally permitted result. This package neither turns marginal coverage into pointwise truth nor defines statistical warrant. Those semantics belong to #312/#313 and their strongest parents. An external effect still needs an independent, pre-action authority check; a policy object authorizes nothing.

Three failures must stay distinct:

* `OBSTRUCTION_WITNESSED`: the declared observation interface cannot guarantee an acceptable decision on this belief set; a finite witness exists.
* `BUDGET_INSUFFICIENT`: a solution exists, but its least worst-case test cost exceeds the supplied budget.
* `CANNOT_CHECK`: family closure is not bound, the exact instrument's size cap is exceeded, or a required assumption/tool cannot be checked.

An empty belief is `CONTRACT_ERROR`, not vacuous universal success. Its cause could be inconsistent evidence or model misspecification. The reference deliberately refuses to select an action from it.

## 2. DF-00 — maximal robust decision rule

Define `Safe(B) = ⋂_{w∈B} G(w)`. An immediate deterministic decision is correct for every possible actual world exactly when it belongs to `Safe(B)`. Therefore this is the **maximal** universally acceptable immediate-decision set.

**Proof.** Membership gives correctness in every world by intersection. If `a ∉ Safe(B)`, some `w∈B` has `a∉G(w)`; because this world is still possible, releasing `a` is not guaranteed correct. This is both soundness and a matching counterexample for every excluded action. ∎

After observing outcome `z` of query `q`, set `B[q=z] = {w∈B:o_q(w)=z}`. If the actual world was in `B` and the observation is valid, it stays in this set. Thus induction preserves actual-world containment along an executed policy. If this set is empty, an assumption has failed; no theorem permits a result based on that empty set.

**Parent:** DRD decision-region inclusion (`B ⊆ region(a)`); version-space elimination. **Not established:** whether a real OCM grounding/closure process supplied the right `B` or `G`.

## 3. DF-01 — an exact observational obstruction criterion

Write `u ≡_Q v` when `o_q(u)=o_q(v)` for every registered query. Let `Cells_Q(B)` be the nonempty intersections of these equivalence classes with `B`.

A finite query policy guarantees a decision on all of `B` **iff** every `C∈Cells_Q(B)` has `Safe(C)≠∅`.

**Necessity.** All worlds in `C` yield the same transcript under any adaptive policy: induction gives the same next query, same next observation, and same stopping decision. If `Safe(C)=∅`, no terminal decision is acceptable for every such world. Therefore a correct policy cannot exist.

**Sufficiency.** Query every member of `Q` once. The full observation vector identifies a cell `C`. Choose any action in `Safe(C)`. This finite construction costs at most `Σ_q c_q`. ∎

A class with empty common action is a directly checkable obstruction witness. **A pair of worlds need not suffice:** for `G(1)={a,b}`, `G(2)={b,c}`, `G(3)={a,c}`, each pair shares an acceptable action but the triple does not. If every query is constant, the triple is an obstruction that a pair-only detector misses.

This is non-identifiability **under the declared queries**, not proof that the representation, all possible experiments, or science itself is inadequate. Adding a legitimate informative query can remove the obstruction. Do not promote this certificate to a J3/J5 necessity claim without a separate lower-level-alternatives argument.

## 4. DF-02 — exact minimax verification cost

Let `V(B)` be the least worst-case sum of query costs among correct deterministic policies, with infinity when no such policy exists. A query *splits* `B` if it has at least two nonempty outcome branches there. Then

`V(B) = 0`, if `Safe(B)≠∅`, and otherwise

`V(B) = min_{q splitting B} [c_q + max_{z:B[q=z]≠∅} V(B[q=z])]`,

where a maximum with an infinite child is infinite, and a minimum over no finite candidate is infinite.

**Proof.** If a safe action exists, immediate release attains zero and positive costs cannot improve it. Otherwise a correct tree must first query. A non-splitting test provides no information, does not change the world or available tests, and costs strictly positively; delete it without harming correctness. Every remaining first query splits `B`, so each child is a proper subset. Its worst-case continuation cost is at least the child's optimum, yielding the lower bound. Conversely, attach an optimal child tree to each branch of a minimizing query; the resulting tree attains the displayed cost. Induction on `|B|` proves existence and equality in every finite case, including infinity. ∎

The induction gives a finite exact dynamic program and a policy witness. `V(B)>b` proves budget insufficiency within this model. A small allocated budget does not prove interface obstruction. Conversely, when a safe action is already established, a **zero additional query budget is sufficient**: zero budget alone is not universally `CANNOT_CHECK`.

This is Bellman optimality for finite decision trees, not a new optimization principle and not a practical polynomial-time solver for arbitrary knowledge spaces.

## 5. DF-03 — finite certificate and policy validation

A certificate binds the complete model fingerprint and one value for every nonempty subset of `W`. A checker processes subsets in increasing cardinality and verifies DF-02 using only previously checked proper subsets. If every row passes, all claimed values equal the mathematical `V`.

**Proof.** The singleton rows obey the base case. For each subsequent subset, all candidate child values are correct by induction, so computing the same min–max expression establishes that row. Complete domain coverage prevents omitting difficult cases. ∎

A separate policy checker validates every nonempty branch, verifies that each leaf action belongs to the common action set of that branch, and sums costs to the root. Its acceptance proves the policy's upper bound, not its optimality. The Bellman certificate supplies the matching lower bound. Replaying one favorable actual world alone establishes neither.

The reference fingerprint includes all allowed-action sets, query outcome tables, exact costs, query source identities, contract, epoch and closure. Changing any of these invalidates the certificate. Hash binding detects a changed declared object; it does not prove an external backend actually implements that object. The caller must establish that refinement separately.

A second finite validation path enumerates all undominated query trees (remaining-test recursion, no `Solver` cache). Agreement between these implementations is useful calibration. Both were written in one session; it is NOT independent-group verification.

## 6. DF-04 — information monotonicity and reopening

For nonempty `B'⊆B`, `Safe(B)⊆Safe(B')` and `V(B')≤V(B)` (with the extended infinity order).

**Proof.** Removing worlds can only enlarge an intersection. Restrict any correct tree on `B` to the branches reachable from `B'`, deleting non-informative queries if needed. All retained leaves remain valid and no path becomes more expensive. Take the optimum. ∎

Admitting a valid observation contracts the belief set. Revoking its authority generally expands the belief set, so both implications reverse in the relevant sense: a previously safe action may cease to be safe and verification cost may rise. Example: two worlds permit only `a` and `b`, respectively; an observation identifying world 0 permits `a` at cost zero. Revoking that observation restores both worlds, invalidates unconditional release of `a`, and restores the positive cost of identifying an acceptable action.

This theorem specifies *which old decision needs reevaluation*: the old action remains sound iff it is still in the expanded common action set. It does not prove an efficient incremental update algorithm; maintaining the explicit set and recomputing the optimum can be exponential. It does not treat changing-world dynamics as mere evidence deletion.

## 7. DF-05 — a unique coarsest sufficient quotient need not exist

A partition `P` of `W` is decision-sufficient without further queries when `Safe(C)≠∅` for every cell `C∈P`. Coarsening is ordered by inclusion of cells.

For the three-world example in DF-01, each of the three partitions having a two-world cell and a singleton is sufficient. A partition coarser than two different such pairings must merge all three worlds. That merged cell is insufficient. Hence there is **no greatest/coarsest sufficient partition**, even though minimum-size sufficient partitions exist (and here there are three).

This does NOT refute a coarsest quotient for exact preservation of a specified deterministic answer function or full future signature. It refutes an unqualified transfer of that result to **set-valued acceptable decisions**. Choosing one permissible decision, preserving all permissible decisions, reproducing a fixed solver's choice, and preserving truth are four different contracts.

**Parent:** overlapping DRD regions, elementary partition order. A new ORION name receives no priority credit. This boundary must be explicit before #201 or language ambiguity work uses a canonical-quotient claim.

## 8. DF-06 — exact zero-query persistent-state bound

For each action let `R_a={w:a∈G(w)}`. Let `τ` be the minimum number of these regions whose union covers `W`; if no cover exists, set `τ=∞`.

In an encode-then-decide model where the encoder **has observed the complete historical state `w` before compression**, and the decoder has no further observations, the minimum number of memory messages is exactly `τ`. The minimum fixed-width mutable message length is `ceil(log2 τ)` bits for finite `τ` (zero bits when `τ=1`).

**Lower bound.** A message cell must have one decoder action valid for every world mapped to it. The actions associated with all messages therefore cover `W`, so there are at least `τ` messages.

**Construction.** Choose a minimum covering set of actions. Encode each world by the index of one chosen action valid in it; the decoder returns that action. This uses `τ` messages. ∎

The integer minimum follows by finite enumeration, but is not free or necessarily efficient. Codebook/decoder description, full-state acquisition, provenance, and construction work are separate resources. This is NOT permission to encode an unobserved hidden world as free advice. It is a bound on compressing already acquired history. A one-bit saved message can be purchased with substantial acquisition and preprocessing costs.

The three-world example requires two messages, whereas lossless identification requires three. A family where one action works for all worlds needs one message regardless of the number of worlds. Thus exact task sufficiency need not coincide with full hidden-state identification.

## 9. DF-07 — exact memory–query Pareto frontier

Keep the encode-after-observation assumption of DF-06. Allow at most `k` memory messages and permit the decoder to make the registered adaptive observations after compression. Define

`V_k(W) = min_{partitions P of W, |P|≤k} max_{C∈P} V(C)`.

This expression is exactly the least worst-case online query cost with at most `k` messages.

**Lower bound.** Any deterministic encoder induces its nonempty inverse-image partition. After receiving a message its decoder must solve the corresponding cell, at worst-case cost at least `V(C)`. Maximizing over cells and minimizing over encoders gives the lower bound.

**Construction.** Choose a minimizing partition, encode its cell, and run the optimal DF-02 tree for that cell. This attains the bound. ∎

`V_k` is non-increasing in `k`. For `b` fixed-width bits use `k=min(2^b,|W|)`. Zero online cost first occurs at `k=τ`, when every cell admits an immediate action. More memory can also make an otherwise unidentifiable online obligation possible, because the encoder had additional historical access; that access must be charged.

**Exact witness.** Four worlds `(x,y)∈{0,1}²`, terminal action must equal `(x,y)`, observing `x` costs 2 and observing `y` costs 3. The frontier at `k=1,2,3,4` is `5,2,2,0`. With two cells the encoder saves `y`, leaving the cheaper `x` query; three cells cannot remove every remaining ambiguity; four messages suffice without queries. The point is a Pareto trade, not a parameter-efficiency claim. The complete reference enumerates all 15 partitions of this witness.

For unknown future contexts, define an action here as a complete response strategy over the **registered** context set, and put that strategy in `G(w)` exactly when it meets every registered obligation at `w`. Then the same theorem holds, with the strategy table and its construction charged. It grants nothing about unregistered future queries or arbitrarily long changing environments.

## 10. DF-08 — direct sum for genuinely independent verification tasks

Suppose worlds are the full Cartesian product `W1×W2`, allowed decisions factor as `G1(w1)×G2(w2)`, every test reads exactly one coordinate with that component's original cost, and there are no coupling constraints, cross-coordinate tests, or shared effects. Then

`V_joint(W1×W2)=V1(W1)+V2(W2)`.

**Upper bound.** Run the two optimal policies successively.

**Lower bound.** Every reachable belief remains a product `B1×B2`. Induct on `|B1|+|B2|`. A query in component 1 creates branches `B1[z]×B2`, whose optima by induction equal `V1(B1[z])+V2(B2)`. Minimizing over component-1 queries yields `V1(B1)+V2(B2)` when component 1 still needs work; the analogous statement holds for component 2. If a component is already decided, extra queries in it cannot improve the other component and have positive cost. The common base case costs zero. Infinity is inherited if either component contains an unsolvable observation cell. ∎

The two-bit witness attains `2+3=5`. Restrict worlds to `(0,0),(1,1)` and one cost-2 observation determines both coordinates: the joint cost becomes 2, not 5. This is not a counterexample to DF-08; it violates its Cartesian-product assumption and is a counterexample to **unconditional** addition of evidence costs.

## 11. DF-09 — matched-interface bounds for shared evidence

For two obligations on the **same** world set and with the **same complete query interface**, let `V1,V2` be the individual optima and `V12` the optimum for satisfying both. Then

`max(V1,V2) ≤ V12 ≤ V1+V2`.

**Lower bound.** Project the output of any joint policy onto either obligation; its query trace solves that obligation too.

**Upper bound.** Run a valid optimum for the first, then a valid optimum for the second. The latter may ignore earlier information or reuse already known observations without requerying. Even without such reuse, the sum is an upper bound. ∎

Both extremes are attainable: independent factors force the sum, while two identical obligations using one test attain the maximum. Do not use component costs measured under **restricted** interfaces for this lower bound. In the correlated witness, component 2 also receives the cheaper component-1 query when measured under the common interface; its matched-interface optimum is 2, not 3.

This is a concrete way to audit claims that many certificates or many agents supply additive information. Independence of identifiers does not establish the product assumption; observation/cost structure must be inspected.

## 12. DF-10 — termination and the price of exactness

Every nonterminal query in a returned optimal tree strictly decreases the size of the feasible world set and never repeats a resolved deterministic query. Hence every path has at most `min(|W|-1,|Q|)` queries. This is a well-founded bound, not an empirical tendency to stop.

The optimizer may evaluate up to `2^n-1` beliefs (`n=|W|`), consider up to `|Q|(2^n-1)` query choices, and scan their world/action tables. The certificate contains the same exponential set of subset values. Memory-frontier computation enumerates up to `Bell(n)` partitions; the zero-query cover search examines up to `2^|A|` action sets. Rational costs require exact integer arithmetic with bit lengths determined by the input rationals and summed path costs. All table storage, policy/certificate storage, hashing, verification, synthesis time and any initial history acquisition remain chargeable.

Instrument caps are safeguards, not complexity theorems: the reference default is 12 worlds for the subset solver/checker, 7 for partition enumeration, and 16 actions for cover enumeration. Exceeding a cap returns `CANNOT_CHECK` through an exception, never `OBSTRUCTION_WITNESSED`.

## 13. DF-11 — observation-constrained encoders, without hidden-world advice

DF-06/07 explicitly assume full historical observation. Remove that assumption by giving the encoder only a registered deterministic signal `z:W→Z`. An admissible encoder has form `e∘z`, with `e:Z→{1,…,k}`. The decoder knows the message and may then use `Q`. Its exact optimum is

`V_k^z = min_{partitions P of z(W), |P|≤k} max_{C∈P} V(z⁻¹(C))`.

**Proof.** Every admissible encoder partitions the attained signal alphabet. A message leaves exactly the union of the corresponding signal fibres possible. DF-02 is the minimum cost to solve that set. This gives the lower bound. Encoding a minimizing signal partition and following an optimal tree on each inverse-image cell attains it. ∎

For zero additional queries set `G_z(s)=⋂_{w:z(w)=s}G(w)`. A zero-query encoder exists iff each attained signal has nonempty `G_z(s)`, and its minimum message count is the region-cover number of this induced signal-level decision relation (apply DF-06). More bits cannot recover a distinction the encoder never observed. If a signal fibre is unsolvable even under all decoder queries, no number of messages makes the task solvable.

**Witness.** In two worlds requiring different actions, with no decoder queries, a full-world encoder could save one bit and decide. An encoder seeing a constant signal cannot decide with any memory. Giving the decoder a cost-2 distinguishing query changes its optimum to 2 but does not make the encoder informative. For the four-world `(x,y)` example, an encoder observing only `y` has a frontier `5,2` for one and two messages. It cannot attain zero decoder cost even with unlimited message capacity. An identity signal recovers DF-07 exactly.

The signal's acquisition cost, fidelity, provenance and availability are still external input obligations. A task family is not permitted to hand one arm this signal while charging the other for acquiring it. The theorem prices online verification conditional on a stated information interface; it does not erase offline learning cost.

**Parent:** decision-region determination plus deterministic encoding/partition factorization. This extension repairs the hidden-advice risk of applying a full-history compression bound to partially observed knowledge.

## 14. Foundation integration and non-consequences

This package supplies a mathematical reference for bounded epistemic control, decision-relative abstraction, channel scheduling and reopening. It does NOT supply an OCM policy trained from language, a noisy-channel model, a causal experiment scheduler, practical large-graph performance, real-world closure certification, an independent checker implementation, or a field-separation result.

The strongest parent object already explains acting without fully identifying the world. The scientific contribution in this package is an explicit, checkable integration boundary and corrections to possible overgeneralizations: set-valued sufficiency need not have a canonical coarsest quotient; budget failure is not observational impossibility; and shared evidence can defeat a naive direct sum. Priority for a new theorem is **not asserted**.

The next frontier is to obtain an acquisition-realistic, noisy, partially observed lifecycle model with revocable certificates and shared evidence, then compare its learning/repair/decision frontier with the strongest DRD, optimal-decision-tree, belief-revision and incremental-computation composition. Promising target: bounds on decision regret and recertification work after evidence revocation, counting the cost of establishing or relaxing family closure. That target is open here, not an assumed positive result.

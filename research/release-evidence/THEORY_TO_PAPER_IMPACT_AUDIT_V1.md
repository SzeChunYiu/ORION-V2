# Theory → paper impact audit V1

**Question (operator, 2026-09-05, verbatim):** *"but we are still developing the mechanics and dynamics as you see the latest commits, no need to update the paper??"*

**Short answer: no paper claim is contradicted by any theory result merged since the papers' evidence pins.** Two rows earn a citation as subsequent work and one is a live reviewer risk about definitional canonicity, not about a claim. Nothing here reopens a frozen terminal, and nothing here licenses a manuscript rewrite.

Audited at ORION-V2 `1d06d8a` (main) and ORION-paper `5bea6b3` (main). Auditor: coordinator session, first pass, by hand. `NO NOVELTY OR BREAKTHROUGH CLAIM`.

## 1. What was audited

Merged on ORION-V2 main since the papers' evidence pins (`d9e588f`, `7cc23d2`, `52d2578`, `ecf3ad4`):

| commit | content |
|---|---|
| `24566f0` (#310) | KS-T21 three-valued warrant intervals, KS-T22 reopening locality, KS-T04c prune–solve with head-share clause; ME gap atlas MEG-01…35 |
| `d756c08` (#317) | batch 1 — MEG-04/06/08/18/22/26/29/30/31/35/01 |
| `eb26335` (#333) | batch 2 — language prerequisites MEG-05/12/13/24/03/17/19/28 |
| `25bf29d` (#341) | batch 3 — dialogue prerequisites MEG-33/25/27/11/10/15/16/21 |
| `4c44e80` (#343) | batch 4 — comparison/organisation MEG-32/14/02/07/20/34/09/23 |
| `05f08fe` (#344) | batch 5 — self-model E1–E8, R1–R3 |
| `1d06d8a` (#347) | batch 6 — lifetime F1–F8 |

Open PRs (#320–#332, #346 Field Dynamics V1) are **`PENDING_MERGE`**: their declared terminals are recorded elsewhere and are not absorbable by any paper until merged.

Papers audited: FLAGSHIP (claim ledger `FLAGSHIP_MACHINE_EPISTEMICS_ATOMIC_CLAIM_LEDGER_V2.json`, 30 claims), PRA (`CLAIM_LEDGER_V1.json`, 17 claims), P-D (`ATOMIC_CLAIM_AUDIT_V2.md`), P-C (`P_C_LICENSED_FOLLOWUP_OUTCOME_LEDGER_V1.md`).

## 2. The decisive structural fact

The merged theory states its own scope: *"Objects: exactly those of the OCM canonical core (`ORION-OCM` `src/ocm/kso/{warrant,types,space,navigation,revocation,admission,abstraction,jump,resources}.py`)"* — antichains `𝒜_E` with `⊕`/`⊗`, three-valued liveness `λ_R`, hyperedge enabling, navigation matrices, Jump certificates.

The papers' formal objects are a different system: FLAGSHIP's scientific-state tuple `(x_t, c_t, i_t, Φ; P_t, S_t, O_t; A_t, R_t; M_t, V_t, X_t)` and its interface rows; PRA's machine states, successor-class layouts and state-cost typing; P-D's gate/dependence strata; P-C's obligation and feedback-screen constructs.

The two systems **share vocabulary** — warrant, evidence, revocation, reopening, authority, feedback — and **do not share objects**. That is why the default classification below is `NO_IMPACT`, and it is also exactly why the shared vocabulary needs one editorial pass: a reviewer who reads both should not find two unrelated formalisms wearing one word with no cross-reference.

## 3. Row-by-row

Classification: `NO_IMPACT` · `CITE_AS_SUBSEQUENT_WORK` · `DEFINITION_SUPERSEDED` · `CLAIM_CORRECTED` · `CANNOT_ASSESS`.

| theory result | paper | class | reason |
|---|---|---|---|
| **MEG-08 / T3** "feedback updates behaviour, never warrant" — liveness signature is independent of the navigation parameters `θ = (w_h, β_r(Q), γ_h, π)` | FLAGSHIP | **`CITE_AS_SUBSEQUENT_WORK`** | The programme's standing position that feedback cannot confer warrant now has an exact theorem with a checker on the canonical core. FLAGSHIP asserts the same separation in prose (V23 §"successful execution is not a warranted transition", the verification/validation distinction). No claim changes; a one-line citation prevents a reviewer asking whether the assertion is argued anywhere. |
| **KS-T18 corollary of KS-T21**: FEEDBACK-admitted atoms carry `⟦0,0⟧`, DEAD under every `R` | FLAGSHIP | **`CITE_AS_SUBSEQUENT_WORK`** | Same reason; this is the machine-side form of the same separation. |
| **KS-T22 reopening locality** — `REOPEN` / `RECHECK` / `UNAFFECTED` partition after a revocation, witness-calibrated | PRA | **`CITE_AS_SUBSEQUENT_WORK`** | PRA's single theory-vocabulary claim is *"a state sufficient for current linguistic prediction and current responsibility decisions can still be insufficient for correct future responsibility [revision]"*. KS-T22 answers a different question on a different object (which atoms must be rechecked once a revocation occurs, not whether a state supports later revision at all). It neither supports nor contradicts the claim. Citing it is optional and belongs in related work, not in the result. |
| **MEG-04 / T1** commit authority is a bottom for internal composition (`rank_c(A ∧ B) = min(...)`; Biba low-water-mark, Denning 1976) | FLAGSHIP | **`CITE_AS_SUBSEQUENT_WORK`** (optional) | FLAGSHIP's interface has an authority row and the V23 targeted re-review already records uncited authority/diagnosis parents. This theorem's *parents* (Biba, Denning) are the citation-worthy item; the theorem itself is machine-side. |
| **KS-T21** three-valued warrant intervals (Kleene homomorphism, exhaustive `n=3`) | FLAGSHIP | **`NO_IMPACT`** on claims; **reviewer risk noted** | FLAGSHIP does not define warrant as a lattice-valued object; it uses "warranted transition" in the systems-engineering sense and defines an interface, not an algebra. No definition is superseded because none coincides. The risk is presentational: see §4. |
| **KS-T04c** prune–solve equivalence with head-share clause; **MEG-06 / T2** restart budget bracket; **MEG-18 / T4** Jump rollback | all four | **`NO_IMPACT`** | Navigation/rollback mechanics of the KSO runtime. No paper cites, measures, or depends on these operators. |
| batches 2–6 (language, dialogue, comparison/organisation, self-model E1–E8/R1–R3, lifetime F1–F8) | all four | **`NO_IMPACT`** | Prerequisites for ORION-OCM milestones M3–M12 (dialogue, self-model, lifetime). No paper makes a claim about those milestones. Batch 6's F-rows about self-diagnosis limits and epistemic identity are about a persistent machine's lifetime, an object no current paper has. |
| batch-1 note: *"two OCM runtime defects surfaced (compose operator factor; navigate start vector)"* | all four | **`NO_IMPACT`** | OCM runtime defects in ORION-OCM. No paper cites those operators. Recorded here so the note is not mistaken for a paper-affecting correction. |
| MEG rows resolving atlas gaps (28/35 per #321, `PENDING_MERGE`) | all four | **`PENDING_MERGE`** | Not merged; not absorbable. Re-audit on merge. |

P-D and P-C: **`NO_IMPACT` across every merged result.** Their claim files use "warrant" only as an evidence-path column header, "reopen" only in the sense of reopening a study terminal, and "feedback" only for E40's feedback screen. No formal-object overlap. (Scope of that absence check: `git ls-tree` over both paper directories filtered by basename for claim/ledger/atomic/spine files — 4 files found and read — plus a keyword scan of each. Control: the same filter returns 413 files repo-wide, so the filter is not silently empty.)

## 4. The one thing that is a real risk, and it is not a claim

FLAGSHIP proposes definitions — *"Machine Epistemics is defined here as the proposed study and engineering of warranted machine-mediated scientific-state transitions"*, *"a machine-epistemic episode is proposed as a bounded object…"* — while the same repository now carries exact, checker-backed theorems using warrant, authority, revocation and reopening on a different formal core. A reviewer reading the paper and then the repository can reasonably ask which is the definition of record.

**Disposition: presentational, one sentence, no claim change, no re-freeze.** The manuscript should state that the interface standard is defined at the level of transitions between scientific states and is deliberately independent of any particular internal representation, and that the repository's KnowledgeSpace theorems are one such internal realization, cited as subsequent work. That sentence is inside the current freeze's wording latitude (it adds no quantity, changes no gate, moves no terminal). If the FLAGSHIP lane judges otherwise, it goes in as a normal `DEFINITION_SCOPE_NOTE` under a new freeze rather than being argued away.

## 5. Verdict

| paper | verdict | action |
|---|---|---|
| FLAGSHIP (V24, NMI Article, PR #149) | claims intact | add the §4 scope sentence; cite MEG-08/T3 (and optionally KS-T18, MEG-04's parents) as subsequent work |
| PRA (V18, JMLR, PR #150) | claims intact | optional related-work citation of KS-T22; no result change |
| P-D (V3, TMLR, PR #145) | claims intact | none |
| P-C (V11, PR #147) | claims intact | none |

**No paper is blocked by the ongoing theory work, and no paper should wait for it.** The theory programme runs on its own track under the work division (ORION-V2 = machine-epistemics science; ORION-OCM = the machine); a paper absorbs a theory result only through this audit, and only in one of the four classes above.

## 6. Limitations, stated

1. **First pass, by hand, by the coordinator** — not the lane-level ledger-by-ledger check with a planted-contradiction control. It is sound for `NO_IMPACT` by object disjointness (the strongest evidence here, since the theory declares its own object scope) and for the two `CITE` rows. It is weaker for any claim whose wording, rather than whose formal object, could collide. A lane-level pass should re-run it with the planted control before the papers' final gate receipts.
2. **`PENDING_MERGE` is a moving front.** Thirteen theory PRs are open, including a Field Dynamics synthesis. Each must be re-audited on merge; a paper that has already merged its gate receipt does not reopen for a `NO_IMPACT` or `CITE` row, but a `CLAIM_CORRECTED` row would reopen it, under a new freeze.
3. **This audit cannot see a claim that is wrong for reasons unrelated to the theory.** It answers only "does the new theory change the papers", not "are the papers right".

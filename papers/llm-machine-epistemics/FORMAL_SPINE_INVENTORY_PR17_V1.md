# Prospective Revision Adequacy Formal-Spine Inventory — PR17 Re-audit V1

**Skill state:** `SzeChunYiu/academic-paper-skills` PR #17 head `ef47c81101e1e1b97864019dde143456a581de1c`, stacked on PR #16 head `087e47330826295a0b114563ec33238951ac56a9`.  
**Paper:** Prospective Revision Adequacy (PRA), V12 scientific master.

## Frozen inventory

| formal_id | kind | canonical expression / definition | scientific role | main-text requirement | status |
|---|---|---|---|---|---|
| PRA-FS-01 | predictive-state definition | `h ~_{P,u} h' <=> P(Y_u^+|H=h)=P(Y_u^+|H=h')`; `S_{P,u}=[H]_{~_{P,u}}` | defines current predictive equivalence relative to a registered protocol | **required** | parent-derived definition specialized to the audit |
| PRA-FS-02 | responsibility definition | `r=(Q,A,ell,sigma)` and `A^*(h)=argmin_a E[ell(a,Q)|H=h]` | fixes the decision semantics whose current/future adequacy is tested | **required** | operational definition |
| PRA-FS-03 | representation/evidence cell | `C(z,x)={h:Z(h)=z, delta(h,x) defined}` | identifies which histories a future decision rule must serve after the same evidence | **required** | definition |
| PRA-FS-04 | compatibility criterion | `I(z,x)= intersection_{h in C(z,x)} A_x^*(h)` | complete one-step criterion for exact `ANY_OPTIMAL_ACTION` compatibility | **required** | formal definition supporting Theorem 1 |
| PRA-FS-05 | theorem | deterministic `g:(z,x)->a` exists for every history in a nonempty cell iff `I(z,x) != empty` | central one-step compatibility characterization | **required** | proved under exact semantics |
| PRA-FS-06 | non-certification | present prediction/decision adequacy alone does not certify future revision adequacy unless the registered future compatibility condition is also known | contribution-defining non-implication | **required** | corollary, bounded to registered protocol/evidence family |
| PRA-FS-07 | one-bit witness | `C_stat*=0`, `C_dyn*=1 bit`, `Omega_dyn=1 bit` | sharp finite witness that current sufficiency can omit a dormant future-revision distinction | **required** | proved finite construction |
| PRA-FS-08 | recurrent boundary | one-step compatibility does not characterize recursively minimal state for multi-step observation sequences | prevents the theorem from swallowing parent recurrent/information-state theory | **required** | explicit scope boundary |

## PR17 reader-recovery test

The V12 main manuscript already lets a competent reader recover:

1. the formal current-history/predictive-state object;
2. the responsibility/decision contract;
3. the representation/evidence cell and exact joint intersection criterion;
4. the theorem and proof;
5. the non-certification corollary;
6. the recurrent-state limitation and parent ownership;
7. the exact one-bit witness.

**Terminal:** `FORMAL_SPINE_PASS_NO_SCIENTIFIC_REWRITE_REQUIRED`.

No extra equation should be added merely for symmetry with the flagship. PR17's anti-overformalization rule applies: PRA already exposes the minimum sufficient formal core in main text.

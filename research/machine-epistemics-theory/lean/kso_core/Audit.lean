-- Axiom audit (not part of the library build): run with `lake env lean Audit.lean`.
import KsoCore
open KsoCore
#print axioms Liveness.kand_mono
#print axioms Liveness.kand_eq_min
#print axioms live_meet
#print axioms live_join
#print axioms synLeq_iff_leq
#print axioms lam_otimes
#print axioms lam_oplus
#print axioms lam_certified_ne_UNKNOWN
#print axioms lam_refines
#print axioms lam_antitone
#print axioms lam_ne_LIVE_of_lower_hit
#print axioms lam_DEAD_of_upper_hit
#print axioms lam_zero_DEAD
#print axioms reach_union
#print axioms reachDead_mono
#print axioms unaffected_unchanged
#print axioms cone_nil_of_unchanged
#print axioms lam_otimesAll_LIVE_iff
#print axioms lam_otimesAll_DEAD_of_part
#print axioms Authority.le_meet
#print axioms Authority.meetAll_le_mem
#print axioms Authority.InternalOnly.commit_zero
#print axioms Mutants.completeness_bit_does_not_compose
#print axioms Mutants.homomorphism_fails_without_wf
#print axioms Mutants.authority_max_raises
#print axioms Mutants.nogood_breaks_unconditional_kleene
#print axioms Mutants.filterN_join

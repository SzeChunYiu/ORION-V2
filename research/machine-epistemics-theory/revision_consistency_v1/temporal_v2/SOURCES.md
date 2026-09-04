# Parent-source cards and search boundary

Primary-source verification performed 2026-09-05. This is a targeted parent search,
not global novelty saturation. Mathematical proofs in THEORY.md are written here;
no uninspected external theorem is silently imported as an axiom.

## P1: may/must and partial-model semantics

Patrice Godefroid, *May/Must Abstraction-Based Software Model Checking for Sound
Verification and Falsification*, MSR-TR-2013-104 (2013; published chapter 2014).
Author-hosted text: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/main-21.pdf
Official record: https://www.microsoft.com/en-us/research/publication/maymust-abstraction-based-software-model-checking-for-sound-verification-and-falsification/

Inspected: parsed full text, especially sections 2-5, Definitions 1-3 and Theorems
4/7. Its may/must relation and information-refinement semantics own the general
machinery behind TV-3/4. This is the author's retrospective presentation, not a new
priority source. It explicitly traces original results to Bruns and Godefroid,
CAV 1999 (pp.274-287) and CONCUR 2000 (pp.168-182).
Original CONCUR work: DOI 10.1007/3-540-44618-4_14; author-uploaded abstract/full-text
entry: https://www.researchgate.net/publication/2806828_Generalized_Model_Checking_Reasoning_about_Partial_State_Spaces
The original abstract was verified; the original full proof was not independently
reconstructed from that edition. The stronger general theorem is NOT claimed as
new here. This package proves its narrow fixed-state relation-envelope fragment.

## P2: safe observations, not merely convergent updates

Shadaj Laddad, Conor Power, Mae Milano, Alvin Cheung, Natacha Crooks and Joseph M.
Hellerstein, *Keep CALM and CRDT On*, PVLDB 16(4), 856-863; DOI
10.14778/3574245.3574268. Author preprint: https://arxiv.org/abs/2210.12605
Full text inspected: https://arxiv.org/pdf/2210.12605 (v1, 2022), sections 1-3.

The source explicitly separates convergent replica updates from safe observations
and exhibits monotone observations whose positive answers survive missing updates.
This directly owns the motivation behind TV-5. Our graph-relative invariant kernel
is not a replacement CALM theorem or a proof about arbitrary distributed programs.
Only the forward composition fact for monotone functions is relevant; no inference
that every pipeline containing a nonmonotone stage must itself be nonmonotone is
used (a constant output stage is an elementary counterexample to that converse).

## P3: finite temporal safety / greatest fixed points

Clarke, Emerson and Sistla, *Automatic Verification of Finite-State Concurrent
Systems Using Temporal Logic Specifications*, TOPLAS 8(2),244-263 (1986), DOI
10.1145/5397.5399. Classic CTL model checking is the ownership parent of TV-1/2.
The publisher full-text retrieval did not succeed in this session. Attribution is
not a claim to have read that proof; the complete elementary safety/GFP and BFS
arguments needed here are supplied in THEORY.md and independently calibrated.
No novelty can be inferred from this retrieval limitation.

## Verification limitations

The PDF screenshot service returned internal errors for the requested pages of
P1/P2. Parsed text supports the inspected definitions and arguments; no result
relies on an unread figure or table. No fabricated figure inspection is claimed.
No paid-database, patent, dissertation or exhaustive changed-vocabulary saturation
was performed. Independent source/assumption review remains NOT_OBTAINED.

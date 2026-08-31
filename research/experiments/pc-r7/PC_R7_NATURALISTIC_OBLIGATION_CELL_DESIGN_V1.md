# PC-R7 — Naturalistic-Domain Obligation Cell (Registered Design V1)

**Class:** binding cell design — freezes the P-C naturalistic cell's role,
arms, stratification, endpoints and terminals **before case intake**. No
dispatch yet: the cell executes on the FM80/SD80 witness-source
infrastructure once SD80's case matrix is frozen. Nothing here may alter
FM80's frozen protocol; this cell runs beside it on the shared case matrix.

**Parent verdict this serves:** P-C status carries
`GENERATED_CELLS_CONDITIONAL_SUPPORT_ONLY` — generated-domain evidence cannot
ground the naturalistic claim (`FORMAL_DISCOVERY_GENERATED_CAMPAIGN_PLAN_V1.json`:
`generated_results_alone_grant_cross_domain_naturalistic_claims: false`). The
P-C decisive-evidence list (`TOP_TIER_SURVIVOR_AND_CONTRACTION_MATRIX_V1.json`)
requires "at least one naturalistic scientific-domain control"; import map:
SD80 → PC-C4. P-C's E20 result block gates on "frozen E30/E60 and
naturalistic-domain evidence". E30/E60 are terminal (mean-null, PC-R6 covers
the tail endpoint); this design is the remaining licensed route **A**.

**Theory revision under test (licensed, pre-registered):** **A — "obligation
structure binds to naturalistic constraint structure."** In generated cells
(BugsInPy), obligations were authored by the harness and the solver's
obligation ledger added nothing on the mean (E30-R11 null, E60 component
null). Revision A's mechanism claim: the obligation ledger earns its keep
exactly when constraints are **externally authored, verifiable, and
consequential** — replication protocols, registered analyses, reviewer-mandated
revisions — because there the ledger's satisfy/defer/reopen bookkeeping maps
onto obligations that really bind. Where constraints are internal
(self-generated subgoals), the ledger is expected mean-neutral. This is a
regime-mechanism prediction, not an unconditional superiority claim.

## 1. Case matrix (shared with FM80/SD80; tagged at intake, pre-outcome)

- Domains: FM80 §2 minimum structure (≥1 formal + 2 empirical sciences),
  ≥30 eligible cases/domain, FM80 §3 eligibility + §4 operational remoteness.
- Witness sources (from SD30/C3/C4 recon): MLRC Journal Track (39 forum
  pages; doi↔arxiv↔openreview linkage 24/30 verified) and RP:P
  (REGISTERED_REPLICATION_VERDICT class).
- **Obligation-provenance tag (this cell's intake annotation, frozen now):**
  each case's binding constraints are classified by an intake rule applied to
  the case's public record, NOT to any arm output: `EXTERNAL_VERIFIABLE`
  (constraint authored by an external authority and checkable against the
  public record: registered analysis plan, replication protocol,
  reviewer/editor mandate) vs `INTERNAL` (self-generated or unverifiable).
  Both tags must be populated ≥15 cases/domain before the cell may run;
  otherwise the cell is `INSUFFICIENT_ELIGIBLE_NATURALISTIC_CASES` (a
  contraction terminal, not a defect).

## 2. Arms (paired, minimal; FM80 §5 resource parity rules apply verbatim)

| Arm | Definition |
|---|---|
| `OBLIGATION` | Full P-C obligation-driven control (decompose → obligation ledger → satisfy/defer → selective reopen), same model family/version, tool budget, corpus, wall-clock class and output contract as its pair |
| `OBLIGATION_FREE` | Same model + budget, direct solve without the obligation ledger (E30-R11 `SIMPLE_DIRECT`/`SAME_MODEL_REFLECTION` analogue) |

No donor/transfer machinery in either arm: this cell isolates the obligation
mechanism, not P-A/P-B transfer (FM80 owns that question).

## 3. Endpoints

- **Primary (external stratum):** case-level registered decision quality on
  the case's own verifiable outcome (did the produced artifact satisfy the
  externally-authored constraints — judged by FM80 §7 independent
  adjudication, blind to arm). Binary per case.
- **Co-primary safety (non-compensatory, both strata):**
  `CRITICAL_CONSTRAINT_VIOLATION` — the artifact violates a binding external
  constraint (including silent constraint drops). Any increase vs
  OBLIGATION_FREE fails the cell regardless of the primary.
- **Secondary:** obligation-ledger coverage (fraction of externally-authored
  constraints represented in the ledger), deferred/reopen counts,
  wall-time/token parity reporting.

## 4. Statistics

Paired within case; risk differences with exact paired tests and 95%
intervals; Holm across the ≥3 domain-level primary tests (FM80 §8 freeze
discipline). Strata analyzed as pre-registered subgroups (external vs
internal), NOT post-hoc slices: the external stratum IS the primary; the
internal stratum carries a non-inferiority margin of 5 pp (frozen).

## 5. Gates (frozen before intake)

- **GN0 `INTAKE_VALID` (hard):** provenance tagging rule applied by two
  independent taggers with ≥90% agreement on a 20-case calibration set
  (disagreements adjudicated + rule clarified BEFORE the run); taggers blind
  to everything downstream.
- **GN1 `EXTERNAL_BINDING` (route gate):** external stratum, OBLIGATION ≥
  OBLIGATION_FREE by ≥10 pp in ≥2/3 domains, Holm CIs excluding 0.
- **GN2 `INTERNAL_HARMLESS`:** internal stratum non-inferiority (RD upper
  bound ≤ +5 pp) AND no CRITICAL_CONSTRAINT_VIOLATION increase in any stratum.

## 6. Pre-registered terminal map

| Outcome | Programme consequence |
|---|---|
| GN0 fail / insufficient cases | `INSUFFICIENT_ELIGIBLE_NATURALISTIC_CASES` — contraction terminal; P-C closes on generated+boundary contract |
| GN1 pass + GN2 pass | theory A survives: obligation structure binds external constraint structure → PC-C4 evidence; P-C manuscript result block re-opened under a new freeze |
| GN1 fail + GN2 pass | theory A refuted: obligations neutral on naturalistic constraints → P-C closes with the regime boundary stated as a registered result |
| GN2 fail | obligations harm naturalistic execution → contraction matrix entry + manuscript limitation |

## 7. Non-goals / no-rescue clause

No generated-cell result may be re-read through this cell. No transfer claim
(FM80's question). No endpoint, stratum margin, arm definition, or tagging
rule may change after intake begins. This design grants no claim until the
cell executes under its own dispatch freeze.

## 8. Custody and dependencies

- Designs `PC_R7_NATURALISTIC_OBLIGATION_CELL_DESIGN_V1.{md,json}` frozen in
  this PR; intake tagging rule + runner freeze in the dispatch PR.
- Execution dependency chain: SD70 (3553181, Sep 3) → E70-GC1 (3553088,
  Sep 4) → PC-R6 suite compute → SD80 case-matrix freeze → this cell.
  Ordering with FM80's own arms is resource-determined, not scientific; the
  shared case matrix and adjudication pool make parallel intake legal.
- Outputs `PC_R7_NATURALISTIC_OBLIGATION_CELL_ROLLUP_V1.{json,md}` +
  `PC_R7_OUTCOME_RECEIPT.md`; archive under
  `research/experiments/results/issue<current>/pc-r7/`; sha256 manifest over
  every case record and artifact read.

# SD70-V3 custody clause — supersession note V1

**State date:** 2026-09-04  
**Refers to:** `SD70_V3_EXECUTION_DESIGN_V1.json` sha256 `662837355020658ab77fc6067060df1b105e54ad757caf0378925178a7723138` (unchanged by this note) and its §3.1 / §11 custody clauses.  
**Authority:** grants nothing. This note records a deviation; it does not amend the design digest.

## Clause superseded, in one respect

Design §3.1 and §11: the protected seed exists **only on the Mac**; generation and evaluation run on the Mac; the seed is never copied to the dispatch host.

## Deviation

`CUSTODY_DEVIATION: seed copied to billy-old post-CHANNEL_END under operator directive 2026-09-04 ("run on laptop/billy-old/lunarc"); channel closed before transfer; seed sha verified both sides`

- Operator directive (verbatim, relayed by the coordinator 2026-09-04): *"if you need to run things, run on laptop billy laptop old via tailscale or lunarc."* Applied to the SD70-V3 protected evaluation.
- Ordering: the model channel was closed on billy-old at `CHANNEL_END.observed_utc = 2026-09-03T13:52:35Z` (canaries 9/9 at start and end; 1140/1140 responses; payload verification 9060/9060). The seed was copied on 2026-09-04, after closure. The seed was therefore never present on the dispatch host while the model channel was open, and could not have reached the model.
- Transfer: `scp` over the operator's tailscale link, Mac → billy-old `~/.orion-custody/sd70-v3/SD70_V3_MASTER_SEED.txt`, mode 600 (directory 700). sha256 of the file bytes identical on both hosts (`3cab4d9cd844566b…`); sha256 of the stripped seed string on both hosts = the design's `seed_commitment.seed_sha256` `d032efa9a570c5ba…`. The Mac copy is retained; nothing was deleted.
- Evaluation of record: billy-old (CPython 3.14.4), fresh clone at ORION-V2 `872c7a3` whose `research/experiments/sd70-v3` tree (`b6601593…`) is identical to main's. A prior Mac-side evaluation (CPython 3.13.12), performed before the directive arrived, is disclosed and compared in the evaluation receipt; it is not the record.

## Second deviation — interpreter (design §13)

`INTERPRETER_DEVIATION: evaluation of record under CPython 3.14.4 on billy-old; design §13 registers CPython 3.13.12 on the Mac for the deterministic arms and evaluation and claims byte-identity only there.` Forced by the same directive. Observed effect: exactly the §13 class — one near-tie task (`sd70v3-0230`) flips in `FIXED_META_LESSON` and its LP control; route, all gates, primary outcomes, Holm, negative controls and ablations are identical to the pinned-interpreter run, which is committed beside the record as `results/protected-crosscheck-mac-py3.13.12/`. See the evaluation receipt §0 and §4.

## What is unchanged

The gold-blindness guarantee the clause protects — oracle absent from the dispatch host while the channel is open — held throughout: `private_oracle.json` and `public_tasks.json` were never copied to billy-old; `prepare` regenerated them there from the seed only after channel closure.

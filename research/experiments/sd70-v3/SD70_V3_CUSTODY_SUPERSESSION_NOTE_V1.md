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
- Evaluation of record (coordinator decision 2026-09-04): the Mac run under the design's registered CPython 3.13.12 (§13), completed before the directive arrived. The billy-old run (CPython 3.14.4, fresh clone at ORION-V2 `872c7a3`, `sd70-v3` tree `b6601593…` identical to main's) is kept as `INTERPRETER_CROSSCHECK`. The seed transfer stands as a custody deviation regardless of which run is the record.

## Interpreter cross-check (design §13), not a deviation of record

The billy-old evaluation under CPython 3.14.4 reproduced the record's route, all gates, primary outcomes, Holm, negative controls and ablations; exactly one near-tie deterministic task (`sd70v3-0230`) flips in `FIXED_META_LESSON` and its LP control — §13's predicted class and magnitude. It is committed as `results/protected-crosscheck-billyold-py3.14.4/`. The next SD70 design version should register the off-Mac interpreter so the operator's directive and the design agree.

## What is unchanged

The gold-blindness guarantee the clause protects — oracle absent from the dispatch host while the channel is open — held throughout: `private_oracle.json` and `public_tasks.json` were never copied to billy-old; `prepare` regenerated them there from the seed only after channel closure.

# SPEED ITEMS FILED — 2026-08-27 (owner machine-time challenge, this window)

Filed as committed work items after the owner's challenge ("It seems crazy that the small change
would be two to three hours machine work still"). The instrument layer is fixed (the speed act);
what remains slow is the certification pipeline and the retry tax. These two items attack the
retry tax and the single largest wall-clock block respectively.

## S1 · Bake-class preflight checks (retry tax killer)
Today's build burned ~1 hour on five guard halts — every one a CORRECT halt, every one
discoverable in seconds before any 12-minute board build started. A `tools/preflight --bake`
class check runs BEFORE any bake/build chain and asserts:
1. **Day-0 reference currency** — the emitter's day-0 reference file exists, matches the live
   board md5 it claims, and printed==round(derived×D) on a probe row (the 31-F stale-default
   halt, twice).
2. **Emitter lineage** — the emitter script's shape matches the reference matrix it will be
   diffed against (the 29c-vs-31f lineage halt).
3. **v0surf signature vs curve** — if the bake moves the pvc curve, assert the v0surf.pkl
   config-signature will still resolve, or demand the refit be in the chain (the frozen-signature
   halt).
4. **RL_O31 / manifest attestation** — every env the emitter needs is manifest-declared.
5. **Frozen-artifact touch list** — the bake's write set is asserted against a declared
   freeze list (pvc_snapshot.json is FROZEN — the near-skew catch).
Cost: seconds. Saves: the ~1hr class of today's retry tax.

## S2 · Walk-forward matrix parallelization
The ~40-minute walk-forward matrix (~50k valuations, 2648 entrant-rows) is embarrassingly
parallel across entrants: each row re-pins the clock (MA.BASE_REF=MA.AGE_REF=Y; MA._pe_clear())
and prices independently. Shard the entrant list across N single-threaded workers (the numeric
pins stay per-worker; determinism preserved because rows are independent and the output is
keyed, order-canonicalized on merge). Target: 40 min → ~8 min on 6 workers.
Guard: a small overlap shard priced by two workers must agree byte-exact (determinism check
in the run itself).

## Parked (disclosed, not filed as work)
Compute-at-import fix (~10 of the 12 board-build minutes): value-path risk, stays parked
until a build window prices it with its own falsifier.

# HALT — THE #323 STORE BATCH CANNOT RIDE THIS LANDING COMMIT

**Measured, both directions, on committed artifacts. No gate was re-spec'd and no figure is predicted.**

The landing order (#306 comment 5189811177, unblocked by 5189920301) puts the #323 corrected store
into the landing commit. It cannot go in. The reason is structural, it is the engine's own guard, and
it stops the landing dead rather than degrading it quietly — which is why it is filed here instead of
being worked around.

## WHAT WAS DONE, IN ORDER

1. `git fetch origin claude/afl-valuation-coordinator-4k9vy5` from this box.
2. The fixture's md5 verified **from this seat's own fetch**, not taken on report:
   `docs/recipe/handover_store/rl_model_data.json` at `bcb12ea` = **`f1e8c9fed35462536d00add604f69a3f`**.
3. Installed with a dry-run-first, all-or-nothing instrument (`install_store_323.py`), which asserts
   **both** ends by full md5 before writing: live store `81d24704` in, fixture `f1e8c9fe` out.
   Measured on install: **2651 → 2650 records**, `leigh-brown` removed, **742 records differing on a
   shared key** — consistent with the batch's own accounting (~730 + the later addenda).
4. Every pin naming the store re-stamped: `data/expected_boot.json` `store`,
   `data/release_contract.json` `identities.store` with `contract_sha256` recomputed by the contract's
   own writer (`9c372afa…` → `588c463c…`), and `data/season_state.json` re-derived from the new store
   by `season_state.derive`. **Measured, not assumed:** the season dials do not move — `exposure_pace`
   stays 0.773 on 305 eligible durable players, median 17; only the source stamp moves.
   `data/release_lineage.json` (sealed history) untouched; the curve's own
   `curve_source_store_md5` provenance left at `81d24704`, because it records the store the ruled curve
   was **derived on** and the selftest's FROZEN-RULER comment says so in as many words.
5. `preboot_assert` → `bootstrap.sh` rc=0 → **Guard 5 PASS on the corrected store** (`f1e8c9fe` ==
   pinned) → tier-2 stamps regenerated.
6. Then the engine was asked to do its first real act on that store. It stopped.

## THE HALT, IN THE ENGINE'S OWN WORDS

```
v0surf FROZEN-SIGNATURE HALT: this build's config signature aca37f9f0e24cb266e7236f49d152d5a
is NOT in data/v0surf.pkl (frozen: 0589a262…, 077d4de8…).
```

The engine will not silently re-fit the year-zero surface — that fallback was removed on the owner's
word, 2026-07-28. So on the corrected store **no board, no book, no seal and no gate can be produced
at all** while the converged surface `ebc3d330` is the frozen one. This is not a degraded result; it
is a refusal to produce any result.

## WHY — THE CAUSE NAMED, NOT GUESSED

`_v0surf_sig` (`_merged_recover.py:1307`) keys the frozen surface on three legs: the pick curve
(`pvc`), the drafted roster (`roster` — one row per real ND-drafted, picked, non-pool player, carrying
its future-group label, draft age and pick), and the declared gates. `v0surf_signature_probe.py`
recomputes those legs and reproduces the engine's own signature exactly, on each store in turn:

| | rehearsal store `81d24704` | corrected store `f1e8c9fe` |
|---|---|---|
| signature | **`077d4de8…`** | **`aca37f9f…`** |
| in the frozen pickle | **yes** — engine proceeds | **no** — engine HALTs |
| `pvc` leg | `28e8449b` | `28e8449b` — **unchanged** |
| `gates` leg | `0a566c97` | `0a566c97` — **unchanged** |
| `roster` leg | `19ec6eaa` | **`31df8ae9`** — the only leg that moves |
| roster rows | 1448 | 1448 |

**Only the roster leg moves, and the row count does not.** The batch's own edits are the cause: the
2008 national-draft slide moves five picks, the two re-keyed players enter the national draft with new
picks, `leigh-brown` leaves it, and three corrected birth years move draft ages. Every one of those is
a field the signature reads.

Both directions are shown: the rehearsal store lands **inside** the frozen set and the engine runs;
the corrected store lands **outside** it and the engine stops. Neither was inferred from the other.

## THE GAP THIS EXPOSES IN THE BATCH'S OWN CLEARANCE

#323 §2 records the seam-measured consequence of the Leigh Brown removal: *"no slide crosses pick 64 —
all affected picks stay pool-class, so the priced 1–64 ladder is untouched."* That measurement is
**correct and it is about the ladder.** The year-zero surface is keyed on the **whole 1448-row drafted
roster**, not on the priced 1–64 ladder. So the ladder can be untouched — it is, the `pvc` leg above is
byte-identical — while the surface is invalidated all the same. The clearance measured the wrong
population for this consequence. Nothing in it was wrong about the ladder.

## WHAT THE OWNER'S OWN WORDS ALREADY SAY

#323's body, owner-worded: *"Fires at the landing — the store identity (`81d24704`) is pinned by every
rehearsal seal until then; these edits move it, so they land as **one batch immediately post-landing**"*
and *"The batch re-stamps the store identity and every seal pinned to it — **its own job, own captures,
post-landing**."*

The measurement above is the mechanical reason that sequencing is right rather than merely tidy: the
batch needs a year-zero refit, and a refit is a new fit, not a landing act.

## WHAT THE BATCH ACTUALLY NEEDS — its own job, plainly

1. A **FIT-CLASS box** (this one is not — see `BOX_CLASS.md`).
2. A **v0surf refit and re-pin** on the corrected store, under the declared lane.
3. **L6 re-entry**, because a new surface derives a new ladder: the adopted curve `01f27f02` is the
   converged point **on store `81d24704`**, and nothing on the record says it still is on `f1e8c9fe`.
   That question is re-opened by the refit, not settled by it.
4. The gates re-run in anger on the corrected store — G-Y0 against the 2.000% hard bar in particular,
   which now has **no dated exception behind it** (retired at L7), and the F5 seal re-measured.
5. Its own captures, and the before/after stage that this landing's deliverable leaves open by name.

**None of that is a landing act, and none of it was rehearsed in L1–L8.** The era's governing
discipline is the seam's own, from the pool-structure ruling (#306 comment 5190059333): *nothing lands
that was not rehearsed.* It applied there to strike unbuilt plumbing from this landing; it applies here
for the same reason and with a measurement behind it.

## STATE LEFT BEHIND

The store install was **reverted in full**. The working substrate is back at `2b5e99eb` — proven by
regenerating the capture byte-identically after the revert — and the live store pin stays `81d24704`.
The instrument, the probe and both probe outputs are committed here so the next seat starts from the
measurement rather than repeating it.

**The text cleanup** named in the checklist alongside the store batch is not defined anywhere on #306
or #323 that this seat could find. It is **not landed**, and it is flagged rather than guessed at.

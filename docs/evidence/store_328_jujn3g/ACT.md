# #328 — THE POST-LANDING STORE ACT. Steps 1–3 executed. **HALTED AT STEP 4.**

Seat `jujn3g`, 2026-08-05, on the seam's fire word ([#328 comment 5191304112](https://github.com/lukemcalister10/afl-rl-engine/issues/328#issuecomment-5191304112)),
on landed main `dab9657`, on a box classified FIT-CLASS before any act (`BOX_CLASS.md`).

**Read the halt first: `REVERSAL_CHECK.md`.** The reversal condition does not hold on the corrected
store — five picks move two board points where the tolerance is one — so the closure re-opens and the
decision returns to the owner. Steps 5, 6 and 7 were **not executed**. This act is not merge-ready on
its own acceptance set, and says so rather than presenting a partial run as a finished one.

---

## STEP 1 — THE CORRECTED STORE INSTALLED, AND EVERY PIN THAT NAMES IT RE-STAMPED AS ITS OWN ACT

**The fixture, verified from this seat's own fetch and not on report:**
`docs/recipe/handover_store/rl_model_data.json` at `bcb12ea` on `claude/afl-valuation-coordinator-4k9vy5`
= **`f1e8c9fed35462536d00add604f69a3f`**, the Addendum-4 re-cut. Addendum 4's trap-guard is satisfied.

**The copy**, through the landing seat's proven instrument (`install_store_323.py`), dry-run first,
both ends asserted by full md5 before anything was written. Measured on install, reproducing the
landing's own accounting exactly:

```
records  2651 -> 2650   removed ['leigh-brown']   added []
records differing on a shared key: 742
INSTALLED — live store is now f1e8c9fed35462536d00add604f69a3f
```

**THE DERIVE-RULE GATE** (`derive_rule_gate.py`) — #323 section 1's headline rule, which nothing had
ever asserted. Every record's career-games counter must equal the sum of its own season rows. It is
read live: `rl_model.py:493` takes the counter straight into the own-form trust weight.

| direction | result |
|---|---|
| the fixture, as installed | **PASS** — 0 of 2650 mismatched, 0 structural faults |
| one counter tampered | **FAILS**, naming the record (`willem-duursma` counter 18, rows sum 17) |
| the live store it replaces | **FAILS on 569 of 2651** — #323's own headline number, reproduced independently here |

That last line is why the gate is worth having: the drift the rule exists to prevent was real, is now
gone, and would be caught if a future weekly feed reintroduced it.

**THE PIN RE-STAMPS** (`restamp_store_pins.py`) — performed as four ordered acts, each through the
artifact's own writer, each re-read and asserted after the write. #328's body described the copy
instrument as if it did this; it does not, and the audit was right to say so. Every write was
preceded by a proof that the file round-trips byte-identically, so the diff carries the intended
fields and no reformatting.

| # | artifact | writer | move |
|---|---|---|---|
| 1 | `data/expected_boot.json` `store` | plain pin | `81d24704` → `f1e8c9fe`, re-read and asserted |
| 2 | `data/release_contract.json` `identities.store` | `release_contract.contract_hash` | pin moved; `contract_sha256` `9c372afa…` → **`588c463c…`**, re-read and re-verified |
| 3 | `data/season_state.json` | `season_state.derive` | re-derived from the new store bytes |
| 4 | tier-2 frozen stamps | `single_source.lock_tier2` | `peak_model_v4.pkl` `f305fe53` · `pvc_snapshot.json` `ade79790` — unchanged, as expected of pure functions of their own bytes |

**The season dials were re-measured, not carried forward.** The landing seat measured that they do not
move; that was treated as a claim to re-test, not a fact to inherit. Re-measured here on the corrected
store: `exposure_pace` **0.773**, 305 eligible durable players, median current games 17,
`calendar_progress` 0.83 — all unchanged. Only the source stamp moves. The contract seal reproduced
`9c372afa` from the pre-write body before the write, which is what proves the writer was used the way
the contract itself uses it.

**Deliberately not moved, each for a stated reason:** `ui/release_pick_curve.json`
`curve_source_store_md5` and its `one_source_selftest.py` FROZEN-RULER assert stay at `81d24704` — the
field records the store the ruled curve was **derived on**, which remains true. `data/release_lineage.json`
is sealed history. `data/rl_build/*.srcmd5` and the `ui/data` bundles are board-derived and would move
at a board rebuild, which this act never reached.

**Guard 5 re-asserted on the corrected store** after re-seeding the workspace: store `f1e8c9fe` ==
pinned, `bootstrap.sh` rc=0.

---

## STEP 2 — THE SURFACE RE-FIT ON THE CORRECTED STORE, PROVEN BOTH SIDES

**Before the refit** (`v0surf_sig_before_refit.json`) — the landing's halt reproduces on this box:

```
v0surf signature aca37f9f0e24cb266e7236f49d152d5a   in the frozen pickle: NO   engine HALTS
frozen set: 0589a262…, 077d4de8…
legs:  pvc 28e8449b (unchanged) · gates 0a566c97 (unchanged) · roster 31df8ae9 (MOVED)
roster rows 1448
```

Only the roster leg moves and the row count does not — the landing's measurement, reproduced
independently here, on a different box, from the same committed probe.

**The gate refused first, and that refusal is the design.** The bake was invoked once without
`RL_BAKE_V0SURF=1`, deliberately:

```
refit HALT: --bake requires RL_BAKE_V0SURF=1. This gate exists so an ordinary build/gate/panel run
cannot trigger a refit (silent refit is the defect being fixed).
```

Nothing was written — `data/v0surf.pkl` re-hashed `ebc3d330`, unchanged. The seat set its env var and
ran again; it did not work around the gate.

**The bake**, through the declared lane (`refit_v0surf.py --bake`, from the prepared workspace,
single-thread, FIT-CLASS box):

```
BAKE WRITTEN: data/v0surf.pkl md5 ebc3d3303a1956a8ec94b4e2c1497bdf -> e4215093693d32929820834cbd8ecb27
              re-pinned expected_boot.json 'v0surf' ; provenance -> session_2026-07-18/legf6/v0surf_refit_log.json
```

**The exact signature set the written pickle carries**, as the audit's closure of fault 2 requires:

```
aca37f9f0e24cb266e7236f49d152d5a   <- shipped
edb15f7ab7c9bded82119c99f4c5ee55
```

The old frozen pair (`0589a262`, `077d4de8`) is **dropped by design** — the bake pickles every surface
*this* build fits and writes that blob whole; it does not merge. Both old signatures remain recoverable
at the landed commit `dab9657`, and the rehearsal store's surface with them.

**After the refit** (`v0surf_sig_after_refit.json`) — the engine builds:

```
v0surf signature aca37f9f…   in the frozen pickle: YES   engine proceeds
frozen set: aca37f9f…, edb15f7a…
```

**Acceptance item 2, on the same box:** `refit_v0surf.py --verify` **REPRODUCES** the new pin
`e4215093693d32929820834cbd8ecb27`. Recorded for the cross-host check that follows.

---

## STEP 3 — THE MATRIX EMITTED, THE DELIBERATE HALT FIRED, THE HARNESS RE-PINNED

**The matrix** was emitted on the corrected store and the new surface through the committed emitter
(`emit_matrix_271.py`), preserved here as `per_entrant_328_corrected_store.json`; the committed
matrices it would otherwise have overwritten were restored byte-identically and none was overwritten.

```
exec OK. store=f1e8c9fe  v0surf=aca37f9f0e24cb266e7236f49d152d5a frozen=True
records=2645   ND 1-64 (teaches curve)=1444   ruled pool=1201
boundary crossers (pool -> ND fit via the slide): ['Daniel Butler']
pool by type: RD 691 · ND 121 · MSD 106 · UNR 59 · IRE 57 · SSP 52 · PDA 51 · PDN 43 · PDS 21
```

**THE DELIBERATE HALT FIRED**, exactly as #328 said it would. The pins were a pass-3-era prediction
carried across the landing deliberately unmoved, and this is the first real matrix since:

```
pins carried:  store 81d24704  v0surf 1cbbd9b00ff4  n 1197
HALT (assert fired): matrix store f1e8c9fe != committed identity 81d24704
```

**The ledgered re-pin**, in-file, old → new, chained onto the file's own ledger as every prior pass did:

| constant | old | new |
|---|---|---|
| `EXPECT_STORE` | `81d24704` | `f1e8c9fe` |
| `EXPECT_V0SURF` | `1cbbd9b00ff4` | `aca37f9f0e24` |
| `EXPECT_N` | 1197 | **1197 — RE-MEASURED on the real emitted matrix, never assumed** |

**Non-vacuity, both directions, after the pins moved.** All four of the loader's asserts demonstrated
able to fire on real bytes:

| fed | result |
|---|---|
| the real emitted matrix, untouched | **PASSES** (n=1197) |
| the pre-store matrix the pins used to name | HALTS — `matrix store 6b9d00a7 != f1e8c9fe` |
| store leg tampered | HALTS |
| surface leg tampered | HALTS |
| population thinned by one row | HALTS — `ND population 1196 != expected 1197` |
| teaching population emptied | HALTS — `EMPTY ND teaching population` |

**The two-axis separation re-proven**, as every prior re-pin required: the FROZEN harness byte-identical
at `e0130cc2`, and the lens basis re-emitted byte-identical at `25a72f85`.

**CHANNEL COMPOSITION — re-measured, not presumed**, on both matrices in turn:

| | n | completed | concluded realised | thin prior fallback | fallback share |
|---|---:|---:|---:|---:|---:|
| committed 279 matrix | 1197 | 301 | 825 | 71 | 5.931% |
| corrected-store matrix | 1197 | **301** | **825** | **71** | **5.931%** |

The 825 + 301 + 71 shape holds on the corrected store. The store did move and the counts legitimately
could have; they did not, and that is a measurement rather than an assumption.

**A note for #326, which queues behind this act.** The audit recorded ND65+ 121 → 122 and RD 693 → 691
on the two stores. The emit above reports **ND 121** and **RD 691** — and the two reconcile exactly:
the emitted figures are post-slide, and the run names its one boundary crosser, `Daniel Butler`, who
leaves the ND pool for the 1–64 fit. Raw store division 122, post-slide pool 121. Both numbers are
right and they measure different populations. #326's Addendum 3 already requires enumeration at build
time, so nothing depends on either being carried as a constant.

---

## STEP 4 — **HALT.** See `REVERSAL_CHECK.md`.

## STEPS 5, 6, 7 — NOT EXECUTED

The order is strictly serial and step 4 says halt. No entrant structure was re-sealed, no gate was run
in anger, no board was rebuilt, no mover was attributed, and no text fossil was touched — including the
step-7 cleanup, which #328 says *rides this act* and which therefore halts with it. There are no
figures below the halt, which is the point of putting one there.

## STEP 8 — WHAT IS FILED

Own captures, none overwritten. Committed here: this record · `BOX_CLASS.md` · `REVERSAL_CHECK.md` and
its per-pick table · the derivation's own output and its control · both signature probes · the emitted
matrix · the re-emitted lens basis · the two instruments this act wrote. The bake's own provenance log
(`session_2026-07-18/legf6/v0surf_refit_log.json`, appended by the bake itself) rides the same commit,
per the seam's second adopted rider.

**Against #328's acceptance set:** items 1, 2 and 3 are met and proven. Item 4 is met for every gate
this act reached (the derive rule, the four harness asserts, the bake's env gate, the signature probe
both directions) and **unreached** for the step-5 re-seal. Items 5 and 6 are **unreached** — the
attribution needs a rebuilt board, and the board is past the halt.

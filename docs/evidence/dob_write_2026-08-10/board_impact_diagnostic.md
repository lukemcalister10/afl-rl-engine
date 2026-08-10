# BOARD BYTE-IMPACT — measured

**Answer: the board moves, but only by a hair. Six players of 804 move, every one of them by exactly
±1 SCAR, on a board total that shifts +4 in 761,583 (+0.0005%). Pick 1 holds at 3000. No ranking of
any consequence changes. But the board md5 does move, and it cannot be produced at all without a
declared v0surf refit — which is why this act is halted, not landed.**

The brief's expectation was **zero board byte change**. That expectation is **wrong**, and this page is
the seat saying so with numbers. It is wrong in mechanism (birth data does reach current-player
pricing, through the V0 pick-curve surface) but very nearly right in magnitude (the price effect is
hairline).

---

## The three builds

All three in the same clean private workspace, same pinned environment (numpy 2.4.4 + bundled OpenBLAS
`05c9f9eb`, `PYTHONHASHSEED=0`, single-thread BLAS), same engine, same config, same everything except
the two variables named. Nothing was written back to the repo; `data/v0surf.pkl` is untouched.

| run | store | v0surf | board md5 |
|---|---|---|---|
| **A** | `0dd6b4a0` (unwritten) | frozen | `6e724cca2bb2fb118ff7ad6ed1f8a4b6` |
| **B** | `0dd6b4a0` (unwritten) | **declared refit** | `6e724cca2bb2fb118ff7ad6ed1f8a4b6` |
| **C** | `d9a24282` (**written**) | **declared refit** | `a672ed3a6a1426a262d932f844e8f87b` |

The refit is declared with `RL_V0SURF_REFIT=1`, which is exactly how the sanctioned refit lane
(`session_2026-07-18/legf6/scripts/refit_v0surf.py`) runs it. Like that lane, these runs are outside
`RL_CONFIG_MODE=gate`, because gate mode rejects `RL_V0SURF_REFIT` as an unpinned override.

**Two controls make the comparison clean:**

1. **A reproduces the shipped board `6e724cca` byte-exact.** So running outside gate mode changes
   nothing here — the manifest values are the code defaults for this build, and these boards are
   directly comparable to the shipped one.
2. **B also reproduces `6e724cca` byte-exact.** A fresh refit on unchanged data returns the frozen
   surface's board bit for bit. **The freeze is faithful and there is no refit weather.** So every
   difference between B and C is caused by the birthdates and by nothing else.

That second control is the important one. It means the diagnostic is not confounded, and it also means
a refit is not itself a source of drift on this engine.

## B vs C — what the birthdates actually move

### Present board (`v`) — 6 movers of 804, all ±1

| player | before | after | move |
|---|---|---|---|
| William McCabe | 624 | 625 | **+1** |
| Mitchell Marsh | 505 | 506 | **+1** |
| Jevan Phillipou | 274 | 273 | **−1** |
| Maxwell King | 155 | 156 | **+1** |
| Luke Urquhart | 142 | 143 | **+1** |
| Isaac Cumming | 40 | 41 | **+1** |

- Board total **761,583 → 761,587**, net **+4**, gross absolute movement **6**.
- Median absolute move **1**. Maximum absolute move **1**. There is no larger move anywhere.
- **PICK 1 numéraire = 3000, PASS** (unconditional standing law, register v30 item 17).
- **Parity gate PASS**: all 804 active board values equal the engine's gated `ev()`, matched by key,
  eps 0.
- Backward board (`back`, 198 rows): **0 movers**.

### Lens columns — same picture

| column | movers | max abs | net |
|---|---|---|---|
| `v` (now) | 6 | 1 | +4 |
| `vM1` (−1 yr) | 15 | 1 | +7 |
| `vM2` (−2 yr) | 26 | 1 | +10 |
| `vP1` (+1 yr) | 7 | 1 | +5 |
| `vP2` (+2 yr) | 6 | 1 | +4 |

Every move in every lens is exactly ±1. Two rows also move `avail_nerf` by 1 (Toby Conway −5 → −6,
Maxwell King −16 → −15).

Everything else that differs — `lensConservation`, `draftAssetTotals`, `phantomLayer`,
`phantomTotals`, the per-club sums — is arithmetic downstream of those same ±1 moves. The sealed F5
entrant layer, the draft PVC, the pick face values and the pick ladder are all byte-identical.

### Reading it

Fourteen mature-age draftees moving out of the young pick-curve sample and into the mature-entry
surfaces reshapes both surfaces very slightly. The reshaping is real but small, and after the
numéraire re-base it lands as ±1 rounding on six current players. **This is a rounding ripple, not a
repricing.** Nobody's valuation changes in any way a human would notice.

## What this does and does not settle

It settles the magnitude: **the price consequence of the birthdates is negligible.**

It does not settle the act. Two things are still true and both are the owner's call, not the seat's:

1. **The board md5 moves.** `6e724cca` → `a672ed3a`. A moved board is a landing with a re-bake behind
   it — board pin, balanced board, UI bundles, book re-seal, fixtures — not a data write.
2. **The v0surf freeze must be re-cut.** The written store's config signature `6ef67f07` is not in
   `data/v0surf.pkl`, so on main the engine simply refuses to build. Landing the birthdates requires
   `RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 refit_v0surf.py --bake` and a `v0surf` re-pin — a surface
   rebuild, which this act's scope guard explicitly forbids.

So the birthdates are correct, written, and cheap. What they need is authorisation for the surface
re-cut that carries them, which is a different menu item from the one this seat was given.

## Reproducing this

`ab_driver.sh` is the driver, verbatim. It bootstraps the private workspace from each checkout in
turn and builds. Board artifacts are not committed (each is ~4 MB of derived data that no gate reads);
the md5s above are the record, and the driver regenerates them.

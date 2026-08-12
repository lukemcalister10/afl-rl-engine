# PRE-REGISTRATION — ORDER 20C, THE PAR-FIX ADOPTION LANDING

**Committed BEFORE any board is built on this branch.** Branch `land/par-fix-adoption`, cut from
`origin/main` `435fa92`. Issue #334, owner ruling + order comment `5261191193`
(*"Yes, adopt."*, 2026-08-12).

This landing carries one lever: the ORDER 20 par arm-split fix (PR #457,
`build/nd-pool-separation` @ `78d5c38`), adopted by the owner on ORDER 20B's evidence (PR #460,
packet `5261022851`). Engine + board + pins + the movers ledger land together in one PR, per the
composition-act precedent (#399): main never carries a window in which the boot guard is broken.

Everything below is a prediction. Each is able to fail; a breach is reported, never quietly
re-scoped.

---

## 1. THE ENGINE FILES

**E1.** `engine/forward_valuation/par_build.py` and `engine/forward_valuation/par_redesign.py` land
**byte-identical** to `build/nd-pool-separation` `78d5c38`. Taken with `git checkout 78d5c38 -- <paths>`;
not re-derived, not "improved". No other engine source changes in this landing.

Measured at entry, for the record:

| file | `origin/main` (HEAD) md5 | `78d5c38` (FIX) md5 |
|---|---|---|
| `par_build.py` | `09e1c8b9e7b5609463f6e7aea8fce206` | `55429817267ffd9813c76104deb21083` |
| `par_redesign.py` | `867185e28b0a0338c0c6fa00d2c613e1` | `a2dc7b24e3c0da7f3b9377cc4a2e9164` |

**E2.** `git diff 78d5c38 -- engine/forward_valuation/par_build.py engine/forward_valuation/par_redesign.py`
on the landed tree is **empty**.

## 2. THE BOARD

**B0 (CONTROL, runs FIRST and gates everything).** Rebuilding the board on the **unmodified** landing
tree with shipped defaults, via ORDER 20B's own harness
(`docs/evidence/par_adoption_2026-08-12/scripts/build_board_o20b.sh <out> -`), reproduces the live
board **`94f1fec59f99c59d5890d5975c79fa9b` byte-identical**. If the control fails, the landing HALTS
and is reported — nothing measured afterwards would be trustworthy.

**B1.** Rebuilding on the **fixed** tree, same harness, same shipped defaults, produces
**`1dbd1480a34c7823f330273211cbb76a`** — ORDER 20's measured FIX board, reproduced twice there.
Any other hash is a HALT-and-report, not a shrug: no surprise board ships.

**B2.** The national pick curve does **not** move: PVC points moved 0 of 64, `picks[]` moved 0 of 64,
`PVC["1"] == 3000` (the numéraire law) on both boards.

## 3. THE MOVERS

Against ORDER 20's committed `fix/BOARD_DELTA_par_armsplit.json`, recomputed on my own two boards with
ORDER 20's own `board_delta.py` (arm predicate `ty=='ND' and ep<=64` = NATIONAL, everything else =
POOL):

**M1.** NATIONAL: n=**668**, movers **279**, total **624418 → 622650**, delta **−1768** (**−0.28314%**).

**M2.** POOL: n=**334**, movers **195**, total **123939 → 126244**, delta **+2305** (**+1.85979%**).

**M3.** The ledger `docs/ledgers/PAR_FIX_MOVERS_2026-08-12.md` / `.json` carries **474 rows**
(279 + 195), every one with before → after → delta, and every one of ORDER 20's 40+40 named top
movers reproduces to the unit.

**M4.** The seven movers ORDER 20B decomposed per channel — Harry Dean, Angus Clarke, Harvey Johnston,
James Leake, Willem Duursma, Will Hayes, Luke Cleary — carry their ISO / POLE / BLEND / BAR / BASE /
LVLPAR attribution into the ledger unchanged, with `BASE` **exactly 0.0** for every one of them
(20B's P14, the dead-channel finding).

## 4. THE PINS

**P1.** Exactly **two** identity pins in `data/expected_boot.json` move:

| key | from | to |
|---|---|---|
| `board` | `94f1fec59f99c59d5890d5975c79fa9b` | `1dbd1480a34c7823f330273211cbb76a` |
| `fv` | `6d36c24bb899792d15c41466377f2916fe0cb5ebee656ae38cea67038b912f7a` | `2621b56a32805f15b5084a45f851e882d1a0c6cf9c4fc2512550d394760f7dc6` |

The `fv` target is ORDER 20's own recorded FIX-tree identity (`fix/board_FIX_par_build.log`
`fv_identity`), predicted here rather than read off my build.

**P2.** Every other pinned identity in `data/expected_boot.json` is **UNCHANGED**, byte-for-byte:
`store` (`d9a24282…`), `config` (`cd38fb00…`), `rl_model` (`de7ce416…`), `engine_head` (`a8071af4…`),
`band` (`34faa865…`), `q97m` (`cfdc7321…`), `v0surf` (`fbc5b393…`), `peak_model` (`f305fe53…`),
`pvc_snapshot` (`ade79790…`), `bust_prior` (`5942aa6a…`), `register` (`652d83e8…`),
`balanced_board_md5` (`234c3414…`, a present-lens baseline that moves at a round transition, not at a
lever landing — ORDER 9 precedent), `as_of_round`, `release_version` (promotion mechanics own that,
not this branch).

**P3.** The three build artifacts that carry the board/fv identity outside `expected_boot.json` are
restamped in the same commit, per the ORDER 9 bake precedent (`7f4d5d2` / `56665de`):
`data/rl_build/rl_app_data.json` (the landed board), `engine/rl_after/rl_app_data.json` +
`.json.srcmd5` (the working board), and `engine/rl_after/rl_app_data.provenance.json`
(`fv_identity`, `fv_identity_expected`, and the `par_build.py` / `par_redesign.py` entries of
`fv_source_hashes`).

**P4.** `boot_guard.assert_boot` **PASSES** on the landed tree — every one of its assertions: checkout
store, register, config, board (full-hash), `rl_model`, the five fitted artifacts, the three
load-path resolutions, and both halves of the forward-valuation provenance check (checkout integrity
and loaded-path integrity).

## 5. THE UNTOUCHED — the scope guards, asserted as numbers

**U1.** The store `engine/rl_after/rl_model_data.json` md5 is **`d9a24282357cf3083b1640466e3ecd83`** at
entry and at exit. Read-only the whole landing.

**U2.** The three frozen pickles are byte-identical at entry and exit and equal their pins:
`data/v0surf.pkl` `fbc5b393…`, `data/q97m.pkl` `cfdc7321…`, `/home/claude/cm_400.pkl` (band)
`34faa865…`. **No pickle is regenerated** — the deferrals are owner-ruled.

**U3.** The instrument `docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py` is
**unmodified**. Its md5 is computed at entry and at exit and the two are asserted **equal to each
other and equal to `origin/main`'s copy**. Computed at entry on this branch, and on `origin/main`:
**`0f8220351c64c56ccfa90c60edcdfa5f`** — which matches ORDER 20B's recorded pin exactly. (No pin hex
was taken on trust from the order text; the value was computed from the file.)

**U4.** `H_POOLSIT` / `H_UNION` and every sitter configuration are **untouched** — that lever lands
with the pool update, per the owner-ruled attribution separation. `LTI_REGISTER.md`,
`docs/OPEN_ITEMS_REGISTER.md` and the directive are untouched by this branch (the seat pen follows
the landing).

**U5.** No shipped default changes beyond what PR #457's two files themselves carry:
`data/model_config.json` is byte-identical at entry and exit, and the config hash `cd38fb00…` does not
move.

## 6. WHAT WOULD MAKE ME REPORT A BREACH

Any of: the control not reproducing `94f1fec5`; the fix board landing on anything other than
`1dbd1480`; the engine files not being byte-identical to `78d5c38`; a third pin moving; the boot guard
failing; any of U1–U5 moving; or the mover counts differing from 279 / 195. Each is reported in
`LANDING_VERIFICATION.md` and in the hand-back, owned, not rationalised.

---

_Generated by [Claude Code](https://claude.ai/code)_

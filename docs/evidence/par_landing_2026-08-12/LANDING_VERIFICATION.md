# LANDING VERIFICATION — ORDER 20C, THE PAR-FIX ADOPTION LANDING

Branch `land/par-fix-adoption`, cut from `origin/main` `435fa92`. Issue #334, owner ruling
`5261191193` (*"Yes, adopt."*, 2026-08-12). Pre-registration `PREREG_ORDER20C.md`, committed at
`7cb5d8d` **before any board was built on this branch**.

**Every pre-registered prediction held. No breach, no surprise.**

---

## 1. THE CONTROL — run FIRST, and it passed

Before the fix was applied, the board was rebuilt on the **unmodified** landing tree using ORDER 20B's
own harness — `docs/evidence/par_adoption_2026-08-12/scripts/build_board_o20b.sh <out> -`, shipped
defaults, no manifest override, `RL_CONFIG_MODE=gate`, single-threaded BLAS, `PYTHONHASHSEED=0`:

```
  variant manifest: (HEAD defaults)
  engine_head: a8071af4  rl_model: de7ce416
  OK 94f1fec59f99c59d5890d5975c79fa9b  -> board_CONTROL.json
```

**`94f1fec59f99c59d5890d5975c79fa9b` — byte-identical to the live pinned board.** (PREREG **B0 —
TRUE**.) The harness is therefore anchored to the exact board the owner decided about, and everything
measured after this point is trustworthy. Had this failed, the landing would have halted here.

## 2. THE FIX BOARD

The two files were then taken off `78d5c38` and the same harness re-run, unchanged:

```
  variant manifest: (HEAD defaults)
  engine_head: a8071af4  rl_model: de7ce416
  OK 1dbd1480a34c7823f330273211cbb76a  -> board_FIX.json
```

**`1dbd1480a34c7823f330273211cbb76a` — byte-identical to ORDER 20/20B's measured FIX board.**
(PREREG **B1 — TRUE**.) No other hash appeared; nothing had to be explained away.

The delta, recomputed with ORDER 20's own `fix/board_delta.py` on my two boards, reproduces its
committed `BOARD_DELTA_par_armsplit.json` on **every** published figure (`movers_verification.txt`):

| arm | | mine | ORDER 20 | |
|---|---|---:|---:|---|
| NATIONAL | n | 668 | 668 | MATCH |
| | movers | 279 | 279 | MATCH |
| | total | 624418 → 622650 | 624418 → 622650 | MATCH |
| | delta | −1768 (−0.2831%) | −1768 | MATCH |
| POOL | n | 334 | 334 | MATCH |
| | movers | 195 | 195 | MATCH |
| | total | 123939 → 126244 | 123939 → 126244 | MATCH |
| | delta | +2305 (+1.8598%) | +2305 | MATCH |

All **40 + 40** of ORDER 20's named top movers reproduce **to the unit**. The national pick curve does
not move — PVC 0 of 64, `picks[]` 0 of 64 — and pick 1 = 3000, the numéraire law. (PREREG **B2, M1,
M2 — TRUE**.)

## 3. BYTE-IDENTITY OF THE ENGINE FILES vs `78d5c38`

The fix was taken verbatim with `git checkout 78d5c38 -- engine/forward_valuation/par_build.py
engine/forward_valuation/par_redesign.py`. Nothing was re-derived, reformatted or "improved".

```
$ git diff 78d5c38 -- engine/forward_valuation/par_build.py engine/forward_valuation/par_redesign.py
(no output)
```

| file | `origin/main` | landed | `78d5c38` |
|---|---|---|---|
| `par_build.py` | `09e1c8b9e7b5609463f6e7aea8fce206` | `55429817267ffd9813c76104deb21083` | `55429817267ffd9813c76104deb21083` |
| `par_redesign.py` | `867185e28b0a0338c0c6fa00d2c613e1` | `a2dc7b24e3c0da7f3b9377cc4a2e9164` | `a2dc7b24e3c0da7f3b9377cc4a2e9164` |

An empty diff against the source branch **is** the proof. (PREREG **E1, E2 — TRUE**.) No other engine
source moves: `rl_model.py` (`de7ce416`) and `_merged_recover.py` (`a8071af4`) are byte-identical to
`origin/main`.

## 4. THE PINS RESTAMPED — exactly two, and the set was asserted before writing

`restamp.py` enumerates every non-note key of `data/expected_boot.json`, prints moved and unmoved
alike, and **asserts the moved set is exactly `{board, fv}`** before it will finish:

| key | from | to |
|---|---|---|
| `board` | `94f1fec59f99c59d5890d5975c79fa9b` | `1dbd1480a34c7823f330273211cbb76a` |
| `fv` | `6d36c24bb899792d15c41466377f2916fe0cb5ebee656ae38cea67038b912f7a` | `2621b56a32805f15b5084a45f851e882d1a0c6cf9c4fc2512550d394760f7dc6` |

The `fv` target was **pre-registered from ORDER 20's own build log before I computed it**, and the
landed tree's computed identity equals it exactly. (PREREG **P1 — TRUE**.)

**Unmoved, printed key by key:** `store`, `config`, `rl_model`, `engine_head`, `band`, `q97m`,
`v0surf`, `peak_model`, `pvc_snapshot`, `bust_prior`, `register`, `balanced_board_md5`, `as_of_round`,
`release_version`, `register_note`, `tag`. (PREREG **P2 — TRUE**.)

Three further identity carriers live outside `expected_boot.json` and are restamped in the same commit,
per the ORDER 9 bake precedent (`7f4d5d2` / `56665de`):

- `data/rl_build/rl_app_data.json` — the landed board
- `engine/rl_after/rl_app_data.json` + `.json.srcmd5` (`own_md5`) — the working board
- `engine/rl_after/rl_app_data.provenance.json` — `fv_identity`, `fv_identity_expected`, and the
  `par_build.py` / `par_redesign.py` entries of `fv_source_hashes`

Both sidecars keep the engine's own **no-trailing-newline** byte convention, so a later rebuild
produces no spurious diff against what landed. (PREREG **P3 — TRUE**.)

## 5. BOOT GUARD ON THE LANDED TREE — PASS

Run against this worktree with `RL_REPO` and `RL_FV` pointed at it (`boot_guard_landed.txt`):

```
--- (A) forward-valuation provenance, both halves (checkout + loaded-path) ---
PASS — no failures

--- (B) assert_boot: store / register / config / board / rl_model / fitted / load-path ---
boot-store guard (Guard 5) PASS  [order20c_landing]
   store d9a24282 == pinned d9a24282  |  rl_model de7ce416 == pinned de7ce416
   |  fv 2621b56a == pinned 2621b56a (checkout+loaded-path)

BOOT GUARD: PASS on the landed tree.
```

That covers every assertion Guard 5 makes: checkout store, register, config hash, board (full-hash
compare), `rl_model`, the five fitted artifacts (`q97m`, `v0surf`, `peak_model`, `pvc_snapshot`,
`bust_prior`), the three load-path resolutions (`q97m`, `v0surf`, `band`), and **both** halves of the
forward-valuation provenance check — checkout integrity and loaded-path integrity. (PREREG **P4 —
TRUE**.)

## 6. THE UNTOUCHED ARTIFACTS — asserted as numbers, not claimed

Each computed from the file on disk at exit and compared against `origin/main`'s own copy of the same
file (`untouched_artifacts.txt`):

| artifact | landed md5 | `origin/main` md5 | |
|---|---|---|---|
| **store** `engine/rl_after/rl_model_data.json` | `d9a24282357cf3083b1640466e3ecd83` | same | UNMOVED |
| **pickle** `data/v0surf.pkl` | `fbc5b39387b2b135284a2e157f46c810` | same | UNMOVED |
| **pickle** `data/q97m.pkl` | `cfdc73216c099e5e8f1fda3968f31c00` | same | UNMOVED |
| **instrument** `noarb_table_338.py` | `0f8220351c64c56ccfa90c60edcdfa5f` | same | UNMOVED |
| `data/model_config.json` | `efe922cbe21fb69262f53bec70302279` | same | UNMOVED |
| `engine/rl_after/rl_model.py` | `de7ce41659adeda756f4fd1a2caaf172` | same | UNMOVED |
| `engine/rl_after/_merged_recover.py` | `a8071af4dd86b7d8d3d9d916ae75f787` | same | UNMOVED |
| `LTI_REGISTER.md` | `652d83e87780e415a01a2de6d8b3cc57` | same | UNMOVED |
| `peak_model_v4.pkl` | `f305fe5330222f4fa14d3654a0e91ef7` | same | UNMOVED |
| `pvc_snapshot.json` | `ade79790efc8ad4585c2c6800a935eaa` | same | UNMOVED |
| `bust_prior_table.json` | `5942aa6ad7be1d482eed737997486c70` | same | UNMOVED |

The **band pickle** `/home/claude/cm_400.pkl` (outside the checkout, on the engine's own load path)
reads `34faa8659cc8f19794f5cb9584fa19b2` == its pin. **No pickle was regenerated** — the v0surf / q97m
/ cm_400 deferrals are owner-ruled. (PREREG **U1, U2 — TRUE**.)

### A note on the instrument pin, deliberately

The order text carried a **garbled md5** for `noarb_table_338.py` and contradicted itself about it
three times in one paragraph. **No hex was taken on trust from it.** I computed the file's md5 on this
branch and on `origin/main`, asserted the two **equal to each other**, and the value is
`0f8220351c64c56ccfa90c60edcdfa5f` — which matches ORDER 20B's independently recorded pin in
`ADOPTION_EVIDENCE.md`. Neither of the order's two candidate strings (`0f8220351c64c56cdc90c60edcdfa5f`,
`0f8220351c64c56cdcaa…`) is correct. The file is untouched by this landing. (PREREG **U3 — TRUE**.)

### Sitter configuration

`H_POOLSIT` / `H_UNION` and all sitter configuration are **untouched**: no non-documentation file on
this branch adds or removes a line mentioning them, and all 8 sitter-config lines are byte-identical to
`origin/main`. That lever lands with the pool update, per the owner-ruled attribution separation.
(PREREG **U4** — TRUE.) `data/model_config.json` is byte-identical and the config hash `cd38fb00…` does
not move, so no shipped default changed beyond what PR #457's two files themselves carry. (PREREG
**U5 — TRUE**.)

## 7. THE BOOK RE-SEALED — a red gate this landing would otherwise have left on main

The board move breaks **F2 book↔board parity** (`one_source_selftest.py` section 3: every shared board
`v` must equal `round(book cur / 1.0524)`). Measured, not assumed:

| book | vs board `94f1fec5` | vs landed board `1dbd1480` |
|---|---:|---:|
| as committed on `origin/main` (`6f356d82`) | **0** mismatches | **398** mismatches |
| re-sealed on the landed tree (`0bcee13b`) | — | **0** mismatches |

So the landing re-seals it, exactly as the ORDER 9 bake did (`7f4d5d2`) when it moved the board. The
book was rebuilt by `engine/rl_after/s4_matrix_M1v7.py` in a **scratchpad copy** of the landed tree
(the checkout is never built in), after asserting that copy carried the landed board, store and `fv`.
The builder's **own** parity gate passed in the same run:

```
BOOK PARITY GATE PASS: all 802 shared board players' present value == round(book cur / 1.0524)
  [numéraire]; 2 board players outside the cohort book (_pvc_exclude): ['adam-treloar', 'jeremy-cameron']
```

### A finding worth the seat's attention: `s4_matrix.json`'s md5 is meaningless

I ran a **book control** — rebuild the book on an `origin/main` tree and check it reproduces main's
committed `s4_matrix.json`. It does **not**: `865aeb3f…` vs main's `6f356d82…`. That looked alarming,
so I diagnosed it rather than shipping past it:

- all **2647** `cur` values are **identical** between main's book and my rebuild — 0 differ;
- both are F2-clean (0 mismatches) against the control board;
- the *keys* share **nothing** — because the book's top-level dict keys are Python **`id()` values**,
  i.e. memory addresses, which differ every process.

The book file is therefore **non-byte-reproducible by construction**, and its md5 carries no identity
information. That is consistent with the repo's own conventions — `s4_matrix.json` is deliberately
**not** pinned in `data/expected_boot.json` and the boot guard does not assert it; F2 keys on the inner
`key` field, not the top-level id. So the md5 churn in this commit is expected noise, not a signal, and
no identity pin is disturbed by the re-seal. Flagged because a future seat diffing this file will
otherwise think something moved.

## 8. THE FULL DIFF vs `origin/main`

Ten files, and no others:

```
data/expected_boot.json                        (2 pins: board, fv)
data/rl_build/rl_app_data.json                 (the landed board)
engine/forward_valuation/par_build.py          (verbatim from 78d5c38)
engine/forward_valuation/par_redesign.py       (verbatim from 78d5c38)
engine/rl_after/rl_app_data.json               (the working board)
engine/rl_after/rl_app_data.json.srcmd5        (own_md5)
engine/rl_after/rl_app_data.provenance.json    (fv identity + 2 source hashes)
engine/rl_after/s4_matrix.json                 (the book, re-sealed — F2 398 -> 0)
engine/rl_after/s4_matrix.json.srcmd5          (own_md5)
docs/ledgers/PAR_FIX_MOVERS_2026-08-12.{md,json}   + docs/evidence/par_landing_2026-08-12/*
```

## 9. THE MOVERS LEDGER

`docs/ledgers/PAR_FIX_MOVERS_2026-08-12.md` + `.json` — **474 rows** (279 national + 195 pool), every
one named, before → after → delta → pct, joined with ORDER 20B's per-channel decomposition for the
seven named large movers (Harry Dean, Angus Clarke, Harvey Johnston, James Leake, Willem Duursma, Will
Hayes, Luke Cleary). `BASE` is **exactly 0.0** for all seven, and for the board as a whole — 20B's
dead-channel finding, carried into the lever's permanent record. (PREREG **M3, M4 — TRUE**.)

One lever, one ledger.

---

## 10. THINGS THE SUPERVISING SEAT SHOULD KNOW

1. **A pre-existing wart I did NOT fix, so it is not mistaken for my work.**
   `data/rl_build/rl_app_data.json.srcmd5` carries `own_md5: 4b448a821f54180182637983f7a26a9d` — the
   board from *before* the ORDER 9 adoption bake. It was already stale on `origin/main` (ORDER 9 moved
   the board beside it and left this sidecar alone), it is read by no guard, and correcting it is not
   this landing's lever. Flagged rather than silently swept in. Its sibling
   `engine/rl_after/rl_app_data.json.srcmd5` **is** current and **is** restamped here.
2. **The book re-seal is a separate commit** (`ORDER 20C step 4`) precisely so the seat can drop it
   independently if it judges the book to belong to a different act. Dropping it costs the F2 gate
   (398 mismatches) but nothing else: no pin, and not the boot guard.
3. **I did not run the full gate suite.** I ran the board build, the delta reproduction, the book
   re-seal (with its own parity gate) and the boot guard. `ship_gates_check.py` carries a
   **pre-existing** RED that ORDER 9 diagnosed and proved older than its own act — it hardcodes
   `RL_GAMMA='0.85'` at `:64` while the manifest pins `1.0`, so it halts on a divergent-override before
   reaching anything this landing changed. I did not work around it and did not touch it.
4. **Not merged.** Branch + PR + STOP, per the order. The register pen follows the landing.

---

_Generated by [Claude Code](https://claude.ai/code)_

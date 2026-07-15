# PLAN — WIRE L-CAPTAIN: THE RULED CAPTAIN CURVE (auto-mode first artifact)
Register item 141 · CONSTRAINTS_v1_15 PART 5 (R98.1) · replaces the retired saturating `capt_prem`.

## Base (STRICT — verified before work)
- Branch `claude/l-captain-curve-wire-r98a1` cut from the re-entry-trio head `0cf723af6aa19743092d740a4a13c082b8d5f9ed`
  EXACTLY (full-URL ls-remote: pin == `refs/heads/claude/reentry-trio-store-correction-4rzfl7` == PR #93 head;
  `git checkout -b … 0cf723af`; HEAD == pin). Owner ruling (2026-07-15): branch STRICT from the trio head; push
  to a NEW branch of my own naming; **never** touch/rewrite/force `trusting-edison`.
- Engine `_merged_recover.py` `fc7045d6` · rl_model `952ddb3d` (== expected_boot). Store `b1fd0bce`, board
  **`800d0399`**, config `c2d233ae`, q97m `cfdc7321` — all Guard-5 asserted == pinned from a fresh bootstrap.
- Prerequisites (per L-CAPTAIN's own text): (1) `rl_model` pin ASSERTED by boot_guard — **PASS** (Guard 5 block
  0f, engine `1073f633`, rides this base) · (2) book re-sealed for the trio store — ✓ (rides this base) · (3) the
  ITEM-74 reconcile rides this chapter's audit. All satisfied or riding.
- FEED read from `origin/main:docs/…` (owner ruling: docs are FEED, not history — read, do not commit onto this
  branch; the candidate line's older doc files reconcile at the promotion merge): CONSTRAINTS_v1_15 PART 5
  (L-CAPTAIN VERBATIM), acceptance_v1_15.json, OPEN_ITEMS_REGISTER items 130 / 140-141. The live saturating
  `capt_prem` is REPLACED (delete-from-live, obituary in RETURN), not disabled.

## FENCE
`engine/rl_after/rl_model.py` (the ONE file carrying `capt_prem`; the level→value legs in `_merged_recover.py`
call it via `MA.capt_prem`, so replacing the function body wires every leg with **no** `_merged_recover.py`
edit — engine_head `fc7045d6` UNCHANGED, the **rl_model** pin moves) · data re-pins (`data/expected_boot.json`
board+rl_model, `data/book_stable_seal.json`, `data/gates_snapshots/gates_fc7045d6.json`) ·
`session_2026-07-15/captaincy/`. **NO store write. Config UNMOVED** (RL_CAPT is a declared kill-switch, not a
manifest dial). S2 (a probabilistic future-captaincy layer) is a NEW directive — out of scope.

## The curve (CONSTRAINTS PART 5 — VERBATIM, verified numerically)
`credit(L) = G · ∫[BAR → L] P(a) da`, `P(a)=1/(1+e^-((a-M)/W))` logistic. **BAR 105.0 · M 109.5 · W 1.85 · G 1.00.**
Closed form (integral of the logistic = W·softplus): `credit(L) = G·W·[softplus((L-M)/W) − softplus((BAR-M)/W)]`,
`softplus(x)=ln(1+e^x)`, **clamped to 0 at/below the bar** (a credit is never negative; continuous — credit=0
exactly at L=BAR). Verified: asymptote `L − 109.6557` (spec 109.66; **NOT** 107.4 = the retired CAPT_THRESH) ·
marginal `P(120)=0.99658` (spec 0.997; do not gate on "exactly") · marginal 0.081→0.500→0.997 at bar/mid/120 ·
marginal = G·P(L) structurally < 1 (the slope-1 ceiling is the logistic asymptote, **not** clamped). Reference
credits invert to clean levels: Gawn 16.34→L=126.00 · Bont 9.85→L=119.50 · Daicos 4.96→L=114.50 (achieved
credits at the engine's projected levels reported in RETURN beside the fitted references).

## The wiring (rl_model.py — replace the `capt_prem` body)
`capt_prem` (`:180`) is the retired saturating curve (`CAPT_GAIN/EXP/CAP`, bar `CAPT_THRESH=107.4`, hard 18-pt
cap — NEVER owner-ratified). It is called by the LIVE path (`_merged_recover.py` `_proj_w4` `:724`
`base=lev+MA.capt_prem(lev)` inside the k-loop over the current year k=0 **and** every projected future year k>0;
`:749` the prod-floor leg) and the dormant `rl_model` ev() path (`:339/:353/:543`). Replacing the function body
wires the ruled curve into **all** legs through the existing level→value plumbing — no new machinery (no HALT).
- `LCAPT_BAR=105.0; LCAPT_M=109.5; LCAPT_W=1.85; LCAPT_G=1.00` — PINNED in-code (item 114: no `os.environ` on a
  board-changing dial). `_capt_ruled(lev)` = the softplus closed form, clamped ≥0.
- The retired saturating body kept as `_capt_saturating(lev)`, reachable ONLY via the kill-switch.
- `capt_prem(lev) = _capt_ruled(lev) if _CAPT else _capt_saturating(lev)`.

## Kill-switch (G-ATTR declared exception, default ON) — RL_CAPT
`_CAPT = os.environ.get('RL_CAPT','1') != '0'` (rl_model.py already imports `os`). Default ON ⇒ ruled curve.
`RL_CAPT=0` ⇒ retired saturating curve ⇒ board **`800d0399`** byte-exact (prove: both md5s). Declared exception,
NOT a manifest dial ⇒ config_sha256 UNMOVED. Gate/bake mode clears ambient model env, so RL_CAPT is never set
there (code default ON = the official ruled board); RL_CAPT=0 ablation runs in the DEV shell only (the gate
reject-scan is never tripped — the improver #90 pattern, dev==gate at base validated there).

## Measurement (MEASURE, never assume — the law's own warning)
- Boards (dev shell, dump.py): base = RL_CAPT=0 (must md5 == 800d0399) · cand = RL_CAPT=1. Per-player
  ev/num/lvl/age. Kill-switch proof = both board md5s. Gate-mode candidate board for B4 byte-agreement.
- **G-COHORT**: all three ratios (y4/y5/y6) vs BOTH **1.30** and the waived **1.335** — state which bound each
  clears. Breaching 1.335 is a HALT (the waiver edge is a wall). Regenerated on the rebuilt book.
- **A-PAIRS** scored: pair_1 gawn/briggs · pair_2 reid/bont · **pair_3 sanders/bont — EXPECTED TO WORSEN**
  (the recorded warning: the curve lifts young upper tails); scored before→after, never smoothed / no hand-edit.
- **A8** Berry/Tsatas by name (ratio). **PICK 1 = 3000.** Three narrowest margins.
- **VALUE-FLOW (item 130):** movers, ΣΔ num-SCAR, age-bucket distribution (≤22 / 23-26 / ≥27), three largest
  lifts + three largest cuts BY NAME. Complete AFFECTED_ROWS with the **credit each mover earned**.
- Achieved credits for Gawn/Bont/Daicos beside the fitted references (16.34 / 9.85 / 4.96).

## Certification & re-pins
- Full ship-gates BASE (RL_CAPT=0) + CAND (default): LOG + SNAPSHOT `data/gates_snapshots/gates_fc7045d6.json`
  + reports committed. Five SSI guards + Guard 5 (now incl. the rl_model assertion) green from FRESH bootstrap.
- Book RE-SEALED (reseal_book.py; store/config UNCHANGED; stable_sha256 advances — the curve moves ev() in every
  credited historical season, G-BOOK). expected_boot RE-PINNED: **board + rl_model** only (engine_head fc7045d6,
  store b1fd0bce, config, band, register, fitted pins all UNCHANGED). Store UNTOUCHED. Config UNMOVED or HALT.

## Order
PLAN(commit) → wire rl_model.py → byte-exact-off proof (both md5s) → candidate board (dev + gate) → dump+measure
(cohort/A-pairs/A8/value-flow/AFFECTED_ROWS/credits) → ship-gates BASE+CAND + snapshot → reseal + re-pin →
fresh-bootstrap Guard 5 + five SSI guards → commit + push to the new branch → PR → RETURN (≤30 lines).

## Time
Band 1.5–3 h (one lever, pattern-proven on #90; the future-projection leg wires through existing plumbing — no
new machinery). No >2×/<½× flag anticipated; actual reported in RETURN.

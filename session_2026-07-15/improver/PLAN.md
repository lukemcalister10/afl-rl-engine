# PLAN — THE IMPROVER BUILD (auto-mode first artifact)
`_eo` TWO-DIRECTIONAL · L-SYMMETRY WIRED · THE S_AGE 29-TAIL — register item 134, the chapter's last writer.

## Base (STRICT — verified before work)
- Branch `claude/improver-build-symmetry-ukvtma` reset to base pin `claude/intelligent-lovelace-6v863q` @
  `557297cd018d76f36cb555edfb6a4816836ca2f9` EXACTLY (full-URL ls-remote + rev-parse; HEAD==pin). Merge line
  `#82→#83→#85→#89→this`; PR based on the #89 branch.
- Engine `edc47017` (== expected_boot engine_head). Base board **`9a9889f8`** reproduced byte-exact in BOTH
  gate mode (`RL_CONFIG_MODE=gate`) and dev mode — the ablation methodology is validated (dev==gate at base).
- Store `340a7a32` UNCHANGED (untouched this build). Config `c2d233ae` UNMOVED (three switches are DECLARED
  kill-switch exceptions on the #85 RL_DAMP / #89 RL_EVW pattern — NOT manifest dials; ablations run in the
  dev shell so the gate reject-scan is never tripped and config_sha256 does not move).
- FEED read from the repo: register items 108, 127, 128, 130, 134; `acceptance_v1_13.json` (L-SYMMETRY /
  L-SAGE-FADE / L-SMOOTH entries); PR #88 `residual_by_age.csv` (age-29 smoothed **+0.3793**, engine 0.0269);
  HANDOVER rev139 §improver. NOTE: the #89 base carries the chapter's engine but the older doc set (v1_10/
  v78); the operative spec docs (v1_13/v101/rev139) are the supervisor's doc-line artifacts and are used as
  the SPEC — this build touches only the fenced files, never the register/constraints.

## FENCE
`engine/rl_after/_merged_recover.py` · data re-pins (`data/expected_boot.json`, `data/book_stable_seal.json`,
`data/gates_snapshots/gates_<engine>.json`) · `session_2026-07-15/improver/`. No store, no config, no other
engine file (all three legs live in `_merged_recover.py`). SCOPE EXCLUDES evidence-weight core (#89), the
absence term (#85), anything PVC/iso_corr/pick-curve (items 130–133: next chapter).

## The live path (verified)
`cp._lvl_eff = _lvl_eff_abs → _inferM1 → _coreM1 → _est` (line 471/384). The `_lvl_eff_*`/`_est_core` twin is
DEAD (comment line 210 "DORMANT twin … superseded via the _inferM1 bind"; verified never bound/called). All
three legs are wired into the LIVE path only; the dormant twin is left byte-identical (byte-exact base is
trivially preserved there) with a one-line note pointing to the live legs.

## LEG 1 — `_eo` TWO-DIRECTIONAL (`RL_EO2`, default ON)
`_inferM1` (line 352) today: `return (1-eo)*L0 + eo*min(L0, max(_upS(...), _lvlcurr(p,Y)))`. The `min(L0, …)`
caps the demonstrated-production target T at L0, so the anti-flattery term can ONLY pull DOWN (comment line
225 "Only ever pulls DOWN"). Kill the `min()`, KEEP the term (HANDOVER rev139: "it is the only anti-flattery
mechanism in the engine"): `T = max(_upS(…), _lvlcurr(p,Y))`; return `(1-eo)*L0 + eo*(T if _EO2 else min(L0,T))`.
Now a player whose demonstrated production sits ABOVE L0 is pulled UP toward it, below is pulled DOWN — over-
and under-priced both expressible. L-SMOOTH: `max`/blend are continuous; `eo→0` still returns L0; no new
threshold. `RL_EO2=0` ⇒ the `min()` is kept ⇒ byte-exact base.

## LEG 2 — L-SYMMETRY WIRED (`RL_LSYM`, default ON)
Spec = acceptance `L-SYMMETRY` (owner verbatim, item 108) + its `asymmetry_corrected` clause, which names
exactly three defects in the LIVE `_est` up-branch (line 316):
`return (Lo + s·gap) if (gap>=TOL_M1 and _radq(p,Y,Lo)) else Lo`  where `s=_S_AGE(age)` (or S_M1), `gap=Lc-Lo`.
  1. **Unequal bar** — a RISE needs `gap>=TOL_M1(5.0)`; a DECLINE needs `drop>DOWN_TOL(3.0)`. → use the SAME
     bar `DOWN_TOL` on both sides ("the same drop … as a rise for it to think you're rising"). No new constant.
  2. **The `_radq` games-test** — a rise additionally needs a 12-game season above the old level; a decline has
     NO games test at all. → REMOVE `_radq` from the rise gate (the decline analog does not exist).
  3. **Cliff vs ramp** — fail either gate and the ENTIRE improvement is DELETED (hard step, "124 denied
     improvers ship at core==Lo"); the decline is a SMOOTH RAMP `sw=clip((drop-DOWN_TOL)/5,0,1)`. → give the
     rise the SAME smooth onset ramp.
Symmetric up-branch (RL_LSYM on): `if gap<=DOWN_TOL: return Lo; sw=clip((gap-DOWN_TOL)/5,0,1); return Lo + sw·s·gap`
(≡ `(1-sw)·Lo + sw·(Lo+s·gap)`). This mirrors the decline `Lo + sw·(Lc·agemult2 - Lo)` term-for-term: same
`DOWN_TOL` bar, same 5-pt onset ramp, `s=_S_AGE` the up-side form/age persistence fraction (the analog of
`agemult2`, kept — L-SYMMETRY corrects the BAR/RAMP/games-test, not the persistence fraction; the S_AGE fraction
is leg 3's territory). Continuous at `gap=DOWN_TOL` (sw=0→Lo). `RL_LSYM=0` ⇒ the hard `TOL_M1`+`_radq` step is
kept ⇒ byte-exact base. Interacts with leg 3 (both read `s=_S_AGE`) — measured in the additivity line.

## LEG 3 — THE S_AGE 29-TAIL (`RL_SAGE29`, default ON) — item 128 scope PRECISELY
`_S_AGE` interpolates `_L3_AX/_L3_AY`; today age-29 = **0.026915** (≈ the CSV's `sage_engine` 0.0269) while the
measurement (PR #88 `residual_by_age.csv`) puts the age-29 smoothed level at **+0.3793** (CI[0.208,0.534], ZERO
EXCLUDED). Wire ONLY the age-29 knot: `_L3_AY[29] : 0.026915 → 0.3793` behind `RL_SAGE29`. The fade reaches
zero AT 30 (age-30 knot 0.0 UNTOUCHED — the measurement validates the 30+ zero) and interpolation stays smooth
(piecewise-linear, continuous; 28=0.1506 → 29=0.3793 → 30=0.0, no discontinuity introduced). Do NOT touch
S_AGE anywhere else (one knot, one consumer `_est`). `RL_SAGE29=0` ⇒ age-29 knot 0.026915 ⇒ byte-exact base.
Implementation: keep `_L3_AY` as the base curve; `_S_AGE` reads a 29-swapped copy when `RL_SAGE29` on.

## Kill-switches (G-ATTR declared exceptions, default ON)
`RL_EO2`, `RL_LSYM`, `RL_SAGE29` — all default ON. All three = 0 together ⇒ board **`9a9889f8`** byte-exact
(prove: both md5s, per-player + export). Constants in-code (item 114); no `os.environ.get` on a board-changing
dial; config_sha256 UNMOVED.

## Measurement & acceptance (assert `acceptance_v1_13.json`, never prose)
- Boards (dump_board.py per #85/#89 house): base(all off), +EO2 only, +LSYM only, +SAGE29 only, all-on.
  Per-leg AFFECTED_ROWS (ablation per switch) + the additivity line `max|Σlegs − total|`.
- VALUE-FLOW (item 130, standing): ΣΔ, mover count, age-bucket delta distribution (≤22 / 23–26 / ≥27), the
  three largest cuts and three largest lifts BY NAME.
- Full ship-gates run on the candidate; LOG + SNAPSHOT `data/gates_snapshots/gates_<engine>.json` committed.
  G-COHORT July-8 construction regenerated: all three ratios + margins to 1.30. A-PAIRS scored (pair 3
  expected-fail; A9 per the owner's pending ruling — SCORED, never smoothed). PICK 1 = 3000. A8 Berry/Tsatas
  by name. Three narrowest margins.
- Named beneficiaries of the 29-tail: Heeney, Dale (item 127) base→new.
- Book RE-SEALED (reseal_book.py; store/config unchanged, head+stable_sha256 advance). expected_boot RE-PINNED
  (board + engine_head only; store/config untouched). Guard 5 fresh-bootstrap PASS; five SSI guards + Guard 5.

## Order
PLAN(commit) → leg 1 → leg 2 → leg 3 (each byte-exact-off checked) → boards+ablation+additivity → value-flow
→ ship-gates+snapshot → reseal+re-pin → Guard 5 fresh bootstrap → commit + push → RETURN (≤30 lines).

## Time
Band 1.5–3 h (three small, pattern-proven legs). No >2×/<½× flag anticipated; actual reported in RETURN.

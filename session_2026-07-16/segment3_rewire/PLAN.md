# PLAN — LEG B SEGMENT 3: THE v1.1 RE-WIRE (`RL_UNCOMP` at the production-value hook)

Build-session artifact (NOT a `docs/` pack doc — CORE: builds never author docs).
**Design of record (READ IN FULL, consumed):** `docs/MEMO_LEGB_functional_form_2026-07-16.md` **v1.1** — decisions (a)–(e) are settled; this segment IMPLEMENTS, it does not redesign.
Directive: `docs/DIRECTIVE_LEGB_segment3_rewire_v1_1_2026-07-16.md` (self-contained brief). Deliverable set + fence: `docs/DIRECTIVE_LEGB_uncompress_2026-07-16.md` (unchanged except where memo v1.1 ⟪v1.1⟫ supersedes: placement · ρ · captain · grid). Acceptance: `docs/acceptance_v1_18.json` (`leg_b.*`, grid {0.55,0.60,0.65,0.70}). Rulings: register items 221/224/225.
Branch **`claude/legb-segment3-v1-rewire-5jy7f3`** (harness-designated), based STRICT on the engine pin `c27d697` — the predecessor decompress lineage continued at its exact head (see §0 branch note).
**MODE: auto — PLAN first, then STOP (checkpoint).** This commit is the checkpoint artifact; HALT with the SHA after push; the owner pastes PROCEED after supervisor prescreen. Implementation does NOT run before PROCEED.

---

## 0 — GUARDS / BASE PINS (verified, recorded)

- **Engine/store base — STRICT ✓**: `git ls-remote … claude/legb-output-price-decompress-3vo8y1` = `c27d69788f92b125a63a2b57ff39fc9e75cdfbd0` == pinned `c27d697`. This working branch was created `-B` from that exact SHA. Identity at the base (`data/expected_boot.json`): board **`8d90c9ac`** · store **`b1fd0bce`** · config **`c2d233aec104…`** · rl_model **`f79fc740`** · engine_head pin **`a83c9f6d`** (the Leg-A landed state; the seg-2 map ships INERT so the board is byte-exact and the engine_head/rl_model pins were deliberately NOT re-stamped mid-candidate — Guard-5 HALTs the guarded wrapper, expected; dev-shell measurement bypasses it per the predecessor's `devbuild.sh`).
- **Docs base — at/after ✓**: `origin/main` = `94ec2d9` (≥ `62ab64d`). `git diff --name-only 62ab64d..origin/main` = **docs/-ONLY** (3 files). FEED docs FETCHED from `origin/main`, never merged into this branch.
- **Guard 5 / FENCE**: store `b1fd0bce` UNTOUCHED at the head (this job never writes the store). Config `c2d233ae` UNMOVED (`RL_UNCOMP` is a declared kill-switch, absent from `data/model_config.json`, not a manifest dial).
- **Branch note (SILENCE-IS-A-RED, owner decision at the checkpoint):** the directive says "CONTINUE this branch [decompress-3vo8y1] — never a sibling"; the harness mandates development on `claude/legb-segment3-v1-rewire-5jy7f3` and forbids pushing elsewhere without explicit permission. These conflict on the *push target*. I resolved to the harness branch **based on the exact decompress head `c27d697`** (the lineage is continued, not forked from main). If you want the work pushed to `claude/legb-output-price-decompress-3vo8y1` instead, say so at PROCEED and I re-point before implementing — nothing on decompress-3vo8y1 is disturbed by this PLAN.

## 1 — PRE-VIEW HASH MANIFEST (audit #16/#22/#45 · acceptance `leg_b.preview_hashes`; recorded BEFORE any candidate metric)

md5 **verified against my own fetch of `origin/main`** — MATCHES the FEED seals (the OPEN RE-SEAL, items 221/224):

| artifact | md5 (fetched) | FEED-required | bytes |
|---|---|---|---|
| `docs/MEMO_LEGB_functional_form_2026-07-16.md` (v1.1) | `c664062cf932ff1497e7b8fb19a2cd63` | `c664062c…` ✓ | 13707 |
| `docs/acceptance_v1_18.json` | `caf8636cdc63c649d57cff72d94eca02` | `caf8636c…` ✓ | 41928 |
| `docs/DIRECTIVE_LEGB_segment3_rewire_v1_1_2026-07-16.md` | `2b8609887e058a82d9cc36b8fa415e03` | (brief) | 5677 |

Any post-view mutation of the memo or acceptance JSON **HALTS the ladder**. This is the segment's pre-view seal.

## 0-CONFIRM — light re-run (directive item 0; register 223/224); evidence in `CONFIRM_measured.txt`

Frozen estimator (`fit_beta` = OLS ln(price)~ln(o) + 1000-boot percentile CI, seed 0), proven-27+ (age≥27, o>0), n=116:
- **β_c (ev vs o) = 0.6219** — memo expects ≈0.622 → **AGREES**.
- **λ_level_now (v1.0 ρ axis vs o) = 0.1236** — memo expects ≈0.124 → **AGREES**. (price6 vs o = 0.6107, item-224's 0.611 → AGREES.)
- **AGREEMENT LINE:** seg-2's committed table reproduces byte/value-exact on this seat's re-run; no divergence — seg-3's numbers govern regardless.
- **Re-wire premise (why v1.1 works), MEASURED:** the NEW ρ axis (realised-output ratio, §4) has **λ_ρ = 0.896 at the games≥10 floor** (CI [0.777, 1.009], includes 1.0) / **0.994 at games≥6** — versus level_now's 0.12. The target axis now tracks realised output; the blend can raise β. See §4 for the floor decision and its grid-headroom implication (**the checkpoint's key risk**).

## 2 — THE HOOK SITE (the exact file:line — memo §2 ⟪v1.1⟫ "the production-value hook, pr = price6, pre-pole-recovery")

**`engine/rl_after/_merged_recover.py:297–298`** — the core `raw_ev`:
```
297 def raw_ev(p,Y=2026):
298     pr=price6(p,b6(p,Y),Y); pr=_l2_blend(pr,p,Y)     # <-- THE HOOK. pr is the production-side board value.
...
307     return pr+w*recover(perf,par)*max(0.0,po-pr)     # pr feeds the pole-recovery term (pr is PRE-pole-recovery at :298)
```
The v1.1 map replaces the diagnostic `_l2_blend` call at **:298** with the production map `_uncomp_prod(pr,p,Y,bb)`, applied ONCE PER PLAYER at `pr = price6(…)`, before the pole-recovery composition at :307. This is the seg-3 diagnostic's exact construction (item 224). Byte-safety invariants preserved: the map returns `pr` unchanged for **synths / non-real players** (the ISO/pole warm-up at :320–335 and :322 calls `raw_ev` on synths — must stay byte-exact), for **RL_UNCOMP=0 / s unset**, and when **references are not yet built** (early load).

## 3 — THE MAP + THE CAPTAIN-OFF PASS (memo §2/§4 ⟪v1.1⟫)

Per real player, at the hook, with `bb = b6(p,Y)` computed once (captain-independent band prior; reused for both passes):
```
pr    = price6(p, bb, Y)                 # captain-INCLUSIVE production (map inert)  [pr(capt on)]
pr0   = price6(p, bb, Y)  under _CAPT_OFF # captain-FREE production (map inert)       [pr(capt off)]
delta = pr - pr0                         # the L-CAPTAIN increment, added back UNCHANGED
rho   = rho_out(p,pos) / RHO_DEN[pos]    # realised-output ratio (§4)
m     = rho_out(p,pos)                   # realised-output margin above REPL (avg-pts); ramp on m (§5)
w     = s * E * ramp(m)                  # E = 1-exp(-Eq/tau), tau=1.1 (saturating, w in [0,s]); w<=0 => return pr
v0p   = pr0**(1-w) * (V_ref_b[pos]*rho)**w    # log-space blend of the CAPTAIN-FREE production toward the output-proportional target
pr'   = C[pos]*v0p + delta               # production-side per-position renorm (§6); captain delta additive & nominal
```
**CAPTAIN-OFF PASS MECHANICS (the reviewable):** `capt_prem(lev)` (`rl_model.py:199`) is the single captain contributor to `price6` — it is folded into every `posval(lev+capt_prem(lev)−REPL)` argument via `v_at_peak → proj_from_peak / prod_floor`. (`capt_bonus`, `rl_model.py:363`, is DEAD — defined, never called on the production path; verified.) The captain-free pass is a module flag **`MA._CAPT_OFF`**: when set, `capt_prem` returns `0.0`; `price6` is recomputed under it → `pr0`. This is a true captain-free production value (NOT `RL_CAPT=0`, which is the *retired saturating* curve, not zero — `rl_model.py:187/200`). No recursion: `price6`/`v_at_peak` never call `raw_ev`, and the map lives only in `raw_ev`. Cost: one extra `price6` per real-player `raw_ev` call (bounded; memoizable per key if the build is slow). **Self-test (carried from seg-2):** `δ` byte-identical to the sum of the seg-2 per-site posval captain increments `Σ posval(lev+capt_prem−REPL) − posval(lev−REPL)` over a sampled captain set — L-CAPTAIN untouched by construction. English/Briggs measured captain-IN (δ rides in `pr'`).

## 4 — ρ CONSTRUCTION + THE QUALIFYING-SEASON GAMES FLOOR (the reviewable; memo §2.1 ⟪v1.1⟫)

- **`rho_out(p,pos)` = recent-2 QUALIFYING-season average points above `REPL[pos]`.** A qualifying season = `games ≥ FLOOR`; injury-wiped seasons (`games < FLOOR`) are **SKIPPED, never averaged in** (the Docherty cure by exclusion). Take the two most-recent qualifying seasons' `avg`, mean them, subtract `REPL[pos]`. **Zero qualifying seasons in window ⇒ w = 0** (map identity; the evidence weight already vanishes there).
- **Denominator `RHO_DEN[pos]`** = the positional **demonstrated-proven MEDIAN of the SAME measure** — median of `rho_out` over `{ p : gfut(p)==pos, _nqual(p,2026) ≥ PROVEN_N (=4), p in valuation scope }`. Built load-time.
- **`V_ref_b[pos]`** = the **median demonstrated-proven `pr0` (captain-free `price6`) per position** — the value scale. Built load-time (captain-free for dimensional consistency with the captain-free blend `pr0`; this is the v1.1 captain-consistent form of the diagnostic's median-`price6`).
- **THE FLOOR I DECLARE: `FLOOR = 10 games`** — the engine's canonical qualifying-season bar. Justification: (i) `_nqual` (`rl_model` via `_merged_recover.py:143`) *defines* a qualifying season as `games ≥ 10`, and the soft evidence bar centres there (`_EVW_Q0 = 11`, ~4-game ramp 9→13, `:180`); (ii) the demonstrated-proven population that forms `RHO_DEN` and `V_ref_b` is itself `_nqual ≥ 4` (≥4 seasons of games≥10), so numerator, denominator, and population share ONE qualifying convention — "the same measure"; (iii) against the frozen estimator's own o-construction (recent-2 *played* seasons, games>0, `calibrate.py:delivered`), the 10-game floor lifts the bar just enough to EXCLUDE injury-wiped seasons the raw games>0 estimator would fold in, while healthy proven-27+ seasons — the overwhelming majority — coincide with the estimator's o.
- **MEASURED λ trade-off (⚠ the checkpoint's key risk — owner ruling invited):** λ_ρ(games≥10) = **0.896** (CI [0.777, 1.009]); λ_ρ(games≥6) = **0.994**; games>0 = 1.0 (≡ estimator's o). The memo asserts "λ≈1 by construction" and sized the grid {0.55–0.70} on λ≈1 (⇒ saturated w≥~0.60). At the **10-game** floor the point estimate 0.896 predicts, by the memo's own β_eff=(1−w)β_c+w·λ_ρ, a saturated (s=0.70, E≈0.974 ⇒ w≈0.68) **β_eff ≈ 0.81 — below 0.85**, i.e. the grid could HALT empty; the CI including 1.0 leaves it genuinely uncertain, and **the frozen s-grid at implementation is the authority** (empty grid ⇒ HALT, do not extend — the rule stands). **The headroom lever is the floor:** `games≥6` (λ≈0.99) predicts β_eff≈0.87 and clears, at the cost of a softer injury-wipe exclusion (keeps 6–9-game seasons). **Recommendation: FLOOR=10** (faithful to the engine's qualifying convention and the memo's "reads his last two REAL seasons"), with `games≥6` offered as the explicit de-risking lever if you prefer to protect grid clearance. **Please rule the floor at PROCEED.**

## 5 — ONSET-RAMP WIDTH (memo §2.2; "at the bar in THIS measure's units, width declared")

The measure at the v1.1 hook is realised output above replacement (avg-points), so the ramp rides `m = rho_out(p,pos)`: **`ramp(m) = clip(m/Δ, 0, 1)`, `Δ = 6.0 avg-points` (DECLARED)** — carried from the seg-2 ratification (register 213), same units (avg-points above REPL), `≈2·S_SH` clears the softplus knee, matches the engine's ~5-unit smooth-onset idiom; no cliff between sub-bar and above-bar players (audit #28); no age gates (audit #29). w→0 continuously at/below the bar, so ρ≤0 is never exponentiated. Δ owner-tunable at this checkpoint.

## 6 — CONSERVATION: re-point the seg-2 C[pos] machinery at the new hook (memo §3)

Production-side, load-time, PER POSITION, across the whole population. **Re-point** (not delete) the seg-2 `_UNCOMP_C` renorm from the per-leg posval accumulator to the production-value hook: one load-time calibration pass over the valuation scope accumulates, per position, `Σ pr0` (pre-map captain-free production) and `Σ v0p` (blended); `C[pos] = Σ pr0 / Σ v0p` makes the position's TOTAL captain-free production unchanged by the map (an explicit per-position budget transfer across year-depths). NEVER per-(pos,year-depth) cell. Pedigree pedestals, iso premiums (`iso_eff`, applied AFTER `raw_ev` at `_prod_path:1160`) and the captain δ are **NOMINAL** — never renormed. The transfer is EXPLICIT in the whole-system SCAR ledger (players + held picks + adjustments; tolerances `abs 200` / `rel 0.0005`).

## 7 — KILL-SWITCH `RL_UNCOMP` (memo §6; the RL_ISOFADE pattern verbatim)

`_UNCOMP = os.environ.get('RL_UNCOMP','1')!='0'` — default ON; DECLARED kill-switch, NOT a manifest dial (config `c2d233ae` UNMOVED). Gates the **map + the load-time reference/`RHO_DEN`/`V_ref_b` build + the C[pos] renorm**. **`RL_UNCOMP=0` ⇒ board `8d90c9ac` BYTE-EXACT** — proven by a dev-shell A/B board build (OFF board built with no `RL_CONFIG_MODE` so the manifest reject-scan never sees the override). Regeneration matrix: `RL_UNCOMP × RL_ISOFADE` (all four) cold-regenerate and hash-equal runtime-switched output (memo §7 separability).

## 8 — THE s DIAL (memo §7; acceptance `leg_b.s_dial_selection` / `beta_proven27`)

FROZEN `fit_beta` (as §0-CONFIRM), unchanged method/sample/weighting/CI across every grid point; precision gates max-CI-width 0.35, min effective n 120. **Grid = {0.55, 0.60, 0.65, 0.70}** (acceptance v1.18). Sweep `RL_UNCOMP_S` in dev-shell, rebuild board/book per point, print β point+CI+eff-n + β_c (map OFF). **Selection: s = the SMALLEST grid value with β point ≥ 0.85.** **Empty grid ⇒ HALT-AND-ASK with the table (do NOT extend).** Selected `s` hard-coded as the canonical `UNCOMP_S_DEFAULT` literal.

## 9 — THE SEG-2 POSVAL-WIRING REMOVAL LIST (delete-don't-disable; obituary — it implemented a superseded design)

Restore each of the six sites to its **pre-seg-2 original** (the exact lines from base `e7cf9ba`, byte-verified; RL_UNCOMP=0 already proves these are byte-exact to the shipped board), delete the posval-level machinery, re-point the load-time block:

| # | file:line (c27d697) | remove | restore-to / disposition |
|---|---|---|---|
| 1,2 | `_merged_recover.py:759–761` | `_E=ctx.get('E',0.0)` + `MA.posval_uncomp(lev,g0,_E)` / `(lev,gg,_E)` | `base=lev+MA.capt_prem(lev)`; `MA.posval(base-MA.REPL[g0])` / `(base-MA.REPL[gg])` |
| 3 | `_merged_recover.py:783` | `MA.posval_uncomp(lev,g,ctx.get('E',0.0))` | `MA.posval(lev+MA.capt_prem(lev)-MA.REPL[g])` |
| 4,5 | `rl_model.py:408–410` | `_E=_UNCOMP_E['cur']` + `posval_uncomp(lev,g0,_E)` / `(lev,gg,_E)` | `base=lev+capt_prem(lev)`; `posval(base-REPL[g0])` / `(base-REPL[gg])` |
| 6 | `rl_model.py:422` | `posval_uncomp(lev,g,_UNCOMP_E['cur'])` | `posval(lev+capt_prem(lev)-REPL[g])` |
| def | `rl_model.py:337–360` | **delete** `posval_uncomp` (with obituary) | superseded by the production-value map (§3) |
| state | `rl_model.py:335–336` | **delete** `_UNCOMP_E`, `_UNCOMP_CAL` (per-leg threading) | not needed once-per-player |
| thread | `_merged_recover.py:861,863` | **delete** the `MA._UNCOMP_E['cur']=…` set/restore in the W4 `raw_ev` wrapper | — |
| load | `_merged_recover.py:1299–1337` | **re-point** the seg-2 L_ref(median level_now)/V_ref(posval)/C block | rebuild as the v1.1 production-value reference: `RHO_DEN` (median `rho_out`) + `V_ref_b` (median `pr0`) + C[pos] over the hook (§4/§6) |
| diag | `_merged_recover.py:276–296, :298, :1339–1362` | **delete** the item-221 diagnostic (`_L2S`/`_l2_blend`/`_L2_LREF`/`_L2_VREFB` + its ref build) | productionised into the `RL_UNCOMP` map (§3) — the diagnostic's job is discharged |

RETAINED in `rl_model.py` (the declared dial/switch, RL_ISOFADE-pattern): `_UNCOMP`, `UNCOMP_S`/`UNCOMP_S_DEFAULT`/`_uncs`, `UNCOMP_DELTA`, `UNCOMP_TAU`. The map + references + C move to `_merged_recover.py` (co-located with the hook, as the diagnostic already was). The `_coreM1 if not _EVW:` hygiene deletion (seg-2, committed `fdc83c5`) is already landed — NOT re-done.

## 10 — DELIVERABLES (the item-206 set; a return without its SHA is incomplete)

A/B identity (`RL_UNCOMP=0`==`8d90c9ac`) · frozen-suite: β_c + β(s) per grid point (est+CI+eff-n) · ≤22 slope vs 0.111 (min effect ≥0.15, CI clear) · English/Briggs captain-IN ≥1.75 · G-COHORT y4∧y5∧y6 ≤1.30 via `ship_gates_check._b1_july8` + committed row-level fixture · L-SMOOTH census at the declared threshold + boundary probes · census-v2 global gauge ≤+15,612 + predeclared cells · **whole-system SCAR ledger** (zero unexplained residual at tol) · **donor-side mover report** (top-30 proven markdowns: name·Δ·ρ·w·earned/prior) · **value-flow + R104.8 decomposition** · **w-export** (per-player-year: `stable_player_id,player,pos,year,leg,E,rho,w,ramp,earned,prior` — Leg D consumes it) · kill-switch regeneration matrix (RL_UNCOMP×RL_ISOFADE) · gate snapshot by engine hash · panel/self-tests (δ captain byte-identity; RL_UNCOMP=0 byte-exact; monotone onset ramp; zero-evidence identity).

## 11 — DERIVED-ARTIFACT REGENERATION (stamped, S1)

`bootstrap.sh`→`rl_export.py` (rebuild board)→re-pin `data/expected_boot.json` `engine_head`+`board`+`panel` in the engine-moving commit→`s4_matrix_M1v7.py` rebuild + G-BOOK re-seal (the map moved)→`run_panel.sh`/`PANEL_EXPECTED.txt` if any of the 10 named move→`ship_gates_check.py` GREEN. Store UNCHANGED `b1fd0bce` · config UNMOVED `c2d233ae` · `RL_PVCFIT` OFF (Leg D untouched).

## 12 — TIME

Segment 3 to this checkpoint: ~20 min (this commit), then HALT. After PROCEED: implementation + removal ~1–1.5 h · frozen-suite + s-selection ~1–1.5 h · deliverables (ledger/movers/decomp/w-export) ~1 h · return ~30 min = **2.5–4 h** (directive band; confirmed). Actual reported in the RETURN; flag if >2×/<½×.

## 13 — FENCE (self-check)

**IN:** `_merged_recover.py` (hook + references + C + kill-switch; sites 1–3 removal), `rl_model.py` (sites 4–6 removal + posval_uncomp delete + dial retention), the deliverable artifacts, derived-artifact regeneration (stamped). **OUT (touch = HALT):** the STORE `b1fd0bce` · `docs/` · `ui/` · the acceptance JSON · gate/guard code (`ship_gates_check.py`, `boot_guard.py`, `data/model_config.json`) · Leg A's τ · the pick curve. Scope growth = a NEW directive (S2).

## 14 — CHECKPOINT — OPEN DECISIONS FOR THE OWNER (paste PROCEED after ruling)

1. **The qualifying-games FLOOR (§4)** — declared **10**; measured λ_ρ(10)=0.896 vs (6)=0.994; grid-clearance headroom is the trade-off. Rule 10, or 6 (de-risk), or another value.
2. **Branch (§0 note)** — PLAN is on `claude/legb-segment3-v1-rewire-5jy7f3` (based `c27d697`); say if you want `claude/legb-output-price-decompress-3vo8y1` instead.
3. Ratify (or adjust): hook site `_merged_recover.py:298` · captain-off pass via `MA._CAPT_OFF` (capt_prem→0 recompute) · V_ref_b = median captain-free `pr0` · onset Δ=6.0 · the removal list.

Pre-view seal holds (memo `c664062c…` · acceptance `caf8636c…`). Base pins + FENCE unchanged; store untouched.

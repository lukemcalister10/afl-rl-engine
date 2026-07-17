# LEG C RELAY — PREFLIGHT FINDINGS (pre-wiring; §1b SITE HALT-AND-ASK)
date: 2026-07-17 · seat 10 · branch claude/legc-relay-dpp-law-10c4z7

## FIRST COMMANDS (item 270 standing law) — PASS
- git fetch origin claude/legb-selection-wire-s010-ho4vl8  -> 273463e
- git checkout -B claude/legc-relay-dpp-law-10c4z7 273463e
- git merge-base --is-ancestor 273463e HEAD  -> PASS (HEAD==273463e)
- store md5 b1fd0bce == pin. Docs (spec v1.3 §1b, corrected CSV Driscoll->100% MID / 90 blend rows)
  live on main 2089c3d; FETCHED as reference, never merged (docs/ is OUT).

## BASE SOUNDNESS
- 273463e reproduces board f2f077b2 (Leg-B default, RL_UNCOMP on) and 8d90c9ac (RL_UNCOMP=0) —
  proven by the Leg-B battery (session_2026-07-16/legb_selection_s010/out/s1_stamps.txt).
- KNOWN pending (not a blocker): 273463e carries STALE Leg-A pins in data/expected_boot.json
  (rl_model f79fc740, engine_head a83c9f6d, board 8d90c9ac) while its engine is Leg-B
  (rl_model.py 94b7016d, _merged_recover.py a0635745). Its own one_source_selftest Guard 5 is RED
  at base — the re-pin was deferred to the bake. Job 3 "expected_boot re-pin (same commit)" closes it.

## SITE MAP (verified by reading + empirical probe)
- futblend (years-1+ §1 blend): rl_model.py:45. IN FENCE. Content ref = quarantined 2b64630
  (+22 lines, clean). REACHES the board: v_at_peak (forward_valuation/distribution_pricing.py:250)
  calls proj_from_peak(g=gfut, g0=bnow, fut=futblend(p)); injecting a blend moved Petracca ev +65. OK.
- obsolete future==present guard: one_source_selftest.py:149-152. IN FENCE. Replace with flex-era
  invariants (future in vocab / <=1 alternate / blend params register-consistent). OK.
- fut-label defect: rl_export.py:169 'fut':[[gg,w] for gg,w in fb]; when REPL[alt]>=REPL[pri] the
  MAX-law low=pri drops the alternate label. Fix: board carries TRUE primary/alternate label; value
  keeps the low bar. IN FENCE (rl_export.py). OK.
- re-ingest (11 primary-future + 4-write rider + 90 blend rows + Driscoll correction): store writes
  to engine/rl_after/rl_model_data.json. IN FENCE. OK.

## THE BLOCKER — §1b YEAR-0 DPP SITE IS NOT IN THE THREE NAMED FILES
- §1b needs the year-0 (current-season) production leg to net a SEASON_PROG remainder against the
  LOWER of the post-collapse dual eligibility bars (banked part vs REPL[present]; remaining vs
  REPL[low]). The board's year-0 REPL bar IS keyed to present (g0=bnow) — GOOD — but for REAL
  players the production sum is computed by _proj_w4 (_merged_recover.py:787, the Leg-B W4 map),
  NOT rl_model.py's proj_from_peak (value()/player_raw are OFF the board path: 0 calls in ev()).
- val()=SCALE*r**0.85 is NONLINEAR, so the SEASON_PROG blend MUST happen before val() — i.e. inside
  the raw production sum. That forecloses any downstream (post-val) injection in rl_model/rl_export.
- Linearity identity (verified): because g0 affects ONLY the k==0 REPL term and Wk/k>=1/multipliers
  are identical, the §1b-adjusted raw production =
      SEASON_PROG * proj_from_peak(g0=present) + (1-SEASON_PROG) * proj_from_peak(g0=low)
  This is a clean 2-call blend BEFORE val — but its only correct home is v_at_peak
  (distribution_pricing.py) or inside _proj_w4 (_merged_recover.py). NEITHER is one of the three
  named IN-fence engine files (rl_model.py / one_source_selftest.py / rl_export.py).

## OPTIONS (owner decision required)
A. Authorize §1b in v_at_peak (forward_valuation/distribution_pricing.py): the 2-call SEASON_PROG
   blend, RL_FLEX-gated, byte-exact at RL_FLEX=0. Touches NO Leg-B dial/constant. Cleanest+correct;
   needs the fence to extend to this 4th file.  [RECOMMENDED]
B. Authorize the §1b k==0 split directly in _proj_w4 (_merged_recover.py) — explicitly "Leg-B's map"
   (FENCE-OUT); needs a named waiver.
C. §1b in rl_model.py proj_from_peak only — a NO-OP on the shipped board (real players use _proj_w4);
   the "+§1b year-0 DPP" attribution would be all-zeros = false. NOT acceptable.
D. Treat §1b board-siting as scope growth -> a new directive (S2).

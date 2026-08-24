# PREREG — WILL GRAHAM DUAL-STREAM CORRECTION (p_dual 90 → 40), 2026-08-24

**Owner word, verbatim (2026-08-24):** "Can we please edit Will Graham to be a 40% only SF then in
the store and recalculate?"

**Context on the record (register v835):** the dual-position MAX law (LEG C, item 275) projects
Graham on his PRIMARY (MID) and swaps the years-1+ replacement bar to the LOWER of {MID, SF} on the
p_dual fraction. At p_dual=90 the measured dual benefit was +490.5 ev (+43.7%). The owner ruled the
store's 90% SF split down to 40%.

## THE EDIT (one field, one row, surgical bytes)
`engine/rl_after/rl_model_data.json`, row `will-graham`: `"p_dual_stream": 90` → `40`. No other byte
of the store moves. The store is the ONE SOURCE (law 1); the owner's word is the authority for an
owner-supplied data field.

## PREDICTIONS (all measured on a scratch build BEFORE this file was committed; emit transcript
`PREDICT_emit.log`, scratch root under the session scratchpad)
- store md5: `daa93053bc2d4eba30d9dc6e06e4af9e` → `fb640ca0baf92bbb122b1ad7e25c5a88`
- board md5: `6fd0f7ded2b280d1a90962c299a152e3` → `82fcd8bb1e552b927299b5702122e321`
- movers: EXACTLY ONE — `will-graham` 1533 → 1271 (−262). Board fut label becomes [MID 0.6, SF 0.4].
- pool: 700,119 → 699,857 (−262; the removed dual-bar benefit, no renormaliser).
- day-0 sitters: 86/86 byte-unmoved (Graham is not in the cohort).
- balanced sibling: rebuilds and reconciles (its md5 moves with the board).
- byte-unmoved: engine_head, rl_model, fv, config, register, v0surf, band, q97m, as_of_round.

## FALSIFIERS
- The lander asserts the predicted board identity BYTE-EXACT at build_proofs; a second mover, or a
  different Graham value, is an abort, not a footnote.
- Any store byte outside the will-graham row moving fails the surgical-edit claim (md5 is the check).
- kill_switch: none declared — the revert is `git revert` of the flip commit (a data edit, not a dial).

## SEQUENCING NOTE
This act lands BEFORE the design arm is commissioned: the rebake trains on the FINAL store (scope
§5.6), which after this landing is fb640ca0. ARM 1 (store-alone, register v834/v835) remains the
staleness report against daa93053 — its purpose is served and it is not re-run.

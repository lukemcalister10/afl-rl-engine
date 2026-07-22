# MEMO — LEG F ADDENDUM v1.2 · 2026-07-18 · amends v1.0/v1.1 (§2.vii added)
### Grounds: the F4 checkpoint (item 356) — the mid/vet forward decline is ~2× realized (an
### L-SYMMETRY breach), driven by two AGE_REF reads inside the production price (`raw_ev`'s
### `pr=price6(b6)`): the `_dev_advance` AGE_CURVE roll consumption (veteran-dominant;
### neutralization restores MID+VET to 1.01× of realized backward) and the demonstrated-level
### band `b6` read; a 6–7% level drop levers ~4× through `v_at_peak`'s `posval(level−REPL)`
### nonlinearity into a 23–28% price drop.

## §2.vii — THE L-SYMMETRY DAMPER (forward-lens-gated; the F3 `_form_anchor_clock` pattern)
A wrapper in `_merged_recover.py` at the CONSUMPTION of the two production-price age reads —
never editing the `_dev_advance` roll itself (its source is HARD-OUT) and never touching the
`v_at_peak` leverage — that tempers the forward AGE_REF advance to the SAME players'
**MEASURED realized backward-transition rate**, taken from the committed −2/−1/now boards (F2
artifacts, by stamp).

THE LAW OF THE RATE (what keeps this a measurement, not a fudge):
1. The rate is measured PER AGE-TRANSITION at the finest resolution the sample supports,
   SMOOTHED (rule 7) — a single pooled scalar only if the data supports no more, DECLARED.
2. The measurement is committed and **SEALED BEFORE any forward render** (the §6 pattern). It is
   never iterated against the backtest total — one measurement, one seal, then the acceptance
   run tells the truth.
3. Forward-only, `RL_LEGF`-gated, k=0-INERT BY CONSTRUCTION; the k=0 dormancy suite EXTENDS to
   the new sites. The backward (−1/−2) artifacts are untouched.
4. No new lens-only growth/decay free parameter (Reid): the damper's only content is the
   measured realized rate. No cohort hand-tuning. F3's cures are the floor (gradient stays
   un-inverted).
5. If the honestly-measured rate does not bring the backtests inside ±5%: HALT AND RETURN — the
   ±5% expectation itself then goes to the OWNER (only he re-rules it).

## THE FENCE GRANT (F4, post-checkpoint)
IN: `_merged_recover.py` LIMITED to the `:287-288` band-read wrapper + the `:820-821`/`:851`
`level_now` consumption wrapper · `session_2026-07-18/legf4/`. HARD-OUT unchanged and absolute:
`rl_model.py` (incl. `_dev_advance` :361) · `distribution_pricing.py` (`v_at_peak`/`price6`) ·
the V0/`_iso_dec` chain `:1121-1171` · the store · the curve · pins/acceptance · `docs/` · ui ·
SEASON_PROG.

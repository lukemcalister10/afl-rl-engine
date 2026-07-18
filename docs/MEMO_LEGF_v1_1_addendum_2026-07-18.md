# MEMO — LEG F ADDENDUM v1.1 · 2026-07-18 · amends MEMO_LEGF v1.0 (§2.iii replaced; §2.vi added)
### Grounds: the item-352 calibration verdict (backtest −30% undershoot; developing cohort −33.3%,
### the inverted gradient; pedigree strip = 36.7% of it; the discrete exit rule mislabels 155
### developing players as retirees). Both changes implement ALREADY-RULED law or the owner's
### item-351 construction — no new doctrine.

## §2.iii (REPLACED) — DISTRIBUTED RETIREMENT LIABILITY (owner-worded, item 351; measured
## superior: aggregate 32,836 ≈ F1's 32,338 while naming no false retirees)
No named exits. At +k, each age-eligible player carries a probability-weighted retirement
haircut h(p) = P(retire | age(p), +k) · vP(p), with P measured from RECORDED historical exit
rates by age (smoothed per rule 7, no wide bins; strawman sealed pre-render, [OWNER] at the
viewing). Phantom intake sizes to the aggregate liability (expected exits ⇒ expected slots).

## §2.vi (NEW) — PROJECTION COMPLIANCE FOR PEDIGREE-ANCHORED ROWS (this is R103.3 / memo-LEGE §2
## honoured, not new law: "the SAME un-compressed map at the projected evidence state")
A zero/low-evidence young player is priced TODAY on the pedigree blend (the Leg-D V0 = curve
entry anchor). His PROJECTED evidence state at +1 is still pedigree-dominant — one more year of
thin production does not erase draft pedigree. The forward lens therefore carries the SAME
pedigree/evidence blend at the advanced state, pedigree weight decaying only as projected
evidence accrues (smooth, no cliff). Defect sites (item-352 addresses): `rl_model.py::
proj_from_peak` (lp·frac, elite-gated runway) · form anchor `rl_export.py:96` · exit bar
`rl_export.py:~526` (superseded by §2.iii).

## THE ACCEPTANCE FOR THE FIX BUILD (F3)
(1) THE BACKTEST: F2's −1 board projected forward reproduces "now" 752,427 within ±5% league
total (and −2→−1 similarly). (2) THE GRADIENT UN-INVERTS: per-cohort signed means order
developing ≥ mid ≥ veteran (developing holds/rises). (3) k=0 balanced `06d8af60` byte-exact ·
RL_LEGF=0 chain byte-exact · store `968de0c7` untouched — all single-thread (item 349). The
owner views the numbers at the viewing regardless; nothing here amends a frozen gate.

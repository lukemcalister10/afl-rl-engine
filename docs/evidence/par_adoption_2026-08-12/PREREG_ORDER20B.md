# PRE-REGISTRATION — ORDER 20B, ADOPTION EVIDENCE FOR THE PAR ARM-SPLIT

**Committed BEFORE any measurement is run.** Branch `build/par-adoption-evidence`, cut from `origin/main`
`9ecc4e9`. Issue #334, order comment 5260713967.

Scope reminder, so the predictions are read against the right thing: **this order measures only.** No
shipped default changes, no board is promoted, `data/expected_boot.json` is not restamped.

Subject: the ORDER 20 arm-split fix on `engine/forward_valuation/par_build.py` + `par_redesign.py`
(branch `build/nd-pool-separation`, PR #457, `78d5c38`).

---

## 0. THE MECHANISM I EXPECT, DECLARED UP FRONT (so the predictions are falsifiable, not post-hoc)

Read off the code before measuring, from `_merged_recover.py` and `par_redesign.py`:

1. **`_v0_uncapped(p) = raw_ev(p, debutyr(p)-1) * iso_eff(p, debutyr(p)-1)`** (`:1233`).
2. At `Y = debutyr-1` a real player has **no scoring rows in range**, so `_ev_qual = 0` (`:212`).
   - `_ev_pw(0) = 0` (`:297`, `gate = Eq²/(Eq²+GK²)`), so the **`_ev_pw` pedigree-par blend leg
     (`:590`) contributes EXACTLY ZERO to v0.**
   - `_expgate` at zero exposure with `_ev_est(0)=0` gives `w = wage·tfade·expgate = 0`, so the
     **pedigree pole term `w·recover(perf,par)·max(0,po−pr)` in `raw_ev` (`:464/:475`) is ZERO at v0** —
     the engine asserts this itself in its own comment at `:465` ("V0-INERT BY CONSTRUCTION").
   - `iso_eff` at `Eq=0` returns `base` **unfaded** (`:507`).
3. Therefore the **only** par channel that can reach v0 is the **V0 pick-surface synthetic table `ISO`
   built at `:497`**, `raw=raw_ev(synth(pk, PR.par_at(pos,min(pk,KMAX),4), pos))` over `PICKS=1..70`,
   isotonised and (with `_ISOFADE`) monotonised into a multiplier `fs`.
4. `cp.KMAX = 70` and `MA.POOL_PICK = 65`. So **grid points 65..70 of the ISO synthetic loop route to
   the POOL arm under the fix** — six of seventy points swap to a differently-fitted surface — and
   isotonic regression + multiplier monotonisation are **global** operators, so a deep-end change can
   propagate to shallow picks.
5. `par_redesign.BASE_RATE` / `shortfall()` / `tilt_band()` are referenced **only** inside
   `par_redesign.py`'s `if __name__=='__main__'` report block. Repo-wide grep finds no other consumer.

## 1. PREDICTIONS

### v0 (Task 1)

- **P1.** v0 moves for national rows under the fix: **≥ 1 in 4 national rows** show a non-zero
  `v0_start` delta.
- **P2 (the sharp one).** Because the pole and the `_ev_pw` leg are both zero-weight at v0, the v0 delta
  ratio `v0_uncapped_FIX / v0_uncapped_HEAD` is a **pure function of (position, effective pick)** — i.e.
  within a (pos, effpk) cell, **every** row shows the *same* ratio to within 1e-9. Falsified if any
  (pos, effpk) cell shows two different ratios.
- **P3.** The ratio in P2 equals **`iso_corr_FIX(pos,pk) / iso_corr_HEAD(pos,pk)`** to within 1e-9 — i.e.
  the ISO table at `:497` is the *whole* v0 channel and `price6`/`b6` carry none of it.
- **P4 (KPD verdict, the owner's question).** KPD v0s **do NOT uniformly go backwards**. I predict the
  KPD v0 delta has **mixed sign across picks** (the isotonic re-fit is a reshape, not a level shift),
  and specifically that **shallow KPD picks (1-10) move by less than 3% in absolute terms**.
- **P5.** The **pool arm's** v0s move by **more** in mean absolute percentage than the national arm's.

### Gates (Task 2)

- **P6.** `_v0_curve_assert`'s D14a (`cross_draft_maxdisp`) stays at **exactly 0.0** under the fix.
  Rationale: v0 on the board path is read off the **frozen D14 `_V0CURVE_META` surface**, which is a
  function of (pos, draft-age, pick) by construction and does not depend on par at all.
- **P7.** D14b (`within_cell_inversions`) stays at **0** under the fix, for the same reason.
- **P8.** D14c (`kpp_depth_monotone`) stays **True** — `_R_surf` is a frozen 24-knot literal
  (`:1123`), par-independent.
- **P9.** `_ruc_prior_cap` binding: the **set of RUCK rows on which the cap binds does not grow** under
  the fix (binding count FIX ≤ binding count HEAD + 2).
- **P10.** **No D14 gate flips red.** If any does, I report it as a BLOCKER without rationalisation.

### `nd_profile` (Task 3)

- **P11.** Recomputing `nd_profile` on a **fixed-engine-emitted** matrix under arm-split strata gives a
  value that **differs from the published 0.9944115616**, because the published figure used HEAD v0s in
  the denominator `Σv0` and the fallback rows' numerators.
- **P12.** The difference is **small relative to the −3.02% headline**: **|Δ| < 0.5%** of the profile.
  Rationale: the v0-side moves ~0.3% on the board and the strata side is the dominant term.
- **P13.** The **final adoption-basis `nd_profile` stays below 1.0** (i.e. the sign flip relative to
  break-even that ORDER 20 reported survives being recomputed at fixed-engine v0s).

### Per-mover decomposition (Tasks 4-5)

- **P14.** For **every** decomposed mover, the **`BASE_RATE` channel contributes EXACTLY 0.0** to the
  price delta — because it has no board consumer at all. If this is false my §0.5 reading is wrong and
  I say so.
- **P15 (Dean).** Harry Dean (pick 3 KPD, −8.5%) — his move comes **NOT** from `BASE_RATE` (P14) and
  **NOT** from a pick-3 kernel move. I predict the dominant channel is the **ISO/V0-synthetic surface
  (`:497`) via v0**, together with the **pick-independent `ramp_shr` shift**, and that the two together
  account for **≥ 70%** of his delta.
- **P16 (Clarke/Johnston).** Angus Clarke (pick 39 SD, −18.4%) and Harvey Johnston (pick 49 SD, +46.9%)
  are driven by **different channels**, not by the same channel with different signs. Specifically I
  predict Johnston's positive move is dominated by the **stalled-prospect bar** (`pr = bestlvl/par` at
  `:2263`) — a *lower* par raises `pr`, releasing the stall cap — and Clarke's negative move is
  dominated by a **different** channel (the `_ev_pw` prior leg and/or v0).
- **P17.** The per-cell surface direction for **deep SD cells (picks 39-49) is DOWN** under the fix
  (national par falls when pool rows are removed), which is the seat's explanation (b)'s premise. I
  predict **explanation (b) is directionally right on the cells and (a) is wrong**, but that **neither
  is a complete account** because both ignore the v0/ISO channel.
- **P18.** At least **one** decomposed mover has an **inactive** dominant consumer under the engine's
  own gating (e.g. `_ev_pw` weight ≈ 0 because he has no qualifying season), which means at least one
  channel that a naive story would invoke is **provably not firing** for him.
- **P19.** The channel contributions **do not sum to the total delta**: the residual (interaction /
  non-linearity between channels) is **non-zero for at least one mover and exceeds 5% of his delta**.
  Decomposition by one-at-a-time switching is not additive and I will not present it as if it were.

### Reproduction / pins

- **P20.** The three pins are UNMOVED at entry and at exit: board `94f1fec59f99c59d5890d5975c79fa9b`,
  store `d9a24282357cf3083b1640466e3ecd83`, instrument `noarb_table_338.py`
  `0f8220351c64c56ccfa90c60edcdfa5f`.
- **P21.** My in-process `ev(p,2026)` harness reproduces ORDER 20's committed board `v` values for the
  named movers **exactly** on both HEAD-par and fixed-par, so the decomposition is anchored to the same
  board the owner is deciding about. Falsified if any named mover's reproduced before/after differs
  from `BOARD_DELTA_par_armsplit.json`.

---

## 2. WHAT WOULD MAKE ME STOP AND REPORT A BLOCKER

- any `_v0_curve_assert` gate red under the fix (P10);
- `_ruc_prior_cap` binding on rows where it did not bind before, in a way that moves v0;
- failure to reproduce the pins (P20) or the committed board values (P21).

## 3. INSTRUMENTS THIS ORDER WILL USE, NAMED IN ADVANCE

- `scripts/stage_fix.py` — stages ORDER 20's two changed files into a scratchpad tree copy. The checkout
  is never edited.
- `scripts/v0_delta.py` — v0 for all rows, both arms, HEAD vs FIX.
- `scripts/gates_fixed.py` — `_v0_curve_assert` + `_ruc_prior_cap` binding on the fixed engine.
- `scripts/channel_decomp.py` — per-mover per-channel switching.
- ORDER 20's own `separation/nd_profile_test.py` (imported, not re-derived) for Task 3.

Population statements accompany every figure. No figure is reported without naming its instrument and
its population.

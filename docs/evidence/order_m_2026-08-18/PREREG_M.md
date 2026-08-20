# PREREG M — ETA SET TO ZERO. DOES A LEGAL BOARD STILL EXIST?

**Seat:** ORDER M, the test seat. **Date:** 2026-08-18.
**Base:** ORDER K's tree, board `f3101883a60b0a7b8cb50f9d8a5abfff`. **Landing candidate:** `1f176444`.
**This file is pushed before the first engine run of this order.** Nothing below is edited afterwards.
Any change is an amendment, dated, with its reason, and the original left standing.

**Nothing here is adopted. Nothing lands on this seat's word.**

---

## 0 · WHAT THE OWNER RULED, AND WHAT THIS SEAT IS TESTING

The counterweight has two halves.

**Half one is KAPPA.** It moves weight off a player's draft pedigree and onto the production he has
actually shown. It reads his performance. It is performance-conditional.

**Half two is ETA.** Engine `_merged_recover.py` lines 3769-3770:

```
if _O32S>=6 and O32_ETA>0.0 and _g>0.0:
    _pi *= max(0.0, 1.0 - O32_ETA*((_g/O32_GAMMA_D)*_math.exp(1.0-_g/O32_GAMMA_D)))
```

`_g` is games played. That is the only input. There is no performance term. The charge peaks at
`GAMMA_D = 14` games and fades away on either side. A player who is producing far above his age bar
and a player who is producing far below it are charged exactly the same, if they have played the same
number of games.

**The measured consequence, on ORDER K's own board f3101883:**

| row | age bar lift | counterweight | net | reads |
|---|---:|---:|---:|---:|
| harry-dean (producing ABOVE his age bar) | **+221** | **−218** | **+3** | 2,403 |
| cooper-duff-tytler | +85 | −152 | **−67** | 1,505 (BELOW the landing candidate's 1,572) |
| isaac-kako (36 games, past the peak) | — | −24 | **+44** | — |

The owner's ruling: a feature meant to reward players performing ahead of expectation must not punish
them. **ETA IS TO BE SET TO ZERO.** This seat does not re-litigate that. It tests whether the board
still obeys the owner's laws once eta is gone.

---

## 1 · THE SEARCH — AXES, FIXED THINGS, AND THE GRID

### 1.1 · Fixed, and not touched by this order

- `eta = 0.0` — **pinned by the owner's ruling. Not an axis.**
- `gamma_d` — with eta = 0 it multiplies nothing. It is reported as inert, never swept.
- the owner-ruled tall/small sitter factor (R-TALLFACTOR, adopted)
- ORDER K's re-sited fade-floor fix (`RL_O36_FLOORFIX` default on)
- ORDER D's pick-curve sitter fade, and every dial below it in the stack
- the engine tree itself: this order changes **no engine line**. It moves declared dials only.

### 1.2 · The free axes

| axis | env var | grid |
|---|---|---|
| S1 age-bar dose | `RL_O36_LAM_S1` | 0.00, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70, 0.85, 1.00 |
| kappa | `RL_O36_KAPPA` | 0.15, 0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60 |
| gamma_u | `RL_O36_GAMMA` | 8, 10, 11, 12, 14, 16 |
| lambda_rel | `RL_O36_LAMBDA` | 0.80, 0.90, 1.00, 1.08, 1.20, 1.30 |

The dose grid is the set of doses ORDER I's leg extract holds. It is not re-cut, because re-cutting it
means a fresh engine leg extraction and this order reuses ORDER K's and ORDER J's machinery rather
than rebuilding it.

**The main axis is the dose.** ETA was what paid for the dose. With eta gone the dose has no payer, so
the expectation is that the dose must fall.

### 1.3 · The navigation instrument, and what it may and may not decide

ORDER J's `o37_sweep.py`, reused whole with `eta` pinned to `[0.0]`. It is arithmetic over ORDER I's
precomputed legs. **It navigates. It decides nothing.** Every number the owner reads comes off a BUILT
board and the standing extended-338 instrument. This is the same separation ORDER J and ORDER K used,
and the same warning applies: the calibrator runs hotter on the young bands than the standing
instrument does.

Two controls must reproduce before the sweep is believed, exactly as ORDER J asserted them:
- the corrected age-fair surface reproduces `REMIX_32R.json` to 1e-9
- the landing-candidate control reads class 1.0421

---

## 2 · THE ACCEPTANCE THRESHOLDS — THE OWNER'S LAWS, AND NOTHING ELSE

These are the only optimisation targets. No diagnostic (slope, W, SSE, the vantage matrix, the band
spreads) is optimised toward. Where a diagnostic is a **ruled constraint** inherited from an earlier
order it is reported as a constraint and its status stated, never chased.

| # | law | rail | reported on |
|---|---|---|---|
| **G1** | the year-1 class cohort grows | ≥ **1.03**, strictly < **1.14** | **THE REGISTERED BASIS: the W2 scorer, draft classes 2005-2015, `ENTRY_FLOOR = 2005`.** ORDER K reads **1.0513** there. The cohort-window reading (ok_class.py, cohort 2005-2015, ORDER K 1.0324) is a DIFFERENT WINDOW, off by one year at both ends (ORDER L). Both are printed. The floor is scored on the registered basis. |
| **G2** | picks 31-40 and 41-64 materially improve vs ORDER K | > 0 points of improvement | every band reported, both windows. Both are expected to stay negative — a known limitation, not a failure of this order |
| **G3** | no ND band and no pool arm above +14% year 0→1 | +14% | both windows. SSP's inherited breach (+52.71% on ORDER K) is reported separately and never masked |
| **G4** | picks 1-10 stay near ORDER K's **+8.22%** | the owner rejected a setting that cut them | primary window; modern window also printed (ORDER K +13.65%) |
| **G5** | **harry-dean ≈ 2,600 · cooper-duff-tytler ≈ 1,800** | their Candidate-31 levels, the owner's stated reference | board points, on the built decision board |
| **G6** | sub-expectation-with-games rows do not rise | ≤ 0 vs the landing candidate | xavier-taylor, daniel-annable, dylan-patterson, by name, with directions |
| **G7** | josh-smillie holds his ruled ~700s | 700 ≤ v < 800 | board points |
| **G8** | mature rows untouched by the age bar | exactly 0 of 429, store-wide | S1's zero-tolerance law |
| **G9** | day-0 entry values bit-identical | 89 / 89 on `derived_v0` | the printed day-0 of a sitter regenerates by construction and is disclosed, as in ORDER D/J/K |
| **G10** | determinism ×2 | byte equality | two identical builds of the decision board |
| **G11** | dial identities | byte-exact | dial-off = `1f176444`; ORDER K's own setting rebuilds to `f3101883` |
| **G12** | continuity | monotone / no cliff | age, games, pick; rho32 monotone and < 1 |

**Inherited ruled constraints, reported not chased:** rho32 monotone; the ruled at-bar continuity
object; max single class ≤ 1.139 (the 1.14 no-arb line); W inside the corrected hindsight 90% CI
[0.3117, 0.5560]; slope in [0.885, 1.115]; J-TOL on the veteran pool (per-row min(25, 0.5%), churn
≤ 0.15% of the board, net ≤ 0.10%).

---

## 3 · THE TENSION THIS SEAT EXPECTS, STATED BEFORE IT IS MEASURED

**ETA IS THE MECHANISM THAT CHARGES THE G6 ROWS.** Xavier Taylor, Daniel Annable and Dylan Patterson
are all below their age bar with games on the board. On ORDER K they are charged by eta. Remove eta
and that charge is gone.

And it is worse than "the ORDER K addition is undone". **The landing candidate `1f176444` already
carries eta at 0.41.** Setting eta to zero therefore removes a charge the base board was already
levying. So the G6 rows can rise **at every dose, including dose 0**.

Kappa is the only remaining charge. Kappa moves weight off pedigree onto shown production, so on a row
whose shown production is below his bar it does bite in the right direction. **This seat's prior is
that kappa alone is too weak to hold these three rows down, and that G6 will be breached.** If that is
what the numbers say, it is reported with its size and the plain sentence that kappa alone cannot
charge them. It is not traded away and it is not rounded away.

---

## 4 · NAMED-ROW PREDICTIONS, WRITTEN BEFORE THE FIRST BUILD

Scored on the built decision board, in board points, against the landing candidate `1f176444`.

| row | landing | ORDER K | ORDER M prediction | reasoning |
|---|---:|---:|---|---|
| **harry-dean** | 2,400 | 2,403 | **UP, into 2,550-2,700** | his eta charge was the largest of any named row; removing it releases essentially all of it |
| **cooper-duff-tytler** | 1,572 | 1,505 | **UP, into 1,620-1,780 — SHORT of 1,800** | his S1 lift is only +85 at dose 0.40 and the dose must fall; releasing eta cannot manufacture the missing pedigree |
| **isaac-kako** | — | +44 | UP, by more than +44 | he was charged −24 by a bump he had already walked past |
| **xavier-taylor** | 1,176 | 1,162 | **RISES — G6 breach** | eta was his charge |
| **daniel-annable** | 1,530 | 1,537 | **RISES, by more than the +7 ORDER K already breached by** | eta was his charge |
| **dylan-patterson** | 1,467 | 1,440 | **RISES — G6 breach** | eta was his charge |
| **josh-smillie** | 772 | 772 | **772, unchanged** | the floor fix is untouched and he has no games channel here |
| **will-green / toby-conway / william-mccabe / alex-dodson** | — | +141 / +86 / +70 / +16 | relief retained in full | the tall factor is fixed and unchanged |
| **murphy-reid, noah-mraz, logan-morris, levi-ashcroft, colby-mckercher** | — | large rises | rise further | they are the age bar's own winners and lose their eta charge too |
| **milan-murdock** (26) | — | −14 | moves toward 0 | the eta charge on a mature row is removed |

**Band and class predictions:**

| quantity | ORDER K | ORDER M prediction |
|---|---:|---|
| G1 class, registered basis (W2 draft 05-15) | 1.0513 | **RISES above 1.0513** at any dose ORDER K's dose is held at; the binding question is whether the dose has to fall far enough to give it back |
| picks 1-10 (primary) | +8.22% | 7.5% to 9.5% |
| picks 11-20 (primary) | +11.16% | 10% to 13% |
| picks 21-30 (primary) | +5.26% | 4% to 7% |
| picks 31-40 (primary) | −10.70% | −12% to −9% |
| picks 41-64 (primary) | −6.89% | −8% to −6% |
| ALL 1-64 (modern) | −0.96% SELL-RED | still SELL-RED, between −3% and +1% |
| picks 21-30 (modern) | −14.26% | still SELL-RED |
| max single class | 1.1363 | **RISES; this seat expects the 1.139 line to be the first thing that breaks as the dose is held up** |

---

## 5 · THE FALSIFIERS — WHAT MAKES THIS ORDER WRONG

| # | falsifier | fires if |
|---|---|---|
| **M1** | the dial-off identity | the dial-off rebuild is not `1f176444` byte-exact |
| **M2** | ORDER K reproducibility | ORDER K's own setting does not rebuild to `f3101883` byte-exact |
| **M3** | determinism | two identical builds of the decision board differ |
| **M4** | S1's mature law | any of the 429 mature rows moves on the age-bar leg |
| **M5** | day-0 | `derived_v0` is not bit-identical on 89 of 89 |
| **M6** | the sweep instrument | the corrected-surface control or the landing-candidate control does not reproduce |
| **M7** | the eta claim itself | eta at zero does **not** materially raise harry-dean — which would mean the diagnosis in §0 was wrong |
| **M8** | continuity | any continuity or monotonicity object breaks |

---

## 6 · THE TWO OUTCOMES, DECLARED IN ADVANCE

Both are reportable results. Neither is a failure of the seat.

**(a) A legal setting exists.** Build it. Run the full standing acceptance suite. Produce the three
owner documents — the player list, the year-1 class with v0, and the no-arb tables in the standing
format (both windows, pool arms, comparison columns for ORDER K / the landing candidate / candidate
31) — each carrying the "what is in this board and what is still broken" box.

**(b) No legal setting exists at any dose.** Then the blind half is load-bearing, and the age bar
cannot ship in its current form. Say so. Quantify it: **what breaks first, and at what dose.** Show
the trade-off curve so the owner can choose knowingly.

**This seat will not declare (a) by relaxing a law, and will not declare (b) without having swept the
whole declared grid.**

---

## 7 · DISCIPLINE

- `export PATH="/root/rl_venv312/bin:$PATH"`
- every numeric and engine run carries `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
  NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1`
- engine runs are **strictly sequential** — never two at once
- staging is PID-unique by the tag discipline: one tag, one directory, one run
- evidence lands in `docs/evidence/order_m_2026-08-18/`
- push-per-step, explicit refspec `git push origin HEAD:land/order-29`, fetch and rebase before every
  push

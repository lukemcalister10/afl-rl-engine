# THE SEASON-CONSTANT CENSUS

**Seat:** INDEPENDENT AUDIT (read-only). **Date:** 2026-08-19. **Branch:** `land/order-29`.
**No engine edit. No dial. No board built. Nothing adopted.**

**The owner's question, restated:** the engine treats a full season as ~22-23 games. Between injury,
suspension and rest, ~18 is a realistic full season. A 15-game player was probably selected for
nearly everything he was available for — not 65% of it. The measured layers already know this. **Do
the legacy layers?**

**Method.** Every site was found by exhaustive grep over `engine/rl_after/*.py` (52 files) and
`engine/forward_valuation/*.py` (8 files), then read in context. Every constant quoted below was
parsed straight out of the source at the line named. The pure functions were re-implemented here so
the reading does not depend on the engine's own reporting. Nothing is skipped: sites that turn out to
be inert are listed as inert, with the proof.

---

# THE ONE-PAGE ANSWER

**Mostly the 22-norm is harmless, and for a specific and satisfying reason: at the two places that
look most like a season normalisation, the constant CANCELS ALGEBRAICALLY. It is not doing any work.
The engine's real bars are absolute games bars — 6, 10, 14, 22 — and a 14-18 game season clears every
one of them.**

**But there is one genuine exception, it is live on the delivered board, and it is exactly the object
the owner's intuition points at.**

### The exception

`lti_register.py:117` computes the lost-season fraction as

```
L = 1 - min(games_2026 / 22, 1)
```

That is a true games-over-season-length participation ratio. It feeds two live things: the
present-production haircut on the board (`avail_hc`), and the young-credit clock advance. **I
confirmed it is live: 41 of the 43 register rows carry an `avail_hc` on the delivered board exactly
equal to the L this formula produces.**

On this store cut it bites on **22 rows**. A row who played 15 games and was then registered out is
booked as having lost **31.8%** of a season. On the owner's 18-game reading he lost **16.7%**. The
haircut is close to double. A 14-game row is booked at 36.4% lost against 22.2%.

**Direction:** the 22-norm makes the lost-production haircut too big, so these players are priced too
LOW. An 18-rebase would raise them.

### Everything else

- **The two `/SEASON` divisions cancel.** `_playable(p,Y) = SEASON × (seasons_elapsed + fE)`, and it
  is consumed only as `_playable(p,Y)/SEASON`. That ratio is identically `seasons_elapsed + fE` for
  **any** value of SEASON. I checked it at 18, 22, 23 and 26 — same numbers. Changing 22 to 18 there
  changes nothing at all.
- **The real bars are absolute games bars, and 14-18 clears all of them.** 6 = is the season readable.
  10 = is it delivered. 14 = does the level count fully. 22 = does the pole gate open. Of the 104
  rows in the 14-18 band in the last completed season, **104 of 104 clear the 6-bar, the 10-bar and
  the 14-bar.** Not one is treated as a partial participant by any bar.
- **The 22-bar is not a season bar.** `POLE_RAMP=22` is measured against *recency-weighted career*
  games. A steady 15-game-a-year player clears it in his second season.
- **The level-trust ramp is already 14.** `LEVEL_RAMP` defaults to 14 games — closer to the owner's
  reading than to 22, and more generous than either.
- **The measured layers do the real work, and they agree with the owner.** The F1 credit curve is at
  **full presence from 11 games** — a 14, 15 or 18-game season already counts as a whole season, not
  64%/68%/82%. A(g) is at 88% of its 22-game value by 15 games. The only layer still climbing is
  `rho31`, and its own scale constant is **29.19 games** — longer than any season — because it is a
  career-evidence curve, not a completeness ratio.

### The house has already used 14 as a full season

`_m1_calib.py:14` and `_m1_refine.py:8` both set `G_FULL=14` and select "full" seasons with
`games >= G_FULL`. Those are standalone calibration scripts, not live — but they show the house's own
working convention for a full season has been **14**, while `lti_register.py` says **22**. **Two
files in the same engine disagree about what a full season is by eight games.**

### Recommendation in one line

**One site is worth a rebase and it is `lti_register.py:117`.** Everything else is either
algebraically inert, already at 14, a label on a frozen fitted object, or superseded by the measured
layers. There is no case for a global 22→18 sweep, and one clear case for a single-line question to
the owner.

---

# THE FULL SITE LIST

Verdict key: **LEAVE** (correct or fit-absorbed) · **CANDIDATE** (for an 18-rebase) ·
**SUPERSEDED** (the measured layers already do this) · **INERT** (constant does no work) ·
**DEAD** (unreachable on the board path).

## Group A — sites that use the season-length constant itself

| # | site | what it computes, for whom | label or live? | mispricing? | verdict |
|---|---|---|---|---|---|
| A1 | `lti_register.py:117` `L = 1 - min(g26/G_FULL,1)` | the lost-season fraction for every availability-register row; feeds the board's `avail_hc` present haircut and the clock advance | **LIVE normalisation, rebasable** | **YES — 22 rows today; a 15-game row is booked at 31.8% lost vs 16.7% on an 18-norm; prices them too LOW** | **CANDIDATE** |
| A2 | `_merged_recover.py:1380` `g += L*cp.SEASON` | LTI clock advance: ages the young-credit clock by the games he is expected to have lost. Identity: `L*SEASON == SEASON − g26`, i.e. it adds exactly "the games he would have played" | LIVE, rebasable | **YES, same population** — adds 4 phantom games too many per row if 18 is the true season; 21 register rows are still under the G0=46 completion bar where it bites | **CANDIDATE (rides A1)** |
| A3 | `_merged_recover.py:135` `_playable = cp.SEASON*(elapsed+fE)` | full-season-equivalent games playable since debut | **INERT — see A4** | no | **INERT** |
| A4 | `_merged_recover.py:302` `POLE_RAMP*min(1,_playable/cp.SEASON)` | the pole/recovery exposure gate | **cp.SEASON CANCELS**: `_playable/cp.SEASON ≡ elapsed+fE` at any SEASON. The live bar is `POLE_RAMP=22` on *recency-weighted career* games, cleared by a 15-game-a-year player in season 2 | no | **LEAVE** |
| A5 | `conditional_prior.py:111` `_playable_fse = SEASON*(elapsed+fE)` | the FV twin of A3 | **INERT — see A6** | no | **INERT** |
| A6 | `conditional_prior.py:117` `LEVEL_RAMP*min(1,_playable_fse/SEASON)` | the reliability shrink on demonstrated level | **SEASON CANCELS**. The live bar is `LEVEL_RAMP`, default **14** — already at the owner's reading | no | **LEAVE — already 14** |
| A7 | `_merged_recover.py:3359` `_k = cp.SEASON/12` in `pv_games` | grosses an MSD entry season (max 12 games, ruling 5) to a full-season equivalent on the games axis that `sigma30bp` and `rho31` read | LIVE, rebasable | measured: **39 MSD rows** would move. An 18-rebase gives *fewer* effective games → σ +0.0245 (more pedigree), ρ −0.0187 (less production) — it pushes MSD rows **toward their draft pedigree**, the opposite of the owner's intent | **LEAVE** (rebasing hurts here) |
| A8 | `_merged_recover.py:5585` `assert LTIREG.G_FULL==cp.SEASON` | one-constant discipline guard | guard only | no | **LEAVE** (but it is the guard that would force A1 and A2 to move together — useful) |
| A9 | `build_peak_model_v4.py:28,51` `w=min(g,SEASON)/SEASON` | season-completeness weight on the TARGET when the peak model is TRAINED | **LABEL on a fitted object** — the board consumes the frozen pickle (`RL_V0SURF_PKL`) and `pvc_snapshot.json`; `fwd_peak` is called only inside the trainer | no, unless refit | **LEAVE — fit-absorbed** (changing it forces a full peak-model refit + PVC snapshot regeneration) |
| A10 | `distribution_pricing.py:34,54` same weight | the same completeness weight in the band-target trainer | **LABEL on a fitted object**; `fwd_peak` called only at line 99, train-time | no, unless refit | **LEAVE — fit-absorbed** |

## Group B — `SEASON_PROG` (a CALENDAR fraction, not a games norm)

`SEASON_PROG` = `calendar_progress` = 0.58 at this cut. It answers "how much of the season has
elapsed", which is a different object from "how many games is a full season". Rebasing the season
length does not touch it.

| # | site | what it computes | verdict |
|---|---|---|---|
| B1 | `rl_model.py:1822` definition (dynamic, from `data/season_state.json`) | the calendar fraction | **LEAVE** |
| B2 | `rl_model.py:1188` / `_merged_recover.py:1320` / `distribution_pricing.py:277` `sp=SEASON_PROG` | §1b dual-bar split: the banked `sp` share nets vs the present bar, the remaining `1−sp` vs the lower bar | **LEAVE** — calendar, not games |
| B3 | `rl_model.py:1826` `elapsed=clamp((s−1)+SEASON_PROG,0,1.6)` inside `debut_factor` | seasons of opportunity so far | **LEAVE** |
| B4 | `rl_model.py:1828` `clamp((22−cg)/22,0,1)` inside `debut_factor` | fades the positive debut signal as a real career sample accrues. LIVE (reached via `unpl_eq`, `rl_model.py:1883`) but only for **pickless** rows (86 on the board), and it is a *career*-games fade, not a season-participation ratio | **LEAVE** (career-sample bar; an 18-rebase would make it fade faster, which is not what the owner is asking for) |
| B5 | `rl_model.py:2022` `+ (g_2026 / SEASON_PROG)` in `P_estab` | the mid-season games gross-up | **DEAD** — `P_HOOK=None` (`rl_model.py:2027`) and the board writes `'P':1.0` frozen (`rl_export.py:350`). Reachable only via `compute.py`, a diagnostic |
| B6 | `rl_model.py:2025` `(1−SEASON_PROG)*max(0,prior−base)` | mid-season benefit-of-doubt, same dead function | **DEAD** |
| B7 | `par_redesign.py:40,156` `CUR_ROUNDS=round(SEASON_PROG*22)` | print label in a standalone mock | **DEAD** (mock; "the board/book path never reads PAR_RAMPS") |

## Group C — the absolute games bars (the ones that actually decide things)

The engine's own comment at `_merged_recover.py:106-109` enumerates them: **"every games bar
(6/10/14/22) prorates to season progress for the IN-PROGRESS season"**. They are absolute games
counts, prorated only by the *calendar* fraction `fE`. **Season length does not enter any of them.**

| # | bar | site(s) | what it asks | 14-18 game season |
|---|---|---|---|---|
| C1 | **6** | `nseas_pro` (`:1436`), `bestlvl` (`:1584`), `current_qual` (`:2753`) | is the season readable at all | **clears — 104/104** |
| C2 | **10** | `o32_delivered` (`:3620`), the R3 run reset (`:4133`) | is the season DELIVERED (games ≥ 10·fE **and** avg ≥ gate bar) | **clears on the games leg — 104/104** |
| C3 | **14** | `LEVEL_RAMP` (`conditional_prior.py:108`) | does the demonstrated level count FULLY | **clears — 104/104**; already the owner's number |
| C4 | **22** | `POLE_RAMP` (`_merged_recover.py:103`) | does the pole/recovery gate open fully — on **recency-weighted career** games | cleared by season 2 at 15 games/yr |
| C5 | **12** | `G_ADQ` | proven-player recent-adequacy window; **deliberately NOT prorated**, and the code says so | **LEAVE** |

**Verdict on the whole group: LEAVE.** None is a `games/SEASON` ratio. The owner's worry — that a
15-game player is scored as a 65% participant — does not happen at any bar.

## Group D — the measured layers (for comparison; they are the answer, not the problem)

All three are functions of **raw games** with no season length anywhere in them.

| layer | form | 11g | 14g | 15g | 18g | 22g |
|---|---|---:|---:|---:|---:|---:|
| F1 credit (presence) | measured isotonic knots | **1.000** | **1.000** | **1.000** | **1.000** | 1.000 |
| A(g) conviction | `1 − exp(−g/9.89)` | 0.671 | 0.757 | 0.781 | 0.838 | 0.892 |
| `rho31` reliability | `1 − exp(−(g/29.19)^0.8015)` + remix | 0.519 | 0.559 | 0.570 | 0.598 | 0.629 |

Half-conviction on A(g) lands at **6.86 games**, which is the owner's "~7". The credit curve is at
full presence from **11**. **SUPERSEDED — these layers already treat a 14-18 game season as a whole
season, exactly as the owner says they should.**

`rho31` is the one still climbing at 15-18 (91-95% of its 22-game reading). But its own scale is
29.19 games — *longer* than a season — so it is measuring career evidence accumulation, not season
completeness. Rebasing a season constant would not touch it; only a refit would, and that refit would
have to be earned on out-of-sample error, not on a convention.

## Group E — inert, dead or out of scope, listed so nothing is silently skipped

| # | site | why it is not a finding |
|---|---|---|
| E1 | `_m1_calib.py:14`, `_m1_refine.py:8` `G_FULL=14` | standalone calibration scripts, imported by nothing. **Named anyway because they are the house's own precedent for calling 14 a full season** — and they disagree with `lti_register.py`'s 22 |
| E2 | `s4_matrix_M1v7_blend.py:63` `G_FULL=44.0` | a two-season evidence ramp, self-labelled `PLACEHOLDER, nothing baked` |
| E3 | `tail_restore.py:13` `RAMP=22.0` | namespace spine; the module "owns NO valuation code" and `RAMP` is overwritten at `bind()` |
| E4 | `par_redesign.py:44` `PAR_RAMPS=22`, `:100,158` `games/22` | standalone mock; its own comment: "nothing wired into engine `value()`… the board/book path never reads PAR_RAMPS" |
| E5 | `_merged_recover.py:1094` `g(m)=clip((m−6)/22,0,1)` | `m` is `Lc − REPL[pos]`, a **points** quantity. The 22 is a points scale, not games |
| E6 | `rl_model.py:961,990` "the 22/23 shelf" | an **age** ladder (ages 22 and 23), not games |
| E7 | `SIGMA30BP_TAU=23.0` (`:3335`) | a fitted career-games decay constant that happens to be near 23; not a season norm, and it is a measured fit |
| E8 | `_ycred_games` G0 = 46 (`:1359`) | census-derived ("median cumulative games end-y3=37 / end-y4=54"), a career bar, not a season norm |
| E9 | `EXPO_DEN=11.0`, `EXPO_F=0.545` (`conditional_prior.py:81-87`) | the in-progress decay-clock pace. `EXPO_DEN=11` is an on-pace floor derived from a zero-collateral study, not a season length. Note it is **already at 11**, consistent with the measured layers |

---

# WHAT WOULD BREAK IF SITE A1/A2 WERE REBASED

Stated so the owner sees the cost, not just the benefit. **This seat is not proposing the change —
it is pricing the question.**

1. **The `G_FULL == cp.SEASON` assertion at `_merged_recover.py:5585` would fire.** That guard exists
   to keep one constant in one place. Rebasing only the LTI side breaks it. Either the assertion is
   re-scoped (LTI's "realistic full season" is a genuinely different object from the FV pipelines'
   "reference full home-and-away", which is what `build_peak_model_v4.py:28` calls its 22), or both
   move and A7/A9/A10 come with it — and A7 moves in the wrong direction while A9/A10 force refits.
2. **My reading is that they are two different objects and should be two constants.** The FV trainers
   want a *reference* season length for a completeness weight on a fitted target. The LTI register
   wants a *realistic* season length to say how much production a player actually lost. Calling both
   22 is what made them one constant; it is not obvious they should be.
3. **No refit is required for A1/A2 alone.** L is a live arithmetic on store games, not a label on a
   fitted surface. That is what makes it rebasable where A9/A10 are not.
4. **Size is bounded and directional.** 22 rows move, all upward, and the second consumer (the clock
   advance) moves the same 21-of-43 rows still under the G0=46 bar upward too. I have not built a
   board, so I am not quoting board points — that would need a dial this seat has no licence to add.

---

# WHAT I COULD NOT VERIFY

1. **Board-point size of an 18-rebase at A1/A2.** There is no dial for the season constant, and this
   seat does not add one. The row-level fractions are measured and published above; the price effect
   is not.
2. **Whether the FV fitted surfaces would improve or degrade under a refit at 18.** `min(g,22)/22` is
   baked into the frozen peak-model pickle and `pvc_snapshot.json`. Answering it means a refit and an
   out-of-sample comparison, which is an order, not a census.
3. **Whether the owner intends the LTI haircut to read "lost vs a realistic season" or "lost vs the
   full fixture".** Both are defensible; they are different questions. The census establishes that
   the code currently answers the second one, on 22 live rows.

---

# FILES

| file | what it is |
|---|---|
| `cen_season.py` / `CENSUS_SEASON_MEASURE_out.txt` | the measured layers re-implemented; the cancellation test at SEASON = 18/22/23/26; the exposure-is-a-career-quantity table |
| `cen_sites.py` / `CENSUS_SEASON_SITES_out.txt` | sites A7 (MSD scaler) and A2 (clock advance) sized row by row |
| `cen_bars.py` / `CENSUS_SEASON_BARS_out.txt` | the 6/10/14/22 bars against every 2025 season row |
| `cen_lti.py` / `CENSUS_SEASON_LTI_out.txt` | site A1, with the board confirmation that 41 of 43 `avail_hc` values equal the formula's L |

**Conventions:** plain speech · no named-player targets (rows appear as consequences, by store key) ·
nulls as nulls · no site skipped silently — inert and dead sites are listed with the proof that they
are inert or dead · every constant parsed from the source at the line named.

**NOTHING WAS EDITED, ADOPTED OR BUILT. READ-ONLY THROUGHOUT.**

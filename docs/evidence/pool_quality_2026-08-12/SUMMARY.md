# ORDER 24B — SUMMARY, AND EVERY PRE-REGISTERED PREDICTION SCORED

Issue #334, ORDER 24B. Branch `build/pool-quality`, cut from `origin/build/pool-dial` @ `254d2e5`.
Brief: comment [5266656676](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5266656676).
Pre-registration: `PREREG_ORDER24B.md`, committed at `1be42ae` **before** any par was computed, any
`q` was formed, any U″ was derived and any engine line was edited. It has not been edited since.

> **levels frozen at #469 values; absolute prices ±few points, MSD up to ~5%; re-trued at landing**

---

## 1. What was done

| step | result |
|---|---|
| **STEP 0 — PREREG** | Committed first. Seven of the supervising seat's expectations (S1–S7) recorded verbatim; twenty-three of my own (B1–B23) on top, including the whole par table I expected to measure. |
| **STEP 1 — CONTROL** | α=1.0 board rebuilt on the unmodified branch: **`ca3544d8df9272db191a67001a1bb9e4`**, byte-identical to ORDER 24's recorded a100. **PASSES.** |
| **STEP 2 — THE PAR TABLE** | Playing par by pathway × depth from the same complete-window harvest that produced `R` (1,390 national rows excluded at the gate, zero present, asserted). K=10 shrink, ORDER 22's form verbatim, every one of 60 cells disclosed with its `n`. `PAR_TABLE.md`. |
| **STEP 3 — THE RULE** | `M = (1−φ)·R + φ·(1 + q·(U″−1))`, `q = clip(avg/par(pathway,d), 0, 1)`. `_pr_mult` extended; both call sites unchanged and still `_pool`-gated. The harvest gains `avg_y`. |
| **STEP 4 — U″** | Re-derived per pathway. Mean preservation prints `1.0000000000` on all 10 rows. The identity `U″−1 = (U′−1)/qbar`, computed independently, residualises to `2.220e-16` — floating-point exact. Control (q≡1) reproduces ORDER 24's U′ to `4.6e-11`. `UPRIME2_TABLE.md`. |
| **STEP 5 — ONE ψ BOARD** | **`e2bf7347e07c08f1efbdda17d6601e4e`**, built twice from scratch in separate throwaway worktrees, identical both times. **0 ND movers.** |
| **STEP 6 — THE TABLE** | `MOVERS_TABLE_PSI.md` / `.json`, 152 rows, seven price columns, the eight named rows flagged. `Q_TABLE.md`: all 188 currently-playing pool rows with games, avg, par, q, φ, a100 and ψ. |

**No blockers, no halts.** Every instrument that could have stopped the build was run and passed on
its own terms.

---

## 2. Board identities

| column | board | md5 |
|---|---|---|
| `pre_act` | main @ `7f4d5d2` | `94f1fec59f99c59d5890d5975c79fa9b` |
| `live` | `origin/main` today | `1dbd1480a34c7823f330273211cbb76a` |
| `pr469` | committed on `land/pool-update` / this branch | `665311ca72576df6ff0bbf6dfd007739` |
| `a025` | ORDER 24, α = 0.25 | `322df660ccce6c017ded341403b7215f` |
| `a050` | ORDER 24, α = 0.50 | `87214d5653e0fb8e48b804f1a890b6bc` |
| `a100` | ORDER 24, α = 1.00 — this order’s control | `ca3544d8df9272db191a67001a1bb9e4` |
| **`psi`** | **ORDER 24B, the quality-conditioned premium** | **`e2bf7347e07c08f1efbdda17d6601e4e`** |

All six prior boards are **pinned by md5 in `o24b_table.py`**, which raises if any of them is not
the recorded artifact. The ψ surface artifact is `e3491b66ff5fd3ad31fa9d210ef0cf95`.

**What did not move, on every build including the control:** `config bf012105` · `rl_model e5eb5e44`
· `curve_artifact 07b7109f`. Only `engine_head` differs (`e832856e` control → `c327c2b1` ψ), which
is the pool block and nothing else.

---

## 3. The separation law

| check | a100 | psi |
|---|---:|---:|
| national rows on the board (`ty==ND`, pick ≤ 64) | 561 | 561 |
| **ND movers vs live `1dbd1480`** | **0** | **0** |
| ND rows absent | 0 | 0 |
| ND board value (live: 620,877) | 620,877 | 620,877 |
| delisted `back` rows moved, of which non-pool | 12 / **0** | 12 / **0** |

`o24b_table.py` asserts this and **raises before it writes anything at all** — the Q table, the
movers table and the JSON are every one of them downstream of the assertion.

---

## 4. Every prediction scored

**The supervising seat's seven presented expectations: all seven HELD.**

| # | expectation | verdict | measured |
|---|---|---|---|
| **S1** | `harrison-ramm` ≈ 540 ± 30 | **HELD** | **567** (top edge of the band) |
| **S2** | `luker-kentfield` ≈ 420 ± 30 | **HELD** | **449** (top edge of the band) |
| **S3** | `vigo-visentini` ≈ 185 ± 5, slightly **UP** vs a100's 182 | **HELD** | **183**, up +1 |
| **S4** | `mani-liddy` 168 **EXACT** | **HELD** | **168**, byte-identical to a100 |
| **S5** | `U″(MSD)` ≈ 2.1 | **HELD** | **2.004494** — 4.5% below 2.1, inside "≈" |
| **S6** | pool total within ~1% of a100's 132,734 | **HELD** | **132,342**, -0.30% |
| **S7** | ND movers 0 | **HELD** | **0** |

**My own twenty-three: seventeen held, six breached.** The breaches are owned by number below;
nothing in `PREREG_ORDER24B.md` has been edited.

| # | prediction | verdict | measured |
|---|---|---|---|
| **B1** | control rebuild == `ca3544d8…` | **HELD** | `ca3544d8df9272db191a67001a1bb9e4` |
| **B2** | 0 ND movers on the ψ board | **HELD** | 0 |
| **B3** | mean preservation `1.0000000000`, all 10 rows | **HELD** | 10/10 |
| **B4** | `U″ ≥ U′` on every pathway, without exception | **HELD** | 10/10, ratios 1.0877–1.1939 |
| **B5** | `qbar ∈ [0.65, 0.92]` for every pathway | **BREACHED** | 9 of 10 inside; **SSP = 0.9194**, above the band |
| **B6** | only partial participants move `a100 → ψ` | **HELD** | 146 full + 55 sitters byte-identical; **0 movers outside the 42** |
| **B7** | direction decided by `q` vs `qbar`, on every one of the 42 | **HELD** | **0 violations**; 9 rows flat at integer rounding |
| **B8** | movers in [24, 40]; ≥18 down; ≤16 up | **HELD** | **33** (26 down, 7 up) |
| **B9** | my 16 predicted par cells within ±5%% | **BREACHED** | **7 of 16** inside (MSD 3/4 · RD 3/4 · SSP 1/4 · ND>64 0/4) |
| **B10** | par rises monotonically d1→d4 on every pathway | **BREACHED** | **2 of 9** (RD, UNR) — and ALL POOL |
| **B11a** | my four reconciliation cells within 5% of the seat's | **HELD** | -3.41% · +1.76% · +0.96% · -2.69% |
| **B11b** | the seat's `n` are games, reproduced within 10%% | **BREACHED** | RD d3 only (−6.9%%); MSD d1 40 vs 162, MSD d2 41 vs 174, SSP d1 134 vs 166 |
| **B12** | `U″(MSD) ∈ [2.00, 2.25]` | **HELD** | **2.004494** |
| **B13** | U″ pathway ordering identical to U′ | **HELD** | rank-identical, all nine |
| **B14** | `harrison-ramm` 563, band [530, 600] | **HELD** | **567** |
| **B15** | `luker-kentfield` 446, band [415, 480] | **HELD** | **449** |
| **B16** | `vigo-visentini` 184, band [180, 190], UP | **HELD** | **183**, up |
| **B17** | `mani-liddy` 168 · `robert-hansen` 143 · `nicholas-martin` 3513, all EXACT | **HELD** | 168 · 143 · 3513 |
| **B18** | `marcus-herbert` 906 · `jai-newcombe` 4883, EXACT | **HELD** | 906 · 4883 |
| **B19** | ≥20 of my 24 named riser calls correct | **HELD** | **24 / 24** |
| **B20** | largest faller is ramm or kentfield; largest riser is francou / riley / van-wyk | **BREACHED** (first limb) | largest faller **`caleb-lewis` -91**; largest riser `oliver-francou` +11 (second limb held) |
| **B21** | ψ pool total in [131,300, 132,900] and below 132,734 | **HELD** | **132,342** |
| **B22** | table carries [140, 175] rows | **HELD** | **152** |
| **B23** | ψ board deterministic | **HELD** | same md5 twice |

### The breaches, owned

**B9 and B10 — I predicted the par table as a smooth, gently rising, roughly pathway-independent
surface. It is nothing of the sort, and the reason is a population fact I should have checked before
predicting rather than after.** The complete-window harvest (`Y ≤ 2021`) is dominated by the rookie
draft: RD carries 1,698 playing cells and 21,326 games, while **MSD carries 14 cells and 121 games**,
PDN 15, PDS 26, SSP 23. The mid-season draft only begins in 2019, so almost no MSD career has a
complete window at all. Consequently:

- **RD and ALL POOL rise smoothly and monotonically** (RD 60.36 → 75.72 across d1→d6) — those are
  the cells with a real sample, and my prediction was right in shape and close in level there (3/4).
- **The thin pathways are essentially their own donor.** MSD's d4–d6 cells are *empty*, so par there
  is exactly the MSD all-depth donor, 61.70, flat by construction. SSP's d4–d6 likewise. My predicted
  rise through the deep cells could not happen, and every one of those predictions failed.
- **`PDA` d2 measures an own par of 30.39 on 15 cells** — the lowest cell in the table by a distance,
  shrunk to 40.56. It is disclosed, not smoothed away.

I predicted the shape of a population I had not sized. That is the breach, and it is mine.

**B11b — I guessed the wrong reconciliation.** I predicted the supervising seat's `n` were games
rather than cells, and that my games totals would reproduce them within 10%. That is true for
`RD d3` (2,679 vs 2,878) and false for the other three. **The real difference is the window
convention, and it is worth the seat's attention**: the seat's cut reads *entry classes* ≤ 2021 and
follows them to the present; this order's harvest gate reads *cell years* ≤ 2021. For a pathway that
has existed for decades the two barely differ. For MSD, which begins in 2019, they differ by an order
of magnitude — the seat sees 162 MSD d1 rows, this harvest sees 9. **The par values still agree**:
all four of my wired cells land within 5% of the seat's, because the shrink pulls the thin cells
toward a donor that is itself a reasonable estimate of the same quantity. The order said reconcile
and explain, not force — so I have explained it and changed nothing.

**B5 — SSP's q-mass ratio is 0.9194, four thousandths above the top of my band.** Cause: SSP's
complete-window population is 23 playing cells whose averages sit close to their own par (which is
mostly the SSP donor), so very little q-mass is lost. A marginal miss on a band I set too tight for a
thin cell; the direction of the prediction was right.

**B20 — I named the wrong largest faller.** I reasoned from the *size of the a100 lift* rather than
from the *depth of the quality shortfall*. `caleb-lewis` plays 2 games at **12.50** — a q of 0.2001, by some
distance the lowest quality among the reachable rows — and he falls 349 → **258**, more than
`harrison-ramm`'s 53. The lever is quality, not price, and my prediction was still reading price.
That is exactly the habit this order exists to break, and I had it too.

---

## 5. What the fix does, in one reading

| board | pool total | vs live | moved vs live | moved vs `pr469` | **moved vs `a100`** |
|---|---:|---:|---:|---:|---:|
| `pre_act` | 123,243 | -1,923 | 119 | 205 | **204** |
| `live` | 125,166 | 0 | 0 | 117 | **118** |
| `pr469` | 132,960 | 7,794 | 117 | 0 | **44** |
| `a025` | 135,583 | 10,417 | 119 | 89 | **89** |
| `a050` | 134,590 | 9,424 | 119 | 89 | **89** |
| `a100` | 132,734 | 7,568 | 118 | 44 | **0** |
| **`psi`** | **132,342** | **7,176** | 118 | 44 | **33** |

| cell (243 pool rows) | n | moved `a100` → `psi` |
|---|---:|---:|
| full participants, `φ = 1` — anchor share **exactly 0** | 146 | **0** |
| **partial participants, `0 < φ < 1`** | **42** | **33** (26 down, 7 up) |
| current sitters, `φ = 0` — `M = R`, no premium leg | 55 | **0** |

**Movers outside the partial cell: 0.** That is arithmetic, not luck. A sitter reads `R` and never
touches `U″`. A full participant carries an anchor share of exactly zero, so no multiplier of any
kind reaches his price. **ψ reaches exactly one population: pool players who are playing, but not
yet playing a full load — the population whose price is still being set by an assumption rather
than by a record.**

### Who moved a100 → ψ, and why

`M_ψ − M_a100 = φ·(U′−1)·(q/qbar − 1)`. **Price does not enter the decision; quality does.** A
partial whose 2026 average is above his pathway's q-mass ratio times par **rises**; below it,
**falls**. Verified on all 42 partials: **zero violations**.

| player | pathway | avg26 | par | q | a100 → ψ |
|---|---|---:|---:|---:|---|
| `caleb-lewis` | MSD | 12.50 | 62.48 | 0.2001 | 349 → **258** (-91) |
| `jacob-newton` | MSD | 27.70 | 62.48 | 0.4434 | 377 → **320** (-57) |
| `harrison-ramm` | MSD | 28.75 | 62.48 | 0.4602 | 620 → **567** (-53) |
| `luker-kentfield` | MSD | 32.33 | 62.81 | 0.5147 | 496 → **449** (-47) |
| `max-ramsden` | MSD | 40.50 | 61.70 | 0.6564 | 321 → **292** (-29) |
| `noah-howes` | MSD | 32.00 | 62.48 | 0.5122 | 282 → **255** (-27) |
| `oliver-francou` | MSD | 71.50 | 56.89 | **1.0000** | 590 → **601** (+11) |
| `jaxon-artemis` | MSD | 54.25 | 56.89 | 0.9536 | 536 → **542** (+6) |
| `flynn-riley` | MSD | 80.00 | 56.89 | **1.0000** | 428 → **434** (+6) |
| `alex-van-wyk` | MSD | 69.00 | 56.89 | **1.0000** | 427 → **433** (+6) |
| `jordan-boyd` | MSD | 66.00 | 61.70 | **1.0000** | 62 → **65** (+3) |

9 partials did not move at all: deep careers (`adam-saad`, `jack-hutchinson`, `lachie-sullivan`, `liam-reidy`, `matt-guelfi`, `matt-owies`, `mitchell-hinge`, `peter-ladhams`, `reilly-o-brien`)
whose evidence fade has all but extinguished the anchor leg, so the multiplier change is invisible
at integer rounding. That is the design working, not an exception.

**The eight named rows:**

| player | g26 | avg26 | q | φ | pre_act | live | pr469 | a025 | a050 | a100 | **psi** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `mani-liddy` | 0 | — | 0 | **0** | 128 | 128 | 1025 | 285 | 238 | 168 | **168** |
| `robert-hansen` | 0 | — | 0 | **0** | 80 | 80 | 650 | 215 | 190 | 143 | **143** |
| `nicholas-martin` | 0 | — | 0 | **0** | 2828 | 2822 | 3520 | 3517 | 3515 | 3513 | **3513** |
| `marcus-herbert` | 8 | 88.87 | **1.000** | **1** | 1053 | 906 | 906 | 906 | 906 | 906 | **906** |
| `jai-newcombe` | 21 | 103.15 | **1.000** | **1** | 4887 | 4883 | 4883 | 4883 | 4883 | 4883 | **4883** |
| `harrison-ramm` | 4 | 28.75 | **0.460** | **0.724638** | 320 | 351 | 406 | 555 | 578 | 620 | **567** |
| `luker-kentfield` | 3 | 32.33 | **0.515** | **0.543478** | 179 | 178 | 268 | 454 | 468 | 496 | **449** |
| `vigo-visentini` | 1 | 84.00 | **1.000** | **0.181159** | 167 | 168 | 150 | 242 | 222 | 182 | **183** |

The owner's law reads off this table directly. `harrison-ramm` plays four games at 28.75 — a little
under half his cell's par — and his premium is cut to match: 620 → 567. `vigo-visentini` plays one
game at 84.00, a quarter above his cell's par, and his premium is now the *whole* premium, larger
than a100's: 182 → 183, up. **The premium did not shrink — U″(MSD) rose from 1.904 to 2.004. It was
aimed.**

### U″ vs U′, and the q-mass

| pathway | qbar `Σeφq / Σeφ` | U (ORDER 21/23) | U′ (a100) | **U″ (ψ)** | (U″−1)/(U′−1) |
|---|---:|---:|---:|---:|---:|
| `RD` | 0.8804 | 1.2063 | 1.239884 | **1.272476** | 1.1359 |
| `ND>64` | 0.8611 | 1.3687 | 1.361599 | **1.419927** | 1.1613 |
| `IRE` | 0.8617 | 1.3380 | 1.326308 | **1.378674** | 1.1605 |
| `UNR` | 0.8534 | 1.5041 | 1.510685 | **1.598397** | 1.1718 |
| `PDA` | 0.8903 | 1.6144 | 1.575357 | **1.646263** | 1.1232 |
| `PDS` | 0.8376 | 1.4160 | 1.779469 | **1.930577** | 1.1939 |
| **MSD** | 0.9000 | 3.0959 | 1.904002 | **2.004494** | 1.1112 |
| `PDN` | 0.8941 | 2.0956 | 1.770823 | **1.862162** | 1.1185 |
| `SSP` | 0.9194 | 1.2001 | 1.167647 | **1.182345** | 1.0877 |
| `ALL POOL` | 0.8778 | 1.2522 | 1.275231 | **1.313536** | 1.1392 |

---

## 6. Anomalies, disclosed

1. **MSD's par rests on 14 playing cells / 121 games**, and its d4–d6 cells are *empty* — par there
   is the pathway donor, flat by construction. Same for SSP d4–d6 and PDN d5–d6. This is the honest
   consequence of deriving par on the population that produced `R`, as ordered; it is the single
   biggest caveat on the MSD prices, and it compounds the standing "MSD up to ~5%" caveat.
2. **The window-convention gap with the supervising seat** (entry class ≤2021 vs cell year ≤2021).
   Par values reconcile within 5%; cell counts do not, and cannot. Reported in `PAR_TABLE.md` §6.
3. **`PDA` d2 own par 30.39 (n=15)** — the outlier cell of the table, shrunk to 40.56 and disclosed.
4. **`brandon-zerk-thatcher`** moves a100 49 → ψ 48 but is **not** in `MOVERS_TABLE_PSI.md`: he
   fails the materiality bar against live on all seven columns. He is in `Q_TABLE.md` and in the
   JSON. 32 of the 33 movers are in the table.
5. **9 of the 42 partials move by less than one point** and therefore appear flat. Their `q` values
   are in `Q_TABLE.md`, so the direction law can be checked on them even though the board cannot
   show it.
6. **The `q = 0` limb is unexercised on this board.** Exactly one historical harvest cell has games
   with no usable average; zero currently-playing pool rows do. The limb is implemented and
   specified, but this board does not test it.

---

## 7. Scope — what did not move

`engine/rl_after/pvc_curve_v2.json` unmodified (`07b7109f` on every build) · store unmodified ·
`data/model_config.json` unmodified (`bf012105`) · `rl_model.py` unmodified (`e5eb5e44`) · national
code path unmodified · `_pr_phi`, `_pr_R`, `_PR_PATH`, `_PR_WHOLE`, the D12 clock, `_a_share`,
`LAM_SIT`, `_ev_qual`, `_surprise`, `_c_w`, `C_H`, `_h_cut`, `_R_surf` all untouched · the prior
fade (D9) untouched · both pool call sites unchanged in shape and still `_pool`-gated · no board,
book, pin or ledger on this branch restamped. **Nothing lands from this order.** `main`, PR #469
and PR #473 were not touched.

## 8. Files

| file | what |
|---|---|
| `PREREG_ORDER24B.md` | the pre-registration, committed first, unedited |
| `PAR_TABLE.md` | the playing par by pathway × depth, all 60 cells with `n` and shrink disclosed |
| `UPRIME2_TABLE.md` | U″ vs U′ per pathway, the q-mass, the mean-preservation proof, the control |
| `Q_TABLE.md` | every currently-playing pool row: games, avg, depth, par, q, φ, ψ weight, a100, ψ |
| `MOVERS_TABLE_PSI.md` / `.json` | **the deliverable** — seven price columns per pool player |
| `SUMMARY.md` | this file |
| `SURFACE_psi.json` | the ψ surface as built (retention unchanged from α=1.0; `uplift` = U″; `par` alongside) |
| `par.json` | the par table as data |
| `o24b_*.py` · `build_board_o24b.sh` | re-runnable machinery |
| `UHARVEST_out.txt` · `PAR_out.txt` · `UDERIVE_CONTROL_out.txt` · `UDERIVE_psi_out.txt` · `TABLE_out.txt` | transcripts |


# ORDER 24 — SUMMARY, AND EVERY PRE-REGISTERED PREDICTION SCORED

Issue #334, ORDER 24 (the cheap path). Branch `build/pool-dial`, based on `land/pool-update` @ `29a3f87`.
Brief: comment [5265706155](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5265706155).
Pre-registration: `PREREG_ORDER24.md`, committed at `f041d93` **before** any board was built, any U'
was derived and any engine line was edited.

> **levels frozen at #469 values; absolute prices ±few points, MSD up to ~5%; re-trued at landing**

---

## 1. What was done

| step | result |
|---|---|
| **STEP 1 — CONTROL** | Board rebuilt on the unmodified branch: **`665311ca72576df6ff0bbf6dfd007739`**, byte-identical to the board committed on `land/pool-update`. |
| **STEP 2 — THE DELIVERY FIX** | Both pool read sites now compute the same object, `M(p,Y) = (1-phi)*R(pathway,cls,tau) + phi*U(pathway)`, with `phi = min(gy/(6*_fEy(Y,p)), 1)`. Pool-gated only; commit `ad96ea5`. |
| **STEP 3 — DIAL + U'** | `R' = 1 + alpha*(R-1)`; U' re-derived per pathway per alpha under the new delivery weights. Mean preservation prints `1.0000000000` on all 10 rows at all 3 alpha. See `UPRIME_TABLE.md`. |
| **STEP 4 — LEVELS FROZEN** | `engine/rl_after/pvc_curve_v2.json` read from the file, never modified, nothing hardcoded from the brief. |
| **STEP 5 — THREE BOARDS** | `a025` `322df660ccce6c017ded341403b7215f` · `a050` `87214d5653e0fb8e48b804f1a890b6bc` · `a100` `ca3544d8df9272db191a67001a1bb9e4`. **0 ND movers on all three.** |
| **STEP 6 — THE TABLE** | `MOVERS_TABLE.md` / `MOVERS_TABLE.json`, 152 rows, six price columns, the named five flagged. |

**Determinism**: `a100` was built twice from scratch (a fresh detached worktree each time) and
produced `ca3544d8df9272db191a67001a1bb9e4` both times. The control's byte-identity to a board built
in a previous session by a different seat is the stronger determinism evidence.

**No blockers, no halts, no anomalies.** Every instrument that could have stopped the build was run
and passed on its own terms.

---

## 2. Board identities

| column | board | md5 |
|---|---|---|
| `pre_act` | main @ `7f4d5d2` — the last board-touching main commit before PR #462 merged (PR #462's base `435fa929` carries the same bytes; the PR body records the same md5 as its own control) | `94f1fec59f99c59d5890d5975c79fa9b` |
| `live` | `origin/main` today | `1dbd1480a34c7823f330273211cbb76a` |
| `pr469` | committed on `land/pool-update` | `665311ca72576df6ff0bbf6dfd007739` |
| `a025` | alpha = 0.25 | `322df660ccce6c017ded341403b7215f` |
| `a050` | alpha = 0.50 | `87214d5653e0fb8e48b804f1a890b6bc` |
| `a100` | alpha = 1.00, the pure delivery fix | `ca3544d8df9272db191a67001a1bb9e4` |

`pre_act` recovery is **not ambiguous** — two independent routes agree (git history on the board file,
and PR #462's own recorded control md5).

---

## 3. The separation law

| check | a025 | a050 | a100 |
|---|---:|---:|---:|
| national rows on the board (`ty==ND`, pick <= 64) | 561 | 561 | 561 |
| **ND movers vs live `1dbd1480`** | **0** | **0** | **0** |
| ND rows absent | 0 | 0 | 0 |
| ND board value (live: 620,877) | 620,877 | 620,877 | 620,877 |
| delisted `back` rows moved, of which non-pool | 12 / **0** | 12 / **0** | 12 / **0** |

`o24_table.py` asserts this and raises before it writes anything.

---

## 4. Every prediction scored

Twenty scoreable sub-claims across the fourteen numbered predictions. **Fifteen held, five breached.**
The breaches are listed by number and owned; nothing in `PREREG_ORDER24.md` has been edited.

| # | prediction | verdict | measured |
|---|---|---|---|
| **P1** | control rebuild == `665311ca...` | **HELD** | `665311ca72576df6ff0bbf6dfd007739` |
| **P2** | 0 ND movers on all three alpha boards | **HELD** | 0 / 0 / 0 |
| **P3** | mean preservation `1.0000000000` on every pathway at every alpha | **HELD** | 10 pathways x 3 alpha, all `1.0000000000` |
| **P4** | `U'(alpha) - 1 == alpha*(U'(1.00) - 1)` exactly | **HELD** | max residual `5.0e-11` (the artifact's own 10-dp rounding) |
| **P5** | full participants byte-identical to `pr469` at every alpha | **HELD** | 146 rows, 0 moved at every alpha |
| **P6a** | never-qualified current sitters byte-identical to `pr469` at alpha=1.00 | **HELD** | 45 rows, 0 moved |
| **P6b** | pool rows moving `pr469 -> a100` in [38, 52] | **HELD** | **44** |
| **P7i** | MSD and PDN U' **fall** | **HELD** | MSD 3.0959 -> 1.9040 · PDN 2.0956 -> 1.7708 |
| **P7ii** | RD, SSP, ND>64, IRE U' **rise** | **BREACHED** | only RD rose (+0.0336). SSP -0.0324 · ND>64 -0.0071 · IRE -0.0117 |
| **P7iii** | a crossover in the landed-U ordering, sitting in [1.4, 1.8] | **BREACHED** | no ordering exists: PDS (U=1.416) **rose +0.363** while ND>64 (U=1.369) fell |
| **P7iv** | MSD U' lands in [2.0, 2.9] | **BREACHED** | **1.9040** — below the band |
| **P8** | `marcus-herbert` delta = 0 at every alpha | **HELD** | 906 / 906 / 906 / 906 |
| **P9** | `jai-newcombe` delta = 0 at every alpha | **HELD** | 4883 / 4883 / 4883 / 4883 |
| **P10a** | `mani-liddy` a025 in [200,500] · a050 in [160,420] · a100 in [90,300] | **HELD** | **285 · 238 · 168** |
| **P10b** | `mani-liddy` strictly `a100 < a050 < a025 < 1025`, a100 within ~2.5x of live 128 | **HELD** | 168 < 238 < 285 < 1025; 168/128 = **1.31x** |
| **P11** | `robert-hansen` a025 in [170,340] · a050 in [140,300] · a100 in [70,220], monotone | **HELD** | **215 · 190 · 143** |
| **P12** | `nicholas-martin` abs(delta) <= 25 at every alpha, direction DOWN, immaterial | **HELD** | -3 · -5 · **-7** on 3520 |
| **P13a** | rows in the table in [110, 210] | **HELD** | **152** |
| **P13b** | material against live on >=1 alpha column in [45, 100] | **BREACHED** | **112** |
| **P14** | pool totals ordered `live < a100 < a050 < a025 < pr469`, and `a100` in [126,500, 132,000] | **BREACHED** | ordering is `live < pr469 < a100 < a050 < a025`; `a100` = **132,734** |

### The breaches, owned

**P7ii / P7iii / P7iv — I predicted the U' move would be a monotone function of the landed U. It is
not, and my reasoning about which cell dominates was the wrong way round.** I argued that the
numerator would gain mass from career non-sitters sitting out the season, lifting low-U pathways.
Measured on the harvest, that cell is **74 of 3,334 cells**; the opposite cell — career sitters
*partly* playing, which moves mass into the denominator — is **389 cells**, five times larger. The
actual driver is each pathway's own **mass swing** between sitting and playing under the new
weighting, which has no relationship to its old U at all:

| pathway | sit mass, career delivery -> current delivery | play mass, career -> current | U'(1.00) vs U |
|---|---|---|---:|
| PDS | 2,121.6 -> **2,524.4** (up) | 1,532.3 -> **1,129.6** (down) | **+0.363** |
| RD | 229,968.3 -> **243,343.3** (up) | 422,824.9 -> **409,449.9** (down) | +0.034 |
| MSD | 13,382.3 -> **11,348.7** (down) | 2,361.6 -> **4,395.2** (up) | **-1.192** |
| PDN | 2,929.9 -> 2,727.8 (down) | 707.2 -> 909.3 (up) | -0.325 |

MSD's premium collapses because MSD's historical sitters were, in large part, *partly playing* —
exactly the population the old delivery mis-classified. That is the defect showing up in the
derivation as well as on the board, and it is the substantive finding of this order.

**P13b — I under-predicted the alpha-column material count by 12 (112 vs a ceiling of 100).** Cause: I
sized the affected population correctly (97 reachable rows) but assumed a good share would fall under
the materiality bar. The >=10% limb is easy to clear on pool rows whose live prices sit at 39-130, and
at alpha < 1 the dial lifts **all 45** never-qualified current sitters materially. The count is high
because the dial reaches a population the delivery fix alone does not.

**P14 — fully breached, and the reason is worth the owner's attention.** I predicted every alpha total
would sit between live and `pr469`. Only alpha=1.00 does. `a025` (135,583) and `a050` (134,590) sit
**above** `pr469` (132,960). **The dial is not a "less of the fix" knob for the board total.** Turning
alpha down turns `R'` back toward 1, which *lifts every current sitter* — and there are 45
never-qualified current sitters against only 10 in the Liddy cell, so the dial's lift outweighs the
delivery fix's withdrawal. alpha = 1.00 is the **only** setting of the three at which the pool total
falls relative to PR #469, and the only setting at which the never-qualified sitters keep exactly the
prices PR #469 gave them.

---

## 5. What the fix does, in one reading

| board | pool total | delta vs live | moved vs live | moved vs `pr469` |
|---|---:|---:|---:|---:|
| `pre_act` | 123,243 | -1,923 | 119 | 205 |
| `live` | 125,166 | 0 | 0 | 117 |
| `pr469` | 132,960 | +7,794 | 117 | 0 |
| `a025` | 135,583 | +10,417 | 119 | 89 |
| `a050` | 134,590 | +9,424 | 119 | 89 |
| `a100` | **132,734** | +7,568 | 118 | **44** |

| cell (243 pool rows) | n | moved vs `pr469`: alpha 0.25 / 0.50 / 1.00 |
|---|---:|---|
| full participants (`gy >= 6*fe`) — anchor share **exactly 0** | 146 | 0 / 0 / **0** |
| partial participants (`0 < gy < 6*fe`) | 42 | 36 / 36 / 36 |
| current sitters **with** a prior qualifying season — the Liddy cell | 10 | 8 / 8 / 8 |
| current sitters with no prior qualifying season | 45 | 45 / 45 / **0** |

The two Liddy-cell rows that do not move are `bailey-banfield` and `jed-bews` — 8- and 12-season
careers whose evidence fade leaves an anchor share of order `1e-4`, so the multiplier change is
invisible at integer rounding. That is the design working, not an exception.

**The named five:**

| player | pre_act | live | pr469 | a025 | a050 | a100 | g26 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `mani-liddy` | 128 | 128 | **1025** | 285 | 238 | **168** | 0 |
| `robert-hansen` | 80 | 80 | **650** | 215 | 190 | **143** | 0 |
| `nicholas-martin` | 2828 | 2822 | 3520 | 3517 | 3515 | 3513 | 0 |
| `marcus-herbert` | 1053 | 906 | 906 | 906 | 906 | **906** | 8 |
| `jai-newcombe` | 4887 | 4883 | 4883 | 4883 | 4883 | **4883** | 21 |

The premium no longer lands inversely to participation: the two players who are not playing lose it,
the two who are playing were never touched by it in the first place (their anchor share is exactly
zero), and the established sitter whose price is carried by his career barely notices.

---

## 6. Scope — what did not move

`engine/rl_after/pvc_curve_v2.json` unmodified · store unmodified · `data/model_config.json`
unmodified · `rl_model.py` unmodified · national code path unmodified (`rl_model: e5eb5e44`,
`config: bf012105`, `curve_artifact: 07b7109f` on every build, including the control) · no board,
book, pin or ledger on this branch was restamped. **Nothing lands from this order.** PR #469 and
`main` were not touched.

## 7. Files

| file | what |
|---|---|
| `PREREG_ORDER24.md` | the pre-registration, committed first, unedited |
| `UPRIME_TABLE.md` | U' per pathway per alpha, sit shares, the harvest control and the mean-preservation proof |
| `MOVERS_TABLE.md` / `.json` | **the deliverable** — six price columns per pool player |
| `SUMMARY.md` | this file |
| `o24_uharvest.py` · `o24_uderive.py` · `o24_stage_surface.py` · `build_board_o24.sh` · `o24_table.py` · `o24_write_docs.py` | re-runnable machinery |
| `UHARVEST_out.txt` · `UDERIVE_CONTROL_out.txt` · `UDERIVE_a*.txt` · `TABLE_out.txt` | transcripts |
| `SURFACE_a0.25.json` · `SURFACE_a0.50.json` · `SURFACE_a1.00.json` | the three dialled surfaces, as built |

# SHIPPING PACKET v2 — THE POOL UPDATE, LANDED

Issue #334, ORDER 25. Branch `land/pool-update-v2`, cut from `origin/build/pool-quality` @ `b3bf20b`.
Owner's word: **"Land"** (comment
[5267147448](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5267147448)).
Brief: comment [5267153255](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5267153255).
Pre-registration: `PREREG_ORDER25.md`, committed at `8e3bbb8` **before** the control was built,
before one amended par cell was computed, before U‴ was derived and before a single engine byte was
edited. It has not been edited since.

**THE PR IS HELD OPEN. NOTHING MERGES WITHOUT THE OWNER'S WORD ON THESE NUMBERS.**

---

## 1. What was landed, in one reading

The pool repricing act, final configuration, all owner-ruled:

| leg | what |
|---|---|
| **delivery** | current-state, intensity dial α = **1.0** (ORDER 24) |
| **premium** | quality-conditioned, `M = (1−φ)·R + φ·(1 + q·(U‴−1))` (ORDER 24B) |
| **the amendment** | the par shrink donor becomes the **all-pool same-depth par** at K=10 — the ORDER 21 class-axis convention — replacing ORDER 24B's pathway all-depth donor |
| **the levels** | **re-trued** on the landed delivery, iterated to a fixed point |

**No code change of any kind.** `rl_model.py` byte-identical, the manifest byte-identical, the store
byte-identical, the national code path untouched. This act moves numbers: the par literals, the
uplift literals and the signed levels.

| board | md5 | total | pool | national |
|---|---|---:|---:|---:|
| `live` (`origin/main`) | `1dbd1480a34c7823f330273211cbb76a` | 746,043 | 125,166 | 620,877 |
| **`landed`** | **`88ce647f531030d8d2e094188b258191`** | **752,429** | **131,552** | **620,877** |
| | | **+6,386 (+0.856%)** | **+6,386 (+5.102%)** | **+0 (+0.000%)** |

---

## 2. The final levels, side by side with the #469 signed values

| level | #469 signed (ORDER 23) | **LANDED (ORDER 25)** | change | %  |
|---|---:|---:|---:|---:|
| `MSD` | 374 | **337** | −37 | **−9.89%** |
| `SSP` | 315 | **309** | −6 | −1.90% |
| `IRE` | 106 | **106** | 0 | 0.00% |
| `PDA` | 188 | **192** | +4 | +2.13% |
| `PDN` | 96 | **96** | 0 | 0.00% |
| `PDS` | 56 | **56** | 0 | 0.00% |
| `UNR` | 66 | **65** | −1 | −1.52% |
| `ND65+` | 298 | **297** | −1 | −0.34% |
| `RD:MID` | 289 | **290** | +1 | +0.35% |
| `RD:SD` | 245 | **245** | 0 | 0.00% |
| `RD:SF` | 217 | **218** | +1 | +0.46% |
| `RD:KPD` | 370 | **369** | −1 | −0.27% |
| `RD:KPF` | 209 | **206** | −3 | −1.44% |
| `RD:RUCK` | 259 | **257** | −2 | −0.77% |

**MSD eases by 9.9%, and that is the headline of the re-truing.** It is also **twice the ease I
pre-registered** — breach C5, owned in §9. The cause is not the par amendment; it is the delivery.
Under ORDER 21/23 the MSD premium `U = 3.0959` was collected by **career sitters**, of whom MSD's
harvest population is largely composed. Under the landed delivery a current sitter reads `R < 1` and
collects nothing, and the premium goes to current participants in proportion to `φ·q`. The pathway's
realised value per point of entry price fell 7.3% at the frozen levels, and the level had to follow
it down. **The owner's instinct that MSD would ease was right; the size is larger than anyone
pre-registered.**

Levels are written as **integers**, because `rl_model.py` builds its lookup with `int(float(v))` and
truncates. The signed table and the engine's table are the same object; the quantisation cost is
0.000%.

---

## 3. The amended par table

**Owner, verbatim:** *"I feel like MSD pars should borrow from the wider pool given the thin sample.
Do they not?"*

```
ORDER 24B:  par(pw,d) = w*par_own(pw,d) + (1-w)*par_donor(pw)   donor = the PATHWAY's ALL-DEPTH par
ORDER 25:   par(pw,d) = w*par_own(pw,d) + (1-w)*par_all(d)      donor = the ALL-POOL SAME-DEPTH par
            w = n/(n+10),  n = the raw exact-depth CELL COUNT   [unchanged]
```

**The amended donor — the all-pool par at each depth. It now rises with depth instead of being one
flat pathway number:**

| depth | d1 | d2 | d3 | d4 | d5 | d6 |
|---|---:|---:|---:|---:|---:|---:|
| all-pool par | 58.57 | 60.56 | 64.41 | 69.65 | 71.45 | 75.63 |

**The wired par, every pathway** (all 60 cells with their `n`, both donors and the shrink are in
`PAR_TABLE_V2.md`):

| pathway | d1 | d2 | d3 | d4 | d5 | d6 |
|---|---:|---:|---:|---:|---:|---:|
| `RD` | 59.74 | 63.05 | 66.86 | 71.19 | 72.34 | 75.79 |
| `ND>64` | 59.87 | 58.74 | 61.75 | 66.40 | 68.32 | 75.45 |
| `IRE` | 55.56 | 57.01 | 60.47 | 66.93 | 69.13 | 77.47 |
| `UNR` | 52.38 | 59.60 | 62.90 | 71.93 | 73.21 | 73.87 |
| `PDA` | 55.48 | 42.46 | 55.31 | 61.72 | 71.85 | 75.82 |
| `PDS` | 57.77 | 53.58 | 58.97 | 70.24 | 67.26 | 68.51 |
| **`MSD`** | **55.24** | **61.60** | **65.07** | **69.65** | **71.45** | **75.63** |
| `PDN` | 56.06 | 60.01 | 58.36 | 70.25 | 71.45 | 75.63 |
| `SSP` | 56.99 | 60.06 | 61.67 | 69.65 | 71.45 | 75.63 |
| `ALL POOL` | 58.57 | 60.56 | 64.41 | 69.65 | 71.45 | 75.63 |

**Where the amendment bites, and where it does not.** The eight cells it moves most are every one of
them an empty or near-empty **deep** cell: `SSP` d6 +33.0% · `PDN` d6 +25.9% · `SSP` d5 +25.6% ·
`MSD` d6 +22.6% · `SSP` d4 +22.4% · `PDN` d5 +18.9% · `MSD` d5 +15.8% · `PDA` d5 +14.7%. An empty
cell **is** its donor, so MSD's fourth-, fifth- and sixth-year players stop being measured against
MSD's own first-year average (61.70) and start being measured against fourth-, fifth- and sixth-year
players (69.65 / 71.45 / 75.63). **Monotone pathways go from 2 of 10 to 6 of 10** — as a consequence
of pointing the donor down the depth axis, not as an imposed shape. No isotonic projection is applied.

**The shallow MSD cells barely move, and two of them move DOWN**: `MSD` d1 −2.9%, `MSD` d2 −1.4%,
`MSD` d3 +3.6%. That matters because it is where the named rows sit.

**The declared reading of "K=10 on games."** Taken as *the par itself is games-weighted* — it is, at
every cell — with `n` the cell count, which is the named ORDER 21 convention and the reading under
which thin cells borrow **more**. The other reading (`w = games/(games+10)`) is computed cell by cell
and published in `PAR_TABLE_V2.md` §6 rather than argued away; under it MSD d1 would weight its own
9-cell sample at 0.800 instead of 0.474, borrowing **less** from the wider pool — the opposite of the
instruction. Worst cell difference between the two readings: 9.82 points.

---

## 4. U‴, and the mean-preservation instrument

| pathway | U (ORDER 21/23) | U′ (ORDER 24) | U″ (ORDER 24B) | **U‴ (LANDED)** | q-mass ratio `qbar` |
|---|---:|---:|---:|---:|---:|
| `RD` | 1.2063 | 1.239884 | 1.272476 | **1.271950** | 0.8814 |
| `ND>64` | 1.3687 | 1.361599 | 1.419927 | **1.419639** | 0.8617 |
| `IRE` | 1.3380 | 1.326308 | 1.378674 | **1.378383** | 0.8624 |
| `UNR` | 1.5041 | 1.510685 | 1.598397 | **1.594177** | 0.8595 |
| `PDA` | 1.6144 | 1.575357 | 1.646263 | **1.668500** | 0.8607 |
| `PDS` | 1.4160 | 1.779469 | 1.930577 | **1.973385** | 0.8008 |
| **`MSD`** | 3.0959 | 1.904002 | 2.004494 | **1.991003** | 0.9122 |
| `PDN` | 2.0956 | 1.770823 | 1.884507 | **1.884507** | 0.8715 |
| `SSP` | 1.2001 | 1.167647 | 1.182345 | **1.186686** | 0.8980 |
| `ALL POOL` | 1.2522 | 1.275231 | 1.313536 | **1.312885** | 0.8778 |

**The instrument, and it can halt.** The entry-weighted mean of `M` over the ORDER 21 harvest
population prints `1.0000000000` on **all ten rows** at **every** derivation of every round, to 1e-9;
the derivation raises otherwise. The identity `U‴−1 == (U_flat−1)/qbar`, computed independently,
residualises to **2.220e-16**.

**Two controls, both exact:**

- **CONTROL A (non-vacuity).** Handed ORDER 24B's own par table, the ORDER 25 machinery reproduces
  ORDER 24B's published U″ **exactly — `0.000e+00` on all nine pathways.** The par is the only moving
  part.
- **CONTROL B.** With `q ≡ 1` it reproduces ORDER 24's flat-premium U′ to **4.6e-11**.

**U‴ is re-derived at EVERY round's candidate levels**, matching ORDER 22/23's iteration convention
exactly (`o22_iterate.sh` / `o23_iterate.sh` both call the uderive step between the level step and
the emit). The entry anchor **is** the level, so the mean-preservation instrument must be re-weighted
whenever the levels move, or it would be preserving the mean of a population weighted by prices
nobody pays.

**FIVE OF NINE PATHWAYS' U FELL, not rose** — a pre-registered prediction (B6) breached, and the
reason is worth the owner's attention. **The empty deep cells the amendment repairs carry no q-mass
in the harvest, because an empty cell has no playing rows in it by definition.** The amendment's
largest effects therefore do not touch the mean-preservation instrument at all; they act only on
LIVE players who have reached those depths. Inside the harvest, the cells that move are the populated
shallow ones, and several of those (RD d1, MSD d1/d2, UNR d1, PDS d1, PDN d1) fell — raising `q`,
raising `qbar`, and lowering `U‴`. **The repair is aimed at live prices, and that is where it lands.**

---

## 5. The iteration

**The calibration target, measured FRESH on this act's own matrices, every round:**

```
national arm profile (engine arm, picks 1-64, n=1443, arm-split) = 0.9900060981
distinct values across all four rounds: 1
```

**Identical to ORDER 23's target, to all ten printed digits.** The separation law holds *at the
calibration target itself*: pool prices moved by 5.1% and the target did not move at all.

**CONVERGED AT ROUND 3 of a declared cap of 8. Round 4 re-ran the whole loop and returned the SAME
integer level table and a RECORD-IDENTICAL matrix — a true fixed point, not a tolerance stop.**

SHRUNK lambda (the quantity the level step is driven by; K=15 uniform):

| pathway | R1 | R2 | R3 | R4 |
|---|---:|---:|---:|---:|
| `RD` | 0.999120 | 0.999649 | 0.999709 | **0.999709** |
| `SSP` | 0.984306 | 0.996604 | 0.999173 | **0.999173** |
| **`MSD`** | **0.926706** | 0.979147 | 1.000669 | **1.000669** |
| `IRE` | 0.995555 | 0.997470 | 0.998066 | **0.998066** |
| `PDA` | 1.010023 | 1.005221 | 0.998909 | **0.998909** |
| `PDN` | 0.995129 | 0.997504 | 0.998243 | **0.998243** |
| `PDS` | 0.993095 | 0.996925 | 0.998117 | **0.998117** |
| `UNR` | 0.987795 | 1.001150 | 1.001731 | **1.001731** |
| `ND>64` | 0.996388 | 0.999978 | 1.000295 | **1.000295** |
| **ALL POOL** | **0.987742** | 0.996935 | 0.999795 | **0.999795** |

**Convergence at the final round: every pathway within the declared 1.0% relative on the shrunk
lambda AND on the raw lambda.** Worst: `PDS` 0.31% raw / 0.19% shrunk. Full trajectory, all four
rounds, both lambdas, the levels in force and the target-stability assert: `ITERATION_V2_out.txt`.

**The ND>64 fixed point, re-found under the amended law.** The law is
`_ND65 = min(measured fixed point, curve[64] chain)` with the chain retired by owner ruling
5262928754, which reads the derived level verbatim. It was **298** under ORDER 23's delivery; it is
**297** here — re-found by iteration, not carried across. Its round-1 raw lambda was 0.997469, nothing
like ORDER 23's 1.53, because the cap was already gone before this act started.

---

## 6. Both headline metrics — read, never targeted

Per the standing law, both are reported and neither is a target.

| pathway | n | CAREER PROFILE | vs target | YR4 / YR0 | vs target |
|---|---:|---:|---:|---:|---:|
| **NATIONAL** | 1443 | 0.990006 | 1.000000 | 1.554717 | 1.000000 |
| `RD` | 691 | 0.989717 | 0.999708 | 1.379793 | 0.887489 |
| `SSP` | 52 | 0.989010 | 0.998994 | 1.290356 | 0.829962 |
| `MSD` | 106 | 0.990791 | 1.000793 | 0.918219 | 0.590602 |
| `IRE` | 57 | 0.987641 | 0.997611 | 1.224739 | 0.787757 |
| `PDA` | 51 | 0.988668 | 0.998648 | 1.593925 | 1.025219 |
| `PDN` | 43 | 0.987731 | 0.997702 | 1.093580 | 0.703395 |
| `PDS` | 21 | 0.986955 | 0.996918 | 1.412386 | 0.908452 |
| `UNR` | 59 | 0.992208 | 1.002224 | 2.442798 | 1.571217 |
| `ND>64` | 120 | 0.990360 | 1.000358 | 1.236736 | 0.795473 |
| **ALL POOL** | 1200 | 0.989803 | 0.999795 | 1.338050 | 0.860639 |

The career profile is the ruled calibration basis and it is at parity. The yr4/yr0 ratio is **not**
at parity and is not asked to be: the pool arm's shape through the years differs from the national
arm's, which is a fact about the populations, not a defect in the calibration. It is printed so the
owner can see it.

---

## 7. No arbitrage — both instruments, every margin listed

`noarb_table_338.py` md5 **`0f8220351c64c56ccfa90c60edcdfa5f`** — computed at run, **UNMODIFIED**.
`noarb_table_allarm.py` asserts that md5 itself before it will proceed.

**ALL-ARM DECIDING INSTRUMENT** — margin vs the 14% annual charge; a negative margin is an arbitrage:

| window | variant | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | apprec 0→1 | margin | verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| PRIMARY 2005-2023 n=2212 | round 1 | 1.0000 | 0.8077 | 0.9740 | 1.0702 | 1.1289 | 1.1094 | −19.23% | **33.23%** | no arb |
| MODERN 2019-2023 n=540 | round 1 | 1.0000 | 0.8227 | 0.9272 | 0.9794 | 0.9769 | 1.0340 | −17.73% | **31.73%** | no arb |
| PRIMARY 2005-2023 n=2212 | **LANDED** | 1.0000 | 0.8077 | 0.9737 | 1.0703 | 1.1291 | 1.1096 | −19.23% | **33.23%** | **no arb** |
| MODERN 2019-2023 n=540 | **LANDED** | 1.0000 | 0.8225 | 0.9256 | 0.9794 | 0.9772 | 1.0345 | −17.75% | **31.75%** | **no arb** |

**LEGACY RETAINED INSTRUMENT** (`noarb_table_338.py`, unmodified):

| group | variant | yr1 | apprec 0→1 | margin vs 14% | verdict |
|---|---|---:|---:|---:|---|
| ALL picks 1-64 | round 1 | 1.0730 | 7.30% | **6.70%** | no arb |
| picks 1-20 | round 1 | 1.1218 | 12.18% | **1.82%** | no arb |
| picks 21-64 | round 1 | 0.9996 | −0.04% | **14.04%** | no arb |
| ALL picks 1-64 | **LANDED** | 1.0730 | 7.30% | **6.70%** | **no arb** |
| picks 1-20 | **LANDED** | 1.1218 | 12.18% | **1.82%** | **no arb** |
| picks 21-64 | **LANDED** | 0.9996 | −0.04% | **14.04%** | **no arb** |

**ARBITRAGES OPENED: 0 of 10 readings.** The tightest margin on the board is picks 1-20 at 1.82%, and
it is **identical to four decimal places before and after the repricing** — this act does not touch
the national arm, and the instrument says so.

---

## 8. Separation, determinism, pins and scope — every assertion, and each can fail

| assertion | result |
|---|---|
| **CONTROL**: unmodified tree rebuilds the ψ board | **`e2bf7347e07c08f1efbdda17d6601e4e`** — byte-identical |
| **SEPARATION**: national rows (`ty==ND`, pick ≤ 64) vs live | **0 movers, 0 absent, 0 extra**, on 561 rows |
| national board value | **620,877 → 620,877**, identical |
| separation at every intermediate lever stage | **0 non-pool movers** at H-only, at ψ-delivery and at LANDED |
| delisted (`back`) rows moved | 12, of which **non-pool 0** |
| **PICK CURVE** | **0 of 64 moved** — the `curve` block asserted unchanged on its bytes before writing |
| `pvc_curve_v2.json` top-level keys moved | **`['pool_levels']`** and nothing else |
| **DETERMINISM**: landed board built twice from scratch | identical both times |
| staged build == landed build (shipped defaults, no staging) | **byte-identical** |
| **PINS MOVED** | exactly **`{board, engine_head}`**, asserted before the file was written |
| pins UNMOVED, printed key by key | `config` · `rl_model` · `store` · `fv` · `band` · `q97m` · `v0surf` · `peak_model` · `pvc_snapshot` · `bust_prior` · `register` · `balanced_board_md5` · `as_of_round` · `release_version` · `tag` |
| **`noarb_table_338.py`** | **`0f8220351c64c56ccfa90c60edcdfa5f`** — unmoved |
| store | `d9a24282357cf3083b1640466e3ecd83` — unmoved |
| every pickle, both instruments, both harnesses, the carried patcher | **UNMOVED**, by computed md5 against `origin/main` |
| `rl_model.py`, `data/model_config.json`, ORDER 23's and 24B's own scripts | **UNMOVED**, by computed md5 against this branch's parent |
| **BOOT GUARD** on the landed tree | **PASS**, both halves |
| **SELF-TEST** section (10), the pool anchors | **fully green**, including the re-signed levels and ORDER 23's ND65+ retirement check |
| self-test net new failures | **0** — 2 on the landed tree, the **same 2** on an `origin/main` control (Guard 1 file-mode checks a git checkout cannot reproduce) |
| **BOOK** re-sealed, F2 parity | 83 mismatches before → **0 after**; builder's own gate PASS on all 802 shared rows |

Identities: board `88ce647f531030d8d2e094188b258191` · `pvc_curve_v2.json` `f6f3027f` · engine head
`3f1468e5` · retention/par/U surface artifact `b7f7bc60` · UI contract `bdc21f33` · config `bf012105`
(unmoved) · `rl_model` `e5eb5e44` (unmoved) · store `d9a24282` (unmoved).

---

## 9. The named rows, and the pre-registration scored

### The named rows, live → landed, with the lever split

| player | pathway | live | ψ at #469 levels | **LANDED** | lever H | lever ψ delivery | lever repricing |
|---|---|---:|---:|---:|---:|---:|---:|
| `harrison-ramm` | MSD | 351 | 567 | **545** | 0 | +161 | +33 |
| `luker-kentfield` | MSD | 178 | 449 | **419** | 0 | +201 | +40 |
| `mani-liddy` | MSD | 128 | 168 | **152** | 0 | **0** | **+24** |
| `robert-hansen` | MSD | 80 | 143 | **132** | 0 | +39 | +13 |
| `vigo-visentini` | RD | 168 | 183 | **182** | 0 | +32 | **−18** |
| `marcus-herbert` | MSD | 906 | 906 | **906** | 0 | 0 | 0 |
| `jai-newcombe` | MSD | 4883 | 4883 | **4883** | 0 | 0 | 0 |
| `nicholas-martin` | SSP | 2822 | 3513 | **3513** | +687 | +3 | +1 |

`marcus-herbert` and `jai-newcombe` do not move by one point, under any lever. Both are full current
participants (φ = 1) carrying an anchor share of **exactly zero**, so no multiplier and no level
reaches them. That is the cheapest available check that the delivery fix touches only the population
it is meant to touch.

Two rows in this table are worth reading twice. **`mani-liddy`'s entire move is the repricing lever
(+24) and his ψ-delivery lever is exactly 0** — he is a current sitter, `M = R`, and the level is the
only thing that reaches him. **`vigo-visentini` is the only named row whose repricing lever is
negative (−18)**: the ψ delivery lifted him +32 and the re-truing of the RD positional levels took
18 of it back, which is the calibration doing its job on a row the delivery had over-lifted.

### The pre-registration, scored. **41 held, 6 breached, and the breaches are mine.**

| # | prediction | verdict | measured |
|---|---|---|---|
| A1 | control == `e2bf7347…` | **HELD** | byte-identical |
| A2 | config/rl_model/curve/store unmoved on the control | **HELD** | 4 of 4 |
| B1 | ALL POOL row collapses onto its own values | **HELD** | worst \|wired−own\| = 0.00e+00 |
| B2 | the cell-count reading is the right one; games reading published | **HELD** | published, §6 of `PAR_TABLE_V2.md` |
| B3 | empty cells rise **+13% to +33%** | **BREACHED** | **+12.89% to +32.97%** — MSD d4 is 0.11pp below my floor |
| B4 | `par(MSD,1)` 55.0–55.6 · `par(MSD,2)` 61.3–61.9 · `par(MSD,3)` 64.8–65.4 | **HELD** | 55.24 · 61.60 · 65.07 |
| B5 | ramm's q rises, kentfield's falls, both under 4% | **HELD** | +1.42% · −3.48% |
| B6 | U‴ ≥ U″ on every pathway but at most one | **BREACHED** | **five fell** (RD, ND>64, IRE, UNR, MSD) |
| B7 | mean preservation `1.0000000000`, all 10 rows, every round | **HELD** | 10/10, every derivation |
| B8 | `U‴(MSD)` ∈ [2.00, 2.20] | **BREACHED** | **1.991003** — 0.45% below my floor |
| C1 | target reproduces ORDER 23's to ≥6 s.f. | **HELD** | `0.9900060981`, all ten digits |
| C2 | one distinct target value across every round | **HELD** | 1 |
| C3 | converges in **4–6** rounds | **BREACHED** | **3** (round 4 confirms the fixed point) |
| C4 | every pathway ∈ [0.94, 1.06] at round 1; pool ∈ [0.97, 1.03] | **BREACHED** | **MSD 0.926706**; pool 0.987742 held |
| C5 | the full level table, band by band | **BREACHED on MSD** | **337, −9.89%** vs my [355, 374] / "0–5% down"; and the "no level moves >6%" clause fails on MSD alone. **All 13 other levels held their bands.** |
| C6 | ND65+ ∈ [285, 310]; its round-1 raw lambda ∈ [0.9, 1.2] | **HELD** | 297 · 0.997469 |
| C7 | levels written as integers, the only curve write | **HELD** | both |
| D1 | board built twice, identical | **HELD** | identical |
| D2 | no-staging build == staged build | **HELD** | byte-identical |
| D3 | 0 ND movers, 0 absent, 620,877 identical | **HELD** | 0 · 0 · identical |
| D4 | pick curve 0 of 64 moved | **HELD** | asserted on bytes |
| D5 | moved pin set, and `rl_model`/`config` unmoved | **HELD** | exactly `{board, engine_head}` |
| D6 | book re-sealed isolated; F2 0 after, >0 before | **HELD** | 83 → 0 |
| D7 | boot guard PASS | **HELD** | both halves |
| D8 | 0 net new self-test failures | **HELD** | 2 landed, same 2 on the main control |
| E `ramm` | ≤ 567, and ∈ [515, 567] | **HELD** | **545** |
| E `kentfield` | ≤ 449, and ∈ [400, 449] | **HELD** | **419** |
| E `liddy` | ∈ [158, 172] ("~168-class") | **BREACHED** | **152** |
| E `hansen` | ∈ [134, 147] ("~143-class") | **BREACHED** | **132** |
| E `visentini` | ∈ [177, 189] | **HELD** | **182** |
| E1 `herbert`/`newcombe` | EXACT, unmoved | **HELD** | 906 · 4883 |
| E `nicholas-martin` | ∈ [3495, 3520] | **HELD** | **3513** |
| E2 | ramm below his ψ value at #469 levels | **HELD** | 567 → 545 |
| F1 | pool total ∈ [127,500, 132,500] | **HELD** | **131,552** |
| F2 | national total 620,877 exactly | **HELD** | exact |
| F3 | rows moved ∈ [110, 130] | **HELD** | **117** |
| F4 | board total ∈ [748,000, 754,000] | **HELD** | **752,429** |
| F5 | lever-sum identity on every row | **HELD** | 117/117, asserted at write |
| F6 | `lever_H` reproduces ORDER 23's H column exactly | **HELD** | **+2,303**, identical |
| G1 | zero arbitrages opened, every margin listed | **HELD** | 0 of 10 |
| G2 | both headline metrics read, not targeted | **HELD** | §6 |
| H1–H5 | store, pickles, instruments, national path, no new dial, nothing merged | **HELD** | §8, and the PR is held open |

### The six breaches, owned

**C5 / C4 — I under-predicted the MSD ease by half.** I predicted 0–5% down and wrote a band of
[355, 374]; MSD landed at **337, −9.89%**, and its round-1 shrunk lambda was **0.9267**, outside the
[0.94, 1.06] I declared. **I reasoned from the wrong quantity.** I anchored on the ψ board's *present*
pool total sitting within 0.5% of the ORDER 23 board's, and concluded the *historical* calibration
would be nearly unchanged. Those are different populations weighted differently. MSD's harvest
population is dominated by career sitters, who under ORDER 21/23 collected `U = 3.0959` and under the
landed delivery collect `R < 1`; the realised value per point of entry price for that pathway had to
fall, and fall hard. I could have checked the harvest's sitter share before predicting — it is
printed in the harvest transcript I had already read (MSD: 40 cells, sit mass 11,349 against play
mass 4,395, i.e. **72% of MSD's entry weight sits**). **I predicted from a board and should have
predicted from the population.**

**E `liddy` and E `hansen` — the consequence of the same error, and the one the owner should look at
hardest.** Both carry φ = 0: they are current sitters, so `M = R` and their price is set by the MSD
level and essentially nothing else. When MSD fell 9.9%, they fell with it: `mani-liddy` 168 → **152**,
`robert-hansen` 143 → **132**. The brief said Liddy "stays ~168-class after the level re-true" and
Hansen "~143-class". **They do not. They are 9.5% and 7.7% below those classes.** This is not a
defect in the machinery — it is the level re-truing doing exactly what it is for, arriving at a row
whose price is nothing but the level. But it is a movement against a stated expectation on a name the
owner has been watching since the Liddy finding opened, and it goes to him rather than into a
footnote.

**B6 and B8 — I predicted U‴ would rise, and five of nine fell.** I reasoned that raising par cuts
q-mass and therefore raises the premium. True — but **only for cells that have playing rows in the
harvest.** The amendment's biggest moves are at *empty* cells, and an empty cell contributes exactly
zero q-mass, so those moves cannot reach the mean-preservation instrument at all. What reaches it is
the populated shallow cells, several of which *fell*. I predicted the direction of the largest par
moves and forgot to ask which of them the instrument can see. `U‴(MSD)` = **1.991003**, 0.45% under
my floor, for the same reason.

**B3 — off by 0.11 percentage points at one edge.** I said the empty cells would rise "+13% to +33%";
MSD d4 rises **+12.89%**. Arithmetic I could have done exactly and rounded instead. It is a breach
and it is recorded as one.

**C3 — it converged faster than I predicted, in 3 rounds against my 4–6.** A breach in the direction
that costs nothing, recorded so the scoring is not selective.

---

## 10. The composed movers ledger

`docs/ledgers/POOL_UPDATE_V2_MOVERS_2026-08-12.md` / `.json`. All **117** movers named,
before → after → delta, with the three-lever split **on every row**, not only on the 36 that move
≥ 50 points.

| lever | board | md5 | total | Δ vs live | moved |
|---|---|---|---:|---:|---:|
| — | LIVE | `1dbd1480…` | 746,043 | 0 | 0 |
| 1 | H retirement | `452623ad…` | 748,355 | +2,312 | 48 |
| 2 | + the ψ retention/delivery machinery | `0cfa973a…` | 751,332 | +5,289 | 82 |
| 3 | + the repricing (**LANDED**) | `88ce647f…` | **752,429** | **+6,386** | **117** |

**Lever totals across every moved row: H retirement +2,303 · ψ delivery +2,965 · repricing +1,118 =
+6,386.** The lever-sum identity is asserted on all 117 rows at write time; the writer halts otherwise.

**Lever 1 is ORDER 23's own board, reused byte-identically.** Nothing in ORDERS 24, 24B or 25 touches
H, so its column total here (**+2,303**) is identical to the H column of ORDER 23's ledger — the
pre-registered check F6, and it held.

**The lever columns and the board-wide lever deltas differ by exactly one row, named rather than
reconciled away:** `jacob-moss` moves 36 → 45 → 57 → **36**, landing back on his live value, so he
carries no total delta and is not a ledger row. He accounts for the whole of each gap (+9 / +12 / −21).

**The ND65+ cap removal (185 → 297) is attributed to lever 3**, the same place ORDER 23's ledger put
it, and lever 2 is therefore staged at the *effective* 185 the live board actually priced at. Stated
here because it is a judgement, not an arithmetic necessity.

**Top movers, both directions**, are in the ledger and in `SEPARATION_V2_out.txt`. The largest rise is
`nicholas-martin` +691 (of which +687 is H retirement, not this act's repricing); the largest fall is
`patrick-carr` −36 (UNR).

---

## 11. Anomalies, disclosed

1. **MSD's par still rests on 14 playing cells / 121 games in the complete-window harvest**, and its
   d4–d6 cells are still *empty*. The amendment gives those cells a **better** donor — fourth-year
   players instead of first-year MSD players — but it does not create MSD data that does not exist.
   The "MSD completion optimism +4.7–8.4%" caveat still travels with the MSD level, and the self-test
   still asserts that it does.
2. **`PDA` d2 measures an own par of 30.39 on 15 cells**, the lowest cell in the table by a distance.
   It shrinks to 42.46 under the amendment (from 40.56), still the outlier. Disclosed, not smoothed.
3. **The `q = 0` limb remains unexercised on this board.** Exactly one historical harvest cell has
   games with no usable average; zero currently-playing pool rows do.
4. **`s4_matrix.json` is not byte-reproducible by construction** (its top-level keys are Python
   `id()` values), so it is deliberately unpinned and the boot guard does not assert it. The ORDER 20C
   finding, carried.
5. **The yr4/yr0 ratio for MSD is 0.918** — below 1, meaning the average MSD cohort is worth less at
   year 4 than at entry on that measure. It is read, not targeted, and it is a property of the
   population rather than of the calibration; the career-profile basis, which is the ruled one, is at
   parity (1.000793).
6. **One row (`jacob-moss`) round-trips through the levers.** Named in §10.

---

## 12. Files

| file | what |
|---|---|
| `PREREG_ORDER25.md` | the pre-registration, committed first, unedited |
| `CONTROL_V2_out.txt` | step 1, the control |
| `PAR_TABLE_V2.md` / `PAR_V2.json` / `PAR_V2_out.txt` | the amended par, all 60 cells, both donors, the declared sensitivity |
| `UDERIVE_V2_out.txt` / `FINAL_SURFACE_V2.json` | U‴, both controls, the mean-preservation instrument |
| `ITERATION_V2_out.txt` / `ITERATION_V2.json` | **the full trajectory, all four rounds** |
| `DERIVE_R1..R3.json`, `DERIVE_FINAL_V2.json` / `_out.txt` | the per-round derivations |
| `FINAL_LEVELS_V2.json` | the signed fixed point |
| `SEPARATION_V2.md`-equivalent: `SEPARATION_V2_out.txt` / `.json` | separation, totals, top movers, named rows |
| `CONSEQUENCE_V2_out.txt` / `.json` | the four-board lever decomposition |
| `NOARB_MARGINS_V2_out.txt` / `.json` | both instruments, every margin |
| `RESTAMP_V2_out.txt` · `boot_guard_landed_v2.txt` · `f2_parity_v2.txt` · `book_build_v2.log` | the landing mechanics |
| `untouched_artifacts_v2.txt` | the scope guards |
| `selftest_landed_v2.txt` · `selftest_origin_main_control_v2.txt` | the self-test and its control |
| `o25_*.py` · `*_o25.sh` | re-runnable machinery |
| `docs/ledgers/POOL_UPDATE_V2_MOVERS_2026-08-12.{md,json}` | the composed ledger |

---

**THE PR IS OPEN AND HELD. Nothing merges without the owner's word on these numbers.**
PRs #469, #473, #475 and `main` were not touched.

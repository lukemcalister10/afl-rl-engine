# SHIPPING PACKET — ORDER 29, THE LANDING BUILD

**2026-08-13 · branch `land/order-29` · build seat · resumed at Step 3 on owner ruling "C".**

> # THE LANDING IS COMPLETE. ALL SEVEN STEPS RAN. NOTHING IS MERGED.
> Board **`88ce647f` → `86c8d5d9`**, total **752,429 → 706,018** (−46,411, **−6.1682%**), **714 of
> 804** rows moved, decomposed across **four levers that reconcile exactly** — 0 rows failing, max
> |residual| **0**.
>
> **Three things are owed to the owner before this merges, and none of them is cosmetic:**
> 1. **P9** — a **live, priced** board row (`kalani-white`) stands in a cell the ruling says must
>    carry **no number**. §6.
> 2. **P12** — the four legs **do not** collapse on fresh entrants. **0 of 46**. §7.
> 3. **P18** — `v0surf` moved. It **had** to; the prediction was mechanically impossible. §9.

---

## 1. THE RULING, AND WHAT IT COST

Owner word **"C"** (#334 comment 5279364952): strict descent (RULEBOOK law 4 / G-MONO) **stands
unamended**; the PAVA-pooled plateaus are separated by the **−1-point-per-pick ordering tiebreak**.

**No assert was relaxed. `_split_ladder` was not touched. No ruled number was nudged to fit.**

### 1.1 The blocks, re-derived rather than assumed — and the shorthand was wrong

The stop doc named "picks 6–11" and "picks 15–20". The artifact's own blocks are **picks 6–12 and
15–21 — seven picks each**. The G-MONO assert prints only its **first eight offending left indices**,
which truncates each 7-pick block by one; ORDER 28 §5.2's published wording ("picks 6–12 pool to
1319.1 and picks 15–21 pool to 812.2") agrees with the artifact, not with the shorthand. **Applying
the tiebreak to the truncated blocks would have left a plateau step behind and the curve would still
have halted.** This is why the ruling said re-derive, and why it was re-derived.

### 1.2 The tiebreak drift table (PREREG P6's ledger gains these lines)

| block | L | pooled | values | plain sum pre | plain sum post | **residual drift** | max move |
|---|---:|---:|---|---:|---:|---:|---:|
| picks 6–12 | 7 | 1319 | 1322 > 1321 > 1320 > 1319 > 1318 > 1317 > 1316 | 9,233 | 9,233 | **+0** | 3 |
| picks 15–21 | 7 | 812 | 815 > 814 > 813 > 812 > 811 > 810 > 809 | 5,684 | 5,684 | **+0** | 3 |
| **whole curve** | | | | **47,315** | **47,315** | **+0 (+0.000000%)** | **3** |

**The drift is zero, and not by luck that was hoped for — by a property that was checked.** Both
blocks have **odd** length, so the sum-preserving anchor `v + (L−1)/2` is an exact integer and each
run is **centred on its pooled value**. Had a block been even-length the best integer anchoring would
have left ±L/2 and that residual would be printed here instead.

* ruling bound **≤ ~0.03%** on the plain sum → measured **0.000000%** — **HELD**
* ruling bound **≤ ~5 points** on any single pick → measured **3** — **HELD**
* **join shifts needed: none.** 1804 > 1322 · 1316 > 1182 · 960 > 815 · 809 > 782
* pick 1 = 3000 **untouched** (the plateaus are interior, as the ruling said)

### 1.3 Strict descent, globally

**0** non-strict steps over 1..64. All **four** block joins strict. The halt at `rl_model.py:1449`
**passes** — verified by building, not by inspecting. `r104_9_strict_descent` is re-declared `true`
and is **true by measurement**, its scope re-worded to state the tiebreak rather than imply the curve
was always strict.

### 1.4 The curve, head to tail

| | |
|---|---|
| head | **3000** at pick 1, anchor untouched |
| seam | pick **56** (last pure loclin) |
| tail zone | **57–64** |
| pick 64 | **179** (the 179-class) |
| `curve_md5` | `df766dff` → **`9729f0c5`** |
| artifact file | `f6f3027f` → **`52aa1125`** |

---

## 2. A CONVENTION DEFECT CAUGHT ON THE WAY THROUGH

The tiebroken artifact was first written with `curve_md5` **`76f8fa96`**, computed the way the stopped
seat's `o29_curve.py` computed it — `json.dumps(curve, sort_keys=True, separators=(',',':'))`.

**That is not this artifact's own convention.** The live artifact declares `df766dff`, and `df766dff`
is reproduced **only** by `json.dumps({str(pick): int(v) for pick in 1..64}, sort_keys=True)` with
**default** separators. The compact hash of the same live curve is `92a6b7c9`, which appears nowhere.

It is load-bearing rather than cosmetic because the payload md5 is **independently recomputed in
exactly one place** — the LEG F5 seal stamp (`seal_structure.py:88`) — and under the old curve the
artifact's self-declared `curve_md5` and that recomputation **agreed**. Every other consumer
(`ui/tools/ingest_inputs.py`, the club-curve provenance test, the contract's
`pick_curve_curve_md5`) checks the field for **mutual equality** and never recomputes it, so a
wrong-convention value would have sat in the chain **looking correct** while the one instrument that
recomputes disagreed. Corrected to `9729f0c5`; the seal stamp now recomputes `9729f0c5` too.

---

## 3. THE TWO COUPLED RE-DERIVATIONS THE BRIEF DID NOT NAME

Installing the ruled curve did not just install a curve. Two further objects are **derived from** it
and had to move with it. Both are documented in full in `V0SURF_REBAKE.md`.

### 3.1 The v0 surface re-bake — inseparable from a curve install

`_v0surf_sig` (`_merged_recover.py:1503-1509`) hashes the **active pick curve itself**, so **any**
curve change invalidates the frozen surface. The #326 no-silent-refit guard halted the build rather
than fitting quietly — the design working.

**The record had already ruled this coupling**, twice: *"defect 3 — `_v0surf_sig` hashes `_PVC0`
itself … so **curve install and v0surf re-bake are inseparable**"*, and, of a seat that re-pinned it,
*"**the omission was the directive text's, not that seat's**"*. ORDER 29's brief omits it the same way.

**The N35 fit-class box proof is GREEN.** Before any new fit was trusted, this box was made to
byte-reproduce the **current** frozen surface through the deterministic fit path, with the **live**
curve installed: refit md5 `fbc5b39387b2b135284a2e157f46c810` **== the committed pin, exact**. So the
bake freezes the engine's arithmetic, not this container's BLAS weather (the item-380 defect).

**This also closes an ORDER-28 open question.** ORDER 28 recorded the declared lane as *shut* and
surface-fit classification as *"untested"*. The #344 lane is landed on this tree; the classification
is now **tested and green**.

`v0surf.pkl` **`fbc5b393` → `5dd34ca8`** · shipped signature `6ef67f07` → `4405cba2` · performed only
through `RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 refit_v0surf.py --bake`, committed **isolated**. The
shipped board carries **no** refit flag and performs **zero** fits.

### 3.2 The book re-seal — a re-price, not a re-count

The board then halted on the #306 L7 reconciliation: repriced entrant layer **56,772** vs sealed
total **62,931**. That assert is the one #306 L7 made non-vacuous (it used to be a printed boolean
the exit code ignored), and it fired correctly.

Re-sealed through the **unmodified** instrument from recorded store intake history:

| | pre | post |
|---|---:|---:|
| entrant_pvc draft | 55,753 | 49,595 |
| entrant_pvc mech | 7,178 | **7,178** (unchanged — mechanisms price at the unmoved pool level) |
| **entrant_pvc total** | **62,931** | **56,772** |
| seal | `c9e7491b` | **`cbb7c431`** |

**The proof that this is lawful — a re-price, not a re-count:** `draft_occupancy`, `mech_occupancy`,
`expected_counts` and `expected_slots_per_year` are **byte-identical** to the previous seal. The
frozen measurement of *who enters* is untouched; only *what their slots are worth* moved, because the
curve moved. The board's repricing (56,772) and the re-measured seal (56,772) agree **exactly** — the
reconciliation is satisfied by agreement, not by adjustment. Committed **isolated**, per P19.

### 3.3 An ops hazard, found and worked around without touching shared state

`/home/claude/v0surf.pkl` — a bootstrap-seeded workspace cache — **shadows** `<repo>/data/v0surf.pkl`
in the engine's own precedence (`_load_v0surf`, and `boot_guard` mirrors it byte-for-byte). It still
held the **pre-bake** pickle, so the first post-bake build read a stale surface and halted again on
the same unknown signature. **The shared copy was deliberately not overwritten**: it carries signature
`6ef67f07`, which other sessions on this box build against, and the re-baked pickle drops it. The
declared first-precedence override `RL_V0SURF_PKL` is used instead — it is **not** in the release
contract's `must_be_unset` (only `RL_V0SURF_REFIT` is).

---

## 4. THE PREREGISTRATION, SCORED — ALL TWENTY, BY NUMBER

`PREREG.md` was committed before any measurement and is **never edited**. Steps 0–2 were scored by the
stopped seat and are carried forward unchanged; Steps 3–7 are scored here.

| # | prediction | outcome |
|---|---|---|
| **P1** | byte-identity at entry reproduces `88ce647f` | **HELD** — exact, on the untouched tree |
| **P2** | the unflag-three, structural (4 clauses) | **HELD** — all four |
| **P3** | the three indirect movers, head Δ < 3% | **HELD** — +1.2510% |
| **P4** | grace-A ON as code default; `RL_GRACE=0` still byte-reproduces dial-off | **HELD** — byte-identical |
| **P5** | the monotone hybrid curve, **wired** | **WIRED — and 4 of its 12 spot values BREACHED BY CONSTRUCTION under ruling C.** Head 3000, seam 56, tail 57–64, pick 64 = 179: all **HELD**. Spot values **8/12 HELD** (1,2,3,5,30,40,50,64); **4/12 BREACHED** (7→1321, 10→1318, 15→815, 20→810) — every one inside a pooled block, exactly as ruling C said. Its re-check clause is satisfied honestly: `r104_9_strict_descent` is now **true by measurement** |
| **P6** | the conservation ledger | **HELD** — weighted `0.000e+00`, plain `+0.0000%`, int drift `−0.0029%`, **plus the tiebreak drift lines the ruling ordered: +0 on both blocks** |
| **P7** | positional ND v0s at every pick, reconciliation < 1e−12 | **HELD** — max &#124;ratio−1&#124; **2.220e-16** at pick 1, against a 1e−12 bound, and reconciled against **what ships** |
| **P8** | pool v0s, Way A, K-shrunk, the predicted pathway levels | **HELD — all nine**, each to 0.05 |
| **P9** | the two n=0 cells unsigned + loud boot assert; **zero** entrants map there | **BREACHED.** The cells *are* unsigned and the guard *is* loud and proven non-vacuous — but "zero entrants" is **wrong**, and wrong by a **live priced row**. See §6 |
| **P10** | the numéraire re-pin, `s → 0.9400914291048137` | **HELD — exactly**, to the last digit |
| **P11** | E6 coherence, both sides together, ×0.945715 | **SUBSTANTIVELY HELD; its quoted constant BREACHED** at −7.09e−06. Measured ×0.945707911339. The failure is **P11's own arithmetic**: its ratio is inconsistent with P10's `s`, which P10 got exactly right. E6 &#124;pin/H − s&#124; = **0.000e+00** |
| **P12** | the printed-day-0 assert; the four legs **collapse** on fresh entrants | **BREACHED — 0 of 46.** See §7 |
| **P13** | mover classes; 800–804 movers; total 705,000–725,000; sign DOWN | **MOSTLY HELD, mover count BREACHED.** Total **706,018** — inside the range. −6.1682% — inside the −3.5…−6.5% band. Sign **DOWN**. Movers **714**, not 800–804. See §8 |
| **P14** | the ten named rows; duursma the only riser | **HELD** — `willem-duursma` is the only named row that rises (+246, +6.19%) |
| **P15** | no-arb, both instruments, on the FINAL board; 0 arbitrages | **PARTIAL.** `noarb_table_338.py` re-run **UNMODIFIED** and reproduced **every value exactly** (the only diff was dict key order) ⇒ **0 arbitrages opened**. But it reads a **frozen** matrix upstream of the board, so it is **not literally "on the final board"**, and the all-arm harness / mark-path / reverse no-arb were **not** re-run. Stated rather than dressed up. See §10 |
| **P16** | the identity gate on the landed board | **NOT RUN.** See §10 |
| **P17** | determinism across two full builds | **HELD** — two independent fresh-workspace builds, both `86c8d5d9` |
| **P18** | the moved-set of pins | **BREACHED TWICE, both owned.** `fv` (pre-existing, ORDER 28) and `v0surf` (structural — P18 was *mechanically impossible* as written). Every other forbidden pin asserted **unmoved**. See §9 |
| **P19** | boot guard PASSES; book re-sealed as an isolated commit | **PARTIAL.** Book re-sealed as an isolated commit — **done**. Guard 5 green on **everything ORDER 29 controls**; red on **`fv` alone**, the inherited ORDER-28 staleness. See §9 |
| **P20** | nothing merges; the PR is opened and HELD | **HELD** |

**Eleven held · three partial · four breached · one not run · one wired-with-a-ruled-breach.** Nothing
here is scored generously; where a prediction cannot be scored as written, it says so and says why.

---

## 5. THE BOARD, AND THE FOUR LEVERS

Every stage is an **actually built board**, never a modelled step.

| stage | board md5 | total | Δ vs LIVE |
|---|---|---:|---:|
| **LIVE** | `88ce647f531030d8d2e094188b258191` | 752,429 | — |
| **B_U** — + unflag-three | `71cbb13b3414d031135771dd7e564b3c` | 743,734 | −8,695 |
| **B_G** — + grace dial | `0017657e0469addda9260964938bad78` | 748,405 | −4,024 |
| **L3** — + curve, v0surf, re-seal | `5c0de646bd71c2e4e371bc83ccf476ef` | 744,033 | −8,396 |
| **FINAL** | **`86c8d5d9ba5b95e2cba05c78fbc31f78`** | **706,018** | **−46,411 (−6.1682%)** |

| lever | movers | Σ delta |
|---|---:|---:|
| 1 — the unflag-three | 543 | −8,695 |
| 2 — the grace dial | 39 | +4,671 |
| 3 — the curve + v0 reprint | 200 | −4,372 |
| 4 — the numéraire scalar | 580 | −38,015 |
| **total** | **714** | **−46,411** — the four sums add to the total **exactly** |

| population | n | LIVE | FINAL | Δ |
|---|---:|---:|---:|---:|
| national (ND 1–64) | 561 | 620,877 | 582,031 | −38,846 (−6.2566%) |
| pool (past 64) | 243 | 131,552 | 123,987 | −7,565 (−5.7506%) |

**Lever 3 is the curve and the surface, not the printed v0s — proven, not asserted.** A counterfactual
board built from the final tree with only the numéraire block reverted reproduced `5c0de646`
**byte-identically**, so `nd_v0`, `pool_v0`, the `curve_md5` field and the P9 guard are all
**value-inert** on the board.

### 5.1 The named rows (P14)

| row | pos | pick | LIVE | L1 unflag | L2 grace | L3 curve+v0 | L4 numéraire | FINAL | Δ |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| harrison-ramm | KPD | 3 | 545 | −4 | 0 | 0 | −18 | 523 | −22 (−4.04%) |
| luker-kentfield | KPF | 11 | 419 | −2 | 0 | 0 | −9 | 408 | −11 (−2.63%) |
| mani-liddy | MID | 15 | 152 | 0 | 0 | 0 | 0 | 152 | 0 |
| robert-hansen | SF | 2 | 132 | 0 | 0 | 0 | −2 | 130 | −2 (−1.52%) |
| dante-visentini | KPF | 56 | 1,274 | −16 | 0 | 0 | −68 | 1,190 | −84 (−6.59%) |
| vigo-visentini | RUCK | 5 | 182 | 0 | 0 | 0 | 0 | 182 | 0 |
| nicholas-martin | SF | pool | 3,513 | −44 | 0 | 0 | −188 | 3,281 | −232 (−6.60%) |
| marcus-herbert | MID | 13 | 906 | −12 | 0 | 0 | −48 | 846 | −60 (−6.62%) |
| jai-newcombe | MID | pool | 4,883 | −61 | 0 | 0 | −261 | 4,561 | −322 (−6.59%) |
| **willem-duursma** | MID | 1 | 3,977 | −50 | **+538** | 0 | −242 | **4,223** | **+246 (+6.19%)** |
| harry-sheezel | SF | 3 | 11,764 | −146 | 0 | 0 | −631 | 10,987 | −777 (−6.60%) |

**`willem-duursma` is the only named row that rises** — grace reaches him and outweighs the other two
levers, exactly the mechanism P14 named. Note the named rows all carry **L3 = 0**: they are priced on
production, not on the entry anchor, and pick 1 is 3000 under both curves.

---

## 6. **OWED DECISION 1 — P9: A LIVE PRICED ROW STANDS IN AN UNSIGNED CELL**

The two n=0 cells were **measured**, not taken on trust — from `LAYER2::fit_pool_keys` × Layer-1
`position_group` across all 954 fit rows. Exactly **`PDN|KPF`** and **`PDS|KPF`**, as P9 said. Both are
published `null`. Their declined fully-shrunk values **92.4** and **84.0** are recorded in
`declined_unsigned`, so it is provable a number existed and was **declined**, not never computed.

**P9 then predicted zero current entrants would map there. That is wrong.**

| row | cell | on the board? | record |
|---|---|---|---|
| **`kalani-white`** | `PDN\|KPF` | **YES — the ACTIVE 804-row board** | PDN, 2025, KPF, **0 career games** |
| `conrad-williams` | `PDN\|KPF` | inactive `back` list | PDN, 2022, 0 games |
| `scott-reed` | `PDS\|KPF` | neither list | PDS, 2008, 0 games |

`kalani-white` maps there under the derivation's **own day-0 key** as well as under the engine's
settled future position, so this is **not** an artefact of which position field the mapping uses.

**How the guard is built, and why it is not a weakened assert.** It is split, and neither half is
softened to let the build pass:

1. **The HALT guards the harm** — `pool_v0_of()` raises on any unsigned cell, and it is the **one**
   accessor, so a later seat cannot read `cells` around it. Today **no pricing leg reads `pool_v0`**
   (the rewire is deferred by owner ruling; pool entrants price from the #326 **signed**
   `pool_levels`, where PDN and PDS are both signed). So **no price on this board comes from a null**,
   and the halt is declared **ARMED** rather than reported as a gate that passed.
2. **The DISCLOSURE guards the forgetting** — every build prints the named rows, **to stderr**
   deliberately: `rl_export.py` execs the engine under `redirect_stdout`, so a stdout print would have
   made a "loud" guard silent in every log. That was measured and fixed.

**Non-vacuity proven on real rows, never on silence:** the accessor returns **212.4** for `RD|MID`
(n=176) and **raises** for `kalani-white`.

**Halting the entire landing on this was considered and rejected as a seat decision** — it would block
a curve the owner has ruled, over a condition that moves **no price** on this board. **The owner owes
a decision:** `kalani-white` needs either a priced answer or a signed `PDN|KPF` **before `pool_v0` is
ever consumed**.

---

## 7. **OWED DECISION 2 — P12: THE LEGS DO NOT COLLAPSE**

P12 predicted that on a fresh entrant the four legs (`_uncomp_prod`, pedigree-pole blend, `ev/raw_ev`,
L7) **collapse**, so printed day-0 == derived v0 × numéraire.

**Measured on the landed board: 0 of 46 fresh entrants collapse to the ladder.** The printed day-0 is
systematically **below** the entry anchor:

| | |
|---|---|
| fresh entrants (board rows, 0 career games, ND pick 1–64) | **46** |
| collapsing exactly to `curve[pick]` | **0** |
| ratio printed / ladder | min **0.3166** · max **0.9037** · **mean 0.5274** |

Examples: `josh-smillie` pick 7 prints **818** against a ladder **1321** (0.619); `brayden-george`
pick 26 prints **208** against **657** (0.317); `sam-allen` pick 29 prints **563** against **623**
(0.904).

**This is not a defect introduced by this landing** — the legs were **explicitly not rewired** (the
consumption rewire is deferred whole, owner-ruled). A 0-game rookie's printed price carries the
engine's establishment/bust/survival discounts, so it is a **risk-adjusted** number, not the raw entry
anchor. What P12 assumed was that those discounts vanish at day 0. **They do not.**

**The value of the measurement is that it sizes the deferred work:** the consumption rewire has to
close a gap averaging **47%** of the entry anchor, varying from 10% to 68% by row. That number did not
exist before this build. **E6 coherence itself holds exactly** (|pin/H − s| = `0.000e+00`).

---

## 8. WHY 714 MOVERS AND NOT 804 (P13)

P13 assumed *"the numéraire scalar reaches every priced row (804)"*. **It does not, and the reason is
the two-sided design working as intended.** The numéraire enters the **player** side through
`BOARD_FACTOR` and the **pick** side through the published ladder, which **already carries × s**.

* **224** rows take no `BOARD_FACTOR` move — of which **130** were re-denominated through **lever 3**
  instead (the ladder channel). They moved; they moved through the other side.
* **90** rows are unmoved by all four levers. **Every one is a pool row** priced from the #326
  owner-**signed** `pool_levels`, read verbatim in ladder currency — constants this act did not
  re-sign, so they correctly do not move. Values 3–391, across MSD/RD/ND/IRE/SSP/UNR/PDN/PDA.

P13's *substance* — the numéraire is the dominant class, the sign is down, the total lands in range —
**holds**. Its arithmetic about reach does not.

---

## 9. THE PINS — P18's TWO BREACHES, AND P19

**Restamped, with the moved-set explicitly asserted. UNDECLARED MOVERS: NONE.**

| pin | old | new | why |
|---|---|---|---|
| `store` | `d9a24282` | **`cb38ef11`** | the unflag-three |
| `board` | `88ce647f` | **`86c8d5d9`** | the landing |
| `rl_model` | `e5eb5e44` | **`a0854d1e`** | grace default + the P9 guard |
| `engine_head` | `3f1468e5` | **`e5109864`** | moved by **ORDER 28**; P18 **lists** it as allowed |
| `config` | `bf012105` | **`eed19a75`** | `RL_GRACE` in the pinned manifest |
| **`v0surf`** | `fbc5b393` | **`5dd34ca8`** | **P18 BREACH — structural. §3.1** |
| `fv` | `2621b56a` | **not restamped** | **P18 BREACH — pre-existing, ORDER 28's** |

**P18's forbidden list, each asserted UNMOVED against a real hash on the final board:** `band` ·
`bust_prior` · `peak_model` · `q97m` · `pvc_snapshot` · `register`. *(An earlier draft of this check
resolved three of them at the wrong paths and silently **skipped** them — the paths were corrected
from `boot_guard.py:225-227` and the assertions are now real rather than vacuous.)*

**Why `v0surf`'s breach is structural rather than incidental.** P18 forbids `v0surf` moving **and**,
through P5, requires the ruled curve to be wired. Given `_v0surf_sig` hashes the curve, **those two
clauses cannot both hold: P18's moved-set was mechanically impossible as written.** P18's *purpose* —
catching an **unexplained** mover — is intact: this one is explained by mechanism, licensed by the
record, proven safe on this box by a green N35 proof, and **decomposed as its own lever**.

**`fv` is deliberately not restamped.** ORDER 28 moved it; this act never touches
`engine/forward_valuation`; re-pinning an identity this act did not move would **launder ORDER 28's
drift through ORDER 29's restamp**.

**Guard 5 (P19)** is green on **everything ORDER 29 controls** — store, board, config, rl_model,
engine_head, v0surf, q97m, band, register, peak_model, bust_prior, pvc_snapshot — and red on **`fv`
alone**. P19 asked for a clean guard; it is clean but for that one inherited red, reported rather than
made green by restamping something this act did not move.

**Pre-existing finding, reported not fixed:** `data/rl_build/rl_app_data.json.srcmd5` carries
`own_md5 4b448a82`, which did **not** match the board file before this act either. Its documented
contract is that `source_md5` advances and `own_md5` stays **unchanged**
(`ui/tools/ownership_store_apply.py:25-31`), so only `source_md5` was advanced to `cb38ef11`.

---

## 10. THE CONTROLS

| control | status |
|---|---|
| byte-identity at entry, dial OFF | **PASS** — `88ce647f` exact (Step 0) |
| `RL_GRACE=0` reproduces dial-off | **PASS** — byte-identical `71cbb13b` |
| G-MONO strict descent on load | **PASS** — the `rl_model.py:1449` halt clears |
| **N35 fit-class box proof** | **PASS — GREEN**, refit reproduces pin `fbc5b393` exactly |
| the #326 no-silent-refit guard | **FIRED IN ANGER**, then satisfied by a declared bake |
| the #306 L7 entrant reconciliation | **FIRED IN ANGER**, then satisfied by agreement (56,772 == 56,772) |
| P7 reconciliation, every pick | **PASS** — 2.220e-16 |
| P9 unsigned-cell guard | **LIVE and NON-VACUOUS on real rows** — and it **found something** |
| **deterministic double-build** | **PASS** — two fresh workspaces, both `86c8d5d9` |
| lever reconciliation, every row | **PASS** — 0 failures, max residual 0 |
| lever-3 isolation (v0 objects inert) | **PASS** — byte-identical counterfactual |
| pin moved-set asserted | **PASS** — no undeclared movers |
| Guard 5 boot guard | **PARTIAL** — green but for the inherited `fv` red |
| book re-seal, isolated commit | **DONE** |
| `noarb_table_338.py`, **unmodified** | **PASS** — every value reproduced; **0 arbitrages opened** |
| all-arm harness · mark-path · reverse no-arb | **NOT RE-RUN on the final board** |
| identity gate (P16) | **NOT RUN** |

**On the ones that did not run, plainly — with the blocking reason MEASURED, not assumed.**

`noarb_table_338.py` was re-run unmodified and reproduced its table exactly, which is a real result —
but the instrument reads a **frozen** walk-forward matrix whose identity pins sit upstream of this
board, so it measures the **teaching basis**, not the landed board.

**The identity gate (P16) was attempted and it refused to run**, which is the gate behaving correctly:

```
PIN ASSERTION FAILED (entry):
  store cb38ef11… != d9a24282…  (engine/rl_after/rl_model_data.json)
  board 86c8d5d9… != 88ce647f…  (engine/rl_after/rl_app_data.json)
```

`o28_gate.py` hard-pins its entry basis to the **pre-landing** store and board (`o28_gate.py:40-41`).
Landing moves both, so the committed gate cannot read the landed board without **re-pointing its
pins** — a change to a committed instrument, which this seat will not make unasked at the end of a
build. **The gate is therefore outstanding, and the work needed is exactly one declared re-point**,
not a re-derivation.

The all-arm harness, the mark-path progression and reverse no-arb were likewise **not** re-run. All of
these are named as **outstanding**, not quietly folded into a PASS: running an instrument on the wrong
basis and reporting its number would be worse than reporting the gap.

---

## 11. STATE

| | |
|---|---|
| branch | `land/order-29` |
| board | **`86c8d5d9ba5b95e2cba05c78fbc31f78`** |
| store | `cb38ef1171dcf20aae66ebf12682be0d` |
| `pvc_curve_v2.json` | `52aa11258e83a0c8a549940ab3b4388a`, `curve_md5` **`9729f0c5`** |
| `rl_model.py` | `a0854d1e8421d956edc3bea5150abf49` |
| `v0surf.pkl` | `5dd34ca82735f5c8f021b1c7320df8f8` |
| entrant seal | `cbb7c431` |
| `s` | **0.9940610814748366 → 0.9400914291048137** |
| PR | **#510, HELD — `[HELD — DO NOT MERGE]`** |

**NOTHING MERGES WITHOUT THE OWNER'S WORD ON THIS PACKET.**

---

### Evidence index

| file | what |
|---|---|
| `PREREG.md` | the twenty predictions, filed before any measurement, never edited |
| `STOP_STEP3_GMONO.md` | the stop this leg resumed from |
| `o29_tiebreak.py` · `TIEBREAK29_out.txt` · `TIEBREAK29.json` | the ruling-C tiebreak and its drift ledger |
| **`V0SURF_REBAKE.md`** · `n35box.sh` · `bake_v0surf.sh` | the coupled re-bake, the N35 proof, the P18 breach |
| `reseal.sh` | the LEG F5 book re-seal |
| `o29_v0s.py` · `V0S29_out.txt` · `V0S29.json` | Steps 4–6: positional v0s, pool v0s, the numéraire |
| `p9probe.py` | the P9 unsigned-cell probe, under all three position conventions |
| `o29_day0.py` · `DAY0_29_out.txt` · `DAY0_29.json` | Step 7 / P12, the collapse that did not happen |
| `o29_pins.py` · `PINS29_out.txt` · `PINS29.json` · `BOOTGUARD29_FINAL.txt` | the restamp and the guard |
| `o29_movers_full.py` · `docs/ledgers/LANDING_29_MOVERS_2026-08-13.{md,json}` | every player, four levers |
| `bb29.sh` | the staged-workspace board builder |

---

# 12. FINAL-BOARD CONTROLS — THE BLOCK THE BUILD SEAT LEFT NOT RUN

**Controls seat, same day, same branch. Entry tip `ba4ab18`. THE BOARD DOES NOT MOVE IN THIS SECTION
AND IS RE-ASSERTED AT THE END OF IT.** Everything below is added evidence under
`docs/evidence/landing_29_2026-08-13/`; the diff against `ba4ab18` outside that directory is **empty**.

§10 left four things outstanding: the identity gate (P16), and — for P15 — the all-arm harness, the
mark-path progression and reverse no-arb, plus the observation that `noarb_table_338.py` had measured
the *teaching basis* rather than the landed board. All four were attempted. **Two came back green,
one came back green and corrected a claim in a delivered packet, and one HALTED and is reported as a
halt rather than worked around.**

## 12.1 P16 — THE IDENTITY GATE. **HELD, BIT-EXACT.**

The refusal §10 measured was a stale basis, not a broken gate. Exactly one declared re-point was
applied, in its own commit, to a **copy** — ORDER 28's `o28_gate.py` is left byte-unchanged
(`1089b2ba…`), because an act does not rewrite a delivered packet's instrument in place:

| # | what | from | to |
|---|---|---|---|
| 1 | `PINS_ASSERT['store']` | `d9a24282…` | **`cb38ef11…`** |
| 2 | `PINS_ASSERT['board']` | `88ce647f…` | **`86c8d5d9…`** |
| 3 | `VARIANT_BOARD` | ORDER 28's step-3 dial-ON scratch board (deleted) | the landed board |
| 4 | stage + output names | `eng28_gate`, `GATE28.*` | `eng29_gate`, `GATE29.*` |

Re-point 3 is a consequence of the landing, not a convenience: ORDER 28 needed two boards because the
dial had moved the scorer but not the shipped board. **ORDER 29 lands the dial**, so the checkout's
board *is* the dial-ON board and the two Ruling-9 readings coincide by construction. Both columns are
still printed so the collapse is visible rather than asserted.

**Nothing the gate checks is weakened** — the full diff ships as `GATE29_REPOINT.diff` and the
code-only diff is four hunks, every one an identity string or an output path. Unchanged byte for byte:
the 1e−6 identity tolerance, Ruling 9's ±2% band, the hard `assert _maxres < 1e-3` on the attribution
residual, the **exit** re-assertion of both pins, the scorer, `band_career`, `score_career`,
`gate_price`, the panel construction and the board-wide control.

| reading | result |
|---|---|
| price-function identity, panel | **12 of 12 PASS** · max &#124;mine/price6 − 1&#124; **0.000e+00** |
| price-function identity, board-wide | **800 of 800 within 1e−6 (100.0%)** · max **0.000e+00** · over **804** active rows |
| attribution residual | max **2.220e-16** against the 1e−3 halt |
| pins at exit | store `cb38ef11` · board `86c8d5d9` — **unmoved**; the gate proves it wrote no byte |

P16 predicted *"price-function identity bit-exact (`0.000e+00`) on the panel and board-wide"*.
**Measured 0.000e+00 on both. HELD — and held bit-exact, not within tolerance.** The 800-of-804 shape
is the historical one (804 rows measured, 4 carrying `price6 = 0` and therefore outside a ratio test).

The Ruling-9 legs read 2 of 12 on the panel and 75 of 804 board-wide. **That is not a gate failure and
is not scored as one:** Ruling 9 compares the *scorer* to a board, and this scorer is the six-career
band scorer, not the shipped pricing chain — the attribution table names every multiplicative leg
between them and closes to 2.220e-16. ORDER 28 read 2 of 12 and 72 of 804 on the identical construction.

## 12.2 P15 — THE AS-OF MATRIX. **REGENERATED. This was the expensive half and it is done.**

`emit_variant_o29.sh`, the sibling of ORDER 25's `emit_variant_o25.sh`, with the staging removed
(ORDER 25 had to inject a candidate that was not yet source; ORDER 29's curve, surface, book and
numéraire are all committed at HEAD) and `RL_V0SURF_PKL` added for the §3.3 shadowing hazard. The
emitter is copied, never modified.

| | |
|---|---|
| `per_entrant_O29FINAL.json` | **`814df691…`** · 24 as-of years · **3m 14s** |
| basis | store **`cb38ef11`** · engine head **`e5109864`** · v0surf **`4405cba2`** (the re-baked *shipped* signature) · `frozen=True` |
| dial | grace-A at its **landed code default** (`RL_GRACE` unset = `'1'`, pinned manifest) |
| population | **2648** records · ND 1–64 teaching **1447** |

Both deltas against the live emit are **+3, and they are the same three rows**: `adam-treloar`,
`dylan-shiel`, `jeremy-cameron` — the unflag-three (lever 1), which stop being `_pvc_exclude` and
therefore start teaching the curve. Nothing else entered; nothing left. **The matrix moved exactly
where the landing says it should.**

## 12.3 P15 — BOTH COHORT INSTRUMENTS ON THE LANDED MATRIX. **HALTED. Reported, not worked around.**

```
noarb_table_338.py  ->  harness_pvc_REPINNED_pass3.py:327
    AssertionError: matrix store cb38ef11 != committed identity d9a24282
noarb_table_allarm.py:50
    AssertionError: store pin moved: cb38ef11
```

Verbatim in `NOARB_LANDED_HALT.txt`. The blocking literals, **measured** (`NOARB_BASIS_out.txt`), not
guessed:

| file | name | holds | landed matrix carries |
|---|---|---|---|
| `harness_pvc_REPINNED_pass3.py` | `EXPECT_STORE` | `d9a24282` | **`cb38ef11`** |
| `harness_pvc_REPINNED_pass3.py` | `EXPECT_V0SURF` | `6ef67f07db98` | **`4405cba2b42f`** |
| `harness_pvc_REPINNED_pass3.py` | `EXPECT_N` | `1197` | **`1200`** |
| `noarb_table_allarm.py` | store + surface, inline | `d9a24282` / `6ef67f07db98` | **`cb38ef11` / `4405cba2b42f`** |

**`noarb_table_338.py` itself carries no pin and needs no edit** — md5 `0f8220351c64c56ccfa90c60edcdfa5f`,
verified unmoved at run. It delegates to the harness, and `noarb_table_allarm.py` asserts *its* md5.
`EXPECT_N` 1197 → 1200 is the unflag-three again, by name.

**The control is what makes the halt diagnostic rather than ambiguous.** The same invocation, the same
instrument copies, on `per_entrant_O25R4.json` — the matrix behind the LIVE board — reproduced
`NOARB_MARGINS_V2` **to the last digit**: PRIMARY **+33.23%**, MODERN **+31.75%**, ND all/1–20/21–64
**+6.70% / +1.82% / +14.04%**, **0 arbitrages**. The pipeline, the runner and this seat are sound. The
pin is the blocker, and only the pin.

**Why this seat stopped instead of re-pointing.** The harness is named `harness_pvc_REPINNED_pass3.py`
and its header is a *log of successive declared re-points* — *"THE PINS WERE RE-POINTED, NEVER PATCHED
AWAY, and the asserts are byte-identical"* — one entry per act that moved the store, and it even quotes
this exact halt shape as proof the assert fires. So the fix is precedented and small: **five literals
in two files, every one measured above.** It is still not this seat's call. One declared re-point was
authorised — the gate's — and the standing instruction is to stop rather than modify a pinned
instrument. Re-pointing the instrument that *defines the basis of the no-arb reading* is the last
thing to do unasked at the end of a landing.

**No arbitrage was opened on the landed basis, because no reading was taken on it.** That is stated
rather than dressed up, and the expensive work is banked: the matrix exists, so the owner's word turns
into numbers in about two minutes.

## 12.4 P15 — MARK-PATH PROGRESSION AND REVERSE NO-ARB. **BOTH PASS, 10 of 10, ON THE LANDED BOARD.**

These carry no store pin, so the landing did not lock them out. `o29_instruments.py` is
`o28_instruments.py` (`cb55c8b6…`) with **two basis substitutions and nothing else**
(`INSTRUMENTS29_REBASIS.diff`) — no predicate, tolerance, bootstrap parameter, depth axis or
population rule touched:

1. **The denominator is now what ships.** ORDER 28 read the *proposed* `candidate.allin` — full float,
   before ruling C. This reads the **shipped** `pvc_curve_v2.json` (`curve_md5 9729f0c5`). The run
   **halts** if any pick outside the two ruled blocks (6–12, 15–21) moves by more than rounding, so
   the provenance is checked rather than assumed. The pool half is unchanged because the landing did
   not move it — verified by `cell × anchor_factor` reproducing the published landed cell table, with
   `anchor_factor` bit-equal to the landed `s = 0.9400914291048137`.
2. **The numerator closes ORDER 28's own declared breach.** That file's header said its marks came from
   an off-dial matrix and named the re-emit as the follow-up. **The follow-up ran.**

| instrument | result |
|---|---|
| mark-path progression | **10 of 10 arms PASS** |
| reverse no-arb | **10 of 10 arms PASS · 0 pathways fail** |

Peaks: ND 1–64 **1.5653** @d3 · RD **1.4660** @d3 · SSP **2.0527** @d2 · MSD **1.2379** @d5 · IRE
**2.0281** @d6 · PDA **1.6901** @d4 · PDN **1.5228** @d5 · PDS **1.3118** @d4 · UNR **1.7261** @d4 ·
ND>64 **1.5181** @d6. Reported as the pre-statement demands: limb 1 is clear on **every** arm, so this
is *"every arm clears by a printed margin"*, **not** *"the test was hard and was survived"* — the
smallest `max m(d≥1)` is MSD **1.2379**, 24% above the failure line.

### 12.4.1 A finding that corrects a delivered packet

ORDER 28 could not measure the dial's effect on the marks, so it **predicted the direction** — higher
at shallow depths, unchanged deeper — and used that prediction to argue its own progressions were
**conservative** and that *"the instruments' PASS shape cannot be manufactured by the gap"*.

Measured, same denominator both sides so it isolates the numerator:

| | mean Δ (landed − live) |
|---|---:|
| shallow, d0–d1 | **−0.0332** |
| deep, d2–d6 | **−0.0815** |

**The prediction does not hold.** The landed marks are **lower at essentially every arm and every
depth, and they fall further deep than shallow** — the opposite shape, consistent with a board that
fell 6.17% under the numéraire re-pin. **ORDER 28's read was optimistic, not conservative.**

Neither verdict in §12.4 depends on that assumption — both instruments run on the landed marks
directly — but ORDER 28's reported margin was defended by a claim that has now been measured and ran
the other way. Recorded because it was measured.

## 12.5 THE SCORE, BY NUMBER

| # | prediction | §4 verdict | **final-board verdict** |
|---|---|---|---|
| **P15** | no-arb, both instruments, on the FINAL board; 0 arbitrages; mark-path PASS on all 10 arms and reverse no-arb PASS on all 10 | PARTIAL | **STILL PARTIAL, and partial differently.** Its *second* clause is now **fully HELD on the landed board**: mark-path **10/10**, reverse no-arb **10/10, 0 fail**. Its *first* clause is **not scorable**: the as-of matrix was regenerated under the landed engine, but **both cohort instruments refuse it on their store/surface/population pins**, so no landed cohort reading exists. **0 arbitrages opened — on the readings that ran.** The live-basis control reproduced ORDER 25's tables to the last digit. §12.3 |
| **P16** | the identity gate on the landed board; identity bit-exact `0.000e+00` on the panel and board-wide | NOT RUN | **HELD.** Panel **12/12**, board-wide **800/800**, max &#124;mine/price6 − 1&#124; **0.000e+00** on both, attribution residual **2.220e-16**, pins re-verified unmoved at exit. §12.1 |

**§4's tally is amended by exactly these two lines: eleven held → twelve held; one not run → none not
run; three partial → two partial.** Every other score in §4 stands untouched.

## 12.6 THE CONTROLS TABLE, EXTENDED

| control | status |
|---|---|
| identity gate (P16), re-pointed and run | **PASS — 800 of 800 board-wide at `0.000e+00`** |
| as-of matrix regenerated under the landed engine | **DONE** — `814df691`, 2648 records, +3 = the unflag-three |
| `noarb_table_338.py`, unmodified, on the LANDED matrix | **HALTED** on `EXPECT_STORE` / `EXPECT_V0SURF` / `EXPECT_N` |
| all-arm harness on the LANDED matrix | **HALTED** on the same pins |
| both cohort instruments on the LIVE matrix (control) | **PASS** — reproduces `NOARB_MARGINS_V2` to the last digit, 0 arbitrages |
| mark-path progression, landed board | **PASS — 10 of 10 arms** |
| reverse no-arb, landed board | **PASS — 10 of 10 arms, 0 pathways fail** |
| ORDER 28's declared off-dial-matrix breach | **CLOSED** — and its stated direction **did not hold** (§12.4.1) |
| board unmoved by this seat | **PASS** — see §12.7 |

## 12.7 THE BOARD DID NOT MOVE

Re-asserted after every control ran:

| | |
|---|---|
| `rl_app_data.json` | **`86c8d5d9ba5b95e2cba05c78fbc31f78`** — unchanged |
| `rl_model_data.json` | `cb38ef1171dcf20aae66ebf12682be0d` |
| `pvc_curve_v2.json` | `52aa11258e83a0c8a549940ab3b4388a` |
| `rl_model.py` | `a0854d1e8421d956edc3bea5150abf49` |
| `_merged_recover.py` | `e51098648c1ccb6951b30d57d9aac3fe` |
| `data/v0surf.pkl` | `5dd34ca82735f5c8f021b1c7320df8f8` |

`git diff ba4ab18..HEAD` outside `docs/evidence/landing_29_2026-08-13/` is **empty**. No engine, store,
curve or surface byte moved. `noarb_table_338.py` is unmodified at `0f8220351c64c56ccfa90c60edcdfa5f`;
`o28_gate.py` and `o28_instruments.py` are byte-unchanged. **The single declared re-point in this
section lives in a new file, not in a committed one.**

**THE MERGE HOLD IS UNCHANGED. NOTHING MERGES WITHOUT THE OWNER'S WORD ON THIS PACKET**, and the
owner now additionally owes a word on §12.3: whether the two cohort instruments are re-pointed to the
landed basis, which is the only thing standing between this branch and a complete P15.

### Evidence index — final-board controls

| file | what |
|---|---|
| `o29_gate.py` · `GATE29.{json,_out.txt}` · `GATE29_REPOINT.diff` | P16: the gate, the declared re-point, and the run |
| `emit_variant_o29.sh` | the as-of matrix re-emitted on the landed tree |
| `run_noarb_o29.sh` · `NOARB_MARGINS_29_out.txt` | both cohort instruments: the live basis, and the landed attempt |
| `NOARB_LANDED_HALT.txt` | the two refusals, verbatim, instrument md5s computed at run |
| `o29_noarb_basis.py` · `NOARB_BASIS_out.txt` | the blocking literals and the +3 rows, measured |
| `o29_instruments.py` · `INSTRUMENTS29.{json,_out.txt}` · `INSTRUMENTS29_REBASIS.diff` | mark-path + reverse no-arb ON the landed board |
| **`NOARB_MARGINS_29.{md,json}`** · `o29_noarb_tables.py` | the owner-facing tables, ORDER 25 layout, landed-vs-live |

---

# 13. THE COHORT INSTRUMENTS RE-POINTED AND RUN — P15 SCORED IN FULL (appended 2026-08-13, supervisor seat, in-session)

§12.3's owed word arrived: the re-point was **authorized by the supervisor seat within the ruled
ORDER 29 spec** (the spec itself mandates both cohort instruments on the FINAL board; #334 comments
5278653175 / 5279364952 carry the brief and the ruling). Applied per the harness's own precedented
convention — ORDER 29's disclosed copies under `noarb/`, header log appended, five identity literals
moved (`EXPECT_STORE d9a24282→cb38ef11` · `EXPECT_V0SURF 6ef67f07db98→4405cba2b42f` ·
`EXPECT_N 1197→1200`, the +3 named as the unflag-three · the allarm inline pair), no tolerance,
window, band or logic touched. `noarb_table_338.py` byte-identical at `0f822035…`, asserted at run.
The composition act's copies and the instrument of record are untouched.

## 13.1 THE READINGS (canonical margins reporter, `noarb/MARGINS_O29.{txt,json}`)

| instrument | reading | apprec 0→1 | margin v14% | verdict |
|---|---|---:|---:|---|
| all-arm | PRIMARY 2005–2023 (n 2215) | −14.71% | **+28.71%** | no arb |
| all-arm | MODERN 2019–2023 (n 540) | −12.66% | **+26.66%** | no arb |
| legacy ND | ALL picks 1–64 (n 1200) | +21.73% | **−7.73%** | **ARB** |
| legacy ND | picks 1–20 | +29.92% | **−15.92%** | **ARB** |
| legacy ND | picks 21–64 | +9.24% | **+4.76%** | no arb |

**ARBITRAGES OPENED: 2 of 10 readings.** Full year paths, the by-arm landed-vs-live table, and the
§5 cliff answer are in `NOARB_MARGINS_29.md` (its HALTED markers now carry the readings).

## 13.2 P15 — FINAL SCORE: **BREACHED, owned by number.**

P15's first clause predicted 0 arbitrages on the final board with both cohort instruments. The
landed reading opens **two**, both in the legacy ND instrument: the historical ND cohort's
rederived day-0 sits low enough against year-1 marks (still produced by the un-rewired four legs)
that yr0→1 appreciation exceeds the 14% carry (+21.7% all-in; +29.9% picks 1–20). The second
clause (mark-path 10/10, reverse no-arb 10/10) stands HELD. The pool yr0→yr1 cliffs did NOT close
(measured per arm in `NOARB_MARGINS_29.md` §5) — they belong to the legs, which this act was ruled
not to touch; P12 measured the same object on fresh entrants (printed ≈ 0.53× v0 × numeraire).

**§4's tally is amended by exactly these lines: P15 PARTIAL → BREACHED (first clause measured and
failed; second clause held). The breach is a finding about the landed board's interim state, not a
measurement failure — and the merge decision now explicitly includes it.**

## 13.3 EXIT ASSERTS, RE-RUN AFTER THE RE-POINT

Board `rl_app_data.json` = `86c8d5d9ba5b95e2cba05c78fbc31f78` (unmoved by any reading — instruments
read the matrix, never the board). `noarb_table_338.py` (all copies) `0f822035…`. Diffs beyond
`docs/evidence/landing_29_2026-08-13/` since `ba4ab18`: none. **THE MERGE HOLD IS UNCHANGED —
NOTHING MERGES WITHOUT THE OWNER'S WORD ON THIS PACKET**, which now includes the two open
arbitrages and the unclosed pool cliffs as named merge considerations.

---

# 14. ORDER 29B — THE ENTRY WIRING (appended 2026-08-13, build seat, entry tip `53e7c92`)

> ## THE PRINTED DAY-0 PRICE NOW **IS** THE DERIVED v0 × NUMÉRAIRE. **89 of 89, TOLERANCE 0.**
> ORDER 29 landed the day-0 OBJECTS and **nothing consumed them** — its own P12 measured the cost:
> **0 of 46** fresh entrants printed the entry anchor, at mean **0.5274×**. ORDER 29B closes exactly
> that. Board **`86c8d5d9` → `36d5dfc7`**, total **706,018 → 717,527** (**+11,509, +1.6301%**),
> **89 movers, all of them entrants, zero coupled movers, zero rows with evidence touched.**
>
> **Three things the owner must read before this merges, and none of them is cosmetic:**
> 1. **The two open ND arbitrages did NOT close. They WIDENED, and a third opened** — 2 of 10 → **3 of
>    10**. Predicted direction **BREACHED**, mechanism measured, nothing tuned. §14.6.
> 2. **The mark-path progression falls 10/10 → 6/10.** Four arms now peak at d0/d1. §14.6.
> 3. **An owed decision on the day-0 predicate** — as-of games vs career-total games. One line of code;
>    it decides whether 1 and 2 above happen at all. This seat did **not** switch after seeing the
>    reading. §14.7.

---

## 14.1 THE PREREGISTRATION, SCORED — ALL THIRTY-ONE, BY NUMBER

`PREREG_29B.md` was committed **before a line of wiring was written** (tip `44adeed`) and is never
edited.

| # | prediction | outcome |
|---|---|---|
| **0.2a** | the branch returns unrounded, so `printed == round(derived v0)` is EXACT, tolerance 0 | **HELD** — 89 of 89, zero mismatches. Pre-rounding was measured to break 18 of 89, which is why it does not |
| **1** | the P12 identity moves **0/46 → 46/46** | **HELD** — exact |
| **2** | the full wired population **89/89**, `kalani-white` included through the borrowed cell | **HELD** — exact |
| **3** | the legacy position-blind reading stays **0/46 both before and after** | **HELD** — 0/46 on both boards, and the reason is printed: `posv/curve = relat_g(pick)` over these 46 rows reads min 0.1005 max 1.9424 mean 0.9531, and equals 1.0 on **0 of 46** |
| **4** | the entry board reproduces ORDER 29's P12 ratio statistics | **HELD** — min **0.3166** max **0.9037** mean **0.5274**, to the digit. The instrument is reading the same object |
| **5** | the `v` mover set is **exactly the 89**; **zero** coupled movers | **HELD** — 89 movers, all `cg == 0`; no `cg > 0` row moved; no `cg == 0` row failed to move |
| **6** | the two entrant-coupled objects; exactly **1** active row reached by the borrow | **HELD** — `kalani-white` only (`conrad-williams` and `scott-reed` are off the board) |
| **7** | `v`/`vP1`/`vP2` = the same 89; `vM1` ≤ 89 extra; `vM2` ≤ 183 extra | **HELD** — vP1/vP2 exactly 89; vM1 **76** extra; vM2 **111** extra. Their **present** price is byte-identical |
| **8** | total **717,527 ± 5** | **HELD EXACTLY** — 717,527. The row-by-row prediction summed to the unit |
| **9** | the ten ORDER-29 named rows unmoved; `kalani-white` 84 → 92 | **HELD** — all ten at **+0**; kalani-white **84 → 92** |
| **10** | one site, `ev(p,Y)`, and the set is complete because it is the function | **HELD** — implemented as declared |
| **11** | the LEG F5 #306 reconciliation does not fire; no re-seal | **HELD** — `f5_draft_pvc` 49,595 · `f5_mech_pvc` 7,178 · `entrant_layer_pvc` **56,772**, all unchanged |
| **12** | the year-zero floor's own population gate | **HELD** |
| **13** | the borrowed cells reproduce `declined_unsigned` **92.4 / 84.0** exactly | **HELD** — 92.35874340265629 and 83.97715038537063, round-1 **92.4 / 84.0** |
| **14** | each borrowed cell flagged **on the cell**, a disclosed field | **HELD** — `cell_signature` (all 54) + `borrowed_cells` (full per-cell provenance); `unsigned_cells` → `[]` |
| **15** | the halt retires, a coverage assert replaces it, and it passes | **HELD** — **1202 of 1202** pool rows map to a signed cell; non-vacuity re-proven on a real row every build |
| **16** | the four fallers named in advance; no fresh entrant on the RUCK 63/64 zero floor | **HELD** — sweid −44, davis −43, anderson −42, torrent −19; the two RUCK entrants sit at picks 42 and 52 |
| **17** | rows sharing a cell print the same number afterwards | **HELD** — the seven `IRE\|SD` rows (85/85/43/43/85/43/45) all print **87** |
| **18** | control at entry reproduces `86c8d5d9` byte-exactly | **HELD** — run before the prereg was committed |
| **19** | deterministic double-build | **HELD** — two fresh workspaces, both `36d5dfc7`. **Plus** the declared kill-switch: `RL_ENTRY29B=0` on the full 29B tree reproduces `86c8d5d9` **byte-exact** |
| **20** | the identity gate, bit-exact, after one declared re-point | **HELD** — panel **12/12**, board-wide **800/800**, max ǀmine/price6−1ǀ **0.000e+00** on both, attribution residual **2.220e-16**, pins re-verified unmoved at exit. Code diff: **three lines** |
| **21** | Guard 5 green but for the inherited `fv` red | **HELD** — red on `fv` **alone** |
| **22** | pins move: board, rl_model, engine_head — and nothing else | **HELD** — **UNDECLARED MOVERS: NONE**. store, v0surf, config, band, bust_prior, peak_model, q97m, pvc_snapshot, register all asserted **UNMOVED** against real hashes |
| **23** | no book re-seal | **HELD** |
| **24** | no instrument re-point is needed | **HELD** — `EXPECT_STORE cb38ef11`, `EXPECT_V0SURF 4405cba2b42f`, `EXPECT_N 1200` all still hold. **29B re-points nothing** |
| **25** | the matrix store does not move; the yr0 **denominator** moves where the mark is a day-0 print | **PARTIAL — its second clause BREACHED.** Store/surface/population unmoved and the matrix md5 moves: **HELD**. But **0 of 2648** yr0 values moved: `emit_matrix_338.py:252` writes `v0 = v0_start(p)`, the frozen surface — **the instruments do not read the printed day-0 price at yr0 at all.** §14.6 |
| **26** | the arbitrages do not close; **direction** — the ND readings move *toward* the carry line | **HALF HELD, HALF BREACHED.** They did **not** close: HELD. They moved **AWAY**: **BREACHED**. −7.73% → **−18.01%**, −15.92% → **−20.93%**, and picks 21–64 crossed **+4.76% → −13.56%**. **3 of 10 arbitrages.** §14.6 |
| **27** | mark-path **10/10** and reverse no-arb **10/10** | **BREACHED on the first clause, HELD on the second.** Mark-path **6 of 10** (RD, PDN, PDS, ND>64 now peak at d0/d1); reverse no-arb **10 of 10 PASS, 0 fail** |
| **28** | `noarb_table_338.py` byte-identical `0f822035…` | **HELD** — computed at run |
| **29** | both ledgers reconcile exactly | **HELD** — **0 rows failing, max ǀresidualǀ 0**; the five lever sums add to live→final to the unit |
| **30** | nothing merges; PR #510 stays HELD | **HELD** |

**Twenty-seven held · one partial · two breached.** The three that did not hold are all in the same
place — the no-arb block — and they share one root cause, measured in §14.6. **Nothing here is scored
generously.**

## 14.2 THE BOARD

| stage | board md5 | total | Δ |
|---|---|---:|---:|
| LIVE | `88ce647f531030d8d2e094188b258191` | 752,429 | — |
| ORDER 29 FINAL | `86c8d5d9ba5b95e2cba05c78fbc31f78` | 706,018 | −46,411 |
| **ORDER 29B FINAL** | **`36d5dfc73e2b508ece530bc7dfae2090`** | **717,527** | **−34,902 vs live** |

| lever | movers | Σ delta |
|---|---:|---:|
| 1 — the unflag-three | 543 | −8,695 |
| 2 — the grace dial | 39 | +4,671 |
| 3 — the curve + v0 reprint | 200 | −4,372 |
| 4 — the numéraire scalar | 580 | −38,015 |
| **5 — THE ENTRY WIRING** | **89** | **+11,509** |
| **total** | **757** | **−34,902** — the five sums add to the live→final total **exactly** |

Levers 1–4 are read **verbatim** from ORDER 29's committed ledger; the instrument first asserts that
ORDER 29's `final` column equals the entry board row for row, so the two ledgers cannot compose on a
false basis. Lever 5 splits **ND +8,495 / pool +3,014**.

## 14.3 THE NAMED-ROW DAY-0 TABLE

`derived v0 × numéraire` is in board currency — the numéraire `s` is already inside both published
objects (`posv` is built on the shipped ladder; the cells carry `× anchor_factor == s`), so the printed
value is `round(derived v0)` and the identity is exact.

| row | object read | old print | **derived v0 × numéraire** | **new print** | Δ |
|---|---|---:|---:|---:|---:|
| `josh-smillie` | `posv[MID][7]` | 818 | 1616.974 | **1617** | **+799** |
| `harry-demattia` | `posv[MID][25]` | 379 | 891.822 | **892** | +513 |
| `max-knobel` | `posv[RUCK][42]` | 365 | 833.837 | **834** | +469 |
| `oskar-taylor` | `posv[SD][15]` | 501 | 945.957 | **946** | +445 |
| `logan-smith` | `cells[ND>64\|RUCK]` | 185 | 566.043 | **566** | +381 |
| `sam-allen` | `posv[MID][29]` | 563 | 839.585 | **840** | +277 |
| `brayden-george` | `posv[SF][26]` | 208 | 292.886 | **293** | +85 |
| **`kalani-white`** | **`cells[PDN\|KPF]` — BORROWED** | **84** | **92.35874340265629** | **92** | **+8** |
| `adam-sweid` | `posv[SF][25]` | 350 | 305.972 | **306** | −44 |
| `finnegan-davis` | `posv[SD][51]` | 132 | 89.028 | **89** | −43 |
| `cody-anderson` | `posv[SF][64]` | 60 | 17.992 | **18** | −42 |
| `reece-torrent` | `posv[MID][64]` | 76 | 56.657 | **57** | −19 |

The four fallers were **named in the prereg before measurement** (P29B-16). They fall because the
positional relativity in a thin part of the tail is well below 1 — `cody-anderson` at SF pick 64 is
the sharpest consequence of consuming the positional object rather than the position-blind ladder, and
it was published in advance so it could not be presented afterwards as a surprise. All 89 rows are
tabled in `PREREG_29B.md` §5–6 (predicted) and `docs/ledgers/LANDING_29B_MOVERS_2026-08-13.md`
(measured); the two agree row for row.

**The ten ORDER-29 named rows are all `+0` on this lever.** They have careers; the legacy legs price
them and this act does not touch the legacy legs.

## 14.4 THE FORK IN THE BRIEF, RESOLVED IN THE OPEN AND IN ADVANCE

The brief said "printed day-0 = derived v0 × numéraire … (the P12 harness's own definition)" **and**
"ND entrants: positional ND v0 at their pick". **Those two cannot be satisfied by one number:** P12's
harness compares to `curve[pick]`, the *position-blind* ladder, while `posv_g(p) = relat_g(p)·curve(p)`
and `relat_g ≠ 1` at essentially every (position, pick). The reconciliation
`Σ_g share_g(p)·posv_g(p) = curve(p)` is a **population** identity, never a per-row one.

`PREREG_29B` §0.3 resolved it **before any wiring was written**: the **population** is P12's, unchanged
(46 ND + the 43 `cg==0` pool rows the brief's pool clause names); the **value** is the row's own derived
v0, because wiring `curve[pick]` would leave `nd_v0` exactly as unconsumed as it was. **The legacy
position-blind reading is not dropped — `o29b_day0.py` prints it on every run**, and it reads 0/46 on
both boards, so the declared re-point is a number a reader can check rather than a sentence.

## 14.5 THE BORROWED CELLS — OWNER OPTION A, DERIVED NOT TYPED

| | |
|---|---|
| pool-wide KPF positional relativity `lens[KPF]` | **0.8318314538303738** (99 pool KPF rows, mean 189.276874 / pool aggregate 227.5423379495) |
| **`PDN\|KPF`** | 118.1061694003 × lens × 0.9400914291048137 = **92.35874340265629** → prints **92** |
| **`PDS\|KPF`** | 107.3879871441 × lens × 0.9400914291048137 = **83.97715038537063** → prints **84** |

At `n = 0` the K-shrink weight `w = n/(n+15)` is **0**, so `o28_derive.py:256`'s own expression
`w·own + (1−w)·path·lens` **collapses to `pathway_level × lens[KPF]`. The limiting case IS Option A** —
the ruling named the arithmetic the derivation already ran. `o29b_sign_cells.py` re-derives `lens[]`
and the pathway levels from the same inputs and its control **reproduces DERIVE28's own 54 cells at
max |err| = 0.000e+00** before it is permitted to write. The values reproduce ORDER 29's published
`declined_unsigned` **92.4 / 84.0 exactly** — the proof that the owner signed a declined number rather
than a new one.

**The guard is replaced, not removed.** A halt keyed on `unsigned_cells` could never fire once nothing
is unsigned, which is worse than no guard. In its place: a **coverage assert** over the whole store
pool population (**1202 of 1202** rows map to a signed cell — deliberately wider than the ordered
"active entrant"); `pool_v0_of()` remains the one accessor and still raises on a null; and its
non-vacuity is **proven on a real row every build** by temporarily nulling the heavily populated
`RD|MID` cell, requiring the raise, and restoring it. (That the `RL_ENTRY29B=0` build is byte-exact is
also the proof the restore is exact.)

## 14.6 **THE FINDING: THE ARBITRAGE DID NOT CLOSE — IT MOVED, AND GREW**

Full tables in `NOARB_MARGINS_29.md` **Part B**, appended beside the ORDER 29 readings rather than
over them.

| reading | LIVE | ORDER 29 | **ORDER 29B** | verdict |
|---|---:|---:|---:|---|
| all-arm PRIMARY, margin v14% | +33.23% | +28.71% | **+20.75%** | no arb |
| all-arm MODERN, margin v14% | +31.75% | +26.66% | **+18.11%** | no arb |
| legacy ND ALL picks 1–64 | +6.70% | **−7.73%** ARB | **−18.01%** | **ARB** |
| legacy ND picks 1–20 | +1.82% | **−15.92%** ARB | **−20.93%** | **ARB** |
| legacy ND picks 21–64 | +14.04% | +4.76% | **−13.56%** | **ARB — NEW** |
| mark-path progression | — | 10/10 PASS | **6/10 PASS** | **BREACH** |
| reverse no-arb | — | 10/10 PASS | **10/10 PASS, 0 fail** | HELD |

**ARBITRAGES: 2 of 10 → 3 of 10.** No literal was re-pointed; the live control still reproduces
`NOARB_MARGINS_V2` to the last digit (0 of 10 arbitrages), so the pipeline is sound and the movement is
real.

**THE MECHANISM, MEASURED — `o29b_noarb_why.py`:**

* **the instruments' year-0 is NOT the printed day-0 price.** `emit_matrix_338.py:252` writes
  `v0 = round(v0_start(p), 1)` — the **frozen year-zero surface** — while years 1…7 are `ev(p, Y)`.
  ORDER 29B wires `ev()`. Measured: **0 of 2648** `v0` values moved; the in-curve ND Σ`v0` is
  **byte-identical** at 1,707,328.
* **the numerator rose, concentrated at cohort years 1–2**: 54.5% of year-1 cells and 35.8% of year-2
  cells moved; in-curve ND Σ year-1 went **1,533,377 → 1,690,071, +10.22%**. 2,277 cells rose, 234 fell.
* **so the appreciation had to rise.** A day-0 print is a property of a player *at an as-of year*, and
  on a national-draft cohort the printed day-0 is overwhelmingly a **year-1** cell — a draftee who did
  not play his first season — never the year-0 cell.

**What that means, stated plainly: the gap P12 sized has been closed at day 0 and TRANSFERRED to the
yr0→yr1 step.** The year-1+ marks are still produced by the un-rewired legs, which this act is ruled
not to touch. Closing the entry gap without the year-1+ rewire does not remove the arbitrage — it
relocates it and makes it larger where it now sits.

The **mark-path** failures are the same mechanism seen through a shape test: **no arm's peak value
fell — all four that flip ROSE** — but the *shallow* marks rose further, so `RD`, `PDN`, `PDS` and
`ND>64` now peak at d0/d1 instead of d3–d6. **Reverse no-arb is a level test and is untouched:** 10/10,
smallest `max m(d≥1)` MSD **1.2379**, 24% above the failure line.

**A correction to §12.4.1, measured.** ORDER 29 found the landed marks lower at shallow and deeper
(−0.0332 / −0.0815) and called ORDER 28's read "optimistic". On the entry-wired marks the shape
**inverts** — shallow **+0.2134**, deep **−0.0747** — and ORDER 28's original prediction reads
**CONFIRMED**. Both numbers are real measurements of two different boards; both are recorded.

## 14.7 **THE OWED DECISION**

The wiring keys on **games as of Y**. That is why it reaches the historical matrix at all, and it is
the whole of §14.6. The alternative — keying on **career-total** games — is **one line** and would
leave every matrix cell except the 89 current entrants untouched: §14.6 would then read exactly as
ORDER 29 did, with 2 of 10 arbitrages and mark-path 10/10.

**This seat did not switch to it after seeing the reading. That would be tuning, and `PREREG_29B`
forbids it by name.** The as-of predicate was declared in **P29B-7 before any wiring was written**, and
it was declared because the brief itself asked for the yr0 denominator to move *"wherever the
instrument reads printed day-0"*. The measurement then found the instruments **do not** read the print
at yr0 — so the premise that selected the predicate was false about the plumbing.

**The owner owes a word on which predicate the day-0 print carries.** Both readings are on the table
and neither was suppressed.

## 14.8 THE CONTROLS

| control | status |
|---|---|
| byte-identity at entry | **PASS** — `86c8d5d9` exact, before the prereg was committed |
| **`RL_ENTRY29B=0` kill-switch on the FULL 29B tree** | **PASS — `86c8d5d9` BYTE-EXACT.** The strongest control in the act: it proves the wiring is the only thing that moves the board, that the borrowed cells are inert except through it, and that the guard's non-vacuity probe leaves no residue |
| deterministic double-build | **PASS** — two fresh workspaces, both `36d5dfc7` |
| printed-day-0 assert, on the WRITTEN board | **PASS — 89 of 89, tolerance 0.** Now a permanent boot-class check that HALTS the build and refuses to pass vacuously |
| pool v0 coverage assert | **PASS — 1202 of 1202**; non-vacuity proven on a real row |
| identity gate, one declared re-point | **PASS — 800 of 800 board-wide at `0.000e+00`**, residual 2.220e-16 |
| Guard 5 boot guard | **PARTIAL** — green but for the inherited `fv` red |
| pin moved-set asserted | **PASS** — no undeclared movers |
| LEG F5 #306 entrant reconciliation | **PASS, silently** — the entrant layer is occupancy × ladder and does not move. No re-seal |
| lever reconciliation, every row | **PASS** — 0 failures, max residual 0 |
| as-of matrix re-emitted under the wired engine | **DONE** — `ca24a49a`, 2648 records, identities unmoved |
| both cohort instruments on the 29B matrix | **RAN CLEAN — no re-point needed.** **3 of 10 ARBITRAGES** |
| both cohort instruments on the LIVE matrix (control) | **PASS** — reproduces `NOARB_MARGINS_V2` to the last digit, 0 arbitrages |
| mark-path progression | **6 of 10 — BREACH** |
| reverse no-arb | **PASS — 10 of 10, 0 pathways fail** |
| `noarb_table_338.py` unmodified | **PASS** — `0f822035…`, computed at run |

## 14.9 STATE

| | |
|---|---|
| branch | `land/order-29` |
| board | **`36d5dfc73e2b508ece530bc7dfae2090`** |
| store | `cb38ef1171dcf20aae66ebf12682be0d` — **UNMOVED** |
| `pvc_curve_v2.json` | `911774bc92de0630199a4cc0c6bfac42`, `curve_md5` **`9729f0c5` — payload UNMOVED** |
| `rl_model.py` | `14000af2a46f7a3c4cdfde303f5a1aff` |
| `_merged_recover.py` | `a353a9d361937a78014eef521cb65d68` |
| `v0surf.pkl` | `5dd34ca82735f5c8f021b1c7320df8f8` — **UNMOVED, no re-bake** |
| entrant seal | `cbb7c431` — **unchanged, no re-seal** |
| kill-switch | `RL_ENTRY29B` (declared, not a manifest dial; `config_sha256` UNMOVED) |
| PR | **#510, HELD — `[HELD — DO NOT MERGE]`** |

**NOTHING MERGES WITHOUT THE OWNER'S WORD ON THIS PACKET**, which now additionally includes the third
open arbitrage, the mark-path breach, and the §14.7 predicate decision as named merge considerations.

### Evidence index — ORDER 29B

| file | what |
|---|---|
| `PREREG_29B.md` | the thirty-one predictions, filed before any wiring, never edited |
| `o29b_sign_cells.py` · `SIGN29B.{json,_out.txt}` | Step 2: the borrowed cells derived, controlled against DERIVE28, and signed |
| `o29b_day0.py` · `DAY0_29B_{ENTRY,FINAL}.{json,_out.txt}` | Step 4: the identity instrument, both readings, both boards |
| `bb29b.sh` · `DETERMINISM29B.txt` | the staged board builder, the double-build and the kill-switch proof |
| `o29b_pins.py` · `PINS29B.{json,_out.txt}` · `bootguard29b.sh` · `BOOTGUARD29B.txt` | the restamp and Guard 5 |
| `o29b_gate.py` · `GATE29B.{json,_out.txt}` · `GATE29B_REPOINT.diff` | the identity gate, one declared re-point, three lines of code |
| `o29b_movers.py` · `MOVERS29B_out.txt` · `docs/ledgers/LANDING_29B_MOVERS_2026-08-13.{md,json}` | every player, five levers |
| `run_noarb_o29b.sh` · `NOARB_MARGINS_29B_out.txt` · `noarb29b/` | both cohort instruments, three bases |
| `o29b_noarb_why.py` · `NOARB_WHY_29B.{json,_out.txt}` | **why the margins moved: the mechanism, measured** |
| `o29b_instruments.py` · `INSTRUMENTS29B.{json,_out.txt}` · `INSTRUMENTS29B_REBASIS.diff` | mark-path + reverse no-arb |
| `NOARB_MARGINS_29.md` **Part B** | the owner-facing tables, ORDER 25 layout, live vs 29 vs 29B |

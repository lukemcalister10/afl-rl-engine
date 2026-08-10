# THE COMPOSITION ACT — THE SIDE-BY-SIDE

Branch `landing/334-composition`, **HELD — nothing merges, no attribution column registers, before
the owner's adoption word.** Base `origin/main`. Store `d9a24282` unchanged throughout — this act
writes no store.

---

## 0. READ THIS FIRST — TWO PRE-REGISTERED GATES FAILED, AND ONE IS STRUCTURAL

### ⛔ THE RELATIVITY GUARD FAILED

Defined and its expectation **committed before any of these boards existed** (`RELATIVITY_GUARD.md`,
`93e9cd0`). Registered expectation: RELATIVITY should **rise or hold** — the package should narrow
the peak-vs-young gap, never widen it.

| board | YOUNG | PEAK | RELATIVITY | Δ(pp) |
|---|---|---|---|---|
| main (pre-act) | 101,209 | 233,430 | 0.433573 | |
| + ITEM B | 102,799 | 233,723 | 0.439833 | +0.626 |
| + era removal | 102,799 | 233,394 | 0.440453 | +0.688 |
| + #336 (BASE) | 96,535 | 228,072 | 0.423265 | −1.031 |
| **FULL ACT** | **93,332** | **226,347** | **0.412340** | **−2.123** |

**0.433573 → 0.412340, a fall of 4.897%.** Not rebalanced to pass; no component retuned to move it.

**The mechanism.** The pick block is constant at 39,949 on every board (this act does not touch the
ladder), so the entire move is in players. Setting the picks aside:

- **young players (rung ≤ 1): 61,260 → 53,383, −12.9%**
- **peak players (rung 4-6): 233,430 → 226,347, −3.0%**

**Young players are cut four times harder than peak players.** The larger contributor is **#336**
(−1.03pp of the −2.12pp): putting never-established players into the par denominator lowers the
reference, and a young player's price leans on that reference far more than an established
player's does. The dials (A + C + E1 + H + SUR) add the remaining −1.09pp.

**This is the owner's own stated worry arriving as a measurement** — the Robey question, *"picks
are fixed in value, year 1 players have dropped so much that the 1.57 year 0 to 5 issue may now
just be a bigger ratio at year 1 to 5 instead? Robbing peter to pay paul?"* Sullivan Robey is
himself a **−449** mover here, every point of it #336.

### ⚠ THE MRAZ RATIO, AND A CURRENCY ERROR OF MINE

Post-act **3,555 → 1,649**:

- **2.939×** comparing board price directly to the pick-35 curve value 561.0
- **3.093×** converting to ladder currency (board × 1.0524) — **the correct comparison**, because
  561.0 is a ladder number and the board is not

I calibrated `RL_SUR_W = 4.0` against the raw 2.939 figure. On the currency-correct reading he lands
**3.093×, marginally above the ruled 3× top**. My own earlier Mraz probe printed both currencies
side by side and I then used the wrong one.

**The two constraints pull against each other, which is why this needs the owner and not a seat.**
Raising the dial to bring Mraz inside 3× cuts thin-record young rows harder — and the relativity
guard has already failed *because* young rows are being cut too hard. Tightening Mraz makes the
relativity breach worse. **They cannot both be satisfied by moving this dial, so I did not move it.**

### ⚠ ITEM E1 MISSES ITS RULED BAND

The ruck book moves **+0.50%** at `RUC_WAGE = 1.0`, i.e. at the **full standard** age wage ramp.
The ruled cautious band is **[+2.9%, +9.0%]**. Reaching +2.9% would require `RUC_WAGE > 1` — *more*
than the standard ramp, contradicting the ruling's own words. Mechanism: the ramp is
`clip(1−(age−20)/6, 0, 1)`, ~1 at age 20 and 0 by 26, and most listed rucks are older, so ending the
pole denial hands most of them almost nothing. **E1 ships as ruled and under its band, flagged.**

---

## 1. THE BOARD

| board | total | Δ vs main | ratio |
|---|---|---|---|
| main (pre-act) | 761,574 | — | 1.000000 |
| + ITEM B | 765,202 | +3,628 | 1.004764 |
| + era removal | 764,492 | +2,918 | 1.003832 |
| **+ #336 / A / C / E1 / E2 / H / SUR** | **723,861** | **−37,713** | **0.950480** |

**668 movers — 84 up, 584 down.** The act cuts the board ~5%, dominated by #336.

## 2. PER-ITEM BOOK DELTA

| item | book delta | ratio | movers | conservation |
|---|---|---|---|---|
| **B** | +3,628 | 1.004764 | 110 | Σ entry_anchor held **exactly** (2.978e-15); the board is not conserved because the anchor reaches price through a **one-sided floor** — see §3 |
| **era** | −710 | 0.999072 | 26 | not a conservation item; 26 of 26 movers KPF, all cuts |
| **#336** | −26,875 | 0.964846 | 567 | a reference re-derivation, not a conserved transfer |
| **A** | −1,400 | 0.998070 | 62 | funded by the re-teach (§3) |
| **C/E2** | +104 | 1.000144 | 31 | funded by the H cuts |
| **E1** | +329 | 1.000455 | 9 | within the ruck book; **under band** |
| **H** | −8,622 | 0.988229 | 70 | **it is the funding** |
| **SUR** | −4,211 | 0.994216 | 50 | a trust correction, not a transfer |

## 3. CONSERVATION — SHOWN, NOT ASSERTED

- **ITEM B**: pool Σ entry_anchor **293,166.0156 → 293,166.0156**, delta 2.978e-15 relative, and
  the law is now a **build-time assertion** — a broken gradient halts the build rather than drifting.
  **But the board is not conserved (+3,628)**, and that is mechanical rather than a wiring error:
  the anchor reaches price through `max(v, floor_frac × anchor)`, a one-sided floor. Raising an
  anchor can lift a price; lowering one only cuts while the floor still binds. **An asymmetric
  transform of a conserved input does not conserve its output.** This is funding the package must
  account for, and it is recorded as an input to the re-teach rather than absorbed quietly.
- **ITEM D**: **PARKED** by owner ruling — no sit-charge tilt ships, the sitter pool keeps its
  current charges.
- **ITEM H**: is the funding, by design. −8,622.
- **The #326 floor (0.45) is untouched. No blanket lifts anywhere** — every H factor is ≤ 1.

## 4. TOP MOVERS WITH PER-ITEM ATTRIBUTION

Columns are kill-switch differences; the **residual is printed, never distributed**.

| player | pos | before | after | total | B | era | 336 | A | C/E2 | E1 | H | SUR | resid |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Noah Mraz | KPD | 3555 | 1649 | −1906 | 0 | 0 | −214 | 0 | 0 | 0 | 0 | **−1692** | 0 |
| Max Hall | SF | 2855 | 1721 | −1134 | 0 | 0 | −58 | 0 | 0 | 0 | **−1076** | 0 | 0 |
| John Noble | SD | 2192 | 1330 | −862 | 0 | 0 | −29 | 0 | 0 | 0 | −833 | 0 | 0 |
| Nicholas Martin | MID | 3655 | 2814 | −841 | 0 | 0 | −62 | −76 | +1 | 0 | −685 | 0 | −19 |
| Harry O'Farrell | KPD | 949 | 200 | −749 | 0 | 0 | −150 | **−599** | +10 | 0 | 0 | 0 | −10 |
| Mark Keane | KPD | 1529 | 914 | −615 | 0 | 0 | −42 | 0 | 0 | 0 | −573 | 0 | 0 |
| Tom McCarthy | SD | 1481 | 892 | −589 | 0 | 0 | −29 | 0 | 0 | 0 | −560 | 0 | 0 |
| Lachlan McAndrew | RUCK | 1252 | 743 | −509 | 0 | 0 | −44 | 0 | 0 | 0 | −465 | 0 | 0 |
| Thomas Sims | KPF | 1069 | 562 | −507 | 0 | 0 | −22 | −485 | +11 | 0 | 0 | 0 | −11 |
| Sullivan Robey | MID | 3067 | 2618 | −449 | 0 | 0 | **−449** | 0 | 0 | 0 | 0 | 0 | 0 |
| James Peatling | MID | 1116 | 677 | −439 | 0 | 0 | −16 | 0 | 0 | 0 | −423 | 0 | 0 |
| Xavier Lindsay | MID | 2092 | 1659 | −433 | 0 | 0 | −404 | −29 | +3 | 0 | 0 | 0 | −3 |
| Marcus Herbert | SD | 1060 | 627 | −433 | 0 | 0 | −40 | 0 | 0 | 0 | −393 | 0 | 0 |
| Taj Hotton | MID | 2296 | 1869 | −427 | 0 | 0 | −427 | 0 | 0 | 0 | 0 | 0 | 0 |
| Oscar Ryan | SD | 701 | 306 | −395 | 0 | 0 | −32 | 0 | 0 | 0 | 0 | −363 | 0 |
| Dyson Sharp | MID | 3182 | 2796 | −386 | 0 | 0 | −386 | 0 | 0 | 0 | 0 | 0 | 0 |
| Harry Dean | KPD | 2703 | 2328 | −375 | 0 | 0 | −375 | 0 | 0 | 0 | 0 | 0 | 0 |
| Luke Trainor | KPD | 1546 | 1174 | −372 | 0 | 0 | −372 | 0 | 0 | 0 | 0 | 0 | 0 |
| Alix Tauru | KPD | 1650 | 1280 | −370 | 0 | 0 | −370 | 0 | 0 | 0 | 0 | 0 | 0 |
| Isaac Kako | SF | 1378 | 1015 | −363 | 0 | 0 | −363 | 0 | 0 | 0 | 0 | 0 | 0 |

**Total |residual| = 344 over 668 movers — mean 0.5 per mover.** The columns sum to each player's
total move to within half a point.

## 5. THE ITEMS, AS BUILT

| item | what shipped |
|---|---|
| **I** | Restated on the ORIGINAL ruler (alignment gate PASS, exact match to the seam's re-run). ND year-0 contrasts **CLEAN** — precondition met. Presented under the LEVEL LAW: the common level stated once as a numeraire property, contrasts only. |
| **B** | Pool year-0 age gradient **0.6859 / 1.4112 / 2.8173** (filed 0.666 / 1.200 / 2.474), continuous in draft age, C5-conserving, build-time asserted. Age-unknown cell empty on this store, rule still coded. |
| **A** | LAM_SIT's ramp carried past `ns==0`, faded on cumulative evidence. Fade **v1 0.359 → v2 0.145 → v3 0.058 → v4 0.024 → v5 0.010 → v6 0.004** — the ruled property exactly. Blends at `ev()`, never `raw_ev`. |
| **C** | Cap release on A's anchor leg, `w = G·Q·gate`, **H = 1.13**. w=0 → old cap exactly. One `sa` reader. |
| **C-Q3** | **Demonstration succeeds** — 24 of 67 top-10-pick rows protected. **z gate ships; the `sa` fallback does not install** (it would let Ugle-Hagan and Logan McDonald through at gate 1.0). |
| **D** | **PARKED** by owner ruling. Derivation filed: corrected contrast 1.1041, CI [0.548, 2.157] covering 1. |
| **E1/E2** | Ruck pole denial ended (**under band, flagged**); ruck ceiling evidence-yielding via C's w. |
| **H** | Ruled cuts as filed, cell-qualified and composing. #326 floor untouched. |
| **salvage 1** | Era removal — pre-registration met on all three axes (26 movers, all KPF, all cuts, ratio 0.999072 vs branch 0.998986). |
| **salvage 2** | #336 reference layer, ported as 13 hunks. |
| **salvage 3** | Surprise law, dial re-calibrated to **4.0** (the ordered ladder said 5.0; 4.0 is the true boundary). Interaction guard with A: **0 of 644 qualifying rows move**. |

## 6. PARKED — RE-MEASURE AFTER THIS LANDS

F1 · the SF band (item G) · **ITEM D** · **the quiet-starter cells** (stage-5/6 G tables, withdrawn
in favour of A+C; measurements stay filed) · E3 ruck residual · the F2 breakpoint · the #326 floor
level · the `ship_gates_check.py` gate-mode `RL_GAMMA` conflict (its own repair item).

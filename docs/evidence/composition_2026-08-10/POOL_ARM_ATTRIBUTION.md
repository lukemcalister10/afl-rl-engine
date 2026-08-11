# ORDER 6 — WHY THE POOL ARM WAS SLASHED. ATTRIBUTION, MECHANISM, AND A HALT-GRADE DISCLOSURE FAILURE

**Owner challenge, verbatim:** *"I notice comparing main to these that a lot of /SSP/MSD players have
been slashed - Noble, Hall, McCarthy, PEatling, Herbert, Keane etc. Is there a reason for that? I
understand if the value of MSD/pool has gone down, but have players like Noble and Peatling not
established themselves on their own production more than their draft arm? And Max Hall nearly halving
his value seems unkind?"* — and on the inversion: *"an odd dynamic?"*

**Attribution and disclosure only. No repair, no retune, no new dials beyond ablation. Nothing is
adopted and nothing ships.**

---

## 1. THE ANSWER IN ONE LINE

**It is ITEM H, and it is one constant.** Every one of the named players is multiplied by
`H_MATNONRD = 0.615` — a flat 38.5% cut — applied at `engine/rl_after/_merged_recover.py:2228` to the
**final production-led price**, keyed on three things and three things only: *is he pool*, *is his type
not RD*, *was his draft age ≥ 21*. **It reads no games, no level, no establishment.**

**And the owner's question has a mechanical answer: NO.** Their own production does not protect them,
because the factor is applied *after* all the production machinery, as a multiplier on the result.

## 2. PER-ITEM ABLATION — single-item removal at the branch tip

Each column is that item removed from FULL, so a positive number is what the item was taking away.

| player | type | draft age | main | FULL | cut | **+noH** | +noA | +noSUR | +noC | +noE1 | +no336P | +no336E | +no336C |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| John Noble | MSD | 22.0 | 2192 | 1330 | −39.3% | **+833** | 0 | 0 | 0 | 0 | −1 | +18 | −1 |
| Max Hall | MSD | 22.0 | 2855 | 1721 | −39.7% | **+1076** | 0 | 0 | 0 | 0 | −1 | +24 | +11 |
| Tom McCarthy | MSD | 25.0 | 1481 | 892 | −39.8% | **+560** | 0 | 0 | 0 | 0 | 0 | +14 | +6 |
| James Peatling | MSD | 21.0 | 1116 | 677 | −39.3% | **+423** | 0 | 0 | 0 | 0 | 0 | +9 | 0 |
| Marcus Herbert | MSD | 24.0 | 1060 | 627 | −40.8% | **+393** | 0 | 0 | 0 | 0 | −1 | +9 | +16 |
| Mark Keane | SSP | 22.0 | 1529 | 914 | −40.2% | **+573** | 0 | 0 | 0 | 0 | 0 | +12 | +13 |
| Lachlan McAndrew | SSP | 22.0 | 1252 | 743 | −40.7% | **+465** | 0 | 0 | 0 | 0 | −1 | +11 | +17 |
| Cooper Sharman | MSD | 21.0 | 450 | 265 | −41.1% | **+165** | 0 | 0 | 0 | 0 | 0 | +4 | 0 |
| **Noah Mraz** *(control)* | ND | 18.0 | 3555 | 1649 | −53.6% | **0** | 0 | **+1692** | 0 | 0 | −1 | +16 | +57 |

**The control works exactly as intended.** Mraz's cut is the **surprise law** (+1692 restores him to
3341 of his 3555), and `noH` moves him by **zero** — he is a national draftee at draft age 18, outside
the cell. So surprise-law cuts and arm cuts are cleanly separated, and none of the named pool players'
cut is the Mraz correction.

## 3. IS THE NEAR-UNIFORMITY ONE MECHANISM OR COINCIDENCE? — one constant, to four decimals

| player | FULL | H-restored | **FULL ÷ restored** |
|---|---|---|---|
| John Noble | 1330 | 2163 | **0.6149** |
| Max Hall | 1721 | 2797 | **0.6153** |
| Tom McCarthy | 892 | 1452 | **0.6143** |
| James Peatling | 677 | 1100 | **0.6155** |
| Marcus Herbert | 627 | 1020 | **0.6147** |
| Mark Keane | 914 | 1487 | **0.6147** |
| Lachlan McAndrew | 743 | 1208 | **0.6151** |
| Cooper Sharman | 265 | 430 | **0.6163** |

`H_MATNONRD` as filed is **0.615**. **It is not a coincidence and it is not several items composing —
it is literally the one constant**, recovered to four decimals on eight independent players.

**Independent cross-check from the commit history**, not from dials: the board built at `7f4e79b` (the
commit *before* ITEM H landed) has md5 `a44dd93d86e2b2d2e7c6130f048e9845` — **byte-identical to the
FULL board with `RL_ITEM_H=0`**. And the board at `897c212` (the ITEM H commit) is
`846560dc1b206996005c7c9e9290207c`, **byte-identical to FULL**. So ITEM H is the only price-moving
change between those points, and everything landed after it is price-inert.

## 4. WHO ITEM H ACTUALLY MOVES — the honest census, which is smaller than the cell

The mature-nonRD **cell** contains **165** store rows. But only **70 active board rows** move when H is
removed (the rest are off the active board or have another constraint binding). Of those 70, **18 sit
exactly at the 0.615 constant**; the others compose with the sitter cells or hit floors.

- aggregate over the 70 movers: FULL **15,045** vs noH **23,667** → H removes **36.4%** of their value
- as a share of the whole board: **1.19%** of board total

**By career games — the owner's question, answered with numbers:**

| career games | n | median cut | total taken |
|---|---|---|---|
| 0 | 43 | −19.6% | 2,421 |
| 1-19 | 14 | −37.9% | 1,280 |
| 20-49 | 6 | −29.2% | 2,179 |
| 50-99 | 5 | −38.4% | 1,880 |
| **100+** | **2** | **−28.9%** | **862** |

**Production buys no protection.** A 158-game player takes the same 0.615 as a zero-game one. Within
the cell, **47.9%** (79 of 165) have established by the engine's own ≥6-game definition, **9** have 100+
career games, and the deepest cuts by median are in the *played* buckets, not the zero-game bucket.

## 5. THE MECHANISM — which code path makes an established pool entrant depend on his entry arm

Measured per channel for the named players (`_h_cut`, `_a_share`, `_b_shape`, `entry_anchor` all called
directly on the live engine at Y=2026):

| channel | file:line | does it still bind an established pool entrant? |
|---|---|---|
| **ITEM H multiplier** | `_merged_recover.py:1999-2011`, applied `:2227` (sit-out arm) and **`:2228`** (year-1+ arm) | **YES — fully, and unconditionally.** `_h_cut` = **0.6150** for Noble (158 games), Hall (44), McCarthy (30), Peatling (88), Keane (63). It reads `_pool`, `type`, `_b_age` — never games. |
| ITEM A anchor leg (`entry_anchor` via `_a_blend`) | `_merged_recover.py:2013-2050`, `2103-2113` | **NO.** `_a_share` = **0.000000** for every named player. The evidence fade `exp(−E_q/τ)` has already retired the entry anchor for them. Mraz, by contrast, carries `_a_share` = 0.358873. |
| surprise law | `_merged_recover.py:1932-1947` | **NO** — it is the `ns==0` sit-out arm only. `noSUR` moves all eight named players by **0**. |
| `basepk_c_p` class baseline, keyed on `effpk` | `rl_model.py` (5 enumerated consumers) | **Partly, but as a RATIO not a level.** Every pool entrant collapses to `effpk = 65` (the single pool index), so his class baseline is the pool band. It enters as `relative = (peak_est / basepk_c_p)^2.2` — his own peak against his class, not a carry of his entry price. |
| par band | `_merged_recover.py:2225` via `PR.par_at(pos, min(effpk,KMAX), T)` | same shape — pool-band keyed, entering as a ratio. |

**So the entry-arm-dependent share of Noble's and Hall's price is:**

| | Noble | Hall |
|---|---|---|
| price at main | 2192 | 2855 |
| price at FULL | 1330 | 1721 |
| **share removed by the entry-arm factor (ITEM H)** | **38.5%** | **38.5%** |
| share carried by his entry anchor through ITEM A | **0.0%** | **0.0%** |
| his entry anchor as an object | 616.3 | 616.3 (identical — the pool arm has one level per division, so their anchors are the same number despite 158 vs 44 games) |

**The owner is right on the mechanics.** Noble and Peatling *have* established themselves on their own
production — the engine's own evidence fade says so, and retires their entry anchor to a weight of
exactly zero. The 38.5% they lose is **not** their draft arm re-asserting itself through the valuation.
It is a flat cell multiplier applied on top of the finished price, and the only thing it asks about
them is how old they were on draft day.

## 6. ORDER 6a — THE INVERSION: TWO INDEPENDENT ITEMS ON THE SAME ARM

The speculative rows and the established rows are moved by **different items in opposite directions**.

| player | type | draft age | games | main | FULL | move | owning item |
|---|---|---|---|---|---|---|---|
| Flynn Perez | SSP | 24.0 | 31 | 113 | 232 | **+105.3%** | **ITEM B** (`afterB` +119 = 100% of it) |
| Paddy Cross | SSP | 23.0 | 10 | 113 | 232 | **+105.3%** | **ITEM B** (+119) |
| Zac Banch | MSD | 22.0 | 10 | 128 | 263 | **+105.5%** | **ITEM B** (+135) |
| Mitch Podhajski | MSD | 21.0 | 2 | 101 | 245 | **+142.6%** | ITEM B (+102) then H (−) and the surprise law (+) |

**ITEM B's effective entry-anchor factor, computed from the live renormaliser `k = 0.726863`:**

| draft age | `_b_shape` | **× k** | effect on the entry anchor |
|---|---|---|---|
| 18 | 0.6859 | **0.4985** | **−50.1%** |
| 19-20 | 1.4112 | 1.0257 | +2.6% |
| **21+** | 2.8173 | **2.0478** | **+104.8%** |

**+104.8% is the +105.3% the owner saw, to a rounding.** One number explains the whole speculative lift.

**Why the same cell moves both ways.** ITEM B multiplies the **entry anchor**; ITEM H multiplies the
**final price**.

- For a pool entrant with **no meaningful production**, the price *is* essentially the anchor → he takes
  B's **+105%** more or less in full.
- For a pool entrant **with real production**, the anchor has already been faded to weight zero → B's
  +105% barely reaches his price at all, and then H removes **38.5%** of the whole thing.

**VERDICT ON THE COORDINATOR'S QUESTION: TWO INDEPENDENT ITEMS, NOT ONE MECHANISM.** ITEM B is not
funding ITEM H. They were ruled separately, they act on different objects, and they happen to land on
the same arm with opposite signs. The net effect is that the mature-drafted pool arm now pays its
established players less and its unproven ones more — which is the inversion, and the owner's
"odd dynamic" is exactly correct.

## 7. ITEM B'S CONSERVATION — over WHAT set the level was preserved

The assert (`_merged_recover.py:2402-2414`) is real and it holds at **2.978e-15**. But it is narrower
than it reads:

> **the quantity conserved is Σ ENTRY ANCHOR over the LIVE POOL POPULATION (n = 1202) — a YEAR-ZERO
> object. It is not board prices, and it is not any subset.**

Measured on the same population:

| set | Σ entry anchor before → after | move |
|---|---|---|
| whole live pool (n=1202) — **the assert's set** | 293,166.0156 → 293,166.0156 | **+0.0000%** ✓ |
| established subset (≥1 season of ≥6 games), n=516 | 128,781.1 → 144,476.4 | **+12.19%** |
| no-evidence subset (0 career games), n=515 | 122,560.4 → 103,286.0 | **−15.73%** |
| **the live BOARD** (prices, 110 movers) | — | **net +3,628** (75 up at median **+100.0%**, 35 down at median **−50.0%**) |

**So: conservation held over the object it was asserted over, and over no other.** It was never a claim
about prices, and the coordinator's suspicion is right that it was not over these rows. On the board
ITEM B is **net positive**, and the two medians (+100.0% and −50.0%) are precisely the two knots
`k × 2.8173` and `k × 0.6859`.

## 8. HALT-GRADE — THE DISCLOSURE FAILURE

### 8.1 The arm is outside every deciding figure

The canonical no-arb population, taken by calling the harness's own loader:

> **n = 1197, and it is 100% type ND. Pool rows in the deciding population: ZERO.**

The emitted matrix carries **1080 pool-arm rows** (691 RD, 106 MSD, 57 IRE, 59 UNR, 52 SSP, 51 PDA, 43
PDN, 21 PDS) — **not one of them enters any figure that any ruling was made on.** Every yr1/yr4/margin
number in MENU.txt, in the decomposition, in the side-by-side, is picks 1-64 national draft only.

### 8.2 ITEM H's own derivation halted, and the interval cannot exclude "no cut"

From `item_h_derive_out.txt` and `PHASE2.md:201-206`, in front of the owner at the ruling:

| cell | ruled | F bent | F corrected | **CI** | eff-n |
|---|---|---|---|---|---|
| named union sitters | 0.280 | 0.1670 | 0.2301 | [0.010, 0.639] | 60.3 |
| all-pool-sitters | 0.804 | 0.3484 | 0.2974 | [0.185, 0.422] | 551.0 |
| **mature nonRD** | **0.615** | **0.7676** | 0.5162 | **[0.115, 1.226]** | **46.2** |

The script's own words: **"HALT-NO-SURPRISE… The cut factors are therefore NOT re-derived; they are
taken AS FILED."** For mature nonRD the corrected-ruler confidence interval is **[0.115, 1.226]**, which
**contains 1.0** — the evidence in front of the owner could not exclude *no cut at all*.

### 8.3 What the ruled evidence does NOT contain

Searched across the directive, `README.md`, `PHASE2.md` and `SIDE_BY_SIDE.md`:

- the directive carries **one line** (`:197-202`): the cut list, cell-qualified, factors named;
- `PHASE2.md` carries the derivation table above, with the halt and the CI;
- **NO board-effect figure for the pool arm appears anywhere.** No count of affected players, no
  aggregate, no split by career games, no named established player, no statement that a 158-game
  MSD recruit takes the same multiplier as a zero-game one.

> ### THE FINDING, STATED AS THE ORDER REQUIRES
>
> **ITEM H's mature-nonRD cut applies a flat 38.5% reduction to established players on an arm that
> appears in NO deciding figure, was sized from a cell whose own corrected-ruler interval [0.115,
> 1.226] cannot exclude "no cut", was taken AS FILED after its derivation script HALTED, and its
> board effect on established pool players was never disclosed in any evidence the owner ruled on.**
>
> **The side-by-side cannot proceed with an unruled arm-wide 38.5% cut inside it.**
>
> The same finding applies, in the other direction, to **ITEM B**: a **+104.8%** entry-anchor lift on
> every 21+-drafted pool entrant, whose conservation law was asserted over an object (Σ entry anchor)
> that is not the thing that moved (prices, net **+3,628**), and whose board inversion against ITEM H
> was never put in front of the owner either.

**Nothing here is repaired.** No factor is changed, no dial is added beyond the ablation switches that
already existed, and no candidate is proposed. This is attribution and disclosure, and the ruling is
the owner's.

## 9. WHAT COULD NOT BE BUILT, stated rather than hidden

Boards at four intermediate commits **cannot be built** and their arms were obtained by dial ablation
at the tip instead:

| ref | item | result |
|---|---|---|
| `55bafa9` | ITEM B (first landing) | **halts** — `#326 HALT: 1202 pool entrant(s) do not price off their own division level`. The *next* commit (`aa1693b`) taught that guard about ITEM B. Verified by diff: `aa1693b` changes **only** the two asserts and adds the B conservation check — **no pricing code** — so `aa1693b` is ITEM B's price effect exactly, and that is what section 6 uses. |
| `9a8bbd9` | #336 | halts (identity/guard) — covered by the three channel dials |
| `ced1512` | ITEM A | halts — covered by `RL_ITEM_A=0` |
| `16155f3` | surprise law | halts — covered by `RL_SUR_W=0` |

This is the documented behaviour recorded in `build_board_switch.sh`'s own header: an intermediate
commit's `expected_boot.json` carries pre-port identities and Guard 5 correctly refuses to boot.

## 10. REPRODUCTION

```
bash build_board_switch.sh <out> RL_ITEM_H=0      # and RL_ITEM_A=0 / RL_SUR_W=0 / RL_C_H=1.0 /
                                                  # RL_RUC_WAGE=0.0 / RL_336_NOP=1 / RL_336_SURVLVL=1
                                                  # RL_336_CLAMP=1 / RL_336_PARSURV=1
bash build_board_at.sh origin/main <out>          # 4b448a821f54180182637983f7a26a9d
bash build_board_at.sh aa1693b   <out>            # 52f70e68f4ea771f291f3ba92d23eac5  (ITEM B landed)
bash build_board_at.sh 6d3d4e2   <out>            # 19c4e26c51ed9bbc0c92e5cb56781bec  (era removal)
bash build_board_at.sh 7f4e79b   <out>            # a44dd93d86e2b2d2e7c6130f048e9845  (== FULL, H off)
bash build_board_at.sh 897c212   <out>            # 846560dc1b206996005c7c9e9290207c  (== FULL)
python3 pool_arm_probe.py                         # the per-channel and conservation measurements
```

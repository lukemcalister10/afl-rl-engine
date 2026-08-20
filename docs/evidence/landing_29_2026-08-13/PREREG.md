# PREREGISTRATION — ORDER 29, THE LANDING BUILD

**2026-08-13 · branch `land/order-29` cut from `origin/build/grace-adoption` `de8a98f` · build seat**

> **FILED BEFORE ANY MEASUREMENT.** No board has been built on this branch by this seat. No store byte
> has moved. No curve has been wired. Nothing below is a report; every line is a prediction that can
> fail, and every failure is owned **by number** in `SHIPPING_PACKET_29.md`. This file is never edited
> after its commit — corrections are appended to the packet, not smuggled back into the predictions.

Authority: register **v715** (`main` `ed6bd31`, `docs/OPEN_ITEMS_REGISTER.md`). Basis:
`docs/evidence/grace_adoption_2026-08-13/SHIPPING_PACKET_28.md` (ORDER 28, nothing landed).

---

## 0. THE FACTS THIS SEAT TOOK AS GIVEN BEFORE PREDICTING (read, not measured)

Stated so the predictions below are auditable against what was already on the branch:

| fact | source, read at design time |
|---|---|
| live board md5 `88ce647f531030d8d2e094188b258191` | `engine/rl_after/rl_app_data.json` |
| live store md5 `d9a24282357cf3083b1640466e3ecd83` | `engine/rl_after/rl_model_data.json` |
| the three flagged rows: `dylan-shiel` ND 2011 pick 4, `jeremy-cameron` ND 2011 pick 12, `adam-treloar` ND 2011 pick 14 | store scan; they are the **only** three `_pvc_exclude` rows in the store |
| candidate curve pre-anchor head `3191.1789716631`, anchor factor `0.940091429105` | `docs/evidence/grace_adoption_2026-08-13/DERIVE28.json::candidate` |
| live numéraire block: `pooled_head_pre_scale 3017.9232`, `s 0.9940610814748366`, `published_pin 3000.0` | `engine/rl_after/pvc_curve_v2.json::numeraire` |
| the ORDER-28 derivation lane (Layer 1 / Layer 2) **already carries all three 2011 rows un-excluded at their natural picks** | `inputs/LAYER2.json::attribution`, `inputs/layer1_player_seasons.json` |
| pool cells `PDN|KPF` and `PDS|KPF` have **n = 0** fit rows | `inputs/LAYER2.json::fit_pool_keys` × Layer-1 `position_group` |

---

## 1. THE PREDICTIONS

### P1 — BYTE-IDENTITY AT ENTRY (the stop-gate)
A full board rebuild from a clean staged copy of this branch's engine, dial OFF, reproduces
**`88ce647f531030d8d2e094188b258191`** exactly. If it does not, the build STOPS at step 0 and reports.

### P2 — THE UNFLAG-THREE, STRUCTURAL
After deleting the three `_pvc_exclude` flags and **nothing else**:
* the store carries **zero** `_pvc_exclude` rows (3 → 0);
* the ND-2011 cohort is **81 rows** with **zero duplicate picks**;
* all three rows are curve-contributing (`_in_pvc` true) at their stored picks 4 / 12 / 14;
* the diff against the live store is exactly **three deleted keys** — no value, pick, position, birth
  year or games field moves on any row.

### P3 — THE THREE INDIRECT MOVERS (the curve cells the three feed)
The flags do **not** gate the ORDER-28 derivation lane (§0). What they gate is the **engine's own
v3.4 kernel curve** (`build_pvc_v34`), through two channels, both of which are predicted to fire:
1. **direct contribution** — the three careers enter `_curve_sample` at picks 4 / 12 / 14 (window ±4);
2. **the slide-up unwind** — `rl_model.py:317-327` slides every *other* ND-2011 row up by the number
   of excluded picks north of it. Unflagging removes that slide, so the whole 2011 ND cohort's
   curve attribution moves by up to **3 picks**.

**Predicted**: the v3.4 pre-anchor head `PVC[1]` moves (pick 1's ±4 window contains pick 4), therefore
`BOARD_FACTOR = (_P1/PVC[1])·s` moves, therefore **every board row moves** through this channel as
well as through the numéraire. The per-pick deltas of the engine's own curve are **enumerated** in the
packet; nothing is asserted without its number. **Predicted magnitude: |Δ| on the v3.4 head under 3%.**

### P4 — GRACE-A ON AS CODE DEFAULT
With `RL_GRACE` defaulted ON in `engine/rl_after/rl_model.py` and added to the pinned manifest:
`RL_GRACE=0` in the environment still reproduces the **dial-off** behaviour byte-for-byte on an
otherwise-unchanged tree (the dial stays a real dial, it merely inverts its default), and the
grace-A law is unchanged from ORDER 28 — entry age ≤ 19 ⇒ seasons 1 and 2 full, age-21 first
diminished; entry 20+ ⇒ nothing; `grace_years(p)` keys on `p['year'] − by(p)`.

### P5 — THE MONOTONE HYBRID CURVE, WIRED
`pvc_curve_v2.json::curve` becomes the ORDER-28 candidate, rounded to int as the artifact schema
requires: head **3000**, seam pick **56**, tail zone **57–64**, pick 64 in the **179-class**, strictly
non-increasing over 1–64 (the artifact's own `r104_9_strict_descent` self-declaration is re-checked,
**not assumed**). No southern loclin extrapolation. Predicted spot values (int):
`1→3000 · 2→2668 · 3→2569 · 5→1804 · 7→1319 · 10→1319 · 15→812 · 20→812 · 30→607 · 40→479 · 50→274 · 64→179`.

### P6 — CONSERVATION LEDGER
Weighted `Σ n_p·v_p` conserved by the PAVA step to floating point (**`0.000e+00`**); plain `Σ v_p`
conserved to **0.0000%**; the anchor (pick 1) untouched by both the boundary and the monotone step.
Rounding to int for the artifact introduces a drift predicted **< 0.05%** on the plain sum, and that
drift is printed rather than absorbed.

### P7 — POSITIONAL ND v0s, CONTINUOUS PER PICK
Six positional v0 curves published at **every pick 1–64** (continuous per pick, **not** band steps).
Reconciliation assert: `Σ_g share_g(p)·posv_g(p) == allin(p)` for every pick, `max |·/allin − 1| < 1e-12`.
Per-position monotonicity is **not** enforced (owner lean); ascents are disclosed as data.
The RUCK relativity floor at picks 63–64 (ORDER 28 §9.4) is expected to persist and is **re-declared**,
not rediscovered.

### P8 — POOL v0s, WAY A, K-SHRUNK
Per pathway × position cells on the MSD **Way A** basis, K = 15 shrink toward the pathway level
(≈ 34% borrow at the median cell), published as the printed pool day-0 object. Predicted anchored
pathway levels (board points): **MSD 334.6 · ND>64 263.9 · RD 230.6 · SSP 216.1 · PDA 187.9 ·
UNR 124.7 · PDN 111.0 · PDS 101.0 · IRE 94.5**, with ND-pick equivalents **MSD 47 · ND>64 52 ·
RD 56 · SSP 57 · PDA 61** and UNR/PDN/PDS/IRE outside 64.

### P9 — THE TWO EMPTY CELLS STAY UNSIGNED
`PDN:KPF` and `PDS:KPF` are published as **`null`**, not as the derivation's fully-shrunk numbers
(**92.4** and **84.0** — recorded here so it is provable that a number existed and was *declined*).
A **loud boot assert** fires if any entrant ever maps to an unsigned cell. Predicted: **zero** current
entrants map to either cell, so the assert is silent on this board — and it is proven non-vacuous by a
synthetic probe, never by its silence.

### P10 — THE NUMÉRAIRE RE-PIN
`s = RL_PICK1 / pooled_head_pre_scale` re-stamped through `_load_numeraire`. The landing publishes the
ORDER-28 ladder, whose own pre-anchor head is **3191.1789716631**, so:

> **predicted new s = 3000 / 3191.1789716631 = 0.9400914291048137** — the **×0.94 class** the register
> ruled ("~x0.94-class under the grace-A head").

**A DISCREPANCY IN THE BRIEF, DECLARED BEFORE MEASUREMENT.** The brief states *"today s = 3000/2850.6
= 1.0524"*. The live artifact does **not** carry that: its numéraire block reads
`pooled_head_pre_scale 3017.9232`, `s 0.9940610814748366`, and `3000/3017.9232 = 0.994061…` — E6-coherent
as committed. **1.0524 is the ORDER-28 identity gate's *attribution* numéraire leg (`ev / board_v`,
`GATE28_out.txt`), a different object from the artifact's `s`.** The prediction above therefore takes
the artifact as the authority. **Predicted old→new: `0.9940610814748366 → 0.9400914291048137`, a player
re-denomination of ×`0.945715`.** If the packet's measured s is instead ~1.0524-based, P10 is BREACHED
and the reason is reported, not reconciled away.

**Dimensional disclosure, made in advance**: today's `H` was measured on the item-271/#328 lane; the new
`H` is the ORDER-28/26B-C2 lane's head. The construction that makes `s` meaningful is
`installed ladder == raw ladder × s`, and that holds exactly for the published ladder against its own
head. The **lane change** is disclosed as a real change of measuring stick, not hidden inside the ratio.

### P11 — E6 COHERENCE, BOTH SIDES TOGETHER
`_load_numeraire` accepts the re-stamped block (`published_pin / pooled_head_pre_scale == s` to 1e-9,
`RL_PICK1 == published_pin`). Picks and players re-denominate **together**: no one-sided scaling.
Predicted board-level effect of the numéraire leg alone: **×0.945715 on every priced row.**

### P12 — THE PRINTED-DAY-0 ASSERT
For every fresh entrant, `printed day-0 price == derived v0 × numéraire` to the artifact's rounding.
The four legs (`_uncomp_prod`, pedigree-pole blend, ev/raw_ev, L7) are verified to **collapse** on
fresh entrants — they are **not** rewired in this act (deferred whole to the consumption-rewire act).

### P13 — THE FINAL BOARD, MOVER CLASSES
Predicted mover classes vs live `88ce647f`, in order of size:
1. **the numéraire scalar** — reaches **every** priced row (804), ×0.945715;
2. **the grace dial** — the ORDER-28 eligible set **E** (75 rows), of which **39** moved there;
3. **the ORDER-28 indirect three** — `shadeau-brain`, `tom-hanily`, `will-mclachlan`;
4. **the unflag-three channel** — the v3.4 kernel curve and hence `BOARD_FACTOR` (P3);
5. **the curve + pool v0 re-print** — every row whose entry anchor reads the ladder or a pool level.

**Predicted mover count: 800–804 of 804** (i.e. essentially the whole board), because a numéraire
re-pin is by construction board-wide. **Predicted total board value: 752,429 → 705,000–725,000**
(a fall of **3.5–6.5%**), the numéraire's −5.43% partly offset by grace's +0.63% and by the curve
and pool re-print. **Predicted sign: DOWN.**

### P14 — NAMED ROWS
`ramm · kentfield · liddy · hansen · visentini · martin · herbert · newcombe · duursma · sheezel` are
each reported live → landed with their per-lever split. Predicted: **`willem-duursma` is the only
named row that rises** (grace reaches him and outweighs the numéraire); every other named row falls
by roughly the numéraire factor, modulated by its own curve/pool anchor.

### P15 — NO-ARB, BOTH INSTRUMENTS, ON THE FINAL BOARD
`noarb_table_338.py` **UNMODIFIED** (the pinned instrument) plus the all-arm harness, plus the
mark-path progression table, plus reverse no-arb, all re-read on the FINAL board.
**Predicted arbitrages opened: 0.** Predicted: mark-path PASS on all 10 arms and reverse no-arb PASS
on all 10 arms, as in ORDER 28.

### P16 — IDENTITY GATE
The delivered-value scorer gate re-runs on the landed board. Predicted: **price-function identity
bit-exact (`0.000e+00`)** on the panel and board-wide, as in ORDER 28 §4 — the identity is a statement
about the scorer and the engine speaking one language and it must survive the landing untouched.

### P17 — DETERMINISM
Two independent full builds of the FINAL configuration, each from a fresh scratch workspace, produce
**identical** `rl_app_data.json` md5s.

### P18 — THE MOVED-SET OF PINS
Exactly these identities move, and the packet records every one old → new:
**store · board · engine_head (`_merged_recover.py`) · `rl_model` · the pvc curve artifact and its
provenance contract/selftest pins**. Anything else moving — `band`, `bust_prior`, `peak_model`,
`q97m`, `v0surf`, `balanced_board`, `fv` — is a **STOP-AND-REPORT**, not a footnote.

### P19 — BOOT GUARD AND BOOK
Boot guard PASSES on the landed tree after restamping; the book is re-sealed as an **isolated commit**.

### P20 — NOTHING MERGES
The PR is opened from `land/order-29` to `main`, titled
`[HELD — DO NOT MERGE] Order 29: the one landing (grace-A + v0s + numeraire re-pin)`, and is **HELD**.

---

## 2. THE STOP RULES

Any of the following STOPS the build at that step, pushes what exists, and is reported precisely:

* P1 fails (byte-identity at entry);
* any assert in P2, P6, P7, P9, P11 or P12 fails;
* the mover set contains a class not in P13 and not explainable by measurement;
* any pin outside P18's list moves;
* an arbitrage is opened (P15).

**No improvising around a failure. No smoothing. Breaches are owned by number.**

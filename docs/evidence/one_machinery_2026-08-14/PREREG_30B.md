# PREREG_30B — THE ONE-MACHINERY BUILD. PRE-REGISTERED PREDICTIONS.

**Committed BEFORE a line of Step-1 wiring exists.** Nothing in this file is edited after commit. Every
prediction is scored by number in `SHIPPING_PACKET_30B.md`, breaches included and owned.

**Authority.** Register `v717` on main `d78866b` (all six owner rulings + pre-flight risks R1–R7); the
pre-posted brief, #334 comment `5291901616`; `SITTER_FADE_PACKET_2.md` + `PREREG_30A2.md` (the fade
derivation); `SHIPPING_PACKET_29.md` §14 (the entry wiring this act builds on).

**Branch** `land/order-29`, entry tip `915c2a0`, entry board `36d5dfc73e2b508ece530bc7dfae2090`,
store `cb38ef1171dcf20aae66ebf12682be0d`, artifact `pvc_curve_v2.json` `911774bc92de0630199a4cc0c6bfac42`.

**THE OBJECT.** `price = w(games) × production-projection + (1 − w) × v0 × fade(clock)` — one formula,
every player, every pathway; pathway-specific VALUES only. The 26A forbidden set (pathway pedestals, par
tables, prior poles) is **DELETED**, not bypassed.

---

## §0 — CONTROL AT ENTRY (run BEFORE this file was written; stated so the order is on the record)

The clean-tree staged rebuild (`bb30b.sh entry`, ORDER 29B's `bb29b.sh` with only ROOT and the scratch
dir re-pointed) reproduced **`36d5dfc73e2b508ece530bc7dfae2090` byte-exactly**, on store
`cb38ef1171dcf20aae66ebf12682be0d`, `rl_model.py` `14000af2a46f7a3c4cdfde303f5a1aff`. Transcript
`CONTROL_ENTRY_30B.txt`. Had it failed, this act would have stopped there and this file would not exist.

**MEASURED-AT-ENTRY FACTS the predictions below are stated against** (all read off the entry board
`36d5dfc7` and the entry artifact, before any 30B change):

| fact | value |
|---|---:|
| active rows / board total | 804 / **717,527** |
| ND in-curve active rows (type ND, pick 1–64) | 561 |
| pool / out-of-curve active rows | 243 |
| career-games == 0 active rows (the 29B wired set) | **89** (ND 1–64 **46** = 20,003 · pool/other **43** = 8,096) |
| **ND-type zero-game rows, any pick (the sitter book)** | **50, Σv = 21,192** |
| active rows with 1 ≤ cg ≤ 15 | 147, Σv = 70,513 |
| — of those, age ≤ 23 (**the at-bar class as I define it below**) | **126, Σv = 65,964** |
| all-in ND curve Σ picks 1–64 | 47,315 (pick 1 = 3,000, pick 64 = 179) |
| numéraire `s` | 0.9400914291048137 (head 3191.178971663107, pin 3000) |
| A2, on the entry artifact | RUCK 63 = 64 = **0.0** · SF 64 = **18.0** · MID 64 = **56.7** |
| per-position ascents on the entry artifact | KPD 24 · KPF 14 · MID 14 · RUCK 15 · SD 19 · SF 21 (**107 total**) |

---

## §1 — THE POSITIONAL v0 RE-FIT (Step 1)

**The construction I will run, stated before it is run.** Per position `g`, on the published cells
`posv_g(p) = relat_g(p)·curve(p)`, `p = 1..64`, with weights `w_g(p) = share_g(p)` (the artifact's own
population share — the weight under which the reconciliation identity is a weighted mean):

1. **weighted PAVA**, non-increasing in `p`;
2. **FLOOR** `max(·, 100.0)` — a lower bound, so pick 64 is ≥ 100 per position and the approach to it is
   monotone by construction (max of a non-increasing sequence and a constant is non-increasing);
3. **the −1-per-pick ordering tiebreak** on every flat run of length ≥ 2 — the same law as the all-in
   curve. On a PAVA plateau above the floor the block is centred on its weighted-mean index so the
   block's weighted sum is preserved exactly; on the floor plateau (which always runs to pick 64) the
   anchor is `v(64) = 100` and `v(p) = 100 + (64 − p)`, because a descending spread there would put pick
   64 below the ruled floor;
4. **CONSERVATION** — one scalar `λ` on the above-floor part, `v'(p) = 100 + λ·(v(p) − 100)`, chosen so
   `Σ_p Σ_g share_g(p)·v'_g(p) = Σ_p curve(p) = 47,315` exactly. `λ` preserves both the monotone order
   and the floor. **No slash**: `λ` is a conservation scalar, not a haircut, and it is published.

**P1.** All six positions come out **strictly ordered**: `ascents = 0` for every position, i.e. **107 → 0**.
**P2.** `posv_g(64) ≥ 100.0` for all six positions, and the three A2 cells (RUCK 63/64, SF 64, MID 64)
land at exactly the floor family (100 or 100 + small tiebreak offsets). **A2 is cured, not masked.**
**P3.** `λ ∈ [0.97, 1.00)` — the floor lift is small because it lands on deep, thin-share cells. The
share-weighted grand total after the re-fit is 47,315 to `< 1e-6` absolute.
**P4.** The **per-pick** reconciliation `Σ_g share_g(p)·posv'_g(p)` no longer equals `curve(p)` pick by
pick. I predict `max_p |ratio − 1| ∈ [0.05, 0.60]`, concentrated at the DEEP end (p ≥ 55), and I will
publish the whole residual vector rather than a summary. This residual is the price of monotonicity and
it is DISCLOSED, not hidden. (The population identity `Σ_p` is exact; the per-pick one is not.)
**P5.** The biggest FALLERS are the deep KPD and SD cells (KPD 64 = 643.5 and SD 64 = 312.0 today, both
ABOVE their own pick-32 values — the most visible non-monotonicity on the artifact). The biggest RISERS
are the three A2 cells. Both are named here before measurement.
**P6.** At Step 1 alone (v0 re-fit, no fade, no blend) the **mover set is exactly the 46 ND in-curve
zero-game rows**, plus zero pool rows (`pool_v0.cells` is untouched at Step 1) — so ≤ 46 movers, and
every mover has `cg == 0`. No row with evidence moves.
**P7.** The 29B printed-day-0 identity **re-verifies against the new cells**: `printed == round(new
derived v0)` on **89 of 89**, tolerance 0.

---

## §2 — THE FADE, RE-DERIVED THEN WIRED (Step 2)

R1 is binding: the law must be calibrated against its own ruler, so `o30a2_recut.py` is re-run with
`POSV` = the STEP-1 FINAL cells and nothing else changed.

**P8.** The re-derived listed-conditional row stays **close** to the ruled values: `|D_LB(2) − 0.5684| ≤
0.05`, `|D_LB(3) − 0.3600| ≤ 0.06`, `|D_LB(4) − 0.3073| ≤ 0.10`. Direction: I expect **D to RISE
slightly** at every depth, because the re-fit lifts the deep tail (the denominator `v0`) only where it
was floored near zero — and those cells were producing the largest ratios. Drift is reported to 4 dp.
**P9.** The re-derived row stays **monotone decreasing** in depth over 2/3/4.
**P10.** The re-derived depth-1 normaliser `RAW(1)` moves by less than 3 % from 1.0286.
**P11.** The 30A control (Q24 in the 30A-2 harness) will **NOT** reproduce 30A's published unconditional
row after the re-fit — it cannot, because the denominator changed. I predict the harness's own control
flags DRIFT and I will report that as EXPECTED-BY-CONSTRUCTION rather than as a defect, with the
unchanged-POSV run published beside it as the true control.
**P12.** The wired clock is `c = (Y − debut(p)) + 1 + φ`, `φ = calendar_progress = 0.92` from
`data/season_state.json`, clamped to `c ≥ 1`; log-linear interpolation `D(c) = D(⌊c⌋)^(1−frac)·D(⌈c⌉)^frac`;
deep end EXTRAPOLATED from the fitted decay past year 4 (ruling 2), never held flat silently. Under this
clock `josh-smillie` (2024 ND, MID 7) sits at `c = 2.92`, `harry-demattia` at `3.92`, `max-knobel` at
`4.92` — reproducing packet 2 §4.2's clocks exactly. **If any of those three clocks disagrees with
packet 2, this act STOPS** — it would mean the clock I wired is not the clock that was ruled.

---

## §3 — THE BLEND (Step 3)

**P13.** Functional form, declared before fitting: `w(g) = 1 − exp(−(g/τ)^β)`, two parameters, `w(0) = 0`
exactly and `w` strictly increasing in `g`. Fitted by least squares to the three cumulative backbone
targets 0.656 (≤2) / 0.694 (≤5) / 0.824 (≤10) — the `≤0` target 0.568 is matched **identically** by
construction, since `w(0) = 0` makes the price exactly `v0 × fade(2) = v0 × D(2)`.
**P14.** The fit's RMS residual against the three free targets is **≤ 0.05 in D units**. If it exceeds
0.10 I will say the form does not fit rather than adding parameters until it does.
**P15.** `w` crosses 0.5 in the **6–10 games** region (the ruled entry-crossover), i.e. `τ ∈ [4, 12]`.
**P16.** The forbidden set — pathway pedestals, par tables, prior poles — is **DELETED from every path
that produces a printed price**, and the completeness audit enumerates every such path. Bars
(REPL/effective), aging/growth deltas and the form machinery are RETAINED and named as retained.
**P17.** No ownership-by-threshold: the 3/6/7/10 ladder survives only as interior estimator definitions.
**A `None` estimate never cliffs a price** — the formula stands on the faded-v0 term. Asserted on the
continuity curve (§5).

---

## §4 — THE MOVERS, NAMED IN ADVANCE

**P18 — THE SITTER BOOK.** The 50 ND-type zero-game rows move **21,192 → 9,500–11,500**, i.e. the
~10,185-class the preview predicted. Direction: DOWN, every row, no exceptions.
**P19 — THE AT-BAR MOVERS CLASS, NAMED BEFORE PRICES.** `cooper-trembath` (MSD 2025, KPF, 24 games,
2,055), `chris-scerri` (SSP 2025, SF, 7 games, 467) and `balyn-o-brien` (SSP 2025, SD, 4 games, 391) are
**at their replacement bar and young**. They **RE-REFERENCE — they do not fade.** Their production term
is re-expressed in the v0 language (the pathway pedestal that priced them is deleted); their youth and
growth pricing is retained. The class I name in advance is **active rows with 1 ≤ cg ≤ 15 and age ≤ 23:
126 rows, Σv = 65,964 today**. Predicted direction: **mixed, net DOWN, |net| ≤ 40 % of 65,964**, and
predicted composition: MORE fallers than risers, with the fallers concentrated in the ND high picks
(their pedestals are the largest) and the risers concentrated in the pool rows that had no pedestal to
lose. If this class moves net UP, or if any single row in it moves by more than ±90 %, that is a
BREACH and it is reported as one.
**P20 — ZERO MOVERS.** There is **no** class predicted to be unmoved. Every player may move in this act
(the numéraire re-pin alone reaches all 804). The prediction is therefore stated as the **bound** in P21,
not as a protected set.
**P21 — BOARD-TOTAL BOUND.** The final board total lands in **[560,000, 720,000]** — at or below the
entry 717,527, and above 78 % of it. A total outside that band stops the act for an owner word rather
than being shipped as a surprise.
**P22 — NUMÉRAIRE DIRECTION.** The re-pin moves `s` **UP** from 0.9400914291048137 (the pooled head
falls when the entry law's deep tail is floored and the sitters fade, so `s = 3000/H` rises), and it is
the largest board-wide scalar of the project. If `s` moves DOWN, the direction is BREACHED and reported.

---

## §5 — THE ASSERT WALL (Step 7), ALL BUILD-FAILING

**P23 — CONTINUITY CURVE.** For a fixed output level, price as a function of games 0 → 15 is
**continuous and monotone non-decreasing in evidence**, with **no cliff at 1** and **no dead zone at
7–10**. Quantitatively: no single-game step exceeds **25 %** of the 0 → 15 range, and every step is
≥ 0. The curve is emitted as an artifact for the packet.
**P24 — COMPLETENESS.** Every code path that produces a printed price is enumerated, each decomposes
into v0-language objects, and **no forbidden-set constant is reachable**. The audit list is committed as
evidence. This assert is build-failing.
**P25 — PRINTED DAY-0 IDENTITY.** Restated under the fade: for every `w(g)=0` row, `printed ==
round(v0 × fade(clock))`, tolerance 0. (29B's `printed == round(v0)` is the `fade = 1` special case and
is SUPERSEDED, not dropped — the 29B flat-hold and its games-as-of predicate are superseded by the
sitting-is-evidence law.)
**P26 — CELL COVERAGE.** Every entrant maps to a signed cell; the 1202-of-1202 pool coverage assert and
its non-vacuity probe still pass.

---

## §6 — CONTROLS

**P27 — DETERMINISTIC DOUBLE-BUILD.** Two fresh workspaces produce the identical board md5.
**P28 — KILL-SWITCH.** `RL_ONEMACH=0` on the full 30B tree reproduces the entry board
`36d5dfc7` **byte-exact** — the proof that the one-machinery block is the only thing that moves it.
(Declared kill-switch, not a manifest dial, exactly as `RL_ENTRY29B`.)
**P29 — PINS.** Pins restamp with the moved set explicitly asserted; **UNDECLARED MOVERS: NONE**. I
declare in advance that `pvc_curve_v2.json`, `rl_model.py` or `_merged_recover.py`, the board and
`engine_head` MOVE; store, `v0surf.pkl`, config, band, `bust_prior`, `peak_model`, `q97m`,
`pvc_snapshot` and the register DO NOT.
**P30 — `noarb_table_338.py` byte-identical `0f822035…` everywhere**, computed at run.
**P31 — NO-ARB.** On the landed-law (29C) basis the ND arbitrage **narrows** from −16.74 % (ALL 1–64)
toward the carry line, and the all-arm MODERN reading returns to **no-arb** (the preview read +2.13 %
with both fades). I do **not** predict every arm closes; I predict the count of arbitraging readings
**falls** from 5 of 5.
**P32 — LEDGER.** Both ledgers reconcile exactly: every per-lever sum adds to live `88ce647f` → final
and to `36d5dfc7` → final, 0 rows failing, max |residual| 0.
**P33 — NOTHING MERGES.** PR #510 stays `[HELD — DO NOT MERGE]`.

---

## §7 — DECLARED RESIDUE AND STOP CONDITIONS

- **R7, the 7-row retired-predicate disagreement** (`toby-conway`, `judson-clarke`, `finlay-macrae`,
  `max-king-stk`, `sam-sturt`, `paddy-dow`, `elliot-himmelberg`) is carried **ACCEPTED AND DECLARED**,
  on Layer 1's `_retired`, exactly as the 30A-2 harness carried it. It is not silently reconciled inside
  a pricing act.
- **STOP CONDITIONS, binding.** Any assert failure · any mover class this file did not name · any
  forbidden-set constant still reachable after deletion · any design question the six rulings do not
  cover ⇒ **STOP at that step, push, report**. No improvisation, no tuning after seeing a reading.

---

*ORDER 30B build seat. `land/order-29`. This file is committed before Step 1 and is never edited.*

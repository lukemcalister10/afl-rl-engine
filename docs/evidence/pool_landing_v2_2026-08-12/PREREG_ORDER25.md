# PREREG — ORDER 25, THE LANDING BUILD (ψ delivery, amended pars, re-trued levels)

Issue #334, ORDER 25. Brief: comment
[5267153255](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5267153255).
Owner's landing word: comment
[5267147448](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5267147448)
— **"Land"**, with the one amendment: *"I feel like MSD pars should borrow from the wider pool given
the thin sample."*

Branch `land/pool-update-v2`, cut from `origin/build/pool-quality` @ `b3bf20b`.

**THIS FILE IS COMMITTED BEFORE ANY MEASUREMENT OF THIS ORDER IS RUN** — before the control board is
built, before one amended par cell is computed, before U‴ is derived, before the first iteration
round is emitted, and before a single engine byte is edited. **It is never edited after commit.**
Every breach is scored by number in `SHIPPING_PACKET_V2.md` and owned by name.

---

## 0. What I am predicting against

The configuration being landed is fixed by owner ruling and is **not** a prediction: current-state
delivery at α = 1.0, the quality-conditioned premium
`M = (1−φ)·R + φ·(1 + q·(U‴−1))`, and the ONE amendment — the par shrink donor becomes the
**all-pool same-depth par**, replacing ORDER 24B's pathway all-depth donor.

The comparison points, all published and all frozen:

| name | what | identity |
|---|---|---|
| `live` | `origin/main` today | board `1dbd1480a34c7823f330273211cbb76a` |
| `pr469` / `landed23` | ORDER 23's landing, this branch's committed board | `665311ca72576df6ff0bbf6dfd007739` |
| `psi` | ORDER 24B's ψ board at the **#469 frozen levels** | `e2bf7347e07c08f1efbdda17d6601e4e` |
| levels in force (#469 signed) | SSP 315 · MSD 374 · IRE 106 · PDA 188 · PDN 96 · PDS 56 · UNR 66 · ND65+ 298 · RD MID 289 / SD 245 / SF 217 / KPD 370 / KPF 209 / RUCK 259 | `pvc_curve_v2.json` `07b7109f` |

---

## A. THE CONTROL (step 1)

**A1.** The unmodified tree, with `SURFACE_psi.json` staged exactly as ORDER 24B staged it, rebuilds
the ψ board **byte-identical to `e2bf7347e07c08f1efbdda17d6601e4e`**. Non-match is a BLOCKER and I
stop, commit and report.

**A2.** On that control build the four non-pool identities are unmoved: `config bf012105` ·
`rl_model e5eb5e44` · `curve_artifact 07b7109f` · store `d9a24282`.

---

## B. THE AMENDED PAR TABLE (step 2)

The amendment is deterministic arithmetic on a published population, so B1–B3 are **low-information
predictions and I declare them as such** — they can only fail if I have misread the rule. The
load-bearing predictions are B4–B8.

**B1.** The donor becomes the all-pool **same-depth** par. The `ALL POOL` row therefore becomes its
own donor and its wired values collapse onto its **raw own** pars:
`[58.57, 60.56, 64.41, 69.65, 71.45, 75.63]` (each within ±0.01 of the ORDER 24B *own* column).

**B2.** The weight stays ORDER 21's class-axis form **verbatim**: `w = n/(n+10)` with `n` the **raw
exact-depth CELL count** — the same `n` ORDER 22's `o22_make_relaxed_surface.py:109-127` uses and the
same `n` ORDER 24B used. The brief's phrase "K=10 on games" is read as *the par itself is
games-weighted* (it is), **not** as a games-count weight. I will publish the games-count variant as a
disclosed sensitivity so the reading is visible and scoreable rather than assumed. **I predict the
cell-count reading is the right one** on two grounds: it is the named ORDER 21 convention, and it is
the reading that makes thin cells borrow MORE, which is the owner's stated purpose.

**B3.** The empty cells move the most, because an empty cell **is** its donor: `MSD` d4/d5/d6,
`SSP` d4/d5/d6 and `PDN` d5/d6 rise from their flat pathway donors (61.70 / 56.88 / 60.07) to the
all-pool depth pars **69.65 / 71.45 / 75.63**. That is a rise of **+13% to +33%** in those cells.

**B4.** The MSD cells that actually carry today's named rows move only a little, and **d2 falls**:
`par(MSD,1)` **55.0–55.6** (was 56.89, DOWN) · `par(MSD,2)` **61.3–61.9** (was 62.48, DOWN) ·
`par(MSD,3)` **64.8–65.4** (was 62.81, UP).

**B5.** Consequently, **before** any level re-truing, `harrison-ramm`'s `q` RISES slightly (his par
falls) and `luker-kentfield`'s `q` FALLS (his par rises). Both moves are **under 4% relative**.

**B6.** **U‴ ≥ U″ on every one of the nine pathways**, without exception — because raising par at the
empty deep cells can only cut q-mass, and a smaller q-mass demands a larger premium to redistribute
the same total. Where par FALLS (RD d1, MSD d1/d2, UNR d1, PDS d1) the effect is the other way, so I
predict the two forces net to a **rise on every pathway but at most one**, and I name RD as the most
likely exception (its d1 par falls and it has no empty cells at all).

**B7.** Mean preservation prints `1.0000000000` on **all 10 rows** to 1e-9, at every round it is run.
This is a HALT instrument, not a claim.

**B8.** `U‴(MSD)` lands in **[2.00, 2.20]** (was `U″ = 2.004494`).

---

## C. THE FULL ITERATION (step 3)

**C1.** The freshly measured calibration target is the **0.9900-class** number and reproduces ORDER
23's `0.9900060981` to **at least 6 significant figures**. The ψ delivery moves pool prices only, and
the arm-split target is the national arm's own profile, so the separation law says it must not move.
**A target that moves by more than 0.1% is a finding I report as a breach, not as noise.**

**C2.** The target is **one distinct value across every round** of the iteration.

**C3.** The iteration **CONVERGES**: every pathway's shrunk lambda within **1.0% relative of 1.0**.
Round count **4–6** (declared cap **8**; non-convergence at 8 is a BLOCKER).

**C4.** The starting (round-1) lambdas at the #469 frozen levels are **already close** — I predict
every pathway's shrunk lambda inside **[0.94, 1.06]** at round 1, and the ALL POOL aggregate inside
**[0.97, 1.03]**. Grounds: mean preservation holds the harvest's entry-weighted mean of `M` at
exactly 1 under both deliveries, and the ψ board's pool total (132,342) sits within 0.5% of the
ORDER 23 landed board's (132,960) at identical levels.

**C5. THE LEVEL SHIFTS vs the #469 signed values.** Direction and band, per pathway:

| level | #469 | predicted landed | band | direction |
|---|---:|---:|---|---|
| `MSD` | 374 | **362** | **[355, 374]** | **DOWN, 0 to −5%** (the owner's "MSD-class eases") |
| `SSP` | 315 | 312 | [303, 320] | down, small |
| `IRE` | 106 | 105 | [102, 109] | down, small |
| `PDA` | 188 | 186 | [180, 192] | down, small |
| `PDN` | 96 | 95 | [92, 99] | down, small |
| `PDS` | 56 | 56 | [54, 58] | flat-ish |
| `UNR` | 66 | 66 | [64, 68] | flat-ish |
| `ND65+` | 298 | 296 | [285, 310] | small |
| `RD:MID` | 289 | 288 | [283, 295] | small |
| `RD:SD` | 245 | 244 | [240, 250] | small |
| `RD:SF` | 217 | 216 | [212, 222] | small |
| `RD:KPD` | 370 | 368 | [362, 376] | small |
| `RD:KPF` | 209 | 208 | [204, 213] | small |
| `RD:RUCK` | 259 | 258 | [253, 264] | small |

**MSD-class eases: magnitude band DECLARED as 0% to 5% DOWN**, central estimate −3%.
**No level moves by more than 6% in either direction.** Every RD positional level stays within ±3%.

**C6.** The `_ND65` fixed point is re-found under the amended law
`_ND65 = min(measured fixed point, curve[64] chain)` — which after ORDER 23's cap removal reads the
derived level verbatim. It lands in **[285, 310]** (it was **298**), and the ND>64 pathway's raw
lambda at round 1 is inside **[0.9, 1.2]** — nothing like ORDER 23's 1.53, because the cap is already
gone.

**C7.** Levels are written as **INTEGERS** (ORDER 22's rule: `rl_model.py` truncates), and this is
the **only** `pvc_curve_v2.json` write of the act.

---

## D. THE BOARD (step 4)

**D1.** The landed board is built **twice from scratch** and is **identical both times**.

**D2.** The landed board built with **NO staging** on the landed tree (shipped defaults only) is
**byte-identical** to the board built from the final staged configuration. Identity by construction,
verified by rebuild.

**D3. SEPARATION — hard failure.** Every ND row (`ty == ND`, pick ≤ 64) is **identical to live
`1dbd1480`**: **0 movers**, 0 absent, ND board value **620,877 → 620,877**. Asserted before anything
is written.

**D4. PICK CURVE 0 of 64 moved.** The `curve` block of `pvc_curve_v2.json` is untouched; only
`pool_levels` moves.

**D5. PINS.** The moved set is asserted BEFORE the file is written and is exactly:
`board` · `curve_artifact` (pvc_curve_v2.json) · `engine_head` (the amended par + U‴ literals) and
the fv-class mirrors that bind them. **UNMOVED, and each printed key by key:** `store d9a24282` ·
`fv 2621b56a` · every pickle · `band` · `q97m` · `v0surf` · `peak_model` · `pvc_snapshot` ·
`bust_prior`. **`rl_model.py` does NOT move** — ORDER 23 already landed its one amendment and this
order has no code change for it. **`config` does NOT move** — H is already retired at `bf012105`.
`noarb_table_338.py` md5 stays **`0f8220351c64c56ccfa90c60edcdfa5f`**.

**D6.** The book is re-sealed in an **ISOLATED commit** (ORDER 20C/23 precedent), and F2 parity
measures **0 mismatches** against the landed board after the re-seal and **>0** before it.

**D7.** The **boot guard PASSES** on the landed tree, both halves.

**D8.** The self-test on the landed tree produces **0 net new failures** against a control run on
`origin/main` (ORDER 23 measured 2 failures on both — Guard 1 file-mode checks a git checkout cannot
reproduce).

---

## E. THE NAMED ROWS (live → landed)

Bands are on the **landed** board. `live` values are from `1dbd1480`.

| player | live | ψ at #469 levels | **predicted landed** | **band** |
|---|---:|---:|---:|---|
| `harrison-ramm` | 351 | 567 | **552** | **≤ 567**, and in [515, 567] |
| `luker-kentfield` | 178 | 449 | **430** | **≤ 449**, and in [400, 449] |
| `mani-liddy` | 128 | 168 | **165** | **~168-class**: [158, 172] |
| `robert-hansen` | 80 | 143 | **141** | **~143-class**: [134, 147] |
| `vigo-visentini` | 168 | 183 | **183** | **~183**: [177, 189] |
| `marcus-herbert` | 906 | 906 | **906** | **EXACT — unmoved** |
| `jai-newcombe` | 4883 | 4883 | **4883** | **EXACT — unmoved** |
| `nicholas-martin` | 2822 | 3513 | 3510 | [3495, 3520] |

**E1.** `marcus-herbert` and `jai-newcombe` do not move by one point from live. They are full
participants (φ = 1) carrying an anchor share of **exactly zero**, so no multiplier of any kind and
no level reaches them.

**E2.** `harrison-ramm` is **below** his ψ value at #469 levels, i.e. the re-truing eases him. He is
the owner's sharpest pre-registered test name.

---

## F. THE BOARD TOTALS AND THE MOVERS

**F1.** Landed **pool** total in **[127,500, 132,500]** — below the ψ board's 132,342 (the level
re-true eases) and above live's 125,166.

**F2.** Landed **national** total **620,877 EXACTLY** — the separation law as a number.

**F3.** Rows moved vs live: **[110, 130]** (ORDER 23's landing moved 117; ψ moves 118 vs live).

**F4.** Board total vs live 746,043: landed in **[748,000, 754,000]**.

**F5.** The composed movers ledger's **three-lever sum identity holds on every row** (lever_H +
lever_retention_delivery + lever_repricing == total delta), asserted at write time; the writer halts
otherwise.

**F6.** `lever_H` reproduces ORDER 23's ledger H column **exactly** on every shared row — it is the
same lever, the same intermediate build, and nothing in ORDERS 24/24B/25 touches it.

---

## G. NO ARBITRAGE

**G1.** **Zero arbitrages opened** on the ORDER 22 margin harness — all readings positive-margin,
every margin listed in the packet.

**G2.** Both headline metrics are **read and reported, never targeted**: the career profile AND
yr4/yr0, per the standing law.

---

## H. SCOPE — what I predict does NOT move

**H1.** The store is untouched: `d9a24282357cf3083b1640466e3ecd83`.

**H2.** Every pickle, both instruments and both harnesses are untouched, verified by computed md5
against `origin/main`, not asserted.

**H3.** The national code path is untouched: `_R_surf`, `LAM_SIT`, `_a_share`, `_ev_qual`,
`_surprise`, `_c_w`, `C_H`, `_h_cut` and the D12 clock all unmodified.

**H4.** `_pr_phi`, `_pr_q`, `_pr_mult`, `_pr_depth`, `_pr_par`, `_pr_R`, `_pr_pathway`, `_PR_PATH`
and `_PR_WHOLE` are unmodified in **shape** — this order changes only the **numbers** in `_PR_PAR`,
`_PR_PAR_ALL`, `_PR_U`, `_PR_U_ALL` and the signed levels. **No new dial, no new threshold, no new
constant.**

**H5.** Nothing merges. The PR is opened to `main` and **held open** for the owner's word. PRs #469,
#473, #475 and `main` are not touched.

---

## I. THE ROUND CAP AND THE BLOCKER CONDITIONS

Declared in advance, each able to fire:

1. Control board ≠ `e2bf7347…` → **BLOCKER**.
2. Mean preservation ≠ 1.0 to 1e-9 on any pathway at any round → **HALT**.
3. Non-convergence after **8** rounds → **BLOCKER**.
4. Any ND row moved vs live → **HARD FAILURE**, build stops.
5. `noarb_table_338.py` md5 moved → **BLOCKER**.
6. Any pin outside the declared moved set → **BLOCKER**, nothing written.
7. Boot guard fails on the landed tree → **BLOCKER**.
8. Any arbitrage opened → reported to the owner in the packet, **never silently retuned**.

On any blocker: stop, commit everything that exists, report it in full.

---

_Committed before any measurement. Not edited afterwards._

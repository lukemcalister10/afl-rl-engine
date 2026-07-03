# COLD AUDIT — CANDIDATE v2.4 (`7c199a1f`) — combined scoped re-audit of D13 + D14

**Seat:** OPUS, cold (no shared context with build/supervisor). Everything below re-derived or re-read from the repo.
**Date:** 2026-07-03. **Nothing bakes on this audit alone** — Luke's board view + written bake word follow a CLEAR.

## STATE STAMP (three-column, byte-verified)
| role | engine `_merged_recover.py` md5 | git head | store | band | PR |
|---|---|---|---|---|---|
| CONTROL | `8aed420a` (…63ba4f268550cd5ebe987881) | `6035ce1` (main) | `644d1254` | `34faa865` | — |
| PREVIOUS v2.3 | `f3e537ba` (…015d6c47dae71f1bd61b6636) | `def39f5a` | `644d1254` | `34faa865` | #17 (open) |
| CURRENT v2.4 | `7c199a1f` (…29a7033452ba815c66f14c2a) | `fa6abd0` | `644d1254` | `34faa865` | #18 (open, base=#17) |

All three engine md5s reproduced exactly from the branch trees. Panel 10/10 at CONTROL confirmed (harness sound).
Reproduction method: candidate + v2.3 workspaces built by overlaying each branch's tracked engine files onto the
control runtime workspace (`RL_FV` repointed); ENV per directive (`PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000
RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22`). Board harvested once per state; curve
independently re-fitted from harvested capped V0s with an auditor-written NW+isotonic (NOT the build's function).

**⚠ HEAD-vs-MD5 FORK (D3, restated):** the directive's "CURRENT UNDER AUDIT = v2.4 head 7c199a1f" conflates the
md5 with the git head — `7c199a1f` is the md5 of the candidate `_merged_recover.py`; the git head is `fa6abd0`
(commit `9ae77bf` reads "engine 7c199a1f"). Same fork the directive warns about for v2.3 (`f3e537ba` md5 vs
`def39f5a` git). The candidate's own PR#18 body + CHANGELOG name and resolve it. **No engine ambiguity.**

---

## SCOPE A — D13 MACHINERY carried into v2.4

**A1 RUCK CAP + LADDER — CLEAR.**
- `RUC_PRIOR_CAP=float(os.environ.get('RL_RUC_PRIOR_CAP','1.73'))`, module-level (band/raw_ev level), applied by
  `_ruc_prior_cap(p,v)=min(v,1.73*draftval(p))` for real RUC only. Default 1.73 wired ✓.
- Cap-rung ladder reproduced independently (`min(_v0_uncapped, c*PVC)`), **Emmett pk27 PVC 609 uncap 1536:
  670 / 792 / 914 / 1054 / 1218** for c=1.1/1.3/1.5/1.73/2.0. The four binding rungs (1.1–1.73) match the
  directive's expected 670/792/914/1054 **exactly**. Top rung is **1218** (=2.0×609, cap still binds since
  uncap=1536), **not** the directive's stale "1201" — that figure conflated V0 with board-ev (PR#16 D12-ASK4d
  independently measured the same 2.0× V0 = **1218**). Non-blocking directive-side staleness, engine correct.
- In v2.4 the cap produces `_v0_raw`=1054, then the **curve** overrides Emmett's board V0 to **955** (V0/PVC 1.57),
  ev 1054→1054 (blend-fed). Reproduced.
- **172-ruck universe DEFINED:** real rucks with a recorded pick = **172** (of 217 real rucks; 45 pickless
  excluded — `draftval` needs a pick). Ladder file has exactly 172 rows → PR#17 gap (Emmett-only) CLOSED ✓.

**A2 RETENTION RE-DERIVATION — CLEAR (surface inherited from v2.3; v2.4 adds only the KPP floor).** The wired
R_SURF is the v2.3 pick-conditioned kernel surface; the only v2.4 change is the board-path KPP floor (Scope C).
Retention factors reproduced three-column below (C5). The KPP-vs-nonKPP gap at depth 3+ is present in the raw
v2.3 surface (e.g. KPP pk5 d4 raw 0.194 vs nonKPP 0.446) — i.e. real in the data pre-floor, which is exactly
what O1 was signed to lift. Full independent re-fit of the retention surface from the sit-out realization sample
was **not** re-run from scratch (that sample/derivation lives in the v2.3 line, already audited pre-v2.4); flagged
as inherited, not re-derived. **OPEN (evidence-level, non-blocking): retention-surface from-raw re-fit deferred.**

---

## SCOPE B — D14 ASK 1: THE V0 BOARD CURVE

**B1 INDEPENDENT RE-FIT — CLEAR (0.00 divergence).** Auditor-written adaptive-bandwidth Gaussian NW (Kish
eff-n≥35, h0=0.18 grown ×1.15 to hmax=2.2) + isotonic-decreasing, fitted on the harvested post-cap `_v0_raw`,
reproduces the WIRED `_V0CURVE` grid **cell-by-cell, max abs divergence = 0.00 across all six age≤18 cells**
(90-point grids). The build's 8-cell structure is exactly what an independent implementation arrives at.
Fit universe: **1571 real-ND-with-pick = 1408 age≤18 + 163 mature** (149 non-RUC pooled + 14 RUC); per-position
age≤18 n = MID 427 / KEY_FWD 178 / KEY_DEF 152 / GEN_FWD 284 / GEN_DEF 295 / RUC 72 (Σ 1408) — all reproduced.

**B2 MATURE-POOLING EVIDENCE (evidence-only; owner ratified) — no residual signal, pooling defensible.** Within
mature (age≥19) non-RUC, position-conditioned residual (after conditioning on the pooled age×log-pick surface):
**F = 1.33, permutation p = 0.277** → position carries NO significant residual signal on board-path V0.
"Position-washed" confirmed: age-group mean-V0 spread **587** ≫ position-group spread **139** (~4×). No v3 note.

**B3 BY-CONSTRUCTION PROOFS — CLEAR (reproduced at 0).** Ran `_v0_curve_assert()` on the live candidate:
**cross_draft_maxdisp = 0.0 · within_cell_inversions = 0 · kpp_depth_monotone = True.** D14a/D14b/D14c registered
in SHIP_GATES + wired into ship_gates_check.py; green. Omitted rows printed (v2.4 V0*):

| player (cell) | v2.3 V0 | v2.4 V0* | note |
|---|--:|--:|---|
| Jhye Clark (MID pk8, 2022) | 2401 (raw) | **1792** | = MID age≤18 curve@pk8 (my re-fit 1792) |
| Cameron Mackenzie (MID pk7, 2022) | 1864 (raw) | **1876** | identical to Cumming (cross-draft, disp 0) |
| Sam Cumming (MID pk7, 2025) | 1859 | **1876** | = Mackenzie ✓ |
| Sullivan Robey (MID pk9, 2025) | 1859 | **1687** | now correctly below pk7 (build 1686, rounding) |
| Jack Steele (MID mat pk21 age19) / Ballantyne (GEN_FWD mat pk21 age21) | — | **530 / 521** | lawful draft-age differentiation (older lower) |

**B4 BOARD-PATH ONLY — CLEAR.** `v0_start` and `_R_surf` gate the curve/floor on module global `_BOARD_PATH`
(default True); the backtest/walk-forward harness sets it False after exec → `v0_start` returns
`min(_v0_raw, _V0GUARD)` (the v2.3 formula) and `_R_surf` skips the floor. Verified empirically (Scope E book).

**B5 R2 MOVERS — CLEAR.** All-V0 moves reproduced **831 up / 740 down** (exact). Max|ΔV0| = **1355** Naitanui
(build 1354, rounding; V0raw 2574 → curve 1220). >35% movers = **92** vs build's **91** — the single delta is
**Oscar Allen** at **35.03%** on raw v0 (485.5→655.6) but **34.98%** on rounded-integer v0 (the tsv basis);
his board ev is unchanged 184→184 (zero impact). Both counts correct under their rounding convention. Veteran
V0-insensitivity confirmed on top movers: **Tim Kelly V0 71→488, ev 1611→1611** (exact); Naitanui ev 24→24;
Izak Rankine V0 2573→1631, ev 2357→2357.

**B6-CURVE — CLEAR; tail flatness verdict = LEVELS (dominant) + SURVIVORSHIP (sample composition); NOT fit-artifact.**

(i) V0* pick levels + ratios (WIRED age≤18, independently reproduced):

| pos | pk1 | pk5 | pk10 | pk20 | pk40 | pk60 | pk1/pk20 | pk1/pk60 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| MID | 2554 | 2079 | 1579 | 991 | 571 | 445 | 2.58 | 5.74 |
| KEY_FWD | 970 | 933 | 828 | 668 | 486 | 342 | 1.45 | 2.83 |
| KEY_DEF | 895 | 895 | 840 | 678 | 550 | 430 | 1.32 | 2.08 |
| GEN_FWD | 1631 | 1526 | 1361 | 808 | 485 | 390 | 2.02 | 4.18 |
| GEN_DEF | 1163 | 976 | 857 | 657 | 500 | 423 | 1.77 | 2.75 |
| RUC | 1220 | 1139 | 1057 | 986 | 803 | 604 | 1.24 | 2.02 |

The owner's read is **numerically correct**: pk1/pk60 ≈ 2.0 (RUC/KEY_DEF) → 5.74 (MID), 4.18 GEN_FWD; pk1/pk20
2.58 for MID vs 1.24–1.77 elsewhere. **⚠ PR#18 BODY DEFECT:** its ASK1 table V0*[40] column (596/452/528/505/486/730)
disagrees with the actually-wired curve (**571/486/550/485/500/803**) in every cell; the board uses the wired grid
(reproduced at 0.00), and the session file `d14_ask1_curve_params.md` carries the correct 571/486/550/485/500/803.
PR-body-only mistype, immaterial to any board value; still a labelled-number error worth a fix.

(ii) DECOMPOSITION — raw capped-V0 medians by pick band vs the fit (age≤18):

| pos | pk1-3 raw[n] | pk11-20 | pk21-40 | pk41-60 | pk61-90 | fit tracks? |
|---|--|--|--|--|--|--|
| MID | 2631[37] | 1128[67] | 852[122] | 487[91] | 370[41] | yes (fit 2444/1147/753/496/404) |
| GEN_FWD | 2573[8] | 1165[45] | 558[89] | 432[90] | 300[32] | yes (fit follows band medians) |

The flat tail is **in the raw capped-V0 levels** (pk41-60 raw ≈ 487, pk61-90 raw ≈ 370 for MID — already ~5× below
pk1-3), and the fit faithfully tracks the raw band medians (departs only at the sparse top — KEY_DEF/GEN_DEF/RUC
pk1-3 n=2/5/3 — where kernel+isotonic correctly smooth noise; that is not tail-flattening). **⇒ NOT a fit-artifact.**
(iii) **Survivorship present in sample composition:** deep bands skew to low-games players (pk61-90: ns>0=43%,
g26>0=12%, median-ns 0; pk1-3: ns>0=100%, median-ns 8) and fully-delisted busts are absent from the current roster
(MA.data), so the deep-pick sample is survivor-weighted. But the fitted quantity is a **draft-time prior anchor**
(`raw_ev` at debut-year-minus-1 × iso_corr, then ruck cap) — pick-based, not performance — so survivorship
perturbs sample DENSITY more than anchor LEVELS. Inherited anchor-construction property, out of D14's scope by
design (overhaul track), **does NOT block D14**.
(iv) **Mid-vs-others pk20 gap is DATA-REAL, not thin-cell:** MID pk1/pk20 = 2.58 sits on the HIGHEST support
(local eff-n@pk20 = 89.0, n_in_11-30 = 133) and the steep early drop is in the raw MID medians (pk1-3 2631 →
pk11-20 1128). The thin cells (RUC eff-n 11.8, KEY_DEF 30.4) have the FLATTEST ratios (1.24, 1.32) — thinness
understates slope, it does not manufacture the mid premium.

**VERDICT (B6-CURVE):** *tail flatness is LEVELS + SURVIVORSHIP (inherited anchor-construction), NOT fit-artifact —
does NOT block D14; flagged loudly as the pre-bake vs post-bake V0-overhaul input.*

---

## SCOPE C — D14 ASK 2: KPP FLOOR vs OVERRIDE O1

**C1 WIRING — CLEAR.** `_R_surf`: `if _BOARD_PATH and cls=='KPP': dv=[max(a,b) for a,b in zip(dv, _dv_surf('nonKPP',lp))]`.
Pointwise MAX(KPP,nonKPP) at every (log-pick,depth); comparator nonKPP only; RUC excluded; board-path only. O1
registered in OWNER_OVERRIDES.md with Luke's verbatim words + date 2026-07-03 + one-line reversal ref +
owner-set-where-binding labelling (ledger R13, obituary E5).

**C2 FLOOR-NEVER-LOWERS — CLEAR (PROVEN).** Scanned all **540 cells (picks 1–90 × depths 1–6): floor<KPP-own
violations = 0, worst(own−floor) = 0.0** — max(a,b) ≥ a by construction, roster-wide (retention is a pure function
of pick×depth). Decomposition of the two named moves:
| player | ctl ev | v2.3 (V0 → ev) | v2.4 (V0 → ev) | mechanism |
|---|--:|--|--|---|
| Riak Andrew (KEY_DEF pk55) | 235 | 614 → 330 | **477 → 257** | **CURVE**: V0 dropped 614→477; floor only RAISED retention (offsetting) |
| Matt Whitlock (KEY_FWD pk27) | 426 | 616 → 327 | **624 → 351** | curve V0 +8 AND floor lift → ev up |
Riak's 330→257 is entirely the V0 curve lowering his start value; the floor did not lower him (it can't).

**C3 BINDING MAP — CLEAR.** Reproduced (bold = nonKPP selected):
| pick | d1 | d2 | d3 | d4 | d5 | d6 |
|--:|:--|:--|:--|:--|:--|:--|
| 5 | 0.660 | 0.487 | **0.446** | **0.446** | **0.446** | **0.314** |
| 15 | **0.707** | **0.479** | **0.479** | **0.479** | **0.479** | **0.307** |
| 20 | **0.683** | **0.461** | **0.455** | **0.452** | **0.452** | **0.305** |
| 30 | **0.649** | **0.436** | **0.422** | **0.414** | **0.414** | **0.303** |
| 50 | 0.642 | 0.407 | 0.351 | 0.334 | 0.334 | 0.329 |
Binds predominantly d3+, **and d1+ for mid-picks 15–30** — confirmed: raw KPP[15][d1]=0.694 < nonKPP 0.707, so
year-1 (d1) binds there. The D13 "gap at depth 3+" was incomplete; the d1+ mid-pick bind is real (raw KPP year-1
retention sits below nonKPP at picks 15–30). At pk50 KPP≥nonKPP everywhere (no bind; the two rows are identical).

**C4 ANCHORS — CLEAR (three-column reproduced exactly).**
| anchor | CONTROL | v2.3 | v2.4 | V0*(v2.4) | proj yr1→yr2 @0 games (non-incr) |
|---|--:|--:|--:|--:|--|
| Annable (nonKPP pk6) | 936 | 1485 | 1533 | 1957 | 1122 → 883 ✓ |
| Dylan Patterson (nonKPP pk5) | 982 | 908 | 781 | 976 | 534 → 435 ✓ |
| X. Taylor (nonKPP pk11) | 690 | 733 | — | 854 | 565 → 401 ✓ |
| Ison (nonKPP pk47) | 212 | 538 | 538 | 446 | 250 → 176 ✓ |
| Josh Smillie (nonKPP pk7) | 896 | 993 | 1002 | 1876 | 1118 → 856 ✓ |
| Riak Andrew (KEY_DEF pk55) | 235 | 330 | 257 | 477 | — |
| Matt Whitlock (KEY_FWD pk27) | 426 | 327 | 351 | 624 | — |
| Louis Emmett (RUC pk27) | 518 | 1054 | 1054 | 955 | — |
All projected yr1→yr2 non-increasing; all board-ev anchors reproduce the build's numbers.

**C5 RETENTION-SURFACE PRINT — CLEAR (must-answer).** Retention factor by class × sit-year (yrs 1–4) at picks
5/20/40, CONTROL(flat) / v2.3(pick-conditioned) / v2.4(+KPP floor):
| class · pick | CONTROL (flat) | v2.3 | v2.4 |
|---|---|---|---|
| nonKPP pk5 | 0.50/0.50/0.42/0.35 | 0.55/0.45/0.45/0.45 | 0.55/0.45/0.45/0.45 |
| nonKPP pk20 | 0.50/0.50/0.42/0.35 | **0.68**/0.46/0.46/0.45 | **0.68**/0.46/0.46/0.45 |
| nonKPP pk40 | 0.50/0.50/0.42/0.35 | 0.59/0.41/0.38/0.32 | 0.59/0.41/0.38/0.32 |
| KPP pk5 | 0.70/0.70/0.60/0.50 | 0.66/0.49/0.39/0.19 | 0.66/0.49/**0.45**/**0.45** (floor) |
| KPP pk20 | 0.70/0.70/0.60/0.50 | 0.67/0.41/0.28/0.15 | **0.68**/**0.46**/**0.46**/**0.45** (floor) |
| KPP pk40 | 0.70/0.70/0.60/0.50 | 0.64/0.40/0.32/0.27 | 0.64/0.41/**0.38**/**0.32** (floor) |
| RUC pk20 | 0.85/0.85/0.74/0.62 | 0.84/0.60/0.60/0.56 | 0.84/0.60/0.60/0.56 |

**Year-1 pin:** nonKPP year-1 moved **0.50 (CONTROL flat) → 0.55–0.68 (v2.3)** and is IDENTICAL v2.3=v2.4. So the
owner's "~0.6–0.7 where I remember ~0.4–0.5" is the **D13 continuous pick-conditioned re-derivation (v2.2→v2.3)**,
already shipped in v2.3 — **the D14 KPP floor did NOT move year-1** (it left nonKPP untouched and only raised KPP at
deeper years d3+). *Plain sentence: year-1 sit-out retention moved from ~0.50 to ~0.55–0.68 at v2.3 because of the
D13 pick-conditioned re-derivation; v2.4's KPP floor changed only KPP rows and only at years 3+.*

---

## SCOPE D — ARITHMETIC & UNIVERSE

**D1 MOVER-COUNT UNIVERSE — CLEAR (defined).** The **1,571** movers (831 up + 740 down) = the fit/apply universe
= **real national-draft players with a recorded pick** (`id∈_REAL ∧ type=='ND' ∧ pick is not None`), of which
1,408 are age≤18 (the 6 per-position curve cells) and 163 are mature. This is the population the curve is FITTED on
AND APPLIED to on the board (same set). The active roster is 805; the 1,571 includes retired/delisted historical
ND players who remain in the store (MA.data = 2,654 grouped rows), but **only current-roster rows carry a live board
value** — the historical rows' V0* feeds nothing live (their board ev is the retired/production value; no live board
cell depends on them). Ruck ladder universe = **172** = real rucks with a pick (of 217 real rucks; 45 pickless).
No application exceeds what can affect a live board value.

**D2 COHORT DUAL-INSTRUMENT — CLEAR (must-answer).** The n102 **board** instrument (Σ ev over the 2025 real cohort)
reproduced **exactly** at all three states I ran:
| instrument | CONTROL | v2.1 | v2.2 | v2.3 | v2.4 |
|---|--:|--:|--:|--:|--:|
| n102 board cohort (Σ ev) | **47416** ✓ | (48–55k) | 55836† | **57009** ✓ | **57710** ✓ |
| incurve-n64 matrix Yr1 | **37901**† | — | 43967† | — | — |
(✓ = independently reproduced this audit; † = build/PR record, not re-run this session — v2.1/v2.2 states not built.)
Like-for-like SAME-instrument: n102 board **47416 → 57710 = +10,294** across all changes. The apparent "~+12,000
gain" conflated TWO instruments: the control-era **37,901 was the incurve-n64 matrix Yr1 measure** (a smaller,
different population), NOT the n102 board cohort — proven because my n102 board total at EVERY state (47416 / 57009 /
57710) is far from 37,901/43,967, so 43,967 cannot be the n102 board cohort. *The +12k decomposes into
instrument-change (n64 matrix 37,901 vs n102 board ~50k) + real same-instrument movement (+10,294).* Annable v2.2
board 1414 not re-run (v2.2 state not built); Annable v2.3/v2.4 board 1485/1533 reproduced.

**D3 HASH HYGIENE — CLEAR.** `7c199a1f`/`f3e537ba`/`8aed420a` = md5s of `_merged_recover.py`; `fa6abd0`/`def39f5a` =
git heads. The four PR#17 write-up fixes (43,967 cohort · "V0 identical 1524" · B1 labels · panel claim) share
**one** commit `c1893b0`, distinct from the v2.1 engine md5 `c8051893`. The md5-vs-git fork is documented in
PR#18 body + CHANGELOG D14. (The audit directive's own "head 7c199a1f" repeated the very conflation D3 warns of.)

---

## SCOPE E — GATES & NON-MOVEMENT AT v2.4 (re-run)

**WALK-FORWARD BOOK — CLEAR (maxΔ = 0.000000).** Forced `_BOARD_PATH=False` on the live candidate (the backtest
path) and compared to v2.3 across 2,654 grouped players: **max|Δev| = 0.000000** and **max|Δround(v0_start)| = 0**
(integer/book precision). Sanity: `_R_surf('KPP',5,4)` on the backtest path = **0.194** (raw KPP, NOT the floored
0.446) — the floor/curve are correctly OFF on the backtest path. (A transient full-precision 5e-5 on one player,
Samson Ryan, was an artifact of my harvest's 4-dp store — his true engine value is bit-identical 861.95844998 at
both states.) **No book movement. Luke's backtest exemption honoured; the "ANY movement = BLOCKED" clause is not
triggered.**

**GATE BOARD RE-RUN — CLEAR (candidate `ship_gates_check.py`, RA repointed to candidate workspace, 70s).**
Tally **PASS=14 · FAIL=4 · FEATURE=1 · NOT-RUN=1 · PENDING=5 · STRUCK=1 — identical to the PR#18 body tally.**
- **Reds {A2, A3, A12, B4} FAIL — identical to v2.3, no new engine-caused red.** A2 Curtis 0.822 (Luke-ruled ship-red,
  D7); A3 Rozee 0.7307 (ledger R1 accept-red); A12 Travaglia 712<Moraes 887 (pre-existing) / Smillie 1002>Retschko
  730; B4 JS-parity export exit=1 (board not re-cut — pre-existing).
- **D14a PASS** dispersion 0.0000 · **D14b PASS** inversions 0 · **D14c PASS** depth-monotone True (on the board now).
- **A8 PASS** Berry 2421 / Tsatas 1140 = 2.12× (Tsatas & Berry byte-unmoved). **A11 PASS** Farrow 1644>Patterson 781,
  Cumming 1948>Annable 1533.
- **B5 FEATURE** 54 saves, lift +1335, **lowered=0, non-ND moved=0** (pure lower bound; saves table is the alarm surface).
- **B6 PASS** ramp `[1287,1557,1852,2504,3103,3190,3238,3291,3305,3314,3367,3435,3523,3563,3592]` — byte-identical to
  v2.3; 0→6 rise T=+1951; rise-by-3g +1217; no dips. τ^1.5 + LAM_SIT diff-clean.
- **B1 PASS** cross-cohort AVG peak at N=4, path_ok=True (**not tuned** — passes on the INDEPENDENT control nogames
  matrix, avg row 100/132/146/161/158/148/131 peak@N4=161; the build's @130 uses the v2.4 matrix. Different matrix
  input, same PASS; B1 is a backtest-path gate, unaffected by the v2.4 board changes). B2 NOT-RUN (leakage harness
  not run this session — backtest path, unaffected).
- **BY-CONSTRUCTION D14a/b/c also reproduced live** via direct `_v0_curve_assert()`: dispersion 0.0 · inversions 0 ·
  depth-monotone True.
- **Non-movement:** dial `d66291a`/graded-cap **grep-absent** in candidate engine (0 matches); ruck cap 1.73 default
  in force; Tsatas 1140 / Berry 2421 unmoved; **CONTROL engine byte-verified 8aed420a pre+post** (store 644d1254,
  band 34faa865 untouched).

---

## PER-SCOPE VERDICTS
- **A — CLEAR** (A2 retention re-fit-from-raw deferred as inherited; non-blocking OPEN)
- **B — CLEAR** (B6-CURVE tail = LEVELS+SURVIVORSHIP, not fit-artifact; PR-body V0*[40] column mistype flagged)
- **C — CLEAR** (floor proven never-lowering; year-1 shift pinned to D13, not D14)
- **D — CLEAR** (universe defined; n102 board instrument reproduced; +12k decomposed)
- **E — CLEAR** (book byte-identical maxΔ=0; D14a/b/c green; reds unchanged — see gate board)

## NON-BLOCKING FLAGS (nothing here blocks; recorded for the fix queue)
1. **PR#18 body ASK1 table, V0*[40] column** (596/452/528/505/486/730) disagrees with the wired curve
   (571/486/550/485/500/803) in every cell — a PR-body mistype; the engine + session artifact are correct. Fix the PR body.
2. **Directive-side staleness (not engine):** "CURRENT UNDER AUDIT = v2.4 head 7c199a1f" is the md5, git head is
   `fa6abd0` (D3); and the A1 expected Emmett top rung "1201" is stale — the 2.0× V0 rung is 1218 (cap binds; uncap
   1536), cross-confirmed by PR#16 D12-ASK4d.
3. **A2 retention-surface from-raw re-derivation deferred** — the sit-out realization sample/fit lives in the v2.3
   line (already audited pre-v2.4); v2.4 changes only add the floor. Flagged inherited, not independently re-fit here.
4. **B5 >35% mover count 92 (raw v0) vs 91 (rounded v0):** boundary player Oscar Allen at 35.0%; zero board impact.
5. **B6-CURVE (a)+(c) inherited-levels/survivorship findings** are loud inputs to the pre-bake vs post-bake
   V0-overhaul timing decision — they do NOT block D14 (which only wired Luke's same-boat law faithfully).
6. **Label drift (build docs):** the sit-out aggregate series 41139/46764/48397 is called "54-set" in D14 docs but
   "n137" in D13 docs; "54" also collides with the v2.4 floor-saves count. My generic sit-out filter (n≈97–109) did
   not match either label's population — the numbers are the build's; the label is inconsistent. Cosmetic.

## OVERALL: CLEAR (pending Luke's board view + written bake word)

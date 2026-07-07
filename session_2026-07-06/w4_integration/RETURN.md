# FABLE WAVE-4 INTEGRATION — RETURN (candidate board + book, multi-lever, per-lever attribution)

**CANDIDATE — NO MERGE, NO PROMOTE.** Rides to the cold audit → owner word → re-bake.
**Store `rl_model_data.json` md5 `e1b4d8bf` — NEVER edited** (Guard 5 asserted at bootstrap, every build step, and end).
Engine head `efea88e5` → **`375b11ef`** (every lever is CODE, kill-switched). Board **`ca5b3653`** (parity 805/805, eps=0).
Book sealed **`264f2847`** (2649 players — key set identical to the baked seal). Branch `claude/fable-wave-4-integration-w4rfpb`.
Deliverable HTML: `session_2026-07-06/w4_integration/w4_board_book.html` (self-contained: anchors · guards · attribution · full board · book curves · PVC).

## The core lever — forward-valuation (present-vs-future) recalibration
Every price integrates `proj_from_peak`'s year-k terms at flat weight 21/1.15^k. That treated a moderate producer's
year-9 margin as being as certain as Bontempelli's year-1 margin. The recalibration is a **form-conditioned (never
age-keyed) weight W(k)** on the year-k term:
- **PROVEN:** `1 + 0.17·kpf_up·g(m)·dur·sh·c_near(k) − 0.60·(1−g(m))·agew·h_far(k)` — the certainty credit on the
  near years of a clearly-above-replacement margin (`g(m)` ramps m=10→30: only the best-of-the-best; `dur` durability,
  `sh` decline gate mirroring the shed; captaincy premium rides inside every credited year), funded by a far-year fade
  on moderate margins (age-ramped 23→26 so a durable young proven player's prime is untouched). The demonstrated-
  production floor carries the same credit — the elder's high floor is credited, not just his projection ("credit the
  margin, not the age").
- **THIN-CAREER YOUNG:** `1 + 0.13·thin·yage·c_yng(k)` — the survivor reward priced forward into years 1-2
  (position-relative runway: a 23yo KPF is pre-peak), flowing into V0 → the year-1 anchors → the book's year-1 cohort.
- **Deep-pick compress** (the owner-agreed #43 cells only): GEN_FWD −12% / GEN_DEF −9% / MID −7% at picks 46+,
  smooth from 38, thin-career only. **MID 1-3 (2.09) NOT touched — stays FLAGGED for your ruling.**

## Headline numbers
| measure | baked v2.5 | W4 candidate | bound |
|---|---|---|---|
| **Cohort no-arbitrage ratio** (walk-forward aggregate y4-6 / y1-2, 2004-2020) | 125.2% | **124.6%** | ≤130 HARD · guide 120-125 ✅ |
| year-1 aggregate (the ordered direction: RAISE year-1, don't cut) | 957,116 | **978,495 (+2.2%)** | ✅ |
| B1 cohort growth law | PASS peak N=4 @143.2 | **PASS peak N=4 @142.1** | peak drop 0.77% ≤ 2% ✅ |
| Board pool (redistribution audit) | 660,325 | 679,055 | **net +2.84%** — see attribution |
| Panel | 10/10 baked | **10/10 candidate re-stamp** | all-levers-OFF = byte-exact baked ✅ |

## Per-lever attribution (leave-one-out; sums ≈ the net, interactions ≈ 0)
| lever | board Δ | movers | what it did |
|---|---|---|---|
| L1 fwd-recal (credit − fade) | +15,510 (+2.28%) | 165 | elite present-margin credit, funded by moderate far-year fade |
| L2 young runway | +7,509 (+1.11%) | 420 | survivor reward forward (year-1 cohort lift, V0-fed) |
| L3 ruck #44 + smooth young headroom | +572 (+0.08%) | 11 | production-derived ceiling; young-ruck fade, no pk20/21 cliff |
| L4 aging decline #45 | +886 (+0.13%) | 12 | form-conditioned shed (12 movers — matches PR #45 exactly) |
| L5 v7 form-conditioned | +1,856 (+0.27%) | 96 | demonstrated producers keep q97 tail; speculation stays compressed |
| L6 KPF treatment | −2,815 (−0.41%) | 27 | established-above-EFV residual compressed; above-REPL reward |
| L7 deep-pick compress | −4,563 (−0.67%) | 191 | the owner-agreed #43 cells only |
| L8 PVC fit (downstream) | picks only | 0 players | verified: 0 player values moved prefit→final |

## Owner anchors — before → after (full per-player lever split in the HTML)
| anchor | baked | candidate | Δ | driver |
|---|---|---|---|---|
| **Marcus Bontempelli** (target ≥+10%) | 3084 | **3524** | **+14.3%** | fwd-recal +440 (present margin + captaincy + durability) |
| **Max Gawn vs Kieren Briggs** | 2112 vs 2145 (BELOW) | **2413 vs 2109 (+14.4% ABOVE)** | ✅ | Gawn fwd-recal +301; Briggs fade −47 |
| **Jeremy Cameron** | 1143 | **1252** | **+9.5%** | KPF reward +41 · fwd-recal +109 |
| **Sam Darcy** (owner read: UNDERPRICED) | 4144 | **4330** | **+4.5%** | young +162 · v7-form +25 · KPF lever **0** (protected) |
| **Willem Duursma** | 4110 | **4295** | +4.5% | young runway +185 (year-1 cohort lifted under the bound) |
| **Zak Butters / Max Holmes** | 5174 / 5386 | **5745 / 5959** | +11.0% / +10.6% | HELD and rising (credit, zero fade — elite) |
| Coniglio / Adams / Blicavs / Guthrie | 112 / 72 / 9 / 465 | 116 / 72 / 9 / 464 | +4 / 0 / 0 / −1 | **faders still drop/hold at scrap** (Coniglio's +4 = lifted V0 floor basis, attributed) |
| Sam Walsh (#45 stack) | 2261 | 2756 | +21.9% | aging +411 (the PR #45 lever) + credit +55 |
| Goad / Green / Smillie (panel sat-outs) | 723 / 536 / 974 | 801 / 563 / 1015 | +10.8% / +5.0% / +4.2% | young-ruck smooth headroom + young credit |
| Louis Emmett (#44 anchor) | 855 | 788 | −7.8% | production-honest ceiling — inside your 650-800 band |
| Riley Thilthorpe (KPF funding side) | 3702 | 3202 | −13.5% | KPF compress −541 (the loose-residual locus: McDonald, Lukosius, Naughton, King, McLean same direction) |

## Sam Darcy — the three-locus breakdown (what was holding him down)
1. **Young-convexity ceiling:** NOT clipped — his band's q97 (100.7) sits above his demonstrated 86.1; the v7 taper is
   now form-relaxed for him (+25).
2. **KPF young-speculative:** the KPF compress is gated `nqual≥4 AND age≥24` — Darcy (nqual 2, age 23) is outside it
   **by construction**; measured KPF lever = 0 on him. The young-KPF ceiling survives.
3. **LTI return-haircut:** B2 = 0 (he has 6 games in 2026). The layer holding him down is the **interrupted-season
   recency/exposure drag: −580 (−12%)** measured by removing the 2026 row — a forfeited-growth-year LEVEL drag, not a
   ceiling dent. The W4 young credit (+162, position-relative runway) offsets part of it; the remainder is the injury
   channel the next-phase LTI re-measure must price NET of this candidate's aging side (no double-count verified —
   `MESH_AND_CAPTAINCY.md`).

## Guards (all on the RESULT; three-column vs baked)
1. **No-arbitrage ≤130:** 124.6% ✅ (in guide). 2. **Monotone pick curve:** fitted PVC non-increasing, smooth;
young-ruck fade cliff-free ✅. 3. **Never-crater (B5):** feature intact, 52 saves (list did NOT grow), 0 lowered ✅.
4. **Survivor peak:** B1 PASS, peak index −0.77% (≤2%), Butters/Holmes rising ✅. 5. **Convexity premium:** young thin
+1.5%, B6 ramp PASS ✅. 6. **Five data guards + Guard 5:** PASS everywhere; panel 10/10; **B2 leakage 0.0 %-pts**;
**B4 parity byte-agree**; **D14a/b/c PASS**; B3 candidate book SEALED (`264f2847`), vs-baked-seal DIFFERS as expected
on a value-moving candidate (identical key set, 2,136 attributed moved records). Ship-gates: FAIL=4 vs baked FAIL=3 —
the moved red IS that B3 comparison; **A2/A12 pre-existing reds unchanged; A3 (Rozee, data-caused knife-edge)
0.73→0.71** — the production-gated credit gives his LTI-wiped 2026 less than his elite 2025; flagged to the injury
phase. 7. **Attribution:** delivered (8 kill-switches; `RL_FWDRECAL/RL_YOUNG/RL_OVPX/RL_KPFFIX/RL_V7FORM/RL_W4_RUC/
RL_FORMDECL/RL_PVCFIT`; ALL-OFF = byte-exact v2.5, verified).

## PVC fit (downstream, separable)
Fitted per the re-stamped spec from 1,448 candidate year-1 anchors (2004-2024, live ruck values): **much steeper than
v3.4** — pick 8 −32%, pick 45 −42% vs pick-1=3000. Picks-only by construction (player board identical with it on or
off). This is the largest owner-facing relative move in the candidate → **your ruling**; A14 (Rivers/Reid/Burgoyne)
reads non-lineball against it (established pick-8ers price ~1.4-1.7× the year-1-typical pick 8). `PVC_FIT_NOTE.md`.

## Queued for owner ruling (nothing auto-applied)
1. **MID 1-3 over-flag (2.09)** — untouched, as ordered. 2. **PVC fitted curve** — accept/reject via `RL_PVCFIT`.
3. **Captaincy TITLE dial** — production-keyed captaincy premium is modelled + credited; the captain-slot/role itself
is not — proposed register-driven dial (`MESH_AND_CAPTAINCY.md`). 4. **Jackson/Xerri cross-position richness** —
pre-existing #44 flag, amplified ~+11% by the credit (both are genuine elite-margin rucks); ruled at calibration.
5. **Net pool +2.84%** — the ordered lifts exceed what the named funding cohorts (KPF residual, deep picks, moderate
far-years) supply; the funding legs are at their data-earned depth, so the remainder is honest net credit — your read.

## Time
Estimated 4-8h (confirmed up front); actual ≈ 6.5h including two full board builds, two walk-forward book builds,
gate1, gates board, and 8 attribution sweeps. Within band.

## IN PLAIN TERMS
Bontempelli clears +10% (3084 → 3524, +14.3%). Gawn now sits clearly above Briggs (2413 vs 2109 — he was below).
Cameron rises (+9.5%), and the key forwards funding it are the ones whose price wasn't backed by output (Thilthorpe,
McDonald, Lukosius, Naughton, Max King). Sam Darcy lifts (+4.5%) — what was holding him down was the interrupted-2026
drag, not his ceiling: the young-KPF machinery never touches him, his boom tail is intact, and he now carries proper
runway credit for a 23-year-old key forward. Duursma gets his runway credit (+4.5%) with the whole year-1 draft class
lifted, Butters and Holmes are held and rise ~+11%, and the genuine faders (Coniglio, Adams, Blicavs, Guthrie) stay
on the scrap heap. The cohort ratio holds at 124.6% — inside your 120-125 guide, better than the baked board — and
every reproducibility guard passes on the candidate. Two things need your word: the new pick curve (it prices picks
much lower against players — real, defensible, but the biggest visual change), and the fact that the whole board is
net +2.8% richer because your ordered lifts are bigger than the named funding pockets. Nothing here is baked — it all
waits for the cold audit and your call.

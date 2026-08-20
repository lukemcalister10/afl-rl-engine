# PACKET — RECENCY AUDIT: THE ENGINE'S EFFECTIVE SEASON WEIGHTS vs THE MEASURED OPTIMUM

**Seat:** recency audit (small scope), issue #334 follow-on to Order 33 seat W4. **READ-ONLY:**
nothing in the engine, board, store or law was touched; every perturbed player existed only in
memory. **Prereg:** `PREREG_RECENCY.md`, pushed before any measurement.

**The one-line answer:** the engine does NOT flat-average a player's seasons — the feared failure
mode is absent. It leans the other way: its effective weighting is MORE recency-concentrated than
W4's measured optimum, holding roughly twice the optimal concentration on the newest read (median
~74% of the price response sits on the in-progress 2026 season alone, ~99% on 2025+2026 together,
vs the optimum's ~57–61% on the latest season). By the letter of the prereg the headline verdict
is the honest **TOO NOISY TO CALL** (the perturbation-size trip fired at 0.130 vs the 0.10 bar);
the DIRECTION, however, is robust at every perturbation size tried and in every class split.

---

## 1 · The designed scheme (code read, plain words)

There is no single season-weight table. The production price reads multi-season history through
five recency-weighted readers, each with its own per-year-back decay:

| reader | where | decay per year back | role |
|---|---|---|---|
| `_lvl_wt` / `_lvl_eff` / `_exposure` | `engine/forward_valuation/conditional_prior.py:100-118` | **0.72** (`RL_RECENCY_DECAY`, pinned env dial) × games | the conservative career level `Lo` and the GBM band-prior features (`_feat` → `cond_prior_band` → `b6`) |
| `_lvlcurr` | `engine/rl_after/_merged_recover.py:305-309` | **KEY 0.40 · GEN 0.35 · MR 0.225** (`LDECAY_G`) × damped games w(g)=g²/(g+5.8) | the steep "current level" `Lc`; blended over `Lo` by evidence weights (`_ev_rec`, `_ev_est`), then through the asymmetric `_est` hold/shed |
| `level_demo` | `engine/rl_after/rl_model.py:757-803` | latest qualifying season at trust `conf` (clamped 0.20–0.92) vs a **0.60**-decay prior; recency-floor: a recent game never weighs less per-game than an older one | the demonstrated-form anchor `b6`/`price6` consume |
| `rho_out` | `engine/rl_after/_merged_recover.py:494-509` | **0.25** (`UNCOMP_DECAY`, owner-set R105.6 "a recent game counts MORE… a quarter") × games | the un-compress ρ axis (strength s=0.10) |
| `track_delta` | `engine/rl_after/rl_model.py:996-1001` | **0.78** calendar | the v4 forward-projection cohort delta |

Everything is recency-weighted BY DESIGN (the L-RECENCY self-test R105.5 enforces per-game weight
non-increasing in years-back); the decays span 0.225–0.78, so the EFFECTIVE weight of a season in
the final price is a blend nobody had measured. That is what this seat measured.

## 2 · The measurement

Candidate build, dial on (`RL_O31=1`, the bb31f staging recipe, store cb38ef11, strictly
sequential, thread-pinned; engine loaded read-only in-process). **38 real players**, stratified
(position group KEY/GEN/MR × 2–6 played seasons, seeded draw fixed in the prereg), base price
≥ 100. For each player, EACH played season's average was raised **+2 points, one season at a
time, in an in-memory copy**, and the price `ev(p, 2026)` (unrounded, one-law lane) re-read.
Normalized responses ŵ_s = the engine's effective season weights.

**Effective weight by years-back (36 usable players; RL_O31 lane):**

| years back | n | mean | median | q25 | q75 |
|---:|---:|---:|---:|---:|---:|
| 0 (2026 in-progress) | 33 | 0.667 | **0.745** | 0.541 | 0.964 |
| 1 (2025) | 34 | 0.259 | 0.161 | 0.061 | 0.323 |
| 2 (2024) | 28 | 0.106 | 0.066 | 0.000 | 0.158 |
| 3 | 19 | 0.111 | 0.002 | 0.000 | 0.105 |
| 4 | 15 | −0.000 | 0.000 | −0.003 | 0.002 |
| 5–6 | 10 | ~0.01 | 0.000 | — | — |

Latest-season share (2025 + 2026-in-progress): **mean 0.856, median 0.985, IQR [0.841, 1.000]**.
Per-player retention ratio ŵ₁/ŵ₀ (n=30 with ŵ₀>0.05): **median 0.19, IQR [0.04, 0.50]** — wide,
per the honesty clause (by group: KEY 0.29, GEN 0.31, MR 0.15).

**By class** (medians of the latest-season share / of the 2026-alone weight):
- seasons-of-history 2–3: 1.000 / 0.884 · 4–6: 0.889 / 0.672 — deeper histories soften it only mildly;
- position group MR 0.992 / **0.867** · GEN 0.988 / 0.524 · KEY 0.979 / 0.601 — mids are the most
  latest-read-priced, talls the least;
- latest completed season <10 games: 1.000 / **0.964** — even a thin current read dominates;
  10–17 games: 1.000 / 0.524; 18+: 0.901 / 0.715.

**Named rows (weights by years-back, newest first):** Nick Daicos [0.79, 0.10, 0.06, 0.04, 0.01];
Errol Gulden [1.03, 0.07, 0.07, −0.07, −0.10, 0.00] — raising his 2022–23 seasons LOWERS his
price; Aaron Cadman [0.76, 0.22, 0.02, 0.00]; Harley Reid [0.58, 0.33, 0.09] — the closest row in
the sample to the W4 optimum shape; Jack Williams [0.24, 0.21, 0.22, 0.33] — the one near-flat row in the
sample, and it is actually OLDEST-heaviest (a thin KPF whose 2023 season carries the most).

## 3 · Honesty: dispersion, nonlinearity, nonmonotone rows

- **The prereg trip FIRED**: median across 10 players of max_s |ŵ_s(δ=+1) − ŵ_s(δ=+4)| = **0.130**
  (bar 0.10). The weights are perturbation-size sensitive — bigger perturbations cross the
  engine's hold/shed and delivered-bar thresholds, moving mass BETWEEN the newest 1–3 seasons
  (e.g. Duursma 2026 weight 1.00 at δ=1 → 0.47 at δ=4). Per the prereg's fixed rule the formal
  verdict is **TOO NOISY TO CALL** and the class splits above are descriptive.
- The DIRECTION survives the trip: the latest-share median is 1.000 at δ=1 and 0.916 at δ=4 on
  the same 10 players — at no size tried does the engine's mass move toward the older seasons.
  Cross-player IQR of the latest share (0.159) is inside the prereg's 0.35 dispersion gate.
- **Nonmonotone rows, disclosed**: 2 of 38 players price DOWN when a past season is improved
  (Reuben Ginbey −40.8 total, Colby McKercher −84.2 total); 25 individual season responses are
  negative (mostly tiny; largest: Tauru/O'Sullivan-Connor 2026 ≈ −13). The `_est` hold/shed
  asymmetry and the `level_demo` growth-vs-baseline branch make "a better past" occasionally read
  as "a worse present-vs-past" — a standalone structural observation, filed here, not ruled on.

## 4 · Comparison to the W4 optimum

W4's benchmark (PACKET_W4 §2, MEASURE_W4 s5): best convex level weighting
`L_w = (P(Y) + w·P(Y−1) + w²·P(Y−2)) / (1+w+w²)`, **w\* = 0.45–0.5 in every fold** → normalized
weights ≈ **[0.57–0.61, 0.27–0.29, 0.12–0.14]** on the last three seasons; per-season retention
0.45–0.5.

| | latest | −1 | −2 and older | retention ratio |
|---|---:|---:|---:|---:|
| W4 optimum | 0.57–0.61 | 0.27–0.29 | 0.12–0.14 | 0.45–0.5 |
| engine, measured (mean) | 0.67 (2026 in-progress) | 0.26 | ~0.11 | — |
| engine, measured (median) | 0.745 | 0.161 | ~0.07 | 0.19 [0.04, 0.50] |

Read with the caveat that W4's grid has no in-progress-season concept (its "latest" is a
completed season; the live board's newest evidence is the 2025/2026 pair): the engine's effective
weighting is **at or beyond the recency-heavy edge of the optimum** — the owner's standing
instinct ("recent seasons should matter more") is honoured and then some. The shortfall relative
to the optimum sits on the **1-to-3-back seasons**: the optimum keeps ~0.27–0.29 on the season
before the latest and ~0.12–0.14 two back; the engine's median row keeps ~0.16 and ~0.07. Mids
(MR group, steepest designed decay 0.225) sit furthest from the optimum; talls (KEY, 0.40)
closest. Nothing anywhere resembles a flat average — that hypothesis is dead on this sample.

**RL_O32 disclosure pass (the ORDER-A repair candidate at this HEAD, 12-player subsample):**
per-player weights are near-identical to the RL_O31 lane (Darcy Jones [0.53, 0.47] in both
lanes; Conor Stone 0.77 on 2026 in both; Tauru's 2026 sign inversion reproduces). Latest-season
share median 1.000, IQR [0.828, 1.000]; 2026-alone median 0.608. The repair does not move the
effective recency weighting — this finding carries to the repair candidate unchanged.

## 5 · Rulings material — descriptive, contingent on §3's noisy call. AWAITING RULING.

IF the W4 optimum is taken as the target, the mispricing direction is: rows whose latest season
diverges most from their history are priced almost wholly off the newest read where the optimum
would keep ~0.29 of the evidence on the season before. From the current board
(`docs/ledgers/CANDIDATE_31_MOVERS.json`, divergence = latest completed avg vs 0.72-decayed
prior history, store-only):

- **Single-season risers (would be over-credited):** Daniel Curtin (+40.2 avg pts, cand 2047),
  Ryan Maric (+39.9, 1238), Zach Reid (+39.3, 912), Ned Long (+37.1, 1145), Finn Callaghan
  (+36.0, 5471), Riley Thilthorpe (+34.9, 4067), Lachlan Ash (+31.5, 5303), Tristan Xerri
  (+30.4, 6948).
- **Single-season faders (would be over-punished):** Stephen Coniglio (−33.4, 211), Zac Fisher
  (−27.0, 116), Kyle Langford (−25.3, 505), Liam Henry (−25.1, 142), Peter Ladhams (−24.4, 449),
  Bailey Scott (−24.3, 20), Koltyn Tholstrup (−24.1, 1488), Jordan De Goey (−23.6, 1365).

**Fix family (named, NOT wired, AWAITING RULING):** a re-weighting inside the production
evidence — soften the effective recency of the level readers (the `LDECAY_G` {0.225/0.35/0.40}
per-group decays, the `level_demo` conf-trust on the latest read, and the in-progress-season
trust) so the MEASURED effective retention ratio lands near the W4-measured 0.45–0.5, re-run
this harness as the acceptance check. Separately filed: the §3 nonmonotone rows (a better past
season lowering today's price) point at the `_est` hold/shed and `level_demo` baseline branches.
No engine edit, no board, no artifact ships from this seat.

## 6 · Files

All in `docs/evidence/order34_recency_2026-08-17/` on `land/order-29`: `PREREG_RECENCY.md`
(pushed first) · `recency_measure.py` (the harness; bb31f staging, in-memory perturbation only) ·
`RECENCY_WEIGHTS.json` + `MEASURE_RECENCY_primary_out.txt` (every number above, per-player) ·
`RECENCY_O32.json` + `MEASURE_RECENCY_o32_out.txt` (the repair-candidate disclosure pass) ·
this packet.

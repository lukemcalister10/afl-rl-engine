# THE CAMEO-STRENGTH-AWARE CONDITIONAL PRIOR — exact specification

Store of record `fb640ca0baf92bbb122b1ad7e25c5a88`. Prereg `PREREG.md` md5 `28b6a0dcb0ffcd0936ce2cbc4453630f`,
stamped 2026-08-24T12:25:14Z, before any fit. Read-only on the repository; zero repo writes.

## 1. TARGET (decided by reproduction, s2)

    T_bp(p) = mean of the top 3 season averages among seasons with games >= 6, in the player's own
              career from debutyr onward;  0.0 if no season qualifies.

This is the recovered bust-prior producer's own target (v835 "peak_ib best-3>=6g else 0"). It is the
ONLY target that reproduces the directive's anchors — picks 12-30, games 1-8: t2 45.0/62.7,
t3 20.5 (68.8% bust)/48.4, all four exact. The seam study's `T_eng` (`cp.fwd_best3_from`) cannot
produce ANY bust rate: it falls back to the best sub-6-game season, so a 3-game 30-average career
scores 30, never 0.

## 2. THE OBJECT

    mu(pos, k, t, g, c) = (1 - A(t,g)) * B(pos,k)  +  A(t,g) * T(c,t)

    k = MA.effpk capped 70 · t = tenure 1..4 · g = career games through Y = debutyr-1+t
    c = RAW games-weighted cameo average through Y = sum(games_s * avg_s) / sum(games_s)
        over seasons with games_s > 0  — the axis the level vocabulary cannot see:
        81.1% of in-scope states have level_through == 0 ("none") while their c spans 4.0 to 86.0.

    B(pos,k)  the DRAFT-DAY BUST PRIOR, v838 MODERNIZED construction verbatim: isotonic decreasing
              on effpk, 5-point moving average, re-projected monotone, position blended to pool at
              credibility w = n/(n+100). A = 0 reduces mu EXACTLY to B: the candidate NESTS its
              own baseline.
    T(c,t)  = M(t) / (1 + exp(-(c - c50(t)) / w_c)),   M(t) = M1 * exp(-(t-1)/tauM),
              c50(t) = c0 + beta*(t-1)
    A(t,g)  = (1 - r) * W / (W + kappa(t)),   kappa(t) = kappa0 * exp(-(t-1)/tauK),
              W = sum_s w(g_s),  w(g) = g^2/(g + 5.8)   <- THE ENGINE'S OWN FIX-1 DAMPING,
              `_DAMP_K`, `_merged_recover.py:191`, reused verbatim, not reinvented.
              r = 0 in CAND-A; r = `_EVW_R` = 0.11 in CAND-B (`_merged_recover.py:208`).

### Fitted constants (TRAIN = debut 2006-2014, n=580 states / 335 players)

| variant | M1 | tauM | c0 | beta | w_c | kappa0 | tauK | r | train RMSE |
|---|---|---|---|---|---|---|---|---|---|
| CAND-A (pre-registered, 7 par) | 118.8946 | 2.4067 | 40.0220 | 0.0000 | 9.0097 | 5.1872 | 0.5197 | 0 | 30.0818 |
| CAND-B (declared variant, 6 par) | 124.3193 | 2.1768 | 40.9558 | — (fixed 0) | 8.2650 | 4.8529 | 0.4591 | 0.11 | 29.8419 |

Refit on the FULL primary window for repricing (no OOS claim): M1=149.7064, tauM=2.1061, c0=45.8848,
w_c=13.6587, kappa0=4.6810, tauK=0.4333.

Fit procedure: `scipy.optimize.least_squares` on ROW-LEVEL realized `T_bp` over in-scope TRAIN states,
bounded, xtol=ftol=1e-12. Squared loss on rows IS the conditional-mean fit — the validation basis.

### Why CAND-B exists (s4, TRAIN only)
- `beta` settled ON its bound in CAND-A and buys 0.05% of train RMSE (30.0818 -> 30.0677 when freed,
  and it wants to go NEGATIVE, -2.8). Dropped: one fewer parameter, tenure effect rides M(t) alone.
- CAND-A's `A` reaches 0.997 at t4, ERASING the pick. Measured residual pick signal (Spearman of
  cameo-residualised outcome on effpk, TRAIN): t1 -0.268 (p=0.0001), t2 -0.250 (p=0.0011),
  t3 -0.220 (p=0.016), t4 -0.114 (p=0.275, n=94 — unresolvable, NOT absent). The engine already
  refuses this erasure by rule (R98.5: "the pedigree hump fades to residual r=0.11, NEVER vanishes").
  CAND-B inherits that constant rather than inventing one.

## 3. CONSTRAINTS — SATISFIED STRUCTURALLY, PROVEN NUMERICALLY

Dense grid, 6 positions x picks 1-70 x t1-4 x g1-8 x c 0-100:
- monotone in pick — 0 violations of 19,392 curves. Structural: mu is a convex combination of B(k)
  (monotone by isotonic construction) and T (constant in k), A in [0,1] and NOT a function of k.
- monotone in cameo average — 0 violations of 192 curves. Structural: T logistic, A >= 0.
- smooth (L-SMOOTH) — max |2nd difference| over pick = 2.65 level-points; no plateau, no cliff, no
  branch anywhere. Every component is C-infinity in g and c. Largest integer step in games is
  g=1->2 at t3 (10.6 level-points) and it is the engine's OWN w(g) rising steeply there, not a cliff.
- weak-late harshness PRESERVED (picks 12-30, games 1-8, cameo<45; measured vs fitted):
  t1 60.7 / 63.9 · t2 45.0 / 48.1 · t3 20.5 / 24.6 · t4 20.4 / 16.3 (CAND-B).
  The bust prior alone says 68.3 / 66.0 / 68.7 / 66.9 at the same four cells — it cannot bend at all.

## 4. DECLARED POOLING CHOICES AND THIN CELLS

- `A` is PICK-INDEPENDENT. Tested (s6D): a pick-tilt parameter fits gamma = -0.0245, 90% CI
  [-0.825, +0.776] — CI includes 0, pooling not contradicted, train RMSE unchanged to 4 decimals.
- POSITION is pooled inside `T` and `A`; position enters ONLY through `B`. Not separately testable
  at these n (RUCK n=94 is the thinnest B cell).
- `B`'s population is the bust-prior producer's own predicate (all GRP-mapped rows by `MA.debut`),
  WIDER than the ND/picked/effpk<=70 scope population. Kept as the producer wrote it; declared.
- CAMEO BAND 65+ is UNRESOLVED at t3 (n=6) and t4 (n=4) and the raw data INVERTS there (t3 65+ mean
  19.5 < 45-65 mean 40.5; t4 65+ mean 0.0, n=4). Monotonicity in c at those cells is IMPOSED BY THE
  CONSTRUCTION, not measured. Declared: any 65+ price at t3/t4 is model, not evidence.
- Resolution ladder (the seam study's, reused): n>=25 RESOLVED · >=15 THIN · >=5 VERY THIN ·
  <5 UNRESOLVED. UNRESOLVED cells are published as UNRESOLVED and never smoothed into confidence.
- Picks 65-70 have NO day-0 anchor (`nd_v0.posv` covers 1-64), so 114 in-scope states and 1 live row
  (aidan-johnson) are UNPRICEABLE by M1. The study's finding (4), unchanged.

## 5. INTEGRATION SITE — the directive's nomination is MEASURED INERT; a different site is proposed

The directive nominates the pw(E) pedigree blend (`_merged_recover.py:297-300`, consumed at `:1256`).
MEASURED at all 52 live in-scope rows (s12): **pw(E_q) max 0.0117, mean 0.00061, median 0.0000020.**
The pedigree par carries at most 1.17% of the level at ANY row in the construction's scope. Cause:
`_EVW_Q0 = 11.0`, the soft 10-game qualifying bar — a 1-8 game season contributes <= 0.065 to E_q,
so `gate = Eq^2/(Eq^2+0.55^2)` ~ 0. `_ev_rec` and `_ev_est` are ~0 for the same reason, so
`_coreM1` collapses to `Lo = cp._lvl_eff_orig` (max |lvl_eff - Lo| = 0.976 over the 52 rows, mean 0.021).
**Placing the prior at the pw(E) term would multiply it by ~nothing.**

There is a second reason that site is wrong: `_lvl_eff` is a CURRENT level consumed by the convex
price curve, while this construction predicts EVENTUAL BEST-3 — a career-peak summary. Substituting
one for the other would double-count the engine's own peak projection.

**PROPOSED SITE: `engine/rl_after/rl_model.py:1235` — `_v4_bp(po,pk)`, the peak model's `bust_prior`
feature.** It is today a pure function of (position, pick) with zero conditioning on evidence state,
consumed by `_v4_feats` (:1245) and `_v4_draft_feat` (:1247), and `peak_model_v4`'s training target
is forward-realised bust-inclusive best-3 — THE SAME UNITS as `mu`. The change is:

    _v4_bp(pos, effpk)   ->   _v4_cp(p, Y) = mu(gfut(p), effpk(p), tenure, games_through, cameo_avg)

Properties: (i) it NESTS the current feature exactly — A=0 gives B(pos,k), which IS today's
`_v4_bp`; (ii) `_v4_draft_feat` is zero-evidence so A=0 identically and **day-0 is byte-exact by
construction**; (iii) it is the same object the design arm is already choosing a table for (owner
decision (a), v838) — this makes that table the A=0 limit of a conditional surface.
REQUIRES a peak-model refit (the feature's distribution moves), which is design-arm business.
CONSEQUENCE, stated plainly: the board effect of the landed lever is therefore NOT the M1 repricing
in §6 — M1 says what the outcomes imply, the refit says what the engine would do about it.

## 6. WHAT WAS NOT BUILT
No repository file was written or modified. Nothing was landed, wired, or proposed for landing.
The year-4 sitter-credit option (s9) is parameterized and reported SEPARATELY and is NOT blended
into any figure above. The sitter fade LEVELS are untouched and stand calibrated.

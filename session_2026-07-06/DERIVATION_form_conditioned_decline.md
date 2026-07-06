# Form-Conditioned Aging Decline — DERIVATION (2026-07-06, candidate)

Single lever: the **DECLINER SHED** decline multiplier in `engine/rl_after/_merged_recover.py`.
Store `e1b4d8bf` (unchanged) · engine head `efea88e5 → 4226b61d` · band `34faa865` · boot_guard PASS.

## 1. Characterize — age-keyed vs form-conditioned (BEFORE)

v2.5's veteran decline is **form-GATED but age-KEYED in magnitude**. In `_coreM1` (the live level core,
bound via `cp._lvl_eff=_inferM1`), an established player (`nq≥PROVEN_N=4`) whose recency-weighted level
`Lc` sits `>DOWN_TOL(3)` below his established level `Lo` is shed toward `Lc·_agemult(age)`:

```
drop=Lo-Lc; if drop<=3: return Lo
sw=clip((drop-3)/5,0,1); return (1-sw)*Lo + sw*Lc*_agemult(age)   # _agemult is a fn of AGE ALONE
```
`_agemult(age)` = interp over `[20,22,25,28,30,32,34,37] → [.92,.89,.85,.79,.73,.68,.62,.55]`.
Consequence: a still-elite elder who dips is multiplied by the SAME age factor as a genuine fader.
A former-Brownlow-level 33yo (Lachie Neale, Lc≈107, 27 above replacement) is shed at `Lc·0.65`.

## 2. The genuine-decliner contrast set (must keep falling)

From the 386-player shed cohort, the bottom-by-`lcr` are the genuine faders (established, output HAS
faded with age, now at/below positional replacement):

| player | pos | age | Lo | Lc | drop | lcr=Lc−REPL | ev |
|---|---|---|---|---|---|---|---|
| Stephen Coniglio | MID | 33 | 82.5 | 67.6 | 14.8 | −12.5 | 112 |
| Taylor Adams | GEN_FWD | 33 | 78.1 | 60.3 | 17.8 | −10.6 | 72 |
| Mark Blicavs | MID | 35 | 79.9 | 70.4 | 9.5 | −9.7 | 9 |
| Cameron Guthrie | MID | 34 | 90.8 | 76.2 | 14.6 | −3.9 | 16 |

These must NOT be lifted — the curve must still drop them. (Verified §5: all Δ=0.)

## 3. Measure — realized decline r = f(age, lcr)

For every established shed-population player-season (`nq≥4 & Lo−Lc>3`, debut..2024, **2369 obs**), the
realized forward level `Lfwd` = washout-inclusive mean of the next up-to-3 complete seasons' avg (a
non-played / <6-game season contributes 0 — the predecessor's convention), and `r = Lfwd/Lc`
(winsor 2.0). Level axis `lcr = Lc − REPL[gfut]` (production above positional replacement).

Realized r is **strongly form-conditioned**, not age-only:

```
mean r by lcr:  [-40,-10) 0.11 | [-10,0) 0.25 | [0,10) 0.41 | [10,20) 0.59 | [20,60) 0.90
mean r by age:  [20,28) 0.50 | [28,30) 0.32 | [30,32) 0.21 | [32,34) 0.12 | [34,40) 0.03
```
A still-elite elder (high lcr) realizes ~90% of current forward; a faded one (low lcr) ~10%. The
age-only `_agemult` collapses this whole lcr axis to a single per-age number → over-sheds the elite.

## 4. Fit — up-only credit bump over the age curve

`_agemult2(age, lcr) = clip(_agemult(age) + bump(age,lcr), 0.53, 0.98)`, where `bump ≥ 0` is the
kernel-smoothed **up-only** residual `E[max(0, r − _agemult(age))]`:

- **Smoothing:** 2-D Nadaraya–Watson, Gaussian kernel, adaptive bandwidth grown until **eff-n ≥ 35**
  per grid node (house convention, cf. the V0/`R_SURF` fits). Grid age `[22,25,28,30,32,34,37]` ×
  lcr `[-15,-5,5,15,30]`.
- **Pooling (DECLARED):** all positions POOLED into one surface (predecessor measured position ~uniform;
  RUC is thinnest). **Shrinkage (DECLARED):** thin cells (eff-n<35) shrink `bump→0` (fall back to the
  1-D age prior); here every node reached eff-n≥40, so the shrink stayed inert.
- **Monotone:** isotonic non-decreasing in lcr at each age; non-increasing in age at each lcr; ≥0.
- **Runtime knots** (0-anchored, positive-lcr only): `_FB_LCR=[0,5,15,30]`, `_FB_Z` per age row.

Resulting `_agemult2` at the knots (vs age-only in brackets):

```
        lcr:   +5     +15    +30
age 30:      0.80    0.82   0.87   [_agemult 0.73]
age 32:      0.73    0.76   0.82   [_agemult 0.68]
age 34:      0.66    0.70   0.76   [_agemult 0.62]
```

## 5. Single-lever safety + verification

- **`lcr≤0` hard-zero** → every below-replacement fader is byte-exact (Coniglio/Adams/Blicavs Δ=0).
- **Up-only** → the curve never sheds MORE than the age baseline: no down-mover, respects the
  predecessor's price6-convexity over-shed caveat.
- Reached **only on the shed down-branch** → every non-shed player is Δ=0 by construction.
- **Kill-switch** `RL_FORMDECL=0` → byte-exact to baked v2.5.

**Results (RL_FORMDECL 1 vs 0, same candidate engine):** 12 movers of 2652, **all UP**, all
above-replacement established shed players, ages 26–30, board total +936 (+0.14%). Panel 10/10 (off and
on). ship_gates verdict `FAIL=3 FEATURE=1 PASS=17 PENDING=4 STRUCK=1` — **identical to baked v2.5**
(the 3 fails A2/A3/A12 are pre-existing amended fails, unchanged). **B1 cohort peak UNMOVED**
(`1:100 2:122 3:133 4:143 5:141 6:133 7:116`); **B3 walk-forward book byte-identical** to the v2.5 seal;
**B4 board parity** PASS on the committed candidate board.

Movers: Sam Walsh +424, Dan Houston +113, Charlie Curnow +86, Adam Cerra +62, Jordan Ridley +43,
Touk Miller +43, Luke Ryan +42, Hugh McCluggage +39, Dylan Moore +37, Andrew Brayshaw +28,
Lloyd Meek +11, Kieren Briggs +8.

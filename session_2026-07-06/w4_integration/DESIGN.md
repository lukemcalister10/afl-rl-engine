# WAVE-4 INTEGRATION — design note (one coherent candidate: forward-valuation recalibration + fold-ins)
**2026-07-06 · base v2.5 `origin/main` (store `e1b4d8bf`, engine `efea88e5`) · multi-lever BY DESIGN (single-lever
discipline OFF, replaced by per-lever attribution + the guard suite). Candidate — no merge, no promote.**

## The axis (where the recalibration lives)
Every board price flows through `proj_from_peak` (rl_model.py:302-320): value = Σ_k posval(level_k + capt − REPL)
· 21/(1.15)^k over the forward horizon (break at age>38 / frac<0.42). The #45 report-only diagnosis pinned the owner's
three reads to exactly this axis: Gawn<Briggs is 4-vs-12 forward years; Bontempelli-vs-young is the runway discount;
the year-k weight treats a moderate producer's year-9 margin as being as certain as an elite's year-1 margin.

**Recalibration = a form-conditioned weight W(k) on the year-k contribution** (never age-keyed; margin/evidence-keyed):

```
W(k) = 1 + CRED·kpf_up·g(m)·dur·sh·c_near(k)            [proven players — the certainty credit]
         − FADE·(1−g(m))·h_far(k)                       [proven players — the moderate-margin far-year fade]
       | 1 + YCRED·thin·yage·c_yng(k)                   [thin-career young — the runway/survivor-forward credit]
       then ×(1 − OVPX·ovpx_gate)                        [deep-pick GEN_FWD 41-70 over-optimism compress]
```
- `m = Lc − REPL[pos]` (demonstrated current level above positional replacement; the same conditioning variable as #45)
- `g(m) = clip((m−6)/22, 0, 1)` — 0 at m≤6 (Briggs 5.1 → no credit), 1 by m≈28 (Bont 41.7, Gawn 48.0)
- `dur` = games(Y−2..Y)/28 clipped [0,1] — durability; `sh` = 1−clip((Lo−Lc−3)/5,0,1) — decline gate (mirrors the shed
  switch: a genuinely declining player earns no certainty credit)
- `c_near(k) = interp(k,[0,2,5],[1,1,0])` — present-tense credit, runway-independent (short-horizon elites benefit most)
- `h_far(k) = interp(k,[4,10],[0,1])` — the funding leg: a moderate-margin established player's years 5+ carry
  washout/decline risk the flat 15% discount never charged ("washes out before Gawn's age")
- young leg: `thin = 1−nqual/4`, `yage = clip((23−age)/2,0,1)`, `c_yng = interp(k,[0,1,4,8],[.6,1,1,0])` — prices the
  survivor reward forward (year-1/2 cohort lift), governed by the ≤130% no-arbitrage bound (baked baseline = 125.2%)
- captaincy: enters through `capt_prem(lev)` inside every credited year — the near-year credit automatically credits a
  captain's premium more (present-tense, runway-independent). Contribution measured + reported; a dedicated captaincy
  dial is PROPOSED (owner rules), not silently invented.

Wired as a monkeypatch of `MA.proj_from_peak` from the head with a per-call player context set by a `raw_ev` wrapper:
synths (pole/ISO/gate/ruck-ceiling) carry no key → context None → byte-exact delegation to the original. The wrapper
binds BEFORE the V0 guard/curve builds, so the young credit flows into V0 → the year-1 anchors → the book's y1 cohort.

## Fold-ins (reconciled, no double-count)
- **#45 aging (RL_FORMDECL)** — verbatim hunks: `_agemult2(age,lcr)` form-conditioned decliner shed. Faders (lcr≤0)
  byte-exact → still drop.
- **#44 ruck (RL_W4_RUC)** — verbatim hunks: production-derived ceiling on the production leg (RUC_CEIL_HEAD=0.80 ×
  synthprice_RUC@REFPK=72). EXTENDED with the owner-required smooth young-ruck headroom (no pk20/21 cliff):
  `head_mult(p) = 1 + YRH·interp(pk,[1,4,18,30],[.7,1,1,0])·clip((25−age)/4,0,1)` applied to BOTH the production
  ceiling and the no-production prior cap (fades in pick AND age; targets the #43 under-priced pocket RUC pk1-20,
  coverage 0.61-0.73, without touching the over-flag RUC 21-40).
- **v7 age-taper form-conditioned (RL_V7FORM)** — the #45 HARD FLAG: `asc' = asc + (1−asc)·φ`,
  `φ = clip((lcr−4)/26,0,1)·min(nq/2,1)·V7W` — a DEMONSTRATED producer keeps more of his q97 tail at any age;
  unproven speculation (lcr≤4 or nq<1) keeps the full compression (the #43 audit: young speculation is
  correctly-to-OVER-priced).
- **KPF treatment (RL_KPFFIX)** — T1-shaped, decomposed per the directive:
  (a) REWARD: `kpf_up=1.6` on the margin-credit for KEY_FWD (a KPF scoring clearly above his low REPL bar is rarer and
  under-levered — Cameron up); (b) COMPRESS the established-above-EFV loose residual only: for established (nqual≥4,
  age≥24) KPFs, `e' = eP + 0.55·(e − eP)` where `eP` = the engine's own price of the player's DEMONSTRATED level
  (band pinned at `_lvl_eff`, same context → the credit survives; only the band/prior excess above demonstrated output
  is compressed). Young/speculative KPFs (nqual<4 or age<24) untouched → the Darcy/Duff-Tytler ceiling is protected by
  construction. No blunt group compression.
- **Over-priced flags (#43, RL_OVPX)** — ONLY the owner-agreed cell: GEN_FWD deep picks, smooth fade
  `interp(pk,[38,46,70,99],[0,1,1,1])` on thin-career (unproven) GEN_FWD, −12% at full depth (partial move toward
  coverage 2.14→~1.7; data-earned, conservative). **MID 1-3 (2.09) NOT touched — stays FLAGGED for owner ruling.**
  All other flagged cells: reported, untouched.
- **PVC fit (RL_PVCFIT, downstream)** — per the re-stamped spec (#41): PVC(k) = end-of-calendar-year-1 as-of value of
  the TYPICAL player at pick k, fitted from the CANDIDATE walk-forward book anchors (2004-2024 ND pool; the anchors
  carry the young lift and the LIVE ruck values — nothing hardcoded), kernel-median over log-pick, parametric top
  blended by ~pick 12 (loclin-at-pick-1 spirit of the spec), isotonic non-increasing, re-anchored to pick1=3000.
  SCOPE: the fitted curve re-prices the PICK side (the trade currency) + display; `draftval` for the RUC prior-cap
  basis stays frozen on the v3.4 curve (PVC0) so #44's V0-scaffold scope is honoured and player pricing does NOT
  feed back through the fit (no circularity; one-iteration drift declared).
- **Injury net of aging** — no new haircut wired (the return-haircut shape is a HYPOTHESIS to re-measure per DECISIONS
  v75 SETTLED #1). Mesh verified instead: the B2 present-unavailability haircut is age-banded BELOW 30 precisely
  because the age curve prices 30+ decline; the recalibration credits proven ELDERS (not the B2 bands' population
  logic) and the credit is gated on current production (`m`, `dur`, `sh`), which an LTI-wiped season already drags —
  overlap measured and reported (Darcy attribution), no second haircut stacked.

## Sizing targets (owner GROUND TRUTH) and the guard fence
Bontempelli ≥ +10% · Gawn clearly above Briggs · Cameron up · Duursma lifted (y1 cohort) · Butters/Holmes HELD ·
faders drop · Darcy up with 3-locus attribution · cohort ratio ≤130% HARD (guide 120-125; baked 125.2%) · B1 PASS ·
monotone pick curve · never-crater (B5 floors ride the lifted V0) · convexity premium holds · panel re-stamped
(CANDIDATE label) · board parity (B4) on the committed candidate · per-lever attribution via kill-switches:
RL_FWDRECAL · RL_YOUNG · RL_OVPX · RL_KPFFIX · RL_V7FORM · RL_W4_RUC (+RL_RUC_YRH) · RL_FORMDECL · RL_PVCFIT.
ALL-OFF ⇒ byte-exact v2.5 (verified).

Redistribution, not injection: net board pool delta reported; FADE/OVPX/KPF-compress fund the credit legs; target
|net| small vs baked.

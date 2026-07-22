# KERNEL-FAMILY λ ROUND — FINDINGS (supervisor item 243) — NOTHING SELECTED, MAP INERT, HALT

One authorized measurement round, same PINNED harness (`rho_kernel_family.py`; frozen `fit_beta`, sample law
`measure.py::measure3` @`2b76d37`). ρ generalised to a per-game recency kernel `K(b)`, `b=years-back=2026−year`:
`ρ_num = Σ games_s·K(b_s)·(avg_s−REPL[pos]) / Σ games_s·K(b_s)` over ALL games>0 seasons (v1.2 was `K=0.5^b`).
Evidence: `KERNEL_FAMILY.txt` / `.out`. Proven-27+ o-sample = 116; RHO_DEN pop per position {MID93 GEN_DEF86 GEN_FWD69 KEY_DEF42 KEY_FWD39 RUC19}.

## HARNESS TRUST — anchors reproduce byte-exact
`geom d=0.50` (the v1.2 law) = **0.8086** (== the prior seg-4 measurement) · `floor6` = **0.9942** (== item-239). The
frozen `fit_beta` + store + o-construction are the pinned ones; the kernel numbers below are trustworthy.

## THE TABLE (λ point·CI·n; both assertions; the two named ρ)
Assertions per candidate — **(A) positive weight for every played game (no exclusion); (B) K(b) strictly
non-increasing in years-back (L-RECENCY)**. Both HELD for ALL 8 candidates (`P R str`; min per-game weight >0
everywhere — even `gauss h=0.8` at b=21 is 5.6e-300, no underflow).

| kernel K(b) | λ | CI | n | asserts | Sam Darcy ρ (ρ_num) | Darcy Moore ρ (ρ_num) | gate |
|---|---|---|---|---|---|---|---|
| geom d=0.10 | 0.9276 | [0.747,1.124] | 107 | P R str | **+3.94** (17.9) | **−2.20** (−21.9) | <0.95 |
| geom d=0.15 | 0.9328 | [0.749,1.142] | 107 | P R str | +3.16 (18.7) | −1.91 (−17.7) | <0.95 |
| geom d=0.20 | 0.8811 | [0.748,1.031] | 108 | P R str | +3.40 (19.2) | −1.75 (−14.3) | <0.95 |
| geom d=0.25 | 0.9225 | [0.782,1.079] | 111 | P R str | +2.94 (19.5) | −1.59 (−11.5) | <0.95 |
| gauss h=0.8 | 0.9326 | [0.774,1.079] | 109 | P R str | +3.84 (20.2) | −2.03 (−17.0) | <0.95 |
| **gauss h=1.0** | **1.0086** | **[0.844,1.219]** | 113 | P R str | +3.66 (21.8) | −2.14 (−12.0) | **≥0.95** |
| gauss h=1.3 | 0.9062 | [0.798,1.034] | 113 | P R str | +3.49 (22.2) | −1.38 (−7.8) | <0.95 |
| soft-shoulder 1.5/0.5 | 0.8078 | [0.728,0.900] | 112 | P R str | +2.52 (21.2) | −0.81 (−3.5) | <0.95 |
| _anchor_ geom d=0.50 (v1.2) | 0.8086 | [0.680,0.968] | 112 | P R str | +2.34 (18.6) | −0.27 (−1.1) | <0.95 |
| _anchor_ floor6 recent-2 (v1.1) | 0.9942 | [0.984,1.000] | 114 | P (excludes <6g) | +3.26 (22.0) | **+0.28** (+2.4) | ≥0.95 |

Sam Darcy (KEY_FWD, REPL 68.4): (2022,4,51.8)(2023,3,19.3)(2024,21,79.0)(2025,17,95.7)(2026,6,81.8).
Darcy Moore (KEY_DEF, REPL 68.4): …(2024,23,74.8)(2025,22,66.7)(**2026,4,33.5**).

## READING THE FINDINGS (for the owner — I select nothing)
1. **Only ONE candidate clears the point gate: `gauss h=1.0`, λ=1.0086 — and NOT robustly.** Its CI [0.844,1.219]
   spans well below 0.95, and its neighbours don't clear (`h=0.8`→0.933, `h=1.3`→0.906); λ(h) is non-monotone
   (0.933 / 1.009 / 0.906), i.e. the point estimate carries ±~0.1 sampling noise. `gauss h=1.0` passing at 1.009 is
   within noise of the ~0.93 cluster. The gate is on the point (`proceed iff λ≥0.95`), which it meets; robustness it
   does not.
2. **The valid-kernel ceiling is ~0.93.** Every candidate that keeps the full weighted history (no exclusion) tops
   out ~0.88–0.93 except the noisy `gauss h=1.0`. None reaches floor6's 0.9942 — because floor6 EXCLUDES sub-6-game
   seasons, and that exclusion is exactly what "weight, don't gate" forbids.
3. **Darcy Moore is the whole tension, on one name.** Under EVERY games×recency kernel his ρ is **NEGATIVE**
   (−0.27 to −2.20) → w=0, priced at identity, NO uplift — because his most-recent 2026 is a **4-game 33.5** (an
   injury/partial season, 34.9 below REPL) and recency-weighting cannot downweight a most-recent season enough
   relative to its recency. Only `floor6` (which EXCLUDES the 4-game season) gives him **+0.28**. So "weight, don't
   gate" prices Moore off his 4-game dip; the gate rule prices him off his last two full seasons. Which is "reality"
   is the owner's ruling — it is the Docherty/interruption question, unavoidable, made concrete.
4. **Sam Darcy is robust across all shapes** (ρ +2.5..+3.9, always positive): a young player with strong recent
   FULL seasons prices up under every kernel — no phantom-rookie risk, real early evidence counted proportionally.
   The kernel choice barely moves him; it moves the injured veteran.

## HALT
Nothing selected. `UNCOMP_S_DEFAULT` stays `None` (map inert; board `8d90c9ac` unchanged). Store `b1fd0bce` /
config `c2d233ae` untouched. The λ gate still HALTS the v1.2 law (0.8086); `gauss h=1.0` is the only point-pass and
it is noise-fragile with a Moore-negative ρ. The owner rules the shape (and whether the ~0.93 valid-kernel ceiling
or a noise-fragile 1.009 is acceptable) at the checkpoint.

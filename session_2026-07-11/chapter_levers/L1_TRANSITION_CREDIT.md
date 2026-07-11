# L1 — YOUNG-GDEF TRANSITION CREDIT · measured result · 2026-07-11
### Data-only lever: `engine/rl_after/ycred_table.json` GEN_DEF rows strengthened by the measured
### transition-expectation gap (new md5 `daaf5e49`; was shipped with the candidate). ENGINE CODE
### UNTOUCHED — the v2.6 L1c formula, w=0.9, φ=(1−g/46)², G0=46, kill-switch RL_YOUNG all unchanged.
### Derivation: `scripts/derive_ycred_gdef_transition.py` (Guard 5 on entry; credit-off matrix
### regenerated on THIS candidate, store 04f38dad asserted). Census: `out/ycred_gdef_transition_census.json`.

## THE MEASURED TRANSITION (T=2026; pool = 387 GDEF ND/RD entrants, classes 2004–2020, fully-observable
## 6-season windows; attrition and busts included)
| quantity | measured |
|---|---|
| P(establish ≥46 games in 6 seasons), picks 1–10 | **0.83** (kernel; raw band 0.88, n=24) |
| P, picks 11–20 / 21–40 / 41–90 | 0.84 / 0.51 / 0.31 (raw bands) |
| median years to establishment | **4.0** → DF = 1.15⁻⁴ = **0.572** (the board's own live lens; NO lens change) |
| washout residual at C+6 | ≈0 (mean 14, median 0; 190/221 exact zero) |
| prize: the board's own established GDEFs (ND, cum g≥46, active, age ≤26), fixed-bw 0.6 log-pick kernel (the A6 convention) + PAVA | pick 2: **3191** · pick 5: 2099 · pick 8: 1718 · pick 21: 1446 (n=30; raw scatter in census — ash 5187@4, campbell 219@5, blakey 3598@10, wilmot 3967@16 …) |
| engine's own year-4 expectation V̄Δ (credit-off path, attrition-inclusive) | pick 2: 1635 · pick 5: 1418 · pick 8: 1386 · pick 21: 931 |
| **credit strengthening** (added to BOTH sat/played rows, trailing tables T=2011–2026) | pick 2: **+0.45** · pick 5: +0.15 · pick 8: **+0.01** · pick 21: +0.14 (R_sat 2026: 0.13→0.58 · 0.13→0.29 · 0.14→0.15 · 0.12→0.25) |

## WHAT THE MEASURED SIZE DOES (L1-only board `9ecbe0fa` vs candidate `8f3675f3`; committed evidence)
| player | old → new | Δ% | transition expectation stated plainly |
|---|---|---|---|
| zeke-uwland (pk 2, 10 g) | 2230 → **2746** | **+23.1%** | 0.83 chance of the pick-2 demonstrated prize 3191 (ash/blakey-anchored), PV 4 yrs @15% ≈ 1515 vs engine's own 4-yr view 935 PV — the gap paid at φ=0.61 |
| dylan-patterson (pk 5, 0 g) | 920 → **992** | +7.8% | 0.83 × prize 2099 PV ≈ 996 — his new price ≈ exactly the genuine-chance PV |
| tobie-travaglia (pk 8, 12 g) | 786 → 792 | **+0.8%** | 0.82 × prize 1718 PV ≈ 806 — his price was ALREADY at the transition PV; the demonstrated outcomes at picks 8–19 on this board split evenly between stars (blakey 3598/wilmot 3967/clark 3307) and value-busts (campbell 219/quaynor 514/jones 96) |
| lachlan-carmichael (pk 21, 0 g) | 634 → 650 | +2.5% | P 0.75 × prize 1446, gap over the engine's 931 — modest |

56 movers, **0 negative**, 47 GEN_DEF + 9 small cross-cell knock-ons (max +6.7% on scrap values) via the
credited-V0 floor basis refit — the D14 by-construction path, not the credit multiplier. **Established
top-end GDEFs byte-identical** (ash 5187, wilmot 3967, blakey 3598, clark 3307, sicily, sinclair,
langdon — named check in the commit); 11 cg≥46 movers exist but are all scrap-valued (≤52 SCAR, max
Δ +2) floor knock-ons.

## HARD-CONSTRAINT EVIDENCE
- Replacement bars: `REPL` untouched (no engine/rl_model edit in this lever — data-only diff).
- Established untouched BY CONSTRUCTION: `_ycred_mult` returns 1.0 at g≥46 (`_merged_recover.py:564`)
  — the strengthened table is unreachable for evidence-complete players; named zero-move check above.
- No blanket young multiplier: only GEN_DEF rows differ (byte-identity ASSERTED over every other
  year×pos×row cell in the derivation script — a moved cell HALTS).
- Leak-free (code-read): table_T pools classes C+6≤T (P, V̄Δ, wash) and C+2≤T (V̄1); prize = as-of-≤T
  matrix values only; T<2011 rows keep shipped values byte-identical; the engine reads table_T at year T.

## HONEST FLAGS (for the owner's ruling eye)
1. **A12 will NOT flip from L1**: the measured transition says travaglia at ~792 is already priced as
   his genuine chance — the pick-8–19 demonstrated outcome distribution is bimodal, and the engine's
   own 4-yr view already matches its mean. The directive expected a flip; the measurement disagrees —
   reported, not forced (same discipline as the L2 null-branch).
2. The pick-1–4 prize rests on ash (5187) + blakey (3598) with campbell (219) the only demonstrated
   top-5 value-bust — n≈3 effective. The credit now claims the OWNER-RULED direction at picks never
   sampled; sensitivity grid (adaptive kernels ≈2100 flat · raw-isotonic 5187 w/ cliff · DF=1
   doubles) committed in the census.
3. uwland +23% stacks on his existing exposure-unlock (+101% low-scorer gain, measurement diagnostic
   B1) — he is now 2746 ≈ 108% of pick-2 currency value. Flagged for the board viewing.

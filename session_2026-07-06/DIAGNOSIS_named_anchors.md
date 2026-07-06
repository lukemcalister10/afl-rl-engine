# Report-Only Diagnosis — Gawn / Cameron / Bontempelli (2026-07-06)

**Scope: REPORT ONLY — no engine logic changed outside the decline curve.** Layer attribution done by
toggling existing layers in a throwaway exec'd copy (v7 age-taper → identity; `RL_RUC_PRIOR_CAP=99`).
Input to the Fable integration design. The decline-curve lever is a **no-op (Δ=0) for all three** —
none reach the shed down-branch (Gawn/Cameron on UP-hold; Bontempelli within the ±3 down-tolerance).

## (a) Are they genuinely low? · (b) What holds them down?

Layer-toggle deltas (value if that layer were removed):

| player | pos | age | Lc | lcr | ev (base) | Δ if v7 off | Δ if RUC-cap off | runway |
|---|---|---|---|---|---|---|---|---|
| Max Gawn | RUC | 35 | 126.5 | +48.0 | 2112 | **+0** | +0 | **4 yrs** |
| Jeremy Cameron | KEY_FWD | 33 | 85.1 | +18.3 | 1143 | **+27** (2.4%) | — | 6 yrs |
| Marcus Bontempelli | MID | 31 | 121.8 | +41.7 | 3084 | **+20** (0.6%) | — | 8 yrs |
| Kieren Briggs (ref) | RUC | 27 | 83.6 | +5.1 | 2153 | +106 | +0 | 12 yrs |

### Gawn — the real cause is RUNWAY, not any single suppressible layer
Gawn 2112 sits just below Briggs 2153 despite **51% more current production** (126.5 vs 83.6). But the
board is expected-FUTURE-value: `proj_from_peak` integrates the forward age curve for **4 seasons** at
age 35 vs **12** for Briggs at 27 (loop breaks at age>38 / `frac<0.42`). Gawn's elite production is
integrated over 3× fewer years. v7 age-taper: **Δ=0** (his value isn't tail-driven). RUC prior cap:
**Δ=0** (doesn't bind — he's demonstrated above start value, byte-exact per the D13 ASK1 scope). RUC
`wage=0` zeros the production-recovery leg for all rucks (neutral Gawn-vs-Briggs). **Conclusion:** the
Gawn<Briggs inversion is the age-runway in the base age curve (`DELTAS`/`frac`, fenced off — it drives
the peak) plus ruck economics. NOT fixable by the decline curve, v7, or the cap. NB: this lever moved
Briggs **+8** (a legit above-replacement dipper, lcr +5.1), slightly WIDENING the gap — Gawn's fix lives
entirely in the ruck job. → **ruck piece.**

### Cameron — KPF + a modest v7 drag
Cameron 1143 (KEY_FWD, 33). v7 age-taper costs him **+27 (2.4%)** — a real but small drag on his q97
upside tail (at 33, `asc=0.40`). The rest is KEY_FWD leverage/distribution and the 6-year runway. Not
genuinely "mispriced" by one layer; a modest v7 drag + KPF economics + runway. → **KPF piece** (+ v7).

### Bontempelli — NOT genuinely under-valued by a fixable layer
Bontempelli 3084 is the **top non-young value on the board**, above every age-peer, and above
production-matched older players. vs younger peers (Daicos 7002 @23, Serong 4170 @25) he is lower purely
because of the **runway discount** (8 forward years vs 16) — correct EFV, not a defect. v7 age-taper
costs him only **+20 (0.6%)**. There is **no clean single layer** whose removal materially lifts him; the
"under-valued" perception is the age-runway in the base age curve, which the fence protects (moving it
moves the peak and every young player).

## HARD FLAG — v7 age-taper as a candidate integration lever (PROPOSED, NOT implemented)

The v7 age-taper `asc=interp(age,[20,22,24,27],[1,.76,.58,.40])` compresses the q97 **upside tail** of
every demonstrated producer toward the median, keyed on **age alone** (flat 0.40 for age≥27). It DOES
suppress still-producing veterans — but **modestly** for the aging-elite (Cameron +27/2.4%,
Bontempelli +20/0.6%, Gawn +0) and **more for still-producing YOUNGER high-ceiling players**
(Serong +111/2.7%, Brayshaw +62, Walsh +49, Daicos +46). So it is a genuine "age-only markdown of
demonstrated upside" — the same class of flaw the decline-shed fix just corrected, one layer up.

**Proposal for the Fable integration (do NOT implement here):** form-condition the v7 tail taper the
same way — let a demonstrated high-level producer (high `lcr`, any age) retain more of his q97 tail,
instead of compressing it by age alone. **Coupling caveat:** v7 is NOT an aging-only lever — it prices
young-player upside too (Daicos/Serong/Sheezel move), so it needs its own scope and its own
verification, and must be measured jointly with the base age curve (runway) since that is the dominant
driver of where Gawn/Cameron/Bontempelli sit. It will not, on its own, put Gawn above Briggs — that is a
runway/ruck-economics question.

## What's left for the coupled pieces
- **Ruck job:** Gawn (runway + wage=0 + ruck pole/cap economics). The aging lever cannot reach him.
- **KPF job:** Cameron (KEY_FWD leverage/distribution + a modest v7 drag).
- **v7 age-taper (new candidate lever):** form-condition the upside-tail compression; coupled to young
  upside + the base runway curve — own scope.
- **Base age curve / runway (`DELTAS`, `proj_from_peak`):** the dominant driver of aging-elite value;
  fenced off (it sets the peak). Any "current-elite-production floor for veterans" would be a deliberate
  EFV-philosophy lever, owner-ruled.

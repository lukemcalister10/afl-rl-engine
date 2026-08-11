# Menu row (SPEC ONLY — NOT BUILT): the ramp de-couple

**Status: specified, not implemented, not measured.** No engine file is touched by this document and
no dial is declared. The owner rules whether it enters the measured set.

---

## The defect it addresses

The A-at-year-1 audit establishes that ITEM A contributes **exactly zero** at a year-1 as-of, because
one six-game threshold is doing **two different jobs at once**:

| job | mechanism | effect at year 1 |
|---|---|---|
| **admission** — may this row use the year-1+ arm at all? | `ns = nseas_pro(p,Y) >= 1`, which counts seasons with `games >= 6·fE` | requires `gy/fE >= 6` |
| **saturation** — how much anchor weight does it carry? | `lam = interp(min(gy/fE,6), [0..6], LAM_SIT)`, `LAM_SIT[6] = 1.0` | `gy/fE >= 6` ⟹ `lam = 1` ⟹ share **0** |

Both are keyed to the **same within-season games count**, so at year 1 they are mutually exclusive by
construction: qualifying to use A is the same act as saturating A to zero.

## The change

**Keep the six-game admission bar exactly as it is.** De-couple only the *saturation*: let the blend's
production weight saturate on **career** games (≈15-20) rather than on the six-game within-season bar.

```
admission   :  unchanged — ns >= 1 still requires a qualifying season   (NOT touched)
saturation  :  lam = interp(min(career_games / G_SAT, 1) * 6, [0..6], LAM_SIT)   with G_SAT ≈ 15-20
```

A qualified year-1 row with, say, 12 career games would then sit part-way up the ramp instead of
pinned at the top, so it carries **real anchor weight** and A lives at year 1 as ruled.

## Mechanism sites

| site | file:line | change |
|---|---|---|
| the ramp itself | `_merged_recover.py` `_a_share` (~:2013) | `lam` reads career games against `G_SAT`, not `gy/fE` against 6 |
| admission gate | `ev()` `if ns==0:` (~:2192) | **unchanged** |
| `sitout_ev`'s own `lam` (~:1945) | **unchanged** | the sit-out arm keeps its within-season ramp; only A's copy de-couples |
| new dial | `RL_A_GSAT` (default `0` = off ⟹ byte-exact) | must be declared in the manifest |

**The sit-out arm must not be changed with it.** `sitout_ev` uses the same `LAM_SIT` ramp for a
different purpose (games-at-pace within the season). Re-pointing both from one edit would move the
whole sit-out population as a side effect — that is the "one ramp, two consumers" trap, and the spec
deliberately touches only A's copy.

## PRE-REGISTERED: measure ONLY in combination with a one-way form

**This must not be measured with the symmetric blend.** Opening the anchor at year 1 with **two-way**
borrowing would let the anchor drag **hot** year-1 rows *down*, and year 1 is already the year the
package cut hardest (main 1.1239 → FULL 0.9974). **The expected result of de-couple + symmetric blend
is a DEEPER year-1 dip, not a repair** — registering that in advance so it cannot later be reported as
a surprise.

Admissible combinations:

- **de-couple + A-FLOOR** — anchor supports cold year-1 rows, never drags hot ones. Expected: year-1
  book **rises**; hot rows untouched.
- **de-couple + A-DRAGFADE** — drag permitted but faded by proof. Expected: **between** FULL and
  de-couple+floor.

## Expected direction, and the checks that must run with it

- **Year 1 rises**, by construction — this is the first candidate that can move year 1 through the A
  site at all. Every other A/C-site candidate measured so far moves it by exactly 0.
- **Year 4 largely unaffected** — at year 4 most rows are far past any 15-20 career-game saturation,
  so the ramp change is inert there. *That expectation must be stated as falsifiable and checked, not
  assumed — it is the same shape of claim that the H ladder's pre-registration got wrong.*
- **The no-arb margin must be printed.** Raising year 1 raises yr0→yr1 appreciation against a flat
  14% charge. FULL sits at −0.26%; a lift past ~+14% opens an arbitrage, which is where V3 (−4.56%)
  and V4 (−2.82%) already sit. A year-1 repair that lands the book in free money has traded one
  breach for another, and the table must show it.
- **Conservation.** A net year-1 lift is a net book lift the re-teach must absorb; its size gets
  printed, not asserted to be small.

## Honest caveat on scope

Even if this works exactly as specified, it repairs **A's** year-1 silence. It does **not** address
where the year-1 value actually went: the decomposition attributes **80.5%** of the year-1 drop to
**#336** and **10.8%** to the **surprise law**, against **0.0%** for ITEM A. This row makes A deliver
its ruled purpose; it is **not** a counterbalance to the measured drop, and should not be sold as one.

**Cost if ruled in:** 2 emits (~2.5 min each) for the two admissible combinations, plus one identity
proof at `RL_A_GSAT=0`.

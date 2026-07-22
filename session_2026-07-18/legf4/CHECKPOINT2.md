# LEG F4 — CHECKPOINT 2 (the honest rate measured + sealed; ±5% UNREACHABLE on −2→−1 — the owner's tension) · seat 13 · 2026-07-19
**Per MEMO_LEGF v1.2 §2.vii point 5 and the directive's HALT law: the honestly-measured realized rate CURES
the diagnosed L-SYMMETRY asymmetry and passes −1→now, but CANNOT bring −2→−1 inside ±5%. I did NOT bend the
rate to force it (forbidden — that would inflate forward to ~flat against real aging). No engine edit. This is
the HALT-AND-RETURN; the ±5% expectation itself now goes to the OWNER.**

## WHAT WAS MEASURED + SEALED (pre-render, never iterated against the backtest — v1.2 §2.vii pt 1-2)
`sealed_rate.json` — `r_real(a)` = value-weighted realized backward-transition rate per age-transition,
pooled over the committed −2/−1/now boards (F2 stamped artifacts), den-weighted 3pt MA + PAVA non-increasing
on a≥24 (rule 7). **SEALED sha256_8 `ef1970db`.** Content is ONLY the measured rate (Reid):
`{18:1.060, 20:1.041, 22:1.008, 24-36:0.869, 38:0.713}` — young ages realize GROWTH, peak-decline ages
~−13%. The honest per-player realized aging rate.

## THE ACCEPTANCE (sealed rate applied to the committed boards — this IS the backtest: backtest.py applies
## r(age) directly, and the §2.vii damper makes the board's r(age) ≈ r_real by construction)
| projection | board | pred | actual | error | ±5% band | verdict |
|---|--:|--:|--:|--:|---|---|
| −1 → now | 771,152 | **718,768** | 752,427 | **−4.5%** | [714,806 , 790,048] | **IN** |
| −2 → −1 | 770,987 | **714,210** | 771,152 | **−7.4%** | [732,594 , 809,710] | **OUT** |

Pre-F4 (F3 board, forward −19.6%): −1→now 558,568 (−25.8% OUT) / −2→−1 554,439 (−28.1% OUT). The honest rate
is a MASSIVE, correct improvement (+160k on −1→now) that lands −1→now IN and halves the −2→−1 miss — **but
−2→−1 stays OUT by 2.4pt.**

## WHY ±5% IS UNREACHABLE ON −2→−1 BY ANY HONEST PER-PLAYER RATE (the structural tension)
The committed boards conserve their TOTAL across years (−2 770,987 → −1 771,152 = +0.0%; −1 → now −2.4%)
**only through ENTRANT/EXIT COMPOSITION**, which the per-player roster-projection backtest structurally omits:
- −2→−1: the −2 roster's matched survivors realize **−6.2%** (value-weighted); 122 players (val 27,441) EXIT;
  the −1 board's total is held flat by NEW entrants NOT in the −2 roster. Projecting the −2 roster forward
  (no entrants, exits kept alive) at ANY honest rate ≤ the survivor rate lands ~714k — the missing ~24k is
  entrant value the backtest cannot see.
- −1→now: the same gap is smaller (89 exits, 18,928; entrants ≈ 72k), so −1→now lands IN at −4.5%.
- To hit −2→−1's target (≈0% / flat) a forward rate would have to keep declining veterans AND to-exit
  players at ~full value — i.e., ABANDON real aging. That is the bend the CHECKPOINT LAW forbids.

**No honest L-symmetric forward rate satisfies BOTH backtests. The −9% composition-controlled reading fails
even worse (both OUT). The board-to-board per-age rate (sealed) is the most favorable honest reading and it
still misses −2→−1.** The residual is a property of the ACCEPTANCE's construction (per-player projection of a
churning roster vs a composition-conserved total), not of the calibration.

## WHAT I DID NOT DO (deliberately — CHECKPOINT LAW)
No engine edit (the two granted `_merged_recover.py` sites are UNTOUCHED — building the damper to the sealed
rate would reproduce the table above, −2→−1 OUT, so I did not ship a fix that fails acceptance nor tune the
rate to pass). No k=0 movement. Store/curve/rl_model/v_at_peak/docs/ui untouched. F3's cures intact.

## THE RETURN — FOR THE OWNER (only he can re-rule ±5%; v1.2 §2.vii pt 5)
The diagnosis and the L-symmetry cure are correct and in hand (sealed `ef1970db`). The blocker is the ±5%
expectation on −2→−1. Options for the owner's ruling (I implement immediately on his word):
- **(A)** Re-rule the backtest to be COMPOSITION-CONTROLLED (credit the F1 phantom-intake / entrant layer into
  the projected total, or match on the same roster) — then the honest rate is assessed on a like-for-like
  total and both land inside ±5%. Most defensible; the entrant value already exists (F1 phantom layer).
- **(B)** Accept the honest sealed rate as F4's landing (−1→now IN, −2→−1 −7.4%) — the best law-compliant
  result; re-scope the residual 2.4pt (pure composition) out of the per-player acceptance.
- **(C)** Re-rule the ±5% bar itself for the −2→−1 leg.
I HALT here rather than bend. Awaiting the owner's ±5% re-ruling.

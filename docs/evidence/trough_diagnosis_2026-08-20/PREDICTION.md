# PREDICTION, WRITTEN BEFORE THE CONFIRMING SWEEP (step 3 of the method)

Source of the prediction: the BAND MODEL ALONE.
`predicted(score) = price6(p_at_SHIPPED_scoring, cond_prior_band(feature vector with index 9 = L(score)), 2026)`
— the player's own scoring row is restored to the shipped state before `price6` is called, so every
continuous input of `v_at_peak` (his `level_now`, age, position, pick) is FROZEN. The ONLY thing that
moves is the conditional-prior band `cm` reads off the level feature. No `ev()` call is involved.

Ranking produced by `tasks/task_03_predict.out` over all 86 rows (5–13 games in 2026 AND played round 23).
Kondogiannis ranks #2 of 86 (44.5 % predicted drop) and Dolan #8 (34.8 %) — both anchored rows land in the
top 8 by the band-only predictor, which is the first confirmation.

## THE PREDICTIONS (third players, chosen by rank, no true sweep seen)

| # | player | g | prior avg | band-only predicted | PREDICTION for the TRUE ev() sweep |
|---|---|---|---|---|---|
| 1 | Billy Cootee | 8 | 47.71 | −52.2 % from score 7 → 15 | true price at 15 is ≥ 25 % BELOW the price at 7 |
| 2 | Charlie West | 7 | 32.33 | −38.0 % from score 59 → 110 | true price at 110 is ≥ 20 % BELOW the price at 59 |
| 3 | Will Hayes | 8 | 36.97 | −43.0 % from score 0 → 35 | true price at 35 is ≥ 20 % BELOW the price at 0 |

## NEGATIVE CONTROLS (predicted band-only drop < 1.5 %)

| player | g | band-only predicted | PREDICTION |
|---|---|---|---|
| Marcus Herbert | 9 | 0.7 % | true sweep max drop < 6 % |
| Mark Keane | 8 | 0.8 % | true sweep max drop < 6 % |
| Sam Lalor | 12 | 1.1 % | true sweep max drop < 6 % |
| Will Day | 10 | 1.0 % | true sweep max drop < 6 % |

If the true sweeps land inside these bounds, the band model is the mechanism site and nothing else needs
to be invoked to explain the trough.

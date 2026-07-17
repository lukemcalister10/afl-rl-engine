# RIDER (ii) — cohort-bootstrap tail influence + short-draft-era caveat
**REPORT-ONLY · finding, not a verdict · gross · busts full weight · no decile bands.**  
`stamps: code_sha=e4177c21934148c19d9cec3c015fee5d28480102 curve_payload=89c14729 store_base=968de0c7 per_entrant=40d7da7c (frozen @ e4177c2; read-only; asserted at load)`

**Declared:** resampling unit = **cohort (draft year)**, not the row — rows within a draft year are correlated, so the cohort is the bootstrap unit. B=4000 (seed 20260718). Realized = `mean(vpath)` on career-complete cohorts (≤2017). Two estimators are reported per exact pick: the **RAW per-exact-pick mean** (no cross-pick borrowing — the finest resolution, where tail fragility is honestly visible) and, as a **contrast**, the fixed-bandwidth **smoothed** kernel (whose tail stability is *borrowed* from neighbours and the pick-99+ sink). Pick 99 = deep sink (raw n≈250), excluded from tail medians. Single-cohort/player swings are exact LOO on the raw mean.

**Headline (the item-325 point):** at the RAW per-exact-pick resolution the deep tail is **far less stable** than the top — median cohort-bootstrap relative SD **34.1% (p50–98)** vs **17.4% (p≤30)**. The smoother *masks* this: its tail rel-SD collapses to **7.4%** only by borrowing across picks/the sink (top 8.2%). A single player can swing an individual deep-tail pick by up to **73%** (worst: **Jake Lloyd at pick 87, 73.1%**).

## Tail influence by exact pick (p50+)
| pick | resid0 % | RAW boot rel-SD % | SMOOTHED boot rel-SD % | 1-cohort swing % (which) | 1-player swing % (who) | #cohorts | raw n |
|---|---|---|---|---|---|---|---|
| 50 | -2.0 | 35.3 | 5.8 | 33.7 (2003) | 33.7 (Sam Fisher) | 14 | 14 |
| 55 | -7.6 | 39.6 | 7.2 | 26.4 (2015) | 26.4 (Jordan Dawson) | 14 | 14 |
| 60 | -14.2 | 48.1 | 7.7 | 49.2 (2014) | 49.2 (Harris Andrews) | 15 | 15 |
| 65 | -18.3 | 39.9 | 8.3 | 31.4 (2016) | 31.4 (Luke Ryan) | 15 | 15 |
| 70 | -20.2 | 43.4 | 8.8 | 42.7 (2006) | 42.7 (Justin Westhoff) | 14 | 14 |
| 75 | -21.3 | 34.6 | 8.4 | 25.9 (2014) | 25.9 (Jeremy Finlayson) | 14 | 14 |
| 80 | -22.7 | 39.1 | 7.4 | 29.2 (2004) | 29.2 (Danyle Pearce) | 14 | 14 |
| 85 | -25.6 | 48.5 | 6.6 | 47.6 (2016) | 47.6 (Rowan Marshall) | 13 | 13 |
| 90 | -28.8 | 33.6 | 6.1 | 25.4 (2016) | 25.4 (Jack Henry) | 11 | 11 |
| 95 | -31.2 | 44.1 | 5.7 | 35.0 (2004) | 35.0 (Scott McMahon) | 11 | 11 |
| 99 *(sink)* | -32.0 | 8.2 | 5.5 | 3.8 (2011) | 3.9 (Rory Laird) | 14 | 250 |

_Full 1–99 series in `rider_ii_bootstrap.json`; curve in `rider_ii_bootstrap.svg`._

**Short-draft-era caveat (declared):** the deep-tail per-exact-pick sample is thin (raw n≈11–15 per pick for picks ~70–98) drawn from only 15 complete cohorts, and the smoothed deep-tail realized leans on the pick-99+ sink. Recent cohorts (>2017) are right-censored and **excluded** from this realized bootstrap — the tail here rests on the older, career-complete drafts only, so its coverage genuinely thins with depth.

## Finding (one plain sentence, no verdict)
At its own (per-exact-pick) resolution the deep tail is markedly less stable than the top under cohort resampling (median bootstrap relative SD ~34% vs ~17%) and a single player or cohort can move an individual deep-tail pick by up to ~73%; the smoothed curve looks steadier there only because it borrows across picks and from the pick-99+ sink, so deep-tail values are neighbourhood/sink averages, not pick-specific estimates.

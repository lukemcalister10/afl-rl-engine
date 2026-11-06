# Survival on the +1/+2 lenses (capped H2, fix plan F1) — engine act, landed 2026-11-06

Owner words (verbatim, in chat): 2026-10-14 "H2 makes the most sense"; on the capped variant "the capped option
seems to keep the board stable, so that's probably the best option?"; the F1 fix plan after the first blind
review was accepted without objection; landing word 2026-11-06 "Yes, please proceed with that plan."

## The rule
S_k(age, career games) = P(on an AFL list at the END of season Y+k | listed at the end of base season Y), fitted
by additive logit on the store's own history (base seasons 2010–2024 for k=1, 2010–2023 for k=2; the listing
fact `_last_listed` from the AFL 2024/2025 lists, else active today, else the last played season as a documented
proxy). Within each age cohort (integer ages; 33+ pooled; cohorts under 5 charged rows merge downward) a charged
row's multiplier is m_i = min(1, S_k(age_i, g_i) / Σ_j w_j S_k(age_i, g_j)), w = the cohort's vP weights —
evidence-only, referenced at the row's own age, capped at 1.0 (nobody rises). Never-played rows are not
charged and not in the reference (their pick price already averages over busts) and carry no published S.
Present value v, the −1/−2 columns, retired rows and phantom picks are untouched by construction.

## Reviews
Blind review 1 (2026-10-14): FAIL — the fit measured "played again", and never-played rows were charged twice.
Fixed by F1 (refit on the listing outcome; 0-game rows out of the charge). Blind review 2: PASS WITH NOTES —
played-row fit and the evidence-only pooled reference, both applied (commit c30acb85 on the act branch).

## Measured (confirming build 96896e1c on store f49dbef6; engine == offline on 804/804 rows)
| | +1 lens | +2 lens | reconciled +1 | reconciled +2 |
|---|---|---|---|---|
| before (e944be20) | 635,134 | 593,206 | +0.58% | +2.72% |
| after (96896e1c) | 627,218 (−1.25%) | 578,436 (−2.49%) | −0.57% | +0.57% |

Present movers 0; +1 322 rows move, +2 323, all down. By evidence at +2: 1–5 games −17.2%, 6–20 −9.1%,
21–50 −4.6%, 51–100 −2.0%, 101+ 0, never-played 0. By age at +2: 18–28 between −1.6% and −4.0%, 29–30 −1.1%,
31–33 −0.1%, 34+ 0 (the only charged veteran is Darcy Fort, 33, 83 games). Biggest at +2: Xerri −681, M. Hall
−437, McCarthy −429, McAndrew −414, Sweet −366, Moyle −349, Herbert −314. Full tables: MEASURED_TABLES_F1.txt.

## Disclosed
Within ages 26–32 the capped rule adds a within-cohort thin-evidence charge on top of r_pop's age-level exit
risk: 1.27% of that band's vP1 and 2.76% of its vP2 (the §2.ix caveat in _merged_recover.py). The age damper is
inert from 34, so veterans carry no exit probability on the lenses — an open item for the damper itself (F3).

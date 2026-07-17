# CLEAN-ROOM GPT — §5 PRINCIPAL FAILURE MODES (verbatim, owner-couriered)
### PROVENANCE: the external clean-room exercise of register item 324 (GPT seeded with data+goal
### only, no engine spec). This §5 self-critique lived in seat-12's chat and was NOT in the repo
### (verified turn-8/9); Luke couriered it 2026-07-18 (item 337). FILED VERBATIM below the rule.
### USE: cold-audit seeding material — CONVERT each mode to a code/artifact ADDRESS the auditor
### computes-and-reports (never seed as a conclusion). The map to our existing instruments is in
### AUDIT_SEED_SHELL SHARD E. This is an external neutral-language input; it carries none of our
### vocabulary, so it is clean seed by construction (the 319/323 leak-guard still runs at seeding).

## 5. Principal failure modes
5.1 Circular player valuations
If the established player-valuation system uses draft pick as an input, early-career `value_asof` may mechanically reproduce draft order.
Detection: inspect the valuation model and compare the pick relationship in career year one with later career years after controlling for games and position.
Response: use a draft-pedigree-free valuation series for this exercise, or place greater weight on later seasons.

5.2 Treating stock values as yearly payoffs
Adding `value_asof` across seasons creates value-years and double-counts the same player asset.
Detection: dimensional audit and extreme dependence on career length.
Response: use a normalised weighted average or an explicitly defined flow measure.

5.3 Right-censoring mistaken for failure
Recent entrants naturally have short histories.
Detection: outcome declines mechanically for newer entry years.
Response: mature-cohort primary fit or a formally specified survival/imputation model.

5.4 Non-random late-draft observations
Picks 70–80 occur only in drafts that ran sufficiently deep. Those drafts may have unusual talent pools, list rules or club demand.
Detection: compare the tail between long- and short-draft eras and include draft length as a cohort diagnostic.
Response: stronger pooling, wider uncertainty intervals and cautious use of RD continuation data.

5.5 Superstar leverage
A small number of exceptional players legitimately influence expected value, especially late in the draft.
Detection: cohort bootstrap, top-one-percent influence runs and leave-one-player-out diagnostics.
Response: retain genuine upside but report uncertainty. Do not replace the mean with the median without changing the stated valuation objective.

5.6 Era and rules changes
Academy bidding, concessions, list-size changes, COVID disruption and recruitment improvements can alter the meaning of a nominal pick.
Detection: cohort residuals, temporal holdouts and rule-era interactions.
Response: recency weighting only if it demonstrably improves held-out calibration; never apply it merely because newer data feels more relevant.

5.7 Position composition mistaken for causal value
Midfielders may appear more valuable partly because the best midfielders are selected earlier.
Detection: compare generic, position-standardised and within-region estimates.
Response: keep the generic pick curve marginal and publish position pathways separately.

5.8 False precision
A smooth table can hide very wide uncertainty, particularly after pick 60.
Detection: cluster-bootstrap intervals and effective sample sizes.
Response: publish intervals or uncertainty grades alongside point values.

5.9 Data coding defects
The supplied file contains several points requiring clarification:
- entry years 2003 and 2026 appear despite the stated 2004–2025 range;
- 18 missing `value_asof` observations belong to 2026 MSD entries;
- all entrants with at least three non-missing `games` observations have non-decreasing games totals, indicating that `games` is cumulative rather than games played in that season;
- all MSD entries have pick 90, which appears to be a pathway placeholder rather than a genuine selection number.
These do not affect the mature national-draft prototype, but they must be resolved before games or MSD pick numbers are used in validation.

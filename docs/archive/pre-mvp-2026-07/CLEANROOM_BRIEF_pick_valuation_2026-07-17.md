# BRIEF — DESIGN A DRAFT-PICK VALUATION METHOD (independent proposal)
You are designing from scratch. You have not seen any existing method and should not assume one.

## The goal
Propose a principled, defensible method to value every AFL draft pick (picks 1 through 80) as an
asset to the club that HOLDS the pick — in one currency, where **pick 1 is defined as 3,000**.
The intent, in the owner's words: *"reasonably and correctly value each pick and pathway to reflect
their value to a holder of that pick."* Your pick values must be consistent with the player values
in the attached data — a pick's worth comes from the players it turns into.

## League context (all you need)
- The AFL national draft runs yearly; clubs pick in order; a pick entitles the club to one player of
  its choice at that slot. Picks are freely tradeable, including NEXT YEAR'S picks (so a method for
  discounting future-year picks is worth a note, though the core job is this year's 1–80).
- Players also enter WITHOUT a national-draft pick: the rookie draft (RD, with its own pick numbers
  continuing after the national draft), and pickless mechanisms (mid-season draft, pre-season
  supplemental, international signings, academies). The data labels every entry mechanism.
- Positions differ in volume and value shape: many midfielders (MID) are drafted, fewer key-position
  forwards/defenders (KFWD/KDEF), general forwards/defenders (GEN_FWD/GDEF), and few ruckmen (RUC).
  Careers differ by position (rucks develop late, for example).
- Many drafted players never establish careers — early exits are common, and commoner at later
  picks. Any honest pick value must reflect that.

## The data (afl_draft_trajectories.csv)
One row per player per season, entry years 2004–2025 (2,649 players, 13,628 player-seasons):
- `player` · `entry_year` · `entry_mechanism` (ND national draft / RD rookie draft / pickless codes)
- `pick` — the player's draft pick number (empty for pickless entries)
- `position` — drafted position
- `season_year`, `career_year` (1 = first season after entry)
- `value_asof` — the player's valuation at the END of that season, in the target currency (the same
  scale your pick values must land on; this is the established player-valuation system, taken as given)
- `games` — AFL games played that season
- `delisted`, `last_game_year` — exit markers. A player who washes out simply stops having rows.
Recent entrants have short histories by construction (a 2024 draftee has one or two rows). Values
for the most recent seasons are provisional but fine for method design.

## What to deliver
1. **Your method**, stated precisely: how you get from this data to a value for each pick 1–80.
   State your estimator, any weighting, how positions and early exits enter, and how you handle
   picks/regions where data is thin.
2. **Your assumptions**, listed, each with why it is safe or how you would test it.
3. **A worked shape**: roughly what your curve would look like (you may compute from the CSV if you
   can; otherwise describe the expected shape and what would surprise you).
4. **Validation**: how you would PROVE your curve is right — what checks, against what, with what
   tolerance, and what failure would send you back to the drawing board.
5. **Failure modes**: the top ways your own method could silently mislead, and how you'd detect each.
6. **Data you wish you had**: anything missing from the CSV that would materially improve the method.

## Ground rules
- Design for the stated intent only. Do not price off market sentiment or trade folklore — the data
  is the authority.
- Be concrete: formulas or procedures, not vibes. If you'd fit something, say what and how.
- If parts of the problem are genuinely underdetermined by this data, say so plainly.

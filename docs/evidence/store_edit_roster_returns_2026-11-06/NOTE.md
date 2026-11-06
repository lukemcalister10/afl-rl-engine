# Roster returns — store-edit act, 2026-11-06

Owner words (verbatim): "Un-retire Bedendo agree."; "Roarty, Purcell, and Mirkov should be added to the store as free agents
attached to those clubs. Roarty Key defender, Purcell General Defender, Mirkov ruckman."; "Purcell April 26, 2005.
Unregistered selection this year. Roarty January 4, 2006. Ireland selection this year."; "Please proceed."
Source: the AFL's list changes ahead of 2027 (docs/inputs/afl_list_changes/2026.csv: Bedendo delisted free agent to
Fremantle; Mirkov "committed to signing" at GWS; Roarty category B at Collingwood; Purcell category B at Hawthorn).

## The edits
- dominic-bedendo (retired 2024, 2 games in 2022): `_retired` true→false, `_last_listed` 2024→2026; adds `afl_club`
  Fremantle, `stable_player_id`, `affl_team` Free Agents, `eligibilities`, and a 2026 season {0 games} — the shape
  every active row carries. alex-mirkov (retired 2024, no games): the same, to GWS, RUCK.
- Two new rows via the lane's `add_row` verb (2026-11-06): finnbarr-roarty (IRE, Post-Draft - Ireland, b. 2006-01-04,
  KPD, Collingwood) and ollie-purcell (UNR, Post-Draft - Unregistered, b. 2005-04-26, SD, Hawthorn), in the shape of
  the 2025 IRE/UNR entrants (pickless, force-active, stream OTHER).
The locations sheet and the positioning register carry all four (Roarty and Purcell are added to the sheet AFTER this
act lands: the inputs check joins every sheet name to a store row, which these two do not have until the act).

## Movers
Four rows appear on the active board at their entry prices (Bedendo and Mirkov move from the dormant back section);
nothing else moves. The dry run is the prediction of record.

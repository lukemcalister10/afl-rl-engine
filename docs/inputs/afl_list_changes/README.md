# AFL end-of-season list changes (owner-couriered, 2026-10-14)

Source: the AFL's "Retirements and delistings" pages for 2025 and 2024
(https://www.afl.com.au/news/retirements-and-delistings/2025, …/2024), transcribed verbatim on 2026-10-14 on the
owner's instruction. Categories as the page states them: `ret` retired, `del` delisted, `trd` traded, `FA` free
agent, `DFA` delisted free agent. Tarryn Thomas (North Melbourne) carried no category on the 2024 page. Owner's word (2026-10-14): he was cut at the
END OF 2023, so he is no 2024 exit; his row carries `cut_2023` (ignored by the matcher) and `_last_listed = 2023`
is set from the override below.

Overrides (owner word, applied by the matcher ahead of the pages): `tarryn-thomas` last listed 2023.

Owner rule (2026-10-14): only `ret` and `del` are list exits. An exit at the end of Y is void if the player
re-appears later (plays or is listed in a later season, or appears on a later year's list), except that a
delisting at the end of 2024 followed by a re-appearance only in 2026 would still stand (no such case is known).
The valid exits set `_last_listed = Y` on the player's store row; this is the listing fact the as-at boards read.


## 2026 (ahead of 2027)
`2026.csv` is the AFL's "Ins and outs: every club's full list changes ahead of 2027" page
(https://www.afl.com.au/news/1628837/…), transcribed verbatim 2026-11-06 with columns club, direction (IN/OUT), name,
detail as the page states it. Exits are OUT rows whose detail is `retired` or starts with `delisted`; a player
"committed to re-drafting" is an exit only if he is not re-listed. Cross-referenced against the owner's
docs/inputs/AFFL_Player_Locations.csv (upload baf6ad5e) — see the chat record of 2026-11-06.

## Owner rulings on the 2026-11-06 upload (locations sheet baf6ad5e, picks workbook)
- Jayden Nguyen = Essendon, Oliver Hannaford = GWS, Brandon Zerk-Thatcher = Port Adelaide ("should always have been":
  store errors; the sheet is right). Bailey Laurie = Melbourne (sheet blank corrected on the owner's word).
- Dominic Bedendo: un-retire (AFL page: delisted free agent to Fremantle; the sheet's WB corrected to FRE).
- Finnbarr Roarty (key defender, Collingwood), Ollie Purcell (general defender, Hawthorn), Alex Mirkov (ruck, GWS):
  added to the sheet as Free agents attached to those AFL clubs; Mirkov is an un-retire (store row alex-mirkov),
  the other two are new store rows.
- Real-life delistings/retirements (blank AFL club on the sheet, 108 players): retired in the store with
  `_last_listed = 2026`; AFFL-owned ones keep their AFFL team.
- Draft pick discount (owner rule): current-year picks 1.0×, next year 0.9×, two years out 0.8× of raw pick value
  in the workbook's "Value (counted)" column (2026 3000 / 2027 2700 / 2028 2400 for pick 1). At the yearly rollover
  each class shifts up one step (2027 → 1.0×, 2028 → 0.9×); 2029 picks are issued in September, so there is a
  three-month window with three classes active. The +2 LENS is not discounted: it is the projected state two years
  on, when those picks are the players taken with them; the workbook values a pick as an asset that cannot be used
  for two years.

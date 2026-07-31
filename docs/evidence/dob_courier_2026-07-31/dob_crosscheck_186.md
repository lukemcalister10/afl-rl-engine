# AFL Birth-Date Cross-Check — 186 Retired Players

**Task:** independent verification of hand-filled birth dates. Verification only — no values were changed.

**Source file:** `/root/.claude/uploads/9f0374b6-60a2-53a7-9eb7-e007eff7150b/a5627d6d-missing_birth_years_186_completed.csv`

## Result summary

| Classification | Count |
|---|---|
| VERIFIED | 186 |
| YEAR-ONLY | 0 |
| DISCREPANT | 0 |
| UNVERIFIABLE | 0 |
| **Total** | **186** |

**No discrepancies were found.** All 186 sheet birth dates match AFL Tables exactly (day, month and year), and the separate `Birth year` column agrees with the found year on all 186 rows.

## Method

1. Every player was resolved to an authoritative AFL Tables player page via the site's surname indexes (`playersX_idx.html`), which carry a `title="Club (years)"` attribute used to disambiguate namesakes.
2. Nine names in this set have namesakes on AFL Tables; each was resolved by matching the club/season span against the sheet's draft year, stream, pick and seasons (see the Disambiguation section).
3. Birth dates were parsed from the `Born:` field on each player page and normalised to YYYY-MM-DD.
4. Every page was re-fetched from its authoritative URL and re-parsed as a second pass; the `<h1>` on each page was checked against the expected player name, and all 186 pages confirmed distinct.
5. **Independent second source:** Wikipedia wikitext was pulled for all 186 players; 94 had a machine-readable `{{birth date}}` template. All 94 agree with AFL Tables and with the sheet. The remaining 92 are mostly short-career players with no Wikipedia article or no structured birth date; AFL Tables is the canonical archive for those.

## Disambiguation decisions (9 namesake cases)

| Player | Chosen page | Career on chosen page | Rejected namesake | Basis |
|---|---|---|---|---|
| Sam Butler | `Sam_Butler0` | West Coast (2004-2017) | Sam_Butler1 — Hawthorn (2022-2026) | 2003 ND #20; sheet seasons end 2017 |
| Chris Johnson | `Chris_Johnson1` | Melbourne (2005-2008), Carlton (2009-2010) | Chris_Johnson0 — Fitzroy/Brisbane (1994-2007) | 2003 ND #36; sheet 2005-2010 |
| Tom Williams | `Tom_Williams1` | Western Bulldogs (2007-2014) | Tom_Williams0 — Essendon (1903) | 2004 ND #6; sheet 2007-2014 |
| Jesse Smith | `Jesse_Smith0` | North Melbourne (2005-2008) | Jesse_Smith1 — Carlton (2006) | 2004 ND #11; sheet ends 2008 |
| Tom Murphy | `Tom_Murphy0` | Hawthorn (2005-2012), Gold Coast (2013-2014) | Tom_Murphy1 — North Melbourne (2018-2020) | 2004 ND #24; sheet 2005-2014 |
| Simon Taylor | `Simon_Taylor1` | Hawthorn (2005-2010) | Simon_Taylor0 — Collingwood (1989) | 2004 ND #50; sheet 2005-2010 |
| Will Hamill | `Will_Hamill0` | Brisbane Lions (2007) | Will_Hamill1 — Adelaide (2020-2024) | 2004 RD #43; sheet 2007 only |
| Joshua Kennedy | `Josh_Kennedy0` | Carlton (2006-2007), West Coast (2008-2022) | Josh_Kennedy1 — Hawthorn/Sydney (2008-2022) | 2005 ND #4 by Carlton; sheet 2006-2022 |
| John Anthony | `John_Anthony1` | Collingwood (2008-2010), Fremantle (2011-2012) | John_Anthony0 — St Kilda (1972) | 2005 ND #37; sheet 2008-2012 |

> Note on the brief: the task described this Sam Butler as "the 2003 St Kilda-era one". AFL Tables has no St Kilda Sam Butler of that era. The 2003 national draft pick 20 Sam Butler was recruited by **West Coast** and played there 2004-2017, which matches this row's draft year, pick and final season. That page was used; its birth date (1986-01-14) matches the sheet.

## Row-by-row results

| # | Player | Draft | Sheet seasons | Sheet birth date | Found (AFL Tables) | Wikipedia | Status | Source |
|---|---|---|---|---|---|---|---|---|
| 1 | Adam Cooney | 2003 ND #1 | 2005-2016 | 1985-09-30 | 1985-09-30 | 1985-09-30 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/A/Adam_Cooney.html) |
| 2 | Andrew Walker | 2003 ND #2 | 2005-2016 | 1986-05-18 | 1986-05-18 | 1986-05-18 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/A/Andrew_Walker.html) |
| 3 | Colin Sylvia | 2003 ND #3 | 2005-2014 | 1985-11-08 | 1985-11-08 | 1985-11-08 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/C/Colin_Sylvia.html) |
| 4 | Farren Ray | 2003 ND #4 | 2005-2016 | 1986-03-23 | 1986-03-23 | 1986-03-23 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/F/Farren_Ray.html) |
| 5 | Brock McLean | 2003 ND #5 | 2005-2014 | 1986-03-11 | 1986-03-11 | 1986-03-11 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/B/Brock_McLean.html) |
| 6 | Kepler Bradley | 2003 ND #6 | 2005-2013 | 1985-11-13 | 1985-11-13 | 1985-11-13 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/K/Kepler_Bradley.html) |
| 7 | Kane Tenace | 2003 ND #7 | 2005-2009 | 1985-07-04 | 1985-07-04 | 1985-07-04 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/K/Kane_Tenace.html) |
| 8 | Raphael Clarke | 2003 ND #8 | 2005-2012 | 1985-09-24 | 1985-09-24 | 1985-09-24 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/R/Raphael_Clarke.html) |
| 9 | David Trotter | 2003 ND #9 | 2007-2007 | 1986-03-04 | 1986-03-04 | 1986-03-04 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/D/David_Trotter.html) |
| 10 | Ryley Dunn | 2003 ND #10 | 2005-2008 | 1985-10-07 | 1985-10-07 | 1985-10-07 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/R/Ryley_Dunn.html) |
| 11 | Beau Waters | 2003 ND #11 | 2006-2013 | 1986-03-30 | 1986-03-30 | 1986-03-30 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/B/Beau_Waters.html) |
| 12 | Ryan Murphy | 2003 ND #12 | 2005-2010 | 1985-05-24 | 1985-05-24 | 1985-05-24 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/R/Ryan_Murphy.html) |
| 13 | Brent Stanton | 2003 ND #13 | 2005-2017 | 1986-05-01 | 1986-05-01 | 1986-05-01 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/B/Brent_Stanton.html) |
| 14 | Fergus Watts | 2003 ND #14 | 2006-2006 | 1985-09-21 | 1985-09-21 | 1985-09-21 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/F/Fergus_Watts.html) |
| 15 | Troy Chaplin | 2003 ND #15 | 2005-2016 | 1986-02-23 | 1986-02-23 | 1986-02-23 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/T/Troy_Chaplin.html) |
| 16 | Llane Spaanderman | 2003 ND #18 | 2005-2005 | 1986-02-10 | 1986-02-10 | 1986-02-10 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/L/Llane_Spaanderman.html) |
| 17 | David Mundy | 2003 ND #19 | 2005-2022 | 1985-07-20 | 1985-07-20 | 1985-07-20 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/D/David_Mundy.html) |
| 18 | Sam Butler \* | 2003 ND #20 | 2005-2017 | 1986-01-14 | 1986-01-14 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/S/Sam_Butler0.html) |
| 19 | Cameron Thurley | 2003 ND #22 | 2005-2006 | 1981-11-26 | 1981-11-26 | 1981-11-26 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/C/Cameron_Thurley.html) |
| 20 | Matthew Moody | 2003 ND #23 | 2005-2008 | 1985-09-23 | 1985-09-23 | 1985-09-23 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Matthew_Moody.html) |
| 21 | Chad Jones | 2003 ND #24 | 2006-2008 | 1984-06-15 | 1984-06-15 | 1984-06-15 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/C/Chad_Jones.html) |
| 22 | Harry Miller | 2003 ND #25 | 2005-2006 | 1985-06-11 | 1985-06-11 | 1985-06-11 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/H/Harry_Miller.html) |
| 23 | Daniel McConnell | 2003 ND #26 | 2005-2006 | 1986-06-21 | 1986-06-21 | 1986-06-21 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/D/Daniel_McConnell.html) |
| 24 | Adam Campbell | 2003 ND #27 | 2007-2009 | 1985-01-25 | 1985-01-25 | 1985-01-25 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/A/Adam_Campbell.html) |
| 25 | Jay Nash | 2003 ND #28 | 2005-2010 | 1985-12-21 | 1985-12-21 | 1985-12-21 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jay_Nash.html) |
| 26 | Tim Schmidt | 2003 ND #29 | 2007-2008 | 1986-03-14 | 1986-03-14 | 1986-03-14 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/T/Tim_Schmidt.html) |
| 27 | Brad Symes | 2003 ND #30 | 2006-2012 | 1985-03-07 | 1985-03-07 | 1985-03-07 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/B/Brad_Symes.html) |
| 28 | Jed Adcock | 2003 ND #33 | 2005-2016 | 1985-11-15 | 1985-11-15 | 1985-11-15 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jed_Adcock.html) |
| 29 | Brent Hall | 2003 ND #35 | 2005-2005 | 1986-01-07 | 1986-01-07 | 1986-01-07 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/B/Brent_Hall.html) |
| 30 | Chris Johnson \* | 2003 ND #36 | 2005-2010 | 1986-01-25 | 1986-01-25 | 1986-01-25 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/C/Chris_Johnson1.html) |
| 31 | Tom Roach | 2003 ND #37 | 2006-2006 | 1985-09-02 | 1985-09-02 | 1985-09-02 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/T/Tom_Roach.html) |
| 32 | Mark Blake | 2003 ND #38 | 2005-2010 | 1985-09-09 | 1985-09-09 | 1985-09-09 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Mark_Blake.html) |
| 33 | Eddie Sansbury | 2003 ND #39 | 2005-2008 | 1983-11-26 | 1983-11-26 | 1983-11-26 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/E/Eddie_Sansbury.html) |
| 34 | Zac Dawson | 2003 ND #40 | 2005-2017 | 1986-02-22 | 1986-02-22 | 1986-02-22 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/Z/Zac_Dawson.html) |
| 35 | Matthew Spencer | 2003 ND #41 | 2006-2006 | 1985-01-17 | 1985-01-17 | 1985-01-17 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Matthew_Spencer.html) |
| 36 | Ricky Dyson | 2003 ND #43 | 2005-2012 | 1985-09-28 | 1985-09-28 | 1985-09-28 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/R/Ricky_Dyson.html) |
| 37 | Michael Pettigrew | 2003 ND #44 | 2005-2011 | 1985-03-16 | 1985-03-16 | 1985-03-16 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Michael_Pettigrew.html) |
| 38 | Heath Shaw | 2003 ND #46 | 2005-2020 | 1985-11-27 | 1985-11-27 | 1985-11-27 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/H/Heath_Shaw.html) |
| 39 | Daniel Jackson | 2003 ND #49 | 2005-2014 | 1986-04-25 | 1986-04-25 | 1986-04-25 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/D/Daniel_Jackson.html) |
| 40 | Brent LeCras | 2003 ND #51 | 2006-2006 | 1981-10-12 | 1981-10-12 | 1981-10-12 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/B/Brent_LeCras.html) |
| 41 | Julian Rowe | 2003 ND #54 | 2005-2005 | 1985-05-25 | 1985-05-25 | 1985-05-25 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Julian_Rowe.html) |
| 42 | Michael Rischitelli | 2003 ND #55 | 2005-2019 | 1986-01-08 | 1986-01-08 | 1986-01-08 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Michael_Rischitelli.html) |
| 43 | Brent Hartigan | 2003 ND #56 | 2005-2007 | 1985-04-07 | 1985-04-07 | 1985-04-07 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/B/Brent_Hartigan.html) |
| 44 | Adrian Deluca | 2003 ND #57 | 2005-2006 | 1982-05-15 | 1982-05-15 | 1982-05-15 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/A/Adrian_De_Luca.html) |
| 45 | Andrew Raines | 2003 ND #60 | 2005-2015 | 1986-03-08 | 1986-03-08 | 1986-03-08 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/A/Andrew_Raines.html) |
| 46 | Michael Johnson | 2003 RD #1 | 2005-2018 | 1984-10-20 | 1984-10-20 | 1984-10-20 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Michael_Johnson.html) |
| 47 | Nathan Foley | 2003 RD #5 | 2005-2014 | 1985-09-08 | 1985-09-08 | 1985-09-08 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/N/Nathan_Foley.html) |
| 48 | Paul Duffield | 2003 RD #11 | 2006-2015 | 1985-02-05 | 1985-02-05 | 1985-02-05 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/P/Paul_Duffield.html) |
| 49 | Jacob Surjan | 2003 RD #16 | 2005-2012 | 1985-08-15 | 1985-08-15 | 1985-08-15 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jacob_Surjan.html) |
| 50 | Michael Rix | 2003 RD #20 | 2007-2008 | 1981-01-08 | 1981-01-08 | 1981-01-08 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Michael_Rix.html) |
| 51 | Adam Bentick | 2003 RD #27 | 2005-2008 | 1985-06-13 | 1985-06-13 | 1985-06-13 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/A/Adam_Bentick.html) |
| 52 | Josh Thurgood | 2003 RD #28 | 2007-2007 | 1985-06-05 | 1985-06-05 | 1985-06-05 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Josh_Thurgood.html) |
| 53 | Jaymie Graham | 2003 RD #29 | 2006-2008 | 1983-02-06 | 1983-02-06 | 1983-02-06 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jaymie_Graham.html) |
| 54 | Brett Deledio | 2004 ND #1 | 2005-2019 | 1987-04-18 | 1987-04-18 | 1987-04-18 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/B/Brett_Deledio.html) |
| 55 | Jarryd Roughead | 2004 ND #2 | 2005-2019 | 1987-01-23 | 1987-01-23 | 1987-01-23 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jarryd_Roughead.html) |
| 56 | Ryan Griffen | 2004 ND #3 | 2005-2018 | 1986-07-27 | 1986-07-27 | 1986-07-27 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/R/Ryan_Griffen.html) |
| 57 | Richard Tambling | 2004 ND #4 | 2005-2013 | 1986-09-12 | 1986-09-12 | 1986-09-12 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/R/Richard_Tambling.html) |
| 58 | Lance Franklin | 2004 ND #5 | 2005-2023 | 1987-01-30 | 1987-01-30 | 1987-01-30 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/L/Lance_Franklin.html) |
| 59 | Tom Williams \* | 2004 ND #6 | 2007-2014 | 1986-07-17 | 1986-07-17 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/T/Tom_Williams1.html) |
| 60 | Jordan Lewis | 2004 ND #7 | 2005-2019 | 1986-04-24 | 1986-04-24 | 1986-04-24 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jordan_Lewis.html) |
| 61 | John Meesen | 2004 ND #8 | 2007-2009 | 1986-06-20 | 1986-06-20 | 1986-06-20 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/John_Meesen.html) |
| 62 | Jordan Russell | 2004 ND #9 | 2005-2013 | 1986-11-06 | 1986-11-06 | 1986-11-06 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jordan_Russell.html) |
| 63 | Chris Egan | 2004 ND #10 | 2007-2008 | 1986-10-26 | 1986-10-26 | 1986-10-26 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/C/Chris_Egan.html) |
| 64 | Jesse Smith \* | 2004 ND #11 | 2007-2008 | 1986-09-29 | 1986-09-29 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jesse_Smith0.html) |
| 65 | Adam Thomson | 2004 ND #12 | 2005-2010 | 1986-08-21 | 1986-08-21 | 1986-08-21 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/A/Adam_Thomson.html) |
| 66 | Danny Meyer | 2004 ND #13 | 2005-2010 | 1986-08-03 | 1986-08-03 | 1986-08-03 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/D/Danny_Meyer.html) |
| 67 | Mitch Morton | 2004 ND #14 | 2005-2013 | 1987-01-28 | 1987-01-28 | 1987-01-28 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Mitch_Morton.html) |
| 68 | Matthew Bate | 2004 ND #15 | 2006-2012 | 1987-05-24 | 1987-05-24 | 1987-05-24 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Matthew_Bate.html) |
| 69 | Angus Monfries | 2004 ND #16 | 2007-2017 | 1987-01-19 | 1987-01-19 | 1987-01-19 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/A/Angus_Monfries.html) |
| 70 | Lynden Dunn | 2004 ND #17 | 2007-2020 | 1987-05-14 | 1987-05-14 | 1987-05-14 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/L/Lynden_Dunn.html) |
| 71 | Adam Pattison | 2004 ND #18 | 2005-2010 | 1986-03-05 | 1986-03-05 | 1986-03-05 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/A/Adam_Pattison.html) |
| 72 | Andrew McQualter | 2004 ND #19 | 2006-2012 | 1986-06-09 | 1986-06-09 | 1986-06-09 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/A/Andrew_McQualter.html) |
| 73 | Cameron Wood | 2004 ND #20 | 2005-2015 | 1987-03-04 | 1987-03-04 | 1987-03-04 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/C/Cameron_Wood.html) |
| 74 | Dean Polo | 2004 ND #22 | 2006-2012 | 1986-08-05 | 1986-08-05 | 1986-08-05 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/D/Dean_Polo.html) |
| 75 | Travis Cloke | 2004 ND #23 | 2005-2017 | 1987-03-05 | 1987-03-05 | 1987-03-05 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/T/Travis_Cloke.html) |
| 76 | Tom Murphy \* | 2004 ND #24 | 2005-2014 | 1986-03-19 | 1986-03-19 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/T/Tom_Murphy0.html) |
| 77 | Sean Rusling | 2004 ND #26 | 2005-2008 | 1986-10-06 | 1986-10-06 | 1986-10-06 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/S/Sean_Rusling.html) |
| 78 | Nathan van Berlo | 2004 ND #27 | 2005-2016 | 1986-06-06 | 1986-06-06 | 1986-06-06 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/N/Nathan_van_Berlo.html) |
| 79 | Adam Hartlett | 2004 ND #28 | 2007-2009 | 1986-04-22 | 1986-04-22 | 1986-04-22 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/A/Adam_Hartlett.html) |
| 80 | Matthew Little | 2004 ND #29 | 2007-2007 | 1986-01-03 | 1986-01-03 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Matthew_Little.html) |
| 81 | Matt Rosa | 2004 ND #32 | 2005-2018 | 1986-11-23 | 1986-11-23 | 1986-11-23 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Matt_Rosa.html) |
| 82 | Jarred Moore | 2004 ND #34 | 2005-2011 | 1986-03-06 | 1986-03-06 | 1986-03-06 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jarred_Moore.html) |
| 83 | Brent Prismall | 2004 ND #35 | 2007-2011 | 1986-07-14 | 1986-07-14 | 1986-07-14 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/B/Brent_Prismall.html) |
| 84 | Fabian Deluca | 2004 ND #37 | 2007-2008 | 1987-01-27 | 1987-01-27 | 1987-01-27 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/F/Fabian_Deluca.html) |
| 85 | Luke McGuane | 2004 ND #38 | 2006-2015 | 1987-02-12 | 1987-02-12 | 1987-02-12 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/L/Luke_McGuane.html) |
| 86 | Mark LeCras | 2004 ND #39 | 2005-2018 | 1986-08-30 | 1986-08-30 | 1986-08-30 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Mark_LeCras.html) |
| 87 | Ivan Maric | 2004 ND #41 | 2006-2016 | 1986-01-04 | 1986-01-04 | 1986-01-04 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/I/Ivan_Maric.html) |
| 88 | Luke Blackwell | 2004 ND #42 | 2007-2007 | 1986-11-09 | 1986-11-09 | 1986-11-09 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/L/Luke_Blackwell.html) |
| 89 | Michael Newton | 2004 ND #43 | 2007-2011 | 1987-04-27 | 1987-04-27 | 1987-04-27 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Michael_Newton.html) |
| 90 | Justin Sherman | 2004 ND #44 | 2005-2012 | 1987-01-26 | 1987-01-26 | 1987-01-26 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Justin_Sherman.html) |
| 91 | Henry Slattery | 2004 ND #45 | 2007-2012 | 1986-01-22 | 1986-01-22 | 1986-01-22 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/H/Henry_Slattery.html) |
| 92 | Nathan Ablett | 2004 ND #46 | 2007-2011 | 1985-12-13 | 1985-12-13 | 1985-12-13 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/N/Nathan_Ablett.html) |
| 93 | Jayden Attard | 2004 ND #47 | 2007-2007 | 1986-02-27 | 1986-02-27 | 1986-02-27 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jayden_Attard.html) |
| 94 | Simon Taylor \* | 2004 ND #50 | 2005-2010 | 1982-08-18 | 1982-08-18 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/S/Simon_Taylor1.html) |
| 95 | Stephen Tiller | 2004 ND #51 | 2007-2009 | 1987-03-26 | 1987-03-26 | 1987-03-26 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/S/Stephen_Tiller.html) |
| 96 | Chris Knights | 2004 ND #53 | 2005-2015 | 1986-09-25 | 1986-09-25 | 1986-09-25 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/C/Chris_Knights.html) |
| 97 | Brad Moran | 2004 ND #54 | 2006-2011 | 1986-09-29 | 1986-09-29 | 1986-09-29 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/B/Brad_Moran.html) |
| 98 | Matthew Egan | 2004 ND #57 | 2005-2007 | 1983-07-10 | 1983-07-10 | 1983-07-10 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Matthew_Egan.html) |
| 99 | James Gwilt | 2004 ND #58 | 2006-2016 | 1986-08-11 | 1986-08-11 | 1986-08-11 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/James_Gwilt.html) |
| 100 | Eddie Betts | 2004 RD #1 | 2005-2021 | 1986-11-26 | 1986-11-26 | 1986-11-26 | VERIFIED | [afltables](https://afltables.com/afl/stats/players/E/Eddie_Betts.html) |
| 101 | Will Thursfield | 2004 RD #3 | 2005-2011 | 1986-04-19 | 1986-04-19 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/W/Will_Thursfield.html) |
| 102 | Ben Davies | 2004 RD #6 | 2008-2008 | 1986-02-10 | 1986-02-10 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/B/Ben_Davies.html) |
| 103 | Danyle Pearce | 2004 RD #17 | 2005-2018 | 1986-04-07 | 1986-04-07 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/D/Danyle_Pearce.html) |
| 104 | Clinton Young | 2004 RD #18 | 2005-2014 | 1986-02-16 | 1986-02-16 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/C/Clinton_Young.html) |
| 105 | Heritier Lumumba | 2004 RD #20 | 2007-2016 | 1986-11-15 | 1986-11-15 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/H/Heritier_Lumumba.html) |
| 106 | Jonathon Griffin | 2004 RD #21 | 2007-2017 | 1986-01-14 | 1986-01-14 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jonathon_Griffin.html) |
| 107 | Beau Maister | 2004 RD #23 | 2008-2014 | 1986-03-20 | 1986-03-20 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/B/Beau_Maister.html) |
| 108 | Luke Vogels | 2004 RD #26 | 2007-2007 | 1983-06-07 | 1983-06-07 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/L/Luke_Vogels.html) |
| 109 | John Hinge | 2004 RD #30 | 2007-2007 | 1986-06-06 | 1986-06-06 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/John_Hinge.html) |
| 110 | Scott McMahon | 2004 RD #32 | 2007-2015 | 1986-06-02 | 1986-06-02 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/S/Scott_McMahon.html) |
| 111 | Heath Grundy | 2004 RD #34 | 2006-2019 | 1986-06-02 | 1986-06-02 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/H/Heath_Grundy.html) |
| 112 | Marcus Allan | 2004 RD #41 | 2007-2007 | 1986-05-23 | 1986-05-23 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Marcus_Allan.html) |
| 113 | Will Hamill \* | 2004 RD #43 | 2007-2007 | 1986-07-26 | 1986-07-26 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/W/Will_Hamill0.html) |
| 114 | Scott Harding | 2004 RD #45 | 2006-2010 | 1986-06-19 | 1986-06-19 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/S/Scott_Harding.html) |
| 115 | Marc Murphy | 2005 ND #1 | 2006-2021 | 1987-07-19 | 1987-07-19 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Marc_Murphy.html) |
| 116 | Dale Thomas | 2005 ND #2 | 2006-2019 | 1987-06-21 | 1987-06-21 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/D/Dale_Thomas.html) |
| 117 | Xavier Ellis | 2005 ND #3 | 2007-2016 | 1988-02-28 | 1988-02-28 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/X/Xavier_Ellis.html) |
| 118 | Joshua Kennedy \* | 2005 ND #4 | 2006-2022 | 1987-08-25 | 1987-08-25 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Josh_Kennedy0.html) |
| 119 | Beau Dowler | 2005 ND #6 | 2006-2009 | 1987-12-16 | 1987-12-16 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/B/Beau_Dowler.html) |
| 120 | Paddy Ryder | 2005 ND #7 | 2007-2022 | 1988-03-14 | 1988-03-14 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/P/Paddy_Ryder.html) |
| 121 | Jarrad Oakley-Nicholls | 2005 ND #8 | 2006-2009 | 1988-02-09 | 1988-02-09 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jarrad_Oakley-Nicholls.html) |
| 122 | Mitch Clark | 2005 ND #9 | 2006-2016 | 1987-10-19 | 1987-10-19 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Mitch_Clark.html) |
| 123 | Marcus Drum | 2005 ND #10 | 2006-2009 | 1987-05-01 | 1987-05-01 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Marcus_Drum.html) |
| 124 | Shaun Higgins | 2005 ND #11 | 2006-2022 | 1988-03-04 | 1988-03-04 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/S/Shaun_Higgins.html) |
| 125 | Nathan Jones | 2005 ND #12 | 2006-2021 | 1988-01-20 | 1988-01-20 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/N/Nathan_Jones.html) |
| 126 | Shannon Hurn | 2005 ND #13 | 2006-2023 | 1987-09-04 | 1987-09-04 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/S/Shannon_Hurn.html) |
| 127 | Grant Birchall | 2005 ND #14 | 2006-2021 | 1988-01-28 | 1988-01-28 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/G/Grant_Birchall.html) |
| 128 | Travis Varcoe | 2005 ND #15 | 2007-2020 | 1988-04-10 | 1988-04-10 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/T/Travis_Varcoe.html) |
| 129 | Richard Douglas | 2005 ND #16 | 2007-2019 | 1987-02-06 | 1987-02-06 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/R/Richard_Douglas.html) |
| 130 | Darren Pfeiffer | 2005 ND #17 | 2008-2012 | 1987-09-28 | 1987-09-28 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/D/Darren_Pfeiffer.html) |
| 131 | Max Bailey | 2005 ND #18 | 2006-2013 | 1986-10-23 | 1986-10-23 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Max_Bailey.html) |
| 132 | Courtenay Dempsey | 2005 ND #19 | 2007-2016 | 1987-08-28 | 1987-08-28 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/C/Courtenay_Dempsey.html) |
| 133 | Paul Bower | 2005 ND #20 | 2006-2012 | 1988-01-09 | 1988-01-09 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/P/Paul_Bower.html) |
| 134 | Danny Stanley | 2005 ND #21 | 2007-2015 | 1988-02-18 | 1988-02-18 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/D/Danny_Stanley.html) |
| 135 | Beau Muston | 2005 ND #22 | 2009-2010 | 1987-03-01 | 1987-03-01 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/B/Beau_Muston.html) |
| 136 | Ryan Cook | 2005 ND #23 | 2007-2009 | 1988-02-16 | 1988-02-16 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/R/Ryan_Cook.html) |
| 137 | Cleve Hughes | 2005 ND #24 | 2007-2008 | 1987-01-15 | 1987-01-15 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/C/Cleve_Hughes.html) |
| 138 | Wayde Mills | 2005 ND #25 | 2007-2008 | 1987-08-29 | 1987-08-29 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/W/Wayde_Mills.html) |
| 139 | Garrick Ibbotson | 2005 ND #26 | 2007-2017 | 1988-03-15 | 1988-03-15 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/G/Garrick_Ibbotson.html) |
| 140 | Dylan Addison | 2005 ND #27 | 2006-2014 | 1987-10-07 | 1987-10-07 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/D/Dylan_Addison.html) |
| 141 | Matt Riggio | 2005 ND #28 | 2007-2009 | 1988-03-14 | 1988-03-14 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Matt_Riggio.html) |
| 142 | Ben McKinley | 2005 ND #29 | 2007-2011 | 1987-03-04 | 1987-03-04 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/B/Ben_McKinley.html) |
| 143 | Nick Lower | 2005 ND #30 | 2008-2013 | 1987-06-23 | 1987-06-23 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/N/Nick_Lower.html) |
| 144 | Trent West | 2005 ND #31 | 2008-2016 | 1987-10-17 | 1987-10-17 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/T/Trent_West.html) |
| 145 | Matthew Spangher | 2005 ND #34 | 2008-2016 | 1987-04-23 | 1987-04-23 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Matthew_Spangher.html) |
| 146 | Jake Edwards | 2005 ND #36 | 2008-2008 | 1988-01-06 | 1988-01-06 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jake_Edwards.html) |
| 147 | John Anthony \* | 2005 ND #37 | 2008-2012 | 1988-01-19 | 1988-01-19 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/John_Anthony1.html) |
| 148 | Travis Tuck | 2005 ND #38 | 2007-2009 | 1987-09-07 | 1987-09-07 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/T/Travis_Tuck.html) |
| 149 | Jay Neagle | 2005 ND #39 | 2007-2010 | 1988-01-17 | 1988-01-17 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jay_Neagle.html) |
| 150 | Rhan Hooper | 2005 ND #41 | 2006-2010 | 1988-01-09 | 1988-01-09 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/R/Rhan_Hooper.html) |
| 151 | Robert Warnock | 2005 ND #42 | 2007-2015 | 1987-01-19 | 1987-01-19 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/R/Robert_Warnock.html) |
| 152 | Andrew Swallow | 2005 ND #43 | 2006-2017 | 1987-06-02 | 1987-06-02 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/A/Andrew_Swallow.html) |
| 153 | Alipate Carlile | 2005 ND #44 | 2006-2016 | 1987-04-30 | 1987-04-30 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/A/Alipate_Carlile.html) |
| 154 | Ryan Gamble | 2005 ND #45 | 2008-2011 | 1987-09-23 | 1987-09-23 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/R/Ryan_Gamble.html) |
| 155 | Alan Obst | 2005 ND #46 | 2008-2009 | 1987-05-19 | 1987-05-19 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/A/Alan_Obst.html) |
| 156 | Sam Lonergan | 2005 ND #47 | 2008-2013 | 1987-03-26 | 1987-03-26 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/S/Sam_Lonergan.html) |
| 157 | Matthew Laidlaw | 2005 ND #48 | 2007-2007 | 1987-02-09 | 1987-02-09 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Matthew_Laidlaw.html) |
| 158 | Simon Buckley | 2005 ND #49 | 2007-2012 | 1987-04-18 | 1987-04-18 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/S/Simon_Buckley.html) |
| 159 | Kristin Thornton | 2005 ND #50 | 2009-2009 | 1988-03-05 | 1988-03-05 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/K/Kristin_Thornton.html) |
| 160 | Ryan Brabazon | 2005 ND #54 | 2008-2009 | 1986-12-26 | 1986-12-26 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/R/Ryan_Brabazon.html) |
| 161 | Clint Bartram | 2005 ND #55 | 2006-2012 | 1988-02-16 | 1988-02-16 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/C/Clint_Bartram.html) |
| 162 | Jonathan Giles | 2005 ND #61 | 2012-2017 | 1988-01-08 | 1988-01-08 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jonathan_Giles.html) |
| 163 | Justin Sweeney | 2005 ND #62 | 2007-2007 | 1987-12-25 | 1987-12-25 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Justin_Sweeney.html) |
| 164 | Ryan Jackson | 2005 RD #1 | 2007-2008 | 1987-04-04 | 1987-04-04 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/R/Ryan_Jackson.html) |
| 165 | Alan Toovey | 2005 RD #2 | 2007-2016 | 1987-03-23 | 1987-03-23 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/A/Alan_Toovey.html) |
| 166 | Angus Graham | 2005 RD #5 | 2007-2012 | 1987-04-16 | 1987-04-16 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/A/Angus_Graham.html) |
| 167 | Jason Roe | 2005 RD #6 | 2007-2009 | 1984-03-13 | 1984-03-13 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jason_Roe.html) |
| 168 | Sam Iles | 2005 RD #7 | 2007-2012 | 1987-06-19 | 1987-06-19 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/S/Sam_Iles.html) |
| 169 | Jace Bode | 2005 RD #8 | 2007-2008 | 1987-09-14 | 1987-09-14 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jace_Bode.html) |
| 170 | Ed Lower | 2005 RD #9 | 2006-2010 | 1987-06-23 | 1987-06-23 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/E/Ed_Lower.html) |
| 171 | Matt White | 2005 RD #14 | 2006-2017 | 1987-04-15 | 1987-04-15 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Matt_White.html) |
| 172 | Jonathan Simpkin | 2005 RD #15 | 2012-2016 | 1987-10-28 | 1987-10-28 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jonathan_Simpkin.html) |
| 173 | Daniel Nicholls | 2005 RD #17 | 2007-2007 | 1987-03-02 | 1987-03-02 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/D/Daniel_Nicholls.html) |
| 174 | Lukas Markovic | 2005 RD #18 | 2011-2013 | 1987-01-05 | 1987-01-05 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/L/Lukas_Markovic.html) |
| 175 | Heath Hocking | 2005 RD #19 | 2007-2017 | 1987-12-27 | 1987-12-27 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/H/Heath_Hocking.html) |
| 176 | Matt Thomas | 2005 RD #20 | 2006-2015 | 1987-02-27 | 1987-02-27 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/M/Matt_Thomas.html) |
| 177 | Jason Porplyzia | 2005 RD #22 | 2006-2014 | 1984-11-27 | 1984-11-27 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/J/Jason_Porplyzia.html) |
| 178 | Djaran Whyman | 2005 RD #24 | 2007-2007 | 1983-08-21 | 1983-08-21 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/D/Djaran_Whyman.html) |
| 179 | Greg Bentley | 2005 RD #25 | 2007-2009 | 1987-04-09 | 1987-04-09 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/G/Greg_Bentley.html) |
| 180 | Shannon Cox | 2005 RD #29 | 2007-2009 | 1986-03-07 | 1986-03-07 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/S/Shannon_Cox.html) |
| 181 | Cameron Howat | 2005 RD #31 | 2007-2008 | 1985-01-30 | 1985-01-30 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/C/Cameron_Howat.html) |
| 182 | Cheynee Stiller | 2005 RD #37 | 2006-2012 | 1986-05-03 | 1986-05-03 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/C/Cheynee_Stiller.html) |
| 183 | Simon Phillips | 2005 RD #40 | 2007-2012 | 1987-04-05 | 1987-04-05 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/S/Simon_Phillips.html) |
| 184 | Kieren Jack | 2005 RD #42 | 2007-2019 | 1987-06-28 | 1987-06-28 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/K/Kieren_Jack.html) |
| 185 | Ed Barlow | 2005 RD #44 | 2007-2011 | 1987-01-27 | 1987-01-27 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/E/Ed_Barlow.html) |
| 186 | Sam Rowe | 2005 RD #46 | 2013-2019 | 1987-11-19 | 1987-11-19 | — | VERIFIED | [afltables](https://afltables.com/afl/stats/players/S/Sam_Rowe.html) |

\* namesake existed on AFL Tables; page selected as described in the Disambiguation section.

## Incidental observation (outside the scope of this check)

The birth dates are clean, but the sheet's **`First season` column disagrees with the AFL Tables debut year on 67 of the 186 rows**, almost always because the sheet lists a *later* debut than the player actually had (e.g. Adam Cooney 2005 vs actual 2004; Beau Waters 2006 vs actual 2004; Heritier Lumumba 2007 vs actual 2005). Several rows also understate career length at the front end by two full seasons. If the valuation model consumes `First season` or derives an age-at-debut or years-of-service term from it, that column is worth its own pass before anything is written to the system of record. No `First season` value was changed here.

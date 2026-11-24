# PSD returns — store-edit act, 2026-11-23

Owner words (verbatim): "We also need to add some players to the pool for PSD: Liam Jones, James Bell, Dominic Bedendo,
Nathan Kreuger, Alex Mirkov, Tyler Sellers, Kallan Dawson ... Can you find them, reactivate them, and put them in the draft
night artifact?"; "Sellers is being added as a SSP player today. Jones, Kreuger and Bell are being added as first nations
category B rookies, a new category, but I think we can classify them as SSP players for our purposes. All have AFL
history, like Bedendo."; "Sellers, Kreuger - Essendon; Jones - Gold Coast; Bell - GWS; Knevitt, still at Richmond, now
Sydney IRL; Green - a selectable free agent now."

Bedendo and Mirkov were already active (roster-returns act, 2026-11-06); nothing to do for them.

## The edits
- kallan-dawson (GWS, 2026 rookie draft pick 17), tyler-sellers (Essendon), nathan-kreuger (Essendon), liam-jones
  (Gold Coast), james-bell (GWS): `_retired` true→false, `_last_listed` →2026 (Bell had none), `eligibilities` added
  (KPD, KPF, KPF, KPD, SF), and a 2026 season {0 games} — the shape the roster-returns act gave Bedendo. Each keeps
  their original draft entry and AFL history; their value comes from that history.
- mitchell-knevitt (Richmond Tigers; AFL Sydney) and steely-green (AFFL free agent; AFL Richmond): `_retired`
  true→false only — both already carry a 2026 season, `_last_listed` 2026 and eligibilities.
The sheet, register and the store's afl_club/affl_team were carried by the ownership courier first (commit 70730ee4).

## Movers
Seven rows appear on the active board; the rest of the board re-scales by rounding only (pool normalisation,
as in the roster-returns act). The dry run is the prediction of record.

## Dry run (2026-11-24) and owner word
Board 159d3972 → 9f8ff91d, store 4c61f352 → e8dd5c5b; 25 of 1029 valued rows move: the seven (Sellers 11→71,
Dawson 10→28, Kreuger 5→19, Jones 10→8, Bell new at 6, Knevitt 17→193, Green 4→114) and 18 rounding movers
(−4..+5). Pool 673,209 → 673,646. Owner: "Yes, Knevitt and Green should be reactivated. Knevitt was never inactive -
he was on Richmond's list in 2026 (AFFL) and was retained through the drafts." board_after is pinned to the dry run.

# Summary — Blind UI Review of "ValueBoard"

What it is: a price list for AFL players in a 16-team fantasy league.
Every player and draft pick gets one number, so you can trade them fairly.
The user is one person: the league owner. A switch publishes a trimmed public version.

I could work out five of the six screens unaided. That is good.
Rankings, the club table, the club drill-in and the trade desk all explain themselves.

What I could not work out from the screen alone:
- AFFL. SCAR. bake. GUARD 5 PASS. panel 10/10. Never defined anywhere.
- The "+2 yr" view. It dumps a page of accounting I could not read.
- Why "OVER FREE" exists. It is just the value minus 190.

Biggest problems:
1. A whole column (Delta vs round) is empty on all 804 rows.
2. The value — the point of the app — is the quietest text in each row. Club names shout instead.
3. The Player Card tab has no way to pick a player. You must scroll an 804-row list first.
4. Build codes and hashes take the top of every screen. They mean nothing to a user.
5. On a phone, header and controls fill more than a whole screen before any data.
6. On a phone, the rankings drop four useful columns but keep an empty dash.
7. On a phone, the club table hides six columns behind a sideways scroll with no hint it scrolls.
8. No sticky column headers. By row 90 you cannot tell what the numbers are.
9. The bar next to each value is the same length for 88% of players.
10. Unfinished parts are shown and described rather than hidden.

Best things in it:
- The player history table shows model changes on the same timeline as real rounds. Excellent.
- Every club stat says "rank 3 of 16" underneath it. Context in one glance.
- The trade verdict in plain English: "you give up 280 — roughly an early fourth-round pick."
  That sentence is the best thing in the app. It breaks on large trades and should be fixed.

Direction: keep the trading-terminal look. Spend the bright green on one number per screen.
Make the tables real tables. Push engineering codes to a single line at the foot of the page.

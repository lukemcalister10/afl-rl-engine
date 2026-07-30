# #274 item 4 — the ten #139 display/navigation items: verified, not rebuilt

Measured 2026-07-30 on the adopted board `f2df6e0a`.

## The finding that shapes this item

**All ten were already implemented — by #222 — and each already had assertions.** What had *not* happened
is verification on the post-adoption tree: `ui/tests/ui_222_items.test.mjs` runs at Final Integration step
14, and steps 14–22 were **SHADOWED** behind the `movers.test.js` red that #274 item 1 clears. So the suite
had never run in this era. When item 1 unshadowed it, three assertions failed — all adoption-stale counts
in a different item (the 30/7 column made the history nine points, not eight, and added a second
model-change tag), measured identically at main tip `f1557b2` and therefore inherited, not caused here.
With those restated, **all ten items verify green on the adopted board.**

So item 4 needed no new display code. Writing some would have been churn against working, tested surfaces —
and the issue's own out-of-scope list is law.

## The ten, each with the assertion that proves it

| #139 item | what it requires | asserted |
|---|---|---|
| **#12** public club-profile click | open a club in Public → that club's profile, not the all-player list | "opening a club in Public routes to the board WITH the club filter set" · "the public board shows that club only, not the all-player list" |
| **#16** public player click | clicking a player in Public opens his profile | "clicking a player in Public opens that player's profile" |
| **#15** universal Back | returns to the actual previous page, club→player and player→club included | "a universal Back control is present" · "Back returns to the CLUB page, not the all-player list" · "the club filter is restored with the page" · "Back exists on the Clubs page too (it is not player-card-specific)" · "Back from Clubs returns to the board" |
| **#13** rename | Board → "AFFL Rankings" | "Board is renamed AFFL Rankings" |
| **#14** per-tab subtitles | five tabs, five subtitles | one assertion per tab: AFFL Rankings/Player Rankings · Clubs/Club Breakdown · Player card/Player Profiles · Trade desk/Trade Desk · Movers/Weekly Review |
| **#9** public ownership | public board shows AFFL/AFL club | "every public row carries the AFFL/AFL club" |
| **#17** public recent form | public cards show Recent Form | "Recent form is exposed on the public card" |
| **#18** card parity | public may show draft pick and rank with denominator; private fields kept private BY DECISION | "the public card shows the draft pick" · "shows rank WITH its denominator" · and four explicit privacy decisions: build provenance, owner override, per-lever attribution all stay hidden, and the hardcoded "— steady" is gone |
| **#11** club summary | club page opens with the comparison metrics before the player list | "the club page opens with the club profile summary" · "the summary carries the comparison-page metrics, each with its rank" · "the summary appears BEFORE the player list" |
| **#5** Free Agents | duplicate spellings canonicalised, display/filtering only | "the Movers club filter lists the Free-Agents pool exactly once" · "both authored spellings canonicalise to one key" · "selecting the pool returns rows of BOTH authored spellings" |

Suite total: **73 of 73**, covering these ten plus items 1, 2, 3 and 21.

## Screenshots

- `04_item4_board_affl_rankings.png` — the renamed board with its subtitle (#13, #14).
- `04_item4_item11_club_summary.png` — a club page reached by clicking a club, summary above the list (#11, #15 route).
- `04_item4_item12_public_club_route.png` — the PUBLIC tier, club opened, filtered to that club (#12).
- `04_item4_item17_18_public_card.png` — a public player card: recent form, draft pick, rank with denominator (#17, #18).

## Note on baselines, recorded because one was wrong first

Item 3's before/after pair was first captured against `HEAD` *after* item 3 was already committed, so the
two images came out byte-identical. The pair was recaptured against `HEAD~1` — the tree carrying items 1
and 2 but not the over-free column — which isolates item 3 alone. Item 2's pair is against the item-1 tree,
which is the correct baseline for the selector change.

The shipped `ui/index.html` was loaded from `file://` with no server for every capture, zero page errors,
and every view was exercised in both tiers.

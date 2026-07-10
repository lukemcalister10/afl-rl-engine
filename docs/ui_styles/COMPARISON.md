# THE FOUR PITCHES — comparison note · FABLE seat · 2026-07-09
### One page, plain language. Same brief, four designers. Every theme shows the SAME two screens
### (the board · the Coleman-Jones player card) in BOTH trims (working aid · public), so any
### difference you feel is the design, not the content. ALL FIGURES INVENTED — not the board.

## How to look
Open each theme's four files in a browser side by side. Judge on: can you read 25 rows without
effort · does the working aid feel like *your* instrument · would you be happy handing the public
file to someone else · which value-number treatment do you trust fastest.

| | 01 · Cockpit | 02 · Broadsheet | 03 · Matchday | 04 · Registry |
|---|---|---|---|---|
| **In a phrase** | the instrument panel | the Saturday form guide | the broadcast package | the Swiss ledger |
| **Optimises for** | long working sessions in the dark; provenance always in eyeshot | calm reading and print authority; feels settled, low-adrenaline | instant legibility at a glance; big numbers, high energy | maximum information per square inch with zero decoration; numbers speak |
| **Palette** | graphite · phosphor-cyan data · amber for your hand | warm paper · ink · brick accent | near-black · one volt accent | white · ink · one blue |
| **Type** | mono figures, quiet sans, 34px rows | Georgia serif display, generous rows | condensed heavy caps, big numerals | Helvetica, small caps, hairlines |
| **Value device (redesigned)** | figure column + separate slim rail — number never sits on the bar | serif figure over a thin ink underline-bar | segmented ten-block power bar, one block a decile | figure + **percentile column**; a 1px index line is the only graphic |
| **Override marker** | amber squared tag `×0.50 ROLE` | print dagger `†` resolved in a footnote | outlined volt chip `OWNER RULE ×0.50` | registry annotation `[rule ×0.50]` |
| **Your reads (pins)** | amber ★ filled/hollow | ★ met / ★ pending in small caps | volt ★ on the row card | ▪ met / ▪ pending column |
| **Risk to weigh** | closest to what you've already seen — least new information | lowest density of the four; a 1000-row scroll is a long newspaper | loudest; energy can tire over a full session | most austere; no warmth, and magnitude lives in numbers not bars |

## What is identical everywhere (the ruled law, not taste)
- **Two trims.** Working aid carries the full identity stamp (board v2.6 · engine 4b08796c · store
  a2fbc9a0 · board id fd90472c · guard 5), the Δ bake/round toggle, and a slugs-off debug toggle
  concept. Public carries values, ranks, movement vs previous round — no IDs, no guard states, no
  reads, no override machinery, no waterfall.
- **No ghost rail.** In all four, the Brodie-rule cut is a *line item in the attribution waterfall*
  (a hollow accent bar with the −876 figure); the board's value graphic never grows a dashed tail.
- **No slugs** in any default view. **Colour never the sole carrier** — every delta is signed and
  arrowed, every state labelled. **Δ scheme as ruled** — working = vs last accepted bake (toggle to
  round); published = vs previous round, no toggle.

## Hybrids that would work if no single pitch wins
- **Cockpit chrome + Registry's percentile column** (replace the rail with numbers on the dark theme).
- **Broadsheet's public trim + Cockpit's working aid** — print for the world, instrument for you.
- **Matchday's movement pills** drop cleanly into any of the other three boards.

## Files
`theme_0N_*/board_working.html · board_public.html · card_working.html · card_public.html` — sixteen
boards, all static, all self-contained, all bannered as invented figures.

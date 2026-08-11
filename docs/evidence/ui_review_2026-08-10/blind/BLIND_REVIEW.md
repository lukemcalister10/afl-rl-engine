# Blind Design Review — "ValueBoard · Matchday"

Reviewed with no access to project documentation, no knowledge of the author, and no design
brief. Everything below comes from driving the rendered page at 1440px and 390px.
Screenshots: `screens/` (58 files).

---

# PART 1 — THE COMPREHENSION TEST

*Written before any critique, from the interface alone.*

## What is this application for?

It is a **valuation board for an Australian-rules-football fantasy or dynasty league**. It puts a
single number — a "value" in a currency the app calls **SCAR** — on 804 real AFL players and on
draft picks, so that they can be compared and traded against each other in one unit. The masthead
calls it a "REAL-DRAFT VALUE ENGINE"; the top strip calls it a "WORKING AID".

The tell that this is *not* a real AFL front-office tool is the two-club columns: every player
carries both an **AFL** club (the real one — North Melbourne, Collingwood) and an **AFFL** club
(a different one — Carlton Blues, North Melbourne). "AFFL" is never expanded anywhere in the UI,
but the pattern is unmistakable: a 16-team fantasy league drafted over the top of the real 18-team
AFL, with its own rosters, its own draft picks, and its own free-agent pool. Harry Sheezel plays
for North Melbourne in real life and is owned by Carlton Blues in this league.

**Who is its user?** One person, almost certainly the owner/commissioner of that league, or a
single team's general manager. Two things make this near-certain: the interface has a
**WORKING / PUBLIC** switch, where PUBLIC strips out the trade tooling and the engine hashes and
publishes only "values, ranks and movement" — so the user is the person who *decides what other
people get to see*. And the working view has a **★ "my reads"** filter and copy that says
*"The model speaks; you overrule"* — a single opinionated operator sitting above a model.

**Domain:** sports analytics — specifically player valuation, weekly re-pricing, and trade
evaluation, in AFL fantasy/dynasty. Round 22 of the 2026 season is the current state.

---

## Per-view verdicts

### 1. AFFL RANKINGS (default view)
**What it's for:** the master list — all 804 players ranked by value, most valuable first, with
filters for position, league club, and grouping. It answers *"who is worth the most right now,
and where does anyone sit in that order?"*
**Confidence: CERTAIN.** This is the one view that explains itself. Rank, name, position, club,
a big number, a bar. No training needed.

**But its controls are not certain.** Inside this one view sit five control groups I could only
partly decode:
- `BOARD LENS: −2 yr · −1 yr · Now · +1 yr · +2 yr` — **probable**: re-price everyone as they'd
  be valued two years ago / two years from now. Choosing `+2 yr` confirmed it (values rise, and a
  `Δ VS NOW` column replaces `Δ VS ROUND`). But `+2 yr` *also* silently injects an eighteen-row
  club table and a paragraph of reconciliation arithmetic above the rankings, which I could not
  decode at all (see failures).
- `Δ BASE: bake | round` — **cannot decode.** "Bake" is not a word the interface ever defines.
  Adjacent grey text says *"Δ vs round arrives with the weekly loop (Phase 3)"*, so one of the two
  options is not live, but the toggle is still offered and still highlighted.
- `FILTER: all | my reads` — **probable**: show only starred players. But **I could find no way to
  star a player.** Clicking the ★ cell navigates to the player card instead of toggling. So the
  reads are pre-loaded from somewhere I cannot see.
- `ASSETS: players only | picks included` — **probable**: mix draft picks into the ranking as if
  they were players. Toggling it changed nothing in the visible top 100, so I never got
  confirmation.
- `DEBUG: slugs off | on` — **certain, and shouldn't be here**: prints `nick-daicos` style URL
  slugs under every player name. This is a developer switch sitting in the main control bar.

Column-level: `VALUE` certain. `POS`, `CLUB`, `PICK · YR` certain. `VS TOP` — probable (a bar
showing this player's share of the #1 price; the footer legend eventually confirms it).
`Δ VS ROUND` — **dead**: all 804 rows show an em-dash. `OVER FREE` — **guessing** until I hovered
it; the tooltip says "value − 190 (the ruled free-hit value)", which is a mechanical restatement
of VALUE and told me nothing about why I'd want it.

### 2. CLUBS
**What it's for:** the 16 league clubs ranked by total asset value, broken into player value vs
draft-pick value, with concentration measures (Top-5, Top-10) and a "Best-23" starting side.
It answers *"which club is richest, and is that wealth concentrated in stars or spread through
depth?"*
**Confidence: CERTAIN on purpose, PROBABLE on the numbers.** This is the best-explained view in
the app — a long lead paragraph defines Best-23 down to the positional structure
(2 K-DEF · 4 G-DEF · 5 MID · 4 G-FWD · 2 K-FWD · 1 RUC + 5 bench) and defines Non-Best-23 as
depth beyond the best side. I understood it. It also took me a full minute of reading to get
there, which is a long time for a table.

### 3. Club detail (drill-in from CLUBS → "OPEN ›")
**What it's for:** one club's seven headline figures, each with its league rank, followed by that
club's players filtered inside the rankings table.
**Confidence: CERTAIN.** Clean, useful, the single best-designed screen in the app — seven stats,
each with "rank N of 16" underneath, is exactly the right amount of context per number.
One contradiction I could not resolve: the stat panel says *"ranked against 16 clubs"* and
*"rank 1 of 16"*, and the band immediately below says **"CLUB RANK 1 OF 17"**.

### 4. PLAYER CARD
**What it's for:** one player's dossier — current value, rank, a five-year value curve, a recent
form line, and a fourteen-point weekly history of value / rank / positional rank / score.
It answers *"what has this player's price done over the season, and why?"*
**Confidence: CERTAIN on purpose; the weekly history table is the best information design in the
whole app.** Interleaving real rounds with `MODEL CHANGE` rows on one timeline — so you can see
that +2,002 came from a re-derivation and not from football — is genuinely excellent and I
have not seen many production tools do it.
**But the view is a navigational dead end.** It contains zero inputs and zero selects. There is no
search, no player picker, no next/previous. Clicking "PLAYER CARD" in the nav shows Harry Sheezel
and only Harry Sheezel unless you first went and clicked a row in Rankings. As a tab, it is a
promise the tab cannot keep.
Undecodable inside it: the `WHY THE PRICE IS WHAT IT IS` panel, which is an empty placeholder
explaining in spec language (`levers:[{label,delta}]`, `§7.4`, `G-ATTR`) what will appear there
one day. `Δ VS LAST BAKE ▲ +3,809` — I still don't know what a bake is, and the same field in
PUBLIC mode is relabelled `Δ VS PREV ROUND` and shows `—`, so the two modes disagree about what
that number even measures.

### 5. TRADE DESK
**What it's for:** stack assets on a GIVE side and a GET side, get the difference in one number
with a plain-English translation. It answers *"am I winning this trade, and by how much?"*
**Confidence: CERTAIN, and it works.** Typing "daic" surfaced Nick and Josh Daicos; picking Nick
added him and moved TOTAL OUT from 4,179 to 15,275 and the verdict from −280 to −11,376. The
translation line — *"You give up 280 — roughly a early fourth-round pick (≈ pick 57)"* — is the
single best sentence in the application, because it converts an abstract currency into something
a person can actually feel.
Below it sits a dashed placeholder for a "DRAFT TRANSLATOR" that "arrives after its calibration
gate" — **cannot decode** what a calibration gate is.

### 6. MOVERS
**What it's for:** diff two points in time and show who rose and fell, by value and by rank.
It answers *"what changed this week?"*
**Confidence: PROBABLE.** The four hero tiles (largest value increase / decrease / rank
improvement / rank decline) are immediately legible and the FROM/TO selectors are obvious. What
degrades it is that the two dropdowns mix real rounds with engineering events — *"30/7
rederivation"*, *"6/8 adoption — redesign era"*, *"10/8 DOB courier + v0surf re-cut"*,
*"10/8 never-rises restore (R12)"* — as peers of "Round 20". The app is honest about this (it
prints a warning when your range spans a model change, which is admirable) but as a user I cannot
choose between them, because I don't know what any of them are.

### 7. PUBLIC mode (a second skin over every tab)
**What it's for:** the shareable version. Masthead becomes "PLAYER VALUES", engine hashes and
guard badges disappear, ★ reads disappear, `Δ VS ROUND` becomes a `MOVEMENT` column reading
"— steady", and TRADE DESK is replaced by a sentence saying trade tooling stays owner-side.
**Confidence: CERTAIN.** The cleanest single idea in the product. It is also, notably, the *better
looking* of the two modes, because it strips the noise.

---

## Labels, abbreviations and numbers I could not work out

Recorded as failures of the interface, not of effort. I did not look at the code.

| Item | Where | Verdict |
|---|---|---|
| **AFFL** | everywhere, incl. the primary tab name | Never expanded. Inferred "some fantasy AFL league" from context only. |
| **SCAR** | Trade Desk verdict, footer | The name of the currency, presumably. Never defined. It is also the *unit of the whole app* and appears in exactly one view. |
| **bake** / **Δ VS LAST BAKE** | rankings control bar, player card | Cannot decode. A rebuild of the model? A weekly snapshot? Both toggle options are offered but a note says one isn't live. |
| **REALGUARD 5 PASS** (rendered as two badges, `REAL` + `GUARD 5 PASS`) | masthead, player card | Cannot decode. No tooltip, not clickable. Reads as a status light for something, but for what, and what would `FAIL` mean? |
| **panel 10/10** | masthead | Cannot decode. Ten of ten what? |
| **board id 4b448a821f54180182637983f7a26a9d · engine c0a7e969 · store d9a24282** | masthead, on every screen | Three build hashes, 50+ characters, in the most valuable pixels on the page. I can guess they are provenance stamps; I cannot imagine using them. |
| **v2.11-final-rc1-PROVISIONAL** | masthead | A version string that says "final", "release candidate 1" and "provisional" simultaneously. |
| **OVER FREE** | rankings column | Tooltip says `value − 190`. It is 100% correlated with VALUE. I could not construct a question it answers. |
| **entrant layer · +2 yr · league WITH Σ718,184 vs WITHOUT Σ655,253 (Δ +62,931) · entrant layer Σ62,931 PVC (103.43 slots/yr) · report-only · k=0 phantom=none · §2.viii seal c9e7491b** | appears above the table on `+2 yr` | **Total decode failure.** Eighteen club rows follow, each tagged `phantom`. I cannot tell if this is a feature or debug output. |
| **`2028 future-entrant reconciliation … visible Picks 1–64 Σ53,536 + national-draft deep-tail residual 2,217 + non-national-draft entry residual 7,178 = sealed F5 entrant layer 62,931 ✓`** | same view | **Total decode failure.** An accounting identity printed as a sentence. `F5`, `MSD/SSP`, `PVC`, `v0surf`, `DOB courier` all unexplained. |
| **`ROUND Rg1-never-rises-10-8 · BASELINE R14 · PLAYERS 804 · PLAYED — · DNP — · BOARD → · RELEASE —`** | Movers strip | Seven labels, four of which have no value at all. |
| **`§7.4`, `G-ATTR`, `Q-THEME`, `calibration gate`** | player card, trade desk | Internal spec references shown to a user. |
| **`DNP`** on every Movers row | Movers table | Harry Sheezel is labelled DNP while his own player card shows a Round 22 score of 96. Either the label is wrong or it means something other than "did not play". |
| **`slugs`** | DEBUG control | Turns on `harry-sheezel` strings. Decodable only by turning it on. |

**Failed views:** none outright — but the **`+2 yr` board lens is a failed state**, and the
**PLAYER CARD is a failed *tab*** (correct content, unreachable by its own navigation).

---

# PART 2 — THE CRITIQUE

## Visual

**Where it looks designed.** There is a real point of view here, and it is not accidental. Near-black
ground (`#0a0c16`), one acid volt-lime accent, a cyan→lime gradient on the value bars, letterspaced
uppercase micro-labels, a mono face for anything machine-generated, and a 4px lime rule down the
left edge of every panel. The condensed two-tone wordmark (VALUE in white / BOARD in lime) is
confident. The player card's stat row — VALUE / Δ VS LAST BAKE / RANK, three columns, huge figures,
tiny labels — is properly composed. The `MODEL CHANGE` badges in the weekly history are a
beautifully judged small detail. Someone with taste made decisions here.

**Where it looks machine-generated.** The masthead. Fifty characters of hex, a version string that
contradicts itself, and two badges nobody can read are given the top of every page. That's not
"technical aesthetic", that's a build log wearing a hat. The same instinct produces `§7.4`,
`G-ATTR`, `k=0 phantom=none` and `§2.viii seal c9e7491b` in user-facing copy. And the placeholder
panels — "renders the moment the export carries levers:[{label,delta}]" — are notes-to-self shipped
as product.

**Typography.** No webfonts at all: `Arial Narrow / Helvetica Neue Condensed / Roboto Condensed`
for display, `Helvetica Neue / Arial` for body, `ui-monospace` for data. Offline-safe, which I
respect, but the condensed stack is the most machine-variable font family in existence — this page
will look meaningfully different on a Mac, a Windows box, and a Linux box, and the wordmark is
built on it. There are also too many letterspaced uppercase micro-labels: `BOARD LENS`, `FILTER`,
`POSITION`, `TEAM LENS`, `ASSETS`, `DEBUG`, `ROUND 22 · 2026` all render at the same weight and
size in the same control bar, so the labels compete with the controls instead of subordinating
to them.

**Color.** The volt-lime is doing at least five jobs: active tab, active toggle, club name on every
row, positive delta, and the "OVERALL" column in Clubs. The footer legend claims *"volt = your
touch (reads · rules · controls)"* — a lovely rule — but the interface breaks its own rule
immediately by painting all 804 club names in it. When the accent is on a thousand elements it
stops being an accent.

**Spacing.** Rows are 8px-gapped bordered cards rather than table rows. It looks nice for ten rows
and is wrong for 804 — it costs about 30% vertical density on the app's primary artifact. The
Clubs and Player Card prose blocks run the full 1140px measure; at ~180 characters per line they
are close to unreadable, and both are load-bearing explanations.

## Information design

**Is the loudest thing the most important thing? No.** On the rankings row the brightest element is
the club name in lime; the second brightest is a cyan-to-lime gradient bar; the actual value —
the entire point of the application — is white text, smaller than the player name. Rank order is
already carried by vertical position, so the bar is redundant with the sort, while the number that
justifies the sort is the quietest thing in the row.

**Encoding.** The `VS TOP` bar is linear against the #1 value of 11,925. Harry Sheezel gets a full
bar; by rank 88 (2,411) every remaining bar is a visually identical 20% stub, and it stays that way
for **seven hundred more rows**. A bar that is the same length for 88% of the dataset is not
encoding anything. Direction and magnitude on deltas are handled well, though — signed pills,
▲/▼ glyphs, red/green, and an explicit note that rank movement is inverted so positive always
means improved. That note is exactly the right kind of care.

**Dead and duplicate columns.** `Δ VS ROUND` is an em-dash on all 804 rows — a whole column, in
prime position, holding nothing, and each dash is drawn inside a pill chip so the emptiness is
*emphasised*. `OVER FREE` is `VALUE − 190`, perfectly rank-correlated with the column two to its
left. Together they occupy roughly a fifth of the table width and carry approximately zero bits.

**Scannability.** No sticky column header on an 804-row list: by row 90 you have no idea what the
right-hand columns are. The rankings table is **not sortable**, while the Clubs table is —
inconsistent, and the sortable one is the one with 16 rows. All 804 rows render at once
(11,388 DOM nodes) with no pagination or virtualisation. The colour legend that explains the entire
visual encoding sits **at the very bottom, below all 804 rows**, where no user will ever see it.

**Two genuinely excellent pieces.** The Clubs "rank N of 16" caption under every stat, and the
Player Card weekly history with model-change rows inline. Both do the thing good information design
does: they give a number its context in the same glance.

## UX

**Navigation.** A `← BACK` button appears in the tab bar once you leave the first tab, and it pushes
all five tabs ~78px to the right. The navigation moves under the cursor as a side effect of using
it. There is also a top strip reading `WORKING AID · LIVE BOARD · READS · RULES · CONTROLS` that is
styled exactly like a menu and is not interactive at all — a false affordance in the first thing
you see. Nothing is sticky, so changing tabs from row 500 means scrolling to the top first.

**Flows I tried.**
- *Look up a specific player.* Failed. There is no global search. The PLAYER CARD tab has no picker.
  The only route is scrolling the master list.
- *Star a player to build "my reads".* Failed. The filter exists; the mechanism does not appear to.
- *Build a trade.* Succeeded, and felt good. But the typeahead dropdown renders inside the panel and
  is clipped by it — the second suggestion is sliced in half and the TOTAL OUT row is covered.
  Added assets have no visible remove control. And when I made the trade large, the plain-English
  translation broke: −11,376 SCAR was described as *"roughly a top-1 pick"*, when the app's own
  footer states pick 1 = 3,000. The best feature degrades silently outside its calibrated range.
  Also: *"roughly **a** early fourth-round pick"*.
- *Compare two weeks in Movers.* Succeeded, but every row was labelled DNP, including players whose
  own cards show scores for that round, while the DNP counter above read `—`.
- *Turn on `picks included`.* No visible change above the fold and no confirmation.

**States.** Filtering to Ruck + Free Agents left 4 rows and the footer helpfully said "rendering all
4 rows" — good. I never saw a zero-result state, a loading state, or an error state. One 404 fires
on load (a missing asset) with no visible consequence.

**Mobile at 390px.** This is the weakest surface.
- The masthead, nav and control panel consume roughly **830px** — more than one full viewport —
  before a single data row. The first thing a phone user sees is a wall of hashes and toggles.
- The control panel reflows into eight ragged rows where labels (`FILTER`, `POSITION`, `TEAM LENS`,
  `ASSETS`, `DEBUG`) end up *after* the controls they label, so `POSITION` sits to the right of the
  position dropdown and `DEBUG` to the right of the debug toggle. Every label is attached to the
  wrong thing.
- Rankings rows drop position, the value bar, OVER FREE and PICK·YR via `display:none` — real data
  removed with no way to get it back — while **keeping** the empty `—` pill. The responsive rule
  kept the only element carrying no information and discarded four that do.
- The Clubs table becomes a 911px-wide horizontal scroller inside a 366px window with **no scroll
  affordance** — no fade, no shadow, no cue. The club-name column takes 250 of the 366 available
  pixels, so the OVERALL figure is clipped mid-digit and six columns are invisible. A user will
  reasonably conclude the data isn't there.
- The Player Card stat row wraps so that "Δ VS LAST BAKE" breaks over two lines and its ▲ and its
  +3,809 land on separate lines.

**Where I hesitated.** Three times, and each is a design signal. (1) The masthead — I spent real
attention trying to parse `REALGUARD 5 PASS` before concluding it was two badges jammed together.
(2) The `Δ BASE bake|round` toggle — I clicked it, watched nothing change, read the adjacent note
saying it wasn't live yet, and stopped trusting the control bar. (3) The `+2 yr` lens — a screen
of accounting appeared above the table and I could not tell whether I had broken something.

---

## THE TEN CHANGES

1. **Delete the two dead columns (`Δ VS ROUND`, `OVER FREE`) and give the width to VALUE** — a table
   that shows 804 identical em-dashes teaches users to stop reading it. *(layout)*
2. **Make VALUE the loudest thing in the row and demote club name from lime to grey** — the number
   the app exists to produce should not be the quietest element on its own primary screen.
   *(styling-only)*
3. **Give the PLAYER CARD tab a player search** — a whole view is currently unreachable except by
   scrolling an 804-row list, which is the single largest functional gap in the product.
   *(structural)*
4. **Move the build hashes, version string and guard badges out of the masthead into a small
   provenance chip that expands on click** — reclaim the top of every page for the round, the
   player count and the mode. *(layout)*
5. **Rebuild the mobile rankings row as a two-line card that keeps position and the delta instead of
   the empty pill, and give every horizontally-scrolling table a visible edge fade** — right now
   phone users silently lose columns and don't know it. *(layout)*
6. **Sticky the table header and the tab bar, and paginate or virtualise past ~100 rows** — 804
   bordered rows with no header anchor is unnavigable by row 90. *(structural)*
7. **Replace the linear `VS TOP` bar with a log or percentile scale, or drop it** — it discriminates
   nothing across 88% of the dataset. *(styling-only)*
8. **Expand every unexplained token on first use — AFFL, SCAR, bake, GUARD, panel 10/10 — and move
   the footer colour legend to the top of the board as a one-line key** — the legend that decodes
   the whole visual language is currently below 804 rows. *(styling-only)*
9. **Hide unfinished machinery instead of describing it: remove the DEBUG toggle, the
   `bake|round` control that isn't live, the `§7.4 / levers:[{label,delta}]` placeholder, and the
   `+2 yr` reconciliation dump — or move all of it behind one explicit "diagnostics" switch.**
   *(structural)*
10. **Fix the trade-desk translator's out-of-range behaviour and the typeahead clipping, and add a
    remove control on staged assets** — the best idea in the app currently produces a wrong sentence
    ("roughly a top-1 pick" for 11,376 in a currency where pick 1 = 3,000) at exactly the moment a
    user tests it hardest. *(layout + logic)*

*Runners-up: resolve "16 clubs" vs "CLUB RANK 1 OF 17"; fix the universal DNP label in Movers; stop
the `← BACK` button from shifting the tab bar; cap prose blocks at ~70 characters; fix "a early".*

---

## Design direction

The instinct here is right and I would keep it: this should look like a **trading terminal, not a
sports website** — near-black, one accent, monospaced numerals, no illustration, no team logos,
information at high density and low decoration. What it needs is *discipline about hierarchy*,
which is the thing terminals actually get right and this doesn't yet. I would redesign toward a
strict three-tier type scale — one display size for the figure that matters, one text size for
names and labels, one micro size for provenance — and I would enforce that the accent colour is
spent on **exactly one thing per screen**: the number the user came for. Everything currently
wearing lime that isn't that number goes grey. The tables become true tables — tabular-lining
numerals, right-aligned, sticky headers, tight zebra banding instead of gapped cards, sortable
everywhere, and roughly 30% more rows per screen. Every metric earns its column by answering a
question the adjacent column doesn't. The engineering layer — hashes, guards, seals, phase notes,
spec sections — retreats entirely behind a single monospace provenance line at the foot of the
page, available to anyone who wants it and invisible to everyone who doesn't; the PUBLIC mode
already proves the product is better when that layer is gone, and the WORKING mode should borrow
its restraint. And I would push much harder on the one thing this app already does better than its
peers: **translating an abstract currency into a sentence a human can feel.** "You give up 280 —
roughly an early fourth-round pick" is worth more than every hash on the page. Build the whole
visual language around making that sentence, and the number behind it, the loudest thing in the
room.

---

## Contamination events

1. **Filenames seen, contents not read.** Listing `ui/` to find `index.html` exposed the names
   `README.md`, `PLAN.md`, `PLAN_v1.1.md`, `PLAN_v1.2.md`, `PLAN_v1.3.md`,
   `HOW_TO_UPDATE_INPUTS.md`, and a `screenshots/` directory. I opened none of them and did not
   look in `screenshots/`.
2. **One accidental read of an authoring comment.** While probing whether the top ribbon
   (`WORKING AID · LIVE BOARD · …`) was interactive, my selector matched the `<html>` element and
   returned its `outerHTML`, which included the `<head>`. That head contained a comment naming an
   internal theme-spec directory, calling the theme's lock "visual law", tagging the page as a tier
   that "never bakes; no value change", and describing it as a read-only "pure view" that "computes
   no price". This slightly de-blinded me on two points: it confirmed the dark-only palette is
   deliberate rather than incidental, and it hinted that "bake" is a pipeline term. I have set both
   aside — the "bake" decode failure above stands, because nothing in the *rendered interface*
   defines it, and my palette critique is about hierarchy, not about whether dark mode was chosen
   on purpose.
3. No other project documentation, no other reviewer's output, no GitHub, and no application source
   file was read.

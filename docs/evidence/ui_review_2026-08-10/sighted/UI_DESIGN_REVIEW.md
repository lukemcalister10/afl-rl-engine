# ValueBoard / Matchday UI — design review

**Standard applied** (the owner's words, issue #334): *"I'd love it if the interface looked like it'd
been designed by the best UI designers and web developers in the world. Not like AI. Like every part of
the information presentation was done with care and consideration for the aesthetics and the user
experience."*

**Method.** `ui/` served locally on port 8791 and driven with Playwright + the pre-installed Chromium.
Every view, every tier, every reachable state, at 1440px and 390px — 50 screenshots in
`screens/`. Computed styles, geometry, chart contents and focus rings measured in the live page;
contrast ratios computed from the actual tokens in `ui/styles/matchday.css`. Nothing in this document
is inferred from source alone unless it says so. **No repository file was written.**

**One-line verdict.** This is not a generic AI-generated app. It has a real point of view — a dark
"matchday" broadcast look, a single volt accent, tabular figures, honest fail-closed states, and a
Movers view whose information design is genuinely good. What it does not yet have is *discipline*: the
type has no scale, the accent colour has no single job, the labels fail contrast everywhere, the
ranking screen has no search and no sorting, the trade desk cannot be cleared, and the marquee section
of the player card prints a developer note where the story should be. It reads like a strong theme
executed feature-by-feature, which is exactly the gap between "competent" and "designed".

---

## 1. What the app is

**Stack.** No framework, no build, no bundler, no dependencies. `ui/index.html` loads seven generated
data bundles as `window.__…__ = {…}` script globals (board working + public, club valuation, ownership
sidecar, positions map, movers, movers transition), then fourteen plain IIFE modules under `ui/app/`
that hang off one `window.MD` namespace, then a single 549-line stylesheet
(`ui/styles/matchday.css`). Rendering is imperative DOM building (`MD.fmt.el` +
`innerHTML`); state is one object, `MD.state` (`ui/app/seam.js:90`); routing is
`MD.go(view)` re-rendering `#root` from scratch (`ui/app/main.js:126`). Dark-only by ruling
(Q‑THEME a). It runs from `file://` as well as from a server.

**Views.** Five tabs — **AFFL Rankings** (the 804-player board), **Clubs** (a sortable 16-club table
plus a hover "pocket profile" and per-club board pages), **Player card**, **Trade desk**, **Movers**
(weekly review). Each tab renders in two tiers, **Working** and **Public**, switched top-right.
`ownership.js`, `pocket.js`, `history.js`, `club_totals.js`, `counting.js`, `positions_data.js` are
not tabs; they are the ownership sidecar, the club hover panel, the card's weekly-history table, the
live club-total computation, the positional counting rule, and the values-free position map.

**Data flow.** Strictly one-way and read-only. `tools/extract_board_view.py` emits stamped, tiered
bundles; the browser authenticates them at boot (`MD.seam.ringFence`, `ui/app/seam.js:11`) by
comparing the board artifact's md5 head against the manifest's declared board id, and paints a
fail-closed screen if they disagree. The UI computes no price. Club totals are summed in the browser
from the board (`club_totals.js`) after a ruling that baked totals go stale.

**Existing intent, honoured.** The README's four ruled letters are all built as described: the
`OWNER OVERRIDE` tag with the pre-override figure one hover away, the Δ-base toggle, the plain-language
trade verdict, dark-only. The parked directive
`docs/directives/PRIORITY_UI_card_and_navigation.md` is substantially delivered: Round review is
retired; tabs carry titles + subtitles; Board is renamed "AFFL Rankings"; the universal Back control
exists and restores board filter state; the card's weekly history is real, with the model-change points
labelled and the score column correctly blank where the feed did not carry a player. **This review does
not re-litigate any of that.** Where I criticise something the directive specified, I say so.

---

## 2. Visual design audit

### 2.1 Typography

Three stacks, declared at `matchday.css:13-15`:

```css
--cond:"Arial Narrow","Helvetica Neue Condensed","Roboto Condensed",Arial,sans-serif;
--sans:"Helvetica Neue",Arial,sans-serif;
--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
```

**No typeface has been chosen.** All three are OS-fallback chains with no webfont and no self-hosted
file. On a Mac the product is Helvetica Neue + Arial Narrow; on Windows it is Arial + Arial Narrow; on
Linux and Android — where `Arial Narrow` does not exist — the "condensed" voice that carries every
player name, every tab, every label and the wordmark silently collapses to regular Arial/Liberation
Sans, and the design loses its only distinguishing letterform. That is the single biggest "this was not
art-directed" tell in the visual layer. The best-in-the-world standard starts with one real family.

**No type scale.** 41 distinct `font-size` declarations, with 26 uses of 11px, 22 of 10px, 19 of 12px,
and one-offs at **8.5px, 9px, 10.5px, 11.5px, 12.5px, 13px, 15px, 16px, 17px, 18px, 19px, 20px, 21px,
22px, 24px, 26px, 32px, 34px**. There is no ratio, no step set, no rhythm — sizes were picked
per-element. The visible result is that six different "small label" treatments (10px `.rowhead .h`,
10px `.card .clubs b`, 10.5px `.stamp`, 11px `.strip .lbl`, 11px `.seg button`, 11.5px `.viewtitle p`)
sit within a few hundred pixels of each other and read as accidental rather than as a hierarchy.

**Uppercase is doing everything.** `text-transform:uppercase` is applied to the banner, wordmark,
sub-brand, tabs, tier switch, view title, view subtitle, strip labels, segment buttons, the native
`<select>`s, column headers, player names (`.row .nm`, 19px/700 caps), positions, AFFL club names, card
name, card id line, section headings, trade pane headings, trade row names, the search input's typed
text, and every tag and badge. When everything shouts, nothing does — and long names suffer worst:
"NASIAH WANGANEEN-MILERA" wraps to two lines and pushes its row 20px taller than its neighbours
(`board_working_top_desktop.png`, rank 4). Caps also destroy the word-shape cue that makes a 804-name
list scannable. A designer would keep caps for micro-labels only and set names in sentence case.

**Numbers are handled well.** `.num{font-family:var(--mono);font-variant-numeric:tabular-nums}`
(`matchday.css:22`) is applied to values, ranks, deltas, over-free and history figures, so columns
align digit-for-digit; grouping is `toLocaleString("en-US")` with rounding to integer
(`ui/app/format.js:6`); movement uses a fixed arrow grammar `▲ +489 / ▼ −82 / — 0`
(`format.js:11`) so colour is never the sole carrier. This is the most professional part of the whole
visual system and should be preserved verbatim through any redesign.

**Rhythm.** There is no vertical rhythm unit. Section margins are `28px 0 12px` on `h2.sec`, `12px` on
`.strip`, `8px` on `.rows`, `16px` on `.desk`, `20px auto 40px` on `.card`, `13px/14px/16px/18px/20px/22px/24px`
paddings elsewhere. Nothing snaps to a 4px or 8px grid consistently.

### 2.2 Colour

Sixteen real hex values in the stylesheet (two more matches, `#139` and `#274`, are GitHub issue
numbers in comments). Thirteen are tokens; **three are not, and two of those duplicate tokens they sit
beside** — see the palette table in the Appendix. `#e06c6c` (`.ofree.belowfree`, `matchday.css:76`) is a
second red 6% away from `--dn:#f0655e`; `#7fe06a` (inside the `.vline` gradient) is a second green next
to `--up:#4ade80`; `#2bd4c8` teal and `#f0c24a` amber exist only inside that one gradient and appear
nowhere else in the language. That is palette drift, not a palette.

**The accent has no single job.** `--volt:#c8f04a` simultaneously means: the brand (`.brand b`), the
page banner, the *active* tab, the *active* segment button, the *selected* tier's underline, the AFFL
club name on every row (`.row .club .affl` — on 804 rows at once), the "picks value" and "overall"
figures in the Clubs table, the club-page rank, the trade **total** (whether the trade is good or bad —
`.ttotal .tfig{color:var(--volt)}`, `matchday.css:210`), the hot end of the value bar, the
`OWNER OVERRIDE` tag, the `MODEL CHANGE` tag, the left border of the strip, the verdict block and every
movers card *including the two negative ones*, plus every section heading's underline. A reader cannot
learn what volt means, because it means eleven things. In `movers_scrolled_mobile.png` the
"LARGEST VALUE **DECREASE**" card wears the same bright lime top rule as "largest increase", with a red
figure inside it — the frame and the content disagree.

**Semantic colour is otherwise sound**: `--up` green / `--dn` red are used consistently for direction,
always paired with an arrow glyph, and the fail-closed and movers-unavailable screens use a dedicated
alarm treatment (`state_movers_absent_desktop.png`) that is genuinely well made.

**Contrast is the serious failure.** `--faint:#525c6d` measures **2.71:1 on `--card`** and **2.53:1 on
`--card-2`** — below the 4.5:1 AA threshold for body text and below even the 3:1 large-text threshold.
And `--faint` is not a decorative colour: it carries **every column header** (`.rowhead .h`, 10px), the
rank number, the AFL club name, the pick·year meta, the over-free figure, the view subtitle, all strip
labels, all card section metas, the history table headers, the DNP tags, "OPEN ›" on the Clubs table,
and every footnote in the product. In other words, the entire labelling layer of the app is
unreadable-by-standard. `--dim:#8b95a6` at 6.04:1 is fine; the fix is mostly to stop using `--faint`
for text and keep it for hairlines.

### 2.3 Spacing, alignment, density

Alignment is better than it first looks: the board uses an explicit CSS grid whose column template is
shared by the header row and the data rows —
`grid-template-columns:48px 24px 1fr 62px 154px 88px 122px 106px 82px 74px` on both `.rowhead.working`
and `.row.working` (`matchday.css:70, 91`). That is a real grid and it holds.

Everything around it is ad-hoc:

- **Container widths disagree per view.** `.app{max-width:1180px}` but `.card{max-width:640px}`
  (`matchday.css:145`). Measured live: on a 1440px viewport the player card is 640px wide — the other
  800px of the screen is empty. The board is full-width; the trade desk is full-width; the card is a
  narrow column. Three different page shapes in one product.
- **Row density is a list, not a table.** Measured row height **55.6px**; with `gap:8px` and a
  1px border per row, 804 rows produce **51,202px of scrollable content** (document height 51,813px)
  and only ~8 rows visible per screen. A ranking of 804 players wants a trading-terminal density
  (32–40px), which would roughly halve the scroll and double the comparison set.
- **The control strip is a wrapping flex row, so labels detach from their controls.** `.strip` is
  `display:flex;flex-wrap:wrap` with the labels as ordinary siblings (`matchday.css:53`). At 1440px
  the word **FILTER** ends line 1 while its `all / my reads` control starts line 2, and **DEBUG** sits
  on line 3 alone (`board_controlstrip_desktop.png`). Change one control's content and the pairing
  re-shuffles — compare `board_working_top_desktop.png` with `board_deltabase_bake_desktop.png`, where
  flipping the Δ base moves *every* label to a different line. Seventeen controls live in that strip
  (measured), plus seven above it.
- **Radii and shadows are actually disciplined**: only `2px` and `999px` radii exist, and box-shadow is
  used exactly twice, both times for overlay elevation. Credit where due.
- **There are zero `transition` declarations in the stylesheet.** Every state change is a hard cut. The
  app feels like a document, not an instrument.

### 2.4 Iconography and affordances

There is no icon set — glyphs only: `★` pins, `▲ ▼ —` movement, `›` on "OPEN ›", `←` on Back, `■` on
error headings. That is a defensible choice for a data product and it is applied consistently. The
problems are the affordances that are *missing* or *lying*:

- **Row hover is invisible.** `.row:hover` moves the background `#12151c → #181c25` and the border
  `#232936 → #2c3446` (`matchday.css:96`) — a contrast change of about 1.15:1. On a row that opens a
  player card, that is no feedback at all (`board_row_hover_desktop.png`: row 4 is the hovered one).
- **Keyboard focus is invisible.** In 549 lines of CSS there is **no `:focus-visible` rule at all** —
  the only focus styling is `.pk-target:focus` (`matchday.css:448`) and one `outline:none` on the trade
  input. The measured computed focus on a tab button is `outline: rgb(16,16,16) auto 1px` — a near-black
  ring on a near-black page (`a11y_focus_ring_desktop.png`). With 804 focusable rows, keyboard use is
  effectively impossible.
- **The Clubs table's sort headers do not look sortable.** Only the active column shows an arrow
  (`clubs.js:39`); the other seven are visually identical to plain labels, with no hover, no cursor
  change declared, and no `aria-sort`.
- **A dead element on the trade desk.** `.trow .vline` renders at **0px width** (measured on all four
  rows). `.trow` is a flex row and `.vline` gets `position:relative;height:11px` with no `flex` or
  `width` (`matchday.css:198, 128`), so the comparison bar the desk was designed around does not exist
  on screen. Its `.vmask` is still positioned to a correct percentage — the code is right, the layout
  never gave it a size.

### 2.5 Where it reads as browser-default or "AI-generic"

1. **Native `<select>` dropped into a bespoke control bar.** `.strip select.boardsel`
   (`matchday.css:124`) restyles colour, border and type but leaves the operating-system control:
   the OS chevron, the OS focus ring, the OS option list, and — visibly — a different height and
   optical weight from the custom segmented buttons standing 6px away
   (`board_controlstrip_desktop.png`). Two selects on the board, two more on Movers. This is the single
   most recognisable "generated UI" signature in the app.
2. **The wall-of-prose explanation block.** The Clubs page opens with a ~100-word paragraph of
   semi-bolded specification text *above* the table (`clubs_working_desktop.png`); the pocket panel
   ends with an ~80-word footnote *inside a tooltip* (`clubs_pocket_hover_desktop.png`); the player card
   closes with a ~120-word note (`card_working_full_desktop.png`); the trade desk closes with a centred
   mono sentence about SCAR and the PVC. All of it is true and careful, and all of it is
   documentation pasted into the interface where a designer would have used a caption, an info
   affordance, or nothing.
3. **Developer stamps in the product masthead.** Every page, every tier of Working, prints
   `board v2.11-final-rc1-PROVISIONAL · engine c0a7e969 · store d9a24282 · board id
   4b448a821f54180182637983f7a26a9d` plus `REAL` and `GUARD 5 PASS` badges at 10.5px mono
   (`masthead_desktop.png`), and the player card repeats the same hashes a third time in its own head
   (`.card .cstamp`). On mobile this consumes 120px of the first screen. Provenance matters; a 32-char
   md5 at the top of a design product is a build artifact, not a design decision.
4. **Placeholders styled as content.** `.awaiting`, `.reserved` and `.translator` are dashed-border
   boxes holding sentences like *"renders the moment the export carries `levers:[{label,delta}]`
   (§7.4, G‑ATTR already requires these to exist)"* — printed in the **first and largest section of
   the player card**, under the heading "WHY THE PRICE IS WHAT IT IS".
5. **Dead columns rendered at full weight.** The board's "Δ vs round" column is `—` on all 804 rows in
   the shipped default; Public's "MOVEMENT" column is `— steady` on every row; the Public card's
   "Δ VS PREV ROUND" headline stat is `—`. Three columns of nothing, each occupying prime horizontal
   space, each with a fully-styled dashed pill drawing the eye to it.
6. **No table treatment on the one real table.** `.ctable` (Clubs) has no zebra, no row rule, no hover
   row highlight, no column-group separation, and no numeric emphasis besides two coloured columns —
   sixteen rows of unstructured figures (`clubs_working_desktop.png`).

---

## 3. Information-design audit

The product is a keeper-league valuation aid. For each view: what does the user arrive wanting, and how
fast does the screen answer?

### 3.1 AFFL Rankings — *"where does everyone sit, and who moved?"*

**Answers the first half well.** Rank, name, value and the value bar form a clean left-to-right read,
and the figures are tabular and comma-grouped. The board's honesty is exemplary: no fabricated numbers,
`—` where data is absent, arrows never relying on colour.

**It does not answer the second half at all, by default.** `MD.config.DELTA_BASE_DEFAULT` is `"round"`
(`ui/app/config.js:27`) — and Δ-vs-round data does not exist yet; the strip says so in its own label
(*"· Δ vs round arrives with the weekly loop (Phase 3)"*). So the shipped default renders **804 empty
dashes** in the movement column. Click `bake` and the same column fills with real, useful chips
(`board_deltabase_bake_desktop.png`: `▲ +3,809`, `▲ +3,046`, `▲ +2,547`…). The app ships pointed at the
empty option. This is the single cheapest high-impact fix in the review.

**What is loudest vs what matters.** The loudest things on a row are the 19px uppercase **name** and the
19px mono **value** — correct. Third loudest is the **volt AFFL club name**, repeated 804 times in the
brightest colour on the page; on a club-filtered page it is the *same club name* repeated 48 times
(`club_profile_desktop.png`). Meanwhile "Over free" — a column that is literally `value − 190` for every
row, so it is perfectly rank-correlated with the value column beside it and adds no information above
about rank 550 — occupies a full column at every width.

**The value bar's encoding is broken below the top of the list.** The track is a fixed **122px** for
every row and the fill is `value / maxValue` linear (`format.js:24`, `matchday.css:128`). Measured
mask positions: rank 1 fills 121px, rank 20 fills 49px, rank 100 fills 23px, **rank 400 fills 3.8px**.
For 90% of the board the bar is a stub. Worse, the track paints a five-stop rainbow
(`#3b4a5e → #2bd4c8 → #7fe06a → #c8f04a → #f0c24a`) that the mask reveals — so hue and length encode the
same variable twice, in a ramp that is not perceptually uniform and that reads as *categorical* (teal
players vs lime players vs amber players) to anyone scanning quickly. One desaturated bar on a
rank-relative or square-root scale would say more with less.

**Missing instruments.** There is **no player search** anywhere on the board — 804 rows, 51,202px of
scroll, and the only way to find a name is the browser's own Ctrl-F (which fails past the rendered
viewport is irrelevant here since all 804 render, but still leaves no in-product path). There is **no
column sorting**: the order is value-descending, permanently. You cannot ask "who is cheapest above the
free line?", "which key defenders are top-100?", "who was taken in the first round and is now outside
the top 300?" — all questions this data can answer and this screen cannot. The header row is **not
sticky**, so after eight rows you are reading unlabelled numbers (`board_working_scrolled_desktop.png`).

### 3.2 Clubs — *"who has the strongest list, and why?"*

The table is the best-organised surface in the product: eight sortable columns, a sensible default
(Overall, descending), one canonical currency, an honest footnote about what Non-Best-23 means. The
figures are right-aligned and tabular.

What it lacks is **magnitude**. Sixteen clubs and seven metrics, all rendered as bare numerals; nothing
shows that West Coast (67,751) is 2.3× Port Adelaide (29,061), or that Hawthorn's 23,894 in picks is an
outlier by a factor of two. A single in-cell bar or a column-normalised heat treatment on one or two
key columns would turn a lookup table into a comparison.

The **pocket profile is the most direct UX defect in the app**. Hovering a club name opens a ~640px-tall
panel that (a) is positioned over the masthead and the page title, (b) covers the five table rows below
its trigger, and (c) **intercepts pointer events on its own trigger row** — Playwright's actionability
checks failed twice with `<div class="pk-foot">… intercepts pointer events`, meaning a real user who
hovers a club then reaches for that row's "OPEN ›" link cannot click it. Inside the panel, thirteen
metrics with `%`, `vs avg` and `×` columns are genuinely useful and genuinely well laid out — this is
a *panel*, not a tooltip, and it should be one.

On the club board page there are **two denominators for the same fact within 40px**: the summary strip
prints `rank 1 of 16` (`board.js:181`, over `ct.clubs.length`) and the banner immediately below prints
`CLUB RANK 1 OF 17` (`board.js:132`, over `Object.keys(clubRanks).length`, which counts the Free Agents
pool). The page also states the same six figures twice, once in `.clubsummary` and again in
`.clubbanner` (`club_profile_desktop.png`).

### 3.3 Player card — *"why is he worth this, and where is he going?"*

The card has the right story arc on paper — identity → value/Δ/rank → **why** → trajectory → form →
history — and its **weekly history table is excellent work**: fourteen points, value/rank/positional
rank each with a signed delta, model-change points visually separated and tagged, scores shown where
recorded and *blank* where the feed did not carry them, with the reasoning stated. That is careful,
honest information design of exactly the kind the owner asked for.

Everything above it underdelivers:

- **The "why" section is empty and speaks in code.** Under the card's largest heading sits
  `.awaiting`, whose text is: *"PER-LEVER ATTRIBUTION — the full 'why the price is what it is'
  waterfall … renders the moment the export carries `levers:[{label,delta}]` (§7.4, G-ATTR already
  requires these to exist)."* The waterfall CSS exists (`.wf`, `matchday.css:170-186`) and is well
  designed. Until the data lands, the card's headline promise resolves to a spec note.
- **Both charts are undimensioned.** Measured: each SVG is 568×148 and contains **five text nodes
  total** — year labels on one, `s1 s2 s3 s4` on the other. No y-axis, no value labels, no gridline, no
  baseline, no units. The "Recent form" line could be showing scores of 96–180 or 9.6–18.0; nothing on
  screen says. Two charts drawn in the identical style, same colour, same height, mean the eye reads
  them as the same measurement.
- **The headline stat row disagrees with the board.** The board's Δ toggle says "round" while the card
  says "Δ VS LAST BAKE" (Working) or "Δ VS PREV ROUND — `—`" (Public). The card ignores the toggle.
- **60% of the desktop screen is empty** beside a 640px card.

### 3.4 Trade desk — *"is this trade good?"*

**The verdict is the best single piece of information design in the product.** `−280 SCAR` in red,
then one plain sentence — *"You give up 280 — roughly a early fourth-round pick (≈ pick 57)"* — then
the ★-read footnote. Translating an abstract currency into a draft pick the owner already has intuition
for is exactly right, and it satisfies Q‑VERDICT (b) properly. (Typo: *"a early"*, from the
`early/mid/late` descriptor in `trade.js:describePick`.)

Around it, the desk is unfinished as an instrument:

- **You cannot remove anything.** The desk seeds a demo trade on open — Max Gawn + Pick 24 for Kieren
  Briggs + Pick 5 (`trade.js:9-19`) — and there is **no removal path in the module at all** (no delete
  button in `.trow`, no click handler, no clear control; measured: 0 removable controls). Every
  addition is permanent for the session. The first thing a real user does is try to clear the example,
  and there is no way to do it.
- **The totals are volt whether you win or lose.** `.ttotal .tfig{color:var(--volt)}` — so a losing
  trade shows both totals in the "good" accent while the verdict below shows red.
- **The comparison bars do not render** (0px, §2.4). Each side is therefore a list of numerals with a
  sum, and the eye must do the comparison the design intended to do for it.
- **The search dropdown is a half-overlay.** With one result showing, the "TOTAL OUT" line is visible
  *through and around* it and the two collide illegibly (`trade_search_open_desktop.png`).
- Typed text is force-uppercased (`text-transform:uppercase` on the input), so the user's own typing
  does not look like typing.

### 3.5 Movers — *"what changed this week?"*

Structurally the strongest view: a from/to range, five preset lenses, four highlight cards (largest
value increase / decrease / rank improvement / decline), then a filtered, well-encoded table with
Δ value, Δ%, Δ rank and Δ positional rank. The direction-and-magnitude encoding is proper: signed
figure + arrow glyph + colour, never colour alone.

Its problems are about defaults and grouping:

- **The default range compares two model re-cuts, not two weeks of football.** It opens on
  `10/8 DOB COURIER + V0SURF RE-CUT → 10/8 NEVER-RISES RESTORE (R12)`, and the view says so honestly in
  its own note. The consequence: the "largest value increase in the league" is **+24 (+1.6%)**, every
  row is marked **DNP**, and a screen titled *Weekly Review* shows a week in which nothing happened
  (`movers_top_desktop.png`). The right default is the most recent *round-to-round* pair.
- **The "Value risers" preset shows 53 non-risers.** Measured on the default range: 60 rows displayed,
  of which only 7 have a non-zero Δ; the rest read `— 0` and `0.0%` (`movers_filter_dnp_desktop.png`
  shows the same shape). A preset should not return rows that contradict its name.
- **The controls for one table are split across 270 vertical pixels**, with the metadata strip and the
  four cards in between: range + presets at the top, club/position/played filters below the cards.
- **Three deltas, three treatments.** Δ value is a filled chip, Δ% is bare text, Δ rank is a chip
  again, Δ pos is bare text. Same family, four visual weights.
- The metadata strip prints raw slugs (`ROUND Rg1-never-rises-10-8 BASELINE Rdob-courier-10-8 … PLAYED —
  DNP — BOARD → RELEASE —`) at 10px `--faint`. It is provenance, and it is presented as a headline.

---

## 4. UX audit

**Navigation model.** Five tabs, always visible, active tab filled volt — location is obvious and the
model is the right one for five views. The universal Back control (`main.js:91-106`) is well built: it
pushes the *whole* location including board filter state, refuses to render when there is nowhere to go,
and names its destination in a `title`. Two flaws: the Back button appears and disappears as the stack
empties, so the tab row shifts horizontally by ~90px between renders; and there is no URL — no
deep-linking, no browser Back, no refresh-safety, no shareable link to a player. For a viewer whose main
job is "look at this player", the absence of a hash route is a real cost.

**Card open/close.** Clicking a row opens the card, `window.scrollTo(0,0)` fires, Back returns to the
board *with the filter restored*. Correct behaviour. But the card is a full page swap rather than an
overlay, so comparing two players means board → card → Back → board → card, four navigations and two
full re-renders, with no memory of where you were in a 51,000px scroll (the scroll position is reset,
though the filter is kept).

**Trade flow.** Two panes, type-ahead in each, verdict below — a good two-step shape. In practice it is
one step forward and none back: pre-seeded, un-removable, un-clearable (§3.4). There is also no
indication that picks and players share one currency until you read the 10px footnote.

**Search / filter ergonomics.** The board's filters are position, club, "my reads", assets, group-by,
lens, Δ base, debug — eight controls, all discrete, none of them a search. Movers adds club/position/
played. The Clubs table has sortable columns and no filter. **The only free-text input in the entire
product is the trade desk's add-asset box.** For an 804-row database this is the largest ergonomic gap.

**States.** Loading: none needed — data ships as inline scripts, and the first paint is complete
(no spinner, no flash, no layout shift measured). Error: **very good**. Corrupting the board stamp
produces a dedicated fail-closed screen that names the reason and prints got/want
(`state_failclosed_desktop.png`); removing the movers bundle produces a red-bordered "MOVERS
UNAVAILABLE — INTEGRITY CHECK FAILED" panel with `reason: no movers bundle`
(`state_movers_absent_desktop.png`). Two caveats: neither offers an action (no "go back", no
"what to do next"), and on the movers failure the masthead one row above still displays green
`REAL` and `GUARD 5 PASS` badges — the page contradicts itself. Empty: filtering the board to a
two-player result renders correctly but with no count and no "no results" copy path exercised;
Movers' presets return rows that do not match the preset (§3.5).

**Keyboard and scroll.** Focus is invisible (§2.4) — the blocking accessibility issue. Rows are real
`<button>`s, so they are reachable and activate on Enter, but with 804 of them and no skip link, no
search and no visible ring, keyboard operation is theoretical. There is no `Esc` handler on the search
dropdown or the pocket panel. Scrolling is native and smooth; the two horizontally-scrolling regions
(`.histwrap`, `.tablewrap`) correctly scroll inside themselves rather than the page — good — but neither
shows a scroll affordance.

**Mobile (390px).**
- **Nothing above rank 1 is data.** Measured on desktop the first row starts 473px down; at 390px the
  banner, wordmark, four lines of hashes, Back, a two-row tab bar, the tier switch, the page title and
  a full-screen control strip come first — the first player is roughly two screens down
  (`board_working_top_mobile.png`).
- **The wrong columns survive.** At 390px the board drops position, the value bar, over-free and
  pick·year, but **keeps the empty `—` movement pill**. Position is a primary attribute in a keeper
  league; it is gone, and a dashed placeholder is not.
- **Movers rows lose their labels.** The header row is hidden at narrow widths but the row keeps four
  numbers, so a mobile row reads `1,476` then `▲ +24 +1.6%` then `▲ +2` with nothing naming any of
  them (`movers_scrolled_mobile.png`).
- **The Clubs table clips.** Values are cut mid-digit at the right edge with no gradient, shadow or
  "scroll →" hint (`clubs_working_mobile.png`).
- **The card's stat row breaks.** "Δ VS LAST BAKE" wraps to two lines and its arrow and figure stack
  onto two more, so the three stats no longer share a baseline (`card_working_top_mobile.png`).
- **The pocket panel is a hover panel on a touch device.** It opens on tap, covers most of the screen,
  and blocks the row beneath it.
- Five breakpoints are in use (360, 480, 480, 560, 720, 920) — written inconsistently as both
  `@media(max-width:480px)` and `@media (max-width:480px)` — with no shared set.

---

## 5. The verdict — ten changes, ranked by impact

| # | Change | Why (one sentence) | Effort | Views touched |
|---|---|---|---|---|
| 1 | **Retire `--faint` as a text colour.** Replace it with a token at ≥4.5:1 (around `#7d8798` on `--card`) and keep `#525c6d` for hairlines only. | Every column header, unit label, footnote and secondary figure in the product currently sits at 2.5–2.9:1 and is unreadable by standard — this one token failure makes the whole labelling layer look unfinished. | CSS-only | All |
| 2 | **Choose and self-host one real type family, on one scale.** A grotesk with a genuine condensed cut and true tabular figures, plus the existing mono; collapse 41 ad-hoc sizes to a 7-step scale; drop caps from names and keep them for micro-labels only. | The product currently has no typeface — three OS fallback chains that render differently on every platform and lose the condensed voice entirely on Linux/Android — and no hierarchy, which is the loudest "not art-directed" signal in the design. | Layout (CSS + a font file) | All |
| 3 | **Give the ranking a search field and sortable columns, and make the header sticky.** | 804 rows and 51,202px of scroll are currently navigable only by scrolling, in one fixed order, with the column labels off-screen after eight rows — the product's central table cannot answer most of the questions its own data holds. | Structural | Board, club pages |
| 4 | **Ship the Δ base that has data, and delete the columns that have none.** Flip `DELTA_BASE_DEFAULT` to `"bake"`; remove Public's "Movement" column and the Public card's Δ stat until round deltas exist. | Three columns currently render nothing but dashes across every row in the shipped default, while the same space filled with real movement is one click away. | CSS-only + one config line | Board, card |
| 5 | **Finish the trade desk: removable rows, a Clear control, an empty state, and real comparison bars.** | The desk opens on a demo trade that cannot be deleted, has no reset, and its value bars compute to 0px — the one tool with a genuine decision at the end of it cannot be operated. | Layout + structural | Trade |
| 6 | **Rebuild the control strip as a labelled toolbar with each label bound to its control**, replace the two native `<select>`s with the app's own control, and collapse it behind a "Filters" affordance on mobile. | Labels detach from their controls whenever the row wraps, seventeen controls compete at equal weight, the OS dropdowns are the app's most visible generic tell, and on a phone the strip costs an entire screen before a single player. | Layout | Board, Movers, Clubs |
| 7 | **Re-cut the value bar: one desaturated fill, rank-relative or square-root scale, no hue ramp.** | Below about rank 60 the current bar is a 4px stub, and its five-stop rainbow encodes the same number a second time in a ramp that reads as categorical rather than continuous. | CSS-only | Board, club pages, trade |
| 8 | **Give the player card its story back:** land the lever waterfall (or replace the spec note with a plain-English summary of the drivers), put axes, units and value labels on both charts, differentiate them visually, and widen the card to use the page. | The card's largest heading — "why the price is what it is" — currently resolves to a developer note about `levers:[{label,delta}]`, and the two charts beneath it carry five text labels between them and no scale. | Layout / structural | Card |
| 9 | **Make interaction visible:** a real `:focus-visible` ring, a hover state with genuine contrast, cursor and `aria-sort` on sortable headers, and short transitions on state changes. | There is no focus styling in 549 lines of CSS, and the hover on a clickable row changes contrast by about 1.15:1 — the app gives almost no feedback that it is interactive. | CSS-only | All |
| 10 | **Fix the mobile priority order and turn the pocket tooltip into a dismissible panel.** Keep position over the dead delta pill, label the Movers figures, hint the horizontal scroll, and stop the panel covering and blocking its own trigger. | At 390px the board hides a primary attribute while keeping an empty placeholder, Movers rows become unlabelled numbers, and the club panel physically prevents the click it invites. | Layout | Board, Movers, Clubs |

### Design direction

Aim at a **broadcast-grade data terminal**, not a dashboard: the current theme is already reaching for
this and should be pushed the rest of the way rather than replaced. Commit to **one typeface family**
with a true condensed cut and real tabular figures, self-hosted, on a seven-step scale where names sit
in sentence case at one clear size, figures sit in the mono at one clear size, and *everything else* is
one small letter-spaced label style — so the page has exactly three typographic voices instead of
twenty. Keep the near-black ground and the volt accent, but **give volt one job**: the user's own
position — what is selected, what is filtered, what is "now". Move club identity, section rules,
totals and tags to the neutral ramp, and reserve green/red strictly for direction, always with the
existing arrow grammar so colour is never load-bearing. Encode magnitude with a single desaturated
bar on a scale that still says something at rank 400 — never with hue. Then raise the density: hairline
rules instead of bordered cards and 8px gaps, rows near 36px, a sticky header, and generous space
around the *page* rather than inside every row, so a screen shows twenty players instead of eight and
the eye compares instead of scrolling. Finally, **move the explanation out of the layout**: the
provenance stamps, the counting-rule essays and the coverage caveats are the product's conscience and
should stay in it — but as a footer, an info affordance and progressive disclosure, not as the first
paragraph of a page. The result should read the way a good broadcast graphics package reads: quiet
ground, one accent, ruthless hierarchy, and figures you can trust at a glance.

---

## 6. Appendix

### 6.1 Screenshot index — `UI_REVIEW/screens/` (50 files)

**Board (AFFL Rankings)**
| File | What it shows |
|---|---|
| `board_working_top_desktop.png` / `_mobile.png` | Default view, Working tier — the shipped state |
| `board_working_scrolled_desktop.png` / `_mobile.png` | Scrolled — header gone, bars flat, mobile column drops |
| `board_controlstrip_desktop.png` | The control strip, isolated — label/control detachment, native selects |
| `masthead_desktop.png` | The masthead, isolated — md5 stamps and badges |
| `board_public_top_desktop.png` / `_mobile.png` | Public tier — "Movement" column dead on every row |
| `board_deltabase_bake_desktop.png` | Δ base = bake — the same column full of real data |
| `board_lens_plus1_picks_desktop.png` / `_mobile.png` | +1yr lens with picks included |
| `board_group_by_club_desktop.png` / `_mobile.png` | Grouped by club |
| `board_filter_myreads_desktop.png` / `_mobile.png` | "My reads" filter |
| `board_filter_narrow_desktop.png` | Narrow filter (Ruck + one club) → 2 rows |
| `board_debug_slugs_desktop.png` / `_mobile.png` | Debug slugs on |
| `board_row_hover_desktop.png` | Row 4 hovered — the near-invisible hover state |
| `a11y_focus_ring_desktop.png` | Keyboard focus on a tab — effectively no ring |

**Clubs** — `clubs_working_desktop.png` / `_mobile.png` (table + intro wall, mobile clipping),
`clubs_pocket_hover_desktop.png` / `_mobile.png` (the pocket panel covering the page and its trigger),
`club_profile_desktop.png` / `_mobile.png` (club board page, duplicate banner, 16-vs-17 denominators).

**Player card** — `card_working_top_desktop.png` / `_mobile.png`,
`card_working_full_desktop.png` / `_mobile.png` (the `.awaiting` "why" block, both charts, the weekly
history table), `card_public_full_desktop.png` / `_mobile.png` (Public parity; Δ stat empty),
`card_from_board_row_desktop.png` / `_mobile.png` (opened by clicking a board row).

**Trade** — `trade_default_desktop.png` / `_mobile.png` (seeded demo trade, verdict block),
`trade_search_open_desktop.png` / `_mobile.png` (dropdown colliding with the total),
`trade_after_add_desktop.png` / `_mobile.png`.

**Movers** — `movers_top_desktop.png` / `_mobile.png`, `movers_scrolled_desktop.png` / `_mobile.png`
(mobile rows without labels), `movers_filter_dnp_desktop.png` / `_mobile.png`.

**States** — `state_failclosed_desktop.png` / `_mobile.png` (ring-fence rejection),
`state_movers_absent_desktop.png` / `_mobile.png` (movers bundle missing),
`state_clubvaluation_absent_desktop.png` (club-valuation bundle missing).

### 6.2 Palette inventory and contrast

All values extracted from `ui/styles/matchday.css`. Ratios computed against the surface each colour is
actually used on. **Bold = fails WCAG AA.**

| Token / literal | Hex | Role | On surface | Ratio | AA body (4.5) | AA large (3.0) |
|---|---|---|---|---|---|---|
| `--pitch` | `#0a0c10` | page ground | — | — | — | — |
| `--card` | `#12151c` | row / panel ground | — | — | — | — |
| `--card-2` | `#181c25` | raised ground, hover | — | — | — | — |
| `--edge` | `#232936` | borders | on `--card` | 1.25 | n/a (non-text) | n/a |
| `--text` | `#f2f5f9` | primary text | `--card` | 16.70 | pass | pass |
| `--text` | `#f2f5f9` | primary text | `--pitch` | 17.90 | pass | pass |
| `--dim` | `#8b95a6` | secondary text | `--card` | 6.04 | pass | pass |
| `--dim` | `#8b95a6` | secondary text | `--pitch` | 6.47 | pass | pass |
| **`--faint`** | **`#525c6d`** | **all labels, headers, meta, footnotes** | **`--card`** | **2.71** | **FAIL** | **FAIL** |
| **`--faint`** | **`#525c6d`** | same, on raised panels | **`--card-2`** | **2.53** | **FAIL** | **FAIL** |
| **`--faint`** | **`#525c6d`** | same, on page ground | **`--pitch`** | **2.90** | **FAIL** | **FAIL** |
| `--volt` | `#c8f04a` | accent (11 different jobs) | `--pitch` | 14.93 | pass | pass |
| `--volt` | `#c8f04a` | accent | `--card` | 13.93 | pass | pass |
| `--pitch` on `--volt` | `#0a0c10`/`#c8f04a` | active tab / segment | — | 14.93 | pass | pass |
| `--volt-soft` | `rgba(200,240,74,.12)` | banner ground, model-change row | — | — | — | — |
| `--up` | `#4ade80` | positive movement | `--card` | 10.48 | pass | pass |
| `--dn` / `--alarm` | `#f0655e` | negative movement, alarm | `--card` | 5.85 | pass | pass |
| `--dn` | `#f0655e` | same | `--pitch` | 6.27 | pass | pass |
| *(untokenised)* | `#e06c6c` | `.ofree.belowfree` — a **second red** 6% from `--dn` | `--card` | 5.68 | pass | pass |
| *(untokenised)* | `#2c3446` | row hover border | `--card-2` | ~1.2 | n/a | n/a |
| *(untokenised, in `.vline`)* | `#3b4a5e` | bar ramp stop 1 | on `--edge` fill | 1.61 | n/a | n/a |
| *(untokenised, in `.vline`)* | `#2bd4c8` | bar ramp stop 2 — teal, used nowhere else | — | — | — | — |
| *(untokenised, in `.vline`)* | `#7fe06a` | bar ramp stop 3 — a **second green** near `--up` | — | — | — | — |
| *(untokenised, in `.vline`)* | `#f0c24a` | bar ramp stop 5 — amber, used nowhere else | — | — | — | — |

**Size: 16 distinct colours** (13 tokens + 3 untokenised literals; the `.vline` ramp contributes 4 stops
of which 3 exist only there). **Worst failure: `--faint #525c6d` on `--card-2` at 2.53:1** — 44% short
of AA body text — carrying the app's entire label layer.

**Other measured inventory**
- Border radii: 2 values (`2px`, `999px`) — disciplined.
- Box shadows: 2 declarations, both overlay elevation — disciplined.
- Transitions: **0**.
- `font-size` declarations: **41 distinct values**, 8.5px–34px.
- Breakpoints: 5 (360, 480, 560, 720, 920), inconsistently written.
- Focus rules: 1 (`.pk-target:focus`); `:focus-visible`: **0**.

### 6.3 Measured geometry

| Measurement | Value |
|---|---|
| Board row height | 55.6px |
| Board rows rendered | 804 (all, no virtualisation) |
| Board rows container height | 51,202px; document 51,813px |
| First data row top | 473px (desktop, 1440×1000) |
| Controls before data | 17 in the strip + 7 above it |
| `vs top` bar track | 122px fixed |
| `vs top` fill: rank 1 / 20 / 100 / 400 | 121px / 49px / 23px / **3.8px** |
| Player card width @1440 viewport | 640px (44% of the screen) |
| Card chart SVGs | 568×148, **5 text nodes total across both** |
| Trade-desk `.vline` width | **0px** on all rows |
| Trade-desk removable controls | **0** |

### 6.4 What I could not render or verify — stated honestly

- **A loading state does not exist to capture.** The data ships as inline `<script>` bundles, so the
  first paint is already complete. There is no spinner, skeleton or progressive state in the code, and
  none appeared at any throttle I observed. Reported as "none", not as "not found".
- **Three failure states were reached only by rewriting the HTTP response in the browser**
  (Playwright request interception): the ring-fence rejection (board stamp altered in flight), the
  movers-absent panel (bundle blocked), and the club-valuation-absent path. These are faithful to what
  the code does, but they are induced states, not naturally occurring ones. **No repo file was changed
  to produce them.**
- **The lever waterfall (`.wf`) could not be seen with data.** The shipped export carries no `levers`
  field, so the card renders `.awaiting`. I read and assessed the CSS, but I have not seen the
  waterfall rendered and make no claim about how it looks in practice.
- **The `OWNER OVERRIDE` tag and its hover were not observed live.** The README states zero overrides
  are currently active, and none appeared on any of the 804 rows.
- **The `+1 yr` / `+2 yr` forward lenses** carry a `lensoff` disabled treatment in CSS; I captured the
  `+1 yr` state but did not verify whether phantom pick lines (`lensPicks`) are populated in the
  shipped bundle.
- **Public-tier Movers and Public-tier Trade** were captured only incidentally; my Public-tier
  screenshots concentrate on Board and Card, which is where the tier differences are specified.
- **No touch-device emulation** — the 390px captures are a narrow desktop viewport, so `:hover`-only
  behaviours (the pocket panel) may differ on a real phone. I have flagged the pocket panel as a
  hover-on-touch risk rather than asserting how iOS resolves it.
- **Cross-platform font rendering is inferred, not measured.** The headless Chromium here resolves
  `Arial Narrow` to a fallback. I verified the stack in CSS and the computed `font-family` string; I did
  not screenshot the app on macOS or Windows.
- The pocket panel's pointer-event interception is asserted from **two independent Playwright
  actionability failures** naming `<div class="pk-foot">` and `<td class="pk-lbl">` as the intercepting
  elements — a stronger form of evidence than a screenshot, but not a human-hand test.

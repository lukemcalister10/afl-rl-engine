# Three treatments of the board view — what each one is, and what it costs

**Read this beside `contact_sheet.html`.** Everything below describes pixels you can look at.
All three treatments render the real board: 804 players, real names, real values, real clubs, real
movement since the last bake, pulled live out of the app. No placeholder text, no invented numbers.

---

## The problem all three are solving

**The problem.** The board is the product. It is 804 players long, and today you can see eight of them
at a time on a big screen and six on a phone — and on a phone the first player is 829 pixels down, past
a wordmark, four lines of build codes, two rows of tabs and a full screen of filters. The whole list is
51,813 pixels tall. There is no search box. The column headings scroll away. The bright green means
eleven different things at once, so it has stopped meaning anything. The bar beside each value is a
4-pixel stub for nine players out of ten. And the movement column ships pointed at data that does not
exist yet, so it prints 804 dashes.

**Why it matters.** None of that is a bug. Each piece works. But together they mean the screen answers
"who is the most valuable player" and almost nothing else — you cannot find a player, cannot compare
a group, cannot see enough of the list at once for your eye to do the work instead of your scroll wheel.

**The trade-off, up front.** All three treatments buy density and speed by giving up decoration: no
bordered cards, no gradients, no shouting. All three make names sentence-case rather than capitals,
which some people read as "less impactful" until they try to find a name in a list of 804. All three
move the build codes off the top of the screen into one line at the very bottom — the provenance is
still there, it is just no longer the first thing you see.

**What is fixed in all three, as a floor:**

- Real self-hosted typefaces, embedded in the file — the same on your Mac, a Windows machine and a phone.
- One accent doing exactly one job. Green and red only ever mean up and down, and always carry an arrow,
  so colour is never the only signal.
- A real table: right-aligned figures on tabular numerals, a sticky header that never scrolls away,
  hairline rules, and twenty-plus players on one screen.
- A value bar that still says something at rank 400 instead of dying at rank 60.
- Search, position and club filters, all as the app's own controls — no operating-system dropdowns.
- On a phone: position, club, value and movement all survive; the first player is roughly 150px down.
- Designed hover and keyboard-focus states, both visible in the contact sheet.

---

## Treatment 1 — **Broadcast**
`treatment_1_broadcast.html`

**What this voice is.** The Friday-night football graphics package. Near-black, condensed lettering,
figures in a single mono, hairline rules and nothing else. It is built for one job: reading down a
ranked list as fast as your eye can move. If the current app has a personality, this is that personality
finished properly rather than replaced.

**The five choices that make it feel designed**

1. **Typeface — Barlow Condensed for words, JetBrains Mono for figures.** Two families, no more.
   Condensed letterforms buy about 15% more name in the same column, which is why broadcast graphics
   have used them for fifty years. Every number in the product is monospaced and column-aligned.
2. **Scale — seven sizes, nothing else.** 10.5 / 12 / 13.5 / 15 / 17 / 22 / 30. The current app uses
   41 different sizes; six of them are "small grey label" within a few hundred pixels of each other.
   Here there are exactly three typographic voices: the name, the figure, and one small letter-spaced
   label used for everything else.
3. **Accent — volt means "you".** The chosen tier, the chosen filters, the keyboard focus ring. That is
   the whole list. Club names, totals, section rules and tags all move to plain grey. You can learn what
   the green means in one second and then trust it.
4. **Density — 34px rows, 25 players on a 1440 screen.** No card borders, no gaps between rows, one
   hairline between them. The whole list drops from 51,813px to 27,595px of scroll.
5. **Value encoding — square root of the share of the top price**, with two hairlines on the track
   marking where the 100th and the 300th player sit. Rank 1 fills the bar, rank 25 fills 62%, rank 400
   still fills 18%. The reference marks show on the part of the track a player has *not* reached, which
   is exactly where a reference mark earns its keep.

**Trade-off.** Condensed type is the least forgiving of the three at small sizes — it wants a good
screen. And volt-as-selection means the value itself is never highlighted; the biggest number on the row
is simply the biggest number on the row.

**Effort to build for real: CSS-only, plus two font files.** The row is already a CSS grid with a shared
column template, which is the hard part and it is already right. This is a stylesheet swap, a search
box, and one config line to flip the movement column to the base that has data.

---

## Treatment 2 — **Terminal**
`treatment_2_terminal.html`
**What this voice is.** A financial terminal. Ruled in both directions, boxy, deliberately dense, and
information-maximal: fifteen columns, a live statistics rail across the top, and 32 players on a screen.
It assumes you already know the vocabulary and would rather have the number than the explanation. This
is the one for the person who has the board open all evening.

**The five choices that make it feel designed**

1. **Typeface — IBM Plex Sans Condensed for words, IBM Plex Mono for figures.** One family, two cuts,
   drawn as a system. Plex Mono is narrow enough to carry a lot of figures in a small column without
   ever losing digit alignment.
2. **Scale — six sizes, terminal-tight**: 9.5 / 10.5 / 11.5 / 12.5 / 14 / 19. Nothing on the screen is
   bigger than 19px including the wordmark, because in this voice nothing gets to shout.
3. **Accent — amber means "the axis".** The column the table is ordered on, in the header and down the
   column itself. Sort by something else and the amber moves with it. Selected controls are plain
   inverted white, not amber, so the accent never has to compete with itself.
4. **Density — 26px rows, 32 players on a 1440 screen, 28 on a phone.** Vertical hairlines between every
   column and a slightly stronger rule every five rows, so the eye can track across a wide table without
   a ruler. The whole list is 21,198px — under half of today's.
5. **Value encoding — distance from the field median (373), on a log-ratio axis.** The centre line is
   the median player; the two ticks are ten times and one tenth of it. The top of the board runs right,
   the tail runs left, and rank 400 sits on the centre line because rank 400 *is* the median. It answers
   a different question from the other two: not "how close to the best" but "how far from ordinary".

**Trade-off.** This is the least welcoming of the three. Fifteen columns is a lot, the type is small,
and it makes no attempt to explain itself in the layout. It is also the one that will need the most care
at very narrow widths.

**Effort to build for real: layout.** The extra columns (age, games, positional rank, Δ%) are all
already in the data bundle or derivable from it in one line. The stat rail is a small computation over
the visible rows. Sorting by column is the one genuinely new mechanic.

---

## Treatment 3 — **Almanac**
`treatment_3_almanac.html`

**What this voice is.** The premium editorial data product — the one that looks like something you pay
for. Air instead of density, a strong typographic ladder, long horizontal rules, and a serif reserved
for the masthead alone. It treats the board as a published reference work rather than an instrument
panel.

**The five choices that make it feel designed**

1. **Typeface — Inter for everything, Instrument Serif for the masthead only.** No monospace anywhere:
   Inter's own tabular figures keep the columns aligned while giving the numbers the same voice as the
   names, which is what makes the page read as one piece rather than a table pasted into a page. The
   serif appears exactly once, in the wordmark, and that single contrast carries the whole "published"
   feeling.
2. **Scale — eight sizes on a 1.2 ratio**, 10 to 34, and a genuine ladder: the value at 19px, the name
   at 16, the club at 12.5, the labels at 10. You can tell the importance of anything on the screen
   without reading it.
3. **Accent — gold is the reading cursor.** The row your pointer or keyboard is on gets a gold rule, a
   gold rank number and a gold dot on its rail. Nothing else in the product is ever gold — not a figure,
   not a control, not a club. In a list this long, a place-keeper is worth more than a highlight.
4. **Density — 36px rows, 23 players on a 1440 screen**, with wide gutters and a 1,352px measure. It
   shows fewer players than the other two on purpose: the space between the rules is what makes it feel
   expensive.
5. **Value encoding — one dot on one rail.** The left end of the rail is the free-hit value (190) —
   "worth exactly what a free agent gives you for nothing" — and the right end is the top of the board.
   Two hairlines mark the 100th and 300th player. Square-root scaled, so rank 400 sits about an eighth
   of the way along rather than vanishing. It is the only one of the three whose scale starts at a
   number that means something in your league rather than at zero.

**Trade-off.** It shows the fewest rows of the three, and the least data per row — the Pick·Yr column
survives but it is deliberately the quietest thing on the line. If your instinct is "give me everything",
this is the wrong one and Terminal is the right one.

**Effort to build for real: layout.** One font file, a new stylesheet, and a slightly narrower column
set. The masthead is a genuine rebuild rather than a restyle, because the hashes and badges come out and
a two-line brand goes in.

---

## Side by side, in numbers

| | Current | 1 · Broadcast | 2 · Terminal | 3 · Almanac |
|---|---|---|---|---|
| Players on a 1440×1000 screen | **8** | 25 | **32** | 23 |
| Players on a 390 phone | **6** | 23 | **28** | 22 |
| Pixels before the first player (phone) | **829** | 165 | 147 | 168 |
| Whole list, top to bottom | **51,813px** | 27,595px | **21,198px** | 29,272px |
| Row height | 55.6px | 34px | 26px | 36px |
| Bar fill at rank 400 | **3.8px** | 21px | at the centre line | 17px |
| Distinct type sizes | **41** | 7 | 6 | 8 |
| Jobs the accent does | **11** | 1 | 1 | 1 |
| Native OS dropdowns | 2 | 0 | 0 | 0 |

---

## If you pick one, what gets built first

- **Broadcast** — the stylesheet, in one pass: tokens, the seven-step scale, the two font files, row
  density, the sticky header. The board is already a shared CSS grid, so the table itself barely
  changes. Then the search box.
- **Terminal** — the columns first, because they are what the voice is for: positional rank, age,
  games, Δ%, and sortable headers with the amber axis. The stat rail after that.
- **Almanac** — the masthead and the type ladder first, because that is where the "expensive" feeling
  comes from and it is also where the hashes currently live. The rail and the cursor after that.

Whichever one you pick, two things should land before the visual work in any of them: **flip the
movement column to the base that has data** (one config line — the column is currently pointed at a feed
that does not exist and prints 804 dashes), and **replace the faint grey used for every label in the
product** (it is currently about half as strong as the readable minimum, and it is what makes the whole
labelling layer look unfinished).

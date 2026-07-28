# How to update ownership, pick holdings and positions (no agent, no LLM)

This is the owner's update path. It is deterministic: a machine reads your spreadsheet, checks it, and
either writes new bundles **or refuses and tells you exactly why**. No model is in the loop.

## The two lanes — read this first, it explains everything else

| lane | what's in it | what a change costs |
|---|---|---|
| **LIVE** | AFFL ownership · pick holdings | **an edit, a command and a reload.** No engine run, no bake, no board move. |
| **BATCHED** | positions | an engine run, a board move, one history column. Not this page. |

Ownership does not affect a single player's value — `affl_team` appears nowhere in the valuation path —
so a trade has no business costing an engine run. Positions **do** feed valuation, so they cannot ride
the live lane: if they did, every trade would trigger a rebuild and you would be back to the old problem.
Same spreadsheet is fine. Two lanes out of it.

## What you edit

Three authored files under `docs/inputs/` (edit in Excel / Sheets, keep the **same file name**):

| File | You change | You never change |
|---|---|---|
| `AFFL_Pick_Locations.xlsx` | the **Owner** column on the *Picks* sheet (who holds a pick); finishing ranges on the *Ladder* sheet | the *Pick Values* tab and the *Raw Value* columns — **reference only, never read** |
| `AFFL_Player_Locations.csv` | a player's **AFFL Team** | player names (they are the join key) |
| `AFFL_Future_Positioning.csv` | future position / blend — **batched, not live** | the `stable_player_id` column |

**Values are never taken from the sheet.** A pick's price is always the engine's own pick curve evaluated
over the pick's band; player values are the shipped board. The sheet is the *authored source of ownership
and bands* — nothing more.

## The three steps

1. **Edit** the spreadsheet on your machine.
2. **Upload** it over the existing file in `docs/inputs/<same name>` using the GitHub web UI
   (open the file → the pencil / "Upload files" → commit). Your click; no agent.
3. **Regenerate + reload.** Run the one deterministic command, then refresh the board:
   ```
   python3 ui/tools/ingest_inputs.py
   ```
   Exit code `0` = clean; `2` = it refused (see below).

That one command writes **both** live-lane bundles:

- `ui/data/club_valuation.js` — pick holdings, each priced off the engine's canonical curve
- `ui/data/ownership.js` — the ownership sidecar the browser reads for club membership

One edit, one command, both outputs. There is deliberately no second mechanism to remember.

**It needs nothing installed.** The workbook is read by `ui/tools/xlsx_read.py`, which uses only the
Python standard library. It used to need `openpyxl`, which meant the live lane *halted* on any machine
without that package — a lane that stops for a missing library is not an edit path.

> **Why a command and not a plain page-reload?** (Fallback taken, stated plainly.) The board is an offline
> viewer that ships its data as pre-baked script bundles so it opens straight from a file with no server
> and no third-party libraries. It cannot fetch and parse a binary `.xlsx` at load time. So the no-LLM
> ingest is this **one deterministic script** — still no model, still validate-or-halt.

## What updates immediately, and what waits for a bake

- **Pick trades** (the Owner column) → live. Re-run the ingest, reload, done.
- **A player moving AFFL club** (the AFFL Team column) → **live.** The sidecar carries your sheet's
  ownership straight to the browser: the board, the Clubs table, club totals, the player card, the Movers
  filter and the public tier all follow it after a re-run and a reload. **No bake, no engine run.**
- **Positions** → batched. Changing one moves player values, so it costs an engine run, a board move and
  one history column. Ask for it as its own piece of work.

**The sidecar overrides; the store falls back.** A player your sheet names takes the sheet's club. A player
it does not name keeps the board's stored `affl_team`. Nothing is deleted from the store — retiring that
field is a separate decision and yours alone.

## Validate-or-HALT: the messages you might see

The ingest prints a **PASS/FAIL verdict for every check** and stops at the first failure. On a HALT it
writes *empty, halted* bundles — **both of them** — so the board refuses to show stale or guessed numbers,
and exits `2`. Nothing is ever guessed.

| Halt message | What went wrong | Fix |
|---|---|---|
| **board id mismatch** | the shipped board changed under the app | re-pin `ui/app/config.js EXPECTED_BOARD` / regenerate `board_view` (engine-side) |
| **STALE-CURVE GUARD … does not byte-match** | the pick curve in the board bundle isn't the engine's canonical curve | do not proceed — this is the S5 stale-curve trap; ask before shipping |
| **UNREADABLE CELL … formula with no cached value** | the workbook was saved without calculating, so a cell has a formula but no value | open the file, let it calculate, save, re-upload |
| **UNREADABLE CELL … cached error value** | a cell holds `#REF!` / `#DIV/0!` / `#N/A` | fix the formula so the cell holds a real value |
| **2027 MULTIPLIER DISAGREEMENT** | the Ladder's `2027 value multiplier` cell ≠ the governing 0.90 | set the cell to `0.9`, or raise the ruling — the ingest will not silently pick |
| **band violation on pick ids …** | a pick's band is outside 1–80, or low > high | fix the Pick (low)/(high) cells |
| **draft year out of [2026, 2027]** | a pick is more than one year ahead | correct the Year column |
| **Owner/Origin '…' does not join to a unique AFFL club** | a club name in the ledger isn't one of the 16 AFFL clubs (or *Free Agents*) | fix the spelling to match a club name |
| **AFFL Team value(s) … are not one of the board club spellings** | the AFFL Team column names a club the board has never seen | fix the spelling — an unknown club would silently split into two in the UI |
| **ambiguous player name(s)** | two players share a name after normalising | disambiguate the names |
| **player name(s) fail the id/board join** | a Player_Locations name has no match in the positioning file or the board | fix the name so it matches |
| **pick-count conservation failed** | the ledger no longer totals 160 across the clubs | restore the full 160-pick ledger |

A clean run ends with two lines naming what it wrote — the pick count and club count, then the number of
players authored and how many of them actually differ from the board.

## One thing the app will tell you rather than guess

The public tier of the board ships its own bundle, and those rows carry no player key — only a display
name. To know whether your sheet moved a public row's player, the app has to match that name back to a
player. Today every one of the 804 names is distinct, so it always matches. If a name ever becomes
ambiguous or stops matching, that row shows **⚠ unverified** instead of a club, and is left out of the club
totals. It does not fall back to the stored club, because with your sheet live the stored club cannot be
assumed current — and a wrong club shown confidently is worse than one the app admits it cannot confirm.

*This viewer never recomputes a value. Picks are priced off the engine's own curve; players carry the
shipped board's numbers; this page only sums and ranks them.*

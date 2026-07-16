# How to update the club-valuation inputs (no agent, no LLM)

This is the owner's update path for pick and player **ownership**. It is deterministic: a machine
reads your spreadsheet, checks it, and either produces a new board overlay **or refuses and tells you
exactly why**. No model is in the loop.

## What you edit

Three authored files under `docs/inputs/` (edit in Excel / Sheets, keep the **same file name**):

| File | You change | You never change |
|---|---|---|
| `AFFL_Pick_Locations.xlsx` | the **Owner** column on the *Picks* sheet (who holds a pick); finishing ranges on the *Ladder* sheet | the *Pick Values* tab and the *Raw Value* columns — **reference only, never read** |
| `AFFL_Player_Locations.csv` | a player's **AFFL Team** | player names (they are the join key) |
| `AFFL_Future_Positioning.csv` | future position / blend | the `stable_player_id` column |

**Values are never taken from the sheet.** A pick's price is always the engine's own pick curve
evaluated over the pick's band; player values are the shipped board. The sheet is the *authored source
of ownership and bands* — nothing more.

## The three steps

1. **Edit** the spreadsheet on your machine.
2. **Upload** it over the existing file in `docs/inputs/<same name>` using the GitHub web UI
   (open the file → the pencil/“Upload files” → commit). Your click; no agent.
3. **Regenerate + reload.** Run the one deterministic command, then refresh the board:
   ```
   python3 ui/tools/ingest_inputs.py
   ```
   It re-reads `docs/inputs/`, re-validates, re-prices every pick, and rewrites
   `ui/data/club_valuation.js`. Then reload the ValueBoard (the **Clubs** tab and the board's
   **picks included** filter show the new numbers). Exit code `0` = clean; `2` = it refused (see below).

> **Why a command and not a plain page-reload?** (Fallback taken, stated plainly.) The board is an
> offline viewer that ships its data as pre-baked script bundles so it opens straight from a file with
> no server and no third-party libraries. It therefore cannot fetch and parse a binary `.xlsx` at load
> time. So the no-LLM ingest is this **one deterministic script** — still no model, still
> validate-or-halt. If a browser-side live fetch is ever wanted, it rides a later pass (it needs the
> inputs published as a fetchable, parseable format); this build ships the committed-bundle path and
> says so.

## Validate-or-HALT: the messages you might see

The ingest prints a **PASS/FAIL verdict for every check** and stops at the first failure. On a HALT it
writes an *empty, halted* overlay (so the board refuses to show stale or guessed club numbers) and
exits `2`. Nothing is ever guessed. What each halt means:

| Halt message | What went wrong | Fix |
|---|---|---|
| **board id mismatch** | the shipped board changed under the app | re-pin `ui/app/config.js EXPECTED_BOARD` / regenerate `board_view` (engine-side) |
| **STALE-CURVE GUARD … does not byte-match** | the pick curve in the board bundle isn't the engine's canonical curve | do not proceed — this is the S5 stale-curve trap; ask before shipping |
| **2027 MULTIPLIER DISAGREEMENT** | the Ladder's `2027 value multiplier` cell ≠ the governing 0.90 (balanced 0.10 discount) | set the cell to `0.9`, or raise the ruling — the ingest will not silently pick |
| **band violation on pick ids …** | a pick's band is outside 1–80, or low > high | fix the Pick (low)/(high) cells |
| **draft year out of [2026, 2027]** | a pick is more than one year ahead | correct the Year column |
| **Owner/Origin '…' does not join to a unique AFFL club** | a club name in the ledger isn't one of the 16 AFFL clubs (or *Free Agents*) | fix the spelling to match a club name |
| **ambiguous player name(s)** | two players share a name after normalising | disambiguate the names |
| **player name(s) fail the id/board join** | a Player_Locations name has no match in the positioning file or the board | fix the name so it matches |
| **the two Max Kings failed the distinctness assertion** | “Max King” and “Maxwell King” collapsed together | keep them spelled distinctly |
| **pick-count conservation failed** | the ledger no longer totals 160 across the clubs | restore the full 160-pick ledger |

A clean run ends with `CLEAN INGEST — 160 picks priced, 16 clubs` and names the top-3 clubs by Overall
Value so you can eyeball them against your Dashboard.

## What updates immediately vs at the next bake

- **Pick trades** (Owner column) → reflected the moment you re-run the ingest. Fully dynamic here.
- **A player moving AFFL club** (AFFL Team column) → validated now, and the summary follows the
  stamped board's ownership, which the ingest asserts agrees with your sheet. A player's *club-of-record
  for value* rides the board and lands at the next board bake (an engine step, outside this viewer).
  The ingest will flag it if your sheet and the board ever disagree — it never silently diverges.

*This viewer never recomputes a value. Picks are priced off the engine's own curve; players carry the
shipped board's numbers; this page only sums and ranks them.*

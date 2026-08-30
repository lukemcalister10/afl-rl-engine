# FW1 — the transcription and what it resolved to · 2026-08-30

Source: four owner screenshots of the FootyWire match statistics tables (the page itself is behind a
Cloudflare bot challenge and was not fetched). **The SC column is the score** — owner word: "The SC
column is the one that matters." AF was ignored.

92 rows = 4 clubs × 23 selected players, which is the FW1 shape (owner: "FW1 is 4 teams playing",
"46 players in a match not 44").

| block | list | rows |
| --- | --- | --- |
| 1 | Western Bulldogs | 23 |
| 2 | Collingwood | 23 |
| 3 | Melbourne | 23 |
| 4 | Carlton | 23 |

Scores: min 12 (Charlie West), max 134 (Marcus Bontempelli), mean 71.8.

## Name resolution — run BEFORE the file is used, not after

**91 of 92 resolve to a unique player who is on the active board. Zero unresolved.**

**One ambiguity, resolved by the owner's own note.** `Bailey Williams` — the store carries exactly
one (`bailey-williams-wb`, Western Bulldogs), which is the one the owner named ("The Bailey Williams
is the Western Bulldogs one"), so this needed no override. `Will Hayes` is the real ambiguity: two
rows, `will-hayes-b` (Collingwood, active, 9 games in 2026) and `will-hayes-1` (no club, `_retired`,
no scoring). The screenshot is the Collingwood list and only one candidate is active, so the target
is `will-hayes-b` — but it is recorded here rather than resolved silently, because a name that maps
to two rows is exactly the case the applier must be told about rather than guess at.

## Three club mismatches — real, and NOT a transcription error

Three players appear in a screenshot for a club the store does not have them at:

| player | appeared in | store `afl_club` | 2026 games |
| --- | --- | --- | --- |
| Lachlan Schultz | Collingwood | Fremantle | 20 |
| Tim Membrey | Collingwood | St Kilda | 19 |
| Harry Sharp | Melbourne | Brisbane | 23 |

These are club moves the store's `afl_club` has not been told about. **It does not affect pricing:**
`afl_club` is an identity/display field and is not read by `ev()` — the register records it as such
at the ID-primary migration ("identity fields, not read by ev()"). It is worth correcting for
display, and it is worth knowing that the field is stale for at least three rows, but it is not a
blocker for applying these scores and it is not evidence the transcription is wrong. The count per
block is exactly 23 in all four cases, which is the check that the transcription did not drift.

## What is NOT settled by this file

The scores are transcribed by eye from images. Name resolution catches a misread NAME; nothing
downstream can catch a misread SCORE on a correctly-spelled name. That check belongs to the owner,
against the screenshots, before this is applied.

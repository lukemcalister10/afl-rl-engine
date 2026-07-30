# FINDING — the owner's CSV update is un-ingested, and ingesting it breaks club-totals parity

Found 2026-07-30 while doing #274 item 2. **Not fixed here** — the fix is outside this wave's fence and
needs a ruling. Reported so it is not discovered by the owner's next upload instead.

## What happened

Item 2 changed `ui/tools/ingest_inputs.py build_clubs()`, so I ran the live ingest to keep its output
consistent. The run was CLEAN (160 picks priced, 16 clubs, all validators PASS) but its two outputs were
then **reverted**, because the run turned out to carry a change that is not mine to make.

## Two facts, measured

**1. The owner's ownership CSV has never been ingested.** `docs/inputs/AFFL_Player_Locations.csv` was
uploaded by the owner at commit `0b105d9`, **2026-07-29 17:48**. The committed sidecar
`ui/data/ownership.js` was generated **2026-07-28 11:08** — before that upload. Regenerating it moves
**18 of 804** players between clubs, e.g.:

| player | committed sidecar | owner's CSV |
|---|---|---|
| Beau McCreery | West Coast Eagles | Sydney Swans |
| Lachie Neale | Sydney Swans | West Coast Eagles |
| Jack Sinclair | Port Adelaide Power | Western Bulldogs |
| Ed Langdon | Sydney Swans | West Coast Eagles |
| Brennan Cox | Sydney Swans | West Coast Eagles |

The sidecar's own counter tells the same story: `nOverriding` **0 → 18**. These are roster changes, so they
move club rosters, Best-23, Top-5/10, and the ladder — not a display detail, and well outside a UI wave.

**2. Ingesting it breaks the club-totals parity suite.** With the refreshed sidecar in place the suite goes
**15 of 17**, failing on "every club agrees on every metric AND on the Best-23 selection" (West Coast:
ui totalPlayer 70657 vs oracle 69967, and five more metrics). The cause is structural, not a bad number:

- `ui/app/club_totals.js` resolves a player's club through `MD.ownership.clubOf()` — **the sidecar**,
  which by #232's design OVERRIDES the store.
- `ingest_inputs.py build_clubs()` — and therefore the parity oracle transcribed from it — reads
  **`affl_team` off the board bundle**, which is store-derived.

While `nOverriding` was 0 those two agreed by coincidence and the divergence was invisible. The moment any
real override exists they disagree. So the #232 live lane's stated promise — *"a trade costs an edit and a
reload, never an engine run"* — does not currently hold: an edit the owner makes to the CSV cannot be
ingested without turning the parity suite red.

Also worth noting: `MD.ownership` gates the sidecar on presence/halt/non-emptiness only — it does **not**
check the sidecar's board pin. So the stale, pre-adoption sidecar (`expectedBoard: 8a38cca4`, while the app
is on `f2df6e0a`) was being honoured, not ignored.

## What this wave did instead

Left both ingest outputs at their committed bytes and shipped item 2 through the browser computation, which
is what the owner's screen actually reads. The parity suite is green at **17 of 17** on the committed tree.

## The decision this needs (not taken here)

Ownership has two sources of truth for the same fact. Either the ingest/oracle side resolves through the
sidecar as the reader does, or ownership stops being duplicated. Either is a change to the ingest's data
semantics and to what the oracle is an oracle OF — engine-lane and ruling-shaped, not a UI display item.
Separately, the owner's 2026-07-29 CSV update is still pending and someone should decide when it lands.

# RL Value Cockpit

Luke's daily-driver viewing layer for the Real-Draft Value Engine — a fast,
dense board of every player with a click-through detail panel showing value and
points trajectories. **Pure view** — it DISPLAYS values and computes NO price
(no score entry, no DB writes, no delta logging; owner-parked until the model
stabilises; see `DATA_CONTRACT.md`). None of the board app's price chain is
ported; only presentational math (rank, rail %, chart coordinates).

## Files

| file | what it is |
|---|---|
| `cockpit.html` | the self-contained cockpit — open it directly in a browser |
| `template.html` | the app (HTML/CSS/JS); `build_cockpit.py` injects the data seam into it |
| `build_cockpit.py` | bakes a self-contained cockpit from the fixture (dev) or board (real) |
| `fixtures/` | synthetic dev data + generator — **not the board** (see below) |
| `DATA_CONTRACT.md` | the `DATA_SEAM` toggle, the source-stamp ring-fence, + the reserved round-history contract |

## Build / refresh

```bash
python3 cockpit/build_cockpit.py                # dev-mode: synthetic fixture -> cockpit.html
python3 cockpit/build_cockpit.py --large        # dev-mode: ~850-row large-N fixture (perf)
python3 cockpit/build_cockpit.py --mode real    # real-mode: the real board
```

**One data seam.** `DATA_SEAM.mode` is the only place the source is chosen:
`dev` loads the synthetic fixture; `real` loads
`data/rl_build/rl_app_data.json` **only if it carries a valid `.srcmd5`
source-stamp**, else it is rejected (the ring-fence — see `DATA_CONTRACT.md`).
The default build is dev, so the shipped `cockpit.html` is a working demo
carrying no real data. After a model re-bake, re-run the one command — no code
change.

Read-only on the engine and data; writes only the chosen cockpit HTML.

## Fixture

`fixtures/fixture.json` (curated edge cases) and `fixtures/fixture_large.json`
(~850 rows) are 100% invented dev data that mirrors the board *schema* but copies
no real rows. Regenerate with `python3 cockpit/fixtures/make_fixture.py`.

## What it does

- **Board** — every player, sortable (value default, name, draft year;
  ties are stable-sorted), filterable by current position, free-text search over
  player + club. A phosphor value rail behind each figure makes the compression
  story scannable (linear / log toggle). Rank column. Same-display-name
  collisions stay distinct by id. The board is **virtualized** — only the
  on-screen window of rows is in the DOM, so the ~850-row large-N fixture
  scrolls smoothly.
- **Detail** — click any row: identity (name, position + reclass note, pick,
  draft year, category, type, club), a value-by-year chart and a
  points-by-career-season chart, and a reserved slot for round-by-round history.

Keyboard: `/` focuses search, arrow keys move between rows, Enter/Space opens a
row, Escape closes the drawer. Reduced-motion respected.

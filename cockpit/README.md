# RL Value Cockpit

Luke's daily-driver viewing layer for the Real-Draft Value Engine — a fast,
dense board of every player with a click-through detail panel showing value and
points trajectories. **Viewing layer only** — no score entry, no DB writes, no
delta logging (owner-parked until the model stabilises; see `DATA_CONTRACT.md`).

## Files

| file | what it is |
|---|---|
| `cockpit.html` | the self-contained cockpit — open it directly in a browser |
| `template.html` | the app (HTML/CSS/JS); `build_cockpit.py` injects data into it |
| `build_cockpit.py` | reads the stable board data and bakes `cockpit.html` |
| `DATA_CONTRACT.md` | the `DATA_SOURCE` seam + the reserved round-history contract |

## Build / refresh

```bash
python3 cockpit/build_cockpit.py
```

Reads `DATA_SOURCE` (declared once at the top of `build_cockpit.py`,
= `data/rl_build/rl_app_data.json`) and writes `cockpit/cockpit.html`. After a
model re-bake, re-run this one command — no code change.

Read-only on the engine and data; writes only `cockpit/cockpit.html`.

## What it does

- **Board** — every player, sortable (value default, name, draft year),
  filterable by current position, free-text search over player + club. A
  phosphor value rail behind each price makes the price compression story
  scannable (linear / log toggle). Rank column.
- **Detail** — click any row: identity (name, position + reclass note, pick,
  draft year, category, type, club), a value-by-year chart and a
  points-by-career-season chart, and a reserved slot for round-by-round history.

Keyboard: `/` focuses search, arrow keys move between rows, Enter/Space opens a
row, Escape closes the drawer. Reduced-motion respected.

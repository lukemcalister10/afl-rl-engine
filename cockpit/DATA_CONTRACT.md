# Cockpit data contract

The viewing layer under `cockpit/` is decoupled from the engine by a single
seam. This file states (i) the `DATA_SOURCE` the viewer reads and how its
schema maps to what the board shows, and (ii) exactly what the future weekly
loop must produce to fill the reserved round-by-round rating section.

---

## (i) DATA_SOURCE — what the viewer reads

```
DATA_SOURCE = data/rl_build/rl_app_data.json
```

Declared once, in `cockpit/build_cockpit.py`. That is the only seam. A model
overhaul re-bake that rewrites this file in place (as `rl_export.py` already
does) auto-updates the cockpit — re-run `python3 cockpit/build_cockpit.py`,
no code change.

### Why this file (not the baked matrix)

| candidate | verdict |
|---|---|
| `data/rl_build/rl_app_data.json` | **chosen.** Stable, unversioned name. It is the file the existing HTML output (`engine/rl_after/rl_build_html.py`) already consumes. Carries a stable per-player `key` slug for identity. |
| `data/s4_matrix_baked_c47cb43d.json` | rejected. Filename is version-stamped by engine md5 — a re-bake changes the hash and breaks the link. Records are keyed by python `id()` (unstable across runs), and it is consumed by the gates harness, not the board. |

The baked matrix does carry the literal field names in the brief
(`Vpath`/`Ppath`/`cur`/`pos`/`cpos`/`yrs`). The stable app-data file carries
the same information under different keys. The loader maps the stable schema to
the display contract and **also prefers the richer baked-contract keys if they
are ever present** — so if a future re-bake enriches the stable file with
`pos`/`cpos`/`Vpath`/`Ppath`/`cur`/`yrs`, they wire in with no change.

### Schema mapping (stable app-data → display contract)

Identity is `key` + `pick` + draft-year cohort — **never surname alone**
(name-collision guard: Max King / Ben King / Maxwell King, Berry, Pickett all
resolve to distinct `key`s).

| brief field | shown as | source in `rl_app_data.json` | notes |
|---|---|---|---|
| player | Player | `name` | |
| identity | (drawer subline) | `key` | stable slug, e.g. `nick-daicos` |
| cur (value) | Value | `v` | current engine value; drives the rank + value rail |
| pos / cpos | Pos | `grp` (current group) | app-data carries current group only; the loader reads `pos`/`cpos` first if present |
| reclass note | `→MID` chip | `fut` (forward blend) | shown when the dominant forward position ≠ current group (94 players); the app-data analogue of cpos≠pos |
| pick | Pick | `pk` | nullable (SSP/rookie shows `—`) |
| year (draft) | Draft | `yr` | |
| cat | Category | `cat` | Father-Son, Academy, Next Gen, … (nullable) |
| type | Type / channel | `ty` + `draft` | ND / RD / MSD / SSP / … |
| — | Club | `club` | |
| Vpath (value by year) | Value trajectory chart | `[vM2, vM1, v, vP1, vP2]` | as-of-year engine values over `[BASE_YEAR−2 … +2]` = 2024–2028; current year (BASE_YEAR) marked amber |
| Ppath (points by year) | Points trajectory chart | `track` → `[{s,a}]` | score-relativity by career season index S1…Sn; empty for the 219 pre-debut/0-game players → renders "No games recorded yet." |
| yrs | chart x-labels | derived from `BASE_YEAR` | or `yrs` if the record carries it |

Rows: `active` (805) + `back` (197, retired players recalled for history,
tagged "retired"). Total 1002. `back` rows have a flat value path (single
as-of-2026 estimate) by construction in `rl_export.py`; the value chart handles
the degenerate/flat case.

---

## (ii) Reserved: round-by-round rating history

The detail panel holds a labelled empty section — **"Round-by-round rating
history — wired in the weekly-loop phase"**. Nothing is rendered there yet
(owner ruling: score-ingestion and the per-round rating-delta log wait for a
stable model, for apples-for-apples comparison). This is the contract the
weekly loop must satisfy to fill it, with **zero change** to the viewer's data
seam.

### What the weekly loop must produce

A **per-player, per-round value series**, keyed by the same stable `key`, added
to the same `DATA_SOURCE` file (or a sibling merged in by `build_cockpit.py`).
Proposed field on each player record:

```jsonc
"rounds": [
  // one entry per graded round, in chronological order
  {
    "yr": 2026,        // season
    "rd": 1,           // round number (or "OR" / finals label)
    "v":  7120,        // engine value AS OF that round (post-grade)
    "d":  +56          // value delta vs the previous round (optional; = v − prev.v)
  }
  // …
]
```

Requirements for apples-for-apples integrity:

1. **Same identity.** Keyed by `key`; the series belongs to exactly one
   player-cohort. No surname joins.
2. **One model per series.** Every `v` in a player's `rounds` must come from the
   same frozen model version. If the model is re-baked mid-season, start a new
   series (or stamp each entry with the engine md5) — never mix versions inside
   one line, or the deltas are meaningless.
3. **Chronological + gap-tolerant.** Missing rounds (bye, injury, not selected)
   are simply absent; the sparkline connects graded points and does not
   fabricate zeros.
4. **Deltas are derived, not authored.** `d` is `v − previous v`; the viewer
   can compute it, so `d` is optional. What the loop owns is the `v`-at-round
   series — the single source of truth.

### Wiring, when it lands

- `build_cockpit.py` already emits a compact per-player model; add `rounds` to
  the mapper (one line) and the loader carries it through untouched.
- The reserved `<div class="reserved">` in `template.html` is the drop-in point
  — replace its placeholder body with a sparkline built the same way as the
  existing `lineChart()` (inline SVG, no libraries), plotting `rounds[].v`
  against round index with the current round marked.

Until that series exists, the section stays reserved and renders nothing fake.

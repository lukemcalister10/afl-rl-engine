# UI DESIGN DIRECTION — the cockpit, grown up · FABLE seat · 2026-07-09
### Deliverable of DIRECTIVE_ui_design_pass_fable_v1_1. Base: main @ d4e8f6dc. Skeleton reviewed:
### `claude/html-cockpit-viewer-xsbfoc` @ 14883c6a · `claude/cockpit-core-viewer-9grm1v` @ 79cd21ee
### (both read-only, unmodified). Direction only — the implementation chapter builds on this.
### Mockups: `docs/ui_direction/mockups/` — ALL figures in them are INVENTED illustrations, not the board.

## 0. THE ONE-SENTENCE DIRECTION
The cockpit is an **instrument panel for one owner**: a dense graphite ledger where every number is
engine-computed cyan, every owner touch is amber, every price movement explains itself in per-lever
plain language — and the screen always states, in the corner, exactly which board it is showing.

## 1. SKELETON REVIEW — what exists, keep/kill

### Which branch line to keep
**Keep the `9grm1v` line as the base.** It is the `xsbfoc` design plus the three things the house
actually needs: the single `DATA_SEAM` with the `.srcmd5` ring-fence (fail-closed rendering — the UI
analogue of Guard 5), the synthetic fixture set (design iteration without touching real data), and the
virtualised board (~1000 rows stay smooth). Where the two differ, `9grm1v`'s text is also the safer
doctrine ("pure view — computes NO price" stated in the file header).
**Obituary — `xsbfoc`'s bare `DATA_SOURCE` seam:** simpler, but it renders whatever file it finds;
after the July 9 review round (B2 reads an unauthenticated file), an unauthenticated viewer input is a
known disease vector — the ring-fence line wins.

### KEEP (the skeleton got these right)
- **The instrument palette and its one semantic rule** — graphite ink, **amber = user controls**,
  **phosphor-cyan = data magnitude**. This rule is the seed of the whole colour system (§3 extends it).
- **The value rail** — the phosphor bar behind each price. It is the signature device; the compression
  story is scannable at a glance. Linear/log toggle stays.
- **Density** — 34px mono-figure rows, ~25 players per screen. This is a ledger, not a dashboard.
- **The drawer** (click row → detail) with identity grid, value/points trajectories, keyboard model
  (`/`, arrows, Enter, Esc), reduced-motion respect.
- **The reserved round-history slot** — renders nothing fake until the weekly loop exists. Correct
  instinct; §5.4 designs what fills it.
- **The readout + mode badge** — engine/source stamps visible in the masthead. §4 promotes this to
  a first-class "which board am I looking at" identity line.
- **Pure-view doctrine + DATA_CONTRACT** — the UI never re-values (SSI). All views below stay inside it.

### KILL (one-line obituaries)
- **The fixed 64px background grid** — decoration competing with a dense table; the row rules already
  carry all the structure. Died of noise.
- **The sort `<select>` dropdown** — redundant with the sortable column headers two centimetres below
  it; two controls for one action is one too many. Died of duplication.
- **`xsbfoc`'s stampless real-data load** — see obituary above. Died of the single-source disease.

## 2. TYPOGRAPHY & DENSITY (confirming and sharpening the skeleton)
- Two faces only: **mono for every figure, key, and stamp** (`tabular-nums`, always right-aligned);
  **the system sans for names and prose**. Player name is the only bold element in a row.
- Type scale: 10.5px uppercase-tracked labels · 12px meta · 13px table body · 17–20px feature figures.
  Nothing larger; magnitude is shown by the rail, not by font size.
- Voice everywhere (CORE rule 6): **player names and values first, jargon in brackets.** Lever labels,
  tooltips, and verdict lines are written for the owner: "Young upside (convexity ceiling) +212",
  never `cvx_ceil_delta`.

## 3. COLOUR SEMANTICS — the rulebook (the design's core)
Four families, never mixed. Position hues stay as small dots only — they never colour figures.

| family | colour | means | used for |
|---|---|---|---|
| **Phosphor cyan** | `#4fc3d4` | *the engine computed this* | value figures, rails, trajectory lines |
| **Amber** | `#e9b949` | *a human touched this* | controls, owner-read pins (anchors), owner overrides, selection |
| **Movement pair** | up `#5dd39e` · down `#e0685e` | *the price moved* | Δ columns, deltas, waterfall bars — always with a signed mono figure, never colour alone |
| **Alarm red** | `#e0685e` on panel | *trust broken* | ring-fence rejection, stamp mismatch — fail-closed screens |

**Provenance / override markers — the Brodie ×0.50 language.** Any multiplicative cut or override on
a displayed value gets a **squared amber-bordered tag right beside the figure**: `×0.50 ROLE`. The
figure shown is always the post-override truth; the rail grows a **hollow "ghost" extension** to where
the value would sit without the cut — the eye sees both the price and the withheld headroom. Hover or
tap the tag for the plain-language sentence ("role-reliability cut: value halved while playing out of
ruck (the Brodie rule)"). The same grammar covers any future owner override: amber tag = a rule, not
the model's own curve, is holding this number. **No silent folds** — if a lever clips a ceiling
(A-DARCY's standing question), the tag is how the owner sees it.

## 4. INFORMATION HIERARCHY — built around the owner's three real jobs
The masthead carries a permanent one-line **identity stamp** (board version · engine md5 · store md5 ·
dev/real badge). After the v2.5-vs-v2.6 green-tick episode, "which board is this" is never implicit.

1. **Board vs his reads** (default landing) — the board as it exists, plus an amber **pin column**:
   each acceptance anchor (Bontempelli, Gawn-vs-Briggs, Cameron, Darcy, Duursma, the faders) shows a
   pin with the read's direction; pin colour states met (filled) / not-yet (hollow). One filter chip —
   "My reads" — collapses the board to the pinned rows. The owner's first question ("does this board
   agree with me?") is answered without leaving the landing screen.
2. **Trade desk** — two panes, **players and picks in one SCAR currency** (picks priced off the
   pick-value curve, shown as first-class rows with the same rail). Totals face each other; the
   verdict is a single plain-language line with the gap figure. Draft-translator slot reserved,
   greyed, labelled "arrives after calibration" — designed-in now, wired later.
3. **Round review** (fills when the weekly loop lands, Phase 3) — "what moved and why": movers ranked
   by |Δ|, each row expanding to the same per-lever waterfall as the player card. History starts
   clean post-overhaul; the view states its round + model version in the header.

**Board vs book vs player card:** no separate book screen. The book (walk-forward history) surfaces
as the player card's trajectory panel and the round-review's per-round series — always stamped with
the model version that produced each segment (DATA_CONTRACT rule: never mix versions in one line;
show a version seam as a small break marker in the sparkline if a re-bake splits a season).

## 5. ATTRIBUTION — per-lever deltas as a visual grammar (G-ATTR made visible)
One grammar, used in the player card and the round review identically: a **waterfall** from the prior
value to the current one. Each lever is a horizontal bar — movement-green right, movement-red left —
with a plain-language label and a signed mono figure. Order: largest |Δ| first. A lever that
contributed nothing prints as a zero line, not omitted (absence is a finding — A-DARCY's availability
layer must be *shown* absent, not skipped). The waterfall's end figure must equal the displayed value
— if the export's lever deltas don't sum, the panel shows the residual as an explicit "unattributed"
bar in alarm red. An unreviewable move should look broken, because it is.

## 6. MOCKUPS (committed, static, invented figures)
| file | fixes the direction for |
|---|---|
| `mockups/01_board.html` | board: rail + Δ column + anchor pins + Brodie-tag + identity stamp |
| `mockups/02_player_card.html` | player card: attribution waterfall + trajectory + reserved history |
| `mockups/03_trade.html` | trade desk: players + picks, one currency, verdict line |
| `mockups/04_round_review.html` | round review: movers, expandable waterfall, version-stamped header |

## 7. IMPLEMENTATION-CHAPTER HANDOFF
**Build order** (each step ships alone; UI reads derived artifacts only, never writes, never re-values):
1. **Adopt the `9grm1v` line** as the base (merge decision is the owner's; review verdict: keep it).
2. **Identity stamp + kill-list** — masthead stamps, drop grid + sort-select. Data: already in `meta`.
3. **Board Δ column + override tags + anchor pins.** Needs from export: previous-accepted-board value
   per player (`vPrev`), an `overrides:[{tag,mult,why}]` array, and an anchors manifest (id, key,
   direction, status) — all into `rl_app_data.json` siblings, stamped.
4. **Player-card waterfall.** Needs: `levers:[{label,delta}]` per player per bake (G-ATTR already
   requires these to exist for multi-lever builds — the export just carries them through).
5. **Trade desk.** Needs: the pick-value curve as a derived, stamped artifact (pick → SCAR).
6. **Round review** — blocked on Phase 3 weekly loop; contract already written in DATA_CONTRACT (ii).
Draft-translator panel ships greyed at step 5; wires only after its calibration gate.

## 8. OPEN DESIGN QUESTIONS FOR THE OWNER (symmetric options)
- **Q-GHOST** — override ghost rail: (a) show the hollow pre-override extension (more information,
  busier rail) · (b) post-only figure with tag alone (cleaner, headroom one hover away).
- **Q-DELTA-BASE** — the board Δ column compares to: (a) the last *accepted* bake (stable, matches
  your ruling cadence) · (b) the previous *round* once the weekly loop lands (fresher, noisier).
  Could be the linear/log-style toggle; pick a default.
- **Q-VERDICT** — trade desk bottom line: (a) figures only, you conclude · (b) a plain-language
  verdict sentence ("You give up 214 SCAR (≈ late second-rounder)") — the model speaks, you overrule.
- **Q-THEME** — (a) dark-only (one look, tuned, instrument identity) · (b) add a light variant
  (daylight readability, double the tuning surface).

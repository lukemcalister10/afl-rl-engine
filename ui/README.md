# Matchday UI — implementation

Owner-facing viewer for the Real-Draft Value Engine board, built to the locked visual law in
`docs/ui_styles/theme_03_matchday_FINAL/` (the **Matchday LOCK**) and the `docs/ui_direction/DESIGN_DIRECTION.md`
direction. **TIER 3: this UI never bakes and changes no value.** It is a *pure view* — it reads the derived
board **read-only** and computes no price (the SSI / DATA_CONTRACT doctrine, the UI analogue of Guard 5).

## Run it
```
cd ui && python3 -m http.server 8791
# open http://127.0.0.1:8791/index.html
```
It also opens directly from `file://` (the board data ships as `window.__…__ = {…}` script bundles, so no
fetch/CORS). Dark-only by ruling (**Q-THEME a**).

## The four ruled letters (owner-worded 2026-07-12), as built
- **Q-GHOST (b)** — override rows show the **post-override figure + `OWNER OVERRIDE` tag**; the model's
  pre-override figure is **one hover away on the tag, never on the rail**. No ghost rail. On the player card
  the rule is a **waterfall line item**, not a ghost.
- **Q-DELTA-BASE** — the **bake / round toggle is built**; DEFAULT = **(a) Δ vs last accepted bake**. The flip
  to **(b) previous round** at go-live is **one line**: `app/config.js › DELTA_BASE_DEFAULT`.
- **Q-VERDICT (b)** — the trade desk closes with a **plain-language verdict sentence** (figures alongside; the
  model speaks, the owner overrules).
- **Q-THEME (a)** — **dark-only.** One look, tuned to the LOCK.

## Views
- **Board** (working / public) — a **player ranking**: a display-only pick-asset filter (owner ruling,
  register v16 item 14) keeps the current and backward lenses players-only; picks stay on the trade desk and
  at the +1/+2 lenses. anchor **pins** (the owner's acceptance reads; Gawn>Briggs is verified live
  from the board), **`OWNER OVERRIDE` tags**, the **Δ-base toggle**, the **±1/2-yr board lens**, a **My reads**
  filter, a **debug/slugs** toggle, and the segmented ten-block power bar. Public tier is the sanitised trim.
- **Player card** (working / public) — value/rank, the **“why the price is what it is” waterfall**, the
  **value-by-year ±2-yr lens trajectory** (real), the **recent-form** season line (real), reserved round history.
- **Trade desk** — players + picks in **one SCAR currency** (picks off the PVC), the **verdict sentence**.
- **Round review** — reserved in the Matchday look (blocked on the Phase-3 weekly loop; renders nothing fake).

## Data seam (read-only)
`tools/extract_board_view.py` reads `data/rl_build/rl_app_data.json` and `data/expected_boot.json` **strictly
read-only** and emits two **tiered, stamped** bundles into `ui/data/`:
- `board_view_working.js` — full working aid (identity-bearing).
- `board_view_public.js` — sanitised (no keys/slugs, no md5/guard stamps, no pathway, no owner-rule). The
  **two-tier UI law made real at the data layer** — the public bundle is leak-proof by construction.

**Ring-fence:** `md5(rl_app_data.json) == the pinned board id (9ecbe0fa…)`, so the app **fail-closes to an
alarm-red screen** if the loaded board's md5 head ≠ `config.EXPECTED_BOARD`. Regenerate the bundles after any
board change: `python3 ui/tools/extract_board_view.py`.

The **±1/2-yr lens** is `[vM2, vM1, v, vP1, vP2] = ev @ 2024/2025/2026/2027/2028` (`engine/rl_after/rl_export.py:66`);
backward boards are real re-values on truncated data, forward boards are projections. Backward lenses include
the `back[]` retired players — the full historical field is 1,002.

## Export-contract gaps (honest; nothing invented, no recomputation)
The v2.8 export does not yet carry two `DESIGN_DIRECTION §7.3/§7.4` fields. Both displays are **fully built and
wired**; where the field is absent the UI shows a clean “awaiting” state and **never a fabricated number**:
- **`vPrev`** (per-player last-accepted-bake value) → the Δ-vs-bake column/toggle.
- **`vRaw`** (pre-override figure) → the `OWNER OVERRIDE` hover.
- **`levers:[{label,delta}]`** → the full per-lever attribution waterfall on the card.
Each is a one-line engine-side export addition (OUT of this UI's fence). When they land, no UI change is needed.

## Fence
IN: `ui/**` only — all new, disjoint from engine/store/gates; reads derived artifacts read-only.
OUT: the store · engine/valuation · gates/guards · docs authoring · ingestion · any recomputation of values.

# PLAN — Matchday UI implementation (first committed artifact)

**Directive:** DIRECTIVE_ui_build_v1 · TIER 3 (never bakes; no value change) · MODE auto · EFFORT high.
**Branch:** `claude/matchday-ui-implementation-a1sscd`. **Candidate PR only — nothing merges without the owner's word.**

## BASE VERIFICATION (done)
- FULL-URL ls-remote: `main` moved to `0f96f281` — **one commit past** the directive's pin `408ab169`.
  That commit is **docs-only** (`DECISIONS v95` + `HANDOVER rev131`), and it *folds in the exact four UI
  letters (§52) + migration rulings (§53)* with no scope change. HANDOVER rev131's standing line sanctions
  "`main == 408ab169` **or newer-verified**". Base drift → **verified benign**; branch rebased onto `0f96f281`.
- tag `v2.8 == 9bd0cfd` ✓ (ALWAYS). Boot-store Guard 5 PASS (store `04f38dad` == pinned).

## THE FOUR RULED LETTERS (build exactly)
- **Q-GHOST (b):** override rows show the **post-override figure + `OWNER OVERRIDE` tag only**; the model's
  pre-override figure is **one hover away, never on the rail**. No ghost rail (consistent with the LOCK).
- **Q-DELTA-BASE:** build the **toggle**; DEFAULT = **(a) Δ vs last accepted bake**. Flip to **(b) previous
  round** ships as a **one-line config** (`config.js › DELTA_BASE_DEFAULT`), not a rebuild.
- **Q-VERDICT (b):** the trade desk closes with a **plain-language verdict sentence** (figures alongside;
  the model speaks, the owner overrules).
- **Q-THEME (a):** **dark-only.** One look, tuned to the LOCK. No light variant.

## VISUAL LAW (the LOCK is law)
`docs/ui_styles/theme_03_matchday_FINAL/` — near-black pitch `#0a0c10`, one **volt** accent `#c8f04a`,
condensed caps for names/labels, mono tabular figures. Signature devices: the **segmented ten-block power
bar** (a block = a decile of the top price; no continuous rail), **movement pills always signed**, override
= an **outlined OWNER RULE chip**. LOCK amendments retained: **full names everywhere** (wrap, never clip),
**comma digit grouping** on every value ("3,462"). Trade desk + round review are translated from the
DESIGN_DIRECTION mockups **into the Matchday visual language** (the old cockpit palette is superseded).

## DATA SEAM (read-only; the UI never re-values — SSI/§7 pure-view doctrine)
- Source (READ-ONLY): `data/rl_build/rl_app_data.json`. **`md5(artifact) == 9ecbe0fa == the pinned board id`** —
  so the ring-fence is exact: the UI **fail-closes to an alarm-red screen if the loaded board's md5 ≠ the
  expected board id** (the UI analogue of Guard 5). Identity stamps sourced from `data/expected_boot.json`.
- Real fields used: `v` (value), `vM2/vM1/v/vP1/vP2` = the **±2-yr lens** (= ev @ 2024/2025/2026/2027/2028;
  backward boards are real re-values on truncated data, forward are projections — `rl_export.py:66`),
  `track` (round trajectory), `picks`+`PVC` (pick→SCAR for the trade desk), `brodieBase` (owner-rule flag),
  name/grp/club/pk/yr/ty/age/cat. `back[]` players surface on the −1/−2 lens boards.
- **Two-tier UI law → two generated data files** (leak-proof by construction, not just hidden client-side):
  `tools/extract_board_view.py` (read-only) emits `data/board_view_working.js` (full, stamped) and
  `data/board_view_public.js` (sanitised: no keys/slugs, no md5/guard stamps, no mech, no owner-rule, movement
  only). Emitted as `window.__…__ = {…}` script files so the app renders from `file://` **and** when served.

## EXPORT-CONTRACT GAPS (honest; in-fence — no recomputation, no invented numbers)
The v2.8 export does **not** carry two §7.3 "NEW export fields":
- `vPrev` (per-player last-accepted-bake value) → the **Q-DELTA-BASE column + toggle are fully built and
  wired to `vPrev`**; where absent the cell shows a clean "awaiting bake-Δ export" state, never a fake Δ.
- `vRaw` (pre-override figure) → the **OWNER OVERRIDE tag + hover are fully built and wired to `vRaw`**; the
  hover states the rule in plain language and, when `vRaw` lands, the pre-override figure. No number invented.
Both are one-line engine-side export additions (OUT of this fence) — flagged in the RETURN, not worked around.

## VIEWS (primary)
1. **Board — working**: identity stamp + guard badges · anchor pins (real reads; Gawn>Briggs verifiable) ·
   OWNER OVERRIDE tags · Δ-base toggle (bake default) · **±1/2-yr lens toggle** · debug/slugs toggle · power bars.
2. **Board — public**: sanitised trim, movement-vs-previous-round scheme, no internals.
3. **Player card — working / public**: value/rank · attribution waterfall ("Why the price is what it is") ·
   **year-lens trajectory** (the five real lens values) · round-by-round from `track` · owner-rule line item.
4. **Trade desk**: players + picks in one SCAR currency (picks off `PVC`) · **plain-language verdict sentence**.
5. **Round review**: reserved/greyed in the Matchday look (blocked on the Phase-3 weekly loop).

## FENCE CHECK
IN: `ui/**` only — all new, disjoint from engine/store/gates; reads derived artifacts READ-ONLY.
OUT: the store · engine/valuation · gates/guards · docs authoring · ingestion · any recomputation of values.
CONCURRENCY: touches ZERO files shared with the parallel store-writing migration build.

## RETURN
≤30 lines · committed artifacts · screenshots of each primary view · an "in plain terms" close · branch ·
head SHA · PR number (candidate; merge-commit policy). BUILD-REPORTED until prescreened. Est. within the 4–8h band.

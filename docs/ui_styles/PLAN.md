# PLAN — UI style exploration (design pitches) · FABLE seat · 2026-07-09
### Deliverable of DIRECTIVE_ui_style_exploration_fable_v1. Base: main @ b303795 (verified live).
### Content reference: `docs/ui_direction/` @ 60172dd (PR #48) — CONTENT survives, AESTHETICS rejected (§32).
### Style contender: Opus cockpit @ 14883c6a / 79cd21ee (read-only). Mode auto — this plan is artifact 1.

## The job
Four genuinely distinct visual themes — different designers, same brief — each applied to the SAME
two screens (the board + the player card, chosen because the card exercises the ruled
override-in-waterfall grammar), each in BOTH trims (§32 two-tier law). All figures INVENTED and
bannered. No engine/data wiring; the viewer branches stay untouched.

## The four pitches
| dir | theme | personality (one line) |
|---|---|---|
| `theme_01_cockpit` | **Cockpit** | the Opus instrument language, faithfully extended — graphite ledger, phosphor-cyan data, amber for the owner's hand |
| `theme_02_broadsheet` | **Broadsheet** | the Saturday form guide — warm paper, serif headlines, hairline rules; print authority, reads like the racing pages |
| `theme_03_matchday` | **Matchday** | the broadcast graphics package — near-black, one electric accent, condensed caps, big confident numerals |
| `theme_04_registry` | **Registry** | the Swiss ledger — white, grid-strict, one ink + one blue, numbers carry everything; austere precision |

## Files per theme (16 boards + note)
`board_working.html` · `board_public.html` · `card_working.html` · `card_public.html`
plus `docs/ui_styles/COMPARISON.md` — one page, plain language, what each theme optimises for.

## Ruled constraints baked into every theme (§32/§34–35, directive FENCE)
- **No player slugs in default views.** Working aid shows a *debug toggle concept* (off) in the toolbar only.
- **No ghost rail.** Override headroom lives as a line item in the attribution waterfall; the rail never grows a dashed extension.
- **Override marker visible-but-clean** — Coleman-Jones ×0.50 (the Brodie rule) is the one case shown; each theme restyles the marker.
- **Value-number presentation redesigned per theme** — the rejected figure-floating-on-rail treatment appears in no pitch; each theme proposes its own device (separated figure/rail columns · print underline-bar · segmented power bar · figure + percentile).
- **Δ scheme as ruled:** working aid = Δ vs last bake with a bake/round toggle; public = Δ vs previous round, no toggle.
- **Verdict voice = Option B** (plain-language sentence) wherever the model concludes.
- **Colour never the sole carrier** — every movement has a sign and glyph; every state has a label.

## Two-tier law per screen
- **WORKING AID:** masthead identity stamp (board v2.6 · engine 4b08796c · store a2fbc9a0 · fd90472c board id · REAL badge · Guard-5 state), Δ toggle, debug affordances, full per-lever waterfall incl. the override line item, anchor pins.
- **PUBLIC:** values, ranks, movement (Δ vs previous round), trajectory. NO board/bake/engine/store IDs, NO guard states, NO override machinery labels, NO pins/reads, NO valuation internals (the waterfall stays home).

## Order of work
1. this PLAN (commit 1) → 2. theme 01 (cockpit contender) → 3. themes 02–04 → 4. COMPARISON.md → 5. PR, BUILD-REPORTED.

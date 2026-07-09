# PLAN — Matchday theme polish (FINAL reference set)

**Directive:** MATCHDAY THEME POLISH v1 · FABLE seat · mode auto (this plan = first committed artifact).
**Base:** live main `b303795` (fetched fresh, verified). Pitch source: `docs/ui_styles/theme_03_matchday/`
at pinned SHA `967487c8` = live tip of `claude/new-session-13lcx4` (PR #54) — verified. The pitch set is
not yet on main; this branch adds **only** the FINAL directory, so the original pitch set stays untouched
on its record branch.

## Steps
1. Copy the four Matchday screens into `theme_03_matchday_FINAL/` (board + player card × working/public).
2. **Amendment 1 — full names everywhere.** Both boards print row-104 as bare "Coleman-Jones";
   restore "Callum Coleman-Jones". Audit all other name sites (cards already full).
3. **Amendment 2 — comma digit grouping.** Replace every thin-space-grouped value ("3 462" → "3,462")
   across all four screens: seven board values ×2 boards, the working card's "1 748" waterfall total,
   and the ungrouped count/denominator "1002" → "1,002" wherever it appears. Years and picks are not
   grouped values and stay as-is.
4. **Amendment 3 — working-card render repair.** Render `card_working.html` in the pre-installed
   Chromium (Playwright screenshot, desktop + narrow widths), identify the layout defects the owner saw,
   name them, and repair them. Re-render to confirm.
5. Re-render all four screens as a §32 retention check: no ghost rail · no slugs in defaults · identity
   stamps working-trim only · Δ = bake+toggle (working) / previous-round (public) · verdict voice B ·
   colour never the sole carrier · "invented figures" banners retained.
6. Add `LOCK.md`: visual law for the UI implementation chapter + the amendment list + owner-ruling cite.
7. Push branch `claude/new-session-a32h24`, open candidate PR. Return ≤30 lines with named defects.

## Fence check
Read-only on engine/data (no engine files touched). Non-winning themes untouched (Cockpit defect MOOT).
No new design elements beyond the three amendments.

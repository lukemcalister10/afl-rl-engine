# LOCK — Matchday FINAL · the visual law for the UI implementation chapter

**This directory is the locked visual reference.** The UI implementation chapter builds under these four
screens. The original pitch set (`../theme_03_matchday/`, pinned SHA `967487c8`, PR #54) stays untouched
as the record; **this FINAL directory supersedes it for build purposes.**

**Owner ruling (2026-07-09/10): Matchday WINS, with three amendments** — applied here:

1. **Full player names everywhere.** "Coleman-Jones" without "Callum" is not acceptable; the
   first-name-dropping broadcast affectation dies. Both boards now print "Callum Coleman-Jones";
   name cells wrap instead of ellipsis-truncating, so no name (or its owner-rule chip) is ever clipped.
2. **Comma digit grouping on every value.** "3,462", never thin-space "3 462" — applied to every
   numeric value on all four screens, including the waterfall's "1,748" start and the "1,002" player
   count/denominator. Years and draft picks are labels, not grouped values.
3. **Working player card repaired** (rendered in Chromium, defects fixed):
   - *Class collision:* the CSS rule for the tracks' centre hairline (`.wf .zero`) also matched the
     availability figure `<span class="fig zero">0 · absent</span>`, absolutely positioning it as a
     1px full-page vertical stripe through the card with stray "0 · absent" text over the banner.
     The hairline class is renamed `zline`.
   - *Waterfall grid misalignment* (consequence of the same collision): with that cell ripped out of
     grid flow, every later cell shifted one column — the "Everything else" and "Your rule" labels
     rendered in the figures column and their tracks stretched across the label column. Aligned now.

**Every §32 constraint retained:** no ghost rail (the owner's rule is a hollow-volt waterfall line
item) · no slugs in default views (debug toggle only, working trim) · identity stamps
(board/engine/store/board-id, guard badges) working-trim only · Δ default = vs last accepted bake with
bake/round toggle on the working board; public tier shows movement vs previous round only · verdict
voice B ("Why the price is what it is") · colour never the sole carrier (pills and figures always
signed; pins carry title text) · "invented figures" pitch banners stay on all four screens.

#!/usr/bin/env python3
"""Render the R-i pause-vs-advance comparison table markdown from two ri_worker JSONs.
Usage: ri_render.py <pause.json> <advance.json> <out.md>"""
import json, sys
pause = json.load(open(sys.argv[1]))['names']
adv = json.load(open(sys.argv[2]))['names']
named = {'sam-darcy', 'jesse-motlop', 'sam-flanders', 'josh-gibcus'}
rows = []
for k, v in pause.items():
    if v['ycred'] > 1.0001 or k in named:
        a = adv[k]
        rows.append((v['player'], v['section'], v['ev'], a['ev'], a['ev'] - v['ev'],
                     v['ycred'], a['ycred'], v['games'], a['games'], k))
rows.sort(key=lambda r: r[4])


def driver(nm, sec, vp, va, d, ycp, yca, gp, ga, k):
    if abs(d) == 0 and gp >= 46:
        return "past G0=46 — no L1c credit either way (value driven by KPF/production, not the young clock)"
    if abs(d) == 0:
        return "0-games sit-out name — value is V0/floor-anchored (draft-year credit); the 2026 clock doesn't reach the shipped value"
    return "young L1c credit fades %.3f→%.3f as the clock advances g %.0f→%.0f (≈%.0f expected games added)" % (ycp, yca, gp, ga, ga - gp)


L = ["# R-i COMPARISON TABLE — L1c fade-clock PAUSE vs ADVANCE for injured young register names — v1 · 2026-07-09",
     "### PROVISIONAL (R-i, DECISIONS §33). Fork-i: does an injured youngster's L1c young-credit clock PAUSE while",
     "### he is out (status quo — the clock keys on career GAMES, so an injured season adds ~0 and it implicitly",
     "### pauses) or ADVANCE by his expected (lost) games (fading the credit as if he had played)? RECOMMENDATION",
     "### = (a) PAUSE (default). Clean toggle `RL_LTI_CLOCK=pause|advance` — an owner flip is this config change,",
     "### NOT a rebuild. **The owner confirms or flips R-i on THIS table BEFORE any bake.** Regenerate:",
     "### `session_2026-07-09/injury_build/run_ri_table.sh`. Engine head tracks the candidate; store a2fbc9a0.",
     "", "Value = board ev(2026). Δ = advance − pause (advancing NEVER raises value). Only the genuinely young,",
     "under-G0 (46-game) register names move; the named exemplars Darcy/Motlop/Flanders sit past G0 (no L1c",
     "credit either way), so R-i does not touch them — Gibcus is the one named exemplar the clock still bites.", "",
     "| player | sec | pause | advance | Δ | yc pause | yc adv | g pause→adv | driver |",
     "|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    L.append("| %s | %s | %d | %d | %+d | %.3f | %.3f | %.0f→%.0f | %s |" %
             (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], driver(*r)))
L += ["", "## Reading / recommendation",
      "- **(a) PAUSE — RECOMMENDED (default).** The games-clock already pauses implicitly; a returning youngster keeps his young-credit runway intact (forfeited-growth-year hypothesis — his lost year costs him Part 1's nerf, not his ceiling). Zero new constant.",
      "- **(b) ADVANCE** fades the credit with NO new evidence against the player — it violates the evidence-quantity rationale the owner accepted for L1c, and it moves the young, low-games names DOWN (O'Farrell −206, Faull −72, Carroll −32, Gibcus −17…) purely for being injured. A-DARCY: Darcy himself is past G0 (Δ0) so his ceiling is untouched either way, but for the general young cohort advance clips the runway through the availability locus.",
      "- **(c) pause + calendar cap** = identical to (a) for every current register name (none is near a sane cap); a dormant guard to derive only if a perpetual-youth case appears.",
      "", "## IN PLAIN TERMS",
      "Injured kids: leave their 'young clock' paused while they're out (recommended) and their comeback keeps full runway — or advance it and they quietly lose value for a year they never played. Only the genuinely young, low-games names move; Darcy/Motlop/Flanders are already past the young-credit line, so this choice barely touches your headline names (Gibcus aside). Your call before any bake."]
open(sys.argv[3], 'w').write("\n".join(L) + "\n")
print("wrote %s (%d rows)" % (sys.argv[3], len(rows)))

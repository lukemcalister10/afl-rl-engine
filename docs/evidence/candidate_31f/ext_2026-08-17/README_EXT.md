# 2026-08-17 — owner-review measurement batch (supervisor in-session, disclosed)

**t338_extended_DISCLOSED.py** — disclosed copy of the canonical noarb_table_338.py (md5 0f822035, untouched),
three declared edits: (1) YEARS 0..12 (owner ask: measure where the path crosses back below yr1);
(2) five tighter pick bands 1-10/11-20/21-30/31-40/41-64 (owner ask); (3) harness import -> the ORDER-29
re-pointed copy (02dcf28c). CONTROL: yr0-7 of the three original groups replicate the published
table_O31FFINAL.json EXACTLY (24/24 ratios). Matrix: per_entrant_O31FFINAL.json (store cb38ef11).

**THE CROSSING**: every group crosses back below its own yr1 at yr8-10 (ALL 1-64 at yr9 = 0.863 vs yr1 1.066;
all-arm PRIMARY at yr9 = 0.8453 vs yr1 1.0376, same-construction replication EXACT on yr0-7).

**FINDING (defect, owner-caught via the Carmichael question): THE ONE-GAME FADE-CURE CLIFF.**
o31_played_units credits a FULL season unit (1.0, or the whole in-progress fraction _fEy) for ANY season with
games > 0. A gameless year-1 row (c_u 1.92, D 0.58) that plays ONE game flips its whole in-progress fraction
to played: c_u -> 1.0, D -> 1.00 — e.g. lachlan-carmichael 453 -> ~740+ (>= +63%) off one game scored 13.
This resurrects, inside the sitter clock, exactly the 0-vs-1-game cliff the owner ruled out of the blend
(ruling 2026-08-14). Candidate fix direction: games-proportional played credit (e.g. min(1, games/expected-
season) per season). NOT yet wired — awaiting the owner's word.

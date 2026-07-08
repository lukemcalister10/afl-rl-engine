# RETURN — L1c RECTIFICATION BUILD · 2026-07-08 · branch `claude/fable-wave-4-integration-w4rfpb` · PR #46
1. BUILT AS DIRECTED: the W4 runway leg is REPLACED by the evidence-conditioned expected-rerating credit —
   e' = e·(1 + w·max(R_cell,0)·φ(games)), cells pos×log-pick-kernel×played/sat, TRAILING (table_T uses classes
   with C+2≤T only; leak-free, asserted in code comments for the auditor), full at zero evidence (V0/day-0),
   φ→0 at G0=46 games (census-derived ≈y3-4). Kill-switch RL_YOUNG; dial RL_YCRED_W; SHIPPED w=0.7.
2. PER-YEAR RATIOS AT w=0.7 (conforming measure, class SUMS avg'd, each year vs min(y1,y2)=y1 61,975):
   y4 131.9% · y5 130.5% · y6 122.3% — y4/y5 still BREACH hard 130 (from 142.4/140.8/131.7). w=0.85 is the
   first PASS: 129.4/127.7/119.7; w=1.0: 126.9/125.1/117.1 (~guide top). SIM-vs-BUILT: the investigation's
   simulated 0.85→120/1.0→116.7 match built **y6**, not binding y4 — mechanism decomposed in the w-table
   (evidence-fade at the y1 anchor · played≪sat re-ratings · trailing zero-credit 2004-05 · clip≥0 · ruc cap).
3. OWNER W-TABLE: session_2026-07-08/l1c_rectification/out/W_TABLE.md (grid {0.5,0.7,0.85,1.0}, y1/y2 figures,
   per-year ratios, named players incl. Duursma/top-3/Gulden/Darcy/Goad/pure-sit-out/mature-age). 0.7 ships as
   default, not a ruling; the owner rules w on sight — 0.85 is the smallest gridded w that passes the hard bound.
4. TRAILING-vs-FULL evidence line (printed once, TRAILING shipped): at T=2016, sat-cell R@pick8 trailing/full =
   MID +0.42/+0.30 · GEN_FWD +0.30/+0.26 · KEY_FWD −0.02/+0.19 · KEY_DEF +0.75/+0.50 — full uses classes the
   credit-year could not see; converges to identity by T=2026 (census artifact).
5. A-SURFACE CROSS-CHECK (owner amendment, report-only): all 12 cells DIVERGE >15% — realized-production A pins
   at the structural ≈+12.6% discount-rate bound while book-basis sat cells run 2-4×; realized basis would land
   w=0.7 at ≈135.7%. Book basis ships (sanctioned: internal no-arbitrage in book currency).
6. HYPOTHESIS TEST (report-only): SUPPORTED, strongly. Top decile carries 90% of net y1→y2 re-rating gain and
   105% of y1→y4 (rest of class net-negative); only 34-41% of players gain at all; per-cell top-decile shares
   0.5-3.9 (census). The owner's distribution story (few reach convex tiers) matches the measured tails —
   informs a future band-pricing root fix; nothing built.
7. SUITE: all-off byte-exact v2.5 ✓ (re-verified on L1c head) · panel re-stamped CANDIDATE, PASS 10/10 ·
   B1/B2(leak 0.0)/B4(board 8e8e9250 byte-agree)/B5/B6/D14a-c PASS · B3 DIFFERS-by-design (key set identical,
   candidate seal committed) · A2/A3/A12 pre-existing reds unchanged · G-ATTR: 1534 movers, 0 negative, +2.31%
   pool · A-DUUR up (4110→4199) · G-MONO: 0 inversions, D14 dispersion 0.0, no pk20/21 cliff.
8. OQ-B THREE NARROWEST MARGINS: (i) y4 at w=0.85 = 129.4 vs hard 130 — 0.6pt; (ii) shipped-w y5 130.5 vs 130 —
   0.5pt over (the breach edge); (iii) DECLARED TENSION: evidence-axis dip on extreme sat cells — a pick-1 MID
   sweeping games 0→14 peaks then dips −7.6% (g4→g7) as the sat premium unwinds faster than evidence accrues
   (credit-off sweep monotone; continuous, no cliff; pk7 −2%, pk5 none; artifacts out/evidence_sweeps.json).
IN PLAIN TERMS: the engine now pays a young player, from the day he's drafted, a measured share of what his
exact kind of player (position, pick, played-or-sat) has historically re-rated to one year later — busts
included, measured only on data the engine could have seen at the time, and fading out as real games replace
the expectation. At the shipped 70% share the draft-class books tighten from a 142% breach to 132% — still
over your 130 line; your table shows 85% is where it first passes. Store untouched (e1b4d8bf entry+exit);
engine pin bumped; time ~4.5h (band 3-6h confirmed).

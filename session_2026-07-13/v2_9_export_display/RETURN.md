# v2.9 EXPORT/DISPLAY BUNDLE — RETURN · 2026-07-13

Branch `claude/v2-9-export-display-jkcd5e` · base candidate kq4dae@**917e4c4** (verified unmoved).
Lineage moves: **kq4dae@917e4c4 → export-display@c99c2a6**. Fence: export/display only; kq4dae untouched.

## THE ZERO-EV-MOVER PROOF (hard acceptance — GREEN)
Wired board **8a66b4ba → f2d6e3f5**. Diff vs the certified 8a66b4ba: **n=804, sum_v=732725, key-set
sym-diff 0, ZERO movers on active AND back** (v + all five lens years). The ONLY diff is new keys.
`rl_export` parity gate PASS (804/804 board v == engine gated ev). Artifact:
`out/ev_invariance_proof.txt`. New keys: top-level `lensPicks`,`lensConservation`; per-row
`vPrev`,`vRaw`,`levers`; `lti_reg` now populated for the two rows that shipped NULL.

## THE FIVE JOBS (each names its committed artifact)
1. **barker/thredgold lti_reg** — FIXED (`rl_export.py`, consumer-wiring). Root cause: the board
   `players` list holds SEPARATE objects from `MA.data` for first-year no-scoring-row rows, so the
   RL_AVAIL tag never reached them. Resolved by stable-key lookup.
   BEFORE: `harley-barker lti_reg=None` · `blake-thredgold lti_reg=None`.
   AFTER:  `harley-barker lti_reg={section:B,out:true,L:1.0,ret_year:2027,flags:[sectionB_no_return_haircut]}`
   · `blake-thredgold lti_reg={section:A,out:true,L:1.0,return_arm:true,ret_year:2027}`. (test §A PASS)
2. **vPrev / vRaw / levers** — `rl_export.py` + committed sidecar `engine/rl_after/export_attribution.json`
   (from the certified stage boards; per-key split closes for all 804; emmett vPrev 1178 / L4 −352 / L2 +25
   / net −327 reproduces CERTIFICATION to the dollar). vRaw null (0 overrides active).
3. **+1/+2 phantom-pick lens entries** — `lensPicks` (60 entries: 2026-EOY-ND picks 1–30 on the +1/+2
   lenses only, PVC face value, rolling labels; never on the current/−1/−2 player ladder — item-14
   exclusion held).
4. **lens-conservation diagnostic** — `lensConservation` (report-only): −2 846900 · −1 801011 · now 732725
   · +1 578672 · +2 452159; spread vs now −2 +15.6% / −1 +9.3% / +1 −21.0% / +2 −38.3%.
5. **UI re-extract + re-pin** — EXPECTED_BOARD 8a66b4ba→f2d6e3f5; `board_view_working.js` /
   `board_view_public.js` regenerated (ring-fence OK). Public bundle refreshed off the certified refit
   values (was stale at de4baef9). Rulings hold: Q-GHOST(b)/Q-DELTA-BASE(a)/Q-VERDICT(b)/Q-THEME(a).

## FINDINGS (out of fence — reported, not worked)
- **REFUTED (benign):** barker/thredgold ship v=777/577 unchanged; the availability haircut is INERT
  for 0-game first-years (`haircut_delta=0`, `out/barker_thredgold_haircut_probe.txt`) — the split-object
  quirk cost only the display tag, now closed. No valuation defect.
- **Conservation spread is wide** (+1 −21%, +2 −38%): the forward lenses run well under, larger than
  "slight." Consistent with undiscounted-future projections decaying + only 30 phantom picks offsetting;
  surfaced per item 12's "or itself a finding" for the owner's lens-discount ruling.

## In plain terms
The two injured first-years now show their "out until 2027" tag on the board — that was a wiring slip
where the board drew a different copy of the player than the one the tag was stamped on; their scores
never actually changed. Every player's number is byte-for-byte what it was before; all I added is new
columns the app was already built to show: last-bake value, per-lever breakdown, and future-draft picks
that appear on the +1/+2 year views. Nothing in the rankings moved.

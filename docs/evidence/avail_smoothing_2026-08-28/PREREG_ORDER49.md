# PREREG — ORDER 49: THE AVAILABILITY EXPOSURE BLEND (TAU 2.5)

**Owner ruling (2026-08-28, verbatim): "Please lock in tau 2.5 and build that"** — ruled on the
tabled TAU=2.5 variant of the availability-smoothing study (AVAIL_SMOOTHING_STUDY.json /
AVAIL_SMOOTHING_VARIANTS.html, Variant A), after reviewing TAU 4 / TAU 3 / TAU 2.5 / cut-cap /
8-game-floor alternatives. Symmetric blend, no cut cap, no games floor.

## The law

For every row in the studied class, the finished price is the exposure blend of the two channels
the engine already prices:

    final = w · v_played + (1 − w) · v_sitter,      w = 1 − exp(−career_games / 2.5)

- `v_played` — the row's price through the full wrapped chain (ORDER 45 net + ORDER 46 final
  guard included), exactly as shipped today.
- `v_sitter` — the row's own scoring-stripped counterfactual through the SAME full chain (the
  verify_cf strip → price → restore method; D7-F6 exact-restore rule enforced with a HALT).
- Symmetric: thin evidence counts partially whichever way it points.

## The class (the STUDIED class, verbatim)

Y=2026 · tenure 1–4 (2026 − draft year + 1) · entry age < 22 (D3 mature-agers excluded, HALT on
missing `_by`) · career games 1–12 (a 0-game row already IS its sitter price; w(12)=0.992) ·
keyless synthetic probes pass through · retired rows pass through.

## Implementation

`engine/rl_after/_merged_recover.py`, ORDER 49 block — the OUTERMOST `ev` wrapper, installed
after the ORDER 46 FINAL GUARD, gated `RL_O49` (default '0' pre-landing; the landing flips the
default and pins the var in gate-mode config). Blends finished prices only; no downstream stage
reads a blended intermediate.

## Pre-registered acceptance (the candidate build must show, before landing)

1. **Kill-switch byte-exactness**: RL_O49=0 board == shipped board 530a4053 byte-exact.
2. **The movers ARE the table**: RL_O49=1 direct movers == the owner-approved TAU 2.5 table —
   79 movers, 70 down (−1,611) · 9 up (+146), net −1,465 board-side — same mover set and same
   deltas within ±1 per row (engine-currency vs board-currency rounding order; any row outside
   ±1, or any mover not in the table, is a FAIL and the landing does not proceed).
3. **Sitters unmoved**: every 0-game class row prices identically under the dial.
4. **Named anchors** (board currency): xavier-taylor 894→873 (−21), lachy-dovaston 680→654
   (−26), max-kondogiannis 414→411 (−3), dylan-patterson 1125→1133 (+8), daniel-annable
   1260→1285 (+25), oskar-taylor 624 unchanged — each ±1.
5. **D7-F6**: zero restore-violation HALTs across the full board build.

Landing then follows the standing transaction discipline (tools/landing): board install with
sidecars, movers model-change entry, UI bundles regenerated, register entry penned.

# #274 item 2 — the Best-23 eligibility selector: measured evidence

Measured 2026-07-30 on the adopted board `f2df6e0a` / store `6b9d00a7`. BEFORE = a clean worktree at
main tip `f1557b2` (the declared adoption stopgap); AFTER = this branch (the ruled selector).

## The law implemented

#271 Addendum 19: the value-maximal 23 fillable from the store's ELIGIBILITIES column, DPP-optimised
(assignment, not first-fit), on absolute board value. Solved as an exact min-cost max-flow, written three
times in lockstep — `ui/app/club_totals.js` (what the browser runs), `ui/tools/ingest_inputs.py` (the live
ingest), and the oracle transcription in `ui/tests/club_totals_parity.test.js`.

## The eligibility column, as carried

`ui/tools/extract_board_view.py` already opened the master store read-only and md5-verified for
`affl_team`; the ELIGIBILITIES column now rides the same read as `elig`. Measured at store `6b9d00a7`:

- **804 of 804** board players carry a non-empty column — no join gap (the store is keyed by board key).
- **Zero** tokens outside the six canonical slot codes.
- List lengths: **618** single-position, **186** dual-position (the DPP players).
- **Every** player's board `posCode` appears among his own eligibilities, so the eligibility axis is a
  strict superset of the modelling axis and the new selector can never return a worse 23 than the old one.
- The PUBLIC bundle does not carry `elig` — verified; the field is working-tier only.

## All 16 clubs at 23, all legally filled

Legality re-derived by an INDEPENDENT method (augmenting-path bipartite matching over the 18 slot
instances) that shares no code with the selector:

| | |
|---|---|
| clubs at exactly 23 distinct players | **16 of 16** |
| clubs legally filling all 18 positional slots | **16 of 16** |
| clubs where the top-23 by raw value is NOT legal | **10 of 16** — so legality is a real constraint |
| clubs whose top-23 IS already legal | **6 of 16**, and Best-23 equals that provable optimum for **6 of 6** |
| clubs exceeding the top-23 upper bound | **0** (impossible, asserted) |

## The two measured axis-artifact cases resolve (#271 A19's own evidence)

Under `posCode` — the modelling axis, which cannot see DPP — these two clubs could not fill the XVIII:

| club | roster | slots filled on the modelling axis | on the eligibility axis | MID-eligible vs grp-MID |
|---|---|---|---|---|
| Adelaide Crows | 46 | **16 of 18** | **18 of 18** | 13 vs 3 — **ten covers** |
| Hawthorn Hawks | 45 | **17 of 18** | **18 of 18** | 10 vs 4 — **six covers** |

Both cover counts match Addendum 19 verbatim. The named players, all selected into their club's Best-23:

- **Connor Rozee** (Adelaide) — `elig ["SD","MID"]`, `grp SD`, v=**2930** — matches A19's "Rozee SD,MID v=2930 foremost".
- **Will Graham** (Hawthorn) — `elig ["SF","MID"]`, `grp SF`, v=**1727** — matches A19's "Graham SF,MID v=1727".
- **Cameron Nairn** (Hawthorn) — `elig ["MID","SF"]`, v=784.
- **Charlie Edwards** (Hawthorn) — `elig ["SD","MID"]`, v=747.

A note on identification, recorded because it is the named hazard: the first lookup here resolved
"Graham" to `jack-graham`, who is Port Adelaide's Jack Graham (v=727), and briefly appeared to contradict
A19's figure. A19 is correct; the lookup was not. Identity by key, never by name fragment.

## Selector vs the stopgap, on the SAME board (the attributable comparison)

Deltas below hold the board fixed, so they measure the selector alone. Never negative — as the
eligibility-superset property predicts. **11 of 16** clubs improve; 5 are unchanged.

| club | stopgap | ruled selector | delta |
|---|---|---|---|
| North Melbourne Kangaroos | 49760 | 50807 | +1047 |
| St Kilda Saints | 49157 | 49897 | +740 |
| Hawthorn Hawks | 27443 | 28105 | +662 |
| Sydney Swans | 43601 | 44162 | +561 |
| Collingwood Magpies | 38242 | 38688 | +446 |
| Fremantle Dockers | 45812 | 46045 | +233 |
| Port Adelaide Power | 29887 | 30092 | +205 |
| Geelong Cats | 52581 | 52705 | +124 |
| Brisbane Lions | 33096 | 33197 | +101 |
| Western Bulldogs | 48992 | 49031 | +39 |
| Adelaide Crows | 36208 | 36235 | +27 |
| West Coast · Melbourne · Carlton · Richmond · Essendon | unchanged | unchanged | 0 |

## Parity and non-vacuity

`ui/tests/club_totals_parity.test.js` — **17 of 17** (was 11 of 11; six assertions added). The reader and
the oracle agree club-for-club, metric-for-metric, and on the ordered Best-23 KEYS, not merely the total.
Levers proven able to fail: a deliberately wrong selector (flow sign flipped, so it picks the cheapest
legal 23 — still legal, so it tests the SELECTION and not a crash) is rejected; a moved player value still
agrees and does change the totals; the top-23-by-raw-value is shown genuinely illegal for 10 of 16 clubs.

## Not shipped, deliberately

`ui/data/club_valuation.js` and `ui/data/ownership.js` are the live ingest's outputs and are left at their
committed state. Running the ingest was attempted and REVERTED — see `02_item2_FINDING_ownership.md`. The
baked club totals in `club_valuation.js` are not read by any UI code (asserted by the parity suite), so
the selector change reaches the owner's screen through the browser computation regardless.

The shipped `ui/index.html` was loaded from `file://` with no server for every capture, zero page errors.

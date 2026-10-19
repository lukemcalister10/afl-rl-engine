# `data/delivered_value/` — LAYER 1, THE DURABLE HARVEST

**This directory is a first-class, pinned dataset. It is NOT evidence for one exercise, and it is
deliberately not under `docs/evidence/`.** Ruling 11 of ORDER 26B (#334 comment 5269952564) creates it
and says it is "kept beyond the exercise".

| file | what | md5 |
|---|---|---|
| `layer1_player_seasons.json` | the dataset | `ad1229ea6f443538479447132382b21c` |
| `layer1_player_seasons.json.md5` | its pin | — |

Builder: `docs/evidence/delivered_value_2026-08-12/o26b_layer1.py`
Source store: `engine/rl_after/rl_model_data.json` md5 `d9a24282357cf3083b1640466e3ecd83`

## THE LAW OF THIS FILE

**Raw facts only. No valuation field may ever be added.** No price, bar, discount, games weight,
projected tail, or tier-as-a-weight. Everything of that kind is Layer 2, which is recomputable from this
file in seconds and which may change as often as the owner rules. Layer 1 must survive all of it.

## CONTENTS

- `entries` — **2,650** rows, one per player: mechanism/pathway, pick, effective pick, entry year, debut
  year, birth year and date, **entry age** (100 % coverage — the DOB courier act landed), day-0
  (acquisition-slot) position, present and future position, career games on both bases, retired flag,
  window-tier label.
- `player_seasons` — **11,484** rows, one per played season: year, games, average, **position played**
  that season, position group.

Ruling 5's *two uses of position* are carried explicitly and neither is collapsed into the other:
`day0_position` is the acquisition slot; `position_played` is the season's own position.

| mechanism | entries | seasons | seasons/entry |
|---|---|---|---|
| ND 1-64 | 1448 | 8191 | 5.66 |
| RD | 691 | 2071 | 3.00 |
| ND>64 | 122 | 445 | 3.65 |
| MSD | 106 | 199 | 1.88 |
| UNR | 59 | 125 | 2.12 |
| IRE | 57 | 131 | 2.30 |
| SSP | 52 | 125 | 2.40 |
| PDA | 51 | 112 | 2.20 |
| PDN | 43 | 59 | 1.37 |
| PDS | 21 | 26 | 1.24 |

Window tiers (Ruling 8, as a **label** on the entry year only): core ≤2014 **1443** ·
augmented 2015–2021 **761** · sensitivity 2022+ **446**.

## DETERMINISM

The file carries **no build timestamp**. Re-running the builder against the same store reproduces the
same bytes and the same md5 — verified twice at build. A pinned dataset with a timestamp in it is not
pinned.

## WHAT IS DELIBERATELY ABSENT

Ruling 8's tier-2/3 **projected tails**. They are produced by the engine's band machinery — the object
ORDER 26B's identity gate stopped on. Their absence is also recorded inside the file's own `omissions`
block so that a later seat cannot read this as a complete tier-2/3 input.

## TWO STORE ANOMALIES MEASURED AT BUILD (recorded, not corrected)

Both are carried in the file's `_doc` block with their counts:

1. **The #323 derive rule does not hold on store `d9a24282`.** `record['games'] == sum(scoring games)`
   was verified 2650/2650 on store `f1e7f20c` (#334 stage A, 2026-08-06). Today **457 records** breach
   it. Every one is an active record carrying a 2026 season row and the lag is **1 or 2 games** — the
   career-games counter is a round-lagged snapshot of the in-progress season. Both numbers are carried
   per entry (`career_games_store`, `career_games_from_seasons`); neither is corrected, because
   correcting a store field is an execution act on the owner's word.
2. **Two historical rows violate the ruled zero-row convention.** #334 addendum 1 (2026-08-06) ruled that
   a did-not-play season carries **no row**, and noted that row *presence* keys the walk-forward horizon.
   `tim-mohr` 2015 and `stewart-crameri` 2016 are written as explicit `games=0 / avg=0.0` rows. (A
   further 142 zero rows sit in the in-progress 2026 season; those are listed-not-yet-played
   placeholders, a different thing.)

Both anomalies are asserted in bounded form by the builder, so a *widening* of either would halt it.

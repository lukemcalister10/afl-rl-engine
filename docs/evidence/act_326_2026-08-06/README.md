# #326 SECOND REHEARSAL — per-division pool ENTRY ANCHORS · 2026-08-05/06

Nothing was pushed and nothing was committed. Everything below lives on a working copy cut from main
tip `a6f6076`, at
`/tmp/claude-0/-home-user-afl-rl-engine/52aec7aa-3e34-5a29-a45f-2e2388143230/scratchpad/rehearsal_326`.

## What was built

The owner's consumption ruling (addendum 5, as amended by addendum 6) put the signed levels where the
pick curve stands for a national draftee: they are the ENTRY ANCHOR a pool entrant's price starts from
before he has a record, and they fade out as games arrive exactly as the national path already fades.

Three sites consume the anchor, and only three:

| site | file | currency | what changed |
|---|---|---|---|
| the thin-record blend | `_merged_recover.py` `sitout_ev` | engine value (level x 1.0524) | a pool entrant blends off his division's level instead of the pool-slot-derived V0 |
| the year-zero floor | `_merged_recover.py` the OUTERMOST `ev` binding | engine value (level x 1.0524) | scope extended from national draftees to engine-pool entrants; basis is the level |
| the ruck prior cap | `_merged_recover.py` `_cap_basis` at `_ruc_ceiling` / `_ruc_prior_cap` / the `ev` fallback | ladder (unconverted) | a pool ruck's cap basis is his division's level, not the ladder's one pool slot |

Left alone deliberately (addendum 6 item 4), byte-for-byte: the staleness cap, the mediocre cap, the
delisted remnant. They face players with real careers and back-boards; moving them is one owner sentence
away and is not this act.

## The gates

| gate | result | evidence |
|---|---|---|
| 0 baseline reproduced | `2b7c1a00` byte-reproduced before any edit | `gate0_baseline_md5.txt` |
| 1 determinism | two builds, both `864b6726` | `gate1_determinism.txt` |
| 2 parity at eps 0 | 804/804 board v == engine gated ev() | `gate2_parity.txt` |
| 3 selftest | 145 PASS / 0 FAIL | `gate3_selftest_asbuilt.txt` |
| 3 REDs | wrong level · wrong position field · currency (3 ways) · silent refit · isolation | `gate3a…gate3e`, `gate5_…`, `gate7_nosilentrefit_RED.txt` |
| 4 reach-the-entry-price | all 14 levels, route + entrant + price recorded | `gate3_selftest_asbuilt.txt` (section 10) |
| 5 wrong-field discriminator | halts the build, naming its 171 rows | `gate5_wrongfield_build_RED.txt` |
| 6 attribution | 177 movers, every one engine-pool-classified; 0 non-pool | `gate6_attribution_classified.txt` |
| 6b ruck-cap route | 14 rows enumerated by paired build | `gate6_ruckcap_route_enumeration.txt` |
| 7 frozen surface | signature `af556bdc` LOADED from `v0surf.pkl` (`d594dc03`), no refit | `gate7_frozen_surface.txt` |
| 8 non-pool byte-identity | 825 of 1002 rows identical in every field; every differing row is pool | `gate8_nonpool_byte_identity.txt` |
| 9 MSD caveat | printed beside the level in the build, the selftest and the artifact | `gate9_msd_caveat.txt` |
| B5 re-scope | both bars 0, verdict FEATURE | `gate9_B5_rescope.txt` |

## Read these too

* `HALT_AND_ASK.md` — three things the record and the code disagree about. None of them blocked the
  work; all three are the owner's or the seam's call, not the implementer's.
* `REPIN_RECONCILIATION.md` — every identity: re-pinned, self-rebuilding, or deliberately left.
* `RUN_COMMANDS.md` — the exact re-run recipe.
* `rehearsal_326b.patch` — the implementation (base `a6f6076`), excluding the two regenerated
  artefacts (the board and the two UI bundles) which rebuild from it.

## Per-level proof (from `gate3_selftest_asbuilt.txt`, section 10)

Every level was proven on a REAL entrant found from the population at build time — no hardcoding, no
synthetic rows. On the floor route the shipped price IS the year's floor fraction times the signed level,
because the anchor multiplies by the board factor and the export divides by it again.

| level | value | tier | live | re-priced | route | entrant | board price |
|---|---|---|---|---|---|---|---|
| IRE | 133 | live | 14 | 12 | floor | Conor McKenna | 7 = 0.05 x 133 |
| MSD | 286 | live | 63 | 37 | floor | Jordan Boyd | 37 = 0.13 x 286 |
| ND65+ | 185 | live | 28 | 11 | floor | Nathan Broad | 10 = 0.05 x 185 |
| PDA | 194 | live | 15 | 7 | floor | Harry Cunningham | 10 = 0.05 x 194 |
| PDN | 123 | live | 16 | 7 | blend | Ricky Mentha | 52 |
| PDS | 145 | probe: retired rows lifted, evaluated, restored | 0 | 20 of 21 | floor | William Langford | 8 |
| RD:KPD | 300 | live | 8 | 3 | floor | Jordon Butts | 15 = 0.05 x 300 |
| RD:KPF | 216 | live | 6 | 1 | floor | Brody Mihocek | 10 = 0.05 x 216 |
| RD:MID | 294 | live | 12 | 5 | floor | Jack Watkins | 132 = 0.45 x 294 |
| RD:RUCK | 282 | live | 9 | 4 | blend | Vigo Visentini | 167 |
| RD:SD | 246 | live | 16 | 2 | floor | Dane Rampe | 12 = 0.05 x 246 |
| RD:SF | 231 | live | 15 | 5 | floor | Bailey Banfield | 11 = 0.05 x 231 |
| SSP | 252 | live | 28 | 12 | floor | Mykelti Lefau | 70 = 0.28 x 252 |
| UNR | 103 | live | 13 | 11 | floor | Mark Blicavs | 5 = 0.05 x 103 |

MSD's level is shown with its completion-optimism caveat (+4.7-8.4%) everywhere it appears.

## Direction, by division (`gate6_attribution_classified.txt`)

177 rows differ in any field; 123 of them in the 2026 price. Zero non-pool movers.

| division | rows touched | price up | price down | price same (lens years moved) |
|---|---|---|---|---|
| MSD | 56 | 20 | 14 | 22 |
| SSP | 19 | 10 | 2 | 7 |
| ND65+ | 17 | 2 | 11 | 4 |
| UNR | 15 | 6 | 8 | 1 |
| IRE | 12 | 3 | 7 | 2 |
| PDA | 12 | 2 | 4 | 6 |
| PDN | 11 | 0 | 8 | 3 |
| RD:RUCK | 10 | 7 | 3 | 0 |
| RD:SF | 8 | 2 | 3 | 3 |
| RD:MID | 7 | 1 | 4 | 2 |
| RD:KPD | 5 | 2 | 1 | 2 |
| RD:SD | 3 | 1 | 1 | 1 |
| RD:KPF | 2 | 1 | 0 | 1 |
| PDS | 0 | — | — | — (all 21 rows retired) |

The confirmed direction holds: UNR / IRE / PDN cut, PDA mixed-leaning-down, MSD and the rookie rucks
mostly rise, ND65+ re-bases down onto min(266.1, curve[64]) = 185.

## Landing note (supervisor-seat, 2026-08-06)
The three full-board JSON dumps from the rehearsal evidence (baseline `2b7c1a00`, rehearsed `864b6726`,
and the ruck-cap ablation build) are NOT duplicated here: the baseline is the prior main artifact and the
rehearsed board IS this act's committed `data/rl_build/rl_app_data.json` — both live in git history, and
their md5s are recorded throughout the gate files. Owner words landing this act (owner-occupied channel,
2026-08-06): "Keep as ruled. Land it." — the pool-veteran floor reach (HALT 1) stands as ruled.

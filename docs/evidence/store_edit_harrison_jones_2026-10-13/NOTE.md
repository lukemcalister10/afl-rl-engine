# Harrison Jones — the retired twin's 2026 game (store-edit spec, Phase 0.3, 2026-10-13)

**Status: spec written and validated (`tools/landing/spec.validate` -> no problems); NOT flown.**
The owner's word goes into `owner_word` verbatim before `tools/land edit --spec
docs/evidence/store_edit_harrison_jones_2026-10-13/ACT_SPEC.json --dry-run`.

## The finding

| row | `_retired` | 2026 row before | career `games` before |
|---|---|---|---|
| `harrison-jones-haw` (Hawthorn RD5 2017, b1999, last game 2020) | true | `{games 1, avg 15.0}` | 2 |
| `harrison-jones` (Essendon ND30 2019, b2001) | false | `{games 7, avg 43.86}` (sum 307.0) | 66 |

**Who credited the 15?** Nobody in the repo's own record:

* `ui/data/movers.js` reports 15..29 carry one Harrison Jones only — `harrison-jones` (Essendon) —
  played R16 **47**, R18 **55**, R21 **67**, R23 **22**, R24 **55**; DNP in 15, 17, 19, 20, 22 and every
  finals week. No report in 15..29 carries a score of 15 for anybody named Jones.
* `scores/R21.csv` 67, `scores/R23.csv` 22, `scores/R24.csv` 55 are those three; `FW1-FW4`, `GF`
  and `docs/evidence/ingest/**` do not list him (FW4's spec touches `harrison-jones` only for the
  career-games re-sum 63 -> 66).
* `git log -S'"key": "harrison-jones-haw", "games": 2' -- engine/rl_after/rl_model_data.json` names
  exactly one commit: **f4a4d34f, 2026-07-02, the initial seed**. The twin's 2026 row predates every
  in-repo writer. In that seed the Essendon row read `{2 games, 30.5}` (sum 61).

**Duplicate or missing?** 61 (seed, 2 games) + 246 (the five reports above) = 307 = 7 x 43.86: the
Essendon row's 7-game average is accounted for by the seed's two games plus the five reports, and the
15 is not one of the five. So it is a duplicate only if the pre-repo R1-R14 baseline wrote one
appearance to BOTH rows. Every writer this tree has (the catch-up's identity law, `tools/ingest`'s
`resolve_names`, `score_ingestor`'s resolver) writes each listed appearance ONCE, to one key, and
resolves to ACTIVE rows only — a retired twin can only receive a game from a name-join that picked the
wrong row, which writes it there INSTEAD OF the active row, not as well. The finding is therefore
**a game the Essendon row is missing**, and the spec moves it:

* `harrison-jones-haw`: `scoring[2026].games` 1 -> 0, `scoring[2026].avg` 15.0 -> 0.0 (the store's
  own shape for a zero-game season row, 136 such rows), `games` 2 -> 1.
* `harrison-jones`: `scoring[2026].games` 7 -> 8, `scoring[2026].avg` 43.86 -> **40.25**
  (`ScoreIngestor._mean(307.0 + 15, 8)` at `ROUND_DECIMALS = 2`, exactly as `tools/ingest` computes
  a week), `games` 66 -> 67 (career = sum of season rows, owner ruling 2026-09-24; the next weekly
  ingest halts on a career count ABOVE the sum, so the twin's career field must move with its row).

If the owner rules it a duplicate instead, delete the three `harrison-jones` edits from `edit.store`;
the three `harrison-jones-haw` edits stand either way.

## Proven without a landing

`tools/landing/steps.apply_store_edits` (the lander's own pure applier) was run on the live store
text in memory: all six edits apply, only the two rows differ, both re-parse, `json.dumps(json.loads)`
round-trips the result byte-exact (1,978,067 -> 1,978,066 bytes), and both rows' career games equal
their season sums afterwards. `season_state.derive` on that edited store moves `source_store_md5`
only — the exposure clock's values are unchanged relative to the same derivation on the live store.

## One landing precondition the seat must know

The live `data/season_state.json` HOLDS `exposure_pace` at the round-24 value (0.909) while a fresh
`season_state.derive` of the live store already reads 0.955 (the finals games lifted the durable
median 20 -> 21). The lander's `store_edit` season-clock step compares the live file to the derivation
of the edited store and allows the hold ONLY for a column whose id carries a finals prefix
(`_finals_exposure_hold`, `feed_round_of`). This act is not a finals week, so its honest column id
(`harrison-jones-twin-game-13-10`) will meet that step as "exposure_pace 0.909 -> 0.955" and halt —
exactly as ANY post-finals out-of-round store edit on this tree would. The round-24 view of the
edited store (the twin's game subtracted back, the Essendon game added back) re-derives 0.909
exactly, so the hold is correct for this act too; generalising the hold to "the calendar holds at 24
and the finals reports are on record" is a one-step lander change outside this act's scope and is
left to the seat, deliberately, rather than mislabelling the column `gf-` to slip past it.

## Board effect

`harrison-jones` is active (board `v` 153, Essendon); `harrison-jones-haw` is a back-section row
(`v` 12). Both may move; `expected_movers` is null (the dry run is the prediction of record), the
board is declared moving, and the column is owed under the standing rule of 2026-07-28.

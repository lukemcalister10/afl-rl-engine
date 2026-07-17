# viewing_pack.py — build transcript (2026-07-17, seat 11)

Tool: `tools/seat/viewing_pack.py` — the owner viewing pack. Two board files in, one
self-contained owner-readable HTML + a `.md` twin out. Every count is computed from the two
boards at generation time and stamped with both input md5s; the tool never accepts a count as an
argument. Reuses `board_diff.by_key` / `board_diff.fnum` (one source). Schema ingested: the
`data/rl_build/rl_app_data.json` board only (top-level object, `active` array of rows carrying
`key`/`name`/`v`/`grp`/`age`/`pk`/`levers`). RED-PATH refuses (loud, non-zero) on schema-unknown
boards and on md5-identical inputs.

## Supervisor known-answer test — FIXTURES NOT PRESENT IN THIS REPO

The directive's KAT names two committed boards as base/cand:
`273463e:data/rl_build/rl_app_data.json` (md5 `8d90c9ac`) → `6306378:data/rl_build/rl_app_data.json`
(md5 `ee70335a`), expected: value-up-rank-down = 119 · movers = 393 · net ΣΔ = +15533 · 804 common,
positional ranks with key tie-break.

Those commits do not exist in `lukemcalister10/afl-rl-engine`: `git cat-file -t 273463e` and
`6306378` both report "Not a valid object name", they are absent from the object store (loose and
packed) and from the on-disk `rl_after` workspace, and **every one of this repo's 50 commits carries
the byte-identical board `790136a3`** — the `8d90c9ac`/`ee70335a` board content appears nowhere
reachable. I therefore could **not** run the supervisor KAT, and I am **not** stating its four
numbers as reproduced, because I did not reproduce them. If the two boards are added to the repo (or
provided as files), the tool is built to consume them directly:
`viewing_pack.py --base 8d90c9ac.json --cand ee70335a.json --out <dir>`.

## Substitute known-answer test — VERIFIED (same schema, hand-computed)

To verify the counting logic that the supervisor KAT would exercise (movers, up/down split, net ΣΔ,
positional ranks with key tie-break, and the value-up-rank-down failure ledger), I ran the tool over
a 6-row in-schema fixture pair whose answer is hand-computable:

| quantity                       | hand-computed | tool output |
|--------------------------------|:-------------:|:-----------:|
| common active rows             | 6             | 6           |
| movers                         | 4             | 4           |
| movers up / down               | 3 / 1         | 3 / 1       |
| net ΣΔ                         | +56           | +56         |
| value-up-rank-down (failures)  | 2 (`aaa`,`bbb`) | 2         |

Ranks base `{aaa:1,bbb:2,ccc:3,ddd:4,eee:5,fff:6}` → cand `{ccc:1,aaa:2,bbb:3,ddd:4,fff:5,eee:6}`.
`aaa` (100→101) and `bbb` (90→95) both gained value yet were passed by `ccc` (80→150) and so lost a
rank — exactly the failure-ledger definition. Tool reproduced all five figures.

RED-PATHs verified: md5-identical inputs → refuse (exit 1); led_default-shape `{key:{num}}` → refuse
(exit 1); top-level list → refuse (exit 1); missing required arg → refuse (exit 1).

## Sample pack (committed)

`board_base.json` (real committed board, md5 `f14d6160`) → `board_cand.json` (a deterministic,
RNG-free perturbation, md5 `5b32d027`), 804 common rows: net ΣΔ **+3233** · movers **335** (up 174 /
down 161) · value-up-rank-down **14**. Rendered `viewing_pack.html` (+ `.md` twin) carry the headline,
the named-players table (from `names.txt`, resolved by key and by name substring), the failure ledger,
and the full movement ledger as a collapsible appendix, with L1–L5 per-stage attribution columns on
the risers/fallers. The HTML is self-contained (no external references).

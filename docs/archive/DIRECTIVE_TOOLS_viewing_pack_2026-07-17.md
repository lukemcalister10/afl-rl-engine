# DIRECTIVE — THE OWNER VIEWING PACK (tools/seat/viewing_pack.py)
2026-07-17 · supervisor seat 11 · Opus · ONE JOB, ONE CHAT · disjoint-file (runs in parallel, S3)
STATUS: ISSUED — fire when pasted by the owner.

## BASE — same block as the base-guard directive (branch `claude/tools-viewing-pack` from origin/main;
## main at-or-after bee58cc7…, docs/-only diff from it; proof committed first). If the base-guard job
## has landed first_commands.sh on main by the time you start, USE IT.
**MERGE ORDER (owner-sequenced, no conflict):** this job and the base-guard job both write only NEW
files under `tools/seat/` (viewing_pack.py here; first_commands.sh there) EXCEPT the base-guard job
also edits the existing `prescreen.sh`. This job edits NO existing file, so the two candidates are
disjoint and merge in either order. Do not touch `prescreen.sh` or `first_commands.sh`.

## THE FIVE
EFFORT: Medium (a formatting tool over committed artifacts; zero valuation logic — why not Low: it
must be trustworthy enough that the owner reads it INSTEAD of raw JSON, so its numbers carry proofs).
MODE: auto; PLAN first. TIME: 1–2 h. FEED: the item-256 ledger schema (register grep — ranks carried) ·
item 295 (the positional-rank tie-break of record) · tools/seat/board_diff.py (reuse its board-load
+ diff, don't duplicate — SSI spirit applies to code). FENCE: `tools/seat/` +
`session_2026-07-17/viewing_pack/` ONLY.

## THE JOB
`tools/seat/viewing_pack.py --base <board.json> --cand <board.json> [--names <file>] --out <dir>`
emits ONE self-contained owner-readable HTML (plus a .md twin) carrying, in this order:
1. The headline: net ΣΔ · movers up/down · the three biggest rises and falls WITH per-stage
   attribution columns when the inputs carry them.
2. THE NAMED ROWS table (from --names, or a sensible default of the biggest movers): value
   before → after · rank before → after (POSITIONAL ranks, ties by key — item 295's convention,
   stated in the artifact's footer) · position/bar columns.
3. THE FAILURE LEDGER (value-up-rank-down subset) — full named list with ranks.
4. THE MOVEMENT LEDGER (all-active) — collapsible/appendix.
Every count in the artifact is computed by this script from the two boards at generation time and
stamped with both input md5s (S1 pattern) — the tool NEVER accepts a count as an argument.
League-manager language in all headings; jargon only in footnotes.
RED-PATH: refuse (non-zero, loud) on schema-unknown boards or md5-identical inputs.
**SCHEMA (single, explicit):** the tool ingests the `data/rl_build/rl_app_data.json` board schema
ONLY — the object at top level, its `active` array of rows carrying `key`, `name`, `v` (value),
`grp`, `age`, `pk` (and the ranks derived from `v`). Both `--base` and `--cand` are files of THIS
schema. Do NOT ingest the `led_default.json` measurement artifact (a different schema, `{key:{num,…}}`)
— it is not a board and is not an input here.
**KNOWN-ANSWER TEST (verified by the supervisor 2026-07-17 in this exact schema):** run over the two
COMMITTED boards `273463e:data/rl_build/rl_app_data.json` (md5 `8d90c9ac`) as --base and
`6306378:data/rl_build/rl_app_data.json` (md5 `ee70335a`) as --cand. The tool MUST reproduce, on the
804 common active rows: value-up-rank-down (failure-ledger) rows = **119** · movers = **393** · net
ΣΔ = **+15533** · ranks POSITIONAL, ties by key. State all four in the committed transcript; a
mismatch on any is a build failure. (NB these are the 8d90c9ac→ee70335a figures, NOT the item-295
115 — that used f2f077b2 as its base, which is a measurement board not committed as an rl_app_data
board. This test uses the two boards that ARE committed in this schema.)

## RETURN
≤20 lines · branch + head SHA + PR · the sample pack committed · "in plain terms" close.

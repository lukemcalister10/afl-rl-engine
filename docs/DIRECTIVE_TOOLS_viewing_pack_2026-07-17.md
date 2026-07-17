# DIRECTIVE — THE OWNER VIEWING PACK (tools/seat/viewing_pack.py)
2026-07-17 · supervisor seat 11 · Opus · ONE JOB, ONE CHAT · disjoint-file (runs in parallel, S3)
STATUS: ISSUED — fire when pasted by the owner.

## BASE — same block as the base-guard directive (branch `claude/tools-viewing-pack` from origin/main;
## main at-or-after bee58cc7…, docs/-only diff from it; proof committed first). If the base-guard job
## has landed first_commands.sh on main by the time you start, USE IT.

## THE FIVE
EFFORT: Medium (a formatting tool over committed artifacts; zero valuation logic — why not Low: it
must be trustworthy enough that the owner reads it INSTEAD of raw JSON, so its numbers carry proofs).
MODE: auto; PLAN first. TIME: 1–2 h. FEED: the item-256 ledger schema (register grep) · item 295
(the positional-rank tie-break of record) · tools/seat/board_diff.py (reuse, don't duplicate — SSI
spirit applies to code). FENCE: `tools/seat/` + `session_2026-07-17/viewing_pack/` ONLY.

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
PROOF: one committed sample run over the two committed boards `273463e:…led_default.json`-derived
values vs `6306378:data/rl_build/rl_app_data.json` — its 115-row failure subset MUST reproduce the
item-295 verified count (the known-answer test), stated in the transcript.

## RETURN
≤20 lines · branch + head SHA + PR · the sample pack committed · "in plain terms" close.

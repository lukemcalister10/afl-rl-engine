# SPEC — THE SEASON-ROLLOVER RUNBOOK · v1 · 2026-07-16 · seat 9 (Fable)
### Owner-shaped (items 218 + this turn's two refinements). DESIGN ONLY — the build is a small
### post-bake chapter (the hygiene leg touches the engine; the lane is held). Ratified acts become
### law at that chapter's directive.

## THE TWO OWNER REQUIREMENTS THAT SHAPE EVERYTHING
1. **STAGED, NOT ATOMIC:** the off-season acts land WEEKS apart — the engine must be FULLY VALID at
   every intermediate state, indefinitely. Therefore: five INDEPENDENT, IDEMPOTENT acts + a
   committed **`data/season_state.json`** (which acts applied · when · by whom · the pins each
   moved) that every build/guard reads. Guard 6 (new): a build asserts its behaviour matches the
   state file — no act half-applied, no act assumed.
2. **ORDER TOLERANCE:** announced positions (act V) may precede the draft (act IV). Acts declare
   PRE-CONDITIONS, not positions in a sequence: V requires only II; IV requires only II; III is the
   DEFAULT that II installs and V supersedes whenever it lands.

## THE FIVE ACTS (each: one command · validate-or-halt · idempotent · state-file entry)
**I. SEAL** — the completed season's walk-forward book becomes history-of-record (tag + md5 pin).
   Pre: season's final scores ingested. Post: nothing else changes; pure record.
**II. ROLL** — BASE_REF/AGE_REF advance one year. Pre: I. REQUIRES THE HYGIENE LEG FIRST: the
   `==2026` literals (rl_model.py:354/368/676/810/921 verified) become config, pinned in the
   manifest, with a byte-identity proof at the old year (the roll is then ONE config move). Post:
   every player ages one year; the season-progress denominators re-anchor; LTI `out_until_<Y>`
   entries where Y ≤ the new year RESOLVE (dropped by the act, logged).
**III. INTERIM POSITIONS (installed BY act II, no separate trigger)** — until V lands, the year-0
   leg reads the owner's FUTURE PRIMARY as present. One convention, engine-wide, reversible.
**IV. DRAFT INTAKE** — new players minted (stable afl-player-v1 IDs; DOB/pick/positions from the
   owner's draft file), priced pure-pedigree at V0 off the LIVE curve (the existing pre-debut
   branch — machinery real today); drafted picks retire into their players; next-year picks enter
   the ledger; the future-pick discount re-anchors. Pre: II + the post-draft owner file.
**V. ANNOUNCED POSITIONS** — the normal locations refresh (the shipped no-LLM flow): present
   positions land, III's convention retires, the future blend pushes to +1. Pre: II + the owner's
   file. MAY PRECEDE IV (order-tolerant by construction).

## THE PHANTOM DRY-RUN (owner-proposed; adopted as the acceptance instrument)
Before the first real off-season: an ISOLATED sandbox copy runs the full runbook against a
synthetic off-season — dummy draft class (phantom IDs, marked), a scrambled announced-positions
file, BOTH act orders (IV→V and V→IV), an LTI entry that resolves and one that doesn't, and a
double-application of every act (idempotence proof). PASS = every intermediate state builds a
valid board, guards green, and the final state matches a hand-computed expectation sheet the owner
signs before the run (the sealed-reads pattern applied to a process).

## SEQUENCING (honest)
The chapter (Legs B–E + bake) → ingestion go-live (the store-write + the LTI re-pin tool + the
weekly wrapper) → THE ROLLOVER CHAPTER (hygiene leg → the five acts + state file + Guard 6) → the
phantom dry-run → the real off-season, rehearsed. The spec is ready NOW so the chapter is a build,
not a design, when its turn comes.

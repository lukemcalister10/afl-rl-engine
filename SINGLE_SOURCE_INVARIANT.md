# THE SINGLE-SOURCE INVARIANT — v1.3 — read this before touching data or code
### CHANGELOG v1.3 (2026-07-13, header corrected 2026-07-14): SILENCE IS A RED added to THE
### DISCIPLINE THAT MAKES THEM REAL. A RULE WAS ADDED and the header was left at v1.2 in error —
### which left two materially different documents both calling themselves v1.2. Corrected here.
### The v1.2 line below stands as written and applies to v1.2 only.
### CHANGELOG v1.2 (2026-07-08): retired-doc pointer fixed — the discipline block referenced "the latest
### KICKOFF §0"; KICKOFF is retired (merged into CORE). No rule changed. v1.1 changelog: archive/CHANGELOG.
### FILE NOTE (filed to the repo 2026-07-13, at the v2.9 seam): this file's REPO copy was behind v1.2
### until now. The filename carries NO version by design (a versioned duplicate would be a lookalike of
### the very document that forbids lookalikes) — the VERSION lives in this header.
### Binding on every build and every supervisor. This is not guidance; it is the acceptance bar. If a change would violate it, STOP.

## THE ONE RULE (plain)
There is **exactly one** authored source of truth: `engine/rl_after/rl_model_data.json`.
- **Never create a second copy of it.** No `.bak`, no `.stageN`, no `_v2`, no "working copy."
- **Every other data file is DERIVED** — generated from the source, read-only, and disposable. The board, the book, the matrices: all regenerated, never hand-edited.
- **If you need different data, change the source.** Not a copy. The source.
- **Retire a feature → strip its fields from the source and code.** Delete, don't disable. A copy earns its existence only as a generated, stamped, read-only artifact — never a hand-edit.

Why this exists: every failure in this project's history — the phantom-repo scare, the `.pre_stage0` revert, the Kako wipe, the stale-boot day — was the same thing: a stale copy read as if current, or an edit made to a derived copy the next rebuild overwrote. Rules in prose didn't stop it. The guards below do, because they make a stale read **fail the build loudly** instead of sitting silent.

## THE FIVE GUARDS (mechanical — each must FAIL/HALT the build, never warn)
1. **One writable source; derived files read-only + source-stamped.** The generator is the only writer of derived files; it marks them read-only and writes the source md5 into each. A hand-edit to a derived file does not survive the next rebuild — so forking earns nothing.
2. **Source-hash assertion on startup.** Every derived artifact carries the md5 of the source it was built from. Every build's first step asserts that stamp == current source md5. Mismatch → HALT.
3. **Lookalike tripwire in the self-test.** The self-test scans the source directory and FAILS if more than one file matches the source pattern (`rl_model_data*.json`). A second lookalike becomes a red test the next build can't pass, the moment it's created.
4. **Correction-sticks canary (permanent).** Write a throwaway edit to the source, run a full rebuild, assert it survives to board + book. Kept in the suite forever: "did a copy or a revert path sneak back?" is answered automatically every build, not discovered when a player's data vanishes again.
5. **Boot-store assertion (added 2026-07-06, `boot_guard.py` + `data/expected_boot.json`).** The other four guards validate whichever directory they run from — so a stale *workspace* (v2.4 data agreeing with v2.4 data) passes them all while the board is wrong. Guard 5 pins the expected store in one manifest and asserts, on ENTRY of every gate/bake/panel/self-test script (before the engine loads), that the store being read matches the pinned source md5. A build that boots on the wrong store HALTS on line one instead of running five confused turns deep. This closes the *base* half of the divergence problem; guards 1-4 close the *data* half.

## THE DISCIPLINE THAT MAKES THEM REAL
- Each guard is wired to **STOP the build**, never to log a warning. A tripwire nobody reads is worse than nothing.
- **SILENCE IS A RED (CORE v2.5, 2026-07-13).** A guard that produces no result — it crashed, its input was missing, its output was swallowed by a pipe — has FAILED, not passed. Every check produces a verdict or HALTs; every harness propagates a non-zero exit. (Why: a BINDING gate raised an exception behind a `| tail -8` and the suite reported PASS.)
- The pipeline is **not "done" until all five pass** from a fresh bootstrap.
- CORE (THE INVARIANT) summarises this block for every seat; this file is the full spec — read it before any data or code work.
- **Navigate by branch name + git SHA, never a store md5.** A store hash is a content check, not a place to stand. (Confusing the two cost real time on 2026-07-05.)

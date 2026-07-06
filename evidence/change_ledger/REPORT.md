# CHANGE LEDGER — build + validation, and the F1/F2 identity-gate confirm  (Wave-0b)

Base: Wave-0a candidate `claude/wave0a-dpp-deadcode-strip-hcalwi`, HEAD `9b5aba37`.
Store `engine/rl_after/rl_model_data.json` md5 = `e1b4d8bf` (== pinned). No engine re-fit, no
source-data edit, no gate modification, `main` not promoted.

---

## PART 1 — the tool  ·  `tools/change_ledger.py`

A committed, re-runnable tool that takes TWO board states (before, after) and prints a plain,
**descriptive** "what moved" report in league-manager language (names + dollars). It is
**descriptive only** — it does not score, gate, abort, or judge "better/worse". A board artifact is
either the full app-data JSON (object with an `active` list) or a bare list of player rows; each row
carries `key`, `name`, position `grp`, draft cohort `yr`, pick `pk`, and the five SCAR value fields
`v / vM1 / vM2 / vP1 / vP2` (= `ev(player)` as of 2026 / 2025 / 2024 / 2027 / 2028).

    python tools/change_ledger.py <before.json> <after.json> [--top N]

It emits:
- **Per-player SCAR delta** — before→after, absolute ($) + %, for every one of the five fields that moved.
- **Grouped roll-ups** — by **position** (`grp`), by **draft cohort** (`yr`), and by **magnitude bucket**
  (`0 / <2% / 2–5% / 5–10% / >10%`; a player is bucketed by its largest |%Δ| across the five fields).
- **Top-N movers named**, both directions (player name + before→after on the present-season price `v`).
- **A one-line headline** — "N of M players moved; max Δ = X ($ and %) on <player>; concentrated in
  <group>; K columns added/dropped."
- **Zero-noise on a no-op** — if nothing moved it says so cleanly (the Wave-0a case, below).

---

## PART 2 — validation

### (a) Zero-delta known-answer  (the Wave-0a cleanup — MUST be 0 moved)  → `zero_delta_run.txt`

- **before** = the shipped baked board `data/rl_build/rl_app_data.json` (blob identical to
  `origin/main@7bc5726`; md5 `7d1eeef8`).
- **after** = the board freshly built from the Wave-0a engine (`bootstrap.sh` → `rl_export.py`),
  frozen here as `board_wave0a_built.json` (md5 `1d6907e8`) — the DPP strip drops the `gf`/`fut`
  export columns.

Result — exactly the known answer:

    HEADLINE: 0 of 805 players moved -- nothing changed in v/vM1/vM2/vP1/vP2; 2 dropped (fut, gf).

0 players moved on any SCAR field; the only schema change is the two dropped columns `gf`, `fut`.
This is the known-answer test: had the ledger reported any value move here, it would be wrong.

### (b) Movement case  (prove it isn't blind)  → `movement_run.txt`

The v2.4 baked board vs the F1/F2 one-source rewire board — i.e. the actual inflation-correction commit:

    before = git show 389ac39:data/rl_build/rl_app_data.json   (v2.4 baked)
    after  = git show 14472db:data/rl_build/rl_app_data.json   (F1/F2 rewire)

Headline from that run:

    795 of 805 players moved; max Δ = $1,092 (+343.4%) on Isaac Kako;
    concentrated in GEN_FWD (206 of 795 movers); 0 columns added/dropped.

It correctly detects and groups the correction. Cross-check against the F1 narrative baked into
`rl_export.py`: the top faller is **Louis Emmett $1,361 → $855** — exactly the "Emmett shipped 1361
vs engine 855" case the F1 comment cites — and the falls cluster in **RUC** (the silently-dropped ruck
cap). The ledger sees real movement and buckets it.

---

## PART 3 — identity/parity gate confirm  (READ-ONLY; nothing modified)

**The systemic finding (F1/F2):** the shipped board was built from a *second* live engine instance,
while the values came from another; the valuation gate was keyed by `id(p)`, matched 0/805 of the
board's objects, and the ruck cap / age-taper / floor were **silently dropped** from the *persisted*
board (over-pricing ~2/3 of players). No gate re-loaded the written board and diffed it against an
independently-computed engine, so the mispriced artifact shipped.

**Closure gate — `engine/rl_after/one_source_selftest.py:83-96` (F1 EXPORT PARITY), the "F1/F2 parity"
check the v2.5 bootstrap runs green:**

- **Loads the board AS PERSISTED** — `one_source_selftest.py:88`
  `board = {r['key']: r['v'] for r in json.load(open(board_path))['active']}` — the same
  `rl_app_data.json` the viewer reads ("the view owns no math"; the viewer renders `v` verbatim).
- **Independently recomputes the engine** — a *fresh* engine instance is exec'd from scratch
  (`one_source_selftest.py:76-78`) and `ev(p, 2026)` (replicating the export's as-of sequence) is
  recomputed for every player (`:90-94`).
- **Diffs load-vs-compute, key-for-key** — `one_source_selftest.py:95`
  `mism = [(k, board[k], gated.get(k)) for k in board if board[k] != gated.get(k)]`, plus a
  set-equality check that the board's player set == the engine's (`:89`) so nothing can be silently
  added/dropped.
- **HALTS, never warns** — a mismatch is `check(False, …)` → `FAIL` → `sys.exit(1)`
  (`one_source_selftest.py:143`); the docstring states "Exits NON-ZERO (build FAILS) on any violation
  — never warns." F2 (`:98-108`) extends the same load-vs-compute diff to the book
  (`s4_matrix.json` cur == board v).

A second, in-process **belt-and-suspenders** gate runs at build time in
`engine/rl_after/rl_export.py:268-278`: it recomputes `ev()` for the in-memory board keyed by stable
key and `raise SystemExit(...)` before the file is ever written (eps=0). Both gates were exercised
here and passed (`rl_export.py`: `PARITY GATE PASS: all 805 …`; `one_source_selftest.py`:
`board==engine (F1) mismatches=0`, `book==board (F2) mismatches=0`).

**Verdict: the gate closes the systemic finding — it is real and complete.** It is *not* the narrower
thing the job warned about: it is neither a book-reproduction-only parity nor a same-instance
self-consistency check. It reads the persisted artifact from disk and diffs it against a
freshly-instantiated engine's gated `ev()`, key-for-key, and fails the build on any divergence —
precisely the load-vs-compute check whose absence let F1/F2 through.

**Boundary (not a gap in the finding's scope):** the gate proves *persisted board == Python engine*.
It assumes the JS/HTML viewer renders `v` verbatim ("the view owns no math") rather than re-deriving
it — that assumption is corroborated by the F2 book parity and the `run_panel.sh` 10/10 panel, but is
outside this specific diff. The F1/F2 systemic finding — a mispriced *persisted* board slipping
through — is fully closed.

---

## Reproduce

    bash bootstrap.sh                                    # seed workspace from THIS checkout (Wave-0a)
    ( cd /home/claude/rl_workspace/rl_after
      export PYTHONHASHSEED=0 PYTHONPATH=$PWD:/home/claude/rl_vendor RL_REPO=<repo>
      python3 rl_export.py )                             # build the Wave-0a board (gf/fut dropped)
    cp /home/claude/rl_workspace/rl_after/rl_app_data.json evidence/change_ledger/board_wave0a_built.json

    # zero-delta known-answer (0 moved):
    python3 tools/change_ledger.py data/rl_build/rl_app_data.json evidence/change_ledger/board_wave0a_built.json

    # movement sanity:
    python3 tools/change_ledger.py \
      <(git show 389ac39:data/rl_build/rl_app_data.json) \
      <(git show 14472db:data/rl_build/rl_app_data.json) --top 8

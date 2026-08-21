# EMERGENCY ROLLBACK RUNBOOK — restoring the live tree to a tagged certified state

**Status: WRITTEN, NOT EXECUTED.** Nothing in this page was run against the live tree. It is the
command sequence the P4b fire drill (2026-08-21) proved out in an isolated scratch checkout of
`baked-v2.11-2026-08-20`, transcribed for the live paths, plus the three steps the drill discovered
the naive sequence omits. Read `FIRE_DRILL.md` beside this file for the measurements behind every
claim here.

The drill's own scratch run is the rehearsal; this page is the real thing, and the real thing needs
an owner word before step 2.

---

## 0. BEFORE ANY COMMAND — the two things that are not commands

**0a. THE OWNER WORD.** A rollback moves the board. RULEBOOK law 10(b) puts tags and releases on the
owner's explicit word, and law 11 requires a numbered claims note plus ONE blind independent review
for any release that moves player values — a rollback is exactly such a release. There is no
emergency exemption written anywhere in the RULEBOOK, and this page does not invent one. If the
board is wrong and the owner is unreachable, the honest act is to **stop publishing**, not to
roll back unilaterally.

**0b. THE PREREG.** P9: an act that touches an engine file commits its predictions and falsifiers
BEFORE the edit. A rollback touches engine files. Write the prereg first — predicted post-rollback
identities are simply the target tag's `data/expected_boot.json`, quoted, and the falsifier is any
identity that lands on something else.

---

## 1. TAKE THE BUILD LOCK — P3, ONE WRITER

The shared workspace `/home/claude/rl_workspace` is the estate's single mutable build surface, and
during this drill the lock was **held by another seat** (`land-round-19205`, an R24 rehearsal
sandbox). A rollback that skips this step races whatever else is mid-flight and produces a result
that looks clean and is void.

```bash
tools/build_lock.sh status                      # who holds it, since when
source tools/build_lock.sh && build_lock_acquire rollback-<tag> 900
```

Do not delete a lock file. Ever. `flock(2)` releases it when the last holder exits.

---

## 2. CHOOSE THE TARGET AND VERIFY THE TAG'S BYTES *BEFORE* TOUCHING THE LIVE TREE

Never restore into the live tree to find out whether the tag is sound. Restore to scratch first;
the whole verification costs about two seconds (measured: 1.71 s to extract, 0.03 s to hash, 0.19 s
of guards).

```bash
TAG=baked-v2.11-2026-08-20                      # the latest owner release tag; verify with `git tag -l`
SCRATCH=$(mktemp -d)
git archive --format=tar "$TAG" | tar -x -C "$SCRATCH"

export PATH="/root/rl_venv312/bin:$PATH"
export RL_REPO="$SCRATCH" CLAUDE_PROJECT_DIR="$SCRATCH" RL_FV="$SCRATCH/engine/forward_valuation"
cd "$SCRATCH"

python3 boot_guard.py rollback_preflight \
  "$SCRATCH/engine/rl_after/rl_model_data.json" \
  "$SCRATCH/engine/rl_after/_merged_recover.py" \
  "$SCRATCH/data/cm_400.pkl" \
  "$SCRATCH/LTI_REGISTER.md"                    # Guard 5: 13 pins, halt-not-warn
python3 release_contract.py check               # the release-state verifier — SEE §2b
python3 ruling_config_check.py
```

**2b. EXPECT `release_contract.py check` TO FAIL ON `baked-v2.11-2026-08-20`, AND KNOW WHY.**
Measured in the drill: that tag's `data/release_contract.json` was last written 2026-08-10 and was
never re-stamped at the 2026-08-20 landing, so it disagrees with its own `expected_boot.json` on
`board`, `store`, `engine_head`, `rl_model`, `fv` and `config_sha256`, with no `held_candidates`
declaration to excuse any of them, and its `season_state.json` names a stale source store. The
contract's self-seal is intact — it is not tampered, it is *stale*. **A rollback to this tag
therefore ships a tree that Guard 5 accepts and the contract gate rejects.** Step 5 re-stamps it;
do not skip step 5 and do not "fix" it by hand.

---

## 3. RESTORE THE BYTES — SCOPED, EXPLICIT PATHS, NEVER THE WHOLE TREE

**THE SINGLE LOUDEST FINDING OF THE DRILL: `git checkout <tag> -- .` IS NOT A ROLLBACK, IT IS A
DELETION.** `baked-v2.11-2026-08-20` predates PACKAGE 1, PACKAGE 2a and PACKAGE 3a. It has no
`acceptance/`, no `tools/landing/`, no `docs/register/` and no `data/sheet_pins.json`. A whole-tree
checkout would un-land the safety net, the lander and the pin migration, and would delete the
register's new-form entries — an append-only record, which P8's explicit-path discipline exists to
protect.

Restore the **value-bearing carriers only**. The estate already enumerates them, and that
enumeration is the list to use rather than a fresh guess: `tools/landing/carriers.py`
(`LEVER_CARRIERS`, plus `ROUND_EXTRA_CARRIERS` when the rollback crosses a round advance). The
engine sources are NOT in the lever carrier set — a lever landing never moves them — so a rollback
must add them explicitly:

```bash
# --- the identity manifests + the board and its sidecars -------------------------------------
git checkout "$TAG" -- data/expected_boot.json
git checkout "$TAG" -- data/rl_build/rl_app_data.json data/rl_build/rl_app_data.json.srcmd5
git checkout "$TAG" -- engine/rl_after/rl_app_data.json engine/rl_after/rl_app_data.json.srcmd5

# --- the store (only if the rollback crosses a round advance) ---------------------------------
git checkout "$TAG" -- engine/rl_after/rl_model_data.json

# --- the engine sources the pins name --------------------------------------------------------
git checkout "$TAG" -- engine/rl_after/_merged_recover.py engine/rl_after/rl_model.py
git checkout "$TAG" -- engine/forward_valuation                 # the 'fv' pin covers the whole set

# --- the fitted artifacts the board's identity is MADE OF -------------------------------------
git checkout "$TAG" -- data/q97m.pkl data/v0surf.pkl data/cm_400.pkl
git checkout "$TAG" -- engine/rl_after/peak_model_v4.pkl engine/rl_after/pvc_snapshot.json \
                       engine/rl_after/bust_prior_table.json

# --- the book and its seal --------------------------------------------------------------------
git checkout "$TAG" -- engine/rl_after/s4_matrix.json engine/rl_after/s4_matrix.json.srcmd5 \
                       data/book_stable_seal.json

# --- the pinned owner input -------------------------------------------------------------------
git checkout "$TAG" -- LTI_REGISTER.md
```

**NEVER roll back, under any circumstance:** `docs/register/` and `docs/OPEN_ITEMS_REGISTER.md` (the
append-only record — the record of the failure is the reason the rollback happened),
`data/release_lineage.json` (append-only; a rollback is a NEW lineage entry, not a deleted one),
`docs/RULEBOOK.md` (owner-signed; only his word amends it), and anything under `acceptance/`,
`tools/` or `docs/proposals/`.

**`data/sheet_pins.json` is a P13 trap.** It does not exist at this tag; its pins were still inside
the engine then. Rolling `_merged_recover.py` back to the tag restores the in-engine pin block and
leaves the live `data/sheet_pins.json` orphaned, with two pin declarations in the tree and no named
writer for either. If the rollback crosses the PACKAGE 3a seam, that is a **stop-and-ask**, not a
step: P13 says a pin moved by any hand other than the writer of record is a halt.

---

## 4. RE-SEED THE SHARED WORKSPACE — THE STEP THE NAIVE SEQUENCE FORGETS

Measured in the drill: after a perfect byte-restore of the repo, `run_panel.sh` **halted**, because
`/home/claude/rl_workspace/rl_after/_merged_recover.py` still carried the LIVE engine `3af8c1f7`
while the restored tree pinned `5ac6780f`. Guard 5 caught it and refused to certify. It caught it
this time; the fitted pickles under `/home/claude/` happened to be identical between the tag and
HEAD, so the loaded-path leg passed **by luck, not by construction** — a rollback across a bake that
moved `q97m.pkl` or `v0surf.pkl` would find the engine loading the wrong pickle.

The repo restore is not the rollback. The workspace restore is half of it.

```bash
bash bootstrap.sh            # re-seeds /home/claude/rl_workspace + cm_400/q97m/v0surf pickles
                             # and hard-asserts the numpy + OpenBLAS env pin on the way through
```

The env pin was measured green during the drill on today's venv: numpy 2.4.4 and bundled OpenBLAS
`05c9f9eb…` byte-exact to `bootstrap.sh`'s pin. That is a measurement, not an assumption, and it is
the reason the tag-era build reproduced at all.

---

## 5. RE-PIN AND RE-STAMP — the identities that do not travel in the bytes

```bash
# 5a. the release contract: re-stamp identities + config_sha256 + contract_sha256 to the restored
#     tree, in the SAME commit as the restore. §2b is why this is mandatory, not optional.
python3 - <<'PY'
import release_contract as rc      # restamp_dynamic(root, as_of_round, store_md5, board_md5, season_state)
PY
python3 release_contract.py check        # must now PASS

# 5b. the season clock, if the rollback crosses an advance
#     data/season_state.json carries source_store_md5 — it reds against a rolled-back store.

# 5c. the generated state file (P6: generated-only; a hand edit is a red)
python3 -m tools.landing.state write

# 5d. the UI bundles and the ownership mirror are PINNED to board+store. If they are not regenerated
#     the live ownership lane silently DISABLES rather than showing a stale club (measured 2026-08-21).
#     They are carriers; regenerate them through their writers of record, never by hand.
```

---

## 6. GATES — the tree must self-certify before anything is published

```bash
export RL_REPO="$PWD" CLAUDE_PROJECT_DIR="$PWD" RL_FV="$PWD/engine/forward_valuation"

python3 boot_guard.py rollback "$PWD/engine/rl_after/rl_model_data.json" \
        "$PWD/engine/rl_after/_merged_recover.py" "$PWD/data/cm_400.pkl" "$PWD/LTI_REGISTER.md"
python3 release_contract.py check
python3 ruling_config_check.py
python3 -m acceptance.runner                      # the current suite — did not exist at the tag
cd engine/rl_after && RL_CONFIG_MODE=bake python3 one_source_selftest.py   # see FIRE_DRILL.md §6
python3 tools/rulebook_lint.py
```

**Rebuild-from-source is the strongest available proof and it is cheap** — 85 seconds, measured, in
either the fenced (`RL_CONFIG_MODE=bake`) or bare posture:

```bash
cd engine/rl_after && RL_CONFIG_MODE=bake python3 rl_export.py
md5sum rl_app_data.json                           # must equal the tag's board pin
```

Do this in a **copy**, not in the live tree, and compare hashes. A build that writes the live board
before its output has been hashed is a build that has already replaced the thing it was meant to
prove.

---

## 7. COMMIT — explicit paths, one transaction (P8)

```bash
git add data/expected_boot.json data/release_contract.json data/rl_build/rl_app_data.json ...
#   ^ every path NAMED. No `git add -A`, no sweep, no bare `git commit`.
git commit -m "ROLLBACK to <tag>: board <old> -> <tag board>. Owner word <date>, verbatim: \"...\""
```

Then, in the same act and not later:

- **append** to `data/release_lineage.json` (a rollback is a transition, and the register is
  append-only in both directions);
- **write** the register entry under `docs/register/entries/`;
- **file** the numbered claims note (`tools/claims.py`) that law 11 requires.

---

## 8. WHAT THIS RUNBOOK DOES NOT COVER, HONESTLY

- **It has never been executed.** Its scratch rehearsal passed; the live sequence has not been run
  and its timings above are the scratch timings.
- **Step 5a's re-stamp is written as a shape, not as a tested one-liner.** `restamp_dynamic` takes a
  season-state argument; the correct call for a rollback (as against an advance) has not been
  exercised. The first real rollback should expect to spend its time here, and should not improvise
  it under pressure — that is precisely the "improvised manual landing" PLAN_v6 2a.3 rules out.
- **The abort path for a failed rollback is the lander's, not this page's.** If a rollback cannot be
  completed, `tools/landing/carriers.py`'s snapshot/restore is the mechanism that puts the tree back,
  and a rollback that cannot complete after abort+retry is an owner call, not a seat's.

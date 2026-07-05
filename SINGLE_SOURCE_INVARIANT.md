# SINGLE_SOURCE_INVARIANT — the one rule that outranks the rest
_DPP-strip final consolidation, 2026-07-05. Enforced by permanent tests that **FAIL the build** (never warn)._

## The invariant
There is **exactly one writable source of truth**: the store
`engine/rl_after/rl_model_data.json`. Every other data-bearing file is **DERIVED** — written only by
its generator, stamped with the source md5, and set **read-only**. No player fact may live anywhere
but the store. No published number may be hand-edited into existence.

This is the rule the "Kako class" broke: Isaac Kako's real 2025 season lived **only** as a hard-coded
patch inside the book generator (`s4_matrix_M1v7.py`), never in the store — so the board and the book
disagreed and the store was silently wrong. That class is now **structurally impossible**; see Guard 4.

## Files
| file | class | writer | rule |
|---|---|---|---|
| `rl_model_data.json` | **SOURCE (writable)** | humans / a store-fold step | the ONLY place a player fact may live |
| `rl_app_data.json` (board) | DERIVED · tier-1 | `rl_export.py` | regenerated every build, stamped `+ read-only` |
| `s4_matrix.json` (book) | DERIVED · tier-1 | `s4_matrix_M1v7.py` | regenerated every build, stamped `+ read-only` |
| `peak_model_v4.pkl` | DERIVED · tier-2 (frozen cache) | `build_peak_model_v4.py` | train-time; read-only; own-provenance stamp |
| `pvc_snapshot.json` | DERIVED · tier-2 (frozen cache) | `build_peak_model_v4.py` (co-emit) | peak-model's **train-time** PVC feature; read-only |
| `params.json`, `rl_passmark.json`, `bust_prior_table.json` | AUTHORED INPUT | humans | hand-editable model constants (not derived) |

Tier-2 caches are deliberately **frozen** to break the SCALE↔PVC↔peak_est bootstrap cycle. They are the
peak model and the exact PVC it was trained on; they are co-generated so they can never drift apart, and
they are **not** re-asserted against the current store each build (rebuilding them is a modelling action).
They may not be hand-edited (read-only + lookalike tripwire).

## The five guards (`single_source.py` + `boot_guard.py`; each FAILS the build)
1. **One writable source; derived read-only + source-md5-stamped.** The generator is the only writer:
   after it writes a derived file it stamps `<file>.srcmd5` with the source md5 and `chmod`s the file to
   `0o444`. Hand-editing a board/book is therefore impossible without tripping the stamp.
2. **Source-hash assertion.** Before a step consumes a derived artifact it asserts the artifact's stamp
   `== current source md5` and **HALTs** on mismatch (a stale or hand-edited board/book, or one built from
   an older store). `rl_export` produces the board; `s4_matrix` asserts the board then produces the book;
   the self-test asserts both.
3. **Lookalike tripwire.** The self-test **FAILS** if more than one file matches `rl_model_data*.json` in
   the source dir, or if any `.pre_stage0` / `.stage0` / `.bak` lookalike exists, or if `rl_model.py` opens
   any file outside the classified set. (This is the `.pre_stage0`/`.stage0` class, now dead.)
4. **Correction-sticks canary** (`guard_correction_canary.py`). Writes a throwaway edit to the source, runs
   a **full rebuild**, and asserts the edit survives all the way to **board + book**. If any generator
   re-injects / overrides / ignores the store (the Kako mechanism), the sentinel does not move and the
   build **FAILS**. Source + derived artifacts are restored byte-for-byte afterwards.
5. **Boot-store assertion** (`boot_guard.py`; stale-boot hardening 2026-07-05). Guards 1–4 protect the data
   *model* but validate whichever **directory** they are imported from — so a stale-but-self-consistent
   workspace copy (`/home/claude/rl_workspace/rl_after`) passes them silently. Guard 5 closes that hole: on
   ENTRY, every gate / panel / bake / self-test asserts that the store it is about to read equals **both**
   the pinned expected (`data/expected_boot.json`) **and** the checked-out repo store, and **HALTS** (non-zero,
   never warns) with a loud message otherwise. This is the manual three-assertion check (engine head / store /
   band) we ran by hand all session, made automatic and permanent. `data/expected_boot.json` is the ONE place
   the expected md5s live — `verify_restore.sh`, `bootstrap.sh`, `run_panel.sh`, `ship_gates_check.py`, and
   `one_source_selftest.py` all read it instead of carrying their own per-bake hex.

## Why the workspace stays (re-seeded + hash-asserted, not deleted)
`/home/claude/rl_workspace/rl_after` is **persistent staging**, not a lookalike: the engine's hardcoded
absolute imports (`par_redesign.py` → `/home/claude/rl_after`, `wire_redesign.py` `_FV`, etc.) resolve there,
and the single-source build **writes** the board/book/`.srcmd5` stamps into it — isolating those writes from
the git checkout is deliberate. So it is genuinely needed. The stale-boot fix is therefore the one the
invariant prescribes for a needed staging dir: `bootstrap.sh` **re-seeds** it from the checked-out source
(`cp -rf engine/rl_after → workspace`) and hard-asserts the seed == the pin (Guard 5), and every consumer
re-asserts workspace == checkout == pin before it reads. A build that boots on the wrong store now HALTs on
line one — it does not run five confused turns later. Obituary for the old failure: all session, builds booted
on the baked-v2.4 store `644d1254` sitting in the workspace while the real candidate `e1b4d8bf` lived in the
checked-out `engine/rl_after/` — hours of ghost premises the four data guards could not catch. Guard 5 is that
gap, closed.

## Rules for every future seat
- **Never** patch a player fact anywhere but `rl_model_data.json`. If the board or book needs different
  data, fold it into the store (a store-fold step) — never a generator-local patch.
- **Never** hand-edit a derived file (`rl_app_data.json`, `s4_matrix.json`, `pvc_snapshot.json`,
  `peak_model_v4.pkl`). Regenerate it via its generator; the read-only bit and the stamp will stop you.
- Build order is fixed: `rl_export.py` → `s4_matrix_M1v7.py` → `one_source_selftest.py` →
  `guard_correction_canary.py`. Any guard failure means **stop and fix the source**, not the derived file.

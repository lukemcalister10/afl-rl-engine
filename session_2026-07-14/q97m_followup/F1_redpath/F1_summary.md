# F1 — ASSERT THE FILE THE ENGINE WILL ACTUALLY LOAD (register item 91)

## The hole (owner-caught, seat-6-widened)
- `boot_guard.py` block (0d) hashes the **repo** file `data/q97m.pkl`.
- `_load_q97m()` (`_merged_recover.py:41`) resolves **`$RL_Q97M_PKL` → `/home/claude/q97m.pkl` → `<repo>/data/q97m.pkl`** — the workspace copy WINS over the repo, the env var beats both.
- `bootstrap.sh` copied the pickle to the workspace and only **echoed** its md5 ("expect cfdc7321") — never asserted it (the store and cm_400 WERE asserted; q97m was left out).
- Net: an env var could point the engine at ANY pickle on disk and Guard 5 still passed. **A guard that cannot fail** — the exact stale-boot hole Guard 5 was built to close, re-opened on the just-frozen artifact.
- `cm_400.pkl` has the same shape: the engine loads `/home/claude/cm_<trees>.pkl`; `run_panel` passes the **repo** `data/cm_400.pkl` to the guard.

## The fix (IN-fence: `boot_guard.py` + `bootstrap.sh` F1 assertion only; engine UNTOUCHED)
1. **`boot_guard.py` block (0e)** — new. Resolves each fitted artifact through the engine's **exact**
   precedence and asserts THE PATH THAT WILL ACTUALLY BE LOADED == the pin:
   - q97m: `$RL_Q97M_PKL → /home/claude/q97m.pkl → <repo>/data/q97m.pkl` (mirrors `_load_q97m` byte-for-byte).
   - cm/band: `/home/claude/cm_<RL_PRIOR_TREES>.pkl` (mirrors `wire_redesign.build`).
   Mismatch ⇒ HALT **naming the resolved path AND the expected pin**. Unresolved ⇒ HALT (engine would fit/retrain).
   Block (0d) is KEPT (repo-source integrity); (0e) is additive — nothing is weakened.
2. **`bootstrap.sh`** — the workspace q97m the engine loads (`/home/claude/q97m.pkl`) is now **asserted**
   against the pin (fail-closed `exit 1`), not merely echoed — matching the store/cm/register assertions.

## RED-PATH PROOFS (all three required + the two A3 proofs) — `redpath_results.txt`
| test | knob | result |
|---|---|---|
| A3.1 (0d) | corrupt repo `data/q97m.pkl` | HALT `checkout q97m ef76c18f != pinned cfdc7321`, rc=1 → restore → **PASS** |
| A3.2 (0d) | corrupt `bust_prior_table.json` | HALT `checkout bust_prior 71fd668a != pinned ffb54267`, rc=1 → restore → **PASS** |
| **F1.1 (0e)** | **`RL_Q97M_PKL` → corrupt pickle** | **HALT `q97m LOAD-PATH MISMATCH: the engine will LOAD /tmp/q97m_corrupt.pkl md5 ef76c18f != pinned cfdc7321`, rc=1 → unset → PASS** |
| **F1.2 (0e)** | **stale `/home/claude/q97m.pkl`** | **HALT `q97m LOAD-PATH MISMATCH: the engine will LOAD /home/claude/q97m.pkl md5 776e6e8d != pinned cfdc7321`, rc=1 → restore → PASS** |
| baseline | clean | PASS rc=0 (both before and after every test) |

**The env var that used to point the engine at any pickle now HALTs. The guard can fail.** All repo files
restored (git status: only `boot_guard.py` + `bootstrap.sh` modified). Board unchanged (F1 touches guard/seed
logic only, never `ev()`).

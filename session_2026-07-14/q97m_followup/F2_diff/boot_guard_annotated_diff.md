# F2 — ANNOTATED LINE-BY-LINE READING of the cumulative `boot_guard.py` diff (`ed13177..HEAD`)

**Disclosure only. The supervisor reads this independently; the owner rules. No self-certification.**

`ed13177` = the BASE this freeze branch sits on (PR #74, config-manifest completion).
`HEAD`    = `f14710d` (the freeze commit; the branch head has not moved since).

## Scope of the whole diff
```
 boot_guard.py | 24 ++++++++++++++++++++++++
 1 file changed, 24 insertions(+)
```
**ONE hunk, +24 lines, ZERO deletions, ZERO modifications to existing lines.** Everything that
`boot_guard.py` HALTed on at `ed13177` it still HALTs on at HEAD, byte-for-byte. The freeze only
ADDED a check. Nothing was weakened, relaxed, re-scoped, or removed.

## The single hunk — inserted between block (0c) [board] and the `_chk()` inner function
```python
+    # (0d) FITTED-ARTIFACT checkout-integrity (q97m FREEZE 2026-07-14, owner ruling): assert every FITTED artifact
+    #      that determines the board equals its pin, exactly as (0)/(0c) do for the store/board. These run
+    #      automatically on EVERY assert_boot entry (no caller need pass a path), so a wrong or missing frozen
+    #      artifact HALTS on line one for panel, gate, build and self-test alike. Backward-compatible: each field
+    #      is skipped when absent from the manifest. Full-hash compare (the pins are full 32-char md5s).
+    _FITTED = (('q97m',         os.path.join('data', 'q97m.pkl')),
+               ('peak_model',   os.path.join('engine', 'rl_after', 'peak_model_v4.pkl')),
+               ('pvc_snapshot', os.path.join('engine', 'rl_after', 'pvc_snapshot.json')),
+               ('bust_prior',   os.path.join('engine', 'rl_after', 'bust_prior_table.json')))
+    for _field, _rel in _FITTED:
+        _pin = exp.get(_field)
+        if _pin is None:
+            continue
+        _fp = os.path.join(root, _rel)
+        _fm = _md5(_fp) if os.path.exists(_fp) else None
+        if _fm is None:
+            fails.append("%s pin present (%s) but %s is ABSENT — cannot assert the frozen artifact (re-freeze + "
+                         "re-pin; for q97m run refit_q97m.py at a bake)" % (_field, _fmt(_pin), _rel))
+        elif not _cmp_on_pin_len(_fm, _pin):
+            fails.append("checkout %s %s != pinned %s (data/expected_boot.json '%s', full-hash compare) — the "
+                         "FROZEN artifact %s and its pin are out of sync (re-freeze + re-pin, or the pin drifted; "
+                         "the board's identity is made of this — never boot on an unverified fitted artifact)"
+                         % (_field, _fmt(_fm), _fmt(_pin), _field, _rel))
```

### Line-by-line

| lines | what it does |
|---|---|
| comment block | Declares intent: assert every FITTED board input == its pin, like (0)/(0c) do for store/board. States it runs on every `assert_boot` entry with no caller path needed, and is backward-compatible (a field absent from the manifest is skipped). |
| `_FITTED = (…)` | A 4-tuple of `(manifest_field, repo_relative_path)`: `q97m`→`data/q97m.pkl`, `peak_model`→`engine/rl_after/peak_model_v4.pkl`, `pvc_snapshot`→`engine/rl_after/pvc_snapshot.json`, `bust_prior`→`engine/rl_after/bust_prior_table.json`. **All four paths are REPO paths under `root` (= `repo_root()`).** |
| `_pin = exp.get(_field)` / `if _pin is None: continue` | Reads the pin from `expected_boot.json`; skips silently if that field is not pinned (backward-compat). |
| `_fp = os.path.join(root, _rel)` | Builds the **repo-checkout** path of the artifact. |
| `_fm = _md5(_fp) if exists else None` | md5 of the **repo file**. |
| `if _fm is None: fails.append("… ABSENT …")` | HALT if the pinned artifact is missing from the checkout. |
| `elif not _cmp_on_pin_len(_fm, _pin): fails.append("… out of sync …")` | HALT if the **repo file's** md5 ≠ pin (full-hash compare). |

## What it now HALTs on that it did NOT before
Booting (panel / gate / build / bootstrap / self-test — every `assert_boot` caller) now HALTs when, **in the repo checkout**, any of:
1. `data/q97m.pkl` is absent, or its md5 ≠ `expected_boot.json 'q97m'` (`cfdc7321…`).
2. `engine/rl_after/peak_model_v4.pkl` is absent, or ≠ `'peak_model'` (`b763f59e…`).
3. `engine/rl_after/pvc_snapshot.json` is absent, or ≠ `'pvc_snapshot'` (`735d2dec…`).
4. `engine/rl_after/bust_prior_table.json` is absent, or ≠ `'bust_prior'` (`ffb54267…`).

(Two of the three extra pins — `peak_model`, `pvc_snapshot`, `bust_prior` — close D6, the three previously-unstamped board inputs; these were explicitly directed. Credit noted; not self-certified.)

## What it no longer HALTs on
**Nothing.** No line was deleted or altered. The guard's prior halts are all intact.

## ⚠ THE GAP THIS HUNK DOES NOT CLOSE (the reason Part 2 / F1 exists — register item 91)
Block (0d) asserts the **REPO** path `os.path.join(root, 'data', 'q97m.pkl')`. But the engine's
`_load_q97m()` (`_merged_recover.py:41`) resolves in a DIFFERENT precedence:
`$RL_Q97M_PKL` → `/home/claude/q97m.pkl` (workspace) → `<repo>/data/q97m.pkl` (last resort).
So the file (0d) asserts is the **last** one the engine would ever load. An `$RL_Q97M_PKL` pointing
anywhere, or a stale `/home/claude/q97m.pkl`, is loaded by the engine while (0d) validates the
untouched repo copy and PASSES. `cm_400.pkl` has the same shape via `_chk('BAND …', band_path=…)`
which the callers point at the **repo** `data/cm_400.pkl` while the engine loads `/home/claude/cm_400.pkl`.
**F1 closes this by asserting the path the engine's own precedence RESOLVES TO.**

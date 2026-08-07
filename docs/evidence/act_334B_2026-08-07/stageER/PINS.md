# Stage ER — PINS, old -> new

`data/expected_boot.json`. Baseline is `ad50dad` (stage 1) — stage 2 (`4d435ea`) was a
teaching-stage commit that moved no pin, so `4d435ea` and `ad50dad` carry identical pins.

| pin | old | new | moved? | why |
|---|---|---|---|---|
| `engine_head` | `e3527be4195732b2e271e9e10ed40ce4` | `a0a20d6e1a9b0d1a7dbb0aa64908aa13` | **MOVED** | `md5(engine/rl_after/_merged_recover.py)`. The era table + `REF` + the five multiplier sites were removed from this file. |
| `board` | `de5110bb57a04d9b24e9c761241e54c7` | `f94e0778f8ab49e81bba8658f1c14a4d` | **MOVED** | The rebuilt board. 28 movers, all KPF, all cuts. |
| `rl_model` | `b35c5521b78dcdfb2423d54f5574330b` | `b35c5521b78dcdfb2423d54f5574330b` | unmoved | `rl_model.py` was NOT touched. It has no era table and no `era.get`; its `AGE_REF`/`BASE_REF`/`SLIP_REF`/`TILT_REF`/`NBAD_REF`/`EXP_LOGREF` are name collisions and its "CONSERVATION NORMALISATION" is a whole-board conservation factor, not era scaling. Verified by recomputing the md5 after the strip. |
| `fv` | `0976195c8454...5f5f18a87` | `0976195c8454...5f5f18a87` | unmoved | `engine/forward_valuation/` has **zero** era hits — every `REF` in it is `BASE_REF`/`AGE_REF`/`WIDTH_REF`. Nothing was edited there. Verified by recomputing `fv_provenance.fv_identity()` after the strip. |
| `v0surf` | `d594dc034e86935b370c49b240a18370` | `d594dc034e86935b370c49b240a18370` | unmoved | The frozen year-zero surface is untouched this stage. It loaded from the freeze; no refit, declared or silent. |
| `store` | `37ced3ce45914e6feb00d27e26922e9a` | `37ced3ce45914e6feb00d27e26922e9a` | unmoved | Read-only stage. |
| `q97m` | `cfdc73216c099e5e8f1fda3968f31c00` | `cfdc73216c099e5e8f1fda3968f31c00` | unmoved | Loaded, never fitted. |
| `band` (cm_400) | `34faa8659cc8f19794f5cb9584fa19b2` | `34faa8659cc8f19794f5cb9584fa19b2` | unmoved | |
| `config` | `cef06fd6250b...5b4b4739` | `cef06fd6250b...5b4b4739` | unmoved | No manifest dial moved. The era table was never a dial — it was unconditional code with no kill-switch. |
| `register` | `652d83e87780e415a01a2de6d8b3cc57` | `652d83e87780e415a01a2de6d8b3cc57` | unmoved | |
| `peak_model` / `pvc_snapshot` / `bust_prior` | unchanged | unchanged | unmoved | |
| `balanced_board_md5` | `123deccb0838c7370ce614d7f4310b01` | `123deccb0838c7370ce614d7f4310b01` | unmoved | Not regenerated this stage; stage 1 likewise left it. |

## Stamping order (the stage-1 pattern, and why)

Guard 5 halts mid-flight on a stale recomputable pin, so the pins that are *derived from source*
were stamped **before** the build and the pin that is *derived from the build* **after** it:

1. Computed `md5(_merged_recover.py)` = `a0a20d6e`, `md5(rl_model.py)` = `b35c5521` (unchanged),
   `fv_identity()` = `0976195c` (unchanged). **Stamped `engine_head` only** — the other two were
   already correct, and re-stamping an unmoved pin would be noise.
2. `RL_VENDOR=... bash bootstrap.sh` -> **Guard 5 PASS**.
3. `rm -f rl_app_data.json && python3 rl_export.py` -> **PARITY GATE PASS**, board `f94e0778`.
4. `python3 s4_matrix_M1v7.py` -> **BOOK PARITY GATE PASS**.
5. `python3 one_source_selftest.py` -> **PASSED**, 146 assertions, exit 0.
6. **Stamped `board`** `de5110bb` -> `f94e0778`, copied the board into `data/rl_build/`.
7. Re-ran `bootstrap.sh` against the final pins -> **Guard 5 PASS** (clean re-entry).

## One extra file corrected, enumerated

`data/rl_build/rl_app_data.json.srcmd5` — the board's sidecar. It was left **stale at stage 1**:
it still carried `own_md5: 113b36f898a32363c49c2a62fb809f4b`, which is the *pre*-stage-1 board,
while `data/rl_build/rl_app_data.json` had already moved to `de5110bb`. Stage 1's commit touched
`rl_app_data.json` but not the sidecar. This stage copies **both** files straight from the
workspace build output, so the pair is now self-consistent:

```
{"derived": "rl_app_data.json", "own_md5": "f94e0778f8ab49e81bba8658f1c14a4d",
 "source": "rl_model_data.json", "source_md5": "37ced3ce45914e6feb00d27e26922e9a", "tier": 1}
```

This is a repair of a pre-existing inconsistency, not a change this stage's work required. Flagged
here so it is not mistaken for a silent edit.

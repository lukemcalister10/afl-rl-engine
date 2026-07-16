# PLAN — LEG A: the `iso_corr` EVIDENCE-FADE + ISO MONOTONIZATION

Build session artifact (NOT a docs/ pack doc — CORE: builds never author docs).
Directive: `docs/DIRECTIVE_LEGA_isofade_2026-07-16.md`. Spec: `docs/SPEC_PVC_FLEX_CHAPTER_v1_2026-07-16.md` §3 Leg A.
Branch `claude/iso-corr-evidence-fade-jnda76`. First committed artifact (MODE: auto).

## GUARDS ON ENTRY (all green — recorded, cited)
- BASE PIN: `git ls-remote … main` = `7a34429d` (at/after `b78dd8e77…`). `git diff --name-only b78dd8e..main` = **11 files, ALL `docs/`** ✓ (docs-only rule holds; note local `main`/`origin/main` refs point at the stale disjoint `00d82dd` "Add files via upload" history — the live main is HEAD `7a34429d`, confirmed by `ls-remote`).
- Guard 5 (bootstrap): store `b1fd0bce` == pinned · rl_model `f79fc740` == pinned · engine `fc7045d6` == expected `engine_head`. HALT-and-ask condition (different engine hash) NOT triggered.
- The current engine `fc7045d6` / board `790136a3` IS the v2.10 line (improver + captaincy candidate). `RL_ISOFADE=0` must reproduce board `790136a3` byte-exact.

## TIME
Estimate: one working session, **2–5 h of chat time** (the directive's band; confirmed, not flagged). Heavy costs: ~40 s per engine import × the A/B + measurement runs, board/book rebuild, gate suite. Actual reported in the RETURN.

## THE MECHANISM (design, verified in code before writing)

### `iso_corr` today (`_merged_recover.py:287–293`)
For each position: `raw = raw_ev(synth(pk,…))` over picks 1–70; `iso = IsotonicRegression(increasing=False).fit_transform(PICKS, raw)` (monotone non-increasing in pick); then the **multiplier** `fs = iso / max(raw,1e-6)` (line 292 — line 291 is a dead pre-assignment, overwritten; left untouched, out of the delete scope). `iso_corr(pos,pk) = interp(min(pk,70), PICKS, fs)`.
The Newcombe trough exists because the **ratio** of a monotone numerator over a **non-monotone** denominator is itself non-monotone (measured `#picks-below-a-later-max`: MID 66, GEN_FWD 63, RUC 59; e.g. GEN_FWD pk10 = 0.882 < pk34 = 1.032; pk19 vs pk34 the item-132 case).

### `w` — the v2.10 evidence weight
`w = _ev_qual(p, Y)` = **effective qualifying seasons** `E_q` (`_merged_recover.py:182`), the same continuous evidence axis the baked v2.10 RL_EVW build introduced. Zero at debut/V0 (no seasons before debut), saturating (~2 per qualifying season).

### Task 1 — THE FADE (exact family member + one parameter + code home)
`iso_eff(p,Y) = 1 + (iso_corr(gfut,effpk) − 1) · fade(w)`,  `w = _ev_qual(p,Y)`.
- **Family member:** `fade(w) = exp(−w / τ)` — the **exponential-decay member of the house pedigree-fade family** `_ev_pw` (`_merged_recover.py:186–189`, `fade = _EVW_R + (1−_EVW_R)·exp(−Eq/_EVW_TAU)`) taken **with residual `_EVW_R → 0`** (iso must dissolve to *exactly* 1.0, not to a floor). One parameter: **τ = `_ISOFADE_TAU` = 1.1 = `_EVW_TAU`** (the pedigree fade rate, in effective-qualifying-season units). Code home cited above.
- `w=0` (debut/V0): `fade=1` → `iso_eff = iso_corr` — **full strength, unchanged BY CONSTRUCTION** (site :982 computes V0 at `Y=debutyr−1`, `E_q=0` → byte-identical).
- `w` saturated (proven, `E_q≥4`): `fade=exp(−4/1.1)=0.026` → `iso_eff` within 2.6 %·|iso_corr−1| of **1.0** (Timothy English, pk19 RUC, `E_q≈6`: `0.882 → ~1.000`, a **pure lift**).
- **Synths (structural scaffolds) do NOT fade.** `iso_eff` fades **real players only** (`_isreal(p)` = `p.get('key') in _REAL`; synths carry no key). Rationale: the fade dissolves a *real player's accumulated career evidence*; a synth is a frozen structural reference (the engine's own convention: "the ISO/pole tables are frozen on ORIGINAL features … synths delegate byte-exact", :303/:570). This keeps site :948 (the RUC-ceiling synth at refpk 72) byte-identical — measured `iso_corr('RUC',70)=0.898` is unchanged by monotonization, so the RUC ceiling scaffold does not move, and the fade's effect is confined to real players (the item-132 intent). Wiring `iso_eff` there still satisfies "wire at every site" (the call now routes through `iso_eff`, which returns the monotonized table for the synth).

### Task 2 — MONOTONIZE the ISO table
Apply `IsotonicRegression(increasing=False).fit_transform(PICKS, fs)` to the **multiplier** `fs` (the house instrument — line 290 already uses it for the numerator; "isotonic non-increasing in pick" is the codebase's own convention, e.g. the V0 pick-order guard). Gated on `_ISOFADE`.
- **Measured properties** (live tables): ΣΔ(multiplier) = **±0.0000 per position** — *genuinely conserving* (item 130/131); result **non-increasing** everywhere (pk19 ≥ pk34 now holds); **two-directional** — lifts troughs, trims local peaks; the Newcombe trough is killed.
- Not the cumulative-max majorant (rejected): it would lift every pick to the highest later peak (e.g. all MID → 1.074), ballooning young value and **growing the unearned-value census** — the opposite of conserving.
- **Over-performer protection is structural:** being "above projection" requires *evidence* (games/production), and evidence dissolves iso via the fade — so a young over-performer's monotonization delta is scaled by a small `fade(E_q)`. A never-played young player (fade=1, full delta) is by definition NOT above projection. Verified in the item-130 scan (Task 7).

### Task 3 — KILL-SWITCH `RL_ISOFADE` (default ON)
`_ISOFADE = os.environ.get('RL_ISOFADE','1')!='0'` — a **declared kill-switch, not a manifest dial** (the `RL_EVW`/`RL_CAPT` pattern; `config_sha256` UNMOVED). Gates BOTH the table monotonization AND the per-site fade. `RL_ISOFADE=0` ⇒ original table + plain `iso_corr` at every site ⇒ board `790136a3` **byte-exact**. Proven by a gated A/B board build (Task 3 / Task 7).

### Task 4 — HYGIENE RIDERS (one-shot, in-fence)
(a) **`SGC_*` env leakage** (`ship_gates_check.py`, rev143 items 149/151/169): `SGC_REPORT_DIR` auto-write tripped three builds by writing reports out of fence. Fix: at ship-gates startup, **reject unrecognised `SGC_*` env** (allow-list the three recognised ones: `SGC_SKIP`, `SGC_B1_MATRIX`, `SGC_REPORT_DIR`) and default the report dir write **in-fence**. Not a threshold change (FENCE-safe).
(b) **DELETE the dead `if not _EVW:` branch** (`_merged_recover.py:358–372`) in `_est` — the pre-EVW discrete-regime path, superseded by the continuous evidence weight, reachable only with `RL_EVW=0` on a code path the live `_inferM1` no longer routes through here. **Delete, don't disable, with an OBITUARY** (SSI / CORE rule 7). Verify dead before cutting.

## THE SITES (all 6, mapped; directive lines + 93 = current)
| directive | current | function | fade arg | note |
|---|---|---|---|---|
| :747 | :840 | `_kpf_prod_efv(p,Y)` | `iso_eff(p,Y)` | real player |
| :855 | :948 | `_build_ruc_ceiling` synth | `iso_eff(sp,Y)` | synth → unfaded (byte-identical) |
| :889 | :982 | `_v0_uncapped(p)` | `iso_eff(p, debutyr−1)` | V0, `E_q=0` → full strength |
| :1032 | :1125 | `_prod_path(p,Y)` | `iso_eff(p,Y)` | **the board path (feeds `ev()`)** |
| :1041 | :1134 | `_prod_path` games-perturbed | `iso_eff(p,Y)` | first-evidence smoothing |
| — | `_ov_angleA.py:39` | diagnostic | `iso_eff(p,Y)` | import `iso_eff` from the exec'd globals |

### Task 5 — SELF-TESTS (SILENCE IS A RED; exit codes propagate)
Add to `one_source_selftest.py` (or a committed self-test in-fence): (i) a **zero-evidence** real player (`E_q≈0`) has `iso_eff == iso_corr` exactly; (ii) a **saturated-evidence** proven player (`E_q≥5`) has `|iso_eff − 1.0| < 0.02`; (iii) the monotonized `ISO[pos]` multiplier is **non-increasing** in pick for every position. Each prints a verdict or HALTs non-zero.

### Task 6 — DERIVED-ARTIFACT REGENERATION (stamped per S1)
`bootstrap.sh` (re-seed workspace) → `rl_export.py` (rebuild board `data/rl_build/rl_app_data.json`) → re-pin `data/expected_boot.json` **`engine_head` + `board` + `panel`** in the engine-moving commit (candidate precedent: the RL_EVW / improver notes) → `s4_matrix_M1v7.py` (rebuild book/matrix) + re-seal (G-BOOK; the formula moved) → update `run_panel.sh` / `PANEL_EXPECTED.txt` pins if any of the 10 named move → `ship_gates_check.py` to GREEN. `RL_PVCFIT` stays OFF (R3) so the frozen pick curve (`MA.PVC`) does NOT move — Leg D untouched.

## Task 7 — MEASURE (frozen suite only; ad-hoc = FINDINGS, never verdicts)
Switch ON vs board `790136a3`: full movers list (expect pure lifts concentrated in proven mid-round picks — **English + the trough rucks the faces**); **WHERE-DOES-THE-VALUE-GO** (ΣΔ · age/cohort distribution · over-performer scan = item-130 HALT check: any young net-strip OR any above-projection young player cut ⇒ **HALT**); census-v2 unearned gauge (must not grow past **+15,612**); L-SMOOTH discontinuity census on the new multipliers; G-COHORT y1–y5 (**hard 1.30**); A-PAIRS scored; English/Briggs priced ratio printed (R104.3 floor 1.75 is a *chapter* acceptance — Leg A need not reach it; print where it lands). Plus the A/B byte-identity (`RL_ISOFADE=0` == `790136a3`).

## FENCE (self-check)
IN: `_merged_recover.py` (iso construction + wiring + both riders) · `_ov_angleA.py:39` · gates/self-test additions · derived-artifact regeneration (board/matrices/pins, stamped) · session artifacts. OUT (touch = HALT): output→price map (Leg B) · the store (no store writes) · PVC/pick code (Leg D; `RL_PVCFIT` stays off) · lens/UI · docs/ authoring · gate thresholds.

## RETURN
≤30 lines: branch · head SHA · PR number · the measured set · kill-switch A/B byte-identity · "in plain terms" close.

# PLAN — R100.11 REWORK: the absence penalty fades on EVIDENCE, not on a clock

Candidate. NO bake, NO tag, NO main merge. Owner rules the affected-row list.

## Base (verified live, strict equality)
- BASE engine head = `a2a06c773d4ca16b1f216c2689ca96f609e66500` (head of PR #83, the determinism fix).
- Branched from base; the workspace was re-seeded from this checkout.
- BASE board reproduced byte-for-byte: `md5(rl_app_data.json) = 800bf461d5ec81d12da2e2426ff15c9c` == pinned. Panel **PASS 10/10**.
- expected_boot pins at base: engine_head `118f8ac6`, board `800bf461`, store `340a7a32`, config `c2d233ae…`, band/register/q97m/rl_model unchanged.

## The ruling (R100.11, DECISIONS v101 §1)
The absence term is a PRIOR about an UNOBSERVED return. Evidence dissolves it in BOTH directions: good
football proves the prior wrong (drop it); bad football is ALREADY IN HIS LEVEL (charging again = a
double-charge). The fade runs on EVIDENCE WEIGHT = **games played since return**, NEVER seasons elapsed.
NO SCHEDULE FALLBACK (recurrence risk is the availability layer's job — `_avail_hc` / LTI; D2 R5).

## What changes (and nothing else)

### 1. The fade — schedule → continuous evidence weight
Current (`_merged_recover.py:399`):
```
fade = clip(1 - npost/_ABS_FADE_N)      # npost = count of post-return seasons with games>=10
```
Two violations: (a) it runs on SEASONS ELAPSED, not evidence; (b) the `games>=10` season counter is a
threshold/branch (violates L-SMOOTH; acceptance_v1_13.json).

Replace with ONE continuous object in games-since-return `g`, using the measured evidence-reliability
curve `w(g) = g²/(g+K)` (Fix 1's curve, `_merged_recover.py:152`) as the EVIDENCE precision and the
absence prior as one pseudo-observation:

```
fade = pw(g) = 1 / (1 + w(g)) = (g + K) / (g² + g + K)
```

- **Declared K = 5.8** — the data-derived scale from Fix 1 (`w: 0→0, 1→0.147, 2→0.513 … 22→17.41`,
  `_merged_recover.py:152-154`). Same measured scale; declared, not re-fit.
- `pw(0) = K/K = 1` — a fresh return (no games yet) carries the FULL prior.
- `pw(g) → 0` as evidence accumulates — the prior dissolves. Smooth, monotone, rational; denominator
  `g²+g+K > 0` for all `g ≥ 0`. NO threshold, NO counter, NO branch (L-SMOOTH satisfied).

### 2. The shed emerges from the construction, not an `if`
The construction is unchanged: `L_abs = min(Lb, Lng·(1-frac))`, `frac = _abs_frac(age_pre)·pw(g)`.
As `g` grows, `frac → 0`, so `Lng·(1-frac) → Lng`; a returner who has played and produced ends at
`min(Lb, Lng) = Lb` — uncharged — because the arithmetic delivers it. No `if level ≥ pre-absence` branch
is added. Bad football is already in `Lb` (min never lifts); good football lifts `Lb` above the faded
prior. Both directions handled by the same `min` + fade, exactly as the ruling requires.

### 3. Evidence weight `g` = games played since the most-recent return
Add `gpost` to `_abs_gap`: `sum(games) for scoring rows with year >= ret` (the return season is the first
evidence). Charged ONCE on the most-recent return (`_abs_gap` already keeps the latest qualifying gap).
The old `npost` (season counter) is retired from the engine path; retained in the dict for the report only.

### 4. Pin the dials (register item 114 — NO `os.environ.get` on a board-changing value)
None of these are in the config manifest (`data/model_config.json`) — so this is a pure in-code pin,
`config_sha256` does NOT move (no config route).
- `RL_DAMP_K` (`:161`) → in-code constant `5.8`.
- `RL_ABS_LREF` (`:353`) → in-code constant `75.0`.
- `RL_ABS_CAP` (`:354`) → in-code constant `0.20` (board-changing; pinned for the grep-clean proof).
- `RL_ABS_FADE_N` (`:355`) → **RETIRED** (the schedule fade is gone).
- NEW constant `_ABS_FADE_K = 5.8` — in-code, pinned, declared = Fix 1's `w(g)` scale.
- KEPT as env kill-switches for the G-ATTR ablation (declared exception, not a dial): `RL_DAMP`,
  `RL_ABSENCE` (`RL_ABSENCE=0` ⇒ byte-exact base; this is the ablation lever the measurement REQUIRES).

## KEEP AS-IS (owner-taken / owner-open — OUT of scope)
Fix 1's `w(g)` in `_lvlcurr` · the multiplicative form `min(Lb, Lng·(1-frac))` · D2's fitted U (`_ABS_EFF`)
· per-player decay netting (shortfall only, never lifting) · charged-ONCE on the most-recent return · the
`<20` clamp (`_abs_frac` positive-eff → 0). The two OPEN assumptions (gap-length magnitude; the age-20
clamp) are the OWNER'S — not resolved here.

## Fence
IN: `engine/rl_after/_merged_recover.py` (fade construction + dial pinning ONLY) · `data/expected_boot.json`
(re-pin engine_head+board) · `run_panel.sh` (re-pin ONLY if a panel value moves) · rebuilt board + book +
seal · `session_2026-07-15/r100_11_rework/`.
OUT: Fix 1's `w(g)` in `_lvlcurr` · the U-curve values · the STORE · the PRICING CURVE / PVC · `TOL_M1` ·
`_radq` · `S_AGE` · `DOWN_TOL` · `_eo` · `PROVEN_N` · pedigree blend · `boot_guard.py` · `bootstrap.sh` ·
CI workflow logic · `docs/`.

## Measurement (G-ATTR, binding)
- Ablate: (a) base board `800bf461` · (b) rework applied. Per-player delta, path-additive.
- The COMPLETE affected-row list in RAW board moves (not netted accounting — the −515-vs−899 lesson,
  item 114), sorted |Δ|. This is the list the owner rules from.
- BAILEY SMITH in full (base: gap 2024, ret 2025, ~37 games since return @116/122; at schedule fade 0.5 he
  is docked −899 RAW vs no-absence). State his exact rework number — expect ~entire shed (`pw(37)≈0.030`).
- JACK BULLER: one line on why absence-alone lifted him +4 (item 114).
- DARCY WILMOT −693: he has NO gap → **unmoved by the rework**; −693 is his pre-existing Fix-1 effect —
  name the Fix-1 season/weight change (owner views this row).
- Gates on the FROZEN suite: G-COHORT y4/y5/y6 vs hard 1.30 (breach ⇒ STOP, mechanism to owner, no tuning)
  · every guard + anchor · three narrowest margins (OQ-B) · PICK 1 = 3000 · re-pin `run_panel.sh` if any
  panel value moves · book REBUILT + re-sealed · expected_boot re-pins recorded old→new.

## Anticipated band
High effort. Single specified lever on a measured, hardware-stable base. Expected: the ~19 gap players the
absence term touches move toward their no-absence value as evidence has accumulated; re-established returners
(Smith) shed ~entirely; fresh returns (few games) barely move. G-COHORT may rise (weakened charges on
returners lift year-4/5 numerators) — watched against 1.30. Flag if any single move is >2× or <½× expectation.

# RETURN — R100.11 REWORK: the absence penalty fades on EVIDENCE, not on a clock

**Candidate. NO bake, NO tag, NO main merge.** The owner rules the affected-row list.

## Heads / identity
- branch: `claude/absence-penalty-evidence-fade-glcl8b` (branched from base a2a06c7, PR #83 head).
- engine head md5: `113a4223` (base 118f8ac6). Board md5: **`24159c49`** (base `800bf461`). Store `340a7a32`,
  config `c2d233ae`, register `652d83e8` — ALL UNCHANGED. Book seal: stable_sha256 `92e401a5` (was `7fcb92c2`),
  head `113a4223`, n=2649.
- Base reproduced first: board `800bf461` byte-exact, panel 10/10 — harness proven before any edit.

## What changed (fence-clean: the fade construction + dial pinning only)
1. **Schedule fade retired.** `clip(1 − npost/_ABS_FADE_N)` and its `≥10g` "re-established" SEASON counter
   (both violated the ruling; the counter also violated L-SMOOTH) → **one continuous object in games-since-
   return** `g`: `fade = pw(g) = 1/(1+w(g)) = (g+K)/(g²+g+K)`, using Fix 1's measured evidence-reliability
   curve `w(g)=g²/(g+K)` as the evidence precision. **Declared K = 5.8** (Fix 1's data-derived scale).
   `pw(0)=1` (fresh return = full prior) → 0 on evidence. Smooth, monotone, no threshold/counter/branch.
2. **The shed EMERGES from the arithmetic, not an `if`.** The prior enters as ONE weighted term:
   `L_abs = Lb − pw(g)·max(0, Lb − Lng·(1−frac))`. At `pw=1` this equals the old `min(Lb, Lng·(1−frac))`;
   as evidence accumulates `pw(g)→0` and `L_abs→Lb` — uncharged. (The old build scaled `frac` INSIDE the
   `min`, so the `Lng<Lb` residual on a returner whose post-return seasons are his best — Bailey Smith —
   never faded. Weighting the whole prior fixes exactly that, with no "if level ≥ pre-absence" branch.)
3. **`g` = games played since the most-recent return** (`gpost`, added to `_abs_gap`; return season is the
   first evidence). Charged ONCE on the most-recent return (unchanged).
4. **Dials pinned, no env on a board-changing value:** `RL_DAMP_K`→5.8, `RL_ABS_LREF`→75.0, `RL_ABS_CAP`→0.20
   (in-code); `RL_ABS_FADE_N` **RETIRED**; new `_ABS_FADE_K`=5.8 in-code. None are in the config manifest ⇒
   `config_sha256` unmoved (no config route). `RL_DAMP`/`RL_ABSENCE` KEPT as the declared ablation
   kill-switches (not dials).

KEPT AS-IS (fence): Fix 1's `w(g)`, the multiplicative form, D2's fitted U (`_ABS_EFF`), the per-player decay
netting (shortfall only, never lifting), charged-once, the <20 clamp. The two OPEN owner assumptions untouched.

## Ablation (G-ATTR) — base 800bf461 → rework 24159c49, RAW board moves
- **28 rows move, ALL carry a gap. NON-gap movers = 0 (separability holds).** ΣΔ = **+1652 num-SCAR** (raw ev
  +1739). Single lever ⇒ one leg; path-additive trivially (max|Σlegs−total| = 0).
- Complete list (sorted |Δ|) in `measurement/AFFECTED_ROWS.md`. Direction: the evidence fade RELAXES over-charges
  on players who have banked game-evidence (net lift); a few small negatives (Zach Reid −34, Curnow −17) are
  players who looked "re-established" by season-count but carry THIN game-evidence — the ruling working as ruled.
- Top moves: **Bailey Smith +808**, Tanner Bruhn +401, Logan McDonald +169, Nikolas Cox +159, Leek Aleer +64,
  Brent Daniels +62, Todd Marshall +36, Zach Reid −34, Curnow −17. None >2× / <½× expectation.

## The three named rows
- **BAILEY SMITH — sheds ~entirely.** base **4344 → rework 5152 (Δ +808)**; level 104.84→110.97. Out 2024,
  returned 2025@116.4 (23g) & 2026@122.4 (14g) = **37 games since return**, `pw(37)=0.0303`. Residual charge
  vs his no-absence value (5243) is just **−91 SCAR** (~3% of the full prior). At base the two-season schedule
  fade (halfway, fade 0.5) still docked him −899 RAW — the exact defect the ruling names.
- **JACK BULLER — the +4 base lift, in one line:** he is a thin-record KEY_FWD priced by the prior/pedigree-
  dominated blend, which is NON-MONOTONE at his low level — the absence charge drops his current-level leg into
  the region where the higher prior leg dominates (raw_ev 27.1→28.6 as level falls 50.2→46.2) and the production
  floor nets **+4**. Under the rework his 15-game evidence (`pw(15)=0.085`) shrinks the charge to ~0, so the lift
  **vanishes: base 40 → rework 36 (Δ −4, back to his no-absence value)**.
- **DARCY WILMOT −693 — a FIX-1 row, UNMOVED by this rework** (he has no gap; base 3544 → rework 3544, Δ 0).
  Mechanism (Fix 1, already in the base): `w(g)=g²/(g+5.8)` down-weights his **in-progress 2026 season (14g,
  his career-high 95.2 avg, the most recent → highest recency weight) from raw-weight 14 to 9.90 (−29%, vs −18%
  for his fuller 26–27g years)** — the rising recent form is damped, so the trend-aware current level falls
  **88.04 → 84.32 = −693 SCAR**. An R98.3-list improver; the owner views this row.

## Gates (frozen suite 764a0d91, head 113a4223) — verdict identical to the base except the intended move
- **G-COHORT (B1) PASS×3: y4 1.2660 · y5 1.2477 · y6 1.1588 vs hard 1.30.** Base was 1.2601/1.2407/1.1521 —
  the rework lifted each ~+0.006 (returner numerators rise), still well under the 1.30 hard bar (no breach; the
  1.20–1.25 band is advisory). Numerators y1 69,851.3 (young denominator UNCUT) … y4 88,429.5.
- **B4 PASS: board md5 24159c49 reproduces (deterministic).** Panel **10/10** — no panel player carries a gap,
  so `run_panel.sh` needs NO re-pin.
- **B3 → PASS at the re-seal** (suite showed DIFFERS-BY-DESIGN against the stale base seal; the re-seal writes
  the exact `92e401a5` the suite recomputed). B2 leakage 0.000. B5 floor-feature 60 saves. B6 ramp monotone.
- **The 3 red anchors (A2 Curtis 0.896, A3 Rozee 0.66, A12 Travaglia/Smillie) are BYTE-IDENTICAL to base** —
  all pre-existing ruled-red, none are gap players. **Zero new fails.** Verdict: PASS=16 FAIL=3 (unchanged) +
  B3 re-seal.
- **PICK 1 = 3000** (board PVC[1]=3000; manifest RL_PICK1=3000).
- **Three narrowest margins (OQ-B):** (1) G-COHORT **y4 1.2660 vs hard 1.30 = 0.034** — the tightest hard-gated
  margin and the one the lever moved (+0.0059); (2) G-COHORT **y5 1.2477 vs 1.30 = 0.052** (+0.0070); (3)
  **A10 Curnow 2026/2025 = 0.57 vs 0.50** ruled floor (a gap player, moved −17 on the board, ratio holds). All
  non-cohort gates byte-unchanged from base.

## Dials-pinned proof
`grep` of `_merged_recover.py` shows **no `os.environ.get` on RL_DAMP_K / RL_ABS_LREF / RL_ABS_CAP /
RL_ABS_FADE_N** (all in-code constants; RL_ABS_FADE_N retired). Only the two declared kill-switches
(`RL_DAMP`, `RL_ABSENCE`) still read env — by design, the ablation levers. Config manifest references none of
them ⇒ `config_sha256` unmoved.

## In plain terms
A player who missed a season used to keep getting docked on a two-year timetable, so Bailey Smith — back and
better than ever, averaging 116 then 122 — was still carrying a big "he was hurt" penalty just because the
calendar said so. Now the penalty fades on FOOTBALL, not the calendar: every game he plays after returning is
evidence that dissolves the "unknown return" guess, in both directions — play well and it drops away, play
badly and that's already in his number so we don't charge it twice. Smith has played 37 games back, so ~97% of
the old penalty is gone and he lands where his form says he should. It touches only the ~28 players with a real
mid-career gap; everyone else is byte-for-byte unchanged, the young cohort is untouched, and pick 1 is still 3000.

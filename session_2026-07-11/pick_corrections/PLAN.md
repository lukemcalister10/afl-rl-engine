# PLAN — PICK CORRECTIONS + PICK RE-DENOMINATION (build; tier-1, candidate only) · 2026-07-11
### Directive: BUILD DIRECTIVE — PICK CORRECTIONS v1a (2026-07-11). MODE auto → this is the first commit.
### Endpoint: CANDIDATE branch + PR only. NO bake, NO tag, NO main merge, NO doc/constraint edits, NO force-push.

## BASE VERIFICATION (done, first action)
- `git ls-remote https://github.com/lukemcalister10/afl-rl-engine.git` (FULL URL):
  `refs/tags/v2.7` == `8f8c00b10e2ef3a1b68dd6864594f5bdfef91340` ✓ · `refs/heads/main` == `a6a8aa9c76b864a30ed5641d6dd48dec91f984f6` ✓
- Working branch `claude/pick-corrections-redenomination-ywqmdi` at a6a8aa9c (== main). Fresh checkout.
- Boot-store guard (Guard 5) PASS on entry: store `a2fbc9a0` (2652 rows) · engine `_merged_recover.py` `7a07e369` ·
  cm_400 `34faa865` · register `652d83e8` · config `69ead79b`.
- Baseline reproduces BYTE-EXACT: `run_panel.sh` = PASS 10/10; baked gate snapshot `gates_7a07e369.json` shows the
  expected reds EXACTLY {A2, A3, A12}, B5 FEATURE (61 saves), A15 STRUCK, all else PASS. This is the control.

## WORKSHEET REUSE (not re-derived)
Evidence branch `claude/pick-integrity-audit-jf73c4 @ d4f0a84` is the worksheet: Q1 (engine handling), Q2
(contamination), Q3 (the-325 = 186 ND / 136 RD / 3 IRE, all 2003-05), Q4 (chained SIM: uniform +5.2% player-vs-pick,
RUC +3.75%; every ratio finding STANDS; 45 floor anchors dip ≤5 SCAR), Q5 (numbering source: rookie ordinals with
pass-picks dropped + PSD fold-ins; 2010-11 ND tails inflated), Q6 (ranked plan). Its `scripts/make_sim_workspace.sh`
gives the two exact engine patches. This build APPLIES the ruled corrections; it re-verifies, it does not re-derive.

## KEY FACTS ESTABLISHED (code + data, verified this seat)
- Source store to edit: `engine/rl_after/rl_model_data.json` (a2fbc9a0; bootstrap copies it verbatim to the workspace).
- Engine primary: `engine/rl_after/rl_model.py` (imported as `MA`). Band-pool line = `rl_model.py:120`
  `grp=[p for p in hist if bandof(p['pick'])==b]`. Chain offset = `rl_model.py:91`
  `_NDC=dict(_Cnt(p['year'] for p in data if p['type']=='ND'))` (ROW COUNT); consumed at `:97`
  `_eff=min(99,_NDC.get(year,75)+rookie_pick)`.
- Store `type` ↔ `_draft`: ND↔National, RD↔Rookie, IRE↔Post-Draft-Ireland, etc. The 325 `_draft=None` rows are all
  2003-2005 and already carry latent `type`: 186 ND, 136 RD, 3 IRE (cross-tab verified).
- Pick assets on the board = `PVC` dict (picks 1-30 shipped as `picks:[{n,v}]`). Baked v2.7 frozen v3.4 values:
  pick1=3000, pick2=2501, … pick30=606. `_PVC0=dict(MA.PVC)` is the frozen ruler (rl_export ships `MA.PVC`).
- Pick-1 anchor `RL_PICK1=3000` fixes PVC[1]; `BOARD_FACTOR=_P1/PVC[1]` rescales SCALE → the band-pool fix flows to
  SCALE and lifts every player ~+5.2% against the 3000-pinned pick currency (Q4 mechanism).
- Guard 5 pins the store md5 in `data/expected_boot.json`; a store edit REQUIRES re-pinning it in the same change
  (candidate-only re-pin — this is a derived artifact, not a bake/tag/merge). rl_model.py md5 is pinned in the same
  file but NOT enforced by boot_guard (informational); it will be re-stamped for hygiene.
- Gate suite `python3 ship_gates_check.py` ≈ 5 min/run (regenerates board via subprocess for B4 parity). Budget for it.

## THE TASKS (per-task commits, G-ATTR separability)

**(b) CHAIN OFFSET — authoritative last-national-pick table.** New source-stamped sidecar
`engine/rl_after/national_draft_last_pick.json` (+ repo copy under data/): per-year (2003-2025) LAST national pick
INCLUDING pass picks. Built from the store's own gapless ND sequences where they are authoritative (19/23 years) and
from web-verified official draft data for the tail years and the two known-bad years 2010 (real ND last = 77) and
2011. Source-cited in the file. Rewire `rl_model.py:91` to load this table (fallback to row-count only if a year is
absent, logged). Commit (b).

**(a) ENGINE — band-pool raw→chained.** `rl_model.py:120` `bandof(p['pick'])` → `bandof(effpk(p))`. One logical
change; before/after cited in the commit. This is the single raw-pick contamination channel (Q2). Commit (a).

**(c) STORE (source only, per SSI).**
  1. Fill `_draft` on the 325 rows from verified latent type: 186 `National` · 136 `Rookie` · 3 `Post-Draft - Ireland`
     (lists from Q3 `out/q3_none_rows.json`). $0 board movement (engine already consumes `type`).
  2. Renumber the 2010-2011 National tails to official picks and separate the expansion concession/mini-draft entrants
     per Q5 (store ND 2010 max 93 / 2011 max 89 are inflated; real 2010 ND = 77). Web-verified.
  3. Correct the 693 Rookie pick ordinals to true rookie-draft picks WHERE web-verifiable (Treacy 5→7 etc., the Q5 set
     + any additional web-verifiable rows); rows not verifiable are FLAGGED (`_pick_unverified: true`), not guessed.
  4. Split Pre-Season Draft rows out of `_draft='Rookie'` (Betts/Grimes/Johnson class; PSD ran 2003-2018) into
     `_draft='Pre-Season Draft'` + `type='PSD'`, chained AFTER national BEFORE rookie (owner ruling): PSD `_eff` =
     last-national-pick + PSD slot; rookie `_eff` = last-national-pick + (#PSD that year) + rookie slot. Only rows
     web-verified as PSD are moved; the rest stay Rookie and are flagged. Engine gets a minimal PSD chaining arm.
  5. Add the pick-semantics schema note (MSD slot never consumed = PICKEQ 60; SSP/post-draft pickless = 94; rookie =
     official slot, chained) as a store sidecar note file — NOT a doc-pack edit.
  6. DRAFT the SSI chaining-contract wording in the RETURN (supervisor's pen edits SINGLE_SOURCE_INVARIANT.md, not me).
  Commit (c). Report row-change counts per category.

**(f) PICKS RE-DENOMINATION.** MEASURE the currency factor from THIS build's regenerated board (ratio of new player
scale to baked, on a fixed anchor cohort; expected ≈1.052 — do not assume). Set the shipped pick assets to
frozen-v3.4 baked PVC × factor (byte-preserved pick-vs-pick ratios: uniform scalar). Full unfreeze is OUT of scope —
the recomputed live PVC is NOT shipped; the frozen ruler is scaled. Report old→new for every pick asset; state the
exact factor prominently. Commit (f).

**(d) REGENERATE + GATES.** Re-pin `data/expected_boot.json` (store + rl_model + board + config, same commit as the
store move). Regenerate board (rl_app_data.json), matrix, gate snapshots. Run the full suite. Expected: all green,
reds EXACTLY {A2, A3, A12}, G-FLOOR trips ONLY on the 45 dispensed rows (≤5 SCAR each). ANY other floor trip → STOP
and report. Commit (d).

**(e) OWNER'S EYEBALL LIST.** One file: every player AND every pick asset — name · key · position/asset · old value ·
new value · Δ absolute · Δ % — sorted by Δ%; the 45 floor-dippers and the RUC cohort (~+3.75% vs +5.24%, ≈−1.4%
relative) explicitly flagged. Plus a one-page summary: distribution stats (min/median/max Δ%), per-position mean Δ%,
the measured currency factor, guard margins before/after (three narrowest). Commit (e). Then push + candidate PR.

## VERIFICATION DISCIPLINE
- Control arm (baked engine+store, pinned cm cache) reproduces byte-exact BEFORE any change — established.
- Per-task: attribute each lever's delta separately (G-ATTR). (a) carries ~all the dollars; (b) moves only 2010-11
  rookies' chained picks; (c) fills/renumbers are $0-or-capped; (f) is a pure pick-side scalar.
- The pinned cm_400.pkl cache is used in both arms (a from-scratch retrain does not reproduce it in this env — Q4
  environment note); the patches provably do not change cm training inputs (every affected pick caps at KMAX=70).
- Web-verification is BOUNDED: what cannot be web-verified is flagged, never guessed (directive-sanctioned).

## EFFORT / TIME
Effort High (per directive). Band 2-4h; each gate run ≈5 min is the pacing cost. Will flag if trending >2×/<½×.
Report actual in the RETURN.

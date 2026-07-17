# LEG C RELAY — PLAN (items 270–275; the one store writer) · 2026-07-17 · seat 10
branch `claude/legc-relay-dpp-law-10c4z7` · EFFORT High · MODE auto · mini-checkpoint after the wiring commit

## THE FIRST COMMANDS (item 270 standing law) — executed, PASS
```
git fetch origin claude/legb-selection-wire-s010-ho4vl8            # -> 273463e
git checkout -B claude/legc-relay-dpp-law-10c4z7 273463e           # designated branch IS the job-branch
git merge-base --is-ancestor 273463e HEAD                          # PASS (HEAD == 273463e)
```
store md5 `b1fd0bce` == pin. Docs (spec v1.3 §1+§1b, corrected CSV) live on main (`e46790f`); FETCHED as
reference, never merged (docs/ is OUT). "Content moved to match" is never conformance — the base IS 273463e.

## BASE STATE
- 273463e reproduces board `f2f077b2` (RL_UNCOMP on, s=0.10) and `8d90c9ac` (RL_UNCOMP=0), proven by the
  Leg-B battery (session_2026-07-16/legb_selection_s010/out/s1_stamps.txt).
- 273463e carries STALE Leg-A pins in data/expected_boot.json (rl_model f79fc740 / engine_head a83c9f6d /
  board 8d90c9ac) over a Leg-B engine (rl_model.py 94b7016d / _merged_recover.py a0635745). Its own Guard 5
  is RED at base — the re-pin was deferred. Job 3 "expected_boot re-pin (same commit)" closes it. NOT a base
  fault; it is the known pending re-pin (this is exactly what items 270–275 tidy).

## THE FIVE ENGINE SITES (verified by read + empirical probe; RL_FLEX=0 ⇒ every A/B proof byte-exact)
1. **futblend years-1+ (§1 blend)** — `engine/rl_after/rl_model.py:45`. Parse `alternate_position` +
   `p_dual_stream` in the load loop; `futblend(p)` returns `[(pri,1-q),(low,q)]`, low = the LOWER-REPL of the
   {primary,alternate} pair (the MAX law, floored ≥0 by construction). Content adapts the quarantined 2b64630
   (+22 lines, verified). REACHES the board via v_at_peak(g=gfut,g0=bnow,fut=futblend); probe: injecting a
   blend moved Petracca ev +65. Kill-switch `RL_FLEX` (default ON; =0 ⇒ `[(gfut,1.0)]` ⇒ byte-exact base).
2. **§1b YEAR-0 DPP** — `engine/forward_valuation/distribution_pricing.py` v_at_peak (OWNER FENCE AMENDMENT
   item 281, LIMITED to this). The board's year-0 REPL bar is keyed to `g0=bnow` (present). §1b: the
   REMAINING-SEASON fraction (1−SEASON_PROG) of the year-0 leg nets vs the LOWER of the post-collapse dual
   eligibility bars; the banked SEASON_PROG fraction stays vs present; level path keyed to present. Because
   g0 affects ONLY the k==0 REPL term (Wk/k≥1/multipliers identical) and `val()`=SCALE·r^0.85 is NONLINEAR,
   the blend is done BEFORE val via the exact identity:
     `proj_1b = SEASON_PROG·proj(g0=present) + (1−SEASON_PROG)·proj(g0=low)`  then `val(proj_1b)`.
   Two proj_from_peak calls, RL_FLEX-gated, no Leg-B dial/constant touched. Single-position players & rows
   whose collapsed set has no lower bar ⇒ single call ⇒ unchanged.
   - Collapse R105.1: eligibilities (hyphenated set, RUCK≡RUC) → a KEY-listed position drops its matching GEN
     (K-FWD⊃G-FWD, K-DEF⊃G-DEF); ≤2 remain. low = argmin REPL over the collapsed set; applies only when
     REPL[low] < REPL[bnow] and the now-board (AGE_REF==BASE_REF). Helper computed once in rl_model.py load
     loop (`_y0dpp_bar`), consumed by v_at_peak.
   - Examples honoured: Sheezel & Petracca (MID,G-FWD) remaining nets vs GEN_FWD 70.9 not MID 80.1;
     a K-DEF also listed G-DEF is NOT a DPP (the G drops → single).
3. **RL_FLEX kill-switch** — `rl_model.py`. `_FLEX=os.environ.get('RL_FLEX','1')!='0'`. Gates BOTH the
   futblend blend AND the §1b year-0 blend (v_at_peak reads MA._FLEX). =0 ⇒ f2f077b2 byte-exact.
4. **Guard update** — `engine/rl_after/one_source_selftest.py:149-152`. REPLACE the obsolete
   `future_position==present_position for every record` seam check with flex-era invariants: (a) every
   future_position ∈ vocab; (b) ≤1 alternate per row (blend streams sum→100); (c) blend params
   register-consistent (alternate∈vocab, 0<p_dual≤100, alternate≠primary). Named for the cold audit.
5. **fut-label fix** — `engine/rl_after/rl_export.py:169`. The board `fut` stream must carry the TRUE
   primary/alternate label regardless of the bar comparison (today when REPL[alt]≥REPL[pri] the MAX-law
   low=pri drops the alternate). Add a label-blend `futstreams(p)` (true alt) used for the board `fut` field
   while VALUE keeps futblend's low bar; + a per-row assertion board labels == store primary/alternate on
   all 90. RL_FLEX=0 ⇒ `[[gfut,1.0]]` ⇒ byte-exact.

## RE-INGEST (job 1; validate-or-halt; stable-ID ONLY over the 804-scope; name-match FORBIDDEN — item 269)
Source: corrected `docs/inputs/AFFL_Future_Positioning.csv` + `AFFL_Player_Locations.csv` (fetched from main).
- future_position ← CSV primary (normalize: strip hyphens, upper, RUCK≡RUC). Expect **ELEVEN** diffs vs base
  present: Carroll·Uwland·Roberts·Lindsay·Thomas·Powell·Graham·Humphrey·Hall·Lloyd·Emmett (item-269 list).
- alternate_position + p_dual_stream ← CSV. Expect **NINETY** blend rows (Driscoll now 100% MID = dropped;
  was 91 at the quarantined content — the register correction).
- eligibilities ← Locations "Position/s" (name→ID via the positioning file's map; HALT on ambiguity — two
  Max Kings verified distinct) + present rider. Expect the **4-write rider**: Flanders/Baker/Langdon
  eligibilities 3-pos→2-pos (G-DEF,G-FWD) + Flanders present MID→GDEF.
- Any count off the 11 / 90 / 4 ⇒ HALT with the finding (item 269 discipline). Store write is JOB 3 (post-
  PROCEED); job 1 is the validated dry-run only.

## SEQUENCE
1. PLAN commit (this).  2. Re-ingest tool + dry-run validate (11/90/4).  3. **THE WIRING COMMIT** = the five
engine sites (code only; store write deferred).  4. **MINI-CHECKPOINT HALT** ≤5 lines + diff SHA + the
RL_FLEX=0⇒f2f077b2 byte-exact proof, for the supervisor's prescreen.  5. **ON PROCEED**: store writes →
board/book regen → expected_boot re-pin (same commit) → FULL BATTERY (A/B chain f2f077b2 / +RL_UNCOMP=0 ⇒
8d90c9ac · suite GREEN · frozen β · G-COHORT y-band both sides floor 1.08/cap 1.30/ideal 1.15–1.25 · E/B raw
· census · pool Δ · net ΣΔ · all-804 sincerity ledger (Bontempelli named) · A-PAIRS 2(±15%)+3 · earned-
component gate with the item-272 TWO-ROW NAMED WAIVER Carroll/Emmett scored-never-flagged, any OTHER negative
= HALT · attribution vs f2f077b2 in stages +writes/+blend/+§1b year-0 with Petracca/Sheezel/Jagga Smith named
rows + the Driscoll delta vs the quarantined reference explained) → candidate PR → RETURN.
NOTE: quarantined board b4c67bb6 will NOT reproduce (Driscoll correction + §1b both move values) — EXPECTED.

## FENCE
IN: rl_model.py · distribution_pricing.py (§1b v_at_peak ONLY, item 281) · one_source_selftest.py ·
rl_export.py · the store re-ingest writes · derived + re-pins · session_2026-07-17/legc_relay/ · the PR.
OUT (touch = HALT): any other store field/row · Leg-B's map/dial/constants (incl _proj_w4 / _uncomp_prod) ·
docs/ · ui · config manifest · the pick curve · any re-tune.

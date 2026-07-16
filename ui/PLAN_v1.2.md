# UI v1.2 — THE CLUB VALUATION LAYER · PLAN (first committed artifact)

Directive: `docs/DIRECTIVE_UI_v1_2_club_valuation_2026-07-16.md`. TIER 3, `ui/`-fenced, no value is
recomputed. Base = the SHIPPED board (tag **v2.10**, board **790136a3**); asserted below.

## BASE + STAMP ASSERTIONS (all PASS at plan time — verified in a read-only dry run)
- `ui/app/config.js EXPECTED_BOARD == "790136a3"` ✓ · working bundle `stamp.board == 790136a3…` ✓ ·
  `stamp.tag == v2.10` · `engine fc7045d6` · `store b1fd0bce`.
- **Canonical pick curve located + stamp-asserted (the S5 stale-curve guard):** the shipped board's
  own pick currency is `rl_app_data.json["PVC"]`, which `rl_export.py` sets to the **adopted
  `engine/rl_after/pvc_curve_L1b.json`** (R3 bake-guard: the held-out `pvc_fit_candidate.json` is
  UNBAKEABLE; numéraire anchor `pick1 == 3000`). It rides into `ui/data/board_view_working.js` as
  `pvc` under the board's own md5 stamp. Cross-check: bundle `pvc` == `pvc_curve_L1b.json` over all
  shared picks ✓, `pvc[1]==3000` ✓. The ingest RE-ASSERTS this byte-match every run; a mismatch or a
  missing curve is a HALT-AND-ASK. **No sheet value is ever ingested.**
- Ladder `2027 value multiplier` cell = **0.9**; R104.5 balanced discount = **0.10** → `1−0.10 = 0.90`
  → **they agree** (no HALT). 0.10 governs; the sheet cell is read + reconciled only.

## THE JOB
1. **Club-name display map (item 178(1)).** `MD.config.CLUB_DISPLAY` + `MD.fmt.club(name)` — the three
   owner-named AFFL clubs shortened (North Melbourne Kangaroos→"North Melbourne" · Collingwood
   Magpies→"Collingwood" · Port Adelaide Power→"Port Adelaide"). Applied at every affl_team display
   site (board rows, club header/banner, the new summary page, the card). **Keys/joins untouched** —
   the long name stays the join key; only the rendered string changes.

2/3. **Inputs ingest + pick pricing (items 2,3; the no-LLM pipeline first half).**
   `ui/tools/ingest_inputs.py` — deterministic Python, read-only over `docs/inputs/` + the board
   bundle + the engine curve. **VALIDATE-OR-HALT.** Emits `ui/data/club_valuation.js`
   (`window.__CLUB_VALUATION__ = {…}`). Validations (each prints a verdict; any fail ⇒ `halt` set,
   overlay refuses):
   - PVC stamp/byte match vs the shipped engine curve; `pvc[1]==3000`.
   - bands within 1–80 and low ≤ high (all 160).
   - every Picks `Owner` joins to exactly one AFFL club (+Free Agents permitted); origin likewise.
   - both drafts ≤ one year ahead (2026/2027 only, base 2026).
   - player names join board↔Player_Locations↔Future_Positioning with ZERO ambiguity via a normalised
     name key (casefold+space-collapse); the two Max Kings asserted distinct ("Max King" vs "Maxwell
     King"). 5 case-only surname variants (MacDonald/Macdonald …) are reconciled by the normal key and
     NOTED, not halted.
   - pick-count conservation: ledger count == Σ per-club counts == 160 (the Dashboard convention).
   - ladder 2027 cell reconciles to 0.90.
   **Pricing:** held pick value = MEAN of the canonical PVC over `[low, high]` inclusive; 2027 × 0.90.
   Ownership is the authored CSV (agrees with the board's `affl_team` today — 0 mismatches, reported).

4. **Club valuation filters (item 178(2)).** Board team-context gains **PLAYERS ONLY** (default,
   current behaviour) / **PICKS INCLUDED**. Picks-included, single-club: the club's held picks list
   (origin · year · round · band · value) renders under the roster and the club total gains
   `+Σ picks`. Issued picks appear ONLY here — the +1/+2 placeholder players are untouched.

5. **Team summary page (item 178(3) / the item-173 page).** New `ui/app/clubs.js` (+ "Clubs" nav
   tab). One sortable table, all AFFL clubs, default-sorted by **Overall Value**; columns: Overall ·
   Total Player · Total Picks · Top-5 · Top-10 · **Best-23** · Non-Best-23. Best-23 = greedy positional
   fill (2 K-DEF·4 G-DEF·5 MID·4 G-FWD·2 K-FWD·1 RUC) by highest board `v` per slot on CURRENT
   posCode, then 5 best-remaining as bench (exact for this structure). Rows link to the club's filtered
   board view. **Count note:** the AFFL league has **16 clubs** + a Free-Agents pool (not 18); the
   summary ranks the 16 real clubs, Free Agents excluded (it is a pool, not a roster). Flagged in RETURN.

6. **Owner update flow (item 181(2) / 178(4); no-LLM second half).** `ui/HOW_TO_UPDATE_INPUTS.md`.
   **FALLBACK TAKEN + declared:** load-time raw-fetch of a binary `.xlsx` from the offline `file://`
   viewer (no external libs, no XLSX parser, by design) is infeasible, so the no-LLM path is the
   deterministic **regeneration script** (`ingest_inputs.py`) — no model in the loop, validate-or-halt.
   Flow: edit sheet → upload over `docs/inputs/<same name>` (GitHub web, owner's click) → run the one
   regeneration command → reload the board. The doc walks it + every HALT message and what it means.

7. **Deferrals (flag only):** posture lens toggles + the +1/+2 re-enable ride post-Leg-E. Untouched.

## FENCE / METHOD
IN: `ui/` only + read-only fetches of `docs/inputs/`. No engine/store/PVC/gate/docs writes. Per-item
commits, each with a before/after screenshot. RETURN ≤30 lines with the clean-ingest verdict list, all
160 picks priced, top-3 clubs named with numbers, the one-pager path, the fallback taken.

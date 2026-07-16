# DIRECTIVE — UI v1.2: THE CLUB VALUATION LAYER · 2026-07-16
### TIER 3 · ui/-FENCED · runs IN PARALLEL with the chapter's Leg A (S3: disjoint files, read-only vs
### store/engine) · NEVER on the bake ladder · fires on the owner's paste into a FRESH Claude Code
### chat. Candidate branch + PR; merges only on the owner's click after his viewing.

## EFFORT: Medium (spec v1.1 §7). Why not High: display + a deterministic ingest + a greedy fill;
no valuation code is touched. Why not Low: four features, one new page, and a data pipeline with
HALT semantics. Build model: Opus.

## MODE: auto — FIRST COMMITTED ARTIFACT is the PLAN. TIME: one session; flag >2× or <½×.

## BASE PIN (full URL): main AT OR AFTER `7a34429d95705bbd1746cc72172052e6b726f23f`,
`git diff --name-only 7a34429..main` = docs/-ONLY (the pen moves main; the Leg-A candidate lives on a
BRANCH and is NOT your base). **You base on the SHIPPED board:** tag `v2.10`, board `790136a3` —
assert `ui/app/config.js EXPECTED_BOARD == "790136a3"` and every bundle stamp before touching
anything; a mismatch is a HALT. The UI NEVER recomputes a value.

## FEED (fetch at the pinned SHA; documents, never prose):
`docs/OPEN_ITEMS_REGISTER.md` items **178** (the owner's feedback batch, VERBATIM — it is the product
spec) · **180** (the filed inputs + validation: name-keying, the two distinct Max Kings, the pick
workbook's four sheets) · **181(2)** (the no-LLM edit requirement) · **173** (the ranking-page
history) · `docs/DECISIONS_v107_2026-07-16.md` **R104.5** (2027 pick discount: **balanced 0.10** —
the only posture in this build) · `docs/SPEC_PVC_FLEX_CHAPTER_v1_2026-07-16.md` §7 ·
`docs/inputs/AFFL_Pick_Locations.xlsx` · `docs/inputs/AFFL_Player_Locations.csv` ·
`docs/inputs/AFFL_Future_Positioning.csv` (name→stable-ID map only) · CORE v2.8 (S1–S6).

## THE JOB (per-task commits, one before/after screenshot each)
1. **CLUB-NAME WRAP FIX (item 178(1)):** a DISPLAY-NAME MAP for exactly the three owner-named clubs —
   North Melbourne Kangaroos → "North Melbourne" · Collingwood Magpies → "Collingwood" · Port
   Adelaide Power → "Port Adelaide". Display-only; keys/joins untouched.
2. **THE INPUTS INGEST (deterministic, VALIDATE-OR-HALT; the no-LLM pipeline's first half):**
   parse the pick workbook's **Picks** sheet (ID · Year · Round · Origin · Owner · Pick low/high) and
   **Ladder** sheet (team finish ranges + the 2027 multiplier cell — READ it, but R104.5's 0.10 is
   the governing number; if the sheet says 0.9, they agree; if not, HALT and flag) and the player
   locations CSV. VALIDATIONS (each prints a verdict; any failure HALTs the overlay, never guesses):
   bands within 1–80 and low ≤ high · every Owner in the AFFL club set (+ Free Agents) · both drafts
   ≤ one year ahead · player names join to stable IDs via the positioning file with ZERO ambiguity
   (the two Max Kings are distinct by name — assert it) · pick-count conservation per the workbook's
   own Dashboard convention. **Values from the sheet are NEVER ingested** — the Pick Values tab and
   Raw Value columns are reference-only.
3. **PICK PRICING (balanced posture only):** a held pick's value = the engine's CURRENT canonical
   pick curve (locate the canonical export; STAMP-ASSERT its provenance against the shipped engine —
   the S5 stale-curve failure never repeats; a missing/ambiguous stamp is a HALT-AND-ASK) evaluated
   as the MEAN over the band [low, high]; 2027 picks × (1 − 0.10). **Issued picks appear ONLY in the
   club-valuation context (owner law, item 178(2))** — the +1/+2 placeholder players are untouched.
4. **CLUB VALUATION FILTERS (item 178(2)):** the team-context view gains "PLAYERS ONLY" (default,
   current behaviour) and "PICKS INCLUDED" (players + the club's held picks, listed with band + value).
5. **THE TEAM SUMMARY PAGE (item 178(3) — the item-173 page, owner-specced):** one ranked table, all
   18 clubs, default-sorted by Overall Value, every column sortable: **Overall Value** (players +
   picks) · **Total Player Value** · **Total Picks Value** · **Top-5 players** · **Top-10 players** ·
   **Best-23** — the best positionally compliant team: fill 2 K-DEF · 4 G-DEF · 5 MID · 4 G-FWD ·
   2 K-FWD · 1 RUC by highest board `v` per slot from the club's roster using CURRENT posCode, then
   the 5 best remaining players of any position as bench (greedy is EXACT for this structure — no
   fallback needed) · **Non-Best-23** (Total Player Value − Best-23). Club rows link to the club's
   filtered board view.
6. **THE OWNER UPDATE FLOW (item 181(2), the no-LLM second half):** the ingest reads
   `docs/inputs/` FROM THE REPO AT LOAD (raw fetch, pinned to main), so the owner's update path is:
   edit the spreadsheet → upload the file over `docs/inputs/<same name>` via the GitHub web UI (his
   click, no agent) → reload the board; the ingest validates-or-halts on the new bytes. SHIP a
   one-page `ui/HOW_TO_UPDATE_INPUTS.md` walking that flow (with the halt messages he might see and
   what each means). If load-time fetch is infeasible from the sitting-view file, fall back to
   committed derived bundles + a regeneration script, and SAY SO in the RETURN — do not silently pick.
7. **DEFERRALS (flag in RETURN, do NOT build):** posture lens toggles and the +1/+2 re-enable ride
   post-Leg-E (spec §3 Leg E / §7). The board's canonical values are balanced and untouched.

## FENCE
IN: `ui/` only (+ read-only fetches of docs/inputs). OUT (touch = HALT): engine/store/PVC code ·
gates · ALL docs/ writes (builds never author docs; the HOW-TO lives under ui/) · the Leg-A branch ·
any value recomputation.

## RETURN (≤30 lines + artifacts): branch · head SHA · PR number · per-item screenshots · the
validation verdict list from a clean ingest of the CURRENT inputs (all 160 picks priced; the top-3
clubs by Overall Value NAMED with their numbers, so the owner can eyeball against his Dashboard) ·
the update-flow one-pager path · any fallback taken · "in plain terms" close.

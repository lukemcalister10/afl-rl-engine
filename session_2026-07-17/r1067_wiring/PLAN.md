# R106.7 WIRING — the leg-blind bar, floor half + item-284 + two owner data corrections

**Branch:** `claude/r1067-wiring-v11-m86stv` (base `6306378` = legc-relay-dpp-law @ store md5 `0efdc5d6`).
**Effort:** High · **Mode:** auto · **Est:** 3–6 h (confirmed).

## Established from the code (probe already read; full ACT-1 verdict is a separate pushed artifact)

- **The site.** `v_at_peak` (distribution_pricing.py:250-269) is where §1b lands. Its `raw = proj_from_peak(...)`
  blend (lines 262-267) is the **already-wired projection half** (item 295). `max(prod, MA.prod_floor(p,lens))`
  (line 269) is the **floor half** this job wires — via `prod_floor` (rl_model.py:441-450).
- **The floor's year-0 number** = `prod_floor`'s `k==0` term: `posval(cur+capt_prem(cur)-REPL[bnow])*21`,
  charged at full weight (`wt=1.0`), no SEASON_PROG split today. `val(prod)` wraps the raw sum (nonlinear ⇒ the
  §1b blend must be done PRE-`val`, on the raw posval, exactly as the projection half does it).
- **FENCE FINDING (halt-and-ask trigger).** On the SHIPPED board (`run_panel.sh` → `_merged_recover.py::ev()`),
  `MA.prod_floor` is monkey-patched to `_merged_recover.py::_prod_floor_w4` (line 816-828, **OUT of fence**), a
  DUPLICATE floor loop that runs for PROVEN players (`n>=PROVEN_N=4` & W4 ctx). Non-proven players fall back to
  the base `rl_model.prod_floor` (**IN fence**). The board/book path (`build_cohort_book.py`) does not load
  `_merged_recover`, so it uses the base function directly. ⇒ ACT-1 names a floor site outside the fence.
  Per the item-281 law I HALT at the checkpoint and ask before touching anything.

## The two owner data corrections (job 1 — done first, own commit)

Stable-ID edit on the SOURCE store, minimal textual replace (no full reserialize; every other row byte-equal):
- McKercher `afl-player-v1-ec36ae407a5d9b9384e1`: `eligibilities` `"G-DEF,G-FWD"` → `"G-DEF,MID"`.
  Fixes a present∉collapsed error (present MID ∉ {GEN_DEF,GEN_FWD}); after: MID ∈ {GEN_DEF,MID}. Bar moves
  GEN_FWD→GEN_DEF ⇒ most of item-295's +105 comes back off.
- Jake Lloyd `afl-player-v1-797837193a7c4b847d81`: `eligibilities` `"MID,G-FWD"` → `"G-DEF,G-FWD"`.
  Fixes present∉collapsed (present GDEF/GEN_DEF ∉ {MID,GEN_FWD}); after: GEN_DEF ∈ {GEN_DEF,GEN_FWD}. Lowbar
  stays GEN_FWD both ways ⇒ ≈ unchanged, now legitimate.
- Validate-or-halt: token vocab hyphenated/comma-joined/no-spaces; present ∈ collapsed for BOTH; net Δ = 0 bytes.

## ACT 1 — the prod_floor probe (job 2 — CHECKPOINT HALT, pushed, then ASK)

Answers (from the code): (a) the floor's remaining-season component is NOT season-scaled today — the whole k==0
present year is charged at full weight vs REPL[bnow]; §1b introduces the SEASON_PROG split (banked `sp` vs bnow,
remaining `1-sp` vs lowbar), pre-`val`. (b) age enters only via `pa_=PEAK_AGE[bnow]`/`frac`/H; §1b leaves the
level path + horizon keyed to present — only the k==0 REPL bar splits. Fence verdict: IN for rl_model.prod_floor;
the proven-player shadow `_prod_floor_w4` is OUT. **Ask the owner** whether base-path wiring suffices (proven-DPP
floor on the shipped board reported as a known gap) or the fence extends to the W4 copy.

## After paste-back (jobs 3-5)

3. **Floor half.** In `rl_model.prod_floor`, split the k==0 REPL term pre-`val`:
   `sp*posval(base-REPL[bnow]) + (1-sp)*posval(base-REPL[lowbar])`, `lowbar=y0dpp_bar(p)` (Now-board only).
   Endpoint assert (sp=0 ⇒ whole year-0 vs low bar; sp=1 ⇒ no-op). Banked component + years-1+ untouched.
   RL_FLEX=0 ⇒ y0dpp_bar None ⇒ byte-exact off. (Mirror into the W4 copy only if the owner extends the fence.)
4. **item-284.** Amend `y0dpp_bar` (and `_collapse_elig` proof): the four cross-class sets
   {KEY_DEF,GEN_FWD}·{KEY_FWD,GEN_DEF}·{RUC,GEN_FWD}·{RUC,GEN_DEF} and present∉collapsed ⇒ return None (single-
   position, no dual bar), REPORT BY NAME (committed artifact), build continues (never halt). Same-line K/G stays
   the silent R105.1 collapse. Add both classes to `one_source_selftest.py` as flag-and-name flex-era checks
   (verdict always produced — silence is a red) + in-session unit-proofs on all four pairs + one present∉ synthetic.
5. **Derived + battery.** Rebuild board/book/panel; re-pin `expected_boot`; per-gate committed verdicts;
   A/B chain (RL_FLEX=0 ⇒ 807e6551 on the corrected store); named rows; the two ledgers. G-COHORT 1.30 = sole
   hard halt; sub-1.08 floor = reported, not halt.

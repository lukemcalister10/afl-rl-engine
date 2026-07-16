# WALK-FORWARD BOOK CALIBRATION — PLAN (auto-mode first artifact)

**Directive:** Walk-Forward Book Calibration v1.1 (Tier 3, READ-ONLY, S3). Priced vs realised, by
cohort, walk-forward. Baseline instrument for the PVC chapter's spec rework (items 130–133).
**This file is committed BEFORE any calibration number** (mode auto). It fixes the cohort grid, the
realised-value construction, and the smoothing spec so the numbers are ruled by a declared method, not
chosen after seeing them.

**Effort band confirmed:** High, 2–4 h. Will flag if it blows past 2× / under ½×.

---

## 0. BASE + SEAL PROVENANCE (what is being scored, and the proof it is the sealed book)

- **Base commit (STRICT):** `9be07b8e5939eeade71106ef1eaee112df183441` — the chapter's final head
  (captaincy build, PR #94). The bake tags this same commit, so this IS the bake head's data.
- **Guard-5 identity at base (asserted, all PASS):** store `b1fd0bce` · engine head `fc7045d6` ·
  rl_model `f79fc740` · config `c2d233ae` · band `cm_400 34faa865` · register `652d83e8`.
- **Book regenerated (scratch, NOT committed over anything):** the frozen generator
  `engine/rl_after/s4_matrix_M1v7.py` run in **gate mode** (RL_CONFIG_MODE=gate → ambient model env
  cleared, `data/model_config.json` pinned), against the base engine in an isolated workspace. Output
  `__meta__` = {engine_head `fc7045d6`, store `b1fd0bce`, config `c2d233ae`, n_players **2649**} —
  **every identity stamp matches the committed seal `data/book_stable_seal.json`.**
- **Seal-assertion status — DECLARED HONESTLY (CORE reporting rule):**
  - **N = 2649 ✓** and **all identity stamps == the seal's stamps ✓.**
  - The committed seal's `stable_sha256 = 99be9b36…`. The regenerated gate book on THIS runner hashes to
    `1b3c856a…`. **Bit-exact stable-hash equality did NOT reproduce across runners.** This is the
    project's known cross-CPU float non-associativity — the same class of issue the determinism chapter
    order-fixed for the *board* (the PAR linear solve); the walk-forward book runs `ev()` as-of across
    24 seasons × 2649 players, a wider float surface not covered by that board-level fix. Thread count
    is ruled out (1-thread build == default build == `1b3c856a`).
  - **Direct content bound (the decisive check):** the book's present-value column `cur` (the 2026
    board path) is cross-validated against the **committed canonical board** from the captaincy session
    (`session_2026-07-15/captaincy/measurement/board_cand.json`, built on the sealing runner). It
    reproduces **2638 / 2649 = 99.6 % EXACT** (raw SCAR); the 11 non-exact are ≤ 4 SCAR float drift
    (e.g. English 3402 vs 3405) plus one edge record (`harrison-jones-haw`, a near-zero board value).
    The generator's own parity law (`book.cur == round(board.v × F)`) holds in the numéraire for the
    same 2638.
  - **Verdict:** the scored book IS the sealed base book, reproduced faithfully; the hash divergence is
    a machine fingerprint (≤4-SCAR drift on 0.4 % of cells), **far below the cohort signal.** The
    calibration is cohort-aggregated and kernel-smoothed, so this drift cannot move a cohort verdict. A
    per-cell robustness note quantifies the headroom in the FINDING.

---

## 1. WHAT "PRICED" AND "REALISED" MEAN HERE (grounded in the book + register)

The book is a walk-forward panel. Per player record (2649 players, 13 628 player-year cells):
`year` = draft class C · `pos` ∈ {MID, GEN_DEF, KEY_DEF, GEN_FWD, KEY_FWD, RUC} · `type` (ND/RD/rookie
families) · `pick` (effective) · `yrs = [C+1 … yend]` · **`Vpath`** = engine as-of PRICED value per
year (walk-forward; the price the book put on the player using only data ≤ Y) · **`Ppath`** = the
REALISED era-adjusted SC average delivered that season (0 if no games) · `cur` = 2026 present value
(board path) · `anchor` = end-of-Yr1 price · `draftval` = PVC pick price at entry.

**Units reconciliation (the crux).** PRICE (`Vpath`/`cur`, SCAR value) and OUTPUT (`Ppath`, SC points)
are different units; the engine's map from output → value is exactly the object under audit. The
register fixes the axes (item 131, verified in code):
- **OUTPUT = above-replacement production** `o = level − REPL[pos]`, with the engine's own table
  `REPL = {MID 80.1, GEN_DEF 78.3, RUC 78.5, KEY_DEF 68.4, GEN_FWD 70.9, KEY_FWD 66.8}` (English +28.4,
  Briggs +9.5 → **output 2.99×**). Here `level` is a **realised** quantity taken from `Ppath` (actual
  delivered output), not an engine estimate — that is what "the walk-forward actually delivered."
- **PRICE = the book's value** (`cur` / `Vpath`) (English 3423 raw, board 3405; Briggs 1599/2182 →
  **price 2.14×** raw). The gap 2.99×→2.14× is the compression (item 131); `iso_corr` then demotes the
  higher pick (item 132).

## 2. TWO INSTRUMENTS (both "priced vs realised"; each serves named axes)

### Instrument 1 — CONTEMPORANEOUS output→price map (serves items 131 compression, 132 iso trough)
One point per player in its **current mature state**:
- `o_i` = **realised current level above replacement** = mean of the player's era-adjusted SC average
  over its **most-recent-2 delivered seasons** (games≥1, from `Ppath`) − `REPL[pos]`. (Recent-2 mirrors
  the engine's recency level; it reproduces English ≈ +28 / Briggs ≈ +5–9. A **recent-3** and a
  **top-3-sustained** variant are computed as a sensitivity band and DECLARED.)
- `p_i` = **current price** = `cur` (the value the owner disputes). A **peak variant** (`p = max Vpath`
  vs `o = top-3-sustained`) is reported alongside to separate the age/runway confound from the map.
- **Systematic layer:** fit the pooled log-log map `log p = α + β·log o` (kernel/local, §4) on the
  contributor population `o>0`, per position and pooled. **β<1 ⟺ the top is compressed** (a unit of
  realised output buys less price at the top). Report β with CI; item 131 implies β≈0.69
  (log2.14/log2.99) as the pairwise check.
- **Signed mispricing (under-priced positive):**
  `m_i = log(o_i/ō) − log(p_i/p̄)` — output log-multiple minus price log-multiple vs pool baselines
  (`ō`,`p̄` = geometric means of the contributor pool). `m>0` = delivered more, relative to the pool,
  than priced for = **under-priced**. Compression shows as `m` rising with `o` (top under-priced);
  the floor shows as `m<0` (over-priced) at the bottom.
- **Residual layer (item 132):** after conditioning on `o`, age and position, take the residual by
  **pick band** and draft class. The `iso_corr` mid-round trough (RUC pick-19 → 0.885, pick-25 → 0.896,
  pick-30 → 0.832, vs pick-34 → 1.000 — a *better* pick, worse permanent multiplier) predicts a
  negative residual for high-value mid-round picks; measure **what remains after the trio reprice**.

### Instrument 2 — WALK-FORWARD priced-then vs realised-later (serves item 130 young cohorts)
For **matured** cohorts only (draft class C with ≥5 seasons elapsed by 2026, i.e. C ≤ 2021), compare
the **as-of-young price** (`anchor` = Yr1 value, and `Vpath` at tenure k∈{1,2,3}) to the **realised
value delivered** (the player's realised sustained output above replacement, and the mature `cur`).
- **Question (item 130):** are young prices systematically **below what the same players realised**
  (young under-priced), and by how much — expressed as the guard's currency (the G-COHORT y4/y5/y6
  young-class ratios, guide 1.20–1.25 / hard 1.30). Per item 131 this is a **BASELINE/DIFF instrument**,
  never a mandate to lift: it establishes the current young gap and the guard headroom, so a later cure
  can be scored by whether it *widens* the gap or *eats* headroom.
- **Right-censoring / truncation:** active players' careers are incomplete → realised is right-censored;
  Instrument 2 is restricted to matured cohorts, and truncation is stated per cohort (share still
  active). Present cohorts (C ≥ 2022) get Instrument 1 only, flagged "realisation incomplete".

## 3. COHORT GRID (draft class × age/tenure × position group; finest honest resolution)

Primary axes, from coarse→fine, with **support-gated refinement** (a slice splits only if it keeps
n ≥ N_min after the split; else it stays pooled and the pooling is DECLARED in the output):
- **Position group** (6): the primary axis (REPL and iso are position-keyed).
- **Age / tenure:** tenure `k = Y − C` (years since draft) is the panel axis; **age** (from the record)
  is the cross-check axis. Age bands: ≤22 (young), 23–26 (prime-build), ≥27 (proven/veteran) — the
  register's own cut (item 130 uses exactly these) — refined to finer bins where support holds.
- **Draft class C:** individual years where n permits; else pooled into eras (pre-2010, 2010–2015,
  2016–2020, 2021–2023, 2024–2026) — declared.
- **Pick band** (Instrument-1 residual + iso axis): 1–6, 7–12, 13–20, 21–34, 35–50, 51–70, rookie/
  pickless — chosen around the mid-round trough (13–34) so it is resolved, not smeared.
- **Type family:** ND/RD vs rookie families (MSD/SSP/IRE/UNR/PDx) reported separately where it matters
  (rookie o→p differs); pooled otherwise, declared.

**N_min = 12** for a reported smoothed cell; **n ≥ 30** for a "firm" verdict, 12–29 "indicative",
< 12 "pooled/withheld". Every reported cell carries its **n** and its **uncertainty** (§4). Cohort
support (data description, not calibration): draft classes 2010–2025 carry ~88–141 players each;
contributor pool (o>0) is the scored population — its size is reported per cell.

## 4. SMOOTHING SPEC (CORE rule 7 — finest supportable resolution, pooled slices DECLARED)

- **Kernel/local smoothing** over the continuous axes (`log o`, age, `log pick`): Nadaraya–Watson /
  local-linear with a Gaussian kernel; bandwidth by Silverman's rule per position, floored so the
  effective window never holds < N_min points (the floor is what "finest *supportable*" means — where
  data is thin the window widens and that widening is reported as the effective-n per cell).
- **The pooled o→p map** (Instrument 1 systematic) is a local-linear fit in `log o`; β is the local
  slope, reported globally and per position, with a **bootstrap** 95 % CI (1000 resamples, player-level
  resample to respect the one-point-per-player design).
- **Per-cell uncertainty:** every calibration cell reports n, effective-n (post-kernel), the point
  estimate, and a **bootstrap SE / 95 % CI**. Cells whose CI spans zero mispricing are marked
  "not distinguishable from fair" — a cohort is only called under/over-priced if its CI excludes 0.
- **DECLARED POOLING:** any slice that is pooled (age band widened, draft classes merged, type families
  combined, kernel window widened past a single bin) is listed in a `POOLING_DECLARED` block in the CSV
  and the FINDING, with the reason (support). No silent bin widening.
- **Survivor handling:** the contributor/mispricing population is defined by realised output, so
  players who never delivered (`o ≤ 0`, ~the near-zero `cur` mass, median cur = 14) are **kept** and
  reported as the "sub-replacement / never-delivered pool" (n, share priced at floor) — NOT dropped
  (dropping them is survivor bias that inflates realised). Instrument 2 likewise keeps busts (their
  realised is low by construction), so young under-pricing is not measured only on the winners.

## 5. OUTPUTS (what gets committed)

1. `PLAN.md` (this file).
2. `calibrate.py` — the analysis (reads the seal-asserted scratch book; reproducible from base).
3. CSVs under `out/`: `cohort_calibration.csv` (the signed mispricing surface: cohort, n, eff-n, mean
   priced, mean realised-output, price-multiple, output-multiple, **signed mispricing m (under-priced
   +)**, bootstrap CI, POOLING flag) · `output_price_map.csv` (pooled + per-position elasticity β, CI —
   the compression) · `iso_pickband_residual.csv` (item 132 trough, remaining after trio) · `young_
   cohort_walkforward.csv` (Instrument 2, item 130, guard currency) · `worked_rows.csv`.
4. `FINDING.md` — the calibration, the three named axes in plain terms, robustness/limits.
5. `OWNER_READ.md` — one page: what the numbers support, what they don't. **No cure proposals.**
6. `RETURN.md` — ≤30 lines + branch + head SHA + PR number.

## 6. FENCE (restated)
IN: read-only analysis; scratch book regeneration (seal-asserted, not committed over anything); writes
only under `session_2026-07-15/book_calibration/`. OUT: any store/engine/config/board/gate/doc write ·
any lever, cure or prototype · the bake and the aging measurement (parallel jobs — not mine). No cure
proposals — the PVC spec rework is the supervisor's, on this baseline. Scope growth ⇒ STOP and return.

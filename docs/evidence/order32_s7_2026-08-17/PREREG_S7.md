# PREREG — ORDER 32 SEAT S7: THE PEDIGREE-LEG CELL FANS

Committed and pushed BEFORE any cell fan is computed. READ-ONLY MANDATE: this seat writes only into
`docs/evidence/order32_s7_2026-08-17/`. No engine, board, or law file is touched.

Program brief: issue #334 comment 5311991190 (ORDER 32). This seat measures the empirical outcome
distribution behind the pedigree leg's v0 cell means, and delivers the design document for the
player-level variance object. The candidate law under which everything here is read:

    price = rho(g) * Phat + [ D(c_u)*(1-rho(g)) + Phi*beta*rho(g) ] * v0

## 1. Populations — the fits' OWN input constructions, reused, not reinvented

**ND lane (pick x position).** Exactly the rows the positional v0 surface is fitted on, by the
verbatim construction at `docs/evidence/candidate_31f/o31f_headfix.py:80-85`:

    L2 = docs/evidence/grace_adoption_2026-08-13/inputs/LAYER2.json
    L1 = docs/evidence/grace_adoption_2026-08-13/inputs/layer1_player_seasons.json
    row(k in L2.fit_nd_keys) = ( pick = L2.attribution[k].pick,
                                 value = L2.grace_a[k].total,
                                 pos  = L1.entries[k].position_group )

CONTROL C1 (able to fail): the population must be 1142 rows with per-position counts
KPD 125 / KPF 143 / MID 422 / RUCK 60 / SD 180 / SF 212 (HEADFIX_31F_out.txt line 5). Any
deviation halts the instrument.

**Pool lane (pool arm).** The `o30a2_recut.py` prefix (everything before `SURF = ...`) is exec'd
VERBATIM — the same transplant `o31f_pool.py` performs, and the file md5 must equal the one
POOL31F.json pins: `fe6f436ab23056d717f693091946309a`. The population loop is then the verbatim
POP construction of `o31f_pool.py:69-83`: non-ND entries with an attribution, a signed pool v0
cell (`MA.pool_v0_of`), an entry year and a grace-A career score; arm = `e['type']`; fitted
window 2004-2021.

CONTROL C2 (able to fail): the fitted pool population must be 840 rows of 1080 total
(POOL31F.json `fade.population_fitted` / `population_total`). Any deviation halts.

## 2. The value measured

Realized career delivered value `ga_total = grace_a[key].total` — the DV lane's grace-A career
score on the #338 minimum-tenure basis. This is THE SAME NUMBER the v0 fits consume as their
target (`value=GA[k]['total']` on the ND lane; `ga_total` on the pool lane). No DF discounting is
applied (the fit rows carry none), no winsorising, no smoothing, no shrinkage. Quantiles are of
raw outcomes.

## 3. Cells

**ND primary cut:** pick bands {1-10, 11-20, 21-30, 31-40, 41-64} x position
{KPD, KPF, MID, RUCK, SD, SF}, PLUS the position-pooled row per band (the all-in band fan).

**ND finer cut (conditional):** position-pooled 5-pick bands
{1-5, 6-10, ..., 56-60, 61-64}; this cut is PUBLISHED only if every cell in it has n >= 34
(the q97 resolution floor of §5); otherwise it is reported as UNSUPPORTED with its n's, and the
primary cut stands alone.

**Pool primary cut:** arm in {RD, SSP, MSD, UNR, IRE, PDA, PDN, PDS}, position-pooled (the
pool arms are known-thin; position-pooling is declared here, up front, not decided after seeing
the data). Any arm label found in the data outside this list is reported under its own name,
never merged.

**Pool per-position split (conditional):** published for an arm x position cell only where that
cell has n >= 20, and flagged as a split of a thin arm. Position here = the pool row's day-0
position group as the o30a2 prefix carries it.

## 4. The quantile estimator

The project's OWN `q()` (o30a2_recut.py): linear interpolation between order statistics at index
`f*(n-1)`. Levels: q10 / q30 / q50 / q70 / q90 / q97 — the production fan's six levels (b6 =
five `cond_prior_band` levels + the q97 head; priced through WQ6 = [.18 x5, .10]).

## 5. Resolution and thin-cell bounds — declared BEFORE the data is seen

- A level f is RESOLVED in a cell iff n*(1-f) >= 1 (at least one order statistic strictly above
  the interpolation index). q97 therefore needs n >= 34; q90 needs n >= 10.
- An UNRESOLVED level is reported as the sample MAX and flagged `BOUND(max)` — a bound, not an
  estimate. It is never smoothed, never interpolated from a neighbouring cell, never borrowed.
- A cell with n < 8 (the project's own N_FLOOR, POOL31F.json `fade.n_floor`) publishes NO fan:
  it reports n, n_zero, min / median / max only, flagged UNRESOLVED.
- Every cell reports: n, n_zero (ga_total <= 1e-9), zero-share, mean, the six levels with
  per-level resolution flags, mean/median, and the fitted-v0 comparator of §6.

## 6. The mean-vs-fit statement

Outcome q-fans of a cell will NOT integrate to the fitted v0 — v0 is the mean of a skewed
distribution (and on the ND lane it is additionally a local-linear, shrunk, PAVA'd, conserved
transform of the cell means, not the raw cell mean itself). Per cell we therefore report
explicitly: (a) the raw cell mean of outcomes; (b) the cell median; (c) mean/median; (d) the
fitted v0 comparator — ND: the head-fixed `posv_headfixed[g][p]` averaged over the cell's own
rows; pool: the mean signed `pool_v0_of` of the cell's rows; and (e) mean_outcome / fitted_v0.
The skew (mean >> median, zero-spike + right tail, widening with pick number) is the EXPECTED
signature and is the finding, not a defect to be corrected here.

## 7. Expected shapes (stated before measurement)

- Late picks (41-64): median near zero, q90/q97 far above the mean — the lottery structure.
- Early picks (1-10): median of the same order as the mean, fan comparatively narrow.
- Pool arms: RD the widest-supported arm; several arms thin enough that only bounds publish.
- Mean > median in essentially every cell.

Deviations from these expectations are reported as findings, not adjusted away.

## 8. Outputs

- `CELLFANS_S7.json` — every cell, machine-readable, with controls and md5s.
- `CELLFANS_S7.md` — owner-readable inline tables.
- `CELLFANS_S7_out.txt` — full console transcript.
- `s7_cellfans.py` — the instrument itself.
- `DESIGN_S7.md` — objective B (the design document; no measurement content gated on it).

## 9. What this seat does NOT do

No refit, no smoothing of fans, no wiring, no engine/board/law edits, no touching of S6's emit.
The board's ruler stays the mean; everything here is measurement + design for owner ruling.

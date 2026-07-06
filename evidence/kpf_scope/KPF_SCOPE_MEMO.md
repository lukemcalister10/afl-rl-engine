# KPF Loose-Pricing — Scope & Proposal (analysis only, no board change)

**2026-07-06 · v2.5 board (store `e1b4d8bf`, engine `efea88e5`) · analysis only — no fit, board untouched.**
Re-measures SETTLED #9 (`docs/DECISIONS_v75_2026-07-06.md:29-31`) and proposes treatments for the owner to choose.
The raw Wave-1a derivation of the held figures was cited to `evidence/measurements_ledger.md` (PR #40, unmerged —
absent from this checkout); the numbers below are a **fresh** re-measurement on the live v2.5 board.

## Store assert
Board **UNTOUCHED**. `md5(rl_model_data.json) = e1b4d8bf` on both `engine/rl_after/` and the workspace copy
(pinned `baked-v2.5-2026-07-05`). All measurement was read-only; `git status` shows only this memo added.

## Locus (who / how many)
KEY_FWD (`KPF`) = `GRP['KFWD']` (`rl_model.py:36`), one of 6 future-position groups; pricing keys curve/peak/aging
off `gfut(p)`. On the priced **board** (805): **103 KEY_FWD** (vs 195 MID). KPF carries the lowest replacement bar
(`REPL=66.8`), lowest expected peak (`EXP_PEAK_BASE=44.7`, `PEAK=72`) and latest peak age (27) of any group —
i.e. key forwards score few SC points and cluster near replacement, which is the root of the loose value spread.

## Re-measured vs held (finest resolution, per-player, no binning; board pool with demonstrated production)

| Finding | Held (SETTLED #9) | Re-measured (v2.5 board) | Verdict |
|---|---|---|---|
| Spread-ratio (value/production dispersion), **CV metric** | KEY_FWD **6.09** vs MID **4.25** | KEY_FWD **6.57** vs MID **4.17** | **CONFIRMED** |
| Elite disconnect (top KPF vs near-replacement ref) | **24.71×** value on **1.36×** production | **27.3×** value on **1.60×** production (P25 ref) | **CONFIRMED** (regime) |
| KPF in the aging-fix locus | **0** | **8–20** (see below) | **CORRECTED** |

**Method / pooling declared.** Production = `cp._lvl_eff_orig(p,2026)` (the engine's demonstrated SC level, the input
the pricing and the decliner-shed both read); value = `ev(p)` (the board price). Pool = board members of the group
with production > 0 (KEY_FWD n=103, MID n=195); no-games sit-out anchors excluded. "Spread-ratio" is reported as the
**coefficient-of-variation ratio** `CV(value)/CV(production)` — this is the statistic that reproduces the held pair
(6.09/4.25). Note the metric choice matters: a P90/P10 relative-spread ratio inverts the ordering (KEY_FWD 16.6 vs MID
24.6), because MID has a longer thin low tail; the CV metric is the one SETTLED #9 used and is declared here. Elite =
top KEY_FWD by value; the held 24.71×/1.36× is reproduced against a **near-replacement (≈P25) reference** — at the group
median the ratio is a milder 13.1× value on 1.45× production. Either way the qualitative finding holds: **value fans out
~13–27× while production barely moves (~1.4–1.6×).**

**Aging-locus overlap — the one correction.** The "aging-star fix" is the demonstrated-level floor
`prod_full = max(prod_v, pf)` (`rl_model.py:659-660`), live in the band via `v_at_peak` → `max(prod, prod_floor)`
(`distribution_pricing.py:255`). Measured on the board it binds for **223 players** (matches the documented ~224:
Petracca, Dawson confirmed floored) — of which **20 are KEY_FWD**. Narrowing to the aging-*star* case (floor binds
**and** old-past-peak proven) still leaves **8 KEY_FWD**; the live overlay DECLINER SHED (`_merged_recover.py:177-181`,
relative drop `Lo−Lc > DOWN_TOL=3`, keyed on the player's OWN SC decline — not an absolute floor) catches a further
**9 KEY_FWD**. So the held "0 KPF" is **not literally true** under any operationalization.

**But the design conclusion of SETTLED #9 still stands.** Where the aging fix touches a KPF it (a) acts on a low absolute
SC base, so the correction is small, and (b) corrects a *different* failure — a proven star whose projection regressed
below still-current output — not the KPF loose-pricing failure, which is value fanning out on tiny production differences
*near replacement*. The aging fix is the wrong instrument for the KPF locus; a KPF-specific treatment is still required.

## Proposed treatments (choose one — NOT implemented here)

- **T1 — KPF-specific production→value curve.** A KEY_FWD-only re-anchor of the above-replacement leverage (a KPF
  `BETA/ICPT` or an effective-floor lift on the `posval(level − REPL)` softplus, `rl_model.py:264-267,318`) so value
  tracks production more tightly and the near-replacement cluster stops fanning out.
  *Tradeoff:* re-levels all 103 KEY_FWD and needs a fit + owner board review; risks flattening the genuine young-KPF
  speculative ceiling (Duff-Tytler / Darcy type — the known KEY_FWD over-compression flag), so the fit must protect the
  demonstrated-elite tail.

- **T2 — KEY_FWD spread compression.** A mechanical group-level compression pulling elite KPF value toward the group
  centre to bring the CV spread-ratio from ~6.57 down toward the MID ~4.17 reference.
  *Tradeoff:* leaves the production→value shape untouched (simpler, no refit) but is blunt — it can under-price a
  genuinely elite KPF and does not fix the root cause (leverage of small production edges near a low replacement bar).

## in plain terms
Key forwards score few fantasy points, so almost all of them sit bunched just above the replacement line — and the pricing
curve turns tiny gaps in that bunch into huge gaps in dollars (value spreads ~6.6× as widely as production for KPFs vs
~4.2× for mids, and the best key forward is worth ~25× a replacement one while producing only ~1.5× as much). The
aging-star fix can't clean this up: it was built to rescue proven stars whose *projection* dipped below what they're still
scoring, it works off absolute SC levels that key forwards mostly never reach, and even where it does clip a KPF it's
fixing the wrong thing (the earlier "0 KPF" was slightly overstated — a handful are touched — but the effect is tiny and
beside the point). Key forwards need their own fix. The owner should choose between **T1** — retune the KPF
production→value curve so price follows output (more correct, needs a fit and care not to crush genuine young-gun
ceilings) — and **T2** — a blunt spread compression on the KPF group (quick, no refit, but can under-price a real elite).

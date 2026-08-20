# PREREG — ORDER 30B-R, THE RESOLUTION SEAT

**Filed before any resolution quantity exists.** `land/order-29`, parent tip `7a1c6ee` (ORDER 30B-P
preview board `6a392bca7ad0dee04a6b4f037c758f65`). Date 2026-08-15.

> **NOTHING IS GREENLIT. NOTHING WIRES.** This order closes three *design* gaps the 30B-P preview
> surfaced — by measurement (T2, T3) and by definition (T1) — and frames the fourth (T4) as an owner
> word. No engine file is edited, no board is built, no dial is added. The lane is
> `docs/evidence/one_machinery_2026-08-14/resolution/` and nothing else.

---

## 0 · THE THREE GAPS, AS THE PREVIEW LEFT THEM

| gap | the preview's finding | this order's task |
|---|---|---|
| **G1** the first-game cliff | `σ(1) = 0.9218` against `D(2) = 0.5502`; `josh-smillie` **471 → 1671 (+254.8%)** on one game. Ruling 6's continuity curve **FAILS**. | **T3** — join the cumulative backbone (≤10 games) to the σ curve (≥16 games), anchor game 0 to the wired sitter law. |
| **G2** the pedigree OBJECT | the blend's pedigree leg is the Step-1 positional `v0` (kako **759.8**); the machinery it replaces leans on `entry_anchor` (kako **1069.0**). | **T4** — quantify both, recommend, do not take. |
| **G3** the share's READING | weight form wired (`(1−w) = σ`); value form not built. kako **748** vs the brief's **900–1000**. | **T1** — resolve *by definition* from the 30B-M harness. |

Plus the owner's in-session **Kako year-3 scenario** — path A (36 modest games in yrs 1–2, then 75 avg
over 20 games in yr 3) against path B (sat two years, then the identical season) — which under a
raw-games clock prices B **above** A. **T2** tests the candidate fix: the engine's own ruled
recency-weighted evidence clock `u = Σ_s games_s × 0.25^(Y − year_s)`.

---

## 1 · METHOD, FIXED IN ADVANCE

**Sources, all committed and pinned by MD5 in every harness:**
`docs/evidence/pedigree_persistence_2026-08-14/{o30bm_measure.py, PERSISTENCE_TABLE.json}` ·
`docs/evidence/sitter_fade_2026-08-14/SITTER_FADE_PACKET_2.md` §6.4 (the cumulative backbone) ·
`docs/evidence/one_machinery_2026-08-14/preview/PREVIEW_MOVERS.json` (804 rows: `production_pts`,
`v0_step1_board`, `sigma`, `fade_D`, `fade_clock`, `cg`) ·
`docs/evidence/grace_adoption_2026-08-13/inputs/layer1_player_seasons.json`
(MD5 `ad1229ea6f443538479447132382b21c`).

**The engine is loaded READ-ONLY**, from a staged copy under the scratchpad, for scorer callables and
`entry_anchor` only — the identical staging 30B-M used. Pinned five-var environment
(`PYTHONHASHSEED=0`, `OPENBLAS/OMP/MKL/NUMEXPR/VECLIB_*_THREADS=1`), sequential, foreground.

**T2's held-out criterion, fixed here before it is run.** States: the 30B-M population — ND
`effective_pick` 1–64, `entry_year ≥ 2005`, state year ≤ 2019 (H = 6 fully observed), force-majeure
pair excluded. Target `R`: the 30B-M discounted remaining 6-season delivered value, unchanged.
Model: the 30B-M `band_fit` design **unchanged** — `R ~ [pos dummies, age, age², o, o², cur, cur3,
games_at_Y, log1p(clock)] + v0`, fitted within clock bands. **Two clocks only:** raw career games `g`
and recency-weighted `u`. The `u` band edges are set by **the raw bands' own population quantiles**
(so the two clocks are compared on identically-sized bands and no edge is chosen after seeing a
result). **Scoring: 5-fold cluster cross-validation, folds by `md5(player key) mod 5`** — deterministic,
no seed. **Metric: pooled out-of-fold RMSE against `R`; lower wins.** Pooled out-of-fold R² and MAE are
reported beside it. **The winner is whichever clock has the lower pooled OOF RMSE. That is the whole
criterion and it is not renegotiable after the reading.**

**T3's join, specified here before it is fitted.** Common object: **printed price at fixed output**.

1. **g = 0** — anchored to the wired sitter law exactly: `price(0; c) = v0 × D(c)`.
2. **1 ≤ g ≤ 10 (thin lane)** — the 30A2 cumulative backbone, §6.4, taken as a *relative lift on the
   sitter price*: `price(g; c) = v0 × D(c) × b(g; c)`, `b(g; c) = B(≤g, depth) / B(≤0, depth)`,
   knots `k ∈ {0, 2, 5, 10}`, interpolated **log-linearly in `log1p(g)`**. Depth-2 knots for `c < 2.5`,
   depth-3 knots for `c ≥ 2.5`; **depth 4 is not extrapolated** (the 30A2 packet declines to wire it),
   so `c ≥ 3.5` holds the depth-3 lift. Disclosed, not hidden.
3. **g ≥ 16 (deep lane)** — the σ persistence curve where it was measured, under **both** readings, so
   the join does not depend on T1's verdict.
4. **11 ≤ g ≤ 15 (bridge)** — **linear in `log1p(g)` between the thin lane's value at g = 10 and the
   deep lane's value at g = 16.** Continuous at both ends by construction. **The conflict in the overlap
   is measured and published separately** (thin lane extrapolated up to 15 against deep lane
   extrapolated down to 11) and is **not** averaged into the wired shape.

**Dispersion and n are reported on every fitted quantity. Nothing is tuned after a reading. Breaches
are owned by number.**

---

## 2 · THE NUMBERED PREDICTIONS

### T1 — the reading, resolved by definition

**R1.** The 30B-M harness constructs σ as `σ_b = β_v0 × mean(v0) / mean(R)` (`o30bm_measure.py`
`band_fit`, line 531) — a ratio of the pedigree term's mean contribution to the mean of the **outcome**.
**Prediction: σ is definitionally a VALUE share, not a mixing weight, so the WEIGHT wiring is NOT the
faithful reading of the measurement.**

**R2.** **Prediction: neither offered wiring is the regression.** The fitted equation is
`R = Π + β·v0 + ε` with the production block `Π` entering at **unit** weight; σ is a derived
*reporting* statistic of that fit, not a coefficient in it. **The faithful wiring is the ADDITIVE form
`price = production + β(g) × v0`, and `β` — not σ — is the object the harness actually estimated.**

**R3.** **Prediction: the weight form's implied value share differs from σ on all four named rows**, and
the direction is set by `v0` against price: it *overstates* pedigree where `v0 > price`. Since
`mean(v0)/mean(R)` exceeds 1 in **every** measured band (2.362 / 1.833 / 1.483 / 1.074 / 1.104),
**prediction: the weight form overstates the pedigree value share in aggregate across the blended book.**

**R4.** **Prediction: under the additive-β form kako prints in [880, 960]** — i.e. **inside the brief's
900–1000 band that the preview breached low at 748** — because the additive form does not shrink his
744.3 production leg by `(1−σ) = 0.761`. *(Seat note, filed blind: the arithmetic
`744.3 + 0.2233 × 759.8` is what motivates the band. If this holds it means P7's breach was a wiring
artefact, not a measurement failure.)*

**R5.** **Prediction: the value (harmonic) form prints kako BELOW the weight form's 748**, because a
harmonic blend is dominated by its smaller leg and `production 744.3 < v0 759.8` only narrowly — so the
harmonic price lands within 20 points of both. Predicted range **[720, 760]**.

### T2 — the clock

**R6.** **Prediction: the recency clock `u` beats raw `g` on the preregistered pooled OOF RMSE**, by at
least **0.5%** relative.

**R7.** **Prediction: the recency clock partially subsumes the AGE_LENS separation** — the ≤20 vs 24+
matched pick-contrast difference at the 16–35 band (preview: **+532.9**, 90% `[+184.2, +881.7]`,
z **+2.51**) shrinks by **≥ 30%** when the band is keyed on `u` rather than `g`. Reason stated in
advance: an older player at 16–35 *raw* games carries those games further back, so his `u` is lower and
he moves down a band, which is precisely the confound the age lens was reading.

**R8.** **Prediction: under a raw-games clock the Kako path-B (sat two years) year-3 price exceeds
path-A (36 modest games first) by 20–30%**, reproducing the owner's arithmetic; **and under the recency
clock the gap closes to ≤ 10%**, but **does not fully close** (it will not reach 0%, because 36 modest
games two and three years back still decay to a real residue).

### T3 — the join

**R9.** **Prediction: under the join, `josh-smillie`'s 0 → 1-game step is ≤ +25%** (it was **+254.8%**).
**The cliff closes.**

**R10.** **Prediction: the joined price curve 0 → 15 at fixed output is monotone non-decreasing for
`josh-smillie`**, i.e. Ruling 6's continuity acceptance curve **passes** under the join where it failed
under the preview.

**R11.** **Prediction: the two measured curves genuinely CONFLICT in the 11–15 overlap** — the thin-lane
extrapolation and the deep-lane extrapolation differ by **≥ 25%** in relative price at g = 13. This will
be shown as a conflict, with both curves published, **not averaged away**; the bridge is declared as a
bridge.

### T4 — the object

**R12.** **Prediction: `entry_anchor` exceeds the Step-1 positional `v0` on ≥ 60% of the 715 blended
rows**, with a median ratio `entry_anchor / v0` in **[1.05, 1.45]**.

**R13.** **Prediction: pedigree as a share of printed rises by ≥ 3 percentage points on the whole
blended book** when the share is applied to `entry_anchor` instead of the Step-1 `v0` (preview
whole-book value share: **0.1342**).

### Housekeeping

**R14.** **Prediction: `git diff 7a1c6ee..HEAD` touches only
`docs/evidence/one_machinery_2026-08-14/resolution/`.** No `engine/`, no `data/`, no board, no dial, no
committed artifact outside this lane moves. No GitHub comment is posted.

**R15.** **Prediction: every number in the packet is reproducible from committed artifacts plus a
read-only engine load**, and the resolution harnesses write nothing outside this lane and the
scratchpad.

---

## 3 · WHAT THIS ORDER WILL NOT DO

- It will **not** choose the pedigree object (T4). That is stated as an owner word and framed with both
  sides priced, including what is genuinely lost either way.
- It will **not** wire anything. The re-priced named rows in the packet are labelled
  **DERIVED, NOT BUILT** — arithmetic on committed legs, not an engine board.
- It will **not** smooth, average, or reconcile the 11–15 conflict. If the two measured curves disagree
  there, the disagreement is the finding.
- It will **not** re-open Step-3's forbidden-set boundary word (STOP §5 Q1–Q4). Those stay OPEN.

*Filed and pushed before the first resolution quantity existed.*

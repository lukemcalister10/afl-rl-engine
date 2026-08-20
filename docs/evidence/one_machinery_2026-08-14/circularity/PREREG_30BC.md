# PREREG — ORDER 30B-C · THE CIRCULARITY DECOMPOSITION

**Seat:** ORDER 30B-C measurement seat · `land/order-29` · 2026-08-16
**Status of this file:** committed and pushed **BEFORE any outcome quantity of this order was computed.**
Everything below §5 is a falsifiable commitment made blind. Two structural facts were read before filing
(the committed panel re-derives at **4,033 states over 767 careers**, and the committed harness md5 is
`e910fe6482ab7b05a92f18c173667073`) — both are *reproductions of already-published structural counts*,
not outcome quantities of this order, and they are stated here as such.

**READ-ONLY. NOTHING WIRES.** No board, store, engine, curve or config file is touched. This order writes
only into `docs/evidence/one_machinery_2026-08-14/circularity/`.

---

## 0 · THE SUSPICION BEING TESTED

The owner, verbatim:

> *"the raw or stalling players get to hold on to their pedigree much longer, a value propped up by the
> pedigree players of the past who went on to achieve something — and I suspect those players are the
> sharp tier guys who played early and well."*

**The claim, made operational.** 30B-M measured a pedigree coefficient `β_b` inside each games band — the
per-unit-`v0` slope of realized remaining delivered value after production, age, position and output have
taken everything they can. 30B-R ruled the faithful wiring of it to be **additive**: `price = P + β(g)·v0`.
The suspicion is that `β_b` at the low/mid-games bands is **not** delivered evenly by the players sitting
in those states — it is delivered almost entirely by the ones who were about to break out, so a player who
keeps stalling is being paid, year after year, out of a conditional expectation whose mass belongs to
somebody else's career.

**This order does not re-open β. It decomposes it, exactly, by who delivered it.**

---

## 1 · BASIS — THE COMMITTED PANEL, REUSED, NOT REBUILT

| element | value |
|---|---|
| panel | the 30B-M primary panel: ND `effective_pick` 1–64, entry years ≥ 2005, state years ≤ 2019, `H = 6` |
| harness | `docs/evidence/pedigree_persistence_2026-08-14/o30bm_measure.py`, md5 **`e910fe6482ab7b05a92f18c173667073`**, **asserted at entry** |
| reuse mechanism | this order `exec`s the committed harness **verbatim up to its `q1 = {}` line** (data load, engine staging, `build_states`, `panel`, `ols`, `cluster_se`, `band_fit`) and calls those objects. **No arithmetic of 30B-M is retyped.** |
| control | panel asserted at **4,033 states / 767 careers**; the five committed band coefficients asserted **to 1e-9**: `0.29683 · 0.36226 · 0.22330 · 0.15315 · 0.02007` |
| Layer 1 | `layer1_player_seasons.json` md5 `ad1229ea6f443538479447132382b21c`, asserted at entry and exit |
| the wired law | `price = P + β(g)·v0`, `β(g)` = the **log-linear-in-log(g) interpolation of `READING.json::beta_curve.points`** — the 30B-R object, read from the committed artifact, never retyped |
| bars | `BARS[pos]` as the committed harness reads them **off the engine** (Ruling 1 asserted): KPD 65.4 · KPF 63.8 · MID 77.1 · RUCK 75.5 · SD 75.3 · SF 67.9 |

**Bands measured:** `0–5`, `6–15`, `16–35` (the brief's low/mid bands). `36–70` and `71+` are computed and
printed for context but no prediction is scored on them.
**Pick tiers:** **T1 = `effective_pick` 1–20** · **T2 = 21–64**. (These are the brief's tiers, not 30B-M's
five bands; the five bands are printed beside them.)

---

## 2 · THE ATOMS, DEFINED BEFORE ANYTHING IS COMPUTED

**A DELIVERED SEASON.** Season `y` is *delivered* iff the player has a store row at `y` with
**`games ≥ 10` AND `avg ≥ BARS[pos_played(y)]`** — a full season's worth of football at or above his own
position's replacement bar, on the engine's own bar, at the bar-group the harness assigns that season.
Anything else — no row, `games < 10`, or at-bar-below — is a **STALL SEASON**. No row is imputed; a
missing season is a stall season, exactly as 30B-M treats it as a zero.

**THE OUTCOME CLASS of a state `(i, Y)`**, on realized seasons only, inside the same `H = 6` window as the
target:

| class | definition |
|---|---|
| **(a) BREAKOUT** | at least one delivered season in `{Y+1, Y+2}` |
| **(b) SLOW-BLOOM** | no delivered season in `{Y+1, Y+2}`, but at least one in `{Y+3 … Y+6}` |
| **(c) BUST** | no delivered season in `{Y+1 … Y+6}` |

Exhaustive, mutually exclusive, computed from the store rows the panel already carries.

**A CONTINUED STALLER at the state** = a state whose `Y+1` and `Y+2` are both stall seasons = classes
(b) ∪ (c). **A STALL PATH of length `k`** = `k` consecutive stall seasons `Y+1 … Y+k`.

---

## 3 · THE THREE MEASUREMENTS

### M1 — THE DELIVERY DECOMPOSITION (exact, not approximate)

Within band `b`, let `Z` be the committed `band_fit` design **minus** the `v0` column, and let
`ṽ0 = v0 − Z(Z'Z)⁻¹Z'v0` be the residualised entry ruler. By Frisch–Waugh–Lovell the committed
coefficient is **exactly a weighted sum of the realized outcomes**:

```
β_b  =  Σ_i c_i ,        c_i  =  ṽ0_i · R_i / Σ_j ṽ0_j²
```

`c_i` is **state `i`'s delivery of the coefficient, in β units.** The identity `Σ c_i = β_b` is asserted to
**1e-9** against `band_fit`'s own output in every band; if it does not hold the order reports the failure
and stops.

Reported per cell (band × tier × outcome class):
- **n**, and the cell's share of the tier's states;
- **signed mass share** `Σ_{i∈cell} c_i / β_b` (sums to 1 across all cells of the band);
- **gross mass share** `Σ|c_i| / Σ_band |c_i|` (who *moves* the coefficient, regardless of sign);
- the same mass expressed in **board points per state** (`c_i · v̄0_band`, so it is readable against a price);
- **dispersion of `R_6`**: mean · p25 · median · p75 · zero share; and mean `v0`, mean `ṽ0`.

**Thin cells:** `n < 8` is not reported as a cell — it collapses into its tier's total for that band and
**every collapse is disclosed by name and count.** No cell is dropped silently.

### M2 — THE STALL-PERSISTENCE QUESTION

For the continued stallers (classes b ∪ c) in each band × tier:

1. **What the law pays at the state:** `β_wired(g_Y) · v0`, the 30B-R additive law's pedigree leg.
2. **What they measured forward:** realized `R_6` with full dispersion, and the **measured pedigree
   excess** = mean residual against the band's own **pick-blind** fit (the committed `band_fit` design
   with the `v0` column removed) — the same instrument 30B-M §2.1 used, restricted to this subgroup, with
   a 300-replicate player-cluster bootstrap on the mean.
3. **The re-price:** for those who have a state at `Y+2` (i.e. played that season), the games advance
   `g_{Y+2} − g_Y`, the law's pay there `β_wired(g_{Y+2})·v0`, and their realized `R_6` from `Y+2`.
4. **β re-fitted on the stall subpopulation** (`β_stall`, states whose next two seasons are both stall
   seasons), band by band, with the committed `band_fit` callable. **If a stall band has `n < 40` the
   committed harness refuses to fit it and this order reports NO SIGNAL for that band rather than
   loosening the rule.**

### M3 — THE WIRED-LAW CHECK ALONG HISTORICAL STALL PATHS

For every T1 (picks 1–20) state in the low/mid bands with a stall path of length `k ≥ 2`, walk the path
year by year and print, at each successive state: `g_t` · `β_wired(g_t)` · **law pedigree pay**
`β_wired(g_t)·v0` · **cohort-measured pay** `β_stall(band(g_t))·v0` (falling back to `β_b` where the stall
band is not estimable, **labelled**) · the **gap** · and the realized `R_6` from that state. Aggregated by
`k = 0,1,2,3,4+` with n and dispersion, and printed as **named historical paths** for real players.

**No tuning.** One pass. Every quantity is the committed harness's arithmetic or a stated identity on it.

---

## 4 · WHAT THIS ORDER MAY NOT DO

MAY NOT: modify the board, store, engine, curve, config or any wiring; re-fit `β`, `τ`, the v0 ladder or
the join; post GitHub comments; recommend a dial. **It measures the owner's suspicion and reports whether
it is true.** Any wiring consequence is stated as a consequence and left to the owner.

---

## 5 · THE PREDICTIONS (committed blind, scored by number)

**C1 — CONTROL.** The panel re-derives at exactly **4,033 states / 767 careers**, all five committed band
coefficients reproduce to **1e-9**, and the FWL identity `Σ_i c_i = β_b` holds to **1e-9** in all five
bands.

**C2 — CLASS MIX.** The BREAKOUT share of states rises with games across the three low/mid bands: it is
between **20% and 55%** at `0–5` and between **45% and 80%** at `16–35`, and it is higher in T1 than in T2
in all three bands.

**C3 — THE OWNER'S CLAIM, PRIMARY LEG.** In tier T1 (picks 1–20), **BREAKOUT states carry ≥ 60% of the
tier's gross β-mass in every one of the three low/mid bands**, and **BUST states carry ≤ 15%** of it in
every one. *This is the owner's suspicion stated as a number; the seat expects it to measure TRUE.*

**C4 — NOBODY COLLECTS ON A BUST.** Across the three low/mid bands **pooled**, states whose player never
had a single delivered season in the entire six-season window (class BUST, both tiers) carry **< 8% of the
gross β-mass** while being **> 15% of the states**. The mass and the population are decoupled.

**C5 — THE STALLER DOES NOT COLLECT.** In T1, the measured pedigree excess (mean pick-blind residual) of
the continued stallers is **less than one third** of the breakouts' in all three bands, and in **at least
one** of the three bands its 90% cluster-bootstrap interval **contains zero**.

**C6 — THE LAW DOES NOT SELF-CORRECT THROUGH `g` (the mechanism).** Because a stalling player accumulates
games slowly, the wired `β(g)` barely moves along a stall path: the **median** two-season change
`|β_wired(g_{Y+2}) − β_wired(g_Y)| / β_wired(g_Y)` for T1 continued stallers is **≤ 25%** in the `0–5` and
`6–15` bands. **And, because the committed `β(g)` curve RISES between its 2.5-game and 10.5-game knots, at
least one named T1 stall path will show the law paying MORE pedigree in a year the player stalled than in
the year before.**

**C7 — THE OVERPAY, AND ITS SIGN.** Along T1 stall paths, the law's pedigree pay exceeds the stall
cohort's measured pedigree contribution at **every** step `k = 1, 2, 3`, and the mean gap is **wider at
`k = 3` than at `k = 1`**.

**C8 — THE STRONG FORM (the seat's riskiest prediction).** In the `0–5` band, the mean of the wired law's
pedigree leg `β_wired(g)·v0` over T1 continued stallers **exceeds their entire mean realized `R_6`** —
i.e. the pedigree top-up alone is larger than everything those players went on to deliver in six seasons.

**C9 — THE NAMES EXIST AND CUT BOTH WAYS.** At least **six** T1 careers have a `k ≥ 2` stall path from a
low/mid state, and at least **one** of them is a genuine slow-bloom who later delivered large value — so
the report will name both an overpaid path and a vindicated one.

**C10 — PROCESS.** One measurement pass. No quantity is tuned after being read. Thin cells collapsed by
the §3 rule and disclosed by name. Every breach above is owned by number in `CIRCULARITY.md`, and any lens
that carries no signal is reported as carrying no signal.

---

## 6 · DELIVERABLES

`docs/evidence/one_machinery_2026-08-14/circularity/`: **this file** · `o30bc_circ.py` (the harness) ·
`CIRCULARITY.json` / `CIRC_out.txt` (raw readings) · **`CIRCULARITY.md`** — the owner-facing answer in his
own terms. Pushed to `land/order-29`. No GitHub comments. **NOTHING WIRES.**

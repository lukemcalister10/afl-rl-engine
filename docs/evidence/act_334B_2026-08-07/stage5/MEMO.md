# STAGE 5 — MEMO: the design, the roads not taken, and every judgement this seat made

Read `README.md` first for the verdict. This file is the reasoning, including the parts that did not work.

---

## 1 · The mechanism, and the two sites

`sitout_ev`'s anchor leg becomes `G · R · entry_anchor(p)`, hoisted once and used at **both** anchor
sites — the blend term and `_surprise`'s anchor argument. Nothing else in the engine is touched.

`_ped_prior`'s `R(τ)/r0` ratio is **not** an anchor: it is a decay statistic, a ratio of two retention
readings whose scale cancels. `G` does not enter it (Addendum 2, site precision). Had `G` entered it,
the pedigree term would have silently re-scaled and stage 4 would have been retuned by a side effect.

**Road not taken:** applying `G` to the whole blended price rather than the anchor leg. That would have
lifted `lam · e_full` too — i.e. lifted the player's *demonstrated production* because his *class* was
under-priced. The owner's standing law is that the fix stays personalised: "games played AND how they
were played both matter". Lifting only the benefit-of-the-doubt leg keeps the player's own record
pulling through `e_full` and the surprise statistic, untouched.

---

## 2 · The teaching target

For every `(player, evaluation-year)` row the engine routes through `sitout_ev`, reconstructed under the
matrix emitter's own walk-forward as-of convention:

```
F        = mean_k [ v(Y+k) / 1.0939^k ] ,  k = 1..4,  busts and out-of-window = 0
G(cell)  = Σ w·(F − lam·e_full)  /  Σ w·(1−lam)·R·A          (kernel- and value-weighted)
```

`F` is the round-2 M2 statistic — the realised discounted future — and the ratio is the engine's own
blend solved for the anchor leg. It is the same shape `R_SURF` was itself taught in (`r = O/V0`, kernel
smoothed, eff-n ≥ 35, isotonic), which is why the two compose cleanly.

**The horizon is a choice and it is disclosed.** `k = 1..4` matches round 2's yr1..yr4 window. The
sensitivity is printed in `FRONTIER.txt`: at `K=3` the quiet starters' measured future reads `0.9758`,
at `K=4` `0.9541`, at `K=5` `0.9099`. **`K=4` is neither the most nor the least favourable** — it is the
one round 2 used, chosen before the landing was known and not revisited after.

**Road not taken:** a fixed point (teach, rebuild, re-teach until `G` and `lam` agree). The directive
forbids it — "taught ONCE from the frozen baseline book, then frozen (no fixed-point)" — and the ban is
right: a fixed point on the engine's own output is how a valuation model learns its own optimism.
§4 records what that ban cost.

---

## 3 · THE TEACH BUDGET, AND WHAT WAS SPENT ON WHAT

The directive allows **one taught pass and at most one re-teach**. Both were used. This section exists so
the supervising seat can audit whether the re-teach was a correction or a tune.

### Pass 1 — taught, built, and fully gated
Board `2772d386`. Whole-cohort yr1 **0.9914**. Quiet starters **0.8780** against their own measured
`0.9541` — **92.0% of honest**. Table filed as `teach_g5_PASS1_superseded.py`.

### The re-teach carried THREE corrections, all diagnosed from pass 1's measurement

**(a) The τ bandwidth was smearing the boundary knot.** τ mass in the teaching book sits at 1.0 / 2.0 /
3.0 (1649 / 1254 / 383 rows) — the fractional τs are the live board, not the book. A τ bandwidth of 0.50
gives every τ=2 row a weight of `exp(−2) = 0.135` when estimating the τ=1 knot, and there are nearly as
many of them, so the τ=1 knot — the one the yr1 landing is read at — was pulled **down** toward the faded
interior. Fixed at 0.35 and never grown; only pick and games grow for eff-n. The surface stays continuous
because the **engine** interpolates between τ knots, exactly as `_R_surf` does over its own integer depths.

**(b) The games axis has a ruled seam at zero and the kernel was smoothing across it.** Round 2
established, and the directive adopted, that the zero-games first-years and the quiet starters are two
populations with *opposite* honesty verdicts. Smoothing across that seam imports the no-lift verdict into
the quiet-starter knots. The `g=0` knot is now taught from `gcum==0` rows only, the `g≥2` knots from
`gcum≥1` rows only. The engine still interpolates continuously over `log1p(games)` between them.

**(c) THE ONE THAT LIFTED THE LANDING, and it needs the most scrutiny.** Pass 1 read the composed law as
`G · R ≤ 1` at every knot — the aging law taken through the `τ=0` pin. That is an **over-read**, and
Addendum 2 says so in its own words: the `τ=0` cell is pinned *because* "no listed player evaluates
there; the no-arb year-0 column reads `v0_start`, not this leg". The engine agrees: its own
`_v0_curve_assert` checks depth monotonicity over `τ ∈ 1..6` and never through 0. Worse, `G·R ≤ 1`
constrains a **decomposed leg**, not a price — and the price is a blend, so the constraint bites in a
place the owner's law never spoke about.

The corrected ceiling puts the aging law where it means something: **no cell may be taught a price above
its own entry anchor**, i.e. the same estimator with `F` replaced by `A`:
`cap = Σw(A − lam·e_full) / Σw(1−lam)·R·A`.

**This seat is aware that the correction lifted the landing, and states the test it applied instead of
that fact:** is the corrected law the one the governing documents state? It is — Addendum 2's own
sentence on the `τ=0` pin, and the engine's own asserted domain. And the check that it is not a
loophole: the measured `F/A` came back **≤ 1 in every resolved cell**, so the new ceiling binds only
where the estimate is noise (the thin deep-RUCK cells), never on the quiet starters the act is for.
It bought **+0.0003** of the landing. **The correction is right and it is nearly worthless.** Anyone
auditing this should be reassured by the second half of that sentence more than the first.

### What the re-teach actually bought
`0.9914 → 0.9945` (+0.0031). Quiet starters `0.8780 → 0.8925`, i.e. 92.0% → **93.5%** of honest.
**No third teach was run**, and the landing was not chased.

---

## 4 · WHY THE SURFACE STILL UNDERSHOOTS — the honest account

The quiet-starter class lands at 93.5% of its own measured discounted future. The missing 6.5% is
**+0.0141 of whole-cohort entry value — more than twice the 0.0055 the floor was missed by.**

The diagnosis, as far as it was taken: `G` is solved from a **cell aggregate** at the **frozen** `lam`,
then installed, after which `lam` moves (the surprise statistic re-reads the lifted anchor — the site the
directive *requires* `G` to enter). The re-read is amplifying for a quiet starter whose `e_full` sits
below his anchor, but a value-weighted cell solve is not a per-player solve, and the players who dominate
the cohort denominator are not the ones the cell average is calibrated on.

**What this seat did NOT do, and would propose:** one *declared, single-pass* consistency correction —
teach `G`, install, measure the realised per-player price against `F`, apply the residual once, freeze.
That is one pass, not a fixed point, and it is arguably inside the directive's ban. It was not attempted
because the teach budget was spent and inventing a compliance argument for a third teach after two
misses is exactly how a seat talks itself into tuning.

**The claim this file does NOT make:** that 1.00 is unreachable through the sit-out leg. It is not
reachable *by this surface*, and the frontier table shows why.

---

## 5 · The taper — taught, not assumed

Addendum 2 required the τ=2 and τ=3 knots **measured before the fit**, with the owner's phase-out shape as
prior only. They were (1254 and 383 rows). What the measurement said:

* the fade is real and it is roughly the shape the owner guessed — quiet-starter `G` runs ~1.28–1.76 at
  τ=1, ~1.00–1.61 at τ=2, ~1.00–1.28 at τ=3, and **exactly 1.0000 at τ=6**;
* but it is **not uniform**: nonKPP fades to 1 by τ=3 at most picks, while KPP and the deepest pool picks
  carry a residual lift into τ=3–4. The surface says so; nothing was flattened to make the shape tidier.

The within-class gate turns the taper law into a number: the largest `|d ln G / dτ|` anywhere on the
shipped surface is **0.567570 per season**, and no player's realised season-to-season step exceeds it
(max **0.475835**). And the counterfactual is measured, not asserted: the **no-taper** arm (hard drop to
`G=1` at τ≥2 — the shape the owner rejected) deepens the persisting-unproven yr1→yr2 fall from −25.4% to
−31.2%, and the taper recovers **all** of it on the whole class (landed −25.0%) and about half on the
quiet-starter subset (−43.2% no-taper → −34.7% landed vs −25.4% baseline). **The quiet-starter subset
still falls harder than baseline. That cost is real, it is the one round 2 warned about, and it is
printed rather than netted away.**

---

## 6 · Pooling, declared

**183 of 300 nodes are POOLED** over the three retention classes; 117 are class-resolved. That is far more
pooling than pass 1 (12 nodes), and the reason is (b) above: splitting the games axis at the ruled seam
halves each node's population, so the eff-n ≥ 35 discipline pools more often. **That is the discipline
working, not failing** — the alternative was class-resolved knots carried by a handful of rows, which is
what produced pass 1's RUCK cells at `G = 2.4–2.7` before the ceiling trimmed them.

Eff-n is computed on the **influence** weight (kernel × value), not the kernel alone, because the estimate
is value-weighted: a node carried by three big anchors is not an eff-n of thirty.

---

## 7 · Everything this stage did NOT touch

The ladder `18203822` · the numéraire (pick-1 = 3000, `NUMÉRAIRE GUARD: PASS`) · `RL_PED_BAR` / `RL_SUR_W`
and the whole reactivity/surprise mechanism (composed with, never deleted — `RL_G5_W=0` reproduces
`b56bbdde` byte-exact through the full gate) · #336 bust-inclusive anchors · poles · `raw_ev` · ISO · the
production path · `v0surf` (re-verified unmoved at three dial values) · the store · `rl_model.py` ·
`engine/forward_valuation` · main.

---

## 8 · The judgement calls, listed, each with its road not taken

| # | call | road not taken |
|---|---|---|
| 1 | `G` multiplies the **anchor leg** at both anchor sites; `_ped_prior` excluded | apply to the whole price — refused, it would lift demonstrated production for a class reason |
| 2 | Teaching target solves the blend for the anchor at frozen `lam` | a fixed point — **forbidden by the directive**, and rightly |
| 3 | Horizon `K=4` | `K=3` (more favourable, `F=0.9758`) or `K=5` (less, `F=0.9099`); chose round 2's own window, before the landing was known |
| 4 | `G ≥ 1` everywhere, phasing **toward** 1 | allowing `G < 1` — refused: the owner's law is a phase-*out*, and cutting the zero-games class was found dishonest by round 2 in both directions |
| 5 | Aging law as **price ≤ entry anchor** per cell | pass 1's `G·R ≤ 1` through the `τ=0` pin — struck as an over-read (§3c), worth +0.0003 |
| 6 | τ bandwidth fixed, games axis split at the ruled seam | one smooth kernel over everything — struck as boundary smearing (§3a,b) |
| 7 | eff-n on the influence weight | eff-n on the kernel weight alone — would have declared thin value-dominated nodes "resolved" |
| 8 | Zero-games knots capped at the measured honesty gap (+0.02 in R) | letting them float — the ruling is explicit that this class is priced honestly already |
| 9 | Pick knots `[5,15,30,50,65]` (adding 65 for the pool index) | `R_SURF`'s own `[5,15,30,50]` with flat extrapolation — refused: pool rows are half the teaching book and deserve a resolved knot |
| 10 | **Side-by-side workbook NOT refreshed**; the sixth column built as a labelled CANDIDATE under `stage5/` | adding a sixth column to the adopted owner-review set — refused: the board did not land, and the owner's review set must not assert that it did |
| 11 | Near-projection criterion reported as a **failure**, with the reason | reclassifying it as granularity — refused: at +43% continuous it is not granularity, and amendment 1's fence was built around a *cut* |
| 12 | Gate-7's "the ladder cannot move" claim **struck in place**, with the correction visible | quietly editing the header — refused: the wrong claim and its correction are both on the record |

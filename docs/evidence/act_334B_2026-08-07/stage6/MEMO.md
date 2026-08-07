# 334 stage B / STAGE 6 — MEMO: the design, the roads not taken, and what this build got wrong first

Governing documents: directive v1 (#334 comment 5217307894) and **Addendum 1** (comment 5217452004),
which amends it and wins where they differ. Built on the stage-5 landing (comment 5217884618).

---

## 1 · The site, and why it is a fence rather than a choice

The directive asked the seat to MEASURE first and then choose between "the production path's young
player credit machinery" and "a taught overlay at the `ev()` production output". Addendum 1 removed
the choice: a correction anywhere on the production path leaks into the sit-out leg, because
`_prod_path` computes `e_full` **before** the leg dispatch and `sitout_ev` consumes it in both the
blend term and the surprise statistic. So the site is fixed:

```
    if ns==0: return round(sitout_ev(p,Y,e))          # <- the sit-out return
    if G6_W or G6_KPD: e = e*(1.0 + _g6_delta(p,Y,pos,e))
    keyruc = ...                                      # <- the staleness / mediocre caps
```

Two properties follow **by construction**, not by care: every sit-out price is untouched (the 165 are
then proved integer-identical anyway, positively, at every rung), and the frozen V0 surface cannot be
disturbed (`ev()` is not on the year-zero fit path — re-proven by declared refit). `RL_G6_W` is a
config-manifest dial and is **not** a `_V0SURF_GATES` key; `_V0SURF_GATES` was not touched.

Addendum 1 F14 fixes the composition order: the correction lands **before** the staleness and
mediocre-for-years caps, so a corrected price is still subject to every release the engine already
applies to it.

## 2 · The demonstrated-level axis: the one real design choice, made by measurement

The owner's hypothesis — *"there might be some cross sections where the signal is stronger, or where
it is already priced in"* — needs an axis that can express "already priced in". Two engine-native
continuous candidates were measured on the same frozen rows before either was chosen (`axis_probe.py`,
printed):

| candidate | value-weighted R² over 5 quantiles | picks 1-20 × above-median | picks 1-10 × top-tercile |
|---|---|---|---|
| `pr = bestlvl/par` (the cross-section's axis) | 0.0239 | 1.0096 | 1.0556 |
| **`z = log(e / entry_anchor)`** | **0.0720** | **0.9154** | **0.9380** |

`z` — how far the engine has *already re-rated* this player off his entry price — separates the
residual three times better and is the only one of the two on which the owner's named cell actually
reads at-or-below par. It is a pure state function of the record (it reads the pre-correction
production leg, never the corrected price), so it opens no feedback channel.

**The cost of that choice is stated in `FRONTIER.txt` §2**: on the `pr` reading the same cell is
*not* at par on this instrument, so the two readings disagree about which rungs the zero-cell gate
strikes. Both are printed and neither is chosen by the seat.

## 3 · The estimator: a marginal decomposition with ONE declared conservation scalar

Addendum 1 fixed the kernel at two axes and made every other axis a declared shape gate. Given that,
the shipped form is deliberately the plainest thing that can be audited line by line:

```
delta = W · d1 · B(cls, log-pick) · Stau(tau) · Sz(z) · Sg(gcum) · Tpk(pick) · Tage(age) / Z
```

each factor a **local value-weighted residual ratio** normalised to the headline, `Z` the single
declared conservation scalar. It is taught in ONE pass; there is no iteration to stop early and no
target to converge on.

### The road not taken: multiplicative backfitting

The first cut backfit the factors jointly. It **diverged** (`Sz` exploded on pass 2, the
renormaliser fell to 0.09) for the ordinary reason: a product of five shapes with normalisation on
only two is not identified. Two defects were found and fixed inside it before it was abandoned —
a naive ratio-of-sums estimator that let rows with **zero predictor mass** (taper zeros, faded clock)
pollute the numerator, and the missing identification constraints. It was abandoned rather than
patched: a fitter that can diverge is a fitter whose result depends on where you stop it.

### What the marginal form costs, measured rather than argued

`Z = 0.715015`. **|Z−1| = 0.285 IS the double-count**: the marginal product multiplies factors that
are correlated in the data (deep-ish picks tend also to carry low `z` and few games). The aggregate
is protected by `Z`; the **corner is not** — the surface can produce +162% at (nonKPP, pick 25, 6
games, z = −0.6) and realises +67% on the current board at rung 1.0. `FRONTIER.txt` §5. The method
fix is orthogonalised rather than marginal shape estimation. That is a re-teach, not a tune, and
this seat did not take it: it is a third structural change to the estimator inside one act, and
making it *after* seeing which rungs the gates strike is exactly the shape of tuning.

## 4 · The fade: measured, and faster than the owner's shape

Pooling the year-1/2/3 evaluation rows over the continuous clock (Addendum 1 F7) the raw residual is
**+0.1284 / −0.0447 / −0.1690**. Normalised to year 1 that is **1.0 / −0.348 / −1.316**: by the
year-2 evaluation the leg is not at par, it is *below* it.

Installed, after the isotonic non-increasing clamp to [0,1]: **[1, 0, 0, 0]** — linear in the
continuous clock from full at τ=1 to zero at τ=2, so the hand-over to arriving evidence is round by
round with no rollover step (probe (d): the observed max step equals the surface's own max slope
exactly).

**The clamp is declared and it is a decision.** The measured year-2 value is negative; installing it
would put a class markdown on a bonus dial, which is precisely the thing Addendum 1 F11 forbids for
KPD. The unclamped measurement is printed beside the installed one everywhere it appears. The honest
sentence is that the data extinguishes the premium **faster** than the owner's "phase out over
seasons 2/3" — the phase-out is not a shape imposed on the data, and the data wanted an even shorter
one.

## 5 · The KPD sub-dial

Young established KPDs measure **F′ = 0.748** — over-priced, and the cross-section reproduces it at
all three evaluation seasons. The owner's words described a **bonus**. So KPD rows are excluded from
the base kernel entirely (they do not lift it and they do not drag it) and carry their own
class-level scalar on `RL_G6_KPD`, default 0: **at the shipped sub-dial a KPD takes exactly zero.**
The identical-career KPD/KPF pair is printed at every rung on both dial settings (`PROBES.txt` (h)).

The KPD surface is a single scalar with no pick axis — n=35 cannot support one. Declared.

## 6 · What the two-axis kernel could not resolve

At eff-n ≥ 35 only `nonKPP` resolves its own pick axis. `KPP` (n=34 after the KPD exclusion) and
`RUCK` (n=11) are POOLED over all classes. The consequence is that the position signal the
cross-section found is largely flattened, and SF/SD — whose own cells measure at or below par —
receive the pooled nonKPP lift. `FRONTIER.txt` §8 prints measured against taught for every position.
This is a direct consequence of the kernel Addendum 1 fixed; it is reported, not worked around, and
a seat with a wider kernel mandate would resolve it.

## 7 · Two ordering defects this build found in itself

**(a) Fixed.** The monotonicity law originally ran *before* the conservation normaliser. The
normaliser divides the base by Z < 1 — i.e. scales it **up** — and re-broke the margin the law had
just secured (the probe suite measured −0.370 where the teach had printed +0.058). The two are
coupled and are now solved **jointly**, iterating the declared L-SMOOTH shrink κ against a
recomputed Z until both hold. Found by an independent probe, not by reading the code.

**(b) Disclosed, not fixed.** The pick-taper endpoint sweep that fixed the declared endpoints
34 → 48 was read under the same pre-normalisation ordering. Post-normalisation the picks 41-64 band
moves +0.516pp at rung 1.0 against its 0.5pp bound. The endpoints were **not** re-picked: re-picking
a declared boundary once you can see which rung it strikes is tuning, and it changes nothing that
matters (rung 1.0 is struck on independent grounds, and every other rung meets the bound).

## 8 · The measurement discrepancy against the cross-section of record

The populations reproduce exactly (414 / 684 / 818 against 414 / 684 / 819) but the levels do not:
this build reads **1.0963 / 0.9344 / 0.8205** where the cross-section reported **1.136 / 1.004 /
0.973**. The seat could not reconcile the cross-section's figures from its published method. The
surface is taught from **this build's own committed rows** and the conservation check is run against
**this build's own aggregate** — so the number the shipped surface conserves is 1.0963, not the
directive's 1.136. `FRONTIER.txt` §7.

## 9 · What this act deliberately does not do

* **No rung recommendation.** Four symmetric candidates; two struck by registered gates with the
  exact figure that struck them; the ruling is the owner's.
* **No relaxation of a gate to reach the owner's range.** The feasible half of the ladder lands
  0.006-0.021 above par on the teaching window and therefore SHORT of [1.04, 1.13]. Three roads out
  are named in `FRONTIER.txt` §4 and all three are the owner's.
* **No registry write.** Registering an un-adopted board poisons the column id against correction.
* **No store write, no ladder move, no numéraire move, no surface refit, no main merge, no tag.**
* **No cap on an individual lift**, because no registered gate carries one — the +67% realised
  maximum is filed as a finding instead.

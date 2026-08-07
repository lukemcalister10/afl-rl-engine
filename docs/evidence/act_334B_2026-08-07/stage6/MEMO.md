# 334 stage B / STAGE 6 — MEMO: the design, the roads not taken, and what this build got wrong first

Governing documents: directive v1 (#334 comment 5217307894) and **Addendum 1** (comment 5217452004),
which amends it and wins where they differ. Built on the stage-5 landing (comment 5217884618).

> **AMENDED 2026-08-07 by the CONFORMANCE REPAIR** (comment 5219329372). The original of this memo
> is kept verbatim as `MEMO_SUPERSEDED.md`. **Read section 10 first** — it says what was wrong, what
> changed, and why this is conformance and not tuning. Sections 2 and 8 carry amendment notes where
> they made claims the reconciliation refuted; the striking is in place, never by deletion.

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
| ~~`pr = bestlvl/par` (the cross-section's axis)~~ | 0.0239 | 1.0096 | 1.0556 |
| **`z = log(e / entry_anchor)`** | **0.0720** | **0.9154** | **0.9380** |

> **AMENDMENT NOTE (conformance repair 5219329372).** The parenthesis "**(the cross-section's
> axis)**" on the `pr` row is **STRUCK — it was false.** The cross-section of record terciled on the
> **season scoring average in the evaluation year**, not on `bestlvl/par`. On that true axis, and
> under the registered estimand, every one of the cross-section's named cells reproduces to the
> third decimal, including the owner's "already priced in" cell: **picks 1-10 × top-tercile = 1.0039,
> dead par, exactly as filed.** The R² figures in the table above were taken under the superseded
> rolling estimand and are left as they were measured. Re-run under the registered estimand with the
> true axis added as a candidate (`AXIS_PROBE.txt`), the ordering is unchanged: `rerate`/`z` 0.0422 ·
> `sa` 0.0273 · `pr` 0.0174. The design choice therefore stands on its own measurement even with the
> right comparator present — which is why it is not re-opened here.
>
> **What is NOT struck: the choice of `z` for the surface's demonstrated-level shape gate.** That
> choice was made by measurement and it is not one of the two registered deviations. Re-opening it
> after seeing which rungs the gates strike would be exactly the tuning the strike law exists to
> prevent. What changed is which axis the **gate** is read on — the registered one — and that is now
> the binding reading in `FRONTIER.txt` §2, with `z` and `pr` printed beside it as disclosed
> secondaries. All three axes agree on the verdict, so nothing turned on the seat's preference.

`z` — how far the engine has *already re-rated* this player off his entry price — separates the
residual three times better on the probe as run. It is a pure state function of the record (it reads
the pre-correction production leg, never the corrected price), so it opens no feedback channel.

~~**The cost of that choice is stated in `FRONTIER.txt` §2**: on the `pr` reading the same cell is
*not* at par on this instrument, so the two readings disagree about which rungs the zero-cell gate
strikes.~~ **STRUCK.** The disagreement was an artefact of testing the wrong cell. On the registered
axis the cell is at par and the gate binds cleanly; the three readings now agree on every rung.

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

~~`Z = 0.715015`~~ → **`Z = 0.772923` under the registered estimand.** **|Z−1| = 0.227 IS the
double-count**: the marginal product multiplies factors that are correlated in the data (deep-ish
picks tend also to carry low `z` and few games). The aggregate is protected by `Z`; the **corner is
not** — the surface can produce ~~+162%~~ **+183%** at (nonKPP, pick 25, 6 games, z = −0.6) and
realises ~~+67%~~ **+85.9%** on the current board at rung 1.0. `FRONTIER.txt` §5. The method
fix is orthogonalised rather than marginal shape estimation. That is a re-teach, not a tune, and
this seat did not take it: it is a third structural change to the estimator inside one act, and
making it *after* seeing which rungs the gates strike is exactly the shape of tuning.

## 4 · The fade: measured, and faster than the owner's shape

> **AMENDED by the conformance repair.** The figures in this section were measured on the superseded
> rolling estimand. Under the REGISTERED estimand the raw residual pooled over the continuous clock
> is **+0.1796 / +0.0306 / −0.0134**, normalised **1.0 / +0.170 / −0.075**, and the installed fade
> after the isotonic clamp is **[1, 0.170, 0, 0]**. The correction at the year-2 clock is 17% of
> full rather than zero. The *shape* finding is unchanged — the premium extinguishes on its own, and
> faster than the owner's "phase out over seasons 2/3" — but see **section 10.4**: the registered
> statistic's horizon is non-stationary, so this fade is the SLOW reading and a stationary one would
> be steeper. The self-extinguishing conclusion survives a fortiori.

~~Pooling the year-1/2/3 evaluation rows over the continuous clock (Addendum 1 F7) the raw residual is
**+0.1284 / −0.0447 / −0.1690**. Normalised to year 1 that is **1.0 / −0.348 / −1.316**: by the
year-2 evaluation the leg is not at par, it is *below* it.~~

~~Installed, after the isotonic non-increasing clamp to [0,1]: **[1, 0, 0, 0]**~~ — the installed
fade is linear in the continuous clock from full at τ=1, so the hand-over to arriving evidence is
round by round with no rollover step (probe (d): the observed max step equals the surface's own max
slope exactly).

**The clamp is declared and it is a decision.** The measured year-2 value is negative; installing it
would put a class markdown on a bonus dial, which is precisely the thing Addendum 1 F11 forbids for
KPD. The unclamped measurement is printed beside the installed one everywhere it appears. The honest
sentence is that the data extinguishes the premium **faster** than the owner's "phase out over
seasons 2/3" — the phase-out is not a shape imposed on the data, and the data wanted an even shorter
one.

## 5 · The KPD sub-dial

Young established KPDs measure **F′ = 0.668** under the registered estimand (~~0.748~~ on the
superseded one) — over-priced, and the cross-section of record filed **0.67**, which the registered
statistic now reproduces exactly; it is below par at all three evaluation seasons. The owner's words described a **bonus**. So KPD rows are excluded from
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

**(a) Fixed.** (The κ figure below is the superseded estimand's; under the registered estimand the
minimal shrink is **κ = 0.912673** for a margin of **+0.023790** — less shrink, thinner margin.)
The monotonicity law originally ran *before* the conservation normaliser. The
normaliser divides the base by Z < 1 — i.e. scales it **up** — and re-broke the margin the law had
just secured (the probe suite measured −0.370 where the teach had printed +0.058). The two are
coupled and are now solved **jointly**, iterating the declared L-SMOOTH shrink κ against a
recomputed Z until both hold. Found by an independent probe, not by reading the code.

**(b) Disclosed, not fixed, and now larger.** The pick-taper endpoint sweep that fixed the declared
endpoints 34 → 48 was read under the same pre-normalisation ordering. Post-normalisation the picks
41-64 band moves ~~+0.516pp at rung 1.0~~ **+0.708pp at rung 1.0 and +0.531pp at rung 0.75** under
the registered estimand, against its 0.5pp bound; it is met at rungs 0.25 and 0.5 (0.177 / 0.354pp).
The endpoints were **again not** re-picked: re-picking a declared boundary once you can see which
rung it strikes is tuning, and both affected rungs are struck on independent grounds anyway.

## 8 · ~~The measurement discrepancy against the cross-section of record~~ — CLOSED

~~The populations reproduce exactly (414 / 684 / 818 against 414 / 684 / 819) but the levels do not:
this build reads **1.0963 / 0.9344 / 0.8205** where the cross-section reported **1.136 / 1.004 /
0.973**. The seat could not reconcile the cross-section's figures from its published method. The
surface is taught from **this build's own committed rows** and the conservation check is run against
**this build's own aggregate** — so the number the shipped surface conserves is 1.0963, not the
directive's 1.136.~~

**STRUCK — the discrepancy is closed and the cause was in this build, not in the record.** The
cross-section discounted to a **fixed career-year-4 point** at the 1.0939 hurdle (the engine's own
no-arb identity); this build substituted a rolling 4-year mean. Re-run on the same frozen matrix,
the registered statistic gives **1.1363 / 1.0041 / 0.9733** — the record to the third decimal — and
the evaluation-year-4 row reads exactly **1.0000**, which is the identity that proves the convention.
The surface has been re-taught and now conserves **1.1363**. `FRONTIER.txt` §7 and section 10 below.

## 9 · What this act deliberately does not do

* **No rung recommendation.** Four symmetric candidates; two struck by registered gates with the
  exact figure that struck them; the ruling is the owner's.
* **No relaxation of a gate to reach the owner's range.** ~~The feasible half of the ladder lands
  0.006-0.021 above par~~ — after the repair **only rung 0.25 survives**, landing 1.0111 on the
  teaching window, and the honest CEILING at any intensity is **1.0248** (rung 0.4193). Both are
  SHORT of [1.04, 1.13]. ~~Three roads~~ **Two roads** out are named in `FRONTIER.txt` §4 and both
  are the owner's; road (a) is withdrawn, the zero-cell bound being vindicated.
* **No new rung values.** The ladder stays 0.25 / 0.5 / 0.75 / 1.0 of the registered residual and
  the infeasible ones are struck. Re-cutting the ladder to sit on the measured frontier (0.4193)
  would be inventing a rung to dodge a strike.
* **No registry write.** Registering an un-adopted board poisons the column id against correction.
* **No store write, no ladder move, no numéraire move, no surface refit, no main merge, no tag.**
* **No cap on an individual lift**, because no registered gate carries one — the realised maximum
  (+85.9% at rung 1.0 after the repair; +67% before it) is filed as a finding instead.

---

## 10 · THE CONFORMANCE REPAIR — what was wrong, what changed, and why this is not tuning

Filed under issue #334 comment **5219329372**, on a reconciliation this build's own `FRONTIER.txt`
§7 asked for. **Two registered conventions were mis-implemented. Both are corrected. Nothing else
about the act moved.**

### 10.1 · What was wrong

**(1) The estimand.** Directive v1 and Addendum 1 registered the estimand as *the value-weighted
aggregate F′ on the year-1 established leg, measured as the cross-section of record measured it* —
**1.136**. The record measured it through the engine's own **no-arb identity**: F = v(**career year
4**) discounted back to the evaluation year at the **1.0939** hurdle, the exact rate for which
1.0939⁴ = 1.432 = the shipped year-4 band. This build substituted a **rolling 4-year mean**,
`mean_k[v(Y+k)/1.0939^k]`, which has no no-arb reading, measured **1.0963**, and taught the surface
to conserve that — **72.2% of the registered residual**. The build then reported the gap as an
unreconciled discrepancy in the record rather than as its own substitution.

**(2) The performance axis.** The cross-section's performance terciles are on the **season scoring
average in the evaluation year**. This build assumed they were on `pr = bestlvl/par`, tested the
"already priced in" cell on that axis, found it *not* at par (+5.6%), and filed a note that the
zero-cell bound might therefore be bounding a real signal — the note that became road (a) in
`FRONTIER.txt` §4. On the true axis that cell reads **+0.39% — dead par, exactly as the record
filed it.**

### 10.2 · What changed

`measure_g6.py` computes the registered F (the superseded rolling statistic is retained as `F_roll`
and printed beside it, never taught from) and carries `sa`, the registered performance axis, read
off the frozen matrix records' own `seasons` rows. `teach_g6.py` therefore teaches to the registered
residual, and the zero-cell gate populations in `teach_g6.py` and `probes_g6.py` are terciled on
`sa`, with `z` and `pr` printed as disclosed secondaries. `g6_table.json` is re-taught (md5
`5656dd8b` → **`61450f0b`**). All four rung boards and all four rung matrices are re-emitted. Every
registered gate is re-run at every rung. `FRONTIER.txt` §2, §4 road (a) and §7 are amended.

**Verification the repair is right, not merely different:** the registered statistic reproduces the
record at all three evaluation years (1.1363 / 1.0041 / 0.9733 vs 1.136 / 1.004 / 0.973), reads
exactly **1.0000** at evaluation year 4 (the no-arb identity), and on the `sa` axis reproduces every
one of the cross-section's ten named cells to the third decimal — picks 21-40 1.3921 (1.38), KPF
1.5038 (1.50), MID 1.2665 (1.27), KPD 0.6680 (0.67), picks 41-64 0.9678 (0.97), draft age 21+
0.8167 (0.82), mid-tercile 1.3493 (1.35), early×below-median 1.2866 (1.28), early×above-median
1.0350 (1.04), picks 1-10×top-tercile 1.0039 (1.004). Reproducing ten independent cells from a
convention change is not a coincidence.

### 10.3 · Why this is conformance and not tuning

Three tests, all of which this repair passes:

1. **It restores a PRE-REGISTERED quantity, it does not choose a new one.** 1.136 is written into
   Addendum 1 as the named estimand. The season-average axis is the axis the cross-section it cites
   was measured on. Neither was invented here.
2. **It moves the act AWAY from the seat's convenience, not toward it.** The repair makes the gates
   **stricter**: rung 0.5 was feasible and is now **struck**, the picks 41-64 taper bound now also
   strikes rung 0.75, and the honesty line worsens at every rung (the median F′ falls from 0.8672 to
   0.7173 at rung 1.0 against 0.9632 → 0.8331 before). A tuning pass does not shrink its own
   feasible set from two rungs to one.
3. **It withdraws the seat's own escape route.** Road (a) — the challenge to the zero-cell bound —
   was the one road out of the frontier that this build had authored. The repair **kills it**: the
   bound is vindicated, the at-par cell is at par, and the owner no longer has that ruling to make.

Nothing that was not one of the two named deviations was touched: the site fence, the two-axis
kernel, the declared tapers and their endpoints (**not** re-picked, again), the L-SMOOTH and
conservation solve, the KPD sub-dial, the dial semantics, the shipped default of 0 and the seat's
silence on the rung all stand exactly as built.

### 10.4 · The non-stationarity caveat, filed

The record's fade quote **1.136 → 1.004 → 0.973** is **horizon-non-stationary**: every term discounts
to the *same* fixed career year 4, so the horizon shortens from three years to one across the
sequence. A stationary-horizon fade is **steeper** than that line reads. The direction is the safe
one — the finding that the development premium is **self-extinguishing survives *a fortiori***.

Where it bites is the taught `Stau`. Measured over the registered (non-stationary) statistic the
fade installs **[1, 0.170, 0, 0]**, where the superseded statistic installed [1, 0, 0, 0]: the
correction at the year-2 clock is 17% of full rather than zero. That is the **slower** of the two
readings, and a stationary measurement would extinguish it faster. The shipped fade is therefore
conservative in the direction of paying the premium *longer*, and that conservatism is a
consequence of the registered convention, not a measurement of the world. Named here so no reader
mistakes it for one.

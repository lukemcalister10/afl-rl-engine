# ITEM 279 — STEP 1 EVIDENCE: the SCAR/VOR dual endpoint derivation

**Scope pin.** Derived at commit `f1557b2` (main tip; one commit past the adoption commit `f60af6c`).
Store `6b9d00a7` · rl_model `7349a1e4` · engine head `404e8113` · fv `d10aa93e` — all Guard-5 asserted at
bootstrap. Adopted SCAR board `f2df6e0a`, adopted surface `ce08c2d1` (frozen pair `b781ed25`/`d071e743`).

**What this step answers, and what it does not.** It is the currency evidence only: the two γ endpoints,
each with its own surface bake, side by side. It rules nothing. The pick-value basis (S-1/S-2), the α dial
(S-3/S-4) and propagation are later steps; α is parked at 1.0 throughout, and both columns are built on the
current basis, so they carry the same known tail warts and the comparison is like-for-like.

## Reproduction conditions

Detached scratch worktree at `f1557b2`, `env -i`, `PYTHONHASHSEED=0`, single-thread BLAS
(`OPENBLAS/OMP/MKL/NUMEXPR/VECLIB_NUM_THREADS=1`), pinned venv (Python 3.12.3 · numpy 2.4.4 ·
scipy 1.17.1 · scikit-learn 1.8.0 · openpyxl 3.1.5), numpy's bundled OpenBLAS hash-checked to the pin
(`05c9f9eb…`) by bootstrap's own gate. Nothing in the scratch worktree was committed. The boards were built
with `RL_V0SURF_REFIT=1`, which is on the release contract's must-unset list — so both derivation boards are
**unbakeable by construction** and cannot be mistaken for shippable states.

Measured cost, first-time path: bootstrap <1s · surface refit ~50s · board build + export 82–91s. One
endpoint derivation is about 90 seconds.

## The four boards

| board | γ | surface | identity | what it is |
|---|---|---|---|---|
| SCAR, frozen load | 0.85 | loaded (adopted) | `f2df6e0a` | reproduces the adopted board exactly |
| SCAR, forced own bake | 0.85 | own refit | `f2df6e0a` | identical to the above — the method adds no artifact |
| **VOR, own surface bake** | **1.0** | **own refit** | **`c8515acd`** | **the proper VOR endpoint (A10's prerequisite met)** |
| VOR, loaded SCAR surface | 1.0 | loaded (SCAR) | `48e782b8` | the mixed-denomination artifact |

The SCAR column is not duplicated into this directory: it is byte-identical to the shipped
`data/rl_build/rl_app_data.json`, and a second copy would be a duplicated assertion that can go stale.
The VOR own-surface board is committed here as `out/board_VOR_gamma1_ownsurface.json` (`c8515acd`), the
counterpart to `#271`'s committed mixed-denomination `board_VOR_gamma1.json`.

## Findings

**1. The surface signature is γ-blind, so the frozen-signature halt can never fire at γ=1.0.** Measured: the
config signature is byte-identical in both columns (`b781ed25`/`d071e743`), while the refit's surface content
moves (`ce08c2d1` → `8990fed6`). Mechanism, confirmed at source: the curve the signature hashes is a loaded
file input (`_L1CURVE` from `pvc_curve_L1b.json`), the roster is γ-invariant, and the gate dict
(`_merged_recover.py:1279`, **37 keys**) contains neither `RL_GAMMA` nor `RL_PICK1`. Consequence: a normal
γ=1.0 build silently prices VOR players on the SCAR surface, with no halt and no warning. The VOR surface
refit must therefore be forced explicitly in the declared lane. This is the latent hole ruling-sheet item 4
closes by adding `RL_GAMMA` to the gates.

**2. Forcing the own bake is not itself an artifact.** At γ=0.85 the forced-refit board equals the
frozen-load board exactly (`f2df6e0a` both). So building both columns with a forced own bake is symmetric,
and the side-by-side is fair.

**3. The own surface bake is not cosmetic — it changes the board.** Same store, same engine, same γ=1.0,
surface the only variable: `c8515acd` (own) vs `48e782b8` (loaded SCAR surface). 177 of 804 active players
change value (22.01%), max absolute change 77 points, and 1,333 of 322,434 strictly-ordered pairs invert
between them. The no-refit VOR board reproduces `#271`'s committed companion `48e782b8` **byte-exactly**,
which confirms by reproduction — not by reading — that the companion is the mixed-denomination artifact
Addendum 10 described.

**4. The instrument reproduces the sealed A13 figure to the digit.** SCAR against the mixed-denomination
companion gives **7,496 of 322,531 strictly-ordered pairs = 2.3241%**, matching the sealed canonical figure
(7,496 / 322,531 = 2.32%). Against the *proper* VOR endpoint the same metric gives **6,370 of 322,531 =
1.975%**. So the mixed-denomination companion overstated the rank leak by 1,126 pairs; the honest dual-derived
figure is 1.98%, not 2.32%. Denominator in both cases is strictly-ordered pairs (322,531 of 322,806 total;
275 pairs tie under SCAR), the order-independent metric per Addendum 13's instrument note — adjacent-pair
counts are tie-sensitive and are not used.

**5. [PARTLY SUPERSEDED — see the ADDENDUM at the end of this file.]** The two consequences drawn below
were reasoned from a *frozen* pick ladder held against a *moving* player side. That is not a like-for-like
currency comparison. The retrospective pick curve has since been re-derived under both endpoints; the
addendum carries the corrected picture and **reverses the sign** of the "picks get dearer" consequence. What
stands from this finding: the *shipped* ladder is indeed γ-invariant, and the conclusion that γ does not
meaningfully fix the tail also stands, but for a better-supported reason given in the addendum.

**5. The shipped pick ladder does not move with γ at all.** Byte-identical in both columns, all 65 points
(`[3000, 2767, 2693, … 571]`, pool 299), because the board ships the frozen adopted curve via the L7 repoint
(`pvc_curve_v2.json`) and γ cannot reach it. Two consequences that matter for the ruling:

- The γ choice reprices **players only**, against an unchanged pick ladder. Picks therefore become dearer
  *as a class* under VOR: the pick share of total board value rises 8.1012% → 8.3876% while the player pool
  falls 3.71% (players 747,840 → 720,060 at the +1 lens; ladder frozen at 65,925). That is a real relative
  price change between players and picks, arriving from the currency choice itself rather than from the α
  dial, and it is the same effect ruling-sheet item 3 flags for the dial.
- Because the ladder is frozen and γ-independent, the `#270` tail finding (picks 57–64 priced ~1.56× realised)
  is **identical under both currencies**. The γ ruling and the tail overpricing are orthogonal: γ cannot fix
  the tail, and the tail does not bear on the γ choice. The tail is step 2/3's work.

The γ-responsive pick quantity — the model's own `val(pick_raw(k))`, before the frozen-ladder repoint — is
reported in `out/curves_picks_279.csv`. Pick *production* is γ-invariant (identical raw in both columns, as
expected, since γ only converts production to value); pick *value* falls under VOR and falls much harder at
the tail: ratio 0.905 at picks 1–3 against 0.463 at picks 50–64. Note this quantity is band-resolved (8
bands), so picks inside a band share a value — it is a coarse instrument and is reported as one.

**6. VOR steepens the board; SCAR compresses it.** Deciles by SCAR rank, VOR/SCAR value ratio: the top decile
**rises** (1.0627) and every decile below falls monotonically to 0.74–0.75 at the bottom. Top player 10,079 →
12,154. Total active player value falls 3.51% (802,390 → 774,236 across 804 matched rows; median 472.5 → 395.0).
Plainly: γ=1.0 pays more for the best players and much less for everyone else; γ=0.85 props up the lower
two-thirds. That is the whole substance of the choice.

Both columns held the numéraire (pick-1 = 3000) and passed the parity gate on all 804 active rows, so the two
boards are in the same units and the comparison means something.

## Files

- `out/derived_279_step1.json` — every measurement in this document, with denominators.
- `out/curves_players_279.csv` — 804 active players, SCAR and VOR value side by side, both ranks, rank delta,
  and the mixed-denomination value for reference. Matched **by key**, never by name substring.
- `out/curves_picks_279.csv` — shipped ladder in both columns (identical), plus the γ-responsive model pick
  value and its ratio, picks 1–64 and the pool.
- `out/nonvacuity_279.json` — each check with its can-fail proof.
- `out/board_VOR_gamma1_ownsurface.json` — the proper VOR endpoint board, `c8515acd`.
- `scripts/` — the probes and the analysis, as run.

## Non-vacuity

Every check here is proven able to fail, recorded in `out/nonvacuity_279.json`: the all-pairs rank metric
returns 0 on identical input and 803 inversions on a single deliberate swap; the ladder-equality check can
report false; the board-reproduction check is live because the VOR board differs from the pin while the SCAR
board matches it; the surface-reproduction check is live for the same reason at `8990fed6` vs `ce08c2d1`; the
player intersection is asserted non-empty (804 of 804 both sides, zero unmatched either way).

## Counts and their denominators

804 active rows on both boards, 804 matched, 0 unmatched either side, of 1,002 exported rows (804 active +
198 back) and 2,651 store rows. 322,531 strictly-ordered pairs of 322,806 total pairs. 177 of 804 players
moved by the surface bake. 37 gate keys in the v0surf signature, 0 of them γ.

## CI posture

No CI was run for this step and nothing in it touches CI. Posture is inherited from the record at `f60af6c`:
guards green with G-Y0 held at 3.035% under the 3.500% ceiling, FV Provenance green, and the one declared
known-red — `movers.test.js` at exactly 2 of 58, the pinned pair, in both Final Integration and Live Scoring.
A third failure in that file would be new.

## Docketed forward, not fixed here

The peak-model builder (`engine/forward_valuation/build_peak_model_v4.py:8`) hard-assigns `RL_GAMMA='0.85'`.
It is inert for this step: the peak model is a committed pinned frozen pickle (`peak_model b763f59e`), loaded
and never fitted, its serve path is γ-free (`GAMMA` appears only at `rl_model.py:504,731,734`), and the
builder cannot run from the tree at all — its `dob_corrected.json` input is absent repo-wide, while
`bust_prior_table.json` is committed. It becomes a live trap only if a later step deliberately retrains the
peak model, which would need that missing input located first. Seam has docketed the retrain gap.

---

# ADDENDUM — the retrospective pick curve re-derived under both endpoints

Added after the first seal, on seam direction: step 1's pick-side evidence was incomplete because the
shipped ladder is frozen, so the original players-vs-picks comparison held a fixed pick side against a
moving player side. Both sides now move in the same currency. This addendum supersedes finding 5's two
consequences; everything else in this file stands.

## Method, and what is held constant

The retrospective curve is re-derived with `#271`'s derivation carried **verbatim** — `pava_ni` /
`build_points` / `fit_year0` / `monotone_strict`, τ=0.12, nmin=35, `PW_FLOOR`=0.11, pin(1)=3000, the ×0.6
blend ceiling, the min(n_pos/200,1) pooling weight, both windows (pool 2004–2024, priors 2006–2020). The
prior *recipe* is untouched in both columns — the prior fix is step 2's work — so the two curves differ by γ
alone. Each column is self-consistent in its prior source: the SCAR column reads the adopted surface
(`v0surf_frozen: true`), the VOR column reads its own bake (`v0surf_frozen: false`, content `8990fed6`). No
mixing.

My script copies differ from `#271`'s originals by **three non-numerical lines** — output directory, output
filename, and the statistic label now following `RL_GAMMA` rather than asserting `SCAR` unconditionally.
Faithfulness proof: my copy reproduces Control A's payload exactly. The label edit is load-bearing — run
unmodified, the VOR column's own metadata would have claimed `statistic: SCAR`.

Measured cost, first-time path: evidence-matrix emit **198s (SCAR) / 202s (VOR)**; the fit itself **3s**.
All eight both-directions checks PASS in both columns, 0 FAIL.

## Controls — one passes, one cannot, and the difference is the finding

| control | payload | verdict |
|---|---|---|
| Control A: `#271`'s committed matrix through its committed fit code | `08ea9375` | **reproduces the adopted curve exactly** — ladder 65,925, pool 299.3, 0 of 64 points differ |
| SCAR re-derived on today's adopted store + adopted surface | `ec9192a2` | **does not reproduce** — ladder 67,401 (+2.24%), 63 of 64 points differ, pool 297.2 |
| VOR re-derived on today's store + own bake | `85576b0f` | differs from SCAR, as it must |

Only pick 1 matches in the SCAR row, because it is pinned at 3000.

**The adopted shipped ladder is not reproducible from the store it ships with.** `pvc_curve_v2.json`'s own
`derived_from` names store `265f55d5`; the adopted store is `6b9d00a7`. Attribution, by diffing the two
matrices directly: the population is **identical** (2,646 records, 1,444 curve-teaching, zero keys added or
removed) and the evidence weights are **byte-identical** (0 of 2,646 `pw` dicts differ), so neither the
method nor the games data moved. The entire difference is in values — `v0` changed on 1,565 records (median
+12.4) and the walk-forward value path on 2,528 of 13,592 cells. That is the adoption's own effect on the
prior surface and the value path. It is **not** the γ question: both γ columns sit on the same store, so the
comparison below is clean. It does bear on step 4's propagation and the G-Y0 re-derivation, and it is
reported here rather than fixed.

## Both curves, side by side

Full 64 points plus the pool in `out/curves_picks_279.csv`. By band, VOR as a ratio of SCAR:

| band | 1-3 | 4-7 | 8-12 | 13-20 | 21-27 | 28-35 | 36-48 | 49-64 |
|---|---|---|---|---|---|---|---|---|
| VOR/SCAR | 1.007 | 0.991 | 0.967 | 0.946 | 0.936 | 0.922 | 0.912 | 0.902 |

Ladder total 67,401 → 63,908 (−5.18%). Pool level 297.2 → 273.7 (−7.91%), on 1,093 pool rows of which 624
never established, identical in both columns. Steepness pick1/pick64: 5.128 (SCAR) → 5.703 (VOR), +11%.

**VOR steepens the pick curve in the same direction it steepens the player board.** The top of the draft
holds its value; everything from pick 8 down loses, worst at the tail.

## Corrected players-vs-picks, both sides in the same currency

| | players | picks (re-derived ladder 1–64) | total | picks share |
|---|---|---|---|---|
| SCAR | 802,390 | 67,401 | 869,791 | 7.7491% |
| VOR | 774,236 | 63,908 | 838,144 | 7.6249% |

Players −3.51%, picks −5.18%, share **−0.124 points**.

**The earlier "picks get dearer as a class under VOR" consequence is withdrawn, and its sign was wrong.**
Picks get slightly *cheaper* as a class under VOR, because the pick side falls further than the player side
once both are allowed to move. The superseded figure (8.1012% → 8.3876%) was an artifact of holding the
frozen ladder against a moving player side.

## The tail, measured against a moving denominator

| | curve mean, picks 55–64 | own realised | ratio |
|---|---|---|---|
| SCAR | 591.3 | 362.2 | 1.633× |
| VOR | 532.4 | 332.1 | 1.603× |

Band n=194. The realised side falls 8.31% while the curve tail falls ~10%, so the overpricing ratio moves
only **−1.80%**. **γ does not meaningfully fix the tail** — this was the original conclusion and it survives
the correction, now on the proper basis: γ moves the curve and its evidence denominator nearly together.
The tail remains step 2 and step 3's work.

## Age-gradient decomposition

At fixed current value, the γ-flip ratio by age band (`out/age_gradient_279.json`):

| age | ≤21 | 22–24 | 25–27 | 28–30 | 31+ |
|---|---|---|---|---|---|
| VOR/SCAR | 0.939 | 0.865 | 0.799 | 0.766 | 0.778 |

Denominator 804 of 804 active rows, zero excluded. "Fixed value" is 20 equal-count SCAR-value bins; the
gradient is stable at 5, 20 and 40 bins (first cut used quintiles wide enough for the ratio to track value
inside a bin — the finding survived tightening). It also survives removing value entirely via a quadratic fit
in log(value): residual correlation with age −0.36, mean residual monotone +0.050 → −0.071 across the bands.
So it is a genuine career-stage effect, not value composition.

Mechanism, visible in the same numbers: the ratio is *not* a pure function of production
(corr(log value, ratio) = 0.71; residual sd 0.108 against total sd 0.156), because value also flows through
the γ-refit v0 surface. Young players lean on that prior, older players on realised production, so the
currency choice reprices career stages differently rather than rescaling uniformly.

## Files added by this addendum

- `out/curves_compare_279.json` — both curves, controls, band table, corrected share, tail ratios, store-drift attribution.
- `out/curves_picks_279.csv` — rewritten: adopted / re-derived SCAR / re-derived VOR per pick, plus the pool.
- `out/derived_279_scar.json`, `out/derived_279_vor.json` — the two derivations as emitted.
- `out/per_entrant_279_scar.json`, `out/per_entrant_279_vor.json` — the evidence matrices behind them.
- `out/age_gradient_279.json` — the age panel with its robustness and can-fail proofs.
- `scripts/emit_matrix_279.py`, `scripts/derive_279.py` — the carried copies; `scripts/compare_curves.py`, `scripts/age_gradient.py`.

## Non-vacuity for this addendum

The curve-equality check demonstrably reports both outcomes: Control A matches the adopted payload, the
SCAR-on-current-store re-derivation does not. The age-gradient metric returns a flat gradient on a flat
synthetic input and a non-flat one on the real input. The both-directions population checks pass 8/8 with 0
FAIL in each column, and their published rule ("no POOL row among the keys the ND fit consumed", and the
converse) is the same instrument that would name violators if any existed.

One cosmetic wart, disclosed: `emit_matrix_279.py` prints `wrote out/per_entrant_271.json` regardless of the
actual output path, because that filename is a literal inside its print statement. The real writes went to
the parameterised paths — confirmed by the worktree staying clean and by the matrices' own `meta` stamps.

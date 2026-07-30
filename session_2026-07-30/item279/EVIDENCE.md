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

---

# SECOND ADDENDUM — ESTIMATE: the VOR adoption echo on player values

**This is an ESTIMATE and bounds one thing only: the pure-currency echo.** It answers "if VOR were fully
adopted and its pick curve flowed back through the system, how far would player values move from the board
already presented (`c8515acd`)?" It is **not** a prediction of the final board — the shipped system still
changes at step 2 (pick-value basis, S-1/S-2) and step 3 (the variance dial). Nothing here rules anything.

## The channel map — every path from the adopted pick curve to player values

| # | channel | code path | full adoption re-points it? |
|---|---|---|---|
| 1 | curve → ev-channel basis | `pvc_curve_v2.json` → `_V2CURVE` → `_PVC0` (`_merged_recover:1612-1619`) | **YES** |
| 1a | → RUCK prior cap / scaffold | `_PVC0` → `draftval(p)` (`:1578`) → `_ruc_prior_cap` | **YES** |
| 1b | → V0 guard + V0 surface rebuild | `_build_v0_guard()`, `_build_v0_curve()` (`:1620-1621`) | **YES** |
| 2 | curve → module PVC | `_V2RAW` → `_PVC2M` → `rl_model.PVC` (`rl_model:929-945`) | **YES** |
| 2a | → pickless unplayed equivalent | `_PVC2M` → `unpl_eq` (`rl_model:1007`) | **YES** |
| 2b | → pedigree pedestal | `_PVC2M` → `pedestal` (`rl_model:1022`) | **YES** |
| 3 | curve → v0 → surface → value | `_v0_uncapped` = `raw_ev(...)` reads 2a/2b; the surface is fit over `_v0_raw`; `v0_start` feeds values | **YES — the feedback loop the convergence pass exists for** |
| 4 | peak-model TRAIN-TIME PVC feature | `pvc_snapshot.json` → `_V4PVC` (`rl_model:657`), entering `_v4_feats` as `np.log(_V4PVC[ep])` | **NO — frozen by its own design note; re-pointing it is train/serve skew** |
| 5 | the peak model itself | `peak_model_v4.pkl`, pinned `b763f59e` | **NO** — serve path γ-free (`GAMMA` only at `rl_model.py:504,731,734`); builder unrunnable, `dob_corrected.json` absent repo-wide. Retrain gap docketed by the seam |
| 6 | frozen ceiling / cm models | `q97m.pkl`, `cm_400.pkl` | **NO** — frozen by owner ruling, loaded never fitted |
| 7 | bust prior | `bust_prior_table.json` → `_v4_bp` | **NO — not a curve channel at all**: values are production-score units by position × pick (33.51–98.13), derived from realised outcomes |
| 8 | superseded L1b artifact | `pvc_curve_L1b.json` → `_L1CURVE` → `_PVC0` (`:1585-1598`) | **AMBIGUOUS — both branches measured, see below** |

The convergence pass re-points channels 1–3 and only those. Channel 4's exclusion is not a judgement call: the
design note at `rl_model.py:657` states that feeding the live post-bake PVC there is train/serve skew, because
`build_peak_model_v4.py` trained the pickle on the snapshot. Channels 5–7 do not carry the curve at all.

**Channel 8 is the ambiguous one and is measured, not assumed.** That block loads the superseded L1b artifact
into `_PVC0` and *does* rebuild the V0 guard and surface — but the v2 block runs after it and overwrites
`_PVC0`, so under `RL_PVC2=1` (the default) it should be inert. Both branches were built: v2 only, and v2+L1b
together. Result below.

**One stale comment found on the way, reported not fixed.** `_merged_recover.py:1573` describes `draftval` as
"FROZEN on the pre-fit v3.4 curve (`_PVC0`)". It is not: `draftval` closes over the `_PVC0` dict, and both the
L1b and v2 blocks mutate that dict in place, so `draftval` tracks the adopted curve. Behaviour is correct —
the RUCK scaffold *should* follow the adopted currency — but the comment would mislead a reader, and it is the
single largest live channel in the measurement below.

## The convergence pass

Each iteration: install the curve into the adopted artifact (the one disclosed pin edit) → reseed → refit the
surface at γ=1.0 (`RL_V0SURF_REFIT=1`) → rebuild the board → re-derive the curve from the new surface. Cost per
iteration: board 126–140s, matrix emit 175–188s, fit 3s.

| step | players moved (of 804) | max abs delta | total value |
|---|---|---|---|
| baseline → it1 | 21 | 28 | −0.052% |
| it1 → it2 | 18 | 2 | −0.003% |
| it2 → it3 | **0** | **0** | 0.000% |

Board identities `c8515acd` → `32ec020a` → `aa798cb1` → `7977d7e5`. The last two carry **identical player
values** and differ only in embedded curve metadata. The curve reached a **fixed point**: payload `817c0f5a`
went in at iteration 3 and came back out as `817c0f5a`, ladder 63,815 → 63,815, pool 273.4 → 273.4. Ladder
sequence 63,908 → 63,818 → 63,815 → 63,815. Surface signature moved every time the curve did
(`b781ed25` → `2b633636` → `76c1e469` → `22f4f961`), which is worth noting against finding 1 of the first seal:
the 37-gate signature is **not** insensitive in general — it hashes the curve and catches a curve change. It is
blind to γ *specifically*, because γ enters only at `rl_model.py:504/731/734` and never touches the hashed
payload.

## The echo, converged, against `c8515acd`

- **21 of 804 active players move** (2.61%); 783 do not move at all
- median absolute delta of movers **22**, max **29** (Alex Van Wyk); median signed delta across all 804 is **0**
- every mover moves **down**
- total active value 774,236 → 773,810, **−0.055%**
- rank movement **245 of 322,434 strictly-ordered pairs = 0.076%**, 6 tie-collapses, max rank shift 27 places
- **top 20 unchanged in both membership and order**
- age profile essentially static: ≤21 shifts −0.0034, 22–24 −0.0018, 25–27 −0.0003, 28–30 **0.0000**, 31+ −0.0003

**Every one of the 21 movers has settled position (`gfut`) RUCK.** By position among the 111 zero-game actives:
RUCK 13 of 14 moved; KPD 0 of 13, KPF 0 of 12, MID 0 of 22, SD 0 of 20, SF 0 of 30. Among the 693 played
actives, 8 moved, all RUCK. Two movers are *listed* KPF but carry `gfut == RUCK`, which is the key the RUCK
branch actually reads — a reminder that listed position and settled position are different fields.

The largest movers sit at effective pick 65, the pool, because the pool level falls hardest (299 → 273, −8.7%).

## Requirement 1: did channels 2a/2b actually consume the swapped curve?

**Yes — fully wired, proven directly.** Instrumenting the same expressions `value()` uses, under each curve:

| player | ep | `_PVC2M` at ep | `unpl_eq` | `value()` | `ev(2026)` | `v0_start` |
|---|---|---|---|---|---|---|
| adam-sweid | 25 | 906 → 865 | 788.4 → 752.7 | 788 → 753 | 571 → 571 | 765.39 → 765.39 |
| aidan-schubert | 23 | 964 → 927 | 841.1 → 808.8 | 841 → 809 | 671 → 671 | 893.14 → 893.14 |
| avery-thomas | 28 | 840 → 795 | 728.7 → 689.6 | 729 → 690 | 472 → 472 | 638.61 → 638.61 |
| will-green (RUCK) | 16 | 1207 → 1165 | 990.5 → 956.0 | 990 → 956 | 698 → **683** | 1165.88 → **1140.28** |
| max-knobel (RUCK) | 42 | 660 → 615 | 397.8 → 370.7 | 398 → 371 | 527 → **509** | 879.92 → **848.97** |

So `unpl_eq` and `value()` move for **every** probed player: 2a/2b are not half-wired.

**But `value()` is not the board price.** Board `v` = `round(ev(p,2026) / 1.0524)` — the L7 numéraire re-base —
verified to the digit on 5 of 5 spot checks (sweid 571→543, green 698→663, knobel 527→501, thomas 472→448,
ludowyke 414→393, each matching its board row). And `ev()` moved only for the RUCK players.

**Mechanism, read out of `ev()` rather than inferred.** A zero-season player returns `round(sitout_ev(p,Y,e))`,
which is V0-anchored — the price comes from `v0_start`, the fitted surface, not from `value()`/`unpl_eq`. And
`ev()` carries an explicit RUCK branch reading `RUC_PRIOR_CAP*draftval(p)` (or `_ruc_ceiling`) and
`_v0_uncapped(p)`, both off the adopted curve; no other position has a curve-reading branch there. That is why
`v0_start` moved for the RUCK players and was *identical* for the non-RUCK ones: the denser non-RUCK surface
(`surfN`) absorbed the curve shift under isotonic pooling, while the thinner RUCK surface (`surfR`) passed it
through.

So the small echo is neither half-wiring nor "domination by 1a". It is: the shipped board prices these rows
through `ev()`, which for them is surface- and RUCK-cap-anchored, and the surface absorbs most of a small curve
move.

## Channel 8 (the ambiguous one): measured INERT on values, but genuinely loaded

Both branches built at the converged curve. Branch A (v2 only) and branch B (v2 + L1b re-pointed) produce
**byte-identical boards** — `7977d7e5` both — with 0 of 804 players differing. The v2 block overwrites `_PVC0`
after the L1b block, so L1b cannot reach player values. Measured, not assumed.

It is **not** inert on load, though, and the proof was accidental: a first attempt that wrote a bare 1–64 curve
into L1b **halted the build** inside `_split_ladder` with "no pool level", because L1b has no `pool_value` field
and carries its pool level as curve entry 65 (its domain is the declared legacy 1–99 exception). A silent
artifact would not have stopped a build. So: loaded and validated at import, inert on values.

## INCIDENT NOTE — two defects of mine in this pass, and the hardening

**Incident 1 — silent path fallback overwrote a committed evidence file.** My iteration wrapper used `env -i`
with an explicit whitelist and did not include `ITEM279_OUT` / `ITEM279_MATRIX_NAME`. The emitter defaulted, and
wrote over the **worktree's** copy of `#271`'s committed `per_entrant_271.json`. Contained to scratch: the main
checkout was verified untouched (`pvc_curve_v2.json` still `6506d8b1`, `per_entrant_271.json` still `2f8b4bd4`),
the worktree was restored with `git checkout`, and nothing was committed. The same stripping would have
defaulted `CURVE_STATISTIC`, letting the VOR column stamp its own metadata `SCAR` — the path fallback and the
label fallback are one defect class, as the seam put it.

**Hardening, and proof it fires.** Both scripts now fail closed, checked *above* the expensive ASOF loop so a
misconfigured run costs a second rather than three minutes:

- no vars → `emit HALT: required output binding absent: ITEM279_OUT, ITEM279_MATRIX_NAME` — 0s
- only `ITEM279_OUT` set → HALT naming just `ITEM279_MATRIX_NAME` — 0s (partial config caught)
- no label → `derive HALT: CURVE_STATISTIC must be set explicitly` — 0s
- **non-vacuity:** iteration 3 ran to completion on the hardened scripts (board `7977d7e5`, matrix 3,241,310
  bytes, fit 8/8 both-directions PASS), so the guards pass when the variables are set

**Incident 2 — two wrong attributions of mine, corrected by measurement.** At iteration 1 I attributed the echo
to channel 1a from board fields alone; that conclusion was right in substance but the reasoning was not, because
board fields cannot distinguish the channels. I then reported that `value()` moving proved 2a/2b carried the
echo; that was also wrong, because `value()` is not the board price path. Only the `ev()` instrumentation
settled it. Both are recorded because the first addendum's method note says measurements decide, and twice in
this pass I stated a mechanism ahead of measuring it.

## Files added by this addendum

- `out/echo_279_estimate.json` — every measurement above, with denominators, plus the channel map verdicts.
- `out/echo_channels_279.json` — the raw probe dumps: `value()`/`unpl_eq` and `ev()`/`v0_start` under both curves.
- `out/board_VOR_converged.json` — the converged board `7977d7e5`.
- `out/derived_279_vor_converged.json` — the converged curve, payload `817c0f5a`, ladder 63,815, pool 273.4.
- `scripts/install_curve.py`, `scripts/iterate.sh` — the convergence lane.
- `scripts/probe_channels.py`, `scripts/probe_ev.py` — the channel instrumentation.
- `scripts/emit_matrix_279.py`, `scripts/derive_279.py` — now carrying the fail-closed guards.

## What this estimate does and does not bound

It bounds the pure-currency echo: with the curve fully flowed back through the lawful channels, the board the
owner has seen moves 21 RUCK players by a median 22 points, leaves the top 20 and the age profile alone, and
does not change the board's shape. It does **not** bound the final board — step 2 changes the pick-value basis
and step 3 adds the variance dial, and either can move far more than this. It also does not cover a peak-model
retrain, which is excluded by design (channel 4) and docketed by the seam (channel 5).

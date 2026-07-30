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

---

# THIRD ADDENDUM — STEP 2: the minimal-vs-structural pick-basis prototype pair (VOR, γ=1.0)

γ ruled VOR by owner word 2026-07-30. Everything here is VOR-denominated. α stays parked at 1.0 — no
variance shaping in either prototype; that is step 3's question. The pool's ruled level lands at
propagation, not here.

**Matrix:** one evidence matrix for both prototypes — `out/per_entrant_279_vor.json`, store `6b9d00a7`,
γ=1.0, own-bake surface (`v0surf_frozen: false`). Own-surface discipline unchanged.

**Cost, measured before building the pair:** each prototype fit is **0.02–0.06s**; the whole pair including
load is **2s wall**. Step 2 needs no engine run, no surface refit and no board rebuild, because both
prototypes consume the matrix that already exists. This is the cheapest step in the job.

**Control:** the harness's baseline path reproduces the step-1 VOR curve payload `85576b0f` exactly, which
proves the harness's fit is the carried-verbatim one and that the only thing changing between runs is the
year-0 contribution.

## The finding that frames the whole step: the shipped curve is 99.975% its own prior

`build_points` gives every entrant one year-0 point carrying `v0` — the **model's** year-0 estimate off the
fitted surface — at weight 1.0, plus its realised path at tenure `k` with weight `es`. `fit_year0` then applies
a time kernel `exp(-ty/τ)` with **τ=0.12**. Measured on the 1,325 curve-teaching rows in window:

| | kernel mass | n points |
|---|---|---|
| prior (ty=0, the model's `v0`) | 1325.000 | 1,325 |
| realised evidence (ty≥1) | 0.329 | 8,764 |

**Realised evidence carries 0.0248% of the mass.** The time-kernel factors are 2.40e−4 at ty=1, 5.78e−8 at
ty=2, 1.39e−11 at ty=3. So the "evidence-weighted" retrospective curve is, in practice, a smoothed re-reading
of the v0 surface — and that surface is fit over `_v0_raw`, which reads the pick curve through
`pedestal`/`unpl_eq`/`draftval`. Curve → surface → v0 → curve, with reality contributing a fortieth of one
percent. That is the owner's S-1 objection, quantified: *"what the model expected of someone like him is
ridiculous to consider when we have the evidence of what he actually did."*

Note the asymmetry, confirmed at source: the **pool level** uses `realised_scar`, which has **no time kernel**
and is pure evidence. So the shipped pick curve's head (1–64) is prior-driven while its pool level is
evidence-driven. They are on different footings, and #270's tail finding — curve ≈1.56× realised at 57–64 — is
exactly what that predicts.

## The two prototypes

Both change only what an entrant contributes as its year-0 point; `fit_year0`, `monotone_strict`, `pava_ni`,
τ, nmin, `PW_FLOOR`, the pin(1)=3000 and both windows are carried verbatim.

- **MINIMAL (S-1, re-weighting inside the current blend).** For a **concluded** career the year-0 slot carries
  what he actually did (evidence-weighted realised value, busts at 0.0) instead of what the model predicted;
  the prior is retired from concluded careers entirely, and their decayed evidence points go with it. Active
  careers are untouched — the prior still stands in for their unwritten share. One point per entrant either
  way, so the bandwidth/`effn` basis is unchanged.
- **STRUCTURAL (S-2, completion over presumption).** Every entrant contributes a completed career value.
  Concluded careers contribute their realised value. Active careers have their unwritten remainder completed
  actuarially from concluded look-alikes, matched on settled position × tenure-so-far, with busts'
  zero-remainders **included** in the stratum. The model prior survives only as an explicit, counted fallback.

Population, of 1,325 curve-teaching rows in the 2004–2024 window: **830 concluded, 495 active, 316 never
established**. Structural provenance: 830 own realised, **424 actuarially completed**, **71 prior fallback**
(thin stratum, min n=20) — so the prior survives on 5.4% of rows, counted, against 100% of the year-0 mass in
the baseline. 66 of 109 strata are usable.

## Both curves, against the VOR baseline

| pick | baseline | minimal | min/base | structural | str/base | str/min |
|---|---|---|---|---|---|---|
| 1 | 3000 | 3000 | 1.000 | 3000 | 1.000 | 1.000 |
| 2 | 2871 | 2773 | 0.966 | 2999 | 1.045 | 1.082 |
| 3 | 2787 | 2434 | 0.873 | 2905 | 1.042 | 1.194 |
| 10 | 1640 | 1464 | 0.893 | 1516 | 0.924 | 1.036 |
| 24 | 895 | 811 | 0.906 | 799 | 0.893 | 0.985 |
| 32 | 739 | 601 | 0.813 | 644 | 0.871 | 1.072 |
| 40 | 635 | 538 | 0.847 | 536 | 0.844 | 0.996 |
| 50 | 564 | 393 | 0.697 | 372 | 0.660 | 0.947 |
| 57 | 536 | 331 | 0.618 | 316 | 0.590 | 0.955 |
| 64 | 526 | 295 | 0.561 | 276 | 0.525 | 0.936 |

Ladder totals: baseline **63,908** → minimal **55,473** (0.868) → structural **55,536** (0.869).

**Two things stand out.**

1. **Both fixes cut the tail hard and leave the head alone.** Picks 50–64 fall to 0.53–0.70 of baseline; picks
   1–3 barely move. Retiring the model prior from concluded careers is, by itself, most of a tail fix — which
   is what the self-reference measurement predicts, since the tail is where busts cluster and where the prior
   was doing the most work.
2. **The two prototypes agree almost exactly.** Ladder ratio structural/minimal = **1.0011**. Per pick they sit
   within ±5% from pick 10 down. The divergence — which S-2 defines as *the* measurement of the surviving
   self-reference — is therefore **small below the top of the draft**. The structural fix buys materially more
   only at picks 2–3 (+8% and +19% against minimal).

## Honest limits of the prototypes, disclosed

The structural fit is **noisier at the top**, and the raw fit says so: monotone violations in the raw
1–64 curve are 0 (baseline), 3 (minimal), **6 (structural)**. Structural raw pick 2 (3121.6) exceeds raw pick 1
(3041.0) — an inversion the carried `monotone_strict` pools away, which is why its pinned pick 2 lands at 2999
against the 3000 pin. Those top two picks are **not separated by the data**; the isotonic step and the pin are
doing it. `effn` at picks 1–3 is only 35–38, so the head is thin in every variant.

Worth naming: the baseline has **zero** raw monotone violations precisely *because* it is fitting the model's
own smooth prior. Once real evidence enters, the raw fit gets bumpy. The baseline's smoothness is a property of
the self-reference, not of reality.

A post-pin strict-descent guard was added to the prototype harness and **never fired** (0 forced points in all
three runs), so no monotone structure in the tables above is manufactured by my code.

## Par teaching population — evidence collected (report-only)

`par_build.py` `gather()` keys `pos = MA.gfut(p)` once per player, so a role migrant refiles his entire career
under his destination position. Measured on the same matrix, with three deliberately separated definitions
because the loose one overstates:

| definition | n | % of 11,209 season observations |
|---|---|---|
| (a) label string differs at all | 3,819 | 34.07% — **overstates**, counts `SF/MID` against settled `SF` |
| (b) settled label present as one half of a dual | 1,673 | 14.93% — **not** contamination |
| **(c) settled label absent from that season entirely** | **2,146** | **19.15% — the real figure** |

786 of 2,646 players carry at least one strictly-foreign season. By destination: SD 30.14%, SF 23.17%, KPD
15.63%, MID 14.23%, KPF 14.21%, RUCK 5.70%. Largest migrants are whole-career relabels — Luke Parker (settled
SD, 16 of 16 seasons recorded MID or SF/MID), Dylan Grimes (settled SD, 15 of 15 recorded KPD), Michael Johnson
(settled SD, 14 of 14 recorded KPD). Full list in `out/par_teaching_population_279.json`. Nothing changed; this
is the evidence for the owner's ruling on which population teaches the par.

## The Stanley observation — the basis work MAKES IT LIVE

Docketed to this basis review as report-only unless the basis work made it live. It does.

`ev()`'s ruck branch caps the production leg at `RUC_PRIOR_CAP*draftval(p)` = 1.4 × curve[effpk]. A basis change
that cuts the curve tail tightens that cap, hardest where the cut is deepest. Mean cap ratio against baseline
across the 54 rucks on the board:

| | n | minimal/baseline | structural/baseline |
|---|---|---|---|
| ep ≥ 40 | 10 | **0.742** | **0.716** |
| ep ≤ 20 | 4 | 0.951 | 0.959 |

Rhys Stanley (ep 47): cap 812 → 610 (minimal) → 584 (structural). Established late-pick rucks are the exposed
group — Gawn (ep 33) 1016 → 812, Briggs (ep 34) 998 → 788, Nankervis and Williams (ep 35) 979 → 774.

**Limit, stated plainly:** this is *exposure*, not a measured repricing. Whether the cap actually binds for a
given veteran depends on the run-time condition `_cpv < e <= _v0_uncapped`, which needs a board build under the
ruled basis — and that build belongs to step 4's propagation, not step 2. Reported, not fixed.

## Files

- `out/proto_basis_279.json` — both prototypes, populations, provenance counts, raw/`effn` diagnostics, the divergence.
- `out/proto_curves_full_279.json` — all three 64-point curves.
- `out/par_teaching_population_279.json` — the par evidence with all three definitions.
- `out/stanley_ruck_scaffold_279.json` — per-ruck cap exposure under each prototype.
- `scripts/proto_basis.py` — the prototype harness.

## Reversal condition (sealed, not yet run)

After the basis ruling lands, the SCAR endpoint is re-derived once under the ruled basis. If the currency choice
would flip, that STOPS before step 3 and returns to the owner.

## CI posture

None run; nothing in step 2 touches CI. Inherited from `f60af6c`: guards green with G-Y0 held at 3.035%, FV
green, and the declared `movers.test.js` known-red at exactly 2 of 58 in Final Integration and Live Scoring.

---

# FOURTH ADDENDUM — the RULED curve, the truncation backtest, the sealed reversal check, and step 3's α evidence

**Rulings in force:** γ=1.0 VOR · basis = **STRUCTURAL** · **hard class cut at 2022** (the 2022 draft class is
the last that teaches; 2023/24/25 out) · α **parked at 1.0** · par = per-season teaching, executing inside step
4's propagation, not here · the pool's ruled level lands at propagation.

**Cost, timed before the full pass:** the ruled derivation is **0.18s**, the reversal check **0.17s**, the whole
pass including the backtest and all four α settings is **3s wall**. No engine run needed.

**Carried verbatim:** `pava_ni`, `monotone_strict`, the pick-distance kernel, τ, nmin, `PW_FLOOR`, pin(1)=3000.
**Disclosed departures, both owner-ruled:** the teaching window's upper bound moves 2024 → 2022, and the year-0
contribution is the structural completed career value.

## 1. The ruled curve

Payload **`4fc40e91`**, ladder total **56,088**. Population after the class cut: **1,197 rows** (down from
1,325 on the 2004–2024 window), of which **825 concluded, 372 active, 265 never established**.

**Fallback share — asserted and reported, as required from here on:** **71 of 1,197 rows = 5.931%**, all of them
thin-stratum; zero rows fell back for want of written seasons. Provenance: 825 own realised + 301 actuarially
completed + 71 prior fallback, and the assert that those three sum to the population passes. So the model prior
survives on under 6% of the teaching population, counted, against 100% of the year-0 kernel mass in the
pre-ruling baseline.

| pick | 1 | 2 | 3 | 5 | 10 | 24 | 32 | 40 | 50 | 57 | 64 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ruled | 3000 | 2999 | 2952 | 1975 | 1511 | 828 | 643 | 545 | 376 | 319 | 279 |

Same top-of-draft caveat as step 2, and it has not improved: 6 raw monotone violations, `effn` 34.5–37.8 at
picks 1–3, and pick 2 at 2999 is the isotonic step plus the pin rather than the data. My post-pin descent guard
did not fire.

## 2. Truncation backtest — report-only seal evidence

Design: on **concluded careers only**, truncate the career to *d* written seasons, apply the structural
completion with the player **left out of his own stratum**, and compare against his actual full realised value.
Leave-one-out, so there is no self-prediction. Not a guard; does not re-open the class cut.

| written depth | n | median abs error | median rel error | median abs rel error | p90 abs error | bias |
|---|---|---|---|---|---|---|
| 2 seasons | 612 | 160.0 | **+8.35%** | 27.16% | 807.6 | over-predicts |
| 3 seasons | 553 | 129.6 | **+7.18%** | 20.83% | 719.2 | over-predicts |
| 4 seasons | 475 | 121.7 | **+4.68%** | 17.14% | 647.9 | over-predicts |

Two honest readings. The completion **improves monotonically with written depth** — median absolute relative
error falls 27% → 21% → 17% — which is what a working actuarial completion should do. And it is **consistently
optimistic**: a median +4.7% to +8.4% over-prediction at every depth. Since the completion supplies 301 of 1,197
teaching rows (25.1%), that optimism is a small upward bias on the ruled curve, concentrated where active
careers are shallow. Reported, not corrected.

## 3. Sealed reversal check — the currency choice STANDS

The SCAR endpoint re-derived once under the ruled basis (structural, ≤2022), own-surface discipline preserved
per column: the SCAR matrix reads the adopted frozen surface (`v0surf_frozen: true`), the VOR matrix its own
bake (`false`). Fallback share identical at 71/1,197 = 5.931% on both sides, so the comparison is not
confounded by differing fallback.

| | payload | ladder | steepness pick1/pick64 |
|---|---|---|---|
| SCAR, ruled basis | `32dc178b` | 58,072 | 9.646 |
| VOR, ruled basis | `4fc40e91` | 56,088 | **10.753** |

VOR/SCAR by band: 1–3 **1.023**, 4–7 1.006, 8–12 0.981, 13–20 0.954, 21–27 0.957, 28–35 0.940, 36–48 0.928,
49–64 **0.904**. Ladder ratio 0.966.

**The choice does not flip.** Under the ruled basis VOR still steepens the curve relative to SCAR (10.75 vs
9.65) and still pays relatively more at the head than the tail (1.023 vs 0.904) — the same direction, and much
the same magnitude, as the step-1 evidence the ruling rested on. No STOP is triggered; step 3 proceeds.

## 4. Step-3 evidence: the α dial (α still parked at 1.0)

α enters as a certainty-equivalent aggregator replacing the kernel-weighted mean inside the year-0 fit:
`CE_α = (Σ W·v^α / Σ W)^(1/α)`. This is the kernel-weighted generalisation of the engine's **own** `_ce0`
(`rl_model.py:815`), which floors busts at 0.0 — the code's own comment says the legacy `_ce` floor of 1.0 is
wrong for busts, and S-3 requires busts at full weight, so `_ce0` is the correct form. The tiered candidate is
the engine's own `_alpha_pvc(k) = 0.6 + (0.8−0.6)·min(k−1,49)/49` — 0.6 at pick 1 rising to 0.8 by pick 50, flat
after. α=1 returns the mean exactly, so it reproduces the ruled curve `4fc40e91` by construction (verified).

**Conservation yardstick (S-3):** total mean production over picks 1–64, honest mean with busts at full weight,
is **56,198.1** board units — the α=1 raw fit summed. The yardstick is the post-pin ladder against that.

| α setting | raw pick 1 | ladder 2–64 | vs honest mean | pick class ÷ numéraire | **conservation ratio** |
|---|---|---|---|---|---|
| 0.6 | 2853.6 | 43,712 | −17.85% | 14.57 | **0.8312** |
| 0.8 | 2921.1 | 48,711 | −8.46% | 16.24 | **0.9202** |
| **1.0** | 2986.5 | 53,088 | −0.23% | 17.70 | **0.9980** |
| tiered 0.6→0.8 | 2853.6 | 46,763 | −12.12% | 15.59 | **0.8855** |

Per-pick ratio against α=1 — the dial bites hardest at the tail, which is where the variance is:

| pick | 3 | 10 | 24 | 32 | 40 | 50 | 64 |
|---|---|---|---|---|---|---|---|
| α=0.6 | 0.926 | 0.899 | 0.778 | 0.736 | 0.703 | 0.649 | 0.602 |
| α=0.8 | 0.963 | 0.952 | 0.895 | 0.879 | 0.862 | 0.838 | 0.814 |
| tiered | 0.928 | 0.911 | 0.836 | 0.831 | 0.833 | 0.838 | 0.814 |

### The post-pin effect, measured at source rather than assumed

Ruling-sheet item 3 requires the post-pin effect be shown, not assumed. Measured: `monotone_strict` does
`fit[0] = PIN1` — it **hard-sets pick 1 to 3000 and does not rescale the ladder**. So α<1 cuts the raw value at
every pick (pick 1 falls 2986.5 → 2853.6 at α=0.6), pick 1 is then forced back to 3000, and **picks 2–64 keep
their cut with no compensating scale-up**.

The consequence is the one the filing anticipated, and it is *larger* than a global rescale would produce, not
smaller: because players scale with pick 1 (`BOARD_FACTOR = RL_PICK1/PVC[1]`), holding pick 1 at 3000 while
cutting everything below it cheapens **picks as a class relative to players**. The `pick class ÷ numéraire`
column above is that relative price: 17.70 at α=1 falling to 14.57 at α=0.6, a 17.7% cheapening of the pick
class against players. That is a real relative-price change the owner would be buying with the dial, and it is
the number to rule on alongside the shape.

**Reading for the ruling:** α=1 conserves by construction (0.998). Every downside-weighted setting pays for its
variance shaping out of the pick class — 8.5% at α=0.8, 12.1% tiered, 17.9% at α=0.6 — against total mean
production. S-3's instruction is that the resisting of edge cases goes to smoothing and the explicit dial and
never to the median as level, and that the ladder total must not be slashed against mean production. Those two
pull against each other here, and the table is the trade.

α remains parked at 1.0. α=1 staying at 1.0 is a legitimate outcome.

## Files

- `out/ruled_alpha_279.json` — the ruled curve with its asserted fallback share, the backtest, the reversal check, and all four α settings with the conservation yardstick.
- `out/ruled_curves_279.json` — the ruled VOR curve and the SCAR reversal curve, 64 points each.
- `scripts/ruled_and_alpha.py` — the harness.

## CI posture

None run; nothing here touches CI. Inherited from `f60af6c`: guards green with G-Y0 held at 3.035%, FV green,
and the declared `movers.test.js` known-red at exactly 2 of 58 in Final Integration and Live Scoring.

---

# FIFTH ADDENDUM — α SCHEDULE EVIDENCE, six settings, full 64-point ladders

**REPORT-ONLY. α stays parked at 1.0. Nothing in this addendum implies or anticipates a ruling.**

Owner viewing request before the α ruling: two additional per-pick linear schedules, on the same `_ce0`
machinery and the same fit pipeline as the ruled curve, with **full 64-point ladders committed** for all six
settings because the sampled tables in the fourth addendum are too coarse for a side-by-side.

All six are derived on the ruled basis: structural completion, hard class cut at 2022, VOR (γ=1.0), own-surface
discipline unchanged. Fallback share **71 of 1,197 = 5.931%**, provenance asserted to sum to population — the
same population as the ruled curve, so the six ladders differ by α alone.

**Control:** the flat α=1.0 schedule reproduces the ruled curve payload `4fc40e91` exactly. **Non-vacuity:** all
six ladders are distinct, and the upside schedule does exceed α=1 at some picks (it would be a dead instrument
if it could not).

Cost: 2s for all six.

## The six schedules

| schedule | α at 1 | α at 64 | ladder total | conservation | pick class ÷ numéraire | vs α=1 |
|---|---|---|---|---|---|---|
| flat 0.6 | 0.60 | 0.60 | 46,712 | 0.8312 | 14.571 | −17.66% |
| flat 0.8 | 0.80 | 0.80 | 51,711 | 0.9202 | 16.237 | −8.24% |
| **flat 1.0 (ruled)** | 1.00 | 1.00 | **56,088** | **0.9980** | **17.696** | 0.00% |
| tiered 0.6→0.8 by 50 | 0.60 | 0.80 | 49,763 | 0.8855 | 15.588 | −11.91% |
| **NEW** linear 0.8→1.00 | 0.80 | 1.00 | 53,866 | 0.9585 | 16.955 | −4.19% |
| **NEW** linear 0.9→1.05 | 0.90 | 1.05 | 55,512 | 0.9878 | 17.504 | −1.08% |

Conservation is the post-pin ladder over total mean production across picks 1–64 (**56,198.1** board units,
honest mean, busts at full weight). "Pick class ÷ numéraire" is Σ(picks 2–64) ÷ pick 1 — the relative price of
the pick class against players, since players scale off pick 1.

## Full ladders

`out/alpha_ladders_279.csv` carries all 64 picks × 6 schedules side by side, plus the α actually applied at
each pick for each schedule, and the three summary rows (ladder total, conservation, pick class ÷ numéraire).
`out/alpha_ladders_full_279.json` carries the same ladders as arrays. Every ladder is 64 points, pinned at
3000, strictly descending.

Sampled every fourth pick for orientation only — the CSV is the artifact to read:

| pick | 0.6 | 0.8 | **1.0** | tiered | 0.8→1.00 | 0.9→1.05 |
|---|---|---|---|---|---|---|
| 1 | 3000 | 3000 | **3000** | 3000 | 3000 | 3000 |
| 4 | 2626 | 2755 | 2865 | 2632 | 2760 | 2818 |
| 8 | 1955 | 2072 | 2170 | 1968 | 2081 | 2131 |
| 16 | 1176 | 1268 | 1338 | 1201 | 1281 | 1315 |
| 24 | 774 | 833 | 828 | 831 | 774 | 809 |
| 32 | 473 | 566 | 643 | 534 | 605 | 634 |
| 40 | 383 | 470 | 545 | 454 | 517 | 543 |
| 48 | 279 | 340 | 400 | 340 | 379 | 400 |
| 56 | 205 | 273 | 331 | 273 | 322 | 337 |
| 64 | 168 | 227 | **279** | 227 | 279 | 292 |

Two internal consistency checks worth noting: the tiered schedule's tail equals flat-0.8's exactly (227 at pick
64), because tiered is flat at 0.8 beyond pick 50; and linear-0.8→1.00's tail equals α=1's exactly (279),
because its α reaches 1.0 at pick 64 by construction. Both are what the constructions require.

## What the two new schedules do that the filed four did not

**Linear 0.8→1.00** is the cheapest visible haircut of the downside-weighted family: it costs **4.2%** of the
pick class against **8.2%** for flat 0.8, because the discount unwinds toward the tail instead of applying
uniformly. Its shape is the inverse of the tiered candidate — tiered is most risk-averse at the *top*, this is
most risk-averse at the top too but releases the tail entirely.

**Linear 0.9→1.05 is a different animal from the other five.** It is the only schedule that crosses α=1, so its
tail is **upside-weighted**: it pays *more* than the honest mean from about pick 45 down — 1.013× at pick 50,
1.025× at 57, 1.047× at 64 — while trimming the head by ~2%. The head trim and the tail lift very nearly cancel,
which is why it conserves at 0.9878 while still reshaping the curve. It buys shape almost without paying for it
in conservation terms.

Two readings of that, both stated because they point opposite ways and the ruling is the owner's:

- It is the schedule that most directly implements the owner's stated design theory — *"the option 'chance' of a
  star is what people want, so pricing should factor that in more"* at the tail. An upside-weighted tail is
  exactly that instrument.
- It moves the tail **further above realised production**, and the tail is already the region `#270` measured at
  ~1.56× busts-included reality on the old basis. The structural basis has since cut the tail roughly in half on
  its own; this schedule would give some of that back. Whether that is desirable is a pricing preference, not a
  correctness question — the owner's S-4 says the variance question is ruled explicitly, not inherited.

## Unchanged limits

Every schedule shares the ruled curve's top-of-draft weakness: 6 raw monotone violations in each, `effn` 34.5–37.8
at picks 1–3, and pick 2 separated from pick 1 by the isotonic step and the pin rather than by the data. The
post-pin descent guard did not fire on any of the six. The truncation backtest's optimism (median +4.7% to +8.4%
depending on written depth, on the 301 completed rows of 1,197) sits underneath all six equally and is not
corrected by any choice of α.

## Files

- `out/alpha_ladders_279.csv` — all six ladders, 64 picks, with per-pick α and the summary rows. **The side-by-side artifact.**
- `out/alpha_ladders_full_279.json` — the same six ladders as arrays.
- `out/alpha_schedules_279.json` — per-schedule metrics, conservation, pick-class effect, control and non-vacuity.
- `scripts/alpha_schedules.py` — the harness.

## CI posture

None run; nothing here touches CI. Inherited from `f60af6c`: guards green with G-Y0 held at 3.035%, FV green,
and the declared `movers.test.js` known-red at exactly 2 of 58 in Final Integration and Live Scoring.

---

# SIXTH ADDENDUM — the FOUR-FITTER PVC PANEL, plus pool / MSD / SSP levels

**REPORT-ONLY. No fitter is adopted; α=1 throughout this experiment; nothing is ruled.** Built with four
parallel subagents under one-writer discipline: I wrote the harness, the judge and every committed file, and
**re-ran every subagent's fitter myself in the pinned environment before it entered the pack** — all four came
back byte-identical to the subagent output.

## Phase 1 — the shared harness, frozen before any fitter ran

`panel/harness_pvc.py` fixes, once, for all four arms: the loader (asserts store `6b9d00a7`, surface
`b781ed25`, and a non-empty population of exactly 1,197); the establishment definition, which is the matrix's
**own** existing classification (no season with ≥6 games — 265 of 1,197) rather than a new one; the structural
year-0 values under the ruled basis with the fallback share counted (**71 of 1,197 = 5.931%**); the folds; the
single output schema, asserted at write time; and the pin/descent step carried verbatim.

Folds are deterministic and identical for all four: **k=5, seed 20260730, fingerprint `66d46e0103ce`**, sizes
240/240/239/239/239, byte-identical across re-runs. Every fitter reports the fingerprint and **the judge refuses
to score a set whose fingerprints disagree**, and refuses if the fitters predicted different held-out rows.

I also put the shipped kernel into the harness as the panel's shared reference, so "the current kernel" is
unambiguous — and it reproduces the ruled ladder `4fc40e91` exactly. That reference was re-verified functionally
before each judging step, as the tamper check on the frozen files.

**The judge was proven able to fail before any fitter was trusted:** a perfect predictor scores RMSE 0.00, a
constant 513.98, an inverted one 4201.60, with strict ordering and per-range perfect-is-zero. It asserts its own
self-test and refuses to certify otherwise.

## Phase 3 — the headline: the fitter choice does not move accuracy

| fitter | ladder | payload | medAE | RMSE | med \|rel\| | conservation |
|---|---|---|---|---|---|---|
| ruled (shipped kernel) | 56,088 | `4fc40e91` | — | — | — | 0.9980 |
| control (kernel + LL boundary) | 55,828 | `7cb36a2c` | 377.44 | 859.17 | 45.75% | 0.9934 |
| loclin (local-linear throughout) | 56,345 | `2e44ad31` | 377.08 | 858.99 | 45.96% | 1.0026 |
| powerspine (power spine + residuals) | 56,226 | `29292004` | 377.37 | 858.29 | 45.92% | 1.0005 |
| distfirst (rate × conditional mean) | 56,088 | `4fc40e91` | 377.44 | 859.13 | 45.58% | 0.9980 |

**All four are statistically indistinguishable.** Overall median absolute error spans 377.08–377.44 and RMSE
858.29–859.17 across 1,197 held-out rows whose p90 absolute error is ~1,170. The spread between fitters is about
0.4 against an error scale of 377 — three orders of magnitude smaller than the error itself. On held-out
accuracy there is nothing to choose between them, and any ruling has to rest on other grounds.

Full 64-point ladders for all four plus the incumbent are in `out/panel_ladders_279.csv`.

## The one real signal: the tail is a kernel boundary artifact

Median absolute error by pick range (n per range: 189 / 188 / 190 / 285 / 345):

| fitter | 1–10 | 11–20 | 21–30 | 31–45 | **46–64** |
|---|---|---|---|---|---|
| control | **877.87** | 447.67 | 486.03 | 366.31 | **265.85** |
| distfirst (= shipped kernel) | **877.87** | 447.67 | 486.03 | 366.31 | 291.15 |
| loclin | 886.45 | 447.82 | 492.86 | 369.01 | **265.35** |
| powerspine | 911.70 | **435.18** | 489.38 | 370.74 | 282.19 |

At picks 46–64, on 345 rows, the **local-linear boundary treatment beats the kernel by about 9%** — 265.85 and
265.35 against the shipped kernel's 291.15. That is out-of-sample confirmation of the boundary argument the
control arm was built to test: the shipped kernel's window is one-sided at the pick-64 edge, borrows from
higher-valued interior picks, and biases the tail **upward**. Part of the residual tail overpricing is a fitting
artifact, not a basis problem.

At picks 1–10 the ordering reverses and the kernel is best (877.87 against 886.45 and 911.70). So the control —
kernel at the head, local-linear at the boundary zones — is the best-performing arm in **both** zones, and its
ladder equalities make that visible: it equals the shipped kernel exactly at picks 3–50 and equals loclin
exactly at picks 1–2 and 51–64 (verified).

## Two structural findings the panel produced

**1. The distribution-first arm is the kernel by algebraic identity — three price readings, not four.** I
verified this myself, independently of the subagent's code: `max |rate × condmean − kernel_mean|` over picks
1–64 is **2.27e-13**. Since `rate = ΣW·1{v>0}/ΣW` and `condmean = ΣW·v/ΣW·1{v>0}`, the indicator cancels and the
product *is* the kernel mean whenever both components share a bandwidth. Its ladder payload is `4fc40e91` — the
ruled curve. With a 1.5× conditional-mean bandwidth it deviates by up to 260, so the machinery is live; the
common-bandwidth policy makes it degenerate. Its identical judge score must be read as **confirmation, not an
independent second reading**. The subagent flagged this itself rather than presenting the match as a result.

Its real contribution is the decomposition, which is new evidence:

| pick | 1 | 10 | 24 | 40 | 64 |
|---|---|---|---|---|---|
| establishment rate | 0.9996 | 0.955 | 0.831 | 0.716 | **0.564** |
| value if established | 2988 | 1563 | 996 | 761 | **495** |

The late picks are cheap mainly because **44% never establish**; those who do are worth about 495. That is the
same shape as the pool levels below, where the median is zero and the mean is carried by a minority.

**2. Every arm is non-monotone at picks 1–3, independently.** All four raw fits put pick 2 or 3 above pick 1
(loclin 3138.6 vs 2995.6; distfirst 3103.4 vs 2986.5; powerspine 3045.4 vs the 3000 pin). Four estimators
disagreeing with monotonicity in the same place is a property of the data, not of any one smoother — effective n
at picks 1–3 is only 34–38. The top of the draft is genuinely unresolved, and the pin is what separates picks 1
and 2 in every arm.

**Smoothness is where the arms genuinely differ**, and it is not an accuracy question:

| | control | loclin | powerspine | distfirst |
|---|---|---|---|---|
| raw monotone violations | 6 | 7 | **0** | 6 |
| picks forced by descent | 8 | 9 | **1** | 8 |

`powerspine` hands over an already strictly-descending curve; its single forced pick is only because its raw
pick 2 (3045.4) exceeds the 3000 pin. The other three need 6–7 violations pooled and 8–9 picks nudged. Against
that, powerspine is the **worst** arm at picks 1–10 (911.70).

## Two things that would be easy to misread

**The positive signed error is arithmetic, not bias.** Every fitter shows a positive median signed error (+153
to +340 by range). The structural values have mean 890.7 against median 559.5, with 22.1% exactly zero and
67.2% below the mean. A **mean** fit on a right-skewed population must over-predict the median row. It is
near-identical across all four and is not evidence of a biased fitter.

**One disclosed comparability asymmetry.** No fitter pinned inside `fold_fit` — every arm's pick-1 held-out
predictions sit in 2900–3100 rather than at 3000 — so the scores are comparable, and I checked this rather than
assuming it. One asymmetry stands: `powerspine` monotonises its fold predictions (PAVA + descent) while the
other three do not; median-by-pick non-monotone steps are 5 for powerspine against 10–11 for the others. That is
part of what its method *is*, it is disclosed, and it should be read as a property of the arm rather than an
unfair advantage.

## Pool / MSD / SSP levels under the ruled basis — and a correction to the brief's denominators

Honest mean, busts at zero, completions for actives, VOR, class cut 2022.

| | n | level | 95% interval on the mean | median | never established | fallback |
|---|---|---|---|---|---|---|
| POOL | 1,005 | 239.7 | [211.1, 268.2] | **0.0** | 56.6% | 6.07% |
| MSD | **44** | 303.2 | [89.0, 517.4] | 3.3 | 50.0% | 2.27% |
| SSP | **31** | 341.0 | [83.6, 598.4] | 0.5 | 45.2% | 6.45% |

**The brief named MSD n=106 and SSP n=52. Those are the store-level entry-stream counts across all 2,651 rows**
— correct as such, and matching amendment C3 exactly — **but they are not what the ruled basis prices.** Under
the class cut the ruled levels rest on **44** and **31** rows. The uncertainty is therefore **wider** than the
brief assumed, not narrower: relative standard errors are 36.0% (MSD) and 38.5% (SSP), against 6.1% for the
pool. The reconciliation chain is in the evidence file (store-level → 2004–2024 pool rows → ruled class cut:
106 → 72 → 44 for MSD, 52 → 43 → 31 for SSP).

And in every one of these populations the **median structural value is at or near zero** — 0.0, 3.3, 0.5 —
because roughly half never establish. These levels are means carried by a minority. **Read the interval, not
the mean.**

One disclosed choice: the completion table is built from concluded **pool** rows and shared across the subsets.
Within-stream tables at n=44 and n=31 would leave almost every active on the model prior, making the
"completion" a prior in disguise. The cost is that MSD/SSP actives are completed against pool-wide look-alikes
rather than stream-mates; per-stream fallback shares are printed so that is visible.

**These levels feed the eventual FHV re-denomination word at adoption. Report-only today.**

## Files

- `out/panel_ladders_279.csv` — all four ladders plus the incumbent, 64 picks, with totals, conservation, raw violations and forced counts. **The side-by-side artifact.**
- `out/panel_comparison_279.json` — the full comparison: harness provenance, judge self-test, error by range, conservation, disclosed parameters, ladder equalities.
- `out/judge_279.json` — the judge's own output.
- `out/conservation_279.json` — conservation and forced-descent lists per fitter.
- `out/levels_pool_msd_ssp_279.json` — the levels with denominators, intervals and the reconciliation.
- `panel/` — the frozen harness, runner, judge, the four fitter modules as run, and their result files.

## CI posture

None run. This addendum is pure fits on the committed matrix — **no engine bake is involved**, so no bake-lane
coordination applies. Posture inherited from `f60af6c`: guards green with G-Y0 held at 3.035%, FV green, and the
declared `movers.test.js` known-red at exactly 2 of 58 in Final Integration and Live Scoring.

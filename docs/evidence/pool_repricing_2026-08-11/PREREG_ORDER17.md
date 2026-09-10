# PRE-REGISTRATION — ORDER 17, POOL REPRICING BUILD PHASE 1

**Written BEFORE any measurement in this act was run.** Standing law: predictions are registered first,
then breaches are reported plainly against them. This act's wider register already carries four owned
pre-registration breaches; this file adds its own.

**Identity asserted at the time of writing:**
- `origin/main` = `d3d5f5592e57ffbe0f90fe5744c7c6fb17392b82`
- live board `data/rl_build/rl_app_data.json` md5 = `94f1fec59f99c59d5890d5975c79fa9b`
- store = `d9a24282357cf3083b1640466e3ecd83`
- instrument `noarb_table_338.py` md5 = `0f8220351c64c56ccfa90c60edcdfa5f` (UNMODIFIED)
- branch `build/pool-repricing-phase1` cut from `d3d5f55`

**One honesty note that qualifies P1 and must be read with it.** P1 below is NOT a blind prediction.
Before writing it the seat had already read `session_2026-07-03/d13/scripts/d13_norm_harvest.py`, the
script that BUILDS the retention surface's derivation population. The prediction is therefore an
inference from a code read, and the measurement tests whether the code read is borne out in the row
counts. The seat records this rather than presenting a read as a forecast.

---

## P1 — THE POPULATION QUESTION (D8 iii)

**Prediction: the question IS determinable, and the answer is SPLIT rather than uniform.**

The directive states the question "cannot be determined from the derivation script", citing
`d13_derive.py`. That is correct about `d13_derive.py` — but `d13_derive.py` is the CONSUMER. It reads
`d13_normcells.json`. The PRODUCER of that file is `d13_norm_harvest.py`, which survives in the repo,
and its population gate is explicit.

P1.a — the harvest gate carries **no `_pool` exclusion**. Its only exclusions are `_double_count`, a
missing position group, and `not (pick or _ft)`. Therefore pool rows were NOT categorically excluded.

P1.b — entry is nevertheless **not uniform across pathways**, because `_ft` is set per pathway in
`rl_model.py`: `_ft=True` for ND (all picks, including >64) and for RD/PSD; `_ft=False` for the
pickless mechanisms (SSP/MSD/IRE/UNR/PDA/PDN/PDS). For those, entry requires a stored `pick`.

P1.c — predicted verdict: **RD and ND>64 rows WERE in `R`'s derivation population** (both carry
`_ft=True`), so for those two pathways the composed `H` multiplier **charged the same effect twice**.
The pickless pathways were **largely OUT**, so for them `H` was a bolt-on to a surface read outside
its evaluated range. Predicted magnitude: >90% of RD and ND>64 rows in; <10% of pickless-pathway rows in.

P1.d — predicted blocker, stated in advance so it is not discovered as an excuse: `d13_normcells.json`
itself is **absent from the repo**, so the population cannot be read back directly from the artefact
and must be RECONSTRUCTED by replaying the harvest gate. The reconstruction is a faithful replay only
if the gate fields are recoverable from the current matrix. If they are not, the honest answer is
"not determinable" and the act says so and stops on task 5.

## P2 — LAYER 1

P2.a — the per-pathway `realised_full` profiles will **reproduce the directive's [PROFILE] table**
(D3) to within 1e-4, because the same harness function on the same matrix is being called. Any
departure is a build error, not a finding.

P2.b — PDS shrunk toward the pool aggregate at K=15 with `w = 21/(21+15) = 0.5833` lands at
`0.5833*0.1259 + 0.4167*0.5218` ≈ **0.291**. No other pathway's layer-1 value moves (all have n>=43,
and the ruling names PDS alone).

P2.c — the ND calibration target is **1.0252**, not 1.00.

## P3 — LAYER 2

P3.a — RD's six positional cells reproduce D3B (RUCK 0.9584 · SF 0.6581 · MID 0.5892 · SD 0.4818 ·
KPF 0.4180 · KPD 0.2825) to within 1e-4.

P3.b — keyed on **pathway x position x age only**. No pick axis. `effpk` is the constant 65 for every
pool entrant, so a pick axis would be a fabricated dimension.

P3.c — after borrowing at K=10 and renormalising, every pathway's entry-weighted mean cell value
equals its layer-1 value **exactly** (that is what the renormalisation guard is for).

P3.d — the borrowed whole-pool shape will be **dominated by RD** (688 of 1197), so thin-cell borrows
are in practice RD borrows. Predicted: the whole-pool shape's rank order matches RD's rank order
exactly (RUCK best, KPD worst).

## P4 — RECONCILIATION

P4.a — under **rule 2** (unsampled remainder priced as its own residual group) every pathway
reconciles at **<= 1e-9** relative. Predicted actual residuals at or below 1e-15 — i.e. float noise,
because the law is an identity.

P4.b — under **rule 1** (remainder carries the pathway value) MSD and IRE fail at ~1.5e-1 and ~1.4e-1,
reproducing [RECON]. The act reports rule 1 as the measured counter-example, and ships rule 2.

## P5 — THE POOL SIT-OUT RETENTION

P5.a — `H_POOLSIT` (0.804) and `H_UNION` (0.280) retire. The derived object replaces the composed read
`0.549 x 0.804 = 0.441` (non-KPP depth 1) rather than multiplying on top of it.

P5.b — predicted direction: the pool-derived depth-1 retention lands **above 0.441**, i.e. the composed
read was harsher than pool history supports. Reason: `H_UNION` re-derived to 0.167 against a shipped
0.280 and `H_MATNONRD` re-derived to 0.5162 with a CI containing 1.0 — the family has a measured
history of not reproducing, and in the one direction tested it did not reproduce as harsher.
Predicted range 0.30-0.65 at depth 1. **This is the weakest prediction in the file and is flagged as
such.**

P5.c — the mean-preserving law: any within-pathway sitter differential must be a redistribution.
Predicted: sitters sit BELOW their pathway's mean and non-sitters correspondingly ABOVE, with the
entry-weighted pathway mean unchanged to float noise. A net charge would be a law breach and is to be
reported as one if found.

## P6 — DRAFT AGE (D7)

P6.a — fitted to **playing quality only**. The participation-inclusive measure that retired ITEM B's
steps is not to be used.

P6.b — predicted: **RD shows a real age signal** on quality (D7's table reads 56.40 / 62.34 / 62.83
across age bands) and it survives at RD's sample size. Predicted: **most thin pathways show no
signal**, and per the ruling they then get **no** age adjustment.

P6.c — predicted count: at most 2 of 9 pool pathways carry a fitted age adjustment. If more than 2 do,
the seat is to suspect it has re-admitted participation through the back door and re-check the measure.

## P7 — THE CONSEQUENCE READ

P7.a — board total moves by about **-0.25%** (the directive's option-C sizing on the ruled basis), and
in any case by less than 1%. Only 82 of 242 pool board rows can move at all.

P7.b — all-arm year-one cohort ratio rises from **0.8850** to roughly **1.03**, i.e. above 1.00, and
the no-arbitrage margin against the 14% charge stays **positive** (predicted +10 to +12 points).

P7.c — both headline metrics reported: the career profile AND year-4-over-year-0. Neither is a target.

P7.d — Noble, Hall, Peatling, Keane, McCarthy, McAndrew do **not** move (>= 10 career games, carry
0.000). Herbert, Podhajski and Coe do move.

## P8 — `_ruc_prior_cap`

P8.a — predicted: it **does** bind on at least one derived pool ruck v0, because RD RUCK is the
best-delivering pool cell (0.9584) and the derived level rises toward it while the cap is a ceiling on
ruck priors. If it binds, that is reported as a build-time finding, not silently clipped.

---

**Breaches will be reported in the summary document plainly, each named against its prediction
number, whether or not they flatter the act.**

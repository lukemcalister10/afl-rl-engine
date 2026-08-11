# THE MARK-UP TRACE (RULING 2.6) INSTRUMENTS — landed 2026-08-10

The trace that took the year-0 -> year-1 mark-up apart term by term and named its driver.
#334 landing comment **5235847132**; brief 5235660463; prior audits 5235555305. This is the
act that ordered the ruck act (comment 5236274192) off its RUCK deficit finding.

## CLASSIFIED BY CONTENT, NOT BY PREFIX

The `an1.py … an13.py` series carries no act name in its filenames and was provisionally
assigned to the sitter act by the landing brief. It is **not** the sitter act's: all thirteen
open `decomp_b.json` or `live.json` — the two files this act's own engine-instrumented
scripts write — and they reproduce MARKUP_PROGRESS steps 7 through 10 in order. They are
landed here. (The sitter act's instruments are `xsec*.py`, landed under
`sitter_act_2026-08-10/`.)

## PATH CONVENTION — TWO TIERS

**Tier 1, the three engine-instrumented emitters** (`decomp.py`, `live.py`, `ycred.py`). These
DO load the engine. They take their paths purely from the environment:

    RL_WORKDIR   a snapshot workspace containing _merged_recover.py and rl_model_data.json
    RL_VENDOR    vendor path (default /home/claude/rl_vendor)
    RL_OUT       output json path      RL_DEC  the decomp rows json (ycred.py only)
    RL_S6        the s6 rows json

Each of the three loads the engine the same way — read `_merged_recover.py`, truncate it at
`print("=== AFTER`, and `exec` the prefix with stdout redirected — then pulls the internals it
needs out of the resulting globals (`MA`, `cp`, `ev`, `v0_start`, `_v0_uncapped`, `_v0_raw`,
`_prod_path`, `_expgate`, `par_pole`, `recover`, `iso_eff`, `_ycred_mult`). `decomp.py` states
that it mirrors `measure_g6.py`'s fold exactly and then re-computes `raw_ev`'s internals with
instrumentation. The snapshot workspace (`ws/`, `ws_b/`) is not landed — re-snapshot
`engine/rl_after` at the pin you want.

**Tier 2, the thirteen readers** (`an*.py`). No engine, no environment, no arguments: they
`open('decomp_b.json')` / `open('live.json')` **relative to the current directory**. Run them
from the directory holding those two files — both are landed here, so `cd` into this directory
and they run as-is.

## WHAT THIS SET CONSUMES

| input | note |
|---|---|
| `s6_rows.json` (md5 `9015cda31efc25bd471dcc74fdc265fa`, 3.6 MB) | the stage-6 per-row emission, session scratchpad root. NOT on main. Not landed here (size, and it is the shared input of four acts) — see the ruck set's README for its provenance. |
| a snapshot of `engine/rl_after` (`_merged_recover.py` + `rl_model_data.json`) | branch engine, store `37ced3ce` |
| `decomp.json` / `decomp_b.json` / `live.json` / `ycred.json` | **landed here** — the outputs of tier 1 and the complete inputs of tier 2. |

Because all four tier-1 outputs are landed, the entire analytic half of this act
(`an1`-`an13`) re-runs with no engine and no branch fetch.

## THE INSTRUMENT

    markup = price / v0  =  surf x prod ,   surf = v0_uncapped/v0 ,  prod = price/v0_uncapped
    excess = price - F                       (F = the realized-value read on the same rows)

and the exact three-term attribution (`an5.py`) splits `excess` into `ptsSURF + ptsPROD +
ptsBASE`, each line carrying its own `chk` residual against the total. `an2.py` splits `prod`
further into band / pole / other.

## KEY FILES AND WHAT THEY FOUND

- `decomp.py` -> `decomp.json`, `decomp_b.json` — the per-row decomposition (`y0`/`y1` with
  `pr`, `pole_credit`, `iso`, `raw`; plus `v0`, `v0u`, `e1`, `s6_price`, `s6_F`).
- `an1.py` — the raw per-position table (pr0/C0/poleSh0 vs pr1/C1/poleSh1).
- `an2.py` — mark-up = surf x prod, with the prod split.
- `an3.py`, `an7.py`, `an8.py`, `an9.py` — the lens-carry counterfactuals. `an8.py` runs two:
  CF-A gives every player the leg production re-pricing on his own raw year-0 value; CF-B
  carries the year-0 lens multiplier into the year-1 price with the leg book conserved exactly
  (constant `k`). `an9.py` restricts to draft age <=18: **the lens-carry closes 99.1% of the
  young KPD excess** — that is the act's verdict.
- `an4.py`, `an5.py` — the exact three-term attribution. KPD excess is **98.6% year-0 lens
  factor**; the RUCK deficit is the ruck production cap; KPF/MID deficit is lens + leg-level
  base.
- `an6.py` — the upper-bound test: kill the pedigree pole entirely. Eliminates the pole as
  driver.
- `an13.py` — the book-level ledger (B5 floor lift, caps cut, pole credit share) and the
  worked examples.
- `live.py` -> `live.json`; `an10.py`, `an11.py`, `an12.py` — the live board scan. 184 live
  year-1-3 ND rows, cohort re-anchoring factor `R_bar = 0.826`, 30 players above 1.8x v0,
  KPD live R = 0.583. `an11.py` drops rows with a degenerate raw year-0 value (`v0u < 50`,
  mature entrants) — a real and deliberate exclusion, stated in its own output line.
- `ycred.py` -> `ycred.json` — the L1c young-credit multiplier `_ycred_mult` (`RL_YOUNG`
  default ON) measured at both ends. It fades 1.337 -> 1.108 and its KPD ratio is 0.775, i.e.
  it works **against** the KPD mark-up. Eliminated as driver.
- `MARKUP_PROGRESS.md` — the act's own step log (steps 1-11), including the engine citations
  (`_merged_recover` `raw_ev`/`par_pole`/`recover`/`_prod_path`/`O1`; `O1` is `_BOARD_PATH`-gated,
  walk-forward off). Those citations are the act's own and were not re-verified by this landing.

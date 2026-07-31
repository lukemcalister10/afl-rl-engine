# L2 — THE TWO WINDOW CANDIDATES, MEASURED. **Both presented. Neither chosen.**

**#290, L2 seat, 2026-07-31.** The owner words the window. L3 does not start before it.
Raw measurement: `l2_window_candidates.json`. Harness: `l2_window_measure.py`.

**Substrate.** The reconstructed L1-exit tree (γ=1.0, stop-point curve `e69a3f38`, v0surf refit
through the declared lane), with **E3 applied** — per-season par keying + `PAR_DUAL_RULE='primary'`
(Q2 PRIMARY, ruled) + the loud empty-group HALT. E3 is L2's own act and is not in question here; the
window is.

**Portability.** The measurement's file-open audit records that `v0surf.pkl` is **never read** by the
par path. Both candidates were measured in one container on one substrate, so the A-vs-B comparison is
unaffected by the v0surf divergence filed alongside this (`V0SURF_DIVERGENCE.md`).

---

## 0 · CONTEXT RE-MEASURED, NOT READ

| the runbook's stated context | my measurement | verdict |
|---|---|---|
| store scoring spans 2005–2026, zero 2004 rows | span **2005–2026**, 22 distinct years, **0 rows in 2004** (and 0 in 2003), no interior gaps, 11,264 scoring rows over 2,651 store rows | **confirmed** |
| 65 rows of the 2003 draft class carry scoring | **65 of 107** store-wide; **64 of 106** once par_build's own pool filter (`GRP[pos]` and `pick or _ft`) applies | **confirmed, with the denominator named** |
| tenure anchoring is draft-year-based; nothing imputes zeros | confirmed by code path **and** by measurement — see §2 | **confirmed** |

Dials at this substrate: `MIN_GAMES=6.0` · `TEN_MAX=6` · `DRAFT_HI=2018` · `H_LOGPICK=0.4` ·
`PAR_DUAL_RULE='primary'`. Groups: MID, SD, SF, KPD, KPF, RUCK.

---

## 1 · CELL POPULATIONS — every count with its denominator

| | **A · censor-aware 2003** | **B · uniform 2004+** | A − B |
|---|---|---|---|
| store rows (denominator) | 2,651 | 2,651 | 0 |
| eligible pool players | **1,759** | **1,653** | **+106** |
| raw played-season rows (g>0) | **5,556** | **5,313** | **+243** |
| gated on-park observations | **4,215** | **4,016** | **+199** |
| starved position groups | **none** | **none** | — |
| thin groups (<4 obs) | none | none | — |

B's pool is exactly A's pool less the 106 pool-eligible 2003-class players (1,759 − 1,653 = 106).
The E3 loud HALT does not fire under either window.

**On-park observations by position** — A / B / delta:

| MID | SD | SF | KPD | KPF | RUCK |
|---|---|---|---|---|---|
| 1,211 / 1,126 / **+85** | 793 / 738 / **+55** | 1,052 / 1,037 / **+15** | 448 / 424 / **+24** | 506 / 497 / **+9** | 205 / 194 / **+11** |

RUCK is the thinnest group under both windows (205 / 194 of 4,215 / 4,016).

---

## 2 · THE CENSORING QUESTION, ANSWERED BY MEASUREMENT

**On-park observations by tenure:**

| tenure | A (2003) | B (2004+) | A − B |
|---|---|---|---|
| **1** | **438** | **438** | **+0** |
| 2 | 689 | 651 | +38 |
| 3 | 786 | 743 | +43 |
| 4 | 826 | 783 | +43 |
| 5 | 767 | 728 | +39 |
| 6 | 709 | 673 | +36 |

**This is the decisive number. Tenure 1 is +0.**

The 2003 class's tenure-1 season is 2004, and the store carries **zero** 2004 scoring rows — measured:
0 of the 106 pool-eligible 2003-class players carries a 2004 season. `gather()` computes
`g = r['games'] if r else 0` and admits only `g > 0`, so an absent season is **skipped, never taught as
a zero**. Candidate A therefore adds observations at tenures **2–6 only** and contributes **nothing** to
the tenure-1 cell that anchors the ramp (`ramp[1] = 0` by construction).

**So "censor-aware" is not work to be done — it is already the behaviour of the code.** Including the
2003 class does not inject a censored or depressed first-year cell. Whatever else separates these two
candidates, it is not zero-imputation at tenure 1.

The 2003 class's 243 raw rows pass the flat gate at **199/243 = 81.9%**, against the pooled rate of
**4,215/5,556 = 75.9%** — i.e. the added rows are slightly *more* established than the cohort average,
which is what surviving to tenure 2+ selects for.

---

## 3 · GATE CLASSIFICATIONS

| | A (2003) | B (2004+) |
|---|---|---|
| on-park under the **live** flat gate (`games ≥ 6`) | 4,215 of 5,556 = **75.86%** | 4,016 of 5,313 = **75.59%** |
| off-park | 1,341 | 1,297 |
| on-park under the **docstring's** base-rate-relative rule | 2,892 | 2,778 |
| **rows where the two rules disagree** | **1,329 of 5,556 = 23.9%** | **1,244 of 5,313 = 23.4%** |

**The window barely moves the gate** (75.86% vs 75.59%) — the gate is not what separates the
candidates.

**But the measurement surfaced a separate, real divergence, which L2's "re-derive the structural gate"
half owns.** `par_build.py` asserts a base-rate-relative gate in two places:

- `:12` (docstring) — *"'on the park' = games_at_tenure >= f * base_play_rate(pos,tenure)
  (base-rate-relative, **NOT flat >=6g**)"*
- `:97` (inline) — *"apply the base-rate-relative gate"*

and the code at `:63` applies `if g >= MIN_GAMES:` — *flat ≥6g*. `base_play_rate` **is** computed
(`:93-96`), returned (`:102`, `:231`) and then used **only to print a report table** (`:264-267`); no
consumer gates on it. The two rules disagree on **23.9%** of rows, so this is not cosmetic.

This is the same class as E5's docstring correction in this very file. **I have not changed the gate,
and I am not proposing to** — it is reported for disposition. (H.3: the last seat proposed weakening a
gate that was working.)

---

## 4 · SURFACE DELTAS

The par surface is on the value path: `_par_prior(p,Y) = PR.par_at(...)` enters the blend at
`_merged_recover.py:580` weighted by `_ev_pw(Eq)`, which fades from 1.0 to the pinned residual floor
`_EVW_R = 0.11` and **never reaches 0**. So every cell below moves player value — most for
low-qualification players, at ≥11% weight for everyone.

Grid: 6 groups × 9 eval picks × 6 tenures = **324 cells**, no NaNs under either window.

| | |
|---|---|
| cells compared | **324 of 324** |
| cells that moved (>1e-9) | **324 — every cell** |
| cells unchanged | 0 |
| **relative delta, median** | **0.471%** |
| relative delta, p90 | 1.309% |
| relative delta, max | **3.207%** |
| largest absolute move | **−1.889 at RUCK · pick 12 · tenure 3** |
| direction | **166 up / 158 down** — no systematic shift |

**The move is redistributive, not a level shift.** Per position, max |Δ| / mean |Δ|:

| MID | SD | SF | KPD | KPF | RUCK |
|---|---|---|---|---|---|
| 1.192 / 0.444 | 1.212 / 0.558 | 1.290 / 0.224 | 0.801 / 0.393 | 0.812 / 0.339 | **1.889 / 0.614** |

**RUCK moves most and is the thinnest group** — 205 observations under A, 194 under B, so 11 added
observations move its surface by up to 3.2%. The RUCK ramp is where the two windows most disagree:

```
RUCK ramp (shrunk, anchored yr1=0)   A: 0.000  0.000  3.163  13.295  21.343  24.209
                                     B: 0.000  0.000  4.892  13.635  22.510  24.559
MID  ramp                            A: 0.000  5.511 11.006  15.869  20.647  24.420
                                     B: 0.000  5.352 10.599  16.195  20.407  24.759
```

Representative cells (`par_at`):

| cell | A | B | Δ | rel |
|---|---|---|---|---|
| MID · 1 · 3 | 84.6021 | 83.6888 | +0.9133 | +1.091% |
| MID · 45 · 6 | 77.8792 | 78.1852 | −0.3060 | −0.391% |
| RUCK · 12 · 3 | 57.0057 | 58.8943 | **−1.8887** | **−3.207%** |
| RUCK · 1 · 3 | 71.5472 | 72.7258 | −1.1786 | −1.621% |
| KPD · 12 · 3 | 60.6012 | 59.9034 | +0.6978 | +1.165% |

---

## 5 · WHAT THE CHOICE ACTUALLY IS

Stated plainly, from the measurements above and nothing else:

- **It is not about zero-imputation.** Tenure 1 is +0 either way (§2).
- **It is not about the gate.** 75.86% vs 75.59% (§3).
- **It is not about starving a position.** Neither window starves or thins any group (§1).
- **It is about 199 extra teaching observations (+5.0% of 4,016), all at tenures 2–6**, and what they
  do to a surface that is on the value path — a **0.471% median / 3.207% max** redistribution
  concentrated in the thinnest group.

Both candidates produce a complete, fittable, non-starved par spine. Neither is disqualified by
anything measured here.

**No recommendation is offered. The window is the owner's word.**

---

## 6 · COSTS, ACTUAL

| act | measured |
|---|---|
| `setup_env.sh` (idempotent re-prove, 5/5 pins independently re-verified) | 3s |
| `bootstrap.sh` + Guard 5 | <1s |
| `refit_v0surf.py --bake` (declared lane) | **66s**, and again **65s** on the determinism re-run |
| `rl_export.py` board | **120s** |
| `s4_matrix_M1v7.py` book | **159s** |
| `one_source_selftest.py` | **88s** |
| **full L1 reconstruction chain** | **367s** (record: 480s) |
| **the L2 measurement itself — both candidates, one process** | **25.6s** |
| one wasted chain (my env slip: missing `PYTHONPATH` for the vendored unidecode) | 6s, recorded |

Every engine act ran strictly serially behind `tools/preboot_assert.sh`, re-proven in this container in
both directions before use.

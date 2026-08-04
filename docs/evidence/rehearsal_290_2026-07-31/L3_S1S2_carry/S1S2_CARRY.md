# L3 act (2) — S-1/S-2 CARRIED INTO THE DERIVATION PATH

**#290 L3, 2026-07-31.** Ruled opening act (2) (seam go: [#290 issuecomment-5143115766](https://github.com/lukemcalister10/afl-rl-engine/issues/290#issuecomment-5143115766)).
Everything below is re-runnable in **3 seconds**: `bash docs/evidence/rehearsal_290_2026-07-31/L3_S1S2_carry/carry_verify.sh`, whose output is committed verbatim beside this file as `CARRY_VERIFY.txt`.

## What the act turned out to be

The hand-back scoped this as *"the logic is in `harness_pvc_REPINNED.py`, an evidence script … the derivation home is where L6 re-derives."* Measured, the gap is **not** that S-1/S-2 needed writing. It is that **the ruled derivation lane was not reachable from the derivation home at all.**

The ruled construction is three parts:

```
committed matrix -> harness_pvc.structural_values()   S-1 / S-2, ruled basis N2
                 -> fitter_control.full_fit()         the ruled FITTER, N3
                 -> pooled_numeraire                  the ruled PIN POLICY, N4 / N14
                 -> the curve (payload · ladder · s)
```

Measured before the act, on the carrier at `5d67fe3`:

| part | on the carrier | on the shaping branch (HOLD) |
|---|---|---|
| `harness_pvc.py` — S-1/S-2 | **absent** (only the step-4 re-pin, `harness_pvc_REPINNED.py`) | present |
| `fitter_control.py` — ruled fitter N3 | **absent** | present |
| `pooled_numeraire.py` — ruled pin policy N4/N14 | **absent** | present |
| `per_entrant_279_vor.json` — the matrix the ruled curve came from | **absent** | present, md5 `77eba4d3` |

**So L6 could not have re-derived the curve from anything reachable from the tree.** That is the third instance of one class, after the v0surf bytes that did not travel (N16) and the ND matrix with no committed input (the watched-number blocker). Same shape each time: the *conclusion* travelled and the *instrument* did not.

## THE ROUND TRIP — the carried lane IS the lane, not a re-implementation

Held to the standard the T1 seat set for itself (*"the applied word IS the treatment that was measured"*). The lane, run from the carrier tree on the matrix the ruled curve was originally derived from:

| | got | want | |
|---|---|---|---|
| payload | `e69a3f38` | `e69a3f38` | **MATCH** |
| ladder Σ(1..64) | **54,722** | 54,722 | **MATCH** |
| `s` | **0.977688** | 0.977688 | **MATCH** |
| `pooled_head_pre_scale` | **3068.4647** | 3068.4647 | **MATCH** |

Four independent identities, including the **N14 numeraire primitive** exactly. Matrix md5 asserted `77eba4d3…` on entry.

## THE PAIRING INTERLOCK — proven able to fire, all four cells

The lane selects its pins by **which `harness_pvc.py` is importable**. That is a real footgun — and it is already guarded: `load_matrix()` asserts store and surface identity on entry, so a wrong pairing halts loudly rather than deriving a quiet wrong curve. Proven in both directions rather than assumed:

| harness | matrix | result | |
|---|---|---|---|
| ORIG (`6b9d00a7`/`b781ed25`) | ruled | **HALT** | `matrix store 81d24704 != committed identity 6b9d00a7` |
| RE-PINNED (`81d24704`/`96d671c9`) | VOR | **HALT** | `matrix store 6b9d00a7 != committed identity 81d24704` |
| ORIG | VOR | **PASS** | ND=1197 |
| RE-PINNED | ruled | **PASS** | ND=1197 |

**The re-pinned harness is therefore NOT committed under the name `harness_pvc.py`.** Two importable files of one name carrying different pins would be the exact hazard the interlock exists to catch. `carry_verify.sh` stages it under that name in a temp dir for the duration of a run and removes it.

## S-1/S-2 ON THE RULED SUBSTRATE — every count with its denominator

```
substrate : store 81d24704 · v0surf 96d671c952c8 · frozen True
counts    : concluded_realised 825 · completed 301 · prior_fallback_thin 71
sums      : 825 + 301 + 71 = 1197 == 1197   OK
```

| ruling | measured | share of 1,197 |
|---|---|---|
| **S-1** — concluded careers vote at full evidence weight, prior retired from them entirely | **825** | 68.9% |
| **S-2** — actives' unwritten remainders completed actuarially from concluded look-alikes | **301** | 25.1% |
| the prior surviving **only** as a counted thin-stratum fallback — the **WATCHED NUMBER** | **71** | **5.931%** |

Identical to the T1 hand-back's figure, on the same committed matrix — as it must be, since the matrix is byte-identical; recorded as a re-measurement through the carried lane, not as a re-quote.

## FIRST-PASS CANDIDATE ON THE RULED SUBSTRATE — a waypoint, not a landing figure

The lane now runs end-to-end on the ruled substrate. One pass:

| | stop-point | ruled substrate, first pass |
|---|---|---|
| payload | `e69a3f38` | **`6dedc611`** |
| ladder Σ(1..64) | 54,722 | **54,532** |
| `s` | 0.977688 | **0.996218** |
| `pooled_head_pre_scale` | 3068.4647 | **3011.3898** |

**This is a WAYPOINT. Nothing between L1 and L6 is a landing figure** (runbook §0). It is a **single pass, not a fixed point** — L6's convergence iterates curve ↔ surface, and only its converged output is judged against the 2.000% bar. No gate moved, nothing installed, no pin re-stamped.

## WHAT WAS CARRIED, AND WHAT DELIBERATELY WAS NOT

**Carried — 7 files, every one asserted BYTE-IDENTICAL to the shaping branch**, so a later merge of that branch is a no-op for them rather than a conflict:

```
session_2026-07-30/item279/panel/harness_pvc.py          ac198ca
session_2026-07-30/item279/panel/fitter_control.py       4ce3e39   <- the ruled fitter, N3
session_2026-07-30/item279/panel/fitter_distfirst.py     a7bde8b
session_2026-07-30/item279/panel/fitter_loclin.py        24a9884
session_2026-07-30/item279/panel/fitter_powerspine.py    ca5b05b
session_2026-07-30/item279/panel/pooled_numeraire.py     edaf783   <- the ruled pin policy, N4/N14
session_2026-07-30/item279/out/per_entrant_279_vor.json  193f24f   <- md5 77eba4d3, the round-trip input
```

The three non-ruled fitters travel because `pooled_numeraire`'s confirmation-condition block iterates all four (`control`, `loclin`, `powerspine`, `distfirst`) and halts without them. They are the panel's controls, not alternatives in play: **N3 rules the fitter is CONTROL.**

**NOT carried, deliberately:** `session_2026-07-30/item279/out/ruled_curve_final_279.json`. Installing the stop-point curve is **L1(b)'s act**, under its own enumerated identity set (Addendum C.3). Placing it here would pre-empt L1 and put a curve artifact on the carrier outside that set. The HOLD on `claude/pre-referee-baseline-shaping-4ql38z` stands unchanged.

**`derive_271.py` NOT changed, and the reason stated rather than left silent.** `session_2026-07-29/item271/derive_271.py:64` builds its year-0 point from raw `r['v0']` at unit weight and fits with `fit_year0` — a time-kernel fit, not the ruled `control` + pooled-numeraire construction. Editing it to consume structural values would author a **different** curve under a fitter **N3 does not rule**. It is the older #271 derivation and it is left alone. The ruled lane is the one carried above.

## FINDINGS DOCKETED

1. **The reachability class has now fired three times** — v0surf bytes, the ND matrix, and now the whole derivation lane. The generalised freeze law already covers it (*an instrument's input is committed, or its emitter and substrate are both reachable*); what this instance adds is that **the law must cover the instrument as well as the input**. For L5.
2. **The lane's pins are path-selected.** `import harness_pvc` decides which pins apply. The `load_matrix` assert makes a wrong pairing loud, so this is a footgun with a working guard rather than a defect — but the guard is the only thing standing between two same-named files. For L5.
3. **The round trip's own input is reachable only from a HOLD branch** until L1 lands the stop-point artifacts. Carried here as `per_entrant_279_vor.json` precisely so the regression does not depend on a branch surviving. Named, not assumed away.

## COSTS

| act | measured |
|---|---|
| `carry_verify.sh` end-to-end (A + B + C) | **3s** |
| the lane, one derivation pass | **1s** |
| engine acts | **none** — this leg touches no bake, no board, no book |

Every run behind `tools/preboot_assert.sh`, serial, PASS each time.

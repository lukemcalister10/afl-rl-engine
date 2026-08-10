# THE SITTER ACT (RULING 2.7) INSTRUMENTS — landed 2026-08-10

The cross-section of the year-1 SITTER cohort — the entrants who played zero games in their
first season. #334 landing comment **5235734225**; QC comment **5235830131**; brief 5235660463.

## CLASSIFIED BY CONTENT, NOT BY PREFIX

The brief that ordered this landing guessed the sitter instruments were the `an*.py` series.
**They are not.** All thirteen `an*.py` read `decomp_b.json` / `live.json` and reproduce the
mark-up trace's steps — they are landed under `markup_trace_2026-08-10/`.

The sitter act's instruments are `xsec.py … xsec5.py`. Every one of them opens the same
cohort filter, which is SITTER_PROGRESS.md step 5 verbatim:

    S = [r for r in recs if r['type']=='ND' and 2004<=r['year']<=2022
         and r.get('pick') and 1<=r['pick']<=64 and r['games_yr1']==0]      # n = 496

## PATH CONVENTION

All five scripts hard-code the absolute scratchpad path
`/tmp/.../scratchpad/matrix.json` and read `['recs']` from it. There are no other inputs and
no engine load — this act is pure arithmetic on a committed matrix.

`matrix.json` (md5 `b564b12e533119f49c2c6bb0c92a5d91`, 3.4 MB) is the **stage4_amend1
per-entrant matrix**, byte-identical to the scratchpad's `s4a1.json` / `stage4a1.json` /
`pe338.json`. It is NOT on main. It lives on origin branch `landing/334-stage-b` at

    docs/evidence/act_334B_2026-08-07/stage4_amend1/noarb/per_entrant_338_stage4a1.json

To re-run: fetch that branch, copy the file to `matrix.json` under your scratchpad root (or
edit the single path constant at the top of each script), then run in numeric order.

## THE INSTRUMENT

Discount `H = 1.0939`. Weight `_w = vpath[0]` (the year-1 price). Outcome `_o = vpath[3]/H^3`
(realized value at career year 4, discounted back to the year-1 evaluation point; busts score
0 in the numerator and stay in the denominator). `F = sum(_o)/sum(_w)` — a ratio of sums, not
a mean of ratios. The three brief anchors reproduce: 27.2% never play, median peak/v0 = 0.745,
aggregate F = 0.984.

The F8 bar applied throughout: **eff-n >= 35 AND a bootstrap CI clear of 1.**

## KEY FILES

- `xsec.py` — the base cross-section: cohort build, the `_w`/`_o` weights, never-played rate.
- `xsec2.py` — the position / pick-band / era / age cuts and the contrasts, plus tail
  concentration (`_np` = never played, `_g2` = year-2 games).
- `xsec3.py` — the year-2 dose-response and quality terciles: `_g2` games and `_a2` (the
  year-2 season average, read off `r['seasons']`).
- `xsec4.py` — the horizon check. `Fh(rows, base, hor)` re-evaluates F at an arbitrary base
  and horizon, which is what distinguishes a real sitter effect from a maturity artifact;
  B=8000 bootstrap; key-position (`KPD/KPF/RUCK`) split.
- `xsec5.py` — era sub-windows, the final robustness pass (B=8000), **and the live exposure**:
  the same cohort filter re-pointed at entry classes 2023-2025 (the 74 current sitters), the
  directional movement on the live book from applying the measured KPP/SMALL cell factors as
  a pure scaling of the sit-charge, and the second-sit live set (2023-24 entrants who sat both
  year 1 and year 2 — the F8-clear over-price).
- `SITTER_PROGRESS.md` — the act's own step log (steps 1-12).

Seeds are fixed per script (20260810 / 20260810 / 7 / 11 / 3) so every published interval is
reproducible exactly.

## WHAT THIS ACT DID NOT WRITE

No `.txt`/`.json` outputs exist for this set: all five scripts print to stdout and the seat
read them there. Nothing was dropped in the landing — there is nothing else to land.

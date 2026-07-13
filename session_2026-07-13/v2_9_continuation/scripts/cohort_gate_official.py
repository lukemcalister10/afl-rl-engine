#!/usr/bin/env python3
"""OFFICIAL G-COHORT gate — verbatim reuse of ship_gates_check.py `_b1_rows` on a matrix path.

This is the AUDITED harness the v2.9 continuation adopts (directive item 1). The construction is
NOT re-derived here: `_b1_rows` below is a byte-for-byte copy of ship_gates_check.py:278-295 (the
shipped B1 gate, owner ruling D5). It reads a walk-forward matrix produced by the official pricer
`s4_matrix_M1v7.py` (gate mode) and computes:

  population : incurve (type in {ND,RD}) AND draft cohort 2004..2020
  per cohort : class-year SUM of Vpath at each depth N (N=1 is end of calendar Yr1 = C+1)
  index      : each cohort normalised to its own Yr1 (=100)  -> denominator = min(y1,y2)=y1
  avg row    : UNWEIGHTED cross-cohort simple mean at each depth (cohorts observed at that depth)

The G-COHORT law (CONSTRAINTS, directive): y4/y5/y6 EACH <= 130 (hard; guide 120-125).

usage: cohort_gate_official.py <matrix.json> [label]
"""
import sys, json
import numpy as np


def _b1_rows(mpath):
    """VERBATIM from ship_gates_check.py:278-295 — do not edit; this IS the official gate."""
    _m = json.load(open(mpath)); _S = {}
    for _k, _v in _m.items():
        if _k.startswith('__'):
            continue
        _C = int(_v['year'])
        if not _v['incurve'] or not (2004 <= _C <= 2020):
            continue
        for _i, _yy in enumerate(_v['yrs']):
            _N = _i + 1
            if _N > 7:
                break
            _S[(_C, _N)] = _S.get((_C, _N), 0.0) + float(_v['Vpath'][_i] or 0.0)
    _co = sorted({c for c, _ in _S})
    _R = {C: {N: 100.0 * _S[(C, N)] / max(_S[(C, 1)], 1e-9) for N in range(1, 8) if (C, N) in _S} for C in _co}
    _AVG = {N: float(np.mean([_R[C][N] for C in _co if N in _R[C]])) for N in range(1, 8) if any(N in _R[C] for C in _co)}
    return _R, _AVG, _co


def report(mpath, label):
    R, AVG, cohorts = _b1_rows(mpath)
    meta = json.load(open(mpath)).get('__meta__', {})
    ratios = {t: AVG.get(t) for t in (4, 5, 6)}
    breach = {t: (ratios[t] is not None and ratios[t] > 130.0) for t in (4, 5, 6)}
    ppk = max(AVG, key=AVG.get)
    path_ok = all(AVG[N + 1] >= 0.95 * AVG[N] for N in range(1, ppk) if N + 1 in AVG)
    out = dict(
        label=label, matrix=mpath,
        engine_head_md5=meta.get('engine_head_md5', '?')[:8], store_md5=meta.get('store_md5', '?')[:8],
        config_sha256=(meta.get('config_sha256') or '-')[:12], n_players=meta.get('n_players'),
        cohorts=cohorts, n_cohorts=len(cohorts),
        avg_row={N: round(AVG[N], 1) for N in sorted(AVG)},
        y4=round(AVG[4], 1) if 4 in AVG else None,
        y5=round(AVG[5], 1) if 5 in AVG else None,
        y6=round(AVG[6], 1) if 6 in AVG else None,
        peak_N=ppk, peak_val=round(AVG[ppk], 1), path_ok=path_ok,
        margin_y4=round(130.0 - AVG[4], 1) if 4 in AVG else None,
        margin_y5=round(130.0 - AVG[5], 1) if 5 in AVG else None,
        margin_y6=round(130.0 - AVG[6], 1) if 6 in AVG else None,
        breach_130=breach, any_breach=any(breach.values()),
    )
    per_cohort = {C: {N: round(R[C][N], 1) for N in sorted(R[C])} for C in cohorts}
    return out, per_cohort


if __name__ == "__main__":
    mpath = sys.argv[1]
    label = sys.argv[2] if len(sys.argv) > 2 else "matrix"
    out, per_cohort = report(mpath, label)
    print(f"=== OFFICIAL G-COHORT (B1 _b1_rows verbatim) | {label} ===")
    print(f"  engine {out['engine_head_md5']} store {out['store_md5']} config {out['config_sha256']} n_players={out['n_players']}")
    print(f"  cohorts (2004-2020, incurve ND+RD): n={out['n_cohorts']} {out['cohorts']}")
    print(f"  AVG row (indexed yr1=100): " + " ".join(f"{N}:{out['avg_row'][N]}" for N in sorted(out['avg_row'])))
    print(f"  y4={out['y4']}  y5={out['y5']}  y6={out['y6']}  (hard 130; guide 120-125)")
    print(f"  margins vs 130: y4={out['margin_y4']}  y5={out['margin_y5']}  y6={out['margin_y6']}")
    print(f"  peak N={out['peak_N']} val={out['peak_val']} path_ok={out['path_ok']}")
    print(f"  GATE: {'BREACH' if out['any_breach'] else 'PASS'}  {out['breach_130']}")
    if len(sys.argv) > 3:
        json.dump({"summary": out, "per_cohort": per_cohort}, open(sys.argv[3], "w"), indent=1)
        print(f"  wrote {sys.argv[3]}")

"""LEG-D ACT-2 — THE PVC RE-DERIVATION (offline, stamped, LOADED not refit).

Implements the OWNER-RULED R1 — THE COMPOSED PATHWAY CONSTRUCTION:

    PVC(p) = Sum_pos P(position | pick p) * E[pathway value | position, pick p]
           = the YEAR-0 point of the fitted 2-D (pick x career-year) trajectory surface.

- Pathway values come from realized career TRAJECTORIES: the walk-forward as-of values
  (`vpath`, end of years 1,2,3,...) plus the year-0 day-after value (`v0`), over the
  2004-2024 in-curve pool (ND/RD, real pick). Source = per_entrant.json, emitted on base
  968de0c7 by emit_matrix.py (verbatim engine quantities; nothing re-invented here).
- BUSTS at REAL outcomes, FULL WEIGHT: no survivor pool, no games floor, no threshold. Every
  entrant is IN (L-SMOOTH / weight-don't-gate BIND).
- CONTINUOUS evidence weighting: each career-year point is weighted by its evidence share
  es = 1 - (pw-PW_FLOOR)/(1-PW_FLOOR), where pw is the engine's prior-share weight (1.0 at
  zero football evidence -> PW_FLOOR=0.11 evidence-rich). A prior-dominated (circular) year
  fades smoothly toward 0; never a cutoff. The year-0 datum carries the entry weight 1.0.
- Fit: per-EXACT-pick, kernel-smoothed NON-MEDIAN (weighted MEAN). Gaussian kernel over
  log-pick, adaptive bandwidth grown until local eff-n >= NMIN (widens into the sparse tail);
  one-sided time kernel exp(-t/TAU) centred at year 0 lets the development pathway inform the
  year-0 slice by a small, G-Y0-bounded amount. The pooled per-pick sample carries the natural
  position mix, so the pooled fit IS composition-weighted (the explicit per-position
  decomposition is emitted for the item-256 ledgers).
- PVC(p) = year-0 point. Isotonic non-increasing (PAVA) + strict-descent epsilon (R104.9, all
  plateaus cleared) + numeraire pin curve(1)=3000 (L7 re-base).
- ENTRY CLOSURE: a zero-evidence entrant's v0_start becomes _PVC0[pick] == this curve once
  loaded; asserted in one_source_selftest.py (not here).

Also builds the NAMED FALLBACK, memo option C (two-ends continuous blend), far enough to COMMIT
the R1-vs-C comparison (job5_r1_vs_c.json). C rules ONLY if R1 cannot satisfy the constraints.

STAMPED: curve_md5 + a source stamp over (store md5, per_entrant md5, this-script md5, config).
LOADED not refit: nothing here runs at engine import; _merged_recover.py loads the artifact.

Usage:  python3 derive_pvc2.py [--tau TAU] [--nmin NMIN] [--label LABEL] [--out FILE]
        (defaults are the shipped derivation; --tau/--nmin drive the multi-start test.)
"""
import os, sys, io, json, hashlib, argparse
import numpy as np

BASE = '/home/user/afl-rl-engine/session_2026-07-17/legd_derivation'
ENG  = '/home/user/afl-rl-engine/engine/rl_after'
STORE = ENG + '/rl_model_data.json'
PER   = BASE + '/out/per_entrant.json'

PW_FLOOR = 0.11            # engine residual prior weight (_ev_pw floor; emit_matrix.py header)
KMIN, KMAX = 1, 99         # curve key range (matches pvc_curve_L1b.json exactly)
PIN1 = 3000                # numeraire (owner-set; RL_PICK1)

def md5(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()

def pava_ni(vals, wts):
    """Non-increasing weighted isotonic regression (PAVA). Returns fitted array."""
    n = len(vals)
    v = [float(x) for x in vals]; w = [float(x) for x in wts]
    stackv = []; stackw = []; stackn = []
    for j in range(n):
        cv, cw, cn = v[j], w[j], 1
        while stackv and stackv[-1] < cv - 1e-12:   # previous block lower than current -> violates non-increasing
            pv, pw_, pn = stackv.pop(), stackw.pop(), stackn.pop()
            cv = (pv * pw_ + cv * cw) / (pw_ + cw); cw = pw_ + cw; cn = pn + cn
        stackv.append(cv); stackw.append(cw); stackn.append(cn)
    out = []
    for bv, bn in zip(stackv, stackn):
        out += [bv] * bn
    return np.array(out)

def load_pool():
    recs = json.load(open(PER))
    P = [r for r in recs if r['incurve'] and r['pick'] and 2004 <= r['year'] <= 2024 and r['v0']]
    return P

def build_points(P, drop_poles=False):
    """Return arrays (logpick, tyear, value, weight, pos) for the 2-D fit.
    t=0 -> v0 (weight 1.0); t=k -> vpath[k-1] (weight = evidence_share(pw_k), poles kept)."""
    lp, ty, val, wt, pos = [], [], [], [], []
    for r in P:
        L = np.log(r['pick'])
        is_pole = (r['games_yr1'] == 0)
        # year-0 datum (the day-after value; the entry anchor) — ALWAYS kept, incl. poles: the entry end uses
        # their day-after V0 for the floor BY DESIGN (audit #44 removes poles only from the EVIDENCE end below).
        lp.append(L); ty.append(0); val.append(r['v0']); wt.append(1.0); pos.append(r['pos'])
        # career-year data (walk-forward as-of), continuous evidence weighting
        pw = r.get('pw', {}); vp = r.get('vpath', [])
        for k in range(1, len(vp) + 1):
            v = vp[k - 1]
            if v is None: continue
            pwk = pw.get(str(k))
            if pwk is None:
                pwk = pw.get(str(min(k, 6)), 1.0)      # pw only emitted k=1..6; reuse last for deeper years
            es = max(0.0, 1.0 - (pwk - PW_FLOOR) / (1.0 - PW_FLOOR))
            if drop_poles and is_pole:                 # prior-removed test: zero the poles on the evidence end
                es = 0.0
            if es <= 0: continue
            lp.append(L); ty.append(k); val.append(v); wt.append(es); pos.append(r['pos'])
    return (np.array(lp), np.array(ty, float), np.array(val, float), np.array(wt, float), np.array(pos))

def fit_year0(points, tau, nmin, hmin=0.10, hmax=0.60):
    """2-D NW fit read at the year-0 slice. Non-median (weighted mean).
    curve_raw(p) = Sum_i K_pick(logp-logp_i;h(p)) * K_time(t_i;tau) * w_i * val_i / Sum(.)

    The adaptive pick-bandwidth h(p) is determined from the YEAR-0 (t=0) sample ONLY, so the
    smoothing width is independent of tau (the time-kernel width). tau then controls the pathway's
    (career-year) influence on the year-0 slice MONOTONICALLY: tau->0 => pure day-after-V0 year-0
    slice (the gate anchor); larger tau => more trajectory credit, bounded by the G-Y0 gate."""
    lp, ty, val, wt, _ = points
    t0 = (ty == 0)
    lp0 = lp[t0]                                        # year-0 (v0) sample drives the bandwidth
    tw = wt * np.exp(-ty / tau)                         # full time-kerneled weight (t=0 -> 1.0)
    grid = list(range(KMIN, KMAX + 1))
    raw, effn = [], []
    for p in grid:
        Lp = np.log(p)
        h = hmin                                        # grow h until the year-0 local eff-n >= nmin
        while h < hmax:
            if np.sum(np.exp(-0.5 * ((lp0 - Lp) / h) ** 2)) >= nmin: break
            h += 0.02
        W = np.exp(-0.5 * ((lp - Lp) / h) ** 2) * tw
        raw.append(float(np.sum(W * val) / np.sum(W)))
        effn.append(float(np.sum(np.exp(-0.5 * ((lp0 - Lp) / h) ** 2))))
    return grid, np.array(raw), np.array(effn)

def monotone_strict(grid, raw, effn):
    """PAVA non-increasing (weighted by eff-n) then strict-descent epsilon; pin(1)=PIN1."""
    fit = pava_ni(raw, effn)
    # pin pick-1 to the numeraire; keep pick>=2 strictly below, preserving shape
    fit = fit.copy()
    fit[0] = PIN1
    # ensure strictly decreasing with a minimal epsilon where flat/rising
    EPS = 1e-3
    for i in range(1, len(fit)):
        if fit[i] >= fit[i - 1] - EPS:
            fit[i] = fit[i - 1] - EPS
    # round to integers (curve currency), then re-enforce strict descent on the integer grid
    ic = [int(round(x)) for x in fit]
    ic[0] = PIN1
    for i in range(1, len(ic)):
        if ic[i] >= ic[i - 1]:
            ic[i] = ic[i - 1] - 1
    return ic

def gy0_pooled(P, curve):
    """Offline G-Y0: comp-weighted per-pick mean v0 vs curve. Pooled net + mean-rel + per-pick residual."""
    from collections import defaultdict
    byp = defaultdict(list)
    for r in P: byp[r['pick']].append(r['v0'])
    cur = {p: curve[p - 1] for p in range(KMIN, KMAX + 1)}
    picks = sorted(byp)
    num = sum(len(byp[p]) * (np.mean(byp[p]) - cur[p]) for p in picks)
    den = sum(len(byp[p]) * cur[p] for p in picks)
    pooled_net = 100.0 * num / den
    mean_rel = 100.0 * np.mean([(r['v0'] - cur[r['pick']]) / cur[r['pick']] for r in P])
    per_pick = {p: dict(n=len(byp[p]), meanV0=round(float(np.mean(byp[p])), 1),
                        curve=cur[p], resid=round(float(np.mean(byp[p]) - cur[p]), 1),
                        rel_pct=round(100.0 * (np.mean(byp[p]) - cur[p]) / cur[p], 2))
                for p in picks}
    return dict(pooled_net_pct=round(pooled_net, 3), pooled_abs_pct=round(abs(pooled_net), 3),
                mean_rel_pct=round(mean_rel, 3), per_pick=per_pick)

# ---------------- memo option C (two-ends continuous blend) — the NAMED FALLBACK ----------------
def build_memo_c(P):
    """C: entry end = day-after pole pricing (dominant where evidence thin); evidence end = life-path
    production up-weighted by faded-prior share; PVC = continuous evidence-weighted blend. Built to
    COMMIT the comparison, not to ship (R1 is the ruled construction)."""
    from collections import defaultdict
    lp_e, val_e, w_e = [], [], []      # entry end (v0, weight = prior share = pw1)
    lp_v, val_v, w_v = [], [], []      # evidence end (life-path peak-window, weight = evidence share)
    for r in P:
        L = np.log(r['pick'])
        pw1 = r['pw'].get('1', 1.0)
        lp_e.append(L); val_e.append(r['v0']); w_e.append(pw1)             # entry end dominant when prior-heavy
        vp = [v for v in r.get('vpath', []) if v is not None]
        if vp:
            # life-path evidence end: mean over the realized path (credits development), evidence weight
            es = max(0.0, 1.0 - (r['pw'].get('1', 1.0) - PW_FLOOR) / (1.0 - PW_FLOOR))
            lp_v.append(L); val_v.append(float(np.mean(vp))); w_v.append(es)
    lp_e, val_e, w_e = map(np.array, (lp_e, val_e, w_e))
    lp_v, val_v, w_v = map(np.array, (lp_v, val_v, w_v))
    grid = list(range(KMIN, KMAX + 1)); raw = []
    for p in grid:
        Lp = np.log(p); h = 0.22
        ke = np.exp(-0.5 * ((lp_e - Lp) / h) ** 2) * w_e
        kv = np.exp(-0.5 * ((lp_v - Lp) / h) ** 2) * w_v
        ee = np.sum(ke * val_e) / np.sum(ke)
        ve = np.sum(kv * val_v) / np.sum(kv) if np.sum(kv) > 0 else ee
        # continuous blend weight = local evidence share at this pick
        alpha = np.sum(kv) / (np.sum(kv) + np.sum(ke))
        raw.append((1 - alpha) * ee + alpha * ve)
    effn = np.ones(len(grid))
    return monotone_strict(grid, np.array(raw), effn)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tau', type=float, default=0.12)    # time-kernel bandwidth (pathway influence; gate-bounded)
    ap.add_argument('--nmin', type=float, default=35.0)   # adaptive-bw target eff-n
    ap.add_argument('--label', default='shipped')
    ap.add_argument('--out', default=ENG + '/pvc_curve_v2.json')
    ap.add_argument('--drop-poles', action='store_true')  # audit #44 prior-removed
    ap.add_argument('--emit-diag', action='store_true')
    args = ap.parse_args()

    P = load_pool()
    pts = build_points(P, drop_poles=args.drop_poles)
    grid, raw, effn = fit_year0(pts, tau=args.tau, nmin=args.nmin)
    curve = monotone_strict(grid, raw, effn)

    # gates (offline)
    gy0 = gy0_pooled(P, curve)
    strict_ok = all(curve[i] < curve[i - 1] for i in range(1, len(curve)))
    pin_ok = (curve[0] == PIN1)

    cfg = dict(tau=args.tau, nmin=args.nmin, pw_floor=PW_FLOOR, pin1=PIN1,
               kmin=KMIN, kmax=KMAX, drop_poles=args.drop_poles, label=args.label)
    stamp = dict(store_md5=md5(STORE)[:8], per_entrant_md5=md5(PER)[:8],
                 script_md5=md5(os.path.abspath(__file__))[:8], config=cfg)
    curve_dict = {str(p): int(curve[p - 1]) for p in range(KMIN, KMAX + 1)}
    curve_md5 = hashlib.md5(json.dumps(curve_dict, sort_keys=True).encode()).hexdigest()[:8]

    out = dict(
        curve=curve_dict, pin=PIN1,
        source='derive_pvc2.py — R1 COMPOSED PATHWAY construction (year-0 point of the 2-D '
               'pick x career-year evidence-weighted NON-median fit; busts full weight, no threshold)',
        construction='R1_composed_pathway', derived_from='out/per_entrant.json (base 968de0c7)',
        curve_md5=curve_md5, stamp=stamp,
        gate='RL_PVC2 (parallel of RL_PVCADOPT). RL_PVC2=0 => _PVC0 stays L1b => board 9829d01a byte-exact.',
        gy0_offline=dict(pooled_abs_pct=gy0['pooled_abs_pct'], mean_rel_pct=gy0['mean_rel_pct']),
        r104_9_strict_descent=strict_ok, numeraire_pin1_3000=pin_ok,
        note='LOADED not refit; the _iso_dec/_fit_pick_curve import-time chain is untouched. Candidate ONLY.',
    )
    json.dump(out, open(args.out, 'w'), indent=1)
    print(f"[{args.label}] tau={args.tau} nmin={args.nmin} -> {args.out}")
    print(f"  curve[1,2,3,10,50,80,99] = {[curve[p-1] for p in (1,2,3,10,50,80,99)]}")
    print(f"  curve_md5={curve_md5}  strict_descent={strict_ok}  pin1==3000={pin_ok}")
    print(f"  G-Y0 offline: pooled |net| = {gy0['pooled_abs_pct']}%  mean-rel = {gy0['mean_rel_pct']}%  (HARD <= 2%)")
    if args.emit_diag:
        json.dump(gy0, open(BASE + '/out/gy0_v2_perpick.json', 'w'), indent=1)
        print("  wrote out/gy0_v2_perpick.json")
    return out, gy0, strict_ok, pin_ok

if __name__ == '__main__':
    main()
